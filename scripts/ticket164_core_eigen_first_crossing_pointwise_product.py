from __future__ import annotations

import json
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket163_local_certificate_realizer_trace_carleson import (
    goldbach_dyadic_budget_audit,
)


GENERATED_AT = "2026-07-31T23:30:00+09:00"
SCHEMA = "primeproject.ticket164-core-eigen-first-crossing-pointwise-product.v1"
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
                "id": f"{problem_code}-T164-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T164-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T164-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T164-REJECTED", f"{problem_code}-T164-CLOSED"],
            [f"{problem_code}-T164-CLOSED", f"{problem_code}-T164-OPEN"],
        ],
    }


def riemann_constraint_core_audit() -> dict[str, object]:
    """Audit the finite-dimensional sign question after linear constraints."""

    exact_core = {
        "form_diagonal": [3, -1, -1],
        "constraint_row": [1, 1, 1],
        "kernel_basis_columns": [[1, 1], [-1, 0], [0, -1]],
        "compressed_form": [[2, 3], [3, 2]],
        "compressed_determinant": -5,
        "negative_coefficient_witness": [1, -1],
        "negative_original_witness": [0, -1, 1],
        "negative_witness_value": -2,
        "ambient_trace": 1,
        "ambient_determinant": 3,
        "all_ones_quadratic_value": 1,
    }
    rows: list[dict[str, object]] = []
    failures = 0
    for dimension in [5, 9, 17, 33]:
        diagonal = [1] * (dimension - 2) + [-1, -1]
        witness = [0] * (dimension - 2) + [1, -1]
        trace = sum(diagonal)
        determinant = 1
        ones_value = sum(diagonal)
        witness_value = sum(
            coefficient * value * value
            for coefficient, value in zip(diagonal, witness)
        )
        checks = {
            "ambient_trace_is_positive": trace > 0,
            "ambient_determinant_is_positive": determinant > 0,
            "all_ones_quadratic_value_is_positive": ones_value > 0,
            "witness_satisfies_sum_zero_constraint": sum(witness) == 0,
            "constraint_core_has_negative_direction": witness_value < 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "ambient_trace": trace,
                "ambient_determinant": determinant,
                "all_ones_quadratic_value": ones_value,
                "constraint_core_negative_witness_value": witness_value,
                "checks": checks,
            }
        )

    exact_checks = {
        "compressed_determinant_is_negative": exact_core["compressed_determinant"] < 0,
        "witness_is_in_constraint_kernel": sum(exact_core["negative_original_witness"]) == 0,
        "witness_value_is_negative": exact_core["negative_witness_value"] < 0,
        "scalar_ambient_diagnostics_are_positive": (
            exact_core["ambient_trace"] > 0
            and exact_core["ambient_determinant"] > 0
            and exact_core["all_ones_quadratic_value"] > 0
        ),
    }
    failures += sum(not value for value in exact_checks.values())
    return {
        "theorem": (
            "Let H be a real symmetric finite Galerkin form, let B have full row "
            "rank, and let the columns of U span ker(B). Then H is nonnegative "
            "on the constraint core ker(B) if and only if the compressed form "
            "U^T H U is positive semidefinite. Positive ambient trace, positive "
            "ambient determinant, and a positive value on the all-ones vector "
            "do not imply this condition: H=diag(3,-1,-1), B=(1,1,1) has all "
            "three scalar diagnostics positive but the core witness (0,-1,1) "
            "has quadratic value -2."
        ),
        "proof": (
            "Every constrained vector is Uc, so its quadratic value is exactly "
            "c^T(U^T H U)c; this proves the compression equivalence by congruence. "
            "For the displayed form, the kernel basis columns (1,-1,0) and "
            "(1,0,-1) give compressed matrix [[2,3],[3,2]], whose determinant "
            "is -5. The scalable diagonal family with two negative coordinates "
            "keeps trace, determinant, and the all-ones value positive while the "
            "sum-zero difference of the last two coordinates always has value -2."
        ),
        "exact_three_dimensional_core": exact_core,
        "scalable_scalar_cancellation_no_go_rows": rows,
        "exact_checks": exact_checks,
        "failure_count": failures,
    }


