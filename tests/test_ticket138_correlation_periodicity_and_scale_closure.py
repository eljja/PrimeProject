from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket138_correlation_periodicity_and_scale_closure import (  # noqa: E402
    SCHEMA,
    build_audit,
    pell_sqrt2_rows,
    periodic_affine_data,
    replay_periodic_fraction,
    sylvester_hadamard,
)


class Ticket138CorrelationPeriodicityScaleClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket138-correlation-periodicity-and-scale-closure.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_cross_gram_bound_uses_signed_correlations(self) -> None:
        self.assertEqual(
            self.audit["riemann"]["exact_contract"]["positive_tail_bounds"],
            "alpha>0 and gamma>0",
        )
        for dimension in [4, 8, 16]:
            matrix = sylvester_hadamard(dimension)
            for left in range(dimension):
                for right in range(dimension):
                    product = sum(
                        matrix[left][column] * matrix[right][column]
                        for column in range(dimension)
                    )
                    self.assertEqual(
                        product, dimension if left == right else 0
                    )
        rows = self.audit["riemann"]["correlation_audit"]["hadamard_rows"]
        for row in rows:
            self.assertEqual(
                Fraction(row["cross_gram_operator_bound"]["exact"]),
                Fraction(row["exact_operator_norm_squared"]["exact"]),
            )
            self.assertGreater(
                Fraction(row["certified_margin"]["exact"]), Fraction(0)
            )

    def test_signed_means_do_not_control_operator_norm(self) -> None:
        rows = self.audit["riemann"]["correlation_audit"][
            "coherent_counterfamily_rows"
        ]
        for row in rows:
            self.assertEqual(Fraction(row["signed_row_sum"]["exact"]), 0)
            self.assertEqual(Fraction(row["signed_column_sum"]["exact"]), 0)
            self.assertEqual(
                Fraction(row["exact_operator_norm_squared"]["exact"]), 1
            )

    def test_periodic_collatz_affine_fixed_points_replay_exactly(self) -> None:
        expected = {
            (1,): Fraction(-1),
            (2,): Fraction(1),
            (1, 2): Fraction(-5, 1),
        }
        for word, fixed_point in expected.items():
            data = periodic_affine_data(word)
            self.assertEqual(data["fixed_point"], fixed_point)
            replay_end, replay_word = replay_periodic_fraction(
                fixed_point, word
            )
            self.assertEqual(replay_end, fixed_point)
            self.assertEqual(replay_word, word)

    def test_subcritical_periodic_codes_are_negative(self) -> None:
        for word in [(1,), (1, 1), (1, 2, 1), (2, 1, 1, 1)]:
            data = periodic_affine_data(word)
            if data["denominator"] < 0:
                self.assertLess(data["fixed_point"], 0)
        audit = self.audit["collatz"]["periodic_code_audit"]
        self.assertEqual(audit["total_word_count"], 9840)
        self.assertGreater(audit["total_subcritical_word_count"], 0)
        self.assertEqual(
            audit["total_nontrivial_positive_integer_fixed_point_count"], 0
        )

    def test_goldbach_all_scale_wheel_bound_includes_near_full_rows(self) -> None:
        rows = self.audit["goldbach"]["wheel_audit"]["rows"]
        self.assertEqual(len(rows), 20)
        self.assertEqual(
            sum(row["complete_period_blocks_M"] == 1 for row in rows), 5
        )
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertGreaterEqual(
                2 * row["hard_stratum_size"] ** 2, row["scale_X"]
            )

    def test_irrational_phase_pell_returns_are_near_not_exact(self) -> None:
        rows = pell_sqrt2_rows()
        self.assertEqual(len(rows), 12)
        previous = float("inf")
        for row in rows:
            self.assertEqual(
                abs(row["pell_residual_p2_minus_2q2"]), 1
            )
            self.assertNotEqual(row["pell_residual_p2_minus_2q2"], 0)
            self.assertLess(row["absolute_phase_error"], previous)
            previous = row["absolute_phase_error"]
        for denominator in range(1, 200):
            nearest = round((2**0.5) * denominator)
            self.assertNotEqual(nearest * nearest, 2 * denominator * denominator)

    def test_each_track_has_one_revised_open_lemma_and_dag(self) -> None:
        expected = {
            "riemann": "ProjectedWeilCrossGramCorrelationBudgetBelowTailGap",
            "collatz": "AffineCappedNaturalCodeWellFoundedness",
            "goldbach": "PointwiseSignedBinaryGoldbachResidualK56",
            "twin_prime": (
                "RegularAperiodicTypeIICancellationWithPositiveTwinMass"
            ),
        }
        for problem, theorem in expected.items():
            with self.subTest(problem=problem):
                section = self.audit[problem]
                self.assertEqual(
                    section["route_decision"]["next_theorem"], theorem
                )
                self.assertEqual(
                    section["proof_dag"]["nodes"][-1]["status"],
                    "open_not_proven",
                )
                self.assertEqual(
                    section["machine_audit"]["conjecture_resolution_count"], 0
                )


if __name__ == "__main__":
    unittest.main()
