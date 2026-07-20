from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket133_quantifier_promotion_exact_reductions import (  # noqa: E402
    SCHEMA,
    build_audit,
    goldbach_power_two_sparse_spike_no_go,
    quadratic_value,
    valuation_affine_constant,
)


class Ticket133QuantifierPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(SCHEMA, "primeproject.ticket133-quantifier-promotion-exact-reductions.v1")
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertIn("None proves or refutes", self.audit["proof_boundary"])

    def test_riemann_gram_reduction_has_exact_negative_witness(self) -> None:
        section = self.audit["riemann"]
        sanity = section["finite_sanity_audit"]
        matrix = [[Fraction(1), Fraction(2)], [Fraction(2), Fraction(1)]]
        self.assertEqual(quadratic_value(matrix, (Fraction(1), Fraction(-1))), -2)
        self.assertEqual(sanity["explicit_indefinite_value"], "-2")
        self.assertEqual(sanity["failure_count"], 0)
        self.assertIn("finite Gram", section["proved_statement"])

    def test_collatz_affine_formula_and_exception_certificate(self) -> None:
        self.assertEqual(valuation_affine_constant([1, 2]), (3, 5))
        section = self.audit["collatz"]
        finite = section["finite_cylinder_audit"]
        self.assertEqual(finite["word_count"], 3905)
        self.assertEqual(finite["contracting_cylinder_count"], 3861)
        self.assertEqual(finite["noncontracting_cylinder_count"], 44)
        self.assertEqual(finite["unique_exception_start_count"], 1)
        self.assertTrue(finite["all_unique_exceptions_terminate"])
        self.assertEqual(section["machine_audit"]["total_failure_count"], 0)

    def test_goldbach_sparse_spike_has_exact_negative_margin(self) -> None:
        section = goldbach_power_two_sparse_spike_no_go()
        contract = section["exact_spike_contract"]
        margin = Fraction(contract["K56_margin"]["exact"])
        spike = Fraction(contract["power_of_two_spike"]["exact"])
        corrected = Fraction(contract["margin_after_spike"]["exact"])
        self.assertGreater(margin, 0)
        self.assertEqual(spike, -2 * margin)
        self.assertEqual(corrected, -margin)
        self.assertTrue(section["finite_mean_audit"]["all_sampled_means_strictly_decrease"])

    def test_twin_lifts_every_audited_admissible_class(self) -> None:
        section = self.audit["twin_prime"]
        rows = section["all_class_audit"]["rows"]
        self.assertEqual([row["sieve_level"] for row in rows], [5, 7, 11, 13])
        self.assertTrue(all(row["admissible_class_count"] == row["expected_class_count"] for row in rows))
        self.assertTrue(all(row["row_failure_count"] == 0 for row in rows))
        self.assertEqual(section["machine_audit"]["admissible_class_count"], 1638)
        self.assertTrue(section["machine_audit"]["all_classes_have_composite_lifts"])

    def test_each_track_names_a_stronger_next_theorem(self) -> None:
        expected = {
            "riemann": "IntervalCertifiedProjectedWeilGramFamily",
            "collatz": "PrefixFreeContractingCylinderCoverOfEveryNaturalCode",
            "goldbach": "HardStratumMaximalBinaryGoldbachResidualK56",
            "twin_prime": "UnboundedParitySensitiveTwinPairSeparation",
        }
        for key, theorem in expected.items():
            with self.subTest(problem=key):
                self.assertEqual(self.audit[key]["route_decision"]["next_theorem"], theorem)
                self.assertEqual(self.audit[key]["machine_audit"]["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
