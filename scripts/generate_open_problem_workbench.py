from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "primeproject.open-problem-workbench.v1"


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for factor in range(2, math.isqrt(limit) + 1):
        if is_prime[factor]:
            start = factor * factor
            is_prime[start : limit + 1 : factor] = b"\x00" * (((limit - start) // factor) + 1)
    return [number for number in range(2, limit + 1) if is_prime[number]], is_prime


def li_approx(x: int) -> float:
    if x < 3:
        return 0.0
    log_x = math.log(x)
    term = x / log_x
    total = term
    factorial = 1.0
    for k in range(1, 8):
        factorial *= k
        total += factorial * x / (log_x ** (k + 1))
    return total


def build_riemann(limit: int, primes: list[int]) -> dict[str, object]:
    checkpoints = [10**k for k in range(2, int(math.log10(limit)) + 1)]
    rows = []
    index = 0
    theta = 0.0
    max_scaled_theta_error = 0.0
    for x in checkpoints:
        while index < len(primes) and primes[index] <= x:
            theta += math.log(primes[index])
            index += 1
        pi_x = index
        li_x = li_approx(x)
        scaled_theta_error = abs(theta - x) / (math.sqrt(x) * (math.log(x) ** 2))
        max_scaled_theta_error = max(max_scaled_theta_error, scaled_theta_error)
        rows.append(
            {
                "x": x,
                "pi_x": pi_x,
                "li_approx": round(li_x, 3),
                "pi_minus_li_approx": round(pi_x - li_x, 3),
                "theta_minus_x": round(theta - x, 3),
                "scaled_theta_error": round(scaled_theta_error, 6),
            }
        )
    return {
        "id": "riemann",
        "title": "Riemann Hypothesis",
        "korean_title": "리만가설",
        "status": "open_not_proven",
        "target_statement": "All non-trivial zeros of the Riemann zeta function have real part 1/2.",
        "tool_position": "PrimeProject can test prime-counting error signatures and RH-compatible envelopes on finite ranges; it cannot turn finite checks into a proof.",
        "finite_result": {
            "limit": limit,
            "checkpoints": rows,
            "max_scaled_theta_error": round(max_scaled_theta_error, 6),
        },
        "proof_gates": [
            "Replace finite prime-counting evidence with a theorem controlling zeta zeros on the full critical strip.",
            "Prove an explicit equivalence strong enough to imply all non-trivial zeros lie on Re(s)=1/2.",
            "Show every numerical or symbolic step is independent of bounded search limits.",
        ],
        "candidate_strategy": [
            "Use generator-fingerprint residuals to look for structured departures from PNT-scale noise.",
            "Convert any stable residual law into a falsifiable analytic lemma before treating it as proof evidence.",
            "Reject any argument that only rephrases finite zero or finite prime-count checks.",
        ],
        "claim_boundary": "No proof claim. Current evidence is only finite RH-compatible diagnostics.",
    }


def build_collatz(limit: int) -> dict[str, object]:
    memo = {1: 0}
    max_steps = {"n": 1, "steps": 0}
    max_peak = {"n": 1, "peak": 1, "ratio": 1.0}

    def trajectory_stats(n: int) -> tuple[int, int]:
        original = n
        seen: list[int] = []
        peak = n
        while n not in memo:
            seen.append(n)
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            peak = max(peak, n)
        steps = memo[n]
        for value in reversed(seen):
            steps += 1
            if value <= limit:
                memo[value] = steps
        return memo[original], peak

    for n in range(2, limit + 1):
        steps, peak = trajectory_stats(n)
        if steps > max_steps["steps"]:
            max_steps = {"n": n, "steps": steps}
        ratio = peak / n
        if ratio > max_peak["ratio"]:
            max_peak = {"n": n, "peak": peak, "ratio": ratio}

    return {
        "id": "collatz",
        "title": "Collatz Conjecture",
        "korean_title": "콜라츠 추측",
        "status": "open_not_proven",
        "target_statement": "Repeatedly applying n/2 for even n and 3n+1 for odd n eventually reaches 1 for every positive integer.",
        "tool_position": "PrimeProject can exhaustively replay trajectories over a bounded range and search for divergent behavior; bounded replay is not a proof over all integers.",
        "finite_result": {
            "limit": limit,
            "tested_start_values": limit,
            "counterexamples": 0,
            "max_total_stopping_time": max_steps,
            "max_peak_ratio": {
                "n": max_peak["n"],
                "peak": max_peak["peak"],
                "ratio": round(max_peak["ratio"], 6),
            },
        },
        "proof_gates": [
            "Prove descent or recurrence for every congruence class without relying on finite enumeration.",
            "Rule out non-trivial cycles and divergent trajectories simultaneously.",
            "Turn stochastic drift intuition into a deterministic inequality with no exceptional infinite set.",
        ],
        "candidate_strategy": [
            "Compress trajectories by odd-only maps and residue-class transitions.",
            "Search for monotone certificates on blocks, then try to lift them to all blocks recursively.",
            "Treat random-walk drift evidence as heuristic until a deterministic certificate exists.",
        ],
        "claim_boundary": "No proof claim. Current evidence is finite exhaustive replay plus blocker list.",
    }


def build_goldbach(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    failures = []
    hardest = {"even": 4, "smallest_prime": 2, "partner": 2}
    decompositions = []
    for even in range(4, limit + 1, 2):
        found = None
        for p in primes:
            if p > even // 2:
                break
            if is_prime[even - p]:
                found = (p, even - p)
                break
        if found is None:
            failures.append(even)
            continue
        if found[0] > hardest["smallest_prime"]:
            hardest = {"even": even, "smallest_prime": found[0], "partner": found[1]}
        if even in {100, 1_000, 10_000, 100_000, limit}:
            decompositions.append({"even": even, "p": found[0], "q": found[1]})

    return {
        "id": "goldbach",
        "title": "Goldbach Conjecture",
        "korean_title": "골드바흐 추측",
        "status": "open_not_proven",
        "target_statement": "Every even integer greater than 2 is the sum of two primes.",
        "tool_position": "PrimeProject can verify every even value up to a chosen public limit and expose the hardest bounded cases; this is not an infinite proof.",
        "finite_result": {
            "limit": limit,
            "tested_even_values": max(0, (limit - 2) // 2),
            "counterexamples": len(failures),
            "first_failures": failures[:5],
            "hardest_smallest_prime_decomposition": hardest,
            "sample_decompositions": decompositions,
        },
        "proof_gates": [
            "Control prime coverage in every residue class strongly enough for all even integers.",
            "Bridge from verified finite range to an analytic theorem for the infinite tail.",
            "State explicit constants and thresholds so no unverified gap remains.",
        ],
        "candidate_strategy": [
            "Use residue-drift tools to detect classes where representations are thinnest.",
            "Compare bounded failures against Hardy-Littlewood-style expected representation counts.",
            "Escalate only if the thin-class model yields a provable lower bound above zero.",
        ],
        "claim_boundary": "No proof claim. Current evidence is bounded exhaustive verification.",
    }


def build_twin_prime(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    checkpoints = [10**k for k in range(2, int(math.log10(limit)) + 1)]
    checkpoint_index = 0
    count = 0
    largest_pair = None
    rows = []
    for p in primes:
        if p + 2 <= limit and is_prime[p + 2]:
            count += 1
            largest_pair = [p, p + 2]
        while checkpoint_index < len(checkpoints) and p >= checkpoints[checkpoint_index]:
            x = checkpoints[checkpoint_index]
            estimate = 2 * 0.6601618158468696 * x / (math.log(x) ** 2)
            rows.append({"x": x, "twin_pairs": count, "hardy_littlewood_estimate": round(estimate, 2)})
            checkpoint_index += 1
    while checkpoint_index < len(checkpoints):
        x = checkpoints[checkpoint_index]
        estimate = 2 * 0.6601618158468696 * x / (math.log(x) ** 2)
        rows.append({"x": x, "twin_pairs": count, "hardy_littlewood_estimate": round(estimate, 2)})
        checkpoint_index += 1

    return {
        "id": "twin-prime",
        "title": "Twin Prime Conjecture",
        "korean_title": "쌍둥이 소수 추측",
        "status": "open_not_proven",
        "target_statement": "There are infinitely many prime pairs p and p+2.",
        "tool_position": "PrimeProject can count twin pairs and compare them with heuristic density curves over finite ranges; unbounded infinitude remains the missing proof step.",
        "finite_result": {
            "limit": limit,
            "twin_pair_count": count,
            "largest_pair_seen": largest_pair,
            "checkpoints": rows,
        },
        "proof_gates": [
            "Prove infinitely many prime gaps of size exactly 2, not merely bounded gaps.",
            "Remove dependence on unproven distribution assumptions such as full Hardy-Littlewood k-tuple strength.",
            "Turn finite density persistence into a lower-bound theorem for all large x.",
        ],
        "candidate_strategy": [
            "Use wheel/residue drift measurements to isolate admissible two-point patterns.",
            "Stress-test whether observed twin density survives generator and modulus changes.",
            "Treat density agreement as a guide for lemma search, not as proof.",
        ],
        "claim_boundary": "No proof claim. Current evidence is finite counting and heuristic comparison.",
    }


def build_payload(limit: int) -> dict[str, object]:
    primes, is_prime = sieve(limit)
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "search_limit": limit,
        "claim_policy": {
            "public_claim": "proof_workbench_only",
            "reason": "These pages are allowed to show finite evidence, proof gates, and candidate strategies, but must not claim a proof until an independently checkable infinite argument exists.",
            "blocked_claims": [
                "Riemann Hypothesis proven",
                "Collatz Conjecture proven",
                "Goldbach Conjecture proven",
                "Twin Prime Conjecture proven",
            ],
        },
        "problems": [
            build_riemann(limit, primes),
            build_collatz(limit),
            build_goldbach(limit, primes, is_prime),
            build_twin_prime(limit, primes, is_prime),
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--output", type=Path, default=Path("data/open_problem_workbench.json"))
    args = parser.parse_args()

    payload = build_payload(args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
