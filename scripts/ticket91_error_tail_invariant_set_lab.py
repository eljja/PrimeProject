from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket86_coefficient_one_boundary_lab import lift_least_residues
from ticket87_two_adic_digit_run_boundary_lab import fixed_log_residue
from ticket89_fixed_log_golden_mean_reduction_lab import fibonacci
from ticket90_normalized_error_ghost_lasso_lab import (
    correction_unit_prefix,
    limiting_correction,
    normalized_error_mod,
)


GENERATED_AT = "2026-07-12T09:10:00+09:00"
SCHEMA = "primeproject.ticket91-error-tail-invariant-set-lab.v1"
MIN_HORIZON = 2
MAX_AUDIT_HORIZON = 256
TAIL_BITS = 20
CONJUGACY_BITS = 12


def truncated_v2(value: int, precision: int) -> int:
    value %= 1 << precision
    if value == 0:
        return precision
    return (value & -value).bit_length() - 1


def avoids_double_zero(word: int, bits: int) -> bool:
    return all(not (((word >> index) & 1) == 0 and ((word >> (index + 1)) & 1) == 0) for index in range(bits - 1))


def analyze_error_tail_invariant_set() -> dict[str, Any]:
    full_precision = MAX_AUDIT_HORIZON + TAIL_BITS + 2
    full_residue, series_metrics = fixed_log_residue(full_precision)
    rows = lift_least_residues(MAX_AUDIT_HORIZON + 1)
    by_horizon = {int(row["horizon"]): row for row in rows}
    units = correction_unit_prefix(MAX_AUDIT_HORIZON + 1, TAIL_BITS)
    alpha = limiting_correction(TAIL_BITS)
    gamma = 7 * alpha % (1 << TAIL_BITS)
    beta = (-gamma) % (1 << TAIL_BITS)

    local_congruence_failures = 0
    limiting_congruence_failures = 0
    tail_shift_failures = 0
    ghost_shadow_failures = 0
    audit_rows: list[dict[str, int]] = []

    for horizon in range(MIN_HORIZON, MAX_AUDIT_HORIZON + 1):
        residue = int(by_horizon[horizon]["residue"])
        tail = ((full_residue - residue) >> (horizon + 1)) % (1 << TAIL_BITS)
        error = normalized_error_mod(horizon, residue, TAIL_BITS)
        local_precision = min(horizon + 3, TAIL_BITS)
        limiting_precision = min(horizon + 2, TAIL_BITS)
        local_model = 7 * units[horizon] * tail
        limiting_model = gamma * tail
        local_congruence_failures += int((error - local_model) % (1 << local_precision) != 0)
        limiting_congruence_failures += int((error - limiting_model) % (1 << limiting_precision) != 0)
        ghost_shadow_failures += int(
            truncated_v2(error - beta, limiting_precision)
            != truncated_v2(tail + 1, limiting_precision)
        )

        if horizon < MAX_AUDIT_HORIZON:
            next_residue = int(by_horizon[horizon + 1]["residue"])
            next_tail = ((full_residue - next_residue) >> (horizon + 2)) % (1 << (TAIL_BITS - 1))
            shifted_tail = (tail - (tail & 1)) // 2
            tail_shift_failures += int(next_tail != shifted_tail % (1 << (TAIL_BITS - 1)))

        if horizon in {2, 3, 4, 8, 16, 32, 64, 128, 256}:
            audit_rows.append(
                {
                    "horizon": horizon,
                    "residue_low_20": residue % (1 << TAIL_BITS),
                    "tail_low_20": tail,
                    "error_low_20": error,
                    "limiting_precision": limiting_precision,
                    "beta_shadow_depth": truncated_v2(error - beta, limiting_precision),
                }
            )

    conjugacy_modulus = 1 << CONJUGACY_BITS
    output_modulus = 1 << (CONJUGACY_BITS - 1)
    gamma_conjugacy = 7 * limiting_correction(CONJUGACY_BITS) % conjugacy_modulus
    beta_conjugacy = (-gamma_conjugacy) % conjugacy_modulus
    conjugacy_failures = 0
    for tail in range(conjugacy_modulus):
        error = gamma_conjugacy * tail % conjugacy_modulus
        shifted_tail = (tail - (tail & 1)) // 2
        mapped_error = error // 2 if error % 2 == 0 else (error + beta_conjugacy) // 2
        conjugacy_failures += int(mapped_error % output_modulus != gamma_conjugacy * shifted_tail % output_modulus)

    legal_words = [word for word in range(conjugacy_modulus) if avoids_double_zero(word, CONJUGACY_BITS)]
    legal_images = {gamma_conjugacy * word % conjugacy_modulus for word in legal_words}
    invariant_failures = sum(
        int(not avoids_double_zero((word - (word & 1)) // 2, CONJUGACY_BITS - 1)) for word in legal_words
    )
    legal_count_failures = int(len(legal_words) != fibonacci(CONJUGACY_BITS + 2))
    injectivity_failures = int(len(legal_images) != len(legal_words))
    beta_tail_failures = sum(
        int(((-7 * limiting_correction(bits)) - (7 * limiting_correction(bits)) * ((1 << bits) - 1)) % (1 << bits) != 0)
        for bits in range(2, CONJUGACY_BITS + 1)
    )

    total_failures = (
        local_congruence_failures
        + limiting_congruence_failures
        + tail_shift_failures
        + ghost_shadow_failures
        + conjugacy_failures
        + invariant_failures
        + legal_count_failures
        + injectivity_failures
        + beta_tail_failures
    )
    return {
        "theorem_name": "NormalizedErrorTailConjugacyAndSingleGhostNoGo",
        "source_ticket": "CO-TICKET-90",
        "exact_tail_identity": {
            "fixed_exponent": "Let R in Z_2 be the odd solution of 3^(R+1)=-7 and write R=r_H+2^(H+1)t_H.",
            "unit": "u_H=3^(2^(H+1))=1+2^(H+3)A_H.",
            "identity": "e_H=7(1-u_H^(-t_H))/2^(H+3).",
            "local_congruence": "e_H=7A_H t_H (mod 2^(H+3)).",
            "limiting_congruence": "With alpha=lim A_H and gamma=7alpha, e_H=gamma t_H (mod 2^(H+2)).",
            "tail_shift": "If b_H=t_H mod 2, then t_(H+1)=(t_H-b_H)/2.",
        },
        "limiting_conjugacy": {
            "coordinate": "e=gamma*t with odd gamma=7 log_2adic(-3)/4.",
            "map": "F(e)=e/2 for even e and F(e)=(e+beta)/2 for odd e, where beta=-gamma.",
            "conjugacy": "Multiplication by gamma conjugates the one-sided binary tail shift to F, losing one output bit per step.",
            "ghost_identification": "The fixed point e=beta is exactly t=-1, the all-one future tail.",
            "shadow_identity": "min(v2(e_H-beta),H+2)=min(v2(t_H+1),H+2); this is only the initial run length of future one bits.",
        },
        "golden_mean_obstruction": {
            "tail_set": "G={one-sided binary tails with no occurrence of 00}.",
            "error_set": "K=gamma*G is invariant under the limiting normalized-error map.",
            "size": "At depth n, G has F_(n+2) words; in the limit it is uncountable and has positive entropy.",
            "single_ghost_no_go": "Separating the actual orbit from beta only proves that a future zero occurs. TICKET87 already proves infinitely many zero bits, but this does not force adjacent zeros.",
            "required_escape": "The additive-two target requires the actual tail orbit to leave G, equivalently the error orbit to leave K, infinitely often.",
        },
        "proof_chain": [
            "Write the fixed 2-adic exponent as its certified prefix plus a 2-adic future tail.",
            "Substitute this decomposition into 3^(R+1)=-7 and solve exactly for the normalized error.",
            "Expand one 2-adic binomial order and use A_H=alpha mod 2^(H+2) to obtain growing-precision conjugacy.",
            "Identify beta=-gamma with the all-one tail and identify beta-shadow depth with the next zero-bit waiting time.",
            "Conjugate the full binary shift, not only one fixed point, to the limiting error map.",
            "Map every no-00 tail into the invariant set K=gamma*G and retain its Fibonacci growth and positive entropy.",
            "Reject single-ghost separation as a route to 00 recurrence and replace it with target-specific escape from K.",
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_audit_horizon": MAX_AUDIT_HORIZON,
            "audited_horizon_count": MAX_AUDIT_HORIZON - MIN_HORIZON + 1,
            "audited_tail_transition_count": MAX_AUDIT_HORIZON - MIN_HORIZON,
            "tail_bits": TAIL_BITS,
            "conjugacy_bits": CONJUGACY_BITS,
            "conjugacy_state_count": conjugacy_modulus,
            "golden_mean_word_count": len(legal_words),
            "golden_mean_image_count": len(legal_images),
            "gamma_low_20": gamma,
            "beta_low_20": beta,
            "local_congruence_failure_count": local_congruence_failures,
            "limiting_congruence_failure_count": limiting_congruence_failures,
            "tail_shift_failure_count": tail_shift_failures,
            "ghost_shadow_failure_count": ghost_shadow_failures,
            "conjugacy_failure_count": conjugacy_failures,
            "golden_mean_invariance_failure_count": invariant_failures,
            "golden_mean_count_failure_count": legal_count_failures,
            "golden_mean_injectivity_failure_count": injectivity_failures,
            "beta_tail_failure_count": beta_tail_failures,
            "total_failure_count": total_failures,
            "samples": audit_rows,
            **series_metrics,
        },
        "theorem_status": "error_tail_conjugacy_and_single_ghost_no_go_proved_no_collatz_resolution" if total_failures == 0 else "error_tail_conjugacy_audit_inconclusive_no_collatz_resolution",
        "discarded_routes": [
            {"route": "separate_only_from_beta", "status": "insufficient", "counteredge": "beta is only the all-one point inside the much larger invariant set gamma*G."},
            {"route": "infer_00_from_infinitely_many_zero_bits", "status": "invalid", "counteredge": "The alternating tail 1010... has infinitely many zeros and no 00."},
            {"route": "fixed_precision_escape_from_golden_set", "status": "insufficient", "counteredge": "Every finite legal cylinder extends to an infinite no-00 tail."},
        ],
        "retained_route": "Exploit the specific arithmetic relation R=log_2adic(-7)/log_2adic(3)-1 to prove its shift orbit exits the no-00 golden-mean set infinitely often.",
        "candidate_theorem": "GoldenMeanInvariantSetEscape: the tail shift orbit of the fixed exponent R leaves G infinitely often, equivalently R contains 00 infinitely often.",
        "next_theorem_target": "GoldenMeanInvariantSetEscape",
        "proof_boundary": "TICKET91 proves an exact growing-precision coordinate theorem and corrects TICKET90's next route. It does not prove 00 recurrence, an additive-two infinite delay theorem, or Collatz.",
        "novelty_boundary": "The tail-error conjugacy packaging is a candidate PrimeProject contribution pending independent review; the golden-mean shift itself is standard symbolic dynamics.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "full invariant-set audit transfer discipline",
        "attempt": "Replace a single limiting ghost by the full target-avoiding invariant set and require escape from that set.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket91_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific invariant-set conjugacy or escape theorem was proved.",
        "candidate_theorem": target,
        "next_experiment": "Identify the full target-avoiding invariant set before using distance from one special state.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket90 = read_json(ROOT / "data/open-problem/ticket90-normalized-error-ghost-lasso-lab.json")
    audit = analyze_error_tail_invariant_set()
    attempts = [
        transfer_attempt(ticket90, "riemann", "RH-TICKET-91", "ExplicitFormulaInvariantSetAudit", "Characterize and escape the full sign-preserving invariant cone, not one limiting kernel."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-91",
            "route": "NormalizedErrorTailConjugacyAndSingleGhostNoGo",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact growing-precision tail conjugacy plus invariant-set route correction",
            "attempt": "Determine what the beta ghost represents and whether separation from it can force the missing 00 recurrence.",
            "bounded_result": {"source_ticket": "CO-TICKET-90", "error_tail_invariant_set_audit": audit},
            "obstruction": audit["golden_mean_obstruction"]["single_ghost_no_go"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET92 around arithmetic escape from the full golden-mean invariant set.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket90, "goldbach", "GB-TICKET-91", "ExceptionalCharacterInvariantSetAudit", "Characterize and escape the full positivity-obstructing character cone."),
        transfer_attempt(ticket90, "twin-prime", "TP-TICKET-91", "ParityBarrierInvariantSetAudit", "Characterize and escape the full parity-preserving sieve invariant set."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "error_tail_invariant_set_open_no_collatz_resolution",
        "claim_boundary": "Ticket 91 proves one exact coordinate theorem and one proof-route no-go but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket91-error-tail-invariant-set-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-91-error-tail-invariant-set.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-91-error-tail-invariant-set.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-91-error-tail-invariant-set.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-91-error-tail-invariant-set.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
