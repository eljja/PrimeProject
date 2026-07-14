from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket119_twin_canonical_pair_doubling_holdout import (  # noqa: E402
    HOLDOUT_HORIZON,
    PREREGISTRATION_COMMIT,
    SCHEMA,
    preregistration_contract,
)


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

    def test_preregistration_contract_matches_public_lineage(self) -> None:
        contract = preregistration_contract()
        self.assertEqual(contract["holdout_horizon"], HOLDOUT_HORIZON)
        self.assertEqual(
            PREREGISTRATION_COMMIT,
            "87bdcf9b16c5e57581e9a411aa61290ef2eea173",
        )

    def test_first_registered_result_is_preserved_without_retuning(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json"
        )
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["schema"], SCHEMA)
        audit = result["twin_canonical_pair_doubling_holdout"]
        self.assertEqual(audit["preregistration_commit"], PREREGISTRATION_COMMIT)
        self.assertEqual(
            audit["preregistration_payload_sha256"],
            "59ca66805000b79e23d25a3ff3fd0043151ff0a4fe46759a30ac313e0d631ea7",
        )
        primary = audit["primary_result"]
        self.assertEqual(primary["status"], "pass_finite_closure")
        self.assertTrue(primary["passes_registered_endpoint"])
        self.assertEqual(primary["holdout_horizon"], HOLDOUT_HORIZON)
        self.assertAlmostEqual(
            primary["finite_lower_bound"],
            1_479_021.828077687,
            places=6,
        )

    def test_result_preserves_partition_scale_and_exact_contracts(self) -> None:
        path = (
            ROOT
            / "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json"
        )
        result = json.loads(path.read_text(encoding="utf-8"))
        audit = result["twin_canonical_pair_doubling_holdout"]
        canonical = audit["canonical_partition"]
        self.assertEqual(
            [
                (group["first_block"], group["last_block"])
                for group in canonical["groups"]
            ],
            [
                ("D256", "D512"),
                ("D1024", "D2048"),
                ("D4096", "D8192"),
                ("D16384", "D32768"),
                ("D65536", "D65536"),
            ],
        )
        self.assertAlmostEqual(
            canonical["normalized_margin"],
            0.1973217174640551,
            places=15,
        )
        self.assertTrue(audit["scale_comparison"]["normalized_margin_non_decreasing"])
        self.assertTrue(audit["best_width_two_comparison"]["same_partition"])
        row = audit["holdout_row"]
        self.assertEqual(row["dyadic_block_count"], 9)
        self.assertEqual(len(row["dyadic_denominator_profile"]), 31)
        self.assertLess(row["time_domain_dyadic_reconstruction_max_error"], 1e-9)
        self.assertLess(row["maximum_profile_reconstruction_error"], 1e-6)
        self.assertLess(row["maximum_gram_identity_error"], 1e-4)
        self.assertLess(row["maximum_layer_phase_error"], 1e-12)


if __name__ == "__main__":
    unittest.main()
