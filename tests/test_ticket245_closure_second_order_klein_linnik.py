from __future__ import annotations

import json
import unittest

from scripts.ticket245_closure_second_order_klein_linnik import (
    AUDIT_KEY,
    ROOT,
    SCHEMA,
    build_audit,
    collatz_second_order_audit,
    goldbach_klein_orbit_audit,
    klein_orbit,
    riemann_closure_margin_audit,
    twin_linnik_audit,
)


class Ticket245ClosureSecondOrderKleinLinnikTests(unittest.TestCase):
    def test_riemann_closure_margin_counterfamily(self) -> None:
        audit = riemann_closure_margin_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "5e329477cb0a2f420f406b1b9f94483f36d9026bb1ef22542c31b68ac139cbb1",
        )
        self.assertEqual(
            [row["exact_minimum_Q_on_K_m"]["exact"] for row in audit["exact_exhaustion_margin_rows"]],
            ["1/5", "1/17", "1/65", "1/257", "1/1025", "1/4097"],
        )
        self.assertTrue(audit["aggregate"]["joint_tightness_plus_pointwise_positivity_uniform_margin_refuted"])

    def test_collatz_second_order_digits_and_adversarial_scan(self) -> None:
        audit = collatz_second_order_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "26b7da7bc74a887b9b954122bc61dfc4277277cbde99e063505e8d6ebbd1423f",
        )
        first = audit["adversarial_first_layer_scan"]
        self.assertEqual(first["primes_scanned"], 1_270_604)
        self.assertEqual(first["bad_line_primes"], [])
        self.assertEqual(first["comparison_line_primes"], [23])
        second = audit["second_order_replay"]
        self.assertEqual(second["primes_scanned"], 5_130)
        self.assertEqual(second["failure_count"], 0)
        row23 = next(row for row in audit["selected_exact_second_order_rows"] if row["prime_q"] == 23)
        self.assertTrue(row23["comparison_line_first_layer"])
        self.assertFalse(row23["q_cubed_divides_2_power_minus_3_power"])

    def test_goldbach_klein_orbits(self) -> None:
        audit = goldbach_klein_orbit_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "92774e213632ee5eb153236bafe3c0b03ec914994db4b4b668b22224c52d6639",
        )
        self.assertEqual(len(klein_orbit(__import__("fractions").Fraction(0))), 2)
        self.assertEqual(len(klein_orbit(__import__("fractions").Fraction(1, 4))), 2)
        self.assertEqual(len(klein_orbit(__import__("fractions").Fraction(1, 5))), 4)
        latest = audit["exact_rational_center_orbit_rows"][-1]
        self.assertEqual(latest["seed_denominator_limit_Q"], 128)
        self.assertEqual(latest["canonical_quarter_torus_orbit_count"], 1_882)
        self.assertEqual(latest["orbit_size_two_count"], 2)

    def test_twin_polynomial_height_witnesses(self) -> None:
        audit = twin_linnik_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "9c40a7487d40b111bb2e9ebc9c4bc9cbcf4edaf9ed73d931632d5df78bd32e98",
        )
        rows = audit["exact_polynomial_height_witness_rows"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["successor_factorization"], "3*5*1")
        self.assertEqual(rows[-1]["first_prime_in_crt_class"], 239_904_063_098_717)
        self.assertTrue(all(row["certificate_verified"] for row in rows))

    def test_machine_boundary_and_classifications(self) -> None:
        root = build_audit()[AUDIT_KEY]
        machine = root["machine_audit"]
        self.assertEqual(machine["new_partial_theorem_count"], 2)
        self.assertEqual(machine["exact_no_go_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["exact_no_go", "partial_theorem", "partial_theorem", "exact_no_go"],
        )

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        root = build_audit()[AUDIT_KEY]
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = root[key]["proof_dag"]
            node_ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            adjacency = {node_id: [] for node_id in node_ids}
            indegree = {node_id: 0 for node_id in node_ids}
            for left, right in dag["edges"]:
                self.assertIn(left, node_ids)
                self.assertIn(right, node_ids)
                adjacency[left].append(right)
                indegree[right] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                current = queue.pop()
                visited += 1
                for successor in adjacency[current]:
                    indegree[successor] -= 1
                    if indegree[successor] == 0:
                        queue.append(successor)
            self.assertEqual(visited, len(node_ids))

    def test_committed_integrated_json_matches_generator(self) -> None:
        path = ROOT / "data/open-problem/ticket245-closure-second-order-klein-linnik.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["ticket"], 245)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertIn(state["deep_focus_problem"], {"riemann", "collatz", "goldbach", "twin_prime"})
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))


if __name__ == "__main__":
    unittest.main()
