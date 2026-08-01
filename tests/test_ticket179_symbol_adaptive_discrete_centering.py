from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket179_symbol_adaptive_discrete_centering import (  # noqa: E402
    build_audit,
    collatz_adaptive_layer_audit,
    discrete_interpolation_counterexample,
    fixed_depth_counterexample,
    goldbach_discrete_target_audit,
    riemann_bounded_symbol_audit,
    square_wave_fourier_coefficient,
    twin_centering_audit,
    valuation_layer_sum,
)


class Ticket179SymbolAdaptiveDiscreteCenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_bounded_symbol_audit()
        cls.collatz = collatz_adaptive_layer_audit()
        cls.goldbach = goldbach_discrete_target_audit()
        cls.twin = twin_centering_audit()

    def test_riemann_bounded_symbol_beats_absolute_row_sum(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        aggregate = self.riemann["aggregate"]
        self.assertTrue(aggregate["bounded_symbol_certificate_passes"])
        self.assertTrue(aggregate["absolute_row_sum_crosses_margin"])
        rows = self.riemann["square_wave_counterfamily"]["finite_sections"]
        self.assertTrue(all(abs(row["fejer_rayleigh_at_zero"]) <= 0.2 for row in rows))
        self.assertGreater(rows[-1]["absolute_row_sum"], rows[0]["absolute_row_sum"])
        self.assertEqual(square_wave_fourier_coefficient(2, 0.2), 0.0)

    def test_adaptive_layer_cake_is_exact(self) -> None:
        valuations = [1, 3, 2, 5]
        self.assertEqual(valuation_layer_sum(valuations), sum(valuations))
        self.assertEqual(valuation_layer_sum(valuations, 2), 7)

    def test_every_tested_fixed_depth_has_a_first_descent_counterexample(self) -> None:
        self.assertEqual(self.collatz["failure_count"], 0)
        for depth in (2, 4, 8, 16):
            row = fixed_depth_counterexample(depth)
            self.assertTrue(all(row["checks"].values()))
            self.assertGreater(row["exact_valuation_sum"], row["exact_log_boundary"])
            self.assertLessEqual(row["fixed_depth_layer_sum"], row["exact_log_boundary"])

    def test_continuous_positivity_is_not_necessary_on_a_grid(self) -> None:
        for size in (8, 16, 32, 64):
            row = discrete_interpolation_counterexample(size)
            self.assertTrue(all(row["checks"].values()))
            self.assertGreater(row["minimum_grid_value"], 0.0)
            self.assertLess(row["minimum_continuous_value"], 0.0)

    def test_finite_goldbach_grid_is_explicitly_bounded(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        rows = self.goldbach["finite_exact_goldbach_grid_rows"]
        self.assertEqual(rows[-1]["even_target_limit"], 1_024)
        self.assertTrue(all(row["all_discrete_targets_positive"] for row in rows))

    def test_twin_centering_identity_and_incoherence_no_go(self) -> None:
        self.assertEqual(self.twin["failure_count"], 0)
        for row in self.twin["centering_counterfamilies"]:
            self.assertTrue(all(row["checks"].values()))
            orthonormal = row["families"]["orthonormal"]
            roots = row["families"]["roots_of_unity"]
            self.assertEqual(orthonormal["maximum_pairwise_coherence"], 0.0)
            self.assertAlmostEqual(orthonormal["zero_mode_to_diagonal_ratio"], 1.0)
            self.assertLess(roots["signed_zero_mode_Z"], 1e-25)

    def test_machine_contract_and_json_keep_all_conjectures_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        path = ROOT / "data" / "open-problem" / "ticket179-symbol-adaptive-discrete-centering.json"
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(all(item["status"] == "open_not_proven" for item in payload["attempts"]))
        self.assertNotIn("Infinity", text)
        self.assertNotIn("NaN", text)


if __name__ == "__main__":
    unittest.main()
