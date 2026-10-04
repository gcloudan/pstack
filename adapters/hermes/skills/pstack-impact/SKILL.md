---
name: pstack-impact
description: Trace downstream breakage and test critical safety facts.
version: 0.1.0
author: Lauren Tan (poteto), adapted for gcloudan
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [change-impact, evidence, pstack]
---

# Check what a change could break

## When to Use

Use for change-impact questions or reviewing a small diff whose downstream
behavior is uncertain. Complement an existing project planning/review recipe;
do not replace it or require a multi-agent panel for a small change.

Read the proposed diff or exact hypothetical change. Establish before/after
behavior and identify the one or two safety facts on which the conclusion
depends. Use `search_files` and `read_file` to follow callers, serialized formats,
state ownership, timing, flags and pinned dependency behavior beyond symbol matches.
Do not invent downstream consumers or quantify likelihood without evidence.

For each material risk, distinguish a source pointer, a traced reachability
argument, an executed check and a live-app reproduction. Take the critical fact
as far as a cheap permitted check allows. Use `terminal` to call the real code
through the existing test/run recipe. Reuse existing checks where they establish
the relevant behavior; add a narrowly scoped probe only when authorized.
If approval or a missing prerequisite blocks the probe, label that fact unproven
or source-inferred. Do not bypass the runtime's approval controls.

Load `pstack-swarm` only when independent slices materially improve coverage.
The parent reads the evidence and resolves contradictions. No mandatory model
comparison, external history connector, new PR or delivery step.

## Verification and pitfalls

Return the changed behavior, critical safety fact with its evidence level,
confirmed risks, checked/cleared cases and the cheapest remaining verification.
A list of callers alone is not impact analysis. Source assertions and green
unrelated tests do not prove safety. A hypothetical review does not authorize
applying the change, editing production data or publishing findings externally.
