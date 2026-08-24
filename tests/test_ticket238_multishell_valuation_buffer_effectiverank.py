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

import ticket238_multishell_valuation_buffer_effectiverank as ticket238  # noqa: E402


class Ticket238MultishellValuationBufferEffectiveRankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket238.build_audit()
        cls.root = cls.audit[ticket238.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket238.SCHEMA)
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

    def test_riemann_multishell_row_sum_and_pairwise_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        rows = computation["exact_multishell_rows"]
        self.assertEqual([row["shell_count_J"] for row in rows], list(range(2, 9)))
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertEqual(
            Fraction(rows[2]["adverse_global_constant_mode_eigenvalue"]["exact"]),
            0,
        )
        self.assertTrue(rows[2]["adverse_global_block_is_joint_gram_realizable"])
        self.assertTrue(rows[2]["joint_gram_strict_positivity_counterexample"])
        self.assertFalse(rows[3]["adverse_global_block_is_joint_gram_realizable"])
        self.assertLess(
            Fraction(rows[3]["adverse_global_constant_mode_eigenvalue"]["exact"]),
            0,
        )
        self.assertTrue(
            computation["aggregate"]["pairwise_principal_angle_sufficiency_refuted"]
        )
        self.assertFalse(
            computation["aggregate"]["arithmetic_weil_multishell_row_sum_proved"]
        )

    def test_collatz_valuation_equivalence_and_run_block_rows(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        rows = computation["exact_run_block_valuation_rows"]
        self.assertEqual([row["one_count_k"] for row in rows], list(range(1, 21)))
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(all(row["v_q_D_k"] > row["v_q_B_k"] for row in rows))
        self.assertTrue(
            computation["aggregate"][
                "all_run_blocks_have_adaptive_valuation_witness_proved"
            ]
        )
        self.assertFalse(
            computation["aggregate"][
                "valuation_witness_escapes_every_finite_palette_proved"
            ]
        )

    def test_goldbach_mesoscopic_buffer_ceiling(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["exact_buffer_rows"]
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertLessEqual(
                row["ordered_prime_representation_count_g_X_N"],
                row["geometric_representation_ceiling_h_plus_1"],
            )
        self.assertTrue(
            computation["aggregate"][
                "sub_x_over_log_squared_inverse_log_margin_refuted"
            ]
        )
        self.assertFalse(
            computation["aggregate"]["mesoscopic_buffered_prime_phase_gain_proved"]
        )

    def test_twin_effective_rank_equivalence_and_support_no_go(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        rows = computation["exact_fixed_effective_rank_rows"]
        self.assertEqual(
            [row["coordinate_count_m"] for row in rows], [4, 8, 16, 32, 64]
        )
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            all(Fraction(row["gram_effective_rank"]["exact"]) == 2 for row in rows)
        )
        self.assertTrue(computation["aggregate"]["support_growth_sufficiency_refuted"])
        self.assertFalse(
            computation["aggregate"]["prime_weighted_effective_rank_divergence_proved"]
        )

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
        ticket238.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket238-multishell-valuation-buffer-effectiverank.json"
        )
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket238.SCHEMA)
        machine = integrated[ticket238.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
