from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket140_spectral_moments_fixed_floor_duality_rotation import (  # noqa: E402
    SCHEMA,
    build_audit,
    evaluate_polynomial,
    exact_fixed_floor_threshold,
    lagrange_coordinate_coefficients,
    minimum_even_moment_order,
)


class Ticket140SpectralMomentsFixedFloorDualityRotationTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            (
                "primeproject.ticket140-spectral-moments-fixed-floor-"
                "duality-rotation.v1"
            ),
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_even_trace_order_thresholds_are_exact(self) -> None:
        expected = {
            4: 4,
            16: 8,
            64: 12,
            256: 16,
            1024: 20,
            4096: 23,
        }
        for rank, order in expected.items():
            self.assertEqual(minimum_even_moment_order(rank), order)
            self.assertLessEqual(rank * 5 ** (2 * order), 6 ** (2 * order))
            self.assertGreater(
                rank * 5 ** (2 * (order - 1)),
                6 ** (2 * (order - 1)),
            )

    def test_fixed_floor_exact_small_thresholds(self) -> None:
        expected = {
            2**4: 34,
            2**6: 134,
            2**8: 533,
            2**10: 2130,
            2**12: 8518,
        }
        for minimum, threshold in expected.items():
            self.assertEqual(exact_fixed_floor_threshold(minimum), threshold)

    def test_verified_collatz_floor_vacuity_certificate(self) -> None:
        audit = self.audit["collatz"]["fixed_floor_audit"]
        self.assertEqual(audit["verified_floor_M"], 2**28)
        self.assertEqual(
            audit["verified_floor_certified_vacuity_period"],
            563_714_459,
        )
        self.assertTrue(
            all(
                all(row["checks"].values())
                for row in audit["rows"]
            )
        )

    def test_lagrange_dual_reconstructs_coordinate(self) -> None:
        points = [Fraction(1, 8), Fraction(1, 4), Fraction(1, 2), Fraction(1)]
        coefficients = lagrange_coordinate_coefficients(points, 0)
        values = [
            evaluate_polynomial(coefficients, point) for point in points
        ]
        self.assertEqual(
            values,
            [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        )

    def test_power_two_measurement_nullspace_and_dual(self) -> None:
        rows = self.audit["goldbach"]["measurement_duality_audit"]["rows"]
        self.assertEqual(len(rows), 10)
        previous = Fraction(0)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(row["nullity"], 1)
            amplification = Fraction(
                row["first_coordinate_l1_amplification"]["exact"]
            )
            self.assertGreater(amplification, previous)
            previous = amplification

    def test_rotation_sums_obey_uniform_bound(self) -> None:
        rows = self.audit["twin_prime"]["sobolev_rotation_audit"]["rows"]
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            bound = Fraction(row["exact_uniform_bound"]["exact"])
            self.assertTrue(
                all(
                    observation["absolute_birkhoff_sum"] < float(bound)
                    for observation in row["observations"]
                )
            )

    def test_each_track_has_one_revised_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilLogOrderEvenTraceMomentBelowTailGap",
            "collatz": (
                "PeriodDependentCycleMinimumDiophantineSeparation"
            ),
            "goldbach": (
                "ArithmeticK56DualCertificateOnPowerOfTwoHardStratum"
            ),
            "twin_prime": (
                "DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass"
            ),
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(
                    section["route_decision"]["next_theorem"], theorem
                )
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"], 0
                )


if __name__ == "__main__":
    unittest.main()
