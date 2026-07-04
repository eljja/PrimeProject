from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket17-breakthrough-attempts.v1"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [n for n in range(2, limit + 1) if is_prime[n]], is_prime


def accelerated_odd_step(n: int) -> tuple[int, int]:
    value = 3 * n + 1
    valuation = 0
    while value % 2 == 0:
        value //= 2
        valuation += 1
    return value, valuation


def riemann_uniform_detector(li_terms: int) -> dict[str, object]:
    heights = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513]
    beta_values = [0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    detector_rows = []
    undetected = []

    for beta in beta_values:
      for height in heights:
        zeros: list[complex] = []
        for critical_height in heights:
            zeros.extend([complex(0.5, critical_height), complex(0.5, -critical_height)])
        zeros.extend(
            [
                complex(beta, height),
                complex(1.0 - beta, height),
                complex(beta, -height),
                complex(1.0 - beta, -height),
            ]
        )
        first_negative = None
        min_li = None
        min_li_index = None
        for n in range(1, li_terms + 1):
            value = sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros)
            if min_li is None or value < min_li:
                min_li = value
                min_li_index = n
            if value < 0 and first_negative is None:
                first_negative = {"n": n, "lambda_n": round(value, 12)}
        row = {
            "beta": beta,
            "height": height,
            "terms_checked": li_terms,
            "first_negative_li": first_negative,
            "min_li": round(float(min_li or 0.0), 12),
            "min_li_index": min_li_index,
        }
        detector_rows.append(row)
        if first_negative is None:
            undetected.append(row)

    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-17",
        "status": "breakthrough_attempt_open",
        "route": "UniformOffCriticalDetector",
        "proof_or_counterexample_mode": "contrapositive_detector_search",
        "attempt": (
            "Assume an off-critical zero exists and search for an effective Li-type detector. "
            "The computation tests whether bounded Li prefixes expose symmetric off-critical surrogate quartets."
        ),
        "bounded_result": {
            "li_terms_checked": li_terms,
            "surrogate_models": len(detector_rows),
            "undetected_models": len(undetected),
            "detector_rows": detector_rows,
        },
        "obstruction": (
            "A finite detector can miss off-critical surrogate models. A proof needs an all-index theorem or an "
            "effective bound forcing a negative Li-type witness from any off-critical zero."
        ),
        "candidate_theorem": (
            "For every zero rho with Re(rho) != 1/2, there exists an explicitly bounded n <= F(rho) such that "
            "a Li/kernel detector is negative, with F usable uniformly in the explicit formula."
        ),
        "next_experiment": "Search for an effective F(beta, gamma) from detector latency over larger surrogate families.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_residue_debt_lift(limit: int, modulus: int, block_steps: int) -> dict[str, object]:
    direct_failures = []
    residue_worst: dict[int, dict[str, object]] = {}
    for start in range(3, limit + 1, 2):
        x = start
        max_debt = 0.0
        total_drift = 0.0
        descended_at = None
        path = []
        for step in range(1, block_steps + 1):
            nxt, valuation = accelerated_odd_step(x)
            drift = math.log(nxt / x)
            total_drift += drift
            max_debt = max(max_debt, total_drift)
            path.append({"from": x, "to": nxt, "v2": valuation, "drift": round(drift, 8)})
            x = nxt
            if x < start:
                descended_at = step
                break
        if descended_at is None:
            direct_failures.append({"start": start, "end": x, "steps": block_steps, "path_prefix": path[:8]})

        residue = start % modulus
        current = residue_worst.get(residue)
        record = {
            "start": start,
            "descended_at": descended_at,
            "max_debt": round(max_debt, 8),
            "end": x,
        }
        if current is None or record["max_debt"] > current["max_debt"]:
            residue_worst[residue] = record

    worst_residues = sorted(
        [{"residue": residue, **record} for residue, record in residue_worst.items()],
        key=lambda row: (row["descended_at"] is None, row["max_debt"]),
        reverse=True,
    )
    candidate_survives = not direct_failures

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-17",
        "status": "breakthrough_attempt_open",
        "route": "ResidueDebtAutomatonLift",
        "proof_or_counterexample_mode": "bounded_counterexample_search_plus_lift_target",
        "attempt": (
            "Track accumulated accelerated-map log debt until the odd trajectory descends below its start. "
            "A future theorem must turn finite residue-debt descent into a global well-founded rank."
        ),
        "bounded_result": {
            "odd_starts_checked": max((limit - 1) // 2, 0),
            "modulus": modulus,
            "block_steps": block_steps,
            "non_descending_blocks": len(direct_failures),
            "sample_failures": direct_failures[:12],
            "worst_residue_debt": worst_residues[:16],
        },
        "obstruction": (
            "Sampled descent is not a proof. The missing step is a lifting theorem showing that every representative "
            "inside a residue-debt state follows a certified descending block or enters the known basin."
        ),
        "candidate_theorem": (
            "There exists a finite residue-debt automaton whose every SCC has strictly negative certified block drift; "
            "therefore no divergent Collatz orbit or non-trivial cycle can remain outside the basin."
        ),
        "next_experiment": "Replace sampled starts with interval arithmetic over residue-debt states and certify every transition.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_residue_profile_cutoff(limit: int, primes: list[int]) -> dict[str, object]:
    counts = [0] * (limit + 1)
    for i, p in enumerate(primes):
        for q in primes[i:]:
            total = p + q
            if total > limit:
                break
            if total % 2 == 0:
                counts[total] += 1

    thresholds = [100, 1_000, 10_000, 50_000]
    profile_rows = []
    direct_counterexamples = [n for n in range(4, limit + 1, 2) if counts[n] == 0]
    for residue in range(0, 30, 2):
        values = [n for n in range(6, limit + 1, 2) if n % 30 == residue]
        row = {"mod30": residue}
        for threshold in thresholds:
            eligible = [n for n in values if n >= threshold]
            if not eligible:
                continue
            worst_n = min(eligible, key=lambda n: counts[n] / (n / (math.log(n) ** 2)))
            scale = worst_n / (math.log(worst_n) ** 2)
            row[f"min_margin_after_{threshold}"] = {
                "n": worst_n,
                "representations": counts[worst_n],
                "normalized_margin": round(counts[worst_n] / scale, 8),
            }
        profile_rows.append(row)

    weakest_profile = min(
        profile_rows,
        key=lambda row: row.get("min_margin_after_50000", {}).get("normalized_margin", float("inf")),
    )

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-17",
        "status": "breakthrough_attempt_open",
        "route": "ResidueProfileExplicitCutoff",
        "proof_or_counterexample_mode": "direct_counterexample_search_plus_profile_lower_envelope",
        "attempt": (
            "Search direct Goldbach counterexamples and profile the weakest residue classes for an explicit "
            "finite-to-infinite cutoff theorem."
        ),
        "bounded_result": {
            "even_limit": limit,
            "direct_counterexamples": direct_counterexamples[:20],
            "direct_counterexample_count": len(direct_counterexamples),
            "profile_lower_envelopes": profile_rows,
            "weakest_profile_after_50000": weakest_profile,
        },
        "obstruction": (
            "Positive finite margins do not give a large-even theorem. The required proof must dominate major/minor "
            "arc and exceptional-character errors for every residue profile."
        ),
        "candidate_theorem": (
            "For each even residue profile modulo 30, an explicit positive lower envelope for R(n) holds for all "
            "n >= N0(profile), and every N0(profile) is below the finite certificate range."
        ),
        "next_experiment": "Attach sourced explicit analytic error terms to each residue-profile envelope.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found in the bounded range.",
    }


