# aligned-equity

Aligned Equity is a Finland-first evidence and lens research platform for public-company alignment analysis.

The repository starts as a standalone Python/data project. Its core stays independently installable, while the optional homelab-analytics boundary is documented and validated through a small external-registry contract.

## Current status

Phase 0 is initialized:

- Finland-first evidence model and source vocabulary
- dimensional scorecard with investment, workplace, and product lenses
- research-state vocabulary for watchlist and thesis movement
- homelab-analytics registry manifest and no-op integration hooks
- repository verification through `ruff`, `mypy`, `pytest`, and schema validation

## Quick Start

```bash
uv sync --dev
make verify-fast
source .envrc
```

Run individual checks:

```bash
make lint
make typecheck
make test
make validate
make hla-contract-check
```

`make hla-contract-check` validates the local registry manifest against the sibling homelab-analytics loader when `/projects/dev/homelab-analytics` is available. It exits successfully with a clear skip message when that repository is not present.

## Repository Layout

```text
.
├── apps/
│   └── validator/              # Local repository and HLA contract validation
├── docs/
│   ├── architecture/           # Evidence, lens, and platform contract docs
│   ├── knowledge/              # Rendered durable knowledge artifact
│   ├── plans/                  # Phase plans
│   ├── product/                # Product framing
│   ├── runbooks/               # Working practices
│   └── sprint-snapshots/       # Rendered sprint state artifacts
├── packages/
│   └── aligned_equity/         # Core Python package
├── schemas/                    # Public vocabulary schemas
└── tests/                      # Repository, schema, and contract tests
```

## Documentation

- `docs/README.md` - documentation index
- `docs/operational-shape.md` - seed operating model and roadmap notes
- `docs/soft-leadership-factors.md` - canonical soft-factor research note
- `docs/architecture/evidence-model.md` - evidence class vocabulary and source model
- `docs/architecture/lens-model.md` - dimensional scorecard and lens model
- `docs/architecture/homelab-analytics-platform-contract.md` - optional HLA boundary
- `docs/plans/phase-0-roadmap.md` - initialization-to-first-sprint roadmap

## Homelab-Analytics Boundary

The root `homelab-analytics.registry.json` is intentionally present from initialization. It declares `aligned_equity.integrations.homelab_analytics` as an external module and reserves future publication keys, but it does not activate real HLA publications yet.

Future HLA-facing work must keep the landing, transformation, and reporting layers explicit and publish app-facing data through declared publication relations.
