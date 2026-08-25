from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.ticket241_finite_information_canonical_errors import (
    AUDIT_KEY,
    PRIME_LIMIT,
    SCHEMA,
    crt_pair,
    deterministic_is_prime,
    riemann_prime_cosine_rank_audit,
)


ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = (
    ROOT / "data/open-problem/ticket241-finite-information-canonical-errors.json"
)


class Ticket241FiniteInformationCanonicalErrorsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads(INTEGRATED.read_text(encoding="utf-8"))
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary(self) -> None:
        machine = self.root["machine_audit"]
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["route_correction_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["bounded_prime_scan_limit"], PRIME_LIMIT)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_rank_no_go(self) -> None:
        data = self.root["riemann"]["reproducible_computation"]
        self.assertTrue(data["aggregate"]["finite_support_rank_cap_proved"])
        self.assertFalse(data["aggregate"]["signed_guinand_weil_lower_bound_proved"])
        for row in data["prime_cosine_rank_rows"]:
            self.assertLessEqual(row["numerical_rank"], row["feature_rank_cap_2m"])
            self.assertGreaterEqual(
                row["numerical_nullity"],
                row["forced_nullity_on_common_mode_complement"],
            )
            self.assertAlmostEqual(
                row["smallest_regularized_eigenvalue"],
                row["diagonal_regularizer_epsilon"],
                places=10,
            )

    def test_riemann_calculation_reproduces_without_prime_scan(self) -> None:
        data = riemann_prime_cosine_rank_audit()
        self.assertEqual(data["failure_count"], 0)
        self.assertEqual(len(data["prime_cosine_rank_rows"]), 4)

    def test_collatz_local_countermodel_and_bounded_scan(self) -> None:
        data = self.root["collatz"]["reproducible_computation"]
        self.assertTrue(all(row["certificate_verified"] for row in data["principal_unit_countermodel_rows"]))
        scan = data["bounded_fixed_base_scan"]
        self.assertEqual(scan["prime_limit"], 100_000_000)
        self.assertEqual(scan["odd_primes_scanned"], 5_761_453)
        self.assertEqual(scan["odd_primes_through_twenty_million"], 1_270_605)
        self.assertEqual(scan["x_depth_at_least_two_count"], 0)
        self.assertEqual(scan["positive_defect_candidate_count"], 0)
        self.assertFalse(data["aggregate"]["all_prime_fixed_base_line_avoidance_proved"])

    def test_goldbach_contract_distinguishes_signed_and_absolute(self) -> None:
        data = self.root["goldbach"]["reproducible_computation"]
        rows = data["prime_window_error_contract_rows"]
        self.assertEqual(len(rows), 15)
        self.assertEqual(
            data["aggregate"]["represented_rows_failing_absolute_certificate"],
            14,
        )
        for row in rows:
            self.assertEqual(
                row["signed_identity_certificate_M_plus_E_at_least_one"],
                row["representation_exists"],
            )
            self.assertTrue(row["split_preserves_total_error"])
            self.assertTrue(row["split_strictly_increases_absolute_budget"])

    def test_twin_periodic_fingerprint_mimicry(self) -> None:
        data = self.root["twin_prime"]["reproducible_computation"]
        rows = data["periodic_fingerprint_crt_rows"]
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(
            data["aggregate"]["arbitrary_finite_periodic_fingerprint_mimicry_proved"]
        )
        for row in rows:
            self.assertTrue(deterministic_is_prime(row["prime_witness_p"]))
            self.assertEqual(
                row["forced_composite_successor_p_plus_2"]
                % row["outside_prime_ell"],
                0,
            )
            self.assertEqual(
                row["periodic_feature_hash_before"],
                row["periodic_feature_hash_at_witness"],
            )

    def test_crt_helper(self) -> None:
        residue, modulus = crt_pair(11, 30, 5, 7)
        self.assertEqual(modulus, 210)
        self.assertEqual(residue % 30, 11)
        self.assertEqual(residue % 7, 5)

    def test_written_track_contracts(self) -> None:
        self.assertEqual(
            [attempt["problem_id"] for attempt in self.audit["attempts"]],
            ["riemann", "collatz", "goldbach", "twin-prime"],
        )
        self.assertTrue(
            all(attempt["status"] == "open_not_proven" for attempt in self.audit["attempts"])
        )
        self.assertTrue(
            all(len(self.root[key]["proof_dag"]["nodes"]) == 4 for key in ("riemann", "collatz", "goldbach", "twin_prime"))
        )


if __name__ == "__main__":
    unittest.main()
