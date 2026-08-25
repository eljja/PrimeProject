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

import ticket239_cancellation_lifting_fourier_crt as ticket239  # noqa: E402


class Ticket239CancellationLiftingFourierCRTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket239.build_audit()
        cls.root = cls.audit[ticket239.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket239.SCHEMA)
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

    def test_riemann_power_decay_and_nonsummable_positive_family(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        summable = computation["exact_summable_power_decay_rows"]
        nonsummable = computation["exact_nonsummable_positive_mixture_rows"]
        self.assertEqual([row["shell_count_J"] for row in summable], [4, 8, 16, 32, 64])
        self.assertTrue(all(row["certificate_verified"] for row in summable))
        self.assertTrue(all(row["certificate_verified"] for row in nonsummable))
        self.assertTrue(any(not row["absolute_row_sum_certificate_passes"] for row in nonsummable))
        self.assertTrue(computation["aggregate"]["absolute_row_sum_necessity_refuted"])
        self.assertFalse(computation["aggregate"]["arithmetic_weil_cancellation_bound_proved"])

    def test_collatz_local_lifting_dichotomy_and_bounded_scan(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        scan = computation["bounded_exception_scan"]
        self.assertEqual(scan["prime_limit"], 200_000)
        self.assertGreater(scan["odd_primes_scanned"], 17_000)
        self.assertEqual(scan["positive_lifting_defect_count"], 0)
        self.assertEqual(scan["valuation_cap_censored_count"], 0)
        self.assertTrue(all(row["all_palette_valuation_witnesses_disabled"] for row in computation["exact_palette_rows"]))
        self.assertTrue(computation["aggregate"]["local_lifting_defect_dichotomy_proved"])
        self.assertFalse(computation["aggregate"]["all_odd_prime_lifting_defects_nonpositive_proved"])

    def test_goldbach_reflection_identity_and_l2_no_go(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["exact_mesoscopic_prime_window_rows"]
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(all(row["same_size_initial_segment_has_zero_reflection"] for row in rows))
        for row in rows:
            dc = Fraction(row["dc_phase_term_m_squared_over_M"]["exact"])
            signed = Fraction(row["signed_nonzero_phase_term"]["exact"])
            self.assertEqual(dc + signed, row["ordered_reflection_count_R_A_h"])
        self.assertTrue(computation["aggregate"]["cardinality_and_parseval_sufficiency_refuted"])
        self.assertFalse(computation["aggregate"]["prime_window_signed_phase_slack_proved"])

    def test_twin_uniform_crt_identity_and_composite_progressions(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        rows = computation["exact_uniform_crt_rows"]
        self.assertEqual([row["coordinate_count_m"] for row in rows], [2, 3, 4, 5, 6])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            self.assertEqual(row["uniform_crt_effective_rank"], row["coordinate_count_m"])
            left, right = row["constructed_composite_pair"]
            factor_left, factor_right = row["outside_composite_factors"]
            self.assertEqual(left % factor_left, 0)
            self.assertEqual(right % factor_right, 0)
        self.assertTrue(computation["aggregate"]["local_effective_rank_sufficiency_refuted"])
        self.assertFalse(computation["aggregate"]["prime_weighted_parity_sensitive_transfer_proved"])

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
        ticket239.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket239-cancellation-lifting-fourier-crt.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket239.SCHEMA)
        machine = integrated[ticket239.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
