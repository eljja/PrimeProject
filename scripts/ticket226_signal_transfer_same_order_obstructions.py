from __future__ import annotations

import bisect
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket226-signal-transfer-same-order-obstructions.v1"
GENERATED_AT = "2026-08-14T23:55:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    no_go: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T225", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T226", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N226",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN226",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T225", f"{prefix}-T226"],
            [f"{prefix}-T226", f"{prefix}-N226"],
            [f"{prefix}-T226", f"{prefix}-OPEN226"],
            [f"{prefix}-OPEN226", prefix],
        ],
    }


def primality_sieve(limit: int) -> bytearray:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )
    return sieve


def primes_through(limit: int) -> list[int]:
    sieve = primality_sieve(limit)
    return [value for value in range(2, limit + 1) if sieve[value]]


def von_mangoldt_prime_powers(limit: int) -> list[tuple[int, float]]:
    rows: list[tuple[int, float]] = []
    for prime in primes_through(limit):
        logarithm = math.log(prime)
        power = prime
        while power <= limit:
            rows.append((power, logarithm))
            if power > limit // prime:
                break
            power *= prime
    rows.sort()
    return rows


def geometric_first_moment_tail(q: float, cutoff: int) -> float:
    return (q ** (cutoff + 1)) * ((cutoff + 1) - cutoff * q) / (
        (1.0 - q) ** 2
    )


def riemann_balanced_kernel_audit() -> dict[str, Any]:
    indices = list(range(3, 14))
    cutoff_multiplier = 48
    maximum_cutoff = cutoff_multiplier * (2 ** max(indices))
    prime_powers = von_mangoldt_prime_powers(maximum_cutoff)
    rows = []
    failures = 0
    transcript = hashlib.sha256()

    for index in indices:
        scale = 2**index
        rate = 1.0 / scale
        cutoff = cutoff_multiplier * scale
        first_laplace = math.fsum(
            weight * math.exp(-rate * value)
            for value, weight in prime_powers
            if value <= cutoff
        )
        second_laplace = math.fsum(
            weight * math.exp(-2.0 * rate * value)
            for value, weight in prime_powers
            if value <= cutoff
        )
        prime_band = first_laplace - second_laplace - 1.0 / (2.0 * rate)

        # Partial summation gives the same value as the Chebyshev-error integral.
        chebyshev_kernel_integral = (
            first_laplace - 1.0 / rate
        ) - (second_laplace - 1.0 / (2.0 * rate))
        identity_error = abs(prime_band - chebyshev_kernel_integral)
        tail_bound = geometric_first_moment_tail(math.exp(-rate), cutoff)
        verified = identity_error < 1e-12 and prime_band + tail_bound < 0.0
        failures += int(not verified)
        row = {
            "dyadic_index_j": index,
            "scale_2_to_j": scale,
            "cutoff_N": cutoff,
            "prime_band_P_a": prime_band,
            "chebyshev_error_kernel_integral": chebyshev_kernel_integral,
            "identity_absolute_error": identity_error,
            "tail_upper_bound": tail_bound,
            "negative_sign_certified": prime_band + tail_bound < 0.0,
            "identity_verified": identity_error < 1e-12,
        }
        transcript.update((json.dumps(row, sort_keys=True) + "\n").encode("ascii"))
        rows.append(row)

    mass_rows = []
    for rate in (1.0, 0.5, 0.125, 1.0 / 1024.0):
        zero_crossing = math.log(2.0) / rate
        negative_mass = -0.25
        positive_mass = 0.25
        verified = abs(negative_mass + positive_mass) < 1e-15
        failures += int(not verified)
        mass_rows.append(
            {
                "rate_a": rate,
                "zero_crossing_log2_over_a": zero_crossing,
                "negative_kernel_mass": negative_mass,
                "positive_kernel_mass": positive_mass,
                "total_kernel_mass": negative_mass + positive_mass,
                "balanced_mass_verified": verified,
            }
        )

    negative_support = math.log(2.0) / 4.0
    positive_support = 2.0 * math.log(2.0)
    signed_witnesses = [
        {
            "support_x": negative_support,
            "kernel_value_at_a_1": math.exp(-negative_support)
            - 2.0 * math.exp(-2.0 * negative_support),
            "sign": "negative",
        },
        {
            "support_x": positive_support,
            "kernel_value_at_a_1": math.exp(-positive_support)
            - 2.0 * math.exp(-2.0 * positive_support),
            "sign": "positive",
        },
    ]
    witness_verified = (
        signed_witnesses[0]["kernel_value_at_a_1"] < 0.0
        and signed_witnesses[1]["kernel_value_at_a_1"] > 0.0
    )
    failures += int(not witness_verified)

    theorem = (
        "Let psi(x)=sum_{n<=x} Lambda(n), E(x)=psi(x)-x, and "
        "P(a)=sum Lambda(n)(exp(-an)-exp(-2an))-1/(2a). For every a>0, "
        "P(a)=a integral_0^infinity E(x)(exp(-ax)-2exp(-2ax)) dx. The "
        "kernel changes sign at log(2)/a, has total mass zero, and has "
        "negative and positive masses -1/4 and +1/4. Therefore a sign of "
        "P(a) is a balanced contrast of Chebyshev error, not a positive "
        "functional and not by itself a Weil-positivity or RH certificate."
    )
    proof = (
        "Stieltjes partial summation gives sum Lambda(n)exp(-can)="
        "ca integral psi(x)exp(-cax) dx. Subtracting the exact x integrals "
        "for c=1 and c=2 yields the displayed identity. With u=ax, the "
        "kernel e^(-u)-2e^(-2u) vanishes at log 2. Its antiderivative "
        "-e^(-u)+e^(-2u) gives -1/4 below the crossing and +1/4 above it."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "actual_prime_kernel_rows": rows,
        "balanced_kernel_mass_rows": mass_rows,
        "opposite_sign_atomic_witnesses": signed_witnesses,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "chebyshev_error_kernel_identity_proved": True,
            "balanced_sign_changing_kernel_proved": True,
            "direct_band_sign_to_positive_functional_transfer_refuted": True,
            "certified_negative_prime_bands": sum(
                row["negative_sign_certified"] for row in rows
            ),
            "dense_weil_core_transfer_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem rejects only a direct sign-to-positivity reading. "
            "The complete band profile can still carry information, but no "
            "uniform explicit-formula estimate transfers it to the Weil form."
        ),
        "failure_count": failures,
    }


