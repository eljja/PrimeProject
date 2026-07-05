from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AT = "2026-07-05T20:44:00+09:00"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_attempt(payload: dict[str, Any], problem_id: str) -> dict[str, Any]:
    for attempt in payload.get("attempts", []):
        if attempt.get("problem_id") == problem_id:
            return attempt
    raise KeyError(f"missing attempt for {problem_id}")


def affine_for_word(word: list[int]) -> tuple[int, int, int]:
    """Return (3^k, c, total_shift) for F_w(n)=(3^k n+c)/2^s."""
    multiplier = 1
    constant = 0
    total_shift = 0
    for valuation in word:
        constant = 3 * constant + (1 << total_shift)
        multiplier *= 3
        total_shift += valuation
    return multiplier, constant, total_shift


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def validate_exact_word_cycle(word: list[int], candidate: int) -> bool:
    value = candidate
    for expected in word:
        step = 3 * value + 1
        actual = v2(step)
        if actual != expected:
            return False
        value = step >> actual
    return value == candidate


def prove_collatz_word_kernel(row: dict[str, Any], *, label: str) -> dict[str, Any]:
    word = [int(value) for value in row["valuation_word"]]
    multiplier, constant, total_shift = affine_for_word(word)
    denominator = (1 << total_shift) - multiplier
    proof_steps = [
        f"Compose the exact accelerated odd Collatz branches for word {word}.",
        f"The composition is F_w(n)=({multiplier}*n+{constant})/2^{total_shift}.",
        "A cycle with this exact word must satisfy F_w(n)=n.",
        f"Therefore (2^{total_shift}-{multiplier})*n={constant}.",
        "Thus a positive integer cycle requires positive denominator, divisibility, and exact valuation replay.",
    ]
    if denominator <= 0:
        independent_status = "globally_eliminated_expanding_word"
        candidate_value = None
        validated = False
        reason = "denominator_nonpositive"
    elif constant % denominator != 0:
        independent_status = "globally_eliminated_nonintegral_fixed_point"
        candidate_value = None
        validated = False
        reason = "fixed_point_not_integral"
    else:
        candidate_value = constant // denominator
        validated = candidate_value > 0 and candidate_value % 2 == 1 and validate_exact_word_cycle(word, candidate_value)
        independent_status = "valid_positive_cycle" if validated else "globally_eliminated_invalid_fixed_point"
        reason = "exact_cycle_validated" if validated else "exact_valuation_replay_failed"

    expected_status = row.get("affine_cycle_status")
    if expected_status is not None and independent_status != expected_status:
        raise AssertionError(f"{label}: expected {expected_status}, got {independent_status}")
    if row.get("total_shift") is not None and int(row["total_shift"]) != total_shift:
        raise AssertionError(f"{label}: total shift mismatch")

    return {
        "label": label,
        "word_length": len(word),
        "total_shift": total_shift,
        "multiplier_3_power": multiplier,
        "affine_constant": constant,
        "denominator_2s_minus_3k": denominator,
        "candidate_value": candidate_value,
        "exact_valuation_replay": validated,
        "independent_status": independent_status,
        "reason": reason,
        "proof_steps": proof_steps,
    }


