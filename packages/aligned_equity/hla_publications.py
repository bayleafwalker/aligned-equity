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
    "aligned_equity_feature_record": {
        "grain": "one row per deterministic feature observation",
        "purpose": (
            "Publish validated feature records with evidence lineage, extraction-rule "
            "identity, confidence, and comparability metadata."
        ),
        "fields": {
            "feature_id": {
                "semantic_type": "feature_identifier",
                "description": "Stable Aligned Equity feature observation identifier.",
            },
            "company_id": {
                "semantic_type": "entity_identifier",
                "description": "Stable Aligned Equity company identity key.",
            },
            "feature_key": {
                "semantic_type": "feature_key",
                "description": "Stable machine key for the deterministic feature.",
            },
            "feature_family": {
                "semantic_type": "feature_family",
                "description": "Governance, remuneration, financial, disclosure, reporting, market, or auxiliary people feature family.",
            },
            "feature_value_type": {
                "semantic_type": "feature_value_type",
                "description": "Declared primitive type for the feature value.",
            },
            "feature_value": {
                "semantic_type": "feature_value",
                "description": "Deterministic extracted primitive value, not a scorecard assessment.",
            },
            "observed_at": {
                "semantic_type": "feature_observed_timestamp",
                "description": "Date or timestamp represented by the underlying evidence.",
            },
            "extracted_at": {
                "semantic_type": "feature_extraction_timestamp",
                "description": "Timestamp when Aligned Equity produced the feature record.",
            },
            "source_evidence_ids": {
                "semantic_type": "evidence_reference_set",
                "description": "Evidence records used to derive the feature.",
            },
            "source_ids": {
                "semantic_type": "source_reference_set",
                "description": "Source-ledger records represented by the linked evidence.",
            },
            "extraction_rule_id": {
                "semantic_type": "extraction_rule_identifier",
                "description": "Stable identifier for the extraction rule or manual coding rubric.",
            },
            "extraction_rule_version": {
                "semantic_type": "extraction_rule_version",
                "description": "Version of the extraction rule used for longitudinal auditability.",
            },
            "extraction_method": {
                "semantic_type": "extraction_method",
                "description": "Exact field, rule-based parse, manual coding, or fixture method.",
            },
            "source_confidence": {
                "semantic_type": "source_confidence",
                "description": "Authority and provenance confidence carried from source evidence.",
            },
            "extraction_confidence": {
                "semantic_type": "extraction_confidence",
                "description": "Reliability of extracting the feature value from source evidence.",
            },
            "interpretation_confidence": {
                "semantic_type": "interpretation_confidence",
                "description": "Reliability of mapping evidence into the deterministic feature.",
            },
            "confidence_notes": {
                "semantic_type": "confidence_caveat",
                "description": "Reason for source, extraction, or interpretation confidence limits.",
            },
            "same_firm_comparable": {
                "semantic_type": "same_firm_comparability",
                "description": "Whether the feature can compare against the same company's prior periods.",
            },
            "cross_firm_comparable": {
                "semantic_type": "cross_firm_comparability",
                "description": "Whether cross-firm comparison is valid without misleading normalization.",
            },
            "period_alignment": {
                "semantic_type": "period_alignment",
                "description": "Whether the feature period lines up with the target analysis period.",
            },
            "accounting_scope": {
                "semantic_type": "accounting_scope",
                "description": "Entity scope represented by the feature.",
            },
            "restatement_status": {
                "semantic_type": "restatement_status",
                "description": "Whether later source changes affect feature interpretation.",
            },
            "comparability_notes": {
                "semantic_type": "comparability_caveat",
                "description": "Caveats required before using the feature in views or scorecards.",
            },
            "bias_flags": {
                "semantic_type": "bias_flag_set",
                "description": "Source-family, extraction, or collection-channel bias flags.",
            },
        },
    },
    "aligned_equity_time_series_view": {
        "grain": "one row per company, feature key, and time-series view",
        "purpose": (
            "Publish same-firm feature histories with ordered observations, lineage "
            "roll-ups, gap notes, restatement exposure, and comparability caveats."
        ),
        "fields": {
            "time_series_id": {
                "semantic_type": "time_series_identifier",
                "description": "Stable Aligned Equity identifier for the time-series view.",
            },
            "company_id": {
                "semantic_type": "entity_identifier",
                "description": "Stable company identity key shared by every included observation.",
            },
            "feature_key": {
                "semantic_type": "feature_key",
                "description": "Single deterministic feature key represented by the series.",
            },
            "feature_family": {
                "semantic_type": "feature_family",
                "description": "Feature family inherited from the included feature records.",
            },
            "observation_periods": {
                "semantic_type": "ordered_feature_observation_set",
                "description": "Ordered observations with period, value, feature lineage, confidence, and comparability metadata.",
            },
            "source_evidence_ids": {
                "semantic_type": "evidence_reference_set",
                "description": "Deduplicated evidence IDs represented by all observations in the view.",
            },
            "source_ids": {
                "semantic_type": "source_reference_set",
                "description": "Deduplicated source-ledger IDs represented by all observations in the view.",
            },
            "series_start": {
                "semantic_type": "series_start",
                "description": "Earliest period, effective date, or observation date represented by the series.",
            },
            "series_end": {
                "semantic_type": "series_end",
                "description": "Latest period, effective date, or observation date represented by the series.",
            },
            "same_firm_comparable": {
                "semantic_type": "same_firm_comparability",
                "description": "Roll-up comparability for using the sequence as a same-firm history.",
            },
            "period_alignment": {
                "semantic_type": "period_alignment",
                "description": "Roll-up period alignment across observations.",
            },
            "accounting_scope": {
                "semantic_type": "accounting_scope",
                "description": "Roll-up entity scope for the represented series.",
            },
            "restatement_status": {
                "semantic_type": "restatement_status",
                "description": "Whether the series includes original, restated, corrected, or unknown observations.",
            },
            "gap_notes": {
                "semantic_type": "coverage_gap_caveat",
                "description": "Explicit gaps in years, quarters, events, or comparable source coverage.",
            },
            "comparability_notes": {
                "semantic_type": "comparability_caveat",
                "description": "Caveats before the series can support interpretation.",
            },
            "confidence_notes": {
                "semantic_type": "confidence_caveat",
                "description": "Confidence caveats before the series can support interpretation.",
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
