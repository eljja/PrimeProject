from __future__ import annotations

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket135_conditional_bridges_and_exceptional_set import (  # noqa: E402
    K56_MARGIN,
    SCHEMA,
    build_audit,
    collatz_survival_audit,
    first_admissible_residues,
    lcm_many,
)


class Ticket135ConditionalBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(SCHEMA, "primeproject.ticket135-conditional-bridges-and-exceptional-set.v1")
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertIn("None proves or refutes", self.audit["proof_boundary"])

    def test_riemann_block_threshold_and_sharp_countermodel(self) -> None:
        section = self.audit["riemann"]
        for row in section["rational_audit"]["accepted_rows"]:
            self.assertGreaterEqual(Fraction(row["schur_margin"]["exact"]), 0)
        bad = section["rational_audit"]["violating_example"]
        self.assertEqual(Fraction(bad["schur_margin"]["exact"]), Fraction(-5, 4))
        self.assertEqual(Fraction(bad["witness_value"]["exact"]), Fraction(-5, 4))

    def test_collatz_survival_mass_is_exactly_partitioned(self) -> None:
        audit = collatz_survival_audit(32)
        self.assertEqual(audit["failure_count"], 0)
        rows = audit["selected_rows"]
        survival = [Fraction(row["survival_mass"]["exact"]) for row in rows]
        self.assertTrue(all(left > right for left, right in zip(survival, survival[1:])))
        self.assertGreater(Fraction(audit["final_survival_mass"]["exact"]), 0)
        self.assertIn("Haar-null", self.audit["collatz"]["proof_boundary"])

    def test_goldbach_sparse_stratum_bridge_uses_required_factor(self) -> None:
        section = self.audit["goldbach"]
        self.assertGreater(Fraction(section["exact_bridge_contract"]["rational_guard"]["exact"]), 0)
        self.assertEqual(
            Fraction(section["exact_bridge_contract"]["sufficient_Lp_threshold"]["exact"]),
            Fraction(5, 6) * K56_MARGIN,
        )
        for row in section["finite_scale_audit"]["rows"]:
            h = row["power_of_two_hard_stratum_size"]
            p = row["moment_order"]
            self.assertEqual(p, 4 * math.ceil(math.log2(h)))
            self.assertLess(row["supremum_inflation_factor"], 6 / 5)

    def test_twin_overlapping_moduli_factor_through_lcm_and_lift(self) -> None:
        self.assertEqual(lcm_many([6, 10, 14, 15]), 210)
        residues = first_admissible_residues(210, 8)
        self.assertEqual(len(residues), 8)
        self.assertTrue(all(math.gcd(a * (a + 2), 210) == 1 for a in residues))
        section = self.audit["twin_prime"]
        rows = section["finite_transcript_audit"]["rows"]
        self.assertEqual(
            section["finite_transcript_audit"]["total_witnesses"],
            sum(row["audited_admissible_residue_count"] for row in rows),
        )
        self.assertEqual(rows[0]["audited_admissible_residue_count"], 15)
        self.assertTrue(all(row["row_failure_count"] == 0 for row in rows))

    def test_each_track_has_one_stronger_open_lemma(self) -> None:
        expected = {
            "riemann": "ProjectedWeilBlockConstantsWithPositiveSchurMargin",
            "collatz": "NaturalCodesCrossAffineDescentThreshold",
            "goldbach": "BinaryGoldbachHardStratumLogMomentBoundK56",
            "twin_prime": "NonCongruenceTypeIITwinSeparation",
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                self.assertEqual(self.audit[problem]["route_decision"]["next_theorem"], theorem)
                self.assertEqual(self.audit[problem]["machine_audit"]["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
