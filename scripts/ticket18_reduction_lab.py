from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket18-reduction-lab.v1"
TWIN_C2 = 0.6601618158468696


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


def factor_distinct(n: int, primes: list[int]) -> list[int]:
    factors: list[int] = []
    value = n
    for p in primes:
        if p * p > value:
            break
        if value % p == 0:
            factors.append(p)
            while value % p == 0:
                value //= p
    if value > 1:
        factors.append(value)
    return factors


def valuation_word_constant(word: tuple[int, ...]) -> tuple[int, int]:
    shift = 0
    constant = 0
    for step_index, valuation in enumerate(word):
        constant = 3 * constant + (1 << shift)
        shift += valuation
        if step_index < 0:
            raise AssertionError("unreachable")
    return shift, constant


def compositions(total: int, parts: int, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    if parts == 1:
        return [prefix + (total,)]
    rows: list[tuple[int, ...]] = []
    remaining_parts = parts - 1
    for first in range(1, total - remaining_parts + 1):
        rows.extend(compositions(total - first, remaining_parts, prefix + (first,)))
    return rows


def riemann_finite_prefix_camouflage(max_n: int, beta_values: list[float], heights: list[float]) -> dict[str, object]:
    rows = []
    best = None
    for beta in beta_values:
        for height in heights:
            zeros = [
                complex(beta, height),
                complex(1.0 - beta, height),
                complex(beta, -height),
                complex(1.0 - beta, -height),
            ]
            contributions = []
            for n in range(1, max_n + 1):
                value = sum((1.0 - (1.0 - 1.0 / rho) ** n).real for rho in zeros)
                contributions.append(value)
            max_abs = max(abs(value) for value in contributions)
            min_value = min(contributions)
            max_value = max(contributions)
            row = {
                "beta": beta,
                "height": height,
                "terms_checked": max_n,
                "max_abs_li_prefix_contribution": round(max_abs, 12),
                "min_li_prefix_contribution": round(min_value, 12),
                "max_li_prefix_contribution": round(max_value, 12),
            }
            rows.append(row)
            if best is None or max_abs < best["max_abs_li_prefix_contribution"]:
                best = row

    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-18",
        "status": "reduction_attempt_open",
        "route": "FinitePrefixCamouflage",
        "proof_or_counterexample_mode": "proof_shortcut_countermodel",
        "attempt": (
            "Attack finite Li-prefix proof routes by placing surrogate off-critical zero quartets at high height. "
            "For any bounded prefix, high-height off-critical zeros can have very small visible effect on those terms."
        ),
        "bounded_result": {
            "li_terms_checked": max_n,
            "surrogate_quartets": len(rows),
            "best_camouflage": best,
            "camouflage_rows": rows,
        },
        "obstruction": (
            "A proof cannot certify RH from any fixed finite Li/Jensen/Hermite prefix unless it adds a separate "
            "tail theorem controlling all unseen zeros and all higher coefficients."
        ),
        "candidate_theorem": (
            "If an off-critical zeta zero exists, an all-index detector or explicit-formula functional must produce "
            "a contradiction with a bound uniform in height; finite prefix positivity alone is disallowed."
        ),
        "next_experiment": "Search for a height-uniform detector bound rather than increasing a finite prefix.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_valuation_branch_cover(steps: int, max_shift: int) -> dict[str, object]:
    threshold = steps * math.log2(3)
    total_density = 0.0
    contracting_density = 0.0
    expanding_density = 0.0
    branch_count = 0
    contracting_count = 0
    expanding_count = 0
    worst_thresholds = []
    worst_expanding = []

    for total_shift in range(steps, max_shift + 1):
        for word in compositions(total_shift, steps):
            shift, constant = valuation_word_constant(word)
            if shift != total_shift:
                raise AssertionError("valuation word shift mismatch")
            weight = 2.0 ** (-shift)
            total_density += weight
            branch_count += 1
            multiplier_contracts = (1 << shift) > (3**steps)
            if multiplier_contracts:
                contracting_count += 1
                contracting_density += weight
                descent_threshold = constant / ((1 << shift) - (3**steps))
                worst_thresholds.append((descent_threshold, word, shift, constant, weight))
            else:
                expanding_count += 1
                expanding_density += weight
                worst_expanding.append((shift - threshold, word, shift, constant, weight))

    worst_thresholds.sort(reverse=True, key=lambda item: item[0])
    worst_expanding.sort(key=lambda item: item[0])
    tail_density = max(0.0, 1.0 - total_density)

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-18",
        "status": "reduction_attempt_open",
        "route": "ExactValuationBranchCover",
        "proof_or_counterexample_mode": "exact_branch_reduction_plus_open_lift",
        "attempt": (
            "Replace sampled Collatz starts with exact accelerated valuation words. Each valuation word gives an "
            "affine branch T^k(n)=(3^k n + c)/2^a and a precise descent condition."
        ),
        "bounded_result": {
            "odd_accelerated_steps": steps,
            "max_total_valuation_shift": max_shift,
            "branch_count_enumerated": branch_count,
            "density_enumerated": round(total_density, 12),
            "tail_density_not_enumerated": round(tail_density, 12),
            "contracting_branch_count": contracting_count,
            "expanding_branch_count": expanding_count,
            "contracting_density": round(contracting_density, 12),
            "expanding_density": round(expanding_density, 12),
            "contraction_threshold_total_shift": round(threshold, 8),
            "largest_descent_thresholds": [
                {
                    "threshold_n_greater_than": round(value, 6),
                    "valuation_word": list(word),
                    "total_shift": shift,
                    "affine_constant": constant,
                    "density_weight": round(weight, 12),
                }
                for value, word, shift, constant, weight in worst_thresholds[:10]
            ],
            "most_expanding_words": [
                {
                    "shift_minus_log2_3k": round(delta, 8),
                    "valuation_word": list(word),
                    "total_shift": shift,
                    "affine_constant": constant,
                    "density_weight": round(weight, 12),
                }
                for delta, word, shift, constant, weight in worst_expanding[:10]
            ],
        },
        "obstruction": (
            "Many finite valuation branches contract only after a threshold, while expanding branches must be routed "
            "into later contracting branches. The missing proof is a well-founded global branch graph, not more samples."
        ),
        "candidate_theorem": (
            "A finite exact valuation-branch graph exists in which every expanding branch reaches a lower-ranked "
            "contracting branch or a verified smaller basin, excluding divergent or cyclic Collatz behavior."
        ),
        "next_experiment": "Build the branch graph between valuation words and search for a strict ordinal-valued rank.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_explicit_error_budget(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    counts = [0] * (limit + 1)
    prime_list = [p for p in primes if p <= limit]
    for i, p in enumerate(prime_list):
        for q in prime_list[i:]:
            total = p + q
            if total > limit:
                break
            if total % 2 == 0:
                counts[total] += 1

    factor_primes = [p for p in primes if p * p <= limit]
    rows = []
    direct_counterexamples = []
    for n in range(4, limit + 1, 2):
        if counts[n] == 0:
            direct_counterexamples.append(n)
            continue
        if n < 32:
            continue
        singular_multiplier = 1.0
        for factor in factor_distinct(n, factor_primes):
            if factor > 2:
                singular_multiplier *= (factor - 1) / (factor - 2)
        estimate = TWIN_C2 * singular_multiplier * n / (math.log(n) ** 2)
        ratio = counts[n] / estimate if estimate > 0 else float("inf")
        rows.append(
            {
                "n": n,
                "mod30": n % 30,
                "representations": counts[n],
                "hl_unordered_estimate": round(estimate, 8),
                "observed_to_estimate_ratio": round(ratio, 8),
            }
        )

    weakest_by_profile = []
    for residue in range(0, 30, 2):
        profile_rows = [row for row in rows if row["mod30"] == residue and row["n"] >= 1000]
        if profile_rows:
            weakest_by_profile.append(min(profile_rows, key=lambda row: row["observed_to_estimate_ratio"]))
    weakest_global = min(rows, key=lambda row: row["observed_to_estimate_ratio"]) if rows else None

    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-18",
        "status": "reduction_attempt_open",
        "route": "ExplicitErrorBudget",
        "proof_or_counterexample_mode": "finite_certificate_plus_error_budget",
        "attempt": (
            "Turn finite Goldbach counts into an analytic proof target by measuring how much explicit major/minor-arc "
            "error a profile-wise lower-bound theorem would need to beat."
        ),
        "bounded_result": {
            "even_limit": limit,
            "direct_counterexamples": direct_counterexamples[:20],
            "direct_counterexample_count": len(direct_counterexamples),
            "weakest_global_ratio": weakest_global,
            "weakest_ratio_by_mod30_profile": weakest_by_profile,
            "required_error_budget_rule": (
                "For each residue profile, a sourced explicit lower-bound theorem must keep total analytic error "
                "below the displayed observed-to-estimate margin before the finite certificate can close the range."
            ),
        },
        "obstruction": (
            "Observed positive margins are not analytic lower bounds. The proof still needs explicit constants that "
            "dominate all exceptional-character, minor-arc, and sieve losses for every sufficiently large even n."
        ),
        "candidate_theorem": (
            "There are explicit constants N0(profile) and epsilon(profile)>0 such that R(n) >= epsilon(profile) "
            "n/log(n)^2 for all even n in that profile above N0, with N0 below the finite certificate limit."
        ),
        "next_experiment": "Attach verifiable published explicit constants and compute whether their N0 falls below the certificate range.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found in the bounded range.",
    }


