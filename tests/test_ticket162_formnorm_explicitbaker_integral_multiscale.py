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

from ticket162_formnorm_explicitbaker_integral_multiscale import (  # noqa: E402
    SCHEMA,
    STATUS,
    atanh_log_interval,
    block_projection_energy,
    build_attempts,
    build_audit,
    certified_log2_three_convergents,
    matveev_threshold,
    smooth_bump_h1_projection_error,
)


class Ticket162FormNormExplicitBakerIntegralMultiscaleTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket162-formnorm-explicitbaker-integral-multiscale.json"
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
        self.assertIn(
            "resolves no target conjecture",
            self.payload["claim_boundary"],
        )

    def test_riemann_h2_to_h1_schedule_separates(self) -> None:
        resolved, _, resolved_bound = smooth_bump_h1_projection_error(
            32,
            1024,
        )
        critical, _, _ = smooth_bump_h1_projection_error(32, 128)
        underresolved, _, _ = smooth_bump_h1_projection_error(32, 5)
        self.assertLess(resolved, critical)
        self.assertLess(critical, underresolved)
        self.assertLessEqual(resolved, resolved_bound)

    def test_riemann_uniform_h1_ball_no_go_is_exact(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        rows = computation["exact_h1_unit_ball_no_go_rows"]
        self.assertEqual(len(rows), 5)
        self.assertTrue(
            all(
                row["source_h1_norm"] == 1.0
                and row["h1_projection_error"] == 1.0
                and all(row["checks"].values())
                for row in rows
            )
        )

    def test_exact_log_intervals_enclose_known_bounds(self) -> None:
        log_two_lower, log_two_upper = atanh_log_interval(2)
        log_three_lower, log_three_upper = atanh_log_interval(3)
        self.assertLess(log_two_lower, log_two_upper)
        self.assertLess(log_three_lower, log_three_upper)
        self.assertLess(log_three_lower / log_two_upper, Fraction(8, 5))
        self.assertGreater(log_three_upper / log_two_lower, Fraction(19, 12))

    def test_matveev_threshold_is_certified_and_minimal(self) -> None:
        certificate = matveev_threshold()
        self.assertEqual(
            certificate["first_certified_asymptotic_length_M"],
            21_554_214_227,
        )
        self.assertTrue(all(certificate["checks"].values()))
        self.assertGreater(certificate["threshold_margin_lower"], 0)
        self.assertLess(certificate["previous_margin_upper"], 0)

    def test_certified_cf_crosses_matveev_threshold(self) -> None:
        _, convergents, certificate = certified_log2_three_convergents(
            21_554_214_227
        )
        self.assertGreater(
            certificate["last_certified_denominator"],
            21_554_214_227,
        )
        upper_denominators = {
            row["denominator_q"]
            for row in convergents
            if row["side"] == "upper"
        }
        self.assertTrue({5, 41, 306, 15_601}.issubset(upper_denominators))

    def test_collatz_selected_family_is_closed_but_sparse(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        candidates = computation["primitive_upper_convergent_rows"]
        coverage = computation["exact_compositional_coverage_no_go_rows"]
        self.assertEqual(len(candidates), 10)
        self.assertTrue(
            all(all(row["checks"].values()) for row in candidates)
        )
        self.assertTrue(all(computation["summary_checks"].values()))
        self.assertGreater(
            coverage[0]["selected_compositional_fraction"],
            coverage[-1]["selected_compositional_fraction"],
        )

    def test_goldbach_integral_moment_gate_is_sharp(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_prime_normalized_moment_rows"]
        spikes = computation["exact_unit_spike_sharpness_rows"]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 2_000, 4_000, 8_000, 16_000],
        )
        self.assertTrue(
            all(
                row["normalized_negative_minor_moment_budget"] >= 1
                and not row["unit_exception_gate_passes"]
                and all(row["checks"].values())
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["normalized_negative_error_budget"] == 1.0
                and all(row["checks"].values())
                for row in spikes
            )
        )

    def test_twin_fixed_bin_checkerboard_is_invisible(self) -> None:
        checkerboard = [
            [1 if (row + column) % 2 == 0 else -1 for column in range(4)]
            for row in range(4)
        ]
        self.assertEqual(block_projection_energy(checkerboard, 2), 0)
        self.assertEqual(block_projection_energy(checkerboard, 4), 16)

    def test_twin_multiscale_energy_telescopes(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        rows = computation["finite_cubic_rough_multiscale_rows"]
        self.assertEqual(
            [row["double_semiprime_pair_count_QQ"] for row in rows],
            [284, 2453, 19074],
        )
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            levels = row["dyadic_projection_levels"]
            detail_sum = sum(
                Fraction(level["detail_energy"]["exact"]) for level in levels
            )
            self.assertEqual(
                detail_sum,
                Fraction(levels[-1]["projection_energy"]["exact"]),
            )

    def test_each_proof_dag_ends_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[key]["proof_dag"]["nodes"]
            self.assertEqual(
                [node["status"] for node in nodes],
                [
                    "refuted_or_insufficient",
                    "proved_exact",
                    "open_not_proven",
                ],
            )

    def test_attempts_have_one_next_lemma_each(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual(len(attempts), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        self.assertTrue(
            all(attempt["candidate_theorem"] for attempt in attempts)
        )

    def test_per_problem_json_contracts(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-162-h1-form-transport.json",
            "collatz": (
                "collatz/co-ticket-162-explicit-family-closure.json"
            ),
            "goldbach": "goldbach/gb-ticket-162-integral-moment.json",
            "twin-prime": (
                "twin-prime/tp-ticket-162-multiscale-incidence.json"
            ),
        }
        for problem_id, relative in paths.items():
            payload = json.loads(
                (
                    ROOT / "data" / "open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)
            self.assertEqual(payload["problem_id"], problem_id)
            self.assertEqual(payload["status"], "open_not_proven")
            self.assertIn("No ", payload["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
