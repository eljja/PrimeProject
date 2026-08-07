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

from ticket191_probe_sevenone_budget_granularity import (  # noqa: E402
    build_audit,
    coordinate_positivity_counterexample,
    finite_seven_one_horizon_row,
    rational_probe_row,
    seven_one_product_bound,
    sparse_arithmetic_scale_row,
)


class Ticket191ProbeSevenOneBudgetGranularityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_rational_probe_scalar_cauchy_modulus(self) -> None:
        for vector in [(1, 0), (0, 1), (1, 1), (2, -1)]:
            row = rational_probe_row(vector, 32, 65)
            self.assertTrue(row["difference_below_modulus"])
            self.assertLessEqual(
                Fraction(row["exact_difference"]["exact"]),
                Fraction(row["certified_probe_modulus"]["exact"]),
            )
        self.assertFalse(
            self.riemann["promotion_contract"][
                "actual_pole_neutral_weil_probe_convergence_verified"
            ]
        )

    def test_coordinate_positivity_does_not_imply_psd(self) -> None:
        row = coordinate_positivity_counterexample(Fraction(3, 2))
        self.assertTrue(row["coordinates_are_positive"])
        self.assertFalse(row["form_is_positive_semidefinite"])
        self.assertEqual(Fraction(row["negative_witness_value"]["exact"]), -1)

    def test_seven_one_finite_exception_range_is_exhaustive(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(17, 27)))
        expected = sum(math.comb(horizon, 7) for horizon in range(17, 27))
        self.assertEqual(expected, 2_195_765)
        self.assertEqual(expected, math.comb(27, 8) - math.comb(17, 8))
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], expected
        )
        self.assertTrue(all(row["contracting"] for row in rows))
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))

    def test_seven_one_product_bound_closes_every_larger_horizon(self) -> None:
        threshold = Fraction(
            self.collatz["analytic_bound"]["bound_at_h_27"]["exact"]
        )
        self.assertEqual(
            threshold,
            Fraction(7_450_580_596_923_828_125, 7_996_018_508_417_728_512),
        )
        self.assertGreater(seven_one_product_bound(26), 1)
        self.assertLess(threshold, 1)
        self.assertTrue(
            all(
                seven_one_product_bound(horizon + 1)
                < seven_one_product_bound(horizon)
                for horizon in range(27, 256)
            )
        )

    def test_seven_one_transcript_is_deterministic(self) -> None:
        first = finite_seven_one_horizon_row(17)
        second = finite_seven_one_horizon_row(17)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], math.comb(17, 7))

    def test_goldbach_exact_budget_is_below_sublinear_coarse_bound(self) -> None:
        rows = self.goldbach["budget_reduction_rows"]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            self.goldbach["aggregate"]["exact_pointwise_budget_is_sufficient"]
        )
        self.assertFalse(
            self.goldbach["aggregate"]["positive_linear_lower_bound_is_necessary"]
        )
        self.assertFalse(
            self.goldbach["aggregate"]["actual_all_target_budget_excess_proved"]
        )

    def test_twin_exact_excess_has_arithmetic_block_granularity(self) -> None:
        rows = self.twin["finite_arithmetic_rows"]
        self.assertTrue(
            all(row["positive_excess_iff_twin_pair_in_block"] for row in rows)
        )
        self.assertTrue(all(row["positive_mass_respects_granularity"] for row in rows))
        self.assertFalse(
            self.twin["aggregate"]["infinitely_many_actual_positive_blocks_proved"]
        )

    def test_sparse_arithmetic_scale_mass_is_not_linear(self) -> None:
        rows = [sparse_arithmetic_scale_row(cutoff) for cutoff in [8, 16, 32, 64]]
        ratios = [
            Fraction(row["normalized_cumulative_over_2_to_J"]["exact"])
            for row in rows
        ]
        self.assertTrue(all(later < earlier for earlier, later in zip(ratios, ratios[1:])))
        self.assertTrue(all(row["positive_block_count"] > 0 for row in rows))
        self.assertFalse(self.twin["aggregate"]["positive_linear_density_is_necessary"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_cycle_stratum_closure_count": 1,
                "quantifier_matched_target_count": 3,
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
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket191-probe-sevenone-budget-granularity.json"
        )
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
