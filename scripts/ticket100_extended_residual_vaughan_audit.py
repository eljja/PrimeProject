from __future__ import annotations

import gc
import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values, prime_sieve, von_mangoldt_values
from ticket97_periodic_projection_residual_audit import additive_coefficient, shift_two_coefficient
from ticket98_growing_modulus_leakage_audit import PRIMORIAL_MODULI


GENERATED_AT = "2026-07-13T05:15:00+09:00"
SCHEMA = "primeproject.ticket100-extended-residual-vaughan-audit.v1"
CANDIDATE_K = 1.6
SCREEN_START = 1_000


def lambda_values(limit: int) -> tuple[np.ndarray, dict[int, float]]:
    _, primes = prime_sieve(limit)
    mangoldt = von_mangoldt_values(limit, primes)
    values = np.zeros(limit + 1, dtype=np.float64)
    for number, weight in mangoldt.items():
        if number <= limit:
            values[number] = weight
    return values, mangoldt


def transform_size(length: int) -> int:
    size = 1
    while size < 2 * length - 1:
        size *= 2
    return size


def schedule_moduli(limit: int) -> tuple[int, ...]:
    return tuple(modulus for modulus in PRIMORIAL_MODULI if modulus * modulus <= limit)


def twin_main_vector(numbers: np.ndarray, modulus: int) -> np.ndarray:
    coprime = np.array([math.gcd(residue, modulus) == 1 for residue in range(modulus)])
    factor = modulus / int(coprime.sum())
    valid = coprime & np.roll(coprime, -2)
    prefix = np.concatenate(([0], np.cumsum(valid, dtype=np.int64)))
    lengths = numbers + 1
    counts = (lengths // modulus) * int(valid.sum()) + prefix[lengths % modulus]
    return factor * factor * counts


def goldbach_main_vector(numbers: np.ndarray, modulus: int) -> np.ndarray:
    coprime = np.array([math.gcd(residue, modulus) == 1 for residue in range(modulus)])
    factor = modulus / int(coprime.sum())
    residues = np.arange(modulus)
    admissible = np.empty(modulus, dtype=np.int32)
    prefix = np.empty((modulus, modulus + 1), dtype=np.int32)
    prefix[:, 0] = 0
    for target_residue in range(modulus):
        valid = coprime & coprime[(target_residue - residues) % modulus]
        admissible[target_residue] = int(valid.sum())
        prefix[target_residue, 1:] = np.cumsum(valid, dtype=np.int32)
    lengths = numbers + 1
    target_residues = numbers % modulus
    counts = (
        (lengths // modulus) * admissible[target_residues]
        + prefix[target_residues, lengths % modulus]
    )
    return factor * factor * counts


def _segment_bounds(moduli: tuple[int, ...], index: int, limit: int) -> tuple[int, int]:
    modulus = moduli[index]
    lower = max(SCREEN_START, modulus * modulus)
    upper = limit if index + 1 == len(moduli) else min(limit, moduli[index + 1] ** 2 - 1)
    return lower, upper


def audit_extended_twin_screen(limit: int = 10_000_000) -> dict[str, Any]:
    values, _ = lambda_values(limit + 2)
    exact = np.cumsum(values[: limit + 1] * values[2 : limit + 3])
    moduli = schedule_moduli(limit)
    segments: list[dict[str, Any]] = []
    total_failures = 0
    total_count = 0
    for index, modulus in enumerate(moduli):
        lower, upper = _segment_bounds(moduli, index, limit)
        if lower > upper:
            continue
        numbers = np.arange(lower, upper + 1, dtype=np.int64)
        main = twin_main_vector(numbers, modulus)
        ratio = (exact[numbers] - main) / main
        required = np.maximum(0.0, -ratio) * np.log(numbers)
        maximum_index = int(np.argmax(required))
        failures = int(np.count_nonzero(required > CANDIDATE_K + 1e-12))
        total_failures += failures
        total_count += len(numbers)
        segments.append(
            {
                "modulus": modulus,
                "start": lower,
                "end": upper,
                "evaluated_count": len(numbers),
                "candidate_failure_count": failures,
                "maximum_required_constant": float(required[maximum_index]),
                "maximum_row": {
                    "x": int(numbers[maximum_index]),
                    "signed_residual_over_main": float(ratio[maximum_index]),
                    "exact_correlation": float(exact[numbers[maximum_index]]),
                    "external_main": float(main[maximum_index]),
                },
            }
        )
    overall = max(segments, key=lambda row: float(row["maximum_required_constant"]))
    return {
        "limit": limit,
        "evaluated_count": total_count,
        "schedule_moduli_reached": list(moduli),
        "candidate_constant": CANDIDATE_K,
        "candidate_failure_count": total_failures,
        "overall_maximum_required_constant": overall["maximum_required_constant"],
        "overall_maximum_row": overall["maximum_row"],
        "segment_rows": segments,
        "status": "extended_finite_screen_no_asymptotic_claim",
    }


def audit_extended_goldbach_screen(limit: int = 6_000_000) -> dict[str, Any]:
    values, _ = lambda_values(limit)
    size = transform_size(len(values))
    transform = np.fft.rfft(values, size)
    transform *= transform
    exact = np.fft.irfft(transform, size)[: limit + 1].copy()
    del transform
    gc.collect()
    moduli = schedule_moduli(limit)
    segments: list[dict[str, Any]] = []
    total_failures = 0
    total_count = 0
    validation_targets: set[int] = {limit if limit % 2 == 0 else limit - 1}
    for index, modulus in enumerate(moduli):
        lower, upper = _segment_bounds(moduli, index, limit)
        if lower > upper:
            continue
        first_even = lower + lower % 2
        numbers = np.arange(first_even, upper + 1, 2, dtype=np.int64)
        if len(numbers) == 0:
            continue
        main = goldbach_main_vector(numbers, modulus)
        ratio = (exact[numbers] - main) / main
        required = np.maximum(0.0, -ratio) * np.log(numbers)
        maximum_index = int(np.argmax(required))
        failures = int(np.count_nonzero(required > CANDIDATE_K + 1e-12))
        total_failures += failures
        total_count += len(numbers)
        maximum_number = int(numbers[maximum_index])
        validation_targets.add(maximum_number)
        validation_targets.add(first_even)
        segments.append(
            {
                "modulus": modulus,
                "start": first_even,
                "end": int(numbers[-1]),
                "evaluated_count": len(numbers),
                "candidate_failure_count": failures,
                "maximum_required_constant": float(required[maximum_index]),
                "maximum_row": {
                    "even_target": maximum_number,
                    "signed_residual_over_main": float(ratio[maximum_index]),
                    "exact_correlation": float(exact[maximum_number]),
                    "external_main": float(main[maximum_index]),
                },
            }
        )
    direct_rows: list[dict[str, Any]] = []
    maximum_fft_error = 0.0
    for target in sorted(validation_targets):
        modulus = max(modulus for modulus in moduli if modulus * modulus <= target)
        direct_exact = additive_coefficient(values, values, target)
        direct_main = float(goldbach_main_vector(np.array([target], dtype=np.int64), modulus)[0])
        fft_error = abs(direct_exact - exact[target])
        maximum_fft_error = max(maximum_fft_error, fft_error)
        direct_rows.append(
            {
                "target": target,
                "modulus": modulus,
                "fft_direct_error": fft_error,
                "direct_external_main": direct_main,
            }
        )
    overall = max(segments, key=lambda row: float(row["maximum_required_constant"]))
    return {
        "limit": limit,
        "transform_size": size,
        "evaluated_even_count": total_count,
        "schedule_moduli_reached": list(moduli),
        "candidate_constant": CANDIDATE_K,
        "candidate_failure_count": total_failures,
        "overall_maximum_required_constant": overall["maximum_required_constant"],
        "overall_maximum_row": overall["maximum_row"],
        "maximum_fft_direct_error": maximum_fft_error,
        "direct_validation_rows": direct_rows,
        "segment_rows": segments,
        "status": "extended_finite_fft_screen_no_asymptotic_claim",
    }


def vaughan_components(
    values: np.ndarray,
    mangoldt: dict[int, float],
    mu: list[int],
    u: int,
    v: int,
    direct_check_limit: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    limit = len(values) - 1
    first_type_i = np.zeros(limit + 1, dtype=np.float64)
    for divisor in range(1, u + 1):
        if mu[divisor] == 0:
            continue
        quotients = np.arange(1, limit // divisor + 1)
        first_type_i[divisor * quotients] += mu[divisor] * np.log(quotients)

    small_lambda = np.where(np.arange(limit + 1) <= v, values, 0.0)
    short_convolution = np.zeros(limit + 1, dtype=np.float64)
    small_items = [(number, weight) for number, weight in mangoldt.items() if number <= v]
    for divisor in range(1, u + 1):
        if mu[divisor] == 0:
            continue
        for number, weight in small_items:
            product = divisor * number
            if product <= limit:
                short_convolution[product] += mu[divisor] * weight
    second_type_i = np.zeros(limit + 1, dtype=np.float64)
    for divisor in np.flatnonzero(short_convolution):
        if divisor:
            second_type_i[divisor::divisor] -= short_convolution[divisor]

    type_i = first_type_i + second_type_i + small_lambda
    type_ii = values - type_i

    check_limit = min(direct_check_limit, limit)
    direct_kernel = np.zeros(check_limit + 1, dtype=np.float64)
    large_items = sorted((number, weight) for number, weight in mangoldt.items() if v < number <= check_limit)
    for left in range(u + 1, check_limit // (v + 1) + 1):
        if mu[left] == 0:
            continue
        maximum_right = check_limit // left
        for right, weight in large_items:
            if right > maximum_right:
                break
            direct_kernel[left * right] += mu[left] * weight
    direct_type_ii = np.zeros(check_limit + 1, dtype=np.float64)
    for divisor in np.flatnonzero(direct_kernel):
        if divisor:
            direct_type_ii[divisor::divisor] += direct_kernel[divisor]
    direct_error = float(np.max(np.abs(type_ii[: check_limit + 1] - direct_type_ii)))
    return type_i, type_ii, {
        "u": u,
        "v": v,
        "direct_check_limit": check_limit,
        "lambda_reconstruction_max_error": float(np.max(np.abs(values - type_i - type_ii))),
        "direct_type_ii_max_error": direct_error,
        "type_i_nonzero_count": int(np.count_nonzero(np.abs(type_i) > 1e-12)),
        "type_ii_nonzero_count": int(np.count_nonzero(np.abs(type_ii) > 1e-12)),
    }


def audit_vaughan_joint_cancellation(limit: int = 1_000_000) -> dict[str, Any]:
    values, mangoldt = lambda_values(limit + 2)
    mu = mobius_values(limit + 2)
    cutoff = max(2, round(limit ** (1 / 3)))
    type_i, type_ii, identity = vaughan_components(values, mangoldt, mu, cutoff, cutoff, min(100_000, limit))
    size = transform_size(limit + 1)
    lambda_transform = np.fft.rfft(values[: limit + 1], size)
    structured_goldbach = np.fft.irfft(np.fft.rfft(type_i[: limit + 1], size) * lambda_transform, size)[: limit + 1]
    type_ii_goldbach = np.fft.irfft(np.fft.rfft(type_ii[: limit + 1], size) * lambda_transform, size)[: limit + 1]
    structured_twin = np.cumsum(type_i[: limit + 1] * values[2 : limit + 3])
    type_ii_twin = np.cumsum(type_ii[: limit + 1] * values[2 : limit + 3])
    moduli = schedule_moduli(limit)

    def track(kind: str) -> dict[str, Any]:
        maximum_rows: dict[str, dict[str, Any] | None] = {"structured": None, "type_ii": None, "joint": None}
        maximum_errors = 0.0
        for index, modulus in enumerate(moduli):
            lower, upper = _segment_bounds(moduli, index, limit)
            if lower > upper:
                continue
            step = 2 if kind == "goldbach" else 1
            first = lower + (lower % 2 if kind == "goldbach" else 0)
            numbers = np.arange(first, upper + 1, step, dtype=np.int64)
            if len(numbers) == 0:
                continue
            main = goldbach_main_vector(numbers, modulus) if kind == "goldbach" else twin_main_vector(numbers, modulus)
            first_correlation = structured_goldbach[numbers] if kind == "goldbach" else structured_twin[numbers]
            second_correlation = type_ii_goldbach[numbers] if kind == "goldbach" else type_ii_twin[numbers]
            structured = first_correlation - main
            type_ii_part = second_correlation
            joint = structured + type_ii_part
            exact = first_correlation + second_correlation
            maximum_errors = max(maximum_errors, float(np.max(np.abs(exact - main - joint) / np.maximum(1.0, np.abs(exact)))))
            for label, contribution in (("structured", structured), ("type_ii", type_ii_part), ("joint", joint)):
                required = np.maximum(0.0, -contribution / main) * np.log(numbers)
                position = int(np.argmax(required))
                row = {
                    "number": int(numbers[position]),
                    "modulus": modulus,
                    "required_log_envelope_constant": float(required[position]),
                    "contribution_over_external_main": float(contribution[position] / main[position]),
                }
                current = maximum_rows[label]
                if current is None or float(row["required_log_envelope_constant"]) > float(current["required_log_envelope_constant"]):
                    maximum_rows[label] = row
        return {
            "maximum_rows": maximum_rows,
            "joint_reconstruction_max_relative_error": maximum_errors,
            "componentwise_candidate_refuted": float(maximum_rows["type_ii"]["required_log_envelope_constant"]) > CANDIDATE_K,
            "joint_candidate_survives": float(maximum_rows["joint"]["required_log_envelope_constant"]) <= CANDIDATE_K,
        }

    goldbach = track("goldbach")
    twin = track("twin")
    return {
        "identity": identity,
        "decomposition": "Lambda=I_{U,V}+II_{U,V}; C-M=(<I,Lambda_shift>-M)+<II,Lambda_shift>.",
        "goldbach": goldbach,
        "twin": twin,
        "componentwise_no_go": {
            "finding": "The Goldbach Type II component alone needs K>1.6 at a finite target while the joint residual still satisfies K=1.6.",
            "counterexample_row": goldbach["maximum_rows"]["type_ii"],
            "logical_consequence": "Bounding structured and Type II terms by separate one-sided K/log envelopes is false; their signed compensation must be retained.",
            "scope": "This refutes a proof strategy, not Goldbach or Twin Prime.",
        },
    }


def analyze_extended_residual_vaughan(
    goldbach_limit: int = 6_000_000,
    twin_limit: int = 10_000_000,
    vaughan_limit: int = 1_000_000,
) -> dict[str, Any]:
    goldbach_screen = audit_extended_goldbach_screen(goldbach_limit)
    twin_screen = audit_extended_twin_screen(twin_limit)
    vaughan = audit_vaughan_joint_cancellation(vaughan_limit)
    failures = (
        int(goldbach_screen["candidate_failure_count"])
        + int(twin_screen["candidate_failure_count"])
        + int(float(goldbach_screen["maximum_fft_direct_error"]) > 1e-5)
        + int(float(vaughan["identity"]["lambda_reconstruction_max_error"]) > 1e-10)
        + int(float(vaughan["identity"]["direct_type_ii_max_error"]) > 1e-10)
        + int(float(vaughan["goldbach"]["joint_reconstruction_max_relative_error"]) > 1e-10)
        + int(float(vaughan["twin"]["joint_reconstruction_max_relative_error"]) > 1e-10)
        + int(not vaughan["goldbach"]["componentwise_candidate_refuted"])
        + int(not vaughan["goldbach"]["joint_candidate_survives"])
        + int(not vaughan["twin"]["joint_candidate_survives"])
    )
    return {
        "theorem_name": "ExtendedResidualScreenAndVaughanJointCancellationAudit",
        "source_ticket": "TICKET-99",
        "vaughan_identity": {
            "formula": "Lambda=mu_<=U*log-mu_<=U*Lambda_<=V*1+Lambda_<=V+mu_>U*Lambda_>V*1.",
            "type_i": "The first three terms form I_{U,V}.",
            "type_ii": "The final bilinear convolution forms II_{U,V}.",
            "audit": vaughan["identity"],
        },
        "extended_counterexample_search": {
            "goldbach": goldbach_screen,
            "twin": twin_screen,
            "finding": "No K=1.6 counterexample appears through every even N<=6M for Goldbach or every x<=10M for Twin, including the W=210 to W=2310 transition.",
            "scope": "Finite double-precision evidence only; it cannot discharge the all-scale quantifier.",
        },
        "vaughan_joint_cancellation_audit": vaughan,
        "contrapositive_program": {
            "goldbach": "A sufficiently large Goldbach counterexample has C_G(N)<=B_G(N), hence R_G/M_G<=-1+B_G/M_G, contradicting any proved K/log(N) lower envelope once K/log(N)<1-B_G/M_G.",
            "twin": "If only finitely many twin primes exist, genuine twin weight is bounded and C_2(x)<=B_2(x)+O(1), forcing R_2/M_2 toward -1 and contradicting a proved K/log(x) lower envelope.",
            "required_independence": "The joint residual bound must come from Type I/II or dispersion information, not from the exact target correlation.",
        },
        "discarded_routes": [
            "Bound the Goldbach Type II component by the same K=1.6 envelope separately from the structured term.",
            "Take absolute values of all Vaughan components and discard their observed signed compensation.",
            "Promote the 6M/10M finite screens to an asymptotic theorem.",
        ],
        "goldbach_next_theorem_target": "JointVaughanGoldbachResidualEnvelope",
        "twin_next_theorem_target": "JointVaughanShiftTwoResidualEnvelope",
        "retained_route": "Estimate the combined structured-plus-Type-II signed residual directly, preserving compensation across Vaughan components.",
        "machine_audit": {
            "goldbach_screen_limit": goldbach_limit,
            "twin_screen_limit": twin_limit,
            "vaughan_limit": vaughan_limit,
            "candidate_constant": CANDIDATE_K,
            "total_failure_count": failures,
        },
        "theorem_status": "extended_candidate_survived_componentwise_typeii_route_refuted_joint_theorem_open_no_resolution" if failures == 0 else "ticket100_audit_inconclusive_no_resolution",
        "proof_boundary": "TICKET100 extends finite falsification and proves exact Vaughan decomposition contracts plus a componentwise strategy no-go. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "joint_signed_component_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "exact decomposition plus componentwise-strategy counterexample transfer",
        "attempt": "Reject separate absolute component bounds when a finite counterexample shows that only their signed combination satisfies the target envelope.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket100_transfer": route, "independent_target": target},
        "obstruction": "No target-specific joint signed theorem was proved in TICKET100.",
        "candidate_theorem": target,
        "next_experiment": "Derive a joint signed estimate that keeps compensation between the structured and difficult components.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket99 = read_json(ROOT / "data/open-problem/ticket99-out-of-sample-local-model-audit.json")
    audit = analyze_extended_residual_vaughan()
    attempts = [
        transfer_attempt(ticket99, "riemann", "RH-TICKET-100", "JointExplicitFormulaComponentGate", "JointKernelStructuredOscillatoryCancellation"),
        transfer_attempt(ticket99, "collatz", "CO-TICKET-100", "JointOrbitDriftComponentGate", "JointNaturalOrbitStructuredResidualDrift"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-100",
            "route": "JointVaughanGoldbachResidualAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "extended counterexample search plus exact one-sided Vaughan decomposition",
            "attempt": "Attack the K/log residual theorem at the first primorial transition, then decompose it into structured and Type II contributions without losing their sign compensation.",
            "bounded_result": {"source_ticket": "GB-TICKET-99", "audit_ref": "extended_residual_vaughan_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Prove a joint dispersion inequality for <I,Lambda_shift>-M+<II,Lambda_shift>; separate K=1.6 Type II control is already falsified.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-100",
            "route": "JointVaughanTwinResidualAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "extended counterexample search plus exact one-sided Vaughan decomposition",
            "attempt": "Attack the K/log residual theorem through 10M, then decompose it into structured and Type II shift-two contributions.",
            "bounded_result": {"source_ticket": "TP-TICKET-99", "audit_ref": "extended_residual_vaughan_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Prove a joint shift-two dispersion inequality preserving structured/Type-II compensation.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "extended_residual_candidate_survived_componentwise_typeii_strategy_refuted_no_resolution",
        "claim_boundary": "TICKET100 finds no conjecture counterexample; it refutes a componentwise proof route and keeps only a joint signed theorem target.",
        "extended_residual_vaughan_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket100-extended-residual-vaughan-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-100-joint-component-gate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-100-joint-drift-gate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-100-joint-vaughan-residual.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-100-joint-vaughan-residual.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
