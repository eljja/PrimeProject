from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket254_diagonal_weighted_reflection_thue import is_prime
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket262_limsup_finiteharmonic_mod8_thirdorder import (
    AUDIT_KEY,
    COLLATZ_BLOCK_COUNT,
    COLLATZ_HARMONIC_CUTOFFS,
    GOLDBACH_ABSTRACT_LEVELS,
    RIEMANN_CRITICAL_COUNT,
    RIEMANN_REPLAY_COUNT,
    SCHEMA,
    TWIN_CONVERGENT_COUNT,
    build_audit,
    least_prime_above,
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


class Ticket262Tests(unittest.TestCase):
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
            "new_partial_theorem_count": 3,
            "exact_no_go_count": 1,
            "candidate_resolution_count": 0,
            "conjecture_resolution_count": 0,
            "proof_dag_count": 4,
            "next_single_lemma_count": 4,
            "deep_focus_problem": "collatz",
            "stagnated_problem_count": 0,
            "riemann_strict_boundary_case_count": 64,
            "riemann_critical_boundary_case_count": 12,
            "collatz_harmonic_cutoff_replay_count": 5,
            "collatz_total_phase_case_count": 1152,
            "goldbach_actual_mod8_certificate_count": 3,
            "goldbach_sharpness_countermodel_count": 16,
            "twin_convergent_count": 1024,
            "twin_joint_third_order_pass_count": 0,
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
            ["partial_theorem", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_exact_limsup_boundary_replays(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "1d0e796a1808951ac38617fabf4e338df387ff4653b8c1f9461e2e211b2c2e95",
        )
        strict = computation["exact_reciprocal_tail_identity_rows"]
        critical = computation["exact_critical_boundary_rows"]
        self.assertEqual(len(strict), RIEMANN_REPLAY_COUNT)
        self.assertEqual(len(critical), RIEMANN_CRITICAL_COUNT)
        for row in strict:
            n = row["index_n"]
            energy = Fraction(n + 1, n)
            next_energy = Fraction(n + 2, n + 1)
            jump = n * (energy - next_energy)
            lag = (n + 1) * next_energy - n * energy
            self.assertEqual(jump, Fraction(1, n + 1))
            self.assertEqual(lag, next_energy - jump)
            self.assertEqual(lag, 1)
            self.assertTrue(row["row_verified"])
        for row in critical:
            n = 4 ** row["power_k"]
            self.assertEqual(row["index_n"], n)
            self.assertEqual(
                Fraction(row["lag_S_n"]["exact"]), -Fraction(1, n)
            )
            self.assertTrue(row["critical_equality_verified"])
        self.assertFalse(
            computation["aggregate"]["actual_weil_packet_limsup_bound_proved"]
        )

    def test_collatz_every_fixed_finite_harmonic_cutoff_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "fc9aa7f31e40f14a0005fe7d75fc732aca63add7bee8ff6fa258f4e733f4d023",
        )
        cases = computation["exact_finite_harmonic_cutoff_cases"]
        self.assertEqual(
            [case["harmonic_cutoff_H"] for case in cases],
            list(COLLATZ_HARMONIC_CUTOFFS),
        )
        phase_total = 0
        for case in cases:
            cutoff = case["harmonic_cutoff_H"]
            modulus = cutoff + 1
            phase_count = COLLATZ_BLOCK_COUNT * modulus
            phase_total += phase_count
            previous_prime = 8 * modulus
            interval_count = 0
            reciprocal_sum = Fraction(0)
            residues = [0] * modulus
            for index in range(1, phase_count + 1):
                prime = least_prime_above(max(previous_prime, index**3, 8 * modulus))
                previous_prime = prime
                residue = (index - 1) % modulus
                exponent = (prime * (2 * residue + 1)) // (2 * modulus)
                point = Fraction(exponent, prime)
                self.assertTrue(is_prime(prime))
                self.assertGreater(prime, index**3)
                self.assertLess(Fraction(2 * residue + 1, 2 * modulus) - point, Fraction(1, prime))
                residues[residue] += 1
                interval_count += int(point < Fraction(3, 4 * modulus))
                reciprocal_sum += Fraction(1, prime)
            self.assertEqual(residues, [COLLATZ_BLOCK_COUNT] * modulus)
            self.assertEqual(interval_count, COLLATZ_BLOCK_COUNT)
            self.assertEqual(
                Fraction(case["star_discrepancy_lower_bound"]["exact"]),
                Fraction(1, 4 * modulus),
            )
            for harmonic_row in case["harmonic_rows"]:
                h = harmonic_row["harmonic_h"]
                self.assertNotEqual(h % modulus, 0)
                self.assertTrue(harmonic_row["ideal_complete_block_sum_zero"])
                self.assertEqual(
                    Fraction(harmonic_row["normalized_chord_error_upper_bound"]["exact"]),
                    8 * h * reciprocal_sum / phase_count,
                )
            self.assertTrue(case["case_verified"])
        self.assertEqual(phase_total, 1152)
        self.assertFalse(
            computation["aggregate"]["canonical_all_nonzero_harmonic_cancellation_proved"]
        )

    def test_goldbach_mod8_necessity_and_two_sharpness_models(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "7c60dd5c0e26f01fcd138fba2088f29872ee60b43e25efe5fc6dbad0cce5e00f",
        )
        actual = computation["exact_q3_mod8_certificate_rows"]
        self.assertEqual([row["level_l"] for row in actual], [0, 1, 2])
        self.assertEqual(
            [row["minus_one_residue_count_mod_8"] for row in actual],
            [7, 1, 7],
        )
        for row in actual:
            level = row["level_l"]
            tie_count = 3 ** (6 * level + 3) + 1
            self.assertEqual(row["tie_would_force_each_nonzero_count"], tie_count)
            self.assertEqual(tie_count % 8, 4)
            self.assertTrue(row["tie_excluded_by_mod_8_contrapositive"])
            self.assertTrue(row["independent_residue_algorithms_agree"])
            self.assertTrue(row["row_verified"])
        abstract = computation["exact_sharpness_countermodel_rows"]
        self.assertEqual([row["level_l"] for row in abstract], list(GOLDBACH_ABSTRACT_LEVELS))
        for row in abstract:
            first = row["product_plus_one_but_non_tie_counts"]
            second = row["N_2_congruent_four_but_non_tie_counts"]
            self.assertEqual(first["product_mod_3"], 1)
            self.assertNotEqual(first["N_1"], first["N_2"])
            self.assertEqual(second["N_2_mod_8"], 4)
            self.assertNotEqual(second["N_1"], second["N_2"])
            self.assertTrue(row["row_verified"])

    def test_twin_bidirectional_third_order_certificate(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "50287b950ca162a0f762bbe7b4ba0d0898871947e950e7e1f52168d4f5e197cd",
        )
        rows = computation["exact_bidirectional_third_order_convergent_rows"]
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
            self.assertTrue(row["both_third_order_expansions_match_direct_B1"])
            for sign in row["sign_tests"]:
                epsilon = sign["epsilon"]
                expected_v = (
                    u**17 + 17 * u**16 * v + 272 * u**15 * v**2 - epsilon
                ) % v**3
                self.assertEqual(
                    int(sign["denominator_third_residue_mod_v_cubed"]), expected_v
                )
                self.assertEqual((coefficient - epsilon) % v**3, expected_v)
                if u:
                    expected_u = (
                        256 * v**17
                        + 4352 * u * v**16
                        + 17408 * u**2 * v**15
                        - epsilon
                    ) % abs(u) ** 3
                    self.assertEqual(
                        int(sign["numerator_third_residue_mod_u_cubed"]), expected_u
                    )
                    self.assertEqual((coefficient - epsilon) % abs(u) ** 3, expected_u)
        self.assertEqual(computation["denominator_third_order_nontrivial_passes"], [])
        self.assertEqual(computation["numerator_third_order_nontrivial_passes"], [])
        self.assertEqual(computation["joint_third_order_passes"], [])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual((state["ticket"], state["parent_ticket"]), (262, 261))
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertFalse(state["program_complete"])
        self.assertEqual(state["deep_focus_problem"], "collatz")


if __name__ == "__main__":
    unittest.main()
