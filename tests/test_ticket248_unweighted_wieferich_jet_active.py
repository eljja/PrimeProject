from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket248_unweighted_wieferich_jet_active import (
    AUDIT_KEY,
    RIEMANN_ORDERS,
    SCHEMA,
    build_audit,
    legendre_even_moment_factorial,
    legendre_even_moment_product,
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


class Ticket248UnweightedWieferichJetActiveTests(unittest.TestCase):
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
        self.assertEqual(machine["new_partial_theorem_count"], 3)
        self.assertEqual(machine["exact_no_go_count"], 1)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "partial_theorem", "partial_theorem", "partial_theorem"],
        )
        self.assertTrue(
            all(
                self.root[key]["problem_status"] == "open_not_proven"
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            )
        )

    def test_riemann_unweighted_moment_formula_and_bound(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "faaba3834a933146319b810147b5d58136ae13d23bd6599297b292d2ba33c1bd",
        )
        self.assertEqual(len(computation["exact_legendre_rows"]), len(RIEMANN_ORDERS))
        for n in RIEMANN_ORDERS:
            self.assertEqual(legendre_even_moment_factorial(n, n - 1), 0)
            for k in (n, n + 1, 2 * n, 256):
                self.assertEqual(
                    legendre_even_moment_factorial(n, k),
                    legendre_even_moment_product(n, k),
                )
        for row in computation["exact_legendre_rows"]:
            partial = Fraction(row["partial_unweighted_energy"]["exact"])
            bound = Fraction(row["proved_all_tail_energy_bound"]["exact"])
            self.assertLessEqual(partial, bound)
            self.assertTrue(row["certificate_verified"])
        self.assertTrue(
            computation["aggregate"]["unweighted_non_hilbert_schmidt_no_go_proved"]
        )
        self.assertFalse(
            computation["aggregate"]["genuine_weil_admissible_closure_reached"]
        )

    def test_collatz_actual_bad_branch_equivalence_scan(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "444834a2768b3e94e21d0f968aef0e93fd87f08c540ca52af08756480b6d2d25",
        )
        scan = computation["exact_modular_scan"]
        self.assertEqual(scan["primes_checked"], 78_495)
        self.assertEqual(scan["W_32_27_zero_primes"], [])
        self.assertEqual(scan["W_2_3_zero_primes"], [23])
        self.assertEqual(scan["separated_bad_primes"], [])
        q23 = next(
            row for row in computation["selected_exact_rows"] if row["prime_q"] == 23
        )
        self.assertNotEqual(q23["W_32_27_mod_q"], 0)
        self.assertEqual(q23["W_2_3_mod_q"], 0)
        self.assertTrue(
            all(row["certificate_verified"] for row in computation["selected_exact_rows"])
        )
        self.assertFalse(
            computation["aggregate"]["finite_scan_proves_global_absence"]
        )

    def test_goldbach_centered_first_jet_invariants(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "49d39cfb54e21607b0ad1e39ddf0734d30d646bab71b90b82fb746a3f80cc18a",
        )
        self.assertEqual(
            computation["exact_modular_replay"]["denominator_cases"], 282
        )
        rows = computation["exact_selected_first_jet_rows"]
        self.assertEqual(len(rows), 36)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        last = rows[-1]
        self.assertEqual(last["limit_X"], 500_000)
        self.assertEqual(last["denominator_q"], 96)
        self.assertEqual(last["phi_times_count_variance"], 208_000)
        self.assertEqual(
            last["phi_times_first_moment_variance"], 22_529_726_453_345_020
        )
        self.assertTrue(
            computation["aggregate"]["centered_first_jet_parseval_identity_proved"]
        )
        self.assertFalse(
            computation["aggregate"]["uniform_all_numerator_saving_proved"]
        )

    def test_twin_active_contamination_identity(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "85f69edcdb7bc23ce3a41d770918c5a4589b4b50a4e003145c47874fa2bd1741",
        )
        rows = computation["exact_active_contamination_rows"]
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        last = rows[-1]
        self.assertEqual(last["prime_power_pair_count_A2"], 59_129)
        self.assertEqual(last["twin_prime_pair_count_pi2"], 58_980)
        self.assertEqual(last["exact_contamination_A2_minus_pi2"], 149)
        self.assertEqual(last["left_active_composite_power_pairs_L"], 14)
        self.assertEqual(last["right_active_composite_power_pairs_R"], 136)
        self.assertEqual(last["both_composite_power_pairs_B"], 1)
        self.assertEqual(last["active_union_bound_L_plus_R"], 150)
        self.assertEqual(last["ticket247_sharp_bound"], 2_822)

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
        path = ROOT / "data/open-problem/ticket248-unweighted-wieferich-jet-active.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(state["ticket"], 248)
        self.assertEqual(state["parent_ticket"], 247)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "goldbach")
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
