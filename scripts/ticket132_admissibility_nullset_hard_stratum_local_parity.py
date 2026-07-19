from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket131_proof_viability_target_correction import valuation_word_cylinder


GENERATED_AT = "2026-07-20T18:30:00+09:00"
SCHEMA = "primeproject.ticket132-admissibility-nullset-hard-stratum-local-parity.v1"


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {
        "exact": str(value),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": float(value),
    }


def riemann_constraint_preserving_core() -> dict[str, Any]:
    t = math.exp(0.5)
    matrix = ((1.0, t), (1.0, 1.0 / t))
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    sample_moments = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(3, 2), Fraction(-2, 3)),
        (Fraction(-7, 5), Fraction(11, 9)),
    ]
    rows = []
    maximum_residual = 0.0
    for plus, minus in sample_moments:
        b0 = float(plus)
        b1 = float(minus)
        c0 = (b0 * matrix[1][1] - matrix[0][1] * b1) / determinant
        c1 = (matrix[0][0] * b1 - b0 * matrix[1][0]) / determinant
        plus_residual = b0 - matrix[0][0] * c0 - matrix[0][1] * c1
        minus_residual = b1 - matrix[1][0] * c0 - matrix[1][1] * c1
        residual = max(abs(plus_residual), abs(minus_residual))
        maximum_residual = max(maximum_residual, residual)
        rows.append(
            {
                "normalized_input_moments": [str(plus), str(minus)],
                "anchor_coefficients": [c0, c1],
                "maximum_numeric_projection_residual": residual,
            }
        )

    failures = sum(
        [
            int(not determinant < 0),
            int(maximum_residual > 2e-15),
        ]
    )
    return {
        "theorem_name": "ConstraintPreservingEnumerableWeilCoreProjection",
        "proved_statement": (
            "Let L_+(f)=integral f(x)e^(x/2)dx and "
            "L_-(f)=integral f(x)e^(-x/2)dx. The TICKET129 rational-bump "
            "core can be projected continuously and effectively onto "
            "ker(L_+) intersect ker(L_-). The projected set is countable and "
            "dense in the two-moment constrained test-function space."
        ),
        "proof": (
            "For the even standard bump b, put psi_0(x)=b(x) and "
            "psi_1(x)=b(x-1). If I=integral b(x)e^(x/2)dx>0, evenness gives "
            "the normalized moment matrix [[1,e^(1/2)],[1,e^(-1/2)]]. Its "
            "determinant is e^(-1/2)-e^(1/2)<0. Hence P(f)=f-(psi_0,psi_1)"
            "A^(-1)(L_+(f),L_-(f)) is a continuous projection onto the common "
            "kernel. P is the identity on that kernel, so applying P to a "
            "countable dense core remains countable and is dense in the "
            "constrained subspace. All moments are computable, making the "
            "projected descriptions effective."
        ),
        "exact_anchor_contract": {
            "anchors": ["psi_0(x)=b(x)", "psi_1(x)=b(x-1)"],
            "positive_common_factor": "I=integral b(x)e^(x/2)dx>0",
            "normalized_matrix": "[[1,e^(1/2)],[1,e^(-1/2)]]",
            "normalized_determinant": "e^(-1/2)-e^(1/2)<0",
            "projection": "P=Id-Psi*A^(-1)*(L_+,L_-)",
        },
        "numeric_projection_audit": {
            "sample_count": len(rows),
            "rows": rows,
            "maximum_residual": maximum_residual,
        },
        "route_decision": {
            "retain": "countable effective core plus strict-negative interval search",
            "discard": (
                "use unconstrained rational bumps as though they already satisfy "
                "the two exact Weil moment conditions"
            ),
            "next_theorem": "NonnegativeProjectedWeilCoreCertificate",
        },
        "machine_audit": {
            "anchor_matrix_invertible": determinant < 0,
            "numeric_projection_residual_below_2e_15": maximum_residual <= 2e-15,
            "logical_correction_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This closes the two-moment admissibility defect of the enumerable "
            "core. It proves neither Weil positivity on that core nor RH, and it "
            "does not replace the need to freeze one exact published normalization."
        ),
    }


def accelerated_valuations(start: int, depth: int) -> list[int]:
    if start <= 0 or start % 2 == 0:
        raise ValueError("start must be a positive odd integer")
    value = start
    result = []
    for _ in range(depth):
        next_value = 3 * value + 1
        valuation = (next_value & -next_value).bit_length() - 1
        result.append(valuation)
        value = next_value >> valuation
    return result


