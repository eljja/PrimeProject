from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket254_diagonal_weighted_reflection_thue import is_prime
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket261_sharpness_weyl_ties_dualcongruence import (
    AUDIT_KEY,
    COLLATZ_CANONICAL_PREFIXES,
    COLLATZ_COUNTERMODEL_COUNT,
    GOLDBACH_ABSTRACT_LEVELS,
    RIEMANN_REPLAY_COUNT,
    SCHEMA,
    TWIN_CONVERGENT_COUNT,
    build_audit,
    fermat_quotient_mod_prime,
    reciprocal_tail_energy,
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


class Ticket261Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        expected = {
            "exact_theorem_count": 4,
            "new_partial_theorem_count": 2,
            "exact_no_go_count": 2,
            "candidate_resolution_count": 0,
            "conjecture_resolution_count": 0,
            "proof_dag_count": 4,
            "next_single_lemma_count": 4,
            "deep_focus_problem": "twin_prime",
            "stagnated_problem_count": 0,
            "riemann_reciprocal_tail_case_count": 128,
            "collatz_countermodel_phase_case_count": 128,
            "collatz_canonical_prefix_count": 16_384,
            "collatz_canonical_dyadic_row_count": 12,
            "goldbach_actual_parity_certificate_count": 3,
            "goldbach_abstract_tie_replay_count": 16,
            "twin_convergent_count": 1024,
            "twin_denominator_first_order_pass_count": 2,
            "twin_numerator_first_order_nontrivial_pass_count": 1,
            "twin_joint_second_order_pass_count": 0,
            "twin_maximum_denominator_digit_count": 519,
            "total_failure_count": 0,
        }
        for key, value in expected.items():
            self.assertEqual(self.root["machine_audit"][key], value)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_summability_necessity_counterfamily(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "8242a67f0d5c2c2b451cef1cb2c48100ffaa008fa05b402ac6274da8a88b670b",
        )
        rows = computation["exact_reciprocal_tail_rows"]
        self.assertEqual(len(rows), RIEMANN_REPLAY_COUNT)
        partial = Fraction(0)
        for row in rows:
            n = row["index_n"]
            energy = reciprocal_tail_energy(n)
            next_energy = reciprocal_tail_energy(n + 1)
            drop = energy - next_energy
            partial += n * drop
            self.assertEqual(drop, Fraction(1, n * (n + 1)))
            self.assertEqual((n + 1) * next_energy - n * energy, 1)
            self.assertEqual(
                Fraction(row["partial_scaled_downward_variation"]["exact"]),
                partial,
            )
            self.assertTrue(row["row_verified"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["summable_scaled_variation_is_necessary_refuted"])
        self.assertFalse(aggregate["actual_weil_packet_used"])

    def test_collatz_first_harmonic_no_go_and_canonical_discrepancy(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "35619c4243f9a4fa6ba7eff5764787d0ee3212d8f9decca0e85938e01b2de750",
        )
        rows = computation["exact_first_harmonic_countermodel_rows"]
        self.assertEqual(len(rows), COLLATZ_COUNTERMODEL_COUNT)
        previous_prime = 13
        for row in rows:
            index = row["index_j"]
            prime = row["prime_modulus_q_j"]
            point = Fraction(row["normalized_point_d_j_over_q_j"]["exact"])
            self.assertTrue(is_prime(prime))
            self.assertGreater(prime, max(previous_prime, index**3))
            self.assertEqual(row["count_in_zero_to_one_third"], (index + 1) // 2)
            self.assertEqual(point < Fraction(1, 3), index % 2 == 1)
            self.assertTrue(row["row_verified"])
            previous_prime = prime
        expected_discrepancies = [
            Fraction(11, 62),
            Fraction(11, 62),
            Fraction(83, 992),
            Fraction(93, 1168),
            Fraction(31, 664),
            Fraction(15015, 396544),
            Fraction(3221, 117632),
            Fraction(134157, 6247424),
            Fraction(111589, 7366144),
            Fraction(656411, 39704576),
            Fraction(70201, 13211648),
            Fraction(5048669, 617562112),
        ]
        canonical = computation["exact_canonical_star_discrepancy_rows"]
        self.assertEqual(
            [row["canonical_prime_prefix_count"] for row in canonical],
            list(COLLATZ_CANONICAL_PREFIXES),
        )
        self.assertEqual(
            [Fraction(row["exact_star_discrepancy"]["exact"]) for row in canonical],
            expected_discrepancies,
        )
        self.assertEqual(
            [row["canonical_prime_prefix_count"] for row in canonical if row["increased_from_previous_dyadic_prefix"]],
            [4096, 16384],
        )
        witness = canonical[-1]["extremal_witness"]
        q = witness["prime_q"]
        expected_d = (
            5 * fermat_quotient_mod_prime(2, q)
            - 3 * fermat_quotient_mod_prime(3, q)
        ) % q
        self.assertEqual(witness["canonical_exponent_D_q"], expected_d)
        self.assertFalse(
            computation["aggregate"]["canonical_angular_discrepancy_tends_to_zero_proved"]
        )

    def test_goldbach_product_parity_and_density_no_go(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "7c01ec5d388159c3ba032b8f87459f71cbd4bc339f2f181ef6bc6113075d810c",
        )
        actual = computation["exact_q3_product_parity_certificate_rows"]
        self.assertEqual([row["level_l"] for row in actual], [0, 1, 2])
        for row in actual:
            counts = row["actual_residue_counts_mod_3"]
            self.assertEqual(row["prime_prefix_product_mod_3_excluding_prime_3"], 2)
            self.assertEqual(counts[2] % 2, 1)
            self.assertEqual(row["tie_would_force_each_nonzero_count"] % 2, 0)
            self.assertTrue(row["minus_one_product_excludes_tie"])
            self.assertTrue(row["independent_residue_algorithms_agree"])
            self.assertTrue(row["row_verified"])
        abstract = computation["exact_density_only_tie_countermodel_rows"]
        self.assertEqual([row["level_l"] for row in abstract], list(GOLDBACH_ABSTRACT_LEVELS))
        for row in abstract:
            self.assertEqual(row["alternating_plus_count"], row["alternating_minus_count"])
            self.assertEqual(row["prefix_difference"], 0)
            self.assertEqual(row["abstract_product_mod_3"], 1)
            self.assertTrue(row["special_tie_verified"])
        self.assertFalse(
            computation["aggregate"]["all_special_prime_prefix_products_minus_one_proved"]
        )

    def test_twin_bidirectional_second_order_certificate(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "3327f229884ca78a1b95a3b2336cc245e4e99cbfff8f2020a24db3299754b70e",
        )
        rows = computation["exact_bidirectional_convergent_rows"]
        self.assertEqual(len(rows), TWIN_CONVERGENT_COUNT)
        for row in rows:
            u = int(row["convergent_numerator"])
            v = int(row["convergent_denominator"])
            coefficient = b1_coefficient_form(u, v)
            self.assertEqual(
                row["B_1_value_sha256"],
                hashlib.sha256(str(coefficient).encode("ascii")).hexdigest(),
            )
            self.assertFalse(row["direct_unit_coefficient_hit"])
            self.assertTrue(row["both_truncated_expansions_match_direct_B1"])
            for sign in row["sign_tests"]:
                epsilon = sign["epsilon"]
                expected_v = (u**17 + 17 * u**16 * v - epsilon) % (v * v)
                self.assertEqual(
                    int(sign["denominator_second_residue_mod_v_squared"]),
                    expected_v,
                )
                self.assertEqual((coefficient - epsilon) % (v * v), expected_v)
                if u:
                    expected_u = (
                        256 * v**17 + 4352 * u * v**16 - epsilon
                    ) % (u * u)
                    self.assertEqual(
                        int(sign["numerator_second_residue_mod_u_squared"]),
                        expected_u,
                    )
                    self.assertEqual((coefficient - epsilon) % (u * u), expected_u)
        self.assertEqual(
            [
                (r["term_index"], r["epsilon"], int(r["numerator"]), int(r["denominator"]))
                for r in computation["denominator_first_order_nontrivial_passes"]
            ],
            [(2, -1, -1, 13), (3, -1, -1, 14)],
        )
        self.assertEqual(
            [
                (r["term_index"], r["epsilon"], int(r["numerator"]), int(r["denominator"]))
                for r in computation["numerator_first_order_nontrivial_passes"]
            ],
            [(5, -1, -3, 41)],
        )
        self.assertEqual(computation["joint_second_order_passes"], [])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual((state["ticket"], state["parent_ticket"]), (261, 260))
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "twin_prime")


if __name__ == "__main__":
    unittest.main()
