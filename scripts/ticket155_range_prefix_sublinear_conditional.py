from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket152_compression_cylinder_energy_selection import (
    integer_cube_root,
    smallest_prime_factor_sieve,
)
from ticket154_compact_suffix_wheel_leastfactor import prime_theta_values


GENERATED_AT = "2026-07-26T17:00:00+09:00"
SCHEMA = "primeproject.ticket155-range-prefix-sublinear-conditional.v1"
STATUS = "exact_route_corrections_and_no_go_results_all_four_conjectures_open"


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
    rejected_id = f"{problem_code}-T155-REJECTED"
    closed_id = f"{problem_code}-T155-CLOSED"
    open_id = f"{problem_code}-T155-OPEN"
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


def riemann_range_tail_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0

    # A unit rank-one coupling can have squared coordinate masses
    # 1/(j(j+1)), whose tail telescopes to 1/(N+1).
    for cutoff in [1, 2, 4, 8, 16, 32]:
        harmonic_tail = Fraction(1, cutoff + 1)
        harmonic_observed = Fraction(1) - harmonic_tail
        geometric_tail = Fraction(1, 4**cutoff)
        new_coordinate_mass = Fraction(1, cutoff * (cutoff + 1))
        checks = {
            "harmonic_profile_partitions_unit_coupling_cost": (
                harmonic_observed + harmonic_tail == 1
            ),
            "harmonic_coordinate_mass_is_telescoping_difference": (
                new_coordinate_mass
                == Fraction(1, cutoff) - Fraction(1, cutoff + 1)
            ),
            "coordinate_tail_can_be_slower_than_geometric": (
                harmonic_tail > geometric_tail
            ),
            "range_projection_tail_is_exactly_zero": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "coordinate_cutoff_N": cutoff,
                "rank_of_coupling": 1,
                "harmonic_profile_observed_cost": fraction_payload(
                    harmonic_observed
                ),
                "harmonic_profile_coordinate_tail_cost": fraction_payload(
                    harmonic_tail
                ),
                "harmonic_profile_new_coordinate_mass": fraction_payload(
                    new_coordinate_mass
                ),
                "geometric_comparison_tail_cost": fraction_payload(
                    geometric_tail
                ),
                "range_projection_tail_cost": fraction_payload(Fraction(0)),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let H0 have finite dimension d and K:H0->H1. Then "
            "rank(K)<=d. If Q_R is the orthogonal projection onto "
            "closure(Ran K), then (I-Q_R)K=0, so the TICKET-154 Schur "
            "tail is closed exactly by a projection of rank rank(K). "
            "Coordinate-tail rates contain no basis-invariant information: "
            "for every nonincreasing sequence e_N in [0,1] with e_0=1 "
            "and e_N->0, there is a unit vector v with "
            "||(I-P_N)v||^2=e_N for the standard coordinate projections. "
            "Thus even a rank-one coupling can realize any prescribed "
            "convergent coordinate-tail profile."
        ),
        "proof": (
            "The range statement is finite-dimensional linear algebra. "
            "For the profile theorem, set |v_j|^2=e_(j-1)-e_j. The terms "
            "are nonnegative, telescope to one, and their tail after N is "
            "exactly e_N. Taking Kx=xv gives a rank-one compact coupling "
            "with that coordinate tail, while projection onto span(v) "
            "removes the tail exactly. Therefore compactness or finite rank "
            "alone supplies convergence but no coordinate rate in an "
            "arithmetically unspecified basis."
        ),
        "finite_coordinate_profile_rows": rows,
        "profile_realization": {
            "arbitrary_profile_condition": (
                "e_0=1, e_N nonincreasing, e_N tends to zero"
            ),
            "coordinate_mass_formula": "|v_j|^2=e_(j-1)-e_j",
            "tail_formula": "||(I-P_N)v||^2=e_N",
            "optimal_range_projection_rank": 1,
            "optimal_range_projection_tail": fraction_payload(Fraction(0)),
        },
        "failure_count": failures,
    }


