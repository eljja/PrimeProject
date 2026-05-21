from __future__ import annotations

from bisect import bisect_left
from itertools import product
from random import Random
from typing import Any, Iterable

from .baselines import ABLATION_COMPONENT_WEIGHTS, build_generator_baseline, compare_fingerprint_to_baselines
from .conjecture_lab import PrimeObservation, build_observations
from .fingerprints import analyze_prime_generator_fingerprints
from .models import KeyRecord


ATTRIBUTION_GENERATORS = ("rejection", "next_prime", "wheel30_next")
CONTROL_MODES = ("none", "bit_length")


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


def run_attribution_confound_grid(
    *,
    limits: list[int],
    train_counts: list[int],
    test_counts: list[int],
    trials: int = 3,
    repeats: int = 1,
    seed: int = 20260521,
    gap_max_steps: int = 1024,
    include_ablation: bool = True,
) -> dict[str, Any]:
    if not limits or not train_counts or not test_counts:
        raise ValueError("limits, train_counts, and test_counts must be non-empty")
    if repeats < 1:
        raise ValueError("repeats must be positive")

    rows = []
    paired_results: dict[str, dict[str, dict[str, Any]]] = {}
    for pair_index, (limit, train_count, test_count) in enumerate(
        product(limits, train_counts, test_counts)
    ):
        base_pair_key = grid_pair_key(limit, train_count, test_count)
        for repeat_index in range(repeats):
            pair_key = grid_pair_key(limit, train_count, test_count, repeat=repeat_index)
            pair_seed = seed + pair_index * repeats + repeat_index
            paired_results[pair_key] = {}
            for control_mode in CONTROL_MODES:
                result = run_synthetic_attribution_benchmark(
                    limit=limit,
                    train_count=train_count,
                    test_count=test_count,
                    trials=trials,
                    seed=pair_seed,
                    gap_max_steps=gap_max_steps,
                    include_ablation=include_ablation,
                    control_mode=control_mode,
                )
                row = summarize_benchmark_row(result, pair_key, base_pair_key, repeat_index)
                rows.append(row)
                paired_results[pair_key][control_mode] = row

    deltas = build_confound_deltas(paired_results)
    return {
        "schema": "primeproject.attribution-confound-grid.v1",
        "limits": limits,
        "train_counts": train_counts,
        "test_counts": test_counts,
        "trials": trials,
        "repeats": repeats,
        "seed": seed,
        "gap_max_steps": gap_max_steps,
        "include_ablation": include_ablation,
        "random_baseline_accuracy": 1 / len(ATTRIBUTION_GENERATORS),
        "rows": rows,
        "deltas": deltas,
        "summary": summarize_confound_deltas(deltas),
    }


def grid_pair_key(limit: int, train_count: int, test_count: int, repeat: int | None = None) -> str:
    key = f"limit={limit};train={train_count};test={test_count}"
    if repeat is not None:
        return f"{key};repeat={repeat}"
    return key


def summarize_benchmark_row(
    result: dict[str, Any],
    pair_key: str,
    base_pair_key: str | None = None,
    repeat: int = 0,
) -> dict[str, Any]:
    profile_accuracy = {
        profile_name: profile_result["accuracy"]
        for profile_name, profile_result in result["ablation"].items()
    }
    return {
        "pair_key": pair_key,
        "base_pair_key": base_pair_key or pair_key,
        "repeat": repeat,
        "limit": result["limit"],
        "train_count": result["train_count"],
        "test_count": result["test_count"],
        "trials": result["trials"],
        "seed": result["seed"],
        "control_mode": result["control"]["mode"],
        "accuracy": result["accuracy"],
        "profile_accuracy": profile_accuracy,
        "baseline_quality": result["baseline_quality"],
    }


