# Release And Ops Mode

## Purpose

Prepare work for repeatable local verification, CI validation, and handoff.

## Required checks

- `make verify-fast` remains the local blocking gate.
- `.github/workflows/verify.yaml` runs the same blocking gate on PRs and `main`.
- `UV_LINK_MODE=copy` is used on the TrueNAS mount when syncing dependencies.
- HLA checks remain optional when the sibling repo is absent.
- Secrets and local state stay outside tracked files.

## Output

Report the verification commands that ran, the result of each, and any checks that were
not run locally.
