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

from ticket186_codimension_twoone_layercake_quantization import (  # noqa: E402
    build_audit,
    finite_codimension_diagonal_row,
    goldbach_bad_survivor_layer_row,
    prime_sieve,
    quantized_twin_counterledger,
    smallest_prime_factors,
    two_one_cycle_row,
)


class Ticket186CodimensionTwoOneLayerCakeQuantizationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_finite_codimension_sections_have_vanishing_gap(self) -> None:
        row = finite_codimension_diagonal_row(256, 3)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(
            Fraction(row["smallest_quotient_quadratic_value"]["exact"]),
            Fraction(1, 256),
        )
        gaps = [
            item["smallest_quotient_quadratic_value"]["decimal"]
            for item in self.riemann["finite_coordinate_quotient_rows"]
        ]
        self.assertTrue(
            all(gaps[index + 1] < gaps[index] for index in range(len(gaps) - 1))
        )

    def test_two_one_closed_form_matches_affine_recurrence(self) -> None:
        row = two_one_cycle_row(8, 4)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(row["word"], [1, 2, 2, 2, 1, 2, 2, 2])
        self.assertEqual(int(row["affine_numerator_B"]), 21_109)
        self.assertEqual(int(row["cycle_denominator_D"]), 9_823)

    def test_all_small_contracting_two_one_words_are_exhausted(self) -> None:
        rows = self.collatz["small_h_complete_rows"]
        self.assertEqual(len(rows), sum(horizon - 1 for horizon in range(5, 9)))
        self.assertEqual(
            {(row["horizon_h"], row["first_block_a"]) for row in rows},
            {
                (horizon, first_block)
                for horizon in range(5, 9)
                for first_block in range(1, horizon)
            },
        )
        self.assertTrue(
            all(row["checks"]["affine_divisibility_fails"] for row in rows)
        )

    def test_two_one_infinite_stratum_is_closed(self) -> None:
        aggregate = self.collatz["aggregate"]
        self.assertTrue(aggregate["infinite_family_proved"])
        self.assertTrue(aggregate["includes_imprimitive_words"])
        self.assertEqual(aggregate["analytic_range_starts_at_h"], 9)
        self.assertEqual(aggregate["divisibility_hits"], 0)

    def test_goldbach_layer_cake_identity(self) -> None:
        primality = prime_sieve(1_000)
        least_factor = smallest_prime_factors(1_000)
        row = goldbach_bad_survivor_layer_row(
            1_000, primality, least_factor
        )
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(
            row["bad_survivor_layer_area"], row["sum_of_bad_pair_gates"]
        )
        self.assertGreater(row["last_subhorizon_bad_survivor_count"], 0)

    def test_nonnegative_subhorizon_layers_never_clear_bad_support(self) -> None:
        rows = self.goldbach["target_layer_cake_rows"]
        self.assertTrue(
            all(row["checks"]["every_subhorizon_layer_is_contaminated"] for row in rows)
        )
        self.assertEqual(
            self.goldbach["aggregate"]["layer_cake_identity_failures"], 0
        )

    def test_goldbach_empty_bad_pair_case_is_vacuous(self) -> None:
        primality = prime_sieve(6)
        least_factor = smallest_prime_factors(6)
        row = goldbach_bad_survivor_layer_row(6, primality, least_factor)
        self.assertEqual(row["bad_candidate_pair_count"], 0)
        self.assertEqual(row["factor_horizon_tau_N"], 0)
        self.assertEqual(row["bad_survivor_layer_area"], 0)
        self.assertTrue(all(row["checks"].values()))

    def test_twin_projector_has_four_unit_resolution(self) -> None:
        row = quantized_twin_counterledger(100_000)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(row["quantized_projector_Delta"], 4)
        self.assertEqual(row["twin_class_count"], 1)
        self.assertEqual(row["normalized_projector_margin"], 4 / 100_000)

    def test_actual_twin_ledgers_reconstruct_counts(self) -> None:
        rows = self.twin["finite_cubic_rough_ledger_rows"]
        self.assertTrue(
            all(row["checks"]["projector_equals_four_times_count"] for row in rows)
        )
        self.assertTrue(all(row["quantized_projector_Delta"] >= 4 for row in rows))

    def test_proof_dags_end_at_one_open_lemma(self) -> None:
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(
                [node["status"] for node in nodes],
                [
                    "proved_exact_input_or_open_target",
                    "proved_exact",
                    "refuted_or_overstrong",
                    "open_not_proven",
                ],
            )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_stratum_closure_count": 1,
                "rejected_target_count": 4,
                "proof_dag_count": 4,
                "finite_arithmetic_diagnostic_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )

    def test_json_contract_has_no_nonfinite_values(self) -> None:
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket186-codimension-twoone-layercake-quantization.json"
        )
        payload_text = path.read_text(encoding="utf-8")
        payload = json.loads(payload_text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(row["status"] == "open_not_proven" for row in payload["attempts"])
        )
        self.assertNotIn(": Infinity", payload_text)
        self.assertNotIn(": -Infinity", payload_text)
        self.assertNotIn(": NaN", payload_text)


if __name__ == "__main__":
    unittest.main()
