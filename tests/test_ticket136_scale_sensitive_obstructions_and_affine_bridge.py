from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket136_scale_sensitive_obstructions_and_affine_bridge import (  # noqa: E402
    SCHEMA,
    accelerated_collatz_step,
    build_audit,
    count_fixed_wheel_rough_evens,
    euler_phi,
    minimal_moment_for_inflation,
    rational_phase_transcript,
)


class Ticket136ScaleSensitiveObstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket136-scale-sensitive-obstructions-and-affine-bridge.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_entrywise_decay_does_not_reduce_operator_norm(self) -> None:
        section = self.audit["riemann"]
        rows = section["rational_audit"]["entrywise_decay_counterfamily"]
        self.assertGreater(len(rows), 4)
        for row in rows:
            self.assertEqual(
                Fraction(row["maximum_absolute_row_sum"]["exact"]), Fraction(1)
            )
            self.assertEqual(
                Fraction(row["maximum_absolute_column_sum"]["exact"]), Fraction(1)
            )
            self.assertEqual(
                Fraction(row["operator_norm_witness_ratio"]["exact"]), Fraction(1)
            )
        self.assertLess(
            Fraction(rows[-1]["maximum_entry"]["exact"]),
            Fraction(rows[0]["maximum_entry"]["exact"]),
        )

    def test_collatz_affine_identity_and_fixed_point_no_go(self) -> None:
        self.assertEqual(accelerated_collatz_step(1), (1, 2))
        self.assertEqual(accelerated_collatz_step(3), (5, 1))
        section = self.audit["collatz"]
        audit = section["finite_orbit_audit"]
        self.assertGreater(audit["exact_identity_check_count"], 0)
        self.assertGreater(audit["necessary_cap_check_count"], 0)
        self.assertEqual(audit["failure_count"], 0)
        for row in audit["slope_only_counterexample_n_equals_1"]:
            self.assertTrue(row["slope_contracts"])
            self.assertFalse(row["strict_descent"])
            self.assertEqual(
                int(row["affine_threshold_left"]),
                int(row["affine_threshold_right"]),
            )

    def test_goldbach_fixed_wheel_count_and_exact_moment_threshold(self) -> None:
        self.assertEqual(euler_phi(15), 8)
        self.assertEqual(count_fixed_wheel_rough_evens(15, 3), 24)
        for size in [2, 8, 64, 1024]:
            moment = minimal_moment_for_inflation(size)
            self.assertGreaterEqual(6**moment, size * 5**moment)
            if moment > 1:
                self.assertLess(6 ** (moment - 1), size * 5 ** (moment - 1))
        rows = self.audit["goldbach"]["finite_wheel_audit"]["rows"]
        self.assertTrue(
            any(
                row["complete_period_blocks"] >= 512
                and row["power_only_moment_is_insufficient"]
                for row in rows
            )
        )

    def test_twin_rational_phases_factor_through_denominators(self) -> None:
        characters = [(1, 3), (2, 5), (1, 8)]
        modulus = 120
        for value in [1, 7, 11, 29]:
            self.assertEqual(
                rational_phase_transcript(value, characters),
                rational_phase_transcript(value + modulus, characters),
            )
        section = self.audit["twin_prime"]
        finite = section["finite_fourier_audit"]
        self.assertGreater(finite["total_witnesses"], 0)
        self.assertEqual(finite["failure_count"], 0)
        self.assertTrue(
            all(row["row_failure_count"] == 0 for row in finite["rows"])
        )

    def test_each_track_has_one_stronger_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin",
            "collatz": "UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes",
            "goldbach": "BinaryGoldbachGrowingWheelResidualBoundK56",
            "twin_prime": "AperiodicScaleGrowingTypeIITwinSeparation",
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(section["route_decision"]["next_theorem"], theorem)
                self.assertEqual(section["proof_dag"]["nodes"][-1]["status"], "open_not_proven")
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"], 0
                )


if __name__ == "__main__":
    unittest.main()
