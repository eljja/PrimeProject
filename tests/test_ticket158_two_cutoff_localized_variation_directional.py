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

from ticket158_two_cutoff_localized_variation_directional import (  # noqa: E402
    SCHEMA,
    build_audit,
    cyclic_total_variation,
    cyclic_trailing_average,
    ordinary_inversion_count,
)


class Ticket158TwoCutoffLocalizedVariationDirectionalTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket158-two-cutoff-localized-variation-directional.json"
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
            "riemann/rh-ticket-158-two-cutoff-budget.json",
            "collatz/co-ticket-158-localized-inversion.json",
            "goldbach/gb-ticket-158-variation-proxy.json",
            "twin-prime/tp-ticket-158-directional-information.json",
        ]
        for relative in paths:
            payload = json.loads(
                (
                    ROOT / "data/open-problem" / relative
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_positive_two_cutoff_composition(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_positive_composition_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            finite_value = Fraction(
                row["finite_archimedean_cutoff_value_q_c_N_T"]["exact"]
            )
            prime_error = Fraction(
                row["prime_band_remainder_A_c_N"]["exact"]
            )
            promoted = Fraction(
                row["promoted_full_form_lower_bound"]["exact"]
            )
            self.assertEqual(promoted, finite_value - prime_error)
            self.assertGreaterEqual(promoted, 0)
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_negative_two_cutoff_composition(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "finite_negative_composition_rows"
        ]
        self.assertEqual(len(rows), 3)
        for row in rows:
            finite_value = Fraction(
                row["finite_archimedean_cutoff_value_q_c_N_T"]["exact"]
            )
            prime_error = Fraction(
                row["prime_band_remainder_A_c_N"]["exact"]
            )
            tail_error = Fraction(
                row["archimedean_tail_budget_B_c_N_T"]["exact"]
            )
            promoted = Fraction(
                row["promoted_full_form_upper_bound"]["exact"]
            )
            self.assertEqual(
                promoted,
                finite_value + prime_error + tail_error,
            )
            self.assertLess(promoted, 0)

    def test_riemann_single_cutoff_no_go_keeps_negative_full_value(
        self,
    ) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "single_cutoff_no_go_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertGreater(
                Fraction(
                    row["finite_archimedean_cutoff_value"]["exact"]
                ),
                0,
            )
            self.assertEqual(
                Fraction(row["full_form_value"]["exact"]),
                -1,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_parametric_words_share_coarse_statistics(
        self,
    ) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "parametric_coarse_inversion_no_go_rows"
        ]
        self.assertEqual([row["large_valuation_K"] for row in rows], [
            6,
            8,
            10,
            12,
        ])
        for row in rows:
            word_a = tuple(row["word_A"])
            word_b = tuple(row["word_B"])
            self.assertEqual(
                ordinary_inversion_count(word_a),
                ordinary_inversion_count(word_b),
            )
            self.assertFalse(row["abstract_start_one_descends_under_A"])
            self.assertTrue(row["abstract_start_one_descends_under_B"])
            self.assertNotEqual(
                row["localized_inversion_gain_A"],
                row["localized_inversion_gain_B"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_natural_scan_refutes_coarse_gain_uniqueness(
        self,
    ) -> None:
        scan = self.audit["collatz"]["reproducible_computation"][
            "finite_natural_first_descent_collision_scan"
        ]
        self.assertEqual(scan["audited_odd_start_count"], 49_999)
        self.assertEqual(scan["coarse_signature_count"], 3_862)
        self.assertEqual(
            scan["ambiguous_coarse_signature_count"],
            677,
        )
        self.assertTrue(
            scan["sample_ambiguous_signature_rows"][0][
                "distinct_localized_gain_count"
            ]
            > 1
        )
        self.assertTrue(all(scan["checks"].values()))

    def test_goldbach_moving_average_variation_bound(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_goldbach_variation_proxy_rows"
        ]
        self.assertEqual(
            [row["even_endpoint_N"] for row in rows],
            [1_000, 2_000, 4_000, 8_000, 16_000, 32_000],
        )
        for row in rows:
            self.assertGreater(
                row["unordered_prime_pair_representations"],
                0,
            )
            for proxy in row["moving_average_variation_rows"]:
                self.assertLessEqual(
                    proxy["actual_complex_residual_l1"],
                    proxy["variation_residual_upper_bound"] + 1e-7,
                )
                self.assertTrue(all(proxy["checks"].values()))

    def test_goldbach_variation_constant_is_sharp(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_variation_constant_sharpness_rows"
        ]
        self.assertEqual(
            [row["dimension_m"] for row in rows],
            [8, 32, 128],
        )
        for row in rows:
            self.assertEqual(
                row["actual_residual_l1"],
                row["variation_residual_upper_bound"],
            )
            self.assertTrue(all(row["checks"].values()))
        self.assertEqual(
            self.audit["goldbach"]["reproducible_computation"][
                "variation_proxy_certificate_counts"
            ],
            {"2": 0, "4": 0, "8": 0},
        )

    def test_cyclic_variation_helper_saturates_on_alternation(
        self,
    ) -> None:
        values = [1 + 0j, -1 + 0j] * 4
        proxy = cyclic_trailing_average(values, 2)
        self.assertTrue(all(value == 0 for value in proxy))
        self.assertEqual(cyclic_total_variation(values), 16)
        self.assertEqual(
            sum(abs(value - model) for value, model in zip(values, proxy)),
            8,
        )

    def test_twin_directional_budget_is_strictly_sharper(self) -> None:
        computation = self.audit["twin_prime"][
            "reproducible_computation"
        ]
        rows = computation["finite_directional_information_margin_rows"]
        self.assertEqual([row["X"] for row in rows], [
            1_000,
            10_000,
            100_000,
            1_000_000,
            10_000_000,
        ])
        self.assertEqual(
            computation["finite_directional_certificate_count"],
            5,
        )
        self.assertEqual(
            computation["finite_rows_with_strict_directional_saving"],
            4,
        )
        for row in rows:
            self.assertLess(
                row["directional_information_upper_ratio"],
                1,
            )
            self.assertLessEqual(
                row["positive_shift_only_pinsker_budget"],
                row["absolute_pinsker_budget"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_information_does_not_determine_shift_sign(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "exact_information_direction_blindness_rows"
        ]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(
                Fraction(row["positive_conditional_shift"]["exact"]),
                -Fraction(row["negative_conditional_shift"]["exact"]),
            )
            self.assertGreater(
                row["shared_mutual_information_nats"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_every_proof_dag_ends_open(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
