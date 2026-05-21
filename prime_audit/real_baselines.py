from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REAL_BASELINE_MANIFEST_SCHEMA = "primeproject.real-world-baseline-manifest.v1"

VALID_OBJECT_TYPES = {
    "rsa-prime",
    "rsa-modulus",
    "dh-prime",
    "ecc-field-prime",
    "ecc-group-order",
    "ecdsa-signature",
    "schnorr-signature",
    "synthetic-prime",
}
VALID_SOURCE_TYPES = {
    "owned-sample",
    "generated-local",
    "public-standard",
    "public-chain",
    "fixture",
    "synthetic",
}
VALID_STATUSES = {"planned", "available", "local-only"}

DEFAULT_REAL_BASELINE_ENTRIES: list[dict[str, Any]] = [
    {
        "baseline_id": "openssl-rsa-prime-owned",
        "library": "OpenSSL",
        "library_version": "owned-lab",
        "algorithm": "RSA",
        "object_type": "rsa-prime",
        "source_type": "owned-sample",
        "sample_count": 0,
        "bit_length": None,
        "fingerprint_path": None,
        "baseline_path": None,
        "license": "Apache-2.0-compatible-summary-only",
        "sensitive": True,
        "status": "planned",
        "notes": "Generate locally from owned keys; publish only aggregate fingerprints.",
    },
    {
        "baseline_id": "boringssl-rsa-prime-owned",
        "library": "BoringSSL",
        "library_version": "owned-lab",
        "algorithm": "RSA",
        "object_type": "rsa-prime",
        "source_type": "owned-sample",
        "sample_count": 0,
        "bit_length": None,
        "fingerprint_path": None,
        "baseline_path": None,
        "license": "Apache-2.0-compatible-summary-only",
        "sensitive": True,
        "status": "planned",
        "notes": "Generate locally from owned keys; compare against OpenSSL and Go baselines.",
    },
    {
        "baseline_id": "go-crypto-rsa-prime-owned",
        "library": "Go crypto/rsa",
        "library_version": "owned-lab",
        "algorithm": "RSA",
        "object_type": "rsa-prime",
        "source_type": "owned-sample",
        "sample_count": 0,
        "bit_length": None,
        "fingerprint_path": None,
        "baseline_path": None,
        "license": "Apache-2.0-compatible-summary-only",
        "sensitive": True,
        "status": "planned",
        "notes": "Generate locally with reproducible build metadata and publish aggregate output only.",
    },
    {
        "baseline_id": "bitcoin-core-ecdsa-signature-public",
        "library": "Bitcoin Core / secp256k1 ecosystem",
        "library_version": "public-chain-or-owned-wallet",
        "algorithm": "ECDSA-secp256k1",
        "object_type": "ecdsa-signature",
        "source_type": "public-chain",
        "sample_count": 0,
        "bit_length": 256,
        "fingerprint_path": None,
        "baseline_path": None,
        "license": "public-metadata-summary-only",
        "sensitive": False,
        "status": "planned",
        "notes": "Use signature metadata only; do not publish private keys or wallet seeds.",
    },
    {
        "baseline_id": "bitcoin-secp256k1-constants",
        "library": "Bitcoin secp256k1",
        "library_version": "public-standard",
        "algorithm": "secp256k1",
        "object_type": "ecc-field-prime",
        "source_type": "public-standard",
        "sample_count": 2,
        "bit_length": 256,
        "fingerprint_path": None,
        "baseline_path": None,
        "license": "public-domain-math-constant",
        "sensitive": False,
        "status": "available",
        "notes": "Public field prime p and group order n are useful controls, not secret targets.",
    },
]


def build_real_baseline_manifest(
    entries: list[dict[str, Any]] | None = None,
    *,
    include_default_entries: bool = True,
    created_at: str | None = None,
) -> dict[str, Any]:
    merged = []
    if include_default_entries:
        merged.extend(dict(entry) for entry in DEFAULT_REAL_BASELINE_ENTRIES)
    if entries:
        merged.extend(dict(entry) for entry in entries)

    normalized = [normalize_real_baseline_entry(entry) for entry in merged]
    errors = validate_real_baseline_entries(normalized)
    status_counts: dict[str, int] = {}
    for entry in normalized:
        status = entry["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "schema": REAL_BASELINE_MANIFEST_SCHEMA,
        "created_at": created_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "entry_count": len(normalized),
        "status_counts": status_counts,
        "entries": normalized,
        "validation": {
            "passed": not errors,
            "errors": errors,
        },
        "handling_policy": {
            "publish_sensitive_material": False,
            "publish_private_primes": False,
            "publish_aggregate_fingerprints": True,
            "local_generation_required_for_owned_samples": True,
        },
    }


