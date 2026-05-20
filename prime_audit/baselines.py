from __future__ import annotations

from math import sqrt
from typing import Any


BASELINE_SCHEMA = "primeproject.generator-baseline.v1"
COMPARISON_SCHEMA = "primeproject.generator-baseline-comparison.v1"
MIN_RECOMMENDED_RECORDS = 30
STRONG_RECOMMENDED_RECORDS = 200


def build_generator_baseline(
    fingerprint_report: dict[str, Any],
    *,
    name: str,
    source: str | None = None,
) -> dict[str, Any]:
    aggregate = fingerprint_report.get("aggregate", {})
    quality = sample_quality(fingerprint_report)
    return {
        "schema": BASELINE_SCHEMA,
        "name": name,
        "source": source,
        "record_count": fingerprint_report.get("record_count", aggregate.get("record_count", 0)),
        "quality": quality,
        "features": baseline_features(aggregate),
    }


def compare_fingerprint_to_baselines(
    fingerprint_report: dict[str, Any],
    baselines: list[dict[str, Any]],
) -> dict[str, Any]:
    target_features = baseline_features(fingerprint_report.get("aggregate", {}))
    target_quality = sample_quality(fingerprint_report)
    comparisons = [
        compare_feature_vectors(target_features, baseline.get("features", {}), baseline, target_quality)
        for baseline in baselines
    ]
    comparisons.sort(key=lambda item: item["distance"])
    return {
        "schema": COMPARISON_SCHEMA,
        "target_record_count": fingerprint_report.get("record_count", 0),
        "target_quality": target_quality,
        "baseline_count": len(baselines),
        "nearest_baseline": comparisons[0] if comparisons else None,
        "comparisons": comparisons,
        "findings": comparison_findings(comparisons),
    }


def baseline_features(aggregate: dict[str, Any]) -> dict[str, Any]:
    signals = aggregate.get("generator_signals", {})
    gaps = aggregate.get("gap_statistics", {})
    return {
        "bit_length_distribution": normalize_counts(aggregate.get("bit_lengths", {})),
        "residue_total_variation": numeric_map(aggregate.get("residue_total_variation", {})),
        "low16_collision_rate": signals.get(
            "low16_collision_rate",
            1 - float(aggregate.get("low16_unique_ratio", 1.0) or 0.0),
        ),
        "next_prime_exposure_score": signals.get("next_prime_exposure_score"),
        "mean_left_gap_over_logp": gaps.get("mean_left_gap_over_logp"),
        "mean_right_gap_over_logp": gaps.get("mean_right_gap_over_logp"),
        "large_left_gap_ratio": safe_ratio(gaps.get("large_left_gap_records"), gaps.get("covered_records")),
        "max_residue_tv": signals.get("max_residue_tv"),
    }


def compare_feature_vectors(
    target: dict[str, Any],
    baseline: dict[str, Any],
    baseline_metadata: dict[str, Any],
    target_quality: dict[str, Any] | None = None,
) -> dict[str, Any]:
    components = {
        "bit_length": distribution_l1(
            target.get("bit_length_distribution", {}),
            baseline.get("bit_length_distribution", {}),
        ),
        "residue_tv": numeric_map_distance(
            target.get("residue_total_variation", {}),
            baseline.get("residue_total_variation", {}),
        ),
        "low16_collision": scalar_distance(
            target.get("low16_collision_rate"),
            baseline.get("low16_collision_rate"),
            scale=1.0,
        ),
        "next_prime_exposure": scalar_distance(
            target.get("next_prime_exposure_score"),
            baseline.get("next_prime_exposure_score"),
            scale=3.0,
        ),
        "right_gap": scalar_distance(
            target.get("mean_right_gap_over_logp"),
            baseline.get("mean_right_gap_over_logp"),
            scale=3.0,
        ),
        "large_left_gap": scalar_distance(
            target.get("large_left_gap_ratio"),
            baseline.get("large_left_gap_ratio"),
            scale=1.0,
        ),
    }
    weights = {
        "bit_length": 0.18,
        "residue_tv": 0.22,
        "low16_collision": 0.18,
        "next_prime_exposure": 0.18,
        "right_gap": 0.10,
        "large_left_gap": 0.14,
    }
    distance = sqrt(sum(weights[key] * (components[key] ** 2) for key in components))
    baseline_quality = baseline_metadata.get("quality") or quality_from_baseline_metadata(baseline_metadata, baseline)
    target_overall = (target_quality or {}).get("overall_confidence", 0.0)
    baseline_overall = baseline_quality.get("overall_confidence", 0.0)
    confidence = sqrt(target_overall * baseline_overall)
    return {
        "baseline_name": baseline_metadata.get("name"),
        "baseline_source": baseline_metadata.get("source"),
        "baseline_record_count": baseline_metadata.get("record_count"),
        "distance": distance,
        "similarity": max(0.0, 1.0 - distance),
        "confidence": confidence,
        "baseline_quality": baseline_quality,
        "components": components,
    }