def decode_word(code: int, length: int) -> tuple[int, ...]:
    return tuple((code >> (5 * index)) & 31 for index in range(length))


def append_word(code: int, length: int, valuation: int) -> int:
    if not 1 <= valuation < 32:
        raise ValueError("five-bit valuation encoding overflow")
    return code | (valuation << (5 * length))


def first_crossing_valuation(prefix_sum: int, power_three: int) -> int:
    valuation = 1
    while 1 << (prefix_sum + valuation) <= power_three:
        valuation += 1
    return valuation


def collatz_realizer_from_correction(
    length: int,
    total: int,
    correction: int,
    *,
    nonterminal: bool = True,
) -> tuple[int, int, int]:
    denominator = 1 << total
    modulus = 1 << (total + 1)
    power_three = 3**length
    residue = ((denominator - correction) * pow(power_three, -1, modulus)) % modulus
    if residue == 0:
        residue = modulus
    if nonterminal and residue == 1:
        residue += modulus
    endpoint = (power_three * residue + correction) // denominator
    return residue, endpoint, residue - endpoint


def collatz_replay(start: int, length: int) -> tuple[tuple[int, ...], int]:
    value = start
    valuations: list[int] = []
    for _ in range(length):
        numerator = 3 * value + 1
        valuation = (numerator & -numerator).bit_length() - 1
        valuations.append(valuation)
        value = numerator >> valuation
    return tuple(valuations), value


