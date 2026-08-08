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

from ticket197_first_rectangle_run_block_sparse_collision import (  # noqa: E402
    build_audit,
    collatz_contiguous_run_row,
    odd_proper_prime_power_metadata,
    ordered_affine_numerator,
    rotate_word,
    xi_rectangle_map,
)


class Ticket197FirstRectangleRunBlockSparseCollisionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket197-first-rectangle-run-block-sparse-collision.json"
            ).read_text(encoding="utf-8")
        )

    def test_xi_D2_maps_outside_open_critical_strip_exactly(self) -> None:
        upper = xi_rectangle_map("upper")
        lower = xi_rectangle_map("lower")
        self.assertEqual(upper["s_real_interval"], ["-3/2", "0"])
        self.assertEqual(lower["s_real_interval"], ["1", "5/2"])
        self.assertFalse(upper["open_critical_strip_intersection"])
        self.assertFalse(lower["open_critical_strip_intersection"])

    def test_xi_first_rectangle_result_is_existential_not_numeric(self) -> None:
        contract = self.audit["riemann"]["reproducible_computation"]["contract"]
        self.assertTrue(contract["actual_xi_D2_zero_free"])
        self.assertTrue(contract["actual_xi_taylor_rouche_section_exists"])
        self.assertFalse(contract["explicit_taylor_degree_exhibited"])
        self.assertFalse(contract["rational_or_interval_rouche_margin_exhibited"])
        self.assertFalse(contract["D2_enters_open_critical_strip"])
        self.assertFalse(contract["full_rh_resolved"])

    def test_contiguous_collatz_closed_form_and_divisibility_obstruction(self) -> None:
        for scale in range(1, 65):
            row = collatz_contiguous_run_row(scale)
            self.assertTrue(row["closed_form_matches_direct"])
            self.assertTrue(row["factorization_matches"])
            self.assertEqual(row["gcd_D_with_2_times_9_power"], 1)
            self.assertTrue(row["reduced_residual_strictly_below_D"])
            self.assertTrue(row["contraction_gate_passes"])
            self.assertTrue(row["product_gate"]["passes"])
            self.assertFalse(row["base_word_divisibility_hit"])
            self.assertEqual(row["cyclic_rotation_divisibility_hit_count"], 0)

    def test_collatz_rotation_identity_preserves_divisibility(self) -> None:
        for scale in range(1, 24):
            word = (1,) * scale + (2,) * (2 * scale)
            denominator = 2 ** (5 * scale) - 3 ** (3 * scale)
            current = word
            for _ in range(len(word)):
                rotated = rotate_word(current, 1)
                left = 2 ** current[0] * ordered_affine_numerator(rotated)
                right = 3 * ordered_affine_numerator(current) + denominator
                self.assertEqual(left, right)
                self.assertEqual(
                    ordered_affine_numerator(current) % denominator == 0,
                    ordered_affine_numerator(rotated) % denominator == 0,
                )
                current = rotated

    def test_goldbach_collision_support_rows_are_exact_and_sparse(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_support_rows"]
        self.assertEqual(len(rows), 17)
        self.assertTrue(all(row["support_below_A_squared"] for row in rows))
        self.assertTrue(all(row["target_18_supported"] for row in rows))
        self.assertTrue(
            all(
                row["collision_supported_even_target_count"]
                + row["collision_free_even_target_count"]
                == row["even_target_count"]
                for row in rows
            )
        )
        self.assertTrue(computation["aggregate"]["density_zero_theorem_proved"])
        self.assertFalse(
            computation["aggregate"]["every_large_even_correlation_bound_proved"]
        )

    def test_goldbach_first_collision_witness_is_nine_plus_nine(self) -> None:
        witness = self.audit["goldbach"]["reproducible_computation"]["witness"]
        self.assertEqual(witness["target_N"], 18)
        self.assertEqual(witness["decomposition"], "9+9=3^2+3^2")
        self.assertTrue(witness["collision_supported"])

    def test_twin_equal_exponent_collisions_are_absent(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        for row in computation["finite_dyadic_rows"]:
            self.assertEqual(row["same_exponent_collision_count"], 0)
            self.assertEqual(row["leading_square_square_collision_count"], 0)
            self.assertTrue(row["all_collisions_touch_exponent_at_least_three"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["equal_exponent_collision_impossible_globally"])
        self.assertTrue(aggregate["square_square_collision_impossible_globally"])
        self.assertFalse(aggregate["parity_breaking_lower_bound_proved"])

    def test_twin_finite_witness_is_mixed_exponent_25_27(self) -> None:
        witness = self.audit["twin_prime"]["reproducible_computation"]["witness"]
        self.assertEqual(witness["pair"], [25, 27])
        self.assertEqual(witness["left"], {"base": 5, "exponent": 2})
        self.assertEqual(witness["right"], {"base": 3, "exponent": 3})
        self.assertFalse(witness["same_exponent"])
        metadata = odd_proper_prime_power_metadata(2**26)
        self.assertEqual(metadata[25], (5, 2))
        self.assertEqual(metadata[27], (3, 3))

    def test_all_attempts_remain_open_and_advance_from_ticket196(self) -> None:
        attempts = self.payload["attempts"]
        self.assertEqual(len(attempts), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        self.assertTrue(
            all(attempt["status"] == "open_not_proven" for attempt in attempts)
        )
        self.assertTrue(all(attempt["candidate_theorem"] for attempt in attempts))
        self.assertTrue(
            all(
                attempt["proof_dag"]["nodes"][0]["status"]
                == "open_input_from_ticket196"
                for attempt in attempts
            )
        )

    def test_machine_contract_has_zero_resolution_and_failure(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["actual_xi_first_rectangle_existence_count"], 1)
        self.assertEqual(
            machine["collatz_infinite_ordered_family_exclusion_count"], 1
        )
        self.assertEqual(machine["goldbach_density_zero_collision_support_count"], 1)
        self.assertEqual(machine["twin_equal_exponent_collision_no_go_count"], 1)
        self.assertEqual(machine["collatz_exact_scale_row_count"], 64)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
