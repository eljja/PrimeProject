from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket142_effective_rank_cycle_direction_haar_liouville import (  # noqa: E402
    SCHEMA,
    build_audit,
    collatz_distinct_product_admits,
    collatz_maximum_distinct_product_minimum,
    twin_liouville_ledger,
)


class Ticket142EffectiveRankCycleDirectionHaarLiouvilleTests(
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
                "primeproject.ticket142-effective-rank-cycle-direction-"
                "haar-liouville.v1"
            ),
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_effective_rank_boundary_family_is_exact(self) -> None:
        rows = self.audit["riemann"]["effective_rank_audit"]["rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                Fraction(row["boundary_normalized_trace"]["exact"]),
                1,
            )
            self.assertEqual(
                Fraction(row["next_normalized_trace"]["exact"]),
                Fraction(1, 4),
            )

    def test_collatz_direction_and_distinct_product_maxima(self) -> None:
        expected = {
            16: 3,
            64: 11,
            256: 279,
            1024: 31,
            4096: 131,
            15601: 285795879,
            16384: 579,
            20000: 1847,
        }
        for period, maximum in expected.items():
            with self.subTest(period=period):
                self.assertEqual(
                    collatz_maximum_distinct_product_minimum(period),
                    maximum,
                )
                self.assertTrue(
                    collatz_distinct_product_admits(period, maximum)
                )
                self.assertFalse(
                    collatz_distinct_product_admits(period, maximum + 4)
                )

    def test_collatz_period_15601_holdout_is_not_a_cycle_count(self) -> None:
        holdout = self.audit["collatz"]["cycle_direction_audit"][
            "period_15601_holdout"
        ]
        self.assertEqual(holdout["first_mod4_candidate"], 268435459)
        self.assertEqual(
            holdout["last_distinct_product_candidate"],
            285795879,
        )
        self.assertEqual(holdout["candidate_minimum_count"], 4340106)
        self.assertIn(
            "minima candidates",
            self.audit["collatz"]["logical_limit"],
        )

    def test_haar_budget_23_is_below_k56_but_24_is_not_uniform(self) -> None:
        audit = self.audit["goldbach"]["haar_dual_audit"]
        self.assertEqual(
            audit["uniform_integer_coefficient_budget_below_K56"],
            23,
        )
        self.assertTrue(all(audit["exact_checks"].values()))
        self.assertEqual(
            Fraction(audit["endpoint_margin"]["exact"]),
            Fraction(23019645297, 2140000000000),
        )
        haar_23 = [
            row
            for row in audit["rows"]
            if row["basis"] == "haar" and row["coefficient_budget"] == 23
        ]
        self.assertTrue(all(row["below_K56"] for row in haar_23))

    def test_basis_change_is_not_an_arithmetic_coefficient_theorem(self) -> None:
        section = self.audit["goldbach"]
        self.assertIn("C_j(TA,TU)", section["haar_dual_audit"][
            "basis_change_identity"
        ])
        self.assertIn("No arithmetic theorem", section["logical_limit"])
        self.assertEqual(
            section["route_decision"]["next_theorem"],
            "UniformEvenGoldbachHaarScaleBudgetBelow56",
        )

    def test_cubic_rough_liouville_ledger_reconstructs_twins(self) -> None:
        expected = {
            1000: (59, -17, -19, 9, 26),
            10000: (358, -104, -84, 2, 137),
            100000: (2486, -564, -556, 138, 936),
            1000000: (17634, -3970, -3992, 1212, 6702),
        }
        for scale, values in expected.items():
            with self.subTest(scale=scale):
                row = twin_liouville_ledger(scale)
                self.assertEqual(
                    (
                        row["A00"],
                        row["A10"],
                        row["A01"],
                        row["A11"],
                        row["direct_twin_count"],
                    ),
                    values,
                )
                self.assertTrue(all(row["checks"].values()))

    def test_each_track_has_one_corrected_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": (
                "ExplicitProjectedWeilFiniteSectionAndTailConvergenceContract"
            ),
            "collatz": (
                "Period15601AffineNumeratorNondivisibilityCertificate"
            ),
            "goldbach": "UniformEvenGoldbachHaarScaleBudgetBelow56",
            "twin_prime": "OneSidedCubicRoughLiouvilleLedgerGap",
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(
                    section["route_decision"]["next_theorem"],
                    theorem,
                )
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"],
                    0,
                )


if __name__ == "__main__":
    unittest.main()
