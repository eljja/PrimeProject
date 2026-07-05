from __future__ import annotations

import json
import math
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AT = "2026-07-06T02:05:00+09:00"
SCHEMA = "primeproject.ticket29-adaptive-frontier-lab.v1"
LOG2_3 = math.log2(3.0)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for prime in range(2, int(limit**0.5) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return flags


def collatz_prefix_certificate(residue: int, bits: int, max_steps: int = 512) -> dict[str, Any]:
    numerator = 1
    constant = 0
    consumed_bits = 0
    prefix_length = 0
    current = residue
    word: list[int] = []

    for _ in range(max_steps):
        valuation = v2(3 * current + 1)
        if consumed_bits + valuation > bits:
            return {
                "status": "needs_split",
                "residue": residue,
                "modulus_bits": bits,
                "prefix_word": word,
                "prefix_length": prefix_length,
                "consumed_bits": consumed_bits,
                "next_valuation": valuation,
                "coefficient_log2_debt": round(prefix_length * LOG2_3 - consumed_bits, 8),
            }

        constant = 3 * constant + (1 << consumed_bits)
        numerator *= 3
        consumed_bits += valuation
        prefix_length += 1
        word.append(valuation)
        current = (3 * current + 1) >> valuation

        denominator = 1 << consumed_bits
        gap = denominator - numerator
        if gap > 0:
            threshold = constant // gap + 1
            base = {
                "residue": residue,
                "modulus_bits": bits,
                "prefix_word": word,
                "prefix_length": prefix_length,
                "consumed_bits": consumed_bits,
                "threshold_min_n_for_descent": threshold,
                "coefficient_log2_margin": round(consumed_bits - prefix_length * LOG2_3, 8),
            }
            if residue == 1 and threshold == 2:
                return {**base, "status": "known_cycle_exception"}
            if threshold <= residue:
                return {**base, "status": "all_lift_descent"}
            return {**base, "status": "finite_threshold_exception"}

    return {
        "status": "max_steps_exhausted",
        "residue": residue,
        "modulus_bits": bits,
        "prefix_word": word,
        "prefix_length": prefix_length,
        "consumed_bits": consumed_bits,
        "coefficient_log2_debt": round(prefix_length * LOG2_3 - consumed_bits, 8),
    }


def keep_top(items: list[dict[str, Any]], item: dict[str, Any], limit: int = 12) -> None:
    items.append(item)
    items.sort(
        key=lambda row: (
            float(row.get("coefficient_log2_debt", 0.0)),
            int(row.get("prefix_length", 0)),
            int(row.get("residue", 0)),
        ),
        reverse=True,
    )
    del items[limit:]


def collatz_adaptive_split(base_bits: int, max_bits: int) -> dict[str, Any]:
    queue: deque[tuple[int, int]] = deque((residue, base_bits) for residue in range(1, 1 << base_bits, 2))
    per_depth: dict[int, dict[str, int]] = {}
    top_open_examples: list[dict[str, Any]] = []
    top_closed_examples: list[dict[str, Any]] = []
    processed_state_count = 0
    split_parent_count = 0
    max_prefix_length = 0
    max_consumed_bits = 0

    while queue:
        residue, bits = queue.popleft()
        processed_state_count += 1
        certificate = collatz_prefix_certificate(residue, bits)
        status = str(certificate["status"])
        row = per_depth.setdefault(
            bits,
            {
                "processed": 0,
                "all_lift_descent": 0,
                "known_cycle_exception": 0,
                "finite_threshold_exception": 0,
                "needs_split": 0,
                "max_steps_exhausted": 0,
                "split_children": 0,
            },
        )
        row["processed"] += 1
        row[status] = row.get(status, 0) + 1
        max_prefix_length = max(max_prefix_length, int(certificate.get("prefix_length", 0)))
        max_consumed_bits = max(max_consumed_bits, int(certificate.get("consumed_bits", 0)))

        if status == "needs_split" and bits < max_bits:
            queue.append((residue, bits + 1))
            queue.append((residue + (1 << bits), bits + 1))
            row["split_children"] += 2
            split_parent_count += 1
        elif status in {"needs_split", "max_steps_exhausted"}:
            keep_top(top_open_examples, certificate)
        elif status == "all_lift_descent" and len(top_closed_examples) < 12:
            top_closed_examples.append(certificate)

    cumulative_processed = 0
    cumulative_closed = 0
    adaptive_depth_rows: list[dict[str, Any]] = []
    for bits in sorted(per_depth):
        row = per_depth[bits]
        closed = row.get("all_lift_descent", 0) + row.get("known_cycle_exception", 0) + row.get(
            "finite_threshold_exception", 0
        )
        open_count = row.get("needs_split", 0) + row.get("max_steps_exhausted", 0)
        cumulative_processed += row["processed"]
        cumulative_closed += closed
        adaptive_depth_rows.append(
            {
                "modulus_bits": bits,
                "processed_at_depth": row["processed"],
                "closed_at_depth": closed,
                "needs_split_at_depth": row.get("needs_split", 0),
                "max_steps_exhausted_at_depth": row.get("max_steps_exhausted", 0),
                "split_children_at_depth": row.get("split_children", 0),
                "open_frontier_at_depth": open_count if bits == max_bits else row.get("split_children", 0),
                "cumulative_processed": cumulative_processed,
                "cumulative_closed": cumulative_closed,
            }
        )

    full_odd_cylinders_at_max = 1 << (max_bits - 1)
    max_row = adaptive_depth_rows[-1]
    open_at_max = int(max_row["needs_split_at_depth"]) + int(max_row["max_steps_exhausted_at_depth"])
    closed_at_max = int(max_row["closed_at_depth"])
    return {
        "base_modulus_bits": base_bits,
        "max_modulus_bits": max_bits,
        "processed_state_count": processed_state_count,
        "split_parent_count": split_parent_count,
        "full_odd_cylinders_at_max_bits": full_odd_cylinders_at_max,
        "processed_fraction_of_full_max_space": round(processed_state_count / full_odd_cylinders_at_max, 8),
        "open_frontier_count_at_max_bits": open_at_max,
        "open_frontier_fraction_of_full_max_space": round(open_at_max / full_odd_cylinders_at_max, 8),
        "closed_at_max_depth": closed_at_max,
        "closed_fraction_of_processed_max_depth": round(
            closed_at_max / max(int(max_row["processed_at_depth"]), 1), 8
        ),
        "max_exact_prefix_length_seen": max_prefix_length,
        "max_consumed_bits_seen": max_consumed_bits,
        "adaptive_depth_rows": adaptive_depth_rows,
        "top_open_frontier_examples": top_open_examples,
        "closed_descent_examples": top_closed_examples,
        "naive_termination_verdict": "not_supported_by_ticket29",
        "interpretation": (
            "Adaptive splitting avoids full enumeration, but the open frontier at the tested max depth is still large. "
            "This does not produce a Collatz counterexample; it refutes the naive claim that merely splitting "
            "needs_split cylinders is enough evidence for termination."
        ),
    }


def mertens_stress(limit: int) -> dict[str, Any]:
    mu = [0] * (limit + 1)
    mu[1] = 1
    composites = bytearray(limit + 1)
    primes: list[int] = []
    for value in range(2, limit + 1):
        if not composites[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            composites[product] = 1
            if value % prime == 0:
                mu[product] = 0
                break
            mu[product] = -mu[value]

    total = 0
    max_from_10k = (0.0, 0, 0)
    max_from_1m = (0.0, 0, 0)
    for n in range(1, limit + 1):
        total += mu[n]
        normalized = abs(total) / math.sqrt(n)
        if n >= 10_000 and normalized > max_from_10k[0]:
            max_from_10k = (normalized, n, total)
        if n >= 1_000_000 and normalized > max_from_1m[0]:
            max_from_1m = (normalized, n, total)
    return {
        "limit": limit,
        "mertens_at_limit": total,
        "max_abs_mertens_over_sqrt_n_from_10000": {
            "value": round(max_from_10k[0], 10),
            "n": max_from_10k[1],
            "mertens": max_from_10k[2],
        },
        "max_abs_mertens_over_sqrt_n_from_1000000": {
            "value": round(max_from_1m[0], 10),
            "n": max_from_1m[1],
            "mertens": max_from_1m[2],
        },
    }


def goldbach_first_witness_scan(prime_flags: bytearray, limit: int) -> dict[str, Any]:
    primes = [value for value in range(2, limit + 1) if prime_flags[value]]
    hardest = {"prime_scans_before_first_witness": 0, "even_n": None, "first_witness": None}
    checked = 0
    counterexample = None
    for even_n in range(4, limit + 1, 2):
        witness = None
        scans = 0
        for prime in primes:
            if prime > even_n // 2:
                break
            scans += 1
            if prime_flags[even_n - prime]:
                witness = [prime, even_n - prime]
                break
        if witness is None:
            counterexample = even_n
            break
        if scans > int(hardest["prime_scans_before_first_witness"]):
            hardest = {
                "prime_scans_before_first_witness": scans,
                "even_n": even_n,
                "first_witness": witness,
            }
        checked += 1
    return {
        "even_limit": limit,
        "checked_even_count": checked,
        "counterexample_found": counterexample,
        "no_counterexample_leq_limit": counterexample is None,
        "hardest_first_witness_row": hardest,
    }


def twin_prime_scan(prime_flags: bytearray, limit: int) -> dict[str, Any]:
    count = 0
    last_pair = None
    previous_start = None
    max_gap_between_starts = {"gap": 0, "from_start": None, "to_start": None}
    for prime in range(3, limit - 1, 2):
        if prime_flags[prime] and prime_flags[prime + 2]:
            count += 1
            last_pair = [prime, prime + 2]
            if previous_start is not None and prime - previous_start > int(max_gap_between_starts["gap"]):
                max_gap_between_starts = {
                    "gap": prime - previous_start,
                    "from_start": previous_start,
                    "to_start": prime,
                }
            previous_start = prime
    return {
        "prime_limit": limit,
        "twin_pair_count": count,
        "last_twin_pair_leq_limit": last_pair,
        "max_gap_between_twin_pair_starts": max_gap_between_starts,
        "largest_pair_certificate_is_not_a_proof": True,
    }


def riemann_attempt() -> dict[str, Any]:
    stress = mertens_stress(10_000_000)
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-29",
        "status": "proof_pressure_open",
        "route": "TailBridgeFrontier",
        "proof_or_counterexample_mode": "counterexample_or_tail_theorem_search",
        "attempt": (
            "Increase the finite RH-compatible stress observable and isolate the missing step: a theorem converting "
            "finite positivity or Mertens-type control into all-height zeta-zero control."
        ),
        "bounded_result": {
            "source_ticket": "RH-TICKET-28",
            "mertens_stress": stress,
            "direct_counterexample_route": "No certified off-critical zeta zero was produced.",
            "no_counterexample_route": "A full proof still requires a tail-uniform all-zero theorem.",
            "contrapositive_route": "An off-critical zero must imply a bounded failed positivity witness; that bridge is open.",
        },
        "obstruction": "Finite Mertens stress remains compatible with RH and cannot decide the zeta zero set.",
        "candidate_theorem": (
            "A formal tail bridge maps any off-critical zero to a finite positivity violation while controlling every "
            "remaining zero contribution."
        ),
        "next_experiment": "Search symbolic tail majorants that survive surrogate off-critical zero red-team tests.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_attempt() -> dict[str, Any]:
    adaptive = collatz_adaptive_split(base_bits=12, max_bits=28)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-29",
        "status": "proof_pressure_open",
        "route": "AdaptiveCylinderSplitTermination",
        "proof_or_counterexample_mode": "minimal_counterexample_contrapositive",
        "attempt": (
            "Attack the strongest Collatz route found so far: assume a minimal counterexample exists, then try to "
            "force it into an exact 2-adic cylinder that descends below its start. Ticket 29 expands only the "
            "needs_split frontier instead of enumerating the full modulus."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-28",
            "adaptive_cylinder_split": adaptive,
            "direct_counterexample_route": "No divergent orbit or non-trivial positive cycle was produced.",
            "no_counterexample_route": "Many exact lift families close by affine descent, but not all tested frontier states close.",
            "contrapositive_route": (
                "A minimal counterexample must remain inside the open adaptive frontier; proving this frontier "
                "eventually empties would close the route."
            ),
            "strongest_closed_statement": (
                "Every all_lift_descent state in the adaptive run is an exact cylinder whose every positive odd lift "
                "descends below its starting value."
            ),
        },
        "obstruction": (
            "At the tested depth, adaptive splitting leaves a large needs_split frontier. The naive split-until-closed "
            "strategy is therefore not a proof without a termination potential."
        ),
        "candidate_theorem": (
            "There is a well-founded valuation-debt potential on needs_split cylinders that strictly decreases after "
            "a bounded number of adaptive refinements."
        ),
        "next_experiment": "Synthesize and falsify candidate potentials on the Ticket 29 open frontier examples.",
        "claim_boundary": "No Collatz proof, no divergent orbit, and no non-trivial positive integer cycle found.",
    }


def goldbach_attempt(prime_flags: bytearray) -> dict[str, Any]:
    scan = goldbach_first_witness_scan(prime_flags, 5_000_000)
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-29",
        "status": "proof_pressure_open",
        "route": "LeastCounterexampleCutoffPressure",
        "proof_or_counterexample_mode": "finite_base_plus_tail_cutoff",
        "attempt": (
            "Extend the least-counterexample finite base and keep the proof obligation explicit: a larger finite "
            "base matters only if an analytic tail theorem forces every counterexample below it."
        ),
        "bounded_result": {
            "source_ticket": "GB-TICKET-28",
            "finite_witness_scan": scan,
            "direct_counterexample_route": "No Goldbach counterexample was found in the finite scan.",
            "no_counterexample_route": "The finite base must be paired with a positive representation lower bound above the cutoff.",
            "contrapositive_route": "A least counterexample N must be forced below the verified base by an explicit tail theorem.",
        },
        "obstruction": "The explicit large-even lower-bound theorem remains missing.",
        "candidate_theorem": (
            "For every even n>N0, the binary Goldbach representation count is positive, and N0<=5,000,000."
        ),
        "next_experiment": "Build a constant-complete main-term-minus-error ledger and reject ineffective exceptional-zero terms.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found up to the finite scan limit.",
    }


