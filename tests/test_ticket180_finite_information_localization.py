from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket180_finite_information_localization import (  # noqa: E402
    build_audit,
    collatz_order_audit,
    collatz_order_pair,
    exceptional_spike_row,
    goldbach_spike_audit,
    ordered_affine_numerator,
    riemann_hidden_frequency_audit,
    toeplitz_section,
    twin_block_localization_audit,
    twin_block_row,
    valuation_layers,
)


class Ticket180FiniteInformationLocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_hidden_frequency_audit()
        cls.collatz = collatz_order_audit()
        cls.goldbach = goldbach_spike_audit()
        cls.twin = twin_block_localization_audit()

    def test_hidden_fourier_mode_leaves_finite_toeplitz_section_unchanged(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        for row in self.riemann["hidden_frequency_counterfamily"]:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(row["finite_section_max_difference"], 0.0)
            self.assertGreater(
                row["perturbed_symbol_value_at_zero"], row["core_margin_delta"]
            )
        base = toeplitz_section(8, 0.2)
        hidden = toeplitz_section(8, 0.2, 17, 1.0)
        self.assertEqual(base, hidden)

    def test_ordered_affine_numerator_depends_on_permutation(self) -> None:
        early = (2, 1, 1)
        delayed = (1, 2, 1)
        self.assertEqual(valuation_layers(early), valuation_layers(delayed))
        self.assertEqual(valuation_layers(early), (3, 1))
        self.assertNotEqual(
            ordered_affine_numerator(early), ordered_affine_numerator(delayed)
        )

    def test_natural_collatz_counterpair_has_different_first_descent(self) -> None:
        pair = collatz_order_pair(2)
        self.assertTrue(all(pair["checks"].values()))
        early, delayed = pair["ordered_realizations"]
        self.assertEqual(early["cylinder_representative"], 9)
        self.assertEqual(early["states"], [9, 7, 11, 17])
        self.assertEqual(early["first_descent_time"], 1)
        self.assertEqual(delayed["cylinder_representative"], 27)
        self.assertEqual(delayed["states"], [27, 41, 31, 47])
        self.assertIsNone(delayed["first_descent_time"])
        self.assertEqual(self.collatz["failure_count"], 0)

    def test_exceptional_spike_breaks_positivity_as_rms_vanishes(self) -> None:
        small = exceptional_spike_row(16)
        large = exceptional_spike_row(4096)
        self.assertTrue(all(small["checks"].values()))
        self.assertTrue(all(large["checks"].values()))
        self.assertLess(large["normalized_minor_rms"], small["normalized_minor_rms"])
        self.assertLess(large["minimum_major_plus_minor"], 0.0)
        self.assertEqual(self.goldbach["failure_count"], 0)

    def test_finite_goldbach_check_remains_explicitly_bounded(self) -> None:
        rows = self.goldbach["finite_exact_goldbach_rows"]
        self.assertEqual(rows[-1]["even_target_limit"], 10_000)
        self.assertTrue(all(not row["counterexample_found"] for row in rows))
        self.assertTrue(all(row["minimum_ordered_goldbach_count"] > 0 for row in rows))

    def test_global_twin_energy_can_hide_one_bad_block(self) -> None:
        first = twin_block_row(8, 8)
        last = twin_block_row(8, 2048)
        self.assertTrue(all(first["checks"].values()))
        self.assertTrue(all(last["checks"].values()))
        self.assertLess(
            last["global_zero_mode_to_diagonal_ratio"],
            first["global_zero_mode_to_diagonal_ratio"],
        )
        self.assertEqual(last["bad_block_zero_mode_to_diagonal_ratio"], 8)
        self.assertEqual(self.twin["failure_count"], 0)

    def test_machine_contract_and_json_keep_all_conjectures_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["exact_theorem_count"], 4)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket180-finite-information-localization.json"
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
