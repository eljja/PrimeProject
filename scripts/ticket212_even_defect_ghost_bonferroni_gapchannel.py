from __future__ import annotations

import bisect
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket212-even-defect-ghost-bonferroni-gapchannel.v1"
GENERATED_AT = "2026-08-12T23:55:00+09:00"
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
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T211", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T212", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N212",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN212",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T211", f"{prefix}-T212"],
            [f"{prefix}-T212", f"{prefix}-N212"],
            [f"{prefix}-T212", f"{prefix}-OPEN212"],
            [f"{prefix}-OPEN212", prefix],
        ],
    }


def zero_configuration_row(
    label: str,
    critical_line_multiplicities: tuple[int, ...],
    off_line_pairs: int,
    certified_sign_changes: int,
) -> dict[str, Any]:
    odd_line_zeros = sum(value % 2 for value in critical_line_multiplicities)
    total = sum(critical_line_multiplicities) + 2 * off_line_pairs
    if certified_sign_changes > odd_line_zeros:
        raise ValueError("certified sign changes exceed available odd line zeros")
    defect = total - certified_sign_changes
    all_line_simple = off_line_pairs == 0 and all(
        value == 1 for value in critical_line_multiplicities
    )
    return {
        "configuration": label,
        "critical_line_multiplicities": list(critical_line_multiplicities),
        "off_critical_symmetric_pairs": off_line_pairs,
        "total_upper_rectangle_zero_count_N": total,
        "available_odd_line_sign_changes": odd_line_zeros,
        "certified_disjoint_sign_changes_L": certified_sign_changes,
        "uncertified_defect_N_minus_L": defect,
        "subtwo_certificate_applies": defect < 2,
        "all_zeros_on_line_and_simple": all_line_simple,
    }


def riemann_even_defect_audit() -> dict[str, Any]:
    rows = [
        zero_configuration_row("all_line_certified", (1, 1, 1, 1), 0, 4),
        zero_configuration_row("one_unseen_simple_line_zero", (1, 1, 1), 0, 2),
        zero_configuration_row("one_off_line_pair", (1, 1, 1), 1, 3),
        zero_configuration_row("one_double_line_zero", (1, 1, 2), 0, 2),
        zero_configuration_row("ticket211_symmetric_off_line_model_band", (), 1, 0),
    ]
    failures = 0
    for row in rows:
        if row["subtwo_certificate_applies"]:
            failures += int(not row["all_zeros_on_line_and_simple"])
    failures += int(rows[-1]["uncertified_defect_N_minus_L"] != 2)

    theorem = (
        "Let R be an upper-half critical-strip rectangle invariant under "
        "s->1-conjugate(s), with no boundary zeros, and let N be its total "
        "zero count with multiplicity. Suppose L disjoint critical-line "
        "intervals have rigorously certified sign changes of the real Hardy "
        "function. If N-L<2, then every zero in R is simple and lies on the "
        "critical line. The constant two is sharp: one symmetric off-line "
        "pair, or one double critical-line zero, has defect exactly two."
    )
    proof = (
        "Each certified sign change contains a distinct critical-line zero of "
        "odd multiplicity. Let O be the total number of distinct odd-multiplicity "
        "critical-line zeros. Functional and conjugation symmetry pair every "
        "off-line upper-half zero with 1-conjugate(rho). Hence N-O equals twice "
        "the off-line multiplicity plus, for each line zero of multiplicity m, "
        "the even integer m-(m mod 2). Thus N-O is a nonnegative even integer. "
        "Since O>=L, N-L=(N-O)+(O-L). If N-L<2, the even term N-O must be zero; "
        "there are no off-line zeros and every line multiplicity is one. At "
        "most one simple line zero can remain outside the certified intervals. "
        "An off-line pair or a double line zero realizes defect two."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "defect_identity": (
            "N-O=2*(off-line upper-half multiplicity pairs)"
            "+sum_line(m-(m mod 2))"
        ),
        "threshold": "N-L<2",
        "configuration_rows": rows,
        "aggregate": {
            "subtwo_defect_certificate_proved": True,
            "threshold_two_is_sharp": True,
            "ticket211_defect_equals_sharp_boundary": True,
            "all_height_subtwo_bound_for_actual_zeta_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem is an exact counting certificate, not a new zeta-zero "
            "verification. PrimeProject does not compute rigorous interval "
            "values of the Hardy function or extend the published finite-height "
            "verification. The unbounded-height defect estimate remains open."
        ),
        "failure_count": failures,
    }


