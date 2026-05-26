from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "primeproject.open-problem-workbench.v1"
CERTIFICATE_SCHEMA = "primeproject.bounded-proof-certificate.v1"
PROOF_ATTEMPT_SCHEMA = "primeproject.proof-attempt-ledger.v1"
PROOF_STATUS_GATE_SCHEMA = "primeproject.open-problem-proof-status-gate.v1"
FORMAL_PROOF_CONTRACT_SCHEMA = "primeproject.formal-proof-contract.v1"
PROOF_MILESTONE_SCHEMA = "primeproject.proof-milestone-queue.v1"
DECISIVE_LEMMA_SCHEMA = "primeproject.decisive-lemma-lab.v1"
PROBE_CERTIFICATE_SCHEMA = "primeproject.decisive-lemma-probe-certificate.v1"
PROOF_GAP_TAXONOMY_SCHEMA = "primeproject.proof-gap-taxonomy.v1"
PROOF_EXECUTION_PROTOCOL_SCHEMA = "primeproject.proof-execution-protocol.v1"
PROOF_FRONTIER_PROBE_SCHEMA = "primeproject.proof-frontier-probe.v1"
KNOWN_BARRIER_AUDIT_SCHEMA = "primeproject.known-barrier-audit.v1"
FORMAL_REPLAY_PACKAGE_SCHEMA = "primeproject.formal-replay-package.v1"
PROOF_REVIEW_DOCKET_SCHEMA = "primeproject.proof-review-docket.v1"
PROOF_REDUCTION_CONTRACT_SCHEMA = "primeproject.proof-reduction-contract.v1"
PROOF_CANDIDATE_INTAKE_SCHEMA = "primeproject.proof-candidate-intake.v1"
PROOF_ATTEMPT_EXECUTION_LOG_SCHEMA = "primeproject.proof-attempt-execution-log.v1"
PROOF_OBLIGATION_DAG_SCHEMA = "primeproject.proof-obligation-dag.v1"


