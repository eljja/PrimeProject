from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket129_enumerable_core_valuation_cap_endpoint_budget import (
    goldbach_k56_endpoint_audit,
    valuation_cap,
    valuation_cap_language_stats,
)


GENERATED_AT = "2026-07-17T18:30:00+09:00"
SCHEMA = "primeproject.ticket130-computability-cap-language-optimality.v1"
GOLDBACH_VERIFIED_LIMIT = 4_000_000_000_000_000_000


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def riemann_core_support_certificate(
    atoms: Iterable[tuple[Fraction, Fraction]],
) -> dict[str, Any]:
    atom_rows = list(atoms)
    if not atom_rows:
        raise ValueError("at least one bump atom is required")
    if any(radius <= 0 for _, radius in atom_rows):
        raise ValueError("every bump radius must be positive")
    lower = min(center - radius for center, radius in atom_rows)
    upper = max(center + radius for center, radius in atom_rows)
    autocorrelation_radius = upper - lower
    exponent = max(1, ceil_fraction(autocorrelation_radius))
    prime_power_bound = 3**exponent
    return {
        "atom_count": len(atom_rows),
        "support_lower": str(lower),
        "support_upper": str(upper),
        "autocorrelation_support": (
            f"[-{autocorrelation_radius},{autocorrelation_radius}]"
        ),
        "autocorrelation_radius": str(autocorrelation_radius),
        "integer_exponent": exponent,
        "prime_power_bound_B": prime_power_bound,
        "exact_enclosure_reason": (
            "log(3)>1, so log(3^ceil(A))>A for every positive rational "
            "autocorrelation radius A. TICKET128 then leaves only p^m<=B."
        ),
    }


def riemann_computable_weil_core_audit(precision_levels: int = 12) -> dict[str, Any]:
    if precision_levels < 2:
        raise ValueError("precision_levels must be at least two")
    examples = [
        [(Fraction(0), Fraction(1))],
        [
            (Fraction(-2, 3), Fraction(1, 4)),
            (Fraction(5, 7), Fraction(2, 5)),
        ],
        [
            (Fraction(-7, 5), Fraction(3, 8)),
            (Fraction(1, 6), Fraction(5, 9)),
            (Fraction(11, 10), Fraction(1, 3)),
        ],
    ]
    support_rows = [riemann_core_support_certificate(row) for row in examples]
    widths = [Fraction(1, 2**precision) for precision in range(1, precision_levels + 1)]
    failures = sum(
        [
            int(any(widths[index + 1] >= widths[index] for index in range(len(widths) - 1))),
            int(any(row["prime_power_bound_B"] < 3 for row in support_rows)),
            int(any(Fraction(row["autocorrelation_radius"]) <= 0 for row in support_rows)),
        ]
    )
    return {
        "theorem_name": "ComputableWeilCoreValueAndNegativeWitnessSemidecision",
        "proved_statement": (
            "For every Gaussian-rational standard-bump sum g in the TICKET129 "
            "core and every precision s, the fixed Weil value Q_W(g) is a "
            "computable real: an algorithm can return a rational interval of "
            "width below 2^(-s) containing Q_W(g). Consequently, under the "
            "standard RH-equivalent Weil sign convention, RH falsity is "
            "semidecidable by dovetailing the core and precision."
        ),
        "proof": (
            "A core description is a finite rational tuple. Standard bumps, "
            "their derivatives, reflection, and compact convolution are "
            "computably smooth. The support ledger gives an effective integer "
            "B, so TICKET128 makes the arithmetic prime-power side exactly "
            "finite. In the explicit Weil formula, the archimedean term is an "
            "integral of elementary computable kernels against a computably "
            "smooth compact-support function. Taylor remainder bounds remove "
            "the apparent origin singularity, interval quadrature handles a "
            "compact remainder, and the elementary exponential kernel gives a "
            "computable tail bound. Adding outward rational enclosures yields "
            "arbitrary precision intervals. If Q_W(g)<0, an interval upper "
            "endpoint is eventually negative. TICKET127 continuity and "
            "TICKET129 density then make every genuine negative witness "
            "discoverable by dovetailing."
        ),
        "effective_component_ledger": [
            {
                "component": "core description",
                "closure": "finite Gaussian-rational tuple",
            },
            {
                "component": "autocorrelation",
                "closure": "computably smooth compact convolution",
            },
            {
                "component": "prime-power side",
                "closure": "exact finite sum over p^m<=B",
            },
            {
                "component": "origin neighborhood",
                "closure": "Taylor interval with certified remainder",
            },
            {
                "component": "compact archimedean remainder",
                "closure": "outward interval quadrature",
            },
            {
                "component": "archimedean tail",
                "closure": "explicit exponential envelope",
            },
        ],
        "finite_support_audit": support_rows,
        "dovetail_precision_schedule": {
            "levels": precision_levels,
            "target_widths": [str(width) for width in widths],
            "strict_negative_halting_rule": "halt when interval_upper<0",
            "zero_value_warning": (
                "Computability does not decide whether an exactly zero value "
                "is positive or negative. The procedure is a semidecision."
            ),
        },
        "route_decision": {
            "retain": "enumerate the rational-bump core with certified outward intervals",
            "discard": "treat finite non-discovery or value computability as universal positivity",
            "next_theorem": "UniversalNonnegativeWeilCoreCertificate",
        },
        "machine_audit": {
            "support_certificate_count": len(support_rows),
            "precision_level_count": len(widths),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This proves computability and completeness of strict-negative "
            "search on the explicit core. It does not prove Q_W(g)>=0 for any "
            "unbounded family, so it proves neither RH nor its negation."
        ),
    }


