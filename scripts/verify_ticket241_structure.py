from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket241-finite-information-canonical-errors.v1"
AUDIT_KEY = "finite_information_canonical_error_audit"


def verify_ticket241_structure() -> str | None:
    integrated = (
        ROOT / "data/open-problem/ticket241-finite-information-canonical-errors.json"
    )
    if not integrated.exists():
        return "missing TICKET-241 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA:
        return "TICKET-241 schema changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "route_correction_count": 4,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "conjecture_resolution_count": 0,
        "bounded_prime_scan_limit": 100_000_000,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if machine.get(key) != expected:
            return f"TICKET-241 machine field changed: {key}"

    expected = {
        "riemann": (
            "FinitePrimeCosineRankNoGoForRegularizedWeilPositivity",
            "SignedGuinandWeilFiniteSectionsConvergeWithoutArtificialDiagonalForEveryAdmissibleTestFamily",
            "riemann",
        ),
        "collatz": (
            "PrincipalUnitFermatLineIndependenceNoGoAndHundredMillionAudit",
            "FixedBaseFermatQuotientLineAvoidanceFor5Fq2Equals3Fq3UnlessFq2EqualsFq3",
            "collatz",
        ),
        "goldbach": (
            "CanonicalErrorContractAndRefinementInstabilityNoGo",
            "FixedBinaryPrimeArcDecompositionHasUniformTargetwisePositiveLowerCertificate",
            "goldbach",
        ),
        "twin_prime": (
            "FinitePeriodicPrimeFingerprintMimicryForShiftTwo",
            "GrowingModulusParitySensitiveTypeIIBoundForShiftTwoLambdaOnInfinitelyManyDyadicBlocks",
            "twin-prime",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-241-prime-cosine-rank-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-241-fermat-line-local-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-241-error-contract-no-go.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-241-periodic-fingerprint-no-go.json",
    }
    for key, (theorem, next_lemma, problem_id) in expected.items():
        track = root.get(key, {})
        if track.get("theorem_name") != theorem:
            return f"TICKET-241 theorem changed: {key}"
        if track.get("problem_id") != problem_id:
            return f"TICKET-241 problem_id changed: {key}"
        if track.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-241 next lemma changed: {key}"
        if len(track.get("proof_dag", {}).get("nodes", [])) != 4:
            return f"TICKET-241 proof DAG changed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-241 track JSON: {key}"
        track_payload = json.loads(paths[key].read_text(encoding="utf-8"))
        if track_payload.get("schema") != SCHEMA:
            return f"TICKET-241 track schema changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if len(rh.get("prime_cosine_rank_rows", [])) != 4:
        return "TICKET-241 RH rank rows changed"
    collatz = root["collatz"]["reproducible_computation"]
    scan = collatz.get("bounded_fixed_base_scan", {})
    if (
        scan.get("odd_primes_scanned") != 5_761_453
        or scan.get("x_depth_at_least_two_count") != 0
        or scan.get("positive_defect_candidate_count") != 0
    ):
        return "TICKET-241 Collatz bounded scan changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if goldbach.get("aggregate", {}).get("represented_rows_failing_absolute_certificate") != 14:
        return "TICKET-241 Goldbach contract rows changed"
    twin = root["twin_prime"]["reproducible_computation"]
    if len(twin.get("periodic_fingerprint_crt_rows", [])) != 5:
        return "TICKET-241 Twin periodic rows changed"
    return None


def main() -> int:
    error = verify_ticket241_structure()
    if error:
        print(error)
        return 1
    print("TICKET-241 structure verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
