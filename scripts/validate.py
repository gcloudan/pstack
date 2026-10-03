#!/usr/bin/env python3
"""Verify preserved source, active profile dependencies and an optional installation."""
from pathlib import Path
import argparse
import hashlib
import json
import re

kit = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--installed-root', type=Path, help='The target .cursor directory containing skills and agents')
args = parser.parse_args()

def require(condition, message):
    if not condition:
        raise SystemExit(message)

snapshot = json.loads((kit / 'upstream/snapshot.json').read_text(encoding='utf-8'))
original = kit / 'upstream/pstack'
actual = {path.relative_to(original).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
          for path in original.rglob('*') if path.is_file()}
require(actual == snapshot['files_sha256'], 'Upstream snapshot has changed; compare it before adoption.')
adoption = json.loads((kit / 'adoption.json').read_text(encoding='utf-8'))
source_skills = {path.parent.name for path in (original / 'skills').glob('*/SKILL.md')}
recorded_skills = {row['id'] for row in adoption['features'] if row['kind'] in ('skill', 'principle')}
require(source_skills == recorded_skills, 'Adoption inventory differs from upstream public skills.')
source_playbooks = {'playbook:' + path.stem for path in (original / 'skills/poteto-mode/playbooks').glob('*.md')}
require(source_playbooks == {row['id'] for row in adoption['features'] if row['kind'] == 'playbook'}, 'Playbook inventory differs.')
for row in adoption['features']:
    require((kit / row['source']).is_file(), f"Missing preserved source: {row['id']}")

def profile(name):
    values = (kit / 'profiles' / name).read_text(encoding='utf-8').splitlines()
    require(len(values) == len(set(values)), f'Duplicate profile entries: {name}')
    require(all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value) for value in values), f'Invalid profile: {name}')
    return values

skills = profile(Path(adoption['active_profile']).name)
agents = profile(Path(adoption['active_agents']).name)
require(set(skills) == {path.parent.name for path in (kit / 'skills').glob('*/SKILL.md')}, 'Core profile and adapted skills differ.')
require(set(agents) == {path.stem for path in (kit / 'agents').glob('*.md')}, 'Core profile and agents differ.')
paths = [kit / 'skills' / name / 'SKILL.md' for name in skills] + [kit / 'agents' / (name + '.md') for name in agents]
for path in paths:
    content = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', content, re.S)
    require(match is not None, f'Missing frontmatter: {path}')
    name = re.search(r'^name: ([a-z0-9-]+)$', match.group(1), re.M)
    require(name is not None and name.group(1) == (path.parent.name if path.name == 'SKILL.md' else path.stem), f'Name mismatch: {path}')
    require(re.search(r'^description: .+', match.group(1), re.M), f'Missing description: {path}')
    for destination in re.findall(r'\]\(([^)]+)\)', content):
        if not re.match(r'^[a-z]+:', destination) and not destination.startswith('#'):
            require((path.parent / destination).is_file(), f'Broken active link: {path}: {destination}')
    if args.installed_root:
        relative = path.relative_to(kit)
        installed = args.installed_root / relative
        require(installed.is_file() and installed.read_bytes() == path.read_bytes(), f'Installed copy differs or missing: {installed}')
for name in skills:
    for path in (kit / 'skills' / name).rglob('*'):
        if path.is_file() and args.installed_root:
            installed = args.installed_root / path.relative_to(kit)
            require(installed.is_file() and installed.read_bytes() == path.read_bytes(), f'Installed resource differs or missing: {installed}')
agent = (kit / 'agents/pstack-investigator.md').read_text(encoding='utf-8')
require('../skills/pstack-how/SKILL.md' in agent, 'Investigator dependency missing.')
require((kit / 'skills/pstack-how/SKILL.md').is_file(), 'Investigator skill absent.')
for row in adoption['features']:
    for name in row.get('adapted_skills', []):
        require(name in skills, f"Adaptation not in installed profile: {row['id']} -> {name}")
print(f'Verified immutable upstream: {len(actual)} files at {snapshot["commit"]}.')
print(f'Verified inventory and core: {len(source_skills)} original skills, {len(source_playbooks)} playbooks, {len(skills)} adapted skills, {len(agents)} agent.')
if args.installed_root:
    installed_rule = args.installed_root / 'rules/pstack-harness.mdc'
    if installed_rule.exists():
        require(installed_rule.read_bytes() == (kit / 'rules/pstack-harness.mdc').read_bytes(), 'Installed project rule differs.')
    print(f'Verified all installed core files and supporting resources: {args.installed_root}.')
print('File integrity and dependency checks only; live Cursor activation is a separate trial.')
