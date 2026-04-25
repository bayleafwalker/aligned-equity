# Homelab-Analytics Platform Contract

Aligned Equity is initialized as a standalone repository with an optional homelab-analytics integration boundary.

The Phase 0 publication spike lives in `docs/specifications/hla-publication-contract-spike.md`.

## Current contract

The root `homelab-analytics.registry.json` declares:

- `schema_version: 1`
- `import_paths: ["."]`
- `extension_modules: ["aligned_equity.integrations.homelab_analytics"]`
- `function_modules: []`
- `minimum_platform_version: "0.1.0"`

The integration module exposes import-safe no-op hooks:

- `register_extensions(registry)`
- `register_pipeline_registries(...)`
- `register_functions(registry)`
- `register_capability_packs(registry)`

This lets homelab-analytics validate the repository as an external source without making HLA a core dependency of Aligned Equity.

## Reserved future publication keys

- `aligned_equity_company_evidence`
- `aligned_equity_scorecard`
- `aligned_equity_research_state`
- `aligned_equity_source_freshness`
- `aligned_equity_feature_record`
- `aligned_equity_time_series_view`
- `aligned_equity_decision_memo`

These keys are reserved for future HLA-backed publications. They must not be used for unrelated outputs.

## Dependency notes from homelab-analytics

- External repositories load through `homelab-analytics.registry.json`.
- External code registers through landing, transformation, reporting, application, function, pipeline, or capability-pack registries.
- Pack-owned publications require complete semantic field metadata.
- Duplicate publication keys are rejected during validation.
- App-facing consumers must read published reporting relations, not warehouse internals.
- The HLA platform expects landing, transformation, and reporting boundaries to remain explicit.

## Future implementation rule

When real HLA publications are added, add contract tests that validate the extension against the sibling homelab-analytics loader and verify that publication field semantics cover every exported column.
