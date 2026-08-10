from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket208_vertical_threeone_unitlog_cyclotomic as ticket208


class Ticket208VerticalThreeOneUnitLogCyclotomicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket208.build_audit()

    def test_sigma_two_vertical_clearance_is_explicit_and_positive(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        previous = float("inf")
        for row in section["vertical_clearance_rows"]:
            lower = float(row["uniform_vertical_clearance_lower_decimal"])
            self.assertGreater(lower, 0)
            self.assertLessEqual(lower, previous)
            previous = lower
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["explicit_sigma_two_vertical_clearance_proved"])
        self.assertFalse(aggregate["horizontal_cofinal_clearance_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_exactly_three_valuation_one_cycles_are_excluded(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        rows = section["exact_enumeration_rows"]
        self.assertEqual(sum(row["enumerated_word_count"] for row in rows), 185)
        self.assertTrue(
            all(row["positive_odd_integer_fixed_point_count"] == 0 for row in rows)
        )
        self.assertTrue(
            section["length_at_least_twelve_exclusion"]["left_exceeds_right"]
        )
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            4,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_three_one_enumeration_independently_replays_every_word(self) -> None:
        total = 0
        for length in range(4, 12):
            maximum = ticket208.total_valuation_upper_bound(length)
            words = ticket208.three_one_words(length, maximum)
            total += len(words)
            for word in words:
                self.assertEqual(word[0], 1)
                self.assertGreaterEqual(word[-1], 2)
                self.assertEqual(word.count(1), 3)
                self.assertLessEqual(sum(word), maximum)
                fixed = ticket208.cycle_fixed_point(word)
                self.assertFalse(
                    fixed is not None
                    and fixed.denominator == 1
                    and fixed.numerator >= 3
                    and fixed.numerator % 2 == 1
                )
        self.assertEqual(total, 185)

    def test_unit_log_goldbach_crt_certificates(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["crt_unit_log_fixture_rows"]:
            target = int(row["canonical_even_target_N"])
            modulus = int(row["modulus_M"])
            self.assertEqual(target % 2, 0)
            self.assertGreater(target, modulus)
            self.assertLessEqual(target, 3 * modulus)
            self.assertGreater(Fraction(row["exact_B_over_bit_length_lower_proxy"]), 0)
            for forcing in row["forcing_rows"]:
                complement = target - forcing["excluded_witness_prime"]
                self.assertGreater(complement, forcing["forcing_divisor"])
                self.assertEqual(complement % forcing["forcing_divisor"], 0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["unit_constant_limsup_lower_bound_proved"])
        self.assertFalse(aggregate["goldbach_counterexample_found"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_cyclotomic_reconstruction_and_zero_mode_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        twin_free_rows = []
        for row in section["interval_reconstruction_rows"]:
            self.assertTrue(row["reconstruction_exact"])
            self.assertEqual(
                Fraction(row["spectral_reconstruction"]),
                row["exact_twin_count_T"],
            )
            self.assertEqual(
                row["zero_mode_raw_contribution"]
                + row["all_nonzero_modes_raw_aggregate"],
                row["cyclotomic_modulus_M"] ** 2 * row["exact_twin_count_T"],
            )
            if row["exact_twin_count_T"] == 0:
                twin_free_rows.append(row)
                self.assertEqual(
                    row["all_nonzero_modes_raw_aggregate"],
                    -row["length_H"],
                )
        self.assertTrue(twin_free_rows)
        for row in section["fixed_dimension_alias_rows"]:
            self.assertFalse(row["is_prime"])
            self.assertTrue(row["root_filter_accepts_as_omega_congruent_to_one"])
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            self.assertEqual(
                self.audit[key]["proof_dag"]["nodes"][-1]["status"],
                "open_not_proven",
            )

    def test_written_outputs_match_attempt_contract(self) -> None:
        ticket208.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket208-vertical-threeone-unitlog-cyclotomic.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], ticket208.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
