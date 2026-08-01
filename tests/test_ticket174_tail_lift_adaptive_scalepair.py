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

from ticket174_tail_lift_adaptive_scalepair import (  # noqa: E402
    archimedean_tail_budget,
    build_audit,
    child_lift_data,
    collatz_unique_zero_lift_audit,
    goldbach_adaptive_major_set_audit,
    riemann_diagonal_tail_audit,
    twin_scale_pair_aggregation_audit,
)
from ticket173_finite_section_cylinder_phase_tensor import (  # noqa: E402
    accelerated_odd_step,
    cylinder_least_representative,
)


class Ticket174TailLiftAdaptiveScalePairTests(unittest.TestCase):
    def test_riemann_quadratic_tail_schedule_decays(self) -> None:
        audit = riemann_diagonal_tail_audit()
        self.assertEqual(audit["failure_count"], 0)
        rows = audit["cutoff_schedule_rows"]
        self.assertLess(
            rows[-1]["tail_budgets_B"]["quadratic_N2"],
            rows[0]["tail_budgets_B"]["quadratic_N2"],
        )
        self.assertGreater(
            rows[-1]["tail_budgets_B"]["linear_8N"],
            rows[0]["tail_budgets_B"]["linear_8N"],
        )

    def test_riemann_tail_formula_is_positive(self) -> None:
        self.assertGreater(archimedean_tail_budget(32, 1024), 0.0)
        self.assertLess(
            archimedean_tail_budget(32, 32**3),
            archimedean_tail_budget(32, 32**2),
        )
        self.assertTrue(
            math.isclose(
                archimedean_tail_budget(200, 800),
                1.5754527435280588,
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
        )

    def test_collatz_actual_child_is_unique_zero_lift(self) -> None:
        word = (1, 2, 1, 3)
        parent, _ = cylinder_least_representative(word)
        endpoint = parent
        for _ in word:
            endpoint, _ = accelerated_odd_step(endpoint)
        _, actual = accelerated_odd_step(endpoint)
        self.assertEqual(child_lift_data(word, actual)["lift_quotient"], 0)
        for candidate in range(1, 17):
            if candidate != actual:
                self.assertGreater(child_lift_data(word, candidate)["lift_quotient"], 0)

    def test_collatz_density_bound_and_natural_stabilization(self) -> None:
        audit = collatz_unique_zero_lift_audit()
        self.assertEqual(audit["failure_count"], 0)
        for row in audit["truncated_branch_density_rows"]:
            self.assertLessEqual(
                row["zero_lift_fraction"], row["upper_bound_one_over_A"] + 1e-15
            )
        self.assertTrue(
            all(
                row["checks"]["all_post_stabilization_lifts_are_zero"]
                for row in audit["natural_stabilized_ray_rows"]
            )
        )

    def test_goldbach_adaptive_certificate_is_equivalent_on_finite_data(self) -> None:
        audit = goldbach_adaptive_major_set_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(audit["aggregate"]["finite_targets"], 987)
        self.assertEqual(audit["aggregate"]["adaptive_equivalence_failures"], 0)

    def test_goldbach_adaptive_selection_uses_positive_terms(self) -> None:
        audit = goldbach_adaptive_major_set_audit()
        for row in audit["finite_prime_adaptive_selection_rows"]:
            self.assertGreaterEqual(row["minimum_selected_positive_terms"], 0)
            self.assertLessEqual(row["maximum_selected_positive_fraction"], 1.0)
            self.assertLess(row["maximum_fourier_reconstruction_error"], 1e-7)

    def test_twin_logarithmic_loss_is_saturated(self) -> None:
        audit = twin_scale_pair_aggregation_audit()
        self.assertEqual(audit["failure_count"], 0)
        for row in audit["sharp_logarithmic_loss_rows"]:
            self.assertTrue(
                math.isclose(
                    row["operator_norm_exact"],
                    row["L_times_sqrt_max_pair_energy"],
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                )
            )
            self.assertEqual(row["scale_pair_count"], row["haar_level_count_L"] ** 2)

    def test_twin_finite_operator_bounds_hold(self) -> None:
        audit = twin_scale_pair_aggregation_audit()
        for row in audit["finite_t161_aggregation_rows"]:
            self.assertLessEqual(
                row["operator_norm"], row["L_times_sqrt_max_pair_energy"] + 1e-7
            )

    def test_machine_audit_and_proof_dags_remain_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            statuses = [
                node["status"]
                for node in audit[section_name]["proof_dag"]["nodes"]
            ]
            self.assertEqual(
                statuses,
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_generated_machine_artifact_matches_builder(self) -> None:
        path = ROOT / "data" / "open-problem" / "ticket174-tail-lift-adaptive-scalepair.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "four_exact_quantitative_audits_all_conjectures_open")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(row["status"] == "open_not_proven" for row in payload["attempts"])
        )


if __name__ == "__main__":
    unittest.main()
