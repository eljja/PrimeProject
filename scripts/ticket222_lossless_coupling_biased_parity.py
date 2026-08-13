from __future__ import annotations

import hashlib
import itertools
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket222-lossless-coupling-biased-parity.v1"
GENERATED_AT = "2026-08-13T16:00:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal_string(value: Decimal, digits: int = 32) -> str:
    return format(value, f".{digits}E")


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    limited: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T221", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T222", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N222",
                "label": limited,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN222",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T221", f"{prefix}-T222"],
            [f"{prefix}-T222", f"{prefix}-N222"],
            [f"{prefix}-T222", f"{prefix}-OPEN222"],
            [f"{prefix}-OPEN222", prefix],
        ],
    }


def laplace_value(
    atoms: tuple[tuple[Decimal, Decimal], ...], s: Decimal
) -> Decimal:
    return sum(weight * (-(s * height)).exp() for height, weight in atoms)


def dyadic_band_value(
    atoms: tuple[tuple[Decimal, Decimal], ...], index: int
) -> Decimal:
    s = Decimal(2) ** (-index)
    return laplace_value(atoms, s) - laplace_value(atoms, Decimal(2) * s)


def riemann_compact_dyadic_injectivity_audit() -> dict[str, Any]:
    getcontext().prec = 100
    measures = {
        "A": (
            (Decimal(1), Decimal(1)),
            (Decimal(4), Decimal(2)),
            (Decimal(9), Decimal(1)),
        ),
        "B": (
            (Decimal(2), Decimal(1)),
            (Decimal(4), Decimal(2)),
            (Decimal(8), Decimal(1)),
        ),
    }
    profile_rows = []
    failures = 0
    transcript = hashlib.sha256()
    for index in range(-12, 13):
        left = dyadic_band_value(measures["A"], index)
        right = dyadic_band_value(measures["B"], index)
        distinct = abs(left - right) > Decimal("1e-90")
        transcript.update(f"{index}:{left}:{right}\n".encode("ascii"))
        profile_rows.append(
            {
                "dyadic_index_j": index,
                "measure_A_band": decimal_string(left),
                "measure_B_band": decimal_string(right),
                "profiles_distinct_at_this_scale": distinct,
            }
        )

    profiles_differ_somewhere = any(
        row["profiles_distinct_at_this_scale"] for row in profile_rows
    )
    failures += int(not profiles_differ_somewhere)
    telescope_rows = []
    mass = Decimal(4)
    for radius in (2, 4, 8, 12, 16, 24, 32):
        atoms = measures["A"]
        direct = sum(
            dyadic_band_value(atoms, index)
            for index in range(-radius, radius + 1)
        )
        boundary = laplace_value(atoms, Decimal(2) ** (-radius)) - (
            laplace_value(atoms, Decimal(2) ** (radius + 1))
        )
        identity = abs(direct - boundary) < Decimal("1e-85")
        failures += int(not identity)
        telescope_rows.append(
            {
                "radius_R": radius,
                "finite_band_sum": decimal_string(direct),
                "telescoping_boundary": decimal_string(boundary),
                "distance_to_total_mass_four": decimal_string(abs(mass - direct)),
                "telescoping_identity_verified": identity,
            }
        )

    theorem = (
        "Let sigma be a finite signed Borel measure supported in a compact "
        "interval [a,b] with 0<a<b, let L_sigma(s)=integral exp(-st) "
        "d sigma(t), and let W_j=L_sigma(2^(-j))-L_sigma(2^(1-j)). If "
        "W_j=0 for every integer j, then sigma=0. Consequently the complete "
        "two-sided dyadic Laplace-band profile is injective on compactly "
        "supported defect measures away from height zero."
    )
    proof = (
        "Write s_j=2^(-j). The equations W_j=0 give "
        "L_sigma(s_j)=L_sigma(s_(j-1)), so all dyadic samples have one "
        "common value. As j tends to minus infinity, s_j tends to infinity; "
        "support in [a,b] with a>0 forces L_sigma(s_j) to zero. Hence every "
        "dyadic sample is zero. Compact support makes L_sigma an entire "
        "function, and the zeros s_j accumulate at the interior point zero, "
        "so the identity theorem gives L_sigma identically zero. Its "
        "derivatives at zero show that every polynomial moment vanishes; "
        "polynomial density in C[a,b] then gives sigma=0. This proves "
        "information sufficiency of the infinite coupled profile, not an "
        "actual-zeta prime-side enclosure or control of unbounded support."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "hypotheses": {
            "measure_class": "finite signed Borel measures",
            "support": "compact [a,b] with 0<a<b",
            "observations": "all W_j for every j in Z",
        },
        "finite_atomic_profile_rows": profile_rows,
        "finite_telescoping_rows": telescope_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "compact_full_dyadic_profile_injectivity_proved": True,
            "finite_example_profiles_differ_somewhere": profiles_differ_somewhere,
            "finite_window_injectivity_claimed": False,
            "unbounded_actual_zeta_defect_support_controlled": False,
            "prime_side_arithmetic_enclosure_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem positively identifies a lossless coupled observable "
            "on compact support. It does not extend by itself to an unbounded "
            "defect measure, and no finite subset of bands is promoted to an "
            "infinite certificate."
        ),
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    return (value & -value).bit_length() - 1


