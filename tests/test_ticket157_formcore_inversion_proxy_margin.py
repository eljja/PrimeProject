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

from ticket157_formcore_inversion_proxy_margin import (  # noqa: E402
    SCHEMA,
    affine_constant,
    build_audit,
    descending_swap_certificate,
)


class Ticket157FormCoreInversionProxyMarginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket157-formcore-inversion-proxy-margin.json"
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
            "riemann/rh-ticket-157-nested-form-core.json",
            "collatz/co-ticket-157-inversion-gain.json",
            "goldbach/gb-ticket-157-phase-proxy-l1.json",
            "twin-prime/tp-ticket-157-information-margin.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_nested_core_budget_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_nested_form_core_rows"
        ]
        self.assertEqual(
            [row["nested_core_dimension_N"] for row in rows],
            [1, 2, 4, 8, 16],
        )
        for row in rows:
            truncated = Fraction(
                row["truncated_form_core_minimum"]["exact"]
            )
            error = Fraction(
                row["uniform_cutoff_form_error_epsilon_T"]["exact"]
            )
            promoted = Fraction(
                row["promoted_exact_form_lower_bound"]["exact"]
            )
            self.assertEqual(truncated - error, promoted)
            self.assertGreater(promoted, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_finite_core_sweep_has_hidden_direction_no_go(
        self,
    ) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_hidden_direction_no_go_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(
                Fraction(row["checked_core_minimum"]["exact"]),
                1,
            )
            self.assertEqual(
                Fraction(row["full_operator_minimum"]["exact"]),
                -1,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_adjacent_swap_gain_telescope_is_exact(self) -> None:
        for word in [
            (1, 1, 2, 3),
            (1, 3),
            (2, 1, 3),
            (1, 1, 4),
        ]:
            certificate = descending_swap_certificate(word)
            descending = tuple(certificate["descending_word"])
            self.assertEqual(
                list(descending),
                sorted(word, reverse=True),
            )
            self.assertEqual(
                certificate["summed_adjacent_swap_gain"],
                affine_constant(descending) - affine_constant(word),
            )
            self.assertTrue(
                all(row["formula_holds"] for row in certificate["swaps"])
            )

    def test_collatz_natural_order_is_decisive_on_finite_scan(self) -> None:
        scan = self.audit["collatz"]["reproducible_computation"][
            "finite_first_descent_inversion_scan"
        ]
        self.assertEqual(scan["audited_odd_start_count"], 49_999)
        self.assertEqual(
            scan["worst_order_multiset_certificate_count"],
            49_733,
        )
        self.assertEqual(
            scan["natural_order_inversion_gain_required_count"],
            266,
        )
        first = scan["sample_inversion_gain_required_rows"][0]
        self.assertEqual(first["initial_odd_start_n"], 27)
        self.assertGreater(
            first["inversion_gain_G"],
            first["worst_order_threshold_excess"],
        )
        self.assertTrue(all(first["checks"].values()))

    def test_goldbach_negative_mass_obeys_l1_proxy_stability(
        self,
    ) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_phase_proxy_rows"
        ]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 2_000, 4_000, 8_000, 16_000, 32_000],
        )
        for row in rows:
            actual = row["actual_minor_negative_mass"]
            self.assertGreater(
                row["unordered_prime_pair_representations"],
                0,
            )
            for proxy in row["data_dependent_block_proxy_rows"]:
                self.assertLessEqual(
                    actual,
                    proxy["stable_negative_mass_upper_bound"] + 1e-7,
                )
                self.assertTrue(all(proxy["checks"].values()))

    def test_goldbach_block_proxy_route_is_rejected(self) -> None:
        computation = self.audit["goldbach"][
            "reproducible_computation"
        ]
        self.assertEqual(
            computation["block_proxy_certificate_counts"],
            {"8": 0, "32": 0, "128": 0},
        )

    def test_goldbach_l2_dimension_loss_is_exact_and_sharp(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_l2_dimension_loss_saturation_rows"
        ]
        for row in rows:
            self.assertEqual(
                Fraction(row["residual_l2_squared"]["exact"]),
                1,
            )
            self.assertEqual(
                Fraction(row["residual_l1"]["exact"]),
                row["sqrt_dimension_factor"],
            )
            self.assertEqual(
                Fraction(row["negative_real_mass"]["exact"]),
                row["sqrt_dimension_factor"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_information_budget_certifies_all_finite_rows(
        self,
    ) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation[
            "finite_cubic_rough_information_margin_rows"
        ]
        self.assertEqual(
            [row["X"] for row in rows],
            [1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        )
        self.assertEqual(
            computation["finite_information_certificate_count"],
            5,
        )
        for row in rows:
            self.assertGreater(row["certificate_slack"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_twin_little_o_is_not_necessary(self) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_little_o_not_necessary_rows"]
        self.assertEqual(len(rows), 6)
        self.assertGreater(
            computation["normalized_information_positive_limit_nats"],
            0,
        )
        for row in rows:
            self.assertEqual(
                Fraction(row["conditional_shift_delta"]["exact"]),
                Fraction(-1, 5),
            )
            self.assertEqual(
                Fraction(
                    row["two_side_actual_conditional_sum"]["exact"]
                ),
                Fraction(2, 5),
            )
            self.assertGreater(row["mutual_information_over_rho"], 0)
            self.assertTrue(all(row["checks"].values()))

    def test_next_lemmas_are_single_and_dags_end_open(self) -> None:
        expected = {
            "riemann": (
                "UniformArchimedeanTailFormBoundOn"
                "NestedExplicitWeilCore"
            ),
            "collatz": (
                "NaturalValuationInversionGainDominates"
                "WorstOrderThresholdExcess"
            ),
            "goldbach": (
                "ArithmeticBinaryGoldbachPhaseProxyWithUniformL1Residual"
                "AndFiniteJoin"
            ),
            "twin_prime": (
                "UniformCubicRoughInformationBudgetBelowSemiprimeMargin"
                "AfterEffectiveCutoff"
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
