from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from prime_audit.analysis import audit_records, report_to_dict
from prime_audit.bitcoin import audit_bitcoin_signatures, parse_der_signature, secp256k1_constants_report
from prime_audit.catalog import classify_public_prime
from prime_audit.conjecture_lab import build_observations, run_lab, summarize_measure
from prime_audit.io import load_records
from prime_audit.prediction import build_residue_factors, score_next_prime_candidates
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

    def test_prediction_ranks_actual_next_prime_candidate(self) -> None:
        payload = score_next_prime_candidates(1000, span=80, modulo=30, top=10)

        self.assertEqual(payload["schema"], "primeproject.prediction.v1")
        self.assertEqual(payload["actual_next_prime"], 1009)
        self.assertIsNotNone(payload["rank_of_actual"])
        self.assertGreater(payload["candidates_scored"], 0)
        self.assertIn("score", payload["top_candidates"][0])

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


if __name__ == "__main__":
    unittest.main()
