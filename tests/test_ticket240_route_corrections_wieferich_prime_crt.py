from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.ticket240_route_corrections_wieferich_prime_crt import (
    AUDIT_KEY,
    PRIME_LIMIT,
    SCHEMA,
    build_audit,
)


ROOT = Path(__file__).resolve().parents[1]


class Ticket240RouteCorrectionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        machine = self.root["machine_audit"]
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["bounded_prime_scan_limit"], PRIME_LIMIT)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_cotlar_route_correction(self) -> None:
        data = self.root["riemann"]["reproducible_computation"]
        aggregate = data["aggregate"]
        self.assertTrue(aggregate["uniform_positive_gram_family_proved"])
        self.assertTrue(
            aggregate["cotlar_sqrt_overlap_summability_necessity_refuted"]
        )
        self.assertFalse(aggregate["arithmetic_weil_signed_operator_lower_bound_proved"])
        rows = data["exact_model_rows"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[-1]["dimension_J"], 1024)
        self.assertEqual(rows[-1]["uniform_gram_lower_bound"]["exact"], "1/2")
        self.assertGreater(rows[-1]["maximum_cotlar_sqrt_overlap_row_sum"], 60)

    def test_collatz_wieferich_reduction_and_bounded_scan(self) -> None:
        data = self.root["collatz"]["reproducible_computation"]
        scan = data["bounded_rational_wieferich_scan"]
        self.assertTrue(data["aggregate"]["local_defect_fermat_depth_reduction_proved"])
        self.assertFalse(data["aggregate"]["all_prime_depth_domination_proved"])
        self.assertEqual(scan["prime_limit"], 20_000_000)
        self.assertEqual(scan["odd_primes_scanned"], 1_270_605)
        self.assertEqual(scan["x_depth_at_least_two_count"], 0)
        self.assertEqual(scan["y_depth_at_least_two_primes"], [23])
        self.assertEqual(scan["first_order_positive_defect_candidate_count"], 0)
        self.assertTrue(
            all(
                row["depth_reduction_verified"]
                for row in data["representative_depth_reduction_rows"]
            )
        )

    def test_goldbach_signed_slack_is_exact_target(self) -> None:
        data = self.root["goldbach"]["reproducible_computation"]
        rows = data["prime_window_signed_slack_rows"]
        self.assertEqual(len(rows), 15)
        self.assertEqual(data["aggregate"]["zero_restricted_window_row_count"], 1)
        for row in rows:
            self.assertEqual(
                row["strict_negative_dc_threshold_passes"],
                row["restricted_prime_window_representation_exists"],
            )
            self.assertEqual(
                row["integral_unit_slack_threshold_passes"],
                row["restricted_prime_window_representation_exists"],
            )
            self.assertTrue(row["equivalence_verified"])

    def test_twin_one_sided_prime_crt_no_go(self) -> None:
        data = self.root["twin_prime"]["reproducible_computation"]
        patterns = data["exact_all_pattern_crt_rows"]
        grams = data["actual_one_sided_prime_weighted_gram_rows"]
        self.assertEqual(len(patterns), 8)
        self.assertTrue(all(row["certificate_verified"] for row in patterns))
        self.assertTrue(
            data["aggregate"][
                "all_finite_crt_patterns_have_infinite_prime_composite_successors"
            ]
        )
        self.assertEqual([row["coordinate_count_m"] for row in grams], [4, 8, 12])
        self.assertEqual(grams[-1]["upper_scale_X"], 10_000_000)
        self.assertGreater(grams[-1]["gram_effective_rank"], 11.99)
        self.assertFalse(data["aggregate"]["two_sided_parity_breaking_main_term_proved"])

    def test_written_integrated_json_matches_schema(self) -> None:
        path = ROOT / "data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            [item["problem_id"] for item in payload["attempts"]],
            ["riemann", "collatz", "goldbach", "twin-prime"],
        )
        self.assertTrue(all(item["status"] == "open_not_proven" for item in payload["attempts"]))


if __name__ == "__main__":
    unittest.main()
