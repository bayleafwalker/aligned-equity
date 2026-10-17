from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.research_case import (
    build_research_case_packet,
    render_research_case_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = REPO_ROOT / "cases/finland/nokia-prh-issuer-record-2026-10-17.json"


def _case_bundle() -> dict[str, Any]:
    return json.loads(CASE_PATH.read_text(encoding="utf-8"))


def test_nokia_finland_case_validates_and_preserves_source_lineage() -> None:
    packet, errors = build_research_case_packet(_case_bundle(), SCHEMA_DIR)

    assert errors == []
    assert packet["decision_output"]["current_research_state"] == "watch"
    assert packet["decision_output"]["value_of_information_assessment"] == "collect_more_evidence"
    assert len(packet["feature_records"]) == 1
    assert packet["feature_records"][0]["feature_key"] == "prh_registered_main_business_line_code"
    assert packet["feature_records"][0]["feature_value"] == "70100"
    assert packet["source_ledger_records"][0]["reuse_posture"] == "reproduction-authorized"
    assert packet["source_ledger_records"][0]["reuse_license_locator"].endswith("/by/4.0/")


def test_nokia_case_view_shows_caveats_and_decision_impact_gap() -> None:
    packet, errors = build_research_case_packet(_case_bundle(), SCHEMA_DIR)
    assert errors == []

    markdown = render_research_case_markdown(packet)

    assert "Activities of head offices" in markdown
    assert "PRH Open Data YTJ API v3" in markdown
    assert "insufficient_evidence" in markdown
    assert "**Decision impact:** Not measured" in markdown
    assert "CC BY 4.0" in markdown


def test_research_case_requires_explicit_source_reuse_posture() -> None:
    bundle = _case_bundle()
    bundle["source_ledger_records"][0].pop("reuse_posture")

    packet, errors = build_research_case_packet(bundle, SCHEMA_DIR)

    assert packet == {}
    assert any("requires an explicit reuse_posture" in error for error in errors)


def test_reproduction_authorized_source_requires_license_and_attribution() -> None:
    bundle = _case_bundle()
    source = bundle["source_ledger_records"][0]
    source.pop("reuse_license_locator")

    packet, errors = build_research_case_packet(bundle, SCHEMA_DIR)

    assert packet == {}
    assert any("without reuse_license_locator" in error for error in errors)


def test_research_case_rejects_orphaned_feature_evidence() -> None:
    bundle = copy.deepcopy(_case_bundle())
    bundle["feature_records"][0]["source_evidence_ids"] = ["missing-evidence"]

    packet, errors = build_research_case_packet(bundle, SCHEMA_DIR)

    assert packet == {}
    assert any("references unknown evidence" in error for error in errors)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda bundle: bundle.update(case=None), "case must be an object"),
        (lambda bundle: bundle.update(case=[]), "case must be an object"),
        (lambda bundle: bundle["case"].pop("status"), "case.status must be a non-empty string"),
        (lambda bundle: bundle["case"].update(observations=[None]), "observations[0] must be an object"),
        (lambda bundle: bundle["case"].update(gaps=[{"claim": "x"}]), "case.gaps must be an array of strings"),
        (lambda bundle: bundle["case"].update(decision_parameters=[]), "decision_parameters must be an object"),
        (
            lambda bundle: bundle["case"]["decision_parameters"].update(unexpected="x"),
            "decision_parameters has unsupported fields",
        ),
        (
            lambda bundle: bundle["case"]["decision_parameters"].update(analysis_date=None),
            "decision_parameters.analysis_date must be a string",
        ),
    ],
)
def test_research_case_rejects_malformed_case_contract_before_rendering(
    mutate: Any, message: str
) -> None:
    bundle = copy.deepcopy(_case_bundle())
    mutate(bundle)

    packet, errors = build_research_case_packet(bundle, SCHEMA_DIR)

    assert packet == {}
    assert any(message in error for error in errors)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("source_ledger_records", ["not-an-object"], "source_ledger_records[0] must be an object"),
        ("evidence_records", [None], "evidence_records[0] must be an object"),
        ("feature_records", [7], "feature_records[0] must be an object"),
    ],
)
def test_research_case_rejects_scalar_records_before_schema_validation(
    field: str, value: list[Any], message: str
) -> None:
    bundle = copy.deepcopy(_case_bundle())
    bundle[field] = value

    packet, errors = build_research_case_packet(bundle, SCHEMA_DIR)

    assert packet == {}
    assert message in errors


@pytest.mark.parametrize("value", [None, [], "not-an-object"])
def test_research_case_rejects_non_object_bundle(value: Any) -> None:
    packet, errors = build_research_case_packet(value, SCHEMA_DIR)  # type: ignore[arg-type]

    assert packet == {}
    assert errors == ["research case bundle must be an object"]
