from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from aligned_equity.evidence import build_decision_output, validate_evidence_record
from aligned_equity.features import validate_feature_record
from aligned_equity.identifiers import validate_entity_identifier_record
from aligned_equity.source_ledger import (
    validate_decision_readiness,
    validate_source_ledger_record,
)
from aligned_equity.validation import SCHEMA_DIR

_DECISION_PARAMETER_FIELDS = (
    "analysis_date",
    "decision_context",
    "current_research_state",
    "dimension",
    "assessment",
    "rationale",
    "likely_action_implication",
    "value_of_information_assessment",
    "value_of_information_note",
)
_CASE_STRING_FIELDS = (
    "case_id",
    "status",
    "predeclared_at",
    "predeclared_question",
    "scope",
    "decision_impact_status",
)


def _validate_case_shape(bundle: Any) -> list[str]:
    """Guard every field consumed by the joiner and Markdown renderer."""

    if not isinstance(bundle, dict):
        return ["research case bundle must be an object"]
    errors: list[str] = []
    case = bundle.get("case")
    if not isinstance(case, dict):
        return ["case must be an object"]
    for field in _CASE_STRING_FIELDS:
        if not isinstance(case.get(field), str) or not case[field].strip():
            errors.append(f"case.{field} must be a non-empty string")
    observations = case.get("observations")
    if not isinstance(observations, list):
        errors.append("case.observations must be an array")
    else:
        for index, observation in enumerate(observations):
            if not isinstance(observation, dict):
                errors.append(f"case.observations[{index}] must be an object")
                continue
            for field in ("evidence_id", "source_section", "statement"):
                if not isinstance(observation.get(field), str) or not observation[field].strip():
                    errors.append(
                        f"case.observations[{index}].{field} must be a non-empty string"
                    )
    gaps = case.get("gaps")
    if not isinstance(gaps, list) or any(not isinstance(gap, str) for gap in gaps):
        errors.append("case.gaps must be an array of strings")
    if "data_attribution" in case and not isinstance(case["data_attribution"], str):
        errors.append("case.data_attribution must be a string when present")

    parameters = case.get("decision_parameters")
    if not isinstance(parameters, dict):
        errors.append("case.decision_parameters must be an object")
    else:
        missing = [field for field in _DECISION_PARAMETER_FIELDS if field not in parameters]
        extras = sorted(set(parameters) - set(_DECISION_PARAMETER_FIELDS) - {"causal_claim"})
        if missing:
            errors.append(f"case.decision_parameters missing fields: {', '.join(missing)}")
        if extras:
            errors.append(f"case.decision_parameters has unsupported fields: {', '.join(extras)}")
        for field in _DECISION_PARAMETER_FIELDS:
            if field in parameters and not isinstance(parameters[field], str):
                errors.append(f"case.decision_parameters.{field} must be a string")
        if "causal_claim" in parameters and not isinstance(parameters["causal_claim"], dict):
            errors.append("case.decision_parameters.causal_claim must be an object")

    if not isinstance(bundle.get("company"), dict):
        errors.append("company must be an object")
    for field in ("source_ledger_records", "evidence_records", "feature_records"):
        records = bundle.get(field)
        if not isinstance(records, list):
            errors.append(f"{field} must be an array")
            continue
        if field != "feature_records" and not records:
            errors.append(f"case requires at least one {field.replace('_records', '').replace('_', '-')} record")
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                errors.append(f"{field}[{index}] must be an object")
    return errors


