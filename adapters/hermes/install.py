#!/usr/bin/env python3
"""Run with Hermes's existing venv Python; preserve native manager gates."""
from pathlib import Path
import json
import sys

source = Path(__file__).resolve().parent
runtime = Path.home() / '.hermes/hermes-agent'
sys.path.insert(0, str(runtime))
from tools.skill_manager_tool import skill_manage
from tools.skills_tool import skills_list, skill_view

before = json.loads(skills_list())
assert before.get('success'), before
before_names = {s['name'] for s in before['skills']}
results = []
for folder in sorted((source / 'skills').iterdir()):
    name = folder.name
    content = (folder / 'SKILL.md').read_text()
    loaded = json.loads(skill_view(name, preprocess=False))
    if name in before_names:
        # First install never overwrites an existing skill. Exact copies are idempotent.
        path = Path.home() / '.hermes/skills/software-development' / name / 'SKILL.md'
        if not path.is_file() or path.read_text() != content:
            raise SystemExit(f'Existing {name} differs; compare and update through skill_manage explicitly.')
        result = {'success': True, 'already_current': True}
    else:
        result = json.loads(skill_manage(action='create', name=name,
            category='software-development', content=content))
    print(name, json.dumps(result))
    if not result.get('success') or result.get('staged'):
        raise SystemExit('Native manager did not install; approval result retained without bypass.')
    assert json.loads(skill_view(name, preprocess=False)).get('success'), name
    results.append(name)
after = json.loads(skills_list())
after_names = {s['name'] for s in after['skills']}
assert before_names <= after_names, 'Existing catalog names lost'
receipt = {'runtime': 'Hermes', 'installed_skills': results,
    'before_count': len(before_names), 'after_count': len(after_names),
    'existing_catalog_preserved': True, 'loader_verified': True,
    'live_model_task_observed': False, 'cursor_agents_installed': False}
# Retain original first-install counts when rerunning an unchanged profile.
receipt_path = source / 'installation.local.json'
if receipt_path.exists():
    previous = json.loads(receipt_path.read_text())
    receipt['before_count'] = previous.get('before_count', receipt['before_count'])
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