def collatz_intercept(word: tuple[int, ...]) -> int:
    height = len(word)
    prefix = 0
    total = 0
    for index, valuation in enumerate(word):
        total += (3 ** (height - index - 1)) * (2**prefix)
        prefix += valuation
    return total


def decode_collatz_word(height: int, total: int, intercept: int) -> tuple[int, ...]:
    if height <= 0 or total <= 0 or intercept <= 0:
        raise ValueError("positive height, total, and intercept required")
    current = intercept
    decoded: list[int] = []
    for remaining in range(height, 1, -1):
        difference = current - 3 ** (remaining - 1)
        if difference <= 0:
            raise ValueError("invalid affine intercept code")
        valuation = v2(difference)
        if valuation <= 0:
            raise ValueError("valuation words use positive exponents")
        decoded.append(valuation)
        current = difference // (2**valuation)
    final_valuation = total - sum(decoded)
    if current != 1 or final_valuation <= 0:
        raise ValueError("inconsistent total valuation or terminal intercept")
    decoded.append(final_valuation)
    return tuple(decoded)


def rotate_word(word: tuple[int, ...]) -> tuple[int, ...]:
    return word[1:] + word[:1]


def collatz_cycle_replay(word: tuple[int, ...]) -> dict[str, Any]:
    total = sum(word)
    intercept = collatz_intercept(word)
    denominator = 2**total - 3 ** len(word)
    divisible = denominator > 0 and intercept % denominator == 0
    exact_cycle = False
    start = None
    if divisible:
        start = intercept // denominator
        value = start
        exact_cycle = value > 0 and value % 2 == 1
        for valuation in word:
            numerator = 3 * value + 1
            exact_cycle = exact_cycle and v2(numerator) == valuation
            value = numerator // (2**valuation)
        exact_cycle = exact_cycle and value == start
    return {
        "word": list(word),
        "height_h": len(word),
        "total_valuation_S": total,
        "intercept_B": intercept,
        "denominator_D": denominator,
        "D_divides_B": divisible,
        "cycle_start": start,
        "exact_cycle_replay": exact_cycle,
    }


