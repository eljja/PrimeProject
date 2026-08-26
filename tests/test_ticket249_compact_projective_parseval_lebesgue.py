from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket249_compact_projective_parseval_lebesgue import (
    AUDIT_KEY,
    SCHEMA,
    build_audit,
    fermat_quotient_residue,
    generalized_wieferich_residue,
    root_sum,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_NODE_STATUSES = {
    "proved",
    "disproved",
    "computed_finite",
    "external_theorem",
    "assumption",
    "heuristic",
    "open",
}


class Ticket249CompactProjectiveParsevalLebesgueTests(unittest.TestCase):
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
        self.assertEqual(machine["new_partial_theorem_count"], 2)
        self.assertEqual(machine["exact_no_go_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "partial_theorem", "exact_no_go", "partial_theorem"],
        )
        self.assertTrue(
            all(
                self.root[key]["problem_status"] == "open_not_proven"
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            )
        )

    def test_riemann_compact_escape_rows(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "eaaa5e2eccd9fa1fcb32504240f86c5ecff7d815eb4d218a5eb22e9248bb999a",
        )
        rows = computation["exact_finite_rank_rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            partial = Fraction(row["exact_partial_unweighted_energy"]["exact"])
            bound = Fraction(row["proved_all_moment_energy_bound"]["exact"])
            self.assertLessEqual(partial, bound)
            self.assertEqual(row["exact_projection_energy"]["exact"], "0/1")
            self.assertTrue(row["certificate_verified"])
        self.assertEqual(rows[-1]["half_degree_n"], 256)
        self.assertEqual(rows[-1]["proved_all_moment_energy_bound"]["exact"], "11/256")
        self.assertTrue(
            computation["aggregate"]["compact_offdiagonal_coercivity_no_go_proved"]
        )
        self.assertFalse(
            computation["aggregate"]["noncompact_arithmetic_offdiagonal_control_proved"]
        )

    def test_collatz_projective_slope_and_scan(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "db860c5bef6ae1b016d468346b1b9941eac90c375f93d4f7c4f67c8ee8e881b7",
        )
        scan = computation["exact_modular_scan"]
        self.assertEqual(scan["primes_checked"], 664_576)
        self.assertEqual(scan["W_32_27_zero_primes"], [])
        self.assertEqual(scan["W_2_3_zero_primes"], [23])
        self.assertEqual(scan["separated_bad_primes"], [])
        for q in (7, 11, 23, 101, 1009):
            u = fermat_quotient_residue(2, q)
            v = fermat_quotient_residue(3, q)
            self.assertEqual(
                generalized_wieferich_residue(32, 27, q),
                (5 * u - 3 * v) % q,
            )
            self.assertEqual(
                generalized_wieferich_residue(2, 3, q), (u - v) % q
            )
        self.assertEqual(
            [row["nonzero_projective_pairs"] for row in computation["exact_finite_field_rows"]],
            [6, 10, 22, 100],
        )

    def test_goldbach_exact_group_ring_spikes(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "439a6562998de91c99533ceacb5ac53d177af9e48165ee51c4eed6ec782d59fe",
        )
        self.assertEqual(
            computation["exact_group_ring_replay"]["reduced_frequency_cases"],
            5_020,
        )
        self.assertEqual(root_sum(17, 34), 17)
        self.assertEqual(root_sum(17, 35), 0)
        rows = computation["exact_selected_spike_rows"]
        self.assertEqual(len(rows), 13)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            all(row["spike_to_total_ratio_squared"]["exact"] == "1/2" for row in rows)
        )
        self.assertEqual(rows[-1]["nonzero_numerators"], [1, 127])
        self.assertTrue(
            computation["aggregate"]["abstract_mean_square_to_uniform_route_refuted"]
        )
        self.assertFalse(
            computation["aggregate"]["actual_prime_count_vector_counterexample_claimed"]
        )

    def test_twin_even_left_classification(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "6df796f1387e44725a337fc60d5fe44a94e2521496caf1cdc39e30bba96f6fd9",
        )
        rows = computation["exact_scale_rows"]
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            all(row["left_even_exponent_base_not_3"] == 1 for row in rows)
        )
        last = rows[-1]
        self.assertEqual(last["left_active_composite_pairs_L"], 14)
        self.assertEqual(last["left_even_exponent_base_3"], 5)
        self.assertEqual(last["left_odd_exponent"], 8)
        self.assertEqual(last["right_active_composite_pairs_R"], 136)
        witnesses = computation["selected_left_active_witnesses"]
        exceptional = [
            row
            for row in witnesses
            if row["category"] == "even_exponent_base_not_3"
        ]
        self.assertEqual(
            [(row["n"], row["n_plus_2"]) for row in exceptional], [(25, 27)]
        )
        self.assertEqual(
            computation["external_theorem"]["modern_primary_source"],
            "https://doi.org/10.1112/S0010437X05001739",
        )

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            nodes = dag["nodes"]
            ids = {node["id"] for node in nodes}
            self.assertEqual(len(ids), len(nodes))
            self.assertTrue(
                all(node["status"] in ALLOWED_NODE_STATUSES for node in nodes)
            )
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

    def test_committed_integrated_json_matches_generator(self) -> None:
        path = ROOT / "data/open-problem/ticket249-compact-projective-parseval-lebesgue.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(state["ticket"], 249)
        self.assertEqual(state["parent_ticket"], 248)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "twin_prime")
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
