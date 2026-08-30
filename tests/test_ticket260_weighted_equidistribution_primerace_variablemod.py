from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket260_weighted_equidistribution_primerace_variablemod import (
    AUDIT_KEY,
    COLLATZ_FIXED_MODULI,
    COLLATZ_TERM_COUNT,
    GOLDBACH_LEVELS,
    SCHEMA,
    TWIN_CONVERGENT_COUNT,
    build_audit,
    summable_demo_energy,
    summable_demo_lag,
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


class Ticket260Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        machine = self.root["machine_audit"]
        expected = {
            "exact_theorem_count": 4,
            "new_partial_theorem_count": 3,
            "exact_no_go_count": 1,
            "candidate_resolution_count": 0,
            "conjecture_resolution_count": 0,
            "proof_dag_count": 4,
            "next_single_lemma_count": 4,
            "deep_focus_problem": "twin_prime",
            "stagnated_problem_count": 0,
            "riemann_weighted_variation_case_count": 16,
            "collatz_phase_case_count": 64,
            "collatz_fixed_modulus_case_count": 15,
            "goldbach_q3_level_count": 3,
            "goldbach_maximum_prefix_length": 28_697_817,
            "goldbach_maximum_endpoint": 547_035_959,
            "goldbach_independent_algorithm_count": 2,
            "twin_convergent_count": 256,
            "twin_first_order_nontrivial_pass_count": 2,
            "twin_second_order_nontrivial_pass_count": 0,
            "twin_maximum_denominator_digit_count": 121,
            "total_failure_count": 0,
        }
        for key, value in expected.items():
            self.assertEqual(machine[key], value)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["partial_theorem", "exact_no_go", "partial_theorem", "partial_theorem"],
        )
        self.assertEqual(
            [attempt["problem_id"] for attempt in self.audit["attempts"]],
            ["riemann", "collatz", "goldbach", "twin-prime"],
        )

    def test_riemann_summable_scaled_variation(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "1fcbc1bb15fcd64f8ce04cd99c19d98ad6dad73dced2e79eb60ed5f19f41beeb",
        )
        self.assertEqual(
            Fraction(computation["weighted_downward_variation_exact"]["exact"]),
            Fraction(1, 3),
        )
        rows = computation["exact_summable_variation_rows"]
        self.assertEqual(len(rows), 16)
        for row in rows:
            n = row["downward_transition_n"]
            self.assertEqual(n, 2 ** row["level_k"])
            self.assertEqual(summable_demo_energy(n + 1), 1 - Fraction(1, n**3))
            self.assertEqual(summable_demo_lag(n), 1 - Fraction(n + 1, n**3))
            self.assertGreater(Fraction(row["lag_partial_sum_S_n"]["exact"]), 0)
            self.assertTrue(row["identity_verified"])
        aggregate = computation["aggregate"]
        self.assertTrue(
            aggregate[
                "summable_scaled_downward_variation_implies_eventual_lag_positivity_proved"
            ]
        )
        self.assertFalse(aggregate["actual_weil_scaled_downward_variation_summable"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_fixed_modulus_equidistribution_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "044392f39a7829cd995fade3f2b9644d524a989631a3f9ce10a908c6fb984d15",
        )
        rows = computation["exact_phase_envelope_rows"]
        self.assertEqual(len(rows), COLLATZ_TERM_COUNT)
        previous_prime = 3
        for row in rows:
            index, prime = row["index_j"], row["prime_order_q_j"]
            self.assertGreater(prime, max(previous_prime, index**3))
            self.assertEqual(row["phase_exponent_d_j"], index)
            self.assertTrue(row["row_verified"])
            previous_prime = prime
        for modulus in COLLATZ_FIXED_MODULI:
            for prefix in range(1, COLLATZ_TERM_COUNT + 1):
                counts = [
                    sum(index % modulus == residue for index in range(1, prefix + 1))
                    for residue in range(modulus)
                ]
                self.assertLessEqual(max(counts) - min(counts), 1)
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["fixed_modulus_exponent_equidistribution_proved"])
        self.assertTrue(aggregate["normalized_phase_sum_tends_to_one_proved"])
        self.assertTrue(
            aggregate["fixed_modulus_equidistribution_implies_cancellation_refuted"]
        )
        self.assertFalse(aggregate["canonical_fermat_quotient_exponents_used"])

    def test_goldbach_q3_prime_race_equivalence_and_certificates(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "bd6146858e8e5587274d75e799d05983d0bf67a2a6ca625fe132e7e52b33c625",
        )
        rows = computation["exact_q3_prime_race_certificate_rows"]
        self.assertEqual([row["level_l"] for row in rows], list(GOLDBACH_LEVELS))
        expected = [
            (0, 6, 57, 269, [1, 25, 31], -6),
            (1, 18, 39_369, 471_749, [1, 19_663, 19_705], -42),
            (2, 30, 28_697_817, 547_035_959, [1, 14_347_849, 14_349_967], -2_118),
        ]
        for row, values in zip(rows, expected):
            level, exponent, length, endpoint, counts, difference = values
            self.assertEqual(
                (
                    row["level_l"],
                    row["exponent_m"],
                    row["forced_prefix_length_T"],
                    row["exact_nth_prime_endpoint"],
                    row["actual_residue_counts"],
                    row["mod_3_prime_race_difference_N1_minus_N2"],
                ),
                (level, exponent, length, endpoint, counts, difference),
            )
            self.assertEqual(
                row["actual_residue_counts"],
                row["independent_segmented_residue_counts"],
            )
            self.assertTrue(row["certificate_verified"])
            self.assertTrue(row["compatible_prefix_excluded"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["q3_compatible_family_prime_race_equivalence_proved"])
        self.assertFalse(aggregate["all_q3_levels_excluded"])
        self.assertFalse(aggregate["strong_goldbach_conjecture_resolved"])

    def test_twin_second_order_variable_denominator_certificate(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "822878ce37c68575312588bd75639f736d9dccf9252b148fcd2170c31ac9c9e8",
        )
        rows = computation["exact_variable_denominator_convergent_rows"]
        self.assertEqual(len(rows), TWIN_CONVERGENT_COUNT)
        for row in rows:
            u = int(row["convergent_numerator"])
            v = int(row["convergent_denominator"])
            coefficient = b1_coefficient_form(u, v)
            self.assertFalse(row["direct_unit_coefficient_hit"])
            self.assertTrue(row["truncated_expansion_matches_direct_B1_mod_v_squared"])
            if v >= 2:
                for sign in row["sign_tests"]:
                    epsilon = sign["epsilon"]
                    expected = (u**17 + 17 * u**16 * v - epsilon) % (v * v)
                    self.assertEqual(
                        int(sign["second_order_residue_mod_v_squared"]), expected
                    )
                    self.assertEqual((coefficient - epsilon) % (v * v), expected)
        first = computation["first_order_nontrivial_passes"]
        self.assertEqual(
            [(row["term_index"], row["epsilon"], int(row["denominator"])) for row in first],
            [(2, -1, 13), (3, -1, 14)],
        )
        self.assertEqual(computation["second_order_nontrivial_passes"], [])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["second_order_denominator_congruence_necessary_proved"])
        self.assertFalse(aggregate["first_order_only_filter_complete"])
        self.assertFalse(aggregate["all_convergents_excluded"])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(dag["acyclic"])
        integrated = (
            ROOT
            / "data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json"
        )
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual((state["ticket"], state["parent_ticket"]), (260, 259))
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "twin_prime")


if __name__ == "__main__":
    unittest.main()
