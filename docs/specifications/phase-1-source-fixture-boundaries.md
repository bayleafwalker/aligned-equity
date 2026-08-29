# Phase 1 Source Fixture Boundaries

Phase 1 accepts source fixtures before live ingestion. A fixture is a small,
repository-controlled source-ledger payload plus representative raw or summarized
source material that exercises normalization contracts without depending on
network access, vendor credentials, browser automation, or recurring jobs.

## Accepted Source Families

| Source family | Phase 1 fixture boundary | Initial evidence classes | Required caveats |
|---|---|---|---|
| `company_ir_annual_reporting` | Company-authored annual reports, corporate governance statements, remuneration reports, remuneration policies, and investor materials already available as stable files or manually captured URLs. | `governance_statement`, `code_deviation`, `remuneration_report`, `remuneration_policy`, `esef_financials`, `earnings_call`, `leadership_change` | Preserve publication date, reporting period, language, board approval or audit context when available, and whether the fixture is a full document or excerpt. |
| `nasdaq_helsinki_announcements` | Manually captured announcement records or fixtures representing Nasdaq Helsinki / Nasdaq Nordic company announcements. | `pdmr_notice`, `leadership_change`, `regulatory_event`, `earnings_call` | Treat as announcement lineage only; do not infer outcome quality from publication alone. |
| `finnish_securities_market_association` | Stable rule-context fixtures for Corporate Governance Code and related Finnish self-regulation references. | `governance_statement`, `code_deviation` | Use as normative context, not company-specific evidence unless linked to a company disclosure. |
| `fin_fsa_supervision` | Manually captured FIN-FSA supervision, issuer, disclosure-obligation, IFRS enforcement, insider, manager transaction, sanction, or supervisory finding fixtures. | `regulatory_event`, `pdmr_notice`, `code_deviation` | Regulatory and legal events remain sparse event overrides, not a recurring primary scored axis. |
| `prh_trade_register` | Registry identity, filing status, digital statement metadata, and registered financial statement fixtures from PRH/Virre surfaces. | `esef_financials`, `regulatory_event` | Use for identity and filing cross-checks; flag lag, incomplete filings, and registry/document mismatch risk. |
| `presentations_transcripts_capital_markets_days` | Company presentation, transcript, capital markets day, and investor Q&A fixtures where source lineage and language status are explicit. | `earnings_call`, `governance_statement` | Prefer same-firm longitudinal comparisons; flag transcript vendor, translation, and prepared-remarks versus Q&A boundaries. |
| `business_media_analyst_coverage` | Reputable media or analyst fixtures used to discover events or check contradictions against primary sources. | `leadership_change`, `regulatory_event` | Default to low or medium source confidence and require corroboration notes when used beyond lead generation. |
| `people_platforms` | Public job board, employee-review, LinkedIn-style, or other people-platform fixtures captured only as auxiliary evidence. | `people_signal_aux` | Always include bias flags. Never treat as core truth or as a primary scored axis. |

## Fixture Requirements

Every accepted fixture must include a source-ledger record with:

- stable `source_id`
- allowed `source_family`
- reproducible `source_locator`
- `retrieval_method` of `manual`, `download`, `fixture`, `registry_api`, or `vendor_feed`
- `collected_at`, `observed_at`, and `freshness_as_of`
- `freshness_status`
- `source_confidence`
- `extraction_readiness`
- same-firm and cross-firm comparability fields
- bias flags when the source family or collection channel can skew coverage

Fixtures may include raw text excerpts, normalized summaries, or hashes. They must
not require live external services during validation.

## Exclusions

- Automated scraping, browser automation, and scheduled ingestion jobs.
- Paid vendor feed integration beyond manually represented fixture payloads.
- Cross-firm ranking unless fixture comparability is explicitly justified.
- People-platform evidence without bias flags.
- Regulatory or legal event fixtures that directly become scorecard dimensions.

## Acceptance For Later Ingestion Work

A later ingestion item may add source-specific collection code only after it names:

- the source family and evidence classes it produces
- the fixture set that proves the source-ledger payload shape
- the identifier normalization contract it depends on
- the freshness and comparability caveats that must survive into evidence records
- the verification command that runs without network access

