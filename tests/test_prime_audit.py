from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from random import Random

from prime_audit.analysis import audit_records, evaluate_policy, report_to_dict
from prime_audit.attribution import run_synthetic_attribution_benchmark, sample_generator_records
from prime_audit.baselines import build_generator_baseline, compare_fingerprint_to_baselines, sample_quality
from prime_audit.bitcoin import audit_bitcoin_signatures, parse_der_signature, secp256k1_constants_report
from prime_audit.catalog import classify_public_prime
from prime_audit.conjecture_lab import build_observations, run_lab, summarize_measure
from prime_audit.fingerprints import analyze_prime_generator_fingerprints, prime_gap_context
from prime_audit.io import load_records
from prime_audit.models import KeyRecord
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
        self.assertEqual(len(result["trials_detail"]), 3)

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


def base64_lines(data: bytes) -> str:
    import base64

    encoded = base64.b64encode(data).decode("ascii")
    return "\n".join(encoded[index : index + 64] for index in range(0, len(encoded), 64))


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
