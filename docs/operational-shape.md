## Revised operating shape for Aligned Equity

### 1. Evidence model: Finland-primary

I’d redefine the core evidence stack like this:

* **Governance core:** Corporate Governance Statement, Corporate Governance Code deviations, board/committee composition, independence, nomination structure, internal control/risk descriptions. ([Arvopaperimarkkinayhdistys][4])
* **Remuneration core:** Remuneration Report, Remuneration Policy, actual payout logic, variable-pay criteria, five-year remuneration-vs-employee-vs-financial-development comparison. ([Arvopaperimarkkinayhdistys][2])
* **Financial structure core:** ESEF annual financial reports, report by the board, IFRS-tagged primary statements, key ratios over time. ([Nasdaq][3])
* **Market-behavior core:** earnings calls, capital-markets days, IR presentations, and **PDMR/manager transaction notifications** as structured behavior signals. The Securities Market Association’s MAR guidance highlights the notification obligations for persons discharging managerial responsibilities and their closely associated persons. ([Arvopaperimarkkinayhdistys][5])
* **Event layer:** management changes, profit warnings, restructurings, major strategy resets, litigation/regulatory items, and selected product/service failures.

That gives you a properly Finnish backbone instead of trying to smuggle the US proxy statement back in through the side door.

### 2. Longitudinal-first, cross-sectional-second

For a 10–20 firm Finland-heavy universe, I’d make the primary unit of value **firm-over-time**, not “rank all companies this quarter.” Your own methodology notes already push in this direction: use exogenous indicators, separate them from later outcomes, and preserve process descriptions over time rather than collapsing everything into a single post-hoc performance story.

So the main analytical views should be:

* same firm over 5–10 years
* same firm before/after major leadership or incentive changes
* same firm before/after major capital allocation shifts
* same firm before/after recurring governance deviations or reporting-style changes

Cross-sectional ranking still exists, but as a secondary convenience layer.

### 3. Dimensional scorecard + lenses

I think your “lenses” point is exactly right.

Keep one underlying dimensional scorecard:

* governance and accountability
* remuneration and incentive alignment
* management-system quality
* candor / reporting quality
* workforce continuity / organizational stability
* adaptability / response quality
* conduct / reliability
* evidence confidence

Then apply thin **lenses** on top:

* **Investment lens:** adds valuation, capital allocation, portfolio fit.
* **Workplace lens:** weights management quality, retention, integrity, psychological-safety-adjacent signals.
* **Product lens:** weights conduct, reliability, support continuity, stability.

That preserves the “bundles, not isolated trivia” logic from your earlier work while avoiding three separate scoring religions. Your notes are explicit that capabilities are bundles involving management systems, norms and values, and other complementary resources rather than isolated variables.

### 4. Enforcement/legal signal as event override, not a main axis

I agree with your caution here.

I would not make “regulatory/legal trouble frequency” a standalone scored dimension for a small Finnish universe. ESMA’s latest consolidated sanctions report explicitly says sanctioning practices differ significantly across member states and that supervisory effectiveness cannot be measured solely by the number or value of sanctions. Finland clearly does have real enforcement actions, but in your likely sample the signal will be too sparse and uneven to support a stable scored axis. Treat it as an **override/event flag**, not a quietly punitive background score. ([ESMA][6])

### 5. People-platform data stays auxiliary

I’d hard-code this as a design rule: LinkedIn / Duunitori / Oikotie / similar sources are **auxiliary evidence with bias flags**, not core truth. Your industry-skew point is exactly the kind of thing that silently poisons a neat-looking model.

## Revised Phase 0 deliverables

This should now be explicit.

### A. Finland-first source inventory

A document that says, for each intended source:

* what signal class it supports
* which firms have it consistently
* since when it is available
* whether it is structured / semi-structured / unstructured
* likely comparability issues

### B. Evidence model spec

Define evidence classes such as:

* `governance_statement`
* `code_deviation`
* `remuneration_report`
* `remuneration_policy`
* `esef_financials`
* `pdmr_notice`
* `earnings_call`
* `leadership_change`
* `regulatory_event`
* `people_signal_aux`

