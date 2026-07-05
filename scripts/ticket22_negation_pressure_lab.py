from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket22-negation-pressure-lab.v1"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [n for n in range(2, limit + 1) if is_prime[n]], is_prime


def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0) is undefined")
    value = abs(n)
    count = 0
    while value % 2 == 0:
        count += 1
        value //= 2
    return count


def accelerated_step(n: int) -> tuple[int, int]:
    value = 3 * n + 1
    valuation = v2(value)
    return value >> valuation, valuation


def riemann_li_detector_horizon(max_terms_factor: float, beta: float, heights: list[float], threshold: float) -> dict[str, object]:
    rows = []
    for height in heights:
        zeros = [
            complex(beta, height),
            complex(1.0 - beta, height),
            complex(beta, -height),
            complex(1.0 - beta, -height),
        ]
        factors = [1.0 - 1.0 / rho for rho in zeros]
        powers = [1.0 + 0.0j for _ in zeros]
        search_limit = int(max(1000, math.ceil(max_terms_factor * height * height)))
        first_negative = None
        first_threshold = None
        min_value = float("inf")
        min_index = 0
        for n in range(1, search_limit + 1):
            for index, factor in enumerate(factors):
                powers[index] *= factor
            contribution = len(zeros) - sum(value.real for value in powers)
            if contribution < min_value:
                min_value = contribution
                min_index = n
            if first_negative is None and contribution < 0:
                first_negative = n
            if first_threshold is None and contribution < threshold:
                first_threshold = n
        rows.append(
            {
                "height": height,
                "search_limit": search_limit,
                "first_negative_li_index": first_negative,
                "first_below_threshold_index": first_threshold,
                "threshold": threshold,
                "minimum_value_seen": round(min_value, 12),
                "minimum_index_seen": min_index,
                "threshold_index_over_height_squared": (
                    round(first_threshold / (height * height), 8) if first_threshold else None
                ),
            }
        )

    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-22",
        "status": "proof_pressure_open",
        "route": "LiDetectorHorizon",
        "proof_or_counterexample_mode": "contrapositive_detector_horizon",
        "attempt": (
            "Assume an off-critical zero quartet exists and ask when it must become visible as a negative Li-type "
            "signal. The computation measures how the detector horizon grows with the zero height."
        ),
        "bounded_result": {
            "offcritical_beta": beta,
            "threshold": threshold,
            "height_rows": rows,
            "horizon_pattern": "first strong negative signal grows on the tested height^2 scale",
            "finite_prefix_strategy_status": "falsified_without_uniform_detector_bound",
        },
        "obstruction": (
            "The contrapositive route is plausible only with an effective all-height detector theorem. Without that "
            "theorem, an arbitrary finite Li-prefix can miss sufficiently high off-critical behavior."
        ),
        "candidate_theorem": (
            "Every off-critical zeta zero at height T and displacement beta-1/2 forces a certified negative Li/kernel "
            "witness before an explicit index N(T,beta), and the proof controls the contribution of all other zeros."
        ),
        "next_experiment": "Replace the empirical height^2 detector table by a symbolic explicit-formula inequality.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def affine_for_word(word: tuple[int, ...]) -> tuple[int, int]:
    total_shift = 0
    c_value = 0
    for valuation in word:
        c_value = 3 * c_value + (1 << total_shift)
        total_shift += valuation
    return total_shift, c_value


def residue_for_word(word: tuple[int, ...]) -> tuple[int, int]:
    total_shift, c_value = affine_for_word(word)
    modulus = 1 << total_shift
    inverse = pow(pow(3, len(word), modulus), -1, modulus)
    base_residue = (-c_value * inverse) % modulus
    for lift in range(2):
        residue = base_residue + lift * modulus
        if validates_word(word, residue):
            return residue, total_shift + 1
    raise ValueError(f"valuation word has no exact 2-adic lift: {word!r}")


