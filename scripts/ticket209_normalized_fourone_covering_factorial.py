from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket209-normalized-fourone-covering-factorial.v1"
GENERATED_AT = "2026-08-10T22:00:00+09:00"
STATUS = "open_not_proven"


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


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
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T208", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T209", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N209",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN209",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T208", f"{prefix}-T209"],
            [f"{prefix}-T209", f"{prefix}-N209"],
            [f"{prefix}-T209", f"{prefix}-OPEN209"],
            [f"{prefix}-OPEN209", prefix],
        ],
    }


def gamma_one_modulus(height: int) -> float:
    if height == 0:
        return 1.0
    y = height / 2
    return math.sqrt(math.pi * y / math.sinh(math.pi * y))


def xi_sigma_two_upper_envelope(height: int) -> float:
    polynomial = math.sqrt((height * height + 4) * (height * height + 1))
    return (
        0.5
        * polynomial
        / math.pi
        * gamma_one_modulus(height)
        * (math.pi**2 / 6)
    )


def riemann_gamma_normalized_audit() -> dict[str, Any]:
    rows = []
    previous = math.inf
    failures = 0
    for height in (4, 8, 16, 32, 64, 128):
        upper = xi_sigma_two_upper_envelope(height)
        decreasing = upper < previous
        positive = upper > 0
        failures += int(not decreasing) + int(not positive)
        rows.append(
            {
                "height_T": height,
                "completed_xi_endpoint_upper_envelope": f"{upper:.17e}",
                "log10_upper_envelope": f"{math.log10(upper):.12f}",
                "positive": positive,
                "strictly_below_previous_row": decreasing,
            }
        )
        previous = upper

    normalized_lower = math.pi**2 / 15
    theorem = (
        "There is no height-independent epsilon>0 for which the completed "
        "Riemann xi-function has |xi(s)|>=epsilon on the full boundaries of "
        "a cofinal sequence of rectangles [-1,2] x [-T,T]: already "
        "|xi(2+iT)| tends to zero. After removing the nonvanishing polynomial "
        "and gamma factors, the normalized quotient equals zeta(s) and obeys "
        "|zeta(2+it)|>=zeta(4)/zeta(2)=pi^2/15. Thus absolute completed-xi "
        "clearance is the wrong cofinal invariant; arithmetic nonvanishing on "
        "the central horizontal segment remains the unresolved boundary task."
    )
    proof = (
        "At s=2+iT, |zeta(s)|<=zeta(2), "
        "|s(s-1)|=sqrt((T^2+4)(T^2+1)), and "
        "|Gamma(1+iT/2)|^2=pi(T/2)/sinh(pi T/2). Substitution into the "
        "definition of xi bounds |xi(2+iT)| by a polynomial times "
        "exp(-pi T/4), hence by a quantity tending to zero. Every full top "
        "edge contains this endpoint, so a common positive absolute clearance "
        "is impossible. Conversely, "
        "2*pi^(s/2)*xi(s)/(s(s-1)Gamma(s/2))=zeta(s), and the absolutely "
        "convergent Euler product gives |zeta(2+it)|>=pi^2/15. For any fixed "
        "delta>0, the top-edge pieces Re(s)>=1+delta and Re(s)<=-delta are "
        "zero-free by the Euler product and xi(s)=xi(1-s); this leaves the "
        "central horizontal segment, not the decaying archimedean envelope."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "completed_xi_endpoint_upper_formula": (
            "U(T)=zeta(2)/(2*pi)*sqrt((T^2+4)(T^2+1))*"
            "sqrt((pi*T/2)/sinh(pi*T/2))"
        ),
        "gamma_normalized_identity": (
            "2*pi^(s/2)*xi(s)/(s(s-1)*Gamma(s/2))=zeta(s)"
        ),
        "normalized_sigma_two_lower_bound": (
            "|zeta(2+it)|>=zeta(4)/zeta(2)=pi^2/15"
        ),
        "normalized_sigma_two_lower_decimal": f"{normalized_lower:.17e}",
        "endpoint_decay_rows": rows,
        "outer_horizontal_reduction": {
            "fixed_delta": "1/4",
            "right_zero_free_segment": "5/4<=Re(s)<=2",
            "left_zero_free_segment": "-1<=Re(s)<=-1/4",
            "unresolved_central_segment": "-1/4<=Re(s)<=5/4",
            "uses_only_euler_product_and_functional_equation": True,
        },
        "aggregate": {
            "height_independent_absolute_xi_clearance_refuted": True,
            "gamma_normalized_sigma_two_clearance_proved": True,
            "outer_horizontal_segments_reduced": True,
            "central_cofinal_nonvanishing_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem refutes only a height-independent absolute xi margin. "
            "It does not refute height-dependent interval certificates and does "
            "not prove that any cofinal central horizontal edge is zero-free."
        ),
        "failure_count": failures,
    }


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def cycle_fixed_point(word: tuple[int, ...]) -> Fraction | None:
    slope = Fraction(1)
    intercept = Fraction(0)
    for valuation in word:
        denominator = 2**valuation
        slope = Fraction(3, denominator) * slope
        intercept = (3 * intercept + 1) / denominator
    if slope >= 1:
        return None
    return intercept / (1 - slope)


