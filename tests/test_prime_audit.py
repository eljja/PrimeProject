from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from random import Random

from prime_audit.analysis import audit_records, evaluate_policy, report_to_dict
from prime_audit.artifact_lineage import build_artifact_lineage
from prime_audit.attribution import (
    build_bit_length_bucket_plan,
    run_attribution_confound_grid,
    run_synthetic_attribution_benchmark,
    sample_generator_records,
)
from prime_audit.baseline_acceptance import build_baseline_acceptance
from prime_audit.baseline_promotion import build_baseline_promotion_plan
from prime_audit.baselines import (
    ABLATION_COMPONENT_WEIGHTS,
    build_generator_baseline,
    compare_fingerprint_to_baselines,
    sample_quality,
)
from prime_audit.bitcoin import audit_bitcoin_signatures, parse_der_signature, secp256k1_constants_report
from prime_audit.bitcoin_integration import build_bitcoin_generator_risk_report
from prime_audit.catalog import classify_public_prime
from prime_audit.claim_ledger import build_claim_ledger
from prime_audit.collection_matrix import build_collection_matrix
from prime_audit.collection_power import build_collection_power
from prime_audit.conjecture_lab import build_observations, run_lab, summarize_measure
from prime_audit.crypto_classifier import run_crypto_classifier
from prime_audit.decision_protocol import build_decision_protocol
from prime_audit.evidence_pack import build_evidence_pack
from prime_audit.feature_vectors import (
    build_feature_vector_payload,
    feature_vector_from_fingerprint,
)
from prime_audit.fingerprints import analyze_prime_generator_fingerprints, prime_gap_context
from prime_audit.io import load_records
from prime_audit.models import KeyRecord
from prime_audit.provenance import build_provenance_audit, build_provenance_requirements
from prime_audit.real_baselines import build_real_baseline_manifest, manifest_public_summary
from prime_audit.research_readiness import build_research_readiness_report
from prime_audit.bias_lab import build_residue_factors, rank_next_prime_candidates
from prime_audit.simulators import (
    add_standard_public_primes,
    generate_synthetic_rsa_dataset,
    records_to_jsonable,
)
from prime_audit.snapshots import build_snapshot, render_snapshot_svgs


