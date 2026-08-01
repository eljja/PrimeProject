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

from ticket175_relative_equivalence_signed_block import (  # noqa: E402
    accelerated_descent_record,
    build_audit,
    collatz_stopping_equivalence_audit,
    goldbach_fixed_farey_audit,
    log_archimedean_tail_budget,
    required_log10_cutoff,
    riemann_absolute_margin_audit,
    twin_block_operator_audit,
)


class Ticket175RelativeEquivalenceSignedBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_absolute_margin_audit()
        cls.collatz = collatz_stopping_equivalence_audit()
        cls.goldbach = goldbach_fixed_farey_audit()
        cls.twin = twin_block_operator_audit()

    def test_riemann_log_tail_solver_hits_requested_scale(self) -> None:
        for dimension, digits in [(100, 190.92), (250, 333.68)]:
            cutoff = required_log10_cutoff(dimension, digits)
            solved = log_archimedean_tail_budget(
                dimension, cutoff * math.log(10.0)
            ) / math.log(10.0)
            self.assertTrue(math.isclose(solved, -digits, abs_tol=1e-9))

    def test_riemann_absolute_margin_route_is_inconclusive(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        for row in self.riemann["published_branch_resolution_rows"]:
            self.assertGreater(
                row["required_log10_T_for_explicit_bound_at_branch_scale"],
                row["published_positive_branch_minus_log10_magnitude"],
            )

    def test_collatz_corrected_log_identity(self) -> None:
        for start in [3, 27, 703, 35_655, 626_331]:
            row = accelerated_descent_record(start)
            self.assertIsNotNone(row["first_descent_horizon"])
            self.assertLess(row["corrected_log_identity_error"], 1e-12)

    def test_collatz_finite_audit_boundary(self) -> None:
        self.assertEqual(self.collatz["failure_count"], 0)
        final = self.collatz["finite_first_descent_rows"][-1]
        self.assertEqual(final["odd_starts_checked"], 499_999)
        self.assertEqual(final["first_descent_counterexamples"], 0)
        self.assertEqual(final["maximum_first_descent_horizon"], 111)
        self.assertEqual(final["maximum_horizon_start"], 626_331)

    def test_goldbach_double_loss_identity(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        self.assertEqual(
            self.goldbach["aggregate"]["double_loss_identity_failures"], 0
        )
        self.assertEqual(self.goldbach["aggregate"]["finite_targets"], 987)

    def test_goldbach_fixed_q16_absolute_gate_degrades_on_ladder(self) -> None:
        fractions = self.goldbach["aggregate"]["q16_pass_fractions_by_support"]
        self.assertTrue(all(left > right for left, right in zip(fractions, fractions[1:])))
        self.assertLess(fractions[-1], 0.25)

    def test_twin_block_operator_domination(self) -> None:
        self.assertEqual(self.twin["failure_count"], 0)
        for row in self.twin["finite_t161_block_operator_rows"]:
            self.assertLessEqual(
                row["physical_operator_norm"],
                row["block_matrix_operator_norm"] + 1e-6,
            )

    def test_twin_matched_scale_projection_recovers_log_loss(self) -> None:
        for row in self.twin["matched_scale_projection_rows"]:
            self.assertTrue(math.isclose(row["physical_operator_norm"], 1.0))
            self.assertTrue(math.isclose(row["block_matrix_operator_norm"], 1.0))
            self.assertEqual(
                row["improvement_factor"], float(row["haar_level_count_L"])
            )

    def test_machine_audit_and_dags_remain_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            statuses = [
                node["status"] for node in audit[section_name]["proof_dag"]["nodes"]
            ]
            self.assertEqual(
                statuses,
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_generated_machine_artifact_matches_builder(self) -> None:
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket175-relative-equivalence-signed-block.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["status"], "four_exact_reductions_all_conjectures_open")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(attempt["status"] == "open_not_proven" for attempt in payload["attempts"])
        )


if __name__ == "__main__":
    unittest.main()
