from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-17T02:15:19+09:00"
SCHEMA = "primeproject.ticket127-exception-repair-effective-bridges.v1"
TOLERANCE = 1e-12


def riemann_dense_core_counterexample_audit() -> dict[str, Any]:
    rational_witness = (Fraction(7, 5), Fraction(2, 1))
    witness_value = rational_witness[0] ** 2 - rational_witness[1] ** 2
    return {
        "theorem_name": "DenseCoreNegativeWitnessSemidecision",
        "setting": (
            "Let V be a separable topological vector space, let Q:V->R be "
            "continuous, and let D={d_0,d_1,...} be an explicitly enumerable "
            "dense core. Normalize the exact RH-equivalent Weil criterion so "
            "that RH requires Q(g)>=0 for every admissible g in V."
        ),
        "proved_statement": (
            "If an admissible g has Q(g)<0, then some enumerated core element "
            "d_j has Q(d_j)<0. If interval evaluation is complete for strict "
            "negative values, dovetailed core enumeration semidecides a "
            "counterexample to the criterion."
        ),
        "proof": (
            "Continuity makes Q^{-1}((-infinity,0)) open. A negative witness g "
            "therefore has an open neighborhood contained in the negative set. "
            "Density gives d_j in that neighborhood. A complete strict-sign "
            "interval evaluator eventually returns an upper endpoint below zero "
            "for d_j, so dovetailing eventually halts on every real violation."
        ),
        "effective_assumptions": [
            "an exact RH-equivalent Weil criterion with one fixed sign convention",
            "a proved dense enumerable core inside the completed admissible space",
            "validated interval evaluation complete for every strict negative core value",
        ],
        "finite_sanity_model": {
            "space": "R^2 with Q(x,y)=x^2-y^2 and dense core Q^2",
            "core_witness": ["7/5", "2"],
            "exact_value": f"{witness_value.numerator}/{witness_value.denominator}",
            "negative": witness_value < 0,
        },
        "route_decision": {
            "retain": "interval-certified enumeration as an RH-counterexample semidecision route",
            "discard": "treating finite failure to find a negative core element as a proof of RH",
            "next_theorem": "IntervalCertifiedWeilCoreEvaluator",
        },
        "machine_audit": {
            "finite_sanity_failure_count": int(witness_value >= 0),
            "conjecture_resolution_count": 0,
            "total_failure_count": int(witness_value >= 0),
        },
        "proof_boundary": (
            "The theorem makes counterexample search complete under its explicit "
            "topological and effective assumptions. It supplies neither the dense "
            "Weil core nor a negative witness, and finite non-discovery proves no RH case."
        ),
    }


