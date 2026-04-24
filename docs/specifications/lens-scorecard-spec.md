# Lens Scorecard Specification

Aligned Equity uses one dimensional scorecard with thin decision lenses on top.

## Scorecard Dimensions

Each dimension can be assessed as `strong_negative`, `negative`, `neutral`, `positive`,
`strong_positive`, or `insufficient_evidence`. Numeric mappings may be added later, but
Phase 0 stores direction and rationale first.

| Dimension | Evidence emphasis |
|---|---|
| governance and accountability | Board composition, independence, code deviations, shareholder treatment, related-party signals. |
| remuneration and incentive alignment | Pay policy, realized pay, long-term incentive design, malus/clawback, and target quality. |
| management-system quality | Operating cadence, capital allocation discipline, risk controls, and follow-through. |
| candor and reporting quality | Consistency between claims, outcomes, warnings, revisions, and disclosure detail. |
| workforce continuity and organizational stability | Leadership churn, restructuring cadence, employee-platform auxiliary signals, and hiring patterns. |
| adaptability and response quality | Response to shocks, regulatory changes, competition, and operational failures. |
| conduct and reliability | Regulatory events, litigation, severe service failures, and trust-impacting conduct. |
| evidence confidence | Coverage, recency, source authority, extraction confidence, and comparability limits. |

## Lens Outputs

| Lens | Primary question | Weighting tendency |
|---|---|---|
| `investment` | Does the evidence improve or weaken long-term owner alignment? | Governance, incentives, candor, adaptability, and conduct dominate. |
| `workplace` | Would this company be a credible place to work or stay? | Management-system quality, workforce continuity, candor, and conduct dominate. |
| `product` | Does the company look reliable as a supplier or product operator? | Conduct, adaptability, management-system quality, and reporting quality dominate. |

Lenses may change weights, output wording, and action thresholds. They may not create
separate evidence vocabularies.

## Research State Transitions

Allowed transitions:

| From | To |
|---|---|
| `watch` | `long_term_candidate`, `dislocation_candidate`, `thesis_weakened`, `deteriorating`, `avoid` |
| `long_term_candidate` | `thesis_strengthened`, `thesis_weakened`, `watch`, `deteriorating`, `avoid` |
| `dislocation_candidate` | `thesis_strengthened`, `thesis_weakened`, `watch`, `deteriorating`, `avoid` |
| `thesis_strengthened` | `long_term_candidate`, `watch`, `thesis_weakened`, `deteriorating` |
| `thesis_weakened` | `watch`, `deteriorating`, `avoid`, `thesis_strengthened` |
| `deteriorating` | `watch`, `avoid`, `thesis_weakened` |
| `avoid` | `watch` |

Transitions require:

- current state
- proposed state
- triggering evidence IDs
- scorecard dimension changes
- confidence and comparability summary
- event override flag when applicable
- human-readable rationale

## Output Contract

Every scorecard or lens output must include:

- company ID and analysis date
- source freshness summary
- dimension assessments with evidence links
- confidence and comparability caveats
- research state before and after any transition
- lens key when the output is lens-specific

Decision-facing outputs must also satisfy
`docs/specifications/decision-output-contract.md`. They should state the decision or
non-decision context, material evidence, likely action implication, and value of
information before any numeric scoring is introduced.
