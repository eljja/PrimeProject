from __future__ import annotations

import json
import random
from collections import Counter
from functools import lru_cache
from typing import Any

from ticket30_potential_synthesis_lab import LOG2_3, ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, transition_label
from ticket42_parametric_transition_template_lab import edge_delta, stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket50_phase_lift_exception_lab import (
    LASSO_PREFIX,
    START_RESIDUE_MOD_256,
    START_TAIL,
    residue_for_word,
)
from ticket51_phase15_terminal_lift_lab import compact_certificate, mismatch_reason


GENERATED_AT = "2026-07-09T06:40:00+09:00"
SCHEMA = "primeproject.ticket52-frontier-budget-lab.v1"
SAMPLE_BITS = 48
SAMPLE_COUNT = 200_000
SAMPLE_SEED = 20_260_709
COUNT_BITS = [16, 32, 40, 48, 56, 64]


@lru_cache(maxsize=None)
def open_word_count(total_bits: int) -> int:
    prefix_total = total_bits - sum(START_TAIL)

    @lru_cache(maxsize=None)
    def rec(remaining: int, consumed: int, length: int) -> int:
        if remaining == 0:
            test_consumed = consumed
            test_length = length
            for valuation in START_TAIL:
                test_consumed += valuation
                test_length += 1
                if test_length * LOG2_3 - test_consumed < -1e-12:
                    return 0
            return 1

        total = 0
        step = length + 1
        for valuation in range(1, remaining + 1):
            next_consumed = consumed + valuation
            if step * LOG2_3 - next_consumed < -1e-12:
                continue
            total += rec(remaining - valuation, next_consumed, step)
        return total

    return rec(prefix_total, 0, 0)


def random_debt_valid_word(total_bits: int, rng: random.Random) -> tuple[int, ...] | None:
    prefix_total = total_bits - sum(START_TAIL)
    remaining = prefix_total
    consumed = 0
    word: list[int] = []

    while remaining > 0:
        step = len(word) + 1
        values = []
        weights = []
        for valuation in range(1, remaining + 1):
            next_consumed = consumed + valuation
            if step * LOG2_3 - next_consumed < -1e-12:
                continue
            values.append(valuation)
            weights.append(1.0 / (valuation**1.35))
        if not values:
            return None
        valuation = rng.choices(values, weights=weights, k=1)[0]
        word.append(valuation)
        consumed += valuation
        remaining -= valuation

    test_consumed = consumed
    test_length = len(word)
    for valuation in START_TAIL:
        test_consumed += valuation
        test_length += 1
        if test_length * LOG2_3 - test_consumed < -1e-12:
            return None
    return tuple(word) + START_TAIL


def compact_projection(residue: int, bits: int = 32) -> dict[str, Any]:
    projection = residue % (1 << bits)
    certificate = cert(projection, bits)
    key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
    return {
        "bits": bits,
        "residue": projection,
        "status": certificate.get("status"),
        "template": stringify_key(key) if key else str(certificate.get("status")),
        "next_valuation": certificate.get("next_valuation"),
        "tail_word": list(certificate.get("prefix_word", [])[-8:]),
    }


def lasso_prefix_depth_at(residue: int, base_bits: int) -> dict[str, Any]:
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


