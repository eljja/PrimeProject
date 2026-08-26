from __future__ import annotations

import json
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    AUDIT_KEY,
    SCHEMA,
    build_audit,
    crt,
    cyclic_binomial_coefficients,
    fermat_quotient,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_NODE_STATUSES = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket251InteriorCrtCyclotomicRightEvenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary_and_classifications(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["new_partial_theorem_count"], 1)
        self.assertEqual(machine["exact_no_go_count"], 3)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in (
                "riemann", "collatz", "goldbach", "twin_prime"
            )],
            ["exact_no_go", "exact_no_go", "exact_no_go", "partial_theorem"],
        )
        self.assertTrue(all(
            self.root[key]["problem_status"] == "open_not_proven"
            for key in ("riemann", "collatz", "goldbach", "twin_prime")
        ))

    def test_riemann_interior_zero_concentration(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "e79a0c6278dedf06d33bbd79125d059adf86c1f2ae1f252afbae78daf5d3ffcd",
        )
        rows = computation["exact_interior_concentration_rows"]
        self.assertEqual(len(rows), 11)
        bounds = [Fraction(row["proved_combined_upper"]["exact"]) for row in rows]
        self.assertTrue(all(right < left for left, right in zip(bounds, bounds[1:])))
        self.assertEqual(
            rows[-1]["proved_combined_upper"]["exact"],
            "7219763056826388766606490402087/14603067372660366226321778266865664",
        )
        self.assertTrue(computation["aggregate"]["noncompactness_proved"])
        self.assertFalse(computation["aggregate"]["actual_weil_form_controlled"])

    def test_collatz_crt_interpolation(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "c184a69eaebae32ffdc9e9043ca4864bf7615e5933a225721616dcda732e2fdc",
        )
        self.assertEqual(crt([1, 2], [3, 5]), (7, 15))
        rows = computation["exact_CRT_interpolation_rows"]
        self.assertEqual(len(rows), 4)
        for row in rows:
            A, B = row["least_nonnegative_A"], row["least_nonnegative_B"]
            for local in row["local_constraints"]:
                q = local["prime_q"]
                self.assertEqual(A % q, 2)
                self.assertEqual(B % q, 3)
                self.assertEqual(fermat_quotient(A, q), local["target_u"])
                self.assertEqual(fermat_quotient(B, q), local["target_v"])
        self.assertFalse(computation["aggregate"]["canonical_fixed_pair_distribution_controlled"])

    def test_goldbach_cyclotomic_family(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "e3c9e81aab8500e964f265aa6ba8bd91105d40f67e1f5c7938f63bb88bcaa857",
        )
        self.assertEqual(cyclic_binomial_coefficients(5, 2), [1, -2, 1, 0, 0])
        rows = computation["exact_cyclotomic_unit_rows"]
        self.assertEqual(len(rows), 32)
        for row in rows:
            q, m = row["prime_modulus_q"], row["exponent_m"]
            self.assertEqual(sum(row["cyclic_coefficients_c"]), 0)
            self.assertTrue(all(value >= 0 for value in row["nonnegative_counts_n"]))
            self.assertEqual(int(row["exact_galois_norm"]), q ** (q - 1 + m))
            self.assertTrue(row["certificate_verified"])
        for q in (5, 7, 11, 13):
            upper = [Decimal(row["outside_pair_to_max_pair_energy_upper_display"]) for row in rows if row["prime_modulus_q"] == q]
            self.assertTrue(all(right < left for left, right in zip(upper, upper[1:])))
        self.assertTrue(computation["aggregate"]["structural_only_quantitative_anti_concentration_refuted"])
        self.assertFalse(computation["aggregate"]["actual_prime_count_vectors_excluded_from_family"])

    def test_twin_right_even_modulo_eight_constraint(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "2881e5c20c714c52c8502ea5ec74617bed8bbc110c35069c488e960a4d711e85",
        )
        rows = computation["exact_scale_rows"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[-1]["right_even_active_pair_count"], 124)
        self.assertEqual(rows[-1]["left_exponent_at_least_two_count"], 0)
        witnesses = computation["selected_witnesses"]
        self.assertEqual((witnesses[0]["p_power"], witnesses[0]["right_even_power"]), (7, 9))
        self.assertTrue(all(row["left_exponent_k"] == 1 for row in witnesses))
        self.assertTrue(computation["aggregate"]["right_even_modulo_eight_constraint_proved"])
        self.assertFalse(computation["aggregate"]["modulo_eight_alone_excludes_odd_composite_left_exponents"])
        self.assertEqual(computation["aggregate"]["finite_scan_composite_left_witness_count"], 0)
        self.assertFalse(computation["aggregate"]["withdrawn_source_used_as_dependency"])

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            nodes = dag["nodes"]
            ids = {node["id"] for node in nodes}
            self.assertEqual(len(ids), len(nodes))
            self.assertTrue(all(node["status"] in ALLOWED_NODE_STATUSES for node in nodes))
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
                current = queue.pop()
                visited += 1
                for successor in adjacency[current]:
                    indegree[successor] -= 1
                    if indegree[successor] == 0:
                        queue.append(successor)
            self.assertEqual(visited, len(nodes))

    def test_committed_outputs_match_generator_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket251-interior-crt-cyclotomic-righteven.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["ticket"], 251)
        self.assertEqual(state["parent_ticket"], 250)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "goldbach")
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))
        self.assertNotIn(
            "RightEvenActivePrimePowerClassification",
            state["problems"]["twin_prime"]["established_results"],
        )


if __name__ == "__main__":
    unittest.main()
