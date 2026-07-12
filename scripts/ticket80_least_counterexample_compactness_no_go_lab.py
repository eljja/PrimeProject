from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-11T13:20:00+09:00"
SCHEMA = "primeproject.ticket80-least-counterexample-compactness-no-go-lab.v1"
MAX_HORIZON = 512
LOWER_BOUNDS = (
    ("one", 1),
    ("two_pow_20", 1 << 20),
    ("two_pow_68", 1 << 68),
    ("two_pow_128", 1 << 128),
    ("ten_pow_100", 10**100),
)
SAMPLE_HORIZONS = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512}


def accelerated_step(n: int) -> tuple[int, int]:
    numerator = 3 * n + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def all_ones_witness(horizon: int, lower_bound: int) -> dict[str, int]:
    if horizon < 1 or lower_bound < 1:
        raise ValueError("horizon and lower_bound must be positive")
    modulus = 1 << (horizon + 1)
    q = max(1, ceil_div(lower_bound + 1, modulus))
    start = modulus * q - 1
    return {"horizon": horizon, "lower_bound": lower_bound, "q": q, "modulus": modulus, "start": start}


def all_ones_iterate(horizon: int, q: int, step: int) -> int:
    if not 0 <= step <= horizon:
        raise ValueError("step must lie in the finite horizon")
    return (3**step) * (1 << (horizon + 1 - step)) * q - 1


def all_ones_affine_constant(step: int) -> int:
    return 3**step - 2**step


def audit_arbitrarily_large_finite_witnesses() -> dict[str, Any]:
    case_count = 0
    step_replay_count = 0
    lower_bound_failures = 0
    residue_failures = 0
    formula_failures = 0
    valuation_failures = 0
    strict_non_descent_failures = 0
    affine_inequality_failures = 0
    samples: list[dict[str, Any]] = []

    for bound_name, lower_bound in LOWER_BOUNDS:
        for horizon in range(1, MAX_HORIZON + 1):
            witness = all_ones_witness(horizon, lower_bound)
            start = witness["start"]
            modulus = witness["modulus"]
            q = witness["q"]
            case_count += 1
            if start < lower_bound:
                lower_bound_failures += 1
            if start % modulus != modulus - 1:
                residue_failures += 1

            current = start
            for step in range(1, horizon + 1):
                current, valuation = accelerated_step(current)
                step_replay_count += 1
                expected = all_ones_iterate(horizon, q, step)
                if current != expected:
                    formula_failures += 1
                if valuation != 1:
                    valuation_failures += 1
                if current <= start:
                    strict_non_descent_failures += 1
                affine_constant = all_ones_affine_constant(step)
                if (1 << step) * start > (3**step) * start + affine_constant:
                    affine_inequality_failures += 1

            if bound_name in {"one", "two_pow_68", "ten_pow_100"} and horizon in SAMPLE_HORIZONS:
                samples.append(
                    {
                        "bound_name": bound_name,
                        "lower_bound": lower_bound,
                        "horizon": horizon,
                        "q": q,
                        "start": start,
                        "residue": modulus - 1,
                        "modulus": modulus,
                        "terminal": current,
                        "all_prefix_iterates_strictly_above_start": True,
                    }
                )

    failure_count = (
        lower_bound_failures
        + residue_failures
        + formula_failures
        + valuation_failures
        + strict_non_descent_failures
        + affine_inequality_failures
    )
    return {
        "max_horizon": MAX_HORIZON,
        "lower_bound_names": [name for name, _ in LOWER_BOUNDS],
        "lower_bound_count": len(LOWER_BOUNDS),
        "finite_witness_case_count": case_count,
        "accelerated_step_replay_count": step_replay_count,
        "lower_bound_failure_count": lower_bound_failures,
        "residue_failure_count": residue_failures,
        "formula_failure_count": formula_failures,
        "valuation_failure_count": valuation_failures,
        "strict_non_descent_failure_count": strict_non_descent_failures,
        "affine_inequality_failure_count": affine_inequality_failures,
        "finite_witness_failure_count": failure_count,
        "samples": samples,
    }