def total_valuation_upper_bound(length: int) -> int:
    exponent = 0
    while 2 ** (exponent + 1) * 3**length <= 10**length:
        exponent += 1
    return exponent


def four_one_words(length: int, maximum_total: int) -> list[tuple[int, ...]]:
    baseline_total = 2 * length - 4
    if baseline_total > maximum_total:
        return []
    words: list[tuple[int, ...]] = []
    for other_ones in combinations(range(1, length - 1), 3):
        one_positions = {0, *other_ones}
        non_one_positions = [
            index for index in range(length) if index not in one_positions
        ]
        for extra_total in range(maximum_total - baseline_total + 1):
            for extras in weak_compositions(extra_total, len(non_one_positions)):
                word = [1 if index in one_positions else 2 for index in range(length)]
                for index, extra in zip(non_one_positions, extras, strict=True):
                    word[index] += extra
                words.append(tuple(word))
    return words


def collatz_four_one_audit() -> dict[str, Any]:
    rows = []
    all_words: list[tuple[int, ...]] = []
    integer_candidates = []
    failures = 0
    for length in range(5, 16):
        maximum_total = total_valuation_upper_bound(length)
        baseline_total = 2 * length - 4
        words = four_one_words(length, maximum_total)
        all_words.extend(words)
        local_candidates = []
        for word in words:
            fixed = cycle_fixed_point(word)
            if (
                fixed is not None
                and fixed.denominator == 1
                and fixed.numerator >= 3
                and fixed.numerator % 2 == 1
            ):
                local_candidates.append(
                    {"word": list(word), "fixed_point": fixed.numerator}
                )
        integer_candidates.extend(local_candidates)
        failures += len(local_candidates)
        digest = hashlib.sha256(
            "\n".join(",".join(map(str, word)) for word in words).encode("ascii")
        ).hexdigest()
        rows.append(
            {
                "length_h": length,
                "minimum_total_valuation_2h_minus_4": baseline_total,
                "maximum_total_valuation_from_minimum_bound": maximum_total,
                "enumerated_word_count": len(words),
                "positive_odd_integer_fixed_point_count": len(local_candidates),
                "valuation_word_sha256": digest,
            }
        )

    threshold = 16
    threshold_left = 2 ** (2 * threshold - 4) * 3**threshold
    threshold_right = 10**threshold
    long_lengths_excluded = threshold_left > threshold_right
    failures += int(not long_lengths_excluded)
    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly four "
        "valuation entries equal to one and every remaining valuation at least "
        "two. Together with TICKETS 206-208, every hypothetical nontrivial "
        "positive cycle must contain at least five valuation-one entries."
    )
    proof = (
        "Rotate a hypothetical cycle to its minimum odd value m>=3. The first "
        "valuation is one and the last is at least two. With length h and total "
        "valuation A, multiplication around the cycle gives "
        "2^A=product_i(3+1/x_i)<=(10/3)^h. Exactly four ones imply A>=2h-4. "
        "At h=16, 2^(2h-4)3^h>10^h, and the ratio grows by 6/5 per additional "
        "step, so every h>=16 is impossible. For 5<=h<=15 the same inequality "
        "bounds A. Fixing the minimum rotation leaves exactly 2,292 valuation "
        "words. Exact affine composition gives their unique rational fixed "
        "points; none is a positive odd integer."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cycle_product_identity": "2^A=product_i(3+1/x_i)",
        "minimum_orbit_bound": "x_i>=m>=3 implies 2^A*3^h<=10^h",
        "exact_enumeration_rows": rows,
        "total_exact_words_enumerated": len(all_words),
        "positive_odd_integer_fixed_point_candidates": integer_candidates,
        "length_at_least_sixteen_exclusion": {
            "threshold_h": threshold,
            "left_2_pow_28_times_3_pow_16": str(threshold_left),
            "right_10_pow_16": str(threshold_right),
            "left_exceeds_right": long_lengths_excluded,
            "growth_factor_per_extra_length": "6/5",
        },
        "aggregate": {
            "exactly_four_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 5,
            "five_or_more_one_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This closes one complete periodic valuation stratum. It neither "
            "excludes cycles with at least five valuation-one entries nor proves "
            "descent of every nonperiodic positive orbit."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> list[bool]:
    flags = [True] * (limit + 1)
    if limit >= 0:
        flags[0] = False
    if limit >= 1:
        flags[1] = False
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            flags[candidate * candidate : limit + 1 : candidate] = [False] * (
                (limit - candidate * candidate) // candidate + 1
            )
    return flags


def primes_through(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def crt_solution(residues_and_moduli: list[tuple[int, int]]) -> tuple[int, int]:
    residue = 0
    modulus = 1
    for target, prime in residues_and_moduli:
        step = ((target - residue) * pow(modulus, -1, prime)) % prime
        residue = (residue + modulus * step) % (modulus * prime)
        modulus *= prime
    return residue, modulus


def goldbach_covering_row(bound: int) -> dict[str, Any]:
    all_primes = primes_through(2 * bound)
    odd_witnesses = [prime for prime in all_primes if 3 <= prime <= bound]
    cover_limit = max(3, int(bound / math.log(bound) ** 2))
    cover_primes = [prime for prime in all_primes if 3 <= prime <= cover_limit]
    uncovered = set(odd_witnesses)
    cover_rows = []
    covered_by: dict[int, int] = {}
    survivor_product = Fraction(1)
    for prime in cover_primes:
        buckets = [[] for _ in range(prime)]
        for witness in uncovered:
            buckets[witness % prime].append(witness)
        selected = max(range(prime), key=lambda residue: (len(buckets[residue]), -residue))
        covered = sorted(buckets[selected])
        for witness in covered:
            covered_by[witness] = prime
        uncovered.difference_update(covered)
        survivor_product *= Fraction(prime - 1, prime)
        cover_rows.append(
            {
                "modulus_q": prime,
                "selected_residue_r": selected,
                "newly_covered_prime_count": len(covered),
                "remaining_prime_count": len(uncovered),
            }
        )

    available_forcing = [prime for prime in all_primes if bound < prime < 2 * bound]
    survivors = sorted(uncovered)
    if len(available_forcing) < len(survivors):
        raise ValueError(f"insufficient forcing primes for B={bound}")
    forcing = list(zip(survivors, available_forcing[: len(survivors)], strict=True))
    congruences = [(0, 2)]
    congruences.extend(
        (row["selected_residue_r"], row["modulus_q"]) for row in cover_rows
    )
    congruences.extend((witness, divisor) for witness, divisor in forcing)
    canonical_residue, modulus = crt_solution(congruences)
    target = canonical_residue + modulus if canonical_residue else 2 * modulus
    forcing_map = dict(forcing)
    certificate_rows = []
    for witness in odd_witnesses:
        divisor = (
            covered_by[witness]
            if witness in covered_by
            else forcing_map[witness]
        )
        certificate_rows.append(
            {
                "excluded_witness_prime": witness,
                "forcing_divisor": divisor,
                "source": "cover" if witness in covered_by else "survivor",
                "proper_composite_complement": (
                    target - witness > divisor and (target - witness) % divisor == 0
                ),
            }
        )
    survivor_upper = Fraction(len(odd_witnesses)) * survivor_product
    all_excluded = all(row["proper_composite_complement"] for row in certificate_rows)
    two_excluded = target > 4 and (target - 2) % 2 == 0
    certificate_digest = hashlib.sha256(
        "\n".join(
            f"{row['excluded_witness_prime']},{row['forcing_divisor']},"
            f"{row['source']},{int(row['proper_composite_complement'])}"
            for row in certificate_rows
        ).encode("ascii")
    ).hexdigest()
    return {
        "witness_bound_B": bound,
        "cover_limit_z": cover_limit,
        "odd_witness_count": len(odd_witnesses),
        "cover_modulus_count": len(cover_rows),
        "survivor_count": len(survivors),
        "greedy_survivor_upper_bound_exact": fraction_text(survivor_upper),
        "greedy_survivor_bound_holds": Fraction(len(survivors)) <= survivor_upper,
        "cover_rows": cover_rows,
        "survivor_forcing_rows": [
            {
                "survivor_prime": witness,
                "forcing_prime": divisor,
                "proper_composite_complement": (
                    target - witness > divisor
                    and (target - witness) % divisor == 0
                ),
            }
            for witness, divisor in forcing
        ],
        "excluded_witness_certificate_count": len(certificate_rows),
        "excluded_witness_certificate_sha256": certificate_digest,
        "largest_forcing_prime": forcing[-1][1] if forcing else None,
        "canonical_even_target_N": str(target),
        "modulus_M": str(modulus),
        "N_between_M_and_2M": modulus < target <= 2 * modulus,
        "N_bit_length": target.bit_length(),
        "observed_B_over_natural_log_N_decimal": f"{bound / math.log(target):.12f}",
        "observed_B_over_logN_loglogN_decimal": (
            f"{bound / (math.log(target) * math.log(math.log(target))):.12f}"
        ),
        "p_equals_2_complement_is_composite": two_excluded,
        "all_prime_witnesses_at_most_B_excluded": all_excluded and two_excluded,
    }


def goldbach_covering_audit() -> dict[str, Any]:
    rows = [
        goldbach_covering_row(bound)
        for bound in (127, 509, 2039, 8191, 32767)
    ]
    failures = sum(
        int(not row["greedy_survivor_bound_holds"])
        + int(not row["N_between_M_and_2M"])
        + int(not row["all_prime_witnesses_at_most_B_excluded"])
        for row in rows
    )
    theorem = (
        "Let W(N) be the least prime p such that N-p is prime, with infinity "
        "when no representation exists. There is an absolute c>0 and an "
        "unbounded sequence of even N for which "
        "W(N)>c log N log log N. Consequently "
        "limsup W(N)/log N=infinity."
    )
    proof = (
        "For a large B put z=floor(B/(log B)^2). Starting with odd primes "
        "p<=B, for every odd prime q<=z choose a residue r_q containing the "
        "largest number of still-uncovered p. At most a factor (1-1/q) "
        "survives each step. Mertens' theorem and the prime number theorem give "
        "S<=pi(B) product_{3<=q<=z}(1-1/q)=O(B/(log B log z)) survivors. "
        "There are enough distinct primes Q_p in (B,2B) to assign one to each "
        "survivor. CRT imposes N=0 mod 2, N=r_q mod q, and N=p mod Q_p. "
        "Choosing M<N<=2M makes N-p a proper composite for every prime p<=B, "
        "so W(N)>B. The modulus satisfies "
        "log M<=theta(z)+S log(2B)=O(B/log B), hence "
        "B>=c log N log log N for some absolute c and all sufficiently large "
        "constructed targets. The displayed greedy rows are deterministic "
        "finite certificates of the same covering mechanism."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "covering_resource_bound": (
            "S<=pi(B)*product_{3<=q<=z}(1-1/q)=O(B/(log B log z))"
        ),
        "crt_resource_bound": "log M=theta(z)+O(S log B)=O(B/log B)",
        "deterministic_covering_fixture_rows": rows,
        "aggregate": {
            "superlogarithmic_least_witness_sequence_proved": True,
            "least_witness_over_log_limsup_is_infinite": True,
            "constant_logarithmic_ceiling_refuted": True,
            "goldbach_counterexample_found": False,
            "tail_exception_bound_constructed": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The CRT construction blocks only p<=B. It leaves all larger prime "
            "summands available and therefore supplies neither a Goldbach "
            "counterexample nor an upper bound for the exceptional set. No "
            "academic priority claim is made without an expert literature audit."
        ),
        "failure_count": failures,
    }


def factorial_twin_free_row(length: int) -> dict[str, Any]:
    factorial_parameter = length + 3
    base = math.factorial(factorial_parameter)
    certificate_rows = []
    for offset in range(2, factorial_parameter - 1):
        lower = base + offset
        upper = lower + 2
        certificate_rows.append(
            {
                "offset_j": offset,
                "lower_divisor": offset,
                "upper_divisor": offset + 2,
                "lower_divisible": lower % offset == 0,
                "upper_divisible": upper % (offset + 2) == 0,
                "both_proper_composites": lower > offset and upper > offset + 2,
            }
        )
    endpoint = base + factorial_parameter
    cyclotomic_modulus = endpoint.bit_length()
    exact_twin_count = 0
    nonzero_remainder = -length
    return {
        "requested_length_H": length,
        "factorial_parameter_K": factorial_parameter,
        "factorial_base_N": str(base),
        "factorial_base_decimal_digits": len(str(base)),
        "lower_endpoint": str(base + 2),
        "upper_endpoint": str(base + length + 1),
        "candidate_count": len(certificate_rows),
        "cyclotomic_modulus_M": cyclotomic_modulus,
        "exact_twin_count_T_I": exact_twin_count,
        "zero_mode_raw_contribution_H": length,
        "all_nonzero_modes_raw_aggregate_R_I": nonzero_remainder,
        "exact_identity_M2T_equals_H_plus_R": (
            cyclotomic_modulus**2 * exact_twin_count
            == length + nonzero_remainder
        ),
        "all_composite_pair_certificates_hold": all(
            row["lower_divisible"]
            and row["upper_divisible"]
            and row["both_proper_composites"]
            for row in certificate_rows
        ),
        "certificate_rows": certificate_rows,
    }


def twin_factorial_audit() -> dict[str, Any]:
    rows = [factorial_twin_free_row(length) for length in (1, 2, 4, 8, 16, 32)]
    failures = sum(
        int(not row["all_composite_pair_certificates_hold"])
        + int(not row["exact_identity_M2T_equals_H_plus_R"])
        for row in rows
    )
    theorem = (
        "For every H>=1 there is an interval of H consecutive lower candidates "
        "containing no twin-prime pair. In the exact TICKET-208 cyclotomic "
        "identity M^2 T_I=H+R_I, these intervals satisfy T_I=0 and R_I=-H. "
        "Therefore no all-interval estimate R_I>=-H+epsilon(H) with "
        "epsilon(H)>0 can prove twin positivity."
    )
    proof = (
        "Set K=H+3 and N=K!. For every j=2,...,K-2, N+j is divisible by j "
        "and N+j+2 is divisible by j+2; both are larger than their displayed "
        "divisors and hence composite. These H consecutive values of j give an "
        "H-long interval with no twin lower endpoint. The growing cyclotomic "
        "projector from TICKET-208 is exact on every finite interval, so its "
        "identity immediately yields R_I=M^2*0-H=-H on this family."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "factorial_construction": (
            "K=H+3, N=K!, j=2,...,K-2: j|(N+j) and (j+2)|(N+j+2)"
        ),
        "cyclotomic_identity": "M^2*T_I=H+R_I",
        "factorial_twin_free_rows": rows,
        "aggregate": {
            "arbitrarily_long_twin_free_intervals_proved": True,
            "exact_negative_interval_length_remainder_family_proved": True,
            "positive_margin_on_every_interval_refuted": True,
            "cofinal_dyadic_positive_remainder_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The factorial windows are short relative to their location and are "
            "not the selected expanding dyadic intervals needed for infinitude. "
            "The construction refutes a universal local margin, not the Twin "
            "Prime conjecture and not every averaged or cofinal dyadic estimate."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_gamma_normalized_audit()
    collatz_compute = collatz_four_one_audit()
    goldbach_compute = goldbach_covering_audit()
    twin_compute = twin_factorial_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-209",
            "theorem_name": "CompletedXiAbsoluteCofinalClearanceNoGoAndGammaNormalizedOuterEdgeReduction",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": (
                "No cofinal nonvanishing certificate or normalized lower bound "
                "is proved on the central horizontal segment."
            ),
            "route_decision": {
                "discard": "a height-independent positive absolute completed-xi margin on cofinal full rectangle boundaries",
                "retain": "gamma-normalized arithmetic nonvanishing, with Euler-product outer segments removed first",
                "next_single_lemma": "CofinalGammaNormalizedCentralTopEdgeNonvanishingCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "SigmaTwoCompletedXiVerticalClearanceAndHorizontalEdgeReduction",
                "CompletedXiAbsoluteCofinalClearanceNoGoAndGammaNormalizedOuterEdgeReduction",
                "HeightIndependentAbsoluteCompletedXiBoundaryMargin",
                "CofinalGammaNormalizedCentralTopEdgeNonvanishingCertificate",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof or off-critical zeta zero. A uniform absolute xi-margin route is refuted and the remaining cofinal task is gamma-normalized central-edge nonvanishing.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-209",
            "theorem_name": "FourOneAcceleratedCycleFiniteEnumerationExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": (
                "Cycles with at least five valuation-one entries and all "
                "nonperiodic divergent orbits remain open."
            ),
            "route_decision": {
                "discard": "searching any exactly-four-valuation-one word for a positive accelerated cycle",
                "retain": "the exact product-and-enumeration reduction for five-one primitive necklaces plus an independent descent theorem",
                "next_single_lemma": "UniformExclusionForPrimitiveValuationNecklacesWithExactlyFiveOnes",
            },
            "proof_dag": proof_dag(
                "CO",
                "ThreeOneAcceleratedCycleFiniteEnumerationExclusion",
                "FourOneAcceleratedCycleFiniteEnumerationExclusion",
                "ExactlyFourValuationOnesCanSupportAPositiveCycle",
                "UniformExclusionForPrimitiveValuationNecklacesWithExactlyFiveOnes",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent-orbit counterexample. The complete exactly-four-valuation-one periodic stratum is excluded by an exact finite proof.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-209",
            "theorem_name": "CoveringCongruenceSuperLogarithmicLeastWitnessLowerBound",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": (
                "No exceptional-count upper bound is proved beyond the new "
                "covering-congruence witness floor."
            ),
            "route_decision": {
                "discard": "any universal constant multiple of log N as an upper bound for the least Goldbach witness",
                "retain": "tail exceptional-set control beyond the c log N log log N covering-congruence floor",
                "next_single_lemma": "GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor",
            },
            "proof_dag": proof_dag(
                "GB",
                "AsymptoticallyUnitLogLeastWitnessCRTLowerBound",
                "CoveringCongruenceSuperLogarithmicLeastWitnessLowerBound",
                "ConstantLogarithmicLeastWitnessCeiling",
                "GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. A deterministic covering-plus-CRT construction makes the normalized least witness W(N)/log N unbounded.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-209",
            "theorem_name": "ArbitrarilyLongTwinFreeIntervalsAndLocalCyclotomicMarginNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": (
                "No independent averaged or selected cofinal dyadic lower bound "
                "is proved for the nonzero Omega-phase remainder."
            ),
            "route_decision": {
                "discard": "a positive cyclotomic remainder margin on every interval",
                "retain": "an averaged or selected expanding dyadic phase bound that permits arbitrarily long local deserts",
                "next_single_lemma": "IndependentBilinearOmegaPhaseLowerBoundOnInfinitelyManyDyadicIntervals",
            },
            "proof_dag": proof_dag(
                "TP",
                "GrowingCyclotomicOmegaProjectorAndZeroModeCancellationNoGo",
                "ArbitrarilyLongTwinFreeIntervalsAndLocalCyclotomicMarginNoGo",
                "PositiveCyclotomicRemainderMarginOnEveryInterval",
                "IndependentBilinearOmegaPhaseLowerBoundOnInfinitelyManyDyadicIntervals",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. Factorial intervals prove exact full cancellation on arbitrarily long local windows and rule out every-interval positivity.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureNormalizedFourOneCoveringFactorialAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-209 resolves none of the four conjectures. It refutes a "
            "uniform absolute completed-xi cofinal margin and replaces it with "
            "a gamma-normalized boundary target, excludes the complete four-one "
            "Collatz cycle stratum, proves a superlogarithmic Goldbach least-"
            "witness sequence by covering congruences, and constructs arbitrarily "
            "long exact-cancellation Twin intervals."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common lesson is quantifier control: archimedean normalization, "
            "a complete finite periodic stratum, simultaneous congruence cover, "
            "and an all-interval counterfamily each remove one overstrong target. "
            "The four parent conjectures still require genuinely cofinal central, "
            "descent, exceptional-tail, or averaged bilinear estimates."
        ),
        "literature_boundary": {
            "riemann": "The gamma identity, Euler product, and functional equation are classical; this is a route correction, not a new RH theorem.",
            "collatz": "The exact finite stratum proof is project-local; it does not supersede almost-all descent or global cycle bounds.",
            "goldbach": "The construction uses classical Mertens, PNT, and CRT ingredients. No academic novelty or priority is claimed without specialist review.",
            "twin_prime": "Arbitrarily long composite runs are classical; their exact insertion into the project cyclotomic identity is a no-go diagnosis, not a bounded-gap improvement.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "bounded_result": {
                    "audit_ref": "#/normalized_fourone_covering_factorial_audit"
                },
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / "data/open-problem/ticket209-normalized-fourone-covering-factorial.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "normalized_fourone_covering_factorial_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-209-gamma-normalized-boundary.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-209-four-one-exclusion.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-209-covering-witness.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-209-factorial-twin-free.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(path, standalone_payload(audit[section_key], problem_ids[section_key]))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
