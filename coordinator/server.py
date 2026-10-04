#!/usr/bin/env python3
"""Loopback coordinator: read-only Hermes metadata and scoped disposable trials."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import argparse
import datetime
import json
import os
import secrets
import sqlite3
import subprocess
import threading
import time
import uuid
import hashlib
from contextlib import closing

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home() / '.hermes'
STATE = ROOT / 'state/coordinator'
TRIALS = {'walkthrough': 'pstack-how', 'delegation': 'pstack-how,pstack-swarm', 'impact': 'pstack-impact'}
LOCK = threading.RLock()
TOKEN = secrets.token_urlsafe(32)
PROCESSES = {}
HEALTH = {'at': 0, 'services': []}

def service_health():
    if time.monotonic() - HEALTH['at'] > 15:
        names = ['hermes-gateway.service', 'pstack-hermes-dashboard.service', 'hindsight.service']
        try:
            result = subprocess.run(['systemctl', '--user', 'is-active', *names],
                                    capture_output=True, text=True, timeout=2)
            states = result.stdout.splitlines()
            HEALTH['services'] = [{'name': name, 'state': states[i] if i < len(states) else 'unknown'}
                                  for i, name in enumerate(names)]
        except (OSError, subprocess.TimeoutExpired):
            HEALTH['services'] = [{'name': name, 'state': 'unknown'} for name in names]
        HEALTH['at'] = time.monotonic()
    return HEALTH['services']

def work_summary(tasks, links):
    visible = [task for task in tasks if task.get('status') != 'archived']
    counts = {status: sum(task.get('status') == status for task in visible)
              for status in ('running', 'ready', 'blocked', 'review', 'todo', 'done', 'triage', 'scheduled')}
    unassigned = sum(task.get('status') == 'ready' and not task.get('assignee') for task in visible)
    index = {(task.get('board'), task.get('id')): task for task in tasks}
    waiting = set()
    for edge in links:
        parent = index.get((edge.get('board'), edge.get('parent_id')))
        child = index.get((edge.get('board'), edge.get('child_id')))
        if parent and child and parent.get('status') != 'done' and child.get('status') == 'todo':
            waiting.add((edge.get('board'), edge.get('child_id')))
    return {'counts': counts, 'ready_without_owner': unassigned,
            'waiting_on_dependencies': len(waiting),
            'needs_attention': unassigned + counts['blocked'] + counts['review']}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read_json(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default

def records(db, table, fields, limit=60, order=None):
    if not db.is_file():
        return [], 'not present'
    try:
        # A normal URI mode=ro honors the current WAL. immutable=1 would miss live WAL writes.
        with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True, timeout=1)) as con:
            con.execute('PRAGMA query_only=ON')
            con.row_factory = sqlite3.Row
            columns = {r[1] for r in con.execute(f'PRAGMA table_info({table})')}
            selected = [f for f in fields if f in columns]
            if not selected:
                return [], 'table or supported metadata missing'
            ordering = f' ORDER BY {order} DESC' if order in columns else ''
            if table == 'sessions' and order == 'last_activity_at' and 'started_at' in columns:
                ordering = ' ORDER BY COALESCE(last_activity_at,started_at) DESC'
            visible = ' WHERE hidden=0' if table == 'sessions' and 'hidden' in columns else ''
            rows = con.execute(f'SELECT {",".join(selected)} FROM {table}{visible}{ordering} LIMIT ?', (limit,))
            return [dict(r) for r in rows], None
    except sqlite3.Error as exc:
        return [], type(exc).__name__

def observer_events():
    path = HOME / 'runtime/pstack-coordinator-events.jsonl'
    if not path.is_file():
        return [], 'Observer has not recorded events in fresh sessions yet.'
    try:
        # Bounded tail; never read transcripts or unrestricted runtime log files.
        with path.open('rb') as stream:
            stream.seek(0, 2)
            size = stream.tell()
            stream.seek(max(0, size - 131072))
            lines = stream.read().decode('utf-8', 'replace').splitlines()
        result = []
        for line in lines:
            try:
                result.append(json.loads(line))
            except ValueError:
                continue
        return result[-120:], None
    except OSError:
        return [], 'Observer log unavailable.'

def leases():
    data = read_json(HOME / 'runtime/active_sessions.json', {})
    result = []
    for item in data.get('entries', [])[:60]:
        pid = item.get('pid')
        alive = False
        if isinstance(pid, int) and pid > 0:
            try:
                os.kill(pid, 0)
                alive = True
            except (OSError, ProcessLookupError):
                pass
        result.append({k: item.get(k) for k in ('session_id', 'pid', 'surface', 'started_at', 'updated_at')}
                      | {'pid_alive': alive, 'evidence': 'registry lease; PID existence is not proof of an active turn'})
    return result

def stream_summary(path):
    if not path.is_file():
        return {'events': 0, 'tool_calls': 0, 'final': None, 'session_id': None}
    counters = {'events': 0, 'tool_calls': 0, 'final': None, 'session_id': None, 'tools': []}
    # Only our own disposable trial output. Do not expose arbitrary session messages.
    with path.open(errors='replace') as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            counters['events'] += 1
            if item.get('type') == 'tool_use':
                counters['tool_calls'] += 1
                name = item.get('name') or item.get('tool_name')
                if name and name not in counters['tools']:
                    counters['tools'].append(str(name))
            if item.get('type') == 'result':
                counters['final'] = str(item.get('text', ''))[-18000:]
                counters['session_id'] = item.get('session_id')
                counters['model_exit_code'] = item.get('exit_code')
                counters['tokens'] = item.get('tokens')
    return counters

def save_job(job):
    STATE.mkdir(parents=True, exist_ok=True)
    target = STATE / (job['id'] + '.json')
    tmp = target.with_suffix('.tmp')
    tmp.write_text(json.dumps(job, indent=2) + '\n')
    tmp.replace(target)

def process_identity(pid):
    try:
        # Linux start ticks disambiguate PID reuse without reading process environment.
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    except (OSError, IndexError):
        return None

def prior_process_exists(job):
    pid = job.get('pid')
    if not isinstance(pid, int) or pid <= 0:
        return None
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return None
    current = process_identity(pid)
    saved = job.get('process_start_ticks')
    return current == saved if current and saved else None

def job_records():
    return [job for path in STATE.glob('*.json') if (job := read_json(path, {})).get('id')]

def job_time(job):
    value = job.get('started_at')
    if isinstance(value, (int, float)):
        return value / 1000 if value > 100_000_000_000 else value
    try:
        return datetime.datetime.fromisoformat(str(value).replace('Z', '+00:00')).timestamp()
    except (ValueError, TypeError):
        return 0

def fixture_hashes():
    base = ROOT / 'adapters/hermes/trial-fixture'
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in base.iterdir() if p.is_file()}

def jobs():
    result = []
    for job in sorted(job_records(), key=job_time, reverse=True)[:30]:
        if job['status'] == 'running' and job['id'] not in PROCESSES:
            absent = prior_process_exists(job) is False
            job['status'] = 'interrupted' if absent else 'owner unavailable'
            job['note'] = ('Prior process is absent; completion was not verified.' if absent
                           else 'Server restarted; process ownership is unresolved. New trials are blocked.')
        job['stream'] = stream_summary(STATE / (job['id'] + '.jsonl'))
        result.append(job)
    return sorted(result, key=job_time, reverse=True)

def launch(kind):
    if kind not in TRIALS:
        raise ValueError('Unknown predefined trial')
    with LOCK:
        if any(p.poll() is None for p in PROCESSES.values()):
            raise ValueError('A coordinator trial is already running; shared fixture has one owner')
        for prior in job_records():
            if prior.get('status') == 'running' and prior['id'] not in PROCESSES:
                if prior_process_exists(prior) is not False:
                    raise ValueError('Prior trial ownership is unresolved; do not launch a second fixture owner')
                prior.update(status='interrupted', ended_at=now(), verification='Prior process absent; no successful completion claimed')
                save_job(prior)
        job = {'id': uuid.uuid4().hex, 'kind': kind, 'status': 'running', 'started_at': now(),
               'scope': 'disposable reminder fixture; investigation only',
               'verification': 'not assessed', 'fixture_commit': subprocess.check_output(
                   ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()}
        job['fixture_sha256'] = fixture_hashes()
        STATE.mkdir(parents=True, exist_ok=True)
        stdout = (STATE / (job['id'] + '.jsonl')).open('w')
        stderr = (STATE / (job['id'] + '.stderr')).open('w')
        cmd = [str(Path.home() / '.local/bin/hermes'), 'chat', '--oneshot', '--format', 'stream-json',
               '--query-file', str(ROOT / 'adapters/hermes/trials' / (kind + '.txt')),
               '--skills', TRIALS[kind], '--max-turns', '24', '--run-budget', '420',
               '--source', 'pstack-coordinator']
        try:
            process = subprocess.Popen(cmd, cwd=ROOT / 'adapters/hermes/trial-fixture',
                                       stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
        finally:
            stdout.close()
            stderr.close()
        job['pid'] = process.pid
        job['process_start_ticks'] = process_identity(process.pid)
        PROCESSES[job['id']] = process
        save_job(job)
        def finish():
            rc = process.wait()
            with LOCK:
                job.update(status='completed' if rc == 0 else 'failed', exit_code=rc, ended_at=now())
                job['fixture_unchanged'] = fixture_hashes() == job['fixture_sha256']
                job['verification'] = ('process exited; evidence review required' if job['fixture_unchanged']
                                       else 'Fixture changed during investigation; requires review')
                save_job(job)
        threading.Thread(target=finish, daemon=True).start()
        return job

def board_metadata():
    paths = [('default', HOME / 'kanban.db')]
    directory = HOME / 'kanban/boards'
    if directory.is_dir():
        for child in sorted(directory.iterdir()):
            if child.is_dir() and not child.is_symlink() and child.name.replace('-', '').replace('_', '').isalnum():
                paths.append((child.name, child / 'kanban.db'))
    tasks, links, runs, boards = [], [], [], []
    for name, path in paths[:30]:
        rows, error = records(path, 'tasks', [
            'id', 'assignee', 'status', 'priority', 'started_at', 'completed_at',
            'last_heartbeat_at', 'session_id', 'current_run_id'], order='created_at', limit=200)
        edges, _ = records(path, 'task_links', ['parent_id', 'child_id'], limit=200)
        attempts, _ = records(path, 'task_runs', [
            'id', 'task_id', 'profile', 'status', 'started_at', 'ended_at', 'last_heartbeat_at', 'outcome'],
            order='started_at')
        tasks.extend(dict(row, board=name) for row in rows)
        links.extend(dict(row, board=name) for row in edges)
        runs.extend(dict(row, board=name) for row in attempts)
        boards.append({'board': name, 'records': len(rows), 'error': error})
    return tasks, links, runs, boards

def snapshot():
    sessions, session_error = records(HOME / 'state.db', 'sessions', [
        'id', 'source', 'parent_session_id', 'started_at', 'ended_at',
        'last_activity_at', 'message_count', 'tool_call_count', 'model', 'input_tokens', 'output_tokens'],
        limit=80, order='last_activity_at')
    delegations, delegation_error = records(HOME / 'state.db', 'async_delegations', [
        'delegation_id', 'parent_session_id', 'state', 'dispatched_at', 'completed_at', 'updated_at', 'owner_pid'],
        order='updated_at')
    tasks, links, runs, boards = board_metadata()
    task_error = '; '.join(f"{b['board']}: {b['error']}" for b in boards if b['error']) or None
    events, observer_note = observer_events()
    return {'observed_at': now(), 'sessions': sessions, 'delegations': delegations, 'tasks': tasks,
            'links': links, 'task_runs': runs, 'boards': boards, 'leases': leases(), 'worker_events': events,
            'jobs': jobs(), 'receipt': read_json(ROOT / 'adapters/hermes/installation.local.json', {}),
            'work': work_summary(tasks, links), 'services': service_health(),
            'errors': {'sessions': session_error, 'delegations': delegation_error,
                       'tasks': task_error, 'observer': observer_note},
            'limits': ['Read-only selected metadata; no transcript bodies or credentials.',
                       'Recorded sessions and leases are not proof of an active model turn.',
                       'Worker observer applies to fresh plugin-enabled sessions.',
                       'A successful process exit still needs evidence review.']}

class Handler(BaseHTTPRequestHandler):
    def allowed_host(self):
        return self.headers.get('Host') in (f'localhost:{self.server.server_port}',
                                           f'127.0.0.1:{self.server.server_port}',
                                           *getattr(self.server, 'extra_hosts', ()))

    def local_control(self):
        return self.client_address[0] in ('127.0.0.1', '::1') and self.headers.get('Host') in (
            f'localhost:{self.server.server_port}', f'127.0.0.1:{self.server.server_port}')

    def send(self, status, content, kind='application/json'):
        data = content.encode() if isinstance(content, str) else json.dumps(content).encode()
        self.send_response(status)
        self.send_header('Content-Type', kind + '; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self.allowed_host():
            return self.send(403, {'error': 'Configured host required'})
        path = urlparse(self.path).path
        if path == '/':
            return self.send(200, (ROOT / 'coordinator/index.html').read_text(), 'text/html')
        if path == '/api/state':
            with LOCK:
                return self.send(200, snapshot())
        if path == '/api/bootstrap':
            return self.send(200, {'token': TOKEN if self.local_control() else None,
                                   'can_launch': self.local_control(), 'trials': list(TRIALS)})
        if path == '/api/access':
            return self.send(200, read_json(ROOT / 'state/coordinator/access.local.json', {'sites': []}))
        if path == '/api/adoption':
            return self.send(200, {'adoption': read_json(ROOT / 'adoption.json', {}),
                                   'receipt': read_json(ROOT / 'adapters/hermes/installation.local.json', {})})
        self.send(404, {'error': 'Not found'})

    def do_POST(self):
        expected_origin = 'http://' + self.headers.get('Host', '')
        if (not self.local_control() or self.headers.get('Origin') != expected_origin
                or not secrets.compare_digest(self.headers.get('X-Coordinator-Token', ''), TOKEN)):
            return self.send(403, {'error': 'Same-origin coordinator token required'})
        path = urlparse(self.path).path
        if path.startswith('/api/trials/'):
            try:
                return self.send(202, launch(path.removeprefix('/api/trials/')))
            except ValueError as exc:
                return self.send(409, {'error': str(exc)})
        self.send(404, {'error': 'Not found'})

    def log_message(self, fmt, *args):
        # Keep request logs free of payloads and titles.
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=9999)
    parser.add_argument('--bind', default='127.0.0.1')
    parser.add_argument('--allow-host', action='append', default=[], help='Additional exact host:port for read-only viewers')
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    server.extra_hosts = tuple(args.allow_host)
    print(f'Coordinator listening on http://{args.bind}:{args.port}', flush=True)
    server.serve_forever()
