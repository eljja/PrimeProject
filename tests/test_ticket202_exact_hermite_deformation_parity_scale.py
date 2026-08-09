from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket202_exact_hermite_deformation_parity_scale as ticket202


class Ticket202ExactHermiteDeformationParityScaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket202.build_audit()

    def test_exact_hermite_no_go_preserves_nodes_and_crosses_threshold(self) -> None:
        before = ticket202.hermite_perturbation_row(2)
        first = ticket202.hermite_perturbation_row(3)
        self.assertFalse(before["all_jet_bounds_below_epsilon"])
        self.assertTrue(first["all_jet_bounds_below_epsilon"])
        self.assertTrue(first["all_hermite_constraints_preserved_exactly"])
        self.assertTrue(first["G_N_iA_is_zero_exactly"])
        self.assertEqual(first["coefficient_c_N"], "-1/11474737664000000")
        self.assertEqual(first["maximum_jet_bound"], "224180121/35306885120")
        section = self.audit["riemann"]["reproducible_computation"]
        self.assertEqual(section["exact_regression"]["first_certifying_N"], 3)
        self.assertFalse(
            section["aggregate"]["xi_completed_zeta_structure_preserved"]
        )

    def test_long_run_deformation_identity_for_independent_parameters(self) -> None:
        expected = {
            (2, 2, 0): "630",
            (4, 7, 3): "15919845493554",
            (10, 10, 8): "645287991783491369250",
            (31, 5, 13): None,
        }
        for parameters, residual in expected.items():
            row = ticket202.collatz_deformed_row(*parameters)
            self.assertTrue(row["direct_numerator_matches_closed_form"])
            self.assertTrue(row["master_identity_holds_exactly"])
            self.assertTrue(row["zero_less_than_F_k_t_less_than_D"])
            self.assertEqual(row["gcd_D_with_2_times_27n"], 1)
            self.assertTrue(row["primitive_word"])
            self.assertFalse(row["affine_divisibility_hit"])
            self.assertEqual(row["cyclic_rotation_divisibility_hit_count"], 0)
            if residual is not None:
                self.assertEqual(row["F_k_t_equals_minus_E_k_t"], residual)
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(section["aggregate"]["regression_word_count"], 729)
        self.assertTrue(
            section["aggregate"][
                "all_nonnegative_long_run_extensions_covered_symbolically"
            ]
        )

    def test_goldbach_dyadic_projector_and_dilution_regression(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        rows = section["exact_finite_rows"]
        self.assertEqual(rows[0]["prime_prime_aggregate_R"], 38397)
        self.assertEqual(rows[0]["relative_defect_one_minus_L_over_C"], "25598/36655")
        self.assertEqual(rows[-1]["prime_composite_semiprime_aggregate_S"], 25629463902)
        self.assertEqual(
            rows[-1]["relative_defect_one_minus_L_over_C"],
            "18844127294/35051527549",
        )
        self.assertTrue(all(row["C_minus_L_equals_2R"] for row in rows))
        self.assertTrue(
            section["aggregate"]["fixed_positive_relative_defect_refuted_asymptotically"]
        )
        self.assertFalse(section["aggregate"]["goldbach_resolved"])

    def test_twin_relative_defect_transfer_and_countermodel(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        actual = section["exact_finite_rows"]
        countermodel = section["exact_abstract_countermodel_rows"]
        self.assertTrue(all(row["normalized_transfer_identity"] for row in actual))
        self.assertEqual(actual[-1]["relative_defect_delta_X"], "45286/88451")
        self.assertTrue(all(row["twin_positive"] for row in countermodel))
        self.assertEqual(countermodel[-1]["relative_defect_delta_X"], "1/596523")
        self.assertTrue(
            section["aggregate"]["fixed_relative_defect_is_stronger_than_infinitude"]
        )
        self.assertFalse(
            section["aggregate"]["fixed_relative_defect_refuted_for_actual_twin_channels"]
        )

    def test_machine_audit_and_claim_boundaries_remain_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.audit[section_key]
            self.assertIn("No ", section["claim_boundary"])
            self.assertEqual(section["proof_dag"]["nodes"][-1]["status"], "open_not_proven")

    def test_written_outputs_match_schema_and_attempts(self) -> None:
        ticket202.write_outputs(self.audit)
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket202-exact-hermite-deformation-parity-scale.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], ticket202.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
