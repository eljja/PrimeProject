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

from ticket184_information_sufficiency_route_correction import (  # noqa: E402
    build_audit,
    cantelli_lower_tail,
    composite_impostor_row,
    goldbach_wheel_row,
    minimal_cycle_prefix_barrier,
    moment_canceling_abel_row,
    twin_cantelli_sharp_row,
)


class Ticket184InformationSufficiencyRouteCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.riemann = cls.audit["riemann"]["reproducible_computation"]
        cls.collatz = cls.audit["collatz"]["reproducible_computation"]
        cls.goldbach = cls.audit["goldbach"]["reproducible_computation"]
        cls.twin = cls.audit["twin_prime"]["reproducible_computation"]

    def test_finite_difference_family_cancels_every_declared_moment(self) -> None:
        for order in [1, 2, 4, 8]:
            row = moment_canceling_abel_row(order, 64, 0.9)
            self.assertEqual(row["cancelled_moment_numerators"], [0] * order)
            self.assertEqual(row["original_uniform_norm"], 1.0)

    def test_finite_moments_do_not_prevent_abel_hidden_unit_mass(self) -> None:
        low = moment_canceling_abel_row(8, 16, 0.9)
        high = moment_canceling_abel_row(8, 64, 0.9)
        self.assertLess(high["abel_uniform_norm"], low["abel_uniform_norm"])
        self.assertGreater(high["desmoothing_distance_lower_bound"], 0.999)
        self.assertEqual(self.riemann["failure_count"], 0)

    def test_minimal_cycle_prefix_barrier_is_not_sufficient(self) -> None:
        row = minimal_cycle_prefix_barrier((1, 3))
        self.assertTrue(row["prefix_barrier_passes"])
        self.assertEqual(row["affine_numerator_B"], 5)
        self.assertEqual(row["cycle_denominator_D"], 7)
        self.assertFalse(row["affine_divisibility_hit"])

    def test_collatz_cycle_branch_is_separate_from_divergence_branch(self) -> None:
        self.assertIn("unbounded", self.collatz["theorem"])
        self.assertIn("still leave the divergent", self.collatz["no_go_scope"])
        finite = self.collatz["finite_first_descent_diagnostic"]
        self.assertEqual(finite["odd_start_limit"], 1_000_000)
        self.assertEqual(finite["unresolved_starts"], [])
        self.assertGreater(finite["maximum_first_descent_steps"], 0)

    def test_prefix_barrier_no_go_has_many_exact_witnesses(self) -> None:
        aggregate = self.collatz["aggregate"]
        self.assertEqual(
            aggregate["prefix_barrier_passes"],
            aggregate["barrier_without_divisibility"],
        )
        self.assertGreater(aggregate["barrier_without_divisibility"], 1_000)

    def test_squarefree_wheel_factorization_is_exact(self) -> None:
        row = goldbach_wheel_row(3 * 5 * 7 * 11)
        self.assertEqual(row["factorization_mismatches"], [])
        self.assertGreater(row["minimum_local_representation_count"], 0)

    def test_composite_impostor_matches_every_unit_residue(self) -> None:
        row = composite_impostor_row(1155)
        self.assertEqual(row["unit_residue_count"], 480)
        self.assertEqual(row["composite_representative_count"], 480)
        self.assertTrue(all(row["checks"].values()))

    def test_cantelli_bound_and_sharp_family(self) -> None:
        generic = cantelli_lower_tail([0.5, 0.5], [0.0, 1.0], 0.5)
        self.assertLessEqual(
            generic["actual_lower_tail_mass"], generic["cantelli_upper_bound"]
        )
        sharp = twin_cantelli_sharp_row(12)
        self.assertTrue(all(sharp["checks"].values()))
        self.assertTrue(
            math.isclose(
                sharp["actual_lower_tail_mass"],
                sharp["cantelli_upper_bound"],
                abs_tol=1e-15,
            )
        )

    def test_twin_root_target_is_weaker_than_every_leaf_target(self) -> None:
        finite = self.twin["finite_prime_pair_root_diagnostic"]
        self.assertGreater(finite["root_actual_to_expected_ratio"], 0.0)
        self.assertGreater(finite["actual_twin_pair_count"], 0)
        self.assertFalse(finite["all_leaf_certificates_pass"])
        self.assertTrue(finite["root_positive_implies_at_least_one_pair"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["decisive_route_correction_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_json_contract_and_proof_dags(self) -> None:
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket184-information-sufficiency-route-correction.json"
        )
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(item["status"] == "open_not_proven" for item in payload["attempts"])
        )
        self.assertNotIn(": Infinity", text)
        self.assertNotIn(": -Infinity", text)
        self.assertNotIn(": NaN", text)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[section_name]["proof_dag"]["nodes"]
            self.assertEqual(nodes[0]["status"], "proved_exact_input")
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_next_lemmas_are_single_and_problem_specific(self) -> None:
        next_lemmas = {
            self.audit[name]["route_decision"]["next_single_lemma"]
            for name in ["riemann", "collatz", "goldbach", "twin_prime"]
        }
        self.assertEqual(len(next_lemmas), 4)
        self.assertTrue(all(" " not in lemma for lemma in next_lemmas))


if __name__ == "__main__":
    unittest.main()
