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

from ticket173_finite_section_cylinder_phase_tensor import (  # noqa: E402
    affine_word,
    build_audit,
    collatz_cylinder_stabilization_audit,
    cylinder_least_representative,
    goldbach_target_phase_audit,
    haar_basis,
    realized_valuations,
    riemann_finite_section_audit,
    twin_tensor_haar_audit,
)


class Ticket173FiniteSectionCylinderPhaseTensorTests(unittest.TestCase):
    def test_riemann_defects_decay_without_uniform_gap(self) -> None:
        audit = riemann_finite_section_audit()
        self.assertEqual(audit["failure_count"], 0)
        rows = audit["asymptotic_lower_defect_rows"]
        self.assertEqual(rows[-1]["exact_lambda_min"]["exact"], "1/128")
        self.assertEqual(rows[-1]["certified_lower_bound"]["exact"], "-1/128")
        self.assertLess(
            rows[-1]["lower_defect_eta_N"]["decimal"],
            rows[0]["lower_defect_eta_N"]["decimal"],
        )

    def test_collatz_affine_word_and_unique_residue_formula(self) -> None:
        word = [1, 2, 1, 3]
        constant, valuation_sum = affine_word(word)
        representative, modulus = cylinder_least_representative(word)
        self.assertGreater(constant, 0)
        self.assertEqual(modulus, 1 << (valuation_sum + 1))
        self.assertEqual(realized_valuations(representative, len(word)), word)

    def test_collatz_all_one_family_is_exponential_and_nonstabilizing(self) -> None:
        for horizon in [1, 2, 4, 8, 16]:
            representative, modulus = cylinder_least_representative([1] * horizon)
            self.assertEqual(representative, (1 << (horizon + 1)) - 1)
            self.assertEqual(modulus, 1 << (horizon + 1))

    def test_collatz_natural_support_examples_stabilize(self) -> None:
        audit = collatz_cylinder_stabilization_audit()
        self.assertEqual(audit["failure_count"], 0)
        self.assertEqual(
            sum(row["words_checked"] for row in audit["exhaustive_small_word_rows"]),
            sum(4**horizon for horizon in range(1, 7)),
        )
        for row in audit["natural_support_stabilization_rows"]:
            self.assertTrue(row["checks"]["representatives_eventually_equal_start"])

    def test_goldbach_exact_weighted_no_go(self) -> None:
        audit = goldbach_target_phase_audit()
        self.assertEqual(audit["failure_count"], 0)
        no_go = audit["exact_weighted_z8_no_go"]
        self.assertEqual(no_go["exact_convolution_value"], 1)
        self.assertGreater(
            no_go["negative_budget_decimal"], no_go["zero_frequency_anchor_decimal"]
        )

    def test_goldbach_zero_padded_reconstruction(self) -> None:
        audit = goldbach_target_phase_audit()
        for row in audit["finite_prime_target_phase_rows"]:
            self.assertGreater(row["minimum_ordered_representation_count"], 0)
            self.assertLess(row["maximum_fourier_reconstruction_error"], 1e-7)
        self.assertLess(
            sum(row["target_phase_gate_pass_count"] for row in audit["finite_prime_target_phase_rows"]),
            sum(row["even_targets_tested"] for row in audit["finite_prime_target_phase_rows"]),
        )

    def test_haar_basis_is_orthonormal(self) -> None:
        basis, scales = haar_basis(16)
        self.assertEqual(len(basis), 16)
        self.assertEqual(len(scales), 16)
        for left in range(16):
            for right in range(16):
                inner = sum(a * b for a, b in zip(basis[left], basis[right]))
                self.assertTrue(
                    math.isclose(
                        inner,
                        1.0 if left == right else 0.0,
                        rel_tol=1e-12,
                        abs_tol=1e-12,
                    )
                )

    def test_twin_cross_scale_countermodel(self) -> None:
        audit = twin_tensor_haar_audit()
        self.assertEqual(audit["failure_count"], 0)
        for row in audit["different_scale_rank_one_no_go_rows"]:
            self.assertLess(row["same_scale_pair_energy"], 1e-12)
            self.assertTrue(
                math.isclose(
                    row["cross_scale_pair_energy"],
                    1.0,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                )
            )

    def test_machine_audit_and_proof_dags_remain_open(self) -> None:
        audit = build_audit()
        self.assertEqual(audit["machine_audit"]["total_failure_count"], 0)
        self.assertEqual(audit["machine_audit"]["conjecture_resolution_count"], 0)
        for section_name in ["riemann", "collatz", "goldbach", "twin_prime"]:
            section = audit[section_name]
            statuses = [node["status"] for node in section["proof_dag"]["nodes"]]
            self.assertEqual(
                statuses,
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_generated_machine_artifact_matches_builder(self) -> None:
        path = (
            ROOT
            / "data"
            / "open-problem"
            / "ticket173-finite-section-cylinder-phase-tensor.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "four_exact_structural_audits_all_conjectures_open")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(all(row["status"] == "open_not_proven" for row in payload["attempts"]))


if __name__ == "__main__":
    unittest.main()
