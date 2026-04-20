from __future__ import annotations

import importlib
import json
from pathlib import Path

from aligned_equity.contracts import FUTURE_HLA_PUBLICATION_KEYS

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_hla_registry_manifest_shape() -> None:
    manifest = json.loads(
        (REPO_ROOT / "homelab-analytics.registry.json").read_text(encoding="utf-8")
    )
    assert manifest["schema_version"] == 1
    assert manifest["import_paths"] == ["."]
    assert manifest["extension_modules"] == ["aligned_equity.integrations.homelab_analytics"]
    assert manifest["function_modules"] == []
    assert manifest["minimum_platform_version"] == "0.1.0"


def test_hla_integration_module_is_import_safe() -> None:
    module = importlib.import_module("aligned_equity.integrations.homelab_analytics")
    for hook_name in (
        "register_extensions",
        "register_pipeline_registries",
        "register_functions",
        "register_capability_packs",
    ):
        assert callable(getattr(module, hook_name))


def test_future_hla_publication_keys_are_reserved_in_docs() -> None:
    text = (REPO_ROOT / "docs/architecture/homelab-analytics-platform-contract.md").read_text(
        encoding="utf-8"
    )
    for publication_key in FUTURE_HLA_PUBLICATION_KEYS:
        assert publication_key in text
