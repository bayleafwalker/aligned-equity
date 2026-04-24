# Source Ledger Record Specification

Source-ledger records describe collected or accepted source material before it is
split into evidence records. They preserve retrieval, freshness, coverage, and
comparability context that later evidence records and decision outputs must not
silently discard.

The schema-backed contract lives in `schemas/source-ledger-record.schema.json`.
Runtime validation is exposed by `aligned_equity.source_ledger.validate_source_ledger_record`.

## Required Record Fields

| Field | Purpose |
|---|---|
| `source_id` | Stable repository-local identifier for the source artifact or feed observation. |
| `source_family` | One of the Finland-first source families from `docs/specifications/finland-source-inventory.md`. |
| `source_name` | Human-readable title for the source artifact or source stream. |
| `source_locator` | URL, registry locator, file path, or fixture locator that can reproduce the source reference. |
| `publisher` | Organization or platform that published the source. |
| `retrieval_method` | Manual collection, download, registry API, vendor feed, or fixture. |
| `collected_at` | Timestamp when Aligned Equity collected or accepted the source. |
| `observed_at` | Date or timestamp represented by the source itself. |
| `freshness_as_of` | Date or timestamp used to judge whether the source is current enough for downstream use. |
| `expected_update_frequency` | Annual, quarterly, event-driven, irregular, one-off, or unknown. |
| `freshness_status` | Current, stale, unknown, or not-applicable. |
| `language` | Source language and translation status. |
| `source_confidence` | Authority and provenance confidence: high, medium, or low. |
| `extraction_readiness` | Whether the source is ready, needs manual review, or is not ready for extraction. |
| `same_firm_comparable` | Whether the source can compare against the same company's prior periods. |
| `cross_firm_comparable` | Whether the source can compare across companies without misleading normalization. |
| `comparability_notes` | Caveats required before using derived evidence in features or scorecards. |
| `bias_flags` | Source-family or collection-channel bias flags. |

## Optional Linkage Fields

- `coverage_start` and `coverage_end`: period covered by the source when the source is
  period-bound.
- `retrieval_notes`: collection caveats that matter before extraction.
- `raw_hash`: hash of the captured source payload when a payload is stored.
- `derived_evidence_ids`: evidence records produced from the source.

## Separation Rules

- Source-ledger records do not contain extracted feature values.
- Evidence records may reference `source_id`, but they own extraction and
  interpretation confidence.
- Freshness and comparability limits travel forward into evidence and decision
  outputs; they are not scorecard dimensions.
- Live ingestion jobs, vendor APIs, and scraping are outside this contract until a
  source-family item explicitly accepts them.