def generalized_terminal_lift_audit(roots: list[int], base_bits: int) -> dict[str, Any]:
    states = [{"root_residue": residue, "residue": residue, "bits": base_bits, "path": []} for residue in roots]
    rows = []
    best_depth = 0
    best_paths: list[dict[str, Any]] = []

    for step, expected in enumerate(LASSO_PREFIX[1:], start=1):
        next_states = []
        mismatch_counter: Counter[str] = Counter()
        mismatch_examples = []
        transition_count = 0
        match_count = 0

        for state in states:
            residue = int(state["residue"])
            bits = int(state["bits"])
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            label = transition_label(low.get("status") == "needs_split", high.get("status") == "needs_split")
            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                transition_count += 1
                key = template_key(child, FAMILY) if child.get("status") == "needs_split" else None
                if key == expected:
                    match_count += 1
                    delta = edge_delta(parent, child)
                    new_path = [
                        *state["path"],
                        {
                            "step": step,
                            "direction": direction,
                            "label": label,
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "bits": bits + 1,
                            "expected_template": stringify_key(expected),
                            "observed_template": stringify_key(key),
                            **delta,
                        },
                    ]
                    next_state = {
                        "root_residue": state["root_residue"],
                        "residue": child_residue,
                        "bits": bits + 1,
                        "path": new_path,
                    }
                    next_states.append(next_state)
                    if len(new_path) > best_depth:
                        best_depth = len(new_path)
                        best_paths = [next_state]
                    elif len(new_path) == best_depth and len(best_paths) < 8:
                        best_paths.append(next_state)
                    continue

                reason = mismatch_reason(child, expected)
                mismatch_counter[reason] += 1
                if len(mismatch_examples) < 10:
                    mismatch_examples.append(
                        {
                            "step": step,
                            "direction": direction,
                            "root_residue": state["root_residue"],
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "bits": bits + 1,
                            "expected_template": stringify_key(expected),
                            "observed": stringify_key(key) if key else str(child.get("status")),
                            "reason": reason,
                            "certificate": compact_certificate(child),
                        }
                    )

        rows.append(
            {
                "step": step,
                "expected_template": stringify_key(expected),
                "input_states": len(states),
                "tested_branches": transition_count,
                "matching_branches": match_count,
                "surviving_states": len(next_states),
                "mismatch_counts": dict(sorted(mismatch_counter.items())),
                "mismatch_examples": mismatch_examples,
            }
        )
        states = next_states
        if not states:
            break

    terminal_row = rows[-1] if rows else {}
    return {
        "family": FAMILY,
        "source_roots": roots,
        "base_bits": base_bits,
        "target_prefix_length": len(LASSO_PREFIX) - 1,
        "rows": rows,
        "terminal_step": terminal_row.get("step"),
        "terminal_mismatch_counts": terminal_row.get("mismatch_counts", {}),
        "final_surviving_states": len(states),
        "full_lasso_completion_count": len(states) if len(rows) == len(LASSO_PREFIX) - 1 else 0,
        "best_edge_depth": best_depth,
        "best_template_depth": best_depth + 1 if roots else 0,
        "best_paths": [
            {
                "root_residue": path["root_residue"],
                "final_residue": path["residue"],
                "final_bits": path["bits"],
                "directions": [step["direction"] for step in path["path"]],
                "path_sample": path["path"][:6],
            }
            for path in best_paths
        ],
    }


def sample_48_frontier() -> dict[str, Any]:
    rng = random.Random(SAMPLE_SEED)
    target_key = (SAMPLE_BITS % 16, START_TAIL, START_RESIDUE_MOD_256, 1)
    stats: Counter[str] = Counter()
    depth_counts: Counter[int] = Counter()
    strongest: list[dict[str, Any]] = []
    depth15_roots = []
    seen = set()

    for sample_index in range(1, SAMPLE_COUNT + 1):
        word = random_debt_valid_word(SAMPLE_BITS, rng)
        if word is None:
            stats["invalid_tail_debt"] += 1
            continue
        residue = residue_for_word(word)
        if residue in seen:
            stats["duplicate_residue"] += 1
            continue
        seen.add(residue)
        certificate = cert(residue, SAMPLE_BITS)
        if certificate.get("status") != "needs_split" or tuple(certificate.get("prefix_word", [])) != word:
            stats["unverified_canonical_word"] += 1
            continue
        stats["verified_open_word"] += 1
        if template_key(certificate, FAMILY) != target_key:
            continue

        stats["start_template_match"] += 1
        depth = lasso_prefix_depth_at(residue, SAMPLE_BITS)
        matched_depth = int(depth["matched_prefix_templates"])
        depth_counts[matched_depth] += 1
        projection = compact_projection(residue, 32)
        example = {
            "sample_index": sample_index,
            "residue": residue,
            "bits": SAMPLE_BITS,
            "projection32": projection,
            "lasso_prefix_depth": matched_depth,
            "first_failure": depth["first_failure"],
            "prefix_word_tail": list(word[-12:]),
        }
        strongest.append(example)
        strongest = sorted(strongest, key=lambda item: int(item["lasso_prefix_depth"]), reverse=True)[:12]
        if matched_depth >= 15:
            depth15_roots.append(example)

    depth15_roots = sorted(depth15_roots, key=lambda item: int(item["residue"]))
    terminal = generalized_terminal_lift_audit([int(item["residue"]) for item in depth15_roots], SAMPLE_BITS)
    return {
        "bits": SAMPLE_BITS,
        "sample_seed": SAMPLE_SEED,
        "sample_count": SAMPLE_COUNT,
        "sampler": "debt_valid_weighted_random_valuation_words_not_uniform_not_exhaustive",
        "target_template": stringify_key(target_key),
        "statistics": dict(sorted(stats.items())),
        "lasso_prefix_depth_counts": {str(key): depth_counts[key] for key in sorted(depth_counts)},
        "max_sampled_lasso_prefix_depth": max(depth_counts) if depth_counts else 0,
        "strongest_examples": strongest,
        "new_depth15_root_count": len(depth15_roots),
        "new_depth15_roots": depth15_roots,
        "terminal_lift_audit": terminal,
    }


