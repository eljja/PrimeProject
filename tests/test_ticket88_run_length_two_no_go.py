from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket30_potential_synthesis_lab import read_json  # noqa: E402
from ticket88_run_length_two_no_go_lab import (  # noqa: E402
    analyze_complement_exponent,
    analyze_golden_shift_countermodel,
    analyze_run_length_two_no_go,
)


class Ticket88RunLengthTwoNoGoTests(unittest.TestCase):
    def test_golden_shift_countermodel(self) -> None:
        audit = analyze_golden_shift_countermodel(10_000)
        self.assertEqual(audit["adjacent_zero_count"], 0)
        self.assertGreater(audit["zero_count"], 90)
        self.assertGreater(audit["one_count"], 9_000)
        self.assertIn("unbounded", audit["nonperiodic_proof"])

    def test_complement_orbit_exact(self) -> None:
        audit = analyze_complement_exponent(512)
        self.assertEqual(audit["total_failure_count"], 0)
        self.assertEqual(audit["eventual_valuation_word"], "1,3")
        self.assertEqual(audit["eventual_mean_valuation"], "2")

    def test_no_go_payload(self) -> None:
        source = read_json(ROOT / "data/open-problem/ticket87-two-adic-digit-run-boundary-lab.json")
        audit = analyze_run_length_two_no_go(source)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["observed_run_length_two_or_more_count"], 32_753)
        self.assertEqual(audit["theorem_status"], "run_length_two_inference_refuted_exactly_no_collatz_resolution")
        self.assertEqual(audit["next_theorem_target"], "FixedLogGoldenMeanExclusion")


if __name__ == "__main__":
    unittest.main()
