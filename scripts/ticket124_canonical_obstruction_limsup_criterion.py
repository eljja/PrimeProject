from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-16T14:00:00+09:00"
SCHEMA = "primeproject.ticket124-canonical-obstruction-limsup-criterion.v1"
TOLERANCE = 1e-12


def obstruction_row(
    known: float,
    singleton: float,
    boundary: float,
    saving: float,
    certificate: float,
) -> dict[str, Any]:
    if known <= 0.0 or singleton <= 0.0:
        raise ValueError("known and singleton budgets must be positive")
    if min(boundary, saving, certificate) < 0.0:
        raise ValueError("boundary, saving, and certificate must be nonnegative")
    if saving > singleton + TOLERANCE or certificate > singleton + TOLERANCE:
        raise ValueError("saving and certificate cannot exceed singleton budget")

    eta = saving / singleton
    eta_certificate = certificate / singleton
    rho = singleton / known
    epsilon = boundary / known
    paired = (singleton - saving) / known
    paired_certificate = (singleton - certificate) / known
    obstruction = paired + epsilon
    obstruction_certificate = paired_certificate + epsilon
    margin = 1.0 - obstruction
    margin_certificate = 1.0 - obstruction_certificate

    return {
        "known_budget": known,
        "independent_singleton_budget": singleton,
        "boundary_budget": boundary,
        "exact_saving": saving,
        "joint_lower_certificate": certificate,
        "eta_exact_saving_fraction": eta,
        "eta_certificate_fraction": eta_certificate,
        "rho_singleton_to_known": rho,
        "epsilon_boundary_to_known": epsilon,
        "paired_component_exact": paired,
        "paired_component_certificate": paired_certificate,
        "canonical_obstruction_exact": obstruction,
        "canonical_obstruction_certificate": obstruction_certificate,
        "exact_normalized_margin": margin,
        "certificate_normalized_margin": margin_certificate,
        "ratio_reconstruction": (1.0 - eta) * rho + epsilon,
        "certificate_ratio_reconstruction": (
            (1.0 - eta_certificate) * rho + epsilon
        ),
        "exact_identity_error": abs(
            obstruction - ((1.0 - eta) * rho + epsilon)
        ),
        "certificate_identity_error": abs(
            obstruction_certificate
            - ((1.0 - eta_certificate) * rho + epsilon)
        ),
        "closes_exact": obstruction < 1.0,
        "closes_by_certificate": obstruction_certificate < 1.0,
    }


def limsup_closure_certificate(limsup_obstruction: float) -> dict[str, Any]:
    if limsup_obstruction < 0.0:
        raise ValueError("canonical obstruction is nonnegative")
    if limsup_obstruction >= 1.0:
        return {
            "criterion_passes": False,
            "certified_delta": 0.0,
            "reason": "limsup obstruction is not strictly below one",
        }
    delta = (1.0 - limsup_obstruction) / 2.0
    return {
        "criterion_passes": True,
        "certified_delta": delta,
        "eventual_obstruction_ceiling": 1.0 - delta,
        "reason": "the limsup definition gives an eventual ceiling below one",
    }