def validates_word(word: tuple[int, ...], seed: int) -> bool:
    value = seed
    for expected in word:
        value, actual = accelerated_step(value)
        if actual != expected:
            return False
    return True


def collatz_mixed_two_adic_cylinder_rank(max_length: int, max_valuation: int) -> dict[str, object]:
    alphabet = list(range(1, max_valuation + 1))
    length_rows = []
    mixed_examples = []
    cycle_candidates: dict[int, dict[str, object]] = {}
    total_expanding = 0
    total_mixed_expanding = 0
    total_validated = 0
    invalid_words = 0
    log2_3 = math.log2(3)

    for length in range(1, max_length + 1):
        expanding_count = 0
        mixed_expanding_count = 0
        validated_count = 0
        best_word = None
        best_multiplier = 0.0
        for word in itertools.product(alphabet, repeat=length):
            total_shift, c_value = affine_for_word(word)
            multiplier = (3**length) / (2**total_shift)
            if (1 << total_shift) > 3**length and c_value % ((1 << total_shift) - 3**length) == 0:
                candidate = c_value // ((1 << total_shift) - 3**length)
                if candidate > 0 and candidate % 2 == 1 and validates_word(word, candidate):
                    cycle_candidates.setdefault(
                        candidate,
                        {
                            "cycle_value": candidate,
                            "word": list(word),
                            "word_length": length,
                            "total_shift": total_shift,
                        },
                    )
            if multiplier <= 1.0:
                continue
            expanding_count += 1
            total_expanding += 1
            if len(set(word)) > 1:
                mixed_expanding_count += 1
                total_mixed_expanding += 1
            try:
                residue, exact_bits = residue_for_word(word)
            except ValueError:
                invalid_words += 1
                continue
            validated_count += 1
            total_validated += 1
            if multiplier > best_multiplier:
                best_multiplier = multiplier
                best_word = word
            if len(set(word)) > 1 and len(mixed_examples) < 12:
                mixed_examples.append(
                    {
                        "word": list(word),
                        "word_length": length,
                        "total_shift": total_shift,
                        "exact_residue_modulus_bits": exact_bits,
                        "residue_mod_2_to_exact_bits": residue,
                        "residue_hex": hex(residue),
                        "expansion_multiplier": round(multiplier, 10),
                    }
                )
        length_rows.append(
            {
                "word_length": length,
                "expanding_words": expanding_count,
                "mixed_expanding_words": mixed_expanding_count,
                "validated_expanding_words": validated_count,
                "best_expanding_word": list(best_word) if best_word else [],
                "best_multiplier": round(best_multiplier, 10),
                "expansion_cutoff_sum_floor": math.floor(length * log2_3),
            }
        )

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-22",
        "status": "proof_pressure_open",
        "route": "MixedTwoAdicCylinderRank",
        "proof_or_counterexample_mode": "mixed_branch_counterexample_pressure",
        "attempt": (
            "Enumerate realizable accelerated Collatz valuation cylinders and separate expanding branches from the "
            "known 1-cycle. This attacks proof strategies that try to prove a universal fixed-block descent."
        ),
        "bounded_result": {
            "max_word_length": max_length,
            "valuation_alphabet": alphabet,
            "total_expanding_words": total_expanding,
            "total_mixed_expanding_words": total_mixed_expanding,
            "validated_expanding_words": total_validated,
            "invalid_expanding_words": invalid_words,
            "cycle_candidates_seen": list(cycle_candidates.values())[:8],
            "nontrivial_cycle_candidates_seen": [
                row for value, row in cycle_candidates.items() if value != 1
            ],
            "length_rows": length_rows,
            "mixed_expanding_examples": mixed_examples,
        },
        "obstruction": (
            "Many finite mixed valuation cylinders are exact and expanding. This does not produce a Collatz "
            "counterexample, but it blocks any proof that depends on a fixed finite descent block for every residue."
        ),
        "candidate_theorem": (
            "There exists a well-founded rank on 2-adic valuation cylinders such that every expanding finite cylinder "
            "must exit into a strictly lower-ranked cylinder before it can form a positive integer cycle or divergent orbit."
        ),
        "next_experiment": "Search for a cylinder rank that decreases after branch switching, not after a fixed block.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_residue_deletion_obstruction(moduli: list[int]) -> dict[str, object]:
    rows = []
    for modulus in moduli:
        unit_residues = [value for value in range(modulus) if math.gcd(value, modulus) == 1]
        unit_set = set(unit_residues)
        costs = []
        weakest = []
        for residue in range(0, modulus, 2):
            seen = set()
            deletion_cost = 0
            pair_count = 0
            for a_value in unit_residues:
                if a_value in seen:
                    continue
                b_value = (residue - a_value) % modulus
                if b_value not in unit_set:
                    continue
                seen.add(a_value)
                seen.add(b_value)
                deletion_cost += 1
                pair_count += 1
            costs.append(deletion_cost)
            weakest.append({"even_residue": residue, "minimum_residue_deletions": deletion_cost, "pair_orbit_count": pair_count})
        weakest.sort(key=lambda row: (row["minimum_residue_deletions"], row["even_residue"]))
        rows.append(
            {
                "modulus": modulus,
                "unit_residue_count": len(unit_residues),
                "even_residue_count": modulus // 2,
                "minimum_deletions_to_create_local_obstruction": min(costs),
                "maximum_deletions_to_create_local_obstruction": max(costs),
                "mean_deletion_cost": round(sum(costs) / len(costs), 6),
                "weakest_even_residues": weakest[:8],
                "local_obstruction_exists_without_deletion": min(costs) == 0,
            }
        )

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-22",
        "status": "proof_pressure_open",
        "route": "ResidueDeletionObstruction",
        "proof_or_counterexample_mode": "local_counterexample_pressure",
        "attempt": (
            "Treat a hypothetical Goldbach counterexample as a local obstruction problem. For each primorial modulus, "
            "measure how many prime residue classes must be deleted before an even residue loses all unit-sum witnesses."
        ),
        "bounded_result": {
            "modulus_rows": rows,
            "strongest_tested_modulus": rows[-1]["modulus"],
            "strongest_tested_minimum_deletion_cost": rows[-1]["minimum_deletions_to_create_local_obstruction"],
            "local_obstruction_found": any(row["local_obstruction_exists_without_deletion"] for row in rows),
        },
        "obstruction": (
            "Small local residue systems are robust, so a Goldbach counterexample is not explained by a simple modular "
            "missing-class obstruction. The missing proof remains an analytic lower bound for actual prime counts."
        ),
        "candidate_theorem": (
            "A quantitative transference theorem converts residue robustness plus explicit prime distribution error "
            "bounds into a positive representation count for every sufficiently large even integer."
        ),
        "next_experiment": "Use the weakest residue rows as stress cases for explicit major/minor-arc error budgets.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def twin_exact_gap_projection(limits: list[int], primes: list[int], max_gap: int) -> dict[str, object]:
    twin_constant = 0.6601618158468696
    rows = []
    for limit in limits:
        local_primes = [prime for prime in primes if prime <= limit]
        prime_set = set(local_primes)
        deleted = {prime + 2 for prime in local_primes if prime + 2 in prime_set}
        model_primes = [prime for prime in local_primes if prime not in deleted]
        original_gap_counts = Counter()
        model_gap_counts = Counter()
        for left, right in zip(local_primes, local_primes[1:]):
            gap = right - left
            if gap <= max_gap:
                original_gap_counts[gap] += 1
        for left, right in zip(model_primes, model_primes[1:]):
            gap = right - left
            if gap <= max_gap:
                model_gap_counts[gap] += 1
        original_bounded = sum(original_gap_counts.values())
        model_bounded = sum(model_gap_counts.values())
        exact_gap = original_gap_counts.get(2, 0)
        deletion_exact_gap = model_gap_counts.get(2, 0)
        estimate = 2 * twin_constant * limit / (math.log(limit) ** 2) if limit > 2 else 0.0
        rows.append(
            {
                "limit": limit,
                "original_exact_gap_2": exact_gap,
                "deletion_model_exact_gap_2": deletion_exact_gap,
                "exact_gap_projection_margin": exact_gap - deletion_exact_gap,
                "original_bounded_gap_count": original_bounded,
                "deletion_model_bounded_gap_count": model_bounded,
                "bounded_gap_retention_ratio": round(model_bounded / original_bounded, 8) if original_bounded else 0.0,
                "exact_gap_to_bounded_ratio": round(exact_gap / original_bounded, 8) if original_bounded else 0.0,
                "hardy_littlewood_scale_estimate": round(estimate, 6),
                "observed_to_hl_scale_ratio": round(exact_gap / estimate, 8) if estimate else None,
            }
        )

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-22",
        "status": "proof_pressure_open",
        "route": "ExactGapProjection",
        "proof_or_counterexample_mode": "exact_gap_selector_vs_deletion_model",
        "attempt": (
            "Construct the simplest exact-gap projection: it separates true prime data from the deletion model that "
            "preserves many bounded gaps while removing every exact gap-2 pair."
        ),
        "bounded_result": {
            "limits": limits,
            "max_gap": max_gap,
            "projection_rows": rows,
            "last_row": rows[-1],
            "deletion_model_rejected_by_exact_gap_projection": all(row["deletion_model_exact_gap_2"] == 0 for row in rows),
        },
        "obstruction": (
            "The exact-gap projection cleanly rejects the deletion shortcut model, but it is still a finite statistic. "
            "A proof needs an unconditional lower bound showing the projection stays positive arbitrarily far out."
        ),
        "candidate_theorem": (
            "There is an unconditional exact-gap-2 lower-bound functional whose value is positive for primes for "
            "arbitrarily large limits and zero on bounded-gap deletion countermodels."
        ),
        "next_experiment": "Search for sieve weights whose parity obstruction does not collapse the exact-gap projection.",
        "claim_boundary": "No Twin Prime proof. Exact-gap projection evidence is finite and does not prove infinitude.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max(args.twin_limits + [args.goldbach_prime_limit])
    primes, _ = sieve(prime_limit)
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "negation_pressure_open_no_resolution",
        "claim_boundary": (
            "Ticket 22 attempts proof by negation pressure: counterexample search, contrapositive detectors, and "
            "finite obstruction tests. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_li_detector_horizon(args.riemann_search_factor, args.riemann_beta, args.riemann_heights, args.riemann_threshold),
            collatz_mixed_two_adic_cylinder_rank(args.collatz_max_word_length, args.collatz_max_valuation),
            goldbach_residue_deletion_obstruction(args.goldbach_moduli),
            twin_exact_gap_projection(args.twin_limits, primes, args.twin_max_gap),
        ],
    }


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-22-li-detector-horizon.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-22-mixed-two-adic-cylinder-rank.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-22-residue-deletion-obstruction.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-22-exact-gap-projection.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 22 negation-pressure proof attempt lab.")
    parser.add_argument("--riemann-search-factor", type=float, default=4.0)
    parser.add_argument("--riemann-beta", type=float, default=0.75)
    parser.add_argument("--riemann-threshold", type=float, default=-1.0)
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[10.0, 20.0, 50.0, 100.0, 200.0, 500.0])
    parser.add_argument("--collatz-max-word-length", type=int, default=12)
    parser.add_argument("--collatz-max-valuation", type=int, default=3)
    parser.add_argument("--goldbach-moduli", type=int, nargs="+", default=[30, 210, 2310])
    parser.add_argument("--goldbach-prime-limit", type=int, default=300_000)
    parser.add_argument("--twin-limits", type=int, nargs="+", default=[10_000, 100_000, 1_000_000, 2_000_000])
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket22-negation-pressure-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket22 negation pressure lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
