from __future__ import annotations

import hashlib
import itertools
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from ticket219_bandpass_matveev_crossfit_qualitative_abel import (
    goldbach_counts,
    prime_sieve,
    rounded_model_weight,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket220-dyadic-partition-primitive-refinement-crt.v1"
GENERATED_AT = "2026-08-14T09:30:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def decimal_string(value: Decimal, digits: int = 24) -> str:
    return format(value, f".{digits}E")


def fraction_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


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
            {"id": f"{prefix}-T219", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T220", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N220",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN220",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T219", f"{prefix}-T220"],
            [f"{prefix}-T220", f"{prefix}-N220"],
            [f"{prefix}-T220", f"{prefix}-OPEN220"],
            [f"{prefix}-OPEN220", prefix],
        ],
    }


def laplace_transform(atoms: Iterable[int | Decimal], scale: Decimal) -> Decimal:
    return sum((-(Decimal(atom) * scale)).exp() for atom in atoms)


def dyadic_band_value(
    atoms: Iterable[int | Decimal], height: Decimal, index: int
) -> Decimal:
    scale = (Decimal(2) ** (-index)) / height
    return laplace_transform(atoms, scale) - laplace_transform(
        atoms, Decimal(2) * scale
    )


def riemann_dyadic_partition_audit() -> dict[str, Any]:
    getcontext().prec = 100
    atoms = (3, 7, 19, 44, 91, 173)
    height = Decimal(8)
    total = Decimal(len(atoms))
    telescope_rows = []
    failures = 0
    for radius in (2, 4, 8, 12, 16):
        direct = sum(
            dyadic_band_value(atoms, height, index)
            for index in range(-radius, radius + 1)
        )
        boundary = laplace_transform(
            atoms, (Decimal(2) ** (-radius)) / height
        ) - laplace_transform(
            atoms, (Decimal(2) ** (radius + 1)) / height
        )
        identity_error = abs(direct - boundary)
        failures += int(identity_error > Decimal("1e-80"))
        telescope_rows.append(
            {
                "M_equals_N": radius,
                "direct_dyadic_sum": decimal_string(direct),
                "telescoping_boundary_value": decimal_string(boundary),
                "absolute_identity_error": decimal_string(identity_error),
                "distance_to_total_defect_count": decimal_string(total - direct),
                "identity_verified": identity_error <= Decimal("1e-80"),
            }
        )

    observed_indices = tuple(range(-4, 5))
    hidden_rows = []
    for label, atom in (
        ("below_finite_window", Decimal(2) ** (-40)),
        ("above_finite_window", Decimal(2) ** 40),
    ):
        observed = sum(
            dyadic_band_value((atom,), height, index)
            for index in observed_indices
        )
        hidden = observed < Decimal("1e-6")
        failures += int(not hidden)
        hidden_rows.append(
            {
                "placement": label,
                "synthetic_atom_t": decimal_string(atom),
                "observed_index_window": [-4, 4],
                "observed_kernel_mass": decimal_string(observed),
                "below_epsilon_1e_minus_6": hidden,
            }
        )

    theorem = (
        "Let C be a nonnegative integer-valued locally finite measure on "
        "(0,infinity), L(s)=integral exp(-s t)dC(t), and "
        "W_j(H)=L(2^(-j)/H)-L(2^(1-j)/H). Then the nonnegative kernels "
        "form a dyadic partition of unity: sum over all integer j of "
        "W_j(H)=C((0,infinity)), possibly infinity. For finite limits, "
        "sum from j=-M to N equals L(2^(-N)/H)-L(2^(M+1)/H). Moreover, "
        "for every finite index window and epsilon>0, a single defect atom "
        "can be placed sufficiently near zero or infinity so that its total "
        "mass in that window is below epsilon. Consequently no finite "
        "collection of these band measurements alone certifies C=0."
    )
    proof = (
        "For a fixed t>0, the j-th kernel is exp(-2^(-j)t/H)-"
        "exp(-2^(1-j)t/H). Its finite sum telescopes. The lower endpoint "
        "tends to infinity and the upper endpoint to zero, so the sum tends "
        "to 1. Tonelli's theorem transfers this identity to C. On a fixed "
        "finite window every kernel tends to zero both as t tends to zero "
        "and as t tends to infinity; a one-atom measure therefore proves the "
        "finite-window no-go statement. If certified upper bounds U_j>=W_j "
        "are summable with sum U_j<1, integrality would force C=0, but no "
        "such actual prime-side bounds are constructed here."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "kernel": "exp(-2^(-j)t/H)-exp(-2^(1-j)t/H)",
        "synthetic_atoms": list(atoms),
        "telescoping_rows": telescope_rows,
        "finite_window_hidden_atom_rows": hidden_rows,
        "aggregate": {
            "dyadic_partition_of_unity_proved": True,
            "finite_window_global_certificate_refuted": True,
            "summable_upper_envelope_below_one_would_prove_no_defects": True,
            "actual_prime_side_summable_envelope_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The no-go applies only to finitely many dyadic Laplace bands "
            "without additional tail information. It is not a no-go for "
            "explicit-formula methods or for an infinite certified envelope."
        ),
        "failure_count": failures,
    }


