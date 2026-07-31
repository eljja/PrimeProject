from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket164_core_eigen_first_crossing_pointwise_product import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_attempts,
    build_audit,
    collatz_first_crossing_audit,
    collatz_realizer_from_correction,
    collatz_replay,
    haar_energy_by_scale,
    haar_vector,
)


class Ticket164CoreEigenFirstCrossingPointwiseProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket164-core-eigen-first-crossing-pointwise-product.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_has_no_failures_or_resolutions(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_global_payload_contract(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(self.payload["status"], STATUS)
        self.assertIn("resolves none", self.payload["claim_boundary"])

    def test_riemann_constraint_compression_counterexample_is_exact(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        core = computation["exact_three_dimensional_core"]
        self.assertEqual(core["compressed_form"], [[2, 3], [3, 2]])
        self.assertEqual(core["compressed_determinant"], -5)
        self.assertEqual(core["negative_witness_value"], -2)
        self.assertTrue(all(computation["exact_checks"].values()))

    def test_riemann_scalar_diagnostic_no_go_scales(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "scalable_scalar_cancellation_no_go_rows"
        ]
        self.assertEqual([row["dimension"] for row in rows], [5, 9, 17, 33])
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(all(row["constraint_core_negative_witness_value"] == -2 for row in rows))

    def test_collatz_affine_realizer_replays_exact_word(self) -> None:
        correction = 5
        start, endpoint, margin = collatz_realizer_from_correction(2, 4, correction)
        self.assertEqual((start, endpoint, margin), (19, 11, 8))
        self.assertEqual(collatz_replay(start, 2), ((1, 3), endpoint))

    def test_collatz_first_crossing_certificate_is_complete_through_17(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        rows = computation["complete_first_crossing_rows"]
        self.assertEqual(computation["maximum_certified_length"], 17)
        self.assertEqual(rows[-1]["noncontracting_prefix_count"], 312_455)
        self.assertEqual(rows[-1]["next_noncontracting_prefix_count"], 663_535)
        self.assertEqual(
            computation["total_potential_non_descent_words_replayed"],
            464_921,
        )
        self.assertEqual(computation["total_replay_failure_count"], 0)
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_collatz_final_valuation_margin_is_not_monotone(self) -> None:
        no_go = self.audit["collatz"]["reproducible_computation"][
            "final_valuation_monotonicity_no_go"
        ]
        rows = no_go["rows"]
        self.assertEqual(rows[0]["valuation_word"], [1, 3])
        self.assertEqual(rows[0]["strict_descent_margin"], 8)
        self.assertEqual(rows[1]["valuation_word"], [1, 4])
        self.assertEqual(rows[1]["strict_descent_margin"], 2)
        self.assertTrue(all(no_go["checks"].values()))

    def test_collatz_small_depth_helper_matches_full_audit(self) -> None:
        small = collatz_first_crossing_audit(max_length=5)
        self.assertEqual(small["maximum_certified_length"], 5)
        self.assertEqual(small["failure_count"], 0)
        self.assertEqual(small["complete_first_crossing_rows"][-1]["word_length_m"], 5)

    def test_goldbach_pointwise_gate_matches_integer_scan(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_prime_pointwise_rows"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[-1]["dyadic_upper_inclusive"], 65_536)
        self.assertTrue(all(row["maximum_normalized_deficit"] < 1 for row in rows))
        self.assertTrue(all(row["observed_zero_count"] == 0 for row in rows))
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_goldbach_l2_gate_is_not_necessary(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["positive_count_l2_no_go_rows"]
        self.assertTrue(all(row["zero_count"] == 0 for row in rows))
        self.assertTrue(all(row["pointwise_gate_passes"] for row in rows))
        self.assertEqual(rows[-1]["l2_budget"]["exact"], "256/1")
        self.assertTrue(all(computation["no_go_checks"].values()))

    def test_haar_scale_energy_is_exact(self) -> None:
        vector = haar_vector(16, 8, 0)
        energy = haar_energy_by_scale(vector)
        self.assertEqual(energy[8], 8)
        self.assertEqual(sum(energy.values()), 8)

    def test_twin_product_haar_detects_anisotropic_energy(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "anisotropic_product_rows"
        ]
        self.assertEqual([row["matrix_side"] for row in rows], [8, 16, 32, 64, 128])
        self.assertTrue(all(row["same_scale_tensor_energy"]["exact"] == "0/1" for row in rows))
        self.assertTrue(
            all(
                row["full_product_haar_energy"]["exact"]
                == row["frobenius_energy"]["exact"]
                for row in rows
            )
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_attempts_and_proof_dags_remain_open(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual({attempt["problem_id"] for attempt in attempts}, {
            "riemann",
            "collatz",
            "goldbach",
            "twin-prime",
        })
        for attempt in attempts:
            self.assertEqual(attempt["status"], "open_not_proven")
            nodes = attempt["proof_dag"]["nodes"]
            self.assertEqual(
                [node["status"] for node in nodes],
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_per_problem_artifacts_match_global_sections(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-164-constraint-core-eigenvalue.json",
            "collatz": "collatz/co-ticket-164-first-crossing-residue.json",
            "goldbach": "goldbach/gb-ticket-164-pointwise-deficit.json",
            "twin-prime": "twin-prime/tp-ticket-164-product-haar.json",
        }
        attempts = {row["problem_id"]: row for row in self.payload["attempts"]}
        for problem_id, relative in paths.items():
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(encoding="utf-8")
            )
            self.assertEqual(artifact["schema"], SCHEMA)
            self.assertEqual(artifact["status"], "open_not_proven")
            self.assertEqual(artifact["theorem_name"], attempts[problem_id]["new_result"])
            self.assertEqual(artifact["candidate_theorem"], attempts[problem_id]["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
