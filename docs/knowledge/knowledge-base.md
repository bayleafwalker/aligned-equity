# Knowledge Base — aligned-equity
Generated: 2026-04-24T14:57:28Z

## Decisions

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
