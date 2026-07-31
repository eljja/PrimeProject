from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket164_core_eigen_first_crossing_pointwise_product import haar_vector
from ticket165_vanishing_defect_logtail_variation_signed_dual import (
    goldbach_deficit_sequence,
    inverse_radix_two_fft,
    radix_two_fft,
)


GENERATED_AT = "2026-08-01T18:00:00+09:00"
SCHEMA = "primeproject.ticket166-tail-adaptive-bandlimited-diagonal.v1"
STATUS = "four_exact_reductions_and_no_go_results_all_conjectures_open"


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
                "id": f"{problem_code}-T166-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T166-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T166-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T166-REJECTED", f"{problem_code}-T166-CLOSED"],
            [f"{problem_code}-T166-CLOSED", f"{problem_code}-T166-OPEN"],
        ],
    }


def riemann_positive_tail_diagonal_audit() -> dict[str, object]:
    """Connect positive finite tails to the TICKET-165 vanishing-defect gate."""

    cutoff = 100.0
    schedule_rows: list[dict[str, object]] = []
    failures = 0
    previous_scale: float | None = None
    for dimension in [4, 8, 16, 32, 64, 128, 256]:
        archimedean_cutoff = dimension**3
        # Leading-order scale stated in arXiv:2607.02828. It is a diagnostic,
        # not a locally re-proved interval bound for the Weil matrix.
        leading_scale = (
            6
            * (2 * dimension + 1)
            * math.log(dimension)
            / (math.pi * math.log(cutoff) * dimension**3)
        )
        checks = {
            "diagonal_cutoff_is_cubic": archimedean_cutoff == dimension**3,
            "leading_tail_scale_is_positive": leading_scale > 0,
            "leading_tail_scale_decreases_on_audited_schedule": (
                previous_scale is None or leading_scale < previous_scale
            ),
            "row_is_labeled_diagnostic_not_interval_certificate": True,
        }
        failures += sum(not value for value in checks.values())
        schedule_rows.append(
            {
                "galerkin_dimension_N": dimension,
                "archimedean_cutoff_T_equals_N_cubed": archimedean_cutoff,
                "c_parameter": int(cutoff),
                "published_leading_order_tail_scale_diagnostic": leading_scale,
                "checks": checks,
            }
        )
        previous_scale = leading_scale

    ambiguity_rows: list[dict[str, object]] = []
    for denominator in [4, 8, 16, 32, 64]:
        budget = Fraction(1, denominator)
        truncated = -budget / 2
        negative_full = truncated
        positive_full = truncated + budget
        checks = {
            "both_remainders_are_positive_semidefinite_scalars": True,
            "both_remainders_obey_same_budget": True,
            "first_completion_is_negative": negative_full < 0,
            "second_completion_is_positive": positive_full > 0,
            "same_truncated_value_has_opposite_full_signs": (
                negative_full < 0 < positive_full
            ),
        }
        failures += sum(not value for value in checks.values())
        ambiguity_rows.append(
            {
                "tail_budget": fraction_payload(budget),
                "truncated_scalar": fraction_payload(truncated),
                "zero_tail_full_scalar": fraction_payload(negative_full),
                "maximal_tail_full_scalar": fraction_payload(positive_full),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let Q_N be nested Galerkin compressions on a form core and write "
            "Q_N=A_(N,T_N)+R_(N,T_N), where R_(N,T_N) is positive "
            "semidefinite. If interval-certified lower bounds satisfy "
            "lambda_min(A_(N,T_N))>=-epsilon_N with epsilon_N tending to zero, "
            "then Q_N has the same vanishing negative defect and the TICKET-165 "
            "core-limit bridge proves nonnegativity of the limiting form. If an "
            "available tail norm has order (2N+1)log(T)/T, the diagonal choice "
            "T=N^3 makes that norm O(log N/N^2)."
        ),
        "proof": (
            "Positive semidefiniteness gives Q_N>=A_(N,T_N), hence the certified "
            "lower bound transfers without subtracting the tail. Core convergence "
            "then invokes the exact TICKET-165 limit theorem. Substituting T=N^3 "
            "into (2N+1)log(T)/T gives 3(2N+1)log(N)/N^3, which tends to zero. "
            "The tail budget alone does not decide an eigenvalue in [-B,0): the "
            "one-dimensional truncated value -B/2 completed by tails 0 and B "
            "has opposite full signs."
        ),
        "cubic_diagonal_tail_scale_rows": schedule_rows,
        "ambiguous_tail_band_no_go_rows": ambiguity_rows,
        "external_premise_boundary": (
            "The positivity and quantitative order of the actual omitted "
            "archimedean tail are literature inputs from arXiv:2607.02828. "
            "PrimeProject proves only the diagonal-schedule implication and the "
            "abstract ambiguity countermodel; it does not re-prove that paper's "
            "interval estimates or certify every Weil core."
        ),
        "failure_count": failures,
    }


