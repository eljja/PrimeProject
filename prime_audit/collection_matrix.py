from __future__ import annotations

from typing import Any


COLLECTION_MATRIX_SCHEMA = "primeproject.real-world-collection-matrix.v1"

RSA_BIT_LENGTHS = [2048, 3072, 4096]
RSA_SAMPLE_TARGET = 500
SIGNATURE_SAMPLE_TARGET = 10000


def build_collection_matrix(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("entries", [])
    rows = [
        rsa_collection_row(entries, "OpenSSL", "openssl-rsa-prime-owned"),
        rsa_collection_row(entries, "BoringSSL", "boringssl-rsa-prime-owned"),
        rsa_collection_row(entries, "Go crypto/rsa", "go-crypto-rsa-prime-owned"),
        signature_collection_row(entries),
    ]
    total_targets = sum(len(row["targets"]) for row in rows)
    complete_targets = sum(1 for row in rows for target in row["targets"] if target["status"] == "available")
    blocked_targets = total_targets - complete_targets
    local_sensitive_count = sum(1 for row in rows if row["sensitive"])
    available_rsa_libraries = sum(
        1
        for row in rows
        if row["track"] == "rsa-prime-generation"
        and any(target["status"] == "available" for target in row["targets"])
    )
    return {
        "schema": COLLECTION_MATRIX_SCHEMA,
        "sample_handling": {
            "raw_private_material_public": False,
            "aggregate_fingerprints_public": True,
            "minimum_replicates_per_label": 3,
            "publication_unit": "aggregate fingerprint, baseline JSON, and feature vector only",
        },
        "row_count": len(rows),
        "target_count": total_targets,
        "complete_target_count": complete_targets,
        "blocked_target_count": blocked_targets,
        "local_sensitive_count": local_sensitive_count,
        "completion_ratio": complete_targets / total_targets if total_targets else 0.0,
        "claim_gate": {
            "status": "open" if available_rsa_libraries >= 2 else "blocked",
            "available_rsa_libraries": available_rsa_libraries,
            "minimum_available_rsa_libraries": 2,
            "minimum_label_replicates": 3,
            "message": "Real-world attribution remains blocked until at least two aggregate RSA library baselines and labelled classifier replicates exist.",
        },
        "rows": rows,
        "next_unlock": next_unlock(rows),
    }


def rsa_collection_row(entries: list[dict[str, Any]], library: str, baseline_id: str) -> dict[str, Any]:
    entry = find_entry(entries, baseline_id)
    targets = [
        {
            "bit_length": bit_length,
            "sample_target": RSA_SAMPLE_TARGET,
            "object_type": "rsa-prime",
            "status": target_status(entry, bit_length),
            "public_output": "aggregate fingerprint + baseline + feature vector",
        }
        for bit_length in RSA_BIT_LENGTHS
    ]
    return {
        "library": library,
        "baseline_id": baseline_id,
        "track": "rsa-prime-generation",
        "sensitive": bool(entry.get("sensitive", True)),
        "targets": targets,
    }


def signature_collection_row(entries: list[dict[str, Any]]) -> dict[str, Any]:
    baseline_id = "bitcoin-core-ecdsa-signature-public"
    entry = find_entry(entries, baseline_id)
    return {
        "library": "Bitcoin Core / wallet metadata",
        "baseline_id": baseline_id,
        "track": "signature-nonce-metadata",
        "sensitive": bool(entry.get("sensitive", False)),
        "targets": [
            {
                "bit_length": 256,
                "sample_target": SIGNATURE_SAMPLE_TARGET,
                "object_type": "ecdsa-signature",
                "status": target_status(entry, 256),
                "public_output": "nonce-risk summary + distribution fingerprint",
            }
        ],
    }


def find_entry(entries: list[dict[str, Any]], baseline_id: str) -> dict[str, Any]:
    for entry in entries:
        if entry.get("baseline_id") == baseline_id:
            return entry
    return {}


def target_status(entry: dict[str, Any], bit_length: int) -> str:
    if entry.get("status") != "available":
        return entry.get("status") or "planned"
    entry_bit_length = entry.get("bit_length")
    if entry_bit_length == bit_length and int(entry.get("sample_count") or 0) > 0:
        return "available"
    return "planned"


def next_unlock(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_rsa = [
        {"library": row["library"], "bit_length": target["bit_length"], "sample_target": target["sample_target"]}
        for row in rows
        if row["track"] == "rsa-prime-generation"
        for target in row["targets"]
        if target["status"] != "available"
    ]
    return [
        {
            "gate": "real_baseline_gate",
            "need": "two available aggregate RSA library baselines",
            "candidate_targets": missing_rsa[:6],
        },
        {
            "gate": "classifier_gate",
            "need": "labelled feature vectors from at least three library families",
            "candidate_targets": missing_rsa[:9],
        },
    ]
