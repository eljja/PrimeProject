from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket118_twin_canonical_adjacent_pair_holdout import (  # noqa: E402
    HOLDOUT_HORIZON,
    RULE_ID,
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


if __name__ == "__main__":
    unittest.main()