def collatz_lossless_code_audit() -> dict[str, Any]:
    alphabet = range(1, 6)
    enumeration_rows = []
    sample_rows = []
    transcript = hashlib.sha256()
    failures = 0
    total_words = 0
    total_divisible = 0

    samples = (
        (1,),
        (2,),
        (1, 2, 3, 4),
        (3, 4, 2, 1),
        (1, 1, 4, 2, 3),
        (5, 1, 2, 4, 3, 2),
    )
    for word in samples:
        intercept = collatz_intercept(word)
        decoded = decode_collatz_word(len(word), sum(word), intercept)
        replay = collatz_cycle_replay(word)
        replay["decoded_word"] = list(decoded)
        replay["decode_matches"] = decoded == word
        failures += int(decoded != word)
        sample_rows.append(replay)

    for height in range(1, 9):
        seen: dict[tuple[int, int], tuple[int, ...]] = {}
        collision_count = 0
        decode_failures = 0
        contracting_count = 0
        divisible_count = 0
        exact_cycle_failures = 0
        for word in itertools.product(alphabet, repeat=height):
            total = sum(word)
            intercept = collatz_intercept(word)
            key = (total, intercept)
            if key in seen and seen[key] != word:
                collision_count += 1
            else:
                seen[key] = word
            try:
                decoded = decode_collatz_word(height, total, intercept)
            except ValueError:
                decoded = ()
            if decoded != word:
                decode_failures += 1
            denominator = 2**total - 3**height
            if denominator > 0:
                contracting_count += 1
                if intercept % denominator == 0:
                    divisible_count += 1
                    if not collatz_cycle_replay(word)["exact_cycle_replay"]:
                        exact_cycle_failures += 1
            transcript.update(
                f"{height}:{','.join(map(str, word))}:{total}:{intercept}\n".encode(
                    "ascii"
                )
            )
        words = 5**height
        total_words += words
        total_divisible += divisible_count
        failures += collision_count + decode_failures + exact_cycle_failures
        enumeration_rows.append(
            {
                "height_h": height,
                "words_checked": words,
                "distinct_S_B_codes": len(seen),
                "code_collision_count": collision_count,
                "decode_failure_count": decode_failures,
                "contracting_word_count": contracting_count,
                "D_divides_B_count": divisible_count,
                "divisible_but_exact_replay_failure_count": exact_cycle_failures,
            }
        )

    theorem = (
        "For every positive accelerated Collatz valuation word "
        "a=(a_1,...,a_h), the triple (h,S,B), where S=sum a_i and "
        "B=sum_i 3^(h-i)2^(a_1+...+a_(i-1)), determines a uniquely. "
        "Indeed a_1=v_2(B-3^(h-1)); division recovers the tail intercept, "
        "and recursion recovers a_1,...,a_(h-1), while S recovers a_h. "
        "Together with D=2^S-3^h, D>0 and D|B are equivalent to this "
        "ordered word realizing a positive accelerated integer cycle."
    )
    proof = (
        "The affine constant satisfies B_h(a)=3^(h-1)+2^(a_1) "
        "B_(h-1)(a_2,...,a_h). Every tail intercept is odd, so the exact "
        "2-adic valuation of B_h-3^(h-1) is a_1. Repeating recovers all "
        "but the final exponent, which is S minus the recovered prefix. "
        "For the cycle criterion, cyclic intercepts satisfy "
        "2^(a_i)B_(i+1)=3B_i+D. Since gcd(D,6)=1, divisibility by D is "
        "rotation invariant. If D|B, all n_i=B_i/D are positive odd "
        "integers and 3n_i+1=2^(a_i)n_(i+1), so the displayed exponent is "
        "the exact 2-adic valuation and the orbit closes. The converse is "
        "the affine fixed-point equation. This closes information recovery "
        "and cycle admissibility, but neither excludes all nontrivial codes "
        "nor controls aperiodic divergence."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "decode_recurrence": (
            "a_1=v2(B_h-3^(h-1)); B_tail=(B_h-3^(h-1))/2^a_1; "
            "a_h=S-sum_(i<h)a_i"
        ),
        "sample_lossless_decode_rows": sample_rows,
        "finite_complete_alphabet_rows": enumeration_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "valuation_alphabet": "1..5",
            "maximum_height": 8,
            "total_words_checked": total_words,
            "total_code_collisions": sum(
                row["code_collision_count"] for row in enumeration_rows
            ),
            "total_decode_failures": sum(
                row["decode_failure_count"] for row in enumeration_rows
            ),
            "total_divisible_codes": total_divisible,
            "slope_intercept_code_injectivity_proved": True,
            "exact_cycle_divisibility_reduction_proved": True,
            "all_nontrivial_codes_excluded": False,
            "aperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The finite enumeration is only a replay. The symbolic decoding "
            "and D|B equivalence hold for every finite positive word, but they "
            "turn cycle exclusion into an all-code divisibility problem rather "
            "than solve it, and they do not address divergent nonperiodic rays."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> tuple[list[int], bytearray]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )
    return [value for value in range(2, limit + 1) if flags[value]], flags


