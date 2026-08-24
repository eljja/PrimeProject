from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket238-multishell-valuation-buffer-effectiverank.v1"
GENERATED_AT = "2026-08-25T14:20:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "multishell_valuation_buffer_effective_rank_audit"


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
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def p_adic_valuation(value: int, prime: int) -> int:
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def riemann_multishell_audit() -> dict[str, Any]:
    rho = Fraction(1, 3)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for shell_count in range(2, 9):
        pair_minimum = 1 - rho
        global_constant_mode = 1 - (shell_count - 1) * rho
        global_orthogonal_mode = 1 + rho
        epsilon = Fraction(1, 4 * shell_count)
        row_sum = (shell_count - 1) * epsilon
        certified_lower_bound = 1 - row_sum
        actual_positive_family_minimum = 1 - epsilon
        verified = (
            pair_minimum > 0
            and global_constant_mode <= pair_minimum
            and row_sum < 1
            and actual_positive_family_minimum >= certified_lower_bound > 0
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{shell_count}:{rho}:{pair_minimum}:{global_constant_mode}:"
                f"{global_orthogonal_mode}:{epsilon}:{row_sum}:"
                f"{certified_lower_bound}:{actual_positive_family_minimum}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "shell_count_J": shell_count,
                "pairwise_cross_norm_rho": fraction_payload(rho),
                "every_two_shell_minimum_eigenvalue": fraction_payload(pair_minimum),
                "adverse_global_constant_mode_eigenvalue": fraction_payload(
                    global_constant_mode
                ),
                "adverse_global_orthogonal_mode_eigenvalue": fraction_payload(
                    global_orthogonal_mode
                ),
                "adverse_global_block_is_positive_semidefinite": (
                    global_constant_mode >= 0
                ),
                "adverse_global_block_is_joint_gram_realizable": (
                    global_constant_mode >= 0
                ),
                "joint_gram_strict_positivity_counterexample": (
                    shell_count == 4
                ),
                "summable_family_cross_norm": fraction_payload(epsilon),
                "summable_family_maximum_row_sum_eta": fraction_payload(row_sum),
                "row_sum_certified_lower_bound": fraction_payload(
                    certified_lower_bound
                ),
                "summable_family_actual_minimum_eigenvalue": fraction_payload(
                    actual_positive_family_minimum
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let H be a Hermitian J-by-J block matrix with identity diagonal and "
        "off-diagonal blocks K_ij=K_ji*. If eta=max_i sum_(j!=i)||K_ij||_op<1, "
        "then H is bounded below by (1-eta)I. Pairwise positive principal "
        "angle data are not sufficient for a strict global lower bound: at "
        "rho=1/3 and J=4, every two-shell principal block has minimum "
        "eigenvalue 2/3, while the full positive-semidefinite regular-simplex "
        "Gram matrix has eigenvalue zero. For the same abstract algebraic "
        "family, the constant eigenvalue is 1-(J-1)rho and becomes negative "
        "once (J-1)rho>1. Thus the TICKET-237 two-shell angle target must be "
        "strengthened to a summable multishell interaction estimate."
    )
    proof = (
        "For a block vector x, bound each cross term by "
        "2||K_ij||||x_i||||x_j|| and use 2ab<=a^2+b^2. The total cross loss is "
        "at most eta sum_i||x_i||^2, proving the lower bound. In the scalar "
        "counterfamily the constant vector has eigenvalue 1-(J-1)rho and its "
        "orthogonal complement has eigenvalue 1+rho. At rho=1/3 and J=4 "
        "this is the jointly realizable Gram matrix of a regular simplex; it "
        "is singular and already refutes strict global positivity. Rows J>=5 "
        "are abstract block-matrix accumulation examples, not joint Gram "
        "realizations. A comparison family with K_ij=1/(4J) has row sum "
        "(J-1)/(4J)<1 and verifies the sufficient certificate."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_multishell_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "normalized_cross_row_sum_criterion_proved": True,
            "pairwise_principal_angle_sufficiency_refuted": True,
            "arithmetic_weil_multishell_row_sum_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The counterfamily and row-sum theorem are abstract finite block "
            "linear algebra. The J=4 row is a jointly realizable singular "
            "regular-simplex Gram matrix; the negative J>=5 rows are only "
            "abstract block systems. The result does not identify actual "
            "Guinand-Weil shell innovations, prove arithmetic decay of their "
            "normalized cross blocks, or locate a zeta zero. Pairwise angle estimates remain "
            "useful inputs but cannot alone certify a cofinal global form."
        ),
        "failure_count": failures,
    }


