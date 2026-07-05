from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AT = "2026-07-06T00:35:00+09:00"
SCHEMA = "primeproject.ticket28-trichotomy-descent-lab.v1"
LOG_2 = math.log(2.0)
LOG_3 = math.log(3.0)
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


def trichotomy_routes(
    direct_condition: str,
    no_counterexample_condition: str,
    contrapositive_condition: str,
    direct_status: str,
    no_counterexample_status: str,
    contrapositive_status: str,
    direct_blocker: str,
    no_counterexample_blocker: str,
    contrapositive_blocker: str,
) -> list[dict[str, str]]:
    return [
        {
            "mode": "direct_counterexample",
            "closure_condition": direct_condition,
            "bounded_status": direct_status,
            "open_blocker": direct_blocker,
        },
        {
            "mode": "prove_no_counterexample",
            "closure_condition": no_counterexample_condition,
            "bounded_status": no_counterexample_status,
            "open_blocker": no_counterexample_blocker,
        },
        {
            "mode": "contrapositive",
            "closure_condition": contrapositive_condition,
            "bounded_status": contrapositive_status,
            "open_blocker": contrapositive_blocker,
        },
    ]


def mobius_mertens_stress(limit: int) -> dict[str, Any]:
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

    mertens = 0
    max_from_100 = (0.0, 0, 0)
    max_from_10k = (0.0, 0, 0)
    max_from_1m = (0.0, 0, 0)
    for n in range(1, limit + 1):
        mertens += mu[n]
        normalized = abs(mertens) / math.sqrt(n)
        if n >= 100 and normalized > max_from_100[0]:
            max_from_100 = (normalized, n, mertens)
        if n >= 10_000 and normalized > max_from_10k[0]:
            max_from_10k = (normalized, n, mertens)
        if n >= 1_000_000 and normalized > max_from_1m[0]:
            max_from_1m = (normalized, n, mertens)

    return {
        "stress_observable": "M(n)/sqrt(n), where M is the Mertens summatory function",
        "limit": limit,
        "mertens_at_limit": mertens,
        "max_abs_mertens_over_sqrt_n_from_100": {
            "value": round(max_from_100[0], 10),
            "n": max_from_100[1],
            "mertens": max_from_100[2],
        },
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
        "counterexample_found": None,
        "interpretation": (
            "This is an RH-compatible finite stress observable, not an RH-equivalent proof or counterexample. "
            "A certified RH counterexample still requires an off-critical zeta zero or an equivalent failed theorem."
        ),
    }


