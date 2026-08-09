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

import ticket203_rouche_transfer_pointwise_primorial as ticket203


class Ticket203RoucheTransferPointwisePrimorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket203.build_audit()

    def test_rouche_transfer_requires_included_zero_count(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        row = section["exact_synthetic_regression"]
        self.assertEqual(row["relative_boundary_error_bound"], "1/10")
        self.assertEqual(row["strict_rouche_margin"], "9/10")
        self.assertEqual(row["comparison_zero_count_inside"], 4)
        self.assertEqual(row["independently_certified_X_zero_count_inside"], 4)
        self.assertTrue(row["certified_list_is_exhaustive"])
        self.assertFalse(
            section["aggregate"]["actual_xi_boundary_margin_constructed"]
        )

    def test_signed_collatz_transfer_identities_and_minimal_no_go(self) -> None:
        forward = ticket203.forward_transfer_row((3, 1), 0, 1)
        self.assertEqual(forward["denominator_D"], 7)
        self.assertEqual(forward["source_numerator_B"], 11)
        self.assertEqual(forward["target_numerator_B_prime"], 7)
        self.assertFalse(forward["source_affine_divisibility"])
        self.assertTrue(forward["target_affine_divisibility"])
        self.assertTrue(
            forward["forward_identity_B_prime_equals_B_minus_Q_over_2"]
        )
        backward = ticket203.backward_transfer_row((1, 3), 0, 1)
        self.assertTrue(backward["backward_identity_B_prime_equals_B_plus_Q"])

        section = self.audit["collatz"]["reproducible_computation"]
        summaries = section["exhaustive_regression"]
        self.assertEqual(
            section["aggregate"]["exhaustive_forward_transfer_count"],
            310_103,
        )
        self.assertEqual(
            [row["target_divisibility_hit_count"] for row in summaries],
            [1, 3, 6, 10, 15, 21],
        )
        self.assertTrue(
            section["aggregate"][
                "all_finite_hits_are_all_two_in_tested_box"
            ]
        )

    def test_goldbach_projector_equivalence_and_stronger_target_model(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        actual = section["exact_actual_channel_rows"]
        abstract = section["exact_abstract_countermodel_rows"]
        self.assertEqual(actual[0]["ordered_prime_prime_R"], 12)
        self.assertEqual(actual[-1]["relative_defect_delta"], "3240/5029")
        self.assertTrue(all(row["positivity_equivalence"] for row in actual))
        bounds = [
            Fraction(row["loglog_N_times_delta_upper_bound_2m2_over_2m"])
            for row in abstract
        ]
        self.assertTrue(
            all(bounds[index + 1] < bounds[index] for index in range(4))
        )
        self.assertTrue(
            section["aggregate"][
                "loglog_scaled_lower_bound_is_stronger_than_goldbach"
            ]
        )
        self.assertFalse(section["aggregate"]["actual_goldbach_counterexample_found"])

    def test_fixed_primorial_residue_collision(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        rows = section["exact_finite_collision_rows"]
        self.assertEqual(rows[-1]["primorial_W"], 2310)
        self.assertEqual(rows[-1]["prime_p_congruent_1_mod_W"], 2311)
        self.assertEqual(rows[-1]["semiprime_pq_congruent_1_mod_W"], 10_679_131)
        self.assertTrue(all(row["full_residue_collision"] for row in rows))
        self.assertTrue(
            all(row["small_divisibility_signature_collision"] for row in rows)
        )
        self.assertFalse(
            section["aggregate"][
                "scale_growing_or_bilinear_switching_weights_refuted"
            ]
        )

    def test_machine_audit_keeps_all_parent_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.audit[section_key]
            self.assertIn("No ", section["claim_boundary"])
            self.assertEqual(
                section["proof_dag"]["nodes"][-1]["status"],
                "open_not_proven",
            )

    def test_written_outputs_match_schema_and_attempts(self) -> None:
        ticket203.write_outputs(self.audit)
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket203-rouche-transfer-pointwise-primorial.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], ticket203.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
