from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket19-proof-pressure-lab.v1"


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


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def riemann_tail_pressure(max_n: int, beta: float, heights: list[float], epsilons: list[float]) -> dict[str, object]:
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
            value = sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros)
            values.append(value)
        max_abs = max(abs(value) for value in values)
        rows.append(
            {
                "height": height,
                "beta": beta,
                "terms_checked": max_n,
                "max_abs_prefix_effect": round(max_abs, 14),
                "min_prefix_effect": round(min(values), 14),
                "max_prefix_effect": round(max(values), 14),
            }
        )

    epsilon_rows = []
    for epsilon in epsilons:
        first = next((row for row in rows if row["max_abs_prefix_effect"] <= epsilon), None)
        epsilon_rows.append(
            {
                "epsilon": epsilon,
                "first_tested_height_below_epsilon": first["height"] if first else None,
                "status": "witnessed_in_test_grid" if first else "not_reached_in_test_grid",
            }
        )

    best = min(rows, key=lambda row: row["max_abs_prefix_effect"]) if rows else None
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-19",
        "status": "proof_pressure_open",
        "route": "TailUniformityPressure",
        "proof_or_counterexample_mode": "finite_prefix_countermodel_family",
        "attempt": (
            "Pressure-test finite-prefix RH proof routes by moving an off-critical surrogate quartet to increasing "
            "heights and measuring how invisible it becomes to the first Li-type coefficients."
        ),
        "bounded_result": {
            "li_terms_checked": max_n,
            "offcritical_beta": beta,
            "height_grid": heights,
            "epsilon_targets": epsilon_rows,
            "best_camouflage_row": best,
            "camouflage_rows": rows,
        },
        "obstruction": (
            "For any fixed prefix, high-height off-critical surrogate data can be made weakly visible in that prefix. "
            "A valid RH proof must therefore include a uniform tail theorem, not only checked positivity."
        ),
        "candidate_theorem": (
            "Every off-critical zero forces a Li/kernel contradiction with an explicit height-uniform bound, or the "
            "explicit formula tail is controlled strongly enough that finite-prefix camouflage is impossible."
        ),
        "next_experiment": "Derive a symbolic upper bound for finite-prefix visibility as a function of N and zero height.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_branch_graph_rank_pressure(max_steps: int) -> dict[str, object]:
    rows = []
    for steps in range(1, max_steps + 1):
        threshold = math.floor(steps * math.log2(3))
        expanding_count = 0
        expanding_density = 0.0
        total_density = 0.0
        for total_shift in range(steps, threshold + 1):
            count = binomial(total_shift - 1, steps - 1)
            expanding_count += count
            expanding_density += count * (2.0 ** (-total_shift))
        # The full probability mass over all positive valuation words of this length is 1.
        # The finite sum below is tracked to make the exact density calculation auditable.
        for total_shift in range(steps, steps + 80):
            total_density += binomial(total_shift - 1, steps - 1) * (2.0 ** (-total_shift))
        rows.append(
            {
                "odd_accelerated_steps": steps,
                "expanding_shift_threshold": threshold,
                "expanding_word_count": expanding_count,
                "expanding_density": round(expanding_density, 12),
                "truncated_total_density_check": round(total_density, 12),
                "all_ones_multiplier": round((3.0 / 2.0) ** steps, 12),
                "all_ones_density": round(2.0 ** (-steps), 12),
            }
        )

    hardest = max(rows, key=lambda row: row["expanding_density"])
    last = rows[-1]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-19",
        "status": "proof_pressure_open",
        "route": "BranchGraphRankSearch",
        "proof_or_counterexample_mode": "fixed_block_contraction_counterexample_plus_rank_target",
        "attempt": (
            "Use exact valuation-word densities to test whether a fixed accelerated block length can prove global "
            "Collatz descent. Every tested length has expanding valuation words, including the all-ones word."
        ),
        "bounded_result": {
            "max_odd_accelerated_steps": max_steps,
            "rows": rows,
            "highest_expanding_density_row": hardest,
            "last_step_row": last,
            "fixed_block_contraction_status": "falsified_for_tested_lengths",
        },
        "obstruction": (
            "Uniform fixed-block contraction fails because finite expanding valuation words are always realizable. "
            "A proof needs a branch graph rank that handles expanding prefixes by routing them to later descent."
        ),
        "candidate_theorem": (
            "There exists a well-founded rank on exact valuation-prefix states such that every expanding prefix either "
            "enters a smaller verified basin or is followed by a finite extension with strictly lower rank."
        ),
        "next_experiment": "Search ordinal-valued or lexicographic ranks on exact valuation-prefix automata instead of fixed block contraction.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_local_obstruction_pressure(moduli: list[int]) -> dict[str, object]:
    rows = []
    for modulus in moduli:
        unit_residues = [r for r in range(modulus) if math.gcd(r, modulus) == 1]
        covered = set()
        for a in unit_residues:
            for b in unit_residues:
                covered.add((a + b) % modulus)
        even_residues = [r for r in range(0, modulus, 2)] if modulus % 2 == 0 else list(range(modulus))
        uncovered = [r for r in even_residues if r not in covered]
        rows.append(
            {
                "modulus": modulus,
                "unit_residue_count": len(unit_residues),
                "target_residue_count": len(even_residues),
                "covered_target_residue_count": len(even_residues) - len(uncovered),
                "uncovered_target_residues": uncovered[:20],
                "uncovered_count": len(uncovered),
            }
        )

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-19",
        "status": "proof_pressure_open",
        "route": "LocalObstructionElimination",
        "proof_or_counterexample_mode": "modular_counterexample_search",
        "attempt": (
            "Search for local modular obstructions to Goldbach using unit prime residues over primorial-style moduli. "
            "If an even residue cannot be expressed as a sum of two prime-eligible residues, that would identify a "
            "structural counterexample route."
        ),
        "bounded_result": {
            "moduli_checked": moduli,
            "rows": rows,
            "total_uncovered_residue_classes": sum(row["uncovered_count"] for row in rows),
        },
        "obstruction": (
            "No tested local modular obstruction appears. This pushes the proof obligation back to analytic lower "
            "bounds for representation counts rather than congruence compatibility."
        ),
        "candidate_theorem": (
            "After local compatibility is certified for primorial residue systems, an explicit circle-method or sieve "
            "lower bound proves every sufficiently large even integer has a positive representation count."
        ),
        "next_experiment": "Combine local compatibility with sourced explicit major/minor arc constants.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def twin_local_and_deletion_pressure(limit: int, primes: list[int], max_gap: int, local_primes: list[int]) -> dict[str, object]:
    admissibility_rows = []
    for p in local_primes:
        forbidden = {0 % p, (-2) % p}
        admissibility_rows.append(
            {
                "prime_modulus": p,
                "forbidden_residue_count": len(forbidden),
                "available_residue_count": p - len(forbidden),
                "admissible": len(forbidden) < p,
            }
        )

    prime_set = set(primes)
    deleted = {p + 2 for p in primes if p + 2 in prime_set}
    model_primes = [p for p in primes if p not in deleted]
    original_gap_counts = Counter()
    model_gap_counts = Counter()
    for p, q in zip(primes, primes[1:]):
        gap = q - p
        if gap <= max_gap:
            original_gap_counts[gap] += 1
    for p, q in zip(model_primes, model_primes[1:]):
        gap = q - p
        if gap <= max_gap:
            model_gap_counts[gap] += 1

    original_bounded = sum(original_gap_counts.values())
    model_bounded = sum(model_gap_counts.values())
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-19",
        "status": "proof_pressure_open",
        "route": "AdmissibilityVsExactGap",
        "proof_or_counterexample_mode": "local_admissibility_plus_deletion_countermodel",
        "attempt": (
            "Separate two facts that are often conflated: the twin pattern is locally admissible, but local "
            "admissibility and bounded-gap survival do not force exact gap-2 infinitude."
        ),
        "bounded_result": {
            "prime_limit": limit,
            "max_gap": max_gap,
            "local_admissibility_rows": admissibility_rows,
            "all_tested_local_patterns_admissible": all(row["admissible"] for row in admissibility_rows),
            "original_exact_gap_2": original_gap_counts.get(2, 0),
            "deletion_model_exact_gap_2": model_gap_counts.get(2, 0),
            "original_bounded_gap_count": original_bounded,
            "deletion_model_bounded_gap_count": model_bounded,
            "bounded_gap_retention_ratio": round(model_bounded / original_bounded, 8) if original_bounded else 0.0,
        },
        "obstruction": (
            "Admissibility is necessary but far from sufficient. A finite deletion model can pass local pattern logic "
            "and retain many bounded gaps while killing every observed exact twin gap."
        ),
        "candidate_theorem": (
            "An exact-gap projection theorem must prove positive gap-2 mass after all admissible wider-gap and parity "
            "countermodels are subtracted with unconditional error control."
        ),
        "next_experiment": "Search exact-gap projection weights that reject deletion countermodels and preserve certified prime mass.",
        "claim_boundary": "No Twin Prime proof. Local admissibility and bounded gaps still do not prove exact gap-2 infinitude.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    primes, _ = sieve(max(args.twin_limit, max(args.twin_local_primes)))
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "proof_pressure_open_no_resolution",
        "claim_boundary": (
            "Ticket 19 applies proof pressure to direct proof, counterexample, and contrapositive routes. It does not "
            "claim a proof or disproof of any of the four open problems."
        ),
        "attempts": [
            riemann_tail_pressure(args.riemann_li_terms, args.riemann_beta, args.riemann_heights, args.riemann_epsilons),
            collatz_branch_graph_rank_pressure(args.collatz_max_steps),
            goldbach_local_obstruction_pressure(args.goldbach_moduli),
            twin_local_and_deletion_pressure(
                args.twin_limit,
                [p for p in primes if p <= args.twin_limit],
                args.twin_max_gap,
                args.twin_local_primes,
            ),
        ],
    }
    return payload


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-19-tail-uniformity-pressure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-19-branch-graph-rank-search.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-19-local-obstruction-elimination.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-19-admissibility-vs-exact-gap.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 19 proof-pressure lab for four open problems.")
    parser.add_argument("--riemann-li-terms", type=int, default=200)
    parser.add_argument("--riemann-beta", type=float, default=0.75)
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[1_000.0, 10_000.0, 100_000.0, 1_000_000.0, 10_000_000.0])
    parser.add_argument("--riemann-epsilons", type=float, nargs="+", default=[1e-3, 1e-6, 1e-9])
    parser.add_argument("--collatz-max-steps", type=int, default=32)
    parser.add_argument("--goldbach-moduli", type=int, nargs="+", default=[6, 30, 210, 2310])
    parser.add_argument("--twin-limit", type=int, default=300_000)
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--twin-local-primes", type=int, nargs="+", default=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket19-proof-pressure-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket19 proof pressure lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
