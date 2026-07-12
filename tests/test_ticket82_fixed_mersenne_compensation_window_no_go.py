from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket82_fixed_mersenne_compensation_window_no_go_lab import (  # noqa: E402
    accelerated_step,
    analyze_fixed_window_no_go,
    audit_horizon,
    reference_symbolic_states,
)


class Ticket82FixedMersenneCompensationWindowNoGoTests(unittest.TestCase):
    def test_reference_symbolic_family_and_word(self) -> None:
        states = reference_symbolic_states(32)
        self.assertEqual([row["incoming_valuation"] for row in states[1:]], [3, 4] + [2] * 30)
        for row in states:
            post_index = row["post_index"]
            numerator = 3 ** (3 + post_index) + row["constant"]
            self.assertEqual(numerator >> row["denominator_power"], row["reference_value"])

    def test_small_explicit_progression_witnesses_replay_exactly(self) -> None:
        for horizon in (0, 1, 2, 4):
            audit = audit_horizon(horizon)
            k = audit["first_certified_progression_exponent"]
            start = (1 << k) - 1
            current = (3**k - 1) // 2
            self.assertGreater(current, start)
            observed: list[int] = []
            for _ in range(horizon):
                current, valuation = accelerated_step(current)
                observed.append(valuation)
                self.assertGreater(current, start)
            self.assertEqual(observed, audit["post_reference_word"])

    def test_full_symbolic_audit_and_claim_boundary(self) -> None:
        result = analyze_fixed_window_no_go()
        audit = result["machine_audit"]
        self.assertEqual(result["computational_failure_count"], 0)
        self.assertEqual(audit["horizon_case_count"], 129)
        self.assertEqual(audit["symbolic_state_count"], 8385)
        self.assertEqual(audit["transition_condition_count"], 8256)
        self.assertEqual(result["next_theorem_target"], "MersenneGrowingWindowDescent")
        self.assertIn("neither constructs a divergent orbit", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
