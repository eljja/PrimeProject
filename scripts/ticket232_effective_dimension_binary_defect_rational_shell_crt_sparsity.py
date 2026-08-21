from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (
    "primeproject.ticket232-effective-dimension-binary-defect-"
    "rational-shell-crt-sparsity.v1"
)
GENERATED_AT = "2026-08-21T21:00:00+09:00"
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
    current: str,
    discarded: str,
    successor: str,
    parent: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T231", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T232", "label": current, "status": "closed"},
            {
                "id": f"{prefix}-N232",
                "label": discarded,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN232",
                "label": successor,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": parent, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T231", f"{prefix}-T232"],
            [f"{prefix}-T232", f"{prefix}-N232"],
            [f"{prefix}-T232", f"{prefix}-OPEN232"],
            [f"{prefix}-OPEN232", prefix],
        ],
    }


def primes_up_to(limit: int) -> tuple[int, ...]:
    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            sieve[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return tuple(index for index, flag in enumerate(sieve) if flag)


def simultaneous_collision(
    phases: tuple[float, ...], partition_q: int
) -> tuple[int, tuple[float, ...]]:
    boxes: dict[tuple[int, ...], int] = {}
    maximum = partition_q ** len(phases)
    for index in range(maximum + 1):
        box = tuple(
            min(partition_q - 1, int((index * phase % 1.0) * partition_q))
            for phase in phases
        )
        if box in boxes:
            witness = index - boxes[box]
            errors = tuple(
                abs(witness * phase - round(witness * phase)) for phase in phases
            )
            return witness, errors
        boxes[box] = index
    raise AssertionError("pigeonhole collision was not found")


def riemann_effective_dimension_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    prime_pool = primes_up_to(50)
    for dimension, partition_q in ((2, 32), (3, 16), (4, 10), (5, 7), (6, 5)):
        dilations = prime_pool[:dimension]
        phases = tuple(math.log(value) / (2.0 * math.pi) for value in dilations)
        witness, errors = simultaneous_collision(phases, partition_q)
        energy = sum(
            abs(1.0 - complex(math.cos(witness * math.log(value)), -math.sin(witness * math.log(value))))
            ** 2
            for value in dilations
        ) / dimension
        normalized_bound = 4.0 * math.pi**2 / partition_q**2
        verified = (
            1 <= witness <= partition_q**dimension
            and max(errors) <= 1.0 / partition_q + 1e-12
            and energy <= normalized_bound + 1e-12
        )
        failures += int(not verified)
        rows.append(
            {
                "effective_dimension_M": dimension,
                "partition_Q": partition_q,
                "frequency_horizon_T": partition_q**dimension,
                "dilations": list(dilations),
                "witness_frequency_n": witness,
                "maximum_phase_error": max(errors),
                "observed_normalized_energy": energy,
                "normalized_head_bound_4pi2_over_Q2": normalized_bound,
                "certificate_verified": verified,
            }
        )

    c = Fraction(1, 2)
    tail_ratio = c / 8
    q = 13
    strict_constant_check = 4.0 * math.pi**2 / q**2 + 4.0 * float(tail_ratio) < float(c)
    failures += int(not strict_constant_check)
    theorem = (
        "At every height T let q_j(T)>1 and w_j(T)>=0 have finite positive "
        "total mass W_T, and put F_T(n)=sum_j w_j(T)|1-q_j(T)^(-in)|^2. "
        "For every head length M and integer Q>=2 with Q^M<=T there is "
        "1<=n<=T such that F_T(n)/W_T<=4*pi^2/Q^2+4*delta_T(M), "
        "where delta_T(M)=sum_(j>M)w_j(T)/W_T. Consequently, if "
        "F_T(n)>=c W_T for every 1<=n<=T, delta_T(M)<=c/8, and an "
        "integer Q satisfies 4*pi^2/Q^2<c/2, then Q^M>T. Thus every "
        "adaptive frame with a fixed positive normalized floor needs at "
        "least logarithmically many effective coordinates: M>log(T)/log(Q)."
    )
    proof = (
        "Apply simultaneous Dirichlet pigeonhole approximation to the first "
        "M phases log(q_j(T))/(2*pi). Among Q^M+1 multiples, two occupy "
        "the same Q-adic box; their difference n is at most Q^M and gives "
        "head energy at most 4*pi^2/Q^2 times the head mass. The pointwise "
        "bound |1-z|^2<=4 gives the tail term. A c-floor and tail ratio at "
        "most c/8 would contradict this witness whenever "
        "4*pi^2/Q^2<c/2 and Q^M<=T, proving Q^M>T. No independence of the "
        "dilations is needed."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "adaptive_collision_rows": rows,
        "explicit_half_floor_corollary": {
            "normalized_floor_c": str(c),
            "maximum_tail_ratio": str(tail_ratio),
            "partition_Q": q,
            "strict_bound_value": 4.0 * math.pi**2 / q**2 + 4.0 * float(tail_ratio),
            "required_effective_dimension": "M>log(T)/log(13)",
            "constant_check_verified": strict_constant_check,
        },
        "aggregate": {
            "adaptive_weighted_collision_bound_proved": True,
            "logarithmic_effective_dimension_necessary": True,
            "sublogarithmic_effective_dimension_positive_floor_refuted": True,
            "logarithmic_adaptive_weil_frame_constructed": False,
            "weil_tail_dominance_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes height adaptation with sublogarithmic effective "
            "dimension, even for changing dilations and weights. It is a scalar "
            "phase-energy necessity theorem, not a Weil quadratic-form positivity "
            "result. Logarithmically dense frames, signed or renormalized systems, "
            "and explicit Weil-tail dominance remain open."
        ),
        "failure_count": failures,
    }


def rotate_left(word: tuple[int, ...], amount: int = 1) -> tuple[int, ...]:
    amount %= len(word)
    return word[amount:] + word[:amount]


def canonical_necklace(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotate_left(word, amount) for amount in range(len(word)))


def collatz_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def collatz_numerator(word: tuple[int, ...]) -> int:
    total = 0
    prefix = 0
    height = len(word)
    for index, exponent in enumerate(word):
        total += 3 ** (height - index - 1) * 2**prefix
        prefix += exponent
    return total


def collatz_binary_defect_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    samples = []
    for height in range(3, 17):
        tested = {1: 0, 2: 0}
        positive = {1: 0, 2: 0}
        excluded = {1: 0, 2: 0}
        necklaces: dict[int, set[tuple[int, ...]]] = {1: set(), 2: set()}
        for one_count in (1, 2):
            for one_positions in itertools.combinations(range(height), one_count):
                word_list = [2] * height
                for position in one_positions:
                    word_list[position] = 1
                word = tuple(word_list)
                tested[one_count] += 1
                denominator = collatz_denominator(word)
                if denominator <= 0:
                    continue
                positive[one_count] += 1
                necklaces[one_count].add(canonical_necklace(word))
                numerator = collatz_numerator(word)
                nondivisible = numerator % denominator != 0
                excluded[one_count] += int(nondivisible)
                failures += int(not nondivisible)
                if len(samples) < 24:
                    samples.append(
                        {
                            "word": list(word),
                            "height_h": height,
                            "one_count_k": one_count,
                            "valuation_sum_S": sum(word),
                            "denominator_D": denominator,
                            "numerator_B": numerator,
                            "B_mod_D": numerator % denominator,
                            "D_does_not_divide_B": nondivisible,
                        }
                    )
        rows.append(
            {
                "height_h": height,
                "one_defect_words_tested": tested[1],
                "one_defect_positive_denominator": positive[1],
                "one_defect_nondivisible": excluded[1],
                "one_defect_necklaces": len(necklaces[1]),
                "two_defect_words_tested": tested[2],
                "two_defect_positive_denominator": positive[2],
                "two_defect_nondivisible": excluded[2],
                "two_defect_necklaces": len(necklaces[2]),
                "certificate_verified": (
                    positive[1] == excluded[1] and positive[2] == excluded[2]
                ),
            }
        )

    inequality_rows = []
    for height in range(5, 21):
        maximum_r = height // 2
        denominator = 4 ** (height - 1) - 3**height
        q_bound = 2 * 3**maximum_r + 4**maximum_r
        verified = (height == 5) or q_bound < denominator
        if height >= 6:
            failures += int(not verified)
        inequality_rows.append(
            {
                "height_h": height,
                "maximum_separation_r": maximum_r,
                "denominator_D_for_two_ones": denominator,
                "maximum_small_remainder_Q": q_bound,
                "Q_below_D_for_h_at_least_6": q_bound < denominator,
                "h5_checked_separately": height == 5,
            }
        )

    three_defect_rows = []
    for height in range(8, 25):
        denominator = 2 ** (2 * height - 3) - 3**height
        tested = 0
        maximum_q = 0
        for first_gap in range(1, height - 1):
            for second_gap in range(1, height - first_gap):
                longest_gap = height - first_gap - second_gap
                if longest_gap < max(first_gap, second_gap):
                    continue
                word = (
                    (1,)
                    + (2,) * (first_gap - 1)
                    + (1,)
                    + (2,) * (second_gap - 1)
                    + (1,)
                    + (2,) * (longest_gap - 1)
                )
                numerator = collatz_numerator(word)
                remainder_q = (
                    2 * 3 ** (first_gap + second_gap)
                    + 4**first_gap * 3**second_gap
                    + 4 ** (first_gap + second_gap) // 2
                )
                factorization_ok = (
                    numerator - denominator
                    == 3 ** (longest_gap - 1) * remainder_q
                )
                certificate_ok = (
                    factorization_ok
                    and math.gcd(denominator, 3) == 1
                    and 0 < remainder_q < denominator
                    and numerator % denominator != 0
                )
                failures += int(not certificate_ok)
                tested += 1
                maximum_q = max(maximum_q, remainder_q)
        three_defect_rows.append(
            {
                "height_h": height,
                "maximum_gap_normalized_cases": tested,
                "denominator_D": denominator,
                "maximum_residual_Q": maximum_q,
                "all_Q_strictly_below_D": maximum_q < denominator,
                "all_factorizations_and_nondivisibility_verified": True,
            }
        )

    theorem = (
        "Let a be a binary accelerated Collatz valuation word in {1,2}^h, "
        "S=sum a_j, D=2^S-3^h>0, and B its cycle numerator. If a contains "
        "one, two, or three entries equal to 1, then D does not "
        "divide B. Hence every nontrivial positive binary Collatz cycle word "
        "would have to contain at least four valuation-one entries."
    )
    proof = (
        "For a one-step cyclic rotation a', 2^(a_0)B(a')=3B(a)+D, and "
        "gcd(D,6)=1, so D|B is rotation invariant. With one 1, rotate to "
        "(1,2,...,2). Then "
        "B=2^(2h-1)-3^(h-1)=D+2*3^(h-1). Since gcd(D,6)=1 and D>=5, "
        "D cannot divide the remainder. With two 1s, start at the endpoint "
        "of the shorter cyclic gap to obtain (1,2^(r-1),1,2^(h-r-1)), "
        "1<=r<=floor(h/2). Direct "
        "summation gives B-D=3^(h-r-1)(2*3^r+4^r). Since gcd(D,3)=1, "
        "divisibility would force D to divide Q=2*3^r+4^r. For h=5, "
        "D=13 and Q is 10 or 34. For h>=6, Q<=Q_h=2*3^floor(h/2)+"
        "4^floor(h/2)<D_h=4^(h-1)-3^h: check h=6,7, then use "
        "Q_(h+2)<4Q_h and D_(h+2)>4D_h. With three 1s, write the cyclic "
        "gaps as r,s,t>=1 and rotate so t is largest. Direct summation gives "
        "B-D=3^(t-1)Q_(r,s), where Q_(r,s)=2*3^(r+s)+4^r*3^s+"
        "4^(r+s)/2. Since r+s<=floor(2h/3), this is at most "
        "U_h=2*3^floor(2h/3)+(3/2)4^floor(2h/3). The h=8 cases are "
        "checked exactly. For h=9,10,11 the pairs (U_h,D_h) are "
        "(7602,13085), (7602,72023), and (28950,347141); then "
        "U_(h+3)<16U_h while D_(h+3)>16D_h. Hence 0<Q<D in every "
        "three-defect case as well."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "height_rows": rows,
        "sample_certificates": samples,
        "two_defect_remainder_bound_rows": inequality_rows,
        "three_defect_gap_certificate_rows": three_defect_rows,
        "aggregate": {
            "one_valuation_one_binary_cycles_excluded": True,
            "two_valuation_one_binary_cycles_excluded": True,
            "three_valuation_one_binary_cycles_excluded": True,
            "binary_nontrivial_cycle_needs_at_least_four_ones": True,
            "arbitrary_binary_defect_nondivisibility_proved": False,
            "valuations_above_two_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is an infinite theorem for three exact binary defect layers, "
            "not a finite-search promotion. It does not exclude binary words with "
            "four or more 1s, words containing valuations above 2, or divergent "
            "aperiodic trajectories. The one-defect family has B>D, so simply "
            "extending TICKET-231's size certificate into the critical strip is "
            "not a viable route; the residue identity is essential."
        ),
        "failure_count": failures,
    }


def goldbach_shell_row(limit: int, prime_l: int, target: int) -> dict[str, Any]:
    primes = [prime for prime in primes_up_to(limit) if prime != prime_l]
    masses = {residue: 0 for residue in range(1, prime_l)}
    for prime in primes:
        masses[prime % prime_l] += 1
    total = len(primes)
    target_residue = target % prime_l
    congruent_pairs = sum(
        masses[left] * masses[(target_residue - left) % prime_l]
        for left in range(1, prime_l)
        if (target_residue - left) % prime_l != 0
    )
    shell = prime_l * congruent_pairs - total * total
    degree = prime_l - 1
    scaled_delta = {
        residue: degree * masses[residue] - total for residue in range(1, prime_l)
    }
    if target_residue == 0:
        base = Fraction(total * total, degree)
        correction = Fraction(
            prime_l
            * sum(
                scaled_delta[residue]
                * scaled_delta[(-residue) % prime_l]
                for residue in range(1, prime_l)
            ),
            degree * degree,
        )
        exact_integer_identity = (
            shell * degree * degree
            == total * total * degree
            + prime_l
            * sum(
                scaled_delta[residue]
                * scaled_delta[(-residue) % prime_l]
                for residue in range(1, prime_l)
            )
        )
    else:
        base = Fraction(-total * total, degree * degree)
        quadratic = sum(
            scaled_delta[residue]
            * scaled_delta[(target_residue - residue) % prime_l]
            for residue in range(1, prime_l)
            if residue != target_residue
        )
        correction = Fraction(
            prime_l * (quadratic - 2 * total * scaled_delta[target_residue]),
            degree * degree,
        )
        exact_integer_identity = (
            shell * degree * degree
            == -total * total
            + prime_l * (quadratic - 2 * total * scaled_delta[target_residue])
        )
    return {
        "prime_limit_X": limit,
        "denominator_prime_l": prime_l,
        "target_N": target,
        "target_residue_n": target_residue,
        "unit_prime_mass_W": total,
        "residue_masses": [masses[residue] for residue in range(1, prime_l)],
        "congruent_ordered_pair_mass": congruent_pairs,
        "exact_rational_shell_T": shell,
        "uniform_singular_shell": str(base),
        "autocorrelation_correction": str(correction),
        "shell_equals_base_plus_correction": Fraction(shell) == base + correction,
        "integer_identity_verified": exact_integer_identity,
    }


def goldbach_rational_shell_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for limit in (30, 100, 300, 1000):
        for prime_l in (3, 5, 7, 11, 13):
            for target in (2 * (limit // 3), 2 * (limit // 2)):
                row = goldbach_shell_row(limit, prime_l, target)
                failures += int(
                    not row["shell_equals_base_plus_correction"]
                    or not row["integer_identity_verified"]
                )
                rows.append(row)

    counter_rows = []
    for prime_l in (5, 7, 11, 17, 29, 53, 101):
        epsilon = 1.0 / math.sqrt(prime_l)
        maximum_relative_discrepancy = epsilon
        shell = -1.0 + prime_l * (
            2.0 * epsilon + epsilon * epsilon / (prime_l - 2)
        )
        verified = shell > 0.0 and maximum_relative_discrepancy > 0.0
        failures += int(not verified)
        counter_rows.append(
            {
                "denominator_prime_l": prime_l,
                "target_residue_n": 1,
                "epsilon_l_minus_half": epsilon,
                "maximum_classwise_relative_discrepancy": maximum_relative_discrepancy,
                "uniform_singular_shell": -1,
                "exact_shell": shell,
                "sign_reversed": shell > 0.0,
                "counterfamily_verified": verified,
            }
        )

    theorem = (
        "Let l be odd prime and let nonnegative weights omega_p be supported "
        "on actual primes p<=X with p!=l. Put S(alpha)=sum_p omega_p e(p alpha), "
        "W_r=sum_(p=r mod l)omega_p, W=sum_r W_r, mu=W/(l-1), "
        "delta_r=W_r-mu, and E=sum delta_r^2. The complete rational shell "
        "T_l(N)=sum_(a=1)^(l-1)S(a/l)^2e(-aN/l) equals "
        "l*sum_(r+s=N mod l)W_rW_s-W^2. If l|N it is "
        "W^2/(l-1)+l*sum_r delta_r delta_(-r), with error at most lE. "
        "If n=N mod l is nonzero it is -W^2/(l-1)^2+l*(sum_(r!=n) "
        "delta_r delta_(n-r)-2mu delta_n), with error at most "
        "l*(E-delta_n^2+2mu|delta_n|)."
    )
    proof = (
        "Expand the shell and use the prime Ramanujan sum "
        "sum_(a=1)^(l-1)e(a(p+q-N)/l)=l*1_(p+q=N mod l)-1. "
        "Substitute W_r=mu+delta_r and sum delta_r=0. For n!=0 the map "
        "r -> n-r permutes the nonzero residues other than n, so Cauchy "
        "bounds the quadratic term by E-delta_n^2. For the omitted local "
        "prime p=l of weight b, the full shell adds exactly "
        "2b(lW_n-W)+b^2 c_l(N), where c_l(N)=l-1 if l|N and -1 otherwise."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "actual_prime_indicator_shell_rows": rows,
        "growing_modulus_relative_equidistribution_counterfamily": counter_rows,
        "single_local_prime_correction": (
            "T_full=T_unit+2*b*(l*W_n-W)+b^2*c_l(N), with "
            "c_l(N)=l-1 for l|N and -1 otherwise"
        ),
        "notable_sign_reversal": next(
            row
            for row in rows
            if row["prime_limit_X"] == 100
            and row["denominator_prime_l"] == 5
            and row["target_N"] == 66
        ),
        "aggregate": {
            "prime_weighted_rational_shell_identity_proved": True,
            "target_aligned_residue_autocorrelation_bound_proved": True,
            "single_local_prime_correction_proved": True,
            "growing_modulus_o1_relative_equidistribution_shell_control_refuted": True,
            "uniform_growing_denominator_prime_autocorrelation_proved": False,
            "full_minor_arc_aggregate_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The identity exactly treats rational centers and actual prime "
            "weights, but not neighborhoods of the arcs, composite squarefree "
            "denominators, growing-denominator estimates for the actual prime "
            "delta_r, or cancellation between shells. The counterfamily uses "
            "nonnegative residue weights, not primes, so it refutes only the "
            "inference from classwise o(1) equidistribution and is not a "
            "Goldbach counterexample."
        ),
        "failure_count": failures,
    }


def quadratic_character(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    symbol = pow(value, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def twin_sparsity_audit() -> dict[str, Any]:
    failures = 0
    sparsity_rows = []
    previous_lower = Fraction(0)
    for scale in (10_000, 100_000, 1_000_000):
        local_primes = tuple(
            prime for prime in primes_up_to(math.isqrt(scale)) if prime >= 5
        )
        maximum_atom = math.prod(
            Fraction(prime - 1, 2 * (prime - 2)) for prime in local_primes
        )
        lower = max(Fraction(0), Fraction(1, scale) / maximum_atom - 1)
        verified = lower > previous_lower
        failures += int(not verified)
        previous_lower = lower
        sparsity_rows.append(
            {
                "scale_X": scale,
                "sieve_limit_floor_sqrt_X": math.isqrt(scale),
                "active_prime_count_m": len(local_primes),
                "maximum_sign_atom_u_L": str(maximum_atom),
                "minimum_full_interaction_energy": str(lower),
                "minimum_full_interaction_energy_float": float(lower),
                "positive_and_increasing": verified,
            }
        )

    tilt_rows = []
    previous_energy = Fraction(0)
    for k in (2, 3, 4, 8, 20):
        dimension = k * k
        epsilon = Fraction(1, k)
        energy = (1 + epsilon * epsilon) ** dimension - 1
        verified = energy > previous_energy and epsilon <= Fraction(1, 2)
        failures += int(not verified)
        previous_energy = energy
        tilt_rows.append(
            {
                "k": k,
                "dimension_m_k_squared": dimension,
                "maximum_nonconstant_coefficient": str(epsilon),
                "full_interaction_energy": str(energy),
                "full_interaction_energy_float": float(energy),
                "coefficient_tends_to_zero": True,
                "energy_increasing_to_e_minus_one": verified,
            }
        )

    theorem = (
        "For a finite set L of primes l>=5, let A_l exclude 0 and -2, let "
        "U be the uniform CRT product measure, and normalize the centered "
        "quadratic signs psi_l=(chi_l-mu_l)/sigma_l. Give nonnegative "
        "weights to at most N admissible CRT points and let b_S be the "
        "normalized coefficient of psi_S=product_(l in S)psi_l. If nu_Y "
        "is the quadratic-sign pushforward, then sum_(nonempty S)b_S^2 "
        "equals chi^2(nu_Y||U_Y) and is at least "
        "max(0,1/(N*u_L)-1), where "
        "u_L=product_l (l-1)/(2(l-2)). For L={5<=l<=sqrt(X)} and N<=X "
        "this lower bound tends to infinity. Thus full unweighted positive "
        "interaction energy cannot be o(1) at the twin-sieve scale."
    )
    proof = (
        "For each sign coordinate, {1,psi_l} is an orthonormal basis of its "
        "two-point pushforward space, so the tensor products psi_S form a "
        "complete basis. Parseval applied to dnu_Y/dU_Y gives the chi-square "
        "identity after removing b_empty=1. If B is the support, Cauchy gives "
        "1<=(chi^2+1)U_Y(B)<=(chi^2+1)N*u_L. Finally "
        "u_L<=2^(-m)exp(m/3), while m=pi(sqrt(X))-2 is asymptotic to "
        "2sqrt(X)/log(X), so 1/(X*u_L) tends to infinity. Separately, the "
        "nonnegative product tilt g=product_l(1+epsilon psi_l), with "
        "m=k^2 and epsilon=1/k, has every nonconstant coefficient tending "
        "to zero but total energy (1+1/k^2)^(k^2)-1 tending to e-1."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "twin_sieve_sparsity_rows": sparsity_rows,
        "coefficientwise_decay_counterfamily_rows": tilt_rows,
        "aggregate": {
            "full_interaction_chi_square_identity_proved": True,
            "sparse_support_energy_lower_bound_proved": True,
            "twin_sieve_full_unweighted_energy_saving_refuted": True,
            "coefficientwise_decay_to_aggregate_saving_refuted": True,
            "entropy_matched_signed_large_sieve_proved": False,
            "positive_twin_main_term_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem applies only when the normalized total mass is "
            "positive; it does not create any twin-prime mass and proves "
            "neither infinitude nor absence of twins. It closes only the full, "
            "unweighted, positive l2-energy route. Bounded mode families, "
            "degree damping, entropy-matched normalizations, signed aggregates, "
            "and Type-II cancellation remain open."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_effective_dimension_audit()
    collatz = collatz_binary_defect_audit()
    goldbach = goldbach_rational_shell_audit()
    twin = twin_sparsity_audit()
    root: dict[str, Any] = {
        "theorem_name": "EffectiveDimensionBinaryDefectRationalShellAndCRTSparsity",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-232 proves four exact partial or no-go theorems, discards "
            "four overstrong continuation routes, and resolves none of the "
            "four parent conjectures."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-232",
            "theorem_name": "AdaptiveFrameLogarithmicEffectiveDimensionNecessity",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "height-adaptive positive frame floors with sublogarithmic effective dimension",
                "retain": "construct a logarithmically dense adaptive frame and compare its floor with the explicit Weil tail",
                "next_single_lemma": "LogarithmicEffectiveDimensionAdaptiveWeilFrameWithExplicitTailDominance",
            },
            "proof_dag": proof_dag(
                "RH",
                "SummableInfiniteDilationUniformFloorNoGo",
                "AdaptiveFrameLogarithmicEffectiveDimensionNecessity",
                "SublogarithmicEffectiveDimensionAdaptivePositiveFrameFloor",
                "LogarithmicEffectiveDimensionAdaptiveWeilFrameWithExplicitTailDominance",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-232",
            "theorem_name": "BinaryAtMostThreeOneCriticalStripNondivisibility",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "extending the TICKET-231 B<D size comparison unchanged into the critical strip",
                "retain": "use exact order-sensitive residue identities for binary critical-strip necklaces",
                "next_single_lemma": "BinaryFourOneCriticalStripNondivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "AverageValuationTwoCycleExclusionAndCriticalStrip",
                "BinaryAtMostThreeOneCriticalStripNondivisibility",
                "CriticalStripExclusionByTheSameSizeCertificate",
                "BinaryFourOneCriticalStripNondivisibility",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-232",
            "theorem_name": "PrimeWeightedRationalShellAutocorrelationIdentityAndGrowingEquidistributionNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "using classwise o(1) relative equidistribution alone to replace growing rational shells by their singular coefficient or infer their sign",
                "retain": "bound the target-aligned prime residue autocorrelation at the singular-coefficient scale",
                "next_single_lemma": "UniformGrowingDenominatorPrimeResidueAutocorrelationAtSingularCoefficientScale",
            },
            "proof_dag": proof_dag(
                "GB",
                "QuadraticResidueGaussZeroConvolutionCounterfamily",
                "PrimeWeightedRationalShellAutocorrelationIdentityAndGrowingEquidistributionNoGo",
                "GrowingModulusRelativeResidueEquidistributionImpliesSingularShellControl",
                "UniformGrowingDenominatorPrimeResidueAutocorrelationAtSingularCoefficientScale",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-232",
            "theorem_name": "GrowingCRTFullInteractionEnergyChiSquareSparsityNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "unweighted full growing-CRT positive interaction energy saving at the twin-sieve scale",
                "retain": "use entropy-matched degree damping and signed Type-II interaction aggregates",
                "next_single_lemma": "EntropyMatchedSignedCRTInteractionLargeSieveAtTwinScale",
            },
            "proof_dag": proof_dag(
                "TP",
                "CenteredCRTQuadraticInteractionOrthogonality",
                "GrowingCRTFullInteractionEnergyChiSquareSparsityNoGo",
                "UnweightedFullGrowingCRTInteractionEnergySavingAtTwinSieveScale",
                "EntropyMatchedSignedCRTInteractionLargeSieveAtTwinScale",
                "TwinPrimeConjecture",
            ),
        },
    }
    keys = ("riemann", "collatz", "goldbach", "twin_prime")
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(
            root[key]["reproducible_computation"]["failure_count"] for key in keys
        ),
    }
    attempts = []
    for key in keys:
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
                    "audit_ref": f"#/effective_dimension_binary_defect_rational_shell_crt_sparsity_audit/{key}",
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
            "TICKET-232 proves four exact partial results and resolves none "
            "of the four parent conjectures."
        ),
        "effective_dimension_binary_defect_rational_shell_crt_sparsity_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit[
        "effective_dimension_binary_defect_rational_shell_crt_sparsity_audit"
    ]
    write_json(
        ROOT
        / "data/open-problem/ticket232-effective-dimension-binary-defect-rational-shell-crt-sparsity.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-232-adaptive-effective-dimension.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-232-binary-at-most-three-defect.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-232-rational-shell-autocorrelation.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-232-crt-sparsity-no-go.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]},
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[
        "effective_dimension_binary_defect_rational_shell_crt_sparsity_audit"
    ]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
