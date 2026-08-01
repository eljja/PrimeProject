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

from ticket172_structure_equivalence_l1_variation import (  # noqa: E402
    SCHEMA,
    build_attempts,
    build_audit,
    finest_mixed_energy_numerator,
)


class Ticket172StructureEquivalenceL1VariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket172-structure-equivalence-l1-variation.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_audit_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_structured_kkt_certificate_and_relative_no_go(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        for row in computation["structured_interval_certificate_rows"]:
            self.assertEqual(
                row["certified_kkt_inertia"],
                {
                    "positive": row["primal_dimension_n"],
                    "negative": row["constraint_rank_r"],
                    "zero": 0,
                },
            )
            self.assertTrue(all(row["checks"].values()))
        for row in computation["whole_relative_norm_necessity_no_go_rows"]:
            self.assertGreater(
                Fraction(
                    row["whole_sign_normalized_relative_norm_squared"]["exact"]
                ),
                1,
            )
            self.assertEqual(row["perturbed_determinant"], -1)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_previous_target_is_equivalent_and_prefixes_bifurcate(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        self.assertIn("equivalent", computation["theorem"])
        self.assertEqual(
            computation["finite_first_descent_diagnostic"][
                "missing_first_descent_count"
            ],
            0,
        )
        for row in computation["exact_finite_prefix_bifurcation_rows"]:
            self.assertEqual(row["ghost_next_valuation"], 1)
            self.assertGreater(row["natural_next_valuation"], 1)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_fourier_l1_bound_is_exactly_sharp(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["exact_l1_sharpness_rows"]
        self.assertEqual(rows[-1]["epsilon"]["exact"], "1/2")
        self.assertEqual(rows[-1]["certified_pointwise_lower_bound"]["exact"], "0/1")
        for row in rows:
            self.assertEqual(
                row["actual_g_minus_minimum"]["exact"],
                row["certified_pointwise_lower_bound"]["exact"],
            )
            self.assertTrue(all(row["checks"].values()))
        for row in computation["finite_prime_representation_spectral_rows"]:
            self.assertGreater(row["minimum_ordered_representation_count"], 0)
            self.assertLessEqual(row["generic_l1_pointwise_lower_bound"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_finest_haar_energy_is_quarter_mixed_difference_energy(self) -> None:
        block = [[1, -1], [-1, 1]]
        self.assertEqual(finest_mixed_energy_numerator(block), 16)
        computation = self.audit["twin_prime"]["reproducible_computation"]
        for row in computation["finite_t161_mixed_variation_rows"]:
            self.assertTrue(
                math.isclose(
                row["exact_finest_fine_fine_haar_energy"]["decimal"],
                row["ticket171_transformed_fine_fine_energy"],
                    rel_tol=1e-12,
                    abs_tol=1e-6,
                )
            )
            self.assertTrue(all(row["checks"].values()))

    def test_zero_margins_do_not_control_mixed_energy(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "exact_marginal_control_no_go_rows"
        ]
        self.assertEqual([row["dyadic_side_N"] for row in rows], [2, 4, 8, 16, 32, 64])
        for row in rows:
            self.assertEqual(row["row_and_column_margins"], 0)
            self.assertEqual(row["fine_fine_energy_fraction"], 1)
            self.assertEqual(row["finest_fine_fine_haar_energy"], row["frobenius_energy"])
            self.assertTrue(all(row["checks"].values()))

    def test_attempts_and_proof_dags_remain_open(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        for attempt in attempts:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertEqual(
                [node["status"] for node in attempt["proof_dag"]["nodes"]],
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_per_problem_artifacts_match_global_attempts(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-172-structured-kkt.json",
            "collatz": "collatz/co-ticket-172-natural-support-equivalence.json",
            "goldbach": "goldbach/gb-ticket-172-fourier-l1.json",
            "twin-prime": "twin-prime/tp-ticket-172-mixed-variation.json",
        }
        attempts = {row["problem_id"]: row for row in self.payload["attempts"]}
        for problem_id, relative in paths.items():
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(encoding="utf-8")
            )
            self.assertEqual(artifact["schema"], SCHEMA)
            self.assertEqual(artifact["status"], "open_not_proven")
            self.assertEqual(artifact["theorem_name"], attempts[problem_id]["new_result"])
            self.assertEqual(
                artifact["candidate_theorem"], attempts[problem_id]["candidate_theorem"]
            )


if __name__ == "__main__":
    unittest.main()
