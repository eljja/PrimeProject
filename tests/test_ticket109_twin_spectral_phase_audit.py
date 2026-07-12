from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket109_twin_spectral_phase_audit import (  # noqa: E402
    analyze_ticket109,
    audit_spectral_phase,
    next_power_of_two,
)


class Ticket109TwinSpectralPhaseAuditTests(unittest.TestCase):
    def test_fft_length_is_power_of_two_and_zero_padded(self) -> None:
        length = next_power_of_two(2 * 4_099)
        self.assertEqual(length & (length - 1), 0)
        self.assertGreaterEqual(length, 2 * 4_099)

    def test_spectral_identity_matches_direct_correlation(self) -> None:
        row = audit_spectral_phase(4_096)
        self.assertLess(row["spectral_identity_absolute_error"], 1e-7)
        self.assertLess(row["contamination_decomposition_absolute_error"], 1e-9)

    def test_single_origin_low_frequency_route_is_refuted(self) -> None:
        row = audit_spectral_phase(4_096)
        self.assertTrue(row["low_frequency_only_route_refuted"])
        self.assertLessEqual(row["best_low_frequency_lower_bound"], 0)
        self.assertGreater(row["symmetric_bump_correlation"], 0)

    def test_full_audit_contract(self) -> None:
        audit = analyze_ticket109()
        self.assertEqual(audit["machine_audit"]["maximum_horizon"], 1_048_576)
        self.assertEqual(audit["machine_audit"]["row_count"], 4)
        self.assertEqual(audit["machine_audit"]["low_frequency_refutation_count"], 4)
        self.assertEqual(audit["machine_audit"]["contract_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
