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
from ticket194_densecore_tenone_theta_layers import (  # noqa: E402
    build_audit,
    exact_binary_mass_classification,
    integer_kth_root,
    monotone_dense_core_no_go_row,
    ten_one_boundary_numerator,
    ten_one_product_bound,
)


class Ticket194DenseCoreTenOneThetaLayersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_uniform_dense_core_extension_contract(self) -> None:
        contract = self.riemann["extension_contract"]
        self.assertTrue(
            contract["uniform_bound_plus_dense_core_convergence_extends_everywhere"]
        )
        self.assertTrue(contract["positivity_passes_to_limit"])
        self.assertFalse(
            contract[
                "positive_monotone_dense_core_convergence_alone_is_sufficient"
            ]
        )
        self.assertFalse(contract["actual_weil_uniform_bound_verified"])
        self.assertFalse(contract["actual_weil_dense_core_convergence_verified"])

    def test_positive_monotone_core_no_go_has_l2_witness(self) -> None:
        rows = self.riemann["positive_monotone_dense_core_no_go_rows"]
        self.assertEqual(
            [row["witness_quadratic_value"] for row in rows],
            list(range(1, 13)),
        )
        row = monotone_dense_core_no_go_row(20)
        self.assertLess(Fraction(row["witness_partial_norm_square"]["exact"]), 1)
        self.assertEqual(row["operator_norm"], 2**20)
        self.assertEqual(row["witness_quadratic_value"], 20)

    def test_integer_kth_root_is_exact_at_boundaries(self) -> None:
        for base in range(2, 40):
            for exponent in range(2, 9):
                power = base**exponent
                self.assertEqual(integer_kth_root(power, exponent), base)
                self.assertEqual(integer_kth_root(power - 1, exponent), base - 1)
                self.assertEqual(integer_kth_root(power + base, exponent), base)

    def test_ten_one_boundary_formula_matches_recurrence(self) -> None:
        for horizon in [10, 11, 13, 16, 25]:
            tails = itertools.islice(
                itertools.combinations(range(1, horizon), 9), 7
            )
            for tail in tails:
                positions = (0,) + tail
                position_set = set(positions)
                word = tuple(
                    1 if index in position_set else 2
                    for index in range(horizon)
                )
                self.assertEqual(
                    ten_one_boundary_numerator(horizon, positions),
                    ordered_affine_numerator(word),
                )

    def test_ten_one_mitm_covers_every_finite_exception_word(self) -> None:
        rows = self.collatz["finite_exception_horizon_rows"]
        self.assertEqual([row["horizon_h"] for row in rows], list(range(25, 39)))
        self.assertTrue(all(row["contracting"] for row in rows))
        self.assertTrue(all(row["divisibility_hit_count"] == 0 for row in rows))
        self.assertTrue(
            all(
                row["represented_word_count"] == row["expected_word_count"]
                for row in rows
            )
        )
        aggregate = self.collatz["aggregate"]
        self.assertEqual(aggregate["finite_exception_word_count"], 470_772_500)
        self.assertEqual(aggregate["left_tuple_count"], 2_626_085)
        self.assertEqual(aggregate["right_tuple_count"], 225_708)

    def test_ten_one_product_bound_closes_the_infinite_tail(self) -> None:
        self.assertGreater(ten_one_product_bound(38), 1)
        self.assertLess(ten_one_product_bound(39), 1)
        self.assertTrue(
            all(
                row["strictly_below_one"]
                for row in self.collatz["analytic_product_rows"]
            )
        )

    def test_binary_power_pair_classification(self) -> None:
        expected = {
            6: 2,
            8: 1,
            10: 2,
            12: 2,
            14: 0,
            16: 1,
            18: 2,
            20: 2,
            22: 0,
            24: 2,
            26: 0,
            28: 0,
            30: 0,
            32: 1,
            34: 2,
            36: 2,
            40: 2,
            42: 0,
            48: 2,
            60: 0,
        }
        for target, expected_count in expected.items():
            row = exact_binary_mass_classification(target)
            self.assertEqual(row["ordered_pair_count"], expected_count)
            self.assertTrue(row["classification_matches_direct_enumeration"])

    def test_goldbach_theta_layers_reconstruct_exact_mass(self) -> None:
        rows = self.goldbach["theta_layer_rows"]
        self.assertEqual(len(rows), 11)
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertEqual(
            self.goldbach["aggregate"]["contamination_scale"],
            "O(sqrt(N) log(N))",
        )
        self.assertFalse(self.goldbach["aggregate"]["all_large_even_targets_proved"])

    def test_twin_interval_theta_layers_reconstruct_exact_mass(self) -> None:
        rows = self.twin["finite_dyadic_rows"]
        self.assertEqual(len(rows), 16)
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertEqual(
            self.twin["aggregate"]["contamination_scale"],
            "O(sqrt(X) log(X))",
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
                "theta_layer_identity_count": 2,
                "represented_collatz_word_count": 470_772_500,
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
            / "ticket194-densecore-tenone-theta-layers.json"
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
