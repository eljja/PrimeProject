from __future__ import annotations

from random import Random
from typing import Any


NULL_CALIBRATION_SCHEMA = "primeproject.null-calibration.v1"


def build_null_calibration(
    *,
    attribution_grid: dict[str, Any],
    iterations: int = 5000,
    seed: int = 20260523,
) -> dict[str, Any]:
    if iterations < 100:
        raise ValueError("iterations must be at least 100")

    random_baseline = float(attribution_grid.get("random_baseline_accuracy", 0.0) or 0.0)
    if not 0 < random_baseline < 1:
        raise ValueError("attribution grid must include a random_baseline_accuracy between 0 and 1")

    controlled_rows = [
        row for row in attribution_grid.get("rows", [])
        if row.get("control_mode") == "bit_length"
    ]
    if not controlled_rows:
        raise ValueError("attribution grid must include bit_length controlled rows")

    profiles = sorted({
        profile
        for row in controlled_rows
        for profile in (row.get("profile_total") or {})
    })
    if not profiles:
        raise ValueError("controlled rows must include profile totals")

    observed = {
        profile: observed_profile_mean(controlled_rows, profile)
        for profile in profiles
    }
    rng = Random(seed)
    null_means = {profile: [] for profile in profiles}
    max_lifts = []
    for _ in range(iterations):
        iteration_lifts = []
        for profile in profiles:
            simulated_values = []
            for row in controlled_rows:
                total = int((row.get("profile_total") or {}).get(profile, 0) or 0)
                if total <= 0:
                    continue
                correct = binomial_sample(total, random_baseline, rng)
                simulated_values.append(correct / total)
            simulated_mean = mean(simulated_values)
            null_means[profile].append(simulated_mean)
            iteration_lifts.append(simulated_mean - random_baseline)
        max_lifts.append(max(iteration_lifts) if iteration_lifts else 0.0)

    profile_results = []
    for profile in profiles:
        null_values = sorted(null_means[profile])
        observed_mean = observed[profile]
        observed_lift = observed_mean - random_baseline
        pointwise_p = tail_probability(null_values, observed_mean)
        familywise_p = corrected_tail_count(
            sum(1 for lift in max_lifts if lift >= observed_lift),
            len(max_lifts),
        )
        profile_results.append(
            {
                "profile": profile,
                "observed_controlled_accuracy": round_float(observed_mean),
                "observed_lift": round_float(observed_lift),
                "null_mean": round_float(mean(null_values)),
                "null_ci95_low": round_float(quantile(null_values, 0.025)),
                "null_ci95_high": round_float(quantile(null_values, 0.975)),
                "pointwise_p_value": round_float(pointwise_p),
                "familywise_p_value": round_float(familywise_p),
                "interpretation": interpret_calibration(observed_lift, pointwise_p, familywise_p),
            }
        )

    profile_results.sort(key=lambda item: item["observed_lift"], reverse=True)
    significant = [item for item in profile_results if item["interpretation"] == "familywise_survives_null"]
    return {
        "schema": NULL_CALIBRATION_SCHEMA,
        "source": {
            "attribution_grid_schema": attribution_grid.get("schema"),
            "controlled_row_count": len(controlled_rows),
            "profile_count": len(profiles),
            "random_baseline_accuracy": random_baseline,
        },
        "method": {
            "name": "row-structured binomial null calibration",
            "iterations": iterations,
            "seed": seed,
            "familywise_control": "maximum observed lift across profiles per simulated iteration",
            "interpretation": "Controls for selecting the best-looking profile after observing multiple attribution profiles.",
        },
        "summary": {
            "profile_count": len(profile_results),
            "familywise_survivor_count": len(significant),
            "top_profile": profile_results[0]["profile"] if profile_results else None,
            "top_familywise_p_value": profile_results[0]["familywise_p_value"] if profile_results else None,
            "claim_floor": "controlled_synthetic_only",
        },
        "profiles": profile_results,
    }


def observed_profile_mean(rows: list[dict[str, Any]], profile: str) -> float:
    values = []
    for row in rows:
        totals = row.get("profile_total") or {}
        corrects = row.get("profile_correct") or {}
        total = int(totals.get(profile, 0) or 0)
        if total <= 0:
            continue
        values.append(float(corrects.get(profile, 0) or 0) / total)
    return mean(values)


def binomial_sample(total: int, probability: float, rng: Random) -> int:
    return sum(1 for _ in range(total) if rng.random() < probability)


def tail_probability(sorted_values: list[float], observed: float) -> float:
    if not sorted_values:
        return 1.0
    count = sum(1 for value in sorted_values if value >= observed)
    return corrected_tail_count(count, len(sorted_values))


def corrected_tail_count(count: int, total: int) -> float:
    if total <= 0:
        return 1.0
    return (count + 1) / (total + 1)


def interpret_calibration(observed_lift: float, pointwise_p: float, familywise_p: float) -> str:
    if observed_lift <= 0.10:
        return "near_null"
    if familywise_p <= 0.05:
        return "familywise_survives_null"
    if pointwise_p <= 0.05:
        return "pointwise_only"
    return "not_significant"


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def quantile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        return 0.0
    index = min(len(sorted_values) - 1, max(0, round((len(sorted_values) - 1) * probability)))
    return sorted_values[index]


def round_float(value: Any) -> float:
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return 0.0
