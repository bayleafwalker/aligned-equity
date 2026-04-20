from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
from aligned_equity.contracts import EVIDENCE_CLASSES, LENS_KEYS, RESEARCH_STATES

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("evidence_class", EVIDENCE_CLASSES)
def test_evidence_class_schema_accepts_allowed_values(evidence_class: str) -> None:
    schema = _schema("evidence-class.schema.json")
    jsonschema.validate({"evidence_class": evidence_class}, schema)


def test_evidence_class_schema_rejects_unknown_value() -> None:
    schema = _schema("evidence-class.schema.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"evidence_class": "proxy_statement"}, schema)


@pytest.mark.parametrize("lens_key", LENS_KEYS)
def test_lens_schema_accepts_allowed_values(lens_key: str) -> None:
    schema = _schema("lens.schema.json")
    jsonschema.validate({"lens_key": lens_key}, schema)


def test_lens_schema_rejects_unknown_value() -> None:
    schema = _schema("lens.schema.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"lens_key": "supplier"}, schema)


@pytest.mark.parametrize("research_state", RESEARCH_STATES)
def test_research_state_schema_accepts_allowed_values(research_state: str) -> None:
    schema = _schema("research-state.schema.json")
    jsonschema.validate({"research_state": research_state}, schema)


def test_research_state_schema_rejects_unknown_value() -> None:
    schema = _schema("research-state.schema.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"research_state": "buy_now"}, schema)


def _schema(name: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / "schemas" / name).read_text(encoding="utf-8"))
