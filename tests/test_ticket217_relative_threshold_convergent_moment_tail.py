from __future__ import annotations

import json
import sys
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket217_relative_threshold_convergent_moment_tail as ticket217


class Ticket217RelativeThresholdConvergentMomentTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket217.build_audit()

    def test_riemann_normalized_certificate_and_multiradius_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for row in section["normalized_certificate_rows"]:
            self.assertLessEqual(
                row["actual_synthetic_pair_count_C_H"],
                row["best_integer_upper_for_C_H"],
            )
        for row in section["finite_absolute_precision_invisibility_rows"]:
            self.assertTrue(row["hidden_at_every_radius"])
            height = row["first_simultaneously_hidden_height"]
            for radius, tolerance in zip(row["radii"], row["absolute_tolerances"]):
                self.assertLess(Fraction(radius) ** height, Fraction(tolerance))
        self.assertFalse(
            section["aggregate"]["finite_absolute_precision_family_sufficient_for_RH"]
        )
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_convergent_compression_and_exact_barrier(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        rows = section["audited_upper_convergent_rows"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[-1]["reduced_upper_convergent_k"], 4_474_633)
        self.assertTrue(all(row["delta_at_least_three_pow_k"] for row in rows))
        self.assertTrue(all(row["all_positive_multiples_excluded"] for row in rows))
        self.assertEqual(
            section["next_unaudited_upper_convergent"],
            {"m": 100_571_885, "k": 71_356_888},
        )
        self.assertEqual(section["single_mountain_k_exclusive_upper_bound"], 71_356_888)
        self.assertFalse(section["aggregate"]["all_single_mountain_cycles_excluded"])
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_second_moment_threshold_is_sharp_and_not_promoted(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        synthetic = section["synthetic_sharpness_rows"]
        self.assertTrue(synthetic[0]["full_support_certified"])
        self.assertEqual(synthetic[1]["support_margin_S2_minus_Bminus1Q"], 0)
        self.assertFalse(synthetic[1]["full_support_certified"])
        self.assertEqual(synthetic[2]["support_margin_S2_minus_Bminus1Q"], 0)
        rows = section["dyadic_goldbach_rows"]
        self.assertTrue(all(row["minimum_exact_representation_count"] > 0 for row in rows))
        self.assertTrue(all(not row["raw_second_moment_certificate_passed"] for row in rows))
        self.assertTrue(all(not row["hardy_littlewood_shape_diagnostic_passed"] for row in rows))
        self.assertEqual(section["aggregate"]["raw_dyadic_blocks_certified"], 0)
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_twin_critical_tail_phase_transition(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        self.assertIn("0<=c_X=o(X)", section["theorem"])
        rows = section["critical_limit_rows"]
        self.assertEqual(len(rows), 12)
        for offset in ("-2", "0", "2"):
            offset_rows = [row for row in rows if row["offset_a"] == offset]
            errors = [Decimal(row["absolute_limit_error"]) for row in offset_rows]
            self.assertTrue(all(left > right for left, right in zip(errors, errors[1:])))
            self.assertLess(errors[-1], Decimal("0.000001"))
        zero_offset = [row for row in rows if row["offset_a"] == "0"][-1]
        self.assertLess(
            abs(Decimal(zero_offset["tail_over_X_log2X"]) - Decimal("0.5")),
            Decimal("0.000001"),
        )
        self.assertFalse(
            section["aggregate"]["actual_twin_Abel_surplus_above_tail_proved"]
        )
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket217.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket217-relative-threshold-convergent-moment-tail.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket217.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        for attempt in integrated["attempts"]:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertTrue(attempt["declared_proposition"])
            self.assertTrue(attempt["discarded_route"])
            self.assertTrue(attempt["remaining_gap"])
            self.assertTrue(attempt["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