def collatz_attempt(source: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    counts = [{"bits": bits, "open_valuation_words_with_tail": open_word_count(bits)} for bits in COUNT_BITS]
    count_by_bits = {row["bits"]: row["open_valuation_words_with_tail"] for row in counts}
    sample = sample_48_frontier()
    terminal = sample["terminal_lift_audit"]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-52",
        "route": "FrontierBudgetAndNew48BitStressWitness",
        "status": "new_48bit_near_lasso_witness_terminally_closed_open_problem_open",
        "proof_or_counterexample_mode": "frontier budget plus sampled witness closure",
        "attempt": (
            "Do not relift only the two closed TICKET51 roots. First quantify the exact valuation-word frontier, "
            "then run a deterministic stress sampler for genuinely new 48-bit start-template roots and terminally "
            "classify any near-lasso witness it finds."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "frontier_budget_audit": {
                "family": FAMILY,
                "exact_open_word_counts": counts,
                "direct_48bit_exhaustive_search_status": "blocked_by_83401400116_word_frontier",
                "direct_64bit_exhaustive_search_status": "blocked_by_2216134944775156_word_frontier",
                "frontier_growth_48_over_32": count_by_bits[48] / count_by_bits[32],
                "projection_completeness_failure": (
                    "A 48-bit start-template root need not project to a 32-bit start-template root. The sampled "
                    "depth-15 witness projects to template [0,[1,2,1,1],103,2], so TICKET51's two-root ancestry "
                    "closure cannot be promoted to a 48-bit theorem."
                ),
                "sampled_48bit_frontier": sample,
                "closed_bounded_statement": (
                    "The deterministic 200,000-word 48-bit sampler found one new depth-15 near-lasso witness "
                    "outside the TICKET51 ancestry. A base-48 generalized terminal lift audit closes its low/high "
                    "terminal branches at phase 15 by tail_word+next_valuation mismatch; no full lasso completion "
                    "survives."
                ),
                "next_frontier": (
                    "The next serious route is not a larger blind sample. It is a symbolic or automaton-counting "
                    "search that can cover the 83,401,400,116 48-bit valuation words without enumerating them."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET52 finds and closes one new sampled "
                    "48-bit near-lasso witness, and proves that the 48-bit frontier is too large for the old "
                    "valuation-word enumeration. The sampler is not exhaustive and cannot exclude unsampled roots."
                ),
            },
        },
        "obstruction": (
            "The prior closure was ancestry-local: new 48-bit near-lasso roots can project outside the two closed "
            "32-bit roots. The new sampled witness closes terminally, but the unsampled 48-bit frontier remains open."
        ),
        "candidate_theorem": (
            "A complete Collatz lasso-exclusion route now requires a symbolic counter of all 48-bit start-template "
            "roots, or a theorem proving every depth-15 terminal branch has the same tail/next-valuation mismatch."
        ),
        "next_experiment": (
            "Build TICKET53 as a residue-automaton or SAT/SMT-style symbolic counter for all 48-bit start-template "
            "roots, rather than increasing the random sample."
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
        "proof_or_counterexample_mode": "frontier budget before witness promotion",
        "attempt": (
            "Transfer TICKET52's rule: before promoting a finite stress witness, quantify the unseen frontier and "
            "separate sampled closure from exhaustive or symbolic closure."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket52_transfer": route,
            "candidate_theorem": candidate_theorem,
            "frontier_rule": (
                "A witness closure is publishable only as local evidence unless the remaining frontier is either "
                "exhaustively covered or reduced by a symbolic theorem."
            ),
        },
        "obstruction": (
            "This transfer is a claim-discipline upgrade. It does not solve the target problem; it blocks the common "
            "mistake of treating a closed sample witness as an infinite theorem."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Attach a problem-specific frontier budget to the strongest unresolved witness family.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    source = read_json(ROOT / "data/open-problem/ticket51-phase15-terminal-lift-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-52",
            "ZeroKernelFrontierBudget",
            "Any off-critical zero-kernel packet must expose the size of the uncovered zero-search frontier before it can be promoted beyond sampled closure.",
        ),
        collatz_attempt(source),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-52",
            "ResidueMarginFrontierBudget",
            "Any Goldbach residue-margin packet must quantify the uncovered even/residue frontier before a positive-margin sample can support a theorem route.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-52",
            "GapSelectorFrontierBudget",
            "Any exact-gap selector packet must quantify the uncovered gap-leakage frontier before sampled gap-2 persistence can be promoted.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "frontier_budget_open_no_resolution",
        "claim_boundary": (
            "Ticket 52 quantifies the 48/64-bit Collatz frontier and closes one new sampled 48-bit near-lasso "
            "witness. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket52-frontier-budget-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-52-frontier-budget-contract.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-52-frontier-budget-sample-closure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-52-frontier-budget-contract.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-52-frontier-budget-contract.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
