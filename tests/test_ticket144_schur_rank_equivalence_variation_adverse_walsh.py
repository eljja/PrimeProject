from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket144_schur_rank_equivalence_variation_adverse_walsh import (  # noqa: E402
    SCHEMA,
    accelerated_collatz,
    build_audit,
    direct_zero_path_means,
    exact_ldl_pivots,
    hilbert_matrix,
    path_mean,
    twin_adverse_row,
    walsh_coefficients_from_counts,
)


class Ticket144SchurRankEquivalenceVariationAdverseWalshTests(
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
                "primeproject.ticket144-schur-rank-equivalence-variation-"
                "adverse-walsh.v1"
            ),
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_hilbert_schur_pivots_are_exactly_positive(
        self,
    ) -> None:
        for size in range(1, 9):
            pivots = exact_ldl_pivots(hilbert_matrix(size))
            with self.subTest(size=size):
                self.assertTrue(all(pivot > 0 for pivot in pivots))
                self.assertEqual(
                    pivots[-1],
                    Fraction(
                        1,
                        (2 * size - 1)
                        * comb(2 * size - 2, size - 1) ** 2,
                    ),
                )

    def test_riemann_finite_prefix_has_negative_extension(self) -> None:
        rows = self.audit["riemann"]["schur_audit"][
            "negative_extension_rows"
        ]
        self.assertTrue(
            all(
                row["new_schur_pivot"] < 0
                and all(row["checks"].values())
                for row in rows
            )
        )

    def test_collatz_rank_equivalence_finite_audit(self) -> None:
        rank = self.audit["collatz"]["rank_equivalence_audit"]
        finite = rank["finite_stopping_rank_audit"]
        self.assertEqual(finite["maximum_input_rank_start"], 77_031)
        self.assertEqual(finite["maximum_input_rank"], 129)
        self.assertTrue(finite["all_audited_input_ranks_drop"])
        self.assertEqual(accelerated_collatz(27), 41)

    def test_goldbach_counterfamily_direct_means(self) -> None:
        for depth in range(1, 9):
            with self.subTest(depth=depth):
                self.assertEqual(
                    direct_zero_path_means(depth),
                    [
                        path_mean(level)
                        for level in range(depth + 1)
                    ],
                )

    def test_goldbach_absolute_variation_crosses_k56(self) -> None:
        rows = self.audit["goldbach"]["variation_audit"]["rows"]
        by_depth = {row["depth"]: row for row in rows}
        self.assertEqual(
            Fraction(
                by_depth[112]["absolute_path_variation"]["exact"]
            ),
            56,
        )
        self.assertFalse(
            by_depth[112]["absolute_variation_exceeds_56"]
        )
        self.assertTrue(
            by_depth[113]["absolute_variation_exceeds_56"]
        )
        self.assertTrue(
            all(row["terminal_sup_norm"] <= 1 for row in rows)
        )

    def test_twin_simplex_and_adverse_reduction(self) -> None:
        for scale in [1_000, 10_000, 100_000, 1_000_000]:
            with self.subTest(scale=scale):
                row = twin_adverse_row(scale)
                self.assertTrue(all(row["checks"].values()))
                self.assertEqual(row["adverse_walsh_part"], 0)
                self.assertGreaterEqual(
                    row["direct_twin_count"],
                    Fraction(
                        row["certified_twin_lower_bound"]["exact"]
                    ),
                )

    def test_twin_l1_is_not_necessary_and_dags_remain_open(
        self,
    ) -> None:
        coefficients = walsh_coefficients_from_counts([90, 5, 4, 1])
        self.assertEqual(coefficients, (100, 90, 88, 82))
        self.assertGreater(sum(abs(value) for value in coefficients[1:]), 100)
        for problem in [
            "riemann",
            "collatz",
            "goldbach",
            "twin_prime",
        ]:
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"][
                        "conjecture_resolution_count"
                    ],
                    0,
                )


if __name__ == "__main__":
    unittest.main()
