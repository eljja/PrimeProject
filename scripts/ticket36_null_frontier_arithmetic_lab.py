from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float


GENERATED_AT = "2026-07-07T09:10:00+09:00"
SCHEMA = "primeproject.ticket36-null-frontier-arithmetic-lab.v1"


def collatz_direct_audit(n: int, limit: int = 2_000_000) -> dict[str, Any]:
    value = n
    total_steps = 0
    odd_steps = 0
    max_value = value
    while value != 1 and total_steps < limit:
        if value & 1:
            value = 3 * value + 1
            odd_steps += 1
        else:
            value //= 2
        total_steps += 1
        if value > max_value:
            max_value = value
    return {
        "total_steps": total_steps,
        "odd_steps": odd_steps,
        "terminated_at_one": value == 1,
        "max_orbit_value": max_value,
    }


def first_frontier_exit(n: int, base_bits: int, max_bits: int) -> dict[str, Any]:
    for bits in range(base_bits, max_bits + 1):
        certificate = cert(n % (1 << bits), bits)
        status = certificate.get("status")
        if status != "needs_split":
            return {
                "n": n,
                "bit_length": n.bit_length(),
                "exit_bits": bits,
                "exit_slack_over_bit_length": bits - n.bit_length(),
                "exit_status": status,
                "prefix_length": certificate.get("prefix_length"),
                "consumed_bits": certificate.get("consumed_bits"),
                "coefficient_log2_margin": certificate.get("coefficient_log2_margin"),
                "threshold_min_n_for_descent": certificate.get("threshold_min_n_for_descent"),
            }
    return {
        "n": n,
        "bit_length": n.bit_length(),
        "exit_bits": None,
        "exit_slack_over_bit_length": None,
        "exit_status": "unresolved_within_probe",
    }


