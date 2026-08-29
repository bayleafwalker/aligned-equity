# Entity Identifier Normalization

Entity identifier records provide the company, security, and source alias keys that
Phase 1 ingestion fixtures must use before longitudinal evidence can be compared.
They are identity normalization records, not issuer profiles or scorecard inputs.

The schema-backed contract lives in `schemas/entity-identifier-record.schema.json`.
Runtime validation is exposed by `aligned_equity.identifiers.validate_entity_identifier_record`.

## Required Record Fields

| Field | Purpose |
|---|---|
| `company_id` | Stable Aligned Equity company key used by evidence, decision outputs, and publications. |
| `display_name` | Current human-readable company name for review surfaces. |
| `domicile_country` | Country code or country name used to distinguish Finland-first identity rules from later markets. |
| `identifier_confidence` | High, medium, or low confidence in the identity mapping. |
| `company_identifiers` | External company identifiers such as Finnish business ID, LEI, or PRH Trade Register number. |
| `source_aliases` | Source-family-specific names, tickers, registry values, or source IDs that map back to `company_id`. |
| `normalization_notes` | Caveats, unresolved ambiguities, name-change notes, or source conflicts. |

## Optional Security Fields

`security_identifiers` records listed or formerly listed securities linked to the
company. A listed security should preserve:

- stable `security_id`
- `isin`
- `ticker`
- `market`
- `mic`
- `currency`
- `listing_status`

Security identifiers are separate from company identifiers because filings,
announcements, source ledgers, and decision outputs may refer to different levels
of the same issuer structure.

## Normalization Rules

- Finnish-domiciled companies require either `business_id` or
  `prh_trade_register_number`.
- Listed securities require both `isin` and `mic` when `listing_status` is
  `listed`.
- Every source alias must use an accepted Phase 1 source family.
- Source aliases are lineage helpers. They do not replace `source_id` in
  source-ledger records or `company_id` in evidence records.
- Low-confidence mappings may be stored, but downstream evidence must carry the
  identity caveat in confidence or comparability notes.

## Out Of Scope

- Corporate action history beyond stable current and fixture identifiers.
- Security master synchronization with live exchange or vendor feeds.
- Entity resolution by fuzzy matching without explicit review.
- Using ticker alone as a durable company identity key.

