from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from aligned_equity.validation import load_json


def validate_source_ledger_record(payload: dict[str, Any], schema_dir: Path) -> list[str]:
    """Validate normalized source-ledger records before evidence extraction."""

    schema = load_json(schema_dir / "source-ledger-record.schema.json")
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        return [f"source-ledger-record.schema.json failed validation: {exc.message}"]

    errors: list[str] = []
    errors.extend(_validate_people_platform_bias(payload))
    errors.extend(_validate_extraction_linkage(payload))
    return errors


def validate_decision_readiness(
    *,
    evidence_records: list[dict[str, Any]],
    source_ledger_records: list[dict[str, Any]],
    value_of_information_assessment: str,
    schema_dir: Path,
) -> list[str]:
    """Validate source-ledger readiness before evidence is used in a decision memo."""

    errors: list[str] = []
    for record in source_ledger_records:
        errors.extend(validate_source_ledger_record(record, schema_dir))
    if errors:
        return errors

    source_records_by_id = {record["source_id"]: record for record in source_ledger_records}
    for evidence in evidence_records:
        source = source_records_by_id.get(evidence["source_id"])
        if source is None:
            errors.append(
                f"evidence {evidence['evidence_id']} references source_id "
                f"{evidence['source_id']} without a source-ledger record"
            )
            continue
        errors.extend(_validate_evidence_source_link(evidence, source))
        errors.extend(
            _validate_decision_use(
                evidence_id=evidence["evidence_id"],
                source=source,
                value_of_information_assessment=value_of_information_assessment,
            )
        )
    return errors


def _validate_people_platform_bias(payload: dict[str, Any]) -> list[str]:
    if payload["source_family"] == "people_platforms" and not payload["bias_flags"]:
        return ["people_platforms source-ledger records require at least one bias flag"]
    return []


def _validate_extraction_linkage(payload: dict[str, Any]) -> list[str]:
    if payload["extraction_readiness"] == "not-ready" and payload.get("derived_evidence_ids"):
        return ["not-ready source-ledger records cannot have derived_evidence_ids"]
    return []


def _validate_evidence_source_link(
    evidence: dict[str, Any],
    source: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if evidence["source_family"] != source["source_family"]:
        errors.append(
            f"evidence {evidence['evidence_id']} source_family "
            f"{evidence['source_family']} does not match source-ledger source_family "
            f"{source['source_family']}"
        )

    derived_evidence_ids = source.get("derived_evidence_ids", [])
    if derived_evidence_ids and evidence["evidence_id"] not in derived_evidence_ids:
        errors.append(
            f"evidence {evidence['evidence_id']} is not listed in source-ledger "
            f"derived_evidence_ids for source_id {source['source_id']}"
        )
    return errors


def _validate_decision_use(
    *,
    evidence_id: str,
    source: dict[str, Any],
    value_of_information_assessment: str,
) -> list[str]:
    errors: list[str] = []
    if source["extraction_readiness"] == "not-ready":
        errors.append(f"evidence {evidence_id} uses not-ready source_id {source['source_id']}")
    if (
        source["extraction_readiness"] == "manual-review-required"
        and value_of_information_assessment != "collect_more_evidence"
    ):
        errors.append(
            f"evidence {evidence_id} uses manual-review-required source_id "
            f"{source['source_id']} without collect_more_evidence VOI"
        )
    if (
        source["freshness_status"] in {"stale", "unknown"}
        and value_of_information_assessment == "more_research_unlikely_to_change_action"
    ):
        errors.append(
            f"evidence {evidence_id} uses {source['freshness_status']} source_id "
            f"{source['source_id']} but VOI says more research is unlikely to change action"
        )
    return errors
