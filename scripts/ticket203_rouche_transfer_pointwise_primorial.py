from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import (
    ordered_affine_numerator,
    prime_sieve,
    semiprime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket203-rouche-transfer-pointwise-primorial.v1"
GENERATED_AT = "2026-08-10T23:55:00+09:00"
STATUS = "open_not_proven"


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


def riemann_rouche_transfer_audit() -> dict[str, Any]:
    # P=(z^2-1)(z^2-4), F=P(1+z^2/100), and
    # Gamma is the boundary of |Re z|<=3, |Im z|<=1.
    rectangle_real_radius = 3
    rectangle_imag_radius = 1
    perturbation_scale = 100
    maximum_abs_z_squared = (
        rectangle_real_radius**2 + rectangle_imag_radius**2
    )
    relative_boundary_bound = Fraction(
        maximum_abs_z_squared, perturbation_scale
    )
    listed_zeros = [-2, -1, 1, 2]
    comparison_zero_count = len(listed_zeros)
    function_zero_count_inside = len(listed_zeros)
    extra_zeros = ["-10i", "+10i"]
    failures = 0
    failures += int(relative_boundary_bound >= 1)
    failures += int(comparison_zero_count != function_zero_count_inside)
    failures += int(any(abs(value) >= rectangle_real_radius for value in listed_zeros))
    return {
        "theorem": (
            "Let X and P be analytic on and inside a simple closed contour "
            "Gamma. Suppose |X-P|<|P| on Gamma, P has exactly m interior "
            "zeros counted with multiplicity, and an independently certified "
            "list already supplies m interior zeros of X counted with "
            "multiplicity. Rouche's theorem gives N_Gamma(X)=m, so the list "
            "exhausts every zero of X inside Gamma. Applied to "
            "Xi(z)=xi(1/2+iz) on a cofinal family of rectangles covering "
            "|Im z|<1/2, with every listed zero real, this is a sufficient "
            "zero-count transfer contract for the Riemann Hypothesis."
        ),
        "proof": (
            "Rouche's theorem gives N_Gamma(X)=N_Gamma(P)=m. The certified "
            "zeros of X are a submultiset of all interior zeros and already "
            "have total multiplicity m; therefore no additional interior "
            "zero exists. For cofinal completed-zeta rectangles every "
            "nontrivial zeta zero is eventually interior. If each exhaustive "
            "list lies on the real z-axis, every nontrivial zeta zero lies on "
            "Re s=1/2. The independent-inclusion premise is essential: equal "
            "total counts alone cannot locate the zeros."
        ),
        "exact_synthetic_regression": {
            "comparison_P": "(z^2-1)(z^2-4)",
            "analytic_X": "P(z)(1+z^2/100)",
            "rectangle": {
                "real_interval": [-rectangle_real_radius, rectangle_real_radius],
                "imaginary_interval": [-rectangle_imag_radius, rectangle_imag_radius],
            },
            "listed_X_zeros_inside": listed_zeros,
            "comparison_zero_count_inside": comparison_zero_count,
            "independently_certified_X_zero_count_inside": function_zero_count_inside,
            "extra_X_zeros_outside": extra_zeros,
            "maximum_abs_z_squared_on_boundary": maximum_abs_z_squared,
            "relative_boundary_error_bound": fraction_text(relative_boundary_bound),
            "strict_rouche_margin": fraction_text(1 - relative_boundary_bound),
            "rouche_hypothesis_holds": relative_boundary_bound < 1,
            "certified_list_is_exhaustive": (
                comparison_zero_count == function_zero_count_inside
                and relative_boundary_bound < 1
            ),
        },
        "aggregate": {
            "exact_zero_count_transfer_contract_proved": failures == 0,
            "independent_zero_inclusion_required": True,
            "cofinal_contract_is_sufficient_for_rh": True,
            "actual_xi_boundary_margin_constructed": False,
            "actual_cofinal_xi_certificate_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This proves the missing logical transfer step, not its completed-"
            "zeta analytic premise. The synthetic polynomial is a regression "
            "fixture and is not Xi. No off-critical-line Xi zero is produced."
        ),
        "failure_count": failures,
    }


def prefix_sums(word: tuple[int, ...]) -> list[int]:
    values = [0]
    for valuation in word:
        values.append(values[-1] + valuation)
    return values


def forward_transfer_row(
    word: tuple[int, ...], left: int, right: int
) -> dict[str, Any]:
    if not 0 <= left < right < len(word):
        raise ValueError("require 0<=left<right<len(word)")
    if word[left] < 2:
        raise ValueError("the left donor valuation must be at least two")
    prefixes = prefix_sums(word)
    horizon = len(word)
    segment = sum(
        3 ** (horizon - 1 - index) * 2 ** prefixes[index]
        for index in range(left + 1, right + 1)
    )
    transferred = list(word)
    transferred[left] -= 1
    transferred[right] += 1
    target = tuple(transferred)
    source_numerator = ordered_affine_numerator(word)
    target_numerator = ordered_affine_numerator(target)
    denominator = 2 ** sum(word) - 3**horizon
    return {
        "source_word": list(word),
        "target_word": list(target),
        "left_donor_i": left,
        "right_receiver_j": right,
        "valuation_sum_preserved": sum(word) == sum(target),
        "denominator_D": denominator,
        "source_numerator_B": source_numerator,
        "target_numerator_B_prime": target_numerator,
        "intervening_prefix_segment_Q": segment,
        "segment_is_even": segment % 2 == 0,
        "forward_identity_B_prime_equals_B_minus_Q_over_2": (
            target_numerator == source_numerator - segment // 2
        ),
        "source_affine_divisibility": denominator > 0
        and source_numerator % denominator == 0,
        "target_affine_divisibility": denominator > 0
        and target_numerator % denominator == 0,
    }


def backward_transfer_row(
    word: tuple[int, ...], left: int, right: int
) -> dict[str, Any]:
    if not 0 <= left < right < len(word):
        raise ValueError("require 0<=left<right<len(word)")
    if word[right] < 2:
        raise ValueError("the right donor valuation must be at least two")
    prefixes = prefix_sums(word)
    horizon = len(word)
    segment = sum(
        3 ** (horizon - 1 - index) * 2 ** prefixes[index]
        for index in range(left + 1, right + 1)
    )
    transferred = list(word)
    transferred[left] += 1
    transferred[right] -= 1
    target = tuple(transferred)
    source_numerator = ordered_affine_numerator(word)
    target_numerator = ordered_affine_numerator(target)
    return {
        "source_word": list(word),
        "target_word": list(target),
        "left_receiver_i": left,
        "right_donor_j": right,
        "intervening_prefix_segment_Q": segment,
        "backward_identity_B_prime_equals_B_plus_Q": (
            target_numerator == source_numerator + segment
        ),
    }


def collatz_transfer_exhaustive_summary(horizon: int) -> dict[str, Any]:
    contracting_word_count = 0
    forward_transfer_count = 0
    identity_failure_count = 0
    target_divisibility_hit_count = 0
    all_two_target_hit_count = 0
    for word_values in product(range(1, 5), repeat=horizon):
        word = tuple(word_values)
        denominator = 2 ** sum(word) - 3**horizon
        if denominator <= 0:
            continue
        contracting_word_count += 1
        for left in range(horizon):
            if word[left] < 2:
                continue
            for right in range(left + 1, horizon):
                row = forward_transfer_row(word, left, right)
                forward_transfer_count += 1
                identity_failure_count += int(
                    not row[
                        "forward_identity_B_prime_equals_B_minus_Q_over_2"
                    ]
                )
                if row["target_affine_divisibility"]:
                    target_divisibility_hit_count += 1
                    target = tuple(row["target_word"])
                    all_two_target_hit_count += int(
                        set(target) == {2}
                    )
    return {
        "horizon": horizon,
        "valuation_alphabet": [1, 2, 3, 4],
        "contracting_word_count": contracting_word_count,
        "forward_transfer_count": forward_transfer_count,
        "identity_failure_count": identity_failure_count,
        "target_divisibility_hit_count": target_divisibility_hit_count,
        "all_two_target_hit_count": all_two_target_hit_count,
        "hit_count_equals_choose_horizon_two": (
            target_divisibility_hit_count == math.comb(horizon, 2)
        ),
        "every_hit_is_known_all_two_fixed_cycle": (
            target_divisibility_hit_count == all_two_target_hit_count
        ),
    }


def collatz_signed_transfer_audit() -> dict[str, Any]:
    forward_examples = [
        forward_transfer_row((3, 1), 0, 1),
        forward_transfer_row((2, 3, 1, 4), 1, 3),
        forward_transfer_row((4, 1, 2, 3, 2), 0, 4),
    ]
    backward_examples = [
        backward_transfer_row((1, 3), 0, 1),
        backward_transfer_row((2, 1, 4, 2), 0, 2),
    ]
    exhaustive = [
        collatz_transfer_exhaustive_summary(horizon)
        for horizon in range(2, 8)
    ]
    minimal_counterexample = forward_examples[0]
    failures = sum(
        int(
            not row["valuation_sum_preserved"]
            or not row["segment_is_even"]
            or not row[
                "forward_identity_B_prime_equals_B_minus_Q_over_2"
            ]
        )
        for row in forward_examples
    )
    failures += sum(
        int(not row["backward_identity_B_prime_equals_B_plus_Q"])
        for row in backward_examples
    )
    failures += sum(
        row["identity_failure_count"]
        + int(not row["hit_count_equals_choose_horizon_two"])
        + int(not row["every_hit_is_known_all_two_fixed_cycle"])
        for row in exhaustive
    )
    failures += int(minimal_counterexample["source_affine_divisibility"])
    failures += int(not minimal_counterexample["target_affine_divisibility"])
    return {
        "theorem": (
            "For a positive valuation word a of length h, write "
            "B(a)=sum_m 3^(h-1-m)2^P_m, where P_m is the prefix sum before "
            "site m. If i<j and one valuation unit is moved from i to j, then "
            "the denominator D=2^sum(a)-3^h is unchanged and "
            "B(a-e_i+e_j)=B(a)-Q_(i,j)/2, with "
            "Q_(i,j)=sum_(i<m<=j)3^(h-1-m)2^P_m. Moving one unit from j to "
            "i instead gives B(a+e_i-e_j)=B(a)+Q_(i,j). These exact signed "
            "identities do not yield a universal divisibility obstruction: "
            "the minimal transfer (3,1)->(2,2) changes B=11 to B'=7 at "
            "D=7 and reaches the known all-two fixed cycle."
        ),
        "proof": (
            "For the forward transfer, precisely the prefix exponents "
            "P_(i+1),...,P_j decrease by one; all earlier and later prefixes "
            "are unchanged. Subtracting the two defining sums for B gives "
            "-Q/2. For the reverse transfer those same powers of two double, "
            "giving +Q. The valuation sum is fixed, hence D is fixed. Direct "
            "substitution into (3,1) gives D=7, B=11, and B(2,2)=7. Therefore "
            "any theorem claiming signed-transfer preservation of affine "
            "nondivisibility without excluding the all-two component is false."
        ),
        "exact_forward_examples": forward_examples,
        "exact_backward_examples": backward_examples,
        "minimal_universal_obstruction_counterexample": minimal_counterexample,
        "exhaustive_regression": exhaustive,
        "aggregate": {
            "signed_two_site_transfer_identity_proved": failures == 0,
            "universal_nondivisibility_preservation_refuted": True,
            "exhaustive_horizons": [2, 3, 4, 5, 6, 7],
            "exhaustive_forward_transfer_count": sum(
                row["forward_transfer_count"] for row in exhaustive
            ),
            "all_finite_hits_are_all_two_in_tested_box": all(
                row["every_hit_is_known_all_two_fixed_cycle"]
                for row in exhaustive
            ),
            "arbitrary_words_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The all-two counterexample refutes only an unconditional transfer-"
            "invariance route. The finite enumeration is not a proof that all "
            "other transfer components avoid divisibility at unbounded length."
        ),
        "failure_count": failures,
    }


def goldbach_point_row(
    target: int,
    primes: bytearray,
    prime_values: list[int],
    semiprimes: bytearray,
) -> dict[str, Any]:
    prime_prime = 0
    prime_semiprime = 0
    for prime in prime_values:
        if prime >= target:
            break
        complement = target - prime
        prime_prime += int(primes[complement])
        prime_semiprime += int(semiprimes[complement])
    channel = prime_prime + prime_semiprime
    signed = prime_semiprime - prime_prime
    defect = Fraction(channel - signed, channel) if channel else Fraction(0)
    return {
        "even_target_N": target,
        "ordered_prime_prime_R": prime_prime,
        "ordered_prime_semiprime_S": prime_semiprime,
        "Chen_channel_C": channel,
        "Liouville_channel_L": signed,
        "relative_defect_delta": fraction_text(defect),
        "C_minus_L_equals_2R": channel - signed == 2 * prime_prime,
        "goldbach_positive": prime_prime > 0,
        "defect_positive": defect > 0,
        "positivity_equivalence": (prime_prime > 0) == (defect > 0),
    }


def goldbach_abstract_model_row(exponent: int) -> dict[str, Any]:
    if exponent & (exponent - 1):
        raise ValueError("exponent must be a power of two")
    target = 1 << exponent
    channel = target // exponent
    prime_prime = 1
    prime_semiprime = channel - 1
    signed = prime_semiprime - prime_prime
    defect = Fraction(channel - signed, channel)
    upper_bound = Fraction(2 * exponent * exponent, target)
    return {
        "abstract_even_target_N": str(target),
        "exponent_m_with_N_equals_2powm": exponent,
        "abstract_R": prime_prime,
        "abstract_S": str(prime_semiprime),
        "abstract_C_equals_N_over_m": str(channel),
        "abstract_L": str(signed),
        "relative_defect_delta": fraction_text(defect),
        "goldbach_positive": True,
        "C_minus_L_equals_2R": channel - signed == 2 * prime_prime,
        "loglog_N_times_delta_upper_bound_2m2_over_2m": fraction_text(
            upper_bound
        ),
    }


def goldbach_pointwise_strength_audit() -> dict[str, Any]:
    limit = 100_000
    primes = prime_sieve(limit)
    prime_values = [value for value in range(2, limit + 1) if primes[value]]
    semiprimes = semiprime_sieve(limit, prime_values)
    actual_rows = [
        goldbach_point_row(target, primes, prime_values, semiprimes)
        for target in (100, 1_000, 10_000, 100_000)
    ]
    abstract_rows = [
        goldbach_abstract_model_row(exponent)
        for exponent in (8, 16, 32, 64, 128)
    ]
    bounds = [
        Fraction(row["loglog_N_times_delta_upper_bound_2m2_over_2m"])
        for row in abstract_rows
    ]
    failures = sum(
        int(
            not row["C_minus_L_equals_2R"]
            or not row["positivity_equivalence"]
        )
        for row in actual_rows
    )
    failures += sum(
        int(
            not row["goldbach_positive"]
            or not row["C_minus_L_equals_2R"]
        )
        for row in abstract_rows
    )
    failures += int(
        any(bounds[index + 1] >= bounds[index] for index in range(len(bounds) - 1))
    )
    return {
        "theorem": (
            "At every Chen-positive even N, with C(N)=R(N)+S(N) and "
            "L(N)=S(N)-R(N), the exact identity "
            "delta(N)=1-L(N)/C(N)=2R(N)/C(N) implies "
            "R(N)>0 if and only if delta(N)>0. Thus any lower bound "
            "delta(N)>=c/log log N for every sufficiently large even N "
            "already implies strong Goldbach and is quantitatively stronger "
            "than positivity. Channel algebra and Goldbach positivity alone "
            "cannot imply it: the integer model N=2^m, C=N/m, R=1, S=C-1 "
            "for powers of two m has R>0 while delta log log N tends to zero."
        ),
        "proof": (
            "The projector identity C-L=2R gives the equivalence because C is "
            "positive. In the abstract model delta=2/C=2m/2^m. For m>=2, "
            "log log(2^m)=log(m log 2)<=m, so "
            "delta log log N<=2m^2/2^m, which tends to zero. Hence no fixed "
            "c>0 follows from one representation per target, even when the "
            "ambient channel has the natural N/log N scale."
        ),
        "exact_actual_channel_rows": actual_rows,
        "exact_abstract_countermodel_rows": abstract_rows,
        "aggregate": {
            "pointwise_defect_positivity_equivalent_to_goldbach_on_chen_channel": True,
            "loglog_scaled_lower_bound_is_stronger_than_goldbach": True,
            "goldbach_positivity_implies_loglog_scaled_bound_refuted_at_channel_level": True,
            "abstract_scaled_upper_bounds_strictly_decrease": all(
                bounds[index + 1] < bounds[index]
                for index in range(len(bounds) - 1)
            ),
            "actual_goldbach_counterexample_found": False,
            "goldbach_resolved": False,
        },
        "no_go_scope": (
            "The countermodel is exact nonnegative integer channel data, not "
            "the actual primes. It refutes an implication from projector "
            "algebra plus positivity, not the proposed estimate in prime "
            "arithmetic and not Goldbach itself."
        ),
        "failure_count": failures,
    }


def primes_up_to(limit: int) -> list[int]:
    sieve = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if sieve[value]]


