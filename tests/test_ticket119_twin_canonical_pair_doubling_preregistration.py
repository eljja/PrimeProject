from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREREGISTRATION = (
    ROOT
    / "data/open-problem/ticket119-canonical-pair-doubling-preregistration.json"
)


class Ticket119CanonicalPairDoublingPreregistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(PREREGISTRATION.read_text(encoding="utf-8"))

    def test_registration_fixes_unseen_sixteen_million_endpoint(self) -> None:
        self.assertEqual(
            self.payload["schema"],
            "primeproject.ticket119-canonical-pair-doubling-preregistration.v1",
        )
        self.assertEqual(
            self.payload["status"],
            "preregistered_before_holdout_execution",
        )
        self.assertEqual(self.payload["holdout_horizon"], 16_777_216)
        self.assertEqual(
            self.payload["source_commit"],
            "2852b1a086233523aaca78526e16d31ef4b4c221",
        )

    def test_registration_reuses_rule_without_new_selection_freedom(self) -> None:
        self.assertEqual(
            self.payload["rule_id"],
            "canonical_adjacent_shell_pairs_v1",
        )
        partition = self.payload["partition_rule"]
        self.assertIn("(0,1), (2,3)", partition["groups"])
        self.assertIn("q=2,...,32", partition["denominator_policy"])
        for banned in ("partitions", "signs", "cutoffs", "alternate"):
            self.assertIn(banned, partition["optimization_ban"])

    def test_registration_states_falsification_and_claim_boundaries(self) -> None:
        primary = self.payload["primary_endpoint"]
        self.assertEqual(primary["pass_condition"], "strictly greater than zero")
        self.assertIn("DyadicPersistenceFromEightMillion", primary["meaning"])
        self.assertIn("Neither outcome proves or disproves", primary["meaning"])
        self.assertEqual(self.payload["execution_policy"]["runs"], 1)
        self.assertIn("No 16M", self.payload["claim_boundary"])

    def test_disclosed_reference_margin_is_exactly_reconstructible(self) -> None:
        reference = self.payload["registered_reference"]
        reconstructed = (
            reference["finite_lower_bound"]
            / reference["known_without_type_ii_minor"]
        )
        self.assertAlmostEqual(
            reference["normalized_margin"],
            reconstructed,
            places=15,
        )


if __name__ == "__main__":
    unittest.main()