def riemann_micro_lemma(ticket25: dict[str, Any]) -> dict[str, Any]:
    attempt25 = find_attempt(ticket25, "riemann")
    bounded = attempt25["bounded_result"]
    missed = bounded.get("kernel_rows", [])
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-26",
        "status": "micro_lemma_closed_target_open",
        "route": "FinitePrefixNonUniversalityLemma",
        "proof_or_counterexample_mode": "shortcut_refutation",
        "attempt": (
            "Close the logical micro-lemma behind Ticket 25: a finite prefix certificate cannot by itself prove "
            "an all-height RH-equivalent statement unless it is paired with a theorem covering the unchecked tail."
        ),
        "formal_micro_lemma_statement": (
            "If a proposed RH route verifies only a finite prefix P and supplies no theorem for n>P or heights "
            "outside the checked window, then the route is not a universal proof certificate."
        ),
        "micro_lemma_certificate": {
            "source_ticket": "RH-TICKET-25",
            "finite_prefix_limit": bounded.get("search_cap"),
            "surrogate_missed_case_count": bounded.get("missed_case_count"),
            "witness_rows": missed,
            "closed_shortcut": "finite_prefix_implies_universal_RH",
            "proof_reason": "Universal quantification cannot be discharged by a finite prefix without a separate tail theorem.",
        },
        "closed_obligation": "Reject finite-prefix-only RH proof attempts.",
        "remaining_obligation": "A genuine RH proof still needs an all-height zeta-zero or equivalent positivity theorem.",
        "target_status": "open_not_proven",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_micro_lemma(ticket24: dict[str, Any]) -> dict[str, Any]:
    attempt24 = find_attempt(ticket24, "collatz")
    bounded = attempt24["bounded_result"]
    false_cycles = bounded.get("false_quotient_cycles_eliminated_by_affine_lift", [])
    certificates = [
        prove_collatz_word_kernel(row, label=f"false_quotient_cycle_{index + 1}")
        for index, row in enumerate(false_cycles)
    ]
    known_cycle = prove_collatz_word_kernel(
        {
            "valuation_word": [2],
            "affine_cycle_status": "valid_positive_cycle",
            "total_shift": 2,
        },
        label="known_1_cycle",
    )
    eliminated = [item for item in certificates if item["independent_status"].startswith("globally_eliminated")]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-26",
        "status": "micro_lemma_closed_target_open",
        "route": "AffineFixedPointNecessaryCondition",
        "proof_or_counterexample_mode": "exact_arithmetic_micro_proof",
        "attempt": (
            "Move the Ticket 25 Collatz affine-lift kernel from an empirical audit into an exact arithmetic "
            "micro-proof certificate."
        ),
        "formal_micro_lemma_statement": (
            "For an accelerated Collatz valuation word w of length k, total shift s, and affine constant c, "
            "any positive integer cycle realizing w must satisfy (2^s-3^k)n=c; hence 2^s>3^k, "
            "2^s-3^k divides c, and the candidate n must replay the exact valuation word."
        ),
        "micro_lemma_certificate": {
            "source_ticket": "CO-TICKET-24",
            "independent_recomputed_false_cycle_count": len(false_cycles),
            "eliminated_false_cycle_count": len(eliminated),
            "known_cycle_status": known_cycle["independent_status"],
            "known_cycle_candidate_value": known_cycle["candidate_value"],
            "false_cycle_certificates": certificates,
            "positive_control_certificate": known_cycle,
        },
        "closed_obligation": "False quotient SCCs are not Collatz counterexamples unless they pass the affine fixed-point kernel.",
        "remaining_obligation": (
            "The full Collatz conjecture still needs a global well-founded rank or cover for every non-cyclic "
            "exact branch and every larger quotient."
        ),
        "target_status": "open_not_proven",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_micro_lemma(ticket25: dict[str, Any]) -> dict[str, Any]:
    attempt25 = find_attempt(ticket25, "goldbach")
    bounded = attempt25["bounded_result"]
    bound = int(bounded.get("finite_bound", 0))
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-26",
        "status": "micro_lemma_closed_target_open",
        "route": "FiniteWindowNonUniversalityLemma",
        "proof_or_counterexample_mode": "shortcut_refutation",
        "attempt": (
            "Close the finite-window shortcut: a verified Goldbach window is a certificate only on its stated "
            "domain and cannot be promoted to all even integers without an explicit large-even theorem."
        ),
        "formal_micro_lemma_statement": (
            "A Goldbach certificate over even integers 4<=n<=B does not decide any even n>B. A proof for all "
            "even n must combine the finite certificate with a separate theorem covering the tail."
        ),
        "micro_lemma_certificate": {
            "source_ticket": "GB-TICKET-25",
            "verified_finite_bound": bound,
            "first_even_outside_certificate": bound + 2 if bound % 2 == 0 else bound + 1,
            "counterexamples_inside_bound": bounded.get("counterexample_count"),
            "closed_shortcut": "finite_window_implies_global_goldbach",
            "proof_reason": "The universal claim ranges over infinitely many even integers outside the finite certificate.",
        },
        "closed_obligation": "Reject finite-window-only Goldbach proof attempts.",
        "remaining_obligation": "A genuine Goldbach proof needs a positive two-prime representation lower bound beyond an explicit cutoff.",
        "target_status": "open_not_proven",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found in the certified finite window.",
    }


