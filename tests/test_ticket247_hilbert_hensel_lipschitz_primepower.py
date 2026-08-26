from __future__ import annotations

import json
import unittest
from fractions import Fraction

from scripts.ticket247_hilbert_hensel_lipschitz_primepower import (
    AUDIT_KEY,
    COLLATZ_LIFT_DEPTH,
    ROOT,
    build_audit,
    collatz_hensel_no_go_audit,
    fixed_base_polynomial,
    goldbach_arc_lipschitz_audit,
    hensel_countermodel,
    integer_nth_root,
    riemann_hilbert_schmidt_audit,
    twin_sharp_prime_power_audit,
)


class Ticket247HilbertHenselLipschitzPrimePowerTests(unittest.TestCase):
    def test_riemann_hilbert_schmidt_no_go_certificates(self) -> None:
        audit = riemann_hilbert_schmidt_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "6f96be5ca5ceffa5ed645e2eb17758ae151b079799bf89baaa00c605cce871a5",
        )
        rows = audit["exact_legendre_certificates"]
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(row["all_exact_moments_zero"] for row in rows))
        self.assertTrue(all(row["recurrence_matches_rodrigues"] for row in rows))
        self.assertEqual(rows[-1]["legendre_half_degree_n"], 16)
        self.assertEqual(
            rows[-1]["unnormalized_L2_norm_squared"]["exact"], "2/65"
        )
        self.assertEqual(
            rows[-1]["dyadic_weight_feature_tail_upper_bound"]["exact"],
            "1/1064960",
        )

    def test_collatz_all_prime_hensel_countermodels(self) -> None:
        audit = collatz_hensel_no_go_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "bcb089ee91757f792ae7151212331f811f48a1cc771eea1386d4d4349ba04156",
        )
        self.assertEqual(audit["exact_modular_replay"]["primes_checked"], 1_226)
        self.assertTrue(audit["exact_modular_replay"]["all_lifts_verified"])
        for q in (7, 23, 101):
            v, digits, verified = hensel_countermodel(q, COLLATZ_LIFT_DEPTH)
            self.assertTrue(verified)
            self.assertEqual(len(digits), COLLATZ_LIFT_DEPTH)
            self.assertEqual(fixed_base_polynomial(3, v, q) % q**COLLATZ_LIFT_DEPTH, 0)
            self.assertNotEqual((3 - v) % q, 0)

    def test_goldbach_center_to_arc_bridge_and_counterfamily(self) -> None:
        audit = goldbach_arc_lipschitz_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "314c9f28ab175a59fce98474b249cf6e8fbc9fb811f2258d8c344d1b113a89b4",
        )
        self.assertEqual(len(audit["exact_selected_arc_rows"]), 27)
        self.assertEqual(
            audit["exhaustive_denominator_summaries"][-1][
                "maximum_M_abs_beta_without_2pi"
            ]["exact"],
            "9914236193/250000000000",
        )
        for row in audit["center_only_uniformity_counterfamily"]:
            self.assertEqual(row["center_value_abs_F_N_0"], 0)
            self.assertEqual(row["exact_abs_F_N_beta"], 2)
            self.assertEqual(
                Fraction(row["test_beta"]["exact"]),
                Fraction(1, 2 * row["frequency_N"]),
            )

    def test_twin_exact_prime_power_count_and_sharp_bound(self) -> None:
        audit = twin_sharp_prime_power_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "7b336b5638d06b913ebee11fc89308a7a186953083f85cfe772a8a4971410d87",
        )
        rows = audit["exact_sharp_contamination_rows"]
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["strictly_improves_ticket246_bound"] for row in rows))
        last = rows[-1]
        self.assertEqual(last["limit_X"], 10_000_000)
        self.assertEqual(last["prime_power_pair_count_A2"], 59_129)
        self.assertEqual(last["twin_prime_pair_count_pi2"], 58_980)
        self.assertEqual(last["composite_prime_power_contamination"], 149)
        self.assertEqual(last["exact_odd_composite_prime_powers_N"], 533)
        self.assertLessEqual(last["composite_prime_power_contamination"], 2 * 533)
        self.assertEqual(integer_nth_root(10_000_002, 3), 215)

    def test_machine_boundary_and_classifications(self) -> None:
        root = build_audit()[AUDIT_KEY]
        machine = root["machine_audit"]
        self.assertEqual(machine["new_partial_theorem_count"], 2)
        self.assertEqual(machine["exact_no_go_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "riemann")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
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
        path = ROOT / "data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(state["ticket"], 247)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 247:
            self.assertEqual(state["deep_focus_problem"], "riemann")
        retained_theorems = {
            "riemann": "HilbertSchmidtInfiniteMomentCoercivityNoGo",
            "collatz": "FormalHenselBranchNoGoForValuationDomination",
            "goldbach": "RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo",
            "twin_prime": "SharpOddPrimePowerContaminationBound",
        }
        for problem, theorem in retained_theorems.items():
            self.assertIn(theorem, state["problems"][problem]["established_results"])
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
