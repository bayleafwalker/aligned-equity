from __future__ import annotations

import hashlib
from pathlib import Path

from aligned_equity.validation import REQUIRED_DOCS, REQUIRED_ROOT_FILES, validate_repository

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repository_contract_validation_passes() -> None:
    assert validate_repository(REPO_ROOT) == []


def test_required_root_files_exist() -> None:
    missing = [path for path in REQUIRED_ROOT_FILES if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_docs_index_includes_durable_docs() -> None:
    index = (REPO_ROOT / "docs/README.md").read_text(encoding="utf-8")
    missing = [
        path.removeprefix("docs/")
        for path in REQUIRED_DOCS
        if path != "docs/README.md" and path.removeprefix("docs/") not in index
    ]
    assert missing == []


def test_research_notes_are_not_byte_duplicate() -> None:
    canonical = REPO_ROOT / "docs/soft-leadership-factors.md"
    pointer = REPO_ROOT / "docs/research-notes.md"
    assert _sha256(canonical) != _sha256(pointer)
    assert "soft-leadership-factors.md" in pointer.read_text(encoding="utf-8")


def test_envrc_uses_repo_local_state() -> None:
    text = (REPO_ROOT / ".envrc").read_text(encoding="utf-8")
    assert 'export SPRINTCTL_DB="${PWD}/.sprintctl/sprintctl.db"' in text
    assert 'export KCTL_DB="${PWD}/.kctl/kctl.db"' in text
    assert 'export KCTL_PROJECT="aligned-equity"' in text


def test_phase_0_specs_capture_required_contract_fields() -> None:
    evidence = (REPO_ROOT / "docs/specifications/evidence-record-spec.md").read_text(
        encoding="utf-8"
    )
    lens = (REPO_ROOT / "docs/specifications/lens-scorecard-spec.md").read_text(
        encoding="utf-8"
    )
    source_inventory = (
        REPO_ROOT / "docs/specifications/finland-source-inventory.md"
    ).read_text(encoding="utf-8")
    source_fixture_boundaries = (
        REPO_ROOT / "docs/specifications/phase-1-source-fixture-boundaries.md"
    ).read_text(encoding="utf-8")
    entity_identifiers = (
        REPO_ROOT / "docs/specifications/entity-identifier-normalization.md"
    ).read_text(encoding="utf-8")
    hla_spike = (
        REPO_ROOT / "docs/specifications/hla-publication-contract-spike.md"
    ).read_text(encoding="utf-8")
    feature_record = (
        REPO_ROOT / "docs/specifications/feature-record-spec.md"
    ).read_text(encoding="utf-8")
    time_series_view = (
        REPO_ROOT / "docs/specifications/time-series-view-contract.md"
    ).read_text(encoding="utf-8")
    reporting_style_change = (
        REPO_ROOT / "docs/specifications/reporting-style-change-detection.md"
    ).read_text(encoding="utf-8")
    remuneration_logic = (
        REPO_ROOT / "docs/specifications/remuneration-logic-extraction.md"
    ).read_text(encoding="utf-8")
    scorecard_run = (
        REPO_ROOT / "docs/specifications/scorecard-run-spec.md"
    ).read_text(encoding="utf-8")
    decision_output = (
        REPO_ROOT / "docs/specifications/decision-output-contract.md"
    ).read_text(encoding="utf-8")

    for field in (
        "source_confidence",
        "extraction_confidence",
        "interpretation_confidence",
        "same_firm_comparable",
        "cross_firm_comparable",
        "bias_flags",
    ):
        assert field in evidence

    source_ledger = (
        REPO_ROOT / "docs/specifications/source-ledger-record-spec.md"
    ).read_text(encoding="utf-8")
    for field in (
        "freshness_status",
        "extraction_readiness",
        "same_firm_comparable",
        "cross_firm_comparable",
        "bias_flags",
    ):
        assert field in source_ledger
    assert "Source-ledger records do not contain extracted feature values" in source_ledger
    assert "Live ingestion jobs" in source_ledger

    assert "Allowed transitions" in lens
    assert "event override" in lens
    assert "people-platform" in source_inventory
    assert "not a primary scored axis" in source_inventory
    for source_family in (
        "company_ir_annual_reporting",
        "nasdaq_helsinki_announcements",
        "finnish_securities_market_association",
        "fin_fsa_supervision",
        "prh_trade_register",
        "presentations_transcripts_capital_markets_days",
        "business_media_analyst_coverage",
        "people_platforms",
    ):
        assert source_family in source_fixture_boundaries
    assert "People-platform evidence without bias flags" in source_fixture_boundaries
    assert "without network access" in source_fixture_boundaries
    for field in (
        "company_id",
        "company_identifiers",
        "security_identifiers",
        "source_aliases",
    ):
        assert field in entity_identifiers
    assert "Using ticker alone" in entity_identifiers
    for field in (
        "feature_id",
        "feature_key",
        "source_evidence_ids",
        "extraction_rule_id",
        "same_firm_comparable",
    ):
        assert field in feature_record
    assert "Feature records do not contain scorecard dimensions" in feature_record
    assert "People-platform-derived features remain auxiliary" in feature_record
    for field in (
        "time_series_id",
        "observation_periods",
        "gap_notes",
        "restatement_status",
    ):
        assert field in time_series_view
    assert "A view must contain one `company_id` and one `feature_key`" in time_series_view
    assert "Time-series views do not contain scorecard dimensions" in time_series_view
    for field in (
        "reporting_topic_added",
        "reporting_specificity_delta",
        "reporting_claim_outcome_divergence",
        "governance_deviation_explanation_change",
    ):
        assert field in reporting_style_change
    assert "People-platform evidence is out of scope" in reporting_style_change
    assert "Reporting-style features are not scorecard assessments" in reporting_style_change
    for field in (
        "variable_pay_criteria_present",
        "long_term_incentive_horizon_years",
        "malus_clawback_mechanism_present",
        "realized_pay_comparison_period_years",
    ):
        assert field in remuneration_logic
    assert "Remuneration-logic features are not scorecard assessments" in remuneration_logic
    assert "People-platform, media, and analyst sources are out of scope" in remuneration_logic
    for field in (
        "scorecard_run_id",
        "dimension_assessments",
        "material_feature_ids",
        "source_freshness_summary",
    ):
        assert field in scorecard_run
    assert "Scorecard runs do not extract feature values" in scorecard_run
    assert "Scorecard runs do not contain lens weights" in scorecard_run
    assert "Aligned Equity does not import HLA" in hla_spike
    assert "aligned_equity_feature_record" in hla_spike
    assert "aligned_equity_time_series_view" in hla_spike
    assert "Feature Record Field Semantics" in hla_spike
    assert "Time-Series View Field Semantics" in hla_spike
    assert "value_of_information_assessment" in decision_output
    assert "causal_design" in decision_output
    assert "numeric predictive" in decision_output


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
