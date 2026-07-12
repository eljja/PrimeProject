from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket110_twin_rational_arc_budget import (  # noqa: E402
    analyze_ticket110,
    audit_rational_arc_budget,
    rational_major_mask,
)


class Ticket110TwinRationalArcBudgetTests(unittest.TestCase):
    def test_rational_mask_is_nonempty_and_fixed(self) -> None:
        frequencies = np.arange(513, dtype=np.float64) / 1024
        mask, count = rational_major_mask(frequencies, 4_096, 8)
        self.assertGreater(count, 0)
        self.assertGreater(int(mask.sum()), 0)
        self.assertTrue(mask[0])

    def test_major_minor_partition_reconstructs_phase(self) -> None:
        row = audit_rational_arc_budget(4_096)
        for candidate in row["rows"]:
            self.assertLess(candidate["major_minor_reconstruction_error"], 1e-9)

    def test_trivial_minor_bound_is_insufficient(self) -> None:
        row = audit_rational_arc_budget(4_096)
        self.assertTrue(row["trivial_minor_bound_route_refuted"])
        self.assertLessEqual(row["best_rigorous_total_lower_bound"], 0)
        self.assertGreater(row["exact_symmetric_correlation"], 0)

    def test_full_audit_contract(self) -> None:
        audit = analyze_ticket110()
        self.assertEqual(audit["machine_audit"]["maximum_horizon"], 1_048_576)
        self.assertEqual(audit["machine_audit"]["row_count"], 4)
        self.assertEqual(audit["machine_audit"]["cutoff_count"], 8)
        self.assertEqual(audit["machine_audit"]["trivial_minor_refutation_count"], 4)
        self.assertEqual(audit["machine_audit"]["contract_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
