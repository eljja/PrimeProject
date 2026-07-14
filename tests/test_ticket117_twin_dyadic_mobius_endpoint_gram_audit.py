from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket117_twin_dyadic_mobius_endpoint_gram_audit import (  # noqa: E402
    SCHEMA,
    audit_dyadic_mobius_endpoint_gram,
    dyadic_outer_blocks,
)


class Ticket117TwinDyadicMobiusEndpointGramAuditTests(unittest.TestCase):
    def test_truncated_dyadic_shells_partition_outer_divisors(self) -> None:
        blocks = dyadic_outer_blocks(17, 292)
        self.assertEqual(blocks[0]["actual_lower"], 17)
        self.assertEqual(blocks[-1]["actual_upper"], 292)
        covered = [
            divisor
            for block in blocks
            for divisor in range(
                int(block["actual_lower"]),
                int(block["actual_upper"]) + 1,
            )
        ]
        self.assertEqual(covered, list(range(17, 293)))
        self.assertEqual(len(covered), len(set(covered)))
        for block in blocks:
            self.assertGreaterEqual(
                int(block["actual_lower"]),
                int(block["shell_lower"]),
            )
            self.assertLessEqual(
                int(block["actual_upper"]),
                int(block["shell_upper"]),
            )

    def test_small_audit_reconstructs_endpoint_and_real_gram(self) -> None:
        row = audit_dyadic_mobius_endpoint_gram(4_096, 3_237.52)
        self.assertLess(
            row["time_domain_dyadic_reconstruction_max_error"],
            1e-12,
        )
        self.assertLess(row["maximum_profile_reconstruction_error"], 1e-9)
        self.assertLess(
            row["inherited_signed_budget_reconstruction_error"],
            1e-9,
        )
        self.assertLess(row["maximum_gram_identity_error"], 1e-8)
        self.assertEqual(row["minor_cell_count"], 162)
        self.assertEqual(len(row["dyadic_denominator_profile"]), 31)
        self.assertEqual(row["dyadic_block_count"], 5)
        self.assertGreater(row["independent_dyadic_budget_ratio"], 1.0)
        self.assertFalse(row["dyadic_closes_finite"])

    def test_generated_artifact_contract(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket117-twin-dyadic-mobius-endpoint-gram-audit.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_dyadic_mobius_endpoint_gram_audit"]
        machine = audit["machine_audit"]
        self.assertEqual(machine["maximum_horizon"], 4_194_304)
        self.assertEqual(machine["row_count"], 6)
        self.assertEqual(machine["minor_cell_count"], 162)
        self.assertEqual(machine["right_denominator_group_count"], 31)
        self.assertEqual(machine["outer_pair_count"], 1_650_675)
        self.assertEqual(machine["dyadic_budget_worsens_count"], 6)
        self.assertEqual(machine["dyadic_improves_sign_count"], 4)
        self.assertEqual(machine["dyadic_finite_closure_count"], 0)
        self.assertEqual(
            machine["denominator_cauchy_finite_closure_count"],
            0,
        )
        self.assertEqual(machine["denominator_cauchy_violation_count"], 0)
        self.assertEqual(machine["width_two_partition_finite_closure_count"], 0)
        self.assertEqual(machine["contract_failure_count"], 0)
        frontier = audit["rows"][-1]
        self.assertAlmostEqual(
            frontier["independent_dyadic_budget_ratio"],
            1.6045760574710985,
            places=12,
        )
        self.assertAlmostEqual(
            frontier["best_width_two_contiguous_partition"]["lower_bound"],
            -1_236.2679265222978,
            places=6,
        )
        self.assertEqual(
            [
                (group["first_block"], group["last_block"])
                for group in frontier["best_width_two_contiguous_partition"][
                    "groups"
                ]
            ],
            [
                ("D128", "D256"),
                ("D512", "D1024"),
                ("D2048", "D4096"),
                ("D8192", "D16384"),
            ],
        )
        self.assertEqual(
            audit["next_theorem_target"],
            "EventuallySubcriticalAdjacentDyadicPairVaughanEndpointBudget",
        )


if __name__ == "__main__":
    unittest.main()
