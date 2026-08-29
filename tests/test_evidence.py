from __future__ import annotations

from typing import Any

from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.evidence import build_decision_output, validate_evidence_record


def test_evidence_record_validation_accepts_core_source() -> None:
    assert validate_evidence_record(_evidence_record(), SCHEMA_DIR) == []


def test_people_signal_aux_requires_bias_flags() -> None:
    payload = _evidence_record(
        source_family="people_platforms",
        evidence_class="people_signal_aux",
        bias_flags=[],
    )

    assert validate_evidence_record(payload, SCHEMA_DIR) == [
        "people_signal_aux evidence requires at least one bias flag"
    ]


def test_legal_or_enforcement_override_requires_regulatory_event_fields() -> None:
    payload = _evidence_record(legal_or_enforcement_override=True)

    assert validate_evidence_record(payload, SCHEMA_DIR) == [
        "legal_or_enforcement_override is only valid for regulatory_event evidence",
        "legal_or_enforcement_override requires override_severity",
        "legal_or_enforcement_override requires override_expiry_review_date",
    ]


def test_regulatory_event_override_accepts_severity_and_review_date() -> None:
    payload = _evidence_record(
        source_family="fin_fsa_supervision",
        evidence_class="regulatory_event",
        legal_or_enforcement_override=True,
        override_severity="thesis_weakened",
        override_expiry_review_date="2026-10-24",
    )

    assert validate_evidence_record(payload, SCHEMA_DIR) == []


def test_build_decision_output_from_valid_evidence_records() -> None:
    payload, errors = build_decision_output(
        evidence_records=[_evidence_record()],
        analysis_date="2026-04-24",
        decision_context="investment",
        current_research_state="watch",
        dimension="governance and accountability",
        assessment="neutral",
        rationale="The evidence is relevant to the current watch decision.",
        likely_action_implication="Preserve watch status pending another primary filing.",
        value_of_information_assessment="collect_more_evidence",
        value_of_information_note="More primary evidence could change follow-up scope.",
        schema_dir=SCHEMA_DIR,
    )

    assert errors == []
    assert payload["company_id"] == "example-company"
    assert payload["material_evidence_ids"] == ["evidence-1"]
    assert payload["confidence_summary"] == (
        "Source confidence: high; extraction confidence: high; "
        "interpretation confidence: medium."
    )
    assert payload["comparability_summary"] == (
        "Same-firm comparability: partial; cross-firm comparability: no."
    )


def test_build_decision_output_applies_source_ledger_readiness_gate() -> None:
    payload, errors = build_decision_output(
        evidence_records=[_evidence_record()],
        source_ledger_records=[_source_ledger_record(extraction_readiness="not-ready")],
        analysis_date="2026-04-24",
        decision_context="investment",
        current_research_state="watch",
        dimension="governance and accountability",
        assessment="neutral",
        rationale="The evidence is relevant to the current watch decision.",
        likely_action_implication="Preserve watch status pending another primary filing.",
        value_of_information_assessment="collect_more_evidence",
        value_of_information_note="More primary evidence could change follow-up scope.",
        schema_dir=SCHEMA_DIR,
    )

    assert payload == {}
    assert errors == ["evidence evidence-1 uses not-ready source_id source-1"]


def test_build_decision_output_rejects_mixed_company_evidence() -> None:
    second = _evidence_record(evidence_id="evidence-2", company_id="other-company")

    payload, errors = build_decision_output(
        evidence_records=[_evidence_record(), second],
        analysis_date="2026-04-24",
        decision_context="investment",
        current_research_state="watch",
        dimension="governance and accountability",
        assessment="neutral",
        rationale="The evidence is relevant to the current watch decision.",
        likely_action_implication="Preserve watch status pending another primary filing.",
        value_of_information_assessment="collect_more_evidence",
        value_of_information_note="More primary evidence could change follow-up scope.",
        schema_dir=SCHEMA_DIR,
    )

    assert payload == {}
    assert errors == ["decision output evidence must belong to exactly one company_id"]


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
