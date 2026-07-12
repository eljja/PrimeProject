from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import prime_sieve, von_mangoldt_values
from ticket95_sharp_contamination_and_equivalence_audit import (
    proper_prime_power_mass_prefix,
    sharp_goldbach_contamination_bound,
    sharp_twin_contamination_bound,
)
from ticket97_periodic_projection_residual_audit import additive_coefficient, shift_two_coefficient
from ticket98_growing_modulus_leakage_audit import PRIMORIAL_MODULI


GENERATED_AT = "2026-07-13T03:10:00+09:00"
SCHEMA = "primeproject.ticket99-out-of-sample-local-model-audit.v1"
CHECKPOINTS = (10_000, 100_000, 1_000_000)
MINIMUM_TRAIN_COUNTS = (1, 2, 4, 8, 16)
ENVELOPE_START = 1_000
CALIBRATION_CEILING = 100_000


def external_coprime_model(length: int, modulus: int) -> tuple[np.ndarray, int]:
    coprime = np.array([math.gcd(residue, modulus) == 1 for residue in range(modulus)])
    phi = int(coprime.sum())
    indices = np.arange(length)
    model = np.where(coprime[indices % modulus], modulus / phi, 0.0)
    return model, phi


def local_pair_density_floor(modulus: int) -> dict[str, Any]:
    model, phi = external_coprime_model(modulus, modulus)
    admissible = sum(
        int(math.gcd(residue, modulus) == 1 and math.gcd(residue + 2, modulus) == 1)
        for residue in range(modulus)
    )
    density = (modulus / phi) ** 2 * admissible / modulus
    return {
        "modulus": modulus,
        "phi": phi,
        "minimum_admissible_residues_per_period": admissible,
        "minimum_pair_density": density,
        "model_period_energy": float(np.dot(model, model)),
    }


def _norm_lower_bounds(
    projection: np.ndarray,
    residual: np.ndarray,
    target: int,
) -> tuple[float, float]:
    goldbach_main = additive_coefficient(projection, projection, target)
    p_norm = float(np.linalg.norm(projection[: target + 1]))
    e_norm = float(np.linalg.norm(residual[: target + 1]))
    goldbach_lower = goldbach_main - 2 * p_norm * e_norm - e_norm * e_norm

    twin_main = shift_two_coefficient(projection, projection, target)
    p_left = float(np.linalg.norm(projection[: target + 1]))
    p_right = float(np.linalg.norm(projection[2 : target + 3]))
    e_left = float(np.linalg.norm(residual[: target + 1]))
    e_right = float(np.linalg.norm(residual[2 : target + 3]))
    twin_lower = twin_main - p_left * e_right - e_left * p_right - e_left * e_right
    return goldbach_lower, twin_lower


