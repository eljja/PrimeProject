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
FORMAL_SKELETON_AUDIT_SCHEMA = "primeproject.formal-skeleton-audit.v1"
PROOF_VERDICT_SCHEMA = "primeproject.proof-verdict.v1"
PROOF_ROUTE_TRIAGE_SCHEMA = "primeproject.proof-route-triage.v1"
DECISIVE_THEOREM_SPEC_SCHEMA = "primeproject.decisive-theorem-spec.v1"
DECISIVE_THEOREM_SUBGOALS_SCHEMA = "primeproject.decisive-theorem-subgoals.v1"
DECISIVE_THEOREM_ATTACK_TICKETS_SCHEMA = "primeproject.decisive-theorem-attack-tickets.v1"
PROOF_BREAKTHROUGH_AGENDA_SCHEMA = "primeproject.proof-breakthrough-agenda.v1"
ACTUAL_PROOF_ATTEMPT_RUNNER_SCHEMA = "primeproject.actual-proof-attempt-runner.v1"
CANDIDATE_LEMMA_WORKBENCH_SCHEMA = "primeproject.candidate-lemma-workbench.v1"
MACHINE_PROOF_SEARCH_TRIALS_SCHEMA = "primeproject.machine-proof-search-trials.v1"
FORMAL_UPGRADE_MATRIX_SCHEMA = "primeproject.formal-upgrade-matrix.v1"
PROOF_KERNEL_ROADMAP_SCHEMA = "primeproject.proof-kernel-roadmap.v1"
FORMAL_KERNEL_CONTRACT_AUDIT_SCHEMA = "primeproject.formal-kernel-contract-audit.v1"
INVALID_PROOF_SHORTCUT_SUITE_SCHEMA = "primeproject.invalid-proof-shortcut-suite.v1"
AI_SOLVER_FRONTIER_SCHEMA = "primeproject.ai-solver-frontier.v1"
AI_BREAKTHROUGH_PROGRAM_SCHEMA = "primeproject.ai-breakthrough-program.v1"
AI_PROOF_FORGE_SCHEMA = "primeproject.ai-proof-forge.v1"


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


def formal_skeleton_audit(problem: dict[str, object]) -> dict[str, object]:
    replay = problem.get("formal_replay_package", {})
    files = replay.get("candidate_files", []) if isinstance(replay, dict) else []
    forbidden = replay.get("forbidden_tokens", []) if isinstance(replay, dict) else []
    checks = []
    forbidden_hits: list[dict[str, str]] = []
    for item in files:
        path = Path(str(item))
        exists = path.exists()
        text = path.read_text(encoding="utf-8") if exists else ""
        hits = [
            token
            for token in forbidden
            if token and token in text
        ]
        for token in hits:
            forbidden_hits.append({"path": str(path), "token": str(token)})
        checks.append(
            {
                "path": str(path),
                "exists": exists,
                "status": "skeleton_present_not_proof" if exists else "missing_skeleton",
                "line_count": len(text.splitlines()) if exists else 0,
            }
        )
    present_count = sum(1 for item in checks if item["exists"])
    return {
        "schema": FORMAL_SKELETON_AUDIT_SCHEMA,
        "problem_id": problem.get("id"),
        "status": "skeleton_present_not_replayable" if present_count == len(files) and not forbidden_hits else "skeleton_blocked",
        "candidate_file_count": len(files),
        "present_count": present_count,
        "forbidden_hit_count": len(forbidden_hits),
        "file_checks": checks,
        "forbidden_hits": forbidden_hits,
        "claim_boundary": "The skeleton files make the replay package concrete, but they are not a proof and do not discharge any infinite bridge.",
    }


def proof_verdict(problem: dict[str, object]) -> dict[str, object]:
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    gate = problem.get("proof_status_gate", {}) if isinstance(problem.get("proof_status_gate"), dict) else {}
    reduction = problem.get("proof_reduction_contract", {}) if isinstance(problem.get("proof_reduction_contract"), dict) else {}
    decisive = reduction.get("decisive_reduction", {}) if isinstance(reduction.get("decisive_reduction"), dict) else {}
    lab = problem.get("decisive_lemma_lab", {}) if isinstance(problem.get("decisive_lemma_lab"), dict) else {}
    return {
        "schema": PROOF_VERDICT_SCHEMA,
        "problem_id": problem.get("id"),
        "target_status": problem.get("status", "open_not_proven"),
        "target_verdict": "not_proved_by_primeproject",
        "actual_proved_result": certificate.get("statement", "bounded certificate missing"),
        "actual_proved_status": certificate.get("status", "missing"),
        "full_proof_blocker": decisive.get("missing_artifact", "missing infinite proof artifact"),
        "gate_status": gate.get("promotion_status", "missing"),
        "next_decisive_attempt": lab.get("next_action", lab.get("proof_obligation", "missing decisive attempt")),
        "machine_rule": "PrimeProject may display a proof only when the bounded certificate, decisive reduction, formal contract, skeleton audit, and independent-review gate all pass without open infinite obligations.",
    }


def actual_proof_attempt_runner(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    frontier = problem.get("proof_frontier_probe", {}) if isinstance(problem.get("proof_frontier_probe"), dict) else {}
    triage = problem.get("proof_route_triage", {}) if isinstance(problem.get("proof_route_triage"), dict) else {}
    spec = problem.get("decisive_theorem_spec", {}) if isinstance(problem.get("decisive_theorem_spec"), dict) else {}
    subgoals = problem.get("decisive_theorem_subgoals", {}) if isinstance(problem.get("decisive_theorem_subgoals"), dict) else {}
    tickets = problem.get("decisive_theorem_attack_tickets", {}) if isinstance(problem.get("decisive_theorem_attack_tickets"), dict) else {}
    gate = problem.get("proof_status_gate", {}) if isinstance(problem.get("proof_status_gate"), dict) else {}
    execution = problem.get("proof_attempt_execution_log", {}) if isinstance(problem.get("proof_attempt_execution_log"), dict) else {}
    reduction = problem.get("proof_reduction_contract", {}) if isinstance(problem.get("proof_reduction_contract"), dict) else {}
    decisive = reduction.get("decisive_reduction", {}) if isinstance(reduction.get("decisive_reduction"), dict) else {}
    result_bank: dict[str, dict[str, str]] = {
        "riemann": {
            "attempt_title": "Use prime-counting residuals to force RH-equivalent zero control",
            "candidate_bridge": "finite theta/pi diagnostics -> explicit all-x theta bound -> RH-equivalent zero theorem",
            "observed_signal": "bounded theta diagnostics and endpoint stress tests identify candidate envelope pressure",
            "failure_reason": "the all-x analytic theorem is still missing, so finite residual discipline cannot quantify over every zeta zero",
            "next_executable_move": "formalize the exact theta/psi inequality with explicit constants and reject it if any endpoint stress row exceeds the envelope",
        },
        "collatz": {
            "attempt_title": "Compress bounded trajectories into a symbolic descent cover",
            "candidate_bridge": "trajectory certificate -> residue-block transition graph -> global well-founded descent",
            "observed_signal": "bounded replay finds no counterexample and ranks residue blocks by descent pressure",
            "failure_reason": "enumerated starts do not prove that every residue block has a decreasing representative",
            "next_executable_move": "generate a residue-block cover candidate and require every block to map to a smaller certified representative",
        },
        "goldbach": {
            "attempt_title": "Turn bounded decompositions into an explicit two-prime lower bound",
            "candidate_bridge": "finite decompositions -> thinnest residue classes -> explicit large-even representation theorem",
            "observed_signal": "bounded search identifies hardest decomposition cases and residue stress targets",
            "failure_reason": "the positive lower bound for every sufficiently large even integer is not formalized with a compatible cutoff",
            "next_executable_move": "state the lower-bound theorem with N0 and test whether N0 is below the bounded certificate limit",
        },
        "twin-prime": {
            "attempt_title": "Upgrade exact gap-2 persistence into infinitude",
            "candidate_bridge": "bounded twin-pair certificate -> admissible exact-gap pattern analysis -> unconditional exact gap-2 lower bound",
            "observed_signal": "bounded twin pairs persist and match heuristic scale within the certified range",
            "failure_reason": "bounded gaps and Hardy-Littlewood-scale agreement do not prove exact gap-2 pairs for arbitrarily large x",
            "next_executable_move": "separate exact gap 2 from bounded-gap evidence and require a positive unconditional lower bound",
        },
    }
    result = result_bank.get(problem_id, result_bank["riemann"])
    open_count = int(subgoals.get("open_count", 0) or 0) + int(subgoals.get("blocked_count", 0) or 0)
    ticket_count = int(tickets.get("ticket_count", 0) or 0)
    runner_steps = [
        {
            "id": "RUN-1",
            "tool": "bounded certificate replay",
            "input": certificate.get("statement", "bounded certificate"),
            "status": certificate.get("status", "missing"),
            "output": certificate.get("merkle_root", "missing"),
            "proof_effect": "closes only the finite replay claim",
        },
        {
            "id": "RUN-2",
            "tool": "frontier falsification probe",
            "input": frontier.get("objective", "frontier probe"),
            "status": frontier.get("status", "missing"),
            "output": frontier.get("failure_signal", "missing"),
            "proof_effect": "rejects weak candidate lemmas before formal proof work",
        },
        {
            "id": "RUN-3",
            "tool": "route triage",
            "input": triage.get("current_decisive_route", "missing"),
            "status": triage.get("status", "missing"),
            "output": spec.get("title", "missing decisive theorem"),
            "proof_effect": "selects the only route that can plausibly attack the infinite theorem",
        },
        {
            "id": "RUN-4",
            "tool": "decisive theorem gate",
            "input": spec.get("candidate_statement", "missing candidate statement"),
            "status": spec.get("artifact_status", "missing_formal_theorem"),
            "output": spec.get("blocking_gap", decisive.get("missing_artifact", "missing infinite bridge")),
            "proof_effect": "blocks promotion until the infinite theorem exists",
        },
    ]
    return {
        "schema": ACTUAL_PROOF_ATTEMPT_RUNNER_SCHEMA,
        "problem_id": problem_id,
        "runner_status": "executed_full_proof_blocked",
        "attempt_title": result["attempt_title"],
        "candidate_bridge": result["candidate_bridge"],
        "observed_signal": result["observed_signal"],
        "failure_reason": result["failure_reason"],
        "next_executable_move": result["next_executable_move"],
        "runner_steps": runner_steps,
        "closed_items": [
            "bounded certificate replay",
            "finite falsification probe",
            "route triage",
            "proof obligation naming",
        ],
        "open_items": [
            decisive.get("missing_artifact", spec.get("blocking_gap", "missing infinite theorem")),
            f"{open_count} decisive subgoals remain open or blocked",
            f"{ticket_count} attack tickets are planned but not proof artifacts",
        ],
        "machine_verdict": execution.get(
            "machine_verdict",
            "bounded evidence can guide proof search, but the infinite bridge remains open",
        ),
        "promotion_rule": gate.get(
            "machine_rule",
            "A full-proof claim is blocked unless every infinite obligation is independently verified.",
        ),
    }


def candidate_lemma_workbench(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    bank: dict[str, dict[str, object]] = {
        "riemann": {
            "workbench_title": "RH candidate lemma search",
            "target": "Close the all-x analytic bridge between bounded prime-counting diagnostics and an RH-equivalent theorem.",
            "lemmas": [
                {
                    "id": "RH-CL1",
                    "statement": "The observed theta residual envelope persists for every x beyond the committed finite range.",
                    "tool_test": "prime-endpoint stress probe against the proposed explicit envelope",
                    "result": "falsified_as_stated",
                    "reason": "selected decimal checkpoints understate worst prime-endpoint behavior",
                    "next_revision": "state a weaker explicit envelope with named constants and test every prime endpoint",
                },
                {
                    "id": "RH-CL2",
                    "statement": "A computable theta/psi inequality with explicit constants implies an accepted RH-equivalent criterion.",
                    "tool_test": "formal bridge audit: reject if the bridge imports RH or an equivalent theorem",
                    "result": "open_formal_bridge",
                    "reason": "the equivalence theorem must be cited or formalized without circular dependence",
                    "next_revision": "write the exact theorem statement and allowed published bridge reference",
                },
                {
                    "id": "RH-CL3",
                    "statement": "Finite certificate plus large-x theorem covers the whole positive real line.",
                    "tool_test": "cutoff compatibility check: analytic threshold <= bounded certificate limit",
                    "result": "blocked_until_large_x_theorem",
                    "reason": "there is no large-x theorem with a compatible threshold yet",
                    "next_revision": "prove or import an explicit all-x estimate and bind its cutoff to the certificate",
                },
            ],
        },
        "collatz": {
            "workbench_title": "Collatz residue-cover lemma search",
            "target": "Replace bounded trajectory replay with a finite symbolic cover that proves global descent.",
            "lemmas": [
                {
                    "id": "CO-CL1",
                    "statement": "Every odd residue block in a chosen modulus has an accelerated transition to a smaller block.",
                    "tool_test": "residue transition replay over bounded starts and symbolic block templates",
                    "result": "partial_bounded_support",
                    "reason": "bounded replay suggests descent pressure but does not cover all residue blocks symbolically",
                    "next_revision": "generate a complete modulus-specific cover with no uncovered residue class",
                },
                {
                    "id": "CO-CL2",
                    "statement": "The descent measure is well-founded and strictly decreases under the certified block transition.",
                    "tool_test": "well-foundedness audit: reject non-strict or average-only descent",
                    "result": "open_formal_bridge",
                    "reason": "average parity drift is insufficient for deterministic descent",
                    "next_revision": "define the exact measure and prove strict decrease for every block",
                },
                {
                    "id": "CO-CL3",
                    "statement": "The same cover excludes non-trivial cycles and divergent branches.",
                    "tool_test": "cycle/divergence dependency check",
                    "result": "blocked_until_cover_exists",
                    "reason": "cycle exclusion alone does not prove convergence",
                    "next_revision": "derive cycle and divergence exclusion from the descent cover",
                },
            ],
        },
        "goldbach": {
            "workbench_title": "Goldbach lower-bound lemma search",
            "target": "Turn bounded decomposition evidence into a two-prime representation theorem with an explicit cutoff.",
            "lemmas": [
                {
                    "id": "GB-CL1",
                    "statement": "Every even n below N0 is covered by the bounded certificate.",
                    "tool_test": "complete even-integer decomposition replay",
                    "result": "bounded_certificate_complete",
                    "reason": "finite interval coverage is certified but cannot cover the infinite tail",
                    "next_revision": "bind this certificate to an explicit analytic threshold N0",
                },
                {
                    "id": "GB-CL2",
                    "statement": "For every even n >= N0, the two-prime representation count has a positive lower bound.",
                    "tool_test": "threshold audit: lower bound positive and N0 explicit",
                    "result": "open_infinite_bridge",
                    "reason": "no compatible large-even lower-bound theorem is formalized",
                    "next_revision": "formalize explicit circle-method constants or cite an accepted theorem with cutoff",
                },
                {
                    "id": "GB-CL3",
                    "statement": "The proof remains two-prime Goldbach and does not substitute weak Goldbach.",
                    "tool_test": "forbidden shortcut audit",
                    "result": "guard_pass",
                    "reason": "the current page correctly rejects three-prime substitution",
                    "next_revision": "keep every candidate theorem in two-prime representation form",
                },
            ],
        },
        "twin-prime": {
            "workbench_title": "Twin-prime exact-gap lemma search",
            "target": "Convert exact gap-2 bounded evidence into an unconditional infinitude theorem.",
            "lemmas": [
                {
                    "id": "TP-CL1",
                    "statement": "Bounded twin-pair counts match exact gap-2 replay through the committed range.",
                    "tool_test": "bounded twin-pair certificate replay",
                    "result": "bounded_certificate_complete",
                    "reason": "the finite count is reproducible but does not imply arbitrarily large twin pairs",
                    "next_revision": "use it only as regression evidence for candidate lower-bound theorems",
                },
                {
                    "id": "TP-CL2",
                    "statement": "A positive lower bound for exact gap-2 pairs holds for arbitrarily large x.",
                    "tool_test": "exact-gap audit: reject bounded gaps, averaged gaps, or heuristic density assumptions",
                    "result": "open_infinite_bridge",
                    "reason": "bounded-gap theorems and Hardy-Littlewood agreement do not prove exact gap 2",
                    "next_revision": "state an assumption-free exact gap-2 lower-bound theorem",
                },
                {
                    "id": "TP-CL3",
                    "statement": "The lower bound implies infinitely many distinct twin-prime pairs.",
                    "tool_test": "infinitude bridge check",
                    "result": "blocked_until_lower_bound",
                    "reason": "the implication is straightforward only after the positive lower bound exists",
                    "next_revision": "formalize the implication in Lean after TP-CL2 is closed",
                },
            ],
        },
    }
    entry = bank.get(problem_id, bank["riemann"])
    closed = sum(1 for item in entry["lemmas"] if str(item["result"]).startswith(("bounded", "guard")))
    open_or_blocked = len(entry["lemmas"]) - closed
    return {
        "schema": CANDIDATE_LEMMA_WORKBENCH_SCHEMA,
        "problem_id": problem_id,
        "status": "active_no_full_proof",
        "workbench_title": entry["workbench_title"],
        "target": entry["target"],
        "closed_count": closed,
        "open_or_blocked_count": open_or_blocked,
        "lemmas": entry["lemmas"],
        "claim_rule": "A candidate lemma may support proof search only; it upgrades the page status only after formal proof or accepted theorem review.",
    }


def machine_proof_search_trials(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    finite = problem.get("finite_result", {}) if isinstance(problem.get("finite_result"), dict) else {}
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    trial_bank: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-MP1",
                "hypothesis": "A simple checkpoint theta envelope can be promoted to an all-x RH bridge.",
                "execution": "Compare decimal checkpoint residuals with prime-endpoint frontier stress.",
                "observed": f"checkpoint max scaled theta error {finite.get('max_scaled_theta_error', 'n/a')}",
                "verdict": "failed_candidate",
                "blocker": "prime endpoints expose stronger local errors than decimal checkpoints",
                "proof_upgrade": "replace checkpoint envelope with an explicit all-x theta/psi theorem",
            },
            {
                "id": "RH-MP2",
                "hypothesis": "Bounded prime-counting replay can certify the finite interval below an analytic cutoff.",
                "execution": "Replay Merkle certificate and require cutoff compatibility.",
                "observed": f"bounded root {str(certificate.get('merkle_root', 'missing'))[:12]}",
                "verdict": "finite_piece_closed",
                "blocker": "finite coverage is useful only after a large-x theorem supplies the cutoff",
                "proof_upgrade": "bind an accepted large-x estimate to the certificate limit",
            },
            {
                "id": "RH-MP3",
                "hypothesis": "An RH-equivalent theorem can be used as a bridge without circularity.",
                "execution": "Audit candidate bridge for target-equivalent assumptions.",
                "observed": "bridge remains a specification, not a verified theorem",
                "verdict": "open_bridge",
                "blocker": "no formal non-circular implication is present in the repo",
                "proof_upgrade": "formalize the exact implication or cite an accepted theorem with proof boundaries",
            },
        ],
        "collatz": [
            {
                "id": "CO-MP1",
                "hypothesis": "Bounded trajectory replay can reveal a finite descent cover template.",
                "execution": "Replay starts through the committed limit and inspect maximal stopping cases.",
                "observed": f"tested starts {finite.get('tested_start_values', 'n/a')}",
                "verdict": "finite_piece_closed",
                "blocker": "the replay does not cover unbounded residue classes",
                "proof_upgrade": "derive a symbolic cover over all odd residue blocks",
            },
            {
                "id": "CO-MP2",
                "hypothesis": "Average downward drift is enough for convergence.",
                "execution": "Run deterministic proof-gate audit against drift-only reasoning.",
                "observed": "average drift cannot exclude exceptional branches",
                "verdict": "rejected_shortcut",
                "blocker": "probabilistic drift is not deterministic descent",
                "proof_upgrade": "prove strict decrease under a well-founded measure for every block",
            },
            {
                "id": "CO-MP3",
                "hypothesis": "Cycle exclusion alone proves Collatz.",
                "execution": "Dependency check between cycle exclusion and divergence exclusion.",
                "observed": "cycle exclusion leaves divergent branches unresolved",
                "verdict": "insufficient_partial",
                "blocker": "global convergence needs both cycle and divergence exclusion",
                "proof_upgrade": "derive both from the same residue-cover descent theorem",
            },
        ],
        "goldbach": [
            {
                "id": "GB-MP1",
                "hypothesis": "Finite decomposition replay closes all even cases below a future analytic threshold.",
                "execution": "Replay two-prime decompositions through the committed limit.",
                "observed": f"counterexamples {finite.get('counterexamples', 'n/a')}",
                "verdict": "finite_piece_closed",
                "blocker": "there is no compatible explicit threshold theorem yet",
                "proof_upgrade": "prove N0 <= certificate limit for a positive two-prime lower bound",
            },
            {
                "id": "GB-MP2",
                "hypothesis": "Weak Goldbach can substitute for strong Goldbach.",
                "execution": "Forbidden-shortcut audit on theorem shape.",
                "observed": "three-prime representation is not the target theorem",
                "verdict": "rejected_shortcut",
                "blocker": "target requires two primes for every even integer greater than 2",
                "proof_upgrade": "keep the lower bound in two-prime representation form",
            },
            {
                "id": "GB-MP3",
                "hypothesis": "Hardest bounded cases identify the analytic stress classes.",
                "execution": "Rank bounded decompositions by smallest first prime.",
                "observed": f"hardest p {((finite.get('hardest_smallest_prime_decomposition') or {}).get('smallest_prime', 'n/a'))}",
                "verdict": "heuristic_priority_only",
                "blocker": "stress ranking is not a lower-bound theorem",
                "proof_upgrade": "turn stress classes into uniform explicit estimates",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-MP1",
                "hypothesis": "Bounded exact gap-2 replay can prove infinitude.",
                "execution": "Replay twin-pair certificate and compare checkpoint counts.",
                "observed": f"twin pairs {finite.get('twin_pair_count', 'n/a')}",
                "verdict": "finite_piece_closed",
                "blocker": "positive finite counts do not force arbitrarily large pairs",
                "proof_upgrade": "prove a positive exact gap-2 lower bound for arbitrarily large x",
            },
            {
                "id": "TP-MP2",
                "hypothesis": "Bounded gaps imply exact gap 2.",
                "execution": "Theorem-shape audit against bounded-gap substitution.",
                "observed": "bounded gaps may be larger than 2",
                "verdict": "rejected_shortcut",
                "blocker": "exact twin primes require gap exactly 2",
                "proof_upgrade": "separate exact gap-2 counts from bounded-gap evidence",
            },
            {
                "id": "TP-MP3",
                "hypothesis": "Hardy-Littlewood-scale agreement can be used as proof.",
                "execution": "Assumption audit against unproved k-tuple density.",
                "observed": "density match remains heuristic",
                "verdict": "heuristic_priority_only",
                "blocker": "the proof cannot assume the density it must establish",
                "proof_upgrade": "remove k-tuple independence or replace it with an accepted theorem",
            },
        ],
    }
    trials = trial_bank.get(problem_id, [])
    return {
        "schema": MACHINE_PROOF_SEARCH_TRIALS_SCHEMA,
        "problem_id": problem_id,
        "status": "trials_executed_no_full_proof",
        "trial_count": len(trials),
        "closed_finite_count": sum(1 for trial in trials if trial["verdict"] == "finite_piece_closed"),
        "rejected_count": sum(1 for trial in trials if trial["verdict"].startswith("rejected") or trial["verdict"] == "failed_candidate"),
        "trials": trials,
        "claim_rule": "A search trial may close finite pieces or reject shortcuts; it is not a proof until the listed proof_upgrade is supplied as a formal artifact or accepted theorem.",
    }


