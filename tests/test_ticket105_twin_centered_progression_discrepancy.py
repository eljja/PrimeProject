from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket105_twin_centered_progression_discrepancy import (  # noqa: E402
    audit_centered_discrepancy,
    progression_baseline_weights,
    totient_values,
)


class Ticket105TwinCenteredProgressionDiscrepancyTests(unittest.TestCase):
    def test_totient_sieve(self) -> None:
        phi = totient_values(12)
        self.assertEqual([int(phi[n]) for n in range(1, 13)], [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4])

    def test_progression_baseline_is_nonnegative(self) -> None:
        baseline, metadata = progression_baseline_weights(2_000)
        self.assertGreaterEqual(float(baseline[metadata["u"] + 1 :].min()), 0.0)
        self.assertIn("q/phi(q)", metadata["progression_model"])

    def test_centered_identity_reconstructs_type_ii(self) -> None:
        row = audit_centered_discrepancy(2_000)
        self.assertLess(row["centered_identity_absolute_error"], 1e-7)
        self.assertGreaterEqual(row["cauchy_centered_required_constant"], abs(row["centered_progression_discrepancy"]) * __import__("math").log(2_000) / row["local_external_main"])


if __name__ == "__main__":
    unittest.main()
