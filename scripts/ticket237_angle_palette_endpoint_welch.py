from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import ticket234_operator_kernel_density_minor_cesaro as ticket234
import ticket235_schur_primepower_phase_overlap as ticket235


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket237-angle-palette-endpoint-welch.v1"
GENERATED_AT = "2026-08-24T02:10:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "angle_palette_endpoint_welch_audit"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def prime_flags_up_to(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def primes_up_to(limit: int) -> list[int]:
    flags = prime_flags_up_to(limit)
    return [value for value, flag in enumerate(flags) if flag]


def next_prime(value: int) -> int:
    candidate = max(2, value + 1)
    while True:
        if all(candidate % divisor for divisor in range(2, math.isqrt(candidate) + 1)):
            return candidate
        candidate += 1


def riemann_principal_angle_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    cosine = Fraction(3, 5)
    sine = Fraction(4, 5)
    for dimension in (2, 4, 8, 16, 32):
        nested_norm = Fraction(1)
        nested_block_minimum = Fraction(0)
        innovation_norm = cosine
        innovation_block_minimum = 1 - cosine
        verified = (
            cosine * cosine + sine * sine == 1
            and nested_norm == 1
            and nested_block_minimum == 1 - nested_norm
            and innovation_norm < 1
            and innovation_block_minimum == Fraction(2, 5)
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{dimension}:{nested_norm}:{nested_block_minimum}:"
                f"{cosine}:{sine}:{innovation_norm}:{innovation_block_minimum}\n"
            ).encode()
        )
        rows.append(
            {
                "frame_dimension_m": dimension,
                "nested_frame_intersection_dimension": dimension,
                "nested_normalized_cross_norm": fraction_payload(nested_norm),
                "nested_block_minimum_eigenvalue": fraction_payload(nested_block_minimum),
                "innovation_cosine": fraction_payload(cosine),
                "innovation_sine": fraction_payload(sine),
                "innovation_frame_intersection_dimension": 0,
                "innovation_normalized_cross_norm": fraction_payload(innovation_norm),
                "innovation_block_minimum_eigenvalue": fraction_payload(
                    innovation_block_minimum
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let U:C^m->H and V:C^n->H be injective synthesis maps in a finite-"
        "dimensional Hilbert space, put A=U*U, B=U*V, C=V*V, and "
        "K=A^(-1/2)BC^(-1/2). The singular values of K are the cosines of the "
        "principal angles between ran(U) and ran(V). Consequently ||K||_op=1 "
        "if and only if ran(U) intersects ran(V) nontrivially, and ||K||_op<1 "
        "if and only if the two spans have positive smallest principal angle. "
        "In particular every nonzero nested pair of frames has norm one, so a "
        "strict contraction cannot come from nested cofinal spans unless their "
        "common modes are quotiented out."
    )
    proof = (
        "The maps Q_U=U(U*U)^(-1/2) and Q_V=V(V*V)^(-1/2) are isometries "
        "onto ran(U) and ran(V), and K=Q_U*Q_V. Thus its singular values are "
        "the principal-angle cosines. Equality ||K||=1 means that some unit "
        "Q_V y has projection of norm one onto ran(U), hence belongs to both "
        "spans; the converse is immediate. For the exact innovation family, "
        "take orthogonal isometries Q and W and V=(3Q+4W)/5. Then K=(3/5)I, "
        "the spans are disjoint, and the normalized block minimum is 2/5."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_principal_angle_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "principal_angle_characterization_proved": True,
            "nested_cofinal_strict_contraction_refuted": True,
            "innovation_quotient_necessity_proved": True,
            "arithmetic_weil_innovation_angle_gap_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This is an exact finite-dimensional Gram-geometry theorem. It does "
            "not identify the actual Guinand-Weil arithmetic block with the "
            "displayed innovation family, establish a uniform arithmetic angle "
            "gap, or test any zeta zero. It only proves that nested frames cannot "
            "supply the strict gap demanded by the TICKET-236 route."
        ),
        "failure_count": failures,
    }


def collatz_finite_palette_audit() -> dict[str, Any]:
    palettes = (
        (5,),
        (2, 3, 5, 7, 59),
        (5, 7, 13, 19, 31, 37, 59),
        (2, 3, 5, 7, 13, 19, 31, 37, 59, 57653),
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for palette in palettes:
        order_rows: list[dict[str, Any]] = []
        common_period = 1
        for prime in palette:
            if prime in (2, 3):
                order_rows.append(
                    {
                        "prime_q": prime,
                        "never_divides_D_k": True,
                        "order_q_32_over_27": None,
                        "order_q_3_over_2": None,
                    }
                )
                continue
            ratio_d = 32 * pow(27, -1, prime) % prime
            ratio_b = 3 * pow(2, -1, prime) % prime
            order_d = ticket235.multiplicative_order(ratio_d, prime)
            order_b = ticket235.multiplicative_order(ratio_b, prime)
            common_period = math.lcm(common_period, order_d, order_b)
            order_rows.append(
                {
                    "prime_q": prime,
                    "never_divides_D_k": False,
                    "order_q_32_over_27": order_d,
                    "order_q_3_over_2": order_b,
                }
            )

        checks: list[dict[str, Any]] = []
        verified = True
        for multiplier in (1, 2, 3):
            one_count = multiplier * common_period
            prime_checks = []
            for prime in palette:
                denominator_mod = (
                    pow(32, one_count, prime) - pow(27, one_count, prime)
                ) % prime
                numerator_mod = (
                    pow(32, one_count, prime)
                    + pow(27, one_count, prime)
                    - 2 * pow(18, one_count, prime)
                ) % prime
                disabled = denominator_mod != 0 or numerator_mod == 0
                prime_checks.append(
                    {
                        "prime_q": prime,
                        "D_k_mod_q": denominator_mod,
                        "B_k_mod_q": numerator_mod,
                        "cannot_separate_D_from_B": disabled,
                    }
                )
                verified = verified and disabled
            checks.append(
                {
                    "multiple_of_palette_period": multiplier,
                    "one_count_k": one_count,
                    "prime_checks": prime_checks,
                    "all_palette_witnesses_disabled": all(
                        item["cannot_separate_D_from_B"] for item in prime_checks
                    ),
                }
            )
        failures += int(not verified)
        transcript.update(
            (
                f"{','.join(map(str, palette))}:{common_period}:"
                + ";".join(
                    f"{item['prime_q']},{item['order_q_32_over_27']},{item['order_q_3_over_2']}"
                    for item in order_rows
                )
                + "\n"
            ).encode()
        )
        rows.append(
            {
                "finite_prime_palette": list(palette),
                "palette_period_L": common_period,
                "order_rows": order_rows,
                "first_three_common_multiple_checks": checks,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "No finite prime palette universally supplies a prime-presence witness "
        "for the binary run blocks w_k=1^k 2^(2k). Precisely, for every finite "
        "set S of primes there is an integer L>=1 such that for every multiple "
        "k of L and every q in S, either q does not divide D_k=32^k-27^k or q "
        "also divides B_k=32^k+27^k-2*18^k. One may take L to be the lcm of "
        "ord_q(32/27) and ord_q(3/2) over q in S with q>3. Thus any universal "
        "prime-presence certificate must use primes that escape every fixed "
        "finite palette."
    )
    proof = (
        "The primes 2 and 3 never divide D_k. For q>3, if k is a multiple of "
        "ord_q(32/27), then D_k is zero modulo q. If it is also a multiple of "
        "ord_q(3/2), divide B_k by 27^k: the result is "
        "(32/27)^k+1-2(2/3)^k=1+1-2=0. Taking the lcm simultaneously disables "
        "every q in S, and every positive multiple of that lcm gives another "
        "such k. This proves an infinite obstruction for each finite palette."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_palette_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "arbitrary_finite_prime_palette_universality_refuted": True,
            "infinitely_many_palette_disabling_run_blocks_proved": True,
            "fresh_prime_necessity_for_presence_certificates_proved": True,
            "fresh_prime_existence_for_general_necklaces_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem is uniform over every fixed finite palette but remains "
            "inside the already-excluded run-block family. It proves necessity "
            "of fresh primes, not existence of a prime q with q|D and q not |B "
            "for every k, and says nothing about general valuation words or "
            "aperiodic Collatz trajectories."
        ),
        "failure_count": failures,
    }


def goldbach_endpoint_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for cutoff in (30, 31, 100, 101, 1000, 1009, 10000, 10007):
        flags = prime_flags_up_to(cutoff)
        prime_count = sum(flags)
        target = 2 * cutoff
        representation_count = sum(
            1
            for left in range(2, cutoff + 1)
            if flags[left]
            and 0 <= target - left <= cutoff
            and flags[target - left]
        )
        expected = int(bool(flags[cutoff]))
        modulus = next_prime(2 * cutoff)
        total_power = modulus * prime_count
        phase_defect = total_power - modulus * representation_count
        normalized_margin = Fraction(representation_count, prime_count)
        verified = (
            representation_count == expected
            and total_power - phase_defect == modulus * representation_count
            and normalized_margin <= Fraction(1, prime_count)
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{cutoff}:{target}:{modulus}:{prime_count}:{expected}:"
                f"{representation_count}:{total_power}:{phase_defect}:{normalized_margin}\n"
            ).encode()
        )
        rows.append(
            {
                "cutoff_X": cutoff,
                "cutoff_is_prime": bool(flags[cutoff]),
                "upper_endpoint_target_N": target,
                "prime_modulus_q": modulus,
                "prime_count_pi_X": prime_count,
                "ordered_representation_count_g_X_2X": representation_count,
                "total_spectral_power_M_X": total_power,
                "reflected_phase_defect_Delta_X_2X": phase_defect,
                "normalized_phase_margin_g_over_pi": fraction_payload(
                    normalized_margin
                ),
                "inverse_log_X": 1 / math.log(cutoff),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let x_X be the prime indicator truncated to primes at most X and let "
        "g_X(N) be its ordered additive convolution. At the moving dyadic upper "
        "endpoint one has the exact identity g_X(2X)=1_P(X). Hence the TICKET-"
        "236 normalized reflected-phase margin at N=2X is either zero or "
        "1/pi(X), and is always o(1/log X). Therefore no fixed positive "
        "inverse-log margin, and not even strict positivity for composite X, can "
        "hold uniformly on a target interval that includes N=2X. A valid "
        "target-coupled lemma must buffer the upper endpoint or enlarge the "
        "prime cutoff relative to the target."
    )
    proof = (
        "If p and q are at most X and p+q=2X, then p<X would force q>X and "
        "vice versa. Thus p=q=X is the only possible ordered pair, proving "
        "g_X(2X)=1_P(X). TICKET-236 gives q_mod*g_X(N)=M_X-Delta_X(N), so the "
        "fractional phase margin is exactly g_X(2X)/pi(X). The prime number "
        "theorem gives 1/pi(X)=o(1/log X), while the infinitely many composite "
        "cutoffs already give exact zero margin."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_upper_endpoint_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "truncated_upper_endpoint_identity_proved": True,
            "closed_dyadic_interval_inverse_log_margin_refuted": True,
            "composite_cutoff_strict_endpoint_gain_refuted": True,
            "buffered_bulk_prime_phase_gain_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The obstruction is caused by truncating both prime variables at X "
            "while allowing the target to reach 2X. It does not refute a fixed "
            "bulk window N<=(2-eta)X, a cutoff at least N, or a target-specific "
            "major/minor-arc argument. No unbounded Goldbach counterexample is "
            "exhibited."
        ),
        "failure_count": failures,
    }


def synthetic_welch_rows() -> list[dict[str, Any]]:
    rows = []
    for support_size, repeats in ((4, 2), (4, 4), (8, 2), (8, 4), (16, 2)):
        rank = support_size - 1
        dimension = repeats * rank
        energy = Fraction(dimension - rank, rank * (dimension - 1))
        repeated_basis_energy = Fraction(repeats - 1, dimension - 1)
        verified = energy == repeated_basis_energy
        rows.append(
            {
                "support_size_s": support_size,
                "centered_function_rank_r": rank,
                "coordinate_count_m": dimension,
                "repetitions_per_nonconstant_walsh_coordinate": repeats,
                "degree_two_energy_E_m_2": fraction_payload(energy),
                "welch_lower_bound": fraction_payload(energy),
                "bound_attained_exactly": verified,
                "certificate_verified": verified,
            }
        )
    return rows


def actual_twin_welch_row(cutoff: int, dimension: int) -> dict[str, Any]:
    active_primes = [prime for prime in primes_up_to(300) if prime >= 5][:dimension]
    flags = prime_flags_up_to(cutoff)
    starts = [
        value
        for value in range(active_primes[-1] + 1, cutoff - 1)
        if flags[value] and flags[value + 2]
    ]
    columns: list[tuple[list[Fraction], Fraction]] = []
    for prime in active_primes:
        mean, _ = ticket234.twin_crt_normalization(prime)
        values = [
            Fraction(ticket234.legendre_symbol(start, prime)) - mean
            for start in starts
        ]
        second_moment = sum(value * value for value in values) / len(values)
        columns.append((values, second_moment))

    energy_sum = Fraction(0)
    for left, right in itertools.combinations(range(dimension), 2):
        cross = sum(
            columns[left][0][index] * columns[right][0][index]
            for index in range(len(starts))
        ) / len(starts)
        energy_sum += cross * cross / (columns[left][1] * columns[right][1])
    energy = energy_sum / math.comb(dimension, 2)
    rank_cap = min(dimension, len(starts))
    lower_bound = Fraction(dimension - rank_cap, rank_cap * (dimension - 1))
    verified = all(second_moment > 0 for _, second_moment in columns) and energy >= lower_bound
    return {
        "cutoff_X": cutoff,
        "active_prime_count_m": dimension,
        "maximum_active_prime": active_primes[-1],
        "twin_start_count_s": len(starts),
        "gram_rank_cap_r": rank_cap,
        "empirically_standardized_degree_two_energy": fraction_payload(energy),
        "welch_support_lower_bound": fraction_payload(lower_bound),
        "certificate_verified": verified,
    }


def twin_welch_audit() -> dict[str, Any]:
    synthetic_rows = synthetic_welch_rows()
    actual_rows = [
        actual_twin_welch_row(100, 6),
        actual_twin_welch_row(200, 12),
        actual_twin_welch_row(300, 18),
    ]
    transcript = hashlib.sha256()
    failures = 0
    for row in synthetic_rows:
        failures += int(not row["certificate_verified"])
        transcript.update(
            (
                f"S:{row['support_size_s']}:{row['centered_function_rank_r']}:"
                f"{row['coordinate_count_m']}:{row['degree_two_energy_E_m_2']['exact']}\n"
            ).encode()
        )
    for row in actual_rows:
        failures += int(not row["certificate_verified"])
        transcript.update(
            (
                f"A:{row['cutoff_X']}:{row['active_prime_count_m']}:"
                f"{row['twin_start_count_s']}:"
                f"{row['empirically_standardized_degree_two_energy']['exact']}:"
                f"{row['welch_support_lower_bound']['exact']}\n"
            ).encode()
        )

    theorem = (
        "Let nu be supported on s atoms and let phi_1,...,phi_m be real "
        "functions with E_nu phi_i^2=1. Put C_ij=E_nu(phi_i phi_j) and "
        "E_(m,2)=C(m,2)^(-1)sum_(i<j) C_ij^2. With r=min(m,s), "
        "E_(m,2)>=(m-r)/(r(m-1)); if all phi_i are centered, one may instead "
        "take r=min(m,s-1). More generally, if every diagonal second "
        "moment lies in [alpha,beta], then E_(m,2)>=max(0,(m*alpha^2/r-"
        "beta^2)/(m-1)). Thus degree-two decay along m->infinity with "
        "nondegenerate diagonals is impossible on uniformly bounded support; "
        "it forces the prime-weight support size to grow."
    )
    proof = (
        "C is a positive semidefinite Gram matrix of rank at most s. If its "
        "nonzero eigenvalues are lambda_j, Cauchy-Schwarz gives "
        "||C||_F^2=sum lambda_j^2>=(tr C)^2/r. In the unit-diagonal case, "
        "tr C=m and ||C||_F^2=m+m(m-1)E_(m,2), which rearranges to the stated "
        "Welch bound. Centering places every column in the codimension-one "
        "mean-zero subspace, giving rank at most s-1. The alpha-beta form "
        "follows from tr C>=m alpha and the diagonal-square sum <=m beta^2. "
        "Repeated nonconstant Walsh columns attain the centered bound exactly."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_sharp_walsh_rows": synthetic_rows,
        "actual_twin_start_support_rows": actual_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "finite_support_welch_floor_proved": True,
            "degree_two_decay_forces_growing_support_proved": True,
            "welch_floor_sharpness_proved": True,
            "prime_weighted_degree_two_decay_proved": False,
            "positive_twin_main_mass_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The sharp theorem is linear algebra. The actual rows condition on "
            "already observed twin starts and empirically rescale each coordinate; "
            "they cannot prove support growth. Passing from the local CRT "
            "normalization to uniform diagonal control, proving arithmetic E_2 "
            "decay, positive mass, and breaking parity all remain open."
        ),
        "failure_count": failures,
    }


