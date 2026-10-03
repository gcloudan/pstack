# What to adopt from the whole pstack

Prepared 3 October 2026 for your future Cursor work setup. Audited snapshot:
`23e4138daa01c42d4969f7a5465f82704e64f798`, plugin version 0.15.6.

**Recommendation: adopt a task-routing system backed by focused investigation,
scoped delegation and real verification. Personalize its defaults. Keep the
expensive review, experimentation and overnight machinery situational.**

My earlier delivery concentrated on personal preference mining. That was too
narrow. `/automate-me` is one way to personalize the system below; it is not
the system you are deciding whether to adopt. The repository now preserves the complete upstream source and ships a first
investigation/delegation integration. See HARNESS_INTEGRATION.md for active scope.

These ratings are engineering judgments for your expressed preferences:
concrete trials, explanations of mechanisms, useful agents without fixed counts
or micromanaging, and evidence behind completion claims. They are not measured
productivity scores. Your work language, tooling and delivery policy can change
the value of the situational features.

## What pstack actually contains

| Layer | Actual contents | What you gain |
|---|---|---|
| Main router | `poteto-mode`, 23 playbooks | Describe the outcome; an agent selects an engineering workflow rather than making you name every skill |
| Workflow library | 24 other public skills | Investigation, design, parallel work, review, verification, explanation, personalization and tool setup |
| Engineering principles | 24 additional principle skills | Named reasoning checks and constraints that steer the workflows |
| Worker definitions | `poteto-agent`, Comment Sicko | Instructions for a delegate to read/apply the mode, and a comment-review specialization |
| Executable helpers | PR watcher, coordinator state CLI, plan checker, decision-log writer, worktree audit, dependency bootstrap | Some instructions have actual code for polling, state and format checks |
| Setup/adoption | `setup-pstack`, `automate-me`, guide | Select available model roles and derive personal working preferences |
| Optional automation pack | Benny, with three separate setup/triage/fix skills | A Slack bug-report-to-reproduction/fix workflow, dormant until set up |

