from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.proof-or-counterexample-lab.v1"


def sha256_json(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
    primes = [n for n in range(2, limit + 1) if is_prime[n]]
    return primes, is_prime


def collatz_audit(limit: int, residue_modulus: int, max_steps: int) -> dict[str, object]:
    direct_counterexamples: list[dict[str, object]] = []
    naive_descent_counterexamples: list[dict[str, object]] = []
    residue_stats: dict[int, dict[str, float]] = defaultdict(
        lambda: {"count": 0, "sum_drift": 0.0, "max_drift": -10**9, "min_drift": 10**9}
    )
    max_steps_seen = {"n": 1, "steps": 0, "peak": 1}

    for n in range(2, limit + 1):
        x = n
        peak = n
        steps = 0
        seen: dict[int, int] = {}
        while x != 1 and steps <= max_steps:
            if x in seen:
                direct_counterexamples.append(
                    {"type": "cycle_candidate", "start": n, "repeat_value": x, "steps": steps}
                )
                break
            seen[x] = steps
            x = 3 * x + 1 if x & 1 else x >> 1
            peak = max(peak, x)
            steps += 1
        if steps > max_steps:
            direct_counterexamples.append({"type": "timeout_candidate", "start": n, "steps": steps, "peak": peak})
        if steps > max_steps_seen["steps"]:
            max_steps_seen = {"n": n, "steps": steps, "peak": peak}

    for n in range(1, limit + 1, 2):
        x = 3 * n + 1
        valuation = 0
        while x % 2 == 0:
            x >>= 1
            valuation += 1
        drift = math.log(x / n)
        residue = n % residue_modulus
        stats = residue_stats[residue]
        stats["count"] += 1
        stats["sum_drift"] += drift
        stats["max_drift"] = max(stats["max_drift"], drift)
        stats["min_drift"] = min(stats["min_drift"], drift)
        if x >= n and len(naive_descent_counterexamples) < 25:
            naive_descent_counterexamples.append(
                {"n": n, "accelerated_next": x, "v2_3n_plus_1": valuation, "log_drift": round(drift, 8)}
            )

    residue_pressure = []
    for residue, stats in residue_stats.items():
        count = int(stats["count"])
        mean_drift = stats["sum_drift"] / count if count else 0.0
        residue_pressure.append(
            {
                "residue": residue,
                "count": count,
                "mean_log_drift": round(mean_drift, 8),
                "max_log_drift": round(stats["max_drift"], 8),
                "min_log_drift": round(stats["min_drift"], 8),
            }
        )
    residue_pressure.sort(key=lambda row: row["mean_log_drift"], reverse=True)

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-16",
        "status": "attempted_no_full_resolution",
        "proof_modes": ["direct_counterexample_search", "candidate_theorem_counterexample", "contrapositive_rank_descent"],
        "direct_counterexample": {
            "searched_starts": limit,
            "max_steps": max_steps,
            "found": bool(direct_counterexamples),
            "candidates": direct_counterexamples[:10],
            "max_steps_seen": max_steps_seen,
        },
        "candidate_counterexamples_found": {
            "target_claim": "Every odd accelerated Collatz step descends immediately.",
            "result": "falsified",
            "examples": naive_descent_counterexamples,
        },
        "residue_pressure": {
            "modulus": residue_modulus,
            "top_mean_drift_residues": residue_pressure[:12],
        },
        "contrapositive_route": (
            "If a well-founded residue-debt rank strictly descends on every accelerated transition "
            "or enters the known basin, then any divergent orbit or non-trivial cycle is impossible."
        ),
        "missing_infinite_bridge": "A finite residue-debt certificate must be lifted from sampled residues to all integers.",
        "next_theorem_to_attempt": "CO-TICKET-17 ResidueDebtAutomatonLift",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found in the bounded direct search.",
    }


