from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket205_winding_extremal_finite_omega as ticket205


class Ticket205WindingExtremalFiniteOmegaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket205.build_audit()

    def test_direct_polygonal_winding_certificate(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        fixture = section["exact_argument_principle_fixture"]
        no_go = section["finite_sample_winding_no_go"]
        self.assertEqual(fixture["image_excursion_Mh_upper"], "11/14")
        self.assertEqual(fixture["zero_avoidance_margin_lower"], "3/14")
        self.assertEqual(fixture["certified_polygon_winding"], 3)
        self.assertEqual(fixture["certified_interior_zero_count"], 3)
        self.assertTrue(fixture["all_segment_disks_exclude_zero"])
        self.assertTrue(no_go["all_sample_values_equal"])
        self.assertEqual((no_go["winding_f0"], no_go["winding_f1"]), (0, 8))
        self.assertFalse(no_go["finite_values_alone_determine_winding"])

    def test_collatz_extremal_stratum_is_removed(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        regression = section["finite_integrality_regression"]
        extrema = section["exact_extremal_inequalities"]
        self.assertEqual(extrema["nontrivial_minimum_outgoing_valuation"], 1)
        self.assertEqual(extrema["nontrivial_maximum_outgoing_valuation_lower"], 2)
        self.assertEqual(regression["total_words_checked"], 87_380)
        self.assertEqual(regression["total_divisible_words"], 8)
        self.assertEqual(regression["non_all_two_divisible_words"], 0)
        self.assertTrue(
            section["aggregate"][
                "all_ge_two_nontrivial_cycle_family_excluded_for_all_lengths"
            ]
        )
        self.assertFalse(section["aggregate"]["mixed_valuation_necklaces_excluded"])

    def test_goldbach_ten_million_witness_stream(self) -> None:
        certificate = self.audit["goldbach"]["reproducible_computation"][
            "exact_finite_witness_certificate"
        ]
        self.assertEqual(certificate["limit"], 10_000_000)
        self.assertEqual(certificate["even_targets_checked"], 4_999_999)
        self.assertEqual(certificate["exception_count"], 0)
        self.assertEqual(certificate["maximum_least_prime_witness"], 751)
        self.assertEqual(certificate["maximum_witness_target"], 3_807_404)
        self.assertEqual(
            certificate["witness_stream_sha256"],
            "ed31375c2d840a190345e901dfaf52e322424d40d7b4afa33ec7977cf0b791dd",
        )
        self.assertEqual(
            certificate["last_target_witness"],
            {
                "target": 10_000_000,
                "least_prime_witness": 29,
                "complementary_prime": 9_999_971,
            },
        )

    def test_omega_divisor_realization_and_product_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        self.assertEqual(section["channel_signs"]["prime_weight_values"], ["1/2"])
        self.assertEqual(
            section["channel_signs"]["semiprime_weight_values"], ["-1"]
        )
        self.assertTrue(
            all(
                row["both_composite"] and row["product_is_positive"]
                for row in section["composite_composite_product_no_go_rows"]
            )
        )
        for value in (1, 2, 4, 12, 30, 210):
            flags = ticket205.prime_power_flags(value)
            self.assertEqual(
                ticket205.prime_power_divisor_sum(value, flags),
                ticket205.omega_with_multiplicity(value),
            )

    def test_machine_audit_keeps_every_conjecture_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.audit[section_key]
            self.assertIn("No ", section["claim_boundary"])
            self.assertEqual(
                section["proof_dag"]["nodes"][-1]["status"], "open_not_proven"
            )

    def test_written_outputs_match_schema_and_attempt_contract(self) -> None:
        ticket205.write_outputs(self.audit)
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket205-winding-extremal-finite-omega.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], ticket205.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
