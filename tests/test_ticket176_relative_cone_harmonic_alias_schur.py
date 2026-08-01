from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket176_relative_cone_harmonic_alias_schur import (  # noqa: E402
    build_audit,
    collatz_harmonic_correction_audit,
    collatz_harmonic_record,
    goldbach_parity_alias_audit,
    mersenne_delay_row,
    positive_top_singular_vectors,
    riemann_relative_cone_audit,
    twin_weighted_schur_audit,
    weighted_schur_bound,
)


class Ticket176RelativeConeHarmonicAliasSchurTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.riemann = riemann_relative_cone_audit()
        cls.collatz = collatz_harmonic_correction_audit()
        cls.goldbach = goldbach_parity_alias_audit()
        cls.twin = twin_weighted_schur_audit()

    def test_riemann_relative_certificate_survives_tiny_scale(self) -> None:
        self.assertEqual(self.riemann["failure_count"], 0)
        for row in self.riemann["relative_scale_rows"]:
            self.assertLess(row["absolute_weyl_lower_bound"], 0)
            self.assertGreater(row["certified_exact_smallest_eigenvalue"], 0)
            self.assertTrue(
                math.isclose(
                    row["relative_lower_margin_delta_minus_epsilon"], 0.05
                )
            )

    def test_riemann_diagonal_tail_data_are_insufficient(self) -> None:
        row = self.riemann["diagonal_only_countermodel"]
        self.assertEqual(row["shared_tail_diagonal"], [0.0, 0.0])
        self.assertGreater(row["harmless_smallest_eigenvalue"], 0)
        self.assertLess(row["adverse_smallest_eigenvalue"], 0)

    def test_collatz_harmonic_envelope_and_exact_exception(self) -> None:
        self.assertEqual(self.collatz["failure_count"], 0)
        finite = self.collatz["finite_first_descent_audit"]
        self.assertEqual(finite["odd_starts_checked"], 49_999)
        self.assertEqual(finite["harmonic_boundary_non_crossing_starts"], [63])
        row = collatz_harmonic_record(63)
        self.assertEqual(row["first_descent_horizon"], 34)
        self.assertFalse(row["crosses_sufficient_harmonic_boundary"])

    def test_collatz_mersenne_family_has_arbitrary_initial_delay(self) -> None:
        for exponent in [4, 8, 16, 32]:
            row = mersenne_delay_row(exponent)
            self.assertEqual(
                row["certified_initial_valuation_one_steps"], exponent - 1
            )
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_parity_alias_is_lossless_and_tighter(self) -> None:
        self.assertEqual(self.goldbach["failure_count"], 0)
        aggregate = self.goldbach["aggregate"]
        self.assertEqual(aggregate["finite_targets"], 987)
        self.assertGreater(
            aggregate["parity_aliased_certificate_pass_count"],
            aggregate["unaliased_certificate_pass_count"],
        )
        self.assertEqual(aggregate["additional_finite_certificates"], 10)
        for row in self.goldbach["finite_fixed_farey_parity_alias_rows"]:
            self.assertLess(row["maximum_alias_identity_error"], 1e-7)
            self.assertTrue(all(row["checks"].values()))

    def test_goldbach_pre_alias_absolute_value_counts_null_direction(self) -> None:
        row = self.goldbach["exact_even_target_kernel_countermodel"]
        self.assertEqual(row["unaliased_spectral_l1"], 4)
        self.assertEqual(row["aliased_spectral_l1"], 0)
        self.assertEqual(set(row["all_even_target_minor_values"]), {0})

    def test_twin_optimized_weighted_schur_equals_spectral_norm(self) -> None:
        self.assertEqual(self.twin["failure_count"], 0)
        matrix = [[1.0, 2.0], [3.0, 4.0]]
        singular_value, left, right = positive_top_singular_vectors(matrix)
        bound = weighted_schur_bound(matrix, left, right)["bound"]
        self.assertTrue(math.isclose(bound, singular_value, rel_tol=1e-12))
        for row in self.twin["finite_t161_weighted_schur_rows"]:
            self.assertTrue(all(row["checks"].values()))

    def test_machine_audit_and_dags_remain_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            statuses = [
                node["status"] for node in audit[section_name]["proof_dag"]["nodes"]
            ]
            self.assertEqual(
                statuses,
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_generated_machine_artifact_matches_builder(self) -> None:
        payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket176-relative-cone-harmonic-alias-schur.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(payload["status"], "four_exact_reductions_all_conjectures_open")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(attempt["status"] == "open_not_proven" for attempt in payload["attempts"])
        )


if __name__ == "__main__":
    unittest.main()
