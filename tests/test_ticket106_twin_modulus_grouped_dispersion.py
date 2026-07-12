from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket106_twin_modulus_grouped_dispersion import audit_grouped_dispersion, grouped_modulus_vectors  # noqa: E402


class Ticket106TwinModulusGroupedDispersionTests(unittest.TestCase):
    def test_grouped_vectors_have_nonempty_support(self) -> None:
        coefficient, _, _, metadata = grouped_modulus_vectors(2_000)
        self.assertGreater(metadata["support_count"], 0)
        self.assertGreater(float(abs(coefficient).max()), 0)

    def test_grouped_identity_reconstructs_centered_terms(self) -> None:
        row = audit_grouped_dispersion(2_000)
        self.assertLess(row["centered_identity_absolute_error"], 1e-7)
        self.assertLess(row["baseline_identity_absolute_error"], 1e-7)

    def test_bucket_partition_covers_grouped_support(self) -> None:
        row = audit_grouped_dispersion(2_000)
        self.assertEqual(sum(bucket["support_count"] for bucket in row["bucket_rows"]), row["support_count"])

    def test_occupancy_ladder_partitions_sparse_and_complement(self) -> None:
        row = audit_grouped_dispersion(2_000)
        for occupancy in row["occupancy_rows"]:
            self.assertAlmostEqual(
                occupancy["signed_contribution"] + occupancy["complement_signed_contribution"],
                row["grouped_centered_discrepancy"],
            )


if __name__ == "__main__":
    unittest.main()