def goldbach_count_parity_audit(limit: int = 100_000) -> dict[str, Any]:
    primes, flags = prime_sieve(limit)
    odd_primes = [prime for prime in primes if prime != 2]
    ordered_counts = [0] * (limit + 1)
    for left_index, left in enumerate(odd_primes):
        if 2 * left > limit:
            break
        for right in odd_primes[left_index:]:
            target = left + right
            if target > limit:
                break
            ordered_counts[target] += 1 if left == right else 2

    parity_failures = 0
    zero_count = 0
    even_positive_count = 0
    odd_positive_count = 0
    parity_zero_positive_examples = []
    transcript = hashlib.sha256()
    for target in range(6, limit + 1, 2):
        count = ordered_counts[target]
        expected_parity = int(bool(flags[target // 2]))
        parity_failures += int(count % 2 != expected_parity)
        zero_count += int(count == 0)
        even_positive_count += int(count > 0 and count % 2 == 0)
        odd_positive_count += int(count % 2 == 1)
        if count > 0 and count % 2 == 0 and len(parity_zero_positive_examples) < 16:
            parity_zero_positive_examples.append(
                {
                    "even_target_N": target,
                    "ordered_odd_prime_representation_count": count,
                    "N_over_2": target // 2,
                    "N_over_2_is_prime": bool(flags[target // 2]),
                    "parity_bit": count % 2,
                }
            )
        transcript.update(f"{target}:{count}\n".encode("ascii"))

    theorem = (
        "For every even N>=6, let R_ord(N) count ordered pairs of odd "
        "primes (p,q) with p+q=N. Then R_ord(N) modulo 2 equals "
        "1_P(N/2). Off-diagonal representations occur in swapped pairs, "
        "and the only fixed point of the swap is p=q=N/2. Therefore the "
        "parity of the Goldbach representation count detects only the "
        "diagonal representation and cannot distinguish zero from a positive "
        "even number of off-diagonal representations."
    )
    proof = (
        "The involution (p,q)->(q,p) partitions all ordered representations "
        "into two-element orbits except when p=q. A fixed point exists "
        "exactly when N/2 is an odd prime, proving the congruence. For N=20, "
        "the four ordered representations (3,17),(17,3),(7,13),(13,7) "
        "already show that parity zero is compatible with strict positivity. "
        "Thus a parity-only replacement for the TICKET-221 cofinal Lp margin "
        "is refuted; an arithmetic one-sided lower bound remains necessary."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_exact_scan": {
            "limit": limit,
            "even_targets_checked": (limit - 4) // 2,
            "parity_identity_failures": parity_failures,
            "zero_representation_count": zero_count,
            "positive_even_parity_count": even_positive_count,
            "positive_odd_parity_count": odd_positive_count,
            "parity_zero_positive_examples": parity_zero_positive_examples,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "ordered_count_parity_identity_proved": True,
            "count_parity_is_zero_detector_refuted": True,
            "finite_scan_counterexamples": zero_count,
            "cofinal_positive_lower_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem refutes only parity of the representation count as a "
            "positivity certificate. It does not weaken phase-resolved circle "
            "methods, singular-series lower bounds, or direct exception-count "
            "estimates. The finite scan is far below the published 4e18 "
            "verification and is included only to replay the identity."
        ),
        "failure_count": parity_failures,
    }


def product(values: Iterable[Fraction]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def twin_biased_parity_audit() -> dict[str, Any]:
    wheel_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
    prefix_rows = []
    failures = 0
    for size in range(2, len(wheel_primes) + 1):
        primes = wheel_primes[:size]
        means = {prime: Fraction(prime - 4, prime) for prime in primes}
        fixed_degree = min(3, size - 1)
        correlations = []
        for selected in itertools.combinations(primes, fixed_degree):
            selected_set = set(selected)
            correlation = product(
                means[prime] for prime in primes if prime not in selected_set
            )
            correlations.append(abs(correlation))
        constant_correlation = product(means.values())
        proper_nonzero = all(
            product(means[prime] for prime in primes if prime not in selected)
            != 0
            for degree in range(size)
            for selected in map(set, itertools.combinations(primes, degree))
        )
        failures += int(not proper_nonzero)
        prefix_rows.append(
            {
                "wheel_prime_count_m": size,
                "largest_wheel_prime": primes[-1],
                "constant_parity_correlation": fraction_string(
                    constant_correlation
                ),
                "constant_parity_correlation_abs_decimal": float(
                    abs(constant_correlation)
                ),
                "audited_fixed_degree_d": fixed_degree,
                "minimum_degree_d_correlation_abs": fraction_string(
                    min(correlations)
                ),
                "maximum_degree_d_correlation_abs": fraction_string(
                    max(correlations)
                ),
                "every_proper_uncentered_monomial_correlation_nonzero": (
                    proper_nonzero
                ),
                "full_degree_correlation": "1/1",
            }
        )

    exact_primes = wheel_primes[:4]
    modulus = 1
    for prime in exact_primes:
        modulus *= prime
    crt_rows = []
    for mask in range(1 << len(exact_primes)):
        selected = {
            prime
            for index, prime in enumerate(exact_primes)
            if mask & (1 << index)
        }
        total = 0
        for residue in range(modulus):
            signs = {
                prime: (-1 if residue % prime == 0 or (residue + 2) % prime == 0 else 1)
                for prime in exact_primes
            }
            parity = 1
            monomial = 1
            for prime in exact_primes:
                parity *= signs[prime]
                if prime in selected:
                    monomial *= signs[prime]
            total += parity * monomial
        empirical = Fraction(total, modulus)
        predicted = product(
            Fraction(prime - 4, prime)
            for prime in exact_primes
            if prime not in selected
        )
        identity = empirical == predicted
        failures += int(not identity)
        crt_rows.append(
            {
                "selected_prime_subset": sorted(selected),
                "degree": len(selected),
                "exact_crt_correlation": fraction_string(empirical),
                "product_bias_prediction": fraction_string(predicted),
                "identity_verified": identity,
            }
        )

    theorem = (
        "Let q_1,...,q_m be distinct odd primes and choose n uniformly "
        "modulo W=product q_i. Put X_q(n)=-1 when q divides n(n+2) and "
        "+1 otherwise, and P=product_q X_q. CRT makes the X_q independent "
        "with mean mu_q=1-4/q. For every subset S, "
        "E[P product_(q in S)X_q]=product_(q not in S)mu_q. Thus, unlike "
        "the balanced cube of TICKET-221, finite-wheel divisibility parity "
        "has nonzero leakage into every proper uncentered degree because no "
        "odd prime has mu_q=0. The leakage from a fixed-degree observable is "
        "exactly attenuated by the product of all omitted local biases."
    )
    proof = (
        "For one odd prime q, exactly the two residues 0 and -2 make "
        "q divide n(n+2), so E[X_q]=(q-2-2)/q=1-4/q. The Chinese remainder "
        "theorem identifies uniform residues modulo W with the product of "
        "uniform residues modulo each q, proving independence. In the "
        "product P times the S-monomial, coordinates in S occur squared and "
        "contribute one; every omitted coordinate contributes its mean. "
        "This corrects, rather than solves, the balanced Boolean stress "
        "model: local bias creates signal, but proving a positive gap-two "
        "prime correlation still requires a scale-growing arithmetic "
        "Type-II estimate and control of the omitted-prime tail."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "bias_formula": "mu_q=1-4/q; correlation(S)=product_(q notin S)mu_q",
        "wheel_prefix_rows": prefix_rows,
        "exact_crt_enumeration": {
            "primes": list(exact_primes),
            "modulus_W": modulus,
            "subset_rows": crt_rows,
        },
        "aggregate": {
            "crt_product_independence_proved": True,
            "biased_parity_leakage_formula_proved": True,
            "balanced_orthogonality_applies_to_actual_finite_wheel": False,
            "proper_uncentered_correlations_all_nonzero": True,
            "arithmetic_type_ii_pair_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem is exact for divisibility signs under a finite "
            "squarefree wheel. P is parity of selected small-prime divisors, "
            "not the full prime indicator. Nonzero leakage is not a positive "
            "lower bound for Lambda(n)Lambda(n+2), and fixed wheels remain "
            "subject to CRT composite-pair countermodels."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_compact_dyadic_injectivity_audit()
    collatz_compute = collatz_lossless_code_audit()
    goldbach_compute = goldbach_count_parity_audit()
    twin_compute = twin_biased_parity_audit()

    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-222",
            "theorem_name": "CompactSupportFullDyadicLaplaceProfileInjectivity",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": (
                "No tail-tight actual-zeta prime-side enclosure is proved for "
                "the unbounded defect class required by RH."
            ),
            "route_decision": {
                "discard": (
                    "treating the full coupled dyadic profile as intrinsically "
                    "information-losing on compact positive-height defects"
                ),
                "retain": (
                    "construct an actual prime-side enclosure on a cofinal "
                    "compact exhaustion with a rigorously vanishing tail"
                ),
                "next_single_lemma": "ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail",
            },
            "proof_dag": proof_dag(
                "RH",
                "ScaleUniformDyadicEnvelopeDivergenceNoGo",
                "CompactSupportFullDyadicLaplaceProfileInjectivity",
                "CompactInjectivityControlsUnboundedActualZetaTail",
                "ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail",
                "Riemann Hypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-222",
            "theorem_name": "SlopeInterceptLosslessValuationCodeAndExactCycleReduction",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": (
                "The lossless code does not prove D does not divide B for all "
                "nontrivial primitive words and does not exclude divergent rays."
            ),
            "route_decision": {
                "discard": (
                    "adding more unordered or scalar Baker summaries after "
                    "the exact ordered intercept is already available"
                ),
                "retain": (
                    "attack all non-all-two primitive (h,S,B) codes by exact "
                    "divisibility or prove first descent on every aperiodic ray"
                ),
                "next_single_lemma": "AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends",
            },
            "proof_dag": proof_dag(
                "CO",
                "OrderBlindLogarithmicSeparationNoGoForPrimitiveWords",
                "SlopeInterceptLosslessValuationCodeAndExactCycleReduction",
                "LosslessCodingExcludesEveryNontrivialCodeOrDivergentRay",
                "AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends",
                "Collatz Conjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-222",
            "theorem_name": "OrderedGoldbachCountParityEqualsDiagonalPrimeIndicator",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": (
                "No all-large-even arithmetic lower bound or exception-count "
                "estimate below one is proved."
            ),
            "route_decision": {
                "discard": (
                    "using the parity bit of the ordered representation count "
                    "as a zero-versus-positive detector"
                ),
                "retain": (
                    "prove a one-sided positive lower bound for the full "
                    "representation count or a strict subunit tail exception bound"
                ),
                "next_single_lemma": "UniformCofinalPositiveGoldbachCountLowerBound",
            },
            "proof_dag": proof_dag(
                "GB",
                "SharpLpDistanceToGoldbachZeroSet",
                "OrderedGoldbachCountParityEqualsDiagonalPrimeIndicator",
                "RepresentationCountParityDetectsGoldbachPositivity",
                "UniformCofinalPositiveGoldbachCountLowerBound",
                "Strong Goldbach Conjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-222",
            "theorem_name": "FiniteWheelBiasedParityLeakageProductFormula",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": (
                "Finite-wheel parity leakage is not a lower bound for the "
                "shift-two von Mangoldt correlation and does not control the tail."
            ),
            "route_decision": {
                "discard": (
                    "applying balanced-cube exact orthogonality literally to "
                    "biased finite-wheel divisibility variables"
                ),
                "retain": (
                    "quantify scale-growing biased parity signal and prove it "
                    "dominates the signed arithmetic Type-II remainder"
                ),
                "next_single_lemma": "ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder",
            },
            "proof_dag": proof_dag(
                "TP",
                "LowDegreeBooleanParityOrthogonalityNoGo",
                "FiniteWheelBiasedParityLeakageProductFormula",
                "NonzeroFiniteWheelLeakageImpliesPositiveTwinCorrelation",
                "ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder",
                "Twin Prime Conjecture",
            ),
        },
    }

    machine_audit = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(
            section["reproducible_computation"]["failure_count"]
            for section in sections.values()
        ),
    }
    audit = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-222 proves four exact information-recovery or parity-"
            "correction theorems and resolves none of the four parent conjectures."
        ),
        "lossless_coupling_biased_parity_audit": {
            "theorem_name": "LosslessCouplingAndBiasedParityCorrectionsForFourOpenProblems",
            "status": STATUS,
            "proof_boundary": (
                "The results identify which coupled observables are lossless and "
                "which parity inferences fail. They prove no parent conjecture."
            ),
            **sections,
            "cross_problem_synthesis": (
                "TICKET-222 moves beyond information-loss no-go statements: "
                "the complete compact RH dyadic profile and Collatz (h,S,B) "
                "code are lossless, while Goldbach count parity is too coarse "
                "and finite-wheel Twin parity is biased rather than orthogonal. "
                "The remaining work is now explicitly arithmetic and cofinal."
            ),
            "literature_boundary": {
                "riemann": (
                    "Weil positivity and the Connes-Consani semi-local program "
                    "motivate coupled test data; compact Laplace injectivity here "
                    "is an elementary project theorem, not an RH advance."
                ),
                "collatz": (
                    "Classical accelerated-map affine coding and Tao's almost-all "
                    "descent boundary remain external context; the recursive "
                    "intercept decoder does not promote density to every orbit."
                ),
                "goldbach": (
                    "Published verification through 4e18 is much stronger than "
                    "the finite replay. The swap-parity identity is algebraic and "
                    "does not improve the verified range or exceptional-set bounds."
                ),
                "twin_prime": (
                    "Ford-Maynard Type-I/II theory shows why substantial Type-II "
                    "information matters for prime-producing lower bounds. The "
                    "finite-wheel bias formula is not such a lower bound."
                ),
            },
            "machine_audit": machine_audit,
        },
        "attempts": [],
    }

    for section in sections.values():
        route = section["route_decision"]
        audit["attempts"].append(
            {
                "problem_id": section["problem_id"],
                "ticket_id": section["ticket_id"],
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": "#/lossless_coupling_biased_parity_audit",
                    "failure_count": section["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": route["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": route["next_single_lemma"],
                "proof_dag": section["proof_dag"],
            }
        )
    return audit


def write_outputs(audit: dict[str, Any]) -> None:
    integrated_path = (
        ROOT / "data/open-problem/ticket222-lossless-coupling-biased-parity.json"
    )
    write_json(integrated_path, audit)
    section_root = audit["lossless_coupling_biased_parity_audit"]
    track_paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-222-compact-dyadic-injectivity.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-222-lossless-intercept-code.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-222-count-parity.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-222-biased-parity-leakage.json",
    }
    for key, path in track_paths.items():
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **section_root[key],
            },
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["lossless_coupling_biased_parity_audit"]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
