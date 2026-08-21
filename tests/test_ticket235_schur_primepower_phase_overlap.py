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

import ticket235_schur_primepower_phase_overlap as ticket235  # noqa: E402


class Ticket235SchurPrimePowerPhaseOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket235.build_audit()
        cls.root = cls.audit[ticket235.AUDIT_KEY]

    def test_global_claim_guard(self) -> None:
        self.assertEqual(self.audit["schema"], ticket235.SCHEMA)
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

    def test_riemann_exact_schur_complement_and_relative_scale(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        rows = computation["exact_rank_one_schur_rows"]
        self.assertEqual([row["frequency_horizon_T"] for row in rows], [64, 256, 1024, 4096])
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        for row in rows:
            horizon = row["frequency_horizon_T"]
            self.assertEqual(
                Fraction(row["indefinite_schur_minimum"]["exact"]),
                Fraction(-3, horizon * horizon),
            )
            self.assertEqual(
                Fraction(row["safe_schur_minimum"]["exact"]),
                Fraction(3, 4 * horizon * horizon),
            )
        self.assertEqual(
            rows[0]["transcript_sha256"],
            "a91949fb4e3c34bf322ad30c3832cbd698f95559aa620649f460c2a69ab24ace",
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["exact_positive_schur_complement_criterion_proved"])
        self.assertFalse(aggregate["arithmetic_weil_tail_schur_domination_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_prime_power_and_primitive_divisor_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        counterexample = computation["general_prime_power_counterexample"]
        self.assertEqual(counterexample["lineage_ticket"], "CO-TICKET-224")
        self.assertEqual(counterexample["lineage_status"], "already_closed_regression_only")
        self.assertEqual(counterexample["valuation_word"], [1, 1, 2, 4, 3])
        self.assertEqual((counterexample["D"], counterexample["B"], counterexample["radical_D"]), (1805, 475, 95))
        self.assertTrue(counterexample["certificate_verified"])

        general = computation["general_valuation_finite_scan"]
        self.assertEqual(general["raw_canonical_positive_D_words"], 63_426)
        self.assertEqual(general["primitive_positive_D_necklaces"], 63_185)
        self.assertEqual(general["radical_false_positive_count"], 1)
        self.assertEqual(
            general["transcript_sha256"],
            "694279deac959d1b18b20b3518f5cccb5666fc6af53f5f4fc62b2a814b25cf2a",
        )

        primitive = computation["binary_primitive_divisor_scan"]
        self.assertEqual(primitive["characterization_failures"], 0)
        self.assertEqual(primitive["primitive_common_divisor_count"], 56)
        self.assertEqual(
            primitive["transcript_sha256"],
            "2d885beb2ec3218db36585e4473f7cffb5e9f7d16bad6d2237723292621a3f3f",
        )
        anchor = next(
            row
            for row in primitive["primitive_common_divisor_rows"]
            if row["one_count_k"] == 14 and row["prime_q"] == 29
        )
        self.assertEqual(
            (anchor["order_q_32_over_27"], anchor["order_q_3_over_2"], anchor["order_q_4"]),
            (14, 7, 14),
        )
        self.assertFalse(computation["aggregate"]["binary_adaptive_radical_deficit_refuted"])
        self.assertFalse(
            computation["aggregate"]["general_prime_presence_only_exclusion_new_in_ticket235"]
        )
        self.assertFalse(computation["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_complete_marginal_spectra_lose_cross_phase(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        rows = computation["exact_cyclic_group_rows"]
        self.assertEqual(len(rows), 24)
        self.assertEqual(rows[0]["prime_modulus_q"], 5)
        self.assertEqual(rows[-1]["prime_modulus_q"], 101)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(all(row["aligned_target_zero_convolution"] == 2 for row in rows))
        self.assertTrue(all(row["translated_target_zero_convolution"] == 0 for row in rows))
        self.assertEqual(
            computation["transcript_sha256"],
            "65e498b309d288abad9152f45503408ee5f91fb1d4d22416c1fd69859fc3740e",
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["complete_marginal_power_spectrum_sufficiency_refuted"])
        self.assertFalse(aggregate["actual_prime_reflected_phase_locking_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_overlap_reduction_and_degree_one_countermodel(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        rows = computation["degree_one_insufficiency_countermodel_rows"]
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            all(Fraction(row["degree_one_cesaro_E_m_1"]["exact"]) == 0 for row in rows)
        )
        self.assertTrue(
            all(Fraction(row["degree_two_cesaro_E_m_2"]["exact"]) == 1 for row in rows)
        )
        actual = computation["actual_twin_start_overlap_audit"]
        self.assertEqual(actual["twin_start_count"], 202)
        self.assertEqual(actual["active_primes"], [5, 7, 11, 13])
        self.assertTrue(all(actual["elementary_symmetric_identity_verified_by_degree"]))
        self.assertEqual(
            [row["exact"] for row in actual["fixed_degree_cesaro_energies"]],
            ["3257/1958592", "9265/5875776", "6301/3917184", "9/81608"],
        )
        for energy, elementary in zip(
            actual["fixed_degree_cesaro_energies"],
            actual["pair_overlap_elementary_moments"],
        ):
            self.assertEqual(Fraction(energy["exact"]), Fraction(elementary["exact"]))
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["fixed_degree_cesaro_overlap_identity_proved"])
        self.assertFalse(aggregate["actual_prime_overlap_moment_concentration_proved"])
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
        ticket235.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket235-schur-primepower-phase-overlap.json"
        integrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket235.SCHEMA)
        machine = integrated[ticket235.AUDIT_KEY]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
