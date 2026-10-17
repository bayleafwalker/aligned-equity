---
doc_id: finland-first-useful-evidence-and-decision-impact
status: planned
---

# Finland-First Useful Evidence and Decision Impact

## Goal

Make the existing `finland-evidence-spine` and `helsinki-ingestion-ledger` work yield one useful, auditable evidence-to-decision path for a Finnish public company. Produce a source-quality-qualified evidence packet and determine whether evidence changed an investment/research decision, supported a deliberate non-decision, or exposed a material evidence gap.

This packet uses the existing source, evidence, feature, lens, and decision contracts. It does not activate broad rankings, prediction, live scraping, vendor APIs, or an HLA runtime dependency.

## Dependencies and boundaries

- Use `docs/specifications/finland-source-inventory.md` and `phase-1-source-fixture-boundaries.md`.
- Use the `helsinki-ingestion-ledger` records for source identity, retrieval, freshness, coverage, confidence, comparability, bias, and issuer/security/source normalization.
- Preserve evidence → feature → scorecard → lens → decision-output separation and the causal-claim guardrails.
- Use `docs/product/six-month-success-criteria.md` as the decision-impact measure.
- Keep the core independently installable. HLA publication stays optional behind the existing registry.

## Work

1. **Predeclare one case.** Choose a Helsinki-listed company only after confirming that primary documents support a bounded sample. State the question, what evidence could change the research state, and what would count as insufficient. Do not choose based on a desired score.
2. **Qualify sources.** For each item record issuer/source, canonical URL or fixture identity, source type, language, publication and retrieval dates, reporting period, entity/security identifiers, covered sections, extraction method, and lineage. Record missing periods, restatements, scope changes, comparability, confidence, and bias flags. Keep primary records distinct from commentary; gaps stay gaps.
3. **Build a bounded output.** Derive only features/lens judgments justified by the packet. Separate source facts, normalized features, analyst judgment, scorecard/lens output, and decision. Link material conclusions to evidence and counterevidence. Sparse legal events remain overrides, not recurring scores; people-platform signals remain auxiliary and bias-flagged.
4. **Record realized impact.** Record action or non-action, research-state change, rationale, evidence gaps, expected value of more information, and the condition that would trigger reconsideration. At follow-up say whether evidence changed the action, preserved non-action, or revealed a gap. Scores and forecasts are not realized outcomes; causal impact needs causal design.

## Acceptance

- One Finnish issuer has a source inventory with explicit coverage and gaps.
- Each material item has lineage, retrieval/reporting context, confidence, and comparability treatment.
- The output distinguishes observations, features, judgment, lens output, and final decision.
- One real decision or explicit non-decision is recorded against the predeclared question and reconstructible from evidence.
- Follow-up records whether evidence changed the decision, preserved non-action, or exposed a gap without unsupported causal claims.
- Missing or biased evidence cannot silently become a favorable score.
- Fixture/schema work remains within Phase 1 boundaries; no live connector, predictive model, broad ranking, or HLA runtime import is needed.

## Completion evidence

A reviewer can reconstruct what was known, how trustworthy and comparable the sources were, what decision was made or withheld, and whether subsequent observed behavior supports the stated decision impact.
