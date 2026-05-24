from __future__ import annotations

import math
from statistics import NormalDist
from typing import Any


COLLECTION_POWER_SCHEMA = "primeproject.collection-power.v1"
SENSITIVITY_ALPHA_VALUES = (0.10, 0.05, 0.01, 0.001)
SENSITIVITY_TARGET_TV_VALUES = (0.20, 0.10, 0.05)


def build_collection_power(
    matrix: dict[str, Any],
    *,
    modulo: int = 210,
    alpha: float = 0.05,
    target_tv: float = 0.10,
) -> dict[str, Any]:
    validate_power_parameters(modulo=modulo, alpha=alpha, target_tv=target_tv)
    rows = [
        target_power(row, target, modulo=modulo, alpha=alpha, target_tv=target_tv)
        for row in matrix.get("rows", [])
        for target in row.get("targets", [])
    ]
    coarse = sum(1 for row in rows if row["power_tier"] == "coarse")
    screening = sum(1 for row in rows if row["power_tier"] == "screening")
    strong = sum(1 for row in rows if row["power_tier"] == "strong")
    sensitivity_rows = build_sensitivity_grid(rows)
    return {
        "schema": COLLECTION_POWER_SCHEMA,
        "method": {
            "name": "multinomial screening floor",
            "alpha": alpha,
            "target_tv": target_tv,
            "target_tv_label": tv_label(target_tv),
            "modulo": modulo,
            "interpretation": "This is a conservative planning heuristic for aggregate fingerprints, not a proof of generator attribution.",
        },
        "summary": {
            "target_count": len(rows),
            "coarse_count": coarse,
            "screening_count": screening,
            "strong_count": strong,
            "minimum_recommended_replicates": matrix.get("sample_handling", {}).get("minimum_replicates_per_label", 3),
            "weakest_targets": weakest_targets(rows),
        },
        "rows": rows,
        "sensitivity": {
            "alpha_values": list(SENSITIVITY_ALPHA_VALUES),
            "target_tv_values": list(SENSITIVITY_TARGET_TV_VALUES),
            "rows": sensitivity_rows,
        },
        "recommendations": recommendations(rows),
    }


def target_power(
    collection_row: dict[str, Any],
    target: dict[str, Any],
    *,
    modulo: int,
    alpha: float,
    target_tv: float,
) -> dict[str, Any]:
    sample_target = max(1, int(target.get("sample_target") or 0))
    bucket_count = bucket_count_for_target(target, modulo)
    z_score = normal_z_for_two_sided_alpha(alpha)
    class_probability = 1.0 / bucket_count
    class_shift_95 = z_score * math.sqrt(class_probability * (1.0 - class_probability) / sample_target)
    typical_tv_noise_floor = math.sqrt((bucket_count - 1) / (4.0 * sample_target))
    conservative_tv_floor_95 = z_score * typical_tv_noise_floor
    min_samples_for_target_tv = minimum_samples_for_tv_floor(
        bucket_count=bucket_count,
        z_score=z_score,
        target_tv=target_tv,
    )
    min_samples_for_10pct_tv = minimum_samples_for_tv_floor(
        bucket_count=bucket_count,
        z_score=z_score,
        target_tv=0.10,
    )
    tier = power_tier(conservative_tv_floor_95)
    return {
        "library": collection_row.get("library"),
        "track": collection_row.get("track"),
        "object_type": target.get("object_type"),
        "bit_length": target.get("bit_length"),
        "sample_target": sample_target,
        "bucket_count": bucket_count,
        "status": target.get("status", "planned"),
        "power_tier": tier,
        "class_shift_95": round(class_shift_95, 6),
        "typical_tv_noise_floor": round(typical_tv_noise_floor, 6),
        "conservative_tv_floor_95": round(conservative_tv_floor_95, 6),
        "target_tv": target_tv,
        "target_tv_label": tv_label(target_tv),
        "min_samples_for_target_tv": min_samples_for_target_tv,
        "sample_gap_to_target_tv": max(0, min_samples_for_target_tv - sample_target),
        "min_samples_for_10pct_tv": min_samples_for_10pct_tv,
        "sample_gap_to_10pct_tv": max(0, min_samples_for_10pct_tv - sample_target),
    }


def bucket_count_for_target(target: dict[str, Any], modulo: int) -> int:
    if target.get("object_type") == "rsa-prime":
        return euler_phi(modulo)
    if target.get("object_type") == "ecdsa-signature":
        return 64
    return max(8, euler_phi(modulo))


def euler_phi(value: int) -> int:
    result = value
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            while remaining % candidate == 0:
                remaining //= candidate
            result -= result // candidate
        candidate += 1
    if remaining > 1:
        result -= result // remaining
    return result


def normal_z_for_two_sided_alpha(alpha: float) -> float:
    if not math.isfinite(alpha) or alpha <= 0 or alpha >= 1:
        raise ValueError("alpha must be between 0 and 1")
    return NormalDist().inv_cdf(1.0 - alpha / 2.0)