def exact_countermodels() -> dict[str, Any]:
    alternating = []
    for index in range(1, 9):
        if index % 2:
            eta, rho, epsilon = 0.2, 1.0, 0.0
        else:
            eta, rho, epsilon = 1.0, 1.0, 0.8
        obstruction = (1.0 - eta) * rho + epsilon
        alternating.append(
            {
                "index": index,
                "eta": eta,
                "rho": rho,
                "epsilon": epsilon,
                "canonical_obstruction": obstruction,
                "normalized_margin": 1.0 - obstruction,
            }
        )

    collapsing = []
    for index in (2, 4, 8, 16, 64, 1024):
        singleton = 1.0 / index
        collapsing.append(
            {
                "index": index,
                "known": 1.0,
                "singleton": singleton,
                "saving": 0.0,
                "boundary": 0.0,
                "saving_fraction": 0.0,
                "canonical_obstruction": singleton,
                "normalized_margin": 1.0 - singleton,
            }
        )

    endpoint = []
    for index in (2, 4, 8, 16, 64, 1024):
        obstruction = 1.0 - 1.0 / index
        endpoint.append(
            {
                "index": index,
                "canonical_obstruction": obstruction,
                "normalized_margin": 1.0 / index,
            }
        )

    finite_prefix = []
    for prefix in (1, 2, 4, 8, 64):
        finite_prefix.append(
            {
                "verified_prefix": prefix,
                "passing_obstruction": 0.5,
                "passing_margin": 0.5,
                "first_unseen_index": prefix + 1,
                "first_unseen_obstruction": 1.25,
                "first_unseen_margin": -0.25,
            }
        )

    return {
        "coordinate_envelope_compensation_no_go": {
            "construction": "Alternate (eta,rho,epsilon)=(1/5,1,0) and (1,1,4/5). Every row has Q=4/5, but separate worst-case envelopes force (1-eta_floor)rho_ceiling+epsilon_ceiling=8/5.",
            "proved_consequence": "The TICKET-123 compatible constant triple is sufficient but not necessary for uniform positive margin.",
            "sequence": alternating,
            "separate_envelope_left": 1.6,
            "joint_limsup": 0.8,
        },
        "positive_saving_floor_not_necessary": {
            "construction": "Set K=1, S=1/n, D=E=0. Then eta=0 at every scale while Q=1/n tends to zero.",
            "proved_consequence": "A positive lower bound for D/S is not necessary when S/K itself vanishes.",
            "sequence": collapsing,
        },
        "endpoint_limsup_sharpness": {
            "construction": "Set Q_n=1-1/n. Every finite row closes, but the margins 1/n tend to zero and limsup Q_n=1.",
            "proved_consequence": "The strict inequality limsup Q<1 is sharp for a fixed eventual positive margin.",
            "sequence": endpoint,
        },
        "finite_prefix_no_go": {
            "construction": "After any finite prefix with Q=1/2, place Q=5/4 at the first unseen scale.",
            "proved_consequence": "No finite prefix estimates the true limsup without an independent tail theorem.",
            "sequence": finite_prefix,
        },
    }


def _tail_envelopes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_tail_max = float("-inf")
    certificate_tail_max = float("-inf")
    result = []
    for row in reversed(rows):
        exact_tail_max = max(
            exact_tail_max, float(row["canonical_obstruction_exact"])
        )
        certificate_tail_max = max(
            certificate_tail_max,
            float(row["canonical_obstruction_certificate"]),
        )
        result.append(
            {
                "start_horizon": int(row["horizon"]),
                "observed_exact_tail_max": exact_tail_max,
                "observed_certificate_tail_max": certificate_tail_max,
                "observed_exact_tail_margin": 1.0 - exact_tail_max,
                "observed_certificate_tail_margin": 1.0
                - certificate_tail_max,
            }
        )
    result.reverse()
    return result


