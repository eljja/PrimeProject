from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket161_commoncore_baker_angle_typeii import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_audit,
    build_attempts,
    continued_fraction_convergents,
    least_natural_parameter,
    tent_projection_error,
)


class Ticket161CommonCoreBakerAngleTypeIITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket161-commoncore-baker-angle-typeii.json"
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

    def test_tent_projection_error_reacts_to_resolution(self) -> None:
        resolved, _ = tent_projection_error(32, 1024)
        critical, _ = tent_projection_error(32, 128)
        underresolved, _ = tent_projection_error(32, 5)
        self.assertLess(resolved, critical)
        self.assertLess(critical, underresolved)

    def test_riemann_transport_rows_and_trends(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        self.assertEqual(len(computation["finite_tent_transport_rows"]), 15)
        self.assertTrue(all(computation["trend_checks"].values()))
        self.assertEqual(computation["failure_count"], 0)

    def test_collatz_least_parameter_congruence(self) -> None:
        self.assertEqual(least_natural_parameter(8, 4), 1)
        self.assertEqual(least_natural_parameter(10, 5), 3)

    def test_continued_fraction_contains_known_convergents(self) -> None:
        convergents = continued_fraction_convergents(50_000)
        self.assertIn((8, 5), convergents)
        self.assertIn((65, 41), convergents)
        self.assertIn((24727, 15601), convergents)

    def test_collatz_exact_scan_and_minimum(self) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        self.assertEqual(computation["scan_limit_m"], 50_000)
        self.assertEqual(computation["observed_failure_lengths"], [])
        self.assertEqual(
            computation["minimum_observed_descent_ratio"]["exact"],
            "13/7",
        )
        self.assertEqual(
            computation["minimum_observed_descent_ratio"]["word_length_m"],
            5,
        )
        self.assertTrue(all(computation["summary_checks"].values()))

    def test_collatz_convergent_candidates_descend(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "continued_fraction_candidate_rows"
        ]
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["descent_holds"] for row in rows))

    def test_goldbach_phase_criterion_improves_energy_route(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_prime_reflection_angle_rows"
        ]
        self.assertEqual([row["even_endpoint_N"] for row in rows], [
            1000,
            2000,
            4000,
            8000,
            16000,
        ])
        self.assertTrue(
            all(
                row["energy_only_positive_certificate_count"] == 0
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["phase_aware_positive_certificate_count"]
                == row["audited_even_count"]
                for row in rows
            )
        )

    def test_goldbach_average_angle_no_go_is_exact(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_average_angle_no_go_rows"
        ]
        self.assertEqual(len(rows), 5)
        self.assertTrue(
            all(
                row["harmful_reflection_coefficient"] == -1.0
                and all(row["checks"].values())
                for row in rows
            )
        )

    def test_twin_checkerboard_has_zero_margins(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "exact_zero_marginal_checkerboard_rows"
        ]
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_twin_centered_incidence_contract(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        rows = computation["finite_cubic_rough_centered_incidence_rows"]
        self.assertEqual(
            [row["double_semiprime_pair_count_QQ"] for row in rows],
            [35, 284, 2453, 19074],
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(all(computation["trend_checks"].values()))

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
            "riemann": (
                "riemann/rh-ticket-161-common-core-resolution.json"
            ),
            "collatz": (
                "collatz/co-ticket-161-baker-front-loaded.json"
            ),
            "goldbach": "goldbach/gb-ticket-161-reflection-angle.json",
            "twin-prime": (
                "twin-prime/tp-ticket-161-centered-typeii.json"
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
