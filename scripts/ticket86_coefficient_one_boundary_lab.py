from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket85_accessible_cycle_supremum_lab import cycle_formula, symbolic_states


GENERATED_AT = "2026-07-12T00:40:00+09:00"
SCHEMA = "primeproject.ticket86-coefficient-one-boundary-lab.v1"
MIN_HORIZON = 2
MAX_HORIZON = 1024
SYMBOLIC_AUDIT_MAX_HORIZON = 256
SAMPLE_HORIZONS = {2, 3, 4, 5, 8, 16, 32, 64, 128, 256, 512, 1024}


def cycle_target_residue(horizon: int, precision: int) -> int:
    cycle = cycle_formula(horizon)
    modulus = 1 << precision
    target = cycle["target_power"]
    return (target.numerator * pow(target.denominator, -1, modulus)) % modulus


def reduced_target_residue(precision: int) -> int:
    return (-7) % (1 << precision)


def lift_least_residues(max_horizon: int) -> list[dict[str, Any]]:
    if max_horizon < MIN_HORIZON:
        raise ValueError("max_horizon must be at least two")

    rows: list[dict[str, Any]] = []
    residue = 5  # 3^(5+1) = -7 (mod 2^5), the H=2 solution.
    previous_residue: int | None = None
    zero_run = 0
    longest_zero_run = 0

    for horizon in range(MIN_HORIZON, max_horizon + 1):
        precision = horizon + 3
        period = 1 << (horizon + 1)
        if horizon > MIN_HORIZON:
            step = 1 << horizon
            modulus = 1 << precision
            candidates = (residue, residue + step)
            valid = [candidate for candidate in candidates if pow(3, candidate + 1, modulus) == reduced_target_residue(precision)]
            if len(valid) != 1:
                raise AssertionError("the reduced discrete-log lift lost uniqueness")
            previous_residue = residue
            residue = valid[0]

        top_bit_added = residue >= (1 << horizon)
        if top_bit_added:
            zero_run = 0
        else:
            zero_run += 1
            longest_zero_run = max(longest_zero_run, zero_run)

        modulus = 1 << precision
        reduced_congruence = pow(3, residue + 1, modulus) == reduced_target_residue(precision)
        cycle_congruence = pow(3, residue, modulus) == cycle_target_residue(horizon, precision)
        nested = previous_residue is None or residue in (previous_residue, previous_residue + (1 << horizon))
        range_guard = 0 < residue < period and residue % 2 == 1
        rows.append(
            {
                "horizon": horizon,
                "precision": precision,
                "period_log2": horizon + 1,
                "residue": residue,
                "residue_bit_length": residue.bit_length(),
                "top_bit_added": top_bit_added,
                "zero_run_length": zero_run,
                "reduced_congruence": reduced_congruence,
                "cycle_congruence": cycle_congruence,
                "nested_lift": nested,
                "range_guard": range_guard,
            }
        )

    return rows


def audit_symbolic_jump(horizon: int, exponent: int) -> dict[str, int]:
    if exponent < (1 << horizon):
        raise ValueError("a jump exponent must contain the horizon top bit")

    valuation_failures = 0
    affine_bound_failures = 0
    denominator_failures = 0
    growth_premise_failures = 0
    states = symbolic_states(horizon)

    for state in states:
        post_index = int(state["post_index"])
        denominator_power = int(state["denominator_power"])
        constant = int(state["constant"])
        modulus = 1 << (denominator_power + 1)
        if (pow(3, exponent + post_index, modulus) + constant) % modulus != 1 << denominator_power:
            valuation_failures += 1
        if abs(constant) >= 1 << (2 * post_index + 1):
            affine_bound_failures += 1
        if denominator_power > post_index + 2:
            denominator_failures += 1

        # The proof uses (3/2)^(k+t) > 4 + 2^(t+1-k).
        # H>=2, k>=2^H, and t<=H reduce this to 81/16 > 9/2.
        if not (horizon >= 2 and exponent >= (1 << horizon) and post_index <= horizon):
            growth_premise_failures += 1

    return {
        "state_count": len(states),
        "valuation_failure_count": valuation_failures,
        "affine_bound_failure_count": affine_bound_failures,
        "denominator_failure_count": denominator_failures,
        "growth_premise_failure_count": growth_premise_failures,
        "total_failure_count": valuation_failures + affine_bound_failures + denominator_failures + growth_premise_failures,
    }


