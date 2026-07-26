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

from ticket155_range_prefix_sublinear_conditional import (  # noqa: E402
    SCHEMA,
    build_audit,
)


class Ticket155RangePrefixSublinearConditionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket155-range-prefix-sublinear-conditional.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_global_and_per_problem_artifacts_match_schema(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(
            {row["problem_id"] for row in self.payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        paths = [
            "riemann/rh-ticket-155-range-tail-coordinate-no-go.json",
            "collatz/co-ticket-155-initial-prefix-descent.json",
            "goldbach/gb-ticket-155-sublinear-wheel-squeeze.json",
            "twin-prime/tp-ticket-155-conditional-semiprime-transfer.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_harmonic_coordinate_tail_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_coordinate_profile_rows"
        ]
        self.assertEqual(
            [row["coordinate_cutoff_N"] for row in rows],
            [1, 2, 4, 8, 16, 32],
        )
        for row in rows:
            cutoff = row["coordinate_cutoff_N"]
            self.assertEqual(
                Fraction(
                    row["harmonic_profile_coordinate_tail_cost"]["exact"]
                ),
                Fraction(1, cutoff + 1),
            )
            self.assertEqual(
                Fraction(
                    row["harmonic_profile_new_coordinate_mass"]["exact"]
                ),
                Fraction(1, cutoff * (cutoff + 1)),
            )
            self.assertEqual(
                Fraction(row["range_projection_tail_cost"]["exact"]),
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_arbitrary_profile_contract_is_basis_dependent(
        self,
    ) -> None:
        profile = self.audit["riemann"]["reproducible_computation"][
            "profile_realization"
        ]
        self.assertEqual(profile["optimal_range_projection_rank"], 1)
        self.assertEqual(
            Fraction(profile["optimal_range_projection_tail"]["exact"]),
            0,
        )
        self.assertIn("e_(j-1)-e_j", profile["coordinate_mass_formula"])

    def test_collatz_reverse_suffix_is_final_record_condition(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_record_equivalence_rows"
        ]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertEqual(
                row["reverse_suffix_floor_two"],
                row["final_value_is_running_maximum"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_later_local_descent_does_not_descend_from_start(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_later_local_descent_no_go_rows"
        ]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertEqual(row["valuation_word"], [1, 2])
            self.assertGreater(row["local_drop"], 0)
            self.assertGreater(row["net_change_from_initial"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_local_descent_wait_has_no_uniform_bound(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_unbounded_waiting_rows"
        ]
        delays = [
            row["certified_initial_all_one_valuation_count"]
            for row in rows
        ]
        self.assertEqual(delays, [1, 2, 4, 7, 12, 20])
        self.assertTrue(
            all(right > left for left, right in zip(delays, delays[1:]))
        )
        for row in rows:
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_sublinear_wheel_schedule_fails_energy_gate(
        self,
    ) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_sublinear_wheel_schedule_rows"]
        self.assertEqual(
            [
                (row["even_endpoint_N"], row["growing_wheel_W"])
                for row in rows
            ],
            [(10_000, 30), (100_000, 210), (1_000_000, 2_310)],
        )
        fractions = []
        for row in rows:
            self.assertLess(
                row["projection_certificate_lower_bound"],
                0,
            )
            self.assertGreater(
                row["actual_prime_theta_reflection_correlation"],
                0,
            )
            self.assertLess(
                row["wheel_exponent_logW_over_logN"],
                0.6,
            )
            self.assertTrue(all(row["checks"].values()))
            fractions.append(row["projection_energy_fraction"])
        self.assertTrue(
            all(
                right < left
                for left, right in zip(fractions, fractions[1:])
            )
        )
        self.assertTrue(
            computation[
                "finite_projection_fractions_strictly_decrease"
            ]
        )

    def test_twin_conditional_transfer_identity_is_exact(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_conditional_transfer_rows"
        ]
        self.assertEqual(
            [row["X"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        )
        for row in rows:
            margin = Fraction(
                row["ambient_margin_below_one"]["exact"]
            )
            shift = Fraction(
                row["total_conditional_transfer_shift"]["exact"]
            )
            deficit = Fraction(
                row["deficit_one_minus_M_over_R"]["exact"]
            )
            incidence = Fraction(
                row["conditional_incidence_M_over_R"]["exact"]
            )
            self.assertEqual(margin - shift, deficit)
            self.assertEqual(1 - incidence, deficit)
            self.assertGreater(deficit, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_twin_absolute_covariance_decay_is_not_relative_saving(
        self,
    ) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_rare_event_covariance_no_go_rows"
        ]
        covariances = []
        for row in rows:
            covariance = Fraction(row["absolute_covariance"]["exact"])
            covariances.append(covariance)
            self.assertEqual(
                Fraction(
                    row["normalized_covariance_over_rho"]["exact"]
                ),
                Fraction(1, 5),
            )
            self.assertEqual(
                Fraction(row["conditional_shift"]["exact"]),
                Fraction(1, 5),
            )
            self.assertTrue(all(row["checks"].values()))
        self.assertTrue(
            all(
                right < left
                for left, right in zip(covariances, covariances[1:])
            )
        )

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "ActualWeilFiniteCoreRangeConstructionAnd"
                "PositiveSchurMatrix"
            ),
            "collatz": (
                "EveryNaturalStartCrossesAnInitialAffineDescentThreshold"
            ),
            "goldbach": (
                "EffectiveGoldbachMajorMinorArcReflectionLowerBound"
                "WithFiniteJoin"
            ),
            "twin_prime": (
                "ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving"
            ),
        }
        for problem, next_theorem in expected.items():
            section = self.audit[problem]
            self.assertEqual(
                section["route_decision"]["next_theorem"],
                next_theorem,
            )
            dag = section["proof_dag"]
            self.assertEqual(len(dag["nodes"]), 3)
            self.assertEqual(len(dag["edges"]), 2)
            self.assertEqual(dag["nodes"][-1]["label"], next_theorem)
            self.assertEqual(
                dag["nodes"][-1]["status"],
                "open_not_proven",
            )

    def test_claim_boundaries_forbid_resolution_claims(self) -> None:
        self.assertIn(
            "resolves no target conjecture",
            self.audit["proof_boundary"],
        )
        for problem in [
            "riemann",
            "collatz",
            "goldbach",
            "twin_prime",
        ]:
            self.assertTrue(
                self.audit[problem]["claim_boundary"].startswith("No ")
            )


if __name__ == "__main__":
    unittest.main()