def build_audit() -> dict[str, Any]:
    source = read_json(
        ROOT
        / "data/open-problem/ticket123-canonical-defect-ratio-closure-bridge.json"
    )
    source_rows = source["canonical_defect_ratio_closure_bridge"][
        "finite_ratio_rows"
    ]
    rows = []
    for source_row in source_rows:
        row = obstruction_row(
            float(source_row["known_budget"]),
            float(source_row["independent_singleton_budget"]),
            float(source_row["boundary_budget"]),
            float(source_row["exact_saving"]),
            float(source_row["joint_lower_certificate"]),
        )
        rows.append({"horizon": int(source_row["horizon"]), **row})

    models = exact_countermodels()
    tails = _tail_envelopes(rows)
    machine = {
        "scale_count": len(rows),
        "exact_closure_count": sum(int(row["closes_exact"]) for row in rows),
        "certificate_closure_count": sum(
            int(row["closes_by_certificate"]) for row in rows
        ),
        "minimum_exact_obstruction": min(
            float(row["canonical_obstruction_exact"]) for row in rows
        ),
        "maximum_exact_obstruction": max(
            float(row["canonical_obstruction_exact"]) for row in rows
        ),
        "last_exact_obstruction": float(
            rows[-1]["canonical_obstruction_exact"]
        ),
        "last_certificate_obstruction": float(
            rows[-1]["canonical_obstruction_certificate"]
        ),
        "maximum_exact_identity_error": max(
            float(row["exact_identity_error"]) for row in rows
        ),
        "maximum_certificate_identity_error": max(
            float(row["certificate_identity_error"]) for row in rows
        ),
        "alternating_joint_limsup": float(
            models["coordinate_envelope_compensation_no_go"]["joint_limsup"]
        ),
        "alternating_separate_envelope_left": float(
            models["coordinate_envelope_compensation_no_go"][
                "separate_envelope_left"
            ]
        ),
        "total_failure_count": 0,
    }
    machine["total_failure_count"] += sum(
        int(float(row["exact_identity_error"]) > TOLERANCE)
        + int(float(row["certificate_identity_error"]) > TOLERANCE)
        for row in rows
    )
    machine["total_failure_count"] += int(
        any(abs(float(row["canonical_obstruction"]) - 0.8) > TOLERANCE for row in models["coordinate_envelope_compensation_no_go"]["sequence"])
    )

    return {
        "theorem_name": "CanonicalObstructionLimsupClosureCriterionAndTripleNoGo",
        "source_ticket": "TICKET-123",
        "notation": {
            "Q_X": "((S_X-D_X)+E_X)/K_X = (1-eta_X)rho_X+epsilon_X",
            "delta_X": "1-Q_X, the exact normalized TICKET-122 budget margin",
        },
        "exact_identity": "delta_X = 1-Q_X",
        "proved_iff_criterion": {
            "name": "EventualPositiveMarginIffLimsupObstructionBelowOne",
            "statement": "There exist delta>0 and X0 such that delta_X>=delta for every X>=X0 if and only if limsup_(X->infinity) Q_X<1.",
            "forward_proof": "If delta_X>=delta eventually, then Q_X<=1-delta eventually, so limsup Q_X<=1-delta<1.",
            "reverse_proof": "If L=limsup Q_X<1, choose delta=(1-L)/2. By the definition of limsup, eventually Q_X<=(1+L)/2=1-delta, hence delta_X>=delta.",
            "scope": "Exact for the normalized TICKET-122 budget sequence; it does not by itself prove the analytic transfer from that budget to exact prime pairs.",
        },
        "retired_target": {
            "name": "VaughanCanonicalDefectRatioTriple",
            "reason": "It takes coordinatewise worst cases and is strictly stronger than the exact joint closure condition. The alternating compensation model closes uniformly but admits no compatible TICKET-123 constant tuple.",
            "status": "retired_as_unnecessarily_strong_not_false_for_vaughan_data",
        },
        "retained_theorem": {
            "name": "VaughanCanonicalObstructionLimsup",
            "statement": "For the actual Vaughan-realizable budgets, prove limsup Q_X<1, or construct an unbounded Vaughan-realizable subsequence with Q_X>=1.",
            "required_independence": "The tail estimate must come from an arithmetic theorem, not from the eight finite rows or a fitted extrapolation.",
            "remaining_bridge": "Even a proof of this route criterion must be paired with a rigorous asymptotic Vaughan-to-exact-gap transfer and parity-survival theorem.",
        },
        "finite_obstruction_rows": rows,
        "observed_tail_envelopes": tails,
        "exact_countermodels": models,
        "route_classification": {
            "riemann": "Non-circular kernel positivity remains open and must be stated on an exact RH-equivalent test class; finite positivity is not the bridge.",
            "collatz": "GoldenMeanInvariantSetEscape is a route-specific Mersenne-delay lemma, not a sufficient global Collatz bridge. Restore ResidueRankDescentCover as the global target.",
            "goldbach": "A joint pointwise residual envelope is conditionally sufficient only after explicit major-term positivity, cutoff, and finite-overlap glue are supplied.",
            "twin_prime": "The limsup criterion is necessary and sufficient only for the selected canonical budget route; exact-gap transfer and parity survival remain open.",
        },
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Weil positivity is an RH-equivalent all-test-function condition; finite sampled positivity is not sufficient.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values",
                "url": "https://arxiv.org/abs/1909.03562",
                "role": "Almost-all logarithmic-density control does not supply a universal descent theorem.",
            },
            {
                "citation": "Oliveira e Silva, Herzog, and Pardi, Empirical verification of the even Goldbach conjecture",
                "url": "https://doi.org/10.1090/S0025-5718-2013-02787-1",
                "role": "Verification through 4e18 is finite overlap evidence, not an all-even proof.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Joint Type I/II information and extremal countermodels motivate a joint obstruction rather than detached coordinate envelopes.",
            },
        ],
        "machine_audit": machine,
        "proof_boundary": "TICKET124 proves an exact iff criterion for one canonical budget route and disproves necessity of the prior modular triple. It proves no conjecture and certifies no conjecture counterexample.",
    }


