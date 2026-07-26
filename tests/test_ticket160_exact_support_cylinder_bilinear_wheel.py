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

from ticket160_exact_support_cylinder_bilinear_wheel import (  # noqa: E402
    SCHEMA,
    build_audit,
    contracting_tail_payload,
    crt_pairwise,
    cylinder_residue,
    valuation_prefix,
)


class Ticket160ExactSupportCylinderBilinearWheelTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data/open-problem/"
                "ticket160-exact-support-cylinder-bilinear-wheel.json"
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
            "riemann/rh-ticket-160-exact-support-transport.json",
            "collatz/co-ticket-160-cylinder-realizability.json",
            "goldbach/gb-ticket-160-bilinear-proxy.json",
            "twin-prime/tp-ticket-160-fixed-wheel-crt.json",
        ]
        for relative in paths:
            payload = json.loads(
                (ROOT / "data/open-problem" / relative).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(payload["schema"], SCHEMA)

    def test_riemann_prime_support_is_exactly_closed(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        row = next(
            item
            for item in section["finite_prime_support_rows"]
            if item["prime_cutoff_c"] == 16
        )
        self.assertEqual(row["interior_prime_power_count"], 9)
        self.assertEqual(row["boundary_prime_power_count"], 1)
        self.assertEqual(row["outside_prime_power_count"], 17)
        self.assertEqual(row["maximum_absolute_omitted_weight"], 0)
        self.assertTrue(all(row["checks"].values()))
        self.assertEqual(
            Fraction(section["prime_support_remainder"]["exact"]),
            0,
        )

    def test_riemann_cross_cutoff_profiles_do_not_nest_raw(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "exact_cross_cutoff_profile_rows"
        ]
        self.assertEqual(
            Fraction(rows[0]["hat_g_4_over_pi"]["exact"]),
            1,
        )
        self.assertEqual(
            Fraction(rows[0]["hat_g_16_over_pi"]["exact"]),
            Fraction(3, 2),
        )
        self.assertEqual(
            Fraction(rows[1]["hat_g_4_over_pi"]["exact"]),
            0,
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_collatz_words_have_unique_exact_cylinders(self) -> None:
        words = [
            (1,),
            (2,),
            (1, 3),
            (3, 1, 1, 2),
            (1, 2, 4, 1, 3),
        ]
        for word in words:
            residue, modulus = cylinder_residue(word)
            self.assertEqual(valuation_prefix(residue, len(word)), word)
            self.assertEqual(modulus, 1 << (sum(word) + 1))

    def test_collatz_contracting_tail_is_exact(self) -> None:
        payload = contracting_tail_payload((1, 1, 4))
        self.assertTrue(payload["contracting"])
        self.assertTrue(all(payload["checks"].values()))
        self.assertGreater(
            payload["least_descending_cylinder_start"],
            Fraction(payload["threshold_C_over_D"]["exact"]),
        )

    def test_collatz_kraft_rows_leave_a_real_gap(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_cylinder_summary_rows"
        ]
        self.assertEqual([row["word_length_m"] for row in rows], [2, 3, 4, 5])
        for row in rows:
            self.assertEqual(
                row["word_count"],
                row["unique_residue_count"],
            )
            self.assertGreater(
                Fraction(row["uncovered_density_lower_bound"]["exact"]),
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_collatz_front_loaded_infinite_family_transfers(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"][
            "front_loaded_unbounded_threshold_natural_transfer"
        ]
        rows = section["exact_natural_transfer_rows"]
        self.assertEqual(rows[-1]["word_length_m"], 1024)
        previous_lower_bound = Fraction(0)
        for row in rows:
            lower_bound = Fraction(
                row["explicit_threshold_lower_bound"]["exact"]
            )
            self.assertGreater(lower_bound, previous_lower_bound)
            self.assertTrue(all(row["checks"].values()))
            previous_lower_bound = lower_bound

    def test_goldbach_bilinear_proxy_identity_is_exact_numerically(
        self,
    ) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_bilinear_proxy_identity_rows"
        ]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertAlmostEqual(
                row["observed_minus_proxy_defect"],
                row["factorized_defect"],
                places=8,
            )
            self.assertGreaterEqual(row["bound_slack"], -1e-9)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_cauchy_constant_one_is_sharp(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "exact_sharp_reflection_counterexample_rows"
        ]
        self.assertEqual([row["group_size_L"] for row in rows], [11, 12, 17, 32])
        for row in rows:
            self.assertAlmostEqual(
                row["positive_reflection_form"],
                1,
                places=9,
            )
            self.assertAlmostEqual(
                row["negative_reflection_form"],
                -1,
                places=9,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_crt_helper_solves_pairwise_system(self) -> None:
        value, modulus = crt_pairwise([2, 3, 2], [3, 5, 7])
        self.assertEqual(modulus, 105)
        self.assertEqual(value % 3, 2)
        self.assertEqual(value % 5, 3)
        self.assertEqual(value % 7, 2)

    def test_twin_fixed_wheel_has_crt_composite_mimics(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_fixed_wheel_crt_rows"
        ]
        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertEqual(
                row["twin_witness"][0] % row["wheel_modulus_M"],
                row["double_composite_witness"][0]
                % row["wheel_modulus_M"],
            )
            self.assertTrue(all(row["checks"].values()))

    def test_twin_factor_horizon_is_necessary_and_sufficient(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "finite_cubic_rough_factor_horizon_rows"
        ]
        self.assertEqual(
            [row["exact_separation_factor_horizon_tau_X"] for row in rows],
            [17, 71, 251, 811, 3037],
        )
        for row in rows:
            self.assertGreater(row["prime_prime_pair_count_PP"], 0)
            self.assertGreater(
                row["semiprime_semiprime_pair_count_QQ"],
                0,
            )
            self.assertTrue(all(row["checks"].values()))

    def test_proof_dags_end_at_one_open_lemma(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            dag = self.audit[key]["proof_dag"]
            self.assertEqual(
                [node["status"] for node in dag["nodes"]],
                [
                    "refuted_or_misidentified",
                    "proved_exact",
                    "open_not_proven",
                ],
            )
            self.assertEqual(len(dag["edges"]), 2)

    def test_claim_boundaries_do_not_claim_solutions(self) -> None:
        self.assertIn(
            "resolves no target conjecture",
            self.audit["proof_boundary"],
        )
        for attempt in self.payload["attempts"]:
            self.assertTrue(attempt["claim_boundary"].startswith("No "))


if __name__ == "__main__":
    unittest.main()
