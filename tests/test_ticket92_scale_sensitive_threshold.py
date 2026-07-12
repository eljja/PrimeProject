from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket92_scale_sensitive_threshold_audit import (  # noqa: E402
    analyze_second_order_defect,
    corrected_maynard_artifact,
    square_coded_no00_bits,
)
from ticket30_potential_synthesis_lab import read_json  # noqa: E402


class Ticket92ScaleSensitiveThresholdTests(unittest.TestCase):
    def test_square_coded_countermodel_avoids_double_zero(self) -> None:
        bits = square_coded_no00_bits(4_096)
        self.assertFalse(any(left == right == 0 for left, right in zip(bits, bits[1:])))
        self.assertIn(0, bits)
        self.assertIn(1, bits)

    def test_second_order_defect_contract(self) -> None:
        audit = analyze_second_order_defect(4_096)
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["maximum_floor_defect"], 14)
        self.assertGreater(machine["second_order_target_event_count"], 500)
        self.assertEqual(audit["next_theorem_target"], "FixedLogSecondOrderDefectRecurrence")

    def test_maynard_threshold_correction_removes_gap_promotion(self) -> None:
        source = read_json(ROOT / "data/open-problem/twin-prime/tp-cegis-14-maynard-sieve-weight.json")
        corrected, audit = corrected_maynard_artifact(source)
        self.assertEqual(corrected["schema"], "primeproject.twin-prime.maynard-sieve-weight-certificate.v2")
        self.assertIsNone(corrected["smallest_bounded_gap"])
        self.assertTrue(all(row["implied_bounded_gap"] is None for row in corrected["maynard_weight_values"]))
        self.assertTrue(all(not row["maynard_two_prime_criterion_certified"] for row in corrected["maynard_weight_values"]))
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertIn(">4", audit["criterion"]["two_prime_threshold"])


if __name__ == "__main__":
    unittest.main()