class PrimeAuditTests(unittest.TestCase):
    def test_synthetic_dataset_flags_shared_and_near_square_keys(self) -> None:
        records = generate_synthetic_rsa_dataset(bits=128, seed=17)
        report = audit_records(records, fermat_max_steps=100_000)
        checks = {finding.check for finding in report.findings}

        self.assertIn("shared_prime_factor", checks)
        self.assertIn("near_square_factorization", checks)

    def test_standard_public_prime_recognition(self) -> None:
        classification = classify_public_prime(2**255 - 19)

        self.assertEqual(classification["recognized_parameter"], "curve25519-field")
        self.assertTrue(classification["is_probable_prime"])

    def test_json_round_trip(self) -> None:
        records = add_standard_public_primes(generate_synthetic_rsa_dataset(bits=128, seed=99))
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "records.json"
            path.write_text(json.dumps(records_to_jsonable(records)), encoding="utf-8")

            loaded = load_records(path)
            report_dict = report_to_dict(audit_records(loaded))

        self.assertEqual(len(loaded), len(records))
        self.assertGreaterEqual(report_dict["summary"]["critical"], 1)
        self.assertGreaterEqual(report_dict["summary"]["info"], 1)

    def test_loads_rsa_key_material_from_pem_der_and_csr(self) -> None:
        modulus = 3233
        exponent = 17
        pkcs1 = der_sequence(der_integer(modulus), der_integer(exponent))
        spki = der_subject_public_key_info(pkcs1)
        csr = der_sequence(
            der_sequence(
                der_integer(0),
                der_sequence(),
                spki,
                der_tlv(0xA0, b""),
            )
        )
        pem = (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            f"{base64_lines(pkcs1)}\n"
            "-----END RSA PUBLIC KEY-----\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pem_path = tmp / "sample.pem"
            der_path = tmp / "sample.der"
            csr_path = tmp / "sample.csr"
            pem_path.write_text(pem, encoding="ascii")
            der_path.write_bytes(spki)
            csr_path.write_bytes(csr)

            pem_record = load_records(pem_path)[0]
            der_record = load_records(der_path)[0]
            csr_record = load_records(csr_path)[0]

        self.assertEqual((pem_record.value, pem_record.public_exponent), (modulus, exponent))
        self.assertEqual((der_record.value, der_record.public_exponent), (modulus, exponent))
        self.assertEqual((csr_record.value, csr_record.public_exponent), (modulus, exponent))

    def test_next_prime_measure_weights_by_left_gap(self) -> None:
        observations = build_observations(100)
        by_prime = {observation.prime: observation for observation in observations}

        self.assertEqual(by_prime[11].next_prime_weight, 4)
        self.assertEqual(by_prime[13].next_prime_weight, 2)
        self.assertGreater(by_prime[11].next_prime_weight, by_prime[13].next_prime_weight)

    def test_gap_lab_reports_generator_summaries(self) -> None:
        payload = run_lab(1000, modulo=30)
        observations = build_observations(1000)
        rejection = summarize_measure(observations, generator="rejection", modulo=30)
        next_prime = summarize_measure(observations, generator="next_prime", modulo=30)

        self.assertIn("next_prime", payload["summaries"])
        self.assertGreater(next_prime.weighted_mean_gap, rejection.weighted_mean_gap)

    def test_snapshot_is_compact_and_renders_svgs(self) -> None:
        snapshot = build_snapshot(1000, modulo=30, bins=12)

        self.assertEqual(snapshot["schema"], "primeproject.snapshot.v1")
        self.assertNotIn("observations", snapshot)
        self.assertIn("gap_histogram", snapshot["generators"]["next_prime"])

        with tempfile.TemporaryDirectory() as tmpdir:
            paths = render_snapshot_svgs(snapshot, tmpdir, "test_snapshot")

        self.assertEqual(len(paths), 3)

    def test_bias_lab_ranks_actual_next_prime_candidate(self) -> None:
        payload = rank_next_prime_candidates(1000, span=80, modulo=30, top=10)

        self.assertEqual(payload["schema"], "primeproject.generator-bias-ranking.v1")
        self.assertEqual(payload["actual_next_prime"], 1009)
        self.assertIsNotNone(payload["rank_of_actual"])
        self.assertGreater(payload["candidates_scored"], 0)
        self.assertIn("score", payload["top_candidates"][0])

    def test_audit_policy_fails_at_configured_threshold(self) -> None:
        records = generate_synthetic_rsa_dataset(bits=128, seed=17)
        report = audit_records(records, fermat_max_steps=100_000)

        strict_policy = evaluate_policy(report.findings, fail_on="high")
        lenient_policy = evaluate_policy(report.findings, fail_on="none")

        self.assertFalse(strict_policy["passed"])
        self.assertGreater(strict_policy["blocking_findings"], 0)
        self.assertTrue(lenient_policy["passed"])

    def test_residue_factors_are_positive_for_coprime_classes(self) -> None:
        factors = build_residue_factors(2000, modulo=30)

        self.assertEqual(set(factors), {1, 7, 11, 13, 17, 19, 23, 29})
        self.assertTrue(all(value > 0 for value in factors.values()))

    def test_bitcoin_constants_are_prime_parameters(self) -> None:
        report = secp256k1_constants_report()

        self.assertEqual(report["curve"], "secp256k1")
        self.assertEqual(report["field_prime_p"]["bit_length"], 256)
        self.assertTrue(report["field_prime_p"]["is_probable_prime"])
        self.assertTrue(report["group_order_n"]["is_probable_prime"])

    def test_bitcoin_signature_audit_flags_reused_r_without_key_recovery(self) -> None:
        report = audit_bitcoin_signatures(
            [
                {"signature_id": "a", "public_key": "02aa", "r": "0x1234", "s": "0x20"},
                {"signature_id": "b", "public_key": "02aa", "r": "0x1234", "s": "0x21"},
            ]
        )

        checks = {finding["check"] for finding in report["findings"]}
        self.assertIn("reused_r", checks)
        self.assertNotIn("private_key", json.dumps(report))

    def test_bitcoin_der_signature_parser_accepts_sighash_byte(self) -> None:
        r, s, sighash = parse_der_signature("300602010102010201")

        self.assertEqual((r, s, sighash), (1, 2, 1))

    def test_prime_generator_fingerprint_extracts_gap_and_residue_signals(self) -> None:
        records = [
            *[
                KeyRecord(
                    key_id=f"toy-{index}",
                    algorithm="prime",
                    value=value,
                    source="unit-test",
                )
                for index, value in enumerate([101, 103, 107, 109, 113, 127, 131, 137])
            ],
        ]
        report = analyze_prime_generator_fingerprints(records, gap_max_steps=64)

        self.assertEqual(report["schema"], "primeproject.generator-fingerprint.v1")
        self.assertEqual(report["record_count"], 8)
        self.assertIn("210", report["aggregate"]["residue_total_variation"])
        self.assertGreater(report["aggregate"]["gap_statistics"]["covered_records"], 0)

    def test_prime_gap_context_finds_neighbors_without_exposing_secret_material(self) -> None:
        context = prime_gap_context(101, max_steps=32)

        self.assertEqual(context["previous_prime"], 97)
        self.assertEqual(context["next_prime"], 103)
        self.assertEqual(context["left_gap"], 4)

    def test_generator_baseline_comparison_ranks_nearest_profile(self) -> None:
        target = fingerprint_report_from_values([101, 103, 107, 109, 113, 127, 131, 137])
        nearby = fingerprint_report_from_values([139, 149, 151, 157, 163, 167, 173, 179])
        distant = fingerprint_report_from_values([257, 263, 269, 271, 277, 281, 283, 293])
        nearby_baseline = build_generator_baseline(nearby, name="nearby-toy")
        distant_baseline = build_generator_baseline(distant, name="distant-toy")

        comparison = compare_fingerprint_to_baselines(target, [distant_baseline, nearby_baseline])

        self.assertEqual(comparison["schema"], "primeproject.generator-baseline-comparison.v1")
        self.assertEqual(comparison["nearest_baseline"]["baseline_name"], "nearby-toy")
        self.assertIn("confidence", comparison["nearest_baseline"])
        self.assertIn("target_quality", comparison)
        self.assertEqual(len(comparison["comparisons"]), 2)

    def test_generator_baseline_comparison_reports_missing_baselines(self) -> None:
        target = fingerprint_report_from_values([101, 103, 107])
        comparison = compare_fingerprint_to_baselines(target, [])

        self.assertEqual(comparison["findings"][0]["check"], "missing_baselines")

    def test_baseline_sample_quality_marks_small_samples_as_low_confidence(self) -> None:
        report = fingerprint_report_from_values([101, 103, 107])
        quality = sample_quality(report)
        baseline = build_generator_baseline(report, name="tiny")
        comparison = compare_fingerprint_to_baselines(report, [baseline])

        self.assertLess(quality["overall_confidence"], 0.35)
        self.assertEqual(comparison["findings"][0]["check"], "low_confidence_baseline_match")

    def test_synthetic_attribution_benchmark_reports_confusion_matrix(self) -> None:
        result = run_synthetic_attribution_benchmark(
            limit=5000,
            train_count=16,
            test_count=8,
            trials=1,
            seed=7,
            gap_max_steps=64,
        )

        self.assertEqual(result["schema"], "primeproject.synthetic-attribution-benchmark.v1")
        self.assertEqual(result["total"], 3)
        self.assertIn("rejection", result["confusion_matrix"])
        self.assertIn("residue_only", result["ablation"])
        self.assertIn("gap_only", result["ablation"])
        self.assertEqual(len(result["trials_detail"]), 3)

    def test_synthetic_attribution_benchmark_can_control_bit_length(self) -> None:
        result = run_synthetic_attribution_benchmark(
            limit=5000,
            train_count=16,
            test_count=8,
            trials=1,
            seed=7,
            gap_max_steps=64,
            control_mode="bit_length",
        )

        self.assertEqual(result["control"]["mode"], "bit_length")
        self.assertGreater(len(result["control"]["train_bit_length_plan"]), 0)
        self.assertGreater(len(result["control"]["test_bit_length_plan"]), 0)
        self.assertIn("bit_length_only", result["ablation"])

    def test_attribution_confound_grid_reports_paired_deltas(self) -> None:
        result = run_attribution_confound_grid(
            limits=[5000],
            train_counts=[16],
            test_counts=[8],
            trials=1,
            repeats=2,
            seed=7,
            gap_max_steps=64,
        )

        self.assertEqual(result["schema"], "primeproject.attribution-confound-grid.v1")
        self.assertEqual(result["repeats"], 2)
        self.assertEqual(len(result["rows"]), 4)
        self.assertGreater(len(result["deltas"]), 0)
        self.assertIn("profiles", result["summary"])
        bit_length = result["summary"]["profiles"]["bit_length_only"]
        self.assertIn("controlled_accuracy", bit_length)
        self.assertIn("ci95_low", bit_length["controlled_accuracy"])
        self.assertIn("controlled_significance", bit_length)
        self.assertIn("p_value", bit_length["controlled_significance"])
        self.assertIn("robust_interpretation", bit_length)

    def test_baseline_comparison_accepts_ablation_weights(self) -> None:
        target = fingerprint_report_from_values([101, 103, 107, 109, 113, 127, 131, 137])
        baseline = build_generator_baseline(target, name="self")
        comparison = compare_fingerprint_to_baselines(
            target,
            [baseline],
            component_weights=ABLATION_COMPONENT_WEIGHTS["residue_only"],
            profile_name="residue_only",
        )

        self.assertEqual(comparison["profile_name"], "residue_only")
        self.assertEqual(comparison["component_weights"], {"residue_tv": 1.0})
        self.assertEqual(comparison["nearest_baseline"]["distance"], 0.0)

    def test_generator_sampling_returns_unique_prime_records(self) -> None:
        observations = build_observations(1000)
        records = sample_generator_records(
            observations,
            generator="next_prime",
            count=12,
            rng=Random(11),
            key_prefix="sample",
        )

        self.assertEqual(len(records), 12)
        self.assertEqual(len({record.value for record in records}), 12)

    def test_generator_sampling_can_follow_bit_length_plan(self) -> None:
        observations = build_observations(1000)
        plan = build_bit_length_bucket_plan(observations, 20)
        records = sample_generator_records(
            observations,
            generator="wheel30_next",
            count=20,
            rng=Random(11),
            key_prefix="controlled",
            bit_length_bucket_plan=plan,
        )
        observed_plan: dict[int, int] = {}
        for record in records:
            bit_length = record.value.bit_length()
            observed_plan[bit_length] = observed_plan.get(bit_length, 0) + 1

        self.assertEqual(observed_plan, plan)

    def test_real_baseline_manifest_tracks_planned_and_available_entries(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        summary = manifest_public_summary(manifest)

        self.assertEqual(manifest["schema"], "primeproject.real-world-baseline-manifest.v1")
        self.assertTrue(manifest["validation"]["passed"])
        self.assertGreaterEqual(summary["planned_count"], 3)
        self.assertIn("OpenSSL", summary["libraries"])
        self.assertFalse(manifest["handling_policy"]["publish_private_primes"])

    def test_collection_matrix_defines_real_world_sample_targets(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        matrix = build_collection_matrix(manifest)

        self.assertEqual(matrix["schema"], "primeproject.real-world-collection-matrix.v1")
        self.assertEqual(matrix["target_count"], 10)
        self.assertEqual(matrix["row_count"], 4)
        self.assertEqual(matrix["blocked_target_count"], 10)
        self.assertEqual(matrix["local_sensitive_count"], 3)
        self.assertEqual(matrix["claim_gate"]["status"], "blocked")
        rsa_rows = [row for row in matrix["rows"] if row["track"] == "rsa-prime-generation"]
        self.assertEqual({target["bit_length"] for row in rsa_rows for target in row["targets"]}, {2048, 3072, 4096})
        self.assertEqual(matrix["sample_handling"]["raw_private_material_public"], False)
        self.assertGreaterEqual(len(matrix["next_unlock"]), 2)

        manifest["entries"][0]["status"] = "available"
        manifest["entries"][0]["sample_count"] = 500
        manifest["entries"][0]["bit_length"] = None
        unspecified = build_collection_matrix(manifest)
        self.assertEqual(unspecified["complete_target_count"], 0)

        manifest["entries"][0]["bit_length"] = 2048
        matched = build_collection_matrix(manifest)
        self.assertEqual(matched["complete_target_count"], 1)

    def test_collection_power_marks_rsa_targets_as_coarse_screening(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        matrix = build_collection_matrix(manifest)
        power = build_collection_power(matrix)

        self.assertEqual(power["schema"], "primeproject.collection-power.v1")
        self.assertEqual(power["summary"]["target_count"], 10)
        self.assertEqual(power["summary"]["coarse_count"], 9)
        self.assertEqual(power["summary"]["strong_count"], 1)
        rsa_rows = [row for row in power["rows"] if row["object_type"] == "rsa-prime"]
        self.assertTrue(all(row["bucket_count"] == 48 for row in rsa_rows))
        self.assertTrue(all(row["min_samples_for_10pct_tv"] > row["sample_target"] for row in rsa_rows))
        signature = next(row for row in power["rows"] if row["object_type"] == "ecdsa-signature")
        self.assertEqual(signature["power_tier"], "strong")
        self.assertGreaterEqual(len(power["recommendations"]), 1)

    def test_provenance_requirements_block_incomplete_real_baselines(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        requirements = build_provenance_requirements(manifest)

        self.assertEqual(requirements["schema"], "primeproject.provenance-requirements.v1")
        self.assertEqual(requirements["row_count"], 4)
        self.assertEqual(requirements["claim_gate"]["status"], "blocked")
        self.assertGreater(requirements["missing_required_count"], 0)
        openssl = next(row for row in requirements["rows"] if row["baseline_id"] == "openssl-rsa-prime-owned")
        self.assertIn("collector", openssl["missing_required_fields"])
        self.assertIn("aggregate_artifact_sha256", openssl["missing_required_fields"])
        self.assertNotIn("raw_material_policy", openssl["missing_required_fields"])

    def test_provenance_audit_blocks_missing_metadata(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        requirements = build_provenance_requirements(manifest)
        audit = build_provenance_audit(requirements)

        self.assertEqual(audit["schema"], "primeproject.provenance-audit.v1")
        self.assertEqual(audit["row_count"], 4)
        self.assertEqual(audit["blocked_count"], 4)
        self.assertEqual(audit["claim_gate"]["status"], "blocked")
        self.assertGreater(audit["summary"]["total_missing_required"], 0)

    def test_provenance_audit_reports_forbidden_field_names_without_values(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        requirements = build_provenance_requirements(manifest)
        complete = complete_provenance_record("openssl-rsa-prime-owned")
        complete["nested"] = {"private_key": "do-not-leak"}
        audit = build_provenance_audit(requirements, [complete])
        row = next(item for item in audit["rows"] if item["baseline_id"] == "openssl-rsa-prime-owned")

        self.assertEqual(row["status"], "blocked")
        self.assertIn("nested.private_key", row["forbidden_public_fields"])
        self.assertNotIn("do-not-leak", json.dumps(audit))

    def test_provenance_audit_passes_complete_public_safe_record(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        requirements = build_provenance_requirements(manifest)
        audit = build_provenance_audit(requirements, [complete_provenance_record("openssl-rsa-prime-owned")])
        row = next(item for item in audit["rows"] if item["baseline_id"] == "openssl-rsa-prime-owned")

        self.assertEqual(row["status"], "pass")
        self.assertEqual(row["missing_required_fields"], [])
        self.assertEqual(row["invalid_fields"], [])

    def test_baseline_acceptance_blocks_uncollected_targets(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        matrix = build_collection_matrix(manifest)
        power = build_collection_power(matrix)
        audit = build_provenance_audit(build_provenance_requirements(manifest))
        acceptance = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_audit=audit,
        )

        self.assertEqual(acceptance["schema"], "primeproject.baseline-acceptance.v1")
        self.assertEqual(acceptance["row_count"], 10)
        self.assertEqual(acceptance["accepted_count"], 0)
        self.assertEqual(acceptance["blocked_count"], 10)
        self.assertEqual(acceptance["claim_gate"]["status"], "blocked")
        self.assertIn("provenance_not_passed", {item["reason"] for item in acceptance["summary"]["dominant_blockers"]})

    def test_baseline_acceptance_distinguishes_screening_from_accepted(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        manifest["entries"][0]["status"] = "available"
        manifest["entries"][0]["bit_length"] = 2048
        manifest["entries"][0]["sample_count"] = 500
        matrix = build_collection_matrix(manifest)
        power = build_collection_power(matrix)
        audit = build_provenance_audit(
            build_provenance_requirements(manifest),
            [complete_provenance_record("openssl-rsa-prime-owned")],
        )
        acceptance = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_audit=audit,
        )
        openssl = next(row for row in acceptance["rows"] if row["baseline_id"] == "openssl-rsa-prime-owned" and row["bit_length"] == 2048)

        self.assertEqual(openssl["acceptance"], "screening_only")
        self.assertEqual(openssl["blocking_reasons"], [])

        for target in matrix["rows"][0]["targets"]:
            if target["bit_length"] == 2048:
                target["sample_target"] = 5000
        stronger_power = build_collection_power(matrix)
        stronger = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=stronger_power,
            provenance_audit=audit,
        )
        promoted = next(row for row in stronger["rows"] if row["baseline_id"] == "openssl-rsa-prime-owned" and row["bit_length"] == 2048)
        self.assertEqual(promoted["acceptance"], "accepted")

    def test_baseline_promotion_plan_selects_minimal_rsa_unlock_path(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        matrix = build_collection_matrix(manifest)
        power = build_collection_power(matrix)
        audit = build_provenance_audit(build_provenance_requirements(manifest))
        acceptance = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_audit=audit,
        )
        plan = build_baseline_promotion_plan(acceptance=acceptance, power=power)

        self.assertEqual(plan["schema"], "primeproject.baseline-promotion-plan.v1")
        self.assertEqual(plan["summary"]["minimal_unlock_target_count"], 2)
        self.assertEqual([row["library"] for row in plan["minimal_unlock_targets"]], ["OpenSSL", "BoringSSL"])
        self.assertEqual([row["bit_length"] for row in plan["minimal_unlock_targets"]], [2048, 2048])
        self.assertEqual(plan["summary"]["projected_samples_for_minimal_unlock"], 9028)
        self.assertEqual(plan["summary"]["dominant_next_step"], "complete_provenance_record")

    def test_baseline_promotion_plan_marks_accepted_targets_ready(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        manifest["entries"][0]["status"] = "available"
        manifest["entries"][0]["bit_length"] = 2048
        manifest["entries"][0]["sample_count"] = 5000
        matrix = build_collection_matrix(manifest)
        for target in matrix["rows"][0]["targets"]:
            if target["bit_length"] == 2048:
                target["sample_target"] = 5000
        power = build_collection_power(matrix)
        audit = build_provenance_audit(
            build_provenance_requirements(manifest),
            [complete_provenance_record("openssl-rsa-prime-owned")],
        )
        acceptance = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_audit=audit,
        )
        plan = build_baseline_promotion_plan(acceptance=acceptance, power=power)
        openssl = next(row for row in plan["rows"] if row["baseline_id"] == "openssl-rsa-prime-owned" and row["bit_length"] == 2048)

        self.assertEqual(openssl["promotion_state"], "ready")
        self.assertEqual(openssl["next_step"], "ready_for_claim_gate")

    def test_feature_vectors_and_classifier_report_label_accuracy(self) -> None:
        alpha_a = feature_vector_from_fingerprint(
            fingerprint_report_from_values([101, 103, 107, 109, 113, 127, 131, 137]),
            vector_id="alpha-a",
            label="alpha",
        )
        alpha_b = feature_vector_from_fingerprint(
            fingerprint_report_from_values([139, 149, 151, 157, 163, 167, 173, 179]),
            vector_id="alpha-b",
            label="alpha",
        )
        beta_a = feature_vector_from_fingerprint(
            fingerprint_report_from_values([1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049]),
            vector_id="beta-a",
            label="beta",
        )
        beta_b = feature_vector_from_fingerprint(
            fingerprint_report_from_values([2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063]),
            vector_id="beta-b",
            label="beta",
        )
        payload = build_feature_vector_payload([alpha_a, alpha_b, beta_a, beta_b])
        report = run_crypto_classifier(payload, feature_space="interaction")

        self.assertEqual(payload["schema"], "primeproject.generator-feature-vectors.v1")
        self.assertEqual(report["schema"], "primeproject.crypto-classifier-report.v1")
        self.assertEqual(report["total"], 4)
        self.assertIn("nearest-centroid", report["model"]["family"])

    def test_bitcoin_generator_risk_report_links_signature_audit_to_manifest(self) -> None:
        audit = audit_bitcoin_signatures(
            [
                {"signature_id": "a", "public_key": "02aa", "r": "0x1234", "s": "0x20"},
                {"signature_id": "b", "public_key": "02aa", "r": "0x1234", "s": "0x21"},
            ]
        )
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        report = build_bitcoin_generator_risk_report(audit, manifest)

        self.assertEqual(report["schema"], "primeproject.bitcoin-generator-risk-report.v1")
        self.assertEqual(report["risk_level"], "critical")
        self.assertGreater(len(report["related_baselines"]), 0)
        self.assertGreater(len(report["research_actions"]), 0)

    def test_research_readiness_report_surfaces_blocking_gaps(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        grid = run_attribution_confound_grid(
            limits=[5000],
            train_counts=[16],
            test_counts=[8],
            trials=1,
            repeats=1,
            seed=7,
            gap_max_steps=64,
            include_ablation=False,
        )
        readiness = build_research_readiness_report(
            manifest=manifest,
            attribution_grid=grid,
        )

        self.assertEqual(readiness["schema"], "primeproject.research-readiness.v1")
        self.assertIn("sim_to_real", readiness["dimensions"])
        self.assertGreater(len(readiness["blocking_gaps"]), 0)
        self.assertGreater(len(readiness["next_actions"]), 0)
        self.assertLess(readiness["overall"]["score"], 0.8)

    def test_evidence_pack_limits_claims_when_gates_fail(self) -> None:
        manifest = build_real_baseline_manifest(created_at="2026-05-22T00:00:00+00:00")
        readiness = build_research_readiness_report(manifest=manifest)
        pack = build_evidence_pack(
            manifest=manifest,
            readiness=readiness,
            generated_at="2026-05-22T00:00:00+00:00",
            file_paths={"missing-extra": "does-not-exist.json"},
        )

        self.assertEqual(pack["schema"], "primeproject.evidence-pack.v1")
        self.assertEqual(pack["claim_level"]["level"], "public_demo_only")
        self.assertEqual(pack["artifact_count"], 1)
        failed = {gate["code"] for gate in pack["publication_gates"] if not gate["passed"]}
        self.assertIn("real_baseline_gate", failed)
        self.assertIn("classifier_gate", failed)
        self.assertIn("provenance_gate", failed)
        self.assertIn("provenance_audit_gate", failed)
        self.assertIn("baseline_acceptance_gate", failed)
        self.assertIn("promotion_plan_gate", failed)
        self.assertGreaterEqual(len(pack["local_collection_protocols"]), 3)

    def test_claim_ledger_blocks_unsupported_real_world_claims(self) -> None:
        evidence = {
            "schema": "primeproject.evidence-pack.v1",
            "claim_level": {
                "level": "public_demo_only",
                "failed_gate_count": 3,
            },
            "publication_gates": [
                {"code": "sensitive_publication_gate", "passed": True, "severity": "critical"},
                {"code": "real_baseline_gate", "passed": False, "severity": "high"},
                {"code": "controlled_signal_gate", "passed": True, "severity": "high"},
                {"code": "classifier_gate", "passed": False, "severity": "high"},
                {"code": "bitcoin_integration_gate", "passed": False, "severity": "medium"},
                {"code": "reproducibility_gate", "passed": True, "severity": "medium"},
                {"code": "provenance_gate", "passed": True, "severity": "medium"},
                {"code": "provenance_audit_gate", "passed": True, "severity": "medium"},
                {"code": "baseline_acceptance_gate", "passed": False, "severity": "high"},
                {"code": "promotion_plan_gate", "passed": True, "severity": "medium"},
            ],
            "artifacts": [
                {"role": "attribution_grid", "exists": True, "sha256": "a" * 64},
                {"role": "baseline_acceptance", "exists": True, "sha256": "b" * 64},
                {"role": "manifest", "exists": True, "sha256": "c" * 64},
                {"role": "project_evolution", "exists": True, "sha256": "d" * 64},
                {"role": "readiness", "exists": True, "sha256": "e" * 64},
                {"role": "snapshot_manifest", "exists": True, "sha256": "f" * 64},
            ],
        }

        ledger = build_claim_ledger(evidence, generated_at="2026-05-23T00:00:00+00:00")
        claims = {claim["claim_id"]: claim for claim in ledger["claims"]}

        self.assertEqual(ledger["schema"], "primeproject.claim-ledger.v1")
        self.assertEqual(claims["synthetic_generator_attribution"]["status"], "allowed")
        self.assertEqual(claims["real_world_generator_attribution"]["status"], "blocked")
        self.assertIn(
            "real_baseline_gate",
            claims["real_world_generator_attribution"]["failed_required_gates"],
        )
        self.assertEqual(claims["bitcoin_nonce_risk_attribution"]["status"], "blocked")
        self.assertIn("bitcoin_risk_report", claims["bitcoin_nonce_risk_attribution"]["missing_required_artifacts"])
        self.assertGreaterEqual(ledger["summary"]["blocked_count"], 2)

    def test_artifact_lineage_detects_checksum_mismatch_and_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest = tmp / "manifest.json"
            readiness = tmp / "readiness.json"
            evidence = tmp / "evidence.json"
            manifest.write_text(json.dumps({"schema": "manifest.v1"}), encoding="utf-8")
            readiness.write_text(json.dumps({"schema": "readiness.v1"}), encoding="utf-8")
            evidence.write_text(
                json.dumps(
                    {
                        "schema": "primeproject.evidence-pack.v1",
                        "artifacts": [
                            {"role": "manifest", "sha256": "0" * 64},
                            {
                                "role": "readiness",
                                "sha256": sha256_text(readiness.read_text(encoding="utf-8")),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            lineage = build_artifact_lineage(
                artifact_paths={
                    "manifest": manifest,
                    "readiness": readiness,
                    "evidence_pack": evidence,
                },
                dependencies={
                    "manifest": ["evidence_pack"],
                    "evidence_pack": ["manifest"],
                },
                generated_at="2026-05-23T00:00:00+00:00",
            )

        self.assertEqual(lineage["schema"], "primeproject.artifact-lineage.v1")
        self.assertEqual(lineage["summary"]["checksum_mismatch_count"], 1)
        self.assertGreaterEqual(lineage["summary"]["cycle_count"], 1)
        self.assertFalse(lineage["summary"]["reproducible"])
        checks = {check["role"]: check["status"] for check in lineage["checksum_checks"]}
        self.assertEqual(checks["manifest"], "mismatch")
        self.assertEqual(checks["readiness"], "match")

    def test_decision_protocol_blocks_claim_promotion_until_gates_pass(self) -> None:
        evidence = {
            "schema": "primeproject.evidence-pack.v1",
            "claim_level": {"level": "public_demo_only"},
            "publication_gates": [
                {"code": "sensitive_publication_gate", "passed": True, "severity": "critical"},
                {"code": "reproducibility_gate", "passed": True, "severity": "medium"},
                {"code": "controlled_signal_gate", "passed": True, "severity": "high"},
                {"code": "real_baseline_gate", "passed": False, "severity": "high"},
                {"code": "classifier_gate", "passed": False, "severity": "high"},
                {"code": "provenance_gate", "passed": True, "severity": "medium"},
                {"code": "provenance_audit_gate", "passed": True, "severity": "medium"},
                {"code": "baseline_acceptance_gate", "passed": False, "severity": "high"},
                {"code": "bitcoin_integration_gate", "passed": False, "severity": "medium"},
            ],
            "artifacts": [
                {"role": "snapshot_manifest", "exists": True, "sha256": "a" * 64},
                {"role": "attribution_grid", "exists": True, "sha256": "b" * 64},
                {"role": "manifest", "exists": True, "sha256": "c" * 64},
                {"role": "readiness", "exists": True, "sha256": "d" * 64},
                {"role": "baseline_acceptance", "exists": True, "sha256": "e" * 64},
            ],
        }
        claim_ledger = {
            "schema": "primeproject.claim-ledger.v1",
            "claims": [
                {"claim_id": "prime_measure_visualization", "status": "allowed"},
                {"claim_id": "synthetic_generator_attribution", "status": "allowed"},
                {"claim_id": "real_world_generator_attribution", "status": "blocked"},
                {"claim_id": "bitcoin_nonce_risk_attribution", "status": "blocked"},
            ],
        }
        lineage = {
            "schema": "primeproject.artifact-lineage.v1",
            "summary": {"reproducible": True},
        }

        protocol = build_decision_protocol(
            evidence_pack=evidence,
            claim_ledger=claim_ledger,
            artifact_lineage=lineage,
            generated_at="2026-05-23T00:00:00+00:00",
        )
        decisions = {decision["decision_id"]: decision for decision in protocol["decisions"]}

        self.assertEqual(protocol["schema"], "primeproject.decision-protocol.v1")
        self.assertEqual(decisions["publish_public_demo"]["status"], "allowed")
        self.assertEqual(decisions["report_controlled_synthetic_signal"]["status"], "allowed")
        self.assertEqual(decisions["promote_real_world_generator_attribution"]["status"], "blocked")
        self.assertIn(
            "gate:real_baseline_gate",
            decisions["promote_real_world_generator_attribution"]["blocking_items"],
        )
        self.assertEqual(decisions["promote_bitcoin_nonce_risk_attribution"]["status"], "blocked")
        self.assertEqual(protocol["summary"]["allowed_count"], 2)
        self.assertEqual(protocol["summary"]["blocked_count"], 2)


def base64_lines(data: bytes) -> str:
    import base64

    encoded = base64.b64encode(data).decode("ascii")
    return "\n".join(encoded[index : index + 64] for index in range(0, len(encoded), 64))


def sha256_text(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fingerprint_report_from_values(values: list[int]) -> dict[str, object]:
    records = [
        KeyRecord(
            key_id=f"prime-{index}",
            algorithm="prime",
            value=value,
            source="unit-test",
        )
        for index, value in enumerate(values)
    ]
    return analyze_prime_generator_fingerprints(records, gap_max_steps=64)


def complete_provenance_record(baseline_id: str) -> dict[str, object]:
    return {
        "baseline_id": baseline_id,
        "library": "OpenSSL",
        "library_version": "3.3.0",
        "algorithm": "RSA",
        "object_type": "rsa-prime",
        "bit_length": 2048,
        "sample_count": 500,
        "collector": "local-owned-lab",
        "collection_date": "2026-05-22",
        "host_platform": "windows-x64",
        "source_commit": "0123456789abcdef",
        "build_config": "release-default",
        "rng_source": "system-csprng",
        "generation_command": "openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048",
        "raw_material_policy": "raw private keys/primes stay local; publish aggregate fingerprints only",
        "aggregate_artifact_sha256": "a" * 64,
    }


def der_subject_public_key_info(pkcs1: bytes) -> bytes:
    algorithm = der_sequence(
        der_oid("1.2.840.113549.1.1.1"),
        der_tlv(0x05, b""),
    )
    return der_sequence(algorithm, der_tlv(0x03, b"\x00" + pkcs1))


def der_sequence(*items: bytes) -> bytes:
    return der_tlv(0x30, b"".join(items))


def der_integer(value: int) -> bytes:
    data = value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")
    if data[0] & 0x80:
        data = b"\x00" + data
    return der_tlv(0x02, data)


def der_oid(oid: str) -> bytes:
    parts = [int(part) for part in oid.split(".")]
    encoded = bytes([parts[0] * 40 + parts[1]])
    for part in parts[2:]:
        encoded += der_base128(part)
    return der_tlv(0x06, encoded)


def der_base128(value: int) -> bytes:
    chunks = [value & 0x7F]
    value >>= 7
    while value:
        chunks.append(0x80 | (value & 0x7F))
        value >>= 7
    return bytes(reversed(chunks))


def der_tlv(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + der_length(len(value)) + value


def der_length(length: int) -> bytes:
    if length < 0x80:
        return bytes([length])
    data = length.to_bytes((length.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(data)]) + data


if __name__ == "__main__":
    unittest.main()
