from __future__ import annotations

from math import log2, sqrt
from pathlib import Path
from random import Random
from typing import Any

from .baselines import baseline_features


FEATURE_VECTOR_SCHEMA = "primeproject.generator-feature-vectors.v1"
FEATURE_VECTOR_VERSION = "generator-feature-vector.v1"

SCALAR_FEATURES = [
    "record_count_log2",
    "bit_length_mean",
    "bit_length_stddev",
    "bit_length_entropy",
    "bit_length_max_mass",
    "residue_tv_30",
    "residue_tv_210",
    "residue_tv_2310",
    "low16_collision_rate",
    "next_prime_exposure_score",
    "mean_left_gap_over_logp",
    "mean_right_gap_over_logp",
    "large_left_gap_ratio",
    "max_residue_tv",
]


def build_feature_vector_payload(
    vectors: list[dict[str, Any]],
    *,
    claim_scope: str = "unspecified",
    source: str | None = None,
) -> dict[str, Any]:
    normalized = [normalize_feature_vector(vector) for vector in vectors]
    labels = sorted({vector["label"] for vector in normalized if vector.get("label")})
    return {
        "schema": FEATURE_VECTOR_SCHEMA,
        "feature_version": FEATURE_VECTOR_VERSION,
        "claim_scope": claim_scope,
        "source": source,
        "feature_names": list(SCALAR_FEATURES),
        "vector_count": len(normalized),
        "labels": labels,
        "vectors": normalized,
    }


def build_controlled_synthetic_feature_vectors(
    *,
    limit: int = 200_000,
    samples_per_label: int = 4,
    record_count: int = 80,
    seed: int = 20260523,
    gap_max_steps: int = 1024,
) -> dict[str, Any]:
    if samples_per_label < 2:
        raise ValueError("samples_per_label must be at least 2")
    if record_count < 2:
        raise ValueError("record_count must be at least 2")

    from .attribution import ATTRIBUTION_GENERATORS, sample_generator_records
    from .conjecture_lab import build_observations
    from .fingerprints import analyze_prime_generator_fingerprints

    observations = build_observations(limit)
    if record_count > len(observations):
        raise ValueError("record_count exceeds available prime observations")
    rng = Random(seed)
    vectors = []
    for generator in ATTRIBUTION_GENERATORS:
        for index in range(samples_per_label):
            records = sample_generator_records(
                observations,
                generator=generator,
                count=record_count,
                rng=rng,
                key_prefix=f"classifier-{generator}-{index}",
            )
            fingerprint = analyze_prime_generator_fingerprints(records, gap_max_steps=gap_max_steps)
            vectors.append(
                feature_vector_from_fingerprint(
                    fingerprint,
                    vector_id=f"{generator}-{index}",
                    label=generator,
                    source="controlled-synthetic-generator",
                )
            )
    payload = build_feature_vector_payload(
        vectors,
        claim_scope="controlled_synthetic_only",
        source="controlled synthetic generator samples; not real-world library evidence",
    )
    payload["generator"] = {
        "limit": limit,
        "samples_per_label": samples_per_label,
        "record_count": record_count,
        "seed": seed,
        "gap_max_steps": gap_max_steps,
    }
    return payload


def feature_vector_from_fingerprint(
    fingerprint_report: dict[str, Any],
    *,
    vector_id: str,
    label: str,
    source: str | None = None,
) -> dict[str, Any]:
    aggregate = fingerprint_report.get("aggregate", {})
    features = baseline_features(aggregate)
    values = flatten_baseline_features(
        features,
        record_count=int(fingerprint_report.get("record_count") or aggregate.get("record_count") or 0),
    )
    return {
        "schema": FEATURE_VECTOR_VERSION,
        "id": vector_id,
        "label": label,
        "source": source or fingerprint_report.get("source"),
        "record_count": int(fingerprint_report.get("record_count") or 0),
        "features": values,
    }


def feature_vector_from_baseline(
    baseline: dict[str, Any],
    *,
    vector_id: str | None = None,
    label: str | None = None,
) -> dict[str, Any]:
    record_count = int(baseline.get("record_count") or 0)
    values = flatten_baseline_features(baseline.get("features", {}), record_count=record_count)
    return {
        "schema": FEATURE_VECTOR_VERSION,
        "id": vector_id or str(baseline.get("name") or "baseline"),
        "label": label or str(baseline.get("name") or "unknown"),
        "source": baseline.get("source"),
        "record_count": record_count,
        "features": values,
    }


