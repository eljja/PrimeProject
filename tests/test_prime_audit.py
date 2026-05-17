from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from prime_audit.analysis import audit_records, report_to_dict
from prime_audit.catalog import classify_public_prime
from prime_audit.conjecture_lab import build_observations, run_lab, summarize_measure
from prime_audit.io import load_records
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


if __name__ == "__main__":
    unittest.main()
