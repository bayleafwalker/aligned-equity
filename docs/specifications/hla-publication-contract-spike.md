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
| `aligned_equity_source_freshness` | one row per company and source family | Publish coverage and freshness. | latest source date, collection date, source authority, missing-source reason, freshness status. |
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
