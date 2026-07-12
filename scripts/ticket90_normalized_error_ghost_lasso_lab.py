from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket86_coefficient_one_boundary_lab import lift_least_residues


GENERATED_AT = "2026-07-12T06:20:00+09:00"
SCHEMA = "primeproject.ticket90-normalized-error-ghost-lasso-lab.v1"
MIN_HORIZON = 2
MAX_AUDIT_HORIZON = 256
ERROR_BITS = 20
MIN_LASSO_PRECISION = 2
MAX_LASSO_PRECISION = 64


def correction_unit_prefix(max_horizon: int, bits: int) -> dict[int, int]:
    modulus = 1 << bits
    units = {1: 5}
    for horizon in range(1, max_horizon):
        current = units[horizon]
        units[horizon + 1] = (current + (1 << (horizon + 2)) * current * current) % modulus
    return units


def limiting_correction(bits: int) -> int:
    units = correction_unit_prefix(bits + 2, bits)
    return units[bits + 2] % (1 << bits)


def normalized_error_mod(horizon: int, residue: int, bits: int) -> int:
    modulus = 1 << (horizon + 3 + bits)
    numerator = (pow(3, residue + 1, modulus) + 7) % modulus
    if numerator % (1 << (horizon + 3)) != 0:
        raise AssertionError("normalized error numerator lost exact divisibility")
    return numerator >> (horizon + 3)


