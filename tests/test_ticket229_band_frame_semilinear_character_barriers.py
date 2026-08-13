from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket229_band_frame_semilinear_character_barriers as ticket229  # noqa: E402


class Ticket229BandFrameSemilinearCharacterBarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket229.build_audit()
        cls.root = cls.audit["band_frame_semilinear_character_barriers_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket229.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_explicit_band_floor_and_tail_mismatch(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["band_rows"]
        self.assertGreaterEqual(len(rows), 8)
        self.assertTrue(
            all(
                current["log10_certified_frame_lower_bound"]
                < previous["log10_certified_frame_lower_bound"]
                for previous, current in zip(rows, rows[1:])
            )
        )
        self.assertTrue(rows[-1]["polynomial_error_eventually_exceeds_bound"])
        for row in section["phase_inequality_rows"]:
            self.assertTrue(row["energy_above_torus_lower"])
            self.assertTrue(row["torus_lower_above_form_lower"])
            self.assertGreaterEqual(row["nearest_m_for_log3_phase"], 1)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["explicit_finite_band_dual_dilation_lower_bound_proved"])
        self.assertTrue(aggregate["polynomial_tail_matching_from_this_bound_refuted"])
        self.assertFalse(aggregate["actual_weil_core_operator_bound_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_finite_equal_slope_union_is_not_cofinal(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(section["eventual_outside_start_height"], 4)
        intersections = section["finite_sample_intersection_rows"]
        self.assertEqual(len(intersections), 1)
        self.assertEqual(intersections[0]["height_h"], 3)
        tail = [
            row
            for row in section["witness_family_rows"]
            if row["height_h"] >= section["eventual_outside_start_height"]
        ]
        self.assertTrue(tail)
        self.assertTrue(all(not row["sample_language_memberships"] for row in tail))
        self.assertTrue(all(row["D_positive"] for row in tail))
        self.assertTrue(all(row["primitive_unique_exception_verified"] for row in tail))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["finite_equal_slope_union_cofinal_coverage_refuted"])
        self.assertFalse(aggregate["exact_cycle_divisibility_for_all_outside_words_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_complete_target_period_is_rank_one(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        for row in section["complete_period_rows"]:
            self.assertTrue(row["complete_sum_equals_l_minus_1_times_J"])
            self.assertTrue(row["complete_period_annihilates_nonconstant_space"])
            self.assertTrue(row["individual_nonzero_target_isometry_verified"])
            self.assertEqual(row["each_nonzero_target_nonconstant_norm"], 1)
        for row in section["window_rows"]:
            bound = Fraction(row["certified_nonconstant_average_norm_upper"])
            self.assertLess(bound, Fraction(row["prime_l"], row["window_length_H"]))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["complete_target_period_character_cancellation_proved"])
        self.assertTrue(aggregate["target_averaging_implies_pointwise_goldbach_refuted"])
        self.assertFalse(aggregate["prime_weighted_single_target_cancellation_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_character_parity_and_mod5_obstruction(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        rows = section["local_character_rows"]
        mod_five = next(row for row in rows if row["prime_l"] == 5)
        self.assertTrue(mod_five["mod5_quadratic_mode_has_no_contraction"])
        self.assertEqual(Fraction(mod_five["worst_normalized_nonconstant_ratio"]), 1)
        for row in rows:
            if row["prime_l"] == 3:
                continue
            for mode in row["mode_rows"]:
                expected = 0 if mode["parity"] == "odd" else 2
                self.assertEqual(mode["nonconstant_singular_value"], expected)
        tensor_with_five = [
            row
            for row in section["tensor_obstruction_rows"]
            if 5 in row["squarefree_local_primes"]
        ]
        self.assertTrue(
            all(row["mod5_supported_mode_blocks_uniform_contraction"] for row in tensor_with_five)
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["odd_shift_two_characters_annihilated_proved"])
        self.assertTrue(aggregate["mod5_quadratic_normalized_no_contraction_proved"])
        self.assertFalse(aggregate["prime_weighted_mod5_quadratic_cancellation_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_each_track_has_one_open_successor_and_a_closed_dag_node(self) -> None:
        for problem in ("riemann", "collatz", "goldbach", "twin_prime"):
            track = self.root[problem]
            self.assertTrue(track["route_decision"]["next_single_lemma"])
            statuses = {node["status"] for node in track["proof_dag"]["nodes"]}
            self.assertIn("closed", statuses)
            self.assertIn("refuted_or_limited", statuses)
            self.assertIn("highest_risk_open", statuses)
            self.assertIn("open_not_proven", statuses)

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket229.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket229-band-frame-semilinear-character-barriers.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket229.SCHEMA)
        machine = integrated["band_frame_semilinear_character_barriers_audit"]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
