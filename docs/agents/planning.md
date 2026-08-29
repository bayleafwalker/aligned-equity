# Planning Mode

## Purpose

Turn a request into a decision-complete implementation plan before repo edits begin.

Use `docs/runbooks/project-working-practices.md` to decide whether the work is new
scope registration, existing sprint-item execution, or direct implementation.

## Allowed actions

- Read code, docs, schemas, tests, local configuration, and sprint state.
- Run non-mutating checks that reduce ambiguity.
- Compare implementation options against architecture and product constraints.

## Required checks

- Confirm the affected boundary: source inventory, evidence record, feature extraction,
  scorecard, lens output, research state, or HLA publication contract.
- Confirm whether the work already exists in `sprintctl`.
- Confirm whether docs, schemas, tests, or validation need to move with the change.
- Identify the local verification path.

## Stop and escalate

- Stop if the plan would make homelab-analytics a runtime dependency.
- Stop if the plan collapses evidence, scorecard interpretation, and lens output into
  one model.
- Stop if the plan treats people-platform data as core truth or legal events as a
  primary scored axis.
