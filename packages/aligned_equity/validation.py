from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.contracts import (
    ACCOUNTING_SCOPE_VALUES,
    COMPARABILITY_LEVELS,
    CONFIDENCE_LEVELS,
    DECISION_CONTEXTS,
    EVIDENCE_CLASSES,
    FEATURE_EXTRACTION_METHODS,
    FEATURE_FAMILIES,
    FEATURE_VALUE_TYPES,
    LENS_KEYS,
    PERIOD_ALIGNMENT_VALUES,
    RESEARCH_STATES,
    RESTATEMENT_STATUS_VALUES,
    SCHEMA_DIR,
    SCORECARD_ASSESSMENTS,
    SCORECARD_DIMENSIONS,
    SOURCE_EXTRACTION_READINESS,
    SOURCE_FAMILIES,
    SOURCE_FRESHNESS_STATUSES,
    SOURCE_RETRIEVAL_METHODS,
    SOURCE_UPDATE_FREQUENCIES,
    VALUE_OF_INFORMATION_ASSESSMENTS,
)

REQUIRED_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    ".gitignore",
    ".envrc",
    ".env.example",
    "pyproject.toml",
    "pytest.ini",
    "Makefile",
    "homelab-analytics.registry.json",
    ".github/workflows/verify.yaml",
)

REQUIRED_DOCS = (
    "docs/README.md",
    "docs/operational-shape.md",
    "docs/soft-leadership-factors.md",
    "docs/research-notes.md",
    "docs/product/vision.md",
    "docs/product/six-month-success-criteria.md",
    "docs/architecture/evidence-model.md",
    "docs/architecture/lens-model.md",
    "docs/architecture/homelab-analytics-platform-contract.md",
    "docs/specifications/finland-source-inventory.md",
    "docs/specifications/phase-1-source-fixture-boundaries.md",
    "docs/specifications/source-ledger-record-spec.md",
    "docs/specifications/entity-identifier-normalization.md",
    "docs/specifications/evidence-record-spec.md",
    "docs/specifications/feature-record-spec.md",
    "docs/specifications/time-series-view-contract.md",
    "docs/specifications/reporting-style-change-detection.md",
    "docs/specifications/remuneration-logic-extraction.md",
    "docs/specifications/scorecard-run-spec.md",
    "docs/specifications/lens-output-contract.md",
    "docs/specifications/lens-scorecard-spec.md",
    "docs/specifications/decision-output-contract.md",
    "docs/specifications/hla-publication-contract-spike.md",
    "docs/agents/planning.md",
    "docs/agents/implementation.md",
    "docs/agents/review.md",
    "docs/agents/release-ops.md",
    "docs/plans/phase-0-roadmap.md",
    "docs/runbooks/project-working-practices.md",
    "docs/runbooks/sprint-and-knowledge-operations.md",
    "docs/knowledge/README.md",
    "docs/knowledge/knowledge-base.md",
    "docs/sprint-snapshots/README.md",
)


