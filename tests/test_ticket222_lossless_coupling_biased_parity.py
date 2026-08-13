from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket222_lossless_coupling_biased_parity as ticket222  # noqa: E402


class Ticket222LosslessCouplingBiasedParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket222.build_audit()
        cls.root = cls.audit["lossless_coupling_biased_parity_audit"]

    def test_global_claim_boundary_is_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket222.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_compact_profile_contract(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["compact_full_dyadic_profile_injectivity_proved"])
        self.assertTrue(aggregate["finite_example_profiles_differ_somewhere"])
        self.assertFalse(aggregate["finite_window_injectivity_claimed"])
        self.assertFalse(aggregate["unbounded_actual_zeta_defect_support_controlled"])
        self.assertTrue(
            all(
                row["telescoping_identity_verified"]
                for row in section["finite_telescoping_rows"]
            )
        )

    def test_collatz_slope_intercept_code_is_lossless(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["total_words_checked"], sum(5**h for h in range(1, 9)))
        self.assertEqual(aggregate["total_code_collisions"], 0)
        self.assertEqual(aggregate["total_decode_failures"], 0)
        self.assertTrue(aggregate["slope_intercept_code_injectivity_proved"])
        self.assertTrue(aggregate["exact_cycle_divisibility_reduction_proved"])
        for row in section["sample_lossless_decode_rows"]:
            self.assertTrue(row["decode_matches"])
            if row["D_divides_B"]:
                self.assertTrue(row["exact_cycle_replay"])

    def test_goldbach_parity_is_diagonal_only(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        finite = section["finite_exact_scan"]
        self.assertEqual(finite["parity_identity_failures"], 0)
        self.assertEqual(finite["zero_representation_count"], 0)
        self.assertGreater(finite["positive_even_parity_count"], 0)
        witness = next(
            row
            for row in finite["parity_zero_positive_examples"]
            if row["even_target_N"] == 20
        )
        self.assertEqual(witness["ordered_odd_prime_representation_count"], 4)
        self.assertEqual(witness["parity_bit"], 0)

    def test_twin_biased_parity_formula(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["crt_product_independence_proved"])
        self.assertTrue(aggregate["biased_parity_leakage_formula_proved"])
        self.assertFalse(aggregate["balanced_orthogonality_applies_to_actual_finite_wheel"])
        self.assertTrue(aggregate["proper_uncentered_correlations_all_nonzero"])
        rows = section["exact_crt_enumeration"]["subset_rows"]
        self.assertEqual(len(rows), 16)
        self.assertTrue(all(row["identity_verified"] for row in rows))

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket222.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket222-lossless-coupling-biased-parity.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket222.SCHEMA)
        self.assertEqual(
            integrated["lossless_coupling_biased_parity_audit"]["machine_audit"][
                "total_failure_count"
            ],
            0,
        )


if __name__ == "__main__":
    unittest.main()
