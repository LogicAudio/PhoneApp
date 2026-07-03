---
name: agentic-human-coexistence
type: reference
governs: []
read_when: Bootstrapping this human+agent repo structure in ANOTHER repo (hand this doc verbatim to that repo's agent), or asking why THIS repo is structured the way it is.
spec_version: 1
---

# Agentic–Human Coexistence — the portable repo operating system

## §0 · What this is and how to use it

This document is the **portable specification** of a human+agent repo operating system — the
structure its origin repo runs on and any repository can adopt. It has two uses:

1. **In this repo** — it explains *why* the structure exists (read §1–§2 and stop).
2. **In any other repo** — hand it **verbatim** to an agent as its build instruction. §3–§9 are the
   contract; §10 is the procedure that installs it. Works for any language or domain (a Python web
   service, a C++ audio plugin, an ML toolbox).

To bootstrap a new repo, give the agent this file plus exactly this prompt:

```text
Read the attached agentic-human-coexistence.md in full. Then execute its §10 Bootstrap
Procedure in this repository, starting with the §10.1 interview. Do not create or
modify any file before the interview is complete.
```

**Durability rule.** This spec is written to stay valid for ~10 years: it names no AI models, no
vendors, no prices, no context sizes in anything durable (see §12). The canonical home of this spec
is its **own dedicated repository**, which ships this file together with the reference gate engines
and templates. Every product repo — including the one this copy lives in — is a downstream copy: it
saves the spec as `Knowledge/agentic-human-coexistence.md` (§10.3 artifact 8) and records the
`spec_version` it was built from in its map file. **Upgrading** = fetch the canonical spec, diff it
against the recorded version, and apply the delta as a normal plan. Copies are never edited
independently — an improvement discovered downstream is contributed to the canonical home first,
bumps `spec_version` there, and flows back out to the fleet.

Reading order for the impatient: **§2** (the shape), **§10** (the procedure). Everything in between
is the contract §10 implements.

---

## §1 · Philosophy: humans and agents coexist

**The coexistence principle.** Humans and agents work in the same repository as peers. Each can read
the whole system; each has a single source of truth; **neither edits the other's artifacts**. The
human curates intent (invariants, assumptions, notes); the agent produces derived work (code, analysis,
generated data); deterministic scripts verify both. A repo is healthy when a human away for three
months and an agent spawned three minutes ago can both orient themselves from the same files, unaided.

**The moat argument.** Models improve every year and are interchangeable — they are plug-ins. What
compounds is everything the models plug into: encoded domain knowledge, named invariants, frozen
verified baselines, procedures written down, and a **uniform structure** repeated across every repo
the company owns. A new model (or a new hire) dropped into a conforming repo is productive
immediately, because the repo itself teaches them. That accumulated, machine-checkable knowledge is
the moat; the model never is.

**One fact, one home.** Every fact lives in exactly one file; everything else links to it.
Dual-maintenance (a README mirroring a map, a rule repeated in a skill) always ends with the two
copies disagreeing. Cross-link, don't copy.

**The rot theorem.** *Every tracked convention either has a deterministic checker or it rots.*
This is empirical: in the origin repo, plans (checked by a script) stayed pristine for hundreds of
commits, while the bug tracker (convention only, no checker) drifted within months — duplicate IDs,
off-template files, a lifecycle nobody followed. Corollary: **do not adopt a convention you will not
gate** (§11).

**Deterministic before generative.** Models produce; scripts verify. Every gate in this system runs
with zero model tokens and no network for its blocking checks, so verification is free, instant,
reproducible, and works identically under any future model — including none.

**Write for a reader with zero memory.** Every doc states when to open it (`read_when:`), what code
it owns (`governs:`), and what to do (normative rules). The reader — human in three years, agent in
three minutes — has no context you don't write down.

---

## §2 · The structure at a glance

```text
REPO/
├── CLAUDE.md                  # TIER 1: the canonical map — always loaded, ≤400 lines
├── AGENTS.md                  # tool-neutral router → "read CLAUDE.md first" (never a 2nd body)
├── README.md                  # human front door, ≤25 lines — points at the map, never mirrors it
├── Knowledge/                 # TIER 2: the rulebook — one normative doc per component
│   ├── conventions.md         #   naming, git workflow, tech stack
│   ├── runbook.md             #   copy-paste operational commands
│   └── _archive/              #   superseded docs (exempt from checks; move, don't delete)
├── Plans/                     # roadmap: NN_slug.md (frontmatter = source of truth)
│   ├── README.md              #   GENERATED status boards — never hand-edited
│   └── CHANGELOG.md           #   one milestone line per landed plan
├── Bugs/                      # defects: NNN_slug.md → Solved/ when closed
├── .claude/skills/            # TIER 3: invokable procedures (SKILL.md per procedure)
└── scripts/
    ├── check_knowledge.py     # doc rot-guard (links, frontmatter, drift)   — deterministic
    ├── check_plans.py         # board generator + staleness checker          — deterministic
    ├── verify.sh              # THE gate: regression + doc health (blocking) — deterministic
    └── hooks/pre-commit       # fast advisory nudge (git core.hooksPath)
```

| Layer | Question it answers | Load behaviour |
|-------|---------------------|----------------|
| **Map** (`CLAUDE.md`) | "Where is X? What must I always do?" | Auto-loaded into every session |
| **Knowledge/** | "How must component X behave?" | Opened on demand via `governs:` / `read_when:` |
| **Skills** | "How do I perform task X?" | Invoked by name |
| **Plans/** | "What should change?" | Frontmatter projected onto a generated board |
| **Bugs/** | "What is broken?" | Filed on trigger, archived on fix |
| **Gates** (`scripts/`) | "Is all of the above still true?" | Run at commit and verify time |

**Rule:** a piece of information appears in exactly one layer; the others link to it.

---

## §3 · Tier 1 — the map file and its pointers

The map is the one file loaded into every agent session and the first file a human opens. Its
filename follows whatever the primary harness — the tool that hosts the agent — auto-loads (today:
`CLAUDE.md`). If the auto-loaded name ever changes, `git mv` the body to the new name and leave a
pointer file at every old name — **one body ever, pointers accumulate** — and add the retired
filename to the stale-signal file (§8).

**Content contract** — the map MUST contain, in this order:

1. One-paragraph identity: what the repo is + the pipeline/purpose in one line.
2. **Read-me-first invariants** — 3–9 bullets; the only always-follow rules anywhere.
3. The development & verification workflow: name the **fragile core** (files where a fix for one
   case silently breaks another) and the gate that protects it — a one-line stub until the first
   fragile core is declared (§11).
4. A repo map table (path → role).
5. The **Knowledge index**: one row per doc with an "open it when…" clause.
6. A doc-taxonomy decision table ("where do I find / put X?") — may point at this spec's §4 table
   until the repo earns its own.
7. Run & test commands (or a pointer to the runbook).

Optional, when earned: a mermaid mental map; a **"Gotchas — learned the hard way"** section
(non-obvious traps, each one sentence); **reciprocal cross-repo pointers** (if repo A consumes
repo B's artifacts, each map names the other).

**Size budget: ≤400 lines.** The map taxes every task, so every line must pay rent. Eviction test:
*"would an agent doing an unrelated task still need this line?"* — if no, move it to a Knowledge doc
and leave a one-line index entry. The map may not state any fact that a Knowledge doc or a script
also states; a list needed by both the map and a script lives in a data file both read.

**Map skeleton** (placeholders in `{BRACES}`):

```markdown
# CLAUDE.md — {REPO_NAME} Context Map

> **What this is.** {ONE_SENTENCE_IDENTITY}. Pipeline in one line: {A → B → C}.
> Detailed behaviour lives in `Knowledge/` (one doc per component, each with `governs:`
> frontmatter). This file is the index — read the relevant doc before changing a component.

## 🚨 Read-me-first invariants
- {INVARIANT_1 — the thing that must never happen}
- {INVARIANT_2 — the thing that burned you once}
- **Fragile core:** touching {FRAGILE_FILES} → run {GATE_COMMAND} before committing.

## 🔁 Development & verification
{FRAGILE_CORE_WORKFLOW — or "no fragile core declared yet; the first 'fix A broke B'
incident adds golden files, per the coexistence spec §11"}

## 📁 Repo map
| Path | Role |
|------|------|
| {src/...} | {role} |

## 📚 Knowledge index
| Doc | Open it when… |
|-----|---------------|
| [conventions.md](Knowledge/conventions.md) | …naming, git workflow, stack |
| [runbook.md](Knowledge/runbook.md) | …you need an operational command |

## ▶️ Run & test
{FENCED_COMMANDS}

<!-- bootstrapped from AgenticHumanCoexistence.md spec_version {N} -->
```

**AGENTS.md** — the tool-neutral router (today's cross-vendor convention). Embed this text,
parameterized. Note it never enumerates skills — that list's one home is the map's index (a second
copy here is exactly the kind that rots):

```markdown
# AGENTS.md

{REPO_NAME} keeps its agent context in three places — read them in this order:

1. **[CLAUDE.md](CLAUDE.md)** — the canonical, always-loaded **map**: system overview, repo
   layout, and the Knowledge index ("for X, read Y"). **Start here.**
2. **[Knowledge/](Knowledge/)** — the **domain knowledge base**: one doc per component, each
   with `governs:` frontmatter naming the code it owns. Open the doc for what you're changing.
3. **Skills** — invokable **procedures**; see the skills index in CLAUDE.md. They live in
   `.claude/skills/` once the first one is earned. Always-follow rules live in CLAUDE.md;
   reference policy lives in `Knowledge/`.

Any agent (this harness or another) should read **CLAUDE.md first**. Keep code and `Knowledge/`
in sync with the deterministic, no-LLM rot-guard: `{CHECKER_COMMAND}`.
```

**README.md** — the human front door, ≤25 lines, **never a mirror** of the map:

```markdown
# {REPO_NAME}

{ONE_PARAGRAPH_IDENTITY}

> **The canonical map is [CLAUDE.md](CLAUDE.md)** — the single index of what each part does
> and which rule file to open for detail. This README is just the front door, not a mirror.

## Quick start
{FENCED_SETUP_AND_RUN_COMMANDS}

Secrets live in {SECRETS_FILE} (git-ignored).
```

---

## §4 · Tier 2 — Knowledge/: the rulebook

One normative doc per component. Every doc under `Knowledge/` (except `README.md` and `_archive/`)
MUST carry this frontmatter, machine-checked (§8):

```yaml
---
name: kebab-slug            # the filename without .md
type: rules                 # rules | runbook | architecture | index | reference
governs:                    # code paths/globs this doc OWNS — every entry must resolve
  - src/core/parser.py      # or `governs: []` for cross-cutting docs
read_when: One line stating the situation in which to open this doc.
---
```

| Field | Semantics |
|-------|-----------|
| `name` | Machine identity; kebab-case, equals the filename minus `.md`. |
| `type` | Taxonomy class (table below). Exactly these five values. |
| `governs` | The ownership contract. Powers the code↔doc drift check. A path that doesn't resolve fails the gate — ownership must be real, not aspirational. `type: rules` docs SHOULD have a non-empty list. |
| `read_when` | The trigger, written so the map's index can quote it. |

**Taxonomy** — the one-line test for each type:

| Type | Test |
|------|------|
| `rules` | "How must component X behave?" — normative, per-component, real `governs:`. |
| `runbook` | "How do I run/operate X?" — copy-paste commands, terse annotations. |
| `architecture` | "How is it built?" — design, diagrams, data flow. Descriptive, not normative. |
| `reference` | Cross-cutting facts that aren't per-file rules (conventions, product scope, policies). |
| `index` | The map itself. Exactly one per repo, at the root. |

**Seed set** for a new repo: `conventions.md` (naming, git workflow, stack) and `runbook.md`.
Add `architecture.md` only when the design is nontrivial. Subdirectories only once >5 docs exist —
then mirror the code layout (`backend/`, `frontend/`, …).

**Anatomy of a rules doc:** H1 → one context paragraph → normative **`Rule:`** statements
(imperative, testable: "When you modify X you MUST run Y") → at least one worked example → optionally
a bug post-mortem tying a rule to the incident that motivated it ("root cause of the {X} bug").
Post-mortems are the highest-value content in the whole system: they are the mistakes the company
never makes twice.

**Naming, stated once:** Knowledge docs are `kebab-case.md` with `name:` equal to the filename stem;
numbered collections (plans, bugs) are `NN_snake_topic.md` / `NNN_snake_topic.md`. No other
convention; the checker enforces both by regex (§8).

**`_archive/`:** superseded docs move here instead of being deleted (history survives) or left in
place (rot). Archived files are exempt from all checks.

**The sync rule (MUST):** when code behaviour changes, the governing doc is updated **in the same
commit**. Find the doc via its `governs:` entry or the map index. If a new requirement *contradicts*
an existing rule → STOP, ask the human, and encode the answer back into the doc (§9).

---

## §5 · Tier 3 — skills: invokable procedures

A skill is a procedure file the harness can invoke by name. Today's location:
`.claude/skills/<name>/SKILL.md`. Every skill ALSO gets a row in the map's index — the
harness-independent fallback that keeps procedures findable by anything that can read.

```yaml
---
name: verify-core
description: Run the deterministic safety net after any change to {FRAGILE_FILES}. Use before committing fragile-core edits — a fix for one case can silently regress another.
---
```

The `description` MUST contain an explicit "Use when/to…" clause — it is the router.

**Two archetypes:**

*Gate/pointer skill* (~25 lines) — orchestrates a script, defers policy to Knowledge:

```markdown
# {Title}

Run this after {TRIGGER}. Deterministic, **zero LLM tokens**.

    {THE_COMMAND}            # what blocks, what advises

- {Guardrail: e.g. "fix the logic universally — never special-case one input to pass"}
- {Guardrail: e.g. "baseline updates are deliberate: justify vs the external source, then lock in"}

Canonical detail: [{rules-doc}](../../../Knowledge/{rules-doc}.md) (the policy).
```

*Deep producer skill* (~70–100 lines) — the model does judgment work and writes an artifact:
role framing ("You are the deep {X} producer") → cost callout in **relative terms only**
("this spends the expensive interactive path; the automated path is cheap") → prerequisite check →
numbered workflow calling a deterministic helper script → structured output contract (JSON schema
inline) → **dry-run first + sanity gate** (preview the old → new delta, refuse implausible outputs,
let the human confirm) → the write-scope invariant.

**Helper-script verb triad.** Every producer skill is backed by `scripts/<name>_skill.py` —
no-model glue with three verbs: `status` (what's ready/stale, zero tokens), `prompt` (assemble the
exact context to a file), `apply` (dry-run by default, `--apply` to write, sanity gate inside).
The SKILL.md holds judgment; the script holds mechanics. **A skill must be reconstructible from
Knowledge + scripts alone** — if the skill format dies with a harness, nothing of value dies with it.

**Division of labor (MUST):** skill = procedure; Knowledge = rules. Cross-link both directions;
never duplicate a rule into a skill.

**Write-scope invariant (MUST for any skill that writes):** one line —
*"writes ONLY {files} — never touches {human-curated files}"*.

**Volatility layering:** model/vendor names and concrete costs may appear ONLY here in Tier 3
(procedures are cheap to update). Tiers 1–2 speak in roles — "cheap automated producer" vs
"deep interactive producer" — and the role→model binding lives in one git-ignored config file.
Both producers write the **identical artifact through the same validated write path** ("two
producers, one contract"), so models stay plug-compatible forever.

---

## §6 · Plans/ — the roadmap plane

One file per plan: `Plans/NN_kebab-slug.md`. The frontmatter is the **source of truth**; every
board is a projection of it.

```yaml
---
status: proposed        # proposed | in-progress | done | superseded   (required)
priority: next          # now | next | later — open plans only, omit otherwise
superseded_by: 12       # only when status: superseded
owner: {name}           # optional; defaults to the repo owner
---
```

**Body template:**

```markdown
# Plan NN — {scope in a few words}

> **Origin ({yyyy-mm-dd}):** "{the human's ask, verbatim}"

## Context
{why this exists}

## Current state (verified by exploration)
{what the code actually does today — measured, not assumed}

## PNN.1 — {item} · SAFE · low
{detail}. **Commit:** `Plan NN: {item}`

## PNN.2 — {item} · RISKY (touches fragile core) · medium
{detail}

## Verification
{how done-ness is proven: commands, expected output}
```

Items carry stable IDs (`PNN.n`), a risk class (**SAFE** = no behaviour change / **RISKY** = touches
the fragile core), an effort tag, and — when finished — `✅ DONE (commit <hash>)` inline. Commit
messages reference the plan: `Plan NN: <item>`.

**`Plans/README.md` is generated, never hand-edited.** A deterministic script projects two boards
from the frontmatter — the full status board and a "next up" board (open plans carrying a priority)
— between these exact sentinels:

```text
<!-- AUTOGEN:status-board:start --> … <!-- AUTOGEN:status-board:end -->
<!-- AUTOGEN:nextup:start -->       … <!-- AUTOGEN:nextup:end -->
```

The board cannot rot: the checker's `--check` mode fails the gate if the projection is stale (§8).

**`Plans/CHANGELOG.md`** is the human-readable pulse: one line per landed plan —
`## YYYY-MM-DD — Plan NN done: {scope}` plus a short paragraph with commit hashes. Full history is
`git log`; per-plan status is the generated board; the changelog is milestones only.

**Lifecycle loop:** edit the plan's frontmatter → run the plans checker to regenerate the boards →
when a plan turns `done`, add its changelog line in the same commit.

---

## §7 · Bugs/ — defect capture

**Trigger:** the human writes `bug: <name + description>` → the agent files `Bugs/NNN_kebab-slug.md`
(next sequential number) from this template:

```markdown
# Bug: {title}

## Description
## Steps to Reproduce
## Expected Behavior
## Actual Behavior
## Potential Causes
- {hypothesis}

## Investigation Steps
- [ ] {step}

## Resolution
{the fix} · **Files Modified:** … · **Date Resolved:** …
```

Investigate via the checkboxes, add the Resolution, then close by moving the file to `Bugs/Solved/`.
`Bugs/README.md` is the front page: an open-bugs table plus a severity legend
(🔴 breaks correctness · 🟡 wrong but bounded · 🔵 cosmetic/tech-debt).

**The honest post-mortem:** in the origin repo, Bugs/ was the only collection without a checker —
and the only one that rotted (duplicate numbers, off-template files, a hand-table that forked from
the prescribed lifecycle). Therefore this spec REQUIRES minimal bug checks, folded into the
knowledge checker (§8): unique sequential `NNN`, filename matches the pattern, required headings
present, every open bug listed in the front page. The rot theorem is not optional.

---

## §8 · Deterministic gates — the anti-rot machinery

Four components. All are **zero-model, zero-network for blocking checks, stdlib-only** in whatever
scripting language the repo chose (default: `python3`, no dependencies — even the frontmatter parser
is hand-rolled, so the gates run on a bare interpreter forever). Findings are split into **HARD**
(exit ≠ 0, gate the build) and **ADVISORY** (print, exit 0).

**1 · Knowledge checker** (`scripts/check_knowledge.py`) — behavioural contract:

| Check | Class | Behaviour |
|-------|-------|-----------|
| Link integrity | HARD | Every relative markdown link in the map, router, README, Knowledge/, Plans/, skills resolves to a real file (strip fenced code blocks first — templates inside fences are exempt). |
| Frontmatter validity | HARD | Every Knowledge doc has the 4 required keys; `type` in the enum; **every `governs:` entry resolves** (exact path or glob); filename matches the §4 pattern and `name` equals the stem. |
| Bug hygiene | HARD | Unique sequential bug numbers; filenames match the pattern; required headings present. |
| Orphan detection | ADVISORY | BFS the link graph from the map; any Knowledge doc unreachable → warn ("every doc gets an index row"). |
| Stale signals | ADVISORY | Scan normative docs line-by-line for retired terms, read from a **data file** (see below). |
| Code↔doc drift | ADVISORY | With `--staged`: a file matched by some doc's `governs:` is staged while none of its owning docs are staged → "update the knowledge?". |

Flags: `--staged` (drift mode, for the pre-commit hook), `--quiet`, `--strict` (advisories become
fatal, for CI).

**Stale-signal data file** — canonical path `Knowledge/_meta/stale_signals.txt`; one retired term
per line, optional `term | required-context-word` to limit false positives, `#` comments; a missing
file means an empty set. It starts **EMPTY** in a new repo and grows by one rule: *every rename,
removal, or migration that retires a term adds that term to the file in the same commit.*
Deprecation creates a tripwire; the checker then catches any doc still using yesterday's name.

**2 · Plans checker** (`scripts/check_plans.py`) — generator AND checker. Default run re-projects
the boards from frontmatter and writes `Plans/README.md`. `--check` (used by gates) fails on: stale
boards, missing sentinels, missing/invalid `status`, invalid `priority`. Advisory: a `done` plan
absent from the changelog; a closed plan still carrying `priority`; nothing prioritized at all.

**3 · The verify gate** (`scripts/verify.sh`) — *the* gate; a thin orchestrator that only calls
checkers (no inline logic to rot):

1. **Domain regression — BLOCKING.** The golden-files suite (below). Until the first goldens
   exist, this stage prints a NOTE and exits 0 — a placeholder, not a silent pass.
2. **Doc & plan health — BLOCKING.** Knowledge checker + plans checker `--check`.
3. **External oracle — ADVISORY.** Cross-check outputs against an independent source of truth
   (a regulator's API, a reference host/validator, a holdout dataset). **Triage, not a gate**:
   false positives are expected; a ❌ means "open the source and look", never "auto-silence it".

**4 · Pre-commit hook** (`scripts/hooks/pre-commit`) — the fast advisory nudge. Installed once per
clone (put it in `scripts/bootstrap.sh`):

```bash
git config core.hooksPath scripts/hooks
```

It blocks ONLY when a declared **fragile-core** file is staged (then it runs the domain regression);
every other commit passes instantly, with the two rot-guards printed as advisories (`|| true`).
Emergency bypass: `git commit --no-verify` — legitimate for WIP branches, never for the main branch.

**The golden-files principle** (domain-abstract): identify the fragile core — the files where *a fix
for one case silently regresses another*. Freeze verified outputs as golden baselines. Every change
re-runs the core against cached inputs and **diffs deterministically, offline**. A baseline update is
deliberate, single-artifact, and justified against the external source of truth — never "regenerate
all to make it pass", and never special-case one input to silence a diff. Instantiations:

- *Financial extraction* → golden JSON per company, diffed field-by-field.
- *Audio plugin* → offline-rendered buffers / parameter dumps checksummed, plus a plugin validator.
- *ML tooling* → fixed-seed metric and output snapshots.

**The meta-rule:** any new convention introduced later MUST arrive with its check **in the same
commit** (§11).

**Reference implementations:** the canonical engines ship with this spec in its dedicated
repository, at the same paths every conforming repo uses
([check_knowledge.py](../scripts/check_knowledge.py), [check_plans.py](../scripts/check_plans.py),
[verify.sh](../scripts/verify.sh), [pre-commit](../scripts/hooks/pre-commit)). COPY them —
byte-identical engines across the fleet, with repo-specific values (signals, fragile-core list) in
config/data files, never edits to the engine. When not accessible, re-implement from the contracts
above. Two caveats: **(1)** never carry another repo's signal list or golden files into a new repo —
those are repo data, and a new repo's list starts empty. **(2)** Answering interview Q7 with anything
other than the default forfeits the copy path and fleet byte-identity — re-implement from the
contracts and accept that cost knowingly.

---

## §9 · The human/agent boundary in data

Every artifact directory MUST carry an **origin legend** (in its README or the map) classifying each
file kind as one of:

- **human-curated** — intent, assumptions, notes. *Agents never edit these.*
- **generated-deterministic** — computed by scripts. *Humans never hand-edit; regenerate instead.*
- **AI-produced** — analysis, syntheses, models. Written only through validated write paths, behind
  dry-run gates.

Example write-scope line from a producer skill: *"writes ONLY `Model/{id}/model_*.json` — never
touches the human's `notes.md` or `assumptions.md`."*

**The conflict rule.** When a new instruction contradicts an existing Knowledge rule: **STOP** —
don't silently pick one. Ask the human (or the doc's `owner:` on a team), then encode the decision
back into the governing doc in the same commit. The doc, not the chat, is where decisions survive.

**Authority & escalation (minimum team rules):** agents work on branches, humans merge to the main
branch. Secrets live in one git-ignored file that agents never write and never echo. Golden-baseline
updates and `_archive/` deletions require explicit human sign-off. Anything that spends money or
leaves the machine (publishing, messaging, deploying) is named in the map's invariants or it is
not allowed.

---

## §10 · Bootstrap procedure (execute in a new repo)

### §10.0 Ground rules
Execute the steps in order. **Write nothing before the interview (§10.1) is complete.** Commit in
small steps labeled with Plan-01 item IDs. All migration moves use `git mv` (history survives).
Nothing is deleted during migration — moved, converted, or archived only.

### §10.1 Interview the human (blocking)

```text
1. What is this repo, in one sentence? What is the pipeline/purpose in one line?
2. What are the 3–7 always-follow invariants — what has burned you before, what
   must never happen? (These become the map's read-me-first bullets, verbatim intent.)
3. Which files are the FRAGILE CORE — where can a change to handle one case silently
   break another? (→ pre-commit block list, golden files, a reliability doc.)
4. What deterministic proof exists that the product works (build/test/render command)?
   If none: what output could be frozen as a golden baseline?
5. Which directories are human-curated vs generated vs AI-produced? (→ origin legends.)
6. Greenfield or migration? Which legacy doc dirs exist (Rules/, Documentation/, Todo/,
   epics/stories, an old Bugs/, README "golden rules", command docs)? Which existing
   naming/branching conventions must survive? (→ the conventions.md seed.)
7. Checker implementation language? (Default: python3, stdlib only.)
```

### §10.2 Explore (read-only) and propose the plan
Map the components, entry points, existing tests/hooks/docs — and inventory **existing agentic
assets**: map or vendor rule files (an existing `CLAUDE.md`, `AGENTS.md`, editor rule files),
agent-framework directories, prompt configs, CI, hooks, verification scripts. These are integrated,
never overwritten (§10.4). Then write up **"Current state (verified by exploration)"** together with
the full proposed item list — including the migration mapping, if any — as a draft of Plan 01.
**The human approves this draft before anything is created or moved**; approved, it becomes Plan 01
verbatim in §10.3 step 5.

### §10.3 Phase 0 — the minimal viable structure (greenfield)
Eight artifacts, one commit each; the bootstrap itself is **Plan 01** (dogfooding: its origin
blockquote is the kickoff prompt, its items are these steps):

1. `CLAUDE.md` from the §3 skeleton — interview invariants + explored repo map + run/test; the
   index starts with 2–3 rows. Include the `spec_version` comment.
2. `AGENTS.md` from the §3 template.
3. `README.md` front door (§3). Existing README? Prepend the pointer block and move any normative
   content into the map or Knowledge — never leave two homes for one fact.
4. `Knowledge/conventions.md` + `Knowledge/runbook.md` (seeds, §4 frontmatter).
5. `Plans/01_bootstrap_agentic_structure.md` + a stub `Plans/README.md` carrying only the §6
   sentinels (its boards are generated by the plans checker in step 7, never by hand) + empty
   `Plans/CHANGELOG.md`.
6. `Bugs/README.md` (open table + severity legend) + `Bugs/Solved/` (with `.gitkeep`).
7. `scripts/`: the two checkers + `verify.sh` + `hooks/pre-commit` per the §8 contracts (copy the
   reference implementations when accessible — mind the §8 caveats) + `bootstrap.sh` (hooksPath,
   environment, checkers) + the empty stale-signal file at its §8 canonical path; run
   `git config core.hooksPath scripts/hooks`, then run the plans checker to fill the boards.
8. The spec itself: save the copy you were handed as `Knowledge/agentic-human-coexistence.md`,
   frontmatter per §4, recording its source `spec_version`.

**DO NOT CREATE YET** (the §11 triggers govern when each appears):

```text
✗ Knowledge subdirectories        ✗ any skill
✗ golden files                    (unless the interview named a fragile core —
                                   then goldens are Plan 01 items, not deferred)
✗ a second plan                   ✗ stale-signal entries (the list starts empty)
✗ architecture.md                 (unless nontrivial design already exists)
```

### §10.4 Migration variant (runs between steps 3 and 4)

| Legacy | → Canonical | Procedure |
|--------|-------------|-----------|
| `Rules/*.md` | `Knowledge/` | `git mv`; convert/add the 4-key frontmatter; one index row each; every `governs:` must resolve. |
| `Documentation/` | `Knowledge/` by taxonomy | Classify each doc (rules/runbook/architecture/reference); unclassifiable or stale → `Knowledge/_archive/`. |
| `Todo/`, epics, stories | `Plans/NN_*.md` | Live intent → `status: proposed` with an origin blockquote (date = migration, note provenance); dead items → one `superseded` plan listing them. |
| Old bug files | Renumber to `NNN_slug.md` | Solved → `Solved/`; open → the README table. |
| README "golden rules" | Map invariants | Verbatim intent; the human confirms each survives translation. |
| Command/workflow docs | `Knowledge/` as `type: runbook` (or `_archive/`) | Skills come later, per the §11 trigger — never bulk-convert during bootstrap. |
| Existing map / vendor rule files | The §3 map | Merge each rule into the map's invariants or its governing Knowledge doc (one home each); the old file becomes the map body or a pointer — never a second body. |
| Agent-framework artifacts (planning dirs, epics/stories, prompt configs) | `Plans/` or `Knowledge/_archive/` | Live intent → `status: proposed` plans; machinery still in active use stays and is named in the map's repo table. |
| Existing CI / hooks / verification scripts | `scripts/` + the §8 gates | Wire them in as verify.sh stages (blocking or advisory per §8); never leave two competing gate entry points. |
| `version.json` and similar | Leave in place | Reference from `conventions.md`; not part of this structure. |

Afterwards the human reviews `Knowledge/_archive/` — the agent proposes, the human disposes.

### §10.5 Gate until green
Run both checkers and `verify.sh`. Fix every HARD finding. Triage advisories — **orphans must reach
zero** (every doc indexed in the map).

### §10.6 Handover
Present the map to the human for sign-off on the invariants and origin legends. Set Plan 01
`status: done`, add its changelog line, regenerate the boards, final commit.

**Acceptance checklist:**

```text
□ both checkers exit 0; --strict shows zero orphans
□ verify.sh runs end-to-end (regression stage may be a placeholder until goldens exist)
□ hooks installed (git config core.hooksPath → scripts/hooks)
□ README ≤25 lines and non-mirroring; map ≤400 lines
□ every Knowledge doc reachable from the map index
□ Plan 01 done, on the board, in the changelog
□ the human signed off on invariants + origin legends
□ the spec copy saved in Knowledge/ and the map records its source spec_version
```

---

## §11 · Growth & maintenance rules

Structure grows on triggers, never in advance — a 3-file repo must not cosplay as a mature one:

| Trigger | Response |
|---------|----------|
| A second rule accumulates about one component | Give it its own Knowledge doc + index row |
| A procedure is performed manually for the second time | Turn it into a skill |
| First "fixing A broke B" incident (or interview named a fragile core) | Golden files + pre-commit block for those files |
| A second concurrent workstream appears | Second plan (until then, one plan is plenty) |
| Knowledge/ exceeds ~5 docs | Introduce subdirectories mirroring the code layout |
| More than 2 skills | Add a skills index table to the map |
| A term is renamed/retired | Add the old term to the stale-signal file, same commit |

**Rot-response rule:** a convention violated twice → add a checker for it or delete the convention.
There is no third option.

**No scheduled reviews.** The gates ARE the review: staleness is caught at commit and verify time,
by construction. A calendar reminder to "review the docs" is exactly the kind of convention that
rots; a checker that fails the build is not.

---

## §12 · What this document deliberately omits (normative)

The following MUST NOT appear in this spec or in any Tier 1/2 file of a bootstrapped repo:

- AI model names, versions, vendors, context sizes, token prices, rate limits (roles only — the
  binding lives in one config file; specifics may appear in Tier 3 skills only).
- Harness feature specifics beyond two filename conventions (the auto-loaded map name and the
  skills directory), each named as "today's location".
- Origin-repo domain content (its tickers, formats, signal lists — a new repo's stale list starts
  empty and its goldens are its own).
- Repo-size numbers as norms — only the budgets and triggers above generalize.
- Checker source code — contracts only; the reference implementation is copied, not transcribed.
- Anything answerable only "as of {year}".

*If a future edit to this document violates §12, the edit is wrong, not §12.*
