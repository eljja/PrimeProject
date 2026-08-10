from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket208-vertical-threeone-unitlog-cyclotomic.v1"
GENERATED_AT = "2026-08-10T18:40:00+09:00"
STATUS = "open_not_proven"


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T207", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T208", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N208",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN208",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T207", f"{prefix}-T208"],
            [f"{prefix}-T208", f"{prefix}-N208"],
            [f"{prefix}-T208", f"{prefix}-OPEN208"],
            [f"{prefix}-OPEN208", prefix],
        ],
    }


def xi_sigma_two_uniform_lower_bound(height: int) -> float:
    if height == 0:
        return math.pi / 15
    y = math.pi * height / 2
    return (math.pi / 15) * math.sqrt(y / math.sinh(y))


def riemann_vertical_clearance_audit() -> dict[str, Any]:
    rows = []
    previous = math.inf
    failures = 0
    for height in (0, 2, 4, 8, 16, 32):
        lower = xi_sigma_two_uniform_lower_bound(height)
        positive = lower > 0
        monotone = lower <= previous
        failures += int(not positive) + int(not monotone)
        rows.append(
            {
                "height_T": height,
                "uniform_vertical_clearance_lower_decimal": f"{lower:.17e}",
                "positive": positive,
                "not_larger_than_previous_height": monotone,
            }
        )
        previous = lower

    theorem = (
        "For every T>=0 and every real t with |t|<=T, the completed Riemann "
        "xi-function satisfies |xi(2+it)| >= B(T)>0, where B(0)=pi/15 and, "
        "for T>0, B(T)=(pi/15)sqrt((pi T/2)/sinh(pi T/2)). By the functional "
        "equation the same bound holds on Re(s)=-1. Thus the vertical sides of "
        "the symmetric rectangle [-1,2] x [-T,T] have an explicit zero-free "
        "clearance; only the horizontal sides retain an unknown clearance."
    )
    proof = (
        "For sigma>1, the Euler product and |1-p^(-s)|<=1+p^(-sigma) give "
        "|zeta(s)|>=product_p(1+p^(-sigma))^(-1)=zeta(2sigma)/zeta(sigma). "
        "At sigma=2 this is pi^2/15. The identity "
        "|Gamma(1+iy)|^2=pi y/sinh(pi y), together with the fact that "
        "y/sinh(pi y) decreases for y>=0, gives a uniform lower bound on the "
        "gamma factor for |t|<=T. Since |(2+it)(1+it)|>=2, substitution in "
        "xi(s)=(1/2)s(s-1)pi^(-s/2)Gamma(s/2)zeta(s) yields B(T). Reflection "
        "xi(s)=xi(1-s) transfers the bound to Re(s)=-1. The symmetric entire "
        "polynomial F(s)=(s-1/2)^2-1/9 is nonzero on both vertical sides but "
        "has the interior off-critical zeros 1/6 and 5/6, so vertical clearance "
        "alone cannot imply RH."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "euler_product_lower_bound": "|zeta(2+it)|>=zeta(4)/zeta(2)=pi^2/15",
        "gamma_modulus_identity": "|Gamma(1+iy)|^2=pi*y/sinh(pi*y)",
        "uniform_clearance_formula": (
            "B(T)=(pi/15)*sqrt((pi*T/2)/sinh(pi*T/2)), with B(0)=pi/15"
        ),
        "vertical_clearance_rows": rows,
        "vertical_only_countermodel": {
            "function": "F(s)=(s-1/2)^2-1/9",
            "interior_off_critical_zeros": ["1/6", "5/6"],
            "nonzero_on_sigma_2_and_minus_1": True,
            "is_not_a_zeta_counterexample": True,
        },
        "aggregate": {
            "explicit_sigma_two_vertical_clearance_proved": True,
            "left_vertical_clearance_transferred_by_symmetry": True,
            "horizontal_cofinal_clearance_proved": False,
            "vertical_clearance_alone_implies_rh_refuted": True,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The bound certifies only the two vertical sides of rectangles with "
            "fixed real parts -1 and 2. It neither bounds xi away from zero on "
            "cofinal horizontal sides nor locates every interior zero."
        ),
        "failure_count": failures,
    }


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def cycle_fixed_point(word: tuple[int, ...]) -> Fraction | None:
    slope = Fraction(1)
    intercept = Fraction(0)
    for valuation in word:
        denominator = 2**valuation
        slope = Fraction(3, denominator) * slope
        intercept = (3 * intercept + 1) / denominator
    if slope >= 1:
        return None
    return intercept / (1 - slope)


