from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket24-bridge-weight-lab.v1"


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


def scan_li_detector(beta: float, height: float, threshold: float, search_limit: int) -> dict[str, object]:
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
    for index in range(1, search_limit + 1):
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
    return {
        "offcritical_beta": beta,
        "height": height,
        "search_limit": search_limit,
        "first_negative_li_index": first_negative,
        "first_below_threshold_index": first_threshold,
        "threshold_seen": first_threshold is not None,
        "minimum_value_seen": round(min_value, 12),
        "minimum_index_seen": min_index,
        "threshold_index_over_height_squared": (
            round(first_threshold / (height * height), 8) if first_threshold else None
        ),
    }


def riemann_uniform_detector_budget(
    betas: list[float],
    heights: list[float],
    threshold: float,
    search_cap: int,
) -> dict[str, object]:
    rows = []
    for beta in betas:
        for height in heights:
            rows.append(scan_li_detector(beta, height, threshold, search_cap))

    seen = [row for row in rows if row["threshold_seen"]]
    by_beta: dict[str, list[float]] = {}
    for row in seen:
        key = str(row["offcritical_beta"])
        by_beta.setdefault(key, []).append(float(row["threshold_index_over_height_squared"]))

    fitted = [
        {
            "offcritical_beta": float(beta),
            "seen_case_count": len(values),
            "mean_threshold_index_over_height_squared": round(sum(values) / len(values), 8),
            "max_threshold_index_over_height_squared": round(max(values), 8),
            "projected_index_at_height_1000": int(math.ceil(max(values) * 1_000_000)),
        }
        for beta, values in sorted(by_beta.items(), key=lambda item: float(item[0]))
    ]
    missed = [row for row in rows if not row["threshold_seen"]]
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-24",
        "status": "proof_pressure_open",
        "route": "UniformDetectorBudget",
        "proof_or_counterexample_mode": "finite_prefix_evasion_budget",
        "attempt": (
            "Convert the off-critical-zero detector experiment into a budget table: if the detector index grows like "
            "height squared, any fixed finite Li-prefix can be evaded by sufficiently high surrogate zeros."
        ),
        "bounded_result": {
            "threshold": threshold,
            "search_cap": search_cap,
            "detector_budget_rows": rows,
            "missed_threshold_cases": missed,
            "missed_threshold_case_count": len(missed),
            "quadratic_budget_fit": fitted,
            "finite_prefix_evasion_status": "observed_for_tested_surrogates" if missed else "not_seen_in_test_grid",
        },
        "obstruction": (
            "The budget table can refute a fixed-prefix proof strategy, but it cannot prove RH or produce a zeta "
            "counterexample. A valid proof still needs an explicit formula theorem that is uniform over all zeros."
        ),
        "candidate_theorem": (
            "A uniform all-height detector theorem bounds the Li/kernel index needed to expose every off-critical "
            "zero and subtracts the contribution of the remaining zero set with explicit constants."
        ),
        "next_experiment": "Replace the empirical height-squared fit with a symbolic inequality in the explicit formula.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def build_collatz_graph(bits: int) -> tuple[list[int], list[int], list[int], int]:
    modulus = 1 << bits
    residues = list(range(1, modulus, 2))
    index_by_residue = {residue: index for index, residue in enumerate(residues)}
    edges = []
    valuations = []
    ambiguous_edges = 0
    for residue in residues:
        value = 3 * residue + 1
        valuation = v2(value)
        if valuation >= bits:
            ambiguous_edges += 1
        edges.append(index_by_residue[((value >> valuation) % modulus)])
        valuations.append(valuation)
    return residues, edges, valuations, ambiguous_edges


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
        next_value = 3 * value + 1
        actual = v2(next_value)
        value = next_value >> actual
        if actual != expected:
            return False
    return value == candidate


