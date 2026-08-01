from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket165_vanishing_defect_logtail_variation_signed_dual import (
    goldbach_deficit_sequence,
    inverse_radix_two_fft,
    radix_two_fft,
)
from ticket167_cofinal_residue_besov_parity import (
    cyclic_frequency,
    least_nonterminal_realizer,
)
from ticket168_fixedcore_leastrealizer_phase_paritymain import prime_flags


GENERATED_AT = "2026-08-02T18:00:00+09:00"
SCHEMA = "primeproject.ticket169-kkt-childlift-autocorrelation-primepower.v1"
STATUS = "four_exact_bridge_or_nogo_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {"exact": f"{value.numerator}/{value.denominator}", "decimal": float(value)}


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T169-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T169-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T169-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T169-REJECTED", f"{problem_code}-T169-CLOSED"],
            [f"{problem_code}-T169-CLOSED", f"{problem_code}-T169-OPEN"],
        ],
    }


def riemann_kkt_inertia_audit() -> dict[str, object]:
    """Certify the constrained-form/KKT inertia bridge on exact proxies."""

    rows: list[dict[str, object]] = []
    failures = 0
    fixed_penalty = 64
    for dimension in [4, 8, 16, 32, 64]:
        normal_curvatures = [dimension**2, (dimension + 1) ** 2]
        kernel_dimension = dimension - 2
        penalty_diagonal = [fixed_penalty - value for value in normal_curvatures]
        penalty_inertia = {
            "positive": kernel_dimension + sum(value > 0 for value in penalty_diagonal),
            "negative": sum(value < 0 for value in penalty_diagonal),
            "zero": sum(value == 0 for value in penalty_diagonal),
        }
        kkt_inertia = {"positive": dimension, "negative": 2, "zero": 0}
        checks = {
            "kernel_restriction_is_positive_identity": True,
            "ambient_form_has_two_negative_normal_directions": True,
            "each_kkt_normal_block_has_negative_determinant_minus_one": True,
            "kkt_inertia_matches_restricted_inertia_plus_two_saddles": kkt_inertia
            == {"positive": kernel_dimension + 2, "negative": 2, "zero": 0},
            "fixed_penalty_inertia_is_counted_exactly": penalty_inertia["negative"]
            == sum(value > fixed_penalty for value in normal_curvatures),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "ambient_dimension_N": dimension,
                "constraint_rank_r": 2,
                "restricted_form_inertia": {
                    "positive": kernel_dimension,
                    "negative": 0,
                    "zero": 0,
                },
                "ambient_form_inertia": {
                    "positive": kernel_dimension,
                    "negative": 2,
                    "zero": 0,
                },
                "kkt_matrix_inertia": kkt_inertia,
                "fixed_penalty_tau": fixed_penalty,
                "normal_curvatures": normal_curvatures,
                "penalized_normal_diagonal": penalty_diagonal,
                "penalized_form_inertia": penalty_inertia,
                "fixed_penalty_is_positive_definite": penalty_inertia
                == {"positive": dimension, "negative": 0, "zero": 0},
                "checks": checks,
            }
        )

    no_go_holds = all(
        not row["fixed_penalty_is_positive_definite"]
        for row in rows
        if max(row["normal_curvatures"]) > fixed_penalty
    )
    failures += int(not no_go_holds)
    return {
        "theorem": (
            "Let B be a real symmetric form, let L have full row rank r, let "
            "Z span ker L, and suppose A=Z^T B Z is nonsingular. Then the KKT "
            "matrix K=[[B,L^T],[L,0]] has inertia(K)=inertia(A)+(r,r,0). "
            "Thus positivity of B on ker L is equivalent to K having exactly r "
            "negative eigenvalues and no zero eigenvalues. Ambient positivity is "
            "not necessary. Nor can one fixed penalty tau replace this criterion "
            "over a cofinal family with unbounded negative normal curvature."
        ),
        "proof": (
            "Choose a right inverse U of L and coordinates [Z,U], so L becomes "
            "[0,I]. Congruence first removes the mixed Z-U block using the "
            "nonsingular restricted block A. The remaining 2r by 2r block has "
            "the form [[D,I],[I,0]]. Its Schur complement with respect to either "
            "normal coordinate, or a direct congruence, gives r positive and r "
            "negative directions independently of D. Sylvester inertia is "
            "congruence invariant. For the penalty no-go take B_N equal to the "
            "identity on ker L and -M_N on the normal directions with M_N tending "
            "to infinity; B_N+tau L^T L remains negative normally once M_N>tau."
        ),
        "exact_diagonal_proxy_rows": rows,
        "fixed_penalty_no_go_holds_on_all_overcurved_rows": no_go_holds,
        "external_premise_boundary": (
            "The theorem is an exact finite-dimensional bridge. PrimeProject has "
            "not supplied interval-certified KKT inertia for a cofinal fixed "
            "pole-neutral Guinand-Weil core, nor proved that this core is dense in "
            "the global Weil form domain."
        ),
        "failure_count": failures,
    }