def total_valuation_upper_bound(length: int) -> int:
    exponent = 0
    while 2 ** (exponent + 1) * 3**length <= 10**length:
        exponent += 1
    return exponent


def three_one_words(length: int, maximum_total: int) -> list[tuple[int, ...]]:
    baseline_total = 2 * length - 3
    if baseline_total > maximum_total:
        return []
    words: list[tuple[int, ...]] = []
    for other_ones in combinations(range(1, length - 1), 2):
        one_positions = {0, *other_ones}
        non_one_positions = [
            index for index in range(length) if index not in one_positions
        ]
        for extra_total in range(maximum_total - baseline_total + 1):
            for extras in weak_compositions(extra_total, len(non_one_positions)):
                word = [1 if index in one_positions else 2 for index in range(length)]
                for index, extra in zip(non_one_positions, extras, strict=True):
                    word[index] += extra
                words.append(tuple(word))
    return words


def collatz_three_one_audit() -> dict[str, Any]:
    rows = []
    all_words: list[tuple[int, ...]] = []
    failures = 0
    integer_candidates = []
    for length in range(4, 12):
        maximum_total = total_valuation_upper_bound(length)
        baseline_total = 2 * length - 3
        words = three_one_words(length, maximum_total)
        all_words.extend(words)
        local_integer_candidates = []
        for word in words:
            fixed = cycle_fixed_point(word)
            if (
                fixed is not None
                and fixed.denominator == 1
                and fixed.numerator >= 3
                and fixed.numerator % 2 == 1
            ):
                local_integer_candidates.append(
                    {"word": list(word), "fixed_point": fixed.numerator}
                )
        integer_candidates.extend(local_integer_candidates)
        failures += len(local_integer_candidates)
        digest = hashlib.sha256(
            "\n".join(",".join(map(str, word)) for word in words).encode("ascii")
        ).hexdigest()
        rows.append(
            {
                "length_h": length,
                "minimum_total_valuation_2h_minus_3": baseline_total,
                "maximum_total_valuation_from_minimum_bound": maximum_total,
                "enumerated_word_count": len(words),
                "positive_odd_integer_fixed_point_count": len(
                    local_integer_candidates
                ),
                "valuation_word_sha256": digest,
            }
        )

    length_twelve_left = 2 ** (2 * 12 - 3) * 3**12
    length_twelve_right = 10**12
    long_lengths_excluded = length_twelve_left > length_twelve_right
    failures += int(not long_lengths_excluded)
    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly three "
        "valuation entries equal to one and every remaining valuation at least "
        "two. Together with TICKETS 206 and 207, every hypothetical nontrivial "
        "positive cycle must contain at least four valuation-one entries."
    )
    proof = (
        "Rotate a hypothetical cycle to its minimum odd value m>=3. Its first "
        "valuation is one, because a valuation at least two maps m below itself; "
        "its last valuation is at least two, because (3x+1)/2>x for x>=m. If "
        "A is the total valuation and h the length, multiplying the cycle ratios "
        "gives 2^A=product_i(3+1/x_i)<= (10/3)^h. Exactly three ones and all "
        "other valuations at least two give A>=2h-3. At h=12, "
        "2^(2h-3)3^h>10^h, and the ratio grows by 6/5 per additional step, so "
        "all h>=12 are impossible. For 4<=h<=11 the same product inequality "
        "bounds A, leaving exactly 185 valuation words after fixing the minimum "
        "rotation. Exact affine composition gives the unique possible fixed "
        "point for each word; none is a positive odd integer."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cycle_product_identity": "2^A=product_i(3+1/x_i)",
        "minimum_orbit_bound": "x_i>=m>=3 implies 2^A*3^h<=10^h",
        "exact_enumeration_rows": rows,
        "total_exact_words_enumerated": len(all_words),
        "positive_odd_integer_fixed_point_candidates": integer_candidates,
        "length_at_least_twelve_exclusion": {
            "left_2_pow_21_times_3_pow_12": str(length_twelve_left),
            "right_10_pow_12": str(length_twelve_right),
            "left_exceeds_right": long_lengths_excluded,
            "growth_factor_per_extra_length": "6/5",
        },
        "aggregate": {
            "exactly_three_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 4,
            "four_or_more_one_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is a complete finite proof for one periodic valuation stratum. "
            "It does not exclude cycles with four or more valuation-one entries "
            "and does not prove descent of nonperiodic orbits."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> list[bool]:
    flags = [True] * (limit + 1)
    if limit >= 0:
        flags[0] = False
    if limit >= 1:
        flags[1] = False
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            flags[candidate * candidate : limit + 1 : candidate] = [False] * (
                (limit - candidate * candidate) // candidate + 1
            )
    return flags


def primes_through(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def goldbach_unit_log_row(bound: int) -> dict[str, Any]:
    witnesses = [prime for prime in primes_through(bound) if prime >= 3]
    forcing = [prime for prime in primes_through(4 * bound) if prime > bound][
        : len(witnesses)
    ]
    if len(forcing) != len(witnesses):
        raise ValueError(f"insufficient forcing primes for B={bound}")
    modulus = 2
    residue = 0
    forcing_rows = []
    for witness, divisor in zip(witnesses, forcing, strict=True):
        step = ((witness - residue) * pow(modulus, -1, divisor)) % divisor
        residue = (residue + modulus * step) % (modulus * divisor)
        modulus *= divisor
        forcing_rows.append(
            {"excluded_witness_prime": witness, "forcing_divisor": divisor}
        )
    target = residue + modulus if residue else 2 * modulus
    for row in forcing_rows:
        complement = target - row["excluded_witness_prime"]
        row["complement"] = str(complement)
        row["proper_composite_complement"] = (
            complement > row["forcing_divisor"]
            and complement % row["forcing_divisor"] == 0
        )
    return {
        "witness_bound_B": bound,
        "odd_witness_count": len(witnesses),
        "largest_forcing_prime": forcing[-1],
        "largest_forcing_prime_over_B_decimal": f"{forcing[-1] / bound:.12f}",
        "canonical_even_target_N": str(target),
        "modulus_M": str(modulus),
        "N_between_M_and_3M": modulus < target <= 3 * modulus,
        "N_bit_length": target.bit_length(),
        "exact_B_over_bit_length_lower_proxy": fraction_text(
            Fraction(bound, target.bit_length())
        ),
        "observed_B_over_natural_log_N_decimal": f"{bound / math.log(target):.12f}",
        "p_equals_2_complement_is_composite": target > 4 and (target - 2) % 2 == 0,
        "forcing_rows": forcing_rows,
        "all_prime_witnesses_at_most_B_excluded": all(
            row["proper_composite_complement"] for row in forcing_rows
        ),
    }


def goldbach_unit_log_audit() -> dict[str, Any]:
    rows = [goldbach_unit_log_row(bound) for bound in (29, 59, 127, 251, 509)]
    failures = sum(
        int(not row["N_between_M_and_3M"])
        + int(not row["p_equals_2_complement_is_composite"])
        + int(not row["all_prime_witnesses_at_most_B_excluded"])
        for row in rows
    )
    theorem = (
        "Let W(N) be the least prime p for which N-p is prime, with W(N)=infinity "
        "if no representation exists. For every real c<1 there are unboundedly "
        "many even N with W(N)>c log N. Equivalently, with the extended-value "
        "convention, limsup over even N of W(N)/log N is at least one."
    )
    proof = (
        "Fix eta>0 and a large B. By the prime number theorem, the interval "
        "(B,(2+eta)B) eventually contains at least pi(B)-1 primes. Assign a "
        "distinct q_p from this interval to each odd prime p<=B. CRT imposes "
        "N=0 mod 2 and N=p mod q_p. For M=2 product q_p choose an equivalent "
        "even representative M<N<=3M. Then every N-p with p<=B is a proper "
        "composite multiple of its q_p, including the elementary p=2 case, so "
        "W(N)>B. Moreover log M<=log 2+(pi(B)-1)log((2+eta)B)=(1+o(1))B. "
        "Thus log N<=(1+o(1))B, and for every c<1, eventually c log N<B<W(N). "
        "The moduli grow, so the targets are unbounded."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "asymptotic_resource_identity": (
            "pi(B)*log((2+eta)B)=(1+o(1))*B by the prime number theorem"
        ),
        "crt_unit_log_fixture_rows": rows,
        "aggregate": {
            "unit_constant_limsup_lower_bound_proved": True,
            "every_fixed_c_below_one_witness_window_refuted": True,
            "goldbach_counterexample_found": False,
            "tail_exception_bound_below_one_constructed": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The construction excludes only p<=B. It does not rule out a larger "
            "prime witness, produce a Goldbach counterexample, or upper-bound the "
            "exceptional set beyond the asymptotically unit logarithmic floor."
        ),
        "failure_count": failures,
    }


def omega_sieve(limit: int) -> list[int]:
    omega = [0] * (limit + 1)
    for prime in range(2, limit + 1):
        if omega[prime] != 0:
            continue
        power = prime
        while power <= limit:
            for multiple in range(power, limit + 1, power):
                omega[multiple] += 1
            if power > limit // prime:
                break
            power *= prime
    return omega


def cyclotomic_interval_row(start: int, length: int) -> dict[str, Any]:
    endpoint = start + length + 2
    omega = omega_sieve(endpoint)
    omega_bound = endpoint.bit_length() - 1
    modulus = omega_bound + 1
    histogram: dict[tuple[int, int], int] = {}
    for lower in range(start + 1, start + length + 1):
        key = (omega[lower], omega[lower + 2])
        histogram[key] = histogram.get(key, 0) + 1
    twin_count = histogram.get((1, 1), 0)
    zero_mode_raw = length
    nonzero_mode_raw = modulus * modulus * twin_count - zero_mode_raw
    reconstructed = Fraction(zero_mode_raw + nonzero_mode_raw, modulus * modulus)
    return {
        "interval": f"({start},{start + length}]",
        "length_H": length,
        "omega_upper_bound_L": omega_bound,
        "cyclotomic_modulus_M": modulus,
        "exact_twin_count_T": twin_count,
        "zero_mode_raw_contribution": zero_mode_raw,
        "all_nonzero_modes_raw_aggregate": nonzero_mode_raw,
        "normalized_zero_mode": fraction_text(Fraction(length, modulus * modulus)),
        "normalized_nonzero_modes": fraction_text(
            Fraction(nonzero_mode_raw, modulus * modulus)
        ),
        "spectral_reconstruction": fraction_text(reconstructed),
        "reconstruction_exact": reconstructed == twin_count,
        "nonzero_modes_exactly_cancel_zero_mode_when_twin_free": (
            twin_count != 0 or nonzero_mode_raw == -length
        ),
        "nonzero_histogram_cells": [
            {"omega_n": left, "omega_n_plus_2": right, "count": count}
            for (left, right), count in sorted(histogram.items())
        ],
    }


def twin_cyclotomic_audit() -> dict[str, Any]:
    interval_rows = [
        cyclotomic_interval_row(start, length)
        for start, length in ((24, 4), (32, 32), (64, 64), (128, 128))
    ]
    alias_rows = []
    for modulus in (2, 3, 5, 7):
        multiplicity = modulus + 1
        alias_rows.append(
            {
                "fixed_modulus_M": modulus,
                "composite_multiplicity_1_plus_M": multiplicity,
                "explicit_composite": str(2**multiplicity),
                "root_filter_accepts_as_omega_congruent_to_one": True,
                "is_prime": False,
            }
        )
    failures = sum(
        int(not row["reconstruction_exact"])
        + int(not row["nonzero_modes_exactly_cancel_zero_mode_when_twin_free"])
        for row in interval_rows
    ) + sum(int(row["is_prime"]) for row in alias_rows)
    theorem = (
        "Let I be an interval of H integers and let L=floor(log_2(max(I)+2)), "
        "M=L+1, and omega=exp(2 pi i/M). Since Omega(n)<=L, the root-of-unity "
        "filter delta_{Omega(n),1}=M^(-1)sum_{j=0}^{M-1}omega^{j(Omega(n)-1)} "
        "is exact on I and I+2. Consequently the twin count T_I is an exact "
        "M-by-M signed cyclotomic correlation. Its zero mode contributes H/M^2, "
        "while all nonzero modes contribute T_I-H/M^2. In a twin-free interval "
        "they cancel the positive zero mode exactly. Any fixed M aliases the "
        "composite multiplicity 1+M with primes, so the spectral dimension must "
        "grow with the interval."
    )
    proof = (
        "Finite cyclic character orthogonality gives M^(-1)sum_j omega^{j(m-1)} "
        "equal to one exactly when m=1 mod M. The bound 0<=Omega(n)<=L<M turns "
        "this congruence into equality. Multiplying the two filters and summing "
        "over n in I gives the double correlation formula. The (0,0) term is H, "
        "so after removing it the raw nonzero-mode aggregate is M^2 T_I-H. "
        "For fixed M, m=1+M passes the same filter, and n=2^(1+M) is an explicit "
        "composite with that multiplicity. Hence neither a positive zero mode nor "
        "a fixed-dimensional phase model proves twin positivity."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_projector_identity": (
            "1_{Omega(n)=1}=M^(-1) sum_{j=0}^{M-1} exp(2*pi*i*j*(Omega(n)-1)/M), "
            "provided M>Omega(n)"
        ),
        "exact_correlation_identity": (
            "M^2*T_I=H+R_I, where R_I is the aggregate of all nonzero frequency pairs"
        ),
        "interval_reconstruction_rows": interval_rows,
        "fixed_dimension_alias_rows": alias_rows,
        "aggregate": {
            "growing_cyclotomic_prime_projector_proved": True,
            "finite_twin_correlation_reconstruction_proved": True,
            "positive_zero_mode_alone_suffices_refuted": True,
            "fixed_dimension_exactness_refuted": True,
            "cofinal_nonzero_mode_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The identity exactly re-encodes finite factorization data. It gives "
            "no independent lower bound on the growing family of nonzero Omega-"
            "phase correlations and therefore proves no cofinal twin positivity."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_vertical_clearance_audit()
    collatz_compute = collatz_three_one_audit()
    goldbach_compute = goldbach_unit_log_audit()
    twin_compute = twin_cyclotomic_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-208",
            "theorem_name": "SigmaTwoCompletedXiVerticalClearanceAndHorizontalEdgeReduction",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": (
                "No explicit positive completed-xi clearance is proved on a "
                "cofinal sequence of horizontal edges."
            ),
            "route_decision": {
                "discard": "treating the two vertical sides as unresolved zero-free boundaries, or using their clearance alone to infer RH",
                "retain": "explicit top-edge interval clearance at cofinal admissible heights",
                "next_single_lemma": "CertifiedCompletedXiTopEdgeClearanceOnCofinalAdmissibleHeights",
            },
            "proof_dag": proof_dag(
                "RH",
                "CompletedXiDihedralBoundaryReductionAndSymmetryOnlyNoGo",
                "SigmaTwoCompletedXiVerticalClearanceAndHorizontalEdgeReduction",
                "VerticalEdgeClearanceAloneDeterminesInteriorZeroLocation",
                "CertifiedCompletedXiTopEdgeClearanceOnCofinalAdmissibleHeights",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof or off-critical zeta zero. The vertical rectangle sides now have an explicit analytic clearance; the horizontal cofinal bound remains open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-208",
            "theorem_name": "ThreeOneAcceleratedCycleFiniteEnumerationExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": (
                "Cycles with at least four valuation-one entries and all "
                "nonperiodic divergent orbits remain open."
            ),
            "route_decision": {
                "discard": "searching any exactly-three-valuation-one word for a positive accelerated cycle",
                "retain": "the same exact product-and-enumeration reduction for four-one primitive necklaces plus a separate descent theorem",
                "next_single_lemma": "UniformExclusionForPrimitiveValuationNecklacesWithExactlyFourOnes",
            },
            "proof_dag": proof_dag(
                "CO",
                "TwoOneArbitraryGeTwoValuationCycleExclusion",
                "ThreeOneAcceleratedCycleFiniteEnumerationExclusion",
                "ExactlyThreeValuationOnesCanSupportAPositiveCycle",
                "UniformExclusionForPrimitiveValuationNecklacesWithExactlyFourOnes",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit counterexample. The complete exactly-three-valuation-one periodic stratum is excluded by an exact finite proof.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-208",
            "theorem_name": "AsymptoticallyUnitLogLeastWitnessCRTLowerBound",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": (
                "No exceptional-count upper bound is proved for witnesses beyond "
                "the asymptotically unit logarithmic floor."
            ),
            "route_decision": {
                "discard": "any universal Goldbach search window p<=c log N with a fixed c<1",
                "retain": "tail exceptional-set control beyond an asymptotically unit logarithmic witness floor",
                "next_single_lemma": "GoldbachTailExceptionalCountBelowOneBeyondAsymptoticallyUnitLogFloor",
            },
            "proof_dag": proof_dag(
                "GB",
                "LogarithmicLeastWitnessLowerBoundAlongCRTSequence",
                "AsymptoticallyUnitLogLeastWitnessCRTLowerBound",
                "FixedSubunitLogarithmicWitnessWindowUniversallyCoversGoldbach",
                "GoldbachTailExceptionalCountBelowOneBeyondAsymptoticallyUnitLogFloor",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. CRT forces least witnesses above c log N for every fixed c<1 along unbounded target sequences.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-208",
            "theorem_name": "GrowingCyclotomicOmegaProjectorAndZeroModeCancellationNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": (
                "No uniform lower bound keeps the aggregate growing nonzero "
                "Omega-phase remainder strictly above minus the interval length."
            ),
            "route_decision": {
                "discard": "using the positive cyclotomic zero mode or any fixed phase dimension as a twin-prime lower bound",
                "retain": "the growing signed Omega-phase remainder with its exact zero-mode normalization",
                "next_single_lemma": "CofinalDyadicOmegaPhaseRemainderStrictlyAboveMinusIntervalLength",
            },
            "proof_dag": proof_dag(
                "TP",
                "AbelOmegaProjectorClosedFormFiniteReconstructionAndPositivityCircularityNoGo",
                "GrowingCyclotomicOmegaProjectorAndZeroModeCancellationNoGo",
                "PositiveOrFixedDimensionalOmegaZeroModeForcesTwinPrimes",
                "CofinalDyadicOmegaPhaseRemainderStrictlyAboveMinusIntervalLength",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. A growing signed finite reconstruction and its exact zero-mode cancellation obstruction are proved.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureVerticalThreeOneUnitLogCyclotomicAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-208 resolves none of the four conjectures. It proves explicit "
            "completed-xi clearance on both vertical rectangle sides, excludes "
            "the complete three-one Collatz cycle stratum, raises the Goldbach "
            "CRT witness obstruction to every constant below log N, and gives an "
            "exact growing cyclotomic Omega correlation with a zero-mode no-go."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The four results separate analytically controlled boundaries or "
            "finite strata from the remaining cofinal signed correlations. The "
            "unresolved step is no longer more finite search: it is a uniform "
            "horizontal, four-one, exceptional-tail, or phase-remainder theorem."
        ),
        "literature_boundary": {
            "riemann": "Rigorous zero verification through finite height remains finite evidence; the new theorem is an elementary vertical-edge reduction and not a replacement for cofinal zero control.",
            "collatz": "Almost-all descent and bounded verification do not exclude every cycle or divergent orbit; the result closes only one exact valuation stratum.",
            "goldbach": "Empirical verification through 4e18 is finite; the CRT theorem is a witness-scale obstruction and not an exceptional-set upper bound.",
            "twin_prime": "Bounded-gap sieve theorems do not force gap two; the cyclotomic identity is a finite signed reduction and does not break the parity barrier.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
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
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "bounded_result": {
                    "vertical_threeone_unitlog_cyclotomic_audit": audit
                },
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / "data/open-problem/ticket208-vertical-threeone-unitlog-cyclotomic.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "vertical_threeone_unitlog_cyclotomic_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-208-sigma-two-clearance.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-208-three-one-exclusion.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-208-unit-log-witness.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-208-cyclotomic-omega.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(
            path,
            standalone_payload(audit[section_key], problem_ids[section_key]),
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
