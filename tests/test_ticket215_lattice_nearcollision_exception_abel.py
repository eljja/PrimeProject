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

import ticket215_lattice_nearcollision_exception_abel as ticket215


class Ticket215LatticeNearCollisionExceptionAbelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket215.build_audit()

    def test_riemann_even_lattice_certificate(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        rows = section["lattice_interval_rows"]
        self.assertEqual(rows[0]["even_nonnegative_defect_candidates"], [0])
        self.assertTrue(rows[0]["certifies_zero_defect"])
        self.assertEqual(rows[1]["even_nonnegative_defect_candidates"], [2])
        self.assertTrue(rows[1]["certifies_positive_defect"])
        self.assertTrue(
            all(row["interval_width"] == 0 for row in section["persistent_offline_pair_rows"])
        )
        self.assertFalse(section["aggregate"]["interval_width_alone_sufficient"])
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_single_mountain_divisibility_reduction(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(section["audited_k_max"], 4096)
        self.assertEqual(section["near_collision_candidate_count"], 0)
        for row in section["checkpoint_rows"]:
            k = row["valuation_one_count_k"]
            m = row["unique_possible_m"]
            delta = 2 ** (k + 2 * m) - 3 ** (k + m)
            previous = 2 ** (k + 2 * (m - 1)) - 3 ** (k + m - 1)
            self.assertGreater(delta, 0)
            self.assertLessEqual(previous, 0)
            self.assertGreater(delta, 3**k - 2**k)
            next_delta = 2 ** (k + 2 * (m + 1)) - 3 ** (k + m + 1)
            self.assertEqual(next_delta, 3 * delta + 2 ** (k + 2 * m))
        self.assertFalse(section["aggregate"]["all_k_near_collision_exclusion_proved"])
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_exception_floor_and_sharp_temperature(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["synthetic_exception_rows"]:
            value = Fraction(row["exact_selector_sum"])
            self.assertEqual(value.numerator // value.denominator, row["exception_count_Z"])
            self.assertTrue(row["floor_selector_equals_Z"])
        for row in section["sharp_temperature_rows"]:
            self.assertEqual(Fraction(row["all_positive_selector_sum"]), 1)
            self.assertTrue(row["subunit_test_fails_at_Bq_equals_one"])
        for row in section["dyadic_goldbach_rows"]:
            self.assertEqual(row["exception_count_Z"], 0)
            self.assertLess(Fraction(row["exact_tail_upper_bound"]), 1)
        self.assertFalse(section["aggregate"]["uniform_arithmetic_selector_bound_proved"])
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_twin_abel_boundary_and_finite_radius_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        counts = [row["twin_lower_endpoint_count_T_X"] for row in section["finite_prime_rows"]]
        self.assertEqual(counts, [8, 35, 205, 1224, 8169])
        self.assertTrue(
            all(row["weighted_sum_between_lower_bound_and_count"] for row in section["finite_prime_rows"])
        )
        epsilon = Fraction(section["epsilon"])
        for row in section["finite_radius_indistinguishability_rows"]:
            self.assertLess(Fraction(row["exact_infinite_tail_bound"]), epsilon)
            self.assertTrue(row["below_epsilon"])
        self.assertFalse(section["aggregate"]["finite_radius_samples_sufficient"])
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket215.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket215-lattice-nearcollision-exception-abel.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket215.SCHEMA)
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
