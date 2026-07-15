from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket122_twin_canonical_joint_defect_audit import (  # noqa: E402
    SCHEMA,
    abstract_countermodels,
    build_audit,
    canonical_pair_row,
    main,
    scalar_mean_row,
)


class Ticket122CanonicalJointDefectAuditTests(unittest.TestCase):
    def test_scalar_opposition_identity_is_exact(self) -> None:
        opposite = scalar_mean_row(7.0, -3.0)
        self.assertEqual(opposite["sign_relation"], "opposite")
        self.assertAlmostEqual(float(opposite["mean_saving"]), 6.0)
        self.assertAlmostEqual(float(opposite["mean_saving_formula"]), 6.0)
        self.assertAlmostEqual(float(opposite["mean_formula_error"]), 0.0)

        aligned = scalar_mean_row(-7.0, -3.0)
        self.assertEqual(aligned["sign_relation"], "same_or_zero")
        self.assertAlmostEqual(float(aligned["mean_saving"]), 0.0)
        self.assertAlmostEqual(float(aligned["mean_saving_formula"]), 0.0)

    def test_joint_identity_and_certificate(self) -> None:
        row = canonical_pair_row(
            5.0,
            -2.0,
            4.0,
            -2.0,
            1.0,
            3.0,
        )
        self.assertAlmostEqual(float(row["mean_saving"]), 4.0)
        self.assertAlmostEqual(float(row["actual_centered_saving"]), 6.0)
        self.assertAlmostEqual(float(row["total_saving"]), 10.0)
        self.assertAlmostEqual(float(row["rationalization_error"]), 0.0)
        self.assertLessEqual(float(row["joint_lower_violation"]), 1e-12)
        self.assertLessEqual(float(row["joint_upper_violation"]), 1e-12)

    def test_local_and_centered_only_countermodels_decay(self) -> None:
        models = abstract_countermodels()
        local = models["first_pair_only_no_go"]["sequence"]
        centered = models["centered_only_total_budget_no_go"]["sequence"]
        self.assertTrue(
            all(
                local[index + 1]["global_saving_fraction"]
                < local[index]["global_saving_fraction"]
                for index in range(len(local) - 1)
            )
        )
        self.assertTrue(
            all(
                centered[index + 1]["total_saving_fraction"]
                < centered[index]["total_saving_fraction"]
                for index in range(len(centered) - 1)
            )
        )
        self.assertLess(local[-1]["global_saving_fraction"], 1.1e-6)
        self.assertLess(centered[-1]["total_saving_fraction"], 1.1e-6)

    def test_finite_audit_reconstructs_every_budget(self) -> None:
        audit = build_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["scale_count"], 8)
        self.assertGreater(machine["pair_group_count"], 8)
        self.assertGreater(machine["pair_denominator_row_count"], 248)
        self.assertGreaterEqual(machine["minimum_pair_total_saving"], 0.0)
        self.assertGreaterEqual(machine["minimum_pair_saving_fraction"], 0.0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertTrue(
            all(
                float(row["joint_lower_certificate"])
                <= float(row["exact_total_saving"]) + 1e-7
                for row in audit["scale_rows"]
            )
        )
        self.assertTrue(
            all(
                math.isclose(
                    float(row["finite_lower_bound"]),
                    float(row["saving_surplus_over_raw_requirement"]),
                    abs_tol=1e-6,
                )
                for row in audit["scale_rows"]
            )
        )

    def test_main_writes_problem_artifacts(self) -> None:
        self.assertEqual(main(), 0)
        path = (
            ROOT
            / "data/open-problem/ticket122-twin-canonical-joint-defect-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertEqual(
            payload["status"],
            "exact_canonical_joint_identity_and_local_only_nogos_open",
        )
        self.assertEqual(
            payload["twin_canonical_joint_defect_audit"]["machine_audit"][
                "total_failure_count"
            ],
            0,
        )
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            (
                ROOT
                / "data/open-problem/twin-prime/tp-ticket-122-canonical-joint-defect-audit.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
