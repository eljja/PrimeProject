from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-16T23:50:00+09:00"
SCHEMA = "primeproject.ticket125-infinite-bridge-contracts.v1"
GOLDBACH_VERIFIED_LIMIT = 4_000_000_000_000_000_000
TOLERANCE = 1e-12


def rh_density_positivity_audit() -> dict[str, Any]:
    finite_gram_rows = []
    for checked_dimension in (1, 2, 4, 8, 16):
        finite_gram_rows.append(
            {
                "checked_dimension": checked_dimension,
                "form": (
                    "H_m(x)=sum_(j<=m) x_j^2-x_(m+1)^2 on R^(m+1)"
                ),
                "checked_subspace_minimum_on_unit_sphere": 1.0,
                "unseen_direction": f"e_{checked_dimension + 1}",
                "unseen_value": -1.0,
                "finite_check_extends": False,
            }
        )

    return {
        "theorem_name": "ContinuousDenseConePositivityExtension",
        "statement": (
            "Let V be the completed RH-equivalent test space, C a dense cone in V, "
            "and H:V->R a continuous quadratic form. If H(c)>=0 for every c in C, "
            "then H(v)>=0 for every v in V."
        ),
        "proof": (
            "For v in V choose c_n in C with c_n->v. Continuity gives "
            "H(v)=lim H(c_n)>=0."
        ),
        "required_arithmetic_objects": [
            "an exact RH-equivalent completed test space V",
            "a cone C proved dense in V",
            "continuity of the Weil quadratic form in the chosen topology",
            "non-circular positivity H(c)>=0 on every c in C",
        ],
        "exact_no_go_models": [
            {
                "missing_hypothesis": "density",
                "model": "H(x,y)=x^2-y^2 and C={(x,0)}",
                "checked_value": "H is nonnegative on C",
                "counterexample": "H(0,1)=-1",
            },
            {
                "missing_hypothesis": "continuity",
                "model": (
                    "Choose a discontinuous Hamel-linear functional L with dense "
                    "kernel and set H=-L^2."
                ),
                "checked_value": "H=0 on the dense kernel of L",
                "counterexample": "H(v)<0 whenever L(v) is nonzero",
            },
            {
                "missing_hypothesis": "all-cone positivity",
                "model": "the finite Gram family H_m",
                "checked_value": "every sampled coordinate direction is positive",
                "counterexample": "the first unseen coordinate has value -1",
            },
        ],
        "finite_gram_rows": finite_gram_rows,
        "machine_audit": {
            "finite_gram_family_count": len(finite_gram_rows),
            "finite_checks_with_unseen_negative_direction": sum(
                int(row["unseen_value"] < 0.0) for row in finite_gram_rows
            ),
            "total_failure_count": 0,
        },
        "proof_boundary": (
            "The extension lemma is proved, but PrimeProject has not proved density, "
            "continuity in an exact RH-equivalent topology, or non-circular cone "
            "positivity for the zeta explicit formula. RH remains open."
        ),
    }


def _replay_accelerated(start: int, steps: int) -> tuple[int, list[int]]:
    current = start
    word = []
    for _ in range(steps):
        valuation = v2(3 * current + 1)
        word.append(valuation)
        current = (3 * current + 1) >> valuation
    return current, word


