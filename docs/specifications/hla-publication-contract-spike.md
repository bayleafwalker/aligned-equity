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
