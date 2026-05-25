from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from typing import Any

from .collection_lint import build_collection_submission_lint, lint_sort_key


COLLECTION_FIXTURE_AUDIT_SCHEMA = "primeproject.collection-fixture-audit.v1"


def build_collection_fixture_audit(*, contract: dict[str, Any]) -> dict[str, Any]:
    fixtures = build_submission_fixtures(contract)
    lint = build_collection_submission_lint(
        contract=contract,
        records=[fixture["record"] for fixture in fixtures],
    )
    lint_rows = {
        str(row.get("task_id")): row
        for row in lint.get("rows", [])
        if row.get("submitted")
    }
    rows = [
        fixture_audit_row(fixture, lint_rows.get(str(fixture["record"].get("task_id"))))
        for fixture in fixtures
    ]
    failed = [row for row in rows if not row["expectation_met"]]
    summary = {
        "fixture_count": len(rows),
        "passed_expectation_count": len(rows) - len(failed),
        "failed_expectation_count": len(failed),
        "expected_pass_count": sum(1 for row in rows if row["expected_status"] == "pass"),
        "expected_warning_count": sum(1 for row in rows if row["expected_status"] == "warning"),
        "expected_blocked_count": sum(1 for row in rows if row["expected_status"] == "blocked"),
        "actual_pass_count": sum(1 for row in rows if row["actual_status"] == "pass"),
        "actual_warning_count": sum(1 for row in rows if row["actual_status"] == "warning"),
        "actual_blocked_count": sum(1 for row in rows if row["actual_status"] == "blocked"),
        "public_safe_fixture_count": sum(1 for row in rows if row["public_safe"]),
    }
    return {
        "schema": COLLECTION_FIXTURE_AUDIT_SCHEMA,
        "source_schemas": {
            "collection_submission_contract": contract.get("schema"),
            "collection_submission_lint": lint.get("schema"),
        },
        "summary": summary,
        "quality_gate": {
            "status": "pass" if not failed and summary["public_safe_fixture_count"] == len(rows) else "fail",
            "message": quality_gate_message(failed),
        },
        "lint_summary": lint.get("summary", {}),
        "rows": rows,
    }


def build_submission_fixtures(contract: dict[str, Any]) -> list[dict[str, Any]]:
    templates = sorted(contract.get("task_templates", []), key=lint_sort_key)
    if not templates:
        return []

    fixtures = []
    cases = [
        ("valid_warning", 0, "warning", ["below_10pct_tv_floor"], make_warning_record),
        ("valid_ready", 1, "pass", [], make_ready_record),
        ("blocked_missing_feature", 2, "blocked", ["feature_vector_missing_features"], make_missing_feature_record),
        ("blocked_forbidden_field", 3, "blocked", ["forbidden_public_fields"], make_forbidden_record),
        ("blocked_provenance_identity", 4, "blocked", ["provenance_baseline_id_mismatch"], make_bad_provenance_record),
        ("blocked_feature_label", 5, "blocked", ["feature_vector_label_mismatch"], make_bad_feature_label_record),
        ("blocked_record_identity", 6, "blocked", ["record_baseline_id_mismatch"], make_bad_record_identity_record),
        ("blocked_reused_checksum_a", 7, "blocked", ["aggregate_artifact_sha256_reused"], make_reused_checksum_record),
        ("blocked_reused_checksum_b", 8, "blocked", ["aggregate_artifact_sha256_reused"], make_reused_checksum_record),
    ]
    for fixture_id, template_index, expected_status, expected_reasons, factory in cases:
        if template_index >= len(templates):
            continue
        template = templates[template_index]
        record = factory(template, fixture_id)
        fixtures.append(
            {
                "fixture_id": fixture_id,
                "task_id": record.get("task_id"),
                "library": template.get("library"),
                "object_type": template.get("object_type"),
                "bit_length": template.get("bit_length"),
                "expected_status": expected_status,
                "expected_reasons": expected_reasons,
                "public_safe": True,
                "record": record,
            }
        )
    return fixtures


