from __future__ import annotations

import hashlib
from pathlib import Path

from aligned_equity.validation import REQUIRED_DOCS, REQUIRED_ROOT_FILES, validate_repository

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repository_contract_validation_passes() -> None:
    assert validate_repository(REPO_ROOT) == []


def test_required_root_files_exist() -> None:
    missing = [path for path in REQUIRED_ROOT_FILES if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_docs_index_includes_durable_docs() -> None:
    index = (REPO_ROOT / "docs/README.md").read_text(encoding="utf-8")
    missing = [
        path.removeprefix("docs/")
        for path in REQUIRED_DOCS
        if path != "docs/README.md" and path.removeprefix("docs/") not in index
    ]
    assert missing == []


def test_research_notes_are_not_byte_duplicate() -> None:
    canonical = REPO_ROOT / "docs/soft-leadership-factors.md"
    pointer = REPO_ROOT / "docs/research-notes.md"
    assert _sha256(canonical) != _sha256(pointer)
    assert "soft-leadership-factors.md" in pointer.read_text(encoding="utf-8")


def test_envrc_uses_repo_local_state() -> None:
    text = (REPO_ROOT / ".envrc").read_text(encoding="utf-8")
    assert 'export SPRINTCTL_DB="${PWD}/.sprintctl/sprintctl.db"' in text
    assert 'export KCTL_DB="${PWD}/.kctl/kctl.db"' in text
    assert 'export KCTL_PROJECT="aligned-equity"' in text


def test_phase_0_specs_capture_required_contract_fields() -> None:
    evidence = (REPO_ROOT / "docs/specifications/evidence-record-spec.md").read_text(
        encoding="utf-8"
    )
    lens = (REPO_ROOT / "docs/specifications/lens-scorecard-spec.md").read_text(
        encoding="utf-8"
    )
    source_inventory = (
        REPO_ROOT / "docs/specifications/finland-source-inventory.md"
    ).read_text(encoding="utf-8")
    hla_spike = (
        REPO_ROOT / "docs/specifications/hla-publication-contract-spike.md"
    ).read_text(encoding="utf-8")
    decision_output = (
        REPO_ROOT / "docs/specifications/decision-output-contract.md"
    ).read_text(encoding="utf-8")

    for field in (
        "source_confidence",
        "extraction_confidence",
        "interpretation_confidence",
        "same_firm_comparable",
        "cross_firm_comparable",
        "bias_flags",
    ):
        assert field in evidence

    assert "Allowed transitions" in lens
    assert "event override" in lens
    assert "people-platform" in source_inventory
    assert "not a primary scored axis" in source_inventory
    assert "Aligned Equity does not import HLA" in hla_spike
    assert "value_of_information_assessment" in decision_output
    assert "causal_design" in decision_output
    assert "numeric predictive" in decision_output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
