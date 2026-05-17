from __future__ import annotations

from dataclasses import dataclass, asdict
from math import gcd, log2
from typing import Iterable


WHEEL_30_RESIDUES = (1, 7, 11, 13, 17, 19, 23, 29)


@dataclass(frozen=True)
class PrimeObservation:
    prime: int
    previous_prime: int
    gap: int
    rejection_weight: int
    next_prime_weight: int
    wheel30_weight: int


@dataclass(frozen=True)
class MeasureSummary:
    generator: str
    total_weight: float
    entropy_bits: float
    effective_support: float
    max_weight_share: float
    mean_gap: float
    weighted_mean_gap: float
    residue_total_variation: float
    residue_distribution: dict[int, float]


def sieve_primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    candidate = 2
    while candidate * candidate <= limit:
        if sieve[candidate]:
            start = candidate * candidate
            step = candidate
            sieve[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
        candidate += 1
    return [index for index, is_prime in enumerate(sieve) if is_prime]


def build_observations(limit: int) -> list[PrimeObservation]:
    primes = sieve_primes(limit)
    observations: list[PrimeObservation] = []
    for previous_prime, prime in zip(primes, primes[1:]):
        observations.append(
            PrimeObservation(
                prime=prime,
                previous_prime=previous_prime,
                gap=prime - previous_prime,
                rejection_weight=1,
                next_prime_weight=prime - previous_prime,
                wheel30_weight=_wheel30_count(previous_prime, prime),
            )
        )
    return observations


def summarize_measure(
    observations: list[PrimeObservation],
    *,
    generator: str,
    modulo: int,
) -> MeasureSummary:
    weights = _weights_for_generator(observations, generator)
    total_weight = float(sum(weights))
    if total_weight == 0:
        raise ValueError("measure has zero total weight")

    probabilities = [weight / total_weight for weight in weights]
    entropy = -sum(prob * log2(prob) for prob in probabilities if prob > 0)
    effective_support = 2**entropy
    max_weight_share = max(probabilities)
    mean_gap = sum(observation.gap for observation in observations) / len(observations)
    weighted_mean_gap = sum(
        observation.gap * weight for observation, weight in zip(observations, weights)
    ) / total_weight
    residue_distribution = weighted_residue_distribution(observations, weights, modulo)
    residue_total_variation = total_variation_from_uniform(residue_distribution, modulo)
    return MeasureSummary(
        generator=generator,
        total_weight=total_weight,
        entropy_bits=entropy,
        effective_support=effective_support,
        max_weight_share=max_weight_share,
        mean_gap=mean_gap,
        weighted_mean_gap=weighted_mean_gap,
        residue_total_variation=residue_total_variation,
        residue_distribution=residue_distribution,
    )


def run_lab(limit: int, modulo: int = 30) -> dict[str, object]:
    observations = build_observations(limit)
    generators = ("rejection", "next_prime", "wheel30_next")
    summaries = {
        generator: asdict(summarize_measure(observations, generator=generator, modulo=modulo))
        for generator in generators
    }
    return {
        "limit": limit,
        "modulo": modulo,
        "prime_count": len(observations) + 1 if observations else 0,
        "observation_count": len(observations),
        "observations": [asdict(observation) for observation in observations],
        "summaries": summaries,
    }


def weighted_residue_distribution(
    observations: Iterable[PrimeObservation],
    weights: Iterable[int],
    modulo: int,
) -> dict[int, float]:
    totals: dict[int, float] = {}
    total_weight = 0.0
    for observation, weight in zip(observations, weights):
        residue = observation.prime % modulo
        if gcd(residue, modulo) != 1:
            continue
        totals[residue] = totals.get(residue, 0.0) + weight
        total_weight += weight
    if total_weight == 0:
        return {}
    return {residue: value / total_weight for residue, value in sorted(totals.items())}


def total_variation_from_uniform(distribution: dict[int, float], modulo: int) -> float:
    residues = [residue for residue in range(modulo) if gcd(residue, modulo) == 1]
    if not residues:
        return 0.0
    uniform = 1 / len(residues)
    return 0.5 * sum(abs(distribution.get(residue, 0.0) - uniform) for residue in residues)


def _weights_for_generator(observations: list[PrimeObservation], generator: str) -> list[int]:
    if generator == "rejection":
        return [observation.rejection_weight for observation in observations]
    if generator == "next_prime":
        return [observation.next_prime_weight for observation in observations]
    if generator == "wheel30_next":
        return [observation.wheel30_weight for observation in observations]
    raise ValueError(f"unknown generator: {generator}")


def _wheel30_count(previous_prime: int, prime: int) -> int:
    count = 0
    for value in range(previous_prime + 1, prime + 1):
        if value % 30 in WHEEL_30_RESIDUES:
            count += 1
    return max(count, 1)

