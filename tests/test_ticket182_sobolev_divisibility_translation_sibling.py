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

from ticket182_sobolev_divisibility_translation_sibling import (  # noqa: E402
    build_audit,
    collatz_cycle_candidate,
    collatz_divisibility_audit,
    fejer_h1_tail_constant,
    goldbach_translation_audit,
    riemann_h1_audit,
    sibling_increment_identity,
    twin_sibling_audit,
    twin_sibling_counterfamily,
)


class Ticket182SobolevDivisibilityTranslationSiblingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_h1_audit()
        cls.collatz = collatz_divisibility_audit()
        cls.goldbach = goldbach_translation_audit()
        cls.twin = twin_sibling_audit()

    def test_fejer_h1_constant_decreases_and_certificates_hold(self) -> None:
        self.assertGreater(fejer_h1_tail_constant(8), fejer_h1_tail_constant(512))
        self.assertEqual(self.riemann["failure_count"], 0)
        for row in self.riemann["h1_certificate_rows"]:
            self.assertLess(row["smooth_certified_norm"], row["core_margin_delta"])
            self.assertEqual(row["hidden_grid_value_max"], 0.0)
            self.assertEqual(row["hidden_grid_derivative_max"], 0.0)
            self.assertEqual(row["hidden_true_uniform_norm"], 2.0)

    def test_raw_prime_proxy_h1_energy_is_not_a_uniform_budget(self) -> None:
        rows = self.riemann["raw_prime_proxy_rows"]
        self.assertEqual(rows[-1]["prime_proxy_cutoff_P"], 100_000)
        self.assertTrue(
            all(
                rows[index + 1]["normalized_derivative_l2_squared"]
                > rows[index]["normalized_derivative_l2_squared"]
                for index in range(len(rows) - 1)
            )
        )

    def test_collatz_cycle_is_equivalent_to_affine_divisibility(self) -> None:
        fixed_repeat = collatz_cycle_candidate((2, 2, 2, 2))
        self.assertTrue(fixed_repeat["cycle_divisibility_hit"])
        self.assertTrue(fixed_repeat["exact_cycle_transition"])
        self.assertTrue(fixed_repeat["is_trivial_fixed_point_repeat"])
        self.assertEqual(fixed_repeat["cycle_candidates"], [1, 1, 1, 1])
        noncycle = collatz_cycle_candidate((3, 1, 2))
        self.assertFalse(noncycle["cycle_divisibility_hit"])

    def test_collatz_finite_audit_keeps_universal_exclusion_open(self) -> None:
        aggregate = self.collatz["aggregate"]
        self.assertEqual(aggregate["words_checked"], 488_280)
        self.assertEqual(aggregate["divisibility_hits"], 8)
        self.assertEqual(aggregate["trivial_fixed_point_repeats"], 8)
        self.assertEqual(aggregate["nontrivial_cycle_candidates"], 0)
        self.assertEqual(self.collatz["failure_count"], 0)

    def test_goldbach_uniform_translation_bound_and_rms_no_go(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        for row in self.goldbach["translation_certificate_rows"]:
            self.assertLessEqual(
                row["smooth"]["actual_fejer_error"],
                row["smooth"]["weighted_uniform_translation_budget"] + 1e-12,
            )
            self.assertLessEqual(
                row["exceptional_spike"]["actual_fejer_error"],
                row["exceptional_spike"]["weighted_uniform_translation_budget"]
                + 1e-12,
            )
            self.assertLess(
                row["exceptional_spike"]["weighted_rms_translation_budget"],
                row["exceptional_spike"]["actual_fejer_error"],
            )
        finite = self.goldbach["finite_prime_indicator_diagnostic"]
        self.assertEqual(finite["even_target_limit"], 20_000)
        self.assertEqual(finite["block_target_count"], 5_000)

    def test_weighted_sibling_identity_and_mean_path_no_go(self) -> None:
        identity = sibling_increment_identity(3.0, 2.0, 5.0, -1.0)
        self.assertTrue(
            math.isclose(identity["left_increment"], identity["left_formula"])
        )
        self.assertTrue(
            math.isclose(identity["right_increment"], identity["right_formula"])
        )
        shallow = twin_sibling_counterfamily(4)
        deep = twin_sibling_counterfamily(20)
        self.assertLess(
            deep["sum_of_level_mean_increments"],
            shallow["sum_of_level_mean_increments"],
        )
        self.assertEqual(deep["selected_leaf_ratio"], 1.0)
        self.assertGreater(deep["selected_path_l1_variation"], 0.99)

    def test_finite_twin_tree_uses_actual_prime_pairs_but_stays_bounded(self) -> None:
        finite = self.twin["finite_prime_pair_diagnostic"]
        self.assertEqual(finite["interval_start"], 100_000)
        self.assertEqual(finite["interval_stop"], 362_144)
        self.assertGreater(finite["actual_twin_pair_count"], 0)
        self.assertLess(finite["maximum_sibling_identity_error"], 1e-12)
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
            / "ticket182-sobolev-divisibility-translation-sibling.json"
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
