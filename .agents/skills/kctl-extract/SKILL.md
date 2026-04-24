---
name: kctl-extract
description: Use at sprint close to extract durable knowledge from sprintctl events.
---

## Goal

Move useful sprint decisions and lessons into the kctl review pipeline.

## Steps

1. Load `.envrc`.
2. Run `kctl preflight --sprint-id <id>` or `sprintctl maintain check --sprint-id <id>`.
3. Run `kctl extract --sprint-id <id>`.
4. Review candidates with `kctl review list --kind all`.
5. Approve or reject each candidate.
6. Publish selected entries and render `docs/knowledge/knowledge-base.md` when publication is in scope.

## Do not

- Do not rely on bare events without payloads for durable knowledge.
- Do not render knowledge artifacts outside `docs/knowledge/knowledge-base.md`.
