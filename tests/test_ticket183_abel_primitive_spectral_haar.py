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

from ticket183_abel_primitive_spectral_haar import (  # noqa: E402
    abel_high_frequency_row,
    build_audit,
    collatz_word_data,
    fourier_margin_certificate,
    haar_global_energy_counterfamily,
    primitive_root,
    repetition_identity_row,
    weighted_haar_tree,
)


class Ticket183AbelPrimitiveSpectralHaarTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_abel_certificate_keeps_the_desmoothing_remainder(self) -> None:
        row = abel_high_frequency_row(0.9, 128, 16, 0.25)
        self.assertLess(row["smoothed_only_certificate"], 0.25)
        self.assertEqual(row["original_uniform_norm"], 1.0)
        self.assertGreater(row["explicit_desmoothing_remainder"], 0.999998)
        self.assertGreaterEqual(row["full_certificate"], 1.0 - 1e-12)

    def test_abel_high_frequency_family_refutes_smoothing_only_transfer(self) -> None:
        rows = self.riemann["high_frequency_counterfamily"]
        self.assertTrue(
            all(
                rows[index + 1]["smoothed_only_certificate"]
                < rows[index]["smoothed_only_certificate"]
                for index in range(len(rows) - 1)
            )
        )
        self.assertTrue(self.riemann["aggregate"]["desmoothing_remainder_tends_to_one"])
        self.assertEqual(self.riemann["failure_count"], 0)

    def test_abel_prime_proxy_is_finite_but_not_a_weil_certificate(self) -> None:
        rows = self.riemann["abel_prime_proxy_diagnostic"]
        self.assertEqual(rows[-1]["prime_proxy_cutoff_P"], 100_000)
        self.assertTrue(
            all(
                rows[index + 1]["abel_derivative_l2_squared"]
                > rows[index]["abel_derivative_l2_squared"]
                for index in range(len(rows) - 1)
            )
        )

    def test_primitive_root_is_unique_for_test_words(self) -> None:
        self.assertEqual(primitive_root((1, 2, 3) * 4), ((1, 2, 3), 4))
        self.assertEqual(primitive_root((1, 2, 2, 1)), ((1, 2, 2, 1), 1))

    def test_repetition_factors_numerator_and_denominator_together(self) -> None:
        row = repetition_identity_row((1, 2, 3), 5)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(
            row["root_divisibility_hit"], row["repeated_divisibility_hit"]
        )

    def test_all_valuation_at_least_two_cycle_hit_is_only_fixed_point(self) -> None:
        fixed = collatz_word_data((2, 2, 2, 2))
        self.assertTrue(fixed["cycle_divisibility_hit"])
        self.assertEqual(fixed["cycle_candidate"], 1)
        aggregate = self.collatz["aggregate"]
        self.assertEqual(aggregate["all_valuations_at_least_two_nontrivial_hits"], 0)
        self.assertEqual(aggregate["all_valuations_at_least_two_words_checked"], 87_380)

    def test_finite_horizon_does_not_exhaust_primitive_contracting_words(self) -> None:
        rows = self.collatz["unbounded_primitive_contracting_family"]
        self.assertEqual(rows[-1]["horizon_h"], 32)
        self.assertTrue(
            all(
                row["is_primitive"]
                and row["is_contracting"]
                and row["contains_valuation_one"]
                for row in rows
            )
        )

    def test_fourier_margin_identity_and_certificate(self) -> None:
        length = 32
        major = [1.0] * length
        actual = [
            1.0 + 0.01 * math.cos(6.0 * math.pi * index / length)
            for index in range(length)
        ]
        row = fourier_margin_certificate(actual, major)
        self.assertLess(row["exact_fourier_identity_error"], 1e-12)
        self.assertTrue(row["certificate_passes"])
        self.assertGreater(row["actual_convolution_minimum"], 0.0)

    def test_sparse_constant_density_certificate_is_impossible(self) -> None:
        rows = self.goldbach["sparse_prime_indicator_no_go_rows"]
        self.assertTrue(
            all(
                row["phase_blind_budget_alpha_one_minus_alpha"]
                >= row["constant_model_margin_alpha_squared"]
                for row in rows
            )
        )
        self.assertTrue(
            all(not row["constant_model_certificate_passes"] for row in rows)
        )

    def test_finite_goldbach_check_stays_explicitly_finite(self) -> None:
        finite = self.goldbach["finite_strong_goldbach_diagnostic"]
        self.assertEqual(finite["even_target_limit"], 50_000)
        self.assertEqual(finite["counterexamples_found"], [])
        self.assertGreaterEqual(
            finite["minimum_unordered_odd_prime_representation_count"], 1
        )

    def test_weighted_haar_variance_identity_and_path_certificate(self) -> None:
        audit = weighted_haar_tree(
            [0.25, 0.25, 0.25, 0.25], [1.0, 1.1, 0.9, 1.0]
        )
        self.assertLess(audit["variance_identity_error"], 1e-14)
        self.assertTrue(audit["all_leaf_certificates_pass"])
        self.assertGreater(audit["minimum_actual_leaf_ratio"], 0.0)

    def test_global_haar_energy_does_not_control_one_bad_path(self) -> None:
        shallow = haar_global_energy_counterfamily(4)
        deep = haar_global_energy_counterfamily(16)
        self.assertLess(deep["global_haar_energy"], shallow["global_haar_energy"])
        self.assertEqual(deep["selected_bad_leaf_ratio"], 0.0)
        self.assertGreater(deep["selected_negative_path_square"], 0.3)

    def test_finite_twin_tree_verifies_identity_but_not_uniform_certificate(self) -> None:
        finite = self.twin["finite_prime_pair_haar_diagnostic"]
        self.assertEqual(finite["actual_twin_pair_count"], 2_298)
        self.assertLess(finite["variance_identity_error"], 1e-12)
        self.assertFalse(finite["all_leaf_certificates_pass"])
        self.assertGreater(finite["minimum_actual_leaf_ratio"], 0.0)

    def test_machine_contract_and_json_keep_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket183-abel-primitive-spectral-haar.json"
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

    def test_proof_dag_uses_only_closed_ticket182_results_as_inputs(self) -> None:
        expected_inputs = {
            "riemann": "FejerH1TailCertificateAndRawPrimeEnergyNoGo",
            "collatz": "AcceleratedCycleIffAffineDivisibility",
            "goldbach": "WeightedTranslationModulusCertificateAndRmsSpikeNoGo",
            "twin_prime": "WeightedSiblingContrastIdentityAndMeanPathNoGo",
        }
        for section_name, expected_label in expected_inputs.items():
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[0]["status"], "proved_exact_input")
            self.assertEqual(nodes[0]["label"], expected_label)
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_goldbach_name_does_not_overstate_phase_control(self) -> None:
        section = self.audit["goldbach"]
        self.assertEqual(
            section["theorem_name"],
            "ExactFourierErrorIdentityAndSparseDensityNoGo",
        )
        self.assertIn("phase-blind", section["route_decision"]["discard"])


if __name__ == "__main__":
    unittest.main()
