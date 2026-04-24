from __future__ import annotations

from typing import Any

from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.source_ledger import validate_source_ledger_record


def test_source_ledger_validation_accepts_core_source() -> None:
    assert validate_source_ledger_record(_source_ledger_record(), SCHEMA_DIR) == []


def test_source_ledger_validation_reports_schema_errors() -> None:
    payload = _source_ledger_record()
    del payload["freshness_status"]

    assert validate_source_ledger_record(payload, SCHEMA_DIR) == [
        "source-ledger-record.schema.json failed validation: 'freshness_status' is a required property"
    ]


def test_people_platform_source_requires_bias_flags() -> None:
    payload = _source_ledger_record(
        source_family="people_platforms",
        source_confidence="low",
        bias_flags=[],
    )

    assert validate_source_ledger_record(payload, SCHEMA_DIR) == [
        "people_platforms source-ledger records require at least one bias flag"
    ]


def test_people_platform_source_accepts_bias_flags() -> None:
    payload = _source_ledger_record(
        source_family="people_platforms",
        source_confidence="low",
        bias_flags=["self-selection bias", "platform coverage bias"],
    )

    assert validate_source_ledger_record(payload, SCHEMA_DIR) == []


def test_not_ready_source_cannot_link_derived_evidence() -> None:
    payload = _source_ledger_record(
        extraction_readiness="not-ready",
        derived_evidence_ids=["evidence-1"],
    )

    assert validate_source_ledger_record(payload, SCHEMA_DIR) == [
        "not-ready source-ledger records cannot have derived_evidence_ids"
    ]


def _source_ledger_record(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source_id": "source-1",
        "source_family": "company_ir_annual_reporting",
        "source_name": "Example annual report",
        "source_locator": "https://example.test/report",
        "publisher": "Example Oyj",
        "retrieval_method": "manual",
        "collected_at": "2026-04-24T12:00:00Z",
        "observed_at": "2026-04-24",
        "freshness_as_of": "2026-04-24",
        "expected_update_frequency": "annual",
        "freshness_status": "current",
        "language": "en",
        "source_confidence": "high",
        "extraction_readiness": "ready",
        "same_firm_comparable": "partial",
        "cross_firm_comparable": "no",
        "comparability_notes": "Cross-firm comparison is not used.",
        "bias_flags": [],
    }
    payload.update(overrides)
    return payload