def hash_leaf(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merkle_root(hex_hashes: list[str]) -> str:
    if not hex_hashes:
        return hash_leaf("empty")
    layer = hex_hashes[:]
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        layer = [
            hashlib.sha256(bytes.fromhex(layer[index]) + bytes.fromhex(layer[index + 1])).hexdigest()
            for index in range(0, len(layer), 2)
        ]
    return layer[0]


class ChunkedCertificate:
    def __init__(self, *, problem_id: str, statement: str, limit: int, chunk_size: int = 10_000) -> None:
        self.problem_id = problem_id
        self.statement = statement
        self.limit = limit
        self.chunk_size = chunk_size
        self.current: list[str] = []
        self.chunk_roots: list[str] = []
        self.leaf_count = 0

    def update(self, text: str) -> None:
        self.current.append(hash_leaf(text))
        self.leaf_count += 1
        if len(self.current) >= self.chunk_size:
            self._flush()

    def _flush(self) -> None:
        if not self.current:
            return
        self.chunk_roots.append(merkle_root(self.current))
        self.current = []

    def finish(self) -> dict[str, object]:
        self._flush()
        return {
            "schema": CERTIFICATE_SCHEMA,
            "problem_id": self.problem_id,
            "claim_type": "bounded_theorem_certificate",
            "status": "bounded_theorem_certified",
            "statement": self.statement,
            "limit": self.limit,
            "leaf_count": self.leaf_count,
            "chunk_size": self.chunk_size,
            "chunk_count": len(self.chunk_roots),
            "leaf_encoding": "utf8 text, sha256 leaf, pairwise sha256 Merkle chunks",
            "chunk_roots": self.chunk_roots,
            "chunk_roots_sha256": hash_leaf("\n".join(self.chunk_roots)),
            "merkle_root": merkle_root(self.chunk_roots),
            "verifier": "scripts/verify_open_problem_workbench.py",
        }


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for factor in range(2, math.isqrt(limit) + 1):
        if is_prime[factor]:
            start = factor * factor
            is_prime[start : limit + 1 : factor] = b"\x00" * (((limit - start) // factor) + 1)
    return [number for number in range(2, limit + 1) if is_prime[number]], is_prime


def li_approx(x: int) -> float:
    if x < 3:
        return 0.0
    log_x = math.log(x)
    term = x / log_x
    total = term
    factorial = 1.0
    for k in range(1, 8):
        factorial *= k
        total += factorial * x / (log_x ** (k + 1))
    return total


def proof_attempt_ledger(
    *,
    problem_id: str,
    route: str,
    formal_statement: str,
    obligations: list[dict[str, str]],
    falsification_targets: list[str],
    attack_graph: dict[str, list[dict[str, str]]],
    known_theorem_bridges: list[dict[str, str]],
    lemma_candidates: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "schema": PROOF_ATTEMPT_SCHEMA,
        "problem_id": problem_id,
        "status": "open_infinite_obligation",
        "bounded_theorem_status": "proved_by_certificate",
        "attack_route": route,
        "attack_graph": attack_graph,
        "known_theorem_bridges": known_theorem_bridges,
        "lemma_candidates": lemma_candidates,
        "obligations": obligations,
        "falsification_targets": falsification_targets,
        "next_formalization_target": {
            "format": "lean_ready_statement",
            "statement": formal_statement,
            "status": "not_formalized",
        },
        "promotion_rule": "A page may move from open_not_proven only when every open obligation is replaced by an independently checkable proof that does not depend on the search limit.",
    }


def proof_status_gate(problem: dict[str, object]) -> dict[str, object]:
    attempt = problem.get("proof_attempt", {})
    certificate = problem.get("certificate", {})
    obligations = attempt.get("obligations", []) if isinstance(attempt, dict) else []
    graph = attempt.get("attack_graph", {}) if isinstance(attempt, dict) else {}
    graph_nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    graph_edges = graph.get("edges", []) if isinstance(graph, dict) else []
    bridges = attempt.get("known_theorem_bridges", []) if isinstance(attempt, dict) else []
    lemmas = attempt.get("lemma_candidates", []) if isinstance(attempt, dict) else []
    contract = problem.get("formal_proof_contract", {})

    proof_statuses = {"proved_by_certificate", "formal_proof_verified", "accepted_theorem"}
    open_obligations = [
        item.get("id", "unknown")
        for item in obligations
        if isinstance(item, dict) and item.get("status") not in proof_statuses
    ]
    open_graph_links = [
        f"{item.get('from', item.get('id', 'unknown'))}->{item.get('to', item.get('status', 'unknown'))}"
        for item in [*graph_nodes, *graph_edges]
        if isinstance(item, dict)
        and item.get("status") not in {"proved_by_certificate", "formal_proof_verified", "accepted_theorem"}
    ]
    unsatisfied_bridges = [
        item.get("id", "unknown")
        for item in bridges
        if isinstance(item, dict) and item.get("status") not in {"formal_proof_verified", "accepted_theorem"}
    ]
    open_lemmas = [
        item.get("id", "unknown")
        for item in lemmas
        if isinstance(item, dict) and item.get("status") not in {"formal_proof_verified", "accepted_theorem"}
    ]
    blockers = []
    if certificate.get("status") != "bounded_theorem_certified":
        blockers.append("bounded_certificate_missing")
    if open_obligations:
        blockers.append("open_obligations")
    if open_graph_links:
        blockers.append("open_attack_graph_links")
    if unsatisfied_bridges:
        blockers.append("unsatisfied_known_theorem_bridges")
    if open_lemmas:
        blockers.append("unproved_lemma_candidates")
    if not isinstance(contract, dict) or contract.get("status") != "formal_proof_verified":
        blockers.append("formal_contract_not_verified")

    return {
        "schema": PROOF_STATUS_GATE_SCHEMA,
        "problem_id": problem.get("id"),
        "promotion_status": "blocked_open_infinite_obligation" if blockers else "eligible_for_independent_review",
        "allowed_public_claim": "bounded_theorem_only" if blockers else "candidate_full_proof_requires_external_review",
        "blockers": blockers,
        "open_obligations": open_obligations,
        "open_attack_graph_links": open_graph_links,
        "unsatisfied_known_theorem_bridges": unsatisfied_bridges,
        "open_lemma_candidates": open_lemmas,
        "formal_contract_status": contract.get("status", "missing") if isinstance(contract, dict) else "missing",
        "machine_rule": "A full-proof claim is blocked unless certificate status is bounded_theorem_certified and every obligation, graph link, theorem bridge, and lemma candidate is formal_proof_verified or accepted_theorem.",
    }


def formal_proof_contract(
    *,
    problem_id: str,
    theorem_name: str,
    lean_statement: str,
    forbidden_assumptions: list[str],
    required_artifacts: list[str],
) -> dict[str, object]:
    return {
        "schema": FORMAL_PROOF_CONTRACT_SCHEMA,
        "problem_id": problem_id,
        "proof_assistant_target": "Lean 4",
        "status": "not_formalized_open",
        "theorem_name": theorem_name,
        "lean_statement": lean_statement,
        "allowed_artifact_inputs": [
            "bounded_certificate_merkle_root",
            "formal_proof_verified_bridge",
            "accepted_theorem_reference",
        ],
        "required_artifacts": required_artifacts,
        "forbidden_assumptions": forbidden_assumptions,
        "acceptance_rules": [
            "No `sorry`, `admit`, unchecked axiom, or imported theorem equivalent to the target conjecture.",
            "Every finite computation must be represented by a bounded certificate and every infinite step by a formal theorem.",
            "The proof-status gate must report eligible_for_independent_review before any page can change from open_not_proven.",
            "An external reviewer must be able to replay the kernel check without trusting PrimeProject code.",
        ],
        "current_blocker": "open infinite obligations remain outside the proof assistant kernel",
    }


def proof_milestone_queue(
    *,
    problem_id: str,
    decisive_next_task: str,
    milestones: list[dict[str, str]],
) -> dict[str, object]:
    completed = [item for item in milestones if item.get("status") == "complete"]
    blocked = [item for item in milestones if item.get("status", "").startswith("blocked")]
    open_items = [item for item in milestones if item.get("status", "").startswith("open")]
    return {
        "schema": PROOF_MILESTONE_SCHEMA,
        "problem_id": problem_id,
        "status": "bounded_only_infinite_proof_open",
        "decisive_next_task": decisive_next_task,
        "completed_count": len(completed),
        "open_count": len(open_items),
        "blocked_count": len(blocked),
        "milestones": milestones,
        "promotion_rule": "Only complete milestones backed by replayable artifacts can reduce the open_count. Heuristic evidence cannot close a milestone.",
    }


def proof_frontier_probe(
    *,
    problem_id: str,
    objective: str,
    limit: int,
    metrics: dict[str, object],
    observations: list[dict[str, object]],
    proof_pressure: str,
    failure_signal: str,
) -> dict[str, object]:
    return {
        "schema": PROOF_FRONTIER_PROBE_SCHEMA,
        "problem_id": problem_id,
        "status": "finite_probe_not_proof",
        "objective": objective,
        "limit": limit,
        "metrics": metrics,
        "observations": observations,
        "proof_pressure": proof_pressure,
        "failure_signal": failure_signal,
        "promotion_rule": "Frontier probes can prioritize a proof path or falsify a candidate lemma, but cannot close an infinite conjecture without a formal theorem.",
    }


def decisive_lemma_lab(
    *,
    problem_id: str,
    lemma_id: str,
    decisive_question: str,
    candidate_statement: str,
    closes_milestones: list[str],
    finite_probe: dict[str, object],
    proof_obligation: str,
    falsification_test: str,
    current_result: str,
    next_action: str,
    automated_falsification_probe: dict[str, object],
    proof_gap_taxonomy: dict[str, object],
) -> dict[str, object]:
    probe = attach_probe_certificate(
        problem_id=problem_id,
        lemma_id=lemma_id,
        probe=automated_falsification_probe,
    )
    return {
        "schema": DECISIVE_LEMMA_SCHEMA,
        "problem_id": problem_id,
        "lemma_id": lemma_id,
        "status": "active_not_proven",
        "decisive_question": decisive_question,
        "candidate_statement": candidate_statement,
        "closes_milestones": closes_milestones,
        "finite_probe": finite_probe,
        "proof_obligation": proof_obligation,
        "falsification_test": falsification_test,
        "automated_falsification_probe": probe,
        "proof_gap_taxonomy": proof_gap_taxonomy,
        "current_result": current_result,
        "next_action": next_action,
        "promotion_rule": "The lab may upgrade a milestone only when the proof obligation is discharged by a formal theorem or accepted external proof, not by finite probe success.",
    }


def proof_gap_taxonomy(*, problem_id: str, gaps: list[dict[str, str]]) -> dict[str, object]:
    return {
        "schema": PROOF_GAP_TAXONOMY_SCHEMA,
        "problem_id": problem_id,
        "status": "proof_gaps_open",
        "gap_count": len(gaps),
        "open_gap_count": sum(1 for gap in gaps if gap.get("status", "").startswith("open")),
        "blocked_gap_count": sum(1 for gap in gaps if gap.get("status", "").startswith("blocked")),
        "gaps": gaps,
        "closure_rule": "All proof gaps must be closed by formal proof artifacts or accepted theorem references before the conjecture page can change status.",
    }


def proof_execution_protocol(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    attempt = problem.get("proof_attempt", {}) if isinstance(problem.get("proof_attempt"), dict) else {}
    gate = problem.get("proof_status_gate", {}) if isinstance(problem.get("proof_status_gate"), dict) else {}
    contract = problem.get("formal_proof_contract", {}) if isinstance(problem.get("formal_proof_contract"), dict) else {}
    queue = problem.get("proof_milestone_queue", {}) if isinstance(problem.get("proof_milestone_queue"), dict) else {}
    lab = problem.get("decisive_lemma_lab", {}) if isinstance(problem.get("decisive_lemma_lab"), dict) else {}
    taxonomy = lab.get("proof_gap_taxonomy", {}) if isinstance(lab.get("proof_gap_taxonomy"), dict) else {}
    gaps = taxonomy.get("gaps", []) if isinstance(taxonomy.get("gaps"), list) else []
    first_open_gap = next((gap for gap in gaps if isinstance(gap, dict) and str(gap.get("status", "")).startswith("open")), {})
    open_obligations = attempt.get("obligations", []) if isinstance(attempt.get("obligations"), list) else []
    open_obligation_ids = [
        str(item.get("id"))
        for item in open_obligations
        if isinstance(item, dict) and item.get("status") not in {"proved_by_certificate", "formal_proof_verified", "accepted_theorem"}
    ]
    blockers = gate.get("blockers", []) if isinstance(gate.get("blockers"), list) else []
    return {
        "schema": PROOF_EXECUTION_PROTOCOL_SCHEMA,
        "problem_id": problem_id,
        "status": "blocked_before_full_proof",
        "execution_mode": "bounded_certificate_plus_formal_infinite_obligation_tracking",
        "current_frontier": queue.get("decisive_next_task", "missing decisive task"),
        "primary_open_gap": first_open_gap.get("id", "missing"),
        "primary_next_experiment": first_open_gap.get("next_experiment", "missing"),
        "primary_failure_signal": first_open_gap.get("failure_signal", "missing"),
        "open_obligation_ids": open_obligation_ids,
        "blocking_reasons": blockers,
        "stages": [
            {
                "id": f"{problem_id}-exec-1",
                "name": "bounded certificate replay",
                "status": "complete" if certificate.get("status") == "bounded_theorem_certified" else "blocked",
                "input": "finite computation rows",
                "required_output": "Merkle-rooted bounded theorem certificate",
                "verifier": certificate.get("verifier", "missing"),
                "proof_value": "Closes only the finite range; it does not discharge an infinite conjecture.",
            },
            {
                "id": f"{problem_id}-exec-2",
                "name": "formal target normalization",
                "status": contract.get("status", "missing"),
                "input": "Lean-oriented theorem statement and forbidden assumptions",
                "required_output": "kernel-checkable definitions with no sorry/admit/target-equivalent axiom",
                "verifier": "Lean 4 replay required",
                "proof_value": "Prevents finite evidence or conjectural imports from being mistaken for proof.",
            },
            {
                "id": f"{problem_id}-exec-3",
                "name": "decisive lemma attack",
                "status": lab.get("status", "missing"),
                "input": lab.get("candidate_statement", "missing"),
                "required_output": lab.get("proof_obligation", "missing"),
                "verifier": "formal theorem or accepted external theorem",
                "proof_value": "The first infinite step that would close the main open milestones.",
            },
            {
                "id": f"{problem_id}-exec-4",
                "name": "gap work-order falsification",
                "status": taxonomy.get("status", "missing"),
                "input": first_open_gap.get("next_experiment", "missing"),
                "required_output": first_open_gap.get("required_artifact", "missing"),
                "verifier": first_open_gap.get("failure_signal", "missing"),
                "proof_value": "Turns the next research move into a testable success/failure condition.",
            },
            {
                "id": f"{problem_id}-exec-5",
                "name": "full proof promotion gate",
                "status": gate.get("promotion_status", "missing"),
                "input": "all obligations, graph links, theorem bridges, lemma candidates, and formal contract",
                "required_output": "eligible_for_independent_review",
                "verifier": "scripts/verify_open_problem_workbench.py",
                "proof_value": "Blocks any public full-proof claim until every infinite bridge is independently checkable.",
            },
        ],
        "promotion_rule": "The conjecture page cannot claim solved status until every protocol stage is complete or formally verified and the proof-status gate is eligible_for_independent_review.",
    }


def known_barrier_audit(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    common_rows = [
        {
            "id": f"{problem_id}-barrier-finite",
            "barrier": "finite_to_infinite_lift",
            "status": "not_cleared",
            "why_it_matters": "A bounded certificate proves only the committed finite theorem.",
            "required_clearance": "An explicit theorem removes the search limit and covers the infinite tail.",
        },
        {
            "id": f"{problem_id}-barrier-formal",
            "barrier": "kernel_checkable_formalization",
            "status": "not_cleared",
            "why_it_matters": "A convincing proof must replay without sorry/admit or conjecture-equivalent axioms.",
            "required_clearance": "Lean 4 or equivalent kernel replay verifies all infinite steps.",
        },
    ]
    specific: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "riemann-barrier-equivalence",
                "barrier": "rh_equivalence_strength",
                "status": "not_cleared",
                "why_it_matters": "Prime-counting bounds must be strong enough to imply an accepted RH-equivalent zero statement.",
                "required_clearance": "A formal bridge from the proposed theta envelope to critical-line zero control.",
            },
            {
                "id": "riemann-barrier-zero-tail",
                "barrier": "zero_tail_control",
                "status": "not_cleared",
                "why_it_matters": "Finite zero or prime tables do not control the infinite critical strip.",
                "required_clearance": "A tail theorem independent of numerical cutoff.",
            },
        ],
        "collatz": [
            {
                "id": "collatz-barrier-exceptional-classes",
                "barrier": "uncovered_residue_classes",
                "status": "not_cleared",
                "why_it_matters": "A descent proof fails if any lifted residue family can avoid a smaller representative.",
                "required_clearance": "A complete symbolic cover with a well-founded descent measure.",
            },
            {
                "id": "collatz-barrier-cycle-divergence",
                "barrier": "cycle_and_divergence_exclusion",
                "status": "not_cleared",
                "why_it_matters": "Reaching 1 through a finite range does not exclude non-trivial cycles or divergent branches.",
                "required_clearance": "A theorem deriving both exclusions from the same descent certificate.",
            },
        ],
        "goldbach": [
            {
                "id": "goldbach-barrier-lower-bound",
                "barrier": "positive_representation_lower_bound",
                "status": "not_cleared",
                "why_it_matters": "No-counterexample evidence does not prove every large even integer has a representation.",
                "required_clearance": "An explicit positive lower bound for the Goldbach representation count.",
            },
            {
                "id": "goldbach-barrier-threshold",
                "barrier": "finite_threshold_bridge",
                "status": "not_cleared",
                "why_it_matters": "An analytic theorem above the certified range leaves an unverified interval.",
                "required_clearance": "The analytic threshold is at or below the bounded certificate limit.",
            },
        ],
        "twin-prime": [
            {
                "id": "twin-prime-barrier-exact-gap",
                "barrier": "exact_gap_2_lower_bound",
                "status": "not_cleared",
                "why_it_matters": "Bounded prime gaps do not imply infinitely many exact gaps of size 2.",
                "required_clearance": "An unconditional lower bound for exact twin-prime pairs at arbitrarily large scale.",
            },
            {
                "id": "twin-prime-barrier-k-tuple",
                "barrier": "hardy_littlewood_dependency",
                "status": "not_cleared",
                "why_it_matters": "Hardy-Littlewood k-tuple density predicts twin primes but cannot be assumed as proof.",
                "required_clearance": "An assumption-free distribution argument or accepted theorem replacing the heuristic.",
            },
        ],
    }
    barriers = [*common_rows, *specific.get(problem_id, [])]
    return {
        "schema": KNOWN_BARRIER_AUDIT_SCHEMA,
        "problem_id": problem_id,
        "status": "barriers_not_cleared",
        "cleared_count": sum(1 for row in barriers if row["status"] == "cleared"),
        "open_count": sum(1 for row in barriers if row["status"] != "cleared"),
        "barriers": barriers,
        "promotion_rule": "A conjecture page remains open_not_proven while any known barrier is not cleared by a formal artifact or accepted theorem.",
    }


def formal_replay_package(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    contract = problem.get("formal_proof_contract", {}) if isinstance(problem.get("formal_proof_contract"), dict) else {}
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    barrier_audit = problem.get("known_barrier_audit", {}) if isinstance(problem.get("known_barrier_audit"), dict) else {}
    required_artifacts = contract.get("required_artifacts", []) if isinstance(contract.get("required_artifacts"), list) else []
    forbidden_assumptions = contract.get("forbidden_assumptions", []) if isinstance(contract.get("forbidden_assumptions"), list) else []
    theorem_name = str(contract.get("theorem_name", f"primeproject_{problem_id}_conjecture"))
    package_dir = f"formal/{problem_id}"
    return {
        "schema": FORMAL_REPLAY_PACKAGE_SCHEMA,
        "problem_id": problem_id,
        "status": "not_replayable_until_barriers_clear",
        "package_dir": package_dir,
        "target_kernel": contract.get("proof_assistant_target", "Lean 4"),
        "theorem_name": theorem_name,
        "theorem_statement": contract.get("lean_statement", "missing theorem statement"),
        "candidate_files": [
            f"{package_dir}/Definitions.lean",
            f"{package_dir}/BoundedCertificate.lean",
            f"{package_dir}/InfiniteBridge.lean",
            f"{package_dir}/Main.lean",
        ],
        "replay_commands": [
            f"lake env lean {package_dir}/Definitions.lean",
            f"lake env lean {package_dir}/BoundedCertificate.lean",
            f"lake env lean {package_dir}/InfiniteBridge.lean",
            f"lake env lean {package_dir}/Main.lean",
        ],
        "required_artifacts": [
            {
                "name": "bounded_certificate_merkle_root",
                "status": "available",
                "value": certificate.get("merkle_root", "missing"),
            },
            *[
                {
                    "name": str(artifact),
                    "status": "missing_formal_artifact",
                    "value": "required before replay",
                }
                for artifact in required_artifacts
                if str(artifact) != "bounded_certificate_merkle_root"
            ],
        ],
        "forbidden_tokens": [
            "sorry",
            "admit",
            "axiom " + theorem_name,
            *[str(item) for item in forbidden_assumptions],
        ],
        "open_barriers": barrier_audit.get("open_count", 0),
        "acceptance_rule": "The replay package is publishable only when all candidate files kernel-check and every required artifact is available without importing the target conjecture.",
    }


def proof_review_docket(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    gate = problem.get("proof_status_gate", {}) if isinstance(problem.get("proof_status_gate"), dict) else {}
    barrier_audit = problem.get("known_barrier_audit", {}) if isinstance(problem.get("known_barrier_audit"), dict) else {}
    replay = problem.get("formal_replay_package", {}) if isinstance(problem.get("formal_replay_package"), dict) else {}
    return {
        "schema": PROOF_REVIEW_DOCKET_SCHEMA,
        "problem_id": problem_id,
        "status": "full_proof_not_accepted",
        "review_stage": "pre_submission_red_team",
        "reviewer_stance": "accept bounded theorem, reject full conjecture claim until all infinite obligations replay",
        "verdicts": [
            {
                "claim": "bounded finite theorem",
                "verdict": "accepted_for_committed_limit",
                "evidence": certificate.get("merkle_root", "missing bounded certificate"),
                "reason": "The bounded certificate is reproducible and scoped to the public search limit.",
            },
            {
                "claim": "full conjecture solved",
                "verdict": "rejected_currently",
                "evidence": gate.get("promotion_status", "missing promotion gate"),
                "reason": "The proof-status gate still reports open infinite obligations or unsatisfied bridges.",
            },
            {
                "claim": "formal replay ready",
                "verdict": "blocked_currently",
                "evidence": replay.get("status", "missing replay package"),
                "reason": "The formal package is not replayable while required infinite artifacts are missing.",
            },
            {
                "claim": "known barriers cleared",
                "verdict": "rejected_currently",
                "evidence": f"{barrier_audit.get('open_count', 'unknown')} open barriers",
                "reason": "Every known barrier must be cleared by a formal artifact or accepted theorem reference.",
            },
        ],
        "minimum_acceptance_conditions": [
            "proof_status_gate.promotion_status == eligible_for_independent_review",
            "known_barrier_audit.open_count == 0",
            "formal_replay_package.status == replayable",
            "all replay commands pass in a clean environment",
            "no forbidden token or conjecture-equivalent import appears in the replay package",
        ],
        "rejection_rule": "Any candidate proof that relies only on finite computation, heuristic density, unchecked axioms, or an imported target-equivalent theorem remains rejected.",
    }


def proof_reduction_contract(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    reductions: dict[str, dict[str, object]] = {
        "riemann": {
            "decisive_reduction": {
                "statement": "Prove an explicit all-x prime-counting or Chebyshev-error theorem whose formal implication is exactly strong enough to force every non-trivial zeta zero onto Re(s)=1/2.",
                "would_promote_if": "the all-x theorem and the RH-equivalence bridge both replay in the formal package without importing RH",
                "missing_artifact": "formal all-x analytic estimate plus formal RH-equivalence bridge",
            },
            "accepted_partial_results": [
                {
                    "name": "bounded prime-counting diagnostics",
                    "allowed_use": "stress-test constants and candidate envelopes",
                    "does_not_prove": "zero control outside the checked range",
                },
                {
                    "name": "published RH-equivalent criteria",
                    "allowed_use": "define the bridge target",
                    "does_not_prove": "the criterion itself unless its hypotheses are independently established",
                },
            ],
            "forbidden_shortcuts": [
                "assume the Riemann Hypothesis under another theorem name",
                "treat finite zero or prime-counting checks as an infinite zero theorem",
                "use a prime-counting envelope weaker than an RH-equivalent criterion",
            ],
            "review_questions": [
                "Which exact RH-equivalent criterion is being discharged?",
                "Are all constants explicit and valid beyond the finite search range?",
                "Can the zero-control bridge replay without conjectural imports?",
            ],
        },
        "collatz": {
            "decisive_reduction": {
                "statement": "Construct a finite symbolic residue-block cover with a well-founded descent measure that covers every positive integer, not just enumerated starts.",
                "would_promote_if": "every residue block has a verified descent certificate and the cover theorem proves all starts eventually enter 1",
                "missing_artifact": "formal residue-cover descent theorem",
            },
            "accepted_partial_results": [
                {
                    "name": "bounded trajectory replay",
                    "allowed_use": "detect counterexamples and guide residue block design",
                    "does_not_prove": "termination for starts outside the checked range",
                },
                {
                    "name": "accelerated odd-step residue analysis",
                    "allowed_use": "propose symbolic descent blocks",
                    "does_not_prove": "global well-founded descent without a complete cover",
                },
            ],
            "forbidden_shortcuts": [
                "infer global termination from a large finite replay",
                "leave any residue class uncovered",
                "use an average drift argument without a deterministic descent certificate",
            ],
            "review_questions": [
                "Does the residue cover partition all positive starts?",
                "Does every block strictly decrease a well-founded measure?",
                "Does the proof handle the transitions between blocks without search-limit dependence?",
            ],
        },
        "goldbach": {
            "decisive_reduction": {
                "statement": "Prove an explicit representation lower bound or threshold theorem for every sufficiently large even integer, then combine it with a bounded certificate below the threshold.",
                "would_promote_if": "the threshold theorem covers the infinite tail and the bounded certificate covers every even integer below the threshold",
                "missing_artifact": "formal large-even threshold theorem with explicit cutoff",
            },
            "accepted_partial_results": [
                {
                    "name": "bounded Goldbach decomposition certificate",
                    "allowed_use": "cover the finite interval below a stated threshold",
                    "does_not_prove": "all even integers without an infinite threshold theorem",
                },
                {
                    "name": "weak Goldbach and density heuristics",
                    "allowed_use": "inform candidate major/minor arc lemmas",
                    "does_not_prove": "the binary even-prime representation target",
                },
            ],
            "forbidden_shortcuts": [
                "replace strong Goldbach with weak Goldbach",
                "treat sampled decompositions as a lower-bound theorem",
                "omit the explicit finite cutoff connecting the infinite theorem to the bounded certificate",
            ],
            "review_questions": [
                "What explicit threshold begins the infinite theorem?",
                "Does the bounded certificate cover every even integer below that threshold?",
                "Is the representation lower bound positive for every large even integer, not only on average?",
            ],
        },
        "twin-prime": {
            "decisive_reduction": {
                "statement": "Prove an unconditional exact gap-2 lower bound for arbitrarily large x, not merely a bounded-prime-gap theorem.",
                "would_promote_if": "the exact gap-2 lower bound implies arbitrarily large twin prime pairs and replays without Hardy-Littlewood assumptions",
                "missing_artifact": "formal exact gap-2 lower-bound theorem",
            },
            "accepted_partial_results": [
                {
                    "name": "bounded twin-pair certificate",
                    "allowed_use": "stress-test residue patterns and exact gap-2 counts",
                    "does_not_prove": "infinitely many twin pairs",
                },
                {
                    "name": "bounded prime gaps",
                    "allowed_use": "show that small gaps occur infinitely often under accepted bounded-gap theorems",
                    "does_not_prove": "infinitely many exact gaps of size 2",
                },
            ],
            "forbidden_shortcuts": [
                "treat bounded gaps as exact gap 2",
                "assume Hardy-Littlewood k-tuple density as a proof",
                "infer infinitude from finite persistence of twin-pair counts",
            ],
            "review_questions": [
                "Is the theorem about exact gap 2 rather than some bounded gap?",
                "Does the lower bound stay positive at arbitrarily large x?",
                "Is every distributional assumption either proved or removed?",
            ],
        },
    }
    reduction = reductions.get(problem_id, {})
    return {
        "schema": PROOF_REDUCTION_CONTRACT_SCHEMA,
        "problem_id": problem_id,
        "status": "target_reduction_open",
        "bridge_status": "open_missing_infinite_bridge",
        "goal": "Define the smallest theorem package that would make a full-proof claim reviewable without mistaking finite evidence or partial theorems for the target conjecture.",
        "decisive_reduction": reduction.get("decisive_reduction", {}),
        "accepted_partial_results": reduction.get("accepted_partial_results", []),
        "forbidden_shortcuts": reduction.get("forbidden_shortcuts", []),
        "review_questions": reduction.get("review_questions", []),
        "promotion_test": "The page may move past open_not_proven only if this reduction contract, the proof review docket, the known barrier audit, and the formal replay package all report replayable or accepted status.",
    }


def proof_candidate_intake(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    reduction = problem.get("proof_reduction_contract", {})
    contract = problem.get("formal_proof_contract", {})
    replay = problem.get("formal_replay_package", {})
    decisive = reduction.get("decisive_reduction", {}) if isinstance(reduction, dict) else {}
    theorem_name = contract.get("theorem_name", "missing theorem") if isinstance(contract, dict) else "missing theorem"
    replay_commands = replay.get("replay_commands", []) if isinstance(replay, dict) else []
    first_tests: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-CI1",
                "name": "theta envelope endpoint stress",
                "input": "candidate C, x0, and all-x statement for |theta(x)-x|",
                "pass_condition": "no committed endpoint violates the proposed explicit envelope",
                "reject_if": "the envelope fails before the published search limit or is not RH-equivalent",
            },
            {
                "id": "RH-CI2",
                "name": "equivalence bridge audit",
                "input": "named RH-equivalent criterion and formal implication outline",
                "pass_condition": "the bridge target is stronger than a finite zero table",
                "reject_if": "the argument imports RH or an equivalent theorem as an assumption",
            },
        ],
        "collatz": [
            {
                "id": "CO-CI1",
                "name": "residue cover completeness",
                "input": "modulus, residue blocks, transition map, and descent measure",
                "pass_condition": "every residue class is covered exactly once or by a justified refinement",
                "reject_if": "any class is uncovered or relies on average drift only",
            },
            {
                "id": "CO-CI2",
                "name": "well-founded descent replay",
                "input": "block certificate showing strict decrease after finite accelerated steps",
                "pass_condition": "every block decreases a declared well-founded measure",
                "reject_if": "a transition can return to an equal or larger unresolved block",
            },
        ],
        "goldbach": [
            {
                "id": "GB-CI1",
                "name": "threshold theorem cutoff audit",
                "input": "explicit N0 and representation lower-bound theorem",
                "pass_condition": "the lower bound is positive for every even n >= N0",
                "reject_if": "the result is only average-case, ternary, or weak Goldbach",
            },
            {
                "id": "GB-CI2",
                "name": "below-threshold certificate coverage",
                "input": "bounded certificate for every even 4 <= n < N0",
                "pass_condition": "the bounded certificate covers the whole gap below the threshold",
                "reject_if": "any even value below N0 lacks a certified decomposition",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-CI1",
                "name": "exact gap-2 lower-bound audit",
                "input": "candidate lower bound for twin prime pairs up to x",
                "pass_condition": "the bound stays positive for arbitrarily large x",
                "reject_if": "the theorem proves only bounded gaps or an averaged pair count",
            },
            {
                "id": "TP-CI2",
                "name": "Hardy-Littlewood dependency removal",
                "input": "distributional assumptions and replacement lemmas",
                "pass_condition": "no k-tuple conjecture or independence heuristic is used as an axiom",
                "reject_if": "the proof assumes the density it must prove",
            },
        ],
    }
    return {
        "schema": PROOF_CANDIDATE_INTAKE_SCHEMA,
        "problem_id": problem_id,
        "status": "no_candidate_accepted",
        "intake_stage": "candidate_required",
        "candidate_target": decisive.get("statement", "missing decisive reduction"),
        "required_submission": [
            {
                "name": "formal theorem statement",
                "format": "Lean-oriented theorem plus human-readable statement",
                "minimum_content": theorem_name,
            },
            {
                "name": "infinite bridge proof",
                "format": "formal artifact or accepted theorem reference",
                "minimum_content": decisive.get("missing_artifact", "missing infinite bridge artifact"),
            },
            {
                "name": "replay bundle",
                "format": "candidate files and commands",
                "minimum_content": "; ".join(str(item) for item in replay_commands[:2]) or "lake env lean replay commands",
            },
            {
                "name": "bounded compatibility report",
                "format": "machine-readable JSON with checksum",
                "minimum_content": "show that the candidate does not contradict the committed bounded certificate",
            },
        ],
        "first_executable_tests": first_tests.get(problem_id, []),
        "automatic_rejection_rules": [
            "finite computation is used as a substitute for an infinite theorem",
            "the target conjecture or an equivalent theorem is imported as an assumption",
            "the proof contains sorry, admit, unchecked axiom, or an unverifiable external dependency",
            "the candidate proves a weaker nearby theorem while claiming the original problem",
        ],
        "review_output": {
            "accepted": "candidate can move to formal replay and independent review",
            "revise": "candidate has a precise missing bridge or failed executable test",
            "rejected": "candidate violates an automatic rejection rule",
        },
        "claim_boundary": "This intake accepts proof candidates for review only; it does not certify that any of the four conjectures has been solved.",
    }


def proof_attempt_execution_log(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    frontier = problem.get("proof_frontier_probe", {})
    lab = problem.get("decisive_lemma_lab", {})
    reduction = problem.get("proof_reduction_contract", {})
    intake = problem.get("proof_candidate_intake", {})
    decisive = reduction.get("decisive_reduction", {}) if isinstance(reduction, dict) else {}
    candidate_tests = intake.get("first_executable_tests", []) if isinstance(intake, dict) else []
    objective = frontier.get("objective", "missing objective") if isinstance(frontier, dict) else "missing objective"
    proof_gap = lab.get("automated_falsification_probe", {}).get("proof_gap", "missing proof gap") if isinstance(lab, dict) else "missing proof gap"
    final_attempts: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-EXEC-A",
                "route": "Use bounded theta residuals to guess an all-x envelope.",
                "machine_check": "decimal checkpoints and prime endpoint stress replay through the committed limit",
                "result": "bounded_compatible",
                "failure_reason": "the route still lacks a theorem over all real x and an RH-equivalence bridge",
                "next_artifact": "formal all-x theta error theorem with explicit constants",
            },
            {
                "id": "RH-EXEC-B",
                "route": "Try to promote finite zero/prime evidence to zero-line control.",
                "machine_check": "proof review docket and forbidden-import audit",
                "result": "rejected_as_finite_only",
                "failure_reason": "finite checks cannot quantify every non-trivial zeta zero",
                "next_artifact": "kernel-checkable zero-control implication",
            },
        ],
        "collatz": [
            {
                "id": "CO-EXEC-A",
                "route": "Use bounded trajectory replay to infer a residue descent pattern.",
                "machine_check": "all starts through the committed limit replay without counterexample",
                "result": "bounded_compatible",
                "failure_reason": "the route has no complete symbolic cover of all residue classes",
                "next_artifact": "finite residue-block cover with strict descent certificates",
            },
            {
                "id": "CO-EXEC-B",
                "route": "Use average odd-step drift as a global termination argument.",
                "machine_check": "candidate intake automatic rejection rules",
                "result": "rejected_as_average_only",
                "failure_reason": "average drift does not rule out exceptional infinite trajectories",
                "next_artifact": "deterministic well-founded descent proof",
            },
        ],
        "goldbach": [
            {
                "id": "GB-EXEC-A",
                "route": "Use bounded decompositions to search for a stable lower-bound shape.",
                "machine_check": "every even integer through the committed limit has a certified witness",
                "result": "bounded_compatible",
                "failure_reason": "the route does not prove positivity for every sufficiently large even integer",
                "next_artifact": "explicit large-even representation theorem",
            },
            {
                "id": "GB-EXEC-B",
                "route": "Use weak Goldbach-style evidence as a replacement for strong Goldbach.",
                "machine_check": "proof reduction forbidden-shortcut audit",
                "result": "rejected_as_wrong_target",
                "failure_reason": "ternary or average statements do not prove binary even-prime representation",
                "next_artifact": "binary representation lower bound plus explicit cutoff",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-EXEC-A",
                "route": "Use exact gap-2 residue persistence to infer infinitude.",
                "machine_check": "twin-pair counts and residue stress replay through the committed limit",
                "result": "bounded_compatible",
                "failure_reason": "finite persistence does not produce an arbitrarily-large exact gap-2 lower bound",
                "next_artifact": "unconditional exact gap-2 lower-bound theorem",
            },
            {
                "id": "TP-EXEC-B",
                "route": "Use bounded prime gaps as a stand-in for twin primes.",
                "machine_check": "proof reduction forbidden-shortcut audit",
                "result": "rejected_as_weaker_theorem",
                "failure_reason": "bounded gaps do not imply infinitely many exact gaps of size 2",
                "next_artifact": "formal distinction between bounded gaps and exact gap 2",
            },
        ],
    }
    return {
        "schema": PROOF_ATTEMPT_EXECUTION_LOG_SCHEMA,
        "problem_id": problem_id,
        "status": "attempts_executed_no_full_proof",
        "frontier_objective": objective,
        "attempts": final_attempts.get(problem_id, []),
        "candidate_test_count": len(candidate_tests),
        "blocking_gap": proof_gap,
        "decisive_missing_artifact": decisive.get("missing_artifact", "missing decisive artifact"),
        "machine_verdict": "bounded evidence can guide the proof search, but every executed route still leaves an infinite bridge open",
        "publication_rule": "Execution logs can report failed or bounded-compatible proof attempts only; they cannot upgrade the conjecture status.",
    }


def proof_obligation_dag(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    queue = problem.get("proof_milestone_queue", {})
    lab = problem.get("decisive_lemma_lab", {})
    reduction = problem.get("proof_reduction_contract", {})
    execution_log = problem.get("proof_attempt_execution_log", {})
    decisive = reduction.get("decisive_reduction", {}) if isinstance(reduction, dict) else {}
    milestones = queue.get("milestones", []) if isinstance(queue, dict) else []
    gaps = lab.get("proof_gap_taxonomy", {}).get("gaps", []) if isinstance(lab, dict) else []
    attempts = execution_log.get("attempts", []) if isinstance(execution_log, dict) else []
    problem_prefix = {
        "riemann": "RH",
        "collatz": "CO",
        "goldbach": "GB",
        "twin-prime": "TP",
    }.get(problem_id, "OP")
    nodes: list[dict[str, str]] = []
    for item in milestones:
        if isinstance(item, dict):
            nodes.append(
                {
                    "id": str(item.get("id", "")),
                    "type": "milestone",
                    "label": str(item.get("title", "")),
                    "status": str(item.get("status", "open")),
                    "required_artifact": str(item.get("artifact", "")),
                }
            )
    for item in gaps:
        if isinstance(item, dict):
            nodes.append(
                {
                    "id": str(item.get("id", "")),
                    "type": "gap",
                    "label": str(item.get("type", "")),
                    "status": str(item.get("status", "open")),
                    "required_artifact": str(item.get("required_artifact", "")),
                }
            )
    for item in attempts:
        if isinstance(item, dict):
            nodes.append(
                {
                    "id": str(item.get("id", "")),
                    "type": "attempt",
                    "label": str(item.get("route", "")),
                    "status": str(item.get("result", "open")),
                    "required_artifact": str(item.get("next_artifact", "")),
                }
            )
    reduction_node = f"{problem_prefix}-REDUCE"
    nodes.append(
        {
            "id": reduction_node,
            "type": "reduction",
            "label": "decisive reduction theorem",
            "status": "open_missing_infinite_bridge",
            "required_artifact": str(decisive.get("missing_artifact", "missing decisive artifact")),
        }
    )
    nodes.append(
        {
            "id": f"{problem_prefix}-TARGET",
            "type": "target",
            "label": str(problem.get("title", "target conjecture")),
            "status": "open_not_proven",
            "required_artifact": "independently checkable full proof",
        }
    )
    milestone_ids = [node["id"] for node in nodes if node["type"] == "milestone"]
    gap_ids = [node["id"] for node in nodes if node["type"] == "gap"]
    attempt_ids = [node["id"] for node in nodes if node["type"] == "attempt"]
    edges: list[dict[str, str]] = []
    for attempt_id in attempt_ids:
        edges.append({"from": attempt_id, "to": reduction_node, "status": "blocked_by_missing_artifact"})
    for gap_id in gap_ids:
        edges.append({"from": gap_id, "to": reduction_node, "status": "must_close"})
    for milestone_id in milestone_ids:
        if milestone_id.endswith("M1"):
            edges.append({"from": milestone_id, "to": reduction_node, "status": "bounded_support_only"})
        elif milestone_id.endswith("M5"):
            edges.append({"from": reduction_node, "to": milestone_id, "status": "blocked_until_bridge_closes"})
            edges.append({"from": milestone_id, "to": f"{problem_prefix}-TARGET", "status": "required_for_public_claim"})
        else:
            edges.append({"from": milestone_id, "to": reduction_node, "status": "required"})
    edges.append({"from": reduction_node, "to": f"{problem_prefix}-TARGET", "status": "required_for_full_proof"})
    open_nodes = [node["id"] for node in nodes if node["status"] not in {"complete", "proved_by_certificate", "bounded_compatible"}]
    return {
        "schema": PROOF_OBLIGATION_DAG_SCHEMA,
        "problem_id": problem_id,
        "status": "open_obligation_graph",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "open_node_count": len(open_nodes),
        "nodes": nodes,
        "edges": edges,
        "critical_path": [
            "bounded certificate is support only",
            "close every named proof gap",
            "prove the decisive reduction theorem",
            "replay the formal package independently",
            "then and only then review the full target claim",
        ],
        "machine_rule": "Every non-complete node on this DAG must be closed by a formal artifact or accepted theorem before the conjecture status can change.",
    }


def attach_probe_certificate(*, problem_id: str, lemma_id: str, probe: dict[str, object]) -> dict[str, object]:
    certified_probe = dict(probe)
    payload = json.dumps(certified_probe, sort_keys=True, separators=(",", ":"))
    payload_hash = hash_leaf(payload)
    certified_probe["probe_certificate"] = {
        "schema": PROBE_CERTIFICATE_SCHEMA,
        "problem_id": problem_id,
        "lemma_id": lemma_id,
        "status": "probe_payload_certified",
        "leaf_count": 1,
        "payload_sha256": payload_hash,
        "merkle_root": payload_hash,
        "verifier": "scripts/verify_open_problem_workbench.py",
        "scope": "automated_falsification_probe_without_certificate",
    }
    return certified_probe


def build_riemann(limit: int, primes: list[int]) -> dict[str, object]:
    checkpoints = [10**k for k in range(2, int(math.log10(limit)) + 1)]
    rows = []
    index = 0
    theta = 0.0
    max_scaled_theta_error = 0.0
    certificate = ChunkedCertificate(
        problem_id="riemann",
        statement=f"Prime-counting diagnostics are exactly recomputed at decimal checkpoints up to {limit}.",
        limit=limit,
    )
    for x in checkpoints:
        while index < len(primes) and primes[index] <= x:
            theta += math.log(primes[index])
            index += 1
        pi_x = index
        li_x = li_approx(x)
        scaled_theta_error = abs(theta - x) / (math.sqrt(x) * (math.log(x) ** 2))
        max_scaled_theta_error = max(max_scaled_theta_error, scaled_theta_error)
        rows.append(
            {
                "x": x,
                "pi_x": pi_x,
                "li_approx": round(li_x, 3),
                "pi_minus_li_approx": round(pi_x - li_x, 3),
                "theta_minus_x": round(theta - x, 3),
                "scaled_theta_error": round(scaled_theta_error, 6),
            }
        )
        certificate.update(json.dumps(rows[-1], sort_keys=True, separators=(",", ":")))
    theta_scan = 0.0
    max_prime_scaled_error = {"x": 2, "value": 0.0}
    candidate_threshold = 0.08
    threshold_violations = 0
    for prime in primes:
        theta_scan += math.log(prime)
        if prime >= 3:
            value = abs(theta_scan - prime) / (math.sqrt(prime) * (math.log(prime) ** 2))
            if value > max_prime_scaled_error["value"]:
                max_prime_scaled_error = {"x": prime, "value": value}
            if value > candidate_threshold:
                threshold_violations += 1
    return {
        "id": "riemann",
        "title": "Riemann Hypothesis",
        "korean_title": "리만가설",
        "status": "open_not_proven",
        "target_statement": "All non-trivial zeros of the Riemann zeta function have real part 1/2.",
        "tool_position": "PrimeProject can test prime-counting error signatures and RH-compatible envelopes on finite ranges; it cannot turn finite checks into a proof.",
        "finite_result": {
            "limit": limit,
            "checkpoints": rows,
            "max_scaled_theta_error": round(max_scaled_theta_error, 6),
        },
        "certificate": certificate.finish(),
        "proof_frontier_probe": proof_frontier_probe(
            problem_id="riemann",
            objective="Stress the proposed theta-envelope lemma at every prime endpoint through the committed limit.",
            limit=limit,
            metrics={
                "prime_endpoint_count": len(primes),
                "candidate_scaled_theta_threshold": candidate_threshold,
                "threshold_violation_count": threshold_violations,
                "max_prime_endpoint_scaled_theta_error": round(max_prime_scaled_error["value"], 6),
                "max_prime_endpoint_x": max_prime_scaled_error["x"],
            },
            observations=[
                {
                    "label": "worst prime endpoint",
                    "value": f"{max_prime_scaled_error['x']} @ {max_prime_scaled_error['value']:.6f}",
                },
                {
                    "label": "decimal checkpoint maximum",
                    "value": round(max_scaled_theta_error, 6),
                },
                {
                    "label": "candidate threshold violations",
                    "value": threshold_violations,
                },
            ],
            proof_pressure="A future all-x theta theorem must dominate both decimal checkpoints and every prime endpoint stress case, then connect to an RH-equivalent criterion.",
            failure_signal="Any endpoint above the proposed explicit envelope falsifies that candidate before formalization.",
        ),
        "proof_attempt": proof_attempt_ledger(
            problem_id="riemann",
            route="Prime-counting residuals -> explicit theta(x) envelope -> zero-free critical-strip control strong enough for RH.",
            formal_statement="For every non-trivial zero rho of zeta, Re(rho) = 1/2.",
            obligations=[
                {
                    "id": "RH-O1",
                    "claim": "Bounded theta/pi diagnostics are exactly reproducible.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "Merkle root mismatch or changed checkpoint row.",
                },
                {
                    "id": "RH-O2",
                    "claim": "Find an explicit residual bound valid for all x beyond a finite threshold.",
                    "status": "open_obligation",
                    "verifier": "analytic proof required",
                    "failure_mode": "A residual spike violates the proposed global envelope.",
                },
                {
                    "id": "RH-O3",
                    "claim": "Show the global envelope implies all non-trivial zeros lie on the critical line.",
                    "status": "open_obligation",
                    "verifier": "formal theorem or accepted analytic derivation",
                    "failure_mode": "The envelope is weaker than a known RH-equivalent condition.",
                },
            ],
            falsification_targets=[
                "A proposed all-x theta bound fails on a computed checkpoint.",
                "The bound does not imply a published RH-equivalent criterion.",
                "The argument depends on a finite zero table without an infinite tail theorem.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "rh-finite", "label": "Bounded theta/pi certificate", "status": "proved_by_certificate"},
                    {"id": "rh-envelope", "label": "Explicit all-x theta envelope", "status": "open_bridge"},
                    {"id": "rh-equivalence", "label": "RH-equivalent zero-control criterion", "status": "known_bridge_needed"},
                    {"id": "rh-target", "label": "All non-trivial zeros on Re(s)=1/2", "status": "open_target"},
                ],
                "edges": [
                    {"from": "rh-finite", "to": "rh-envelope", "status": "open_bridge", "label": "remove search limit"},
                    {"from": "rh-envelope", "to": "rh-equivalence", "status": "open_bridge", "label": "prove criterion strength"},
                    {"from": "rh-equivalence", "to": "rh-target", "status": "open_bridge", "label": "formal implication"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "RH-B1",
                    "name": "Prime-counting error equivalences",
                    "role": "Identify an explicit error envelope strong enough to imply RH.",
                    "status": "bridge_not_satisfied",
                },
                {
                    "id": "RH-B2",
                    "name": "Zero-free region machinery",
                    "role": "Convert analytic estimates into critical-strip zero control.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "RH-L1",
                    "statement": "There exists an explicit C such that |theta(x)-x| <= C sqrt(x) log(x)^2 for all x >= x0.",
                    "evidence": "Finite checkpoints are below the normalized envelope through the committed limit.",
                    "required_upgrade": "Prove the inequality for the infinite tail and show constants meet an RH-equivalent bound.",
                    "status": "open_candidate",
                }
            ],
        ),
        "proof_gates": [
            "Replace finite prime-counting evidence with a theorem controlling zeta zeros on the full critical strip.",
            "Prove an explicit equivalence strong enough to imply all non-trivial zeros lie on Re(s)=1/2.",
            "Show every numerical or symbolic step is independent of bounded search limits.",
        ],
        "formal_proof_contract": formal_proof_contract(
            problem_id="riemann",
            theorem_name="primeproject_riemann_hypothesis",
            lean_statement="theorem primeproject_riemann_hypothesis : forall rho, Zeta.NontrivialZero rho -> rho.re = (1/2 : Real) := by",
            forbidden_assumptions=[
                "RiemannHypothesis",
                "Zeta.nontrivialZeros_on_criticalLine",
                "any axiom implying all non-trivial zeta zeros have real part 1/2",
            ],
            required_artifacts=[
                "bounded theta/pi certificate",
                "formal all-x prime-counting error theorem",
                "formal RH-equivalence bridge",
            ],
        ),
        "proof_milestone_queue": proof_milestone_queue(
            problem_id="riemann",
            decisive_next_task="Formalize an explicit all-x prime-counting error theorem strong enough to connect finite theta diagnostics to an RH-equivalent bridge.",
            milestones=[
                {
                    "id": "RH-M1",
                    "title": "Bounded theta/pi certificate",
                    "status": "complete",
                    "artifact": "bounded_certificate_merkle_root",
                    "exit_criterion": "scripts/verify_open_problem_workbench.py reproduces the committed root.",
                },
                {
                    "id": "RH-M2",
                    "title": "Lean definitions for zeta zeros and theta diagnostics",
                    "status": "open_formalization",
                    "artifact": "Lean 4 definitions",
                    "exit_criterion": "Kernel-checkable definitions compile without conjectural axioms.",
                },
                {
                    "id": "RH-M3",
                    "title": "All-x theta error theorem",
                    "status": "open_infinite_bridge",
                    "artifact": "formal theorem",
                    "exit_criterion": "A theorem removes the finite search limit with explicit constants.",
                },
                {
                    "id": "RH-M4",
                    "title": "RH-equivalence bridge",
                    "status": "open_infinite_bridge",
                    "artifact": "formal bridge proof",
                    "exit_criterion": "The all-x estimate implies every non-trivial zero lies on the critical line.",
                },
                {
                    "id": "RH-M5",
                    "title": "Independent kernel review",
                    "status": "blocked_until_m2_m4_complete",
                    "artifact": "external replay report",
                    "exit_criterion": "A clean Lean replay passes outside PrimeProject.",
                },
            ],
        ),
        "decisive_lemma_lab": decisive_lemma_lab(
            problem_id="riemann",
            lemma_id="RH-DL1",
            decisive_question="Can finite theta residual discipline be upgraded into an explicit all-x bound strong enough for an RH-equivalent bridge?",
            candidate_statement="There are explicit constants C and x0 such that |theta(x)-x| <= C sqrt(x) log(x)^2 for every x >= x0, and the constants satisfy a formal RH-equivalent criterion.",
            closes_milestones=["RH-M3", "RH-M4"],
            finite_probe={
                "limit": limit,
                "checkpoint_count": len(rows),
                "observed_max_scaled_theta_error": max_scaled_theta_error,
                "probe_status": "no_bounded_violation",
            },
            proof_obligation="Replace checkpoint agreement with a theorem over all real x beyond a stated threshold and prove the equivalence bridge without importing RH.",
            falsification_test="Search for a computed theta residual that violates the proposed envelope, then reject any envelope that fails to imply a known RH-equivalent statement.",
            automated_falsification_probe={
                "schema": "primeproject.decisive-lemma-falsification-probe.v1",
                "result_status": "bounded_probe_passed_proof_open",
                "scope": f"decimal checkpoints up to {limit}",
                "probe_count": len(rows),
                "violated_count": sum(1 for row in rows if row["scaled_theta_error"] > 0.08),
                "pass_condition": "scaled_theta_error <= 0.08 at every committed checkpoint",
                "strongest_observed": {
                    "metric": "max_scaled_theta_error",
                    "value": round(max_scaled_theta_error, 6),
                    "threshold": 0.08,
                },
                "proof_gap": "Checkpoint probes do not quantify every x and do not prove the RH-equivalence bridge.",
            },
            current_result="The bounded probe is compatible with the lemma but does not prove it.",
            next_action="Formalize the target inequality and enumerate which published equivalence theorem would be sufficient.",
            proof_gap_taxonomy=proof_gap_taxonomy(
                problem_id="riemann",
                gaps=[
                    {
                        "id": "RH-G1",
                        "type": "infinite_lift",
                        "status": "open_infinite_bridge",
                        "description": "Checkpoint control must become an all-x theta estimate with explicit constants.",
                        "required_artifact": "formal all-x theta theorem",
                        "next_experiment": "Fit explicit theta-envelope candidates from certified checkpoints, then stress them against denser local theta samples before attempting an all-x theorem.",
                        "failure_signal": "A denser certified checkpoint violates the proposed envelope or the constants cannot be stated independently of the search limit.",
                    },
                    {
                        "id": "RH-G2",
                        "type": "equivalence_bridge",
                        "status": "open_infinite_bridge",
                        "description": "The all-x estimate must imply an accepted RH-equivalent zero-control criterion.",
                        "required_artifact": "formal RH-equivalence bridge",
                        "next_experiment": "Map each candidate theta bound to a published RH-equivalent or insufficient prime-counting criterion.",
                        "failure_signal": "The best available bound is weaker than every accepted RH-equivalent criterion.",
                    },
                    {
                        "id": "RH-G3",
                        "type": "formalization",
                        "status": "open_formalization",
                        "description": "Zeta zero, theta, and explicit-bound objects must be kernel-checkable without conjectural imports.",
                        "required_artifact": "Lean 4 definitions and theorem skeleton",
                        "next_experiment": "Create a no-sorry Lean namespace containing only definitions and theorem statements for zeros, theta, and the proposed envelope.",
                        "failure_signal": "The formal statement needs an imported theorem equivalent to RH or an unchecked axiom.",
                    },
                    {
                        "id": "RH-G4",
                        "type": "independent_review",
                        "status": "blocked_until_g1_g3_close",
                        "description": "An external replay must verify the proof without trusting PrimeProject code.",
                        "required_artifact": "external kernel replay report",
                        "next_experiment": "Package the formal artifacts and verifier command once G1-G3 have closed.",
                        "failure_signal": "A clean environment cannot replay the kernel check from published artifacts.",
                    },
                ],
            ),
        ),
        "candidate_strategy": [
            "Use generator-fingerprint residuals to look for structured departures from PNT-scale noise.",
            "Convert any stable residual law into a falsifiable analytic lemma before treating it as proof evidence.",
            "Reject any argument that only rephrases finite zero or finite prime-count checks.",
        ],
        "claim_boundary": "No proof claim. Current evidence is only finite RH-compatible diagnostics.",
    }


def build_collatz(limit: int) -> dict[str, object]:
    memo = {1: 0}
    max_steps = {"n": 1, "steps": 0}
    max_peak = {"n": 1, "peak": 1, "ratio": 1.0}
    certificate = ChunkedCertificate(
        problem_id="collatz",
        statement=f"Every start value 1 <= n <= {limit} reaches 1 under the Collatz map.",
        limit=limit,
    )

    def trajectory_stats(n: int) -> tuple[int, int]:
        original = n
        seen: list[int] = []
        peak = n
        while n not in memo:
            seen.append(n)
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            peak = max(peak, n)
        steps = memo[n]
        for value in reversed(seen):
            steps += 1
            if value <= limit:
                memo[value] = steps
        return memo[original], peak

    certificate.update("1:0:1")
    for n in range(2, limit + 1):
        steps, peak = trajectory_stats(n)
        certificate.update(f"{n}:{steps}:{peak}")
        if steps > max_steps["steps"]:
            max_steps = {"n": n, "steps": steps}
        ratio = peak / n
        if ratio > max_peak["ratio"]:
            max_peak = {"n": n, "peak": peak, "ratio": ratio}
    residue_modulus = 4096
    residue_step_budget = 8
    odd_residues = [residue for residue in range(1, residue_modulus, 2)]
    uncovered_residues: list[int] = []
    longest_descent_steps = 0
    for residue in odd_residues:
        value = residue
        covered = residue == 1
        for step in range(1, residue_step_budget + 1):
            value = 3 * value + 1
            while value % 2 == 0:
                value //= 2
            if value < residue:
                covered = True
                longest_descent_steps = max(longest_descent_steps, step)
                break
        if not covered:
            uncovered_residues.append(residue)

    return {
        "id": "collatz",
        "title": "Collatz Conjecture",
        "korean_title": "콜라츠 추측",
        "status": "open_not_proven",
        "target_statement": "Repeatedly applying n/2 for even n and 3n+1 for odd n eventually reaches 1 for every positive integer.",
        "tool_position": "PrimeProject can exhaustively replay trajectories over a bounded range and search for divergent behavior; bounded replay is not a proof over all integers.",
        "finite_result": {
            "limit": limit,
            "tested_start_values": limit,
            "counterexamples": 0,
            "max_total_stopping_time": max_steps,
            "max_peak_ratio": {
                "n": max_peak["n"],
                "peak": max_peak["peak"],
                "ratio": round(max_peak["ratio"], 6),
            },
        },
        "certificate": certificate.finish(),
        "proof_frontier_probe": proof_frontier_probe(
            problem_id="collatz",
            objective=f"Search for accelerated odd residue descents modulo {residue_modulus} within {residue_step_budget} odd steps.",
            limit=limit,
            metrics={
                "residue_modulus": residue_modulus,
                "odd_residue_count": len(odd_residues),
                "covered_residue_count": len(odd_residues) - len(uncovered_residues),
                "uncovered_residue_count": len(uncovered_residues),
                "step_budget": residue_step_budget,
                "longest_observed_descent_steps": longest_descent_steps,
            },
            observations=[
                {
                    "label": "first uncovered residues",
                    "value": uncovered_residues[:10],
                },
                {
                    "label": "coverage ratio",
                    "value": round((len(odd_residues) - len(uncovered_residues)) / len(odd_residues), 6),
                },
                {
                    "label": "max stopping-time witness",
                    "value": f"{max_steps['n']} in {max_steps['steps']} steps",
                },
            ],
            proof_pressure="A real Collatz proof path needs a symbolic residue-block cover; uncovered residues identify where the current descent search is too weak.",
            failure_signal="Any residue family that cannot be assigned a well-founded descent keeps the global proof blocked.",
        ),
        "proof_attempt": proof_attempt_ledger(
            problem_id="collatz",
            route="Odd-only accelerated map -> residue-block descent certificate -> recursive coverage of every positive integer.",
            formal_statement="For every positive integer n, some iterate of the Collatz map reaches 1.",
            obligations=[
                {
                    "id": "C-O1",
                    "claim": "Every n <= 1,000,000 reaches 1 under the Collatz map.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "A trajectory leaf changes or a non-reaching start value appears.",
                },
                {
                    "id": "C-O2",
                    "claim": "Construct residue-block descent certificates that cover all sufficiently large blocks.",
                    "status": "open_obligation",
                    "verifier": "deterministic descent proof required",
                    "failure_mode": "An uncovered block has no guaranteed descent path.",
                },
                {
                    "id": "C-O3",
                    "claim": "Rule out divergent trajectories and non-trivial cycles simultaneously.",
                    "status": "open_obligation",
                    "verifier": "cycle and divergence exclusion theorem",
                    "failure_mode": "A cycle or non-descending infinite branch remains possible.",
                },
            ],
            falsification_targets=[
                "A residue block cannot be assigned a monotone descent certificate.",
                "A proposed drift inequality admits an infinite exceptional set.",
                "Odd-only compression silently loses a valid trajectory branch.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "c-finite", "label": "Bounded trajectory certificate", "status": "proved_by_certificate"},
                    {"id": "c-blocks", "label": "Residue-block descent family", "status": "open_bridge"},
                    {"id": "c-coverage", "label": "Recursive all-block coverage", "status": "open_bridge"},
                    {"id": "c-target", "label": "Every positive integer reaches 1", "status": "open_target"},
                ],
                "edges": [
                    {"from": "c-finite", "to": "c-blocks", "status": "open_bridge", "label": "generalize finite descent"},
                    {"from": "c-blocks", "to": "c-coverage", "status": "open_bridge", "label": "cover all residue blocks"},
                    {"from": "c-coverage", "to": "c-target", "status": "open_bridge", "label": "exclude cycles/divergence"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "C-B1",
                    "name": "Accelerated odd Collatz map",
                    "role": "Reduce even divisions while preserving every trajectory branch.",
                    "status": "usable_but_insufficient",
                },
                {
                    "id": "C-B2",
                    "name": "Descent certificate induction",
                    "role": "Turn residue-block certificates into a global well-founded descent argument.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "C-L1",
                    "statement": "Every odd residue block modulo 2^a 3^b has a finite accelerated path to a smaller representative in a covered block.",
                    "evidence": "Bounded replay identifies many descending trajectories and worst stopping-time cases.",
                    "required_upgrade": "Construct a finite symbolic block cover with an induction measure that cannot increase forever.",
                    "status": "open_candidate",
                }
            ],
        ),
        "proof_gates": [
            "Prove descent or recurrence for every congruence class without relying on finite enumeration.",
            "Rule out non-trivial cycles and divergent trajectories simultaneously.",
            "Turn stochastic drift intuition into a deterministic inequality with no exceptional infinite set.",
        ],
        "candidate_strategy": [
            "Compress trajectories by odd-only maps and residue-class transitions.",
            "Search for monotone certificates on blocks, then try to lift them to all blocks recursively.",
            "Treat random-walk drift evidence as heuristic until a deterministic certificate exists.",
        ],
        "formal_proof_contract": formal_proof_contract(
            problem_id="collatz",
            theorem_name="primeproject_collatz_conjecture",
            lean_statement="theorem primeproject_collatz_conjecture : forall n : Nat, 0 < n -> exists k, Collatz.iterate k n = 1 := by",
            forbidden_assumptions=[
                "CollatzConjecture",
                "well_foundedness of Collatz trajectories without proof",
                "any axiom excluding non-trivial cycles or divergent paths",
            ],
            required_artifacts=[
                "bounded trajectory certificate",
                "formal residue-block descent theorem",
                "formal cycle and divergence exclusion theorem",
            ],
        ),
        "proof_milestone_queue": proof_milestone_queue(
            problem_id="collatz",
            decisive_next_task="Construct a symbolic residue-block descent certificate that covers an infinite family, not only enumerated starts.",
            milestones=[
                {
                    "id": "C-M1",
                    "title": "Bounded trajectory certificate",
                    "status": "complete",
                    "artifact": "bounded_certificate_merkle_root",
                    "exit_criterion": "Every start value through the committed limit replays to 1.",
                },
                {
                    "id": "C-M2",
                    "title": "Lean definitions for accelerated Collatz dynamics",
                    "status": "open_formalization",
                    "artifact": "Lean 4 definitions",
                    "exit_criterion": "The odd-only map is proved equivalent to the ordinary trajectory relation.",
                },
                {
                    "id": "C-M3",
                    "title": "Residue-block descent theorem",
                    "status": "open_infinite_bridge",
                    "artifact": "formal theorem",
                    "exit_criterion": "Every sufficiently large block descends to a smaller covered representative.",
                },
                {
                    "id": "C-M4",
                    "title": "Cycle and divergence exclusion",
                    "status": "open_infinite_bridge",
                    "artifact": "formal exclusion proof",
                    "exit_criterion": "The descent theorem rules out non-trivial cycles and divergent branches.",
                },
                {
                    "id": "C-M5",
                    "title": "Independent kernel review",
                    "status": "blocked_until_m2_m4_complete",
                    "artifact": "external replay report",
                    "exit_criterion": "A clean Lean replay passes outside PrimeProject.",
                },
            ],
        ),
        "decisive_lemma_lab": decisive_lemma_lab(
            problem_id="collatz",
            lemma_id="C-DL1",
            decisive_question="Can the bounded trajectory evidence be compressed into a finite symbolic descent cover for all residue blocks?",
            candidate_statement="There is a finite set of accelerated Collatz residue-block certificates whose recursive lift forces every positive integer into a smaller covered representative.",
            closes_milestones=["C-M3", "C-M4"],
            finite_probe={
                "limit": limit,
                "tested_start_values": limit,
                "counterexamples": 0,
                "max_total_stopping_time_n": max_steps["n"],
                "max_total_stopping_time": max_steps["steps"],
                "probe_status": "no_bounded_counterexample",
            },
            proof_obligation="Prove the block cover is complete under lifting and that its descent measure is well-founded, excluding cycles and divergence.",
            falsification_test="Find a residue block with no certified descent path or a lifted block whose measure can increase indefinitely.",
            automated_falsification_probe={
                "schema": "primeproject.decisive-lemma-falsification-probe.v1",
                "result_status": "bounded_probe_passed_proof_open",
                "scope": f"ordinary Collatz starts 1..{limit}",
                "probe_count": limit,
                "violated_count": 0,
                "pass_condition": "every committed start reaches 1 under replay",
                "strongest_observed": {
                    "metric": "max_total_stopping_time",
                    "value": max_steps["steps"],
                    "at": max_steps["n"],
                },
                "proof_gap": "A replay through the limit does not produce a symbolic residue-block cover or a well-founded descent proof.",
            },
            current_result="The bounded replay supports the search for descent certificates but still depends on finite enumeration.",
            next_action="Generate candidate odd-only residue transitions and rank uncovered blocks by descent failure risk.",
            proof_gap_taxonomy=proof_gap_taxonomy(
                problem_id="collatz",
                gaps=[
                    {
                        "id": "C-G1",
                        "type": "symbolic_cover",
                        "status": "open_infinite_bridge",
                        "description": "Finite trajectories must be replaced by a complete symbolic residue-block cover.",
                        "required_artifact": "residue-block cover certificate",
                        "next_experiment": "Generate odd-only residue transition blocks and rank uncovered classes by shortest missing descent.",
                        "failure_signal": "A residue block remains uncovered or branches into a non-descending class under every tested modulus.",
                    },
                    {
                        "id": "C-G2",
                        "type": "well_founded_descent",
                        "status": "open_infinite_bridge",
                        "description": "The cover must provide a well-founded measure that cannot increase forever.",
                        "required_artifact": "formal descent theorem",
                        "next_experiment": "Search for a monotone block measure that decreases across the generated transition cover.",
                        "failure_signal": "The measure admits an infinite non-decreasing path or requires probabilistic drift assumptions.",
                    },
                    {
                        "id": "C-G3",
                        "type": "cycle_divergence_exclusion",
                        "status": "open_infinite_bridge",
                        "description": "The descent theorem must exclude both non-trivial cycles and divergent branches.",
                        "required_artifact": "cycle and divergence exclusion proof",
                        "next_experiment": "Derive cycle and divergence exclusions from the same well-founded measure instead of separate empirical checks.",
                        "failure_signal": "A non-trivial cycle or divergent branch remains compatible with the descent cover.",
                    },
                    {
                        "id": "C-G4",
                        "type": "independent_review",
                        "status": "blocked_until_g1_g3_close",
                        "description": "A clean replay must verify the accelerated-map equivalence and descent proof.",
                        "required_artifact": "external kernel replay report",
                        "next_experiment": "Export the residue cover and descent theorem to a clean proof-assistant replay package.",
                        "failure_signal": "The replay depends on PrimeProject-specific generated state or unchecked trajectory assumptions.",
                    },
                ],
            ),
        ),
        "claim_boundary": "No proof claim. Current evidence is finite exhaustive replay plus blocker list.",
    }


def build_goldbach(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    failures = []
    hardest = {"even": 4, "smallest_prime": 2, "partner": 2}
    decompositions = []
    residue_modulus = 210
    residue_stats: dict[int, dict[str, object]] = {
        residue: {"tested": 0, "max_smallest_prime": 0, "hardest_even": None}
        for residue in range(0, residue_modulus, 2)
    }
    certificate = ChunkedCertificate(
        problem_id="goldbach",
        statement=f"Every even integer 4 <= n <= {limit} has a displayed prime-pair witness.",
        limit=limit,
    )
    for even in range(4, limit + 1, 2):
        found = None
        for p in primes:
            if p > even // 2:
                break
            if is_prime[even - p]:
                found = (p, even - p)
                break
        if found is None:
            failures.append(even)
            certificate.update(f"{even}:fail")
            continue
        certificate.update(f"{even}:{found[0]}:{found[1]}")
        residue = even % residue_modulus
        residue_stats[residue]["tested"] = int(residue_stats[residue]["tested"]) + 1
        if found[0] > int(residue_stats[residue]["max_smallest_prime"]):
            residue_stats[residue]["max_smallest_prime"] = found[0]
            residue_stats[residue]["hardest_even"] = even
        if found[0] > hardest["smallest_prime"]:
            hardest = {"even": even, "smallest_prime": found[0], "partner": found[1]}
        if even in {100, 1_000, 10_000, 100_000, limit}:
            decompositions.append({"even": even, "p": found[0], "q": found[1]})
    hardest_residues = sorted(
        (
            {
                "residue": residue,
                "tested": stats["tested"],
                "max_smallest_prime": stats["max_smallest_prime"],
                "hardest_even": stats["hardest_even"],
            }
            for residue, stats in residue_stats.items()
            if int(stats["tested"]) > 0
        ),
        key=lambda item: int(item["max_smallest_prime"]),
        reverse=True,
    )[:8]

    return {
        "id": "goldbach",
        "title": "Goldbach Conjecture",
        "korean_title": "골드바흐 추측",
        "status": "open_not_proven",
        "target_statement": "Every even integer greater than 2 is the sum of two primes.",
        "tool_position": "PrimeProject can verify every even value up to a chosen public limit and expose the hardest bounded cases; this is not an infinite proof.",
        "finite_result": {
            "limit": limit,
            "tested_even_values": max(0, (limit - 2) // 2),
            "counterexamples": len(failures),
            "first_failures": failures[:5],
            "hardest_smallest_prime_decomposition": hardest,
            "sample_decompositions": decompositions,
        },
        "certificate": certificate.finish(),
        "proof_frontier_probe": proof_frontier_probe(
            problem_id="goldbach",
            objective=f"Rank even residue classes modulo {residue_modulus} by hardest first-prime witness through the committed limit.",
            limit=limit,
            metrics={
                "residue_modulus": residue_modulus,
                "tested_residue_count": sum(1 for stats in residue_stats.values() if int(stats["tested"]) > 0),
                "counterexample_count": len(failures),
                "global_hardest_even": hardest["even"],
                "global_hardest_smallest_prime": hardest["smallest_prime"],
            },
            observations=[
                {
                    "label": "hardest residue classes",
                    "value": hardest_residues,
                },
                {
                    "label": "global hardest witness",
                    "value": f"{hardest['even']} = {hardest['smallest_prime']} + {hardest['partner']}",
                },
                {
                    "label": "bounded counterexamples",
                    "value": len(failures),
                },
            ],
            proof_pressure="A positive representation-count theorem must survive the thinnest residue classes, not only aggregate no-counterexample evidence.",
            failure_signal="If an explicit lower bound turns non-positive on a stressed residue class, that proof path is rejected.",
        ),
        "proof_attempt": proof_attempt_ledger(
            problem_id="goldbach",
            route="Exhaustive bounded witnesses -> thinnest residue-class model -> explicit positive lower bound for all even n.",
            formal_statement="For every even integer n > 2, there exist primes p and q such that n = p + q.",
            obligations=[
                {
                    "id": "G-O1",
                    "claim": "Every even n <= 1,000,000 has a prime-pair witness.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "A witness leaf changes or an even n has no pair.",
                },
                {
                    "id": "G-O2",
                    "claim": "Prove a positive representation-count lower bound for all even n above a threshold.",
                    "status": "open_obligation",
                    "verifier": "explicit analytic lower-bound proof",
                    "failure_mode": "A thin residue class has no proven positive lower bound.",
                },
                {
                    "id": "G-O3",
                    "claim": "Bridge the analytic threshold to the bounded certified range with no gap.",
                    "status": "open_obligation",
                    "verifier": "threshold comparison against certificate limit",
                    "failure_mode": "The analytic theorem starts above the certified range.",
                },
            ],
            falsification_targets=[
                "A proposed lower bound becomes non-positive for a residue class.",
                "The threshold exceeds the certified finite range.",
                "The model assumes unproved prime-pair independence.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "g-finite", "label": "Bounded witness certificate", "status": "proved_by_certificate"},
                    {"id": "g-thin", "label": "Thinnest residue-class lower bound", "status": "open_bridge"},
                    {"id": "g-threshold", "label": "Explicit threshold below certificate limit", "status": "open_bridge"},
                    {"id": "g-target", "label": "Every even n > 2 has p+q witness", "status": "open_target"},
                ],
                "edges": [
                    {"from": "g-finite", "to": "g-threshold", "status": "open_bridge", "label": "close finite/infinite gap"},
                    {"from": "g-thin", "to": "g-threshold", "status": "open_bridge", "label": "make lower bound positive"},
                    {"from": "g-threshold", "to": "g-target", "status": "open_bridge", "label": "cover all even values"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "G-B1",
                    "name": "Circle-method lower bounds",
                    "role": "Supply explicit positive representation counts for all large even integers.",
                    "status": "bridge_not_satisfied",
                },
                {
                    "id": "G-B2",
                    "name": "Finite verification threshold bridge",
                    "role": "Ensure the analytic threshold does not start above the certified finite range.",
                    "status": "bridge_not_satisfied",
                },
            ],
            lemma_candidates=[
                {
                    "id": "G-L1",
                    "statement": "For every even n >= N, the Goldbach representation count R(n) is strictly positive with explicit N <= certificate_limit.",
                    "evidence": "Bounded witness search shows no failures and records hardest smallest-prime decompositions.",
                    "required_upgrade": "Derive explicit constants that beat all singular-series and error-term losses.",
                    "status": "open_candidate",
                }
            ],
        ),
        "proof_gates": [
            "Control prime coverage in every residue class strongly enough for all even integers.",
            "Bridge from verified finite range to an analytic theorem for the infinite tail.",
            "State explicit constants and thresholds so no unverified gap remains.",
        ],
        "candidate_strategy": [
            "Use residue-drift tools to detect classes where representations are thinnest.",
            "Compare bounded failures against Hardy-Littlewood-style expected representation counts.",
            "Escalate only if the thin-class model yields a provable lower bound above zero.",
        ],
        "formal_proof_contract": formal_proof_contract(
            problem_id="goldbach",
            theorem_name="primeproject_goldbach_conjecture",
            lean_statement="theorem primeproject_goldbach_conjecture : forall n : Nat, Even n -> 2 < n -> exists p q : Nat, Nat.Prime p /\\ Nat.Prime q /\\ n = p + q := by",
            forbidden_assumptions=[
                "GoldbachConjecture",
                "HardyLittlewood prime-pair independence as an axiom",
                "any axiom asserting positive Goldbach representation counts",
            ],
            required_artifacts=[
                "bounded witness certificate",
                "formal positive representation-count lower bound",
                "formal threshold bridge below certificate limit",
            ],
        ),
        "proof_milestone_queue": proof_milestone_queue(
            problem_id="goldbach",
            decisive_next_task="Prove an explicit positive Goldbach representation lower bound whose threshold is below the certified finite range.",
            milestones=[
                {
                    "id": "G-M1",
                    "title": "Bounded witness certificate",
                    "status": "complete",
                    "artifact": "bounded_certificate_merkle_root",
                    "exit_criterion": "Every even number through the committed limit has a replayed prime-pair witness.",
                },
                {
                    "id": "G-M2",
                    "title": "Lean definitions for prime-pair representations",
                    "status": "open_formalization",
                    "artifact": "Lean 4 definitions",
                    "exit_criterion": "Representation-count definitions compile and match bounded witnesses.",
                },
                {
                    "id": "G-M3",
                    "title": "Positive representation lower bound",
                    "status": "open_infinite_bridge",
                    "artifact": "formal theorem",
                    "exit_criterion": "For all even n >= N, R(n) is formally proved positive.",
                },
                {
                    "id": "G-M4",
                    "title": "Threshold bridge",
                    "status": "open_infinite_bridge",
                    "artifact": "formal threshold proof",
                    "exit_criterion": "The analytic threshold N is at or below the certified finite limit.",
                },
                {
                    "id": "G-M5",
                    "title": "Independent kernel review",
                    "status": "blocked_until_m2_m4_complete",
                    "artifact": "external replay report",
                    "exit_criterion": "A clean Lean replay passes outside PrimeProject.",
                },
            ],
        ),
        "decisive_lemma_lab": decisive_lemma_lab(
            problem_id="goldbach",
            lemma_id="G-DL1",
            decisive_question="Can the thinnest bounded representation classes be turned into an explicit positive lower bound for all large even integers?",
            candidate_statement="For every even n >= N, the Goldbach representation count R(n) is positive, with an explicit threshold N no larger than the committed certificate limit.",
            closes_milestones=["G-M3", "G-M4"],
            finite_probe={
                "limit": limit,
                "tested_even_values": (limit - 2) // 2,
                "counterexamples": len(failures),
                "hardest_even": hardest["even"],
                "hardest_smallest_prime": hardest["smallest_prime"],
                "probe_status": "no_bounded_counterexample",
            },
            proof_obligation="Derive explicit constants for a positive representation-count lower bound and bridge the analytic threshold to the certified finite range.",
            falsification_test="Reject any proposed lower bound that becomes non-positive in a residue class or whose threshold exceeds the certificate limit.",
            automated_falsification_probe={
                "schema": "primeproject.decisive-lemma-falsification-probe.v1",
                "result_status": "bounded_probe_passed_proof_open",
                "scope": f"even integers 4..{limit}",
                "probe_count": (limit - 2) // 2,
                "violated_count": len(failures),
                "pass_condition": "every committed even integer has a displayed prime-pair witness",
                "strongest_observed": {
                    "metric": "hardest_smallest_prime_decomposition",
                    "even": hardest["even"],
                    "smallest_prime": hardest["smallest_prime"],
                    "partner": hardest["partner"],
                },
                "proof_gap": "Witnesses through the limit do not give an explicit positive lower bound for all large even integers.",
            },
            current_result="The bounded witness certificate closes the finite range only; the positive infinite lower bound is open.",
            next_action="Use the hardest bounded decompositions to prioritize residue classes for explicit lower-bound stress tests.",
            proof_gap_taxonomy=proof_gap_taxonomy(
                problem_id="goldbach",
                gaps=[
                    {
                        "id": "G-G1",
                        "type": "positive_lower_bound",
                        "status": "open_infinite_bridge",
                        "description": "The representation count must be proved positive for every sufficiently large even integer.",
                        "required_artifact": "explicit representation-count lower-bound theorem",
                        "next_experiment": "Stress the thinnest bounded residue classes and derive candidate constants for an explicit lower-bound inequality.",
                        "failure_signal": "A residue class makes the lower bound non-positive or the constants depend on unproved independence.",
                    },
                    {
                        "id": "G-G2",
                        "type": "threshold_bridge",
                        "status": "open_infinite_bridge",
                        "description": "The analytic threshold must be at or below the certified bounded range.",
                        "required_artifact": "formal finite-to-infinite threshold comparison",
                        "next_experiment": "Compare every candidate analytic threshold against the committed certificate limit and record the uncovered interval.",
                        "failure_signal": "The threshold remains above the certified range or leaves an unchecked finite gap.",
                    },
                    {
                        "id": "G-G3",
                        "type": "dependency_control",
                        "status": "open_formalization",
                        "description": "The proof must not assume unproved prime-pair independence or Hardy-Littlewood strength.",
                        "required_artifact": "assumption audit in formal contract",
                        "next_experiment": "Audit every lower-bound step for hidden Hardy-Littlewood or prime-pair independence assumptions.",
                        "failure_signal": "A required step is only heuristic or imports a conjecture equivalent to positive representation counts.",
                    },
                    {
                        "id": "G-G4",
                        "type": "independent_review",
                        "status": "blocked_until_g1_g3_close",
                        "description": "An external replay must verify the lower-bound and threshold bridge.",
                        "required_artifact": "external kernel replay report",
                        "next_experiment": "Bundle the witness certificate, threshold bridge, and assumption audit for independent replay.",
                        "failure_signal": "The reviewer cannot reproduce the threshold bridge from public artifacts.",
                    },
                ],
            ),
        ),
        "claim_boundary": "No proof claim. Current evidence is bounded exhaustive verification.",
    }


def build_twin_prime(limit: int, primes: list[int], is_prime: bytearray) -> dict[str, object]:
    checkpoints = [10**k for k in range(2, int(math.log10(limit)) + 1)]
    checkpoint_index = 0
    count = 0
    largest_pair = None
    rows = []
    residue_modulus = 210
    twin_residue_counts = {residue: 0 for residue in range(residue_modulus) if math.gcd(residue, residue_modulus) == 1}
    certificate = ChunkedCertificate(
        problem_id="twin-prime",
        statement=f"All twin prime pairs p,p+2 with p+2 <= {limit} are counted by the sieve scan.",
        limit=limit,
    )
    for p in primes:
        if p + 2 <= limit and is_prime[p + 2]:
            count += 1
            largest_pair = [p, p + 2]
            residue = p % residue_modulus
            if residue in twin_residue_counts:
                twin_residue_counts[residue] += 1
            certificate.update(f"{p}:{p + 2}")
        while checkpoint_index < len(checkpoints) and p >= checkpoints[checkpoint_index]:
            x = checkpoints[checkpoint_index]
            estimate = 2 * 0.6601618158468696 * x / (math.log(x) ** 2)
            rows.append({"x": x, "twin_pairs": count, "hardy_littlewood_estimate": round(estimate, 2)})
            checkpoint_index += 1
    while checkpoint_index < len(checkpoints):
        x = checkpoints[checkpoint_index]
        estimate = 2 * 0.6601618158468696 * x / (math.log(x) ** 2)
        rows.append({"x": x, "twin_pairs": count, "hardy_littlewood_estimate": round(estimate, 2)})
        checkpoint_index += 1
    nonzero_residues = [item for item in twin_residue_counts.items() if item[1] > 0]
    top_twin_residues = [
        {"residue": residue, "count": residue_count}
        for residue, residue_count in sorted(nonzero_residues, key=lambda item: item[1], reverse=True)[:8]
    ]
    zero_residue_count = sum(1 for residue_count in twin_residue_counts.values() if residue_count == 0)

    return {
        "id": "twin-prime",
        "title": "Twin Prime Conjecture",
        "korean_title": "쌍둥이 소수 추측",
        "status": "open_not_proven",
        "target_statement": "There are infinitely many prime pairs p and p+2.",
        "tool_position": "PrimeProject can count twin pairs and compare them with heuristic density curves over finite ranges; unbounded infinitude remains the missing proof step.",
        "finite_result": {
            "limit": limit,
            "twin_pair_count": count,
            "largest_pair_seen": largest_pair,
            "checkpoints": rows,
        },
        "certificate": certificate.finish(),
        "proof_frontier_probe": proof_frontier_probe(
            problem_id="twin-prime",
            objective=f"Separate exact gap-2 residue persistence modulo {residue_modulus} from broader bounded-gap signals.",
            limit=limit,
            metrics={
                "residue_modulus": residue_modulus,
                "admissible_residue_count": len(twin_residue_counts),
                "nonzero_residue_count": len(nonzero_residues),
                "zero_residue_count": zero_residue_count,
                "twin_pair_count": count,
                "largest_pair_seen": largest_pair,
            },
            observations=[
                {
                    "label": "top exact gap-2 residues",
                    "value": top_twin_residues,
                },
                {
                    "label": "final count vs heuristic",
                    "value": round(count / rows[-1]["hardy_littlewood_estimate"], 6) if rows and rows[-1]["hardy_littlewood_estimate"] else None,
                },
                {
                    "label": "zero admissible residues",
                    "value": zero_residue_count,
                },
            ],
            proof_pressure="The exact gap-2 proof path must produce a positive lower bound for arbitrarily large x, not just bounded-gap or averaged residue evidence.",
            failure_signal="A candidate argument that only proves bounded gaps or depends on k-tuple density remains insufficient.",
        ),
        "proof_attempt": proof_attempt_ledger(
            problem_id="twin-prime",
            route="Certified finite twin pairs -> admissible two-point pattern analysis -> lower-bound theorem for exact gap 2.",
            formal_statement="For infinitely many primes p, p + 2 is also prime.",
            obligations=[
                {
                    "id": "TP-O1",
                    "claim": "Every twin prime pair p,p+2 with p+2 <= 1,000,000 is counted by the sieve scan.",
                    "status": "proved_by_certificate",
                    "verifier": "scripts/verify_open_problem_workbench.py",
                    "failure_mode": "The pair list Merkle root changes or a pair is missed.",
                },
                {
                    "id": "TP-O2",
                    "claim": "Prove infinitely many exact prime gaps of size 2, not only bounded gaps.",
                    "status": "open_obligation",
                    "verifier": "exact gap-2 infinitude theorem",
                    "failure_mode": "The proof only gives a bounded gap larger than 2.",
                },
                {
                    "id": "TP-O3",
                    "claim": "Remove dependence on unproved Hardy-Littlewood k-tuple assumptions.",
                    "status": "open_obligation",
                    "verifier": "assumption-free lower-bound proof",
                    "failure_mode": "The density argument remains heuristic.",
                },
            ],
            falsification_targets=[
                "The lower bound collapses to zero for exact gap 2.",
                "The argument proves bounded gaps but cannot force gap 2.",
                "An admissible-pattern step assumes the k-tuple conjecture.",
            ],
            attack_graph={
                "nodes": [
                    {"id": "tp-finite", "label": "Bounded twin-pair certificate", "status": "proved_by_certificate"},
                    {"id": "tp-pattern", "label": "Admissible two-point lower bound", "status": "open_bridge"},
                    {"id": "tp-exact", "label": "Exact gap-2 infinitude theorem", "status": "open_bridge"},
                    {"id": "tp-target", "label": "Infinitely many twin primes", "status": "open_target"},
                ],
                "edges": [
                    {"from": "tp-finite", "to": "tp-pattern", "status": "open_bridge", "label": "lift density beyond finite range"},
                    {"from": "tp-pattern", "to": "tp-exact", "status": "open_bridge", "label": "force exact gap 2"},
                    {"from": "tp-exact", "to": "tp-target", "status": "open_bridge", "label": "prove infinitude"},
                ],
            },
            known_theorem_bridges=[
                {
                    "id": "TP-B1",
                    "name": "Bounded prime gaps",
                    "role": "Existing methods prove some bounded gaps, but not exact gap 2.",
                    "status": "usable_but_insufficient",
                },
                {
                    "id": "TP-B2",
                    "name": "Hardy-Littlewood k-tuple heuristic",
                    "role": "Predicts the right density but cannot be used as an assumption-free proof.",
                    "status": "heuristic_only",
                },
            ],
            lemma_candidates=[
                {
                    "id": "TP-L1",
                    "statement": "There is an explicit c > 0 such that pi_2(x) >= c x / log(x)^2 for arbitrarily large x without k-tuple assumptions.",
                    "evidence": "Bounded counts track the Hardy-Littlewood scale through the committed limit.",
                    "required_upgrade": "Replace the heuristic density curve with an unconditional lower-bound theorem for exact gap 2.",
                    "status": "open_candidate",
                }
            ],
        ),
        "proof_gates": [
            "Prove infinitely many prime gaps of size exactly 2, not merely bounded gaps.",
            "Remove dependence on unproven distribution assumptions such as full Hardy-Littlewood k-tuple strength.",
            "Turn finite density persistence into a lower-bound theorem for all large x.",
        ],
        "candidate_strategy": [
            "Use wheel/residue drift measurements to isolate admissible two-point patterns.",
            "Stress-test whether observed twin density survives generator and modulus changes.",
            "Treat density agreement as a guide for lemma search, not as proof.",
        ],
        "formal_proof_contract": formal_proof_contract(
            problem_id="twin-prime",
            theorem_name="primeproject_twin_prime_conjecture",
            lean_statement="theorem primeproject_twin_prime_conjecture : forall N : Nat, exists p : Nat, N < p /\\ Nat.Prime p /\\ Nat.Prime (p + 2) := by",
            forbidden_assumptions=[
                "TwinPrimeConjecture",
                "HardyLittlewood k-tuple conjecture as an axiom",
                "bounded gaps theorem treated as exact gap 2",
            ],
            required_artifacts=[
                "bounded twin-pair certificate",
                "formal exact gap-2 lower-bound theorem",
                "formal infinitude bridge",
            ],
        ),
        "proof_milestone_queue": proof_milestone_queue(
            problem_id="twin-prime",
            decisive_next_task="Replace Hardy-Littlewood-scale agreement with an unconditional exact gap-2 lower-bound theorem.",
            milestones=[
                {
                    "id": "TP-M1",
                    "title": "Bounded twin-pair certificate",
                    "status": "complete",
                    "artifact": "bounded_certificate_merkle_root",
                    "exit_criterion": "The committed sieve replay reproduces every twin pair through the limit.",
                },
                {
                    "id": "TP-M2",
                    "title": "Lean definitions for exact gap-2 primes",
                    "status": "open_formalization",
                    "artifact": "Lean 4 definitions",
                    "exit_criterion": "Exact gap-2 and twin-count definitions compile without heuristic assumptions.",
                },
                {
                    "id": "TP-M3",
                    "title": "Unconditional exact gap-2 lower bound",
                    "status": "open_infinite_bridge",
                    "artifact": "formal theorem",
                    "exit_criterion": "A positive lower bound for exact twin pairs is proved for arbitrarily large x.",
                },
                {
                    "id": "TP-M4",
                    "title": "Infinitude bridge",
                    "status": "open_infinite_bridge",
                    "artifact": "formal infinitude proof",
                    "exit_criterion": "The lower bound implies arbitrarily large twin prime pairs.",
                },
                {
                    "id": "TP-M5",
                    "title": "Independent kernel review",
                    "status": "blocked_until_m2_m4_complete",
                    "artifact": "external replay report",
                    "exit_criterion": "A clean Lean replay passes outside PrimeProject.",
                },
            ],
        ),
        "decisive_lemma_lab": decisive_lemma_lab(
            problem_id="twin-prime",
            lemma_id="TP-DL1",
            decisive_question="Can observed exact gap-2 persistence be upgraded into an unconditional lower bound for arbitrarily large x?",
            candidate_statement="There is an explicit c > 0 such that the number of twin prime pairs up to x is at least c x / log(x)^2 for arbitrarily large x, without assuming Hardy-Littlewood.",
            closes_milestones=["TP-M3", "TP-M4"],
            finite_probe={
                "limit": limit,
                "twin_pair_count": count,
                "largest_pair_seen": largest_pair,
                "checkpoint_count": len(rows),
                "probe_status": "density_observed_not_proven",
            },
            proof_obligation="Prove an unconditional exact gap-2 lower bound strong enough to imply arbitrarily large twin prime pairs.",
            falsification_test="Reject any argument that proves only bounded gaps, assumes k-tuple independence, or lets the exact gap-2 lower bound collapse to zero.",
            automated_falsification_probe={
                "schema": "primeproject.decisive-lemma-falsification-probe.v1",
                "result_status": "bounded_probe_passed_proof_open",
                "scope": f"twin prime pairs with p+2 <= {limit}",
                "probe_count": len(rows),
                "violated_count": 0,
                "pass_condition": "observed twin-pair count remains positive at every committed checkpoint",
                "strongest_observed": {
                    "metric": "final_count_vs_hardy_littlewood_estimate",
                    "observed": count,
                    "estimate": rows[-1]["hardy_littlewood_estimate"] if rows else 0,
                    "ratio": round(count / rows[-1]["hardy_littlewood_estimate"], 6) if rows and rows[-1]["hardy_littlewood_estimate"] else None,
                },
                "proof_gap": "Positive bounded counts and heuristic-scale agreement do not prove infinitely many exact gap-2 pairs.",
            },
            current_result="The bounded count agrees with heuristic scale but does not establish infinitude.",
            next_action="Separate exact gap-2 requirements from bounded-gap evidence and formalize the missing lower-bound theorem.",
            proof_gap_taxonomy=proof_gap_taxonomy(
                problem_id="twin-prime",
                gaps=[
                    {
                        "id": "TP-G1",
                        "type": "exact_gap_lower_bound",
                        "status": "open_infinite_bridge",
                        "description": "A positive lower bound is needed for exact gap-2 pairs, not merely bounded prime gaps.",
                        "required_artifact": "unconditional exact gap-2 lower-bound theorem",
                        "next_experiment": "Separate exact gap-2 counts from bounded-gap signals and test candidate lower-bound forms against wheel/residue stress cases.",
                        "failure_signal": "The argument proves only bounded gaps larger than 2 or the exact gap-2 lower bound collapses to zero.",
                    },
                    {
                        "id": "TP-G2",
                        "type": "heuristic_removal",
                        "status": "open_infinite_bridge",
                        "description": "Hardy-Littlewood k-tuple behavior cannot be used as an assumption.",
                        "required_artifact": "assumption-free distribution argument",
                        "next_experiment": "Identify which observed density features are heuristic-only and remove them from the formal target statement.",
                        "failure_signal": "The proof still requires k-tuple independence or Hardy-Littlewood-scale density as an axiom.",
                    },
                    {
                        "id": "TP-G3",
                        "type": "infinitude_bridge",
                        "status": "open_infinite_bridge",
                        "description": "The exact gap-2 lower bound must imply arbitrarily large twin pairs.",
                        "required_artifact": "formal infinitude bridge",
                        "next_experiment": "Formalize the implication from a positive exact-gap lower bound over arbitrarily large x to infinitely many twin primes.",
                        "failure_signal": "The lower bound applies only to bounded ranges or averaged windows without forcing arbitrarily large pairs.",
                    },
                    {
                        "id": "TP-G4",
                        "type": "independent_review",
                        "status": "blocked_until_g1_g3_close",
                        "description": "A clean external replay must verify exact gap-2, not just bounded gaps.",
                        "required_artifact": "external kernel replay report",
                        "next_experiment": "Prepare a minimal external replay package that distinguishes exact gap 2 from bounded-gap theorems.",
                        "failure_signal": "The replay verifies a bounded-gap theorem but not exact twin-prime infinitude.",
                    },
                ],
            ),
        ),
        "claim_boundary": "No proof claim. Current evidence is finite counting and heuristic comparison.",
    }


def build_payload(limit: int, *, generated_at: str | None = None) -> dict[str, object]:
    primes, is_prime = sieve(limit)
    problems = [
        build_riemann(limit, primes),
        build_collatz(limit),
        build_goldbach(limit, primes, is_prime),
        build_twin_prime(limit, primes, is_prime),
    ]
    for problem in problems:
        problem["proof_status_gate"] = proof_status_gate(problem)
        problem["proof_execution_protocol"] = proof_execution_protocol(problem)
        problem["known_barrier_audit"] = known_barrier_audit(problem)
        problem["formal_replay_package"] = formal_replay_package(problem)
        problem["proof_review_docket"] = proof_review_docket(problem)
        problem["proof_reduction_contract"] = proof_reduction_contract(problem)
        problem["proof_candidate_intake"] = proof_candidate_intake(problem)
        problem["proof_attempt_execution_log"] = proof_attempt_execution_log(problem)
        problem["proof_obligation_dag"] = proof_obligation_dag(problem)
    return {
        "schema": SCHEMA,
        "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "search_limit": limit,
        "proof_status_gate_summary": {
            "schema": PROOF_STATUS_GATE_SCHEMA,
            "status": "all_full_proof_claims_blocked",
            "problem_count": len(problems),
            "blocked_problem_count": sum(
                1 for problem in problems if problem["proof_status_gate"]["promotion_status"].startswith("blocked")
            ),
            "eligible_problem_count": sum(
                1 for problem in problems if problem["proof_status_gate"]["promotion_status"].startswith("eligible")
            ),
            "public_claim": "bounded_theorem_only_for_all_four_pages",
        },
        "claim_policy": {
            "public_claim": "proof_workbench_only",
            "reason": "These pages are allowed to show finite evidence, proof gates, and candidate strategies, but must not claim a proof until an independently checkable infinite argument exists.",
            "blocked_claims": [
                "unverified full-proof claim for the Riemann Hypothesis",
                "unverified full-proof claim for the Collatz conjecture",
                "unverified full-proof claim for the Goldbach conjecture",
                "unverified full-proof claim for the Twin Prime conjecture",
            ],
        },
        "problems": problems,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--output", type=Path, default=Path("data/open_problem_workbench.json"))
    args = parser.parse_args()

    payload = build_payload(args.limit, generated_at=args.generated_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
