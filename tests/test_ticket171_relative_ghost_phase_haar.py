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

from ticket171_relative_ghost_phase_haar import (  # noqa: E402
    SCHEMA,
    build_attempts,
    build_audit,
    matrix_product,
    orthonormal_haar4,
    transpose,
)


class Ticket171RelativeGhostPhaseHaarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket171-relative-ghost-phase-haar.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_audit_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_relative_certificate_beats_global_gap_requirement(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        rows = computation["exact_anisotropic_proxy_rows"]
        self.assertEqual([row["scale_n"] for row in rows], [2, 4, 8, 16, 32, 64])
        self.assertTrue(computation["relative_certificate_holds_on_all_rows"])
        self.assertEqual(
            rows[-1]["sign_normalized_relative_operator_error"]["exact"], "1/2"
        )
        self.assertGreater(
            rows[-1]["absolute_error_to_gap_ratio"]["decimal"],
            rows[0]["absolute_error_to_gap_ratio"]["decimal"],
        )
        for row in rows:
            self.assertEqual(row["approximate_inertia"], row["perturbed_inertia"])
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_all_one_ray_is_infinite_but_not_natural(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        rows = computation["exact_all_one_ghost_rows"]
        self.assertTrue(computation["infinite_non_descending_residual_ray_exists"])
        self.assertTrue(computation["no_positive_natural_start_realizes_the_entire_ray"])
        self.assertEqual(computation["two_adic_limit"], "-1 in Z_2")
        for row in rows:
            m = row["all_one_prefix_length_m"]
            self.assertEqual(row["least_positive_realizer_n_m"], 2 ** (m + 1) - 1)
            self.assertGreater(
                row["odd_endpoint_after_m_steps_u_m"],
                row["least_positive_realizer_n_m"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_positive_signals_have_same_shell_energy_but_different_max(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["exact_positive_phase_ambiguity_rows"]
        self.assertTrue(
            computation["shell_energy_only_pointwise_determination_no_go_holds"]
        )
        self.assertEqual(rows[2]["epsilon"]["exact"], "1/4")
        self.assertEqual(rows[2]["g_plus_uniform_norm_squared"]["exact"], "3/2")
        self.assertEqual(rows[2]["g_minus_uniform_norm_squared"]["exact"], "5/4")
        for row in rows:
            plus = [Fraction(item["exact"]) for item in row["g_plus_normalized_dft"]]
            minus = [Fraction(item["exact"]) for item in row["g_minus_normalized_dft"]]
            self.assertEqual([abs(value) for value in plus], [abs(value) for value in minus])
            self.assertTrue(all(row["checks"].values()))

    def test_haar_basis_is_orthonormal(self) -> None:
        haar = orthonormal_haar4()
        identity = matrix_product(haar, transpose(haar))
        for row in range(4):
            for column in range(4):
                self.assertAlmostEqual(identity[row][column], 1.0 if row == column else 0.0)

    def test_twin_haar_transform_preserves_norms_and_exposes_fine_energy(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        rows = computation["finite_t161_haar_resolution_rows"]
        self.assertEqual([row["X"] for row in rows], [10000, 100000, 1000000, 10000000])
        for row in rows:
            self.assertAlmostEqual(
                row["original_top_singular_value"],
                row["haar_top_singular_value"],
                places=6,
            )
            self.assertGreaterEqual(row["fine_fine_energy_fraction"], 0.0)
            self.assertLessEqual(row["fine_fine_energy_fraction"], 1.0 + 1e-12)
            self.assertTrue(all(row["checks"].values()))

    def test_every_fixed_haar_depth_has_an_invisible_next_scale(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "exact_finite_depth_invisibility_rows"
        ]
        self.assertEqual(
            [row["controlled_maximum_dyadic_level_J"] for row in rows],
            [1, 2, 3, 4, 5],
        )
        for row in rows:
            self.assertEqual(row["all_controlled_coarse_aggregates"], 0)
            self.assertGreater(row["next_scale_haar_coefficient"], 0)
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

    def test_per_problem_artifacts_match_global_attempts(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-171-relative-kkt.json",
            "collatz": "collatz/co-ticket-171-ghost-ray.json",
            "goldbach": "goldbach/gb-ticket-171-shell-phase.json",
            "twin-prime": "twin-prime/tp-ticket-171-haar-resolution.json",
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