def collatz_word_data(word: tuple[int, ...]) -> dict[str, Any]:
    length = len(word)
    valuation_sum = sum(word)
    prefix_sum = 0
    cycle_numerator = 0
    for index, valuation in enumerate(word):
        cycle_numerator += 3 ** (length - 1 - index) * 2**prefix_sum
        prefix_sum += valuation
    odd_divisor = 2**valuation_sum - 3**length
    ghost = Fraction(cycle_numerator, odd_divisor)

    orbit = [ghost]
    current = ghost
    exact_valuations = []
    for valuation in word:
        numerator = 3 * current + 1
        integer_numerator = numerator.numerator
        exponent = 0
        while integer_numerator % 2 == 0:
            exponent += 1
            integer_numerator //= 2
        exact_valuations.append(exponent)
        current = numerator / 2**valuation
        orbit.append(current)

    return {
        "word": list(word),
        "length_h": length,
        "valuation_sum_A": valuation_sum,
        "valuation_one_count_k": word.count(1),
        "cycle_numerator_C": cycle_numerator,
        "odd_divisor_D": odd_divisor,
        "ghost_fixed_point": str(ghost),
        "ghost_reduced_denominator": ghost.denominator,
        "ghost_is_two_adic_integer": ghost.denominator % 2 == 1,
        "ghost_is_positive_rational": ghost > 0,
        "ghost_is_positive_integer": ghost.denominator == 1 and ghost > 0,
        "ordinary_integrality_D_divides_C": cycle_numerator % abs(odd_divisor) == 0,
        "prescribed_valuations_replayed": exact_valuations == list(word),
        "cycle_closes_exactly": current == ghost,
        "orbit": [str(value) for value in orbit[:-1]],
    }


def collatz_two_adic_ghost_audit() -> dict[str, Any]:
    density_floor = math.log(Fraction(6, 5), 2)
    family_rows = [collatz_word_data((1, 2, 2) * repetitions) for repetitions in range(1, 9)]

    enumeration_rows = []
    total_failures = 0
    for length in range(1, 9):
        words_tested = 0
        positive_contracting = 0
        above_density_floor = 0
        automatic_two_adic = 0
        positive_integer = 0
        transcript = []
        for word in itertools.product(range(1, 5), repeat=length):
            words_tested += 1
            data = collatz_word_data(word)
            if data["odd_divisor_D"] <= 0:
                continue
            positive_contracting += 1
            if word.count(1) / length < density_floor:
                continue
            above_density_floor += 1
            automatic_two_adic += int(data["ghost_is_two_adic_integer"])
            positive_integer += int(data["ghost_is_positive_integer"])
            total_failures += int(not data["prescribed_valuations_replayed"])
            total_failures += int(not data["cycle_closes_exactly"])
            transcript.append(
                f"{','.join(map(str, word))}:{data['cycle_numerator_C']}:"
                f"{data['odd_divisor_D']}:{data['ghost_reduced_denominator']}"
            )
        total_failures += int(automatic_two_adic != above_density_floor)
        enumeration_rows.append(
            {
                "length_h": length,
                "alphabet": "valuations 1..4",
                "words_tested": words_tested,
                "positive_contracting_words": positive_contracting,
                "above_ticket211_density_floor": above_density_floor,
                "two_adic_ghosts": automatic_two_adic,
                "positive_integer_fixed_points": positive_integer,
                "transcript_sha256": hashlib.sha256(
                    "\n".join(transcript).encode("ascii")
                ).hexdigest(),
            }
        )

    for row in family_rows:
        total_failures += int(not row["ghost_is_two_adic_integer"])
        total_failures += int(row["ghost_reduced_denominator"] != 5)

    theorem = (
        "For every nonempty accelerated-Collatz valuation word "
        "w=(a_1,...,a_h), put A=sum a_i and "
        "C=sum_{j=0}^{h-1}3^{h-1-j}2^{a_1+...+a_j}, with the empty prefix "
        "equal to zero. The formal cycle has the unique fixed point "
        "x=C/(2^A-3^h). Both C and 2^A-3^h are odd, so x is always a "
        "2-adic integer and the prescribed valuation cycle is realized in "
        "Z_2. Therefore no obstruction based only on membership in Z_2 can "
        "exclude any high-one-density word. A positive integer cycle instead "
        "requires 2^A-3^h>0 and the ordinary odd divisibility "
        "2^A-3^h divides C."
    )
    proof = (
        "Composing x->(3x+1)/2^{a_i} gives "
        "T_w(x)=(3^h x+C)/2^A, so its fixed point is the displayed rational. "
        "The first term of C is odd and every later term is even; the divisor "
        "is even minus odd. Hence the reduced denominator remains odd and x "
        "belongs to Z_2. Applying each affine step produces the corresponding "
        "cyclic rotation, which is again odd in Z_2, so v_2(3x_i+1)=a_i and "
        "the word closes exactly. Ordinary positivity needs the divisor to be "
        "positive, while membership in Z requires the odd divisor to divide C. "
        "The family (1,2,2)^m has ghost 23/5 for every m, proving that even "
        "the TICKET-211 density floor does not repair the 2-adic no-go."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "corrected_integrality_predicate": "(2^A-3^h)>0 and (2^A-3^h)|C",
        "density_floor_decimal": f"{density_floor:.12f}",
        "ghost_family_rows": family_rows,
        "finite_word_enumeration": enumeration_rows,
        "aggregate": {
            "two_adic_ghost_exists_for_every_valuation_word": True,
            "uniform_two_adic_membership_obstruction_refuted": True,
            "ordinary_odd_divisibility_identified": True,
            "odd_divisibility_excluded_for_all_high_density_words": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This proves that Z_2 membership and local valuation replay are "
            "vacuous as exclusion tests. It does not prove uniform failure of "
            "the ordinary divisibility D|C, does not exclude divergent integer "
            "orbits, and produces no positive integer Collatz counterexample."
        ),
        "failure_count": total_failures,
    }


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            flags[candidate * candidate : limit + 1 : candidate] = b"\x00" * (
                (limit - candidate * candidate) // candidate + 1
            )
    return flags


