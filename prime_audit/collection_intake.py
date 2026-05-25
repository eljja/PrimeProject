from __future__ import annotations

import json
from math import isfinite
from pathlib import Path
from typing import Any

from .feature_vectors import FEATURE_VECTOR_VERSION, SCALAR_FEATURES


COLLECTION_INTAKE_SCHEMA = "primeproject.collection-intake.v1"

FORBIDDEN_FIELD_NAMES = {
    "private_key",
    "private_prime",
    "wallet_seed",
    "raw_signature_owner",
    "raw_key_file",
}


def build_collection_intake(
    *,
    handoff: dict[str, Any],
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    task_rows = {row.get("task_id"): row for row in handoff.get("rows", []) if row.get("task_id")}
    records_by_task: dict[str, list[dict[str, Any]]] = {}
    for record in records or []:
        task_id = record.get("task_id")
        if task_id:
            records_by_task.setdefault(task_id, []).append(record)
    rows = [
        intake_row(task, records_by_task.get(task_id))
        for task_id, task in sorted(task_rows.items(), key=lambda item: intake_sort_key(item[1]))
    ]
    extra = [
        extra_intake_row(record)
        for record in records or []
        if record.get("task_id") not in task_rows
    ]
    rows.extend(extra)
    apply_cross_record_checks(rows)
    summary = intake_summary(rows)
    return {
        "schema": COLLECTION_INTAKE_SCHEMA,
        "source_schemas": {
            "collection_handoff": handoff.get("schema"),
        },
        "summary": summary,
        "claim_gate": {
            "status": "open" if summary["accepted_rsa_library_count"] >= 2 else "blocked",
            "message": (
                "At least two RSA library intake records are accepted."
                if summary["accepted_rsa_library_count"] >= 2
                else (
                    "Real-world intake remains blocked until at least two RSA library tasks pass sample, "
                    "provenance, checksum, feature-vector contract, duplicate-submission, reused-artifact, "
                    "and public-safety checks."
                )
            ),
        },
        "rows": rows,
        "public_safety": {
            "forbidden_field_names": sorted(FORBIDDEN_FIELD_NAMES),
            "private_material_publication_allowed": False,
        },
    }


def load_intake_records(paths: list[str | Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path_value in paths:
        payload = json.loads(Path(path_value).read_text(encoding="utf-8"))
        if isinstance(payload, list):
            records.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
            records.extend(item for item in payload["records"] if isinstance(item, dict))
        elif isinstance(payload, dict):
            records.append(payload)
    return records


def intake_row(task: dict[str, Any], records: list[dict[str, Any]] | None) -> dict[str, Any]:
    records = records or []
    record = records[0] if records else {}
    submitted = bool(records)
    sample_count = int(record.get("sample_count") or 0)
    required_samples = int(task.get("target_samples_for_10pct_tv") or task.get("planned_sample_target") or 0)
    planned_samples = int(task.get("planned_sample_target") or 0)
    checksum = str(record.get("aggregate_artifact_sha256") or "")
    forbidden = aggregate_forbidden_field_paths(records)
    missing = []
    if not submitted:
        missing.append("intake_record")
    if len(records) > 1:
        missing.append("duplicate_intake_record")
    if submitted and sample_count < planned_samples:
        missing.append("planned_sample_target")
    if submitted and not is_sha256_hex(checksum):
        missing.append("aggregate_artifact_sha256")
    if submitted and not record.get("provenance_record"):
        missing.append("provenance_record")
    if submitted:
        missing.extend(validate_provenance_identity(record, task))
    if submitted and not record.get("feature_vector_path"):
        missing.append("feature_vector_path")
    feature_vector_contract = (
        validate_feature_vector_contract(record, task, sample_count=sample_count)
        if submitted
        else {
            "present": False,
            "status": "not_submitted",
            "label": None,
            "blocking_reasons": [],
        }
    )
    missing.extend(feature_vector_contract["blocking_reasons"])
    if submitted and record.get("claim_scope") != "real_world":
        missing.append("real_world_claim_scope")
    blockers = list(dict.fromkeys([*missing, *("forbidden_public_fields" for _ in forbidden)]))
    status = "accepted" if submitted and not blockers else "blocked"
    if status == "accepted" and sample_count < required_samples:
        status = "screening_only"
    return {
        "task_id": task.get("task_id"),
        "priority": task.get("priority"),
        "library": task.get("library"),
        "baseline_id": task.get("baseline_id"),
        "track": task.get("track"),
        "object_type": task.get("object_type"),
        "bit_length": task.get("bit_length"),
        "submitted": submitted,
        "submission_count": len(records),
        "sample_count": sample_count,
        "planned_sample_target": planned_samples,
        "target_samples_for_10pct_tv": required_samples,
        "remaining_samples_to_10pct_tv": max(0, required_samples - sample_count),
        "claim_scope": record.get("claim_scope", "missing" if submitted else "not_submitted"),
        "aggregate_artifact_sha256": checksum if is_sha256_hex(checksum) else None,
        "provenance_record_present": bool(record.get("provenance_record")),
        "feature_vector_path": record.get("feature_vector_path"),
        "feature_vector_summary_present": feature_vector_contract["present"],
        "feature_vector_label": feature_vector_contract["label"],
        "feature_vector_contract": feature_vector_contract["status"],
        "forbidden_public_fields": forbidden,
        "blocking_reasons": blockers,
        "status": status,
    }


def extra_intake_row(record: dict[str, Any]) -> dict[str, Any]:
    forbidden = forbidden_field_paths(record)
    return {
        "task_id": record.get("task_id"),
        "priority": "PX",
        "library": record.get("library", "unknown"),
        "baseline_id": record.get("baseline_id", "unknown"),
        "track": record.get("track", "unknown"),
        "object_type": record.get("object_type", "unknown"),
        "bit_length": record.get("bit_length"),
        "submitted": True,
        "submission_count": 1,
        "sample_count": int(record.get("sample_count") or 0),
        "planned_sample_target": 0,
        "target_samples_for_10pct_tv": 0,
        "remaining_samples_to_10pct_tv": 0,
        "claim_scope": record.get("claim_scope", "missing"),
        "aggregate_artifact_sha256": record.get("aggregate_artifact_sha256"),
        "provenance_record_present": bool(record.get("provenance_record")),
        "feature_vector_path": record.get("feature_vector_path"),
        "feature_vector_summary_present": bool(feature_vector_payload(record)),
        "feature_vector_label": None,
        "feature_vector_contract": "unknown_task",
        "forbidden_public_fields": forbidden,
        "blocking_reasons": ["unknown_task", *("forbidden_public_fields" for _ in forbidden)],
        "status": "blocked",
    }


def apply_cross_record_checks(rows: list[dict[str, Any]]) -> None:
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
            row["status"] = "blocked"
            row["reused_aggregate_artifact_sha256"] = checksum


def intake_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    submitted = [row for row in rows if row.get("submitted")]
    accepted = [row for row in rows if row.get("status") == "accepted"]
    screening = [row for row in rows if row.get("status") == "screening_only"]
    blocked = [row for row in rows if row.get("status") == "blocked"]
    accepted_rsa_libraries = sorted(
        {
            row.get("library")
            for row in accepted
            if row.get("track") == "rsa-prime-generation" and row.get("library")
        }
    )
    p0_blocked = [row for row in blocked if row.get("priority") == "P0"]
    return {
        "task_count": len(rows),
        "submitted_count": len(submitted),
        "accepted_count": len(accepted),
        "screening_only_count": len(screening),
        "blocked_count": len(blocked),
        "p0_blocked_count": len(p0_blocked),
        "accepted_rsa_library_count": len(accepted_rsa_libraries),
        "accepted_rsa_libraries": accepted_rsa_libraries,
        "remaining_p0_samples_for_10pct_tv": sum(
            int(row.get("remaining_samples_to_10pct_tv") or 0)
            for row in rows
            if row.get("priority") == "P0"
        ),
        "forbidden_public_field_count": sum(len(row.get("forbidden_public_fields") or []) for row in rows),
        "duplicate_submission_count": sum(
            1 for row in rows if "duplicate_intake_record" in (row.get("blocking_reasons") or [])
        ),
        "reused_aggregate_hash_count": sum(
            1 for row in rows if "aggregate_artifact_sha256_reused" in (row.get("blocking_reasons") or [])
        ),
        "feature_vector_contract_blocked_count": sum(
            1 for row in rows if any(str(reason).startswith("feature_vector_") for reason in row.get("blocking_reasons", []))
        ),
        "dominant_blockers": dominant_blockers(rows),
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


def forbidden_field_paths(payload: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in FORBIDDEN_FIELD_NAMES:
                paths.append(path)
            paths.extend(forbidden_field_paths(value, path))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            paths.extend(forbidden_field_paths(value, f"{prefix}[{index}]"))
    return paths


def aggregate_forbidden_field_paths(records: list[dict[str, Any]]) -> list[str]:
    if len(records) <= 1:
        return forbidden_field_paths(records[0]) if records else []
    paths = []
    for index, record in enumerate(records):
        paths.extend(forbidden_field_paths(record, f"records[{index}]"))
    return paths


def validate_feature_vector_contract(record: dict[str, Any], task: dict[str, Any], *, sample_count: int) -> dict[str, Any]:
    vector = feature_vector_payload(record)
    if not vector:
        return {
            "present": False,
            "status": "missing",
            "label": None,
            "blocking_reasons": ["feature_vector_summary"],
        }

    reasons = []
    if vector.get("schema") != FEATURE_VECTOR_VERSION:
        reasons.append("feature_vector_schema")
    label = str(vector.get("label") or "")
    if not label:
        reasons.append("feature_vector_label")
    elif label != str(task.get("library") or ""):
        reasons.append("feature_vector_label_mismatch")

    record_count = optional_int(vector.get("record_count"))
    if record_count is None or record_count != sample_count:
        reasons.append("feature_vector_record_count_mismatch")

    features = vector.get("features") if isinstance(vector.get("features"), dict) else {}
    missing_features = [name for name in SCALAR_FEATURES if name not in features]
    if missing_features:
        reasons.append("feature_vector_missing_features")
    non_numeric = [name for name in SCALAR_FEATURES if name in features and not finite_number(features.get(name))]
    if non_numeric:
        reasons.append("feature_vector_non_numeric")

    bit_length = task.get("bit_length")
    bit_length_mean = features.get("bit_length_mean")
    if bit_length and finite_number(bit_length_mean) and abs(float(bit_length_mean) - float(bit_length)) > 0.5:
        reasons.append("feature_vector_bit_length_mismatch")

    return {
        "present": True,
        "status": "pass" if not reasons else "blocked",
        "label": label or None,
        "blocking_reasons": list(dict.fromkeys(reasons)),
    }


def validate_provenance_identity(record: dict[str, Any], task: dict[str, Any]) -> list[str]:
    provenance = record.get("provenance_record")
    if not isinstance(provenance, dict):
        return []
    reasons = []
    if provenance.get("baseline_id") != task.get("baseline_id"):
        reasons.append("provenance_baseline_id_mismatch")
    if provenance.get("library") != task.get("library"):
        reasons.append("provenance_library_mismatch")
    return reasons


def feature_vector_payload(record: dict[str, Any]) -> dict[str, Any] | None:
    payload = record.get("feature_vector_summary") or record.get("feature_vector")
    return payload if isinstance(payload, dict) else None


def finite_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return isfinite(number)


def optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def is_sha256_hex(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdefABCDEF" for character in value)


def intake_sort_key(row: dict[str, Any]) -> tuple[int, str, int]:
    priority_rank = {"P0": 0, "P1": 1, "P2": 2}
    return (
        priority_rank.get(str(row.get("priority")), 9),
        str(row.get("library") or ""),
        int(row.get("bit_length") or 0),
    )
