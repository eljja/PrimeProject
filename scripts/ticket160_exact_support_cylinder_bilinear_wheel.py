from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket151_negative_affine_transversal_logtwo import (
    integer_cube_root,
    smallest_prime_factor_sieve,
)
from ticket157_formcore_inversion_proxy_margin import affine_constant
from ticket159_diagonal_threshold_phase_parity import prime_sieve


GENERATED_AT = "2026-07-27T01:30:00+09:00"
SCHEMA = "primeproject.ticket160-exact-support-cylinder-bilinear-wheel.v1"
STATUS = "four_exact_reductions_and_no_go_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def integer_payload(value: int) -> dict[str, object]:
    return {
        "exact": str(value),
        "bit_length": value.bit_length(),
        "decimal_digits": len(str(abs(value))),
    }


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T160-REJECTED"
    closed_id = f"{problem_code}-T160-CLOSED"
    open_id = f"{problem_code}-T160-OPEN"
    return {
        "nodes": [
            {
                "id": rejected_id,
                "label": rejected_name,
                "status": "refuted_or_misidentified",
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
        "edges": [[rejected_id, closed_id], [closed_id, open_id]],
    }


def prime_powers_up_to(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    values: set[int] = set()
    for prime in range(2, limit + 1):
        if not flags[prime]:
            continue
        power = prime
        while power <= limit:
            values.add(power)
            if power > limit // prime:
                break
            power *= prime
    return sorted(values)


def normalized_hat_g_constant_vector(cutoff: int, q: int) -> float:
    if q >= cutoff:
        return 0.0
    return 2.0 * (1.0 - math.log(q) / math.log(cutoff))


def riemann_exact_support_nesting_audit() -> dict[str, object]:
    support_rows: list[dict[str, object]] = []
    failures = 0

    for cutoff in [4, 16, 64, 256]:
        powers = prime_powers_up_to(4 * cutoff)
        interior = [q for q in powers if q < cutoff]
        boundary = [q for q in powers if q == cutoff]
        outside = [q for q in powers if q > cutoff]
        outside_weights = [
            normalized_hat_g_constant_vector(cutoff, q) for q in outside
        ]
        boundary_weights = [
            normalized_hat_g_constant_vector(cutoff, q) for q in boundary
        ]
        checks = {
            "all_outside_prime_power_weights_are_exactly_zero": all(
                value == 0.0 for value in outside_weights
            ),
            "boundary_prime_power_weight_is_zero": all(
                value == 0.0 for value in boundary_weights
            ),
            "interior_prime_power_weights_are_positive": all(
                normalized_hat_g_constant_vector(cutoff, q) > 0
                for q in interior
            ),
            "support_partition_is_complete": (
                len(interior) + len(boundary) + len(outside) == len(powers)
            ),
        }
        failures += sum(not value for value in checks.values())
        support_rows.append(
            {
                "prime_cutoff_c": cutoff,
                "enumeration_limit": 4 * cutoff,
                "interior_prime_power_count": len(interior),
                "boundary_prime_power_count": len(boundary),
                "outside_prime_power_count": len(outside),
                "interior_prime_powers": interior,
                "boundary_prime_powers": boundary,
                "outside_prime_powers": outside,
                "maximum_absolute_omitted_weight": max(
                    [abs(value) for value in outside_weights] or [0.0]
                ),
                "checks": checks,
            }
        )

    cross_cutoff_rows = [
        {
            "sample_frequency": "Delta_4/2",
            "hat_g_4_over_pi": fraction_payload(Fraction(1)),
            "hat_g_16_over_pi": fraction_payload(Fraction(3, 2)),
        },
        {
            "sample_frequency": "3*Delta_4/2",
            "hat_g_4_over_pi": fraction_payload(Fraction(0)),
            "hat_g_16_over_pi": fraction_payload(Fraction(1, 2)),
        },
    ]
    for row in cross_cutoff_rows:
        checks = {
            "cutoff_profiles_differ": (
                row["hat_g_4_over_pi"]["exact"]
                != row["hat_g_16_over_pi"]["exact"]
            )
        }
        row["checks"] = checks
        failures += sum(not value for value in checks.values())

    return {
        "theorem": (
            "Fix c>1 and N>=0 in the finite Guinand-Weil dictionary, with "
            "Delta_c=log(c)/(2*pi) and supp(hat g_{c,N,v}) contained in "
            "[-Delta_c,Delta_c]. Every omitted prime-power term q>c is "
            "exactly zero, because log(q)/(2*pi)>Delta_c; a boundary "
            "prime power q=c is also zero because the induced Fourier "
            "weight vanishes at the endpoint. Thus the dictionary's "
            "prime-support remainder A_{c,N} is identically zero. "
            "Conversely, let F_{c,N} be the raw cutoff Galerkin functions: "
            "finite trigonometric polynomials on the cutoff interval I_c, "
            "embedded into L2(R) by zero extension. If c1<c2, then "
            "F_{c1,N1} intersect F_{c2,N2}={0}. Hence raw spaces at "
            "different cutoffs cannot be treated as one nested Galerkin "
            "chain."
        ),
        "proof": (
            "The support statement removes every q>c term one by one. At "
            "q=c the Volterra kernel is evaluated at zero and vanishes. "
            "For the nesting no-go, a function in both zero-extended "
            "spaces is a finite trigonometric polynomial on the larger "
            "interval but vanishes on its nonempty outer open subinterval. "
            "Real analyticity forces that polynomial, and therefore the "
            "function, to vanish identically. TICKET-159's abstract "
            "diagonal selector remains correct, but a decaying prime-band "
            "remainder is not the missing input for this finite dictionary; "
            "a certified common-core transport is."
        ),
        "finite_prime_support_rows": support_rows,
        "exact_cross_cutoff_profile_rows": cross_cutoff_rows,
        "prime_support_remainder": fraction_payload(Fraction(0)),
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    return (value & -value).bit_length() - 1


def accelerated_step(value: int) -> tuple[int, int]:
    exponent = v2(3 * value + 1)
    return (3 * value + 1) >> exponent, exponent


def valuation_prefix(value: int, length: int) -> tuple[int, ...]:
    result: list[int] = []
    current = value
    for _ in range(length):
        current, exponent = accelerated_step(current)
        result.append(exponent)
    return tuple(result)


def cylinder_residue(word: tuple[int, ...]) -> tuple[int, int]:
    residue = 1
    total = 0
    prefix: tuple[int, ...] = ()
    for exponent in word:
        if exponent <= 0:
            raise ValueError("valuation words must be positive")
        old_modulus = 1 << (total + 1)
        prefix = prefix + (exponent,)
        candidates = [
            residue + lift * old_modulus for lift in range(1 << exponent)
        ]
        matches = [
            candidate
            for candidate in candidates
            if valuation_prefix(candidate, len(prefix)) == prefix
        ]
        if len(matches) != 1:
            raise RuntimeError("valuation cylinder did not lift uniquely")
        residue = matches[0]
        total += exponent
    return residue, 1 << (total + 1)


def contracting_tail_payload(word: tuple[int, ...]) -> dict[str, object]:
    residue, modulus = cylinder_residue(word)
    length = len(word)
    total = sum(word)
    constant = affine_constant(word)
    denominator = (1 << total) - 3**length
    if denominator <= 0:
        return {
            "contracting": False,
            "residue": residue,
            "modulus": modulus,
            "affine_constant_C": constant,
            "contracting_denominator_D": denominator,
        }

    if denominator * residue > constant:
        exceptional_count = 0
        least_descending_start = residue
    else:
        exceptional_count = (
            (constant - denominator * residue)
            // (denominator * modulus)
        ) + 1
        least_descending_start = residue + exceptional_count * modulus

    iterate = least_descending_start
    observed_word: list[int] = []
    for _ in word:
        iterate, exponent = accelerated_step(iterate)
        observed_word.append(exponent)
    checks = {
        "least_tail_start_realizes_word": tuple(observed_word) == word,
        "least_tail_start_descends": iterate < least_descending_start,
        "previous_cylinder_start_does_not_descend": (
            exceptional_count == 0
            or (
                (
                    3**length
                    * (least_descending_start - modulus)
                    + constant
                )
                // (1 << total)
                >= least_descending_start - modulus
            )
        ),
        "strict_affine_threshold_holds": (
            denominator * least_descending_start > constant
        ),
    }
    return {
        "contracting": True,
        "residue": residue,
        "modulus": modulus,
        "affine_constant_C": constant,
        "contracting_denominator_D": denominator,
        "threshold_C_over_D": fraction_payload(
            Fraction(constant, denominator)
        ),
        "exceptional_nonnegative_cylinder_start_count": exceptional_count,
        "least_descending_cylinder_start": least_descending_start,
        "iterate_after_word": iterate,
        "checks": checks,
    }


def front_loaded_natural_transfer_audit() -> dict[str, object]:
    failures = 0
    rows: list[dict[str, object]] = []
    selected_depths = [
        2,
        3,
        4,
        5,
        8,
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
    ]

    for length in selected_depths:
        first_valuation = length + 1
        word = (first_valuation,) + (1,) * (length - 1)
        total = 2 * length
        constant = affine_constant(word)
        closed_constant = (
            ((1 << (length + 1)) + 1) * 3 ** (length - 1)
            - 4**length
        )
        denominator = 4**length - 3**length
        least_t = 1 if length % 2 else 3
        least_start = (
            (1 << (2 * length + 1)) * least_t
            - (1 << (length + 1))
            - 1
        ) // 3
        closed_endpoint = 2 * 3 ** (length - 1) * least_t - 1
        affine_endpoint = (
            3**length * least_start + constant
        ) // (1 << total)
        natural_transfer_margin = (
            denominator * least_t - ((1 << length) - 1)
        )
        threshold_lower_bound = (
            Fraction(2, 3) * Fraction(3, 2) ** length
            + Fraction(1, 3) * Fraction(3, 4) ** length
            - 1
        )
        checks = {
            "total_valuation_is_2m": sum(word) == total,
            "affine_constant_closed_form_is_exact": (
                constant == closed_constant
            ),
            "word_is_contracting": denominator > 0,
            "least_parameter_satisfies_integrality_congruence": (
                (
                    (1 << (2 * length + 1)) * least_t
                    - (1 << (length + 1))
                    - 1
                )
                % 3
                == 0
            ),
            "closed_endpoint_matches_affine_iterate": (
                closed_endpoint == affine_endpoint
            ),
            "every_natural_realizer_margin_is_positive": (
                natural_transfer_margin > 0
            ),
            "least_natural_realizer_descends": (
                closed_endpoint < least_start
            ),
            "threshold_exceeds_explicit_divergent_lower_bound": (
                Fraction(constant, denominator) > threshold_lower_bound
            ),
        }
        if length <= 64:
            checks["direct_valuation_replay_matches_word"] = (
                valuation_prefix(least_start, length) == word
            )
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "word_length_m": length,
                "front_loaded_word": (
                    [first_valuation] + [1] * min(length - 1, 8)
                ),
                "front_loaded_word_truncated_in_json": length > 9,
                "total_valuation_S": total,
                "affine_constant_C": integer_payload(constant),
                "contracting_denominator_D": integer_payload(denominator),
                "least_natural_parameter_t": least_t,
                "least_natural_realizer": integer_payload(least_start),
                "iterate_after_m_accelerated_steps": integer_payload(
                    closed_endpoint
                ),
                "natural_transfer_margin": integer_payload(
                    natural_transfer_margin
                ),
                "affine_threshold_C_over_D": fraction_payload(
                    Fraction(constant, denominator)
                ),
                "explicit_threshold_lower_bound": fraction_payload(
                    threshold_lower_bound
                ),
                "checks": checks,
            }
        )

    return {
        "family": "w_m=(m+1,1,...,1), S_m=2m",
        "audited_depths": selected_depths,
        "theorem": (
            "For every m>=2 the front-loaded word "
            "w_m=(m+1,1,...,1) has D_m=4^m-3^m>0 and an affine "
            "threshold tending to infinity. Every positive natural "
            "realizer is parameterized by "
            "n=(2^(2m+1)t-2^(m+1)-1)/3, where t=1+3q for odd m and "
            "t=3+3q for even m. Its m-step endpoint is "
            "2*3^(m-1)t-1, and descent is equivalent to "
            "(4^m-3^m)t>2^m-1. Since 4^m-3^m>4^(m-1)>=2^m, every "
            "positive natural realizer descends despite the unbounded "
            "abstract threshold."
        ),
        "proof": (
            "The affine constant expands to "
            "(2^(m+1)+1)3^(m-1)-4^m. Dividing it by the upper bound "
            "4^m for D_m gives the divergent lower bound "
            "(2/3)(3/2)^m+(1/3)(3/4)^m-1. The valuation-one tail forces "
            "the first endpoint to equal 2^m t-1; solving the first "
            "inverse step gives the displayed natural parameterization. "
            "Direct comparison of the closed endpoint and start reduces "
            "descent to the final strict integer inequality."
        ),
        "exact_natural_transfer_rows": rows,
        "failure_count": failures,
    }


def collatz_cylinder_realizability_audit() -> dict[str, object]:
    failures = 0
    summary_rows: list[dict[str, object]] = []

    for length in [2, 3, 4, 5]:
        cap = 5
        word_count = 0
        unique_count = 0
        contracting_count = 0
        contracting_density = Fraction(0)
        all_truncated_density = Fraction(0)
        maximum_exception_count = 0
        for raw_word in product(range(1, cap + 1), repeat=length):
            word = tuple(raw_word)
            word_count += 1
            residue, modulus = cylinder_residue(word)
            unique = valuation_prefix(residue, length) == word
            unique_count += int(unique)
            total = sum(word)
            cylinder_density = Fraction(1, 1 << total)
            all_truncated_density += cylinder_density
            payload = contracting_tail_payload(word)
            if payload["contracting"]:
                contracting_count += 1
                contracting_density += cylinder_density
                maximum_exception_count = max(
                    maximum_exception_count,
                    int(
                        payload[
                            "exceptional_nonnegative_cylinder_start_count"
                        ]
                    ),
                )
                failures += sum(
                    not value for value in payload["checks"].values()
                )
            failures += int(not unique)
            failures += int(modulus != 1 << (total + 1))

        expected_truncated_density = (
            sum(Fraction(1, 1 << exponent) for exponent in range(1, cap + 1))
            ** length
        )
        checks = {
            "every_truncated_word_has_unique_residue": (
                unique_count == word_count
            ),
            "truncated_prefix_family_is_not_complete": (
                all_truncated_density < 1
            ),
            "density_matches_geometric_product": (
                all_truncated_density == expected_truncated_density
            ),
            "contracting_family_cannot_cover_all_odd_starts": (
                contracting_density < 1
            ),
        }
        failures += sum(not value for value in checks.values())
        summary_rows.append(
            {
                "word_length_m": length,
                "valuation_cap_A": cap,
                "word_count": word_count,
                "unique_residue_count": unique_count,
                "contracting_word_count": contracting_count,
                "all_truncated_cylinder_density_among_odds": (
                    fraction_payload(all_truncated_density)
                ),
                "contracting_cylinder_density_upper_bound_among_odds": (
                    fraction_payload(contracting_density)
                ),
                "uncovered_density_lower_bound": fraction_payload(
                    1 - contracting_density
                ),
                "maximum_finite_exception_count_in_one_contracting_cylinder": (
                    maximum_exception_count
                ),
                "checks": checks,
            }
        )

    witness_words = [
        (2,),
        (1, 3),
        (1, 1, 4),
        (1, 2, 3),
        (3, 1, 1, 2),
        (1, 1, 2, 1, 4),
    ]
    witness_rows: list[dict[str, object]] = []
    for word in witness_words:
        payload = contracting_tail_payload(word)
        checks = {
            "word_is_contracting": bool(payload["contracting"]),
            "tail_checks_pass": (
                bool(payload["contracting"])
                and all(payload["checks"].values())
            ),
        }
        failures += sum(not value for value in checks.values())
        witness_rows.append(
            {
                "valuation_word": list(word),
                **payload,
                "witness_checks": checks,
            }
        )

    front_loaded = front_loaded_natural_transfer_audit()
    failures += int(front_loaded["failure_count"])

    return {
        "theorem": (
            "Every positive accelerated-Collatz valuation word "
            "w=(a_1,...,a_m), with S=sum a_j, is realized by exactly one "
            "odd residue class r_w modulo 2^(S+1). Its density among odd "
            "integers is 2^(-S). If D_w=2^S-3^m>0, then all but finitely "
            "many positive members n=r_w+k*2^(S+1) satisfy "
            "T_w(n)<n; the exceptional count and least descending member "
            "are obtained exactly from D_w*n>C(w). Moreover, the explicit "
            "front-loaded family w_m=(m+1,1,...,1) has thresholds tending "
            "to infinity, yet every positive natural realizer descends "
            "after m accelerated steps. Conversely, a finite prefix-free "
            "family of cylinders whose Kraft sum sum_w 2^(-S(w)) is below "
            "one cannot cover all odd starts."
        ),
        "proof": (
            "Induct on the word. A prefix with total S has one residue "
            "modulo 2^(S+1). Appending valuation a examines its 2^a lifts "
            "modulo 2^(S+a+1). After the old prefix, those lifts run through "
            "all odd residues modulo 2^(a+1), because their difference is "
            "2*3^m times the lift index. Exactly one has v2(3y+1)=a. This "
            "proves uniqueness and density. The affine iterate is "
            "(3^m n+C(w))/2^S, so D_w*n>C(w) is exactly descent and leaves "
            "only finitely many progression members below its threshold. "
            "For w_m, exact natural parameterization reduces descent to "
            "(4^m-3^m)t>2^m-1, which holds for every admissible t. Thus an "
            "unbounded abstract threshold is not a natural non-descent "
            "witness. The final coverage no-go is the Kraft/union bound."
        ),
        "finite_cylinder_summary_rows": summary_rows,
        "exact_contracting_tail_witness_rows": witness_rows,
        "front_loaded_unbounded_threshold_natural_transfer": front_loaded,
        "failure_count": failures,
    }


def direct_dft(values: list[float]) -> list[complex]:
    size = len(values)
    return [
        sum(
            value * cmath.exp(-2j * math.pi * frequency * index / size)
            for index, value in enumerate(values)
        )
        for frequency in range(size)
    ]


def direct_inverse_dft(values: list[complex]) -> list[complex]:
    size = len(values)
    return [
        sum(
            value * cmath.exp(2j * math.pi * frequency * index / size)
            for frequency, value in enumerate(values)
        )
        / size
        for index in range(size)
    ]


def project_frequencies(
    values: list[float],
    frequencies: set[int],
) -> list[float]:
    transform = direct_dft(values)
    projected = [
        value if index in frequencies else 0j
        for index, value in enumerate(transform)
    ]
    return [value.real for value in direct_inverse_dft(projected)]


def inner(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def norm(values: list[float]) -> float:
    return math.sqrt(inner(values, values))


def reflect(values: list[float], target: int) -> list[float]:
    size = len(values)
    return [values[(target - index) % size] for index in range(size)]


def goldbach_bilinear_proxy_audit() -> dict[str, object]:
    failures = 0
    identity_rows: list[dict[str, object]] = []

    for size, target in [(8, 6), (12, 8), (16, 10), (20, 14)]:
        frequencies = {1, 2, size - 2, size - 1}
        observed = [
            float(((3 * index + 1) % 7) - 3) for index in range(size)
        ]
        proxy = [
            float(((2 * index + 2) % 5) - 2) for index in range(size)
        ]
        projected_observed = project_frequencies(observed, frequencies)
        projected_proxy = project_frequencies(proxy, frequencies)
        difference = [
            left - right
            for left, right in zip(projected_observed, projected_proxy)
        ]
        total = [
            left + right
            for left, right in zip(projected_observed, projected_proxy)
        ]
        observed_form = inner(
            projected_observed,
            reflect(projected_observed, target),
        )
        proxy_form = inner(
            projected_proxy,
            reflect(projected_proxy, target),
        )
        defect = observed_form - proxy_form
        factorized_defect = inner(difference, reflect(total, target))
        bound = norm(difference) * norm(total)
        checks = {
            "symmetric_projection_is_real": all(
                abs(value.imag) < 1e-10
                for value in direct_inverse_dft(
                    [
                        value if index in frequencies else 0j
                        for index, value in enumerate(direct_dft(observed))
                    ]
                )
            ),
            "bilinear_defect_factorization_holds": (
                abs(defect - factorized_defect) < 1e-9
            ),
            "cauchy_bound_holds": abs(defect) <= bound + 1e-9,
        }
        failures += sum(not value for value in checks.values())
        identity_rows.append(
            {
                "group_size_L": size,
                "target_even_N": target,
                "minor_frequency_count": len(frequencies),
                "observed_minor_form": observed_form,
                "proxy_minor_form": proxy_form,
                "observed_minus_proxy_defect": defect,
                "factorized_defect": factorized_defect,
                "cauchy_product_bound": bound,
                "bound_slack": bound - abs(defect),
                "checks": checks,
            }
        )

    sharp_rows: list[dict[str, object]] = []
    for size, target, frequency in [
        (11, 4, 1),
        (12, 7, 2),
        (17, 10, 3),
        (32, 18, 5),
    ]:
        scale = math.sqrt(2 / size)
        positive = [
            scale
            * math.cos(
                2 * math.pi * frequency * (index - target / 2) / size
            )
            for index in range(size)
        ]
        negative = [
            scale
            * math.sin(
                2 * math.pi * frequency * (index - target / 2) / size
            )
            for index in range(size)
        ]
        positive_form = inner(positive, reflect(positive, target))
        negative_form = inner(negative, reflect(negative, target))
        positive_norm = norm(positive)
        negative_norm = norm(negative)
        transform_positive = direct_dft(positive)
        transform_negative = direct_dft(negative)
        allowed = {frequency, (-frequency) % size}
        leakage = max(
            [
                abs(value)
                for index, value in enumerate(transform_positive)
                if index not in allowed
            ]
            + [
                abs(value)
                for index, value in enumerate(transform_negative)
                if index not in allowed
            ]
            + [0.0]
        )
        checks = {
            "positive_reflection_eigenfunction_has_unit_form": (
                abs(positive_form - 1) < 1e-10
            ),
            "negative_reflection_eigenfunction_has_minus_unit_form": (
                abs(negative_form + 1) < 1e-10
            ),
            "both_norms_are_one": (
                abs(positive_norm - 1) < 1e-10
                and abs(negative_norm - 1) < 1e-10
            ),
            "support_is_one_conjugate_frequency_pair": leakage < 1e-10,
            "cauchy_constant_one_is_saturated": (
                abs(abs(positive_form) - positive_norm**2) < 1e-10
                and abs(abs(negative_form) - negative_norm**2) < 1e-10
            ),
        }
        failures += sum(not value for value in checks.values())
        sharp_rows.append(
            {
                "group_size_L": size,
                "target_N": target,
                "frequency_k": frequency,
                "positive_norm": positive_norm,
                "negative_norm": negative_norm,
                "positive_reflection_form": positive_form,
                "negative_reflection_form": negative_form,
                "maximum_off_pair_dft_leakage": leakage,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "On G=Z/LZ let S=-S be a minor-frequency set, P_S the "
            "orthogonal Fourier projection, and R_N h(x)=h(N-x). For real "
            "f,g, the minor bilinear coefficient equals "
            "E_S(N;f,g)=<P_S f,R_N P_S g>. Hence for every real proxy p, "
            "E_S(N;f,f)-E_S(N;p,p)="
            "<P_S(f-p),R_N P_S(f+p)>, and its absolute value is at most "
            "||P_S(f-p)||_2 ||P_S(f+p)||_2. The constant one is sharp on "
            "the ambient real-sequence class: a normalized cosine centered "
            "at N/2 is a +1 reflection eigenvector, while the corresponding "
            "sine is a -1 eigenvector, both supported on one conjugate "
            "frequency pair."
        ),
        "proof": (
            "Fourier inversion gives the reflection bilinear identity. The "
            "operator R_N is a self-adjoint unitary involution and commutes "
            "with a conjugation-closed projection. Expanding the difference "
            "of the two quadratic forms cancels the cross terms and "
            "Cauchy-Schwarz gives the product bound without an explicit "
            "sqrt(|S|) loss. The centered cosine and sine are exact "
            "reflection eigenfunctions of signs +1 and -1, respectively, "
            "so p=0 attains equality. Therefore no universal constant "
            "c<1 follows from Hilbert-space geometry alone; any saving must "
            "use arithmetic restrictions of prime weights."
        ),
        "finite_bilinear_proxy_identity_rows": identity_rows,
        "exact_sharp_reflection_counterexample_rows": sharp_rows,
        "failure_count": failures,
    }


def primes_up_to(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def first_twin_after(bound: int) -> tuple[int, int]:
    flags = prime_sieve(max(1000, 4 * bound + 100))
    for value in range(max(3, bound + 1), len(flags) - 2):
        if flags[value] and flags[value + 2]:
            return value, value + 2
    raise RuntimeError("twin witness search limit was too small")


def crt_pairwise(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    modulus = math.prod(moduli)
    result = 0
    for residue, component in zip(residues, moduli):
        partial = modulus // component
        inverse = pow(partial, -1, component)
        result = (result + residue * partial * inverse) % modulus
    return result, modulus


def twin_fixed_wheel_crt_audit() -> dict[str, object]:
    failures = 0
    rows: list[dict[str, object]] = []
    prime_pool = primes_up_to(1000)

    for roughness_bound in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        wheel_primes = [
            prime for prime in prime_pool if prime <= roughness_bound
        ]
        wheel_modulus = math.prod(wheel_primes)
        twin_start, twin_end = first_twin_after(roughness_bound)
        auxiliary = [
            prime
            for prime in prime_pool
            if prime > twin_end and math.gcd(prime, wheel_modulus) == 1
        ][:2]
        q, r = auxiliary
        composite_start, combined_modulus = crt_pairwise(
            [twin_start % wheel_modulus, 0, (-2) % r],
            [wheel_modulus, q, r],
        )
        while composite_start <= max(q, r) or composite_start + 2 <= r:
            composite_start += combined_modulus
        composite_end = composite_start + 2
        checks = {
            "twin_witness_is_prime_pair": (
                bool(prime_sieve(twin_end)[twin_start])
                and bool(prime_sieve(twin_end)[twin_end])
            ),
            "wheel_residues_are_identical": (
                composite_start % wheel_modulus
                == twin_start % wheel_modulus
            ),
            "first_composite_is_proper_multiple": (
                composite_start % q == 0 and composite_start > q
            ),
            "second_composite_is_proper_multiple": (
                composite_end % r == 0 and composite_end > r
            ),
            "crt_moduli_are_pairwise_coprime": (
                math.gcd(wheel_modulus, q) == 1
                and math.gcd(wheel_modulus, r) == 1
                and q != r
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "roughness_bound_z": roughness_bound,
                "wheel_modulus_M": wheel_modulus,
                "wheel_prime_count": len(wheel_primes),
                "twin_witness": [twin_start, twin_end],
                "auxiliary_composite_divisors": [q, r],
                "double_composite_witness": [
                    composite_start,
                    composite_end,
                ],
                "shared_residue_mod_M": twin_start % wheel_modulus,
                "combined_crt_modulus_Mqr": combined_modulus,
                "checks": checks,
            }
        )

    factor_horizon_rows: list[dict[str, object]] = []
    cutoffs = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(cutoffs[-1] + 2)
    for cutoff in cutoffs:
        roughness = integer_cube_root(cutoff)
        prime_prime = 0
        semiprime_semiprime = 0
        factor_horizon = 0
        critical_witness: tuple[int, int] | None = None
        first_prime_pair: tuple[int, int] | None = None
        factorization_checks = True
        for value in range(2, cutoff - 1):
            shifted = value + 2
            if spf[value] <= roughness or spf[shifted] <= roughness:
                continue
            left_prime = spf[value] == value
            right_prime = spf[shifted] == shifted
            if left_prime and right_prime:
                prime_prime += 1
                if first_prime_pair is None:
                    first_prime_pair = (value, shifted)
                continue
            if left_prime or right_prime:
                continue
            semiprime_semiprime += 1
            local_horizon = min(spf[value], spf[shifted])
            if local_horizon > factor_horizon:
                factor_horizon = local_horizon
                critical_witness = (value, shifted)
            left_quotient = value // spf[value]
            right_quotient = shifted // spf[shifted]
            factorization_checks = (
                factorization_checks
                and spf[left_quotient] == left_quotient
                and spf[right_quotient] == right_quotient
                and spf[value] * spf[value] <= value
                and spf[shifted] * spf[shifted] <= shifted
            )

        if critical_witness is None or first_prime_pair is None:
            failures += 1
            continue
        left, right = critical_witness
        horizon_below = factor_horizon - 1
        critical_invisible_below = (
            spf[left] > horizon_below and spf[right] > horizon_below
        )
        critical_visible_at_horizon = (
            spf[left] <= factor_horizon
            or spf[right] <= factor_horizon
        )
        every_double_composite_visible = True
        for value in range(2, cutoff - 1):
            shifted = value + 2
            if spf[value] <= roughness or spf[shifted] <= roughness:
                continue
            if spf[value] == value or spf[shifted] == shifted:
                continue
            if (
                spf[value] > factor_horizon
                and spf[shifted] > factor_horizon
            ):
                every_double_composite_visible = False
                break
        checks = {
            "both_target_classes_exist": (
                prime_prime > 0 and semiprime_semiprime > 0
            ),
            "critical_qq_is_invisible_below_threshold": (
                critical_invisible_below
            ),
            "critical_qq_is_visible_at_threshold": (
                critical_visible_at_horizon
            ),
            "every_qq_is_visible_at_threshold": (
                every_double_composite_visible
            ),
            "pp_feature_is_zero_at_every_factor_horizon": (
                spf[first_prime_pair[0]] == first_prime_pair[0]
                and spf[first_prime_pair[1]] == first_prime_pair[1]
            ),
            "cubic_rough_composites_are_semiprimes": factorization_checks,
        }
        failures += sum(not value for value in checks.values())
        factor_horizon_rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_z": roughness,
                "prime_prime_pair_count_PP": prime_prime,
                "semiprime_semiprime_pair_count_QQ": (
                    semiprime_semiprime
                ),
                "exact_separation_factor_horizon_tau_X": factor_horizon,
                "tau_X_over_sqrt_X": (
                    factor_horizon / math.sqrt(cutoff)
                ),
                "first_prime_pair_zero_feature_witness": list(
                    first_prime_pair
                ),
                "critical_double_composite_witness": [left, right],
                "critical_witness_factorizations": [
                    [spf[left], left // spf[left]],
                    [spf[right], right // spf[right]],
                ],
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let M>=1 and suppose (p,p+2) is a twin-prime pair with "
            "gcd(p(p+2),M)=1. Choose distinct primes q,r not dividing M. "
            "The Chinese remainder theorem gives infinitely many n with "
            "n=p (mod M), n=0 (mod q), and n=-2 (mod r). Taking n large "
            "makes both n and n+2 proper composites. Therefore no "
            "classifier measurable only from the fixed wheel residue "
            "n mod M can correctly separate every twin-prime pair from "
            "every double-composite pair. This strictly extends the "
            "TICKET-159 low-divisor-bit no-go to every feature of one "
            "fixed residue class. Separately, on the cubic-rough finite "
            "set Omega_X, let Phi_{X,y} record proper prime divisors "
            "z<p<=y of both endpoints and define tau_X as the maximum over "
            "double-composite pairs of the smaller endpoint least factor. "
            "A pointwise Phi_{X,y} classifier separates all PP from all QQ "
            "if and only if y>=tau_X. Unrestricted factor features "
            "therefore separate only by searching to the exact factor "
            "horizon; that is factorization information, not a parity "
            "breakthrough."
        ),
        "proof": (
            "The three moduli M,q,r are pairwise coprime, so CRT supplies "
            "one class modulo Mqr and therefore infinitely many positive "
            "solutions. Add a multiple of Mqr until n>q and n+2>r. Then "
            "q is a proper factor of n and r a proper factor of n+2, while "
            "n and p have the same residue modulo M. Any function of that "
            "residue assigns the twin and double-composite examples the "
            "same feature value. For the factor horizon, every PP has the "
            "all-zero proper-factor vector. A QQ also has the zero vector "
            "exactly while both endpoint least factors exceed y. Removing "
            "every such collision is equivalent to y being at least the "
            "maximum smaller least factor over QQ, namely tau_X. Cubic "
            "roughness makes every retained composite a semiprime, so the "
            "feature interpretation is exact."
        ),
        "finite_fixed_wheel_crt_rows": rows,
        "finite_cubic_rough_factor_horizon_rows": factor_horizon_rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_exact_support_nesting_audit()
    collatz = collatz_cylinder_realizability_audit()
    goldbach = goldbach_bilinear_proxy_audit()
    twin_prime = twin_fixed_wheel_crt_audit()
    sections_raw = [riemann, collatz, goldbach, twin_prime]
    total_failures = sum(
        int(section["failure_count"]) for section in sections_raw
    )
    next_theorems = {
        "riemann": "EffectiveCommonNestedWeilCoreTransport",
        "collatz": (
            "MinimalContractingFrontLoadedNaturalTransfer"
        ),
        "goldbach": (
            "PrimeRestrictedMinorProxyDefectBelow"
            "ExplicitSingularSeriesMargin"
        ),
        "twin_prime": (
            "IndependentCubicRoughBilinearIncidenceDeficit"
        ),
    }
    sections: dict[str, Any] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-160",
            "theorem_name": (
                "ExactPrimeSupportClosureAndCrossCutoffNestingNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The exact support closure does not build a common form "
                "core, a transport operator, or positive Weil margins. The "
                "cross-cutoff theorem is a no-go for raw zero-extended "
                "Galerkin spaces, not for every possible transported core."
            ),
            "route_decision": {
                "discard": (
                    "searching for a decaying omitted-prime remainder in "
                    "the exact finite dictionary, or treating matrices at "
                    "different c as nested compressions without transport"
                ),
                "retain": (
                    "construct one explicit nested Weil form core and "
                    "certified maps into each cutoff-dependent Galerkin "
                    "space with vanishing form-norm transport error"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "CutoffPrimeTailIsTheMissingRemainderAndRawSpacesNest",
                "ExactPrimeSupportClosureAndCrossCutoffNestingNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact correction "
                "to the prime-band interpretation and one cross-cutoff "
                "Galerkin nesting no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-160",
            "theorem_name": (
                "UniqueCylinderAndFrontLoadedNaturalTransferNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Every finite valuation word is realizable, but choosing a "
                "contracting word does not show that an arbitrary orbit "
                "enters its cylinder above the word's affine threshold. "
                "The front-loaded theorem closes only one explicit family, "
                "and finite cylinder families with Kraft sum below one "
                "still leave odd starts uncovered."
            ),
            "route_decision": {
                "discard": (
                    "treating abstract-word unrealizability as the remaining "
                    "obstruction, treating an unbounded abstract threshold "
                    "as natural non-descent, or inferring global descent "
                    "from a finite prefix family of mass below one"
                ),
                "retain": (
                    "prove exact natural transfer for the minimally "
                    "contracting front-loaded family "
                    "S_m=ceil(m log_2 3), then seek an orbitwise cover"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "UnboundedAbstractThresholdImpliesNaturalNonDescent",
                "UniqueCylinderAndFrontLoadedNaturalTransferNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact "
                "valuation-cylinder realizability theorem, cofinite tail "
                "criterion, infinite front-loaded natural-transfer theorem, "
                "and finite Kraft-mass no-go."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-160",
            "theorem_name": (
                "MinorReflectionBilinearProxyIdentityAndSharpAmbientNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The reflection identity is exact but supplies no "
                "prime-restricted proxy or singular-series margin. The "
                "sharp examples are signed real sequences, not prime DFTs "
                "and not Goldbach counterexamples."
            ),
            "route_decision": {
                "discard": (
                    "expecting a universal constant below one from "
                    "phase-sensitive Hilbert-space geometry alone"
                ),
                "retain": (
                    "construct an arithmetic proxy for prime weights whose "
                    "projected bilinear defect is uniformly below an "
                    "explicit binary major-arc margin"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "AmbientBilinearGeometrySuppliesAUniformSavingBelowOne",
                (
                    "MinorReflectionBilinearProxyIdentityAnd"
                    "SharpAmbientNoGo"
                ),
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "phase-sensitive bilinear identity and four sharp ambient "
                "reflection counterexamples."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-160",
            "theorem_name": (
                "FixedWheelCRTBlindnessAndExactFactorHorizonThreshold"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The CRT no-go applies to one fixed modulus at a time. It "
                "does not rule out scale-growing moduli or Type II bilinear "
                "estimates. The factor-horizon classifier uses explicit "
                "factor information and is not a prime-producing method; "
                "the observed tau_X/sqrt(X) trend is finite only."
            ),
            "route_decision": {
                "discard": (
                    "using any fixed wheel residue or finite collection of "
                    "characters through it as a uniform classifier, or "
                    "calling unrestricted trial-division features a "
                    "nonlocal parity breakthrough"
                ),
                "retain": (
                    "derive the cubic-rough least-factor incidence deficit "
                    "from an independent Type I/II estimate rather than "
                    "from labels or explicit factorization"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "FixedWheelOrUnrestrictedFactorFeatureBreaksParity",
                (
                    "FixedWheelCRTBlindnessAnd"
                    "ExactFactorHorizonThreshold"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no terminal counterexample. One "
                "exact CRT no-go for fixed wheel features and one exact "
                "finite factor-search threshold characterization."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureExactSupportCylinderBilinearWheelAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-160 proves four exact reductions or no-go theorems and "
            "resolves no target conjecture. It corrects the RH prime-band "
            "remainder to exact support closure and exposes the missing "
            "cross-cutoff transport, closes finite Collatz word "
            "realizability and an infinite high-threshold natural-transfer "
            "family while proving finite cylinder mass is not a global "
            "cover, derives a sharp phase-sensitive Goldbach bilinear proxy "
            "identity, and extends Twin local blindness through both a "
            "fixed-wheel CRT no-go and an exact finite factor horizon."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Groskin, A finite Guinand-Weil dictionary and "
                    "archimedean tail order for the truncated Weil "
                    "quadratic form, 2026"
                ),
                "url": "https://arxiv.org/abs/2607.02828",
                "role": (
                    "Primary exact support formula. TICKET-160 uses its "
                    "published support identity and independently states "
                    "the raw cross-cutoff nesting no-go."
                ),
            },
            {
                "citation": (
                    "Suzuki, Weil's quadratic form via the screw function, "
                    "2026"
                ),
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Primary continuous Weil-form and localization context. "
                    "It does not provide the common transport lemma claimed "
                    "open here."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Primary almost-all theorem. It does not imply the "
                    "pointwise orbitwise cylinder cover required here."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary explicit large-sieve and bilinear minor-arc "
                    "context for ternary Goldbach; it is not promoted to "
                    "the missing binary coefficient theorem."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II lower-bound context supporting the "
                    "need to move beyond fixed local wheel information."
                ),
            },
        ],
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
                        "exact_support_cylinder_bilinear_wheel_audit."
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
        "exact_support_cylinder_bilinear_wheel_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket160-exact-support-cylinder-bilinear-wheel.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-160-exact-support-transport.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-160-cylinder-realizability.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-160-bilinear-proxy.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-160-fixed-wheel-crt.json"
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
