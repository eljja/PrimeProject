from __future__ import annotations

from typing import Any

from .collection_intake import FORBIDDEN_FIELD_NAMES
from .feature_vectors import FEATURE_VECTOR_VERSION, SCALAR_FEATURES


COLLECTION_SUBMISSION_CONTRACT_SCHEMA = "primeproject.collection-submission-contract.v1"

REQUIRED_RECORD_FIELDS = [
    "task_id",
    "sample_count",
    "claim_scope",
    "aggregate_artifact_sha256",
    "provenance_record",
    "feature_vector_path",
    "feature_vector_summary",
]


def build_collection_submission_contract(*, handoff: dict[str, Any]) -> dict[str, Any]:
    tasks = [submission_task_template(row) for row in handoff.get("rows", [])]
    p0_tasks = [task for task in tasks if task.get("priority") == "P0"]
    return {
        "schema": COLLECTION_SUBMISSION_CONTRACT_SCHEMA,
        "source_schemas": {"collection_handoff": handoff.get("schema")},
        "summary": {
            "task_count": len(tasks),
            "p0_count": len(p0_tasks),
            "required_record_field_count": len(REQUIRED_RECORD_FIELDS),
            "required_scalar_feature_count": len(SCALAR_FEATURES),
            "forbidden_public_field_count": len(FORBIDDEN_FIELD_NAMES),
            "claim_scope_required": "real_world",
            "feature_vector_schema": FEATURE_VECTOR_VERSION,
            "private_material_publication_allowed": False,
        },
        "record_contract": {
            "required_fields": list(REQUIRED_RECORD_FIELDS),
            "claim_scope_must_equal": "real_world",
            "aggregate_artifact_sha256": {
                "encoding": "hex",
                "length": 64,
                "must_be_unique_across_task_ids": True,
            },
            "sample_count": {
                "must_meet_planned_sample_target": True,
                "screening_only_below_10pct_tv_floor": True,
            },
        },
        "feature_vector_contract": {
            "schema": FEATURE_VECTOR_VERSION,
            "required_scalar_features": list(SCALAR_FEATURES),
            "record_count_must_equal_sample_count": True,
            "bit_length_mean_must_match_task_bit_length": True,
            "all_scalar_features_must_be_finite_numbers": True,
        },
        "public_safety": {
            "private_material_publication_allowed": False,
            "forbidden_field_names": sorted(FORBIDDEN_FIELD_NAMES),
            "forbidden_payload_policy": "Any forbidden field anywhere in the submitted public record blocks intake.",
        },
        "acceptance_checks": acceptance_checks(),
        "task_templates": tasks,
    }


def submission_task_template(row: dict[str, Any]) -> dict[str, Any]:
    sample_count = int(row.get("target_samples_for_10pct_tv") or row.get("planned_sample_target") or 0)
    planned_sample_target = int(row.get("planned_sample_target") or 0)
    forbidden = list((row.get("collector_contract") or {}).get("must_not_publish") or [])
    return {
        "task_id": row.get("task_id"),
        "priority": row.get("priority"),
        "library": row.get("library"),
        "baseline_id": row.get("baseline_id"),
        "track": row.get("track"),
        "object_type": row.get("object_type"),
        "bit_length": row.get("bit_length"),
        "planned_sample_target": planned_sample_target,
        "target_samples_for_10pct_tv": sample_count,
        "minimum_replicates": (row.get("collector_contract") or {}).get("minimum_replicates"),
        "public_output": row.get("public_output"),
        "must_not_publish": sorted(set([*forbidden, *FORBIDDEN_FIELD_NAMES])),
        "submission_record_template": submission_record_template(row, sample_count),
    }


def submission_record_template(row: dict[str, Any], sample_count: int) -> dict[str, Any]:
    task_id = str(row.get("task_id") or "task-id")
    label = str(row.get("library") or row.get("baseline_id") or "real-world-baseline")
    bit_length = float(row.get("bit_length") or 0)
    return {
        "task_id": task_id,
        "sample_count": sample_count,
        "claim_scope": "real_world",
        "aggregate_artifact_sha256": "0" * 64,
        "provenance_record": {
            "baseline_id": row.get("baseline_id"),
            "library": row.get("library"),
            "source_commit": "<public source commit>",
            "build_config": "<public build flags>",
            "rng_source": "<public RNG description>",
            "generation_command": "<public command or reproducible recipe>",
        },
        "feature_vector_path": f"data/real_world/{task_id.replace(':', '_')}.feature.json",
        "feature_vector_summary": {
            "schema": FEATURE_VECTOR_VERSION,
            "id": f"{task_id}-feature-summary",
            "label": label,
            "record_count": sample_count,
            "features": {feature: example_feature_value(feature, bit_length, sample_count) for feature in SCALAR_FEATURES},
        },
    }


def example_feature_value(feature: str, bit_length: float, sample_count: int) -> float:
    if feature == "record_count_log2":
        return 0.0 if sample_count <= 0 else round(sample_count.bit_length() - 1, 6)
    if feature == "bit_length_mean":
        return bit_length
    if feature in {"bit_length_stddev", "low16_collision_rate", "next_prime_exposure_score"}:
        return 0.0
    if feature == "bit_length_entropy":
        return 0.0
    if feature == "bit_length_max_mass":
        return 1.0
    return 0.0


def acceptance_checks() -> list[dict[str, Any]]:
    return [
        {
            "code": "known_task",
            "blocks": True,
            "message": "task_id must match one collection handoff task.",
        },
        {
            "code": "single_submission_per_task",
            "blocks": True,
            "message": "Only one public aggregate submission per task_id is accepted in one intake run.",
        },
        {
            "code": "sample_floor",
            "blocks": True,
            "message": "sample_count must meet planned_sample_target; below the 10% TV floor remains screening_only.",
        },
        {
            "code": "checksum_integrity",
            "blocks": True,
            "message": "aggregate_artifact_sha256 must be a 64-character SHA-256 hex digest and not reused across task IDs.",
        },
        {
            "code": "provenance_record",
            "blocks": True,
            "message": "A public provenance_record must accompany the aggregate artifact.",
        },
        {
            "code": "feature_vector_contract",
            "blocks": True,
            "message": "feature_vector_summary must match schema, scalar features, record_count, and bit_length_mean constraints.",
        },
        {
            "code": "public_safety",
            "blocks": True,
            "message": "Private keys, raw primes, wallet seeds, raw key files, and raw signature owner fields must not appear.",
        },
    ]
