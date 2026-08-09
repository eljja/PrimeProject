from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket198_verified_height_primitive_word_quantifier_strength as ticket198


class Ticket198VerifiedHeightPrimitiveWordQuantifierStrengthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket198.build_audit()

    def test_machine_boundary(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_verified_height_rectangle_transfer(self) -> None:
        rh = self.audit["riemann"]["reproducible_computation"]
        contract = rh["contract"]
        self.assertEqual(
            contract["integer_rectangle_levels_transferred"],
            ticket198.VERIFIED_RH_HEIGHT - 1,
        )
        self.assertTrue(contract["D3_enters_open_critical_strip"])
        self.assertTrue(contract["all_integer_m_through_verified_height_zero_free"])
        self.assertFalse(contract["explicit_taylor_degree_exhibited"])
        self.assertFalse(contract["full_rh_resolved"])

    def test_rectangle_coordinate_map(self) -> None:
        row = ticket198.rh_rectangle_row(3)
        self.assertEqual(row["upper_s_real_interval"], ["-5/2", "1/6"])
        self.assertEqual(row["lower_s_real_interval"], ["5/6", "7/2"])
        self.assertEqual(row["minimum_distance_from_critical_line"], "1/3")
        self.assertTrue(row["enters_open_critical_strip"])

    def test_collatz_fixed_run_family_is_primitive_and_admissible(self) -> None:
        for one_run_count in range(2, 13):
            for scale in [2, 3, 7, 16]:
                row = ticket198.collatz_fixed_run_row(one_run_count, scale)
                self.assertEqual(row["cyclic_run_count"], 2 * one_run_count)
                self.assertEqual(row["one_density"], "1/3")
                self.assertTrue(row["primitive"])
                self.assertTrue(row["contraction_gate_passes"])
                self.assertTrue(row["product_gate_passes"])

    def test_collatz_result_is_not_ticket183_repetition_reclaim(self) -> None:
        collatz = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(collatz["prior_exact_input"]["ticket"], "TICKET-183")
        self.assertEqual(
            collatz["prior_exact_input"]["role"],
            "reused_input_not_new_ticket198_result",
        )
        self.assertTrue(
            collatz["aggregate"][
                "infinite_primitive_family_for_every_fixed_run_count_r_ge_2"
            ]
        )
        self.assertFalse(
            collatz["aggregate"][
                "fixed_run_count_plus_scalar_gates_is_finite_search"
            ]
        )

    def test_goldbach_diagonal_is_inside_collision_support(self) -> None:
        goldbach = self.audit["goldbach"]["reproducible_computation"]
        self.assertTrue(
            goldbach["surrogate_countermodel"][
                "failure_set_subset_of_collision_support"
            ]
        )
        self.assertTrue(
            goldbach["aggregate"][
                "collision_free_margin_implies_log_squared_exception_bound"
            ]
        )
        self.assertFalse(
            goldbach["aggregate"][
                "collision_free_margin_sufficient_for_full_goldbach"
            ]
        )
        self.assertTrue(
            all(
                row["diagonal_missing_from_collision_count"] == 0
                for row in goldbach["finite_stratum_rows"]
            )
        )

    def test_goldbach_finite_scan_is_not_promoted(self) -> None:
        goldbach = self.audit["goldbach"]["reproducible_computation"]
        self.assertEqual(
            goldbach["aggregate"]["finite_actual_goldbach_failure_count"], 0
        )
        self.assertFalse(
            goldbach["surrogate_countermodel"][
                "is_actual_goldbach_representation_function"
            ]
        )
        self.assertIn("finite scan", goldbach["no_go_scope"].lower())

    def test_twin_mass_count_inequality(self) -> None:
        twin = self.audit["twin_prime"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["weighted_mass_below_count_times_cap"]
                for row in twin["finite_dyadic_rows"]
            )
        )
        self.assertTrue(
            twin["aggregate"]["mass_dominance_forces_unbounded_pair_count"]
        )
        self.assertFalse(twin["aggregate"]["parity_breaking_lower_bound_proved"])

    def test_twin_sparse_inference_ratio_decreases(self) -> None:
        twin = self.audit["twin_prime"]["reproducible_computation"]
        ratios = [
            row["upper_bound_ratio_to_sqrtXlogX"]
            for row in twin["sparse_inference_countermodel_rows"]
        ]
        self.assertTrue(all(left > right for left, right in zip(ratios, ratios[1:])))
        self.assertLess(ratios[-1], 1e-30)

    def test_written_artifacts_match_build(self) -> None:
        ticket198.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket198-verified-height-primitive-word-quantifier-strength.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket198.SCHEMA)
        self.assertEqual(len(integrated["attempts"]), 4)
        self.assertTrue(
            all(row["status"] == "open_not_proven" for row in integrated["attempts"])
        )
        self.assertEqual(
            integrated[
                "verified_height_primitive_word_quantifier_strength_audit"
            ]["machine_audit"],
            self.audit["machine_audit"],
        )


if __name__ == "__main__":
    unittest.main()
