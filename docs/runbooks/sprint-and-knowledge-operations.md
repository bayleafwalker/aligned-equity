# Sprint And Knowledge Operations

**Classification:** CROSS-CUTTING

## Purpose

This runbook covers the repo's `sprintctl` and `kctl` operating model. It follows the
homelab-analytics workflow shape while keeping Aligned Equity state repo-local.

Use `sprintctl` for live sprint execution state. Use `kctl` for extracting, reviewing,
publishing, and rendering durable knowledge from sprint events.

For repo-wide startup order, source-of-truth precedence, done criteria, and coordination
rules, use `runbooks/project-working-practices.md`.

## Shared State

### Local only

These stay machine-local and gitignored:

- `.sprintctl/sprintctl.db`
- `.sprintctl/claims/claim-<item_id>.token`
- `.kctl/kctl.db`
- `sprint-*.json`
- `handoff-*.json`
- `handoff-*.txt`

### Committed

These are the shared repo artifacts:

- `docs/sprint-snapshots/sprint-current.txt`
- `docs/knowledge/knowledge-base.md`

Treat committed files as the shared repo view. The SQLite databases are local execution
state and should not be committed.

## Daily Use

### 1. Start from the project-scoped DB

Load `.envrc` before using either CLI:

```bash
source .envrc
echo "$SPRINTCTL_DB"
echo "$KCTL_DB"
echo "$KCTL_PROJECT"
```

Both DB paths must point inside this repository, not home-directory defaults.

### 2. Refresh tools when needed

`sprintctl` and `kctl` are private source-installed user tools. They are not PyPI
dependencies.

Refresh them from source when missing or stale:

```bash
uv tool install --force --reinstall /projects/dev/sprintctl --python python3
uv tool install --force --reinstall /projects/dev/kctl --python python3
```

After reinstalling, verify active commands and scoped state:

```bash
source .envrc
command -v sprintctl
command -v kctl
sprintctl sprint list
kctl status --kind all
```

### 3. Use repo-local wrapper targets

The repo ships a small wrapper layer for canonical sprint and knowledge flows. These
targets source `.envrc`, use repo-local DB paths, and keep repeated command shapes out of
ad hoc shell history.

- `make sprint-resume [ITEM=<item-id>]` wraps claim resume using `SPRINTCTL_INSTANCE_ID`, `SPRINTCTL_RUNTIME_SESSION_ID`, or `CODEX_THREAD_ID`
- `make claim-recover ITEM=<item-id>` wraps `sprintctl claim recover --item-id <item-id> --json`
- `make claim-heartbeat CLAIM_ID=<claim-id> CLAIM_TOKEN=<claim-token> [ACTOR=<actor>] [CLAIM_TTL=300]`
- `make item-verify-auth PY_FILES="path1 path2" TESTS="tests/test_a.py tests/test_b.py"`
- `make snapshot-refresh [SPRINT_ID=<sprint-id>]` renders `docs/sprint-snapshots/sprint-current.txt`
- `make knowledge-publish CANDIDATE=<id> CATEGORY=<decision|pattern|lesson|risk|reference> BODY="..." [TITLE="..."] [TAGS='[\"workflow\"]'] [COORDINATION=1]`

Use raw `sprintctl` and `kctl` commands when a flow is not covered by a wrapper.

## Dispatch And Claim Lifecycle

Use `sprintctl agent-protocol --json` as the authoritative claim lifecycle reference.

Default dispatch flow:

1. Inspect active sprint and pending work:
   ```bash
   source .envrc
   sprintctl sprint show --detail --json
   sprintctl next-work --json
   ```
2. Add or select the item:
   ```bash
   sprintctl item add --sprint-id <id> --track <track> --title "<title>" --json
   ```
3. Claim and activate:
   ```bash
   sprintctl claim start --item-id <item-id> --actor <name> --branch "$(git branch --show-current)" --worktree "$PWD" --commit-sha "$(git rev-parse HEAD)" --json
   ```
4. Log decisions and lessons while context is current:
   ```bash
   sprintctl item note --id <item-id> --type decision --summary "..." --detail "..." --tags workflow
   ```
5. Complete with proof:
   ```bash
   sprintctl item done-from-claim --id <item-id> --claim-id <claim-id> --claim-token <claim-token> --actor <name> --json
   ```
6. Refresh the shared view when needed:
   ```bash
   make snapshot-refresh
   ```

Ownership proof is always `claim_id` plus `claim_token`. Treat claim tokens as secrets and
keep them out of git.

## Event Capture

Log durable execution events when facts are discovered, not only at sprint close.

Useful event types:

- `decision`
- `lesson-learned`
- `blocker-resolved`
- `pattern-noted`
- `risk-accepted`

Use summaries, details, tags, and git context so later `kctl` extraction yields useful
candidate knowledge rather than noise.

## Sprint Snapshot Policy

- Run `sprintctl render --output docs/sprint-snapshots/sprint-current.txt` only after DB state is correct.
- Render when the workflow needs a new shared artifact now or a natural batch boundary has been reached.
- Do not treat every item close as a mandatory snapshot commit.
- Keep snapshot updates explainable in the commit message when committed with related workflow changes.

## Sprint Close

Before closing a sprint:

- run `sprintctl maintain check`
- move unfinished work with `sprintctl maintain carryover --from-sprint <id> --to-sprint <next-id>`
- close the sprint with `sprintctl sprint status --id <id> --status closed`
- run `kctl extract --sprint-id <id>` when sprint events should become durable knowledge candidates
- review candidates with `kctl review list`, `kctl review show`, `kctl review approve`, and `kctl review reject`
- publish intentionally with `kctl publish ...`, then render `docs/knowledge/knowledge-base.md`

## Useful Structured Surfaces

Prefer JSON output when another agent or script needs machine-readable state.

- `sprintctl sprint show --detail --json`
- `sprintctl item list --sprint-id <id> --json`
- `sprintctl item show --id <item-id> --json`
- `sprintctl claim list --item-id <item-id> --json`
- `sprintctl claim list-sprint --sprint-id <id> --json`
- `sprintctl claim resume --instance-id <id> --json`
- `sprintctl claim start --item-id <item-id> --actor <name> --json`
- `sprintctl item done-from-claim --id <item-id> --claim-id <claim-id> --claim-token <token> --json`
- `sprintctl usage --context --json`
- `sprintctl agent-protocol --json`
- `sprintctl handoff --format json --output <path>`
- `kctl preflight --sprint-id <id> --json`
- `kctl review list --json`
- `kctl status --kind all --json`

## Recovery

If a local DB is lost:

- treat `docs/sprint-snapshots/sprint-current.txt` as the shared view of the current sprint
- recreate the relevant sprint and items manually in `sprintctl`
- use local export and handoff bundles only as advisory inputs, not as canonical repo state
