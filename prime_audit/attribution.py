from __future__ import annotations

from bisect import bisect_left
from random import Random
from typing import Any

from .baselines import ABLATION_COMPONENT_WEIGHTS, build_generator_baseline, compare_fingerprint_to_baselines
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
    include_ablation: bool = True,
    control_mode: str = "none",
) -> dict[str, Any]:
    if train_count < 2 or test_count < 1:
        raise ValueError("train_count must be at least 2 and test_count must be positive")
    if trials < 1:
        raise ValueError("trials must be positive")
    if control_mode not in {"none", "bit_length"}:
        raise ValueError("control_mode must be 'none' or 'bit_length'")

    observations = build_observations(limit)
    if not observations:
        raise ValueError("limit is too small for attribution benchmark")
    if max(train_count, test_count) > len(observations):
        raise ValueError("sample counts exceed available unique prime observations")
    train_bucket_plan = None
    test_bucket_plan = None
    if control_mode == "bit_length":
        train_bucket_plan = build_bit_length_bucket_plan(observations, train_count)
        test_bucket_plan = build_bit_length_bucket_plan(observations, test_count)

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
            bit_length_bucket_plan=train_bucket_plan,
        )
        report = analyze_prime_generator_fingerprints(records, gap_max_steps=gap_max_steps)
        baseline_reports[generator] = report
        baselines.append(build_generator_baseline(report, name=generator, source="synthetic-ground-truth"))

    profiles = {"all": ABLATION_COMPONENT_WEIGHTS["all"]}
    if include_ablation:
        profiles = dict(ABLATION_COMPONENT_WEIGHTS)
    results = {
        name: empty_profile_result()
        for name in profiles
    }
    for trial in range(trials):
        for generator in ATTRIBUTION_GENERATORS:
            records = sample_generator_records(
                observations,
                generator=generator,
                count=test_count,
                rng=rng,
                key_prefix=f"test-{trial}-{generator}",
                bit_length_bucket_plan=test_bucket_plan,
            )
            fingerprint = analyze_prime_generator_fingerprints(records, gap_max_steps=gap_max_steps)
            for profile_name, component_weights in profiles.items():
                comparison = compare_fingerprint_to_baselines(
                    fingerprint,
                    baselines,
                    component_weights=component_weights,
                    profile_name=profile_name,
                )
                add_attribution_result(results[profile_name], trial, generator, comparison)

    primary = finalize_profile_result(results["all"])
    ablation = {
        name: finalize_profile_result(result)
        for name, result in results.items()
    }

    return {
        "schema": "primeproject.synthetic-attribution-benchmark.v1",
        "limit": limit,
        "seed": seed,
        "train_count": train_count,
        "test_count": test_count,
        "trials": trials,
        "gap_max_steps": gap_max_steps,
        "include_ablation": include_ablation,
        "control": {
            "mode": control_mode,
            "train_bit_length_plan": train_bucket_plan or {},
            "test_bit_length_plan": test_bucket_plan or {},
        },
        "generators": list(ATTRIBUTION_GENERATORS),
        "accuracy": primary["accuracy"],
        "correct": primary["correct"],
        "total": primary["total"],
        "confusion_matrix": primary["confusion_matrix"],
        "ablation": ablation,
        "baseline_quality": {
            baseline["name"]: baseline.get("quality")
            for baseline in baselines
        },
        "trials_detail": primary["trials_detail"],
    }


def empty_profile_result() -> dict[str, Any]:
    return {
        "correct": 0,
        "total": 0,
        "confusion_matrix": {
            generator: {candidate: 0 for candidate in ATTRIBUTION_GENERATORS}
            for generator in ATTRIBUTION_GENERATORS
        },
        "trials_detail": [],
    }