def audit_dual_topology_escape() -> dict[str, Any]:
    formula_failures = 0
    archimedean_growth_failures = 0
    two_adic_precision_failures = 0
    fixed_point_failures = 0
    samples: list[dict[str, Any]] = []
    previous = 0

    for horizon in range(1, MAX_HORIZON + 1):
        start = (1 << (horizon + 1)) - 1
        if start <= previous:
            archimedean_growth_failures += 1
        previous = start
        if v2(start + 1) != horizon + 1:
            two_adic_precision_failures += 1
        terminal = all_ones_iterate(horizon, 1, horizon)
        replay = start
        for _ in range(horizon):
            replay, valuation = accelerated_step(replay)
            if valuation != 1:
                formula_failures += 1
        if replay != terminal:
            formula_failures += 1
        if horizon in SAMPLE_HORIZONS:
            samples.append(
                {
                    "horizon": horizon,
                    "positive_integer": start,
                    "archimedean_lower_bound": 1 << horizon,
                    "two_adic_precision_to_minus_one": horizon + 1,
                    "terminal": terminal,
                }
            )

    ghost = -1
    ghost_next, ghost_valuation = accelerated_step(ghost)
    if ghost_next != ghost or ghost_valuation != 1:
        fixed_point_failures += 1
    failure_count = formula_failures + archimedean_growth_failures + two_adic_precision_failures + fixed_point_failures
    return {
        "sequence": "x_H=2^(H+1)-1",
        "archimedean_behavior": "x_H tends to positive infinity",
        "two_adic_behavior": "v2(x_H-(-1))=H+1, so x_H tends to -1 in Z_2",
        "two_adic_limit": ghost,
        "limit_accelerated_image": ghost_next,
        "limit_valuation": ghost_valuation,
        "limit_is_positive_integer": False,
        "formula_failure_count": formula_failures,
        "archimedean_growth_failure_count": archimedean_growth_failures,
        "two_adic_precision_failure_count": two_adic_precision_failures,
        "fixed_point_failure_count": fixed_point_failures,
        "dual_topology_failure_count": failure_count,
        "samples": samples,
    }


