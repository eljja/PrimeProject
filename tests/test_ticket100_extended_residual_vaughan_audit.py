from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket100_extended_residual_vaughan_audit import (  # noqa: E402
    audit_extended_goldbach_screen,
    audit_extended_twin_screen,
    audit_vaughan_joint_cancellation,
)


class Ticket100ExtendedResidualVaughanAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.goldbach = audit_extended_goldbach_screen(200_000)
        cls.twin = audit_extended_twin_screen(200_000)
        cls.vaughan = audit_vaughan_joint_cancellation(100_000)

    def test_extended_candidate_has_no_small_screen_failure(self) -> None:
        self.assertEqual(self.goldbach["candidate_failure_count"], 0)
        self.assertEqual(self.twin["candidate_failure_count"], 0)
        self.assertLess(self.goldbach["maximum_fft_direct_error"], 1e-6)

    def test_vaughan_identity_and_direct_type_ii_replay(self) -> None:
        identity = self.vaughan["identity"]
        self.assertLess(identity["lambda_reconstruction_max_error"], 1e-10)
        self.assertLess(identity["direct_type_ii_max_error"], 1e-10)

    def test_joint_reconstruction_contracts(self) -> None:
        self.assertLess(self.vaughan["goldbach"]["joint_reconstruction_max_relative_error"], 1e-10)
        self.assertLess(self.vaughan["twin"]["joint_reconstruction_max_relative_error"], 1e-10)

    def test_component_labels_and_scope(self) -> None:
        for track in (self.vaughan["goldbach"], self.vaughan["twin"]):
            self.assertEqual(set(track["maximum_rows"]), {"structured", "type_ii", "joint"})
        self.assertIn("proof strategy", self.vaughan["componentwise_no_go"]["scope"])


if __name__ == "__main__":
    unittest.main()