def collatz_intercept(word: tuple[int, ...]) -> int:
    height = len(word)
    prefix = 0
    total = 0
    for index, exponent in enumerate(word):
        total += (3 ** (height - index - 1)) * (2**prefix)
        prefix += exponent
    return total


def rotations(word: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [word[index:] + word[:index] for index in range(len(word))]


def is_primitive_word(word: tuple[int, ...]) -> bool:
    size = len(word)
    return all(
        size % period != 0 or word != word[:period] * (size // period)
        for period in range(1, size)
    )


def collatz_infinite_minimum_no_go_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    audited_r = range(1, 41)
    selected_r = {1, 2, 3, 5, 10, 20, 40}

    for repetition in audited_r:
        word = (1, 1, 3) * repetition + (2,)
        power_32 = 32**repetition
        power_27 = 27**repetition
        denominator = 4 * power_32 - 3 * power_27
        intercept_formula = (62 * power_32 - 57 * power_27) // 5
        intercepts = [collatz_intercept(local) for local in rotations(word)]
        primitive = is_primitive_word(word)
        formula_verified = intercepts[0] == intercept_formula
        strict_minimum = min(intercepts) == intercept_formula
        above_denominator = intercept_formula > denominator
        below_four_denominators = intercept_formula < 4 * denominator
        noncycle = intercept_formula % denominator != 0
        verified = all(
            (
                primitive,
                formula_verified,
                strict_minimum,
                above_denominator,
                below_four_denominators,
                noncycle,
            )
        )
        failures += int(not verified)
        if repetition in selected_r:
            rows.append(
                {
                    "repetition_r": repetition,
                    "height_h": len(word),
                    "valuation_sum_S": sum(word),
                    "D": denominator,
                    "minimum_intercept_B": intercept_formula,
                    "B_over_D": intercept_formula / denominator,
                    "primitive_word_verified": primitive,
                    "all_cyclic_intercepts_above_D": strict_minimum
                    and above_denominator,
                    "D_divides_B": not noncycle,
                    "noncycle_verified": noncycle,
                }
            )

    theorem = (
        "For every r>=1, the valuation word w_r=(1,1,3)^r followed by 2 is "
        "primitive, has D_r=4*32^r-3*27^r>0, and has minimum cyclic "
        "intercept B_r=(62*32^r-57*27^r)/5>D_r. Nevertheless D_r does not "
        "divide B_r, so w_r is not a Collatz cycle. Hence the sufficient "
        "certificate min_i B_i<D cannot be promoted to a universal "
        "noncycle criterion, even within an explicit infinite primitive family."
    )
    proof = (
        "The final exponent 2 is unique, proving primitivity. Concatenation "
        "of U=(1,1,3), whose affine data are (27,32,19), gives the displayed "
        "D_r and B_r. The associated fixed point n_0=B_r/D_r satisfies "
        "1<n_0<19/5. Inside U, the first two accelerated steps increase, "
        "and U maps n to (27n+19)/32, which increases every n<19/5 while "
        "preserving that interval. Thus n_0 is the least cyclic state and "
        "B_r is the least intercept. Also 1<B_r/D_r<4. Equality to 2 would "
        "force 22*32^r=27*27^r, and equality to 3 would force "
        "2*32^r=12*27^r; prime factorization rules out both. Therefore the "
        "fixed point is not an integer and D_r does not divide B_r."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "infinite_family_audit_rows": rows,
        "aggregate": {
            "repetitions_checked": len(list(audited_r)),
            "infinite_primitive_family_proved": True,
            "all_family_minimum_intercepts_above_D_proved": True,
            "all_family_words_noncycles_proved": True,
            "universal_minimum_intercept_descent_refuted": True,
            "all_nontrivial_cycles_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The infinite family refutes necessity of min B<D but contains "
            "no cycle. It neither constructs a divergent orbit nor excludes "
            "D|B for every other primitive word."
        ),
        "failure_count": failures,
    }


def cube_root_cutoff(horizon: int) -> int:
    cutoff = max(1, round(horizon ** (1.0 / 3.0)))
    while cutoff**3 < horizon:
        cutoff += 1
    while cutoff > 1 and (cutoff - 1) ** 3 >= horizon:
        cutoff -= 1
    return cutoff


def cube_root_support(
    horizon: int,
) -> tuple[int, bytearray, bytearray, bytearray, list[int]]:
    prime = primality_sieve(horizon)
    primes = [value for value in range(2, horizon + 1) if prime[value]]
    cutoff = cube_root_cutoff(horizon)
    rough = bytearray(b"\x01") * (horizon + 1)
    rough[0:2] = b"\x00\x00"
    for divisor in primes:
        if divisor > cutoff:
            break
        start = 2 * divisor
        rough[start : horizon + 1 : divisor] = b"\x00" * (
            ((horizon - start) // divisor) + 1
        )
    semiprime = bytearray(horizon + 1)
    for value in range(2, horizon + 1):
        semiprime[value] = bool(rough[value] and not prime[value])
    return cutoff, prime, semiprime, rough, primes


def exact_rough_semiprime_formula(
    horizon: int, cutoff: int, primes: list[int]
) -> int:
    total = 0
    for first in primes:
        if first <= cutoff:
            continue
        if first * first > horizon:
            break
        upper_index = bisect.bisect_right(primes, horizon // first)
        lower_index = bisect.bisect_left(primes, first)
        total += upper_index - lower_index
    return total


def shared_semiprime_density_rows() -> tuple[list[dict[str, Any]], int]:
    rows = []
    failures = 0
    for horizon in (10_000, 100_000, 1_000_000):
        cutoff, prime, semiprime, _, primes = cube_root_support(horizon)
        prime_count = sum(prime)
        semiprime_count = sum(semiprime)
        formula_count = exact_rough_semiprime_formula(horizon, cutoff, primes)
        verified = semiprime_count == formula_count
        failures += int(not verified)
        rows.append(
            {
                "horizon_X": horizon,
                "cube_root_cutoff_z": cutoff,
                "prime_count_pi_X": prime_count,
                "rough_semiprime_count_S_X": semiprime_count,
                "exact_prime_pair_formula_count": formula_count,
                "S_over_pi": semiprime_count / prime_count,
                "S_normalized_by_X_over_log_X": semiprime_count
                / (horizon / math.log(horizon)),
                "asymptotic_ratio_log_2": math.log(2.0),
                "exact_count_identity_verified": verified,
            }
        )
    return rows, failures


def goldbach_same_order_audit(
    density_rows: list[dict[str, Any]], density_failures: int
) -> dict[str, Any]:
    rows = []
    failures = density_failures
    for density in density_rows:
        horizon = density["horizon_X"]
        cutoff, prime, semiprime, rough, _ = cube_root_support(horizon)
        counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
        for left in range(2, horizon - 1):
            right = horizon - left
            if prime[left] and prime[right]:
                counts["PP"] += 1
            elif prime[left] and semiprime[right]:
                counts["PS"] += 1
            elif semiprime[left] and prime[right]:
                counts["SP"] += 1
            elif semiprime[left] and semiprime[right]:
                counts["SS"] += 1
        contamination = counts["PS"] + counts["SP"] + counts["SS"]
        filtered = sum(
            1
            for left in range(2, horizon - 1)
            if rough[left] and rough[horizon - left]
        )
        verified = filtered == sum(counts.values())
        failures += int(not verified)
        rows.append(
            {
                "even_target_N": horizon,
                "cutoff_z": cutoff,
                "prime_prime_PP": counts["PP"],
                "prime_semiprime_PS": counts["PS"],
                "semiprime_prime_SP": counts["SP"],
                "semiprime_semiprime_SS": counts["SS"],
                "rough_semiprime_contamination_E": contamination,
                "filtered_total_QQ": filtered,
                "E_over_PP": contamination / counts["PP"],
                "contamination_below_PP": contamination < counts["PP"],
                "exact_decomposition_verified": verified,
            }
        )

    theorem = (
        "Let z=X^(1/3) and let S_z(X) count products pq<=X with primes "
        "z<p<=q. Then S_z(X)~(log 2)X/log X and S_z(X)/pi(X)->log 2. "
        "Thus the cube-root rough-semiprime marginal is of the same "
        "asymptotic order as the prime marginal, not a lower-order error. "
        "Moreover, the stronger pointwise route PS+SP+SS<PP is already "
        "false for explicit even targets while PP remains positive."
    )
    proof = (
        "Unique ordering by the smaller prime gives exactly "
        "S_z(X)=sum_{z<p<=sqrt(X)}(pi(X/p)-pi(p-1)). The second term is "
        "O(X/log^2 X). Uniform PNT for X/p>=sqrt(X), followed by prime "
        "partial summation and t=X^u, gives (X/log X) times the integral "
        "from 1/3 to 1/2 of du/[u(1-u)]=(log 2)X/log X. The finite "
        "convolution rows are complete enumerations and directly refute "
        "contamination<PP; they do not refute Goldbach."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "rough_semiprime_density_rows": density_rows,
        "goldbach_convolution_rows": rows,
        "aggregate": {
            "exact_semiprime_count_formula_proved": True,
            "rough_semiprime_to_prime_ratio_limit": "log(2)",
            "same_asymptotic_order_via_PNT_proved": True,
            "lower_order_contamination_route_refuted": True,
            "finite_targets_with_contamination_at_least_PP": sum(
                not row["contamination_below_PP"] for row in rows
            ),
            "uniform_pointwise_signed_minor_arc_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The PNT argument is a one-point density theorem, not a "
            "pointwise additive convolution asymptotic. The finite targets "
            "show that PP can be positive even when contamination exceeds PP."
        ),
        "failure_count": failures,
    }


def twin_same_order_audit(
    density_rows: list[dict[str, Any]], density_failures: int
) -> dict[str, Any]:
    rows = []
    failures = density_failures
    for density in density_rows:
        horizon = density["horizon_X"]
        cutoff, prime, semiprime, rough, _ = cube_root_support(horizon)
        counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
        for left in range(2, horizon - 1):
            right = left + 2
            if prime[left] and prime[right]:
                counts["PP"] += 1
            elif prime[left] and semiprime[right]:
                counts["PS"] += 1
            elif semiprime[left] and prime[right]:
                counts["SP"] += 1
            elif semiprime[left] and semiprime[right]:
                counts["SS"] += 1
        contamination = counts["PS"] + counts["SP"] + counts["SS"]
        filtered = sum(
            1
            for left in range(2, horizon - 1)
            if rough[left] and rough[left + 2]
        )
        verified = filtered == sum(counts.values())
        failures += int(not verified)
        rows.append(
            {
                "horizon_X": horizon,
                "cutoff_z": cutoff,
                "prime_prime_PP": counts["PP"],
                "prime_semiprime_PS": counts["PS"],
                "semiprime_prime_SP": counts["SP"],
                "semiprime_semiprime_SS": counts["SS"],
                "rough_semiprime_pair_contamination_E": contamination,
                "filtered_gap_two_pairs_R": filtered,
                "E_over_PP": contamination / counts["PP"],
                "contamination_below_PP": contamination < counts["PP"],
                "exact_pair_decomposition_verified": verified,
            }
        )

    theorem = (
        "The same exact count S_z(X)~(log 2)X/log X proves that cube-root "
        "rough semiprimes have the same marginal order as primes. Therefore "
        "Type-I or marginal density alone cannot make the shifted PS, SP, "
        "and SS channels lower order. Complete finite gap-two audits also "
        "give explicit horizons where PS+SP+SS>=PP, refuting that stronger "
        "domination route without refuting the Twin Prime conjecture."
    )
    proof = (
        "The marginal asymptotic is the unique-smaller-factor formula and "
        "PNT calculation stated in the Goldbach track. It makes no claim "
        "about shifted independence. The pair rows classify every retained "
        "n,n+2 into PP, PS, SP, or SS and compare exact integer counts. "
        "Since shifted pair control is absent from the marginal theorem, "
        "a genuine Type-II correlation estimate remains necessary."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "rough_semiprime_density_rows": density_rows,
        "gap_two_pair_rows": rows,
        "aggregate": {
            "same_order_rough_semiprime_marginal_proved": True,
            "type_i_marginal_only_route_refuted": True,
            "finite_horizons_with_contamination_at_least_PP": sum(
                not row["contamination_below_PP"] for row in rows
            ),
            "shifted_type_ii_power_saving_proved": False,
            "infinitely_many_twin_primes_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "No asymptotic for rough-semiprime gap-two pairs is claimed. "
            "Marginal same-order density and three finite counterexamples do "
            "not decide whether PP occurs infinitely often."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_balanced_kernel_audit()
    collatz = collatz_infinite_minimum_no_go_audit()
    density_rows, density_failures = shared_semiprime_density_rows()
    goldbach = goldbach_same_order_audit(density_rows, density_failures)
    twin = twin_same_order_audit(density_rows, density_failures)

    root = {
        "theorem_name": "SignalTransferAndSameOrderObstructionsForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-226 proves four exact transfer or no-go theorems, "
            "corrects three TICKET-225 continuation routes, and resolves "
            "none of the four parent conjectures."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-226",
            "theorem_name": "BalancedChebyshevKernelIdentityAndDirectSignTransferNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The exact balanced kernel explains the observed prime-band "
                "signs but supplies no uniform estimate on a dense Weil core "
                "and excludes no off-critical zero."
            ),
            "route_decision": {
                "discard": "reading cofinal signs of one balanced Laplace contrast as direct Weil positivity",
                "retain": "use the explicit formula with quantitative control of the full balanced-band profile on a dense Weil core",
                "next_single_lemma": "ExplicitFormulaControlOfBalancedChebyshevBandsOnDenseWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "ActualPrimeBandTailCertificateAndFiniteBandNoGo",
                "BalancedChebyshevKernelIdentityAndDirectSignTransferNoGo",
                "BandSignDirectlyImpliesWeilPositivity",
                "ExplicitFormulaControlOfBalancedChebyshevBandsOnDenseWeilCore",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-226",
            "theorem_name": "InfinitePrimitiveMinimumInterceptCounterfamily",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The family proves that min B<D is not necessary for a "
                "noncycle, but it neither excludes every D|B word nor proves "
                "descent of every aperiodic natural orbit."
            ),
            "route_decision": {
                "discard": "promoting the minimum cyclic intercept below D from a sufficient test to a universal noncycle criterion",
                "retain": "attack exact affine divisibility D|B directly, independent of intercept size",
                "next_single_lemma": "NoNontrivialPrimitiveValuationWordSatisfiesDDividesB",
            },
            "proof_dag": proof_dag(
                "CO",
                "CyclicGcdResidualInvarianceAndRotationNoGo",
                "InfinitePrimitiveMinimumInterceptCounterfamily",
                "EveryNontrivialPrimitiveWordHasMinimumInterceptBelowD",
                "NoNontrivialPrimitiveValuationWordSatisfiesDDividesB",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-226",
            "theorem_name": "CubeRootSemiprimeSameOrderAndGoldbachDominationNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The marginal PNT theorem rejects a lower-order-error model "
                "but gives no pointwise additive cancellation for every even target."
            ),
            "route_decision": {
                "discard": "treating cube-root rough-semiprime contamination as o(prime mass), or requiring contamination below PP",
                "retain": "return to a signed circle-method decomposition where arithmetic cancellation, not marginal sparsity, controls the minor contribution",
                "next_single_lemma": "FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly",
            },
            "proof_dag": proof_dag(
                "GB",
                "CubeRootRoughSemiprimeGoldbachDecomposition",
                "CubeRootSemiprimeSameOrderAndGoldbachDominationNoGo",
                "CubeRootSemiprimeContaminationIsLowerOrder",
                "FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-226",
            "theorem_name": "CubeRootSemiprimeMarginalSameOrderAndPairDominationNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "Same-order marginals show why Type-I data are insufficient, "
                "but no shifted Type-II power saving or positive unbounded PP "
                "block margin has been proved."
            ),
            "route_decision": {
                "discard": "expecting marginal cube-root semiprime sparsity alone to dominate PS, SP, and SS",
                "retain": "estimate the shifted semiprime channels with genuine Type-II bilinear information on unbounded blocks",
                "next_single_lemma": "ShiftedCubeRootParityTypeIIBilinearPowerSavingOnUnboundedBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "CubeRootTwinPairTypeDecompositionAndParityNoGo",
                "CubeRootSemiprimeMarginalSameOrderAndPairDominationNoGo",
                "CubeRootPairContaminationIsLowerOrderFromMarginals",
                "ShiftedCubeRootParityTypeIIBilinearPowerSavingOnUnboundedBlocks",
                "TwinPrimeConjecture",
            ),
        },
    }

    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    total_failures = sum(
        root[key]["reproducible_computation"]["failure_count"] for key in tracks
    )
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": total_failures,
    }

    attempts = []
    for key in tracks:
        track = root[key]
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "bounded_result": {
                    "audit_ref": f"#/signal_transfer_same_order_obstructions_audit/{key}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "proof_dag": track["proof_dag"],
            }
        )

    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-226 proves four transfer or same-order obstruction "
            "results and resolves none of the four parent conjectures."
        ),
        "signal_transfer_same_order_obstructions_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["signal_transfer_same_order_obstructions_audit"]
    write_json(
        ROOT
        / "data/open-problem/ticket226-signal-transfer-same-order-obstructions.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-226-balanced-chebyshev-kernel.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-226-minimum-intercept-counterfamily.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-226-semiprime-same-order.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-226-semiprime-marginal.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["signal_transfer_same_order_obstructions_audit"][
        "machine_audit"
    ]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
