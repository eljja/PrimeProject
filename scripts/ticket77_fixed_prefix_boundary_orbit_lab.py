from __future__ import annotations

from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json
from ticket76_symbolic_boundary_recurrence_lab import (
    boundary_state,
    reconstruct_source_layers,
    replay_word,
)


GENERATED_AT = "2026-07-11T01:20:00+09:00"
SCHEMA = "primeproject.ticket77-fixed-prefix-boundary-orbit-lab.v1"
EXAMPLE_LIMIT = 8
ORBIT_AUDIT_MAX_PREFIX_LENGTH = 10
TRACE_GUARD = 100_000


def pressure_step(boundary_quotient: int, unit: int) -> dict[str, Any]:
    if boundary_quotient <= 0 or unit <= 0 or unit % 2 == 0:
        raise ValueError("pressure_step requires a positive quotient and a positive odd unit")
    digit = (-boundary_quotient * pow(unit, -1, 16)) % 16
    numerator = boundary_quotient + digit * unit
    if numerator % 16:
        raise RuntimeError("canonical four-bit pressure digit did not clear the low four bits")
    next_quotient = numerator // 16
    return {
        "digit": digit,
        "next_boundary_quotient": next_quotient,
        "strict_pressure_continues": next_quotient % 2 == 0,
        "boundary_event": "strictly_beyond_boundary" if next_quotient % 2 == 0 else "equality_boundary_rollback",
        "normalized_valuation": 4 + v2(next_quotient),
    }


def trace_strict_pressure_segment(boundary_quotient: int, prefix_length: int) -> dict[str, Any]:
    unit = 3 ** (prefix_length + 1)
    current = boundary_quotient
    seen: dict[int, int] = {}
    examples: list[dict[str, int]] = []
    entered_finite_orbit_at: int | None = None

    for step_index in range(TRACE_GUARD):
        if current < unit and entered_finite_orbit_at is None:
            entered_finite_orbit_at = step_index
        if current in seen:
            return {
                "status": "two_adic_fixed_cycle" if prefix_length == 0 and current == 2 else "unexpected_strict_cycle",
                "pressure_step_count": step_index,
                "entered_finite_orbit_at": entered_finite_orbit_at,
                "terminal_boundary_quotient": current,
                "cycle_start": seen[current],
                "cycle_length": step_index - seen[current],
                "examples": examples,
            }
        seen[current] = step_index
        transition = pressure_step(current, unit)
        next_quotient = int(transition["next_boundary_quotient"])
        if len(examples) < EXAMPLE_LIMIT:
            examples.append(
                {
                    "step": step_index + 1,
                    "source_boundary_quotient": current,
                    "digit": int(transition["digit"]),
                    "next_boundary_quotient": next_quotient,
                }
            )
        if not transition["strict_pressure_continues"]:
            return {
                "status": "equality_boundary_reached",
                "pressure_step_count": step_index + 1,
                "entered_finite_orbit_at": entered_finite_orbit_at,
                "terminal_boundary_quotient": next_quotient,
                "terminal_parity": "odd",
                "rollback_effect": "the equality valuation is lift-unstable, so stable-prefix normalization rolls it back",
                "examples": examples,
            }
        current = next_quotient

    return {
        "status": "trace_guard_exhausted",
        "pressure_step_count": TRACE_GUARD,
        "entered_finite_orbit_at": entered_finite_orbit_at,
        "terminal_boundary_quotient": current,
        "examples": examples,
    }