def load_real_baseline_entries(paths: list[str | Path]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(payload, dict) and "entries" in payload:
            entries.extend(payload["entries"])
        elif isinstance(payload, list):
            entries.extend(payload)
        elif isinstance(payload, dict):
            entries.append(payload)
        else:
            raise ValueError(f"Unsupported baseline entry payload in {path}")
    return entries


def normalize_real_baseline_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "baseline_id": str(entry.get("baseline_id") or "").strip(),
        "library": str(entry.get("library") or "").strip(),
        "library_version": str(entry.get("library_version") or "unknown").strip(),
        "algorithm": str(entry.get("algorithm") or "").strip(),
        "object_type": str(entry.get("object_type") or "").strip(),
        "source_type": str(entry.get("source_type") or "").strip(),
        "sample_count": int(entry.get("sample_count") or 0),
        "bit_length": entry.get("bit_length"),
        "fingerprint_path": entry.get("fingerprint_path"),
        "baseline_path": entry.get("baseline_path"),
        "license": str(entry.get("license") or "unknown").strip(),
        "sensitive": bool(entry.get("sensitive", False)),
        "status": str(entry.get("status") or "planned").strip(),
        "notes": str(entry.get("notes") or "").strip(),
    }
    if normalized["bit_length"] is not None:
        normalized["bit_length"] = int(normalized["bit_length"])
    return normalized


def validate_real_baseline_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        baseline_id = entry.get("baseline_id")
        if not baseline_id:
            errors.append(_entry_error(index, baseline_id, "missing_baseline_id"))
        elif baseline_id in seen:
            errors.append(_entry_error(index, baseline_id, "duplicate_baseline_id"))
        seen.add(str(baseline_id))

        for field in ("library", "algorithm"):
            if not entry.get(field):
                errors.append(_entry_error(index, baseline_id, f"missing_{field}"))
        if entry.get("object_type") not in VALID_OBJECT_TYPES:
            errors.append(_entry_error(index, baseline_id, "invalid_object_type"))
        if entry.get("source_type") not in VALID_SOURCE_TYPES:
            errors.append(_entry_error(index, baseline_id, "invalid_source_type"))
        if entry.get("status") not in VALID_STATUSES:
            errors.append(_entry_error(index, baseline_id, "invalid_status"))
        if int(entry.get("sample_count") or 0) < 0:
            errors.append(_entry_error(index, baseline_id, "negative_sample_count"))
        if entry.get("bit_length") is not None and int(entry["bit_length"]) <= 0:
            errors.append(_entry_error(index, baseline_id, "invalid_bit_length"))
        if entry.get("status") == "available" and entry.get("sample_count", 0) == 0:
            errors.append(_entry_error(index, baseline_id, "available_without_samples"))
        if entry.get("sensitive") and entry.get("status") == "available":
            errors.append(_entry_error(index, baseline_id, "sensitive_available_public_manifest"))
    return errors


def manifest_public_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("entries", [])
    return {
        "schema": "primeproject.real-world-baseline-summary.v1",
        "entry_count": len(entries),
        "available_count": sum(1 for entry in entries if entry.get("status") == "available"),
        "planned_count": sum(1 for entry in entries if entry.get("status") == "planned"),
        "local_only_count": sum(1 for entry in entries if entry.get("status") == "local-only"),
        "libraries": sorted({entry.get("library") for entry in entries if entry.get("library")}),
        "object_types": sorted({entry.get("object_type") for entry in entries if entry.get("object_type")}),
    }


def _entry_error(index: int, baseline_id: Any, code: str) -> dict[str, Any]:
    return {
        "index": index,
        "baseline_id": baseline_id,
        "code": code,
    }
