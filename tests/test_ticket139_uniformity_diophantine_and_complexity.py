from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket139_uniformity_diophantine_and_complexity import (  # noqa: E402
    SCHEMA,
    barycentric_annihilator,
    build_audit,
    collatz_cycle_window_audit,
)


class Ticket139UniformityDiophantineComplexityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket139-uniformity-diophantine-complexity.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_tight_frame_norm_stays_one_while_l1_budget_grows(self) -> None:
        rows = self.audit["riemann"]["tight_frame_audit"]["rows"]
        previous = Fraction(0)
        for row in rows:
            bound = Fraction(row["cross_gram_l1_bound"]["exact"])
            self.assertEqual(
                Fraction(row["exact_operator_norm_squared"]["exact"]), 1
            )
            self.assertGreater(bound, previous)
            previous = bound
        self.assertEqual(
            Fraction(rows[-1]["cross_gram_l1_bound"]["exact"]),
            Fraction(17, 2),
        )

    def test_collatz_cycle_window_first_gap_is_exact(self) -> None:
        audit = self.audit["collatz"]["cycle_window_audit"]
        self.assertEqual(audit["maximum_period"], 20_000)
        self.assertEqual(audit["excluded_period_count"], 19_999)
        self.assertEqual(
            audit["arithmetically_unexcluded_periods"][0]["period"], 15_601
        )
        self.assertEqual(
            audit["arithmetically_unexcluded_periods"][0][
                "candidate_total_valuation"
            ],
            24_727,
        )

    def test_collatz_window_comparison_uses_only_integers(self) -> None:
        minimum = 2**28
        for period, expected in [(15_600, False), (15_601, True)]:
            three_power = 3**period
            valuation_sum = three_power.bit_length()
            fits = (
                (1 << valuation_sum) * (3 * minimum) ** period
                <= (3 * (3 * minimum + 1)) ** period
            )
            self.assertEqual(fits, expected)
        small = collatz_cycle_window_audit(
            minimum_cycle_value=2**28,
            maximum_period=100,
        )
        self.assertEqual(small["excluded_period_count"], 100)

    def test_barycentric_annihilator_identity_on_generic_nodes(self) -> None:
        result = barycentric_annihilator([2, 5, 11, 19])
        self.assertEqual(result["annihilated_moments"], [0, 0, 0])
        self.assertEqual(
            result["first_surviving_moment"],
            result["expected_first_surviving_moment"],
        )
        self.assertNotEqual(result["first_surviving_moment"], 0)

    def test_power_two_moment_countermodels_are_exact(self) -> None:
        rows = self.audit["goldbach"]["moment_annihilator_audit"]["rows"]
        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                row["annihilated_moment_count"], row["moment_order"]
            )
            self.assertGreater(int(row["maximum_pointwise_amplitude"]), 0)

    def test_irrational_rotation_complexity_grows_at_checkpoints(self) -> None:
        rows = self.audit["twin_prime"]["irrational_rotation_audit"]["rows"]
        self.assertEqual(len(rows), 9)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertGreaterEqual(
                float(row["worst_label_lipschitz_lower_bound"]),
                row["orbit_size"],
            )

    def test_each_track_has_one_revised_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilSignedGramSpectralRadiusBelowTailGap",
            "collatz": "AllPeriodSupercriticalCycleDiophantineExclusion",
            "goldbach": "LocalizedPowerOfTwoSignedGoldbachResidualK56",
            "twin_prime": (
                "UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass"
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
