from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket123_canonical_defect_ratio_closure_bridge import (  # noqa: E402
    SCHEMA,
    abstract_countermodels,
    bridge_guarantee,
    build_attempts,
    build_audit,
    main,
    ratio_bridge_row,
)


class Ticket123CanonicalDefectRatioClosureBridgeTests(unittest.TestCase):
    def test_ratio_identity_is_exact(self) -> None:
        row = ratio_bridge_row(10.0, 12.0, 0.5, 3.0, 2.0)
        self.assertAlmostEqual(row["eta_exact_saving_fraction"], 0.25)
        self.assertAlmostEqual(row["rho_singleton_to_known"], 1.2)
        self.assertAlmostEqual(row["epsilon_boundary_to_known"], 0.05)
        self.assertAlmostEqual(row["exact_normalized_margin"], 0.05)
        self.assertAlmostEqual(row["ratio_identity_margin"], 0.05)
        self.assertLessEqual(row["exact_identity_error"], 1e-15)

    def test_bridge_guarantee_has_positive_compatible_margin(self) -> None:
        result = bridge_guarantee(100.0, 0.25, 1.1, 0.05)
        self.assertAlmostEqual(result["guaranteed_normalized_margin"], 0.125)
        self.assertAlmostEqual(result["guaranteed_absolute_margin"], 12.5)

    def test_independent_premise_countermodels_fail(self) -> None:
        models = abstract_countermodels()
        saving = models["saving_fraction_alone_no_go"]["sequence"]
        boundary = models["ratio_without_boundary_no_go"]["sequence"]
        compatibility = models["compatibility_sharpness"]["sequence"]
        finite = models["finite_prefix_no_go"]["sequence"]
        self.assertEqual({row["saving_fraction"] for row in saving}, {0.25})
        self.assertLess(saving[-1]["normalized_margin"], -100_000.0)
        self.assertEqual(
            {row["singleton_to_known"] for row in boundary}, {0.5}
        )
        self.assertLess(boundary[-1]["normalized_margin"], -100_000.0)
        self.assertEqual(compatibility[0]["normalized_margin"], 0.0)
        self.assertLess(compatibility[-1]["normalized_margin"], 0.0)
        self.assertTrue(
            all(
                row["passing_parameters"]["normalized_margin"] > 0.0
                and row["first_unseen_parameters"]["normalized_margin"] < 0.0
                for row in finite
            )
        )

    def test_finite_audit_reconstructs_ticket122(self) -> None:
        audit = build_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["scale_count"], 8)
        self.assertEqual(machine["exact_closure_count"], 2)
        self.assertEqual(machine["certificate_closure_count"], 1)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertLessEqual(machine["maximum_exact_identity_error"], 1e-12)
        self.assertLessEqual(
            machine["frontier_transition_reconstruction_error"], 1e-12
        )
        rows = audit["finite_ratio_rows"]
        self.assertEqual(rows[-1]["horizon"], 16_777_216)
        self.assertTrue(rows[-1]["closes_exact"])
        self.assertTrue(rows[-1]["closes_by_certificate"])
        self.assertGreater(
            audit["frontier_transition"]["rho_change_contribution"], 0.0
        )
        self.assertLess(
            audit["frontier_transition"]["eta_change_contribution"], 0.0
        )

    def test_other_problem_proxies_are_rejected_without_transfer(self) -> None:
        attempts = {row["problem_id"]: row for row in build_attempts()}
        self.assertEqual(set(attempts), {"riemann", "collatz", "goldbach", "twin-prime"})
        for problem_id in ("riemann", "collatz", "goldbach"):
            self.assertEqual(
                attempts[problem_id]["status"],
                "legacy_proxy_rejected_problem_specific_target_preserved_open",
            )
            self.assertIn(
                "discarded_legacy_proxy",
                attempts[problem_id]["bounded_result"],
            )
        self.assertEqual(
            attempts["twin-prime"]["candidate_theorem"],
            "VaughanCanonicalDefectRatioTriple",
        )

    def test_main_writes_all_problem_artifacts(self) -> None:
        self.assertEqual(main(), 0)
        path = (
            ROOT
            / "data/open-problem/ticket123-canonical-defect-ratio-closure-bridge.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertEqual(
            payload["status"],
            "exact_ratio_bridge_and_independent_premise_nogos_open",
        )
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            payload["canonical_defect_ratio_closure_bridge"]["machine_audit"][
                "total_failure_count"
            ],
            0,
        )
        self.assertTrue(
            (
                ROOT
                / "data/open-problem/twin-prime/tp-ticket-123-defect-ratio-closure-bridge.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
