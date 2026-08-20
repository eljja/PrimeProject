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

import ticket231_summable_frame_critical_strip_gauss_crt as ticket231  # noqa: E402


class Ticket231SummableFrameCriticalStripGaussCRTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket231.build_audit()
        cls.root = cls.audit["summable_frame_critical_strip_gauss_crt_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket231.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_summable_head_tail_certificates(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["weighted_head_tail_rows"]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertTrue(row["certificate_verified"])
            self.assertLessEqual(
                row["witness_frequency_n"], row["maximum_frequency_Q_to_M"]
            )
            self.assertLessEqual(
                row["observed_head_energy"], row["head_energy_bound"] + 1e-11
            )
            self.assertEqual(
                Fraction(row["exact_tail_weight_mass"]),
                Fraction(1, 2 ** row["head_size_M"]),
            )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["summable_infinite_dilation_liminf_zero_proved"])
        self.assertTrue(
            aggregate["positive_uniform_floor_for_fixed_summable_frame_refuted"]
        )
        self.assertFalse(aggregate["height_adaptive_or_renormalized_frame_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_rotation_excludes_average_two_except_trivial_word(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        for row in section["mixed_word_certificate_samples"]:
            word = tuple(row["certificate_rotation"])
            self.assertTrue(ticket231.suffix_condition(word))
            self.assertGreater(ticket231.collatz_numerator(word), 0)
            self.assertLess(
                ticket231.collatz_numerator(word),
                ticket231.collatz_denominator(word),
            )
        for row in section["height_rows"]:
            self.assertEqual(row["all_two_equality_word_count"], 1)
            self.assertEqual(
                row["strict_nontrivial_exclusions"],
                row["words_with_S_at_least_2h"] - 1,
            )
        for height in range(1, 8):
            word = (2,) * height
            self.assertEqual(
                ticket231.collatz_numerator(word),
                ticket231.collatz_denominator(word),
            )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["nontrivial_cycle_critical_strip_proved"])
        self.assertFalse(aggregate["critical_strip_nondivisibility_proved"])
        self.assertFalse(aggregate["aperiodic_descent_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_true_zero_convolution_gauss_counterfamily(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        rows = section["quadratic_residue_counterfamily_rows"]
        self.assertGreaterEqual(len(rows), 10)
        for row in rows:
            prime = row["prime_p"]
            mass = row["nonzero_quadratic_residue_count_W"]
            self.assertEqual(prime % 4, 3)
            self.assertEqual(mass, (prime - 1) // 2)
            self.assertEqual(row["convolution_at_zero"], 0)
            self.assertAlmostEqual(
                row["nonprincipal_coefficient_magnitude"],
                math.sqrt(prime + 1) / 2,
            )
            self.assertEqual(
                Fraction(row["exact_expected_signed_aggregate"]),
                -Fraction(mass * mass, prime),
            )
            self.assertTrue(row["certificate_verified"])
        self.assertLess(
            rows[-1]["maximum_mode_to_mass_ratio"],
            rows[0]["maximum_mode_to_mass_ratio"],
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["true_zero_convolution_counterfamily_proved"])
        self.assertTrue(aggregate["ticket230_spike_positivity_overclaim_corrected"])
        self.assertFalse(aggregate["prime_specific_minor_arc_bound_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_centered_crt_gram_matrix_is_exactly_diagonal(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        mod_three = next(
            row for row in section["local_centered_rows"] if row["prime_l"] == 3
        )
        self.assertTrue(mod_three["degenerate_zero_mode"])
        self.assertEqual(Fraction(mod_three["centered_variance"]), 0)
        for row in section["local_centered_rows"]:
            self.assertTrue(row["certificate_verified"])
            self.assertEqual(
                Fraction(row["centered_variance"]),
                Fraction(row["expected_variance"]),
            )
        for row in section["crt_product_gram_rows"]:
            self.assertTrue(row["gram_identity_verified"])
            self.assertEqual(Fraction(row["maximum_exact_off_diagonal"]), 0)
            self.assertEqual(row["orthogonal_mode_count"], 2 ** len(row["active_primes"]))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["centered_crt_interaction_orthogonality_proved"])
        self.assertFalse(aggregate["full_local_function_basis_claimed"])
        self.assertFalse(aggregate["prime_weighted_growing_modulus_saving_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_each_track_has_one_open_successor_and_claim_guard(self) -> None:
        for problem in ("riemann", "collatz", "goldbach", "twin_prime"):
            track = self.root[problem]
            self.assertTrue(track["route_decision"]["next_single_lemma"])
            statuses = {node["status"] for node in track["proof_dag"]["nodes"]}
            self.assertEqual(
                statuses,
                {
                    "closed",
                    "refuted_or_limited",
                    "highest_risk_open",
                    "open_not_proven",
                },
            )

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket231.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket231-summable-frame-critical-strip-gauss-crt.json"
        )
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket231.SCHEMA)
        machine = integrated["summable_frame_critical_strip_gauss_crt_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