def analyze_compactness_no_go() -> dict[str, Any]:
    finite = audit_arbitrarily_large_finite_witnesses()
    dual = audit_dual_topology_escape()
    computational_failures = int(finite["finite_witness_failure_count"]) + int(dual["dual_topology_failure_count"])
    status = (
        "least_counterexample_finite_prefix_compactness_refuted_exactly_no_collatz_resolution"
        if computational_failures == 0
        else "least_counterexample_compactness_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "FiniteLeastCounterexamplePrefixCompactnessNoGo",
        "source_ticket": "CO-TICKET-79",
        "necessary_condition": (
            "If N is a least positive Collatz counterexample, every accelerated prefix satisfies "
            "A^j(N)>=N, equivalently 2^S_j*N<=3^j*N+C_j."
        ),
        "finite_satisfiability_theorem": (
            "For every horizon H>=1 and lower bound B>=1 there is an odd n>=B whose first H accelerated valuations "
            "are all 1 and whose first H iterates are all strictly greater than n."
        ),
        "exact_witness": {
            "choice": "q=ceil((B+1)/2^(H+1)), n=2^(H+1)*q-1",
            "cylinder": "n=-1 mod 2^(H+1)",
            "iterate": "A^j(n)=3^j*2^(H+1-j)*q-1 for 0<=j<=H",
            "affine_constant": "C_j=3^j-2^j",
            "strict_non_descent": "A^j(n)>n for 1<=j<=H because 3^j>2^j",
        },
        "positive_integer_cylinder_stabilization_criterion": {
            "statement": (
                "For nested compatible cylinders with moduli tending to infinity, the represented 2-adic point is a "
                "positive ordinary integer iff the least nonnegative cylinder residues eventually stabilize at one positive value."
            ),
            "proof": (
                "If the point is n>0, every modulus larger than n has least residue n. Conversely an eventually constant "
                "compatible residue sequence represents that ordinary integer."
            ),
            "ticket80_application": "The residues 2^(H+1)-1 never stabilize and converge 2-adically to -1.",
        },
        "proof_chain": [
            "A least counterexample can never have an iterate below itself; otherwise minimality and strong induction close its orbit.",
            "The displayed all-ones family satisfies every finite collection of these necessary non-descent inequalities at arbitrarily large natural starts.",
            "The compatible residue cylinders are nested and converge in Z_2 to -1, an accelerated valuation-1 fixed point outside the positive integers.",
            "Therefore finite satisfiability plus 2-adic compactness yields neither a contradiction nor a positive counterexample.",
            "Any valid continuation must add a horizon-independent Archimedean bound or prove eventual residue stabilization; neither follows from the finite prefix constraints.",
        ],
        "machine_audit": {"finite_witnesses": finite, "dual_topology_escape": dual},
        "computational_failure_count": computational_failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "finite_non_descent_prefix_contradiction",
                "status": "refuted_by_arbitrarily_large_all_ones_witnesses",
                "counteredge": "Every finite horizon and lower bound has a positive witness satisfying all prefix inequalities.",
            },
            {
                "family": "two_adic_compactness_to_positive_counterexample",
                "status": "refuted_by_dual_topology_escape",
                "counteredge": "The nested positive witnesses escape to infinity ordinarily while converging to -1 in Z_2.",
            },
            {
                "family": "finite_verified_lower_bound_plus_prefix_search",
                "status": "refuted_as_finite_strategy",
                "counteredge": "The construction works above every prescribed finite lower bound B.",
            },
        ],
        "discarded_route": (
            "Derive a Collatz contradiction from any fixed finite set of least-counterexample non-descent inequalities, "
            "or use 2-adic compactness alone to promote their finite witnesses to a positive integer."
        ),
        "retained_route": (
            "Track one fixed ordinary integer across every horizon. A valid proof must force eventual least-residue "
            "stabilization or a uniform Archimedean upper bound, not merely compatible cylinders."
        ),
        "candidate_theorem": (
            "LeastCounterexampleUniformHeightBound: from all exact non-descent inequalities and arithmetic constraints "
            "for one fixed positive N, derive an explicit horizon-independent upper bound N<=U that overlaps a certified finite verification range."
        ),
        "next_theorem_target": "LeastCounterexampleUniformHeightBound",
        "equivalence_warning": (
            "Proving that every stabilized positive-integer cylinder path has a descent prefix is equivalent to the "
            "coefficient-stopping-time form of Collatz; it is not an independently solved bridge."
        ),
        "literature_context": [
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996)",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Established 2-adic parity-prefix and conjugacy context; no rediscovery claim.",
            },
            {
                "citation": "Niu, Parity vectors and paradoxical sequences in the accelerated Collatz map (2026 preprint)",
                "url": "https://arxiv.org/abs/2605.13886",
                "role": "Recent primary context for sharp finite parity-vector and paradoxical-sequence results; it also makes no Collatz claim.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum of Mathematics, Pi 10 (2022)",
                "url": "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F",
                "role": "Primary context for the gap between almost-all descent and an all-positive-integer theorem.",
            },
        ],
        "novelty_boundary": (
            "Finite parity-prefix realizability is established mathematics. PrimeProject claims only the explicit "
            "least-counterexample finite-satisfiability no-go formulation, the residue-stabilization guard, its audit, "
            "and integration with TICKET78-79."
        ),
        "proof_boundary": (
            "TICKET80 proves a restricted proof-route no-go theorem. It does not show that a least counterexample exists, "
            "does not construct a positive divergent orbit, and neither proves nor disproves Collatz."
        ),
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
        "proof_or_counterexample_mode": "finite-satisfiability compactness guard transfer",
        "attempt": (
            "Transfer only the guard that finite satisfiability does not identify an admissible global object without "
            "a target-specific compactness and admissibility theorem. No Collatz witness or conclusion is transferred."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "ticket80_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No target-specific compactness escape or admissibility theorem was proved for this problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Construct a problem-specific finite-satisfiability family before using this guard as progress.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket79 = read_json(ROOT / "data/open-problem/ticket79-archimedean-two-adic-rank-no-go-lab.json")
    collatz_audit = analyze_compactness_no_go()
    attempts = [
        transfer_attempt(
            ticket79,
            "riemann",
            "RH-TICKET-80",
            "FiniteZeroDataCompactnessAdmissibilityGuard",
            "Any compactness limit of finite zero constraints must be proved to be the actual zeta function and retain an all-height positivity margin.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-80",
            "route": "LeastCounterexampleFinitePrefixCompactnessNoGo",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact arbitrarily-large finite witnesses plus dual-topology compactness counteredge",
            "attempt": (
                "Combine least-counterexample non-descent inequalities with exact valuation cylinders, then test whether "
                "finite truncations or their 2-adic compactness limit force a contradiction."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-79", "least_counterexample_compactness_no_go_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET81 around a horizon-independent height bound for one fixed stabilized natural cylinder path.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket79,
            "goldbach",
            "GB-TICKET-80",
            "FiniteRepresentationMarginCompactnessGuard",
            "A limit of finite positive-margin constraints must retain an explicit uniform margin for every sufficiently large even integer.",
        ),
        transfer_attempt(
            ticket79,
            "twin-prime",
            "TP-TICKET-80",
            "FiniteSieveWeightCompactnessGuard",
            "A limit of finite sieve optimizers must retain exact gap-2 mass and break parity uniformly rather than only converge as a relaxed weight system.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "least_counterexample_compactness_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 80 proves one restricted Collatz proof-route no-go theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket80-least-counterexample-compactness-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-80-least-counterexample-compactness-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-80-least-counterexample-compactness-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-80-least-counterexample-compactness-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-80-least-counterexample-compactness-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