def goldbach_witness_count(target: int, flags: bytearray, primes: list[int]) -> int:
    return sum(
        1
        for prime in primes
        if prime <= target // 2 and flags[target - prime]
    )


def even_bonferroni_sum(witness_count: int, order: int) -> int:
    if order % 2:
        raise ValueError("the upper Bonferroni order must be even")
    return sum(
        (-1) ** index * math.comb(witness_count, index)
        for index in range(min(order, witness_count) + 1)
    )


def goldbach_bonferroni_audit(limit: int = 2_000_000) -> dict[str, Any]:
    flags = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if flags[value]]
    target_rows = []
    failures = 0
    for target in (100, 1_000, 10_000, 100_000, 1_000_000, 2_000_000):
        count = goldbach_witness_count(target, flags, primes)
        row = {
            "even_target_N": target,
            "unordered_full_range_witness_count_A": count,
            "exact_zero_indicator_product": int(count == 0),
            "bonferroni_order_2": str(even_bonferroni_sum(count, 2)),
            "bonferroni_order_4": str(even_bonferroni_sum(count, 4)),
            "bonferroni_order_6": str(even_bonferroni_sum(count, 6)),
        }
        failures += int(count <= 0)
        target_rows.append(row)

    identity_rows = []
    for witnesses in range(13):
        for order in (0, 2, 4, 6):
            value = even_bonferroni_sum(witnesses, order)
            closed_form = (
                1
                if witnesses == 0
                else math.comb(witnesses - 1, order)
            )
            failures += int(value != closed_form)
            identity_rows.append(
                {
                    "witness_count_A": witnesses,
                    "even_truncation_order": order,
                    "bonferroni_upper_bound": str(value),
                    "closed_form": str(closed_form),
                    "exact_zero_indicator": int(witnesses == 0),
                    "false_positive": witnesses > order and value > 0,
                }
            )

    multiplicity_rows = []
    for cutoff in (1_000, 10_000, 100_000, 1_000_000, 2_000_000):
        odd_prime_count = bisect.bisect_right(primes, cutoff) - 1
        unordered_odd_prime_pairs = odd_prime_count * (odd_prime_count + 1) // 2
        even_target_bins = cutoff - 2
        pigeonhole_lower_bound = (
            unordered_odd_prime_pairs + even_target_bins - 1
        ) // even_target_bins
        multiplicity_rows.append(
            {
                "prime_cutoff_x": cutoff,
                "odd_prime_count": odd_prime_count,
                "unordered_odd_prime_pair_count": unordered_odd_prime_pairs,
                "possible_even_sums_6_through_2x": even_target_bins,
                "maximum_representation_count_lower_bound": pigeonhole_lower_bound,
            }
        )

    theorem = (
        "For an even N let y_p=1 if N-p is prime, for primes p<=N/2, and "
        "let A(N)=sum y_p. The full Goldbach-exception indicator is exactly "
        "I_0(N)=product_{p<=N/2}(1-y_p). Its inclusion-exclusion truncation "
        "through any fixed even order 2r is an upper bound, but for A>=1 it "
        "equals binomial(A-1,2r). Hence every represented target with "
        "A>=2r+1 contributes at least one false exception. Moreover, the "
        "prime number theorem and an exact pigeonhole count over unordered "
        "pairs of odd primes imply that A(N) is unbounded. Therefore every "
        "fixed-order, unnormalized Bonferroni upper bound is at least one on "
        "arbitrarily large represented targets and cannot prove all "
        "sufficiently large dyadic full-range exception counts below one."
    )
    proof = (
        "The product is one exactly when every witness bit is zero and is zero "
        "otherwise. Expanding it gives the complete inclusion-exclusion sum. "
        "For integer A>=1, Pascal's identity yields "
        "sum_{j=0}^{k}(-1)^j binomial(A,j)=(-1)^k binomial(A-1,k), with "
        "the binomial interpreted as zero when k>A-1. At even k=2r this is "
        "a nonnegative upper bound and is at least one once A>=2r+1. Thus "
        "larger representation multiplicity worsens the fixed-order upper "
        "bound. For odd primes p<=q<=x there are P(P+1)/2 unordered pairs, "
        "where P=pi(x)-1, distributed over at most x-2 even sums from 6 "
        "through 2x. Some target therefore has at least "
        "ceil(P(P+1)/(2(x-2))) representations. By the prime number theorem "
        "this lower bound is asymptotic to x/(2 log(x)^2) and tends to "
        "infinity. Hence every fixed 2r fails on arbitrarily large targets. "
        "The full product or a uniformly controlled resummation is required "
        "before an integer-below-one argument can close Goldbach."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_exception_indicator": "I_0(N)=product_{p<=N/2}(1-1_P(N-p))",
        "even_truncation_identity": (
            "sum_{j=0}^{2r}(-1)^j*C(A,j)=C(A-1,2r) for A>=1"
        ),
        "identity_rows": identity_rows,
        "representation_multiplicity_lower_bound_rows": multiplicity_rows,
        "finite_target_rows": target_rows,
        "finite_limit": limit,
        "aggregate": {
            "full_witness_product_identity_proved": True,
            "fixed_even_bonferroni_route_refuted": True,
            "unbounded_representation_multiplicity_from_pnt_proved": True,
            "finite_targets_all_represented": True,
            "uniform_resummed_product_bound_below_one_proved": False,
            "goldbach_counterexample_found": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The Bonferroni identity and pair-count pigeonhole argument are "
            "exact; unbounded multiplicity imports the prime number theorem. "
            "They reject only fixed-order inclusion-exclusion. The finite "
            "targets are diagnostics, not a Goldbach tail theorem. No "
            "minor-arc cancellation or strictly subunit full exception bound "
            "is proved."
        ),
        "failure_count": failures,
    }


