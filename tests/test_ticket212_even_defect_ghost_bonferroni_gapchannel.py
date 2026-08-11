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

import ticket212_even_defect_ghost_bonferroni_gapchannel as ticket212


class Ticket212EvenDefectGhostBonferroniGapChannelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket212.build_audit()

    def test_riemann_subtwo_certificate_and_sharp_boundary(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for row in section["configuration_rows"]:
            if row["subtwo_certificate_applies"]:
                self.assertTrue(row["all_zeros_on_line_and_simple"])
        sharp = [
            row
            for row in section["configuration_rows"]
            if row["configuration"] in {
                "one_off_line_pair",
                "one_double_line_zero",
                "ticket211_symmetric_off_line_model_band",
            }
        ]
        self.assertTrue(sharp)
        self.assertTrue(
            all(row["uncertified_defect_N_minus_L"] == 2 for row in sharp)
        )
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_every_collatz_word_has_two_adic_ghost(self) -> None:
        for word in ((1,), (2,), (1, 2), (1, 2, 2), (4, 1, 3, 2)):
            data = ticket212.collatz_word_data(word)
            self.assertTrue(data["ghost_is_two_adic_integer"])
            self.assertTrue(data["prescribed_valuations_replayed"])
            self.assertTrue(data["cycle_closes_exactly"])
            self.assertEqual(data["cycle_numerator_C"] % 2, 1)
            self.assertEqual(data["odd_divisor_D"] % 2, 1)
        family = self.audit["collatz"]["reproducible_computation"][
            "ghost_family_rows"
        ]
        self.assertTrue(all(row["ghost_fixed_point"] == "23/5" for row in family))
        self.assertTrue(all(row["ghost_reduced_denominator"] == 5 for row in family))
        self.assertFalse(
            self.audit["collatz"]["reproducible_computation"]["aggregate"]
            ["collatz_conjecture_resolved"]
        )

    def test_collatz_finite_enumeration_replays_exactly(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "finite_word_enumeration"
        ]
        self.assertEqual([row["words_tested"] for row in rows], [4**n for n in range(1, 9)])
        self.assertTrue(
            all(row["two_adic_ghosts"] == row["above_ticket211_density_floor"] for row in rows)
        )
        self.assertTrue(all(len(row["transcript_sha256"]) == 64 for row in rows))

    def test_goldbach_product_and_bonferroni_identity(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        for row in section["identity_rows"]:
            self.assertEqual(row["bonferroni_upper_bound"], row["closed_form"])
            if row["witness_count_A"] > row["even_truncation_order"]:
                self.assertTrue(row["false_positive"])
        for row in section["finite_target_rows"]:
            self.assertGreater(row["unordered_full_range_witness_count_A"], 0)
            self.assertEqual(row["exact_zero_indicator_product"], 0)
        multiplicity_rows = section["representation_multiplicity_lower_bound_rows"]
        for row in multiplicity_rows:
            pair_count = row["odd_prime_count"] * (row["odd_prime_count"] + 1) // 2
            bins = row["possible_even_sums_6_through_2x"]
            self.assertEqual(row["unordered_odd_prime_pair_count"], pair_count)
            self.assertEqual(
                row["maximum_representation_count_lower_bound"],
                (pair_count + bins - 1) // bins,
            )
        self.assertGreater(
            multiplicity_rows[-1]["maximum_representation_count_lower_bound"],
            multiplicity_rows[0]["maximum_representation_count_lower_bound"],
        )
        self.assertTrue(
            section["aggregate"]["unbounded_representation_multiplicity_from_pnt_proved"]
        )
        self.assertFalse(section["aggregate"]["goldbach_conjecture_resolved"])

    def test_goldbach_sample_counts_replay(self) -> None:
        flags = ticket212.prime_sieve(2_000_000)
        primes = [value for value in range(2, 2_000_001) if flags[value]]
        expected = self.audit["goldbach"]["reproducible_computation"][
            "finite_target_rows"
        ]
        for row in expected:
            self.assertEqual(
                ticket212.goldbach_witness_count(
                    row["even_target_N"], flags, primes
                ),
                row["unordered_full_range_witness_count_A"],
            )

    def test_twin_gap_channel_countermodel_and_finite_rows(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["countermodel_rows"]:
            self.assertEqual(row["gap_2_channel"], 0)
            self.assertGreater(row["finite_gap_aggregate"], 0)
        for row in section["finite_prime_channel_rows"]:
            self.assertTrue(row["gap_two_positive"])
            self.assertGreater(row["bounded_gap_aggregate"], 0)
            self.assertEqual(len(row["transcript_sha256"]), 64)
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        ticket212.write_outputs(self.audit)
        integrated_path = (
            ROOT
            / "data/open-problem/ticket212-even-defect-ghost-bonferroni-gapchannel.json"
        )
        integrated = json.loads(integrated_path.read_text(encoding="utf-8"))
        self.assertEqual(integrated["schema"], ticket212.SCHEMA)
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
