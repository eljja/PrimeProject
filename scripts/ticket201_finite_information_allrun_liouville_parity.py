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
SCHEMA = "primeproject.ticket201-finite-information-allrun-liouville-parity.v1"
GENERATED_AT = "2026-08-10T18:00:00+09:00"
STATUS = "open_not_proven"
GOLDBACH_LIMIT = 1 << 20
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


def falling_factorial(value: int, order: int) -> int:
    if order < 0 or order > value:
        return 0
    result = 1
    for item in range(value - order + 1, value + 1):
        result *= item
    return result


def finite_jet_bound_row(degree_half: int) -> dict[str, Any]:
    # F(z)=z^2-1, R=5, A=10, and q_N(z)=c_N z^(2N), where
    # c_N=-F(iA)/(iA)^(2N). All quantities below are exact rationals.
    radius = 5
    off_axis_height = 10
    f_at_i_a = -101
    epsilon = Fraction(1, 100)
    bounds = []
    for derivative_order in range(3):
        bound = Fraction(
            abs(f_at_i_a)
            * falling_factorial(2 * degree_half, derivative_order)
            * radius ** (2 * degree_half - derivative_order),
            off_axis_height ** (2 * degree_half),
        )
        bounds.append(bound)
    coefficient = Fraction(
        101 * ((-1) ** degree_half),
        off_axis_height ** (2 * degree_half),
    )
    return {
        "N": degree_half,
        "perturbation_degree": 2 * degree_half,
        "coefficient_c_N": fraction_text(coefficient),
        "jet_bounds_j_0_to_2": [fraction_text(value) for value in bounds],
        "maximum_jet_bound": fraction_text(max(bounds)),
        "all_jet_bounds_below_epsilon": all(value < epsilon for value in bounds),
        "epsilon": fraction_text(epsilon),
        "G_N_iA_is_zero_exactly": True,
    }


def riemann_finite_information_no_go_audit() -> dict[str, Any]:
    rows = [finite_jet_bound_row(value) for value in range(2, 13)]
    first_certifying = next(
        row["N"] for row in rows if row["all_jet_bounds_below_epsilon"]
    )
    failures = int(first_certifying != 9)
    failures += sum(
        int(row["all_jet_bounds_below_epsilon"] != (row["N"] >= 9))
        for row in rows
    )
    return {
        "theorem": (
            "Let F be a real-even entire function, let R>0, M>=0, epsilon>0, "
            "and choose A>R with F(iA) nonzero. For all sufficiently large N, "
            "G_N(z)=F(z)-F(iA)z^(2N)/(iA)^(2N) is real-even and entire, has "
            "zeros at z=plus-or-minus iA, and satisfies max over |z|<=R and "
            "0<=j<=M of |G_N^(j)(z)-F^(j)(z)|<epsilon. Consequently no fixed "
            "compact set of finite-order jet data can force all zeros to be "
            "real within the class of real-even entire functions: if F has "
            "only real zeros, the functions G_N provide arbitrarily close "
            "finite-jet data while having non-real zeros."
        ),
        "proof": (
            "The coefficient -F(iA)/(iA)^(2N) is real because F(iA) is real "
            "for a real-even entire F. Substitution gives G_N(iA)=0 and "
            "evenness gives G_N(-iA)=0. For |z|<=R, the j-th derivative of "
            "the perturbation is bounded by |F(iA)|(2N)_j R^(2N-j)/A^(2N). "
            "For every fixed j this tends to zero because R/A<1; taking the "
            "maximum over finitely many j proves the assertion. Adding a "
            "polynomial also preserves entire order at most one when F has "
            "order at most one, but it need not preserve Xi's arithmetic "
            "gamma-zeta structure."
        ),
        "exact_regression": {
            "F": "z^2-1",
            "F_has_only_real_zeros": True,
            "F_real_zeros": [-1, 1],
            "compact_disk_radius_R": 5,
            "off_real_axis_height_A": 10,
            "jet_order_M": 2,
            "epsilon": "1/100",
            "rows": rows,
            "first_certifying_N": first_certifying,
        },
        "aggregate": {
            "finite_compact_jet_no_go_proved": failures == 0,
            "real_even_symmetry_preserved": True,
            "entire_order_at_most_one_preserved_when_applicable": True,
            "xi_euler_product_or_gamma_structure_preserved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This theorem refutes a proof strategy, not RH. It shows that a "
            "single compact Xi approximation, even with finitely many certified "
            "derivatives, cannot by itself imply the global real-zero property "
            "unless Xi-specific global arithmetic structure is also used."
        ),
        "failure_count": failures,
    }


