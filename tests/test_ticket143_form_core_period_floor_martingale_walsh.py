from __future__ import annotations

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket143_form_core_period_floor_martingale_walsh import (  # noqa: E402
    SCHEMA,
    build_audit,
    collatz_affine_numerator,
    dyadic_point_ledger,
    twin_walsh_row,
)


class Ticket143FormCorePeriodFloorMartingaleWalshTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket143-form-core-period-floor-martingale-walsh.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_graph_compressions_are_positive_but_witness_is_negative(
        self,
    ) -> None:
        section = self.audit["riemann"]
        form = section["form_core_audit"]
        self.assertEqual(form["negative_witness"]["form_value"], -1)
        self.assertTrue(
            all(
                Fraction(row["rank_one_schur_margin"]["exact"]) > 0
                for row in form["rows"]
            )
        )
        self.assertIn("form core", section["proved_statement"])

    def test_collatz_period_15601_is_below_imported_odd_period_floor(
        self,
    ) -> None:
        period = self.audit["collatz"]["period_floor_audit"]
        branch = period["retired_ticket142_branch"]
        self.assertEqual(branch["odd_period"], 15_601)
        self.assertEqual(
            branch["published_odd_period_floor"],
            72_000_000_000,
        )
        self.assertTrue(branch["closed_under_published_premise"])
        self.assertIn(
            "not re-proved",
            period["external_published_premise"]["source_role"],
        )

    def test_collatz_raw_word_space_and_order_sensitivity(self) -> None:
        period = self.audit["collatz"]["period_floor_audit"]
        space = period["raw_valuation_word_space"]
        self.assertEqual(space["decimal_digits"], 7_069)
        self.assertEqual(
            int(space["exact_count"]),
            math.comb(24_725, 15_599),
        )
        self.assertNotEqual(
            collatz_affine_numerator((1, 1, 4)),
            collatz_affine_numerator((1, 2, 3)),
        )

    def test_goldbach_martingale_reconstructs_every_point(self) -> None:
        values = [Fraction(value) for value in [3, -2, 5, 7, -1, 4, 0, 9]]
        for point, target in enumerate(values):
            with self.subTest(point=point):
                ledger = dyadic_point_ledger(values, point)
                self.assertEqual(
                    Fraction(ledger["reconstruction"]["exact"]),
                    target,
                )
                self.assertTrue(all(ledger["checks"].values()))

    def test_goldbach_constant_root_mode_breaks_uniform_cap_23(self) -> None:
        audit = self.audit["goldbach"]["martingale_audit"]
        rows = audit["root_mode_no_go_rows"]
        first_failure = min(
            row["depth"]
            for row in rows
            if row["root_coefficient_exceeds_23"]
        )
        self.assertEqual(first_failure, 10)
        self.assertTrue(
            all(row["pointwise_below_K56"] for row in rows)
        )

    def test_twin_walsh_inversion_and_circularity_identity(self) -> None:
        for scale in [1_000, 10_000, 100_000, 1_000_000]:
            with self.subTest(scale=scale):
                row = twin_walsh_row(scale)
                self.assertTrue(all(row["checks"].values()))
                self.assertEqual(
                    row["one_sided_gap"],
                    4 * row["direct_twin_count"],
                )
                self.assertGreater(row["walsh_l1_margin"], 0)

    def test_each_track_has_one_open_next_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ExplicitWeilFormCoreCompressionCertificateFamily",
            "collatz": (
                "PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness"
            ),
            "goldbach": (
                "UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56"
            ),
            "twin_prime": (
                "UniformCubicRoughWalshL1ContractionBelowOne"
            ),
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
