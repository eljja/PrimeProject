from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket224_sharp_completeness_thresholds as ticket224  # noqa: E402


class Ticket224SharpCompletenessThresholdsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket224.build_audit()
        cls.root = cls.audit["sharp_completeness_thresholds_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket224.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_quarter_constant_is_verified_and_attained(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["sharp_quarter_tail_envelope_proved"])
        self.assertTrue(aggregate["uniform_constant_optimality_proved"])
        self.assertTrue(aggregate["strict_sign_margin_certificate_proved"])
        self.assertFalse(aggregate["actual_zeta_prime_side_margin_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])
        self.assertEqual(len(section["model_tail_rows"]), 6)
        self.assertEqual(len(section["sharpness_rows"]), 9)
        self.assertTrue(
            all(row["bound_verified"] for row in section["model_tail_rows"])
        )
        self.assertTrue(
            all(row["equality_verified"] for row in section["sharpness_rows"])
        )

    def test_collatz_prime_power_criterion_and_radical_counterexample(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        witness = section["explicit_radical_false_positive"]
        finite = section["finite_audit"]
        self.assertEqual(witness["valuation_word"], [1, 1, 2, 4, 3])
        self.assertEqual(witness["D"], 1805)
        self.assertEqual(witness["B"], 475)
        self.assertEqual(witness["rad_D"], 95)
        self.assertTrue(witness["rad_D_divides_B"])
        self.assertFalse(witness["D_divides_B"])
        self.assertTrue(witness["verified"])
        self.assertEqual(finite["words_checked"], 1360)
        self.assertEqual(finite["prime_power_criterion_mismatches"], 0)
        self.assertEqual(finite["radical_false_positive_count"], 5)
        self.assertFalse(section["aggregate"]["all_nontrivial_cycles_excluded"])

    def test_goldbach_square_root_exactness_and_false_diagonals(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["primality_filter_mismatches"] == 0
                and row["exactness_verified"]
                for row in section["square_root_exactness_rows"]
            )
        )
        for row in section["subthreshold_false_positive_rows"]:
            self.assertTrue(row["diagonal_false_positive_verified"])
            self.assertGreater(row["false_positive_excess"], 0)
            self.assertTrue(row["z_below_sqrt_N"])
            self.assertFalse(ticket224.is_prime(row["composite_m"]))
        self.assertFalse(
            section["aggregate"][
                "sub_square_root_prime_weighted_remainder_controlled"
            ]
        )

    def test_twin_square_root_exactness_and_crt_countermodels(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["primality_filter_mismatches"] == 0
                for row in section["square_root_exactness_rows"]
            )
        )
        for row in section["subthreshold_crt_countermodels"]:
            n = row["composite_n"]
            self.assertTrue(row["countermodel_verified"])
            self.assertEqual(n % row["external_left_factor"], 0)
            self.assertEqual((n + 2) % row["external_right_factor"], 0)
            self.assertGreater(math.sqrt(n + 2), row["cutoff_z"])
            self.assertFalse(ticket224.is_prime(n))
            self.assertFalse(ticket224.is_prime(n + 2))
        self.assertFalse(
            section["aggregate"][
                "uniform_sub_square_root_type_ii_separation_proved"
            ]
        )

    def test_square_root_filter_contract_directly(self) -> None:
        for horizon in (500, 5000):
            cutoff = math.ceil(math.sqrt(horizon))
            primes = ticket224.primes_through(cutoff)
            for value in range(2, horizon + 1):
                self.assertEqual(
                    ticket224.wheel_filter(value, cutoff, primes),
                    ticket224.is_prime(value),
                )

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket224.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket224-sharp-completeness-thresholds.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket224.SCHEMA)
        machine = integrated["sharp_completeness_thresholds_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
