# Scorecard Run Specification

Scorecard runs convert evidence, feature records, and same-firm time-series views
into directional dimension assessments. They preserve material lineage,
confidence, source freshness, and comparability caveats before any lens-specific
weighting, research-state transition, or decision-output wording.

The schema-backed contract lives in `schemas/scorecard-run.schema.json`.

## Required Run Fields

| Field | Purpose |
|---|---|
| `scorecard_run_id` | Stable repository-local identifier for a scorecard evaluation. |
| `company_id` | Stable company identity key shared by all assessed material. |
| `analysis_date` | Date the scorecard run was produced. |
| `dimension_assessments` | Directional assessments for one or more scorecard dimensions. |
| `material_evidence_ids` | Evidence records that materially support the run. |
| `material_feature_ids` | Feature records that materially support the run. |
| `time_series_ids` | Same-firm time-series views that materially support the run. |
| `source_ids` | Source-ledger records represented by material evidence or features. |
| `confidence_summary` | Source, extraction, interpretation, freshness, and coverage limits. |
| `comparability_summary` | Same-firm and cross-firm caveats that constrain interpretation. |
| `source_freshness_summary` | Source-ledger freshness and extraction-readiness caveats. |
| `scorecard_notes` | Human-readable scope, caveats, and run context. |

At least one of `material_evidence_ids`, `material_feature_ids`, or
`time_series_ids` must be non-empty.

## Dimension Assessment Fields

Each `dimension_assessments` entry contains:

- `dimension`
- `assessment`
- `rationale`
- `evidence_ids`
- `feature_ids`
- `time_series_ids`
- `confidence`
- `comparability_notes`

The allowed dimensions are:

- `governance and accountability`
- `remuneration and incentive alignment`
- `management-system quality`
- `candor and reporting quality`
- `workforce continuity and organizational stability`
- `adaptability and response quality`
- `conduct and reliability`
- `evidence confidence`

The allowed assessment values are:

- `strong_negative`
- `negative`
- `neutral`
- `positive`
- `strong_positive`
- `insufficient_evidence`

Each dimension assessment must link to at least one evidence record, feature
record, or time-series view.

## Separation Rules

- Scorecard runs do not extract feature values.
- Scorecard runs do not own source retrieval, freshness, entity normalization, or
  time-series grouping.
- Scorecard runs do not contain lens weights, lens-specific action thresholds, or
  research-state transitions.
- `insufficient_evidence` is an assessment value, not permission to omit
  confidence or comparability notes.
- Numeric mappings may be added later, but this contract stores directional
  assessments and rationale first.
- Decision outputs may consume scorecard runs, but they must still satisfy
  `docs/specifications/decision-output-contract.md`.
