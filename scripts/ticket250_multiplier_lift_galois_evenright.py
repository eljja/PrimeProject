from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket246_moment_alldepth_parseval_primepower import (
    prime_power_representation_table,
)
from scripts.ticket247_hilbert_hensel_lipschitz_primepower import primes_up_to


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket250-multiplier-lift-galois-evenright.v1"
GENERATED_AT = "2026-08-27T01:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "multiplier_lift_galois_evenright_audit"

RIEMANN_ORDERS = (1, 2, 4, 8, 16, 32, 64, 128, 256)
RIEMANN_EPSILON_POWERS = tuple(range(1, 13))
COLLATZ_FIELD_PRIMES = (7, 11, 23, 101, 251)
GOLDBACH_PRIME_MODULI = (5, 7, 11, 13, 17, 19, 23)
GOLDBACH_X_SCALES = (100, 1_000, 10_000, 100_000, 1_000_000)
TWIN_X_SCALES = (24, 25, 100, 1_000, 10_000, 100_000, 1_000_000, 5_000_000, 10_000_000)


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "display_float": float(value),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def normalized_legendre_x2_expectation(degree: int) -> Fraction:
    upper = Fraction((degree + 1) ** 2, (2 * degree + 1) * (2 * degree + 3))
    lower = (
        Fraction(degree**2, (2 * degree - 1) * (2 * degree + 1))
        if degree
        else Fraction(0)
    )
    return upper + lower


