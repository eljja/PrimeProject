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

import ticket230_quantitative_recurrence_necklace_fourier_centering as ticket230  # noqa: E402


class Ticket230QuantitativeRecurrenceNecklaceFourierCenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket230.build_audit()
        cls.root = cls.audit[
            "quantitative_recurrence_necklace_fourier_centering_audit"
        ]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket230.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_dirichlet_rate_certificates(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["pigeonhole_rows"]
        self.assertEqual(len(rows), 12)
        self.assertEqual({row["dimension_m"] for row in rows}, {2, 3})
        for row in rows:
            self.assertTrue(row["phase_bound_verified"])
            self.assertTrue(row["energy_bound_verified"])
            self.assertTrue(row["frequency_bound_verified"])
            self.assertTrue(row["sequence_rate_verified"])
            self.assertLessEqual(
                row["witness_frequency_n"], row["maximum_index_Q_to_m"]
            )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["quantitative_finite_dilation_recurrence_proved"])
        self.assertTrue(
            aggregate["slower_than_T_minus_2_over_m_global_floor_refuted"]
        )
        self.assertFalse(aggregate["infinite_or_adaptive_weil_frame_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_rotation_identity_and_necklace_reduction(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        for row in section["sample_rotation_rows"]:
            self.assertTrue(row["all_rotation_identities_verified"])
            word = tuple(row["word"])
            rotated = ticket230.rotate_left(word)
            denominator = ticket230.collatz_denominator(word)
            self.assertEqual(
                2 ** word[0] * ticket230.collatz_numerator(rotated),
                3 * ticket230.collatz_numerator(word) + denominator,
            )
            self.assertEqual(
                math.gcd(denominator, ticket230.collatz_numerator(word)),
                math.gcd(denominator, ticket230.collatz_numerator(rotated)),
            )
        for row in section["height_rows"]:
            self.assertEqual(
                row["primitive_positive_denominator_word_count"],
                row["height_h"] * row["canonical_necklace_count"],
            )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["cycle_divisibility_necklace_invariance_proved"])
        self.assertFalse(aggregate["all_primitive_necklaces_excluded"])
        self.assertFalse(aggregate["aperiodic_descent_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_modewise_decay_counterexample(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        rows = section["counterexample_rows"]
        self.assertGreaterEqual(len(rows), 7)
        previous_mode_ratio = Fraction(1)
        for row in rows:
            mode_ratio = Fraction(row["maximum_mode_to_mass_ratio"])
            error_ratio = Fraction(row["error_to_principal_ratio"])
            self.assertLess(mode_ratio, previous_mode_ratio)
            self.assertGreater(error_ratio, 0)
            self.assertEqual(
                row["target_aligned_nonprincipal_error"],
                row["spike_scale_m"] ** 2 - 1,
            )
            self.assertTrue(row["sampled_fourier_formula_verified"])
            previous_mode_ratio = mode_ratio
        self.assertGreater(Fraction(rows[-1]["error_to_principal_ratio"]), Fraction(9, 10))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["modewise_relative_decay_counterexample_proved"])
        self.assertTrue(
            aggregate["modewise_o_of_mass_implies_pointwise_positivity_refuted"]
        )
        self.assertFalse(aggregate["prime_specific_signed_minor_arc_bound_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_local_mean_requires_one_third_centering(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        mod_five = section["mod5_exact_row"]
        self.assertEqual(mod_five["allowed_start_residues"], [1, 2, 4])
        self.assertEqual(mod_five["raw_quadratic_character_sum"], 1)
        self.assertEqual(Fraction(mod_five["raw_local_mean"]), Fraction(1, 3))
        self.assertEqual(Fraction(mod_five["centered_character_sum"]), 0)
        for row in section["local_character_rows"]:
            self.assertTrue(row["identity_verified"])
            self.assertEqual(
                row["raw_quadratic_character_sum"],
                row["predicted_sum_minus_chi_of_minus_h"],
            )
        for row in section["bounded_twin_sample_rows"]:
            self.assertTrue(row["all_starts_in_admissible_residues"])
            self.assertTrue(row["finite_sample_only_not_asymptotic_proof"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["uncentered_zero_cancellation_target_refuted"])
        self.assertFalse(aggregate["centered_prime_weighted_typeII_saving_proved"])
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
        ticket230.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket230-quantitative-recurrence-necklace-fourier-centering.json"
        )
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket230.SCHEMA)
        machine = integrated[
            "quantitative_recurrence_necklace_fourier_centering_audit"
        ]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
