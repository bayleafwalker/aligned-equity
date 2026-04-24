from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest
from aligned_equity.contracts import (
    CAUSAL_CLAIM_TYPES,
    DECISION_CONTEXTS,
    EVIDENCE_CLASSES,
    LENS_KEYS,
    RESEARCH_STATES,
    SOURCE_EXTRACTION_READINESS,
    SOURCE_FRESHNESS_STATUSES,
    SOURCE_RETRIEVAL_METHODS,
    SOURCE_UPDATE_FREQUENCIES,
    VALUE_OF_INFORMATION_ASSESSMENTS,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("evidence_class", EVIDENCE_CLASSES)
def test_evidence_class_schema_accepts_allowed_values(evidence_class: str) -> None:
    schema = _schema("evidence-class.schema.json")
    jsonschema.validate({"evidence_class": evidence_class}, schema)


def test_evidence_class_schema_rejects_unknown_value() -> None:
    schema = _schema("evidence-class.schema.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"evidence_class": "proxy_statement"}, schema)


def test_evidence_record_schema_accepts_required_contract() -> None:
    schema = _schema("evidence-record.schema.json")
    jsonschema.validate(_evidence_record_payload(), schema)


def test_entity_identifier_record_schema_accepts_required_contract() -> None:
    schema = _schema("entity-identifier-record.schema.json")
    jsonschema.validate(_entity_identifier_payload(), schema)


def test_entity_identifier_record_schema_rejects_unknown_source_family() -> None:
    schema = _schema("entity-identifier-record.schema.json")
    payload = _entity_identifier_payload()
    payload["source_aliases"][0]["source_family"] = "unknown_feed"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_evidence_record_schema_rejects_unknown_source_family() -> None:
    schema = _schema("evidence-record.schema.json")
    payload = _evidence_record_payload()
    payload["source_family"] = "us_proxy_statement_feed"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_source_ledger_record_schema_accepts_required_contract() -> None:
    schema = _schema("source-ledger-record.schema.json")
    jsonschema.validate(_source_ledger_payload(), schema)


@pytest.mark.parametrize("retrieval_method", SOURCE_RETRIEVAL_METHODS)
def test_source_ledger_schema_accepts_retrieval_methods(retrieval_method: str) -> None:
    schema = _schema("source-ledger-record.schema.json")
    payload = _source_ledger_payload()
    payload["retrieval_method"] = retrieval_method
    jsonschema.validate(payload, schema)


@pytest.mark.parametrize("update_frequency", SOURCE_UPDATE_FREQUENCIES)
def test_source_ledger_schema_accepts_update_frequencies(update_frequency: str) -> None:
    schema = _schema("source-ledger-record.schema.json")
    payload = _source_ledger_payload()
    payload["expected_update_frequency"] = update_frequency
    jsonschema.validate(payload, schema)


@pytest.mark.parametrize("freshness_status", SOURCE_FRESHNESS_STATUSES)
def test_source_ledger_schema_accepts_freshness_statuses(freshness_status: str) -> None:
    schema = _schema("source-ledger-record.schema.json")
    payload = _source_ledger_payload()
    payload["freshness_status"] = freshness_status
    jsonschema.validate(payload, schema)


@pytest.mark.parametrize("extraction_readiness", SOURCE_EXTRACTION_READINESS)
def test_source_ledger_schema_accepts_extraction_readiness(
    extraction_readiness: str,
) -> None:
    schema = _schema("source-ledger-record.schema.json")
    payload = _source_ledger_payload()
    payload["extraction_readiness"] = extraction_readiness
    jsonschema.validate(payload, schema)


def test_source_ledger_schema_rejects_unknown_freshness_status() -> None:
    schema = _schema("source-ledger-record.schema.json")
    payload = _source_ledger_payload()
    payload["freshness_status"] = "good_enough"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


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


def test_decision_output_schema_accepts_required_contract() -> None:
    schema = _schema("decision-output.schema.json")
    jsonschema.validate(_decision_output_payload(), schema)


@pytest.mark.parametrize("decision_context", DECISION_CONTEXTS)
def test_decision_output_schema_accepts_decision_contexts(decision_context: str) -> None:
    schema = _schema("decision-output.schema.json")
    payload = _decision_output_payload()
    payload["decision_context"] = decision_context
    jsonschema.validate(payload, schema)


@pytest.mark.parametrize("voi_assessment", VALUE_OF_INFORMATION_ASSESSMENTS)
def test_decision_output_schema_accepts_value_of_information_assessments(
    voi_assessment: str,
) -> None:
    schema = _schema("decision-output.schema.json")
    payload = _decision_output_payload()
    payload["value_of_information_assessment"] = voi_assessment
    jsonschema.validate(payload, schema)


@pytest.mark.parametrize("claim_type", CAUSAL_CLAIM_TYPES)
def test_decision_output_schema_accepts_causal_claim_types(claim_type: str) -> None:
    schema = _schema("decision-output.schema.json")
    payload = _decision_output_payload()
    payload["causal_claim"] = {"claim_type": claim_type}
    if claim_type == "causal_effect":
        payload["causal_claim"]["causal_design"] = "Matched longitudinal review."
    jsonschema.validate(payload, schema)


def test_decision_output_schema_rejects_causal_effect_without_design() -> None:
    schema = _schema("decision-output.schema.json")
    payload = _decision_output_payload()
    payload["causal_claim"] = {"claim_type": "causal_effect"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_decision_output_schema_rejects_missing_evidence_links() -> None:
    schema = _schema("decision-output.schema.json")
    payload = _decision_output_payload()
    del payload["material_evidence_ids"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def _schema(name: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / "schemas" / name).read_text(encoding="utf-8"))


def _evidence_record_payload() -> dict[str, Any]:
    return {
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


def _entity_identifier_payload() -> dict[str, Any]:
    return {
        "company_id": "example-company",
        "display_name": "Example Oyj",
        "domicile_country": "FI",
        "identifier_confidence": "high",
        "company_identifiers": {"business_id": "1234567-8"},
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


def _source_ledger_payload() -> dict[str, Any]:
    return {
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


def _decision_output_payload() -> dict[str, Any]:
    return {
        "company_id": "example-company",
        "analysis_date": "2026-04-24",
        "decision_context": "investment",
        "current_research_state": "watch",
        "material_evidence_ids": ["evidence-1"],
        "scorecard_dimension_assessments": [
            {
                "dimension": "governance and accountability",
                "assessment": "neutral",
                "rationale": "Evidence is relevant to the current watch decision.",
                "evidence_ids": ["evidence-1"],
            }
        ],
        "confidence_summary": "Source confidence is medium and extraction confidence is high.",
        "comparability_summary": "Same-firm comparison is partial; cross-firm comparison is not used.",
        "likely_action_implication": "Preserve watch status pending another primary filing.",
        "value_of_information_assessment": "more_research_unlikely_to_change_action",
        "value_of_information_note": "More research is unlikely to change action before the next filing.",
        "causal_claim": {"claim_type": "decision_relevance"},
    }
