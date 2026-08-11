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

import ticket218_adaptive_radius_spike_residual_surplus as ticket218


class Ticket218AdaptiveRadiusSpikeResidualSurplusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket218.build_audit()

    def test_riemann_scale_adaptive_signal_and_open_boundary(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        rows = section["scale_adaptive_rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertLess(Decimal(row["absolute_decimal_error"]), Decimal("1e-75"))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["scale_adaptive_radius_certificate_proved"])
        self.assertTrue(aggregate["first_atom_schedule_phase_transition_proved"])
        self.assertFalse(aggregate["actual_zeta_scale_adaptive_upper_bound_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_neighbor_spike_barrier_and_extended_bound(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        rows = section["audited_upper_convergent_rows"]
        self.assertEqual(section["certified_continued_fraction_coefficient_count"], 100)
        self.assertEqual(len(rows), 49)
        self.assertTrue(all(row["all_positive_multiples_excluded"] for row in rows))
        self.assertEqual(
            sum(row["four_q_plus_qnext_below_three_pow_p"] for row in rows),
            48,
        )
        self.assertTrue(rows[0]["fallback_exact_base_difference_barrier"])
        next_upper = section["next_unaudited_upper_convergent"]
        self.assertEqual(
            next_upper["p"],
            16672027258049147969018986102532625254200541727292,
        )
        self.assertEqual(
            next_upper["q"],
            11828991589305104738667316989568711874512497900863,
        )
        self.assertEqual(next_upper["q_decimal"], str(next_upper["q"]))
        self.assertEqual(
            section["single_mountain_k_exclusive_upper_bound"],
            11828991589305104738667316989568711874512497900863,
        )
        self.assertFalse(section["aggregate"]["all_single_mountain_cycles_excluded"])
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_goldbach_exact_eighth_residual_moment_certificate(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        rows = section["dyadic_goldbach_rows"]
        self.assertEqual([row["dyadic_start_X"] for row in rows], [128, 512, 2048, 8192, 32768])
        for row in rows:
            self.assertGreater(row["minimum_exact_representation_count"], 0)
            moments = {entry["order_p"]: entry for entry in row["moment_rows"]}
            self.assertFalse(moments[4]["full_support_certificate_passed"])
            self.assertTrue(moments[8]["full_support_certificate_passed"])
            self.assertLess(
                int(moments[8]["exact_residual_integer_sum"]),
                int(moments[8]["exact_zero_coordinate_threshold"]),
            )
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["exact_eighth_moment_blocks_certified"], 5)
        self.assertEqual(aggregate["exact_fourth_moment_blocks_certified"], 0)
        self.assertFalse(aggregate["cofinal_eighth_moment_arithmetic_bound_proved"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_twin_strict_surplus_transfer_and_finite_diagnostic(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        rows = section["finite_actual_twin_diagnostic_rows"]
        self.assertEqual([row["X"] for row in rows], [1_000, 10_000, 100_000, 1_000_000])
        self.assertTrue(all(row["finite_transfer_inequality_checked"] for row in rows))
        self.assertTrue(all(row["finite_partial_surplus_over_X_log2X"] > 0 for row in rows))
        self.assertLess(abs(rows[-1]["coefficient_one_tail_over_X_log2X"] - 0.5), 0.00001)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["strict_abel_surplus_to_count_transfer_proved"])
        self.assertTrue(aggregate["critical_constant_sharp_for_transfer_proved"])
        self.assertFalse(aggregate["actual_twin_abel_liminf_above_one_half_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket218.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket218-adaptive-radius-spike-residual-surplus.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket218.SCHEMA)
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
