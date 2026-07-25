from __future__ import annotations

import json
from fractions import Fraction
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket144_schur_rank_equivalence_variation_adverse_walsh import (
    exact_ldl_pivots,
    twin_adverse_row,
    walsh_coefficients_from_counts,
)


GENERATED_AT = "2026-07-26T18:00:00+09:00"
SCHEMA = "primeproject.ticket146-toeplitz-polynomial-phase-frechet.v1"
STATUS = "exact_reductions_and_route_no_go_theorems_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T146-REJECTED"
    closed_id = f"{problem_code}-T146-CLOSED"
    open_id = f"{problem_code}-T146-OPEN"
    return {
        "nodes": [
            {
                "id": rejected_id,
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": closed_id,
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": open_id,
                "label": next_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [rejected_id, closed_id],
            [closed_id, open_id],
        ],
    }


def real_toeplitz(
    moments: Sequence[Fraction],
    size: int | None = None,
) -> list[list[Fraction]]:
    dimension = len(moments) if size is None else size
    if dimension < 1 or len(moments) < dimension:
        raise ValueError("one real moment per Toeplitz diagonal required")
    return [
        [moments[abs(row - column)] for column in range(dimension)]
        for row in range(dimension)
    ]


def levinson_real(
    moments: Sequence[Fraction],
) -> dict[str, object]:
    if not moments or moments[0] == 0:
        raise ValueError("nonzero zeroth moment required")
    error = moments[0]
    coefficients: list[Fraction] = []
    errors = [error]
    reflections: list[Fraction] = []
    rows: list[dict[str, object]] = []

    for order in range(1, len(moments)):
        numerator = moments[order] + sum(
            coefficients[index - 1] * moments[order - index]
            for index in range(1, order)
        )
        reflection = -numerator / error
        previous = coefficients
        coefficients = [
            previous[index - 1]
            + reflection * previous[order - index - 1]
            for index in range(1, order)
        ] + [reflection]
        next_error = error * (1 - reflection * reflection)
        reflections.append(reflection)
        errors.append(next_error)
        rows.append(
            {
                "order": order,
                "reflection_coefficient": fraction_payload(reflection),
                "previous_error": fraction_payload(error),
                "next_error": fraction_payload(next_error),
                "recurrence_factor": fraction_payload(
                    1 - reflection * reflection
                ),
                "prediction_coefficients": [
                    fraction_payload(value) for value in coefficients
                ],
            }
        )
        error = next_error
        if error == 0 and order + 1 < len(moments):
            raise ValueError("zero Levinson error before final order")

    return {
        "reflection_coefficients": [
            fraction_payload(value) for value in reflections
        ],
        "prediction_errors": [
            fraction_payload(value) for value in errors
        ],
        "rows": rows,
    }


def riemann_toeplitz_audit() -> dict[str, object]:
    sample_moments = [
        Fraction(2),
        Fraction(1),
        Fraction(3, 4),
        Fraction(1, 3),
        Fraction(1, 5),
        Fraction(1, 8),
        Fraction(1, 13),
    ]
    sample = levinson_real(sample_moments)
    sample_pivots = [
        exact_ldl_pivots(real_toeplitz(sample_moments, size))[-1]
        for size in range(1, len(sample_moments) + 1)
    ]
    sample_errors = [
        Fraction(row["exact"])
        for row in sample["prediction_errors"]
    ]
    sample_checks = {
        "levinson_errors_equal_exact_schur_pivots": (
            sample_errors == sample_pivots
        ),
        "sample_sections_are_positive": all(
            value > 0 for value in sample_pivots
        ),
        "sample_has_nontrivial_reflections": sum(
            Fraction(row["exact"]) != 0
            for row in sample["reflection_coefficients"]
        )
        >= 5,
    }

    fixed_lag_rows = []
    failures = sum(not value for value in sample_checks.values())
    for lag in range(1, 13):
        moments = [Fraction(1)] + [Fraction(0)] * lag + [Fraction(2)]
        recurrence = levinson_real(moments)
        pivots = [
            exact_ldl_pivots(real_toeplitz(moments, size))[-1]
            for size in range(1, len(moments) + 1)
        ]
        reflections = [
            Fraction(row["exact"])
            for row in recurrence["reflection_coefficients"]
        ]
        errors = [
            Fraction(row["exact"])
            for row in recurrence["prediction_errors"]
        ]
        checks = {
            "first_lag_reflections_are_zero": (
                reflections[:lag] == [Fraction(0)] * lag
            ),
            "new_reflection_is_minus_two": (
                reflections[lag] == Fraction(-2)
            ),
            "prefix_is_identity": (
                pivots[: lag + 1] == [Fraction(1)] * (lag + 1)
            ),
            "first_unseen_section_is_indefinite": pivots[-1] == -3,
            "levinson_matches_schur": errors == pivots,
        }
        failures += sum(not value for value in checks.values())
        fixed_lag_rows.append(
            {
                "visible_lag_count": lag,
                "first_unseen_lag": lag + 1,
                "unseen_moment": 2,
                "last_reflection_coefficient": -2,
                "last_schur_pivot": -3,
                "checks": checks,
            }
        )

    return {
        "exact_shift_core_identity": (
            "Assume W(tilde(phi))=conjugate(W(phi)). For "
            "Q(f,g)=W(f*tilde(g)) and log-translations tau_h, "
            "Q(tau_(jh)f,tau_(kh)f)=r_(j-k), where "
            "r_m=W(tau_(mh)(f*tilde(f))). The Gram family is Hermitian "
            "Toeplitz."
        ),
        "levinson_reduction": (
            "For every nonzero preceding prediction error E_(m-1), the "
            "exact Toeplitz Schur pivot satisfies "
            "E_m=E_(m-1)(1-|kappa_m|^2). If E_0>0, all nested sections "
            "are positive exactly when every reflection coefficient obeys "
            "|kappa_m|<1."
        ),
        "finite_lag_no_go": (
            "For every L, moments r_0=1, r_1=...=r_L=0, and "
            "r_(L+1)=2 agree with the identity core through lag L, but "
            "the next reflection coefficient is -2 and the next Schur "
            "pivot is -3. In the unrestricted Hermitian Toeplitz moment "
            "class, no fixed-lag rule certifies all sections without "
            "additional structural constraints."
        ),
        "sample_moments": [fraction_payload(value) for value in sample_moments],
        "sample_recurrence": sample,
        "sample_exact_schur_pivots": [
            fraction_payload(value) for value in sample_pivots
        ],
        "sample_checks": sample_checks,
        "fixed_lag_rows": fixed_lag_rows,
        "failure_count": failures,
    }


def polynomial_value(
    coefficients: Sequence[int],
    value: int,
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def first_polynomial_counteredge(
    modulus: int,
    coefficients: Sequence[int],
    search_limit: int = 100_000,
) -> dict[str, object]:
    if modulus < 1 or not coefficients:
        raise ValueError("positive modulus and nonempty polynomial required")
    degree = len(coefficients) - 1
    leading = coefficients[-1]
    if degree > 0 and leading <= 0:
        raise ValueError("audit profiles must have positive leading term")

    leading_difference = (
        0
        if degree == 0
        else leading
        * modulus**degree
        * (6**degree - 4**degree)
    )
    found = None
    for k in range(1, search_limit + 1):
        start = 4 * modulus * k - 1
        successor = 6 * modulus * k - 1
        difference = polynomial_value(
            coefficients, successor
        ) - polynomial_value(coefficients, start)
        if difference >= 0:
            found = {
                "k": k,
                "start": start,
                "successor": successor,
                "rank_difference": difference,
            }
            break
    if found is None:
        raise RuntimeError("finite audit did not reach eventual counteredge")

    checks = {
        "same_residue_mod_M": (
            found["start"] % modulus == found["successor"] % modulus
        ),
        "residue_is_minus_one": found["start"] % modulus == (-1) % modulus,
        "accelerated_valuation_is_one": (
            (3 * found["start"] + 1) % 2 == 0
            and (3 * found["start"] + 1) % 4 != 0
        ),
        "accelerated_successor_matches": (
            (3 * found["start"] + 1) // 2 == found["successor"]
        ),
        "rank_does_not_decrease": found["rank_difference"] >= 0,
        "difference_leading_term_is_nonnegative": leading_difference >= 0,
    }
    return {
        "modulus": modulus,
        "degree": degree,
        "coefficients_ascending": list(coefficients),
        "difference_leading_coefficient_in_k": leading_difference,
        "first_audited_counteredge": found,
        "checks": checks,
    }


def collatz_polynomial_rank_audit() -> dict[str, object]:
    profiles = [
        ("constant", [7]),
        ("linear", [-100, 1]),
        ("quadratic_delayed", [17, -1000, 1]),
        ("cubic", [-2, 7, -50, 1]),
        ("quartic", [3, -1, 2, -5, 1]),
        ("quintic", [-11, 4, -3, 2, -1, 1]),
    ]
    rows = []
    for modulus in [1, 2, 5, 16, 31]:
        for name, coefficients in profiles:
            row = first_polynomial_counteredge(modulus, coefficients)
            row["profile"] = name
            rows.append(row)
    failures = sum(
        not value
        for row in rows
        for value in row["checks"].values()
    )
    return {
        "theorem": (
            "Fix M. Let R(n)=P_r(n) on each odd residue r mod M, with "
            "real polynomials P_r, and suppose R is bounded below on "
            "positive odd integers. Then R(T(n))<R(n) cannot hold on "
            "every accelerated Collatz edge."
        ),
        "proof": (
            "Use n=4Mk-1 and T(n)=6Mk-1 in the same residue -1 mod M. "
            "A polynomial P_(-1) bounded below along the positive ray is "
            "constant or has positive leading coefficient. In the first "
            "case the rank difference is zero; in the second, "
            "P(6Mk-1)-P(4Mk-1) has positive leading coefficient "
            "a_d M^d(6^d-4^d), so it is positive for all sufficiently "
            "large k."
        ),
        "scope": (
            "The theorem excludes every fixed finite-modulus "
            "piecewise-polynomial lower-bounded one-step rank. It does "
            "not exclude oscillatory, history-dependent, unbounded-state, "
            "or adaptive block-descent certificates."
        ),
        "profile_count": len(profiles),
        "row_count": len(rows),
        "rows": rows,
        "failure_count": failures,
    }


def cyclic_convolution(
    left: Sequence[int],
    right: Sequence[int],
) -> list[int]:
    if len(left) != len(right) or not left:
        raise ValueError("equal nonempty cyclic vectors required")
    size = len(left)
    return [
        sum(left[index] * right[(target - index) % size] for index in range(size))
        for target in range(size)
    ]


def cyclic_autocorrelation(values: Sequence[int]) -> list[int]:
    if not values:
        raise ValueError("nonempty cyclic vector required")
    size = len(values)
    return [
        sum(
            values[index] * values[(index + lag) % size]
            for index in range(size)
        )
        for lag in range(size)
    ]


def cyclic_translate(values: Sequence[int], shift: int) -> list[int]:
    size = len(values)
    translated = [0] * size
    for index, value in enumerate(values):
        translated[(index + shift) % size] = value
    return translated


def goldbach_phase_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for modulus in [11, 13, 17, 19, 23, 29]:
        base = [0] * modulus
        base[0] = 1
        base[1] = 1
        shifted = cyclic_translate(base, 2)
        base_convolution = cyclic_convolution(base, base)
        shifted_convolution = cyclic_convolution(shifted, shifted)
        base_autocorrelation = cyclic_autocorrelation(base)
        shifted_autocorrelation = cyclic_autocorrelation(shifted)
        checks = {
            "means_match": sum(base) == sum(shifted),
            "all_power_spectrum_data_match_via_autocorrelation": (
                base_autocorrelation == shifted_autocorrelation
            ),
            "base_endpoint_is_one": base_convolution[0] == 1,
            "shifted_endpoint_is_zero": shifted_convolution[0] == 0,
            "translation_convolution_identity": all(
                shifted_convolution[target]
                == base_convolution[(target - 4) % modulus]
                for target in range(modulus)
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "modulus": modulus,
                "base_support": [0, 1],
                "translated_support": [2, 3],
                "endpoint": 0,
                "base_endpoint_convolution": base_convolution[0],
                "translated_endpoint_convolution": shifted_convolution[0],
                "cyclic_autocorrelation": base_autocorrelation,
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "On Z/qZ, translation g(x)=f(x-a) preserves the mean, every "
            "cyclic autocorrelation, and hence every Fourier magnitude "
            "|f_hat(k)|. Nevertheless "
            "(g*g)(t)=(f*f)(t-2a), so a fixed endpoint convolution is "
            "not determined by the power spectrum."
        ),
        "circle_method_identity": (
            "(f*f)(N)=q^(-1) sum_k f_hat(k)^2 exp(2*pi*i*k*N/q). "
            "The square retains twice the Fourier phase; replacing it by "
            "|f_hat(k)|^2 changes the mathematical object."
        ),
        "exact_counterexample": (
            "For q>=11, f=1_{0,1}, a=2, and endpoint N=0, the original "
            "convolution equals 1 while the translated convolution equals "
            "0, although all magnitude-only Fourier data agree."
        ),
        "scope": (
            "These vectors are not the von Mangoldt function and are not "
            "Goldbach counterexamples. The theorem refutes only a "
            "magnitude-only or power-spectrum derivation of signed "
            "pointwise scale cancellation. Coarse absolute upper bounds "
            "from magnitudes remain valid but discard the phase saving "
            "needed for a tight K=56 budget."
        ),
        "rows": rows,
        "failure_count": failures,
    }


def frechet_row(counts: Sequence[int]) -> dict[str, object]:
    a00, a10, a01, a11 = walsh_coefficients_from_counts(counts)
    first_negative = (a00 - a10) // 2
    second_negative = (a00 - a01) // 2
    lower = max(0, first_negative + second_negative - a00)
    upper = min(first_negative, second_negative)
    reconstructed = (a00 - a10 - a01 + a11) // 4
    checks = {
        "marginal_first_is_integral": (a00 - a10) % 2 == 0,
        "marginal_second_is_integral": (a00 - a01) % 2 == 0,
        "walsh_reconstruction_is_integral": (
            (a00 - a10 - a01 + a11) % 4 == 0
        ),
        "walsh_reconstructs_twin_class": reconstructed == counts[3],
        "frechet_lower_bound_holds": counts[3] >= lower,
        "frechet_upper_bound_holds": counts[3] <= upper,
    }
    return {
        "category_counts": list(counts),
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "first_negative_marginal": first_negative,
        "second_negative_marginal": second_negative,
        "frechet_lower": lower,
        "frechet_upper": upper,
        "reconstructed_twin_class": reconstructed,
        "checks": checks,
    }


def twin_frechet_audit() -> dict[str, object]:
    same_marginal_rows = [
        frechet_row([0, 50, 50, 0]),
        frechet_row([25, 25, 25, 25]),
    ]
    finite_rows = []
    for scale in [1_000, 10_000, 100_000, 1_000_000]:
        source = twin_adverse_row(scale)
        row = frechet_row(source["category_counts"])
        row["X"] = scale
        row["one_sided_zero_budget_checks"] = {
            "A10_nonpositive": row["A10"] <= 0,
            "A01_nonpositive": row["A01"] <= 0,
            "A11_nonnegative": row["A11"] >= 0,
            "certified_quarter_mass": (
                row["category_counts"][3] * 4 >= row["A00"]
            ),
        }
        finite_rows.append(row)

    checks = {
        "counterpair_has_same_marginal_Walsh_data": all(
            same_marginal_rows[0][key] == same_marginal_rows[1][key]
            for key in ["A00", "A10", "A01"]
        ),
        "counterpair_has_different_twin_mass": (
            same_marginal_rows[0]["category_counts"][3]
            != same_marginal_rows[1]["category_counts"][3]
        ),
        "zero_twin_row_has_perfect_marginal_cancellation": (
            same_marginal_rows[0]["A10"] == 0
            and same_marginal_rows[0]["A01"] == 0
        ),
        "all_rows_pass_frechet_contract": all(
            all(row["checks"].values())
            for row in same_marginal_rows + finite_rows
        ),
        "all_finite_rows_pass_zero_budget_sign_pattern": all(
            all(row["one_sided_zero_budget_checks"].values())
            for row in finite_rows
        ),
    }
    failures = sum(not value for value in checks.values())
    return {
        "frechet_theorem": (
            "Let N=A00 and let u=(N-A10)/2 and v=(N-A01)/2 be the "
            "two negative Liouville marginals. Then every joint table "
            "satisfies max(0,u+v-N)<=N_(-- )<=min(u,v), and both bounds "
            "are sharp."
        ),
        "marginal_no_go": (
            "The tables (0,50,50,0) and (25,25,25,25) have identical "
            "(A00,A10,A01)=(100,0,0), but twin masses 0 and 25. Even "
            "perfect one-variable Liouville cancellation does not control "
            "the joint prime class."
        ),
        "one_sided_sufficient_reduction": (
            "If A10<=epsilon_1 A00, A01<=epsilon_2 A00, and "
            "A11>=-gamma A00 with epsilon_1+epsilon_2+gamma<1, then "
            "N_(-- ) >= "
            "(1-epsilon_1-epsilon_2-gamma)A00/4 > 0. Helpful signs need "
            "no absolute-value control."
        ),
        "same_marginal_counterpair": same_marginal_rows,
        "finite_cubic_rough_rows": finite_rows,
        "checks": checks,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_toeplitz_audit()
    collatz = collatz_polynomial_rank_audit()
    goldbach = goldbach_phase_audit()
    twin_prime = twin_frechet_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )

    riemann_next = "ExplicitWeilShiftCoreReflectionCoefficientUnitDiskBound"
    collatz_next = "SymbolicCylinderAdaptiveBlockDescentBeyondPolynomialRanks"
    goldbach_next = "PhaseResolvedBinaryGoldbachScaleEnvelopeSummableK56"
    twin_next = "CubicRoughOneSidedJointLiouvilleTypeIIMargin"

    return {
        "theorem_name": "FourConjectureToeplitzPolynomialPhaseFrechetAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET146 proves four exact reductions or route no-go theorems. "
            "It supplies no conjecture proof or counterexample. The RH "
            "translation core lacks an all-core unit-disk estimate, the "
            "Collatz theorem excludes only finite-modulus polynomial "
            "one-step ranks, the Goldbach counterexample is not arithmetic, "
            "and the Twin result does not prove any eventual Type II bound."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-146",
            "theorem_name": (
                "ShiftGeneratedWeilToeplitzLevinsonReductionAndFiniteLagNoGo"
            ),
            "declared_proposition": (
                "An involution-compatible shift-generated convolution core "
                "is Hermitian Toeplitz and its Schur pivots satisfy the "
                "exact Levinson reflection recurrence; in the unrestricted "
                "Hermitian Toeplitz moment class, no fixed number of "
                "moments certifies every future pivot."
            ),
            "mathematical_argument": riemann[
                "exact_shift_core_identity"
            ]
            + " "
            + riemann["levinson_reduction"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No actual all-order Weil reflection coefficient is bounded "
                "here. The adversarial finite-lag moments are not asserted "
                "to arise from the Weil functional, and density of one "
                "lattice shift orbit in the full Weil test core is not "
                "asserted."
            ),
            "route_decision": {
                "discard": (
                    "a fixed-lag normalized moment recurrence as an "
                    "all-section positivity certificate without extra "
                    "Weil-specific structure"
                ),
                "retain": (
                    "compute the actual shift moments from the Weil explicit "
                    "formula and prove every resulting reflection "
                    "coefficient lies in the open unit disk"
                ),
                "next_theorem": riemann_next,
            },
            "proof_dag": proof_dag(
                "RH",
                "FixedLagNormalizedWeilMomentSignRecurrence",
                (
                    "ShiftGeneratedWeilToeplitzLevinsonReductionAnd"
                    "FiniteLagNoGo"
                ),
                riemann_next,
            ),
            "claim_boundary": (
                "No RH proof or zeta-zero counterexample. Exact Toeplitz "
                "reduction plus an unrestricted-Toeplitz finite-lag "
                "proof-route no-go only."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-146",
            "theorem_name": (
                "FiniteModulusPiecewisePolynomialCollatzRankNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["scope"],
            "route_decision": {
                "discard": (
                    "every lower-bounded one-step rank polynomial on each "
                    "class of a fixed finite residue partition"
                ),
                "retain": (
                    "adaptive multi-step descent on symbolic cylinders with "
                    "a lift-closed proof independent of stopping time"
                ),
                "next_theorem": collatz_next,
            },
            "proof_dag": proof_dag(
                "CO",
                "FiniteModulusPiecewisePolynomialOneStepRank",
                "FiniteModulusPiecewisePolynomialCollatzRankNoGo",
                collatz_next,
            ),
            "claim_boundary": (
                "No Collatz proof or orbit counterexample. A broad "
                "nonoscillatory one-step rank grammar is excluded."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-146",
            "theorem_name": (
                "PowerSpectrumInsufficiencyForPointwiseBinaryConvolution"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach[
                "circle_method_identity"
            ],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["scope"],
            "route_decision": {
                "discard": (
                    "a signed pointwise K56 envelope inferred only from "
                    "Fourier magnitudes, energy, or power spectrum"
                ),
                "retain": (
                    "major/minor-arc scale bounds that preserve the squared "
                    "Fourier phase and the target endpoint"
                ),
                "next_theorem": goldbach_next,
            },
            "proof_dag": proof_dag(
                "GB",
                "MagnitudeOnlyBinaryGoldbachScaleEnvelopeK56",
                (
                    "PowerSpectrumInsufficiencyForPointwiseBinary"
                    "Convolution"
                ),
                goldbach_next,
            ),
            "claim_boundary": (
                "No Goldbach proof or Goldbach counterexample. The exact "
                "cyclic vectors refute a magnitude-only inference, not an "
                "estimate for the von Mangoldt residual."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-146",
            "theorem_name": (
                "FrechetMarginalLiouvilleNoGoAndOneSidedWalshReduction"
            ),
            "declared_proposition": twin_prime["frechet_theorem"],
            "mathematical_argument": (
                twin_prime["marginal_no_go"]
                + " "
                + twin_prime["one_sided_sufficient_reduction"]
            ),
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The exact tables are abstract rough-support parity tables. "
                "The four finite arithmetic rows do not prove eventual "
                "Walsh signs or a scale-uniform Type II margin."
            ),
            "route_decision": {
                "discard": (
                    "separate marginal Liouville cancellation as a route "
                    "to positive twin mass"
                ),
                "retain": (
                    "one-sided arithmetic bounds for A10, A01, and the "
                    "joint A11 term with a total budget below one"
                ),
                "next_theorem": twin_next,
            },
            "proof_dag": proof_dag(
                "TP",
                "IndependentMarginalLiouvilleCancellationImpliesTwins",
                (
                    "FrechetMarginalLiouvilleNoGoAndOneSidedWalsh"
                    "Reduction"
                ),
                twin_next,
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. Exact Frechet "
                "bounds, a marginal no-go pair, and a sufficient one-sided "
                "budget reduction only."
            ),
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    attempts = []
    for problem_id in ["riemann", "collatz", "goldbach", "twin-prime"]:
        key = problem_id.replace("-", "_")
        section = audit[key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "attempt": section["declared_proposition"],
                "bounded_result": {
                    "audit_ref": (
                        "toeplitz_polynomial_phase_frechet_audit."
                        f"{key}"
                    )
                },
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"][
                    "next_theorem"
                ],
                "next_experiment": section["route_decision"]["retain"],
                "claim_boundary": section["claim_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "toeplitz_polynomial_phase_frechet_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket146-toeplitz-polynomial-phase-frechet.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-146-toeplitz-levinson.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-146-piecewise-polynomial-rank-no-go.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-146-power-spectrum-phase-no-go.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-146-frechet-marginal-no-go.json"
        ),
    }
    for attempt in attempts:
        problem_id = str(attempt["problem_id"])
        key = problem_id.replace("-", "_")
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                **attempt,
                "result": audit[key],
            },
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
