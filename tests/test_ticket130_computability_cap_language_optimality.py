from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket130_computability_cap_language_optimality import (  # noqa: E402
    build_audit,
    collatz_cap_language_audit,
    goldbach_uniform_coefficient_optimality_audit,
    mechanical_cap_word,
    relative_increment_row,
    riemann_computable_weil_core_audit,
    riemann_core_support_certificate,
    twin_relative_increment_audit,
    valuation_word_residue,
)


class Ticket130ComputabilityCapLanguageOptimalityTests(unittest.TestCase):
    def test_riemann_core_has_effective_support_and_precision_ledgers(self) -> None:
        support = riemann_core_support_certificate(
            [
                (Fraction(-2, 3), Fraction(1, 4)),
                (Fraction(5, 7), Fraction(2, 5)),
            ]
        )
        self.assertGreater(support["prime_power_bound_B"], 1)
        self.assertEqual(support["autocorrelation_radius"], "853/420")
        audit = riemann_computable_weil_core_audit(8)
        widths = [
            Fraction(value)
            for value in audit["dovetail_precision_schedule"]["target_widths"]
        ]
        self.assertTrue(
            all(widths[index + 1] < widths[index] for index in range(len(widths) - 1))
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_cap_language_has_an_exact_survivor_at_every_prefix(self) -> None:
        word = mechanical_cap_word(256)
        self.assertTrue(set(word).issubset({1, 2}))
        residue, modulus = valuation_word_residue(word)
        self.assertGreater(residue, 0)
        self.assertLess(residue, modulus)
        audit = collatz_cap_language_audit(256)
        self.assertTrue(audit["machine_audit"]["every_prefix_hits_the_cap"])
        self.assertTrue(audit["machine_audit"]["rho_power_41_below_one"])
        self.assertTrue(
            audit["machine_audit"]["every_checkpoint_below_chernoff_bound"]
        )
        self.assertIn(
            "LeastCounterexampleValuationCapLanguageExtinction",
            audit["route_decision"]["discard"],
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_goldbach_k56_is_route_optimal_at_the_fixed_cutoff(self) -> None:
        audit = goldbach_uniform_coefficient_optimality_audit()
        certificate = audit["exact_partial_product_certificate"]
        self.assertEqual(certificate["rows"][-1]["last_prime"], 47)
        self.assertGreater(Fraction(certificate["exact_gap"]), 0)
        self.assertTrue(audit["machine_audit"]["first_crossing_is_47"])
        self.assertTrue(
            audit["machine_audit"][
                "k57_uniform_endpoint_fails_before_contamination"
            ]
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_twin_relative_increment_threshold_is_exact(self) -> None:
        endpoint = Fraction(23, 25)
        row = relative_increment_row(endpoint, Fraction(2, 23), Fraction(0))
        self.assertEqual(Fraction(row["Q_X"]), 1)
        self.assertEqual(Fraction(row["positive_defect"]), Fraction(2, 25))
        audit = twin_relative_increment_audit()
        self.assertTrue(audit["machine_audit"]["threshold_hits_one_exactly"])
        self.assertTrue(
            audit["machine_audit"]["endpoint_envelope_threshold_is_sharp"]
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_all_four_conjectures_remain_open(self) -> None:
        audit = build_audit(depth=64)
        machine = audit["machine_audit"]
        self.assertEqual(machine["problem_count"], 4)
        self.assertEqual(machine["exact_intermediate_theorem_count"], 5)
        self.assertEqual(machine["retired_impossible_target_count"], 1)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
