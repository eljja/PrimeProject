from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-16T10:30:00+09:00"
SCHEMA = "primeproject.ticket123-canonical-defect-ratio-closure-bridge.v1"
TOLERANCE = 1e-12


def ratio_bridge_row(
    known: float,
    singleton: float,
    boundary: float,
    saving: float,
    certificate: float,
) -> dict[str, Any]:
    if known <= 0.0 or singleton <= 0.0:
        raise ValueError("known and singleton budgets must be positive")
    if boundary < 0.0 or saving < 0.0 or certificate < 0.0:
        raise ValueError("boundary, saving, and certificate must be nonnegative")

    eta = saving / singleton
    eta_certificate = certificate / singleton
    rho = singleton / known
    epsilon = boundary / known
    exact_delta = (known - (singleton - saving) - boundary) / known
    certificate_delta = (
        known - (singleton - certificate) - boundary
    ) / known
    ratio_delta = 1.0 - (1.0 - eta) * rho - epsilon
    ratio_certificate_delta = (
        1.0 - (1.0 - eta_certificate) * rho - epsilon
    )
    critical_eta = (singleton + boundary - known) / singleton

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
        "critical_eta_for_zero_margin": critical_eta,
        "nonnegative_critical_eta": max(0.0, critical_eta),
        "exact_eta_headroom": eta - critical_eta,
        "certificate_eta_headroom": eta_certificate - critical_eta,
        "exact_normalized_margin": exact_delta,
        "certificate_normalized_margin": certificate_delta,
        "ratio_identity_margin": ratio_delta,
        "ratio_certificate_margin": ratio_certificate_delta,
        "exact_identity_error": abs(exact_delta - ratio_delta),
        "certificate_identity_error": abs(
            certificate_delta - ratio_certificate_delta
        ),
        "closes_exact": exact_delta > 0.0,
        "closes_by_certificate": certificate_delta > 0.0,
    }


def bridge_guarantee(
    known: float,
    eta_floor: float,
    rho_ceiling: float,
    epsilon_ceiling: float,
) -> dict[str, float]:
    if known <= 0.0:
        raise ValueError("known must be positive")
    if not 0.0 <= eta_floor <= 1.0:
        raise ValueError("eta_floor must lie in [0, 1]")
    if rho_ceiling < 0.0 or epsilon_ceiling < 0.0:
        raise ValueError("ratio ceilings must be nonnegative")
    delta = 1.0 - (1.0 - eta_floor) * rho_ceiling - epsilon_ceiling
    return {
        "guaranteed_normalized_margin": delta,
        "guaranteed_absolute_margin": delta * known,
    }