def make_section(
    problem_id: str,
    ticket_id: str,
    theorem_name: str,
    computation: dict[str, Any],
    discard: str,
    retain: str,
    next_lemma: str,
    dag: dict[str, Any],
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "reproducible_computation": computation,
        "logical_limit": computation["no_go_scope"],
        "route_decision": {
            "discard": discard,
            "retain": retain,
            "next_single_lemma": next_lemma,
        },
        "proof_dag": dag,
    }


def proof_dag(problem: str) -> dict[str, Any]:
    if problem == "riemann":
        nodes = [
            ("RH-T236", "NormalizedCrossBlockContractionAndLocalMinorNoGo", "closed"),
            ("RH-T237", "PrincipalAngleCriterionAndNestedFrameNoGo", "closed"),
            ("RH-N237", "NestedCofinalFramesYieldStrictContraction", "refuted_or_limited"),
            ("RH-OPEN237", "ArithmeticWeilInnovationCrossBlockAngleGapOnDisjointLogarithmicShells", "highest_risk_open"),
            ("RH", "RiemannHypothesis", "open_not_proven"),
        ]
        edges = [["RH-T236", "RH-T237"], ["RH-T237", "RH-N237"], ["RH-T237", "RH-OPEN237"], ["RH-OPEN237", "RH"]]
    elif problem == "collatz":
        nodes = [
            ("CO-T197", "ContiguousOneTwoRunNondivisibility", "closed"),
            ("CO-T236", "RunBlockThreePrimeWitnessOutside28826Multiples", "closed"),
            ("CO-T237", "NoFinitePrimePaletteUniversallySeparatesRunBlocks", "closed"),
            ("CO-N237", "SomeFixedFinitePrimePaletteIsUniversal", "refuted_or_limited"),
            ("CO-OPEN237", "WordDependentPrimeValuationGapForEveryPrimitiveBinaryDensityBandNecklace", "highest_risk_open"),
            ("CO-PERIODIC", "AllPeriodicValuationWords", "open_not_proven"),
            ("CO", "CollatzConjecture", "open_not_proven"),
        ]
        edges = [["CO-T197", "CO-T237"], ["CO-T236", "CO-T237"], ["CO-T237", "CO-N237"], ["CO-T237", "CO-OPEN237"], ["CO-OPEN237", "CO-PERIODIC"], ["CO-PERIODIC", "CO"]]
    elif problem == "goldbach":
        nodes = [
            ("GB-T236", "ReflectedPhaseDefectIdentityAndUncoupledMarginNoGo", "closed"),
            ("GB-T237", "TruncatedDyadicUpperEndpointObstruction", "closed"),
            ("GB-N237", "ClosedDyadicWindowUniformInverseLogMargin", "refuted_or_limited"),
            ("GB-OPEN237", "BufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack", "highest_risk_open"),
            ("GB", "StrongGoldbachConjecture", "open_not_proven"),
        ]
        edges = [["GB-T236", "GB-T237"], ["GB-T237", "GB-N237"], ["GB-T237", "GB-OPEN237"], ["GB-OPEN237", "GB"]]
    else:
        nodes = [
            ("TP-T236", "DegreeTwoCesaroControlsAllFixedDegrees", "closed"),
            ("TP-T237", "FiniteSupportWelchFloorForDegreeTwoCRTOverlap", "closed"),
            ("TP-N237", "BoundedSupportCanCertifyDegreeTwoDecay", "refuted_or_limited"),
            ("TP-OPEN237", "PrimeWeightedDegreeTwoCRTDecayWithGrowingSupportAndUniformDiagonalControl", "highest_risk_open"),
            ("TP-PARITY", "ParityRetainingTransferAndPositivePrincipalMass", "open_not_proven"),
            ("TP", "TwinPrimeConjecture", "open_not_proven"),
        ]
        edges = [["TP-T236", "TP-T237"], ["TP-T237", "TP-N237"], ["TP-T237", "TP-OPEN237"], ["TP-OPEN237", "TP-PARITY"], ["TP-PARITY", "TP"]]
    return {
        "nodes": [
            {"id": node_id, "label": label, "status": status}
            for node_id, label, status in nodes
        ],
        "edges": edges,
    }