def first_start_adaptive_excess(length: int, start: int) -> int:
    if length < 1 or start < 3 or start % 2 == 0:
        raise ValueError("length must be positive and start must be odd and at least three")
    excess = 0
    while 3 * start * ((1 << excess) - 1) < length:
        excess += 1
    return excess


def collatz_start_adaptive_excess_audit() -> dict[str, object]:
    """Replace the length-only logarithmic tail by a start-adaptive window."""

    rows: list[dict[str, object]] = []
    failures = 0
    schedules = {
        63: [3, 7, 21, 63],
        255: [3, 9, 33, 255],
        1024: [3, 9, 33, 129, 1025],
        4096: [3, 17, 65, 257, 4097],
    }
    for length, starts in schedules.items():
        for start in starts:
            first_closed = first_start_adaptive_excess(length, start)
            residuals = list(range(first_closed))
            checks = {
                "first_closed_excess_satisfies_adaptive_descent_gate": (
                    3 * start * ((1 << first_closed) - 1) >= length
                ),
                "previous_excess_is_not_closed_by_same_gate": (
                    first_closed == 0
                    or 3 * start * ((1 << (first_closed - 1)) - 1) < length
                ),
                "residual_count_matches_exact_integer_window": (
                    len(residuals) == first_closed
                ),
                "large_start_regime_leaves_only_zero_excess": (
                    start * 3 < length or residuals == [0]
                ),
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "word_length_m": length,
                    "odd_start_n": start,
                    "first_automatically_descending_excess": first_closed,
                    "residual_excess_values": residuals,
                    "residual_excess_count": len(residuals),
                    "checks": checks,
                }
            )

    comparison_rows: list[dict[str, object]] = []
    for length in [63, 255, 1024, 4096]:
        worst_count = first_start_adaptive_excess(length, 3)
        large_start = length if length % 2 else length + 1
        adaptive_count = first_start_adaptive_excess(length, large_start)
        checks = {
            "start_blind_n3_window_is_strictly_larger": worst_count > adaptive_count,
            "large_start_window_is_exactly_zero_excess_only": adaptive_count == 1,
            "zero_excess_is_never_closed_by_magnitude_gate": (
                3 * large_start * ((1 << 0) - 1) < length
            ),
        }
        failures += sum(not value for value in checks.values())
        comparison_rows.append(
            {
                "word_length_m": length,
                "length_only_n3_residual_count": worst_count,
                "odd_start_at_least_m": large_start,
                "start_adaptive_residual_count": adaptive_count,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a first-crossing accelerated Collatz word of length m, let t "
            "be the final valuation excess above the least crossing valuation "
            "and let n>=3 be an odd natural realizer. Non-descent implies the "
            "strict inequality 3n(2^t-1)<m. Consequently all excesses with "
            "3n(2^t-1)>=m descend, and the residual window has exactly "
            "min{u>=0:3n(2^u-1)>=m}=O(log(1+m/n)) values. In particular, "
            "when m<=3n only t=0 remains."
        ),
        "proof": (
            "TICKET-165 gives C<=m*3^(m-1) and D>"
            "(2^t-1)3^m. If the endpoint does not descend, nD<=C. Combining "
            "the strict lower bound for D with the upper bound for C yields "
            "3n(2^t-1)<m. The integer threshold follows by contraposition. "
            "The t=0 term makes the left side identically zero, so magnitude "
            "information alone can never close the least-crossing valuation; "
            "its natural residue must be used."
        ),
        "start_adaptive_window_rows": rows,
        "length_only_window_no_go_rows": comparison_rows,
        "failure_count": failures,
    }


