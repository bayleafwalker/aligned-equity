from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.contracts import EVIDENCE_CLASSES, LENS_KEYS, RESEARCH_STATES, SCHEMA_DIR

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
    "docs/architecture/evidence-model.md",
    "docs/architecture/lens-model.md",
    "docs/architecture/homelab-analytics-platform-contract.md",
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
        ("lens.schema.json", {"lens_key": LENS_KEYS[0]}),
        ("research-state.schema.json", {"research_state": RESEARCH_STATES[0]}),
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
