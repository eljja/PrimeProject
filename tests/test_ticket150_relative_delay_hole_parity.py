from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket150_relative_delay_hole_parity import (  # noqa: E402
    SCHEMA,
    build_audit,
    sharp_hole_witness,
    type_two_delay_witness,
)


class Ticket150RelativeDelayHoleParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket150-relative-delay-hole-parity.json"
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
        self.assertIn("relative_delay_hole_parity_audit", self.payload)

    def test_relative_form_threshold_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_relative_threshold_rows"
        ]
        self.assertEqual(len(rows), 96)
        for row in rows:
            q = Fraction(row["relative_form_norm_q"]["exact"])
            combined = Fraction(row["combined_eigenvalue"]["exact"])
            self.assertEqual(combined >= 0, q <= 1)
            self.assertEqual(combined > 0, q < 1)
            self.assertTrue(all(row["checks"].values()))

    def test_compact_reference_has_no_positive_ambient_floor(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_compact_coercivity_rows"
        ]
        self.assertEqual(len(rows), 16)
        for row in rows:
            lower = Fraction(
                row["candidate_ambient_lower_bound_c"]["exact"]
            )
            witness = Fraction(row["witness_reference_value"]["exact"])
            self.assertLess(witness, lower)
            self.assertTrue(row["violates_P_ge_cI"])

    def test_exit_types_one_and_three_contract_locally(self) -> None:
        rows = {
            row["exit_order_r"]: row
            for row in self.audit["collatz"]["reproducible_computation"][
                "finite_exit_type_rows"
            ]
        }
        self.assertEqual(rows[1]["strict_local_descents"], 999)
        self.assertEqual(rows[1]["local_equalities"], 1)
        self.assertEqual(rows[2]["strict_local_expansions"], 1_000)
        self.assertEqual(rows[3]["strict_local_descents"], 1_000)
        self.assertTrue(all(row["failure_count"] == 0 for row in rows.values()))

    def test_type_two_crt_witness_defeats_any_audited_window(self) -> None:
        for shadow_pairs in [0, 1, 3, 6]:
            for delay in [1, 5, 17, 40]:
                row = type_two_delay_witness(shadow_pairs, delay)
                self.assertEqual(
                    row["post_exit_valuations"],
                    [1, 1] + [1] * delay,
                )
                self.assertTrue(all(row["checks"].values()))

    def test_sharp_nonnegative_endpoint_hole_radius(self) -> None:
        for modulus in [6, 30, 210]:
            for endpoint in range(0, modulus, 2):
                row = sharp_hole_witness(modulus, endpoint)
                self.assertEqual(row["constructed_convolution"], 0)
                self.assertEqual(
                    row["constructed_distance_squared"],
                    row["sharp_hole_radius_squared"],
                )
                self.assertTrue(all(row["checks"].values()))

    def test_primorial_relative_radius_decreases(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "primorial_relative_radius_rows"
        ]
        ratios = [
            Fraction(row["relative_radius_squared"]["exact"]) for row in rows
        ]
        self.assertGreater(len(ratios), 10)
        self.assertTrue(
            all(right < left for left, right in zip(ratios, ratios[1:]))
        )
        self.assertTrue(
            self.audit["goldbach"]["reproducible_computation"][
                "primorial_ratio_strictly_decreasing_in_audit"
            ]
        )

    def test_twin_cover_deficit_is_exact_parity_bias(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_source_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(
                row["cover_deficit_E_minus_L_minus_R"],
                row["twin_edges_T"] - row["double_semiprime_edges_D"],
            )
            self.assertEqual(
                2 * row["cover_deficit_E_minus_L_minus_R"],
                -row["A10_plus_A01"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_existence_does_not_imply_positive_cover_deficit(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "synthetic_separation_rows"
        ]
        witness = next(
            row
            for row in rows
            if row["twins_exist"] and not row["positive_cover_deficit"]
        )
        self.assertGreater(witness["twin_cell_T"], 0)
        self.assertLessEqual(witness["cover_deficit"], 0)

    def test_proof_dags_end_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