def load_feature_vector_specs(specs: list[str]) -> list[dict[str, str]]:
    parsed: list[dict[str, str]] = []
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"Feature vector input requires label=path, got {spec!r}")
        label, path = spec.split("=", 1)
        label = label.strip()
        path = path.strip()
        if not label or not path:
            raise ValueError(f"Feature vector input requires label=path, got {spec!r}")
        parsed.append({"label": label, "path": path})
    return parsed


def load_feature_vectors_from_files(
    *,
    fingerprint_specs: list[str] | None = None,
    baseline_specs: list[str] | None = None,
) -> list[dict[str, Any]]:
    import json

    vectors: list[dict[str, Any]] = []
    for spec in load_feature_vector_specs(fingerprint_specs or []):
        path = Path(spec["path"])
        payload = json.loads(path.read_text(encoding="utf-8"))
        vectors.append(
            feature_vector_from_fingerprint(
                payload,
                vector_id=path.stem,
                label=spec["label"],
                source=str(path),
            )
        )
    for spec in load_feature_vector_specs(baseline_specs or []):
        path = Path(spec["path"])
        payload = json.loads(path.read_text(encoding="utf-8"))
        vectors.append(
            feature_vector_from_baseline(
                payload,
                vector_id=path.stem,
                label=spec["label"],
            )
        )
    return vectors


def flatten_baseline_features(features: dict[str, Any], *, record_count: int = 0) -> dict[str, float]:
    bit_length_stats = distribution_stats(features.get("bit_length_distribution", {}))
    residue_tv = features.get("residue_total_variation", {})
    values = {
        "record_count_log2": log2(record_count + 1),
        "bit_length_mean": bit_length_stats["mean"],
        "bit_length_stddev": bit_length_stats["stddev"],
        "bit_length_entropy": bit_length_stats["entropy"],
        "bit_length_max_mass": bit_length_stats["max_mass"],
        "residue_tv_30": float(residue_tv.get("30") or 0.0),
        "residue_tv_210": float(residue_tv.get("210") or 0.0),
        "residue_tv_2310": float(residue_tv.get("2310") or 0.0),
        "low16_collision_rate": float(features.get("low16_collision_rate") or 0.0),
        "next_prime_exposure_score": float(features.get("next_prime_exposure_score") or 0.0),
        "mean_left_gap_over_logp": float(features.get("mean_left_gap_over_logp") or 0.0),
        "mean_right_gap_over_logp": float(features.get("mean_right_gap_over_logp") or 0.0),
        "large_left_gap_ratio": float(features.get("large_left_gap_ratio") or 0.0),
        "max_residue_tv": float(features.get("max_residue_tv") or 0.0),
    }
    return {name: values[name] for name in SCALAR_FEATURES}


def distribution_stats(distribution: dict[str, Any]) -> dict[str, float]:
    items = [(float(key), float(value)) for key, value in distribution.items()]
    total = sum(value for _, value in items)
    if total <= 0:
        return {"mean": 0.0, "stddev": 0.0, "entropy": 0.0, "max_mass": 0.0}
    normalized = [(key, value / total) for key, value in items]
    mean = sum(key * weight for key, weight in normalized)
    variance = sum(((key - mean) ** 2) * weight for key, weight in normalized)
    entropy = -sum(weight * log2(weight) for _, weight in normalized if weight > 0)
    max_mass = max((weight for _, weight in normalized), default=0.0)
    return {
        "mean": mean,
        "stddev": sqrt(variance),
        "entropy": entropy,
        "max_mass": max_mass,
    }


def normalize_feature_vector(vector: dict[str, Any]) -> dict[str, Any]:
    features = vector.get("features", {})
    return {
        "schema": FEATURE_VECTOR_VERSION,
        "id": str(vector.get("id") or ""),
        "label": str(vector.get("label") or ""),
        "source": vector.get("source"),
        "record_count": int(vector.get("record_count") or 0),
        "features": {
            name: float(features.get(name) or 0.0)
            for name in SCALAR_FEATURES
        },
    }