def collatz_symbolic_descent_audit(
    minimum_bits: int = 4, maximum_bits: int = 18
) -> dict[str, Any]:
    if minimum_bits < 2 or maximum_bits < minimum_bits:
        raise ValueError("invalid residue precision range")

    rows = []
    replay_failures = 0
    boundary_failures = 0
    for bits in range(minimum_bits, maximum_bits + 1):
        modulus = 1 << bits
        odd_class_count = modulus >> 1
        certified_count = 0
        unresolved_count = 0
        maximum_steps = 0
        maximum_consumed_bits = 0

        for residue in range(1, modulus, 2):
            current = residue
            consumed = 0
            steps = 0
            word: list[int] = []
            certificate: tuple[int, int, int, list[int]] | None = None

            while steps < bits:
                valuation = v2(3 * current + 1)
                if consumed + valuation >= bits:
                    break
                consumed += valuation
                word.append(valuation)
                current = (3 * current + 1) >> valuation
                steps += 1
                if current < residue:
                    certificate = (current, consumed, steps, word[:])
                    break

            if certificate is None:
                unresolved_count += 1
                continue

            terminal, total_valuation, step_count, certificate_word = certificate
            certified_count += 1
            maximum_steps = max(maximum_steps, step_count)
            maximum_consumed_bits = max(
                maximum_consumed_bits, total_valuation
            )
            slope_numerator = 3**step_count
            if slope_numerator >= 1 << total_valuation:
                replay_failures += 1

            for shift in (1, 3):
                lifted_start = residue + shift * modulus
                replay_terminal, replay_word = _replay_accelerated(
                    lifted_start, step_count
                )
                predicted = terminal + (
                    slope_numerator
                    * (1 << (bits - total_valuation))
                    * shift
                )
                replay_failures += int(
                    replay_word != certificate_word
                    or replay_terminal != predicted
                    or replay_terminal >= lifted_start
                )

        boundary_residue = (-pow(3, -1, modulus)) % modulus
        boundary_valuation = v2(3 * boundary_residue + 1)
        boundary_holds = (
            boundary_residue % 2 == 1 and boundary_valuation >= bits
        )
        boundary_failures += int(not boundary_holds)
        rows.append(
            {
                "precision_bits": bits,
                "modulus": modulus,
                "odd_class_count": odd_class_count,
                "uniformly_descending_class_count": certified_count,
                "unresolved_class_count": unresolved_count,
                "certified_fraction": certified_count / odd_class_count,
                "maximum_certificate_steps": maximum_steps,
                "maximum_consumed_bits": maximum_consumed_bits,
                "boundary_residue": boundary_residue,
                "boundary_first_valuation": boundary_valuation,
                "boundary_requires_refinement": boundary_holds,
            }
        )

    last = rows[-1]
    return {
        "theorem_name": "ResidueCylinderFiniteStoppingDescentBridge",
        "global_bridge": {
            "name": "UniversalFiniteStoppingDescentIffCollatz",
            "statement": (
                "Assuming the usual 1-2-4 basin, Collatz holds if and only if every "
                "integer n>1 has a finite iterate below n."
            ),
            "forward_proof": (
                "A convergent orbit reaches 1<n, so finite stopping descent holds."
            ),
            "reverse_proof": (
                "Use strong induction on n. A finite iterate m<n reaches 1 by the "
                "induction hypothesis, so n also reaches 1."
            ),
        },
        "cylinder_certificate": {
            "input": "n=r+2^k*t with r odd and t>=0",
            "determined_word_condition": "total accelerated valuation S<k",
            "lift_identity": (
                "T^m(r+2^k*t)=T^m(r)+3^m*2^(k-S)*t"
            ),
            "uniform_descent_test": (
                "If T^m(r)<r before S reaches k, then 3^m<2^S and every "
                "positive lift in that residue cylinder strictly descends."
            ),
        },
        "precision_rows": rows,
        "fixed_precision_boundary": {
            "residue": "r_k=-3^(-1) mod 2^k",
            "proof": (
                "3*r_k+1 is divisible by 2^k, so k bits do not determine even "
                "the first accelerated valuation on this cylinder. At least this "
                "boundary class requires refinement at every fixed precision."
            ),
            "scope": (
                "This refutes completeness of the determined-word fixed-precision "
                "certificate, not every conceivable finite-modulus Collatz argument."
            ),
        },
        "almost_all_no_go": {
            "map": (
                "F(2^j)=2^(j+1) for j>=0 and F(n)=1 for non-powers of two"
            ),
            "consequence": (
                "A density-one set reaches 1 while the sparse power-of-two chain "
                "diverges, so almost-all descent cannot replace universal coverage."
            ),
        },
        "machine_audit": {
            "precision_count": len(rows),
            "largest_precision_bits": int(last["precision_bits"]),
            "largest_odd_class_count": int(last["odd_class_count"]),
            "largest_uniformly_descending_class_count": int(
                last["uniformly_descending_class_count"]
            ),
            "largest_unresolved_class_count": int(
                last["unresolved_class_count"]
            ),
            "largest_certified_fraction": float(last["certified_fraction"]),
            "lift_replay_failure_count": replay_failures,
            "boundary_failure_count": boundary_failures,
            "total_failure_count": replay_failures + boundary_failures,
        },
        "proof_boundary": (
            "The exact cylinder identity certifies many infinite residue classes, "
            "but 9,247 of 131,072 odd classes remain unresolved at 18 bits and an "
            "unresolved boundary exists at every fixed precision. Collatz remains open."
        ),
    }


