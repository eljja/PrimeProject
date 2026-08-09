from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket201_finite_information_allrun_liouville_parity as ticket201


class Ticket201FiniteInformationAllRunLiouvilleParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket201.build_audit()

    def test_finite_jet_no_go_has_exact_threshold_and_off_axis_zero(self) -> None:
        before = ticket201.finite_jet_bound_row(8)
        first = ticket201.finite_jet_bound_row(9)
        self.assertFalse(before["all_jet_bounds_below_epsilon"])
        self.assertTrue(first["all_jet_bounds_below_epsilon"])
        self.assertEqual(first["coefficient_c_N"], "-101/1000000000000000000")
        self.assertEqual(first["maximum_jet_bound"], "15453/3276800")
        self.assertTrue(first["G_N_iA_is_zero_exactly"])
        section = self.audit["riemann"]["reproducible_computation"]
        self.assertTrue(section["exact_regression"]["F_has_only_real_zeros"])
        self.assertTrue(section["aggregate"]["finite_compact_jet_no_go_proved"])
        self.assertFalse(
            section["aggregate"]["xi_euler_product_or_gamma_structure_preserved"]
        )

    def test_all_run_collatz_master_identity_and_divisibility_obstruction(self) -> None:
        for run_pairs, scale in ((2, 2), (4, 7), (16, 16), (31, 5), (8, 32)):
            row = ticket201.collatz_all_run_row(run_pairs, scale)
            self.assertTrue(row["master_identity_holds_exactly"])
            self.assertTrue(row["direct_numerator_matches_closed_form"])
            self.assertTrue(row["zero_less_than_F_k_less_than_D"])
            self.assertEqual(row["gcd_D_with_2_times_27n"], 1)
            self.assertFalse(row["affine_divisibility_hit"])
            self.assertEqual(row["cyclic_rotation_divisibility_hit_count"], 0)
            self.assertTrue(row["primitive_word"])
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertTrue(
            section["aggregate"]["all_run_pair_counts_covered_symbolically"]
        )
        self.assertFalse(section["aggregate"]["arbitrary_valuation_words_covered"])

    def test_goldbach_liouville_projector_is_exact(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["exact_finite_rows"]:
            self.assertTrue(row["R_equals_C_minus_L_over_2"])
            self.assertTrue(row["S_equals_C_plus_L_over_2"])
            self.assertEqual(
                row["semiprime_only_saturation_L_equals_C"],
                row["prime_prime_R"] == 0,
            )
        self.assertTrue(
            section["aggregate"][
                "ticket200_next_lemma_is_goldbach_equivalent_given_chen_positivity"
            ]
        )
        self.assertFalse(section["aggregate"]["goldbach_resolved"])

    def test_twin_liouville_projector_is_exact(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["exact_finite_rows"]:
            self.assertTrue(row["T_equals_C2_minus_L2_over_2"])
            self.assertEqual(
                row["semiprime_only_saturation_L2_equals_C2"],
                row["twin_channel_T"] == 0,
            )
        self.assertTrue(
            section["aggregate"]["ticket200_next_lemma_is_twin_prime_equivalent"]
        )
        self.assertFalse(section["aggregate"]["twin_prime_resolved"])

    def test_attempts_have_one_open_lemma_and_zero_resolutions(self) -> None:
        attempts = ticket201.build_attempts(self.audit)
        self.assertEqual(len(attempts), 4)
        self.assertEqual(self.audit["machine_audit"]["conjecture_resolution_count"], 0)
        self.assertEqual(self.audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(
            self.audit["machine_audit"][
                "previous_next_lemmas_reclassified_as_equivalent_count"
            ],
            2,
        )
        for attempt in attempts:
            nodes = attempt["proof_dag"]["nodes"]
            self.assertEqual(
                sum(node["status"] == "highest_risk_open" for node in nodes),
                1,
            )
            self.assertEqual(attempt["status"], ticket201.STATUS)

    def test_generated_outputs_match_schema(self) -> None:
        ticket201.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket201-finite-information-allrun-liouville-parity.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket201.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        self.assertEqual(
            integrated["finite_information_allrun_liouville_parity_audit"][
                "machine_audit"
            ]["conjecture_resolution_count"],
            0,
        )


if __name__ == "__main__":
    unittest.main()
