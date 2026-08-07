from __future__ import annotations

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

from ticket195_finitejet_elevenone_squarelayer import (  # noqa: E402
    ELEVEN_ONES,
    analytic_tail_start,
    boundary_numerator,
    build_audit,
    contracting_start,
    finite_even_jet_ambiguity_row,
    fixed_one_product_bound,
    fixed_stratum_decidability_row,
    rouche_unit_disk_row,
)
from ticket180_finite_information_localization import (  # noqa: E402
    ordered_affine_numerator,
)


class Ticket195FiniteJetElevenOneSquareLayerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket195-finitejet-elevenone-squarelayer.json"
            ).read_text(encoding="utf-8")
        )

    def test_finite_even_jet_extension_forces_nonreal_root_exactly(self) -> None:
        for order in range(13):
            row = finite_even_jet_ambiguity_row(order)
            self.assertEqual(row["matched_through_degree"], 2 * order)
            self.assertEqual(
                row["extended_polynomial_value_at_i"]["numerator"], 0
            )
            self.assertEqual(row["forced_nonreal_roots"], ["i", "-i"])

    def test_rouche_synthetic_margin_is_strict_and_exact(self) -> None:
        for order in range(1, 13):
            row = rouche_unit_disk_row(order)
            margin = Fraction(
                row["strict_rouche_margin"]["numerator"],
                row["strict_rouche_margin"]["denominator"],
            )
            self.assertGreater(margin, 0)
            self.assertEqual(row["certified_zero_count_inside"], 0)

    def test_fixed_one_count_strata_have_finite_decision_ranges(self) -> None:
        for one_count in range(1, 33):
            row = fixed_stratum_decidability_row(one_count)
            start = row["contracting_range_starts_at_h"]
            tail = row["analytic_exclusion_starts_at_h"]
            self.assertEqual(start, contracting_start(one_count))
            self.assertEqual(tail, analytic_tail_start(one_count))
            self.assertLess(start, tail)
            self.assertTrue(row["finite_decision_range_is_finite"])

    def test_eleven_one_boundary_formula_matches_direct_recurrence(self) -> None:
        samples = [
            (27, tuple(range(11))),
            (31, (0, 2, 4, 7, 10, 13, 16, 19, 23, 27, 30)),
            (41, (0, 1, 5, 9, 13, 17, 21, 25, 30, 35, 40)),
        ]
        for horizon, positions in samples:
            position_set = set(positions)
            word = tuple(
                1 if index in position_set else 2 for index in range(horizon)
            )
            self.assertEqual(
                boundary_numerator(ELEVEN_ONES, horizon, positions),
                ordered_affine_numerator(word),
            )
        validation = self.audit["collatz"]["reproducible_computation"][
            "boundary_formula_validation"
        ]
        self.assertEqual(validation["formula_mismatch_count"], 0)
        self.assertGreater(validation["normalized_words_checked"], 10000)

    def test_eleven_one_mitm_is_complete_and_has_no_hit(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        rows = computation["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(27, 42)))
        self.assertTrue(all(row["coverage_matches_binomial_count"] for row in rows))
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))
        aggregate = computation["aggregate"]
        self.assertEqual(aggregate["finite_exception_word_count"], 3151735808)
        self.assertEqual(
            aggregate["finite_exception_word_count"],
            math.comb(41, 11) - math.comb(26, 11),
        )
        self.assertEqual(aggregate["left_tuple_count"], 4266158)
        self.assertEqual(aggregate["right_tuple_count"], 1893528)

    def test_eleven_one_product_bound_closes_infinite_tail(self) -> None:
        self.assertGreaterEqual(fixed_one_product_bound(11, 41), 1)
        self.assertLess(fixed_one_product_bound(11, 42), 1)
        self.assertEqual(contracting_start(11), 27)
        self.assertEqual(analytic_tail_start(11), 42)

    def test_goldbach_square_and_higher_layers_reconstruct_exact_mass(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        for row in computation["prime_square_layer_rows"]:
            self.assertTrue(row["checks"]["split_reconstructs_theta_mass"])
            self.assertTrue(row["checks"]["theta_mass_matches_direct_mass"])
            self.assertTrue(
                row["checks"]["actual_contamination_below_full_envelope"]
            )
        witness = computation["cube_support_no_go_witness"]
        self.assertEqual(sum(witness["ordered_pair"]), witness["target_N"])
        self.assertEqual(witness["left_prime_power"], {"base": 3, "exponent": 3})

    def test_twin_square_and_higher_interval_layers_reconstruct_mass(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        for row in computation["finite_dyadic_rows"]:
            self.assertTrue(row["checks"]["left_split_matches_direct_mass"])
            self.assertTrue(row["checks"]["right_split_matches_direct_mass"])
            self.assertTrue(
                row["checks"]["actual_contamination_below_full_envelope"]
            )
        witness = computation["cube_support_no_go_witness"]
        self.assertEqual(witness["shift_two_pair"], [27, 29])
        self.assertEqual(witness["dyadic_block"], [16, 32])

    def test_all_four_attempts_remain_open(self) -> None:
        attempts = self.payload["attempts"]
        self.assertEqual(len(attempts), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        self.assertTrue(all(attempt["status"] == "open_not_proven" for attempt in attempts))
        self.assertTrue(all(attempt["candidate_theorem"] for attempt in attempts))

    def test_machine_contract_has_zero_resolution_and_failure(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["represented_collatz_word_count"], 3151735808)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
