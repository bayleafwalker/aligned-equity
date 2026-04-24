from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json


def validate_entity_identifier_record(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate normalized company, security, and source alias identifiers."""

    schema = load_json(schema_dir / "entity-identifier-record.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"entity-identifier-record.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_finnish_company_identifiers(payload))
    errors.extend(_validate_listed_security_identifiers(payload))
    return errors


def _validate_finnish_company_identifiers(payload: dict[str, Any]) -> list[str]:
    if payload["domicile_country"].lower() not in {"fi", "finland"}:
        return []

    company_identifiers = payload["company_identifiers"]
    if company_identifiers.get("business_id") or company_identifiers.get(
        "prh_trade_register_number"
    ):
        return []
    return ["Finnish entity identifier records require business_id or prh_trade_register_number"]


def _validate_listed_security_identifiers(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for security in payload.get("security_identifiers", []):
        if security["listing_status"] != "listed":
            continue
        missing = [field for field in ("isin", "mic") if not security.get(field)]
        if missing:
            errors.append(
                f"listed security {security['security_id']} requires {', '.join(missing)}"
            )
    return errors
