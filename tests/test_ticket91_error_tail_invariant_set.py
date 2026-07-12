from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket91_error_tail_invariant_set_lab import (  # noqa: E402
    analyze_error_tail_invariant_set,
    avoids_double_zero,
    truncated_v2,
)


class Ticket91ErrorTailInvariantSetTests(unittest.TestCase):
    def test_truncated_valuation_and_language(self) -> None:
        self.assertEqual(truncated_v2(0, 8), 8)
        self.assertEqual(truncated_v2(40, 8), 3)
        self.assertTrue(avoids_double_zero(0b101101, 6))
        self.assertFalse(avoids_double_zero(0b101001, 6))

    def test_exact_tail_conjugacy_audit(self) -> None:
        audit = analyze_error_tail_invariant_set()
        machine = audit["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjugacy_state_count"], 4_096)
        self.assertEqual(machine["golden_mean_word_count"], 377)
        self.assertEqual(machine["golden_mean_image_count"], 377)

    def test_route_correction_and_boundary(self) -> None:
        audit = analyze_error_tail_invariant_set()
        self.assertEqual(audit["theorem_status"], "error_tail_conjugacy_and_single_ghost_no_go_proved_no_collatz_resolution")
        self.assertEqual(audit["next_theorem_target"], "GoldenMeanInvariantSetEscape")
        self.assertIn("does not prove 00 recurrence", audit["proof_boundary"])
        self.assertIn("all-one", audit["limiting_conjugacy"]["ghost_identification"])


if __name__ == "__main__":
    unittest.main()
