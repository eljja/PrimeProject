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

from ticket153_essential_tail_geometric_reflection_parity import (  # noqa: E402
    SCHEMA,
    build_audit,
)


class Ticket153EssentialTailGeometricReflectionParityTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket153-essential-tail-geometric-reflection-parity.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_keeps_every_conjecture_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_generated_global_and_per_problem_artifacts(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(len(self.payload["attempts"]), 4)
        self.assertEqual(
            {row["problem_id"] for row in self.payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        paths = [
            "riemann/rh-ticket-153-essential-tail-schur.json",
            "collatz/co-ticket-153-geometric-cylinder-tail.json",
            "goldbach/gb-ticket-153-reflection-energy.json",
            "twin-prime/tp-ticket-153-cubic-rough-parity.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_positive_tail_has_essential_norm_obstruction(
        self,
    ) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_essential_norm_rows"
        ]
        self.assertEqual(len(rows), 5)
        for row in rows:
            delta = Fraction(
                row["positive_identity_tail_delta"]["exact"]
            )
            lower = Fraction(
                row["operator_norm_distance_lower_bound"]["exact"]
            )
            self.assertEqual(lower, delta)
            self.assertGreater(delta, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_schur_margin_is_exact_and_sharp(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_schur_complement_rows"
        ]
        self.assertEqual(len(rows), 8)
        self.assertEqual(
            sum(row["certified_positive"] for row in rows),
            4,
        )
        for row in rows:
            delta = Fraction(
                row["tail_coercivity_delta"]["exact"]
            )
            norm_squared = Fraction(
                row["coupling_norm_squared"]["exact"]
            )
            core = Fraction(row["finite_core_floor"]["exact"])
            margin = Fraction(row["exact_schur_margin"]["exact"])
            self.assertEqual(margin, core - norm_squared / delta)
            self.assertEqual(row["certified_positive"], margin >= 0)
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_children_have_exact_geometric_tail(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_extension_partition_rows"
        ]
        self.assertEqual(len(rows), 21)
        for row in rows:
            cap = row["lift_residue_bits_B"]
            counts = {
                int(key): value
                for key, value in row[
                    "exact_next_valuation_counts"
                ].items()
            }
            self.assertEqual(
                counts,
                {
                    valuation: 1 << (cap - valuation)
                    for valuation in range(1, cap + 1)
                },
            )
            self.assertEqual(
                Fraction(row["conditional_tail_mass"]["exact"]),
                Fraction(1, 1 << cap),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_noncontracting_coefficient_tail_decays(self) -> None:
        computation = self.audit["collatz"][
            "reproducible_computation"
        ]
        rows = computation["finite_negative_drift_rows"]
        probabilities = [
            Fraction(
                row[
                    "exact_noncontracting_linear_coefficient_probability"
                ]["exact"]
            )
            for row in rows
        ]
        self.assertEqual(
            [row["word_length_m"] for row in rows],
            [4, 8, 16, 32, 64, 128],
        )
        self.assertTrue(
            all(
                right < left
                for left, right in zip(
                    probabilities,
                    probabilities[1:],
                )
            )
        )
        self.assertTrue(
            computation[
                "finite_noncontracting_probabilities_strictly_decreasing"
            ]
        )
        self.assertAlmostEqual(
            computation["constants"]["expected_log_linear_multiplier"],
            math.log(3 / 4),
            places=15,
        )

    def test_goldbach_prime_theta_reflection_identity(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_reflection_energy_rows"
        ]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000],
        )
        for row in rows:
            self.assertGreater(
                row["unordered_prime_pair_representations"],
                0,
            )
            self.assertGreater(
                row["prime_theta_reflection_correlation"],
                0,
            )
            self.assertAlmostEqual(
                row["prime_theta_reflection_correlation"],
                row["symmetric_projection_energy"]
                - row["antisymmetric_projection_energy"],
                places=7,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_cubic_rough_parity_identity(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cubic_rough_parity_rows"
        ]
        self.assertEqual(
            [row["X"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        )
        for row in rows:
            self.assertEqual(
                row["symmetrized_shifted_liouville_sum"],
                2
                * (
                    row["semiprime_semiprime_pairs_QQ"]
                    - row["prime_prime_pairs_PP"]
                ),
            )
            self.assertGreater(
                row["prime_prime_excess_PP_minus_QQ"],
                0,
            )
            self.assertLess(
                row["symmetrized_shifted_liouville_sum"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "ActualWeilPositiveTailDecompositionWithCertified"
                "SchurComplement"
            ),
            "collatz": (
                "UniformAffineOffsetControlOnNaturalValuationRays"
            ),
            "goldbach": (
                "ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArc"
                "ReflectionGap"
            ),
            "twin_prime": (
                "UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs"
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