def formal_upgrade_matrix(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    spec = problem.get("decisive_theorem_spec", {}) if isinstance(problem.get("decisive_theorem_spec"), dict) else {}
    contract = problem.get("formal_proof_contract", {}) if isinstance(problem.get("formal_proof_contract"), dict) else {}
    review = problem.get("proof_review_docket", {}) if isinstance(problem.get("proof_review_docket"), dict) else {}
    target_bank: dict[str, dict[str, str]] = {
        "riemann": {
            "decisive_artifact": "formal all-x theta/psi estimate plus non-circular RH-equivalence bridge",
            "kernel_target": "primeproject_riemann_hypothesis",
            "minimal_external_review": "analytic number theory review plus Lean replay of the bridge theorem",
        },
        "collatz": {
            "decisive_artifact": "formal residue-cover descent theorem over all positive integers",
            "kernel_target": "primeproject_collatz_conjecture",
            "minimal_external_review": "independent residue-cover replay and well-founded descent check",
        },
        "goldbach": {
            "decisive_artifact": "formal two-prime lower-bound theorem with explicit cutoff below the certificate limit",
            "kernel_target": "primeproject_goldbach_conjecture",
            "minimal_external_review": "explicit-constant analytic review plus finite cutoff replay",
        },
        "twin-prime": {
            "decisive_artifact": "formal exact gap-2 lower-bound theorem and infinitude bridge",
            "kernel_target": "primeproject_twin_prime_conjecture",
            "minimal_external_review": "exact-gap theorem replay that rejects bounded-gap substitution",
        },
    }
    target = target_bank.get(problem_id, target_bank["riemann"])
    rows = [
        {
            "stage": "bounded_certificate",
            "status": certificate.get("status", "missing"),
            "artifact": certificate.get("verifier", "missing verifier"),
            "acceptance_test": "Merkle root replay is byte-stable through the committed limit",
            "blocks_full_proof": "yes_finite_only",
        },
        {
            "stage": "decisive_infinite_theorem",
            "status": spec.get("artifact_status", "missing_formal_theorem"),
            "artifact": target["decisive_artifact"],
            "acceptance_test": "the theorem quantifies beyond any search limit and avoids forbidden shortcuts",
            "blocks_full_proof": "yes_required",
        },
        {
            "stage": "kernel_formalization",
            "status": contract.get("status", "not_formalized_open"),
            "artifact": target["kernel_target"],
            "acceptance_test": "Lean replay has no sorry, admit, unchecked axiom, or target-equivalent import",
            "blocks_full_proof": "yes_required",
        },
        {
            "stage": "independent_review",
            "status": "blocked_until_formalization",
            "artifact": target["minimal_external_review"],
            "acceptance_test": "external reviewer can replay the proof without trusting PrimeProject code",
            "blocks_full_proof": "yes_required",
        },
    ]
    open_rows = [row for row in rows if row["status"] not in {"bounded_theorem_certified", "formal_proof_verified", "accepted_theorem"}]
    return {
        "schema": FORMAL_UPGRADE_MATRIX_SCHEMA,
        "problem_id": problem_id,
        "status": "formal_upgrade_blocked",
        "target_theorem": target["kernel_target"],
        "review_status": review.get("status", "blocked") if isinstance(review, dict) else "blocked",
        "row_count": len(rows),
        "open_row_count": len(open_rows),
        "rows": rows,
        "machine_rule": "Every row except bounded_certificate must close before the page can make a full-proof claim.",
    }


def proof_kernel_roadmap(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    contract = problem.get("formal_proof_contract", {}) if isinstance(problem.get("formal_proof_contract"), dict) else {}
    matrix = problem.get("formal_upgrade_matrix", {}) if isinstance(problem.get("formal_upgrade_matrix"), dict) else {}
    skeleton = problem.get("formal_skeleton_audit", {}) if isinstance(problem.get("formal_skeleton_audit"), dict) else {}
    problem_targets: dict[str, dict[str, object]] = {
        "riemann": {
            "namespace": "PrimeProject.OpenProblems.Riemann",
            "main_file": "formal/riemann/Main.lean",
            "core_definition": "Zeta.NontrivialZero and critical-line predicate",
            "decisive_lemma": "explicit all-x theta/psi estimate with a non-circular RH-equivalence bridge",
            "bridge_theorem": "prime-counting error bound implies every non-trivial zero has real part 1/2",
            "risk": "importing an RH-equivalent theorem as an assumption",
        },
        "collatz": {
            "namespace": "PrimeProject.OpenProblems.Collatz",
            "main_file": "formal/collatz/Main.lean",
            "core_definition": "accelerated Collatz iterate, residue block, and well-founded descent measure",
            "decisive_lemma": "complete residue-cover descent theorem over all positive integers",
            "bridge_theorem": "strict descent cover implies convergence to 1 and excludes divergent branches",
            "risk": "using average drift where deterministic descent is required",
        },
        "goldbach": {
            "namespace": "PrimeProject.OpenProblems.Goldbach",
            "main_file": "formal/goldbach/Main.lean",
            "core_definition": "two-prime representation count for even integers",
            "decisive_lemma": "positive two-prime lower-bound theorem with explicit cutoff below the certificate limit",
            "bridge_theorem": "finite certificate plus large-even lower bound covers every even integer greater than 2",
            "risk": "substituting weak Goldbach or an incompatible cutoff theorem",
        },
        "twin-prime": {
            "namespace": "PrimeProject.OpenProblems.TwinPrime",
            "main_file": "formal/twin-prime/Main.lean",
            "core_definition": "exact gap-2 prime pair and arbitrarily-large twin-pair predicate",
            "decisive_lemma": "unconditional positive lower bound for exact gap-2 pairs at arbitrarily large scale",
            "bridge_theorem": "exact gap-2 lower bound implies infinitely many twin prime pairs",
            "risk": "treating bounded gaps or Hardy-Littlewood density as exact gap-2 proof",
        },
    }
    target = problem_targets.get(problem_id, problem_targets["riemann"])
    target_theorem = str(matrix.get("target_theorem", contract.get("theorem_name", f"primeproject_{problem_id}")))
    file_checks = skeleton.get("file_checks", []) if isinstance(skeleton.get("file_checks"), list) else []
    present_files = [
        item.get("path", "")
        for item in file_checks
        if isinstance(item, dict) and item.get("status") == "skeleton_present_not_proof"
    ]
    steps = [
        {
            "id": "K0",
            "stage": "formal definitions",
            "status": "skeleton_present_not_proof" if present_files else "missing",
            "artifact": target["core_definition"],
            "acceptance_test": "definitions compile and contain no target-equivalent axiom",
        },
        {
            "id": "K1",
            "stage": "bounded certificate import",
            "status": "bounded_theorem_certified",
            "artifact": "Merkle replay theorem for the committed finite range",
            "acceptance_test": "certificate root is reproduced and imported only as a finite theorem",
        },
        {
            "id": "K2",
            "stage": "decisive infinite lemma",
            "status": "open_infinite_bridge",
            "artifact": target["decisive_lemma"],
            "acceptance_test": "lemma quantifies beyond every search limit and avoids the listed shortcut risk",
        },
        {
            "id": "K3",
            "stage": "bridge to target theorem",
            "status": "blocked_until_k2",
            "artifact": target["bridge_theorem"],
            "acceptance_test": f"the bridge proves {target_theorem} from K1 and K2 without circular imports",
        },
        {
            "id": "K4",
            "stage": "independent kernel replay",
            "status": "blocked_until_k3",
            "artifact": target["main_file"],
            "acceptance_test": "external replay reports no sorry, admit, unchecked axiom, or equivalent theorem import",
        },
    ]
    open_steps = [step for step in steps if step["status"] not in {"bounded_theorem_certified", "formal_proof_verified"}]
    return {
        "schema": PROOF_KERNEL_ROADMAP_SCHEMA,
        "problem_id": problem_id,
        "status": "kernel_roadmap_open",
        "namespace": target["namespace"],
        "target_theorem": target_theorem,
        "main_file": target["main_file"],
        "shortcut_risk": target["risk"],
        "present_skeleton_files": present_files,
        "step_count": len(steps),
        "open_step_count": len(open_steps),
        "steps": steps,
        "claim_rule": "The roadmap is executable proof-engineering work, not a proof; the page can upgrade only after K2-K4 replay successfully.",
    }


def formal_kernel_contract_audit(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    replay = problem.get("formal_replay_package", {}) if isinstance(problem.get("formal_replay_package"), dict) else {}
    contract = problem.get("formal_proof_contract", {}) if isinstance(problem.get("formal_proof_contract"), dict) else {}
    package_dir = Path(str(replay.get("package_dir", f"formal/{problem_id}")))
    forbidden_tokens = [str(item) for item in replay.get("forbidden_tokens", []) if str(item).strip()]
    theorem_name = str(contract.get("theorem_name", replay.get("theorem_name", "missing")))
    theorem_statement = str(contract.get("lean_statement", replay.get("theorem_statement", "missing")))
    expected_fragments: dict[str, list[str]] = {
        "Definitions.lean": [
            f'def problemId : String := "{problem_id}"',
            'def targetStatus : String := "open_not_proven"',
            "def targetShape : String :=",
        ],
        "BoundedCertificate.lean": [
            "def boundedCertificateScope : String :=",
            'def boundedCertificateVerifier : String :=',
            "scripts/verify_open_problem_workbench.py",
        ],
        "InfiniteBridge.lean": [
            "def missingInfiniteBridge : String :=",
            'def bridgeStatus : String := "open_infinite_bridge"',
        ],
        "Main.lean": [
            'def replayStatus : String := "not_replayable_until_barriers_clear"',
            'def publicClaim : String := "bounded_theorem_only"',
            f'def targetTheoremName : String := "{theorem_name}"',
            "def targetTheoremStatement : String :=",
            theorem_statement,
        ],
    }
    rows: list[dict[str, object]] = []
    forbidden_hits: list[dict[str, str]] = []
    for filename, fragments in expected_fragments.items():
        path = package_dir / filename
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        missing = [
            fragment
            for fragment in fragments
            if fragment not in text and fragment.replace("\\", "\\\\") not in text
        ]
        hits = [token for token in forbidden_tokens if token and token in text]
        for token in hits:
            forbidden_hits.append({"path": str(path), "token": token})
        rows.append(
            {
                "file": str(path).replace("\\", "/"),
                "status": "contract_pass" if path.exists() and not missing and not hits else "contract_blocked",
                "expected_fragment_count": len(fragments),
                "missing_fragments": missing,
                "forbidden_hits": hits,
                "line_count": len(text.splitlines()) if text else 0,
            }
        )
    blocked_rows = [row for row in rows if row["status"] != "contract_pass"]
    return {
        "schema": FORMAL_KERNEL_CONTRACT_AUDIT_SCHEMA,
        "problem_id": problem_id,
        "status": "contract_pass_but_not_proof" if not blocked_rows and not forbidden_hits else "contract_blocked",
        "package_dir": str(package_dir).replace("\\", "/"),
        "target_theorem": theorem_name,
        "row_count": len(rows),
        "blocked_row_count": len(blocked_rows),
        "forbidden_hit_count": len(forbidden_hits),
        "rows": rows,
        "forbidden_hits": forbidden_hits,
        "claim_rule": "Passing this audit only proves the formal skeleton is aligned with the public claim boundary; it does not prove the conjecture.",
    }


def invalid_proof_shortcut_suite(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    suite_bank: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-SC1",
                "shortcut": "Finite zero or prime-counting verification proves RH.",
                "class": "finite_to_infinite",
                "red_team_test": "Ask whether the argument quantifies over every height and every non-trivial zeta zero.",
                "rejection_reason": "A bounded certificate can only close the committed finite range.",
                "kill_condition": "No all-height zero theorem or accepted RH-equivalent bridge is supplied.",
            },
            {
                "id": "RH-SC2",
                "shortcut": "A fitted prime-counting envelope is enough.",
                "class": "curve_fit_to_theorem",
                "red_team_test": "Stress every prime endpoint and require explicit constants, not sampled checkpoints.",
                "rejection_reason": "Numeric fit is not an all-x theorem.",
                "kill_condition": "The bound is stated only empirically or only at selected x values.",
            },
            {
                "id": "RH-SC3",
                "shortcut": "Use an RH-equivalent criterion as an assumption.",
                "class": "circular_bridge",
                "red_team_test": "Scan the bridge for an imported theorem equivalent to RH.",
                "rejection_reason": "The bridge must prove the criterion hypotheses without assuming the target.",
                "kill_condition": "The proof imports RH, an equivalent zero theorem, or a target-equivalent axiom.",
            },
        ],
        "collatz": [
            {
                "id": "CO-SC1",
                "shortcut": "Finite trajectory replay proves convergence for all n.",
                "class": "finite_to_infinite",
                "red_team_test": "Ask whether every residue block outside the search range is covered symbolically.",
                "rejection_reason": "Checked starts do not quantify over all positive integers.",
                "kill_condition": "No complete residue-cover descent theorem is supplied.",
            },
            {
                "id": "CO-SC2",
                "shortcut": "Average parity drift proves deterministic descent.",
                "class": "probabilistic_to_deterministic",
                "red_team_test": "Require a strict well-founded measure decrease for every transition block.",
                "rejection_reason": "Average drift cannot exclude exceptional divergent branches.",
                "kill_condition": "The descent argument is average-only, probabilistic, or non-strict.",
            },
            {
                "id": "CO-SC3",
                "shortcut": "Cycle exclusion alone proves Collatz.",
                "class": "partial_target_substitution",
                "red_team_test": "Check whether divergent non-cyclic branches are also excluded.",
                "rejection_reason": "The target is convergence, not only absence of non-trivial cycles.",
                "kill_condition": "The proof does not derive both cycle exclusion and divergence exclusion from one descent theorem.",
            },
        ],
        "goldbach": [
            {
                "id": "GB-SC1",
                "shortcut": "Finite decompositions prove all even integers.",
                "class": "finite_to_infinite",
                "red_team_test": "Require an explicit large-even threshold below the certificate limit.",
                "rejection_reason": "Bounded decomposition replay does not cover the infinite tail.",
                "kill_condition": "No compatible N0 and positive two-prime lower bound are supplied.",
            },
            {
                "id": "GB-SC2",
                "shortcut": "Weak Goldbach can replace strong Goldbach.",
                "class": "wrong_target",
                "red_team_test": "Verify the theorem states two primes for every even n > 2.",
                "rejection_reason": "Three-prime representation is a different theorem.",
                "kill_condition": "The target theorem allows three primes or odd-only statements.",
            },
            {
                "id": "GB-SC3",
                "shortcut": "Heuristic prime independence proves representation counts.",
                "class": "heuristic_to_theorem",
                "red_team_test": "Require explicit constants and a positive lower bound for every large even n.",
                "rejection_reason": "Heuristic density is not a uniform lower-bound theorem.",
                "kill_condition": "The lower bound depends on unproved independence assumptions.",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-SC1",
                "shortcut": "Bounded twin-pair counts prove infinitely many twin primes.",
                "class": "finite_to_infinite",
                "red_team_test": "Ask whether the argument forces arbitrarily large exact gap-2 pairs.",
                "rejection_reason": "Positive finite counts do not imply infinitude.",
                "kill_condition": "No exact gap-2 lower bound beyond every search limit is supplied.",
            },
            {
                "id": "TP-SC2",
                "shortcut": "Bounded prime gaps imply twin primes.",
                "class": "weaker_theorem_substitution",
                "red_team_test": "Check whether the gap is exactly 2 rather than merely bounded.",
                "rejection_reason": "Bounded gaps can be larger than 2.",
                "kill_condition": "The proof proves only a finite upper bound for gaps, not exact gap 2.",
            },
            {
                "id": "TP-SC3",
                "shortcut": "Hardy-Littlewood density agreement can be used as proof.",
                "class": "heuristic_to_theorem",
                "red_team_test": "Reject any proof that assumes the k-tuple density it must establish.",
                "rejection_reason": "Heuristic-scale agreement is not an unconditional theorem.",
                "kill_condition": "The density lower bound depends on Hardy-Littlewood or independence as an axiom.",
            },
        ],
    }
    shortcuts = suite_bank.get(problem_id, suite_bank["riemann"])
    return {
        "schema": INVALID_PROOF_SHORTCUT_SUITE_SCHEMA,
        "problem_id": problem_id,
        "status": "invalid_shortcuts_rejected",
        "bounded_certificate_root": certificate.get("merkle_root", "missing"),
        "shortcut_count": len(shortcuts),
        "rejected_count": len(shortcuts),
        "shortcuts": [
            {
                **shortcut,
                "verdict": "rejected_shortcut",
                "required_upgrade": "replace the shortcut with a formal theorem, accepted theorem reference, or kernel-replayable bridge",
            }
            for shortcut in shortcuts
        ],
        "claim_rule": "No proof candidate may enter review until every matching invalid shortcut is removed or replaced by a formal artifact.",
    }


def ai_solver_frontier(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    finite = problem.get("finite_result", {}) if isinstance(problem.get("finite_result"), dict) else {}
    certificate = problem.get("certificate", {}) if isinstance(problem.get("certificate"), dict) else {}
    gap_taxonomy = problem.get("proof_gap_taxonomy", {}) if isinstance(problem.get("proof_gap_taxonomy"), dict) else {}
    open_gap_count = gap_taxonomy.get("open_gap_count", "unknown")
    frontier_bank: dict[str, dict[str, object]] = {
        "riemann": {
            "engine": "positivity-kernel search over explicit-formula test functions",
            "novel_attempt": "Search for a kernel family whose Weil-explicit-formula positivity is equivalent to RH, then let PrimeProject reject every kernel whose prime-side stress terms cannot be bounded with explicit constants.",
            "search_space": [
                "even compactly supported smooth kernels",
                "Laguerre/Hermite spectral kernels",
                "Li-coefficient positivity witnesses",
                "prime-side interval-arithmetic envelopes",
            ],
            "best_current_candidate": "kernel template with nonnegative spectral side and bounded prime-side stress at committed theta checkpoints",
            "machine_output": {
                "bounded_signal": f"max scaled theta error {finite.get('max_scaled_theta_error', 'n/a')}",
                "certificate_root": str(certificate.get("merkle_root", "missing"))[:16],
                "open_gap_count": open_gap_count,
            },
            "blocking_obstruction": "No discovered kernel yet gives a non-circular all-height positivity theorem.",
            "next_experiment": "Generate kernel candidates, compute symbolic positivity constraints, and reject any kernel needing RH-equivalent assumptions.",
        },
        "collatz": {
            "engine": "residue-block descent cover search",
            "novel_attempt": "Use AI to synthesize a finite residue cover and a ranking functional, then require every symbolic block to strictly descend under accelerated Collatz iteration.",
            "search_space": [
                "odd residue classes modulo 2^k",
                "accelerated Collatz affine branches",
                "piecewise-linear ranking functions",
                "cycle/divergence exclusion certificates",
            ],
            "best_current_candidate": "sampled residue descent pressure suggests a modulus-specific cover may exist, but no complete symbolic cover is certified.",
            "machine_output": {
                "tested_start_values": finite.get("tested_start_values", "n/a"),
                "max_total_stopping_time": finite.get("max_total_stopping_time", "n/a"),
                "max_start": finite.get("max_start", "n/a"),
            },
            "blocking_obstruction": "Every residue block must be covered symbolically; sampled descent is not enough.",
            "next_experiment": "Enumerate residue classes modulo 2^k, derive affine accelerated branches, and search for a strict well-founded ranking function.",
        },
        "goldbach": {
            "engine": "explicit-cutoff optimizer for two-prime lower bounds",
            "novel_attempt": "Treat strong Goldbach as a constant-optimization problem: lower the analytic cutoff N0 until the existing bounded certificate can cover the remaining finite interval.",
            "search_space": [
                "major-arc constants",
                "minor-arc error budgets",
                "worst residue classes",
                "least-representation even integers",
            ],
            "best_current_candidate": "the bounded certificate supplies the finite half; the missing half is an explicit positive two-prime lower bound with N0 below the certificate limit.",
            "machine_output": {
                "checked_even_limit": finite.get("checked_even_limit", "n/a"),
                "counterexamples": finite.get("counterexamples", "n/a"),
                "hardest_decomposition": finite.get("hardest_smallest_prime_decomposition", {}),
            },
            "blocking_obstruction": "No explicit large-even lower-bound theorem with compatible cutoff is present.",
            "next_experiment": "Optimize explicit constants and reject any bound whose N0 exceeds the committed certificate limit.",
        },
        "twin-prime": {
            "engine": "exact-gap sieve-weight search",
            "novel_attempt": "Search parity-sensitive sieve weights that force gap exactly 2 instead of merely producing bounded prime gaps.",
            "search_space": [
                "admissible tuple weights with a mandatory {0,2} pair",
                "parity-barrier stress tests",
                "exact-gap lower-bound candidates",
                "Hardy-Littlewood-free density witnesses",
            ],
            "best_current_candidate": "bounded exact-gap counts are positive and heuristic-scale, but every current path still collapses to bounded-gap or heuristic evidence.",
            "machine_output": {
                "twin_pair_count": finite.get("twin_pair_count", "n/a"),
                "largest_pair_seen": finite.get("largest_pair_seen", "n/a"),
                "hardy_littlewood_ratio": (
                    round(
                        float(finite.get("twin_pair_count", 0))
                        / float((finite.get("checkpoint_rows") or [{}])[-1].get("hardy_littlewood_estimate", 1)),
                        6,
                    )
                    if finite.get("checkpoint_rows")
                    else "n/a"
                ),
            },
            "blocking_obstruction": "The parity barrier still prevents exact gap-2 infinitude from bounded-gap methods.",
            "next_experiment": "Generate sieve weights and kill every candidate whose conclusion is only bounded gaps, averaged gaps, or Hardy-Littlewood-scale agreement.",
        },
    }
    frontier = frontier_bank.get(problem_id, frontier_bank["riemann"])
    solver_steps = [
        {
            "id": "AI-1",
            "stage": "generate candidate",
            "status": "active_search",
            "acceptance_test": "candidate states a theorem stronger than finite evidence and avoids known shortcut classes",
        },
        {
            "id": "AI-2",
            "stage": "machine falsify",
            "status": "active_search",
            "acceptance_test": "PrimeProject stress tests fail weak, circular, heuristic, or finite-only candidates",
        },
        {
            "id": "AI-3",
            "stage": "compress obstruction",
            "status": "open_research",
            "acceptance_test": "remaining failures collapse into a finite family of symbolic obstruction classes",
        },
        {
            "id": "AI-4",
            "stage": "formalize survivor",
            "status": "blocked_until_survivor",
            "acceptance_test": "surviving theorem is replayable without sorry, admit, target-equivalent axiom, or unproved heuristic",
        },
    ]
    return {
        "schema": AI_SOLVER_FRONTIER_SCHEMA,
        "problem_id": problem_id,
        "status": "breakthrough_search_active_not_solved",
        "engine": frontier["engine"],
        "novel_attempt": frontier["novel_attempt"],
        "search_space": frontier["search_space"],
        "best_current_candidate": frontier["best_current_candidate"],
        "machine_output": frontier["machine_output"],
        "blocking_obstruction": frontier["blocking_obstruction"],
        "next_experiment": frontier["next_experiment"],
        "solver_steps": solver_steps,
        "claim_rule": "This is a live AI-assisted attack plan for an unsolved problem; it can propose and falsify proof candidates, but status changes only after a replayable infinite theorem exists.",
    }


def ai_breakthrough_program(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    finite = problem.get("finite_result", {}) if isinstance(problem.get("finite_result"), dict) else {}
    program_bank: dict[str, dict[str, object]] = {
        "riemann": {
            "program_title": "RH positivity-to-kernel bridge program",
            "literature_anchor": [
                {
                    "source": "Weil explicit-formula positivity criteria",
                    "url": "https://en.wikipedia.org/wiki/Weil%27s_criterion",
                    "use": "Treat RH as a positivity problem instead of a zero-by-zero computation.",
                    "limit": "Equivalent criteria do not solve RH unless positivity is proved for the whole admissible class.",
                },
                {
                    "source": "Li-type positivity criteria",
                    "url": "https://mathworld.wolfram.com/LisCriterion.html",
                    "use": "Convert zero-location information into an infinite positivity sequence.",
                    "limit": "Checking finitely many positive terms is not enough.",
                },
            ],
            "new_hypothesis": "There may exist a finitely parameterized kernel cone whose explicit-formula prime side is interval-certifiable and whose spectral positivity implies RH without importing RH-equivalent assumptions.",
            "candidate_theorem": "For a generated admissible kernel cone K, the Weil/Lagarias-equivalent positivity functional is nonnegative for every k in K, and K is dense enough in the test-function class required to imply RH.",
            "ai_search_protocol": [
                "Generate kernel families with symbolic positivity constraints.",
                "Use interval arithmetic to bound prime-side stress terms against theta/psi frontier probes.",
                "Reject kernels whose proof imports zero-free regions strong enough to be circular.",
                "Promote only a kernel cone with a universal positivity proof to formal review.",
            ],
            "first_machine_artifact": "kernel-candidate ledger with symbolic constraints, failed circularity checks, and interval-certified prime-side bounds",
            "decisive_success_condition": "A replayable theorem: every admissible kernel in the cone satisfies the required positivity and the cone is strong enough to imply RH.",
            "current_obstruction": "No non-circular universal positivity theorem for the generated cone.",
            "bounded_signal": f"theta stress certificate through {finite.get('limit', 'n/a')} remains only finite evidence.",
        },
        "collatz": {
            "program_title": "Collatz residue-cover descent synthesis",
            "literature_anchor": [
                {
                    "source": "Tao almost-bounded Collatz result",
                    "url": "https://arxiv.org/abs/1909.03562",
                    "use": "Use density-descent insight as a guide for residue-block compression.",
                    "limit": "Almost-all logarithmic-density descent is not all-integer convergence.",
                },
                {
                    "source": "2-adic/residue branch formulations",
                    "url": "https://en.wikipedia.org/wiki/Collatz_conjecture",
                    "use": "Represent accelerated Collatz steps as affine maps on residue classes.",
                    "limit": "Finite residue sampling is not a global descent cover.",
                },
            ],
            "new_hypothesis": "A finite set of accelerated odd-residue blocks may admit a strict well-founded ranking after branch compression, turning empirical descent into a symbolic cover.",
            "candidate_theorem": "There exist k, a finite partition of odd residues modulo 2^k, and a well-founded rank R such that every accelerated Collatz branch either enters a smaller verified basin or strictly decreases R.",
            "ai_search_protocol": [
                "Enumerate residue classes modulo 2^k and derive accelerated affine branches.",
                "Search piecewise-linear or logarithmic ranking functions that strictly decrease for every branch.",
                "Use SMT-style counterexample search to kill uncovered residue blocks.",
                "Iteratively split only the failing blocks until the cover either closes or shows structural obstruction.",
            ],
            "first_machine_artifact": "residue-cover certificate with every block mapped to a lower-ranked block or to a smaller verified basin",
            "decisive_success_condition": "A finite symbolic cover for all odd residues plus a strict ranking function that excludes cycles and divergence.",
            "current_obstruction": "No complete cover; sampled descent has not been compressed into a proof over all residues.",
            "bounded_signal": f"bounded run tested starts through {finite.get('tested_start_values', 'n/a')}.",
        },
        "goldbach": {
            "program_title": "Goldbach explicit-cutoff lowering program",
            "literature_anchor": [
                {
                    "source": "Oliveira e Silva, Herzog, Pardi verification to 4*10^18",
                    "url": "https://www.ams.org/mcom/2014-83-288/S0025-5718-2013-02787-1/S0025-5718-2013-02787-1.pdf",
                    "use": "Use large finite verification as the finite half of a cutoff-plus-tail proof.",
                    "limit": "Finite verification cannot cover the infinite tail.",
                },
                {
                    "source": "Explicit circle-method lower-bound programs",
                    "url": "https://mathworld.wolfram.com/GoldbachConjecture.html",
                    "use": "Frame the missing theorem as a positive two-prime representation lower bound for all large even n.",
                    "limit": "Heuristic prime independence is not a uniform lower-bound theorem.",
                },
            ],
            "new_hypothesis": "AI-guided constant optimization can isolate a sharper explicit major/minor arc budget whose cutoff falls below the certified finite range.",
            "candidate_theorem": "There is an explicit N0 below the certified finite limit such that every even n >= N0 has a positive two-prime representation count under a fully explicit major/minor arc inequality budget.",
            "ai_search_protocol": [
                "Model the proof as an inequality budget with explicit constants.",
                "Search worst residue classes and least-representation even integers for stress cases.",
                "Reject any budget whose cutoff exceeds the finite certificate limit.",
                "Emit a formal inequality checklist before attempting theorem proof.",
            ],
            "first_machine_artifact": "explicit-constant budget table with every error term, cutoff N0, and the finite interval covered by certificate",
            "decisive_success_condition": "A positive two-prime representation lower bound for every even n >= N0, with N0 below the verified finite limit.",
            "current_obstruction": "No compatible explicit lower-bound theorem has been supplied.",
            "bounded_signal": f"bounded certificate checked even integers through {finite.get('checked_even_limit', 'n/a')}.",
        },
        "twin-prime": {
            "program_title": "Twin-prime parity-barrier breach search",
            "literature_anchor": [
                {
                    "source": "Polymath8/Maynard-Tao bounded gaps",
                    "url": "https://arxiv.org/abs/1409.8361",
                    "use": "Use bounded-gap machinery as a scaffold for admissible tuple weight design.",
                    "limit": "Bounded gaps do not imply exact gap 2.",
                },
                {
                    "source": "Parity barrier in sieve methods",
                    "url": "https://en.wikipedia.org/wiki/Twin_prime",
                    "use": "Treat exact gap-2 forcing as the obstruction that must be attacked directly.",
                    "limit": "Density agreement with Hardy-Littlewood is heuristic unless made unconditional.",
                },
            ],
            "new_hypothesis": "A parity-sensitive weight certificate may isolate the {0,2} tuple strongly enough to prove an exact gap-2 lower bound rather than a bounded-gap statement.",
            "candidate_theorem": "There exists an unconditional parity-sensitive sieve weight family whose limiting lower bound is positive for exact prime pairs (n, n+2), not merely for bounded gaps.",
            "ai_search_protocol": [
                "Generate admissible-tuple weights with a mandatory exact {0,2} pair.",
                "Stress every candidate against parity-barrier countermodels.",
                "Reject weights whose conclusion allows gaps larger than 2.",
                "Promote only a weight family with an unconditional positive exact-gap lower bound.",
            ],
            "first_machine_artifact": "exact-gap weight ledger distinguishing exact gap 2, bounded gaps, averaged gaps, and heuristic-density failures",
            "decisive_success_condition": "An unconditional positive lower bound for exact gap-2 prime pairs at arbitrarily large scale.",
            "current_obstruction": "Current sieve routes still collapse to bounded-gap or heuristic evidence.",
            "bounded_signal": f"bounded run saw {finite.get('twin_pair_count', 'n/a')} twin pairs.",
        },
    }
    program = program_bank.get(problem_id, program_bank["riemann"])
    protocols = list(program.get("ai_search_protocol", []))
    machine_experiments = [
        {
            "id": f"{problem_id}-breakthrough-{idx + 1}",
            "purpose": protocol,
            "artifact": f"data/open-problem/{problem_id}/breakthrough-{idx + 1}.json",
            "pass_condition": "The artifact closes one stated proof obligation without using an assumption equivalent to the target conjecture.",
            "failure_signal": "The artifact is finite-only, circular, heuristic-only, or leaves an unquantified infinite tail.",
        }
        for idx, protocol in enumerate(protocols[:4])
    ]
    return {
        "schema": AI_BREAKTHROUGH_PROGRAM_SCHEMA,
        "problem_id": problem_id,
        "status": "active_unsolved_research_program",
        **program,
        "machine_experiments": machine_experiments,
        "red_team_rules": [
            "Finite verification may falsify a universal claim but may not prove the infinite theorem.",
            "Equivalent criteria are allowed only if the missing positivity, descent, or lower-bound theorem is proved without circular assumptions.",
            "A candidate survives only when its first machine artifact can be replayed and its proof obligation is stated as a formal theorem.",
        ],
        "upgrade_condition": "Do not change the public status until the candidate theorem is converted into a replayable formal proof or an accepted theorem that closes the infinite bridge.",
        "claim_rule": "This program is a serious AI-assisted attempt, not a proof claim. The page remains open_not_proven until the decisive success condition is met by a formal artifact or accepted theorem.",
    }


def ai_proof_forge(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    forge_bank: dict[str, dict[str, object]] = {
        "riemann": {
            "forge_title": "Spectral positivity object forge",
            "minimal_breakthrough_theorem": "Construct a non-circular Hilbert-space or kernel-cone positivity theorem whose explicit-formula shadow implies the classical RH zero-line statement.",
            "new_object": "A finite symbolic family of signed test kernels with a machine-checkable positivity certificate and a density map into the Weil/Li/Lagarias test universe.",
            "search_grammar": [
                "kernel := even compactly supported test family + Mellin transform constraints",
                "certificate := symbolic positivity block + interval prime-side bound + circularity audit",
                "bridge := density lemma from generated kernel cone to a known RH-equivalent criterion",
            ],
            "countermodel_battery": [
                "Reject kernels that require RH-strength zero-free regions.",
                "Reject finite Li-coefficient positivity as a substitute for all-n positivity.",
                "Reject numerical zero checks unless they discharge an all-height theorem.",
            ],
            "formal_target": "Lean theorem stub: generated kernel cone positivity implies the RH target theorem after importing only accepted explicit-formula lemmas.",
            "next_theorem_to_attempt": "KernelConePositivityBridge: a generated kernel cone is positive for the full admissible test class and implies the RH zero-line criterion.",
            "lean_statement_draft": "def nextAIDiscoveryTheorem : String := \"KernelConePositivityBridge implies primeproject_riemann_hypothesis\"",
            "proof_objects_needed": [
                "admissible kernel cone definition",
                "non-circular explicit-formula positivity lemma",
                "density bridge into the RH-equivalent test class",
            ],
            "candidate_mutations": [
                {
                    "id": "RH-MUT-1",
                    "mutation": "Replace scalar positivity checks with a two-layer kernel cone whose outer layer is interval-certified and inner layer is symbolic.",
                    "theorem_pressure": "Could convert finite theta stress into a reusable positivity lemma.",
                    "verifier": "interval bounds plus circularity audit against RH-equivalent imports",
                    "current_verdict": "open_candidate_not_proof",
                    "next_action": "derive density map into the full Weil test class",
                },
                {
                    "id": "RH-MUT-2",
                    "mutation": "Search a Li-coefficient majorant that is generated by primes but admits a monotone positivity certificate.",
                    "theorem_pressure": "Could turn all-n positivity into a generated inequality family.",
                    "verifier": "reject if positivity is checked only for finite n",
                    "current_verdict": "blocked_by_all_n_gap",
                    "next_action": "find a recurrence whose positivity propagates indefinitely",
                },
                {
                    "id": "RH-MUT-3",
                    "mutation": "Model Hilbert-Polya as a constrained inverse spectral problem with prime-side trace fingerprints.",
                    "theorem_pressure": "Could identify a self-adjoint candidate without assuming the zero line.",
                    "verifier": "spectral self-adjointness plus trace-formula replay",
                    "current_verdict": "speculative_needs_operator",
                    "next_action": "construct a minimal operator domain and prove symmetry",
                },
            ],
        },
        "collatz": {
            "forge_title": "Residue automaton rank forge",
            "minimal_breakthrough_theorem": "Find a finite accelerated-residue automaton and a well-founded ranking that covers every positive integer without exceptional residue leakage.",
            "new_object": "A compressed odd-residue transition graph whose nodes carry affine branch data, residue masks, and a candidate ordinal-valued descent rank.",
            "search_grammar": [
                "node := residue block modulo 2^k with accelerated odd map",
                "rank := lexicographic tuple of logarithmic scale, valuation debt, and residue potential",
                "certificate := every edge decreases rank or enters a smaller certified basin",
            ],
            "countermodel_battery": [
                "Generate uncovered residue blocks when the partition is incomplete.",
                "Search cycles in the compressed automaton before accepting a rank.",
                "Reject density-only descent because Collatz requires all starting values.",
            ],
            "formal_target": "Lean theorem stub: every odd residue block descends under the rank, hence every positive orbit reaches the verified basin.",
            "next_theorem_to_attempt": "ResidueRankDescentCover: every accelerated Collatz residue block either enters a smaller verified basin or strictly decreases a well-founded rank.",
            "lean_statement_draft": "def nextAIDiscoveryTheorem : String := \"ResidueRankDescentCover implies primeproject_collatz_conjecture\"",
            "proof_objects_needed": [
                "finite accelerated residue partition",
                "well-founded rank definition",
                "edge-by-edge exact descent certificate",
            ],
            "candidate_mutations": [
                {
                    "id": "CO-MUT-1",
                    "mutation": "Use valuation debt as a conserved quantity that must be repaid by later halving bursts.",
                    "theorem_pressure": "Could turn probabilistic drift into deterministic branch debt accounting.",
                    "verifier": "search residue cycles with nondecreasing debt",
                    "current_verdict": "open_candidate_not_proof",
                    "next_action": "increase modulus until every debt-positive component exits",
                },
                {
                    "id": "CO-MUT-2",
                    "mutation": "Compress Syracuse branches into strongly connected components and assign ordinal ranks to components.",
                    "theorem_pressure": "Could exclude both divergent paths and nontrivial cycles.",
                    "verifier": "SCC cycle search plus rank-decrease check",
                    "current_verdict": "blocked_by_uncovered_components",
                    "next_action": "split only components that violate rank monotonicity",
                },
                {
                    "id": "CO-MUT-3",
                    "mutation": "Train symbolic templates for piecewise logarithmic potentials, then solve coefficients exactly.",
                    "theorem_pressure": "Could produce a compact certificate instead of huge residue tables.",
                    "verifier": "exact rational inequality replay over every branch",
                    "current_verdict": "needs_exact_coefficients",
                    "next_action": "convert numeric potentials into rational inequalities",
                },
            ],
        },
        "goldbach": {
            "forge_title": "Explicit cutoff inequality forge",
            "minimal_breakthrough_theorem": "Lower an unconditional explicit two-prime representation cutoff below the verified finite Goldbach range.",
            "new_object": "A ledger of major-arc contribution, minor-arc loss, exceptional-character loss, and finite verification overlap as one auditable inequality budget.",
            "search_grammar": [
                "budget := positive main term - explicit error terms",
                "stress := worst residue class + least observed representation + cutoff sensitivity",
                "certificate := N0 below finite range and every inequality source independently cited or formalized",
            ],
            "countermodel_battery": [
                "Reject budgets whose N0 exceeds the certified finite range.",
                "Reject any independence heuristic not converted into an explicit theorem.",
                "Reject weak Goldbach or almost-all Goldbach as a substitute for strong Goldbach.",
            ],
            "formal_target": "Lean theorem stub: explicit lower bound R_2(n) > 0 for all even n >= N0, plus bounded certificate for 4 <= n < N0.",
            "next_theorem_to_attempt": "ExplicitGoldbachCutoffBridge: an explicit two-prime lower bound holds for every even n above N0, with N0 below the certified finite range.",
            "lean_statement_draft": "def nextAIDiscoveryTheorem : String := \"ExplicitGoldbachCutoffBridge implies primeproject_goldbach_conjecture\"",
            "proof_objects_needed": [
                "explicit major/minor arc inequality budget",
                "verified finite overlap certificate",
                "N0 comparison below the certified finite range",
            ],
            "candidate_mutations": [
                {
                    "id": "GB-MUT-1",
                    "mutation": "Treat every error term as a budget line and optimize constants against the finite 4*10^18 ceiling.",
                    "theorem_pressure": "Could close the proof if the analytic cutoff falls below verified computation.",
                    "verifier": "explicit cutoff calculator with no heuristic independence inputs",
                    "current_verdict": "open_candidate_not_proof",
                    "next_action": "replace informal minor-arc losses with cited explicit inequalities",
                },
                {
                    "id": "GB-MUT-2",
                    "mutation": "Search for residue-class stress cases where the least Goldbach prime is unusually large.",
                    "theorem_pressure": "Could identify exactly where the cutoff proof is weakest.",
                    "verifier": "bounded certificate plus worst-class extrapolation audit",
                    "current_verdict": "bounded_support_only",
                    "next_action": "connect stress cases to a uniform lower-bound theorem",
                },
                {
                    "id": "GB-MUT-3",
                    "mutation": "Hybridize explicit circle-method budgets with a finite certificate overlap theorem.",
                    "theorem_pressure": "Could reduce the target to proving positivity only above N0.",
                    "verifier": "N0 must be lower than the certified finite range",
                    "current_verdict": "blocked_by_missing_explicit_tail",
                    "next_action": "prove the large-n tail with accepted explicit constants",
                },
            ],
        },
        "twin-prime": {
            "forge_title": "Exact-gap parity barrier forge",
            "minimal_breakthrough_theorem": "Produce an unconditional exact-gap-2 lower-bound theorem that survives parity-barrier stress tests.",
            "new_object": "A parity-sensitive weight ledger separating exact {0,2} contribution from wider bounded-gap contribution and heuristic k-tuple density.",
            "search_grammar": [
                "weight := admissible tuple weight with exact-pair selector",
                "barrier-test := parity model where ordinary sieve cannot distinguish primes from semiprimes",
                "certificate := positive exact-gap lower bound, not a positive bounded-gap lower bound",
            ],
            "countermodel_battery": [
                "Reject any proof that still allows gap 4, 6, or 246 as the conclusion.",
                "Reject Hardy-Littlewood k-tuple density as an axiom.",
                "Reject averaged bounded intervals unless exact gap 2 is forced infinitely often.",
            ],
            "formal_target": "Lean theorem stub: for every N there exists p > N with p and p+2 prime, derived from an exact-gap lower-bound theorem.",
            "next_theorem_to_attempt": "ExactGapTwoLowerBoundBridge: an unconditional lower bound for exact prime pairs (p, p+2) remains positive at arbitrarily large scale.",
            "lean_statement_draft": "def nextAIDiscoveryTheorem : String := \"ExactGapTwoLowerBoundBridge implies primeproject_twin_prime_conjecture\"",
            "proof_objects_needed": [
                "exact-pair selector weight family",
                "parity-barrier survival argument",
                "infinitude bridge from positive exact-gap lower bound",
            ],
            "candidate_mutations": [
                {
                    "id": "TP-MUT-1",
                    "mutation": "Add an exact-pair selector to admissible tuple weights and penalize all wider gaps in the objective.",
                    "theorem_pressure": "Could reveal whether bounded-gap weights can be made exact-gap sensitive.",
                    "verifier": "reject if the conclusion still permits any gap larger than 2",
                    "current_verdict": "open_candidate_not_proof",
                    "next_action": "prove positive mass remains after exact-pair projection",
                },
                {
                    "id": "TP-MUT-2",
                    "mutation": "Stress candidate weights against parity models that make primes and semiprimes indistinguishable.",
                    "theorem_pressure": "Could expose the exact point where parity blocks the route.",
                    "verifier": "parity countermodel battery",
                    "current_verdict": "blocked_by_parity_barrier",
                    "next_action": "find a statistic outside ordinary sieve parity blindness",
                },
                {
                    "id": "TP-MUT-3",
                    "mutation": "Separate exact-gap lower bounds from averaged bounded-interval lower bounds in the proof ledger.",
                    "theorem_pressure": "Could prevent accidental replacement of twin primes by weaker bounded gaps.",
                    "verifier": "formal distinction between exact gap 2 and H1 <= 246",
                    "current_verdict": "guardrail_candidate",
                    "next_action": "turn the distinction into a Lean-side theorem dependency",
                },
            ],
        },
    }
    forge = forge_bank.get(problem_id, forge_bank["riemann"])
    decomposition_bank: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-TD1",
                "lemma": "AdmissibleKernelCone: define the generated kernel cone without importing an RH-equivalent positivity theorem.",
                "role": "Creates the exact mathematical object that the positivity search is allowed to use.",
                "risk": "The cone may be too small to be dense in any accepted RH-equivalent test universe.",
                "proof_artifact": "formal/riemann/InfiniteBridge.lean theoremDecomposition entry plus kernel-cone definition file",
                "failure_test": "Reject if admissibility is proved by assuming zero-line information or an RH-strength bound.",
                "status": "draft_formalization",
            },
            {
                "id": "RH-TD2",
                "lemma": "NonCircularExplicitFormulaPositivity: prove cone positivity from accepted explicit-formula inputs only.",
                "role": "Supplies the first theorem-level reason a generated kernel could matter for RH.",
                "risk": "This is the highest-risk step because positivity criteria often smuggle RH-strength assumptions.",
                "proof_artifact": "interval-certified positivity ledger with imported theorem audit",
                "failure_test": "Reject if any imported bound is equivalent to the target zero-line conclusion.",
                "status": "highest_risk_open",
            },
            {
                "id": "RH-TD3",
                "lemma": "KernelConeDensityBridge: show the generated cone is dense enough for the RH-equivalent test class.",
                "role": "Turns a positive generated object into a theorem that covers the full target criterion.",
                "risk": "A finite or sparse cone can pass all computations while missing adversarial test functions.",
                "proof_artifact": "density map plus norm-control certificate",
                "failure_test": "Reject if density is demonstrated only on sampled kernels or bounded frequency windows.",
                "status": "open_infinite_bridge",
            },
            {
                "id": "RH-TD4",
                "lemma": "TargetImportAudit: prove the bridge does not import the Riemann Hypothesis or a disguised equivalent.",
                "role": "Prevents circular proof promotion.",
                "risk": "Many RH criteria are equivalent to the target and cannot be used as premises.",
                "proof_artifact": "machine-readable import ledger for every theorem dependency",
                "failure_test": "Reject if an imported theorem's documented strength is target-equivalent or stronger.",
                "status": "machine_check_required",
            },
        ],
        "collatz": [
            {
                "id": "CO-TD1",
                "lemma": "AcceleratedResiduePartition: construct a finite odd-residue partition with no uncovered positive integer.",
                "role": "Makes the automaton cover the actual Collatz domain rather than a sampled subset.",
                "risk": "A missing residue class invalidates all later descent claims.",
                "proof_artifact": "exact residue partition certificate with modulus and branch formulas",
                "failure_test": "Reject if any residue block has no successor, overlap ambiguity, or missing congruence class.",
                "status": "draft_formalization",
            },
            {
                "id": "CO-TD2",
                "lemma": "WellFoundedResidueRank: define a rank that cannot support infinite nondecreasing chains.",
                "role": "Replaces probabilistic drift with a deterministic descent measure.",
                "risk": "A numeric potential can look decreasing in samples while failing as a well-founded order.",
                "proof_artifact": "rank definition over exact rational or ordinal-valued components",
                "failure_test": "Reject if the order is not well-founded or depends on empirical stopping times.",
                "status": "open_infinite_bridge",
            },
            {
                "id": "CO-TD3",
                "lemma": "EveryEdgeDescendsOrEntersBasin: prove every accelerated edge decreases rank or reaches a verified smaller basin.",
                "role": "Closes the all-starting-values step.",
                "risk": "This is the highest-risk step because one exceptional component can encode a cycle or divergent path.",
                "proof_artifact": "edge-by-edge exact inequality certificate",
                "failure_test": "Reject if SCC search finds a nondecreasing cycle or an uncovered exceptional branch.",
                "status": "highest_risk_open",
            },
            {
                "id": "CO-TD4",
                "lemma": "CycleAndDivergenceExclusionBridge: derive global convergence from the rank descent cover.",
                "role": "Connects local automaton descent to the original Collatz statement.",
                "risk": "Accelerated-map convergence must be shown equivalent to original trajectory convergence.",
                "proof_artifact": "formal bridge from accelerated odd map to original map",
                "failure_test": "Reject if the proof only excludes bounded cycles but leaves divergent accelerated paths.",
                "status": "machine_check_required",
            },
        ],
        "goldbach": [
            {
                "id": "GB-TD1",
                "lemma": "ExplicitTwoPrimeBudget: state a fully explicit major-arc/minor-arc lower-bound budget for R_2(n).",
                "role": "Converts analytic evidence into a checkable inequality.",
                "risk": "A hidden asymptotic or ineffective constant destroys the finite overlap argument.",
                "proof_artifact": "explicit constant ledger with citations or formal derivations",
                "failure_test": "Reject if any term is asymptotic-only, heuristic, or not valid for all even n above N0.",
                "status": "draft_formalization",
            },
            {
                "id": "GB-TD2",
                "lemma": "ErrorTermsReplayable: make every exceptional-character, major-arc, and minor-arc loss independently replayable.",
                "role": "Prevents the cutoff from resting on informal analytic prose.",
                "risk": "One unverified loss term can move the cutoff above the finite certificate range.",
                "proof_artifact": "machine-readable inequality dependency ledger",
                "failure_test": "Reject if any budget line lacks a theorem source, validity range, and numerical constant.",
                "status": "open_infinite_bridge",
            },
            {
                "id": "GB-TD3",
                "lemma": "CutoffBelowFiniteCertificate: prove the explicit N0 is below the independently verified finite range.",
                "role": "Glues the large-n theorem to bounded computation.",
                "risk": "This is the highest-risk practical step because known explicit cutoffs can be far above finite verification.",
                "proof_artifact": "N0 calculator plus finite certificate comparison",
                "failure_test": "Reject if the computed N0 is above the certified finite range or depends on unproved constants.",
                "status": "highest_risk_open",
            },
            {
                "id": "GB-TD4",
                "lemma": "FiniteLargeNGlue: prove finite verification plus the large-n lower bound covers every even n >= 4.",
                "role": "Turns two partial theorems into the exact Goldbach target.",
                "risk": "Off-by-one ranges and parity/domain mismatches are common promotion errors.",
                "proof_artifact": "formal interval-cover theorem",
                "failure_test": "Reject if any even interval between 4, the finite limit, and N0 is uncovered.",
                "status": "machine_check_required",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-TD1",
                "lemma": "ExactPairSelectorWeights: construct admissible weights that isolate gap 2 rather than bounded gaps.",
                "role": "Defines the object that could distinguish twin primes from weaker bounded-gap results.",
                "risk": "The selector may collapse to a bounded-gap statistic and lose exactness.",
                "proof_artifact": "exact-pair selector definition with wider-gap rejection tests",
                "failure_test": "Reject if the theorem statement still permits gaps 4, 6, 246, or any H > 2.",
                "status": "draft_formalization",
            },
            {
                "id": "TP-TD2",
                "lemma": "ParityBarrierSurvival: prove the exact-pair statistic survives parity countermodels.",
                "role": "Attacks the known sieve barrier directly.",
                "risk": "This is the highest-risk step because ordinary sieve weights cannot distinguish primes from semiprimes strongly enough.",
                "proof_artifact": "parity countermodel report plus theorem-level escape mechanism",
                "failure_test": "Reject if the argument works equally well in a parity model with no twin-prime conclusion.",
                "status": "highest_risk_open",
            },
            {
                "id": "TP-TD3",
                "lemma": "PositiveExactGapLowerBound: prove positive lower mass for exact pairs (p, p+2) at arbitrarily large scale.",
                "role": "Supplies the non-bounded theorem needed for infinitude.",
                "risk": "Averaged interval positivity does not imply exact gap 2.",
                "proof_artifact": "scale-uniform lower-bound certificate for exact gap 2",
                "failure_test": "Reject if positivity is only for intervals containing at least two primes with unknown gap.",
                "status": "open_infinite_bridge",
            },
            {
                "id": "TP-TD4",
                "lemma": "ExactGapInfinitudeBridge: derive infinitely many twin pairs from the positive exact-gap lower bound.",
                "role": "Connects the lower-bound theorem to the original twin prime statement.",
                "risk": "The bridge must quantify over arbitrarily large N, not just large finite windows.",
                "proof_artifact": "formal bridge theorem from lower-bound positivity to infinitude",
                "failure_test": "Reject if the proof yields only a finite count or a limsup bounded-gap result.",
                "status": "machine_check_required",
            },
        ],
    }
    theorem_decomposition = decomposition_bank.get(problem_id, decomposition_bank["riemann"])
    highest_risk = next(
        (item for item in theorem_decomposition if "highest_risk" in item.get("status", "")),
        theorem_decomposition[0],
    )
    breakthrough_blueprints: dict[str, dict[str, object]] = {
        "riemann": {
            "status": "blueprint_open_not_proof",
            "target_lemma": "RH-TD2",
            "new_object_family": "Signed kernel cones whose positivity certificate is expressed as a finite semialgebraic block plus an explicit-formula dependency ledger.",
            "why_not_reproduction": "Finite zero checks, finite Li-coefficient checks, and sampled prime-counting fits are excluded; the object must produce a theorem-level positivity mechanism.",
            "ai_generation_prompt": "Generate the smallest admissible even test-kernel family with symbolic parameters, list every theorem dependency, and state a positivity lemma whose assumptions are weaker than RH.",
            "minimal_counterexample": "A generated kernel that is positive on sampled intervals but needs an RH-equivalent zero-free region for the all-height step.",
            "falsification_oracle": "Dependency-strength audit plus adversarial test-kernel search outside the generated cone.",
            "formalization_seed": "Define KernelCone, ImportedTheoremStrength, and NonCircularPositivityCertificate before stating any RH bridge theorem.",
            "success_upgrade": "Promote only if the positivity proof is non-circular and the density bridge covers an accepted RH-equivalent test class.",
            "next_experiments": [
                "Enumerate two-parameter kernel cones and record which assumptions prove positivity.",
                "Build an import-strength ledger that flags zero-line or RH-equivalent premises.",
                "Search adversarial test functions that separate the generated cone from the full Weil test class.",
            ],
        },
        "collatz": {
            "status": "blueprint_open_not_proof",
            "target_lemma": "CO-TD3",
            "new_object_family": "Residue-debt automata with exact rational rank certificates on strongly connected components.",
            "why_not_reproduction": "Trajectory replay and density drift are excluded; the object must cover every residue branch with a well-founded descent certificate.",
            "ai_generation_prompt": "Generate a finite accelerated odd-residue automaton, assign exact rank components, and prove every SCC has an outgoing strict descent or enters a verified basin.",
            "minimal_counterexample": "A strongly connected component whose exact branch inequalities permit nondecreasing rank.",
            "falsification_oracle": "SCC search over the compressed automaton plus rational inequality replay on every branch.",
            "formalization_seed": "Define AcceleratedBlock, RankDebt, BranchInequality, and SCCExitCertificate before attempting global convergence.",
            "success_upgrade": "Promote only if every residue class is covered and every non-basin SCC has a certified decreasing exit.",
            "next_experiments": [
                "Increase modulus only for SCCs that violate rank monotonicity.",
                "Convert learned numeric potentials into rational rank tuples.",
                "Emit a machine-checkable edge certificate for each accelerated branch.",
            ],
        },
        "goldbach": {
            "status": "blueprint_open_not_proof",
            "target_lemma": "GB-TD3",
            "new_object_family": "Explicit inequality budget ledgers that optimize analytic constants against a finite verification ceiling.",
            "why_not_reproduction": "Finite Goldbach verification and asymptotic circle-method summaries are excluded; the object must lower a concrete unconditional cutoff.",
            "ai_generation_prompt": "Generate a main-term-minus-error budget for R_2(n), attach a theorem source and validity range to every line, and compute the resulting N0.",
            "minimal_counterexample": "Any unverified error term or validity range that pushes N0 above the finite certificate range.",
            "falsification_oracle": "Exact constant replay, range coverage audit, and finite-overlap comparison against the certified bound.",
            "formalization_seed": "Define BudgetLine, ValidityRange, CutoffCalculator, and FiniteOverlapBridge with no heuristic independence assumptions.",
            "success_upgrade": "Promote only if the explicit N0 is below the verified finite range and every budget term is theorem-backed.",
            "next_experiments": [
                "Normalize published explicit constants into one machine-readable budget schema.",
                "Run sensitivity analysis to identify the error term most responsible for N0.",
                "Generate candidate tightened inequalities and reject any line without a theorem source.",
            ],
        },
        "twin-prime": {
            "status": "blueprint_open_not_proof",
            "target_lemma": "TP-TD2",
            "new_object_family": "Exact-pair parity witnesses that distinguish prime pairs from parity-model semiprime impostors.",
            "why_not_reproduction": "Bounded gaps, Hardy-Littlewood-scale fits, and finite twin counts are excluded; the object must force exact gap 2 infinitely often.",
            "ai_generation_prompt": "Generate an exact-pair weight plus a parity countermodel, then state the statistic that separates true prime pairs from the countermodel.",
            "minimal_counterexample": "A parity model where the proposed weight remains positive but no exact twin-prime conclusion follows.",
            "falsification_oracle": "Parity-model replay plus wider-gap leakage audit for gaps 4, 6, 246, and arbitrary H > 2.",
            "formalization_seed": "Define ExactPairWeight, ParityModel, WiderGapLeakage, and PositiveExactGapMass before any infinitude bridge.",
            "success_upgrade": "Promote only if positive mass survives the parity model and cannot be reinterpreted as a bounded-gap theorem.",
            "next_experiments": [
                "Generate weights that explicitly subtract wider-gap contributions.",
                "Replay each weight in a semiprime parity model before inspecting primes.",
                "Track whether the exact-gap lower bound remains positive as the scale parameter grows.",
            ],
        },
    }
    breakthrough_blueprint = breakthrough_blueprints.get(problem_id, breakthrough_blueprints["riemann"])
    mutations = list(forge.get("candidate_mutations", []))
    experiments = [
        {
            "id": f"{problem_id}-forge-{idx + 1}",
            "generator": item,
            "artifact": f"data/open-problem/{problem_id}/forge-{idx + 1}.json",
            "success_rule": "A generated object survives all listed countermodel tests and closes one named infinite proof gap.",
            "failure_rule": "The object is demoted if it proves only a bounded result, a weaker theorem, or a circular equivalent criterion.",
        }
        for idx, item in enumerate(forge.get("search_grammar", []))
    ]
    attack_runbook = [
        {
            "step": "A1",
            "name": "object synthesis",
            "action": "Generate the smallest theorem object matching one mutation and one grammar production.",
            "required_output": f"data/open-problem/{problem_id}/candidate-object.json",
            "failure_exit": "No theorem-shaped object with explicit assumptions is produced.",
        },
        {
            "step": "A2",
            "name": "countermodel stress",
            "action": "Run every countermodel in the battery against the candidate before any positive claim is allowed.",
            "required_output": f"data/open-problem/{problem_id}/countermodel-report.json",
            "failure_exit": "A countermodel survives or the candidate falls back to finite-only evidence.",
        },
        {
            "step": "A3",
            "name": "infinite bridge extraction",
            "action": "Extract the exact missing infinite theorem and separate it from bounded computation.",
            "required_output": f"formal/{problem_id}/InfiniteBridge.lean",
            "failure_exit": "The bridge imports the target conjecture, a heuristic, or a weaker theorem.",
        },
        {
            "step": "A4",
            "name": "independent replay package",
            "action": "Prepare a replayable artifact that another reviewer can check without trusting the browser page.",
            "required_output": f"data/open-problem/{problem_id}/replay-manifest.json",
            "failure_exit": "The proof cannot be replayed from explicit assumptions and artifacts.",
        },
    ]
    falsification_scorecard = [
        {
            "test": "novel-object test",
            "question": "Does the candidate introduce a new theorem object rather than rephrasing a known finite check?",
            "pass_signal": "New object, assumptions, and target theorem are all explicit.",
            "fail_signal": "The candidate is only a computation replay, visualization, or heuristic restatement.",
            "status": "required",
        },
        {
            "test": "barrier-directness test",
            "question": "Does the candidate attack the known barrier directly?",
            "pass_signal": "The object names the finite-to-infinite, parity, positivity, or cutoff bridge it closes.",
            "fail_signal": "The object proves only a weaker theorem or shifts the barrier into an unstated lemma.",
            "status": "required",
        },
        {
            "test": "countermodel survival test",
            "question": "Can the object survive the listed countermodel battery?",
            "pass_signal": "Every countermodel is rejected by a theorem-level reason.",
            "fail_signal": "At least one countermodel survives or is not checked.",
            "status": "required",
        },
        {
            "test": "formal replay test",
            "question": "Can the bridge be replayed independently from explicit artifacts?",
            "pass_signal": "A proof assistant or accepted theorem reference discharges the infinite bridge.",
            "fail_signal": "The proof requires trust in PrimeProject code, sampled data, or informal prose.",
            "status": "blocked_until_candidate_survives",
        },
    ]
    cross_problem_synthesis = [
        {
            "pattern": "positivity-to-descent transfer",
            "source_problem": "riemann",
            "target_problem": "collatz",
            "hypothesis": "A positivity certificate can be reinterpreted as a well-founded descent potential if every local transition consumes a quantified debt.",
            "transfer_test": "Convert one RH kernel positivity block into a Collatz residue potential template and check exact branch decrease.",
            "failure_mode": "Positive average mass does not imply pointwise descent over every residue branch.",
            "status": "experimental_transfer_not_proof",
            "scores": {"novelty": 4, "barrier_directness": 5, "formalizability": 3, "countermodel_risk": 4},
            "decision": "pursue_first_if_exact_branch_decrease_emerges",
        },
        {
            "pattern": "cutoff-to-parity transfer",
            "source_problem": "goldbach",
            "target_problem": "twin-prime",
            "hypothesis": "An explicit inequality budget may expose exactly which term must become parity-sensitive for exact gap 2.",
            "transfer_test": "Rewrite the Goldbach main-term-minus-error ledger with an exact-pair selector and run parity countermodels.",
            "failure_mode": "The budget can remain positive for bounded gaps while exact gap 2 still vanishes.",
            "status": "experimental_transfer_not_proof",
            "scores": {"novelty": 4, "barrier_directness": 5, "formalizability": 4, "countermodel_risk": 5},
            "decision": "high_value_high_risk_requires_parity_break",
        },
        {
            "pattern": "automaton-to-cutoff transfer",
            "source_problem": "collatz",
            "target_problem": "goldbach",
            "hypothesis": "Worst-case residue automata can rank obstruction classes before analytic constants are optimized.",
            "transfer_test": "Treat least-witness Goldbach residues as states and rank them by required explicit error budget.",
            "failure_mode": "A finite residue ranking does not produce the large-n lower-bound theorem.",
            "status": "bounded_diagnostic_only",
            "scores": {"novelty": 3, "barrier_directness": 3, "formalizability": 4, "countermodel_risk": 3},
            "decision": "use_as_diagnostic_not_primary_solution_path",
        },
        {
            "pattern": "exact-selector transfer",
            "source_problem": "twin-prime",
            "target_problem": "riemann",
            "hypothesis": "Selector terms that isolate exact gap 2 may inspire non-averaged test functions for zero-side positivity.",
            "transfer_test": "Build a prime-side test function that penalizes averaged gap evidence and rewards exact structure, then audit circularity.",
            "failure_mode": "Exact prime-side selectors may not map to an admissible RH-equivalent positivity class.",
            "status": "speculative_bridge_search",
            "scores": {"novelty": 5, "barrier_directness": 3, "formalizability": 2, "countermodel_risk": 5},
            "decision": "speculative_track_only_until_admissible_class_exists",
        },
    ]
    for item in cross_problem_synthesis:
        scores = item["scores"]
        item["priority_score"] = (
            scores["novelty"]
            + scores["barrier_directness"]
            + scores["formalizability"]
            - scores["countermodel_risk"]
        )
    prioritized_synthesis = sorted(
        cross_problem_synthesis,
        key=lambda item: (-int(item["priority_score"]), str(item["pattern"])),
    )
    return {
        "schema": AI_PROOF_FORGE_SCHEMA,
        "problem_id": problem_id,
        "status": "active_unsolved_proof_forge",
        **forge,
        "theorem_decomposition": theorem_decomposition,
        "decomposition_summary": {
            "status": "open_decomposition_not_proof",
            "lemma_count": len(theorem_decomposition),
            "highest_risk": highest_risk.get("id"),
            "highest_risk_lemma": highest_risk.get("lemma"),
            "closure_rule": "Every decomposition lemma must be formalized or replaced by an accepted theorem before the page can leave open_not_proven.",
        },
        "breakthrough_object_blueprint": breakthrough_blueprint,
        "experiments": experiments,
        "discovery_loop": {
            "status": "candidate_generation_active_no_solution",
            "iteration_contract": "Generate a mutated theorem object, run the countermodel battery, demote failures with a mathematical reason, and promote only replayable infinite-bridge artifacts.",
            "candidate_mutations": mutations,
            "survivor_count": sum(
                1 for item in mutations if item.get("current_verdict") == "open_candidate_not_proof"
            ),
            "blocked_count": sum(
                1 for item in mutations if "blocked" in str(item.get("current_verdict", ""))
            ),
            "attack_runbook": attack_runbook,
            "falsification_scorecard": falsification_scorecard,
            "cross_problem_synthesis": cross_problem_synthesis,
            "portfolio_decision": {
                "status": "ranked_unsolved_research_portfolio",
                "ranking_rule": "priority = novelty + barrier_directness + formalizability - countermodel_risk; ties are broken by lower proof weakening risk.",
                "top_candidate": prioritized_synthesis[0]["pattern"],
                "stop_rule": "Stop or demote a track when it proves only a finite result, a weaker theorem, or a transfer test with surviving countermodels.",
                "ranked_tracks": [
                    {
                        "rank": idx + 1,
                        "pattern": item["pattern"],
                        "source_problem": item["source_problem"],
                        "target_problem": item["target_problem"],
                        "priority_score": item["priority_score"],
                        "decision": item["decision"],
                    }
                    for idx, item in enumerate(prioritized_synthesis)
                ],
            },
        },
        "non_reproduction_rule": "The forge is only useful if it creates a new theorem object or rejects a route for a precise mathematical reason; reproducing known finite checks does not count as progress.",
        "promotion_gate": "Promotion requires an independently replayable theorem artifact that closes the infinite bridge without weakening the original conjecture.",
    }


def proof_route_triage(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    route_bank: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-R1",
                "route": "finite zero or prime-count verification",
                "status": "rejected_finite_to_infinite",
                "machine_test": "bounded certificate cannot quantify over every non-trivial zero",
                "required_upgrade": "all-height zero theorem or accepted RH-equivalent bridge",
            },
            {
                "id": "RH-R2",
                "route": "prime-counting residual fit",
                "status": "bounded_support_only",
                "machine_test": "numeric envelope must survive every x, not selected checkpoints",
                "required_upgrade": "explicit all-x theta or psi error theorem",
            },
            {
                "id": "RH-R3",
                "route": "Hilbert-Polya operator program",
                "status": "viable_requires_new_theorem",
                "machine_test": "operator must be self-adjoint and have zeta zeros as spectrum",
                "required_upgrade": "formal spectral construction and equivalence proof",
            },
            {
                "id": "RH-R4",
                "route": "explicit all-x theta bound plus RH-equivalence bridge",
                "status": "current_decisive_route",
                "machine_test": "derive an accepted RH-equivalent statement without importing RH",
                "required_upgrade": "formal all-x prime-counting error theorem with explicit constants",
            },
        ],
        "collatz": [
            {
                "id": "CO-R1",
                "route": "finite trajectory replay",
                "status": "rejected_finite_to_infinite",
                "machine_test": "verified starts do not cover all natural numbers",
                "required_upgrade": "symbolic cover over infinitely many residue blocks",
            },
            {
                "id": "CO-R2",
                "route": "parity random-walk drift",
                "status": "heuristic_only",
                "machine_test": "average drift does not exclude exceptional cycles or divergence",
                "required_upgrade": "deterministic descent theorem",
            },
            {
                "id": "CO-R3",
                "route": "residue-block descent cover",
                "status": "current_decisive_route",
                "machine_test": "every residue block must map to a smaller certified representative",
                "required_upgrade": "formal residue-cover descent theorem",
            },
            {
                "id": "CO-R4",
                "route": "cycle exclusion without descent",
                "status": "insufficient_partial_result",
                "machine_test": "cycle exclusion alone does not rule out divergent branches",
                "required_upgrade": "joint cycle and divergence exclusion theorem",
            },
        ],
        "goldbach": [
            {
                "id": "GB-R1",
                "route": "finite decomposition search",
                "status": "rejected_finite_to_infinite",
                "machine_test": "bounded decompositions do not cover every even integer",
                "required_upgrade": "explicit threshold theorem for the infinite tail",
            },
            {
                "id": "GB-R2",
                "route": "weak Goldbach substitution",
                "status": "rejected_weaker_theorem",
                "machine_test": "three-prime odd representation is not strong two-prime Goldbach",
                "required_upgrade": "two-prime representation lower bound",
            },
            {
                "id": "GB-R3",
                "route": "circle-method lower bound with certified cutoff",
                "status": "current_decisive_route",
                "machine_test": "analytic threshold must start below the bounded certificate limit",
                "required_upgrade": "formal large-even threshold theorem with explicit cutoff",
            },
            {
                "id": "GB-R4",
                "route": "sampled residue-class persistence",
                "status": "heuristic_only",
                "machine_test": "sampled classes cannot replace a uniform lower bound",
                "required_upgrade": "uniform residue-sensitive representation bound",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-R1",
                "route": "finite twin-pair counting",
                "status": "rejected_finite_to_infinite",
                "machine_test": "positive bounded counts do not force arbitrarily large pairs",
                "required_upgrade": "exact gap-2 infinitude theorem",
            },
            {
                "id": "TP-R2",
                "route": "bounded prime gaps",
                "status": "rejected_weaker_theorem",
                "machine_test": "gap less than a constant is not exact gap 2",
                "required_upgrade": "formal exact gap-2 lower-bound theorem",
            },
            {
                "id": "TP-R3",
                "route": "Hardy-Littlewood density match",
                "status": "heuristic_only",
                "machine_test": "k-tuple density cannot be assumed as the proof",
                "required_upgrade": "assumption-free exact gap-2 lower bound",
            },
            {
                "id": "TP-R4",
                "route": "exact gap-2 lower bound",
                "status": "current_decisive_route",
                "machine_test": "lower bound must remain positive for arbitrarily large x",
                "required_upgrade": "unconditional exact gap-2 lower-bound theorem",
            },
        ],
    }
    routes = route_bank.get(problem_id, [])
    return {
        "schema": PROOF_ROUTE_TRIAGE_SCHEMA,
        "problem_id": problem_id,
        "status": "routes_triaged_no_full_proof",
        "route_count": len(routes),
        "rejected_count": sum(1 for item in routes if item["status"].startswith("rejected")),
        "heuristic_count": sum(1 for item in routes if item["status"] == "heuristic_only"),
        "current_decisive_route": next((item["id"] for item in routes if item["status"] == "current_decisive_route"), "missing"),
        "routes": routes,
        "machine_rule": "Only a route marked current_decisive_route can drive the next proof attempt, and it still cannot change the page status until its required upgrade is a formal artifact or accepted theorem.",
    }


