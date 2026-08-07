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

from ticket189_corefive_sublinear_shift import (  # noqa: E402
    balanced_five_gaps,
    build_audit,
    canonical_five_one_word,
    finite_five_one_horizon_row,
    five_one_closed_form,
    five_one_cycle_row,
    five_one_global_bound,
    harmonic_drift_row,
    proper_prime_power_budget_row,
    summable_core_row,
)
from ticket188_nested_fourone_primepower_dyadic import prime_power_metadata  # noqa: E402


class Ticket189CoreFiveSublinearShiftTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_summable_core_family_has_exact_tail_modulus(self) -> None:
        row = summable_core_row(4, 16)
        self.assertEqual(
            Fraction(row["operator_error_to_limit"]["exact"]), Fraction(1, 16)
        )
        self.assertEqual(
            Fraction(row["adjacent_core_operator_drift"]["exact"]),
            Fraction(1, 16 * 17),
        )
        self.assertEqual(
            Fraction(row["exact_remaining_drift_sum"]["exact"]), Fraction(1, 16)
        )
        self.assertEqual(
            Fraction(row["minimum_full_matrix_eigenvalue"]["exact"]),
            Fraction(1, 8),
        )
        self.assertTrue(all(row["checks"].values()))

    def test_vanishing_adjacent_drift_does_not_imply_convergence(self) -> None:
        small = harmonic_drift_row(64)
        large = harmonic_drift_row(128)
        self.assertGreater(
            Fraction(large["scalar_core_value_H_N"]["exact"]),
            Fraction(small["scalar_core_value_H_N"]["exact"]),
        )
        self.assertLess(
            Fraction(large["adjacent_drift"]["exact"]),
            Fraction(small["adjacent_drift"]["exact"]),
        )
        counterfamily = self.riemann["vanishing_but_nonsummable_drift_counterfamily"]
        self.assertTrue(counterfamily["adjacent_drift_tends_to_zero"])
        self.assertFalse(counterfamily["core_sequence_converges"])
        self.assertFalse(
            self.riemann["promotion_contract"]["actual_pole_neutral_weil_family_verified"]
        )

    def test_five_one_closed_form_matches_affine_recurrence(self) -> None:
        row = five_one_cycle_row(5, 4, 4, 4, 5)
        self.assertTrue(all(row["checks"].values()))
        word = canonical_five_one_word(5, 4, 4, 4, 5)
        self.assertEqual(len(word), 22)
        self.assertEqual(sum(value == 1 for value in word), 5)
        self.assertEqual(
            five_one_closed_form(5, 4, 4, 4, 5),
            int(row["affine_numerator_B"]),
        )

    def test_five_one_finite_exception_range_is_exhaustive(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(13, 22)))
        expected = sum(math.comb(horizon, 5) for horizon in range(13, 22))
        self.assertEqual(expected, 72_897)
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], expected
        )
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))
        self.assertTrue(all(row["contracting"] for row in rows))

    def test_five_one_majorant_closes_all_horizons_from_22(self) -> None:
        exact_bound = Fraction(
            self.collatz["analytic_bound"]["bound_at_h_22"]["exact"]
        )
        self.assertEqual(exact_bound, Fraction(131_155_153_587, 68_719_476_736))
        self.assertLess(exact_bound, 2)
        self.assertTrue(
            all(
                five_one_global_bound(horizon + 1)
                <= five_one_global_bound(horizon)
                for horizon in range(22, 256)
            )
        )
        for horizon in [22, 23, 41, 80, 159]:
            gaps = balanced_five_gaps(horizon)
            self.assertEqual(sum(gaps), horizon)
            self.assertEqual(gaps[-1], max(gaps))

    def test_five_one_transcript_is_deterministic(self) -> None:
        first = finite_five_one_horizon_row(21)
        second = finite_five_one_horizon_row(21)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], math.comb(21, 5))

    def test_proper_prime_power_budget_is_ordered_and_sublinear(self) -> None:
        metadata = prime_power_metadata(1_000_000)
        rows = [
            proper_prime_power_budget_row(target, metadata)
            for target in [1_000, 10_000, 100_000, 1_000_000]
        ]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(
                row["actual_proper_prime_power_count_A_N"]
                <= row["exponent_sum_upper_bound"]
                <= row["simplified_upper_bound"]
                for row in rows
            )
        )
        self.assertLess(rows[-1]["bound_over_N"], rows[-2]["bound_over_N"])
        self.assertTrue(
            self.goldbach["aggregate"]["sublinear_contamination_budget_proved"]
        )
        self.assertFalse(
            self.goldbach["aggregate"]["positive_linear_every_target_lower_bound_proved"]
        )

    def test_goldbach_weighted_decomposition_stays_below_new_budget(self) -> None:
        rows = self.goldbach["finite_decomposition_rows"]
        budgets = self.goldbach["prime_power_budget_rows"]
        self.assertEqual(rows[-1]["even_target_N"], 1_000_000)
        for row, budget in zip(rows, budgets):
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["weighted_prime_power_contamination"],
                budget["simplified_contamination_mass_bound"],
            )

    def test_shift_two_decomposition_keeps_prime_power_terms(self) -> None:
        rows = self.twin["finite_dyadic_decomposition_rows"]
        self.assertEqual([row["dyadic_exponent_j"] for row in rows], list(range(4, 20)))
        self.assertIn(
            [25, 27, 2, 3],
            rows[0]["contamination_examples_left_right_exponents"],
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        witness = self.twin["positive_correlation_no_go_witness"]
        self.assertGreater(witness["positive_von_mangoldt_weight"], 0)
        self.assertFalse(witness["both_endpoints_prime"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_cycle_stratum_closure_count": 1,
                "cross_problem_primepower_bridge_count": 1,
                "rejected_or_corrected_route_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_json_contract_has_four_open_attempts_and_finite_values(self) -> None:
        path = ROOT / "data" / "open-problem" / "ticket189-corefive-sublinear-shift.json"
        payload_text = path.read_text(encoding="utf-8")
        payload = json.loads(payload_text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(row["status"] == "open_not_proven" for row in payload["attempts"])
        )
        self.assertNotIn(": Infinity", payload_text)
        self.assertNotIn(": -Infinity", payload_text)
        self.assertNotIn(": NaN", payload_text)


if __name__ == "__main__":
    unittest.main()
