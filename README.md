# Pstack adoption review and initial Cursor kit

Use `/automate-me` to turn selected conversations into your own working
preferences. Use `work-mode` to apply those preferences in everyday work.
The builder is adapted from pstack; this is a small independent kit, not the
full pstack plugin. No plugin installation or model configuration is required.

**Start with [the whole-pstack adoption review](docs/PSTACK_ADOPTION_REVIEW.md).**
It ranks all 25 ordinary skills, 24 principles, 23 playbooks, worker definitions,
helpers and optional integrations, and recommends what to keep or adapt.

This repository currently ships three initial personal/adoption skills. It is
not yet a dependency-complete fork of the recommended pstack workflows. The
review distinguishes those recommendations from installed capabilities.
The [automate-me review](docs/AUTOMATE_ME_REVIEW.md) is a narrower appendix.

## What is included

| File | Purpose |
|---|---|
| `skills/automate-me/SKILL.md` | Explicitly invoked builder; reads selected evidence and drafts/updates your mode |
| `skills/work-mode/SKILL.md` | Small starter personal mode; based only on the present conversation |
| `skills/repo-onboarding/SKILL.md` | Optional workflow for repository status questions |
| `docs/cursor-user-rule.txt` | Text to activate the mode across new Cursor Agent chats |
| `docs/WORKSPACE-AGENTS.section.md` | Alternative activation snippet for selected repositories |
| `docs/history-selection.example.md` | Template for selecting work and exported chat evidence |
| `docs/preference-seed.md` | Why each starter preference is present |
| `scripts/install.ps1` / `scripts/install.sh` | Copy the three skills; preserve differing installed files by default |

## Clone on the work computer

The selected hosting destination is `gcloudan/pstack`. Once the prepared commit
is pushed, clone it on the work computer:

```sh
git clone https://github.com/gcloudan/pstack.git cursor-work-style
cd cursor-work-style
```

The delivery report records whether publication succeeded. A Git bundle is also
prepared as a self-contained cloneable copy. If remote access is unavailable,
copy `cursor-work-style.bundle` through your permitted file-transfer route,
then clone it:

```sh
git clone /path/to/cursor-work-style.bundle cursor-work-style
cd cursor-work-style
```

On Windows, an example after copying the bundle to Downloads is:

```powershell
git clone "$HOME/Downloads/cursor-work-style.bundle" "$HOME/cursor-work-style"
Set-Location "$HOME/cursor-work-style"
```

Offline clones have a file-path origin. For later updates, obtain another bundle
and fetch it, or set origin to a hosted remote once one exists. A bundle does not
provide a sync service. If hosting is preferred, push this prepared repository
to the selected work-accessible repository, then use its URL instead. Cloning
upstream pstack would not include this adaptation.

If you clone the bundle on a machine with an authenticated GitHub connection,
publish this prepared repository with:

```sh
git remote set-url origin https://github.com/gcloudan/pstack.git
git push -u origin main
```

No force push is required. If the remote has acquired other work, reconcile it
before pushing rather than overwriting it. Publication from the preparation
machine was attempted but blocked by missing valid GitHub credentials.

## Install once

Windows PowerShell:

```powershell
./scripts/install.ps1
```

macOS/Linux shell:

```sh
sh scripts/install.sh
```

If execution policy blocks a local PowerShell script, copy the three skill
directories under `skills/` into `$HOME/.cursor/skills/` yourself. No execution
policy change or extra runtime is needed for manual installation. The result is
`~/.cursor/skills/automate-me/SKILL.md`, `work-mode/SKILL.md`, and
`repo-onboarding/SKILL.md`. Keep all three, because their relative links depend
on this arrangement. Open a fresh Cursor Agent chat to check discovery.

The scripts accept a custom root for a trial:

```powershell
./scripts/install.ps1 -SkillsRoot ./scratch/skills
```

```sh
sh scripts/install.sh --skills-root ./scratch/skills
```

## Activate across projects

Cursor documents user-level skills in `~/.cursor/skills` and a separate global
User Rules setting. In **Cursor Settings → Rules** (the Customize → Rules area
in current documentation), add the text from `docs/cursor-user-rule.txt` as a
User Rule. This is a one-time manual setting; the installer does not edit an
undocumented settings store. See [Cursor skills](https://cursor.com/docs/skills)
and [Cursor rules](https://cursor.com/docs/rules).

For a quick explicit trial, invoke `/work-mode` in a chat. For session use, the
skills documentation describes selecting a skill as a Custom Mode with
Alt+Enter on Windows. Availability alone does not mean every task uses it.
The User Rule requests the persistent behavior; verify it in a fresh chat.

If you prefer selected repositories, merge `docs/WORKSPACE-AGENTS.section.md`
into each project's existing root `AGENTS.md` instead of using a User Rule.
Do not overwrite the project's existing instructions. For remote/cloud agents,
local files need a supported sync or repository installation; a file on your
laptop cannot be assumed present in another execution environment.

Ask a fresh work chat: “Read my work-mode and tell me its four preferences,
then apply them to this task.” Confirm it can find the installed file. The
current request and project instructions still determine scope and permissions.

## Make it yours with selected history

1. Review the starter preferences. They are a seed, not a full history profile.
2. Make a source selection using `docs/history-selection.example.md`.
3. Place permitted exports in a local private directory, or supply the active
   Cursor workspace's transcript location. Select multiple projects explicitly
   if you want preferences from across them. Prior ChatGPT/Codex chats need an
   accessible export or another authorized source; cloning cannot import them.
4. Invoke `/automate-me` with those source paths and your existing work-mode.
5. Review the actual draft and evidence, then accept/edit the changes.

Keep raw histories and the analysis watermark outside the shared repository.
`history/`, `private/` and `state/` are ignored for a local experiment, but Git
ignore is not a scrubber for previously tracked files. Commit only the concise
mode you intend to share. Work-specific preferences can stay on the work
machine; this repository need not receive them.

## Updates without losing your mode

An ordinary install preserves a differing installed skill and returns exit 2
to signal that comparison is needed. It is safe to rerun unchanged installs.
Before replacing files, compare the installed mode with the source and copy
your accepted personalized mode back into `skills/work-mode/SKILL.md` if it
belongs in this repository. Then install the reviewed version explicitly:

```powershell
./scripts/install.ps1 -ReplaceExisting
```

```sh
sh scripts/install.sh --replace-existing
```

These flags affect all three kit files that differ. They back up the previous
files in a sibling `work-style-backups` directory before copying. They do not
delete other skills or edit User Rules. The mode retains a stable `work-mode`
name, so its activation text need not change on each refresh.

## Limits

This delivery prepares and checks the portable files; it cannot verify your
work Cursor configuration from this machine. History mining happens only when
you invoke the builder with accessible selected sources. The scripts do not
install upstream pstack, choose models or supply subagent tools. A shorter rule
can improve consistency, but no productivity gain has been measured.
