from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-12T15:20:00+09:00"
SCHEMA = "primeproject.ticket93-twin-correlation-excess-bridge.v1"
CORRELATION_LIMIT = 2_000_000
SURROGATE_LIMIT = 200_000
TRUNCATION_LEVELS = (10, 30, 100, 300)
FORD_MAYNARD_SOURCE = "https://arxiv.org/abs/2407.14368"


def prime_sieve(limit: int) -> tuple[bytearray, list[int]]:
    if limit < 2:
        return bytearray(limit + 1), []
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if not is_prime[prime]:
            continue
        start = prime * prime
        is_prime[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return is_prime, [value for value in range(2, limit + 1) if is_prime[value]]


def von_mangoldt_values(limit: int, primes: list[int]) -> dict[int, float]:
    values: dict[int, float] = {}
    for prime in primes:
        weight = math.log(prime)
        power = prime
        while power <= limit:
            values[power] = weight
            if power > limit // prime:
                break
            power *= prime
    return values


def prime_power_count_bound(limit: int) -> float:
    if limit < 2:
        return 0.0
    return math.sqrt(limit) * math.floor(math.log2(limit))


def contamination_weight_bound(limit: int) -> float:
    y = limit + 2
    return 2.0 * prime_power_count_bound(y) * math.log(y) ** 2


def correlation_row(
    limit: int,
    is_prime: bytearray,
    mangoldt: dict[int, float],
) -> dict[str, Any]:
    correlation = 0.0
    twin_weight = 0.0
    contamination = 0.0
    supported_pair_count = 0
    twin_pair_count = 0
    proper_prime_power_pair_count = 0
    for value, weight in mangoldt.items():
        if value > limit:
            continue
        shifted = value + 2
        shifted_weight = mangoldt.get(shifted)
        if shifted_weight is None:
            continue
        product = weight * shifted_weight
        correlation += product
        supported_pair_count += 1
        if is_prime[value] and is_prime[shifted]:
            twin_weight += product
            twin_pair_count += 1
        else:
            contamination += product
            proper_prime_power_pair_count += 1

    actual_proper_prime_powers = sum(
        int(value <= limit + 2 and not is_prime[value]) for value in mangoldt
    )
    count_bound = prime_power_count_bound(limit + 2)
    weight_bound = contamination_weight_bound(limit)
    decomposition_error = abs(correlation - twin_weight - contamination)
    return {
        "limit": limit,
        "lambda_correlation": correlation,
        "twin_prime_weight": twin_weight,
        "proper_prime_power_contamination": contamination,
        "supported_pair_count": supported_pair_count,
        "twin_pair_count": twin_pair_count,
        "proper_prime_power_pair_count": proper_prime_power_pair_count,
        "actual_proper_prime_power_count": actual_proper_prime_powers,
        "prime_power_count_bound": count_bound,
        "contamination_weight_bound": weight_bound,
        "correlation_minus_bound": correlation - weight_bound,
        "decomposition_error": decomposition_error,
        "count_bound_holds": actual_proper_prime_powers <= count_bound,
        "contamination_bound_holds": contamination <= weight_bound,
    }


def mobius_values(limit: int) -> list[int]:
    mu = [1] * (limit + 1)
    is_prime, primes = prime_sieve(limit)
    del is_prime
    for prime in primes:
        for multiple in range(prime, limit + 1, prime):
            mu[multiple] *= -1
        square = prime * prime
        for multiple in range(square, limit + 1, square):
            mu[multiple] = 0
    mu[0] = 0
    return mu


def truncated_divisor_surrogate(limit: int, truncation: int, mu: list[int]) -> list[float]:
    values = [0.0] * (limit + 3)
    for divisor in range(1, truncation + 1):
        if mu[divisor] == 0:
            continue
        weight = mu[divisor] * math.log(truncation / divisor)
        for multiple in range(divisor, limit + 3, divisor):
            values[multiple] += weight
    return values


def analyze_surrogate_no_go(
    limit: int,
    mangoldt: dict[int, float],
    truncations: tuple[int, ...] = TRUNCATION_LEVELS,
) -> dict[str, Any]:
    exact = [0.0] * (limit + 3)
    for value, weight in mangoldt.items():
        if value <= limit + 2:
            exact[value] = weight
    mu = mobius_values(max(truncations))
    rows: list[dict[str, Any]] = []
    total_failures = 0

    for truncation in truncations:
        surrogate = truncated_divisor_surrogate(limit, truncation, mu)
        pointwise_minorant_violations = sum(
            int(surrogate[value] > exact[value] + 1e-12)
            for value in range(2, limit + 1)
        )
        pair_false_positives = 0
        surrogate_correlation = 0.0
        exact_correlation = 0.0
        for value in range(2, limit + 1):
            surrogate_product = surrogate[value] * surrogate[value + 2]
            exact_product = exact[value] * exact[value + 2]
            surrogate_correlation += surrogate_product
            exact_correlation += exact_product
            pair_false_positives += int(surrogate_product > 1e-12 and exact_product == 0.0)
        route_blocked = pointwise_minorant_violations > 0 and pair_false_positives > 0 and surrogate_correlation > 0
        total_failures += int(not route_blocked)
        rows.append(
            {
                "truncation": truncation,
                "pointwise_minorant_violation_count": pointwise_minorant_violations,
                "pair_false_positive_count": pair_false_positives,
                "surrogate_correlation": surrogate_correlation,
                "exact_correlation": exact_correlation,
                "surrogate_to_exact_ratio": surrogate_correlation / exact_correlation,
                "positive_surrogate_is_not_lower_bound": route_blocked,
            }
        )

    return {
        "definition": "Lambda_R(n)=sum_{d|n,d<=R} mu(d) log(R/d).",
        "pointwise_obstruction": "Lambda_R is not a pointwise minorant of Lambda and is positive on many non-prime powers.",
        "pair_obstruction": "A positive sum Lambda_R(n)Lambda_R(n+2) contains many pairs where the exact Lambda product is zero.",
        "consequence": "No positive truncated-divisor correlation can be promoted to a twin-prime lower bound without a separately proved signed remainder estimate.",
        "rows": rows,
        "total_failure_count": total_failures,
    }


def analyze_twin_correlation_bridge(
    correlation_limit: int = CORRELATION_LIMIT,
    surrogate_limit: int = SURROGATE_LIMIT,
) -> dict[str, Any]:
    maximum_limit = max(correlation_limit + 2, surrogate_limit + 2)
    is_prime, primes = prime_sieve(maximum_limit)
    mangoldt = von_mangoldt_values(maximum_limit, primes)
    checkpoints = sorted({1_000, 10_000, 100_000, 1_000_000, correlation_limit})
    checkpoints = [value for value in checkpoints if value <= correlation_limit]
    correlation_rows = [correlation_row(value, is_prime, mangoldt) for value in checkpoints]
    decomposition_failures = sum(
        int(float(row["decomposition_error"]) > 1e-7)
        + int(not row["count_bound_holds"])
        + int(not row["contamination_bound_holds"])
        for row in correlation_rows
    )
    surrogate = analyze_surrogate_no_go(surrogate_limit, mangoldt)
    total_failures = decomposition_failures + int(surrogate["total_failure_count"])
    final = correlation_rows[-1]

    return {
        "theorem_name": "TwinPrimeLambdaCorrelationExcessSufficiencyAndSurrogateNoGo",
        "source_ticket": "TP-TICKET-92",
        "exact_correlation_bridge": {
            "correlation": "C_2(x)=sum_{n<=x} Lambda(n)Lambda(n+2).",
            "decomposition": "C_2(x)=T_2(x)+E_pp(x), where T_2 is the twin-prime weight and E_pp has at least one proper prime power.",
            "proper_power_count": "Q(y)<=sqrt(y) floor(log2(y)).",
            "contamination_bound": "0<=E_pp(x)<=B(x)=2 sqrt(x+2) floor(log2(x+2)) log^2(x+2).",
            "sufficiency": "If limsup_x (C_2(x)-B(x))=+infinity, then twin primes are infinite.",
            "linear_corollary": "Any proved C_2(x)>=c x for all sufficiently large x, with c>0, implies twin-prime infinitude because B(x)=o(x).",
        },
        "proof_chain": [
            "Separate Lambda-supported pairs into genuine prime-prime pairs and pairs containing a proper prime power.",
            "Overcount proper prime powers by exponent and bound their number by sqrt(y) floor(log2(y)).",
            "Charge each contaminated shifted pair to one of at most two proper-power positions and bound each weight by log^2(y).",
            "Deduce the explicit contamination bound B(x).",
            "If only finitely many twin primes existed, T_2(x) would be bounded, hence C_2(x)-B(x) would be bounded above.",
            "Take the contrapositive to obtain the exact correlation-excess sufficiency theorem.",
            "Falsify the shortcut from positive truncated-divisor correlation to C_2 by pointwise and pairwise counterexamples.",
        ],
        "surrogate_no_go": surrogate,
        "type_ii_boundary": {
            "exact_identity": "Lambda=mu*log turns C_2 into a signed shifted divisor convolution.",
            "missing_input": "A lower bound needs cancellation control for the signed bilinear remainder, not only nonnegative sieve mass.",
            "research_alignment": "Ford-Maynard show in a general prime-producing sieve framework that substantial Type II information is necessary for nontrivial lower bounds.",
            "source": FORD_MAYNARD_SOURCE,
        },
        "machine_audit": {
            "correlation_limit": correlation_limit,
            "surrogate_limit": surrogate_limit,
            "checkpoint_count": len(correlation_rows),
            "final_lambda_correlation": final["lambda_correlation"],
            "final_twin_prime_weight": final["twin_prime_weight"],
            "final_contamination": final["proper_prime_power_contamination"],
            "final_twin_pair_count": final["twin_pair_count"],
            "final_proper_prime_power_pair_count": final["proper_prime_power_pair_count"],
            "final_contamination_bound": final["contamination_weight_bound"],
            "final_correlation_minus_bound": final["correlation_minus_bound"],
            "truncation_count": len(surrogate["rows"]),
            "decomposition_failure_count": decomposition_failures,
            "surrogate_no_go_failure_count": surrogate["total_failure_count"],
            "total_failure_count": total_failures,
            "checkpoints": correlation_rows,
        },
        "theorem_status": "exact_correlation_excess_bridge_and_surrogate_no_go_proved_no_twin_prime_resolution" if total_failures == 0 else "twin_correlation_bridge_audit_inconclusive_no_twin_prime_resolution",
        "discarded_routes": [
            {"route": "positive_truncated_divisor_correlation", "status": "not_a_lower_bound", "counteredge": "Lambda_R exceeds Lambda pointwise and creates positive shifted pairs where the exact product is zero."},
            {"route": "absolute_value_control_of_mobius_remainder", "status": "parity_blind", "counteredge": "Taking absolute values deletes the signed cancellation needed for a lower bound."},
            {"route": "finite_positive_exact_correlation", "status": "finite_only", "counteredge": "A positive correlation through a finite x does not force unbounded excess over prime-power contamination."},
        ],
        "retained_route": "Prove an all-scale signed Type II estimate strong enough to make C_2(x)-B(x) unbounded, with every prime-power and truncation remainder explicit.",
        "candidate_theorem": "ShiftTwoTypeIICorrelationExcess: limsup_x(C_2(x)-B(x))=+infinity via a signed bilinear estimate unavailable to parity-blind sieve weights.",
        "next_theorem_target": "ShiftTwoTypeIICorrelationExcess",
        "proof_boundary": "TICKET93 proves an exact sufficient bridge and a surrogate proof-route no-go. It does not prove the required correlation lower bound or the Twin Prime Conjecture.",
        "novelty_boundary": "The explicit contamination contract and falsification packaging are candidate PrimeProject contributions; von Mangoldt correlations and the sieve parity barrier are established background.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "exact-target correlation and contamination audit transfer discipline",
        "attempt": "Separate the exact target contribution from sparse algebraic contamination and reject positive surrogates that are not certified lower bounds.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket93_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific correlation excess theorem or signed remainder estimate was proved.",
        "candidate_theorem": target,
        "next_experiment": "Write an exact target-weight decomposition and prove every discarded contribution is quantitatively negligible.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket92 = read_json(ROOT / "data/open-problem/ticket92-scale-sensitive-threshold-audit.json")
    audit = analyze_twin_correlation_bridge()
    attempts = [
        transfer_attempt(ticket92, "riemann", "RH-TICKET-93", "ExplicitFormulaContaminationExcess", "Separate zero terms from smoothing contamination before any sign lower bound."),
        transfer_attempt(ticket92, "collatz", "CO-TICKET-93", "ExactOrbitContaminationExcess", "Separate genuine natural-orbit witnesses from 2-adic completion contamination."),
        transfer_attempt(ticket92, "goldbach", "GB-TICKET-93", "GoldbachLambdaCorrelationExcess", "Bound prime-power contamination in the binary Lambda convolution before proving positivity."),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-93",
            "route": "TwinPrimeLambdaCorrelationExcessSufficiencyAndSurrogateNoGo",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact von Mangoldt correlation bridge plus truncated-divisor lower-bound falsification",
            "attempt": "Replace bounded-gap mass by the exact shift-two Lambda correlation and isolate the smallest lower bound that forces infinitely many genuine twin primes.",
            "bounded_result": {"source_ticket": "TP-TICKET-92", "twin_correlation_excess_audit": audit},
            "obstruction": audit["type_ii_boundary"]["missing_input"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET94 around a signed shift-two Type II remainder decomposition and adversarial parity tests.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "twin_correlation_excess_open_no_twin_prime_resolution",
        "claim_boundary": "Ticket 93 proves one exact sufficiency bridge and one proof-route no-go but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket93-twin-correlation-excess-bridge.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-93-correlation-excess.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-93-correlation-excess.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-93-correlation-excess.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-93-correlation-excess.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
