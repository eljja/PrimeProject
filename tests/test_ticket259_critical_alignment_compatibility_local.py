from __future__ import annotations

import json
import unittest
from fractions import Fraction
from math import gcd
from pathlib import Path

from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket259_critical_alignment_compatibility_local import (
    AUDIT_KEY, COLLATZ_PRIME_LIMIT, GOLDBACH_PREFIX_T, SCHEMA,
    TWIN_ROOT_LOWER, TWIN_ROOT_UPPER, build_audit, compatibility_record,
    critical_energy, critical_lag_partial_sum,
)

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"proved", "disproved", "computed_finite", "external_theorem", "assumption", "heuristic", "open"}


class Ticket259Tests(unittest.TestCase):
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
            "exact_theorem_count": 4, "new_partial_theorem_count": 1,
            "exact_no_go_count": 3, "candidate_resolution_count": 0,
            "conjecture_resolution_count": 0, "proof_dag_count": 4,
            "next_single_lemma_count": 4, "deep_focus_problem": "goldbach",
            "stagnated_problem_count": 0, "total_failure_count": 0,
        }
        for key, value in expected.items():
            self.assertEqual(machine[key], value)
        self.assertEqual(
            [self.root[key]["result_classification"] for key in ("riemann", "collatz", "goldbach", "twin_prime")],
            ["exact_no_go", "exact_no_go", "partial_theorem", "exact_no_go"],
        )
        self.assertEqual(
            [attempt["problem_id"] for attempt in self.audit["attempts"]],
            ["riemann", "collatz", "goldbach", "twin-prime"],
        )

    def test_riemann_critical_equality_no_go(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "aa676e636fbf50546075b2cd12b026a73f9f3a3a12554032b7323a229cc38441")
        self.assertEqual(Fraction(computation["total_variation_exact"]["exact"]), Fraction(2, 3))
        rows = computation["exact_critical_threshold_rows"]
        self.assertEqual(len(rows), 12)
        for row in rows:
            n = row["downward_transition_n"]
            self.assertEqual(n, 4 ** row["level_k"])
            self.assertEqual(critical_energy(n + 1), 1 - Fraction(1, n))
            self.assertEqual(critical_lag_partial_sum(n), -Fraction(1, n))
            self.assertEqual(Fraction(row["scaled_downward_jump_n_times_drop"]["exact"]), 1)
            self.assertTrue(row["identity_verified"])
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["nonstrict_critical_threshold_route_refuted"])
        self.assertFalse(aggregate["actual_weil_packet_analyzed"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_alignment_no_go(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "1ee64aea8a3265150d2928074b69d57a931be3e9426e0252750c7d15a46ae73c")
        rows = computation["exact_alignment_envelope_rows"]
        self.assertEqual((len(rows), rows[-1]["prime_order_q_N"]), (166, COLLATZ_PRIME_LIMIT))
        self.assertTrue(all(row["envelope_verified"] for row in rows))
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["normalized_phase_sum_tends_to_one_proved"])
        self.assertTrue(aggregate["sublinear_from_order_data_alone_refuted"])
        self.assertFalse(aggregate["canonical_fermat_quotient_exponents_used"])
        self.assertFalse(aggregate["canonical_sublinear_phase_sum_proved"])

    def test_goldbach_classification_and_q13_certificate(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "d20605cd3390770e05234eab2c4a433b023457ac354ab2cd16a4ad87d18caf84")
        rows = computation["exact_compatibility_classification_rows"]
        self.assertEqual(len(rows), 208)
        for row in rows:
            self.assertEqual(row, compatibility_record(row["prime_q"], row["ratio_s_equals_m_over_q"]))
            self.assertEqual(row["compatible"], row["ratio_s_equals_m_over_q"] % 4 == 2)
        certificate = computation["q13_m26_exact_prime_prefix_certificate"]
        counts = [1, 11267061, 11268282, 11267049, 11267171, 11266891, 11267204, 11267666, 11267232, 11267306, 11266978, 11266998, 11267948]
        self.assertEqual(certificate["forced_total_prime_count_T"], GOLDBACH_PREFIX_T)
        self.assertEqual(certificate["exact_nth_prime_endpoint"], 2_798_637_773)
        self.assertEqual(certificate["prime_pi_before_endpoint"], GOLDBACH_PREFIX_T - 1)
        self.assertEqual(certificate["actual_first_T_prime_residue_counts"], counts)
        self.assertEqual(certificate["independent_direct_segmented_counts"], counts)
        self.assertEqual(certificate["actual_reflection_differences"], [0, -887, 1284, 71, -135, -341, -462, 462, 341, 135, -71, -1284, 887])
        self.assertEqual(certificate["primitive_odd_character_moment_remainder"], [-958, 1746, -64, -121])
        self.assertTrue(certificate["certificate_verified"])
        self.assertFalse(computation["aggregate"]["all_compatible_even_q_divisible_prefixes_excluded"])

    def test_twin_fixed_local_window_no_go(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(computation["transcript_sha256"], "8d11c60fee0923ead2f28e5ec4e2f422ff1d8014f42a3b7ea19d24a7475f992d")
        rows = computation["exact_local_witness_rows"]
        self.assertEqual(len(rows), 30)
        for row in rows:
            modulus = row["modulus_M"]
            u, v = int(row["primitive_numerator_u"]), int(row["denominator_v_equals_M_power_N"])
            self.assertEqual(v, modulus ** row["power_exponent_N"])
            self.assertEqual(gcd(abs(u), v), 1)
            self.assertTrue(TWIN_ROOT_LOWER < Fraction(u, v) < TWIN_ROOT_UPPER)
            self.assertLess(u * u - 2 * v * v, 0)
            self.assertEqual(b1_coefficient_form(u, v) % modulus, 1 % modulus)
            self.assertTrue(row["witness_verified"])
        self.assertTrue(computation["aggregate"]["finite_coefficient_congruence_plus_fixed_window_route_refuted"])
        self.assertFalse(computation["aggregate"]["scale_dependent_convergent_exclusion_proved"])

    def test_dags_and_committed_state(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            ids = {node["id"] for node in dag["nodes"]}
            self.assertTrue(all(node["status"] in ALLOWED for node in dag["nodes"]))
            self.assertEqual(sum(node["status"] == "open" for node in dag["nodes"]), 1)
            self.assertEqual(len(ids), len(dag["nodes"]))
            self.assertTrue(dag["acyclic"])
        integrated = ROOT / "data/open-problem/ticket259-critical-alignment-compatibility-local.json"
        self.assertEqual(json.loads(integrated.read_text(encoding="utf-8")), build_audit())
        state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["ticket"], 259)
        self.assertEqual((state["resolved_count"], state["candidate_resolution_count"]), (0, 0))
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 259:
            self.assertEqual(state["parent_ticket"], 258)
            self.assertEqual(state["deep_focus_problem"], "goldbach")
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            self.assertIn(
                self.root[key]["theorem_name"],
                state["problems"][key]["established_results"],
            )


if __name__ == "__main__":
    unittest.main()
