from __future__ import annotations

import itertools
import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket180_finite_information_localization import (  # noqa: E402
    ordered_affine_numerator,
)
from ticket193_everywhere_nineone_parity_envelope import (  # noqa: E402
    all_space_witness_row,
    build_audit,
    finite_nine_one_horizon_row,
    nine_one_boundary_numerator,
    nine_one_product_bound,
    power_of_two_contamination,
)


class Ticket193EverywhereNineOneParityEnvelopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_everywhere_convergence_contract_and_dense_core_no_go(self) -> None:
        contract = self.riemann["extension_contract"]
        self.assertTrue(
            contract["everywhere_pointwise_convergence_forces_uniform_bound"]
        )
        self.assertTrue(contract["associated_forms_converge_pointwise"])
        self.assertFalse(contract["dense_core_pointwise_convergence_is_sufficient"])
        self.assertFalse(contract["actual_weil_everywhere_convergence_verified"])
        rows = self.riemann["dense_core_spike_rows"]
        self.assertEqual(
            [row["operator_norm"] for row in rows], [2, 4, 8, 16, 32, 64]
        )

    def test_complete_space_witness_has_finite_norm_and_divergent_values(self) -> None:
        rows = self.riemann["all_space_failure_witness_rows"]
        self.assertEqual(
            [row["quadratic_value_q_n_x"] for row in rows], list(range(1, 13))
        )
        self.assertTrue(all(row["partial_norm_square_below_two"] for row in rows))
        row = all_space_witness_row(20)
        self.assertLess(Fraction(row["partial_norm_square"]["exact"]), 2)
        self.assertEqual(row["quadratic_value_q_n_x"], 20)

    def test_boundary_formula_matches_recurrence(self) -> None:
        for horizon in [9, 10, 12, 16, 22]:
            tails = list(itertools.islice(itertools.combinations(range(1, horizon), 8), 5))
            for tail in tails:
                positions = (0,) + tail
                position_set = set(positions)
                word = tuple(
                    1 if index in position_set else 2
                    for index in range(horizon)
                )
                self.assertEqual(
                    nine_one_boundary_numerator(horizon, positions),
                    ordered_affine_numerator(word),
                )

    def test_nine_one_mitm_covers_full_finite_range(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(22, 35)))
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))
        self.assertTrue(
            all(
                row["represented_word_count"] == row["expected_word_count"]
                and row["left_tuple_count"] == row["expected_left_tuple_count"]
                and row["right_tuple_count"] == row["expected_right_tuple_count"]
                for row in rows
            )
        )
        total = sum(row["represented_word_count"] for row in rows)
        self.assertEqual(total, 52_157_326)
        self.assertEqual(total, math.comb(34, 9) - math.comb(21, 9))

    def test_nine_one_product_bound_closes_larger_horizons(self) -> None:
        self.assertGreater(nine_one_product_bound(34), 1)
        self.assertLess(nine_one_product_bound(35), 1)
        self.assertTrue(
            all(
                nine_one_product_bound(horizon + 1)
                < nine_one_product_bound(horizon)
                for horizon in range(35, 256)
            )
        )
        self.assertEqual(
            self.collatz["aggregate"]["finite_exception_word_count"],
            52_157_326,
        )

    def test_mitm_transcript_is_deterministic(self) -> None:
        first = finite_nine_one_horizon_row(22)
        second = finite_nine_one_horizon_row(22)
        self.assertEqual(
            first["mitm_transcript_sha256"], second["mitm_transcript_sha256"]
        )
        self.assertEqual(first["represented_word_count"], math.comb(21, 8))

    def test_power_of_two_contamination_is_exactly_classified(self) -> None:
        self.assertEqual(power_of_two_contamination(6)["ordered_pair_count"], 2)
        self.assertEqual(power_of_two_contamination(8)["ordered_pair_count"], 1)
        self.assertEqual(power_of_two_contamination(10)["ordered_pair_count"], 2)
        self.assertEqual(power_of_two_contamination(12)["ordered_pair_count"], 2)
        self.assertEqual(power_of_two_contamination(14)["ordered_pair_count"], 0)
        self.assertTrue(
            all(
                power_of_two_contamination(target)["at_most_two_ordered_pairs"]
                for target in range(6, 1000, 2)
            )
        )

    def test_goldbach_parity_envelope_is_sharper_and_finite_only(self) -> None:
        rows = self.goldbach["parity_envelope_rows"]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(all(row["base_compression"]["checks"].values()) for row in rows)
        )
        self.assertTrue(
            all(
                row["parity_separated_envelope"]
                < row["ticket192_weighted_envelope"]
                for row in rows
            )
        )
        self.assertEqual(
            self.goldbach["aggregate"]["finite_sample_envelope_success_count"],
            len(rows),
        )
        self.assertFalse(self.goldbach["aggregate"]["all_large_even_targets_proved"])

    def test_twin_odd_only_envelope_is_sharper_and_finite_only(self) -> None:
        rows = self.twin["finite_dyadic_rows"]
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(all(row["base_compression"]["checks"].values()) for row in rows)
        )
        self.assertTrue(
            all(
                row["odd_local_contamination_envelope"]
                <= row["ticket192_local_weighted_envelope"]
                for row in rows
            )
        )
        self.assertTrue(
            self.twin["aggregate"][
                "even_supported_pairs_excluded_for_all_X_ge_4"
            ]
        )
        self.assertFalse(
            self.twin["aggregate"]["infinitely_many_envelope_successes_proved"]
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_infinite_cycle_stratum_closure_count": 1,
                "parity_sharpened_envelope_count": 2,
                "represented_collatz_word_count": 52_157_326,
                "rejected_or_corrected_route_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_json_contract_has_four_open_attempts(self) -> None:
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket193-everywhere-nineone-parity-envelope.json"
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