Inventory: **49 public SKILL.md files = 25 ordinary skills + 24 principles;
23 router playbooks; two agent definitions; three extra Benny skills outside
the public skills directory.** The manifest registers `skills/` and `agents/`.
Benny is a separate setup, not three automatically active slash skills.
Source: [plugin manifest](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/.cursor-plugin/plugin.json),
[source tree](https://github.com/cursor/plugins/tree/23e4138daa01c42d4969f7a5465f82704e64f798/pstack).

Most of the stack consists of instructions, templates and reference prompts.
Cursor supplies agent tools, model access and scheduled loops. MCP connectors
supply tracker/chat/observability access. The helpers do specific jobs; there
is no universal scheduler here that makes every prompt rule execute reliably.
The main mode also embeds the author's writing style, tool choices and autonomy
policy. Those can be separated from the workflow mechanisms.

## The flow you would be adopting

```mermaid
flowchart TD
    A[You give an outcome and completion evidence] --> B[Your mode routes the task]
    B --> C[Understand relevant code and constraints]
    C --> D{What work is needed?}
    D --> E[Reproduce and fix]
    D --> F[Design and build]
    D --> G[Investigate or explain]
    D --> H[Measure and improve]
    E --> I[Delegate useful independent responsibilities]
    F --> I
    G --> I
    H --> I
    I --> J[Parent checks outputs and resolves contradictions]
    J --> K[Relevant tests and real behavior evidence]
    K --> L[Report or deliver within authorized scope]
    M[/automate-me: selected history and your corrections] --> N[Personal defaults]
    N --> B
    O[/setup-pstack: available model roles] --> I
```

For example, “the export duplicates rows on retry; reproduce it, fix it and
show me that retry works” should select a bug workflow. The parent can give one
worker ownership of reproducing the failure, another an independent caller or
persistence check if useful, and keep implementation ownership clear. You do
not need to dictate their searches. Their brief needs the question, scope,
relevant sources, done predicate and evidence contract. The parent still owns
the answer and the delivered change.

For a tiny, single-path bug, the same workflow may need no workers. For a wide
migration it may need many units, with only a few running concurrently. The
number of scenarios, total workers and concurrency limit are different numbers.
This is the delegation behavior I recommend carrying over.

## Rating key

- **5/5: carry over as a core mechanism.** Adapt the stated defaults.
- **4/5: strong feature to retain, invoked when relevant.**
- **3/5: useful after adaptation, or only for a matching workflow.**
- **2/5: borrow selected ideas; substantial stock assumptions or low immediate need.**
- **1/5: leave out of the initial setup, or reject the particular default.**

Scores rank carry-over value after the changes described. They do not mean
every 5/5 skill should run on every task. Source names below correspond to the
[skills directory](https://github.com/cursor/plugins/tree/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills).
The detailed appendices retain the reviewers' independent, sometimes more
conservative ratings of the stock instructions. These main tables are my
synthesis of what to preserve after adaptation, rather than an agreement score.

## All 25 ordinary skills, ranked for your adoption

| Skill | Score | What is worth adopting | Change or limit |
|---|---:|---|---|
| `poteto-mode` | 5 | A single entry point that selects the workflow, coordinates tools and checks delivery | Fork the router into your mode; remove compulsory ceremonies, author's prose rules and broad external-action grants |
| `how` | 5 | Trace actual callers/data flow before relying on documentation; split a complex subsystem into distinct questions | Replace fixed 2–4 explorers; let a small question finish directly rather than always hand it to an explainer |
| `blast-radius` | 5 | Identify the one or two facts a change's safety depends on and prove them with real code | Keep proportionate probes; do not require multiple models for a tiny change |
| `swarm` | 5 | Scoped coverage workers, explicit done predicate, isolation, exact revisions, evidence and one aggregated report | Adapt Task/cloud fields; choose size and concurrency from coverage, tools and budget |
| `create-verification-skill` | 5 | Build a reusable project-specific launch/drive/observe/cleanup recipe and feature map, then execute a real feature | One successful feature is a seed, not whole-app coverage; use the work project's actual tools |
| `maintain-verification-skill` | 5 | Detect drift between source, runbook and actual app; distinguish harness gaps from product failures | Batch source readers; one owner of shared live state; run at relevant checkpoints |
| `architect` | 4 | Establish caller-facing types, ownership and module shape before implementation; revise a wrong sketch | Trigger for consequential boundaries, not every function call; competing designs only when useful |
| `why` | 4 | Reconstruct design rationale from commits, issues, docs and other available evidence; label inference | Query relevant sources rather than all categories; absent MCPs stay absent; history does not override current code |
| `recall` | 4 | Recover your previous decisions and in-flight context into a current-state brief | Explicit source scope; distinguish old intent from today's code; it is retrieval, not lasting memory |
| `interrogate` | 4 | Independent adversarial reviews with common intent/context; parent deduplicates, checks and explains dispositions | Scale panel to risk; agreement is a prioritization signal, not proof; avoid automatic scope growth |
| `arena` | 4 | Independently build/design alternatives, compare actual artifacts and combine the best parts coherently | Extra candidates and judging have overhead; use when the choice matters; verify the combined output |
| `tdd` | 4 | Capture an affordable failing behavioral test before fixing a regression | Not a requirement to invent a test for every reversible prose or cosmetic change |
| `benchmark-checklist` | 4 | Check errors, completed work, realistic conditions, A/B comparability, variability and the limiting work | Useful when reporting a measurement; sample counts and platform commands need adaptation |
| `teach` | 4 | Combine implementation and rationale into an explanation that develops your understanding | Do not automatically pay for both full investigations when a direct explanation suffices |
| `figure-it-out` | 4 | Construct a bespoke workflow when a stock playbook cannot cover the job; make completion auditable | Adapt its broad intervention and delivery defaults; avoid designing an elaborate process for small work |
| `show-me-your-work` | 4 | A decision trail recording what changed, why, evidence and result, useful while you are away | Record consequential decisions rather than every command; local log by default unless sharing is requested |
| `automate-me` | 4 | Personalize the working mode from selected human evidence and your review | Adoption mechanism; preserve the router explicitly; fix confidence, cutoff and dependency assumptions |
| `technical-writing` | 4 | Write for the reader's task, with concrete names, conditions and expected outcomes | Keep clarity; relax rigid punctuation, sentence and document-shape rules |
| `bro` | 4 | A direct “say that plainly” repair command | Keep optional; the normal answer should already be understandable |
| `typescript-best-practices` | 3 | Useful concrete type/boundary patterns when your project uses TypeScript | Verify examples rather than copy every claimed invariant; not a global requirement for other languages |
| `setup-pstack` | 3 | A shared mapping from roles to available models, so each workflow reads one policy | Model/budget presets are choices; don't import slugs; preserve exact custom settings on rerun |
| `reflect` | 3 | Convert recurring execution failures into a reusable correction, preferably a script or structural check | One retrospective need not require a four-agent panel; incident scope is not permanent global policy |
| `unslop` | 3 | Remove filler, vague claims and unnecessary jargon | Keep meaning and natural language; wholesale word/punctuation bans are the author's taste |
| `no-comments` | 2 | Review narration, stale explanations and comments compensating for an unenforced invariant | Reject deletion on ambiguity; preserve contracts/legal notices/useful constraints until a replacement is verified |
| `make-bot-ui` | 1 | A specialized dashboard-to-bot webhook workflow | Leave out initially: Grok Bot, sender keys and Tailscale are a separate infrastructure use case |

The highest-value addition beyond what I already built is **a task router plus
actual project verification recipes**, not another personal-style paragraph.
`how`, `blast-radius` and `swarm` supply the investigation/delegation contracts
around those recipes. The bug/feature/refactor playbooks connect the pieces.

## All 23 playbooks

These are routes inside the mode, not 23 independent agent tools. Scores are
about retaining the workflow, not enabling automatic execution or merge.
Source: [playbooks](https://github.com/cursor/plugins/tree/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/poteto-mode/playbooks).

| Playbook | Score | Carry-over decision |
|---|---:|---|
| Investigation | 5 | Read-only, source-backed answers; preserve scope and separate implementation from intent |
| Bug fix | 5 | Reproduce, root-cause, fix and verify on the affected surface; delivery follows the request |
| Feature | 5 | Define data/ownership, implement behavior and demonstrate it; reduce mandatory architecture/arena/delegation for small features |
| Refactoring | 5 | State preserved behavior and compare before/after; avoid automatic expansion into redesign |
| Prototype | 4 | Settle observable unknowns cheaply; a genuine product/preference decision still belongs to you |
| Perf issue | 4 | Trace a real slow path and compare with a valid baseline; avoid optimizing a convenient unrelated number |
| Hillclimb | 4 | One hypothesis/change/measurement loop with regression gates and accepted-win records; stop on budget/noise, not fixed attempts |
| Runtime forensics | 4 | Useful live diagnosis; explicitly authorize instrumentation that changes running state despite the read-only label |
| Trace forensics | 4 | Use captured profiles/traces for diagnosis; do not invent a runtime observation from a static trace |
| Session pickup | 4 | Restore brief, branch, current state and evidence; prior summaries are leads, not current proof |
| Pause safely | 4 | Stop writers, externalize recoverable state and leave a resumption brief; distinguish explicit pause from routine progress |
| Authoring a skill | 4 | Focused instructions, reference validity and behavioral checks; no universal PR requirement |
| Eval | 4 | Freeze tasks/rubric, compare variants with blinded judging and tool/artifact evidence; use representative repetitions before a broad conclusion |
| Babysit | 4 | Triage actual CI/review/conflict status and bound polling; merge authorization remains a separate choice |
| Opening a PR | 4 | Ordered commits, useful intent and validation evidence; allow drafts and local-only outcomes according to project policy |
| Autonomous run | 4 | A countable done predicate, bounded scope and decision trail; clear stop conditions and budget |
| Visual parity | 3 | Compare controlled visual states; realistic tolerances plus interaction checks rather than unconditional zero pixels |
| Multi-phase plan | 3 | Dependencies, ownership and evidence contracts are valuable; replace fixed lane counts and universal perf/screenshots/video |
| Shipping | 3 | Verify the relevant revision before landing a contiguous stack; automatic merging requires the actual task's authority and work policy |
| Autopilot-stack | 3 | Independent implementation with one integration owner and a reviewed linear stack; retain when you want to land it yourself |
| Worktree cleanup | 3 | Inventory candidates and preserve recoverability; adapt OS commands and never equate scratch files with disposable work |
| Orchestrate | 2 | Good for a real multi-day fleet: durable briefs, single writers, ledger and frontier; heavy for daily tasks and currently Graphite-dependent |
| Autopilot-full | 2 | PR owners plus fresh verification rounds can serve a trusted queue; initial adoption should not assume automatic merges/cloud fleets |

## All 24 principles

The principles often overlap with the workflows. I would preserve their
decision-changing checks, not require the agent to recite principle names in
every reply. Source: `skills/principle-*/SKILL.md` in the pinned tree.

| Principle | Score | What to retain or change |
|---|---:|---|
| prove-it-works | 5 | Inspect the real artifact/behavior; label tested scope and unobserved integration |
| fix-root-causes | 5 | Follow the causal path rather than suppress the symptom |
| sequence-verifiable-units | 5 | Deliver units whose evidence can be checked before the next dependency |
| model-the-domain | 5 | Put ownership/state relationships in an explicit structure rather than scattered assumptions |
| make-operations-idempotent | 5 | Retry/partial-run behavior should converge instead of duplicating work |
| separate-before-serializing-shared-state | 5 | Remove unnecessary shared writes; one writer when sharing is a real invariant |
| encode-lessons-in-structure | 5 | Prefer an enforceable check or tool over another repeated instruction |
| boundary-discipline | 4 | Validate at actual trust boundaries; do not blindly trust internal values crossing an implicit boundary |
| type-system-discipline | 4 | Encode meaningful states and validate external data; types alone do not prove every runtime invariant |
| test-behavior-not-implementation | 4 | Assert relevant observable behavior; correct the overbroad assertion heuristic discussed below |
| explain-the-number | 4 | Establish what was measured and why the comparison answers the question |
| guard-the-context-window | 4 | Scope and summarize bulk work; extra agents are useful only when they save useful context/work |
| foundational-thinking | 4 | Clarify data structures and shared ownership before committing to logic |
| attack-the-premise | 4 | Repeated failed fixes should trigger reconsideration of the assumed cause |
| minimize-reader-load | 4 | Reduce hidden state and unnecessary indirection; don't delete a boundary merely because it has one caller |
| experience-first | 4 | Judge the user-visible outcome and polish; concrete acceptance criteria make this operational |
| never-block-on-the-human | 4 | Complete authorized reversible work without repeated permission requests; keep real external-action boundaries |
| laziness-protocol | 4 | Prefer the smallest sufficient change; deletion itself is not proof of simplification |
| subtract-before-you-add | 3 | Remove proven obsolete pieces; not a mandatory destructive cleanup phase before every feature |
| build-the-lever | 3 | Make a repeatable tool when repetition or verification justifies it; don't script every one-off edit |
| redesign-from-first-principles | 3 | Explore a coherent design when a new requirement breaks the old model; don't mandate a rewrite |
| outcome-oriented-execution | 3 | Avoid throwaway intermediates in a controlled migration; compatibility can be necessary for rollout |
| migrate-callers-then-delete-legacy-apis | 3 | Good for controlled internal callers; not safe as a universal rule for public APIs or staggered deployments |
| exhaust-the-design-space | 3 | Compare meaningfully different alternatives when a choice is consequential; no fixed prototype count |

## The two workers, actual code and optional packs

| Component | Score | Value and boundary |
|---|---:|---|
| `poteto-agent` wrapper | 4 | A worker reads the actual mode before acting; adapt to `work-agent` and your chosen router so author defaults don't re-enter through delegates |
| Comment Sicko | 2 | A focused comment/invariant lens; use a read-only report followed by reviewed edits, rather than ambiguous deletion |
| `watch-pr` helper | 4 | Actual PR/stack polling, explicit blockers, query-error/backoff policy, frozen queue and structured status; requires Bun/dependencies and authenticated GitHub tooling |
| `orch` state CLI | 3 | Actual plain TSV/JSON units, inbox, gates, status and PR/SHA ledger; atomic writes/PID locks; stock frontier resolution assumes Graphite |
| `check-plan.mjs` | 2 | Actual structural checking; preserve evidence-schema checks but change fixed counts/prose rules; it does not verify behavior |
| `show-me-your-work/scripts/log.sh` | 4 | Small actual append-only TSV writer, cell sanitization and spreadsheet-formula protection; shell availability and writer ownership still matter |
| `worktree-audit.sh` | 2 | Read-only candidate report, not deletion; macOS-oriented commands, path parsing and incomplete remote state need adaptation before trusting buckets |
| `bootstrap.ts` | 3 | Hashes package/lockfile and installs frozen dependencies when needed; first helper invocation can install packages, so this needs to match the work environment |
| Benny setup | 2 | Copies a configurable automation pack into a project and keeps user configuration separate; a later opt-in infrastructure project |
| Benny triage | 3 | Evidence-based classification of incoming reports can be useful if Slack is a real work intake channel |
| Benny reproduce/fix | 3 | Confirm a report on the real surface before fixing; requires app driving, repositories, credentials and explicit message/delivery authority |
| Guide and examples | 4 | Good onboarding around goal + checkable outcome; treat claims and recipes as prompts to validate, not executed receipts |

The helpers are stronger than plain advice for the specific operations they
implement. They cannot determine whether an agent's `live-ui-verified` label
was honestly established. Evidence inspection and project checks remain part
of the parent workflow. Existing helper tests are present, but the Bun test
suite was **not run here** because Bun/dependencies were unavailable.

## What is load-bearing, versus style or ceremony

| Preserve | Why it changes the outcome |
|---|---|
| Route by actual task and completion predicate | A diagnosis, fix, prototype and migration need different evidence and delivery |
| Read caller paths, ownership and actual versions | Prevents a plausible answer about an unused or obsolete implementation |
| Brief independent responsibilities and clear write ownership | Lets workers choose their methods without overlapping edits or losing the user's scope |
| Parent owns synthesis and checks contradictions | Prevents forwarding confident worker reports as if they were verification |
| Bind receipts/verdicts to the relevant revision | Old checks cannot silently approve new code |
| Observe the consequential behavior and preserve evidence | A checklist, compilation or model agreement is insufficient for a live claim |
| Durable state for genuinely long runs | Work survives context changes, stopped agents and restarts |
| Explicit personal/project/source boundaries | One incident or one project's policy cannot quietly become a rule for every project |

| Adapt or omit | Why it does not deserve universal status |
|---|---|
| Always 2–4 explorers or ten live lanes | Preset counts do not establish useful coverage |
| Always design twice, always a multi-model panel | Diversity can help; unnecessary duplication can consume the parent review budget |
| Mandatory architecture for every function boundary | An ordinary helper call is not automatically an architectural decision |
| Always open a ready PR, never draft | Delivery/review policy belongs to the work project and current request |
| Always live + perf + screenshots + video for every PR | Applicability matters; a docs edit and a latency change need different checks |
| Punctuation bans and forced named-principle citations | The author's expression preferences, not verification mechanisms |
| Delete ambiguous comments | Removes potentially useful constraints before understanding or replacing them |
| Automatic team-chat/ticket actions | A personal preference skill does not establish permission to speak for you |
| Copying specific model slugs/budget mappings | Runtime availability and measured task quality should determine the choice |

Some prescriptions are useful in a high-throughput environment with app-driving
tools, cloud workers and a frequent-PR culture. They become ceremony when copied
into a different environment without those conditions. This is not a claim that
the author had no reason for them.

## Source claims that need care

**The ten lanes are not ten named review specialties.** In the multi-phase
plan, lane 1 compares a regression scenario with trunk. Lanes 2–10 are
scenario/screenshot/pass-predicate placeholders. The plan separately asks for
one gates lane, one perf lane and at least two audit lanes: at least 14 verifier
workers in that prescribed round, apart from owners/coordinator. The sensible
carry-over is a justified coverage matrix, not filling nine slots to satisfy
the number. `interrogate` is separate: default model reviewers share a rubric.
Source: [multi-phase plan](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md#L65-L76).

**I ran the plan checker.** The original template with the model filled passed
with zero screenshots and no executed boxes. Removing lane 10 failed with
“expected 1 to 10.” That proves format/count enforcement, not safe execution.
The local probe is `audit/probe_pstack_plan.py` in this investigation workspace;
it is not an app test and not part of the installed skill kit.

**Test quality is valuable; one assertion claim is inaccurate.** The
test-behavior principle lists `toBeDefined`, `toBeTruthy`, `toBeInstanceOf` and
positive-value assertions among shapes supposedly still passing when imported
functions return undefined. On the subject's returned value, those assertions
would fail. A weak smoke test may need strengthening; it should not be deleted
because this generalization says it detects nothing. Source:
[test-behavior principle](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/principle-test-behavior-not-implementation/SKILL.md#L15-L18).

**A claimed type invariant is not established by the example.** The TypeScript
example says start + duration prevents negative ranges, but `durationMs: number`
still accepts a negative number. It needs construction/validation enforcing
non-negativity if that is the actual invariant. Keep the data-model idea; fix
the example. Source: [type patterns](https://github.com/cursor/plugins/blob/23e4138daa01c42d4969f7a5465f82704e64f798/pstack/skills/typescript-best-practices/references/patterns.md#L74-L84).

**Model setup is configuration, not optimization proof.** The previous setup
audit found that reruns can rebuild default effort suffixes for a same-family
role even when the prior slug differed. The broad “preserves non-default
models” description is not a promise to preserve every exact customization.
No model-role optimality or spend reduction was measured here.

The setup writes `~/.cursor/rules/pstack-models.mdc`. That source instruction
does not establish that an arbitrary user-global rule file is discovered by
your work Cursor. Verify the loaded configuration or use a supported User Rule
or project rule instead of assuming the file applies everywhere. Current
[Cursor rules documentation](https://cursor.com/docs/rules) distinguishes
project rule files from global User Rules.

**Some read-only labels conflict with instructions.** Runtime forensics can
inject instrumentation or hotfix live code. Comment Sicko's instructions
describe edits despite read-only descriptions elsewhere. Interpret actual
actions and permissions, not the label alone.

**The coordinator assumes infrastructure that other routes avoid.** Ordinary
PR routes allow GitHub/Origin without requiring `gt`; Orchestrate derives its
stack frontier from Graphite. Its durable-state invariants are portable, but
its stock frontier is not a generic plain-Git implementation.

Some long-run recipes also read `origin/main:pstack/...` paths every tick.
Installing a plugin in its cache does not put those files in every project's
trunk. A fork must either vendor them at the named paths or adapt the loader.
The broad mode says to open a PR at the end of other playbooks, but the
Investigation leaf explicitly says no PR. Preserve the specific read-only
contract instead of turning an explanation into delivery ceremony.

## Why the author appears to have built it this way

The README states an aim of less, higher-quality code and reliable parallel
work. The mechanisms support an interpretation: reduce individual-agent drift,
settle risky design choices before code grows, make evidence reviewable, then
scale independent ownership. The wrappers keep workers on the same workflow;
the router makes the library usable without memorizing commands; state and
watchers address the failure modes of long PR programs.

This is an interpretation of public instructions, not access to her private
intentions or a controlled effectiveness study. There is direct history showing
attention to instruction cost: commit
[b0b9c7a](https://github.com/cursor/plugins/commit/b0b9c7a) says it cut 19
instructions the selected model followed without the text. That supports your
question about unnecessary rules. It does not prove every retained clause is
needed or every removed clause is redundant for your models.

## What I would carry into your work setup

**First, the core system:** a personal router, relevant `how`/`why` investigation,
`blast-radius`, adaptive `swarm`, bug/feature/refactor workflows, behavioral
verification principles and a project-local verification skill. Add clear
briefs, parent review and authorized autonomy. These are the pieces that let
you name a result rather than micromanage the steps.

**Keep available for matching tasks:** `architect`, `arena`, `interrogate`,
`tdd`, perf/benchmark/hillclimb, trace diagnosis, teaching/recall, session
pickup/pause, skill evaluation and a decision trail. Invoke them when they can
change the decision or establish missing evidence.

**Later, if your work calls for it:** PR watchers, stack shipping, autonomous
queues and the coordinator. Begin with one real unit and check the entire
brief → implementation → evidence → delivery path before a fleet. Benny and
bot dashboards are separate opt-in integrations.

**Leave out as general rules:** fixed counts, always-PR/never-draft policy,
mandatory giant reviews for tiny tasks, automatic messages, aggressive comment
deletion and author-specific prose/model presets.

## How adoption and cloning should actually work

Your target repository is `gcloudan/pstack`. It now holds the complete pinned
upstream package plus the adapted seven-skill core, worker and these reviews.
Only profile-listed adaptations are installed; ratings are not activation.
The repository is published at
[gcloudan/pstack](https://github.com/gcloudan/pstack); SSH access and the pushed
commit were checked on 3 October 2026.

For the full system, there are two legitimate paths:

| Path | What it means | Fit for your request |
|---|---|---|
| Install upstream pstack as a Cursor plugin | Preserve its package, agents, references and helpers; configure/personalize it | Convenient for a stock trial, but retains author assumptions unless intentionally changed |
| Maintain your fork with selected mechanisms | Keep upstream source/provenance separate from adapted router/workflows; ship dependency-complete selections and work activation | Best fit for inspecting, choosing and owning your system |

I recommend the second path for your stated goal. A proper fork should keep an
audited upstream snapshot, a decision map of kept/adapted/omitted features, your
router and worker wrapper, and complete selected skill directories including
references/scripts. Blindly copying SKILL.md files loses dependencies. Merely
copying a new personal-mode file does not compose the base router for you.

`/automate-me` would then edit a **personal preference section** of your mode,
from selected chats and explicit direction. The mode's routing table still
names the workflows we actually shipped. `/setup-pstack` would map roles to
available models where you choose that policy. A worker wrapper should read
your mode, and retained workflow worker references should be adapted too,
otherwise delegates may reload the original author's wrapper.

You do not need to modify Cursor itself. Cursor documents user skill folders
such as `~/.cursor/skills` and custom subagent definitions in its own supported
locations. A loader/installer must place these resources where your work Cursor
can discover them; execution still uses its actual tools. Local files are not
automatically present on every remote/cloud machine. See
[Cursor skills](https://cursor.com/docs/skills),
[Cursor subagents](https://cursor.com/docs/subagents),
[Cursor plugins](https://cursor.com/docs/plugins).

Across projects, share the general router and personal defaults. Keep launch
commands, test gates, product constraints, credentials and delivery policy in
the workspace. Test adoption on one real work task before declaring it active
everywhere. You give the outcome and acceptable evidence; the adapted system
selects the workflow and worker responsibilities.

## Evidence and remaining limits

This review combines three source audits, direct inspection of the main router,
manifest and helpers, earlier scoped trials, and the current Node plan-checker
probe. Read the detailed source audits for exact clauses and dependencies:

- [Engineering workflows and all principles](source-audits/PSTACK_WORKFLOW_FEATURES.md)
- [Verification, reviews, experiments and writing](source-audits/PSTACK_VERIFICATION_FEATURES.md)
- [Coordination, adoption and integrations](source-audits/PSTACK_COORDINATION_FEATURES.md)
- [The narrower automate-me review](AUTOMATE_ME_REVIEW.md)

The score is about useful mechanisms and stock assumptions. It is not a claim
that all 49 skills were executed or that multi-model work improves every task.
The previous trials exercised selected onboarding/fix behavior, not the entire
library. No work-machine Cursor configuration, employer integrations, live
PR fleet or full upstream Bun test suite was verified here. The first dependency-complete investigation/delegation batch is now prepared
and exercised. Most rated workflows remain preserved for later integration;
see [the integration record](HARNESS_INTEGRATION.md).
