from __future__ import annotations

import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket242_quantifier_order_parseval_diagonal_crt import (
    AUDIT_KEY,
    ORDER_SCAN_LIMIT,
    SCHEMA,
    build_audit,
    deterministic_is_prime,
    multiplicative_order,
)


ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = (
    ROOT
    / "data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json"
)


class Ticket242QuantifierOrderParsevalDiagonalCRTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads(INTEGRATED.read_text(encoding="utf-8"))
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        machine = self.root["machine_audit"]
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertEqual(self.audit["status"], "open_not_proven")
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["next_single_lemma_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["bounded_order_scan_limit"], ORDER_SCAN_LIMIT)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_moving_vector_no_go(self) -> None:
        data = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            data["transcript_sha256"],
            "f694cbcb62bd7a5fbe6cb3ade6516ceddb753012675f000aa9970cad15226e4f",
        )
        for row in data["moving_vector_rows"]:
            self.assertEqual(Fraction(row["smallest_eigenvalue"]["exact"]), -1)
            self.assertEqual(
                Fraction(row["fixed_early_coordinate_probe_value"]["exact"]), 1
            )
            self.assertEqual(row["negative_eigenvalue_count"], 1)
            self.assertTrue(row["certificate_verified"])
        self.assertTrue(data["aggregate"]["growing_family_uniform_positivity_refuted"])
        self.assertFalse(
            data["aggregate"]["signed_guinand_weil_uniform_tail_bound_proved"]
        )
        self.assertFalse(data["aggregate"]["riemann_hypothesis_resolved"])

    def test_collatz_order_core_reduction(self) -> None:
        data = self.root["collatz"]["reproducible_computation"]
        scan = data["bounded_identity_scan"]
        self.assertEqual(scan["prime_limit"], 200_000)
        self.assertEqual(scan["odd_primes_scanned"], 17_981)
        self.assertEqual(scan["order_core_lifting_identity_failures"], 0)
        self.assertEqual(scan["bad_line_candidate_count"], 0)
        self.assertEqual(scan["largest_order_seen"], 199_998)
        self.assertEqual(scan["order_witness_prime"], 199_999)
        self.assertEqual(
            data["transcript_sha256"],
            "ede3279e2ec7d5e375ec2e3ea65349459e401f9174c8eee13b7b697aacc70fec",
        )
        self.assertTrue(data["aggregate"]["order_core_lte_reduction_proved"])
        self.assertTrue(data["aggregate"]["multiplicative_orders_unbounded_proved"])
        self.assertFalse(
            data["aggregate"]["all_prime_order_core_square_divisor_transfer_proved"]
        )

    def test_collatz_selected_orders_recompute(self) -> None:
        rows = self.root["collatz"]["reproducible_computation"][
            "selected_order_core_rows"
        ]
        for row in rows:
            prime = row["prime_q"]
            ratio = 32 * pow(27, -1, prime) % prime
            self.assertEqual(
                multiplicative_order(ratio, prime), row["order_d_of_32_over_27"]
            )
            self.assertEqual(
                row["q_squared_divides_order_core"],
                row["q_squared_divides_full_fermat_power"],
            )

    def test_goldbach_parseval_scale_obstruction(self) -> None:
        data = self.root["goldbach"]["reproducible_computation"]
        rows = data["parseval_scale_rows"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(
            [row["parseval_global_L2_energy_pi_X"] for row in rows],
            [168, 430, 1229, 3245, 9592, 25997, 78498],
        )
        for row in rows:
            self.assertGreater(row["parseval_to_natural_scale_ratio"], 1)
            self.assertLessEqual(
                row["ordered_representation_count_R_X_N"],
                row["parseval_global_L2_energy_pi_X"],
            )
            self.assertTrue(row["certificate_verified"])
        self.assertEqual(
            data["transcript_sha256"],
            "fa85d668b1b025ab2a81b01ed957cc2ada5f4758a99e0a39874434521ac05280",
        )
        self.assertTrue(data["aggregate"]["l2_only_natural_scale_certificate_refuted"])
        self.assertFalse(data["aggregate"]["uniform_binary_goldbach_lower_bound_proved"])

    def test_twin_growing_modulus_diagonal_crt(self) -> None:
        data = self.root["twin_prime"]["reproducible_computation"]
        rows = data["growing_modulus_diagonal_crt_rows"]
        self.assertEqual(len(rows), 6)
        self.assertEqual(
            [row["growing_period_M_j"] for row in rows],
            [30, 210, 2310, 30030, 510510, 9699690],
        )
        previous = 1
        for row in rows:
            prime = row["strictly_increasing_prime_witness_p_j"]
            self.assertGreater(prime, previous)
            self.assertTrue(deterministic_is_prime(prime))
            self.assertEqual(
                prime % row["growing_period_M_j"],
                row["admissible_residue_a_j"],
            )
            self.assertEqual(
                row["forced_composite_successor_p_j_plus_2"]
                % row["outside_prime_ell_j"],
                0,
            )
            self.assertTrue(row["certificate_verified"])
            previous = prime
        self.assertEqual(
            data["transcript_sha256"],
            "5cc91d6440bc282199fd9b5f348d758fa23b256a593c890d2199e49f75c1ed79",
        )
        self.assertTrue(
            data["aggregate"]["arbitrary_growing_period_diagonal_mimicry_proved"]
        )
        self.assertFalse(data["aggregate"]["scale_local_type_ii_cancellation_proved"])

    def test_proof_dag_and_successor_contract(self) -> None:
        expected_ids = ["riemann", "collatz", "goldbach", "twin-prime"]
        self.assertEqual(
            [attempt["problem_id"] for attempt in self.audit["attempts"]],
            expected_ids,
        )
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.root[key]
            self.assertEqual(len(section["proof_dag"]["nodes"]), 4)
            statuses = {node["status"] for node in section["proof_dag"]["nodes"]}
            self.assertEqual(
                statuses,
                {
                    "closed_input",
                    "refuted_or_limited",
                    "proved_exact",
                    "highest_risk_open",
                },
            )
            self.assertTrue(section["route_decision"]["next_single_lemma"])

    def test_integrated_output_reproduces(self) -> None:
        rebuilt = build_audit()
        self.assertEqual(rebuilt, self.audit)
        self.assertEqual(
            rebuilt[AUDIT_KEY]["machine_audit"]["conjecture_resolution_count"], 0
        )


if __name__ == "__main__":
    unittest.main()