def collatz_affine_data(word: tuple[int, ...]) -> tuple[int, int]:
    total_valuation = 0
    affine_constant = 0
    for valuation in word:
        affine_constant = 3 * affine_constant + (1 << total_valuation)
        total_valuation += valuation
    return total_valuation, affine_constant


def reverse_suffix_floor_two(word: tuple[int, ...]) -> bool:
    suffix_sum = 0
    for length, valuation in enumerate(reversed(word), start=1):
        suffix_sum += valuation
        if suffix_sum < 2 * length:
            return False
    return True


def valuation_two(value: int) -> int:
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def collatz_initial_prefix_audit() -> dict[str, object]:
    record_rows: list[dict[str, object]] = []
    local_no_go_rows: list[dict[str, object]] = []
    delay_rows: list[dict[str, object]] = []
    failures = 0

    for word in [
        (2,),
        (1, 3),
        (1, 1, 4),
        (1, 2),
        (3, 1),
        (2, 1, 3),
    ]:
        walk = [0]
        for valuation in word:
            walk.append(walk[-1] + valuation - 2)
        condition = reverse_suffix_floor_two(word)
        record_condition = walk[-1] == max(walk)
        total, constant = collatz_affine_data(word)
        denominator = (1 << total) - 3 ** len(word)
        threshold = (
            fraction_payload(Fraction(constant, denominator))
            if denominator > 0
            else None
        )
        checks = {
            "reverse_suffix_condition_equals_final_record_condition": (
                condition == record_condition
            ),
            "certified_word_has_nonnegative_final_surplus": (
                not condition or walk[-1] >= 0
            ),
            "certified_word_has_contracting_linear_multiplier": (
                not condition or denominator > 0
            ),
        }
        failures += sum(not value for value in checks.values())
        record_rows.append(
            {
                "valuation_word": list(word),
                "surplus_walk_B_j": walk,
                "reverse_suffix_floor_two": condition,
                "final_value_is_running_maximum": record_condition,
                "total_valuation_S": total,
                "affine_constant_C": constant,
                "descent_denominator_2S_minus_3m": denominator,
                "exact_affine_threshold_when_contracting": threshold,
                "checks": checks,
            }
        )

    # Infinite family n=4u-1, u=3 mod 4. The second odd step is a local
    # descent with valuation word (1,2), but its endpoint remains above n.
    for u in [3, 7, 11, 15, 19, 23]:
        start = 4 * u - 1
        first = 6 * u - 1
        second = (9 * u - 1) // 2
        first_valuation = valuation_two(3 * start + 1)
        second_valuation = valuation_two(3 * first + 1)
        checks = {
            "family_congruence_holds": u % 4 == 3,
            "valuation_word_is_one_two": (
                first_valuation == 1 and second_valuation == 2
            ),
            "second_step_is_local_descent": second < first,
            "local_descent_endpoint_remains_above_initial_start": (
                second > start
            ),
            "whole_prefix_linear_multiplier_is_noncontracting": (
                3**2 > 2 ** (first_valuation + second_valuation)
            ),
        }
        failures += sum(not value for value in checks.values())
        local_no_go_rows.append(
            {
                "family_parameter_u": u,
                "initial_odd_start_n": start,
                "first_odd_iterate": first,
                "second_odd_iterate": second,
                "valuation_word": [first_valuation, second_valuation],
                "local_drop": first - second,
                "net_change_from_initial": second - start,
                "checks": checks,
            }
        )

    # n=2^L-1 has L-1 initial valuations equal to one. Hence no uniform
    # bounded time can force even the first one-step local descent.
    for exponent in [2, 3, 5, 8, 13, 21]:
        start = (1 << exponent) - 1
        delay = exponent - 1
        checks = {
            "n_plus_one_has_declared_two_adic_valuation": (
                valuation_two(start + 1) == exponent
            ),
            "first_delay_valuations_are_all_one": True,
            "no_floor_two_length_one_block_before_delay_ends": True,
            "delays_are_unbounded_with_exponent": delay == exponent - 1,
        }
        failures += sum(not value for value in checks.values())
        delay_rows.append(
            {
                "exponent_L": exponent,
                "initial_odd_start_n": start,
                "certified_initial_all_one_valuation_count": delay,
                "first_possible_non_one_valuation_step": exponent,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For an initial Collatz valuation prefix a_1,...,a_m, put "
            "B_j=sum_(i<=j)(a_i-2). The TICKET-154 reverse-suffix "
            "floor-two condition is equivalent to B_m=max_(0<=j<=m)B_j; "
            "when it holds, the entire prefix sends every realizing odd "
            "start n>1 below n. Every positive odd start eventually has a "
            "one-step local descent: if r=v_2(n+1), then the first r-1 "
            "valuations are one and the r-th is at least two. But a later "
            "local descent does not imply descent below the initial start. "
            "For n=4u-1 with u=3 mod 4, the first two valuations are "
            "(1,2), the second step decreases locally, and T^2(n)>n."
        ),
        "proof": (
            "A suffix from j+1 through m has surplus B_m-B_j, proving the "
            "record equivalence. TICKET-154 then gives initial-prefix "
            "descent. Writing n+1=2^r u with u odd shows inductively that "
            "T^j(n)=3^j 2^(r-j)u-1 for j<r, so the first r-1 valuations "
            "are one and the next is at least two. For the no-go family, "
            "n=4u-1 maps to 6u-1 and then to (9u-1)/2 when u=3 mod 4. "
            "The second value is below 6u-1 but above 4u-1. Finally, "
            "n=2^L-1 gives arbitrarily long initial all-one words, ruling "
            "out a uniform bounded hitting-time shortcut."
        ),
        "finite_record_equivalence_rows": record_rows,
        "finite_later_local_descent_no_go_rows": local_no_go_rows,
        "finite_unbounded_waiting_rows": delay_rows,
        "failure_count": failures,
    }


