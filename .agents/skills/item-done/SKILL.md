---
name: item-done
description: Use when a sprint item is implemented and verified.
---

## Goal

Close a sprint item with verification and ownership proof.

## Steps

1. Confirm targeted verification passed.
2. Log any durable design or workflow lesson as a `sprintctl event`.
3. Mark done with `sprintctl item done-from-claim --claim-id <id> --claim-token <token>`.
4. Remove the local claim-token recovery file after release.
5. Refresh the sprint snapshot when the workflow needs a shared artifact.

## Do not

- Do not close an item with failing verification.
- Do not manufacture knowledge events when nothing durable was learned.
