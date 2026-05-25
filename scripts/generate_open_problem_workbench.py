from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "primeproject.open-problem-workbench.v1"
CERTIFICATE_SCHEMA = "primeproject.bounded-proof-certificate.v1"
PROOF_ATTEMPT_SCHEMA = "primeproject.proof-attempt-ledger.v1"


def hash_leaf(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merkle_root(hex_hashes: list[str]) -> str:
    if not hex_hashes:
        return hash_leaf("empty")
    layer = hex_hashes[:]
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        layer = [
            hashlib.sha256(bytes.fromhex(layer[index]) + bytes.fromhex(layer[index + 1])).hexdigest()
            for index in range(0, len(layer), 2)
        ]
    return layer[0]


class ChunkedCertificate:
    def __init__(self, *, problem_id: str, statement: str, limit: int, chunk_size: int = 10_000) -> None:
        self.problem_id = problem_id
        self.statement = statement
        self.limit = limit
        self.chunk_size = chunk_size
        self.current: list[str] = []
        self.chunk_roots: list[str] = []
        self.leaf_count = 0

    def update(self, text: str) -> None:
        self.current.append(hash_leaf(text))
        self.leaf_count += 1
        if len(self.current) >= self.chunk_size:
            self._flush()

    def _flush(self) -> None:
        if not self.current:
            return
        self.chunk_roots.append(merkle_root(self.current))
        self.current = []

    def finish(self) -> dict[str, object]:
        self._flush()
        return {
            "schema": CERTIFICATE_SCHEMA,
            "problem_id": self.problem_id,
            "claim_type": "bounded_theorem_certificate",
            "status": "bounded_theorem_certified",
            "statement": self.statement,
            "limit": self.limit,
            "leaf_count": self.leaf_count,
            "chunk_size": self.chunk_size,
            "chunk_count": len(self.chunk_roots),
            "leaf_encoding": "utf8 text, sha256 leaf, pairwise sha256 Merkle chunks",
            "chunk_roots": self.chunk_roots,
            "chunk_roots_sha256": hash_leaf("\n".join(self.chunk_roots)),
            "merkle_root": merkle_root(self.chunk_roots),
            "verifier": "scripts/verify_open_problem_workbench.py",
        }


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


def proof_attempt_ledger(
    *,
    problem_id: str,
    route: str,
    formal_statement: str,
    obligations: list[dict[str, str]],
    falsification_targets: list[str],
    attack_graph: dict[str, list[dict[str, str]]],
    known_theorem_bridges: list[dict[str, str]],
    lemma_candidates: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "schema": PROOF_ATTEMPT_SCHEMA,
        "problem_id": problem_id,
        "status": "open_infinite_obligation",
        "bounded_theorem_status": "proved_by_certificate",
        "attack_route": route,
        "attack_graph": attack_graph,
        "known_theorem_bridges": known_theorem_bridges,
        "lemma_candidates": lemma_candidates,
        "obligations": obligations,
        "falsification_targets": falsification_targets,
        "next_formalization_target": {
            "format": "lean_ready_statement",
            "statement": formal_statement,
            "status": "not_formalized",
        },
        "promotion_rule": "A page may move from open_not_proven only when every open obligation is replaced by an independently checkable proof that does not depend on the search limit.",
    }


def build_riemann(limit: int, primes: list[int]) -> dict[str, object]:
    checkpoints = [10**k for k in range(2, int(math.log10(limit)) + 1)]
    rows = []
    index = 0
    theta = 0.0
    max_scaled_theta_error = 0.0
    certificate = ChunkedCertificate(
        problem_id="riemann",
        statement=f"Prime-counting diagnostics are exactly recomputed at decimal checkpoints up to {limit}.",
        limit=limit,
    )
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
        certificate.update(json.dumps(rows[-1], sort_keys=True, separators=(",", ":")))
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
        "certificate": certificate.finish(),
        "proof_attempt": proof_attempt_ledger(
            problem_id="riemann",
            route="Prime-counting residuals -> explicit theta(x) envelope -> zero-free critical-strip control strong enough for RH.",
            formal_statement="For every non-trivial zero rho of zeta, Re(rho) = 1/2.",
            obligations=[
                {
                    "id": "RH-O1",
                    "claim": "Bounded theta/pi diagnostics are exactly reproducible.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "Merkle root mismatch or changed checkpoint row.",
                },
                {
                    "id": "RH-O2",
                    "claim": "Find an explicit residual bound valid for all x beyond a finite threshold.",
                    "status": "open_obligation",
                    "verifier": "analytic proof required",
                    "failure_mode": "A residual spike violates the proposed global envelope.",
                },
                {
                    "id": "RH-O3",
                    "claim": "Show the global envelope implies all non-trivial zeros lie on the critical line.",
                    "status": "open_obligation",
                    "verifier": "formal theorem or accepted analytic derivation",
                    "failure_mode": "The envelope is weaker than a known RH-equivalent condition.",
                },
            ],
            falsification_targets=[
                "A proposed all-x theta bound fails on a computed checkpoint.",
                "The bound does not imply a published RH-equivalent criterion.",
                "The argument depends on a finite zero table without an infinite tail theorem.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "rh-finite", "label": "Bounded theta/pi certificate", "status": "proved_by_certificate"},
                    {"id": "rh-envelope", "label": "Explicit all-x theta envelope", "status": "open_bridge"},
                    {"id": "rh-equivalence", "label": "RH-equivalent zero-control criterion", "status": "known_bridge_needed"},
                    {"id": "rh-target", "label": "All non-trivial zeros on Re(s)=1/2", "status": "open_target"},
                ],
                "edges": [
                    {"from": "rh-finite", "to": "rh-envelope", "status": "open_bridge", "label": "remove search limit"},
                    {"from": "rh-envelope", "to": "rh-equivalence", "status": "open_bridge", "label": "prove criterion strength"},
                    {"from": "rh-equivalence", "to": "rh-target", "status": "open_bridge", "label": "formal implication"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "RH-B1",
                    "name": "Prime-counting error equivalences",
                    "role": "Identify an explicit error envelope strong enough to imply RH.",
                    "status": "bridge_not_satisfied",
                },
                {
                    "id": "RH-B2",
                    "name": "Zero-free region machinery",
                    "role": "Convert analytic estimates into critical-strip zero control.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "RH-L1",
                    "statement": "There exists an explicit C such that |theta(x)-x| <= C sqrt(x) log(x)^2 for all x >= x0.",
                    "evidence": "Finite checkpoints are below the normalized envelope through the committed limit.",
                    "required_upgrade": "Prove the inequality for the infinite tail and show constants meet an RH-equivalent bound.",
                    "status": "open_candidate",
                }
            ],
        ),
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
    certificate = ChunkedCertificate(
        problem_id="collatz",
        statement=f"Every start value 1 <= n <= {limit} reaches 1 under the Collatz map.",
        limit=limit,
    )

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

    certificate.update("1:0:1")
    for n in range(2, limit + 1):
        steps, peak = trajectory_stats(n)
        certificate.update(f"{n}:{steps}:{peak}")
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
        "certificate": certificate.finish(),
        "proof_attempt": proof_attempt_ledger(
            problem_id="collatz",
            route="Odd-only accelerated map -> residue-block descent certificate -> recursive coverage of every positive integer.",
            formal_statement="For every positive integer n, some iterate of the Collatz map reaches 1.",
            obligations=[
                {
                    "id": "C-O1",
                    "claim": "Every n <= 1,000,000 reaches 1 under the Collatz map.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "A trajectory leaf changes or a non-reaching start value appears.",
                },
                {
                    "id": "C-O2",
                    "claim": "Construct residue-block descent certificates that cover all sufficiently large blocks.",
                    "status": "open_obligation",
                    "verifier": "deterministic descent proof required",
                    "failure_mode": "An uncovered block has no guaranteed descent path.",
                },
                {
                    "id": "C-O3",
                    "claim": "Rule out divergent trajectories and non-trivial cycles simultaneously.",
                    "status": "open_obligation",
                    "verifier": "cycle and divergence exclusion theorem",
                    "failure_mode": "A cycle or non-descending infinite branch remains possible.",
                },
            ],
            falsification_targets=[
                "A residue block cannot be assigned a monotone descent certificate.",
                "A proposed drift inequality admits an infinite exceptional set.",
                "Odd-only compression silently loses a valid trajectory branch.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "c-finite", "label": "Bounded trajectory certificate", "status": "proved_by_certificate"},
                    {"id": "c-blocks", "label": "Residue-block descent family", "status": "open_bridge"},
                    {"id": "c-coverage", "label": "Recursive all-block coverage", "status": "open_bridge"},
                    {"id": "c-target", "label": "Every positive integer reaches 1", "status": "open_target"},
                ],
                "edges": [
                    {"from": "c-finite", "to": "c-blocks", "status": "open_bridge", "label": "generalize finite descent"},
                    {"from": "c-blocks", "to": "c-coverage", "status": "open_bridge", "label": "cover all residue blocks"},
                    {"from": "c-coverage", "to": "c-target", "status": "open_bridge", "label": "exclude cycles/divergence"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "C-B1",
                    "name": "Accelerated odd Collatz map",
                    "role": "Reduce even divisions while preserving every trajectory branch.",
                    "status": "usable_but_insufficient",
                },
                {
                    "id": "C-B2",
                    "name": "Descent certificate induction",
                    "role": "Turn residue-block certificates into a global well-founded descent argument.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "C-L1",
                    "statement": "Every odd residue block modulo 2^a 3^b has a finite accelerated path to a smaller representative in a covered block.",
                    "evidence": "Bounded replay identifies many descending trajectories and worst stopping-time cases.",
                    "required_upgrade": "Construct a finite symbolic block cover with an induction measure that cannot increase forever.",
                    "status": "open_candidate",
                }
            ],
        ),
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
    certificate = ChunkedCertificate(
        problem_id="goldbach",
        statement=f"Every even integer 4 <= n <= {limit} has a displayed prime-pair witness.",
        limit=limit,
    )
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
            certificate.update(f"{even}:fail")
            continue
        certificate.update(f"{even}:{found[0]}:{found[1]}")
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
        "certificate": certificate.finish(),
        "proof_attempt": proof_attempt_ledger(
            problem_id="goldbach",
            route="Exhaustive bounded witnesses -> thinnest residue-class model -> explicit positive lower bound for all even n.",
            formal_statement="For every even integer n > 2, there exist primes p and q such that n = p + q.",
            obligations=[
                {
                    "id": "G-O1",
                    "claim": "Every even n <= 1,000,000 has a prime-pair witness.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "A witness leaf changes or an even n has no pair.",
                },
                {
                    "id": "G-O2",
                    "claim": "Prove a positive representation-count lower bound for all even n above a threshold.",
                    "status": "open_obligation",
                    "verifier": "explicit analytic lower-bound proof",
                    "failure_mode": "A thin residue class has no proven positive lower bound.",
                },
                {
                    "id": "G-O3",
                    "claim": "Bridge the analytic threshold to the bounded certified range with no gap.",
                    "status": "open_obligation",
                    "verifier": "threshold comparison against certificate limit",
                    "failure_mode": "The analytic theorem starts above the certified range.",
                },
            ],
            falsification_targets=[
                "A proposed lower bound becomes non-positive for a residue class.",
                "The threshold exceeds the certified finite range.",
                "The model assumes unproved prime-pair independence.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "g-finite", "label": "Bounded witness certificate", "status": "proved_by_certificate"},
                    {"id": "g-thin", "label": "Thinnest residue-class lower bound", "status": "open_bridge"},
                    {"id": "g-threshold", "label": "Explicit threshold below certificate limit", "status": "open_bridge"},
                    {"id": "g-target", "label": "Every even n > 2 has p+q witness", "status": "open_target"},
                ],
                "edges": [
                    {"from": "g-finite", "to": "g-threshold", "status": "open_bridge", "label": "close finite/infinite gap"},
                    {"from": "g-thin", "to": "g-threshold", "status": "open_bridge", "label": "make lower bound positive"},
                    {"from": "g-threshold", "to": "g-target", "status": "open_bridge", "label": "cover all even values"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "G-B1",
                    "name": "Circle-method lower bounds",
                    "role": "Supply explicit positive representation counts for all large even integers.",
                    "status": "bridge_not_satisfied",
                },
                {
                    "id": "G-B2",
                    "name": "Finite verification threshold bridge",
                    "role": "Ensure the analytic threshold does not start above the certified finite range.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "G-L1",
                    "statement": "For every even n >= N, the Goldbach representation count R(n) is strictly positive with explicit N <= certificate_limit.",
                    "evidence": "Bounded witness search shows no failures and records hardest smallest-prime decompositions.",
                    "required_upgrade": "Derive explicit constants that beat all singular-series and error-term losses.",
                    "status": "open_candidate",
                }
            ],
        ),
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
    certificate = ChunkedCertificate(
        problem_id="twin-prime",
        statement=f"All twin prime pairs p,p+2 with p+2 <= {limit} are counted by the sieve scan.",
        limit=limit,
    )
    for p in primes:
        if p + 2 <= limit and is_prime[p + 2]:
            count += 1
            largest_pair = [p, p + 2]
            certificate.update(f"{p}:{p + 2}")
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
        "certificate": certificate.finish(),
        "proof_attempt": proof_attempt_ledger(
            problem_id="twin-prime",
            route="Certified finite twin pairs -> admissible two-point pattern analysis -> lower-bound theorem for exact gap 2.",
            formal_statement="For infinitely many primes p, p + 2 is also prime.",
            obligations=[
                {
                    "id": "TP-O1",
                    "claim": "Every twin prime pair p,p+2 with p+2 <= 1,000,000 is counted by the sieve scan.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "The pair list Merkle root changes or a pair is missed.",
                },
                {
                    "id": "TP-O2",
                    "claim": "Prove infinitely many exact prime gaps of size 2, not only bounded gaps.",
                    "status": "open_obligation",
                    "verifier": "exact gap-2 infinitude theorem",
                    "failure_mode": "The proof only gives a bounded gap larger than 2.",
                },
                {
                    "id": "TP-O3",
                    "claim": "Remove dependence on unproved Hardy-Littlewood k-tuple assumptions.",
                    "status": "open_obligation",
                    "verifier": "assumption-free lower-bound proof",
                    "failure_mode": "The density argument remains heuristic.",
                },
            ],
            falsification_targets=[
                "The lower bound collapses to zero for exact gap 2.",
                "The argument proves bounded gaps but cannot force gap 2.",
                "An admissible-pattern step assumes the k-tuple conjecture.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "tp-finite", "label": "Bounded twin-pair certificate", "status": "proved_by_certificate"},
                    {"id": "tp-pattern", "label": "Admissible two-point lower bound", "status": "open_bridge"},
                    {"id": "tp-exact", "label": "Exact gap-2 infinitude theorem", "status": "open_bridge"},
                    {"id": "tp-target", "label": "Infinitely many twin primes", "status": "open_target"},
                ],
                "edges": [
                    {"from": "tp-finite", "to": "tp-pattern", "status": "open_bridge", "label": "lift density beyond finite range"},
                    {"from": "tp-pattern", "to": "tp-exact", "status": "open_bridge", "label": "force exact gap 2"},
                    {"from": "tp-exact", "to": "tp-target", "status": "open_bridge", "label": "prove infinitude"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "TP-B1",
                    "name": "Bounded prime gaps",
                    "role": "Existing methods prove some bounded gaps, but not exact gap 2.",
                    "status": "usable_but_insufficient",
                },
                {
                    "id": "TP-B2",
                    "name": "Hardy-Littlewood k-tuple heuristic",
                    "role": "Predicts the right density but cannot be used as an assumption-free proof.",
                    "status": "heuristic_only",
                },
            ],
            lemma_candidates=[
                {
                    "id": "TP-L1",
                    "statement": "There is an explicit c > 0 such that pi_2(x) >= c x / log(x)^2 for arbitrarily large x without k-tuple assumptions.",
                    "evidence": "Bounded counts track the Hardy-Littlewood scale through the committed limit.",
                    "required_upgrade": "Replace the heuristic density curve with an unconditional lower-bound theorem for exact gap 2.",
                    "status": "open_candidate",
                }
            ],
        ),
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


def build_payload(limit: int, *, generated_at: str | None = None) -> dict[str, object]:
    primes, is_prime = sieve(limit)
    return {
        "schema": SCHEMA,
        "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
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
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--output", type=Path, default=Path("data/open_problem_workbench.json"))
    args = parser.parse_args()

    payload = build_payload(args.limit, generated_at=args.generated_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
