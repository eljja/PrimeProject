from __future__ import annotations

import json
import unittest

from scripts.ticket246_moment_alldepth_parseval_primepower import (
    AUDIT_KEY,
    ROOT,
    build_audit,
    collatz_all_depth_audit,
    fixed_base_polynomial,
    goldbach_residue_parseval_audit,
    riemann_finite_moment_audit,
    twin_prime_power_proxy_audit,
)


class Ticket246MomentAllDepthParsevalPrimePowerTests(unittest.TestCase):
    def test_riemann_finite_moment_annihilators(self) -> None:
        audit = riemann_finite_moment_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "b69bddb4b9317df798192eb20375e83c87132c4804c1cdb57fe71723a8667765",
        )
        rows = audit["exact_finite_difference_moment_rows"]
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(row["all_exact_moment_sums_zero"] for row in rows))
        self.assertEqual(rows[-1]["moment_count_m"], 12)
        self.assertEqual(rows[-1]["unnormalized_L2_norm_squared"], 32_247_603_683_100)

    def test_collatz_all_depth_polynomial_identity(self) -> None:
        audit = collatz_all_depth_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "7c570287e63987c481e1b978c549ff1889b3dcc058ef859fe5c1befb32456269",
        )
        replay = audit["exact_modular_replay"]
        self.assertEqual(replay["primes_scanned"], 17_981)
        self.assertEqual(replay["bad_difference_valuation_counts"], {"1": 17_981})
        self.assertEqual(
            replay["comparison_difference_valuation_counts"],
            {"1": 17_980, "2": 1},
        )
        q = 7
        u = (2 ** (q - 1) - 1) // q
        v = (3 ** (q - 1) - 1) // q
        self.assertEqual(32 ** (q - 1) - 27 ** (q - 1), q * fixed_base_polynomial(u, v, q))
        self.assertEqual(2 ** (q - 1) - 3 ** (q - 1), q * (u - v))
        row23 = next(row for row in audit["selected_all_depth_rows"] if row["prime_q"] == 23)
        self.assertEqual(row23["comparison_difference_q_adic_valuation_capped_at_six"], "2")

    def test_goldbach_rational_center_parseval_bridge(self) -> None:
        audit = goldbach_residue_parseval_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "36eb596f31cf8cc962d8f1bb069323d36d8e8478dd095922c64ad5a529a67e10",
        )
        self.assertEqual(len(audit["exact_selected_residue_variance_rows"]), 27)
        summaries = audit["exhaustive_denominator_summaries"]
        self.assertEqual([row["denominators_checked"] for row in summaries], [62, 62, 62])
        self.assertEqual(summaries[-1]["maximum_relative_variance"]["exact"], "37003/215654912")
        self.assertTrue(audit["aggregate"]["exact_residual_parseval_identity_proved"])

    def test_twin_prime_power_contamination_and_minimal_counterexample(self) -> None:
        audit = twin_prime_power_proxy_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "9b1df6145208e9fe91b48bca1b3a3f09be2de3bec22beaff05c0bd40ae0ecb1a",
        )
        self.assertEqual(audit["minimal_false_proxy_pair"]["n"], 7)
        self.assertEqual(audit["minimal_false_proxy_pair"]["right_prime_power"], "3^2")
        last = audit["exact_prime_power_proxy_rows"][-1]
        self.assertEqual(last["limit_X"], 5_000_000)
        self.assertEqual(last["prime_power_pair_count_A2"], 32_585)
        self.assertEqual(last["twin_prime_pair_count_pi2"], 32_463)
        self.assertLessEqual(
            last["composite_prime_power_contamination"],
            last["explicit_contamination_bound_B"],
        )

    def test_machine_boundary_and_classifications(self) -> None:
        root = build_audit()[AUDIT_KEY]
        machine = root["machine_audit"]
        self.assertEqual(machine["new_partial_theorem_count"], 3)
        self.assertEqual(machine["exact_no_go_count"], 1)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "collatz")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "partial_theorem", "partial_theorem", "partial_theorem"],
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
        path = ROOT / "data/open-problem/ticket246-moment-alldepth-parseval-primepower.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(state["ticket"], 246)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 246:
            self.assertEqual(state["deep_focus_problem"], "collatz")
        retained_theorems = {
            "riemann": "FiniteEvenMomentAnnihilatorNoGo",
            "collatz": "AllDepthFixedBaseFermatPolynomialIdentity",
            "goldbach": "RationalCenterResidueParsevalBridge",
            "twin_prime": "PrimePowerPairProxyContaminationBound",
        }
        for problem, theorem in retained_theorems.items():
            self.assertIn(theorem, state["problems"][problem]["established_results"])
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
