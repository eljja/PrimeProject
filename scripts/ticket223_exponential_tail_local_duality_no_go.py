from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket223-exponential-tail-local-duality-no-go.v1"
GENERATED_AT = "2026-08-14T17:00:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


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
            {"id": f"{prefix}-T222", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T223", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N223",
                "label": limited,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN223",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T222", f"{prefix}-T223"],
            [f"{prefix}-T223", f"{prefix}-N223"],
            [f"{prefix}-T223", f"{prefix}-OPEN223"],
            [f"{prefix}-OPEN223", prefix],
        ],
    }


def geometric_tail(ratio: Decimal, cutoff: int) -> Decimal:
    return ratio ** (cutoff + 1) / (Decimal(1) - ratio)


def riemann_exponential_tail_audit() -> dict[str, Any]:
    getcontext().prec = 90
    eta = Decimal(2).ln()
    weighted_norm = Decimal(1)
    rows = []
    failures = 0
    transcript = hashlib.sha256()

    for cutoff in (4, 8, 12, 16, 24, 32):
        total_variation_tail = (Decimal(4) ** (-cutoff)) / Decimal(3)
        exponential_bound = (-eta * cutoff).exp() * weighted_norm
        band_tails = []
        for index in range(-6, 13):
            s = Decimal(2) ** (-index)
            first_ratio = -(Decimal(4) ** -1) * (-s).exp()
            second_ratio = -(Decimal(4) ** -1) * (-(Decimal(2) * s)).exp()
            tail = geometric_tail(first_ratio, cutoff) - geometric_tail(
                second_ratio, cutoff
            )
            band_tails.append(abs(tail))
            transcript.update(
                f"{cutoff}:{index}:{tail}:{total_variation_tail}\n".encode("ascii")
            )
        maximum_band_tail = max(band_tails)
        tv_bound_verified = maximum_band_tail <= total_variation_tail
        exponential_bound_verified = total_variation_tail <= exponential_bound
        failures += int(not tv_bound_verified)
        failures += int(not exponential_bound_verified)
        rows.append(
            {
                "cutoff_T": cutoff,
                "maximum_observed_band_tail": format(maximum_band_tail, ".30E"),
                "exact_total_variation_tail": format(total_variation_tail, ".30E"),
                "uniform_exponential_bound": format(exponential_bound, ".30E"),
                "tv_bound_verified": tv_bound_verified,
                "exponential_bound_verified": exponential_bound_verified,
            }
        )

    theorem = (
        "Let sigma be a finite signed Borel measure supported on [a,infinity) "
        "with a>0 and integral exp(eta t) d|sigma|(t)<infinity for some "
        "eta>0. Put L_sigma(s)=integral exp(-st) d sigma(t) and "
        "W_j=L_sigma(2^(-j))-L_sigma(2^(1-j)). If W_j=0 for every integer "
        "j, then sigma=0. Moreover, truncating sigma at height T changes "
        "every dyadic band by at most exp(-eta T) times the exponential "
        "total-variation norm, uniformly in j."
    )
    proof = (
        "The exponential moment makes L_sigma holomorphic on Re(s)>-eta. "
        "The band equations make all dyadic samples L_sigma(2^(-j)) equal. "
        "As j tends to minus infinity, support above a forces these samples "
        "to zero, so every sample is zero. The samples accumulating at s=0 "
        "now accumulate inside the holomorphy domain; the identity theorem "
        "gives L_sigma identically zero. Uniqueness of the Laplace transform "
        "then gives sigma=0. For the tail, |sigma|([T,infinity)) is at most "
        "exp(-eta T) integral exp(eta t)d|sigma|, and the band kernel has "
        "absolute value at most one. This extends TICKET-222 from compact "
        "support to an exponentially tight unbounded class, but does not "
        "construct an RH-equivalent zeta defect measure in that class."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "hypotheses": {
            "support": "[a,infinity) with a>0",
            "tail": "finite exponential total-variation moment",
            "observations": "all two-sided dyadic bands",
        },
        "model_measure": {
            "atoms": "t=n for n>=1",
            "weights": "(-1)^n 4^(-n)",
            "eta": "log(2)",
            "weighted_norm": "1",
        },
        "cofinal_tail_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "exponential_tail_dyadic_injectivity_proved": True,
            "uniform_cofinal_truncation_bound_proved": True,
            "all_model_tail_checks_pass": failures == 0,
            "actual_zeta_defect_measure_constructed": False,
            "prime_side_equivalent_bands_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes the abstract analytic tail step only under "
            "an exponential moment. It does not show that an RH-equivalent "
            "zero defect has this moment or that its bands are computable "
            "with rigorous prime-side signs."
        ),
        "failure_count": failures,
    }


