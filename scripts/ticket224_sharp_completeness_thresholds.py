from __future__ import annotations

import hashlib
import itertools
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket224-sharp-completeness-thresholds.v1"
GENERATED_AT = "2026-08-14T20:00:00+09:00"
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
            {"id": f"{prefix}-T223", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T224", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N224",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN224",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T223", f"{prefix}-T224"],
            [f"{prefix}-T224", f"{prefix}-N224"],
            [f"{prefix}-T224", f"{prefix}-OPEN224"],
            [f"{prefix}-OPEN224", prefix],
        ],
    }


def geometric_tail(ratio: Decimal, cutoff: int) -> Decimal:
    return ratio ** (cutoff + 1) / (Decimal(1) - ratio)


def riemann_sharp_tail_audit() -> dict[str, Any]:
    getcontext().prec = 100
    eta = Decimal(2).ln()
    quarter = Decimal(1) / Decimal(4)
    rows = []
    sharp_rows = []
    failures = 0
    transcript = hashlib.sha256()

    for cutoff in (4, 8, 12, 16, 24, 32):
        sharp_bound = quarter * (-eta * cutoff).exp()
        band_tails = []
        for index in range(-8, 15):
            s = Decimal(2) ** (-index)
            first_ratio = -(Decimal(4) ** -1) * (-s).exp()
            second_ratio = -(Decimal(4) ** -1) * (-(Decimal(2) * s)).exp()
            tail = geometric_tail(first_ratio, cutoff) - geometric_tail(
                second_ratio, cutoff
            )
            band_tails.append(abs(tail))
            transcript.update(f"{cutoff}:{index}:{tail}\n".encode("ascii"))
        maximum = max(band_tails)
        verified = maximum <= sharp_bound
        failures += int(not verified)
        rows.append(
            {
                "cutoff_T": cutoff,
                "maximum_observed_band_tail": format(maximum, ".30E"),
                "sharp_quarter_exponential_bound": format(sharp_bound, ".30E"),
                "bound_verified": verified,
            }
        )

    for index in range(0, 9):
        scale = Decimal(2) ** (-index)
        support = (Decimal(2) ** index) * Decimal(2).ln()
        atom_mass = (-eta * support).exp()
        kernel = (-scale * support).exp() - (
            -Decimal(2) * scale * support
        ).exp()
        band = atom_mass * kernel
        bound = quarter * (-eta * support).exp()
        equality = band == bound and kernel == quarter
        failures += int(not equality)
        sharp_rows.append(
            {
                "dyadic_index_j": index,
                "support_T": format(support, ".30E"),
                "unit_weighted_norm_atom_mass": format(atom_mass, ".30E"),
                "band_kernel": format(kernel, ".30E"),
                "band_value": format(band, ".30E"),
                "quarter_bound": format(bound, ".30E"),
                "equality_verified": equality,
            }
        )

    theorem = (
        "Let sigma be a finite signed Borel measure on (0,infinity) with "
        "finite norm ||sigma||_eta=integral exp(eta t)d|sigma|(t), eta>0. "
        "For W_j(sigma)=integral (exp(-2^(-j)t)-exp(-2^(1-j)t)) "
        "d sigma(t), the tail sigma restricted to [T,infinity) satisfies "
        "sup_j |W_j| <= (1/4) exp(-eta T)||sigma||_eta. The constant "
        "1/4 is optimal uniformly: equality holds for a suitably normalized "
        "atom at T=2^j log 2. Consequently a truncated band has a certified "
        "full-band sign whenever its absolute margin is strictly greater "
        "than this sharp tail envelope."
    )
    proof = (
        "For u>0, k(u)=exp(-u)-exp(-2u). Differentiation gives its unique "
        "maximum k(log 2)=1/4. Therefore the absolute tail band is at most "
        "one quarter of the tail total variation, which is at most "
        "exp(-eta T)||sigma||_eta/4. For T=2^j log 2, the measure "
        "exp(-eta T) delta_T has weighted norm one and attains equality at "
        "dyadic scale 2^(-j). The triangle inequality proves the strict "
        "sign-margin certificate, while the extremal atom shows that a "
        "uniformly smaller envelope is impossible."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "kernel_optimization": {
            "kernel": "k(u)=exp(-u)-exp(-2u)",
            "maximizer": "u=log(2)",
            "maximum": "1/4",
        },
        "model_tail_rows": rows,
        "sharpness_rows": sharp_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "sharp_quarter_tail_envelope_proved": True,
            "uniform_constant_optimality_proved": True,
            "strict_sign_margin_certificate_proved": True,
            "actual_zeta_prime_side_margin_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "TICKET-223's factor-one envelope is not sharp; factor one "
            "quarter is optimal for this band kernel. The theorem remains "
            "abstract and supplies no RH-equivalent zeta defect or "
            "prime-side lower margin."
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


def valuation(value: int, prime: int) -> int:
    exponent = 0
    while value % prime == 0:
        exponent += 1
        value //= prime
    return exponent


def collatz_prime_power_audit() -> dict[str, Any]:
    witness_word = (1, 1, 2, 4, 3)
    witness_sum = sum(witness_word)
    witness_d = 2**witness_sum - 3 ** len(witness_word)
    witness_b = collatz_intercept(witness_word)
    witness_factors = factor_integer(witness_d)
    witness_radical = math.prod(witness_factors)
    witness_rows = [
        {
            "prime_q": prime,
            "v_q_D": exponent,
            "v_q_B": valuation(witness_b, prime),
            "prime_power_condition_passes": valuation(witness_b, prime)
            >= exponent,
        }
        for prime, exponent in witness_factors.items()
    ]

    failures = 0
    words_checked = 0
    primitive_positive_words = 0
    criterion_mismatches = 0
    radical_false_positives = []
    for height in range(2, 6):
        for word in itertools.product(range(1, 5), repeat=height):
            words_checked += 1
            exponent_sum = sum(word)
            denominator = 2**exponent_sum - 3**height
            if denominator <= 0 or not is_primitive_word(word):
                continue
            primitive_positive_words += 1
            intercept = collatz_intercept(word)
            factors = factor_integer(denominator)
            criterion = all(
                valuation(intercept, prime) >= exponent
                for prime, exponent in factors.items()
            )
            exact = intercept % denominator == 0
            criterion_mismatches += int(criterion != exact)
            radical = math.prod(factors)
            if intercept % radical == 0 and not exact:
                radical_false_positives.append(
                    {
                        "valuation_word": list(word),
                        "D": denominator,
                        "B": intercept,
                        "rad_D": radical,
                        "factorization_D": {
                            str(prime): exponent
                            for prime, exponent in factors.items()
                        },
                    }
                )

    explicit_valid = (
        witness_d == 1805
        and witness_b == 475
        and witness_factors == {5: 1, 19: 2}
        and witness_radical == 95
        and witness_b % witness_radical == 0
        and witness_b % witness_d != 0
        and is_primitive_word(witness_word)
    )
    failures += criterion_mismatches
    failures += int(not explicit_valid)
    failures += int(not radical_false_positives)

    theorem = (
        "For any positive accelerated Collatz valuation word with "
        "D=2^S-3^h>0 and intercept B, the exact finite-cycle condition "
        "D|B is equivalent to v_q(B)>=v_q(D) for every prime q dividing D. "
        "Thus every failed cycle has a prime-power valuation-deficit "
        "certificate. Checking only rad(D)|B is insufficient: the primitive "
        "word (1,1,2,4,3) has D=1805=5*19^2 and B=475=5^2*19, so rad(D)=95 "
        "divides B but D does not."
    )
    proof = (
        "Unique factorization gives D|B exactly when each prime exponent in "
        "D is no larger than the corresponding exponent in B. The stated "
        "word has S=11 and h=5, hence D=2^11-3^5=1805. Direct evaluation "
        "of the affine intercept gives B=475. Its length is prime and it is "
        "nonconstant, hence primitive. The displayed factorizations prove "
        "radical divisibility and exhibit the missing second power of 19."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "explicit_radical_false_positive": {
            "valuation_word": list(witness_word),
            "primitive": is_primitive_word(witness_word),
            "S": witness_sum,
            "h": len(witness_word),
            "D": witness_d,
            "B": witness_b,
            "factorization_D": {
                str(prime): exponent
                for prime, exponent in witness_factors.items()
            },
            "rad_D": witness_radical,
            "rad_D_divides_B": witness_b % witness_radical == 0,
            "D_divides_B": witness_b % witness_d == 0,
            "valuation_rows": witness_rows,
            "verified": explicit_valid,
        },
        "finite_audit": {
            "heights": [2, 3, 4, 5],
            "alphabet": [1, 2, 3, 4],
            "words_checked": words_checked,
            "primitive_positive_words": primitive_positive_words,
            "prime_power_criterion_mismatches": criterion_mismatches,
            "radical_false_positive_count": len(radical_false_positives),
            "sample_radical_false_positives": radical_false_positives[:12],
        },
        "aggregate": {
            "prime_power_cycle_criterion_proved": True,
            "radical_only_sufficiency_refuted": True,
            "explicit_primitive_counterexample_verified": explicit_valid,
            "all_nontrivial_cycles_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact adaptive test must retain prime multiplicities. Full "
            "factorization of D merely restates D|B and does not uniformly "
            "exclude nontrivial words or control aperiodic trajectories."
        ),
        "failure_count": failures,
    }


def primes_through(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for value in range(2, math.isqrt(limit) + 1):
        if sieve[value]:
            for multiple in range(value * value, limit + 1, value):
                sieve[multiple] = False
    return [value for value, prime in enumerate(sieve) if prime]


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


def wheel_filter(value: int, cutoff: int, primes: list[int] | None = None) -> bool:
    if value < 2:
        return False
    if value <= cutoff:
        return is_prime(value)
    local_primes = primes if primes is not None else primes_through(cutoff)
    return all(value % prime != 0 for prime in local_primes)


def ordered_goldbach_count(target: int, predicate: Any) -> int:
    return sum(
        1
        for left in range(2, target - 1)
        if predicate(left) and predicate(target - left)
    )


def square_root_filter_rows() -> tuple[list[dict[str, Any]], int]:
    rows = []
    failures = 0
    for horizon in (100, 1_000, 10_000, 100_000):
        cutoff = math.isqrt(horizon)
        if cutoff * cutoff < horizon:
            cutoff += 1
        primes = primes_through(cutoff)
        mismatches = sum(
            wheel_filter(value, cutoff, primes) != is_prime(value)
            for value in range(2, horizon + 1)
        )
        failures += mismatches
        rows.append(
            {
                "horizon_X": horizon,
                "cutoff_z": cutoff,
                "prime_count_through_z": len(primes),
                "integers_checked": horizon - 1,
                "primality_filter_mismatches": mismatches,
                "exactness_verified": mismatches == 0,
            }
        )
    return rows, failures


def goldbach_square_root_audit() -> dict[str, Any]:
    exact_rows, failures = square_root_filter_rows()
    false_rows = []
    for cutoff in (3, 5, 7, 11, 17, 29):
        primes = primes_through(cutoff)
        left_factor, right_factor = next_primes(cutoff + 1, 2)
        composite = left_factor * right_factor
        target = 2 * composite
        actual = ordered_goldbach_count(target, is_prime)
        filtered = ordered_goldbach_count(
            target, lambda value: wheel_filter(value, cutoff, primes)
        )
        valid = (
            not is_prime(composite)
            and wheel_filter(composite, cutoff, primes)
            and filtered > actual
            and cutoff < math.sqrt(target)
        )
        failures += int(not valid)
        false_rows.append(
            {
                "cutoff_z": cutoff,
                "external_factors": [left_factor, right_factor],
                "composite_m": composite,
                "even_target_N": target,
                "actual_ordered_goldbach_count": actual,
                "filtered_ordered_pair_count": filtered,
                "false_positive_excess": filtered - actual,
                "z_below_sqrt_N": cutoff < math.sqrt(target),
                "diagonal_false_positive_verified": valid,
            }
        )

    theorem = (
        "Define Q_z(m) to be exact primality for m<=z and, for m>z, the "
        "condition that m has no prime divisor at most z. If z>=sqrt(X), "
        "then Q_z(m) is equivalent to primality for every 2<=m<=X; hence "
        "for every even N<=X the Q_z ordered representation count equals "
        "the exact Goldbach count. This threshold cannot be replaced by an "
        "arbitrary fixed wheel: for primes r,s>z, m=rs passes Q_z although "
        "composite, and N=2m contains the false diagonal pair (m,m)."
    )
    proof = (
        "Every composite m<=X has a prime divisor at most sqrt(m), hence at "
        "most sqrt(X)<=z; Q_z rejects it, while it accepts every prime. "
        "Substitution in the ordered convolution proves count equality. "
        "Conversely, if r and s are primes above z, no sieving prime divides "
        "m=rs. The filtered convolution for 2m contains all genuine prime "
        "representations plus the nonprime diagonal, so it strictly exceeds "
        "the true count."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "square_root_exactness_rows": exact_rows,
        "subthreshold_false_positive_rows": false_rows,
        "aggregate": {
            "square_root_wheel_primality_equivalence_proved": True,
            "goldbach_filtered_count_exact_at_square_root_proved": True,
            "fixed_subthreshold_wheel_sufficiency_refuted": True,
            "sub_square_root_prime_weighted_remainder_controlled": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Sieving to sqrt(X) is an exact finite decision procedure, not "
            "an all-X proof and not an analytic improvement. A useful proof "
            "must obtain a uniform positive result with less than complete "
            "square-root factor information."
        ),
        "failure_count": failures,
    }


def crt(congruences: list[tuple[int, int]]) -> tuple[int, int]:
    modulus = product(local_modulus for _, local_modulus in congruences)
    value = 0
    for residue, local_modulus in congruences:
        partial = modulus // local_modulus
        value += residue * partial * pow(partial, -1, local_modulus)
    return value % modulus, modulus


def twin_survivor_residue(primes: list[int]) -> tuple[int, int]:
    congruences = []
    for prime in primes:
        if prime == 2:
            residue = 1
        elif prime == 3:
            residue = 2
        else:
            residue = 1
        congruences.append((residue, prime))
    return crt(congruences)


def twin_square_root_audit() -> dict[str, Any]:
    exact_rows, failures = square_root_filter_rows()
    countermodels = []
    for cutoff in (3, 5, 7, 11, 17, 29):
        primes = primes_through(cutoff)
        wheel_residue, wheel = twin_survivor_residue(primes)
        left_factor, right_factor = next_primes(cutoff + 1, 2)
        base, progression_modulus = crt(
            [
                (wheel_residue, wheel),
                (0, left_factor),
                (-2, right_factor),
            ]
        )
        witness = base + progression_modulus
        valid = (
            wheel_filter(witness, cutoff, primes)
            and wheel_filter(witness + 2, cutoff, primes)
            and witness % left_factor == 0
            and (witness + 2) % right_factor == 0
            and witness > left_factor
            and witness + 2 > right_factor
            and not is_prime(witness)
            and not is_prime(witness + 2)
            and cutoff < math.sqrt(witness + 2)
        )
        failures += int(not valid)
        countermodels.append(
            {
                "cutoff_z": cutoff,
                "wheel_W": wheel,
                "wheel_survivor_residue": wheel_residue,
                "external_left_factor": left_factor,
                "external_right_factor": right_factor,
                "composite_n": witness,
                "composite_n_plus_2": witness + 2,
                "progression_modulus": progression_modulus,
                "z_below_sqrt_X": cutoff < math.sqrt(witness + 2),
                "countermodel_verified": valid,
            }
        )

    theorem = (
        "With the same Q_z filter, if z>=sqrt(X), then for every n with "
        "n+2<=X, Q_z(n)Q_z(n+2)=1 exactly when (n,n+2) is a twin-prime "
        "pair. For every finite z this implication fails at larger scales: "
        "CRT gives an infinite progression surviving every prime at most z "
        "while n is divisible by a chosen prime r>z and n+2 by another "
        "prime s>z."
    )
    proof = (
        "Square-root exactness applies separately to n and n+2. For the "
        "countermodel, select a residue avoiding 0 and -2 modulo every "
        "prime at most z, then impose n=0 mod r and n=-2 mod s. Pairwise "
        "coprimality lets CRT combine the conditions. Every sufficiently "
        "large member is a proper multiple on both sides but has the same "
        "finite-wheel signature as a candidate twin pair."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "square_root_exactness_rows": exact_rows,
        "subthreshold_crt_countermodels": countermodels,
        "aggregate": {
            "square_root_twin_filter_equivalence_proved": True,
            "finite_subthreshold_twin_filter_sufficiency_refuted": True,
            "infinite_countermodel_progression_per_cutoff_proved": True,
            "uniform_sub_square_root_type_ii_separation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Exact square-root trial division decides bounded candidates but "
            "does not imply infinitely many candidates. Below that complete "
            "information threshold, an analytic parity/Type-II separation "
            "is still required."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_sharp_tail_audit()
    collatz = collatz_prime_power_audit()
    goldbach = goldbach_square_root_audit()
    twin = twin_square_root_audit()

    tracks = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-224",
            "theorem_name": "SharpQuarterDyadicTailEnvelopeAndSignCertificate",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No RH-equivalent actual-zeta defect or rigorous prime-side "
                "band margin is constructed."
            ),
            "route_decision": {
                "discard": "using the nonsharp factor-one tail envelope or treating an abstract sign certificate as an RH criterion",
                "retain": "derive actual-zeta prime-side bands whose certified margins dominate the sharp quarter tail",
                "next_single_lemma": "PrimeSideDyadicBandMarginsExceedSharpQuarterTailEnvelopeAtCofinalCutoffs",
            },
            "proof_dag": proof_dag(
                "RH",
                "ExponentialTailDyadicProfileInjectivityAndUniformCofinalTruncation",
                "SharpQuarterDyadicTailEnvelopeAndSignCertificate",
                "NonsharpFactorOneTailOrAbstractSignImpliesRH",
                "PrimeSideDyadicBandMarginsExceedSharpQuarterTailEnvelopeAtCofinalCutoffs",
                "Riemann Hypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-224",
            "theorem_name": "PrimePowerValuationCycleCriterionAndRadicalNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Prime-power factorization exactly recognizes finite cycles "
                "but does not uniformly exclude them or prove descent for "
                "aperiodic trajectories."
            ),
            "route_decision": {
                "discard": "radical-only code-adaptive divisibility as a complete cycle obstruction",
                "retain": "bound a missing prime-power valuation in every nontrivial primitive code and combine it with aperiodic descent",
                "next_single_lemma": "UniformPrimePowerDeficitOrUniversalAperiodicDescent",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedModulusPrimitiveFalsePositiveConstruction",
                "PrimePowerValuationCycleCriterionAndRadicalNoGo",
                "RadicalDivisibilityIsACompleteAdaptiveCycleTest",
                "UniformPrimePowerDeficitOrUniversalAperiodicDescent",
                "Collatz Conjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-224",
            "theorem_name": "SquareRootWheelCompletenessAndGoldbachSubthresholdNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The square-root filter is exact only at each finite horizon; "
                "no uniform sub-square-root prime-weighted remainder bound is proved."
            ),
            "route_decision": {
                "discard": "claiming that any fixed or incomplete wheel count equals the prime Goldbach count",
                "retain": "beat complete square-root sieving by a uniform prime-weighted remainder below the local margin",
                "next_single_lemma": "SubSquareRootPrimeWeightedGoldbachRemainderBelowUniformLocalMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "FiniteWheelUniformLocalMarginAndTwinFactorIdentity",
                "SquareRootWheelCompletenessAndGoldbachSubthresholdNoGo",
                "FixedOrIncompleteWheelCountEqualsPrimeGoldbachCount",
                "SubSquareRootPrimeWeightedGoldbachRemainderBelowUniformLocalMargin",
                "Strong Goldbach Conjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-224",
            "theorem_name": "SquareRootTwinFilterCompletenessAndSubthresholdCRTNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "Exact bounded primality filtering does not create infinitely "
                "many twin candidates; sub-square-root Type-II separation remains open."
            ),
            "route_decision": {
                "discard": "treating survival below the square-root completeness threshold as twin primality",
                "retain": "prove a uniform sub-square-root bilinear estimate that removes the CRT composite-pair mass",
                "next_single_lemma": "UniformSubSquareRootTypeIIBilinearSeparationForGapTwo",
            },
            "proof_dag": proof_dag(
                "TP",
                "FixedWheelCompositePairCountermodel",
                "SquareRootTwinFilterCompletenessAndSubthresholdCRTNoGo",
                "SubSquareRootWheelSurvivalCertifiesTwinPrimality",
                "UniformSubSquareRootTypeIIBilinearSeparationForGapTwo",
                "Twin Prime Conjecture",
            ),
        },
    }

    failure_count = sum(
        track["reproducible_computation"]["failure_count"]
        for track in tracks.values()
    )
    root = {
        "theorem_name": "SharpCompletenessThresholdsForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-224 proves four exact threshold or no-go theorems and "
            "resolves none of the four parent conjectures."
        ),
        **tracks,
        "cross_problem_synthesis": (
            "Each track now has an explicit completeness threshold. RH band "
            "signs require a margin above the optimal quarter tail envelope. "
            "Collatz cycle divisibility requires every prime-power "
            "multiplicity, not only the radical. Goldbach and Twin filters "
            "become exact at square-root factor depth, while incomplete "
            "wheels admit explicit composite false positives. These are "
            "decision boundaries, not proofs of the parent conjectures."
        ),
        "literature_boundary": {
            "riemann": "The result is a kernel optimization inside the project's Laplace model, not a new RH equivalence.",
            "collatz": "The prime-power criterion is unique factorization applied to the exact cycle equation; no priority claim is made.",
            "goldbach": "Square-root trial division is elementary; the unsolved content remains a uniform sub-square-root prime correlation estimate.",
            "twin_prime": "The CRT false positives instantiate the classical parity barrier and do not improve bounded-gap theorems.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_corrected_route_count": 4,
            "next_single_lemma_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failure_count,
        },
    }

    attempts = []
    for key, track in tracks.items():
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "declared_proposition": track["declared_proposition"],
                "new_result": track["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/sharp_completeness_thresholds_audit/{key}",
                    "failure_count": track["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"][
                    "next_single_lemma"
                ],
                "proof_dag": track["proof_dag"],
            }
        )

    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-224 proves four bounded threshold or no-go results and "
            "resolves none of the four parent conjectures."
        ),
        "sharp_completeness_thresholds_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["sharp_completeness_thresholds_audit"]
    write_json(
        ROOT / "data/open-problem/ticket224-sharp-completeness-thresholds.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-224-sharp-quarter-tail.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-224-prime-power-criterion.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-224-square-root-wheel.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-224-square-root-wheel.json",
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
            audit["sharp_completeness_thresholds_audit"]["machine_audit"],
            indent=2,
        )
    )
    if audit["sharp_completeness_thresholds_audit"]["machine_audit"][
        "total_failure_count"
    ]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
