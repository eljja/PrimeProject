from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    AUDIT_KEY,
    SCHEMA,
    build_audit,
    evaluate_homogeneous,
    quadratic_multiply,
    quadratic_power,
    second_prime_in_residue,
    separated_detector,
    unit_powers_seventeen,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket254DiagonalWeightedReflectionThueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["new_partial_theorem_count"], 2)
        self.assertEqual(machine["exact_no_go_count"], 2)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in (
                "riemann", "collatz", "goldbach", "twin_prime"
            )],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )
        self.assertTrue(all(
            self.root[key]["problem_status"] == "open_not_proven"
            for key in ("riemann", "collatz", "goldbach", "twin_prime")
        ))

    def test_riemann_positive_diagonal_counterexample(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "0be64af7360d626405108d0fee5944f6132fdb6065fd57690c657f3e160df05c",
        )
        for row in computation["exact_block_operator_rows"]:
            dimension = row["block_dimension_L"]
            diagonal = Fraction(row["fourier_diagonal"]["exact"])
            off_diagonal = Fraction(row["common_off_diagonal"]["exact"])
            packet_energy = diagonal + (dimension - 1) * off_diagonal
            self.assertEqual(diagonal, 1)
            self.assertEqual(packet_energy, 0)
            self.assertEqual(
                Fraction(row["orthogonal_complement_eigenvalue"]["exact"]),
                Fraction(dimension, dimension - 1),
            )
        self.assertFalse(computation["aggregate"]["actual_weil_form_analyzed"])

    def test_collatz_nonnegative_weighted_identity(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "6ce9f4399b2372016d2c0bb7d9aa02e8bc14b7b5ee124687ba55c6f76638be46",
        )
        for prime in (7, 11, 47):
            self.assertEqual(separated_detector(prime, 3, 5), 1)
            self.assertEqual(separated_detector(prime, 1, 1), 0)
            self.assertEqual(separated_detector(prime, 0, 0), 0)
        for row in computation["exact_nonnegative_weighted_rows"]:
            self.assertEqual(
                Fraction(row["weighted_complete_detector_sum"]["exact"]),
                Fraction(row["weighted_incidence_sum"]["exact"]),
            )
        self.assertFalse(
            computation["aggregate"]["signed_incomplete_character_route_rejected"]
        )

    def test_goldbach_even_reflection_exclusion(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "253518284e5b939aa42449fd309978e3fe0c7bda7d83944ee96217eed38394f6",
        )
        rows = computation["exact_even_reflection_exclusion_rows"]
        self.assertEqual(len(rows), 50)
        for row in rows:
            q = row["prime_modulus_q"]
            m = row["even_cyclotomic_exponent_m"]
            residue = m % q
            coefficients = cyclic_binomial_coefficients(q, m)
            first, second, index = second_prime_in_residue(q, residue)
            self.assertEqual(m % 2, 0)
            self.assertNotEqual(residue, 0)
            self.assertEqual(coefficients[residue], coefficients[0])
            self.assertEqual(row["forced_count_at_reflected_residue"], 1)
            self.assertEqual(
                (row["first_prime_in_reflected_residue"], row["second_prime_in_reflected_residue"], row["global_index_of_second_residue_prime"]),
                (first, second, index),
            )
            self.assertGreaterEqual(row["forced_total_prime_count_T"], index)
            self.assertTrue(row["unique_prime_prefix_excluded"])
        self.assertEqual(rows[0]["prime_modulus_q"], 5)
        self.assertEqual(rows[0]["even_cyclotomic_exponent_m"], 8)
        self.assertFalse(
            computation["aggregate"]["odd_or_q_divisible_compatible_tails_excluded"]
        )

    def test_twin_seventeen_thue_reduction_audit(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "1cc60a2de6cbf63644bb1751a558602cdf696651b181a1a14606b62ec457fcf3",
        )
        rows = computation["exact_unit_twisted_thue_polynomials"]
        units = unit_powers_seventeen()
        self.assertEqual(len(rows), 17)
        for row, unit in zip(rows, units, strict=True):
            self.assertEqual(
                (row["unit_rational_part_a_j"], row["unit_sqrt2_part_b_j"]),
                unit,
            )
            for u, v in ((1, 0), (0, 1), (2, -1), (-3, 2)):
                direct = quadratic_multiply(unit, quadratic_power((u, v), 17))
                evaluated = (
                    evaluate_homogeneous(row["A_j_coefficients_for_u_power_17_minus_k_v_power_k"], u, v),
                    evaluate_homogeneous(row["B_j_coefficients_for_u_power_17_minus_k_v_power_k"], u, v),
                )
                self.assertEqual(evaluated, direct)
        finite = computation["finite_box_audit"]
        self.assertEqual(finite["exact_grid_case_count"], 10608)
        self.assertEqual(finite["coefficient_one_point_count"], 2)
        self.assertEqual(finite["admissible_positive_point_count"], 0)
        self.assertTrue(all(point["reduced_y"] < 0 for point in finite["coefficient_one_points"]))
        self.assertFalse(computation["aggregate"]["all_seventeen_thue_equations_solved"])

    def test_proof_dags(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            nodes = dag["nodes"]
            ids = {node["id"] for node in nodes}
            self.assertEqual(len(ids), len(nodes))
            self.assertTrue(all(node["status"] in ALLOWED for node in nodes))
            self.assertEqual(sum(node["status"] == "open" for node in nodes), 1)
            adjacency = {node_id: [] for node_id in ids}
            indegree = {node_id: 0 for node_id in ids}
            for source, target in dag["edges"]:
                self.assertIn(source, ids)
                self.assertIn(target, ids)
                adjacency[source].append(target)
                indegree[target] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                source = queue.pop()
                visited += 1
                for target in adjacency[source]:
                    indegree[target] -= 1
                    if indegree[target] == 0:
                        queue.append(target)
            self.assertEqual(visited, len(nodes))

    def test_committed_outputs_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket254-diagonal-weighted-reflection-thue.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["ticket"], 254)
        self.assertEqual(state["parent_ticket"], 253)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "goldbach")
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))


if __name__ == "__main__":
    unittest.main()
