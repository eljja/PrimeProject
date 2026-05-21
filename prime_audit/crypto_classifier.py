from __future__ import annotations

from math import sqrt
from typing import Any

from .feature_vectors import SCALAR_FEATURES, normalize_feature_vector


CRYPTO_CLASSIFIER_SCHEMA = "primeproject.crypto-classifier-report.v1"


def run_crypto_classifier(
    feature_payload: dict[str, Any],
    *,
    feature_space: str = "interaction",
) -> dict[str, Any]:
    vectors = [normalize_feature_vector(vector) for vector in feature_payload.get("vectors", [])]
    labels = sorted({vector["label"] for vector in vectors if vector.get("label")})
    usable = [vector for vector in vectors if vector.get("label")]
    predictions = leave_one_out_predictions(usable, feature_space=feature_space)
    correct = sum(1 for row in predictions if row["correct"])
    total = len(predictions)
    label_summary = summarize_labels(predictions, labels)
    return {
        "schema": CRYPTO_CLASSIFIER_SCHEMA,
        "model": {
            "family": "nearest-centroid",
            "feature_space": feature_space,
            "dependency": "stdlib",
            "purpose": "screening baseline before heavier XGBoost/RandomForest experiments",
        },
        "vector_count": len(vectors),
        "usable_vector_count": len(usable),
        "label_count": len(labels),
        "accuracy": correct / total if total else None,
        "correct": correct,
        "total": total,
        "labels": label_summary,
        "predictions": predictions,
        "findings": classifier_findings(vectors, usable, predictions),
    }


def leave_one_out_predictions(vectors: list[dict[str, Any]], *, feature_space: str) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    for index, target in enumerate(vectors):
        train = [vector for offset, vector in enumerate(vectors) if offset != index]
        labels = sorted({vector["label"] for vector in train})
        centroids = {
            label: centroid([vector for vector in train if vector["label"] == label], feature_space=feature_space)
            for label in labels
        }
        if not centroids:
            continue
        target_values = expanded_values(target, feature_space=feature_space)
        distances = [
            {
                "label": label,
                "distance": euclidean_distance(target_values, values),
            }
            for label, values in centroids.items()
        ]
        distances.sort(key=lambda item: item["distance"])
        predicted = distances[0]["label"]
        predictions.append(
            {
                "id": target["id"],
                "actual": target["label"],
                "predicted": predicted,
                "correct": predicted == target["label"],
                "margin": classification_margin(distances),
                "distances": distances,
            }
        )
    return predictions


def expanded_values(vector: dict[str, Any], *, feature_space: str) -> dict[str, float]:
    base = {name: float(vector["features"].get(name) or 0.0) for name in SCALAR_FEATURES}
    if feature_space == "linear":
        return base
    if feature_space != "interaction":
        raise ValueError(f"Unsupported feature space: {feature_space}")
    expanded = dict(base)
    interaction_pairs = [
        ("residue_tv_210", "next_prime_exposure_score"),
        ("residue_tv_2310", "mean_right_gap_over_logp"),
        ("low16_collision_rate", "max_residue_tv"),
        ("bit_length_entropy", "large_left_gap_ratio"),
    ]
    for left, right in interaction_pairs:
        expanded[f"{left}*{right}"] = base[left] * base[right]
    for name in ("residue_tv_210", "next_prime_exposure_score", "low16_collision_rate"):
        expanded[f"{name}^2"] = base[name] ** 2
    return expanded


def centroid(vectors: list[dict[str, Any]], *, feature_space: str) -> dict[str, float]:
    expanded = [expanded_values(vector, feature_space=feature_space) for vector in vectors]
    keys = sorted({key for values in expanded for key in values})
    if not expanded:
        return {key: 0.0 for key in keys}
    return {
        key: sum(values.get(key, 0.0) for values in expanded) / len(expanded)
        for key in keys
    }


def euclidean_distance(left: dict[str, float], right: dict[str, float]) -> float:
    keys = set(left) | set(right)
    return sqrt(sum((left.get(key, 0.0) - right.get(key, 0.0)) ** 2 for key in keys))


def classification_margin(distances: list[dict[str, Any]]) -> float | None:
    if len(distances) < 2:
        return None
    return float(distances[1]["distance"]) - float(distances[0]["distance"])


def summarize_labels(predictions: list[dict[str, Any]], labels: list[str]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for label in labels:
        rows = [row for row in predictions if row["actual"] == label]
        correct = sum(1 for row in rows if row["correct"])
        summary[label] = {
            "total": len(rows),
            "correct": correct,
            "accuracy": correct / len(rows) if rows else None,
        }
    return summary


def classifier_findings(
    vectors: list[dict[str, Any]],
    usable: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if len(usable) < len(vectors):
        findings.append(
            {
                "check": "missing_labels",
                "severity": "low",
                "message": "Some feature vectors have no label and were excluded from classifier evaluation.",
            }
        )
    label_counts: dict[str, int] = {}
    for vector in usable:
        label_counts[vector["label"]] = label_counts.get(vector["label"], 0) + 1
    small_labels = {label: count for label, count in label_counts.items() if count < 2}
    if small_labels:
        findings.append(
            {
                "check": "insufficient_label_replicates",
                "severity": "medium",
                "message": "Leave-one-out evaluation needs at least two vectors per label.",
                "evidence": small_labels,
            }
        )
    if not predictions:
        findings.append(
            {
                "check": "no_classifier_trials",
                "severity": "high",
                "message": "No classifier predictions were produced.",
            }
        )
    return findings
