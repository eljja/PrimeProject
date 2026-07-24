from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket137_cancellation_entropy_and_information_budget import (  # noqa: E402
    SCHEMA,
    affine_cap,
    build_audit,
    cylinder_residue,
    prefix_affine_cap_mass,
    rational_phase_pair_transcript,
    sylvester_hadamard,
    terminal_affine_cap_mass,
    valuation_prefix,
)


class Ticket137CancellationEntropyInformationBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket137-cancellation-entropy-and-information-budget.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_hadamard_cancellation_defeats_absolute_schur(self) -> None:
        matrix = sylvester_hadamard(8)
        self.assertEqual(len(matrix), 8)
        for left in range(8):
            for right in range(8):
                product = sum(
                    matrix[left][column] * matrix[right][column]
                    for column in range(8)
                )
                self.assertEqual(product, 8 if left == right else 0)
        rows = self.audit["riemann"]["hadamard_audit"]["rows"]
        for row in rows:
            self.assertGreater(
                Fraction(row["true_operator_margin"]["exact"]), Fraction(0)
            )
            self.assertLess(
                Fraction(row["absolute_schur_margin"]["exact"]), Fraction(0)
            )

    def test_collatz_affine_caps_and_mass_are_exact(self) -> None:
        for lower_bound in [2, 10, 1000]:
            for depth in [4, 8, 16]:
                cap = affine_cap(lower_bound, depth)
                self.assertLessEqual(
                    (2**cap) * lower_bound**depth,
                    (3 * lower_bound + 1) ** depth,
                )
                self.assertGreater(
                    (2 ** (cap + 1)) * lower_bound**depth,
                    (3 * lower_bound + 1) ** depth,
                )
                self.assertLessEqual(
                    prefix_affine_cap_mass(lower_bound, depth),
                    terminal_affine_cap_mass(lower_bound, depth),
                )

    def test_every_finite_collatz_word_has_large_natural_representatives(self) -> None:
        for word in [(1, 2, 1), (2, 1, 3), (3, 2, 2)]:
            residue, modulus = cylinder_residue(word)
            self.assertEqual(Fraction(2, modulus), Fraction(1, 2 ** sum(word)))
            for multiplier in [1, 9, 101]:
                self.assertEqual(
                    valuation_prefix(residue + multiplier * modulus, len(word)),
                    word,
                )

    def test_goldbach_subpower_wheel_keeps_log_moment_pressure(self) -> None:
        rows = self.audit["goldbach"]["wheel_audit"]["rows"]
        self.assertGreaterEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(
                row["hard_residues_per_period"],
                sum(
                    1
                    for index in range(1, row["wheel"] + 1)
                    if gcd(2 * index, row["wheel"]) == 1
                ),
            )
            self.assertGreater(row["hard_stratum_size"], 0)
            self.assertGreater(
                row["minimum_p_for_factor_at_most_6_over_5"], 1
            )

    def test_twin_rational_fourier_budget_has_in_range_collisions(self) -> None:
        characters = [(1, 3), (2, 5), (1, 8)]
        for value in [1, 7, 29]:
            self.assertEqual(
                rational_phase_pair_transcript(value, characters),
                rational_phase_pair_transcript(value + 120, characters),
            )
        audit = self.audit["twin_prime"]["information_budget_audit"]
        self.assertGreater(audit["total_collision_count"], 0)
        self.assertEqual(audit["failure_count"], 0)
        self.assertTrue(
            all(row["row_failure_count"] == 0 for row in audit["rows"])
        )

    def test_each_track_has_one_revised_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin",
            "collatz": "ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet",
            "goldbach": "NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56",
            "twin_prime": "IrrationalOrSupercriticalAperiodicTypeIITwinSeparation",
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(section["route_decision"]["next_theorem"], theorem)
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"], 0
                )


if __name__ == "__main__":
    unittest.main()
