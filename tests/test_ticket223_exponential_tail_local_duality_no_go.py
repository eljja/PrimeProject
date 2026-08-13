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

import ticket223_exponential_tail_local_duality_no_go as ticket223  # noqa: E402


class Ticket223ExponentialTailLocalDualityNoGoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket223.build_audit()
        cls.root = cls.audit["exponential_tail_local_duality_no_go_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket223.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_exponential_tail_contract(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["exponential_tail_dyadic_injectivity_proved"])
        self.assertTrue(aggregate["uniform_cofinal_truncation_bound_proved"])
        self.assertFalse(aggregate["actual_zeta_defect_measure_constructed"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])
        rows = section["cofinal_tail_rows"]
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["tv_bound_verified"] for row in rows))
        self.assertTrue(all(row["exponential_bound_verified"] for row in rows))

    def test_collatz_fixed_modulus_false_positive_formula(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        rows = section["witness_rows"]
        self.assertEqual(len(rows), sum(1 for m in range(5, 200) if math.gcd(m, 6) == 1))
        for row in rows:
            self.assertTrue(row["M_divides_D"])
            self.assertTrue(row["M_divides_B"])
            self.assertTrue(row["positive_false_positive"])
            self.assertTrue(row["primitive_nontrivial_word"])
            self.assertFalse(row["actual_cycle_divisibility"])
            self.assertEqual(
                row["D_minus_B_decimal"], row["expected_D_minus_B_decimal"]
            )
        extra = ticket223.fixed_modulus_witness(1001)
        self.assertTrue(extra["M_divides_D"] and extra["M_divides_B"])
        self.assertTrue(extra["positive_false_positive"])

    def test_goldbach_uniform_local_floor(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        exact = section["exact_wheel_audit"]
        self.assertEqual(exact["wheel_W"], 3 * 5 * 7 * 11)
        self.assertEqual(exact["minimum_observed_ratio"], exact["uniform_floor"])
        self.assertEqual(
            exact["floor_equality_residue_count"],
            exact["expected_equality_residue_count"],
        )
        floors = [
            Fraction(row["wheel_normalized_floor"])
            for row in section["wheel_prefix_rows"]
        ]
        self.assertTrue(all(left > right for left, right in zip(floors, floors[1:])))
        self.assertTrue(all(value > 0 for value in floors))
        self.assertFalse(section["aggregate"]["prime_weighted_global_remainder_controlled"])

    def test_twin_fixed_wheel_composite_countermodels(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        rows = section["wheel_prefix_countermodels"]
        self.assertEqual(len(rows), 13)
        self.assertTrue(all(row["countermodel_verified"] for row in rows))
        self.assertTrue(
            section["aggregate"]["fixed_wheel_composite_pair_countermodel_proved"]
        )
        self.assertFalse(
            section["aggregate"]["scale_growing_type_ii_dominance_proved"]
        )
        for row in rows:
            n = int(row["composite_pair_n"])
            self.assertEqual(n % row["external_left_factor_r"], 0)
            self.assertEqual((n + 2) % row["external_right_factor_s"], 0)

    def test_goldbach_twin_local_factor_identity(self) -> None:
        goldbach_rows = self.root["goldbach"]["reproducible_computation"][
            "wheel_prefix_rows"
        ]
        twin_rows = self.root["twin_prime"]["reproducible_computation"][
            "wheel_prefix_countermodels"
        ]
        self.assertEqual(len(goldbach_rows), len(twin_rows))
        for goldbach, twin in zip(goldbach_rows, twin_rows):
            self.assertEqual(goldbach["largest_prime"], twin["largest_wheel_prime"])
            self.assertEqual(
                goldbach["wheel_normalized_floor"],
                twin["normalized_survivor_density"],
            )

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket223.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket223-exponential-tail-local-duality-no-go.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket223.SCHEMA)
        machine = integrated["exponential_tail_local_duality_no_go_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
