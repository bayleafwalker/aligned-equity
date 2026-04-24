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
    "aligned_equity_source_freshness": {
        "grain": "one row per source-ledger record",
        "purpose": (
            "Publish source freshness, retrieval, readiness, and comparability metadata "
            "without exposing raw source payloads."
        ),
        "fields": {
            "source_id": {
                "semantic_type": "source_identifier",
                "description": "Stable Aligned Equity source-ledger record identifier.",
            },
            "source_family": {
                "semantic_type": "source_family",
                "description": "Accepted Finland-first source family for the source record.",
            },
            "source_name": {
                "semantic_type": "source_display_name",
                "description": "Human-readable name for the source artifact or stream.",
            },
            "source_locator": {
                "semantic_type": "source_locator",
                "description": "Reproducible source URL, registry locator, file path, or fixture locator.",
            },
            "publisher": {
                "semantic_type": "publisher",
                "description": "Organization or platform that published the source.",
            },
            "retrieval_method": {
                "semantic_type": "retrieval_method",
                "description": "Manual, download, registry API, vendor feed, or fixture retrieval path.",
            },
            "collected_at": {
                "semantic_type": "collection_timestamp",
                "description": "Timestamp when Aligned Equity collected or accepted the source.",
            },
            "observed_at": {
                "semantic_type": "source_observed_timestamp",
                "description": "Date or timestamp represented by the source itself.",
            },
            "freshness_as_of": {
                "semantic_type": "freshness_assessment_timestamp",
                "description": "Date or timestamp used to judge whether the source is current enough.",
            },
            "expected_update_frequency": {
                "semantic_type": "expected_update_frequency",
                "description": "Expected source update cadence.",
            },
            "freshness_status": {
                "semantic_type": "freshness_status",
                "description": "Current, stale, unknown, or not-applicable freshness status.",
            },
            "language": {
                "semantic_type": "source_language",
                "description": "Source language and translation status.",
            },
            "source_confidence": {
                "semantic_type": "source_confidence",
                "description": "Authority and provenance confidence for the source record.",
            },
            "extraction_readiness": {
                "semantic_type": "extraction_readiness",
                "description": "Whether the source is ready, needs manual review, or is not ready.",
            },
            "same_firm_comparable": {
                "semantic_type": "same_firm_comparability",
                "description": "Whether same-firm longitudinal comparison is valid.",
            },
            "cross_firm_comparable": {
                "semantic_type": "cross_firm_comparability",
                "description": "Whether cross-firm comparison is valid without misleading normalization.",
            },
            "comparability_notes": {
                "semantic_type": "comparability_caveat",
                "description": "Caveats required before derived evidence is compared or scored.",
            },
            "bias_flags": {
                "semantic_type": "bias_flag_set",
                "description": "Source-family or collection-channel bias flags.",
            },
        },
    },
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
