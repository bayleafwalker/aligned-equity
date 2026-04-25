# Feature Record Specification

Feature records are deterministic facts extracted from normalized evidence. They
preserve evidence lineage, extraction-rule identity, confidence, and comparability
before any scorecard interpretation, lens weighting, or decision-output wording.

The schema-backed contract lives in `schemas/feature-record.schema.json`.
Runtime validation is exposed by `aligned_equity.features.validate_feature_record`.

## Required Record Fields

| Field | Purpose |
|---|---|
| `feature_id` | Stable repository-local identifier for the extracted feature observation. |
| `company_id` | Stable company identity key inherited from the source evidence records. |
| `feature_key` | Stable machine key for the deterministic feature, such as `board_independence_ratio` or `variable_pay_criteria_present`. |
| `feature_family` | One of the schema-backed feature families for governance, remuneration, financial development, disclosure style, reporting change, capital-markets signal, or auxiliary people signal features. |
| `feature_value_type` | Declared primitive value type: boolean, categorical, numeric, text, or date. |
| `feature_value` | Extracted primitive value. It must be a deterministic observation, not a score, forecast, or lens assessment. |
| `observed_at` | Date or timestamp represented by the underlying evidence. |
| `extracted_at` | Timestamp when Aligned Equity produced the feature record. |
| `source_evidence_ids` | Evidence records used to derive the feature. At least one evidence ID is required. |
| `source_ids` | Source-ledger IDs represented by the linked evidence. At least one source ID is required. |
| `extraction_rule_id` | Stable identifier for the extraction rule or manual coding rubric. |
| `extraction_rule_version` | Version of the extraction rule so longitudinal changes are auditable. |
| `extraction_method` | Exact field, rule-based parse, manual coding, or fixture. |

## Optional Period Fields

- `period_start` and `period_end`: reporting period covered by the feature when it
  is period-bound.
- `effective_date`: date the governance, remuneration, policy, or practice feature
  became effective when different from publication or observation date.
- `feature_unit`: unit for numeric values, such as percent, EUR, count, or ratio.

## Confidence And Comparability

Feature records carry forward the same confidence and comparability vocabulary as
evidence records:

- `source_confidence`
- `extraction_confidence`
- `interpretation_confidence`
- `confidence_notes`
- `same_firm_comparable`
- `cross_firm_comparable`
- `period_alignment`
- `accounting_scope`
- `restatement_status`
- `comparability_notes`
- `bias_flags`

These fields are required because Phase 2 is longitudinal-first. A feature that
cannot safely compare against the same firm's prior periods must say so before it
is eligible for time-series views or scorecard use.

## Determinism Rules

- Feature records must derive from one or more evidence records.
- Feature records do not own source retrieval, source freshness, or identity
  normalization. Those remain in source-ledger and entity records.
- Feature records do not contain scorecard dimensions, lens-specific weights,
  research-state transitions, or action recommendations.
- `feature_value` must be the output of a named extraction rule or manual coding
  rubric, not a probabilistic judgment.
- People-platform-derived features remain auxiliary and require bias flags.
- Legal and enforcement events remain event overrides in evidence and lens logic;
  they are not a primary scored feature family.