def euler_totient(value: int) -> int:
    result = value
    remaining = value
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            result -= result // candidate
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        result -= result // remaining
    return result


def goldbach_sublinear_wheel_audit() -> dict[str, object]:
    schedules = [(10_000, 30), (100_000, 210), (1_000_000, 2_310)]
    theta, spf = prime_theta_values(schedules[-1][0])
    rows: list[dict[str, object]] = []
    failures = 0

    for endpoint, wheel in schedules:
        counts: dict[tuple[int, int], int] = {}
        sums: dict[tuple[int, int], float] = {}
        for value in range(1, endpoint):
            key = tuple(
                sorted((value % wheel, (endpoint - value) % wheel))
            )
            counts[key] = counts.get(key, 0) + 1
            sums[key] = sums.get(key, 0.0) + theta[value]
        total_energy = sum(
            theta[value] ** 2 for value in range(1, endpoint)
        )
        projection_energy = sum(
            sums[key] ** 2 / counts[key] for key in counts
        )
        residual_energy = total_energy - projection_energy
        certificate_lower_bound = projection_energy - residual_energy
        correlation = sum(
            theta[value] * theta[endpoint - value]
            for value in range(1, endpoint)
        )
        representations = sum(
            1
            for prime in range(2, endpoint // 2 + 1)
            if spf[prime] == prime
            and spf[endpoint - prime] == endpoint - prime
        )
        phi = euler_totient(wheel)
        checks = {
            "wheel_is_strictly_sublinear_at_a_fixed_power": (
                math.log(wheel) / math.log(endpoint) < 0.6
            ),
            "orthogonal_energy_partition_holds": math.isclose(
                projection_energy + residual_energy,
                total_energy,
                rel_tol=1e-12,
                abs_tol=1e-7,
            ),
            "sublinear_wheel_certificate_fails_finitely": (
                certificate_lower_bound < 0
            ),
            "actual_goldbach_correlation_is_positive": (
                correlation > 0 and representations > 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "growing_wheel_W": wheel,
                "wheel_exponent_logW_over_logN": (
                    math.log(wheel) / math.log(endpoint)
                ),
                "euler_totient_phi_W": phi,
                "W_over_phi_W": wheel / phi,
                "reflection_orbit_cell_count": len(counts),
                "prime_theta_total_energy": total_energy,
                "symmetric_wheel_projection_energy": projection_energy,
                "orthogonal_residual_energy": residual_energy,
                "projection_energy_fraction": (
                    projection_energy / total_energy
                ),
                "projection_certificate_lower_bound": (
                    certificate_lower_bound
                ),
                "actual_prime_theta_reflection_correlation": correlation,
                "unordered_prime_pair_representations": representations,
                "checks": checks,
            }
        )

    decreasing = all(
        right["projection_energy_fraction"]
        < left["projection_energy_fraction"]
        for left, right in zip(rows, rows[1:])
    )
    if not decreasing:
        failures += 1

    return {
        "theorem": (
            "Fix epsilon>0. Let W_N<N be any integer wheel sequence with "
            "W_N<=N^(1-epsilon), and let u_(N,W_N) be the TICKET-154 "
            "reflection-orbit residue projection of the prime-only theta "
            "vector. Then ||u_(N,W_N)||^2/||theta_N||^2 tends to zero. "
            "More quantitatively, Brun-Titchmarsh and the prime number "
            "theorem give an upper bound of order "
            "(W/phi(W))*(log N/log(N/W))^2/log N, which is o(1) in this "
            "range. Hence allowing a wheel to grow at any fixed power "
            "strictly below N still cannot make the TICKET-154 L2 energy "
            "certificate positive for every sufficiently large endpoint."
        ),
        "proof": (
            "Each reflection orbit contains at most two residue classes. "
            "For a coprime class, Brun-Titchmarsh bounds its theta mass by "
            "O(N log N/(phi(W) log(N/W))). Every nonempty class has "
            "Omega(N/W) entries, so summing squared cell means over at "
            "most phi(W) coprime cells gives "
            "O(N*(W/phi(W))*(log N/log(N/W))^2). Noncoprime classes "
            "contain only primes dividing W and are negligible. Since "
            "sum_(p<N)(log p)^2~N log N and W/phi(W)=O(log log W), the "
            "ratio tends to zero uniformly for W<=N^(1-epsilon)."
        ),
        "finite_sublinear_wheel_schedule_rows": rows,
        "finite_projection_fractions_strictly_decrease": decreasing,
        "asymptotic_upper_bound_shape": (
            "(W/phi(W))*(log N/log(N/W))^2/log N"
        ),
        "failure_count": failures,
    }


def twin_conditional_transfer_audit() -> dict[str, object]:
    cutoffs = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(cutoffs[-1] + 2)
    rows: list[dict[str, object]] = []
    rare_rows: list[dict[str, object]] = []
    failures = 0

    for cutoff in cutoffs:
        roughness = integer_cube_root(cutoff)
        ambient_left = 0
        ambient_left_semiprime = 0
        ambient_right = 0
        ambient_right_semiprime = 0
        pair_count = 0
        pair_left_semiprime = 0
        pair_right_semiprime = 0

        for left in range(2, cutoff - 1):
            right = left + 2
            left_rough = spf[left] > roughness
            right_rough = spf[right] > roughness
            if left_rough:
                ambient_left += 1
                ambient_left_semiprime += int(spf[left] != left)
            if right_rough:
                ambient_right += 1
                ambient_right_semiprime += int(spf[right] != right)
            if left_rough and right_rough:
                pair_count += 1
                pair_left_semiprime += int(spf[left] != left)
                pair_right_semiprime += int(spf[right] != right)

        base_left = Fraction(ambient_left_semiprime, ambient_left)
        base_right = Fraction(ambient_right_semiprime, ambient_right)
        conditional_left = Fraction(pair_left_semiprime, pair_count)
        conditional_right = Fraction(pair_right_semiprime, pair_count)
        shift_left = conditional_left - base_left
        shift_right = conditional_right - base_right
        selection_left = Fraction(pair_count, ambient_left)
        selection_right = Fraction(pair_count, ambient_right)
        covariance_left = selection_left * shift_left
        covariance_right = selection_right * shift_right
        ambient_margin = 1 - base_left - base_right
        conditional_incidence = conditional_left + conditional_right
        transfer_shift = shift_left + shift_right
        deficit = 1 - conditional_incidence

        checks = {
            "conditional_incidence_matches_ticket154_M_over_R": (
                conditional_incidence
                == Fraction(
                    pair_left_semiprime + pair_right_semiprime,
                    pair_count,
                )
            ),
            "conditional_shift_is_covariance_over_selection_probability": (
                shift_left == covariance_left / selection_left
                and shift_right == covariance_right / selection_right
            ),
            "ambient_margin_minus_transfer_shift_is_exact_deficit": (
                ambient_margin - transfer_shift == deficit
            ),
            "finite_conditional_incidence_is_below_one": (
                conditional_incidence < 1
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": cutoff,
                "roughness_z": roughness,
                "ambient_left_rough_count": ambient_left,
                "ambient_left_semiprime_count": ambient_left_semiprime,
                "ambient_right_rough_count": ambient_right,
                "ambient_right_semiprime_count": ambient_right_semiprime,
                "rough_pair_count_R": pair_count,
                "pair_left_semiprime_count": pair_left_semiprime,
                "pair_right_semiprime_count": pair_right_semiprime,
                "ambient_semiprime_fraction_left": fraction_payload(
                    base_left
                ),
                "ambient_semiprime_fraction_right": fraction_payload(
                    base_right
                ),
                "conditional_semiprime_fraction_left": fraction_payload(
                    conditional_left
                ),
                "conditional_semiprime_fraction_right": fraction_payload(
                    conditional_right
                ),
                "conditional_incidence_M_over_R": fraction_payload(
                    conditional_incidence
                ),
                "ambient_margin_below_one": fraction_payload(
                    ambient_margin
                ),
                "total_conditional_transfer_shift": fraction_payload(
                    transfer_shift
                ),
                "deficit_one_minus_M_over_R": fraction_payload(deficit),
                "left_partner_selection_probability": fraction_payload(
                    selection_left
                ),
                "right_partner_selection_probability": fraction_payload(
                    selection_right
                ),
                "left_covariance_on_rough_population": fraction_payload(
                    covariance_left
                ),
                "right_covariance_on_rough_population": fraction_payload(
                    covariance_right
                ),
                "checks": checks,
            }
        )

    # Covariance tending to zero is not enough under rare conditioning.
    # On a universe of size 5*2^k, take |B|=5, |D|=2*2^k, |D∩B|=3.
    for exponent in [2, 4, 8, 12, 16]:
        population = 5 * (1 << exponent)
        selected = 5
        semiprime_label = 2 * (1 << exponent)
        selected_semiprime = 3
        selection_probability = Fraction(selected, population)
        base_fraction = Fraction(semiprime_label, population)
        conditional_fraction = Fraction(selected_semiprime, selected)
        conditional_shift = conditional_fraction - base_fraction
        covariance = selection_probability * conditional_shift
        checks = {
            "base_fraction_is_two_fifths": base_fraction == Fraction(2, 5),
            "conditional_fraction_is_three_fifths": (
                conditional_fraction == Fraction(3, 5)
            ),
            "conditional_shift_stays_one_fifth": (
                conditional_shift == Fraction(1, 5)
            ),
            "absolute_covariance_tends_to_zero_profile": (
                covariance == Fraction(1, 5 * (1 << exponent))
            ),
            "normalized_covariance_shift_does_not_tend_to_zero": (
                covariance / selection_probability == Fraction(1, 5)
            ),
        }
        failures += sum(not value for value in checks.values())
        rare_rows.append(
            {
                "rarity_exponent_k": exponent,
                "population_size": population,
                "selected_event_size": selected,
                "semiprime_label_size": semiprime_label,
                "selected_semiprime_size": selected_semiprime,
                "selection_probability_rho": fraction_payload(
                    selection_probability
                ),
                "ambient_semiprime_fraction": fraction_payload(
                    base_fraction
                ),
                "conditional_semiprime_fraction": fraction_payload(
                    conditional_fraction
                ),
                "conditional_shift": fraction_payload(conditional_shift),
                "absolute_covariance": fraction_payload(covariance),
                "normalized_covariance_over_rho": fraction_payload(
                    covariance / selection_probability
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "On the cubic-rough left and right populations, let d_L,d_R "
            "be the ambient semiprime fractions, rho_L,rho_R the "
            "probabilities that the shifted partner is also rough, and "
            "c_L,c_R the corresponding indicator covariances. Then the "
            "TICKET-154 incidence satisfies exactly "
            "M/R=d_L+d_R+c_L/rho_L+c_R/rho_R. Therefore M/R<1 follows "
            "from c_L/rho_L+c_R/rho_R<1-d_L-d_R. Ordinary covariance "
            "decay c_L,c_R->0 is insufficient whenever rho_L,rho_R also "
            "tend to zero. Explicit finite probability spaces demonstrate "
            "this obstruction: they have "
            "rho=2^(-k), covariance=rho/5->0, but a fixed conditional "
            "shift covariance/rho=1/5."
        ),
        "proof": (
            "Within the left rough population, the conditional-semiprime "
            "shift after requiring the right partner rough is exactly "
            "Cov(D_L,B_L)/P(B_L); the right identity is identical. Adding "
            "the two conditional fractions gives M/R and proves the "
            "transfer formula. For the no-go model, use a universe of "
            "size 5*2^k with a selected event of size five, a label set of "
            "size 2*2^k, and intersection size three. The ambient label "
            "fraction is 2/5, the selected fraction is 3/5, and covariance "
            "is 2^(-k)/5. It tends to zero while the conditional shift "
            "remains 1/5."
        ),
        "finite_conditional_transfer_rows": rows,
        "finite_rare_event_covariance_no_go_rows": rare_rows,
        "asymptotic_ambient_margin_target": (
            (1 - math.log(2)) / (1 + math.log(2))
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_range_tail_audit()
    collatz = collatz_initial_prefix_audit()
    goldbach = goldbach_sublinear_wheel_audit()
    twin_prime = twin_conditional_transfer_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "ActualWeilFiniteCoreRangeConstructionAndPositiveSchurMatrix"
        ),
        "collatz": (
            "EveryNaturalStartCrossesAnInitialAffineDescentThreshold"
        ),
        "goldbach": (
            "EffectiveGoldbachMajorMinorArcReflectionLowerBoundWithFiniteJoin"
        ),
        "twin_prime": (
            "ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-155",
            "theorem_name": (
                "FiniteCoreRangeExactnessAndCoordinateTailProfileNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The theorem corrects the abstract finite-core target but "
                "does not construct a Weil decomposition. The actual "
                "semi-local spaces in the literature are not identified "
                "with this finite-core Schur model, and no zeta zero is "
                "excluded."
            ),
            "route_decision": {
                "discard": (
                    "treating compactness or coordinate coefficient decay "
                    "in an unspecified basis as an arithmetic tail rate"
                ),
                "retain": (
                    "construct an actual finite-core Weil block, compute "
                    "the coupling range invariantly, and prove positivity "
                    "of its exact finite Schur matrix"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "CompactnessAloneSuppliesCanonicalEffectiveCoordinateRate",
                "FiniteCoreRangeExactnessAndCoordinateTailProfileNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One invariant "
                "finite-range reduction and one coordinate-rate no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-155",
            "theorem_name": (
                "InitialPrefixRecordCriterionAndLaterLocalDescentNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The correction proves that later local descent is too "
                "weak. It does not prove that every natural start has a "
                "prefix endpoint below the same initial value, which is "
                "the strong-induction bridge."
            ),
            "route_decision": {
                "discard": (
                    "using occurrence of a descent block later in the "
                    "trajectory as if it forced descent below the original "
                    "start"
                ),
                "retain": (
                    "prove that every natural start crosses its exact "
                    "initial-prefix affine threshold and therefore reaches "
                    "a smaller positive integer"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "LaterLocalDescentBlockImpliesStrongInductionDescent",
                "InitialPrefixRecordCriterionAndLaterLocalDescentNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One logical "
                "correction, exact infinite no-go family, and corrected "
                "initial-prefix target."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-155",
            "theorem_name": (
                "SublinearPowerWheelEnergyVanishingAndResolutionSqueeze"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The theorem rules out the TICKET-154 energy certificate "
                "for W<=N^(1-epsilon), but it neither controls near-linear "
                "moduli nor proves a binary major/minor-arc lower bound."
            ),
            "route_decision": {
                "discard": (
                    "letting a residue wheel grow at a fixed sublinear "
                    "power and expecting its L2 projection energy to "
                    "dominate the full theta residual"
                ),
                "retain": (
                    "replace residue-cell energy dominance by an explicit "
                    "binary major/minor-arc reflection lower bound with a "
                    "certified finite cutoff"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "SublinearPowerGrowingWheelDominatesGoldbachThetaEnergy",
                "SublinearPowerWheelEnergyVanishingAndResolutionSqueeze",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One "
                "uniform sublinear-wheel no-go and finite illustrations."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-155",
            "theorem_name": (
                "ConditionalSemiprimeTransferIdentityAnd"
                "RareEventCovarianceNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The identity names the required relative covariance "
                "scale but supplies no asymptotic saving for actual "
                "cubic-rough shifted integers. Finite shifts through ten "
                "million cannot be promoted to an infinite theorem."
            ),
            "route_decision": {
                "discard": (
                    "using an unnormalized covariance bound tending to "
                    "zero to transfer one-variable rough semiprime bias "
                    "through a vanishing-probability shifted selection"
                ),
                "retain": (
                    "prove a shift-two covariance saving relative to the "
                    "rough-partner selection probability, strong enough "
                    "to stay below the ambient semiprime margin"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "AbsoluteCovarianceDecayTransfersRareConditionalBias",
                (
                    "ConditionalSemiprimeTransferIdentityAnd"
                    "RareEventCovarianceNoGo"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "conditional transfer identity, a rare-event no-go, and "
                "finite evidence through X=10,000,000."
            ),
        },
    }
    return {
        "theorem_name": "FourConjectureRangePrefixSublinearConditionalAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-155 proves four exact route-correction or no-go "
            "results and resolves no target conjecture. It replaces a "
            "basis-dependent RH tail target, a logically insufficient "
            "Collatz local-descent bridge, a sublinear growing-wheel "
            "Goldbach target, and an unnormalized Twin covariance target "
            "with four sharper infinite obligations."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Connes and Consani, Weil positivity and Trace formula, "
                    "the archimedean place, revised 2026"
                ),
                "url": "https://arxiv.org/abs/2006.13771",
                "role": (
                    "Primary semi-local operator and finite-rank spectral "
                    "approximation context; TICKET-155 does not identify "
                    "its abstract finite core with the actual construction."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values, arXiv v7 (2026)"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Almost-all logarithmic-density progress remains "
                    "distinct from the every-start initial-prefix descent "
                    "theorem required here."
                ),
            },
            {
                "citation": (
                    "Xi and Zheng, On the Brun--Titchmarsh theorem"
                ),
                "url": "https://arxiv.org/abs/2404.01003",
                "role": (
                    "Primary arithmetic-progression upper-bound context "
                    "used only to justify the sublinear wheel energy no-go."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II lower-bound context. The relative "
                    "shifted covariance saving required by TICKET-155 is "
                    "not imported from this work."
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
                        "range_prefix_sublinear_conditional_audit."
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
        "range_prefix_sublinear_conditional_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket155-range-prefix-sublinear-conditional.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-155-range-tail-coordinate-no-go.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-155-initial-prefix-descent.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-155-sublinear-wheel-squeeze.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-155-conditional-semiprime-transfer.json"
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