def collatz_nontrivial_path_correction_audit() -> dict[str, Any]:
    source = read_json(
        ROOT / "data/open-problem/ticket126-route-correction-audit.json"
    )["route_correction_audit"]["collatz"]
    last = source["precision_rows"][-1]
    trivial_present = bool(last.get("trivial_fixed_path_present"))
    unresolved = int(last["unresolved_class_count"])
    nontrivial = int(last["nontrivial_unresolved_class_count"])
    expected_nontrivial = unresolved - 1
    failures = int(not trivial_present) + int(nontrivial != expected_nontrivial)
    return {
        "theorem_name": "NontrivialEventuallyLowPathIffFiniteStoppingCounterexample",
        "corrected_statement": (
            "For every positive odd integer n>1, n has no finite strict "
            "Collatz descent if and only if its compatible residue path is a "
            "nontrivial eventually-low infinite path in the adaptive unresolved tree."
        ),
        "proof": (
            "Apply the exact TICKET126 path equivalence to n>1. TICKET125 proves "
            "that every n>1 has a finite strict descent exactly when Collatz "
            "holds. The fixed n=1 path is eventually low and survives every "
            "tree level, but it belongs to the known terminal basin and is not a counterexample."
        ),
        "historical_correction": {
            "ticket": "TICKET-126",
            "error": (
                "The original Collatz corollary said that all eventually-low "
                "paths must be absent, omitting the necessary n>1 qualifier."
            ),
            "repair": (
                "Retain the exact path equivalence, explicitly keep the n=1 "
                "path, and exclude only nontrivial eventually-low paths."
            ),
            "scientific_effect": (
                "The old exclusion target was impossible because n=1 is a "
                "permanent witness. The corrected target is logically equivalent to Collatz."
            ),
        },
        "exact_28_bit_audit": {
            "odd_class_count": int(last["odd_class_count"]),
            "all_unresolved_class_count": unresolved,
            "trivial_fixed_path_count": 1,
            "nontrivial_unresolved_class_count": nontrivial,
            "nontrivial_unresolved_mass": float(
                last["nontrivial_unresolved_mass"]
            ),
            "maximum_all_low_run": int(
                last["maximum_consecutive_low_refinements"]
            ),
            "maximum_nontrivial_low_run": int(
                last["maximum_nontrivial_consecutive_low_refinements"]
            ),
            "longest_nontrivial_witnesses": list(
                last["longest_nontrivial_low_run_witnesses"]
            ),
        },
        "route_decision": {
            "retain": "natural-number inverse-limit paths with n>1",
            "discard": "the impossible target of excluding the fixed n=1 path",
            "next_theorem": "UniformNontrivialEventuallyLowPathExclusion",
        },
        "machine_audit": {
            "base_exception_present": trivial_present,
            "nontrivial_count_identity_holds": nontrivial == expected_nontrivial,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The equivalence and correction are exact. The finite 28-bit tree "
            "still leaves nontrivial classes and does not prove their uniform exclusion."
        ),
    }