def abstract_countermodels() -> dict[str, Any]:
    saving_only = []
    eta = 0.25
    for scale in (1.0, 2.0, 10.0, 100.0, 1_000_000.0):
        singleton = scale
        saving = eta * singleton
        saving_only.append(
            {
                "scale": scale,
                "known": 1.0,
                "singleton": singleton,
                "boundary": 0.0,
                "saving": saving,
                "saving_fraction": eta,
                "normalized_margin": 1.0 - singleton + saving,
            }
        )

    ratio_without_boundary = []
    rho = 0.5
    for boundary in (0.0, 0.25, 0.5, 1.0, 1_000_000.0):
        singleton = rho
        saving = 0.2 * singleton
        ratio_without_boundary.append(
            {
                "known": 1.0,
                "singleton": singleton,
                "boundary": boundary,
                "saving": saving,
                "singleton_to_known": rho,
                "normalized_margin": 1.0 - singleton + saving - boundary,
            }
        )

    compatibility = []
    for excess in (0.0, 0.01, 0.1, 1.0):
        eta_fixed = 0.2
        rho_fixed = 1.0
        epsilon = 0.2 + excess
        compatibility.append(
            {
                "eta": eta_fixed,
                "rho": rho_fixed,
                "epsilon": epsilon,
                "compatibility_left": (1.0 - eta_fixed) * rho_fixed
                + epsilon,
                "normalized_margin": -excess,
            }
        )

    finite_prefix = []
    for verified_prefix in (1, 2, 4, 8, 64):
        finite_prefix.append(
            {
                "verified_prefix": verified_prefix,
                "passing_parameters": {
                    "known": 1.0,
                    "singleton": 2.0,
                    "boundary": 0.0,
                    "saving": 2.0,
                    "normalized_margin": 1.0,
                },
                "first_unseen_parameters": {
                    "index": verified_prefix + 1,
                    "known": 1.0,
                    "singleton": 2.0,
                    "boundary": 0.0,
                    "saving": 0.0,
                    "normalized_margin": -1.0,
                },
            }
        )

    return {
        "saving_fraction_alone_no_go": {
            "construction": "Fix eta=1/4, K=1, E=0, S=M, and D=eta*S. The saving fraction stays positive while the normalized margin 1-(1-eta)M tends to minus infinity.",
            "purpose": "A uniform positive canonical saving fraction is insufficient without a singleton-to-known ratio bound.",
            "sequence": saving_only,
        },
        "ratio_without_boundary_no_go": {
            "construction": "Fix K=1, S/K=1/2, and D/S=1/5, then let E grow. The singleton ratio remains bounded while the margin tends to minus infinity.",
            "purpose": "A singleton-to-known ratio bound is insufficient without a boundary envelope.",
            "sequence": ratio_without_boundary,
        },
        "compatibility_sharpness": {
            "construction": "At eta=1/5 and rho=1, epsilon=1/5 gives zero margin; epsilon=1/5+t gives margin -t.",
            "purpose": "Non-strict compatibility cannot yield a fixed positive delta.",
            "sequence": compatibility,
        },
        "finite_prefix_no_go": {
            "construction": "For every finite B, use K=1,S=D=2,E=0 through B and K=1,S=2,D=E=0 at B+1.",
            "purpose": "An arbitrarily long finite pass prefix does not imply eventual closure.",
            "sequence": finite_prefix,
        },
    }


def _frontier_transition(rows: list[dict[str, Any]]) -> dict[str, Any]:
    left = next(row for row in rows if row["horizon"] == 8_388_608)
    right = next(row for row in rows if row["horizon"] == 16_777_216)
    eta_mid = 0.5 * (
        left["eta_exact_saving_fraction"]
        + right["eta_exact_saving_fraction"]
    )
    rho_mid = 0.5 * (
        left["rho_singleton_to_known"] + right["rho_singleton_to_known"]
    )
    eta_contribution = rho_mid * (
        right["eta_exact_saving_fraction"]
        - left["eta_exact_saving_fraction"]
    )
    rho_contribution = -(1.0 - eta_mid) * (
        right["rho_singleton_to_known"]
        - left["rho_singleton_to_known"]
    )
    epsilon_contribution = -(
        right["epsilon_boundary_to_known"]
        - left["epsilon_boundary_to_known"]
    )
    observed = (
        right["exact_normalized_margin"]
        - left["exact_normalized_margin"]
    )
    reconstructed = (
        eta_contribution + rho_contribution + epsilon_contribution
    )
    return {
        "from_horizon": left["horizon"],
        "to_horizon": right["horizon"],
        "observed_margin_change": observed,
        "eta_change_contribution": eta_contribution,
        "rho_change_contribution": rho_contribution,
        "epsilon_change_contribution": epsilon_contribution,
        "reconstructed_margin_change": reconstructed,
        "reconstruction_error": abs(observed - reconstructed),
        "interpretation": "The 8M-to-16M finite improvement is dominated by the decrease in S/K; eta decreases and contributes adversely. This is descriptive and supplies no asymptotic trend.",
    }


