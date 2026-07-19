from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket132_admissibility_nullset_hard_stratum_local_parity import (  # noqa: E402
    accelerated_valuations,
    build_audit,
    collatz_natural_code_topology,
    crt,
    goldbach_power_of_two_hard_stratum,
    riemann_constraint_preserving_core,
    twin_local_sieve_countermodel,
)


class Ticket132BoundaryTheoremTests(unittest.TestCase):
    def test_riemann_anchor_projection_is_invertible(self) -> None:
        audit = riemann_constraint_preserving_core()
        self.assertTrue(audit["machine_audit"]["anchor_matrix_invertible"])
        self.assertLessEqual(
            audit["numeric_projection_audit"]["maximum_residual"], 2e-15
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_accelerated_valuation_replay(self) -> None:
        self.assertEqual(accelerated_valuations(1, 4), [2, 2, 2, 2])
        self.assertEqual(accelerated_valuations(3, 4), [1, 4, 2, 2])

    def test_collatz_natural_codes_hit_every_small_cylinder(self) -> None:
        audit = collatz_natural_code_topology(4, 4)
        replay = audit["finite_cylinder_replay"]
        self.assertEqual(replay["word_count"], 340)
        self.assertEqual(replay["positive_representative_replay_count"], 1020)
        self.assertEqual(replay["failure_count"], 0)

    def test_goldbach_power_two_stratum_keeps_minimal_multiplier(self) -> None:
        audit = goldbach_power_of_two_hard_stratum()
        contract = audit["fixed_endpoint_contract"]
        self.assertGreater(
            Fraction(contract["margin_K56_at_multiplier_one"]["exact"]), 0
        )
        self.assertLess(
            Fraction(
                contract["margin_K57_at_multiplier_one_using_lower_floor"]["exact"]
            ),
            0,
        )
        self.assertTrue(
            audit["machine_audit"]["all_power_rows_have_minimal_multiplier"]
        )

    def test_crt_solver(self) -> None:
        residue, modulus = crt([(1, 2), (2, 3), (1, 5)])
        self.assertEqual(modulus, 30)
        self.assertEqual(residue, 11)

    def test_twin_crt_rows_are_small_prime_clean_and_composite(self) -> None:
        audit = twin_local_sieve_countermodel((5, 11, 29, 97))
        self.assertEqual(audit["machine_audit"]["audited_level_count"], 4)
        self.assertEqual(audit["machine_audit"]["constructed_pair_count"], 12)
        self.assertTrue(audit["machine_audit"]["all_crt_rows_pass"])
        self.assertTrue(all(row["row_failure_count"] == 0 for row in audit["crt_rows"]))

    def test_all_conjectures_remain_open(self) -> None:
        audit = build_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["problem_count"], 4)
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
