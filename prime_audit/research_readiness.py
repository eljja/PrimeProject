from __future__ import annotations

from typing import Any


RESEARCH_READINESS_SCHEMA = "primeproject.research-readiness.v1"

EXPECTED_REAL_BASELINES = {
    "openssl": "OpenSSL RSA owned prime baseline",
    "boringssl": "BoringSSL RSA owned prime baseline",
    "go crypto/rsa": "Go crypto/rsa owned prime baseline",
    "bitcoin": "Bitcoin Core or wallet signature metadata baseline",
}

ATTRIBUTION_BASELINE_OBJECT_TYPES = {
    "rsa-prime",
    "rsa-modulus",
    "dh-prime",
    "ecdsa-signature",
    "schnorr-signature",
}


def build_research_readiness_report(
    *,
    manifest: dict[str, Any],
    attribution_grid: dict[str, Any] | None = None,
    classifier_report: dict[str, Any] | None = None,
    bitcoin_risk_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sim_to_real = assess_sim_to_real(manifest)
    attribution = assess_attribution_validation(attribution_grid or {})
    classifier = assess_classifier(classifier_report or {})
    bitcoin = assess_bitcoin_integration(bitcoin_risk_report or {}, manifest)
    dimensions = {
        "sim_to_real": sim_to_real,
        "attribution_validation": attribution,
        "classifier": classifier,
        "bitcoin_integration": bitcoin,
    }
    weighted_score = (
        0.35 * sim_to_real["score"]
        + 0.25 * attribution["score"]
        + 0.25 * classifier["score"]
        + 0.15 * bitcoin["score"]
    )
    return {
        "schema": RESEARCH_READINESS_SCHEMA,
        "overall": {
            "score": round(weighted_score, 4),
            "label": readiness_label(weighted_score),
        },
        "dimensions": dimensions,
        "blocking_gaps": blocking_gaps(dimensions),
        "next_actions": next_actions(dimensions),
    }


def assess_sim_to_real(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("entries", [])
    status_counts = manifest.get("status_counts", {})
    library_text = " ".join(str(entry.get("library") or "").lower() for entry in entries)
    covered = {
        key: label
        for key, label in EXPECTED_REAL_BASELINES.items()
        if key in library_text
    }
    missing = {
        key: label
        for key, label in EXPECTED_REAL_BASELINES.items()
        if key not in covered
    }
    sensitive_count = sum(1 for entry in entries if entry.get("sensitive"))
    manifest_available_count = int(status_counts.get("available") or 0)
    available_count = sum(1 for entry in entries if is_available_attribution_baseline(entry))
    public_control_count = sum(
        1
        for entry in entries
        if entry.get("status") == "available" and not is_available_attribution_baseline(entry)
    )
    planned_count = int(status_counts.get("planned") or 0)
    local_only_count = int(status_counts.get("local-only") or 0)
    coverage_score = len(covered) / len(EXPECTED_REAL_BASELINES)
    availability_score = min(1.0, available_count / max(1, len(EXPECTED_REAL_BASELINES)))
    planning_score = min(1.0, (planned_count + local_only_count + available_count) / max(1, len(EXPECTED_REAL_BASELINES)))
    policy_score = 1.0 if not manifest.get("validation", {}).get("errors") else 0.0
    raw_score = 0.35 * coverage_score + 0.25 * availability_score + 0.25 * planning_score + 0.15 * policy_score
    gaps = []
    readiness_cap = None
    if missing:
        gaps.append(
            {
                "code": "missing_expected_baselines",
                "severity": "medium",
                "message": "Some target real-world baseline families are not registered.",
                "evidence": missing,
            }
        )
    if available_count < 2:
        gaps.append(
            {
                "code": "insufficient_available_real_baselines",
                "severity": "high",
                "message": "At least two available aggregate generator baselines are needed before real attribution claims.",
                "evidence": {
                    "available_count": available_count,
                    "manifest_available_count": manifest_available_count,
                    "public_control_count": public_control_count,
                },
            }
        )
        readiness_cap = {
            "max_score": 0.54,
            "max_label": "scaffold_ready",
            "reason": "Sim-to-real evidence cannot be research-ready until at least two aggregate generator baselines are available; public constants count only as controls.",
        }
    score = min(raw_score, readiness_cap["max_score"]) if readiness_cap else raw_score
    return {
        "score": round(score, 4),
        "label": readiness_label(score),
        "raw_score": round(raw_score, 4),
        "readiness_cap": readiness_cap,
        "registered_count": len(entries),
        "available_count": available_count,
        "manifest_available_count": manifest_available_count,
        "public_control_count": public_control_count,
        "planned_count": planned_count,
        "local_only_count": local_only_count,
        "sensitive_count": sensitive_count,
        "expected_coverage": covered,
        "gaps": gaps,
    }


def is_available_attribution_baseline(entry: dict[str, Any]) -> bool:
    if entry.get("status") != "available":
        return False
    if entry.get("source_type") == "public-standard":
        return False
    if entry.get("object_type") not in ATTRIBUTION_BASELINE_OBJECT_TYPES:
        return False
    return int(entry.get("sample_count") or 0) > 0


def assess_attribution_validation(grid: dict[str, Any]) -> dict[str, Any]:
    if not grid:
        return {
            "score": 0.0,
            "label": "not_started",
            "rows": 0,
            "repeats": 0,
            "robust_profiles": [],
            "gaps": [
                {
                    "code": "missing_attribution_grid",
                    "severity": "medium",
                    "message": "No paired attribution grid was provided.",
                }
            ],
        }
    profiles = grid.get("summary", {}).get("profiles", {})
    robust = [
        name
        for name, value in profiles.items()
        if str(value.get("robust_interpretation") or "").startswith("robust_survives")
    ]
    significant = [
        name
        for name, value in profiles.items()
        if value.get("controlled_significance", {}).get("label") in {"significant", "strong"}
    ]
    repeats = int(grid.get("repeats") or 0)
    rows = len(grid.get("rows", []))
    score = min(1.0, 0.20 + 0.20 * min(repeats, 3) / 3 + 0.20 * min(rows, 24) / 24 + 0.40 * min(len(robust), 2) / 2)
    gaps = []
    if not robust:
        gaps.append(
            {
                "code": "no_robust_controlled_profile",
                "severity": "medium",
                "message": "No fingerprint profile is yet robust after bit-length control.",
            }
        )
    if repeats < 3:
        gaps.append(
            {
                "code": "low_repeat_count",
                "severity": "low",
                "message": "Increase repeats for tighter confidence intervals.",
                "evidence": {"repeats": repeats},
            }
        )
    return {
        "score": round(score, 4),
        "label": readiness_label(score),
        "rows": rows,
        "repeats": repeats,
        "profile_count": len(profiles),
        "robust_profiles": robust,
        "significant_profiles": significant,
        "gaps": gaps,
    }


def assess_classifier(report: dict[str, Any]) -> dict[str, Any]:
    if not report:
        return {
            "score": 0.0,
            "label": "not_started",
            "vector_count": 0,
            "label_count": 0,
            "accuracy": None,
            "gaps": [
                {
                    "code": "missing_classifier_report",
                    "severity": "high",
                    "message": "No classifier report is bundled yet.",
                }
            ],
        }
    vector_count = int(report.get("usable_vector_count") or report.get("vector_count") or 0)
    label_count = int(report.get("label_count") or 0)
    total = int(report.get("total") or 0)
    claim_scope = str(report.get("claim_scope") or "unspecified")
    accuracy = report.get("accuracy")
    accuracy_score = float(accuracy) if accuracy is not None else 0.0
    sample_score = min(1.0, vector_count / 24)
    label_score = min(1.0, label_count / 4)
    trial_score = min(1.0, total / 24)
    score = 0.25 * sample_score + 0.25 * label_score + 0.25 * trial_score + 0.25 * accuracy_score
    gaps = []
    real_world_claim_ready = claim_scope == "real_world"
    if not real_world_claim_ready:
        score = min(score, 0.49)
        gaps.append(
            {
                "code": "classifier_scope_not_real_world",
                "severity": "high",
                "message": "Bundled classifier evidence is not scoped to real-world library attribution.",
                "evidence": {"claim_scope": claim_scope},
            }
        )
    if label_count < 3:
        gaps.append(
            {
                "code": "low_label_count",
                "severity": "high",
                "message": "Classifier needs at least three real labels to be useful for attribution.",
                "evidence": {"label_count": label_count},
            }
        )
    if vector_count < 12:
        gaps.append(
            {
                "code": "low_vector_count",
                "severity": "medium",
                "message": "Classifier vector count is too small for stable conclusions.",
                "evidence": {"vector_count": vector_count},
            }
        )
    return {
        "score": round(score, 4),
        "label": readiness_label(score),
        "vector_count": vector_count,
        "label_count": label_count,
        "claim_scope": claim_scope,
        "real_world_claim_ready": real_world_claim_ready,
        "accuracy": accuracy,
        "total": total,
        "gaps": gaps,
    }


def assess_bitcoin_integration(report: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    related_count = 0
    if report:
        related_count = len(report.get("related_baselines", []))
    else:
        text = " ".join(
            str(entry.get(field) or "")
            for entry in manifest.get("entries", [])
            for field in ("baseline_id", "library", "algorithm", "object_type")
        ).lower()
        related_count = int("bitcoin" in text or "secp256k1" in text)
    score = 0.0
    if related_count:
        score += 0.35
    if report:
        score += 0.35
        if report.get("nonce_fingerprint"):
            score += 0.30
    gaps = []
    if not report:
        gaps.append(
            {
                "code": "missing_bitcoin_risk_report",
                "severity": "medium",
                "message": "Bitcoin signature audit is not yet connected to a bundled risk report.",
            }
        )
    if not related_count:
        gaps.append(
            {
                "code": "missing_bitcoin_baseline",
                "severity": "medium",
                "message": "No Bitcoin or secp256k1 baseline is registered.",
            }
        )
    return {
        "score": round(min(score, 1.0), 4),
        "label": readiness_label(min(score, 1.0)),
        "risk_level": report.get("risk_level") if report else None,
        "related_baseline_count": related_count,
        "gaps": gaps,
    }


def blocking_gaps(dimensions: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    gaps = []
    for dimension, payload in dimensions.items():
        for gap in payload.get("gaps", []):
            if gap.get("severity") in {"high", "critical"}:
                gaps.append({"dimension": dimension, **gap})
    return gaps


def next_actions(dimensions: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    actions = []
    if dimensions["sim_to_real"]["available_count"] < 2:
        actions.append(
            {
                "priority": "P0",
                "track": "sim-to-real",
                "action": "Generate at least two local owned-library aggregate baselines with matched bit-length and sample counts.",
            }
        )
    if not dimensions["classifier"].get("real_world_claim_ready"):
        actions.append(
            {
                "priority": "P0",
                "track": "classifier",
                "action": "Export real-world labelled feature vectors for OpenSSL, BoringSSL, Go, and a suspicious sample before trusting classifier output.",
            }
        )
    if not dimensions["attribution_validation"]["robust_profiles"]:
        actions.append(
            {
                "priority": "P1",
                "track": "controlled-attribution",
                "action": "Expand attribution-grid repeats and limits until at least one profile survives bit-length control.",
            }
        )
    if dimensions["bitcoin_integration"]["score"] < 0.7:
        actions.append(
            {
                "priority": "P1",
                "track": "bitcoin",
                "action": "Bundle a Bitcoin risk report from owned or public metadata summaries and compare it with registered baselines.",
            }
        )
    return actions


def readiness_label(score: float) -> str:
    if score >= 0.80:
        return "research_ready"
    if score >= 0.55:
        return "prototype_ready"
    if score >= 0.30:
        return "scaffold_ready"
    return "not_started"
