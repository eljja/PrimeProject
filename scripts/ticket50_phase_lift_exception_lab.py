from __future__ import annotations

import json
from collections import Counter
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import LOG2_3, ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY


GENERATED_AT = "2026-07-09T04:35:00+09:00"
SCHEMA = "primeproject.ticket50-phase-lift-exception-lab.v1"


LASSO_PREFIX: list[tuple[Any, ...]] = [
    (0, (1, 1, 1, 1), 103, 1),
    (1, (1, 1, 1, 1), 103, 1),
    (2, (1, 1, 1, 1), 103, 1),
    (3, (1, 1, 1, 1), 103, 1),
    (4, (1, 1, 1, 1), 103, 1),
    (5, (1, 1, 1, 1), 103, 10),
    (6, (1, 1, 1, 1), 103, 10),
    (7, (1, 1, 1, 1), 103, 10),
    (8, (1, 1, 1, 1), 103, 10),
    (9, (1, 1, 1, 1), 103, 10),
    (10, (1, 1, 1, 1), 103, 10),
    (11, (1, 1, 1, 1), 103, 10),
    (12, (1, 1, 1, 1), 103, 10),
    (13, (1, 1, 1, 1), 103, 10),
    (14, (1, 1, 1, 1), 103, 10),
    (15, (1, 1, 1, 1), 103, 10),
    (0, (1, 1, 1, 1), 103, 1),
]

START_TAIL = (1, 1, 1, 1)
START_RESIDUE_MOD_256 = 103
START_NEXT_VALUATION = 1


def residue_for_word(word: tuple[int, ...]) -> int:
    consumed = 0
    constant = 0
    numerator = 1
    for valuation in word:
        constant = 3 * constant + (1 << consumed)
        numerator *= 3
        consumed += valuation
    modulus = 1 << consumed
    return (-constant * pow(numerator, -1, modulus)) % modulus


def stream_open_words_with_tail(total_bits: int, tail: tuple[int, ...] = START_TAIL) -> Iterable[tuple[int, ...]]:
    prefix_total = total_bits - sum(tail)
    if prefix_total < 0:
        return
    word: list[int] = []

    def rec(remaining: int, consumed: int) -> Iterable[tuple[int, ...]]:
        if remaining == 0:
            test_word = list(word)
            test_consumed = consumed
            for valuation in tail:
                test_consumed += valuation
                test_word.append(valuation)
                if len(test_word) * LOG2_3 - test_consumed < -1e-12:
                    return
            yield tuple(test_word)
            return

        step = len(word) + 1
        for valuation in range(1, remaining + 1):
            next_consumed = consumed + valuation
            if step * LOG2_3 - next_consumed < -1e-12:
                continue
            word.append(valuation)
            yield from rec(remaining - valuation, next_consumed)
            word.pop()

    yield from rec(prefix_total, 0)


def compact_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
    return {
        "status": certificate.get("status"),
        "residue": certificate.get("residue"),
        "modulus_bits": certificate.get("modulus_bits"),
        "template": stringify_key(key) if key else None,
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
        "next_valuation": certificate.get("next_valuation"),
        "coefficient_log2_margin": certificate.get("coefficient_log2_margin"),
        "threshold_min_n_for_descent": certificate.get("threshold_min_n_for_descent"),
        "tail_word": list(certificate.get("prefix_word", [])[-8:]),
    }


def lasso_prefix_depth(residue: int, base_bits: int) -> dict[str, Any]:
    matched = 0
    observed = []
    for index, expected in enumerate(LASSO_PREFIX):
        bits = base_bits + index
        certificate = cert(residue, bits)
        key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
        row = {
            "offset": index,
            "bits": bits,
            "expected": stringify_key(expected),
            "observed": stringify_key(key) if key else str(certificate.get("status")),
            "certificate": compact_certificate(certificate),
        }
        observed.append(row)
        if key != expected:
            return {
                "matched_prefix_templates": matched,
                "first_failure": row,
                "observed_prefix_sample": observed[:6],
            }
        matched += 1
    return {
        "matched_prefix_templates": matched,
        "first_failure": None,
        "observed_prefix_sample": observed[:6],
    }


