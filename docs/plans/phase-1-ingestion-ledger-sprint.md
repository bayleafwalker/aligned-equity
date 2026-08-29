# Phase 1 Ingestion Ledger Sprint

Sprint: `helsinki-ingestion-ledger`

## Goal

Establish the Phase 1 ingestion and normalization foundation for Finland-first
evidence while preserving core package independence and avoiding connector-heavy
dependencies until each source family is explicitly accepted.

## Scope

- Define source-ledger records that track source identity, retrieval context,
  freshness, coverage, confidence, comparability, and bias flags before feature
  extraction.
- Establish accepted Phase 1 source-family boundaries for governance statements,
  remuneration reports and policies, ESEF filings, PDMR notices, earnings-call
  materials, and sparse regulatory or legal events.
- Specify company, security, and source identifier normalization before any
  longitudinal feature extraction depends on those identifiers.
- Add schema-backed validation helpers only where they support normalized
  source-ledger records and existing decision-output evidence lineage.
- Keep HLA publication metadata compatible with ingestion metadata without
  making homelab-analytics a runtime dependency.

## Out Of Scope

- Live scraping, vendor APIs, browser automation, or recurring ingestion jobs.
- Numeric prediction, lens weighting, or scorecard scoring.
- Homelab-analytics runtime imports from the core package.
- Treating people-platform signals as primary truth rather than auxiliary
  evidence with bias flags.

## Deliverables

- Source-ledger schema and tests.
- Source-family fixture boundary document for accepted Phase 1 inputs.
- Normalization specification for company, security, and source identifiers.
- Core validation helper for source-ledger records.
- Decision-output readiness gates for evidence that originated from ingestion.
- HLA publication metadata check covering source-ledger fields that must survive
  publication.

## Acceptance

- The sprint snapshot shows all Phase 1 items and no orphan active claims.
- Any behavior change has targeted tests in the same change.
- `make verify-fast` passes before handoff or PR update.
- The core package remains installable without homelab-analytics on
  `PYTHONPATH`.

