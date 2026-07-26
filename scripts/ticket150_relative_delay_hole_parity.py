from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-07-28T09:00:00+09:00"
SCHEMA = "primeproject.ticket150-relative-delay-hole-parity.v1"
STATUS = "exact_partial_theorems_and_sharp_no_go_results_all_conjectures_open"


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
    rejected_id = f"{problem_code}-T150-REJECTED"
    closed_id = f"{problem_code}-T150-CLOSED"
    open_id = f"{problem_code}-T150-OPEN"
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
        "edges": [[rejected_id, closed_id], [closed_id, open_id]],
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def riemann_relative_form_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    relative_sizes = [
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(1),
        Fraction(5, 4),
        Fraction(3, 2),
        Fraction(2),
    ]
    for index in range(1, 17):
        reference_eigenvalue = Fraction(1, 2**index)
        for relative_size in relative_sizes:
            perturbation_eigenvalue = -relative_size * reference_eigenvalue
            combined_eigenvalue = (
                reference_eigenvalue + perturbation_eigenvalue
            )
            checks = {
                "reference_direction_positive": reference_eigenvalue > 0,
                "relative_norm_identity": (
                    abs(perturbation_eigenvalue)
                    == relative_size * reference_eigenvalue
                ),
                "nonnegative_at_or_below_one": (
                    (relative_size <= 1) == (combined_eigenvalue >= 0)
                ),
                "strictly_positive_below_one": (
                    (relative_size < 1) == (combined_eigenvalue > 0)
                ),
                "strictly_negative_above_one": (
                    (relative_size > 1) == (combined_eigenvalue < 0)
                ),
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "basis_index_j": index,
                    "reference_eigenvalue_pj": fraction_payload(
                        reference_eigenvalue
                    ),
                    "relative_form_norm_q": fraction_payload(relative_size),
                    "absolute_perturbation_norm": fraction_payload(
                        abs(perturbation_eigenvalue)
                    ),
                    "combined_eigenvalue": fraction_payload(
                        combined_eigenvalue
                    ),
                    "checks": checks,
                }
            )

    coercivity_rows: list[dict[str, object]] = []
    for exponent in range(1, 17):
        candidate_lower_bound = Fraction(1, 2**exponent)
        witness_index = exponent + 1
        witness_value = Fraction(1, 2**witness_index)
        check = witness_value < candidate_lower_bound
        failures += int(not check)
        coercivity_rows.append(
            {
                "candidate_ambient_lower_bound_c": fraction_payload(
                    candidate_lower_bound
                ),
                "witness_basis_index": witness_index,
                "witness_reference_value": fraction_payload(witness_value),
                "violates_P_ge_cI": check,
            }
        )

    return {
        "theorem": (
            "Let P be a nonnegative self-adjoint operator with trivial "
            "kernel and form domain Q(P), and let k be a symmetric form on "
            "Q(P). Assume there is a bounded self-adjoint B such that "
            "k[v,w]=<P^(1/2)v,BP^(1/2)w>. If ||B||<=1 then p+k is "
            "nonnegative; if ||B||<1 then p+k>=(1-||B||)p. The threshold "
            "is sharp: for "
            "every q>1 and every tail index j, K=-q p_j<.,e_j>e_j makes "
            "P+K negative on e_j even when the absolute norm q p_j is "
            "arbitrarily small. Moreover, an injective positive compact "
            "operator on an infinite-dimensional Hilbert space cannot "
            "satisfy P>=cI for any c>0."
        ),
        "proof": (
            "For v in Q(P), writing u=P^(1/2)v gives "
            "(p+k)[v]=<u,(I+B)u>>=(1-||B||)||u||^2. "
            "For the sharp family take Pe_j=p_j e_j with p_j down to zero "
            "and K=-q p_j<.,e_j>e_j. Its relative norm is q, its absolute "
            "norm is q p_j, and the combined eigenvalue is (1-q)p_j. "
            "Finally, positive compact eigenvalues tend to zero, so every "
            "claimed ambient lower bound c is violated by a tail "
            "eigenvector."
        ),
        "finite_relative_threshold_rows": rows,
        "finite_compact_coercivity_rows": coercivity_rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is not used")
    value = abs(value)
    return (value & -value).bit_length() - 1


def accelerated_collatz(value: int) -> tuple[int, int]:
    if value <= 0 or value % 2 == 0:
        raise ValueError("accelerated Collatz expects a positive odd integer")
    numerator = 3 * value + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def odd_part(value: int) -> int:
    return value >> v2(value)


def type_two_delay_witness(shadow_pairs: int, delay: int) -> dict[str, object]:
    if shadow_pairs < 0 or delay < 1:
        raise ValueError("shadow_pairs must be nonnegative and delay positive")
    two_modulus = 1 << (delay + 1)
    nine_power = 9**shadow_pairs
    coefficient = pow(nine_power, -1, two_modulus)
    while (
        coefficient == 1 and shadow_pairs == 0
    ) or (1 << (3 * shadow_pairs + 2)) * coefficient - 5 <= 0:
        coefficient += two_modulus

    exit_odd_coefficient = nine_power * coefficient
    start = (1 << (3 * shadow_pairs + 2)) * coefficient - 5
    expected_exit = 4 * exit_odd_coefficient - 5

    current = start
    shadow_valuations: list[int] = []
    for _ in range(2 * shadow_pairs):
        current, valuation = accelerated_collatz(current)
        shadow_valuations.append(valuation)
    actual_exit = current

    post_values: list[int] = []
    post_valuations: list[int] = []
    for _ in range(delay + 2):
        current, valuation = accelerated_collatz(current)
        post_values.append(current)
        post_valuations.append(valuation)

    checks = {
        "exact_shadow_word": shadow_valuations == [1, 2] * shadow_pairs,
        "exact_type_two_exit": actual_exit == expected_exit,
        "crt_divisibility_by_nine_power": (
            exit_odd_coefficient % nine_power == 0
        ),
        "crt_mersenne_congruence": (
            exit_odd_coefficient % two_modulus == 1
        ),
        "post_prefix_is_one_one_then_delay_ones": (
            post_valuations == [1, 1] + [1] * delay
        ),
        "all_post_values_above_exit": min(post_values) > actual_exit,
        "all_post_values_above_original_start": min(post_values) > start,
    }
    return {
        "shadow_pair_count_L": shadow_pairs,
        "forced_post_delay_H": delay,
        "coefficient_c": str(coefficient),
        "exit_odd_coefficient_d": str(exit_odd_coefficient),
        "original_start_n": str(start),
        "type_two_exit_x": str(actual_exit),
        "shadow_valuations": shadow_valuations,
        "post_exit_valuations": post_valuations,
        "minimum_post_exit_value": str(min(post_values)),
        "checks": checks,
    }


def collatz_exit_type_audit() -> dict[str, object]:
    local_rows: list[dict[str, object]] = []
    failures = 0
    for exit_order in [1, 2, 3]:
        strict_descents = 0
        equalities = 0
        strict_expansions = 0
        row_failures = 0
        for coefficient in range(3, 2_003, 2):
            exit_value = (1 << exit_order) * coefficient - 5
            first, first_valuation = accelerated_collatz(exit_value)
            if exit_order == 1:
                expected = odd_part(3 * coefficient - 7)
                check = (
                    first == expected
                    and first <= exit_value
                    and (first == exit_value) == (coefficient == 3)
                )
                strict_descents += int(first < exit_value)
                equalities += int(first == exit_value)
            elif exit_order == 2:
                second, second_valuation = accelerated_collatz(first)
                expected = 9 * coefficient - 10
                check = (
                    (first_valuation, second_valuation) == (1, 1)
                    and second == expected
                    and first > exit_value
                    and second > exit_value
                )
                strict_expansions += int(
                    first > exit_value and second > exit_value
                )
            else:
                second, second_valuation = accelerated_collatz(first)
                expected = odd_part(9 * coefficient - 5)
                check = (
                    first_valuation == 1
                    and second_valuation >= 3
                    and second == expected
                    and second < exit_value
                )
                strict_descents += int(second < exit_value)
            row_failures += int(not check)
        failures += row_failures
        local_rows.append(
            {
                "exit_order_r": exit_order,
                "odd_coefficients_audited": 1_000,
                "strict_local_descents": strict_descents,
                "local_equalities": equalities,
                "strict_local_expansions": strict_expansions,
                "failure_count": row_failures,
            }
        )

    delay_rows: list[dict[str, object]] = []
    for shadow_pairs in range(0, 7):
        for delay in [1, 2, 4, 8, 16, 32]:
            row = type_two_delay_witness(shadow_pairs, delay)
            failures += sum(not value for value in row["checks"].values())
            delay_rows.append(row)

    return {
        "theorem": (
            "Write a post-shadow exit as x_r=2^r d-5 with d odd and "
            "r in {1,2,3}. For positive exits, r=1 satisfies "
            "T(x_1)<=x_1 with equality only at x_1=1, while r=3 satisfies "
            "T^2(x_3)<x_3. In contrast, r=2 has valuation prefix (1,1) "
            "and T(x_2),T^2(x_2)>x_2. More strongly, for every shadow "
            "length L and every H there is a positive start whose exact "
            "(1,2)^L shadow exits with r=2 and is followed by (1,1,1^H), "
            "with every one of those H+2 post-exit iterates above both the "
            "exit and the original start."
        ),
        "proof": (
            "For r=1 direct substitution gives "
            "T(2d-5)=oddpart(3d-7)<=(3d-7)/2<=2d-5. For r=3, the first "
            "two valuations are 1 and at least 3 and "
            "T^2(8d-5)=oddpart(9d-5)<8d-5. For r=2 the first valuations "
            "are (1,1) and T^2(4d-5)=9d-10>4d-5. Given L,H, choose "
            "d divisible by 9^L and congruent to 1 modulo 2^(H+1). The "
            "Chinese remainder theorem supplies such positive d. Reversing "
            "the exact shadow identity gives the required positive start, "
            "and 9d-10 is congruent to -1 modulo 2^(H+1), forcing H "
            "additional valuation-one expansion steps."
        ),
        "finite_exit_type_rows": local_rows,
        "finite_crt_delay_rows": delay_rows,
        "failure_count": failures,
    }


def prime_divisors(value: int) -> list[int]:
    divisors: list[int] = []
    remaining = value
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            divisors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1 if candidate == 2 else 2
    if remaining > 1:
        divisors.append(remaining)
    return divisors


def euler_phi(value: int) -> int:
    result = value
    for prime in prime_divisors(value):
        result = result // prime * (prime - 1)
    return result


def wheel_main_term(modulus: int, endpoint: int) -> int:
    result = 1
    for prime in prime_divisors(modulus):
        result *= prime - 1 if endpoint % prime == 0 else prime - 2
    return result


def wheel_fixed_point_count(modulus: int, endpoint: int) -> int:
    half_modulus = modulus // 2
    first = (endpoint // 2) % half_modulus
    candidates = [first, first + half_modulus]
    return sum(
        candidate % 2 == 1 and math.gcd(candidate, modulus) == 1
        for candidate in candidates
    )


def cyclic_convolution(values: list[int], endpoint: int) -> int:
    modulus = len(values)
    return sum(
        values[index] * values[(endpoint - index) % modulus]
        for index in range(modulus)
    )


def sharp_hole_witness(modulus: int, endpoint: int) -> dict[str, object]:
    reduced = [
        math.gcd(residue, modulus) == 1 for residue in range(modulus)
    ]
    values = [int(value) for value in reduced]
    visited: set[int] = set()
    compatible = [
        residue
        for residue in range(modulus)
        if reduced[residue] and reduced[(endpoint - residue) % modulus]
    ]
    for residue in compatible:
        if residue in visited:
            continue
        partner = (endpoint - residue) % modulus
        visited.add(residue)
        visited.add(partner)
        values[min(residue, partner)] = 0

    distance_squared = sum(
        (values[index] - int(reduced[index])) ** 2
        for index in range(modulus)
    )
    main_term = wheel_main_term(modulus, endpoint)
    fixed_points = wheel_fixed_point_count(modulus, endpoint)
    sharp_radius_squared = (main_term + fixed_points) // 2
    return {
        "endpoint_N": endpoint,
        "local_main_term_m": main_term,
        "reflection_fixed_points_h": fixed_points,
        "sharp_hole_radius_squared": sharp_radius_squared,
        "constructed_distance_squared": distance_squared,
        "constructed_convolution": cyclic_convolution(values, endpoint),
        "checks": {
            "fixed_point_count_is_zero_or_one": fixed_points in [0, 1],
            "radius_numerator_is_even": (
                (main_term + fixed_points) % 2 == 0
            ),
            "constructed_hole_is_exact": (
                cyclic_convolution(values, endpoint) == 0
            ),
            "constructed_distance_is_sharp": (
                distance_squared == sharp_radius_squared
            ),
        },
    }


def goldbach_sharp_hole_radius_audit() -> dict[str, object]:
    exact_rows: list[dict[str, object]] = []
    failures = 0
    for modulus in [6, 30, 210, 2_310]:
        endpoint_rows = [
            sharp_hole_witness(modulus, endpoint)
            for endpoint in range(0, modulus, 2)
        ]
        failures_here = sum(
            not value
            for row in endpoint_rows
            for value in row["checks"].values()
        )
        failures += failures_here
        phi = euler_phi(modulus)
        exact_rows.append(
            {
                "wheel_modulus_W": modulus,
                "reduced_residue_count_phiW": phi,
                "even_endpoints_audited": modulus // 2,
                "minimum_sharp_radius_squared": min(
                    row["sharp_hole_radius_squared"]
                    for row in endpoint_rows
                ),
                "maximum_sharp_radius_squared": max(
                    row["sharp_hole_radius_squared"]
                    for row in endpoint_rows
                ),
                "minimum_relative_radius_squared": min(
                    Fraction(row["sharp_hole_radius_squared"], phi)
                    for row in endpoint_rows
                ).__str__(),
                "sample_rows": endpoint_rows[: min(8, len(endpoint_rows))],
                "failure_count": failures_here,
            }
        )

    primorial_rows: list[dict[str, object]] = []
    primorial = 2
    phi = 1
    main_term_at_two = 1
    previous_ratio: Fraction | None = None
    monotone = True
    for prime in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
        primorial *= prime
        phi *= prime - 1
        main_term_at_two *= prime - 2
        radius_squared = (main_term_at_two + 1) // 2
        ratio = Fraction(radius_squared, phi)
        if previous_ratio is not None:
            monotone = monotone and ratio < previous_ratio
        previous_ratio = ratio
        primorial_rows.append(
            {
                "largest_odd_prime_z": prime,
                "primorial_wheel_W": str(primorial),
                "phi_W": str(phi),
                "endpoint_N": 2,
                "local_main_term_m": str(main_term_at_two),
                "fixed_points_h": 1,
                "sharp_radius_squared": str(radius_squared),
                "relative_radius_squared": fraction_payload(ratio),
            }
        )
    failures += int(not monotone)

    return {
        "theorem": (
            "Let W be even and squarefree, G the reduced residues, "
            "g=1_G, and tau_N(a)=N-a. Put "
            "m=(g*g)(N) and let h be the number of fixed points of tau_N "
            "inside G. Among all nonnegative cyclic weights f with "
            "(f*f)(N)=0, the exact minimum of ||f-g||_2^2 is (m+h)/2. "
            "Consequently ||f-g||_2^2<(m+h)/2 forces positivity, and the "
            "threshold is sharp. For primorial W and N=2, h=1 and the "
            "relative sharp radius (m+1)/(2 phi(W)) tends to zero. Thus "
            "there is no fixed epsilon>0 for which "
            "||f-g||_2^2<epsilon phi(W) forces (f*f)(2)>0 uniformly over "
            "all primorial W."
        ),
        "proof": (
            "The compatible reduced residues split under tau_N into "
            "two-cycles and h fixed points. Since f is nonnegative and "
            "the endpoint convolution is zero, every two-cycle must have "
            "at least one zero weight and every fixed point must have zero "
            "weight. The least squared distance from g is therefore one "
            "per two-cycle and one per fixed point, namely "
            "(m-h)/2+h=(m+h)/2; zeroing exactly one member of every orbit "
            "attains equality. For N=2 on a primorial wheel, "
            "m=product_(3<=p<=z)(p-2), h=1, and "
            "m/phi(W)=product_(3<=p<=z)(1-1/(p-1)) tends to zero because "
            "the reciprocal-prime sum diverges."
        ),
        "finite_exact_wheel_rows": exact_rows,
        "primorial_relative_radius_rows": primorial_rows,
        "primorial_ratio_strictly_decreasing_in_audit": monotone,
        "failure_count": failures,
    }


def twin_cover_parity_audit() -> dict[str, object]:
    source_path = (
        ROOT
        / "data/open-problem/ticket149-smooth-escape-wheel-cover.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_rows = source["smooth_escape_wheel_cover_audit"]["twin_prime"][
        "reproducible_computation"
    ]["finite_cover_rows"]
    rows: list[dict[str, object]] = []
    failures = 0
    for source_row in source_rows:
        edge_count = int(source_row["edge_count_E"])
        left_cover = int(source_row["left_semiprime_edges_L"])
        right_cover = int(source_row["right_semiprime_edges_R"])
        double_semiprime = int(source_row["double_semiprime_edges_D"])
        twins = int(source_row["exact_twin_count"])
        a10 = (
            2 * left_cover - edge_count
        )
        a01 = (
            2 * right_cover - edge_count
        )
        deficit = edge_count - left_cover - right_cover
        checks = {
            "deficit_equals_twin_minus_double_semiprime": (
                deficit == twins - double_semiprime
            ),
            "deficit_equals_negative_liouville_marginal_half": (
                2 * deficit == -(a10 + a01)
            ),
            "positive_deficit_is_twin_dominance": (
                (deficit > 0) == (twins > double_semiprime)
            ),
            "source_lower_bound_matches": (
                deficit
                == int(source_row["marginal_only_twin_lower_bound"])
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": int(source_row["X"]),
                "rough_edges_E": edge_count,
                "twin_edges_T": twins,
                "double_semiprime_edges_D": double_semiprime,
                "cover_deficit_E_minus_L_minus_R": deficit,
                "A10_plus_A01": a10 + a01,
                "normalized_deficit": fraction_payload(
                    Fraction(deficit, edge_count)
                ),
                "checks": checks,
            }
        )

    synthetic_rows: list[dict[str, object]] = []
    for twins, double_semiprime in [(1, 2), (2, 2), (3, 2), (1, 100)]:
        left_only = 0
        right_only = 0
        edge_count = twins + double_semiprime
        left_cover = double_semiprime + left_only
        right_cover = double_semiprime + right_only
        deficit = edge_count - left_cover - right_cover
        check = deficit == twins - double_semiprime
        failures += int(not check)
        synthetic_rows.append(
            {
                "twin_cell_T": twins,
                "double_semiprime_cell_D": double_semiprime,
                "left_only_cell": left_only,
                "right_only_cell": right_only,
                "edge_count_E": edge_count,
                "cover_deficit": deficit,
                "twins_exist": twins > 0,
                "positive_cover_deficit": deficit > 0,
                "identity_passes": check,
            }
        )

    return {
        "theorem": (
            "On cubic-rough gap-two support, let T be the twin cell and D "
            "the double-semiprime cell. Then "
            "E-L-R=T-D=-(A10+A01)/2. Hence a uniform cover deficit "
            "L+R<=(1-delta)E is exactly the parity-sensitive inequality "
            "T-D>=delta E, equivalently "
            "A10+A01<=-2 delta E. It is stronger than merely asserting "
            "that a twin exists in the interval: T>0 does not imply T>D."
        ),
        "proof": (
            "Partition every rough edge into the four endpoint parity cells "
            "D=(semiprime,semiprime), the two mixed cells, and "
            "T=(prime,prime). Then E is the sum of all four cells, while "
            "L and R each contain D and one different mixed cell. "
            "Subtraction leaves T-D. The Liouville identities "
            "L=(E+A10)/2 and R=(E+A01)/2 give the second equality. "
            "A table with T=1 and D=2 has a twin but negative cover "
            "deficit, proving that existence alone is insufficient."
        ),
        "finite_source_rows": rows,
        "synthetic_separation_rows": synthetic_rows,
        "source_artifact": str(source_path.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "source_sha256": file_sha256(source_path),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_relative_form_audit()
    collatz = collatz_exit_type_audit()
    goldbach = goldbach_sharp_hole_radius_audit()
    twin_prime = twin_cover_parity_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": "ActualWeilPrimeArchimedeanRelativeFormBoundAtMostOne",
        "collatz": (
            "TypeTwoAdaptiveValuationSurplusDescentBelowShadowEntry"
        ),
        "goldbach": "VonMangoldtEndpointReflectionMassRetentionK56",
        "twin_prime": (
            "PositiveCubicRoughMassAndOneSidedLiouvilleMarginalGap"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-150",
            "theorem_name": (
                "RelativeFormThresholdAndCompactAmbientCoercivityNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "This is an abstract quadratic-form theorem. No decomposition "
                "of the actual Weil form into a positive reference and "
                "relatively bounded prime/archimedean perturbation is "
                "constructed, and no zeta zero is controlled. Compact "
                "ambient L2 coercivity is ruled out; the correct energy-form "
                "topology and a relative bound at most one remain missing."
            ),
            "route_decision": {
                "discard": (
                    "a compact positive reference that is uniformly coercive "
                    "in the ambient L2 norm, or absolute tail smallness as a "
                    "substitute for a relative form estimate"
                ),
                "retain": (
                    "decompose the actual Weil form in its energy topology "
                    "and certify a prime-plus-archimedean relative form norm "
                    "at most one"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "CompactReferenceAmbientL2Coercivity",
                "RelativeFormThresholdAndCompactAmbientCoercivityNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One sharp abstract "
                "form threshold and one compact-coercivity no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-150",
            "theorem_name": (
                "ThreeExitLocalCompensationAndTypeTwoArbitraryDelayNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Local descent below the r=1 or r=3 exit need not repay the "
                "preceding (9/8)^L shadow expansion. The r=2 CRT family "
                "defeats every fixed post-exit horizon but does not produce "
                "an infinite divergent orbit. An adaptive, unbounded "
                "valuation-surplus theorem remains unproved."
            ),
            "route_decision": {
                "discard": (
                    "any fixed-length post-shadow descent window selected "
                    "only from the three exit types"
                ),
                "retain": (
                    "for r=2, use an adaptive stopping time whose accumulated "
                    "valuation surplus repays both the shadow expansion and "
                    "the forced Mersenne-like delay"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedThreeExitTypePostShadowDescentWindow",
                "ThreeExitLocalCompensationAndTypeTwoArbitraryDelayNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent positive orbit. Two local "
                "exit contractions and an arbitrary finite-delay no-go."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-150",
            "theorem_name": (
                "SharpWheelEndpointHoleRadiusAndGrowingRelativeL2NoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The theorem concerns nonnegative cyclic wheel weights, not "
                "the interval von Mangoldt convolution. The sharp hole "
                "witnesses are not prime weights and endpoint N=2 on a "
                "primorial wheel is not a Goldbach counterexample. Actual "
                "endpoint-reflection mass retention at the K56 scale remains "
                "unproved."
            ),
            "route_decision": {
                "discard": (
                    "a wheel-independent relative L2 closeness threshold as "
                    "a pointwise positivity certificate on growing wheels"
                ),
                "retain": (
                    "control nonnegative von Mangoldt mass on the exact "
                    "endpoint-reflection orbits, with arithmetic cancellation "
                    "strong enough for the K56 finite-glue budget"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "UniformRelativeL2WheelTransferToEveryEndpoint",
                "SharpWheelEndpointHoleRadiusAndGrowingRelativeL2NoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "nonnegative endpoint stability radius and a growing-wheel "
                "relative-L2 no-go."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-150",
            "theorem_name": (
                "SemiprimeCoverDeficitExactParityEquivalence"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The identity does not estimate A10+A01 or prove positive "
                "rough edge mass at all scales. It shows that the cover "
                "deficit is a signed prime-versus-double-semiprime parity "
                "bias, not an unsigned combinatorial shortcut. The required "
                "one-sided Liouville gap remains open."
            ),
            "route_decision": {
                "discard": (
                    "treating the semiprime cover deficit as an unsigned "
                    "marginal statistic that avoids the parity problem"
                ),
                "retain": (
                    "prove positive cubic-rough mass together with the "
                    "explicit signed one-sided Liouville marginal gap "
                    "A10+A01<=-2 delta A00"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "UnsignedSemiprimeCoverAvoidsParityBarrier",
                "SemiprimeCoverDeficitExactParityEquivalence",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. One exact parity "
                "equivalence, finite source replay, and synthetic separation."
            ),
        },
    }
    return {
        "theorem_name": "FourConjectureRelativeDelayHoleParityAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-150 proves four exact intermediate or no-go theorems "
            "and resolves no target conjecture. It fixes the RH relative-form "
            "threshold, isolates an arbitrarily delayed Collatz exit type, "
            "computes the sharp nonnegative Goldbach wheel endpoint-hole "
            "radius, and identifies the Twin semiprime-cover deficit as an "
            "exact parity-sensitive twin-minus-double-semiprime bias."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Current primary Weil-form context. TICKET-150 supplies "
                    "only an abstract relative-form theorem."
                ),
            },
            {
                "citation": "Niu, Parity vectors and paradoxical sequences in the accelerated Collatz map",
                "url": "https://arxiv.org/abs/2605.13886",
                "role": (
                    "Current primary finitary parity-vector boundary. The "
                    "CRT delay family is not a universal Collatz theorem."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary explicit minor-arc context for the distinction "
                    "between cyclic wheel geometry and arithmetic residuals."
                ),
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II and parity-boundary context. The "
                    "TICKET-150 identity supplies no missing signed estimate."
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
                    "audit_ref": f"relative_delay_hole_parity_audit.{key}"
                },
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_theorem"],
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
        "relative_delay_hole_parity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket150-relative-delay-hole-parity.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-150-relative-form-threshold.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-150-type-two-delay.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-150-endpoint-hole-radius.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-150-cover-parity-equivalence.json"
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
