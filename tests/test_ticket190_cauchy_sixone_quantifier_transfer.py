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

from ticket190_cauchy_sixone_quantifier_transfer import (  # noqa: E402
    alternating_cauchy_pair_row,
    alternating_positive_core_row,
    build_audit,
    compatible_diagonal_core_row,
    finite_six_one_horizon_row,
    goldbach_sparse_hole_row,
    six_one_product_bound,
    sparse_block_model_row,
)


class Ticket190CauchySixOneQuantifierTransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_alternating_core_has_direct_cauchy_modulus(self) -> None:
        row = alternating_positive_core_row(32)
        self.assertTrue(row["positive"])
        self.assertEqual(
            Fraction(row["next_adjacent_drift_norm"]["exact"]), Fraction(1, 33)
        )
        for left, right in [(4, 9), (8, 17), (16, 33), (32, 65)]:
            pair = alternating_cauchy_pair_row(left, right)
            self.assertTrue(pair["difference_below_modulus"])
            self.assertLessEqual(
                Fraction(pair["exact_core_difference"]["exact"]),
                Fraction(pair["alternating_cauchy_modulus"]["exact"]),
            )

    def test_absolute_summable_drift_is_not_necessary(self) -> None:
        family = self.riemann["alternating_nonsummable_family"]
        self.assertTrue(family["direct_cauchy_modulus_proved"])
        self.assertFalse(family["absolute_adjacent_drift_sum_converges"])
        self.assertFalse(
            self.riemann["promotion_contract"][
                "actual_pole_neutral_weil_cauchy_modulus_verified"
            ]
        )

    def test_uniform_bound_is_exact_l2_extension_boundary(self) -> None:
        bounded = compatible_diagonal_core_row(64, True)
        unbounded = compatible_diagonal_core_row(64, False)
        self.assertEqual(Fraction(bounded["operator_norm"]["exact"]), 1)
        self.assertEqual(Fraction(unbounded["operator_norm"]["exact"]), 64)
        self.assertTrue(
            self.riemann["bounded_extension_family"]["bounded_l2_extension_exists"]
        )
        self.assertFalse(
            self.riemann["unbounded_extension_counterfamily"][
                "bounded_l2_extension_exists"
            ]
        )

    def test_six_one_finite_exception_range_is_exhaustive(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(15, 23)))
        expected = sum(math.comb(horizon, 6) for horizon in range(15, 23))
        self.assertEqual(expected, 238_722)
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], expected
        )
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))
        self.assertTrue(all(row["contracting"] for row in rows))

    def test_six_one_product_bound_closes_every_larger_horizon(self) -> None:
        threshold = Fraction(
            self.collatz["analytic_bound"]["bound_at_h_23"]["exact"]
        )
        self.assertEqual(
            threshold, Fraction(11_920_928_955_078_125, 12_339_534_735_212_544)
        )
        self.assertLess(threshold, 1)
        self.assertGreater(six_one_product_bound(22), 1)
        self.assertTrue(
            all(
                six_one_product_bound(horizon + 1)
                < six_one_product_bound(horizon)
                for horizon in range(23, 256)
            )
        )

    def test_six_one_transcript_is_deterministic(self) -> None:
        first = finite_six_one_horizon_row(22)
        second = finite_six_one_horizon_row(22)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], math.comb(22, 6))

    def test_goldbach_sparse_holes_preserve_average_mass(self) -> None:
        rows = [goldbach_sparse_hole_row(2**exponent) for exponent in range(8, 17)]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(
                later["hole_density"] < earlier["hole_density"]
                for earlier, later in zip(rows, rows[1:])
            )
        )
        self.assertTrue(
            all(
                later["relative_average_deficit"]
                < earlier["relative_average_deficit"]
                for earlier, later in zip(rows, rows[1:])
            )
        )
        self.assertTrue(
            self.goldbach["aggregate"]["density_one_promotion_refuted"]
        )
        self.assertFalse(
            self.goldbach["aggregate"]["pointwise_major_minor_lower_bound_proved"]
        )

    def test_sparse_unbounded_twin_mass_is_not_linear(self) -> None:
        rows = [sparse_block_model_row(exponent) for exponent in [4, 8, 16, 32]]
        ratios = [
            Fraction(row["normalized_cumulative_mass"]["exact"]) for row in rows
        ]
        self.assertTrue(all(later < earlier for earlier, later in zip(ratios, ratios[1:])))
        self.assertTrue(
            self.twin["aggregate"]["linear_cumulative_to_block_transfer_proved"]
        )
        self.assertFalse(
            self.twin["aggregate"]["unbounded_mass_implies_linear_limsup"]
        )
        self.assertFalse(self.twin["aggregate"]["unbounded_exact_excess_proved"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_cycle_stratum_closure_count": 1,
                "quantifier_or_topology_boundary_count": 3,
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
        path = ROOT / "data" / "open-problem" / "ticket190-cauchy-sixone-quantifier-transfer.json"
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
