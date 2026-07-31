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

from ticket166_tail_adaptive_bandlimited_diagonal import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_attempts,
    build_audit,
    first_start_adaptive_excess,
)


class Ticket166TailAdaptiveBandlimitedDiagonalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket166-tail-adaptive-bandlimited-diagonal.json"
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

    def test_riemann_cubic_schedule_has_vanishing_leading_scale(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "cubic_diagonal_tail_scale_rows"
        ]
        self.assertEqual(
            [row["galerkin_dimension_N"] for row in rows],
            [4, 8, 16, 32, 64, 128, 256],
        )
        scales = [
            row["published_leading_order_tail_scale_diagnostic"] for row in rows
        ]
        self.assertTrue(all(left > right for left, right in zip(scales, scales[1:])))
        self.assertLess(scales[-1], 1e-4)
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_riemann_ambiguous_tail_band_has_opposite_completions(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "ambiguous_tail_band_no_go_rows"
        ]
        for row in rows:
            truncated = Fraction(row["truncated_scalar"]["exact"])
            negative = Fraction(row["zero_tail_full_scalar"]["exact"])
            positive = Fraction(row["maximal_tail_full_scalar"]["exact"])
            self.assertEqual(truncated, negative)
            self.assertLess(negative, 0)
            self.assertGreater(positive, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_start_adaptive_threshold_is_minimal(self) -> None:
        for length, start in [(63, 3), (63, 63), (1024, 3), (1024, 1025)]:
            threshold = first_start_adaptive_excess(length, start)
            self.assertGreaterEqual(3 * start * ((1 << threshold) - 1), length)
            self.assertLess(3 * start * ((1 << (threshold - 1)) - 1), length)

    def test_collatz_large_start_leaves_only_zero_excess(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "length_only_window_no_go_rows"
        ]
        self.assertEqual([row["word_length_m"] for row in rows], [63, 255, 1024, 4096])
        self.assertTrue(all(row["start_adaptive_residual_count"] == 1 for row in rows))
        self.assertTrue(
            all(
                row["length_only_n3_residual_count"]
                > row["start_adaptive_residual_count"]
                for row in rows
            )
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_goldbach_bandlimited_certificate_dominates_finite_maximum(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_low_pass_diagnostic_rows"]
        self.assertEqual(
            [row["low_pass_bandwidth_K"] for row in rows],
            [16, 64, 256, 1024, 4096],
        )
        self.assertTrue(
            all(row["bernstein_plus_error_upper_certificate"] < 1 for row in rows)
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_goldbach_full_bandwidth_spike_evades_half_grid(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "full_bandwidth_spike_no_go_rows"
        ]
        self.assertEqual([row["cyclic_grid_size"] for row in rows], [16, 32, 64, 128, 256])
        self.assertTrue(
            all(
                row["nonzero_dft_coefficient_count"] == row["cyclic_grid_size"]
                and all(row["checks"].values())
                for row in rows
            )
        )

    def test_twin_centered_shifted_selector_saturates_haar_duality(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "shifted_diagonal_haar_rows"
        ]
        self.assertEqual([row["matrix_side_N"] for row in rows], [8, 16, 32, 64, 128])
        for row in rows:
            energy = row["double_centered_selector_frobenius_energy"]["exact"]
            self.assertEqual(row["full_product_haar_energy"]["exact"], energy)
            self.assertEqual(row["shifted_diagonal_signed_pairing"]["exact"], energy)
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
            "riemann": "riemann/rh-ticket-166-positive-tail-diagonal.json",
            "collatz": "collatz/co-ticket-166-start-adaptive-excess.json",
            "goldbach": "goldbach/gb-ticket-166-bandlimited-anchor.json",
            "twin-prime": "twin-prime/tp-ticket-166-shifted-diagonal-haar.json",
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
