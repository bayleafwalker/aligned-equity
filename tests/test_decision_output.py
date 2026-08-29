from __future__ import annotations

from typing import Any

from aligned_equity.contracts import SCHEMA_DIR
from aligned_equity.decision_output import validate_decision_output


def test_decision_output_validation_accepts_valid_payload() -> None:
    assert validate_decision_output(_payload(), SCHEMA_DIR) == []


def test_decision_output_validation_requires_dimension_evidence_to_be_material() -> None:
    payload = _payload()
    payload["scorecard_dimension_assessments"][0]["evidence_ids"] = ["evidence-2"]

    assert validate_decision_output(payload, SCHEMA_DIR) == [
        "dimension assessment 'governance and accountability' references evidence outside "
        "material_evidence_ids: ['evidence-2']"
    ]


def test_decision_output_validation_rejects_unsupported_causal_language() -> None:
    payload = _payload()
    payload["scorecard_dimension_assessments"][0][
        "rationale"
    ] = "The governance change caused better operating results."

    errors = validate_decision_output(payload, SCHEMA_DIR)

    assert errors == [
        "scorecard_dimension_assessments[0].rationale uses causal language without "
        "causal_effect claim type and causal_design metadata"
    ]


def test_decision_output_validation_accepts_causal_language_with_design_metadata() -> None:
    payload = _payload()
    payload["scorecard_dimension_assessments"][0][
        "rationale"
    ] = "The governance change caused better operating results."
    payload["causal_claim"] = {
        "claim_type": "causal_effect",
        "causal_design": "Manual same-firm before-after review with documented confounders.",
    }

    assert validate_decision_output(payload, SCHEMA_DIR) == []


def test_decision_output_validation_accepts_stop_research_voi_assessment() -> None:
    payload = _payload()
    payload["value_of_information_assessment"] = "more_research_unlikely_to_change_action"
    payload["value_of_information_note"] = (
        "Additional detail is unlikely to change the current non-decision."
    )

    assert validate_decision_output(payload, SCHEMA_DIR) == []


def _payload() -> dict[str, Any]:
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
        "value_of_information_assessment": "collect_more_evidence",
        "value_of_information_note": "More primary evidence could change follow-up scope.",
        "causal_claim": {"claim_type": "decision_relevance"},
    }