### C. Lens spec

A thin document defining:

* underlying dimensions
* lens weights
* lens-specific evidence
* which outputs each lens is allowed to produce

### D. Plugin contract artifact

You were right to make this concrete. Phase 0 should produce:

* what Aligned Equity **imports** from homelab-analytics, if anything
* what it **reimplements**
* what it **publishes**
* the published artifact/schema boundary
* what is private-only vs publishable

That is not “future learning.” That is one of the actual outputs.

### E. Research-state vocabulary

I like your positive-specification version better than a non-goals list. I’d use something like:

* `long_term_candidate`
* `dislocation_candidate`
* `watch`
* `thesis_strengthened`
* `thesis_weakened`
* `deteriorating`
* `avoid`

Closed vocabularies are underrated. They stop systems from inventing new metaphysics at 02:00.

## Revised roadmap

### Phase 0 — Finland-first design

* source inventory
* evidence model
* lens model
* plugin contract
* research-state vocabulary
* success criteria

### Phase 1 — Ingestion and normalization

* ingest CG statements, remuneration reports/policies, ESEF filings, PDMR notices, earnings calls
* normalize company/entity/security history
* track evidence freshness and comparability

### Phase 2 — Longitudinal feature extraction

* deterministic features first
* time-series views per firm
* deviation/explanation extraction
* remuneration-logic extraction
* reporting-style change detection

### Phase 3 — Scorecards and reports

* dimensional scorecard
* lens-specific outputs
* same-firm-over-time reports
* watchlist and state transitions

### Phase 4 — Publication and HLA integration

* emit contract artifacts
* private read models first
* curated public outputs second

## The unresolved piece: success criteria

You’re right that “help foundations of decisions” is too soft.

I’d pick one **primary success test** and two **secondary tests** before scoring code ships.

My recommendation for the primary one:

**After 6 months, Aligned Equity must have materially changed the reasoning of at least 3 real decisions or non-decisions across investment, workplace, or product contexts, with evidence traceable to the scorecard and source ledger.**

Then add two secondaries:

* it surfaced at least one meaningful same-firm change you would likely have missed otherwise
* when stress-tested on 3 firms you know well, it avoided embarrassing misses in the core dimensions

That is measurable enough to be honest, but not fake-precise.

## Net change to the original plan

The plan is now:

* **Finland-primary**
* **structured-first**
* **longitudinal-first**
* **dimensional scorecard with lenses**
* **event overrides instead of sparse pseudo-metrics**
* **explicit plugin contract**
* **explicit success criteria**

That is a much better machine.

The next useful step is to turn this into a Phase 0 document with five concrete artifacts: source inventory, evidence schema, lens schema, plugin contract, and success criteria.

[1]: https://www.cgfinland.fi/en/securities-market-association/self-regulation/?utm_source=chatgpt.com "Self-regulation – Arvopaperimarkkinayhdistys"
[2]: https://www.cgfinland.fi/wp-content/uploads/2026/02/corporate-governance-code-2026.pdf?utm_source=chatgpt.com "CORPORATE GOVERNANCE FINNISH CORPORATE GOVERNANCE"
[3]: https://www.nasdaq.com/docs/2025/03/03/xHTML%20reporting%20to%20FIN%20OAM_revised_03_2025.pdf?utm_source=chatgpt.com "xHTML REPORTING TO OAM"
[4]: https://www.cgfinland.fi/wp-content/uploads/2024/11/corporate-governance-code-2025.pdf?utm_source=chatgpt.com "Corporate
Governance
FINNISH CORPORATE
GOVERNANCE"
[5]: https://www.cgfinland.fi/materiaalipankki/?utm_source=chatgpt.com "Materiaalipankki – Arvopaperimarkkinayhdistys"
[6]: https://www.esma.europa.eu/press-news/esma-news/esma-publishes-second-consolidated-report-sanctions?utm_source=chatgpt.com "ESMA publishes second consolidated report on sanctions"