def collatz_valuation_audit() -> dict[str, Any]:
    selected_witnesses = {
        1: 5,
        2: 59,
        3: 5,
        4: 59,
        5: 5,
        6: 59,
        7: 5,
        8: 41,
        9: 5,
        10: 31,
        11: 5,
        12: 59,
        13: 5,
        14: 43,
        15: 5,
        16: 41,
        17: 5,
        18: 59,
        19: 5,
        20: 31,
    }
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for one_count, prime in selected_witnesses.items():
        denominator = 32**one_count - 27**one_count
        numerator = 32**one_count + 27**one_count - 2 * 18**one_count
        denominator_valuation = p_adic_valuation(denominator, prime)
        numerator_valuation = p_adic_valuation(numerator, prime)
        verified = (
            numerator % denominator != 0
            and denominator_valuation > numerator_valuation
            and denominator_valuation > 0
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{one_count}:{prime}:{denominator_valuation}:"
                f"{numerator_valuation}:{numerator % denominator}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "one_count_k": one_count,
                "run_block_word": f"1^{one_count} 2^{2 * one_count}",
                "witness_prime_q": prime,
                "v_q_D_k": denominator_valuation,
                "v_q_B_k": numerator_valuation,
                "presence_witness_in_this_row": numerator_valuation == 0,
                "B_k_mod_D_k": str(numerator % denominator),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For positive integers D and B, D does not divide B if and only if "
        "there exists a prime q with v_q(D)>v_q(B). Consequently TICKET-197's "
        "all-k nondivisibility theorem for D_k=32^k-27^k and "
        "B_k=32^k+27^k-2*18^k already implies a word-dependent prime-power "
        "valuation witness for every binary run block. Conversely, demanding "
        "such a witness for every primitive binary density-band necklace is "
        "exactly equivalent to universal affine nondivisibility on that class; "
        "it is not a weaker bridge toward that periodic-cycle exclusion."
    )
    proof = (
        "Unique factorization gives D|B exactly when v_q(D)<=v_q(B) for every "
        "prime q. Negating this statement proves the equivalence. TICKET-197 "
        "proved D_k does not divide B_k for every k>=1 by reducing divisibility "
        "to the impossible inequality D_k<=3^k-2^k. Applying the valuation "
        "equivalence yields the run-block witness. The exact audit records one "
        "such prime for k=1,...,20 and checks both valuations directly."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_run_block_valuation_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "valuation_gap_divisibility_equivalence_proved": True,
            "all_run_blocks_have_adaptive_valuation_witness_proved": True,
            "general_necklace_valuation_gap_is_weaker_bridge_refuted": True,
            "valuation_witness_escapes_every_finite_palette_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The universal equivalence does not prove nondivisibility for "
            "general necklaces; it only shows that the proposed valuation-gap "
            "statement has the same missing quantifier. TICKET-197 supplies "
            "that input only for one run-block family. Valuations above two, "
            "other periodic words, and aperiodic divergence remain open."
        ),
        "failure_count": failures,
    }


