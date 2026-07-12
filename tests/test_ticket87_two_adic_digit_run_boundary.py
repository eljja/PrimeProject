from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket86_coefficient_one_boundary_lab import lift_least_residues  # noqa: E402
from ticket87_two_adic_digit_run_boundary_lab import (  # noqa: E402
    analyze_digit_runs,
    fixed_log_residue,
    residue_at,
    run_certificate,
)


class Ticket87TwoAdicDigitRunBoundaryTests(unittest.TestCase):
    def test_padic_log_prefix_matches_hensel_lifts(self) -> None:
        full_residue, _ = fixed_log_residue(512)
        for row in lift_least_residues(512):
            self.assertEqual(residue_at(full_residue, int(row["horizon"])), int(row["residue"]))

    def test_run_identity_on_small_complete_runs(self) -> None:
        full_residue, _ = fixed_log_residue(128)
        top_bits = [horizon for horizon in range(2, 129) if (full_residue >> horizon) & 1]
        for start, next_start in zip(top_bits, top_bits[1:]):
            certificate = run_certificate(full_residue, start, next_start)
            exponent = residue_at(full_residue, start)
            valuation = next_start + 2
            self.assertEqual(pow(3, exponent + 1, 1 << valuation), (-7) % (1 << valuation))
            self.assertNotEqual(pow(3, exponent + 1, 1 << (valuation + 1)), (-7) % (1 << (valuation + 1)))
            self.assertEqual(certificate["zero_run_length"], next_start - start - 1)

    def test_small_audit_contract(self) -> None:
        audit = analyze_digit_runs(4_096)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertGreater(audit["machine_audit"]["positive_zero_run_count"], 500)
        self.assertGreaterEqual(audit["machine_audit"]["longest_observed_zero_run"], 13)
        self.assertIn("D(k)>log2(k)+1", audit["delay_statement"])
        self.assertEqual(audit["next_theorem_target"], "TwoAdicRunLengthTwoInfinitude")


if __name__ == "__main__":
    unittest.main()