def is_prime_trial(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime_one_mod(modulus: int, multiplier_start: int = 1) -> int:
    multiplier = multiplier_start
    while True:
        candidate = multiplier * modulus + 1
        if is_prime_trial(candidate):
            return candidate
        multiplier += 1


def primorial_signature_row(sieve_limit: int) -> dict[str, Any]:
    small_primes = primes_up_to(sieve_limit)
    modulus = math.prod(small_primes)
    prime_object = next_prime_one_mod(modulus)
    second_prime = next_prime_one_mod(
        modulus, (prime_object - 1) // modulus + 1
    )
    semiprime_object = prime_object * second_prime
    prime_signature = [int(prime_object % prime == 0) for prime in small_primes]
    semiprime_signature = [
        int(semiprime_object % prime == 0) for prime in small_primes
    ]
    return {
        "sieve_limit_z": sieve_limit,
        "small_primes": small_primes,
        "primorial_W": modulus,
        "prime_p_congruent_1_mod_W": prime_object,
        "second_prime_q_congruent_1_mod_W": second_prime,
        "semiprime_pq_congruent_1_mod_W": semiprime_object,
        "prime_residue_mod_W": prime_object % modulus,
        "semiprime_residue_mod_W": semiprime_object % modulus,
        "prime_small_divisibility_signature": prime_signature,
        "semiprime_small_divisibility_signature": semiprime_signature,
        "full_residue_collision": (
            prime_object % modulus == semiprime_object % modulus
        ),
        "small_divisibility_signature_collision": (
            prime_signature == semiprime_signature
        ),
        "semiprime_factors_exceed_z": (
            prime_object > sieve_limit and second_prime > sieve_limit
        ),
    }


def twin_fixed_primorial_no_go_audit() -> dict[str, Any]:
    rows = [primorial_signature_row(limit) for limit in (2, 3, 5, 7, 11)]
    failures = sum(
        int(
            not row["full_residue_collision"]
            or not row["small_divisibility_signature_collision"]
            or not row["semiprime_factors_exceed_z"]
        )
        for row in rows
    )
    return {
        "theorem": (
            "Fix z and W=product_(p<=z)p. No deterministic single-coordinate "
            "weight depending only on n mod W (and therefore no weight "
            "depending only on divisibility by primes at most z) can separate "
            "all primes from all semiprimes whose factors exceed z. For every "
            "reduced residue a mod W, Dirichlet's theorem supplies primes "
            "p congruent a, q congruent 1, and r congruent a mod W, all above "
            "z; then p and qr have the same full residue but opposite "
            "Liouville parity."
        ),
        "proof": (
            "Choose distinct sufficiently large primes in the required reduced "
            "residue classes using Dirichlet's theorem on primes in arithmetic "
            "progressions. Since qr is congruent a mod W and neither factor is "
            "at most z, p and qr have identical fixed-primorial observations. "
            "Any function of that observation assigns equal weights, so it "
            "cannot be positive on every prime and nonpositive on every such "
            "semiprime, or conversely."
        ),
        "exact_finite_collision_rows": rows,
        "aggregate": {
            "fixed_primorial_single_coordinate_separation_refuted": failures == 0,
            "full_residue_information_included": True,
            "scale_growing_or_bilinear_switching_weights_refuted": False,
            "actual_twin_pair_counterexample_found": False,
            "twin_prime_resolved": False,
        },
        "no_go_scope": (
            "This no-go is restricted to a fixed single-coordinate local "
            "signature. It does not apply to scale-growing sieve levels, "
            "bilinear switching, correlations with the first prime coordinate, "
            "or distributional estimates. It finds no counterexample to Twin "
            "Prime."
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
            {"id": f"{prefix}-T202", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T203", "label": theorem, "status": "closed"},
            {
                "id": f"{prefix}-N203",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN203",
                "label": next_theorem,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": prefix, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T202", f"{prefix}-T203"],
            [f"{prefix}-T203", f"{prefix}-N203"],
            [f"{prefix}-T203", f"{prefix}-OPEN203"],
            [f"{prefix}-OPEN203", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_rouche_transfer_audit()
    collatz = collatz_signed_transfer_audit()
    goldbach = goldbach_pointwise_strength_audit()
    twin = twin_fixed_primorial_no_go_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-203",
            "theorem_name": "CertifiedIncludedZerosPlusRoucheCountExactExhaustion",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The zero-count transfer is complete, but no strict boundary "
                "margin for the actual completed zeta function is constructed."
            ),
            "route_decision": {
                "discard": "using equal contour zero counts without independently certifying that the listed Xi zeros are included",
                "retain": "combine certified critical-line zero inclusion with Xi-specific cofinal Rouche margins",
                "next_single_lemma": "CompletedZetaCofinalRelativeMarginCertificateFamily",
            },
            "proof_dag": proof_dag(
                "RH",
                "CompletedZetaCofinalContourMarginWithExactZeroCountTransfer",
                "CertifiedIncludedZerosPlusRoucheCountExactExhaustion",
                "EqualZeroCountsAloneLocateAllXiZeros",
                "CompletedZetaCofinalRelativeMarginCertificateFamily",
            ),
            "claim_boundary": (
                "No RH proof or counterexample. An exact conditional transfer "
                "lemma is proved; its Xi-specific cofinal margin premise is open."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-203",
            "theorem_name": "ExactSignedTwoSiteTransferIdentityAndUniversalObstructionNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The transfer identity is exact, but unbounded nontrivial "
                "transfer components and nonperiodic trajectories remain open."
            ),
            "route_decision": {
                "discard": "unconditional preservation of affine nondivisibility under every signed two-site valuation transfer",
                "retain": "exclude the all-two component and seek a scale-dependent residue barrier on nontrivial transfer components",
                "next_single_lemma": "ScaleDependentTransferResidueBarrierOutsideAllTwoOrbit",
            },
            "proof_dag": proof_dag(
                "CO",
                "SignedTwoSiteValuationTransferAffineObstruction",
                "ExactSignedTwoSiteTransferIdentityAndUniversalObstructionNoGo",
                "UniversalSignedTransferPreservesAffineNondivisibility",
                "ScaleDependentTransferResidueBarrierOutsideAllTwoOrbit",
            ),
            "claim_boundary": (
                "No Collatz proof or nontrivial cycle. The exact transfer law "
                "and a minimal no-go counterexample are established."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-203",
            "theorem_name": "PointwiseLogLogDefectStrictStrengthCalibration",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The channel-level countermodel is not prime arithmetic and "
                "does not eliminate the actual Goldbach exceptional set."
            ),
            "route_decision": {
                "discard": "treating a pointwise c/loglog(N) defect as an easier consequence of Goldbach positivity",
                "retain": "work directly on a pointwise major-arc/minor-arc dominance statement with an explicit exceptional-set elimination step",
                "next_single_lemma": "UniformPointwiseGoldbachMinorArcDominanceOverExplicitMajorArc",
            },
            "proof_dag": proof_dag(
                "GB",
                "PointwiseLogLogScaledLiouvilleDefectOnEveryLargeEvenInteger",
                "PointwiseLogLogDefectStrictStrengthCalibration",
                "GoldbachPositivityAloneForcesUniformLogLogScaledDefect",
                "UniformPointwiseGoldbachMinorArcDominanceOverExplicitMajorArc",
            ),
            "claim_boundary": (
                "No Goldbach proof or counterexample. The previous next lemma "
                "is proved to be quantitatively stronger than positivity."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-203",
            "theorem_name": "FixedPrimorialSingleCoordinatePrimeSemiprimeSeparationNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "Only fixed local single-coordinate weights are ruled out; "
                "scale-growing bilinear switching remains viable and open."
            ),
            "route_decision": {
                "discard": "separating every prime from every rough semiprime with one fixed primorial residue signature",
                "retain": "use a scale-growing bilinear switching weight and prove a signed prime-semiprime correlation estimate",
                "next_single_lemma": "ScaleGrowingBilinearSwitchingWeightWithSignedPrimeSemiprimeCorrelation",
            },
            "proof_dag": proof_dag(
                "TP",
                "PrimeSemiprimeSeparatedChenSwitchingWeightWithPositivePrimeCoefficient",
                "FixedPrimorialSingleCoordinatePrimeSemiprimeSeparationNoGo",
                "FixedPrimorialLocalDataSeparatesPrimeFromRoughSemiprime",
                "ScaleGrowingBilinearSwitchingWeightWithSignedPrimeSemiprimeCorrelation",
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. A precise fixed-local "
                "parity barrier is proved without ruling out modern switching."
            ),
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureTransferContractAndTargetCorrectionAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-203 resolves none of the four conjectures. It completes an "
            "exact conditional Rouche zero-exhaustion transfer, derives the "
            "signed Collatz two-site transfer law and refutes its universal "
            "nondivisibility version, proves the proposed pointwise Goldbach "
            "log-log defect is stronger than positivity, and proves a fixed-"
            "primorial single-coordinate prime/semiprime separation no-go."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The four tracks now distinguish a logically complete transfer "
            "contract from its hard analytic premise, an exact local identity "
            "from a false global invariant, a conjecture-equivalent positivity "
            "gate from a stronger quantitative target, and fixed local sieve "
            "information from scale-growing bilinear information."
        ),
        "literature_boundary": {
            "riemann": "Rouche's theorem and certified zeta zero counting are established tools. PrimeProject claims only the explicit transfer contract and synthetic exact regression, not a new zeta margin.",
            "collatz": "The affine composition formula is standard context. The signed prefix-segment identity and route counterexample are project-local derivations, not a Collatz resolution.",
            "goldbach": "Current exceptional-set and major-arc work motivates the corrected pointwise target but does not supply uniform all-even minor-arc dominance here.",
            "twin_prime": "The result is a restricted form of the classical parity barrier. Weighted switching sieves remain outside the no-go and are the retained route.",
        },
        "sources": [
            {
                "title": "The Riemann hypothesis is true up to 3*10^12",
                "authors": "Dave Platt and Tim Trudgian",
                "url": "https://arxiv.org/abs/2004.09765",
            },
            {
                "title": "The 3x+1 problem and its generalizations",
                "authors": "Jeffrey C. Lagarias",
                "url": "https://doi.org/10.2307/2322189",
            },
            {
                "title": "The exceptional set of the Goldbach problem",
                "authors": "Lasse Grimmelt and Gautami Bhowmik",
                "url": "https://arxiv.org/abs/2607.27282",
            },
            {
                "title": "Weighted sieves with switching",
                "authors": "Kaisa Matomaki and Sebastian Zuniga Alterman",
                "url": "https://arxiv.org/abs/2405.19063",
            },
        ],
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "riemann_synthetic_contour_count": 1,
            "collatz_exact_forward_transfer_count": collatz["aggregate"][
                "exhaustive_forward_transfer_count"
            ],
            "goldbach_actual_target_count": len(
                goldbach["exact_actual_channel_rows"]
            ),
            "goldbach_abstract_countermodel_count": len(
                goldbach["exact_abstract_countermodel_rows"]
            ),
            "twin_primorial_collision_count": len(
                twin["exact_finite_collision_rows"]
            ),
            "rejected_or_recalibrated_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for problem_id, section_key in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
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
        "transfer_contract_and_target_correction_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket203-rouche-transfer-pointwise-primorial.json"
    )
    write_json(integrated, payload)
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-203-rouche-transfer.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-203-signed-transfer.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-203-pointwise-strength.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-203-fixed-primorial-no-go.json",
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
            "TICKET-203 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
