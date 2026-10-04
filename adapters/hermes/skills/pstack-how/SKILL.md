---
name: pstack-how
description: Trace active subsystem behavior with source evidence.
version: 0.1.0
license: MIT
author: Lauren Tan (poteto), adapted for gcloudan
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [investigation, source-tracing, pstack]
---

# Explain how a subsystem works

## When to Use

Use for implementation walkthroughs, ownership questions and checking whether
documentation describes current behavior. Use an existing project recipe when
it already supplies the needed trace. For an actual bug, retain the existing
`systematic-debugging` workflow; a walkthrough is not a repair authorization.

Use `search_files` and `read_file` to trace reachable entry points, callers,
data transformations and ownership boundaries. Documentation supplies pointers;
unused legacy code does not establish active behavior. Run inexpensive relevant
checks through `terminal` when the task permits them, recording actual results.

Handle a narrow path directly. When independent questions improve coverage,
load `pstack-swarm` with `skill_view` and use the available `delegate_task` tool.
Give each child the original question, responsibility, source pointers, permitted
actions and required evidence. Children choose their own searches. Investigation
briefs prohibit edits and external actions, but that is a task contract, not a
claim of sandbox-enforced read-only execution. If delegation is unavailable,
work sequentially and disclose that limitation.

Read the returned source and spot-check consequential claims. Resolve conflicts
by tracing or permitted probes, not model votes. Explain the few files that own
the behavior, the flow and important gaps. Separate source inference, documentation,
history and observed runtime results. Historical motivation needs actual records.

## Pitfalls and verification

No fixed worker count or mandatory separate explainer. Shared live app state
needs one owner. A source trace is not proof that a live application works.
The explanation is complete when its material claims have source or command
evidence and missing coverage is explicit. Do not change product code merely
to complete an explanation.
