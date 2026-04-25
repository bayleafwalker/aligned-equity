# Phase 3 Scorecard Bridge Sprint

Sprint: `turku-scorecard-bridge`

## Goal

Establish Phase 3 scorecard, lens-output, same-firm report, and research-state
contracts over the longitudinal feature spine.

## Scope

- Define scorecard-run and dimension-assessment records that consume evidence,
  feature records, and time-series views without erasing lineage or caveats.
- Add runtime validation for scorecard payloads after the contract is specified.
- Define lens-specific output shape for investment, workplace, and product
  contexts without creating separate evidence vocabularies.
- Define same-firm over-time report contracts that summarize feature histories,
  scorecard movement, and material caveats.
- Implement research-state transition validation against the existing allowed
  transition vocabulary.
- Add HLA semantic metadata for scorecard and research-state publication
  surfaces while keeping HLA optional.

## Out Of Scope

- Numeric scoring or predictive rankings.
- New ingestion jobs, scrapers, vendor feeds, or source-family additions.
- Causal-effect claims without a separate causal-design contract.
- HLA runtime registration beyond package-level metadata and contract tests.
- Public publishing workflows beyond reserved publication surfaces.

## Work Items

| Item | Track | Deliverable |
|---|---|---|
| #24 | workflow | Sprint packet, live sprint state, and refreshed snapshot. |
| #25 | scorecards | Schema-backed scorecard run and dimension assessment contract. |
| #26 | scorecards | Runtime scorecard validation helper and focused tests. |
| #27 | lenses | Lens-specific output contract over scorecard and decision contexts. |
| #28 | reports | Same-firm over-time report contract over time-series views and scorecards. |
| #29 | states | Research-state transition validation helper and tests. |
| #30 | platform | HLA metadata for scorecard and research-state surfaces. |

## Acceptance

- Scorecard, lens, report, and state contracts preserve evidence, feature,
  confidence, comparability, and source-freshness boundaries.
- Runtime helpers validate semantic guardrails where JSON Schema is not enough.
- HLA metadata covers required fields for new publication surfaces without adding
  homelab-analytics as a core dependency.
- Documentation index and repository validation include new durable artifacts.
- Sprint state is updated through `sprintctl` and
  `docs/sprint-snapshots/sprint-current.txt` is generated from live state.

## Verification

- Run focused tests for any changed contract or helper.
- Run `make verify-fast` before closing each implementation item.
- Run `make hla-contract-check` when HLA publication metadata changes.
