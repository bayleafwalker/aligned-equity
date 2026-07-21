<!-- agentops-render: DO NOT HAND-EDIT
     project_id: a40e9a1d-cf76-4bae-a330-f62ecc9e59f8
     project: homelab-analytics
     member: aligned-equity
     render: baseline
     source_bundle_sha256: d4e198d6d12cb511b05e976ea8457535be93ecc6644f9cd27aa60a89f8d7614e
     tool: agentops-render/v1
-->

# Homelab-analytics project scope

This repository participates in the `homelab-analytics` multi-repository
project. The project is a read and instruction projection; each member
repository remains the authority for its own runtime behavior and Git
history.

- Canonical binding and shared sources live in the `homelab-analytics` home
  repository, at its root (in-place topology — no project folder, no
  worktrees).
- Cross-cutting project work is tracked in the homelab-analytics sprintctl
  backlog.
- Use `sprintctl usage --context --project --json` and
  `sprintctl next-work --project --json --explain` from any member repository
  checkout. Every union row must retain its `origin_repo`.
- Direct repository sessions remain supported. Omitting `--project` must keep
  the repository-local sprintctl behavior unchanged.
- Project instructions are baseline guidance followed by member-owned
  overrides. The member's authored `AGENTS.md` remains authoritative for local
  workflow and safety constraints.

Treat a dirty, divergent, or unexpectedly branched member worktree as a stop
condition; resolve it through the owning repository rather than resetting it
from project tooling.
