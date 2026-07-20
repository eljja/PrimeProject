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

from ticket134_uniformity_thresholds_and_scale_no_go import (  # noqa: E402
    K56_MARGIN,
    SCHEMA,
    admissible_classes,
    build_audit,
    congruence_interval,
    fraction_matrix,
    gershgorin_lower_margins,
    interval_box,
    quadratic_interval_upper,
)


class Ticket134UniformityThresholdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()

    def test_global_boundary_is_open_and_failure_free(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(
            SCHEMA,
            "primeproject.ticket134-uniformity-thresholds-and-scale-no-go.v1",
        )
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertIn("None proves or refutes", self.audit["proof_boundary"])

    def test_riemann_rational_preconditioner_and_negative_witness(self) -> None:
        positive = fraction_matrix([[2, 3], [3, 5]])
        lower, upper = interval_box(positive, Fraction(1, 1000))
        direct = gershgorin_lower_margins(lower, upper)
        self.assertTrue(any(margin < 0 for margin in direct))
        transform = fraction_matrix([[1, Fraction(-3, 2)], [0, 1]])
        transformed = congruence_interval(lower, upper, transform)
        self.assertTrue(all(margin > 0 for margin in gershgorin_lower_margins(*transformed)))

        indefinite = fraction_matrix([[1, 2], [2, 1]])
        indefinite_box = interval_box(indefinite, Fraction(1, 100))
        self.assertEqual(
            quadratic_interval_upper(*indefinite_box, [Fraction(1), Fraction(-1)]),
            Fraction(-49, 25),
        )
        self.assertEqual(self.audit["riemann"]["machine_audit"]["total_failure_count"], 0)

    def test_collatz_all_one_words_defeat_every_bounded_depth(self) -> None:
        section = self.audit["collatz"]
        rows = section["finite_replay_audit"]["rows"]
        self.assertEqual(len(rows), 24)
        for row in rows:
            depth = row["depth"]
            self.assertEqual(int(row["residue"]), 2 ** (depth + 1) - 1)
            self.assertEqual(int(row["modulus"]), 2 ** (depth + 1))
            self.assertGreater(int(row["strict_growth"]), 0)
        self.assertIn("unbounded depth", section["proved_statement"])

    def test_goldbach_logarithmic_moment_threshold(self) -> None:
        section = self.audit["goldbach"]
        rows = section["finite_threshold_audit"]["rows"]
        amplitude = 2 * float(K56_MARGIN)
        for row in rows:
            critical = row["normalized_Lp_norms"]["log_critical"]
            self.assertAlmostEqual(critical, amplitude / math.e, places=15)
        subcritical = [
            row["normalized_Lp_norms"]["sqrt_log_subcritical"] for row in rows
        ]
        supercritical = [
            row["normalized_Lp_norms"]["log_squared_supercritical"] for row in rows
        ]
        self.assertTrue(all(a > b for a, b in zip(subcritical, subcritical[1:])))
        self.assertTrue(all(a < b for a, b in zip(supercritical, supercritical[1:])))

    def test_twin_growing_primorial_lifts_have_quantitative_bound(self) -> None:
        classes, modulus = admissible_classes([2, 3, 5, 7])
        self.assertEqual(modulus, 210)
        self.assertEqual(len(classes), 15)
        section = self.audit["twin_prime"]
        growing = section["growing_level_audit"]
        self.assertEqual([row["sieve_level"] for row in growing["rows"]], [5, 7, 11, 13, 17])
        self.assertEqual(growing["total_admissible_classes_lifted"], 23913)
        self.assertTrue(all(row["row_failure_count"] == 0 for row in growing["rows"]))
        self.assertTrue(section["machine_audit"]["all_witnesses_below_twice_modulus"])

    def test_each_track_names_a_stronger_next_theorem(self) -> None:
        expected = {
            "riemann": "UniformProjectedWeilGramTailCertificate",
            "collatz": "WellFoundedUnboundedContractingPrefixCover",
            "goldbach": "LogScaleMomentOrMaximalGoldbachResidualK56",
            "twin_prime": "NearFullScaleParitySensitiveTwinSeparation",
        }
        for key, theorem in expected.items():
            with self.subTest(problem=key):
                self.assertEqual(self.audit[key]["route_decision"]["next_theorem"], theorem)
                self.assertEqual(self.audit[key]["machine_audit"]["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