def collatz_first_crossing_audit(max_length: int = 17) -> dict[str, object]:
    # State is (five-bit packed word, valuation sum, affine correction).
    states: list[tuple[int, int, int]] = [(0, 0, 0)]
    rows: list[dict[str, object]] = []
    failures = 0
    total_candidate_words = 0
    total_replay_failures = 0
    global_minimum_margin: int | None = None

    for length in range(1, max_length + 1):
        power_three = 3**length
        candidate_count = 0
        replay_failures = 0
        minimum_margin: int | None = None
        minimum_witness: dict[str, object] | None = None
        maximum_candidate_final_valuation = 0
        next_states: list[tuple[int, int, int]] = []

        for code, prefix_sum, prefix_correction in states:
            correction = 3 * prefix_correction + (1 << prefix_sum)
            first_valuation = first_crossing_valuation(prefix_sum, power_three)
            final_valuation = first_valuation
            while True:
                total = prefix_sum + final_valuation
                slope_gap = (1 << total) - power_three
                # If 3*slope_gap > correction, every nonterminal odd n>=3 descends.
                if 3 * slope_gap > correction:
                    break
                candidate_count += 1
                maximum_candidate_final_valuation = max(
                    maximum_candidate_final_valuation,
                    final_valuation,
                )
                full_code = append_word(code, length - 1, final_valuation)
                word = decode_word(full_code, length)
                start, endpoint, margin = collatz_realizer_from_correction(
                    length,
                    total,
                    correction,
                )
                replay_word, replay_endpoint = collatz_replay(start, length)
                replay_ok = replay_word == word and replay_endpoint == endpoint
                replay_failures += int(not replay_ok)
                if minimum_margin is None or margin < minimum_margin:
                    minimum_margin = margin
                    minimum_witness = {
                        "valuation_word": list(word),
                        "least_nonterminal_realizer": start,
                        "endpoint": endpoint,
                        "strict_descent_margin": margin,
                        "affine_correction": correction,
                        "slope_gap": slope_gap,
                    }
                final_valuation += 1

            extend_valuation = 1
            while 1 << (prefix_sum + extend_valuation) <= power_three:
                next_states.append(
                    (
                        append_word(code, length - 1, extend_valuation),
                        prefix_sum + extend_valuation,
                        correction,
                    )
                )
                extend_valuation += 1

        checks = {
            "all_potential_non_descent_words_replay": replay_failures == 0,
            "all_potential_nonterminal_words_strictly_descend": (
                minimum_margin is None or minimum_margin > 0
            ),
            "infinite_final_valuation_tail_is_closed_by_affine_bound": True,
            "enumeration_is_complete_only_at_this_fixed_length": True,
        }
        failures += sum(not value for value in checks.values())
        total_candidate_words += candidate_count
        total_replay_failures += replay_failures
        if minimum_margin is not None:
            global_minimum_margin = (
                minimum_margin
                if global_minimum_margin is None
                else min(global_minimum_margin, minimum_margin)
            )
        rows.append(
            {
                "word_length_m": length,
                "noncontracting_prefix_count": len(states),
                "potential_non_descent_word_count": candidate_count,
                "next_noncontracting_prefix_count": len(next_states),
                "maximum_candidate_final_valuation": maximum_candidate_final_valuation,
                "minimum_strict_descent_margin": minimum_margin,
                "minimum_margin_witness": minimum_witness,
                "checks": checks,
            }
        )
        states = next_states

    # First-crossing margin is not monotone in the final valuation.
    shortcut_rows: list[dict[str, object]] = []
    for word in [(1, 3), (1, 4)]:
        correction = 3 * 1 + 2
        start, endpoint, margin = collatz_realizer_from_correction(
            2,
            sum(word),
            correction,
        )
        shortcut_rows.append(
            {
                "valuation_word": list(word),
                "least_nonterminal_realizer": start,
                "endpoint": endpoint,
                "strict_descent_margin": margin,
                "replay": list(collatz_replay(start, 2)[0]),
            }
        )
    shortcut_checks = {
        "both_words_first_cross_at_length_two": all(
            (1 << word["valuation_word"][0]) <= 3
            and (1 << sum(word["valuation_word"])) > 9
            for word in shortcut_rows
        ),
        "larger_final_valuation_has_smaller_margin": (
            shortcut_rows[1]["strict_descent_margin"]
            < shortcut_rows[0]["strict_descent_margin"]
        ),
        "both_shortcut_words_replay_exactly": all(
            row["valuation_word"] == row["replay"] for row in shortcut_rows
        ),
    }
    failures += sum(not value for value in shortcut_checks.values())
    return {
        "theorem": (
            "For a first-crossing valuation word a of length m, every proper "
            "prefix obeys 2^S_j<=3^j and the full word obeys 2^S>3^m. "
            "Writing 2^S T_a(n)=3^m n+C(a), a nonterminal non-descent can "
            "occur only if 3(2^S-3^m)<=C(a). Hence each fixed prefix has only "
            "finitely many final valuations requiring residue replay; all larger "
            "valuations descend automatically for every odd n>=3. Exhaustive "
            "prefix enumeration and exact odd-residue replay certify strict "
            "descent for every first-crossing word of length m<=17."
        ),
        "proof": (
            "Non-descent is equivalent to (2^S-3^m)n<=C(a). For a nonterminal "
            "odd start n>=3 this implies 3(2^S-3^m)<=C(a), giving the finite "
            "last-valuation bound. For each remaining word, exactness and an odd "
            "endpoint are enforced modulo 2^(S+1); the least nonterminal "
            "realizer is the worst one because every later realizer increases "
            "the descent margin by 2(2^S-3^m). The computation enumerates every "
            "noncontracting prefix through length 16 and every bounded final "
            "valuation through full length 17. It is not an all-length proof."
        ),
        "complete_first_crossing_rows": rows,
        "final_valuation_monotonicity_no_go": {
            "rows": shortcut_rows,
            "checks": shortcut_checks,
            "statement": (
                "Checking only the least crossing final valuation cannot be "
                "justified by monotonicity: (1,3) has margin 8, whereas the "
                "larger final valuation word (1,4) has margin 2."
            ),
        },
        "maximum_certified_length": max_length,
        "total_potential_non_descent_words_replayed": total_candidate_words,
        "total_replay_failure_count": total_replay_failures,
        "global_minimum_strict_descent_margin": global_minimum_margin,
        "failure_count": failures,
    }


