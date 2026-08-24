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

import ticket237_angle_palette_endpoint_welch as ticket237  # noqa: E402


class Ticket237AnglePaletteEndpointWelchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket237.build_audit()
        cls.root = cls.audit[ticket237.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket237.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertIn("resolves none", self.audit["claim_boundary"])
        self.assertEqual(
            self.root["machine_audit"],
            {
                "exact_partial_or_no_go_theorem_count": 4,
                "refuted_or_reduced_route_count": 4,
                "next_single_lemma_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        self.assertEqual(
            {row["problem_id"] for row in self.audit["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )

    def test_riemann_principal_angle_and_nested_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        rows = computation["exact_principal_angle_rows"]
        self.assertEqual([row["frame_dimension_m"] for row in rows], [2, 4, 8, 16, 32])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertEqual(Fraction(row["nested_normalized_cross_norm"]["exact"]), 1)
            self.assertEqual(Fraction(row["nested_block_minimum_eigenvalue"]["exact"]), 0)
            self.assertEqual(Fraction(row["innovation_normalized_cross_norm"]["exact"]), Fraction(3, 5))
            self.assertEqual(Fraction(row["innovation_block_minimum_eigenvalue"]["exact"]), Fraction(2, 5))
        self.assertEqual(
            computation["transcript_sha256"],
            "fd62bdfa9c45783e6130244c51dd0f4710ff599876966585ef0b983eb4da88cc",
        )
        self.assertTrue(computation["aggregate"]["nested_cofinal_strict_contraction_refuted"])
        self.assertFalse(computation["aggregate"]["arithmetic_weil_innovation_angle_gap_proved"])
        self.assertFalse(computation["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_every_finite_palette_is_disabled(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        rows = computation["finite_palette_rows"]
        self.assertEqual(
            [(row["finite_prime_palette"], row["palette_period_L"]) for row in rows],
            [
                ([5], 2),
                ([2, 3, 5, 7, 59], 174),
                ([5, 7, 13, 19, 31, 37, 59], 5220),
                ([2, 3, 5, 7, 13, 19, 31, 37, 59, 57653], 2594340),
            ],
        )
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertTrue(
                all(
                    check["all_palette_witnesses_disabled"]
                    for check in row["first_three_common_multiple_checks"]
                )
            )
        self.assertEqual(
            computation["transcript_sha256"],
            "49967e87d8f554e67eb9eda00554ae3530f6556d81de89d706c206fefd6a0ecc",
        )
        self.assertTrue(computation["aggregate"]["arbitrary_finite_prime_palette_universality_refuted"])
        self.assertFalse(computation["aggregate"]["fresh_prime_existence_for_general_necklaces_proved"])
        self.assertFalse(computation["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_dyadic_upper_endpoint_obstruction(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["exact_upper_endpoint_rows"]
        self.assertEqual(
            [(row["cutoff_X"], row["prime_count_pi_X"], row["ordered_representation_count_g_X_2X"]) for row in rows],
            [(30, 10, 0), (31, 11, 1), (100, 25, 0), (101, 26, 1), (1000, 168, 0), (1009, 169, 1), (10000, 1229, 0), (10007, 1230, 1)],
        )
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            expected = int(row["cutoff_is_prime"])
            self.assertEqual(row["ordered_representation_count_g_X_2X"], expected)
            self.assertEqual(
                Fraction(row["normalized_phase_margin_g_over_pi"]["exact"]),
                Fraction(expected, row["prime_count_pi_X"]),
            )
        self.assertEqual(
            computation["transcript_sha256"],
            "eab7e70119f64a68bb7710865a84a7e3ae22e83f9209416ed682e7c87b9ab9f9",
        )
        self.assertTrue(computation["aggregate"]["closed_dyadic_interval_inverse_log_margin_refuted"])
        self.assertFalse(computation["aggregate"]["buffered_bulk_prime_phase_gain_proved"])
        self.assertFalse(computation["aggregate"]["strong_goldbach_conjecture_resolved"])

    def test_twin_finite_support_welch_floor(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        sharp_rows = computation["exact_sharp_walsh_rows"]
        self.assertEqual(
            [(row["support_size_s"], row["coordinate_count_m"], row["degree_two_energy_E_m_2"]["exact"]) for row in sharp_rows],
            [(4, 6, "1/5"), (4, 12, "3/11"), (8, 14, "1/13"), (8, 28, "1/9"), (16, 30, "1/29")],
        )
        self.assertTrue(all(row["bound_attained_exactly"] for row in sharp_rows))
        actual_rows = computation["actual_twin_start_support_rows"]
        self.assertEqual(
            [(row["cutoff_X"], row["active_prime_count_m"], row["twin_start_count_s"], row["welch_support_lower_bound"]["exact"]) for row in actual_rows],
            [(100, 6, 4, "1/10"), (200, 12, 9, "1/33"), (300, 18, 11, "7/187")],
        )
        self.assertTrue(all(row["certificate_verified"] for row in actual_rows))
        self.assertEqual(
            computation["transcript_sha256"],
            "dbc58d3770c892e560789a49d7d929199bddacd9709e9977fcff9836ab78fd8f",
        )
        self.assertTrue(computation["aggregate"]["degree_two_decay_forces_growing_support_proved"])
        self.assertFalse(computation["aggregate"]["prime_weighted_degree_two_decay_proved"])
        self.assertFalse(computation["aggregate"]["twin_prime_conjecture_resolved"])

    def test_each_track_has_one_successor_and_guarded_dag(self) -> None:
        for problem in ("riemann", "collatz", "goldbach", "twin_prime"):
            track = self.root[problem]
            self.assertTrue(track["route_decision"]["next_single_lemma"])
            statuses = {node["status"] for node in track["proof_dag"]["nodes"]}
            self.assertIn("closed", statuses)
            self.assertIn("refuted_or_limited", statuses)
            self.assertIn("highest_risk_open", statuses)
            self.assertIn("open_not_proven", statuses)

    def test_outputs_are_reproducible(self) -> None:
        ticket237.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket237-angle-palette-endpoint-welch.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket237.SCHEMA)
        machine = integrated[ticket237.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
