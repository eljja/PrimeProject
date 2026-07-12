from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket103_twin_local_block_audit import audit_local_block, audit_local_blocks  # noqa: E402


class Ticket103TwinLocalBlockAuditTests(unittest.TestCase):
    def test_small_local_block_reconstructs_exact_correlation(self) -> None:
        row = audit_local_block(20_000)
        self.assertEqual(row["block_start"], 10_001)
        self.assertEqual(row["block_length"], 10_000)
        self.assertGreater(row["local_external_main"], 0)
        self.assertLess(row["reconstruction_relative_error"], 1e-12)
        self.assertLess(row["lambda_reconstruction_max_error"], 1e-10)

    def test_local_type_ii_support_does_not_collapse(self) -> None:
        row = audit_local_block(20_000)
        self.assertGreater(row["type_ii_support_fraction"], 0.01)
        self.assertTrue(row["noncollapse_contract_passes"])

    def test_universal_local_type_ii_nonnegativity_has_small_counterexample(self) -> None:
        row = audit_local_block(1_000)
        self.assertFalse(row["type_ii_is_nonnegative"])
        self.assertLess(row["type_ii_local_correlation"], 0)
        self.assertGreater(row["type_ii_required_constant"], 1.7)

    def test_doubling_schedule_is_required(self) -> None:
        with self.assertRaises(ValueError):
            audit_local_blocks((20_000, 50_000))


if __name__ == "__main__":
    unittest.main()
