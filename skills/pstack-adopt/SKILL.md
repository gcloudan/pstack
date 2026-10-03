---
name: pstack-adopt
description: "Evaluate and integrate a selected pstack feature into an existing Cursor harness, preserving upstream provenance and recording the adaptation and trial. Use when asked to carry over another pstack skill or playbook."
---

# Adopt one coherent feature

Use the user's supplied clone containing `adoption.json` and
`upstream/snapshot.json`, or the open repository if those files exist there.
If the clone or target harness is unavailable, request its path or repository;
prepare a reviewable integration in the clone while distinguishing that from
installation. Do not search unrelated private histories or whole home folders.

Read the selected upstream skill, its referenced resources/callers, the
adoption record and the relevant existing target rules, skills and agents.
Choose one useful mechanism or a coherent dependency batch. Prefer improving
an existing equivalent recipe over installing a conflicting duplicate.

Record what decision the feature changes, where the current harness lacks it,
what to preserve, adapt or omit, and which concrete dependencies must ship.
Keep author presets separate from required invariants. Do not import fixed
counts, unsupported models, broad permission grants or delivery ceremony merely
because the upstream wrapper used them.

Keep `upstream/pstack` unchanged. Author only the adapted resources, narrowly
scoped harness activation and the installer/profile needed to discover them.
Use namespaced additions when names collide. Keep existing user preferences
and project instructions; show a diff before replacing existing harness files
unless those specific edits are already authorized.

Trial the feature on a representative permitted task, using actual artifacts
or command results where relevant. Choose meaningful behavioral checks, not
tests that just repeat the new wording. Check references and installed copies.
If a trial requires an unavailable runtime, account or project prerequisite,
record it as untested or blocked rather than label it successful.

Update `adoption.json` with source, target resources, decision, verification and
actual integration status. Preserve separate states for source preserved,
adapted/tested, installed and observed active in Cursor. Add the next useful
candidate only as a queue item; do not silently activate the whole upstream.
Commit/publish within the existing task's authorization.