def goldbach_audit(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    counts = [0] * (limit + 1)
    for i, p in enumerate(primes):
        if p > limit:
            break
        for q in primes[i:]:
            total = p + q
            if total > limit:
                break
            if total % 2 == 0:
                counts[total] += 1

    direct_counterexamples = [n for n in range(4, limit + 1, 2) if counts[n] == 0]
    hard_cases = []
    for n in range(6, limit + 1, 2):
        scale = n / (math.log(n) ** 2)
        normalized = counts[n] / scale if scale > 0 else 0.0
        hard_cases.append({"n": n, "representations": counts[n], "normalized_margin": round(normalized, 8)})
    hard_cases.sort(key=lambda row: (row["representations"], row["normalized_margin"], row["n"]))

    residue_profile = defaultdict(lambda: {"count": 0, "min_representations": 10**9, "min_n": None})
    for n in range(6, limit + 1, 2):
        key = f"mod30={n % 30}"
        residue_profile[key]["count"] += 1
        if counts[n] < residue_profile[key]["min_representations"]:
            residue_profile[key]["min_representations"] = counts[n]
            residue_profile[key]["min_n"] = n

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-16",
        "status": "attempted_no_full_resolution",
        "proof_modes": ["direct_counterexample_search", "candidate_lower_bound_counterexample", "contrapositive_cutoff_bridge"],
        "direct_counterexample": {
            "searched_even_limit": limit,
            "found": bool(direct_counterexamples),
            "candidates": direct_counterexamples[:20],
        },
        "hardest_even_numbers": hard_cases[:20],
        "candidate_counterexamples_found": {
            "target_claim": "A uniform representation lower bound can ignore residue-profile worst cases.",
            "result": "stress_cases_found",
            "examples": hard_cases[:10],
        },
        "residue_profile_minima": dict(sorted(residue_profile.items())),
        "contrapositive_route": (
            "If every even n >= N0 has an explicit positive lower bound for the Goldbach representation count "
            "and every even n < N0 is finitely certified, then a Goldbach counterexample cannot exist."
        ),
        "missing_infinite_bridge": "An unconditional explicit lower bound with cutoff below the finite certificate range.",
        "next_theorem_to_attempt": "GB-TICKET-17 ResidueProfileExplicitCutoff",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found in the bounded direct search.",
    }


def twin_prime_audit(limit: int, primes: list[int], is_prime: bytearray, max_gap: int) -> dict[str, object]:
    twin_starts = [p for p in primes if p + 2 <= limit and is_prime[p + 2]]
    gap_counts = Counter()
    shortcut_counterexamples = []
    for a, b in zip(primes, primes[1:]):
        gap = b - a
        if gap <= max_gap:
            gap_counts[gap] += 1
        if gap > 2 and gap <= max_gap and len(shortcut_counterexamples) < 20:
            shortcut_counterexamples.append({"p": a, "q": b, "gap": gap})

    twin_free_intervals = []
    for a, b in zip(twin_starts, twin_starts[1:]):
        twin_free_intervals.append({"from_twin_start": a, "to_twin_start": b, "distance": b - a})
    twin_free_intervals.sort(key=lambda row: row["distance"], reverse=True)

    bounded_gap_mass = sum(count for gap, count in gap_counts.items() if gap <= max_gap)
    exact_gap_mass = gap_counts.get(2, 0)
    wider_gap_mass = bounded_gap_mass - exact_gap_mass
    leakage_ratio = wider_gap_mass / bounded_gap_mass if bounded_gap_mass else 0.0

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-16",
        "status": "attempted_no_full_resolution",
        "proof_modes": ["finite_evidence_search", "proof_shortcut_counterexample", "contrapositive_exact_gap_lower_bound"],
        "direct_counterexample": {
            "finite_refutation_possible": False,
            "reason": "The negation is an eventual statement: there exists N after which no twin primes occur.",
            "searched_prime_limit": limit,
            "twin_pairs_found": len(twin_starts),
        },
        "gap_distribution": {str(gap): gap_counts[gap] for gap in sorted(gap_counts)},
        "largest_observed_twin_free_intervals": twin_free_intervals[:10],
        "candidate_counterexamples_found": {
            "target_claim": "Bounded prime gaps alone imply exact twin-prime gaps.",
            "result": "falsified_by_wider_gaps",
            "bounded_gap_mass": bounded_gap_mass,
            "exact_gap_mass": exact_gap_mass,
            "wider_gap_mass": wider_gap_mass,
            "leakage_ratio": round(leakage_ratio, 8),
            "examples": shortcut_counterexamples,
        },
        "contrapositive_route": (
            "If an exact gap-2 lower bound grows without bound, then the negation of the twin prime conjecture "
            "is impossible. Bounded-gap evidence must be separated from exact-gap evidence."
        ),
        "missing_infinite_bridge": "A parity-barrier-resistant lower bound for exact gap 2, not just some bounded gap.",
        "next_theorem_to_attempt": "TP-TICKET-17 ExactGapTwoProjection",
        "claim_boundary": "No Twin Prime proof. Finite data cannot refute the eventual no-more-twins negation.",
    }


