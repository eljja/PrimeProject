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

import ticket207_dihedral_twoone_logwitness_abel as ticket207


class Ticket207DihedralTwoOneLogWitnessAbelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket207.build_audit()

    def test_completed_xi_boundary_reduction_and_symmetry_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        self.assertEqual(section["off_critical_line_zeros"], ["1/6", "5/6"])
        for row in section["boundary_reconstruction_rows"]:
            self.assertTrue(row["bottom_reconstructed_by_conjugation"])
            self.assertTrue(row["right_lower_reconstructed_by_conjugation"])
            self.assertTrue(row["left_reconstructed_by_reflection"])
            self.assertEqual(
                row["sampled_clearance_squared_full"],
                row["sampled_clearance_squared_fundamental"],
            )
            self.assertEqual(
                row["sampled_derivative_squared_full"],
                row["sampled_derivative_squared_fundamental"],
            )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["symmetry_only_implication_of_rh_refuted"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_exactly_two_valuation_one_collatz_cycles_are_excluded(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(
            Fraction(section["long_case_bounds"][0]["minimum_upper_bound"]),
            Fraction(26485, 9823),
        )
        self.assertLess(Fraction(26485, 9823), 3)
        for rows in section["finite_replay_cases"].values():
            for row in rows:
                self.assertFalse(
                    row["returns_to_start"] and row["exactly_two_valuation_ones"]
                )
        self.assertTrue(all(row["excluded"] for row in section["short_symbolic_cases"]))
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            3,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_logarithmic_goldbach_witness_crt_certificates(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["crt_logarithmic_fixture_rows"]:
            target = int(row["canonical_even_target_N"])
            modulus = int(row["modulus_M"])
            self.assertLess(modulus, target)
            self.assertLess(target, 2 * modulus)
            self.assertEqual(target % 2, 0)
            self.assertLessEqual(target.bit_length(), 3 * row["witness_bound_B"])
            for forcing in row["forcing_rows"]:
                complement = target - forcing["excluded_witness_prime"]
                self.assertGreater(complement, forcing["forcing_divisor"])
                self.assertEqual(complement % forcing["forcing_divisor"], 0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["universal_sublogarithmic_witness_basis_refuted"])
        self.assertFalse(aggregate["goldbach_counterexample_found"])

    def test_abel_projector_identity_and_exact_finite_reconstruction(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for denominator in (4, 8, 16):
            scale = Fraction(denominator - 1, denominator)
            self.assertEqual(ticket207.abel_omega_projector(1, scale), 1)
            for omega in range(2, 50):
                value = ticket207.abel_omega_projector(omega, scale)
                self.assertGreater(value, 0)
        for x_value in (1, 2, 8, 64):
            scale = Fraction(16 * x_value - 1, 16 * x_value)
            for omega in range(2, 30):
                self.assertLessEqual(
                    ticket207.abel_omega_projector(omega, scale),
                    Fraction(1, 8 * x_value),
                )
        for row in section["finite_reconstruction_rows"]:
            weighted = Fraction(row["abel_sum_S_X"])
            self.assertEqual(
                weighted.numerator // weighted.denominator,
                row["exact_twin_count_T_X"],
            )
            self.assertLessEqual(Fraction(row["positive_composite_leakage"]), Fraction(1, 8))
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_keeps_all_four_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.audit[key]
            self.assertTrue(section["claim_boundary"].startswith("No "))
            self.assertEqual(section["proof_dag"]["nodes"][-1]["status"], "open_not_proven")

    def test_written_outputs_match_attempt_contract(self) -> None:
        ticket207.write_outputs(self.audit)
        path = ROOT / "data/open-problem/ticket207-dihedral-twoone-logwitness-abel.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], ticket207.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
