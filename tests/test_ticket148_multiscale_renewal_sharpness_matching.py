from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket148_multiscale_renewal_sharpness_matching import (  # noqa: E402
    SCHEMA,
    accelerated_collatz,
    build_audit,
    cubic_rough_edges,
    discrete_haar_rows,
    exact_matrix_rank,
    matching_ledger,
)


class Ticket148MultiscaleRenewalSharpnessMatchingTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket148-multiscale-renewal-sharpness-matching.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["historical_correction_count"], 1)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_generated_wrapper_schema(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(len(self.payload["attempts"]), 4)
        self.assertIn(
            "multiscale_renewal_sharpness_matching_audit",
            self.payload,
        )

    def test_discrete_haar_is_exact_orthogonal_basis(self) -> None:
        for level in range(1, 9):
            rows = discrete_haar_rows(level)
            dimension = 2**level
            self.assertEqual(len(rows), dimension)
            self.assertEqual(exact_matrix_rank(rows), dimension)
            for index, row in enumerate(rows):
                self.assertGreater(sum(value * value for value in row), 0)
                for previous in rows[:index]:
                    self.assertEqual(
                        sum(a * b for a, b in zip(row, previous)),
                        0,
                    )

    def test_complete_basis_does_not_promote_finite_positivity(
        self,
    ) -> None:
        for prefix_size in range(1, 100):
            diagonal = [1] * (prefix_size + 1)
            diagonal[prefix_size] = -1
            self.assertTrue(all(value > 0 for value in diagonal[:prefix_size]))
            self.assertLess(diagonal[prefix_size], 0)

    def test_accelerated_collatz_pair_identity(self) -> None:
        for exponent in range(1, 15):
            for coefficient in [1, 2, 3, 8]:
                value = 2 * coefficient * 8**exponent - 5
                first, valuation_one = accelerated_collatz(value)
                second, valuation_two = accelerated_collatz(first)
                self.assertEqual((valuation_one, valuation_two), (1, 2))
                self.assertEqual(
                    second,
                    2 * (9 * coefficient) * 8 ** (exponent - 1) - 5,
                )

    def test_minus_five_cylinder_defeats_every_fixed_horizon(
        self,
    ) -> None:
        for pair_count in range(1, 21):
            modulus = 2 ** (3 * pair_count + 1)
            for lift in [0, 1, 5]:
                start = modulus * (lift + 1) - 5
                value = start
                valuations = []
                for _ in range(2 * pair_count):
                    value, valuation = accelerated_collatz(value)
                    valuations.append(valuation)
                self.assertEqual(valuations, [1, 2] * pair_count)
                self.assertEqual(
                    value,
                    2 * 9**pair_count * (lift + 1) - 5,
                )
                self.assertGreater(value, start)

    def test_phase_quantization_rate_is_order_sharp(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_numeric_rows"
        ]
        scaled = [
            row[
                "scaled_relative_error_M_times_error_over_energy"
            ]
            for row in rows
        ]
        self.assertEqual(scaled, sorted(scaled))
        self.assertLess(abs(scaled[-1] - math.pi / 3), 0.02)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))

    def test_cubic_rough_support_is_a_matching(self) -> None:
        for scale in [13, 100, 1_000, 10_000]:
            degrees: dict[int, int] = {}
            for left, right in cubic_rough_edges(scale):
                degrees[left] = degrees.get(left, 0) + 1
                degrees[right] = degrees.get(right, 0) + 1
            self.assertLessEqual(max(degrees.values(), default=0), 1)

    def test_matching_marginals_do_not_determine_coupling(self) -> None:
        for multiplier in range(1, 50):
            correlated = matching_ledger(
                {
                    "++": 2 * multiplier,
                    "+-": 0,
                    "-+": 0,
                    "--": 2 * multiplier,
                }
            )
            anticorrelated = matching_ledger(
                {
                    "++": 0,
                    "+-": 2 * multiplier,
                    "-+": 2 * multiplier,
                    "--": 0,
                }
            )
            self.assertEqual(
                (
                    correlated["A00"],
                    correlated["A10"],
                    correlated["A01"],
                ),
                (
                    anticorrelated["A00"],
                    anticorrelated["A10"],
                    anticorrelated["A01"],
                ),
            )
            self.assertNotEqual(correlated["A11"], anticorrelated["A11"])
            self.assertNotEqual(
                correlated["negative_negative_edges"],
                anticorrelated["negative_negative_edges"],
            )

    def test_t142_cells_invert_exactly(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cubic_rough_cell_rows"
        ]
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                row["exact_cell_counts"]["--"],
                {1_000: 26, 10_000: 137, 100_000: 936, 1_000_000: 6_702}[
                    row["X"]
                ],
            )

    def test_proof_dags_end_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
