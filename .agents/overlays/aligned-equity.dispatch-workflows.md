# Aligned equity dispatch workflow overlay

## Repository boundaries

- Keep the core package independently installable without `homelab-analytics`
  on `PYTHONPATH`. Any integration belongs behind
  `aligned_equity.integrations.homelab_analytics` and
  `homelab-analytics.registry.json`.
- Preserve the Finland-first source model in `docs/operational-shape.md`.
  Treat people-platform signals as auxiliary evidence with bias flags, not core
  truth. Treat sparse enforcement or legal events as event overrides, not a
  primary scored axis.
- For domain-impact work, identify the affected source inventory, evidence
  record, feature extraction, scorecard, lens output, research state, or HLA
  publication boundary. Confirm whether each source is core evidence, auxiliary
  evidence, or an event override before approving scope.

## Local sprint and knowledge workflow

- Load the repo-local environment before using sprintctl or kctl:
  `SPRINTCTL_DB=${PWD}/.sprintctl/sprintctl.db`,
  `KCTL_DB=${PWD}/.kctl/kctl.db`, and `KCTL_PROJECT=aligned-equity`.
- Prefer `tools/workflow.sh` for `sprint-resume`, `claim-recover`,
  `claim-heartbeat`, `item-verify-auth`, `snapshot-refresh`, and
  `knowledge-publish`. It enforces the local database paths and records claim
  identity consistently.
- Claim recovery tokens under `.sprintctl/claims/` are local crash-recovery
  aids, not authority to adopt another identity. Follow `sprintctl
  agent-protocol --json` for actual claim ownership and handoff rules.
- Use three-word hyphenated sprint codenames. Consult live sprintctl state rather
  than a committed snapshot before creating, resuming, or claiming work.

## Verification and documentation

- Run targeted tests while editing. Before pushing or opening a PR, run
  `make verify-fast`; it includes lint, type checks, tests, validation, and the
  homelab-analytics contract check.
- Behavior changes require updated tests. Documentation or architecture changes
  that affect discoverability must update `docs/README.md`.
- Do not introduce source-ingestion dependencies until an accepted ingestion
  work item needs them.