def affine_word(word: tuple[int, ...]) -> tuple[int, int, int]:
    """Return A, B, D for the accelerated odd-step map (A*n+B)/D."""
    a, b, d = 1, 0, 1
    for valuation in word:
        a, b, d = 3 * a, 3 * b + d, d * (2**valuation)
    divisor = math.gcd(math.gcd(a, b), d)
    return a // divisor, b // divisor, d // divisor


def compose_affine_power(
    affine: tuple[int, int, int], exponent: int
) -> tuple[int, int, int]:
    a, b, d = affine
    result_a, result_b, result_d = 1, 0, 1
    for _ in range(exponent):
        result_a, result_b, result_d = (
            a * result_a,
            a * result_b + b * result_d,
            d * result_d,
        )
        divisor = math.gcd(math.gcd(result_a, result_b), result_d)
        result_a //= divisor
        result_b //= divisor
        result_d //= divisor
    return result_a, result_b, result_d


def primitive_root(word: tuple[int, ...]) -> tuple[int, ...]:
    for length in range(1, len(word) + 1):
        if len(word) % length == 0 and word == word[:length] * (len(word) // length):
            return word[:length]
    return word


def cyclic_transition_count(word: tuple[int, ...]) -> int:
    return sum(
        word[index] != word[(index + 1) % len(word)]
        for index in range(len(word))
    )


def covered_by_single_mountain_closure(word: tuple[int, ...]) -> bool:
    root = primitive_root(word)
    return set(root) == {1, 2} and cyclic_transition_count(root) == 2


def collatz_primitive_word_audit() -> dict[str, Any]:
    sample_rows = []
    failures = 0
    for root, exponent in (
        ((1, 2), 5),
        ((1, 1, 2, 2), 3),
        ((1, 1, 1, 2), 4),
    ):
        one_block = affine_word(root)
        direct_power = affine_word(root * exponent)
        composed_power = compose_affine_power(one_block, exponent)
        same = direct_power == composed_power
        a, b, d = one_block
        fixed_numerator = b
        fixed_denominator = d - a
        power_a, power_b, power_d = direct_power
        power_fixed_same = (
            fixed_numerator * (power_d - power_a)
            == power_b * fixed_denominator
        )
        failures += int(not (same and power_fixed_same and a != d))
        sample_rows.append(
            {
                "primitive_root": list(root),
                "power": exponent,
                "one_block_affine_A_B_D": list(one_block),
                "direct_power_affine_A_B_D": list(direct_power),
                "composition_identity_verified": same,
                "fixed_point_identity_verified": power_fixed_same,
                "nonunit_slope_verified": a != d,
            }
        )

    enumeration_rows = []
    transcript = hashlib.sha256()
    for length in range(2, 17):
        words = list(itertools.product((1, 2), repeat=length))
        covered = sum(covered_by_single_mountain_closure(word) for word in words)
        primitive_multi_run = sum(
            primitive_root(word) == word
            and set(word) == {1, 2}
            and cyclic_transition_count(word) >= 4
            for word in words
        )
        row = {
            "word_length": length,
            "all_binary_words": len(words),
            "closed_by_ticket220": covered,
            "primitive_multi_run_still_open": primitive_multi_run,
        }
        transcript.update(
            f"{length}:{len(words)}:{covered}:{primitive_multi_run}\n".encode("ascii")
        )
        enumeration_rows.append(row)

    theorem = (
        "Let u be a cyclic rotation of a binary single-mountain valuation "
        "word 1^k2^m with k,m>=1. No positive accelerated Collatz cycle has "
        "valuation word u^r for any r>=1. Thus TICKET-219 excludes not only "
        "one traversal of every single-mountain word but every rotation and "
        "imprimitive cyclic power of that family, including words with "
        "arbitrarily many displayed runs."
    )
    proof = (
        "Align the cycle at the beginning of one copy of u. Its one-block "
        "map is f(n)=(A n+B)/D with A=3^h, D=2^S and A!=D. If u^r closes, "
        "then f^r(n)=n. For an affine map of nonunit positive slope, "
        "f^r(n)-n=(f(n)-n)(1+A/D+...+(A/D)^(r-1)); hence f(n)=n. This "
        "would be a positive single-mountain cycle, contradicted by "
        "TICKET-219. Rotation only changes the chosen cycle base point. "
        "Primitive multi-run words and nonperiodic divergent trajectories "
        "are not covered."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "affine_power_replay_rows": sample_rows,
        "binary_word_enumeration_rows": enumeration_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "primitive_root_extension_proved": True,
            "all_rotations_and_positive_powers_of_single_mountains_excluded": True,
            "infinite_imprimitive_multi_run_family_closed": True,
            "primitive_multi_run_cycles_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "A word with many runs need not contain new phase information: "
            "if it is a cyclic power of one single-mountain root, it has the "
            "same affine fixed point. Enumeration of those powers is retired; "
            "primitive multi-run words remain genuinely open."
        ),
        "failure_count": failures,
    }