def multiplicative_order(value: int, modulus: int) -> int:
    if math.gcd(value, modulus) != 1:
        raise ValueError("multiplicative order requires coprime inputs")
    current = 1
    for order in range(1, modulus + 1):
        current = (current * value) % modulus
        if current == 1:
            return order
    raise ArithmeticError("order not found within Euler bound")


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


def fixed_modulus_witness(modulus: int) -> dict[str, Any]:
    if modulus <= 1 or math.gcd(modulus, 6) != 1:
        raise ValueError("modulus must be greater than one and coprime to six")
    order_two = multiplicative_order(2, modulus)
    ratio = (4 * pow(3, -1, modulus)) % modulus
    height = multiplicative_order(ratio, modulus)
    word = (2 + order_two,) + (2,) * (height - 1)
    exponent_sum = sum(word)
    intercept = collatz_intercept(word)
    denominator = (2**exponent_sum) - (3**height)
    expected_gap = 4 * ((2**order_two) - 1) * (3 ** (height - 1))
    return {
        "modulus_M": modulus,
        "order_of_two_r": order_two,
        "word_height_h": height,
        "valuation_word": list(word),
        "exponent_sum_S": exponent_sum,
        "D_decimal": str(denominator),
        "B_decimal": str(intercept),
        "D_minus_B_decimal": str(denominator - intercept),
        "expected_D_minus_B_decimal": str(expected_gap),
        "M_divides_D": denominator % modulus == 0,
        "M_divides_B": intercept % modulus == 0,
        "positive_false_positive": 0 < intercept < denominator,
        "primitive_nontrivial_word": is_primitive_word(word)
        and any(exponent != 2 for exponent in word),
        "actual_cycle_divisibility": intercept % denominator == 0,
    }


def collatz_fixed_modulus_no_go_audit() -> dict[str, Any]:
    moduli = [value for value in range(5, 200) if math.gcd(value, 6) == 1]
    rows = [fixed_modulus_witness(modulus) for modulus in moduli]
    family_moduli = [(5, 7), (5, 7, 11), (5, 7, 11, 13)]
    family_rows = []
    for family in family_moduli:
        combined = math.lcm(*family)
        witness = fixed_modulus_witness(combined)
        family_rows.append(
            {
                "finite_modulus_family": list(family),
                "combined_lcm": combined,
                "simultaneous_false_positive": witness,
            }
        )
    failures = sum(
        int(
            not (
                row["M_divides_D"]
                and row["M_divides_B"]
                and row["positive_false_positive"]
                and row["primitive_nontrivial_word"]
                and not row["actual_cycle_divisibility"]
                and row["D_minus_B_decimal"] == row["expected_D_minus_B_decimal"]
            )
        )
        for row in rows
    )
    failures += sum(
        int(
            not row["simultaneous_false_positive"]["positive_false_positive"]
        )
        for row in family_rows
    )
    theorem = (
        "For every integer M>1 coprime to 6, let r=ord_M(2) and "
        "h=ord_M(4*3^(-1)). The primitive non-all-two valuation word "
        "a=(2+r,2,...,2) of length h has M dividing both "
        "D=2^(sum a_i)-3^h and its Collatz intercept B, but 0<B<D. Hence "
        "D does not divide B. Taking the least common multiple gives one "
        "such false positive for every finite family of fixed moduli coprime "
        "to 6."
    )
    proof = (
        "All exponents are congruent to two modulo r. Therefore D is "
        "congruent to 4^h-3^h, which is zero modulo M by the definition of "
        "h. Every prefix power in B is likewise congruent to the all-two "
        "prefix, so B is congruent to sum 3^(h-i)4^(i-1)=4^h-3^h and is "
        "also zero modulo M. Direct summation gives "
        "D-B=4(2^r-1)3^(h-1)>0. The unique enlarged first exponent makes "
        "the word primitive and nontrivial. Thus every fixed modular sieve "
        "whose moduli are coprime to 6 "
        "admits a provable non-cycle that passes all of its divisibility "
        "tests; a successful obstruction must grow with the code or use a "
        "nonlocal descent argument."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "audited_modulus_range": {"minimum": 5, "maximum": 199},
        "witness_rows": rows,
        "finite_family_rows": family_rows,
        "aggregate": {
            "moduli_checked": len(rows),
            "constructive_fixed_modulus_no_go_proved": True,
            "finite_fixed_modulus_families_defeated": True,
            "nontrivial_cycle_found": False,
            "divergent_orbits_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The construction rules out fixed finite modular congruence "
            "tests with moduli coprime to 6 as a complete cycle certificate. "
            "It does not rule out "
            "code-adaptive moduli, Archimedean estimates, or all aperiodic "
            "divergent trajectories."
        ),
        "failure_count": failures,
    }


