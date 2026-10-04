#!/usr/bin/env python3
"""Add LAN viewing and a password-protected native dashboard without changing gateway ownership."""
from pathlib import Path
import json
import os
import secrets
import subprocess
import sys
import urllib.request

root = Path(__file__).resolve().parent.parent
current = json.load(urllib.request.urlopen('http://127.0.0.1:9999/api/state', timeout=5))
if any(job['status'] in ('running', 'owner unavailable') for job in current['jobs']):
    raise SystemExit('A coordinator trial is active or unresolved; wait before restarting its owner.')
runtime = Path.home() / '.hermes/hermes-agent'
sys.path.insert(0, str(runtime))
from plugins.dashboard_auth.basic import hash_password

host = '192.168.8.174'
state = root / 'state/coordinator'
state.mkdir(parents=True, exist_ok=True)
private = Path.home() / '.hermes/runtime'
private.mkdir(parents=True, exist_ok=True)
env = private / 'pstack-dashboard.env'
login = private / 'pstack-dashboard-login.txt'
if not env.exists():
    password = secrets.token_urlsafe(18)
    env.write_text('HERMES_DASHBOARD_BASIC_AUTH_USERNAME=hermes\n'
                   f'HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH={hash_password(password)}\n'
                   f'HERMES_DASHBOARD_BASIC_AUTH_SECRET={secrets.token_urlsafe(48)}\n'
                   f'HERMES_DASHBOARD_PUBLIC_URL=http://{host}:9119\n')
    login.write_text('Username: hermes\nPassword: ' + password + '\n')
    env.chmod(0o600)
    login.chmod(0o600)
units = Path.home() / '.config/systemd/user'
unit = units / 'pstack-coordinator.service'
old = unit.read_text()
if f'{root}/coordinator/server.py' not in old:
    raise SystemExit('Coordinator service is not owned by this clone; preserve it.')
new = old.replace('--port 9999\n', f'--port 9999 --bind 0.0.0.0 --allow-host {host}:9999\n')
unit.write_text(new)
native = units / 'pstack-hermes-dashboard.service'
content = f'''[Unit]
Description=Hermes native browser dashboard with password authentication
After=network.target

[Service]
Type=simple
WorkingDirectory={runtime}
EnvironmentFile={env}
ExecStart=/home/hermes/.local/bin/hermes dashboard --host 0.0.0.0 --port 9119 --skip-build --no-open
Restart=on-failure
RestartSec=5
UMask=0077

[Install]
WantedBy=default.target
'''
if native.exists() and native.read_text() != content:
    raise SystemExit('Existing dashboard service differs; preserve it.')
native.write_text(content)
sites = [
    {'name': 'Coordinator & subagent observer', 'status': 'live',
     'description': 'Actual worker start/stop receipts, delegation records, sessions, native task metadata and pstack trial evidence. Home-network viewing is read-only.',
     'links': [{'label': 'Home network', 'url': f'http://{host}:9999/'},
               {'label': 'Workers', 'url': f'http://{host}:9999/#workers'},
               {'label': 'Tasks', 'url': f'http://{host}:9999/#tasks'},
               {'label': 'This computer (SSH tunnel)', 'url': 'http://localhost:9999/'}]},
    {'name': 'Native Hermes dashboard', 'status': 'password login',
     'description': 'The existing Hermes browser UI: chat, sessions, skills, plugins, models, schedules and settings. Native embedded chat handles its own live worker display.',
     'links': [{'label': 'Home network', 'url': f'http://{host}:9119/'},
               {'label': 'Sessions', 'url': f'http://{host}:9119/sessions'},
               {'label': 'Native Kanban', 'url': f'http://{host}:9119/kanban'},
               {'label': 'Chat', 'url': f'http://{host}:9119/chat'},
               {'label': 'Skills', 'url': f'http://{host}:9119/skills'}]},
    {'name': 'Browser editor (code-server)', 'status': 'already live',
     'description': 'Existing browser editor and terminal on Hermes. This is an editor, not an agent coordinator.',
     'links': [{'label': 'Home network', 'url': f'http://{host}:8080/'}]},
    {'name': 'Original pstack adoption board', 'status': 'local viewer',
     'description': 'Static feature inventory. Its adoption map is also available inside the network coordinator under Stack adoption.',
     'links': [{'label': 'This computer (SSH tunnel)', 'url': 'http://localhost:18765/'},
               {'label': 'Network adoption view', 'url': f'http://{host}:9999/#adoption'}]},
    {'name': 'Hindsight memory API', 'status': 'internal API',
     'description': 'Internal memory service on Hermes localhost:8888. It is not a general agent/coordinator website.', 'links': []},
]
(state / 'access.local.json').write_text(json.dumps({'sites': sites}, indent=2))
subprocess.run(['systemd-analyze', '--user', 'verify', str(unit), str(native)], check=True)
subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
subprocess.run(['systemctl', '--user', 'restart', 'pstack-coordinator.service'], check=True)
subprocess.run(['systemctl', '--user', 'enable', '--now', 'pstack-hermes-dashboard.service'], check=True)
print('LAN coordinator and authenticated native dashboard services configured.')
print('New dashboard login is stored privately at ' + str(login))
