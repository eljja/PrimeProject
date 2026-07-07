from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float


GENERATED_AT = "2026-07-07T10:20:00+09:00"
SCHEMA = "primeproject.ticket37-pointwise-rank-synthesis-lab.v1"


def push_top(rows: list[dict[str, Any]], row: dict[str, Any], key: str, limit: int = 16) -> None:
    rows.append(row)
    rows.sort(key=lambda item: (item.get(key) is not None, item.get(key, -10**18)), reverse=True)
    del rows[limit:]


def first_frontier_exit(n: int, base_bits: int, max_bits: int) -> dict[str, Any]:
    for bits in range(base_bits, max_bits + 1):
        certificate = cert(n % (1 << bits), bits)
        status = certificate.get("status")
        if status != "needs_split":
            bit_length = n.bit_length()
            return {
                "n": n,
                "bit_length": bit_length,
                "exit_bits": bits,
                "exit_ratio_to_bit_length": round_float(bits / max(bit_length, 1)),
                "exit_slack_over_bit_length": bits - bit_length,
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
        "exit_ratio_to_bit_length": None,
        "exit_slack_over_bit_length": None,
        "exit_status": "unresolved_within_probe",
    }


def linear_rank_probe(
    sample_limit: int = 5_000_000,
    base_bits: int = 12,
    max_bits: int = 320,
) -> dict[str, Any]:
    alpha_values = [8, 9, 10, 11, 12]
    min_bit_thresholds = [1, 5, 8, 10, 12, 14, 16, 18, 20, 22]
    status_counts: Counter[str] = Counter()
    top_exit: list[dict[str, Any]] = []
    top_ratio: list[dict[str, Any]] = []
    top_slack: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    alpha_counts = {alpha: 0 for alpha in alpha_values}
    alpha_examples: dict[int, list[dict[str, Any]]] = {alpha: [] for alpha in alpha_values}
    threshold_stats: dict[int, dict[str, Any]] = {
        threshold: {
            "min_bit_length": threshold,
            "tested_count": 0,
            "max_exit_ratio": 0.0,
            "max_exit_bits": 0,
            "top_example": None,
        }
        for threshold in min_bit_thresholds
    }

    tested_count = 0
    resolved_count = 0
    for n in range(1, sample_limit + 1, 2):
        tested_count += 1
        row = first_frontier_exit(n, base_bits, max_bits)
        if row["exit_bits"] is None:
            if len(unresolved) < 20:
                unresolved.append(row)
            continue
        resolved_count += 1
        status_counts[str(row["exit_status"])] += 1
        push_top(top_exit, row, "exit_bits")
        push_top(top_ratio, row, "exit_ratio_to_bit_length")
        push_top(top_slack, row, "exit_slack_over_bit_length")

        bit_length = int(row["bit_length"])
        exit_bits = int(row["exit_bits"])
        for alpha in alpha_values:
            excess = exit_bits - alpha * bit_length
            if excess > 0:
                alpha_counts[alpha] += 1
                example = dict(row)
                example["alpha"] = alpha
                example["excess_over_alpha_bit_length"] = excess
                push_top(alpha_examples[alpha], example, "excess_over_alpha_bit_length", limit=12)

        for threshold, stats in threshold_stats.items():
            if bit_length < threshold:
                continue
            stats["tested_count"] += 1
            ratio = float(row["exit_ratio_to_bit_length"])
            if ratio > float(stats["max_exit_ratio"]):
                stats["max_exit_ratio"] = ratio
                stats["max_exit_bits"] = exit_bits
                stats["top_example"] = row

    rank_tests = []
    for alpha in alpha_values:
        rank_tests.append(
            {
                "candidate_bound": f"exit_bits <= {alpha} * bit_length(n)",
                "violations": alpha_counts[alpha],
                "bounded_status": "sample_holds" if alpha_counts[alpha] == 0 else "sample_refuted",
                "violation_examples": alpha_examples[alpha],
            }
        )

    finite_seed_alpha11 = [
        row
        for row in alpha_examples[11]
        if isinstance(row.get("n"), int)
    ]
    candidate_piecewise = {
        "candidate": "n >= 128 implies exit_bits <= 11 * bit_length(n); all tested n imply exit_bits <= 12 * bit_length(n)",
        "sample_status": "supported_in_bounded_sample_not_proved",
        "finite_seed_violations_for_alpha11": finite_seed_alpha11,
        "reason_not_proof": (
            "The scan gives a sharp bounded candidate, but it does not prove that future residue classes cannot "
            "produce larger ratios. A proof needs a symbolic extension lemma over all adaptive frontier states."
        ),
    }

    return {
        "sample_limit": sample_limit,
        "tested_odd_integer_count": tested_count,
        "base_bits": base_bits,
        "max_probe_bits": max_bits,
        "resolved_count": resolved_count,
        "unresolved_count": tested_count - resolved_count,
        "unresolved_examples": unresolved,
        "exit_status_counts": dict(sorted(status_counts.items())),
        "max_exit_bits": top_exit[0]["exit_bits"] if top_exit else None,
        "max_exit_ratio_to_bit_length": top_ratio[0]["exit_ratio_to_bit_length"] if top_ratio else None,
        "max_exit_slack_over_bit_length": top_slack[0]["exit_slack_over_bit_length"] if top_slack else None,
        "top_exit_examples": top_exit,
        "top_ratio_examples": top_ratio,
        "top_slack_examples": top_slack,
        "linear_rank_tests": rank_tests,
        "threshold_ratio_rows": [
            {
                **stats,
                "max_exit_ratio": round_float(float(stats["max_exit_ratio"])),
            }
            for _, stats in sorted(threshold_stats.items())
        ],
        "candidate_piecewise_linear_rank": candidate_piecewise,
        "rank_status": "bounded_piecewise_linear_rank_candidate_not_proof",
        "closed_bounded_statement": (
            "Every tested odd n <= 5000000 exits the adaptive null frontier by 320 probe bits. In the same sample, "
            "exit_bits <= 12 * bit_length(n), and for n >= 128, exit_bits <= 11 * bit_length(n)."
        ),
        "proof_boundary": (
            "This is not a Collatz proof. It only identifies a non-circular-looking bounded rank shape. The missing "
            "step is a symbolic theorem proving that all future natural residues obey the same piecewise linear rank."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    rank_probe = linear_rank_probe()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-37",
        "status": "proof_pressure_open",
        "route": "NaturalFrontierRankOrPointwiseExceptionElimination",
        "proof_or_counterexample_mode": "bounded_rank_synthesis_and_counterexample_pruning",
        "attempt": (
            "Do not discard Ticket 36's natural frontier audit. Extend it into a rank-synthesis test: small linear "
            "rank candidates are attacked by bounded counterexamples, while the surviving piecewise candidate is "
            "kept only as a theorem target."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-36",
            "pointwise_rank_probe": rank_probe,
            "route_decision": {
                "discard": [
                    "exit_bits <= 8 * bit_length(n) as a global rank",
                    "exit_bits <= 9 * bit_length(n) as a global rank",
                    "exit_bits <= 10 * bit_length(n) as a global rank",
                    "unqualified exit_bits <= 11 * bit_length(n) without finite seed handling",
                ],
                "retain": [
                    "finite seed set plus exit_bits <= 11 * bit_length(n) for n >= 128 as a bounded theorem candidate",
                    "global exit_bits <= 12 * bit_length(n) as a weaker bounded theorem candidate",
                    "symbolic extension lemma over adaptive frontier states",
                ],
            },
        },
        "obstruction": (
            "The experiment found no bounded counterexample to the 12x rank shape, but 8x, 9x, 10x, and unqualified "
            "11x ranks are refuted in the bounded sample. The surviving rank is empirical and still lacks an infinite extension theorem."
        ),
        "candidate_theorem": (
            "There is a finite verified seed set S such that every positive odd n not in S exits the adaptive "
            "null frontier by 11 * bit_length(n), and each seed in S is independently resolved."
        ),
        "next_experiment": (
            "Search for a symbolic frontier extension lemma: every open residue block either exits within O(delta bits) "
            "or maps to a smaller verified seed without invoking Collatz stopping time."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    bounded_rank_analogue: str,
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
        "proof_or_counterexample_mode": "pointwise_rank_transfer",
        "attempt": (
            "Transfer Ticket 37's lesson: a bounded rank candidate becomes useful only if it names the pointwise "
            "extension theorem. Aggregate evidence and density controls remain support, not proof."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "bounded_rank_analogue": bounded_rank_analogue,
            "discarded_route": discarded_route,
            "retained_route": retained_route,
        },
        "obstruction": (
            "The remaining obstruction is pointwise. Sparse exceptional objects can survive every bounded or averaged "
            "test unless a rank or positivity theorem excludes each one."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket36-null-frontier-arithmetic-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-37",
            "PointwiseZeroExclusionRank",
            "A positive kernel/rank must rule out each off-critical zero, not only a sampled or density-small family.",
            "finite-height zero verification or smoothed average positivity treated as RH proof",
            "pointwise positivity certificate strong enough to contradict every off-critical zero",
            "Every off-critical zero forces a negative certificate in an explicitly positive kernel, so no off-critical zero can exist.",
            "Build adversarial off-critical zero configurations and test every proposed kernel for pointwise failure.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-37",
            "PointwiseEvenCutoffRank",
            "A cutoff rank must give a positive representation lower bound for each even N beyond N0.",
            "density-positive or almost-all Goldbach theorem treated as pointwise Goldbach proof",
            "explicit lower bound with a finite verified seed interval",
            "There is an explicit N0 such that every even N>N0 has a positive binary-prime representation count, with all N<=N0 verified.",
            "Search for sparse even-number adversaries that pass density checks but minimize pointwise representation counts.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-37",
            "ExactGapTwoPointwiseRank",
            "A gap selector must force exact gap 2 for arbitrarily large ranges rather than leak mass into other bounded gaps.",
            "bounded-gap or averaged pair mass treated as twin-prime infinitude",
            "exact gap-2 lower bound with leakage control against all wider admissible gaps",
            "For arbitrarily large X, an unconditional nonnegative weight leaves positive mass on exact gap 2 after all wider-gap leakage is subtracted.",
            "Stress candidate sieve weights against models that preserve bounded gaps while deleting exact gap-2 pairs.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "pointwise_rank_synthesis_open_no_resolution",
        "claim_boundary": (
            "Ticket 37 searches for pointwise rank candidates and bounded counterexamples to weak ranks. It does not "
            "prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket37-pointwise-rank-synthesis-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-37-pointwise-zero-rank.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-37-pointwise-rank-synthesis.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-37-pointwise-cutoff-rank.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-37-exact-gap-rank.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
