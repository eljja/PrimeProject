from __future__ import annotations

import json
import sys
import unittest

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket185_spectral_cycle_factor_granularity import (  # noqa: E402
    build_audit,
    goldbach_factor_horizon_row,
    neutral_autocorrelation_escape_row,
    prime_sieve,
    single_one_cycle_row,
    smallest_prime_factors,
)


class Ticket185SpectralCycleFactorGranularityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_neutral_projection_constraints_hold(self) -> None:
        row = neutral_autocorrelation_escape_row(32)
        self.assertTrue(row["checks"]["two_neutral_constraints_hold"])
        self.assertLess(
            max(abs(value) for value in row["neutral_moment_residuals"]),
            1e-12,
        )
        self.assertEqual(row["normalized_autocorrelation_value_at_zero"], 1.0)

    def test_low_frequency_mass_escapes_monotonically(self) -> None:
        rows = self.riemann["spectral_escape_rows"]
        masses = [row["normalized_low_band_spectral_mass"] for row in rows]
        self.assertTrue(all(masses[index + 1] < masses[index] for index in range(3)))
        self.assertLess(masses[-1], 0.01)
        self.assertEqual(self.riemann["failure_count"], 0)

    def test_single_one_cycle_closed_forms(self) -> None:
        row = single_one_cycle_row(8)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(int(row["affine_numerator_B"]) - int(row["cycle_denominator_D"]), 2 * 3**7)
        self.assertEqual(row["gcd_B_D"], 1)

    def test_single_one_infinite_family_has_no_divisibility_hits(self) -> None:
        rows = self.collatz["single_one_cycle_rows"]
        self.assertTrue(all(row["checks"]["affine_divisibility_fails"] for row in rows))
        self.assertEqual(self.collatz["aggregate"]["divisibility_hits"], 0)
        self.assertTrue(self.collatz["aggregate"]["infinite_family_proved"])

    def test_collatz_route_restores_strict_partial_target(self) -> None:
        section = self.audit["collatz"]
        self.assertIn("equivalent", section["route_decision"]["discard"])
        self.assertIn("ExactlyTwoOnes", section["route_decision"]["next_single_lemma"])

    def test_goldbach_factor_horizon_is_exact(self) -> None:
        primality = prime_sieve(1_000)
        least_factor = smallest_prime_factors(1_000)
        row = goldbach_factor_horizon_row(1_000, primality, least_factor)
        self.assertGreater(row["bad_survivors_before_horizon"], 0)
        self.assertEqual(row["bad_survivors_at_horizon"], 0)
        self.assertTrue(all(row["checks"].values()))

    def test_goldbach_empty_bad_pair_boundary_has_zero_horizon(self) -> None:
        primality = prime_sieve(10)
        least_factor = smallest_prime_factors(10)
        for target in [6, 8, 10]:
            row = goldbach_factor_horizon_row(target, primality, least_factor)
            self.assertEqual(row["exact_bad_pair_factor_horizon_tau_N"], 0)
            self.assertEqual(row["last_bad_survivor_witness"], [])
            self.assertEqual(row["bad_survivors_at_horizon"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_finite_targets_keep_prime_support_separate(self) -> None:
        rows = self.goldbach["target_factor_horizon_rows"]
        self.assertEqual([row["even_target_N"] for row in rows], [100, 500, 1_000, 5_000, 10_000, 50_000])
        self.assertTrue(all(row["bad_survivors_at_horizon"] == 0 for row in rows))
        self.assertTrue(all(row["unordered_prime_representation_count"] > 0 for row in rows))

    def test_twin_one_sided_certificate_equals_positive_count(self) -> None:
        rows = self.twin["finite_prime_pair_block_rows"]
        self.assertTrue(all(row["checks"]["one_sided_is_exactly_positive_count"] for row in rows))
        self.assertTrue(any(row["positive_but_absolute_fails"] > 0 for row in rows))

    def test_twin_subhalf_absolute_certificate_is_impossible(self) -> None:
        rows = self.twin["finite_prime_pair_block_rows"]
        self.assertGreater(sum(row["subhalf_expected_blocks"] for row in rows), 0)
        self.assertEqual(self.twin["aggregate"]["subhalf_absolute_pass_count"], 0)
        self.assertTrue(all(row["checks"]["subhalf_absolute_certificate_is_impossible"] for row in rows))

    def test_proof_dags_end_at_one_open_lemma(self) -> None:
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[0]["status"], "proved_exact_input")
            self.assertEqual(nodes[1]["status"], "proved_exact")
            self.assertEqual(nodes[2]["status"], "refuted_or_overstrong")
            self.assertEqual(nodes[3]["status"], "open_not_proven")

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "rejected_target_count": 4,
                "proof_dag_count": 4,
                "finite_arithmetic_diagnostic_count": 4,
                "decisive_route_correction_count": 3,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )

    def test_json_contract_has_no_nonfinite_values(self) -> None:
        path = ROOT / "data" / "open-problem" / "ticket185-spectral-cycle-factor-granularity.json"
        if not path.exists():
            self.skipTest("generated artifact is created by the ticket script")
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(all(row["status"] == "open_not_proven" for row in payload["attempts"]))
        self.assertNotIn(": Infinity", text)
        self.assertNotIn(": -Infinity", text)
        self.assertNotIn(": NaN", text)


if __name__ == "__main__":
    unittest.main()