def primes_through(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for value in range(2, int(limit**0.5) + 1):
        if sieve[value]:
            for multiple in range(value * value, limit + 1, value):
                sieve[multiple] = False
    return [value for value, prime in enumerate(sieve) if prime]


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def euler_phi_squarefree(primes: Iterable[int]) -> int:
    return product(prime - 1 for prime in primes)


def goldbach_local_count(target: int, primes: tuple[int, ...]) -> int:
    return product(
        (prime - 1) if target % prime == 0 else (prime - 2)
        for prime in primes
    )


def normalized_local_floor(primes: tuple[int, ...]) -> Fraction:
    result = Fraction(1, 1)
    for prime in primes:
        result *= Fraction(prime * (prime - 2), (prime - 1) ** 2)
    return result


def goldbach_local_margin_audit() -> dict[str, Any]:
    audit_primes = (3, 5, 7, 11)
    wheel = product(audit_primes)
    phi = euler_phi_squarefree(audit_primes)
    floor = normalized_local_floor(audit_primes)
    residue_rows = []
    failures = 0
    minimum_ratio: Fraction | None = None
    equality_count = 0
    for target in range(wheel):
        direct = sum(
            1
            for residue in range(wheel)
            if math.gcd(residue, wheel) == 1
            and math.gcd(target - residue, wheel) == 1
        )
        formula = goldbach_local_count(target, audit_primes)
        ratio = Fraction(direct * wheel, phi * phi)
        minimum_ratio = ratio if minimum_ratio is None else min(minimum_ratio, ratio)
        equality = ratio == floor
        equality_count += int(equality)
        failures += int(direct != formula)
        failures += int(ratio < floor)
        if target < 24 or equality and len(residue_rows) < 40:
            residue_rows.append(
                {
                    "target_residue_mod_W": target,
                    "direct_admissible_count": direct,
                    "formula_admissible_count": formula,
                    "normalized_ratio": fraction_string(ratio),
                    "attains_uniform_floor": equality,
                    "coprime_to_W": math.gcd(target, wheel) == 1,
                }
            )
    failures += int(minimum_ratio != floor)
    failures += int(equality_count != phi)

    prefix_rows = []
    prefix: list[int] = []
    for prime in [value for value in primes_through(43) if value > 2]:
        prefix.append(prime)
        current = normalized_local_floor(tuple(prefix))
        prefix_rows.append(
            {
                "largest_prime": prime,
                "prime_count": len(prefix),
                "wheel_normalized_floor": fraction_string(current),
                "wheel_normalized_floor_decimal": f"{float(current):.15f}",
            }
        )

    theorem = (
        "Let W be a squarefree product of odd primes and A_W(N) count "
        "residues a modulo W for which both a and N-a are coprime to W. "
        "Then A_W(N)=product_(p|W,p|N)(p-1) product_(p|W,p not|N)(p-2). "
        "After division by the independent coprime density (phi(W)/W)^2, "
        "the ratio is at least C_W=product_(p|W)p(p-2)/(p-1)^2, with "
        "equality exactly when gcd(N,W)=1. The products C_W are bounded "
        "below by the positive infinite odd-prime product C_* because "
        "sum_p 1/(p-1)^2 converges."
    )
    proof = (
        "For each odd p dividing W, one residue is forbidden when p divides "
        "N and two distinct residues are forbidden otherwise. CRT multiplies "
        "the local counts. Normalization gives p/(p-1) in the first case "
        "and p(p-2)/(p-1)^2 in the second. Replacing the second factor by "
        "the first only increases the product, proving the floor and its "
        "equality condition. Since one minus the floor factor is "
        "1/(p-1)^2 and the sum of these deficits converges, the infinite "
        "product is positive. This proves a uniform local margin, not a "
        "prime-weighted Goldbach representation."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_wheel_audit": {
            "wheel_primes": list(audit_primes),
            "wheel_W": wheel,
            "phi_W": phi,
            "uniform_floor": fraction_string(floor),
            "minimum_observed_ratio": fraction_string(minimum_ratio or Fraction()),
            "floor_equality_residue_count": equality_count,
            "expected_equality_residue_count": phi,
            "sample_residue_rows": residue_rows,
        },
        "wheel_prefix_rows": prefix_rows,
        "aggregate": {
            "crt_local_count_formula_proved": True,
            "uniform_positive_normalized_local_floor_proved": True,
            "goldbach_twin_local_factor_identity_proved": True,
            "prime_weighted_global_remainder_controlled": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Every finite wheel is locally admissible for every even target, "
            "so local congruence positivity cannot by itself force two actual "
            "primes. The remaining issue is a uniform prime-weighted global "
            "remainder smaller than the local main term."
        ),
        "failure_count": failures,
    }


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


