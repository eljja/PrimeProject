from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket227_mellin_block_buchstab_lifts as ticket227  # noqa: E402


class Ticket227MellinBlockBuchstabLiftsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket227.build_audit()
        cls.root = cls.audit["mellin_block_buchstab_lifts_audit"]

    def test_global_claim_boundary_remains_open(self) -> None:
        self.assertEqual(self.audit["schema"], ticket227.SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_corrected_route_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_single_ratio_alias_and_dual_visibility(self) -> None:
        section = self.root["riemann"]["reproducible_computation"]
        rows = section["mellin_alias_rows"]
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(row["q2_alias_zero_verified"])
            self.assertTrue(row["q3_alias_visible_verified"])
        self.assertTrue(rows[0]["quadrature_identity_verified"])
        self.assertTrue(rows[1]["quadrature_identity_verified"])
        self.assertIsNone(rows[2]["quadrature_identity_verified"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["single_dilation_infinite_alias_family_proved"])
        self.assertTrue(
            aggregate[
                "dual_incommensurate_dilation_removes_nonconstant_line_aliases_proved"
            ]
        )
        self.assertFalse(aggregate["uniform_dense_weil_core_frame_bound_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_symbolic_interval_endpoints(self) -> None:
        certified, interval_floor, ratio_1, ratio_infinity = (
            ticket227.suffix_interval_certificate((4, 2, 1))
        )
        self.assertTrue(certified)
        self.assertEqual(interval_floor, 1)
        self.assertEqual(ratio_1, Fraction(4385, 3367))
        self.assertEqual(ratio_infinity, Fraction(559, 320))

    def test_collatz_infinite_family_formulas(self) -> None:
        section = self.root["collatz"]["reproducible_computation"]
        self.assertGreaterEqual(
            section["bounded_suffix_search"]["certificate_count"], 1
        )
        rows = section["selected_family_rows"]
        self.assertEqual(
            [row["repetition_r"] for row in rows], [1, 2, 3, 5, 10, 20, 40]
        )
        for row in rows:
            self.assertTrue(row["formula_verified"])
            self.assertTrue(row["primitive_unique_marker_4_verified"])
            self.assertTrue(row["strict_unit_interval_1_2_verified"])
            self.assertFalse(row["D_divides_B"])
            self.assertGreater(row["B_over_D"], 1.0)
            self.assertLess(row["B_over_D"], 2.0)
        aggregate = section["aggregate"]
        self.assertTrue(
            aggregate["general_repeated_block_suffix_interval_criterion_proved"]
        )
        self.assertFalse(aggregate["all_primitive_words_excluded"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_factor_cells_preserve_ticket226_counts(self) -> None:
        section = self.root["goldbach"]["reproducible_computation"]
        expected = {
            10_000: {"PP": 254, "PS": 118, "SP": 118, "SS": 34},
            100_000: {"PP": 1620, "PS": 759, "SP": 759, "SS": 294},
            1_000_000: {"PP": 10804, "PS": 5833, "SP": 5833, "SS": 3216},
        }
        for row in section["factor_cell_rows"]:
            self.assertEqual(row["counts"], expected[row["even_target_N"]])
            self.assertTrue(row["factor_pair_count_verified"])
            self.assertTrue(row["bin_totals_verified"])
            self.assertTrue(row["exact_decomposition_verified"])
            self.assertEqual(row["q_divides_N_exception_identity_failures"], 0)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["exact_PS_SP_SS_factor_lifts_proved"])
        self.assertFalse(aggregate["uniform_moving_residue_prime_estimate_proved"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_factor_cells_preserve_ticket226_counts(self) -> None:
        section = self.root["twin_prime"]["reproducible_computation"]
        expected = {
            10_000: {"PP": 205, "PS": 78, "SP": 76, "SS": 35},
            100_000: {"PP": 1224, "PS": 559, "SP": 537, "SS": 253},
            1_000_000: {"PP": 8169, "PS": 4332, "SP": 4350, "SS": 2453},
        }
        for row in section["factor_cell_rows"]:
            self.assertEqual(row["counts"], expected[row["horizon_X"]])
            self.assertEqual(row["SS_shared_prime_factor_collisions"], 0)
            self.assertTrue(row["factor_pair_count_verified"])
            self.assertTrue(row["bin_totals_verified"])
            self.assertTrue(row["exact_decomposition_verified"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["SS_factor_graph_disjointness_proved"])
        self.assertFalse(aggregate["uniform_shifted_bilinear_power_saving_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_track_artifacts_are_reproducible(self) -> None:
        ticket227.write_outputs(self.audit)
        integrated = json.loads(
            (
                ROOT
                / "data/open-problem/ticket227-mellin-block-buchstab-lifts.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(integrated["schema"], ticket227.SCHEMA)
        machine = integrated["mellin_block_buchstab_lifts_audit"]["machine_audit"]
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)


if __name__ == "__main__":
    unittest.main()
