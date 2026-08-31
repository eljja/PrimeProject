from __future__ import annotations

import hashlib
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket264_asymmetric_threshold_fixed2adic_head import (
    AUDIT_KEY,
    COLLATZ_GRID_SIZES,
    GOLDBACH_MODULUS_EXPONENTS,
    RIEMANN_ONE_SIDED_PAIRS,
    RIEMANN_REPLAY_COUNT,
    SCHEMA,
    TWIN_EXACTNESS_THRESHOLD,
    build_audit,
)


sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


class Ticket264Tests(unittest.TestCase):
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
            "deep_focus_problem": "riemann",
            "stagnated_problem_count": 0,
            "riemann_replay_case_count": 192,
            "collatz_grid_replay_count": 6,
            "collatz_harmonic_threshold_case_count": 252,
            "goldbach_phase_period_replay_count": 16,
            "goldbach_fixed_modulus_countermodel_count": 242,
            "twin_head_certificate_row_count": 39,
            "twin_subthreshold_convergent_count": 38,
            "twin_first_above_threshold_term_index": 38,
            "total_failure_count": 0,
        }
        self.assertEqual(self.root["machine_audit"], expected)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["partial_theorem", "partial_theorem", "exact_no_go", "partial_theorem"],
        )

    def test_riemann_asymmetric_sharp_bound(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "6e19883f2161d8c5b312d882bd9b273885f7a6a70acb2045d979b1796623099a",
        )
        families = computation["exact_asymmetric_reciprocal_families"]
        self.assertEqual(len(families), len(RIEMANN_ONE_SIDED_PAIRS))
        for family, (positive, negative) in zip(families, RIEMANN_ONE_SIDED_PAIRS, strict=True):
            self.assertEqual(Fraction(family["envelope_sum"]["exact"]), positive + negative)
            self.assertEqual(len(family["exact_rows"]), RIEMANN_REPLAY_COUNT)
            for row in family["exact_rows"]:
                n = row["index_n"]
                expected_lag = 1 - positive - negative if n % 2 == 0 else 1 + positive + negative
                self.assertEqual(Fraction(row["lag_S_n"]["exact"]), expected_lag)
                self.assertTrue(row["row_verified"])
        self.assertEqual([row["regime"] for row in families], ["strict", "critical", "supercritical"])
        self.assertTrue(computation["aggregate"]["joint_coefficient_one_sharp_proved"])
        self.assertFalse(computation["aggregate"]["actual_weil_one_sided_envelope_sum_below_limit_proved"])

    def test_collatz_explicit_threshold_cutoff(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "eff593194a2fdaa1dc70665a18cfe69598bde8468da4135f2d41e6195e5902eb",
        )
        rows = computation["exact_complete_grid_threshold_replays"]
        self.assertEqual([row["complete_grid_size_N"] for row in rows], list(COLLATZ_GRID_SIZES))
        for row in rows:
            modulus = row["complete_grid_size_N"]
            self.assertEqual(row["canonical_threshold_cutoff_K_N"], modulus - 1)
            for item in row["harmonic_tests"]:
                h = item["harmonic_h"]
                expected = Fraction(1 if h % modulus == 0 else 0)
                self.assertEqual(Fraction(item["normalized_weyl_magnitude_squared"]["exact"]), expected)
                self.assertEqual(item["threshold_one_over_h_squared_pass"], h < modulus)
        self.assertFalse(computation["aggregate"]["canonical_fermat_quotient_threshold_cutoff_diverges_proved"])

    def test_goldbach_all_fixed_two_adic_no_go(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "2e35b078945a1ddc732a322fb6aa44941ad6d3706f374991f62f2d64b0d5c3fb",
        )
        phases = computation["exact_two_adic_phase_period_rows"]
        self.assertEqual([row["modulus_exponent_m"] for row in phases], list(GOLDBACH_MODULUS_EXPONENTS))
        for row in phases:
            m = row["modulus_exponent_m"]
            period = 1 if m <= 3 else 2 ** (m - 3)
            modulus = 2**m
            self.assertEqual(row["least_level_period"], period)
            self.assertEqual(
                row["one_period_tie_residues"],
                [(3 ** (6 * level + 3) + 1) % modulus for level in range(period)],
            )
            self.assertTrue(row["period_verified"])
        for row in computation["exact_fixed_modulus_nontie_countermodels"]:
            m = row["modulus_exponent_m"]
            level = row["level_l"]
            middle = 3 ** (6 * level + 3) + 1
            self.assertEqual(int(row["abstract_N_1"]), middle - 2**m)
            self.assertEqual(int(row["abstract_N_2"]), middle + 2**m)
            self.assertTrue(row["same_total_as_tie"] and row["non_tie"] and row["row_verified"])
        self.assertFalse(computation["aggregate"]["actual_q3_special_prime_race_nonvanishing_proved"])

    def test_twin_complete_subthreshold_head(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "53b7d19352a60fad2e2c26ec11b6f4d9cf5b3e3a879620251b024171657ccaf6",
        )
        rows = computation["exact_head_and_crossing_rows"]
        self.assertEqual(len(rows), 39)
        self.assertEqual(sum(row["at_or_below_exactness_threshold"] for row in rows), 38)
        for row in rows:
            u = int(row["convergent_numerator"])
            v = int(row["convergent_denominator"])
            value = b1_coefficient_form(u, v)
            self.assertEqual(int(row["B_1_value"]), value)
            self.assertEqual(row["B_1_value_sha256"], hashlib.sha256(str(value).encode("ascii")).hexdigest())
            if v <= TWIN_EXACTNESS_THRESHOLD:
                self.assertNotEqual(abs(value), 1)
                self.assertTrue(row["direct_unit_free"])
        self.assertEqual(int(rows[37]["convergent_denominator"]), 110221790993960069)
        self.assertEqual(int(rows[38]["convergent_denominator"]), 309742427372962732)
        self.assertLessEqual(int(rows[37]["convergent_denominator"]), TWIN_EXACTNESS_THRESHOLD)
        self.assertGreater(int(rows[38]["convergent_denominator"]), TWIN_EXACTNESS_THRESHOLD)
        self.assertFalse(computation["aggregate"]["all_unique_root_convergents_excluded"])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["ticket"], 264)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertIn(state["deep_focus_problem"], state["problems"])
        self.assertFalse(state["program_complete"])


if __name__ == "__main__":
    unittest.main()
