# Project Working Practices

## Source of truth

Use this order when sources disagree:

1. live `sprintctl` state for execution status, claims, and active work
2. rendered sprint snapshots when a committed shared view is needed
3. runbooks and `AGENTS.md` for durable process rules
4. architecture, product, and plan docs for intended behavior
5. session notes for local history only

## Working loop

- Load `.envrc` before using sprint or knowledge tooling.
- Keep repository changes small enough to verify locally.
- Run targeted tests during implementation and `make verify-fast` before push or PR.
- Update docs when behavior, architecture, or public contracts change.
- Keep HLA integration optional and contract-bound.

## Done criteria

Docs-only changes:

- update the durable doc in the right location
- update `docs/README.md` when discoverability changes
- run the relevant validation or grep checks

Behavior or contract changes:

- update tests in the same change
- run `make verify-fast`
- document public interface changes

HLA boundary changes:

- preserve import safety without HLA installed
- run `make hla-contract-check` when the sibling HLA repo is available
- update `docs/architecture/homelab-analytics-platform-contract.md`
