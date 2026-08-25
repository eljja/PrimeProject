from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket240-route-corrections-wieferich-prime-crt.v1"
AUDIT_KEY = "route_corrections_wieferich_prime_crt_audit"


def verify_ticket240_structure() -> str | None:
    integrated = (
        ROOT
        / "data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json"
    )
    if not integrated.exists():
        return "missing TICKET-240 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA:
        return "TICKET-240 schema changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "route_correction_count": 4,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "conjecture_resolution_count": 0,
        "bounded_prime_scan_limit": 20_000_000,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if machine.get(key) != expected:
            return f"TICKET-240 machine field changed: {key}"

    expected = {
        "riemann": (
            "CotlarNormSummabilityNoGoForUniformGramLowerBounds",
            "ArithmeticWeilSignedBlockOperatorSymbolHasUniformPositiveLowerBoundAfterCommonModeRemoval",
        ),
        "collatz": (
            "RunBlockDefectFermatQuotientReductionAndTwentyMillionAudit",
            "RationalWieferichDepthDominationFor32Over27Versus2Over3AtEveryOddPrime",
        ),
        "goldbach": (
            "SignedFourierSlackIntegralityEquivalenceAndIntermediateTargetNoGo",
            "BinaryPrimeMajorArcMainTermMinusAllExplicitErrorsIsAtLeastOneForEverySufficientlyLargeEvenTarget",
        ),
        "twin_prime": (
            "OneSidedPrimeWeightedCRTFullSupportAndCompositeSuccessorNoGo",
            "ParityBreakingTwoSidedLambdaLambdaMainTermDominatesGrowingCRTErrorOnCofinalDyadicBlocks",
        ),
    }
    track_paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-240-cotlar-norm-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-240-wieferich-depth.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-240-signed-slack-equivalence.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-240-one-sided-prime-crt.json",
    }
    for key, (theorem, next_lemma) in expected.items():
        track = root.get(key, {})
        if track.get("theorem_name") != theorem:
            return f"TICKET-240 theorem changed: {key}"
        if track.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-240 next lemma changed: {key}"
        if len(track.get("proof_dag", {}).get("nodes", [])) != 4:
            return f"TICKET-240 proof DAG changed: {key}"
        path = track_paths[key]
        if not path.exists():
            return f"missing TICKET-240 track JSON: {key}"
        track_payload = json.loads(path.read_text(encoding="utf-8"))
        if track_payload.get("schema") != SCHEMA:
            return f"TICKET-240 track schema changed: {key}"

    expected_problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for key, expected_problem_id in expected_problem_ids.items():
        if root[key].get("problem_id") != expected_problem_id:
            return f"TICKET-240 problem_id changed: {key}"

    collatz = root["collatz"]["reproducible_computation"]
    scan = collatz.get("bounded_rational_wieferich_scan", {})
    if (
        scan.get("odd_primes_scanned") != 1_270_605
        or scan.get("x_depth_at_least_two_count") != 0
        or scan.get("y_depth_at_least_two_primes") != [23]
    ):
        return "TICKET-240 Collatz bounded scan changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if goldbach.get("aggregate", {}).get("zero_restricted_window_row_count") != 1:
        return "TICKET-240 Goldbach signed-slack rows changed"
    twin = root["twin_prime"]["reproducible_computation"]
    if (
        len(twin.get("exact_all_pattern_crt_rows", [])) != 8
        or len(twin.get("actual_one_sided_prime_weighted_gram_rows", [])) != 3
    ):
        return "TICKET-240 Twin CRT rows changed"
    return None


def main() -> int:
    error = verify_ticket240_structure()
    if error:
        print(error)
        return 1
    print("TICKET-240 structure verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
