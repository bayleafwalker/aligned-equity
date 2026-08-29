# Homelab-Analytics Publication Contract Spike

This spike defines how future Aligned Equity outputs can be published through
homelab-analytics without making HLA a runtime dependency of the core package.

## Current Boundary

- Core package: independently installable.
- HLA manifest: `homelab-analytics.registry.json`.
- HLA hooks: `aligned_equity.integrations.homelab_analytics`.
- Current hook behavior: import-safe no-op.
- Runtime dependency direction: HLA may load Aligned Equity as an external extension;
  Aligned Equity does not import HLA in normal package use.

## Reserved Publications

| Publication key | Grain | Purpose | Required semantic metadata |
|---|---|---|---|
| `aligned_equity_company_evidence` | one row per normalized evidence record | Publish source lineage and evidence metadata. | company identity, evidence class, source family, dates, confidence, comparability, bias flags. |
| `aligned_equity_scorecard` | one row per company analysis date and scorecard run | Publish dimension assessments. | dimension, assessment value, rationale, evidence links, confidence summary, comparability caveats. |
| `aligned_equity_research_state` | one row per state transition | Publish research-state history. | prior state, next state, triggering evidence, transition rationale, override flag, actor or process source. |
| `aligned_equity_source_freshness` | one row per source-ledger record | Publish source freshness, retrieval, extraction-readiness, and comparability metadata. | source ID, source family, locator, publisher, retrieval method, collection date, observed date, freshness status, confidence, extraction readiness, comparability, bias flags. |
| `aligned_equity_feature_record` | one row per deterministic feature observation | Publish feature values before scorecard interpretation. | feature ID, company ID, feature key, feature family, primitive value, evidence lineage, extraction rule, confidence, comparability, bias flags. |
| `aligned_equity_time_series_view` | one row per company, feature key, and time-series view | Publish same-firm feature histories. | time-series ID, company ID, feature key, ordered observations, lineage roll-ups, series dates, gap notes, restatement status, confidence, comparability caveats. |
| `aligned_equity_decision_memo` | one row per company, analysis date, and decision context | Publish decision-support outputs. | decision context, current research state, material evidence, confidence summary, comparability caveats, action implication, value-of-information assessment, causal-claim metadata. |

## Decision Memo Field Semantics

The package-level metadata contract lives in
`aligned_equity.hla_publications.HLA_PUBLICATION_METADATA`. For the reserved
`aligned_equity_decision_memo` publication, every required field from
`schemas/decision-output.schema.json` must have semantic metadata before a future HLA
implementation publishes rows.

Required field semantics:

- `company_id`: stable company identity key.
- `analysis_date`: date the decision memo was produced.
- `decision_context`: investment, workplace, or product decision context.
- `current_research_state`: research state before any later transition is applied.
- `material_evidence_ids`: evidence records that materially support the memo.
- `scorecard_dimension_assessments`: directional scorecard assessments with rationale and evidence links.
- `confidence_summary`: source, extraction, interpretation, freshness, and coverage limits.
- `comparability_summary`: same-firm and cross-firm caveats.
- `likely_action_implication`: practical action or non-action implication.
- `value_of_information_assessment`: whether more evidence is expected to change action.
- `value_of_information_note`: rationale for the value-of-information assessment.
- `causal_claim`: claim type and causal-design metadata when causal effects are asserted.

## Source Freshness Field Semantics

The reserved `aligned_equity_source_freshness` publication is the HLA-compatible
surface for Phase 1 source-ledger metadata. Its field metadata must cover every
required field from `schemas/source-ledger-record.schema.json`.

Required field semantics:

- `source_id`: stable source-ledger record identifier.
- `source_family`: accepted Finland-first source family.
- `source_name`: human-readable source artifact or stream name.
- `source_locator`: reproducible URL, registry locator, path, or fixture locator.
- `publisher`: organization or platform that published the source.
- `retrieval_method`: manual, download, registry API, vendor feed, or fixture path.
- `collected_at`: timestamp when Aligned Equity collected or accepted the source.
- `observed_at`: date or timestamp represented by the source itself.
- `freshness_as_of`: date or timestamp used for freshness assessment.
- `expected_update_frequency`: expected update cadence.
- `freshness_status`: current, stale, unknown, or not-applicable source status.
- `language`: source language and translation status.
- `source_confidence`: authority and provenance confidence.
- `extraction_readiness`: ready, manual-review-required, or not-ready extraction status.
- `same_firm_comparable`: same-firm longitudinal comparability.
- `cross_firm_comparable`: cross-firm comparability.
- `comparability_notes`: caveats before derived evidence is compared or scored.
- `bias_flags`: source-family or collection-channel bias flags.

