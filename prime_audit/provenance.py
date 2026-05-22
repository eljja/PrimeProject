from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROVENANCE_REQUIREMENTS_SCHEMA = "primeproject.provenance-requirements.v1"
PROVENANCE_AUDIT_SCHEMA = "primeproject.provenance-audit.v1"

REQUIRED_FIELDS = [
    "baseline_id",
    "library",
    "library_version",
    "algorithm",
    "object_type",
    "bit_length",
    "sample_count",
    "collector",
    "collection_date",
    "host_platform",
    "source_commit",
    "build_config",
    "rng_source",
    "generation_command",
    "raw_material_policy",
    "aggregate_artifact_sha256",
]

SENSITIVE_FORBIDDEN_PUBLIC_FIELDS = [
    "private_key",
    "private_prime",
    "wallet_seed",
    "raw_signature_owner",
]


def build_provenance_requirements(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("entries", [])
    rows = [provenance_row(entry) for entry in entries if entry.get("source_type") != "public-standard"]
    return {
        "schema": PROVENANCE_REQUIREMENTS_SCHEMA,
        "required_fields": REQUIRED_FIELDS,
        "forbidden_public_fields": SENSITIVE_FORBIDDEN_PUBLIC_FIELDS,
        "row_count": len(rows),
        "missing_required_count": sum(len(row["missing_required_fields"]) for row in rows),
        "public_safety": {
            "raw_private_material_public": False,
            "aggregate_artifacts_public": True,
            "review_required_before_status_available": True,
        },
        "rows": rows,
        "claim_gate": {
            "status": "blocked" if any(row["missing_required_fields"] for row in rows) else "open",
            "message": "Real-world baselines need complete provenance before being used for attribution claims.",
        },
    }


def provenance_row(entry: dict[str, Any]) -> dict[str, Any]:
    template = default_template(entry)
    missing = [field for field in REQUIRED_FIELDS if not has_value(template.get(field))]
    return {
        "baseline_id": entry.get("baseline_id"),
        "library": entry.get("library"),
        "object_type": entry.get("object_type"),
        "status": entry.get("status"),
        "sensitive": bool(entry.get("sensitive")),
        "required_field_count": len(REQUIRED_FIELDS),
        "missing_required_fields": missing,
        "missing_required_count": len(missing),
        "completion_ratio": (len(REQUIRED_FIELDS) - len(missing)) / len(REQUIRED_FIELDS),
        "template": template,
    }


def default_template(entry: dict[str, Any]) -> dict[str, Any]:
    raw_policy = (
        "raw private keys/primes stay local; publish aggregate fingerprints only"
        if entry.get("sensitive")
        else "publish public metadata summaries only"
    )
    return {
        "baseline_id": entry.get("baseline_id"),
        "library": entry.get("library"),
        "library_version": entry.get("library_version"),
        "algorithm": entry.get("algorithm"),
        "object_type": entry.get("object_type"),
        "bit_length": entry.get("bit_length"),
        "sample_count": entry.get("sample_count"),
        "collector": None,
        "collection_date": None,
        "host_platform": None,
        "source_commit": None,
        "build_config": None,
        "rng_source": None,
        "generation_command": None,
        "raw_material_policy": raw_policy,
        "aggregate_artifact_sha256": None,
    }


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, int) and value < 0:
        return False
    return True


def build_provenance_audit(
    requirements: dict[str, Any],
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    required_fields = list(requirements.get("required_fields") or REQUIRED_FIELDS)
    forbidden_fields = list(requirements.get("forbidden_public_fields") or SENSITIVE_FORBIDDEN_PUBLIC_FIELDS)
    rows = [
        provenance_audit_row(record, required_fields, forbidden_fields)
        for record in audit_records_from_requirements(requirements, records)
    ]
    blocked_count = sum(1 for row in rows if row["status"] == "blocked")
    total_missing = sum(len(row["missing_required_fields"]) for row in rows)
    forbidden_count = sum(len(row["forbidden_public_fields"]) for row in rows)
    invalid_count = sum(len(row["invalid_fields"]) for row in rows)
    return {
        "schema": PROVENANCE_AUDIT_SCHEMA,
        "requirements_schema": requirements.get("schema"),
        "row_count": len(rows),
        "pass_count": len(rows) - blocked_count,
        "blocked_count": blocked_count,
        "summary": {
            "total_missing_required": total_missing,
            "forbidden_public_field_count": forbidden_count,
            "invalid_field_count": invalid_count,
            "public_safe": forbidden_count == 0,
        },
        "rows": rows,
        "claim_gate": {
            "status": "open" if blocked_count == 0 else "blocked",
            "message": (
                "Provenance records are complete and public artifacts contain no forbidden sensitive fields."
                if blocked_count == 0
                else "Attribution claims stay blocked until provenance records are complete and public-safe."
            ),
        },
    }


def load_provenance_records(paths: list[str | Path]) -> list[dict[str, Any]]:
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


def audit_records_from_requirements(
    requirements: dict[str, Any],
    records: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    if records:
        by_id = {record.get("baseline_id"): record for record in records if record.get("baseline_id")}
        merged = []
        for row in requirements.get("rows", []):
            baseline_id = row.get("baseline_id")
            record = dict(row.get("template") or {})
            record.update(by_id.get(baseline_id, {}))
            merged.append(record)
        extra_records = [
            record
            for record in records
            if record.get("baseline_id") not in {row.get("baseline_id") for row in requirements.get("rows", [])}
        ]
        return [*merged, *extra_records]
    return [dict(row.get("template") or {}) for row in requirements.get("rows", [])]


def provenance_audit_row(
    record: dict[str, Any],
    required_fields: list[str],
    forbidden_fields: list[str],
) -> dict[str, Any]:
    missing = [field for field in required_fields if not has_value(record.get(field))]
    forbidden = forbidden_field_paths(record, set(forbidden_fields))
    invalid = invalid_provenance_fields(record)
    blocked = bool(missing or forbidden or invalid)
    return {
        "baseline_id": record.get("baseline_id"),
        "library": record.get("library"),
        "object_type": record.get("object_type"),
        "missing_required_fields": missing,
        "forbidden_public_fields": forbidden,
        "invalid_fields": invalid,
        "status": "blocked" if blocked else "pass",
        "completion_ratio": (len(required_fields) - len(missing)) / len(required_fields) if required_fields else 1.0,
    }


def forbidden_field_paths(payload: Any, forbidden_fields: set[str], prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in forbidden_fields:
                paths.append(path)
            paths.extend(forbidden_field_paths(value, forbidden_fields, path))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            paths.extend(forbidden_field_paths(value, forbidden_fields, f"{prefix}[{index}]"))
    return paths


def invalid_provenance_fields(record: dict[str, Any]) -> list[dict[str, str]]:
    invalid = []
    sha = record.get("aggregate_artifact_sha256")
    if has_value(sha) and not is_sha256_hex(str(sha)):
        invalid.append(
            {
                "field": "aggregate_artifact_sha256",
                "reason": "expected 64 lowercase or uppercase hexadecimal characters",
            }
        )
    return invalid


def is_sha256_hex(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdefABCDEF" for character in value)
