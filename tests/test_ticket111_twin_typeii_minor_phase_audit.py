from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket111_twin_typeii_minor_phase_audit import (  # noqa: E402
    HOLDOUT_HORIZON,
    analyze_ticket111,
    audit_typeii_minor_phase,
)


class Ticket111TwinTypeIIMinorPhaseAuditTests(unittest.TestCase):
    def test_component_cross_spectrum_reconstructs_exactly(self) -> None:
        row = audit_typeii_minor_phase(4_096)
        self.assertLess(row["component_reconstruction_error"], 1e-9)
        self.assertLess(row["minor_component_reconstruction_error"], 1e-9)
        self.assertEqual(row["lambda_reconstruction_max_error"], 0.0)

    def test_phase_blind_singleton_envelope_cannot_close(self) -> None:
        row = audit_typeii_minor_phase(4_096)
        self.assertTrue(row["phase_blind_route_refuted"])
        self.assertLessEqual(row["phase_blind_lower_bound"], 0)
        self.assertGreater(row["exact_symmetric_correlation"], 0)

    def test_frozen_power_saving_candidate_survives_holdout(self) -> None:
        row = audit_typeii_minor_phase(HOLDOUT_HORIZON, "post_selection_holdout")
        self.assertTrue(row["registered_lower_inequality_passes"])
        self.assertTrue(row["registered_positivity_closes"])
        self.assertGreater(row["registered_power_saving_lower_bound"], 0)

    def test_full_audit_contract(self) -> None:
        audit = analyze_ticket111()
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 2_097_152)
        self.assertEqual(machine["row_count"], 5)
        self.assertEqual(machine["calibration_row_count"], 4)
        self.assertEqual(machine["holdout_row_count"], 1)
        self.assertEqual(machine["phase_blind_refutation_count"], 5)
        self.assertEqual(machine["holdout_candidate_failure_count"], 0)
        self.assertEqual(machine["contract_failure_count"], 0)
        self.assertEqual(
            audit["next_theorem_target"],
            "PhaseAwareVaughanTypeIIMinorArcPowerSaving",
        )


if __name__ == "__main__":
    unittest.main()