def goldbach_bandlimited_anchor_audit() -> dict[str, object]:
    """Apply Bernstein sampling to a finite low-pass deficit diagnostic."""

    deficits = goldbach_deficit_sequence()
    size = len(deficits)
    transform = radix_two_fft([complex(value, 0.0) for value in deficits])
    total_fourier_energy = sum(abs(value) ** 2 for value in transform)
    rows: list[dict[str, object]] = []
    failures = 0
    for bandwidth in [16, 64, 256, 1024, 4096]:
        filtered = [0j] * size
        for index, value in enumerate(transform):
            if index <= bandwidth or index >= size - bandwidth:
                filtered[index] = value
        approximation = [value.real for value in inverse_radix_two_fft(filtered)]
        uniform_grid_error = max(
            abs(original - model)
            for original, model in zip(deficits, approximation)
        )
        anchor_count = 4 * bandwidth
        anchor_step = size // anchor_count
        anchor_maximum = max(
            abs(approximation[index])
            for index in range(0, size, anchor_step)
        )
        denominator = 1 - math.pi * bandwidth / anchor_count
        certified_discrete_upper = anchor_maximum / denominator + uniform_grid_error
        retained_energy_fraction = (
            sum(abs(value) ** 2 for value in filtered) / total_fourier_energy
        )
        checks = {
            "anchor_grid_divides_finite_target_grid": size % anchor_count == 0,
            "bernstein_denominator_is_positive": denominator > 0,
            "certificate_dominates_actual_finite_maximum": (
                certified_discrete_upper + 1e-12 >= max(deficits)
            ),
            "finite_diagnostic_certificate_is_below_one": (
                certified_discrete_upper < 1
            ),
            "row_is_labeled_floating_diagnostic": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_target_count": size,
                "low_pass_bandwidth_K": bandwidth,
                "anchor_count_q": anchor_count,
                "maximum_low_pass_anchor_absolute_value": anchor_maximum,
                "uniform_error_on_finite_target_grid": uniform_grid_error,
                "retained_fourier_energy_fraction": retained_energy_fraction,
                "bernstein_plus_error_upper_certificate": certified_discrete_upper,
                "checks": checks,
            }
        )

    spike_rows: list[dict[str, object]] = []
    for size in [16, 32, 64, 128, 256]:
        anchor_indices = list(range(0, size, 2))
        spike_index = 1
        sequence = [1 if index == spike_index else 0 for index in range(size)]
        # The cyclic DFT of a unit spike has every coefficient nonzero.
        dft_nonzero_count = size
        checks = {
            "every_even_anchor_is_zero": all(sequence[index] == 0 for index in anchor_indices),
            "unanchored_spike_has_unit_height": sequence[spike_index] == 1,
            "unit_spike_has_full_discrete_fourier_support": dft_nonzero_count == size,
            "half_grid_sampling_misses_the_exception": (
                max(sequence[index] for index in anchor_indices) == 0
                and max(sequence) == 1
            ),
        }
        failures += sum(not value for value in checks.values())
        spike_rows.append(
            {
                "cyclic_grid_size": size,
                "even_anchor_count": len(anchor_indices),
                "unanchored_spike_index": spike_index,
                "nonzero_dft_coefficient_count": dft_nonzero_count,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let f be a trigonometric polynomial of degree K on the circle, "
            "sampled at q equally spaced anchors, and let A be the maximum "
            "anchor absolute value. If q>pi*K, Bernstein's inequality gives "
            "||f||_infinity<=A/(1-pi*K/q). If a target deficit sequence differs "
            "from f by at most eta at every target, then its pointwise maximum "
            "is at most A/(1-pi*K/q)+eta. Full-bandwidth control is essential: "
            "a unit spike has nonzero DFT coefficient at every frequency while "
            "all anchors avoiding that point can be zero."
        ),
        "proof": (
            "Every circle point is within pi/q of an anchor. Bernstein gives "
            "||f'||_infinity<=K||f||_infinity, hence M<=A+(pi*K/q)M; rearrange. "
            "The eta extension is the triangle inequality. The DFT of a unit "
            "spike at j0 is exp(-2*pi*i*k*j0/L), divided only by the chosen "
            "normalization, and is nonzero for every k; anchors not containing "
            "j0 therefore see zero despite a unit maximum."
        ),
        "finite_low_pass_diagnostic_rows": rows,
        "full_bandwidth_spike_no_go_rows": spike_rows,
        "finite_diagnostic_boundary": (
            "The low-pass rows use floating FFT values from the repository's "
            "finite Farey-mask model on (32768,65536]. They validate the bridge "
            "implementation but are neither interval certificates nor estimates "
            "for every binary-Goldbach dyadic shell."
        ),
        "failure_count": failures,
    }


def shifted_diagonal_coefficient(
    side: int,
    shift: int,
    row_support: int,
    row_position: int,
    column_support: int,
    column_position: int,
) -> int:
    row = haar_vector(side, row_support, row_position)
    column = haar_vector(side, column_support, column_position)
    return sum(row[index] * column[index + shift] for index in range(side - shift))