def twin_gap_channel_rows(limit: int = 10_000_000) -> list[dict[str, Any]]:
    flags = prime_sieve(limit + 32)
    primes = [value for value in range(2, limit + 1) if flags[value]]
    gaps = tuple(range(2, 31, 2))
    rows = []
    lower = 32
    while 2 * lower <= limit:
        upper = 2 * lower
        start = bisect.bisect_left(primes, lower)
        stop = bisect.bisect_left(primes, upper)
        counts = {
            str(gap): sum(1 for prime in primes[start:stop] if flags[prime + gap])
            for gap in gaps
        }
        transcript = ";".join(f"{gap}:{counts[str(gap)]}" for gap in gaps)
        rows.append(
            {
                "dyadic_lower_X": lower,
                "dyadic_upper_2X": upper,
                "gap_channel_counts": counts,
                "gap_two_positive": counts["2"] > 0,
                "bounded_gap_aggregate": sum(counts.values()),
                "dominant_gap_channel": max(gaps, key=lambda gap: counts[str(gap)]),
                "transcript_sha256": hashlib.sha256(
                    transcript.encode("ascii")
                ).hexdigest(),
            }
        )
        lower *= 2
    return rows


def twin_gap_channel_audit() -> dict[str, Any]:
    rows = twin_gap_channel_rows()
    countermodel_rows = [
        {
            "dyadic_index_j": index,
            "gap_2_channel": 0,
            "gap_6_channel": 1,
            "all_other_channels": 0,
            "finite_gap_aggregate": 1,
        }
        for index in range(10, 21)
    ]
    failures = sum(
        int(not row["gap_two_positive"])
        + int(row["bounded_gap_aggregate"] <= 0)
        for row in rows
    )

    theorem = (
        "Let T_{j,h} count prime pairs p,p+h with 2^j<=p<2^{j+1}, for "
        "even h in a fixed finite set H containing 2. The twin-prime "
        "conjecture is equivalent to T_{j,2}>0 for infinitely many j. If "
        "sum_{h in H}T_{j,h}>0 for infinitely many j, finite pigeonhole only "
        "implies that some h in H is positive infinitely often; it does not "
        "select h=2. The exact countermodel T_{j,6}=1 and T_{j,h}=0 for "
        "h!=6 has positive bounded-gap aggregate on every block and no "
        "gap-two mass."
    )
    proof = (
        "Every twin pair belongs to one dyadic block, and each bounded block "
        "contains finitely many integers, so infinitely many twin pairs are "
        "equivalent to gap-two positivity on infinitely many dyadic indices. "
        "For a finite channel set H, infinitely many positive aggregate "
        "blocks contain infinitely many occurrences distributed among "
        "finitely many h; one channel therefore recurs infinitely often. "
        "Nothing in this pigeonhole statement identifies that channel as two, "
        "as the gap-six countermodel proves. Thus bounded-gap positivity and "
        "even exact aggregate mass require a gap-two channel-isolation input."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "minimal_dyadic_equivalence": (
            "infinitely many twin primes iff T_{j,2}>0 for infinitely many j"
        ),
        "finite_channel_set": list(range(2, 31, 2)),
        "countermodel_rows": countermodel_rows,
        "finite_prime_channel_rows": rows,
        "finite_limit": 10_000_000,
        "aggregate": {
            "dyadic_gap_two_equivalence_proved": True,
            "bounded_gap_aggregate_selects_gap_two_refuted": True,
            "finite_gap_two_blocks_all_positive": True,
            "gap_two_positive_on_infinitely_many_blocks_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The channel countermodel is logical, not a model of the primes, "
            "and does not weaken bounded-gap theorems. The sieve through ten "
            "million is finite. No parity-breaking lower bound for the actual "
            "gap-two channel is obtained."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_even_defect_audit()
    collatz_compute = collatz_two_adic_ghost_audit()
    goldbach_compute = goldbach_bonferroni_audit()
    twin_compute = twin_gap_channel_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-212",
            "theorem_name": "EvenCriticalLineDefectSubTwoSaturationCertificate",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No all-height bound N-L<2 is proved for the actual completed zeta function.",
            "route_decision": {
                "discard": "requiring exact equality N=L when the symmetry-quantized sufficient threshold is N-L<2",
                "retain": "a rigorous all-height total-count minus certified-line-count defect strictly below two",
                "next_single_lemma": "UniformAllHeightCriticalLineDefectStrictlyBelowTwo",
            },
            "proof_dag": proof_dag(
                "RH",
                "EffectiveCriticalLineRectangleZeroCountEqualityCertificate",
                "EvenCriticalLineDefectSubTwoSaturationCertificate",
                "ExactEqualityIsTheMinimalSaturationThreshold",
                "UniformAllHeightCriticalLineDefectStrictlyBelowTwo",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-critical zeta zero. An exact symmetry-parity theorem relaxes finite-rectangle saturation from equality to a sharp sub-two defect.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-212",
            "theorem_name": "TwoAdicGhostUniversalityAndOddDivisibilityCorrection",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The ordinary odd divisibility D|C is not excluded uniformly, and nonperiodic divergence remains open.",
            "route_decision": {
                "discard": "searching for a Z_2-membership obstruction, because every valuation word has a two-adic ghost cycle",
                "retain": "uniform ordinary odd-divisor nondivisibility for every positive high-one-density word",
                "next_single_lemma": "UniformOddDivisorNondivisibilityForHighOneDensityWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "Uniform2AdicIntegralityObstructionForHighOneDensityWords",
                "TwoAdicGhostUniversalityAndOddDivisibilityCorrection",
                "TwoAdicMembershipCanExcludeHighDensityCycleWords",
                "UniformOddDivisorNondivisibilityForHighOneDensityWords",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or positive integer counterexample. The proposed 2-adic membership obstruction is refuted and replaced by the exact ordinary odd-divisibility predicate.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-212",
            "theorem_name": "FullWitnessProductIdentityAndFixedBonferroniNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No uniformly controlled full-product resummation or subunit tail exceptional bound is proved.",
            "route_decision": {
                "discard": "using any fixed even-order unnormalized Bonferroni truncation to upper-bound the full exception count below one",
                "retain": "a uniformly controlled resummation of the full witness product with dyadic total below one",
                "next_single_lemma": "UniformFullWitnessProductResummationBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "FullRangeBinaryGoldbachExceptionalCountStrictlyBelowOne",
                "FullWitnessProductIdentityAndFixedBonferroniNoGo",
                "FixedOrderBonferroniUpperBoundCanCloseFullExceptions",
                "UniformFullWitnessProductResummationBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The exact full-range exception product is identified and every fixed even Bonferroni truncation is ruled out as a subunit upper-bound route.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-212",
            "theorem_name": "DyadicGapTwoEquivalenceAndFiniteGapAggregateNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No arithmetic lower bound selects the actual gap-two channel on infinitely many dyadic blocks.",
            "route_decision": {
                "discard": "promoting positive bounded-gap aggregate mass to gap-two positivity without a channel-isolation theorem",
                "retain": "actual prime-indicator gap-two positivity on infinitely many dyadic blocks",
                "next_single_lemma": "GapTwoDyadicChannelPositiveOnInfinitelyManyBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "SparseDyadicBilinearOmegaStrictPositivity",
                "DyadicGapTwoEquivalenceAndFiniteGapAggregateNoGo",
                "FiniteBoundedGapAggregateSelectsGapTwo",
                "GapTwoDyadicChannelPositiveOnInfinitelyManyBlocks",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. The minimal dyadic gap-two quantifier is isolated, and aggregate bounded-gap positivity is proved insufficient to select it.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "EvenDefectGhostBonferroniGapChannelAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-212 proves four exact partial or no-go theorems and resolves "
            "none of the parent conjectures. It supplies a sharp sub-two RH "
            "saturation certificate, corrects a vacuous Collatz 2-adic target, "
            "rejects fixed-order Goldbach Bonferroni closure, and separates "
            "bounded-gap aggregate positivity from the gap-two channel."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Each track contains a quantized missing unit: two zero-count units "
            "for RH symmetry, an odd ordinary divisor for Collatz integrality, "
            "the complete witness product for Goldbach exceptions, and the "
            "specific gap-two channel for Twin Prime. Aggregate or local data "
            "that omit that unit cannot close the corresponding conjecture."
        ),
        "literature_boundary": {
            "riemann": "Platt and Trudgian rigorously verified RH through height 3e12 using interval arithmetic and Turing's method. PrimeProject proves only an abstract defect-count lemma and performs no new zeta verification.",
            "collatz": "A 2026 Dhiman-Pandey preprint independently develops two-adic ghost cycles and non-semilinearity of the ordinary divisibility predicate. PrimeProject claims no priority for ghost-cycle universality.",
            "goldbach": "The finite computation is far below the published verification through 4e18 and supplies no new analytic Goldbach range.",
            "twin_prime": "Maynard's bounded-gap theorem does not select gap two; the channel countermodel is elementary and is not an improvement to bounded-gap constants.",
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
                    "audit_ref": "#/even_defect_ghost_bonferroni_gapchannel_audit"
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
    integrated = ROOT / "data/open-problem/ticket212-even-defect-ghost-bonferroni-gapchannel.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "even_defect_ghost_bonferroni_gapchannel_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-212-even-defect-saturation.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-212-two-adic-ghost-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-212-full-witness-bonferroni.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-212-gap-channel-isolation.json",
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
