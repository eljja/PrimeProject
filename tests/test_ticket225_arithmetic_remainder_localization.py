from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket225_arithmetic_remainder_localization as ticket225  # noqa: E402


class Ticket225ArithmeticRemainderLocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket225.build_audit()
        cls.root = cls.audit["arithmetic_remainder_localization_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket225.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_actual_prime_band_and_finite_family_no_go(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["actual_prime_band_rows"]
        kernels = section["finite_band_kernel_rows"]
        self.assertEqual(len(rows), 13)
        self.assertTrue(all(row["negative_sign_certified"] for row in rows))
        for row in rows:
            lower, upper = row["certified_full_band_interval"]
            self.assertLessEqual(lower, upper)
            self.assertGreater(row["von_mangoldt_tail_upper_bound"], 0.0)
            self.assertLess(upper, 0.0)
        self.assertEqual(len(kernels), 6)
        self.assertTrue(
            all(row["nonzero_signed_atomic_kernel_verified"] for row in kernels)
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["actual_von_mangoldt_band_tail_bound_proved"])
        self.assertFalse(aggregate["explicit_formula_transfer_to_weil_positivity_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_cyclic_gcd_invariance_and_rotation_no_go(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        rows = section["finite_height_rows"]
        witness = section["ticket224_witness_rotation_rows"]
        self.assertEqual(sum(row["positive_primitive_words"] for row in rows), 97016)
        self.assertTrue(
            all(row["cyclic_gcd_invariance_failures"] == 0 for row in rows)
        )
        self.assertTrue(
            all(row["cyclic_transition_identity_failures"] == 0 for row in rows)
        )
        self.assertEqual({row["gcd_D_B"] for row in witness}, {95})
        self.assertEqual({row["residual_D_over_gcd"] for row in witness}, {19})
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["cyclic_transition_checks"], 655188)
        self.assertEqual(aggregate["nontrivial_cycles_found"], 0)
        self.assertFalse(aggregate["all_nontrivial_cycles_excluded"])
        self.assertFalse(aggregate["aperiodic_descent_proved"])

    def test_cyclic_transition_identity_directly(self) -> None:
        for word in ((1, 2, 3), (1, 1, 2, 4, 3), (2, 5, 1, 3)):
            denominator = 2 ** sum(word) - 3 ** len(word)
            rotated = ticket225.rotations(word)
            for index, local in enumerate(rotated):
                following = rotated[(index + 1) % len(word)]
                self.assertEqual(
                    (2 ** local[0]) * ticket225.collatz_intercept(following),
                    3 * ticket225.collatz_intercept(local) + denominator,
                )

    def test_goldbach_cube_root_semiprime_decomposition(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["classification_mismatches"] == 0
                and row["rough_semiprime_factorization_failures"] == 0
                for row in section["cube_root_classification_rows"]
            )
        )
        for row in section["convolution_decomposition_rows"]:
            self.assertTrue(row["exact_decomposition_verified"])
            self.assertEqual(
                row["filtered_convolution"],
                row["prime_prime_PP"]
                + row["prime_semiprime_PS"]
                + row["semiprime_prime_SP"]
                + row["semiprime_semiprime_SS"],
            )
        self.assertTrue(
            all(row["SS_diagonal_present"] for row in section["rough_semiprime_false_diagonal_rows"])
        )
        self.assertFalse(
            section["aggregate"]["rough_semiprime_contamination_uniformly_controlled"]
        )

    def test_twin_cube_root_pair_type_decomposition(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        for row in section["pair_type_rows"]:
            self.assertTrue(row["exact_pair_decomposition_verified"])
            self.assertGreater(row["semiprime_semiprime_SS"], 0)
            self.assertGreater(row["contaminating_pairs"], 0)
        for row in section["explicit_SS_countermodels"]:
            self.assertTrue(row["verified"])
            left, right = row["composite_pair"]
            self.assertEqual(right - left, 2)
            self.assertFalse(ticket225.is_prime(left))
            self.assertFalse(ticket225.is_prime(right))
        self.assertFalse(
            section["aggregate"]["rough_semiprime_pair_contamination_uniformly_controlled"]
        )
        self.assertFalse(section["aggregate"]["infinitely_many_twin_primes_proved"])

    def test_cube_root_survivors_are_prime_or_rough_semiprime(self) -> None:
        for horizon in (500, 5000):
            cutoff, _, labels, sieve = ticket225.cube_root_labels(horizon)
            self.assertGreaterEqual(cutoff**3, horizon)
            for value in range(2, horizon + 1):
                if labels[value] == "rough_semiprime":
                    factors = ticket225.factor_integer(value)
                    self.assertFalse(bool(sieve[value]))
                    self.assertEqual(sum(factors.values()), 2)
                    self.assertGreater(min(factors), cutoff)

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket225.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket225-arithmetic-remainder-localization.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket225.SCHEMA)
        machine = integrated["arithmetic_remainder_localization_audit"][
            "machine_audit"
        ]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
