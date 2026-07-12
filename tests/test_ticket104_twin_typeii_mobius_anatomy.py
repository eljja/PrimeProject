from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ticket104_twin_typeii_mobius_anatomy import audit_mobius_anatomy, outer_mobius_weights  # noqa: E402


class Ticket104TwinTypeIIMobiusAnatomyTests(unittest.TestCase):
    def test_outer_weights_are_nonnegative(self) -> None:
        _, weights, metadata = outer_mobius_weights(2_000)
        start = metadata["u"] + 1
        self.assertGreater(metadata["nonzero_weight_count"], 0)
        self.assertGreaterEqual(float(weights[start:].min()), -1e-12)

    def test_outer_and_abel_identities_reconstruct_type_ii(self) -> None:
        row = audit_mobius_anatomy(2_000)
        self.assertLess(row["outer_identity_absolute_error"], 1e-7)
        self.assertLess(row["abel_reconstruction_absolute_error"], 1e-7)

    def test_triangle_bounds_dominate_actual_signed_sum(self) -> None:
        row = audit_mobius_anatomy(2_000)
        self.assertGreaterEqual(row["l1_signed_mass"], abs(row["outer_weight_signed_sum"]))
        self.assertGreaterEqual(row["abel_triangle_envelope"], abs(row["outer_weight_signed_sum"]))


if __name__ == "__main__":
    unittest.main()