def build_research_case_packet(
    bundle: dict[str, Any], schema_dir: Path = SCHEMA_DIR
) -> tuple[dict[str, Any], list[str]]:
    """Validate and join a bounded research case using the existing contracts."""

    errors = _validate_case_shape(bundle)
    if errors:
        return {}, errors
    case = bundle.get("case", {})
    company = bundle.get("company", {})
    sources = bundle.get("source_ledger_records", [])
    evidence = bundle.get("evidence_records", [])
    features = bundle.get("feature_records", [])
    errors = []

    if not case.get("case_id") or not case.get("predeclared_question"):
        errors.append("case requires case_id and predeclared_question")
    if not isinstance(sources, list) or not sources:
        errors.append("case requires at least one source-ledger record")
    if not isinstance(evidence, list) or not evidence:
        errors.append("case requires at least one evidence record")
    if not isinstance(features, list):
        errors.append("feature_records must be an array")
    if errors:
        return {}, errors

    errors.extend(validate_entity_identifier_record(company, schema_dir))
    for source in sources:
        if not source.get("reuse_posture") or not source.get("reuse_posture_notes"):
            errors.append(
                f"source_id {source.get('source_id', '[unknown]')} requires an explicit "
                "reuse_posture and reuse_posture_notes for a research case"
            )
        if (
            source.get("reuse_posture") == "reproduction-authorized"
            and not source.get("reuse_license_locator")
        ):
            errors.append(
                f"source_id {source.get('source_id', '[unknown]')} has reproduction-authorized "
                "reuse_posture without reuse_license_locator"
            )
        errors.extend(validate_source_ledger_record(source, schema_dir))
    for record in evidence:
        errors.extend(validate_evidence_record(record, schema_dir))
    for feature in features:
        errors.extend(validate_feature_record(feature, schema_dir))
    if errors:
        return {}, errors
    if any(source.get("reuse_posture") == "reproduction-authorized" for source in sources) and not case.get(
        "data_attribution"
    ):
        errors.append("case must include data_attribution for reproduced licensed source data")

    source_ids = {record["source_id"] for record in sources}
    evidence_by_id = {record["evidence_id"]: record for record in evidence}
    if len(source_ids) != len(sources):
        errors.append("source-ledger source_id values must be unique within a case")
    if len(evidence_by_id) != len(evidence):
        errors.append("evidence_id values must be unique within a case")

    for record in evidence:
        if record["company_id"] != company.get("company_id"):
            errors.append(
                f"evidence {record['evidence_id']} company_id does not match case company"
            )
    errors.extend(
        validate_decision_readiness(
            evidence_records=evidence,
            source_ledger_records=sources,
            value_of_information_assessment=case.get("decision_parameters", {}).get(
                "value_of_information_assessment", ""
            ),
            schema_dir=schema_dir,
        )
    )

    feature_ids: set[str] = set()
    for feature in features:
        feature_id = feature["feature_id"]
        if feature_id in feature_ids:
            errors.append(f"feature_id {feature_id} is duplicated")
        feature_ids.add(feature_id)
        if feature["company_id"] != company.get("company_id"):
            errors.append(f"feature {feature_id} company_id does not match case company")
        unknown_evidence = set(feature["source_evidence_ids"]) - set(evidence_by_id)
        if unknown_evidence:
            errors.append(f"feature {feature_id} references unknown evidence: {sorted(unknown_evidence)}")
        unknown_sources = set(feature["source_ids"]) - source_ids
        if unknown_sources:
            errors.append(f"feature {feature_id} references unknown sources: {sorted(unknown_sources)}")
        expected_sources = {
            evidence_by_id[evidence_id]["source_id"]
            for evidence_id in feature["source_evidence_ids"]
            if evidence_id in evidence_by_id
        }
        if not expected_sources.issubset(set(feature["source_ids"])):
            errors.append(f"feature {feature_id} omits a source linked by its evidence")

    observations = case.get("observations", [])
    for observation in observations:
        if observation.get("evidence_id") not in evidence_by_id:
            errors.append(
                f"case observation references unknown evidence_id "
                f"{observation.get('evidence_id', '[missing]')}"
            )
    if errors:
        return {}, errors

    parameters = case.get("decision_parameters", {})
    decision, decision_errors = build_decision_output(
        evidence_records=evidence,
        source_ledger_records=sources,
        schema_dir=schema_dir,
        **parameters,
    )
    if decision_errors:
        return {}, decision_errors
    return {
        "case": case,
        "company": company,
        "source_ledger_records": sources,
        "evidence_records": evidence,
        "feature_records": features,
        "decision_output": decision,
    }, []


