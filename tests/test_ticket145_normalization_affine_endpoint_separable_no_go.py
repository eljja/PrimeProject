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
    exact_ldl_pivots,
    hilbert_matrix,
)
from ticket145_normalization_affine_endpoint_separable_no_go import (  # noqa: E402
    SCHEMA,
    accelerated_collatz,
    adverse_part,
    build_audit,
    conditional_path,
    diagonal_scale,
    dyadic_level_increment_sums,
    favorable_slack,
)


class Ticket145NormalizationAffineEndpointSeparableNoGoTests(
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
                "primeproject.ticket145-normalization-affine-endpoint-"
                "separable-no-go.v1"
            ),
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_normalized_pivot_formula_and_scaling(self) -> None:
        for size in range(1, 10):
            matrix = hilbert_matrix(size)
            pivot = exact_ldl_pivots(matrix)[-1]
            eta = pivot / matrix[-1][-1]
            with self.subTest(size=size):
                self.assertEqual(
                    eta,
                    Fraction(
                        1,
                        comb(2 * size - 2, size - 1) ** 2,
                    ),
                )

        matrix = hilbert_matrix(6)
        scales = [Fraction(index + 2) for index in range(6)]
        scaled = diagonal_scale(matrix, scales)
        original_pivots = exact_ldl_pivots(matrix)
        scaled_pivots = exact_ldl_pivots(scaled)
        for index in range(6):
            self.assertEqual(
                scaled_pivots[index],
                scales[index] ** 2 * original_pivots[index],
            )
            self.assertEqual(
                scaled_pivots[index] / scaled[index][index],
                original_pivots[index] / matrix[index][index],
            )

    def test_collatz_same_residue_expanding_family(self) -> None:
        for modulus in range(1, 65):
            for multiplier in [1, 3, 9]:
                start = 4 * modulus * multiplier - 1
                successor = accelerated_collatz(start)
                with self.subTest(
                    modulus=modulus,
                    multiplier=multiplier,
                ):
                    self.assertEqual(
                        successor,
                        6 * modulus * multiplier - 1,
                    )
                    self.assertEqual(
                        successor % modulus,
                        start % modulus,
                    )
                    self.assertGreater(successor, start)

    def test_goldbach_endpoint_is_exact_but_aggregate_is_empty(
        self,
    ) -> None:
        for depth in range(2, 9):
            size = 1 << depth
            values = [
                Fraction(57),
                *([Fraction(-57, size - 1)] * (size - 1)),
            ]
            self.assertTrue(
                all(
                    value == 0
                    for value in dyadic_level_increment_sums(values)
                )
            )
            for leaf, value in enumerate(values):
                path = conditional_path(values, leaf)
                endpoint = path[0] + sum(
                    (
                        path[index] - path[index - 1]
                        for index in range(1, len(path))
                    ),
                    Fraction(),
                )
                self.assertEqual(endpoint, value)
            self.assertGreater(max(abs(value) for value in values), 56)

    def test_twin_slack_identity_and_nonnecessity(self) -> None:
        for a10 in range(-6, 7):
            for a01 in range(-6, 7):
                for a11 in range(-6, 7):
                    deficit = a10 + a01 - a11
                    majorant = adverse_part(a10, a01, a11)
                    self.assertGreaterEqual(majorant, deficit)
                    self.assertEqual(
                        majorant - deficit,
                        favorable_slack(a10, a01, a11),
                    )

        witness = self.audit["twin_prime"][
            "separable_majorant_audit"
        ]["synthetic_nonnecessity_witness"]
        self.assertEqual(witness["direct_twin_count"], 1)
        self.assertEqual(witness["joint_deficit_C"], 96)
        self.assertEqual(witness["adverse_part_B"], 178)
        self.assertGreater(witness["adverse_part_B"], witness["A00"])

    def test_all_proof_dags_reject_then_close_then_remain_open(
        self,
    ) -> None:
        for problem in [
            "riemann",
            "collatz",
            "goldbach",
            "twin_prime",
        ]:
            nodes = self.audit[problem]["proof_dag"]["nodes"]
            with self.subTest(problem=problem):
                self.assertEqual(
                    [node["status"] for node in nodes],
                    [
                        "refuted_or_circular",
                        "proved_exact",
                        "open_not_proven",
                    ],
                )
                self.assertEqual(
                    self.audit[problem]["machine_audit"][
                        "conjecture_resolution_count"
                    ],
                    0,
                )


if __name__ == "__main__":
    unittest.main()
