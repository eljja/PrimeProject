from __future__ import annotations

import json
import math
import sys
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket187_positive_ray_threeone_signature_interval import (  # noqa: E402
    build_audit,
    canonical_three_one_word,
    finite_three_one_horizon_row,
    goldbach_signature_row,
    prime_sieve,
    quantized_twin_interval,
    smallest_prime_factors,
    three_one_closed_form,
    three_one_cycle_row,
)


class Ticket187PositiveRayThreeOneSignatureIntervalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_riemann_numerical_replay_is_positive_but_not_interval_certified(self) -> None:
        aggregate = self.riemann["aggregate"]
        replay = self.riemann["pole_neutral_numerical_replay"]
        self.assertTrue(aggregate["pole_neutral_replay_values_positive"])
        self.assertTrue(replay["difference_below_reported_tail_remainder"])
        self.assertFalse(replay["is_rigorous_interval_certificate"])
        self.assertGreater(Decimal(replay["route1_center"]["exact_decimal"]), 0)

    def test_riemann_source_provenance_is_pinned(self) -> None:
        source = self.riemann["source_provenance"]
        self.assertEqual(source["arxiv"], "2607.02828v1")
        self.assertEqual(source["license"], "CC BY 4.0")
        self.assertEqual(
            source["source_sha256"],
            "95e0f1d613d217478b1145ddef7fd884"
            "b0aa2c42bb477474848e44256df8f83d",
        )
        self.assertEqual(len(source["vector"]), 7)

    def test_reported_ldlt_provenance_is_internally_consistent_not_rerun(self) -> None:
        provenance = self.riemann["reported_interval_ldlt_provenance"]
        self.assertEqual(provenance["dimension"], 401)
        self.assertEqual(provenance["n_pos"], 401)
        self.assertEqual(provenance["n_neg"], 0)
        self.assertIsNone(provenance["undetermined_pivot"])
        self.assertTrue(provenance["certified_positive_definite"])
        self.assertFalse(provenance["independently_rerun_by_primeproject"])

    def test_positive_ray_does_not_promote_to_matrix_psd(self) -> None:
        counter = self.riemann["finite_section_no_go_extension"]
        self.assertTrue(counter["agrees_on_original_section"])
        self.assertTrue(counter["extension_is_indefinite"])
        self.assertFalse(self.riemann["aggregate"]["cofinal_family_certified"])

    def test_three_one_closed_form_matches_recurrence(self) -> None:
        row = three_one_cycle_row(4, 4, 5)
        self.assertTrue(all(row["checks"].values()))
        word = canonical_three_one_word(4, 4, 5)
        self.assertEqual(sum(value == 1 for value in word), 3)
        self.assertEqual(three_one_closed_form(4, 4, 5), 12_190_991)

    def test_three_one_finite_exception_range_is_complete(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(8, 13)))
        self.assertEqual(
            sum(row["word_count"] for row in rows),
            sum(math.comb(horizon, 3) for horizon in range(8, 13)),
        )
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"], 645
        )
        self.assertTrue(
            all(row["divisibility_hit_count"] == 0 for row in rows)
        )

    def test_three_one_threshold_bound_is_exact(self) -> None:
        bound = self.collatz["analytic_bound"]
        self.assertLess(
            Fraction(bound["tail_at_h_13"]["exact"]),
            Fraction(bound["available_budget"]["exact"]),
        )
        self.assertEqual(bound["analytic_range_starts_at_h"], 13)
        self.assertTrue(self.collatz["aggregate"]["infinite_family_proved"])

    def test_finite_horizon_transcript_is_deterministic(self) -> None:
        first = finite_three_one_horizon_row(12)
        second = finite_three_one_horizon_row(12)
        self.assertEqual(
            first["remainder_transcript_sha256"],
            second["remainder_transcript_sha256"],
        )
        self.assertEqual(first["word_count"], 220)

    def test_goldbach_prime_and_bad_signatures_are_identical(self) -> None:
        is_prime = prime_sieve(1_000)
        least_factor = smallest_prime_factors(1_000)
        row = goldbach_signature_row(1_000, is_prime, least_factor)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(row["shared_gate_sigma_N"], 29)
        self.assertEqual(row["maximum_indistinguishable_depth_Y"], 28)

    def test_signed_postprocessing_cannot_restore_lost_signature_label(self) -> None:
        rows = self.goldbach["target_signature_rows"]
        self.assertTrue(
            all(row["checks"]["truncated_signatures_are_identical"] for row in rows)
        )
        self.assertEqual(
            self.goldbach["aggregate"]["largest_indistinguishable_depth"], 310
        )

    def test_quantized_interval_rounding_rules_are_sharp(self) -> None:
        positive = quantized_twin_interval(Fraction(1, 1000), Fraction(7999, 1000))
        zero = quantized_twin_interval(Fraction(-1, 1000), Fraction(3999, 1000))
        ambiguous = quantized_twin_interval(Fraction(0), Fraction(4))
        self.assertTrue(positive["positive_count_certified"])
        self.assertTrue(zero["zero_count_certified"])
        self.assertTrue(ambiguous["ambiguous_between_zero_and_positive"])

    def test_actual_twin_ledgers_are_recovered_from_half_unit_intervals(self) -> None:
        for row in self.twin["finite_cubic_rough_interval_rows"]:
            self.assertTrue(all(row["checks"].values()))
            interval = row["certified_count_interval"]
            self.assertEqual(
                interval["minimum_compatible_twin_count"],
                row["direct_twin_count"],
            )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_stratum_closure_count": 1,
                "attributed_primary_artifact_audit_count": 1,
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
            / "ticket187-positive-ray-threeone-signature-interval.json"
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
