from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket144_schur_rank_equivalence_variation_adverse_walsh import (  # noqa: E402
    exact_ldl_pivots,
    walsh_coefficients_from_counts,
)
from ticket146_toeplitz_polynomial_phase_frechet import (  # noqa: E402
    SCHEMA,
    build_audit,
    cyclic_autocorrelation,
    cyclic_convolution,
    cyclic_translate,
    first_polynomial_counteredge,
    frechet_row,
    levinson_real,
    real_toeplitz,
)


class Ticket146ToeplitzPolynomialPhaseFrechetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket146-toeplitz-polynomial-phase-frechet.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_levinson_errors_are_exact_schur_pivots(self) -> None:
        moments = [
            Fraction(2),
            Fraction(1),
            Fraction(3, 4),
            Fraction(1, 3),
            Fraction(1, 5),
            Fraction(1, 8),
            Fraction(1, 13),
        ]
        recurrence = levinson_real(moments)
        errors = [
            Fraction(row["exact"])
            for row in recurrence["prediction_errors"]
        ]
        pivots = [
            exact_ldl_pivots(real_toeplitz(moments, size))[-1]
            for size in range(1, len(moments) + 1)
        ]
        self.assertEqual(errors, pivots)

    def test_every_fixed_lag_prefix_has_an_unseen_negative_pivot(
        self,
    ) -> None:
        for lag in range(1, 18):
            moments = [Fraction(1)] + [Fraction(0)] * lag + [Fraction(2)]
            recurrence = levinson_real(moments)
            reflections = [
                Fraction(row["exact"])
                for row in recurrence["reflection_coefficients"]
            ]
            pivots = [
                exact_ldl_pivots(real_toeplitz(moments, size))[-1]
                for size in range(1, len(moments) + 1)
            ]
            with self.subTest(lag=lag):
                self.assertEqual(reflections[:lag], [Fraction(0)] * lag)
                self.assertEqual(reflections[-1], -2)
                self.assertEqual(pivots[:-1], [Fraction(1)] * (lag + 1))
                self.assertEqual(pivots[-1], -3)

    def test_piecewise_polynomial_counteredges(self) -> None:
        profiles = [
            [9],
            [-100, 1],
            [17, -1000, 1],
            [-2, 7, -50, 1],
            [3, -1, 2, -5, 1],
        ]
        for modulus in [1, 3, 7, 16, 64]:
            for coefficients in profiles:
                row = first_polynomial_counteredge(
                    modulus,
                    coefficients,
                )
                edge = row["first_audited_counteredge"]
                with self.subTest(
                    modulus=modulus,
                    coefficients=coefficients,
                ):
                    self.assertEqual(
                        (3 * edge["start"] + 1) // 2,
                        edge["successor"],
                    )
                    self.assertEqual(
                        edge["start"] % modulus,
                        edge["successor"] % modulus,
                    )
                    self.assertGreaterEqual(edge["rank_difference"], 0)

    def test_translation_preserves_power_data_but_moves_convolution(
        self,
    ) -> None:
        for modulus in [11, 17, 23]:
            values = [
                ((index * index + 3 * index + 1) % 7) - 3
                for index in range(modulus)
            ]
            for shift in [1, 2, 4]:
                translated = cyclic_translate(values, shift)
                original_convolution = cyclic_convolution(values, values)
                translated_convolution = cyclic_convolution(
                    translated,
                    translated,
                )
                with self.subTest(modulus=modulus, shift=shift):
                    self.assertEqual(
                        cyclic_autocorrelation(values),
                        cyclic_autocorrelation(translated),
                    )
                    self.assertEqual(
                        translated_convolution,
                        [
                            original_convolution[
                                (target - 2 * shift) % modulus
                            ]
                            for target in range(modulus)
                        ],
                    )

    def test_goldbach_phase_counterexample_is_exact(self) -> None:
        for modulus in [11, 13, 17, 19, 23, 29]:
            values = [0] * modulus
            values[0] = values[1] = 1
            translated = cyclic_translate(values, 2)
            self.assertEqual(
                cyclic_autocorrelation(values),
                cyclic_autocorrelation(translated),
            )
            self.assertEqual(cyclic_convolution(values, values)[0], 1)
            self.assertEqual(
                cyclic_convolution(translated, translated)[0],
                0,
            )

    def test_frechet_bounds_hold_for_all_small_tables(self) -> None:
        for plus_plus in range(7):
            for plus_minus in range(7):
                for minus_plus in range(7):
                    for minus_minus in range(7):
                        row = frechet_row(
                            [
                                plus_plus,
                                plus_minus,
                                minus_plus,
                                minus_minus,
                            ]
                        )
                        self.assertTrue(all(row["checks"].values()))

    def test_perfect_marginals_do_not_determine_twin_mass(self) -> None:
        no_twins = frechet_row([0, 50, 50, 0])
        uniform = frechet_row([25, 25, 25, 25])
        for key in ["A00", "A10", "A01"]:
            self.assertEqual(no_twins[key], uniform[key])
        self.assertEqual(no_twins["reconstructed_twin_class"], 0)
        self.assertEqual(uniform["reconstructed_twin_class"], 25)
        self.assertNotEqual(no_twins["A11"], uniform["A11"])

    def test_one_sided_walsh_budget_is_a_valid_sufficient_bound(
        self,
    ) -> None:
        for counts in [
            [10, 3, 2, 1],
            [25, 25, 25, 25],
            [90, 5, 4, 1],
            [1, 2, 3, 10],
        ]:
            a00, a10, a01, a11 = walsh_coefficients_from_counts(counts)
            epsilon_1 = Fraction(max(a10, 0), a00)
            epsilon_2 = Fraction(max(a01, 0), a00)
            gamma = Fraction(max(-a11, 0), a00)
            budget = epsilon_1 + epsilon_2 + gamma
            lower = Fraction(a00, 4) * (1 - budget)
            if budget < 1:
                self.assertGreaterEqual(Fraction(counts[3]), lower)

    def test_all_proof_dags_close_one_route_and_remain_open(self) -> None:
        for problem in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[problem]["proof_dag"]["nodes"]
            with self.subTest(problem=problem):
                self.assertEqual(
                    [node["status"] for node in nodes],
                    [
                        "refuted_or_insufficient",
                        "proved_exact",
                        "open_not_proven",
                    ],
                )


if __name__ == "__main__":
    unittest.main()