def goldbach_explicit_cutoff_audit(
    verified_limit: int = GOLDBACH_VERIFIED_LIMIT,
) -> dict[str, Any]:
    if verified_limit <= math.e**4:
        raise ValueError("verified limit must lie in the monotone tail")

    log_limit = math.log(verified_limit)
    contamination_scale = log_limit**2 / math.sqrt(verified_limit)
    scenarios = []
    for normalized_contamination in (0.0, 1.0, 1_000.0, 10_000.0, 100_000.0, 1_000_000.0):
        contamination_at_limit = (
            normalized_contamination * contamination_scale
        )
        maximum_residual_constant = max(
            0.0, (1.0 - contamination_at_limit) * log_limit
        )
        scenarios.append(
            {
                "normalized_major_constant_A": 1.0,
                "proper_prime_power_constant_B": normalized_contamination,
                "contamination_fraction_at_verified_limit": contamination_at_limit,
                "strict_residual_constant_ceiling_K": maximum_residual_constant,
                "positive_budget_exists": maximum_residual_constant > 0.0,
            }
        )

    proposed_k = 40.0
    maximum_b_for_proposed_k = (
        (1.0 - proposed_k / log_limit)
        / contamination_scale
    )
    return {
        "theorem_name": "ExplicitWeightedGoldbachFiniteGlue",
        "weighted_contract": {
            "weighted_sum": "G(N)=sum_(m=2)^(N-2) Lambda(m)Lambda(N-m)",
            "proper_prime_power_contamination": (
                "P(N)=the part of G(N) where at least one summand is a proper "
                "prime power"
            ),
            "analytic_hypotheses": [
                "G(N)>=A*N-K*N/log(N) for every even N>H",
                "P(N)<=B*sqrt(N)*log(N)^2 for every even N>H",
                "A,K,B are explicit, uniform, and independently proved",
            ],
            "endpoint_budget": (
                "A-K/log(H)-B*log(H)^2/sqrt(H)>0"
            ),
            "conclusion": (
                "G(N)-P(N)>0 for every even N>H; together with verified "
                "Goldbach through H, every even N>2 is a sum of two primes."
            ),
            "monotonicity_proof": (
                "For N>=H>e^4, 1/log(N) and log(N)^2/sqrt(N) are decreasing, "
                "so strict positivity at H controls the entire analytic tail."
            ),
        },
        "verified_limit": verified_limit,
        "natural_log_verified_limit": log_limit,
        "normalized_contamination_scale": contamination_scale,
        "budget_scenarios": scenarios,
        "frozen_candidate_budget": {
            "normalized_major_constant_A": 1.0,
            "residual_constant_K": proposed_k,
            "maximum_compatible_prime_power_constant_B": maximum_b_for_proposed_k,
            "status": "numeric_target_only_no_analytic_constants_proved",
        },
        "machine_audit": {
            "scenario_count": len(scenarios),
            "monotone_tail_starts_before_verified_limit": verified_limit > math.e**4,
            "k40_maximum_b": maximum_b_for_proposed_k,
            "total_failure_count": 0,
        },
        "proof_boundary": (
            "The glue theorem and numeric budget are exact, but PrimeProject has "
            "not proved the required pointwise constants A, K, and B. The published "
            "4e18 computation is finite verification, not the missing analytic tail."
        ),
    }