def riemann_surrogate_audit(li_terms: int) -> dict[str, object]:
    critical_heights = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513]
    zeros: list[complex] = []
    for height in critical_heights:
        zeros.extend([complex(0.5, height), complex(0.5, -height)])

    beta = 0.65
    height = critical_heights[0]
    zeros.extend(
        [
            complex(beta, height),
            complex(1.0 - beta, height),
            complex(beta, -height),
            complex(1.0 - beta, -height),
        ]
    )

    li_coefficients = []
    first_negative = None
    for n in range(1, li_terms + 1):
        value = sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros)
        rounded = round(value, 12)
        li_coefficients.append(rounded)
        if first_negative is None and value < 0:
            first_negative = {"n": n, "lambda_n": rounded}

    min_li = min(li_coefficients)
    finite_prefix_survives = first_negative is None

    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-16",
        "status": "attempted_no_full_resolution",
        "proof_modes": ["candidate_theorem_counterexample", "contrapositive_zero_exclusion", "finite_prefix_obstruction"],
        "direct_counterexample": {
            "searched": False,
            "reason": "This lab does not implement certified zeta zero isolation; it attacks finite-prefix proof routes instead.",
        },
        "surrogate_zero_model": {
            "critical_line_zero_count": len(critical_heights) * 2,
            "off_critical_quartet": [
                {"real": beta, "imag": height},
                {"real": 1.0 - beta, "imag": height},
                {"real": beta, "imag": -height},
                {"real": 1.0 - beta, "imag": -height},
            ],
            "li_terms_checked": li_terms,
            "min_li_coefficient": min_li,
            "first_negative_li": first_negative,
            "finite_prefix_survives": finite_prefix_survives,
        },
        "candidate_counterexamples_found": {
            "target_claim": "A finite Li/Jensen/Hermite prefix can certify RH without a uniform all-index theorem.",
            "result": "falsified_as_proof_strategy",
            "reason": (
                "The constructed symmetric surrogate includes off-critical zeros. Whether finite Li terms detect it or not, "
                "the lesson is the same: a bounded prefix only produces an oracle for candidate routes, not a theorem over all zeros."
            ),
        },
        "contrapositive_route": (
            "Assume an off-critical zero exists. Construct a test kernel or Li-type coefficient that becomes negative. "
            "A valid proof must make this construction uniform over all heights and all off-critical displacements."
        ),
        "missing_infinite_bridge": "Uniform off-critical-zero detector over the full zero set, with no RH-equivalent axiom.",
        "next_theorem_to_attempt": "RH-TICKET-17 UniformOffCriticalDetector",
        "claim_boundary": "No RH proof and no certified RH counterexample. This is a counterexample to finite-prefix proof strategies.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max(args.goldbach_limit, args.twin_limit)
    primes, is_prime = sieve(prime_limit)
    results = [
        riemann_surrogate_audit(args.riemann_li_terms),
        collatz_audit(args.collatz_limit, args.collatz_residue_modulus, args.collatz_max_steps),
        goldbach_audit(args.goldbach_limit, [p for p in primes if p <= args.goldbach_limit], is_prime),
        twin_prime_audit(args.twin_limit, [p for p in primes if p <= args.twin_limit], is_prime, args.twin_max_gap),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "attempted_no_full_resolution",
        "claim_boundary": (
            "The lab can find direct counterexamples if they occur inside the bounded search, and can falsify proof routes. "
            "It does not claim a proof of any open problem."
        ),
        "limits": {
            "riemann_li_terms": args.riemann_li_terms,
            "collatz_limit": args.collatz_limit,
            "collatz_residue_modulus": args.collatz_residue_modulus,
            "goldbach_limit": args.goldbach_limit,
            "twin_limit": args.twin_limit,
            "twin_max_gap": args.twin_max_gap,
        },
        "problems": results,
    }
    payload["payload_sha256"] = sha256_json({k: v for k, v in payload.items() if k != "payload_sha256"})
    return payload


def write_problem_artifacts(payload: dict[str, object]) -> None:
    mapping = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-16-proof-or-counterexample.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-16-proof-or-counterexample.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-16-proof-or-counterexample.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-16-proof-or-counterexample.json",
    }
    for problem in payload["problems"]:
        write_json(mapping[str(problem["problem_id"])], problem)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run proof-or-counterexample probes for the four open-problem pages.")
    parser.add_argument("--riemann-li-terms", type=int, default=80)
    parser.add_argument("--collatz-limit", type=int, default=100_000)
    parser.add_argument("--collatz-residue-modulus", type=int, default=64)
    parser.add_argument("--collatz-max-steps", type=int, default=10_000)
    parser.add_argument("--goldbach-limit", type=int, default=100_000)
    parser.add_argument("--twin-limit", type=int, default=200_000)
    parser.add_argument("--twin-max-gap", type=int, default=40)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/proof-or-counterexample-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_problem_artifacts(payload)
    print(f"proof-or-counterexample lab written to {args.output}")
    print(payload["payload_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