def analyze_boundary() -> dict[str, Any]:
    rows = lift_least_residues(MAX_HORIZON)
    prefix_failures = sum(
        int(not row[key])
        for row in rows
        for key in ("reduced_congruence", "cycle_congruence", "nested_lift", "range_guard")
    )
    jump_rows = [row for row in rows if bool(row["top_bit_added"])]
    symbolic_rows = [row for row in jump_rows if int(row["horizon"]) <= SYMBOLIC_AUDIT_MAX_HORIZON]
    symbolic_audits = [audit_symbolic_jump(int(row["horizon"]), int(row["residue"])) for row in symbolic_rows]
    symbolic_failures = sum(item["total_failure_count"] for item in symbolic_audits)
    total_failures = prefix_failures + symbolic_failures
    samples = [row for row in rows if int(row["horizon"]) in SAMPLE_HORIZONS]

    return {
        "theorem_name": "InfiniteCoefficientOneMersenneDelay",
        "source_ticket": "CO-TICKET-85",
        "exact_reduction": {
            "cycle_target": "tau_H=(7*3^(H-1)-2^(H+1))/(2^(H+1)-3^H)",
            "original_congruence": "3^r=tau_H (mod 2^(H+3))",
            "reduced_congruence": "3^(r+1)=-7 (mod 2^(H+3))",
            "reason": "After clearing the odd denominator, the difference is 2^(H+1)(3^r+1)-3^(H-1)(3^(r+1)+7); odd r makes the first term divisible by 2^(H+3).",
        },
        "infinite_jump_lemma": (
            "The least residues r_H are nested: r_(H+1) is r_H or r_H+2^(H+1). "
            "If the second case occurred only finitely often, r_H would stabilize at an ordinary positive integer r and "
            "2^(H+3) would divide 3^(r+1)+7 for arbitrarily large H, forcing the impossible equality 3^(r+1)=-7."
        ),
        "growth_lemma": (
            "At every top-bit height, 2^H<=r_H<2^(H+1). For 0<=t<=H the exact affine state has "
            "d_t<=t+2 and |c_t|<2^(2t+1). Since (3/2)^(r_H+t)>=81/16>9/2>=4+2^(t+1-r_H), "
            "the state exceeds 2^r_H-1 through t=H."
        ),
        "delay_statement": (
            "There are infinitely many positive odd exponents k=r_H such that D(k)>H and 2^H<=k<2^(H+1). "
            "Because D(k) is integral, D(k)>=H+1>log2(k)."
        ),
        "proof_chain": [
            "Reduce the accessible-cycle target congruence exactly to the fixed 2-adic discrete logarithm 3^(r+1)=-7.",
            "Lift the unique odd residue one precision bit at a time; each new residue is unchanged or gains the new top bit.",
            "Prove that top-bit gains occur infinitely often by ruling out stabilization at a positive ordinary exponent.",
            "At a top-bit height use k=r_H directly, without the extra period used in TICKET85.",
            "Combine the exact valuation prefix, affine-constant bound, and elementary growth inequality to obtain D(k)>H.",
            "Use 2^H<=k<2^(H+1) and integrality of D(k) to conclude D(k)>log2(k).",
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_horizon": MAX_HORIZON,
            "prefix_case_count": len(rows),
            "top_bit_case_count": len(jump_rows),
            "zero_bit_case_count": len(rows) - len(jump_rows),
            "longest_observed_zero_run": max(int(row["zero_run_length"]) for row in rows),
            "maximum_precision": MAX_HORIZON + 3,
            "symbolic_audit_max_horizon": SYMBOLIC_AUDIT_MAX_HORIZON,
            "symbolic_jump_case_count": len(symbolic_rows),
            "symbolic_state_count": sum(item["state_count"] for item in symbolic_audits),
            "prefix_failure_count": prefix_failures,
            "symbolic_failure_count": symbolic_failures,
            "total_failure_count": total_failures,
            "samples": samples,
        },
        "theorem_status": "restricted_coefficient_one_delay_proved_no_collatz_resolution" if total_failures == 0 else "coefficient_one_audit_inconclusive_no_collatz_resolution",
        "refuted_candidate": {
            "claim": "D(k)<=log2(k) for every positive Mersenne exponent k",
            "status": "refuted_on_an_infinite_explicitly_defined_subsequence",
            "scope": "Mersenne descent delay only; this is not a divergent orbit.",
        },
        "discarded_route": "Treat a finite H<=1024 prefix audit as proof that every horizon uses the least residue successfully.",
        "retained_route": "Study additive excess through the binary digit runs of the fixed 2-adic exponent solving 3^(r+1)=-7.",
        "candidate_theorem": "TwoAdicDigitRunBoundary: prove or refute unbounded usable zero runs, which would force unbounded D(k)-log2(k) along this construction.",
        "next_theorem_target": "TwoAdicDigitRunBoundary",
        "proof_boundary": "This proves an infinite restricted lower-bound subsequence. It proves neither Collatz convergence nor divergence and resolves none of the four open problems.",
        "novelty_boundary": "The derivation is a PrimeProject candidate result. A literature-wide novelty search and independent peer verification are still required before publication.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "nested-prefix non-stabilization transfer discipline",
        "attempt": "Transfer only the principle that a nested finite witness family needs a proved non-stabilization mechanism before claiming infinitely many witnesses.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket86_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific nested witness family with an exact non-stabilization identity was proved.",
        "candidate_theorem": target,
        "next_experiment": "Construct a target-specific nested witness and identify what stabilization would imply.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket85 = read_json(ROOT / "data/open-problem/ticket85-accessible-cycle-supremum-lab.json")
    audit = analyze_boundary()
    attempts = [
        transfer_attempt(ticket85, "riemann", "RH-TICKET-86", "NestedZeroWitnessNonStabilization", "Find a nested off-line-zero certificate whose stabilization contradicts the zeta functional equation."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-86",
            "route": "InfiniteCoefficientOneMersenneDelay",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact two-adic reduction plus infinite top-bit subsequence",
            "attempt": "Remove the extra-period loss in TICKET85 on an infinite subsequence and cross the coefficient-one zero-additive boundary.",
            "bounded_result": {"source_ticket": "CO-TICKET-85", "coefficient_one_boundary_audit": audit},
            "obstruction": audit["discarded_route"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET87 around the binary zero-run boundary of the fixed 2-adic logarithm.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket85, "goldbach", "GB-TICKET-86", "NestedExceptionalWitnessNonStabilization", "Find a nested Goldbach exception certificate whose stabilization contradicts an exact local identity."),
        transfer_attempt(ticket85, "twin-prime", "TP-TICKET-86", "NestedExactGapWitnessNonStabilization", "Find a nested exact-gap witness family with a target-specific non-stabilization theorem."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "coefficient_one_boundary_open_no_collatz_resolution",
        "claim_boundary": "Ticket 86 proves one restricted infinite Mersenne delay theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket86-coefficient-one-boundary-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-86-coefficient-one-boundary.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-86-coefficient-one-boundary.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-86-coefficient-one-boundary.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-86-coefficient-one-boundary.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
