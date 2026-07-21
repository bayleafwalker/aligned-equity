# Agent Guidance

> Environment reference: `/projects/dev/AGENTS.md` covers shared workspace paths, tool persistence, direnv, and local-vs-devbox expectations.

## Repository posture

- Primary language: Python.
- Package manager and runner: `uv`.
- Verification: `make verify-fast`.
- The core package must remain independently installable without homelab-analytics on `PYTHONPATH`.
- Homelab-analytics integration belongs behind `aligned_equity.integrations.homelab_analytics` and the root `homelab-analytics.registry.json`.

## Development workflow

- Load `.envrc` before using `sprintctl` or `kctl`.
- Use repo-local sprint and knowledge state:
  - `SPRINTCTL_DB=${PWD}/.sprintctl/sprintctl.db`
  - `KCTL_DB=${PWD}/.kctl/kctl.db`
  - `KCTL_PROJECT=aligned-equity`
- Run targeted tests while editing and `make verify-fast` before pushing or opening a PR.
- Behavior changes must add or update tests in the same change.
- Documentation or architecture changes should update `docs/README.md` when discoverability changes.

## Architecture rules

- Preserve the Finland-first source model from `docs/operational-shape.md`.
- Keep evidence, features, scorecards, lenses, and publication contracts separate.
- Treat people-platform signals as auxiliary evidence with bias flags, not core truth.
- Treat sparse enforcement/legal events as event overrides, not a primary scored axis.
- Do not add ingestion dependencies until an ingestion work item actually needs them.
- Do not make homelab-analytics a runtime dependency of the core package.

## Current verification entrypoints

- `make lint`
- `make typecheck`
- `make test`
- `make validate`
- `make hla-contract-check`
- `make verify-fast`

<!-- agentops-project-pointer:start -->
See `.agents/project.generated.md` for cross-repo project context (agentops-managed; do not hand-edit).
<!-- agentops-project-pointer:end -->
