from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import cyclic_binomial_coefficients
from scripts.ticket254_diagonal_weighted_reflection_thue import quadratic_multiply, quadratic_power, unit_powers_seventeen
from scripts.ticket255_aggregate_incomplete_odd_local import (
    AUDIT_KEY, SCHEMA, TWIN_EXPECTED_BAD, build_audit,
    incomplete_frequency_families, kth_prime_in_residue,
    prefix_residue_count, split_thue_solution_counts,
)

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"proved", "disproved", "computed_finite", "external_theorem", "assumption", "heuristic", "open"}


class Ticket255AggregateIncompleteOddLocalTests(unittest.TestCase):
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
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_strict_dominance_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "2ba4e6b1090ad6d74f803dc96b1762f0e0cf5057bd0f11f12ee81036d8b99493")
        for row in computation["exact_positive_block_rows"]:
            dimension = row["block_dimension_L"]
            diagonal = Fraction(row["diagonal_entry"]["exact"])
            self.assertEqual(diagonal, 1 + Fraction(1, dimension))
            self.assertLessEqual(diagonal, Fraction(row["absolute_off_diagonal_row_sum"]["exact"]))
            self.assertGreater(Fraction(row["orthogonal_complement_eigenvalue"]["exact"]), 0)
            self.assertEqual(Fraction(row["normalized_dirichlet_packet_energy"]["exact"]), dimension + Fraction(1, dimension))
            self.assertFalse(row["strictly_diagonally_dominant"])
        self.assertFalse(computation["aggregate"]["actual_weil_form_analyzed"])

    def test_collatz_incomplete_recovery_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "cc49768b5030292430f99a91e8eef1047ac66704a68a859ea1e06cd4b86a9293")
        rows = computation["exact_missing_fourier_coefficient_rows"]
        self.assertEqual(len(rows), 48)
        for row in rows:
            prime = row["prime_q"]
            self.assertEqual(tuple(row["frequency_support_H"]), incomplete_frequency_families(prime)[row["support_family"]])
            self.assertNotIn(row["missing_frequency_h0"], row["frequency_support_H"])
            self.assertEqual(Fraction(row["delta_zero_fourier_coefficient_at_h0"]["exact"]), Fraction(1, prime))
            self.assertEqual(Fraction(row["any_H_supported_sum_coefficient_at_h0"]["exact"]), 0)
        self.assertFalse(computation["aggregate"]["approximate_or_canonical_only_recovery_rejected"])

    def test_goldbach_odd_reflection_prefix_exclusion(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "ab8cb879f9a4dbdc1825584e054a56687f770fc0b6c3a40f939be7f06dc2b3fb")
        rows = computation["exact_odd_reflection_prefix_exclusion_rows"]
        self.assertEqual([(r["prime_modulus_q"], r["odd_cyclotomic_exponent_m"]) for r in rows], [(5, 9), (5, 11), (7, 13), (7, 15)])
        for row in rows:
            q, m, t = row["prime_modulus_q"], row["odd_cyclotomic_exponent_m"], row["forced_uniform_shift_t"]
            residue = m % q
            coefficients = cyclic_binomial_coefficients(q, m)
            kth_prime, kth_index = kth_prime_in_residue(q, residue, 2 * t - 1)
            self.assertEqual(coefficients[residue], -coefficients[0])
            self.assertEqual(row["forced_count_at_m_mod_q_2t_minus_1"], 2 * t - 1)
            self.assertEqual(row["actual_first_T_prime_count_at_m_mod_q"], prefix_residue_count(q, residue, q * t))
            self.assertEqual((row["forced_count_th_residue_prime"], row["global_index_lambda_of_forced_count_th_residue_prime"]), (kth_prime, kth_index))
            self.assertLess(q * t, kth_index)
            self.assertTrue(row["unique_prime_prefix_excluded"])
        self.assertFalse(computation["aggregate"]["q_divisible_compatible_tails_excluded"])

    def test_twin_local_cover_and_direct_enumeration(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "3d89ca8e3ca658a6bff44a8e532a441a2be41ac89c5d8d46b2af84d8c84a6a63")
        survivors = set(range(17))
        for row in computation["exact_split_prime_local_obstruction_rows"]:
            prime = row["split_prime_p"]
            square_root, counts = split_thue_solution_counts(prime)
            self.assertEqual(square_root, row["least_square_root_s_of_two_mod_p"])
            self.assertEqual(counts, row["solution_counts_by_unit_twist_j"])
            self.assertEqual(tuple(row["locally_obstructed_twists"]), TWIN_EXPECTED_BAD[prime])
            survivors.difference_update(row["locally_obstructed_twists"])
            self.assertEqual(sorted(survivors), row["cumulative_surviving_twists"])
        self.assertEqual(survivors, {1, 16})
        direct_counts = [0] * 17
        units = unit_powers_seventeen()
        for u in range(103):
            for v in range(103):
                powered = quadratic_power((u, v), 17)
                for twist, unit in enumerate(units):
                    if quadratic_multiply(unit, powered)[1] % 103 == 1:
                        direct_counts[twist] += 1
        self.assertEqual(direct_counts, computation["exact_split_prime_local_obstruction_rows"][0]["solution_counts_by_unit_twist_j"])
        self.assertTrue(all(w["B_j_u_v"] == 1 and w["reduced_y"] == -1 and not w["admissible_positive_point"] for w in computation["surviving_twist_integer_witnesses"]))
        self.assertEqual(computation["aggregate"]["surviving_twists"], [1, 16])
        self.assertFalse(computation["aggregate"]["surviving_twists_globally_solved"])

    def test_proof_dags(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            adjacency = {node_id: [] for node_id in ids}
            indegree = {node_id: 0 for node_id in ids}
            for source, target in dag["edges"]:
                self.assertIn(source, ids); self.assertIn(target, ids)
                adjacency[source].append(target); indegree[target] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                source = queue.pop(); visited += 1
                for target in adjacency[source]:
                    indegree[target] -= 1
                    if indegree[target] == 0: queue.append(target)
            self.assertEqual(visited, len(ids))

    def test_committed_outputs_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket255-aggregate-incomplete-odd-local.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual((state["ticket"], state["parent_ticket"]), (255, 254))
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "twin_prime")
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))


if __name__ == "__main__":
    unittest.main()