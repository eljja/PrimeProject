from __future__ import annotations

import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket221_sharp_obstruction_certificates as ticket221


class Ticket221SharpObstructionCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket221.build_audit()

    def test_riemann_scale_uniform_envelope_diverges(self) -> None:
        section = self.audit["sharp_obstruction_certificate_audit"]["riemann"]
        computation = section["reproducible_computation"]
        self.assertEqual(
            [row["dyadic_index_j"] for row in computation["scale_maximum_rows"]],
            list(range(-12, 13)),
        )
        self.assertTrue(
            all(
                row["maximum_one_quarter_verified"]
                and row["stationary_point_verified"]
                for row in computation["scale_maximum_rows"]
            )
        )
        self.assertEqual(
            computation["universal_envelope_partial_sum_rows"][0][
                "universal_envelope_partial_sum_lower_bound"
            ],
            "3/4",
        )
        aggregate = computation["aggregate"]
        self.assertTrue(aggregate["universal_coordinatewise_envelope_diverges"])
        self.assertFalse(aggregate["actual_arithmetic_coupled_tail_budget_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_collatz_order_information_is_not_in_baker_datum(self) -> None:
        section = self.audit["sharp_obstruction_certificate_audit"]["collatz"]
        computation = section["reproducible_computation"]
        self.assertTrue(
            all(
                row["single_baker_datum_for_all_permutations"]
                and row["distinct_intercept_count"] > 1
                for row in computation["permutation_class_rows"]
            )
        )
        self.assertTrue(
            all(
                row["identity_verified"]
                for row in computation["adjacent_swap_identity_rows"]
            )
        )
        witness = computation["opposite_side_witness"]
        self.assertEqual(witness["common_A"], 81)
        self.assertEqual(witness["common_D"], 1024)
        self.assertEqual(witness["common_D_minus_A"], 943)
        self.assertEqual(witness["low_fixed_point"], "133/943")
        self.assertEqual(witness["high_fixed_point"], "995/943")
        self.assertTrue(all(witness["checks"].values()))
        aggregate = computation["aggregate"]
        self.assertFalse(
            aggregate["baker_separation_alone_sufficient_for_primitive_words"]
        )
        self.assertFalse(aggregate["collatz_conjecture_resolved"])

    def test_goldbach_lp_zero_barrier_is_sharp(self) -> None:
        section = self.audit["sharp_obstruction_certificate_audit"]["goldbach"]
        computation = section["reproducible_computation"]
        self.assertEqual(len(computation["exact_lp_radius_rows"]), 12)
        self.assertTrue(
            all(
                row["sharp_boundary_verified"]
                for row in computation["exact_lp_radius_rows"]
            )
        )
        self.assertTrue(
            all(
                all(row["checks"].values())
                for row in computation["finite_prefix_extension_rows"]
            )
        )
        previous = computation["ticket220_finite_margin_summary"]
        self.assertEqual(previous["direct_eighth_moment_folds_certified"], 150)
        self.assertEqual(previous["refinement_bridges_certified"], 140)
        self.assertLess(
            Decimal(previous["worst_minkowski_to_zero_barrier_ratio"]),
            Decimal(1),
        )
        aggregate = computation["aggregate"]
        self.assertFalse(
            aggregate["uniform_cofinal_margin_from_prime_distribution_proved"]
        )
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_twin_low_degree_parity_orthogonality(self) -> None:
        section = self.audit["sharp_obstruction_certificate_audit"]["twin_prime"]
        computation = section["reproducible_computation"]
        rows = computation["boolean_parity_orthogonality_rows"]
        self.assertEqual([row["boolean_dimension_m"] for row in rows], list(range(2, 13)))
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(
            all(row["maximum_low_degree_absolute_correlation_sum"] == 0 for row in rows)
        )
        self.assertTrue(
            all(
                row["full_degree_correlation_sum"] == 2 ** row["boolean_dimension_m"]
                for row in rows
            )
        )
        aggregate = computation["aggregate"]
        self.assertFalse(
            aggregate["arithmetic_parity_breaking_type_ii_lower_bound_proved"]
        )
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        root = self.audit["sharp_obstruction_certificate_audit"]
        machine = root["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["corrected_next_lemma_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

        ticket221.write_outputs(self.audit)
        integrated_path = (
            ROOT / "data/open-problem/ticket221-sharp-obstruction-certificates.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket221.SCHEMA)
        self.assertEqual(integrated["status"], "open_not_proven")
        self.assertEqual(len(integrated["attempts"]), 4)
        for attempt in integrated["attempts"]:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertTrue(attempt["declared_proposition"])
            self.assertTrue(attempt["discarded_route"])
            self.assertTrue(attempt["remaining_gap"])
            self.assertTrue(attempt["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