def build_audit() -> dict[str, Any]:
    source = read_json(
        ROOT
        / "data/open-problem/ticket122-twin-canonical-joint-defect-audit.json"
    )
    source_audit = source["twin_canonical_joint_defect_audit"]
    rows = []
    for source_row in source_audit["scale_rows"]:
        row = ratio_bridge_row(
            float(source_row["known_without_type_ii_minor"]),
            float(source_row["independent_singleton_budget"]),
            float(source_row["boundary_and_variation_budget"]),
            float(source_row["exact_total_saving"]),
            float(source_row["joint_lower_certificate"]),
        )
        rows.append(
            {
                "horizon": int(source_row["horizon"]),
                "source_closes_finite": bool(source_row["closes_finite"]),
                **row,
            }
        )

    countermodels = abstract_countermodels()
    transition = _frontier_transition(rows)
    machine = {
        "scale_count": len(rows),
        "exact_closure_count": sum(int(row["closes_exact"]) for row in rows),
        "certificate_closure_count": sum(
            int(row["closes_by_certificate"]) for row in rows
        ),
        "minimum_exact_eta": min(
            float(row["eta_exact_saving_fraction"]) for row in rows
        ),
        "minimum_certificate_eta": min(
            float(row["eta_certificate_fraction"]) for row in rows
        ),
        "maximum_rho": max(
            float(row["rho_singleton_to_known"]) for row in rows
        ),
        "minimum_rho": min(
            float(row["rho_singleton_to_known"]) for row in rows
        ),
        "maximum_epsilon": max(
            float(row["epsilon_boundary_to_known"]) for row in rows
        ),
        "minimum_exact_margin": min(
            float(row["exact_normalized_margin"]) for row in rows
        ),
        "maximum_exact_margin": max(
            float(row["exact_normalized_margin"]) for row in rows
        ),
        "maximum_exact_identity_error": max(
            float(row["exact_identity_error"]) for row in rows
        ),
        "maximum_certificate_identity_error": max(
            float(row["certificate_identity_error"]) for row in rows
        ),
        "frontier_transition_reconstruction_error": float(
            transition["reconstruction_error"]
        ),
        "saving_only_terminal_margin": countermodels[
            "saving_fraction_alone_no_go"
        ]["sequence"][-1]["normalized_margin"],
        "boundary_terminal_margin": countermodels[
            "ratio_without_boundary_no_go"
        ]["sequence"][-1]["normalized_margin"],
        "total_failure_count": 0,
    }
    for field in (
        "maximum_exact_identity_error",
        "maximum_certificate_identity_error",
        "frontier_transition_reconstruction_error",
    ):
        machine["total_failure_count"] += int(
            float(machine[field]) > TOLERANCE
        )
    machine["total_failure_count"] += sum(
        int(row["closes_exact"] != row["source_closes_finite"])
        for row in rows
    )

    return {
        "theorem_name": "CanonicalDefectRatioClosureBridgeAndIndependentPremiseNoGo",
        "source_ticket": "TICKET-122",
        "notation": {
            "K": "known_without_type_ii_minor > 0",
            "S": "independent_singleton_budget >= 0",
            "E": "boundary_and_variation_budget >= 0",
            "D": "exact canonical joint saving, with canonical budget S-D",
            "eta": "saving fraction lower bound D/S",
            "rho": "singleton-to-known upper bound S/K",
            "epsilon": "boundary-to-known upper bound E/K",
        },
        "exact_identity": "(K-(S-D)-E)/K = 1-(1-D/S)(S/K)-E/K",
        "proved_bridge": {
            "name": "CanonicalDefectRatioClosureBridge",
            "hypotheses": "K>0, 0<=eta<=1, D>=eta*S, S<=rho*K, E<=epsilon*K, and (1-eta)rho+epsilon<=1-delta.",
            "conclusion": "K-(S-D)-E >= delta*K.",
            "proof": "D>=eta*S gives K-(S-D)-E >= K-(1-eta)S-E. Since 1-eta>=0, S<=rho*K and E<=epsilon*K give at least K[1-(1-eta)rho-epsilon], which is at least delta*K by compatibility.",
        },
        "finite_ratio_rows": rows,
        "frontier_transition": transition,
        "abstract_countermodels": countermodels,
        "discarded_candidates": [
            "uniform positive saving fraction without S/K control",
            "uniform S/K control without E/K control",
            "non-strict compatibility used to claim positive delta",
            "eventual closure inferred from any finite pass prefix",
        ],
        "retained_theorem": {
            "name": "VaughanCanonicalDefectRatioTriple",
            "statement": "Prove fixed constants eta,rho,epsilon,delta with 0<eta<=1 and delta>0 such that D_X>=eta*S_X, S_X<=rho*K_X, E_X<=epsilon*K_X, and (1-eta)rho+epsilon<=1-delta for every sufficiently large X.",
            "counterexample_route": "Construct a Vaughan-realizable unbounded sequence on which every proposed compatible constant tuple fails through vanishing D/S, unbounded S/K, excessive E/K, or nonpositive combined margin.",
            "equivalence_warning": "This is a sufficient modular package for the TICKET-122 margin, not a proved estimate and not a parity-breaking theorem by itself.",
        },
        "literature_boundary": [
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Joint Type I/II information is essential, and extremal sequences can certify insufficiency of weaker information contracts.",
            },
            {
                "citation": "Maynard, Small gaps between primes",
                "url": "https://annals.math.princeton.edu/2015/181-1/p07",
                "role": "Bounded-gap sieve conclusions do not isolate the exact gap two required here.",
            },
            {
                "citation": "Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations",
                "url": "https://arxiv.org/abs/1509.05422",
                "role": "Logarithmically averaged fixed-shift cancellation does not supply this unweighted endpoint ratio triple.",
            },
        ],
        "machine_audit": machine,
        "proof_boundary": "TICKET123 proves an algebraic closure bridge and four proof-strategy no-go families. It proves no conjecture and certifies no conjecture counterexample.",
    }