def audit_unit_orbits() -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for prefix_length in range(ORBIT_AUDIT_MAX_PREFIX_LENGTH + 1):
        unit = 3 ** (prefix_length + 1)
        expected_order = 3**prefix_length
        inverse_16 = pow(16, -1, unit)
        order_identity_holds = pow(16, expected_order, unit) == 1
        order_minimality_holds = (
            prefix_length == 0 or pow(16, expected_order // 3, unit) != 1
        )
        class_audits = []
        for residue_class in (1, 2):
            expected = {value for value in range(1, unit) if value % 3 == residue_class}
            orbit = []
            current = residue_class
            for _ in range(expected_order):
                orbit.append(current)
                current = (current * inverse_16) % unit
            orbit_set = set(orbit)
            odd_values = sorted(value for value in orbit_set if value % 2 == 1)
            even_values = sorted(value for value in orbit_set if value % 2 == 0)
            class_audits.append(
                {
                    "residue_class_mod_3": residue_class,
                    "orbit_size": len(orbit_set),
                    "expected_class_size": len(expected),
                    "covers_residue_class": orbit_set == expected,
                    "returns_to_start": current == residue_class,
                    "odd_representative_count": len(odd_values),
                    "first_odd_representative": odd_values[0] if odd_values else None,
                    "even_representative_count": len(even_values),
                    "first_even_representative": even_values[0] if even_values else None,
                }
            )
        audits.append(
            {
                "prefix_length": prefix_length,
                "unit": unit,
                "expected_order": expected_order,
                "order_identity_holds": order_identity_holds,
                "order_minimality_holds": order_minimality_holds,
                "class_audits": class_audits,
            }
        )
    return audits


def audit_observed_sources() -> dict[str, Any]:
    fourth, fifth, reconstruction = reconstruct_source_layers()
    layers = ((5, fourth), (6, fifth))
    source_count = 0
    prerequisite_failure_count = 0
    one_step_identity_failure_count = 0
    trace_guard_failure_count = 0
    unexpected_strict_cycle_count = 0
    two_adic_fixed_cycle_count = 0
    equality_boundary_count = 0
    max_pressure_steps = 0
    max_pressure_source: dict[str, Any] | None = None
    prefix_lengths: Counter[int] = Counter()
    path_lengths: Counter[int] = Counter()
    status_counts: Counter[str] = Counter()
    trace_cache: dict[tuple[int, int], dict[str, Any]] = {}
    examples: list[dict[str, Any]] = []

    for depth, entries in layers:
        for source_entry in entries:
            source_count += 1
            source = source_entry["row"]["child_certificate"]
            boundary = boundary_state(source)
            prefix_length = int(boundary["prefix_length"])
            boundary_quotient = int(boundary["boundary_quotient"])
            unit = 3 ** (prefix_length + 1)
            prefix_lengths[prefix_length] += 1
            prerequisites_hold = (
                boundary_quotient > 0
                and boundary_quotient % 3 != 0
                and ((1 << int(boundary["boundary_slack"])) * boundary_quotient - 1) % 3 == 0
            )
            if not prerequisites_hold:
                prerequisite_failure_count += 1

            transition = pressure_step(boundary_quotient, unit)
            digit = int(transition["digit"])
            child_residue = int(source["residue"]) | (digit << int(source["modulus_bits"]))
            child_current, replay_mismatches = replay_word(
                child_residue,
                tuple(int(value) for value in boundary["word"]),
            )
            actual_valuation = v2(3 * child_current + 1)
            predicted_valuation = int(boundary["boundary_slack"]) + int(
                transition["normalized_valuation"]
            )
            if replay_mismatches or actual_valuation != predicted_valuation:
                one_step_identity_failure_count += 1

            cache_key = (prefix_length, boundary_quotient)
            trace = trace_cache.get(cache_key)
            if trace is None:
                trace = trace_strict_pressure_segment(boundary_quotient, prefix_length)
                trace_cache[cache_key] = trace
            status = str(trace["status"])
            status_counts[status] += 1
            pressure_steps = int(trace["pressure_step_count"])
            path_lengths[pressure_steps] += 1
            if status == "equality_boundary_reached":
                equality_boundary_count += 1
            elif status == "two_adic_fixed_cycle":
                two_adic_fixed_cycle_count += 1
            elif status == "unexpected_strict_cycle":
                unexpected_strict_cycle_count += 1
            elif status == "trace_guard_exhausted":
                trace_guard_failure_count += 1
            if pressure_steps > max_pressure_steps:
                max_pressure_steps = pressure_steps
                max_pressure_source = {
                    "depth": depth,
                    "root_id": int(source_entry["root_id"]),
                    "residue": int(source["residue"]),
                    "modulus_bits": int(source["modulus_bits"]),
                    "prefix_length": prefix_length,
                    "boundary_quotient": boundary_quotient,
                    "trace": trace,
                }
            if len(examples) < EXAMPLE_LIMIT:
                examples.append(
                    {
                        "depth": depth,
                        "residue": int(source["residue"]),
                        "modulus_bits": int(source["modulus_bits"]),
                        "prefix_length": prefix_length,
                        "boundary_quotient": boundary_quotient,
                        "canonical_digit": digit,
                        "trace_status": status,
                        "pressure_step_count": pressure_steps,
                    }
                )

    return {
        "reconstruction": reconstruction,
        "source_count": source_count,
        "unique_boundary_state_count": len(trace_cache),
        "prefix_length_distribution": [
            {"prefix_length": key, "source_count": prefix_lengths[key]}
            for key in sorted(prefix_lengths)
        ],
        "status_counts": dict(sorted(status_counts.items())),
        "strict_pressure_equality_boundary_count": equality_boundary_count,
        "two_adic_fixed_cycle_count": two_adic_fixed_cycle_count,
        "unexpected_strict_cycle_count": unexpected_strict_cycle_count,
        "trace_guard_failure_count": trace_guard_failure_count,
        "prerequisite_failure_count": prerequisite_failure_count,
        "one_step_identity_failure_count": one_step_identity_failure_count,
        "max_strict_pressure_step_count": max_pressure_steps,
        "max_strict_pressure_source": max_pressure_source,
        "pressure_step_distribution": [
            {"pressure_step_count": key, "source_count": path_lengths[key]}
            for key in sorted(path_lengths)
        ],
        "examples": examples,
    }


def analyze_fixed_prefix_boundary_orbit() -> dict[str, Any]:
    orbit_audits = audit_unit_orbits()
    observed = audit_observed_sources()
    orbit_failure_count = sum(
        int(not audit["order_identity_holds"])
        + int(not audit["order_minimality_holds"])
        + sum(
            int(not row["covers_residue_class"]) + int(not row["returns_to_start"])
            for row in audit["class_audits"]
        )
        for audit in orbit_audits
    )
    nonexceptional_parity_failures = sum(
        1
        for audit in orbit_audits
        for row in audit["class_audits"]
        if audit["prefix_length"] >= 1
        and (row["odd_representative_count"] == 0 or row["even_representative_count"] == 0)
    )
    exceptional_rows = [
        row
        for audit in orbit_audits
        if audit["prefix_length"] == 0
        for row in audit["class_audits"]
        if row["odd_representative_count"] == 0
    ]
    computational_failures = (
        orbit_failure_count
        + nonexceptional_parity_failures
        + int(len(exceptional_rows) != 1)
        + int(observed["prerequisite_failure_count"])
        + int(observed["one_step_identity_failure_count"])
        + int(observed["unexpected_strict_cycle_count"])
        + int(observed["trace_guard_failure_count"])
    )
    status = (
        "fixed_prefix_boundary_orbit_classified_no_collatz_resolution"
        if computational_failures == 0
        else "fixed_prefix_boundary_orbit_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "FixedStablePrefixBoundaryOrbitAndTwoAdicGhostClassification",
        "source_ticket": "CO-TICKET-76",
        "source_status": "symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution",
        "pressure_map": {
            "unit": "u = 3^(m+1)",
            "canonical_digit": "h(A) is the unique h in {0,...,15} with A+h*u = 0 mod 16",
            "successor": "P(A) = (A+h(A)*u)/16",
            "strict_pressure_condition": "P(A) even means the next valuation lies strictly beyond the new modulus boundary",
            "equality_rollback_condition": "P(A) odd means the valuation reaches the boundary exactly; stable-prefix normalization rolls that equality step back",
        },
        "proof_chain": [
            "Reachability gives 2^d*A = 3*T^m(r)+1, hence 3 does not divide A.",
            "If A>u, then 0<P(A)<A; the normalized boundary orbit eventually enters 1<=A<u.",
            "Inside 1<=A<u, P(A) is the least positive representative of 16^(-1)*A modulo u.",
            "The multiplicative order of 16 modulo 3^(m+1) is 3^m by v3(16^(3^j)-1)=j+1.",
            "For m>=1 the orbit is every unit in one nonzero residue class modulo 3 and contains both even and odd representatives.",
            "Odd P(A) ends a strict-beyond-boundary segment but does not end the stable-prefix orbit, because the equality valuation is rolled back.",
            "The all-depth compatible cylinders converge to a 2-adic point N satisfying T^m(N)=-1/3.",
            "Such a point is not a positive integer and therefore is not a Collatz counterexample.",
        ],
        "orbit_identity": {
            "formula": "ord_(3^(m+1))(16) = 3^m",
            "valuation_identity": "v3(16^(3^j)-1) = j+1",
            "audited_prefix_lengths": [0, ORBIT_AUDIT_MAX_PREFIX_LENGTH],
            "audit_failure_count": orbit_failure_count,
            "nonexceptional_parity_failure_count": nonexceptional_parity_failures,
            "exceptional_zero_odd_rows": exceptional_rows,
            "audits": orbit_audits,
        },
        "observed_source_audit": observed,
        "computational_failure_count": computational_failures,
        "theorem_status": status,
        "bounded_lemma": (
            "The exact TICKET76 recurrence gives an eventually periodic inverse-16 boundary orbit of period 3^m. "
            "Strict pressure segments reach equality boundaries, but equality rollback preserves the stable prefix; the "
            "all-depth completion is a 2-adic preimage of -1/3 rather than a positive integer."
        ),
        "discarded_route": (
            "Treat P(A) odd as extinction of the stable prefix. It only marks an equality valuation at the current modulus; "
            "the lift-stability rule must roll that step back before the next refinement."
        ),
        "closed_route": (
            "Promote an all-depth fixed-prefix compatible cylinder directly to a natural-number counterexample. The exact "
            "completion lands at a 2-adic preimage of -1/3, not at a positive integer."
        ),
        "remaining_obstruction": (
            "A positive integer may shadow longer and longer finite prefixes without realizing one fixed 2-adic ghost. The "
            "project still lacks a well-founded rank controlling successive changing-prefix approximation events."
        ),
        "candidate_theorem": (
            "ChangingPrefixNaturalAdmissibilityRank: every positive-integer boundary refinement either enters the known basin "
            "or strictly decreases a global rank, while every nondecreasing compatible limit is proved non-natural."
        ),
        "next_theorem_target": "ChangingPrefixNaturalAdmissibilityRank",
        "formalization_boundary": (
            "The modular orbit classification is an elementary exact argument, with finite orbit identities audited through "
            f"m={ORBIT_AUDIT_MAX_PREFIX_LENGTH}. The 2-adic admissibility bridge still requires formalization and does not prove Collatz."
        ),
        "proof_boundary": (
            "TICKET77 classifies fixed-prefix boundary completions as 2-adic ghosts. It does not exclude infinitely many "
            "changing-prefix events, divergence, or nontrivial cycles of the accelerated Collatz map."
        ),
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "orbit closure proof discipline",
        "attempt": (
            "Transfer only the TICKET77 discipline: derive an exact normalized orbit, classify every recurrent state, and "
            "separate nonphysical completion points from admissible counterexamples. No Collatz theorem is transferred."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "ticket77_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No problem-specific orbit classification was performed for this problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Derive a problem-specific normalized orbit and classify its admissible recurrent states.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket76 = read_json(ROOT / "data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json")
    collatz_audit = analyze_fixed_prefix_boundary_orbit()
    attempts = [
        transfer_attempt(
            ticket76,
            "riemann",
            "RH-TICKET-77",
            "ExplicitFormulaRecurrentStateClassification",
            "Every recurrent normalized explicit-formula state is classified and any off-line state violates an exact positivity or admissibility condition.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-77",
            "route": "FixedPrefixBoundaryOrbitAndTwoAdicGhostClassification",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact orbit classification plus positive-integer admissibility",
            "attempt": (
                "Classify the exact TICKET76 fixed-prefix recurrence globally, distinguish strict pressure from equality "
                "rollback, and decide whether its all-depth completion is an admissible positive-integer counterexample."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-76", "fixed_prefix_boundary_orbit_audit": collatz_audit},
            "obstruction": collatz_audit["remaining_obstruction"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Construct an admissibility rank across changing-prefix approximations to 2-adic ghosts.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket76,
            "goldbach",
            "GB-TICKET-77",
            "ExceptionalStateAdmissibilityClassification",
            "Every recurrent exceptional-state orbit is either analytically inadmissible or has a uniform positive representation margin.",
        ),
        transfer_attempt(
            ticket76,
            "twin-prime",
            "TP-TICKET-77",
            "ParityStateOrbitClassification",
            "Every recurrent parity-sensitive sieve state is classified and at least one admissible class retains a positive exact-gap lower bound.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "fixed_prefix_boundary_orbit_open_no_collatz_resolution",
        "claim_boundary": "Ticket 77 classifies a fixed-prefix Collatz boundary orbit but does not solve any open problem.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-77-fixed-prefix-boundary-orbit.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-77-fixed-prefix-boundary-orbit.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-77-fixed-prefix-boundary-orbit.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-77-fixed-prefix-boundary-orbit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
