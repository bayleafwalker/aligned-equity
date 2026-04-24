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
    "aligned_equity_decision_memo",
)
