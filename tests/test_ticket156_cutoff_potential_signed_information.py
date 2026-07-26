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

from ticket156_cutoff_potential_signed_information import (  # noqa: E402
    SCHEMA,
    build_audit,
)


class Ticket156CutoffPotentialSignedInformationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket156-cutoff-potential-signed-information.json"
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
            "riemann/rh-ticket-156-three-axis-cutoff.json",
            "collatz/co-ticket-156-weighted-suffix-potential.json",
            "goldbach/gb-ticket-156-signed-minor-negative-mass.json",
            "twin-prime/tp-ticket-156-normalized-mutual-information.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_three_axis_margin_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_three_axis_error_budget_rows"
        ]
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]["positivity_certified"])
        self.assertFalse(rows[1]["positivity_certified"])
        for row in rows:
            observed = Fraction(
                row["computed_minimum_eigenvalue"]["exact"]
            )
            total = Fraction(row["total_operator_error"]["exact"])
            certified = Fraction(row["certified_lower_bound"]["exact"])
            self.assertEqual(observed - total, certified)
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_fixed_cutoff_sign_can_reverse_at_limit(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_precision_stable_cutoff_reversal_rows"
        ]
        for row in rows:
            self.assertLess(
                Fraction(
                    row["positive_limit_family_lambda_min"]["exact"]
                ),
                0,
            )
            self.assertGreater(
                Fraction(
                    row["negative_limit_family_lambda_min"]["exact"]
                ),
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_weighted_potential_identity_is_exact(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_weighted_identity_rows"
        ]
        for row in rows:
            self.assertEqual(
                Fraction(row["weighted_suffix_potential_Phi"]["exact"]),
                Fraction(
                    row[
                        "normalized_affine_constant_C_over_2S"
                    ]["exact"]
                ),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_floor_two_is_not_necessary(self) -> None:
        scan = self.audit["collatz"]["reproducible_computation"][
            "finite_first_descent_scan"
        ]
        self.assertEqual(scan["audited_odd_start_count"], 49_999)
        self.assertEqual(
            scan["first_descent_prefixes_failing_floor_two"],
            12_991,
        )
        first = scan["sample_exact_no_go_rows"][0]
        self.assertEqual(first["initial_odd_start_n"], 7)
        self.assertEqual(first["valuation_word"], [1, 1, 2, 3])
        self.assertEqual(first["first_descent_endpoint"], 5)
        self.assertEqual(
            Fraction(first["exact_affine_threshold_theta"]["exact"]),
            Fraction(73, 47),
        )
        self.assertTrue(all(first["checks"].values()))

    def test_goldbach_signed_minor_partition_reconstructs(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_signed_minor_rows"
        ]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 2_000, 4_000, 8_000, 16_000, 32_000],
        )
        for index, row in enumerate(rows):
            self.assertLess(row["reconstruction_error"], 1e-6)
            if index < 3:
                self.assertGreater(
                    row["one_sided_certificate_lower_bound"],
                    0,
                )
            else:
                self.assertLess(
                    row["one_sided_certificate_lower_bound"],
                    0,
                )
            self.assertLess(
                row["phase_blind_certificate_lower_bound"],
                0,
            )
            self.assertGreater(
                row["unordered_prime_pair_representations"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))
        computation = self.audit["goldbach"]["reproducible_computation"]
        self.assertEqual(computation["one_sided_certificate_count"], 3)
        self.assertEqual(computation["phase_blind_certificate_count"], 0)

    def test_twin_information_requires_rare_event_normalization(
        self,
    ) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_rare_event_information_no_go_rows"]
        information = [row["mutual_information_nats"] for row in rows]
        self.assertTrue(
            all(
                right < left
                for left, right in zip(information, information[1:])
            )
        )
        self.assertTrue(
            computation["rare_event_information_strictly_decreases"]
        )
        limit = computation["normalized_information_limit_nats"]
        self.assertGreater(limit, 0)
        self.assertAlmostEqual(
            rows[-1]["mutual_information_over_rho"],
            limit,
            places=6,
        )
        for row in rows:
            self.assertEqual(
                Fraction(row["conditional_shift_delta"]["exact"]),
                Fraction(1, 5),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_arithmetic_rows_obey_pinsker(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cubic_rough_information_rows"
        ]
        self.assertEqual(
            [row["X"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        )
        for row in rows:
            self.assertTrue(all(row["checks"].values()))
            self.assertTrue(all(row["left"]["checks"].values()))
            self.assertTrue(all(row["right"]["checks"].values()))

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "ExplicitWeilGalerkinCoreAndUniformTwoAxisOperatorErrorBound"
            ),
            "collatz": (
                "EveryNaturalValuationRayCrossesItsWeightedSuffixPotential"
            ),
            "goldbach": (
                "UniformBinaryGoldbachMinorNegativePhaseMassBound"
                "WithFiniteJoin"
            ),
            "twin_prime": (
                "ShiftTwoCubicRoughMutualInformationLittleOSelectionMass"
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
