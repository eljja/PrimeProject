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

from ticket181_regularized_localization_quantized_slack import (  # noqa: E402
    build_audit,
    collatz_quantization_audit,
    collatz_quantized_word,
    discrete_fejer_weights,
    fejer_first_moment,
    goldbach_fejer_audit,
    riemann_fejer_audit,
    twin_tree_localization_audit,
    twin_tree_row,
)


class Ticket181RegularizedLocalizationQuantizedSlackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_fejer_audit()
        cls.collatz = collatz_quantization_audit()
        cls.goldbach = goldbach_fejer_audit()
        cls.twin = twin_tree_localization_audit()

    def test_continuous_fejer_moment_and_certificate(self) -> None:
        self.assertGreater(fejer_first_moment(8), fejer_first_moment(256))
        self.assertEqual(self.riemann["failure_count"], 0)
        for row in self.riemann["fejer_certificate_rows"]:
            self.assertLess(
                row["smooth_model_certified_norm"], row["core_margin_delta"]
            )
            self.assertEqual(row["hidden_sine_sampled_values_max"], 0.0)
            self.assertEqual(row["hidden_sine_sampled_slope_max"], 0.0)
            self.assertEqual(row["hidden_sine_true_uniform_norm"], 1.0)

    def test_collatz_slack_is_one_quantum_or_more_after_equality_exclusion(self) -> None:
        item = collatz_quantized_word((3,))
        self.assertGreater(item["multiplier_gap_D"], 0)
        self.assertGreaterEqual(item["descent_slack_H"], item["cylinder_modulus_M"])
        self.assertEqual(
            item["descent_slack_H"] % item["cylinder_modulus_M"], 0
        )
        self.assertTrue(all(item["checks"].values()))

    def test_collatz_fixed_point_proves_equality_exclusion_is_necessary(self) -> None:
        boundary = self.collatz["fixed_point_boundary"]
        self.assertEqual(boundary["valuation_word"], [2])
        self.assertEqual(boundary["least_cylinder_representative"], 1)
        self.assertEqual(boundary["odd_endpoint"], 1)
        self.assertEqual(boundary["descent_slack_H"], 0)
        self.assertFalse(boundary["least_representative_descends"])
        self.assertEqual(self.collatz["failure_count"], 0)

    def test_discrete_fejer_kernel_and_exception_removal_budget(self) -> None:
        weights = discrete_fejer_weights(64, 8)
        self.assertTrue(all(weight >= -1e-14 for weight in weights))
        self.assertTrue(math.isclose(sum(weights), 1.0, abs_tol=1e-12))
        self.assertEqual(self.goldbach["failure_count"], 0)
        for row in self.goldbach["discrete_fejer_rows"]:
            self.assertGreater(row["smooth_model"]["certificate_margin"], 0.0)
            self.assertLessEqual(
                row["exceptional_spike"]["certificate_margin"], 0.0
            )

    def test_goldbach_counterexample_search_is_explicitly_finite(self) -> None:
        search = self.goldbach["finite_exact_search"]
        self.assertEqual(search["even_target_limit"], 100_000)
        self.assertEqual(search["even_targets_checked"], 49_999)
        self.assertFalse(search["counterexample_found"])
        self.assertIsNone(search["first_counterexample"])

    def test_dyadic_path_l2_no_go_and_l1_localization(self) -> None:
        shallow = twin_tree_row(8)
        deep = twin_tree_row(128)
        self.assertLess(
            deep["maximum_single_edge_oscillation"],
            shallow["maximum_single_edge_oscillation"],
        )
        self.assertLess(
            deep["bad_path_l2_oscillation"],
            shallow["bad_path_l2_oscillation"],
        )
        self.assertEqual(deep["bad_path_l1_oscillation"], 1.0)
        self.assertEqual(deep["bad_path_leaf_ratio"], 1.0)
        self.assertEqual(self.twin["failure_count"], 0)

    def test_machine_contract_and_json_keep_all_conjectures_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["exact_theorem_count"], 4)
        self.assertEqual(audit["machine_audit"]["rejected_target_count"], 4)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket181-regularized-localization-quantized-slack.json"
        )
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(item["status"] == "open_not_proven" for item in payload["attempts"])
        )
        self.assertNotIn(": Infinity", text)
        self.assertNotIn(": -Infinity", text)
        self.assertNotIn(": NaN", text)


if __name__ == "__main__":
    unittest.main()
