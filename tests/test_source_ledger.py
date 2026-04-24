from __future__ import annotations

from typing import Any

from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.source_ledger import (
    validate_decision_readiness,
    validate_source_ledger_record,
)


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


def test_decision_readiness_accepts_current_ready_source() -> None:
    assert (
        validate_decision_readiness(
            evidence_records=[_evidence_record()],
            source_ledger_records=[_source_ledger_record(derived_evidence_ids=["evidence-1"])],
            value_of_information_assessment="more_research_unlikely_to_change_action",
            schema_dir=SCHEMA_DIR,
        )
        == []
    )


def test_decision_readiness_requires_source_ledger_for_material_evidence() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record()],
        source_ledger_records=[],
        value_of_information_assessment="collect_more_evidence",
        schema_dir=SCHEMA_DIR,
    ) == [
        "evidence evidence-1 references source_id source-1 without a source-ledger record"
    ]


def test_decision_readiness_rejects_source_family_mismatch() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record(source_family="fin_fsa_supervision")],
        source_ledger_records=[_source_ledger_record()],
        value_of_information_assessment="collect_more_evidence",
        schema_dir=SCHEMA_DIR,
    ) == [
        "evidence evidence-1 source_family fin_fsa_supervision does not match "
        "source-ledger source_family company_ir_annual_reporting"
    ]


def test_decision_readiness_rejects_unlinked_derived_evidence() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record()],
        source_ledger_records=[_source_ledger_record(derived_evidence_ids=["evidence-2"])],
        value_of_information_assessment="collect_more_evidence",
        schema_dir=SCHEMA_DIR,
    ) == [
        "evidence evidence-1 is not listed in source-ledger derived_evidence_ids "
        "for source_id source-1"
    ]


def test_decision_readiness_rejects_not_ready_source() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record()],
        source_ledger_records=[_source_ledger_record(extraction_readiness="not-ready")],
        value_of_information_assessment="collect_more_evidence",
        schema_dir=SCHEMA_DIR,
    ) == ["evidence evidence-1 uses not-ready source_id source-1"]


def test_decision_readiness_requires_collect_more_evidence_for_manual_review() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record()],
        source_ledger_records=[
            _source_ledger_record(extraction_readiness="manual-review-required")
        ],
        value_of_information_assessment="monitor_freshness",
        schema_dir=SCHEMA_DIR,
    ) == [
        "evidence evidence-1 uses manual-review-required source_id source-1 "
        "without collect_more_evidence VOI"
    ]


def test_decision_readiness_rejects_stale_source_when_voi_says_stop_research() -> None:
    assert validate_decision_readiness(
        evidence_records=[_evidence_record()],
        source_ledger_records=[_source_ledger_record(freshness_status="stale")],
        value_of_information_assessment="more_research_unlikely_to_change_action",
        schema_dir=SCHEMA_DIR,
    ) == [
        "evidence evidence-1 uses stale source_id source-1 but VOI says more "
        "research is unlikely to change action"
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


def _evidence_record(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "evidence_id": "evidence-1",
        "company_id": "example-company",
        "source_id": "source-1",
        "source_family": "company_ir_annual_reporting",
        "evidence_class": "governance_statement",
        "document_type": "annual report",
        "observed_at": "2026-04-24",
        "collected_at": "2026-04-24T12:00:00Z",
        "source_locator": "https://example.test/report",
        "language": "en",
        "extraction_method": "manual",
        "source_confidence": "high",
        "extraction_confidence": "high",
        "interpretation_confidence": "medium",
        "confidence_notes": "Manual fixture with primary source lineage.",
        "same_firm_comparable": "partial",
        "cross_firm_comparable": "no",
        "period_alignment": "point-in-time",
        "accounting_scope": "not-applicable",
        "restatement_status": "not-applicable",
        "comparability_notes": "Cross-firm comparison is not used.",
        "bias_flags": [],
        "legal_or_enforcement_override": False,
    }
    payload.update(overrides)
    return payload
