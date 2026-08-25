from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket242-quantifier-order-parseval-diagonal-crt.v1"
AUDIT_KEY = "quantifier_order_parseval_diagonal_crt_audit"


def verify_ticket242_structure() -> str | None:
    integrated = (
        ROOT
        / "data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json"
    )
    if not integrated.exists():
        return "missing TICKET-242 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-242 schema or status changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "route_correction_count": 4,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "conjecture_resolution_count": 0,
        "bounded_order_scan_limit": 200_000,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if machine.get(key) != expected:
            return f"TICKET-242 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
            "UniformSignedGuinandWeilTailBoundOnFrequencyTightNormalizedAdmissibleTestClasses",
        ),
        "collatz": (
            "collatz",
            "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
            "UniformOrderCoreSquareDivisorTransferFrom32Over27To2Over3",
        ),
        "goldbach": (
            "goldbach",
            "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
            "FixedBinaryPrimeMinorArcCoefficientIsLittleOOfTargetMainUniformlyOnBufferedEvenTargets",
        ),
        "twin_prime": (
            "twin-prime",
            "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
            "ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
        ),
    }
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-242-moving-vector-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-242-order-core-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-242-parseval-scale-no-go.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-242-growing-period-diagonal-crt.json",
    }
    for key, (problem_id, theorem, next_lemma) in expected.items():
        track = root.get(key, {})
        if track.get("problem_id") != problem_id:
            return f"TICKET-242 problem_id changed: {key}"
        if track.get("theorem_name") != theorem:
            return f"TICKET-242 theorem changed: {key}"
        if track.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-242 next lemma changed: {key}"
        nodes = track.get("proof_dag", {}).get("nodes", [])
        if len(nodes) != 4 or not any(
            node.get("status") == "highest_risk_open" for node in nodes
        ):
            return f"TICKET-242 proof DAG changed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-242 track JSON: {key}"
        track_payload = json.loads(paths[key].read_text(encoding="utf-8"))
        if track_payload.get("schema") != SCHEMA:
            return f"TICKET-242 track schema changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if (
        len(rh.get("moving_vector_rows", [])) != 6
        or rh.get("transcript_sha256")
        != "f694cbcb62bd7a5fbe6cb3ade6516ceddb753012675f000aa9970cad15226e4f"
    ):
        return "TICKET-242 RH moving-vector rows changed"

    collatz = root["collatz"]["reproducible_computation"]
    scan = collatz.get("bounded_identity_scan", {})
    if (
        scan.get("odd_primes_scanned") != 17_981
        or scan.get("order_core_lifting_identity_failures") != 0
        or scan.get("largest_order_seen") != 199_998
    ):
        return "TICKET-242 Collatz order-core scan changed"

    goldbach = root["goldbach"]["reproducible_computation"]
    if len(goldbach.get("parseval_scale_rows", [])) != 7:
        return "TICKET-242 Goldbach Parseval rows changed"

    twin = root["twin_prime"]["reproducible_computation"]
    rows = twin.get("growing_modulus_diagonal_crt_rows", [])
    if len(rows) != 6 or rows[-1].get("strictly_increasing_prime_witness_p_j") != 902_071_199:
        return "TICKET-242 Twin diagonal CRT rows changed"

    attempts = payload.get("attempts", [])
    if (
        [attempt.get("problem_id") for attempt in attempts]
        != ["riemann", "collatz", "goldbach", "twin-prime"]
        or any(attempt.get("status") != "open_not_proven" for attempt in attempts)
    ):
        return "TICKET-242 attempt boundary changed"
    return None


def main() -> int:
    error = verify_ticket242_structure()
    if error:
        print(error)
        return 1
    print("TICKET-242 structure verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
