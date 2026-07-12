from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket100_extended_residual_vaughan_audit import lambda_values
from ticket104_twin_typeii_mobius_anatomy import HORIZONS, outer_mobius_weights


GENERATED_AT = "2026-07-13T15:20:00+09:00"
SCHEMA = "primeproject.ticket105-twin-centered-progression-discrepancy.v1"


def totient_values(limit: int) -> np.ndarray:
    phi = np.arange(limit + 1, dtype=np.int64)
    for prime in range(2, limit + 1):
        if phi[prime] == prime:
            phi[prime::prime] -= phi[prime::prime] // prime
    return phi


def progression_baseline_weights(horizon: int) -> tuple[np.ndarray, dict[str, Any]]:
    lower = horizon // 2 + 1
    _, mangoldt = lambda_values(horizon + 2)
    _, _, metadata = outer_mobius_weights(horizon)
    u = int(metadata["u"])
    v = int(metadata["v"])
    maximum_d = int(metadata["maximum_outer_divisor"])
    phi = totient_values(horizon)
    baseline = np.zeros(maximum_d + 1, dtype=np.float64)
    large_lambda = sorted((number, weight) for number, weight in mangoldt.items() if number > v)

    for divisor in range(u + 1, maximum_d + 1):
        maximum_r = horizon // divisor
        total = 0.0
        for number, weight in large_lambda:
            if number > maximum_r:
                break
            modulus = divisor * number
            count = horizon // modulus - (lower - 1) // modulus
            if count and modulus % 2 == 1:
                total += weight * count * modulus / int(phi[modulus])
        baseline[divisor] = total
    return baseline, {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "u": u,
        "v": v,
        "maximum_outer_divisor": maximum_d,
        "progression_model": "E[Lambda(qm+2)]=q/phi(q) when gcd(2,q)=1; zero when q is even, with exact finite multiple counts.",
    }


def audit_centered_discrepancy(horizon: int) -> dict[str, Any]:
    mu, shifted_weights, metadata = outer_mobius_weights(horizon)
    baseline_weights, baseline_meta = progression_baseline_weights(horizon)
    start = int(metadata["u"]) + 1
    end = int(metadata["maximum_outer_divisor"])
    centered_weights = shifted_weights - baseline_weights
    actual = float(np.dot(mu[start : end + 1], shifted_weights[start : end + 1]))
    baseline = float(np.dot(mu[start : end + 1], baseline_weights[start : end + 1]))
    centered = float(np.dot(mu[start : end + 1], centered_weights[start : end + 1]))
    reconstruction_error = abs(actual - baseline - centered)
    centered_slice = centered_weights[start : end + 1]
    mu_slice = mu[start : end + 1]
    centered_signed_terms = mu_slice * centered_slice
    negative_centered_mass = float(-np.sum(centered_signed_terms[centered_signed_terms < 0]))
    cauchy_envelope = float(np.linalg.norm(mu_slice) * np.linalg.norm(centered_slice))

    from ticket103_twin_local_block_audit import audit_local_block

    local = audit_local_block(horizon)
    main = float(local["local_external_main"])
    scale = math.log(horizon) / main
    correlation_denominator = float(np.linalg.norm(mu_slice) * np.linalg.norm(centered_slice))
    return {
        **baseline_meta,
        "exact_type_ii": actual,
        "progression_baseline_component": baseline,
        "centered_progression_discrepancy": centered,
        "centered_identity_absolute_error": reconstruction_error,
        "baseline_required_constant": max(0.0, -baseline) * scale,
        "centered_required_constant": max(0.0, -centered) * scale,
        "negative_centered_mass_required_constant": negative_centered_mass * scale,
        "cauchy_centered_required_constant": cauchy_envelope * scale,
        "mobius_centered_cosine": centered / correlation_denominator if correlation_denominator else 0.0,
        "centered_l2_norm": float(np.linalg.norm(centered_slice)),
        "local_external_main": main,
    }


def analyze_ticket105() -> dict[str, Any]:
    rows = [audit_centered_discrepancy(horizon) for horizon in HORIZONS]
    contract_failures = sum(int(float(row["centered_identity_absolute_error"]) > 1e-7) for row in rows)
    worst_cauchy = max(rows, key=lambda row: float(row["cauchy_centered_required_constant"]))
    worst_negative = max(rows, key=lambda row: float(row["negative_centered_mass_required_constant"]))
    return {
        "theorem_name": "CenteredProgressionTypeIIDiscrepancyAudit",
        "source_ticket": "TICKET-104",
        "exact_centering": {
            "identity": "T_X=sum mu(d)A0_X(d)+sum mu(d)(A_X(d)-A0_X(d)), with A0 using the coprime progression mean q/phi(q).",
            "baseline_independence": "A0 uses only divisibility, one-factor Lambda(r), exact block counts, and q/phi(q); it does not read Lambda(qm+2).",
            "remaining_object": "The centered term couples mu(d) to prime-distribution errors Lambda(drm+2)-dr/phi(dr) on odd progressions.",
        },
        "information_boundary": {
            "finding": "Termwise negative centered mass and Cauchy-Schwarz discard the sign alignment needed for a K/log lower bound.",
            "worst_negative_mass_row": worst_negative,
            "worst_cauchy_row": worst_cauchy,
            "scope": "Finite audited failure of these envelopes is not a no-go for dispersion, large-sieve, or bilinear estimates that retain progression structure.",
        },
        "rows": rows,
        "discarded_routes": [
            "Replace Lambda(drm+2) by a global mean 1 without parity and progression-density correction.",
            "Bound every centered outer-divisor discrepancy independently.",
            "Use Cauchy-Schwarz on the full centered d-vector as the final Type II estimate.",
            "Treat finite small cosine as proof of uniform orthogonality.",
        ],
        "next_theorem_target": "MobiusWeightedPrimeProgressionDiscrepancyBound",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET105 proves an exact finite centering identity and isolates a progression-discrepancy target. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin centered-discrepancy audit",
        "attempt": "Preserve the existing infinite target; no prime-progression shortcut is transferred across problems.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET105 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket104 = read_json(ROOT / "data/open-problem/ticket104-twin-typeii-mobius-anatomy.json")
    audit = analyze_ticket105()
    attempts = [
        transferred_attempt(ticket104, "riemann", "RH-TICKET-105", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket104, "collatz", "CO-TICKET-105", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket104, "goldbach", "GB-TICKET-105", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-105",
            "status": "progression_centering_exact_full_vector_envelopes_insufficient_open",
            "route": "CenteredPrimeProgressionTypeIIDiscrepancy",
            "proof_or_counterexample_mode": "exact independent centering plus envelope falsification",
            "attempt": "Subtract the coprime arithmetic-progression mean from each shifted-prime weight before testing Möbius cancellation.",
            "bounded_result": {"source_ticket": "TP-TICKET-104", "audit_ref": "twin_centered_progression_discrepancy"},
            "obstruction": audit["information_boundary"]["finding"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Use dispersion or bilinear large-sieve structure to control the centered progression discrepancy before absolute values are taken.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "progression_centering_exact_full_vector_envelopes_insufficient_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_centered_progression_discrepancy": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket105-twin-centered-progression-discrepancy.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-105-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-105-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-105-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-105-centered-progression-discrepancy.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
