from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket131_proof_viability_target_correction import valuation_word_cylinder
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    accelerated_valuations,
    crt,
    first_primes_above,
    fraction_payload,
    primes_through,
)


GENERATED_AT = "2026-07-20T23:30:00+09:00"
SCHEMA = "primeproject.ticket133-quantifier-promotion-exact-reductions.v1"


def quadratic_value(matrix: list[list[Fraction]], vector: tuple[Fraction, ...]) -> Fraction:
    return sum(
        vector[row] * matrix[row][column] * vector[column]
        for row in range(len(vector))
        for column in range(len(vector))
    )


def rational_grid(numerator_bound: int = 2, denominator_bound: int = 3) -> list[Fraction]:
    return sorted(
        {
            Fraction(numerator, denominator)
            for denominator in range(1, denominator_bound + 1)
            for numerator in range(-numerator_bound, numerator_bound + 1)
        }
    )


def riemann_projected_gram_reduction() -> dict[str, Any]:
    matrices = [
        (
            "positive_definite",
            [[Fraction(2), Fraction(-1)], [Fraction(-1), Fraction(2)]],
        ),
        (
            "positive_semidefinite_singular",
            [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]],
        ),
        (
            "indefinite",
            [[Fraction(1), Fraction(2)], [Fraction(2), Fraction(1)]],
        ),
    ]
    values = rational_grid()
    rows = []
    failures = 0
    for label, matrix in matrices:
        tested = []
        for vector in product(values, repeat=len(matrix)):
            if all(value == 0 for value in vector):
                continue
            tested.append((quadratic_value(matrix, vector), vector))
        minimum, witness = min(tested, key=lambda item: item[0])
        negative_count = sum(value < 0 for value, _ in tested)
        expected_negative = label == "indefinite"
        failures += int((negative_count > 0) != expected_negative)
        rows.append(
            {
                "label": label,
                "matrix": [[str(value) for value in row] for row in matrix],
                "rational_vectors_tested": len(tested),
                "negative_vector_count": negative_count,
                "minimum_exact_value": str(minimum),
                "minimum_witness": [str(value) for value in witness],
            }
        )

    explicit_witness = (Fraction(1), Fraction(-1))
    explicit_value = quadratic_value(matrices[-1][1], explicit_witness)
    failures += int(explicit_value != -2)
    return {
        "theorem_name": "ProjectedWeilCoreGramFamilyEquivalence",
        "proved_statement": (
            "Let K be the two-moment constrained test-function space from TICKET132, "
            "let B be a continuous symmetric Weil bilinear form on K, let Q(f)=B(f,f), "
            "and let D be the rational linear span of the projected enumerable core. "
            "Then Q is nonnegative on all of K if and only if every finite Gram "
            "matrix (B(d_i,d_j)) is nonnegative on every rational coefficient vector. "
            "If Q has a strict negative witness in K, one finite rational Gram "
            "inequality is strictly negative."
        ),
        "proof": (
            "The forward implication is immediate. Conversely, every d in D is a "
            "finite rational combination of projected core generators, so the Gram "
            "hypothesis gives Q(d)>=0. TICKET132 makes D dense in K. For any f in K, "
            "choose d_n in D converging to f; continuity gives Q(f)=lim Q(d_n)>=0. "
            "If Q(f)<0 instead, continuity makes the strict-negative set open, and "
            "density supplies d in D with Q(d)<0. Expanding d in finitely many "
            "generators gives the finite rational Gram witness."
        ),
        "exact_reduction": {
            "domain": "K=ker(L_+) intersect ker(L_-)",
            "dense_core": "D=Q-linear span of the TICKET132 projected core",
            "finite_obligations": "q^T G_m q>=0 for every m and every q in Q^m",
            "negative_witness": "one strict q^T G_m q<0 refutes universal positivity",
            "required_assumption": "continuity of the fixed normalized Weil bilinear form on K",
        },
        "finite_sanity_audit": {
            "rows": rows,
            "explicit_indefinite_witness": ["1", "-1"],
            "explicit_indefinite_value": str(explicit_value),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "countable universal Gram-family proof or strict-negative interval search",
            "discard": "treat any finite initial segment of Gram matrices as universal positivity",
            "next_theorem": "IntervalCertifiedProjectedWeilGramFamily",
        },
        "machine_audit": {
            "sanity_matrix_count": len(rows),
            "strict_negative_witness_verified": explicit_value == -2,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is an exact countable reduction of projected-core positivity. It "
            "proves none of the infinitely many Weil Gram inequalities and therefore "
            "does not prove or disprove RH."
        ),
    }