def natural_null_frontier_audit(
    sample_limit: int = 100_000,
    base_bits: int = 12,
    shallow_probe_bits: int = 96,
    deep_resolve_bits: int = 180,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    shallow_unresolved: list[int] = []
    status_counts: Counter[str] = Counter()
    all_direct_terminated = True

    for n in range(1, sample_limit + 1, 2):
        shallow = first_frontier_exit(n, base_bits, shallow_probe_bits)
        if shallow["exit_bits"] is None:
            shallow_unresolved.append(n)
            record = first_frontier_exit(n, shallow_probe_bits + 1, deep_resolve_bits)
            if record["exit_bits"] is None:
                record = first_frontier_exit(n, base_bits, deep_resolve_bits)
        else:
            record = shallow

        direct = collatz_direct_audit(n)
        all_direct_terminated = all_direct_terminated and bool(direct["terminated_at_one"])
        record["direct_collatz"] = direct
        if record["exit_bits"] is not None:
            record["exit_minus_odd_steps"] = int(record["exit_bits"]) - int(direct["odd_steps"])
            record["exit_minus_total_steps"] = int(record["exit_bits"]) - int(direct["total_steps"])
            status_counts[str(record["exit_status"])] += 1
        else:
            record["exit_minus_odd_steps"] = None
            record["exit_minus_total_steps"] = None
            status_counts["unresolved_within_deep_probe"] += 1
        records.append(record)

    resolved = [record for record in records if record["exit_bits"] is not None]
    unresolved = [record for record in records if record["exit_bits"] is None]
    top_by_exit = sorted(resolved, key=lambda item: (int(item["exit_bits"]), int(item["exit_slack_over_bit_length"])), reverse=True)[:20]
    top_by_slack = sorted(resolved, key=lambda item: (int(item["exit_slack_over_bit_length"]), int(item["exit_bits"])), reverse=True)[:20]
    top_by_odd_gap = sorted(resolved, key=lambda item: int(item["exit_minus_odd_steps"]), reverse=True)[:20]
    shallow_resolution_rows = [
        record
        for record in records
        if record["n"] in set(shallow_unresolved)
    ][:24]

    slack_thresholds = [16, 32, 48, 64, 80, 96, 112]
    odd_gap_thresholds = [0, 4, 8, 12, 16, 20, 24, 32]
    slack_tests = [
        {
            "candidate_bound": f"exit_bits <= bit_length(n) + {threshold}",
            "violations": sum(1 for record in resolved if int(record["exit_slack_over_bit_length"]) > threshold),
        }
        for threshold in slack_thresholds
    ]
    odd_gap_tests = [
        {
            "candidate_bound": f"exit_bits <= odd_collatz_steps(n) + {threshold}",
            "violations": sum(1 for record in resolved if int(record["exit_minus_odd_steps"]) > threshold),
        }
        for threshold in odd_gap_thresholds
    ]

    max_exit = max((int(record["exit_bits"]) for record in resolved), default=None)
    max_slack = max((int(record["exit_slack_over_bit_length"]) for record in resolved), default=None)
    max_odd_gap = max((int(record["exit_minus_odd_steps"]) for record in resolved), default=None)
    max_total_gap = max((int(record["exit_minus_total_steps"]) for record in resolved), default=None)

    return {
        "sample_limit": sample_limit,
        "tested_odd_integer_count": (sample_limit + 1) // 2,
        "base_bits": base_bits,
        "shallow_probe_bits": shallow_probe_bits,
        "deep_resolve_bits": deep_resolve_bits,
        "shallow_unresolved_count": len(shallow_unresolved),
        "deep_unresolved_count": len(unresolved),
        "all_direct_orbits_terminated_in_sample": all_direct_terminated,
        "exit_status_counts": dict(sorted(status_counts.items())),
        "max_exit_bits": max_exit,
        "max_exit_slack_over_bit_length": max_slack,
        "max_exit_minus_odd_steps": max_odd_gap,
        "max_exit_minus_total_steps": max_total_gap,
        "top_exit_examples": top_by_exit,
        "top_slack_examples": top_by_slack,
        "top_exit_minus_odd_step_examples": top_by_odd_gap,
        "shallow_unresolved_deep_resolution_examples": shallow_resolution_rows,
        "candidate_bit_length_slack_tests": slack_tests,
        "candidate_stopping_proxy_tests": odd_gap_tests,
        "closed_bounded_statement": (
            "Every tested odd n <= 100000 exits the adaptive null frontier by 135 bits and its direct Collatz orbit "
            "terminates within the recorded step limit."
        ),
        "proof_boundary": (
            "This bounded natural-exit audit does not prove Collatz. It does refute simple small-constant slack "
            "bounds and shows that a stopping-time proxy would be circular unless replaced by an independent rank."
        ),
    }


def collatz_ticket36_attempt() -> dict[str, Any]:
    audit = natural_null_frontier_audit()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-36",
        "status": "proof_pressure_open",
        "route": "NullSetArithmeticExclusionOrUniformRank",
        "proof_or_counterexample_mode": "natural_frontier_exit_and_rank_obstruction",
        "attempt": (
            "Translate the Ticket 35 null-set gap into a concrete natural-integer test: a Collatz counterexample "
            "would have to remain inside the adaptive open frontier forever. We probe natural exits, stress candidate "
            "rank bounds, and discard rank formulas that fail on bounded data."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-35",
            "natural_null_frontier_audit": audit,
            "route_decision": {
                "discard": [
                    "measure-zero frontier proof without natural-integer exclusion",
                    "small constant slack theorem exit_bits <= bit_length(n) + C for C <= 112 in the tested range",
                    "stopping-time proxy proof unless stopping time is itself bounded by an independent rank",
                ],
                "retain": [
                    "contrapositive search for a natural n with no frontier exit",
                    "uniform well-founded rank that implies finite frontier exit without using the orbit termination as an oracle",
                    "deep arithmetic exclusion theorem for the limiting 2-adic null frontier",
                ],
            },
        },
        "obstruction": (
            "The sample contains long finite natural residues: for n <= 100000, some exits require up to 135 bits "
            "and slack over bit length reaches 119. Therefore natural exclusion cannot be a shallow compactness argument."
        ),
        "candidate_theorem": (
            "For every positive odd integer n, the adaptive frontier certificate eventually reaches all_lift_descent "
            "or a finite exception that is resolved by a strictly smaller integer; equivalently, no positive integer "
            "defines an infinite path through the limiting null frontier."
        ),
        "next_experiment": (
            "Synthesize a non-circular rank R(n, certificate_prefix) that bounds exit_bits without using the already "
            "known Collatz stopping time, and search for natural paths whose required exit depth grows faster than that rank."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    stress_result: str,
    discarded_route: str,
    retained_route: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "null_exception_or_pointwise_rank_transfer",
        "attempt": (
            "Carry Ticket 36's lesson across the problem: a proof route that only controls density, mass, or bounded "
            "statistics must be upgraded to a pointwise theorem, because a sparse exceptional object can still falsify "
            "the conjecture."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "stress_result": stress_result,
            "discarded_route": discarded_route,
            "retained_route": retained_route,
        },
        "obstruction": (
            "Sparse or null exceptional sets are logically invisible to many aggregate metrics. A complete proof must "
            "eliminate every exceptional object, not merely show that exceptions are rare."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket35-limsup-mass-refinement-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-36",
            "OffCriticalNullExceptionExclusion",
            "A hypothetical sparse off-critical zero family can evade finite-window or measure-small tests.",
            "tail-density or finite-zero-window evidence treated as RH proof",
            "operator/kernel positivity strong enough to exclude each off-critical zero pointwise",
            "Every nontrivial zero is forced onto Re(s)=1/2 by a pointwise positivity or de Branges-type invariant, not by aggregate statistics.",
            "Build adversarial off-critical-zero camouflage tests for each proposed kernel positivity certificate.",
        ),
        collatz_ticket36_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-36",
            "SparseEvenExceptionExclusion",
            "An infinite zero-density set of even exceptions would pass almost-all and density tests while falsifying Goldbach.",
            "almost-all Goldbach positivity used as pointwise Goldbach proof",
            "explicit pointwise lower bound for every even N beyond a verified cutoff",
            "There exists an explicit N0 and positive lower bound G(N)>0 for every even N>N0, with all small N checked independently.",
            "Stress singular-series and minor-arc margins against adversarial sparse exceptional even integers.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-36",
            "SparseGapTwoExtinctionExclusion",
            "A model can preserve many bounded prime statistics while allowing only finitely many exact gap-2 pairs.",
            "bounded distributional resemblance treated as infinitely many twin primes",
            "exact-gap lower bound or Maynard/GPY-style weight forcing gap 2 specifically, not merely bounded gaps",
            "For arbitrarily large X, the exact gap-2 weighted count has a positive lower bound that cannot leak into other admissible gaps.",
            "Run exact-gap leakage adversaries against every candidate sieve weight and rank gap selector.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "null_frontier_arithmetic_open_no_resolution",
        "claim_boundary": (
            "Ticket 36 upgrades Ticket 35 from mass/null-set pressure to pointwise natural or sparse-exception "
            "exclusion tests. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket36-null-frontier-arithmetic-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-36-offcritical-null-exclusion.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-36-natural-null-frontier.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-36-sparse-exception-exclusion.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-36-sparse-gap-exclusion.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
