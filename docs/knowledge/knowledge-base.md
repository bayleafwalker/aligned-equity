# Knowledge Base — aligned-equity
Generated: 2026-04-24T16:01:29Z

## Decisions

### HLA source freshness metadata covers source-ledger ingestion fields
Source: track: platform, sprint: 2
Tags: source-ledger

Added package-level metadata for aligned_equity_source_freshness and tests that require metadata coverage for every required source-ledger schema field. This keeps ingestion freshness, readiness, comparability, and bias metadata compatible with future HLA publications without adding HLA runtime imports.

---

### Identifier normalization separates company, security, and source aliases
Source: track: entities, sprint: 2
Tags: phase-1

Added schema-backed entity identifier records and a validation helper. Finnish entities require business ID or PRH identity, listed securities require ISIN and MIC, and source aliases map accepted source families back to stable company IDs without making tickers durable company keys.

---

### Decision outputs now gate ingested evidence readiness
Source: track: product, sprint: 2
Tags: readiness

Added validate_decision_readiness and threaded it into build_decision_output when source-ledger records are supplied. Decision outputs now require source-ledger linkage, matching source families, derived-evidence consistency, ready extraction status, and VOI alignment for stale, unknown, or manual-review sources.

---

### Phase 1 source families accept fixtures before live ingestion
Source: track: sources, sprint: 2
Tags: phase-1

Defined accepted fixture boundaries for each Finland-first source family. Fixtures must use source-ledger records, run without network access, preserve freshness and comparability caveats, and keep people-platform signals auxiliary with bias flags.

---

### Source-ledger records now have runtime validation
Source: track: ingestion, sprint: 2
Tags: ingestion

Added aligned_equity.source_ledger.validate_source_ledger_record to validate source-ledger schema payloads and enforce Phase 1 guardrails: people-platform sources need bias flags, and not-ready sources cannot link derived evidence IDs.

---

### Opened Phase 1 ingestion-ledger sprint
Source: track: workflow, sprint: 2
Tags: ingestion

Created helsinki-ingestion-ledger as the Phase 1 sprint for source-ledger, source-family, identifier-normalization, validation-helper, readiness-gate, and HLA metadata work. The scope explicitly excludes live ingestion jobs, numeric scoring, and HLA runtime dependencies.

---

### Source ledger is a separate contract before evidence extraction
Source: track: evidence, sprint: 2
Tags: phase-1

Added a schema-backed source-ledger record specification for retrieval method, freshness, coverage, source confidence, extraction readiness, comparability, and bias flags. Source-ledger records describe accepted source material before derived evidence records and explicitly exclude live ingestion jobs or extracted feature values.

---

### Decision memo HLA metadata prepared
Source: track: platform, sprint: 1
Tags: hla, publication-metadata

Added package-level semantic metadata for aligned_equity_decision_memo and tests that require metadata coverage for every required decision-output schema field.

---

### Decision outputs are now a contract surface
Source: track: product, sprint: 1
Tags: decision-quality, contract

The decision memo schema, validation helper, VOI assessment enum, and causal-design guardrail implement the knowledge-base assessment without introducing numeric predictive scoring.

---

### Evidence-to-decision vertical slice implemented
Source: track: evidence, sprint: 1
Tags: evidence, decision-quality

Added schema-backed normalized evidence validation and a deterministic builder that carries material evidence IDs, confidence summaries, and comparability summaries into decision-output validation without adding ingestion or numeric scoring.

---

### Phase 0 starts with specification artifacts before ingestion dependencies
Source: sprint: 1
Tags: phase-0, evidence-model, ingestion

The Finland evidence spine is captured as source inventory, evidence record, lens scorecard, HLA publication spike, and six-month decision-impact docs. This preserves the architecture rule that ingestion-heavy dependencies wait for accepted ingestion work.

---

### Copied HLA working-process model
Source: track: workflow, sprint: 1
Tags: workflow, dispatch

Aligned Equity adopted the fuller homelab-analytics source-of-truth, dispatch, claim, snapshot, and closeout workflow shape while preserving Finland-first architecture boundaries.

---

### Onboard HLA-style workflow without importing HLA runtime dependencies
Source: sprint: 1
Tags: workflow, hla-boundary, phase-0

Aligned Equity adopted repo-local sprintctl and kctl workflow targets, agent mode guides, and reusable skills from the homelab-analytics operating model while keeping the core package independently installable and HLA integration behind the manifest and no-op hooks.

---
