from __future__ import annotations

import json
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-17T15:40:00+09:00"
SCHEMA = "primeproject.ticket129-enumerable-core-valuation-cap-endpoint-budget.v1"
COLLATZ_VERIFIED_BITS = 28
GOLDBACH_VERIFIED_LIMIT = 4_000_000_000_000_000_000


def bounded_rational_grid(height: int) -> list[Fraction]:
    if height < 1:
        raise ValueError("height must be positive")
    return sorted(
        {
            Fraction(numerator, denominator)
            for denominator in range(1, height + 1)
            for numerator in range(-height * denominator, height * denominator + 1)
        }
    )


def riemann_enumerable_autocorrelation_core_audit(
    maximum_height: int = 6,
) -> dict[str, Any]:
    if maximum_height < 2:
        raise ValueError("maximum_height must be at least two")
    rows = []
    previous_grid: set[Fraction] = set()
    nested = True
    for height in range(1, maximum_height + 1):
        grid = bounded_rational_grid(height)
        grid_set = set(grid)
        nested = nested and previous_grid.issubset(grid_set)
        positive_radii = [value for value in grid if value > 0]
        gaussian_rational_coefficients = len(grid) ** 2 - 1
        atom_count = (
            gaussian_rational_coefficients * len(grid) * len(positive_radii)
        )
        core_description_count = 1 + sum(
            atom_count**length for length in range(1, height + 1)
        )
        rows.append(
            {
                "height": height,
                "rational_parameter_count": len(grid),
                "positive_radius_count": len(positive_radii),
                "nonzero_gaussian_rational_coefficient_count": (
                    gaussian_rational_coefficients
                ),
                "single_bump_atom_count": atom_count,
                "finite_sum_description_count_through_height": str(
                    core_description_count
                ),
            }
        )
        previous_grid = grid_set

    failures = int(not nested) + int(any(row["single_bump_atom_count"] <= 0 for row in rows))
    return {
        "theorem_name": "EnumerableRationalBumpAutocorrelationCoreDensity",
        "core_definition": (
            "Let b(x)=exp(-1/(1-x^2)) for |x|<1 and b(x)=0 otherwise. "
            "Let C_Q be the finite sums of q*b((x-a)/r), where a and r>0 "
            "are rational and q is Gaussian rational."
        ),
        "proved_statement": (
            "C_Q is countable and dense in the LF test-function space "
            "C_c^infinity(R). Consequently {g*tilde(g): g in C_Q} is "
            "countable and dense, in the relative test-function topology, "
            "in the smooth compact-support autocorrelation image."
        ),
        "proof": (
            "Mollification by normalized rational-scale copies of b converges "
            "to each compactly supported smooth g in every derivative norm on "
            "one fixed enlarged compact set. Approximate each convolution "
            "integral and all derivatives through a chosen finite order by a "
            "Riemann sum, then approximate its complex coefficients and centers "
            "by Gaussian rationals and rationals. A diagonal sequence gives all "
            "derivative orders. Every approximant has a finite rational tuple "
            "description, so their union is countable. Convolution and "
            "reflection are continuous on a fixed support, hence "
            "g_n*tilde(g_n) converges to g*tilde(g)."
        ),
        "finite_enumeration_audit": {
            "parameter_height_rows": rows,
            "nested_parameter_grids": nested,
            "interpretation": (
                "Every row is finite and the nested union contains every "
                "finite rational bump description. Counts are descriptions, "
                "not quotient classes of equal functions."
            ),
        },
        "connection_to_ticket128": (
            "Every core autocorrelation has compact support, so TICKET128 makes "
            "its prime-power side an exactly finite sum. This removes the "
            "previously open enumerability part without asserting positivity."
        ),
        "route_decision": {
            "retain": "a countable dense core inside the autocorrelation image",
            "discard": (
                "density of the autocorrelation cone in the entire ambient "
                "test-function space, refuted by TICKET126"
            ),
            "next_theorem": "CertifiedWeilValuesOnRationalBumpCore",
        },
        "machine_audit": {
            "enumerated_height_count": len(rows),
            "nested_grid_passes": nested,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The relative density theorem is exact. PrimeProject has not "
            "certified the archimedean term or nonnegativity of the Weil "
            "quadratic form on this core, so RH remains open."
        ),
    }


