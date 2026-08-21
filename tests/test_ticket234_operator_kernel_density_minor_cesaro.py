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

import ticket234_operator_kernel_density_minor_cesaro as ticket234  # noqa: E402


class Ticket234OperatorKernelDensityMinorCesaroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket234.build_audit()
        cls.root = cls.audit[ticket234.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket234.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertIn("resolves none", self.audit["claim_boundary"])
        self.assertEqual(
            self.root["machine_audit"],
            {
                "exact_partial_or_no_go_theorem_count": 4,
                "refuted_or_corrected_route_count": 4,
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

    def test_riemann_scalar_floor_has_exact_kernel_and_tail_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["first_horizon_with_logarithmic_dimension_below_band_dimension"],
            35,
        )
        rows = computation["exact_finite_field_kernel_rows"]
        self.assertEqual([row["frequency_horizon_T"] for row in rows], [64, 256, 1024, 4096])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(all(row["nullity_lower_bound"] > 0 for row in rows))
        self.assertTrue(all(row["maximum_exact_modular_residual"] == 0 for row in rows))
        self.assertEqual(
            rows[0]["transcript_sha256"],
            "783f612bbbfa76530b185c995aebe43738dd33a4d6c9c22591e09dd5cf572dda",
        )
        perturbations = computation["arbitrarily_small_signed_tail_rows"]
        self.assertTrue(
            all(
                Fraction(row["quadratic_value_on_unit_kernel_vector"]["exact"])
                == -Fraction(row["epsilon"]["exact"])
                for row in perturbations
            )
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["scalar_diagonal_floor_with_singular_full_gram_proved"])
        self.assertFalse(aggregate["actual_weil_tail_kernel_compatibility_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_every_fixed_finite_affine_sieve_has_false_positives(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        totals = computation["fixed_affine_modulus_totals"]
        self.assertEqual(totals["moduli_checked"], 66)
        self.assertEqual(totals["maximum_one_count_k"], 198)
        self.assertEqual(totals["failure_count"], 0)
        self.assertEqual(
            totals["transcript_sha256"],
            "7299d7a4c09b0f2c9bb319c9605be6114984c4be104b0893f0ba5da73b72f0b4",
        )
        rows = {row["modulus_M"]: row for row in computation["fixed_affine_modulus_rows"]}
        self.assertEqual(
            (rows[5]["affine_order_r1"], rows[5]["affine_order_r2"], rows[5]["one_count_k"]),
            (2, 4, 4),
        )
        self.assertEqual(
            (rows[199]["affine_order_r1"], rows[199]["affine_order_r2"], rows[199]["one_count_k"]),
            (66, 198, 198),
        )
        self.assertTrue(all(row["finite_modulus_false_positive_verified"] for row in rows.values()))
        self.assertTrue(
            all(
                row["certificate_verified"]
                for row in computation["simultaneous_fixed_modulus_family_rows"]
            )
        )
        radical = computation["radical_deficit_finite_scan"]
        self.assertEqual(radical["raw_density_band_words"], 1_893_010)
        self.assertEqual(radical["primitive_necklaces"], 90_272)
        self.assertEqual(radical["radical_false_positives"], 0)
        self.assertEqual(
            radical["transcript_sha256"],
            "1cccdf893126fde404f1546078b581194aa41025797370c5a41319c86d404344",
        )
        self.assertFalse(computation["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_half_channels_cancel_major_mass_exactly(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["central_half_channel_rows"]
        self.assertEqual([row["even_target_N"] for row in rows], [100, 1000, 10000])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            all(
                row["central_major_LL"] >= row["central_major_LL_lower_bound"]
                and row["central_major_UU"] >= row["central_major_UU_lower_bound"]
                and row["central_major_LU"] >= row["central_major_LU_lower_bound"]
                for row in rows
            )
        )
        self.assertTrue(all(row["exact_full_LL_target_coefficient"] == 0 for row in rows))
        self.assertTrue(all(row["minor_LL_equals_negative_major_LL"] for row in rows))
        self.assertEqual(
            computation["central_half_channel_transcript_sha256"],
            "d2122cff761d2e13b5e9335f88bcad8bf936f583dda057f53dfc323f190fedf8",
        )
        self.assertEqual(
            computation["central_half_channel_transcript_precision_decimal_places"], 6
        )
        self.assertEqual(
            computation["central_half_channel_row_precision_decimal_places"], 9
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["strict_full_minor_margin_equivalent_to_goldbach_endpoint"])
        self.assertFalse(aggregate["inverse_log_minor_reflection_coherence_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_critical_noise_is_fixed_degree_cesaro_poissonization(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        moving = computation["moving_half_exact_counterexample_rows"]
        self.assertTrue(all(row["certificate_verified"] for row in moving))
        self.assertTrue(
            all(Fraction(row["degree_one_cesaro_E_m_1"]["exact"]) == Fraction(1, 8) for row in moving)
        )
        self.assertLess(
            abs(float(Fraction(moving[-1]["critical_noise_D_m"]["exact"])) - (math.exp(1 / 8) - 1)),
            0.001,
        )
        actual = computation["actual_twin_start_finite_audit_rows"]
        self.assertEqual([row["twin_start_count"] for row in actual], [202, 1220, 1219])
        self.assertTrue(all(row["certificate_verified"] for row in actual))
        self.assertEqual(actual[0]["critical_noise_D_m"]["exact"], "12301/5222912")
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["critical_noise_fixed_degree_cesaro_equivalence_proved"])
        self.assertTrue(aggregate["fixed_labeled_coefficientwise_decay_sufficiency_refuted"])
        self.assertFalse(aggregate["actual_prime_weighted_fixed_degree_cesaro_decay_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

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
        ticket234.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket234-operator-kernel-density-minor-cesaro.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket234.SCHEMA)
        machine = integrated[ticket234.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