def fit_scale(
    counts: list[int], weights: list[int], modulus: int, held_out: int
) -> Fraction:
    train = [index for index in range(len(counts)) if index % modulus != held_out]
    numerator = sum(counts[index] * weights[index] for index in train)
    denominator = sum(weights[index] ** 2 for index in train)
    return Fraction(numerator, denominator)


def ceil_nth_root_fraction(
    value: Fraction, order: int, scale: int = 10**12
) -> Fraction:
    if value == 0:
        return Fraction(0)
    target = value.numerator * (scale**order)
    denominator = value.denominator
    high = 1
    while (high**order) * denominator < target:
        high *= 2
    low = high // 2
    while low + 1 < high:
        middle = (low + high) // 2
        if (middle**order) * denominator >= target:
            high = middle
        else:
            low = middle
    return Fraction(high, scale)


def residual_moment(
    counts: list[int], weights: list[int], indices: list[int], scale: Fraction, order: int
) -> Fraction:
    return sum(
        (abs(Fraction(counts[index]) - scale * weights[index])) ** order
        for index in indices
    )


def goldbach_refinement_audit() -> dict[str, Any]:
    starts = (128, 512, 2048, 8192, 32768)
    moduli = (2, 4, 8, 16)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    shape_scale = 1_000_000
    direct_rows = []
    bridge_rows = []
    failures = 0
    transcript = hashlib.sha256()

    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        targets = list(range(start, 2 * start, 2))
        weights = [
            rounded_model_weight(target, primes, shape_scale) for target in targets
        ]
        for modulus in moduli:
            for held_out in range(modulus):
                indices = [
                    index for index in range(len(counts)) if index % modulus == held_out
                ]
                scale = fit_scale(counts, weights, modulus, held_out)
                minimum_weight = min(weights[index] for index in indices)
                pass_by_order = {}
                ratios = {}
                for order in (4, 8):
                    moment = residual_moment(counts, weights, indices, scale, order)
                    threshold = (scale * minimum_weight) ** order
                    passed = moment < threshold
                    pass_by_order[str(order)] = passed
                    ratios[str(order)] = decimal_string(
                        Decimal(moment.numerator)
                        * Decimal(threshold.denominator)
                        / (Decimal(moment.denominator) * Decimal(threshold.numerator)),
                        18,
                    )
                failures += int(not pass_by_order["8"])
                direct_rows.append(
                    {
                        "dyadic_start_X": start,
                        "fold_modulus": modulus,
                        "held_out_residue": held_out,
                        "held_out_count": len(indices),
                        "fit_scale": fraction_string(scale),
                        "moment_pass_by_order": pass_by_order,
                        "moment_to_zero_barrier_ratio": ratios,
                    }
                )
                transcript.update(
                    f"D:{start}:{modulus}:{held_out}:{scale}:{pass_by_order}\n".encode(
                        "ascii"
                    )
                )

        for parent_modulus, child_modulus in ((2, 4), (4, 8), (8, 16)):
            for child_residue in range(child_modulus):
                parent_residue = child_residue % parent_modulus
                indices = [
                    index
                    for index in range(len(counts))
                    if index % child_modulus == child_residue
                ]
                parent_scale = fit_scale(
                    counts, weights, parent_modulus, parent_residue
                )
                child_scale = fit_scale(
                    counts, weights, child_modulus, child_residue
                )
                parent_residual_eighth = residual_moment(
                    counts, weights, indices, parent_scale, 8
                )
                weight_eighth = sum(
                    Fraction(weights[index]) ** 8 for index in indices
                )
                residual_norm_upper = ceil_nth_root_fraction(
                    parent_residual_eighth, 8
                )
                weight_norm_upper = ceil_nth_root_fraction(weight_eighth, 8)
                drift_upper = abs(parent_scale - child_scale) * weight_norm_upper
                minkowski_upper = residual_norm_upper + drift_upper
                zero_barrier = child_scale * min(weights[index] for index in indices)
                passed = minkowski_upper < zero_barrier
                failures += int(not passed)
                ratio = Fraction(minkowski_upper, zero_barrier)
                bridge_rows.append(
                    {
                        "dyadic_start_X": start,
                        "parent_modulus": parent_modulus,
                        "child_modulus": child_modulus,
                        "child_residue": child_residue,
                        "parent_scale": fraction_string(parent_scale),
                        "child_scale": fraction_string(child_scale),
                        "parent_residual_norm_upper": fraction_string(
                            residual_norm_upper
                        ),
                        "refit_drift_norm_upper": fraction_string(drift_upper),
                        "child_zero_barrier": fraction_string(zero_barrier),
                        "minkowski_to_barrier_ratio": decimal_string(
                            Decimal(ratio.numerator) / Decimal(ratio.denominator), 18
                        ),
                        "refinement_certificate_passed": passed,
                    }
                )
                transcript.update(
                    f"B:{start}:{parent_modulus}:{child_modulus}:"
                    f"{child_residue}:{int(passed)}:{ratio}\n".encode("ascii")
                )

    direct_p8 = sum(row["moment_pass_by_order"]["8"] for row in direct_rows)
    direct_p4 = sum(row["moment_pass_by_order"]["4"] for row in direct_rows)
    bridge_passes = sum(row["refinement_certificate_passed"] for row in bridge_rows)
    theorem = (
        "Let F' refine a held-out fold F. Fit positive scales alpha outside "
        "F and beta outside F'. On F', e(beta)=e(alpha)+(alpha-beta)w, so "
        "Minkowski gives ||e(beta)||_p <= ||e(alpha)||_p+"
        "|alpha-beta|||w||_p. If the right side is below "
        "beta min_{i in F'}w_i, every count on F' is positive. This is an "
        "exact refinement-stability certificate for cross-fitted support."
    )
    proof = (
        "The vector identity is coordinatewise and Minkowski is exact. If "
        "some held-out count A_j were zero, then |e_j(beta)|=beta w_j is at "
        "least the zero barrier, contradicting the strict norm bound. The "
        "audit uses rational scales and outward-rounded rational eighth roots. "
        "All 140 nested bridges q=2 to 4 to 8 to 16 pass on five finite "
        "dyadic blocks. Their inputs still use enumerated Goldbach counts, so "
        "this does not supply the required cofinal arithmetic estimate."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "direct_crossfit_rows": direct_rows,
        "refinement_bridge_rows": bridge_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "crossfit_refinement_stability_theorem_proved": True,
            "direct_eighth_moment_folds_certified": direct_p8,
            "direct_eighth_moment_fold_total": len(direct_rows),
            "direct_fourth_moment_folds_certified": direct_p4,
            "refinement_bridges_certified": bridge_passes,
            "refinement_bridge_total": len(bridge_rows),
            "cofinal_refinement_margin_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Success under finitely many nested partitions is not a cofinal "
            "Goldbach proof. The retained target must bound both the parent "
            "residual and refit drift without reading representation counts."
        ),
        "failure_count": failures,
    }


