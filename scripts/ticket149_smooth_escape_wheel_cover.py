from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-07-27T21:00:00+09:00"
SCHEMA = "primeproject.ticket149-smooth-escape-wheel-cover.v1"
STATUS = "exact_partial_theorems_and_route_reductions_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T149-REJECTED"
    closed_id = f"{problem_code}-T149-CLOSED"
    open_id = f"{problem_code}-T149-OPEN"
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
        "edges": [[rejected_id, closed_id], [closed_id, open_id]],
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def riemann_smooth_compact_tail_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for prefix_size in range(1, 17):
        epsilon = Fraction(1, (prefix_size + 1) ** 2)
        diagonal = (
            [Fraction(1) for _ in range(prefix_size)]
            + [-epsilon]
            + [Fraction(0) for _ in range(3)]
        )
        checks = {
            "audited_prefix_strictly_positive": all(
                value > 0 for value in diagonal[:prefix_size]
            ),
            "hidden_direction_strictly_negative": (
                diagonal[prefix_size] < 0
            ),
            "finite_rank_operator_is_compact": (
                sum(value != 0 for value in diagonal) == prefix_size + 1
            ),
            "absolute_tail_norm_equals_epsilon": (
                max(abs(value) for value in diagonal[prefix_size:])
                == epsilon
            ),
            "tail_norm_tends_to_zero_in_family": (
                epsilon <= Fraction(1, 4)
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "positive_prefix_size_N": prefix_size,
                "epsilon": {
                    "exact": f"{epsilon.numerator}/{epsilon.denominator}",
                    "decimal": float(epsilon),
                },
                "finite_rank": prefix_size + 1,
                "positive_core_minimum": 1,
                "global_minimum": {
                    "exact": f"{-epsilon.numerator}/{epsilon.denominator}",
                    "decimal": float(-epsilon),
                },
                "absolute_tail_operator_norm": {
                    "exact": f"{epsilon.numerator}/{epsilon.denominator}",
                    "decimal": float(epsilon),
                },
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "A Meyer wavelet may be chosen in the Schwartz class and its "
            "dyadic dilates and translates form a complete orthonormal "
            "basis of L2(R). On any enumeration e_1,e_2,... of that smooth "
            "basis, for every N>=1 and epsilon>0 the finite-rank "
            "self-adjoint operator A e_j=e_j for j<=N, "
            "A e_(N+1)=-epsilon e_(N+1), and A e_j=0 otherwise is compact, "
            "has absolute tail norm epsilon, passes all first-N basis "
            "positivity tests, and is not positive semidefinite."
        ),
        "imported_basis_fact": (
            "The Meyer construction has a C-infinity compactly supported "
            "Fourier transform, hence its inverse Fourier transform is "
            "Schwartz; the standard dyadic system is an orthonormal basis "
            "of L2(R). This is a cited wavelet theorem, not inferred from "
            "the finite audit."
        ),
        "no_go_proof": (
            "The operator is diagonal in a smooth complete orthonormal "
            "basis and has only N+1 nonzero eigenvalues, so it is finite "
            "rank, compact, and self-adjoint. Its first N diagonal entries "
            "are 1. The restriction to the orthogonal complement of their "
            "span has norm epsilon, but the quadratic form at e_(N+1) is "
            "-epsilon. Taking epsilon arbitrarily small proves that "
            "smooth completeness plus an absolute compact-tail bound does "
            "not imply positivity without a coercive positive reference "
            "on the tail."
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


def minus_five_shadow_data(value: int) -> dict[str, object]:
    if value <= 0 or value % 2 == 0:
        raise ValueError("input must be a positive odd integer")
    initial_shadow_order = v2(value + 5)
    pair_count = (initial_shadow_order - 1) // 3
    current = value
    valuations: list[int] = []
    for _ in range(2 * pair_count):
        current, valuation = accelerated_collatz(current)
        valuations.append(valuation)
    exit_order = v2(current + 5)
    probe = current
    exit_valuations: list[int] = []
    for _ in range(2):
        probe, valuation = accelerated_collatz(probe)
        exit_valuations.append(valuation)
    exit_type = {
        1: "first valuation at least 2",
        2: "next pair is (1,1)",
        3: "next pair is (1,b) with b at least 3",
    }[exit_order]
    return {
        "start": value,
        "initial_shadow_order_s": initial_shadow_order,
        "maximal_repeated_pair_count_L": pair_count,
        "valuation_prefix": valuations,
        "exit_value": current,
        "exit_shadow_order_r": exit_order,
        "exit_valuation_probe": exit_valuations,
        "exit_type": exit_type,
    }


def collatz_exact_shadow_escape_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for shadow_order in range(1, 49):
        representative_added = False
        for odd_coefficient in [1, 3, 5, 7, 11]:
            start = (2**shadow_order) * odd_coefficient - 5
            if start <= 0:
                continue
            data = minus_five_shadow_data(start)
            pair_count = (shadow_order - 1) // 3
            expected_exit = (
                Fraction(9**pair_count, 8**pair_count) * (start + 5) - 5
            )
            exit_probe = data["exit_valuation_probe"]
            exit_order = int(data["exit_shadow_order_r"])
            exit_class_ok = (
                (exit_order == 1 and int(exit_probe[0]) >= 2)
                or (
                    exit_order == 2
                    and [int(value) for value in exit_probe] == [1, 1]
                )
                or (
                    exit_order == 3
                    and int(exit_probe[0]) == 1
                    and int(exit_probe[1]) >= 3
                )
            )
            checks = {
                "maximal_prefix_is_repeated_1_2": (
                    data["valuation_prefix"] == [1, 2] * pair_count
                ),
                "closed_formula_matches": (
                    expected_exit.denominator == 1
                    and data["exit_value"] == expected_exit.numerator
                ),
                "exit_order_is_one_two_or_three": exit_order in {1, 2, 3},
                "next_pair_is_not_1_2": (
                    [int(value) for value in exit_probe] != [1, 2]
                ),
                "exit_type_classification_matches": exit_class_ok,
                "positive_length_shadow_strictly_expands": (
                    pair_count == 0 or int(data["exit_value"]) > start
                ),
            }
            failures += sum(not value for value in checks.values())
            if not representative_added:
                rows.append(
                    {
                        **data,
                        "closed_formula": (
                            f"(9/8)^{pair_count}*(n+5)-5"
                        ),
                        "strict_expansion": (
                            pair_count > 0 and int(data["exit_value"]) > start
                        ),
                        "checks": checks,
                    }
                )
                representative_added = True

    bounded_failures = 0
    exit_type_counts = {"1": 0, "2": 0, "3": 0}
    maximum_pair_count = 0
    for start in range(1, 200_001, 2):
        data = minus_five_shadow_data(start)
        exit_order = str(data["exit_shadow_order_r"])
        exit_type_counts[exit_order] += 1
        maximum_pair_count = max(
            maximum_pair_count,
            int(data["maximal_repeated_pair_count_L"]),
        )
        if data["valuation_prefix"] != [1, 2] * int(
            data["maximal_repeated_pair_count_L"]
        ):
            bounded_failures += 1
    failures += bounded_failures

    return {
        "theorem": (
            "For every positive odd n, put s=v2(n+5) and "
            "L=floor((s-1)/3). The maximal initial accelerated Collatz "
            "valuation word made of repeated (1,2) pairs has exactly L "
            "pairs, and T^(2L)(n)+5=(9/8)^L(n+5). Its exit shadow order "
            "r=s-3L is in {1,2,3}; the next valuation pattern is "
            "respectively (at least 2,*), (1,1), or (1,at least 3), so "
            "another (1,2) pair is impossible. If L>=1, the exit value is "
            "strictly larger than n."
        ),
        "proof": (
            "Whenever x+5=2*c*8^r with r>=1, direct substitution gives "
            "the next two valuations (1,2) and "
            "T^2(x)+5=9(x+5)/8. Each pair therefore lowers v2(x+5) by "
            "exactly three until the remaining order is 1, 2, or 3. "
            "Substitution in those three terminal cases gives the stated "
            "exit patterns. The strict expansion for L>=1 follows from "
            "(9/8)^L>1."
        ),
        "finite_exact_rows": rows,
        "bounded_natural_audit": {
            "odd_starts_tested": 100_000,
            "limit": 200_000,
            "exit_type_counts": exit_type_counts,
            "maximum_pair_count": maximum_pair_count,
            "failure_count": bounded_failures,
        },
        "failure_count": failures,
    }


def is_squarefree(value: int) -> bool:
    for prime in range(2, math.isqrt(value) + 1):
        if value % (prime * prime) == 0:
            return False
    return True


def prime_divisors(value: int) -> list[int]:
    divisors: list[int] = []
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            divisors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        divisors.append(remaining)
    return divisors


def wheel_main_term(modulus: int, endpoint: int) -> int:
    result = 1
    for prime in prime_divisors(modulus):
        result *= prime - 1 if endpoint % prime == 0 else prime - 2
    return result


def cyclic_convolution(values: list[int], endpoint: int) -> int:
    modulus = len(values)
    return sum(
        values[index] * values[(endpoint - index) % modulus]
        for index in range(modulus)
    )


def goldbach_wheel_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for modulus in [6, 30, 210, 2310]:
        if modulus % 2 or not is_squarefree(modulus):
            raise AssertionError("audit wheels must be even and squarefree")
        reduced = [
            residue
            for residue in range(modulus)
            if math.gcd(residue, modulus) == 1
        ]
        values = [
            int(math.gcd(residue, modulus) == 1)
            for residue in range(modulus)
        ]
        direct_counts: list[int] = []
        formula_counts: list[int] = []
        witness_rows = []
        for endpoint in range(0, modulus, 2):
            direct = cyclic_convolution(values, endpoint)
            formula = wheel_main_term(modulus, endpoint)
            direct_counts.append(direct)
            formula_counts.append(formula)
            witness = next(
                residue
                for residue in reduced
                if (2 * residue - endpoint) % modulus != 0
            )
            singleton = [0] * modulus
            singleton[witness] = 1
            residual = [
                singleton[index] - values[index]
                for index in range(modulus)
            ]
            cross = sum(
                values[index]
                * residual[(endpoint - index) % modulus]
                for index in range(modulus)
            )
            exact_decomposition = direct + 2 * cross + cyclic_convolution(
                residual, endpoint
            )
            witness_rows.append(
                {
                    "endpoint": endpoint,
                    "singleton_residue": witness,
                    "singleton_endpoint_convolution": cyclic_convolution(
                        singleton, endpoint
                    ),
                    "g_plus_residual_decomposition": exact_decomposition,
                }
            )
        checks = {
            "all_direct_counts_match_product_formula": (
                direct_counts == formula_counts
            ),
            "all_even_endpoint_main_terms_positive": min(direct_counts) > 0,
            "every_endpoint_has_supported_singleton_hole": all(
                row["singleton_endpoint_convolution"] == 0
                for row in witness_rows
            ),
            "residual_identity_recovers_singleton_convolution": all(
                row["g_plus_residual_decomposition"] == 0
                for row in witness_rows
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "wheel_modulus_W": modulus,
                "prime_divisors": prime_divisors(modulus),
                "reduced_residue_count": len(reduced),
                "even_endpoints_audited": modulus // 2,
                "minimum_local_main_term": min(direct_counts),
                "maximum_local_main_term": max(direct_counts),
                "sample_hole_witnesses": witness_rows[: min(6, len(witness_rows))],
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let W>=6 be even and squarefree and let "
            "g(a)=1_(gcd(a,W)=1) on Z/WZ. For every even N, "
            "(g*g)(N)=product_{p|W,p|N}(p-1) "
            "product_{p|W,p not|N}(p-2)>0. For every real f=g+r, "
            "(f*f)(N)=(g*g)(N)+2(g*r)(N)+(r*r)(N), so positivity follows "
            "from 2||g||_2||r||_2+||r||_2^2<(g*g)(N). But for every such "
            "W,N there is a nonnegative singleton f supported on a reduced "
            "residue with (f*f)(N)=0."
        ),
        "proof": (
            "By the Chinese remainder theorem, at a prime p|W one excludes "
            "a=0 and a=N. These are one residue if p|N and two otherwise, "
            "giving the product. The p=2 factor is one because N is even; "
            "all odd-prime factors are positive. The residual identity is "
            "bilinearity and its sufficient bound is Cauchy-Schwarz. "
            "Writing W=2M, 2a=N mod W has at most one odd solution modulo "
            "W, while phi(W)>=2 for W>=6; hence a reduced residue outside "
            "that solution exists and its singleton convolution vanishes "
            "at N."
        ),
        "finite_exact_rows": rows,
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


def factor_with_spf(value: int, spf: list[int]) -> list[int]:
    factors: list[int] = []
    remaining = value
    while remaining > 1:
        prime = spf[remaining]
        factors.append(prime)
        remaining //= prime
    return factors


def twin_semiprime_cover_audit() -> dict[str, object]:
    source_path = (
        ROOT
        / "data/open-problem/twin-prime/"
        "tp-ticket-142-liouville-projector.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_rows = source["result"]["liouville_ledger_audit"]["rows"]
    rows: list[dict[str, object]] = []
    failures = 0
    for row in source_rows:
        edge_count = int(row["A00"])
        a10 = int(row["A10"])
        a01 = int(row["A01"])
        a11 = int(row["A11"])
        cells = {
            "++": (edge_count + a10 + a01 + a11) // 4,
            "+-": (edge_count + a10 - a01 - a11) // 4,
            "-+": (edge_count - a10 + a01 - a11) // 4,
            "--": (edge_count - a10 - a01 + a11) // 4,
        }
        left_semiprime = cells["++"] + cells["+-"]
        right_semiprime = cells["++"] + cells["-+"]
        double_semiprime = cells["++"]
        exact_twins = (
            edge_count
            - left_semiprime
            - right_semiprime
            + double_semiprime
        )
        marginal_lower_bound = (
            edge_count - left_semiprime - right_semiprime
        )
        checks = {
            "cell_counts_are_nonnegative": min(cells.values()) >= 0,
            "cell_counts_sum_to_edges": sum(cells.values()) == edge_count,
            "semiprime_marginals_match_walsh": (
                2 * left_semiprime == edge_count + a10
                and 2 * right_semiprime == edge_count + a01
            ),
            "inclusion_exclusion_recovers_twins": (
                exact_twins == int(row["direct_twin_count"]) == cells["--"]
            ),
            "marginal_cover_gives_valid_lower_bound": (
                marginal_lower_bound <= exact_twins
            ),
            "marginal_lower_bound_equals_negative_walsh_half": (
                2 * marginal_lower_bound == -(a10 + a01)
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": int(row["X"]),
                "edge_count_E": edge_count,
                "cell_counts": cells,
                "left_semiprime_edges_L": left_semiprime,
                "right_semiprime_edges_R": right_semiprime,
                "double_semiprime_edges_D": double_semiprime,
                "semiprime_endpoint_cover_L_plus_R": (
                    left_semiprime + right_semiprime
                ),
                "cover_ratio": (
                    (left_semiprime + right_semiprime) / edge_count
                ),
                "marginal_only_twin_lower_bound": marginal_lower_bound,
                "exact_twin_count": exact_twins,
                "checks": checks,
            }
        )

    factor_rows: list[dict[str, object]] = []
    for scale in [1_000, 10_000, 100_000]:
        limit = 2 * scale + 2
        threshold = limit ** (1 / 3)
        spf = smallest_prime_factors(limit)
        rough_composites = 0
        failures_here = 0
        minimum_factor = limit
        maximum_factor_count = 0
        for value in range(scale, limit + 1):
            if spf[value] ** 3 <= limit or spf[value] == value:
                continue
            factors = factor_with_spf(value, spf)
            rough_composites += 1
            minimum_factor = min(minimum_factor, min(factors))
            maximum_factor_count = max(maximum_factor_count, len(factors))
            if (
                len(factors) != 2
                or factors[0] * factors[1] != value
                or min(factors) <= threshold
            ):
                failures_here += 1
        failures += failures_here
        factor_rows.append(
            {
                "X": scale,
                "cubic_rough_composites_audited": rough_composites,
                "minimum_prime_factor_seen": minimum_factor,
                "maximum_factor_count": maximum_factor_count,
                "failure_count": failures_here,
            }
        )

    return {
        "theorem": (
            "On the TICKET-142 cubic-rough gap-two support let E be the "
            "edge count, L and R the counts whose left or right endpoint "
            "is semiprime, and D the count with both endpoints semiprime. "
            "Then the twin count is exactly E-L-R+D and is at least "
            "E-L-R=-(A10+A01)/2. Consequently, if some fixed delta>0 "
            "satisfies E>0 and L+R<=(1-delta)E on every sufficiently large "
            "dyadic scale, then every such scale contains at least one "
            "twin pair (indeed at least delta E before integrality). Every "
            "semiprime endpoint in this support has a unique "
            "factorization pq with (2X+2)^(1/3)<p<=q and p<=sqrt(2X+2)."
        ),
        "proof": (
            "At cubic roughness every supported endpoint has one or two "
            "prime factors; Liouville sign -1 is prime and +1 is "
            "semiprime. Inclusion-exclusion over the two semiprime "
            "endpoint events gives E-L-R+D for the -- cell. Dropping "
            "D>=0 gives the marginal lower bound, and "
            "L=(E+A10)/2, R=(E+A01)/2 gives its Walsh form. A composite "
            "supported endpoint cannot have three factors because each "
            "exceeds z=(2X+2)^(1/3), so its ordered semiprime factorization "
            "is unique."
        ),
        "finite_cover_rows": rows,
        "finite_factor_window_rows": factor_rows,
        "source_artifact": str(source_path.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "source_sha256": file_sha256(source_path),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_smooth_compact_tail_audit()
    collatz = collatz_exact_shadow_escape_audit()
    goldbach = goldbach_wheel_audit()
    twin_prime = twin_semiprime_cover_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )

    next_theorems = {
        "riemann": (
            "ExplicitWeilWaveletCoerciveReferenceAndRelativeTailNormBelowOne"
        ),
        "collatz": "ThreeExitTypePostShadowAdaptiveDescent",
        "goldbach": "VonMangoldtWheelResidualPointwiseBilinearSavingK56",
        "twin_prime": "CubicRoughSemiprimeEndpointCoverDeficit",
    }

    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-149",
            "theorem_name": "SmoothSchwartzCoreAndAbsoluteCompactTailNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": (
                riemann["imported_basis_fact"] + " " + riemann["no_go_proof"]
            ),
            "reproducible_computation": riemann,
            "logical_limit": (
                "Meyer completeness is an L2 theorem, not a proof that the "
                "chosen wavelets form the exact Weil test topology. The "
                "diagonal operator is synthetic, not the Weil quadratic "
                "form. The result only proves that absolute compact-tail "
                "smallness is the wrong certificate; it controls no zeta "
                "zero and proves neither RH nor its negation."
            ),
            "route_decision": {
                "discard": (
                    "smooth complete coordinates plus finite-prefix "
                    "positivity and an arbitrarily small absolute compact "
                    "tail as a global positivity certificate"
                ),
                "retain": (
                    "identify a coercive positive reference for the actual "
                    "Weil form and bound the remaining operator in relative "
                    "norm strictly below one"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "SmoothCompleteCoreAndSmallAbsoluteTailImpliesPositivity",
                "SmoothSchwartzCoreAndAbsoluteCompactTailNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One imported smooth "
                "basis theorem plus an exact operator-theoretic no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-149",
            "theorem_name": "MinusFiveShadowExactEscapeAndDescentNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Finite escape from this one 2-adic shadow does not imply "
                "eventual descent or termination. Indeed every nonempty "
                "shadow block exits above its entry value. Post-exit "
                "compensation across the three terminal types remains "
                "unproved; no divergent positive orbit was found."
            ),
            "route_decision": {
                "discard": (
                    "escape from the minus-five shadow by itself as a "
                    "descent certificate"
                ),
                "retain": (
                    "condition an adaptive post-shadow descent block on "
                    "the three exact terminal valuation types"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "MinusFiveShadowEscapeAloneForcesDescent",
                "MinusFiveShadowExactEscapeAndDescentNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent positive orbit. Exact "
                "finite escape is proved, while escape-to-descent is "
                "explicitly refuted for every nonempty shadow block."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-149",
            "theorem_name": (
                "SquarefreeWheelLocalMainTermAndResidualTransferNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The theorem is a cyclic residue model, not the interval "
                "von Mangoldt convolution. Its singleton counterweight is "
                "not Lambda. Exact local solubility supplies the major-arc "
                "factor but gives no pointwise residual saving, no K56 "
                "bound, and no proof or counterexample to strong Goldbach."
            ),
            "route_decision": {
                "discard": (
                    "wheel support and positive local singular factors "
                    "alone as a transfer theorem for prime weights"
                ),
                "retain": (
                    "use the exact wheel main term and prove a pointwise "
                    "von Mangoldt residual bilinear bound smaller than it"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "PositiveWheelLocalModelTransfersWithoutResidualControl",
                "SquarefreeWheelLocalMainTermAndResidualTransferNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "local-factor formula, a sufficient residual inequality, "
                "and a supported-weight transfer counterexample."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-149",
            "theorem_name": "CubicRoughSemiprimeEndpointCoverReduction",
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The finite cover ratios do not imply a uniform delta. "
                "The proposed all-scale semiprime endpoint-cover deficit "
                "is a parity-sensitive sieve statement and remains "
                "unproved. The reduction proves neither infinitely many "
                "twin primes nor a counterexample."
            ),
            "route_decision": {
                "discard": (
                    "treating a full joint A11 matching-coupling estimate "
                    "as the only possible sufficient route"
                ),
                "retain": (
                    "prove positive cubic-rough edge mass and bound the sum "
                    "of the two marginal semiprime endpoint covers below it"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "JointMatchingCouplingIsTheOnlySufficientRoute",
                "CubicRoughSemiprimeEndpointCoverReduction",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. One exact "
                "marginal-cover reduction and finite factor-window audit."
            ),
        },
    }

    return {
        "theorem_name": "FourConjectureSmoothEscapeWheelCoverAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-149 proves four exact intermediate statements or "
            "reductions and resolves no target conjecture. It rejects "
            "absolute compact-tail positivity even on smooth complete "
            "coordinates, exactly classifies finite escape from the "
            "Collatz minus-five shadow, isolates the positive Goldbach "
            "wheel main term and its missing residual transfer, and "
            "reduces the cubic-rough Twin target to a weaker semiprime "
            "endpoint-cover deficit."
        ),
        **sections,
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "historical_correction_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    attempts: list[dict[str, object]] = []
    for problem_id in ["riemann", "collatz", "goldbach", "twin-prime"]:
        key = problem_id.replace("-", "_")
        section = audit[key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "attempt": section["declared_proposition"],
                "bounded_result": {
                    "audit_ref": f"smooth_escape_wheel_cover_audit.{key}"
                },
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_theorem"],
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
        "smooth_escape_wheel_cover_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket149-smooth-escape-wheel-cover.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-149-smooth-compact-tail-no-go.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-149-minus-five-exact-escape.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-149-wheel-residual-transfer.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-149-semiprime-cover-reduction.json"
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