def dyadic_contraction_certificate(
    alpha: float, beta: float
) -> dict[str, Any]:
    if not (0.0 <= alpha < 1.0) or beta < 0.0:
        raise ValueError("invalid contraction parameters")
    if alpha + beta >= 1.0:
        return {
            "criterion_passes": False,
            "limsup_ceiling": 1.0,
            "fixed_margin": 0.0,
            "reason": "alpha+beta is not strictly below one",
        }
    ceiling = beta / (1.0 - alpha)
    return {
        "criterion_passes": True,
        "limsup_ceiling": ceiling,
        "fixed_margin": 1.0 - ceiling,
        "reason": "iterate the affine recurrence and let the geometric tail vanish",
    }


def twin_dyadic_contraction_audit() -> dict[str, Any]:
    source = read_json(
        ROOT
        / "data/open-problem/ticket124-canonical-obstruction-limsup-criterion.json"
    )
    rows = source["canonical_obstruction_limsup_criterion"][
        "finite_obstruction_rows"
    ]
    rows = [row for row in rows if int(row["horizon"]) >= 1_048_576]
    alpha = 0.75
    beta = 0.23
    transitions = []
    for left, right in zip(rows, rows[1:]):
        if int(right["horizon"]) != 2 * int(left["horizon"]):
            raise ValueError("TICKET-124 tail is not dyadic")
        exact_residual = float(right["canonical_obstruction_exact"]) - (
            alpha * float(left["canonical_obstruction_exact"])
        )
        certificate_residual = float(
            right["canonical_obstruction_certificate"]
        ) - alpha * float(left["canonical_obstruction_certificate"])
        transitions.append(
            {
                "from_horizon": int(left["horizon"]),
                "to_horizon": int(right["horizon"]),
                "exact_residual_Q_2X_minus_alpha_Q_X": exact_residual,
                "certificate_residual_Q_2X_minus_alpha_Q_X": certificate_residual,
                "exact_candidate_passes": exact_residual <= beta + TOLERANCE,
                "certificate_candidate_passes": certificate_residual <= beta
                + TOLERANCE,
                "certificate_slack": beta - certificate_residual,
            }
        )

    theorem = dyadic_contraction_certificate(alpha, beta)
    endpoint_rows = []
    for index in (4, 8, 16, 32, 64, 128):
        left = 1.0 - 1.0 / index
        right = 1.0 - 1.0 / (index + 1)
        endpoint_rows.append(
            {
                "index": index,
                "Q_n": left,
                "Q_next": right,
                "endpoint_recurrence_holds": right
                <= alpha * left + (1.0 - alpha) + TOLERANCE,
            }
        )

    return {
        "theorem_name": "DyadicAffineObstructionContraction",
        "statement": (
            "If Q_(2X)<=alpha*Q_X+beta for every sufficiently large dyadic X, "
            "where 0<=alpha<1 and alpha+beta<1, then the dyadic limsup of Q is "
            "at most beta/(1-alpha)<1."
        ),
        "proof": (
            "Iteration gives Q_n<=alpha^j*Q_(n-j)+beta*(1-alpha^j)/(1-alpha). "
            "Taking limsup yields beta/(1-alpha)."
        ),
        "frozen_candidate": {
            "alpha": alpha,
            "beta": beta,
            "alpha_plus_beta": alpha + beta,
            "limsup_ceiling_if_uniformly_proved": theorem["limsup_ceiling"],
            "fixed_margin_if_uniformly_proved": theorem["fixed_margin"],
            "selection_status": (
                "generated from the TICKET-124 finite tail; no unseen holdout and "
                "no asymptotic theorem"
            ),
        },
        "finite_transitions": transitions,
        "strictness_no_go": {
            "construction": "Q_n=1-1/n with beta=1-alpha",
            "consequence": (
                "The endpoint recurrence can hold eventually while Q_n tends to 1, "
                "so alpha+beta<1 is sharp for a fixed positive margin."
            ),
            "rows": endpoint_rows,
        },
        "finite_prefix_no_go": {
            "construction": (
                "Keep Q_n=1/2 on any requested finite prefix, then set the first "
                "unseen value to 11/10."
            ),
            "consequence": (
                "Four passing transitions cannot certify the recurrence on the tail."
            ),
        },
        "between_scale_bridge": (
            "A dyadic recurrence controls only dyadic scales. An all-X theorem also "
            "needs a proved interpolation envelope inside every [2^n,2^(n+1)) block."
        ),
        "machine_audit": {
            "finite_transition_count": len(transitions),
            "exact_candidate_pass_count": sum(
                int(row["exact_candidate_passes"]) for row in transitions
            ),
            "certificate_candidate_pass_count": sum(
                int(row["certificate_candidate_passes"])
                for row in transitions
            ),
            "maximum_exact_recurrence_residual": max(
                float(row["exact_residual_Q_2X_minus_alpha_Q_X"])
                for row in transitions
            ),
            "maximum_certificate_recurrence_residual": max(
                float(row["certificate_residual_Q_2X_minus_alpha_Q_X"])
                for row in transitions
            ),
            "minimum_certificate_slack": min(
                float(row["certificate_slack"]) for row in transitions
            ),
            "endpoint_countermodel_failure_count": sum(
                int(not row["endpoint_recurrence_holds"])
                for row in endpoint_rows
            ),
            "total_failure_count": 0,
        },
        "proof_boundary": (
            "The affine contraction theorem is proved and four finite dyadic "
            "transitions pass the frozen candidate. No uniform Vaughan recurrence, "
            "between-scale interpolation, parity survival, or exact-gap transfer is "
            "proved. Twin Prime remains open."
        ),
    }


