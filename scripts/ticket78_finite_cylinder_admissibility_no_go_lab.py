from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterator

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-11T04:10:00+09:00"
SCHEMA = "primeproject.ticket78-finite-cylinder-admissibility-no-go-lab.v1"
MAX_TOTAL_VALUATION = 16
SHIFTED_REPRESENTATIVES_PER_WORD = 4
EXAMPLE_TOTALS = {1, 4, 8, 12, 16}
EXAMPLE_LIMIT = 12


def compositions(total: int) -> Iterator[tuple[int, ...]]:
    if total <= 0:
        raise ValueError("total must be positive")
    for mask in range(1 << (total - 1)):
        word: list[int] = []
        previous = 0
        for offset in range(total - 1):
            if (mask >> offset) & 1:
                word.append(offset + 1 - previous)
                previous = offset + 1
        word.append(total - previous)
        yield tuple(word)


def affine_constant(word: tuple[int, ...]) -> tuple[int, int]:
    consumed = 0
    constant = 0
    for valuation in word:
        constant = 3 * constant + (1 << consumed)
        consumed += valuation
    return consumed, constant


def valuation_word_residue(word: tuple[int, ...]) -> dict[str, int]:
    consumed, constant = affine_constant(word)
    modulus = 1 << (consumed + 1)
    power_of_three = 3 ** len(word)
    residue = ((1 << consumed) - constant) * pow(power_of_three, -1, modulus) % modulus
    return {
        "consumed_bits": consumed,
        "affine_constant": constant,
        "power_of_three": power_of_three,
        "modulus": modulus,
        "residue": residue,
    }


def replay_word(start: int, word: tuple[int, ...]) -> dict[str, Any]:
    current = start
    observed: list[int] = []
    for _ in word:
        valuation = v2(3 * current + 1)
        observed.append(valuation)
        current = (3 * current + 1) >> valuation
    consumed, constant = affine_constant(word)
    affine_numerator = (3 ** len(word)) * start + constant
    return {
        "observed_word": tuple(observed),
        "terminal": current,
        "affine_terminal": affine_numerator >> consumed,
        "affine_divisible": affine_numerator % (1 << consumed) == 0,
    }


def audit_valuation_cylinders() -> dict[str, Any]:
    total_word_count = 0
    total_representative_count = 0
    residue_collision_count = 0
    formula_failure_count = 0
    representative_failure_count = 0
    count_identity_failure_count = 0
    per_total: list[dict[str, Any]] = []
    examples: list[dict[str, Any]] = []

    for total in range(1, MAX_TOTAL_VALUATION + 1):
        profiles: dict[int, list[tuple[int, ...]]] = defaultdict(list)
        word_count = 0
        representative_count = 0
        total_formula_failures = 0
        total_representative_failures = 0

        for word in compositions(total):
            word_count += 1
            total_word_count += 1
            cylinder = valuation_word_residue(word)
            residue = int(cylinder["residue"])
            modulus = int(cylinder["modulus"])
            profiles[residue].append(word)
            formula_holds = residue % 2 == 1 and 0 < residue < modulus
            if not formula_holds:
                formula_failure_count += 1
                total_formula_failures += 1

            witness_rows = []
            for shift in range(SHIFTED_REPRESENTATIVES_PER_WORD):
                representative = residue + shift * modulus
                replay = replay_word(representative, word)
                representative_count += 1
                total_representative_count += 1
                replay_holds = (
                    replay["observed_word"] == word
                    and replay["terminal"] == replay["affine_terminal"]
                    and replay["affine_divisible"]
                )
                if not replay_holds:
                    representative_failure_count += 1
                    total_representative_failures += 1
                if total in EXAMPLE_TOTALS and len(examples) < EXAMPLE_LIMIT and shift < 2:
                    witness_rows.append(
                        {
                            "shift": shift,
                            "positive_integer": representative,
                            "terminal": int(replay["terminal"]),
                            "replay_holds": replay_holds,
                        }
                    )
            if witness_rows and len(examples) < EXAMPLE_LIMIT:
                examples.append(
                    {
                        "valuation_word": list(word),
                        "total_valuation": total,
                        "modulus": modulus,
                        "residue": residue,
                        "positive_integer_witnesses": witness_rows,
                    }
                )

        collision_count = sum(1 for words in profiles.values() if len(words) > 1)
        residue_collision_count += collision_count
        expected_word_count = 1 << (total - 1)
        count_identity_holds = word_count == expected_word_count and len(profiles) == expected_word_count
        if not count_identity_holds:
            count_identity_failure_count += 1
        per_total.append(
            {
                "total_valuation": total,
                "word_count": word_count,
                "expected_composition_count": expected_word_count,
                "unique_residue_count": len(profiles),
                "residue_collision_count": collision_count,
                "shifted_positive_representative_count": representative_count,
                "formula_failure_count": total_formula_failures,
                "representative_replay_failure_count": total_representative_failures,
                "count_identity_holds": count_identity_holds,
            }
        )

    return {
        "max_total_valuation": MAX_TOTAL_VALUATION,
        "total_word_count": total_word_count,
        "expected_total_word_count": (1 << MAX_TOTAL_VALUATION) - 1,
        "shifted_representatives_per_word": SHIFTED_REPRESENTATIVES_PER_WORD,
        "total_positive_representative_count": total_representative_count,
        "residue_collision_count": residue_collision_count,
        "formula_failure_count": formula_failure_count,
        "representative_replay_failure_count": representative_failure_count,
        "count_identity_failure_count": count_identity_failure_count,
        "per_total_valuation": per_total,
        "examples": examples,
    }


