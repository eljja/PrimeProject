from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import prime_sieve


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket207-dihedral-twoone-logwitness-abel.v1"
GENERATED_AT = "2026-08-10T16:20:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def gaussian_square_shift(
    x: Fraction,
    y: Fraction,
    c: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return ((x-1/2)+iy)^2-c^2 as an exact Gaussian rational."""
    a = x - Fraction(1, 2)
    return a * a - y * y - c * c, 2 * a * y


def conjugate(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return value[0], -value[1]


def riemann_dihedral_boundary_audit() -> dict[str, Any]:
    c = Fraction(1, 3)
    rows = []
    failures = 0
    for half_width, height in (
        (Fraction(2, 5), Fraction(1)),
        (Fraction(1, 2), Fraction(2)),
        (Fraction(3, 4), Fraction(3)),
    ):
        center = Fraction(1, 2)
        top_points = [
            (center - half_width + 2 * half_width * Fraction(index, 8), height)
            for index in range(9)
        ]
        right_upper = [
            (center + half_width, height * Fraction(index, 8))
            for index in range(9)
        ]
        bottom_matches = all(
            gaussian_square_shift(x, -height, c)
            == conjugate(gaussian_square_shift(x, height, c))
            for x, _ in top_points
        )
        right_lower_matches = all(
            gaussian_square_shift(center + half_width, -y, c)
            == conjugate(gaussian_square_shift(center + half_width, y, c))
            for _, y in right_upper
        )
        left_matches = all(
            gaussian_square_shift(center - half_width, y, c)
            == gaussian_square_shift(center + half_width, -y, c)
            for y in [
                -height + 2 * height * Fraction(index, 8)
                for index in range(9)
            ]
        )
        full_points = (
            top_points
            + [(x, -height) for x, _ in top_points]
            + right_upper
            + [(center + half_width, -y) for _, y in right_upper]
            + [
                (center - half_width, -height + 2 * height * Fraction(index, 8))
                for index in range(9)
            ]
        )
        fundamental_points = top_points + right_upper
        full_clearance_squared = min(
            real * real + imag * imag
            for real, imag in (
                gaussian_square_shift(x, y, c) for x, y in full_points
            )
        )
        fundamental_clearance_squared = min(
            real * real + imag * imag
            for real, imag in (
                gaussian_square_shift(x, y, c)
                for x, y in fundamental_points
            )
        )
        full_derivative_squared = max(
            4 * ((x - center) ** 2 + y * y) for x, y in full_points
        )
        fundamental_derivative_squared = max(
            4 * ((x - center) ** 2 + y * y)
            for x, y in fundamental_points
        )
        failures += int(not bottom_matches)
        failures += int(not right_lower_matches)
        failures += int(not left_matches)
        failures += int(full_clearance_squared != fundamental_clearance_squared)
        failures += int(full_derivative_squared != fundamental_derivative_squared)
        rows.append(
            {
                "rectangle_half_width": fraction_text(half_width),
                "rectangle_height": fraction_text(height),
                "exact_boundary_samples": len(full_points),
                "fundamental_domain_samples": len(fundamental_points),
                "bottom_reconstructed_by_conjugation": bottom_matches,
                "right_lower_reconstructed_by_conjugation": right_lower_matches,
                "left_reconstructed_by_reflection": left_matches,
                "sampled_clearance_squared_full": fraction_text(
                    full_clearance_squared
                ),
                "sampled_clearance_squared_fundamental": fraction_text(
                    fundamental_clearance_squared
                ),
                "sampled_derivative_squared_full": fraction_text(
                    full_derivative_squared
                ),
                "sampled_derivative_squared_fundamental": fraction_text(
                    fundamental_derivative_squared
                ),
            }
        )

    zeros = [Fraction(1, 2) - c, Fraction(1, 2) + c]
    failures += int(any(zero == Fraction(1, 2) for zero in zeros))
    theorem = (
        "Let xi be the completed Riemann xi-function and let R be a rectangle "
        "symmetric about the real axis and Re(s)=1/2. The identities "
        "xi(s)=xi(1-s) and xi(conjugate(s))=conjugate(xi(s)) imply that all "
        "boundary values, the boundary minimum of |xi|, and the boundary "
        "maximum of |xi'| are determined by the full top edge together with "
        "the upper half of the right edge. Consequently a rigorous TICKET-206 "
        "winding certificate needs interval evaluation only on that fundamental "
        "boundary domain. These symmetries alone cannot imply RH."
    )
    proof = (
        "Conjugation maps the top edge to the bottom and the upper right edge "
        "to the lower right edge. Reflection s->1-s maps the left edge to the "
        "right edge. Differentiating xi(s)=xi(1-s) gives "
        "xi'(s)=-xi'(1-s), so derivative magnitudes obey the same reduction. "
        "These maps partition the full boundary into images of the stated "
        "fundamental domain, proving equality of the extrema. For the no-go, "
        "F_c(s)=(s-1/2)^2-c^2 with 0<c<1/2 is entire, real on the real axis, "
        "and satisfies both symmetries, but its zeros 1/2-c and 1/2+c lie off "
        "the critical line. Symmetry therefore reduces certified work but does "
        "not supply the missing nonvanishing bound for xi."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_surrogate": "F_c(s)=(s-1/2)^2-c^2 with c=1/3",
        "off_critical_line_zeros": [fraction_text(value) for value in zeros],
        "boundary_reconstruction_rows": rows,
        "aggregate": {
            "top_plus_upper_right_boundary_reduction_proved": True,
            "clearance_and_derivative_extrema_reduction_proved": True,
            "symmetry_only_implication_of_rh_refuted": True,
            "completed_xi_cofinal_interval_bounds_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The polynomial F_c refutes only a symmetry-only proof template. It "
            "is not a zeta counterexample. No rigorous positive xi-clearance is "
            "proved on a cofinal family of rectangles."
        ),
        "failure_count": failures,
    }


def accelerated_collatz_step(value: int) -> tuple[int, int]:
    if value <= 0 or value % 2 == 0:
        raise ValueError("accelerated Collatz input must be a positive odd integer")
    numerator = 3 * value + 1
    valuation = 0
    while numerator % 2 == 0:
        numerator //= 2
        valuation += 1
    return numerator, valuation


def collatz_replay(start: int, length: int) -> dict[str, Any]:
    value = start
    orbit = [value]
    valuations = []
    for _ in range(length):
        value, valuation = accelerated_collatz_step(value)
        orbit.append(value)
        valuations.append(valuation)
    return {
        "start": start,
        "length": length,
        "orbit": orbit,
        "valuations": valuations,
        "returns_to_start": value == start,
        "exactly_two_valuation_ones": valuations.count(1) == 2,
    }


def collatz_two_one_exclusion_audit() -> dict[str, Any]:
    long_case_bounds = [
        {
            "length_range": "h>=8",
            "q_upper_bound": "729/4096",
            "minimum_upper_bound": "26485/9823",
            "conclusion": "m<3 contradicts nontrivial odd minimum m>=3",
        },
        {
            "length_range": "h=7",
            "q_upper_bound": "243/1024",
            "minimum_upper_bound": "6439/1909",
            "conclusion": "m<4 leaves m=3",
        },
        {
            "length_range": "h=6",
            "q_upper_bound": "81/256",
            "minimum_upper_bound": "1549/295",
            "conclusion": "m<6 leaves m in {3,5}",
        },
        {
            "length_range": "h=5",
            "q_upper_bound": "27/64",
            "minimum_upper_bound": "367/13",
            "conclusion": "m<29 leaves odd m in [3,27]",
        },
    ]
    replay_cases = {
        "h_eq_7": [collatz_replay(3, 7)],
        "h_eq_6": [collatz_replay(value, 6) for value in (3, 5)],
        "h_eq_5": [collatz_replay(value, 5) for value in range(3, 29, 2)],
    }
    failures = sum(
        int(row["returns_to_start"] and row["exactly_two_valuation_ones"])
        for rows in replay_cases.values()
        for row in rows
    )
    short_cases = [
        {
            "length": 4,
            "word_shape": "(1,1,b,c), b,c>=2",
            "cycle_minimum_formula": "m=(57+2^(b+2))/(2^(b+c+2)-81)",
            "m_ge_3_constraint": "(3*2^c-1)*2^(b+2)<=300",
            "remaining_pair": "(b,c)=(2,2)",
            "remaining_pair_denominator": -17,
            "excluded": True,
        },
        {
            "length": 4,
            "word_shape": "(1,b,1,c), b,c>=2",
            "cycle_minimum_formula": "m=(45+10*2^b)/(2^(b+c+2)-81)",
            "m_ge_3_constraint": "(12*2^c-10)*2^b<=288",
            "remaining_pair": "(b,c)=(2,2)",
            "remaining_pair_denominator": -17,
            "excluded": True,
        },
        {
            "length": 3,
            "word_shape": "(1,1,b), b>=2",
            "cycle_minimum_formula": "m=19/(2^(b+2)-27)",
            "only_positive_m_ge_3_candidate": "b=3 gives m=19/5",
            "excluded": True,
        },
        {
            "length": 2,
            "word_shape": "(1,1)",
            "cycle_denominator": -5,
            "excluded": True,
        },
    ]
    failures += sum(int(not row["excluded"]) for row in short_cases)
    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly two "
        "valuation entries equal to one and every remaining entry at least two. "
        "Combined with TICKET-206, every hypothetical nontrivial positive cycle "
        "must contain at least three valuation-one entries."
    )
    proof = (
        "Rotate a hypothetical h-cycle to its minimum odd value m. Its first "
        "valuation is one; a valuation at least two would map below m. Put r "
        "contraction steps between the two valuation-one steps and s after the "
        "second, so r+s=h-2. The second one cannot be the last transition, "
        "because G(x)=(3x+1)/2>x for every predecessor x>=m; hence s>=1. "
        "Every valuation-at-least-two step is bounded above by "
        "F(x)=(3x+1)/4. With q=(3/4)^(h-2) and q_s=(3/4)^s, monotonicity gives "
        "m<=F^s G F^r G(m)=1+q_s-3q/4+(9q/4)m. For h>=5, q_s<=3/4 and "
        "the resulting bound is at most (7/4-3q/4)/(1-9q/4), increasing in q. "
        "For h>=8 it is 26485/9823<3. For h=7,6,5 it leaves respectively "
        "m=3, m in {3,5}, and odd m<=27; exact deterministic replay excludes "
        "all these finite candidates. For h=4 the second one is in position "
        "two or three. The two exact cycle formulas and m>=3 inequalities leave "
        "only b=c=2, whose denominator is negative. For h=3 the sole candidate "
        "is m=19/5, and h=2 has negative denominator. Thus no case remains."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "envelope_identity": (
            "F^s G F^r G(m)=1+q_s-3q/4+(9q/4)m, "
            "q=(3/4)^(h-2), q_s=(3/4)^s"
        ),
        "long_case_bounds": long_case_bounds,
        "finite_replay_cases": replay_cases,
        "short_symbolic_cases": short_cases,
        "aggregate": {
            "exactly_two_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 3,
            "three_or_more_one_mixed_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem excludes a complete periodic valuation stratum. It does "
            "not treat cycles with at least three valuation-one entries or prove "
            "that every nonperiodic orbit descends."
        ),
        "failure_count": failures,
    }


def primes_through(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def goldbach_logarithmic_witness_row(bound: int) -> dict[str, Any]:
    witnesses = [prime for prime in primes_through(bound) if prime >= 3]
    forcing = [
        prime for prime in primes_through(3 * bound) if bound < prime < 3 * bound
    ][: len(witnesses)]
    if len(forcing) != len(witnesses):
        raise ValueError(f"insufficient fixture forcing primes for B={bound}")
    modulus = 2
    residue = 0
    forcing_rows = []
    for witness, divisor in zip(witnesses, forcing, strict=True):
        step = ((witness - residue) * pow(modulus, -1, divisor)) % divisor
        residue = (residue + modulus * step) % (modulus * divisor)
        modulus *= divisor
        forcing_rows.append(
            {
                "excluded_witness_prime": witness,
                "forcing_divisor": divisor,
            }
        )
    target = residue + modulus
    for row in forcing_rows:
        complement = target - row["excluded_witness_prime"]
        row["complement"] = str(complement)
        row["proper_composite_complement"] = (
            complement > row["forcing_divisor"]
            and complement % row["forcing_divisor"] == 0
        )
    bit_bound = target.bit_length() <= 3 * bound
    return {
        "witness_bound_B": bound,
        "odd_witness_count": len(witnesses),
        "forcing_prime_count_in_B_to_3B_used": len(forcing),
        "canonical_even_target_N": str(target),
        "modulus_M": str(modulus),
        "N_in_M_to_2M": modulus < target < 2 * modulus,
        "N_bit_length": target.bit_length(),
        "three_B": 3 * bound,
        "exact_logarithmic_scale_certificate": bit_bound,
        "p_equals_2_complement_is_composite": target > 4 and (target - 2) % 2 == 0,
        "forcing_rows": forcing_rows,
        "all_prime_witnesses_at_most_B_excluded": all(
            row["proper_composite_complement"] for row in forcing_rows
        ),
    }


def goldbach_logarithmic_witness_audit() -> dict[str, Any]:
    rows = [
        goldbach_logarithmic_witness_row(bound)
        for bound in (11, 19, 29, 43, 59)
    ]
    failures = sum(
        int(not row["N_in_M_to_2M"])
        + int(not row["exact_logarithmic_scale_certificate"])
        + int(not row["p_equals_2_complement_is_composite"])
        + int(not row["all_prime_witnesses_at_most_B_excluded"])
        for row in rows
    )
    theorem = (
        "Let W(N) be the least prime p for which N-p is prime, with W(N)=infinity "
        "if no such p exists. There is an unbounded sequence of even N such that "
        "W(N)>(1/3) log N. Consequently no o(log N) witness cutoff can be a "
        "universal basis for strong Goldbach."
    )
    proof = (
        "For each sufficiently large B, the prime number theorem gives at least "
        "pi(B)-1 primes in (B,3B). Assign a distinct q_p in that interval to "
        "each odd prime p<=B. CRT gives N=0 mod 2 and N=p mod q_p. With "
        "M=2 product(q_p), choose the representative M<N<2M. For large B, "
        "N-p is a proper multiple of q_p for every odd p<=B, while N-2 is an "
        "even composite, so W(N)>B. Also PNT yields "
        "log M<=log 2+(pi(B)-1)log(3B)<=2B eventually. Hence "
        "log N<log(2M)<3B and W(N)>B>(1/3)log N. Since M tends to infinity, "
        "the constructed sequence is unbounded. The exact fixtures replace "
        "the real logarithm by bit_length(N)<=3B, which implies log N<3B."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "crt_logarithmic_fixture_rows": rows,
        "aggregate": {
            "logarithmic_least_witness_lower_bound_proved": True,
            "universal_sublogarithmic_witness_basis_refuted": True,
            "goldbach_counterexample_found": False,
            "tail_exception_bound_below_one_constructed": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The construction blocks only p<=B and leaves all larger summands "
            "available. It proves a lower bound on the least witness, not a "
            "Goldbach exception or an upper bound for the exceptional set."
        ),
        "failure_count": failures,
    }


def big_omega(value: int) -> int:
    if value < 1:
        raise ValueError("Omega is defined here only for positive integers")
    count = 0
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            remaining //= divisor
            count += 1
        divisor += 1
    if remaining > 1:
        count += 1
    return count


def abel_omega_projector(omega: int, scale: Fraction) -> Fraction:
    if omega < 0 or not (0 < scale < 1):
        raise ValueError("omega must be nonnegative and scale must lie in (0,1)")
    if omega == 0:
        return Fraction(0)
    return omega * (1 - scale) ** (omega - 1)


def twin_abel_reconstruction_row(x_value: int) -> dict[str, Any]:
    flags = prime_sieve(2 * x_value + 2)
    scale = Fraction(16 * x_value - 1, 16 * x_value)
    weighted_sum = Fraction(0)
    twin_count = 0
    largest_composite_weight = Fraction(0)
    for left in range(x_value + 1, 2 * x_value + 1):
        left_omega = big_omega(left)
        right_omega = big_omega(left + 2)
        left_weight = abel_omega_projector(left_omega, scale)
        right_weight = abel_omega_projector(right_omega, scale)
        weighted_sum += left_weight * right_weight
        if flags[left] and flags[left + 2]:
            twin_count += 1
        if left_omega >= 2:
            largest_composite_weight = max(largest_composite_weight, left_weight)
        if right_omega >= 2:
            largest_composite_weight = max(largest_composite_weight, right_weight)
    leakage = weighted_sum - twin_count
    reconstructed = weighted_sum.numerator // weighted_sum.denominator
    return {
        "dyadic_X": x_value,
        "scale_r_X": fraction_text(scale),
        "exact_twin_count_T_X": twin_count,
        "abel_sum_S_X": fraction_text(weighted_sum),
        "positive_composite_leakage": fraction_text(leakage),
        "leakage_upper_bound": "1/8",
        "largest_observed_composite_weight": fraction_text(
            largest_composite_weight
        ),
        "proved_composite_weight_upper_bound": fraction_text(
            Fraction(1, 8 * x_value)
        ),
        "floor_S_X": reconstructed,
        "exact_reconstruction": reconstructed == twin_count,
        "leakage_below_one_eighth": leakage <= Fraction(1, 8),
    }


def twin_abel_projector_audit() -> dict[str, Any]:
    identity_rows = []
    failures = 0
    for denominator in (4, 8, 16):
        scale = Fraction(denominator - 1, denominator)
        values = []
        for omega in range(1, 8):
            closed = omega * (1 - scale) ** (omega - 1)
            direct = sum(
                Fraction((-1) ** (index - 1) * index, 1)
                * Fraction(_comb(omega, index), 1)
                * scale ** (index - 1)
                for index in range(1, omega + 1)
            )
            failures += int(direct != closed)
            values.append(
                {
                    "Omega": omega,
                    "direct_normalized_Abel_sum": fraction_text(direct),
                    "closed_form": fraction_text(closed),
                }
            )
        identity_rows.append({"r": fraction_text(scale), "values": values})
    reconstruction_rows = [
        twin_abel_reconstruction_row(x_value)
        for x_value in (32, 64, 128, 256)
    ]
    failures += sum(
        int(not row["exact_reconstruction"])
        + int(not row["leakage_below_one_eighth"])
        for row in reconstruction_rows
    )
    theorem = (
        "For 0<r<1 and m>=1, the normalized Abel Omega projector "
        "Q_r(m)=r^(-1) sum_{j=1}^m (-1)^(j-1) j binom(m,j) r^j equals "
        "m(1-r)^(m-1). Thus Q_r(1)=1 but Q_r(m)>0 for every composite "
        "multiplicity m>=2, so no fixed r is an exact prime indicator. For each "
        "integer X>=1, however, r_X=1-1/(16X) gives an exact finite identity: "
        "if S_X=sum_{X<n<=2X} Q_rX(Omega(n))Q_rX(Omega(n+2)) and T_X is the "
        "number of twin-prime lower endpoints in that interval, then "
        "T_X<=S_X<=T_X+1/8, hence floor(S_X)=T_X."
    )
    proof = (
        "Differentiate (1-r)^m and multiply by -1 to obtain the closed form. "
        "For r_X, every composite m>=2 has Q_rX(m)=m/(16X)^(m-1)<=1/(8X), "
        "while primes have weight one. Each twin term contributes exactly one. "
        "Every other one of the X terms contains a composite endpoint and is "
        "nonnegative and at most 1/(8X), so the total leakage is at most 1/8. "
        "Taking the floor recovers T_X exactly. This is a finite re-encoding of "
        "factorization: proving a positive lower bound for S_X independently "
        "of T_X remains the original shift-two arithmetic problem."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "abel_identity_rows": identity_rows,
        "finite_reconstruction_rows": reconstruction_rows,
        "aggregate": {
            "normalized_abel_closed_form_proved": True,
            "fixed_scale_exact_prime_indicator_refuted": True,
            "scale_dependent_finite_twin_count_reconstruction_proved": True,
            "independent_positive_main_term_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The floor identity uses exact Omega values and only repackages the "
            "finite twin count. Positivity of S_X on all large intervals is not "
            "proved and cannot be inferred from nonnegative Abel leakage."
        ),
        "failure_count": failures,
    }


def _comb(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    result = 1
    for index in range(1, k + 1):
        result = result * (n - index + 1) // index
    return result


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    limited: str,
    open_lemma: str,
    parent: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T206", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T207", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N207",
                "label": limited,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN207",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": parent, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T206", f"{prefix}-T207"],
            [f"{prefix}-T207", f"{prefix}-N207"],
            [f"{prefix}-T207", f"{prefix}-OPEN207"],
            [f"{prefix}-OPEN207", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_dihedral_boundary_audit()
    collatz_compute = collatz_two_one_exclusion_audit()
    goldbach_compute = goldbach_logarithmic_witness_audit()
    twin_compute = twin_abel_projector_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-207",
            "theorem_name": "CompletedXiDihedralBoundaryReductionAndSymmetryOnlyNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No rigorous positive xi-clearance is constructed on a cofinal family of reduced rectangle boundaries.",
            "route_decision": {
                "discard": "using completed-xi reflection and conjugation symmetries alone to force critical-line zeros",
                "retain": "rigorous interval evaluation on the top edge and upper-right half-edge only",
                "next_single_lemma": "RigorousCompletedXiTopAndRightBoundaryIntervalBoundsOnCofinalRectangles",
            },
            "proof_dag": proof_dag(
                "RH",
                "ZeroFreeBoundaryAdaptiveMeshTerminationAndClearanceComplexityNoGo",
                "CompletedXiDihedralBoundaryReductionAndSymmetryOnlyNoGo",
                "CompletedXiSymmetryAloneForcesCriticalLineZeros",
                "RigorousCompletedXiTopAndRightBoundaryIntervalBoundsOnCofinalRectangles",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof or counterexample. The certified boundary workload is reduced exactly, and a symmetry-only proof template is refuted.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-207",
            "theorem_name": "TwoOneArbitraryGeTwoValuationCycleExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Cycles with at least three valuation-one entries and all nonperiodic divergent orbits remain open.",
            "route_decision": {
                "discard": "searching any exactly-two-valuation-one period for a positive cycle",
                "retain": "primitive mixed necklaces with at least three valuation-one entries plus a separate global descent argument",
                "next_single_lemma": "UniformExclusionForPrimitiveMixedNecklacesWithAtLeastThreeOnes",
            },
            "proof_dag": proof_dag(
                "CO",
                "SingleOneArbitraryGeTwoValuationCycleExclusion",
                "TwoOneArbitraryGeTwoValuationCycleExclusion",
                "ExactlyTwoValuationOnesCanSupportANontrivialPositiveCycle",
                "UniformExclusionForPrimitiveMixedNecklacesWithAtLeastThreeOnes",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or counterexample. The complete exactly-two-valuation-one periodic stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-207",
            "theorem_name": "LogarithmicLeastWitnessLowerBoundAlongCRTSequence",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "The construction gives no Goldbach exception and no exceptional-count upper bound for witnesses above the logarithmic floor.",
            "route_decision": {
                "discard": "using any sublogarithmic prime-witness window as a universal Goldbach basis",
                "retain": "tail exceptional-set control beyond a logarithmic witness floor",
                "next_single_lemma": "GoldbachTailExceptionalCountBelowOneBeyondLogarithmicWitnessFloor",
            },
            "proof_dag": proof_dag(
                "GB",
                "UnboundedLeastWitnessCRTNoGoForFixedPrimeBases",
                "LogarithmicLeastWitnessLowerBoundAlongCRTSequence",
                "SublogarithmicPrimeWitnessWindowUniversallyCoversGoldbach",
                "GoldbachTailExceptionalCountBelowOneBeyondLogarithmicWitnessFloor",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. An unbounded CRT sequence forces the least witness above one third of log N.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-207",
            "theorem_name": "AbelOmegaProjectorClosedFormFiniteReconstructionAndPositivityCircularityNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No independent signed arithmetic main term or uniform positive lower bound for the Abel correlation is proved.",
            "route_decision": {
                "discard": "using nonnegative fixed-scale Abel smoothing alone as a parity-breaking twin-prime lower bound",
                "retain": "a signed arithmetic majorant with an independently proved main term and controlled Abel tail",
                "next_single_lemma": "SignedArithmeticMajorantForAbelProjectorTailWithIndependentMainTerm",
            },
            "proof_dag": proof_dag(
                "TP",
                "BinomialOmegaPrimeProjectorAndEveryFiniteTruncationNoGo",
                "AbelOmegaProjectorClosedFormFiniteReconstructionAndPositivityCircularityNoGo",
                "NonnegativeAbelRegularizationAloneBreaksParity",
                "SignedArithmeticMajorantForAbelProjectorTailWithIndependentMainTerm",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. Abel smoothing is solved exactly as a finite reconstruction and shown not to provide independent positivity.",
        },
    }
    failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    boundary = (
        "TICKET-207 resolves none of the four conjectures. It reduces completed-xi "
        "rectangle certification to a dihedral fundamental boundary and refutes "
        "symmetry-only reasoning, excludes all accelerated Collatz cycles with "
        "exactly two valuation-one entries, strengthens the Goldbach least-witness "
        "CRT obstruction to logarithmic scale, and derives an exact Abel-Omega "
        "finite reconstruction while proving that its positivity is not independent."
    )
    return {
        "theorem_name": "FourConjectureDihedralTwoOneLogWitnessAbelAudit",
        "status": STATUS,
        "proof_boundary": boundary,
        **sections,
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
        section = audit[section_key]
        decision = section["route_decision"]
        attempts.append(
            {
                "problem_id": section["problem_id"],
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": decision["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": decision["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": decision["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "dihedral_twoone_logwitness_abel_audit": audit,
        "attempts": attempts,
    }
    integrated = ROOT / "data/open-problem/ticket207-dihedral-twoone-logwitness-abel.json"
    write_json(integrated, payload)
    file_map = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-207-dihedral-boundary.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-207-two-one-general.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-207-log-witness.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-207-abel-projector.json",
    }
    section_map = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        section = audit[section_map[problem_id]]
        write_json(
            file_map[problem_id],
            {
                "schema": "primeproject.open-problem-attempt.v1",
                "generated_at": GENERATED_AT,
                **attempt,
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "route_decision": section["route_decision"],
            },
        )
    print(f"integrated_sha256 {hashlib.sha256(integrated.read_bytes()).hexdigest()}")


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
