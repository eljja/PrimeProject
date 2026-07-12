from __future__ import annotations

from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-11T23:05:00+09:00"
SCHEMA = "primeproject.ticket85-accessible-cycle-supremum-lab.v1"
MIN_HORIZON = 2
MAX_HORIZON = 256
SAMPLE_HORIZONS = {2, 3, 4, 8, 16, 32, 64, 128, 256}


def cycle_formula(length: int) -> dict[str, Any]:
    if length < 2:
        raise ValueError("cycle length must be at least 2")
    power_two = 1 << (length + 1)
    power_three = 3**length
    constant = 5 * 3 ** (length - 1) - power_two
    denominator = power_two - power_three
    cycle_value = Fraction(constant, denominator)
    target_numerator = 7 * 3 ** (length - 1) - power_two
    target_denominator = denominator
    target = Fraction(target_numerator, target_denominator)
    return {
        "length": length,
        "valuation_sum": length + 1,
        "mean_valuation": Fraction(length + 1, length),
        "reciprocal_mean": Fraction(length, length + 1),
        "constant": constant,
        "denominator": denominator,
        "cycle_value": cycle_value,
        "target_power": target,
    }


def symbolic_states(horizon: int) -> list[dict[str, int]]:
    constant = -1
    denominator_power = 1
    states = [{"post_index": 0, "constant": constant, "denominator_power": denominator_power, "incoming_valuation": 2}]
    for post_index in range(1, horizon + 1):
        valuation = 2 if post_index == 1 else 1
        constant = 3 * constant + (1 << denominator_power)
        denominator_power += valuation
        states.append({"post_index": post_index, "constant": constant, "denominator_power": denominator_power, "incoming_valuation": valuation})
    return states


def target_modulus_value(target: Fraction, precision: int) -> int:
    modulus = 1 << precision
    return (target.numerator * pow(target.denominator, -1, modulus)) % modulus


def hensel_exponent_residue(target: Fraction, precision: int) -> tuple[int, int]:
    residue = 1
    lift_count = 0
    if target_modulus_value(target, 3) != 3:
        raise AssertionError("target is outside the odd exponent image modulo 8")
    for current_precision in range(3, precision):
        step = 1 << (current_precision - 2)
        modulus = 1 << (current_precision + 1)
        target_residue = target_modulus_value(target, current_precision + 1)
        candidates = (residue, residue + step)
        valid = [candidate for candidate in candidates if pow(3, candidate, modulus) == target_residue]
        if len(valid) != 1:
            raise AssertionError("cycle exponent lift lost uniqueness")
        residue = valid[0]
        lift_count += 1
    return residue, lift_count


def audit_horizon(horizon: int) -> dict[str, Any]:
    cycle = cycle_formula(horizon)
    states = symbolic_states(horizon)
    final_d = states[-1]["denominator_power"]
    precision = final_d + 1
    residue, lift_count = hensel_exponent_residue(cycle["target_power"], precision)
    period_log2 = precision - 2
    period = 1 << period_log2
    exponent = residue + period
    formula_failure_count = 0
    accessibility_failure_count = 0
    valuation_failure_count = 0
    constant_bound_failure_count = 0

    if final_d != horizon + 2:
        formula_failure_count += 1
    cycle_value = cycle["cycle_value"]
    replayed_cycle = cycle_value
    for valuation in [2] + [1] * (horizon - 1):
        replayed_cycle = (3 * replayed_cycle + 1) / (1 << valuation)
    if replayed_cycle != cycle_value:
        formula_failure_count += 1
    cycle_mod8 = (cycle_value.numerator * pow(cycle_value.denominator, -1, 8)) % 8
    if cycle_mod8 != 1 or target_modulus_value(cycle["target_power"], 4) != 3:
        accessibility_failure_count += 1

    first_image = (3 * cycle_value + 1) / 4
    y_plus_one = first_image + 1
    if y_plus_one.numerator % (1 << horizon) != 0 or y_plus_one.numerator % (1 << (horizon + 1)) == 0:
        formula_failure_count += 1

    for state in states:
        post_index = state["post_index"]
        d_t = state["denominator_power"]
        constant = state["constant"]
        modulus = 1 << (d_t + 1)
        if (pow(3, exponent + post_index, modulus) + constant) % modulus != 1 << d_t:
            valuation_failure_count += 1
        if abs(constant) >= 1 << (2 * post_index + 1):
            constant_bound_failure_count += 1

    range_failure_count = int(not (0 < residue < period and period < exponent < 2 * period))
    base_growth_guard = 3**9 > 1 << 14
    growth_failure_count = int(not (base_growth_guard and exponent >= (1 << (horizon + 1)) + 1))
    exponent_cap_failure_count = int(exponent >= 1 << (horizon + 2))
    total_failures = (
        formula_failure_count
        + accessibility_failure_count
        + valuation_failure_count
        + constant_bound_failure_count
        + range_failure_count
        + growth_failure_count
        + exponent_cap_failure_count
    )
    return {
        "horizon": horizon,
        "cycle_word": "2," + ",".join("1" for _ in range(horizon - 1)),
        "mean_valuation": f"{horizon + 1}/{horizon}",
        "reciprocal_mean": f"{horizon}/{horizon + 1}",
        "precision": precision,
        "lift_count": lift_count,
        "residue": residue,
        "period_log2": period_log2,
        "exponent": exponent,
        "post_descent_delay_strict_lower_bound": horizon,
        "logarithmic_lower_bound": "delay > log2(k_H)-2",
        "symbolic_state_count": len(states),
        "formula_failure_count": formula_failure_count,
        "accessibility_failure_count": accessibility_failure_count,
        "valuation_failure_count": valuation_failure_count,
        "constant_bound_failure_count": constant_bound_failure_count,
        "range_failure_count": range_failure_count,
        "growth_failure_count": growth_failure_count,
        "exponent_cap_failure_count": exponent_cap_failure_count,
        "total_failure_count": total_failures,
    }


