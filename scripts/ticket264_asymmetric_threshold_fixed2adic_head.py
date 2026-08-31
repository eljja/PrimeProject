from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(0)

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket254_diagonal_weighted_reflection_thue import fraction_record, write_json
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import certified_root_continued_fraction


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket264-asymmetric-threshold-fixed2adic-head.v1"
GENERATED_AT = "2026-09-01T23:59:30+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "asymmetric_threshold_fixed2adic_head_audit"

RIEMANN_REPLAY_COUNT = 64
RIEMANN_ONE_SIDED_PAIRS = (
    (Fraction(1, 4), Fraction(1, 2)),
    (Fraction(1, 3), Fraction(2, 3)),
    (Fraction(3, 4), Fraction(1, 2)),
)
COLLATZ_GRID_SIZES = (4, 8, 16, 32, 64, 128)
GOLDBACH_MODULUS_EXPONENTS = tuple(range(1, 17))
GOLDBACH_LEVELS = tuple(range(16))
TWIN_HEAD_CERTIFICATE_COUNT = 39
TWIN_COEFFICIENTS = tuple(comb(17, k) * 2 ** (k // 2) for k in range(18))
TWIN_ABSOLUTE_COEFFICIENT_SUM = sum(TWIN_COEFFICIENTS)
TWIN_JET_ORDER = 9
TWIN_EXACTNESS_THRESHOLD = (
    TWIN_ABSOLUTE_COEFFICIENT_SUM + 1
) * 16**TWIN_JET_ORDER


@lru_cache(maxsize=1)
def riemann_asymmetric_envelope_audit() -> dict[str, Any]:
    families: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for positive, negative in RIEMANN_ONE_SIDED_PAIRS:
        rows: list[dict[str, Any]] = []
        for index in range(1, RIEMANN_REPLAY_COUNT + 1):
            error = positive / index if index % 2 == 0 else -negative / index
            next_error = (
                positive / (index + 1)
                if (index + 1) % 2 == 0
                else -negative / (index + 1)
            )
            energy = Fraction(1) + error
            next_energy = Fraction(1) + next_error
            jump = index * (energy - next_energy)
            lag = (index + 1) * next_energy - index * energy
            expected_jump = (
                positive + Fraction(index, index + 1) * negative
                if index % 2 == 0
                else -negative - Fraction(index, index + 1) * positive
            )
            expected_lag = (
                Fraction(1) - positive - negative
                if index % 2 == 0
                else Fraction(1) + positive + negative
            )
            scaled_positive = index * max(error, Fraction(0))
            scaled_negative = index * max(-error, Fraction(0))
            verified = (
                jump == expected_jump
                and lag == expected_lag
                and lag == next_energy - jump
                and scaled_positive == (positive if index % 2 == 0 else 0)
                and scaled_negative == (negative if index % 2 else 0)
            )
            failures += int(not verified)
            rows.append(
                {
                    "index_n": index,
                    "energy_E_n": fraction_record(energy),
                    "next_energy_E_n_plus_1": fraction_record(next_energy),
                    "scaled_positive_error": fraction_record(scaled_positive),
                    "scaled_negative_error": fraction_record(scaled_negative),
                    "scaled_signed_jump_J_n": fraction_record(jump),
                    "lag_S_n": fraction_record(lag),
                    "row_verified": verified,
                }
            )
            transcript.update(
                f"{positive}:{negative}:{index}:{energy}:{next_energy}:"
                f"{jump}:{lag}:{int(verified)}\n".encode("ascii")
            )
        total = positive + negative
        families.append(
            {
                "limit_L": fraction_record(Fraction(1)),
                "positive_reciprocal_envelope_A_plus": fraction_record(positive),
                "negative_reciprocal_envelope_A_minus": fraction_record(negative),
                "envelope_sum": fraction_record(total),
                "regime": "strict" if total < 1 else "critical" if total == 1 else "supercritical",
                "predicted_liminf_lag": fraction_record(1 - total),
                "exact_rows": rows,
            }
        )
    theorem = (
        "Let E_n tend to L>0, a_n=E_n-L, A_+=limsup n max(a_n,0), "
        "A_-=limsup n max(-a_n,0), J_n=n(E_n-E_(n+1)), and "
        "S_n=(n+1)E_(n+1)-nE_n. If A_+ and A_- are finite, then "
        "limsup J_n<=A_++A_- and liminf S_n>=L-A_+-A_-. Thus "
        "A_++A_-<L gives an eventual positive lag margin. The coefficient "
        "one on each one-sided envelope is jointly optimal, including the "
        "critical boundary A_++A_-=L."
    )
    proof = (
        "Since a_n-a_(n+1)<=max(a_n,0)+max(-a_(n+1),0), "
        "J_n is at most n a_n^+ + [n/(n+1)](n+1)a_(n+1)^-. "
        "Taking limsups gives A_++A_-. The exact identity "
        "S_n=E_(n+1)-J_n and E_(n+1)->L gives the lag bound. For arbitrary "
        "P,M>=0, set a_n=P/n at even n and a_n=-M/n at odd n. Then the "
        "one-sided envelopes are P,M, the even subsequence has J_n->P+M "
        "and S_n=L-P-M, and the odd subsequence has S_n=L+P+M. Hence no "
        "smaller universal coefficient on either side is valid. These are "
        "abstract sequences, not Guinand-Weil packet energies."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_asymmetric_reciprocal_families": families,
        "algorithm": "closed-form Fraction evaluation of three asymmetric alternating reciprocal families",
        "complexity": "O(FN) exact rational operations; the inequality and sharpness proof are symbolic",
        "random_seed": None,
        "input_range": {
            "limit_L": "1",
            "one_sided_envelope_pairs": [[str(p), str(m)] for p, m in RIEMANN_ONE_SIDED_PAIRS],
            "index_min": 1,
            "index_max": RIEMANN_REPLAY_COUNT,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "asymmetric_envelope_bound_proved": True,
            "joint_coefficient_one_sharp_proved": True,
            "strict_condition_weaker_than_symmetric_half_limit": True,
            "replayed_row_count": len(RIEMANN_ONE_SIDED_PAIRS) * RIEMANN_REPLAY_COUNT,
            "actual_weil_one_sided_envelope_sum_below_limit_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_threshold_cutoff_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    harmonic_cases = 0
    for modulus in COLLATZ_GRID_SIZES:
        tests: list[dict[str, Any]] = []
        for harmonic in range(1, modulus + 1):
            magnitude_squared = Fraction(1 if harmonic % modulus == 0 else 0)
            threshold_pass = magnitude_squared <= Fraction(1, harmonic * harmonic)
            expected = harmonic < modulus
            verified = threshold_pass == expected
            failures += int(not verified)
            harmonic_cases += 1
            tests.append(
                {
                    "harmonic_h": harmonic,
                    "normalized_weyl_magnitude_squared": fraction_record(magnitude_squared),
                    "threshold_one_over_h_squared_pass": threshold_pass,
                    "row_verified": verified,
                }
            )
            transcript.update(
                f"{modulus}:{harmonic}:{magnitude_squared}:{int(threshold_pass)}:{int(verified)}\n".encode("ascii")
            )
        cutoff = modulus - 1
        rows.append(
            {
                "complete_grid_size_N": modulus,
                "canonical_threshold_cutoff_K_N": cutoff,
                "next_harmonic_fails": True,
                "harmonic_tests": tests,
                "case_verified": all(item["row_verified"] for item in tests),
            }
        )
    theorem = (
        "For any sequence x_j in R/Z put W_N(h)=N^(-1)sum_(j<=N) "
        "exp(2*pi*i*h*x_j), E_N(H)=max_(1<=|h|<=H)|W_N(h)|, and "
        "K_N=max({0} union {1<=H<=N:E_N(H)<=1/H}). Then W_N(h)->0 for "
        "every fixed nonzero integer h if and only if K_N->infinity. When "
        "K_N>=1 one has E_N(K_N)<=1/K_N by construction."
    )
    proof = (
        "The admissible H form an initial segment because E_N(H) is "
        "nondecreasing while 1/H is decreasing. If every fixed harmonic "
        "vanishes, then for each fixed H the maximum of its finitely many "
        "harmonics tends to zero, so eventually E_N(H)<=1/H and K_N>=H. "
        "Conversely, if K_N tends to infinity, every fixed h is eventually "
        "inside the cutoff and |W_N(h)|<=E_N(K_N)<=1/K_N->0. The complete "
        "M-point grids have exact zero sums for 1<=|h|<M and magnitude one "
        "at h=M, hence K_M=M-1. No canonical Fermat-quotient cancellation "
        "estimate follows from this logical equivalence."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_complete_grid_threshold_replays": rows,
        "algorithm": "exact complete-root sum dichotomy and rational threshold comparisons",
        "complexity": "O(sum M) exact integer/rational checks; the equivalence is symbolic",
        "random_seed": None,
        "input_range": {"complete_grid_sizes": list(COLLATZ_GRID_SIZES)},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "pointwise_weyl_iff_explicit_threshold_cutoff_diverges_proved": True,
            "complete_grid_replay_count": len(rows),
            "harmonic_threshold_case_count": harmonic_cases,
            "canonical_fermat_quotient_threshold_cutoff_diverges_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def _tie_count(level: int) -> int:
    return 3 ** (6 * level + 3) + 1


def _predicted_period(modulus_exponent: int) -> int:
    return 1 if modulus_exponent <= 3 else 2 ** (modulus_exponent - 3)


@lru_cache(maxsize=1)
def goldbach_fixed_two_adic_no_go_audit() -> dict[str, Any]:
    phase_rows: list[dict[str, Any]] = []
    countermodels: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for exponent in GOLDBACH_MODULUS_EXPONENTS:
        modulus = 2**exponent
        period = _predicted_period(exponent)
        residues = [_tie_count(level) % modulus for level in range(period)]
        repeats = all(
            _tie_count(level + period) % modulus == residues[level]
            for level in range(period)
        )
        least = period == 1 or any(
            residues[index] != residues[index % (period // 2)]
            for index in range(period)
        )
        verified = repeats and least
        failures += int(not verified)
        phase_rows.append(
            {
                "modulus_exponent_m": exponent,
                "modulus_two_to_m": modulus,
                "least_level_period": period,
                "one_period_tie_residues": residues,
                "period_verified": verified,
            }
        )
        transcript.update(
            f"period:{exponent}:{modulus}:{period}:{','.join(map(str, residues))}:{int(verified)}\n".encode("ascii")
        )
        for level in GOLDBACH_LEVELS:
            middle = _tie_count(level)
            if middle <= modulus:
                continue
            n1 = middle - modulus
            n2 = middle + modulus
            model_verified = (
                n1 >= 0
                and n1 + n2 == 2 * middle
                and n1 != n2
                and n2 % modulus == middle % modulus
            )
            failures += int(not model_verified)
            countermodels.append(
                {
                    "modulus_exponent_m": exponent,
                    "level_l": level,
                    "tie_count_M_l": str(middle),
                    "abstract_N_1": str(n1),
                    "abstract_N_2": str(n2),
                    "common_residue_mod_two_to_m": middle % modulus,
                    "same_total_as_tie": n1 + n2 == 2 * middle,
                    "non_tie": n1 != n2,
                    "row_verified": model_verified,
                }
            )
            transcript.update(
                f"model:{exponent}:{level}:{middle}:{n1}:{n2}:{middle % modulus}:{int(model_verified)}\n".encode("ascii")
            )
    theorem = (
        "Let M_l=3^(6l+3)+1 be the forced value of each nonzero modulo-three "
        "prime-residue count at a q=3 special-prefix tie. For every m>=1, "
        "the sequence M_l modulo 2^m has least period 1 for m<=3 and "
        "2^(m-3) for m>=4. Nevertheless, for every fixed m and every l "
        "with M_l>2^m, the integer pair (M_l-2^m,M_l+2^m) has the same "
        "total and the same second-coordinate residue modulo 2^m as the tie "
        "but is not tied. Therefore no fixed two-adic tie signature together "
        "with the total count is sufficient to decide the tie."
    )
    proof = (
        "For m>=3, the multiplicative order of 3 modulo 2^m is 2^(m-2); "
        "this follows inductively from v_2(3^(2^r)-1)=r+2. Since increasing "
        "l adds six to the exponent and v_2(6)=1, the least level period is "
        "2^(m-3); m=1,2,3 are checked directly. The displayed shifted pair "
        "is nonnegative under M_l>2^m, sums to 2M_l, differs by 2^(m+1), "
        "and its second entry is congruent to M_l modulo 2^m. These are "
        "abstract count models, not claims that such pairs occur as actual "
        "prime residue counts. They refute sufficiency of the fixed-modulus "
        "information, not the strong Goldbach conjecture."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_two_adic_phase_period_rows": phase_rows,
        "exact_fixed_modulus_nontie_countermodels": countermodels,
        "algorithm": "exact modular exponentiation and integer shifted-count construction",
        "complexity": "O(sum 2^(m-3) + ML) modular/integer operations on the declared finite replay",
        "random_seed": None,
        "input_range": {
            "modulus_exponent_min": min(GOLDBACH_MODULUS_EXPONENTS),
            "modulus_exponent_max": max(GOLDBACH_MODULUS_EXPONENTS),
            "countermodel_level_min": min(GOLDBACH_LEVELS),
            "countermodel_level_max": max(GOLDBACH_LEVELS),
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_fixed_two_adic_phase_periods_proved": True,
            "fixed_two_adic_signature_sufficiency_refuted": True,
            "phase_period_replay_count": len(phase_rows),
            "countermodel_count": len(countermodels),
            "actual_q3_special_prime_race_nonvanishing_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_subthreshold_head_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(
        TWIN_HEAD_CERTIFICATE_COUNT
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_denominator = 0
    subthreshold_count = 0
    first_above_index: int | None = None
    for source in source_rows:
        index = source["term_index"]
        numerator = int(source["convergent_numerator"])
        denominator = int(source["convergent_denominator"])
        coefficient = b1_coefficient_form(numerator, denominator)
        nondecreasing = denominator >= previous_denominator
        strict_after_first = index <= 1 or denominator > previous_denominator
        previous_denominator = denominator
        at_or_below = denominator <= TWIN_EXACTNESS_THRESHOLD
        if at_or_below:
            subthreshold_count += 1
        elif first_above_index is None:
            first_above_index = index
        direct_unit_free = abs(coefficient) != 1
        verified = nondecreasing and strict_after_first and (direct_unit_free if at_or_below else True)
        failures += int(not verified)
        digest = hashlib.sha256(str(coefficient).encode("ascii")).hexdigest()
        rows.append(
            {
                "term_index": index,
                "partial_quotient": source["partial_quotient"],
                "convergent_numerator": str(numerator),
                "convergent_denominator": str(denominator),
                "at_or_below_exactness_threshold": at_or_below,
                "B_1_value": str(coefficient),
                "B_1_value_sha256": digest,
                "direct_unit_free": direct_unit_free,
                "denominator_nondecreasing": nondecreasing,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient}:{int(at_or_below)}:{int(direct_unit_free)}:{int(verified)}\n".encode("ascii")
        )
    crossing_verified = (
        subthreshold_count == 38
        and first_above_index == 38
        and int(rows[37]["convergent_denominator"]) == 110221790993960069
        and int(rows[38]["convergent_denominator"]) == 309742427372962732
        and all(row["direct_unit_free"] for row in rows[:38])
    )
    failures += int(not crossing_verified)
    theorem = (
        "Let p_n/q_n be the certified continued-fraction convergents to the "
        "unique real root used by the degree-17 Twin branch, and put "
        "V_0=188580743973175296. Every convergent with q_n<=V_0 is among "
        "n=0,...,37, and none satisfies B_1(p_n,q_n)=+1 or -1. The next "
        "denominator is q_38=309742427372962732>V_0. Thus the entire finite "
        "subthreshold head is closed; only the infinite n>=38 tail remains."
    )
    proof = (
        "The certified rational root bracket fixes the first 39 continued-"
        "fraction terms. Exact recurrence gives nondecreasing denominators "
        "and strict increase after the initial modulus-one duplication. "
        "Direct integer evaluation of B_1 on indices 0 through 37 gives no "
        "unit value. Since q_37=110221790993960069<=V_0<q_38 and all later "
        "continued-fraction denominators strictly increase, there can be no "
        "additional subthreshold convergent. TICKET-263's ninth-order "
        "equivalence applies in the later root-cone tail, but this theorem "
        "does not exclude infinitely many later congruence passes."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "coefficient_vector_a_0_through_a_17": list(TWIN_COEFFICIENTS),
        "ninth_order_exactness_threshold_V_0": str(TWIN_EXACTNESS_THRESHOLD),
        "exact_head_and_crossing_rows": rows,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fraction plus exact degree-17 integer evaluation through the first threshold crossing",
        "complexity": "O(K*17) exact big-integer terms for K=39",
        "random_seed": None,
        "input_range": {"certified_convergent_count": TWIN_HEAD_CERTIFICATE_COUNT},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_subthreshold_unique_root_convergents_unit_free_proved": True,
            "subthreshold_convergent_count": subthreshold_count,
            "first_above_threshold_term_index": first_above_index,
            "last_subthreshold_denominator": rows[37]["convergent_denominator"],
            "first_above_threshold_denominator": rows[38]["convergent_denominator"],
            "crossing_verified": crossing_verified,
            "all_unique_root_convergents_excluded": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    rejected_name: str,
    open_name: str,
    *,
    external_name: str | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T263", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T264", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-CERT264", "label": f"{theorem_name}ExactReplay", "status": "computed_finite"},
        {"id": f"{code}-REJECT264", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN264", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T263", f"{code}-T264"],
        [f"{code}-T264", f"{code}-CERT264"],
        [f"{code}-T264", f"{code}-REJECT264"],
        [f"{code}-T264", f"{code}-OPEN264"],
    ]
    if external_name:
        nodes.append({"id": f"{code}-EXT264", "label": external_name, "status": "external_theorem"})
        edges.append([f"{code}-EXT264", f"{code}-T264"])
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": [f"{code}-T263", f"{code}-T264", f"{code}-OPEN264"],
        "acyclic": True,
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    classification: str,
    computation: dict[str, Any],
    discarded: str,
    parked: list[str],
    retained: str,
    next_lemma: str,
    prior_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    external_name: str | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-264",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": classification,
        "problem_status": STATUS,
        "reproducible_computation": computation,
        "finite_computation_boundary": finite_boundary,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "parked": parked,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "stagnation_count": 0,
        "proof_dag": proof_dag(
            code, prior_name, theorem_name, rejected_name, next_lemma,
            external_name=external_name,
        ),
        "claim_boundary": claim_boundary,
    }


@lru_cache(maxsize=1)
def build_audit() -> dict[str, Any]:
    riemann = riemann_asymmetric_envelope_audit()
    collatz = collatz_threshold_cutoff_audit()
    goldbach = goldbach_fixed_two_adic_no_go_audit()
    twin = twin_subthreshold_head_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "AsymmetricReciprocalEnvelopeForScaledJumpMargin", "partial_theorem", riemann,
            "treating the symmetric max-envelope threshold A<L/2 as the sharpest rate-only formulation",
            ["an arithmetic proof that actual Guinand-Weil packet energies satisfy A_++A_-<L"],
            "the strictly weaker sharp one-sided envelope-sum criterion and its asymmetric critical family",
            "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit",
            "SharpReciprocalEnvelopeForScaledJumpMargin",
            "NoAsymmetricImprovementOverTheSymmetricFactorTwoBound",
            "The abstract criterion is now sharper, but neither one-sided reciprocal envelope is bounded for actual Guinand-Weil packets.",
            "No RH proof or disproof; the missing step is an arithmetic packet estimate, not another sequence inequality.",
            f"Three abstract Fraction families and {riemann['aggregate']['replayed_row_count']} rows are checked; none is an actual Weil packet.",
        ),
        "collatz": section(
            "collatz", "CO", "PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges", "partial_theorem", collatz,
            "claiming that the TICKET-263 diagonal cutoff can only be existential and cannot be selected from the finite prefix data",
            ["a proof that the explicit threshold cutoff diverges for canonical fixed-base Fermat-quotient phases"],
            "the exact maximal threshold functional K_N, equivalent to all fixed-h cancellation",
            "CanonicalFermatQuotientThresholdCutoffDiverges",
            "PointwiseWeylCancellationIffSomeGrowingCutoffUniformCancellation",
            "EveryDataDefinedGrowingCutoffFailsToEncodePointwiseWeylCancellation",
            "K_N is explicit and finite-data-defined, but its divergence is not proved for the canonical Fermat-quotient sequence.",
            "No Collatz proof or counterexample; this is a computable quantifier reformulation without a canonical arithmetic estimate.",
            f"Exact complete grids M={list(COLLATZ_GRID_SIZES)} give {collatz['aggregate']['harmonic_threshold_case_count']} threshold checks; they are not canonical prefixes.",
        ),
        "goldbach": section(
            "goldbach", "GB", "EveryFixedTwoAdicTieSignatureHasNonTieCountModels", "exact_no_go", goldbach,
            "climbing to any one fixed power-of-two congruence and treating the tie residue plus total as sufficient",
            ["noncongruential control of the q=3 special prime-race integer gap"],
            "the exact all-m phase periods and universal shifted-count countermodels",
            "Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo",
            "Q3TieForcesLevelPhasedModuloThirtyTwo",
            "SomeFixedTwoAdicTieSignatureAndTotalSufficeToDecideEverySpecialTie",
            "Every fixed two-adic congruence loses the integer displacement by a multiple of its modulus; an all-level nonzero prime-race estimate is still absent.",
            "No strong Goldbach proof or counterexample; the no-go concerns only a fixed-modulus information route and uses abstract count models.",
            f"Periods are replayed for m=1..16 and {goldbach['aggregate']['countermodel_count']} valid (m,l) countermodels with l=0..15; the theorem itself is symbolic for all m,l.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "AllSubthresholdUniqueRootConvergentsAreUnitFree", "partial_theorem", twin,
            "leaving the finitely many unique-root convergents below the TICKET-263 exactness threshold as an unresolved global subcase",
            ["global exclusion of joint ninth-order congruences on every later unique-root convergent"],
            "the certified first threshold crossing and exact unit-free evaluation of the complete finite head",
            "NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences",
            "NinthOrderJointCongruenceExactOnRootCone",
            "SomeAdditionalSubthresholdUniqueRootConvergentMayRemainBeyondTheCertifiedHead",
            "The finite q<=V_0 head is closed, but infinitely many q>V_0 convergents remain and no recurrence excludes all ninth-order passes.",
            "No twin-prime proof or counterexample; only one degree-17 branch's finite continued-fraction head is completely closed.",
            "The first 39 certified convergents locate q_37<=V_0<q_38 and evaluate all 38 subthreshold B_1 values exactly.",
        ),
    }
    total_failures = sum(item["reproducible_computation"]["failure_count"] for item in sections.values())
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureAsymmetricThresholdFixedTwoAdicHeadAudit",
            "summary": (
                "TICKET-264 proves three partial theorems and one exact route no-go: a sharp asymmetric RH-packet envelope, "
                "an explicit Collatz Weyl threshold-cutoff equivalence, failure of every fixed two-adic Goldbach tie signature, "
                "and complete closure of the Twin degree-17 subthreshold convergent head. All parent conjectures remain open."
            ),
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 3,
                "exact_no_go_count": 1,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "riemann",
                "stagnated_problem_count": 0,
                "riemann_replay_case_count": riemann["aggregate"]["replayed_row_count"],
                "collatz_grid_replay_count": collatz["aggregate"]["complete_grid_replay_count"],
                "collatz_harmonic_threshold_case_count": collatz["aggregate"]["harmonic_threshold_case_count"],
                "goldbach_phase_period_replay_count": goldbach["aggregate"]["phase_period_replay_count"],
                "goldbach_fixed_modulus_countermodel_count": goldbach["aggregate"]["countermodel_count"],
                "twin_head_certificate_row_count": len(twin["exact_head_and_crossing_rows"]),
                "twin_subthreshold_convergent_count": twin["aggregate"]["subthreshold_convergent_count"],
                "twin_first_above_threshold_term_index": twin["aggregate"]["first_above_threshold_term_index"],
                "total_failure_count": total_failures,
            },
        },
        "attempts": [
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "result_classification": item["result_classification"],
                "status": STATUS,
                "bounded_result": {"audit_ref": f"#/{AUDIT_KEY}/{key}", "failure_count": item["reproducible_computation"]["failure_count"]},
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
            }
            for key, item in sections.items()
        ],
    }


def build_research_state(audit: dict[str, Any]) -> dict[str, Any]:
    previous = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    root = audit[AUDIT_KEY]
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        old = previous["problems"][key]
        established = list(old.get("established_results", []))
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        if item["route_decision"]["discard"] not in retired:
            retired.append(item["route_decision"]["discard"])
        parked = list(old.get("parked_routes", []))
        for route in item["route_decision"]["parked"]:
            if route not in parked:
                parked.append(route)
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": established,
            "retired_routes": retired,
            "parked_routes": parked,
            "remaining_gap": item["logical_limit"],
            "next_single_lemma": item["route_decision"]["next_single_lemma"],
            "stagnation_count": item["stagnation_count"],
            "unresolved_dependencies": [node["label"] for node in item["proof_dag"]["nodes"] if node["status"] in {"assumption", "heuristic", "open"}],
            "finite_computation_boundary": item["finite_computation_boundary"],
            "proof_dag_status": "acyclic_with_one_open_frontier",
            "validation_status": {
                "generator_failure_count": item["reproducible_computation"]["failure_count"],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 264,
        "parent_ticket": 263,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "riemann",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(ROOT / "data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json", audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-264-asymmetric-reciprocal-envelope.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-264-explicit-threshold-cutoff.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-264-fixed-two-adic-no-go.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-264-subthreshold-head.json",
    }
    for key, path in paths.items():
        write_json(path, {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]})
    write_json(ROOT / "data/open-problem/four-problem-research-state.json", build_research_state(audit))


if __name__ == "__main__":
    payload = build_audit()
    write_outputs(payload)
    machine = payload[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, ensure_ascii=False, indent=2))
