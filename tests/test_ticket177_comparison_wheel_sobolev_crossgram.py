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

from ticket177_comparison_wheel_sobolev_crossgram import (  # noqa: E402
    build_audit,
    collatz_six_wheel_audit,
    collatz_wheel_record,
    goldbach_sobolev_audit,
    riemann_comparison_majorant_audit,
    six_wheel_candidates,
    sobolev_pointwise_certificate,
    twin_signed_crossgram_audit,
)


class Ticket177ComparisonWheelSobolevCrossGramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_comparison_majorant_audit()
        cls.collatz = collatz_six_wheel_audit()
        cls.goldbach = goldbach_sobolev_audit()
        cls.twin = twin_signed_crossgram_audit()

    def test_riemann_predeclared_comparison_weight_is_exact(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        rows = self.riemann["relative_scale_rows"]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertGreater(row["certified_relative_margin"], 0)
            self.assertTrue(
                math.isclose(
                    row["predeclared_sine_weight_bound"],
                    row["comparison_spectral_radius"],
                    rel_tol=1e-12,
                )
            )
            self.assertGreaterEqual(
                row["constant_weight_comparison_bound"],
                row["comparison_spectral_radius"],
            )

    def test_collatz_post_first_states_use_six_wheel(self) -> None:
        self.assertEqual(self.collatz["failure_count"], 0)
        for start in [3, 27, 63, 703, 35_655]:
            row = collatz_wheel_record(start)
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["six_wheel_discrete_envelope"],
                row["odd_only_discrete_envelope"] + 1e-14,
            )

    def test_six_wheel_order_bound_holds_in_every_odd_residue(self) -> None:
        for start in [1, 3, 5, 7, 9, 11]:
            for index, value in enumerate(
                six_wheel_candidates(start, 32), start=1
            ):
                self.assertGreaterEqual(value, start + 3 * index - 2)
                self.assertEqual(value % 2, 1)
                self.assertNotEqual(value % 3, 0)

    def test_collatz_static_wheel_is_sharper_but_not_equivalent(self) -> None:
        finite = self.collatz["finite_first_descent_audit"]
        self.assertEqual(finite["odd_starts_checked"], 49_999)
        self.assertEqual(finite["six_wheel_boundary_non_crossing_starts"], [63])
        coefficients = self.collatz["asymptotic_coefficients"]
        self.assertTrue(
            math.isclose(coefficients["new_to_old_ratio"], 2 / 3)
        )

    def test_goldbach_sobolev_bridge_has_both_valid_routes(self) -> None:
        derivative_route = sobolev_pointwise_certificate(2.0, 1.0, 100.0)
        energy_route = sobolev_pointwise_certificate(1.0, 4.0, 0.01)
        false_route = sobolev_pointwise_certificate(
            1.0, 2 * math.pi * 1.1, 1.1**2 / 2
        )
        self.assertTrue(derivative_route["certificate_passes"])
        self.assertTrue(energy_route["certificate_passes"])
        self.assertFalse(false_route["certificate_passes"])

    def test_goldbach_raw_scale_is_reported_as_failure_not_proof(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        aggregate = self.goldbach["aggregate"]
        self.assertEqual(aggregate["support_count"], 5)
        self.assertEqual(aggregate["raw_global_certificate_pass_count"], 0)
        self.assertEqual(aggregate["cosine_counterexample_count"], 4)
        ratios = [
            row["sobolev_cubic_ratio"]
            for row in self.goldbach["finite_fixed_farey_rows"]
        ]
        self.assertGreater(ratios[0], ratios[-1])

    def test_twin_block_norm_summary_loses_signed_cross_information(self) -> None:
        self.assertEqual(self.twin["failure_count"], 0)
        rows = self.twin["identical_norm_summary_counterfamilies"]
        self.assertEqual(
            {tuple(row["component_operator_norms"]) for row in rows},
            {(1.0, 1.0)},
        )
        self.assertEqual(
            sorted(row["aggregate_operator_norm"] for row in rows),
            [0.0, 1.0, 2.0],
        )
        self.assertEqual(
            self.twin["aggregate"]["t161_rows_without_signed_cross_gram"],
            4,
        )

    def test_machine_audit_and_dags_remain_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            statuses = [
                node["status"]
                for node in audit[section_name]["proof_dag"]["nodes"]
            ]
            self.assertEqual(
                statuses,
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_generated_machine_artifacts_match_claim_boundary(self) -> None:
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket177-comparison-wheel-sobolev-crossgram.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            payload["status"],
            "four_exact_refinements_all_conjectures_open",
        )
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(
                attempt["status"] == "open_not_proven"
                for attempt in payload["attempts"]
            )
        )
        for path in [
            "riemann/rh-ticket-177-comparison-majorant.json",
            "collatz/co-ticket-177-six-wheel-envelope.json",
            "goldbach/gb-ticket-177-sobolev-certificate.json",
            "twin-prime/tp-ticket-177-signed-crossgram.json",
        ]:
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / path).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(artifact["status"], "open_not_proven")


if __name__ == "__main__":
    unittest.main()