def collatz_lift_status(word: list[int]) -> dict[str, object]:
    total_shift, constant = affine_for_word(word)
    denominator = (1 << total_shift) - (3 ** len(word))
    multiplier = (3 ** len(word)) / (2 ** total_shift)
    if denominator <= 0:
        return {
            "affine_cycle_status": "globally_eliminated_expanding_word",
            "candidate_value": None,
            "validated_as_exact_cycle": False,
            "total_shift": total_shift,
            "expansion_multiplier": round(multiplier, 12),
        }
    if constant % denominator != 0:
        return {
            "affine_cycle_status": "globally_eliminated_nonintegral_fixed_point",
            "candidate_value": None,
            "validated_as_exact_cycle": False,
            "total_shift": total_shift,
            "expansion_multiplier": round(multiplier, 12),
        }
    candidate = constant // denominator
    valid = candidate > 0 and candidate % 2 == 1 and validate_collatz_cycle(word, candidate)
    return {
        "affine_cycle_status": "valid_positive_cycle" if valid else "globally_eliminated_invalid_fixed_point",
        "candidate_value": candidate,
        "validated_as_exact_cycle": valid,
        "total_shift": total_shift,
        "expansion_multiplier": round(multiplier, 12),
    }


def collatz_lift_aware_rank_probe(modulus_bits: list[int]) -> dict[str, object]:
    rows = []
    false_cycles = []
    positive_cycles = []
    first_clean_bits = None
    for bits in modulus_bits:
        residues, edges, valuations, ambiguous_edges = build_collatz_graph(bits)
        components = tarjan_scc(edges)
        cycle_components = [component for component in components if len(component) > 1 or edges[component[0]] == component[0]]
        nontrivial_components = [component for component in cycle_components if len(component) > 1]
        if first_clean_bits is None and len(cycle_components) == 1 and len(cycle_components[0]) == 1:
            cycle_residues, word = ordered_cycle(cycle_components[0], edges, valuations, residues)
            status = collatz_lift_status(word)
            if status["candidate_value"] == 1:
                first_clean_bits = bits

        cycle_examples = []
        for component in sorted(cycle_components, key=len, reverse=True)[:8]:
            cycle_residues, word = ordered_cycle(component, edges, valuations, residues)
            status = collatz_lift_status(word)
            example = {
                "cycle_length": len(cycle_residues),
                "sample_residues": cycle_residues[:16],
                "valuation_word": word,
                **status,
            }
            cycle_examples.append(example)
            if status["affine_cycle_status"] == "valid_positive_cycle":
                positive_cycles.append({"modulus_bits": bits, **example})
            elif len(cycle_residues) > 1:
                false_cycles.append({"modulus_bits": bits, **example})

        nondecreasing_edges = sum(1 for index, target in enumerate(edges) if residues[target] >= residues[index])
        rows.append(
            {
                "modulus_bits": bits,
                "odd_state_count": len(residues),
                "scc_count": len(components),
                "cycle_component_count": len(cycle_components),
                "nontrivial_cycle_component_count": len(nontrivial_components),
                "largest_cycle_component_size": max(len(component) for component in cycle_components),
                "ambiguous_high_valuation_edges": ambiguous_edges,
                "integer_rank_nondecreasing_edges": nondecreasing_edges,
                "integer_rank_nondecreasing_rate": round(nondecreasing_edges / len(residues), 8),
                "cycle_examples": cycle_examples,
            }
        )

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-24",
        "status": "proof_pressure_open",
        "route": "LiftAwareRankProbe",
        "proof_or_counterexample_mode": "quotient_cycle_lift_elimination",
        "attempt": (
            "Push the Collatz quotient-cycle witnesses through an affine lift audit. A modular SCC is accepted as a "
            "true cycle candidate only if its valuation word has a positive integral fixed point that validates exactly."
        ),
        "bounded_result": {
            "modulus_bits_tested": modulus_bits,
            "lift_rows": rows,
            "first_tested_modulus_with_only_known_cycle": first_clean_bits,
            "false_quotient_cycles_eliminated_by_affine_lift": false_cycles[:10],
            "false_quotient_cycle_count": len(false_cycles),
            "positive_cycle_candidates_seen": positive_cycles[:10],
            "nontrivial_positive_cycle_candidates_seen": [
                row for row in positive_cycles if row.get("candidate_value") != 1
            ],
        },
        "obstruction": (
            "The affine lift audit removes the tested false quotient cycles and leaves only the known 1-cycle, but it "
            "does not prove that every larger modulus and every divergent branch admits a well-founded descent rank."
        ),
        "candidate_theorem": (
            "Every finite quotient SCC of the accelerated Collatz map either fails the affine lift cycle condition or "
            "is the known 1-cycle, and all non-cyclic branches eventually enter a lower exact-cylinder rank."
        ),
        "next_experiment": "Formalize the affine lift elimination lemma and then attack the non-cyclic branch rank.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def first_goldbach_witness(even: int, primes: list[int], is_prime: bytearray) -> tuple[int, int] | None:
    for prime in primes:
        if prime > even // 2:
            break
        if is_prime[even - prime]:
            return prime, even - prime
    return None