def crt(congruences: list[tuple[int, int]]) -> tuple[int, int]:
    modulus = product(item[1] for item in congruences)
    value = 0
    for residue, local_modulus in congruences:
        partial = modulus // local_modulus
        value += residue * partial * pow(partial, -1, local_modulus)
    return value % modulus, modulus


def survivor_residue(primes: tuple[int, ...]) -> tuple[int, int]:
    congruences = []
    for prime in primes:
        residue = 2 if prime == 3 else 1
        congruences.append((residue, prime))
    return crt(congruences)


def twin_composite_countermodel_audit() -> dict[str, Any]:
    prefix_rows = []
    failures = 0
    prefix: list[int] = []
    odd_primes = [value for value in primes_through(43) if value > 2]
    for prime in odd_primes:
        prefix.append(prime)
        wheel_primes = tuple(prefix)
        residue, wheel = survivor_residue(wheel_primes)
        external = next_primes(prime + 1, 2)
        left_factor, right_factor = external
        base, progression_modulus = crt(
            [
                (residue, wheel),
                (0, left_factor),
                (-2, right_factor),
            ]
        )
        witness = base + progression_modulus
        survivor_count = product(value - 2 for value in wheel_primes)
        phi = euler_phi_squarefree(wheel_primes)
        normalized_density = Fraction(survivor_count * wheel, phi * phi)
        expected_density = normalized_local_floor(wheel_primes)
        valid = (
            math.gcd(witness * (witness + 2), wheel) == 1
            and witness % left_factor == 0
            and (witness + 2) % right_factor == 0
            and witness > left_factor
            and witness + 2 > right_factor
            and normalized_density == expected_density
        )
        failures += int(not valid)
        prefix_rows.append(
            {
                "largest_wheel_prime": prime,
                "wheel_prime_count": len(wheel_primes),
                "wheel_W": str(wheel),
                "survivor_residue_a": str(residue),
                "external_left_factor_r": left_factor,
                "external_right_factor_s": right_factor,
                "composite_pair_n": str(witness),
                "composite_pair_n_plus_2": str(witness + 2),
                "infinite_progression_modulus": str(progression_modulus),
                "wheel_survivor_count": survivor_count,
                "normalized_survivor_density": fraction_string(normalized_density),
                "countermodel_verified": valid,
            }
        )

    theorem = (
        "For every finite squarefree odd wheel W and every residue a modulo "
        "W avoiding 0 and -2 modulo each prime divisor, there are infinitely "
        "many n congruent to a modulo W for which both n and n+2 are "
        "composite. Choose distinct primes r,s not dividing W and solve "
        "n=0 mod r and n=-2 mod s together with n=a mod W by CRT. Moreover, "
        "the normalized density of wheel survivors is exactly "
        "C_W=product_(p|W)p(p-2)/(p-1)^2, the minimum normalized Goldbach "
        "local factor from the companion theorem."
    )
    proof = (
        "The three congruences have pairwise coprime moduli, so CRT gives an "
        "infinite arithmetic progression. Large members are proper multiples "
        "of r while their shifts by two are proper multiples of s, yet their "
        "entire finite-wheel signature is the all-survivor signature. The "
        "survivor count is product(p-2); division by the squared coprime "
        "density gives C_W. Thus fixed-wheel biased parity signal is real "
        "but cannot certify twin primality. Any successful lower bound must "
        "let the arithmetic information scale grow and dominate the omitted "
        "prime Type-II remainder."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "wheel_prefix_countermodels": prefix_rows,
        "aggregate": {
            "wheel_prefixes_checked": len(prefix_rows),
            "fixed_wheel_composite_pair_countermodel_proved": True,
            "infinitely_many_countermodels_per_survivor_class_proved": True,
            "goldbach_twin_local_factor_identity_proved": True,
            "scale_growing_type_ii_dominance_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem defeats certificates depending on one fixed finite "
            "wheel. It does not defeat wheels growing with the search scale "
            "or analytic estimates that control the omitted-prime tail."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_exponential_tail_audit()
    collatz = collatz_fixed_modulus_no_go_audit()
    goldbach = goldbach_local_margin_audit()
    twin = twin_composite_countermodel_audit()

    tracks = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-223",
            "theorem_name": "ExponentialTailDyadicProfileInjectivityAndUniformCofinalTruncation",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No RH-equivalent exponentially weighted zeta defect with "
                "rigorously computable prime-side bands is constructed."
            ),
            "route_decision": {
                "discard": "claiming that compact support is essential for full dyadic injectivity",
                "retain": "build an RH-equivalent exponentially weighted defect and prime-side band enclosure",
                "next_single_lemma": "RHEquivalentExponentiallyWeightedDefectWithPrimeSideDyadicBands",
            },
            "proof_dag": proof_dag(
                "RH",
                "CompactSupportFullDyadicLaplaceProfileInjectivity",
                "ExponentialTailDyadicProfileInjectivityAndUniformCofinalTruncation",
                "AbstractExponentialTailImpliesActualZetaTail",
                "RHEquivalentExponentiallyWeightedDefectWithPrimeSideDyadicBands",
                "Riemann Hypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-223",
            "theorem_name": "FixedModulusPrimitiveFalsePositiveConstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Fixed modular sieves with moduli coprime to 6 are eliminated, "
                "but code-adaptive "
                "divisibility and aperiodic descent remain open."
            ),
            "route_decision": {
                "discard": "any finite fixed family of modular D and B congruence tests with moduli coprime to 6 as a complete cycle proof",
                "retain": "use code-growing prime obstructions or prove first descent for every aperiodic ray",
                "next_single_lemma": "CodeAdaptiveLargePrimeObstructionOrUniversalAperiodicDescent",
            },
            "proof_dag": proof_dag(
                "CO",
                "SlopeInterceptLosslessValuationCodeAndExactCycleReduction",
                "FixedModulusPrimitiveFalsePositiveConstruction",
                "FixedFiniteModularSieveCanExcludeEveryPrimitiveCode",
                "CodeAdaptiveLargePrimeObstructionOrUniversalAperiodicDescent",
                "Collatz Conjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-223",
            "theorem_name": "FiniteWheelUniformLocalMarginAndTwinFactorIdentity",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "A positive local singular factor is not a positive lower "
                "bound for the global prime representation count."
            ),
            "route_decision": {
                "discard": "searching for a finite congruence obstruction to even Goldbach targets",
                "retain": "bound the prime-weighted global remainder below the uniform local margin",
                "next_single_lemma": "PrimeWeightedGoldbachRemainderStrictlyBelowUniformLocalMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "OrderedGoldbachCountParityEqualsDiagonalPrimeIndicator",
                "FiniteWheelUniformLocalMarginAndTwinFactorIdentity",
                "FiniteLocalAdmissibilityForcesPrimeRepresentation",
                "PrimeWeightedGoldbachRemainderStrictlyBelowUniformLocalMargin",
                "Strong Goldbach Conjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-223",
            "theorem_name": "FixedWheelCompositePairCountermodel",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "Fixed wheels are insufficient, but no scale-growing "
                "Type-II lower bound for Lambda(n)Lambda(n+2) is proved."
            ),
            "route_decision": {
                "discard": "using any fixed finite-wheel signature as a certificate of twin primality",
                "retain": "grow arithmetic information with scale and dominate the omitted-prime remainder",
                "next_single_lemma": "ScaleGrowingWheelSignalWithUniformTypeIIRemainderDominance",
            },
            "proof_dag": proof_dag(
                "TP",
                "FiniteWheelBiasedParityLeakageProductFormula",
                "FixedWheelCompositePairCountermodel",
                "NonzeroFixedWheelLeakageCertifiesTwinPrimes",
                "ScaleGrowingWheelSignalWithUniformTypeIIRemainderDominance",
                "Twin Prime Conjecture",
            ),
        },
    }

    failure_count = sum(
        track["reproducible_computation"]["failure_count"]
        for track in tracks.values()
    )
    root = {
        "theorem_name": "ExponentialTailAndLocalDualityBoundaryForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-223 proves four exact analytic, modular, or local-density "
            "results. It resolves none of the four parent conjectures."
        ),
        **tracks,
        "cross_problem_synthesis": (
            "The RH observable remains injective beyond compact support under "
            "an exponential tail. Collatz admits explicit primitive false "
            "positives for every fixed modular sieve with moduli coprime to "
            "6. Goldbach has a uniform "
            "positive local margin whose exact minimum equals the normalized "
            "twin-wheel survivor density, while every fixed twin wheel also "
            "admits infinitely many composite-pair countermodels. The open "
            "barriers are therefore prime-side global remainder control, "
            "code-adaptive arithmetic, and an RH-equivalent defect model."
        ),
        "literature_boundary": {
            "riemann": (
                "Connes-Consani motivates semi-local positivity; the "
                "exponential-tail Laplace theorem here is elementary and is "
                "not an RH criterion."
            ),
            "collatz": (
                "Tao's almost-all descent remains strictly weaker than every "
                "orbit. The fixed-modulus construction concerns cycle sieves "
                "only and makes no literature-priority claim."
            ),
            "goldbach": (
                "The local product is the classical singular-series factor. "
                "The project contribution is the explicit cross-track audit, "
                "not a new Goldbach asymptotic or verification record."
            ),
            "twin_prime": (
                "Ford-Maynard explains the need for substantial Type-II "
                "information. The CRT countermodel is a fixed-wheel no-go, "
                "not a twin-prime lower bound."
            ),
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
    for problem_id, track in tracks.items():
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "declared_proposition": track["declared_proposition"],
                "new_result": track["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/exponential_tail_local_duality_no_go_audit/{problem_id}",
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
            "TICKET-223 proves four bounded theorems or no-go results and "
            "resolves none of the four parent conjectures."
        ),
        "exponential_tail_local_duality_no_go_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["exponential_tail_local_duality_no_go_audit"]
    write_json(
        ROOT
        / "data/open-problem/ticket223-exponential-tail-local-duality-no-go.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-223-exponential-tail-injectivity.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-223-fixed-modulus-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-223-local-margin-duality.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-223-fixed-wheel-countermodel.json",
    }
    for key, destination in destinations.items():
        track = root[key]
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **track,
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps(audit["exponential_tail_local_duality_no_go_audit"]["machine_audit"], indent=2))
    if audit["exponential_tail_local_duality_no_go_audit"]["machine_audit"][
        "total_failure_count"
    ]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