def audit_cross_fitted_checkpoint(
    values: np.ndarray,
    target: int,
    goldbach_budget: float,
    twin_budget: float,
) -> dict[str, Any]:
    indices = np.arange(len(values))
    configurations: list[dict[str, Any]] = []
    reconstruction_failures = 0

    for modulus in PRIMORIAL_MODULI:
        if modulus >= len(values):
            for minimum in MINIMUM_TRAIN_COUNTS:
                configurations.append(
                    {
                        "modulus": modulus,
                        "minimum_train_count": minimum,
                        "evaluation_count": 0,
                        "status": "empty_no_shared_train_residue",
                    }
                )
            continue

        residues = indices % modulus
        periods = indices // modulus
        train_mask = periods % 2 == 0
        evaluation_mask = ~train_mask
        train_counts = np.bincount(residues[train_mask], minlength=modulus)
        train_sums = np.bincount(residues[train_mask], weights=values[train_mask], minlength=modulus)
        train_means = np.divide(
            train_sums,
            train_counts,
            out=np.zeros_like(train_sums),
            where=train_counts > 0,
        )

        for minimum in MINIMUM_TRAIN_COUNTS:
            eligible = evaluation_mask & (train_counts[residues] >= minimum)
            evaluation_count = int(eligible.sum())
            if evaluation_count == 0:
                configurations.append(
                    {
                        "modulus": modulus,
                        "minimum_train_count": minimum,
                        "evaluation_count": 0,
                        "status": "empty_minimum_occupancy_not_met",
                    }
                )
                continue

            observed = np.where(eligible, values, 0.0)
            projection = np.where(eligible, train_means[residues], 0.0)
            residual = observed - projection
            goldbach_main = additive_coefficient(projection, projection, target)
            goldbach_signed = (
                additive_coefficient(projection, residual, target)
                + additive_coefficient(residual, projection, target)
                + additive_coefficient(residual, residual, target)
            )
            goldbach_exact = additive_coefficient(observed, observed, target)
            twin_main = shift_two_coefficient(projection, projection, target)
            twin_signed = (
                shift_two_coefficient(projection, residual, target)
                + shift_two_coefficient(residual, projection, target)
                + shift_two_coefficient(residual, residual, target)
            )
            twin_exact = shift_two_coefficient(observed, observed, target)
            goldbach_lower, twin_lower = _norm_lower_bounds(projection, residual, target)
            goldbach_error = abs(goldbach_exact - goldbach_main - goldbach_signed) / max(
                1.0, abs(goldbach_exact), abs(goldbach_main), abs(goldbach_signed)
            )
            twin_error = abs(twin_exact - twin_main - twin_signed) / max(
                1.0, abs(twin_exact), abs(twin_main), abs(twin_signed)
            )
            reconstruction_failures += int(goldbach_error > 1e-12) + int(twin_error > 1e-12)
            configurations.append(
                {
                    "modulus": modulus,
                    "minimum_train_count": minimum,
                    "evaluation_count": evaluation_count,
                    "evaluation_fraction": evaluation_count / len(values),
                    "train_evaluation_overlap_count": 0,
                    "goldbach_exact_restricted_correlation": goldbach_exact,
                    "goldbach_norm_only_lower_bound": goldbach_lower,
                    "goldbach_margin_over_full_contamination_budget": goldbach_lower - goldbach_budget,
                    "goldbach_exact_reconstruction_relative_error": goldbach_error,
                    "goldbach_certified": goldbach_lower > goldbach_budget,
                    "twin_exact_restricted_correlation": twin_exact,
                    "twin_norm_only_lower_bound": twin_lower,
                    "twin_margin_over_full_contamination_budget": twin_lower - twin_budget,
                    "twin_exact_reconstruction_relative_error": twin_error,
                    "twin_certified": twin_lower > twin_budget,
                    "status": "nonempty_data_disjoint_evaluation",
                }
            )

    nonempty = [row for row in configurations if int(row["evaluation_count"]) > 0]
    best_goldbach = max(nonempty, key=lambda row: float(row["goldbach_margin_over_full_contamination_budget"]))
    best_twin = max(nonempty, key=lambda row: float(row["twin_margin_over_full_contamination_budget"]))
    return {
        "target": target,
        "configuration_count": len(configurations),
        "nonempty_configuration_count": len(nonempty),
        "empty_configuration_count": len(configurations) - len(nonempty),
        "goldbach_certificate_count": sum(int(row["goldbach_certified"]) for row in nonempty),
        "twin_certificate_count": sum(int(row["twin_certified"]) for row in nonempty),
        "reconstruction_failure_count": reconstruction_failures,
        "best_nonempty_goldbach_row": best_goldbach,
        "best_nonempty_twin_row": best_twin,
    }


