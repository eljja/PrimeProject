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

import ticket200_derivative_mesh_three_run_chen_channels as ticket200


class Ticket200DerivativeMeshThreeRunChenChannelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket200.build_audit()

    def test_derivative_mesh_bridge_has_exact_threshold(self) -> None:
        coarse = ticket200.rh_derivative_mesh_row(2)
        first = ticket200.rh_derivative_mesh_row(4)
        self.assertFalse(coarse["strict_rouche_margin_certified"])
        self.assertTrue(first["strict_rouche_margin_certified"])
        self.assertEqual(
            first["propagated_strict_clearance_eta_minus_Lh_over_2"],
            "7/4",
        )
        self.assertEqual(
            self.audit["riemann"]["reproducible_computation"]["failure_count"],
            0,
        )
        self.assertFalse(
            self.audit["riemann"]["reproducible_computation"]["aggregate"][
                "actual_Xi_interval_certificate_constructed"
            ]
        )

    def test_three_run_closed_form_and_residual_interval(self) -> None:
        self.assertEqual(ticket200.ordered_affine_numerator((1, 2, 2, 1, 2, 2)), 1357)
        for scale in range(2, 7):
            row = ticket200.collatz_three_run_row(scale)
            self.assertNotEqual(row["finite_base_residue_B_mod_D"], "0")
            self.assertFalse(row["affine_divisibility_hit"])
        for scale in (7, 8, 16, 64, 128):
            row = ticket200.collatz_three_run_row(scale)
            self.assertTrue(row["zero_less_than_B_minus_2D_less_than_D"])
            self.assertFalse(row["affine_divisibility_hit"])
            self.assertEqual(row["cyclic_rotation_divisibility_hit_count"], 0)
            self.assertTrue(row["primitive_word"])

    def test_semiprime_support_is_exact_on_boundary_examples(self) -> None:
        primes = ticket200.prime_sieve(64)
        prime_values = [value for value in range(2, 65) if primes[value]]
        semiprimes = ticket200.semiprime_sieve(64, prime_values)
        for value in (4, 6, 9, 10, 14, 15, 21, 25, 49):
            self.assertTrue(semiprimes[value], value)
        for value in (1, 2, 5, 8, 12, 16, 18, 27):
            self.assertFalse(semiprimes[value], value)

    def test_goldbach_chen_channels_do_not_overclaim(self) -> None:
        section = self.audit["goldbach"]
        computation = section["reproducible_computation"]
        self.assertEqual(computation["failure_count"], 0)
        self.assertEqual(computation["logical_countermodel"], {
            "R": 0,
            "S": 1,
            "C": 1,
            "meaning": "C>0 and C=R+S do not logically imply R>0.",
            "is_an_arithmetic_goldbach_counterexample": False,
        })
        self.assertFalse(computation["aggregate"]["goldbach_resolved"])
        self.assertFalse(
            computation["aggregate"][
                "semiprime_only_channel_eliminated_above_threshold"
            ]
        )

    def test_twin_chen_channels_do_not_cross_parity_barrier(self) -> None:
        section = self.audit["twin_prime"]
        computation = section["reproducible_computation"]
        self.assertEqual(computation["failure_count"], 0)
        self.assertTrue(
            computation["aggregate"][
                "imported_infinitely_many_chen_positive_blocks"
            ]
        )
        self.assertFalse(
            computation["aggregate"][
                "infinitely_many_twin_positive_blocks_proved"
            ]
        )
        self.assertFalse(computation["logical_countermodel"]["is_a_twin_prime_counterexample"])

    def test_attempts_have_one_open_lemma_and_zero_resolutions(self) -> None:
        attempts = ticket200.build_attempts(self.audit)
        self.assertEqual(len(attempts), 4)
        self.assertEqual(
            self.audit["machine_audit"]["conjecture_resolution_count"], 0
        )
        self.assertEqual(self.audit["machine_audit"]["total_failure_count"], 0)
        for attempt in attempts:
            nodes = attempt["proof_dag"]["nodes"]
            self.assertEqual(
                sum(node["status"] == "highest_risk_open" for node in nodes),
                1,
            )
            self.assertEqual(attempt["status"], ticket200.STATUS)

    def test_generated_outputs_match_schema(self) -> None:
        ticket200.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket200-derivative-mesh-three-run-chen-channels.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket200.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        self.assertEqual(
            integrated["derivative_mesh_three_run_chen_channel_audit"][
                "machine_audit"
            ]["conjecture_resolution_count"],
            0,
        )


if __name__ == "__main__":
    unittest.main()