def goldbach_representation_count(even: int, primes: list[int], is_prime: bytearray) -> int:
    count = 0
    for prime in primes:
        if prime > even // 2:
            break
        if is_prime[even - prime]:
            count += 1
    return count


def goldbach_explicit_window_budget(limit: int, sample_stride: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    counterexamples = []
    hardest_first = {"even": None, "smallest_prime": 0, "partner": None}
    for even in range(4, limit + 1, 2):
        witness = first_goldbach_witness(even, primes, is_prime)
        if witness is None:
            counterexamples.append(even)
            break
        if witness[0] > hardest_first["smallest_prime"]:
            hardest_first = {"even": even, "smallest_prime": witness[0], "partner": witness[1]}

    sampled_rows = []
    weakest_count = None
    weakest_ratio = None
    for even in range(max(10_000, sample_stride), limit + 1, sample_stride):
        if even % 2:
            even += 1
        count = goldbach_representation_count(even, primes, is_prime)
        scale = even / (math.log(even) ** 2)
        ratio = count / scale if scale else 0.0
        row = {
            "even": even,
            "representation_count": count,
            "n_over_log_squared_n": round(scale, 6),
            "count_to_scale_ratio": round(ratio, 8),
        }
        sampled_rows.append(row)
        if weakest_count is None or count < weakest_count["representation_count"]:
            weakest_count = row
        if weakest_ratio is None or ratio < weakest_ratio["count_to_scale_ratio"]:
            weakest_ratio = row

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-24",
        "status": "proof_pressure_open",
        "route": "ExplicitWindowBudget",
        "proof_or_counterexample_mode": "counterexample_search_plus_lower_bound_stress",
        "attempt": (
            "Combine direct counterexample search with sampled representation-count stress tests. The aim is to see "
            "which finite windows are weakest for an eventual explicit positive lower bound."
        ),
        "bounded_result": {
            "search_limit": limit,
            "sample_stride": sample_stride,
            "counterexamples_found": counterexamples,
            "first_counterexample": counterexamples[0] if counterexamples else None,
            "hardest_first_witness": hardest_first,
            "sampled_count_rows": sampled_rows[:30],
            "sampled_count_row_count": len(sampled_rows),
            "weakest_sampled_representation_count": weakest_count,
            "weakest_sampled_count_to_scale_ratio": weakest_ratio,
            "exceptional_set_status": "empty_through_bound" if not counterexamples else "counterexample_found",
        },
        "obstruction": (
            "The sampled count budget can identify weak finite windows, but the conjecture needs a theorem proving a "
            "positive representation count for all sufficiently large even integers, not just sampled or bounded ones."
        ),
        "candidate_theorem": (
            "An explicit circle-method lower bound proves r_2(N) > 0 for every even N >= N0, with finite verified "
            "coverage for all even N < N0."
        ),
        "next_experiment": "Use the weakest sampled windows to tune explicit major/minor-arc error budgets.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def gap_counts(primes: list[int], max_gap: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for left, right in zip(primes, primes[1:]):
        gap = right - left
        if gap <= max_gap:
            counts[gap] += 1
    return counts


def twin_exact_gap_weight_search(limits: list[int], primes: list[int], max_gap: int) -> dict[str, object]:
    rows = []
    for limit in limits:
        local_primes = [prime for prime in primes if prime <= limit]
        local_set = set(local_primes)
        deleted_right_twins = {prime + 2 for prime in local_primes if prime + 2 in local_set}
        deletion_model = [prime for prime in local_primes if prime not in deleted_right_twins]
        original_counts = gap_counts(local_primes, max_gap)
        deletion_counts = gap_counts(deletion_model, max_gap)
        original_bounded_without_two = sum(count for gap, count in original_counts.items() if gap != 2)
        deletion_bounded_without_two = sum(count for gap, count in deletion_counts.items() if gap != 2)
        bounded_total = sum(original_counts.values())
        deletion_total = sum(deletion_counts.values())
        exact_gap = original_counts.get(2, 0)
        row = {
            "limit": limit,
            "original_exact_gap_2": exact_gap,
            "deletion_model_exact_gap_2": deletion_counts.get(2, 0),
            "exact_gap_weight_margin": exact_gap - deletion_counts.get(2, 0),
            "bounded_gap_total": bounded_total,
            "deletion_model_bounded_gap_total": deletion_total,
            "bounded_gap_retention_ratio": round(deletion_total / bounded_total, 8) if bounded_total else 0.0,
            "bounded_without_gap_2": original_bounded_without_two,
            "deletion_bounded_without_gap_2": deletion_bounded_without_two,
            "bounded_without_gap_2_retention_ratio": (
                round(deletion_bounded_without_two / original_bounded_without_two, 8)
                if original_bounded_without_two
                else 0.0
            ),
            "gap_head": [
                {
                    "gap": gap,
                    "original_count": original_counts.get(gap, 0),
                    "deletion_model_count": deletion_counts.get(gap, 0),
                }
                for gap in (2, 4, 6, 8, 10, 12)
            ],
        }
        rows.append(row)

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-24",
        "status": "proof_pressure_open",
        "route": "ExactGapWeightSearch",
        "proof_or_counterexample_mode": "exact_gap_weight_vs_bounded_gap_shortcut",
        "attempt": (
            "Compare exact-gap-2 and bounded-gap-only weights on true prime data and a deletion model that removes "
            "every twin pair. This tests whether the proposed statistic is really an exact-gap statistic."
        ),
        "bounded_result": {
            "limits": limits,
            "max_gap": max_gap,
            "weight_rows": rows,
            "last_row": rows[-1],
            "bounded_only_weight_is_fooled": all(row["bounded_without_gap_2_retention_ratio"] > 0.95 for row in rows),
            "exact_gap_weight_separates_deletion_model": all(row["exact_gap_weight_margin"] > 0 for row in rows),
        },
        "obstruction": (
            "The exact-gap weight separates the finite deletion model, but a proof needs a lower bound showing that "
            "this exact-gap weight remains positive arbitrarily far out without Hardy-Littlewood assumptions."
        ),
        "candidate_theorem": (
            "There is an unconditional nonnegative exact-gap-2 sieve weight with a positive lower bound for infinitely "
            "many scales and with a fully explicit parity-error term."
        ),
        "next_experiment": "Search for exact-gap weights whose main term and parity-error budget can be written as a formal inequality.",
        "claim_boundary": "No Twin Prime proof. Exact-gap weight evidence is finite and not an infinitude proof.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max([args.goldbach_limit, *args.twin_limits])
    primes, is_prime = sieve(prime_limit)
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "bridge_weight_open_no_resolution",
        "claim_boundary": (
            "Ticket 24 tests proof-bridge candidates and exact-gap weights. It does not prove or disprove RH, "
            "Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_uniform_detector_budget(
                args.riemann_betas,
                args.riemann_heights,
                args.riemann_threshold,
                args.riemann_search_cap,
            ),
            collatz_lift_aware_rank_probe(args.collatz_modulus_bits),
            goldbach_explicit_window_budget(args.goldbach_limit, args.goldbach_sample_stride, primes, is_prime),
            twin_exact_gap_weight_search(args.twin_limits, primes, args.twin_max_gap),
        ],
    }


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-24-uniform-detector-budget.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-24-lift-aware-rank-probe.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-24-explicit-window-budget.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-24-exact-gap-weight-search.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 24 proof-bridge and weight lab.")
    parser.add_argument("--riemann-betas", type=float, nargs="+", default=[0.6, 0.75, 0.9])
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[100.0, 200.0, 500.0])
    parser.add_argument("--riemann-threshold", type=float, default=-1.0)
    parser.add_argument("--riemann-search-cap", type=int, default=1_000_000)
    parser.add_argument("--collatz-modulus-bits", type=int, nargs="+", default=[8, 10, 12, 14, 16, 18])
    parser.add_argument("--goldbach-limit", type=int, default=2_000_000)
    parser.add_argument("--goldbach-sample-stride", type=int, default=2_000)
    parser.add_argument("--twin-limits", type=int, nargs="+", default=[100_000, 1_000_000, 2_000_000, 3_000_000])
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket24-bridge-weight-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket24 bridge weight lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
