# Remuneration-Logic Extraction Boundary

Remuneration-logic extraction converts remuneration policies, remuneration
reports, and related company disclosures into deterministic `remuneration_logic`
feature records. The boundary captures incentive architecture and realized-pay
logic before any scorecard assessment, investment lens weighting, workplace
interpretation, or decision-output wording.

The output of this process must satisfy `schemas/feature-record.schema.json` and
can feed `docs/specifications/time-series-view-contract.md`.

## Source Scope

Accepted source families:

- `company_ir_annual_reporting`
- `nasdaq_helsinki_announcements` when the announcement publishes, corrects, or
  materially changes remuneration policy or report information
- `finnish_securities_market_association` only as Finnish Corporate Governance
  Code context for what the company should disclose
- `fin_fsa_supervision` only when the event concerns disclosure, correction, or
  supervisory context

Accepted evidence classes:

- `remuneration_report`
- `remuneration_policy`
- `governance_statement`
- `code_deviation`
- `regulatory_event`

People-platform, media, and analyst sources are out of scope for primary
remuneration-logic extraction. They may identify questions for review, but the
feature must link to company, rule-context, announcement, or supervisory
evidence before it can affect a scorecard or decision output.

## Extraction Targets

| Target | Feature key | Value type | Boundary |
|---|---|---|---|
| Variable pay criteria presence | `variable_pay_criteria_present` | boolean | Whether the policy or report names criteria for variable remuneration. |
| Variable pay criteria specificity | `variable_pay_criteria_specificity` | categorical | Whether criteria are specific, partly specific, generic, or undisclosed. |
| Financial metric link | `variable_pay_financial_metric_link` | boolean | Whether variable pay explicitly links to financial development, not whether the link is good. |
| Nonfinancial metric link | `variable_pay_nonfinancial_metric_link` | boolean | Whether variable pay explicitly links to nonfinancial criteria such as safety, conduct, customers, people, or sustainability. |
| Long-term incentive horizon | `long_term_incentive_horizon_years` | numeric | Stated vesting, performance, or holding horizon in years when disclosed. |
| Malus or clawback mechanism | `malus_clawback_mechanism_present` | boolean | Whether malus, clawback, or equivalent recovery terms are disclosed. |
| Remuneration-policy effective date | `remuneration_policy_effective_date` | date | Date when the policy became or becomes effective. |
| Realized-pay comparison period | `realized_pay_comparison_period_years` | numeric | Number of years covered by disclosed pay, employee, and financial development comparison. |
| Pay-outcome explanation specificity | `pay_outcome_explanation_specificity` | categorical | Whether realized pay outcomes are explained with concrete metrics, partly explained, generic, or undisclosed. |
| Board discretion disclosure | `board_discretion_disclosed` | boolean | Whether board or committee discretion over remuneration outcomes is disclosed. |

Initial categorical values should stay literal in `feature_value` until a later
schema adds closed vocabularies. Recommended values are `specific`,
`partly_specific`, `generic`, and `undisclosed`.

## Extraction Rules

- Extract policy design and realized-pay outcomes as separate feature records.
- Use `remuneration_policy` evidence for forward-looking design and
  `remuneration_report` evidence for realized outcomes.
- Link every feature to the exact evidence records used through
  `source_evidence_ids`.
- Use `effective_date` for policy adoption, amendment, or expiration dates.
- Use `period_start` and `period_end` for realized-pay and comparison-period
  features.
- Use `feature_unit` for numeric horizons and comparison periods, such as `years`
  or `percent`.
- Set `same_firm_comparable` to `partial` when policy scope, executive population,
  reporting period, language, or disclosure format changes.
- Set `cross_firm_comparable` to `partial` or `no` unless the feature is extracted
  from the same disclosed concept and comparable executive population.
- Preserve Finnish Corporate Governance Code deviations as evidence context; do
  not convert them into remuneration logic unless they directly alter or explain
  a remuneration feature.

## Confidence Rules

- `source_confidence` is usually `high` for company-authored remuneration reports,
  remuneration policies, and official announcements.
- `extraction_confidence` is `high` only for exact fields, tables, or clearly
  labeled policy clauses.
- `interpretation_confidence` is lower when the feature depends on narrative
  coding, translated language, ambiguous executive scope, or summary-only
  fixtures.
- `confidence_notes` must identify whether the feature came from a policy clause,
  report table, board explanation, code-deviation explanation, announcement, or
  fixture comparison.
- Missing criteria, missing realized-pay explanations, or absent clawback language
  should be recorded as deterministic absence only when the source scope is broad
  enough to support that conclusion.

## Separation Rules

- Remuneration-logic features are not scorecard assessments.
- A feature can say that a criterion, horizon, clawback term, or explanation is
  present or absent; it must not say that incentives are aligned or misaligned.
- Realized-pay comparison features preserve disclosed relationships; they do not
  infer causality between pay and financial development.
- Scorecards may use remuneration features to assess remuneration and incentive
  alignment, but they must carry forward confidence and comparability notes.
- Decision outputs must not make numeric predictive claims from remuneration
  features without a separate causal-design contract.