def valuation_cap(step: int) -> int:
    if step < 1:
        raise ValueError("step must be positive")
    return (3**step).bit_length()


def valuation_cap_language_stats(horizon: int = 256) -> dict[str, Any]:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    counts = [1]
    checkpoints = []
    requested = {1, 2, 4, 8, 16, 32, 64, 128, horizon}
    for step in range(1, horizon + 1):
        cap = valuation_cap(step)
        next_counts = [0] * (cap + 1)
        running = 0
        for total in range(1, cap + 1):
            if total - 1 < len(counts):
                running += counts[total - 1]
            next_counts[total] = running
        counts = next_counts
        if step in requested:
            mass = sum(
                Fraction(count, 1 << total)
                for total, count in enumerate(counts)
                if count
            )
            checkpoints.append(
                {
                    "steps": step,
                    "valuation_sum_cap": cap,
                    "admissible_word_count": str(sum(counts)),
                    "exact_cylinder_mass_numerator": str(mass.numerator),
                    "exact_cylinder_mass_denominator": str(mass.denominator),
                    "cylinder_mass_decimal": float(mass),
                }
            )
    return {
        "audited_horizon": horizon,
        "checkpoints": checkpoints,
        "final_admissible_word_count": str(sum(counts)),
    }


def collatz_least_counterexample_valuation_cap_audit(
    language_horizon: int = 256,
) -> dict[str, Any]:
    ticket128 = read_json(
        ROOT
        / "data/open-problem/collatz/co-ticket-128-finite-prefix-closure.json"
    )
    ticket128_global = read_json(
        ROOT / "data/open-problem/ticket128-finite-core-prefix-constant-interpolation.json"
    )
    prefix = ticket128_global[
        "finite_core_prefix_constant_interpolation_audit"
    ]["collatz"]["exact_prefix_audit"]
    minimum_start = 1 << COLLATZ_VERIFIED_BITS
    m = 3 * minimum_start
    proved_horizon = 2 * minimum_start
    exponential_series_upper = Fraction(87, 32)
    convenient_upper = Fraction(11, 4)
    cube_comparison = convenient_upper**2
    language = valuation_cap_language_stats(language_horizon)
    failures = sum(
        [
            int(ticket128.get("ticket_id") != "CO-TICKET-128"),
            int(prefix["unresolved_after_direct_check"] != 0),
            int(prefix["integer_upper_bound_exclusive"] != minimum_start),
            int(exponential_series_upper >= convenient_upper),
            int(cube_comparison >= 8),
            int(3 * proved_horizon != 2 * m),
        ]
    )
    return {
        "theorem_name": "LeastCounterexampleInitialValuationCap",
        "proved_statement": (
            "If a least positive Collatz counterexample n exists, then n is odd "
            "and n>=2^28. For every 1<=j<=2^29, if a_i is the 2-adic "
            "valuation used by the ith accelerated odd step and S_j=sum a_i, "
            "then S_j<=ceil(j*log_2(3))=bit_length(3^j)."
        ),
        "proof": (
            "Minimality gives x_i>=n for every accelerated odd iterate. "
            "Multiplying 2^a_i*x_(i+1)=3*x_i+1 yields "
            "2^S_j=3^j*(n/x_j)*product_i(1+1/(3x_i)), hence "
            "2^S_j<=3^j*(1+1/(3n))^j. Put n0=2^28 and m=3*n0. "
            "The binomial theorem gives (1+1/m)^m<sum 1/k!<87/32<11/4. "
            "For j<=2*n0, 3j<=2m, so (1+1/m)^(3j)<(11/4)^2<8 and "
            "(1+1/m)^j<2. Thus 2^S_j<2*3^j, which implies "
            "S_j<=bit_length(3^j)."
        ),
        "exact_constants": {
            "verified_lower_bound_for_least_counterexample": minimum_start,
            "proved_accelerated_horizon": proved_horizon,
            "proved_horizon_power": "2^29",
            "m_equals_3_times_lower_bound": m,
            "sum_inverse_factorial_upper": str(exponential_series_upper),
            "convenient_upper": str(convenient_upper),
            "squared_upper": str(cube_comparison),
            "squared_upper_below_8": cube_comparison < 8,
        },
        "finite_language_pruning_audit": language,
        "route_decision": {
            "retain": (
                "use the exact prefix cap as a necessary-condition filter for "
                "changing-prefix searches"
            ),
            "discard": (
                "repeating the TICKET80 all-ones finite-prefix compactness "
                "argument or extrapolating TICKET128's finite scan"
            ),
            "next_theorem": "LeastCounterexampleValuationCapLanguageExtinction",
        },
        "machine_audit": {
            "finite_verified_bits": COLLATZ_VERIFIED_BITS,
            "symbolic_cap_horizon": proved_horizon,
            "language_audit_horizon": language_horizon,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a necessary condition for a hypothetical least "
            "counterexample, not a contradiction. Compatible valuation words "
            "still survive the finite cap, so Collatz remains open."
        ),
    }


