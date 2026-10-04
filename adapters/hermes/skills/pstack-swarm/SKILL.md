---
name: pstack-swarm
description: Delegate distinct responsibilities and verify coverage.
version: 0.1.0
license: MIT
author: Lauren Tan (poteto), adapted for gcloudan
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, coverage, pstack]
---

# Delegate by responsibility

## When to Use

Use when separate investigations or disjoint work units improve coverage or
context isolation. A small task can stay in the parent. Existing project worker
recipes take precedence when compatible with the requested outcome.

State the done predicate and required coverage. Choose the smallest useful
set of independent responsibilities; total responsibilities and simultaneous
capacity are different. A coverage task needs every required slice. First
success finishes only a race explicitly designed around that criterion.

Use the runtime's actual `delegate_task` schema. On the inspected Hermes version,
the `tasks` array accepts separate `goal` and `context` per child. Do not invent
model-facing toolsets, named Cursor agents or model overrides. Inspect current
tool definitions if the runtime changes. When delegation is absent, work through
the responsibilities sequentially and say so.

Each child's context includes original intent, corrections, responsibility,
relevant pointers, allowed actions, revision/method when relevant and expected
return: findings, source/command evidence, checks run, gaps and contradictions.
Repeat shared background per child; it does not inherit the conversation.
Let children choose their searches. Give writers disjoint files or isolated
outputs, and one owner for shared live state. Investigation-only briefs prohibit
edits, but do not pretend that prose removes a child's actual tool permissions.

Read the findings and important artifacts. PASS/ISSUES/BLOCKED labels are not
proof. Spot-check consequential claims, reconcile conflicts and account for
failed or missing slices. Retry only when a bounded retry can add missing evidence.
The parent owns the final answer, artifacts and delivery scope.

## Pitfalls and verification

Do not overwrite an existing debugging, planning or test workflow just to add
parallelism. No fixed count, cloud placement or mandatory multi-model panel.
Finish with one report stating established coverage, evidence, changes if
authorized, disagreements and remaining gaps.
