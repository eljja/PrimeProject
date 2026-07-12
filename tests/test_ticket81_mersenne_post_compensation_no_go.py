from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket81_mersenne_post_compensation_no_go_lab import (  # noqa: E402
    EXACT_DESCENT_EXCEPTIONS,
    accelerated_step,
    analyze_post_compensation_no_go,
    expected_post_block_valuation,
    initial_block_iterate,
    mersenne_start,
    post_block_iterate,
)


class Ticket81MersennePostCompensationNoGoTests(unittest.TestCase):
    def test_exact_initial_block_and_stabilized_residue(self) -> None:
        for k in range(2, 65):
            start = mersenne_start(k)
            current = start
            for step in range(1, k):
                current, valuation = accelerated_step(current)
                self.assertEqual(valuation, 1)
                self.assertEqual(current, initial_block_iterate(k, step))
                self.assertGreater(current, start)
            self.assertEqual(start % (1 << k), start)

    def test_first_post_block_step_and_exact_exception_set(self) -> None:
        observed_exceptions: set[int] = set()
        for k in range(2, 257):
            current = initial_block_iterate(k, k - 1)
            post, valuation = accelerated_step(current)
            self.assertEqual(valuation, expected_post_block_valuation(k))
            self.assertEqual(post, post_block_iterate(k))
            if post < mersenne_start(k):
                observed_exceptions.add(k)
        self.assertEqual(observed_exceptions, EXACT_DESCENT_EXCEPTIONS)

    def test_full_audit_has_no_failure_and_preserves_claim_boundary(self) -> None:
        result = analyze_post_compensation_no_go()
        audit = result["machine_audit"]
        self.assertEqual(result["computational_failure_count"], 0)
        self.assertEqual(audit["mersenne_case_count"], 1023)
        self.assertEqual(audit["initial_step_replay_count"], 523776)
        self.assertEqual(audit["descent_exception_k"], [2, 4, 8])
        self.assertEqual(audit["post_compensation_non_descent_count"], 1020)
        self.assertEqual(result["next_theorem_target"], "MersenneAdaptiveCompensationWindow")
        self.assertIn("neither proves nor disproves Collatz", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