def validate_power_parameters(*, modulo: int, alpha: float, target_tv: float) -> None:
    if modulo < 2:
        raise ValueError("modulo must be at least 2")
    normal_z_for_two_sided_alpha(alpha)
    if not math.isfinite(target_tv) or target_tv <= 0 or target_tv >= 1:
        raise ValueError("target_tv must be between 0 and 1")


def minimum_samples_for_tv_floor(*, bucket_count: int, z_score: float, target_tv: float) -> int:
    return math.ceil((z_score**2 * (bucket_count - 1)) / (4.0 * target_tv**2))


def tv_label(target_tv: float) -> str:
    percentage = target_tv * 100
    if abs(percentage - round(percentage)) < 1e-9:
        return f"{int(round(percentage))}pct"
    label = f"{percentage:.3f}".rstrip("0").rstrip(".")
    return f"{label.replace('.', '_')}pct"


def build_sensitivity_grid(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for row in rows:
        object_type = str(row.get("object_type") or "unknown")
        current = profiles.get(object_type)
        sample_target = int(row.get("sample_target") or 0)
        if not current or sample_target > int(current.get("planned_sample_target") or 0):
            profiles[object_type] = {
                "object_type": object_type,
                "bucket_count": int(row.get("bucket_count") or 0),
                "planned_sample_target": sample_target,
            }

    sensitivity = []
    for profile in sorted(profiles.values(), key=lambda item: str(item["object_type"])):
        bucket_count = int(profile["bucket_count"])
        planned_sample_target = int(profile["planned_sample_target"])
        for alpha in SENSITIVITY_ALPHA_VALUES:
            z_score = normal_z_for_two_sided_alpha(alpha)
            for target_tv in SENSITIVITY_TARGET_TV_VALUES:
                min_samples = minimum_samples_for_tv_floor(
                    bucket_count=bucket_count,
                    z_score=z_score,
                    target_tv=target_tv,
                )
                sensitivity.append(
                    {
                        "object_type": profile["object_type"],
                        "bucket_count": bucket_count,
                        "planned_sample_target": planned_sample_target,
                        "alpha": alpha,
                        "target_tv": target_tv,
                        "target_tv_label": tv_label(target_tv),
                        "min_samples": min_samples,
                        "sample_gap_vs_planned_target": max(0, min_samples - planned_sample_target),
                    }
                )
    return sensitivity


def power_tier(conservative_tv_floor_95: float) -> str:
    if conservative_tv_floor_95 <= 0.10:
        return "strong"
    if conservative_tv_floor_95 <= 0.20:
        return "screening"
    return "coarse"


def weakest_targets(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "library": row["library"],
            "bit_length": row["bit_length"],
            "sample_target": row["sample_target"],
            "conservative_tv_floor_95": row["conservative_tv_floor_95"],
            "target_tv_label": row["target_tv_label"],
            "min_samples_for_target_tv": row["min_samples_for_target_tv"],
            "min_samples_for_10pct_tv": row["min_samples_for_10pct_tv"],
        }
        for row in sorted(rows, key=lambda item: item["conservative_tv_floor_95"], reverse=True)[:3]
    ]


def recommendations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    needs_more = [row for row in rows if row["sample_gap_to_target_tv"] > 0]
    rsa_gaps = [row for row in needs_more if row["object_type"] == "rsa-prime"]
    signature_gaps = [row for row in needs_more if row["object_type"] == "ecdsa-signature"]
    actions = []
    if rsa_gaps:
        max_needed = max(row["min_samples_for_target_tv"] for row in rsa_gaps)
        target_label = tv_display(float(rsa_gaps[0].get("target_tv") or 0.10))
        actions.append(
            {
                "priority": "P0",
                "track": "rsa-prime-generation",
                "action": f"Treat 500 RSA primes per bit length as coarse screening; target about {max_needed} primes per library/bit-length for conservative {target_label} TV drift claims.",
            }
        )
    if signature_gaps:
        max_needed = max(row["min_samples_for_target_tv"] for row in signature_gaps)
        target_label = tv_display(float(signature_gaps[0].get("target_tv") or 0.10))
        actions.append(
            {
                "priority": "P1",
                "track": "signature-nonce-metadata",
                "action": f"Raise signature metadata targets toward {max_needed} rows when nonce-bucket claims need conservative {target_label} TV resolution.",
            }
        )
    if not actions:
        actions.append(
            {
                "priority": "P1",
                "track": "publication",
                "action": "Current sample targets clear the conservative planning floor; focus on independent replicates and provenance metadata.",
            }
        )
    return actions


def tv_display(target_tv: float) -> str:
    percentage = target_tv * 100
    if abs(percentage - round(percentage)) < 1e-9:
        return f"{int(round(percentage))}%"
    return f"{percentage:.3f}".rstrip("0").rstrip(".") + "%"
