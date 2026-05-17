from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, gcd, log
from typing import Iterable

from .conjecture_lab import build_observations, sieve_primes, weighted_residue_distribution


@dataclass(frozen=True)
class PrimeCandidateScore:
    candidate: int
    offset: int
    score: float
    base_density: float
    wheel_factor: float
    residue_factor: float
    gap_survival: float
    is_prime: bool


def score_next_prime_candidates(
    start: int,
    *,
    span: int = 512,
    modulo: int = 210,
    top: int = 12,
    training_limit: int | None = None,
) -> dict[str, object]:
    if start < 2:
        raise ValueError("start must be at least 2")
    if span < 4:
        raise ValueError("span must be at least 4")
    if top < 1:
        raise ValueError("top must be positive")

    end = start + span
    observed_limit = max(end, training_limit or end)
    primes = sieve_primes(observed_limit)
    prime_set = set(primes)
    actual_next = next((prime for prime in primes if prime > start), None)
    residues = coprime_residues(modulo)
    residue_factors = build_residue_factors(max(1000, observed_limit), modulo)
    wheel_factor = modulo / len(residues)
    expected_gap = max(2.0, log(max(start, 3)))
    scored: list[PrimeCandidateScore] = []

    for candidate in range(start + 1, end + 1):
        if candidate > 2 and candidate % 2 == 0:
            continue
        if candidate != 2 and gcd(candidate, modulo) != 1:
            continue
        offset = candidate - start
        base_density = 1 / log(max(candidate, 3))
        residue_factor = residue_factors.get(candidate % modulo, 1.0)
        gap_survival = exp(-offset / expected_gap)
        score = base_density * wheel_factor * residue_factor * gap_survival
        scored.append(
            PrimeCandidateScore(
                candidate=candidate,
                offset=offset,
                score=score,
                base_density=base_density,
                wheel_factor=wheel_factor,
                residue_factor=residue_factor,
                gap_survival=gap_survival,
                is_prime=candidate in prime_set,
            )
        )

    ranked = sorted(scored, key=lambda item: item.score, reverse=True)
    rank_of_actual = None
    if actual_next is not None:
        for index, item in enumerate(ranked, start=1):
            if item.candidate == actual_next:
                rank_of_actual = index
                break

    return {
        "schema": "primeproject.prediction.v1",
        "start": start,
        "span": span,
        "modulo": modulo,
        "training_limit": observed_limit,
        "expected_gap": expected_gap,
        "actual_next_prime": actual_next,
        "actual_offset": actual_next - start if actual_next is not None else None,
        "rank_of_actual": rank_of_actual,
        "candidates_scored": len(scored),
        "top_candidates": [asdict(item) for item in ranked[:top]],
    }


def build_residue_factors(limit: int, modulo: int) -> dict[int, float]:
    observations = build_observations(limit)
    if not observations:
        return {residue: 1.0 for residue in coprime_residues(modulo)}

    weights = [observation.next_prime_weight for observation in observations]
    distribution = weighted_residue_distribution(observations, weights, modulo)
    residues = coprime_residues(modulo)
    uniform = 1 / len(residues)
    return {
        residue: max(0.2, min(5.0, distribution.get(residue, uniform) / uniform))
        for residue in residues
    }


def coprime_residues(modulo: int) -> list[int]:
    if modulo < 2:
        raise ValueError("modulo must be at least 2")
    residues = [residue for residue in range(modulo) if gcd(residue, modulo) == 1]
    if not residues:
        raise ValueError("modulo has no coprime residues")
    return residues


def normalize_scores(candidates: Iterable[PrimeCandidateScore]) -> list[dict[str, float | int | bool]]:
    rows = list(candidates)
    total = sum(item.score for item in rows)
    if total <= 0:
        return [{**asdict(item), "normalized_score": 0.0} for item in rows]
    return [{**asdict(item), "normalized_score": item.score / total} for item in rows]
