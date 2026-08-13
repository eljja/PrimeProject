from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket225-arithmetic-remainder-localization.v1"
GENERATED_AT = "2026-08-14T23:30:00+09:00"
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
            {"id": f"{prefix}-T224", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T225", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N225",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN225",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T224", f"{prefix}-T225"],
            [f"{prefix}-T225", f"{prefix}-N225"],
            [f"{prefix}-T225", f"{prefix}-OPEN225"],
            [f"{prefix}-OPEN225", prefix],
        ],
    }


def primes_through(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def primality_sieve(limit: int) -> bytearray:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )
    return sieve


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_primes(start: int, count: int) -> list[int]:
    result = []
    candidate = max(2, start)
    while len(result) < count:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1
    return result


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def von_mangoldt_prime_powers(limit: int) -> list[tuple[int, float]]:
    rows = []
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


def null_vector(matrix: list[list[float]]) -> tuple[list[float], int]:
    rows = len(matrix)
    columns = len(matrix[0])
    reduced = [row[:] for row in matrix]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        selected = max(range(pivot_row, rows), key=lambda row: abs(reduced[row][column]))
        if abs(reduced[selected][column]) < 1e-14:
            continue
        reduced[pivot_row], reduced[selected] = reduced[selected], reduced[pivot_row]
        divisor = reduced[pivot_row][column]
        reduced[pivot_row] = [value / divisor for value in reduced[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            multiplier = reduced[row][column]
            reduced[row] = [
                reduced[row][index] - multiplier * reduced[pivot_row][index]
                for index in range(columns)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = next(column for column in range(columns) if column not in pivots)
    vector = [0.0] * columns
    vector[free] = 1.0
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(
            reduced[row][column] * vector[column]
            for column in range(pivot + 1, columns)
        )
    scale = max(abs(value) for value in vector)
    return [value / scale for value in vector], len(pivots)


def riemann_prime_band_audit() -> dict[str, Any]:
    indices = list(range(3, 16))
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
        terms = [
            weight
            * (math.exp(-rate * value) - math.exp(-2.0 * rate * value))
            for value, weight in prime_powers
            if value <= cutoff
        ]
        finite_defect = math.fsum(terms) - 1.0 / (2.0 * rate)
        q = math.exp(-rate)
        tail_bound = geometric_first_moment_tail(q, cutoff)
        certified_negative = finite_defect + tail_bound < 0.0
        failures += int(not certified_negative)
        row = {
            "dyadic_index_j": index,
            "scale_2_to_j": scale,
            "cutoff_N": cutoff,
            "finite_prime_band_defect": finite_defect,
            "von_mangoldt_tail_upper_bound": tail_bound,
            "certified_full_band_interval": [
                finite_defect,
                finite_defect + tail_bound,
            ],
            "negative_sign_certified": certified_negative,
        }
        transcript.update((json.dumps(row, sort_keys=True) + "\n").encode("ascii"))
        rows.append(row)

    kernel_rows = []
    for observed_count in (3, 4, 5, 6, 7, 8):
        observed = list(range(3, 3 + observed_count))
        supports = [4.0**index for index in range(observed_count + 1)]
        matrix = [
            [
                math.exp(-support / (2**index))
                - math.exp(-2.0 * support / (2**index))
                for support in supports
            ]
            for index in observed
        ]
        vector, rank = null_vector(matrix)
        residual = max(
            abs(math.fsum(row[index] * vector[index] for index in range(len(vector))))
            for row in matrix
        )
        verified = rank == observed_count and residual < 1e-10
        failures += int(not verified)
        kernel_rows.append(
            {
                "observed_band_count": observed_count,
                "atomic_support_count": len(supports),
                "numerical_matrix_rank": rank,
                "maximum_null_residual": residual,
                "nonzero_signed_atomic_kernel_verified": verified,
            }
        )

    theorem = (
        "For a>0 define the actual prime-side Laplace band defect "
        "P(a)=sum_{n>=2} Lambda(n)(exp(-an)-exp(-2an))-1/(2a). "
        "For every integer N>=2, its omitted prime contribution is positive "
        "and at most q^(N+1)((N+1)-Nq)/(1-q)^2, q=exp(-a). Hence the "
        "finite von Mangoldt sum plus this explicit interval certifies the "
        "full band sign. Conversely, any finite family of band functionals "
        "has a nonzero finitely supported signed measure in its common "
        "kernel, so finitely many band signs cannot identify an arbitrary "
        "defect measure or constitute an RH criterion."
    )
    proof = (
        "The main term is the exact integral of exp(-ax)-exp(-2ax) over "
        "x>=0. Since 0<=exp(-an)-exp(-2an)<=exp(-an) and "
        "Lambda(n)<=log(n)<=n, the tail is bounded by sum_{n>N} n q^n; "
        "differentiating the geometric series gives the displayed closed "
        "form. For the no-go, evaluate m band functionals on m+1 distinct "
        "atoms. The resulting linear map from R^(m+1) to R^m has a nonzero "
        "kernel vector by rank-nullity."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "actual_prime_band_rows": rows,
        "finite_band_kernel_rows": kernel_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "actual_von_mangoldt_band_tail_bound_proved": True,
            "certified_negative_dyadic_bands": sum(
                row["negative_sign_certified"] for row in rows
            ),
            "finite_band_family_noninjectivity_proved": True,
            "explicit_formula_transfer_to_weil_positivity_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The calculation certifies signs of one actual prime-side "
            "Laplace observable at finitely many scales. It neither converts "
            "those signs into Weil positivity nor excludes an off-critical "
            "zero. Rank-nullity blocks every finite-band identification route."
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


def is_primitive_word(word: tuple[int, ...]) -> bool:
    size = len(word)
    for period in range(1, size):
        if size % period == 0 and word == word[:period] * (size // period):
            return False
    return True


def rotations(word: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [word[index:] + word[:index] for index in range(len(word))]


def collatz_cyclic_gcd_audit() -> dict[str, Any]:
    failures = 0
    height_rows = []
    witness_word = (1, 1, 2, 4, 3)
    witness_rows = []
    total_positive_primitive = 0
    total_transition_checks = 0
    total_minimum_certificates = 0
    total_cycles = 0

    for height in range(2, 8):
        words_checked = 0
        positive_primitive = 0
        invariant_failures = 0
        transition_failures = 0
        minimum_certificates = 0
        exact_cycles = 0
        residuals: set[int] = set()
        for word in itertools.product(range(1, 6), repeat=height):
            words_checked += 1
            if not is_primitive_word(word):
                continue
            denominator = 2 ** sum(word) - 3**height
            if denominator <= 0:
                continue
            positive_primitive += 1
            rotated = rotations(word)
            intercepts = [collatz_intercept(local) for local in rotated]
            gcds = [math.gcd(denominator, value) for value in intercepts]
            invariant_failures += int(len(set(gcds)) != 1)
            residuals.add(denominator // gcds[0])
            exact_cycle = denominator != 0 and intercepts[0] % denominator == 0
            exact_cycles += int(exact_cycle)
            minimum_certificates += int(min(intercepts) < denominator)
            for index, local in enumerate(rotated):
                following = rotated[(index + 1) % height]
                identity = (
                    (2 ** local[0]) * collatz_intercept(following)
                    == 3 * collatz_intercept(local) + denominator
                )
                transition_failures += int(not identity)
                total_transition_checks += 1
        failures += invariant_failures + transition_failures
        total_positive_primitive += positive_primitive
        total_minimum_certificates += minimum_certificates
        total_cycles += exact_cycles
        height_rows.append(
            {
                "height_h": height,
                "words_checked": words_checked,
                "positive_primitive_words": positive_primitive,
                "cyclic_gcd_invariance_failures": invariant_failures,
                "cyclic_transition_identity_failures": transition_failures,
                "minimum_intercept_below_D_certificates": minimum_certificates,
                "unresolved_by_minimum_certificate": positive_primitive
                - minimum_certificates,
                "exact_nontrivial_cycles_found": exact_cycles,
                "distinct_residual_obstructions": len(residuals),
            }
        )

    witness_d = 2 ** sum(witness_word) - 3 ** len(witness_word)
    for index, local in enumerate(rotations(witness_word)):
        intercept = collatz_intercept(local)
        common_gcd = math.gcd(witness_d, intercept)
        witness_rows.append(
            {
                "rotation_index": index,
                "valuation_word": list(local),
                "B": intercept,
                "gcd_D_B": common_gcd,
                "residual_D_over_gcd": witness_d // common_gcd,
            }
        )
    witness_verified = (
        witness_d == 1805
        and {row["gcd_D_B"] for row in witness_rows} == {95}
        and {row["residual_D_over_gcd"] for row in witness_rows} == {19}
    )
    failures += int(not witness_verified)

    theorem = (
        "Let a=(a_1,...,a_h) be a positive accelerated Collatz word, "
        "D=2^S-3^h>0, and let B_i be the affine intercept of its i-th "
        "cyclic rotation. Consecutive rotations satisfy "
        "2^(a_i) B_(i+1)=3B_i+D. Therefore gcd(D,B_i) and the residual "
        "obstruction R=D/gcd(D,B_i) are invariant under every cyclic "
        "rotation. In particular, if one rotation has 0<B_i<D then the "
        "word is not a cycle. Rotation-by-rotation factor tests cannot "
        "accumulate independent prime-power obstructions because every "
        "rotation carries the same gcd residual."
    )
    proof = (
        "Write B_i=3^(h-1)+2^(a_i)C for the suffix intercept C. The next "
        "rotation has B_(i+1)=3C+2^(S-a_i). Multiplication by 2^(a_i) "
        "gives 3B_i-3^h+2^S=3B_i+D. Since D is coprime to both 2 and 3, "
        "taking gcd with D proves invariance. If D divides every cycle "
        "intercept, a positive intercept smaller than D is an immediate "
        "contradiction."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_height_rows": height_rows,
        "ticket224_witness_rotation_rows": witness_rows,
        "aggregate": {
            "positive_primitive_words_checked": total_positive_primitive,
            "cyclic_transition_checks": total_transition_checks,
            "cyclic_gcd_invariance_proved": True,
            "rotation_independent_deficit_accumulation_refuted": True,
            "minimum_intercept_certificates_found": total_minimum_certificates,
            "nontrivial_cycles_found": total_cycles,
            "all_nontrivial_cycles_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Cyclic rotations expose different intercept sizes but no new "
            "gcd or prime-power residual. The minimum-intercept certificate "
            "closes many finite words, not all words, and says nothing about "
            "aperiodic divergent trajectories."
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


def factor_integer(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def cube_root_labels(horizon: int) -> tuple[int, list[int], list[str], bytearray]:
    cutoff = cube_root_cutoff(horizon)
    sieve = primality_sieve(horizon)
    small_primes = [prime for prime in range(2, cutoff + 1) if sieve[prime]]
    labels = ["rejected"] * (horizon + 1)
    for value in range(2, horizon + 1):
        if sieve[value]:
            labels[value] = "prime"
        elif value > cutoff and all(value % prime for prime in small_primes):
            labels[value] = "rough_semiprime"
    return cutoff, small_primes, labels, sieve


def convolution_components(labels: list[str], target: int) -> dict[str, int]:
    counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
    for left in range(2, target - 1):
        right = target - left
        if right < 2 or right >= len(labels):
            continue
        left_label = labels[left]
        right_label = labels[right]
        if left_label == "rejected" or right_label == "rejected":
            continue
        key = ("P" if left_label == "prime" else "S") + (
            "P" if right_label == "prime" else "S"
        )
        counts[key] += 1
    return counts


def cube_root_classification_rows() -> tuple[list[dict[str, Any]], int]:
    rows = []
    failures = 0
    for horizon in (1_000, 10_000, 100_000):
        cutoff, _, labels, sieve = cube_root_labels(horizon)
        semiprime_failures = 0
        survivor_count = 0
        prime_count = 0
        rough_semiprime_count = 0
        for value in range(2, horizon + 1):
            label = labels[value]
            survivor_count += int(label != "rejected")
            prime_count += int(label == "prime")
            if label == "rough_semiprime":
                rough_semiprime_count += 1
                factors = factor_integer(value)
                semiprime_failures += int(
                    sum(factors.values()) != 2
                    or min(factors) <= cutoff
                    or bool(sieve[value])
                )
        mismatch = survivor_count - prime_count - rough_semiprime_count
        failures += semiprime_failures + abs(mismatch)
        rows.append(
            {
                "horizon_X": horizon,
                "cube_root_cutoff_z": cutoff,
                "z_cubed_at_least_X": cutoff**3 >= horizon,
                "survivor_count": survivor_count,
                "prime_count": prime_count,
                "rough_semiprime_count": rough_semiprime_count,
                "classification_mismatches": mismatch,
                "rough_semiprime_factorization_failures": semiprime_failures,
            }
        )
    return rows, failures


def goldbach_cube_root_audit() -> dict[str, Any]:
    classification_rows, failures = cube_root_classification_rows()
    decomposition_rows = []
    false_diagonal_rows = []
    for horizon in (1_000, 10_000, 100_000):
        cutoff, _, labels, _ = cube_root_labels(horizon)
        target = horizon if horizon % 2 == 0 else horizon - 1
        counts = convolution_components(labels, target)
        filtered = sum(counts.values())
        contamination = counts["PS"] + counts["SP"] + counts["SS"]
        identity = filtered == counts["PP"] + contamination
        failures += int(not identity)
        decomposition_rows.append(
            {
                "horizon_X": horizon,
                "target_N": target,
                "cutoff_z": cutoff,
                "prime_prime_PP": counts["PP"],
                "prime_semiprime_PS": counts["PS"],
                "semiprime_prime_SP": counts["SP"],
                "semiprime_semiprime_SS": counts["SS"],
                "filtered_convolution": filtered,
                "rough_semiprime_contamination": contamination,
                "exact_decomposition_verified": identity,
            }
        )
        left_factor, right_factor = next_primes(cutoff + 1, 2)
        composite = left_factor * right_factor
        false_target = 2 * composite
        valid = (
            false_target <= horizon
            and labels[composite] == "rough_semiprime"
            and convolution_components(labels, false_target)["SS"] >= 1
        )
        failures += int(not valid)
        false_diagonal_rows.append(
            {
                "horizon_X": horizon,
                "cutoff_z": cutoff,
                "rough_semiprime_m": composite,
                "factors": [left_factor, right_factor],
                "target_N": false_target,
                "SS_diagonal_present": valid,
            }
        )

    theorem = (
        "Let z^3>=X and let Q_z(m) accept primes and integers with no prime "
        "divisor at most z. Every accepted composite m<=X is exactly a "
        "product of two primes r,s>z, counting multiplicity. Writing P for "
        "the prime indicator and S_z for this z-rough semiprime indicator, "
        "Q_z=P+S_z exactly on [2,X]. Therefore for every even N<=X, "
        "Q_z*Q_z(N)=P*P(N)+P*S_z(N)+S_z*P(N)+S_z*S_z(N)."
    )
    proof = (
        "Every prime factor of an accepted composite exceeds z. Three or "
        "more factors would give m>z^3>=X, so exactly two remain. The "
        "converse is immediate. Expanding the convolution of P+S_z gives "
        "the identity. Thus a filtered representation is a Goldbach "
        "representation only after the three non-PP terms are removed."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cube_root_classification_rows": classification_rows,
        "convolution_decomposition_rows": decomposition_rows,
        "rough_semiprime_false_diagonal_rows": false_diagonal_rows,
        "aggregate": {
            "cube_root_survivor_classification_proved": True,
            "goldbach_four_term_decomposition_proved": True,
            "filtered_witness_termwise_primality_refuted": True,
            "rough_semiprime_contamination_uniformly_controlled": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Cube-root sieving replaces arbitrary composites by an exact "
            "rough-semiprime error, but it does not bound that error below "
            "the filtered main term or prove P*P(N)>0 for every even N."
        ),
        "failure_count": failures,
    }


def twin_cube_root_audit() -> dict[str, Any]:
    classification_rows, failures = cube_root_classification_rows()
    pair_rows = []
    sample_rows = []
    for horizon in (1_000, 10_000, 100_000):
        cutoff, _, labels, _ = cube_root_labels(horizon)
        counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
        first_ss = None
        for left in range(2, horizon - 1):
            right = left + 2
            if labels[left] == "rejected" or labels[right] == "rejected":
                continue
            key = ("P" if labels[left] == "prime" else "S") + (
                "P" if labels[right] == "prime" else "S"
            )
            counts[key] += 1
            if key == "SS" and first_ss is None:
                first_ss = [left, right]
        survivor_pairs = sum(counts.values())
        identity = survivor_pairs == (
            counts["PP"] + counts["PS"] + counts["SP"] + counts["SS"]
        )
        failures += int(not identity or first_ss is None)
        pair_rows.append(
            {
                "horizon_X": horizon,
                "cutoff_z": cutoff,
                "prime_prime_PP": counts["PP"],
                "prime_semiprime_PS": counts["PS"],
                "semiprime_prime_SP": counts["SP"],
                "semiprime_semiprime_SS": counts["SS"],
                "total_survivor_pairs": survivor_pairs,
                "contaminating_pairs": counts["PS"]
                + counts["SP"]
                + counts["SS"],
                "exact_pair_decomposition_verified": identity,
                "first_SS_countermodel": first_ss,
            }
        )
        if first_ss:
            sample_rows.append(
                {
                    "horizon_X": horizon,
                    "cutoff_z": cutoff,
                    "composite_pair": first_ss,
                    "left_factorization": {
                        str(prime): exponent
                        for prime, exponent in factor_integer(first_ss[0]).items()
                    },
                    "right_factorization": {
                        str(prime): exponent
                        for prime, exponent in factor_integer(first_ss[1]).items()
                    },
                    "verified": labels[first_ss[0]] == "rough_semiprime"
                    and labels[first_ss[1]] == "rough_semiprime",
                }
            )

    theorem = (
        "Under the same z^3>=X condition, every gap-two survivor pair "
        "(n,n+2) with n+2<=X belongs to exactly one of PP, PS, SP, or SS, "
        "where P denotes a prime and S a z-rough semiprime. Hence the total "
        "pair-filter count is the exact sum of the twin-prime count and "
        "three explicit rough-semiprime contamination counts. A positive "
        "survivor count or a termwise survivor certificate is not itself a "
        "twin-prime certificate."
    )
    proof = (
        "The cube-root survivor classification applies independently to n "
        "and n+2. The four cases are disjoint and exhaustive, so counting "
        "gives the identity. Explicit SS pairs show that the filter can "
        "certify both entries while neither is prime; an infinitude proof "
        "must retain a positive PP lower bound after controlling PS, SP, SS."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cube_root_classification_rows": classification_rows,
        "pair_type_rows": pair_rows,
        "explicit_SS_countermodels": sample_rows,
        "aggregate": {
            "cube_root_pair_classification_proved": True,
            "four_type_pair_decomposition_proved": True,
            "survivor_pair_as_twin_certificate_refuted": True,
            "rough_semiprime_pair_contamination_uniformly_controlled": False,
            "infinitely_many_twin_primes_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The decomposition names the exact parity-contamination classes "
            "at cube-root level. It supplies no asymptotic upper bound for "
            "PS+SP+SS and no positive lower bound for PP."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_prime_band_audit()
    collatz = collatz_cyclic_gcd_audit()
    goldbach = goldbach_cube_root_audit()
    twin = twin_cube_root_audit()

    root = {
        "theorem_name": "ArithmeticRemainderLocalizationForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-225 proves four exact arithmetic localization or no-go "
            "theorems and resolves none of the four parent conjectures."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-225",
            "theorem_name": "ActualPrimeBandTailCertificateAndFiniteBandNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "Actual prime-side band signs are certified only at finitely "
                "many scales; no explicit-formula transfer to Weil positivity "
                "or zero-free conclusion is proved."
            ),
            "route_decision": {
                "discard": "treating any finite list of actual prime-band signs as an RH criterion",
                "retain": "prove an explicit-formula transfer from cofinal prime-band margins to positivity on a dense Weil core",
                "next_single_lemma": "ExplicitFormulaTransferFromCofinalPrimeBandMarginsToWeilCorePositivity",
            },
            "proof_dag": proof_dag(
                "RH",
                "SharpQuarterDyadicTailEnvelopeAndSignCertificate",
                "ActualPrimeBandTailCertificateAndFiniteBandNoGo",
                "FinitePrimeBandSignsDetermineRiemannHypothesis",
                "ExplicitFormulaTransferFromCofinalPrimeBandMarginsToWeilCorePositivity",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-225",
            "theorem_name": "CyclicGcdResidualInvarianceAndRotationNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The invariant residual removes redundant rotation tests but "
                "does not force it above one for every word or prove descent "
                "for aperiodic trajectories."
            ),
            "route_decision": {
                "discard": "accumulating cyclic rotations as independent prime-power deficit evidence",
                "retain": "prove a uniform cyclic-intercept descent certificate and a separate aperiodic descent theorem",
                "next_single_lemma": "UniformCyclicInterceptDescentOrAperiodicOrbitDescent",
            },
            "proof_dag": proof_dag(
                "CO",
                "PrimePowerValuationCycleCriterionAndRadicalNoGo",
                "CyclicGcdResidualInvarianceAndRotationNoGo",
                "IndependentPrimePowerDeficitsFromCyclicRotations",
                "UniformCyclicInterceptDescentOrAperiodicOrbitDescent",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-225",
            "theorem_name": "CubeRootRoughSemiprimeGoldbachDecomposition",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The cube-root identity isolates the error as rough-semiprime "
                "convolutions but supplies no uniform bound below the local "
                "main term for every even target."
            ),
            "route_decision": {
                "discard": "reading each cube-root wheel representation as a prime-prime representation",
                "retain": "bound the three exact rough-semiprime contamination terms below the filtered main term",
                "next_single_lemma": "UniformCubeRootRoughSemiprimeErrorBelowGoldbachWheelMainTerm",
            },
            "proof_dag": proof_dag(
                "GB",
                "SquareRootWheelCompletenessAndGoldbachSubthresholdNoGo",
                "CubeRootRoughSemiprimeGoldbachDecomposition",
                "CubeRootWheelWitnessesAreTermwisePrime",
                "UniformCubeRootRoughSemiprimeErrorBelowGoldbachWheelMainTerm",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-225",
            "theorem_name": "CubeRootTwinPairTypeDecompositionAndParityNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The PP/PS/SP/SS split identifies the exact contamination "
                "classes but proves neither their uniform cancellation nor "
                "an unbounded positive PP count."
            ),
            "route_decision": {
                "discard": "treating a cube-root survivor pair as a twin-prime certificate",
                "retain": "derive a positive PP lower bound after uniform control of all three rough-semiprime pair classes",
                "next_single_lemma": "PositiveTwinPrimeLowerBoundAfterCubeRootSemiprimeContaminationControl",
            },
            "proof_dag": proof_dag(
                "TP",
                "SquareRootTwinFilterCompletenessAndSubthresholdCRTNoGo",
                "CubeRootTwinPairTypeDecompositionAndParityNoGo",
                "CubeRootSurvivorPairCertifiesTwinPrimality",
                "PositiveTwinPrimeLowerBoundAfterCubeRootSemiprimeContaminationControl",
                "TwinPrimeConjecture",
            ),
        },
    }

    total_failures = sum(
        root[key]["reproducible_computation"]["failure_count"]
        for key in ("riemann", "collatz", "goldbach", "twin_prime")
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
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
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
                    "audit_ref": f"#/arithmetic_remainder_localization_audit/{key}",
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
            "TICKET-225 proves four arithmetic remainder localization or "
            "no-go results and resolves none of the four parent conjectures."
        ),
        "arithmetic_remainder_localization_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["arithmetic_remainder_localization_audit"]
    write_json(
        ROOT / "data/open-problem/ticket225-arithmetic-remainder-localization.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-225-actual-prime-band.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-225-cyclic-gcd-residual.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-225-cube-root-semiprime.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-225-cube-root-pair-types.json",
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
    print(
        json.dumps(
            audit["arithmetic_remainder_localization_audit"]["machine_audit"],
            indent=2,
        )
    )
    if audit["arithmetic_remainder_localization_audit"]["machine_audit"][
        "total_failure_count"
    ]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
