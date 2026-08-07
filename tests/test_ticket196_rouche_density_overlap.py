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

from ticket196_rouche_density_overlap import (  # noqa: E402
    build_audit,
    one_two_scalar_profile_row,
    rational_rectangle_row,
)


class Ticket196RoucheDensityOverlapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket196-rouche-density-overlap.json"
            ).read_text(encoding="utf-8")
        )

    def test_rational_rectangles_separate_real_and_nonreal_zero_examples(self) -> None:
        for index in range(2, 13):
            row = rational_rectangle_row(index)
            self.assertTrue(
                row["real_zero_polynomial"]["rouche_certificate_exists"]
            )
            self.assertEqual(row["real_zero_polynomial"]["upper_zero_count"], 0)
            self.assertEqual(row["real_zero_polynomial"]["lower_zero_count"], 0)
            self.assertFalse(
                row["nonreal_zero_polynomial"][
                    "zero_free_rouche_certificate_exists"
                ]
            )
            self.assertEqual(
                row["nonreal_zero_polynomial"]["upper_witness"], "i"
            )
            self.assertEqual(
                row["nonreal_zero_polynomial"]["lower_witness"], "-i"
            )

    def test_rouche_exhaustion_is_marked_target_equivalent_not_solved(self) -> None:
        contract = self.audit["riemann"]["reproducible_computation"]["contract"]
        self.assertTrue(contract["certificate_family_implies_all_zeros_real"])
        self.assertTrue(contract["all_zeros_real_implies_certificate_family_exists"])
        self.assertFalse(contract["certificate_family_is_strictly_weaker_than_rh"])
        self.assertFalse(contract["actual_xi_first_rectangle_certified"])

    def test_one_third_profiles_pass_both_scalar_collatz_gates_exactly(self) -> None:
        for scale in range(1, 65):
            row = one_two_scalar_profile_row(scale)
            self.assertEqual(row["horizon_h"], 3 * scale)
            self.assertEqual(row["one_count_r"], scale)
            self.assertGreater(
                row["contraction_left_2_power"], row["contraction_right_3_power"]
            )
            self.assertGreater(
                row["cycle_product_bound"]["numerator"],
                row["cycle_product_bound"]["denominator"],
            )
            self.assertEqual(
                row["first_position_one_word_count"],
                math.comb(3 * scale - 1, scale - 1),
            )
            self.assertFalse(row["affine_divisibility_verified"])

    def test_collatz_density_window_contains_one_third(self) -> None:
        window = self.audit["collatz"]["reproducible_computation"][
            "density_window"
        ]
        self.assertLess(window["lower_decimal"], 1 / 3)
        self.assertGreater(window["upper_decimal"], 1 / 3)
        self.assertEqual(window["interior_rational"], "1/3")
        aggregate = self.audit["collatz"]["reproducible_computation"][
            "aggregate"
        ]
        self.assertTrue(aggregate["infinite_profile_family_proved"])
        self.assertFalse(aggregate["actual_cycle_found"])

    def test_goldbach_collision_inclusion_exclusion_identity(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        for row in computation["finite_target_rows"]:
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["collision_corrected_envelope"], row["old_union_envelope"]
            )
            self.assertAlmostEqual(
                row["envelope_saving"], row["Q_convolved_Q_collision"], places=10
            )

    def test_goldbach_double_charge_witness_is_nine_plus_nine(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        witness = computation["overlap_witness"]
        self.assertEqual(witness["target_N"], 18)
        self.assertEqual(witness["ordered_pair"], [9, 9])
        self.assertAlmostEqual(witness["weight"], math.log(3) ** 2, places=12)
        row = next(
            row for row in computation["finite_target_rows"] if row["target_N"] == 18
        )
        self.assertEqual(row["collision_support_count"], 1)

    def test_twin_collision_inclusion_exclusion_identity(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        for row in computation["finite_dyadic_rows"]:
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["collision_corrected_envelope"], row["old_union_envelope"]
            )
            self.assertAlmostEqual(
                row["envelope_saving"], row["Q_left_Q_right_collision"], places=10
            )

    def test_twin_double_charge_witness_is_twenty_five_twenty_seven(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        witness = computation["overlap_witness"]
        self.assertEqual(witness["dyadic_block"], [16, 32])
        self.assertEqual(witness["shift_two_pair"], [25, 27])
        self.assertAlmostEqual(
            witness["weight"], math.log(5) * math.log(3), places=12
        )
        self.assertEqual(computation["finite_dyadic_rows"][0]["collision_support_count"], 1)

    def test_all_four_attempts_remain_open_with_single_next_lemmas(self) -> None:
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
        self.assertTrue(all(attempt["proof_dag"] for attempt in attempts))
        self.assertTrue(
            all(
                attempt["proof_dag"]["nodes"][0]["status"]
                == "open_input_from_ticket195"
                for attempt in attempts
            )
        )

    def test_machine_contract_has_zero_resolution_and_failure(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rouche_exhaustion_equivalence_count"], 1)
        self.assertEqual(machine["scalar_density_no_go_count"], 1)
        self.assertEqual(machine["collision_corrected_envelope_count"], 2)
        self.assertEqual(machine["scalar_admissible_profile_count"], 64)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
