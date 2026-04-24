from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json

CAUSAL_LANGUAGE_PATTERN = re.compile(
    r"\b(caus(?:e|ed|es|ing|al)|driv(?:e|es|en|ing)|lead(?:s|ing)? to|"
    r"result(?:s|ed|ing)? in|because of)\b",
    re.IGNORECASE,
)


def validate_decision_output(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate a decision memo payload against contract and causal-claim guardrails."""

    errors: list[str] = []
    schema = load_json(schema_dir / "decision-output.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"decision-output.schema.json failed validation: {exc.message}"]

    errors.extend(_validate_material_evidence_links(payload))
    errors.extend(_validate_causal_language(payload))
    return errors


def _validate_material_evidence_links(payload: dict[str, Any]) -> list[str]:
    material_evidence_ids = set(payload["material_evidence_ids"])
    errors: list[str] = []
    for assessment in payload["scorecard_dimension_assessments"]:
        assessment_evidence = set(assessment["evidence_ids"])
        missing = sorted(assessment_evidence - material_evidence_ids)
        if missing:
            dimension = assessment["dimension"]
            errors.append(
                f"dimension assessment {dimension!r} references evidence outside "
                f"material_evidence_ids: {missing}"
            )
    return errors


def _validate_causal_language(payload: dict[str, Any]) -> list[str]:
    causal_claim = payload["causal_claim"]
    if causal_claim["claim_type"] == "causal_effect" and causal_claim.get("causal_design"):
        return []

    text_fields = [
        ("likely_action_implication", payload["likely_action_implication"]),
        ("value_of_information_note", payload["value_of_information_note"]),
    ]
    text_fields.extend(
        (f"scorecard_dimension_assessments[{index}].rationale", assessment["rationale"])
        for index, assessment in enumerate(payload["scorecard_dimension_assessments"])
    )

    errors: list[str] = []
    for field_name, text in text_fields:
        if CAUSAL_LANGUAGE_PATTERN.search(text):
            errors.append(
                f"{field_name} uses causal language without causal_effect claim type "
                "and causal_design metadata"
            )
    return errors
