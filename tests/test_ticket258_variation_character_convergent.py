from __future__ import annotations

import json
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path

from scripts.ticket253_density_character_prefix_lebesgue import fermat_quotient_mod_prime
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import (
    AUDIT_KEY,
    COLLATZ_PRIME_LIMIT,
    SCHEMA,
    TWIN_CF_TERM_COUNT,
    build_audit,
    constructed_character_blind_counts,
    cyclotomic_polynomial,
    induced_partial_sum,
    prescribed_bv_energy,
)

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"proved", "disproved", "computed_finite", "external_theorem", "assumption", "heuristic", "open"}


class Ticket258VariationCharacterConvergentTests(unittest.TestCase):
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
        self.assertEqual(machine["deep_focus_problem"], "twin_prime")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_bounded_total_variation_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "38b8848a883363638d20c80bab9be204bfde0d9fabd6e0c2d17f34244845215b")
        self.assertEqual(Fraction(computation["total_variation_exact"]["exact"]), 2)
        rows = computation["exact_bounded_variation_spike_rows"]
        self.assertEqual(len(rows), 12)
        for row in rows:
            level = row["spike_level_k"]
            dimension = row["packet_dimension_L"]
            self.assertEqual(dimension, 4**level)
            self.assertEqual(prescribed_bv_energy(dimension), 1 - Fraction(1, 2**level))
            self.assertEqual(induced_partial_sum(dimension - 1), 1 - 2**level)
            self.assertTrue(row["identity_verified"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["finite_total_variation_proved"])
        self.assertTrue(aggregate["ordinary_bounded_variation_repair_refuted"])
        self.assertFalse(aggregate["actual_weil_packet_analyzed"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_rational_independence_boundary(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "7314b839d426d6ba0b5fdfbf9d259d9c585f2a7f9f06510d8f325fb060b72dd1")
        rows = computation["exact_canonical_phase_rows"]
        self.assertEqual(len(rows), 166)
        self.assertEqual(rows[-1]["prime_q"], COLLATZ_PRIME_LIMIT)
        for row in rows:
            q = row["prime_q"]
            self.assertGreaterEqual(q, 5)
            self.assertEqual(row["canonical_phase_exponent_D_q"], (5 * fermat_quotient_mod_prime(2, q) - 3 * fermat_quotient_mod_prime(3, q)) % q)
            self.assertTrue(row["phase_is_nontrivial_primitive_qth_root"])
            self.assertTrue(row["certificate_verified"])
        aggregate = computation["aggregate"]
        self.assertEqual(aggregate["trivial_phase_primes"], [])
        self.assertTrue(aggregate["rational_linear_independence_proved_for_nontrivial_distinct_prime_phases"])
        self.assertFalse(aggregate["sublinear_phase_sum_bound_proved"])
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_primitive_character_classification(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "6067f098366c338c9b8387b32f532cb54c58e2d6a838e9e29a2704c3fb657570")
        rows = computation["exact_modulus_classification_rows"]
        self.assertEqual([row["prime_q"] for row in rows], [5, 7, 11, 13, 17, 19])
        self.assertEqual([row["one_primitive_odd_character_is_complete"] for row in rows], [True, False, False, False, True, False])
        for row in rows:
            blind = row["blind_vector_certificate"]
            if row["q_minus_1_is_power_of_two"]:
                self.assertIsNone(blind)
            else:
                self.assertIsNotNone(blind)
                assert blind is not None
                self.assertTrue(blind["reflection_asymmetric"])
                self.assertTrue(blind["primitive_character_moment_is_zero"])
                self.assertEqual(blind["primitive_character_moment_remainder"], [0])
                self.assertEqual(blind, constructed_character_blind_counts(row["prime_q"]))
        self.assertEqual(list(cyclotomic_polynomial(6)), [1, -1, 1])
        q5 = computation["actual_q5_quartic_certificate"]
        self.assertEqual(q5["prime_prefix_length"], 1_255)
        self.assertEqual(q5["last_prime"], 10_243)
        self.assertEqual(q5["residue_counts"], [1, 313, 313, 317, 311])
        self.assertEqual(q5["antisymmetric_half_vector"], [2, -4])
        self.assertTrue(q5["quartic_character_detects_asymmetry"])
        self.assertFalse(computation["aggregate"]["all_compatible_even_q_divisible_prefixes_excluded"])

    def test_twin_continued_fraction_reduction_and_certificate(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "317333a17662c51bd54e8fe174948df0548dfb1c43a1f41af389c2b02df3dd1d")
        self.assertEqual(computation["derivative_lower_bound"]["rational_bound"], 544)
        digits = computation["continued_fraction_partial_quotients"]
        self.assertEqual(len(digits), TWIN_CF_TERM_COUNT)
        self.assertEqual(digits[:20], [-1, 1, 12, 1, 1, 1, 6, 2, 2, 26, 1, 5, 4, 6, 2, 1, 1, 50, 1, 15])
        rows = computation["certified_convergent_rows"]
        p_minus_two, p_minus_one = 0, 1
        q_minus_two, q_minus_one = 1, 0
        for digit, row in zip(digits, rows, strict=True):
            p = digit * p_minus_one + p_minus_two
            q = digit * q_minus_one + q_minus_two
            self.assertEqual((int(row["convergent_numerator"]), int(row["convergent_denominator"])), (p, q))
            self.assertEqual(gcd(abs(p), q), 1)
            self.assertEqual(int(row["B_1_at_convergent"]), b1_coefficient_form(p, q))
            self.assertFalse(row["unit_coefficient_hit"])
            p_minus_two, p_minus_one = p_minus_one, p
            q_minus_two, q_minus_one = q_minus_one, q
        finite = computation["finite_convergent_audit"]
        self.assertEqual(finite["term_count"], 128)
        self.assertEqual(finite["maximum_excluded_denominator"], "67076610336720215425112731771403002965838278844687475228751003")
        self.assertEqual(finite["maximum_excluded_denominator_digit_count"], 62)
        self.assertEqual(finite["unit_coefficient_hits"], [])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["continued_fraction_necessity_proved"])
        self.assertTrue(aggregate["linear_denominator_scan_necessity_refuted"])
        self.assertFalse(aggregate["all_convergents_excluded"])
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
        integrated = ROOT / "data/open-problem/ticket258-variation-character-convergent.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["ticket"], 258)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 258:
            self.assertEqual(state["parent_ticket"], 257)
            self.assertEqual(state["deep_focus_problem"], "twin_prime")
        expected = {
            "riemann": "BoundedTotalVariationPacketEnergyLagNoGo",
            "collatz": "DistinctPrimeCyclotomicPhaseRationalIndependence",
            "goldbach": "PrimitiveOddCharacterCompletenessClassification",
            "twin_prime": "UnitCoefficientSolutionsAreRootConvergents",
        }
        for key, theorem in expected.items():
            self.assertIn(theorem, state["problems"][key]["established_results"])
            self.assertEqual(state["problems"][key]["stagnation_count"], 0)


if __name__ == "__main__":
    unittest.main()
