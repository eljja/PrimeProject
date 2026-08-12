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

import ticket219_bandpass_matveev_crossfit_qualitative_abel as ticket219


class Ticket219BandpassMatveevCrossFitQualitativeAbelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket219.build_audit()

    def test_riemann_positive_bandpass_certificate_and_boundary(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        self.assertEqual(len(section["synthetic_replay_rows"]), 7)
        self.assertTrue(
            all(
                row["upper_bound_covers_exact_band_count"]
                for row in section["synthetic_replay_rows"]
            )
        )
        self.assertGreater(Decimal(section["kernel_floor_on_closed_band"]), 0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["positive_dyadic_bandpass_certificate_proved"])
        self.assertTrue(aggregate["cofinal_actual_defect_condition_equivalent_to_RH"])
        self.assertFalse(aggregate["prime_side_actual_zeta_enclosure_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_matveev_tail_closes_single_mountain_family(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        threshold = section["matveev_threshold_certificate"]
        self.assertEqual(threshold["first_certified_numerator_p"], 27_456_680_737)
        self.assertTrue(all(threshold["checks"].values()))
        self.assertEqual(section["ticket218_audited_upper_convergent_count"], 49)
        self.assertGreater(
            section["first_unaudited_upper_convergent"]["p"],
            threshold["first_certified_numerator_p"],
        )
        self.assertTrue(all(section["range_glue_checks"].values()))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["all_positive_single_mountain_cycles_excluded"])
        self.assertFalse(aggregate["all_multi_run_cycles_excluded"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_cross_fitted_eighth_moment(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        rows = section["dyadic_goldbach_rows"]
        self.assertEqual(
            [row["dyadic_start_X"] for row in rows],
            [128, 512, 2048, 8192, 32768],
        )
        folds = [fold for row in rows for fold in row["fold_rows"]]
        self.assertEqual(len(folds), 10)
        self.assertTrue(all(fold["training_and_test_disjoint"] for fold in folds))
        self.assertTrue(
            all(fold["eighth_moment_held_out_support_certified"] for fold in folds)
        )
        aggregate = section["aggregate"]
        self.assertEqual(aggregate["exact_eighth_moment_held_out_folds_certified"], 10)
        self.assertEqual(aggregate["exact_fourth_moment_held_out_folds_certified"], 1)
        self.assertFalse(aggregate["cofinal_cross_fitted_eighth_moment_bound_proved"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_twin_qualitative_abel_equivalence_and_sparse_no_go(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        rows = section["finite_and_sparse_diagnostic_rows"]
        self.assertEqual([row["X"] for row in rows], [1_000, 10_000, 100_000, 1_000_000])
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertLess(rows[-1]["sparse_Abel_over_X_log2X"], rows[0]["sparse_Abel_over_X_log2X"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["qualitative_abel_infinitude_equivalence_proved"])
        self.assertTrue(
            aggregate[
                "ticket218_density_scale_condition_not_necessary_for_abstract_infinitude"
            ]
        )
        self.assertFalse(aggregate["actual_twin_abel_transform_unbounded_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["closed_infinite_subfamily_count"], 1)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket219.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket219-bandpass-matveev-crossfit-qualitative-abel.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket219.SCHEMA)
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
