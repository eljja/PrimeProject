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

from ticket192_uniform_eightone_weighted_envelope import (  # noqa: E402
    build_audit,
    eight_one_product_bound,
    finite_eight_one_horizon_row,
    unbounded_core_row,
)


class Ticket192UniformEightOneWeightedEnvelopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_pointwise_core_convergence_does_not_supply_uniform_bound(self) -> None:
        rows = self.riemann["finite_section_counterexample_rows"]
        self.assertTrue(all(row["positive_semidefinite"] for row in rows))
        self.assertEqual(
            [row["operator_norm"] for row in rows], [2, 4, 8, 16, 32, 64]
        )
        self.assertFalse(
            self.riemann["extension_contract"][
                "pointwise_dense_core_cauchy_is_sufficient"
            ]
        )
        self.assertFalse(
            self.riemann["extension_contract"][
                "actual_pole_neutral_weil_uniform_bound_verified"
            ]
        )

    def test_unbounded_coordinate_witness_is_exact(self) -> None:
        row = unbounded_core_row(37)
        self.assertEqual(row["unit_coordinate_witness"], 37)
        self.assertEqual(row["witness_quadratic_value"], 37)
        self.assertEqual(row["operator_norm"], 37)

    def test_eight_one_rotation_normalized_range_is_exhaustive(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(20, 31)))
        expected = sum(math.comb(horizon - 1, 7) for horizon in range(20, 31))
        self.assertEqual(expected, 5_777_343)
        self.assertEqual(expected, math.comb(30, 8) - math.comb(19, 8))
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], expected
        )
        self.assertTrue(all(row["contracting"] for row in rows))
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))

    def test_eight_one_product_bound_closes_all_larger_horizons(self) -> None:
        threshold = Fraction(
            self.collatz["analytic_bound"]["bound_at_h_31"]["exact"]
        )
        self.assertGreater(eight_one_product_bound(30), 1)
        self.assertLess(threshold, 1)
        self.assertEqual(threshold, Fraction(256 * 5**31, 6**31))
        self.assertTrue(
            all(
                eight_one_product_bound(horizon + 1)
                < eight_one_product_bound(horizon)
                for horizon in range(31, 256)
            )
        )

    def test_eight_one_transcript_is_deterministic(self) -> None:
        first = finite_eight_one_horizon_row(20)
        second = finite_eight_one_horizon_row(20)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], math.comb(19, 7))

    def test_goldbach_weighted_envelope_halves_count_budget(self) -> None:
        rows = self.goldbach["weighted_budget_rows"]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(
                row["weighted_contamination_envelope"]
                <= row["ticket191_simplified_budget"] / 2.0 + 1e-9
                for row in rows
            )
        )
        self.assertEqual(
            self.goldbach["aggregate"]["finite_sample_budget_excess_count"],
            len(rows),
        )
        self.assertFalse(self.goldbach["aggregate"]["all_large_even_targets_proved"])

    def test_twin_local_weighted_envelope_is_sufficient_only_finitely(self) -> None:
        rows = self.twin["finite_dyadic_rows"]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertEqual(
            self.twin["aggregate"]["finite_block_envelope_success_count"],
            len(rows),
        )
        self.assertFalse(
            self.twin["aggregate"]["infinitely_many_envelope_successes_proved"]
        )

    def test_weighted_prime_power_bridge_is_shared(self) -> None:
        self.assertTrue(
            self.goldbach["aggregate"]["weighted_envelope_theorem_proved"]
        )
        self.assertTrue(
            self.twin["aggregate"]["local_weighted_envelope_theorem_proved"]
        )
        self.assertTrue(
            self.goldbach["aggregate"]["count_budget_factor_two_removed"]
        )
        self.assertTrue(self.twin["aggregate"]["count_budget_factor_two_removed"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_cycle_stratum_closure_count": 1,
                "weighted_envelope_bridge_count": 2,
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
            / "ticket192-uniform-eightone-weighted-envelope.json"
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
