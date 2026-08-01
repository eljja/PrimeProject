from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket169_kkt_childlift_autocorrelation_primepower import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_attempts,
    build_audit,
)


class Ticket169KKTChildLiftAutocorrelationPrimePowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket169-kkt-childlift-autocorrelation-primepower.json"
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

    def test_riemann_kkt_inertia_tracks_only_the_constraint_rank(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "exact_diagonal_proxy_rows"
        ]
        self.assertEqual(
            [row["ambient_dimension_N"] for row in rows], [4, 8, 16, 32, 64]
        )
        for row in rows:
            self.assertEqual(
                row["kkt_matrix_inertia"],
                {"positive": row["ambient_dimension_N"], "negative": 2, "zero": 0},
            )
            self.assertTrue(all(row["checks"].values()))
        self.assertTrue(
            self.audit["riemann"]["reproducible_computation"][
                "fixed_penalty_no_go_holds_on_all_overcurved_rows"
            ]
        )
        self.assertFalse(rows[-1]["fixed_penalty_is_positive_definite"])

    def test_collatz_exact_child_lift_is_unique(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "exact_child_lift_rows"
        ]
        self.assertEqual(
            [row["unique_selected_lift_k"] for row in rows],
            [0, 3, 1, 5, 29, 45, 77, 13],
        )
        for row in rows:
            self.assertEqual(row["child_correction"], 7)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_fixed_residue_width_never_determines_next_valuation(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "fixed_residue_memory_no_go_rows"
        ]
        self.assertEqual(
            [row["retained_residue_bits_q"] for row in rows], list(range(2, 17))
        )
        for row in rows:
            q = row["retained_residue_bits_q"]
            self.assertIn(q, row["next_valuations"])
            self.assertGreater(max(row["next_valuations"]), q)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_phase_sensitive_bounds_are_subunit(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_goldbach_tail_rows"
        ]
        self.assertEqual(
            [row["low_pass_bandwidth_K"] for row in rows],
            [16, 64, 256, 1024, 4096],
        )
        for row in rows:
            self.assertGreaterEqual(
                row["phase_sensitive_autocorrelation_l1_sqrt_bound"] + 1e-10,
                row["observed_uniform_tail"],
            )
            self.assertLess(
                row["phase_sensitive_autocorrelation_l1_sqrt_bound"], 1
            )
            self.assertTrue(row["passes_subunit_autocorrelation_gate"])
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_diagonal_energy_exact_no_go(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_diagonal_energy_no_go_rows"
        ]
        self.assertEqual([row["cyclic_length_L"] for row in rows], [4, 16, 64, 256])
        for row in rows:
            self.assertEqual(
                row["shared_diagonal_energy_C0"]["exact"],
                f'{row["cyclic_length_L"]}/1',
            )
            self.assertEqual(row["aligned_all_mode_uniform_norm"]["exact"], "1/1")
            self.assertTrue(all(row["checks"].values()))

    def test_twin_prime_power_removal_is_exact_up_to_float_roundoff(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_prime_power_removal_rows"
        ]
        self.assertEqual(
            [row["cutoff_x"] for row in rows],
            [128, 512, 2048, 8192, 32768, 65536],
        )
        self.assertEqual(rows[-1]["exact_twin_prime_pair_count"], 860)
        self.assertEqual(rows[-1]["exact_contaminated_pair_count"], 41)
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertLessEqual(
                row["higher_prime_power_contamination"],
                row["explicit_contamination_upper_bound"],
            )

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
            "riemann": "riemann/rh-ticket-169-kkt-inertia.json",
            "collatz": "collatz/co-ticket-169-child-lift.json",
            "goldbach": "goldbach/gb-ticket-169-autocorrelation.json",
            "twin-prime": "twin-prime/tp-ticket-169-prime-power-removal.json",
        }
        attempts = {row["problem_id"]: row for row in self.payload["attempts"]}
        for problem_id, relative in paths.items():
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(artifact["schema"], SCHEMA)
            self.assertEqual(artifact["status"], "open_not_proven")
            self.assertEqual(artifact["theorem_name"], attempts[problem_id]["new_result"])
            self.assertEqual(
                artifact["candidate_theorem"], attempts[problem_id]["candidate_theorem"]
            )


if __name__ == "__main__":
    unittest.main()
