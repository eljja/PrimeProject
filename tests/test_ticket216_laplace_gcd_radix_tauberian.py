from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket216_laplace_gcd_radix_tauberian as ticket216


class Ticket216LaplaceGCDRadixTauberianTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket216.build_audit()

    def test_riemann_first_atom_threshold_and_delayed_atom_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for row in section["threshold_rows"]:
            if row["certifies_no_offline_pair_through_H"]:
                self.assertEqual(row["actual_synthetic_pair_count_through_H"], 0)
        for row in section["fixed_tolerance_no_go_rows"]:
            self.assertLess(
                Fraction(row["transform_of_one_delayed_pair"]),
                Fraction(row["epsilon"]),
            )
        self.assertFalse(
            section["aggregate"]["fixed_positive_tolerance_sufficient_for_RH"]
        )
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_cross_power_gcd_identity_audit(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(section["audited_k_max"], 4096)
        self.assertEqual(section["gcd_equality_candidate_count"], 0)
        for row in section["checkpoint_rows"]:
            k = row["valuation_one_count_k"]
            m = row["valuation_two_count_m"]
            delta = 2 ** (k + 2 * m) - 3 ** (k + m)
            common = gcd(3**k - 2**k, 4**m - 3**m)
            self.assertEqual(common == delta, row["delta_equals_cross_power_gcd"])
            self.assertEqual(
                delta,
                2**k * (4**m - 3**m) - 3**m * (3**k - 2**k),
            )
        self.assertFalse(section["aggregate"]["all_k_gcd_gap_proved"])
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_radix_selector_decodes_full_histogram(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["synthetic_rows"]:
            self.assertEqual(row["decoded_histogram"], row["histogram_h_a"])
            self.assertEqual(row["exception_digit_h_0"], row["counts"].count(0))
        for row in section["dyadic_goldbach_rows"]:
            self.assertTrue(row["full_histogram_recovered"])
            self.assertEqual(row["exception_digit_h_0"], 0)
        differences = [
            Fraction(row["exact_selector_difference"])
            for row in section["finite_precision_no_go_rows"]
        ]
        self.assertTrue(all(left > right for left, right in zip(differences, differences[1:])))
        self.assertFalse(section["aggregate"]["uniform_arithmetic_selector_bound_proved"])
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_twin_quantitative_abel_count_transfer(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["finite_prime_rows"]:
            self.assertTrue(row["lower_factor_inequality_holds"])
            self.assertLessEqual(
                row["transferred_integer_lower_bound_for_T_Y"],
                row["actual_bounded_twin_count_T_Y"],
            )
        for row in section["tail_scale_rows"]:
            self.assertLess(
                Fraction(row["adaptive_tail_over_X_log2X_scale"]), 1
            )
        self.assertFalse(
            section["aggregate"]["fixed_dilation_sufficient_at_Hardy_Littlewood_scale"]
        )
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket216.write_outputs(self.audit)
        integrated_path = (
            ROOT / "data/open-problem/ticket216-laplace-gcd-radix-tauberian.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket216.SCHEMA)
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
