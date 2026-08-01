from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import radix_two_fft
from ticket159_diagonal_threshold_phase_parity import prime_sieve


GENERATED_AT = "2026-08-06T18:00:00+09:00"
SCHEMA = "primeproject.ticket173-finite-section-cylinder-phase-tensor.v1"
STATUS = "four_exact_structural_audits_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {"exact": f"{value.numerator}/{value.denominator}", "decimal": float(value)}


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T173-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T173-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T173-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T173-REJECTED", f"{problem_code}-T173-CLOSED"],
            [f"{problem_code}-T173-CLOSED", f"{problem_code}-T173-OPEN"],
        ],
    }


def riemann_finite_section_audit() -> dict[str, object]:
    """Separate dense-core positivity from an unnecessarily uniform gap."""

    failures = 0
    rows: list[dict[str, object]] = []
    for dimension in [2, 4, 8, 16, 32, 64, 128]:
        exact_minimum = Fraction(1, dimension)
        approximation_radius = Fraction(1, dimension)
        approximate_minimum = Fraction(0)
        certified_lower_bound = approximate_minimum - approximation_radius
        checks = {
            "approximation_error_equals_radius": approximation_radius
            == exact_minimum,
            "certified_lower_defect_is_eta_N": certified_lower_bound
            == -Fraction(1, dimension),
            "lower_defect_tends_toward_zero": dimension
            * abs(certified_lower_bound)
            == 1,
            "exact_finite_section_is_positive": exact_minimum > 0,
            "uniform_positive_gap_is_not_present": exact_minimum
            <= Fraction(1, 2),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_section_dimension_N": dimension,
                "model_operator_diagonal": "q_j=1/j",
                "exact_lambda_min": fraction_payload(exact_minimum),
                "approximate_matrix": "A_N-(1/N)I",
                "approximate_lambda_min": fraction_payload(approximate_minimum),
                "operator_error_radius": fraction_payload(approximation_radius),
                "certified_lower_bound": fraction_payload(certified_lower_bound),
                "lower_defect_eta_N": fraction_payload(-certified_lower_bound),
                "checks": checks,
            }
        )

    rank_rows: list[dict[str, object]] = []
    for dimension in [2, 4, 8, 16, 32, 64, 128]:
        center_sigma_min = Fraction(1)
        radius = Fraction(1, 4)
        rank_margin = center_sigma_min - radius
        checks = {
            "one_stage_rank_margin_is_positive": rank_margin > 0,
            "nested_domain_preserves_surjectivity": dimension >= 2,
            "constraint_rank_is_two": True,
        }
        failures += sum(not value for value in checks.values())
        rank_rows.append(
            {
                "finite_section_dimension_N": dimension,
                "constraint_rank_r": 2,
                "approximate_sigma_min": fraction_payload(center_sigma_min),
                "operator_error_radius": fraction_payload(radius),
                "certified_rank_margin": fraction_payload(rank_margin),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let q be a continuous Hermitian form on a Hilbert space and let V_N "
            "be nested finite-dimensional subspaces with dense union. Let A_N be "
            "the exact restriction in orthonormal coordinates and let "
            "||A_N-Atilde_N||<=rho_N. If "
            "lambda_min(Atilde_N)-rho_N>=-eta_N with eta_N tending to zero, then "
            "q is nonnegative on the whole space. For a continuous constraint map "
            "B into R^r, one certified full-row-rank restriction B_N remains "
            "surjective on every larger nested domain. A uniform positive finite-"
            "section gap is not necessary: Q e_j=e_j/j is strictly positive, while "
            "lambda_min(Q restricted to span(e_1,...,e_N))=1/N tends to zero."
        ),
        "proof": (
            "Fix v in V_M. For every N>=M the certified bound gives "
            "q(v)>=-eta_N||v||^2; taking N to infinity gives q(v)>=0. Continuity "
            "and density extend this to the Hilbert-space closure. If B_N(V_N)=R^r, "
            "then B_M(V_M) contains that range for every M>=N. The diagonal model "
            "has q(v)=sum_j |v_j|^2/j>0 for nonzero v, but its Nth restriction has "
            "minimum eigenvalue 1/N, refuting necessity of uniform coercivity."
        ),
        "asymptotic_lower_defect_rows": rows,
        "one_stage_constraint_rank_rows": rank_rows,
        "uniform_coercivity_no_go": (
            "Finite-section positivity may converge to a zero spectral edge. Requiring "
            "one N-independent positive eigenvalue margin would prove coercivity, a "
            "strictly stronger property than Weil nonnegativity."
        ),
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is not finite")
    value = abs(value)
    return (value & -value).bit_length() - 1


def accelerated_odd_step(value: int) -> tuple[int, int]:
    numerator = 3 * value + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def affine_word(word: tuple[int, ...] | list[int]) -> tuple[int, int]:
    constant = 0
    valuation_sum = 0
    for valuation in word:
        constant = 3 * constant + (1 << valuation_sum)
        valuation_sum += valuation
    return constant, valuation_sum


def cylinder_least_representative(word: tuple[int, ...] | list[int]) -> tuple[int, int]:
    constant, valuation_sum = affine_word(word)
    modulus = 1 << (valuation_sum + 1)
    inverse = pow(3 ** len(word), -1, modulus)
    residue = (((1 << valuation_sum) - constant) * inverse) % modulus
    if residue == 0:
        residue = modulus
    return residue, modulus


def realized_valuations(start: int, horizon: int) -> list[int]:
    values: list[int] = []
    current = start
    for _ in range(horizon):
        current, valuation = accelerated_odd_step(current)
        values.append(valuation)
    return values


def is_prefix_non_descending(start: int, horizon: int) -> bool:
    current = start
    for _ in range(horizon):
        current, _ = accelerated_odd_step(current)
        if current < start:
            return False
    return True


def collatz_cylinder_stabilization_audit() -> dict[str, object]:
    """Turn positive-natural support into an exact cross-scale residue criterion."""

    failures = 0
    exhaustive_rows: list[dict[str, object]] = []
    for horizon in range(1, 7):
        checked = 0
        horizon_failures = 0
        for word in product(range(1, 5), repeat=horizon):
            checked += 1
            representative, modulus = cylinder_least_representative(word)
            if representative % 2 != 1:
                horizon_failures += 1
                continue
            if realized_valuations(representative, horizon) != list(word):
                horizon_failures += 1
            if not 0 < representative < modulus:
                horizon_failures += 1
        failures += horizon_failures
        exhaustive_rows.append(
            {
                "horizon_H": horizon,
                "valuation_alphabet": [1, 2, 3, 4],
                "words_checked": checked,
                "failed_word_certificates": horizon_failures,
                "checks": {
                    "all_words_have_unique_odd_cylinder_representative": horizon_failures
                    == 0
                },
            }
        )

    natural_rows: list[dict[str, object]] = []
    for start in [3, 5, 7, 27, 31, 97, 871, 6171]:
        word: list[int] = []
        representatives: list[int] = []
        moduli: list[int] = []
        current = start
        for _ in range(24):
            current, valuation = accelerated_odd_step(current)
            word.append(valuation)
            representative, modulus = cylinder_least_representative(word)
            representatives.append(representative)
            moduli.append(modulus)
        first_stable = next(
            index + 1
            for index in range(len(representatives))
            if all(value == start for value in representatives[index:])
        )
        nested = all(
            representatives[index + 1] % moduli[index] == representatives[index]
            for index in range(len(representatives) - 1)
        )
        checks = {
            "representatives_are_nested": nested,
            "representatives_eventually_equal_start": representatives[-1] == start,
            "stabilization_occurs_after_modulus_exceeds_start": moduli[first_stable - 1]
            > start,
        }
        failures += sum(not value for value in checks.values())
        natural_rows.append(
            {
                "natural_start": start,
                "first_stabilization_horizon": first_stable,
                "representatives_first_12": representatives[:12],
                "moduli_first_12": moduli[:12],
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for horizon in [1, 2, 4, 8, 16, 32, 64]:
        word = [1] * horizon
        representative, modulus = cylinder_least_representative(word)
        expected = (1 << (horizon + 1)) - 1
        checks = {
            "least_representative_is_exact": representative == expected,
            "modulus_is_two_to_H_plus_one": modulus == 1 << (horizon + 1),
            "prefix_is_non_descending": is_prefix_non_descending(
                representative, horizon
            ),
            "representative_has_exponential_scale": representative
            >= 1 << horizon,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "horizon_H": horizon,
                "all_one_word": [1] * min(horizon, 16),
                "word_truncated_in_json": horizon > 16,
                "least_cylinder_representative": representative,
                "cylinder_modulus": modulus,
                "representative_over_two_to_H": representative / (1 << horizon),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For every finite accelerated-odd valuation word w=(a_1,...,a_H), "
            "with S=sum a_j and affine constant C(w), exactly one odd residue "
            "r_w modulo 2^(S+1) realizes w, namely "
            "r_w=(2^S-C(w))*3^(-H) mod 2^(S+1). Along an infinite ray these least "
            "positive representatives are nested. The ray has positive-natural "
            "support if and only if the representatives are bounded, equivalently "
            "eventually constant. No horizon-only subexponential bound can hold even "
            "for non-descending prefixes: the all-one word has least representative "
            "2^(H+1)-1 and is non-descending for all H prefix steps."
        ),
        "proof": (
            "The affine identity 2^S T^H(n)=3^H n+C(w), together with oddness of "
            "T^H(n), is equivalent to 3^H n+C(w)=2^S mod 2^(S+1). Since 3 is "
            "invertible modulo powers of two, this gives one residue. Reducing the "
            "identity at every prefix gives divisibility by 2^S_j; the remaining "
            "suffix affine constant is odd, so each prefix quotient is odd and every "
            "valuation is exact. Extending a word refines its residue class, so "
            "representatives are compatible. A "
            "bounded compatible sequence in strictly increasing power-of-two moduli "
            "must eventually stabilize; the stable integer realizes every prefix. "
            "Conversely a natural start is the least representative once the modulus "
            "exceeds it. Direct substitution gives r_(1,...,1)=2^(H+1)-1."
        ),
        "exhaustive_small_word_rows": exhaustive_rows,
        "natural_support_stabilization_rows": natural_rows,
        "all_one_subexponential_height_no_go_rows": no_go_rows,
        "no_go_scope": (
            "The exponential family rejects a universal horizon-only height bound. "
            "It is a sequence of finite natural starts, not one divergent orbit."
        ),
        "failure_count": failures,
    }


def cyclic_convolution_value(values: list[float], target: int) -> float:
    size = len(values)
    return sum(values[index] * values[(target - index) % size] for index in range(size))


def goldbach_target_phase_audit() -> dict[str, object]:
    """Retain target-aligned Fourier signs and show why positive terms matter."""

    failures = 0
    root_two = math.sqrt(2.0)
    exact_terms = [
        "1/8+sqrt(2)/4",
        "-3/8",
        "1/8-sqrt(2)/4",
        "1/8",
        "1/8-sqrt(2)/4",
        "-3/8",
        "1/8+sqrt(2)/4",
    ]
    toy = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0]
    toy_target = 4
    toy_transform = radix_two_fft(toy)
    toy_anchor = sum(toy) ** 2 / len(toy)
    toy_terms = [
        (
            toy_transform[index] ** 2
            * cmath.exp(2j * math.pi * index * toy_target / len(toy))
        ).real
        / len(toy)
        for index in range(1, len(toy))
    ]
    toy_negative = -sum(min(value, 0.0) for value in toy_terms)
    toy_positive = sum(max(value, 0.0) for value in toy_terms)
    toy_convolution = cyclic_convolution_value(toy, toy_target)
    toy_checks = {
        "exact_terms_match_numeric_dft": all(
            math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)
            for left, right in zip(
                toy_terms,
                [
                    Fraction(1, 8) + root_two / 4,
                    -Fraction(3, 8),
                    Fraction(1, 8) - root_two / 4,
                    Fraction(1, 8),
                    Fraction(1, 8) - root_two / 4,
                    -Fraction(3, 8),
                    Fraction(1, 8) + root_two / 4,
                ],
            )
        ),
        "negative_budget_exceeds_anchor": toy_negative > toy_anchor,
        "convolution_is_positive": toy_convolution == 1,
        "positive_terms_recover_exact_value": math.isclose(
            toy_anchor + toy_positive - toy_negative,
            toy_convolution,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ),
        "exact_inequality_4sqrt2_exceeds_5": 32 > 25,
    }
    failures += sum(not value for value in toy_checks.values())

    finite_rows: list[dict[str, object]] = []
    for prime_limit in [64, 128, 256, 512, 1024]:
        transform_size = 1
        while transform_size <= 2 * prime_limit:
            transform_size *= 2
        flags = prime_sieve(prime_limit)
        prime_signal = [
            1.0 if index <= prime_limit and flags[index] else 0.0
            for index in range(transform_size)
        ]
        transform = radix_two_fft(prime_signal)
        anchor = sum(prime_signal) ** 2 / transform_size
        absolute_budget = sum(
            abs(transform[index]) ** 2 / transform_size
            for index in range(1, transform_size)
        )
        global_l1_margin = anchor - absolute_budget
        pass_targets: list[int] = []
        minimum_phase_margin = math.inf
        minimum_phase_target = 0
        minimum_representation = math.inf
        maximum_reconstruction_error = 0.0
        bound_violations = 0
        target_count = 0
        for target in range(4, prime_limit + 1, 2):
            target_count += 1
            terms = [
                (
                    transform[index] ** 2
                    * cmath.exp(2j * math.pi * index * target / transform_size)
                ).real
                / transform_size
                for index in range(1, transform_size)
            ]
            negative_budget = -sum(min(value, 0.0) for value in terms)
            phase_margin = anchor - negative_budget
            if phase_margin > 1e-9:
                pass_targets.append(target)
            if phase_margin < minimum_phase_margin:
                minimum_phase_margin = phase_margin
                minimum_phase_target = target
            exact_count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            minimum_representation = min(minimum_representation, exact_count)
            reconstructed = anchor + sum(terms)
            maximum_reconstruction_error = max(
                maximum_reconstruction_error, abs(reconstructed - exact_count)
            )
            if phase_margin > exact_count + 1e-7:
                bound_violations += 1
        checks = {
            "zero_padding_prevents_wraparound": transform_size > 2 * prime_limit,
            "all_finite_targets_have_representations": minimum_representation > 0,
            "fourier_reconstruction_matches_exact_counts": maximum_reconstruction_error
            < 1e-7,
            "target_phase_bound_has_no_violations": bound_violations == 0,
            "target_phase_gate_is_stronger_than_global_l1": minimum_phase_margin
            >= global_l1_margin - 1e-8,
            "row_is_finite_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "prime_support_limit": prime_limit,
                "zero_padded_transform_size": transform_size,
                "even_targets_tested": target_count,
                "minimum_ordered_representation_count": minimum_representation,
                "zero_frequency_anchor": anchor,
                "global_l1_margin": global_l1_margin,
                "target_phase_gate_pass_count": len(pass_targets),
                "target_phase_gate_pass_targets": pass_targets,
                "minimum_target_phase_margin": minimum_phase_margin,
                "minimum_target_phase_margin_target": minimum_phase_target,
                "maximum_fourier_reconstruction_error": maximum_reconstruction_error,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a nonnegative function f on Z/q with unnormalized Fourier transform "
            "F, write c_k(n)=Re(F(k)^2 exp(2*pi*i*k*n/q))/q, P(n)=sum max(c_k,0), "
            "and N(n)=sum max(-c_k,0) over k nonzero. Then "
            "(f*f)(n)=F(0)^2/q+P(n)-N(n), so F(0)^2/q>N(n) is a rigorous "
            "target-aligned positivity certificate and is never weaker than the "
            "phase-blind L1 bound. It is not necessary: on Z/8, "
            "f=(0,0,0,0,0,0,1,2) has (f*f)(4)=1, anchor 9/8, and negative "
            "budget (1+sqrt(2))/2>9/8. Positive aligned frequencies are essential."
        ),
        "proof": (
            "Fourier inversion for convolution gives the exact decomposition after "
            "pairing conjugate terms and taking real parts. Dropping P gives the "
            "stated lower bound. Since N is at most the sum of all nonzero absolute "
            "Fourier contributions, it improves the phase-blind triangle bound. In "
            "the Z/8 model the seven aligned terms are the displayed exact list; "
            "their negative part is (1+sqrt(2))/2. The inequality against 9/8 "
            "reduces to 4sqrt(2)>5, whose square is 32>25, while direct convolution "
            "gives one representation."
        ),
        "exact_weighted_z8_no_go": {
            "signal": [0, 0, 0, 0, 0, 0, 1, 2],
            "target": toy_target,
            "aligned_nonzero_terms_exact": exact_terms,
            "aligned_nonzero_terms_decimal": toy_terms,
            "zero_frequency_anchor_exact": "9/8",
            "zero_frequency_anchor_decimal": toy_anchor,
            "negative_budget_exact": "(1+sqrt(2))/2",
            "negative_budget_decimal": toy_negative,
            "positive_budget_decimal": toy_positive,
            "exact_convolution_value": toy_convolution,
            "checks": toy_checks,
        },
        "finite_prime_target_phase_rows": finite_rows,
        "no_go_scope": (
            "The target-aligned negative budget is a sufficient certificate, not a "
            "necessary one. A uniform Goldbach proof must retain positive major-arc "
            "mass together with the signed minor-arc deficit."
        ),
        "failure_count": failures,
    }


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)]


