from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket170_interval_tail_besov_multiscale import (  # noqa: E402
    SCHEMA,
    build_attempts,
    build_audit,
    collatz_tail_threshold,
    collatz_word_data,
    dyadic_autocorrelation_shells,
    matrix_sign_bilinear_max,
)


class Ticket170IntervalTailBesovMultiscaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket170-interval-tail-besov-multiscale.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_audit_has_no_false_resolution(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_riemann_gap_stability_and_entrywise_no_go(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        rows = computation["exact_interval_proxy_rows"]
        self.assertEqual(
            [row["positive_block_dimension_n"] for row in rows],
            [4, 8, 16, 32, 64, 128],
        )
        self.assertTrue(computation["vanishing_entrywise_radius_no_go_holds"])
        self.assertEqual(rows[0]["vanishing_but_unstable_entry_radius"]["exact"], "1/2")
        self.assertEqual(rows[-1]["vanishing_but_unstable_entry_radius"]["exact"], "1/64")
        for row in rows:
            self.assertEqual(row["stable_frobenius_and_operator_radius"]["exact"], "1/2")
            self.assertNotEqual(
                row["unstable_exact_inertia"],
                row["approximate_kkt_canonical_inertia"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_affine_data_and_tail_threshold(self) -> None:
        self.assertEqual(collatz_word_data([1, 1, 1]), (3, 3, 19))
        row = collatz_tail_threshold([1] * 8)
        self.assertEqual(row["correction_C"], 3**8 - 2**8)
        self.assertEqual(row["least_prefix_start_n0"], 2**9 - 1)
        self.assertEqual(row["tail_threshold_A"], 7)

    def test_collatz_every_audited_tail_child_descends(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        rows = computation["prefixwise_finite_tail_rows"]
        self.assertEqual([row["tail_threshold_A"] for row in rows], [3, 2, 3, 2, 2, 4, 2, 1])
        for row in rows:
            self.assertTrue(row["threshold_is_minimal"])
            self.assertEqual(len(row["audited_tail_children"]), 5)
            for child in row["audited_tail_children"]:
                self.assertGreater(child["exact_descent_slack"], 0)
                self.assertLess(child["child_endpoint"], child["least_child_start"])
                self.assertTrue(all(child["checks"].values()))

    def test_collatz_global_cap_is_refuted_by_all_one_family(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        self.assertTrue(
            computation["no_fixed_global_immediate_descent_tail_threshold"]
        )
        rows = computation[
            "all_one_global_cap_no_go_rows"
        ]
        self.assertEqual(
            [row["all_one_word_length_m"] for row in rows],
            [1, 2, 4, 8, 16, 32, 64],
        )
        self.assertEqual([row["tail_threshold_A"] for row in rows], [3, 3, 4, 7, 11, 21, 40])
        for row in rows:
            self.assertTrue(all(row["checks"].values()))

    def test_dyadic_shells_partition_all_cyclic_frequencies(self) -> None:
        for size in [8, 16, 64, 16384]:
            shells = dyadic_autocorrelation_shells(size)
            indices = [index for shell in shells for index in shell]
            self.assertEqual(sorted(indices), list(range(size)))
            self.assertEqual(len(indices), len(set(indices)))

    def test_goldbach_shell_bound_is_valid_but_finite(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_goldbach_autocorrelation_shell_rows"
        ]
        self.assertEqual(
            [row["low_pass_bandwidth_K"] for row in rows],
            [16, 64, 256, 1024, 4096],
        )
        for row in rows:
            self.assertGreaterEqual(
                row["autocorrelation_besov_shell_sqrt_bound"] + 1e-10,
                row["exact_autocorrelation_l1_sqrt_bound"],
            )
            self.assertGreaterEqual(
                row["exact_autocorrelation_l1_sqrt_bound"] + 1e-10,
                row["observed_uniform_tail"],
            )
            self.assertLess(row["autocorrelation_besov_shell_sqrt_bound"], 1)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_fixed_lag_window_no_go_is_exact(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_fixed_lag_window_no_go_rows"
        ]
        self.assertEqual([row["retained_lag_window_H"] for row in rows], [1, 2, 4, 8, 16, 32])
        for row in rows:
            self.assertEqual(row["hidden_lag_q"], row["retained_lag_window_H"] + 1)
            self.assertEqual(row["shared_normalized_zero_lag"]["exact"], "1/1")
            self.assertEqual(row["hidden_normalized_coefficient_at_plus_minus_q"]["exact"], "1/2")
            self.assertEqual(row["hidden_cosine_signal_uniform_norm_squared"]["exact"], "2/1")
            self.assertTrue(all(row["checks"].values()))

    def test_twin_sign_search_obeys_spectral_bridge(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_t161_sign_bilinear_rows"
        ]
        self.assertEqual([row["X"] for row in rows], [10000, 100000, 1000000, 10000000])
        for row in rows:
            self.assertLessEqual(
                row["normalized_max_sign_bilinear_deviation"],
                row["four_times_normalized_spectral_bound"] + 1e-12,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_fixed_partition_can_hide_fine_dependence(self) -> None:
        checkerboard = [[1, -1], [-1, 1]]
        self.assertEqual(matrix_sign_bilinear_max(checkerboard), 4)
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "exact_fixed_partition_invisibility_rows"
        ]
        for row in rows:
            self.assertEqual(row["coarse_top_singular_value"], 0)
            self.assertGreater(row["fine_top_singular_value"], 0)
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
            "riemann": "riemann/rh-ticket-170-interval-gap.json",
            "collatz": "collatz/co-ticket-170-child-tail.json",
            "goldbach": "goldbach/gb-ticket-170-autocorrelation-besov.json",
            "twin-prime": "twin-prime/tp-ticket-170-multiscale-typeii.json",
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