def analyze_finite_cylinder_no_go() -> dict[str, Any]:
    audit = audit_valuation_cylinders()
    computational_failures = (
        int(audit["residue_collision_count"])
        + int(audit["formula_failure_count"])
        + int(audit["representative_replay_failure_count"])
        + int(audit["count_identity_failure_count"])
    )
    status = (
        "finite_two_adic_natural_separator_refuted_exactly_no_collatz_resolution"
        if computational_failures == 0
        else "finite_cylinder_admissibility_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "FiniteValuationCylinderNaturalDensityNoGo",
        "source_ticket": "CO-TICKET-77",
        "source_status": "fixed_prefix_boundary_orbit_classified_no_collatz_resolution",
        "literature_context": [
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996), 1154-1169",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Primary source for the 2-adic shift conjugacy; TICKET78 does not claim to rediscover it.",
            },
            {
                "citation": "Rozier, Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding, INTEGERS 19 (2019)",
                "url": "https://arxiv.org/abs/1805.00133",
                "role": "Primary parity-sequence context and inverse-transform formulas.",
            },
        ],
        "exact_cylinder_formula": {
            "word": "a=(a_1,...,a_m), every a_i>=1",
            "total": "S=sum_i a_i",
            "affine_constant_recurrence": "C_0=0; C_(j+1)=3*C_j+2^(a_1+...+a_j)",
            "accelerated_iterate": "T^m(n)=(3^m*n+C_m)/2^S",
            "unique_residue": "r_a = 3^(-m)*(2^S-C_m) mod 2^(S+1)",
            "cylinder": "n = r_a + q*2^(S+1), q>=0",
        },
        "proof_chain": [
            "The displayed congruence makes the affine numerator exactly 2^S modulo 2^(S+1), so the terminal iterate is odd.",
            "Induction through the affine prefixes gives the exact valuation word a for every n in the residue class.",
            "The odd coefficient 3^m is invertible modulo 2^(S+1), so the residue class is unique.",
            "Each finite cylinder contains r_a+q*2^(S+1) for every q>=0 and therefore infinitely many positive integers.",
            "Equivalently, positive integers are dense in Z_2; every finite 2-adic neighborhood of a TICKET77 ghost contains positive naturals.",
            "A locally constant finite-prefix Boolean separator that accepts every positive integer must therefore accept every 2-adic point.",
            "Hence finite residue bits, finite valuation words, or any continuous finite-state 2-adic coordinate cannot certify non-naturality of a ghost.",
        ],
        "machine_audit": audit,
        "computational_failure_count": computational_failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "fixed_residue_bits",
                "status": "refuted_by_natural_density",
                "counteredge": "Every residue modulo 2^k has infinitely many positive representatives.",
            },
            {
                "family": "finite_accelerated_valuation_word",
                "status": "refuted_by_exact_cylinder_formula",
                "counteredge": "Every finite positive valuation word has one exact residue class modulo 2^(S+1), populated by infinitely many naturals.",
            },
            {
                "family": "continuous_two_adic_natural_classifier",
                "status": "refuted_by_density_and_continuity",
                "counteredge": "A continuous Boolean map constant on all positive naturals is constant on their 2-adic closure Z_2.",
            },
        ],
        "discarded_route": (
            "Separate TICKET77 ghosts from positive integers with any fixed amount of residue, valuation-word, parity-word, "
            "or other locally constant 2-adic state. Every such neighborhood contains positive naturals."
        ),
        "retained_route": (
            "Couple growing 2-adic precision to an Archimedean height or descent quantity. The separator must be non-local in "
            "the 2-adic topology and must control actual integer magnitude across changing prefixes."
        ),
        "candidate_theorem": (
            "ArchimedeanTwoAdicCoupledDescent: every positive-integer accelerated trajectory either enters the known basin or "
            "strictly decreases a well-founded rank using both Archimedean height and growing 2-adic prefix precision; the "
            "rank cannot factor through any fixed finite 2-adic quotient."
        ),
        "next_theorem_target": "ArchimedeanTwoAdicCoupledDescent",
        "novelty_boundary": (
            "The 2-adic conjugacy and density principles are established mathematics. PrimeProject claims only an exact "
            "integration with the TICKET77 boundary state, a replayable finite-word audit, and a proof-route no-go guard."
        ),
        "proof_boundary": (
            "TICKET78 proves a no-go statement for finite or continuous purely 2-adic natural-admissibility separators. It "
            "does not exclude non-continuous or Archimedean-coupled ranks and does not prove Collatz."
        ),
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "finite-neighborhood no-go transfer discipline",
        "attempt": (
            "Transfer only the TICKET78 requirement that a finite local neighborhood cannot settle an infinite admissibility "
            "question when target objects are dense in the completion. No Collatz formula, count, or theorem is transferred."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "ticket78_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No problem-specific density or finite-neighborhood theorem was proved for this problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Derive a problem-specific local-to-global obstruction before using this transfer.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket77 = read_json(ROOT / "data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json")
    collatz_audit = analyze_finite_cylinder_no_go()
    attempts = [
        transfer_attempt(
            ticket77,
            "riemann",
            "RH-TICKET-78",
            "FiniteKernelNeighborhoodNoGoTransfer",
            "An actual-zeta detector couples all-height analytic tails to a nonlocal positivity margin rather than a fixed finite coefficient neighborhood.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-78",
            "route": "FiniteCylinderNaturalAdmissibilityNoGo",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact finite-cylinder theorem plus topological density counteredge",
            "attempt": (
                "Determine whether any finite 2-adic residue or valuation-prefix coordinate can distinguish TICKET77 ghosts "
                "from positive integers, and derive the exact finite-word cylinder formula."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-77", "finite_cylinder_no_go_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Synthesize and falsify Archimedean-plus-2-adic changing-prefix ranks.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket77,
            "goldbach",
            "GB-TICKET-78",
            "FiniteCongruenceNeighborhoodNoGoTransfer",
            "A global positive representation margin uses explicit analytic size bounds in addition to every finite local congruence condition.",
        ),
        transfer_attempt(
            ticket77,
            "twin-prime",
            "TP-TICKET-78",
            "FiniteSieveStateNoGoTransfer",
            "An exact gap-2 lower bound couples sieve state to a nonlocal parity-breaking estimate rather than a fixed finite admissibility pattern.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "finite_cylinder_admissibility_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 78 proves a Collatz proof-route no-go lemma but does not solve any open problem.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-78-finite-cylinder-admissibility-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-78-finite-cylinder-admissibility-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-78-finite-cylinder-admissibility-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-78-finite-cylinder-admissibility-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
