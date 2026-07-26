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

from ticket159_diagonal_threshold_phase_parity import (  # noqa: E402
    SCHEMA,
    build_audit,
    collatz_threshold,
    doubling_selector,
    inverse_radix_two_fft,
    radix_two_fft,
)


class Ticket159DiagonalThresholdPhaseParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket159-diagonal-threshold-phase-parity.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_global_and_per_problem_artifacts_match_schema(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(
            {row["problem_id"] for row in self.payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        paths = [
            "riemann/rh-ticket-159-effective-diagonal-selector.json",
            "collatz/co-ticket-159-affine-threshold.json",
            "goldbach/gb-ticket-159-phase-energy.json",
            "twin-prime/tp-ticket-159-rough-fiber.json",
        ]
        for relative in paths:
            payload = json.loads(
                (ROOT / "data/open-problem" / relative).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_doubling_selector_is_effective(self) -> None:
        cutoff, trace = doubling_selector(
            lambda value: Fraction(7, value),
            Fraction(1, 100),
        )
        self.assertLessEqual(Fraction(7, cutoff), Fraction(1, 100))
        self.assertGreater(Fraction(7, cutoff // 2), Fraction(1, 100))
        self.assertTrue(trace[-1]["meets_target"])

    def test_riemann_selector_rows_close_exactly(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_effective_diagonal_selector_rows"
        ]
        self.assertEqual(
            [row["nested_core_dimension_N"] for row in rows],
            [1, 2, 4, 8, 16],
        )
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertGreater(
                Fraction(row["promoted_full_form_core_lower_bound"]["exact"]),
                0,
            )

    def test_riemann_every_preassigned_schedule_is_refuted(self) -> None:
        families = self.audit["riemann"]["reproducible_computation"][
            "exact_preassigned_schedule_no_go_families"
        ]
        self.assertEqual(len(families), 4)
        for family in families:
            for row in family["rows"]:
                self.assertEqual(
                    Fraction(row["bound_at_preassigned_cutoff"]["exact"]),
                    1,
                )
                self.assertEqual(
                    Fraction(row["bound_at_next_cutoff"]["exact"]),
                    0,
                )
                self.assertTrue(all(row["checks"].values()))

    def test_collatz_threshold_identity(self) -> None:
        self.assertEqual(collatz_threshold((2,)), Fraction(1))
        self.assertEqual(collatz_threshold((1, 1, 2, 3)), Fraction(73, 47))
        self.assertIsNone(collatz_threshold((1,)))

    def test_collatz_rotation_records_are_exact(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        self.assertGreater(section["record_count"], 5)
        previous = Fraction(0)
        for row in section["finite_record_rotation_threshold_rows"]:
            current = Fraction(
                row["universal_first_term_lower_bound"]["exact"]
            )
            self.assertGreater(current, previous)
            self.assertTrue(all(row["checks"].values()))
            previous = current

    def test_fft_inverse_round_trip(self) -> None:
        values = [0.0, 1.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0]
        recovered = inverse_radix_two_fft(radix_two_fft(values))
        for observed, expected in zip(recovered, values):
            self.assertAlmostEqual(observed.real, expected, places=10)
            self.assertAlmostEqual(observed.imag, 0.0, places=10)

    def test_goldbach_energy_rows_are_valid_but_nonresolving(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        rows = section["finite_prime_dft_energy_rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertEqual(row["observed_zero_representation_count"], 0)
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["maximum_absolute_minor_coefficient"],
                row["minor_energy_l2_squared"] + 1e-7,
            )

    def test_goldbach_energy_is_phase_blind(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_energy_phase_blindness_rows"
        ]
        self.assertEqual([row["transform_size_L"] for row in rows], [4, 8, 16, 32])
        for row in rows:
            self.assertEqual(
                row["positive_zero_coefficient"],
                -row["negative_zero_coefficient"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_rough_fiber_has_zero_feature_information(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        self.assertTrue(section["all_rows_have_both_labels"])
        self.assertTrue(
            section["all_rows_have_twin_and_double_composite_witnesses"]
        )
        rows = section["finite_rough_stratum_rows"]
        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertGreater(row["twin_prime_pair_count"], 0)
            self.assertGreater(row["rough_non_twin_pair_count"], 0)
            self.assertGreater(row["rough_both_composite_pair_count"], 0)
            self.assertEqual(
                row["conditional_mutual_information_bits"],
                0.0,
            )
            self.assertGreater(row["conditional_label_entropy_bits"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_proof_dags_end_at_one_open_lemma(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(
                [node["status"] for node in dag["nodes"]],
                [
                    "refuted_or_insufficient",
                    "proved_exact",
                    "open_not_proven",
                ],
            )
            self.assertEqual(len(dag["edges"]), 2)

    def test_claim_boundaries_do_not_claim_solutions(self) -> None:
        self.assertIn(
            "resolves no target conjecture",
            self.audit["proof_boundary"],
        )
        for attempt in self.payload["attempts"]:
            self.assertTrue(attempt["claim_boundary"].startswith("No "))


if __name__ == "__main__":
    unittest.main()
