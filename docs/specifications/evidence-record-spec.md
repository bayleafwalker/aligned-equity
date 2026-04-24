# Evidence Record Specification

Evidence records preserve source lineage before any feature extraction, scorecard
interpretation, lens weighting, or publication.

The schema-backed contract lives in `schemas/evidence-record.schema.json`.

## Required Record Fields

| Field | Purpose |
|---|---|
| `evidence_id` | Stable repository-local identifier for the normalized evidence record. |
| `company_id` | Stable company identity key, mapped separately from display names and tickers. |
| `source_id` | Stable key for the source document, registry entry, announcement, or platform record. |
| `source_family` | One of the source families from `docs/specifications/finland-source-inventory.md`. |
| `evidence_class` | One of the schema-backed evidence classes. |
| `document_type` | Specific document or event type, such as annual report, remuneration policy, PDMR notice, or earnings transcript. |
| `observed_at` | Date or timestamp of the underlying event or disclosure. |
| `period_start` / `period_end` | Reporting period when the evidence is period-bound. |
| `effective_date` | Date the governance, remuneration, or policy evidence became effective when different from publication date. |
| `collected_at` | Timestamp when Aligned Equity collected or observed the source. |
| `source_locator` | URL, registry locator, file path, or other reproducible source reference. |
| `language` | Source language and translation status. |
| `raw_hash` | Hash of the captured source payload when a payload is stored. |
| `extraction_method` | Manual, parser, registry API, transcript vendor, or other method. |

## Confidence Fields

Confidence is not a scorecard dimension. It travels alongside evidence and scorecard
outputs.

| Field | Values | Meaning |
|---|---|---|
| `source_confidence` | high, medium, low | Authority and provenance of the source. |
| `extraction_confidence` | high, medium, low | Reliability of extracting the relevant fact from the source. |
| `interpretation_confidence` | high, medium, low | Reliability of mapping the evidence into a feature or scorecard signal. |
| `confidence_notes` | text | Reason for any confidence limit. |

## Comparability Fields

| Field | Values | Meaning |
|---|---|---|
| `same_firm_comparable` | yes, partial, no | Whether the evidence can compare against the same company's prior periods. |
| `cross_firm_comparable` | yes, partial, no | Whether the evidence can compare across companies without misleading normalization. |
| `period_alignment` | aligned, shifted, point-in-time, unknown | Whether the period lines up with the target analysis period. |
| `accounting_scope` | parent, group, segment, unknown, not-applicable | Entity scope used by the source. |
| `restatement_status` | original, restated, corrected, unknown, not-applicable | Whether later source changes affect interpretation. |
| `comparability_notes` | text | Caveats required before using the evidence in features or scorecards. |

## Bias And Override Fields

- `bias_flags`: required for `people_signal_aux`, optional elsewhere.
- `legal_or_enforcement_override`: true only for sparse legal, enforcement, sanction, or
  severe reliability events that should override normal state transitions.
- `override_severity`: watch, thesis_weakened, deteriorating, or avoid.
- `override_expiry_review_date`: date when the override must be reviewed for continued
  relevance.

## Separation Rules

- Evidence records do not own feature values.
- Feature extraction does not own lens-specific weighting.
- Scorecards do not erase source confidence or comparability caveats.
- Lens outputs do not invent new evidence classes.
- Decision outputs consume material evidence IDs and carry confidence and comparability
  summaries forward rather than recomputing source lineage.