def comparison_findings(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not comparisons:
        return [
            {
                "check": "missing_baselines",
                "severity": "high",
                "message": "No generator baselines were provided for comparison.",
            }
        ]
    nearest = comparisons[0]
    findings: list[dict[str, Any]] = []
    if nearest.get("confidence", 0.0) < 0.35:
        findings.append(
            {
                "check": "low_confidence_baseline_match",
                "severity": "low",
                "message": "Nearest baseline match is based on limited sample quality; treat attribution as tentative.",
                "evidence": {
                    "nearest_baseline": nearest["baseline_name"],
                    "confidence": nearest.get("confidence", 0.0),
                },
            }
        )
    if nearest["distance"] >= 0.45:
        findings.append(
            {
                "check": "out_of_baseline_distribution",
                "severity": "medium",
                "message": "Target fingerprint is far from the nearest baseline; review generator provenance.",
                "evidence": {
                    "nearest_baseline": nearest["baseline_name"],
                    "distance": nearest["distance"],
                    "confidence": nearest.get("confidence", 0.0),
                },
            }
        )
    weak_components = {
        key: value
        for key, value in nearest["components"].items()
        if value >= 0.35
    }
    if weak_components:
        findings.append(
            {
                "check": "baseline_component_drift",
                "severity": "low",
                "message": "One or more fingerprint components drift from the nearest baseline.",
                "evidence": weak_components,
            }
        )
    return findings


def normalize_counts(counts: dict[str, Any]) -> dict[str, float]:
    numeric = {str(key): float(value) for key, value in counts.items()}
    total = sum(numeric.values())
    if total <= 0:
        return {}
    return {key: value / total for key, value in numeric.items()}


def numeric_map(values: dict[str, Any]) -> dict[str, float]:
    return {str(key): float(value) for key, value in values.items() if value is not None}


def distribution_l1(left: dict[str, float], right: dict[str, float]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    return 0.5 * sum(abs(left.get(key, 0.0) - right.get(key, 0.0)) for key in keys)


def numeric_map_distance(left: dict[str, float], right: dict[str, float]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    return min(1.0, sum(abs(left.get(key, 0.0) - right.get(key, 0.0)) for key in keys) / len(keys))


def scalar_distance(left: Any, right: Any, *, scale: float) -> float:
    if left is None or right is None:
        return 0.0
    return min(1.0, abs(float(left) - float(right)) / scale)


def safe_ratio(numerator: Any, denominator: Any) -> float | None:
    if numerator is None or denominator in {None, 0}:
        return None
    return float(numerator) / float(denominator)


def sample_quality(fingerprint_report: dict[str, Any]) -> dict[str, Any]:
    record_count = int(fingerprint_report.get("record_count", 0) or 0)
    aggregate = fingerprint_report.get("aggregate", {})
    gap_stats = aggregate.get("gap_statistics", {})
    gap_records = int(gap_stats.get("covered_records", 0) or 0)
    features = baseline_features(aggregate)
    completeness = feature_completeness(features)
    sample_size_score = min(1.0, record_count / STRONG_RECOMMENDED_RECORDS)
    minimum_sample_score = min(1.0, record_count / MIN_RECOMMENDED_RECORDS)
    gap_coverage = safe_ratio(gap_records, record_count) or 0.0
    overall = (
        0.45 * sample_size_score
        + 0.25 * minimum_sample_score
        + 0.15 * gap_coverage
        + 0.15 * completeness
    )
    return {
        "record_count": record_count,
        "minimum_recommended_records": MIN_RECOMMENDED_RECORDS,
        "strong_recommended_records": STRONG_RECOMMENDED_RECORDS,
        "sample_size_score": sample_size_score,
        "minimum_sample_score": minimum_sample_score,
        "gap_coverage": gap_coverage,
        "feature_completeness": completeness,
        "overall_confidence": min(1.0, overall),
    }


def quality_from_baseline_metadata(metadata: dict[str, Any], features: dict[str, Any]) -> dict[str, Any]:
    record_count = int(metadata.get("record_count", 0) or 0)
    completeness = feature_completeness(features)
    sample_size_score = min(1.0, record_count / STRONG_RECOMMENDED_RECORDS)
    minimum_sample_score = min(1.0, record_count / MIN_RECOMMENDED_RECORDS)
    overall = 0.55 * sample_size_score + 0.30 * minimum_sample_score + 0.15 * completeness
    return {
        "record_count": record_count,
        "minimum_recommended_records": MIN_RECOMMENDED_RECORDS,
        "strong_recommended_records": STRONG_RECOMMENDED_RECORDS,
        "sample_size_score": sample_size_score,
        "minimum_sample_score": minimum_sample_score,
        "gap_coverage": 0.0,
        "feature_completeness": completeness,
        "overall_confidence": min(1.0, overall),
    }


def feature_completeness(features: dict[str, Any]) -> float:
    checks = [
        bool(features.get("bit_length_distribution")),
        bool(features.get("residue_total_variation")),
        features.get("low16_collision_rate") is not None,
        features.get("next_prime_exposure_score") is not None,
        features.get("mean_right_gap_over_logp") is not None,
        features.get("large_left_gap_ratio") is not None,
    ]
    return sum(1 for value in checks if value) / len(checks)
