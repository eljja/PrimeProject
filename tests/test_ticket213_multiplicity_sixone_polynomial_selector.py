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

import ticket213_multiplicity_sixone_polynomial_selector as ticket213


class Ticket213MultiplicitySixOnePolynomialSelectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket213.build_audit()

    def test_riemann_multiplicity_count_is_exact_rh_contract(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for row in section["configuration_rows"]:
            self.assertEqual(
                row["multiplicity_subtwo_certificate"],
                row["all_zeros_on_critical_line"],
            )
            self.assertEqual(
                row["sign_change_subtwo_certificate"],
                row["all_zeros_on_line_and_simple"],
            )
            self.assertEqual(row["multiplicity_aware_defect_N_minus_M"] % 2, 0)
        double = next(
            row
            for row in section["configuration_rows"]
            if row["configuration"] == "double_line_zero_is_RH_compatible"
        )
        self.assertTrue(double["multiplicity_subtwo_certificate"])
        self.assertFalse(double["sign_change_subtwo_certificate"])
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_six_one_stratum_is_exhausted(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(section["exact_length_cap_h"], 22)
        self.assertEqual(section["total_exact_words_enumerated"], 376_788)
        self.assertEqual(section["ordinary_divisibility_candidate_count"], 0)
        self.assertEqual(section["positive_odd_integer_fixed_point_count"], 0)
        self.assertEqual(
            [row["length_h"] for row in section["exact_enumeration_rows"]],
            list(range(7, 23)),
        )
        self.assertTrue(
            all(
                len(row["valuation_word_and_divisor_sha256"]) == 64
                for row in section["exact_enumeration_rows"]
            )
        )
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            7,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_six_one_word_generator_contract(self) -> None:
        words = list(ticket213.six_one_words(7, 12))
        self.assertEqual(len(words), 5)
        for word in words:
            self.assertEqual(word.count(1), 6)
            self.assertEqual(word[0], 1)
            self.assertGreaterEqual(word[-1], 2)
            self.assertLessEqual(sum(word), 12)

    def test_goldbach_polynomial_interpolation_and_no_go(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["finite_interpolation_rows"]:
            order = row["interpolation_order_M"]
            values = [Fraction(value) for value in row["values_at_A_0_through_M_plus_1"]]
            self.assertEqual(values[0], 1)
            self.assertTrue(all(value == 0 for value in values[1 : order + 1]))
            self.assertEqual(
                values[-1],
                Fraction((-1) ** order),
            )
        self.assertTrue(
            section["aggregate"]["fixed_degree_polynomial_majorant_route_refuted"]
        )
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_twin_nonnegative_selector_characterization(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["weight_audit_rows"]:
            self.assertEqual(
                row["support_only_at_gap_two_with_positive_weight"],
                row["basis_equivalence_observed"],
            )
        pure = section["weight_audit_rows"][0]
        self.assertTrue(pure["support_only_at_gap_two_with_positive_weight"])
        self.assertTrue(
            all(
                not row["support_only_at_gap_two_with_positive_weight"]
                for row in section["weight_audit_rows"][1:]
            )
        )
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket213.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket213-multiplicity-sixone-polynomial-selector.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket213.SCHEMA)
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
