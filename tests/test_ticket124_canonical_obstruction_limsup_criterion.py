from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket124_canonical_obstruction_limsup_criterion import (  # noqa: E402
    SCHEMA,
    build_attempts,
    build_audit,
    exact_countermodels,
    limsup_closure_certificate,
    main,
    obstruction_row,
)


class Ticket124CanonicalObstructionLimsupCriterionTests(unittest.TestCase):
    def test_obstruction_identity_is_exact(self) -> None:
        row = obstruction_row(10.0, 12.0, 0.5, 3.0, 2.0)
        self.assertAlmostEqual(row["canonical_obstruction_exact"], 0.95)
        self.assertAlmostEqual(row["exact_normalized_margin"], 0.05)
        self.assertAlmostEqual(row["ratio_reconstruction"], 0.95)
        self.assertLessEqual(row["exact_identity_error"], 1e-15)

    def test_limsup_certificate_is_strict(self) -> None:
        passing = limsup_closure_certificate(0.8)
        endpoint = limsup_closure_certificate(1.0)
        self.assertTrue(passing["criterion_passes"])
        self.assertAlmostEqual(passing["certified_delta"], 0.1)
        self.assertFalse(endpoint["criterion_passes"])
        self.assertEqual(endpoint["certified_delta"], 0.0)

    def test_prior_ratio_triple_is_not_necessary(self) -> None:
        models = exact_countermodels()
        alternating = models["coordinate_envelope_compensation_no_go"]
        self.assertTrue(
            all(
                abs(row["canonical_obstruction"] - 0.8) <= 1e-15
                for row in alternating["sequence"]
            )
        )
        self.assertAlmostEqual(alternating["joint_limsup"], 0.8)
        self.assertAlmostEqual(alternating["separate_envelope_left"], 1.6)
        collapsing = models["positive_saving_floor_not_necessary"]["sequence"]
        self.assertEqual({row["saving_fraction"] for row in collapsing}, {0.0})
        self.assertGreater(collapsing[-1]["normalized_margin"], 0.99)

    def test_endpoint_and_finite_prefix_do_not_close_uniformly(self) -> None:
        models = exact_countermodels()
        endpoint = models["endpoint_limsup_sharpness"]["sequence"]
        finite = models["finite_prefix_no_go"]["sequence"]
        self.assertTrue(all(row["normalized_margin"] > 0.0 for row in endpoint))
        self.assertLess(endpoint[-1]["normalized_margin"], 0.001)
        self.assertTrue(
            all(
                row["passing_margin"] > 0.0
                and row["first_unseen_margin"] < 0.0
                for row in finite
            )
        )

    def test_finite_audit_reconstructs_ticket123(self) -> None:
        audit = build_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["scale_count"], 8)
        self.assertEqual(machine["exact_closure_count"], 2)
        self.assertEqual(machine["certificate_closure_count"], 1)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertLessEqual(machine["maximum_exact_identity_error"], 1e-12)
        self.assertAlmostEqual(machine["alternating_joint_limsup"], 0.8)
        self.assertAlmostEqual(
            machine["alternating_separate_envelope_left"], 1.6
        )
        self.assertEqual(
            audit["retired_target"]["name"],
            "VaughanCanonicalDefectRatioTriple",
        )
        self.assertEqual(
            audit["retained_theorem"]["name"],
            "VaughanCanonicalObstructionLimsup",
        )

    def test_problem_routes_are_reclassified(self) -> None:
        attempts = {row["problem_id"]: row for row in build_attempts()}
        self.assertEqual(
            set(attempts), {"riemann", "collatz", "goldbach", "twin-prime"}
        )
        self.assertEqual(
            attempts["collatz"]["candidate_theorem"],
            "ResidueRankDescentCover",
        )
        self.assertEqual(
            attempts["twin-prime"]["candidate_theorem"],
            "VaughanCanonicalObstructionLimsup",
        )

    def test_main_writes_all_problem_artifacts(self) -> None:
        self.assertEqual(main(), 0)
        path = (
            ROOT
            / "data/open-problem/ticket124-canonical-obstruction-limsup-criterion.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertEqual(
            payload["status"],
            "exact_iff_route_criterion_and_prior_target_no_go_open",
        )
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            (
                ROOT
                / "data/open-problem/twin-prime/tp-ticket-124-obstruction-limsup-criterion.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
