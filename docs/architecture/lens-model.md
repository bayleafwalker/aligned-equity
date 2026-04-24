# Lens Model

Aligned Equity uses one dimensional scorecard with thin decision lenses on top. The scorecard owns the evidence interpretation; lenses own context-specific weighting and output shape.

The detailed Phase 0 scorecard and transition contract lives in `docs/specifications/lens-scorecard-spec.md`.

## Dimensions

- governance and accountability
- remuneration and incentive alignment
- management-system quality
- candor and reporting quality
- workforce continuity and organizational stability
- adaptability and response quality
- conduct and reliability
- evidence confidence

## Lens keys

- `investment`
- `workplace`
- `product`

The JSON vocabulary contract lives in `schemas/lens.schema.json`.

## Research states

- `long_term_candidate`
- `dislocation_candidate`
- `watch`
- `thesis_strengthened`
- `thesis_weakened`
- `deteriorating`
- `avoid`

The JSON vocabulary contract lives in `schemas/research-state.schema.json`.

## Rules

- Lenses may weight dimensions differently, but they must not invent separate evidence vocabularies.
- Cross-sectional ranking is secondary to same-firm-over-time analysis.
- Lens outputs must carry evidence confidence and source freshness alongside conclusions.
