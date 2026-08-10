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

import ticket204_mesh_necklace_exceptional_kernel as ticket204


class Ticket204MeshNecklaceExceptionalKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket204.build_audit()

    def test_derivative_mesh_certificate_and_sampling_no_go(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        certified = section["exact_certified_regression"]
        no_go = section["finite_sampling_no_go"]
        self.assertEqual(certified["certified_contour_supremum_upper"], "39/280")
        self.assertEqual(certified["strict_rouche_margin_lower"], "241/280")
        self.assertTrue(certified["rouche_hypothesis_certified"])
        self.assertEqual(no_go["maximum_sample_ratio"], 0)
        self.assertEqual(no_go["missed_midpoint_ratio"], 2)
        self.assertEqual(no_go["comparison_zero_count_inside"], 0)
        self.assertEqual(no_go["analytic_zero_count_inside"], 8)
        self.assertFalse(
            section["aggregate"]["actual_xi_relative_derivative_bound_constructed"]
        )

    def test_collatz_rotation_and_power_reduction(self) -> None:
        rotation = ticket204.rotation_identity_row((3, 1))
        self.assertEqual(rotation["denominator_D"], 7)
        self.assertEqual(rotation["numerator_B"], 11)
        self.assertEqual(rotation["rotated_numerator_B"], 5)
        self.assertTrue(rotation["identity_2a0_Brot_equals_3B_plus_D"])
        self.assertTrue(rotation["divisibility_invariant"])

        repeated = ticket204.repetition_identity_row((4, 1), 4)
        self.assertTrue(repeated["numerator_factorization_holds"])
        self.assertTrue(repeated["denominator_factorization_holds"])
        self.assertTrue(repeated["rational_cycle_value_preserved"])
        self.assertTrue(repeated["divisibility_equivalent"])

        aggregate = self.audit["collatz"]["reproducible_computation"]["aggregate"]
        self.assertGreater(
            aggregate["cross_length_cyclic_necklace_count"],
            aggregate["cross_length_unique_primitive_necklace_count"],
        )
        self.assertGreater(aggregate["repeated_necklaces_removed"], 0)
        self.assertEqual(
            aggregate["non_all_two_divisible_word_count_in_tested_box"], 0
        )
        self.assertFalse(aggregate["nontrivial_cycles_excluded_for_all_lengths"])

    def test_goldbach_subunit_threshold_and_density_no_go(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        finite = section["exact_finite_prime_arithmetic_rows"]
        one_exception = section["one_exception_no_go_rows"]
        sparse = section["sparse_infinite_exception_no_go_rows"]
        self.assertEqual(finite[-1]["limit"], 10_000)
        self.assertEqual(finite[-1]["exception_count"], 0)
        self.assertTrue(all(row["exception_count"] == 1 for row in one_exception))
        self.assertTrue(all(not row["subunit_threshold_met"] for row in one_exception))
        densities = [Fraction(row["exception_density"]) for row in sparse]
        self.assertTrue(
            all(densities[index + 1] < densities[index] for index in range(4))
        )
        self.assertTrue(all(row["still_has_counterexamples"] for row in sparse))
        self.assertFalse(
            section["aggregate"]["actual_tail_exception_bound_below_one_constructed"]
        )

    def test_twin_psd_no_go_and_indefinite_rank_two_escape(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        no_go = section["psd_square_semiprime_no_go"]
        escape = section["exact_indefinite_rank_two_escape"]
        self.assertFalse(no_go["strict_psd_parity_separator_exists"])
        self.assertEqual(escape["exact_rank"], 2)
        self.assertEqual(escape["principal_minor_on_1_and_first_prime"], "-9/4")
        self.assertEqual(set(escape["prime_channel_values_K_1_p"]), {"1/2"})
        self.assertEqual(escape["semiprime_channel_distinct_values_K_p_q"], ["-1"])
        self.assertTrue(escape["formal_factor_channel_separation_holds"])
        self.assertFalse(
            section["aggregate"]["factorization_free_arithmetic_realization_constructed"]
        )

    def test_machine_audit_keeps_all_parent_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
            section = self.audit[section_key]
            self.assertIn("No ", section["claim_boundary"])
            self.assertEqual(
                section["proof_dag"]["nodes"][-1]["status"],
                "open_not_proven",
            )

    def test_written_outputs_match_schema_and_attempts(self) -> None:
        ticket204.write_outputs(self.audit)
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket204-mesh-necklace-exceptional-kernel.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema"], ticket204.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )


if __name__ == "__main__":
    unittest.main()