def validate_repository(repo_root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_required_paths(repo_root))
    errors.extend(_validate_docs_index(repo_root))
    errors.extend(_validate_research_deduplication(repo_root))
    errors.extend(_validate_envrc(repo_root))
    errors.extend(_validate_registry_manifest(repo_root))
    errors.extend(_validate_schemas(repo_root))
    errors.extend(_validate_hla_hooks())
    return errors


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_required_paths(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in (*REQUIRED_ROOT_FILES, *REQUIRED_DOCS):
        if not (repo_root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")
    return errors


def _validate_docs_index(repo_root: Path) -> list[str]:
    index = (repo_root / "docs/README.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for relative_path in REQUIRED_DOCS:
        if relative_path == "docs/README.md":
            continue
        docs_relative = relative_path.removeprefix("docs/")
        if docs_relative not in index:
            errors.append(f"docs/README.md does not index {relative_path}")
    return errors


def _validate_research_deduplication(repo_root: Path) -> list[str]:
    canonical = repo_root / "docs/soft-leadership-factors.md"
    pointer = repo_root / "docs/research-notes.md"
    errors: list[str] = []
    if _sha256(canonical) == _sha256(pointer):
        errors.append("docs/research-notes.md still duplicates docs/soft-leadership-factors.md")
    pointer_text = pointer.read_text(encoding="utf-8")
    if "soft-leadership-factors.md" not in pointer_text:
        errors.append("docs/research-notes.md must point to the canonical research document")
    return errors


def _validate_envrc(repo_root: Path) -> list[str]:
    text = (repo_root / ".envrc").read_text(encoding="utf-8")
    expected = (
        'export SPRINTCTL_DB="${PWD}/.sprintctl/sprintctl.db"',
        'export KCTL_DB="${PWD}/.kctl/kctl.db"',
        'export KCTL_PROJECT="aligned-equity"',
    )
    return [f".envrc missing {value}" for value in expected if value not in text]


def _validate_registry_manifest(repo_root: Path) -> list[str]:
    manifest = load_json(repo_root / "homelab-analytics.registry.json")
    expected = {
        "schema_version": 1,
        "import_paths": ["."],
        "extension_modules": ["aligned_equity.integrations.homelab_analytics"],
        "function_modules": [],
        "minimum_platform_version": "0.1.0",
    }
    errors: list[str] = []
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"homelab-analytics.registry.json has unexpected {key!r}")
    return errors


def _validate_schemas(repo_root: Path) -> list[str]:
    examples = (
        ("evidence-class.schema.json", {"evidence_class": EVIDENCE_CLASSES[0]}),
        (
            "entity-identifier-record.schema.json",
            {
                "company_id": "example-company",
                "display_name": "Example Oyj",
                "domicile_country": "FI",
                "identifier_confidence": CONFIDENCE_LEVELS[0],
                "company_identifiers": {"business_id": "1234567-8"},
                "security_identifiers": [
                    {
                        "security_id": "example-share",
                        "isin": "FI0000000000",
                        "ticker": "EXMPL",
                        "market": "Nasdaq Helsinki",
                        "mic": "XHEL",
                        "currency": "EUR",
                        "listing_status": "listed",
                    }
                ],
                "source_aliases": [
                    {
                        "source_family": SOURCE_FAMILIES[0],
                        "source_value": "Example Oyj",
                        "source_id": "source-1",
                    }
                ],
                "normalization_notes": "Manual smoke-test identity mapping.",
            },
        ),
        (
            "source-ledger-record.schema.json",
            {
                "source_id": "source-1",
                "source_family": SOURCE_FAMILIES[0],
                "source_name": "Example annual report",
                "source_locator": "https://example.test/report",
                "publisher": "Example Oyj",
                "retrieval_method": SOURCE_RETRIEVAL_METHODS[0],
                "collected_at": "2026-04-24T12:00:00Z",
                "observed_at": "2026-04-24",
                "freshness_as_of": "2026-04-24",
                "expected_update_frequency": SOURCE_UPDATE_FREQUENCIES[0],
                "freshness_status": SOURCE_FRESHNESS_STATUSES[0],
                "language": "en",
                "source_confidence": CONFIDENCE_LEVELS[0],
                "extraction_readiness": SOURCE_EXTRACTION_READINESS[0],
                "same_firm_comparable": COMPARABILITY_LEVELS[1],
                "cross_firm_comparable": COMPARABILITY_LEVELS[2],
                "comparability_notes": "Cross-firm comparison is not used.",
                "bias_flags": [],
            },
        ),
        (
            "evidence-record.schema.json",
            {
                "evidence_id": "evidence-1",
                "company_id": "example-company",
                "source_id": "source-1",
                "source_family": SOURCE_FAMILIES[0],
                "evidence_class": EVIDENCE_CLASSES[0],
                "document_type": "annual report",
                "observed_at": "2026-04-24",
                "collected_at": "2026-04-24T12:00:00Z",
                "source_locator": "https://example.test/report",
                "language": "en",
                "extraction_method": "manual",
                "source_confidence": CONFIDENCE_LEVELS[0],
                "extraction_confidence": CONFIDENCE_LEVELS[0],
                "interpretation_confidence": CONFIDENCE_LEVELS[1],
                "confidence_notes": "Manual smoke-test payload.",
                "same_firm_comparable": COMPARABILITY_LEVELS[1],
                "cross_firm_comparable": COMPARABILITY_LEVELS[2],
                "period_alignment": PERIOD_ALIGNMENT_VALUES[2],
                "accounting_scope": ACCOUNTING_SCOPE_VALUES[4],
                "restatement_status": RESTATEMENT_STATUS_VALUES[4],
                "comparability_notes": "Cross-firm comparison is not used.",
                "bias_flags": [],
                "legal_or_enforcement_override": False,
            },
        ),
        (
            "feature-record.schema.json",
            {
                "feature_id": "feature-1",
                "company_id": "example-company",
                "feature_key": "board_independence_ratio",
                "feature_family": FEATURE_FAMILIES[0],
                "feature_value_type": FEATURE_VALUE_TYPES[2],
                "feature_value": 0.75,
                "feature_unit": "ratio",
                "observed_at": "2026-04-24",
                "period_start": "2025-01-01",
                "period_end": "2025-12-31",
                "extracted_at": "2026-04-24T12:30:00Z",
                "source_evidence_ids": ["evidence-1"],
                "source_ids": ["source-1"],
                "extraction_rule_id": "board_independence_ratio",
                "extraction_rule_version": "1",
                "extraction_method": FEATURE_EXTRACTION_METHODS[0],
                "source_confidence": CONFIDENCE_LEVELS[0],
                "extraction_confidence": CONFIDENCE_LEVELS[0],
                "interpretation_confidence": CONFIDENCE_LEVELS[1],
                "confidence_notes": "Manual smoke-test feature payload.",
                "same_firm_comparable": COMPARABILITY_LEVELS[0],
                "cross_firm_comparable": COMPARABILITY_LEVELS[1],
                "period_alignment": PERIOD_ALIGNMENT_VALUES[0],
                "accounting_scope": ACCOUNTING_SCOPE_VALUES[1],
                "restatement_status": RESTATEMENT_STATUS_VALUES[0],
                "comparability_notes": "Same-firm comparison is valid for the fixture period.",
                "bias_flags": [],
            },
        ),
        ("lens.schema.json", {"lens_key": LENS_KEYS[0]}),
        (
            "lens-output.schema.json",
            {
                "lens_output_id": "lens-output-1",
                "scorecard_run_id": "scorecard-1",
                "company_id": "example-company",
                "analysis_date": "2026-04-25",
                "lens_key": LENS_KEYS[0],
                "decision_context": DECISION_CONTEXTS[0],
                "dimension_emphasis": [SCORECARD_DIMENSIONS[0]],
                "material_scorecard_dimensions": [SCORECARD_DIMENSIONS[0]],
                "material_evidence_ids": ["evidence-1"],
                "material_feature_ids": ["feature-1"],
                "time_series_ids": ["series-1"],
                "confidence_summary": "Confidence is medium.",
                "comparability_summary": "Same-firm comparison is partial.",
                "lens_rationale": "The lens emphasizes governance for the decision context.",
                "allowed_output_uses": ["decision_memo"],
            },
        ),
        ("research-state.schema.json", {"research_state": RESEARCH_STATES[0]}),
        (
            "scorecard-run.schema.json",
            {
                "scorecard_run_id": "scorecard-1",
                "company_id": "example-company",
                "analysis_date": "2026-04-25",
                "dimension_assessments": [
                    {
                        "dimension": SCORECARD_DIMENSIONS[0],
                        "assessment": SCORECARD_ASSESSMENTS[2],
                        "rationale": "Primary evidence and feature lineage support a neutral assessment.",
                        "evidence_ids": ["evidence-1"],
                        "feature_ids": ["feature-1"],
                        "time_series_ids": ["series-1"],
                        "confidence": CONFIDENCE_LEVELS[1],
                        "comparability_notes": "Same-firm comparison is partial.",
                    }
                ],
                "material_evidence_ids": ["evidence-1"],
                "material_feature_ids": ["feature-1"],
                "time_series_ids": ["series-1"],
                "source_ids": ["source-1"],
                "confidence_summary": "Source confidence is medium.",
                "comparability_summary": "Same-firm comparison is partial.",
                "source_freshness_summary": "Source freshness is current.",
                "scorecard_notes": "Smoke-test scorecard payload.",
            },
        ),
        (
            "decision-output.schema.json",
            {
                "company_id": "example-company",
                "analysis_date": "2026-04-24",
                "decision_context": DECISION_CONTEXTS[0],
                "current_research_state": RESEARCH_STATES[2],
                "material_evidence_ids": ["evidence-1"],
                "scorecard_dimension_assessments": [
                    {
                        "dimension": "governance and accountability",
                        "assessment": "neutral",
                        "rationale": "Evidence is relevant to the decision context.",
                        "evidence_ids": ["evidence-1"],
                    }
                ],
                "confidence_summary": "Source confidence is medium.",
                "comparability_summary": "Same-firm comparison is partial.",
                "likely_action_implication": "Preserve watch status.",
                "value_of_information_assessment": VALUE_OF_INFORMATION_ASSESSMENTS[0],
                "value_of_information_note": "More primary evidence could change follow-up scope.",
                "causal_claim": {"claim_type": "decision_relevance"},
            },
        ),
    )
    errors: list[str] = []
    for schema_name, payload in examples:
        schema_path = repo_root / "schemas" / schema_name
        try:
            jsonschema.validate(payload, load_json(schema_path))
        except Exception as exc:
            errors.append(f"{schema_name} failed validation smoke test: {exc}")
    if SCHEMA_DIR.name != "schemas":
        errors.append("schema directory constant is misconfigured")
    return errors


def _validate_hla_hooks() -> list[str]:
    module = importlib.import_module("aligned_equity.integrations.homelab_analytics")
    errors: list[str] = []
    for hook_name in (
        "register_extensions",
        "register_pipeline_registries",
        "register_functions",
        "register_capability_packs",
    ):
        if not callable(getattr(module, hook_name, None)):
            errors.append(f"HLA integration hook is missing or not callable: {hook_name}")
    return errors


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
