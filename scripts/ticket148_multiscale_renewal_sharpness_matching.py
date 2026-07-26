from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-07-27T15:00:00+09:00"
SCHEMA = "primeproject.ticket148-multiscale-renewal-sharpness-matching.v1"
STATUS = (
    "exact_partial_theorems_route_no_go_and_geometry_correction_"
    "all_conjectures_open"
)


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T148-REJECTED"
    closed_id = f"{problem_code}-T148-CLOSED"
    open_id = f"{problem_code}-T148-OPEN"
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
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor == 0:
                continue
            matrix[row] = [
                matrix[row][index] - factor * matrix[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def discrete_haar_rows(level: int) -> list[list[int]]:
    if level < 0:
        raise ValueError("level must be nonnegative")
    dimension = 2**level
    rows = [[1] * dimension]
    for scale in range(level):
        block_count = 2**scale
        block_size = dimension // block_count
        half = block_size // 2
        for block in range(block_count):
            row = [0] * dimension
            start = block * block_size
            row[start : start + half] = [1] * half
            row[start + half : start + block_size] = [-1] * half
            rows.append(row)
    return rows


def riemann_haar_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for level in range(1, 9):
        matrix = discrete_haar_rows(level)
        dimension = 2**level
        off_diagonal_max = max(
            abs(sum(a * b for a, b in zip(matrix[i], matrix[j])))
            for i in range(dimension)
            for j in range(i)
        )
        norms = [sum(value * value for value in row) for row in matrix]
        rank = exact_matrix_rank(matrix)
        prefix_size = min(8, dimension - 1)
        diagonal = [1] * dimension
        diagonal[prefix_size] = -1
        checks = {
            "row_count_equals_dimension": len(matrix) == dimension,
            "exact_full_rank": rank == dimension,
            "pairwise_orthogonal": off_diagonal_max == 0,
            "positive_row_norms": min(norms) > 0,
            "finite_prefix_positive": min(diagonal[:prefix_size]) > 0,
            "hidden_next_direction_negative": diagonal[prefix_size] < 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "level": level,
                "dimension": dimension,
                "row_count": len(matrix),
                "exact_rank": rank,
                "off_diagonal_dot_product_max": off_diagonal_max,
                "row_norm_min": min(norms),
                "row_norm_max": max(norms),
                "positive_prefix_size": prefix_size,
                "first_negative_basis_index_zero_based": prefix_size,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "The unit-interval translates together with all dyadic Haar "
            "wavelets form a complete orthonormal basis of L2(R). "
            "Nevertheless, for every N there is a bounded self-adjoint "
            "operator diagonal in that basis whose first N tested "
            "directions are positive and whose (N+1)-st direction is "
            "negative."
        ),
        "completeness_proof": (
            "On each unit interval, dyadic conditional expectations "
            "converge in L2 to the function. Their successive differences "
            "are exactly the Haar detail spaces. Truncating first to "
            "finitely many unit intervals and then refining the dyadic "
            "partition proves density; orthogonality gives an orthonormal "
            "basis after normalization."
        ),
        "finite_positivity_no_go_proof": (
            "Enumerate the complete basis as e_1,e_2,... and define "
            "A_N e_j=e_j except A_N e_(N+1)=-e_(N+1). Then A_N is bounded "
            "and self-adjoint. Its quadratic form is positive on each of "
            "e_1,...,e_N but is -1 on e_(N+1). Completeness therefore does "
            "not turn any finite prefix positivity audit into global "
            "positivity."
        ),
        "finite_exact_rows": rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is undefined")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def accelerated_collatz(value: int) -> tuple[int, int]:
    if value <= 0 or value % 2 == 0:
        raise ValueError("accelerated Collatz input must be a positive odd")
    valuation = v2(3 * value + 1)
    return (3 * value + 1) // (2**valuation), valuation


def collatz_minus_five_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for pair_count in range(1, 17):
        modulus = 2 ** (3 * pair_count + 1)
        representative = modulus - 5
        expected_image = 2 * (9**pair_count) - 5
        current = representative
        valuations = []
        for _ in range(2 * pair_count):
            current, valuation = accelerated_collatz(current)
            valuations.append(valuation)

        lift_rows = []
        for lift in [0, 1, 2, 7]:
            lifted_input = representative + modulus * lift
            lifted = lifted_input
            lifted_valuations = []
            for _ in range(2 * pair_count):
                lifted, valuation = accelerated_collatz(lifted)
                lifted_valuations.append(valuation)
            lifted_expected = (
                expected_image + 2 * (9**pair_count) * lift
            )
            lift_rows.append(
                {
                    "lift": lift,
                    "input": lifted_input,
                    "image": lifted,
                    "expected_image": lifted_expected,
                    "valuation_word_matches": (
                        lifted_valuations == [1, 2] * pair_count
                    ),
                    "formula_matches": lifted == lifted_expected,
                    "strictly_expands": lifted > lifted_input,
                }
            )

        checks = {
            "valuation_word_is_repeated_1_2": (
                valuations == [1, 2] * pair_count
            ),
            "representative_formula_matches": current == expected_image,
            "representative_strictly_expands": current > representative,
            "all_sampled_lifts_match": all(
                row["formula_matches"] for row in lift_rows
            ),
            "all_sampled_lifts_expand": all(
                row["strictly_expands"] for row in lift_rows
            ),
        }
        failures += sum(not value for value in checks.values())
        failures += sum(
            not row["valuation_word_matches"] for row in lift_rows
        )
        rows.append(
            {
                "renewal_pair_count": pair_count,
                "residue_modulus": modulus,
                "least_positive_representative": representative,
                "valuation_word": valuations,
                "image_after_pairs": current,
                "expected_image": expected_image,
                "expansion": current - representative,
                "odd_haar_mass": {
                    "exact": f"1/{2 ** (3 * pair_count)}",
                    "decimal": 2.0 ** (-3 * pair_count),
                },
                "sample_lifts": lift_rows,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For every L>=1, n_L=2^(3L+1)-5 has first 2L accelerated "
            "Collatz valuations (1,2)^L and "
            "T^(2L)(n_L)=2*9^L-5>n_L. More strongly, every nonnegative "
            "lift n_L+2^(3L+1)t has the same valuation word and maps to "
            "2*9^L(1+t)-5, which is larger than its input."
        ),
        "proof": (
            "For r>=1 and integer c>=1, x=2*c*8^r-5 satisfies "
            "v2(3x+1)=1 and its first accelerated image is 3*c*8^r-7. "
            "The next valuation is exactly 2 and the second image is "
            "2*(9c)*8^(r-1)-5. Iterating L pairs from c=1+t,r=L gives "
            "the formula. Strict expansion follows from 9^L>8^L."
        ),
        "cylinder_measure": (
            "The exact residue class modulo 2^(3L+1) has Haar mass "
            "2^(-3L) relative to odd 2-adic integers."
        ),
        "finite_exact_rows": rows,
        "failure_count": failures,
    }


def direct_cyclic_convolution(values: Sequence[float], target: int) -> float:
    length = len(values)
    return sum(
        values[index] * values[(target - index) % length]
        for index in range(length)
    )


def goldbach_phase_rate_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for sector_count in [4, 8, 16, 32, 64, 128]:
        modulus = 4 * sector_count**2
        endpoint = sector_count**2 + 2 * sector_count - 1
        theta = 2 * math.pi * endpoint / modulus
        delta = math.pi / sector_count - math.pi / (
            2 * sector_count**2
        )
        values = [
            1 + math.cos(2 * math.pi * index / modulus)
            for index in range(modulus)
        ]
        direct = direct_cyclic_convolution(values, endpoint)
        exact_formula = modulus + (modulus / 2) * math.cos(theta)
        quantized = float(modulus)
        error = abs(direct - quantized)
        expected_error = (modulus / 2) * math.sin(delta)
        energy = sum(value * value for value in values)
        expected_energy = 3 * modulus / 2
        relative_error = error / energy
        scaled_relative_error = sector_count * relative_error
        checks = {
            "function_is_nonnegative": min(values) >= -1e-12,
            "endpoint_phase_identity": abs(
                theta - (math.pi / 2 + delta)
            )
            <= 1e-12,
            "nearest_sector_is_pi_over_two": delta < (
                math.pi / sector_count
            ),
            "direct_convolution_matches_formula": abs(
                direct - exact_formula
            )
            <= 1e-9 * modulus,
            "error_formula_matches": abs(error - expected_error)
            <= 1e-9 * modulus,
            "parseval_energy_matches": abs(energy - expected_energy)
            <= 1e-9 * modulus,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "sector_count_M": sector_count,
                "modulus_q": modulus,
                "endpoint_N": endpoint,
                "endpoint_phase": theta,
                "phase_offset_delta": delta,
                "direct_convolution": direct,
                "quantized_convolution": quantized,
                "absolute_error": error,
                "expected_error": expected_error,
                "energy": energy,
                "relative_error_error_over_energy": relative_error,
                "scaled_relative_error_M_times_error_over_energy": (
                    scaled_relative_error
                ),
                "limit_target_pi_over_three": math.pi / 3,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "The O(E/M) endpoint-phase quantization rate from TICKET-147 "
            "is order-sharp even for nonnegative real functions. For every "
            "M divisible by 4, let q=4M^2, N=M^2+2M-1, and "
            "f(x)=1+cos(2*pi*x/q) on Z/qZ. Nearest M-sector phase "
            "quantization has error (q/2)sin(pi/M-pi/(2M^2)); with "
            "E=sum f^2=3q/2, M*error/E tends to pi/3."
        ),
        "proof": (
            "The unnormalized Fourier transform of f is supported at "
            "0,+1,-1 with coefficients q,q/2,q/2. The exact endpoint "
            "convolution is q+(q/2)cos(2*pi*N/q). The endpoint phase is "
            "pi/2+delta, delta=pi/M-pi/(2M^2), while nearest-sector "
            "quantization replaces the +/-1 phases by +/-pi/2, canceling "
            "their pair. Hence the stated error is exact. Parseval gives "
            "E=3q/2, and M sin(delta)/3 tends to pi/3."
        ),
        "finite_numeric_rows": rows,
        "failure_count": failures,
    }


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if spf[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if spf[multiple] == multiple:
                spf[multiple] = prime
    return spf


def cubic_rough_edges(scale: int) -> list[tuple[int, int]]:
    limit = 2 * scale + 2
    spf = smallest_prime_factors(limit)
    threshold = 2 * scale + 2
    return [
        (value, value + 2)
        for value in range(scale, 2 * scale + 1)
        if spf[value] ** 3 > threshold
        and spf[value + 2] ** 3 > threshold
    ]


def matching_ledger(cell_counts: dict[str, int]) -> dict[str, int]:
    n_pp = cell_counts["++"]
    n_pm = cell_counts["+-"]
    n_mp = cell_counts["-+"]
    n_mm = cell_counts["--"]
    return {
        "A00": n_pp + n_pm + n_mp + n_mm,
        "A10": n_pp + n_pm - n_mp - n_mm,
        "A01": n_pp - n_pm + n_mp - n_mm,
        "A11": n_pp - n_pm - n_mp + n_mm,
        "negative_negative_edges": n_mm,
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin_matching_audit() -> dict[str, object]:
    failures = 0
    graph_rows = []
    for scale in [13, 100, 1_000, 10_000, 100_000]:
        edges = cubic_rough_edges(scale)
        degrees: dict[int, int] = {}
        for left, right in edges:
            degrees[left] = degrees.get(left, 0) + 1
            degrees[right] = degrees.get(right, 0) + 1
        max_degree = max(degrees.values(), default=0)
        checks = {
            "support_is_matching": max_degree <= 1,
            "edge_endpoints_in_range": all(
                scale <= left <= 2 * scale
                and right == left + 2
                and right <= 2 * scale + 2
                for left, right in edges
            ),
        }
        failures += sum(not value for value in checks.values())
        graph_rows.append(
            {
                "X": scale,
                "edge_count": len(edges),
                "vertex_count": len(degrees),
                "maximum_degree": max_degree,
                "checks": checks,
            }
        )

    counter_rows = []
    for multiplier in range(1, 17):
        correlated_cells = {
            "++": 2 * multiplier,
            "+-": 0,
            "-+": 0,
            "--": 2 * multiplier,
        }
        anticorrelated_cells = {
            "++": 0,
            "+-": 2 * multiplier,
            "-+": 2 * multiplier,
            "--": 0,
        }
        correlated = matching_ledger(correlated_cells)
        anticorrelated = matching_ledger(anticorrelated_cells)
        checks = {
            "same_edge_count": correlated["A00"] == anticorrelated["A00"],
            "same_left_marginal": correlated["A10"] == anticorrelated["A10"],
            "same_right_marginal": correlated["A01"] == anticorrelated["A01"],
            "opposite_joint_extremes": (
                correlated["A11"] == 4 * multiplier
                and anticorrelated["A11"] == -4 * multiplier
            ),
            "negative_negative_cells_differ": (
                correlated["negative_negative_edges"] == 2 * multiplier
                and anticorrelated["negative_negative_edges"] == 0
            ),
        }
        failures += sum(not value for value in checks.values())
        counter_rows.append(
            {
                "edge_count": 4 * multiplier,
                "correlated_ledger": correlated,
                "anticorrelated_ledger": anticorrelated,
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
        a00 = int(row["A00"])
        a10 = int(row["A10"])
        a01 = int(row["A01"])
        a11 = int(row["A11"])
        numerators = {
            "++": a00 + a10 + a01 + a11,
            "+-": a00 + a10 - a01 - a11,
            "-+": a00 - a10 + a01 - a11,
            "--": a00 - a10 - a01 + a11,
        }
        cells = {
            label: numerator // 4
            for label, numerator in numerators.items()
        }
        checks = {
            "all_cell_numerators_divisible_by_four": all(
                numerator % 4 == 0 for numerator in numerators.values()
            ),
            "all_cells_nonnegative": min(cells.values()) >= 0,
            "cells_sum_to_edge_count": sum(cells.values()) == a00,
            "negative_negative_matches_direct_twins": (
                cells["--"] == int(row["direct_twin_count"])
            ),
            "ledger_reconstruction_matches": matching_ledger(cells)
            == {
                "A00": a00,
                "A10": a10,
                "A01": a01,
                "A11": a11,
                "negative_negative_edges": cells["--"],
            },
        }
        failures += sum(not value for value in checks.values())
        arithmetic_rows.append(
            {
                "X": int(row["X"]),
                "ledger": {
                    "A00": a00,
                    "A10": a10,
                    "A01": a01,
                    "A11": a11,
                },
                "exact_cell_counts": cells,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For X>=13, the cubic-rough gap-two support defined by "
            "spf(n)^3>2X+2 and spf(n+2)^3>2X+2 is a matching. No two "
            "admitted edges share a vertex. On a matching, however, A00 "
            "and the two endpoint marginals A10,A01 still do not determine "
            "the joint A11 or the -- cell count."
        ),
        "matching_proof": (
            "If edges (n,n+2) and (n+2,n+4) were both admitted, all three "
            "numbers would have smallest prime factor greater than 3, "
            "because 3^3=27<=2X+2. But one of three consecutive odd "
            "numbers spaced by two is divisible by 3. This contradiction "
            "shows that the maximum degree is one."
        ),
        "coupling_no_go": (
            "On 4m disjoint edges, use 2m ++ and 2m -- labels, or instead "
            "2m +- and 2m -+ labels. Both assignments have "
            "(A00,A10,A01)=(4m,0,0), but A11 is +4m versus -4m and the -- "
            "count is 2m versus 0. The missing object is endpoint coupling, "
            "not long-path geometry."
        ),
        "correction_to_ticket147": (
            "TICKET-147's path-cut identity remains true for arbitrary "
            "gap-two graphs, but its long-path counterfamily cannot occur "
            "inside the actual TICKET-142 cubic-rough support when X>=13. "
            "This ticket replaces that application with the exact matching "
            "coupling no-go."
        ),
        "finite_graph_rows": graph_rows,
        "matching_counterfamily_rows": counter_rows,
        "finite_cubic_rough_cell_rows": arithmetic_rows,
        "source_artifact": str(source_path.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "source_sha256": file_sha256(source_path),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_haar_audit()
    collatz = collatz_minus_five_audit()
    goldbach = goldbach_phase_rate_audit()
    twin_prime = twin_matching_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )

    riemann_next = "SmoothWeilWaveletCoreAndUniformMatrixTailPositivityBound"
    collatz_next = "AdaptiveRenewalRankEscapingMinusFiveTwoAdicShadow"
    goldbach_next = (
        "VonMangoldtEndpointSectorCancellationBeyondSharpGeometricRate"
    )
    twin_next = "CubicRoughLiouvilleMatchingCouplingTypeIIBound"

    return {
        "theorem_name": "FourConjectureMultiscaleRenewalSharpnessMatchingAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-148 proves four exact intermediate results and resolves "
            "no target conjecture. It closes an L2 multiscale completeness "
            "subproblem while refuting finite-prefix positivity promotion; "
            "constructs an expanding Collatz cylinder for every fixed "
            "renewal horizon; proves generic endpoint-phase quantization "
            "cannot beat order 1/M; and corrects the cubic-rough support "
            "from a path model to a matching while preserving a coupling "
            "no-go."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-148",
            "theorem_name": (
                "DyadicHaarMultiscaleCompletenessAndFiniteScalePositivityNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": (
                riemann["completeness_proof"]
                + " "
                + riemann["finite_positivity_no_go_proof"]
            ),
            "reproducible_computation": riemann,
            "logical_limit": (
                "The Haar theorem is for L2(R), whereas the exact Weil "
                "criterion uses a specific smooth test space and quadratic "
                "form. Haar wavelets are discontinuous, and the synthetic "
                "diagonal operator is not the Weil operator. No actual "
                "zeta-zero or Weil-matrix tail is controlled."
            ),
            "route_decision": {
                "discard": (
                    "complete multiscale coordinates plus positivity on "
                    "any finite prefix as a global positivity certificate"
                ),
                "retain": (
                    "construct a smooth wavelet core inside the exact Weil "
                    "test topology and prove a uniform positive tail bound "
                    "for the actual Weil matrix"
                ),
                "next_theorem": riemann_next,
            },
            "proof_dag": proof_dag(
                "RH",
                "FinitePrefixPositivityPromotesOnCompleteCoordinates",
                (
                    "DyadicHaarMultiscaleCompletenessAnd"
                    "FiniteScalePositivityNoGo"
                ),
                riemann_next,
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact L2 "
                "completeness theorem and one operator-theoretic no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-148",
            "theorem_name": "MinusFiveCylinderNoFixedRenewalHorizon",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Each cylinder is sparse and finite-horizon expansion does "
                "not imply a divergent positive orbit. The construction "
                "shadows the known negative 2-adic cycle -5,-7 and only "
                "rules out a universal fixed renewal depth; adaptive or "
                "unbounded descent remains possible."
            ),
            "route_decision": {
                "discard": (
                    "any proof claiming that a fixed number of repeated "
                    "renewal blocks forces descent for every positive odd "
                    "integer"
                ),
                "retain": (
                    "build an adaptive renewal rank that detects escape "
                    "from arbitrarily long finite shadows of the -5,-7 "
                    "2-adic cycle"
                ),
                "next_theorem": collatz_next,
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedRenewalHorizonForcesUniversalDescent",
                "MinusFiveCylinderNoFixedRenewalHorizon",
                collatz_next,
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent positive orbit. An "
                "infinite exact family defeating every fixed horizon."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-148",
            "theorem_name": (
                "NonnegativeEndpointPhaseQuantizationOrderSharpness"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The sharp example is a nonnegative trigonometric function, "
                "not the von Mangoldt function. It proves a generic "
                "geometric lower barrier only and does not exclude "
                "arithmetic phase cancellation, major/minor-arc bounds, or "
                "a Goldbach representation theorem."
            ),
            "route_decision": {
                "discard": (
                    "improving the TICKET-147 phase error to o(E/M) using "
                    "only nonnegativity, reality, conjugate symmetry, and "
                    "Parseval energy"
                ),
                "retain": (
                    "prove von Mangoldt-specific endpoint sector "
                    "cancellation beyond the now sharp generic 1/M rate"
                ),
                "next_theorem": goldbach_next,
            },
            "proof_dag": proof_dag(
                "GB",
                "GenericNonnegativePhaseQuantizationIsLittleOEnergyOverM",
                "NonnegativeEndpointPhaseQuantizationOrderSharpness",
                goldbach_next,
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "order-sharpness theorem for a generic analytic route."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-148",
            "theorem_name": "CubicRoughGapTwoMatchingAndCouplingNoGo",
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": (
                twin_prime["matching_proof"]
                + " "
                + twin_prime["coupling_no_go"]
            ),
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The matching counterfamily uses abstract signs, not the "
                "actual Liouville function. Exact finite cell inversion "
                "does not prove a uniform arithmetic coupling estimate, a "
                "Type II bound, or infinitely many twin primes."
            ),
            "route_decision": {
                "discard": (
                    "the TICKET-147 long-path switch-deficit target on the "
                    "actual cubic-rough support, and any inference of joint "
                    "parity from matching topology plus marginals"
                ),
                "retain": (
                    "estimate the actual Liouville endpoint coupling across "
                    "the cubic-rough matching by a Type II bilinear bound"
                ),
                "next_theorem": twin_next,
            },
            "proof_dag": proof_dag(
                "TP",
                "CubicRoughLongPathSwitchDeficitOrMarginalClosure",
                "CubicRoughGapTwoMatchingAndCouplingNoGo",
                twin_next,
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. One exact support "
                "geometry correction and one matching-coupling no-go."
            ),
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "historical_correction_count": 1,
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
                        "multiscale_renewal_sharpness_matching_audit."
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
        "multiscale_renewal_sharpness_matching_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket148-multiscale-renewal-sharpness-matching.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-148-haar-multiscale-no-go.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-148-minus-five-renewal-no-go.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-148-phase-rate-sharpness.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-148-matching-coupling-correction.json"
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