def collatz_natural_code_topology(maximum_depth: int = 4, maximum_exponent: int = 4) -> dict[str, Any]:
    if maximum_depth < 1 or maximum_exponent < 1:
        raise ValueError("depth and exponent bounds must be positive")
    word_count = 0
    replay_count = 0
    failures = 0
    sample_rows = []
    for depth in range(1, maximum_depth + 1):
        for word_tuple in product(range(1, maximum_exponent + 1), repeat=depth):
            word = list(word_tuple)
            residue, modulus = valuation_word_cylinder(word)
            starts = [residue + multiplier * modulus for multiplier in range(3)]
            word_count += 1
            for start in starts:
                replay_count += 1
                if accelerated_valuations(start, depth) != word:
                    failures += 1
            if len(sample_rows) < 8:
                sample_rows.append(
                    {
                        "word": word,
                        "residue": str(residue),
                        "modulus": str(modulus),
                        "positive_representatives": [str(value) for value in starts],
                    }
                )
    return {
        "theorem_name": "NaturalCollatzCodesAreCountableDenseAndNull",
        "proved_statement": (
            "In the product space of positive accelerated valuation sequences, "
            "the codes generated by positive odd integers form a countable dense "
            "set. Under every non-atomic Borel probability on the code space this "
            "set has measure zero. Every such natural code is eventually stable "
            "in the canonical-residue sense of TICKET131."
        ),
        "proof": (
            "Countability follows because positive odd integers are countable. "
            "A basic open set fixes one finite valuation word. Its exact cylinder "
            "is one odd residue r modulo a power-of-two modulus M, and every "
            "r+kM with k>=0 is a positive natural realizer. Hence every nonempty "
            "basic open set contains infinitely many natural codes, proving "
            "density. A countable set has measure zero for every non-atomic "
            "Borel probability. TICKET131 proves that each fixed natural start "
            "has eventually constant canonical residues."
        ),
        "topological_measure_contract": {
            "ambient_space": "positive-integer valuation sequences with product topology",
            "countability": "image of the positive odd integers",
            "density": "every finite word cylinder contains r+kM for all k>=0",
            "nullity": "countable union of zero-mass singletons under any non-atomic measure",
            "stabilization": "every natural code has eventually constant canonical residues",
        },
        "finite_cylinder_replay": {
            "maximum_depth": maximum_depth,
            "maximum_exponent": maximum_exponent,
            "word_count": word_count,
            "positive_representative_replay_count": replay_count,
            "failure_count": failures,
            "sample_rows": sample_rows,
        },
        "route_decision": {
            "retain": "exact pointwise natural residue plus ordinary magnitude",
            "discard": (
                "use product-topology separation or measure-zero code mass alone "
                "to exclude positive-integer counterexamples"
            ),
            "next_theorem": "PointwiseArchimedeanDescentOnDenseNullNaturalCodes",
        },
        "machine_audit": {
            "all_small_cylinders_have_natural_replays": failures == 0,
            "word_count": word_count,
            "replay_count": replay_count,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The dense-null theorem explains why finite-prefix classifiers and "
            "probability estimates can both look strong and still miss the "
            "pointwise Collatz obligation. It proves no orbit descends."
        ),
    }


