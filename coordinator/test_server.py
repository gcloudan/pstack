"""Behavioral checks for read-only snapshots and the coordinator request boundary."""
from pathlib import Path
import importlib.util
import json
import sqlite3
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from contextlib import closing

spec = importlib.util.spec_from_file_location('coordinator_server', Path(__file__).with_name('server.py'))
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.old_home, self.old_state = server.HOME, server.STATE
        server.HOME = self.home
        server.STATE = self.home / 'trial-state'

    def tearDown(self):
        server.HOME, server.STATE = self.old_home, self.old_state
        self.temp.cleanup()

    def test_snapshot_bounds_hides_records_and_omits_sensitive_columns(self):
        path = self.home / 'state.db'
        with closing(sqlite3.connect(path)) as con:
            con.execute('CREATE TABLE sessions(id TEXT,source TEXT,hidden INTEGER,last_activity_at INTEGER,system_prompt TEXT,model_config TEXT)')
            con.executemany('INSERT INTO sessions VALUES(?,?,?,?,?,?)', [
                (str(i), 'cli', int(i == 99), i, 'PRIVATE_PROMPT_SENTINEL', 'SECRET_CONFIG_SENTINEL') for i in range(100)])
            con.commit()
        before = path.read_bytes()
        result = server.snapshot()
        self.assertEqual(len(result['sessions']), 80)
        self.assertEqual(result['sessions'][0]['id'], '98')
        serialized = json.dumps(result)
        self.assertNotIn('PRIVATE_PROMPT_SENTINEL', serialized)
        self.assertNotIn('SECRET_CONFIG_SENTINEL', serialized)
        self.assertNotIn('system_prompt', serialized)
        self.assertEqual(path.read_bytes(), before)
        self.assertIsNotNone(result['errors']['tasks'])

    def test_missing_or_changed_schema_is_unavailable_not_empty_success(self):
        rows, error = server.records(self.home / 'missing.db', 'sessions', ['id'])
        self.assertEqual(rows, [])
        self.assertIsNotNone(error)
        self.assertFalse((self.home / 'missing.db').exists())
        path = self.home / 'empty.db'
        with closing(sqlite3.connect(path)):
            pass
        rows, error = server.records(path, 'sessions', ['id'])
        self.assertEqual(rows, [])
        self.assertIsNotNone(error)

    def test_named_boards_are_visible_even_when_default_is_empty(self):
        for board, task in [('default', None), ('life-ops', 'existing-task')]:
            path = self.home / ('kanban.db' if board == 'default' else 'kanban/boards/life-ops/kanban.db')
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as con:
                con.execute('CREATE TABLE tasks(id TEXT,status TEXT,title TEXT)')
                if task:
                    con.execute('INSERT INTO tasks VALUES(?,?,?)', (task, 'ready', 'PRIVATE_TITLE'))
                con.commit()
        result = server.snapshot()
        self.assertEqual(result['tasks'], [{'id': 'existing-task', 'status': 'ready', 'board': 'life-ops'}])
        self.assertNotIn('PRIVATE_TITLE', json.dumps(result))

    def test_open_record_does_not_become_running_job(self):
        server.STATE.mkdir()
        job = {'id': 'prior-owner', 'status': 'running', 'kind': 'walkthrough'}
        (server.STATE / 'prior-owner.json').write_text(json.dumps(job))
        result = server.jobs()[0]
        self.assertEqual(result['status'], 'owner unavailable')
        self.assertEqual(json.loads((server.STATE / 'prior-owner.json').read_text())['status'], 'running')

    def test_unresolved_prior_owner_blocks_a_second_launch(self):
        server.STATE.mkdir()
        (server.STATE / 'prior.json').write_text(json.dumps({'id': 'prior', 'status': 'running'}))
        with self.assertRaisesRegex(ValueError, 'ownership is unresolved'):
            server.launch('walkthrough')

    def test_newest_job_is_not_lost_by_uuid_filename_order(self):
        server.STATE.mkdir()
        for i in range(31):
            name = f'{31-i:032d}'
            (server.STATE / (name + '.json')).write_text(json.dumps({
                'id': name, 'status': 'completed', 'started_at': f'2026-01-{i+1:02d}T00:00:00Z'}))
        rows = server.jobs()
        self.assertEqual(len(rows), 30)
        self.assertEqual(rows[0]['started_at'], '2026-01-31T00:00:00Z')

    def test_native_millisecond_and_iso_job_timestamps_sort_together(self):
        server.STATE.mkdir()
        for name, stamp in [('native', 1791092176688), ('iso', '2026-01-01T00:00:00Z')]:
            (server.STATE / (name + '.json')).write_text(json.dumps({'id': name, 'status': 'completed', 'started_at': stamp}))
        self.assertEqual(server.jobs()[0]['id'], 'native')

    def test_http_blocks_cross_origin_and_arbitrary_hosts(self):
        http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        threading.Thread(target=http.serve_forever, daemon=True).start()
        base = f'http://127.0.0.1:{http.server_port}'
        try:
            def rejected(request, status):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request)
                self.assertEqual(caught.exception.code, status)
            rejected(urllib.request.Request(base + '/api/state', headers={'Host': 'foreign.example'}), 403)
            rejected(urllib.request.Request(base + '/api/trials/walkthrough', data=b''), 403)
            rejected(urllib.request.Request(base + '/api/trials/walkthrough', data=b'',
                headers={'Origin': 'http://foreign.example', 'X-Coordinator-Token': server.TOKEN}), 403)
            rejected(urllib.request.Request(base + '/api/trials/arbitrary-command', data=b'',
                headers={'Origin': base, 'X-Coordinator-Token': server.TOKEN}), 409)
            http.extra_hosts = (f'192.168.8.174:{http.server_port}',)
            lan_host = http.extra_hosts[0]
            bootstrap = json.load(urllib.request.urlopen(urllib.request.Request(base + '/api/bootstrap',
                headers={'Host': lan_host})))
            self.assertFalse(bootstrap['can_launch'])
            self.assertIsNone(bootstrap['token'])
            rejected(urllib.request.Request(base + '/api/trials/walkthrough', data=b'',
                headers={'Host': lan_host, 'Origin': 'http://' + lan_host,
                         'X-Coordinator-Token': server.TOKEN}), 403)
            self.assertFalse(server.STATE.exists())
        finally:
            http.shutdown()
            http.server_close()

if __name__ == '__main__':
    unittest.main()
