from __future__ import annotations

from typing import Any

from .collection_intake import (
    aggregate_forbidden_field_paths,
    forbidden_field_paths,
    is_sha256_hex,
    optional_int,
    validate_feature_vector_contract,
    validate_public_relative_path,
    validate_provenance_identity,
    validate_record_identity,
)


COLLECTION_SUBMISSION_LINT_SCHEMA = "primeproject.collection-submission-lint.v1"


def build_collection_submission_lint(
    *,
    contract: dict[str, Any],
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    templates = {
        template.get("task_id"): template
        for template in contract.get("task_templates", [])
        if template.get("task_id")
    }
    records_by_task: dict[str, list[dict[str, Any]]] = {}
    for record in records or []:
        task_id = record.get("task_id")
        if task_id:
            records_by_task.setdefault(str(task_id), []).append(record)

    rows = [
        lint_task_row(template, records_by_task.get(task_id), contract=contract)
        for task_id, template in sorted(templates.items(), key=lambda item: lint_sort_key(item[1]))
    ]
    rows.extend(
        lint_unknown_task_row(record, contract=contract)
        for record in records or []
        if record.get("task_id") not in templates
    )
    apply_lint_cross_record_checks(rows)
    summary = lint_summary(rows)
    return {
        "schema": COLLECTION_SUBMISSION_LINT_SCHEMA,
        "source_schemas": {
            "collection_submission_contract": contract.get("schema"),
        },
        "summary": summary,
        "lint_gate": {
            "status": lint_gate_status(summary),
            "message": lint_gate_message(summary),
        },
        "rows": rows,
    }


def lint_task_row(
    template: dict[str, Any],
    records: list[dict[str, Any]] | None,
    *,
    contract: dict[str, Any],
) -> dict[str, Any]:
    records = records or []
    submitted = bool(records)
    if not submitted:
        return {
            "task_id": template.get("task_id"),
            "priority": template.get("priority"),
            "library": template.get("library"),
            "baseline_id": template.get("baseline_id"),
            "object_type": template.get("object_type"),
            "bit_length": template.get("bit_length"),
            "submitted": False,
            "submission_count": 0,
            "sample_count": 0,
            "planned_sample_target": int(template.get("planned_sample_target") or 0),
            "target_samples_for_10pct_tv": int(template.get("target_samples_for_10pct_tv") or 0),
            "aggregate_artifact_sha256": None,
            "blocking_reasons": [],
            "warning_reasons": ["awaiting_submission"],
            "forbidden_public_fields": [],
            "feature_vector_contract": "not_submitted",
            "status": "awaiting_submission",
        }

    record = records[0]
    sample_count = optional_int(record.get("sample_count")) or 0
    required_fields = list((contract.get("record_contract") or {}).get("required_fields") or [])
    missing_fields = [field for field in required_fields if field not in record or record.get(field) in (None, "")]
    blockers = [f"missing_field:{field}" for field in missing_fields]
    warnings = []

    if len(records) > 1:
        blockers.append("duplicate_submission_record")
    if record.get("task_id") != template.get("task_id"):
        blockers.append("task_id_mismatch")
    blockers.extend(validate_record_identity(record, template))
    if record.get("claim_scope") != (contract.get("record_contract") or {}).get("claim_scope_must_equal", "real_world"):
        blockers.append("real_world_claim_scope")

    planned_samples = int(template.get("planned_sample_target") or 0)
    tv_floor_samples = int(template.get("target_samples_for_10pct_tv") or planned_samples)
    if sample_count < planned_samples:
        blockers.append("planned_sample_target")
    elif sample_count < tv_floor_samples:
        warnings.append("below_10pct_tv_floor")

    checksum = str(record.get("aggregate_artifact_sha256") or "")
    if not is_sha256_hex(checksum):
        blockers.append("aggregate_artifact_sha256")
    if not record.get("provenance_record"):
        blockers.append("provenance_record")
    blockers.extend(validate_provenance_identity(record, template))
    if not record.get("feature_vector_path"):
        blockers.append("feature_vector_path")
    else:
        blockers.extend(validate_public_relative_path(record.get("feature_vector_path"), "feature_vector_path"))

    vector_contract = validate_feature_vector_contract(record, template, sample_count=sample_count)
    blockers.extend(vector_contract.get("blocking_reasons") or [])
    forbidden = aggregate_forbidden_field_paths(records)
    if forbidden:
        blockers.append("forbidden_public_fields")

    blockers = list(dict.fromkeys(blockers))
    warnings = list(dict.fromkeys(warnings))
    status = "blocked" if blockers else "warning" if warnings else "pass"
    return {
        "task_id": template.get("task_id"),
        "priority": template.get("priority"),
        "library": template.get("library"),
        "baseline_id": template.get("baseline_id"),
        "object_type": template.get("object_type"),
        "bit_length": template.get("bit_length"),
        "submitted": True,
        "submission_count": len(records),
        "sample_count": sample_count,
        "planned_sample_target": planned_samples,
        "target_samples_for_10pct_tv": tv_floor_samples,
        "aggregate_artifact_sha256": checksum if is_sha256_hex(checksum) else None,
        "blocking_reasons": blockers,
        "warning_reasons": warnings,
        "forbidden_public_fields": forbidden,
        "feature_vector_contract": vector_contract.get("status"),
        "feature_vector_label": vector_contract.get("label"),
        "status": status,
    }


def lint_unknown_task_row(record: dict[str, Any], *, contract: dict[str, Any]) -> dict[str, Any]:
    forbidden = forbidden_field_paths(record)
    checksum = str(record.get("aggregate_artifact_sha256") or "")
    return {
        "task_id": record.get("task_id"),
        "priority": "PX",
        "library": record.get("library", "unknown"),
        "baseline_id": record.get("baseline_id", "unknown"),
        "object_type": record.get("object_type", "unknown"),
        "bit_length": record.get("bit_length"),
        "submitted": True,
        "submission_count": 1,
        "sample_count": optional_int(record.get("sample_count")) or 0,
        "planned_sample_target": 0,
        "target_samples_for_10pct_tv": 0,
        "aggregate_artifact_sha256": checksum if is_sha256_hex(checksum) else None,
        "blocking_reasons": ["unknown_task", *("forbidden_public_fields" for _ in forbidden)],
        "warning_reasons": [],
        "forbidden_public_fields": forbidden,
        "feature_vector_contract": "unknown_task",
        "status": "blocked",
        "contract_task_count": len(contract.get("task_templates", [])),
    }


def apply_lint_cross_record_checks(rows: list[dict[str, Any]]) -> None:
    hashes: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        checksum = str(row.get("aggregate_artifact_sha256") or "")
        if row.get("submitted") and is_sha256_hex(checksum):
            hashes.setdefault(checksum.lower(), []).append(row)

    for checksum, matching_rows in hashes.items():
        task_ids = {row.get("task_id") for row in matching_rows}
        if len(matching_rows) < 2 or len(task_ids) < 2:
            continue
        for row in matching_rows:
            reasons = list(row.get("blocking_reasons") or [])
            if "aggregate_artifact_sha256_reused" not in reasons:
                reasons.append("aggregate_artifact_sha256_reused")
            row["blocking_reasons"] = reasons
            row["reused_aggregate_artifact_sha256"] = checksum
            row["status"] = "blocked"


def lint_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    submitted = [row for row in rows if row.get("submitted")]
    awaiting = [row for row in rows if row.get("status") == "awaiting_submission"]
    passed = [row for row in rows if row.get("status") == "pass"]
    warnings = [row for row in rows if row.get("status") == "warning"]
    blocked = [row for row in rows if row.get("status") == "blocked"]
    return {
        "task_count": len(rows),
        "submitted_count": len(submitted),
        "awaiting_submission_count": len(awaiting),
        "pass_count": len(passed),
        "warning_count": len(warnings),
        "blocked_count": len(blocked),
        "forbidden_public_field_count": sum(len(row.get("forbidden_public_fields") or []) for row in rows),
        "feature_vector_blocked_count": sum(
            1
            for row in rows
            if any(str(reason).startswith("feature_vector_") for reason in row.get("blocking_reasons", []))
        ),
        "reused_aggregate_hash_count": sum(
            1 for row in rows if "aggregate_artifact_sha256_reused" in (row.get("blocking_reasons") or [])
        ),
        "dominant_blockers": dominant_blockers(rows),
        "dominant_warnings": dominant_warnings(rows),
    }


def dominant_blockers(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in rows:
        for reason in row.get("blocking_reasons", []):
            counts[reason] = counts.get(reason, 0) + 1
    return [
        {"reason": reason, "count": count}
        for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def dominant_warnings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in rows:
        for reason in row.get("warning_reasons", []):
            counts[reason] = counts.get(reason, 0) + 1
    return [
        {"reason": reason, "count": count}
        for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def lint_gate_status(summary: dict[str, Any]) -> str:
    if int(summary.get("submitted_count") or 0) == 0:
        return "waiting"
    if int(summary.get("blocked_count") or 0) > 0:
        return "blocked"
    if int(summary.get("warning_count") or 0) > 0:
        return "warning"
    return "ready_for_intake"


def lint_gate_message(summary: dict[str, Any]) -> str:
    status = lint_gate_status(summary)
    if status == "ready_for_intake":
        return "Submitted records satisfy the public contract and can proceed to collection intake."
    if status == "warning":
        return "Submitted records satisfy blocking checks but remain below one or more stronger screening floors."
    if status == "blocked":
        return "Submitted records violate the public contract and should be fixed before collection intake."
    return "No submitted records are available; collectors can use the task templates before intake."


def lint_sort_key(row: dict[str, Any]) -> tuple[int, str, int]:
    priority_rank = {"P0": 0, "P1": 1, "P2": 2, "PX": 9}
    return (
        priority_rank.get(str(row.get("priority")), 9),
        str(row.get("library") or ""),
        int(row.get("bit_length") or 0),
    )