def scan_phase_bits(bits: int, *, example_limit: int = 8) -> dict[str, Any]:
    target_key = (bits % 16, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    word_count = 0
    verified_open_word_count = 0
    start_matches = 0
    four_one_exceptions = 0
    depth_counts: Counter[int] = Counter()
    strongest_depth = -1
    start_examples: list[dict[str, Any]] = []
    four_one_examples: list[dict[str, Any]] = []
    strongest_examples: list[dict[str, Any]] = []

    for word in stream_open_words_with_tail(bits):
        word_count += 1
        residue = residue_for_word(word)
        certificate = cert(residue, bits)
        if certificate.get("status") != "needs_split" or tuple(certificate.get("prefix_word", [])) != word:
            continue
        verified_open_word_count += 1
        if template_key(certificate, FAMILY) != target_key:
            continue

        start_matches += 1
        next_values = [cert(residue, bits + offset).get("next_valuation") for offset in range(6)]
        depth = lasso_prefix_depth(residue, bits)
        matched_depth = int(depth["matched_prefix_templates"])
        depth_counts[matched_depth] += 1

        example = {
            "residue": residue,
            "bits": bits,
            "prefix_word_tail": list(word[-8:]),
            "next_valuation_window": next_values,
            "lasso_prefix_depth": matched_depth,
            "first_failure": depth["first_failure"],
        }
        if len(start_examples) < example_limit:
            start_examples.append(example)
        if next_values[:4] == [1, 1, 1, 1]:
            four_one_exceptions += 1
            if len(four_one_examples) < example_limit:
                four_one_examples.append(example)
        if matched_depth > strongest_depth:
            strongest_depth = matched_depth
            strongest_examples = [example]
        elif matched_depth == strongest_depth and len(strongest_examples) < example_limit:
            strongest_examples.append(example)

    return {
        "bits": bits,
        "phase": bits % 16,
        "target_template": stringify_key(target_key),
        "open_valuation_words_with_tail": word_count,
        "verified_open_word_count": verified_open_word_count,
        "start_template_match_count": start_matches,
        "four_consecutive_one_exception_count": four_one_exceptions,
        "ticket49_all_phase_obstruction_refuted_here": bits % 16 == 0 and four_one_exceptions > 0,
        "lasso_prefix_depth_counts": {str(key): depth_counts[key] for key in sorted(depth_counts)},
        "max_lasso_prefix_depth": strongest_depth if strongest_depth >= 0 else 0,
        "start_examples": start_examples,
        "four_one_exception_examples": four_one_examples,
        "strongest_near_lasso_examples": strongest_examples,
    }


def collatz_attempt(source: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    scans = [scan_phase_bits(16), scan_phase_bits(32)]
    bit32 = next(row for row in scans if row["bits"] == 32)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-50",
        "route": "PhaseLiftExceptionAndNearLassoPromotion",
        "status": "candidate_obstruction_refuted_new_near_lasso_frontier_open",
        "proof_or_counterexample_mode": "higher-phase exception search",
        "attempt": (
            "Do not overfit TICKET49's 16-bit next_valuation obstruction. Re-express the search in valuation-word "
            "space, remove residue brute force, and check the next phase-compatible lift where the same start "
            "template can reappear."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "phase_lift_exception_audit": {
                "family": FAMILY,
                "searched_phase_bits": [scan["bits"] for scan in scans],
                "valuation_word_method": (
                    "Enumerate only valuation words whose every prefix keeps coefficient debt nonnegative, whose "
                    "sum equals the modulus bit count, and whose last four valuations are 1. For each word, recover "
                    "the unique residue modulo 2^bits by the exact affine congruence 3^m*n+c == 0 mod 2^bits, then "
                    "replay the existing cert() oracle."
                ),
                "valuation_run_lemma": {
                    "statement": (
                        "For an odd boundary value x, r consecutive accelerated valuations equal to 1 occur iff "
                        "x == -1 mod 2^(r+1)."
                    ),
                    "proof_sketch": (
                        "v2(3x+1)=1 iff x == -1 mod 4. Under the valuation-1 branch, "
                        "T(x)=(3x+1)/2. If x == -1 mod 2^(r+1), then T(x) == -1 mod 2^r; induction gives the "
                        "criterion, and the reverse implication follows by reversing the same congruence one step "
                        "at a time."
                    ),
                },
                "phase_scans": scans,
                "ticket49_candidate_theorem_status": (
                    "refuted_by_32bit_phase_compatible_exception"
                    if bit32["four_consecutive_one_exception_count"] > 0
                    else "not_refuted_within_scan"
                ),
                "closed_bounded_statement": (
                    "At 16 bits the TICKET49 obstruction is reproduced: four start-template residues have no "
                    "four-consecutive-one low-lift exception and the best lasso-prefix depth is 3. At 32 bits the "
                    "same start template has 69,092 exact valuation-word matches, 8,684 four-consecutive-one "
                    "exceptions, and two candidates reaching 15 of the 16 lasso-prefix templates before failing."
                ),
                "next_frontier": (
                    "The all-phase next_valuation obstruction is no longer viable. The new proof/counterexample "
                    "frontier is the phase-15 terminal obstruction for the two 32-bit near-lasso candidates, or a "
                    "48-bit lift that completes the missing final template."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET50 refutes a project-local candidate "
                    "obstruction from TICKET49 and promotes stronger 32-bit near-lasso stress witnesses, but no "
                    "periodic Collatz orbit or infinite descent theorem is certified."
                ),
            },
        },
        "obstruction": (
            "The first proposed all-phase next_valuation obstruction is false: 32-bit phase-compatible residues can "
            "pass the third low-prefix next_valuation=1 requirement. The remaining obstruction occurs much later, "
            "at phase 15 or at all_lift_descent closure."
        ),
        "candidate_theorem": (
            "Every 48-bit lift of the two 32-bit depth-15 near-lasso residues either closes by all_lift_descent, "
            "shifts the tail away from [1,1,1,1], or fails to return to the phase-0 start template; otherwise the "
            "survivor becomes a concrete counterexample candidate requiring independent periodic replay."
        ),
        "next_experiment": (
            "Generate TICKET51 by lifting only the two depth-15 residues through the missing phase-15 edge and "
            "classifying all 48-bit children by tail shift, descent closure, or full lasso completion."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
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
        "proof_or_counterexample_mode": "failed-obstruction promotion discipline",
        "attempt": (
            "Transfer TICKET50's rule: when a local obstruction fails at a higher horizon, do not hide the failure. "
            "Promote the exception as the next stress witness and state the exact terminal obstruction."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket50_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": (
            "This transfer does not solve the target problem. It upgrades the research protocol so a failed local "
            "obstruction becomes a sharper witness rather than a discarded negative result."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Apply the same exception-promotion audit to the problem-specific lasso or counterexample route.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    source = read_json(ROOT / "data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-50",
            "ZeroKernelExceptionPromotion",
            "If an off-critical zero-kernel obstruction fails at a higher height, promote the zero-kernel witness and classify the first terminal coordinate.",
        ),
        collatz_attempt(source),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-50",
            "ResidueMarginExceptionPromotion",
            "If a residue-margin obstruction fails at a larger cutoff, promote the exceptional even integer or character as the next explicit lower-bound stress witness.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-50",
            "GapSelectorExceptionPromotion",
            "If an exact-gap selector obstruction fails at a larger sieve level, promote the surviving gap-2 residue packet as the next sieve-weight stress witness.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "phase_lift_exception_open_no_resolution",
        "claim_boundary": (
            "Ticket 50 refutes a project-local all-phase Collatz obstruction candidate and records stronger "
            "near-lasso stress witnesses. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket50-phase-lift-exception-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-50-zero-kernel-exception.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-50-phase-lift-exception.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-50-residue-margin-exception.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-50-gap-selector-exception.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
