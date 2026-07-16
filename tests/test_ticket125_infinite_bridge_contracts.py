from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket125_infinite_bridge_contracts import (  # noqa: E402
    GOLDBACH_VERIFIED_LIMIT,
    SCHEMA,
    build_attempts,
    build_audit,
    collatz_symbolic_descent_audit,
    dyadic_contraction_certificate,
    goldbach_explicit_cutoff_audit,
    main,
    rh_density_positivity_audit,
    twin_dyadic_contraction_audit,
)


class Ticket125InfiniteBridgeContractsTests(unittest.TestCase):
    def test_rh_extension_requires_all_three_hypotheses(self) -> None:
        audit = rh_density_positivity_audit()
        missing = {
            row["missing_hypothesis"]
            for row in audit["exact_no_go_models"]
        }
        self.assertEqual(
            missing, {"density", "continuity", "all-cone positivity"}
        )
        self.assertEqual(
            audit["machine_audit"][
                "finite_checks_with_unseen_negative_direction"
            ],
            5,
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_cylinders_replay_and_leave_a_boundary(self) -> None:
        audit = collatz_symbolic_descent_audit(4, 12)
        machine = audit["machine_audit"]
        last = audit["precision_rows"][-1]
        self.assertEqual(machine["largest_precision_bits"], 12)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertGreater(last["uniformly_descending_class_count"], 0)
        self.assertGreater(last["unresolved_class_count"], 0)
        self.assertTrue(last["boundary_requires_refinement"])
        self.assertEqual(
            last["uniformly_descending_class_count"]
            + last["unresolved_class_count"],
            last["odd_class_count"],
        )

    def test_collatz_full_audit_has_expected_18_bit_frontier(self) -> None:
        audit = collatz_symbolic_descent_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["largest_odd_class_count"], 131_072)
        self.assertEqual(
            machine["largest_uniformly_descending_class_count"], 121_825
        )
        self.assertEqual(machine["largest_unresolved_class_count"], 9_247)
        self.assertAlmostEqual(
            machine["largest_certified_fraction"],
            121_825 / 131_072,
        )

    def test_goldbach_endpoint_budget_is_explicit(self) -> None:
        audit = goldbach_explicit_cutoff_audit()
        self.assertEqual(audit["verified_limit"], GOLDBACH_VERIFIED_LIMIT)
        self.assertGreater(audit["natural_log_verified_limit"], 42.0)
        self.assertLess(audit["natural_log_verified_limit"], 43.0)
        candidate = audit["frozen_candidate_budget"]
        self.assertAlmostEqual(candidate["residual_constant_K"], 40.0)
        self.assertGreater(
            candidate["maximum_compatible_prime_power_constant_B"], 72_000
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_dyadic_contraction_is_strict(self) -> None:
        passing = dyadic_contraction_certificate(0.75, 0.23)
        endpoint = dyadic_contraction_certificate(0.75, 0.25)
        self.assertTrue(passing["criterion_passes"])
        self.assertAlmostEqual(passing["limsup_ceiling"], 0.92)
        self.assertAlmostEqual(passing["fixed_margin"], 0.08)
        self.assertFalse(endpoint["criterion_passes"])

    def test_twin_finite_candidate_passes_but_stays_bounded(self) -> None:
        audit = twin_dyadic_contraction_audit()
        machine = audit["machine_audit"]
        self.assertEqual(machine["finite_transition_count"], 4)
        self.assertEqual(machine["exact_candidate_pass_count"], 4)
        self.assertEqual(machine["certificate_candidate_pass_count"], 4)
        self.assertLessEqual(
            machine["maximum_certificate_recurrence_residual"], 0.23
        )
        self.assertEqual(machine["endpoint_countermodel_failure_count"], 0)
        self.assertIn("no unseen holdout", audit["frozen_candidate"]["selection_status"])

    def test_attempts_preserve_open_claim_boundary(self) -> None:
        audit = build_audit()
        attempts = {row["problem_id"]: row for row in build_attempts(audit)}
        self.assertEqual(
            set(attempts), {"riemann", "collatz", "goldbach", "twin-prime"}
        )
        self.assertEqual(
            attempts["collatz"]["candidate_theorem"],
            "AdaptiveResidueFiniteStoppingCover",
        )
        self.assertEqual(
            attempts["twin-prime"]["candidate_theorem"],
            "DyadicVaughanObstructionContractionAndInterpolation",
        )
        self.assertTrue(
            all("No conjecture proof" in row["claim_boundary"] for row in attempts.values())
        )
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_main_writes_shared_and_problem_artifacts(self) -> None:
        self.assertEqual(main(), 0)
        path = ROOT / "data/open-problem/ticket125-infinite-bridge-contracts.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            payload["status"],
            "four_exact_bridge_contracts_proved_missing_arithmetic_hypotheses_open",
        )
        self.assertTrue(
            (
                ROOT
                / "data/open-problem/twin-prime/tp-ticket-125-dyadic-obstruction-contraction.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
