"""Synthetic native hook registry test, isolated from the real observer receipt."""
from pathlib import Path
import importlib.util
import json
import os
import tempfile
import sys

runtime = Path.home() / '.hermes/hermes-agent'
sys.path.insert(0, str(runtime))
with tempfile.TemporaryDirectory(prefix='pstack-observer-check-') as folder:
    os.environ['HERMES_HOME'] = folder
    from hermes_cli.plugins import PluginContext, PluginManager
    from hermes_cli.plugins_manifest import PluginManifest
    from hermes_cli.plugins_dispatch import PluginDispatchMixin
    spec = importlib.util.spec_from_file_location('observer_check', Path(__file__).parent / 'observer/__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manager = PluginManager()
    context = PluginContext(PluginManifest(name='pstack-coordinator', key='pstack-coordinator'), manager)
    module.register(context)
    common = {'parent_session_id': 'test-parent', 'child_session_id': 'test-child',
              'child_subagent_id': 'test-worker', 'child_role': 'leaf',
              'child_goal': 'PRIVATE_GOAL_SENTINEL', 'child_summary': 'PRIVATE_SUMMARY_SENTINEL',
              'tool_call_history': ['PRIVATE_TOOL_SENTINEL'], 'telemetry_schema_version': 1}
    for event in ('subagent_start', 'subagent_stop'):
        for callback in manager._hooks[event]:
            PluginDispatchMixin._invoke_hook_callback(callback, common | {'child_status': 'completed', 'duration_ms': 12})
    path = Path(folder) / 'runtime/pstack-coordinator-events.jsonl'
    text = path.read_text()
    rows = [json.loads(line) for line in text.splitlines()]
    assert len(rows) == 2
    assert rows[0]['event'] == 'subagent_start' and rows[1]['event'] == 'subagent_stop'
    assert rows[1]['child_status'] == 'completed'
    assert all(row['parent_session_id'] == 'test-parent' for row in rows)
    assert 'PRIVATE_' not in text
    assert set(rows[0]) <= set(module.START_FIELDS) | {'event', 'event_id', 'at', 'observer', 'schema_version'}
    print('PASS native registry dispatch: start/stop IDs retained; goals, summaries and tool history excluded.')
