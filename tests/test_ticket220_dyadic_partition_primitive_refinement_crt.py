from __future__ import annotations

import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket220_dyadic_partition_primitive_refinement_crt as ticket220


class Ticket220DyadicPartitionPrimitiveRefinementCRTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket220.build_audit()

    def test_riemann_partition_telescope_and_finite_window_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        rows = section["telescoping_rows"]
        self.assertEqual([row["M_equals_N"] for row in rows], [2, 4, 8, 12, 16])
        self.assertTrue(all(row["identity_verified"] for row in rows))
        self.assertLess(
            Decimal(rows[-1]["distance_to_total_defect_count"]),
            Decimal(rows[0]["distance_to_total_defect_count"]),
        )
        self.assertTrue(
            all(
                row["below_epsilon_1e_minus_6"]
                for row in section["finite_window_hidden_atom_rows"]
            )
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["dyadic_partition_of_unity_proved"])
        self.assertTrue(aggregate["finite_window_global_certificate_refuted"])
        self.assertFalse(aggregate["actual_prime_side_summable_envelope_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_primitive_root_extension(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertTrue(
            all(
                row["composition_identity_verified"]
                and row["fixed_point_identity_verified"]
                and row["nonunit_slope_verified"]
                for row in section["affine_power_replay_rows"]
            )
        )
        self.assertTrue(ticket220.covered_by_single_mountain_closure((1, 2) * 5))
        self.assertTrue(
            ticket220.covered_by_single_mountain_closure((2, 1, 1, 2, 1, 1))
        )
        self.assertFalse(
            ticket220.covered_by_single_mountain_closure((1, 2, 1, 1, 2, 2))
        )
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["primitive_root_extension_proved"])
        self.assertTrue(aggregate["infinite_imprimitive_multi_run_family_closed"])
        self.assertFalse(aggregate["primitive_multi_run_cycles_excluded"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_exact_refinement_stability(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["direct_eighth_moment_folds_certified"], 150)
        self.assertEqual(aggregate["direct_eighth_moment_fold_total"], 150)
        self.assertEqual(aggregate["direct_fourth_moment_folds_certified"], 137)
        self.assertEqual(aggregate["refinement_bridges_certified"], 140)
        self.assertEqual(aggregate["refinement_bridge_total"], 140)
        self.assertTrue(
            all(
                row["refinement_certificate_passed"]
                for row in section["refinement_bridge_rows"]
            )
        )
        self.assertLess(
            max(
                Decimal(row["minkowski_to_barrier_ratio"])
                for row in section["refinement_bridge_rows"]
            ),
            Decimal(1),
        )
        self.assertFalse(aggregate["cofinal_refinement_margin_proved"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_twin_finite_wheel_crt_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        rows = section["finite_wheel_crt_witness_rows"]
        self.assertEqual([row["wheel_W"] for row in rows], [30, 210, 2310, 30030, 510510])
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        for row in rows:
            n = row["composite_pair_witness_n"]
            self.assertEqual(n % row["external_prime_q"], 0)
            self.assertEqual((n + 2) % row["external_prime_r"], 0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["finite_wheel_crt_no_go_proved"])
        self.assertFalse(aggregate["parity_sensitive_bilinear_lower_bound_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["closed_infinite_subfamily_count"], 1)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket220.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket220-dyadic-partition-primitive-refinement-crt.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket220.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        for attempt in integrated["attempts"]:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertTrue(attempt["declared_proposition"])
            self.assertTrue(attempt["discarded_route"])
            self.assertTrue(attempt["remaining_gap"])
            self.assertTrue(attempt["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