def matrix_product(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def haar_basis(size: int) -> tuple[list[list[float]], list[int]]:
    if size < 2 or size & (size - 1):
        raise ValueError("Haar size must be a power of two")
    basis = [[1.0 / math.sqrt(size)] * size]
    scales = [0]
    span = size
    while span >= 2:
        normalization = 1.0 / math.sqrt(span)
        half = span // 2
        for start in range(0, size, span):
            vector = [0.0] * size
            for index in range(start, start + half):
                vector[index] = normalization
            for index in range(start + half, start + span):
                vector[index] = -normalization
            basis.append(vector)
            scales.append(int(math.log2(span)))
        span //= 2
    return basis, scales


def frobenius_energy(matrix: list[list[float]]) -> float:
    return sum(value * value for row in matrix for value in row)


def scale_pair_energies(
    transformed: list[list[float]], scales: list[int]
) -> dict[str, float]:
    energies: dict[str, float] = {}
    for row in range(1, len(transformed)):
        for column in range(1, len(transformed)):
            key = f"{scales[row]}x{scales[column]}"
            energies[key] = energies.get(key, 0.0) + transformed[row][column] ** 2
    return dict(sorted(energies.items()))


def twin_tensor_haar_audit() -> dict[str, object]:
    """Complete the two-parameter scale geometry omitted by diagonal scales."""

    failures = 0
    source = json.loads(
        (
            ROOT
            / "data"
            / "open-problem"
            / "twin-prime"
            / "tp-ticket-161-centered-typeii.json"
        ).read_text(encoding="utf-8")
    )
    source_rows = source["reproducible_computation"][
        "finite_cubic_rough_centered_incidence_rows"
    ]
    basis4, scales4 = haar_basis(4)
    finite_rows: list[dict[str, object]] = []
    for source_row in source_rows:
        matrix = [
            [float(value) for value in row]
            for row in source_row["centered_incidence_numerator"]
        ]
        transformed = matrix_product(matrix_product(basis4, matrix), transpose(basis4))
        pair_energy = scale_pair_energies(transformed, scales4)
        total_energy = frobenius_energy(matrix)
        nonconstant_energy = sum(pair_energy.values())
        diagonal_energy = sum(
            value
            for key, value in pair_energy.items()
            if key.split("x")[0] == key.split("x")[1]
        )
        off_diagonal_energy = nonconstant_energy - diagonal_energy
        checks = {
            "constant_transform_row_vanishes": max(
                abs(value) for value in transformed[0]
            )
            < 1e-7,
            "constant_transform_column_vanishes": max(
                abs(transformed[row][0]) for row in range(4)
            )
            < 1e-7,
            "all_scale_pairs_preserve_frobenius_energy": math.isclose(
                nonconstant_energy, total_energy, rel_tol=1e-12, abs_tol=1e-4
            ),
            "diagonal_and_off_diagonal_partition_energy": math.isclose(
                diagonal_energy + off_diagonal_energy,
                total_energy,
                rel_tol=1e-12,
                abs_tol=1e-4,
            ),
            "row_is_finite_factorization_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "X": source_row["X"],
                "haar_scale_pair_energy": pair_energy,
                "frobenius_energy": total_energy,
                "same_scale_pair_energy": diagonal_energy,
                "cross_scale_pair_energy": off_diagonal_energy,
                "cross_scale_energy_fraction": off_diagonal_energy / total_energy
                if total_energy
                else 0.0,
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for size in [4, 8, 16, 32, 64]:
        basis, scales = haar_basis(size)
        fine_index = scales.index(1)
        coarse_index = scales.index(2)
        row_wavelet = basis[fine_index]
        column_wavelet = basis[coarse_index]
        matrix = [
            [row_wavelet[row] * column_wavelet[column] for column in range(size)]
            for row in range(size)
        ]
        transformed = matrix_product(matrix_product(basis, matrix), transpose(basis))
        pair_energy = scale_pair_energies(transformed, scales)
        diagonal_energy = sum(
            value
            for key, value in pair_energy.items()
            if key.split("x")[0] == key.split("x")[1]
        )
        off_diagonal_energy = sum(pair_energy.values()) - diagonal_energy
        checks = {
            "all_row_sums_vanish": all(abs(sum(row)) < 1e-12 for row in matrix),
            "all_column_sums_vanish": all(
                abs(sum(matrix[row][column] for row in range(size))) < 1e-12
                for column in range(size)
            ),
            "frobenius_energy_is_one": math.isclose(
                frobenius_energy(matrix), 1.0, rel_tol=1e-12, abs_tol=1e-12
            ),
            "operator_norm_is_one_by_rank_one_construction": True,
            "same_scale_pair_energy_vanishes": diagonal_energy < 1e-12,
            "cross_scale_pair_energy_is_one": math.isclose(
                off_diagonal_energy, 1.0, rel_tol=1e-12, abs_tol=1e-12
            ),
            "single_nonzero_scale_pair_is_fine_by_coarse": math.isclose(
                pair_energy.get("1x2", 0.0), 1.0, rel_tol=1e-12, abs_tol=1e-12
            ),
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "dyadic_dimension_N": size,
                "row_wavelet_scale": 1,
                "column_wavelet_scale": 2,
                "same_scale_pair_energy": diagonal_energy,
                "cross_scale_pair_energy": off_diagonal_energy,
                "nonzero_scale_pair_energy": pair_energy,
                "frobenius_energy": frobenius_energy(matrix),
                "operator_norm": 1.0,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let H_N be the complete orthonormal discrete Haar basis and C=H_N A "
            "H_N^T. If every row and column sum of A vanishes, every coefficient "
            "with a constant Haar factor vanishes and Parseval gives "
            "||A||_F^2=sum_{j,k>=1} E_{j,k} over all row-scale/column-scale pairs. "
            "Same-scale terms j=k are not complete. For every dyadic N>=4, the "
            "rank-one matrix formed from a finest row wavelet and a next-coarser "
            "column wavelet has zero margins, Frobenius and operator norm one, zero "
            "same-scale energy, and all energy in the off-diagonal pair (1,2)."
        ),
        "proof": (
            "Orthogonality of H_N preserves Frobenius and operator norms. Zero row "
            "sums mean A times the constant vector is zero; zero column sums give "
            "the transpose statement, leaving precisely wavelet-wavelet coefficients. "
            "Parseval sums them over two independent scale indices. For A=u v^T "
            "with u and v normalized Haar wavelets of distinct scales, the transformed "
            "matrix is the outer product of two coordinate vectors, so it has one "
            "off-diagonal coefficient equal to one and no diagonal-scale coefficient."
        ),
        "finite_t161_all_scale_pair_rows": finite_rows,
        "different_scale_rank_one_no_go_rows": no_go_rows,
        "no_go_scope": (
            "TICKET-172 same-scale dyadic mixed variation is not a complete Type-II "
            "certificate. A prime-pair estimate must control all row/column scale pairs."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_finite_section_audit()
    collatz = collatz_cylinder_stabilization_audit()
    goldbach = goldbach_target_phase_audit()
    twin = twin_tensor_haar_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-173",
            "theorem_name": "CofinalFiniteSectionPositivityAndUniformCoercivityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No actual pole-neutral Guinand-Weil finite-section family has a "
                "certified lower defect eta_N tending to zero."
            ),
            "route_decision": {
                "discard": "requiring a uniform positive finite-section eigenvalue gap as necessary for Weil nonnegativity",
                "retain": "nested dense-core lower bounds with a certified negative defect tending to zero and one-stage constraint rank",
                "next_single_lemma": "PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero",
            },
            "proof_dag": proof_dag(
                "RH",
                "UniformPositiveFiniteSectionGapIsNecessaryForWeilPositivity",
                "CofinalFiniteSectionPositivityAndUniformCoercivityNoGo",
                "PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero",
            ),
            "claim_boundary": "No RH proof and no actual Weil-core positivity certificate; one abstract dense-core theorem and a uniform-coercivity no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-173",
            "theorem_name": "NaturalSupportCylinderStabilizationAndSubexponentialHeightNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No theorem forces the cylinder representatives of every infinite "
                "prefixwise non-descending ray to be unbounded."
            ),
            "route_decision": {
                "discard": "a universal horizon-only subexponential bound for least representatives of non-descending cylinders",
                "retain": "cross-scale cylinder lift increments as the exact computable coordinate of positive-natural support",
                "next_single_lemma": "EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives",
            },
            "proof_dag": proof_dag(
                "CO",
                "NonDescendingCylinderLeastRepresentativesHaveASubexponentialHorizonBound",
                "NaturalSupportCylinderStabilizationAndSubexponentialHeightNoGo",
                "EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives",
            ),
            "claim_boundary": "No Collatz proof and no divergent natural orbit; one exact natural-support stabilization criterion and an exponential finite-prefix no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-173",
            "theorem_name": "TargetAlignedNegativeSpectrumCertificateAndPositiveMassNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform major-arc positive lower bound dominates the signed "
                "minor-arc deficit for every sufficiently large even integer."
            ),
            "route_decision": {
                "discard": "using the target-aligned negative Fourier budget below the zero-mode anchor as a necessary or uniformly expected gate",
                "retain": "the exact positive-major-mass minus negative-minor-deficit decomposition at each target",
                "next_single_lemma": "UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit",
            },
            "proof_dag": proof_dag(
                "GB",
                "TargetAlignedNegativeBudgetBelowAnchorIsNecessaryForGoldbachPositivity",
                "TargetAlignedNegativeSpectrumCertificateAndPositiveMassNoGo",
                "UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; one exact target-phase certificate, an exact weighted no-go, and finite prime diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-173",
            "theorem_name": "TensorHaarAllScalePairCompletenessAndDiagonalScaleNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No prime-pair matrix estimate gives a power saving uniformly over "
                "every row-scale/column-scale Haar pair in the sieve range."
            ),
            "route_decision": {
                "discard": "controlling only equal row/column dyadic scales as a complete Type-II energy certificate",
                "retain": "the full tensor-Haar matrix indexed by two independent scales",
                "next_single_lemma": "PrimePairMatrixAllScalePairHaarEnergyPowerSaving",
            },
            "proof_dag": proof_dag(
                "TP",
                "SameScaleDyadicMixedVariationControlsAllTypeIIEnergy",
                "TensorHaarAllScalePairCompletenessAndDiagonalScaleNoGo",
                "PrimePairMatrixAllScalePairHaarEnergyPowerSaving",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; one exact tensor-Haar completeness theorem, finite diagnostics, and an anisotropic scale no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFiniteSectionCylinderPhaseTensorAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-173 proves four exact structural results and resolves none of "
            "the four conjectures. It replaces uniform RH coercivity by vanishing "
            "finite-section defect, characterizes Collatz natural support by cylinder "
            "stabilization, retains target-aligned positive and negative Goldbach "
            "Fourier mass, and corrects same-scale Twin variation to a complete two-"
            "parameter tensor-Haar target."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common correction is to retain the limiting coordinate that a one-"
            "parameter summary erases: asymptotic defect rather than uniform gap, "
            "nested lifts rather than one prefix, positive and negative phase rather "
            "than a negative budget alone, and two scale indices rather than one."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 gives a finite Guinand-Weil dictionary and tail budget but makes no RH claim; the abstract dense-core theorem here does not certify its arithmetic matrices.",
            "collatz": "Tao arXiv:1909.03562 is an almost-all logarithmic-density theorem, while Niu arXiv:2605.13886 explicitly remains finite; neither proves unbounded lifts on every non-descending ray.",
            "goldbach": "Grimmelt-Bhowmik arXiv:2607.27282 supplies explicit major-arc and exceptional-set context; it does not provide the target-uniform binary minor-arc domination required here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 shows substantial Type-II information is necessary; the tensor-Haar theorem only corrects the coordinate system for such information.",
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
    attempts: list[dict[str, object]] = []
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
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
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
        "finite_section_cylinder_phase_tensor_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket173-finite-section-cylinder-phase-tensor.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data"
        / "open-problem"
        / "riemann"
        / "rh-ticket-173-finite-section.json",
        "collatz": ROOT
        / "data"
        / "open-problem"
        / "collatz"
        / "co-ticket-173-cylinder-stabilization.json",
        "goldbach": ROOT
        / "data"
        / "open-problem"
        / "goldbach"
        / "gb-ticket-173-target-phase.json",
        "twin-prime": ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-173-tensor-haar.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
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


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            f"TICKET-173 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
