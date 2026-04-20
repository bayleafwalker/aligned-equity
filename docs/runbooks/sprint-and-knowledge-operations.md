# Sprint And Knowledge Operations

## Local state

These paths are local and gitignored:

- `.sprintctl/sprintctl.db`
- `.sprintctl/claims/claim-<item_id>.token`
- `.kctl/kctl.db`
- `sprint-*.json`
- `handoff-*.json`
- `handoff-*.txt`

## Committed artifacts

- `docs/sprint-snapshots/sprint-current.txt` when a shared sprint view is intentionally rendered
- `docs/knowledge/knowledge-base.md` when reviewed knowledge is intentionally published

## Setup

```bash
source .envrc
echo "$SPRINTCTL_DB"
echo "$KCTL_DB"
echo "$KCTL_PROJECT"
```

Both DB paths must point inside this repository, not the home directory.

## Tool refresh

`sprintctl` and `kctl` are private source-installed tools in the surrounding workspace. Refresh them from source when missing or stale:

```bash
uv tool install --force --reinstall /projects/dev/sprintctl --python python3
uv tool install --force --reinstall /projects/dev/kctl --python python3
```

## Policy

- Record live sprint state in `sprintctl` before rendering a committed snapshot.
- Publish durable knowledge intentionally through `kctl`; do not hand-edit generated knowledge as a substitute for publication.
- Keep handoff bundles local unless a task explicitly asks for a committed artifact.