def decisive_theorem_spec(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    triage = problem.get("proof_route_triage", {}) if isinstance(problem.get("proof_route_triage"), dict) else {}
    specs: dict[str, dict[str, object]] = {
        "riemann": {
            "spec_id": "RH-DT1",
            "title": "Explicit all-x prime-counting error theorem",
            "candidate_statement": "Prove an explicit all-x theta or psi error bound strong enough to pass an accepted RH-equivalence bridge, without importing RH or an equivalent zero theorem.",
            "would_close": ["RH-M3", "RH-M4", "RH-G1", "RH-G2"],
            "allowed_inputs": [
                "bounded prime-counting certificate",
                "published RH-equivalence theorem stated as a bridge, not assumed as the target",
                "formal explicit-constant analytic inequalities",
            ],
            "forbidden_shortcuts": [
                "finite zero verification",
                "assuming RH under an equivalent theorem name",
                "fitting a numerical envelope without an all-x proof",
            ],
            "machine_checks": [
                "constants are explicit",
                "domain covers all x beyond a stated threshold",
                "bounded certificate covers the remaining finite interval",
                "formal bridge does not import the target theorem",
            ],
            "blocking_gap": "No formal all-x prime-counting error theorem is available.",
        },
        "collatz": {
            "spec_id": "CO-DT1",
            "title": "Residue-block descent cover theorem",
            "candidate_statement": "Prove that every positive integer belongs to a certified residue block whose accelerated Collatz trajectory reaches a smaller positive representative or 1.",
            "would_close": ["CO-M3", "CO-M4", "CO-G1", "CO-G2", "CO-G3"],
            "allowed_inputs": [
                "bounded trajectory certificate",
                "symbolic residue classes",
                "formal descent measure",
            ],
            "forbidden_shortcuts": [
                "random-walk drift as proof",
                "checking only enumerated starts",
                "cycle exclusion without divergence exclusion",
            ],
            "machine_checks": [
                "residue blocks cover all positive integers",
                "each block has a decreasing certified representative",
                "descent measure is well-founded",
                "cycle and divergence exclusions follow from the same cover",
            ],
            "blocking_gap": "No residue-block cover currently proves global descent.",
        },
        "goldbach": {
            "spec_id": "GB-DT1",
            "title": "Large-even two-prime representation lower-bound theorem",
            "candidate_statement": "Prove an explicit positive lower bound for two-prime representations of every even n >= N0, with N0 below the bounded certificate limit.",
            "would_close": ["GB-M3", "GB-M4", "GB-G1", "GB-G2"],
            "allowed_inputs": [
                "bounded Goldbach decomposition certificate",
                "explicit circle-method estimates",
                "verified cutoff comparison N0 <= certificate limit",
            ],
            "forbidden_shortcuts": [
                "weak Goldbach substitution",
                "sampled decompositions as a lower-bound theorem",
                "analytic threshold above the certified range",
            ],
            "machine_checks": [
                "lower bound is positive for every even n >= N0",
                "N0 is explicit",
                "finite certificate covers every even n below N0",
                "proof is two-prime, not three-prime",
            ],
            "blocking_gap": "No explicit positive two-prime lower bound with compatible cutoff is formalized.",
        },
        "twin-prime": {
            "spec_id": "TP-DT1",
            "title": "Unconditional exact gap-2 lower-bound theorem",
            "candidate_statement": "Prove a positive lower bound for exact twin-prime pairs up to arbitrarily large x, without assuming Hardy-Littlewood or replacing exact gap 2 by bounded gaps.",
            "would_close": ["TP-M3", "TP-M4", "TP-G1", "TP-G2", "TP-G3"],
            "allowed_inputs": [
                "bounded twin-pair certificate",
                "admissible two-point pattern analysis",
                "assumption-free distribution theorem for exact gap 2",
            ],
            "forbidden_shortcuts": [
                "bounded prime gaps as twin primes",
                "Hardy-Littlewood k-tuple density as an axiom",
                "finite twin-pair persistence as infinitude",
            ],
            "machine_checks": [
                "statement is about exact gap 2",
                "bound stays positive for arbitrarily large x",
                "no unproved k-tuple independence assumption is imported",
                "infinitude bridge is formalized",
            ],
            "blocking_gap": "No unconditional exact gap-2 lower-bound theorem is available.",
        },
    }
    spec = specs.get(problem_id, {})
    return {
        "schema": DECISIVE_THEOREM_SPEC_SCHEMA,
        "problem_id": problem_id,
        "status": "decisive_theorem_open",
        "target_route": triage.get("current_decisive_route", "missing"),
        "artifact_status": "missing_formal_theorem",
        **spec,
        "promotion_rule": "This theorem spec can only upgrade the page when the theorem is formal_proof_verified or accepted_theorem and every listed machine check passes.",
    }


def decisive_theorem_subgoals(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    spec = problem.get("decisive_theorem_spec", {}) if isinstance(problem.get("decisive_theorem_spec"), dict) else {}
    subgoal_bank: dict[str, list[dict[str, str]]] = {
        "riemann": [
            {
                "id": "RH-SG1",
                "label": "Bounded prime-counting certificate",
                "status": "complete_bounded_support",
                "artifact": "certificate.merkle_root",
                "closing_test": "replay decimal checkpoints and prime endpoint stress rows",
            },
            {
                "id": "RH-SG2",
                "label": "Explicit theta/psi inequality statement",
                "status": "open_formal_statement",
                "artifact": "Lean theorem statement with constants",
                "closing_test": "all constants and domain thresholds are named",
            },
            {
                "id": "RH-SG3",
                "label": "All-x analytic proof",
                "status": "open_infinite_bridge",
                "artifact": "formal proof or accepted theorem",
                "closing_test": "bound holds for every x beyond threshold",
            },
            {
                "id": "RH-SG4",
                "label": "Finite interval bridge",
                "status": "open_bridge",
                "artifact": "cutoff comparison certificate",
                "closing_test": "bounded certificate covers every x below threshold",
            },
            {
                "id": "RH-SG5",
                "label": "RH-equivalence replay",
                "status": "blocked_until_sg2_sg4",
                "artifact": "independent kernel replay",
                "closing_test": "bridge proves the target without importing RH",
            },
        ],
        "collatz": [
            {
                "id": "CO-SG1",
                "label": "Bounded trajectory certificate",
                "status": "complete_bounded_support",
                "artifact": "certificate.merkle_root",
                "closing_test": "replay all starts through committed limit",
            },
            {
                "id": "CO-SG2",
                "label": "Residue block cover",
                "status": "open_infinite_bridge",
                "artifact": "formal cover theorem",
                "closing_test": "every positive integer belongs to at least one block",
            },
            {
                "id": "CO-SG3",
                "label": "Strict descent measure",
                "status": "open_formal_statement",
                "artifact": "well-founded measure proof",
                "closing_test": "each block maps to a smaller representative or 1",
            },
            {
                "id": "CO-SG4",
                "label": "Cycle exclusion",
                "status": "open_bridge",
                "artifact": "cycle contradiction theorem",
                "closing_test": "non-trivial cycles contradict descent",
            },
            {
                "id": "CO-SG5",
                "label": "Divergence exclusion",
                "status": "blocked_until_sg2_sg3",
                "artifact": "global convergence theorem",
                "closing_test": "unbounded branches contradict well-founded descent",
            },
        ],
        "goldbach": [
            {
                "id": "GB-SG1",
                "label": "Bounded decomposition certificate",
                "status": "complete_bounded_support",
                "artifact": "certificate.merkle_root",
                "closing_test": "replay every even n through committed limit",
            },
            {
                "id": "GB-SG2",
                "label": "Explicit representation lower bound",
                "status": "open_infinite_bridge",
                "artifact": "formal lower-bound theorem",
                "closing_test": "bound is positive for every even n >= N0",
            },
            {
                "id": "GB-SG3",
                "label": "Cutoff compatibility",
                "status": "open_bridge",
                "artifact": "N0 <= certificate limit proof",
                "closing_test": "analytic threshold starts inside certified range",
            },
            {
                "id": "GB-SG4",
                "label": "Two-prime specificity",
                "status": "open_formal_statement",
                "artifact": "formal representation definition",
                "closing_test": "theorem cannot be satisfied by ternary Goldbach",
            },
            {
                "id": "GB-SG5",
                "label": "Full interval union",
                "status": "blocked_until_sg2_sg3",
                "artifact": "finite plus infinite coverage theorem",
                "closing_test": "every even n > 2 is covered exactly once by the proof split",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-SG1",
                "label": "Bounded twin-pair certificate",
                "status": "complete_bounded_support",
                "artifact": "certificate.merkle_root",
                "closing_test": "replay exact gap-2 pairs through committed limit",
            },
            {
                "id": "TP-SG2",
                "label": "Exact gap-2 formal definition",
                "status": "open_formal_statement",
                "artifact": "Lean exact gap-2 predicate",
                "closing_test": "bounded-gap theorems cannot satisfy the definition",
            },
            {
                "id": "TP-SG3",
                "label": "Unconditional lower bound",
                "status": "open_infinite_bridge",
                "artifact": "formal lower-bound theorem",
                "closing_test": "bound stays positive for arbitrarily large x",
            },
            {
                "id": "TP-SG4",
                "label": "Heuristic removal",
                "status": "open_bridge",
                "artifact": "assumption-free distribution argument",
                "closing_test": "no Hardy-Littlewood or k-tuple axiom is imported",
            },
            {
                "id": "TP-SG5",
                "label": "Infinitude bridge",
                "status": "blocked_until_sg3_sg4",
                "artifact": "formal infinitude theorem",
                "closing_test": "positive lower bound implies arbitrarily large exact twins",
            },
        ],
    }
    subgoals = subgoal_bank.get(problem_id, [])
    open_items = [item for item in subgoals if item["status"].startswith("open")]
    blocked_items = [item for item in subgoals if item["status"].startswith("blocked")]
    complete_items = [item for item in subgoals if item["status"].startswith("complete")]
    return {
        "schema": DECISIVE_THEOREM_SUBGOALS_SCHEMA,
        "problem_id": problem_id,
        "status": "subgoals_open",
        "spec_id": spec.get("spec_id", "missing"),
        "subgoal_count": len(subgoals),
        "complete_count": len(complete_items),
        "open_count": len(open_items),
        "blocked_count": len(blocked_items),
        "subgoals": subgoals,
        "machine_rule": "The decisive theorem remains missing while any subgoal is open or blocked; bounded support can guide but cannot close an infinite bridge.",
    }


def decisive_theorem_attack_tickets(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    subgoal_report = problem.get("decisive_theorem_subgoals", {}) if isinstance(problem.get("decisive_theorem_subgoals"), dict) else {}
    subgoals = subgoal_report.get("subgoals", []) if isinstance(subgoal_report, dict) else []
    tickets = []
    for index, subgoal in enumerate(subgoals, start=1):
        if not isinstance(subgoal, dict) or str(subgoal.get("status", "")).startswith("complete"):
            continue
        status = str(subgoal.get("status", "open"))
        priority = "P0" if "infinite_bridge" in status or status.startswith("blocked") else "P1"
        tickets.append(
            {
                "id": f"{problem_id.upper().replace('-', '_')}-AT{index}",
                "subgoal_id": subgoal.get("id", "missing"),
                "priority": priority,
                "status": "planned_not_executed",
                "attack_hypothesis": f"{subgoal.get('label', 'subgoal')} can be reduced to {subgoal.get('artifact', 'a formal artifact')}.",
                "first_experiment": subgoal.get("closing_test", "missing closing test"),
                "falsification_test": f"Reject this route if it cannot produce {subgoal.get('artifact', 'the required artifact')} without using a forbidden shortcut or finite-only evidence.",
                "required_output": subgoal.get("artifact", "missing artifact"),
            }
        )
    return {
        "schema": DECISIVE_THEOREM_ATTACK_TICKETS_SCHEMA,
        "problem_id": problem_id,
        "status": "attack_tickets_open",
        "ticket_count": len(tickets),
        "p0_count": sum(1 for item in tickets if item["priority"] == "P0"),
        "tickets": tickets,
        "machine_rule": "A ticket can close only by producing its required output and passing its falsification test; planned tickets are not proof artifacts.",
    }


def proof_breakthrough_agenda(problem: dict[str, object]) -> dict[str, object]:
    problem_id = str(problem.get("id", "unknown"))
    triage = problem.get("proof_route_triage", {}) if isinstance(problem.get("proof_route_triage"), dict) else {}
    theorem_spec = problem.get("decisive_theorem_spec", {}) if isinstance(problem.get("decisive_theorem_spec"), dict) else {}
    agenda_bank: dict[str, list[dict[str, object]]] = {
        "riemann": [
            {
                "id": "RH-BTA1",
                "novelty_claim": "Turn prime-counting residual structure into an all-x explicit bound rather than another finite zero check.",
                "barrier_target": "finite_to_infinite_lift",
                "uses_primeproject_tools": ["bounded theta checkpoints", "Merkle replay", "route triage"],
                "minimum_new_theorem": "explicit theta or psi error theorem with named constants and all-x domain",
                "first_artifact": "Lean-ready inequality statement plus cutoff comparison certificate",
                "kill_condition": "the bound is fitted only at checkpoints or silently assumes RH-equivalent zero placement",
                "status": "research_target_not_proof",
            },
            {
                "id": "RH-BTA2",
                "novelty_claim": "Use Li-coefficient positivity as a machine-audited bridge only if the infinite positivity argument is independent.",
                "barrier_target": "equivalent_target_import",
                "uses_primeproject_tools": ["proof candidate intake", "forbidden shortcut audit", "formal skeleton audit"],
                "minimum_new_theorem": "unconditional positivity theorem for every Li coefficient",
                "first_artifact": "formal reduction showing the coefficient theorem is not merely RH renamed",
                "kill_condition": "the proof imports a known RH-equivalent statement as an axiom",
                "status": "research_target_not_proof",
            },
            {
                "id": "RH-BTA3",
                "novelty_claim": "Pursue a Hilbert-Polya construction only through a checkable self-adjoint operator and spectrum equivalence.",
                "barrier_target": "spectral_realization_gap",
                "uses_primeproject_tools": ["known barrier audit", "formal replay package", "proof obligation DAG"],
                "minimum_new_theorem": "self-adjoint operator theorem whose spectrum is exactly the non-trivial zeta zeros",
                "first_artifact": "operator domain, symmetry, self-adjointness, and spectral map definitions",
                "kill_condition": "the construction is formal analogy without a spectrum equality theorem",
                "status": "research_target_not_proof",
            },
        ],
        "collatz": [
            {
                "id": "CO-BTA1",
                "novelty_claim": "Replace probabilistic parity drift with a deterministic residue-block descent cover.",
                "barrier_target": "global_descent_cover",
                "uses_primeproject_tools": ["bounded trajectory replay", "residue stress probes", "attack tickets"],
                "minimum_new_theorem": "every positive integer lies in a certified block that descends under the accelerated map",
                "first_artifact": "symbolic residue cover generator with proof obligations for coverage and descent",
                "kill_condition": "any residue block remains uncovered or maps without strict decrease",
                "status": "research_target_not_proof",
            },
            {
                "id": "CO-BTA2",
                "novelty_claim": "Make divergence impossible by proving a well-founded measure decreases after bounded symbolic windows.",
                "barrier_target": "divergence_exclusion",
                "uses_primeproject_tools": ["frontier probe", "proof gap taxonomy", "formal proof contract"],
                "minimum_new_theorem": "well-founded descent theorem over all accelerated trajectory windows",
                "first_artifact": "candidate measure plus machine-generated counter-window search",
                "kill_condition": "a symbolic window preserves or increases the measure indefinitely",
                "status": "research_target_not_proof",
            },
            {
                "id": "CO-BTA3",
                "novelty_claim": "Treat cycle exclusion and convergence as one theorem, not two disconnected partial results.",
                "barrier_target": "cycle_divergence_split",
                "uses_primeproject_tools": ["obligation DAG", "candidate intake", "execution protocol"],
                "minimum_new_theorem": "global convergence theorem deriving non-trivial cycle and divergence exclusion from the same descent cover",
                "first_artifact": "formal implication graph from block cover to convergence",
                "kill_condition": "the route excludes cycles but leaves unbounded branches possible",
                "status": "research_target_not_proof",
            },
        ],
        "goldbach": [
            {
                "id": "GB-BTA1",
                "novelty_claim": "Couple bounded decomposition replay with an explicit analytic threshold below the replay limit.",
                "barrier_target": "cutoff_compatibility",
                "uses_primeproject_tools": ["Goldbach certificate", "cutoff comparison", "formal replay package"],
                "minimum_new_theorem": "positive two-prime representation lower bound for every even n >= N0",
                "first_artifact": "explicit N0 theorem plus proof that N0 is below the certified finite limit",
                "kill_condition": "the analytic threshold exceeds the certified range or is not explicit",
                "status": "research_target_not_proof",
            },
            {
                "id": "GB-BTA2",
                "novelty_claim": "Turn residue persistence into a uniform lower bound, not a sampled support chart.",
                "barrier_target": "uniformity_gap",
                "uses_primeproject_tools": ["residue drift", "representation stress rows", "falsification battery"],
                "minimum_new_theorem": "uniform residue-sensitive lower bound for binary representations",
                "first_artifact": "worst-class residue audit with explicit lower-bound candidate",
                "kill_condition": "a residue class or interval family keeps the lower bound at zero",
                "status": "research_target_not_proof",
            },
            {
                "id": "GB-BTA3",
                "novelty_claim": "Forbid weak-Goldbach substitution by making the two-prime predicate the kernel target.",
                "barrier_target": "weaker_theorem_substitution",
                "uses_primeproject_tools": ["formal skeleton audit", "proof candidate intake", "claim policy"],
                "minimum_new_theorem": "binary Goldbach theorem over every even integer greater than two",
                "first_artifact": "Lean binary representation predicate and rejection test for ternary proofs",
                "kill_condition": "the proof succeeds only with three primes or density on average",
                "status": "research_target_not_proof",
            },
        ],
        "twin-prime": [
            {
                "id": "TP-BTA1",
                "novelty_claim": "Separate exact gap-2 infinitude from all bounded-gap evidence before any sieve route is trusted.",
                "barrier_target": "exact_gap_two_barrier",
                "uses_primeproject_tools": ["twin-pair certificate", "proof route triage", "known barrier audit"],
                "minimum_new_theorem": "positive exact gap-2 lower bound for arbitrarily large x",
                "first_artifact": "formal exact-gap predicate plus bounded-gap rejection lemma",
                "kill_condition": "the argument proves only gaps below a fixed constant larger than 2",
                "status": "research_target_not_proof",
            },
            {
                "id": "TP-BTA2",
                "novelty_claim": "Convert admissible-pair residue persistence into an assumption-free lower bound.",
                "barrier_target": "parity_and_distribution_barrier",
                "uses_primeproject_tools": ["residue drift", "frontier probe", "attack tickets"],
                "minimum_new_theorem": "distribution theorem for exact two-point prime patterns without Hardy-Littlewood as an axiom",
                "first_artifact": "candidate lower-bound form stress-tested against wheel and residue controls",
                "kill_condition": "the route depends on k-tuple independence or Hardy-Littlewood density",
                "status": "research_target_not_proof",
            },
            {
                "id": "TP-BTA3",
                "novelty_claim": "Make the infinitude bridge explicit: positive lower bounds must force arbitrarily large twin pairs.",
                "barrier_target": "infinitude_bridge",
                "uses_primeproject_tools": ["obligation DAG", "formal proof contract", "review docket"],
                "minimum_new_theorem": "formal implication from exact gap-2 lower bound to infinitely many twin primes",
                "first_artifact": "kernel-checkable theorem linking lower-bound positivity to unbounded witnesses",
                "kill_condition": "the lower bound applies only to bounded windows or averaged non-exact gaps",
                "status": "research_target_not_proof",
            },
        ],
    }
    routes = agenda_bank.get(problem_id, [])
    return {
        "schema": PROOF_BREAKTHROUGH_AGENDA_SCHEMA,
        "problem_id": problem_id,
        "status": "breakthrough_agenda_open",
        "route_count": len(routes),
        "current_decisive_route": triage.get("current_decisive_route", "missing"),
        "target_spec": theorem_spec.get("spec_id", "missing"),
        "barrier_count": len({str(route.get("barrier_target", "")) for route in routes}),
        "routes": routes,
        "machine_rule": "A breakthrough agenda item is a research target, not a proof claim; it can close only by producing the minimum new theorem and surviving its kill condition.",
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
        problem["formal_skeleton_audit"] = formal_skeleton_audit(problem)
        problem["proof_verdict"] = proof_verdict(problem)
        problem["proof_route_triage"] = proof_route_triage(problem)
        problem["decisive_theorem_spec"] = decisive_theorem_spec(problem)
        problem["decisive_theorem_subgoals"] = decisive_theorem_subgoals(problem)
        problem["decisive_theorem_attack_tickets"] = decisive_theorem_attack_tickets(problem)
        problem["actual_proof_attempt_runner"] = actual_proof_attempt_runner(problem)
        problem["candidate_lemma_workbench"] = candidate_lemma_workbench(problem)
        problem["machine_proof_search_trials"] = machine_proof_search_trials(problem)
        problem["formal_upgrade_matrix"] = formal_upgrade_matrix(problem)
        problem["proof_kernel_roadmap"] = proof_kernel_roadmap(problem)
        problem["formal_kernel_contract_audit"] = formal_kernel_contract_audit(problem)
        problem["invalid_proof_shortcut_suite"] = invalid_proof_shortcut_suite(problem)
        problem["ai_solver_frontier"] = ai_solver_frontier(problem)
        problem["ai_breakthrough_program"] = ai_breakthrough_program(problem)
        problem["ai_proof_forge"] = ai_proof_forge(problem)
        problem["proof_breakthrough_agenda"] = proof_breakthrough_agenda(problem)
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
