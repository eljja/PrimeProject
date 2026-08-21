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

import ticket233_logarithmic_frame_density_shell_entropy as ticket233  # noqa: E402


class Ticket233LogarithmicFrameDensityShellEntropyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket233.build_audit()
        cls.root = cls.audit[ticket233.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket233.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertIn("resolves none", self.audit["claim_boundary"])
        self.assertEqual(
            self.root["machine_audit"],
            {
                "exact_partial_theorem_count": 4,
                "refuted_or_corrected_route_count": 4,
                "next_single_lemma_count": 4,
                "proof_dag_count": 4,
                "lineage_regression_correction_count": 1,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        self.assertEqual(
            {row["problem_id"] for row in self.audit["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )

    def test_riemann_logarithmic_scalar_threshold_is_sharp(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        for row in computation["deterministic_seeded_frame_rows"]:
            self.assertTrue(row["certificate_verified"])
            self.assertGreaterEqual(row["minimum_normalized_energy"], 1.0)
            self.assertLessEqual(row["hoeffding_union_failure_bound"], 0.5)
            self.assertGreater(
                row["prime_phase_modulus_P"], row["frequency_horizon_T"]
            )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["logarithmic_scalar_adaptive_frame_exists"])
        self.assertTrue(
            aggregate["ticket232_logarithmic_lower_bound_sharp_for_scalar_energy"]
        )
        self.assertFalse(aggregate["actual_weil_quadratic_form_transfer_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_lineage_k12_mitm_and_noncofinality(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["stratum_closed"]
                for row in computation["arbitrary_tail_closed_multiplicity_lineage_rows"]
            )
        )
        binary_rows = computation["binary_closed_multiplicity_lineage_rows"]
        self.assertEqual([row["valuation_one_count_k"] for row in binary_rows], list(range(4, 12)))
        self.assertTrue(all(row["stratum_closed"] for row in binary_rows))
        validation = computation["twelve_one_boundary_validation"]
        self.assertEqual(validation["exhaustive_normalized_words_checked"], 18_564)
        self.assertEqual(validation["exhaustive_formula_mismatch_count"], 0)
        self.assertEqual(validation["seeded_samples_checked"], 2_176)
        self.assertEqual(validation["seeded_formula_mismatch_count"], 0)
        totals = computation["twelve_one_finite_horizon_totals"]
        self.assertEqual(totals["finite_exact_horizons"], [29, 45])
        self.assertEqual(totals["left_tuple_count"], 7_768_320)
        self.assertEqual(totals["right_tuple_count"], 18_398_403)
        self.assertEqual(totals["represented_normalized_words"], 28_729_599_990)
        self.assertEqual(totals["represented_normalized_words"], totals["expected_normalized_words"])
        self.assertEqual(totals["divisibility_hits"], 0)
        self.assertGreater(Fraction(totals["product_bound_at_h45"]["exact"]), 1)
        self.assertLess(Fraction(totals["product_bound_at_h46"]["exact"]), 1)
        rows = computation["twelve_one_finite_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(29, 46)))
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertEqual(
            rows[0]["mitm_transcript_sha256"],
            "657fb3699f36c2080f1dc8e36dcd66675b8e5d153909ad25f4be86f56aeed564",
        )
        regression = computation["finite_density_band_scan_totals"]
        self.assertEqual(regression["raw_binary_words"], 1_893_010)
        self.assertEqual(regression["primitive_necklaces"], 90_272)
        self.assertEqual(regression["divisibility_hits"], 0)
        self.assertTrue(regression["regression_only"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["binary_exactly_twelve_positive_cycle_stratum_excluded"])
        self.assertEqual(aggregate["binary_remaining_multiplicity_lower_bound_k"], 13)
        self.assertEqual(aggregate["general_remaining_multiplicity_lower_bound_k"], 8)
        self.assertTrue(aggregate["finite_fixed_multiplicity_ladder_noncofinal"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_squarefree_shell_parseval_and_sparse_no_go(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertTrue(
            all(row["certificate_verified"] for row in computation["squarefree_indicator_algebra_rows"])
        )
        self.assertTrue(
            all(row["parseval_identity_verified"] for row in computation["prime_modulus_parseval_rows"])
        )
        sparse = computation["actual_prime_sparse_denominator_no_go_rows"]
        self.assertTrue(all(row["certificate_verified"] for row in sparse))
        self.assertTrue(
            all(
                int(row["correction_to_mu_squared_ratio"])
                == row["expected_ratio_l_times_l_minus_2"]
                for row in sparse
            )
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["polylogarithmic_squarefree_prime_shell_asymptotic_proved"])
        self.assertTrue(aggregate["unrestricted_growing_denominator_actual_prime_asymptotic_refuted"])
        self.assertFalse(aggregate["minor_arc_negative_mass_controlled"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_critical_entropy_and_parity_retention_no_go(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        rows = computation["critical_entropy_exact_rows"]
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        signed = [Fraction(row["centered_even_mixture_signed_aggregate"]["exact"]) for row in rows]
        self.assertTrue(all(value > 0 for value in signed))
        self.assertAlmostEqual(
            float(signed[-1]), math.cosh(0.5) - 1.0, delta=0.005
        )
        self.assertTrue(
            all(row["certificate_verified"] for row in computation["full_parity_retention_no_go_rows"]
        ))
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["signed_product_damping_large_sieve_bound_proved"])
        self.assertTrue(aggregate["critical_entropy_plus_centered_marginals_saving_refuted"])
        self.assertTrue(aggregate["bounded_entropy_product_damping_full_parity_retention_refuted"])
        self.assertFalse(aggregate["positive_twin_main_term_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_each_track_has_one_successor_and_a_guarded_proof_dag(self) -> None:
        for problem in ("riemann", "collatz", "goldbach", "twin_prime"):
            track = self.root[problem]
            self.assertTrue(track["route_decision"]["next_single_lemma"])
            statuses = {node["status"] for node in track["proof_dag"]["nodes"]}
            self.assertIn("closed", statuses)
            self.assertIn("refuted_or_limited", statuses)
            self.assertIn("highest_risk_open", statuses)
            self.assertIn("open_not_proven", statuses)

    def test_outputs_are_reproducible(self) -> None:
        ticket233.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket233-logarithmic-frame-density-shell-entropy.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket233.SCHEMA)
        machine = integrated[ticket233.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
