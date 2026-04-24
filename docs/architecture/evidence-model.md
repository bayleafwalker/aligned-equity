# Evidence Model

Aligned Equity uses a Finland-first evidence model. Evidence records should preserve source identity, date, company identity, comparability notes, and confidence before any scorecard interpretation is added.

The detailed Phase 0 record contract lives in `docs/specifications/evidence-record-spec.md`.
The Finland-first source spine lives in `docs/specifications/finland-source-inventory.md`.

## Evidence classes

- `governance_statement`
- `code_deviation`
- `remuneration_report`
- `remuneration_policy`
- `esef_financials`
- `pdmr_notice`
- `earnings_call`
- `leadership_change`
- `regulatory_event`
- `people_signal_aux`

The JSON vocabulary contract lives in `schemas/evidence-class.schema.json`.

## Source treatment

- Governance and remuneration documents are core evidence for Finnish listed-company accountability and incentive alignment.
- ESEF financials and report-by-board material are core evidence for financial structure and long-run context.
- PDMR notices, earnings calls, IR materials, and capital-markets days are market-behavior evidence.
- Leadership changes, warnings, restructurings, litigation, regulatory events, and major product or service failures are event-layer evidence.
- LinkedIn, Duunitori, Oikotie, Glassdoor-like platforms, and other people-platform data are auxiliary evidence with explicit bias flags.

## Design rules

- Preserve raw source lineage before feature extraction.
- Prefer same-firm longitudinal comparisons over broad ranking.
- Treat sparse enforcement and legal signals as event overrides.
- Do not collapse evidence confidence into the same score as the behavior being evaluated.
