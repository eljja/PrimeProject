from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_LINEAGE_SCHEMA = "primeproject.artifact-lineage.v1"


DEFAULT_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "collection_matrix": ("manifest",),
    "collection_power": ("collection_matrix",),
    "provenance_requirements": ("manifest",),
    "provenance_audit": ("provenance_requirements",),
    "baseline_acceptance": ("manifest", "collection_matrix", "collection_power", "provenance_audit"),
    "baseline_promotion_plan": ("baseline_acceptance", "collection_power"),
    "collection_handoff": (
        "manifest",
        "collection_matrix",
        "collection_power",
        "provenance_requirements",
        "provenance_audit",
        "baseline_acceptance",
        "baseline_promotion_plan",
        "classifier_report",
    ),
    "collection_submission_contract": ("collection_handoff",),
    "collection_submission_lint": ("collection_submission_contract",),
    "collection_fixture_audit": ("collection_submission_contract", "collection_submission_lint"),
    "collection_intake": ("collection_handoff", "collection_submission_contract"),
    "classifier_report": ("feature_vectors",),
    "readiness": ("manifest", "attribution_grid", "classifier_report"),
    "null_calibration": ("attribution_grid",),
    "replication_audit": ("attribution_grid", "null_calibration"),
    "evidence_pack": (
        "manifest",
        "readiness",
        "attribution_grid",
        "null_calibration",
        "replication_audit",
        "feature_vectors",
        "classifier_report",
        "baseline_acceptance",
        "project_evolution",
        "snapshot_manifest",
        "collection_matrix",
        "collection_power",
        "provenance_requirements",
        "provenance_audit",
        "baseline_promotion_plan",
        "collection_handoff",
        "collection_submission_contract",
        "collection_submission_lint",
        "collection_fixture_audit",
        "collection_intake",
    ),
    "claim_ledger": ("evidence_pack",),
}


DEFAULT_ARTIFACT_PATHS: dict[str, str] = {
    "manifest": "data/baselines/real_world/manifest.json",
    "readiness": "data/research_readiness.json",
    "attribution_grid": "data/attribution_confound_grid.json",
    "null_calibration": "data/null_calibration.json",
    "replication_audit": "data/replication_audit.json",
    "baseline_acceptance": "data/baseline_acceptance.json",
    "baseline_promotion_plan": "data/baseline_promotion_plan.json",
    "collection_handoff": "data/collection_handoff.json",
    "collection_submission_contract": "data/collection_submission_contract.json",
    "collection_submission_lint": "data/collection_submission_lint.json",
    "collection_fixture_audit": "data/collection_fixture_audit.json",
    "collection_intake": "data/collection_intake.json",
    "feature_vectors": "data/feature_vectors.json",
    "classifier_report": "data/crypto_classifier_report.json",
    "collection_matrix": "data/collection_matrix.json",
    "collection_power": "data/collection_power.json",
    "provenance_requirements": "data/provenance_requirements.json",
    "provenance_audit": "data/provenance_audit.json",
    "project_evolution": "data/project_evolution.json",
    "snapshot_manifest": "data/snapshots/manifest.json",
    "evidence_pack": "data/evidence_pack.json",
    "claim_ledger": "data/claim_ledger.json",
}


