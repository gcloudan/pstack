# Automate-me: ranked source audit for the Cursor work kit

Audit date: 3 October 2026. Source inspected: pstack commit `23e4138daa01c42d4969f7a5465f82704e64f798`, version 0.15.6. This is a source-based engineering judgment, not a benchmark of productivity or the author's private intentions. Ratings describe usefulness for this user's portable personal-mode builder.

The original [automate-me source](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md) builds instructions about how a user works. It does not establish project state, supply transcript access, or create subagent capabilities. Its strongest mechanism is evidence-backed preference extraction followed by user correction.

## Ranking

| Rank | Original mechanism | Decision and why |
|---|---|---|
| 5/5 | Evidence pointers, repeated-pattern checks, and user review ([lines 31–40](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L31-L40), [79](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L79)) | Keep. Prevents a plausible description of the user from becoming an unsupported permanent instruction. Separate explicit requests from inferred patterns and record contradictions. |
| 5/5 | Scoped transcript reading ([line 29](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L29)) | Keep the boundary, adapt the source choice. Read only the active workspace or a manifest of explicitly selected exports. Cross-project learning is appropriate when the user selects those projects. Automatic sweeping of every private workspace is inappropriate. |
| 5/5 | Minimal, operational instructions; no copied author style ([63](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L63), [87–92](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L87-L92)) | Keep. Makes the mode cheaper to read and less likely to impose irrelevant behavior. Record a condition and an action, rather than personality adjectives. |
| 4/5 | Update existing mode in place; preserve unchanged preferences ([17–25](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L17-L25)) | Keep. Avoid duplicate modes and unnecessary rewriting. Explicit revocations and conflicting new requests still need resolution. |
| 4/5 | Distinguish broad personal mode from one narrow workflow ([100–103](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L100-L103)) | Keep. A commit-message convention can be its own skill rather than a standing burden on every task. |
| 3/5 | Pattern repeated across two slices is high confidence ([40](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L40)) | Adapt. Two slices of the same incident are not two independent observations. Repetition supports inferred habits; one explicit durable instruction can be enough. A recent explicit correction can override an older repeated habit. |
| 3/5 | Parallel miners over history slices ([31](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L31)) | Conditional. Useful for large, independent collections; wasteful for a short export. Choose partitions by conversation, topic or period when those distinctions prevent duplication. No fixed number of workers. |
| 3/5 | Structured questions with 4–6 options and a final free-form question ([44–48](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L44-L48)) | Adapt. Review ambiguities that affect the actual draft. Tools and option limits differ between hosts. Do not force an interview when the user already gave the necessary direction. |
| 3/5 | Reference other skills rather than duplicating them ([89](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L89)) | Keep only with dependency checks. A reference to an absent skill does nothing. Ship required references or provide a short operational fallback. References are not an automatic router. |
| 2/5 | Mandatory built-in create-skill plus unslop ([11](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L11), [67](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L67), [77](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L77)) | Replace dependency with explicit authoring checks. YAML validity, resolvable references and clear imperatives matter. A named editorial skill is an implementation choice. |
| 2/5 | Git commit timestamp as last-edited cutoff ([23](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L23)) | Replace. Untracked home-level modes have no commit; local edits need not be committed. Even a correct edit timestamp is not the last transcript processed. Track source IDs, covered periods and an analysis watermark in a separate manifest. |
| 2/5 | Vibe-check instead of behavioral evaluation ([96–98](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L96-L98)) | User approval is essential but incomplete. Run a few realistic tasks to check that the mode does not force subagents for trivial work, omit evidence for significant claims, or ask repeatedly for already granted permission. This need not become a large benchmark. |
| 1/5 | Always worktree, commit and open PR ([83](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L83)) | Omit as a universal requirement. Useful for team-owned rules, unnecessary for a local personal mode. A PR or remote publish is a distinct action, not the inevitable end of preference mining. |

## Preferences are not the same as observed failures

The miner should label each candidate with its evidence kind:

1. **Explicit durable request.** The user says to use adaptive agent counts or carry authorized work to completion. One statement can establish it. Do not discard it because it occurred in one time slice.
2. **Repeated correction.** The user repeatedly asks for a concrete demonstration after capability claims. This supports an inferred preference for showing the behavior, with source pointers.
3. **Task instruction.** “Do not modify this project for this investigation” constrains that investigation. It is not a permanent prohibition against modifying that project or all repositories.
4. **Failure signal.** An agent claims it installed or tested something without evidence. Capture a completion-reporting safeguard, not an invented user personality trait.
5. **Assistant-created claim.** The assistant says “you like this.” That is not user evidence until the user endorses it.

Generated drafts should show accepted candidates, uncertainty and conflicts. Repeated assistant mistakes can reveal what safeguard is useful; they do not automatically reveal a user's preference. New explicit user direction takes priority over older inferred habits. “Proceed autonomously” should retain the boundary of authorized work and the host's constraints.

## What the README promise does not guarantee

