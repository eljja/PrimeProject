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

import ticket226_signal_transfer_same_order_obstructions as ticket226  # noqa: E402


class Ticket226SignalTransferSameOrderObstructionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket226.build_audit()
        cls.root = cls.audit["signal_transfer_same_order_obstructions_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket226.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_balanced_chebyshev_kernel_identity(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(len(section["actual_prime_kernel_rows"]), 11)
        for row in section["actual_prime_kernel_rows"]:
            self.assertTrue(row["identity_verified"])
            self.assertTrue(row["negative_sign_certified"])
            self.assertLess(row["identity_absolute_error"], 1e-12)
        for row in section["balanced_kernel_mass_rows"]:
            self.assertTrue(row["balanced_mass_verified"])
            self.assertAlmostEqual(row["negative_kernel_mass"], -0.25)
            self.assertAlmostEqual(row["positive_kernel_mass"], 0.25)
            self.assertAlmostEqual(row["total_kernel_mass"], 0.0)
        witnesses = section["opposite_sign_atomic_witnesses"]
        self.assertLess(witnesses[0]["kernel_value_at_a_1"], 0.0)
        self.assertGreater(witnesses[1]["kernel_value_at_a_1"], 0.0)
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_chebyshev_kernel_mass_directly(self) -> None:
        crossing = math.log(2.0)
        antiderivative = lambda value: -math.exp(-value) + math.exp(-2 * value)
        negative = antiderivative(crossing) - antiderivative(0.0)
        positive = -antiderivative(crossing)
        self.assertAlmostEqual(negative, -0.25)
        self.assertAlmostEqual(positive, 0.25)

    def test_collatz_infinite_counterfamily_formulas(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        rows = section["infinite_family_audit_rows"]
        self.assertEqual([row["repetition_r"] for row in rows], [1, 2, 3, 5, 10, 20, 40])
        for row in rows:
            self.assertTrue(row["primitive_word_verified"])
            self.assertTrue(row["all_cyclic_intercepts_above_D"])
            self.assertFalse(row["D_divides_B"])
            self.assertTrue(row["noncycle_verified"])
            self.assertGreater(row["B_over_D"], 1.0)
            self.assertLess(row["B_over_D"], 4.0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["infinite_primitive_family_proved"])
        self.assertTrue(aggregate["universal_minimum_intercept_descent_refuted"])
        self.assertFalse(aggregate["all_nontrivial_cycles_excluded"])
        self.assertFalse(aggregate["aperiodic_descent_proved"])

    def test_collatz_family_directly(self) -> None:
        for repetition in range(1, 13):
            word = (1, 1, 3) * repetition + (2,)
            denominator = 4 * 32**repetition - 3 * 27**repetition
            formula = (62 * 32**repetition - 57 * 27**repetition) // 5
            intercepts = [
                ticket226.collatz_intercept(local)
                for local in ticket226.rotations(word)
            ]
            self.assertTrue(ticket226.is_primitive_word(word))
            self.assertEqual(intercepts[0], formula)
            self.assertEqual(min(intercepts), formula)
            self.assertGreater(formula, denominator)
            self.assertNotEqual(formula % denominator, 0)

    def test_rough_semiprime_exact_count_and_same_order_contract(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        rows = section["rough_semiprime_density_rows"]
        self.assertEqual([row["horizon_X"] for row in rows], [10_000, 100_000, 1_000_000])
        for row in rows:
            self.assertTrue(row["exact_count_identity_verified"])
            self.assertEqual(
                row["rough_semiprime_count_S_X"],
                row["exact_prime_pair_formula_count"],
            )
        self.assertLess(rows[0]["S_over_pi"], rows[-1]["S_over_pi"])
        self.assertEqual(
            section["aggregate"]["rough_semiprime_to_prime_ratio_limit"],
            "log(2)",
        )

    def test_goldbach_domination_route_has_finite_counterexamples(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        rows = section["goldbach_convolution_rows"]
        for row in rows:
            self.assertTrue(row["exact_decomposition_verified"])
            self.assertEqual(
                row["filtered_total_QQ"],
                row["prime_prime_PP"] + row["rough_semiprime_contamination_E"],
            )
            self.assertFalse(row["contamination_below_PP"])
            self.assertGreater(row["prime_prime_PP"], 0)
        self.assertFalse(section["aggregate"]["strong_goldbach_conjecture_resolved"])

    def test_twin_marginal_limit_is_not_pair_asymptotic(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        rows = section["gap_two_pair_rows"]
        for row in rows:
            self.assertTrue(row["exact_pair_decomposition_verified"])
            self.assertEqual(
                row["filtered_gap_two_pairs_R"],
                row["prime_prime_PP"]
                + row["rough_semiprime_pair_contamination_E"],
            )
        self.assertTrue(rows[0]["contamination_below_PP"])
        self.assertFalse(rows[1]["contamination_below_PP"])
        self.assertFalse(rows[2]["contamination_below_PP"])
        aggregate = section["aggregate"]
        self.assertFalse(aggregate["shifted_type_ii_power_saving_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket226.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket226-signal-transfer-same-order-obstructions.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket226.SCHEMA)
        machine = integrated["signal_transfer_same_order_obstructions_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
