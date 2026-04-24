from __future__ import annotations

from typing import Any

from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.identifiers import validate_entity_identifier_record


def test_entity_identifier_validation_accepts_finnish_listed_company() -> None:
    assert validate_entity_identifier_record(_identifier_record(), SCHEMA_DIR) == []


def test_entity_identifier_validation_reports_schema_errors() -> None:
    payload = _identifier_record()
    del payload["source_aliases"]

    assert validate_entity_identifier_record(payload, SCHEMA_DIR) == [
        "entity-identifier-record.schema.json failed validation: 'source_aliases' is a required property"
    ]


def test_finnish_company_requires_business_id_or_prh_identifier() -> None:
    payload = _identifier_record(company_identifiers={"lei": "74370000000000000000"})

    assert validate_entity_identifier_record(payload, SCHEMA_DIR) == [
        "Finnish entity identifier records require business_id or prh_trade_register_number"
    ]


def test_listed_security_requires_isin_and_mic() -> None:
    payload = _identifier_record(
        security_identifiers=[
            {
                "security_id": "example-share",
                "ticker": "EXMPL",
                "market": "Nasdaq Helsinki",
                "currency": "EUR",
                "listing_status": "listed",
            }
        ]
    )

    assert validate_entity_identifier_record(payload, SCHEMA_DIR) == [
        "listed security example-share requires isin, mic"
    ]


def test_delisted_security_can_preserve_partial_identifier_history() -> None:
    payload = _identifier_record(
        security_identifiers=[
            {
                "security_id": "example-old-share",
                "ticker": "OLD",
                "listing_status": "delisted",
            }
        ]
    )

    assert validate_entity_identifier_record(payload, SCHEMA_DIR) == []


def _identifier_record(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "company_id": "example-company",
        "display_name": "Example Oyj",
        "legal_name": "Example Oyj",
        "domicile_country": "FI",
        "identifier_confidence": "high",
        "company_identifiers": {
            "business_id": "1234567-8",
            "lei": "74370000000000000000",
            "prh_trade_register_number": "123456",
        },
        "security_identifiers": [
            {
                "security_id": "example-share",
                "isin": "FI0000000000",
                "ticker": "EXMPL",
                "market": "Nasdaq Helsinki",
                "mic": "XHEL",
                "currency": "EUR",
                "listing_status": "listed",
            }
        ],
        "source_aliases": [
            {
                "source_family": "company_ir_annual_reporting",
                "source_value": "Example Oyj",
                "source_id": "source-1",
            }
        ],
        "normalization_notes": "Fixture identity mapping for schema validation.",
    }
    payload.update(overrides)
    return payload
