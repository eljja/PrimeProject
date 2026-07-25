from __future__ import annotations

import cmath
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-07-27T09:00:00+09:00"
SCHEMA = "primeproject.ticket147-fiber-compensation-phase-graph.v1"
STATUS = "exact_partial_theorems_and_route_no_go_all_conjectures_open"


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
    rejected_id = f"{problem_code}-T147-REJECTED"
    closed_id = f"{problem_code}-T147-CLOSED"
    open_id = f"{problem_code}-T147-OPEN"
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
        "edges": [
            [rejected_id, closed_id],
            [closed_id, open_id],
        ],
    }


def polynomial_from_integer_roots(roots: Sequence[int]) -> list[int]:
    coefficients = [1]
    for root in roots:
        updated = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            updated[index] -= root * coefficient
            updated[index + 1] += coefficient
        coefficients = updated
    return coefficients


def exact_matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / scale for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor == 0:
                continue
            matrix[row] = [
                matrix[row][index]
                - factor * matrix[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def riemann_fiber_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for generator_count in range(1, 9):
        alias_count = generator_count + 1
        generator_fibers = [
            [
                base**power
                for power in range(alias_count)
            ]
            for base in range(1, generator_count + 1)
        ]
        annihilator = polynomial_from_integer_roots(
            list(range(1, generator_count + 1))
        )
        residuals = [
            sum(
                row[index] * annihilator[index]
                for index in range(alias_count)
            )
            for row in generator_fibers
        ]
        rank = exact_matrix_rank(generator_fibers)
        checks = {
            "fiber_rank_equals_generator_count": rank == generator_count,
            "nonzero_annihilator": any(annihilator),
            "annihilator_is_orthogonal": residuals == [0] * generator_count,
            "alias_dimension_exceeds_rank": alias_count > rank,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "generator_count": generator_count,
                "alias_count": alias_count,
                "fiber_rank": rank,
                "annihilator_coefficients_ascending": annihilator,
                "orthogonality_residuals": residuals,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For h>0 and finitely many generators f_1,...,f_K in "
            "L2(R), the closed span of all lattice translates "
            "f_j(x-nh), n in Z, is a proper subspace of L2(R)."
        ),
        "proof": (
            "Under Fourier fiberization over a fundamental interval of "
            "length 2*pi/h, L2(R) becomes L2([0,2*pi/h),ell2(Z)). At "
            "almost every frequency, all lattice translates multiply each "
            "generator fiber by a scalar Fourier character. Their range "
            "therefore has dimension at most K, while the ambient fiber "
            "ell2(Z) has infinite dimension. A finite-generator lattice "
            "shift space cannot equal L2(R)."
        ),
        "finite_exact_model": (
            "For K generators on K+1 aliases, the K Vandermonde rows "
            "(1,j,...,j^K) are annihilated by the coefficient vector of "
            "prod_(j=1)^K (x-j)."
        ),
        "rows": rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is not used")
    count = 0
    while value % 2 == 0:
        count += 1
        value //= 2
    return count


def accelerated_collatz(value: int) -> tuple[int, int]:
    valuation = v2(3 * value + 1)
    return (3 * value + 1) >> valuation, valuation


def first_run_compensation(value: int) -> dict[str, int]:
    if value < 1 or value % 2 == 0:
        raise ValueError("a positive odd value is required")
    run_length = 0
    current = value
    while True:
        current, valuation = accelerated_collatz(current)
        if valuation >= 2:
            return {
                "run_length": run_length,
                "compensation_valuation": valuation,
                "block_image": current,
            }
        run_length += 1


def compensation_word_representative(
    run_length: int,
    compensation_valuation: int,
) -> int:
    if run_length < 0 or compensation_valuation < 2:
        raise ValueError("invalid run-compensation word")
    exponent = run_length + 1
    modulus = 1 << compensation_valuation
    inverse = pow(3**exponent, -1, 1 << (compensation_valuation - 1))
    candidates = [inverse, inverse + (1 << (compensation_valuation - 1))]
    quotient = next(
        candidate
        for candidate in candidates
        if (3**exponent * candidate - 1) % modulus != 0
    )
    return (1 << exponent) * quotient - 1


def collatz_compensation_audit(limit: int = 200_001) -> dict[str, object]:
    sample_count = 0
    good_count = 0
    formula_failures = 0
    descent_failures = 0
    sample_rows = []
    for value in range(3, limit + 1, 2):
        block = first_run_compensation(value)
        run_length = block["run_length"]
        compensation = block["compensation_valuation"]
        image = block["block_image"]
        formula_numerator = (
            3 ** (run_length + 1) * (value + 1)
            - 2 ** (run_length + 1)
        )
        formula_denominator = 2 ** (run_length + compensation)
        formula_ok = formula_numerator % formula_denominator == 0
        formula_ok = (
            formula_ok
            and formula_numerator // formula_denominator == image
        )
        formula_failures += int(not formula_ok)
        good = compensation >= run_length + 2
        if good:
            good_count += 1
            descent_failures += int(not image < value)
        sample_count += 1
        if len(sample_rows) < 20 and (
            good or compensation == 2
        ):
            sample_rows.append(
                {
                    "n": value,
                    "run_length": run_length,
                    "compensation_valuation": compensation,
                    "block_image": image,
                    "good_two_thirds_word": good,
                    "strict_descent": image < value,
                }
            )

    residual_rows = []
    residual_failures = 0
    for run_length in range(1, 13):
        value = compensation_word_representative(run_length, 2)
        block = first_run_compensation(value)
        checks = {
            "word_is_realized": (
                block["run_length"] == run_length
                and block["compensation_valuation"] == 2
            ),
            "outside_two_thirds_cover": 2 < run_length + 2,
            "first_compensation_does_not_descend": (
                block["block_image"] >= value
            ),
        }
        residual_failures += sum(not item for item in checks.values())
        residual_rows.append(
            {
                "run_length": run_length,
                "compensation_valuation": 2,
                "least_positive_representative": value,
                "block_image": block["block_image"],
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let r be the initial number of accelerated Collatz valuations "
            "equal to one and let b>=2 be the next valuation. If b>=r+2, "
            "then T^(r+1)(n)<n for every positive odd n>1 realizing that "
            "word. These words have exact relative odd-Haar mass 2/3."
        ),
        "exact_formula": (
            "Write n+1=2^(r+1)q with q odd. Then "
            "T^(r+1)(n)=(3^(r+1)q-1)/2^(b-1)."
        ),
        "descent_proof": (
            "The worst case is b=r+2. Descent reduces to "
            "q(4^(r+1)-3^(r+1))>2^(r+1)-1. For r>=1 this follows from "
            "4^m-3^m>=4^(m-1)>=2^m with m=r+1. For r=0 it is strict "
            "unless q=1, which is exactly n=1."
        ),
        "haar_mass_proof": (
            "The word 1^r,b has relative odd-Haar mass 2^(-(r+b)). "
            "Summing b>=r+2 and r>=0 gives "
            "sum_r 2^(-r)sum_(b>=r+2)2^(-b)=2/3."
        ),
        "exact_haar_mass": fraction_payload(Fraction(2, 3)),
        "finite_natural_audit": {
            "limit": limit,
            "odd_values_tested": sample_count,
            "good_cover_values": good_count,
            "formula_failure_count": formula_failures,
            "descent_failure_count": descent_failures,
            "sample_rows": sample_rows,
        },
        "residual_b_equals_two_rows": residual_rows,
        "failure_count": (
            formula_failures + descent_failures + residual_failures
        ),
    }


def dft(values: Sequence[float]) -> list[complex]:
    length = len(values)
    return [
        sum(
            value * cmath.exp(-2j * math.pi * frequency * index / length)
            for index, value in enumerate(values)
        )
        for frequency in range(length)
    ]


def quantize_phase(value: complex, sector_count: int) -> complex:
    if sector_count < 1:
        raise ValueError("positive sector count required")
    magnitude = abs(value)
    if magnitude == 0:
        return 0j
    angle = cmath.phase(value)
    sector = round(angle * sector_count / (2 * math.pi))
    quantized_angle = 2 * math.pi * sector / sector_count
    return magnitude * cmath.exp(1j * quantized_angle)


def direct_cyclic_convolution(values: Sequence[int], target: int) -> int:
    length = len(values)
    return sum(
        values[index] * values[(target - index) % length]
        for index in range(length)
    )


def phase_quantized_convolution(
    values: Sequence[int],
    target: int,
    sector_count: int,
) -> tuple[complex, complex]:
    length = len(values)
    spectrum = dft(values)
    endpoint_terms = [
        spectrum[frequency] ** 2
        * cmath.exp(2j * math.pi * frequency * target / length)
        for frequency in range(length)
    ]
    exact_fourier = sum(endpoint_terms) / length
    quantized = (
        sum(quantize_phase(value, sector_count) for value in endpoint_terms)
        / length
    )
    return exact_fourier, quantized


def prime_indicator(limit: int) -> list[int]:
    is_prime = [True] * limit
    if limit > 0:
        is_prime[0] = False
    if limit > 1:
        is_prime[1] = False
    for prime in range(2, math.isqrt(limit - 1) + 1):
        if not is_prime[prime]:
            continue
        for composite in range(prime * prime, limit, prime):
            is_prime[composite] = False
    return [int(value) for value in is_prime]


def goldbach_phase_quantization_audit() -> dict[str, object]:
    finite_rows = []
    failures = 0
    for length in [31, 61, 127]:
        values = prime_indicator(length)
        target = (length // 3) * 2
        direct = direct_cyclic_convolution(values, target)
        energy = sum(value * value for value in values)
        for sectors in [8, 16, 32, 64]:
            exact_fourier, quantized = phase_quantized_convolution(
                values,
                target,
                sectors,
            )
            actual_error = abs(exact_fourier - quantized)
            rational_bound = Fraction(22 * energy, 7 * sectors)
            checks = {
                "fourier_matches_direct_convolution": (
                    abs(exact_fourier.real - direct) < 1e-8
                    and abs(exact_fourier.imag) < 1e-8
                ),
                "quantization_error_within_rational_bound": (
                    actual_error <= float(rational_bound) + 1e-9
                ),
            }
            failures += sum(not value for value in checks.values())
            finite_rows.append(
                {
                    "cyclic_length": length,
                    "target": target,
                    "sector_count": sectors,
                    "direct_convolution": direct,
                    "energy": energy,
                    "actual_quantization_error": round(actual_error, 12),
                    "rational_energy_bound": fraction_payload(
                        rational_bound
                    ),
                    "checks": checks,
                }
            )

    scale_rows = []
    for exponent in range(3, 13):
        scale = 10**exponent
        logarithm = math.log(scale)
        sufficient_sectors = math.ceil(11 * logarithm**3 / 196)
        bound_ratio = (
            11 * logarithm**3 / (196 * sufficient_sectors)
        )
        fixed_64_ratio = 11 * logarithm**3 / (196 * 64)
        checks = {
            "sufficient_sector_formula_meets_k56": bound_ratio <= 1,
            "positive_sector_count": sufficient_sectors > 0,
        }
        failures += sum(not value for value in checks.values())
        scale_rows.append(
            {
                "N": scale,
                "sufficient_sector_count_crude_lambda_bound": (
                    sufficient_sectors
                ),
                "guarantee_to_K56_ratio": round(bound_ratio, 12),
                "fixed_64_sector_ratio": round(fixed_64_ratio, 12),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For the endpoint-aligned terms "
            "z_k=f_hat(k)^2 exp(2*pi*i*k*N/q), nearest M-sector phase "
            "quantization gives |c_N-c_N^(M)| <= "
            "22/(7M) sum_x |f(x)|^2."
        ),
        "proof": (
            "The angular error is at most pi/M, so each chord is at most "
            "pi|z_k|/M <=22|z_k|/(7M). Sum and use Parseval: "
            "q^(-1)sum_k|f_hat(k)|^2=sum_x|f(x)|^2."
        ),
        "lambda_corollary": (
            "For Lambda supported on [1,N], the elementary energy bound "
            "sum Lambda(n)^2<=N log(N)^2 makes the quantization error at "
            "most 22N log(N)^2/(7M). To fit 56N/log(N), it suffices that "
            "M>=ceil(11 log(N)^3/196)."
        ),
        "fixed_resolution_no_go": (
            "For fixed M, this Parseval-only guarantee divided by the K56 "
            "budget is 11 log(N)^3/(196M), which diverges. This refutes "
            "fixed phase resolution only for this uniform energy route; it "
            "does not refute arithmetic cancellation of the actual Lambda "
            "phases."
        ),
        "finite_prime_indicator_rows": finite_rows,
        "scale_rows": scale_rows,
        "failure_count": failures,
    }


def path_ledger(signs: Sequence[int]) -> dict[str, int]:
    if len(signs) < 2 or any(sign not in {-1, 1} for sign in signs):
        raise ValueError("a path with +/-1 labels is required")
    edge_count = len(signs) - 1
    a10 = sum(signs[:-1])
    a01 = sum(signs[1:])
    a11 = sum(
        signs[index] * signs[index + 1]
        for index in range(edge_count)
    )
    negative_negative = sum(
        signs[index] == -1 and signs[index + 1] == -1
        for index in range(edge_count)
    )
    cut_count = sum(
        signs[index] != signs[index + 1]
        for index in range(edge_count)
    )
    return {
        "A00": edge_count,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "negative_negative_edges": negative_negative,
        "cut_count": cut_count,
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin_path_cut_audit() -> dict[str, object]:
    counter_rows = []
    failures = 0
    for multiplier in range(1, 17):
        vertex_count = 4 * multiplier
        alternating = [
            1 if index % 2 == 0 else -1
            for index in range(vertex_count)
        ]
        block = [1] * (2 * multiplier) + [-1] * (2 * multiplier)
        alternating_ledger = path_ledger(alternating)
        block_ledger = path_ledger(block)
        checks = {
            "same_unsigned_path": (
                alternating_ledger["A00"] == block_ledger["A00"]
            ),
            "same_left_marginal": (
                alternating_ledger["A10"] == block_ledger["A10"] == 1
            ),
            "same_right_marginal": (
                alternating_ledger["A01"] == block_ledger["A01"] == -1
            ),
            "alternating_joint_is_negative_extreme": (
                alternating_ledger["A11"] == -(vertex_count - 1)
            ),
            "block_joint_is_positive_extreme": (
                block_ledger["A11"] == vertex_count - 3
            ),
            "twin_cells_differ": (
                alternating_ledger["negative_negative_edges"] == 0
                and block_ledger["negative_negative_edges"]
                == 2 * multiplier - 1
            ),
            "cut_identity_both": (
                alternating_ledger["A11"]
                == alternating_ledger["A00"]
                - 2 * alternating_ledger["cut_count"]
                and block_ledger["A11"]
                == block_ledger["A00"] - 2 * block_ledger["cut_count"]
            ),
        }
        failures += sum(not value for value in checks.values())
        counter_rows.append(
            {
                "vertex_count": vertex_count,
                "alternating_ledger": alternating_ledger,
                "single_block_ledger": block_ledger,
                "checks": checks,
            }
        )

    source_path = (
        ROOT
        / "data/open-problem/twin-prime/"
        "tp-ticket-142-liouville-projector.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_rows = source["result"]["liouville_ledger_audit"]["rows"]
    arithmetic_rows = []
    for row in source_rows:
        edge_count = int(row["A00"])
        joint = int(row["A11"])
        cut_numerator = edge_count - joint
        checks = {
            "cut_count_is_integral": cut_numerator % 2 == 0,
            "cut_count_is_nonnegative": cut_numerator >= 0,
            "cut_count_at_most_edges": cut_numerator <= 2 * edge_count,
        }
        failures += sum(not value for value in checks.values())
        cut_count = cut_numerator // 2
        arithmetic_rows.append(
            {
                "X": int(row["X"]),
                "edge_count_A00": edge_count,
                "joint_A11": joint,
                "liouville_sign_switch_edges": cut_count,
                "switch_ratio": round(cut_count / edge_count, 12),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Every finite gap-two support graph is a disjoint union of "
            "paths. For a +/-1 labeling, A11=|E|-2*Cut. The unsigned graph "
            "and both directed endpoint marginals do not determine A11 or "
            "the negative-negative edge count."
        ),
        "counterfamily": (
            "On P_(4m), alternating signs and one block of 2m plus signs "
            "followed by 2m minus signs both have "
            "(A00,A10,A01)=(4m-1,1,-1). Their A11 values are -(4m-1) and "
            "4m-3, while their negative-negative edge counts are 0 and "
            "2m-1."
        ),
        "support_only_no_go": (
            "The alternating labeling attains A11=-A00 on the same path "
            "geometry. Therefore no lower bound A11>=-gamma*A00 with "
            "gamma<1 can follow from unsigned gap-two support topology "
            "alone. Arithmetic information about the actual Liouville "
            "labels is indispensable."
        ),
        "counterfamily_rows": counter_rows,
        "finite_cubic_rough_rows": arithmetic_rows,
        "source_artifact": str(source_path.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "source_sha256": file_sha256(source_path),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_fiber_audit()
    collatz = collatz_compensation_audit()
    goldbach = goldbach_phase_quantization_audit()
    twin_prime = twin_path_cut_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )

    riemann_next = (
        "InfiniteMultiscaleWeilFiberCompletenessAndMatrixSchurBound"
    )
    collatz_next = (
        "ResidualThirdIteratedRunCompensationRenewalDescent"
    )
    goldbach_next = "ArithmeticPhaseSectorImbalanceBoundSummableK56"
    twin_next = "CubicRoughLiouvillePathSwitchDeficitTypeIIBound"

    return {
        "theorem_name": "FourConjectureFiberCompensationPhaseGraphAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET147 proves four exact intermediate results. It supplies "
            "no proof or counterexample to any target conjecture. The RH "
            "theorem is an L2 lattice-shift completeness obstruction, the "
            "Collatz theorem covers an exact two-thirds cylinder family "
            "but leaves a residual third, the Goldbach theorem controls "
            "phase discretization error but not arithmetic sector "
            "imbalance, and the Twin theorem proves a support-topology "
            "no-go rather than an actual Liouville correlation estimate."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-147",
            "theorem_name": (
                "FiniteGeneratorLatticeShiftFiberIncompleteness"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The theorem concerns L2 completeness. It does not prove "
                "that the exact Weil test topology is L2, does not bound "
                "any actual Weil reflection coefficient, and does not "
                "exclude a determining family obtained from infinitely "
                "many scales or non-lattice translations."
            ),
            "route_decision": {
                "discard": (
                    "promoting positivity on finitely many lattice-shift "
                    "generator orbits to full L2 test-space positivity"
                ),
                "retain": (
                    "an infinite multiscale or continuum-shift core with a "
                    "proved test-space completeness theorem and matrix "
                    "Schur bounds for its actual Weil moments"
                ),
                "next_theorem": riemann_next,
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteLatticeShiftCoreIsComplete",
                "FiniteGeneratorLatticeShiftFiberIncompleteness",
                riemann_next,
            ),
            "claim_boundary": (
                "No RH proof or zeta-zero counterexample. An exact "
                "finite-generator L2 completeness no-go only."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-147",
            "theorem_name": (
                "FirstRunCompensationTwoThirdsPointwiseDescentCover"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": (
                collatz["exact_formula"]
                + " "
                + collatz["descent_proof"]
                + " "
                + collatz["haar_mass_proof"]
            ),
            "reproducible_computation": collatz,
            "logical_limit": (
                "The exact pointwise theorem leaves a one-third Haar family "
                "of first-compensation words, including infinitely many "
                "positive b=2 cylinders. Haar mass is not an all-integer "
                "quantifier, and no renewal theorem for the residual family "
                "is proved."
            ),
            "route_decision": {
                "discard": (
                    "treating the first two-thirds block cover or its Haar "
                    "mass as a proof for every positive integer"
                ),
                "retain": (
                    "iterate the run-compensation decomposition on the "
                    "residual third and prove a pointwise renewal descent "
                    "cover without invoking observed stopping time"
                ),
                "next_theorem": collatz_next,
            },
            "proof_dag": proof_dag(
                "CO",
                "FirstCompensationCoversEveryNaturalCode",
                "FirstRunCompensationTwoThirdsPointwiseDescentCover",
                collatz_next,
            ),
            "claim_boundary": (
                "No Collatz proof or divergent orbit. An infinite "
                "pointwise descent family of exact Haar mass two-thirds "
                "plus an explicit residual family only."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-147",
            "theorem_name": (
                "EndpointPhaseQuantizationEnergyBoundAndFixedResolutionNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": (
                goldbach["proof"] + " " + goldbach["lambda_corollary"]
            ),
            "reproducible_computation": goldbach,
            "logical_limit": (
                "Phase quantization only approximates the exact endpoint "
                "convolution. The theorem does not bound the signed "
                "imbalance among quantized Lambda phase sectors, major/minor "
                "arc errors, or the full binary Goldbach residual."
            ),
            "route_decision": {
                "discard": (
                    "fixed endpoint-phase resolution combined only with "
                    "Parseval energy as a scale-uniform K56 certificate"
                ),
                "retain": (
                    "growing phase sectors together with arithmetic "
                    "major/minor-arc bounds for the signed sector imbalance"
                ),
                "next_theorem": goldbach_next,
            },
            "proof_dag": proof_dag(
                "GB",
                "FixedResolutionParsevalPhaseEnvelopeK56",
                (
                    "EndpointPhaseQuantizationEnergyBoundAnd"
                    "FixedResolutionNoGo"
                ),
                goldbach_next,
            ),
            "claim_boundary": (
                "No Goldbach proof or Goldbach counterexample. Exact phase "
                "discretization control and a limitation of one energy-only "
                "certification route."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-147",
            "theorem_name": (
                "GapTwoPathCutMarginalNoGoAndArithmeticLabelReduction"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": (
                twin_prime["counterfamily"]
                + " "
                + twin_prime["support_only_no_go"]
            ),
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The counterfamily uses abstract +/-1 labels on an exact "
                "gap-two path, not alternative values of the Liouville "
                "function. The finite cubic-rough rows do not prove a "
                "uniform switch deficit or Type II estimate."
            ),
            "route_decision": {
                "discard": (
                    "deriving a joint A11 margin from unsigned gap-two "
                    "support topology and endpoint marginals alone"
                ),
                "retain": (
                    "prove an arithmetic upper bound on actual cubic-rough "
                    "Liouville sign switches together with the one-sided "
                    "marginal budget"
                ),
                "next_theorem": twin_next,
            },
            "proof_dag": proof_dag(
                "TP",
                "UnsignedPathTopologyAndMarginalsControlJointParity",
                "GapTwoPathCutMarginalNoGoAndArithmeticLabelReduction",
                twin_next,
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. Exact path-cut "
                "identity, an infinite abstract-label no-go family, and an "
                "arithmetic next target only."
            ),
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
    attempts = []
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
                        "fiber_compensation_phase_graph_audit."
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
        "fiber_compensation_phase_graph_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket147-fiber-compensation-phase-graph.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-147-finite-shift-fiber-no-go.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-147-run-compensation-cover.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-147-phase-quantization.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-147-path-cut-no-go.json"
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
