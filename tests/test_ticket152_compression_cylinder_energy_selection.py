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

from ticket152_compression_cylinder_energy_selection import (  # noqa: E402
    SCHEMA,
    build_audit,
    first_descent_index,
    realize_next_valuation,
    valuation_word,
    word_cylinder,
)


class Ticket152CompressionCylinderEnergySelectionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket152-compression-cylinder-energy-selection.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_generated_wrapper_and_per_problem_artifacts(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(len(self.payload["attempts"]), 4)
        self.assertEqual(
            {row["problem_id"] for row in self.payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        paths = [
            "riemann/rh-ticket-152-compression-tail.json",
            "collatz/co-ticket-152-cylinder-cover.json",
            "goldbach/gb-ticket-152-global-l2-no-go.json",
            "twin-prime/tp-ticket-152-selection-coverage.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_compressions_need_an_infinite_exhaustion(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        hidden = computation["finite_hidden_direction_rows"]
        tails = computation["finite_tail_certificate_rows"]
        self.assertEqual(len(hidden), 7)
        self.assertEqual(len(tails), 9)
        for row in hidden:
            self.assertGreaterEqual(
                Fraction(
                    row["checked_compression_minimum_mu_N"]["exact"]
                ),
                -1,
            )
            self.assertLess(
                Fraction(row["full_spectral_infimum"]["exact"]),
                -1,
            )
            self.assertTrue(all(row["checks"].values()))
        for row in tails:
            epsilon = Fraction(
                row["operator_norm_tail_epsilon"]["exact"]
            )
            finite_minimum = Fraction(
                row["finite_rank_minimum"]["exact"]
            )
            certified = Fraction(
                row["certified_full_lower_bound"]["exact"]
            )
            self.assertEqual(certified, finite_minimum - epsilon)
            self.assertGreaterEqual(certified, -1)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_word_is_one_exact_arithmetic_cylinder(self) -> None:
        words = [[1], [2], [1, 1], [1, 2, 3], [3, 1]]
        for word in words:
            cylinder = word_cylinder(word)
            residue = cylinder["least_positive_residue"]
            modulus = cylinder["modulus"]
            self.assertEqual(valuation_word(residue, len(word)), word)
            for lift in range(20):
                self.assertEqual(
                    valuation_word(residue + lift * modulus, len(word)),
                    word,
                )

    def test_collatz_descent_set_is_a_terminal_cylinder_tail(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_cylinder_tail_rows"
        ]
        self.assertEqual(len(rows), 10)
        for row in rows:
            word = row["valuation_word"]
            self.assertEqual(
                row["first_descent_lift_index_k"],
                first_descent_index(word),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_next_valuation_is_unbounded_on_each_cylinder(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_unbounded_next_valuation_rows"
        ]
        self.assertEqual(len(rows), 25)
        for row in rows:
            parent = row["parent_word"]
            valuation = row[
                "constructed_missing_next_valuation_B_plus_1"
            ]
            witness = realize_next_valuation(parent, valuation)
            replay = valuation_word(
                witness["start_n"],
                len(parent) + 1,
            )
            self.assertEqual(replay, parent + [valuation])
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_global_l2_ball_is_already_missed_finitely(
        self,
    ) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_uniform_baseline_rows"]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000],
        )
        ratios = []
        for row in rows:
            endpoint = row["even_endpoint_N"]
            self.assertEqual(
                row["uniform_endpoint_hole_radius_squared"],
                endpoint / 2,
            )
            self.assertGreater(
                row["von_mangoldt_minus_one_l2_squared"],
                row["uniform_endpoint_hole_radius_squared"],
            )
            self.assertGreater(
                row["von_mangoldt_endpoint_convolution"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))
            ratios.append(row["l2_to_hole_radius_squared_ratio"])
        self.assertTrue(
            all(right > left for left, right in zip(ratios, ratios[1:]))
        )
        self.assertTrue(computation["finite_ratio_strictly_increasing"])

    def test_twin_selection_transfer_threshold_is_sharp(self) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_actual_selection_rows"]
        sharp = computation["finite_sharp_counterselection_rows"]
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(sharp), 4)
        for row, counterrow in zip(rows, sharp):
            ambient_sum = row["ambient_liouville_sum_A"]
            omitted = row["omitted_vertices_q"]
            self.assertLess(ambient_sum, 0)
            self.assertGreaterEqual(omitted, -ambient_sum)
            self.assertFalse(
                row["ambient_bias_guarantees_selected_negative"]
            )
            self.assertGreaterEqual(
                counterrow["sharp_maximum_selected_sum"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))
            self.assertTrue(all(counterrow["checks"].values()))

    def test_twin_gap_two_coverage_decreases_in_finite_audit(self) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_actual_selection_rows"]
        coverages = [
            Fraction(row["selected_coverage_E_over_M"]["exact"])
            for row in rows
        ]
        self.assertTrue(
            all(
                right < left
                for left, right in zip(coverages, coverages[1:])
            )
        )
        self.assertTrue(computation["finite_coverage_strictly_decreasing"])
        target = computation["target_constants"][
            "required_retention_limit"
        ]
        self.assertAlmostEqual(
            target,
            2 * math.log(2) / (1 + math.log(2)),
            places=15,
        )

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "ActualWeilCoreCompressionWithCertifiedOperatorNorm"
                "TailBelowMargin"
            ),
            "collatz": (
                "TypeTwoCountableExtensionCoverWithUniformAnalytic"
                "ValuationTail"
            ),
            "goldbach": (
                "EndpointBilinearVonMangoldtErrorBelowSingularSeries"
                "MainTermK56"
            ),
            "twin_prime": (
                "DirectShiftedCubicRoughLiouvilleSumNegativeProportion"
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
            self.assertEqual(
                dag["nodes"][-1]["status"],
                "open_not_proven",
            )


if __name__ == "__main__":
    unittest.main()