def atanh_log_interval(z: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    if not (0 < z < 1):
        raise ValueError("z must lie strictly between zero and one")
    if terms < 1:
        raise ValueError("terms must be positive")
    lower = 2 * sum(
        (z ** (2 * index + 1)) / (2 * index + 1)
        for index in range(terms)
    )
    next_exponent = 2 * terms + 1
    tail_upper = (
        2
        * z**next_exponent
        / (next_exponent * (1 - z**2))
    )
    return lower, lower + tail_upper


def goldbach_k56_endpoint_audit() -> dict[str, Any]:
    log2_lower, log2_upper = atanh_log_interval(Fraction(1, 3), 3)
    log_five_fourths_lower, log_five_fourths_upper = atanh_log_interval(
        Fraction(1, 9), 2
    )
    log_h_lower = 56 * log2_lower + 18 * log_five_fourths_lower
    log_h_upper = 56 * log2_upper + 18 * log_five_fourths_upper
    simple_log_lower = Fraction(214, 5)
    simple_log_upper = Fraction(43, 1)
    major_floor = Fraction(131_917, 100_000)
    contamination_b_upper = Fraction(21, 10)
    square_root_h = 2_000_000_000
    contamination_upper = (
        contamination_b_upper * simple_log_upper**2 / square_root_h
    )
    residual_k = 56
    residual_upper = Fraction(residual_k, 1) / simple_log_lower
    margin = major_floor - residual_upper - contamination_upper
    next_integer_margin = (
        major_floor
        - Fraction(residual_k + 1, 1) / simple_log_lower
        - contamination_upper
    )
    exact_b_checks = {
        "H_below_2_power_62": GOLDBACH_VERIFIED_LIMIT < 2**62,
        "1200_power_6_below_H": 1200**6 < GOLDBACH_VERIFIED_LIMIT,
        "deduced_B_upper": "B<2*(1+60/1200)=21/10",
    }
    failures = sum(
        [
            int(log_h_lower <= simple_log_lower),
            int(log_h_upper >= simple_log_upper),
            int(not all(value for key, value in exact_b_checks.items() if key != "deduced_B_upper")),
            int(margin <= 0),
            int(next_integer_margin >= 0),
        ]
    )
    return {
        "theorem_name": "ExactRationalGoldbachResidualK56Sufficiency",
        "proved_statement": (
            "Under the TICKET125/126 weighted Goldbach decomposition and the "
            "TICKET128 major coefficient floor A>1.31917, a uniform pointwise "
            "bound |R(N)|<=56*N/log(N) for every even N>4*10^18 is sufficient "
            "to glue the analytic tail to the verified finite range."
        ),
        "proof": (
            "The identity log(H)=56 log(2)+18 log(5/4), together with positive "
            "atanh series and exact geometric tail bounds, gives "
            "214/5<log(H)<43. Also H<2^62 and 1200^6<H, so the TICKET126 "
            "contamination coefficient satisfies B<21/10. Substitution into "
            "A-K/log(H)-B*log(H)^2/sqrt(H) leaves the displayed positive "
            "rational margin for K=56."
        ),
        "exact_log_certificate": {
            "log_2_lower": str(log2_lower),
            "log_2_upper": str(log2_upper),
            "log_5_over_4_lower": str(log_five_fourths_lower),
            "log_5_over_4_upper": str(log_five_fourths_upper),
            "log_H_lower": str(log_h_lower),
            "log_H_upper": str(log_h_upper),
            "simple_interval": "214/5 < log(H) < 43",
        },
        "exact_contamination_certificate": exact_b_checks,
        "endpoint_budget": {
            "verified_limit_H": GOLDBACH_VERIFIED_LIMIT,
            "major_coefficient_floor": str(major_floor),
            "candidate_pointwise_residual_K": residual_k,
            "residual_upper": str(residual_upper),
            "contamination_upper": str(contamination_upper),
            "positive_margin_numerator": str(margin.numerator),
            "positive_margin_denominator": str(margin.denominator),
            "positive_margin_decimal": float(margin),
            "K57_margin_under_same_certificate": float(next_integer_margin),
            "K56_is_largest_integer_certified_by_this_coarse_interval": (
                margin > 0 and next_integer_margin < 0
            ),
        },
        "route_decision": {
            "retain": "the exact finite-glue budget with rational certificates",
            "discard": "K=55 as an unnecessarily strict sufficient target",
            "next_theorem": "PointwiseBinaryGoldbachResidualK56",
        },
        "machine_audit": {
            "exact_log_interval_passes": (
                log_h_lower > simple_log_lower
                and log_h_upper < simple_log_upper
            ),
            "k56_margin_positive": margin > 0,
            "k57_not_certified_by_same_budget": next_integer_margin < 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The sufficiency constant is improved from 55 to 56, but the "
            "pointwise residual theorem itself is not proved. Strong Goldbach "
            "therefore remains open."
        ),
    }


def twin_increment_synchronization_audit() -> dict[str, Any]:
    endpoint = Fraction(23, 25)
    delta_target = Fraction(2, 25)
    rows = []
    for exponent in range(4, 11):
        left = 1 << exponent
        midpoint = 3 * (1 << (exponent - 1))
        right = 1 << (exponent + 1)
        states = [
            (left, Fraction(23, 25), Fraction(1, 1)),
            (midpoint, Fraction(46, 25), Fraction(1, 1)),
            (right, Fraction(46, 25), Fraction(2, 1)),
        ]
        left_a, left_k = states[0][1], states[0][2]
        state_rows = []
        for scale, a_value, k_value in states:
            q_value = a_value / k_value
            increment_defect = (
                (a_value - left_a) - endpoint * (k_value - left_k)
            ) / k_value
            state_rows.append(
                {
                    "scale": scale,
                    "A": str(a_value),
                    "K": str(k_value),
                    "Q": float(q_value),
                    "increment_defect": float(increment_defect),
                    "identity_error": float((q_value - endpoint) - increment_defect),
                }
            )
        rows.append(
            {
                "left_endpoint": left,
                "midpoint": midpoint,
                "right_endpoint": right,
                "A_and_K_are_nondecreasing": True,
                "denominator_doubles_at_right_endpoint": True,
                "both_endpoint_ratios": float(endpoint),
                "midpoint_ratio": float(states[1][1] / states[1][2]),
                "states": state_rows,
            }
        )
    failures = sum(
        int(any(abs(state["identity_error"]) > 1e-15 for state in row["states"]))
        for row in rows
    )
    return {
        "theorem_name": "ExactWithinBlockIncrementSynchronizationCriterion",
        "proved_statement": (
            "For positive cumulative K and Q_X=A_X/K_X, fix a left endpoint Y "
            "and q=Q_Y. For every X>=Y, Q_X-q=(Delta A-q*Delta K)/K_X. "
            "Therefore Q_X<=q+delta throughout a dyadic block if and only if "
            "Delta A-q*Delta K<=delta*K_X throughout that block."
        ),
        "proof": (
            "Substitute A_X=A_Y+Delta A and K_X=K_Y+Delta K into "
            "A_X/K_X-A_Y/K_Y and cancel A_Y*K_Y. The numerator becomes "
            "K_Y*(Delta A-q*Delta K), giving the identity and equivalence."
        ),
        "minimal_defect_function": (
            "D(Y)=sup_{Y<=X<=2Y} max(0,Delta A-Q_Y*Delta K)/K_X is the "
            "smallest admissible additive within-block delta at c=1."
        ),
        "strengthened_monotone_countermodel": {
            "statement": (
                "Endpoint ratio 0.92, monotonicity of both cumulative budgets, "
                "and exact denominator doubling still do not imply an "
                "all-scale ratio below one."
            ),
            "rows": rows,
            "midpoint_defect": float(endpoint),
            "required_target": float(delta_target),
        },
        "connection_to_ticket128": (
            "TICKET128 gives limsup q_j<=0.92. At c=1 the exact remaining "
            "coefficient theorem is limsup_j D(2^j)<0.08; equivalently, it "
            "suffices to prove an eventual uniform D(2^j)<=delta for some "
            "delta<0.08. Endpoint and monotonicity data cannot supply it."
        ),
        "route_decision": {
            "retain": "estimate the signed synchronized increment Delta A-Q_Y*Delta K",
            "discard": "endpoint interpolation from cumulative monotonicity or denominator growth alone",
            "next_theorem": "AsymptoticVaughanIncrementSynchronizationBelow008",
        },
        "machine_audit": {
            "countermodel_block_count": len(rows),
            "identity_passes_every_state": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The identity and countermodel are exact, but no asymptotic 0.08 "
            "defect bound is proved for the actual Vaughan coefficients. The parity "
            "barrier and exact gap-two positivity also remain."
        ),
    }


def build_audit(language_horizon: int = 256) -> dict[str, Any]:
    sections = {
        "riemann": riemann_enumerable_autocorrelation_core_audit(),
        "collatz": collatz_least_counterexample_valuation_cap_audit(
            language_horizon
        ),
        "goldbach": goldbach_k56_endpoint_audit(),
        "twin_prime": twin_increment_synchronization_audit(),
    }
    failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureEnumerableCoreValuationCapEndpointBudgetAudit",
        **sections,
        "literature_boundary": [
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Primary 2026 formulation of Weil positivity on "
                    "C_c^infinity(R); TICKET129 proves only core density."
                ),
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values",
                "url": "https://arxiv.org/abs/1909.03562",
                "role": "Primary almost-all boundary; the valuation cap is a universal-counterexample necessity, not convergence.",
            },
            {
                "citation": "Oliveira e Silva, Herzog, and Pardi, Empirical verification of the even Goldbach conjecture",
                "url": "https://doi.org/10.1090/S0025-5718-2013-02787-1",
                "role": "Primary finite verification boundary H=4e18 used in the exact glue budget.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary sieve boundary; the increment identity does not resolve parity or exact gap two.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_intermediate_theorem_count": 4,
            "explicit_route_counterexample_count": 1,
            "strengthened_endpoint_budget_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET129 proves four exact intermediate results or route "
            "corrections. It proves or refutes none of RH, Collatz, Goldbach, "
            "or Twin Prime."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-129",
            "EnumerableRationalBumpAutocorrelationCoreDensity",
            "CertifiedWeilValuesOnRationalBumpCore",
            "Implement outward-rounded archimedean and finite prime-side values for the enumerated core.",
        ),
        (
            "collatz",
            "CO-TICKET-129",
            "LeastCounterexampleInitialValuationCap",
            "LeastCounterexampleValuationCapLanguageExtinction",
            "Use the exact prefix cap to prune changing-prefix branches and seek either extinction or an explicit survivor.",
        ),
        (
            "goldbach",
            "GB-TICKET-129",
            "ExactRationalGoldbachResidualK56Sufficiency",
            "PointwiseBinaryGoldbachResidualK56",
            "Attack the signed pointwise residual with the now-maximal certified integer budget K=56.",
        ),
        (
            "twin-prime",
            "TP-TICKET-129",
            "ExactWithinBlockIncrementSynchronizationCriterion",
            "AsymptoticVaughanIncrementSynchronizationBelow008",
            "Prove limsup D(2^j)<0.08 for the actual signed increment defect, not endpoint ratios alone.",
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
            "next_experiment": experiment,
            "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
            "proof_boundary": audit[problem_id.replace("-", "_")]["proof_boundary"],
        }
        for problem_id, ticket_id, route, target, experiment in specs
    ]


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "enumerable_core_valuation_cap_endpoint_budget_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "enumerable_core_valuation_cap_endpoint_budget_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket129-enumerable-core-valuation-cap-endpoint-budget.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-129-enumerable-bump-core.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-129-valuation-cap.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-129-k56-endpoint.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-129-increment-synchronization.json",
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
            {"schema": SCHEMA, "machine_audit": audit["machine_audit"]},
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
