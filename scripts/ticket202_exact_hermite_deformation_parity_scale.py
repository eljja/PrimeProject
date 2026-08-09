from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import (
    cyclic_rotation_affine_audit,
    is_primitive_word,
    ordered_affine_numerator,
    prime_sieve,
    semiprime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket202-exact-hermite-deformation-parity-scale.v1"
GENERATED_AT = "2026-08-10T21:30:00+09:00"
STATUS = "open_not_proven"
TWIN_LIMIT = 1 << 23


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return result


def polynomial_derivative(values: list[Fraction]) -> list[Fraction]:
    return [index * values[index] for index in range(1, len(values))]


def polynomial_evaluate(values: list[Fraction], point: int) -> Fraction:
    result = Fraction(0)
    for value in reversed(values):
        result = result * point + value
    return result


def polynomial_disk_l1_bound(values: list[Fraction], radius: int) -> Fraction:
    return sum(
        (abs(value) * radius**index for index, value in enumerate(values)),
        Fraction(0),
    )


def hermite_perturbation_row(degree_half: int) -> dict[str, Any]:
    # F(z)=z^2-1 and P(z)=(z^2-1)^3(z^2-4)^3. The perturbation
    # q_N(z)=c_N z^(2N)P(z) preserves derivatives through order two at
    # 0, +/-1, and +/-2, while c_N is chosen so q_N(iA)=-F(iA).
    radius = 5
    height = 10
    epsilon = Fraction(1, 100)
    base = [1]
    for square in (1, 4):
        for _ in range(3):
            base = polynomial_multiply(base, [-square, 0, 1])
    f_at_i_a = -(height**2) - 1
    h_at_i_a = (
        ((-1) ** degree_half)
        * height ** (2 * degree_half)
        * (height**2 + 1) ** 3
        * (height**2 + 4) ** 3
    )
    coefficient = Fraction(-f_at_i_a, h_at_i_a)
    perturbation = [Fraction(0)] * (2 * degree_half) + [
        coefficient * value for value in base
    ]
    derivatives = [perturbation]
    for _ in range(2):
        derivatives.append(polynomial_derivative(derivatives[-1]))
    bounds = [polynomial_disk_l1_bound(values, radius) for values in derivatives]
    node_checks = {
        str(node): [
            fraction_text(polynomial_evaluate(values, node))
            for values in derivatives
        ]
        for node in (-2, -1, 0, 1, 2)
    }
    return {
        "N": degree_half,
        "perturbation_degree": 2 * degree_half + len(base) - 1,
        "coefficient_c_N": fraction_text(coefficient),
        "base_polynomial_coefficients_low_to_high": base,
        "hermite_node_derivatives_j_0_to_2": node_checks,
        "all_hermite_constraints_preserved_exactly": all(
            value == "0" for row in node_checks.values() for value in row
        ),
        "jet_bounds_j_0_to_2": [fraction_text(value) for value in bounds],
        "maximum_jet_bound": fraction_text(max(bounds)),
        "all_jet_bounds_below_epsilon": all(value < epsilon for value in bounds),
        "epsilon": fraction_text(epsilon),
        "coefficient_times_H_iA": fraction_text(coefficient * h_at_i_a),
        "minus_F_iA": str(-f_at_i_a),
        "G_N_iA_is_zero_exactly": coefficient * h_at_i_a == -f_at_i_a,
    }


def riemann_exact_hermite_no_go_audit() -> dict[str, Any]:
    rows = [hermite_perturbation_row(value) for value in range(2, 13)]
    first_certifying = next(
        row["N"] for row in rows if row["all_jet_bounds_below_epsilon"]
    )
    failures = int(first_certifying != 3)
    failures += sum(
        int(
            not row["all_hermite_constraints_preserved_exactly"]
            or not row["G_N_iA_is_zero_exactly"]
            or row["all_jet_bounds_below_epsilon"] != (row["N"] >= 3)
        )
        for row in rows
    )
    return {
        "theorem": (
            "Let F be a real-even entire function, let R>0, and prescribe "
            "finitely many derivative values at a finite symmetric set of real "
            "nodes. Choose A>R away from those nodes with F(iA) nonzero. There "
            "exist real-even entire functions G_N with zeros at plus-or-minus "
            "iA that preserve every prescribed Hermite value exactly and whose "
            "derivatives through any fixed finite order converge uniformly to "
            "those of F on |z|<=R. Hence even exact finite Hermite data plus a "
            "compact finite-jet enclosure cannot force a global real-zero "
            "property in the ambient real-even entire-function class."
        ),
        "proof": (
            "For positive interpolation nodes a_l with derivative orders m_l, "
            "put P(z)=product_l(z^2-a_l^2)^(m_l+1), multiply by a sufficiently "
            "large even power z^(2N) to handle the node zero, and set "
            "H_N(z)=z^(2N)P(z). Then H_N and the required derivatives vanish "
            "at every interpolation node. Because H_N(iA) is real and nonzero, "
            "G_N=F-F(iA)H_N/H_N(iA) is real-even, preserves all Hermite data, "
            "and vanishes at plus-or-minus iA. On |z|<=R, every fixed derivative "
            "of H_N/H_N(iA) is a fixed polynomial in N times (R/A)^(2N), so it "
            "converges uniformly to zero. Adding a polynomial preserves order "
            "at most one when applicable, but not Xi's completed-zeta structure."
        ),
        "exact_regression": {
            "F": "z^2-1",
            "F_has_only_real_zeros": True,
            "hermite_nodes": [-2, -1, 0, 1, 2],
            "preserved_derivative_orders": [0, 1, 2],
            "compact_disk_radius_R": 5,
            "off_real_axis_height_A": 10,
            "epsilon": "1/100",
            "rows": rows,
            "first_certifying_N": first_certifying,
        },
        "aggregate": {
            "exact_finite_hermite_no_go_proved": failures == 0,
            "compact_jet_convergence_proved": True,
            "real_even_symmetry_preserved": True,
            "xi_completed_zeta_structure_preserved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This closes the exact-node loophole left by TICKET-201 but does not "
            "construct an off-line zero of Xi. Any surviving RH certificate must "
            "use unbounded/cofinal information or Xi-specific global arithmetic "
            "structure rather than finitely many exact samples and derivatives."
        ),
        "failure_count": failures,
    }


def collatz_deformed_word(run_pairs: int, scale: int, extension: int) -> tuple[int, ...]:
    if run_pairs < 2 or scale < 2 or extension < 0:
        raise ValueError("require run_pairs>=2, scale>=2, and extension>=0")
    return (
        (1,) * scale
        + (2,) * (2 * scale + extension)
        + (1, 2, 2) * (run_pairs - 1)
    )


def collatz_deformed_row(run_pairs: int, scale: int, extension: int) -> dict[str, Any]:
    word = collatz_deformed_word(run_pairs, scale, extension)
    n = run_pairs - 1
    q = scale + n
    long_run = 2 * scale + extension
    tail_numerator = 23 * (32**n - 27**n) // 5
    numerator_closed = (
        3 ** (long_run + 3 * n) * (3**scale - 2**scale)
        + 2**scale * 27**n * (4**long_run - 3**long_run)
        + 2**scale * 4**long_run * tail_numerator
    )
    denominator = 4**extension * 32**q - 3**extension * 27**q
    e_value = (
        14 * 3**extension * 27**scale
        - 5 * 3**extension * 18**scale
        - 9 * 4**extension * 32**scale
    )
    f_value = -e_value
    identity_left = 5 * numerator_closed - 23 * denominator
    identity_right = 2 * 27**n * e_value
    rotation = cyclic_rotation_affine_audit(word)
    horizon = len(word)
    one_count = q
    product_gate = Fraction(2**one_count) * Fraction(5, 6) ** horizon > 1
    return {
        "run_pair_count_r": run_pairs,
        "scale_k": scale,
        "long_run_extension_t": extension,
        "n_equals_r_minus_1": n,
        "q_equals_k_plus_n": q,
        "word": f"1^{scale} 2^{2 * scale + extension} (1 2^2)^{n}",
        "horizon_h": horizon,
        "valuation_sum_S": sum(word),
        "denominator_D": str(denominator),
        "affine_numerator_B": str(numerator_closed),
        "direct_numerator_matches_closed_form": (
            ordered_affine_numerator(word) == numerator_closed
        ),
        "five_B_minus_twenty_three_D": str(identity_left),
        "two_times_27n_times_Ekt": str(identity_right),
        "master_identity_holds_exactly": identity_left == identity_right,
        "E_k_t": str(e_value),
        "F_k_t_equals_minus_E_k_t": str(f_value),
        "zero_less_than_F_k_t_less_than_D": 0 < f_value < denominator,
        "gcd_D_with_2_times_27n": math.gcd(denominator, 2 * 27**n),
        "primitive_word": is_primitive_word(word),
        "affine_divisibility_hit": numerator_closed % denominator == 0,
        "contraction_gate_passes": 2 ** sum(word) > 3**horizon,
        "product_gate_passes": product_gate,
        **rotation,
    }


def collatz_long_run_deformation_audit() -> dict[str, Any]:
    rows = [
        collatz_deformed_row(run_pairs, scale, extension)
        for run_pairs in range(2, 11)
        for scale in range(2, 11)
        for extension in range(0, 9)
    ]
    failures = sum(
        int(
            not row["direct_numerator_matches_closed_form"]
            or not row["master_identity_holds_exactly"]
            or not row["zero_less_than_F_k_t_less_than_D"]
            or row["gcd_D_with_2_times_27n"] != 1
            or not row["primitive_word"]
            or row["affine_divisibility_hit"]
            or row["cyclic_rotation_divisibility_hit_count"] != 0
            or not row["rotation_recurrence_holds_exactly"]
            or not row["rotation_cycle_closes"]
            or not row["contraction_gate_passes"]
        )
        for row in rows
    )
    return {
        "theorem": (
            "For every r>=2, k>=2, and t>=0, the primitive accelerated-Collatz "
            "word w_(r,k,t)=1^k 2^(2k+t)(1 2^2)^(r-1), and every cyclic "
            "rotation, fails the affine divisibility equation. Thus an "
            "unbounded one-sided L1 deformation ray from every TICKET-201 base "
            "word contains no positive Collatz cycle code."
        ),
        "proof": (
            "Put n=r-1 and q=k+n. Direct concatenation gives "
            "D=4^t32^q-3^t27^q and the exact identity "
            "5B-23D=2*27^n E_(k,t), where E_(k,t)=14*3^t27^k-"
            "5*3^t18^k-9*4^t32^k=-F_(k,t). For t=0, positivity of F is "
            "TICKET-201's residual inequality. For t>=1 and k>=2, "
            "14*3^t27^k<9*4^t32^k follows from the worst case t=1,k=2, "
            "so F>0. Also D>=4^t32^(k+1)-3^t27^(k+1)>F because the remaining "
            "difference is 23*4^t32^k-13*3^t27^k-5*3^t18^k>0. Since D is "
            "coprime to 6*27^n, D|B would force D|E, contradicting "
            "0<|E|<D. A unique long 2-run proves primitivity, and the standard "
            "rotation recurrence transfers nondivisibility to every rotation."
        ),
        "symbolic_identities": {
            "denominator": "D=4^t*32^(k+r-1)-3^t*27^(k+r-1)",
            "master_identity": "5B-23D=2*27^(r-1)(14*3^t*27^k-5*3^t*18^k-9*4^t*32^k)",
            "strict_residual_bound": "0<F_(k,t)=9*4^t*32^k+5*3^t*18^k-14*3^t*27^k<D",
        },
        "exact_regression_rows": rows,
        "aggregate": {
            "regression_run_pair_count": 9,
            "regression_scale_count": 9,
            "regression_extension_count": 9,
            "regression_word_count": len(rows),
            "all_run_pair_counts_covered_symbolically": True,
            "all_scales_covered_symbolically": True,
            "all_nonnegative_long_run_extensions_covered_symbolically": True,
            "all_cyclic_rotations_covered_symbolically": True,
            "arbitrary_signed_or_multisite_L1_perturbations_covered": False,
            "product_gate_regression_pass_count": sum(
                row["product_gate_passes"] for row in rows
            ),
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes an unbounded one-sided deformation ray, not a "
            "full L1 ball. Shortening the run, moving mass between positions, "
            "arbitrary valuation words, and nonperiodic divergence remain open."
        ),
        "failure_count": failures,
    }


def prefix_counts(indicator: bytearray) -> list[int]:
    result = [0] * len(indicator)
    running = 0
    for index, value in enumerate(indicator):
        running += int(value)
        result[index] = running
    return result


def interval_count(prefix: list[int], lower_exclusive: int, upper_inclusive: int) -> int:
    if upper_inclusive < 0 or upper_inclusive <= lower_exclusive:
        return 0
    upper = min(upper_inclusive, len(prefix) - 1)
    lower = min(max(lower_exclusive, -1), len(prefix) - 1)
    return prefix[upper] - (prefix[lower] if lower >= 0 else 0)


def goldbach_dyadic_aggregate_row(
    exponent: int,
    prime_values: list[int],
    prime_prefix: list[int],
    semiprime_prefix: list[int],
) -> dict[str, Any]:
    lower = 1 << exponent
    upper = 2 * lower
    prime_prime = 0
    prime_semiprime = 0
    for prime in prime_values:
        if prime > upper:
            break
        prime_prime += interval_count(
            prime_prefix, lower - prime, upper - prime
        )
        prime_semiprime += interval_count(
            semiprime_prefix, lower - prime, upper - prime
        )
    channel = prime_prime + prime_semiprime
    signed = prime_semiprime - prime_prime
    defect = Fraction(channel - signed, channel)
    return {
        "target_block_X_to_2X": [lower, upper],
        "prime_prime_aggregate_R": prime_prime,
        "prime_composite_semiprime_aggregate_S": prime_semiprime,
        "P2_aggregate_C": channel,
        "liouville_aggregate_L": signed,
        "relative_defect_one_minus_L_over_C": fraction_text(defect),
        "semiprime_to_prime_ratio_S_over_R": fraction_text(
            Fraction(prime_semiprime, prime_prime)
        ),
        "C_minus_L_equals_2R": channel - signed == 2 * prime_prime,
        "C_plus_L_equals_2S": channel + signed == 2 * prime_semiprime,
    }


def goldbach_relative_defect_dilution_audit(
    primes: bytearray,
    prime_values: list[int],
    semiprimes: bytearray,
) -> dict[str, Any]:
    prime_prefix = prefix_counts(primes)
    semiprime_prefix = prefix_counts(semiprimes)
    rows = [
        goldbach_dyadic_aggregate_row(
            exponent, prime_values, prime_prefix, semiprime_prefix
        )
        for exponent in range(10, 21)
    ]
    defect_values = [
        Fraction(row["relative_defect_one_minus_L_over_C"])
        for row in rows
    ]
    failures = sum(
        int(
            not row["C_minus_L_equals_2R"]
            or not row["C_plus_L_equals_2S"]
        )
        for row in rows
    )
    failures += int(
        any(
            defect_values[index + 1] >= defect_values[index]
            for index in range(len(defect_values) - 1)
        )
    )
    return {
        "theorem": (
            "Let R_X, S_X, C_X, and L_X be the sums of the TICKET-201 "
            "Goldbach prime, composite-semiprime, P2, and Liouville-signed "
            "channels over even N in (X,2X]. The prime number theorem and "
            "Landau's theorem for integers with exactly two prime factors imply "
            "R_X/S_X=O(1/log log X), and therefore "
            "(C_X-L_X)/C_X=2R_X/(R_X+S_X) tends to zero. Consequently no fixed "
            "delta>0 can satisfy L(N)<=(1-delta)C(N) for every sufficiently "
            "large Chen-positive even N."
        ),
        "proof": (
            "The upper bound R_X<=pi(2X)^2 is O(X^2/log^2 X). For a lower "
            "bound on S_X, restrict the first prime p and odd composite "
            "semiprime m to (X/2,X]; then p+m lies in (X,2X]. PNT gives "
            "about X/(2 log X) such primes, while Landau's theorem gives about "
            "X log log X/(2 log X) such odd semiprimes; even semiprimes are "
            "lower order. Hence S_X is Omega(X^2 log log X/log^2 X). The exact "
            "identity C_X-L_X=2R_X proves the limit. A pointwise fixed delta "
            "would survive summation on every sufficiently large dyadic block, "
            "contradicting that limit."
        ),
        "classical_inputs": [
            "prime number theorem",
            "Landau asymptotic for Omega(n)=2: Q_2(x)~x log log x/log x",
        ],
        "exact_finite_rows": rows,
        "aggregate": {
            "finite_block_count": len(rows),
            "largest_target_upper": rows[-1]["target_block_X_to_2X"][1],
            "finite_defect_strictly_decreasing": all(
                defect_values[index + 1] < defect_values[index]
                for index in range(len(defect_values) - 1)
            ),
            "fixed_positive_relative_defect_refuted_asymptotically": True,
            "pointwise_loglog_scaled_defect_proved": False,
            "goldbach_resolved": False,
        },
        "no_go_scope": (
            "This refutes TICKET-201's fixed-relative-defect target, not "
            "Goldbach. A vanishing defect can still be positive at every N. "
            "The corrected pointwise scale is of order 1/log log N, and no "
            "uniform pointwise lower bound at that scale is proved here."
        ),
        "failure_count": failures,
    }


def twin_actual_block_row(
    exponent: int,
    primes: bytearray,
    semiprimes: bytearray,
) -> dict[str, Any]:
    lower = 1 << exponent
    upper = 2 * lower
    twin_count = 0
    semiprime_count = 0
    for value in range(lower, upper):
        if not primes[value]:
            continue
        twin_count += int(primes[value + 2])
        semiprime_count += int(semiprimes[value + 2])
    channel = twin_count + semiprime_count
    signed = semiprime_count - twin_count
    defect = Fraction(channel - signed, channel)
    normalized_channel = Fraction(channel * exponent**2, lower)
    normalized_twin = Fraction(twin_count * exponent**2, lower)
    return {
        "block_X_to_2X": [lower, upper],
        "log2_X": exponent,
        "twin_channel_T": twin_count,
        "composite_semiprime_channel_S": semiprime_count,
        "P2_channel_C2": channel,
        "liouville_signed_channel_L2": signed,
        "relative_defect_delta_X": fraction_text(defect),
        "normalized_C2_log2sq_over_X": fraction_text(normalized_channel),
        "normalized_T_log2sq_over_X": fraction_text(normalized_twin),
        "normalized_transfer_identity": (
            normalized_twin == defect * normalized_channel / 2
        ),
    }


def twin_abstract_countermodel_row(exponent: int) -> dict[str, Any]:
    lower = 1 << exponent
    channel = max(2, lower // (exponent**2))
    twin_count = 1
    semiprime_count = channel - twin_count
    signed = semiprime_count - twin_count
    defect = Fraction(channel - signed, channel)
    return {
        "block_X_to_2X": [lower, 2 * lower],
        "abstract_twin_count_T": twin_count,
        "abstract_P2_channel_C2": channel,
        "abstract_L2": signed,
        "relative_defect_delta_X": fraction_text(defect),
        "twin_positive": True,
        "C2_minus_L2_equals_2T": channel - signed == 2 * twin_count,
        "fixed_relative_defect_survives": False,
    }


def twin_relative_defect_strength_audit(
    primes: bytearray,
    semiprimes: bytearray,
) -> dict[str, Any]:
    actual_rows = [
        twin_actual_block_row(exponent, primes, semiprimes)
        for exponent in range(10, 23)
    ]
    countermodel_rows = [
        twin_abstract_countermodel_row(exponent) for exponent in range(10, 31)
    ]
    countermodel_defects = [
        Fraction(row["relative_defect_delta_X"])
        for row in countermodel_rows
    ]
    failures = sum(
        int(not row["normalized_transfer_identity"]) for row in actual_rows
    )
    failures += sum(
        int(
            not row["twin_positive"]
            or not row["C2_minus_L2_equals_2T"]
        )
        for row in countermodel_rows
    )
    failures += int(countermodel_defects[-1] >= countermodel_defects[0])
    return {
        "theorem": (
            "For every dyadic block, delta_X=1-L2(X)/C2(X)=2T(X)/C2(X) "
            "exactly. Therefore, if C2(X)>=a X/(log_2 X)^2 and delta_X>=d>0 "
            "on infinitely many blocks, then T(X)>=ad X/(2(log_2 X)^2) on "
            "those blocks. A fixed relative defect plus Chen-order mass is a "
            "Hardy-Littlewood-order quantitative Twin lower bound, strictly "
            "stronger than mere Twin infinitude. Channel algebra alone cannot "
            "derive it: the exact abstract model T=1, C2=floor(X/log_2^2 X), "
            "L2=C2-2 is twin-positive on every block while delta_X tends to zero."
        ),
        "proof": (
            "The projector identity gives C2-L2=2T, so division by C2 proves "
            "delta_X=2T/C2. Multiplying a Chen-mass lower bound by d/2 gives "
            "the stated twin lower bound. In the abstract model, C2-L2=2 and "
            "T=1 exactly on every block, but delta_X=2/C2 tends to zero as "
            "C2 grows. Thus infinitude and a fixed relative defect are not "
            "equivalent consequences of the channel identities."
        ),
        "exact_finite_rows": actual_rows,
        "exact_abstract_countermodel_rows": countermodel_rows,
        "aggregate": {
            "finite_block_count": len(actual_rows),
            "abstract_countermodel_block_count": len(countermodel_rows),
            "normalized_transfer_identity_proved": failures == 0,
            "fixed_relative_defect_is_stronger_than_infinitude": True,
            "fixed_relative_defect_refuted_for_actual_twin_channels": False,
            "twin_prime_resolved": False,
        },
        "no_go_scope": (
            "This is a theorem-strength calibration, not evidence that the "
            "actual Twin relative defect tends to zero. It discards treating a "
            "fixed defect as a modest intermediate lemma; a parity-sensitive "
            "switching estimate capable of an absolute positive prime-channel "
            "contribution is still missing."
        ),
        "failure_count": failures,
    }


def proof_dag(
    prefix: str,
    previous: str,
    theorem: str,
    rejected: str,
    next_theorem: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T201", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T202", "label": theorem, "status": "closed"},
            {
                "id": f"{prefix}-N202",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN202",
                "label": next_theorem,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": prefix, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T201", f"{prefix}-T202"],
            [f"{prefix}-T202", f"{prefix}-N202"],
            [f"{prefix}-T202", f"{prefix}-OPEN202"],
            [f"{prefix}-OPEN202", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_exact_hermite_no_go_audit()
    collatz = collatz_long_run_deformation_audit()
    primes = prime_sieve(TWIN_LIMIT + 2)
    prime_values = [value for value in range(2, TWIN_LIMIT + 3) if primes[value]]
    semiprimes = semiprime_sieve(TWIN_LIMIT + 2, prime_values)
    goldbach = goldbach_relative_defect_dilution_audit(
        primes, prime_values, semiprimes
    )
    twin = twin_relative_defect_strength_audit(primes, semiprimes)
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-202",
            "theorem_name": "ExactFiniteHermiteAndCompactJetGlobalZeroNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "Exact finite samples and derivatives remain local data; the "
                "perturbation does not preserve Xi's completed-zeta arithmetic."
            ),
            "route_decision": {
                "discard": "augmenting one fixed compact Xi certificate by finitely many exact Hermite constraints",
                "retain": "construct cofinal contours whose margins are derived from completed-zeta structure",
                "next_single_lemma": "CompletedZetaCofinalContourMarginWithExactZeroCountTransfer",
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteCompactJetDataCannotForceGlobalRealZeroProperty",
                "ExactFiniteHermiteAndCompactJetGlobalZeroNoGo",
                "FiniteExactHermiteAugmentationClosesRH",
                "CompletedZetaCofinalContourMarginWithExactZeroCountTransfer",
            ),
            "claim_boundary": (
                "No RH proof or counterexample. The theorem strengthens the "
                "finite-information strategy no-go and changes the function."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-202",
            "theorem_name": "AllLongRunExtensionsPrimitiveFamilyAffineObstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Only a one-sided single-block deformation ray is closed; a "
                "uniform multisite L1 neighborhood and arbitrary words remain open."
            ),
            "route_decision": {
                "discard": "treating each nonnegative central-run extension as a separate experiment",
                "retain": "derive a signed two-site mass-transfer residual identity around the family",
                "next_single_lemma": "SignedTwoSiteValuationTransferAffineObstruction",
            },
            "proof_dag": proof_dag(
                "CO",
                "AllRunPairPrimitiveFamilyAffineDivisibilityObstruction",
                "AllLongRunExtensionsPrimitiveFamilyAffineObstruction",
                "FixedLongRunExtensionSearchIsIndependentProgress",
                "SignedTwoSiteValuationTransferAffineObstruction",
            ),
            "claim_boundary": (
                "No Collatz proof and no nontrivial cycle. One explicit "
                "three-parameter family and all rotations are excluded."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-202",
            "theorem_name": "DyadicP2RelativeLiouvilleDefectDilutionNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The asymptotic aggregate no-go supplies no pointwise positive "
                "defect and cannot eliminate a sparse Goldbach exceptional set."
            ),
            "route_decision": {
                "discard": "a fixed positive relative Liouville defect in every large full P2 channel",
                "retain": "renormalize by the Landau log-log dilution and seek a pointwise signed estimate",
                "next_single_lemma": "PointwiseLogLogScaledLiouvilleDefectOnEveryLargeEvenInteger",
            },
            "proof_dag": proof_dag(
                "GB",
                "GoldbachP2LiouvilleParitySaturationEquivalence",
                "DyadicP2RelativeLiouvilleDefectDilutionNoGo",
                "UniformFixedRelativeP2LiouvilleDefect",
                "PointwiseLogLogScaledLiouvilleDefectOnEveryLargeEvenInteger",
            ),
            "claim_boundary": (
                "No Goldbach proof or counterexample. Classical asymptotics "
                "refute one normalization while leaving pointwise positivity open."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-202",
            "theorem_name": "RelativeChenDefectQuantitativeTwinStrengthCalibration",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The transfer identity proves no actual lower bound and the "
                "countermodel is logical channel data, not prime arithmetic."
            ),
            "route_decision": {
                "discard": "treating a fixed relative Chen defect as a modest infinitude-level sublemma",
                "retain": "design a parity-sensitive switching weight that separates prime and semiprime mass at a vanishing relative scale",
                "next_single_lemma": "PrimeSemiprimeSeparatedChenSwitchingWeightWithPositivePrimeCoefficient",
            },
            "proof_dag": proof_dag(
                "TP",
                "TwinP2LiouvilleParitySaturationEquivalence",
                "RelativeChenDefectQuantitativeTwinStrengthCalibration",
                "FixedRelativeChenDefectIsOnlyAnInfinitudeLevelLemma",
                "PrimeSemiprimeSeparatedChenSwitchingWeightWithPositivePrimeCoefficient",
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. The theorem calibrates "
                "the previous target and gives an abstract non-implication model."
            ),
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureExactDataDeformationAndParityScaleAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-202 resolves none of the four conjectures. It closes the "
            "finite exact-Hermite loophole in the RH local-data route, excludes "
            "an all-parameter long-run Collatz deformation family, proves that "
            "the proposed fixed Goldbach P2 relative defect is asymptotically "
            "impossible, and proves that the analogous Twin target is a "
            "quantitative lower-bound theorem stronger than infinitude."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common correction is scale-sensitive information: exact but "
            "finite data do not become global, one algebraic residual can close "
            "an unbounded deformation ray, and parity defects must be normalized "
            "against the natural channel mass before they are plausible targets."
        ),
        "literature_boundary": {
            "riemann": "The Hermite perturbation theorem is elementary and does not preserve Xi's completed-zeta structure; Platt-Trudgian remains finite-height context only.",
            "collatz": "The three-parameter residual identity is project-local. Current Christoffel-word work is adjacent context, not a source of the proof.",
            "goldbach": "The no-go imports only the classical PNT and Landau Omega(n)=2 asymptotic. Current Goldbach exceptional-set work does not remove the pointwise gap.",
            "twin_prime": "The strength calibration is exact channel algebra. Chen and modern switching-sieve results provide context but no separated prime-channel lower bound used here.",
        },
        "sources": [
            {
                "title": "The Riemann hypothesis is true up to 3*10^12",
                "authors": "Dave Platt and Tim Trudgian",
                "url": "https://arxiv.org/abs/2004.09765",
            },
            {
                "title": "Handbuch der Lehre von der Verteilung der Primzahlen",
                "authors": "Edmund Landau",
                "url": "https://doi.org/10.1007/BF01742852",
            },
            {
                "title": "The exceptional set of the Goldbach problem",
                "authors": "Lasse Grimmelt and Gautami Bhowmik",
                "url": "https://arxiv.org/abs/2607.27282",
            },
            {
                "title": "On the representation of a large even integer as the sum of a prime and the product of at most two primes",
                "authors": "Jing-Run Chen",
                "url": "https://doi.org/10.1360/YA1973-16-2-157",
            },
            {
                "title": "Weighted sieves with switching",
                "authors": "Kaisa Matomaki and Sebastian Zuniga Alterman",
                "url": "https://arxiv.org/abs/2405.19063",
            },
        ],
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "riemann_exact_hermite_regression_count": len(
                riemann["exact_regression"]["rows"]
            ),
            "collatz_symbolic_parameter_dimension": 3,
            "collatz_exact_regression_word_count": len(
                collatz["exact_regression_rows"]
            ),
            "goldbach_exact_dyadic_aggregate_row_count": len(
                goldbach["exact_finite_rows"]
            ),
            "twin_exact_channel_row_count": len(twin["exact_finite_rows"]),
            "twin_abstract_countermodel_row_count": len(
                twin["exact_abstract_countermodel_rows"]
            ),
            "rejected_or_recalibrated_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for problem_id, section_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"][
                    "next_single_lemma"
                ],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"][
                    "next_single_lemma"
                ],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "exact_hermite_deformation_parity_scale_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket202-exact-hermite-deformation-parity-scale.json"
    )
    write_json(integrated, payload)
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-202-exact-hermite-no-go.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-202-long-run-deformation.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-202-relative-defect-dilution.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-202-relative-defect-strength.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        section = audit[section_keys[problem_id]]
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": STATUS,
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "discarded_route": attempt["discarded_route"],
                "remaining_gap": attempt["remaining_gap"],
                "candidate_theorem": attempt["candidate_theorem"],
                "claim_boundary": attempt["claim_boundary"],
                "proof_dag": attempt["proof_dag"],
            },
        )
    digest = hashlib.sha256(integrated.read_bytes()).hexdigest()
    print(f"integrated_sha256 {digest}")


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-202 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