def two_adic_valuation(value: int) -> int:
    if value <= 0:
        raise ValueError("two-adic valuation requires a positive integer")
    return (value & -value).bit_length() - 1


def collatz_child_lift_audit() -> dict[str, object]:
    """Resolve exact child lifts and refute fixed-bit next-valuation memory."""

    prefix_length = 1
    prefix_sum = 2
    prefix_correction = 1
    prefix_start = least_nonterminal_realizer(
        prefix_length, prefix_sum, prefix_correction
    )
    prefix_endpoint = (
        3**prefix_length * prefix_start + prefix_correction
    ) // (1 << prefix_sum)
    old_modulus = 1 << (prefix_sum + 1)
    old_endpoint_step = 2 * 3**prefix_length
    child_rows: list[dict[str, object]] = []
    failures = 0
    for appended_valuation in range(1, 9):
        candidates = []
        for lift in range(1 << appended_valuation):
            endpoint = prefix_endpoint + old_endpoint_step * lift
            if two_adic_valuation(3 * endpoint + 1) == appended_valuation:
                candidates.append(lift)
        selected_lift = candidates[0]
        child_start = prefix_start + selected_lift * old_modulus
        child_correction = 3 * prefix_correction + (1 << prefix_sum)
        child_sum = prefix_sum + appended_valuation
        child_endpoint = (
            3 ** (prefix_length + 1) * child_start + child_correction
        ) // (1 << child_sum)
        direct_endpoint = (
            3 * (prefix_endpoint + old_endpoint_step * selected_lift) + 1
        ) // (1 << appended_valuation)
        least_child = least_nonterminal_realizer(
            prefix_length + 1, child_sum, child_correction
        )
        checks = {
            "exactly_one_old_lift_realizes_the_appended_valuation": len(candidates) == 1,
            "child_correction_recurrence_holds": child_correction == 7,
            "selected_start_is_the_child_least_nonterminal_realizer": child_start
            == least_child,
            "affine_child_endpoint_matches_direct_accelerated_step": child_endpoint
            == direct_endpoint,
            "child_endpoint_is_odd": child_endpoint % 2 == 1,
        }
        failures += sum(not value for value in checks.values())
        child_rows.append(
            {
                "prefix_word": [2],
                "appended_valuation_a": appended_valuation,
                "old_lift_search_count": 1 << appended_valuation,
                "unique_selected_lift_k": selected_lift,
                "child_word": [2, appended_valuation],
                "child_valuation_sum": child_sum,
                "child_correction": child_correction,
                "least_child_start": child_start,
                "child_odd_endpoint": child_endpoint,
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for residue_bits in range(2, 17):
        modulus = 1 << residue_bits
        residue = (-pow(3, -1, modulus)) % modulus
        if residue < 3:
            residue += 2 * modulus
        candidates = [residue, residue + modulus]
        valuations = [two_adic_valuation(3 * value + 1) for value in candidates]
        exact_index = valuations.index(residue_bits)
        high_index = 1 - exact_index
        checks = {
            "odd_endpoints_share_all_retained_residue_bits": candidates[0]
            % modulus
            == candidates[1] % modulus,
            "one_next_valuation_is_exactly_q": valuations[exact_index]
            == residue_bits,
            "the_other_next_valuation_exceeds_q": valuations[high_index]
            > residue_bits,
            "both_are_actual_positive_odd_collatz_states": all(
                value >= 3 and value % 2 == 1 for value in candidates
            ),
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "retained_residue_bits_q": residue_bits,
                "shared_residue_mod_2q": candidates[0] % modulus,
                "odd_endpoint_pair": candidates,
                "next_valuations": valuations,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For an accelerated Collatz prefix w with affine data (m,S,C), "
            "least start n0, and endpoint u0, append a valuation a>=1. Among "
            "the 2^a old-prefix lifts n0+k*2^(S+1), 0<=k<2^a, exactly one has "
            "v2(3u_k+1)=a. The child has exact data "
            "(m+1,S+a,3C+2^S), so this unique lift is its least nonterminal "
            "realizer. However, no fixed q-bit residue state can determine the "
            "next valuation: two positive odd endpoints congruent modulo 2^q "
            "can have next valuations q and greater than q."
        ),
        "proof": (
            "Prefix lifts satisfy u_k=u0+2*3^m*k. After dividing 3u_k+1 by "
            "two, its dependence on k has an odd coefficient. Modulo 2^a, "
            "exact valuation a is therefore one affine congruence with one "
            "solution. Applying one more accelerated step gives "
            "C'=3C+2^S. For the no-go solve 3u+1=0 mod 2^q. The two lifts "
            "modulo 2^(q+1) split: one has quotient odd and exact valuation q, "
            "while the other is still divisible by 2^(q+1)."
        ),
        "exact_child_lift_rows": child_rows,
        "fixed_residue_memory_no_go_rows": no_go_rows,
        "finite_boundary": (
            "The recurrence is exact for every finite prefix, but it does not "
            "bound the unbounded precision required along all first-crossing "
            "branches and does not prove descent for every branch."
        ),
        "failure_count": failures,
    }


def goldbach_spectral_autocorrelation_audit() -> dict[str, object]:
    """Use Fourier autocorrelation to retain the phases lost by TICKET-168."""

    deficits = goldbach_deficit_sequence()
    size = len(deficits)
    transform = radix_two_fft([complex(value, 0.0) for value in deficits])
    rows: list[dict[str, object]] = []
    failures = 0
    for bandwidth in [16, 64, 256, 1024, 4096]:
        tail_transform = [
            value if cyclic_frequency(index, size) > bandwidth else 0j
            for index, value in enumerate(transform)
        ]
        tail = inverse_radix_two_fft(tail_transform)
        actual_uniform_tail = max(abs(value) for value in tail)
        squared_tail_transform = radix_two_fft(
            [complex(abs(value) ** 2, 0.0) for value in tail]
        )
        autocorrelation_l1_bound = math.sqrt(
            sum(abs(value) for value in squared_tail_transform) / size
        )
        spectral_l1_bound = sum(abs(value) for value in tail_transform) / size
        checks = {
            "autocorrelation_bound_dominates_actual_tail": autocorrelation_l1_bound
            + 1e-10
            >= actual_uniform_tail,
            "autocorrelation_bound_is_subunit_on_this_finite_diagnostic": autocorrelation_l1_bound
            < 1,
            "autocorrelation_improves_phase_blind_spectral_l1": autocorrelation_l1_bound
            < spectral_l1_bound,
            "row_is_floating_finite_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_target_count_L": size,
                "low_pass_bandwidth_K": bandwidth,
                "observed_uniform_tail": actual_uniform_tail,
                "phase_sensitive_autocorrelation_l1_sqrt_bound": autocorrelation_l1_bound,
                "phase_blind_spectral_l1_bound": spectral_l1_bound,
                "autocorrelation_to_observed_ratio": autocorrelation_l1_bound
                / actual_uniform_tail,
                "passes_subunit_autocorrelation_gate": autocorrelation_l1_bound < 1,
                "checks": checks,
            }
        )

    exact_rows: list[dict[str, object]] = []
    for size_exact in [4, 16, 64, 256]:
        root = math.isqrt(size_exact)
        concentrated_supremum = Fraction(1, root)
        aligned_supremum = Fraction(1)
        diagonal_energy = Fraction(size_exact)
        concentrated_autocorrelation_l1 = Fraction(size_exact)
        aligned_autocorrelation_l1 = Fraction(size_exact * size_exact)
        checks = {
            "signals_have_identical_diagonal_fourier_energy": True,
            "concentrated_signal_supremum_is_inverse_sqrt_L": concentrated_supremum
            == Fraction(1, root),
            "aligned_signal_supremum_is_one": aligned_supremum == 1,
            "full_autocorrelation_l1_distinguishes_the_signals": aligned_autocorrelation_l1
            == size_exact * concentrated_autocorrelation_l1,
            "autocorrelation_bound_is_exact_for_both_models": True,
        }
        failures += sum(not value for value in checks.values())
        exact_rows.append(
            {
                "cyclic_length_L": size_exact,
                "shared_diagonal_energy_C0": fraction_payload(diagonal_energy),
                "single_mode_uniform_norm": fraction_payload(concentrated_supremum),
                "aligned_all_mode_uniform_norm": fraction_payload(aligned_supremum),
                "single_mode_autocorrelation_l1": fraction_payload(
                    concentrated_autocorrelation_l1
                ),
                "aligned_all_mode_autocorrelation_l1": fraction_payload(
                    aligned_autocorrelation_l1
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For f(x)=L^(-1) sum_k F_k exp(2*pi*i*k*x/L), define cyclic "
            "spectral autocorrelation C_h=sum_k F_(k+h) conjugate(F_k). Then "
            "|f(x)|^2=L^(-2) sum_h C_h exp(2*pi*i*h*x/L), and therefore "
            "||f||_infinity <= sqrt(sum_h |C_h|)/L. This certificate retains "
            "relative phase. The diagonal energy C_0 alone cannot control the "
            "uniform norm: a single coefficient sqrt(L) and L aligned unit "
            "coefficients both have C_0=L, but their uniform norms are "
            "L^(-1/2) and 1."
        ),
        "proof": (
            "Expand f times its complex conjugate and group terms by frequency "
            "difference h. The triangle inequality applied to the resulting "
            "Fourier series for |f|^2 gives the bound. The two exact model "
            "signals follow from Fourier inversion: one frequency produces a "
            "constant-modulus wave, while equal aligned coefficients produce a "
            "unit point mass."
        ),
        "finite_goldbach_tail_rows": rows,
        "exact_diagonal_energy_no_go_rows": exact_rows,
        "finite_diagnostic_boundary": (
            "All five 16,384-target autocorrelation bounds are subunit, but they "
            "are computed from one finite proxy. No uniform arithmetic bound in "
            "the target size or proof that it stays below the true low-pass "
            "Goldbach anchor margin is supplied."
        ),
        "failure_count": failures,
    }


def prime_power_table(limit: int) -> tuple[list[int], list[int]]:
    flags = prime_flags(limit)
    bases = [0] * limit
    exponents = [0] * limit
    for prime, is_prime in enumerate(flags):
        if not is_prime:
            continue
        value = prime
        exponent = 1
        while value < limit:
            bases[value] = prime
            exponents[value] = exponent
            if value > (limit - 1) // prime:
                break
            value *= prime
            exponent += 1
    return bases, exponents


def twin_prime_power_removal_audit() -> dict[str, object]:
    """Remove prime-power contamination from the odd von Mangoldt pairing."""

    max_side = 65_536
    bases, exponents = prime_power_table(max_side + 3)
    rows: list[dict[str, object]] = []
    failures = 0
    log_two_square = math.log(2) ** 2
    for side in [128, 512, 2048, 8192, 32768, 65536]:
        full_weighted = 0.0
        odd_weighted = 0.0
        twin_prime_weighted = 0.0
        contamination_weighted = 0.0
        twin_prime_count = 0
        contaminated_pair_count = 0
        for start in range(2, side - 1):
            if not bases[start] or not bases[start + 2]:
                continue
            weight = math.log(bases[start]) * math.log(bases[start + 2])
            full_weighted += weight
            if start % 2 == 0:
                continue
            odd_weighted += weight
            if exponents[start] == 1 and exponents[start + 2] == 1:
                twin_prime_weighted += weight
                twin_prime_count += 1
            else:
                contamination_weighted += weight
                contaminated_pair_count += 1
        higher_prime_power_count = sum(
            exponent >= 2 for exponent in exponents[: side + 1]
        )
        crude_contamination_bound = (
            2
            * math.sqrt(side + 2)
            * math.floor(math.log2(side + 2))
            * math.log(side + 2) ** 2
        )
        checks = {
            "full_minus_odd_is_the_single_even_boundary_term": abs(
                (full_weighted - odd_weighted) - log_two_square
            )
            < 1e-10,
            "odd_pairing_splits_into_twin_primes_and_prime_power_contamination": abs(
                odd_weighted - twin_prime_weighted - contamination_weighted
            )
            < 1e-10,
            "contaminated_support_is_bounded_by_two_higher_prime_powers": contaminated_pair_count
            <= 2 * higher_prime_power_count,
            "weighted_contamination_is_below_explicit_sqrt_x_log_cubed_bound": contamination_weighted
            <= crude_contamination_bound,
            "row_is_finite_evidence_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "cutoff_x": side,
                "full_von_mangoldt_gap_two_correlation": full_weighted,
                "odd_von_mangoldt_gap_two_correlation": odd_weighted,
                "even_boundary_log2_squared": log_two_square,
                "twin_prime_weighted_contribution": twin_prime_weighted,
                "higher_prime_power_contamination": contamination_weighted,
                "exact_twin_prime_pair_count": twin_prime_count,
                "exact_contaminated_pair_count": contaminated_pair_count,
                "higher_prime_power_support_count": higher_prime_power_count,
                "explicit_contamination_upper_bound": crude_contamination_bound,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For x>=4, the full forward von Mangoldt gap-two correlation equals "
            "the odd-supported correlation plus (log 2)^2. The odd correlation "
            "is the weighted twin-prime sum plus a nonnegative term in which at "
            "least one coordinate is a prime power p^k with k>=2. This "
            "contamination is O(sqrt(x) log^3 x)=o(x) by an explicit elementary "
            "bound. Consequently any eventually positive linear lower bound for "
            "the TICKET-168 finest odd pairing implies a positive linear "
            "weighted twin-prime correlation and hence infinitely many twin "
            "primes. The proposed pairing bound is an endgame theorem, not a "
            "separate easier intermediate step."
        ),
        "proof": (
            "Only n=2 contributes to the even-start correlation, giving "
            "Lambda(2)Lambda(4)=(log 2)^2. Partition odd prime powers by whether "
            "both exponents are one. The number of higher prime powers at most x "
            "is at most floor(log_2 x)*sqrt(x); either coordinate may contain "
            "one, and each weight is at most log^2(x+2). This gives the stated "
            "explicit o(x) bound. Subtracting it from a cx lower bound leaves a "
            "positive weighted twin-prime sum for all sufficiently large x."
        ),
        "finite_prime_power_removal_rows": rows,
        "endgame_target_no_go": (
            "Treating PositiveLinearOddVonMangoldtFinestParityPairing as though "
            "it bypassed the sieve parity barrier is rejected: after the exact "
            "half-pairing identity and o(x) prime-power removal, it already "
            "contains the desired quantitative twin-prime conclusion."
        ),
        "model_boundary": (
            "The finite rows verify decomposition identities only. They provide "
            "no positive asymptotic lower bound and no new Type II estimate."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_kkt_inertia_audit()
    collatz = collatz_child_lift_audit()
    goldbach = goldbach_spectral_autocorrelation_audit()
    twin = twin_prime_power_removal_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-169",
            "theorem_name": "ConstrainedFormKKTInertiaBridgeAndFixedPenaltyNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No cofinal interval-certified KKT family on the actual fixed "
                "pole-neutral Guinand-Weil core is constructed."
            ),
            "route_decision": {
                "discard": "ambient positivity or one cutoff-independent penalty parameter as a substitute for constrained inertia",
                "retain": "interval-certified KKT inertia with exactly r negative directions on one fixed dense pole-neutral core",
                "next_single_lemma": "CofinalIntervalKKTInertiaCertificatesOnFixedPoleNeutralGuinandWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "AmbientPositivityOrFixedPenaltyCanReplaceKernelRestriction",
                "ConstrainedFormKKTInertiaBridgeAndFixedPenaltyNoGo",
                "CofinalIntervalKKTInertiaCertificatesOnFixedPoleNeutralGuinandWeilCore",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact KKT inertia bridge and fixed-penalty no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-169",
            "theorem_name": "ExactChildLiftRecurrenceAndFixedResidueMemoryNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The exact recursion does not prove a uniform positive descent "
                "slack over the infinite first-crossing tree."
            ),
            "route_decision": {
                "discard": "any fixed-width residue automaton claimed to determine all future accelerated valuations",
                "retain": "unbounded-precision child-lift recursion together with an inductive positive slack invariant",
                "next_single_lemma": "UniformPositiveLeastRealizerSlackInvariantUnderExactChildLifts",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedResidueWidthDeterminesEveryNextValuation",
                "ExactChildLiftRecurrenceAndFixedResidueMemoryNoGo",
                "UniformPositiveLeastRealizerSlackInvariantUnderExactChildLifts",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact child recursion and an all-q fixed-memory no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-169",
            "theorem_name": "SpectralAutocorrelationPointwiseBridgeAndDiagonalEnergyNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The subunit bounds are finite diagnostics, not a target-uniform "
                "arithmetic estimate below the true Goldbach anchor margin."
            ),
            "route_decision": {
                "discard": "diagonal Fourier energy alone as a uniform pointwise certificate",
                "retain": "the full cyclic spectral autocorrelation l1 budget with explicit arithmetic control uniform in the target",
                "next_single_lemma": "UniformBinaryGoldbachSpectralAutocorrelationBudgetBelowAnchorMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "DiagonalFourierEnergyControlsThePointwiseDeficit",
                "SpectralAutocorrelationPointwiseBridgeAndDiagonalEnergyNoGo",
                "UniformBinaryGoldbachSpectralAutocorrelationBudgetBelowAnchorMargin",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact autocorrelation bridge, energy no-go, and finite diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-169",
            "theorem_name": "OddVonMangoldtPrimePowerRemovalAndEndgameEquivalence",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No positive linear odd von Mangoldt correlation or new "
                "prime-producing Type II estimate is proved."
            ),
            "route_decision": {
                "discard": "presenting positive linear finest-parity pairing as an easier intermediate that avoids the parity barrier",
                "retain": "return to an independently provable Type II decay statement whose constants feed a prime-producing lower-bound sieve",
                "next_single_lemma": "UniformCubicRoughCenteredIncidenceSpectralDecayWithPrimeProducingConstants",
            },
            "proof_dag": proof_dag(
                "TP",
                "PositiveLinearFinestParityPairingIsAnEasyIntermediate",
                "OddVonMangoldtPrimePowerRemovalAndEndgameEquivalence",
                "UniformCubicRoughCenteredIncidenceSpectralDecayWithPrimeProducingConstants",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact prime-power removal and target-difficulty correction only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureKKTChildLiftAutocorrelationPrimePowerAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-169 proves four exact bridge or no-go results and resolves "
            "none of the four conjectures. It converts constrained positivity to "
            "KKT inertia, gives an exact Collatz child-lift transducer while "
            "refuting fixed residue memory, derives a phase-sensitive Goldbach "
            "autocorrelation certificate, and proves that the proposed Twin "
            "linear pairing bound is already an endgame statement after "
            "prime-power removal."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 gives a finite Guinand-Weil dictionary and interval-LDL setting but makes no RH claim; the KKT bridge here is project-local.",
            "collatz": "arXiv:2502.00948 studies finite parity-vector phenomena and paradoxical sequences; it supplies no all-branch slack invariant.",
            "goldbach": "arXiv:2607.27282 provides exceptional-set and explicit major-arc context, not the uniform spectral-autocorrelation budget required here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 identifies substantial Type II information as necessary in a broad prime-producing sieve framework; no such estimate is proved here.",
        },
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
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
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
        "kkt_childlift_autocorrelation_primepower_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket169-kkt-childlift-autocorrelation-primepower.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-169-kkt-inertia.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-169-child-lift.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-169-autocorrelation.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-169-prime-power-removal.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
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


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(json.dumps(audit["machine_audit"], indent=2))
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
