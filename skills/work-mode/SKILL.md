---
name: work-mode
description: "Apply the user's working preferences for practical demonstrations, adaptive delegation and evidence-backed engineering. Use when asked to use work-mode or follow the user's working style."
---

# My working mode

Starter based on explicit preferences in the pstack investigation conversation.
It has not been mined from the user's full history. Use /automate-me to revise it
from selected work conversations. Project-specific instructions and the current
request determine scope, capabilities and authorization.

- When asked to try or assess a workflow, use it on a concrete permitted task
  and show what changed. Distinguish a source review from an actual trial.
- Choose subagents by independently answerable questions or disjoint changes,
  not a preset count. State each worker's responsibility. Let workers choose
  their searches and commands; the parent reviews the combined result.
- Explain important mechanisms with concrete examples. When the user asks why
  an instruction helps, name the decision it changes and the evidence for it.
  Label presets and preferences as such rather than present them as necessities.
- Match verification to the claim. Distinguish code tracing, current checks,
  prior receipts and untested live behavior. Do not claim that a green checklist,
  compilation or worker agreement proves every user path.

For repository onboarding/current-state questions, use
[repo-onboarding](../repo-onboarding/SKILL.md) when its scope matches. For bugs,
features or reviews, use the project's available workflow and verification
instructions rather than force an investigation or an unavailable pstack tool.
For new preference mining, use [automate-me](../automate-me/SKILL.md).

Do not turn a task-specific instruction or a project's facts into global policy.
This mode adds preferences, not permissions or tools. Opt out when the user asks.
