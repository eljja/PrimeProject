from __future__ import annotations

import sys
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket118_twin_canonical_adjacent_pair_holdout import (  # noqa: E402
    HOLDOUT_HORIZON,
    RULE_ID,
    SCHEMA,
    canonical_adjacent_partition,
    preregistration_contract,
)


class Ticket118CanonicalAdjacentPairPreregistrationTests(unittest.TestCase):
    def test_canonical_partition_is_result_independent(self) -> None:
        self.assertEqual(
            canonical_adjacent_partition(8),
            [(0, 2), (2, 4), (4, 6), (6, 8)],
        )
        self.assertEqual(
            canonical_adjacent_partition(9),
            [(0, 2), (2, 4), (4, 6), (6, 8), (8, 9)],
        )

    def test_preregistration_contract_is_frozen(self) -> None:
        preregistration = preregistration_contract()
        self.assertEqual(preregistration["holdout_horizon"], HOLDOUT_HORIZON)
        self.assertEqual(preregistration["rule_id"], RULE_ID)
        self.assertEqual(
            preregistration["status"],
            "preregistered_before_holdout_execution",
        )
        self.assertIn(
            "No 8M result was used",
            preregistration["claim_boundary"],
        )

    def test_generated_holdout_passes_only_the_registered_finite_endpoint(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        audit = payload["twin_canonical_adjacent_pair_holdout"]
        primary = audit["primary_result"]
        self.assertEqual(primary["holdout_horizon"], HOLDOUT_HORIZON)
        self.assertEqual(primary["status"], "pass_finite_closure")
        self.assertTrue(primary["passes_registered_endpoint"])
        self.assertAlmostEqual(
            primary["finite_lower_bound"],
            156_726.96996317152,
            places=6,
        )
        self.assertTrue(
            audit["best_width_two_comparison"]["same_partition"]
        )
        row = audit["holdout_row"]
        self.assertLess(
            row["time_domain_dyadic_reconstruction_max_error"],
            1e-9,
        )
        self.assertLess(row["maximum_profile_reconstruction_error"], 1e-6)
        self.assertLess(row["maximum_gram_identity_error"], 1e-4)
        self.assertEqual(
            audit["next_theorem_target"],
            "EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget",
        )


if __name__ == "__main__":
    unittest.main()
