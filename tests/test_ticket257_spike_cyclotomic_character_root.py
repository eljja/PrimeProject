from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket253_density_character_prefix_lebesgue import (
    fermat_quotient_mod_prime,
)
from scripts.ticket257_spike_cyclotomic_character_root import (
    AUDIT_KEY,
    SCHEMA,
    TWIN_DENOMINATOR_LIMIT,
    b1_coefficient_form,
    build_audit,
    direct_packet_energy,
    induced_lag_partial_sum,
    prescribed_packet_energy,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved",
    "disproved",
    "computed_finite",
    "external_theorem",
    "assumption",
    "heuristic",
    "open",
}


class Ticket257SpikeCyclotomicCharacterRootTests(unittest.TestCase):
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
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_sparse_spike_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "2654791b7d15314396158a2a60a103f76cb57f74a2ee477bf32d47213a767f56",
        )
        rows = computation["exact_sparse_spike_rows"]
        self.assertEqual(len(rows), 8)
        for row in rows:
            k = row["spike_level_k"]
            dimension = row["packet_dimension_L_equals_4_power_k"]
            self.assertEqual(dimension, 4**k)
            expected_energy = Fraction(1) - Fraction(1, 2**k)
            self.assertEqual(prescribed_packet_energy(dimension), expected_energy)
            self.assertEqual(
                Fraction(row["direct_energy_from_reconstructed_lags"]["exact"]),
                direct_packet_energy(dimension),
            )
            self.assertEqual(
                induced_lag_partial_sum(dimension - 1), Fraction(1 - 2**k)
            )
            self.assertTrue(row["identity_verified"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["lag_partial_sums_unbounded_below_proved"])
        self.assertTrue(aggregate["positivity_and_convergence_only_route_refuted"])
        self.assertTrue(aggregate["scaled_downward_variation_repair_proved"])
        self.assertFalse(aggregate["actual_weil_packet_analyzed"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_distinct_prime_cyclotomic_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "627c0da86ba9bd0f734d01ace2f1fb18df1778244c975655a877f52ca7ecf9a5",
        )
        rows = computation["exact_canonical_phase_prefix_rows"]
        self.assertEqual(len(rows), 22)
        expected_pairs = [
            (7, 6), (11, 3), (13, 4), (17, 1), (19, 18), (23, 11),
            (29, 18), (31, 10), (37, 25), (41, 11), (43, 33), (47, 46),
            (53, 5), (59, 35), (61, 19), (67, 5), (71, 56), (73, 56),
            (79, 12), (83, 48), (89, 47), (97, 70),
        ]
        self.assertEqual(
            [(row["prime_q"], row["canonical_phase_exponent_D_q"]) for row in rows],
            expected_pairs,
        )
        conductor = 1
        degree = 1
        for row in rows:
            q = row["prime_q"]
            d = (
                5 * fermat_quotient_mod_prime(2, q)
                - 3 * fermat_quotient_mod_prime(3, q)
            ) % q
            conductor *= q
            degree *= q - 1
            self.assertEqual(row["canonical_phase_exponent_D_q"], d)
            self.assertNotEqual(d, 0)
            self.assertEqual(row["coprime_conductor_product"], conductor)
            self.assertEqual(row["cyclotomic_compositum_degree"], degree)
            self.assertTrue(row["finite_prefix_exact_zero_impossible"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["every_finite_distinct_prime_phase_sum_nonzero_proved"])
        self.assertFalse(aggregate["sublinear_phase_sum_bound_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_q11_character_prefix_exclusion(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "b294b8571a28f6988cdb0fd7d0353f683eb02d8aeae4b42b031ab4801f4b022f",
        )
        rows = computation["exact_reflection_character_certificate_rows"]
        self.assertEqual(
            [(row["prime_q"], row["exponent_m"]) for row in rows],
            [(5, 10), (7, 14), (11, 22)],
        )
        for row in rows:
            q = row["prime_q"]
            self.assertEqual(
                cyclic_binomial_coefficients(q, row["exponent_m"]),
                row["coefficients"],
            )
            self.assertEqual(sum(row["actual_prime_residue_counts"]), row["prime_prefix_length_T"])
            self.assertTrue(row["actual_vector_is_reflection_asymmetric"])
            product = 1
            for residue, count in enumerate(row["actual_prime_residue_counts"]):
                if residue:
                    character = pow(residue, (q - 1) // 2, q)
                    product = product * pow(character, count, q) % q
            self.assertEqual(product, row["actual_quadratic_character_product_mod_q"])
            self.assertEqual(product, row["product_recomputed_independently_from_counts"])
            self.assertTrue(row["certificate_verified"])
        q11 = rows[-1]
        self.assertEqual(q11["prime_prefix_length_T"], 7_759_741)
        self.assertEqual(q11["last_prime_in_prefix"], 137_141_243)
        self.assertEqual(
            q11["actual_prime_residue_counts"],
            [1, 776123, 776078, 775943, 775798, 775646, 776178, 776150, 775928, 775841, 776055],
        )
        self.assertEqual(q11["actual_quadratic_character_product_mod_q"], 10)
        self.assertEqual(q11["reflection_symmetric_expected_product_mod_q"], 1)
        self.assertTrue(q11["quadratic_character_certificate_excludes_prefix"])
        self.assertFalse(rows[0]["quadratic_character_certificate_excludes_prefix"])
        self.assertFalse(rows[1]["quadratic_character_certificate_excludes_prefix"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["all_odd_character_moments_characterize_symmetry_proved"])
        self.assertFalse(aggregate["quadratic_character_is_complete_asymmetry_detector"])
        self.assertFalse(aggregate["all_compatible_even_q_divisible_prefixes_excluded"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_unique_root_neighbor_reduction(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "70e6d98d1a8476ac6ea9db6eb2bc27895a7a84622e256f3cdd12d8881f92e5b1",
        )
        bracket = computation["exact_root_bracket"]
        self.assertEqual(Fraction(bracket["lower"]["exact"]), Fraction(-14651, 200000))
        self.assertEqual(Fraction(bracket["upper"]["exact"]), Fraction(-7325499, 100000000))
        self.assertLess(bracket["cleared_lower_form_value"], 0)
        self.assertGreater(bracket["cleared_upper_form_value"], 0)
        self.assertLess(
            (Fraction(bracket["upper"]["exact"]) - Fraction(bracket["lower"]["exact"]))
            * TWIN_DENOMINATOR_LIMIT,
            1,
        )
        self.assertEqual(b1_coefficient_form(-1, 1), -470832)
        self.assertEqual(b1_coefficient_form(0, 1), 256)
        self.assertLess(b1_coefficient_form(-74, 1000), 0)
        self.assertGreater(b1_coefficient_form(-73, 1000), 1)
        finite = computation["finite_denominator_audit"]
        self.assertEqual(finite["absolute_v_limit"], 200000)
        self.assertEqual(finite["candidate_evaluation_count"], 400399)
        self.assertEqual(finite["maximum_candidate_span_per_sign"], 2)
        self.assertEqual(finite["nonzero_v_coefficient_one_hits"], [])
        self.assertEqual(finite["v_zero_integral_solutions"], [{"u": 1, "v": 0, "reduced_y": -1}])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["strict_monotonicity_and_unique_real_root_proved"])
        self.assertTrue(aggregate["all_integral_solutions_reduce_to_unique_root_neighbors_proved"])
        self.assertTrue(aggregate["primitive_double_divisibility_conditions_proved"])
        self.assertFalse(aggregate["single_absolute_branch_globally_solved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            graph = {node_id: [] for node_id in ids}
            indegree = {node_id: 0 for node_id in ids}
            for source, target in dag["edges"]:
                self.assertIn(source, ids)
                self.assertIn(target, ids)
                graph[source].append(target)
                indegree[target] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                source = queue.pop()
                visited += 1
                for target in graph[source]:
                    indegree[target] -= 1
                    if indegree[target] == 0:
                        queue.append(target)
            self.assertEqual(visited, len(ids))

    def test_committed_outputs_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket257-spike-cyclotomic-character-root.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(state["ticket"], 257)
        if state["ticket"] == 257:
            self.assertEqual(state["parent_ticket"], 256)
            self.assertEqual(state["deep_focus_problem"], "goldbach")
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        expected = {
            "riemann": "PositiveConvergentPacketEnergyLagPartialSumNoGo",
            "collatz": "DistinctPrimeCyclotomicPhaseExactCancellationNoGo",
            "goldbach": "QuadraticCharacterReflectionObstructionAndNextPrefixExclusion",
            "twin_prime": "UniqueRealRootNeighborReductionAndBoundedExclusion",
        }
        for key, theorem in expected.items():
            self.assertIn(theorem, state["problems"][key]["established_results"])
            self.assertEqual(state["problems"][key]["stagnation_count"], 0)


if __name__ == "__main__":
    unittest.main()
