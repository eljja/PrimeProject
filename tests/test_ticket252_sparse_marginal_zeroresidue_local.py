from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket252_sparse_marginal_zeroresidue_local import (
    AUDIT_KEY,
    SCHEMA,
    build_audit,
    cyclic_binomial_coefficients,
    is_prime,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket252SparseMarginalZeroResidueLocalTests(unittest.TestCase):
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
        self.assertEqual(machine["new_partial_theorem_count"], 1)
        self.assertEqual(machine["exact_no_go_count"], 3)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in (
                "riemann", "collatz", "goldbach", "twin_prime"
            )],
            ["exact_no_go", "exact_no_go", "partial_theorem", "exact_no_go"],
        )
        self.assertTrue(all(
            self.root[key]["problem_status"] == "open_not_proven"
            for key in ("riemann", "collatz", "goldbach", "twin_prime")
        ))

    def test_riemann_sparse_projection_bounds(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "3e7c26600452d330e977e7880ca71b028709cad8966df6c63c41be6a1e910294",
        )
        rows = computation["exact_sparse_projection_rows"]
        self.assertEqual(len(rows), 12)
        combined = [Fraction(row["proved_combined_upper"]["exact"]) for row in rows]
        self.assertTrue(all(right < left for left, right in zip(combined, combined[1:])))
        for row in rows:
            delta = Fraction(row["delta"]["exact"])
            s = row["delta_power"]
            self.assertEqual(
                Fraction(row["proved_low_frequency_energy_upper"]["exact"]),
                2 * delta * (s + 1),
            )
            self.assertEqual(
                Fraction(row["proved_tail_energy_upper_using_pi_squared_gt_9"]["exact"]),
                2 * delta / 27,
            )
        self.assertTrue(computation["aggregate"]["operator_positive_selfadjoint_noncompact_proved"])
        self.assertFalse(computation["aggregate"]["actual_weil_kernel_controlled"])

    def test_collatz_uniform_marginal_countermodels(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "d134c93741ae3151e80bc4443e7abbbbab5ba578292ade37cef147e17cfb324c",
        )
        rows = computation["exact_uniform_marginal_countermodel_rows"]
        self.assertEqual(len(rows), 11)
        for row in rows:
            q = row["prime_q"]
            self.assertTrue(row["each_of_four_marginals_is_exactly_uniform"])
            self.assertEqual(row["hit_graph_separated_target_count"], q - 1)
            self.assertEqual(row["miss_graph_separated_target_count"], 0)
            self.assertEqual(Fraction(row["hit_graph_target_mass"]["exact"]), Fraction(q - 1, q))
        self.assertFalse(computation["aggregate"]["canonical_fixed_pair_distribution_controlled"])

    def test_goldbach_zero_residue_criterion_and_tail_counterexample(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "5c95a4a8bf5019dc499a4fc45abcd82b1c10ede06659f59d0d28ee036eb06717",
        )
        rows = computation["exact_zero_residue_criterion_rows"]
        self.assertEqual(len(rows), 68)
        for row in rows:
            q, m = row["prime_modulus_q"], row["exponent_m"]
            c = row["cyclic_coefficients_c"]
            self.assertEqual(c, cyclic_binomial_coefficients(q, m))
            self.assertEqual(row["c0_minus_min_c"], c[0] - min(c))
            self.assertEqual(row["zero_residue_compatibility"], c[0] - min(c) <= 1)
            if m < q:
                self.assertTrue(row["low_degree_m_less_than_q_excluded"])
        witness = next(
            row for row in rows
            if row["prime_modulus_q"] == 5 and row["exponent_m"] == 8
        )
        self.assertEqual(witness["cyclic_coefficients_c"], [-55, 20, 20, -55, 70])
        self.assertEqual(witness["compatible_nonnegative_integer_vector"], [1, 76, 76, 1, 126])
        self.assertTrue(computation["aggregate"]["all_low_degree_m_less_than_q_excluded"])
        self.assertTrue(computation["aggregate"]["zero_residue_only_global_exclusion_refuted"])
        self.assertFalse(computation["aggregate"]["actual_prime_count_vectors_fully_excluded"])

    def test_twin_finite_modulus_prime_residue_certificates(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "079a60fde7d3f69814681f455edadebbe8b8d0aaf199e7821a0dad94d3ee02b4",
        )
        rows = computation["exact_finite_modulus_rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            M = row["modulus_M"]
            p, r = row["prime_p_minus_one_class"], row["prime_r_plus_one_class"]
            k, m = row["odd_left_exponent_k"], row["right_half_exponent_m"]
            self.assertTrue(is_prime(p) and is_prime(r) and p != r)
            self.assertEqual(p % 8, 7)
            self.assertEqual(k % 2, 1)
            self.assertEqual((pow(p, k, M) + 2 - pow(r, 2 * m, M)) % M, 0)
            self.assertTrue(row["certificate_verified"])
        self.assertFalse(computation["aggregate"]["global_integer_equation_solved"])

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
        twin_nodes = self.root["twin_prime"]["proof_dag"]["nodes"]
        self.assertEqual(sum(node["status"] == "external_theorem" for node in twin_nodes), 1)

    def test_committed_outputs_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket252-sparse-marginal-zeroresidue-local.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["ticket"], 252)
        self.assertEqual(state["parent_ticket"], 251)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "goldbach")
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))


if __name__ == "__main__":
    unittest.main()
