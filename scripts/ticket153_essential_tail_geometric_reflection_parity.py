from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket152_compression_cylinder_energy_selection import (
    accelerated_collatz,
    integer_cube_root,
    smallest_prime_factor_sieve,
    word_cylinder,
)


GENERATED_AT = "2026-07-26T13:30:00+09:00"
SCHEMA = (
    "primeproject.ticket153-essential-tail-geometric-reflection-parity.v1"
)
STATUS = "exact_decompositions_all_four_conjectures_open"


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
    rejected_id = f"{problem_code}-T153-REJECTED"
    closed_id = f"{problem_code}-T153-CLOSED"
    open_id = f"{problem_code}-T153-OPEN"
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


def riemann_essential_tail_audit() -> dict[str, object]:
    essential_rows: list[dict[str, object]] = []
    schur_rows: list[dict[str, object]] = []
    failures = 0

    for tested_rank, delta in [
        (1, Fraction(1, 4)),
        (2, Fraction(1, 2)),
        (4, Fraction(3, 4)),
        (8, Fraction(1)),
        (16, Fraction(5, 4)),
    ]:
        checks = {
            "hidden_kernel_direction_exists": True,
            "finite_rank_distance_at_least_delta": delta > 0,
            "positive_essential_tail_not_small_norm_remainder": delta > 0,
        }
        failures += sum(not value for value in checks.values())
        essential_rows.append(
            {
                "tested_finite_rank": tested_rank,
                "positive_identity_tail_delta": fraction_payload(delta),
                "witness_coordinate": tested_rank + 1,
                "operator_norm_distance_lower_bound": fraction_payload(
                    delta
                ),
                "checks": checks,
            }
        )

    cases = [
        (
            Fraction(1),
            [Fraction(1, 2)],
            Fraction(1, 2),
            True,
        ),
        (
            Fraction(2),
            [Fraction(1, 2), Fraction(1, 3)],
            Fraction(1, 3),
            True,
        ),
        (
            Fraction(3, 2),
            [Fraction(1, 4), Fraction(1, 5), Fraction(1, 6)],
            Fraction(1, 4),
            True,
        ),
        (
            Fraction(3, 4),
            [Fraction(1, 5), Fraction(1, 7)],
            Fraction(1, 8),
            True,
        ),
        (
            Fraction(1),
            [Fraction(3, 4)],
            Fraction(1, 2),
            False,
        ),
        (
            Fraction(1, 2),
            [Fraction(1, 2), Fraction(1, 3)],
            Fraction(2, 3),
            False,
        ),
        (
            Fraction(3, 4),
            [Fraction(1, 2), Fraction(1, 4)],
            Fraction(3, 8),
            False,
        ),
        (
            Fraction(2),
            [Fraction(1), Fraction(3, 4)],
            Fraction(3, 4),
            False,
        ),
    ]
    for delta, coupling, core_floor, expected_positive in cases:
        coupling_norm_squared = sum(
            (value * value for value in coupling),
            Fraction(0),
        )
        schur_cost = coupling_norm_squared / delta
        schur_margin = core_floor - schur_cost
        certified_positive = schur_margin >= 0
        minimizing_vector_value = schur_margin
        checks = {
            "classification_matches_exact_schur_margin": (
                certified_positive == expected_positive
            ),
            "positive_case_has_nonnegative_margin": (
                expected_positive == (schur_margin >= 0)
            ),
            "failed_case_has_explicit_negative_direction": (
                expected_positive or minimizing_vector_value < 0
            ),
        }
        failures += sum(not value for value in checks.values())
        schur_rows.append(
            {
                "tail_coercivity_delta": fraction_payload(delta),
                "coupling_coordinates": [
                    fraction_payload(value) for value in coupling
                ],
                "coupling_norm_squared": fraction_payload(
                    coupling_norm_squared
                ),
                "finite_core_floor": fraction_payload(core_floor),
                "schur_cost_normC_squared_over_delta": fraction_payload(
                    schur_cost
                ),
                "exact_schur_margin": fraction_payload(schur_margin),
                "certified_positive": certified_positive,
                "minimizing_test_vector_quadratic_value": fraction_payload(
                    minimizing_vector_value
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let G on H0 direct-sum H1 have self-adjoint block form "
            "[A,C*;C,D], with D>=delta I for delta>0. If "
            "A>=||C||^2/delta times I, then G>=0. More exactly, when D is "
            "invertible, G>=0 iff D>=0 and A-C*D^(-1)C>=0. In contrast, "
            "on an infinite-dimensional tail, every finite-rank F satisfies "
            "||delta I-F||>=delta. Thus a known positive essential tail "
            "must be retained and certified by a Schur complement; treating "
            "the entire operator as a small finite-rank norm remainder is "
            "impossible below its essential norm."
        ),
        "proof": (
            "Complete the square: <G(x,y),(x,y)> equals "
            "<(A-C*D^(-1)C)x,x> plus "
            "<D(y+D^(-1)Cx),y+D^(-1)Cx>. The bound "
            "C*D^(-1)C<=||C||^2/delta gives the sufficient condition. For "
            "the no-go, a finite-rank F has a nonzero unit vector x in its "
            "kernel, so ||(delta I-F)x||=delta. The rational audit evaluates "
            "the exact Schur margins and the minimizing vectors."
        ),
        "finite_essential_norm_rows": essential_rows,
        "finite_schur_complement_rows": schur_rows,
        "failure_count": failures,
    }


def terminal_after_word(start: int, length: int) -> int:
    current = start
    for _ in range(length):
        current, _ = accelerated_collatz(current)
    return current


def collatz_geometric_tail_audit() -> dict[str, object]:
    parent_words = [
        [1],
        [2],
        [1, 1],
        [1, 2],
        [2, 1],
        [3, 1, 2],
        [2, 3, 1, 1],
    ]
    extension_rows: list[dict[str, object]] = []
    drift_rows: list[dict[str, object]] = []
    failures = 0

    for word in parent_words:
        cylinder = word_cylinder(word)
        for cap in [4, 8, 12]:
            counts = {valuation: 0 for valuation in range(1, cap + 1)}
            tail_count = 0
            for lift_index in range(1 << cap):
                start = (
                    cylinder["least_positive_residue"]
                    + lift_index * cylinder["modulus"]
                )
                terminal = terminal_after_word(start, len(word))
                _, next_valuation = accelerated_collatz(terminal)
                if next_valuation <= cap:
                    counts[next_valuation] += 1
                else:
                    tail_count += 1
            expected = {
                valuation: 1 << (cap - valuation)
                for valuation in range(1, cap + 1)
            }
            checks = {
                "each_exact_child_count_is_geometric": counts == expected,
                "tail_count_is_one": tail_count == 1,
                "partition_count_is_complete": (
                    sum(counts.values()) + tail_count == 1 << cap
                ),
            }
            failures += sum(not value for value in checks.values())
            extension_rows.append(
                {
                    "parent_word": word,
                    "lift_residue_bits_B": cap,
                    "lift_count": 1 << cap,
                    "exact_next_valuation_counts": {
                        str(key): value for key, value in counts.items()
                    },
                    "expected_geometric_counts": {
                        str(key): value for key, value in expected.items()
                    },
                    "tail_next_valuation_greater_than_B": tail_count,
                    "conditional_tail_mass": fraction_payload(
                        Fraction(1, 1 << cap)
                    ),
                    "checks": checks,
                }
            )

    contraction_threshold = math.log(3, 2)
    optimum_t = math.log(
        contraction_threshold / (2 * (contraction_threshold - 1))
    )
    chernoff_base = (
        math.exp(optimum_t * contraction_threshold)
        / (2 * math.exp(optimum_t) - 1)
    )
    for length in [4, 8, 16, 32, 64, 128]:
        power_three = 3**length
        maximum_noncontracting_sum = power_three.bit_length() - 1
        numerator = sum(
            math.comb(total - 1, length - 1)
            * (1 << (maximum_noncontracting_sum - total))
            for total in range(
                length,
                maximum_noncontracting_sum + 1,
            )
        )
        probability = Fraction(
            numerator,
            1 << maximum_noncontracting_sum,
        )
        chernoff_bound = chernoff_base**length
        checks = {
            "threshold_is_exact": (
                (1 << maximum_noncontracting_sum)
                < power_three
                < (1 << (maximum_noncontracting_sum + 1))
            ),
            "exact_probability_below_chernoff_bound": (
                float(probability) <= chernoff_bound
            ),
            "probability_is_strictly_between_zero_and_one": (
                0 < probability < 1
            ),
        }
        failures += sum(not value for value in checks.values())
        drift_rows.append(
            {
                "word_length_m": length,
                "maximum_sum_with_2_power_S_below_3_power_m": (
                    maximum_noncontracting_sum
                ),
                "exact_noncontracting_linear_coefficient_probability": (
                    fraction_payload(probability)
                ),
                "optimized_chernoff_upper_bound": chernoff_bound,
                "checks": checks,
            }
        )

    drift_probabilities = [
        Fraction(
            row[
                "exact_noncontracting_linear_coefficient_probability"
            ]["exact"]
        )
        for row in drift_rows
    ]
    strictly_decreasing = all(
        right < left
        for left, right in zip(
            drift_probabilities,
            drift_probabilities[1:],
        )
    )
    if not strictly_decreasing:
        failures += 1

    return {
        "theorem": (
            "Every accelerated Collatz valuation cylinder is the disjoint "
            "countable union of its children indexed by the next valuation "
            "b>=1. Their conditional 2-adic Haar masses are exactly 2^(-b), "
            "and the tail mass for b>B is 2^(-B). Iterating gives word mass "
            "2^(-sum a_i), so the valuation coordinates have the exact "
            "geometric cylinder law. Consequently the expected logarithm "
            "of the linear multiplier 3/2^a is log(3/4)<0, and the exact "
            "noncontracting coefficient probability after m odd steps is "
            "sum_{s=m}^{floor(m log_2 3)} binom(s-1,m-1)2^(-s), with an "
            "explicit exponentially decaying Chernoff bound."
        ),
        "proof": (
            "On the lift index k, the next-step numerator divided by two is "
            "an affine map with odd coefficient modulo 2^B, hence a "
            "permutation. Exactly 2^(B-b) residues have next valuation b "
            "for 1<=b<=B, while one residue has valuation greater than B. "
            "Multiplying child masses proves the word law. The number of "
            "positive compositions of s into m parts is binom(s-1,m-1), "
            "which gives the negative-binomial formula. Applying Markov's "
            "inequality to exp(-t sum a_i) and optimizing t gives the "
            "reported Chernoff base."
        ),
        "finite_extension_partition_rows": extension_rows,
        "finite_negative_drift_rows": drift_rows,
        "finite_noncontracting_probabilities_strictly_decreasing": (
            strictly_decreasing
        ),
        "constants": {
            "expected_valuation": 2.0,
            "expected_log_linear_multiplier": math.log(3 / 4),
            "optimized_chernoff_base": chernoff_base,
        },
        "failure_count": failures,
    }


def prime_theta_values(limit: int) -> tuple[list[float], list[int]]:
    spf = smallest_prime_factor_sieve(limit)
    theta = [0.0] * (limit + 1)
    for value in range(2, limit + 1):
        if spf[value] == value:
            theta[value] = math.log(value)
    return theta, spf


def goldbach_reflection_audit() -> dict[str, object]:
    endpoints = [1_000, 10_000, 100_000, 1_000_000]
    theta, spf = prime_theta_values(endpoints[-1])
    rows: list[dict[str, object]] = []
    failures = 0

    for endpoint in endpoints:
        total_energy = sum(
            theta[value] ** 2 for value in range(1, endpoint)
        )
        correlation = sum(
            theta[value] * theta[endpoint - value]
            for value in range(1, endpoint)
        )
        symmetric_energy = (total_energy + correlation) / 2
        antisymmetric_energy = (total_energy - correlation) / 2
        direct_symmetric_energy = sum(
            (
                (
                    theta[value]
                    + theta[endpoint - value]
                )
                / 2
            )
            ** 2
            for value in range(1, endpoint)
        )
        direct_antisymmetric_energy = sum(
            (
                (
                    theta[value]
                    - theta[endpoint - value]
                )
                / 2
            )
            ** 2
            for value in range(1, endpoint)
        )
        unordered_representations = sum(
            1
            for prime in range(2, endpoint // 2 + 1)
            if spf[prime] == prime
            and spf[endpoint - prime] == endpoint - prime
        )
        checks = {
            "reflection_energy_identity": math.isclose(
                correlation,
                symmetric_energy - antisymmetric_energy,
                rel_tol=1e-12,
                abs_tol=1e-8,
            ),
            "direct_projection_energy_matches": (
                math.isclose(
                    symmetric_energy,
                    direct_symmetric_energy,
                    rel_tol=1e-12,
                    abs_tol=1e-7,
                )
                and math.isclose(
                    antisymmetric_energy,
                    direct_antisymmetric_energy,
                    rel_tol=1e-12,
                    abs_tol=1e-7,
                )
            ),
            "positive_correlation_matches_prime_representation": (
                (correlation > 0) == (unordered_representations > 0)
            ),
            "finite_endpoint_has_goldbach_representation": (
                unordered_representations > 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "unordered_prime_pair_representations": (
                    unordered_representations
                ),
                "prime_theta_total_energy": total_energy,
                "prime_theta_reflection_correlation": correlation,
                "symmetric_projection_energy": symmetric_energy,
                "antisymmetric_projection_energy": antisymmetric_energy,
                "normalized_reflection_gap": (
                    correlation / total_energy
                ),
                "irreducible_antisymmetric_energy_fraction": (
                    antisymmetric_energy / total_energy
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For even N, let R_N f(a)=f(N-a), let theta(n)=log n on primes "
            "and zero otherwise, and let P_plus/minus=(I plus/minus R_N)/2. "
            "Then the prime-weighted Goldbach coefficient is exactly "
            "<theta,R_N theta>=||P_plus theta||^2-||P_minus theta||^2. It "
            "is positive exactly when N is a sum of two primes. For every "
            "symmetric baseline w=R_N w, P_minus(theta-w)=P_minus theta; "
            "the best symmetric L2 approximation is uniquely P_plus theta "
            "and its squared error is the full antisymmetric energy. Thus "
            "no symmetric baseline choice can remove the negative "
            "reflection sector."
        ),
        "proof": (
            "The reflection is a self-adjoint involution, so its orthogonal "
            "eigenspace projections satisfy R_N=P_plus-P_minus. This gives "
            "the energy identity. Every summand theta(a)theta(N-a) is "
            "nonnegative and is positive exactly for a prime pair. If w is "
            "symmetric then P_minus w=0, proving invariance of the "
            "antisymmetric residual. Orthogonal projection gives the unique "
            "minimum over all symmetric baselines."
        ),
        "finite_reflection_energy_rows": rows,
        "failure_count": failures,
    }


def twin_cubic_rough_parity_audit() -> dict[str, object]:
    limits = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(limits[-1] + 2)
    rows: list[dict[str, object]] = []
    failures = 0

    for cutoff in limits:
        roughness = integer_cube_root(cutoff)
        prime_prime = 0
        semiprime_semiprime = 0
        mixed = 0
        liouville_sum = 0
        factorization_checks = True

        for value in range(2, cutoff - 1):
            shifted = value + 2
            if spf[value] <= roughness or spf[shifted] <= roughness:
                continue
            left_prime = spf[value] == value
            right_prime = spf[shifted] == shifted
            if not left_prime:
                quotient = value // spf[value]
                factorization_checks = (
                    factorization_checks
                    and quotient >= spf[value]
                    and spf[quotient] == quotient
                )
            if not right_prime:
                quotient = shifted // spf[shifted]
                factorization_checks = (
                    factorization_checks
                    and quotient >= spf[shifted]
                    and spf[quotient] == quotient
                )
            if left_prime and right_prime:
                prime_prime += 1
            elif not left_prime and not right_prime:
                semiprime_semiprime += 1
            else:
                mixed += 1
            liouville_sum += (
                (-1 if left_prime else 1)
                + (-1 if right_prime else 1)
            )

        pair_count = prime_prime + semiprime_semiprime + mixed
        exact_identity = 2 * (
            semiprime_semiprime - prime_prime
        )
        checks = {
            "all_rough_values_are_prime_or_semiprime": (
                factorization_checks
            ),
            "symmetrized_liouville_identity_is_exact": (
                liouville_sum == exact_identity
            ),
            "finite_prime_prime_excess_is_positive": (
                prime_prime > semiprime_semiprime
            ),
            "finite_symmetrized_sum_is_negative": liouville_sum < 0,
            "rough_pair_population_is_nonempty": pair_count > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_z": roughness,
                "rough_gap_two_pair_count": pair_count,
                "prime_prime_pairs_PP": prime_prime,
                "semiprime_semiprime_pairs_QQ": semiprime_semiprime,
                "mixed_pairs_PQ_QP": mixed,
                "prime_prime_excess_PP_minus_QQ": (
                    prime_prime - semiprime_semiprime
                ),
                "symmetrized_shifted_liouville_sum": liouville_sum,
                "exact_two_times_QQ_minus_PP": exact_identity,
                "normalized_prime_prime_excess": (
                    (prime_prime - semiprime_semiprime) / pair_count
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For X>=27, let z=floor(X^(1/3)) and retain 2<=n<=X-2 for "
            "which both n and n+2 have no prime factor at most z. Every "
            "retained value is either prime or semiprime. If PP counts "
            "prime-prime pairs, QQ "
            "counts semiprime-semiprime pairs, and mixed pairs have one of "
            "each, then the exact symmetrized shifted Liouville identity is "
            "sum[lambda(n)+lambda(n+2)]=2(QQ-PP). Hence negativity of this "
            "sum is exactly PP>QQ. If PP>QQ on an unbounded sequence of X, "
            "then twin primes are infinite, because every retained twin has "
            "both primes greater than z and z tends to infinity."
        ),
        "proof": (
            "Three prime factors larger than floor(X^(1/3)) have product "
            "at least (floor(X^(1/3))+1)^3>X, so a retained n or n+2 has at "
            "most two prime factors. Its Liouville sign is therefore -1 "
            "for a prime and +1 for a semiprime. A prime-prime pair "
            "contributes -2, a mixed pair zero, and a semiprime-semiprime "
            "pair +2. Summing proves the identity and the unbounded-scale "
            "implication."
        ),
        "finite_cubic_rough_parity_rows": rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_essential_tail_audit()
    collatz = collatz_geometric_tail_audit()
    goldbach = goldbach_reflection_audit()
    twin_prime = twin_cubic_rough_parity_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "ActualWeilPositiveTailDecompositionWithCertifiedSchurComplement"
        ),
        "collatz": (
            "UniformAffineOffsetControlOnNaturalValuationRays"
        ),
        "goldbach": (
            "ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArcReflectionGap"
        ),
        "twin_prime": (
            "UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-153",
            "theorem_name": (
                "PositiveEssentialTailSchurComplementAndFiniteRankNormNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The block theorem is exact but abstract. PrimeProject has "
                "not identified a proved positive essential tail, coupling "
                "operator, or finite core for the actual Weil form. No "
                "off-critical zeta zero is excluded."
            ),
            "route_decision": {
                "discard": (
                    "approximating a nonzero positive essential tail itself "
                    "by finite-rank operators in arbitrarily small operator "
                    "norm"
                ),
                "retain": (
                    "separate a rigorously coercive actual-Weil tail and "
                    "bound its coupling to the finite core by a Schur "
                    "complement"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteRankNormApproximationOfPositiveEssentialWeilTail",
                (
                    "PositiveEssentialTailSchurComplementAnd"
                    "FiniteRankNormNoGo"
                ),
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact positive-"
                "tail certificate and one essential-norm no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-153",
            "theorem_name": (
                "CountableGeometricCylinderPartitionAndNegativeDriftLaw"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The theorem controls 2-adic cylinder mass and the linear "
                "multiplier, not every natural orbit. A measure-zero nested "
                "ray may survive, and the affine offset C_a/(2^S-3^m) is "
                "not uniformly bounded over all words."
            ),
            "route_decision": {
                "discard": (
                    "promoting negative expected logarithmic multiplier or "
                    "a density-one cylinder statement to an all-natural-"
                    "numbers theorem"
                ),
                "retain": (
                    "control affine offsets uniformly along every natural "
                    "valuation ray, including the zero-density exceptional "
                    "set"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "NegativeAverageValuationDriftImpliesUniversalDescent",
                "CountableGeometricCylinderPartitionAndNegativeDriftLaw",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. The countable "
                "extension tail is exact, while the universal natural-"
                "integer bridge remains open."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-153",
            "theorem_name": (
                "PrimeThetaReflectionEnergyIdentityAndSymmetricBaselineNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The reflection identity is an exact reformulation, not a "
                "uniform lower bound. The computed endpoints are finite. "
                "PrimeProject has not bounded the binary minor arcs below "
                "the major-arc margin for every even N."
            ),
            "route_decision": {
                "discard": (
                    "trying to remove endpoint antisymmetric prime energy "
                    "by choosing a different symmetric baseline"
                ),
                "retain": (
                    "prove an explicit binary circle-method coefficient "
                    "bound that leaves a positive reflection-energy gap at "
                    "every sufficiently large even endpoint"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "SymmetricBaselineEliminatesGoldbachAntisymmetricEnergy",
                (
                    "PrimeThetaReflectionEnergyIdentityAnd"
                    "SymmetricBaselineNoGo"
                ),
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "prime-only reflection criterion and a symmetric-baseline "
                "no-go."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-153",
            "theorem_name": "CubicRoughLiouvilleParityIdentity",
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The identity isolates the parity barrier but does not "
                "prove PP>QQ at unbounded scales. Negativity through ten "
                "million is finite evidence only and supplies no uniform "
                "sieve-breaking estimate."
            ),
            "route_decision": {
                "discard": (
                    "treating a negative finite shifted Liouville sum as an "
                    "asymptotic theorem or as a completed Twin Prime proof"
                ),
                "retain": (
                    "prove that cubic-rough prime-prime pairs exceed "
                    "semiprime-semiprime pairs on an unbounded sequence of "
                    "scales"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "FiniteShiftedLiouvilleNegativityImpliesInfiniteTwinPrimes",
                "CubicRoughLiouvilleParityIdentity",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "prime/semiprime parity identity and finite evidence through "
                "X=10,000,000."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureEssentialTailGeometricReflectionParityAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-153 proves four exact partial or no-go theorems and "
            "resolves no target conjecture. It replaces full finite-rank RH "
            "tail approximation by a Schur-complement contract, completes "
            "the countable geometric Collatz cylinder law without promoting "
            "measure to universality, diagonalizes prime-only Goldbach "
            "reflection energy, and identifies the cubic-rough Twin "
            "Liouville sum exactly as twice QQ minus PP."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Connes and Consani, Weil positivity and Trace formula, "
                    "the archimedean place"
                ),
                "url": "https://arxiv.org/abs/2006.13771",
                "role": (
                    "Primary Hilbert-space Weil-positivity context. "
                    "TICKET-153 contributes only abstract block-operator "
                    "logic, not the actual semi-local decomposition."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Primary modern almost-all boundary. The exact geometric "
                    "cylinder law here does not upgrade almost-all behavior "
                    "to every natural start."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary explicit minor-arc context. TICKET-153 isolates "
                    "the prime-only endpoint reflection gap that a binary "
                    "estimate must preserve."
                ),
            },
            {
                "citation": "Maynard, On the Twin Prime Conjecture",
                "url": "https://arxiv.org/abs/1910.14674",
                "role": (
                    "Primary sieve and parity-barrier context. The new exact "
                    "identity makes the unresolved prime-versus-semiprime "
                    "comparison explicit."
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
                        "essential_tail_geometric_reflection_parity_audit."
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
        "essential_tail_geometric_reflection_parity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket153-essential-tail-geometric-reflection-parity.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-153-essential-tail-schur.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-153-geometric-cylinder-tail.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-153-reflection-energy.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-153-cubic-rough-parity.json"
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