def twin_bounded_gap_countermodel(limit: int, primes: list[int], max_gap: int) -> dict[str, object]:
    prime_set = set(primes)
    original_gap_counts = Counter()
    for p, q in zip(primes, primes[1:]):
        gap = q - p
        if gap <= max_gap:
            original_gap_counts[gap] += 1

    deleted = {p + 2 for p in primes if p + 2 in prime_set}
    model_primes = [p for p in primes if p not in deleted]
    model_gap_counts = Counter()
    for p, q in zip(model_primes, model_primes[1:]):
        gap = q - p
        if gap <= max_gap:
            model_gap_counts[gap] += 1

    exact_original = original_gap_counts.get(2, 0)
    exact_model = model_gap_counts.get(2, 0)
    bounded_original = sum(original_gap_counts.values())
    bounded_model = sum(model_gap_counts.values())
    retained_ratio = bounded_model / bounded_original if bounded_original else 0.0

    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-18",
        "status": "reduction_attempt_open",
        "route": "BoundedGapCountermodel",
        "proof_or_counterexample_mode": "proof_shortcut_countermodel",
        "attempt": (
            "Construct a finite adversarial prime-like model by deleting the second member of every observed twin pair. "
            "The model has zero exact gap-2 pairs but retains many wider bounded gaps."
        ),
        "bounded_result": {
            "prime_limit": limit,
            "max_gap": max_gap,
            "original_exact_gap_2": exact_original,
            "model_exact_gap_2": exact_model,
            "original_bounded_gap_count": bounded_original,
            "model_bounded_gap_count": bounded_model,
            "bounded_gap_retention_ratio": round(retained_ratio, 8),
            "deleted_prime_count": len(deleted),
            "original_gap_distribution": {str(gap): original_gap_counts[gap] for gap in sorted(original_gap_counts)},
            "countermodel_gap_distribution": {str(gap): model_gap_counts[gap] for gap in sorted(model_gap_counts)},
        },
        "obstruction": (
            "A bounded-gap theorem can remain true in a model with no exact gap-2 pairs. Any twin-prime proof must "
            "isolate exact gap 2 and survive this deletion-style parity countermodel."
        ),
        "candidate_theorem": (
            "A signed or orthogonalized exact-gap projection has positive certified mass on true primes and zero or "
            "negative certified mass on bounded-gap-only countermodels."
        ),
        "next_experiment": "Search projection weights that distinguish exact gap 2 from wider bounded gaps under deletion countermodels.",
        "claim_boundary": "No Twin Prime proof. Bounded-gap evidence still does not prove infinitely many exact gap-2 pairs.",
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    prime_limit = max(args.goldbach_limit, args.twin_limit)
    primes, is_prime = sieve(prime_limit)
    payload = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "reduction_attempts_open_no_resolution",
        "claim_boundary": (
            "Ticket 18 converts proof hopes into falsifiable reduction tests. It closes no open problem and reports "
            "only bounded countermodels, exact finite reductions, and missing infinite bridges."
        ),
        "attempts": [
            riemann_finite_prefix_camouflage(args.riemann_li_terms, args.riemann_betas, args.riemann_heights),
            collatz_valuation_branch_cover(args.collatz_steps, args.collatz_max_shift),
            goldbach_explicit_error_budget(args.goldbach_limit, [p for p in primes if p <= args.goldbach_limit], is_prime),
            twin_bounded_gap_countermodel(args.twin_limit, [p for p in primes if p <= args.twin_limit], args.twin_max_gap),
        ],
    }
    return payload


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-18-finite-prefix-camouflage.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-18-valuation-branch-cover.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-18-explicit-error-budget.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-18-bounded-gap-countermodel.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ticket 18 reduction lab for four open problems.")
    parser.add_argument("--riemann-li-terms", type=int, default=200)
    parser.add_argument("--riemann-betas", type=float, nargs="+", default=[0.55, 0.65, 0.75, 0.85])
    parser.add_argument("--riemann-heights", type=float, nargs="+", default=[1_000.0, 10_000.0, 100_000.0, 1_000_000.0])
    parser.add_argument("--collatz-steps", type=int, default=8)
    parser.add_argument("--collatz-max-shift", type=int, default=28)
    parser.add_argument("--goldbach-limit", type=int, default=200_000)
    parser.add_argument("--twin-limit", type=int, default=300_000)
    parser.add_argument("--twin-max-gap", type=int, default=60)
    parser.add_argument("--output", type=Path, default=ROOT / "data/open-problem/ticket18-reduction-lab.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    write_json(args.output, payload)
    write_attempt_artifacts(payload)
    print(f"ticket18 reduction lab written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
