from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket127_exception_repair_effective_bridges import (  # noqa: E402
    collatz_nontrivial_path_correction_audit,
    goldbach_singular_series_lower_bound_audit,
    riemann_dense_core_counterexample_audit,
    twin_raw_budget_transport_audit,
)


class Ticket127ExceptionRepairEffectiveBridgesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/ticket127-exception-repair-effective-bridges.json"
            ).read_text(encoding="utf-8")
        )
        cls.audit = cls.payload["effective_bridge_audit"]

    def test_riemann_counterexample_route_is_only_a_semidecision(self) -> None:
        audit = riemann_dense_core_counterexample_audit()
        self.assertEqual(
            audit["theorem_name"], "DenseCoreNegativeWitnessSemidecision"
        )
        self.assertTrue(audit["finite_sanity_model"]["negative"])
        self.assertIn("finite failure", audit["route_decision"]["discard"])
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_collatz_base_exception_is_removed_from_counterexamples(self) -> None:
        audit = collatz_nontrivial_path_correction_audit()
        finite = audit["exact_28_bit_audit"]
        self.assertEqual(finite["all_unresolved_class_count"], 4_027_110)
        self.assertEqual(finite["trivial_fixed_path_count"], 1)
        self.assertEqual(finite["nontrivial_unresolved_class_count"], 4_027_109)
        self.assertEqual(finite["maximum_nontrivial_low_run"], 23)
        self.assertEqual(finite["longest_nontrivial_witnesses"], [27, 31])
        self.assertEqual(
            audit["route_decision"]["next_theorem"],
            "UniformNontrivialEventuallyLowPathExclusion",
        )
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_goldbach_singular_series_closes_only_a(self) -> None:
        audit = goldbach_singular_series_lower_bound_audit()
        self.assertEqual(audit["proved_statement"], "S(N)>=1 for every positive even N.")
        self.assertEqual(
            audit["exact_normalization_consequence"]["closed_coefficient"],
            "A=1",
        )
        self.assertAlmostEqual(
            audit["endpoint_budget"]["strict_required_residual_K_ceiling"],
            42.83274372223497,
        )
        self.assertIn("pointwise", audit["route_decision"]["remaining_premise"])
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_twin_normalized_recurrence_equals_raw_transport(self) -> None:
        audit = twin_raw_budget_transport_audit()
        finite = audit["finite_16m_to_32m_audit"]
        self.assertAlmostEqual(
            finite["known_budget_growth_gamma"], 2.0115420952456007
        )
        self.assertAlmostEqual(
            finite["adverse_numerator_growth_u"], 1.8603305083667954
        )
        self.assertAlmostEqual(
            finite["paired_residual_contribution"]
            + finite["boundary_residual_contribution"],
            finite["normalized_recurrence_residual"],
        )
        self.assertGreater(finite["raw_transport_slack"], 0.0)
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)

    def test_no_conjecture_resolution_is_recorded(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_intermediate_theorem_count"], 4)
        self.assertEqual(machine["historical_logic_correction_count"], 1)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for attempt in self.payload["attempts"]:
            self.assertIn("No conjecture proof", attempt["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