def twin_prime_attempt(prime_flags: bytearray) -> dict[str, Any]:
    scan = twin_prime_scan(prime_flags, 20_000_000)
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-29",
        "status": "proof_pressure_open",
        "route": "ExactGapTailPressure",
        "proof_or_counterexample_mode": "last_pair_contradiction_search",
        "attempt": (
            "Extend exact gap-2 finite evidence while keeping the last-pair contrapositive honest. A finite last "
            "observed pair is not a certified largest pair."
        ),
        "bounded_result": {
            "source_ticket": "TP-TICKET-28",
            "finite_exact_gap_scan": scan,
            "direct_counterexample_route": "No certified largest twin-prime pair was produced.",
            "no_counterexample_route": "Infinitude still requires an exact-gap-2 lower bound on arbitrarily large scales.",
            "contrapositive_route": "Assume a largest pair; force exact-gap-2 mass beyond it. The forcing theorem is open.",
        },
        "obstruction": "Finite exact-gap persistence does not prove infinitely many exact gap-2 pairs.",
        "candidate_theorem": (
            "A deletion-sensitive exact-gap-2 lower-bound functional remains positive on unbounded intervals."
        ),
        "next_experiment": "Search exact-gap functionals that collapse under gap-2 deletion but not under bounded-gap noise.",
        "claim_boundary": "No Twin Prime proof and no certified largest twin-prime pair.",
    }


def build_payload() -> dict[str, Any]:
    prime_flags = prime_sieve(20_000_000)
    attempts = [
        riemann_attempt(),
        collatz_attempt(),
        goldbach_attempt(prime_flags),
        twin_prime_attempt(prime_flags),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "adaptive_frontier_open_no_resolution",
        "claim_boundary": (
            "Ticket 29 pushes the counterexample/no-counterexample/contrapositive program one step further. It "
            "closes additional bounded evidence and exposes a sharper Collatz frontier, but it does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> None:
    payload = build_payload()
    output = ROOT / "data/open-problem/ticket29-adaptive-frontier-lab.json"
    write_json(output, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-29-tail-bridge-frontier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-29-adaptive-cylinder-split.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-29-least-counterexample-cutoff.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-29-exact-gap-tail-pressure.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem[attempt["problem_id"]], attempt)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
