from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket23-cegis-rank-lab.v1"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for prime in range(2, int(limit**0.5) + 1):
        if is_prime[prime]:
            start = prime * prime
            is_prime[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return [value for value in range(2, limit + 1) if is_prime[value]], is_prime


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is undefined")
    count = 0
    value = abs(value)
    while value % 2 == 0:
        count += 1
        value //= 2
    return count


def riemann_detector_bound_cegis(
    betas: list[float],
    heights: list[float],
    max_search_index: int,
    threshold: float,
) -> dict[str, object]:
    rows = []
    missed = []
    for beta in betas:
        displacement = abs(beta - 0.5)
        for height in heights:
            zeros = [
                complex(beta, height),
                complex(1.0 - beta, height),
                complex(beta, -height),
                complex(1.0 - beta, -height),
            ]
            factors = [1.0 - 1.0 / zero for zero in zeros]
            powers = [1.0 + 0.0j for _ in zeros]
            first_negative = None
            first_threshold = None
            min_value = float("inf")
            min_index = 0
            for index in range(1, max_search_index + 1):
                for factor_index, factor in enumerate(factors):
                    powers[factor_index] *= factor
                contribution = len(zeros) - sum(value.real for value in powers)
                if contribution < min_value:
                    min_value = contribution
                    min_index = index
                if first_negative is None and contribution < 0.0:
                    first_negative = index
                if first_threshold is None and contribution < threshold:
                    first_threshold = index
                    break
            row = {
                "offcritical_beta": beta,
                "displacement_from_half": round(displacement, 8),
                "height": height,
                "search_limit": max_search_index,
                "first_negative_li_index": first_negative,
                "first_below_threshold_index": first_threshold,
                "threshold": threshold,
                "minimum_value_seen": round(min_value, 12),
                "minimum_index_seen": min_index,
                "threshold_seen": first_threshold is not None,
                "threshold_index_over_height_squared": (
                    round(first_threshold / (height * height), 8) if first_threshold else None
                ),
            }
            rows.append(row)
            if first_threshold is None:
                missed.append(row)

    seen = [row for row in rows if row["threshold_seen"]]
    worst_seen = max(
        seen,
        key=lambda row: float(row["threshold_index_over_height_squared"] or 0.0),
    )
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-23",
        "status": "proof_pressure_open",
        "route": "DetectorBoundCEGIS",
        "proof_or_counterexample_mode": "contrapositive_detector_bound_cegis",
        "attempt": (
            "Treat an off-critical zero quartet as an adversary and test whether a fixed Li-type detector prefix can "
            "force a negative witness uniformly across height and displacement."
        ),
        "bounded_result": {
            "offcritical_betas": betas,
            "heights": heights,
            "uniform_prefix_tested_index": max_search_index,
            "threshold": threshold,
            "detector_rows": rows,
            "missed_threshold_cases": missed,
            "missed_threshold_case_count": len(missed),
            "worst_seen_threshold_case": worst_seen,
            "cegis_interpretation": (
                "A fixed finite prefix is refuted as a proof route when an allowed surrogate case has no threshold "
                "witness inside that prefix."
            ),
        },
        "obstruction": (
            "The experiment supplies counterexamples to finite-prefix detector claims, not to RH. A real "
            "contrapositive proof must prove an explicit all-height detector bound and control interference from the "
            "rest of the zero set."
        ),
        "candidate_theorem": (
            "For every off-critical zero displacement delta and height T, a Li/kernel witness below an explicit "
            "N(delta,T) becomes negative after subtracting a rigorously bounded contribution from all other zeros."
        ),
        "next_experiment": "Turn the empirical N(delta,T) table into a symbolic inequality in the explicit formula.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def build_collatz_graph(bits: int) -> tuple[list[int], list[int], list[int], int]:
    modulus = 1 << bits
    odds = list(range(1, modulus, 2))
    index_by_residue = {residue: index for index, residue in enumerate(odds)}
    edges = []
    valuations = []
    ambiguous_edges = 0
    for residue in odds:
        value = 3 * residue + 1
        valuation = v2(value)
        if valuation >= bits:
            ambiguous_edges += 1
        next_residue = (value >> valuation) % modulus
        edges.append(index_by_residue[next_residue])
        valuations.append(valuation)
    return odds, edges, valuations, ambiguous_edges


def tarjan_scc(edges: list[int]) -> list[list[int]]:
    index = 0
    stack: list[int] = []
    on_stack = [False] * len(edges)
    indices = [-1] * len(edges)
    lows = [0] * len(edges)
    components: list[list[int]] = []

    def visit(node: int) -> None:
        nonlocal index
        indices[node] = index
        lows[node] = index
        index += 1
        stack.append(node)
        on_stack[node] = True

        target = edges[node]
        if indices[target] < 0:
            visit(target)
            lows[node] = min(lows[node], lows[target])
        elif on_stack[target]:
            lows[node] = min(lows[node], indices[target])

        if lows[node] == indices[node]:
            component = []
            while True:
                target = stack.pop()
                on_stack[target] = False
                component.append(target)
                if target == node:
                    break
            components.append(component)

    for node in range(len(edges)):
        if indices[node] < 0:
            visit(node)
    return components


def ordered_cycle(component: list[int], edges: list[int], valuations: list[int], residues: list[int]) -> tuple[list[int], list[int]]:
    start = component[0]
    seen: set[int] = set()
    cycle_residues = []
    word = []
    current = start
    while current not in seen:
        seen.add(current)
        cycle_residues.append(residues[current])
        word.append(valuations[current])
        current = edges[current]
    return cycle_residues, word


def affine_for_word(word: list[int]) -> tuple[int, int]:
    total_shift = 0
    constant = 0
    for valuation in word:
        constant = 3 * constant + (1 << total_shift)
        total_shift += valuation
    return total_shift, constant


def validate_collatz_cycle(word: list[int], candidate: int) -> bool:
    value = candidate
    for expected in word:
        step_value = 3 * value + 1
        actual = v2(step_value)
        value = step_value >> actual
        if actual != expected:
            return False
    return value == candidate


def collatz_cycle_candidate(word: list[int]) -> dict[str, object]:
    total_shift, constant = affine_for_word(word)
    denominator = (1 << total_shift) - (3 ** len(word))
    if denominator <= 0:
        return {
            "candidate_value": None,
            "candidate_status": "no_positive_affine_fixed_point_expanding_word",
            "total_shift": total_shift,
        }
    if constant % denominator != 0:
        return {
            "candidate_value": None,
            "candidate_status": "nonintegral_affine_fixed_point",
            "total_shift": total_shift,
        }
    candidate = constant // denominator
    valid = candidate > 0 and candidate % 2 == 1 and validate_collatz_cycle(word, candidate)
    return {
        "candidate_value": candidate,
        "candidate_status": "valid_positive_cycle" if valid else "invalid_positive_cycle_candidate",
        "total_shift": total_shift,
        "validated_as_exact_cycle": valid,
    }


def collatz_cylinder_rank_cegis(modulus_bits: list[int]) -> dict[str, object]:
    rows = []
    false_cycles = []
    positive_cycles = []
    for bits in modulus_bits:
        residues, edges, valuations, ambiguous_edges = build_collatz_graph(bits)
        components = tarjan_scc(edges)
        cycle_components = [component for component in components if len(component) > 1 or edges[component[0]] == component[0]]
        integer_nondecrease_edges = sum(1 for index, target in enumerate(edges) if residues[target] >= residues[index])
        cycle_examples = []
        for component in sorted(cycle_components, key=len, reverse=True)[:6]:
            cycle_residues, word = ordered_cycle(component, edges, valuations, residues)
            candidate = collatz_cycle_candidate(word)
            multiplier = (3 ** len(word)) / (2 ** sum(word))
            example = {
                "cycle_length": len(cycle_residues),
                "sample_residues": cycle_residues[:16],
                "valuation_word": word,
                "valuation_sum": sum(word),
                "expansion_multiplier": round(multiplier, 12),
                **candidate,
            }
            cycle_examples.append(example)
            if candidate.get("candidate_status") == "valid_positive_cycle":
                positive_cycles.append({"modulus_bits": bits, **example})
            elif len(cycle_residues) > 1:
                false_cycles.append({"modulus_bits": bits, **example})

        valuation_histogram = Counter(valuations)
        rows.append(
            {
                "modulus_bits": bits,
                "odd_state_count": len(residues),
                "scc_count": len(components),
                "cycle_component_count": len(cycle_components),
                "nontrivial_cycle_component_count": sum(1 for component in cycle_components if len(component) > 1),
                "largest_cycle_component_size": max(len(component) for component in cycle_components),
                "ambiguous_high_valuation_edges": ambiguous_edges,
                "integer_rank_nondecreasing_edges": integer_nondecrease_edges,
                "integer_rank_nondecreasing_rate": round(integer_nondecrease_edges / len(residues), 8),
                "valuation_histogram_head": [
                    {"valuation": valuation, "count": count}
                    for valuation, count in valuation_histogram.most_common(8)
                ],
                "cycle_examples": cycle_examples,
            }
        )

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-23",
        "status": "proof_pressure_open",
        "route": "CylinderRankCEGIS",
        "proof_or_counterexample_mode": "rank_synthesis_counterexample_guided_search",
        "attempt": (
            "Build finite odd-residue quotient graphs for the accelerated Collatz map, search for SCC obstructions to "
            "simple rank descent, and audit whether quotient cycles lift to true positive integer cycles."
        ),
        "bounded_result": {
            "modulus_bits_tested": modulus_bits,
            "modulus_rows": rows,
            "false_quotient_cycles_seen": false_cycles[:8],
            "false_quotient_cycle_count": len(false_cycles),
            "positive_cycle_candidates_seen": positive_cycles[:8],
            "nontrivial_positive_cycle_candidates_seen": [
                row for row in positive_cycles if row.get("candidate_value") != 1
            ],
            "rank_probe": (
                "The ordinary integer residue rank has about one third nondecreasing edges on tested quotients, and "
                "finite quotient SCCs can be false cycles unless the rank is lift-aware."
            ),
        },
        "obstruction": (
            "Finite quotient SCCs are useful CEGIS witnesses against naive rank functions, but false quotient cycles "
            "are not Collatz counterexamples. The missing theorem is a lift-aware well-founded rank over exact "
            "2-adic cylinders."
        ),
        "candidate_theorem": (
            "There exists a computable well-founded rank on exact accelerated valuation cylinders such that every "
            "positive integer branch either reaches the 1-cycle or eventually crosses to a strictly lower rank."
        ),
        "next_experiment": "Synthesize lift-aware rank features from exact residue, valuation debt, and escape depth.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_exceptional_set_cegis(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    counterexamples = []
    hardest = {"even": None, "smallest_prime": 0, "partner": None}
    sample_targets = {4, 6, 8, 10, 100, 1000, 10_000, 100_000, limit}
    samples = []
    buckets = Counter()
    for even in range(4, limit + 1, 2):
        witness = None
        for prime in primes:
            if prime > even // 2:
                break
            if is_prime[even - prime]:
                witness = (prime, even - prime)
                break
        if witness is None:
            counterexamples.append(even)
            break
        if witness[0] > hardest["smallest_prime"]:
            hardest = {"even": even, "smallest_prime": witness[0], "partner": witness[1]}
        if even in sample_targets:
            samples.append({"even": even, "p": witness[0], "q": witness[1]})
        for cutoff in (3, 5, 11, 101, 1000):
            if witness[0] <= cutoff:
                buckets[f"smallest_p_le_{cutoff}"] += 1
                break
        else:
            buckets["smallest_p_gt_1000"] += 1

    tested_even_values = max(0, (limit - 2) // 2)
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-23",
        "status": "proof_pressure_open",
        "route": "ExceptionalSetCEGIS",
        "proof_or_counterexample_mode": "direct_counterexample_search_plus_hardest_witness",
        "attempt": (
            "Search directly for a Goldbach counterexample up to the bound and record the hardest smallest-prime "
            "witness, because any proof candidate must explain those stress cases rather than only average behavior."
        ),
        "bounded_result": {
            "search_limit": limit,
            "tested_even_values": tested_even_values,
            "counterexamples_found": counterexamples,
            "first_counterexample": counterexamples[0] if counterexamples else None,
            "hardest_smallest_prime_witness": hardest,
            "sample_decompositions": samples,
            "smallest_witness_bucket_counts": dict(buckets),
            "exceptional_set_status": "empty_through_bound" if not counterexamples else "counterexample_found",
        },
        "obstruction": (
            "An empty bounded exceptional set is not a proof. The proof gap is an explicit lower bound that remains "
            "positive for every sufficiently large even integer, plus finite verification below the cutoff."
        ),
        "candidate_theorem": (
            "A quantitative circle-method or transference theorem proves the Goldbach representation count is positive "
            "for all even N >= N0, with a separately certified finite check below N0."
        ),
        "next_experiment": "Use the hardest smallest-prime witnesses as stress targets for explicit major/minor arc budgets.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def gap_counts(primes: list[int], max_gap: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for left, right in zip(primes, primes[1:]):
        gap = right - left
        if gap <= max_gap:
            counts[gap] += 1
    return counts


def twin_parity_projection_cegis(limits: list[int], primes: list[int], max_gap: int) -> dict[str, object]:
    rows = []
    for limit in limits:
        local_primes = [prime for prime in primes if prime <= limit]
        local_set = set(local_primes)
        deleted_right_twins = {prime + 2 for prime in local_primes if prime + 2 in local_set}
        deletion_model = [prime for prime in local_primes if prime not in deleted_right_twins]
        original_counts = gap_counts(local_primes, max_gap)
        deletion_counts = gap_counts(deletion_model, max_gap)
        original_bounded = sum(original_counts.values())
        deletion_bounded = sum(deletion_counts.values())
        row = {
            "limit": limit,
            "original_exact_gap_2": original_counts.get(2, 0),
            "deletion_model_exact_gap_2": deletion_counts.get(2, 0),
            "original_bounded_gap_count": original_bounded,
            "deletion_model_bounded_gap_count": deletion_bounded,
            "bounded_gap_retention_ratio": round(deletion_bounded / original_bounded, 8) if original_bounded else 0.0,
            "gap_head": [
                {
                    "gap": gap,
                    "original_count": original_counts.get(gap, 0),
                    "deletion_model_count": deletion_counts.get(gap, 0),
                    "difference": original_counts.get(gap, 0) - deletion_counts.get(gap, 0),
                }
                for gap in (2, 4, 6, 8, 10, 12)
            ],
        }
        rows.append(row)

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-23",
        "status": "proof_pressure_open",
        "route": "ParityProjectionCEGIS",
        "proof_or_counterexample_mode": "bounded_gap_shortcut_falsification",
        "attempt": (
            "Compare prime data with a deletion model that removes every exact gap-2 pair while preserving most "
            "bounded-gap mass, then ask which projection can distinguish the two."
        ),
        "bounded_result": {
            "limits": limits,
            "max_gap": max_gap,
            "projection_rows": rows,
            "last_row": rows[-1],
            "bounded_gap_shortcut_fails": all(
                row["deletion_model_exact_gap_2"] == 0 and row["bounded_gap_retention_ratio"] > 0.85
                for row in rows
            ),
            "exact_gap_projection_survives_finite_test": all(row["original_exact_gap_2"] > 0 for row in rows),
        },
        "obstruction": (
            "This rejects a bounded-gap shortcut, not the twin-prime negation. A proof needs an unconditional exact "
            "gap-2 lower bound that survives the parity obstruction."
        ),
        "candidate_theorem": (
            "A sieve or dynamical projection gives a positive lower bound for exact gap-2 prime pairs for arbitrarily "
            "large limits, while vanishing on deletion models that keep only wider bounded gaps."
        ),
        "next_experiment": "Search for exact-gap weights whose main term is positive and whose parity-error term is explicit.",
        "claim_boundary": "No Twin Prime proof. The exact-gap projection remains finite evidence only.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max([args.goldbach_limit, *args.twin_limits])
    primes, is_prime = sieve(prime_limit)
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "cegis_rank_open_no_resolution",
        "claim_boundary": (
            "Ticket 23 performs counterexample-guided proof pressure and rank synthesis tests. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_detector_bound_cegis(
                args.riemann_betas,
                args.riemann_heights,
                args.riemann_max_search_index,
                args.riemann_threshold,
            ),
            collatz_cylinder_rank_cegis(args.collatz_modulus_bits),
            goldbach_exceptional_set_cegis(args.goldbach_limit, primes, is_prime),
            twin_parity_projection_cegis(args.twin_limits, primes, args.twin_max_gap),
        ],
    }


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-23-detector-bound-cegis.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-23-cylinder-rank-cegis.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-23-exceptional-set-cegis.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-23-parity-projection-cegis.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 23 CEGIS rank proof-pressure lab.")
    parser.add_argument("--riemann-betas", type=float, nargs="+", default=[0.6, 0.75, 0.9])
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[20.0, 50.0, 100.0, 200.0])
    parser.add_argument("--riemann-max-search-index", type=int, default=180_000)
    parser.add_argument("--riemann-threshold", type=float, default=-1.0)
    parser.add_argument("--collatz-modulus-bits", type=int, nargs="+", default=[8, 10, 12, 14])
    parser.add_argument("--goldbach-limit", type=int, default=1_000_000)
    parser.add_argument("--twin-limits", type=int, nargs="+", default=[100_000, 1_000_000, 2_000_000, 3_000_000])
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket23-cegis-rank-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket23 CEGIS rank lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
