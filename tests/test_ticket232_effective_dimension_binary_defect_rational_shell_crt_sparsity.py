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

import ticket232_effective_dimension_binary_defect_rational_shell_crt_sparsity as ticket232  # noqa: E402


class Ticket232EffectiveDimensionBinaryDefectRationalShellCRTSparsityTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket232.build_audit()
        cls.root = cls.audit[
            "effective_dimension_binary_defect_rational_shell_crt_sparsity_audit"
        ]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket232.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertIn("resolves none", self.audit["claim_boundary"])
        self.assertEqual(
            self.root["machine_audit"],
            {
                "exact_partial_theorem_count": 4,
                "refuted_or_corrected_route_count": 4,
                "next_single_lemma_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        self.assertEqual(
            {row["problem_id"] for row in self.audit["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )

    def test_riemann_logarithmic_effective_dimension_barrier(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        for row in section["adaptive_collision_rows"]:
            self.assertTrue(row["certificate_verified"])
            self.assertLessEqual(
                row["observed_normalized_energy"],
                row["normalized_head_bound_4pi2_over_Q2"] + 1e-12,
            )
            self.assertLessEqual(
                row["witness_frequency_n"], row["frequency_horizon_T"]
            )
        corollary = section["explicit_half_floor_corollary"]
        self.assertEqual(Fraction(corollary["normalized_floor_c"]), Fraction(1, 2))
        self.assertEqual(Fraction(corollary["maximum_tail_ratio"]), Fraction(1, 16))
        self.assertEqual(corollary["partition_Q"], 13)
        self.assertTrue(corollary["constant_check_verified"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["logarithmic_effective_dimension_necessary"])
        self.assertFalse(aggregate["weil_tail_dominance_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_one_two_three_defect_formulas(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        for height in range(3, 25):
            one = (1,) + (2,) * (height - 1)
            denominator = ticket232.collatz_denominator(one)
            if denominator > 0:
                numerator = ticket232.collatz_numerator(one)
                self.assertEqual(numerator - denominator, 2 * 3 ** (height - 1))
                self.assertNotEqual(numerator % denominator, 0)
        for height in range(5, 18):
            for gap in range(1, height // 2 + 1):
                word = (1,) + (2,) * (gap - 1) + (1,) + (2,) * (height - gap - 1)
                denominator = ticket232.collatz_denominator(word)
                numerator = ticket232.collatz_numerator(word)
                remainder = 2 * 3**gap + 4**gap
                self.assertEqual(
                    numerator - denominator,
                    3 ** (height - gap - 1) * remainder,
                )
                self.assertNotEqual(numerator % denominator, 0)
        self.assertTrue(
            all(row["certificate_verified"] for row in section["height_rows"])
        )
        self.assertTrue(
            all(
                row["all_factorizations_and_nondivisibility_verified"]
                for row in section["three_defect_gap_certificate_rows"]
            )
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["three_valuation_one_binary_cycles_excluded"])
        self.assertTrue(aggregate["binary_nontrivial_cycle_needs_at_least_four_ones"])
        self.assertFalse(aggregate["aperiodic_descent_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_actual_prime_shell_identity_and_no_go(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        rows = section["actual_prime_indicator_shell_rows"]
        self.assertEqual(len(rows), 40)
        self.assertTrue(
            all(
                row["shell_equals_base_plus_correction"]
                and row["integer_identity_verified"]
                for row in rows
            )
        )
        notable = section["notable_sign_reversal"]
        self.assertEqual(notable["residue_masses"], [5, 7, 7, 5])
        self.assertEqual(notable["unit_prime_mass_W"], 24)
        self.assertEqual(notable["exact_rational_shell_T"], 19)
        self.assertEqual(Fraction(notable["uniform_singular_shell"]), -36)
        self.assertEqual(Fraction(notable["autocorrelation_correction"]), 55)
        counter = section["growing_modulus_relative_equidistribution_counterfamily"]
        self.assertTrue(all(row["sign_reversed"] for row in counter))
        self.assertLess(counter[-1]["maximum_classwise_relative_discrepancy"], 0.1)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["prime_weighted_rational_shell_identity_proved"])
        self.assertFalse(aggregate["full_minor_arc_aggregate_bound_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_chi_square_sparsity_and_modewise_no_go(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        rows = section["twin_sieve_sparsity_rows"]
        self.assertEqual([row["active_prime_count_m"] for row in rows], [23, 63, 166])
        lower = [Fraction(row["minimum_full_interaction_energy"]) for row in rows]
        self.assertTrue(all(right > left for left, right in zip(lower, lower[1:])))
        self.assertAlmostEqual(float(lower[0]), 266.0097241407741, places=10)
        tilt = section["coefficientwise_decay_counterfamily_rows"]
        energies = [Fraction(row["full_interaction_energy"]) for row in tilt]
        self.assertTrue(
            all(right > left for left, right in zip(energies, energies[1:]))
        )
        self.assertLess(
            Fraction(tilt[-1]["maximum_nonconstant_coefficient"]), Fraction(1, 10)
        )
        self.assertLess(float(energies[-1]), math.e - 1)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["full_interaction_chi_square_identity_proved"])
        self.assertTrue(aggregate["twin_sieve_full_unweighted_energy_saving_refuted"])
        self.assertFalse(aggregate["positive_twin_main_term_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_each_track_has_one_successor_and_proof_dag(self) -> None:
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

    def test_outputs_are_reproducible(self) -> None:
        ticket232.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket232-effective-dimension-binary-defect-rational-shell-crt-sparsity.json"
        )
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket232.SCHEMA)
        machine = integrated[
            "effective_dimension_binary_defect_rational_shell_crt_sparsity_audit"
        ]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
