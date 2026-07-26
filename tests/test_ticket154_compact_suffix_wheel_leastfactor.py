from __future__ import annotations

import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket154_compact_suffix_wheel_leastfactor import (  # noqa: E402
    SCHEMA,
    build_audit,
)


class Ticket154CompactSuffixWheelLeastFactorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket154-compact-suffix-wheel-leastfactor.json"
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
            "riemann/rh-ticket-154-compact-schur-tail.json",
            "collatz/co-ticket-154-reverse-suffix-descent.json",
            "goldbach/gb-ticket-154-fixed-wheel-projection.json",
            "twin-prime/tp-ticket-154-least-factor-deficit.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_compact_tail_pays_exact_schur_error(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_compact_promotion_rows"
        ]
        self.assertEqual(
            [row["finite_tail_cutoff_N"] for row in rows],
            [1, 2, 4, 8, 12, 16],
        )
        for row in rows:
            cutoff = row["finite_tail_cutoff_N"]
            tail = Fraction(
                row[
                    "preconditioned_coupling_tail_norm_squared"
                ]["exact"]
            )
            finite_margin = Fraction(
                row["finite_schur_margin"]["exact"]
            )
            full_margin = Fraction(
                row["certified_full_schur_margin"]["exact"]
            )
            self.assertEqual(tail, Fraction(1, 3 * 4**cutoff))
            self.assertEqual(finite_margin, tail)
            self.assertEqual(full_margin, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_uncertified_finite_cutoff_hides_negativity(
        self,
    ) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_hidden_tail_counterexample_rows"
        ]
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertEqual(
                Fraction(row["observed_schur_margin"]["exact"]),
                Fraction(1, 2),
            )
            self.assertEqual(
                Fraction(row["full_schur_margin"]["exact"]),
                Fraction(-1, 2),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_reverse_suffix_certificate_controls_affine_term(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_reverse_suffix_certificate_rows"
        ]
        self.assertEqual(len(rows), 7)
        for row in rows:
            threshold = Fraction(row["exact_affine_threshold"]["exact"])
            bound = Fraction(
                row["theorem_threshold_upper_bound"]["exact"]
            )
            self.assertLessEqual(threshold, bound)
            if row["reverse_suffix_floor_q"] == 2:
                self.assertLessEqual(threshold, 1)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_certificate_mass_has_exact_ballot_formula(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_certificate_mass_rows"
        ]
        masses = []
        for row in rows:
            length = row["word_length_m"]
            mass = Fraction(
                row["exact_reverse_suffix_certificate_mass"]["exact"]
            )
            self.assertEqual(
                mass,
                Fraction(math.comb(2 * length, length), 4**length),
            )
            self.assertTrue(all(row["checks"].values()))
            masses.append(mass)
        self.assertTrue(
            all(
                right < left
                for left, right in zip(masses, masses[1:])
            )
        )

    def test_collatz_total_surplus_does_not_determine_threshold(
        self,
    ) -> None:
        computation = self.audit["collatz"]["reproducible_computation"]
        no_go = computation["same_surplus_affine_threshold_no_go"]
        self.assertEqual(no_go["word_one"], [1, 3])
        self.assertEqual(no_go["word_two"], [3, 1])
        self.assertEqual(
            Fraction(no_go["word_one_threshold"]["exact"]),
            Fraction(5, 7),
        )
        self.assertEqual(
            Fraction(no_go["word_two_threshold"]["exact"]),
            Fraction(11, 7),
        )
        self.assertTrue(all(no_go["checks"].values()))
        for row in computation["finite_affine_ordering_rows"]:
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_fixed_wheel_projection_identity_and_no_go(
        self,
    ) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["finite_fixed_wheel_projection_rows"]
        self.assertEqual(len(rows), 9)
        by_wheel: dict[int, list[float]] = {}
        for row in rows:
            self.assertEqual(
                row["admissible_residue_pair_count_direct"],
                row["admissible_residue_pair_count_formula"],
            )
            self.assertFalse(row["projection_certificate_positive"])
            self.assertGreater(
                row["actual_prime_theta_reflection_correlation"],
                row["projection_certificate_lower_bound"],
            )
            self.assertTrue(all(row["checks"].values()))
            by_wheel.setdefault(
                row["fixed_wheel_W"],
                [],
            ).append(row["projection_energy_fraction"])
        for wheel, values in by_wheel.items():
            self.assertIn(wheel, [6, 30, 210])
            self.assertTrue(
                all(
                    right < left
                    for left, right in zip(values, values[1:])
                )
            )
        self.assertTrue(
            all(
                computation[
                    "fixed_wheel_projection_fractions_strictly_decrease"
                ].values()
            )
        )

    def test_twin_least_factor_deficit_is_exact(self) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_least_factor_deficit_rows"]
        self.assertEqual(
            [row["X"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        )
        for row in rows:
            self.assertEqual(
                row["deficit_R_minus_M"],
                row["prime_prime_excess_PP_minus_QQ"],
            )
            self.assertEqual(
                row["total_medium_least_factor_incidence_M"],
                2 * row["semiprime_semiprime_pairs_QQ"]
                + row["mixed_pairs_PQ_QP"],
            )
            self.assertLess(row["mean_pair_incidence_M_over_R"], 1)
            self.assertTrue(all(row["checks"].values()))

    def test_twin_small_prime_fingerprint_has_parity_collisions(
        self,
    ) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_small_prime_fingerprint_collision_rows"
        ]
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertIsNotNone(row["prime_prime_example"])
            self.assertIsNotNone(row["semiprime_semiprime_example"])
            self.assertEqual(
                row["shared_small_prime_divisibility_fingerprint"],
                "all_zero_for_primes_at_most_z",
            )
            self.assertTrue(all(row["checks"].values()))

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "ActualWeilCompactCouplingWithEffective"
                "PreconditionedTailRate"
            ),
            "collatz": (
                "EveryNaturalValuationRayHitsAReverseSuffix"
                "SurplusDescentBlock"
            ),
            "goldbach": (
                "EffectiveGrowingWheelProjectionDominanceAtEvery"
                "LargeEvenEndpoint"
            ),
            "twin_prime": (
                "UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne"
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
