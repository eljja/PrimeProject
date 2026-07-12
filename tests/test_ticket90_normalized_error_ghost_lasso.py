from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket90_normalized_error_ghost_lasso_lab import (  # noqa: E402
    analyze_normalized_error,
    correction_unit_prefix,
    limiting_correction,
)


class Ticket90NormalizedErrorGhostLassoTests(unittest.TestCase):
    def test_correction_recurrence_and_limit(self) -> None:
        units = correction_unit_prefix(32, 32)
        self.assertEqual(units[1], 5)
        self.assertEqual(units[2] % 8, 5)
        self.assertEqual(units[32], limiting_correction(32))

    def test_normalized_error_audit(self) -> None:
        audit = analyze_normalized_error()
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["lasso_precision_count"], 63)
        self.assertEqual(machine["maximum_lasso_precision"], 64)
        self.assertTrue(audit["correction_limit"]["beta_is_odd"])

    def test_claim_boundary(self) -> None:
        audit = analyze_normalized_error()
        self.assertEqual(audit["theorem_status"], "fixed_precision_error_lasso_no_go_proved_no_collatz_resolution")
        self.assertEqual(audit["next_theorem_target"], "GrowingPrecisionErrorGhostSeparation")
        self.assertIn("does not prove", audit["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
