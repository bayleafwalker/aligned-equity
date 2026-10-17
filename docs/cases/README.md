# Bounded Finland-first research cases

These cases exercise the source-ledger, evidence, feature and decision-output
contracts on a deliberately narrow Finnish issuer question. They are manually
researched examples, not live feeds, personalized recommendations, accepted
investment decisions, or evidence of realized decision impact.

## Nokia issuer identity and source-adequacy sample

The [case bundle](../../cases/finland/nokia-prh-issuer-record-2026-10-17.json)
records a manually retrieved PRH YTJ Open Data API response, its SHA-256, a
normalized Nokia entity, registered main-business-line feature, evidence links,
the CC BY 4.0 reuse posture, comparability caveats and an explicit
insufficient-evidence research disposition. It contains selected registry
fields, attributes PRH and includes no PRH logo. Linked company documents have
not been copied or treated as licensed sources.

Render the case view from the repository root after installing the project:

```sh
uv run --project . python -m apps.research_case \
  cases/finland/nokia-prh-issuer-record-2026-10-17.json
```

The renderer validates identity, source, evidence, feature and decision
contracts before producing Markdown. The bundle and validator work offline;
they do not fetch source documents at runtime. The source URLs and SHA-256
digests identify the documents manually reviewed when the bundle was prepared.

The sample's watch state is only an example research disposition for the
bounded question. It is not a user portfolio state. The registry classification
does not establish Nokia's consolidated business mix. No investor action,
change in decision, or later outcome was supplied, so the sample makes no
decision-impact claim.
