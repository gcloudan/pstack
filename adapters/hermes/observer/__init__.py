"""Additive Linux Hermes observer. Never records goals, summaries or tool arguments."""
import datetime
import fcntl
import json
import os
import uuid
from hermes_constants import get_hermes_home

START_FIELDS = ('parent_session_id', 'parent_turn_id', 'parent_subagent_id',
                'child_session_id', 'child_subagent_id', 'child_role')
STOP_FIELDS = ('parent_session_id', 'parent_turn_id', 'child_session_id',
               'child_role', 'child_status', 'duration_ms')

def append_event(event, fields, payload):
    record = {'event': event, 'event_id': uuid.uuid4().hex,
              'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'observer': 'pstack-coordinator', 'schema_version': 1}
    for key in fields:
        value = payload.get(key)
        if isinstance(value, (str, int, float)) or value is None:
            record[key] = value[:160] if isinstance(value, str) else value
    runtime = get_hermes_home() / 'runtime'
    runtime.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = runtime / 'pstack-coordinator-events.jsonl'
    lock_path = runtime / 'pstack-coordinator-events.lock'
    flags = os.O_CREAT | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0)
    lock_fd = os.open(lock_path, flags, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        if path.exists() and path.stat().st_size > 8 * 1024 * 1024:
            path.replace(path.with_suffix('.jsonl.previous'))
        fd = os.open(path, flags | os.O_APPEND, 0o600)
        try:
            os.write(fd, (json.dumps(record, separators=(',', ':')) + '\n').encode())
        finally:
            os.close(fd)
    finally:
        os.close(lock_fd)

def on_start(**kwargs):
    append_event('subagent_start', START_FIELDS, kwargs)

def on_stop(**kwargs):
    append_event('subagent_stop', STOP_FIELDS, kwargs)

def register(ctx):
    ctx.register_hook('subagent_start', on_start)
    ctx.register_hook('subagent_stop', on_stop)
