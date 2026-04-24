from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json


def validate_source_ledger_record(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate normalized source-ledger records before evidence extraction."""

    schema = load_json(schema_dir / "source-ledger-record.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"source-ledger-record.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_people_platform_bias(payload))
    errors.extend(_validate_extraction_linkage(payload))
    return errors


def _validate_people_platform_bias(payload: dict[str, Any]) -> list[str]:
    if payload["source_family"] == "people_platforms" and not payload["bias_flags"]:
        return ["people_platforms source-ledger records require at least one bias flag"]
    return []


def _validate_extraction_linkage(payload: dict[str, Any]) -> list[str]:
    if payload["extraction_readiness"] == "not-ready" and payload.get("derived_evidence_ids"):
        return ["not-ready source-ledger records cannot have derived_evidence_ids"]
    return []
