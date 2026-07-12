from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket107_twin_sparse_tail_recombination import (  # noqa: E402
    analyze_ticket107,
    audit_sparse_tail_recombination,
)


class Ticket107TwinSparseTailRecombinationTests(unittest.TestCase):
    def test_q_built_type_ii_matches_vaughan_decomposition(self) -> None:
        row = audit_sparse_tail_recombination(2_000)
        self.assertLess(row["type_ii_q_to_vaughan_max_error"], 1e-9)
        self.assertLess(row["lambda_reconstruction_max_error"], 1e-10)

    def test_sparse_q_and_n_correlations_match(self) -> None:
        row = audit_sparse_tail_recombination(2_000)
        self.assertLess(row["sparse_shifted_q_to_n_absolute_error"], 1e-9)
        self.assertLess(row["joint_correlation_absolute_error"], 1e-9)

    def test_q_to_n_grouping_cannot_increase_l1(self) -> None:
        row = audit_sparse_tail_recombination(2_000)
        self.assertLessEqual(row["sparse_n_l1"], row["sparse_q_l1"] + 1e-9)
        self.assertLessEqual(row["sparse_n_support_count"], row["sparse_q_support_count"])

    def test_audited_sparse_centered_sign_is_not_stable(self) -> None:
        audit = analyze_ticket107()
        self.assertEqual(audit["machine_audit"]["centered_sparse_sign_count"], 2)
        self.assertEqual(audit["machine_audit"]["maximum_horizon"], 8_000_000)
        self.assertEqual(audit["machine_audit"]["row_count"], 6)
        self.assertEqual(audit["machine_audit"]["contract_failure_count"], 0)


if __name__ == "__main__":
    unittest.main()