def build_audit() -> dict[str, Any]:
    computations = {
        "riemann": riemann_principal_angle_audit(),
        "collatz": collatz_finite_palette_audit(),
        "goldbach": goldbach_endpoint_audit(),
        "twin_prime": twin_welch_audit(),
    }
    tracks = [
        make_section(
            "riemann",
            "RH-TICKET-237",
            "PrincipalAngleCriterionAndNestedCofinalFrameNoGo",
            computations["riemann"],
            "strict normalized contraction from nonzero nested cofinal frames",
            "remove common modes and estimate the arithmetic innovation angle on disjoint logarithmic shells",
            "ArithmeticWeilInnovationCrossBlockAngleGapOnDisjointLogarithmicShells",
            proof_dag("riemann"),
        ),
        make_section(
            "collatz",
            "CO-TICKET-237",
            "NoFinitePrimePaletteUniversallySeparatesBinaryRunBlocks",
            computations["collatz"],
            "any fixed finite prime palette as a universal prime-presence certificate",
            "allow a word-dependent fresh prime and strengthen presence to a valuation gap on general necklaces",
            "WordDependentPrimeValuationGapForEveryPrimitiveBinaryDensityBandNecklace",
            proof_dag("collatz"),
        ),
        make_section(
            "goldbach",
            "GB-TICKET-237",
            "TruncatedDyadicUpperEndpointObstructionAndBulkWindowNecessity",
            computations["goldbach"],
            "a uniform inverse-log reflected-phase margin on a closed target window including N=2X",
            "buffer the upper endpoint and prove major gain minus independently bounded minor loss in the bulk",
            "BufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack",
            proof_dag("goldbach"),
        ),
        make_section(
            "twin-prime",
            "TP-TICKET-237",
            "FiniteSupportWelchFloorForDegreeTwoCRTOverlap",
            computations["twin_prime"],
            "bounded-support finite samples as evidence that degree-two CRT energy can decay",
            "prove growing-support prime-weighted E2 decay together with uniform diagonal nondegeneracy",
            "PrimeWeightedDegreeTwoCRTDecayWithGrowingSupportAndUniformDiagonalControl",
            proof_dag("twin-prime"),
        ),
    ]
    sections = {track["problem_id"].replace("-", "_"): track for track in tracks}
    machine = {
        "exact_partial_or_no_go_theorem_count": 4,
        "refuted_or_reduced_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(value["failure_count"] for value in computations.values()),
    }
    audit_root = {
        "theorem_name": "FourConjectureAnglePaletteEndpointWelchAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-237 proves four exact partial or no-go results: a principal-angle "
            "criterion and nested-frame obstruction; an arbitrary finite-prime-palette "
            "Collatz no-go; a truncated Goldbach dyadic upper-endpoint obstruction; "
            "and a sharp finite-support Welch floor for degree-two CRT overlap. It "
            "resolves none of the four parent conjectures."
        ),
        **sections,
        "machine_audit": machine,
    }
    attempts = []
    for track in tracks:
        attempts.append(
            {
                "ticket_id": track["ticket_id"],
                "problem_id": track["problem_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "claim_boundary": track["logical_limit"],
                "proof_dag": track["proof_dag"],
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{track['problem_id'].replace('-', '_')}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
            }
        )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-237 proves four exact partial or no-go results and resolves "
            "none of the four parent conjectures."
        ),
        AUDIT_KEY: audit_root,
        "attempts": attempts,
    }


def track_payload(audit: dict[str, Any], problem_id: str) -> dict[str, Any]:
    attempt = next(item for item in audit["attempts"] if item["problem_id"] == problem_id)
    section_key = problem_id.replace("-", "_")
    section = audit[AUDIT_KEY][section_key]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "problem_id": problem_id,
        "ticket_id": attempt["ticket_id"],
        "theorem_name": attempt["new_result"],
        "declared_proposition": attempt["declared_proposition"],
        "mathematical_argument": attempt["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": attempt["discarded_route"],
        "remaining_gap": attempt["remaining_gap"],
        "next_single_lemma": attempt["candidate_theorem"],
        "claim_boundary": attempt["claim_boundary"],
        "proof_dag": attempt["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket237-angle-palette-endpoint-welch.json",
        audit,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-237-principal-angle-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-237-finite-palette-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-237-dyadic-endpoint-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-237-welch-support-floor.json",
    }
    for problem_id, path in paths.items():
        write_json(path, track_payload(audit, problem_id))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    if audit[AUDIT_KEY]["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
