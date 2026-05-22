from __future__ import annotations

from typing import Any


PROVENANCE_REQUIREMENTS_SCHEMA = "primeproject.provenance-requirements.v1"

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
