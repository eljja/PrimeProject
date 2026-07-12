from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket101_vaughan_cutoff_energy_audit import (  # noqa: E402
    audit_cutoff_frontier,
    audit_energy_equivalences,
)


class Ticket101VaughanCutoffEnergyAuditTests(unittest.TestCase):
    def test_energy_identities_and_equivalence_contract(self) -> None:
        audit = audit_energy_equivalences((10_000, 100_000))
        self.assertEqual(audit["failure_count"], 0)
        self.assertIn("algebraically equivalent", audit["novelty_verdict"])
        for row in audit["checkpoint_rows"]:
            self.assertLess(row["goldbach_identity_error"], 1e-7)
            self.assertLess(row["twin_identity_error"], 1e-7)

    def test_small_cutoff_frontier_records_nonempty_components(self) -> None:
        audit = audit_cutoff_frontier(
            100_000,
            balanced_pairs=((32, 32), (40, 32), (46, 40)),
            near_cutoffs=(100, 200, 316),
        )
        self.assertEqual(audit["limit"], 100_000)
        self.assertGreater(audit["evaluated_pair_count"], 0)
        self.assertIn("separate_budget_sum", audit["best_balanced_goldbach_row"]["goldbach"])
        self.assertIn("separate_budget_sum", audit["best_balanced_twin_row"]["twin"])

    def test_full_collapse_has_zero_type_ii_support_in_small_audit(self) -> None:
        audit = audit_cutoff_frontier(
            100_000,
            balanced_pairs=((40, 40),),
            near_cutoffs=(300, 316, 317),
        )
        self.assertIsNotNone(audit["full_collapse_row"])
        self.assertEqual(audit["full_collapse_row"]["type_ii_support_count"], 0)


if __name__ == "__main__":
    unittest.main()
