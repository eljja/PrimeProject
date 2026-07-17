from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket131_proof_viability_target_correction import (  # noqa: E402
    build_audit,
    collatz_stabilization_and_cap_correction,
    goldbach_arithmetic_stratification,
    riemann_finite_positivity_no_go,
    twin_relative_increment_reparameterization,
    valuation_cylinder_replay_audit,
    valuation_word_cylinder,
)


class Ticket131ProofViabilityTargetCorrectionTests(unittest.TestCase):
    def test_riemann_finite_positivity_has_an_exact_blind_spot(self) -> None:
        audit = riemann_finite_positivity_no_go(ambient_dimension=7, observed_dimension=4)
        countermodel = audit["exact_countermodel"]
        self.assertTrue(
            all(row["values_equal"] for row in countermodel["observed_rows"])
        )
        self.assertEqual(countermodel["negative_witness_value"], -1)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_exact_cylinders_are_nested(self) -> None:
        first_residue, first_modulus = valuation_word_cylinder([2])
        second_residue, second_modulus = valuation_word_cylinder([2, 1])
        self.assertEqual((first_residue, first_modulus), (1, 8))
        self.assertEqual((second_residue, second_modulus), (9, 16))
        self.assertEqual(second_residue % first_modulus, first_residue)

    def test_collatz_scope_correction_and_stabilization_contract(self) -> None:
        audit = collatz_stabilization_and_cap_correction(128)
        scope = audit["strict_cap_scope_correction"]
        self.assertEqual(scope["ticket129_strict_cap_horizon_2H"], 2**29)
        self.assertEqual(scope["first_exact_demonstration_scale_3H"], 3 * 2**28)
        self.assertTrue(audit["machine_audit"]["all_exact_cylinders_nested"])
        self.assertEqual(audit["machine_audit"]["historical_target_correction_count"], 1)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_small_exact_cylinders_replay(self) -> None:
        replay = valuation_cylinder_replay_audit(4, 4)
        self.assertEqual(replay["word_count"], 340)
        self.assertEqual(replay["failure_count"], 0)

    def test_goldbach_k57_stratum_has_exact_103_boundary(self) -> None:
        audit = goldbach_arithmetic_stratification()
        boundary = audit["k57_boundary"]
        self.assertEqual(boundary["largest_certified_prime"], 103)
        self.assertGreater(Fraction(boundary["margin_at_p_103"]["exact"]), 0)
        self.assertLess(Fraction(boundary["margin_at_p_107"]["exact"]), 0)
        self.assertGreater(
            audit["stratified_rows"][0]["covered_even_integer_density"], 0.76
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_twin_relative_target_is_an_exact_ratio_identity(self) -> None:
        audit = twin_relative_increment_reparameterization()
        exact = audit["exact_equivalence"]
        self.assertEqual(Fraction(exact["equivalent_multiplier"]), Fraction(25, 23))
        self.assertEqual(Fraction(exact["additive_headroom"]), Fraction(2, 25))
        self.assertEqual(Fraction(exact["sharp_ceiling"]), 1)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_all_four_conjectures_remain_open(self) -> None:
        audit = build_audit(depth=128)
        machine = audit["machine_audit"]
        self.assertEqual(machine["problem_count"], 4)
        self.assertEqual(machine["exact_intermediate_theorem_count"], 5)
        self.assertEqual(machine["historical_target_correction_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
