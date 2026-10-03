# Your pstack harness

The complete pstack v0.15.6 source is preserved in `upstream/pstack` at commit
`23e4138daa01c42d4969f7a5465f82704e64f798`. The working layer under `skills/`
adapts selected mechanisms to fit your existing Cursor harness.

Start with [the feature rankings](docs/PSTACK_ADOPTION_REVIEW.md) and
[the integration record](docs/HARNESS_INTEGRATION.md). `adoption.json` tracks
77 source features: 49 public skills/principles, 23 playbooks, two agents and
three separate Benny automation skills. Preserved source is not automatically enabled.

## First integration batch

| Component | What it does |
|---|---|
| `pstack-router` | Uses an existing compatible project recipe first; routes supported investigation tasks |
| `pstack-how` | Traces reachable implementation, checks documentation against code, reports evidence and gaps |
| `pstack-swarm` | Assigns independent responsibilities when useful; distinguishes complete coverage from a first-success race |
| `pstack-investigator` agent | Shares the investigation contract with a scoped read-only worker |
| `pstack-adopt` | Compares and integrates the next upstream feature against the actual harness |
| `repo-onboarding` | Establishes current repository behavior and verification status |
| `work-mode` / `automate-me` | Starter preferences and a builder using selected accessible history |

This batch does not port every engineering workflow or choose models for you.
The source remains available for the next feature-by-feature integration.

## Clone on your work computer

```sh
git clone https://github.com/gcloudan/pstack.git
cd pstack
```

For an existing clone, use `git pull --ff-only`. An offline bundle can also be
cloned with `git clone /path/to/cursor-work-style.bundle pstack`.

## Preview and install

For a specific existing project on Windows:

```powershell
./scripts/install.ps1 -WorkspaceRoot 'C:/path/to/project' -DryRun
./scripts/install.ps1 -WorkspaceRoot 'C:/path/to/project'
```

On macOS/Linux:

```sh
sh scripts/install.sh --workspace-root /path/to/project --dry-run
sh scripts/install.sh --workspace-root /path/to/project
```

Without a workspace argument, either installer installs the core into
`~/.cursor/skills` and `~/.cursor/agents`. For cross-project activation, add
[the User Rule text](docs/cursor-user-rule.txt) in Cursor's Rules settings.
The installer does not edit that UI setting. A workspace installation also
adds the namespaced `.cursor/rules/pstack-harness.mdc` rule.

Installers copy the complete seven-skill profile, supporting resources and one
agent. They preserve differing existing packages by default and exit 2 to flag
comparison. Other packages may still be installed; this is not an atomic transaction.
After comparing changes, `-ReplaceExisting` or `--replace-existing` backs up
overwritten files under a sibling `pstack-harness-backups` directory. Extra
files and unrelated skills, rules and agents remain in place.

For a scratch install, use `-SkillsRoot ./scratch/skills` or
`--skills-root ./scratch/skills`. The agent root must be the adjacent `agents`
directory because its shared contract uses relative paths. Manual installation
must copy every folder listed in `profiles/core.skills`, plus the agent listed
in `profiles/core.agents`; copying only SKILL.md files loses resources.

Open a fresh Cursor chat and ask it to read `/pstack-router`, describe the
available routes and investigate a small subsystem. Local files do not prove
discovery or availability in remote/cloud environments.

## Keep adopting features

In the harness clone, invoke `/pstack-adopt` with the feature and target project,
for example: “Compare upstream blast-radius with this project's existing
change-planning workflow. Add only the missing useful behavior and verify it.”

The process is compare → adapt → exercise → record → install. Launch commands,
test gates, product constraints and delivery policy stay in each workspace.
The next candidates are change impact, reusable verification recipes, then
test-driven implementation and architecture planning where needed.

Use `/automate-me` later with selected accessible conversation exports. Cloning
does not import prior chats. The current mode is a conversation-based seed;
no full-history profile has been generated. Keep raw history and private state
outside shared commits.

## Checks and provenance

`python scripts/validate.py` checks the snapshot, inventory and active dependencies.
`--installed-root /path/to/project/.cursor` also compares installed resources.
Python is optional for installation. [Verification](docs/VERIFICATION.md)
records the actual trials and remaining work-side checks.

The original MIT license is retained. This repository supplies instructions and
resources; Cursor supplies model access, execution and subagent capabilities.
See [origin notice](NOTICE.md).
