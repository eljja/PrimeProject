from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket21-two-adic-branch-lab.v1"


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
        raise ValueError("v2(0) is undefined here")
    count = 0
    value = abs(n)
    while value % 2 == 0:
        count += 1
        value //= 2
    return count


def accelerated_odd_step(n: int) -> tuple[int, int]:
    value = 3 * n + 1
    valuation = v2(value)
    return value >> valuation, valuation


def riemann_prefix_evasion(max_n: int, beta: float, heights: list[float]) -> dict[str, object]:
    rows = []
    for height in heights:
        zeros = [
            complex(beta, height),
            complex(1.0 - beta, height),
            complex(beta, -height),
            complex(1.0 - beta, -height),
        ]
        values = []
        for n in range(1, max_n + 1):
            values.append(sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros))
        max_abs = max(abs(value) for value in values)
        rows.append(
            {
                "height": height,
                "max_abs_prefix_effect": round(max_abs, 18),
                "height_times_max_abs": round(height * max_abs, 12),
                "height_squared_times_max_abs": round(height * height * max_abs, 8),
            }
        )
    best = min(rows, key=lambda row: row["max_abs_prefix_effect"])
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-21",
        "status": "proof_pressure_open",
        "route": "PrefixEvasionQuantifier",
        "proof_or_counterexample_mode": "finite_prefix_countermodel_quantifier",
        "attempt": (
            "Quantify the countermodel pressure against finite Li-prefix proof routes: as surrogate off-critical zero "
            "height grows, its first-prefix effect becomes arbitrarily small in the tested family."
        ),
        "bounded_result": {
            "li_terms_checked": max_n,
            "offcritical_beta": beta,
            "height_rows": rows,
            "best_evasion_row": best,
            "finite_prefix_claim_status": "blocked_without_uniform_tail_theorem",
        },
        "obstruction": (
            "No fixed finite prefix can rule out sufficiently high off-critical behavior by itself. A proof must include "
            "a theorem that quantifies over the entire zero set or the entire Li sequence."
        ),
        "candidate_theorem": (
            "For every off-critical zero, a height-uniform detector bound produces a contradiction in the Li/kernel "
            "sequence before any finite certificate is promoted."
        ),
        "next_experiment": "Turn the empirical height table into a symbolic N,H,Re(rho) inequality.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_two_adic_branch_exclusion(lengths: list[int]) -> dict[str, object]:
    rows = []
    for length in lengths:
        seed = (1 << (length + 1)) - 1
        x = seed
        valuations = []
        for _ in range(length):
            x, valuation = accelerated_odd_step(x)
            valuations.append(valuation)
        exit_next, exit_valuation = accelerated_odd_step(x)
        predicted_exit_valuation = 1 + v2((3 ** (length + 1)) - 1)
        rows.append(
            {
                "shadow_length": length,
                "seed_formula": f"2^{length + 1} - 1",
                "seed_hex": hex(seed),
                "all_ones_prefix_verified": valuations == [1] * length,
                "state_after_prefix_formula": f"2*3^{length} - 1",
                "state_after_prefix_hex": hex(x),
                "exit_valuation": exit_valuation,
                "predicted_exit_valuation": predicted_exit_valuation,
                "exit_matches_formula": exit_valuation == predicted_exit_valuation,
                "state_after_exit_hex": hex(exit_next),
                "asymptotic_multiplier": round((3.0 / 2.0) ** length, 12),
            }
        )

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-21",
        "status": "proof_pressure_open",
        "route": "TwoAdicBranchExclusion",
        "proof_or_counterexample_mode": "partial_branch_theorem_plus_open_global_rank",
        "attempt": (
            "Prove the simplest 2-adic obstruction is not a positive-integer counterexample: finite positive shadows of "
            "the all-ones branch eventually leave that branch because v2(n+1) is finite."
        ),
        "bounded_result": {
            "shadow_lengths_checked": lengths,
            "longest_shadow_length": rows[-1]["shadow_length"],
            "longest_shadow_seed_hex": rows[-1]["seed_hex"],
            "longest_exit_valuation": rows[-1]["exit_valuation"],
            "all_rows_match_exit_formula": all(row["exit_matches_formula"] for row in rows),
            "branch_exclusion_statement": (
                "If n is a positive odd integer and s=v2(n+1), then n can follow the all-ones accelerated branch for "
                "at most s-1 steps; an infinite all-ones branch would require n=-1 in the 2-adics, not a positive integer."
            ),
            "shadow_rows": rows,
        },
        "obstruction": (
            "This closes only the all-ones 2-adic branch. Collatz still needs a global rank or cover for every other "
            "valuation-prefix branch and every possible branch switching pattern."
        ),
        "candidate_theorem": (
            "Every expanding 2-adic branch shadow has finite positive-integer escape depth and escapes into a lower-ranked "
            "valuation-prefix state, yielding a global well-founded rank."
        ),
        "next_experiment": "Generalize from the all-ones branch to mixed expanding valuation-prefix cylinders.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_witness_spectrum(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    witness_counts = Counter()
    hardest = None
    direct_counterexamples = []
    for n in range(4, limit + 1, 2):
        witness = None
        for p in primes:
            if p > n // 2:
                break
            if is_prime[n - p]:
                witness = p
                break
        if witness is None:
            direct_counterexamples.append(n)
            continue
        witness_counts[witness] += 1
        if hardest is None or witness > hardest["smallest_witness_prime"]:
            hardest = {
                "even": n,
                "smallest_witness_prime": witness,
                "partner": n - witness,
            }
    top_witnesses = [
        {"smallest_witness_prime": p, "even_count": count}
        for p, count in witness_counts.most_common(12)
    ]
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-21",
        "status": "proof_pressure_open",
        "route": "WitnessSpectrum",
        "proof_or_counterexample_mode": "bounded_counterexample_search_plus_witness_distribution",
        "attempt": (
            "Search direct bounded counterexamples and measure the smallest-prime witness spectrum. This tests whether "
            "finite failures concentrate in rare witness classes, while keeping the finite-to-infinite boundary explicit."
        ),
        "bounded_result": {
            "even_limit": limit,
            "direct_counterexample_count": len(direct_counterexamples),
            "direct_counterexamples": direct_counterexamples[:20],
            "distinct_smallest_witness_primes": len(witness_counts),
            "hardest_smallest_witness_case": hardest,
            "top_smallest_witness_primes": top_witnesses,
        },
        "obstruction": (
            "A bounded witness spectrum is not a lower-bound theorem for all larger even integers. It can guide which "
            "minor-arc or exceptional cases matter, but it does not close the conjecture."
        ),
        "candidate_theorem": (
            "An explicit analytic lower bound proves every sufficiently large even integer has at least one prime-pair "
            "witness, and finite witness certificates cover all smaller even integers."
        ),
        "next_experiment": "Use the hardest witness cases to stress explicit lower-bound constants.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def twin_deletion_persistence_ladder(limits: list[int], primes: list[int], max_gap: int) -> dict[str, object]:
    rows = []
    for limit in limits:
        local_primes = [p for p in primes if p <= limit]
        prime_set = set(local_primes)
        deleted = {p + 2 for p in local_primes if p + 2 in prime_set}
        model_primes = [p for p in local_primes if p not in deleted]
        original_gap_counts = Counter()
        model_gap_counts = Counter()
        for p, q in zip(local_primes, local_primes[1:]):
            gap = q - p
            if gap <= max_gap:
                original_gap_counts[gap] += 1
        for p, q in zip(model_primes, model_primes[1:]):
            gap = q - p
            if gap <= max_gap:
                model_gap_counts[gap] += 1
        original_bounded = sum(original_gap_counts.values())
        model_bounded = sum(model_gap_counts.values())
        rows.append(
            {
                "limit": limit,
                "original_exact_gap_2": original_gap_counts.get(2, 0),
                "deletion_model_exact_gap_2": model_gap_counts.get(2, 0),
                "original_bounded_gap_count": original_bounded,
                "deletion_model_bounded_gap_count": model_bounded,
                "bounded_gap_retention_ratio": round(model_bounded / original_bounded, 8) if original_bounded else 0.0,
                "deleted_prime_count": len(deleted),
            }
        )
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-21",
        "status": "proof_pressure_open",
        "route": "DeletionPersistenceLadder",
        "proof_or_counterexample_mode": "bounded_gap_shortcut_countermodel_ladder",
        "attempt": (
            "Repeat the exact-gap deletion countermodel over increasing limits. A valid twin-prime proof must defeat "
            "this bounded-gap-only model, not merely show bounded gaps persist."
        ),
        "bounded_result": {
            "limits": limits,
            "max_gap": max_gap,
            "rows": rows,
            "last_row": rows[-1],
        },
        "obstruction": (
            "The countermodel keeps many bounded gaps while deleting exact gap 2 in every tested range. This blocks "
            "proof routes that silently replace exact gap 2 with bounded-gap mass."
        ),
        "candidate_theorem": (
            "An exact-gap lower-bound functional remains positive for true primes but cannot be mimicked by deletion "
            "models that preserve wider bounded gaps."
        ),
        "next_experiment": "Optimize signed exact-gap projection weights against the deletion ladder.",
        "claim_boundary": "No Twin Prime proof. Deletion persistence remains a countermodel to bounded-gap shortcut proofs.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max(args.goldbach_limit, max(args.twin_limits))
    primes, is_prime = sieve(prime_limit)
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "proof_pressure_open_no_resolution",
        "claim_boundary": (
            "Ticket 21 closes only narrow proof-pressure subgoals. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_prefix_evasion(args.riemann_li_terms, args.riemann_beta, args.riemann_heights),
            collatz_two_adic_branch_exclusion(args.collatz_shadow_lengths),
            goldbach_witness_spectrum(args.goldbach_limit, [p for p in primes if p <= args.goldbach_limit], is_prime),
            twin_deletion_persistence_ladder(args.twin_limits, [p for p in primes if p <= max(args.twin_limits)], args.twin_max_gap),
        ],
    }
    return payload


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-21-prefix-evasion-quantifier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-21-two-adic-branch-exclusion.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-21-witness-spectrum.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-21-deletion-persistence-ladder.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 21 two-adic branch proof-pressure lab.")
    parser.add_argument("--riemann-li-terms", type=int, default=200)
    parser.add_argument("--riemann-beta", type=float, default=0.75)
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[1_000.0, 10_000.0, 100_000.0, 1_000_000.0, 10_000_000.0])
    parser.add_argument("--collatz-shadow-lengths", type=int, nargs="+", default=[1, 2, 4, 8, 16, 32, 64, 96, 128])
    parser.add_argument("--goldbach-limit", type=int, default=200_000)
    parser.add_argument("--twin-limits", type=int, nargs="+", default=[10_000, 50_000, 100_000, 300_000, 1_000_000])
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket21-two-adic-branch-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket21 two-adic branch lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