def add_attribution_result(
    result: dict[str, Any],
    trial: int,
    true_generator: str,
    comparison: dict[str, Any],
) -> None:
    nearest = comparison["nearest_baseline"]
    predicted = nearest["baseline_name"] if nearest else None
    if predicted in result["confusion_matrix"][true_generator]:
        result["confusion_matrix"][true_generator][predicted] += 1
    is_correct = predicted == true_generator
    result["correct"] += 1 if is_correct else 0
    result["total"] += 1
    result["trials_detail"].append(
        {
            "trial": trial,
            "true_generator": true_generator,
            "predicted_generator": predicted,
            "correct": is_correct,
            "distance": nearest["distance"] if nearest else None,
            "confidence": nearest["confidence"] if nearest else None,
            "components": nearest["components"] if nearest else None,
        }
    )


def finalize_profile_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        **result,
        "accuracy": result["correct"] / result["total"] if result["total"] else 0.0,
    }


def sample_generator_records(
    observations: list[PrimeObservation],
    *,
    generator: str,
    count: int,
    rng: Random,
    key_prefix: str,
    bit_length_bucket_plan: dict[int, int] | None = None,
) -> list[KeyRecord]:
    weights = weights_for_generator(observations, generator)
    if bit_length_bucket_plan is None:
        selected = weighted_sample_without_replacement(observations, weights, count, rng)
    else:
        if sum(bit_length_bucket_plan.values()) != count:
            raise ValueError("bit-length bucket plan must sum to count")
        selected = weighted_sample_by_bit_length_plan(
            observations,
            weights,
            bit_length_bucket_plan,
            rng,
        )
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


def bucket_observations_by_bit_length(
    observations: list[PrimeObservation],
) -> dict[int, list[PrimeObservation]]:
    buckets: dict[int, list[PrimeObservation]] = {}
    for observation in observations:
        buckets.setdefault(observation.prime.bit_length(), []).append(observation)
    return dict(sorted(buckets.items()))


def build_bit_length_bucket_plan(
    observations: list[PrimeObservation],
    count: int,
) -> dict[int, int]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if count > len(observations):
        raise ValueError("count exceeds population")
    if count == 0:
        return {}

    buckets = bucket_observations_by_bit_length(observations)
    total = len(observations)
    allocations: dict[int, int] = {}
    remainders: list[tuple[float, int, int]] = []
    assigned = 0
    for bit_length, bucket in buckets.items():
        exact = count * len(bucket) / total
        base = min(len(bucket), int(exact))
        allocations[bit_length] = base
        assigned += base
        remainders.append((exact - base, len(bucket) - base, bit_length))

    for _, capacity, bit_length in sorted(remainders, reverse=True):
        if assigned >= count:
            break
        if capacity <= 0:
            continue
        allocations[bit_length] += 1
        assigned += 1

    while assigned < count:
        progressed = False
        for bit_length, bucket in buckets.items():
            if allocations[bit_length] >= len(bucket):
                continue
            allocations[bit_length] += 1
            assigned += 1
            progressed = True
            if assigned >= count:
                break
        if not progressed:
            raise ValueError("unable to allocate bit-length control plan")

    return {bit_length: allocation for bit_length, allocation in allocations.items() if allocation > 0}


def weighted_sample_by_bit_length_plan(
    observations: list[PrimeObservation],
    weights: list[int],
    bit_length_bucket_plan: dict[int, int],
    rng: Random,
) -> list[PrimeObservation]:
    by_bucket: dict[int, list[tuple[PrimeObservation, int]]] = {}
    for observation, weight in zip(observations, weights):
        by_bucket.setdefault(observation.prime.bit_length(), []).append((observation, weight))

    selected: list[PrimeObservation] = []
    for bit_length, bucket_count in bit_length_bucket_plan.items():
        if bucket_count < 0:
            raise ValueError("bit-length bucket counts must be non-negative")
        bucket = by_bucket.get(bit_length, [])
        if bucket_count > len(bucket):
            raise ValueError(f"bit-length bucket {bit_length} exceeds population")
        if bucket_count == 0:
            continue
        bucket_observations = [observation for observation, _ in bucket]
        bucket_weights = [weight for _, weight in bucket]
        selected.extend(
            weighted_sample_without_replacement(bucket_observations, bucket_weights, bucket_count, rng)
        )
    return selected


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
