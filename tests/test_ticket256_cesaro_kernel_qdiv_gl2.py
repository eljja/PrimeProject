from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    quadratic_multiply,
    quadratic_power,
    unit_powers_seventeen,
)
from scripts.ticket256_cesaro_kernel_qdiv_gl2 import (
    AUDIT_KEY,
    SCHEMA,
    TWIN_BOX_RADIUS,
    build_audit,
    inverse_surviving_twist_transform,
    normalized_packet_energy,
    surviving_twist_transform,
    symmetric_lag_partial_sums,
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


class Ticket256CesaroKernelQDivGL2Tests(unittest.TestCase):
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
        self.assertEqual(machine["new_partial_theorem_count"], 4)
        self.assertEqual(machine["exact_no_go_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["partial_theorem"] * 4,
        )

    def test_riemann_packet_cesaro_identity_and_nonnecessity(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "a4d61abe3161c28b13f5f333e2fae644f2c9171107dde94d92e38adc6b8615d1",
        )
        for row in computation["exact_packet_cesaro_rows"]:
            coefficients = [
                Fraction(item["exact"])
                for item in row["lag_coefficients_a_0_through_a_L_minus_1"]
            ]
            partial = symmetric_lag_partial_sums(coefficients)
            energy = normalized_packet_energy(coefficients)
            self.assertEqual(
                partial,
                [
                    Fraction(item["exact"])
                    for item in row[
                        "symmetric_lag_partial_sums_S_0_through_S_L_minus_1"
                    ]
                ],
            )
            self.assertEqual(energy, sum(partial, Fraction(0)) / len(partial))
            self.assertGreaterEqual(energy, 0)
        second = computation["exact_packet_cesaro_rows"][1]
        self.assertEqual(Fraction(second["minimum_partial_sum"]["exact"]), -1)
        self.assertEqual(Fraction(second["normalized_packet_energy"]["exact"]), 0)
        self.assertFalse(
            computation["aggregate"]["uniform_partial_sum_lower_bound_is_necessary"]
        )
        self.assertFalse(
            computation["aggregate"]["actual_weil_lag_partial_sums_analyzed"]
        )

    def test_collatz_sharp_incomplete_kernel(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "e50be6fa63328562b64c1fa1023ad706493a60e47d84705d24aebec05d412de3",
        )
        for row in computation["exact_canonical_incomplete_kernel_rows"]:
            prime = row["prime_q"]
            self.assertEqual(
                Fraction(row["exact_error_magnitude"]["exact"]), Fraction(1, prime)
            )
            self.assertEqual(
                row["canonical_slope_D_q"],
                (
                    5 * row["fermat_quotient_F_q_2"]
                    - 3 * row["fermat_quotient_F_q_3"]
                )
                % prime,
            )
            self.assertTrue(row["renormalized_error_has_unit_modulus"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["one_missing_frequency_minimax_sharp"])
        self.assertTrue(aggregate["decay_only_not_nontrivial_phase_cancellation"])
        self.assertFalse(aggregate["renormalized_cross_prime_cancellation_proved"])

    def test_goldbach_q_divisible_parity_and_prefix_asymmetry(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "6ded0f179c955a164110a035c40971e60b948905edbb9c3377af7ac985ef8619",
        )
        self.assertEqual(
            computation["aggregate"]["odd_q_divisible_compatible_pair_count"], 0
        )
        rows = computation["exact_q_divisible_prefix_exclusion_rows"]
        self.assertEqual(
            [(row["prime_modulus_q"], row["q_divisible_even_exponent_m"]) for row in rows],
            [(5, 10), (7, 14)],
        )
        for row in rows:
            q = row["prime_modulus_q"]
            m = row["q_divisible_even_exponent_m"]
            coefficients = cyclic_binomial_coefficients(q, m)
            target = row["forced_symmetric_residue_counts"]
            actual = row["actual_first_T_prime_residue_counts"]
            self.assertEqual(coefficients, row["cyclic_coefficients"])
            self.assertTrue(all(target[r] == target[-r % q] for r in range(q)))
            witness = row["least_asymmetry_witness_residue"]
            self.assertNotEqual(actual[witness], actual[-witness % q])
            self.assertNotEqual(target, actual)
            self.assertTrue(row["unique_prime_prefix_excluded"])
        self.assertFalse(
            computation["aggregate"]["all_q_divisible_compatible_tails_excluded"]
        )

    def test_twin_gl2_bijection_and_correct_norm_sign(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "b16cc63924090d6e214ecdaaa8c47018fced6bae337cc3445ed9cbd3a85eb7a9",
        )
        self.assertEqual(computation["determinant"], 1)
        units = unit_powers_seventeen()
        failures = 0
        for u in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
            for v in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
                transformed = surviving_twist_transform(u, v)
                self.assertEqual(
                    inverse_surviving_twist_transform(*transformed), (u, v)
                )
                a1, b1 = quadratic_multiply(
                    units[1], quadratic_power((u, v), 17)
                )
                a16, b16 = quadratic_multiply(
                    units[16], quadratic_power(transformed, 17)
                )
                correct_reduced_y = transformed[0] ** 2 - 2 * transformed[1] ** 2
                failures += int(
                    not (
                        a16 == -a1
                        and b16 == b1
                        and correct_reduced_y == -(u * u - 2 * v * v)
                    )
                )
        self.assertEqual(failures, 0)
        box = computation["finite_box_audit"]
        self.assertEqual(box["exact_grid_case_count"], 16641)
        self.assertEqual(box["coefficient_one_point_count"], 1)
        self.assertEqual(box["admissible_absolute_branch_point_count"], 0)
        self.assertEqual(
            (box["coefficient_one_points"][0]["u"], box["coefficient_one_points"][0]["v"]),
            (1, 0),
        )
        self.assertFalse(
            computation["aggregate"]["single_absolute_branch_globally_solved"]
        )

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
        integrated = ROOT / "data/open-problem/ticket256-cesaro-kernel-qdiv-gl2.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(state["ticket"], 256)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 256:
            self.assertEqual(state["deep_focus_problem"], "twin_prime")
        historical = {
            "riemann": "ToeplitzPacketCesaroLagPartialSumCriterion",
            "collatz": "SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage",
            "goldbach": "QDivisibleReflectionAsymmetryPrimePrefixExclusion",
            "twin_prime": "SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction",
        }
        for problem_key, theorem in historical.items():
            self.assertIn(theorem, state["problems"][problem_key]["established_results"])


if __name__ == "__main__":
    unittest.main()
