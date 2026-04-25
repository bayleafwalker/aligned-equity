# Reporting-Style Change Detection Specification

Reporting-style change detection converts same-firm disclosure shifts into
deterministic `disclosure_style` and `reporting_change` feature records. It is
designed for longitudinal evidence review, not sentiment scoring, peer ranking,
or automated credibility judgments.

The output of this process must satisfy `schemas/feature-record.schema.json` and
can feed `docs/specifications/time-series-view-contract.md`.

## Source Scope

Accepted source families:

- `company_ir_annual_reporting`
- `nasdaq_helsinki_announcements`
- `presentations_transcripts_capital_markets_days`
- `fin_fsa_supervision` when the event concerns disclosure, correction,
  supervision, or enforcement context
- `business_media_analyst_coverage` only as contradiction discovery or
  corroboration, not as primary reporting-style evidence

Accepted evidence classes:

- `governance_statement`
- `code_deviation`
- `remuneration_report`
- `remuneration_policy`
- `esef_financials`
- `earnings_call`
- `leadership_change`
- `regulatory_event`

People-platform evidence is out of scope for reporting-style change detection.
It can inform workforce or auxiliary people-signal features, but it must not be
used as primary evidence for disclosure quality.

## Change Types

| Change type | Feature family | Detection boundary |
|---|---|---|
| `topic_added` | `reporting_change` | A governance, remuneration, financial, risk, workforce, conduct, or strategy topic appears after being absent in comparable prior periods. |
| `topic_removed` | `reporting_change` | A previously recurring topic disappears from comparable company-authored reporting. |
| `specificity_increased` | `disclosure_style` | The source adds concrete metrics, dates, responsible bodies, policy mechanics, or outcome references. |
| `specificity_decreased` | `disclosure_style` | The source replaces concrete metrics, dates, bodies, mechanics, or outcomes with broader language. |
| `boilerplate_increased` | `disclosure_style` | Repeated generic language grows relative to company-specific detail. |
| `claim_outcome_divergence` | `reporting_change` | Prior management claims are contradicted or materially softened by later outcomes, warnings, revisions, or corrections. |
| `restatement_or_correction` | `reporting_change` | A filing, announcement, or supervisory record changes the interpretation of a prior period. |
| `deviation_explanation_changed` | `reporting_change` | Governance-code deviation explanation appears, disappears, or materially changes rationale. |

## Required Feature Keys

Initial deterministic keys should be narrow and auditable:

- `reporting_topic_added`
- `reporting_topic_removed`
- `reporting_specificity_delta`
- `reporting_boilerplate_delta`
- `reporting_claim_outcome_divergence`
- `reporting_restatement_or_correction`
- `governance_deviation_explanation_change`

Each feature record must identify the matched topic or section in
`confidence_notes` or `comparability_notes` until a structured topic vocabulary is
accepted in a later sprint.

## Detection Rules

- Compare a company against its own prior reporting before making cross-firm
  observations.
- Require at least two comparable source periods before emitting a change feature,
  unless the feature represents a one-off correction, restatement, or supervisory
  event.
- Preserve the prior-period and current-period evidence IDs in
  `source_evidence_ids`.
- Use `period_start` and `period_end` for period-bound reporting changes.
- Use `effective_date` for corrections, restatements, governance-code deviation
  explanations, or policy changes when the effective date differs from the source
  publication date.
- Set `same_firm_comparable` to `partial` when language, document scope, audited
  status, translation, or reporting-period coverage changed.
- Set `cross_firm_comparable` to `no` unless a later contract defines a stable
  topic taxonomy and normalization method.
- Flag `restatement_status` as `restated` or `corrected` when the current source
  changes prior-period interpretation.

## Confidence And Bias Rules

- `source_confidence` follows the underlying evidence source authority.
- `extraction_confidence` is `high` only when section anchors, topic labels, or
  exact fields are stable across compared periods.
- `interpretation_confidence` is usually `medium` or `low` for narrative change
  features unless the change is a correction, restatement, or explicit code
  deviation explanation.
- `confidence_notes` must state whether the change was detected from exact fields,
  matched sections, manually coded topics, or fixture comparison.
- Translation, excerpt-only fixtures, missing prior periods, changed report
  structure, and vendor transcript differences must appear in `bias_flags` or
  `comparability_notes`.

## Separation Rules

- Reporting-style features are not scorecard assessments.
- A detected change does not prove candor, deception, or management quality by
  itself.
- Omission detection is a prompt for review unless the company-specific prior
  reporting baseline is strong enough to support a deterministic feature.
- Business-media or analyst sources can identify possible contradictions, but
  the feature must link to primary company, announcement, or supervisory evidence
  before it can affect a scorecard or decision output.
- Legal and enforcement events remain event overrides when severe; ordinary
  reporting-style changes remain feature evidence for longitudinal review.
