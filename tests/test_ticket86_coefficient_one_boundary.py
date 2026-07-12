from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket86_coefficient_one_boundary_lab import (  # noqa: E402
    MAX_HORIZON,
    analyze_boundary,
    audit_symbolic_jump,
    cycle_target_residue,
    lift_least_residues,
)


class Ticket86CoefficientOneBoundaryTests(unittest.TestCase):
    def test_exact_reduction_matches_cycle_target(self) -> None:
        for row in lift_least_residues(96):
            horizon = int(row["horizon"])
            precision = horizon + 3
            residue = int(row["residue"])
            self.assertEqual(pow(3, residue, 1 << precision), cycle_target_residue(horizon, precision))
            self.assertEqual(pow(3, residue + 1, 1 << precision), (-7) % (1 << precision))

    def test_lifts_are_nested_and_top_bits_recur_in_audit(self) -> None:
        rows = lift_least_residues(256)
        previous = None
        jump_count = 0
        for row in rows:
            horizon = int(row["horizon"])
            residue = int(row["residue"])
            if previous is not None:
                self.assertIn(residue, (previous, previous + (1 << horizon)))
            if bool(row["top_bit_added"]):
                self.assertGreaterEqual(residue, 1 << horizon)
                self.assertLess(residue, 1 << (horizon + 1))
                jump_count += 1
            previous = residue
        self.assertGreater(jump_count, 64)

    def test_symbolic_jump_contract(self) -> None:
        rows = lift_least_residues(96)
        for row in rows:
            if bool(row["top_bit_added"]):
                audit = audit_symbolic_jump(int(row["horizon"]), int(row["residue"]))
                self.assertEqual(audit["total_failure_count"], 0)

    def test_boundary_payload_has_no_failures(self) -> None:
        audit = analyze_boundary()
        self.assertEqual(audit["machine_audit"]["max_horizon"], MAX_HORIZON)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["theorem_status"], "restricted_coefficient_one_delay_proved_no_collatz_resolution")
        self.assertIn("D(k)>=H+1>log2(k)", audit["delay_statement"])
        self.assertEqual(audit["next_theorem_target"], "TwoAdicDigitRunBoundary")


if __name__ == "__main__":
    unittest.main()
