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

from ticket188_nested_fourone_primepower_dyadic import (  # noqa: E402
    balanced_four_gaps,
    build_audit,
    canonical_four_one_word,
    finite_four_one_horizon_row,
    four_one_closed_form,
    four_one_cycle_row,
    four_one_global_bound,
    integer_nth_root,
    prime_power_metadata,
)


class Ticket188NestedFourOnePrimePowerDyadicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_nested_defect_is_nondecreasing(self) -> None:
        defects = [
            Fraction(row["negative_defect"]["exact"])
            for row in self.riemann["exact_nested_interlacing_rows"]
        ]
        self.assertEqual(defects, [Fraction(0)] + [Fraction(1, 7)] * 5)
        self.assertTrue(
            all(left <= right for left, right in zip(defects, defects[1:]))
        )

    def test_moving_negative_direction_refutes_defect_only_promotion(self) -> None:
        rows = self.riemann["moving_negative_direction_counterfamily"]
        defects = [Fraction(row["negative_defect"]["exact"]) for row in rows]
        self.assertTrue(all(row["indefinite"] for row in rows))
        self.assertTrue(all(not row["exactly_nested"] for row in rows))
        self.assertTrue(
            all(left > right for left, right in zip(defects, defects[1:]))
        )
        self.assertFalse(
            self.riemann["aggregate"]["common_form_weil_contract_verified"]
        )

    def test_four_one_closed_form_matches_recurrence(self) -> None:
        row = four_one_cycle_row(4, 4, 4, 4)
        self.assertTrue(all(row["checks"].values()))
        word = canonical_four_one_word(4, 4, 4, 4)
        self.assertEqual(len(word), 16)
        self.assertEqual(sum(value == 1 for value in word), 4)
        self.assertEqual(
            four_one_closed_form(4, 4, 4, 4),
            int(row["affine_numerator_B"]),
        )

    def test_four_one_finite_exception_range_is_complete(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(10, 16)))
        self.assertEqual(
            sum(row["word_count"] for row in rows),
            sum(math.comb(horizon, 4) for horizon in range(10, 16)),
        )
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], 4_116
        )
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))

    def test_four_one_majorant_closes_every_horizon_from_16(self) -> None:
        self.assertEqual(
            Fraction(
                self.collatz["analytic_bound"]["bound_at_h_16"]["exact"]
            ),
            Fraction(63_175_275, 33_554_432),
        )
        self.assertLess(four_one_global_bound(16), 2)
        self.assertTrue(
            all(
                four_one_global_bound(horizon + 1)
                <= four_one_global_bound(horizon)
                for horizon in range(16, 128)
            )
        )
        for horizon in [16, 17, 31, 64, 127]:
            self.assertEqual(sum(balanced_four_gaps(horizon)), horizon)
            self.assertEqual(
                balanced_four_gaps(horizon)[-1],
                max(balanced_four_gaps(horizon)),
            )

    def test_four_one_transcript_is_deterministic(self) -> None:
        first = finite_four_one_horizon_row(15)
        second = finite_four_one_horizon_row(15)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], 1_365)

    def test_prime_power_metadata_is_exact_on_representative_values(self) -> None:
        metadata = prime_power_metadata(100)
        self.assertEqual(metadata[2], (2, 1))
        self.assertEqual(metadata[16], (2, 4))
        self.assertEqual(metadata[81], (3, 4))
        self.assertIsNone(metadata[72])
        self.assertEqual(integer_nth_root(100_000, 2), 316)
        self.assertEqual(integer_nth_root(100_000, 5), 10)

    def test_von_mangoldt_decomposition_keeps_contamination(self) -> None:
        rows = self.goldbach["finite_decomposition_rows"]
        self.assertEqual(
            [row["even_target_N"] for row in rows],
            [18, 100, 1_000, 10_000, 100_000],
        )
        n18 = rows[0]
        self.assertEqual(n18["ordered_prime_power_contamination_count"], 3)
        self.assertIn(
            [9, 9, 2, 2],
            n18["contamination_examples_left_right_exponents"],
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_subfour_twin_interval_is_exact_count_oracle(self) -> None:
        rows = self.twin["finite_dyadic_rows"]
        self.assertEqual([row["dyadic_exponent_j"] for row in rows], list(range(4, 20)))
        self.assertEqual(rows[-1]["direct_twin_count_C_j"], 3_785)
        for row in rows:
            interval = row["sound_subfour_interval"]
            self.assertTrue(interval["exact_count_certified"])
            self.assertEqual(
                interval["minimum_compatible_twin_count"],
                row["direct_twin_count_C_j"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_width_four_is_sharp_and_no_infinite_claim_is_made(self) -> None:
        boundary = self.twin["sharp_width_four_counterinterval"]
        self.assertTrue(boundary["ambiguous_between_zero_and_positive"])
        self.assertFalse(
            self.twin["aggregate"]["independent_analytic_interval_construction"]
        )
        self.assertEqual(self.twin["aggregate"]["conjecture_resolution_count"], 0)

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_stratum_closure_count": 1,
                "rejected_or_corrected_route_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_json_contract_has_four_open_attempts_and_finite_values(self) -> None:
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket188-nested-fourone-primepower-dyadic.json"
        )
        payload_text = path.read_text(encoding="utf-8")
        payload = json.loads(payload_text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(row["status"] == "open_not_proven" for row in payload["attempts"])
        )
        self.assertNotIn(": Infinity", payload_text)
        self.assertNotIn(": -Infinity", payload_text)
        self.assertNotIn(": NaN", payload_text)


if __name__ == "__main__":
    unittest.main()