def analyze_cycle_supremum() -> dict[str, Any]:
    rows = [audit_horizon(horizon) for horizon in range(MIN_HORIZON, MAX_HORIZON + 1)]
    failures = sum(int(row["total_failure_count"]) for row in rows)
    states = sum(int(row["symbolic_state_count"]) for row in rows)
    lifts = sum(int(row["lift_count"]) for row in rows)
    samples = [row for row in rows if int(row["horizon"]) in SAMPLE_HORIZONS]
    status = "accessible_cycle_supremum_one_proved_no_collatz_resolution" if failures == 0 else "accessible_cycle_supremum_audit_inconclusive_no_collatz_resolution"
    return {
        "theorem_name": "AccessibleCycleCoefficientSupremumOne",
        "source_ticket": "CO-TICKET-84",
        "cycle_family": {
            "word": "w_m=(2,1,...,1) of length m>=2",
            "valuation_sum": "S_m=m+1",
            "cycle_constant": "C_m=5*3^(m-1)-2^(m+1)",
            "cycle_value": "x_m=C_m/(2^(m+1)-3^m)",
            "first_image_guard": "If y_m=(3x_m+1)/4 then v2(y_m+1)=m, proving the following m-1 valuation-one steps are exact.",
            "accessibility": "x_m=1 mod 8, hence 2x_m+1=3 mod 16 and lies in the odd 2-adic exponent image.",
            "reciprocal_mean": "m/(m+1) approaches 1 from below.",
        },
        "supremum_statement": (
            "Among accessible finite periodic accelerated valuation words, reciprocal mean valuation has supremum 1. "
            "It is not attained: equality requires the all-ones word, whose cycle is -1 and whose exponent target -1 is 7 mod 8, outside the odd power-of-3 image."
        ),
        "delay_statement": (
            "For every H>=2, choosing m=H and lifting the length-H cycle yields a positive exponent k_H with "
            "D(k_H)>H>log2(k_H)-2. Consequently every c*log2(k)+C window with fixed c<1 and C fails infinitely often."
        ),
        "proof_chain": [
            "Composition of the word (2,1^(m-1)) gives valuation sum m+1 and constant C_m=5*3^(m-1)-2^(m+1).",
            "Its fixed point x_m=C_m/(2^(m+1)-3^m) is 1 modulo 8, so the target 2x_m+1 lies in the odd exponent image.",
            "The first valuation is exactly 2; for y_m=(3x_m+1)/4, the identity y_m+1=2^m/(2^(m+1)-3^m) proves the next m-1 valuations are exactly 1.",
            "At precision H+3, the unique exponent residue is lifted one bit at a time and shifted by one period to a positive exponent k_H between 2^(H+1) and 2^(H+2).",
            "The symbolic affine and growth bounds from TICKET84 force every post iterate through H above 2^k_H-1, so D(k_H)>H.",
            "Since k_H<2^(H+2), H>log2(k_H)-2.",
            "Every valuation is at least 1, so reciprocal mean is at most 1; the accessible family m/(m+1) approaches 1, proving the supremum.",
            "Mean 1 requires the all-ones word. Its fixed point is -1 and target 2x+1=-1=7 mod 8, so no odd 2-adic exponent maps to it; the supremum is not attained."
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_horizon": MAX_HORIZON,
            "horizon_case_count": len(rows),
            "symbolic_state_count": states,
            "hensel_lift_count": lifts,
            "maximum_precision": MAX_HORIZON + 3,
            "total_failure_count": failures,
            "samples": samples,
        },
        "computational_failure_count": failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {"family": "accessible_coefficient_supremum_below_one", "status": "refuted_by_cycle_family", "counteredge": "m/(m+1) approaches 1 through accessible exact cycles."},
            {"family": "accessible_coefficient_one_attained", "status": "refuted_by_exponent_image_mod8", "counteredge": "The only mean-one word is all ones; its cycle -1 targets 7 mod 8 rather than the odd power-of-3 coset 3 mod 8."},
            {"family": "subunit_logarithmic_mersenne_window", "status": "refuted_with_arbitrary_additive_constant", "counteredge": "D(k_H)>log2(k_H)-2 makes every c log2(k)+C with c<1 fail eventually."},
        ],
        "discarded_route": "Search for an accessible periodic cycle with reciprocal mean strictly above 1, or treat the inaccessible all-ones cycle as an attained natural exponent construction.",
        "retained_route": "Attack the coefficient-one boundary: sharpen the additive constant, or prove/refute a universal Mersenne upper window log2(k)+O(1).",
        "candidate_theorem": "CoefficientOneBoundary: determine the optimal additive term B(k) in explicit lower bounds D(k)>=log2(k)-B(k), and independently test a universal upper bound D(k)<=log2(k)+O(1) for Mersenne starts.",
        "next_theorem_target": "CoefficientOneBoundary",
        "equivalence_warning": "Near-logarithmic finite delay is not divergence. No upper bound for all Mersenne starts, and no theorem for all integers, is proved.",
        "novelty_boundary": "PrimeProject claims the explicit accessible cycle family, exact supremum corollary, coefficient-one-minus-two delay construction, and audit. Independent literature review remains required.",
        "proof_boundary": "TICKET85 proves a restricted cycle-optimization and finite-delay theorem. It solves none of the four open problems and constructs no divergent orbit."
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {"problem_id": problem_id, "ticket_id": ticket_id, "status": "proof_pressure_open", "route": route, "proof_or_counterexample_mode": "accessible completion-family optimization transfer discipline", "attempt": "Transfer only the discipline of proving admissibility before optimizing a completion-space family.", "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket85_transfer": route, "candidate_theorem": target}, "obstruction": "No target-specific accessible completion family was proved.", "candidate_theorem": target, "next_experiment": "Construct and classify a target-specific admissible family.", "claim_boundary": f"No {label} proof and no certified {label} counterexample."}


