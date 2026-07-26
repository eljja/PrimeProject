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

from ticket149_smooth_escape_wheel_cover import (  # noqa: E402
    SCHEMA,
    accelerated_collatz,
    build_audit,
    cyclic_convolution,
    minus_five_shadow_data,
    wheel_main_term,
)


class Ticket149SmoothEscapeWheelCoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket149-smooth-escape-wheel-cover.json"
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
        self.assertIn("smooth_escape_wheel_cover_audit", self.payload)

    def test_smooth_basis_absolute_tail_no_go_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_exact_rows"
        ]
        self.assertEqual(len(rows), 16)
        for row in rows:
            epsilon = Fraction(row["epsilon"]["exact"])
            self.assertGreater(epsilon, 0)
            self.assertLessEqual(epsilon, Fraction(1, 4))
            self.assertEqual(
                Fraction(row["global_minimum"]["exact"]),
                -epsilon,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_minus_five_pair_identity(self) -> None:
        for exponent in range(1, 15):
            for coefficient in [1, 2, 3, 8]:
                value = 2 * coefficient * 8**exponent - 5
                first, valuation_one = accelerated_collatz(value)
                second, valuation_two = accelerated_collatz(first)
                self.assertEqual((valuation_one, valuation_two), (1, 2))
                self.assertEqual(
                    second + 5,
                    9 * (value + 5) // 8,
                )

    def test_minus_five_shadow_escape_is_exact_and_maximal(self) -> None:
        for value in range(1, 100_001, 2):
            data = minus_five_shadow_data(value)
            pair_count = int(data["maximal_repeated_pair_count_L"])
            self.assertEqual(data["valuation_prefix"], [1, 2] * pair_count)
            self.assertIn(data["exit_shadow_order_r"], [1, 2, 3])
            self.assertNotEqual(data["exit_valuation_probe"], [1, 2])
            if pair_count:
                self.assertGreater(data["exit_value"], value)

    def test_squarefree_wheel_product_formula(self) -> None:
        for modulus in [6, 30, 210]:
            values = [
                int(math.gcd(residue, modulus) == 1)
                for residue in range(modulus)
            ]
            for endpoint in range(0, modulus, 2):
                direct = cyclic_convolution(values, endpoint)
                self.assertEqual(direct, wheel_main_term(modulus, endpoint))
                self.assertGreater(direct, 0)

    def test_wheel_supported_singletons_can_have_endpoint_holes(self) -> None:
        for modulus in [6, 30, 210]:
            reduced = [
                residue
                for residue in range(modulus)
                if math.gcd(residue, modulus) == 1
            ]
            for endpoint in range(0, modulus, 2):
                witness = next(
                    residue
                    for residue in reduced
                    if (2 * residue - endpoint) % modulus != 0
                )
                values = [0] * modulus
                values[witness] = 1
                self.assertEqual(cyclic_convolution(values, endpoint), 0)

    def test_twin_semiprime_cover_identity(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cover_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                row["exact_twin_count"],
                row["edge_count_E"]
                - row["left_semiprime_edges_L"]
                - row["right_semiprime_edges_R"]
                + row["double_semiprime_edges_D"],
            )
            self.assertGreaterEqual(
                row["exact_twin_count"],
                row["marginal_only_twin_lower_bound"],
            )

    def test_cubic_rough_composites_have_two_large_factors(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_factor_window_rows"
        ]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertGreater(row["cubic_rough_composites_audited"], 0)
            self.assertEqual(row["maximum_factor_count"], 2)
            self.assertEqual(row["failure_count"], 0)

    def test_proof_dags_end_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