def audit_external_checkpoint(
    values: np.ndarray,
    target: int,
    goldbach_budget: float,
    twin_budget: float,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    exact_goldbach = additive_coefficient(values, values, target)
    exact_twin = shift_two_coefficient(values, values, target)

    for modulus in PRIMORIAL_MODULI:
        if modulus > target:
            continue
        projection, _ = external_coprime_model(len(values), modulus)
        residual = values - projection
        density = local_pair_density_floor(modulus)
        main_lower = float(density["minimum_pair_density"]) * max(0, target + 1 - modulus)
        goldbach_main = additive_coefficient(projection, projection, target)
        goldbach_signed = exact_goldbach - goldbach_main
        twin_main = shift_two_coefficient(projection, projection, target)
        twin_signed = exact_twin - twin_main
        goldbach_lower, twin_lower = _norm_lower_bounds(projection, residual, target)
        failures += int(goldbach_main + 1e-7 < main_lower) + int(twin_main + 1e-7 < main_lower)
        rows.append(
            {
                "modulus": modulus,
                "minimum_pair_density": density["minimum_pair_density"],
                "exact_local_main_lower_bound": main_lower,
                "goldbach_external_main": goldbach_main,
                "goldbach_signed_residual": goldbach_signed,
                "goldbach_signed_residual_over_main": goldbach_signed / goldbach_main,
                "goldbach_norm_only_lower_bound": goldbach_lower,
                "goldbach_certified": goldbach_lower > goldbach_budget,
                "twin_external_main": twin_main,
                "twin_signed_residual": twin_signed,
                "twin_signed_residual_over_main": twin_signed / twin_main,
                "twin_norm_only_lower_bound": twin_lower,
                "twin_certified": twin_lower > twin_budget,
            }
        )
    return {
        "target": target,
        "row_count": len(rows),
        "main_lower_bound_failure_count": failures,
        "goldbach_norm_certificate_count": sum(int(row["goldbach_certified"]) for row in rows),
        "twin_norm_certificate_count": sum(int(row["twin_certified"]) for row in rows),
        "rows": rows,
    }


def _transform_size(length: int) -> int:
    size = 1
    while size < 2 * length - 1:
        size *= 2
    return size


def _scheduled_modulus(number: int, moduli: tuple[int, ...]) -> int:
    selected = moduli[0]
    for modulus in moduli:
        if modulus * modulus <= number:
            selected = modulus
    return selected


def audit_finite_residual_envelope(values: np.ndarray, limit: int) -> dict[str, Any]:
    if limit <= CALIBRATION_CEILING:
        raise ValueError("screen_limit must exceed the calibration ceiling so that holdout validation is nonempty")
    schedule_moduli = tuple(modulus for modulus in PRIMORIAL_MODULI if modulus * modulus <= limit)
    transform_size = _transform_size(limit + 1)
    lambda_transform = np.fft.rfft(values[: limit + 1], transform_size)
    exact_goldbach = np.fft.irfft(lambda_transform * lambda_transform, transform_size)[: limit + 1]
    exact_twin = np.cumsum(values[: limit + 1] * values[2 : limit + 3])
    models: dict[int, np.ndarray] = {}
    goldbach_main: dict[int, np.ndarray] = {}
    twin_main: dict[int, np.ndarray] = {}
    for modulus in schedule_moduli:
        model, _ = external_coprime_model(limit + 3, modulus)
        models[modulus] = model
        transform = np.fft.rfft(model[: limit + 1], transform_size)
        goldbach_main[modulus] = np.fft.irfft(transform * transform, transform_size)[: limit + 1]
        twin_main[modulus] = np.cumsum(model[: limit + 1] * model[2 : limit + 3])

    def envelope_row(kind: str, number: int) -> dict[str, Any]:
        modulus = _scheduled_modulus(number, schedule_moduli)
        exact = float(exact_goldbach[number] if kind == "goldbach" else exact_twin[number])
        main = float(goldbach_main[modulus][number] if kind == "goldbach" else twin_main[modulus][number])
        ratio = (exact - main) / main
        required_constant = max(0.0, -ratio) * math.log(number)
        return {
            "number": number,
            "modulus": modulus,
            "exact_correlation": exact,
            "external_main": main,
            "signed_residual": exact - main,
            "signed_residual_over_main": ratio,
            "required_log_envelope_constant": required_constant,
        }

    goldbach_rows = [envelope_row("goldbach", number) for number in range(ENVELOPE_START, limit + 1, 2)]
    twin_rows = [envelope_row("twin", number) for number in range(ENVELOPE_START, limit + 1)]

    def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
        calibration = [row for row in rows if int(row["number"]) <= CALIBRATION_CEILING]
        validation = [row for row in rows if int(row["number"]) > CALIBRATION_CEILING]
        calibration_max = max(calibration, key=lambda row: float(row["required_log_envelope_constant"]))
        validation_max = max(validation, key=lambda row: float(row["required_log_envelope_constant"]))
        return {
            "calibration_count": len(calibration),
            "validation_count": len(validation),
            "calibration_maximum_row": calibration_max,
            "validation_maximum_row": validation_max,
        }

    goldbach_summary = summarize(goldbach_rows)
    twin_summary = summarize(twin_rows)
    calibration_maximum = max(
        float(goldbach_summary["calibration_maximum_row"]["required_log_envelope_constant"]),
        float(twin_summary["calibration_maximum_row"]["required_log_envelope_constant"]),
    )
    candidate_constant = math.ceil(calibration_maximum * 10) / 10
    goldbach_validation_failures = sum(
        int(float(row["required_log_envelope_constant"]) > candidate_constant + 1e-12)
        for row in goldbach_rows
        if int(row["number"]) > CALIBRATION_CEILING
    )
    twin_validation_failures = sum(
        int(float(row["required_log_envelope_constant"]) > candidate_constant + 1e-12)
        for row in twin_rows
        if int(row["number"]) > CALIBRATION_CEILING
    )

    validation_targets = sorted(
        {
            ENVELOPE_START,
            CALIBRATION_CEILING,
            limit,
            int(goldbach_summary["calibration_maximum_row"]["number"]),
            int(goldbach_summary["validation_maximum_row"]["number"]),
        }
    )
    direct_rows: list[dict[str, Any]] = []
    maximum_fft_error = 0.0
    for target in validation_targets:
        if target % 2 != 0:
            continue
        modulus = _scheduled_modulus(target, schedule_moduli)
        direct_exact = additive_coefficient(values, values, target)
        direct_main = additive_coefficient(models[modulus], models[modulus], target)
        exact_error = abs(direct_exact - exact_goldbach[target])
        main_error = abs(direct_main - goldbach_main[modulus][target])
        maximum_fft_error = max(maximum_fft_error, exact_error, main_error)
        direct_rows.append(
            {
                "target": target,
                "modulus": modulus,
                "exact_fft_error": exact_error,
                "main_fft_error": main_error,
            }
        )

    return {
        "method": "double-precision all-scale discovery screen with direct Goldbach replay at extrema and boundaries",
        "screen_limit": limit,
        "screen_start": ENVELOPE_START,
        "calibration_ceiling": CALIBRATION_CEILING,
        "schedule": "W(n) is the largest primorial modulus in the chain with W(n)^2<=n",
        "schedule_moduli_reached": list(schedule_moduli),
        "candidate_log_envelope_constant": candidate_constant,
        "candidate_inequality": "R_W(n)>=-K M_W(n)/log(n)",
        "goldbach": goldbach_summary,
        "twin": twin_summary,
        "goldbach_validation_failure_count": goldbach_validation_failures,
        "twin_validation_failure_count": twin_validation_failures,
        "direct_validation_rows": direct_rows,
        "maximum_fft_direct_error": maximum_fft_error,
        "status": "finite_candidate_survived_holdout_not_an_asymptotic_theorem",
    }


def analyze_out_of_sample_local_models(
    checkpoints: tuple[int, ...] = CHECKPOINTS,
    screen_limit: int = 1_000_000,
) -> dict[str, Any]:
    maximum = max(max(checkpoints), screen_limit)
    is_prime, primes = prime_sieve(maximum + 2)
    mangoldt = von_mangoldt_values(maximum + 2, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum + 2, is_prime, mangoldt)
    values = np.zeros(maximum + 3, dtype=np.float64)
    for value, weight in mangoldt.items():
        if value <= maximum + 2:
            values[value] = weight

    cross_fit_rows: list[dict[str, Any]] = []
    external_rows: list[dict[str, Any]] = []
    for target in checkpoints:
        goldbach_budget = sharp_goldbach_contamination_bound(target, mass_prefix)
        twin_budget = sharp_twin_contamination_bound(target, mass_prefix)
        checkpoint_values = values[: target + 3]
        cross_fit_rows.append(audit_cross_fitted_checkpoint(checkpoint_values, target, goldbach_budget, twin_budget))
        external_rows.append(audit_external_checkpoint(checkpoint_values, target, goldbach_budget, twin_budget))

    envelope = audit_finite_residual_envelope(values, screen_limit)
    cross_fit_failures = sum(int(row["reconstruction_failure_count"]) for row in cross_fit_rows)
    external_failures = sum(int(row["main_lower_bound_failure_count"]) for row in external_rows)
    certificate_failures = sum(int(row["goldbach_certificate_count"]) + int(row["twin_certificate_count"]) for row in cross_fit_rows)
    certificate_failures += sum(int(row["goldbach_norm_certificate_count"]) + int(row["twin_norm_certificate_count"]) for row in external_rows)
    envelope_failures = (
        int(envelope["goldbach_validation_failure_count"])
        + int(envelope["twin_validation_failure_count"])
        + int(float(envelope["maximum_fft_direct_error"]) > 1e-5)
    )
    total_failures = cross_fit_failures + external_failures + certificate_failures + envelope_failures
    return {
        "theorem_name": "OutOfSampleAndExternalLocalModelResidualAudit",
        "source_ticket": "TICKET-98",
        "cross_fit_contract": {
            "split": "For n=r+qW, even q periods train the residue mean and odd q periods form the evaluation set.",
            "disjointness": "No evaluated Lambda value is used to estimate its projection value.",
            "occupancy": "An evaluation index is admitted only when its residue has at least m training observations, for preregistered m in {1,2,4,8,16}.",
            "scope": "This is deterministic data separation, not probabilistic independence and not a prime-distribution theorem.",
        },
        "external_local_main_theorem": {
            "model": "A_W(n)=W/phi(W) when gcd(n,W)=1 and zero otherwise; it uses W only and no Lambda samples.",
            "density": "d_W=2 product_{3<=p|W}(1-1/(p-1)^2).",
            "goldbach_lower": "For even N, sum_{n<=N} A_W(n)A_W(N-n) >= d_W max(0,N+1-W).",
            "twin_lower": "For x>=0, sum_{n<=x} A_W(n)A_W(n+2) >= d_W max(0,x+1-W).",
            "proof": "CRT leaves one admissible class mod 2 and at least p-2 classes for every odd p|W; each complete W-block contributes their product. The boundary is discarded.",
            "uniform_positivity": "The decreasing d_W product has a positive limit because sum_p 1/(p-1)^2 converges.",
        },
        "sufficient_residual_theorem": {
            "candidate": "For W(n) the largest primorial with W(n)^2<=n, prove R_W(n)>=-K M_W(n)/log(n) uniformly for all sufficiently large relevant n.",
            "goldbach_implication": "For every sufficiently large even N, C_G=M_G+R_G>=M_G(1-K/log N), while the sharp proper-prime-power budget is o(N); hence every such N has a prime representation after finite verification.",
            "twin_implication": "C_2(x)>=M_2(x)(1-K/log x) is linear while the sharp contamination budget is o(x), forcing unbounded genuine twin-prime weight.",
            "independence_requirement": "The residual estimate must be proved from Type II, dispersion, or higher-order arithmetic information without reading the target correlation C_G or C_2.",
            "known_barrier": "The modulus schedule grows near the square-root scale; one-point progression control and generic transference do not supply the required binary signed estimate.",
        },
        "machine_audit": {
            "checkpoint_count": len(checkpoints),
            "maximum_checkpoint": max(checkpoints),
            "cross_fit_configuration_count": sum(int(row["configuration_count"]) for row in cross_fit_rows),
            "cross_fit_goldbach_certificate_count": sum(int(row["goldbach_certificate_count"]) for row in cross_fit_rows),
            "cross_fit_twin_certificate_count": sum(int(row["twin_certificate_count"]) for row in cross_fit_rows),
            "external_goldbach_norm_certificate_count": sum(int(row["goldbach_norm_certificate_count"]) for row in external_rows),
            "external_twin_norm_certificate_count": sum(int(row["twin_norm_certificate_count"]) for row in external_rows),
            "cross_fit_failure_count": cross_fit_failures,
            "external_main_failure_count": external_failures,
            "envelope_validation_failure_count": envelope_failures,
            "total_failure_count": total_failures,
            "cross_fit_checkpoint_rows": cross_fit_rows,
            "external_checkpoint_rows": external_rows,
            "finite_residual_envelope_screen": envelope,
        },
        "theorem_status": (
            "data_separation_and_external_local_main_proved_finite_residual_candidate_survived_no_resolution"
            if total_failures == 0
            else "ticket99_out_of_sample_audit_inconclusive_no_resolution"
        ),
        "discarded_routes": [
            "Select an empty evaluation set because its zero lower bound is numerically less negative.",
            "Use a fitted projection on the same target values being certified.",
            "Treat the finite K/log(n) holdout screen as an all-scale residual theorem.",
            "Use one-point W-trick pseudorandomness as if it resolved affine-degenerate binary correlations.",
        ],
        "goldbach_next_theorem_target": "UniformExternalLocalModelGoldbachResidualDecay",
        "twin_next_theorem_target": "UniformExternalLocalModelShiftTwoResidualDecay",
        "retained_route": "Prove the signed external-model residual envelope independently; use finite screens only to falsify constants and locate worst cases.",
        "proof_boundary": "TICKET99 proves data-separation and external local-main contracts and reports a finite residual-envelope candidate. It does not prove any of the four conjectures or a counterexample.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "out_of_sample_external_model_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "data-separated and externally specified local-model transfer",
        "attempt": "Require every fitted structural component to be estimated away from the evaluated target, or specify it arithmetically without target samples.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket99_transfer": route, "independent_target": target},
        "obstruction": "No target-specific uniform signed residual theorem was proved in TICKET99.",
        "candidate_theorem": target,
        "next_experiment": "State an external main model and falsify a quantitative residual envelope on disjoint finite data before attempting an all-scale proof.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket98 = read_json(ROOT / "data/open-problem/ticket98-growing-modulus-leakage-audit.json")
    audit = analyze_out_of_sample_local_models()
    attempts = [
        transfer_attempt(ticket98, "riemann", "RH-TICKET-99", "ExternalKernelModelResidualGate", "ExternallySpecifiedKernelConeResidualDecay"),
        transfer_attempt(ticket98, "collatz", "CO-TICKET-99", "OutOfSampleNaturalOrbitResidualGate", "OutOfSampleNaturalOrbitSignedDrift"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-99",
            "route": "OutOfSampleAndExternalGoldbachLocalModelAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "cross-fit leakage control plus external coprime main theorem",
            "attempt": "Replace fitted row-unique residue means by disjoint estimates and a target-independent W-local model, then isolate the signed residual theorem.",
            "bounded_result": {"source_ticket": "GB-TICKET-98", "audit_ref": "out_of_sample_local_model_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Attack the uniform external-model residual bound with Type II or dispersion estimates and use the finite K=1.6 screen only as a falsifier.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-99",
            "route": "OutOfSampleAndExternalTwinLocalModelAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "cross-fit leakage control plus external coprime main theorem",
            "attempt": "Replace fitted row-unique residue means by disjoint estimates and a target-independent W-local model, then isolate the shift-two signed residual theorem.",
            "bounded_result": {"source_ticket": "TP-TICKET-98", "audit_ref": "out_of_sample_local_model_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Attack the uniform shift-two external-model residual bound with Type II information and use the finite K=1.6 screen only as a falsifier.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "out_of_sample_and_external_local_models_audited_signed_residual_theorem_open_no_resolution",
        "claim_boundary": "TICKET99 removes fitted-target leakage and proves the external local main bound, but the signed binary residual theorem remains open.",
        "out_of_sample_local_model_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket99-out-of-sample-local-model-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-99-external-kernel-residual.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-99-out-of-sample-drift.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-99-external-local-residual.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-99-external-local-residual.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