def render_research_case_markdown(packet: dict[str, Any]) -> str:
    """Render a validated packet with source lineage and limits visible."""

    case = packet["case"]
    company = packet["company"]
    sources = {source["source_id"]: source for source in packet["source_ledger_records"]}
    evidence = {record["evidence_id"]: record for record in packet["evidence_records"]}
    decision = packet["decision_output"]

    lines = [
        f"# {company['display_name']}: {case['case_id']}",
        "",
        f"**Case status:** {case['status']}",
        f"**Question (predeclared {case['predeclared_at']}):** {case['predeclared_question']}",
        "",
        case["scope"],
        "",
        "## Sources",
        "",
        "| Source | Observed | Freshness | Readiness | Reuse posture |",
        "|---|---|---|---|---|",
    ]
    for source in packet["source_ledger_records"]:
        lines.append(
            f"| [{source['source_name']}]({source['source_locator']}) "
            f"(`{source['source_id']}`) | {source['observed_at']} | "
            f"{source['freshness_status']} as of {source['freshness_as_of']} | "
            f"{source['extraction_readiness']} | {source['reuse_posture']} |"
        )
    lines.extend(["", "Source reuse notes: "])
    lines.extend(f"- `{source['source_id']}`: {source['reuse_posture_notes']}" for source in sources.values())
    if case.get("data_attribution"):
        lines.extend(["", f"**Attribution:** {case['data_attribution']}"])

    lines.extend(["", "## Source observations", ""])
    for observation in case.get("observations", []):
        record = evidence[observation["evidence_id"]]
        source = sources[record["source_id"]]
        lines.extend(
            [
                f"### {record['evidence_id']}",
                "",
                f"**Source section:** {observation['source_section']}  ",
                f"**Source:** [{source['source_name']}]({record['source_locator']})  ",
                f"**Confidence:** source {record['source_confidence']}; extraction "
                f"{record['extraction_confidence']}; interpretation {record['interpretation_confidence']}",
                "",
                observation["statement"],
                "",
                f"Limit: {record['confidence_notes']}",
                "",
            ]
        )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in packet["feature_records"]:
        grouped[feature["feature_key"]].append(feature)
    lines.extend(["## Normalized features", ""])
    for feature_key, observations in sorted(grouped.items()):
        ordered = sorted(
            observations,
            key=lambda item: item.get("period_start")
            or item.get("effective_date")
            or item["observed_at"],
        )
        unit = ordered[0].get("feature_unit", "")
        lines.extend(
            [
                f"### `{feature_key}` ({unit})",
                "",
                "| Observation | Value | Scope | Comparability |",
                "|---|---:|---|---|",
            ]
        )
        for feature in ordered:
            period = feature.get("period_start", feature.get("effective_date", feature["observed_at"]))
            lines.append(
                f"| {period} | {feature['feature_value']} | "
                f"{feature['accounting_scope']} | {feature['same_firm_comparable']} |"
            )
        lines.extend(["", ordered[0]["comparability_notes"], ""])

    lines.extend(["## Decision view", ""])
    lines.extend(
        [
            f"- **Context:** {decision['decision_context']}",
            f"- **Research state:** {decision['current_research_state']}",
            f"- **Assessment:** {decision['scorecard_dimension_assessments'][0]['assessment']}",
            f"- **Rationale:** {decision['scorecard_dimension_assessments'][0]['rationale']}",
            f"- **Implication:** {decision['likely_action_implication']}",
            f"- **Value of information:** {decision['value_of_information_assessment']} — "
            f"{decision['value_of_information_note']}",
            f"- **Decision impact:** {case['decision_impact_status']}",
            "",
            "### Open evidence gaps",
            "",
        ]
    )
    lines.extend(f"- {gap}" for gap in case.get("gaps", []))
    lines.extend(
        [
            "",
            "This view is an internal research example. It is not a personalized "
            "recommendation, does not authorize a trade, and does not claim that any "
            "decision changed or that evidence caused an outcome.",
            "",
        ]
    )
    return "\n".join(lines)