def build_confound_deltas(
    paired_results: dict[str, dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    deltas = []
    for pair_key, pair in paired_results.items():
        uncontrolled = pair.get("none")
        controlled = pair.get("bit_length")
        if not uncontrolled or not controlled:
            continue
        profile_names = sorted(
            set(uncontrolled["profile_accuracy"]) & set(controlled["profile_accuracy"])
        )
        for profile_name in profile_names:
            uncontrolled_accuracy = uncontrolled["profile_accuracy"][profile_name]
            controlled_accuracy = controlled["profile_accuracy"][profile_name]
            delta = uncontrolled_accuracy - controlled_accuracy
            deltas.append(
                {
                    "pair_key": pair_key,
                    "base_pair_key": uncontrolled.get("base_pair_key", pair_key),
                    "repeat": uncontrolled.get("repeat", 0),
                    "limit": uncontrolled["limit"],
                    "train_count": uncontrolled["train_count"],
                    "test_count": uncontrolled["test_count"],
                    "profile": profile_name,
                    "uncontrolled_accuracy": uncontrolled_accuracy,
                    "controlled_accuracy": controlled_accuracy,
                    "accuracy_drop": delta,
                    "interpretation": interpret_confound_delta(
                        profile_name,
                        uncontrolled_accuracy,
                        controlled_accuracy,
                    ),
                }
            )
    return deltas


def interpret_confound_delta(
    profile_name: str,
    uncontrolled_accuracy: float,
    controlled_accuracy: float,
) -> str:
    random_accuracy = 1 / len(ATTRIBUTION_GENERATORS)
    drop = uncontrolled_accuracy - controlled_accuracy
    if profile_name == "bit_length_only" and drop >= 0.2:
        return "bit_length_confound"
    if controlled_accuracy >= random_accuracy + 0.25:
        return "survives_bit_length_control"
    if uncontrolled_accuracy >= random_accuracy + 0.25 and controlled_accuracy <= random_accuracy + 0.1:
        return "control_sensitive"
    return "inconclusive"


def summarize_confound_deltas(deltas: list[dict[str, Any]]) -> dict[str, Any]:
    by_profile: dict[str, list[dict[str, Any]]] = {}
    for delta in deltas:
        by_profile.setdefault(delta["profile"], []).append(delta)

    profile_summary = {}
    for profile_name, profile_deltas in sorted(by_profile.items()):
        uncontrolled_values = [delta["uncontrolled_accuracy"] for delta in profile_deltas]
        controlled_values = [delta["controlled_accuracy"] for delta in profile_deltas]
        drop_values = [delta["accuracy_drop"] for delta in profile_deltas]
        uncontrolled_stats = distribution_summary(uncontrolled_values)
        controlled_stats = distribution_summary(controlled_values)
        drop_stats = distribution_summary(drop_values)
        profile_summary[profile_name] = {
            "mean_uncontrolled_accuracy": uncontrolled_stats["mean"],
            "mean_controlled_accuracy": controlled_stats["mean"],
            "mean_accuracy_drop": drop_stats["mean"],
            "uncontrolled_accuracy": uncontrolled_stats,
            "controlled_accuracy": controlled_stats,
            "accuracy_drop": drop_stats,
            "runs": len(profile_deltas),
            "interpretations": count_labels(delta["interpretation"] for delta in profile_deltas),
        }
        profile_summary[profile_name]["robust_interpretation"] = interpret_profile_summary(
            profile_name,
            profile_summary[profile_name],
        )

    ranked_confounds = sorted(
        profile_summary.items(),
        key=lambda item: item[1]["mean_accuracy_drop"],
        reverse=True,
    )
    return {
        "profiles": profile_summary,
        "most_confound_sensitive_profiles": [
            {"profile": profile_name, **summary}
            for profile_name, summary in ranked_confounds
            if summary["accuracy_drop"]["ci95_low"] > 0
        ],
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def distribution_summary(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {
            "mean": 0.0,
            "stddev": 0.0,
            "standard_error": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "count": 0,
        }
    average = mean(values)
    if len(values) <= 1:
        stddev = 0.0
    else:
        variance = sum((value - average) ** 2 for value in values) / (len(values) - 1)
        stddev = variance ** 0.5
    standard_error = stddev / (len(values) ** 0.5)
    margin = 1.96 * standard_error
    return {
        "mean": average,
        "stddev": stddev,
        "standard_error": standard_error,
        "ci95_low": average - margin,
        "ci95_high": average + margin,
        "count": len(values),
    }


def interpret_profile_summary(profile_name: str, summary: dict[str, Any]) -> str:
    random_accuracy = 1 / len(ATTRIBUTION_GENERATORS)
    drop = summary["accuracy_drop"]
    controlled = summary["controlled_accuracy"]
    uncontrolled = summary["uncontrolled_accuracy"]
    if profile_name == "bit_length_only" and drop["ci95_low"] > 0.05:
        return "robust_bit_length_confound"
    if controlled["ci95_low"] > random_accuracy + 0.1:
        return "robust_survives_bit_length_control"
    if uncontrolled["ci95_low"] > random_accuracy + 0.1 and controlled["ci95_high"] <= random_accuracy + 0.1:
        return "robust_control_sensitive"
    return "inconclusive"


def count_labels(labels: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))


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