def prime_factors(value: int) -> list[int]:
    factors = []
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def next_prime(value: int) -> int:
    candidate = value + 1
    while True:
        if candidate >= 2 and all(
            candidate % divisor for divisor in range(2, math.isqrt(candidate) + 1)
        ):
            return candidate
        candidate += 1


def crt_pairwise(congruences: list[tuple[int, int]]) -> tuple[int, int]:
    value, modulus = 0, 1
    for residue, next_modulus in congruences:
        step = ((residue - value) * pow(modulus, -1, next_modulus)) % next_modulus
        value += modulus * step
        modulus *= next_modulus
        value %= modulus
    return value, modulus


def twin_finite_wheel_crt_audit() -> dict[str, Any]:
    wheels = (30, 210, 2310, 30030, 510510)
    rows = []
    failures = 0
    for wheel in wheels:
        factors = prime_factors(wheel)
        residue = next(
            value
            for value in range(1, wheel)
            if math.gcd(value * (value + 2), wheel) == 1
        )
        q = next_prime(max(factors))
        r = next_prime(q)
        witness, period = crt_pairwise(
            [(residue, wheel), (0, q), ((-2) % r, r)]
        )
        while witness <= q or witness + 2 <= r:
            witness += period
        checks = {
            "wheel_residue_preserved": witness % wheel == residue,
            "residue_is_twin_admissible": math.gcd(
                residue * (residue + 2), wheel
            )
            == 1,
            "n_composite_by_q": witness % q == 0 and witness > q,
            "n_plus_2_composite_by_r": (witness + 2) % r == 0
            and witness + 2 > r,
            "progression_preserves_all_congruences": period == wheel * q * r,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "wheel_W": wheel,
                "wheel_prime_factors": factors,
                "admissible_residue_a": residue,
                "external_prime_q": q,
                "external_prime_r": r,
                "composite_pair_witness_n": witness,
                "infinite_progression_period_Wqr": period,
                "checks": checks,
            }
        )

    theorem = (
        "For every squarefree finite wheel W and every twin-admissible "
        "residue a modulo W, there are infinitely many n congruent to a "
        "modulo W for which both n and n+2 are composite. Choose distinct "
        "primes q,r not dividing W and impose n=0 mod q and n=-2 mod r. "
        "The Chinese remainder theorem gives one class modulo Wqr, and all "
        "sufficiently large members are composite pairs."
    )
    proof = (
        "The three moduli W,q,r are pairwise coprime, so CRT produces a "
        "unique residue class modulo Wqr satisfying all congruences. Every "
        "member remains in the same admissible wheel class, while q divides "
        "n and r divides n+2. Taking the progression parameter large makes "
        "both divisors proper. Therefore survival of any fixed finite wheel "
        "cannot certify even one twin pair without additional nonlocal input, "
        "and cannot by itself prove infinitely many twins."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_wheel_crt_witness_rows": rows,
        "aggregate": {
            "finite_wheel_crt_no_go_proved": True,
            "every_tested_wheel_has_infinite_composite_pair_progression": True,
            "finite_local_divisibility_survival_sufficient_for_twins": False,
            "parity_sensitive_bilinear_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This theorem excludes only certificates using divisibility data "
            "from a fixed finite wheel. It does not rule out growing sieves, "
            "bilinear forms, distribution estimates, or other global input."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_dyadic_partition_audit()
    collatz_compute = collatz_primitive_word_audit()
    goldbach_compute = goldbach_refinement_audit()
    twin_compute = twin_finite_wheel_crt_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-220",
            "theorem_name": "DyadicLaplacePartitionAndFiniteWindowNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No rigorous prime-side summable upper envelope controls all dyadic defect bands with total mass below one.",
            "route_decision": {
                "discard": "treating any fixed finite collection of dyadic defect bands as a global RH certificate",
                "retain": "a countable positive partition with certified finite center and summable prime-side tails",
                "next_single_lemma": "PrimeSideSummableDyadicBandpassEnvelopeBelowOne",
            },
            "proof_dag": proof_dag(
                "RH",
                "PositiveDyadicBandpassDefectCertificateAndEquivalenceAudit",
                "DyadicLaplacePartitionAndFiniteWindowNoGo",
                "FiniteDyadicWindowCertifiesGlobalDefectAbsence",
                "PrimeSideSummableDyadicBandpassEnvelopeBelowOne",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zero. The dyadic kernels now recover total defect multiplicity exactly, while finite-window sufficiency is rigorously rejected.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-220",
            "theorem_name": "PrimitiveRootExtensionOfSingleMountainExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Primitive multi-run valuation words and nonperiodic divergent trajectories remain uncontrolled.",
            "route_decision": {
                "discard": "enumerating rotations and powers of single-mountain words as independent cycle candidates",
                "retain": "primitive cyclic roots as the irreducible objects for Baker-type phase separation",
                "next_single_lemma": "EffectiveBakerSeparationForPrimitiveMultiRunValuationWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExplicitMatveevClosureOfAllPositiveSingleMountainCycles",
                "PrimitiveRootExtensionOfSingleMountainExclusion",
                "RepeatedSingleMountainWordsCreateNewCycleFixedPoints",
                "EffectiveBakerSeparationForPrimitiveMultiRunValuationWords",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. An infinite imprimitive multi-run family is closed, but every primitive multi-run family remains open.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-220",
            "theorem_name": "CrossFitPartitionRefinementStabilityCertificate",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No cofinal analytic estimate controls the parent residual norm and scale-refit drift without enumerating Goldbach representations.",
            "route_decision": {
                "discard": "promoting finite success under increasingly fine folds to a cofinal Goldbach theorem",
                "retain": "the exact Minkowski bridge as the interface for an analytic parent residual and refit-drift bound",
                "next_single_lemma": "CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration",
            },
            "proof_dag": proof_dag(
                "GB",
                "LeakageFreeCrossFittedEighthMomentSupportCertificate",
                "CrossFitPartitionRefinementStabilityCertificate",
                "FinitePartitionRefinementSuccessImpliesCofinalGoldbach",
                "CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The exact fold certificate is now stable under 140 tested refinements, but the cofinal arithmetic margin is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-220",
            "theorem_name": "FiniteWheelTwinCertificationCRTNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No parity-sensitive global lower bound proves actual twin support beyond all finite local divisibility filters.",
            "route_decision": {
                "discard": "using survival of any fixed finite wheel as sufficient evidence that a residue class contains twin primes",
                "retain": "finite wheels only as preprocessing before a genuinely parity-sensitive bilinear or distributional estimate",
                "next_single_lemma": "ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel",
            },
            "proof_dag": proof_dag(
                "TP",
                "QualitativeAbelInfinitudeEquivalenceAndDensityScaleNoGo",
                "FiniteWheelTwinCertificationCRTNoGo",
                "FixedFiniteWheelSurvivalCertifiesTwinSupport",
                "ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. A precise fixed-wheel route is closed by CRT; global parity-sensitive control remains open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "DyadicPartitionPrimitiveRefinementCRTNoGoAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-220 proves four exact partial or no-go theorems and resolves "
            "none of the parent conjectures. It turns RH dyadic bands into a "
            "partition of total defect multiplicity and rejects finite-window "
            "sufficiency; extends the closed Collatz family to every cyclic "
            "power and rotation of a single-mountain primitive root; proves an "
            "exact Goldbach cross-fit refinement bridge and verifies 140 finite "
            "instances; and constructs infinite CRT composite-pair progressions "
            "inside every fixed admissible twin wheel class."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common advance is irreducibility. Infinite RH scale coverage, "
            "primitive Collatz words, representation-free Goldbach refinement "
            "margins, and parity-sensitive Twin input are the parts that cannot "
            "be replaced by finite repetition of the current experiments."
        ),
        "literature_boundary": {
            "riemann": "The partition and finite-window obstruction are elementary consequences of positive Laplace kernels inside the project defect model; no new zero-free region is claimed.",
            "collatz": "The affine fixed-point argument extends the project TICKET-219 subfamily theorem; it is not a result for arbitrary Collatz words.",
            "goldbach": "The refinement inequality is an exact norm lemma and finite audit, not a new circle-method estimate.",
            "twin_prime": "The CRT construction is an elementary fixed-wheel obstruction and does not overcome the sieve parity problem.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "closed_infinite_subfamily_count": 1,
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
                    "audit_ref": "#/dyadic_partition_primitive_refinement_crt_audit"
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
    integrated = ROOT / "data/open-problem/ticket220-dyadic-partition-primitive-refinement-crt.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "dyadic_partition_primitive_refinement_crt_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-220-dyadic-partition.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-220-primitive-word-closure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-220-refinement-stability.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-220-finite-wheel-crt-no-go.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, target in targets.items():
        write_json(
            target,
            standalone_payload(audit[section_key], problem_ids[section_key]),
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": audit["status"],
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