def riemann_attempt() -> dict[str, Any]:
    stress = mobius_mertens_stress(5_000_000)
    routes = trichotomy_routes(
        "Exhibit a certified non-trivial zeta zero with real part not equal to 1/2, or an equivalent failed RH theorem.",
        "Prove every non-trivial zero lies on the critical line with explicit control over all heights.",
        "Show that any off-critical zero forces a finite Li/kernel/correlator contradiction below a computable index.",
        "no_certified_offcritical_zero_found_by_ticket28",
        "finite_mertens_stress_only",
        "tail_uniform_bridge_open",
        "No zeta-zero certificate was generated.",
        "Finite Mertens data cannot control the zeta zero set.",
        "The project still lacks a uniform tail theorem converting an off-critical zero into a bounded contradiction.",
    )
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-28",
        "status": "proof_pressure_open",
        "route": "CounterexampleProofContrapositiveTrichotomy",
        "proof_or_counterexample_mode": "finite_stress_plus_tail_obligation",
        "attempt": (
            "Use the user's proof trichotomy explicitly: search for a finite counterexample signal, identify the "
            "theorem needed to prove no counterexample exists, and state the contrapositive bridge that would turn "
            "an off-critical zero into a bounded contradiction."
        ),
        "bounded_result": {
            "source_ticket": "RH-TICKET-27",
            "trichotomy_routes": routes,
            "mertens_stress": stress,
            "global_route_status": "all_global_routes_open",
            "strongest_closed_statement": "No RH counterexample was produced by the finite Mertens stress scan.",
        },
        "obstruction": (
            "The finite stress scan is compatible with RH but does not see zeta zeros. The missing object is still a "
            "tail-uniform zero or positivity theorem."
        ),
        "candidate_theorem": (
            "Every hypothetical off-critical zero produces a computably bounded violation of a formally verified "
            "positivity kernel, with all remaining zeros controlled by an explicit tail majorant."
        ),
        "next_experiment": "Synthesize the tail majorant as a symbolic inequality and run CEGIS against off-critical surrogate zeros.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_prefix_certificate(residue: int, bits: int, max_steps: int = 512) -> dict[str, Any]:
    affine_numerator = 1
    affine_constant = 0
    consumed_bits = 0
    word: list[int] = []
    current = residue

    for _ in range(max_steps):
        valuation = v2(3 * current + 1)
        if consumed_bits + valuation > bits:
            return {
                "status": "needs_split",
                "residue": residue,
                "prefix_word": word,
                "prefix_length": len(word),
                "consumed_bits": consumed_bits,
                "next_valuation": valuation,
                "coefficient_log2_margin": round(consumed_bits - len(word) * LOG2_3, 8),
                "coefficient_log2_debt": round(len(word) * LOG2_3 - consumed_bits, 8),
            }

        affine_constant = 3 * affine_constant + (1 << consumed_bits)
        affine_numerator *= 3
        consumed_bits += valuation
        word.append(valuation)
        current = (3 * current + 1) >> valuation

        denominator = 1 << consumed_bits
        denominator_minus_numerator = denominator - affine_numerator
        if denominator_minus_numerator > 0:
            threshold_min_n = affine_constant // denominator_minus_numerator + 1
            base = {
                "residue": residue,
                "prefix_word": word,
                "prefix_length": len(word),
                "consumed_bits": consumed_bits,
                "affine_numerator_3_pow_k": affine_numerator,
                "affine_denominator_2_pow_s": denominator,
                "affine_constant": affine_constant,
                "threshold_min_n_for_descent": threshold_min_n,
                "coefficient_log2_margin": round(consumed_bits - len(word) * LOG2_3, 8),
            }
            if residue == 1 and threshold_min_n == 2:
                return {
                    **base,
                    "status": "known_cycle_exception",
                    "interpretation": "n=1 is the known fixed cycle; every larger lift in this cylinder descends.",
                }
            if threshold_min_n <= residue:
                return {
                    **base,
                    "status": "all_lift_descent",
                    "interpretation": "Every positive odd n in this exact cylinder descends below its start.",
                }
            return {
                **base,
                "status": "finite_threshold_exception",
                "interpretation": "All sufficiently large lifts descend; finitely many smaller lifts need induction/base checks.",
            }

    return {
        "status": "max_steps_exhausted",
        "residue": residue,
        "prefix_word": word,
        "prefix_length": len(word),
        "consumed_bits": consumed_bits,
        "coefficient_log2_margin": round(consumed_bits - len(word) * LOG2_3, 8),
    }


def keep_top_needs_split(top: list[dict[str, Any]], item: dict[str, Any], limit: int = 12) -> None:
    top.append(item)
    top.sort(
        key=lambda row: (
            float(row.get("coefficient_log2_debt", 0.0)),
            int(row.get("prefix_length", 0)),
            int(row.get("residue", 0)),
        ),
        reverse=True,
    )
    del top[limit:]