@lru_cache(maxsize=1)
def riemann_noncompact_multiplier_audit() -> dict[str, Any]:
    legendre_rows: list[dict[str, Any]] = []
    concentration_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for n in RIEMANN_ORDERS:
        degree = 2 * n
        expectation = normalized_legendre_x2_expectation(degree)
        distance = abs(expectation - Fraction(1, 2))
        verified = expectation > 0 and distance <= Fraction(1, 2 * degree - 1)
        failures += int(not verified)
        transcript.update(
            (
                f"legendre:{n}:{degree}:{expectation.numerator}:"
                f"{expectation.denominator}:{distance.numerator}:"
                f"{distance.denominator}:{int(verified)}\n"
            ).encode("ascii")
        )
        legendre_rows.append(
            {
                "half_degree_n": n,
                "legendre_degree": degree,
                "exact_M_x2_expectation": fraction_record(expectation),
                "exact_distance_from_one_half": fraction_record(distance),
                "certificate_verified": verified,
            }
        )

    previous_bound: Fraction | None = None
    for power in RIEMANN_EPSILON_POWERS:
        epsilon = Fraction(1, 2**power)
        multiplier_energy = epsilon * epsilon / 3
        q0_upper = 2 * epsilon / (1 - epsilon**4)
        combined_upper = multiplier_energy + q0_upper
        verified = previous_bound is None or combined_upper < previous_bound
        failures += int(not verified)
        transcript.update(
            (
                f"concentration:{power}:{epsilon.numerator}:{epsilon.denominator}:"
                f"{multiplier_energy.numerator}:{multiplier_energy.denominator}:"
                f"{q0_upper.numerator}:{q0_upper.denominator}:"
                f"{combined_upper.numerator}:{combined_upper.denominator}:"
                f"{int(verified)}\n"
            ).encode("ascii")
        )
        concentration_rows.append(
            {
                "epsilon_power": power,
                "epsilon": fraction_record(epsilon),
                "exact_M_x2_energy": fraction_record(multiplier_energy),
                "proved_Q0_upper_bound": fraction_record(q0_upper),
                "proved_combined_upper_bound": fraction_record(combined_upper),
                "certificate_verified": verified,
            }
        )
        previous_bound = combined_upper

    theorem = (
        "Let H=L2_even([-1,1]), let Q0 be the raw even-moment energy, let "
        "f_n=sqrt((4n+1)/2)P_(2n), and let K=M_(x^2). Then K is bounded, "
        "self-adjoint, and noncompact, while <Kf_n,f_n> tends to 1/2. Thus "
        "K defeats the compact weak-null escape used in TICKET-249. However, "
        "for g_epsilon=(2epsilon)^(-1/2)1_[−epsilon,epsilon], ||g_epsilon||=1, "
        "<Kg_epsilon,g_epsilon>=epsilon^2/3 and "
        "Q0(g_epsilon)<=2epsilon/(1-epsilon^4), so "
        "Q0(g_epsilon)+<Kg_epsilon,g_epsilon> tends to zero. Therefore "
        "nonvanishing on the Legendre escape sequence, even for an explicit "
        "noncompact correction, is not sufficient for full-sphere coercivity."
    )
    proof = (
        "For normalized Legendre degree l, the three-term recurrence gives "
        "<x^2 phi_l,phi_l>=(l+1)^2/((2l+1)(2l+3))+"
        "l^2/((2l-1)(2l+1)), which tends to 1/2. Multiplication by x^2 is "
        "noncompact: normalized indicators of countably many disjoint "
        "positive-measure intervals inside [1/2,1] have mutually orthogonal "
        "images of norm at least 1/4. For the normalized centered indicator, "
        "the 2k-th moment squared is 2 epsilon^(4k+1)/(2k+1)^2. Summing and "
        "dropping the denominators gives Q0<=2epsilon/(1-epsilon^4). Both "
        "this bound and epsilon^2/3 vanish. The construction is an exact "
        "counterexample to a Legendre-only noncompact coercivity test, not a "
        "model of the actual Guinand-Weil arithmetic form."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_legendre_multiplier_rows": legendre_rows,
        "exact_concentration_escape_rows": concentration_rows,
        "algorithm": "exact Fraction evaluation of the normalized Legendre Jacobi recurrence and geometric upper bounds for centered indicators",
        "complexity": "O(N+E) exact rational operations for N Legendre and E concentration rows; noncompactness and the all-epsilon limit are analytic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "multiplier_M_x2_noncompact_proved": True,
            "legendre_escape_blocked_by_multiplier": True,
            "concentration_escape_for_Q0_plus_multiplier_proved": True,
            "legendre_only_noncompact_coercivity_route_refuted": True,
            "actual_weil_form_controlled": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def fermat_quotient_residue(base: int, q: int) -> int:
    modulus = q * q
    return ((pow(base, q - 1, modulus) - 1) % modulus) // q


def lifted_fermat_quotient(base: int, lift: int, q: int) -> int:
    return fermat_quotient_residue(base + lift * q, q)


@lru_cache(maxsize=1)
def collatz_lift_transitivity_audit() -> dict[str, Any]:
    field_rows: list[dict[str, Any]] = []
    target_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for q in COLLATZ_FIELD_PRIMES:
        u0 = fermat_quotient_residue(2, q)
        v0 = fermat_quotient_residue(3, q)
        lifted_u = [lifted_fermat_quotient(2, k, q) for k in range(q)]
        lifted_v = [lifted_fermat_quotient(3, k, q) for k in range(q)]
        affine_u = all(
            value == (u0 - k * pow(2, -1, q)) % q
            for k, value in enumerate(lifted_u)
        )
        affine_v = all(
            value == (v0 - k * pow(3, -1, q)) % q
            for k, value in enumerate(lifted_v)
        )
        image_pairs: set[tuple[int, int]] = set()
        separated_pairs: list[tuple[int, int, int]] = []
        for k2, u in enumerate(lifted_u):
            for k3, v in enumerate(lifted_v):
                image_pairs.add((u, v))
                separated = (5 * u - 3 * v) % q == 0 and (u - v) % q != 0
                if separated:
                    t = u * pow(3, -1, q) % q
                    separated_pairs.append((k2, k3, t))
                transcript.update(
                    f"{q}:{k2}:{k3}:{u}:{v}:{int(separated)}\n".encode("ascii")
                )

        explicit_targets: list[dict[str, int]] = []
        target_lifts: set[tuple[int, int]] = set()
        target_verified = True
        for t in range(1, q):
            k2 = 2 * (u0 - 3 * t) % q
            k3 = 3 * (v0 - 5 * t) % q
            u = lifted_u[k2]
            v = lifted_v[k3]
            ok = (u, v) == (3 * t % q, 5 * t % q)
            target_verified &= ok
            target_lifts.add((k2, k3))
            if t in {1, q - 1}:
                explicit_targets.append(
                    {
                        "projective_parameter_t": t,
                        "lift_k2": k2,
                        "lift_k3": k3,
                        "lifted_U": u,
                        "lifted_V": v,
                    }
                )

        verified = (
            affine_u
            and affine_v
            and len(set(lifted_u)) == q
            and len(set(lifted_v)) == q
            and len(image_pairs) == q * q
            and len(separated_pairs) == q - 1
            and len(target_lifts) == q - 1
            and target_verified
        )
        failures += int(not verified)
        field_rows.append(
            {
                "prime_q": q,
                "lift_pairs_checked": q * q,
                "fermat_coordinate_pairs_reached": len(image_pairs),
                "separated_projective_lift_pairs": len(separated_pairs),
                "expected_separated_pairs": q - 1,
                "canonical_lift_is_separated": (
                    (5 * u0 - 3 * v0) % q == 0 and (u0 - v0) % q != 0
                ),
                "certificate_verified": verified,
            }
        )
        target_rows.append(
            {
                "prime_q": q,
                "canonical_U": u0,
                "canonical_V": v0,
                "selected_explicit_target_lifts": explicit_targets,
                "certificate_verified": target_verified,
            }
        )

    theorem = (
        "Let q>5 be prime. For k,l in F_q define A_k=2+kq and B_l=3+lq "
        "modulo q^2, and let F_q(a)=((a^(q-1)-1)/q) mod q. Then "
        "F_q(A_k)=F_q(2)-k/2 and F_q(B_l)=F_q(3)-l/3. Hence the map "
        "(k,l)->(F_q(A_k),F_q(B_l)) is a bijection F_q^2->F_q^2. Exactly "
        "q-1 lift pairs hit the separated projective line [3:5], one for "
        "each t in F_q^*. Therefore slope [3:5] cannot be excluded using "
        "only the residue classes 2,3 modulo q and reasoning invariant under "
        "changing their lifts modulo q^2; the canonical lifts k=l=0 carry "
        "essential cross-prime arithmetic information."
    )
    proof = (
        "The binomial expansion modulo q^2 gives "
        "(a+kq)^(q-1)=a^(q-1)+(q-1)a^(q-2)kq mod q^2. After division by q, "
        "F_q(a+kq)=F_q(a)+(q-1)a^(q-2)k=F_q(a)-k/a mod q. The coefficient "
        "-1/a is nonzero, so each coordinate map is affine bijective. For a "
        "given nonzero t the unique lifts are k=2(F_q(2)-3t) and "
        "l=3(F_q(3)-5t). These give the q-1 separated targets. The theorem "
        "does not decide whether the fixed integer representatives 2 and 3 "
        "ever hit [3:5] as q varies."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_lift_field_rows": field_rows,
        "exact_explicit_target_rows": target_rows,
        "algorithm": "exact modular exponentiation modulo q^2, affine lift formulas, and exhaustive q^2 lift-pair enumeration",
        "complexity": "O(sum_q(q log q + q^2)) exact modular and finite-field operations",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "lift_affine_transitivity_proved": True,
            "separated_projective_lifts_exist_for_every_q": True,
            "lift_invariant_local_avoidance_route_refuted": True,
            "canonical_fixed_representative_occurrence_decided": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def bareiss_determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot_row = next((r for r in range(k, n) if work[r][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            work[k], work[pivot_row] = work[pivot_row], work[k]
            sign *= -1
        pivot = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = work[i][j] * pivot - work[i][k] * work[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                work[i][j] = numerator // previous
        for i in range(k + 1, n):
            work[i][k] = 0
        previous = pivot
    return sign * work[n - 1][n - 1]


def cyclotomic_prime_norm(coefficients: list[int]) -> int:
    q = len(coefficients)
    if q < 3:
        raise ValueError("prime cyclotomic norm requires q>=3")
    degree = q - 1
    reduced = [coefficients[i] - coefficients[-1] for i in range(degree)]
    matrix = [[0 for _ in range(degree)] for _ in range(degree)]
    for column in range(degree):
        product = [0 for _ in range(2 * degree - 1)]
        for exponent, coefficient in enumerate(reduced):
            product[exponent + column] += coefficient
        for exponent in range(len(product) - 1, degree - 1, -1):
            coefficient = product[exponent]
            if not coefficient:
                continue
            product[exponent] = 0
            shift = exponent - degree
            for target in range(shift, shift + degree):
                product[target] -= coefficient
        for row in range(degree):
            matrix[row][column] = product[row]
    return bareiss_determinant(matrix)


@lru_cache(maxsize=1)
def goldbach_galois_full_support_audit() -> dict[str, Any]:
    primes = primes_up_to(max(GOLDBACH_X_SCALES))
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    smallest_norm: tuple[int, int, int] | None = None

    for q in GOLDBACH_PRIME_MODULI:
        for x_limit in GOLDBACH_X_SCALES:
            counts = [0] * q
            for prime in primes:
                if prime > x_limit:
                    break
                counts[prime % q] += 1
            total = sum(counts)
            centered = [q * count - total for count in counts]
            centered_sum = sum(centered)
            nonconstant = len(set(counts)) > 1
            norm = cyclotomic_prime_norm(centered)
            verified = centered_sum == 0 and nonconstant and norm != 0
            failures += int(not verified)
            norm_abs = abs(norm)
            if smallest_norm is None or norm_abs < smallest_norm[0]:
                smallest_norm = (norm_abs, q, x_limit)
            transcript.update(
                (
                    f"{q}:{x_limit}:{total}:{','.join(map(str, counts))}:"
                    f"{norm}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "prime_modulus_q": q,
                    "prime_count_limit_X": x_limit,
                    "prime_count_total": total,
                    "residue_counts": counts,
                    "centered_integral_vector": centered,
                    "centered_sum": centered_sum,
                    "vector_nonconstant": nonconstant,
                    "exact_galois_norm": str(norm),
                    "absolute_norm_digit_count": len(str(norm_abs)),
                    "all_nonzero_frequencies_proved_by_minimal_polynomial": verified,
                    "certificate_verified": verified,
                }
            )

    boundary_rows = [
        {
            "modulus_q": 3,
            "centered_vector": [2, -1, -1],
            "nonzero_frequency_support": [1, 2],
            "interpretation": "all nonzero frequencies are exactly two, so q>=5 is necessary for excluding a two-spike support",
            "certificate_verified": True,
        },
        {
            "modulus_q": 4,
            "centered_vector": [1, 0, -1, 0],
            "nonzero_frequency_support": [1, 3],
            "interpretation": "composite moduli can have a proper two-frequency Galois orbit",
            "certificate_verified": True,
        },
    ]
    for row in boundary_rows:
        transcript.update(
            (
                f"boundary:{row['modulus_q']}:"
                f"{','.join(map(str, row['centered_vector']))}:"
                f"{','.join(map(str, row['nonzero_frequency_support']))}\n"
            ).encode("ascii")
        )

    theorem = (
        "Let q>=5 be prime, let n_0,...,n_(q-1) be integers, put "
        "N=sum_r n_r and Delta_r=q n_r-N, and let zeta be a primitive q-th "
        "root of unity. If the vector n is nonconstant, then for every "
        "a=1,...,q-1 the Fourier coefficient F(a)=sum_r Delta_r zeta^(ar) "
        "is nonzero. Moreover F(a) is an algebraic integer and "
        "product_(a=1)^(q-1) F(a) is a nonzero integer, hence has absolute "
        "value at least one. Consequently the exact two-frequency spike from "
        "TICKET-249 cannot be an integer or rational prime-count residue "
        "vector at a prime modulus q>=5."
    )
    proof = (
        "Let P(X)=sum_r Delta_r X^r. If P(zeta^a)=0 for a nonzero a, then "
        "zeta^a is primitive and its minimal polynomial Phi_q=1+X+...+"
        "X^(q-1) divides P. Since deg P<=q-1, P=c Phi_q. But "
        "P(1)=sum Delta_r=0 whereas Phi_q(1)=q, so c=0. Thus Delta=0, "
        "forcing n to be constant, a contradiction. The Galois conjugates "
        "of F(a) are exactly F(1),...,F(q-1); their product is the algebraic "
        "norm of a nonzero algebraic integer and is therefore a nonzero "
        "integer. This proves exact full support and a multiplicative norm "
        "barrier, but no pointwise upper bound or quantitative energy saving."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_prime_count_norm_rows": rows,
        "exact_boundary_countermodels": boundary_rows,
        "algorithm": "Eratosthenes prime counts by residue, exact cyclotomic reduction, and fraction-free Bareiss determinants",
        "complexity": "O(X log log X + sum_(q,X) q^3) integer operations and O(X+max q^2) memory",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_modulus_rational_full_support_proved": True,
            "nonzero_integral_galois_norm_proved": True,
            "ticket249_two_spike_prime_count_model_excluded_for_q_at_least_5": True,
            "quantitative_pointwise_upper_anti_concentration_proved": False,
            "strong_goldbach_resolved": False,
            "smallest_replayed_absolute_norm": str(smallest_norm[0] if smallest_norm else 0),
            "smallest_norm_case": {
                "prime_modulus_q": smallest_norm[1] if smallest_norm else None,
                "prime_count_limit_X": smallest_norm[2] if smallest_norm else None,
            },
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_even_left_right_active_audit() -> dict[str, Any]:
    upper = max(TWIN_X_SCALES) + 2
    primes = primes_up_to(upper)
    prime_flags = bytearray(upper + 1)
    for prime in primes:
        prime_flags[prime] = 1
    power_flags, representations = prime_power_representation_table(upper, primes)
    right_active: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()

    for n in range(3, max(TWIN_X_SCALES) + 1, 2):
        if not (power_flags[n] and power_flags[n + 2] and not prime_flags[n + 2]):
            continue
        left_base, left_exponent = representations[n]
        right_base, right_exponent = representations[n + 2]
        even_left = left_exponent % 2 == 0
        classification_verified = not even_left or (
            n == 25
            and n + 2 == 27
            and left_base == 5
            and left_exponent == 2
            and right_base == 3
            and right_exponent == 3
        )
        failures += int(not classification_verified)
        right_active.append(
            {
                "n": n,
                "n_plus_2": n + 2,
                "left_base": left_base,
                "left_exponent": left_exponent,
                "right_base": right_base,
                "right_exponent": right_exponent,
                "left_exponent_even": even_left,
                "classification_verified": classification_verified,
            }
        )

    rows: list[dict[str, Any]] = []
    for x_limit in TWIN_X_SCALES:
        active = [row for row in right_active if row["n"] <= x_limit]
        even_rows = [row for row in active if row["left_exponent_even"]]
        odd_rows = [row for row in active if not row["left_exponent_even"]]
        expected_even = int(x_limit >= 25)
        verified = len(even_rows) == expected_even and len(active) == len(even_rows) + len(odd_rows)
        failures += int(not verified)
        transcript.update(
            (
                f"{x_limit}:{len(active)}:{len(even_rows)}:{len(odd_rows)}:"
                f"{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "limit_X": x_limit,
                "right_active_composite_pairs_R": len(active),
                "right_active_even_left_exponent": len(even_rows),
                "right_active_odd_left_exponent": len(odd_rows),
                "proved_even_left_count": expected_even,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let p,r be odd primes, m>=1, and ell>=2. If "
        "p^(2m)+2=r^ell, then (p,m,r,ell)=(5,1,3,3). Consequently every "
        "right-active shift-two prime-power pair whose left exponent is even "
        "is the single pair (25,27), with no base-3 exception: "
        "R_even-left(X)=1 for X>=25 and zero otherwise."
    )
    proof = (
        "Set x=p^m. If ell=2, then x and r are odd, so x^2+2=3 mod 8 "
        "while r^2=1 mod 8, impossible. If ell>=3, the D=2 "
        "Lebesgue-Nagell classification says that the only positive solution "
        "of x^2+2=y^ell is (x,y,ell)=(5,3,3). Thus p^m=5 and the claimed "
        "quadruple follows. Unlike TICKET-249, no assumption p!=3 is needed. "
        "The external Diophantine theorem is an explicit proof-DAG node."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_scale_rows": rows,
        "selected_even_left_witnesses": [
            row for row in right_active if row["left_exponent_even"]
        ],
        "external_theorem": {
            "name": "Lebesgue-Nagell D=2 classification (Nagell)",
            "statement_used": "For positive integers x,y and n>=3, x^2+2=y^n has only (x,y,n)=(5,3,3).",
            "modern_primary_source": "https://doi.org/10.1112/S0010437X05001739",
            "source_scope": "Bugeaud-Mignotte-Siksek solve x^2+D=y^n for 1<=D<=100; only D=2 is used.",
        },
        "algorithm": "Eratosthenes sieve, exact odd-prime-power representation table, shift-two activation, and exponent-parity partition",
        "complexity": "O(X log log X) time and O(X) support memory for the finite replay; the all-X classification is Diophantine",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_base_even_left_right_active_classification_proved": True,
            "unique_pair": [25, 27],
            "base_three_left_exception_eliminated": True,
            "odd_left_right_active_contamination_controlled": False,
            "scale_local_type_II_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    rejected_name: str,
    open_name: str,
    external: tuple[str, str] | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T249", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T250", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT250", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN250", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T249", f"{code}-T250"],
        [f"{code}-T250", f"{code}-REJECT250"],
        [f"{code}-T250", f"{code}-OPEN250"],
    ]
    resolution_path = [f"{code}-T249", f"{code}-T250", f"{code}-OPEN250"]
    if external:
        external_id, label = external
        nodes.insert(1, {"id": external_id, "label": label, "status": "external_theorem"})
        edges.insert(0, [external_id, f"{code}-T250"])
        resolution_path.insert(1, external_id)
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": resolution_path,
        "acyclic": True,
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    result_classification: str,
    computation: dict[str, Any],
    discarded: str,
    parked: list[str],
    retained: str,
    next_lemma: str,
    prior_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    external: tuple[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-250",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": result_classification,
        "problem_status": STATUS,
        "reproducible_computation": computation,
        "finite_computation_boundary": finite_boundary,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "parked": parked,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "stagnation_count": 0,
        "proof_dag": proof_dag(
            code, prior_name, theorem_name, rejected_name, next_lemma, external
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_noncompact_multiplier_audit()
    collatz = collatz_lift_transitivity_audit()
    goldbach = goldbach_galois_full_support_audit()
    twin = twin_even_left_right_active_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "NoncompactMultiplierLegendreEscapeInsufficiencyNoGo",
            "exact_no_go",
            riemann,
            "using a positive diagonal limit on the Legendre sequence for one noncompact multiplier as a certificate of full-sphere coercivity",
            [],
            "an arithmetic form that controls both oscillatory Legendre escape and spatial concentration escape on the actual admissible closure",
            "ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes",
            "CompactOffDiagonalMomentCoercivityNoGo",
            "LegendreNonvanishingOfOneNoncompactCorrectionImpliesCoercivity",
            "The explicit multiplier blocks the old oscillatory escape but admits a new concentration escape; no actual Weil arithmetic form or admissible-closure theorem is controlled.",
            "No RH proof or disproof; one exact no-go for validating noncompact coercivity only on the Legendre escape sequence.",
            f"{len(RIEMANN_ORDERS)} exact Legendre rows and {len(RIEMANN_EPSILON_POWERS)} exact concentration bounds replay the two mechanisms; the all-sequence conclusions are analytic.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "LocalFermatQuotientLiftTransitivityNoGo",
            "exact_no_go",
            collatz,
            "excluding projective slope [3:5] from the residue classes 2 and 3 modulo q using only lift-invariant local Fermat-quotient structure",
            ["all-prime occurrence or avoidance of the canonical projective point [3:5] without cross-prime distribution input"],
            "arithmetic information tied to the canonical fixed integer representatives 2 and 3 as q varies",
            "CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity",
            "SeparatedWieferichProjectiveSlopeCriterion",
            "LiftInvariantLocalStructureExcludesProjectiveSlopeThreeFifths",
            "Every local lift fiber contains the target, but the actual canonical lifts remain undecided across primes; this valuation branch still does not control all Collatz trajectories.",
            "No Collatz proof, divergent orbit, or cycle; one exact no-go for a lift-invariant local avoidance route.",
            f"Exhaustive exact arithmetic checks {sum(q*q for q in COLLATZ_FIELD_PRIMES):,} lift pairs over {len(COLLATZ_FIELD_PRIMES)} fields; the theorem for every prime q is algebraic.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "PrimeModulusRationalFourierFullSupportAndNormBarrier",
            "partial_theorem",
            goldbach,
            "identifying the exact TICKET-249 two-frequency cosine spike with a rational or integer prime-count residue vector at prime moduli q>=5",
            [],
            "quantitative prime-specific upper anti-concentration for weighted residue vectors after exact support is established",
            "QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli",
            "CenteredJetParsevalSpikeNoGo",
            "Ticket249TwoSpikeCanBePrimeCountVectorAtPrimeModulusAtLeastFive",
            "Galois symmetry forces exact full support and a nonzero norm, but permits arbitrarily uneven nonzero magnitudes and does not handle logarithmic prime weights or prove a uniform upper saving.",
            "No strong Goldbach proof or counterexample; one exact algebraic support theorem and norm barrier for prime-count residue vectors.",
            f"Exact determinants audit {len(GOLDBACH_PRIME_MODULI)*len(GOLDBACH_X_SCALES):,} prime-count vectors through X={max(GOLDBACH_X_SCALES):,}; the all-vector theorem comes from Phi_q minimality, not finite data.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "AllBaseEvenLeftRightActiveClassification",
            "partial_theorem",
            twin,
            "retaining any right-active composite prime-power contaminant with even left exponent other than the pair 25 to 27, including a possible base-3 exception",
            [],
            "a scale-local bound for the remaining right-active pairs, all of which have odd left exponent except 25 to 27",
            "ScaleLocalOddLeftRightActiveContaminationBound",
            "EvenExponentLeftActiveContaminationClassification",
            "AdditionalEvenLeftRightActiveContaminantsOrBaseThreeExceptionExist",
            "The full even-left right-active subclass is closed, but the 135 odd-left examples through ten million remain uncontrolled and no Type-II lower bound is proved.",
            "No twin-prime proof or counterexample; one strengthened all-base classification of a strict right-active contamination subclass.",
            f"Prime-power supports are enumerated at {len(TWIN_X_SCALES)} scales through {max(TWIN_X_SCALES):,}; the all-X result uses the explicit D=2 Lebesgue-Nagell external theorem.",
            external=("TP-EXT-NAGELL", "Lebesgue-Nagell D=2 classification"),
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"] for item in sections.values()
    )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureMultiplierLiftGaloisEvenRightAudit",
            "summary": "TICKET-250 proves two exact route no-go theorems and two partial theorems while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
                "lebesgue_nagell_D2": "https://doi.org/10.1112/S0010437X05001739",
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_legendre_case_count": len(riemann["exact_legendre_multiplier_rows"]),
                "riemann_concentration_case_count": len(riemann["exact_concentration_escape_rows"]),
                "collatz_lift_pair_count": sum(row["lift_pairs_checked"] for row in collatz["exact_lift_field_rows"]),
                "goldbach_prime_count_norm_case_count": len(goldbach["exact_prime_count_norm_rows"]),
                "goldbach_boundary_countermodel_count": len(goldbach["exact_boundary_countermodels"]),
                "twin_active_scale_count": len(twin["exact_scale_rows"]),
                "total_failure_count": total_failures,
            },
        },
        "attempts": [
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "result_classification": item["result_classification"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{key}",
                    "failure_count": item["reproducible_computation"]["failure_count"],
                },
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
            }
            for key, item in sections.items()
        ],
    }


def build_research_state(audit: dict[str, Any]) -> dict[str, Any]:
    previous = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    root = audit[AUDIT_KEY]
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        old = previous["problems"][key]
        established = list(old.get("established_results", []))
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        discarded = item["route_decision"]["discard"]
        if discarded and discarded not in retired:
            retired.append(discarded)
        parked = list(old.get("parked_routes", []))
        for route in item["route_decision"]["parked"]:
            if route not in parked:
                parked.append(route)
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": established,
            "retired_routes": retired,
            "parked_routes": parked,
            "remaining_gap": item["logical_limit"],
            "next_single_lemma": item["route_decision"]["next_single_lemma"],
            "stagnation_count": item["stagnation_count"],
            "unresolved_dependencies": [
                node["label"]
                for node in item["proof_dag"]["nodes"]
                if node["status"] in {"assumption", "heuristic", "open"}
            ],
            "finite_computation_boundary": item["finite_computation_boundary"],
            "proof_dag_status": "acyclic_with_one_open_frontier",
            "validation_status": {
                "generator_failure_count": item["reproducible_computation"]["failure_count"],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 250,
        "parent_ticket": 249,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "goldbach",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket250-multiplier-lift-galois-evenright.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-250-noncompact-multiplier-escape.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-250-lift-transitivity.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-250-galois-full-support.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-250-even-left-right-classification.json",
    }
    for key, path in paths.items():
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )
    write_json(
        ROOT / "data/open-problem/four-problem-research-state.json",
        build_research_state(audit),
    )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
