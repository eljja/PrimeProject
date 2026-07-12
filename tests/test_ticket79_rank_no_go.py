from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket79_archimedean_two_adic_rank_no_go_lab import (  # noqa: E402
    accelerated_step,
    analyze_rank_no_go,
    contraction_value,
    expansion_value,
)


class Ticket79RankNoGoTests(unittest.TestCase):
    def test_exact_expansion_family(self) -> None:
        for m in (1, 2, 8, 32):
            for q in (1, 2, 7):
                start = expansion_value(m, q)
                current = start
                for step in range(m):
                    self.assertEqual(current, expansion_value(m, q, step))
                    current, valuation = accelerated_step(current)
                    self.assertEqual(valuation, 1)
                self.assertEqual(current, expansion_value(m, q, m))
                self.assertGreater(current * (1 << m), start * (3**m))

    def test_exact_nonterminal_contraction_family(self) -> None:
        for r in (1, 2, 8, 32, 64):
            start = contraction_value(r)
            self.assertEqual(3 * start + 1, 5 * (1 << (2 * r + 1)))
            terminal, valuation = accelerated_step(start)
            self.assertEqual(terminal, 5)
            self.assertEqual(valuation, 2 * r + 1)

    def test_full_audit_has_no_failure(self) -> None:
        audit = analyze_rank_no_go()
        self.assertEqual(audit["computational_failure_count"], 0)
        self.assertEqual(
            audit["theorem_status"],
            "bounded_archimedean_two_adic_one_step_rank_refuted_exactly_no_collatz_resolution",
        )
        self.assertEqual(
            audit["next_theorem_target"],
            "MinimalCounterexampleValuationSurplusContradiction",
        )


if __name__ == "__main__":
    unittest.main()
