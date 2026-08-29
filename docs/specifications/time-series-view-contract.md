# Same-Firm Time-Series View Contract

Same-firm time-series views group deterministic feature records into ordered
company histories. They are the Phase 2 read model for longitudinal analysis and
must preserve lineage, confidence, and comparability before any scorecard,
lens-specific weighting, or decision-output language is produced.

The view consumes records that satisfy `schemas/feature-record.schema.json` and
`aligned_equity.features.validate_feature_record`.

## Required View Fields

| Field | Purpose |
|---|---|
| `time_series_id` | Stable repository-local identifier for the view. |
| `company_id` | Stable company identity key shared by every included feature record. |
| `feature_key` | Single deterministic feature key represented by the series. |
| `feature_family` | Feature family inherited from the included feature records. |
| `observation_periods` | Ordered observations with period, observed date, value, and feature lineage. |
| `source_evidence_ids` | Deduplicated evidence IDs represented by all observations in the view. |
| `source_ids` | Deduplicated source-ledger IDs represented by all observations in the view. |
| `series_start` | Earliest period start, effective date, or observation date represented by the series. |
| `series_end` | Latest period end, effective date, or observation date represented by the series. |
| `same_firm_comparable` | Roll-up comparability for using the sequence as a same-firm history. |
| `period_alignment` | Roll-up period alignment across observations. |
| `accounting_scope` | Roll-up entity scope for the represented series. |
| `restatement_status` | Whether the series includes original, restated, corrected, or unknown observations. |
| `comparability_notes` | Required caveats before the series can support interpretation. |
| `confidence_notes` | Required caveats before the series can support interpretation. |

## Observation Fields

Each `observation_periods` entry must keep the feature record visible:

- `feature_id`
- `feature_value`
- `feature_value_type`
- `feature_unit` when present
- `observed_at`
- `period_start` and `period_end` when present on the feature
- `effective_date` when present on the feature
- `source_evidence_ids`
- `source_ids`
- `extraction_rule_id`
- `extraction_rule_version`
- `source_confidence`
- `extraction_confidence`
- `interpretation_confidence`
- `same_firm_comparable`
- `period_alignment`
- `accounting_scope`
- `restatement_status`
- `bias_flags`

## Eligibility Rules

- A view must contain one `company_id` and one `feature_key`.
- Every observation must link back to at least one feature record.
- Every included feature record must have `same_firm_comparable` set to `yes` or
  `partial`.
- A view with any `partial` same-firm comparability must keep the roll-up
  `same_firm_comparable` value as `partial`.
- A view must not drop observations only because they weaken a trend narrative.
- People-platform-derived observations remain auxiliary and must carry their bias
  flags into the view.
- Legal and enforcement event overrides remain evidence or lens events; they do
  not become a primary time-series axis unless represented by a deterministic
  feature family accepted for that purpose.

## Ordering And Gap Rules

- Sort period-bound observations by `period_start`, then `period_end`, then
  `observed_at`.
- Sort point-in-time observations by `effective_date` when present, otherwise
  `observed_at`.
- Preserve gaps explicitly with `gap_notes`; do not interpolate missing years,
  quarters, or events in the view contract.
- Multiple observations for the same period must preserve distinct `feature_id`
  values unless a later restatement supersedes an original observation.
- Restated or corrected observations must not silently overwrite originals; the
  view must expose `restatement_status` and lineage for each represented period.

## Separation Rules

- Time-series views do not contain scorecard dimensions, lens weights, action
  recommendations, research-state transitions, or numeric predictive claims.
- Time-series views do not own source retrieval, source freshness, or entity
  normalization.
- Feature extraction rules own feature values; the time-series view owns only
  grouping, ordering, lineage roll-ups, and comparability caveats.
- Scorecards and decision outputs may consume time-series views, but they must
  carry forward confidence and comparability notes rather than recomputing or
  hiding them.
