from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.decision_output import validate_decision_output
from aligned_equity.validation import load_json


def validate_evidence_record(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate normalized evidence before it is used in decision output."""

    schema = load_json(schema_dir / "evidence-record.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"evidence-record.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_people_signal_bias(payload))
    errors.extend(_validate_override_fields(payload))
    return errors


def build_decision_output(
    *,
    evidence_records: list[dict[str, Any]],
    analysis_date: str,
    decision_context: str,
    current_research_state: str,
    dimension: str,
    assessment: str,
    rationale: str,
    likely_action_implication: str,
    value_of_information_assessment: str,
    value_of_information_note: str,
    schema_dir: Path,
    causal_claim: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Build and validate a minimal evidence-to-decision memo payload."""

    errors: list[str] = []
    for record in evidence_records:
        errors.extend(validate_evidence_record(record, schema_dir))
    if errors:
        return {}, errors

    company_ids = {record["company_id"] for record in evidence_records}
    if len(company_ids) != 1:
        return {}, ["decision output evidence must belong to exactly one company_id"]

    evidence_ids = [record["evidence_id"] for record in evidence_records]
    payload: dict[str, Any] = {
        "company_id": evidence_records[0]["company_id"],
        "analysis_date": analysis_date,
        "decision_context": decision_context,
        "current_research_state": current_research_state,
        "material_evidence_ids": evidence_ids,
        "scorecard_dimension_assessments": [
            {
                "dimension": dimension,
                "assessment": assessment,
                "rationale": rationale,
                "evidence_ids": evidence_ids,
            }
        ],
        "confidence_summary": _confidence_summary(evidence_records),
        "comparability_summary": _comparability_summary(evidence_records),
        "likely_action_implication": likely_action_implication,
        "value_of_information_assessment": value_of_information_assessment,
        "value_of_information_note": value_of_information_note,
        "causal_claim": causal_claim or {"claim_type": "decision_relevance"},
    }
    return payload, validate_decision_output(payload, schema_dir)


def _validate_people_signal_bias(payload: dict[str, Any]) -> list[str]:
    if payload["evidence_class"] == "people_signal_aux" and not payload["bias_flags"]:
        return ["people_signal_aux evidence requires at least one bias flag"]
    return []


def _validate_override_fields(payload: dict[str, Any]) -> list[str]:
    if not payload["legal_or_enforcement_override"]:
        return []

    errors: list[str] = []
    if payload["evidence_class"] != "regulatory_event":
        errors.append("legal_or_enforcement_override is only valid for regulatory_event evidence")
    if not payload.get("override_severity"):
        errors.append("legal_or_enforcement_override requires override_severity")
    if not payload.get("override_expiry_review_date"):
        errors.append("legal_or_enforcement_override requires override_expiry_review_date")
    return errors


def _confidence_summary(evidence_records: list[dict[str, Any]]) -> str:
    source_levels = sorted({record["source_confidence"] for record in evidence_records})
    extraction_levels = sorted({record["extraction_confidence"] for record in evidence_records})
    interpretation_levels = sorted(
        {record["interpretation_confidence"] for record in evidence_records}
    )
    return (
        f"Source confidence: {', '.join(source_levels)}; "
        f"extraction confidence: {', '.join(extraction_levels)}; "
        f"interpretation confidence: {', '.join(interpretation_levels)}."
    )


def _comparability_summary(evidence_records: list[dict[str, Any]]) -> str:
    same_firm = sorted({record["same_firm_comparable"] for record in evidence_records})
    cross_firm = sorted({record["cross_firm_comparable"] for record in evidence_records})
    return (
        f"Same-firm comparability: {', '.join(same_firm)}; "
        f"cross-firm comparability: {', '.join(cross_firm)}."
    )
