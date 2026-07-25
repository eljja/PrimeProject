from __future__ import annotations

import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket147_fiber_compensation_phase_graph import (  # noqa: E402
    SCHEMA,
    accelerated_collatz,
    build_audit,
    compensation_word_representative,
    direct_cyclic_convolution,
    exact_matrix_rank,
    first_run_compensation,
    path_ledger,
    phase_quantized_convolution,
    polynomial_from_integer_roots,
    prime_indicator,
)


class Ticket147FiberCompensationPhaseGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket147-fiber-compensation-phase-graph.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_generated_wrapper_schema(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(len(self.payload["attempts"]), 4)
        self.assertIn(
            "fiber_compensation_phase_graph_audit",
            self.payload,
        )

    def test_vandermonde_annihilator(self) -> None:
        for generator_count in range(1, 10):
            coefficients = polynomial_from_integer_roots(
                list(range(1, generator_count + 1))
            )
            self.assertEqual(len(coefficients), generator_count + 1)
            for base in range(1, generator_count + 1):
                self.assertEqual(
                    sum(
                        coefficient * base**power
                        for power, coefficient in enumerate(coefficients)
                    ),
                    0,
                )

    def test_finite_fiber_rank_deficit(self) -> None:
        for generator_count in range(1, 9):
            rows = [
                [
                    base**power
                    for power in range(generator_count + 1)
                ]
                for base in range(1, generator_count + 1)
            ]
            self.assertEqual(exact_matrix_rank(rows), generator_count)
            self.assertLess(generator_count, len(rows[0]))

    def test_accelerated_collatz(self) -> None:
        self.assertEqual(accelerated_collatz(3), (5, 1))
        self.assertEqual(accelerated_collatz(5), (1, 4))
        self.assertEqual(accelerated_collatz(7), (11, 1))

    def test_first_run_exact_formula(self) -> None:
        for value in range(3, 50_001, 2):
            block = first_run_compensation(value)
            run_length = block["run_length"]
            compensation = block["compensation_valuation"]
            numerator = (
                3 ** (run_length + 1) * (value + 1)
                - 2 ** (run_length + 1)
            )
            denominator = 2 ** (run_length + compensation)
            self.assertEqual(numerator % denominator, 0)
            self.assertEqual(
                numerator // denominator,
                block["block_image"],
            )

    def test_two_thirds_words_descend_pointwise(self) -> None:
        for value in range(3, 100_001, 2):
            block = first_run_compensation(value)
            if (
                block["compensation_valuation"]
                >= block["run_length"] + 2
            ):
                self.assertLess(block["block_image"], value)

    def test_two_thirds_mass_is_exact(self) -> None:
        partial = Fraction(0)
        for run_length in range(30):
            partial += Fraction(1, 2 ** (2 * run_length + 1))
        tail = Fraction(2, 3) - partial
        self.assertEqual(tail, Fraction(1, 3 * 2**59))
        self.assertEqual(
            self.audit["collatz"]["reproducible_computation"][
                "exact_haar_mass"
            ]["exact"],
            "2/3",
        )

    def test_residual_b_equals_two_family(self) -> None:
        for run_length in range(1, 20):
            value = compensation_word_representative(run_length, 2)
            block = first_run_compensation(value)
            self.assertEqual(block["run_length"], run_length)
            self.assertEqual(block["compensation_valuation"], 2)
            self.assertGreaterEqual(block["block_image"], value)

    def test_fourier_convolution_identity(self) -> None:
        for length in [31, 61, 127]:
            values = prime_indicator(length)
            target = (length // 3) * 2
            direct = direct_cyclic_convolution(values, target)
            exact_fourier, _ = phase_quantized_convolution(
                values,
                target,
                32,
            )
            self.assertAlmostEqual(exact_fourier.real, direct, places=8)
            self.assertAlmostEqual(exact_fourier.imag, 0.0, places=8)

    def test_phase_quantization_energy_bound(self) -> None:
        for row in self.audit["goldbach"]["reproducible_computation"][
            "finite_prime_indicator_rows"
        ]:
            self.assertTrue(
                row["checks"]["quantization_error_within_rational_bound"]
            )
            bound = Fraction(row["rational_energy_bound"]["exact"])
            self.assertLessEqual(
                row["actual_quantization_error"],
                float(bound) + 1e-9,
            )

    def test_fixed_phase_resolution_ratio_diverges(self) -> None:
        ratios = [
            row["fixed_64_sector_ratio"]
            for row in self.audit["goldbach"]["reproducible_computation"][
                "scale_rows"
            ]
        ]
        self.assertEqual(ratios, sorted(ratios))
        self.assertGreater(ratios[-1], ratios[0])
        for row in self.audit["goldbach"]["reproducible_computation"][
            "scale_rows"
        ]:
            required = row[
                "sufficient_sector_count_crude_lambda_bound"
            ]
            logarithm = math.log(row["N"])
            self.assertGreaterEqual(
                required,
                11 * logarithm**3 / 196,
            )

    def test_path_cut_identity(self) -> None:
        for signs in [
            [1, -1, 1, -1],
            [1, 1, -1, -1],
            [1, -1, -1, 1, 1, -1],
        ]:
            ledger = path_ledger(signs)
            self.assertEqual(
                ledger["A11"],
                ledger["A00"] - 2 * ledger["cut_count"],
            )

    def test_same_path_marginal_counterfamily(self) -> None:
        for multiplier in range(1, 30):
            vertex_count = 4 * multiplier
            alternating = path_ledger(
                [
                    1 if index % 2 == 0 else -1
                    for index in range(vertex_count)
                ]
            )
            block = path_ledger(
                [1] * (2 * multiplier) + [-1] * (2 * multiplier)
            )
            self.assertEqual(
                (alternating["A00"], alternating["A10"], alternating["A01"]),
                (block["A00"], block["A10"], block["A01"]),
            )
            self.assertEqual(alternating["negative_negative_edges"], 0)
            self.assertEqual(
                block["negative_negative_edges"],
                2 * multiplier - 1,
            )

    def test_proof_dags_end_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
