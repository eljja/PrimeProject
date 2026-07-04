from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket20-valuation-prefix-lab.v1"


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


def accelerated_odd_step(n: int) -> tuple[int, int]:
    value = 3 * n + 1
    valuation = 0
    while value % 2 == 0:
        value //= 2
        valuation += 1
    return value, valuation


def valuation_prefix(n: int, steps: int) -> list[int]:
    values = []
    x = n
    for _ in range(steps):
        x, valuation = accelerated_odd_step(x)
        values.append(valuation)
    return values


def all_ones_residue(length: int) -> tuple[list[int], int]:
    if length < 1:
        raise ValueError("length must be positive")
    residues = [3]
    modulus = 4
    current = 1
    while current < length:
        next_modulus = modulus * 2
        next_residues = []
        for residue in residues:
            for lift in (residue, residue + modulus):
                if valuation_prefix(lift, current + 1) == [1] * (current + 1):
                    next_residues.append(lift)
        residues = sorted(set(next_residues))
        modulus = next_modulus
        current += 1
        if not residues:
            raise RuntimeError(f"failed to extend all-ones residue to length {current}")
    return residues, modulus


def riemann_prefix_uniformity_contract(max_n: int, beta: float, heights: list[float]) -> dict[str, object]:
    rows = []
    for height in heights:
        zeros = [
            complex(beta, height),
            complex(1.0 - beta, height),
            complex(beta, -height),
            complex(1.0 - beta, -height),
        ]
        prefix_values = []
        for n in range(1, max_n + 1):
            value = sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros)
            prefix_values.append(value)
        max_abs = max(abs(value) for value in prefix_values)
        rows.append(
            {
                "height": height,
                "max_abs_prefix_effect": round(max_abs, 16),
                "scaled_by_height_squared": round(max_abs * height * height, 8),
                "terms_checked": max_n,
            }
        )
    best = min(rows, key=lambda row: row["max_abs_prefix_effect"])
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-20",
        "status": "proof_pressure_open",
        "route": "UniformTailContract",
        "proof_or_counterexample_mode": "contrapositive_tail_requirement",
        "attempt": (
            "Convert finite-prefix camouflage into a proof obligation: any RH route using Li-type positivity must state "
            "a uniform tail contract strong enough to forbid high-height off-critical zero camouflage."
        ),
        "bounded_result": {
            "li_terms_checked": max_n,
            "offcritical_beta": beta,
            "height_rows": rows,
            "best_camouflage_row": best,
            "observed_scaling": "prefix effect decays roughly with high zero height in this surrogate family",
        },
        "obstruction": (
            "Finite computations can be made insensitive to sufficiently high surrogate off-critical zeros. The missing "
            "artifact is a symbolic tail bound tied to the actual zeta zero set."
        ),
        "candidate_theorem": (
            "A height-uniform explicit-formula tail theorem proves that every off-critical zeta zero forces a detectable "
            "negative Li/kernel witness before any finite proof-status gate is allowed to close."
        ),
        "next_experiment": "Formalize the tail contract as an inequality over zero height, displacement, and Li index.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_all_ones_prefix_lab(lengths: list[int]) -> dict[str, object]:
    rows = []
    for length in lengths:
        residues, modulus = all_ones_residue(length)
        residue = residues[0]
        affine_constant = (3**length) - (2**length)
        values = valuation_prefix(residue, length)
        rows.append(
            {
                "prefix_length": length,
                "modulus_bits": int(math.log2(modulus)),
                "residue_count": len(residues),
                "sample_residue_hex": hex(residue),
                "valuation_prefix_verified": values == [1] * length,
                "asymptotic_multiplier": round((3.0 / 2.0) ** length, 12),
                "odd_density_exact": f"{len(residues)} / 2^{length}",
                "odd_density_float": float(len(residues) / (modulus // 2)),
                "affine_constant_hex": hex(affine_constant),
                "branch_formula": f"T^{length}(n) = (3^{length} n + (3^{length} - 2^{length})) / 2^{length}",
            }
        )

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-20",
        "status": "proof_pressure_open",
        "route": "ValuationPrefixRankCEGIS",
        "proof_or_counterexample_mode": "exact_expanding_prefix_certificate",
        "attempt": (
            "Construct exact residue certificates for the all-ones accelerated valuation prefix. This gives a concrete "
            "expanding branch at every tested finite length, so a proof must use rank/extension logic rather than fixed block contraction."
        ),
        "bounded_result": {
            "prefix_lengths": lengths,
            "longest_prefix_length": rows[-1]["prefix_length"],
            "longest_prefix_residue_hex": rows[-1]["sample_residue_hex"],
            "longest_prefix_multiplier": rows[-1]["asymptotic_multiplier"],
            "longest_prefix_odd_density": rows[-1]["odd_density_exact"],
            "all_ones_rows": rows,
            "longest_prefix": rows[-1],
        },
        "obstruction": (
            "Every finite tested length has an exact expanding residue branch. This does not create a Collatz counterexample, "
            "but it blocks any proof that claims a universal fixed-length contraction."
        ),
        "candidate_theorem": (
            "The infinite all-ones 2-adic branch is excluded from positive integers by a well-founded valuation-prefix rank, "
            "and every finite expanding prefix has a certified extension into a lower-ranked descending branch."
        ),
        "next_experiment": "Run CEGIS over valuation-prefix states to synthesize the first nontrivial well-founded rank.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_unit_pair_multiplicity(moduli: list[int]) -> dict[str, object]:
    rows = []
    for modulus in moduli:
        unit_residues = [r for r in range(modulus) if math.gcd(r, modulus) == 1]
        counts: dict[int, int] = defaultdict(int)
        for a in unit_residues:
            for b in unit_residues:
                counts[(a + b) % modulus] += 1
        targets = list(range(0, modulus, 2)) if modulus % 2 == 0 else list(range(modulus))
        target_counts = [counts[target] for target in targets]
        rows.append(
            {
                "modulus": modulus,
                "unit_residue_count": len(unit_residues),
                "target_residue_count": len(targets),
                "uncovered_target_count": sum(1 for count in target_counts if count == 0),
                "min_ordered_unit_pair_count": min(target_counts),
                "max_ordered_unit_pair_count": max(target_counts),
                "mean_ordered_unit_pair_count": round(sum(target_counts) / len(target_counts), 8),
            }
        )

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-20",
        "status": "proof_pressure_open",
        "route": "LocalMultiplicityBarrier",
        "proof_or_counterexample_mode": "local_counterexample_elimination",
        "attempt": (
            "Strengthen the local obstruction test by measuring how many ordered unit-residue prime pairs cover each "
            "even residue class. A local counterexample route would need uncovered or extremely thin classes."
        ),
        "bounded_result": {
            "moduli_checked": moduli,
            "rows": rows,
            "uncovered_total": sum(row["uncovered_target_count"] for row in rows),
        },
        "obstruction": (
            "The tested primorial residue systems have no uncovered even target classes. Goldbach remains an analytic "
            "lower-bound problem, not a local congruence obstruction in these systems."
        ),
        "candidate_theorem": (
            "Local multiplicity plus explicit major/minor arc estimates gives a positive lower bound for every sufficiently "
            "large even integer, with the remaining small range covered by certificate."
        ),
        "next_experiment": "Attach explicit analytic constants to the strongest local multiplicity rows.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def twin_admissibility_constant_pressure(limit: int, primes: list[int], local_primes: list[int], max_gap: int) -> dict[str, object]:
    product = 1.0
    local_rows = []
    for p in local_primes:
        forbidden = {0 % p, (-2) % p}
        admissible = len(forbidden) < p
        factor = None
        if p > 2:
            factor = (1.0 - len(forbidden) / p) / ((1.0 - 1.0 / p) ** 2)
            product *= factor
        local_rows.append(
            {
                "prime_modulus": p,
                "forbidden_residue_count": len(forbidden),
                "available_residue_count": p - len(forbidden),
                "admissible": admissible,
                "singular_factor": round(factor, 12) if factor is not None else None,
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
        "ticket_id": "TP-TICKET-20",
        "status": "proof_pressure_open",
        "route": "AdmissibilityConstantVsDeletion",
        "proof_or_counterexample_mode": "singular_series_pressure_plus_countermodel",
        "attempt": (
            "Compute the positive local singular-series pressure for the twin pattern, then compare it with a deletion "
            "countermodel that preserves many bounded gaps while eliminating observed exact gap-2 pairs."
        ),
        "bounded_result": {
            "prime_limit": limit,
            "local_rows": local_rows,
            "partial_singular_product_without_factor_2": round(product, 12),
            "partial_two_c2_estimate": round(2.0 * product, 12),
            "original_exact_gap_2": original_gap_counts.get(2, 0),
            "deletion_model_exact_gap_2": model_gap_counts.get(2, 0),
            "original_bounded_gap_count": original_bounded,
            "deletion_model_bounded_gap_count": model_bounded,
            "bounded_gap_retention_ratio": round(model_bounded / original_bounded, 8) if original_bounded else 0.0,
        },
        "obstruction": (
            "Positive local singular-series pressure is heuristic support, not an unconditional lower bound. The deletion "
            "countermodel keeps this distinction visible by killing exact gap 2 in finite data."
        ),
        "candidate_theorem": (
            "An unconditional exact-gap lower-bound theorem converts positive admissible local density into infinitely many "
            "actual gap-2 prime pairs while defeating deletion and parity countermodels."
        ),
        "next_experiment": "Search for an exact-gap lower-bound functional that has positive mass on primes and nonpositive mass on deletion models.",
        "claim_boundary": "No Twin Prime proof. Positive local constants and bounded-gap retention still do not prove exact gap-2 infinitude.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    primes, _ = sieve(max(args.twin_limit, max(args.twin_local_primes)))
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "proof_pressure_open_no_resolution",
        "claim_boundary": (
            "Ticket 20 sharpens proof-pressure certificates. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_prefix_uniformity_contract(args.riemann_li_terms, args.riemann_beta, args.riemann_heights),
            collatz_all_ones_prefix_lab(args.collatz_lengths),
            goldbach_unit_pair_multiplicity(args.goldbach_moduli),
            twin_admissibility_constant_pressure(
                args.twin_limit,
                [p for p in primes if p <= args.twin_limit],
                args.twin_local_primes,
                args.twin_max_gap,
            ),
        ],
    }
    return payload


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-20-uniform-tail-contract.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-20-valuation-prefix-rank-cegis.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-20-local-multiplicity-barrier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-20-admissibility-constant-vs-deletion.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 20 valuation-prefix proof-pressure lab.")
    parser.add_argument("--riemann-li-terms", type=int, default=200)
    parser.add_argument("--riemann-beta", type=float, default=0.75)
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[1_000.0, 10_000.0, 100_000.0, 1_000_000.0, 10_000_000.0])
    parser.add_argument("--collatz-lengths", type=int, nargs="+", default=[1, 2, 4, 8, 16, 32, 64])
    parser.add_argument("--goldbach-moduli", type=int, nargs="+", default=[6, 30, 210, 2310])
    parser.add_argument("--twin-limit", type=int, default=300_000)
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--twin-local-primes", type=int, nargs="+", default=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket20-valuation-prefix-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket20 valuation-prefix lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
