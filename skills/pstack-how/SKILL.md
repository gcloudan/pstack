---
name: pstack-how
description: "Trace active entry points, callers, data flow and ownership to explain how a subsystem works. Use for implementation walkthroughs and placement questions; motivation requires historical evidence."
---

# Understand the implementation

State the question and relevant subsystem. Use the existing project's source
navigation or investigation recipe if it already provides the needed trace.
Read documentation as a map, then identify the reachable entry point, callers,
state/data transformations and boundaries in current code. Do not infer active
behavior from names or an unused legacy implementation.

Handle a narrow path directly. For a broad question, choose independently
answerable angles when they improve coverage or keep bulky evidence out of the
parent. Use [pstack-swarm](../pstack-swarm/SKILL.md) for that fan-out. There is no
minimum, maximum preset or obligatory separate explainer. Use only available
concurrency. Shared live app state needs one owner.

Give investigators the original question, their responsibility, relevant
source pointers and the [return contract](references/investigation-contract.md).
Use the installed `pstack-investigator` when available, or an available generic
read-only worker with the same contract. Inherit the model unless a supported
role choice was explicitly configured. If workers are unavailable, trace the
chosen angles sequentially and disclose that limitation.

Spot-check consequential claims against original source; resolve disagreement
by tracing the path or running a permitted probe, not counting model votes.
Separate implementation, documentation, history and observed runtime behavior.
Label gaps. Historical motivation is inferred unless the selected record
supports it; do not invent an unavailable `why` workflow or connector.

Return a connected explanation at the depth requested, naming the few files
that own the behavior, the relevant flow and material gotchas. A diagram is
useful when it clarifies that flow. No compulsory headings or principle recital.
Checks prove their asserted cases; source tracing is not a live-app trial.

Default scope is investigation. Run relevant inexpensive non-mutating checks
when permitted; state the prerequisite for anything that cannot be observed.
Do not change product code, live state, credentials or delivery merely to
complete the explanation unless the current task authorizes it.
