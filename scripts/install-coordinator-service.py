#!/usr/bin/env python3
"""Install this clone's loopback coordinator as an additive Linux user service."""
from pathlib import Path
import os
import signal
import subprocess
import sys
import urllib.request
import json

root = Path(__file__).resolve().parent.parent
unit = Path.home() / '.config/systemd/user/pstack-coordinator.service'
if '\n' in str(root) or '"' in str(root) or '%' in str(root):
    raise SystemExit('Unsupported service path; review quoting before installation.')
text = f'''[Unit]
Description=Pstack Hermes loopback coordinator
After=network.target

[Service]
Type=simple
WorkingDirectory={root}
ExecStart=/usr/bin/python3 "{root}/coordinator/server.py" --port 9999
Restart=on-failure
RestartSec=3
UMask=0077
KillMode=control-group

[Install]
WantedBy=default.target
'''
prior_authored = text.replace(f'WorkingDirectory={root}', f'WorkingDirectory="{root}"')
if unit.exists() and unit.read_text() not in (text, prior_authored):
    raise SystemExit('Existing service differs; preserve and compare it before replacement.')
# Validate the candidate before changing a running owner.
candidate = root / 'state/coordinator/pstack-coordinator.service'
candidate.parent.mkdir(parents=True, exist_ok=True)
candidate.write_text(text)
subprocess.run(['systemd-analyze', '--user', 'verify', str(candidate)], check=True)
# Stop only the previously started coordinator, with no running trial and verified cwd/command.
pid_path = root / 'state/coordinator/server.pid'
if pid_path.exists():
    pid = int(pid_path.read_text().strip())
    proc = Path('/proc') / str(pid)
    if proc.exists():
        cwd = (proc / 'cwd').resolve()
        command = (proc / 'cmdline').read_bytes().split(b'\0')
        if cwd != root or b'coordinator/server.py' not in command:
            raise SystemExit('Recorded process is not the expected owned coordinator; no signal sent.')
        snapshot = json.load(urllib.request.urlopen('http://127.0.0.1:9999/api/state', timeout=3))
        if any(j['status'] in ('running', 'owner unavailable') for j in snapshot['jobs']):
            raise SystemExit('A trial is active or unresolved; wait before changing its service owner.')
        os.kill(pid, signal.SIGTERM)
        pid_path.unlink()
unit.parent.mkdir(parents=True, exist_ok=True)
unit.write_text(text)
subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
subprocess.run(['systemctl', '--user', 'enable', '--now', 'pstack-coordinator.service'], check=True)
subprocess.run(['systemctl', '--user', 'is-active', 'pstack-coordinator.service'], check=True)
print('User service installed. Login user-manager persistence follows the host configuration.')