def build_attempts() -> list[dict[str, Any]]:
    common_boundary = "No conjecture proof and no certified conjecture counterexample."
    return [
        {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-124",
            "status": "global_target_contract_sharpened_open",
            "route": "ExactTestClassKernelPositivityContract",
            "proof_or_counterexample_mode": "separate an exact all-test-function criterion from finite kernel evidence",
            "attempt": "Retain non-circular explicit-formula positivity only with an exact admissible test class and an independent positivity premise.",
            "bounded_result": {
                "global_target": "NonCircularExplicitFormulaKernelPositivity",
                "discarded_shortcut": "finite or sampled kernel-cone positivity",
                "audit_ref": "canonical_obstruction_limsup_criterion",
            },
            "obstruction": "No independent all-test-function positivity theorem or density bridge is proved.",
            "candidate_theorem": "AdmissibleKernelConeDensityAndPositivity",
            "next_experiment": "Formalize the test class and reject any premise equivalent to zero placement before searching positivity certificates.",
            "claim_boundary": common_boundary,
        },
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-124",
            "status": "route_specific_target_reclassified_global_bridge_open",
            "route": "GoldenMeanRouteScopeCorrection",
            "proof_or_counterexample_mode": "demote a route lemma and restore the universal descent bridge",
            "attempt": "Keep GoldenMeanInvariantSetEscape as a Mersenne-delay subroute, but stop presenting it as a sufficient bridge to Collatz.",
            "bounded_result": {
                "route_specific_target": "GoldenMeanInvariantSetEscape",
                "global_target": "ResidueRankDescentCover",
                "audit_ref": "canonical_obstruction_limsup_criterion",
            },
            "obstruction": "Golden-mean escape for one fixed 2-adic exponent does not cover every positive integer orbit.",
            "candidate_theorem": "ResidueRankDescentCover",
            "next_experiment": "Synthesize exact residue ranks and use nondecreasing SCCs as counterexamples to each proposed finite cover.",
            "claim_boundary": common_boundary,
        },
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-124",
            "status": "conditional_sufficiency_contract_sharpened_open",
            "route": "JointResidualCutoffContract",
            "proof_or_counterexample_mode": "attach pointwise residual control to explicit cutoff and finite glue",
            "attempt": "Retain joint signed Vaughan cancellation only as part of an explicit major-term, cutoff, and finite-overlap theorem.",
            "bounded_result": {
                "route_specific_target": "JointBalancedVaughanGoldbachResidualEnvelope",
                "global_target": "ExplicitGoldbachCutoffBridge",
                "audit_ref": "canonical_obstruction_limsup_criterion",
            },
            "obstruction": "The residual inequality lacks a proved explicit constant and cutoff below the verified finite range.",
            "candidate_theorem": "ExplicitJointBalancedGoldbachCutoff",
            "next_experiment": "Derive a pointwise constant K and prove the resulting cutoff lies below 4e18 before invoking finite verification.",
            "claim_boundary": common_boundary,
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-124",
            "status": "exact_iff_route_criterion_proved_prior_triple_retired_open",
            "route": "CanonicalObstructionLimsupCriterion",
            "proof_or_counterexample_mode": "exact equivalence plus countermodels to an overstrong modular target",
            "attempt": "Replace detached eta-rho-epsilon envelopes by the exact joint obstruction Q_X and prove its limsup closure criterion.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-123",
                "audit_ref": "canonical_obstruction_limsup_criterion",
            },
            "obstruction": "No arithmetic tail theorem proves limsup Q_X<1 for actual Vaughan-realizable budgets, and exact-gap transfer remains open.",
            "candidate_theorem": "VaughanCanonicalObstructionLimsup",
            "next_experiment": "Bound the paired residual and boundary term jointly on dyadic Vaughan blocks, preserving covariance instead of taking separate suprema.",
            "claim_boundary": common_boundary,
        },
    ]


def main() -> int:
    audit = build_audit()
    attempts = build_attempts()
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_iff_route_criterion_and_prior_target_no_go_open",
        "claim_boundary": audit["proof_boundary"],
        "canonical_obstruction_limsup_criterion": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket124-canonical-obstruction-limsup-criterion.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-124-kernel-contract-sharpened.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-124-golden-mean-scope-correction.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-124-explicit-cutoff-contract.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-124-obstruction-limsup-criterion.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
