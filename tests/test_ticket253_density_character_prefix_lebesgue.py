from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket253_density_character_prefix_lebesgue import (
    AUDIT_KEY,
    GOLDBACH_COMPATIBLE_PAIRS,
    SCHEMA,
    build_audit,
    complete_nontrivial_linear_character_sum,
    first_n_primes,
    is_prime,
    prime_factors,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket253DensityCharacterPrefixLebesgueTests(unittest.TestCase):
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
        self.assertEqual(machine["new_partial_theorem_count"], 3)
        self.assertEqual(machine["exact_no_go_count"], 1)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in (
                "riemann", "collatz", "goldbach", "twin_prime"
            )],
            ["partial_theorem", "exact_no_go", "partial_theorem", "partial_theorem"],
        )
        self.assertTrue(all(
            self.root[key]["problem_status"] == "open_not_proven"
            for key in ("riemann", "collatz", "goldbach", "twin_prime")
        ))

    def test_riemann_density_packet_identity(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "00bebb686b3544d67b49612c512f28feee544d678ceab6c5fa269f64e9e16299",
        )
        rows = computation["exact_periodic_density_rows"]
        self.assertEqual(len(rows), 11)
        for row in rows:
            size = row["dirichlet_half_bandwidth_N"]
            selected = sum(
                1 for frequency in range(-size, size + 1)
                if frequency % 6 in {1, 5}
            )
            energy = Fraction(selected, 2 * size + 1)
            self.assertEqual(
                Fraction(row["exact_projection_energy"]["exact"]), energy
            )
            self.assertLessEqual(
                row["integer_discrepancy_abs_3count_minus_total"], 3
            )
        self.assertTrue(
            computation["aggregate"]["projection_energy_equals_symmetric_frequency_density_proved"]
        )
        self.assertFalse(
            computation["aggregate"]["actual_weil_form_dominates_projection"]
        )

    def test_collatz_complete_character_dichotomy(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "455240ed72e4017bfbc63ba310348eb9e2618370d829ee093253e1d66e6883c2",
        )
        for prime in (7, 11, 43):
            self.assertEqual(
                complete_nontrivial_linear_character_sum(prime, 0), prime - 1
            )
            for residue in range(1, prime):
                self.assertEqual(
                    complete_nontrivial_linear_character_sum(prime, residue), -1
                )
        for row in computation["exact_canonical_character_rows"]:
            prime = row["prime_q"]
            slope_hit = row["slope_residue_D_q"] == 0
            self.assertEqual(
                Fraction(row["full_orthogonality_average"]["exact"]),
                Fraction(int(slope_hit), 1),
            )
            self.assertEqual(
                row["complete_nontrivial_character_sum_exact_integer"],
                prime - 1 if slope_hit else -1,
            )
            self.assertEqual(slope_hit, row["rational_wieferich_32_over_27"])
        self.assertFalse(computation["aggregate"]["cross_prime_distribution_controlled"])

    def test_goldbach_unique_prime_prefix_criterion_rows(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "a14b831094b7733f9186b166b2346c3e295617c705ded50c46ef38a62994e0ff",
        )
        rows = computation["exact_compatible_tail_prefix_rows"]
        self.assertEqual(len(rows), len(GOLDBACH_COMPATIBLE_PAIRS))
        maximum = max(row["forced_total_prime_count_qt"] for row in rows)
        primes = first_n_primes(maximum)
        for row in rows:
            q = row["prime_modulus_q"]
            m = row["cyclotomic_exponent_m"]
            coefficients = cyclic_binomial_coefficients(q, m)
            shift = 1 - coefficients[0]
            target = [value + shift for value in coefficients]
            total = q * shift
            actual = [0] * q
            for prime in primes[:total]:
                actual[prime % q] += 1
            self.assertEqual(row["cyclic_coefficients_c"], coefficients)
            self.assertEqual(row["forced_prime_count_vector"], target)
            self.assertEqual(row["actual_first_qt_prime_residue_counts"], actual)
            self.assertNotEqual(actual, target)
            self.assertEqual(
                row["l1_discrepancy"],
                sum(abs(actual[index] - target[index]) for index in range(q)),
            )
        witness = rows[0]
        self.assertEqual((witness["prime_modulus_q"], witness["cyclotomic_exponent_m"]), (5, 8))
        self.assertEqual(witness["forced_prime_count_vector"], [1, 76, 76, 1, 126])
        self.assertEqual(witness["l1_discrepancy"], 142)
        self.assertFalse(computation["aggregate"]["all_compatible_tail_exponents_excluded"])

    def test_twin_external_reduction_and_exact_frontier(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "b98e7851ac77f39a65148a17da8a40600d25774928d13483a1fcef4d4b7b8bb6",
        )
        exponents = computation["remaining_prime_exponents"]
        self.assertEqual(len(exponents), 84)
        self.assertEqual(exponents[0], 17)
        self.assertEqual(exponents[-1], 911)
        self.assertNotIn(13, exponents)
        self.assertTrue(all(
            is_prime(exponent)
            and 17 <= exponent <= 911
            and exponent % 24 in {13, 17, 19, 23}
            for exponent in exponents
        ))
        self.assertEqual(
            computation["residue_class_counts"],
            {"13": 20, "17": 20, "19": 23, "23": 21},
        )
        scan = computation["finite_odd_exponent_factor_scan"]
        self.assertEqual(scan["tested_odd_exponent_count"], 4999)
        self.assertEqual(scan["allowed_exponent_count"], 331)
        self.assertEqual(scan["rejected_exponent_count"], 4668)
        allowed_set = set(exponents)
        self.assertTrue(all(
            all(factor in allowed_set for factor in prime_factors(exponent))
            for exponent in scan["first_twenty_allowed_exponents"]
        ))
        self.assertFalse(computation["aggregate"]["all_remaining_84_prime_exponents_excluded"])

    def test_proof_dags(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            nodes = dag["nodes"]
            ids = {node["id"] for node in nodes}
            self.assertEqual(len(ids), len(nodes))
            self.assertTrue(all(node["status"] in ALLOWED for node in nodes))
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
                source = queue.pop()
                visited += 1
                for target in adjacency[source]:
                    indegree[target] -= 1
                    if indegree[target] == 0:
                        queue.append(target)
            self.assertEqual(visited, len(nodes))
        twin_nodes = self.root["twin_prime"]["proof_dag"]["nodes"]
        self.assertEqual(sum(node["status"] == "external_theorem" for node in twin_nodes), 1)

    def test_committed_outputs_and_state(self) -> None:
        integrated = ROOT / "data/open-problem/ticket253-density-character-prefix-lebesgue.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["ticket"], 253)
        self.assertEqual(state["parent_ticket"], 252)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "twin_prime")
        self.assertTrue(all(problem["stagnation_count"] == 0 for problem in state["problems"].values()))


if __name__ == "__main__":
    unittest.main()
