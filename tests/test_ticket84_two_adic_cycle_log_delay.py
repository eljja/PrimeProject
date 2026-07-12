from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket84_two_adic_cycle_log_delay_lab import (  # noqa: E402
    analyze_two_adic_cycle_bound,
    cycle_symbolic_states,
    explicit_cycle_exponent,
    lift_discrete_log_residues,
)


class Ticket84TwoAdicCycleLogDelayTests(unittest.TestCase):
    def test_negative_two_adic_cycle_is_exact(self) -> None:
        states = cycle_symbolic_states(32)
        self.assertEqual([row["incoming_valuation"] for row in states[1:]], [2, 1] * 16)
        self.assertEqual([row["ghost_value"] for row in states[:4]], [-7, -5, -7, -5])

    def test_hensel_lifts_and_small_positive_exponents(self) -> None:
        residues = lift_discrete_log_residues(32)
        for precision, residue in residues.items():
            self.assertEqual(pow(3, residue, 1 << precision), (-13) % (1 << precision))
            self.assertEqual(residue % 2, 1)
        self.assertEqual(explicit_cycle_exponent(2, residues)["exponent"], 13)
        self.assertEqual(explicit_cycle_exponent(3, residues)["exponent"], 37)
        self.assertEqual(explicit_cycle_exponent(4, residues)["exponent"], 69)

    def test_full_audit_and_claim_boundary(self) -> None:
        result = analyze_two_adic_cycle_bound()
        audit = result["machine_audit"]
        self.assertEqual(audit["horizon_case_count"], 255)
        self.assertEqual(audit["maximum_precision"], 386)
        self.assertEqual(audit["symbolic_state_count"], 33150)
        self.assertEqual(audit["total_failure_count"], 0)
        self.assertEqual(result["next_theorem_target"], "AccessibleCycleCoefficientSupremum")
        self.assertIn("neither divergence", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
