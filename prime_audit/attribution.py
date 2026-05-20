from __future__ import annotations

from bisect import bisect_left
from random import Random
from typing import Any

from .baselines import build_generator_baseline, compare_fingerprint_to_baselines
from .conjecture_lab import PrimeObservation, build_observations
from .fingerprints import analyze_prime_generator_fingerprints
from .models import KeyRecord


ATTRIBUTION_GENERATORS = ("rejection", "next_prime", "wheel30_next")


def run_synthetic_attribution_benchmark(
    *,
    limit: int = 200_000,
    train_count: int = 80,
    test_count: int = 40,
    trials: int = 3,
    seed: int = 20260521,
    gap_max_steps: int = 1024,
) -> dict[str, Any]:
    if train_count < 2 or test_count < 1:
        raise ValueError("train_count must be at least 2 and test_count must be positive")
    if trials < 1:
        raise ValueError("trials must be positive")

    observations = build_observations(limit)
    if not observations:
        raise ValueError("limit is too small for attribution benchmark")
    if max(train_count, test_count) > len(observations):
        raise ValueError("sample counts exceed available unique prime observations")

    rng = Random(seed)
    baselines = []
    baseline_reports: dict[str, dict[str, Any]] = {}
    for generator in ATTRIBUTION_GENERATORS:
        records = sample_generator_records(
            observations,
            generator=generator,
            count=train_count,
            rng=rng,
            key_prefix=f"train-{generator}",
        )
        report = analyze_prime_generator_fingerprints(records, gap_max_steps=gap_max_steps)
        baseline_reports[generator] = report
        baselines.append(build_generator_baseline(report, name=generator, source="synthetic-ground-truth"))

    confusion = {
        generator: {candidate: 0 for candidate in ATTRIBUTION_GENERATORS}
        for generator in ATTRIBUTION_GENERATORS
    }
    trial_rows = []
    correct = 0
    total = 0
    for trial in range(trials):
        for generator in ATTRIBUTION_GENERATORS:
            records = sample_generator_records(
                observations,
                generator=generator,
                count=test_count,
                rng=rng,
                key_prefix=f"test-{trial}-{generator}",
            )
            fingerprint = analyze_prime_generator_fingerprints(records, gap_max_steps=gap_max_steps)
            comparison = compare_fingerprint_to_baselines(fingerprint, baselines)
            nearest = comparison["nearest_baseline"]
            predicted = nearest["baseline_name"] if nearest else None
            if predicted in confusion[generator]:
                confusion[generator][predicted] += 1
            is_correct = predicted == generator
            correct += 1 if is_correct else 0
            total += 1
            trial_rows.append(
                {
                    "trial": trial,
                    "true_generator": generator,
                    "predicted_generator": predicted,
                    "correct": is_correct,
                    "distance": nearest["distance"] if nearest else None,
                    "confidence": nearest["confidence"] if nearest else None,
                    "components": nearest["components"] if nearest else None,
                }
            )

    return {
        "schema": "primeproject.synthetic-attribution-benchmark.v1",
        "limit": limit,
        "seed": seed,
        "train_count": train_count,
        "test_count": test_count,
        "trials": trials,
        "gap_max_steps": gap_max_steps,
        "generators": list(ATTRIBUTION_GENERATORS),
        "accuracy": correct / total if total else 0.0,
        "correct": correct,
        "total": total,
        "confusion_matrix": confusion,
        "baseline_quality": {
            baseline["name"]: baseline.get("quality")
            for baseline in baselines
        },
        "trials_detail": trial_rows,
    }


def sample_generator_records(
    observations: list[PrimeObservation],
    *,
    generator: str,
    count: int,
    rng: Random,
    key_prefix: str,
) -> list[KeyRecord]:
    weights = weights_for_generator(observations, generator)
    selected = weighted_sample_without_replacement(observations, weights, count, rng)
    return [
        KeyRecord(
            key_id=f"{key_prefix}-{index}",
            algorithm="prime",
            value=observation.prime,
            source=f"synthetic:{generator}",
            metadata={
                "generator": generator,
                "previous_prime": observation.previous_prime,
                "gap": observation.gap,
            },
        )
        for index, observation in enumerate(selected)
    ]


def weighted_sample_without_replacement(
    observations: list[PrimeObservation],
    weights: list[int],
    count: int,
    rng: Random,
) -> list[PrimeObservation]:
    if count > len(observations):
        raise ValueError("count exceeds population")
    keyed = []
    for observation, weight in zip(observations, weights):
        if weight <= 0:
            continue
        keyed.append((rng.random() ** (1 / weight), observation))
    keyed.sort(key=lambda item: item[0], reverse=True)
    return [observation for _, observation in keyed[:count]]


def weighted_sample_with_replacement(
    observations: list[PrimeObservation],
    weights: list[int],
    count: int,
    rng: Random,
) -> list[PrimeObservation]:
    cumulative = []
    running = 0
    for weight in weights:
        running += weight
        cumulative.append(running)
    if running <= 0:
        raise ValueError("weights must contain positive mass")
    selected = []
    for _ in range(count):
        ticket = rng.randrange(1, running + 1)
        selected.append(observations[bisect_left(cumulative, ticket)])
    return selected


def weights_for_generator(observations: list[PrimeObservation], generator: str) -> list[int]:
    if generator == "rejection":
        return [observation.rejection_weight for observation in observations]
    if generator == "next_prime":
        return [observation.next_prime_weight for observation in observations]
    if generator == "wheel30_next":
        return [observation.wheel30_weight for observation in observations]
    raise ValueError(f"unknown generator: {generator}")