def _preserved_attempt(
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
    proxy: str,
    proxy_failure: str,
) -> dict[str, Any]:
    names = {
        "riemann": "Riemann Hypothesis",
        "collatz": "Collatz Conjecture",
        "goldbach": "Goldbach Conjecture",
    }
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "legacy_proxy_rejected_problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "reject a finite proxy and preserve the independent infinite target",
        "attempt": f"Audit and discard {proxy} as a proof route without transferring the Twin ratio bridge.",
        "bounded_result": {
            "source_ticket": f"{ticket_id.split('-')[0]}-TICKET-122",
            "discarded_legacy_proxy": proxy,
            "proxy_failure": proxy_failure,
            "independent_target": target,
        },
        "obstruction": proxy_failure,
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with a problem-specific proof and counterexample oracle.",
        "claim_boundary": f"No {names[problem_id]} proof and no certified counterexample.",
    }


def build_attempts() -> list[dict[str, Any]]:
    return [
        _preserved_attempt(
            "riemann",
            "RH-TICKET-123",
            "NonCircularKernelPositivityPreservedAfterFiniteJensenNoGo",
            "NonCircularExplicitFormulaKernelPositivity",
            "finite Jensen-polynomial hyperbolicity",
            "Any finite family of hyperbolic Jensen polynomials leaves all untested degrees and shifts open and does not locate every nontrivial zeta zero.",
        ),
        _preserved_attempt(
            "collatz",
            "CO-TICKET-123",
            "GoldenMeanEscapePreservedAfterFiniteStoppingNoGo",
            "GoldenMeanInvariantSetEscape",
            "finite stopping-time and density verification",
            "A finite stopping-time loop either terminates only on verified inputs or silently assumes the missing descent; density-one behavior permits a sparse exceptional orbit.",
        ),
        _preserved_attempt(
            "goldbach",
            "GB-TICKET-123",
            "JointBalancedGoldbachPreservedAfterMeanSeriesNoGo",
            "JointBalancedVaughanGoldbachResidualEnvelope",
            "finite mean singular-series agreement",
            "Mean or density agreement permits sparse zero representation counts and therefore cannot prove pointwise positivity for every large even integer.",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-123",
            "status": "exact_ratio_bridge_proved_independent_premise_nogos_open",
            "route": "CanonicalDefectRatioClosureBridge",
            "proof_or_counterexample_mode": "exact normalized bridge, premise no-go families, and finite bottleneck attribution",
            "attempt": "Factor the TICKET-122 full margin into saving, singleton-to-known, and boundary ratios, then identify the exact compatibility condition.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-122",
                "audit_ref": "canonical_defect_ratio_closure_bridge",
            },
            "obstruction": "No uniform compatible eta-rho-epsilon tuple is proved for every sufficiently large Vaughan scale.",
            "candidate_theorem": "VaughanCanonicalDefectRatioTriple",
            "next_experiment": "Attack D/S, S/K, and E/K with separate arithmetic estimators while checking the compatibility plane before combining them.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]


def main() -> int:
    audit = build_audit()
    attempts = build_attempts()
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_ratio_bridge_and_independent_premise_nogos_open",
        "claim_boundary": audit["proof_boundary"],
        "canonical_defect_ratio_closure_bridge": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket123-canonical-defect-ratio-closure-bridge.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-123-finite-jensen-proxy-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-123-finite-stopping-proxy-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-123-mean-series-proxy-no-go.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-123-defect-ratio-closure-bridge.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