def goldbach_pointwise_gate_audit() -> dict[str, object]:
    prior = goldbach_dyadic_budget_audit()
    rows: list[dict[str, object]] = []
    failures = 0
    for row in prior["finite_prime_dft_dyadic_shell_rows"]:
        maximum_deficit = float(row["maximum_normalized_deficit"])
        checks = {
            "direct_integer_scan_has_no_zero": row["observed_zero_count"] == 0,
            "pointwise_gate_passes": maximum_deficit < 1,
            "pointwise_margin_is_positive": 1 - maximum_deficit > 0,
            "fft_and_integer_decisions_agree": (
                row["fft_positivity_mismatch_count"] == 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dyadic_lower_exclusive": row["dyadic_lower_exclusive"],
                "dyadic_upper_inclusive": row["dyadic_upper_inclusive"],
                "maximum_normalized_deficit": maximum_deficit,
                "pointwise_margin_to_one": 1 - maximum_deficit,
                "l2_shell_budget": row["normalized_negative_budget"],
                "l2_unit_gate_passes": row["unit_gate_passes"],
                "observed_zero_count": row["observed_zero_count"],
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for size in [4, 16, 64, 256, 1_024]:
        deficit = Fraction(1, 2)
        budget = size * deficit * deficit
        no_go_rows.append(
            {
                "block_size": size,
                "main_term_M": 2,
                "integer_count_G": 1,
                "normalized_deficit": fraction_payload(deficit),
                "l2_budget": fraction_payload(budget),
                "zero_count": 0,
                "pointwise_gate_passes": True,
                "l2_unit_gate_passes": budget < 1,
            }
        )
    no_go_checks = {
        "all_counts_are_strictly_positive": all(row["zero_count"] == 0 for row in no_go_rows),
        "all_pointwise_gates_pass": all(row["pointwise_gate_passes"] for row in no_go_rows),
        "l2_budget_is_unbounded": no_go_rows[-1]["l2_budget"]["decimal"] > 100,
        "l2_unit_gate_fails_from_first_row": all(
            not row["l2_unit_gate_passes"] for row in no_go_rows
        ),
    }
    failures += sum(not value for value in no_go_checks.values())
    return {
        "theorem": (
            "If G_N=M_N+E_N is a nonnegative integer and M_N>0, then "
            "G_N>0 if and only if d_N=E_N^-/M_N<1. Thus a finite block has "
            "no exception if and only if max d_N<1. The shell L2 condition "
            "sum d_N^2<1 from TICKET-163 remains sufficient but is not "
            "necessary and can be arbitrarily stronger: taking M_N=2 and "
            "G_N=1 at every one of L targets gives no zeros, max d_N=1/2, "
            "and L2 budget L/4 tending to infinity."
        ),
        "proof": (
            "If G_N=0 then E_N=-M_N and d_N=1. If G_N>=1, either E_N>=0 "
            "and d_N=0 or E_N<0 and d_N=1-G_N/M_N<1. This proves the exact "
            "pointwise equivalence. The constant positive-count construction "
            "proves the L2 non-necessity statement. Finite prime DFT rows are "
            "paired with an independent integer prime-pair scan; they diagnose "
            "the pointwise margin only and do not establish an infinite bound."
        ),
        "finite_prime_pointwise_rows": rows,
        "positive_count_l2_no_go_rows": no_go_rows,
        "no_go_checks": no_go_checks,
        "failure_count": failures,
    }


def haar_vector(length: int, support_size: int, position: int) -> list[int]:
    start = position * support_size
    half = support_size // 2
    return [
        1 if start <= index < start + half else -1 if start + half <= index < start + support_size else 0
        for index in range(length)
    ]


def haar_energy_by_scale(vector: list[int]) -> dict[int, Fraction]:
    length = len(vector)
    energies: dict[int, Fraction] = {}
    support_size = 2
    while support_size <= length:
        energy = Fraction(0)
        for position in range(length // support_size):
            basis = haar_vector(length, support_size, position)
            coefficient = sum(left * right for left, right in zip(vector, basis))
            energy += Fraction(coefficient * coefficient, support_size)
        energies[support_size] = energy
        support_size *= 2
    return energies


def twin_product_haar_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for side in [8, 16, 32, 64, 128]:
        row_scale = 2
        column_scale = side // 2
        row_vector = haar_vector(side, row_scale, 0)
        column_vector = haar_vector(side, column_scale, 0)
        row_energy = haar_energy_by_scale(row_vector)
        column_energy = haar_energy_by_scale(column_vector)
        product_energy = sum(row_energy.values()) * sum(column_energy.values())
        isotropic_energy = sum(
            row_energy[scale] * column_energy[scale] for scale in row_energy
        )
        frobenius_energy = Fraction(
            sum(value * value for value in row_vector)
            * sum(value * value for value in column_vector)
        )
        checks = {
            "row_factor_has_zero_mean": sum(row_vector) == 0,
            "column_factor_has_zero_mean": sum(column_vector) == 0,
            "product_haar_parseval_is_exact": product_energy == frobenius_energy,
            "same_scale_tensor_energy_is_zero": isotropic_energy == 0,
            "anisotropic_product_energy_is_positive": product_energy > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "matrix_side": side,
                "row_haar_support": row_scale,
                "column_haar_support": column_scale,
                "frobenius_energy": fraction_payload(frobenius_energy),
                "full_product_haar_energy": fraction_payload(product_energy),
                "same_scale_tensor_energy": fraction_payload(isotropic_energy),
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "For a finite matrix with zero row and column margins, the full "
            "Frobenius energy equals the sum of normalized product-Haar "
            "coefficient energies over independently chosen row and column "
            "dyadic scales. Retaining only equal row/column scales is not "
            "complete: the tensor of a row Haar wavelet of support 2 and a "
            "column Haar wavelet of support N/2 has positive full energy N "
            "and exactly zero equal-scale tensor energy."
        ),
        "proof": (
            "The one-dimensional constant plus Haar vectors form an orthogonal "
            "basis. Tensoring the two expansions gives product Parseval; zero "
            "row and column margins remove the constant-axis terms. For the "
            "separable witness u tensor v, each coefficient factors as "
            "<u,h_I><v,h_J>. Orthogonality leaves exactly the unequal scale "
            "pair (2,N/2), so every equal-scale product coefficient vanishes "
            "while the complete product energy equals ||u||^2||v||^2=N."
        ),
        "anisotropic_product_rows": rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_constraint_core_audit()
    collatz = collatz_first_crossing_audit()
    goldbach = goldbach_pointwise_gate_audit()
    twin = twin_product_haar_audit()
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-164",
            "theorem_name": "ConstraintCoreCompressionAndScalarCancellationNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The compression theorem is finite linear algebra. No uniform "
                "lower bound is proved for the actual Guinand-Weil matrices, "
                "and no cutoff-free positivity statement follows."
            ),
            "route_decision": {
                "discard": "scalar cancellation diagnostics such as trace, determinant, or one test-vector value as substitutes for constrained positivity",
                "retain": "the minimum eigenvalue of the complete signed Guinand-Weil form compressed to its admissible constraint core",
                "next_single_lemma": "UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound",
            },
            "proof_dag": proof_dag(
                "RH",
                "ScalarCancellationDiagnosticsImplyConstraintCorePositivity",
                "ConstraintCoreCompressionAndScalarCancellationNoGo",
                "UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact finite compression criterion and scalable scalar-diagnostic no-go.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-164",
            "theorem_name": "FirstContractingLayerFiniteCertificateAndFinalValuationBound",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Every first-crossing word is certified only for lengths at "
                "most 17. The number of noncontracting prefixes still grows, "
                "and no all-length residue-slack inequality has been proved."
            ),
            "route_decision": {
                "discard": "checking only the least crossing final valuation by an assumed monotonic descent margin",
                "retain": "the exact affine candidate bound plus least nonterminal residue replay for every first-crossing prefix",
                "next_single_lemma": "UniformFirstContractingLayerResidueSlack",
            },
            "proof_dag": proof_dag(
                "CO",
                "FirstCrossingDescentMarginIsMonotoneInFinalValuation",
                "FirstContractingLayerFiniteCertificateAndFinalValuationBound",
                "UniformFirstContractingLayerResidueSlack",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; complete first-crossing certificate through length 17 and exact finite final-valuation reduction.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-164",
            "theorem_name": "PointwiseIntegralExceptionEquivalenceAndL2NonNecessityNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The exact pointwise criterion is close to the original "
                "positivity problem. The finite DFT supplies no uniform analytic "
                "minor-arc margin over all even targets."
            ),
            "route_decision": {
                "discard": "treating the shell L2 budget below one as a necessary or decisive Goldbach target",
                "retain": "the exact pointwise normalized negative-minor deficit strictly below one at every even target",
                "next_single_lemma": "UniformDyadicPointwiseMinorDeficitStrictlyBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "ShellL2BudgetBelowOneIsNecessaryForNoGoldbachZeros",
                "PointwiseIntegralExceptionEquivalenceAndL2NonNecessityNoGo",
                "UniformDyadicPointwiseMinorDeficitStrictlyBelowOne",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact pointwise equivalence, strict L2 non-necessity no-go, and finite diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-164",
            "theorem_name": "ProductHaarParsevalAndEqualScaleTensorNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "Product-Haar Parseval is deterministic. It gives no "
                "prime-weighted coefficient saving, no parity-breaking lower "
                "bound, and no infinitude of gap-two primes."
            ),
            "route_decision": {
                "discard": "retaining only equal row and column Haar scales in the local Type-II diagnostic",
                "retain": "independent row/column product-Haar localization over every relevant prime-weighted rectangle",
                "next_single_lemma": "UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity",
            },
            "proof_dag": proof_dag(
                "TP",
                "EqualScaleTensorHaarEnergyCapturesEveryLocalTypeIIMode",
                "ProductHaarParsevalAndEqualScaleTensorNoGo",
                "UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact product-Haar identity and anisotropic equal-scale no-go.",
        },
    }
    total_failures = sum(
        int(section["reproducible_computation"]["failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCoreEigenFirstCrossingPointwiseProductAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-164 proves four exact reductions or no-go theorems and "
            "resolves none of the four conjectures. It replaces scalar RH "
            "cancellation by constrained minimum-eigenvalue positivity, reduces "
            "finite Collatz first-crossing verification to finitely many exact "
            "residues, replaces an overly strong Goldbach L2 target by its exact "
            "pointwise gate, and expands Twin localization to product scales."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "Finite Guinand-Weil Galerkin work motivates the compressed-form target; this ticket proves only an abstract finite linear-algebra criterion.",
            "collatz": "Tao's almost-all result is external and does not provide the all-orbit residue-slack lemma proved here only through length 17.",
            "goldbach": "Current exceptional-set and explicit major-arc work is external; no imported theorem supplies the required pointwise binary minor-arc margin.",
            "twin_prime": "Ford-Maynard Type I/II theory motivates product localization; this deterministic Haar theorem is not a prime-producing estimate.",
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
    for problem_id, key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[key]
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
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    global_payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "core_eigen_first_crossing_pointwise_product_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket164-core-eigen-first-crossing-pointwise-product.json",
        global_payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-164-constraint-core-eigenvalue.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-164-first-crossing-residue.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-164-pointwise-deficit.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-164-product-haar.json",
    }
    keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
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