def twin_micro_lemma(ticket25: dict[str, Any]) -> dict[str, Any]:
    attempt25 = find_attempt(ticket25, "twin-prime")
    bounded = attempt25["bounded_result"]
    rows = bounded.get("counterkernel_rows", [])
    separated_rows = [
        {
            "limit": row.get("limit"),
            "exact_gap_2_retention_after_deletion": row.get("exact_gap_2_retention_after_deletion"),
            "bounded_without_gap_2_retention_ratio": row.get("bounded_without_gap_2_retention_ratio"),
            "separates_bounded_gap_from_exact_gap_2": (
                row.get("exact_gap_2_retention_after_deletion") == 0
                and float(row.get("bounded_without_gap_2_retention_ratio", 0.0)) > 0.0
            ),
        }
        for row in rows
    ]
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-26",
        "status": "micro_lemma_closed_target_open",
        "route": "BoundedGapExactGapSeparationLemma",
        "proof_or_counterexample_mode": "finite_countermodel_shortcut_refutation",
        "attempt": (
            "Close the bounded-gap shortcut: a statistic that remains positive after deleting all exact gap-2 "
            "pairs cannot by itself imply the twin prime conjecture."
        ),
        "formal_micro_lemma_statement": (
            "Any proof route whose decisive statistic is invariant under deleting exact gap-2 pairs while retaining "
            "bounded gaps proves at most a bounded-gap statement, not infinitely many exact twin pairs."
        ),
        "micro_lemma_certificate": {
            "source_ticket": "TP-TICKET-25",
            "separation_rows": separated_rows,
            "all_tested_rows_separate": all(row["separates_bounded_gap_from_exact_gap_2"] for row in separated_rows),
            "closed_shortcut": "bounded_gap_positive_mass_implies_exact_gap_2_infinitude",
        },
        "closed_obligation": "Reject bounded-gap-only substitutions for twin-prime infinitude.",
        "remaining_obligation": "A genuine twin-prime proof needs an unconditional lower bound for exact gap 2 at arbitrarily large scale.",
        "target_status": "open_not_proven",
        "claim_boundary": "No Twin Prime proof and no Twin Prime counterexample.",
    }


def build_payload() -> dict[str, Any]:
    ticket24 = read_json(ROOT / "data/open-problem/ticket24-bridge-weight-lab.json")
    ticket25 = read_json(ROOT / "data/open-problem/ticket25-formal-lemma-kernel.json")
    attempts = [
        riemann_micro_lemma(ticket25),
        collatz_micro_lemma(ticket24),
        goldbach_micro_lemma(ticket25),
        twin_micro_lemma(ticket25),
    ]
    return {
        "schema": "primeproject.ticket26-micro-lemma-closure.v1",
        "generated_at": GENERATED_AT or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "micro_lemma_closed_full_conjectures_open",
        "claim_boundary": (
            "Ticket 26 closes small proof-kernel obligations and shortcut refutations. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> None:
    payload = build_payload()
    output = ROOT / "data/open-problem/ticket26-micro-lemma-closure.json"
    write_json(output, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-26-finite-universal-gap.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-26-affine-fixed-point-proof.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-26-finite-window-gap.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-26-bounded-gap-model-separation.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem[attempt["problem_id"]], attempt)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