## Feature Record Field Semantics

The reserved `aligned_equity_feature_record` publication is the HLA-compatible
surface for deterministic Phase 2 feature observations. Its field metadata must
cover every required field from `schemas/feature-record.schema.json`.

Required field semantics:

- `feature_id`: stable feature observation identifier.
- `company_id`: stable company identity key.
- `feature_key`: stable deterministic feature key.
- `feature_family`: governance, remuneration, financial, disclosure, reporting,
  market, or auxiliary people feature family.
- `feature_value_type`: declared primitive value type.
- `feature_value`: extracted primitive value, not a scorecard assessment.
- `observed_at`: date or timestamp represented by the underlying evidence.
- `extracted_at`: timestamp when Aligned Equity produced the feature record.
- `source_evidence_ids`: evidence records used to derive the feature.
- `source_ids`: source-ledger records represented by the linked evidence.
- `extraction_rule_id`: stable extraction rule or manual coding rubric.
- `extraction_rule_version`: extraction rule version for longitudinal auditability.
- `extraction_method`: exact field, rule-based parse, manual coding, or fixture.
- `source_confidence`: authority and provenance confidence.
- `extraction_confidence`: reliability of feature-value extraction.
- `interpretation_confidence`: reliability of evidence-to-feature mapping.
- `confidence_notes`: confidence caveats.
- `same_firm_comparable`: same-firm longitudinal comparability.
- `cross_firm_comparable`: cross-firm comparability.
- `period_alignment`: period alignment status.
- `accounting_scope`: represented entity scope.
- `restatement_status`: restatement or correction status.
- `comparability_notes`: caveats before view or scorecard use.
- `bias_flags`: source-family, extraction, or collection-channel bias flags.

## Time-Series View Field Semantics

The reserved `aligned_equity_time_series_view` publication is the HLA-compatible
surface for same-firm feature histories. It publishes the read model defined by
`docs/specifications/time-series-view-contract.md` and must not expose scorecard
dimensions, lens weights, or decision recommendations.

Required field semantics:

- `time_series_id`: stable time-series view identifier.
- `company_id`: stable company identity key.
- `feature_key`: single deterministic feature key represented by the series.
- `feature_family`: feature family inherited from the included feature records.
- `observation_periods`: ordered observations with value, period, feature lineage,
  confidence, and comparability metadata.
- `source_evidence_ids`: deduplicated evidence IDs represented by the view.
- `source_ids`: deduplicated source-ledger IDs represented by the view.
- `series_start`: earliest represented period, effective date, or observation date.
- `series_end`: latest represented period, effective date, or observation date.
- `same_firm_comparable`: roll-up same-firm comparability.
- `period_alignment`: roll-up period alignment.
- `accounting_scope`: roll-up entity scope.
- `restatement_status`: whether the view includes original, restated, corrected,
  or unknown observations.
- `gap_notes`: explicit gaps in years, quarters, events, or comparable source
  coverage.
- `comparability_notes`: caveats before interpretation.
- `confidence_notes`: confidence caveats before interpretation.

## Future HLA Shape

When real HLA integration is implemented:

- Landing owns raw source payload registration and validation.
- Transformation owns normalized evidence, feature extraction, and state-transition
  models.
- Reporting owns publication-ready marts under the reserved publication keys.
- Application consumers read reporting publications, not landing payloads or warehouse
  internals.

## Acceptance For A Future Spike-To-Implementation Sprint

- Add publication contract tests that validate every exported field has semantic metadata.
- Validate the manifest through the sibling HLA loader.
- Keep duplicate publication-key rejection active.
- Prove the core package imports without HLA on `PYTHONPATH`.
- Add no ingestion-heavy dependencies until an accepted ingestion item requires them.
