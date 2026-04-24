# Project Working Practices

**Classification:** CROSS-CUTTING

## Purpose

This runbook defines the repository's default working practices for how work starts,
moves, and closes. It is adapted from the homelab-analytics process model, but the
architecture rules are Aligned Equity rules: evidence, features, scorecards, lenses,
decision outputs, and publication contracts stay separate.

For sprintctl and kctl command details, use `runbooks/sprint-and-knowledge-operations.md`.

## Source-Of-Truth Stack

When sources disagree, follow them in this order:

1. `sprintctl` live state for execution status, claims, active work, and structured events
2. `docs/sprint-snapshots/sprint-current.txt` for the shared current sprint view when a tracked artifact is needed
3. runbooks, `AGENTS.md`, mode guides, and skills for durable process rules
4. architecture, product, plan, and specification docs for intended behavior
5. committed knowledge artifacts for curated reusable decisions and lessons
6. session notes for local history only

Interpretation rules:

- use live `sprintctl` state to choose or resume sprint work when the local DB is available
- use sprint docs, plans, and session notes to explain work, not to override live execution state
- promote repeated rules from session history into tracked runbooks, skills, or guides
- keep Aligned Equity's Finland-first, source-led, longitudinal model ahead of generic platform habits

## Working Loops

### 1. New scope registration

**Start trigger:** accepted scope needs execution tracking and is not represented in `sprintctl`.

**Consult first:** product, architecture, specification docs, and current sprint context.

**While in progress:**

- use `sprint-packet` when a new sprint or item set needs a reusable implementation packet
- load `.envrc` before using sprint or knowledge tooling
- slice items by deliverable or repo boundary, not by vague task labels
- render `docs/sprint-snapshots/sprint-current.txt` after live sprint state is registered

**Close-out artifacts:** registered sprint/items and refreshed sprint snapshot when the state needs to be shared.

### 2. Resume or dispatch sprint work

**Start trigger:** the request says continue, resume, dispatch, pick up next work, or execute scoped sprint activity.

**Consult first:** live `sprintctl` item state, claims, recent events, and `sprintctl agent-protocol --json`.

**While in progress:**

- claim sprint items before implementation when ownership could be ambiguous
- prefer `sprintctl claim start --item-id <id> --actor <name> --json` for atomic claim plus activation
- persist claim tokens only in `.sprintctl/claims/claim-<item_id>.token` when recovery is needed; never commit them
- heartbeat long-running claims, then complete with `sprintctl item done-from-claim`
- use `sprintctl item note` or `sprintctl event add` for durable decisions, blockers, lessons, and dispatch milestones
- refresh the sprint snapshot after live state changes when a committed shared view is needed

**Close-out artifacts:** updated item state, claim metadata, events, and a refreshed sprint snapshot.

### 3. Implementation

**Start trigger:** a scoped item or direct request is ready for repo changes.

**Consult first:** relevant contracts, source inventory, architecture docs, fixtures, validators, and package extension points.

**While in progress:**

- preserve evidence, features, scorecards, lenses, decision outputs, and publication boundaries
- keep homelab-analytics optional and contract-bound; do not add it as a core runtime dependency
- add or update tests for behavior and contract changes
- update docs when behavior, architecture, or public contracts change
- use focused checks during implementation and `make verify-fast` before push or PR

**Close-out artifacts:** repo change, matching verification, and sprint updates when the work is sprint-scoped.

### 4. Review

**Start trigger:** the change shape is stable enough to inspect for defects, regressions, and missing coverage.

**Consult first:** diff, relevant specs, architecture docs, and verification output.

**While in progress:**

- review findings before summaries
- check traceability between requirements, implementation, tests, and docs
- confirm confidence, comparability, and causal-claim guardrails still hold when decision outputs change
- note residual risk or verification debt explicitly

**Close-out artifacts:** findings-first review notes or reviewer handoff.

### 5. Release or push

**Start trigger:** work is about to move to a branch push, PR, CI, or release-oriented handoff.

**Consult first:** changed files, verification path, branch state, and release/ops docs affected by the change.

**While in progress:**

- run the smallest useful checks first, then broader repo gates
- run `make verify-fast` before pushing a branch that will trigger CI
- keep secrets reference-based and out of tracked files
- commit at a reviewable scope boundary

**Close-out artifacts:** commit, pushed branch, verification summary, and PR or handoff material when requested.

## Done By Change Class

### Docs-only change

- update the durable doc in the correct tracked location
- update `docs/README.md` when adding a discoverable durable doc
- run relevant validation, grep, or diff checks needed to prove consistency
- do not claim runtime behavior changed unless tests or code changed with it

### Behavior or contract change

- update or add tests in the same change
- update docs when externally visible behavior or accepted scope changes
- run targeted tests for changed behavior
- run `make verify-fast` before push or PR
- keep sprint state current if the work is sprint-scoped

### Architecture change

- update the relevant architecture or decision docs under `docs/`
- confirm source, evidence, scorecard, lens, decision-output, and publication boundaries still hold
- verify the boundary through focused tests, validators, or contract checks

### HLA boundary change

- preserve import safety without homelab-analytics installed
- keep the root `homelab-analytics.registry.json` as the external registry boundary
- run `make hla-contract-check` when the sibling HLA repo is available
- update HLA contract docs and reserved publication keys together

### Sprint-state change

- record live sprint state in `sprintctl` first
- refresh `docs/sprint-snapshots/sprint-current.txt` from `sprintctl render` afterward
- keep handoff bundles local unless a task explicitly asks for a committed artifact
- remove recovered claim-token files after successful item completion or release

## Multi-Agent Coordination

Use claims and handoff artifacts to coordinate shared sprint work.

Required claim identity:

- ownership proof: `claim_id` plus `claim_token`
- identity metadata: runtime session id, instance id, branch, worktree, commit SHA, and PR reference when available

Coordination rules:

- do not infer ownership from sprint docs, plans, session notes, actor name, branch, or worktree alone
- if an exclusive claim belongs to another live session, stop repo edits and resolve a handoff or choose different work
- add event records when decisions are made or blockers are resolved, not only at sprint close
- use `sprintctl claim handoff` when ownership moves to another session
- use `sprintctl handoff --format json --output <path>` when work pauses materially

## Sprint Close

**Start trigger:** the sprint is substantially complete or needs formal close-out and carryover decisions.

**While in progress:**

- run `sprintctl maintain check`
- carry over unfinished work that belongs in the next sprint
- close the sprint only after execution state is accurate
- run `kctl extract`, review candidates, and publish knowledge when that output belongs in repo memory

**Close-out artifacts:** correct sprint status, refreshed sprint snapshot, reviewed knowledge candidates, and rendered knowledge base when published.
