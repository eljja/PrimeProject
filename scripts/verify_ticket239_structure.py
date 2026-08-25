from __future__ import annotations

import json
from pathlib import Path


SCHEMA = "primeproject.ticket239-cancellation-lifting-fourier-crt.v1"
PROBLEMS = {"riemann", "collatz", "goldbach", "twin-prime"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_ticket239_structure() -> str | None:
    path = Path("data/open-problem/ticket239-cancellation-lifting-fourier-crt.json")
    if not path.exists():
        return "missing ticket239 cancellation/lifting/Fourier/CRT audit"
    ticket = read_json(path)
    if ticket.get("schema") != SCHEMA or ticket.get("status") != "open_not_proven":
        return "ticket239 schema or status changed"

    audit = ticket.get("cancellation_lifting_fourier_crt_audit", {})
    if audit.get("machine_audit") != {
        "exact_partial_or_no_go_theorem_count": 4,
        "refuted_or_reduced_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": 0,
    }:
        return "ticket239 global machine audit changed"

    theorems = {
        "riemann": "PowerDecaySchurThresholdAndNonsummablePositiveGramNoGo",
        "collatz": "LocalLiftingDefectDichotomyAndPaletteCriterion",
        "goldbach": "MesoscopicReflectionFourierIdentityAndL2NoGo",
        "twin-prime": "UniformCRTGramIdentityAndCompositeProgressionNoGo",
    }
    next_lemmas = {
        "riemann": "ArithmeticWeilCrossBlockCotlarSteinCancellationBoundOnCofinalLogarithmicShells",
        "collatz": "RunBlockLocalLiftingDefectNonpositiveForEveryOddPrime",
        "goldbach": "MesoscopicPrimeWindowSignedFourierRemainderExceedsNegativeDCWithUniformSlack",
        "twin-prime": "ParitySensitiveTransferFromPrimeWeightedCRTOrthogonalityToPositiveTwinPrincipalMass",
    }
    track_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-239-cancellation-threshold.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-239-lifting-defect.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-239-reflection-fourier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-239-uniform-crt-no-go.json"),
    }
    sections = {
        "riemann": audit.get("riemann", {}),
        "collatz": audit.get("collatz", {}),
        "goldbach": audit.get("goldbach", {}),
        "twin-prime": audit.get("twin_prime", {}),
    }
    attempts = {row.get("problem_id"): row for row in ticket.get("attempts", [])}
    if set(attempts) != PROBLEMS:
        return "ticket239 attempts missing problems"

    required_statuses = {
        "closed_input",
        "closed",
        "refuted_or_limited",
        "highest_risk_open",
        "open_not_proven",
    }
    for problem_id, attempt in attempts.items():
        track_path = track_paths[problem_id]
        if not track_path.exists():
            return f"{problem_id}: ticket239 artifact missing"
        track = read_json(track_path)
        section = sections[problem_id]
        nodes = section.get("proof_dag", {}).get("nodes", [])
        statuses = {node.get("status") for node in nodes}
        if (
            attempt.get("status") != "open_not_proven"
            or attempt.get("new_result") != theorems[problem_id]
            or attempt.get("candidate_theorem") != next_lemmas[problem_id]
            or attempt.get("bounded_result", {}).get("failure_count") != 0
            or section.get("theorem_name") != theorems[problem_id]
            or section.get("route_decision", {}).get("next_single_lemma")
            != next_lemmas[problem_id]
            or track.get("schema") != SCHEMA
            or track.get("status") != "open_not_proven"
            or track.get("theorem_name") != theorems[problem_id]
            or track.get("next_single_lemma") != next_lemmas[problem_id]
            or not required_statuses.issubset(statuses)
            or sum(node.get("status") == "highest_risk_open" for node in nodes) != 1
            or not nodes
            or nodes[-1].get("status") != "open_not_proven"
        ):
            return f"{problem_id}: ticket239 contract changed"

    rh = sections["riemann"].get("reproducible_computation", {})
    sufficient = rh.get("exact_summable_power_decay_rows", [])
    no_go = rh.get("exact_nonsummable_positive_mixture_rows", [])
    if (
        [row.get("shell_count_J") for row in sufficient] != [4, 8, 16, 32, 64]
        or [row.get("shell_count_J") for row in no_go] != [4, 8, 16, 32, 64]
        or any(row.get("certificate_verified") is not True for row in sufficient + no_go)
        or no_go[-1].get("absolute_row_sum_certificate_passes") is not False
        or rh.get("transcript_sha256")
        != "1ec85f2a1658cc80e59e119ada9b9b9980264355e18f5e9103318f2ba66e19e5"
        or rh.get("aggregate", {}).get("absolute_row_sum_necessity_refuted") is not True
        or rh.get("aggregate", {}).get("arithmetic_weil_cancellation_bound_proved") is not False
        or rh.get("aggregate", {}).get("riemann_hypothesis_resolved") is not False
    ):
        return "ticket239 RH cancellation boundary changed"

    collatz = sections["collatz"].get("reproducible_computation", {})
    scan = collatz.get("bounded_exception_scan", {})
    if (
        scan.get("prime_limit") != 200000
        or scan.get("odd_primes_scanned") != 17982
        or scan.get("positive_lifting_defect_count") != 0
        or scan.get("valuation_cap_censored_count") != 0
        or collatz.get("transcript_sha256")
        != "f9bb7522f8a4e115e11571ec70625a7a7201f7cc05311a74fbb32401be28dfe3"
        or collatz.get("aggregate", {}).get("local_lifting_defect_dichotomy_proved") is not True
        or collatz.get("aggregate", {}).get("all_odd_prime_lifting_defects_nonpositive_proved") is not False
        or collatz.get("aggregate", {}).get("collatz_conjecture_resolved") is not False
    ):
        return "ticket239 Collatz lifting boundary changed"

    goldbach = sections["goldbach"].get("reproducible_computation", {})
    fourier_rows = goldbach.get("exact_mesoscopic_prime_window_rows", [])
    if (
        len(fourier_rows) != 12
        or any(row.get("certificate_verified") is not True for row in fourier_rows)
        or goldbach.get("transcript_sha256")
        != "47c1899be5b94434d7253c6ce7edd7ed7227aa8377ce3b8665c8adfd5159aec7"
        or goldbach.get("aggregate", {}).get("cardinality_and_parseval_sufficiency_refuted") is not True
        or goldbach.get("aggregate", {}).get("prime_window_signed_phase_slack_proved") is not False
        or goldbach.get("aggregate", {}).get("strong_goldbach_conjecture_resolved") is not False
    ):
        return "ticket239 Goldbach Fourier boundary changed"

    twin = sections["twin-prime"].get("reproducible_computation", {})
    crt_rows = twin.get("exact_uniform_crt_rows", [])
    if (
        [row.get("coordinate_count_m") for row in crt_rows] != [2, 3, 4, 5, 6]
        or any(
            row.get("certificate_verified") is not True
            or row.get("uniform_crt_gram_is_identity") is not True
            or row.get("uniform_crt_effective_rank") != row.get("coordinate_count_m")
            for row in crt_rows
        )
        or twin.get("transcript_sha256")
        != "3de4a619fbaef65ad33c039cc93022074b8e5de4206246a8ae4e8aaf716de379"
        or twin.get("aggregate", {}).get("local_effective_rank_sufficiency_refuted") is not True
        or twin.get("aggregate", {}).get("prime_weighted_parity_sensitive_transfer_proved") is not False
        or twin.get("aggregate", {}).get("twin_prime_conjecture_resolved") is not False
    ):
        return "ticket239 Twin CRT boundary changed"

    if (
        "resolves none" not in str(audit.get("proof_boundary", "")).lower()
        or "resolves none" not in str(ticket.get("claim_boundary", "")).lower()
    ):
        return "ticket239 proof boundary changed"
    return None


if __name__ == "__main__":
    error = verify_ticket239_structure()
    if error:
        raise SystemExit(f"ticket239 structure verification failed: {error}")
    print("ticket239 structure verified")
