---
name: sprint-resume
description: Use when work already exists in sprintctl and the task is to continue or pick up an item.
---

## Goal

Resume sprint work without duplicating scope or stealing another live claim.

## Steps

1. Load `.envrc`.
2. Inspect sprint, item, claim, and recent event state.
3. If no active claim exists, use `sprintctl claim start`.
4. Persist the returned claim token to `.sprintctl/claims/claim-<item_id>.token`.
5. If a claim exists and ownership is ambiguous, stop and request a handoff or choose a
   different item.
6. Move implementation through targeted verification, then close with `item-done`.

## Do not

- Do not infer ownership from docs or branch names when live claims exist.
- Do not heartbeat a claim without matching ownership proof.