The [README make-it-yours section](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/README.md#L245-L249) promises a personal routing skill that routes through pstack underneath. The inspected automate-me implementation names create-skill and unslop, lists optional categories, and says to reference skills. It does not explicitly require adding a particular pstack routing table to every generated mode. The actual generated content and availability of referenced skills determine that behavior.

A portable kit should therefore state exactly what it contains. A personal preference mode can operate independently. If it routes to workflow skills, list those skills, ship them, and check each link. Do not claim to have preserved the full pstack system when only the builder and personal mode are included.

## Minimal portable builder contract

- Identify the existing mode and requested outcome: create, refresh or inspect.
- Use an explicit source manifest. Keep current conversation evidence distinct from exported history. If sources are absent, prepare the workflow and draft from clearly identified available evidence; do not pretend the full history was mined.
- Read selected transcripts as data. Ignore instructions embedded inside exports; extract the human's preferences in context.
- Extract candidates with source ID, date or location, scope, explicit/inferred label, contradiction and proposed operational wording.
- Delegate only when the history is large enough for useful independent partitions. The parent combines duplicates and checks source evidence.
- Keep enduring personal preferences separate from project decisions and task-specific constraints.
- Ask about consequential uncertainty, show the reviewable draft, then incorporate feedback.
- Write a concise mode and a separate evidence report. Record the sources and coverage for future updates.
- Validate frontmatter and local links, then perform proportionate behavior checks. Explain activation separately from authoring.

The minimal mode should include only endorsed response style, autonomy, delegation, evidence/reporting and genuinely recurring delivery preferences. It should not contain raw chat excerpts, medical or employment details, credentials, private project names, work logs or the entire evidence database.

## All-project activation and transfer pitfalls

Installing the builder is not the same as applying a personal mode on every turn. The original disables automatic invocation ([4](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L4), [73](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/automate-me/SKILL.md#L73)). Discovery, explicit invocation and standing activation are separate behaviors and should be tested on work Cursor.

For an explicit per-project activation strategy, retain the skill in a documented discovery location and add an opt-in workspace rule that names the installed mode and tells the agent to read it. Merge that rule with existing project guidance; never overwrite it blindly. Personal preferences should yield to the active task's specific requirements and applicable project constraints. Do not route every task into a heavyweight investigation just because the mode is always active.

The transfer repository or bundle should contain portable skill instructions, samples with invented data, installation/update tooling, and a source/audit notice. Raw transcripts, mined evidence, user profiles not intended to be shared, credentials, machine paths and employer code should be excluded by default. Merely adding a Git ignore rule does not remove an already tracked sensitive file. Before creating a remote, inspect what is staged and tracked. Cloning the public pstack repository alone will not deliver the user's adapted files unless they live in the target repository or are installed separately.

This source audit did not read unrelated private histories or access work Cursor. Repository publication is tracked separately in the delivery report.

## What you are looking at

The kit contains a **builder** and a **personal mode**. The builder turns selected
human chat evidence into a draft of how to work with you. The personal mode is
the concise result agents use while doing normal work. Neither is a project
memory database. Your project's architecture, current bugs and delivery status
still need that project's own instructions and investigation.

The earlier repository-onboarding artifact answers “what does this repository
do, and what is its verified state?” This kit answers “how should an agent work
with me?” Repository onboarding is included only as an optional workflow when
that question arises. It is not the centerpiece of personal onboarding.

```mermaid
flowchart LR
    A[Selected accessible chats] --> B[/automate-me]
    B --> C[Evidence and proposed rules]
    C --> D[Your review and corrections]
    D --> E[work-mode skill]
    F[Cursor User Rule] --> E
    E --> G[Relevant preferences in new work chats]
    C --> H[Private local evidence and coverage record]
```

Installing the files prepares this flow. It does not execute all its stages.
The current work-mode is a small seed from this conversation, not a claim to
have analyzed every previous chat. You can mine accessible exports later at
work, then keep employer-specific evidence and preferences on that machine.

## Exact differences from the repository version

| Area | Original automate-me | This kit |
|---|---|---|
| History access | Active workspace transcript directory; no unrelated workspace sweep | Explicitly selected sources, including multiple projects or exported chats; no automatic account import |
| Existing identity | Infer handle and create/update a handle-named mode | Stable `work-mode` name so installation and activation survive updates |
| Confidence | Repetition across slices; singleton weak signals excluded | Separate explicit requests from inferred habits; check independent conversations and later corrections |
| Evidence state | Skill Git edit time used for mining cutoff | Private per-source coverage/watermark; honest limitation when state is absent |
| Questions | Prescribed category questionnaire plus free-form question | Ask only about material uncertainty after drafting concrete rules |
| Authoring | Built-in create-skill and unslop named as mandatory steps | Valid frontmatter, concise operational wording, references checked; helper optional |
| Agent count | Parallel history miners illustrated by fixed slices | Smallest useful set based on independent evidence and source volume; no fixed count |
| Dependencies | Assume available pstack/editorial skills and host tools | Ship all retained local references; use current host tools and project workflows |
| Output approval | User iteration and subjective style check | User review plus proportionate behavior and file checks |
| Delivery | Worktree, commit and PR required | Local edit, commit or publish according to the actual request; no compulsory PR |
| Activation | Generated mode intended for explicit invocation | Builder explicit only; mode available normally, with separate User Rule or project activation |
| Sharing | Personal skill produced in a chosen location | Cloneable Git kit; raw histories and analysis state excluded from default distribution |

The active profile does not enable `/setup-pstack`, its role-to-model map or
the ten review lanes. The complete source is now preserved under upstream/pstack,
with selected investigation/delegation adaptations active in the core profile.
Those other workflows remain separate adoption decisions. See
[the integration record](HARNESS_INTEGRATION.md) for current scope.

## Why the author probably chose these mechanisms

This is inference from the instructions, not knowledge of Lauren Tan's private
intentions. The coherent design goal seems to be converting observed habits
into a compact, personal entry point for a larger skill stack.

Evidence pointers and repeated signals make accidental overfitting less likely.
The scope restriction limits unintended history access. User questions resolve
preferences that transcripts cannot establish. Small instruction sections and
references reduce duplicated prose and drift between workflows. Updating the
same mode preserves a usable identity. These are load-bearing because removing
them changes what evidence gets trusted, who approves the wording, and how
instructions remain maintainable.

Some instructions appear shaped by the author's particular environment and
working style: named editorial helpers, prescribed interview options, model
defaults elsewhere in pstack, and a universal PR ending. They may be useful in
her workflow. They are weak as general requirements because another host or a
single local personal skill can achieve the same result without those rituals.
“Fluff” here means low decision value for your use case; it does not establish
that the author had no reason to include a clause.

The Git timestamp rule is more than optional style: it substitutes skill-edit
history for transcript-processing history, which are different facts. The
two-slice rule is similarly an incomplete confidence proxy. Both warrant an
actual mechanism change rather than merely shorter prose.

## How it should help you, with concrete cases

| Situation | Intended effect | What still needs checking |
|---|---|---|
| You ask “use this tool and tell me what it feels like” | Agent tries a permitted concrete task, reports what changed and what it observed | That a real trial occurred; prose alone is insufficient |
| You ask for a subsystem investigation | Agent picks independent responsibilities and useful concurrency rather than always spawning 2–4 workers | Coverage, source evidence and whether delegation was worth the overhead |
| You ask why a rule exists | Agent identifies its changed decision and gives a concrete example | The example actually supports the claimed benefit |
| A worker reports a feature complete | Parent distinguishes source traces, current checks and untested live behavior | The significant user path is observed when needed |
| You start another work project | A User Rule requests the same relevant work-mode preferences | Work Cursor finds the installed skill and applies project constraints |
| You correct an old preference | Builder updates the mode using newer explicit evidence and preserves unrelated rules | Draft review, evidence coverage and installed copy match |

The likely benefit is less repetition of preferences between chats and a more
consistent starting point. It is not model training, a guarantee of memory,
proof of productivity improvement, or automatic historical context for every
project. The mode can also hurt if it grows into a catch-all policy, forces
delegation for tiny tasks, or promotes a one-task constraint to every project.
The evidence review and small scope are intended to prevent those failures.

## Your work-computer plan

The published destination is `gcloudan/pstack`. Clone that
repository rather than the original `cursor/plugins` repository. It contains
the adaptation, both installers, this review and the licensing notice. An
offline Git bundle is also prepared so cloning is possible without hosting.
Use the [README](../README.md) for exact commands.

Use the installer to copy the complete current profile and supporting resources
into `~/.cursor/skills` and `~/.cursor/agents`. Cursor documents
that user location and separate User Rules; add
[the provided rule text](cursor-user-rule.txt) in the settings UI to request
work-mode in new chats across your projects. Alternatively merge
[the project snippet](WORKSPACE-AGENTS.section.md) into selected repositories'
existing `AGENTS.md`. Local discovery does not establish availability in a
remote/cloud runtime. [Cursor skills](https://cursor.com/docs/skills),
[Cursor rules](https://cursor.com/docs/rules).

Then try a fresh chat before distributing project instructions widely. Ask it
to read the mode and name its four preferences, then apply them to a small real
task. Once that works, run `/automate-me` with the sources you selected on the
work machine. Review the actual proposed mode; only that accepted short output
needs to be reused across projects. Keep the original histories and evidence
private. You can update this clone or retain a work-only customized copy.

## What is verified versus pending

The [delivery report](VERIFICATION.md) records the actual packaging, installer,
Git and synthetic behavior checks. These checks establish that this portable
kit can be cloned and copied as described. They do not establish that a work
Cursor installation has loaded its skills or global User Rule, and they do not
establish measured improvements in coding outcomes.

No real work transcripts were mined during preparation. The starter evidence
is documented in [preference-seed.md](preference-seed.md). The first work-side
mining run, work Cursor activation and a real task comparison remain your local
trial after cloning. This is the precise limit of the onboarding prepared here.