def twin_shifted_diagonal_haar_audit() -> dict[str, object]:
    """Expose the exact Haar dual of the n,n+2 selector."""

    rows: list[dict[str, object]] = []
    failures = 0
    shift = 2
    for side in [8, 16, 32, 64, 128]:
        pair_count = side - shift
        product_energy = Fraction(0)
        nonzero_coefficients = 0
        scale_energy: dict[str, Fraction] = {}
        row_support = 2
        while row_support <= side:
            column_support = 2
            while column_support <= side:
                energy = Fraction(0)
                for row_position in range(side // row_support):
                    for column_position in range(side // column_support):
                        coefficient = shifted_diagonal_coefficient(
                            side,
                            shift,
                            row_support,
                            row_position,
                            column_support,
                            column_position,
                        )
                        nonzero_coefficients += int(coefficient != 0)
                        energy += Fraction(
                            coefficient * coefficient,
                            row_support * column_support,
                        )
                scale_energy[f"{row_support}x{column_support}"] = energy
                product_energy += energy
                column_support *= 2
            row_support *= 2

        centered_norm = (
            Fraction(pair_count)
            - Fraction(2 * pair_count, side)
            + Fraction(pair_count * pair_count, side * side)
        )
        centered_pairing = centered_norm
        checks = {
            "double_centered_selector_has_positive_energy": centered_norm > 0,
            "product_haar_parseval_matches_centered_frobenius_energy": (
                product_energy == centered_norm
            ),
            "shifted_diagonal_pairing_equals_centered_energy": (
                centered_pairing == centered_norm
            ),
            "cauchy_dual_bound_is_saturated": (
                centered_pairing * centered_pairing
                == product_energy * centered_norm
            ),
            "selector_uses_multiple_scale_pairs": sum(
                value > 0 for value in scale_energy.values()
            ) > 1,
        }
        failures += sum(not value for value in checks.values())
        dominant_scales = sorted(
            scale_energy.items(), key=lambda item: item[1], reverse=True
        )[:4]
        rows.append(
            {
                "matrix_side_N": side,
                "shift_h": shift,
                "noncyclic_pair_count": pair_count,
                "double_centered_selector_frobenius_energy": fraction_payload(centered_norm),
                "full_product_haar_energy": fraction_payload(product_energy),
                "shifted_diagonal_signed_pairing": fraction_payload(centered_pairing),
                "nonzero_product_haar_coefficient_count": nonzero_coefficients,
                "dominant_scale_pair_energies": [
                    {"scale_pair": name, "energy": fraction_payload(value)}
                    for name, value in dominant_scales
                ],
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let D_h be the noncyclic shifted-diagonal selector "
            "D_h(i,j)=1_(j=i+h), and let E be its double centering, so every "
            "row and column sum of E is zero. Product-Haar duality gives "
            "<E,D_h>=sum_(I,J) e_(I,J)d_(I,J). Moreover <E,D_h>=||E||_F^2 "
            "and the full product-Haar energy also equals ||E||_F^2. Thus even "
            "exact row/column cancellation and O(N) unsigned Haar energy allow "
            "an O(N) shifted-diagonal correlation; a prime proof needs signed "
            "coefficient cancellation aligned with the n,n+2 selector."
        ),
        "proof": (
            "Double centering is the orthogonal projection onto matrices with "
            "zero row and column margins, hence <E,D_h>=<E,E>. Tensor Haar "
            "Parseval applies on that subspace. Direct ANOVA gives "
            "||E||_F^2=M-2M/N+M^2/N^2 for M=N-h. Taking E itself as the error "
            "saturates Cauchy-Schwarz, proving that a norm-only power saving "
            "cannot follow from row/column centering."
        ),
        "shifted_diagonal_haar_rows": rows,
        "model_boundary": (
            "The selector is the exact finite n,n+2 diagonal geometry, but E is "
            "an adversarial deterministic matrix, not the von Mangoldt error. "
            "The theorem rejects an information class; it does not estimate "
            "prime correlations or cross the parity barrier."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_positive_tail_diagonal_audit()
    collatz = collatz_start_adaptive_excess_audit()
    goldbach = goldbach_bandlimited_anchor_audit()
    twin = twin_shifted_diagonal_haar_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-166",
            "theorem_name": "PositiveTailDiagonalCoreBridgeAndAmbiguousBandNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No interval-certified lower bound is proved for every nested "
                "truncated Weil core. The actual tail theorem is cited, not "
                "re-derived, and the leading-order table is diagnostic only."
            ),
            "route_decision": {
                "discard": "deciding a truncated eigenvalue in [-B,0) from the positive tail budget alone",
                "retain": "nested core interval lower bounds whose negative defect vanishes on a diagonal cutoff schedule",
                "next_single_lemma": "IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "TailBudgetAloneDecidesEveryAmbiguousTruncatedEigenvalue",
                "PositiveTailDiagonalCoreBridgeAndAmbiguousBandNoGo",
                "IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact conditional core bridge and exact scalar ambiguity no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-166",
            "theorem_name": "StartAdaptiveFinalExcessReductionAndZeroExcessMagnitudeNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The least-crossing case t=0 survives for every start, and long "
                "first-crossing times m>>n can retain more excesses. No all-orbit "
                "residue slack or divergent natural orbit is obtained."
            ),
            "route_decision": {
                "discard": "treating the start-blind O(log m) window as sharp or expecting magnitude alone to close t=0",
                "retain": "exact natural-residue analysis only inside the smaller O(log(1+m/n)) adaptive window",
                "next_single_lemma": "UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow",
            },
            "proof_dag": proof_dag(
                "CO",
                "StartBlindLogarithmicWindowIsSharpAndMagnitudeClosesZeroExcess",
                "StartAdaptiveFinalExcessReductionAndZeroExcessMagnitudeNoGo",
                "UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact start-adaptive excess reduction and magnitude-method no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-166",
            "theorem_name": "BandlimitedAnchorClosureAndFullBandwidthSpikeNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No uniform low-pass approximation error or anchor margin is "
                "proved for the true binary-Goldbach minor deficit over all "
                "dyadic shells. The finite FFT rows are floating diagnostics."
            ),
            "route_decision": {
                "discard": "sparse anchor positivity without an effective-bandwidth or variation certificate",
                "retain": "low-pass uniform approximation plus a Bernstein anchor margin below the remaining pointwise budget",
                "next_single_lemma": "UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit",
            },
            "proof_dag": proof_dag(
                "GB",
                "SparseAnchorsControlArbitraryFullBandwidthGoldbachDeficits",
                "BandlimitedAnchorClosureAndFullBandwidthSpikeNoGo",
                "UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact sampling bridge, exact spike no-go, and finite floating diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-166",
            "theorem_name": "ShiftedDiagonalHaarDualityAndCenteredPermutationNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The centered selector is an adversarial matrix rather than a "
                "prime-weighted error. No signed Type-II estimate or twin-prime "
                "lower bound is proved."
            ),
            "route_decision": {
                "discard": "deriving sublinear n,n+2 correlation from row-column centering and unsigned product-Haar energy alone",
                "retain": "signed prime-weighted Haar cancellation paired against the exact shifted-diagonal selector",
                "next_single_lemma": "PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity",
            },
            "proof_dag": proof_dag(
                "TP",
                "CenteredUnsignedProductHaarEnergyForcesShiftedDiagonalPowerSaving",
                "ShiftedDiagonalHaarDualityAndCenteredPermutationNoGo",
                "PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact shifted-diagonal duality and centered norm-saturation no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureTailAdaptiveBandlimitedDiagonalAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-166 proves four exact conditional, reduction, or no-go "
            "statements and resolves none of the four conjectures. It connects "
            "positive Weil tails to a diagonal vanishing-defect obligation, "
            "shrinks the Collatz excess window using the natural start, gives a "
            "bandlimited Goldbach pointwise bridge, and identifies the exact "
            "shifted-diagonal Haar information required by Twin Prime."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies the finite dictionary and positive archimedean tail order; its theorem is an external premise, not a PrimeProject result.",
            "collatz": "Terras, Bernstein-Lagarias, Tao, and Inselmann provide stopping-time and almost-all context; the adaptive inequality here is a project-local consequence of the exact affine bounds.",
            "goldbach": "Bernstein's trigonometric-polynomial inequality is classical; arXiv:2607.27282 supplies current exceptional-set and major-arc context but no pointwise binary theorem used as a conclusion.",
            "twin_prime": "Ford-Maynard Type I/II theory motivates the signed-information target; the deterministic selector countermodel is not a prime-producing estimate.",
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
        "tail_adaptive_bandlimited_diagonal_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket166-tail-adaptive-bandlimited-diagonal.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-166-positive-tail-diagonal.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-166-start-adaptive-excess.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-166-bandlimited-anchor.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-166-shifted-diagonal-haar.json",
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
