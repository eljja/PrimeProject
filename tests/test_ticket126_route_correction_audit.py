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

from ticket126_route_correction_audit import (  # noqa: E402
    GOLDBACH_VERIFIED_LIMIT,
    PREREGISTRATION_COMMIT,
    RECOVERY_PREREGISTRATION_COMMIT,
    collatz_eventually_low_tree_audit,
    goldbach_prime_power_contamination_audit,
    preregistration_contract,
    proper_prime_power_count_bound,
    riemann_autocorrelation_cone_audit,
)


class Ticket126RouteCorrectionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/ticket126-route-correction-audit.json"
            ).read_text(encoding="utf-8")
        )
        cls.audit = cls.payload["route_correction_audit"]

    def test_preregistration_freezes_primary_twin_endpoint(self) -> None:
        contract = preregistration_contract()
        twin = contract["twin_prime"]
        self.assertEqual(twin["holdout_horizon"], 33_554_432)
        self.assertEqual(twin["source_horizon"], 16_777_216)
        self.assertEqual(twin["alpha"], 0.75)
        self.assertEqual(twin["beta"], 0.23)
        self.assertEqual(twin["execution_policy"]["runs"], 1)
        self.assertFalse(twin["execution_policy"]["retuning_after_result"])

    def test_riemann_density_shortcut_is_refuted_without_claiming_rh(self) -> None:
        audit = riemann_autocorrelation_cone_audit()
        self.assertEqual(
            audit["theorem_name"],
            "ContinuousEvaluationSeparatesAutocorrelationCone",
        )
        self.assertIn("not dense", audit["proved_statement"])
        self.assertIn(
            "NonCircularWeilAutocorrelationPositivity",
            audit["route_decision"]["next_theorem"],
        )
        self.assertIn("neither RH", audit["proof_boundary"])
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_adaptive_tree_replays_ticket125(self) -> None:
        audit = collatz_eventually_low_tree_audit(4, 18)
        machine = audit["machine_audit"]
        self.assertEqual(machine["ticket125_replay_mismatch_count"], 0)
        self.assertEqual(machine["largest_unresolved_class_count"], 9_247)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_collatz_target_counts_only_eventually_low_paths(self) -> None:
        audit = self.audit["collatz"]
        equivalence = audit["proved_equivalence"]
        self.assertIn("eventually-low", equivalence["statement"])
        self.assertIn("not eventually low", audit["boundary_ray_correction"]["proved_fact"])
        self.assertEqual(
            audit["retained_target"]["name"],
            "UniformNontrivialEventuallyLowPathExclusion",
        )
        self.assertEqual(audit["machine_audit"]["maximum_precision_bits"], 28)
        self.assertEqual(
            audit["machine_audit"]["largest_unresolved_class_count"],
            4_027_110,
        )
        row = audit["precision_rows"][-1]
        self.assertTrue(row["trivial_fixed_path_present"])
        self.assertEqual(row["longest_low_run_witnesses"], [1])
        self.assertEqual(row["nontrivial_unresolved_class_count"], 4_027_109)
        self.assertEqual(
            row["maximum_nontrivial_consecutive_low_refinements"], 23
        )
        self.assertEqual(row["longest_nontrivial_low_run_witnesses"], [27, 31])
        self.assertIn("n=1", audit["base_exception_correction"]["exception"])

    def test_goldbach_prime_power_count_bound_dominates_exact_counts(self) -> None:
        audit = goldbach_prime_power_contamination_audit()
        for row in audit["count_sanity_rows"]:
            self.assertTrue(row["bound_holds"])
            self.assertLessEqual(
                row["actual_distinct_proper_prime_power_count"],
                proper_prime_power_count_bound(row["limit"]),
            )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_goldbach_closes_b_but_not_a_or_k(self) -> None:
        audit = self.audit["goldbach"]
        tail = audit["uniform_tail"]
        self.assertEqual(tail["verified_limit"], GOLDBACH_VERIFIED_LIMIT)
        self.assertAlmostEqual(tail["explicit_uniform_B"], 2.0949181787429647)
        self.assertGreater(tail["k_40_budget_margin"], 0.0)
        self.assertEqual(
            audit["route_decision"]["closed_premise"],
            "proper-prime-power contamination constant B",
        )
        self.assertEqual(
            audit["route_decision"]["remaining_premises"],
            [
                "uniform positive major coefficient A",
                "uniform pointwise residual constant K",
            ],
        )
        self.assertGreater(GOLDBACH_VERIFIED_LIMIT, math.exp(6) * 4)

    def test_twin_holdout_preserves_registration_and_recovery_history(self) -> None:
        twin = self.audit["twin_prime"]
        self.assertEqual(twin["preregistration_commit"], PREREGISTRATION_COMMIT)
        self.assertEqual(
            twin["recovery_preregistration_commit"],
            RECOVERY_PREREGISTRATION_COMMIT,
        )
        self.assertEqual(twin["failed_unserialized_execution_count"], 1)
        self.assertEqual(twin["valid_recovery_execution_count"], 1)
        self.assertFalse(twin["retuned_after_result"])

    def test_twin_primary_residual_is_exact_and_passes_finitely(self) -> None:
        result = self.audit["twin_prime"]["primary_result"]
        expected = result["holdout_certificate_obstruction"] - (
            result["alpha"] * result["source_certificate_obstruction"]
        )
        self.assertAlmostEqual(result["certificate_recurrence_residual"], expected)
        self.assertLessEqual(
            result["certificate_recurrence_residual"], result["beta"]
        )
        self.assertTrue(result["primary_endpoint_passes"])
        self.assertEqual(
            result["status"], "pass_finite_preregistered_transition"
        )

    def test_no_conjecture_resolution_is_recorded(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertIn("none of the four conjectures", self.payload["claim_boundary"])
        for attempt in self.payload["attempts"]:
            self.assertIn("No conjecture proof", attempt["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
