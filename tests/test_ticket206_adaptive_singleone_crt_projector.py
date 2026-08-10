from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket206_adaptive_singleone_crt_projector as ticket206


class Ticket206AdaptiveSingleOneCRTProjectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket206.build_audit()

    def test_adaptive_winding_termination_and_clearance_complexity(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        self.assertTrue(section["termination_certificate"]["uniform_bisection_terminates"])
        rows = section["clearance_complexity_rows"]
        self.assertEqual(rows[1]["epsilon"], "1/16")
        self.assertEqual(rows[1]["uniform_global_criterion_fails_for_every_N_at_most"], 96)
        self.assertEqual(rows[1]["uniform_global_criterion_certified_at_N"], 128)
        self.assertTrue(section["aggregate"]["fixed_uniform_segment_budget_refuted"])
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_single_one_collatz_stratum_is_excluded(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        regression = section["finite_integrality_regression"]
        expected = sum(length * 4 ** (length - 1) for length in range(1, 9))
        self.assertEqual(regression["total_words_checked"], expected)
        self.assertEqual(regression["positive_integral_cycle_words"], 0)
        self.assertEqual(section["length_cases"]["h_eq_3"]["trajectory_prefix"], [3, 5, 1])
        self.assertEqual(
            section["aggregate"]["minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"],
            2,
        )
        self.assertFalse(section["aggregate"]["two_or_more_one_mixed_necklaces_excluded"])

    def test_goldbach_crt_progressions_exclude_every_bounded_witness(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["crt_fixture_rows"]:
            self.assertTrue(row["all_N_equals_N0_plus_tM_are_even"])
            self.assertTrue(row["p_equals_2_complement_is_composite"])
            self.assertTrue(row["all_prime_witnesses_at_most_B_excluded"])
            self.assertTrue(all(item["proper_composite_complement"] for item in row["forcing_rows"]))
        self.assertTrue(section["aggregate"]["fixed_bounded_prime_witness_basis_refuted"])
        self.assertFalse(section["aggregate"]["goldbach_counterexample_found"])

    def test_binomial_omega_projector_and_truncation_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for omega in range(0, 20):
            self.assertEqual(ticket206.omega_binomial_projector(omega, max(1, omega)), int(omega == 1))
        for row in section["crt_false_positive_rows"]:
            self.assertTrue(row["n0_divisible_by_left_product"])
            self.assertTrue(row["n0_plus_2_divisible_by_right_product"])
            self.assertGreater(row["Omega_n_lower_bound"], row["truncation_R"])
            self.assertTrue(row["truncated_shift_two_product_positive"])
        self.assertFalse(section["aggregate"]["uniform_infinite_tail_cancellation_proved"])
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            self.assertTrue(self.audit[key]["claim_boundary"].startswith("No "))
            self.assertEqual(self.audit[key]["proof_dag"]["nodes"][-1]["status"], "open_not_proven")

    def test_written_outputs_match_attempt_contract(self) -> None:
        ticket206.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket206-adaptive-singleone-crt-projector.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], ticket206.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