def goldbach_buffer_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for cutoff in (100, 1_000, 10_000, 100_000):
        flags = prime_flags_up_to(cutoff)
        prime_count = sum(flags)
        for buffer_width in (0, 1, math.isqrt(cutoff)):
            target = 2 * cutoff - buffer_width
            representation_count = sum(
                1
                for left in range(2, cutoff + 1)
                if flags[left]
                and 2 <= target - left <= cutoff
                and flags[target - left]
            )
            interval_lower = max(2, target - cutoff)
            interval_upper = min(cutoff, target - 2)
            available_left_integers = max(0, interval_upper - interval_lower + 1)
            geometric_bound = buffer_width + 1
            normalized_margin = Fraction(representation_count, prime_count)
            normalized_ceiling = Fraction(geometric_bound, prime_count)
            verified = (
                available_left_integers <= geometric_bound
                and representation_count <= available_left_integers
                and normalized_margin <= normalized_ceiling
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{cutoff}:{buffer_width}:{target}:{prime_count}:"
                    f"{available_left_integers}:{representation_count}:"
                    f"{normalized_margin}:{normalized_ceiling}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "cutoff_X": cutoff,
                    "upper_endpoint_buffer_h": buffer_width,
                    "target_N": target,
                    "prime_count_pi_X": prime_count,
                    "available_left_integer_count": available_left_integers,
                    "ordered_prime_representation_count_g_X_N": representation_count,
                    "geometric_representation_ceiling_h_plus_1": geometric_bound,
                    "normalized_actual_margin": fraction_payload(normalized_margin),
                    "normalized_geometric_ceiling": fraction_payload(
                        normalized_ceiling
                    ),
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let g_X be the ordered convolution of the prime indicator truncated "
        "at X. For every integer h with 0<=h<=X-2, "
        "g_X(2X-h)<=h+1. Therefore a normalized margin "
        "g_X(2X-h)/pi(X)>=c/log X forces "
        "h+1>=c*pi(X)/log X=(c+o(1))X/(log X)^2. In particular every buffer "
        "h=o(X/(log X)^2) is too thin for a uniform positive inverse-log "
        "margin, independently of any major/minor-arc estimate."
    )
    proof = (
        "If p,q<=X and p+q=2X-h, then X-h<=p<=X. There are at most h+1 "
        "possible integers p, hence at most h+1 ordered prime pairs. Divide "
        "by pi(X) for the exact normalized ceiling. The stated necessary "
        "buffer scale follows from the prime number theorem pi(X)~X/log X. "
        "The finite audit checks the exact count and ceiling for three buffer "
        "widths at each of four cutoffs."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_buffer_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "geometric_buffer_ceiling_proved": True,
            "sub_x_over_log_squared_inverse_log_margin_refuted": True,
            "mesoscopic_buffer_scale_necessity_proved": True,
            "mesoscopic_buffered_prime_phase_gain_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is a necessary support-geometry condition near the truncated "
            "upper endpoint. It does not show that a buffer of order "
            "X/(log X)^2 is sufficient, estimate the actual reflected minor "
            "term there, or produce a Goldbach counterexample. Fixed positive-"
            "fraction bulk windows are not refuted."
        ),
        "failure_count": failures,
    }


def twin_effective_rank_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    latent_rank = 2
    for coordinate_count in (4, 8, 16, 32, 64):
        repetitions = coordinate_count // latent_rank
        support_size = coordinate_count + 1
        energy = Fraction(repetitions - 1, coordinate_count - 1)
        effective_rank = Fraction(latent_rank)
        recovered_energy = (
            Fraction(coordinate_count, 1) / effective_rank - 1
        ) / (coordinate_count - 1)
        verified = energy == recovered_energy and support_size > coordinate_count
        failures += int(not verified)
        transcript.update(
            (
                f"{support_size}:{coordinate_count}:{latent_rank}:"
                f"{repetitions}:{energy}:{effective_rank}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "support_size_s": support_size,
                "coordinate_count_m": coordinate_count,
                "latent_centered_rank_r": latent_rank,
                "repetitions_per_latent_mode": repetitions,
                "gram_effective_rank": fraction_payload(effective_rank),
                "degree_two_energy_E_m_2": fraction_payload(energy),
                "support_grows_with_m": True,
                "degree_two_energy_stays_at_least_one_third": energy >= Fraction(1, 3),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let C be the Gram matrix of m centered, variance-one coordinates and "
        "let E_(m,2) be the average squared off-diagonal correlation. With "
        "effective rank r_eff(C)=(tr C)^2/||C||_F^2, one has the exact identity "
        "r_eff=m/(1+(m-1)E_(m,2)), or equivalently "
        "E_(m,2)=(m/r_eff-1)/(m-1). Hence along m tending to infinity, "
        "E_(m,2) tends to zero if and only if r_eff tends to infinity. Growing "
        "sample support alone is insufficient: repeating two orthonormal "
        "centered modes while support and m grow keeps r_eff=2 and makes "
        "E_(m,2) tend to 1/2."
    )
    proof = (
        "Because C_ii=1, ||C||_F^2=m+2 sum_(i<j)|C_ij|^2="
        "m+m(m-1)E_(m,2), while tr C=m. Substitution gives both identities. "
        "They show E_(m,2)->0 iff 1/r_eff=1/m+(1-1/m)E_(m,2)->0. For the "
        "counterfamily, repeat each of two orthonormal modes m/2 times. Its "
        "only nonzero Gram eigenvalues are m/2,m/2, so r_eff=2 and exactly "
        "E_(m,2)=(m/2-1)/(m-1), regardless of the larger ambient support."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_fixed_effective_rank_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "degree_two_effective_rank_identity_proved": True,
            "degree_two_decay_iff_effective_rank_divergence_proved": True,
            "support_growth_sufficiency_refuted": True,
            "prime_weighted_effective_rank_divergence_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The identity is exact for normalized Gram matrices, and the "
            "counterfamily is synthetic. It does not prove effective-rank "
            "growth for actual prime-weighted CRT coordinates, uniform "
            "diagonal nondegeneracy, a positive twin main term, or any parity-"
            "breaking transfer."
        ),
        "failure_count": failures,
    }


