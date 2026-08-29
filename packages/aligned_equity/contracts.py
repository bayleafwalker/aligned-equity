from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"

EVIDENCE_CLASSES = (
    "governance_statement",
    "code_deviation",
    "remuneration_report",
    "remuneration_policy",
    "esef_financials",
    "pdmr_notice",
    "earnings_call",
    "leadership_change",
    "regulatory_event",
    "people_signal_aux",
)

SOURCE_FAMILIES = (
    "company_ir_annual_reporting",
    "nasdaq_helsinki_announcements",
    "finnish_securities_market_association",
    "fin_fsa_supervision",
    "prh_trade_register",
    "presentations_transcripts_capital_markets_days",
    "business_media_analyst_coverage",
    "people_platforms",
)

CONFIDENCE_LEVELS = (
    "high",
    "medium",
    "low",
)

COMPARABILITY_LEVELS = (
    "yes",
    "partial",
    "no",
)

PERIOD_ALIGNMENT_VALUES = (
    "aligned",
    "shifted",
    "point-in-time",
    "unknown",
)

ACCOUNTING_SCOPE_VALUES = (
    "parent",
    "group",
    "segment",
    "unknown",
    "not-applicable",
)

RESTATEMENT_STATUS_VALUES = (
    "original",
    "restated",
    "corrected",
    "unknown",
    "not-applicable",
)

SOURCE_RETRIEVAL_METHODS = (
    "manual",
    "download",
    "registry_api",
    "vendor_feed",
    "fixture",
)

SOURCE_UPDATE_FREQUENCIES = (
    "annual",
    "quarterly",
    "event-driven",
    "irregular",
    "one-off",
    "unknown",
)

SOURCE_FRESHNESS_STATUSES = (
    "current",
    "stale",
    "unknown",
    "not-applicable",
)

SOURCE_EXTRACTION_READINESS = (
    "ready",
    "manual-review-required",
    "not-ready",
)

FEATURE_FAMILIES = (
    "governance_practice",
    "remuneration_logic",
    "financial_development",
    "disclosure_style",
    "reporting_change",
    "capital_markets_signal",
    "people_signal_aux",
)

FEATURE_VALUE_TYPES = (
    "boolean",
    "categorical",
    "numeric",
    "text",
    "date",
)

FEATURE_EXTRACTION_METHODS = (
    "exact_field",
    "rule_based_parse",
    "manual_coding",
    "fixture",
)

LENS_KEYS = (
    "investment",
    "workplace",
    "product",
)

RESEARCH_STATES = (
    "long_term_candidate",
    "dislocation_candidate",
    "watch",
    "thesis_strengthened",
    "thesis_weakened",
    "deteriorating",
    "avoid",
)

DECISION_CONTEXTS = LENS_KEYS

VALUE_OF_INFORMATION_ASSESSMENTS = (
    "collect_more_evidence",
    "monitor_freshness",
    "more_research_unlikely_to_change_action",
)

SCORECARD_ASSESSMENTS = (
    "strong_negative",
    "negative",
    "neutral",
    "positive",
    "strong_positive",
    "insufficient_evidence",
)

SCORECARD_DIMENSIONS = (
    "governance and accountability",
    "remuneration and incentive alignment",
    "management-system quality",
    "candor and reporting quality",
    "workforce continuity and organizational stability",
    "adaptability and response quality",
    "conduct and reliability",
    "evidence confidence",
)

CAUSAL_CLAIM_TYPES = (
    "association",
    "warning_signal",
    "decision_relevance",
    "causal_effect",
)

FUTURE_HLA_PUBLICATION_KEYS = (
    "aligned_equity_company_evidence",
    "aligned_equity_scorecard",
    "aligned_equity_research_state",
    "aligned_equity_source_freshness",
    "aligned_equity_feature_record",
    "aligned_equity_time_series_view",
    "aligned_equity_decision_memo",
)