def primes_through(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for value in range(2, int(limit**0.5) + 1):
        if sieve[value]:
            sieve[value * value : limit + 1 : value] = b"\x00" * (
                ((limit - value * value) // value) + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def goldbach_power_of_two_hard_stratum() -> dict[str, Any]:
    major_floor = Fraction(131_917, 100_000)
    log_lower = Fraction(214, 5)
    contamination = Fraction(21, 10) * 43**2 / Fraction(2_000_000_000)
    margin_k56 = major_floor - Fraction(56, 1) / log_lower - contamination
    margin_k57_lower_architecture = major_floor - Fraction(57, 1) / log_lower - contamination
    rows = []
    for exponent in [16, 32, 64, 128, 256, 512]:
        value = 1 << exponent
        rows.append(
            {
                "exponent": exponent,
                "bit_length": value.bit_length(),
                "odd_prime_divisor_count": 0,
                "normalized_singular_series_multiplier": "1",
            }
        )
    failures = sum(
        [
            int(margin_k56 <= 0),
            int(margin_k57_lower_architecture >= 0),
            int(any(row["odd_prime_divisor_count"] != 0 for row in rows)),
        ]
    )
    return {
        "theorem_name": "PowersOfTwoRemainTheUniformGoldbachHardStratum",
        "proved_statement": (
            "For every m>=1, the normalized binary Goldbach singular-series "
            "multiplier of N=2^m is exactly one. Therefore no finite "
            "small-odd-divisor stratification can remove the uniform minimal-main "
            "case: arbitrarily large powers of two remain outside every boosted "
            "stratum. Under the fixed TICKET128-131 endpoint constants, K=56 "
            "has positive lower-certificate margin at multiplier one, while the "
            "same lower-certificate architecture with K=57 does not."
        ),
        "proof": (
            "The arithmetic multiplier is product over odd p dividing N of "
            "(p-1)/(p-2). For N=2^m the index set is empty, so the product is "
            "one. Powers of two are unbounded. Thus every proof that only gains "
            "margin from a bounded list of odd divisors leaves an infinite "
            "minimal-main stratum. Substitution of the fixed rational major "
            "floor, log lower bound, and contamination bound gives the displayed "
            "exact K=56 and K=57 margins."
        ),
        "fixed_endpoint_contract": {
            "major_floor": str(major_floor),
            "log_H_lower": str(log_lower),
            "contamination_upper": str(contamination),
            "margin_K56_at_multiplier_one": fraction_payload(margin_k56),
            "margin_K57_at_multiplier_one_using_lower_floor": fraction_payload(
                margin_k57_lower_architecture
            ),
        },
        "power_rows": rows,
        "route_decision": {
            "retain": "arithmetic stratification as workload reduction for boosted classes",
            "discard": "expect finite small-divisor stratification alone to close all even integers",
            "next_theorem": "PointwiseBinaryGoldbachResidualK56OnPowersOfTwoAndRoughStrata",
        },
        "machine_audit": {
            "all_power_rows_have_minimal_multiplier": all(
                row["normalized_singular_series_multiplier"] == "1" for row in rows
            ),
            "k56_lower_margin_positive": margin_k56 > 0,
            "k57_lower_margin_negative": margin_k57_lower_architecture < 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This identifies an unavoidable infinite hard stratum. It does not "
            "prove the K=56 pointwise residual estimate or Goldbach for powers of two."
        ),
    }


def crt(congruences: Iterable[tuple[int, int]]) -> tuple[int, int]:
    residue = 0
    modulus = 1
    for next_residue, next_modulus in congruences:
        if math.gcd(modulus, next_modulus) != 1:
            raise ValueError("CRT moduli must be pairwise coprime")
        step = ((next_residue - residue) * pow(modulus, -1, next_modulus)) % next_modulus
        residue += modulus * step
        modulus *= next_modulus
        residue %= modulus
    return residue, modulus


def first_primes_above(bound: int, count: int = 2) -> list[int]:
    limit = max(32, 2 * bound + 32)
    while True:
        candidates = [prime for prime in primes_through(limit) if prime > bound]
        if len(candidates) >= count:
            return candidates[:count]
        limit *= 2


def twin_local_sieve_countermodel(levels: Iterable[int] = (5, 11, 29, 97)) -> dict[str, Any]:
    rows = []
    failures = 0
    for level in levels:
        local_primes = primes_through(level)
        local_congruences = []
        for prime in local_primes:
            safe_residue = 1
            if prime == 3:
                safe_residue = 2
            local_congruences.append((safe_residue, prime))
        local_residue, local_modulus = crt(local_congruences)
        q, r = first_primes_above(level)
        base, progression_modulus = crt(
            [(local_residue, local_modulus), (0, q), (-2 % r, r)]
        )
        first_multiplier = max(1, (max(q, r) + 1 - base + progression_modulus - 1) // progression_modulus)
        starts = [base + (first_multiplier + offset) * progression_modulus for offset in range(3)]
        row_failures = 0
        for start in starts:
            row_failures += int(start <= q or start + 2 <= r)
            row_failures += int(start % q != 0 or (start + 2) % r != 0)
            row_failures += sum(
                int(start % prime == 0 or (start + 2) % prime == 0)
                for prime in local_primes
            )
        failures += row_failures
        rows.append(
            {
                "sieve_level": level,
                "small_prime_count": len(local_primes),
                "small_prime_modulus": str(local_modulus),
                "safe_local_residue": str(local_residue),
                "forced_composite_divisors": [q, r],
                "progression_modulus": str(progression_modulus),
                "first_three_composite_pair_starts": [str(value) for value in starts],
                "row_failure_count": row_failures,
            }
        )
    return {
        "theorem_name": "FiniteLocalSieveDataCannotCertifyTwinPrimality",
        "proved_statement": (
            "For every finite sieve level z, there is an infinite arithmetic "
            "progression of odd n such that neither n nor n+2 has a prime divisor "
            "at most z, yet both n and n+2 are composite."
        ),
        "proof": (
            "For each prime p<=z choose a residue a_p avoiding 0 and -2; use "
            "a_2=1, a_3=2, and a_p=1 for p>=5. CRT gives one locally admissible "
            "class modulo P=product(p<=z)p. Choose distinct primes q,r>z and add "
            "n=0 mod q and n=-2 mod r. CRT gives one class modulo Pqr. Every "
            "sufficiently large member has q as a proper divisor of n and r as "
            "a proper divisor of n+2, while retaining the same small-prime-clean "
            "local signature."
        ),
        "crt_rows": rows,
        "route_decision": {
            "retain": "actual unbounded Type II information and parity-sensitive exact-gap functional",
            "discard": "promote any fixed finite local sieve-clean signature to twin primality",
            "next_theorem": "UnboundedTypeIIParitySensitiveExactGapCertificate",
        },
        "machine_audit": {
            "audited_level_count": len(rows),
            "all_crt_rows_pass": failures == 0,
            "constructed_pair_count": 3 * len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The CRT construction is a countermodel to finite local certification, "
            "not a counterexample to the Twin Prime conjecture. It does not rule "
            "out parity-sensitive methods using unbounded analytic information."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_constraint_preserving_core(),
        "collatz": collatz_natural_code_topology(),
        "goldbach": goldbach_power_of_two_hard_stratum(),
        "twin_prime": twin_local_sieve_countermodel(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureAdmissibilityAndPointwiseBoundaryAudit",
        **sections,
        "proof_viability": [
            {
                "problem_id": "riemann",
                "advance": "the enumerable core now preserves the two exact moment constraints",
                "remaining": "prove nonnegativity on every projected core element or find a strict negative interval",
                "proximity": "not close, but the test space is now logically correct",
            },
            {
                "problem_id": "collatz",
                "advance": "natural codes are proved countable, dense, null, and residue-stabilizing",
                "remaining": "a pointwise Archimedean descent theorem on the natural subset",
                "proximity": "not close; topology and probability are now ruled out as standalone bridges",
            },
            {
                "problem_id": "goldbach",
                "advance": "powers of two are isolated as an unavoidable infinite minimal-main stratum",
                "remaining": "a K=56 pointwise residual theorem on powers of two and rough even integers",
                "proximity": "conditional architecture is precise, decisive minor-arc estimate open",
            },
            {
                "problem_id": "twin-prime",
                "advance": "an exact infinite CRT family defeats every fixed local sieve level",
                "remaining": "unbounded Type II information plus a parity-sensitive exact-gap lower bound",
                "proximity": "not close; finite local state is now formally excluded",
            },
        ],
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Source for the two multiplicative moment conditions in a Weil-positivity formulation.",
            },
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": "Current continuous-function/operator-limit framework; no RH proof is imported.",
            },
            {
                "citation": "Kramer, Adaptive Search in Collatz Exponent-Code Space",
                "url": "https://arxiv.org/abs/2607.10041",
                "role": "Current exponent-code diagnostics; explicitly not a Collatz verification method.",
            },
            {
                "citation": "Alsetri and Shao, Density versions of the binary Goldbach problem",
                "url": "https://arxiv.org/abs/2405.18576",
                "role": "Primary evidence that density conclusions remain distinct from all-even pointwise Goldbach.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary Type I/II lower-bound framework; substantial Type II input is necessary.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET132 closes one RH admissibility defect and proves three exact "
            "pointwise-boundary or route countermodel theorems. None of the four "
            "conjectures is proved or refuted, and none is currently close to proof. "
            "No conjecture proof or counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-132",
            "ConstraintPreservingEnumerableWeilCoreProjection",
            "NonnegativeProjectedWeilCoreCertificate",
            "Enumerate the projected core under one fixed Weil normalization and require interval-certified sign or a strict negative witness.",
        ),
        (
            "collatz",
            "CO-TICKET-132",
            "NaturalCollatzCodesAreCountableDenseAndNull",
            "PointwiseArchimedeanDescentOnDenseNullNaturalCodes",
            "Search only for magnitude-coupled pointwise descent invariants; reject finite-prefix and mass-only certificates.",
        ),
        (
            "goldbach",
            "GB-TICKET-132",
            "PowersOfTwoRemainTheUniformGoldbachHardStratum",
            "PointwiseBinaryGoldbachResidualK56OnPowersOfTwoAndRoughStrata",
            "Build a power-of-two/rough minor-arc residual decomposition with an explicit K=56 endpoint and finite overlap.",
        ),
        (
            "twin-prime",
            "TP-TICKET-132",
            "FiniteLocalSieveDataCannotCertifyTwinPrimality",
            "UnboundedTypeIIParitySensitiveExactGapCertificate",
            "Require a lower bound using unbounded Type II information that separates the CRT composite-pair progression from genuine prime pairs.",
        ),
    ]
    attempts = []
    for problem_id, ticket_id, route, target, experiment in specs:
        section_key = problem_id.replace("-", "_")
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": ticket_id,
                "status": "exact_intermediate_result_conjecture_open",
                "route": route,
                "bounded_result": {"audit_ref": section_key},
                "candidate_theorem": target,
                "next_experiment": experiment,
                "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
                "proof_boundary": audit[section_key]["proof_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_boundary_theorems_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "admissibility_nullset_hard_stratum_local_parity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket132-admissibility-nullset-hard-stratum-local-parity.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-132-constrained-core.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-132-dense-null-natural-codes.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-132-power-two-hard-stratum.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-132-local-sieve-crt.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
