from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket199_symmetric_sampling_two_run_squarefree_filter as ticket199


class Ticket199SymmetricSamplingTwoRunSquarefreeFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket199.build_audit()

    def test_machine_boundary(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_countermodels_are_exact(self) -> None:
        rh = self.audit["riemann"]["reproducible_computation"]
        self.assertTrue(rh["aggregate"]["all_countermodels_exact"])
        self.assertFalse(rh["aggregate"]["actual_Xi_zero_exhibited"])
        for row in rh["exact_rational_rows"]:
            self.assertTrue(row["all_boundary_samples_match_F_equals_one"])
            self.assertTrue(row["constructed_off_real_zero_exact"])
            self.assertTrue(row["Q_at_a_nonzero"])

    def test_gaussian_interpolation_basis(self) -> None:
        row = ticket199.rh_sampling_row(4)
        self.assertEqual(row["a_squared"], {"real": "0", "imag": "2"})
        self.assertEqual(row["constructed_G_at_a"], {"real": "0", "imag": "0"})

    def test_collatz_closed_form_and_residual_interval(self) -> None:
        for scale in [2, 3, 4, 5, 8, 32, 128]:
            row = ticket199.collatz_two_run_row(scale)
            self.assertTrue(row["direct_numerator_matches_closed_form"])
            self.assertTrue(row["B_congruent_to_2R_mod_D"])
            self.assertFalse(row["affine_divisibility_hit"])
            self.assertEqual(row["cyclic_rotation_divisibility_hit_count"], 0)
            self.assertTrue(row["rotation_recurrence_holds_exactly"])
            self.assertTrue(row["rotation_cycle_closes"])
            if scale >= 5:
                self.assertTrue(row["D_less_than_R_less_than_2D"])

    def test_collatz_base_residues_are_nonzero(self) -> None:
        collatz = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(
            collatz["base_case_residues"],
            {"2": "7066", "3": "151754", "4": "1746214"},
        )
        self.assertTrue(collatz["aggregate"]["all_scales_k_ge_2_excluded"])
        self.assertFalse(collatz["aggregate"]["all_fixed_run_counts_resolved"])

    def test_squarefree_lambda_projector_small_values(self) -> None:
        primes = ticket199.prime_sieve(128)
        squarefree = ticket199.squarefree_sieve(128, primes)
        mangoldt = ticket199.von_mangoldt_support_sieve(128, primes)
        filtered = [
            value
            for value in range(2, 129)
            if squarefree[value] and mangoldt[value]
        ]
        expected = [value for value in range(2, 129) if primes[value]]
        self.assertEqual(filtered, expected)
        for proper_power in [4, 8, 9, 16, 25, 27, 32, 49, 64, 81, 121, 125]:
            self.assertFalse(squarefree[proper_power] and mangoldt[proper_power])

    def test_goldbach_filter_removes_collision_support(self) -> None:
        goldbach = self.audit["goldbach"]["reproducible_computation"]
        self.assertTrue(
            goldbach["aggregate"]["prime_power_collision_removed_algebraically"]
        )
        self.assertEqual(
            goldbach["aggregate"]["finite_collision_target_failure_count"], 0
        )
        self.assertFalse(
            goldbach["aggregate"]["eventual_positive_lower_bound_proved"]
        )
        self.assertEqual(
            goldbach["projector_audit"]["proper_prime_power_leakage_count"], 0
        )

    def test_twin_detector_matches_exact_pair_support(self) -> None:
        twin = self.audit["twin_prime"]["reproducible_computation"]
        self.assertTrue(twin["aggregate"]["all_finite_supports_match"])
        self.assertTrue(twin["aggregate"]["prime_power_free_detector_constructed"])
        self.assertFalse(
            twin["aggregate"]["infinitely_many_positive_blocks_proved"]
        )
        self.assertTrue(
            all(row["exact_support_match"] for row in twin["finite_dyadic_rows"])
        )

    def test_all_next_lemmas_remain_open(self) -> None:
        attempts = ticket199.build_attempts(self.audit)
        self.assertEqual(len(attempts), 4)
        self.assertTrue(all(row["status"] == "open_not_proven" for row in attempts))
        self.assertTrue(
            all(
                any(
                    node["status"] == "highest_risk_open"
                    for node in row["proof_dag"]["nodes"]
                )
                for row in attempts
            )
        )

    def test_written_artifacts_match_build(self) -> None:
        ticket199.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket199-symmetric-sampling-two-run-squarefree-filter.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket199.SCHEMA)
        self.assertEqual(len(integrated["attempts"]), 4)
        self.assertEqual(
            integrated["symmetric_sampling_two_run_squarefree_filter_audit"][
                "machine_audit"
            ],
            self.audit["machine_audit"],
        )


if __name__ == "__main__":
    unittest.main()
