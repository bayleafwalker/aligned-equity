# Finland-First Source Inventory

This inventory defines the Phase 0 source spine for Finnish listed-company alignment
analysis. It is a specification, not an ingestion backlog. Sources become ingestion work
only when a later sprint accepts that scope.

## Source Tiers

| Tier | Source family | Primary use | Evidence classes | Default confidence | Notes |
|---|---|---|---|---|---|
| Core | Company IR and annual reporting | Company-authored governance, remuneration, financial, strategy, and event evidence | `governance_statement`, `code_deviation`, `remuneration_report`, `remuneration_policy`, `esef_financials`, `earnings_call`, `leadership_change` | high for authorship, medium for interpretation | Preserve document version, language, publication date, reporting period, and whether the source is audited or board-approved. |
| Core | Nasdaq Helsinki / Nasdaq Nordic company announcements | Timely disclosures, releases, market notices, and listing context | `pdmr_notice`, `leadership_change`, `regulatory_event`, `earnings_call` | high for publication event, medium for semantic classification | Treat as announcement lineage. Do not assume the announcement alone proves outcome quality. |
| Core | Finnish Securities Market Association self-regulation | Corporate Governance Code, code deviations, takeover-code context, and interpretation anchors | `governance_statement`, `code_deviation` | high for rule context | Use as normative context for Finnish listed companies, not as company-specific evidence by itself. |
| Core | FIN-FSA issuer and market supervision material | Disclosure obligation, IFRS enforcement, insider/manager transaction context, sanctions, and supervisory findings | `regulatory_event`, `pdmr_notice`, `code_deviation` | high for supervisory event, sparse for scoring | Regulatory and legal events are event overrides. They are not a primary scored axis. |
| Core | PRH Trade Register, Virre, and PRH open data | Company identity, registered financial statements, filing status, and digital statement metadata | `esef_financials`, `regulatory_event` | high for registry fact, variable for document completeness | Use for identity and filing cross-checks. Registered statements may be incomplete or lag operating disclosures. |
| Supporting | Company presentations, transcripts, capital markets days, and investor Q&A | Candor, consistency, capital allocation narrative, and management-system signals | `earnings_call`, `governance_statement` | medium | Prefer same-firm longitudinal changes over peer ranking. Flag transcript vendor and language translation risk. |
| Supporting | Reputable business media and analyst coverage | Event discovery and contradiction checks | `leadership_change`, `regulatory_event` | low to medium | Use as lead-generation or corroboration unless the primary document is unavailable. |
| Auxiliary | LinkedIn, job boards, employee-review platforms, and other people-platform signals | Workforce continuity, hiring pattern, reputation, and reorganization clues | `people_signal_aux` | low | Always attach bias flags. Never treat as core truth. |

## Phase 0 Source Rules

- Every source record needs a stable source family, source owner, collection timestamp,
  original URL or locator, document date, and reporting period where applicable.
- Same-firm longitudinal comparability is the default comparison mode.
- Cross-firm comparison is allowed only when the document type, fiscal period, language,
  and accounting scope are comparable enough to state why.
- Evidence confidence, extraction confidence, and interpretation confidence are separate
  fields.
- A sparse enforcement or legal event can override a research state, but it does not
  become a recurring primary score dimension.

## Official Reference Anchors

- Finnish Securities Market Association:
  [Corporate Governance Code](https://www.cgfinland.fi/en/corporate-governance-code/).
- FIN-FSA:
  [issuer, disclosure-obligation, ESEF, and market-supervision sections](https://www.finanssivalvonta.fi/en/functions/sitemap/).
- PRH:
  [digital financial statements](https://www.prh.fi/en/companiesandorganisations/financial_statements/limited_liability_companies_co-operatives_and_other_companies/digital.html)
  and related Trade Register services.
- Nasdaq:
  [Helsinki market](https://www.nasdaq.com/solutions/european-markets/helsinki)
  and company announcement surfaces.
