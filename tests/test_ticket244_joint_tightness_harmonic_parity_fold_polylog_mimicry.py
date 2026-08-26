from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry import (
    AUDIT_KEY,
    ROOT,
    SCHEMA,
    build_audit,
    collatz_harmonic_audit,
    goldbach_parity_fold_audit,
    harmonic_prefixes_mod_prime,
    riemann_joint_tightness_audit,
    twin_polylog_mimicry_audit,
)


class Ticket244JointTightnessHarmonicParityFoldPolylogMimicryTests(
    unittest.TestCase
):
    def test_riemann_joint_tightness_certificate(self) -> None:
        audit = riemann_joint_tightness_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "ba395b597b5ad65a2e1542934cb1781646c445f36e3b2828931e423fde04b07b",
        )
        self.assertEqual(len(audit["physical_only_counterfamily_gram_rows"]), 5)
        self.assertTrue(
            all(
                row["minimum_pair_distance_squared"]["exact"] == "2"
                for row in audit["physical_only_counterfamily_gram_rows"]
            )
        )
        self.assertEqual(
            [
                row["squared_L2_translation_bound"]["exact"]
                for row in audit["exact_translation_bound_rows"]
            ],
            ["5/4", "5/16", "5/64", "5/256", "5/1024"],
        )

    def test_collatz_harmonic_identities(self) -> None:
        audit = collatz_harmonic_audit()
        replay = audit["bounded_harmonic_replay"]
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(replay["primes_scanned"], 2_259)
        self.assertEqual(replay["bad_line_count"], 0)
        self.assertEqual(replay["first_order_positive_candidate_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "bf5611e2479fe672d7d3a6b8d746f99c79bfee67bc7f894075681ca39b6723a2",
        )
        for prime in (7, 11, 59, 109):
            half, third = harmonic_prefixes_mod_prime(prime)
            f2 = ((pow(2, prime - 1, prime * prime) - 1) // prime) % prime
            f3 = ((pow(3, prime - 1, prime * prime) - 1) // prime) % prime
            self.assertEqual((half + 2 * f2) % prime, 0)
            self.assertEqual((2 * third + 3 * f3) % prime, 0)

    def test_goldbach_exact_parity_fold(self) -> None:
        audit = goldbach_parity_fold_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(audit["aggregate"]["finite_even_targets_checked"], 8_290)
        self.assertEqual(
            audit["transcript_sha256"],
            "ba16a10093eb8fe103469b86dec9e5768dcfed91fccc7944168c6c775a0d3c61",
        )
        for row in audit["exact_parity_fold_rows"]:
            self.assertEqual(row["full_sum_vs_odd_sum_coefficient_failures"], 0)
            self.assertEqual(row["exact_half_turn_phase_failures"], 0)
            self.assertTrue(row["certificate_verified"])

    def test_twin_polylog_period_witnesses(self) -> None:
        audit = twin_polylog_mimicry_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            audit["transcript_sha256"],
            "506feb7368986984fd026ada7be00bb70d5049766f2ab1d0c02ee24686cb8d7c",
        )
        rows = audit["finite_polylog_period_witness_rows"]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertLess(
                row["scale_dependent_period_M_X"], row["bertrand_prime_ell_X"]
            )
            self.assertLess(
                row["bertrand_prime_ell_X"],
                2 * row["scale_dependent_period_M_X"],
            )
            self.assertEqual(
                row["forced_composite_successor_p_plus_2"]
                % row["bertrand_prime_ell_X"],
                0,
            )
            self.assertTrue(row["certificate_verified"])

    def test_machine_boundary_and_classifications(self) -> None:
        payload = build_audit()
        self.assertEqual(payload["schema"], SCHEMA)
        self.assertTrue(payload["iteration_complete"])
        self.assertFalse(payload["program_complete"])
        root = payload[AUDIT_KEY]
        machine = root["machine_audit"]
        self.assertEqual(machine["partial_theorem_count"], 3)
        self.assertEqual(machine["exact_no_go_count"], 1)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["partial_theorem", "partial_theorem", "partial_theorem", "exact_no_go"],
        )

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        root = build_audit()[AUDIT_KEY]
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = root[key]["proof_dag"]
            node_ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(
                sum(node["status"] == "open" for node in dag["nodes"]), 1
            )
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
        path = ROOT / (
            "data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-"
            "polylog-mimicry.json"
        )
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_advances_exactly_one_ticket(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(state["ticket"], 244)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        retained = {
            "riemann": "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
            "collatz": "FixedBaseBadLineHarmonicSumEquivalence",
            "goldbach": "ExactParityArcFoldingForEvenBinaryGoldbach",
            "twin_prime": "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
        }
        for problem, theorem in retained.items():
            self.assertIn(theorem, state["problems"][problem]["established_results"])
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
