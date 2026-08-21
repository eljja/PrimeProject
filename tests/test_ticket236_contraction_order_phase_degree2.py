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

import ticket236_contraction_order_phase_degree2 as ticket236  # noqa: E402


class Ticket236ContractionOrderPhaseDegreeTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket236.build_audit()
        cls.root = cls.audit[ticket236.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket236.SCHEMA)
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

    def test_riemann_global_contraction_and_local_minor_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        rows = computation["exact_coherent_rank_one_rows"]
        self.assertEqual([row["block_dimension_m"] for row in rows], [4, 8, 16, 32, 64, 128])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            dimension = row["block_dimension_m"]
            self.assertEqual(Fraction(row["unsafe_cross_entry_2_over_m"]["exact"]), Fraction(2, dimension))
            self.assertGreaterEqual(Fraction(row["every_coordinate_two_by_two_minor"]["exact"]), 0)
            self.assertEqual(Fraction(row["unsafe_normalized_operator_norm"]["exact"]), 2)
            self.assertEqual(Fraction(row["unsafe_full_block_minimum_eigenvalue"]["exact"]), -1)
            self.assertEqual(Fraction(row["safe_full_block_minimum_eigenvalue"]["exact"]), Fraction(1, 2))
        self.assertEqual(
            computation["transcript_sha256"],
            "8c6817245d62ebd56cd2bb1ebdc09c556f14ded2b8084a777f177ba27811b2c3",
        )
        self.assertTrue(computation["aggregate"]["normalized_cross_block_contraction_iff_proved"])
        self.assertFalse(computation["aggregate"]["arithmetic_weil_normalized_contraction_proved"])
        self.assertFalse(computation["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_three_prime_order_witness(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        orders = {
            row["prime_q"]: (
                row["order_q_32_over_27"],
                row["order_q_3_over_2"],
                row["order_q_4"],
            )
            for row in computation["witness_order_rows"]
        }
        self.assertEqual(orders, {5: (1, 2, 2), 59: (2, 58, 29), 57653: (29, 28826, 28826)})
        period = computation["complete_residue_period_audit"]
        self.assertEqual(period["period"], 28826)
        self.assertEqual(
            period["coverage_counts"],
            {"q_5": 14413, "q_59": 13916, "q_57653": 496, "uncovered": 1},
        )
        self.assertEqual(period["residue_failure_count"], 0)
        self.assertEqual(
            period["transcript_sha256"],
            "9b23e815a83ae737cc71af674f66b2e4c44954a72b188862c7c429e18d08b197",
        )
        exception = period["anchor_rows"][-1]
        self.assertEqual(exception["one_count_k"], 28826)
        self.assertIsNone(exception["selected_prime_q"])
        self.assertTrue(exception["all_three_common_at_exception"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["run_block_order_separated_witness_outside_28826_multiples_proved"])
        self.assertFalse(aggregate["run_block_nondivisibility_newly_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_phase_defect_identity_and_margin_no_go(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["exact_actual_prime_rows"]
        self.assertEqual(
            [(row["cutoff_X"], row["prime_count_pi_X"]) for row in rows],
            [(100, 25), (1000, 168), (10000, 1229), (100000, 9592)],
        )
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertEqual(row["ordered_representation_count_g_X_4"], 1)
            self.assertEqual(
                Fraction(row["normalized_phase_margin_g_over_pi"]["exact"]),
                Fraction(1, row["prime_count_pi_X"]),
            )
            self.assertEqual(
                row["total_spectral_power_M_X"] - row["reflected_phase_defect_Delta_X_4"],
                row["prime_modulus_q"],
            )
        self.assertEqual(
            computation["transcript_sha256"],
            "d075449ac3bca0bbf0a4edff052588b95a7a38047d7b245dbb2bf02ac4f4cffc",
        )
        self.assertTrue(all(row["certificate_verified"] for row in computation["direct_complex_dft_rows"]))
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["uncoupled_inverse_log_uniform_margin_refuted"])
        self.assertFalse(aggregate["target_coupled_prime_phase_gain_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_degree_two_controls_all_fixed_degrees(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        rows = computation["actual_twin_start_diagnostic_rows"]
        self.assertEqual(
            [(row["cutoff_X"], row["active_prime_count_m"], row["twin_start_count"]) for row in rows],
            [(10000, 4, 202), (100000, 6, 1220), (1000000, 8, 8164)],
        )
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertTrue(row["degree_one_from_degree_two_squared_bound_verified"])
            self.assertTrue(all(bound["bound_verified"] for bound in row["higher_degree_bound_rows"]))
        self.assertEqual(
            [value["exact"] for value in rows[0]["fixed_degree_cesaro_energies"]],
            ["3257/1958592", "9265/5875776", "6301/3917184", "9/81608"],
        )
        self.assertEqual(
            computation["transcript_sha256"],
            "c1ba12041bd9e671f97ab24ac2534baab627f2e177502c20a375455450035c98",
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["degree_two_controls_every_fixed_degree_proved"])
        self.assertFalse(aggregate["actual_prime_degree_two_decay_proved"])
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
        ticket236.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket236-contraction-order-phase-degree2.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket236.SCHEMA)
        machine = integrated[ticket236.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
