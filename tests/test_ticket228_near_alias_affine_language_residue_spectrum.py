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

import ticket228_near_alias_affine_language_residue_spectrum as ticket228  # noqa: E402


class Ticket228NearAliasAffineLanguageResidueSpectrumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket228.build_audit()
        cls.root = cls.audit["near_alias_affine_language_residue_spectrum_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket228.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_near_aliases_destroy_a_uniform_frame_bound(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["near_alias_rows"]
        self.assertGreaterEqual(len(rows), 10)
        self.assertTrue(
            all(
                current["normalized_dual_energy"]
                < previous["normalized_dual_energy"]
                for previous, current in zip(rows, rows[1:])
            )
        )
        self.assertLess(rows[-1]["normalized_dual_energy"], 1e-12)
        self.assertGreater(rows[-1]["frequency_tau_2pi_q_over_log2"], 1e7)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["finite_dilation_arbitrarily_large_near_aliases_proved"])
        self.assertTrue(aggregate["unweighted_uniform_full_line_frame_bound_refuted"])
        self.assertFalse(aggregate["explicit_bandlimited_diophantine_loss_bound_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_binary_affine_language_has_an_exact_noncycle_cone(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(section["block_affine_data"], [[81, 256, 221], [81, 256, 223]])
        self.assertEqual(section["suffix_affine_data"], [27, 64, 47])
        cone = section["global_ratio_cone"]
        self.assertEqual(Fraction(cone["lower"]), Fraction(887, 700))
        self.assertEqual(Fraction(cone["upper"]), Fraction(7123, 5600))
        self.assertGreater(Fraction(cone["lower"]), 1)
        self.assertLess(Fraction(cone["upper"]), 2)
        rows = section["level_rows"]
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[-1]["distinct_word_count_2_to_r"], 1024)
        for row in rows:
            self.assertEqual(
                row["distinct_word_count_2_to_r"], 2 ** row["block_count_r"]
            )
            self.assertEqual(row["verification_failures"], 0)
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["words_computationally_checked"], 2046)
        self.assertTrue(aggregate["binary_branching_primitive_noncycle_language_proved"])
        self.assertFalse(aggregate["all_primitive_cycle_words_excluded"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_unit_operator_spectrum_is_exact(self) -> None:
        for prime in ticket228.LOCAL_PRIMES:
            zero = ticket228.single_residue_operator_check(prime, 0)
            nonzero = ticket228.single_residue_operator_check(prime, 1)
            self.assertTrue(zero["gram_identity_verified"])
            self.assertEqual(zero["principal_singular_value"], prime - 1)
            self.assertEqual(zero["nonconstant_singular_value"], 0)
            self.assertEqual(zero["local_survival_fraction"], "1")
            self.assertTrue(nonzero["gram_identity_verified"])
            self.assertEqual(nonzero["principal_singular_value"], prime - 2)
            self.assertEqual(nonzero["nonconstant_singular_value"], 1)
            self.assertEqual(
                Fraction(nonzero["local_survival_fraction"]),
                Fraction(prime - 2, prime - 1),
            )
        section = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            section["exhaustive_residue_cases_checked"], sum(ticket228.LOCAL_PRIMES)
        )
        self.assertTrue(
            all(row["divisor_case_has_zero_exclusions"] for row in section["factor_cell_residue_rows"])
        )
        self.assertFalse(section["aggregate"]["strong_goldbach_conjecture_resolved"])

    def test_twin_cross_gram_and_mod_three_no_go_are_exact(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        rows = section["cross_operator_rows"]
        self.assertEqual([row["prime_l"] for row in rows], list(ticket228.LOCAL_PRIMES))
        self.assertTrue(all(row["cross_gram_shape_verified"] for row in rows))
        mod_three = rows[0]
        self.assertEqual(mod_three["prime_l"], 3)
        self.assertEqual(mod_three["joint_allowed_unit_pairs"], 0)
        self.assertTrue(mod_three["mod3_joint_mask_is_zero"])
        empirical_mod_three = [
            row for row in section["factor_cell_residue_rows"] if row["prime_l"] == 3
        ]
        self.assertEqual(len(empirical_mod_three), len(ticket228.HORIZONS))
        self.assertTrue(all(row["joint_local_survivors"] == 0 for row in empirical_mod_three))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["mod3_simultaneous_side_channel_route_refuted"])
        self.assertFalse(aggregate["uniform_shifted_bilinear_power_saving_proved"])
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
        ticket228.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket228-near-alias-affine-language-residue-spectrum.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket228.SCHEMA)
        machine = integrated["near_alias_affine_language_residue_spectrum_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
