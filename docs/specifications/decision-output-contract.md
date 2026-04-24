# Decision Output Contract

Decision outputs connect scorecard evidence to a real decision or non-decision. They are
not numeric rankings and they do not make causal claims unless a causal design is
declared.

The schema-backed contract lives in `schemas/decision-output.schema.json`.

The first runtime vertical slice validates normalized evidence records, confirms they
belong to one company, and builds a decision memo with material evidence IDs plus
confidence and comparability summaries. This keeps decision output downstream of
evidence lineage without introducing ingestion or numeric scoring.

When evidence comes from Phase 1 source-ledger records, decision-output construction
also applies ingestion readiness gates through
`aligned_equity.source_ledger.validate_decision_readiness`.

## Required Fields

| Field | Purpose |
|---|---|
| `company_id` | Stable company identity key. |
| `analysis_date` | Date of the decision output. |
| `decision_context` | One of `investment`, `workplace`, or `product`. |
| `current_research_state` | Current schema-backed research state. |
| `material_evidence_ids` | Evidence records that materially support the output. |
| `scorecard_dimension_assessments` | Directional dimension assessments with rationale and evidence links. |
| `confidence_summary` | Source, extraction, interpretation, freshness, and coverage limits that matter for the decision. |
| `comparability_summary` | Same-firm and cross-firm caveats that constrain interpretation. |
| `likely_action_implication` | Practical decision or non-decision implication. |
| `value_of_information_assessment` | Whether more evidence is worth collecting before action. |
| `value_of_information_note` | Why more research may or may not change the decision. |
| `causal_claim` | Structured guardrail distinguishing association, warning signal, decision relevance, and causal effect claims. |

## Value Of Information Assessments

- `collect_more_evidence`: missing or weak evidence could plausibly change the decision.
- `monitor_freshness`: the current decision can stand, but source age or coverage needs monitoring.
- `more_research_unlikely_to_change_action`: additional research is unlikely to change the current action or non-action.

## Ingestion Readiness Gates

- Every material evidence record from ingestion must have a matching
  source-ledger record by `source_id`.
- The evidence `source_family` must match the source-ledger `source_family`.
- If a source-ledger record has `derived_evidence_ids`, every material evidence ID
  must be listed there.
- `not-ready` sources cannot support decision output.
- `manual-review-required` sources require
  `value_of_information_assessment = collect_more_evidence`.
- `stale` or `unknown` source freshness cannot be paired with
  `more_research_unlikely_to_change_action`.

## Causal-Claim Guardrails

Decision outputs may describe association, warning signals, confidence, comparability,
and decision relevance. They must not say that one company attribute caused an outcome
unless `causal_claim.claim_type` is `causal_effect` and `causal_design` explains the
identification basis.

This rule exists because Aligned Equity is a decision-support system. Governance,
management-system, workforce, and conduct signals can be decision-relevant without
being validated causal explanations of later outcomes.

## Calibration Path

Phase 0 keeps directional assessments and rationale first. Future calibration work can
compare stated confidence and decision implications against later review artifacts, but
the current contract avoids fake precision and does not publish numeric predictive
scores.
