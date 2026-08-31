from __future__ import annotations

import hashlib
import json
import sys
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path

from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import certified_root_continued_fraction
from scripts.ticket265_sparse_cutoff_growing2adic_mod32 import (
    AUDIT_KEY,
    COLLATZ_DYADIC_MODULI,
    GOLDBACH_LEVELS,
    RIEMANN_LIMIT,
    RIEMANN_NEGATIVE_SPIKE,
    RIEMANN_POSITIVE_SPIKE,
    RIEMANN_SPIKE_EXPONENTS,
    SCHEMA,
    TWIN_CONVERGENT_COUNT,
    build_audit,
)


sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket265Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        self.assertEqual(
            self.root["machine_audit"],
            {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "collatz",
                "stagnated_problem_count": 0,
                "riemann_sparse_spike_replay_count": 16,
                "collatz_dyadic_good_bad_replay_count": 9,
                "goldbach_symbolic_threshold_replay_count": 32,
                "goldbach_lower_exponent_countermodel_count": 32,
                "goldbach_inherited_actual_certificate_count": 3,
                "twin_certified_convergent_count": 1024,
                "twin_either_sign_filter_count": 35,
                "twin_later_either_sign_filter_count": 33,
                "total_failure_count": 0,
            },
        )
        self.assertEqual(
            [self.root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )

    def test_riemann_sparse_density_one_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "5a346cdb311835e55975d7658b1300b4a63e330d092e9905a64d5b2b45a1154e")
        rows = computation["exact_sparse_reciprocal_spike_rows"]
        self.assertEqual([row["spike_exponent_k"] for row in rows], list(RIEMANN_SPIKE_EXPONENTS))
        for row in rows:
            n = row["positive_spike_index_n"]
            self.assertEqual(Fraction(row["scaled_positive_error"]["exact"]), RIEMANN_POSITIVE_SPIKE)
            self.assertEqual(Fraction(row["scaled_negative_error"]["exact"]), RIEMANN_NEGATIVE_SPIKE)
            self.assertEqual(
                Fraction(row["lag_S_n"]["exact"]),
                RIEMANN_LIMIT - RIEMANN_POSITIVE_SPIKE - RIEMANN_NEGATIVE_SPIKE,
            )
            self.assertEqual(row["zero_error_gap_before_next_pair"], n - 2)
            self.assertTrue(row["row_verified"])

    def test_collatz_good_bad_dyadic_prefixes(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "d59a4440065a0be5da37bb2fd930a5961bb4da94505c4d35498f793d6a513ae0")
        rows = computation["exact_dyadic_good_bad_prefix_rows"]
        self.assertEqual([row["dyadic_grid_modulus_q"] for row in rows], list(COLLATZ_DYADIC_MODULI))
        for row in rows:
            q = row["dyadic_grid_modulus_q"]
            self.assertEqual(row["exact_good_cutoff_K_N"], q - 1)
            self.assertEqual(row["positive_arc_bad_prefix_N"], 3 * q // 4)
            self.assertEqual(row["positive_arc_new_odd_root_count"], q // 4)
            self.assertGreater(Fraction(row["exact_rational_lower_bound_for_abs_W_N_1"]["exact"]), Fraction(1, 6))
            self.assertLessEqual(row["bad_prefix_cutoff_upper_bound"], 5)
            self.assertTrue(row["row_verified"])

    def test_goldbach_least_decisive_growing_modulus(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "226b63fbf8d4a6e057a54aa9a2d33bdd957809975781e5e7ff5e49275fcdb82c")
        for row, level in zip(computation["exact_growing_modulus_threshold_rows"], GOLDBACH_LEVELS, strict=True):
            middle = 3 ** (6 * level + 3) + 1
            exponent = middle.bit_length()
            self.assertEqual(int(row["tie_count_M_l"]), middle)
            self.assertEqual(row["least_decisive_exponent_m_l"], exponent)
            self.assertLessEqual(2 ** (exponent - 1), middle)
            self.assertLess(middle, 2**exponent)
        for row in computation["sharp_lower_exponent_nontie_countermodels"]:
            middle = int(row["tie_count_M_l"])
            shift = 2 ** row["insufficient_exponent_m_l_minus_1"]
            n1, n2 = int(row["abstract_N_1"]), int(row["abstract_N_2"])
            self.assertEqual((n1, n2), (middle - shift, middle + shift))
            self.assertEqual(n1 + n2, 2 * middle)
            self.assertEqual(n2 % shift, middle % shift)
            self.assertNotEqual(n1, n2)
        source_path = ROOT / computation["inherited_source"]["path"]
        self.assertEqual(hashlib.sha256(source_path.read_bytes()).hexdigest(), computation["inherited_source"]["sha256"])
        self.assertTrue(all(row["decisive_residue_mismatch"] for row in computation["inherited_actual_decisive_residue_rows"]))

    def test_twin_mod32_filter_and_countermodels(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "ac6c6393114bfa59bb25827d6639ddfc87e8cb05e9f98382fad13ef0963a8c88")
        self.assertTrue(all(row["minimum_two_adic_valuation_when_v_even"] >= 5 for row in computation["exact_two_adic_valuation_rows"]))
        for row in computation["explicit_filter_insufficiency_countermodels"]:
            plus_u, plus_v = row["plus_pair_u_v"]
            minus_u, minus_v = row["minus_pair_u_v"]
            self.assertEqual(gcd(plus_u, plus_v), 1)
            self.assertEqual((plus_u + plus_v) % 32, 1)
            self.assertEqual((minus_u + minus_v) % 32, 31)
            self.assertGreater(b1_coefficient_form(plus_u, plus_v), 1)
            self.assertLess(b1_coefficient_form(minus_u, minus_v), -1)
        _, source_rows, _, _ = certified_root_continued_fraction(TWIN_CONVERGENT_COUNT)
        rows = computation["certified_convergent_mod32_filter_rows"]
        self.assertEqual(len(rows), TWIN_CONVERGENT_COUNT)
        for source, row in zip(source_rows, rows, strict=True):
            u, v = int(source["convergent_numerator"]), int(source["convergent_denominator"])
            value = b1_coefficient_form(u, v)
            self.assertEqual(row["B_1_value_sha256"], hashlib.sha256(str(value).encode("ascii")).hexdigest())
            if abs(value) == 1:
                self.assertTrue(row["denominator_even"])
                self.assertEqual((u + v) % 32, value % 32)
        self.assertEqual(computation["aggregate"]["either_sign_filter_count"], 35)
        self.assertEqual(computation["aggregate"]["later_either_sign_filter_count"], 33)

    def test_dags_outputs_and_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertEqual((state["ticket"], state["parent_ticket"]), (265, 264))
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertEqual(state["deep_focus_problem"], "collatz")
        self.assertFalse(state["program_complete"])


if __name__ == "__main__":
    unittest.main()