def twin_exact_gap_projection(limit: int, primes: list[int], is_prime: bytearray, max_gap: int) -> dict[str, object]:
    gap_counts = Counter()
    for p, q in zip(primes, primes[1:]):
        gap = q - p
        if gap <= max_gap:
            gap_counts[gap] += 1

    exact = gap_counts.get(2, 0)
    wider = sum(count for gap, count in gap_counts.items() if 4 <= gap <= max_gap)
    suppression_needed = exact / wider if wider else 1.0
    checkpoints = []
    for checkpoint in [1_000, 10_000, 50_000, 100_000, limit]:
        if checkpoint > limit:
            continue
        local_primes = [p for p in primes if p <= checkpoint]
        local_counts = Counter()
        for p, q in zip(local_primes, local_primes[1:]):
            gap = q - p
            if gap <= max_gap:
                local_counts[gap] += 1
        local_exact = local_counts.get(2, 0)
        local_wider = sum(count for gap, count in local_counts.items() if 4 <= gap <= max_gap)
        checkpoints.append(
            {
                "x": checkpoint,
                "exact_gap_2": local_exact,
                "wider_bounded_gaps": local_wider,
                "required_wider_suppression": round(local_exact / local_wider, 8) if local_wider else None,
            }
        )

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-17",
        "status": "breakthrough_attempt_open",
        "route": "ExactGapTwoProjection",
        "proof_or_counterexample_mode": "proof_shortcut_counterexample_plus_projection_target",
        "attempt": (
            "Quantify how much a sieve weight must suppress wider bounded gaps before a bounded-gap signal can "
            "be converted into an exact gap-2 lower-bound candidate."
        ),
        "bounded_result": {
            "prime_limit": limit,
            "max_gap": max_gap,
            "gap_distribution": {str(gap): gap_counts[gap] for gap in sorted(gap_counts)},
            "exact_gap_2": exact,
            "wider_bounded_gaps": wider,
            "required_wider_suppression": round(suppression_needed, 8),
            "checkpoints": checkpoints,
        },
        "obstruction": (
            "Bounded gaps are dominated by wider gaps. Any proof route must create an exact-gap projection that "
            "survives parity models and does not assume Hardy-Littlewood k-tuple behavior."
        ),
        "candidate_theorem": (
            "There exists a non-negative sieve projection whose exact gap-2 contribution remains positive after all "
            "wider admissible gap contributions are subtracted with certified error control."
        ),
        "next_experiment": "Search signed/orthogonalized gap projection weights and reject those that fail parity-model tests.",
        "claim_boundary": "No Twin Prime proof. Finite data cannot refute the eventual no-more-twins negation.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max(args.goldbach_limit, args.twin_limit)
    primes, is_prime = sieve(prime_limit)
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "breakthrough_attempts_open_no_resolution",
        "claim_boundary": "Ticket 17 attempts sharpen proof or counterexample routes; they do not solve any open problem.",
        "attempts": [
            riemann_uniform_detector(args.riemann_li_terms),
            collatz_residue_debt_lift(args.collatz_limit, args.collatz_modulus, args.collatz_block_steps),
            goldbach_residue_profile_cutoff(args.goldbach_limit, [p for p in primes if p <= args.goldbach_limit]),
            twin_exact_gap_projection(args.twin_limit, [p for p in primes if p <= args.twin_limit], is_prime, args.twin_max_gap),
        ],
    }
    return payload


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-17-uniform-offcritical-detector.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-17-residue-debt-automaton-lift.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-17-residue-profile-explicit-cutoff.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-17-exact-gap-two-projection.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 17 breakthrough attempts for four open problems.")
    parser.add_argument("--riemann-li-terms", type=int, default=200)
    parser.add_argument("--collatz-limit", type=int, default=200_000)
    parser.add_argument("--collatz-modulus", type=int, default=128)
    parser.add_argument("--collatz-block-steps", type=int, default=64)
    parser.add_argument("--goldbach-limit", type=int, default=200_000)
    parser.add_argument("--twin-limit", type=int, default=300_000)
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket17-breakthrough-attempts.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket17 breakthrough attempts written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
