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

import ticket214_cofinal_sevenone_exponential_cardinal as ticket214


class Ticket214CofinalSevenOneExponentialCardinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket214.build_audit()

    def test_riemann_cofinal_equivalence_and_density_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        rows = section["density_one_countermodel_rows"]
        self.assertTrue(all(row["defect_N_minus_M"] == 2 for row in rows))
        self.assertTrue(all(not row["rectangle_RH"] for row in rows))
        relative = [Fraction(row["relative_defect"]) for row in rows]
        self.assertTrue(all(left > right for left, right in zip(relative, relative[1:])))
        seen = False
        for row in section["monotone_defect_rows"]:
            seen = seen or row["defect"] > 0
            if seen:
                self.assertFalse(row["exact_multiplicity_equality"])
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_seven_one_stratum_is_exhausted(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(section["exact_length_cap_h"], 26)
        self.assertEqual(section["total_exact_words_enumerated"], 4_349_349)
        self.assertEqual(section["ordinary_divisibility_candidate_count"], 0)
        self.assertEqual(section["positive_odd_integer_fixed_point_count"], 0)
        self.assertEqual(
            [row["length_h"] for row in section["exact_enumeration_rows"]],
            list(range(8, 27)),
        )
        self.assertTrue(
            all(
                row["candidate_word_count"]
                >= row["h_equals_2k_binomial_lower_bound"]
                for row in section["fixed_stratum_complexity_rows"]
            )
        )
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            8,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_seven_one_word_generator_contract(self) -> None:
        words = list(ticket214.k_one_words(8, 7, 13))
        self.assertEqual(len(words), 5)
        for word in words:
            self.assertEqual(word.count(1), 7)
            self.assertEqual(word[0], 1)
            self.assertGreaterEqual(word[-1], 2)
            self.assertLessEqual(sum(word), 13)

    def test_goldbach_exponential_selector_and_occupancy(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["synthetic_selector_rows"]:
            selector = Fraction(row["exact_selector_sum"])
            self.assertEqual(selector < 1, not row["has_zero"])
            self.assertTrue(row["selector_subunit_iff_all_positive_verified"])
        for row in section["dyadic_goldbach_rows"]:
            self.assertEqual(row["observed_exception_count"], 0)
            self.assertGreater(row["maximum_zeros_consistent_with_only_B_S_U"], 0)
            self.assertLess(
                Fraction(row["positive_block_selector_upper_bound_B_over_2_pow_k"]),
                1,
            )
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_twin_cardinal_and_lagrange_selectors(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["finite_lagrange_rows"]:
            values = [Fraction(value) for value in row["selector_values"]]
            order = row["gap_cutoff_2M"] // 2
            self.assertEqual(values[0], 1)
            self.assertTrue(all(value == 0 for value in values[1:order]))
            self.assertTrue(row["finite_gap_exact_selector_verified"])
        for row in section["prime_gap_audit_rows"]:
            self.assertTrue(row["exceptional_gap_one_omitted"])
            self.assertEqual(
                row["cardinal_sine_symbolic_functional"],
                row["consecutive_gap_two_count"],
            )
        self.assertFalse(section["aggregate"]["unbounded_gap_two_count_proved"])
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket214.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket214-cofinal-sevenone-exponential-cardinal.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket214.SCHEMA)
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
