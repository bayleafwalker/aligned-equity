---
name: sprint-snapshot
description: Use to render current sprintctl state into docs/sprint-snapshots/sprint-current.txt.
---

## Goal

Keep the committed sprint snapshot aligned with live sprintctl state.

## Steps

1. Load `.envrc`.
2. Run `make snapshot-refresh` or `sprintctl render --output docs/sprint-snapshots/sprint-current.txt`.
3. Review the diff to confirm the snapshot is generated, not manually edited.

## Do not

- Do not use the snapshot as the primary source when the sprintctl DB is available.
- Do not edit the snapshot manually.