def valuation_affine_constant(word: Iterable[int]) -> tuple[int, int]:
    total_shift = 0
    constant = 0
    for exponent in word:
        constant = 3 * constant + (1 << total_shift)
        total_shift += exponent
    return total_shift, constant


def accelerated_iterate(start: int, depth: int) -> int:
    value = start
    for _ in range(depth):
        next_value = 3 * value + 1
        valuation = (next_value & -next_value).bit_length() - 1
        value = next_value >> valuation
    return value


def collatz_reaches_one(start: int, step_limit: int = 100_000) -> bool:
    value = start
    for _ in range(step_limit):
        if value == 1:
            return True
        value = value // 2 if value % 2 == 0 else 3 * value + 1
    return False


def collatz_contracting_cylinder_exclusion(
    maximum_depth: int = 5, maximum_exponent: int = 5
) -> dict[str, Any]:
    contracting_rows = []
    noncontracting_count = 0
    boundary_failures = 0
    exact_formula_failures = 0
    exception_starts: set[int] = set()
    word_count = 0
    for depth in range(1, maximum_depth + 1):
        for word_tuple in product(range(1, maximum_exponent + 1), repeat=depth):
            word = list(word_tuple)
            word_count += 1
            residue, modulus = valuation_word_cylinder(word)
            total_shift, constant = valuation_affine_constant(word)
            gap = (1 << total_shift) - 3**depth
            representative = residue
            affine_numerator = 3**depth * representative + constant
            exact_formula_failures += int(affine_numerator % (1 << total_shift) != 0)
            exact_formula_failures += int(
                accelerated_iterate(representative, depth)
                != affine_numerator // (1 << total_shift)
            )
            if gap <= 0:
                noncontracting_count += 1
                boundary_failures += int(accelerated_iterate(representative, depth) <= representative)
                continue

            threshold = constant // gap
            exception_count = (
                0
                if residue > threshold
                else ((threshold - residue) // modulus) + 1
            )
            exceptions = [residue + index * modulus for index in range(exception_count)]
            exception_starts.update(exceptions)
            for start in exceptions:
                boundary_failures += int(accelerated_valuations(start, depth) != word)
                boundary_failures += int(accelerated_iterate(start, depth) < start)
            first_descending = residue + exception_count * modulus
            boundary_failures += int(accelerated_valuations(first_descending, depth) != word)
            boundary_failures += int(accelerated_iterate(first_descending, depth) >= first_descending)
            contracting_rows.append(
                {
                    "word": word,
                    "residue": str(residue),
                    "modulus": str(modulus),
                    "total_shift": total_shift,
                    "affine_constant": str(constant),
                    "positive_gap": str(gap),
                    "non_descent_threshold": str(threshold),
                    "exact_exception_count": exception_count,
                    "first_descending_realizer": str(first_descending),
                }
            )

    termination_failures = sum(not collatz_reaches_one(start) for start in exception_starts)
    failures = exact_formula_failures + boundary_failures + termination_failures
    largest_rows = sorted(
        contracting_rows,
        key=lambda row: (row["exact_exception_count"], int(row["non_descent_threshold"])),
        reverse=True,
    )[:12]
    return {
        "theorem_name": "ContractingValuationCylinderLeastCounterexampleExclusion",
        "proved_statement": (
            "For a finite accelerated valuation word w of length k, total shift S, "
            "affine constant c, exact natural cylinder n=r+tM, and gap "
            "g=2^S-3^k>0, the k-step iterate is below n exactly when n>c/g. "
            "Consequently the cylinder has exactly max(0,floor((floor(c/g)-r)/M)+1) "
            "non-descending natural realizers. After those finitely many values are "
            "verified to terminate, no least Collatz counterexample can lie in the "
            "entire cylinder."
        ),
        "proof": (
            "Induction on the valuation word gives A^k(n)=(3^k n+c)/2^S. "
            "Thus A^k(n)<n is equivalent to c<(2^S-3^k)n. When g>0 this is "
            "exactly n>c/g. Intersecting the finite interval n<=floor(c/g) with "
            "the progression r+tM gives the displayed exact count. If a least "
            "counterexample N were a larger realizer, A^k(N)<N would contradict "
            "minimality; the explicitly checked finite exceptions terminate."
        ),
        "exact_cylinder_contract": {
            "iterate_formula": "A^k(n)=(3^k*n+c_w)/2^S",
            "contracting_condition": "g_w=2^S-3^k>0",
            "descent_condition": "n>c_w/g_w",
            "exception_count": "max(0,floor((floor(c_w/g_w)-r_w)/M_w)+1)",
            "least_counterexample_use": "contracting cylinders reduce to finite direct checks",
        },
        "finite_cylinder_audit": {
            "maximum_depth": maximum_depth,
            "maximum_exponent": maximum_exponent,
            "word_count": word_count,
            "contracting_cylinder_count": len(contracting_rows),
            "noncontracting_cylinder_count": noncontracting_count,
            "unique_exception_start_count": len(exception_starts),
            "all_unique_exceptions_terminate": termination_failures == 0,
            "largest_exception_rows": largest_rows,
            "exact_formula_failure_count": exact_formula_failures,
            "boundary_failure_count": boundary_failures,
            "termination_failure_count": termination_failures,
        },
        "route_decision": {
            "retain": "adaptive exact-cylinder cover with finite exception discharge",
            "discard": "treat a positive average valuation surplus as pointwise descent",
            "next_theorem": "PrefixFreeContractingCylinderCoverOfEveryNaturalCode",
        },
        "machine_audit": {
            "audited_word_count": word_count,
            "contracting_cylinder_count": len(contracting_rows),
            "finite_exceptions_verified": len(exception_starts),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The symbolic theorem completely handles each contracting cylinder after "
            "finite exceptions, but expanding cylinders remain and no prefix-free "
            "cover of every natural code is proved. Collatz remains open."
        ),
    }


def goldbach_power_two_sparse_spike_no_go() -> dict[str, Any]:
    margin = Fraction(23_019_645_297, 2_140_000_000_000)
    spike = -2 * margin
    rows = []
    failures = 0
    previous: dict[int, Fraction] = {}
    for exponent in [8, 12, 16, 20, 24]:
        horizon = 1 << exponent
        even_count = horizon // 2 - 1
        power_count = exponent - 1
        means = {}
        for power in [1, 2, 4]:
            mean = Fraction(power_count, even_count) * abs(spike) ** power
            means[str(power)] = fraction_payload(mean)
            if power in previous:
                failures += int(mean >= previous[power])
            previous[power] = mean
        rows.append(
            {
                "horizon": str(horizon),
                "power_of_two_exception_count": power_count,
                "even_argument_count": even_count,
                "cesaro_lp_means": means,
            }
        )
    corrected_margin = margin + spike
    failures += int(corrected_margin != -margin)
    return {
        "theorem_name": "PowerOfTwoSparseSpikesDefeatEveryFiniteCesaroLpBridge",
        "proved_statement": (
            "Let m_56=23019645297/2140000000000 be the positive TICKET132 K=56 "
            "endpoint margin, and define a normalized residual perturbation e(N) "
            "on even N by e(2^j)=-2m_56 and e(N)=0 otherwise. For every fixed "
            "finite p>0, the Cesaro L^p mean of e over even N<=X tends to zero, "
            "yet m_56+e(2^j)=-m_56<0 for every j. Thus arbitrarily strong finite-Lp "
            "average convergence alone cannot close the power-of-two Goldbach stratum."
        ),
        "proof": (
            "There are at most floor(log_2 X) powers of two and asymptotically X/2 "
            "even arguments up to X. Hence the p-th mean is at most "
            "2*log_2(X)*|2m_56|^p/(X-2), which tends to zero for every fixed finite p. "
            "At every power of two the perturbation is exactly -2m_56, so adding it "
            "to the positive endpoint margin gives -m_56."
        ),
        "exact_spike_contract": {
            "K56_margin": fraction_payload(margin),
            "power_of_two_spike": fraction_payload(spike),
            "margin_after_spike": fraction_payload(corrected_margin),
            "support": "even N that are powers of two",
            "finite_Lp_limit": "zero for every fixed 0<p<infinity",
            "pointwise_power_two_failure": "present at every 2^j",
        },
        "finite_mean_audit": {
            "powers_checked": [1, 2, 4],
            "rows": rows,
            "all_sampled_means_strictly_decrease": failures == 0,
        },
        "route_decision": {
            "retain": "pointwise or maximal residual control on powers of two and rough evens",
            "discard": "promote any collection of finite Cesaro Lp residual bounds to all-even positivity",
            "next_theorem": "HardStratumMaximalBinaryGoldbachResidualK56",
        },
        "machine_audit": {
            "audited_horizon_count": len(rows),
            "audited_Lp_exponents": 3,
            "exact_negative_power_margin_verified": corrected_margin == -margin,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The spike sequence is a countermodel to an average-to-pointwise proof "
            "inference, not the actual Goldbach residual and not a Goldbach counterexample."
        ),
    }


def admissible_residues(modulus: int, primes: Iterable[int]) -> list[int]:
    prime_list = list(primes)
    return [
        residue
        for residue in range(modulus)
        if all(residue % prime not in {0, (-2) % prime} for prime in prime_list)
    ]


def twin_all_admissible_classes_composite_lifts(
    levels: Iterable[int] = (5, 7, 11, 13)
) -> dict[str, Any]:
    rows = []
    failures = 0
    total_classes = 0
    for level in levels:
        local_primes = primes_through(level)
        modulus = math.prod(local_primes)
        residues = admissible_residues(modulus, local_primes)
        expected_count = math.prod(1 if prime == 2 else prime - 2 for prime in local_primes)
        q, r = first_primes_above(level)
        row_failures = int(len(residues) != expected_count)
        samples = []
        for residue in residues:
            base, progression_modulus = crt(
                [(residue, modulus), (0, q), (-2 % r, r)]
            )
            start = base + progression_modulus
            row_failures += int(start % modulus != residue)
            row_failures += int(start % q != 0 or (start + 2) % r != 0)
            row_failures += int(start <= q or start + 2 <= r)
            row_failures += sum(
                int(start % prime == 0 or (start + 2) % prime == 0)
                for prime in local_primes
            )
            if len(samples) < 6:
                samples.append(
                    {
                        "admissible_residue": str(residue),
                        "first_composite_pair_start": str(start),
                        "forced_divisors": [q, r],
                    }
                )
        failures += row_failures
        total_classes += len(residues)
        rows.append(
            {
                "sieve_level": level,
                "primorial_modulus": str(modulus),
                "local_prime_count": len(local_primes),
                "admissible_class_count": len(residues),
                "expected_class_count": expected_count,
                "forced_divisors": [q, r],
                "progression_modulus": str(modulus * q * r),
                "sample_lifts": samples,
                "row_failure_count": row_failures,
            }
        )
    return {
        "theorem_name": "EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts",
        "proved_statement": (
            "Fix a finite set of primes P, W=product(P), and any residue a modulo W "
            "with a and a+2 nonzero modulo every p in P. For any distinct primes "
            "q,r outside P, there is an infinite arithmetic progression of n with "
            "n=a mod W, q dividing n, and r dividing n+2. Every sufficiently large "
            "member is composite-composite while reproducing the entire prescribed "
            "admissible residue class modulo W."
        ),
        "proof": (
            "The moduli W,q,r are pairwise coprime. CRT solves n=a mod W, n=0 mod q, "
            "and n=-2 mod r in one class modulo Wqr. Every member preserves the full "
            "W-residue, hence all local admissibility data. Sufficiently large members "
            "have q and r as proper divisors of n and n+2 respectively."
        ),
        "surjective_lift_contract": {
            "source": "every admissible residue class modulo a finite primorial W",
            "target": "an infinite composite-composite progression with the same W-residue",
            "construction": "CRT(a mod W, 0 mod q, -2 mod r)",
            "classifier_consequence": "no function of n mod W alone separates prime pairs from all composites",
        },
        "all_class_audit": {
            "rows": rows,
            "audited_level_count": len(rows),
            "total_admissible_classes_lifted": total_classes,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "unbounded Type II or other global parity-sensitive information",
            "discard": "any exact-gap classifier that factors through one fixed finite residue modulus",
            "next_theorem": "UnboundedParitySensitiveTwinPairSeparation",
        },
        "machine_audit": {
            "audited_level_count": len(rows),
            "admissible_class_count": total_classes,
            "all_classes_have_composite_lifts": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This strengthens TICKET132 from one clean signature to every admissible "
            "finite residue class. It is not a counterexample to Twin Prime and does "
            "not address methods whose information grows unboundedly with scale."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_projected_gram_reduction(),
        "collatz": collatz_contracting_cylinder_exclusion(),
        "goldbach": goldbach_power_two_sparse_spike_no_go(),
        "twin_prime": twin_all_admissible_classes_composite_lifts(),
    }
    failures = sum(section["machine_audit"]["total_failure_count"] for section in sections.values())
    return {
        "theorem_name": "FourConjectureQuantifierPromotionExactReductionAudit",
        **sections,
        "cross_problem_theorem": {
            "name": "FiniteInformationPromotionRequiresProblemSpecificUniformControl",
            "statement": (
                "The four exact reductions isolate four noninterchangeable universal "
                "obligations: all projected Weil Gram inequalities, an adaptive "
                "contracting-cylinder cover, a hard-stratum maximal Goldbach bound, "
                "and Twin information not factoring through a fixed residue modulus."
            ),
            "transfer_rule": (
                "Compactness, density, or average convergence may organize a proof, "
                "but each target still needs its named pointwise or universal control."
            ),
        },
        "proof_viability": [
            {
                "problem_id": "riemann",
                "advance": "projected-core positivity is reduced exactly to a countable universal Gram family",
                "remaining": "certify every member of that infinite family or find one strict negative interval",
                "proximity": "not close; the universal quantifier is now exact rather than finite-dimensional",
            },
            {
                "problem_id": "collatz",
                "advance": "every contracting valuation cylinder reduces to an exact finite exception set",
                "remaining": "a prefix-free adaptive contracting cover of every natural code",
                "proximity": "not close, but the pointwise Archimedean obligation is localized",
            },
            {
                "problem_id": "goldbach",
                "advance": "a sparse exact countermodel rules out all finite-Lp average-to-pointwise promotions",
                "remaining": "a maximal K=56 residual bound on powers of two and rough evens",
                "proximity": "conditional architecture remains the most explicit; decisive pointwise bound open",
            },
            {
                "problem_id": "twin-prime",
                "advance": "every admissible finite residue class has infinite composite-pair lifts",
                "remaining": "unbounded parity-sensitive separation and positive exact-gap lower bound",
                "proximity": "not close; every fixed-modulus classifier is now excluded",
            },
        ],
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Weil positivity and its two moment constraints; no RH proof is imported.",
            },
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": "Current continuous-form and operator-limit setting; the proposed limit remains open.",
            },
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map",
                "url": "https://doi.org/10.4153/CJM-1996-060-x",
                "role": "Finite symbolic coding context; no all-natural descent theorem is imported.",
            },
            {
                "citation": "Alsetri and Shao, Density versions of the binary Goldbach problem",
                "url": "https://arxiv.org/abs/2405.18576",
                "role": "Density results are kept separate from the all-even pointwise target.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Type I/II lower-bound context; no exact-gap parity bridge is imported.",
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
            "TICKET133 proves four exact reduction, finite-exception, or countermodel "
            "theorems. None proves or refutes RH, Collatz, Goldbach, or Twin Prime; "
            "all four conjecture-resolution counters remain zero. No conjecture proof "
            "or counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-133",
            "ProjectedWeilCoreGramFamilyEquivalence",
            "IntervalCertifiedProjectedWeilGramFamily",
            "Freeze one published Weil normalization and interval-certify Gram entries while dovetailing strict-negative witnesses.",
        ),
        (
            "collatz",
            "CO-TICKET-133",
            "ContractingValuationCylinderLeastCounterexampleExclusion",
            "PrefixFreeContractingCylinderCoverOfEveryNaturalCode",
            "Extend only noncontracting cylinders and search for a prefix-free cover whose finite exception sets terminate.",
        ),
        (
            "goldbach",
            "GB-TICKET-133",
            "PowerOfTwoSparseSpikesDefeatEveryFiniteCesaroLpBridge",
            "HardStratumMaximalBinaryGoldbachResidualK56",
            "Replace average residual control by a supremum or maximal inequality on powers of two and rough even integers.",
        ),
        (
            "twin-prime",
            "TP-TICKET-133",
            "EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts",
            "UnboundedParitySensitiveTwinPairSeparation",
            "Require scale-growing Type II information that distinguishes every CRT composite lift from genuine prime pairs.",
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
        "status": "exact_quantifier_reductions_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "quantifier_promotion_exact_reduction_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket133-quantifier-promotion-exact-reductions.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-133-gram-family-reduction.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-133-contracting-cylinder-exceptions.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-133-power-two-spike-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-133-all-residue-composite-lifts.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