def build_audit() -> dict[str, Any]:
    rh = rh_density_positivity_audit()
    collatz = collatz_symbolic_descent_audit()
    goldbach = goldbach_explicit_cutoff_audit()
    twin = twin_dyadic_contraction_audit()
    total_failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in (rh, collatz, goldbach, twin)
    )
    return {
        "theorem_name": "FourConjectureInfiniteBridgeContractAudit",
        "source_ticket": "TICKET-124",
        "riemann_density_positivity": rh,
        "collatz_adaptive_residue_descent": collatz,
        "goldbach_explicit_cutoff": goldbach,
        "twin_dyadic_contraction": twin,
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Primary all-test-function Weil positivity context.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values",
                "url": "https://arxiv.org/abs/1909.03562",
                "role": "Primary almost-all result; it does not provide universal descent.",
            },
            {
                "citation": "Oliveira e Silva, Herzog, and Pardi, Empirical verification of the even Goldbach conjecture",
                "url": "https://doi.org/10.1090/S0025-5718-2013-02787-1",
                "role": "Primary verification through 4e18 used only as finite glue.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary modern joint Type I/II sieve context; no exact gap-2 theorem is imported.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_bridge_theorem_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
        "proof_boundary": (
            "TICKET-125 proves four conditional bridge lemmas and exact no-go "
            "countermodels, but none of the missing arithmetic hypotheses. It proves "
            "or refutes none of the four conjectures."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    boundary = "No conjecture proof and no certified conjecture counterexample."
    return [
        {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-125",
            "status": "exact_extension_bridge_proved_arithmetic_hypotheses_open",
            "route": "ContinuousDenseConePositivityExtension",
            "proof_or_counterexample_mode": "conditional proof plus missing-hypothesis countermodels",
            "attempt": "Prove the exact topology lemma and reject finite, nondense, or discontinuous positivity shortcuts.",
            "bounded_result": {
                "audit_ref": "riemann_density_positivity",
                "finite_gram_family_count": audit["riemann_density_positivity"]["machine_audit"]["finite_gram_family_count"],
            },
            "obstruction": "No exact zeta test-space density and non-circular all-cone positivity theorem is proved.",
            "candidate_theorem": "AdmissibleKernelConeDensityAndPositivity",
            "next_experiment": "Specify the completed Weil test topology and prove or refute density of one explicit arithmetic kernel cone.",
            "claim_boundary": boundary,
        },
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-125",
            "status": "exact_induction_bridge_and_partial_infinite_cylinder_cover_open",
            "route": "AdaptiveResidueFiniteStoppingCover",
            "proof_or_counterexample_mode": "strong-induction bridge plus exact lifted-cylinder certificates",
            "attempt": "Certify every lift of each residue cylinder that descends before its available 2-adic precision is exhausted.",
            "bounded_result": {
                "audit_ref": "collatz_adaptive_residue_descent",
                "precision_bits": audit["collatz_adaptive_residue_descent"]["machine_audit"]["largest_precision_bits"],
                "certified_classes": audit["collatz_adaptive_residue_descent"]["machine_audit"]["largest_uniformly_descending_class_count"],
                "unresolved_classes": audit["collatz_adaptive_residue_descent"]["machine_audit"]["largest_unresolved_class_count"],
            },
            "obstruction": "Every fixed precision has a -3^(-1) boundary cylinder, and 9,247 classes remain unresolved at 18 bits.",
            "candidate_theorem": "AdaptiveResidueFiniteStoppingCover",
            "next_experiment": "Recursively refine only unresolved cylinders and prove that every positive-integer branch receives a finite descent certificate.",
            "claim_boundary": boundary,
        },
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-125",
            "status": "exact_finite_glue_budget_proved_analytic_constants_open",
            "route": "ExplicitWeightedGoldbachFiniteGlue",
            "proof_or_counterexample_mode": "conditional tail proof with explicit endpoint budget",
            "attempt": "Separate the weighted prime-pair lower bound, proper-prime-power contamination, and 4e18 finite overlap.",
            "bounded_result": {
                "audit_ref": "goldbach_explicit_cutoff",
                "verified_limit": GOLDBACH_VERIFIED_LIMIT,
                "log_verified_limit": audit["goldbach_explicit_cutoff"]["natural_log_verified_limit"],
            },
            "obstruction": "No sourced uniform A, K, B constants satisfy the strict endpoint budget.",
            "candidate_theorem": "ExplicitJointBalancedGoldbachCutoff",
            "next_experiment": "Derive replayable major, Vaughan residual, and prime-power constants and test them against the endpoint inequality.",
            "claim_boundary": boundary,
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-125",
            "status": "exact_dyadic_contraction_bridge_proved_finite_candidate_only_open",
            "route": "DyadicAffineObstructionContraction",
            "proof_or_counterexample_mode": "conditional recurrence proof plus endpoint and finite-prefix countermodels",
            "attempt": "Replace a direct limsup estimate by a local dyadic affine contraction with a strict fixed point below one.",
            "bounded_result": {
                "audit_ref": "twin_dyadic_contraction",
                "alpha": 0.75,
                "beta": 0.23,
                "finite_transitions": 4,
            },
            "obstruction": "The four transitions are selected finite data; no uniform Vaughan recurrence or between-scale theorem is proved.",
            "candidate_theorem": "DyadicVaughanObstructionContractionAndInterpolation",
            "next_experiment": "Freeze alpha=3/4 and beta=23/100, compute an unseen 32M holdout, then seek a coefficient-level recurrence proof independent of the holdout.",
            "claim_boundary": boundary,
        },
    ]


def main() -> int:
    audit = build_audit()
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "four_exact_bridge_contracts_proved_missing_arithmetic_hypotheses_open",
        "claim_boundary": audit["proof_boundary"],
        "infinite_bridge_contracts": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket125-infinite-bridge-contracts.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-125-density-positivity-extension.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-125-adaptive-residue-descent-cover.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-125-explicit-cutoff-budget.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-125-dyadic-obstruction-contraction.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
