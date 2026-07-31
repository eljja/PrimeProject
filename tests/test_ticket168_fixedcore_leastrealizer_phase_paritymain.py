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

from ticket168_fixedcore_leastrealizer_phase_paritymain import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_attempts,
    build_audit,
)


class Ticket168FixedCoreLeastRealizerPhaseParityMainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket168-fixedcore-leastrealizer-phase-paritymain.json"
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

    def test_riemann_fixed_projection_is_nested_and_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "fixed_moment_projection_rows"
        ]
        self.assertEqual(
            [row["ambient_dimension_N"] for row in rows],
            [4, 8, 16, 32, 64],
        )
        for row in rows:
            self.assertEqual(row["constraint_rank"], 2)
            self.assertEqual(
                row["projected_core_dimension"], row["ambient_dimension_N"] - 2
            )
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_cutoff_varying_constraints_miss_fixed_negative_witness(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "cutoff_varying_constraint_no_go_rows"
        ]
        self.assertEqual(
            [row["constraint"] for row in rows],
            ["x_1=0", "x_2=0", "x_1=0", "x_2=0", "x_1=0", "x_2=0"],
        )
        for row in rows:
            self.assertEqual(row["restricted_minimum"]["exact"], "1/1")
            self.assertEqual(row["fixed_global_witness_value"]["exact"], "-2/1")
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_least_realizer_gap_is_strictly_increasing(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "least_realizer_monotonicity_rows"
        ]
        self.assertEqual(
            [row["correction_C"] for row in rows], [1, 9, 17, 25, 33]
        )
        self.assertEqual(
            [row["least_descent_gap_n0_minus_u0"] for row in rows],
            [2, 0, -2, -4, -6],
        )
        for row in rows:
            gaps = [item["descent_gap_nk_minus_uk"] for item in row["lift_rows"]]
            self.assertEqual(gaps, list(range(gaps[0], gaps[0] + 10, 2)))
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_finite_extension_remains_bounded(self) -> None:
        finite = self.audit["collatz"]["reproducible_computation"][
            "finite_first_crossing_extension"
        ]
        self.assertEqual(finite["maximum_certified_length"], 20)
        self.assertEqual(finite["total_potential_non_descent_words_counted"], 7_553_085)
        self.assertEqual(finite["total_bad_realizer_count"], 0)
        self.assertEqual(finite["global_minimum_exact_residue_slack"], 192)

    def test_goldbach_phase_blind_minimax_fails_finite_gate(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_phase_blind_gap_rows"
        ]
        self.assertEqual(
            [row["low_pass_bandwidth_K"] for row in rows],
            [16, 64, 256, 1024, 4096],
        )
        for row in rows:
            self.assertLess(row["observed_uniform_tail"], 1)
            self.assertGreater(row["optimal_phase_blind_spectral_l1_bound"], 1)
            self.assertFalse(row["passes_subunit_phase_blind_gate"])
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_exact_magnitude_family_attains_spectral_l1(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_aligned_magnitude_no_go_rows"
        ]
        self.assertEqual(
            [row["paired_or_real_mode_count"] for row in rows],
            [2, 4, 8, 16, 32, 64],
        )
        for row in rows:
            self.assertEqual(row["spectral_l1_minimax_value"]["exact"], "1/1")
            self.assertTrue(all(row["checks"].values()))

    def test_twin_finest_parity_pairing_is_half_the_target(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_prime_indicator_rows"
        ]
        self.assertEqual(
            [row["matrix_side_N"] for row in rows],
            [128, 512, 2048, 8192, 32768, 65536],
        )
        self.assertEqual(rows[-1]["exact_prime_indicator_twin_pair_count"], 860)
        for row in rows:
            count = Fraction(row["exact_prime_indicator_twin_pair_count"])
            fine = Fraction(row["finest_parity_pairing"]["exact"])
            coarse = Fraction(row["coarse_completion_pairing"]["exact"])
            self.assertEqual(fine, count / 2)
            self.assertEqual(coarse, count / 2)
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
            "riemann": "riemann/rh-ticket-168-fixed-neutral-core.json",
            "collatz": "collatz/co-ticket-168-least-realizer.json",
            "goldbach": "goldbach/gb-ticket-168-phase-minimax.json",
            "twin-prime": "twin-prime/tp-ticket-168-parity-main-term.json",
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
