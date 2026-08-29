# Lens Output Contract

Lens outputs apply a decision context to an existing scorecard run. They may
emphasize different scorecard dimensions and change output wording, but they do
not create new evidence vocabularies, extract new features, recompute source
lineage, or produce numeric rankings.

The schema-backed contract lives in `schemas/lens-output.schema.json`.

## Required Fields

| Field | Purpose |
|---|---|
| `lens_output_id` | Stable repository-local identifier for the lens output. |
| `scorecard_run_id` | Scorecard run consumed by the lens. |
| `company_id` | Stable company identity key inherited from the scorecard run. |
| `analysis_date` | Date the lens output was produced. |
| `lens_key` | Investment, workplace, or product lens. |
| `decision_context` | Decision context; it must match `lens_key`. |
| `dimension_emphasis` | Scorecard dimensions the lens emphasizes for this context. |
| `material_scorecard_dimensions` | Scorecard dimensions that materially affect the output. |
| `material_evidence_ids` | Evidence records carried forward from the scorecard run. |
| `material_feature_ids` | Feature records carried forward from the scorecard run. |
| `time_series_ids` | Time-series views carried forward from the scorecard run. |
| `confidence_summary` | Confidence caveats carried forward and lens-specific caveats. |
| `comparability_summary` | Comparability caveats carried forward and lens-specific caveats. |
| `lens_rationale` | Human-readable rationale for the contextual emphasis. |
| `allowed_output_uses` | Decision memo, watchlist, or same-firm report use. |

At least one material evidence, feature, or time-series ID must be present.

## Lens Boundaries

- `investment` emphasizes owner alignment, governance, incentives, candor,
  adaptability, conduct, and evidence confidence.
- `workplace` emphasizes management-system quality, workforce continuity,
  candor, conduct, adaptability, and evidence confidence.
- `product` emphasizes conduct, reliability, adaptability, management-system
  quality, reporting quality, and evidence confidence.

These are weighting tendencies, not new scorecard dimensions.

## Separation Rules

- Lens outputs do not contain scorecard dimension assessments directly; they
  reference the source scorecard run.
- Lens outputs do not create research-state transitions.
- Lens outputs do not publish action recommendations unless consumed by a
  decision output that satisfies `docs/specifications/decision-output-contract.md`.
- Lens outputs do not override confidence, comparability, source freshness, or
  causal-claim guardrails.
- Lens outputs must not make numeric predictive claims.
