from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket120_twin_low_divisor_pair_savings_audit import (  # noqa: E402
    SCHEMA,
    _pair_budget,
    abstract_countermodels,
)


RESULT = (
    ROOT
    / "data/open-problem/ticket120-twin-low-divisor-pair-savings-audit.json"
)


class Ticket120TwinLowDivisorPairSavingsAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(RESULT.read_text(encoding="utf-8"))
        self.audit = self.payload["twin_low_divisor_pair_savings_audit"]

    def test_exact_pair_identity_extremizers(self) -> None:
        aligned = _pair_budget(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        opposite = _pair_budget(1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        self.assertEqual(aligned["singleton_budget"], 4.0)
        self.assertEqual(aligned["paired_budget"], 4.0)
        self.assertEqual(aligned["total_saving"], 0.0)
        self.assertEqual(opposite["singleton_budget"], 4.0)
        self.assertEqual(opposite["paired_budget"], 0.0)
        self.assertEqual(opposite["total_saving"], 4.0)

    def test_weak_contract_fixed_fraction_is_exactly_refuted(self) -> None:
        models = abstract_countermodels()
        aligned = models[0]
        self.assertTrue(aligned["positive_semidefinite"])
        self.assertEqual(aligned["gram_determinant"], 0.0)
        self.assertEqual(
            aligned["paired_budget"] / aligned["singleton_budget"],
            1.0,
        )
        discarded = self.audit["discarded_candidate"]
        self.assertEqual(
            discarded["status"],
            "refuted_by_exact_weak_contract_countermodel",
        )
        self.assertEqual(discarded["witness"], aligned["model"])

    def test_machine_audit_reconstructs_all_scale_rows(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["scale_count"], 8)
        self.assertEqual(machine["denominator_row_count"], 248)
        self.assertEqual(machine["maximum_cauchy_excess"], 0.0)
        self.assertEqual(machine["minimum_denominator_saving"], 0.0)
        self.assertLess(
            machine["maximum_registered_group_reconstruction_error"],
            1e-8,
        )
        self.assertEqual(machine["total_failure_count"], 0)

    def test_sixteen_million_saving_is_centered_not_scalar(self) -> None:
        row = self.audit["scale_rows"][-1]
        self.assertEqual(row["horizon"], 16_777_216)
        self.assertEqual((row["first_block"], row["second_block"]), ("D256", "D512"))
        self.assertAlmostEqual(
            row["total_saving_fraction"],
            0.19722612342819168,
            places=15,
        )
        self.assertLess(row["mean_share_of_saving"], 0.0001)
        self.assertAlmostEqual(
            row["paired_to_known_ratio"],
            0.4519542463375894,
            places=15,
        )
        self.assertEqual(row["opposite_mean_denominator_count"], 1)
        self.assertEqual(row["negative_centered_cosine_count"], 15)
        self.assertAlmostEqual(
            row["centered_cosine_median"],
            -0.4028108691331668,
            places=15,
        )

    def test_retained_target_requires_arithmetic_structure(self) -> None:
        retained = self.audit["retained_theorem"]
        self.assertEqual(
            retained["name"],
            "VaughanLowDivisorDenominatorSummedAngleGap",
        )
        self.assertIn("not implied by Gram positivity", retained["required_input"])
        self.assertIn("does not prove", self.audit["proof_boundary"])
        attempts = self.payload["attempts"]
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        for attempt in attempts:
            self.assertIn("No ", attempt["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