def build_artifact_lineage(
    *,
    artifact_paths: dict[str, str | Path] | None = None,
    dependencies: dict[str, tuple[str, ...] | list[str]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    paths = dict(DEFAULT_ARTIFACT_PATHS)
    if artifact_paths:
        paths.update({role: str(path) for role, path in artifact_paths.items()})
    dependency_map = {role: tuple(values) for role, values in DEFAULT_DEPENDENCIES.items()}
    if dependencies:
        dependency_map.update({role: tuple(values) for role, values in dependencies.items()})

    nodes = [artifact_node(role, path) for role, path in sorted(paths.items())]
    node_by_role = {node["role"]: node for node in nodes}
    edges = [
        {"from": dependency, "to": role, "valid": dependency in node_by_role and role in node_by_role}
        for role, deps in sorted(dependency_map.items())
        for dependency in deps
    ]
    cycles = find_cycles({role: tuple(deps) for role, deps in dependency_map.items()})
    checksum_checks = evidence_pack_checksum_checks(node_by_role)
    missing_nodes = [node["role"] for node in nodes if not node["exists"]]
    checksum_mismatches = [check for check in checksum_checks if check["status"] == "mismatch"]
    invalid_edges = [edge for edge in edges if not edge["valid"]]

    return {
        "schema": ARTIFACT_LINEAGE_SCHEMA,
        "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "missing_count": len(missing_nodes),
            "invalid_edge_count": len(invalid_edges),
            "checksum_mismatch_count": len(checksum_mismatches),
            "cycle_count": len(cycles),
            "reproducible": not missing_nodes and not invalid_edges and not checksum_mismatches and not cycles,
        },
        "policy": {
            "lineage_is_outside_evidence_pack": True,
            "reason": "The lineage report audits the evidence pack and claim ledger, so it is generated after them to avoid circular checksums.",
            "publishable_unit": "schemas, checksums, dependency edges, and mismatch flags only",
        },
        "nodes": nodes,
        "edges": edges,
        "checksum_checks": checksum_checks,
        "cycles": cycles,
        "findings": lineage_findings(missing_nodes, invalid_edges, checksum_mismatches, cycles),
    }


def artifact_node(role: str, path_value: str | Path) -> dict[str, Any]:
    path = Path(path_value)
    if not path.exists():
        return {
            "role": role,
            "path": str(path).replace("\\", "/"),
            "exists": False,
            "schema": None,
            "sha256": None,
            "bytes": 0,
        }
    data = path.read_bytes()
    hash_bytes = data
    schema = None
    try:
        payload = json.loads(data.decode("utf-8"))
        if isinstance(payload, dict):
            schema = payload.get("schema")
            hash_bytes = canonical_json_bytes(payload)
    except (UnicodeDecodeError, json.JSONDecodeError):
        schema = None
    return {
        "role": role,
        "path": str(path).replace("\\", "/"),
        "exists": True,
        "schema": schema,
        "sha256": hashlib.sha256(hash_bytes).hexdigest(),
        "bytes": len(hash_bytes),
        "hash_policy": "canonical_json" if schema else "raw_bytes",
    }


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")


def evidence_pack_checksum_checks(nodes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    pack_node = nodes.get("evidence_pack")
    if not pack_node or not pack_node.get("exists"):
        return []
    try:
        pack = json.loads(Path(pack_node["path"]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    checks = []
    for artifact in pack.get("artifacts", []):
        role = artifact.get("role")
        node = nodes.get(role)
        expected = artifact.get("sha256")
        actual = node.get("sha256") if node else None
        if not node or not node.get("exists"):
            status = "missing"
        elif expected == actual:
            status = "match"
        else:
            status = "mismatch"
        checks.append(
            {
                "role": role,
                "status": status,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "schema": node.get("schema") if node else None,
            }
        )
    return checks


def find_cycles(graph: dict[str, tuple[str, ...]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in visiting:
            index = stack.index(node)
            cycle = stack[index:] + [node]
            if cycle not in cycles:
                cycles.append(cycle)
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, ()):
            visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)
    return cycles


def lineage_findings(
    missing_nodes: list[str],
    invalid_edges: list[dict[str, Any]],
    checksum_mismatches: list[dict[str, Any]],
    cycles: list[list[str]],
) -> list[dict[str, Any]]:
    findings = []
    if missing_nodes:
        findings.append(
            {
                "severity": "high",
                "check": "missing_lineage_artifact",
                "message": "One or more declared public artifacts are missing.",
                "evidence": {"roles": missing_nodes},
            }
        )
    if invalid_edges:
        findings.append(
            {
                "severity": "high",
                "check": "invalid_lineage_edge",
                "message": "One or more dependency edges points to an undeclared artifact role.",
                "evidence": {"edges": invalid_edges},
            }
        )
    if checksum_mismatches:
        findings.append(
            {
                "severity": "critical",
                "check": "evidence_pack_checksum_mismatch",
                "message": "The evidence pack records a checksum that does not match the current artifact.",
                "evidence": {"roles": [check["role"] for check in checksum_mismatches]},
            }
        )
    if cycles:
        findings.append(
            {
                "severity": "critical",
                "check": "lineage_cycle",
                "message": "Artifact dependencies contain a cycle; publish outputs in a separate post-pack audit instead.",
                "evidence": {"cycles": cycles},
            }
        )
    if not findings:
        findings.append(
            {
                "severity": "info",
                "check": "lineage_reproducible",
                "message": "Declared artifacts exist, evidence-pack checksums match, and dependency graph is acyclic.",
                "evidence": {},
            }
        )
    return findings
