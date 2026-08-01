from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket178_toeplitz_lowbit_split_zeromode import (  # noqa: E402
    build_audit,
    collatz_lowbit_occupancy_audit,
    goldbach_frequency_split_audit,
    lowbit_occupancy_record,
    mersenne_lowbit_no_go,
    positive_split_counterfamily,
    riemann_toeplitz_threshold_audit,
    toeplitz_average_row_lower,
    toeplitz_max_row_sum,
    twin_zeromode_crossgram_audit,
)


class Ticket178ToeplitzLowBitSplitZeroModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_toeplitz_threshold_audit()
        cls.collatz = collatz_lowbit_occupancy_audit()
        cls.goldbach = goldbach_frequency_split_audit()
        cls.twin = twin_zeromode_crossgram_audit()

    def test_riemann_summability_threshold(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        rows = self.riemann["finite_profile_rows"]
        by_exponent = {row["decay_exponent_s"]: row for row in rows}
        self.assertFalse(by_exponent[1.0]["summable_profile_below_core_margin"])
        self.assertTrue(by_exponent[1.25]["summable_profile_below_core_margin"])
        self.assertTrue(by_exponent[2.0]["summable_profile_below_core_margin"])
        for exponent in (0.75, 1.0):
            last = by_exponent[exponent]["finite_sections"][-1]
            self.assertGreater(
                last["all_ones_rayleigh_lower_bound"],
                last.get("core_margin_delta", 0.25),
            )

    def test_toeplitz_rayleigh_lower_is_below_schur_upper(self) -> None:
        for exponent in (0.75, 1.0, 1.25, 2.0):
            lower = toeplitz_average_row_lower(64, exponent, 0.02)
            upper = toeplitz_max_row_sum(64, exponent, 0.02)
            self.assertLessEqual(lower, upper)

    def test_collatz_lowbit_layer_and_finite_audit(self) -> None:
        self.assertEqual(self.collatz["failure_count"], 0)
        finite = self.collatz["finite_first_descent_audit"]
        self.assertEqual(finite["odd_starts_checked"], 49_999)
        self.assertEqual(finite["lowbit_certificate_crossing_count"], 44_537)
        self.assertEqual(finite["lowbit_certificate_non_crossing_count"], 5_462)
        for start in (3, 27, 63, 703, 35_655):
            row = lowbit_occupancy_record(start)
            self.assertIsNotNone(row["first_descent_horizon"])
            self.assertLessEqual(row["layer_cake_lower_bound"], row["valuation_sum"])

    def test_mersenne_family_defeats_fixed_horizon_mixing(self) -> None:
        for exponent in (8, 16, 32, 64):
            row = mersenne_lowbit_no_go(exponent)
            self.assertEqual(row["all_one_valuation_prefix_length"], exponent - 2)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_frequency_split_is_honest_about_scale(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        rows = self.goldbach["finite_fixed_farey_split_rows"]
        self.assertGreater(rows[0]["passing_split_count"], 0)
        self.assertTrue(all(row["passing_split_count"] == 0 for row in rows[1:]))
        self.assertEqual(
            self.goldbach["aggregate"]["supports_with_passing_predeclared_split"],
            1,
        )

    def test_global_sobolev_budget_is_not_necessary(self) -> None:
        for frequency in (16, 64, 256, 1_024):
            row = positive_split_counterfamily(frequency)
            self.assertGreater(row["rigorous_pointwise_lower_bound"], 0)
            self.assertFalse(row["global_certificate_passes"])
            self.assertTrue(row["split_certificate_passes"])

    def test_twin_signed_zero_mode_preserves_phase(self) -> None:
        self.assertEqual(self.twin["failure_count"], 0)
        for row in self.twin["absolute_phase_erasure_counterfamilies"]:
            self.assertEqual(row["absolute_cross_gram_entry"], 1.0)
            self.assertAlmostEqual(
                row["aligned_signed_zero_mode"],
                row["component_count_m"] ** 2,
            )
            self.assertLess(row["root_of_unity_signed_zero_mode"], 1e-25)

    def test_machine_contract_and_json_are_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket178-toeplitz-lowbit-split-zeromode.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], audit["status"])
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(attempt["status"] == "open_not_proven" for attempt in payload["attempts"])
        )
        self.assertIn("T", payload["generated_at"])
        self.assertIn("+09:00", payload["generated_at"])
        self.assertNotIn("Infinity", path.read_text(encoding="utf-8"))
        self.assertNotIn("NaN", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
