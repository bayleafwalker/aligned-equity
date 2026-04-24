from __future__ import annotations

from typing import Final, TypedDict


class PublicationFieldMetadata(TypedDict):
    semantic_type: str
    description: str


class PublicationMetadata(TypedDict):
    grain: str
    purpose: str
    fields: dict[str, PublicationFieldMetadata]


HLA_PUBLICATION_METADATA: Final[dict[str, PublicationMetadata]] = {
    "aligned_equity_decision_memo": {
        "grain": "one row per company, analysis date, and decision context",
        "purpose": "Publish decision-support outputs without exposing raw source payloads.",
        "fields": {
            "company_id": {
                "semantic_type": "entity_identifier",
                "description": "Stable Aligned Equity company identity key.",
            },
            "analysis_date": {
                "semantic_type": "analysis_date",
                "description": "Date the decision memo was produced.",
            },
            "decision_context": {
                "semantic_type": "decision_context",
                "description": "Investment, workplace, or product decision context.",
            },
            "current_research_state": {
                "semantic_type": "research_state",
                "description": "Research state before any later transition is applied.",
            },
            "material_evidence_ids": {
                "semantic_type": "evidence_reference_set",
                "description": "Evidence records that materially support the memo.",
            },
            "scorecard_dimension_assessments": {
                "semantic_type": "dimension_assessment_set",
                "description": "Directional scorecard assessments with rationale and evidence links.",
            },
            "confidence_summary": {
                "semantic_type": "confidence_summary",
                "description": "Source, extraction, interpretation, freshness, and coverage limits.",
            },
            "comparability_summary": {
                "semantic_type": "comparability_summary",
                "description": "Same-firm and cross-firm caveats that constrain interpretation.",
            },
            "likely_action_implication": {
                "semantic_type": "decision_implication",
                "description": "Practical action or non-action implication for the decision context.",
            },
            "value_of_information_assessment": {
                "semantic_type": "value_of_information_assessment",
                "description": "Whether more evidence is expected to change action.",
            },
            "value_of_information_note": {
                "semantic_type": "value_of_information_rationale",
                "description": "Reasoning behind the value-of-information assessment.",
            },
            "causal_claim": {
                "semantic_type": "causal_claim_guardrail",
                "description": "Claim type and causal-design metadata when causal effects are asserted.",
            },
        },
    }
}
