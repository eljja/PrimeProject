from __future__ import annotations

import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket243_bandlimit_principal_unit_half_arc_dyadic_mimicry import (
    AUDIT_KEY,
    LOCAL_MODEL_SCAN_LIMIT,
    SCHEMA,
    build_audit,
    deterministic_is_prime,
    multiplicative_order,
)


ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = (
    ROOT
    / "data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json"
)
STATE = ROOT / "data/open-problem/four-problem-research-state.json"


class Ticket243BandlimitPrincipalUnitHalfArcDyadicMimicryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads(INTEGRATED.read_text(encoding="utf-8"))
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        machine = self.root["machine_audit"]
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["partial_theorem_count"], 1)
        self.assertEqual(machine["exact_no_go_count"], 3)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["deep_focus_problem"], "collatz")
        self.assertEqual(machine["stagnated_problem_count"], 0)
        self.assertEqual(machine["local_model_scan_limit"], LOCAL_MODEL_SCAN_LIMIT)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_exact_bandlimited_gram(self) -> None:
        data = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            data["transcript_sha256"],
            "6b52e81598d394e05fffe373733e2a7638a9de662610abd8f1b63c59e46e90cf",
        )
        for row in data["exact_cosine_gram_rows"]:
            self.assertEqual(Fraction(row["gram_diagonal"]["exact"]), 1)
            self.assertEqual(
                Fraction(row["maximum_off_diagonal_absolute_value"]["exact"]), 0
            )
            self.assertEqual(
                Fraction(row["minimum_pair_distance_squared"]["exact"]), 2
            )
            self.assertTrue(row["real_even"])
            self.assertTrue(row["certificate_verified"])
        self.assertTrue(data["aggregate"]["relative_compactness_refuted"])
        self.assertFalse(
            data["aggregate"]["uniform_signed_guinand_weil_tail_proved"]
        )

    def test_collatz_unbounded_order_countermodels(self) -> None:
        data = self.root["collatz"]["reproducible_computation"]
        scan = data["bounded_universal_model_replay"]
        self.assertEqual(scan["prime_limit"], 50_000)
        self.assertEqual(scan["primes_scanned"], 5_130)
        self.assertEqual(scan["failure_count"], 0)
        self.assertEqual(scan["largest_countermodel_order"], 24_999)
        self.assertEqual(scan["largest_order_witness_prime"], 49_999)
        self.assertEqual(
            data["transcript_sha256"],
            "fa66801a2a9d21ff3f873a7ac22501d9e8193aea8a9404b42e2e318fdbdff59f",
        )
        self.assertTrue(
            data["aggregate"]["unbounded_order_local_countermodel_family_proved"]
        )
        self.assertFalse(
            data["aggregate"]["fixed_base_32_over_27_exception_excluded"]
        )

    def test_collatz_selected_rows_independently_recompute(self) -> None:
        rows = self.root["collatz"]["reproducible_computation"][
            "selected_principal_unit_rows"
        ]
        for row in rows:
            prime = row["prime_q"]
            modulus = prime * prime
            generator = row["primitive_root_t"]
            teichmuller = row["teichmuller_lift_T_mod_q_squared"]
            a_unit = row["A_mod_q_squared"]
            b_unit = row["B_mod_q_squared"]
            ratio_u = a_unit * pow(b_unit, -1, modulus) % modulus
            ratio_v = (
                pow(a_unit, 5, modulus)
                * pow(pow(b_unit, 3, modulus), -1, modulus)
            ) % modulus
            order = row["order_d_of_V_mod_q"]
            self.assertEqual(multiplicative_order(generator, prime), prime - 1)
            self.assertEqual(pow(teichmuller, prime - 1, modulus), 1)
            self.assertEqual(ratio_u, row["U_equals_A_over_B_mod_q_squared"])
            self.assertEqual(
                ratio_v,
                row["V_equals_A_power_5_over_B_power_3_mod_q_squared"],
            )
            self.assertEqual(order, (prime - 1) // 2)
            self.assertEqual(multiplicative_order(ratio_v % prime, prime), order)
            self.assertEqual(pow(ratio_v, order, modulus), 1)
            self.assertEqual(ratio_u % prime, 1)
            self.assertNotEqual(ratio_u, 1)
            self.assertEqual((ratio_u - 1) % prime, 0)
            self.assertNotEqual((ratio_u - 1) % modulus, 0)

    def test_goldbach_exact_half_arc_energy_floor(self) -> None:
        data = self.root["goldbach"]["reproducible_computation"]
        rows = data["exact_half_frequency_rows"]
        self.assertEqual(
            [row["prime_count_pi_X"] for row in rows],
            [168, 430, 1229, 3245, 9592, 25997, 78498],
        )
        for row in rows:
            cutoff = row["prime_cutoff_X"]
            count = row["prime_count_pi_X"]
            half_width = Fraction(row["half_frequency_arc_half_width"]["exact"])
            pointwise = Fraction(row["pointwise_absolute_S_floor"]["exact"])
            energy = Fraction(row["exact_integrated_energy_floor"]["exact"])
            self.assertEqual(half_width, Fraction(1, 6 * cutoff))
            self.assertEqual(pointwise, Fraction(count - 3, 2))
            self.assertEqual(energy, Fraction((count - 3) ** 2, 12 * cutoff))
            self.assertEqual(energy, 2 * half_width * pointwise * pointwise)
            self.assertTrue(row["certificate_verified"])
        self.assertEqual(
            data["transcript_sha256"],
            "db3723c1a9cdabd673471f1564af46489235e620f7384d6dcae6f3d3f1446392",
        )
        self.assertFalse(data["aggregate"]["strong_goldbach_resolved"])

    def test_twin_fixed_period_dyadic_witnesses(self) -> None:
        data = self.root["twin_prime"]["reproducible_computation"]
        rows = data["finite_dyadic_witness_rows"]
        self.assertEqual(len(rows), 16)
        for row in rows:
            prime = row["prime_mimic_p"]
            successor = row["forced_composite_successor_p_plus_2"]
            start = row["dyadic_block_start_X"]
            self.assertGreaterEqual(prime, start)
            self.assertLessEqual(prime, 2 * start)
            self.assertTrue(deterministic_is_prime(prime))
            self.assertEqual(prime % row["fixed_period_M"], row["admissible_residue_a"])
            self.assertEqual(successor, prime + 2)
            self.assertEqual(successor % row["outside_prime_ell"], 0)
            self.assertGreater(successor, row["outside_prime_ell"])
            self.assertEqual(
                successor,
                row["outside_prime_ell"] * row["successor_cofactor"],
            )
            self.assertTrue(row["certificate_verified"])
        self.assertEqual(
            data["transcript_sha256"],
            "3858c95f26b5cf54bc5873b288814a47c38add509e0adf65068b79cf85f8fadd",
        )
        self.assertFalse(data["aggregate"]["growing_modulus_uniformity_proved"])

    def test_proof_dag_state_and_successor_contract(self) -> None:
        allowed = {
            "proved",
            "disproved",
            "computed_finite",
            "external_theorem",
            "assumption",
            "heuristic",
            "open",
        }
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.root[key]
            nodes = section["proof_dag"]["nodes"]
            edges = section["proof_dag"]["edges"]
            ids = {node["id"] for node in nodes}
            self.assertTrue(all(node["status"] in allowed for node in nodes))
            self.assertEqual(sum(node["status"] == "open" for node in nodes), 1)
            self.assertTrue(all(left in ids and right in ids for left, right in edges))
            self.assertTrue(section["route_decision"]["next_single_lemma"])
            self.assertEqual(section["stagnation_count"], 0)
            self.assertEqual(section["problem_status"], "open_not_proven")

        state = json.loads(STATE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(state["ticket"], 243)
        self.assertEqual(state["resolved_count"], 0)
        self.assertFalse(state["program_complete"])
        self.assertIn(
            "UnboundedOrderPrincipalUnitTransferCountermodels",
            state["problems"]["collatz"]["established_results"],
        )
        self.assertEqual(set(state["problems"]), set(("riemann", "collatz", "goldbach", "twin_prime")))

    def test_integrated_output_reproduces(self) -> None:
        rebuilt = build_audit()
        self.assertEqual(rebuilt, self.audit)
        self.assertEqual(
            rebuilt[AUDIT_KEY]["machine_audit"]["conjecture_resolution_count"], 0
        )


if __name__ == "__main__":
    unittest.main()
