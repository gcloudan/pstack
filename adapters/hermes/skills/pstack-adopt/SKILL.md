---
name: pstack-adopt
description: Integrate useful pstack methods into an existing harness.
version: 0.1.0
license: MIT
author: Lauren Tan (poteto), adapted for gcloudan
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pstack, adoption, skills]
---

# Adopt the next useful feature

## When to Use

Use when asked to carry another pstack feature into this harness. Locate the
user-supplied clone containing `adoption.json` and `upstream/snapshot.json`.
If unavailable, ask for its path. Do not sweep private history or home folders.

Read the selected original skill, referenced dependencies, adoption decision
and relevant existing Hermes skills using `read_file` and `skill_view`.
Identify the decision-changing behavior that is missing. Keep an equivalent
existing recipe; do not add a duplicate router, fixed worker count, unsupported
model policy or original author's delivery defaults.

Keep `upstream/pstack` unchanged. Author the selected adaptation under
`adapters/hermes/skills` in the clone. Use `skill_manage` for native installation
and supporting resources, preserving its approval result: staged is not installed.
Compare existing customized skills before any authorized update. Do not use
the Cursor installer for Hermes or copy Cursor agent definitions into its runtime.

Exercise a representative permitted task, inspect meaningful evidence and
record gaps. Update the adoption ledger and Hermes receipt separately: source
preserved, instructions adapted, installed, loader verified and live task observed
are distinct states. Verify native `skills_list` and `skill_view` discovery in
a fresh process/session. Do not restart running chats to refresh their caches.

## Pitfalls and verification

History-based preferences are a separate explicitly selected workflow. Existing
planning, debugging and TDD remain project choices. A missing account or runtime
means the feature is untested, not successful. Commit or publish only within
the current task's authorization. A future queue item is not automatic activation.