def main() -> int:
    ticket84 = read_json(ROOT / "data/open-problem/ticket84-two-adic-cycle-log-delay-lab.json")
    audit = analyze_cycle_supremum()
    attempts = [
        transfer_attempt(ticket84, "riemann", "RH-TICKET-85", "AccessibleKernelFamilyGuard", "Classify admissible kernel families before optimizing positivity margins."),
        {"problem_id": "collatz", "ticket_id": "CO-TICKET-85", "route": "AccessibleCycleCoefficientSupremumOne", "status": audit["theorem_status"], "proof_or_counterexample_mode": "exact accessible periodic cycle family plus positive exponent lifts", "attempt": "Determine the exact supremum of logarithmic delay coefficients obtainable from accessible periodic valuation cycles.", "bounded_result": {"source_ticket": "CO-TICKET-84", "accessible_cycle_supremum_audit": audit}, "obstruction": audit["discarded_route"], "candidate_theorem": audit["candidate_theorem"], "next_experiment": "Build TICKET86 at the coefficient-one additive boundary.", "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample."},
        transfer_attempt(ticket84, "goldbach", "GB-TICKET-85", "AccessibleCharacterFamilyGuard", "Classify admissible exceptional-character families before optimizing constants."),
        transfer_attempt(ticket84, "twin-prime", "TP-TICKET-85", "AccessibleParityFamilyGuard", "Classify admissible parity-breaking families before optimizing exact-gap mass."),
    ]
    payload = {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": "accessible_cycle_supremum_open_no_collatz_resolution", "claim_boundary": "Ticket 85 proves one restricted Collatz cycle-family theorem but solves none of the four open problems.", "attempts": attempts}
    write_json(ROOT / "data/open-problem/ticket85-accessible-cycle-supremum-lab.json", payload)
    paths = {"riemann": ROOT / "data/open-problem/riemann/rh-ticket-85-accessible-cycle-supremum.json", "collatz": ROOT / "data/open-problem/collatz/co-ticket-85-accessible-cycle-supremum.json", "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-85-accessible-cycle-supremum.json", "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-85-accessible-cycle-supremum.json"}
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
