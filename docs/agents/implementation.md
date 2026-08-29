# Implementation Mode

## Purpose

Execute accepted work while keeping verification close to the changed surface.

## Required inputs

- The accepted scope or active sprint item.
- The relevant architecture, specification, schema, and test contracts.
- Live `sprintctl` item and claim state when the work is sprint-scoped.

## Required checks

- Preserve the Finland-first source model.
- Keep evidence, features, scorecards, lenses, and publication contracts separate.
- Keep HLA optional and contract-bound.
- Update tests when Python behavior or repository validation changes.
- Update `docs/README.md` when discoverability changes.
- Run targeted tests during implementation.
- Run `make verify-fast` before push, PR, or broad handoff.

## Output

- Implement the change end to end where feasible.
- Report what changed, which verification commands ran, and any residual gap.
- Record durable design or workflow lessons in `sprintctl` events when the work is
  sprint-scoped.