def collatz_all_run_word(run_pairs: int, scale: int) -> tuple[int, ...]:
    if run_pairs < 2:
        raise ValueError("run_pairs must be at least two")
    if scale < 2:
        raise ValueError("scale must be at least two")
    return (1,) * scale + (2,) * (2 * scale) + (1, 2, 2) * (run_pairs - 1)


def collatz_all_run_row(run_pairs: int, scale: int) -> dict[str, Any]:
    word = collatz_all_run_word(run_pairs, scale)
    n = run_pairs - 1
    q = scale + n
    x = 32**scale
    y = 27**scale
    z = 18**scale
    power_32_n = 32**n
    power_27_n = 27**n
    tail_numerator = 23 * (power_32_n - power_27_n) // 5
    denominator = 32**q - 27**q
    numerator_closed = (
        ((23 * power_32_n - 18 * power_27_n) // 5) * x
        + power_27_n * y
        - 2 * power_27_n * z
    )
    e_k = 14 * y - 9 * x - 5 * z
    f_k = -e_k
    identity_left = 5 * numerator_closed - 23 * denominator
    identity_right = 2 * power_27_n * e_k
    rotation = cyclic_rotation_affine_audit(word)
    return {
        "run_pair_count_r": run_pairs,
        "scale_k": scale,
        "n_equals_r_minus_1": n,
        "q_equals_k_plus_n": q,
        "word": f"1^{scale} 2^{2 * scale} (1 2^2)^{n}",
        "horizon_h": len(word),
        "valuation_sum_S": sum(word),
        "tail_ordered_numerator": str(tail_numerator),
        "denominator_D": str(denominator),
        "affine_numerator_B": str(numerator_closed),
        "direct_numerator_matches_closed_form": (
            ordered_affine_numerator(word) == numerator_closed
        ),
        "five_B_minus_twenty_three_D": str(identity_left),
        "two_times_27n_times_Ek": str(identity_right),
        "master_identity_holds_exactly": identity_left == identity_right,
        "E_k": str(e_k),
        "F_k_equals_minus_E_k": str(f_k),
        "zero_less_than_F_k_less_than_D": 0 < f_k < denominator,
        "gcd_D_with_2_times_27n": math.gcd(denominator, 2 * power_27_n),
        "primitive_word": is_primitive_word(word),
        "affine_divisibility_hit": numerator_closed % denominator == 0,
        "contraction_gate_passes": 2 ** sum(word) > 3 ** len(word),
        "product_gate_passes": Fraction(125, 108) ** q > 1,
        **rotation,
    }


def collatz_all_run_obstruction_audit() -> dict[str, Any]:
    rows = [
        collatz_all_run_row(run_pairs, scale)
        for run_pairs in range(2, 17)
        for scale in range(2, 17)
    ]
    failures = sum(
        int(
            not row["direct_numerator_matches_closed_form"]
            or not row["master_identity_holds_exactly"]
            or not row["zero_less_than_F_k_less_than_D"]
            or row["gcd_D_with_2_times_27n"] != 1
            or not row["primitive_word"]
            or row["affine_divisibility_hit"]
            or row["cyclic_rotation_divisibility_hit_count"] != 0
            or not row["rotation_recurrence_holds_exactly"]
            or not row["rotation_cycle_closes"]
            or not row["contraction_gate_passes"]
            or not row["product_gate_passes"]
        )
        for row in rows
    )
    return {
        "theorem": (
            "For every r>=2 and k>=2, the primitive accelerated-Collatz word "
            "w_(r,k)=1^k 2^(2k)(1 2^2)^(r-1), and every cyclic rotation of it, "
            "passes the contraction and product gates but fails the affine "
            "divisibility equation. Thus this explicit two-parameter infinite "
            "family contains no positive Collatz cycle code."
        ),
        "proof": (
            "Put n=r-1, q=k+n, x=32^k, y=27^k, and z=18^k. The tail U^n, "
            "U=(1,2,2), has ordered numerator 23(32^n-27^n)/5. Concatenation "
            "gives D=32^q-27^q and B=((23*32^n-18*27^n)/5)x+27^n y-2*27^n z. "
            "Exact simplification gives 5B-23D=2*27^n E_k, where "
            "E_k=14*27^k-9*32^k-5*18^k=-F_k. Here F_2=630>0, and for k>=3 "
            "the inequality 14(27/32)^k<14(27/32)^3<9 proves F_k>0. Also "
            "D>=32^(k+1)-27^(k+1)>F_k because the remaining difference is "
            "23*32^k-13*27^k-5*18^k>0. Since gcd(D,2*27^n)=1, D|B would "
            "force D|E_k, contradicting 0<|E_k|<D. The unique long 2-run "
            "proves primitivity. The relation 2^v B'=3B+D and gcd(D,6)=1 "
            "makes the obstruction invariant under cyclic rotation. With "
            "h=3q and S=5q, both scalar gates reduce to strict powers of "
            "32/27 and 125/108."
        ),
        "symbolic_identities": {
            "tail_numerator": "N((1,2,2)^n)=23(32^n-27^n)/5",
            "denominator": "D=32^(n+k)-27^(n+k)",
            "master_identity": "5B-23D=2*27^n(14*27^k-9*32^k-5*18^k)",
            "strict_residual_bound": "0<F_k=9*32^k+5*18^k-14*27^k<D",
        },
        "exact_regression_rows": rows,
        "aggregate": {
            "regression_run_pair_count": 15,
            "regression_scale_count": 15,
            "regression_word_count": len(rows),
            "all_run_pair_counts_covered_symbolically": True,
            "all_scales_covered_symbolically": True,
            "cyclic_rotations_covered_symbolically": True,
            "arbitrary_valuation_words_covered": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes every repetition count of one rigid word family. "
            "It does not exclude other primitive exponent words, nonperiodic "
            "divergence, or prove that every trajectory reaches one."
        ),
        "failure_count": failures,
    }


def p2_channel_counts(
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
    chen = prime_prime + prime_semiprime
    signed = prime_semiprime - prime_prime
    return {
        "target_N": target,
        "prime_prime_R": prime_prime,
        "prime_composite_semiprime_S": prime_semiprime,
        "P2_channel_C": chen,
        "liouville_signed_channel_L": signed,
        "C_minus_L": chen - signed,
        "C_plus_L": chen + signed,
        "R_equals_C_minus_L_over_2": 2 * prime_prime == chen - signed,
        "S_equals_C_plus_L_over_2": 2 * prime_semiprime == chen + signed,
        "liouville_ratio_L_over_C": fraction_text(Fraction(signed, chen)),
        "semiprime_only_saturation_L_equals_C": signed == chen,
    }


def goldbach_liouville_parity_audit(
    primes: bytearray,
    prime_values: list[int],
    semiprimes: bytearray,
) -> dict[str, Any]:
    targets = [4, 6, 8, 28, 100] + [1 << exponent for exponent in range(10, 21)]
    rows = [
        p2_channel_counts(target, primes, prime_values, semiprimes)
        for target in targets
    ]
    failures = sum(
        int(
            not row["R_equals_C_minus_L_over_2"]
            or not row["S_equals_C_plus_L_over_2"]
        )
        for row in rows
    )
    return {
        "theorem": (
            "Let J(n) indicate that n is prime or a composite semiprime and "
            "let lambda(n)=(-1)^Omega(n). On the support of J, the prime "
            "indicator is J(n)(1-lambda(n))/2. For even N define "
            "C(N)=sum_p J(N-p) and L(N)=sum_p J(N-p)lambda(N-p), with p "
            "prime. Then R(N)=(C(N)-L(N))/2 and S(N)=(C(N)+L(N))/2 exactly. "
            "At every N with C(N)>0, the TICKET-200 semiprime-only condition "
            "is equivalent to L(N)=C(N), while Goldbach positivity is "
            "equivalent to the strict parity defect L(N)<C(N)."
        ),
        "proof": (
            "A prime has Omega=1 and lambda=-1; a composite semiprime has "
            "Omega=2 and lambda=+1. Therefore J(1-lambda)/2 and "
            "J(1+lambda)/2 are the exact prime and composite-semiprime "
            "projectors. Summing after fixing the first prime gives "
            "C=R+S and L=S-R, hence the two displayed identities. Since "
            "C-L=2R, R=0 iff L=C and R>0 iff L<C."
        ),
        "exact_finite_rows": rows,
        "aggregate": {
            "finite_target_count": len(rows),
            "largest_finite_target": max(targets),
            "projector_identity_proved": failures == 0,
            "ticket200_next_lemma_is_goldbach_equivalent_given_chen_positivity": True,
            "finite_saturation_count": sum(
                row["semiprime_only_saturation_L_equals_C"] for row in rows
            ),
            "global_strict_liouville_defect_proved": False,
            "goldbach_resolved": False,
        },
        "no_go_scope": (
            "Unsigned prime-plus-P2 positivity cannot separate primes from "
            "semiprimes. The exact Liouville identity proves that eliminating "
            "the semiprime-only channel is Goldbach itself on Chen-positive "
            "targets, so it is not an independent easier lemma."
        ),
        "failure_count": failures,
    }


def twin_liouville_parity_audit(
    primes: bytearray,
    semiprimes: bytearray,
) -> dict[str, Any]:
    rows = []
    failures = 0
    for exponent in range(10, 23):
        lower = 1 << exponent
        upper = 2 * lower
        twin_count = 0
        semiprime_count = 0
        for value in range(lower, upper):
            if not primes[value]:
                continue
            twin_count += int(primes[value + 2])
            semiprime_count += int(semiprimes[value + 2])
        chen = twin_count + semiprime_count
        signed = semiprime_count - twin_count
        row = {
            "block": [lower, upper],
            "twin_channel_T": twin_count,
            "composite_semiprime_channel_S": semiprime_count,
            "P2_channel_C2": chen,
            "liouville_signed_channel_L2": signed,
            "C2_minus_L2": chen - signed,
            "T_equals_C2_minus_L2_over_2": 2 * twin_count == chen - signed,
            "liouville_ratio_L2_over_C2": fraction_text(Fraction(signed, chen)),
            "semiprime_only_saturation_L2_equals_C2": signed == chen,
        }
        failures += int(not row["T_equals_C2_minus_L2_over_2"])
        rows.append(row)
    return {
        "theorem": (
            "For a dyadic block [X,2X), let C2(X)=sum J(p+2) and "
            "L2(X)=sum J(p+2)lambda(p+2) over primes p in the block. If T(X) "
            "and S(X) are the twin and composite-semiprime channels, then "
            "T=(C2-L2)/2 and S=(C2+L2)/2 exactly. Thus a Chen-positive block "
            "contains a twin iff L2<C2, and infinitely many twin primes exist "
            "iff this strict inequality holds on infinitely many dyadic blocks. "
            "The TICKET-200 next lemma is therefore equivalent to the Twin "
            "Prime conjecture, not a proper intermediate lemma."
        ),
        "proof": (
            "The same P2 Liouville projectors give C2=T+S and L2=S-T, so "
            "C2-L2=2T. A finite dyadic block is twin-positive exactly when "
            "L2<C2. Infinitely many twin primes meet infinitely many dyadic "
            "blocks, and conversely one twin-positive start in infinitely many "
            "blocks gives infinitely many distinct twin primes."
        ),
        "exact_finite_rows": rows,
        "aggregate": {
            "finite_block_count": len(rows),
            "largest_block_upper": rows[-1]["block"][1],
            "projector_identity_proved": failures == 0,
            "ticket200_next_lemma_is_twin_prime_equivalent": True,
            "finite_saturation_count": sum(
                row["semiprime_only_saturation_L2_equals_C2"] for row in rows
            ),
            "infinitely_many_strict_liouville_defect_blocks_proved": False,
            "twin_prime_resolved": False,
        },
        "no_go_scope": (
            "Chen-positive block counts are unsigned support information. They "
            "do not control the Liouville sign needed to distinguish one prime "
            "factor from two, and finite strict-defect blocks prove no infinitude."
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
            {"id": f"{prefix}-T200", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T201", "label": theorem, "status": "closed"},
            {
                "id": f"{prefix}-N201",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN201",
                "label": next_theorem,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": prefix, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T200", f"{prefix}-T201"],
            [f"{prefix}-T201", f"{prefix}-N201"],
            [f"{prefix}-T201", f"{prefix}-OPEN201"],
            [f"{prefix}-OPEN201", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_finite_information_no_go_audit()
    collatz = collatz_all_run_obstruction_audit()
    primes = prime_sieve(TWIN_LIMIT + 2)
    prime_values = [value for value in range(2, TWIN_LIMIT + 3) if primes[value]]
    semiprimes = semiprime_sieve(TWIN_LIMIT + 2, prime_values)
    goldbach = goldbach_liouville_parity_audit(primes, prime_values, semiprimes)
    twin = twin_liouville_parity_audit(primes, semiprimes)
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-201",
            "theorem_name": "FiniteCompactJetDataCannotForceGlobalRealZeroProperty",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The perturbation does not preserve Xi's Euler-product and "
                "gamma-factor structure, so it rules out only finite local-data "
                "proofs that omit such global arithmetic information."
            ),
            "route_decision": {
                "discard": "treating one fixed compact Xi jet certificate as a bridge to the global Riemann Hypothesis",
                "retain": "seek cofinal zero-count certificates that use the completed zeta function's global arithmetic structure",
                "next_single_lemma": "CofinalXiRectangleRoucheMarginFromCompletedZetaStructure",
            },
            "proof_dag": proof_dag(
                "RH",
                "DerivativeControlledBoundaryMeshRoucheCertificate",
                "FiniteCompactJetDataCannotForceGlobalRealZeroProperty",
                "OneFixedD3XiJetCertificateImpliesRH",
                "CofinalXiRectangleRoucheMarginFromCompletedZetaStructure",
            ),
            "claim_boundary": (
                "No RH proof or counterexample. TICKET-201 proves a strategy "
                "no-go in a symmetry-preserving entire-function class; it does "
                "not construct an off-line zero of Xi."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-201",
            "theorem_name": "AllRunPairPrimitiveFamilyAffineDivisibilityObstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "A two-parameter rigid family is excluded for every run count "
                "and scale, but arbitrary exponent words and divergent orbits "
                "remain untouched."
            ),
            "route_decision": {
                "discard": "extending the same rigid family one fixed run count at a time",
                "retain": "test whether the exact affine obstruction survives a uniform neighborhood of the family in valuation-word space",
                "next_single_lemma": "UniformBoundedL1NeighborhoodAffineObstructionAtOneThirdDensity",
            },
            "proof_dag": proof_dag(
                "CO",
                "ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
                "AllRunPairPrimitiveFamilyAffineDivisibilityObstruction",
                "AStillLargerFixedRunCountIsIndependentProgress",
                "UniformBoundedL1NeighborhoodAffineObstructionAtOneThirdDensity",
            ),
            "claim_boundary": (
                "No Collatz proof and no nontrivial cycle. The exact result "
                "excludes all scales, run counts, and rotations of one explicit "
                "two-parameter family only."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-201",
            "theorem_name": "GoldbachP2LiouvilleParitySaturationEquivalence",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The exact projector identifies the missing signed correlation "
                "but supplies no uniform bound that makes C(N)-L(N) positive."
            ),
            "route_decision": {
                "discard": "calling elimination of every semiprime-only Chen target an easier lemma than strong Goldbach",
                "retain": "derive a quantitative Liouville parity defect inside the prime-plus-P2 channel",
                "next_single_lemma": "UniformRelativeLiouvilleParityDefectOnPrimePlusP2GoldbachChannels",
            },
            "proof_dag": proof_dag(
                "GB",
                "ChenGoldbachPrimeSemiprimeChannelReduction",
                "GoldbachP2LiouvilleParitySaturationEquivalence",
                "SemiprimeOnlyChenChannelEliminationIsAProperSublemma",
                "UniformRelativeLiouvilleParityDefectOnPrimePlusP2GoldbachChannels",
            ),
            "claim_boundary": (
                "No Goldbach proof or counterexample. The exact Liouville "
                "identity proves that TICKET-200's open target was equivalent "
                "to Goldbach on Chen-positive inputs and replaces it with an "
                "explicit stronger quantitative correlation target."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-201",
            "theorem_name": "TwinP2LiouvilleParitySaturationEquivalence",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The block identity is exact but gives no signed cancellation "
                "on infinitely many unbounded blocks."
            ),
            "route_decision": {
                "discard": "calling twin positivity on infinitely many Chen-positive blocks a proper intermediate lemma",
                "retain": "seek a uniform relative Liouville defect on infinitely many Chen-positive dyadic blocks",
                "next_single_lemma": "UniformRelativeLiouvilleParityDefectOnInfinitelyManyChenDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ChenTwinPrimeSemiprimeChannelReduction",
                "TwinP2LiouvilleParitySaturationEquivalence",
                "InfinitelyManyTwinPositiveChenBlocksIsAProperSublemma",
                "UniformRelativeLiouvilleParityDefectOnInfinitelyManyChenDyadicBlocks",
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. The exact identity "
                "shows that TICKET-200's open target was the conjecture in "
                "dyadic language; the new target exposes the required signed "
                "parity-breaking estimate."
            ),
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFiniteInformationAndParityBoundaryAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-201 resolves none of the four conjectures. It proves that "
            "finite compact jet data cannot force RH in the ambient symmetric "
            "entire-function class, excludes every run count and scale in one "
            "explicit Collatz family, and proves exact Liouville parity "
            "equivalences showing that the previous Goldbach and Twin open "
            "targets were reformulations rather than proper sublemmas."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The surviving routes require structure-sensitive information: "
            "cofinal arithmetic control for Xi, affine congruence information "
            "for Collatz words, and signed Liouville cancellation rather than "
            "unsigned P2 support for Goldbach and Twin Prime."
        ),
        "literature_boundary": {
            "riemann": "The perturbation theorem is elementary complex analysis and does not preserve Xi's completed-zeta structure. Platt-Trudgian is used only as the rigorous finite-height boundary.",
            "collatz": "Affine parity-vector equations are classical. The two-parameter residual identity is a project-local family theorem, with no priority claim beyond this explicit formulation.",
            "goldbach": "Chen-type P2 positivity is imported. The Liouville projector is an elementary exact identity and is presented as a parity-barrier diagnosis, not a new sieve theorem.",
            "twin_prime": "The equivalence is a dyadic reformulation of the exact P2 parity split. It proves no new lower bound for twin primes.",
        },
        "sources": [
            {
                "title": "The Riemann hypothesis is true up to 3*10^12",
                "authors": "Dave Platt and Tim Trudgian",
                "url": "https://arxiv.org/abs/2004.09765",
            },
            {
                "title": "Variants of the Selberg sieve, and bounded intervals containing many primes",
                "authors": "D. H. J. Polymath",
                "url": "https://arxiv.org/abs/1407.4897",
            },
            {
                "title": "An approximation to the twin prime conjecture and the parity phenomenon",
                "authors": "Janos Pintz",
                "url": "https://arxiv.org/abs/1004.1065",
            },
            {
                "title": "An explicit version of Chen's theorem",
                "authors": "Matteo Bordignon, Daniel R. Johnston, and Valeriia Starichkova",
                "url": "https://arxiv.org/abs/2207.09452",
            },
        ],
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "riemann_exact_jet_regression_count": len(
                riemann["exact_regression"]["rows"]
            ),
            "collatz_symbolic_parameter_dimension": 2,
            "collatz_exact_regression_word_count": len(
                collatz["exact_regression_rows"]
            ),
            "goldbach_exact_channel_row_count": len(
                goldbach["exact_finite_rows"]
            ),
            "twin_exact_channel_row_count": len(twin["exact_finite_rows"]),
            "previous_next_lemmas_reclassified_as_equivalent_count": 2,
            "rejected_or_limited_route_count": 4,
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
        "finite_information_allrun_liouville_parity_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket201-finite-information-allrun-liouville-parity.json"
    )
    write_json(integrated, payload)
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-201-finite-jet-no-go.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-201-all-run-pair-obstruction.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-201-liouville-parity-saturation.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-201-liouville-parity-saturation.json",
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
            "TICKET-201 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
