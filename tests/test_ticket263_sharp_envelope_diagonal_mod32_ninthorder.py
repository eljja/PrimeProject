from __future__ import annotations

import hashlib
import json
import sys
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path

from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket263_sharp_envelope_diagonal_mod32_ninthorder import (
    AUDIT_KEY,
    COLLATZ_GRID_SIZES,
    GOLDBACH_ABSTRACT_LEVELS,
    RIEMANN_AMPLITUDES,
    RIEMANN_REPLAY_COUNT,
    SCHEMA,
    TWIN_ABSOLUTE_COEFFICIENT_SUM,
    TWIN_COEFFICIENTS,
    TWIN_CONVERGENT_COUNT,
    TWIN_EXACTNESS_THRESHOLD,
    TWIN_JET_ORDER,
    build_audit,
)


sys.set_int_max_str_digits(0)
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


class Ticket263Tests(unittest.TestCase):
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
            "new_partial_theorem_count": 4,
            "exact_no_go_count": 0,
            "candidate_resolution_count": 0,
            "conjecture_resolution_count": 0,
            "proof_dag_count": 4,
            "next_single_lemma_count": 4,
            "deep_focus_problem": "twin_prime",
            "stagnated_problem_count": 0,
            "riemann_replay_case_count": 192,
            "collatz_grid_replay_count": 5,
            "collatz_harmonic_case_count": 119,
            "goldbach_actual_mod32_certificate_count": 3,
            "goldbach_mod32_countermodel_count": 15,
            "twin_convergent_count": 1024,
            "twin_tail_exactness_applicable_count": 986,
            "twin_first_tail_exactness_term_index": 38,
            "twin_joint_ninth_order_pass_count": 0,
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
            ["partial_theorem"] * 4,
        )

    def test_riemann_sharp_reciprocal_envelope(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "419e873421db459aa17b81d92e6436b160c67faf03604f4d70f999a606c40fc1",
        )
        families = computation["exact_alternating_reciprocal_envelope_families"]
        self.assertEqual(len(families), len(RIEMANN_AMPLITUDES))
        for family, amplitude in zip(families, RIEMANN_AMPLITUDES, strict=True):
            self.assertEqual(Fraction(family["reciprocal_envelope_A"]["exact"]), amplitude)
            self.assertEqual(len(family["exact_rows"]), RIEMANN_REPLAY_COUNT)
            for row in family["exact_rows"]:
                n = row["index_n"]
                sign = -1 if n % 2 else 1
                self.assertEqual(Fraction(row["scaled_absolute_error"]["exact"]), amplitude)
                self.assertEqual(
                    Fraction(row["scaled_signed_jump_J_n"]["exact"]),
                    sign * amplitude * Fraction(2 * n + 1, n + 1),
                )
                self.assertEqual(
                    Fraction(row["lag_S_n"]["exact"]), 1 - 2 * sign * amplitude
                )
                self.assertTrue(row["row_verified"])
        self.assertTrue(computation["aggregate"]["optimal_factor_two_proved"])
        self.assertFalse(computation["aggregate"]["actual_weil_reciprocal_envelope_proved"])

    def test_collatz_diagonal_uniformization_replay(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "22e5034bb28e5a95a31566c5c5d2b39817d88920c3cdb56add478f8b4364707e",
        )
        cases = computation["exact_complete_grid_replays"]
        self.assertEqual([row["grid_modulus_M"] for row in cases], list(COLLATZ_GRID_SIZES))
        self.assertEqual(sum(len(row["harmonic_rows"]) for row in cases), 119)
        for row in cases:
            modulus = row["grid_modulus_M"]
            self.assertEqual(row["residue_counts"], [1] * modulus)
            self.assertEqual(Fraction(row["exact_star_discrepancy"]["exact"]), Fraction(1, modulus))
            for harmonic in row["harmonic_rows"]:
                self.assertNotEqual(harmonic["harmonic_h"] % modulus, 0)
                self.assertTrue(harmonic["complete_root_sum_zero"])
                self.assertEqual(
                    Fraction(harmonic["normalized_weyl_magnitude_squared"]["exact"]),
                    0,
                )
        self.assertFalse(
            computation["aggregate"]["canonical_growing_cutoff_uniform_cancellation_proved"]
        )

    def test_goldbach_level_phased_mod32_and_countermodels(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "56e7343267be9727182a5823af00472ac99896a1cdda8a6a381005135aebfd42",
        )
        actual = computation["exact_actual_q3_mod32_certificate_rows"]
        self.assertEqual([row["actual_N_2_mod_32"] for row in actual], [31, 25, 15])
        self.assertEqual([row["tie_forced_mod_32"] for row in actual], [28, 4, 12])
        self.assertTrue(all(row["tie_excluded_by_mod_32_contrapositive"] for row in actual))
        symbolic = computation["exact_symbolic_mod32_phase_rows"]
        self.assertEqual([row["level_l"] for row in symbolic], list(GOLDBACH_ABSTRACT_LEVELS))
        phase = [28, 4, 12, 20]
        for row in symbolic:
            level = row["level_l"]
            tie_count = 3 ** (6 * level + 3) + 1
            self.assertEqual(row["tie_forced_mod_32"], phase[level % 4])
            self.assertEqual(tie_count % 32, phase[level % 4])
            self.assertTrue(row["exact_two_adic_valuation_two"])
        countermodels = computation["exact_mod32_nonsufficiency_countermodels"]
        self.assertEqual([row["level_l"] for row in countermodels], list(range(1, 16)))
        for row in countermodels:
            self.assertTrue(row["same_total_as_tie"])
            self.assertTrue(row["non_tie"])
            self.assertTrue(row["row_verified"])

    def test_twin_ninth_order_tail_exactness_certificate(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "fc07b6910a4ad7e83a0df7b467e2b864a9d35c342d6628c97365bfa43fc1352e",
        )
        self.assertEqual(TWIN_ABSOLUTE_COEFFICIENT_SUM, 2744210)
        self.assertEqual(TWIN_EXACTNESS_THRESHOLD, 188580743973175296)
        self.assertEqual(computation["coefficient_vector_a_0_through_a_17"], list(TWIN_COEFFICIENTS))
        rows = computation["exact_ninth_order_convergent_rows"]
        self.assertEqual(len(rows), TWIN_CONVERGENT_COUNT)
        applicable = 0
        first_applicable = None
        nontrivial_passes = []
        for row in rows:
            u = int(row["convergent_numerator"])
            v = int(row["convergent_denominator"])
            coefficient = b1_coefficient_form(u, v)
            self.assertEqual(gcd(abs(u), v), 1)
            self.assertEqual(
                row["B_1_value_sha256"],
                hashlib.sha256(str(coefficient).encode("ascii")).hexdigest(),
            )
            if row["tail_exactness_theorem_applicable"]:
                applicable += 1
                if first_applicable is None:
                    first_applicable = row["term_index"]
                self.assertGreater(v, TWIN_EXACTNESS_THRESHOLD)
                self.assertGreaterEqual(16 * abs(u), v)
                self.assertLessEqual(abs(u), v)
                self.assertLess(
                    (TWIN_ABSOLUTE_COEFFICIENT_SUM + 1) * v**17,
                    (abs(u) * v) ** TWIN_JET_ORDER,
                )
            for sign in row["sign_tests"]:
                epsilon = sign["epsilon"]
                difference = coefficient - epsilon
                expected = []
                for order in range(1, TWIN_JET_ORDER + 1):
                    joint = u != 0 and difference % v**order == 0 and difference % abs(u) ** order == 0
                    expected.append(joint)
                self.assertEqual(sign["joint_pass_by_order_1_through_9"], expected)
                self.assertTrue(sign["ninth_order_expansions_match_direct_B1"])
                if abs(u) >= 2 and v >= 2 and expected[-1]:
                    nontrivial_passes.append((row["term_index"], epsilon))
        self.assertEqual((applicable, first_applicable), (986, 38))
        self.assertEqual(nontrivial_passes, [])
        self.assertEqual(computation["joint_ninth_order_passes"], [])
        self.assertEqual(
            len(computation["degenerate_modulus_one_joint_ninth_order_passes"]), 2
        )
        self.assertFalse(computation["aggregate"]["all_unique_root_convergents_excluded"])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual((state["ticket"], state["parent_ticket"]), (263, 262))
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertEqual(state["deep_focus_problem"], "twin_prime")
        self.assertFalse(state["program_complete"])


if __name__ == "__main__":
    unittest.main()