def _primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            sieve[prime * prime :: prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return [number for number, flag in enumerate(sieve) if flag]


def goldbach_singular_series_lower_bound_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for maximum_m in (2, 4, 10, 100, 1_000, 10_000):
        prime_product = 1.0
        for prime in _primes_up_to(maximum_m + 1):
            if prime > 2:
                prime_product *= 1.0 - 1.0 / (prime - 1) ** 2
        telescoping = (maximum_m + 1) / (2.0 * maximum_m)
        holds = prime_product + TOLERANCE >= telescoping > 0.5
        failures += int(not holds)
        rows.append(
            {
                "maximum_m": maximum_m,
                "prime_subset_product": prime_product,
                "full_integer_telescoping_product": telescoping,
                "subset_product_dominates": holds,
            }
        )

    ticket126 = read_json(
        ROOT / "data/open-problem/ticket126-route-correction-audit.json"
    )["route_correction_audit"]["goldbach"]
    tail = ticket126["uniform_tail"]
    return {
        "theorem_name": "UniformBinaryGoldbachSingularSeriesLowerBound",
        "definition": (
            "For even N, S(N)=2*C2*product_{p|N,p>2}(p-1)/(p-2), "
            "where C2=product_{p>2}(1-1/(p-1)^2). Define the exact residual "
            "R(N)=G(N)-S(N)N."
        ),
        "proved_statement": "S(N)>=1 for every positive even N.",
        "proof": (
            "Every correction factor (p-1)/(p-2) is at least one. For M>=2, "
            "the prime-indexed factors of C2 form a subset of the factors "
            "1-1/m^2, 2<=m<=M. All factors lie in (0,1), so the prime subset "
            "product is at least the full product. The latter telescopes to "
            "(M+1)/(2M)>1/2. Taking the convergent decreasing prime-product "
            "limit gives C2>=1/2 and hence S(N)>=1."
        ),
        "exact_normalization_consequence": {
            "identity": "G(N)=S(N)N+R(N)",
            "lower_bound": "G(N)>=N-|R(N)|",
            "closed_coefficient": "A=1",
            "scope": (
                "This closes only the singular-series coefficient after R is "
                "defined against the exact Hardy-Littlewood model. It proves no residual estimate."
            ),
        },
        "finite_sanity_rows": rows,
        "endpoint_budget": {
            "verified_limit_H": int(tail["verified_limit"]),
            "proper_prime_power_B": float(tail["explicit_uniform_B"]),
            "strict_required_residual_K_ceiling": float(
                tail["strict_K_ceiling_for_A_1"]
            ),
        },
        "route_decision": {
            "closed_premise": "normalized singular-series coefficient A=1",
            "remaining_premise": (
                "prove |R(N)|<=K*N/log(N) pointwise for every even N>H with "
                "an explicit K below the endpoint ceiling"
            ),
            "next_theorem": "ExplicitPointwiseBinaryGoldbachResidualConstant",
        },
        "machine_audit": {
            "finite_product_case_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The local singular-series factor is no longer an unknown constant. "
            "The pointwise binary Goldbach residual is the unresolved analytic core, "
            "so Goldbach remains open."
        ),
    }


def twin_raw_budget_transport_audit() -> dict[str, Any]:
    source = read_json(
        ROOT / "data/open-problem/ticket124-canonical-obstruction-limsup-criterion.json"
    )["canonical_obstruction_limsup_criterion"]["finite_obstruction_rows"][-1]
    holdout_payload = read_json(
        ROOT / "data/open-problem/ticket126-route-correction-audit.json"
    )["route_correction_audit"]["twin_prime"]
    holdout = holdout_payload["obstruction_row"]
    primary = holdout_payload["primary_result"]

    def raw_certificate_numerator(row: dict[str, Any]) -> float:
        return (
            float(row["independent_singleton_budget"])
            + float(row["boundary_budget"])
            - float(row["joint_lower_certificate"])
        )

    source_k = float(source["known_budget"])
    holdout_k = float(holdout["known_budget"])
    source_a = raw_certificate_numerator(source)
    holdout_a = raw_certificate_numerator(holdout)
    source_q = source_a / source_k
    holdout_q = holdout_a / holdout_k
    alpha = float(primary["alpha"])
    beta = float(primary["beta"])
    normalized_residual = holdout_q - alpha * source_q
    raw_threshold = (
        alpha * (holdout_k / source_k) * source_a + beta * holdout_k
    )
    raw_slack = raw_threshold - holdout_a
    paired_residual = float(holdout["paired_component_certificate"]) - (
        alpha * float(source["paired_component_certificate"])
    )
    boundary_residual = float(holdout["epsilon_boundary_to_known"]) - (
        alpha * float(source["epsilon_boundary_to_known"])
    )
    errors = [
        abs(source_q - float(source["canonical_obstruction_certificate"])),
        abs(holdout_q - float(holdout["canonical_obstruction_certificate"])),
        abs(normalized_residual - float(primary["certificate_recurrence_residual"])),
        abs(raw_slack / holdout_k - (beta - normalized_residual)),
        abs(paired_residual + boundary_residual - normalized_residual),
    ]
    return {
        "theorem_name": "RawBudgetTransportIffNormalizedAffineContraction",
        "proved_statement": (
            "For K_X,K_2X>0 and Q_X=A_X/K_X, the normalized inequality "
            "Q_2X<=alpha*Q_X+beta is equivalent to the raw transport inequality "
            "A_2X<=alpha*(K_2X/K_X)*A_X+beta*K_2X."
        ),
        "proof": (
            "Multiply the normalized inequality by positive K_2X and substitute "
            "Q_X=A_X/K_X. Division by K_2X proves the reverse implication."
        ),
        "sufficient_growth_corollary": (
            "If A_2X<=u*A_X+v*K_2X, K_2X>=gamma*K_X, K_X>0, "
            "and A_X,u>=0, gamma>0, "
            "then Q_2X<=(u/gamma)Q_X+v."
        ),
        "finite_16m_to_32m_audit": {
            "source_horizon": int(source["horizon"]),
            "holdout_horizon": int(holdout["horizon"]),
            "source_known_budget_K": source_k,
            "holdout_known_budget_K": holdout_k,
            "known_budget_growth_gamma": holdout_k / source_k,
            "source_adverse_numerator_A": source_a,
            "holdout_adverse_numerator_A": holdout_a,
            "adverse_numerator_growth_u": holdout_a / source_a,
            "source_Q": source_q,
            "holdout_Q": holdout_q,
            "alpha": alpha,
            "beta": beta,
            "normalized_recurrence_residual": normalized_residual,
            "raw_transport_threshold": raw_threshold,
            "raw_transport_slack": raw_slack,
            "paired_residual_contribution": paired_residual,
            "boundary_residual_contribution": boundary_residual,
        },
        "route_decision": {
            "retain": "coefficient-level raw numerator and denominator transport",
            "discard": "inferring a uniform tail recurrence from five finite endpoint transitions",
            "next_theorem": "UniformVaughanRawBudgetTransportAndInterpolation",
        },
        "machine_audit": {
            "maximum_identity_error": max(errors),
            "finite_transition_passes": normalized_residual <= beta + TOLERANCE,
            "conjecture_resolution_count": 0,
            "total_failure_count": int(max(errors) > TOLERANCE),
        },
        "proof_boundary": (
            "The theorem exactly exposes what a normalized recurrence means in "
            "raw Vaughan budgets. The finite audit proves no uniform coefficient "
            "transport, all-X interpolation, parity breakthrough, or Twin Prime theorem."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_dense_core_counterexample_audit(),
        "collatz": collatz_nontrivial_path_correction_audit(),
        "goldbach": goldbach_singular_series_lower_bound_audit(),
        "twin_prime": twin_raw_budget_transport_audit(),
    }
    failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureExceptionRepairAndEffectiveBridgeAudit",
        **sections,
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Primary Weil-autocorrelation criterion context; no RH positivity theorem is imported.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values",
                "url": "https://arxiv.org/abs/1909.03562",
                "role": "Primary almost-all boundary; the corrected target remains universal over n>1.",
            },
            {
                "citation": "Friedlander, Goldston, Iwaniec, and Suriajaya, Exceptional zeros and the Goldbach problem",
                "url": "https://doi.org/10.1016/j.jnt.2021.06.004",
                "role": "Primary source for the binary Goldbach singular-series normalization.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary sieve context; no exact-gap parity theorem is imported.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_intermediate_theorem_count": 4,
            "historical_logic_correction_count": 1,
            "closed_structural_premise_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET127 proves four exact intermediate statements, including one "
            "public correction, but proves or refutes none of RH, Collatz, "
            "Goldbach, or Twin Prime."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    boundary = "No conjecture proof and no certified conjecture counterexample."
    specs = [
        (
            "riemann",
            "RH-TICKET-127",
            "DenseCoreNegativeWitnessSemidecision",
            "IntervalCertifiedWeilCoreEvaluator",
            "Enumerate an independently proved dense Weil core with strict-sign interval certificates.",
        ),
        (
            "collatz",
            "CO-TICKET-127",
            "NontrivialEventuallyLowPathIffFiniteStoppingCounterexample",
            "UniformNontrivialEventuallyLowPathExclusion",
            "Synthesize ranks only after removing the permanent n=1 path.",
        ),
        (
            "goldbach",
            "GB-TICKET-127",
            "UniformBinaryGoldbachSingularSeriesLowerBound",
            "ExplicitPointwiseBinaryGoldbachResidualConstant",
            "Derive and interval-audit a uniform pointwise residual K below the exact endpoint ceiling.",
        ),
        (
            "twin-prime",
            "TP-TICKET-127",
            "RawBudgetTransportIffNormalizedAffineContraction",
            "UniformVaughanRawBudgetTransportAndInterpolation",
            "Prove raw coefficient transport uniformly and independently of further endpoint fitting.",
        ),
    ]
    return [
        {
            "problem_id": problem_id,
            "ticket_id": ticket_id,
            "status": "exact_intermediate_result_conjecture_open",
            "route": route,
            "bounded_result": {"audit_ref": problem_id.replace("-", "_")},
            "candidate_theorem": target,
            "next_experiment": next_experiment,
            "claim_boundary": boundary,
            "proof_boundary": audit[problem_id.replace("-", "_")]["proof_boundary"],
        }
        for problem_id, ticket_id, route, target, next_experiment in specs
    ]


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exception_repaired_effective_bridges_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "effective_bridge_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket127-exception-repair-effective-bridges.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-127-dense-core-semidecision.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-127-nontrivial-path-correction.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-127-singular-series-lower-bound.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-127-raw-budget-transport.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