def fixture_audit_row(fixture: dict[str, Any], lint_row: dict[str, Any] | None) -> dict[str, Any]:
    lint_row = lint_row or {}
    actual_reasons = [
        *[str(reason) for reason in lint_row.get("blocking_reasons", [])],
        *[str(reason) for reason in lint_row.get("warning_reasons", [])],
    ]
    expected_reasons = list(fixture.get("expected_reasons") or [])
    missing_reasons = [reason for reason in expected_reasons if reason not in actual_reasons]
    actual_status = str(lint_row.get("status") or "missing")
    expectation_met = actual_status == fixture.get("expected_status") and not missing_reasons
    return {
        "fixture_id": fixture.get("fixture_id"),
        "task_id": fixture.get("task_id"),
        "library": fixture.get("library"),
        "object_type": fixture.get("object_type"),
        "bit_length": fixture.get("bit_length"),
        "expected_status": fixture.get("expected_status"),
        "actual_status": actual_status,
        "expected_reasons": expected_reasons,
        "actual_reasons": actual_reasons,
        "missing_expected_reasons": missing_reasons,
        "expectation_met": expectation_met,
        "public_safe": bool(fixture.get("public_safe")),
    }


def make_warning_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    sample_count = int(template.get("planned_sample_target") or 0)
    record["sample_count"] = sample_count
    record["feature_vector_summary"]["record_count"] = sample_count
    record["feature_vector_summary"]["features"]["record_count_log2"] = sample_count.bit_length() - 1
    return record


def make_ready_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    return base_record(template, fixture_id)


def make_missing_feature_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    features = dict(record["feature_vector_summary"].get("features") or {})
    features.pop("residue_tv_210", None)
    record["feature_vector_summary"]["features"] = features
    return record


def make_forbidden_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    record["private_prime"] = "<redacted-fixture-marker>"
    return record


def make_bad_provenance_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    provenance = dict(record.get("provenance_record") or {})
    provenance["baseline_id"] = f"{template.get('baseline_id')}-wrong"
    record["provenance_record"] = provenance
    return record


def make_bad_feature_label_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    summary = dict(record.get("feature_vector_summary") or {})
    summary["label"] = f"{template.get('library')}-wrong"
    record["feature_vector_summary"] = summary
    return record


def make_bad_record_identity_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    record["baseline_id"] = f"{template.get('baseline_id')}-wrong"
    return record


def make_reused_checksum_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = base_record(template, fixture_id)
    record["aggregate_artifact_sha256"] = sha256(b"primeproject-fixture:reused-checksum").hexdigest()
    return record


def base_record(template: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    record = deepcopy(template.get("submission_record_template") or {})
    sample_count = int(template.get("target_samples_for_10pct_tv") or template.get("planned_sample_target") or 0)
    if not record:
        record = {
            "task_id": template.get("task_id"),
            "sample_count": sample_count,
            "claim_scope": "real_world",
            "provenance_record": {},
            "feature_vector_path": "",
            "feature_vector_summary": {"features": {}},
        }
    record["task_id"] = template.get("task_id")
    record["sample_count"] = sample_count
    record["claim_scope"] = "real_world"
    record["aggregate_artifact_sha256"] = sha256(
        f"primeproject-fixture:{template.get('task_id')}:{fixture_id}".encode("utf-8")
    ).hexdigest()
    provenance = dict(record.get("provenance_record") or {})
    provenance.setdefault("baseline_id", template.get("baseline_id"))
    provenance.setdefault("library", template.get("library"))
    provenance.setdefault("source_commit", "fixture-public-commit")
    provenance.setdefault("build_config", "fixture-public-build")
    provenance.setdefault("rng_source", "fixture-public-rng")
    provenance.setdefault("generation_command", "fixture-public-command")
    record["provenance_record"] = provenance
    record["feature_vector_path"] = f"data/fixtures/{str(template.get('task_id')).replace(':', '_')}.{fixture_id}.json"
    summary = dict(record.get("feature_vector_summary") or {})
    summary["record_count"] = sample_count
    summary["label"] = str(template.get("library") or template.get("baseline_id") or "fixture")
    features = dict(summary.get("features") or {})
    features["bit_length_mean"] = float(template.get("bit_length") or features.get("bit_length_mean") or 0.0)
    features["record_count_log2"] = sample_count.bit_length() - 1 if sample_count > 0 else 0.0
    summary["features"] = features
    record["feature_vector_summary"] = summary
    return record


def quality_gate_message(failed: list[dict[str, Any]]) -> str:
    if not failed:
        return "Submission lint behavior matches all public-safe fixture expectations."
    return "One or more fixture expectations failed; update lint logic or fixture expectations before using collector submissions."
