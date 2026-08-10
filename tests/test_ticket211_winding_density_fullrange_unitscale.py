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

import ticket211_winding_density_fullrange_unitscale as ticket211


class Ticket211WindingDensityFullRangeUnitScaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket211.build_audit()

    def test_symmetric_entire_model_has_off_line_lattice_zeros(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for ordinate in range(-3, 4):
            for real in (Fraction(1, 4), Fraction(3, 4)):
                root = complex(float(real), ordinate)
                self.assertLess(
                    abs(ticket211.symmetric_entire_countermodel(root)), 1e-11
                )
                self.assertNotEqual(real, Fraction(1, 2))
        for sample in (complex(-1, 2), complex(0.3, -1.2), complex(1.4, 3.1)):
            self.assertAlmostEqual(
                ticket211.symmetric_entire_countermodel(1 - sample).real,
                ticket211.symmetric_entire_countermodel(sample).real,
                places=10,
            )
            self.assertAlmostEqual(
                ticket211.symmetric_entire_countermodel(1 - sample).imag,
                ticket211.symmetric_entire_countermodel(sample).imag,
                places=10,
            )
        for row in section["band_rows"]:
            self.assertTrue(row["sample_respects_exact_bound"])
            self.assertEqual(row["total_zeros_in_closed_band_rectangle"], 2)
            self.assertEqual(row["critical_line_zeros_in_band"], 0)
            self.assertEqual(row["argument_principle_winding_increment"], 2)
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_density_floor_and_rational_counterfamily_are_exact(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        floor = math.log(Fraction(6, 5), 2)
        self.assertAlmostEqual(
            float(section["necessary_density_bound"]["decimal"]), floor, places=11
        )
        orbit = [Fraction(23, 5), Fraction(37, 5), Fraction(29, 5)]
        for current, valuation, expected in zip(
            orbit, (1, 2, 2), orbit[1:] + orbit[:1], strict=True
        ):
            self.assertEqual((3 * current + 1) / 2**valuation, expected)
        product = math.prod(Fraction(3) + 1 / value for value in orbit)
        self.assertEqual(product, 32)
        for row in section["counterfamily_rows"]:
            repetitions = row["block_repetitions_m"]
            word = (1, 2, 2) * repetitions
            self.assertEqual(ticket211.affine_word_fixed_point(word), Fraction(23, 5))
            self.assertGreater(Fraction(repetitions, 3 * repetitions), floor)
            self.assertFalse(row["positive_integer_fixed_point"])
            self.assertTrue(row["aggregate_checks_hold"])
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_small_witness_and_full_exception_predicates_differ(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["finite_dyadic_rows"]:
            self.assertGreater(row["small_witness_exception_count"], 0)
            self.assertEqual(row["full_goldbach_exception_count"], 0)
            self.assertEqual(len(row["transcript_sha256"]), 64)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["small_witness_below_one_route_refuted"])
        self.assertFalse(aggregate["full_range_tail_exception_bound_proved"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_goldbach_finite_rows_replay_independently(self) -> None:
        expected = self.audit["goldbach"]["reproducible_computation"][
            "finite_dyadic_rows"
        ]
        replay = ticket211.goldbach_exception_rows()
        self.assertEqual(replay, expected)

    def test_factorial_twin_desert_certificates_and_unit_limit_rows(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        rows = section["factorial_unit_scale_rows"]
        for row in rows[:6]:
            parameter = row["factorial_parameter_K"]
            base = math.factorial(parameter)
            for offset in range(2, parameter - 1):
                self.assertEqual((base + offset) % offset, 0)
                self.assertEqual((base + offset + 2) % (offset + 2), 0)
            self.assertTrue(row["all_composite_pair_certificates_hold"])
        ratios = [
            float(row["H_over_log_X_over_loglog_X_decimal"]) for row in rows
        ]
        self.assertGreater(ratios[-1], 1.0)
        self.assertLess(ratios[-1], max(ratios))
        self.assertTrue(
            section["aggregate"]["asymptotically_unit_scale_twin_deserts_proved"]
        )
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket211.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket211-winding-density-fullrange-unitscale.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket211.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        for attempt in integrated["attempts"]:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertTrue(attempt["declared_proposition"])
            self.assertTrue(attempt["discarded_route"])
            self.assertTrue(attempt["remaining_gap"])
            self.assertTrue(attempt["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