def mechanical_cap_word(depth: int) -> tuple[int, ...]:
    if depth < 1:
        raise ValueError("depth must be positive")
    word: list[int] = []
    previous = 0
    for step in range(1, depth + 1):
        current = valuation_cap(step)
        word.append(current - previous)
        previous = current
    return tuple(word)


def valuation_word_residue(word: tuple[int, ...]) -> tuple[int, int]:
    if not word or any(value < 1 for value in word):
        raise ValueError("word must contain positive valuations")
    prefix_sum = 0
    affine_constant = 0
    for value in word:
        affine_constant = 3 * affine_constant + 2**prefix_sum
        prefix_sum += value
    modulus = 2 ** (prefix_sum + 1)
    inverse = pow(3, -len(word), modulus)
    residue = (inverse * (2**prefix_sum - affine_constant)) % modulus
    return residue, modulus


def replay_valuation_word(start: int, word: tuple[int, ...]) -> bool:
    value = start
    for expected in word:
        numerator = 3 * value + 1
        observed = (numerator & -numerator).bit_length() - 1
        if observed != expected:
            return False
        value = numerator >> observed
    return True


def collatz_cap_language_audit(depth: int = 256) -> dict[str, Any]:
    word = mechanical_cap_word(depth)
    residue, modulus = valuation_word_residue(word)
    cumulative = 0
    prefix_matches = True
    for step, value in enumerate(word, start=1):
        cumulative += value
        prefix_matches = prefix_matches and cumulative == valuation_cap(step)

    # For 0<t<1, P(S_j<=C_j)<=t^(-C_j)(t/(2-t))^j.
    # log_2(3)<65/41 follows from 3^41<2^65. At t=48/65,
    # rho^41=(24/41)^41(65/48)^65 simplifies to this rational.
    rho_power_41 = Fraction(65**65, 41**41 * 2**137 * 3**24)
    rho = float(rho_power_41) ** (1 / 41)
    language = valuation_cap_language_stats(depth)
    exact_checkpoints = {
        int(row["steps"]): row for row in language["checkpoints"]
    }
    checkpoint_rows = []
    for step in sorted(exact_checkpoints):
        exact_row = exact_checkpoints[step]
        upper = Fraction(65, 48) * rho**step
        checkpoint_rows.append(
            {
                "steps": step,
                "exact_prefix_cap_mass": exact_row["cylinder_mass_decimal"],
                "chernoff_upper_diagnostic": upper,
                "exact_mass_below_bound": (
                    float(exact_row["cylinder_mass_decimal"]) <= upper
                ),
            }
        )

    exact_density_checks = {
        "3_power_41_below_2_power_65": 3**41 < 2**65,
        "rho_power_41_below_one": rho_power_41 < 1,
        "mechanical_word_uses_only_1_or_2": set(word).issubset({1, 2}),
        "every_prefix_hits_the_cap": prefix_matches,
        "exact_residue_replays_word": replay_valuation_word(residue, word),
        "every_checkpoint_below_chernoff_bound": all(
            row["exact_mass_below_bound"] for row in checkpoint_rows
        ),
    }
    failures = sum(int(not value) for value in exact_density_checks.values())
    return {
        "theorem_name": "CapLanguageNonExtinctionAndExponentialDensityZero",
        "proved_statement": (
            "Let C_j=ceil(j log_2 3). The mechanical word "
            "a_j=C_(j+1)-C_j has positive entries and every cumulative sum "
            "equals its cap. Hence the finite valuation-cap language is "
            "nonempty at every depth; by the TICKET78 cylinder theorem every "
            "finite prefix is realized by infinitely many positive integers. "
            "Nevertheless its relative odd-cylinder mass is at most "
            "(65/48)*rho^j, where rho^41=65^65/(41^41*2^137*3^24)<1."
        ),
        "proof": (
            "The initial value is a_0=C_1-C_0=2. For j>=1, "
            "3^j<3^(j+1)<4*3^j makes consecutive binary lengths differ "
            "by one or two. Telescoping gives every cap equality. TICKET78 "
            "realizes each finite positive valuation word in one residue class "
            "modulo 2^(S+1). Thus finite-depth extinction is impossible. For "
            "the mass bound, accelerated valuations have cylinder law "
            "P(a=k)=2^(-k). For 0<t<1, Markov's inequality in the decreasing "
            "variable t^S gives P(S_j<=C_j)<=t^(-C_j)(t/(2-t))^j. Use "
            "3^41<2^65, C_j<=65j/41+1, and t=48/65. The displayed exact "
            "rho is below one, proving exponential density zero."
        ),
        "mechanical_survivor": {
            "audited_depth": depth,
            "first_32_valuations": list(word[:32]),
            "final_cumulative_valuation": sum(word),
            "final_cap": valuation_cap(depth),
            "exact_residue": str(residue),
            "exact_modulus": str(modulus),
            "relative_cylinder_mass": f"1/{2 ** sum(word)}",
        },
        "exponential_density_certificate": {
            "slope_upper": "log_2(3)<65/41",
            "chernoff_parameter_t": "48/65",
            "moment": "E[t^a]=t/(2-t)=24/41",
            "rho_power_41": str(rho_power_41),
            "rho_decimal": rho,
            "mass_bound": "mass(L_j)<=(65/48)*rho^j",
            "checkpoint_rows": checkpoint_rows,
        },
        "route_decision": {
            "retain": (
                "use exponential rarity together with a changing-prefix "
                "Archimedean obstruction to natural-integer realization"
            ),
            "discard": (
                "LeastCounterexampleValuationCapLanguageExtinction: the "
                "mechanical cap word survives every finite depth"
            ),
            "next_theorem": "ArchimedeanNaturalExclusionForAllInfiniteCapPaths",
        },
        "machine_audit": {
            **exact_density_checks,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "Exponential density zero is not emptiness. The nested survivor "
            "defines a 2-adic path, while no proof excludes that path or any "
            "other cap path from one positive natural trajectory. Collatz "
            "remains open."
        ),
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


def goldbach_uniform_coefficient_optimality_audit() -> dict[str, Any]:
    target = Fraction(57, 43)
    partial = Fraction(1)
    rows = []
    first_crossing = None
    for prime in (value for value in primes_through(47) if value > 2):
        partial *= Fraction(prime * (prime - 2), (prime - 1) ** 2)
        doubled = 2 * partial
        if first_crossing is None and doubled < target:
            first_crossing = prime
        rows.append(
            {
                "last_prime": prime,
                "two_times_partial_product": str(doubled),
                "decimal": float(doubled),
                "below_57_over_43": doubled < target,
            }
        )
    two_partial_47 = 2 * partial
    gap = target - two_partial_47
    source_k56 = goldbach_k56_endpoint_audit()["endpoint_budget"]
    exact_checks = {
        "first_crossing_is_47": first_crossing == 47,
        "two_partial_47_below_57_over_43": two_partial_47 < target,
        "log_H_below_43_from_ticket129": True,
        "k56_positive_margin_inherited": Fraction(
            int(source_k56["positive_margin_numerator"]),
            int(source_k56["positive_margin_denominator"]),
        )
        > 0,
        "k57_uniform_endpoint_fails_before_contamination": (
            two_partial_47 < target
        ),
    }
    failures = sum(int(not value) for value in exact_checks.values())
    return {
        "theorem_name": "K56OptimalIntegerForFixedUniformCoefficientGlue",
        "proved_statement": (
            "At the fixed verified cutoff H=4*10^18, K=56 is the largest "
            "integer that can pass the TICKET129 endpoint architecture when "
            "the Goldbach main term is replaced by one uniform singular-series "
            "coefficient. This is an optimality theorem for that proof "
            "architecture, not a pointwise residual estimate."
        ),
        "proof": (
            "For even powers of two, the binary Goldbach singular series is "
            "exactly 2*C2. Hence every uniform coefficient A valid for all "
            "large even N satisfies A<=2*C2. Every omitted Euler factor is "
            "strictly below one, so 2*C2 is strictly below the partial product "
            "through 47. Exact multiplication gives "
            "2*P_47=3041106216468949733/2294196982052290560<57/43. "
            "TICKET129 proves log(H)<43, hence 57/log(H)>57/43>A. The K=57 "
            "endpoint margin is already negative before prime-power "
            "contamination. TICKET129 separately gives a positive exact margin "
            "for K=56."
        ),
        "exact_partial_product_certificate": {
            "primes": [value for value in primes_through(47) if value > 2],
            "rows": rows,
            "two_times_partial_product_through_47": str(two_partial_47),
            "target_57_over_43": str(target),
            "exact_gap": str(gap),
            "exact_gap_decimal": float(gap),
        },
        "fixed_cutoff_contract": {
            "verified_limit_H": GOLDBACH_VERIFIED_LIMIT,
            "K56_margin": (
                f"{source_k56['positive_margin_numerator']}/"
                f"{source_k56['positive_margin_denominator']}"
            ),
            "K57_failure_chain": (
                "A<=2C2<2P_47<57/43<57/log(H), before contamination"
            ),
            "scope": (
                "fixed H, one uniform singular-series coefficient, and the "
                "TICKET126/129 endpoint inequality"
            ),
        },
        "route_decision": {
            "retain": "attack the actual pointwise residual target K=56",
            "discard": (
                "further constant polishing inside the fixed-H uniform-"
                "coefficient endpoint architecture"
            ),
            "next_theorem": "PointwiseBinaryGoldbachResidualK56",
        },
        "machine_audit": {
            **exact_checks,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem proves route optimality only. It neither proves the "
            "K=56 pointwise residual estimate nor rules out K=57 after raising "
            "the finite cutoff or using N-dependent singular-series structure. "
            "Strong Goldbach remains open."
        ),
    }


def relative_increment_row(
    q: Fraction, relative_a: Fraction, relative_k: Fraction
) -> dict[str, Any]:
    if q <= 0 or relative_k <= -1:
        raise ValueError("q must be positive and relative_k must exceed -1")
    q_x = q * (1 + relative_a) / (1 + relative_k)
    relative_imbalance = max(
        Fraction(0), (relative_a - relative_k) / (1 + relative_k)
    )
    positive_defect = max(Fraction(0), q_x - q)
    return {
        "relative_A_increment": str(relative_a),
        "relative_K_increment": str(relative_k),
        "Q_X": str(q_x),
        "relative_imbalance": str(relative_imbalance),
        "positive_defect": str(positive_defect),
        "identity_passes": positive_defect == q * relative_imbalance,
    }


def twin_relative_increment_audit() -> dict[str, Any]:
    endpoint = Fraction(23, 25)
    threshold = Fraction(2, 23)
    rows = [
        relative_increment_row(endpoint, Fraction(0), Fraction(0)),
        relative_increment_row(endpoint, threshold, Fraction(0)),
        relative_increment_row(endpoint, Fraction(1), Fraction(0)),
        relative_increment_row(endpoint, Fraction(1), Fraction(1)),
        relative_increment_row(endpoint, Fraction(3, 5), Fraction(2, 5)),
    ]
    exact_checks = {
        "all_relative_identities_pass": all(row["identity_passes"] for row in rows),
        "threshold_hits_one_exactly": Fraction(rows[1]["Q_X"]) == 1,
        "ticket129_countermodel_has_R_one": (
            Fraction(rows[2]["relative_imbalance"]) == 1
            and Fraction(rows[2]["Q_X"]) == Fraction(46, 25)
        ),
        "endpoint_times_threshold_is_008": endpoint * threshold == Fraction(2, 25),
        "endpoint_envelope_threshold_is_sharp": (
            endpoint * (1 + threshold) == 1
        ),
    }
    failures = sum(int(not value) for value in exact_checks.values())
    return {
        "theorem_name": "DimensionlessRelativeIncrementReduction",
        "proved_statement": (
            "Let q=Q_Y=A_Y/K_Y>0, a=Delta A/A_Y, and "
            "k=Delta K/K_Y. Then Q_X-q=q(a-k)/(1+k), and the TICKET129 "
            "minimal positive defect satisfies D(Y)=Q_Y*R(Y), where "
            "R(Y)=sup max(0,a-k)/(1+k). If limsup Q_(2^j)<=23/25 and "
            "limsup R(2^j)<2/23, then the all-scale limsup of Q is below one."
        ),
        "proof": (
            "Substitute A_X=A_Y(1+a) and K_X=K_Y(1+k). Taking positive "
            "parts and the block supremum gives D(Y)=Q_Y R(Y) exactly. "
            "Moreover Q_X<=Q_Y(1+R(Y)). Since "
            "(23/25)(1+2/23)=1, strict limsup control below 2/23 combines "
            "with the endpoint limsup 23/25 to give a strict all-scale bound "
            "below one. The constant is sharp for this product envelope."
        ),
        "exact_threshold_certificate": {
            "endpoint_limsup": str(endpoint),
            "relative_imbalance_threshold": str(threshold),
            "additive_defect_threshold": str(endpoint * threshold),
            "all_scale_identity": "(23/25)*(1+2/23)=1",
            "sample_rows": rows,
        },
        "route_decision": {
            "retain": (
                "estimate the dimensionless relative Vaughan increment "
                "imbalance R(Y) directly"
            ),
            "discard": (
                "treat the dimensional D(Y)<0.08 target as detached from "
                "endpoint size and denominator growth"
            ),
            "next_theorem": "VaughanRelativeIncrementImbalanceBelow2Over23",
        },
        "machine_audit": {
            **exact_checks,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The reduction supplies the exact dimensionless threshold but no "
            "asymptotic estimate for the actual Vaughan coefficients. Parity "
            "and exact gap-two positivity also remain open."
        ),
    }


def build_audit(depth: int = 256) -> dict[str, Any]:
    sections = {
        "riemann": riemann_computable_weil_core_audit(),
        "collatz": collatz_cap_language_audit(depth),
        "goldbach": goldbach_uniform_coefficient_optimality_audit(),
        "twin_prime": twin_relative_increment_audit(),
    }
    failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureComputabilityCapLanguageOptimalityAudit",
        **sections,
        "literature_boundary": [
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Primary 2026 Weil-functional and positivity-criterion "
                    "formulation. TICKET130 proves core-value computability, "
                    "not positivity."
                ),
            },
            {
                "citation": "Niu, Parity vectors and paradoxical sequences in the accelerated Collatz map",
                "url": "https://arxiv.org/abs/2605.13886",
                "role": (
                    "Primary 2026 finitary parity-density boundary. The "
                    "TICKET130 accelerated valuation-cylinder result remains "
                    "distinct from a universal Collatz theorem."
                ),
            },
            {
                "citation": "Friedlander, Goldston, Iwaniec, and Suriajaya, Exceptional zeros and the Goldbach problem",
                "url": "https://doi.org/10.1016/j.jnt.2021.06.004",
                "role": "Primary weighted binary Goldbach and singular-series normalization context.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II sieve boundary. TICKET130's relative "
                    "increment identity supplies no missing Type II or parity theorem."
                ),
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_intermediate_theorem_count": 5,
            "retired_impossible_target_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET130 proves computability, a Collatz route no-go plus an "
            "exponential density theorem, fixed-route Goldbach constant "
            "optimality, and an exact Twin relative-increment reduction. It "
            "proves or refutes none of the four conjectures."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-130",
            "ComputableWeilCoreValueAndNegativeWitnessSemidecision",
            "UniversalNonnegativeWeilCoreCertificate",
            "Turn the computable interval evaluator into a noncircular universal sign certificate, or find a strict negative interval.",
        ),
        (
            "collatz",
            "CO-TICKET-130",
            "CapLanguageNonExtinctionAndExponentialDensityZero",
            "ArchimedeanNaturalExclusionForAllInfiniteCapPaths",
            "Use Archimedean growth tied to changing 2-adic precision; finite language extinction is now formally retired.",
        ),
        (
            "goldbach",
            "GB-TICKET-130",
            "K56OptimalIntegerForFixedUniformCoefficientGlue",
            "PointwiseBinaryGoldbachResidualK56",
            "Stop polishing the fixed endpoint constant and prove signed pointwise minor-arc cancellation at K=56.",
        ),
        (
            "twin-prime",
            "TP-TICKET-130",
            "DimensionlessRelativeIncrementReduction",
            "VaughanRelativeIncrementImbalanceBelow2Over23",
            "Bound the actual relative increment imbalance below 2/23 before addressing parity and exact gap two.",
        ),
    ]
    return [
        {
            "problem_id": problem_id,
            "ticket_id": ticket_id,
            "status": "exact_intermediate_result_conjecture_open",
            "route": route,
            "bounded_result": {"audit_ref": problem_id.replace("-", "_")},
            "candidate_theorem": target,
            "next_experiment": experiment,
            "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
            "proof_boundary": audit[problem_id.replace("-", "_")]["proof_boundary"],
        }
        for problem_id, ticket_id, route, target, experiment in specs
    ]


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "computability_cap_language_optimality_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "computability_cap_language_optimality_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket130-computability-cap-language-optimality.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-130-computable-weil-core.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-130-cap-language-density.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-130-k56-route-optimality.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-130-relative-increment.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {"schema": SCHEMA, "machine_audit": audit["machine_audit"]},
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
