from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json


def validate_feature_record(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate deterministic feature records before time-series or scorecard use."""

    schema = load_json(schema_dir / "feature-record.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"feature-record.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_feature_value_type(payload))
    errors.extend(_validate_people_signal_bias(payload))
    errors.extend(_validate_period_pair(payload))
    return errors


def _validate_feature_value_type(payload: dict[str, Any]) -> list[str]:
    value_type = payload["feature_value_type"]
    value = payload["feature_value"]

    if value_type == "boolean" and not isinstance(value, bool):
        return ["boolean feature_value_type requires a boolean feature_value"]
    if value_type == "numeric" and (not isinstance(value, int | float) or isinstance(value, bool)):
        return ["numeric feature_value_type requires a numeric feature_value"]
    if value_type in {"categorical", "text", "date"} and not isinstance(value, str):
        return [f"{value_type} feature_value_type requires a string feature_value"]
    return []


def _validate_people_signal_bias(payload: dict[str, Any]) -> list[str]:
    if payload["feature_family"] == "people_signal_aux" and not payload["bias_flags"]:
        return ["people_signal_aux feature records require at least one bias flag"]
    return []


def _validate_period_pair(payload: dict[str, Any]) -> list[str]:
    has_period_start = "period_start" in payload
    has_period_end = "period_end" in payload
    if has_period_start != has_period_end:
        return ["period_start and period_end must be provided together"]
    return []