def proof_dag(problem: str) -> dict[str, Any]:
    if problem == "riemann":
        nodes = [
            ("RH-T237", "PrincipalAngleCriterionAndNestedCofinalFrameNoGo", "closed_input"),
            ("RH-T238", "MultishellNormalizedCrossRowSumCriterionAndPairwiseAngleNoGo", "closed"),
            ("RH-N238", "PairwiseAngleGapAloneImpliesGlobalCofinalPositivity", "refuted_or_limited"),
            ("RH-OPEN238", "ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells", "highest_risk_open"),
            ("RH", "RiemannHypothesis", "open_not_proven"),
        ]
        edges = [["RH-T237", "RH-T238"], ["RH-T238", "RH-N238"], ["RH-T238", "RH-OPEN238"], ["RH-OPEN238", "RH"]]
    elif problem == "collatz":
        nodes = [
            ("CO-T197", "ContiguousOneTwoRunNondivisibility", "closed_input"),
            ("CO-T237", "NoFinitePrimePaletteUniversallySeparatesRunBlocks", "closed_input"),
            ("CO-T238", "AdaptiveValuationCriterionEquivalenceAndRunBlockClosure", "closed"),
            ("CO-N238", "GeneralNecklaceValuationGapIsAWeakerIntermediateLemma", "refuted_or_limited"),
            ("CO-OPEN238", "RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette", "highest_risk_open"),
            ("CO-PERIODIC", "AllPeriodicValuationWords", "open_not_proven"),
            ("CO", "CollatzConjecture", "open_not_proven"),
        ]
        edges = [["CO-T197", "CO-T238"], ["CO-T237", "CO-T238"], ["CO-T238", "CO-N238"], ["CO-T238", "CO-OPEN238"], ["CO-OPEN238", "CO-PERIODIC"], ["CO-PERIODIC", "CO"]]
    elif problem == "goldbach":
        nodes = [
            ("GB-T237", "TruncatedDyadicUpperEndpointObstruction", "closed_input"),
            ("GB-T238", "MesoscopicBufferWidthNecessaryForInverseLogReflectedMargin", "closed"),
            ("GB-N238", "AnyDivergingUpperEndpointBufferSupportsInverseLogMargin", "refuted_or_limited"),
            ("GB-OPEN238", "MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack", "highest_risk_open"),
            ("GB", "StrongGoldbachConjecture", "open_not_proven"),
        ]
        edges = [["GB-T237", "GB-T238"], ["GB-T238", "GB-N238"], ["GB-T238", "GB-OPEN238"], ["GB-OPEN238", "GB"]]
    else:
        nodes = [
            ("TP-T237", "FiniteSupportWelchFloorForDegreeTwoCRTOverlap", "closed_input"),
            ("TP-T238", "DegreeTwoEnergyEffectiveRankEquivalenceAndSupportGrowthNoGo", "closed"),
            ("TP-N238", "GrowingSupportAloneImpliesDegreeTwoDecay", "refuted_or_limited"),
            ("TP-OPEN238", "PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl", "highest_risk_open"),
            ("TP-PARITY", "ParityRetainingTransferAndPositivePrincipalMass", "open_not_proven"),
            ("TP", "TwinPrimeConjecture", "open_not_proven"),
        ]
        edges = [["TP-T237", "TP-T238"], ["TP-T238", "TP-N238"], ["TP-T238", "TP-OPEN238"], ["TP-OPEN238", "TP-PARITY"], ["TP-PARITY", "TP"]]
    return {
        "nodes": [
            {"id": node_id, "label": label, "status": status}
            for node_id, label, status in nodes
        ],
        "edges": edges,
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


def build_audit() -> dict[str, Any]:
    computations = {
        "riemann": riemann_multishell_audit(),
        "collatz": collatz_valuation_audit(),
        "goldbach": goldbach_buffer_audit(),
        "twin_prime": twin_effective_rank_audit(),
    }
    tracks = [
        make_section(
            "riemann",
            "RH-TICKET-238",
            "MultishellNormalizedCrossRowSumCriterionAndPairwiseAngleNoGo",
            computations["riemann"],
            "pairwise positive principal angles as a sufficient cofinal global positivity certificate",
            "sum normalized innovation interactions across all logarithmic shells and control the maximum block row sum",
            "ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells",
            proof_dag("riemann"),
        ),
        make_section(
            "collatz",
            "CO-TICKET-238",
            "AdaptiveValuationCriterionEquivalenceAndRunBlockClosure",
            computations["collatz"],
            "the all-necklace valuation-gap target as a weaker intermediate statement than affine nondivisibility",
            "first prove that run-block witnesses escape every fixed finite valuation palette, then transfer the mechanism by controlled run complexity",
            "RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette",
            proof_dag("collatz"),
        ),
        make_section(
            "goldbach",
            "GB-TICKET-238",
            "MesoscopicBufferWidthNecessaryForInverseLogReflectedMargin",
            computations["goldbach"],
            "any diverging upper-endpoint buffer as sufficient geometry for an inverse-log phase margin",
            "work at buffer width at least the mesoscopic X/(log X)^2 scale and separate reflected gain from minor loss pointwise",
            "MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack",
            proof_dag("goldbach"),
        ),
        make_section(
            "twin-prime",
            "TP-TICKET-238",
            "DegreeTwoEnergyEffectiveRankEquivalenceAndSupportGrowthNoGo",
            computations["twin_prime"],
            "growing prime-weight support as sufficient for degree-two CRT correlation decay",
            "prove divergence of the normalized prime-weighted CRT Gram effective rank together with uniform diagonal control",
            "PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl",
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
        "total_failure_count": sum(
            computation["failure_count"] for computation in computations.values()
        ),
    }
    audit_root = {
        "theorem_name": "FourConjectureMultishellValuationBufferEffectiveRankAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-238 proves four exact partial or no-go results: a multishell "
            "row-sum positivity criterion and pairwise-angle obstruction; an "
            "adaptive valuation equivalence with run-block closure; a sharp "
            "mesoscopic Goldbach buffer necessity; and an exact degree-two "
            "effective-rank equivalence with a support-growth counterfamily. It "
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
            "TICKET-238 proves four exact partial or no-go results and resolves "
            "none of the four parent conjectures."
        ),
        AUDIT_KEY: audit_root,
        "attempts": attempts,
    }


def track_payload(audit: dict[str, Any], problem_id: str) -> dict[str, Any]:
    attempt = next(
        item for item in audit["attempts"] if item["problem_id"] == problem_id
    )
    section = audit[AUDIT_KEY][problem_id.replace("-", "_")]
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
        ROOT
        / "data/open-problem/ticket238-multishell-valuation-buffer-effectiverank.json",
        audit,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-238-multishell-row-sum.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-238-valuation-equivalence.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-238-mesoscopic-buffer.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-238-effective-rank.json",
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
