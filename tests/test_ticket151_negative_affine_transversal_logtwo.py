from __future__ import annotations

import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket151_negative_affine_transversal_logtwo import (  # noqa: E402
    SCHEMA,
    affine_word_data,
    build_audit,
    cyclic_convolution,
    weighted_hole_radius,
)


class Ticket151NegativeAffineTransversalLogTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket151-negative-affine-transversal-logtwo.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_generated_wrapper_schema_and_attempts(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(len(self.payload["attempts"]), 4)
        self.assertIn(
            "negative_affine_transversal_logtwo_audit",
            self.payload,
        )
        self.assertEqual(
            {attempt["problem_id"] for attempt in self.payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )

    def test_riemann_negative_part_is_the_exact_threshold(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        positive_rows = computation["finite_large_positive_spectrum_rows"]
        negative_rows = computation[
            "finite_negative_threshold_failure_rows"
        ]
        self.assertEqual(len(positive_rows), 48)
        self.assertEqual(len(negative_rows), 16)
        for row in positive_rows:
            full_norm = Fraction(row["full_relative_norm"]["exact"])
            negative_norm = Fraction(row["negative_part_norm"]["exact"])
            minimum = Fraction(
                row["minimum_eigenvalue_of_I_plus_B"]["exact"]
            )
            self.assertGreater(full_norm, 1)
            self.assertLessEqual(negative_norm, 1)
            self.assertEqual(minimum, 1 - negative_norm)
            self.assertGreaterEqual(minimum, 0)
            self.assertTrue(all(row["checks"].values()))
        for row in negative_rows:
            negative_norm = Fraction(row["negative_part_norm"]["exact"])
            minimum = Fraction(
                row["minimum_eigenvalue_of_I_plus_B"]["exact"]
            )
            self.assertGreater(negative_norm, 1)
            self.assertEqual(minimum, 1 - negative_norm)
            self.assertLess(minimum, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_affine_threshold_and_natural_counterexample(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_positive_surplus_nondescending_rows"
        ]
        self.assertEqual(len(rows), 32)
        witness = next(row for row in rows if row["start_n"] == "165")
        self.assertEqual(witness["length_m"], 17)
        self.assertEqual(witness["valuation_sum_S"], 27)
        self.assertEqual(witness["multiplier_gap_D"], "5077565")
        self.assertEqual(witness["terminal_Tm_n"], "167")
        for row in rows:
            start = int(row["start_n"])
            length = row["length_m"]
            replay = affine_word_data(start, length)
            threshold = Fraction(row["exact_descent_threshold_C_over_D"]["exact"])
            self.assertEqual(replay["valuation_word"], row["valuation_word"])
            self.assertGreater(int(row["multiplier_gap_D"]), 0)
            self.assertLessEqual(Fraction(start), threshold)
            self.assertFalse(row["strict_descent"])
            self.assertTrue(row["same_word_lift_descends"])
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_type_two_forced_horizon_cannot_descend(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_type_two_forced_affine_rows"
        ]
        self.assertEqual(len(rows), 35)
        for row in rows:
            shadow_pairs = row["shadow_pair_count_L"]
            delay = row["forced_post_delay_H"]
            expected_word = [value for _ in range(shadow_pairs) for value in (1, 2)]
            expected_word.extend([1, 1])
            expected_word.extend([1] * delay)
            self.assertEqual(row["valuation_word"], expected_word)
            self.assertLess(int(row["multiplier_gap_D"]), 0)
            self.assertFalse(row["strict_descent"])
            self.assertTrue(all(row["checks"].values()))

    def test_weighted_reflection_hole_radius_is_constructively_sharp(
        self,
    ) -> None:
        weights = [
            Fraction(7, 3),
            Fraction(5, 2),
            Fraction(4, 3),
            Fraction(3, 2),
            Fraction(2, 3),
            Fraction(1, 2),
        ]
        for endpoint in range(len(weights)):
            witness = weights.copy()
            visited: set[int] = set()
            for index in range(len(weights)):
                if index in visited:
                    continue
                partner = (endpoint - index) % len(weights)
                visited.update({index, partner})
                if partner == index:
                    witness[index] = Fraction(0)
                elif weights[index] <= weights[partner]:
                    witness[index] = Fraction(0)
                else:
                    witness[partner] = Fraction(0)
            distance = sum(
                (left - right) ** 2
                for left, right in zip(weights, witness)
            )
            self.assertEqual(
                distance,
                weighted_hole_radius(weights, endpoint),
            )
            self.assertEqual(cyclic_convolution(witness, endpoint), 0)

    def test_goldbach_global_moments_do_not_determine_endpoint_mass(
        self,
    ) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_permutation_moment_counterrows"
        ]
        self.assertEqual(len(rows), 16)
        for row in rows:
            hole = [Fraction(value) for value in row["hole_weights"]]
            positive = [
                Fraction(value) for value in row["positive_weights"]
            ]
            self.assertEqual(sorted(hole), sorted(positive))
            self.assertEqual(cyclic_convolution(hole, 3), 0)
            self.assertGreater(cyclic_convolution(positive, 3), 0)
            for power in range(1, 7):
                self.assertEqual(
                    sum(value**power for value in hole),
                    sum(value**power for value in positive),
                )
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_prime_indicator_audit_stays_finite(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_prime_indicator_radius_rows"
        ]
        self.assertEqual([row["cutoff"] for row in rows], [100, 1000, 10000, 20000])
        for row in rows:
            self.assertEqual(row["zero_radius_endpoints"], [])
            self.assertGreater(
                row["minimum_prime_indicator_hole_radius_squared"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_cubic_rough_population_is_prime_or_semiprime(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cubic_rough_population_rows"
        ]
        self.assertEqual([row["X"] for row in rows], [1000, 10000, 100000, 1000000])
        distances = []
        for row in rows:
            self.assertEqual(row["other_composite_count"], 0)
            self.assertLess(row["normalized_liouville_mean"], 0)
            self.assertTrue(all(row["checks"].values()))
            distances.append(row["distance_to_log_two"])
        self.assertTrue(
            all(right < left for left, right in zip(distances, distances[1:]))
        )
        target = self.audit["twin_prime"]["reproducible_computation"][
            "target_constants"
        ]["semiprime_to_prime_ratio_log_two"]
        self.assertAlmostEqual(target, math.log(2), places=15)

    def test_twin_shifted_selection_has_no_automatic_sign_transfer(
        self,
    ) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        countermodels = computation["finite_selection_countermodel_rows"]
        shifted = computation["finite_gap_two_shifted_rows"]
        self.assertEqual(len(countermodels), 4)
        self.assertEqual(len(shifted), 4)
        for row in countermodels:
            self.assertGreater(
                row["prime_only_selected_deficit_T_minus_D"],
                0,
            )
            self.assertLess(
                row["semiprime_only_selected_deficit_T_minus_D"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))
        for row in shifted:
            self.assertGreater(row["gap_two_cubic_rough_edges_E"], 0)
            self.assertLess(
                Fraction(
                    row["left_edge_conditioned_liouville_mean"]["exact"]
                ),
                0,
            )
            self.assertLess(
                Fraction(
                    row["right_edge_conditioned_liouville_mean"]["exact"]
                ),
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_next_lemmas_are_single_and_proof_dags_end_open(self) -> None:
        expected = {
            "riemann": "ActualWeilNegativeRelativeFormPartBoundAtMostOne",
            "collatz": (
                "TypeTwoAffineThresholdCylinderCoverBelowShadowEntry"
            ),
            "goldbach": (
                "OrbitResolvedVonMangoldtApproximationInsideWeightedHoleRadiusK56"
            ),
            "twin_prime": (
                "PositiveGapTwoCubicRoughMassAndShiftedLogTwoMarginalTransfer"
            ),
        }
        for problem, next_theorem in expected.items():
            section = self.audit[problem]
            self.assertEqual(
                section["route_decision"]["next_theorem"],
                next_theorem,
            )
            dag = section["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["label"], next_theorem)
            self.assertEqual(dag["nodes"][-1]["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
