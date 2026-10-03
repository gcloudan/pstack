---
name: repo-onboarding
description: "Establish a repository's current behavior, architecture and verification status before taking ownership or planning changes. Use for project onboarding, current-state briefs and subsystem walkthroughs."
---

# Repository onboarding

Produce a brief that lets the user decide what to work on next. Treat onboarding as investigation unless the user also authorizes changes. Keep roadmap, implementation, historical receipts and checks run now distinct.

## Establish the question

Read applicable workspace instructions. Identify the user's decision, the relevant subsystem and allowed actions. For a whole-project question, establish entry points, active routes, current worktree state and runnable checks before choosing investigation angles. Read documentation as a map; trace claims through the code that is actually reachable.

## Choose the work shape

Handle a narrow path directly. Delegate when independently answerable questions would improve coverage, reduce the parent context, or provide a useful independent challenge. Choose the smallest useful worker set, within available concurrency; there is no target count. State each worker's responsibility and avoid overlapping broad assignments.

Assign questions rather than arbitrary file groups. Examples include delivered behavior versus roadmap, data flow across boundaries, and what existing verification establishes. These are examples, not required roles. If subagents are unavailable, work through the selected questions sequentially and disclose that limitation.

Each worker gets the overall question, its specific responsibility, relevant file pointers, allowed actions and this return contract:

- Findings with source locations or recorded command results.
- The active path or boundary that makes each finding relevant.
- What was checked and what remains uncertain.
- Consequential contradictions or gaps, without repairing them during an investigation.

Use the session's available delegation tools. Inherit its model unless the user or project requests a supported alternative. File pointers can replace large copied context, but include enough of the brief that the worker cannot miss scope or later corrections. Concurrent authors, if separately authorized, must own disjoint edits or isolated checkouts.

## Resolve and verify

Do not treat worker agreement as independent proof. Resolve material contradictions against original source or behavior. Use a separate synthesizer when broad or conflicting findings justify a fresh pass; it must receive the original question and scope as well as the findings. For small, consistent findings, synthesize directly.

For conclusions that change the user's next action, identify the fact they depend on and get proportionate evidence. A source reference proves an implementation exists; a real caller trace proves reachability. A build proves compilation; tests prove their asserted cases. Where cheap and consequential, run a probe against the real implementation. Label anything that still requires installed-app, service or external-provider observation. Do not substitute a checklist, model agreement or old receipt for that observation.

Report available safe checks and run relevant inexpensive ones within the authorized scope. Generated test/build artifacts may change; disclose that when it matters. Do not consume cloud usage, change credentials, install software or mutate a live app merely to complete an onboarding brief without task authorization. Never read secrets just to inventory configuration.

## Deliver the brief

Lead with current status and what the user can safely do next. Explain the active flow and the few files that own it. Include confirmed findings, material uncertainty and commands/evidence used. State how documentation differs from reality when that affects a decision. Scale detail to the task; do not force headings, a diagram, a plan or a review panel into a simple answer.

This skill provides a workflow, not extra capabilities or permission. Workspace rules and available tools determine the concrete commands, constraints and verification surfaces.