def collatz_cylinder_descent(bits_values: list[int]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for bits in bits_values:
        counts: dict[str, int] = {}
        top_needs_split: list[dict[str, Any]] = []
        descent_examples: list[dict[str, Any]] = []
        threshold_examples: list[dict[str, Any]] = []
        max_prefix_length = 0
        max_consumed_bits = 0
        for residue in range(1, 1 << bits, 2):
            certificate = collatz_prefix_certificate(residue, bits)
            status = str(certificate["status"])
            counts[status] = counts.get(status, 0) + 1
            max_prefix_length = max(max_prefix_length, int(certificate.get("prefix_length", 0)))
            max_consumed_bits = max(max_consumed_bits, int(certificate.get("consumed_bits", 0)))
            if status == "needs_split":
                keep_top_needs_split(top_needs_split, certificate)
            elif status == "all_lift_descent" and len(descent_examples) < 8:
                descent_examples.append(certificate)
            elif status in {"known_cycle_exception", "finite_threshold_exception"} and len(threshold_examples) < 8:
                threshold_examples.append(certificate)

        total = 1 << (bits - 1)
        all_lift = counts.get("all_lift_descent", 0)
        known_cycle = counts.get("known_cycle_exception", 0)
        finite_threshold = counts.get("finite_threshold_exception", 0)
        needs_split = counts.get("needs_split", 0)
        closed_nontrivial_denominator = max(total - known_cycle, 1)
        rows.append(
            {
                "modulus_bits": bits,
                "odd_cylinder_count": total,
                "all_lift_descent_count": all_lift,
                "known_cycle_exception_count": known_cycle,
                "finite_threshold_exception_count": finite_threshold,
                "needs_split_count": needs_split,
                "max_steps_exhausted_count": counts.get("max_steps_exhausted", 0),
                "closed_nontrivial_cylinder_rate": round(all_lift / closed_nontrivial_denominator, 8),
                "needs_split_rate": round(needs_split / total, 8),
                "max_exact_prefix_length": max_prefix_length,
                "max_consumed_bits": max_consumed_bits,
                "top_needs_split_examples": top_needs_split,
                "descent_certificate_examples": descent_examples,
                "threshold_or_cycle_examples": threshold_examples,
            }
        )
    return {
        "bits_tested": bits_values,
        "cylinder_descent_rows": rows,
        "max_bits_row": rows[-1],
        "all_nontrivial_cylinders_closed_at_max_bits": rows[-1]["needs_split_count"] == 0
        and rows[-1]["max_steps_exhausted_count"] == 0,
        "interpretation": (
            "Exact affine cylinders prove descent for many full lift families. The remaining states are not Collatz "
            "counterexamples; they are cylinders whose valuation prefix consumes all available 2-adic bits before a "
            "strict affine contraction is certified."
        ),
    }


def collatz_stopping_scan(limit: int, max_steps: int = 10_000) -> dict[str, Any]:
    failures: list[int] = []
    max_stopping_steps = {"steps": 0, "n": None}
    max_peak_debt = {"peak_log_debt": 0.0, "n": None, "steps_to_descent": None}
    for start in range(3, limit + 1, 2):
        current = start
        debt = 0.0
        peak_debt = 0.0
        for step in range(1, max_steps + 1):
            valuation = v2(3 * current + 1)
            current = (3 * current + 1) >> valuation
            debt += LOG_3 - valuation * LOG_2
            peak_debt = max(peak_debt, debt)
            if current < start:
                if step > int(max_stopping_steps["steps"]):
                    max_stopping_steps = {"steps": step, "n": start}
                if peak_debt > float(max_peak_debt["peak_log_debt"]):
                    max_peak_debt = {
                        "peak_log_debt": round(peak_debt, 10),
                        "peak_multiplier": round(math.exp(peak_debt), 6),
                        "n": start,
                        "steps_to_descent": step,
                    }
                break
        else:
            failures.append(start)
            if len(failures) >= 8:
                break
    return {
        "odd_start_limit": limit,
        "max_steps_per_start": max_steps,
        "failed_to_descend_below_start": failures,
        "no_stopping_counterexample_leq_limit": not failures,
        "max_stopping_steps": max_stopping_steps,
        "max_peak_valuation_debt": max_peak_debt,
        "interpretation": (
            "If every odd n>1 eventually descends below n, Collatz follows by strong induction. This scan supplies "
            "finite evidence only; it does not prove the universal descent theorem."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    cylinder = collatz_cylinder_descent([12, 14, 16, 18, 20, 22])
    stopping = collatz_stopping_scan(1_000_000)
    routes = trichotomy_routes(
        "Find an odd n whose accelerated orbit never reaches 1, or a non-trivial positive integer cycle.",
        "Prove every odd n>1 eventually descends below n, then use strong induction.",
        "Assume a minimal divergent orbit or non-trivial cycle exists; force it into an exact cylinder that descends below its start.",
        "no_counterexample_leq_1000000_and_ticket26_closed_false_cycles",
        "many_exact_cylinders_closed_but_not_all",
        "minimal_counterexample_cylinder_descent_bridge_open",
        "Finite search and false-cycle elimination are not exhaustive over all odd integers.",
        "The exact cylinder cover still has needs_split states at the tested modulus.",
        "A minimal counterexample can hide in a cylinder whose valuation prefix needs more 2-adic information.",
    )
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-28",
        "status": "proof_pressure_open",
        "route": "LiftCoordinateDebtRankCEGIS",
        "proof_or_counterexample_mode": "exact_cylinder_descent_contrapositive",
        "attempt": (
            "Replace the refuted quotient-only rank with an exact affine-cylinder descent test. Each residue cylinder "
            "is followed only while its valuation word is certified by the available 2-adic bits; if the affine "
            "coefficient becomes contracting and the threshold is below the cylinder base, every lift in that cylinder descends."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-27",
            "trichotomy_routes": routes,
            "stopping_scan": stopping,
            "cylinder_descent": cylinder,
            "strongest_closed_statement": (
                "For every listed all_lift_descent cylinder, the exact accelerated affine map sends every positive "
                "odd lift in that cylinder below its starting value."
            ),
        },
        "obstruction": (
            "At 2^22, the exact cover still contains needs_split cylinders. They are not counterexamples, but they "
            "prevent promotion to a global strong-induction proof."
        ),
        "candidate_theorem": (
            "There exists a finite or recursively certified adaptive 2-adic cylinder partition such that every "
            "non-1 cylinder has an exact affine descent word; then no minimal Collatz counterexample can exist."
        ),
        "next_experiment": (
            "Run adaptive splitting only on needs_split cylinders and synthesize a debt-aware priority rule that "
            "proves termination of the split process."
        ),
        "claim_boundary": "No Collatz proof, no divergent orbit, and no non-trivial positive integer cycle found.",
    }


def goldbach_witness_scan(prime_flags: bytearray, limit: int) -> dict[str, Any]:
    primes = [value for value in range(2, limit + 1) if prime_flags[value]]
    counterexample: int | None = None
    hardest = {"prime_scans_before_first_witness": 0, "even_n": None, "first_witness": None}
    checked_even_count = 0
    for even_n in range(4, limit + 1, 2):
        witness: tuple[int, int] | None = None
        scans = 0
        for prime in primes:
            if prime > even_n // 2:
                break
            scans += 1
            if prime_flags[even_n - prime]:
                witness = (prime, even_n - prime)
                break
        if witness is None:
            counterexample = even_n
            break
        if scans > int(hardest["prime_scans_before_first_witness"]):
            hardest = {
                "prime_scans_before_first_witness": scans,
                "even_n": even_n,
                "first_witness": list(witness),
            }
        checked_even_count += 1
    return {
        "even_limit": limit,
        "checked_even_count": checked_even_count,
        "counterexample_found": counterexample,
        "no_counterexample_leq_limit": counterexample is None,
        "hardest_first_witness_row": hardest,
        "interpretation": (
            "This is a witness scan for the finite base region. It is not a Goldbach proof unless paired with an "
            "explicit theorem covering every even integer above the limit."
        ),
    }


def goldbach_attempt(prime_flags: bytearray) -> dict[str, Any]:
    scan = goldbach_witness_scan(prime_flags, 2_000_000)
    routes = trichotomy_routes(
        "Find an even integer n>=4 with no representation n=p+q by primes p,q.",
        "Prove a positive lower bound for the Goldbach representation count for every even n above an explicit cutoff.",
        "Assume the least Goldbach counterexample N exists; combine finite verification below B with a tail theorem forcing N<=B.",
        "no_counterexample_leq_2000000",
        "tail_lower_bound_not_closed",
        "least_counterexample_cutoff_bridge_open",
        "Finite search cannot rule out a larger counterexample.",
        "No explicit positive lower-bound theorem has been proved inside PrimeProject.",
        "The analytic cutoff has not been pushed below the verified finite base.",
    )
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-28",
        "status": "proof_pressure_open",
        "route": "WitnessCutoffTrichotomy",
        "proof_or_counterexample_mode": "finite_witness_scan_plus_explicit_tail",
        "attempt": (
            "Treat Goldbach as a least-counterexample problem: scan the finite base for a direct counterexample, "
            "then isolate the exact large-even lower-bound theorem needed to prove no larger counterexample exists."
        ),
        "bounded_result": {
            "source_ticket": "GB-TICKET-27",
            "trichotomy_routes": routes,
            "finite_witness_scan": scan,
            "global_route_status": "finite_base_extended_tail_open",
            "strongest_closed_statement": "Every even integer 4<=n<=2,000,000 has a displayed first-prime witness in the scan.",
        },
        "obstruction": "The project still lacks an explicit large-even lower-bound theorem with all constants effective.",
        "candidate_theorem": (
            "For every even n>N0, the Goldbach representation count is positive, and N0 is no larger than the "
            "committed finite witness scan limit."
        ),
        "next_experiment": "Build a constant ledger for main term minus error and reject any ineffective exceptional-zero dependency.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found up to the finite scan limit.",
    }


def twin_prime_scan(prime_flags: bytearray, limit: int) -> dict[str, Any]:
    twin_pair_count = 0
    last_pair: list[int] | None = None
    previous_start: int | None = None
    max_gap_between_twin_starts = {"gap": 0, "from_start": None, "to_start": None}
    for prime in range(3, limit - 1, 2):
        if prime_flags[prime] and prime_flags[prime + 2]:
            twin_pair_count += 1
            last_pair = [prime, prime + 2]
            if previous_start is not None and prime - previous_start > int(max_gap_between_twin_starts["gap"]):
                max_gap_between_twin_starts = {
                    "gap": prime - previous_start,
                    "from_start": previous_start,
                    "to_start": prime,
                }
            previous_start = prime
    return {
        "prime_limit": limit,
        "twin_pair_count": twin_pair_count,
        "last_twin_pair_leq_limit": last_pair,
        "max_gap_between_twin_pair_starts": max_gap_between_twin_starts,
        "counterexample_found": None,
        "interpretation": (
            "A finite list of twin primes is evidence only. A Twin Prime counterexample would require a certified "
            "last twin pair, and a proof requires an exact-gap-2 lower bound at arbitrarily large scales."
        ),
    }


def twin_prime_attempt(prime_flags: bytearray) -> dict[str, Any]:
    scan = twin_prime_scan(prime_flags, 10_000_000)
    routes = trichotomy_routes(
        "Certify a largest twin-prime pair and prove no larger pair exists.",
        "Prove a positive exact-gap-2 lower-bound functional on infinitely many scales.",
        "Assume a last twin pair exists; force contradiction by showing exact-gap-2 mass survives beyond that scale.",
        "no_largest_twin_pair_certificate",
        "exact_gap_2_tail_lower_bound_not_closed",
        "last_pair_contradiction_bridge_open",
        "The finite scan cannot certify absence above the limit.",
        "Bounded-gap statistics remain insufficient unless they collapse under gap-2 deletion.",
        "No exact-gap-2 lower-bound functional has been proved beyond finite data.",
    )
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-28",
        "status": "proof_pressure_open",
        "route": "ExactGapTailTrichotomy",
        "proof_or_counterexample_mode": "finite_exact_gap_scan_plus_tail_lower_bound",
        "attempt": (
            "Separate exact gap 2 from bounded-gap evidence. The finite scan records exact twin pairs, while the "
            "proof route demands a functional that remains positive on unbounded scales and fails under exact-gap deletion."
        ),
        "bounded_result": {
            "source_ticket": "TP-TICKET-27",
            "trichotomy_routes": routes,
            "finite_exact_gap_scan": scan,
            "global_route_status": "finite_exact_gap_evidence_tail_open",
            "strongest_closed_statement": "The scan finds exact twin-prime pairs up to 10,000,000, including the listed last pair.",
        },
        "obstruction": "The scan does not imply infinitely many exact gap-2 pairs, and no last-pair contradiction theorem is closed.",
        "candidate_theorem": (
            "An exact-gap-2 lower-bound functional is positive on infinitely many dyadic intervals and is destroyed "
            "by deleting every exact gap-2 pair."
        ),
        "next_experiment": "Search sieve features whose finite value collapses under exact-gap deletion but remains stable under bounded-gap noise.",
        "claim_boundary": "No Twin Prime proof and no certified largest twin-prime pair.",
    }


def build_payload() -> dict[str, Any]:
    prime_flags = prime_sieve(10_000_000)
    attempts = [
        riemann_attempt(),
        collatz_attempt(),
        goldbach_attempt(prime_flags),
        twin_prime_attempt(prime_flags),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "trichotomy_descent_open_no_resolution",
        "claim_boundary": (
            "Ticket 28 implements the proof trichotomy requested by the user: search for counterexamples, record "
            "finite evidence for no counterexample, and isolate the contrapositive bridge. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> None:
    payload = build_payload()
    output = ROOT / "data/open-problem/ticket28-trichotomy-descent-lab.json"
    write_json(output, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-28-mertens-tail-trichotomy.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-28-lift-coordinate-debt-rank-cegis.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-28-witness-cutoff-trichotomy.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-28-exact-gap-tail-trichotomy.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem[attempt["problem_id"]], attempt)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