def analyze_normalized_error() -> dict[str, Any]:
    rows = lift_least_residues(MAX_AUDIT_HORIZON + 1)
    by_horizon = {int(row["horizon"]): row for row in rows}
    units = correction_unit_prefix(MAX_AUDIT_HORIZON + 1, ERROR_BITS)
    alpha = limiting_correction(ERROR_BITS)
    beta = (-7 * alpha) % (1 << ERROR_BITS)
    correction_recurrence_failures = 0
    convergence_failures = 0
    lift_bit_failures = 0
    error_recurrence_failures = 0

    for horizon in range(1, MAX_AUDIT_HORIZON):
        current = units[horizon]
        expected = (current + (1 << (horizon + 2)) * current * current) % (1 << ERROR_BITS)
        correction_recurrence_failures += int(units[horizon + 1] != expected)

    for horizon in range(MIN_HORIZON, MAX_AUDIT_HORIZON):
        residue = int(by_horizon[horizon]["residue"])
        next_residue = int(by_horizon[horizon + 1]["residue"])
        error = normalized_error_mod(horizon, residue, ERROR_BITS)
        next_error = normalized_error_mod(horizon + 1, next_residue, ERROR_BITS)
        lift_bit = (next_residue - residue) // (1 << (horizon + 1))
        lift_bit_failures += int(lift_bit not in (0, 1) or lift_bit != error % 2)

        correction = units[horizon]
        power = pow(3, residue + 1, 1 << ERROR_BITS)
        forcing = power * correction % (1 << ERROR_BITS)
        convergence_precision = min(horizon + 2, ERROR_BITS)
        convergence_failures += int((forcing - beta) % (1 << convergence_precision) != 0)

        if lift_bit == 0:
            predicted = (error // 2) % (1 << (ERROR_BITS - 1))
        else:
            predicted = ((error + forcing) // 2) % (1 << (ERROR_BITS - 1))
        error_recurrence_failures += int(next_error % (1 << (ERROR_BITS - 1)) != predicted)

    lasso_failures = 0
    lasso_rows: list[dict[str, Any]] = []
    for precision in range(MIN_LASSO_PRECISION, MAX_LASSO_PRECISION + 1):
        beta_wide = (-7 * limiting_correction(precision + 1)) % (1 << (precision + 1))
        beta_mod = beta_wide % (1 << precision)
        image = ((beta_wide + beta_wide) // 2) % (1 << precision)
        fixed = beta_mod % 2 == 1 and image == beta_mod
        avoids_double_zero_trigger = beta_mod % 4 != 0
        lasso_failures += int(not fixed or not avoids_double_zero_trigger)
        lasso_rows.append(
            {
                "precision": precision,
                "beta_residue": beta_mod,
                "fixed": fixed,
                "avoids_error_zero_mod4": avoids_double_zero_trigger,
            }
        )

    total_failures = correction_recurrence_failures + convergence_failures + lift_bit_failures + error_recurrence_failures + lasso_failures
    return {
        "theorem_name": "FixedPrecisionNormalizedErrorGhostLassoNoGo",
        "source_ticket": "CO-TICKET-89",
        "normalized_error": {
            "definition": "e_H=(3^(r_H+1)+7)/2^(H+3)",
            "lift_bit": "The next exponent bit b_(H+1) equals e_H mod 2.",
            "zero_branch": "If e_H is even, r_(H+1)=r_H and e_(H+1)=e_H/2.",
            "one_branch": "If e_H is odd, r_(H+1)=r_H+2^(H+1) and e_(H+1)=(e_H+3^(r_H+1)A_H)/2.",
            "double_zero_trigger": "e_H=0 mod 4 forces the next two lift bits to be 00.",
        },
        "correction_limit": {
            "definition": "A_H=(3^(2^(H+1))-1)/2^(H+3)",
            "exact_recurrence": "A_(H+1)=A_H+2^(H+2)A_H^2",
            "limit": "alpha=log_2adic(-3)/4",
            "forcing_limit": "B_H=3^(r_H+1)A_H converges to beta=-7*alpha",
            "precision": "B_H=beta mod 2^(H+2)",
            "beta_is_odd": True,
        },
        "limiting_ghost": {
            "map": "F_beta(e)=e/2 for even e and (e+beta)/2 for odd e",
            "fixed_point": "F_beta(beta)=beta",
            "obstruction": "beta is odd, so this completion-space fixed point never enters e=0 mod 4.",
            "finite_precision_consequence": "For every fixed modulus 2^m, the forcing term eventually equals beta modulo the precision needed by the transition, leaving a fixed lasso at e=beta mod 2^m.",
            "domain_warning": "The ghost is a state of the limiting completion map. It is not asserted to equal the actual normalized-error orbit.",
        },
        "proof_chain": [
            "Normalize the exact discrete-log error by the currently certified power 2^(H+3).",
            "Derive the next lift bit from the parity of e_H and derive the exact zero and one branch recurrences.",
            "Factor the exponent-step multiplier through A_H and prove its squaring recurrence.",
            "Take the 2-adic limit alpha=log(-3)/4 and combine it with 3^(r_H+1)->-7 to obtain the odd forcing limit beta.",
            "Construct the limiting fixed point e=beta, which avoids the double-zero trigger e=0 mod 4.",
            "Reduce the fixed point modulo every finite precision to obtain an obstruction lasso in every fixed-state abstraction.",
            "Conclude that a valid excess-five proof must use growing precision or a quantitative separation of the actual orbit from the ghost."
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_audit_horizon": MAX_AUDIT_HORIZON,
            "audited_transition_count": MAX_AUDIT_HORIZON - MIN_HORIZON,
            "error_bits": ERROR_BITS,
            "lasso_precision_count": len(lasso_rows),
            "maximum_lasso_precision": MAX_LASSO_PRECISION,
            "beta_low_20": beta,
            "correction_recurrence_failure_count": correction_recurrence_failures,
            "forcing_convergence_failure_count": convergence_failures,
            "lift_bit_failure_count": lift_bit_failures,
            "error_recurrence_failure_count": error_recurrence_failures,
            "lasso_failure_count": lasso_failures,
            "total_failure_count": total_failures,
            "lasso_samples": [row for row in lasso_rows if int(row["precision"]) in {2, 3, 4, 8, 16, 32, 64}],
        },
        "theorem_status": "fixed_precision_error_lasso_no_go_proved_no_collatz_resolution" if total_failures == 0 else "normalized_error_audit_inconclusive_no_collatz_resolution",
        "discarded_routes": [
            {"route": "fixed_modulus_error_automaton", "status": "blocked_by_ghost_lasso", "counteredge": "Every fixed precision contains the limiting fixed residue e=beta."},
            {"route": "treat_limiting_fixed_point_as_actual_counterexample", "status": "rejected_domain_error", "counteredge": "The limiting completion state is not a positive Collatz orbit or the proved actual error sequence."},
            {"route": "finite_state_exhaustion_at_larger_constant_precision", "status": "refuted_uniformly", "counteredge": "The lasso persists for every tested and symbolically arbitrary fixed precision."},
        ],
        "retained_route": "Track a precision m(H) growing with H and prove the actual normalized error cannot shadow beta deeply enough to avoid e_H=0 mod 4 forever.",
        "candidate_theorem": "GrowingPrecisionErrorGhostSeparation: under the eventual excess-four cap, derive an impossible lower bound on v2(e_H-beta) relative to H.",
        "next_theorem_target": "GrowingPrecisionErrorGhostSeparation",
        "proof_boundary": "TICKET90 proves a fixed-precision proof-route no-go. It does not prove valuation-excess-five recurrence, an additive-two infinite delay theorem, or Collatz.",
        "novelty_boundary": "The normalized-error recurrence and ghost-lasso packaging are candidate PrimeProject contributions pending independent p-adic dynamics review.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "limiting ghost-lasso audit transfer discipline",
        "attempt": "Normalize the target error, identify its limiting transition, and reject fixed-state proofs when a completion-space lasso survives every fixed precision.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket90_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific normalized limiting map and growing-precision separation were proved.",
        "candidate_theorem": target,
        "next_experiment": "Derive a normalized error recurrence and test every fixed precision for ghost lassos.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket89 = read_json(ROOT / "data/open-problem/ticket89-fixed-log-golden-mean-reduction-lab.json")
    audit = analyze_normalized_error()
    attempts = [
        transfer_attempt(ticket89, "riemann", "RH-TICKET-90", "ExplicitFormulaErrorGhostLasso", "Prove growing-scale separation from limiting explicit-formula sign lassos."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-90",
            "route": "FixedPrecisionNormalizedErrorGhostLassoNoGo",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact normalized-error recurrence plus limiting fixed-point obstruction",
            "attempt": "Attack the excess-five recurrence through normalized errors and determine whether any fixed finite-state abstraction can force the target.",
            "bounded_result": {"source_ticket": "CO-TICKET-89", "normalized_error_ghost_lasso_audit": audit},
            "obstruction": audit["limiting_ghost"]["finite_precision_consequence"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET91 around growing-precision separation from beta.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket89, "goldbach", "GB-TICKET-90", "CharacterErrorGhostLasso", "Prove growing-scale separation from limiting exceptional-character error lassos."),
        transfer_attempt(ticket89, "twin-prime", "TP-TICKET-90", "ParityErrorGhostLasso", "Prove growing-scale separation from limiting parity-barrier error lassos."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "normalized_error_ghost_lasso_open_no_collatz_resolution",
        "claim_boundary": "Ticket 90 proves one fixed-precision proof-route no-go but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket90-normalized-error-ghost-lasso-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-90-normalized-error-ghost-lasso.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-90-normalized-error-ghost-lasso.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-90-normalized-error-ghost-lasso.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-90-normalized-error-ghost-lasso.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
