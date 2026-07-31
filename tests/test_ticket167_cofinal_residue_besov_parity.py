from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket167_cofinal_residue_besov_parity import (  # noqa: E402
    SCHEMA,
    STATUS,
    bad_realizer_count,
    build_attempts,
    build_audit,
    least_nonterminal_realizer,
)


class Ticket167CofinalResidueBesovParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket167-cofinal-residue-besov-parity.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_has_no_failures_or_resolutions(self) -> None:
        self.assertEqual(
            self.audit["machine_audit"],
            {
                "exact_theorem_count": 4,
                "rejected_target_count": 4,
                "proof_dag_count": 4,
                "conjecture_resolution_count": 0,
                "total_failure_count": 0,
            },
        )

    def test_global_payload_contract(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(self.payload["status"], STATUS)
        self.assertIn("resolves none", self.payload["claim_boundary"])

    def test_riemann_cofinal_proxy_keeps_exact_positive_pivots(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "cofinal_exact_ldl_proxy_rows"
        ]
        self.assertEqual(
            [row["cofinal_dimension_Nj"] for row in rows],
            [2, 4, 8, 16, 32, 64, 128, 256],
        )
        pivots = [Fraction(row["smallest_exact_ldl_pivot"]["exact"]) for row in rows]
        self.assertTrue(all(left > right > 0 for left, right in zip(pivots, pivots[1:])))
        self.assertEqual(pivots[-1], Fraction(1, 65_536))
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_riemann_non_dense_nested_family_misses_negative_direction(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "non_dense_nested_subspace_no_go_rows"
        ]
        for row in rows:
            self.assertEqual(row["restricted_minimum"]["exact"], "1/1")
            self.assertEqual(row["omitted_e1_value"]["exact"], "-1/1")
            self.assertEqual(row["closure_codimension"], 1)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_closed_form_counts_synthetic_bad_realizers(self) -> None:
        for quotient in [0, 1, 3, 7, 15, 31]:
            correction = 9 + 8 * quotient
            self.assertEqual(least_nonterminal_realizer(1, 2, correction), 9)
            self.assertEqual(bad_realizer_count(1, 2, correction), quotient + 1)

    def test_collatz_finite_first_crossing_count_remains_zero(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(computation["maximum_certified_length"], 18)
        self.assertEqual(computation["total_potential_non_descent_words_counted"], 1_120_444)
        self.assertEqual(computation["total_bad_realizer_count"], 0)
        self.assertGreater(computation["global_minimum_exact_residue_slack"], 0)
        self.assertTrue(
            all(
                row["exact_bad_realizer_count"] == 0
                and all(row["checks"].values())
                for row in computation["finite_first_crossing_exact_count_rows"]
            )
        )

    def test_goldbach_shell_bound_is_valid_but_fails_gate(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_besov_shell_certificate_rows"
        ]
        self.assertEqual(
            [row["low_pass_bandwidth_K"] for row in rows],
            [16, 64, 256, 1024, 4096],
        )
        for row in rows:
            self.assertGreaterEqual(
                row["dyadic_shell_l1_uniform_bound"],
                row["observed_uniform_high_frequency_tail"],
            )
            self.assertGreater(row["combined_pointwise_certificate"], 1)
            self.assertFalse(row["passes_subunit_gate"])
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_aligned_shells_refute_scale_l2_promotion(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "aligned_shell_l2_no_go_rows"
        ]
        self.assertEqual([row["disjoint_shell_count_J"] for row in rows], [2, 4, 8, 16, 32, 64])
        for row in rows:
            count = row["disjoint_shell_count_J"]
            self.assertEqual(row["aligned_sum_at_origin"]["exact"], "1/1")
            self.assertEqual(Fraction(row["scale_l2_budget_squared"]["exact"]), Fraction(1, count))
            self.assertTrue(all(row["checks"].values()))

    def test_twin_finest_parity_energy_has_exact_linear_formula(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finest_parity_scale_rows"
        ]
        self.assertEqual([row["matrix_side_N"] for row in rows], [8, 16, 32, 64, 128, 256])
        for row in rows:
            side = row["matrix_side_N"]
            energy = Fraction(row["finest_2x2_product_haar_energy"]["exact"])
            self.assertEqual(energy, Fraction(side - 2, 2))
            self.assertEqual(row["nonzero_finest_2x2_coefficients"], side // 2 - 1)
            self.assertTrue(all(row["checks"].values()))

    def test_attempts_and_proof_dags_remain_open(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        for attempt in attempts:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertEqual(
                [node["status"] for node in attempt["proof_dag"]["nodes"]],
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_per_problem_artifacts_match_global_sections(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-167-cofinal-core.json",
            "collatz": "collatz/co-ticket-167-realizer-count.json",
            "goldbach": "goldbach/gb-ticket-167-besov-tail.json",
            "twin-prime": "twin-prime/tp-ticket-167-parity-scale.json",
        }
        attempts = {row["problem_id"]: row for row in self.payload["attempts"]}
        for problem_id, relative in paths.items():
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(encoding="utf-8")
            )
            self.assertEqual(artifact["schema"], SCHEMA)
            self.assertEqual(artifact["status"], "open_not_proven")
            self.assertEqual(artifact["theorem_name"], attempts[problem_id]["new_result"])
            self.assertEqual(
                artifact["candidate_theorem"], attempts[problem_id]["candidate_theorem"]
            )


if __name__ == "__main__":
    unittest.main()
