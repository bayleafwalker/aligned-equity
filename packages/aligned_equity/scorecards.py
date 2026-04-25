from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json


def validate_scorecard_run(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate scorecard runs before lens output or state-transition use."""

    schema = load_json(schema_dir / "scorecard-run.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"scorecard-run.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_dimension_uniqueness(payload))
    errors.extend(_validate_dimension_links_are_material(payload))
    errors.extend(_validate_insufficient_evidence_notes(payload))
    return errors


def _validate_dimension_uniqueness(payload: dict[str, Any]) -> list[str]:
    dimensions = [
        assessment["dimension"] for assessment in payload["dimension_assessments"]
    ]
    if len(dimensions) != len(set(dimensions)):
        return ["scorecard dimension_assessments must not repeat a dimension"]
    return []


def _validate_dimension_links_are_material(payload: dict[str, Any]) -> list[str]:
    material_evidence_ids = set(payload["material_evidence_ids"])
    material_feature_ids = set(payload["material_feature_ids"])
    material_time_series_ids = set(payload["time_series_ids"])
    errors: list[str] = []

    for index, assessment in enumerate(payload["dimension_assessments"]):
        unknown_evidence_ids = set(assessment["evidence_ids"]) - material_evidence_ids
        unknown_feature_ids = set(assessment["feature_ids"]) - material_feature_ids
        unknown_time_series_ids = (
            set(assessment["time_series_ids"]) - material_time_series_ids
        )
        if unknown_evidence_ids:
            errors.append(
                f"dimension_assessments[{index}] evidence_ids must be material to the scorecard run"
            )
        if unknown_feature_ids:
            errors.append(
                f"dimension_assessments[{index}] feature_ids must be material to the scorecard run"
            )
        if unknown_time_series_ids:
            errors.append(
                f"dimension_assessments[{index}] time_series_ids must be material to the scorecard run"
            )
    return errors


def _validate_insufficient_evidence_notes(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for index, assessment in enumerate(payload["dimension_assessments"]):
        if assessment["assessment"] != "insufficient_evidence":
            continue
        linked_material = (
            assessment["evidence_ids"]
            or assessment["feature_ids"]
            or assessment["time_series_ids"]
        )
        if linked_material:
            continue
        if "insufficient" not in assessment["rationale"].lower():
            errors.append(
                f"dimension_assessments[{index}] insufficient_evidence requires rationale explaining the evidence gap"
            )
    return errors
