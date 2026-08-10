from __future__ import annotations

import hashlib
import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ticket209_normalized_fourone_covering_factorial as ticket209


class Ticket209NormalizedFourOneCoveringFactorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket209.build_audit()

    def test_completed_xi_absolute_endpoint_envelope_decays(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        previous = math.inf
        for row in section["endpoint_decay_rows"]:
            upper = float(row["completed_xi_endpoint_upper_envelope"])
            self.assertGreater(upper, 0)
            self.assertLess(upper, previous)
            previous = upper
        self.assertLess(previous, 1e-35)
        aggregate = section["aggregate"]
        self.assertTrue(
            aggregate["height_independent_absolute_xi_clearance_refuted"]
        )
        self.assertTrue(aggregate["gamma_normalized_sigma_two_clearance_proved"])
        self.assertFalse(aggregate["central_cofinal_nonvanishing_proved"])
        self.assertFalse(aggregate["riemann_hypothesis_resolved"])

    def test_exactly_four_valuation_one_cycles_are_excluded(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        rows = section["exact_enumeration_rows"]
        self.assertEqual(sum(row["enumerated_word_count"] for row in rows), 2292)
        self.assertTrue(
            all(row["positive_odd_integer_fixed_point_count"] == 0 for row in rows)
        )
        self.assertTrue(
            section["length_at_least_sixteen_exclusion"]["left_exceeds_right"]
        )
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            5,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_four_one_enumeration_independently_replays_every_word(self) -> None:
        total = 0
        for length in range(5, 16):
            maximum = ticket209.total_valuation_upper_bound(length)
            words = ticket209.four_one_words(length, maximum)
            total += len(words)
            for word in words:
                self.assertEqual(word[0], 1)
                self.assertGreaterEqual(word[-1], 2)
                self.assertEqual(word.count(1), 4)
                self.assertLessEqual(sum(word), maximum)
                fixed = ticket209.cycle_fixed_point(word)
                self.assertFalse(
                    fixed is not None
                    and fixed.denominator == 1
                    and fixed.numerator >= 3
                    and fixed.numerator % 2 == 1
                )
        self.assertEqual(total, 2292)

    def test_goldbach_greedy_covering_crt_certificates(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        ratios = []
        for row in section["deterministic_covering_fixture_rows"]:
            target = int(row["canonical_even_target_N"])
            modulus = int(row["modulus_M"])
            bound = row["witness_bound_B"]
            self.assertEqual(target % 2, 0)
            self.assertGreater(target, modulus)
            self.assertLessEqual(target, 2 * modulus)
            self.assertTrue(row["greedy_survivor_bound_holds"])
            self.assertTrue(row["all_prime_witnesses_at_most_B_excluded"])
            self.assertLessEqual(
                Fraction(row["survivor_count"]),
                Fraction(row["greedy_survivor_upper_bound_exact"]),
            )
            survivor_forcing = {
                item["survivor_prime"]: item["forcing_prime"]
                for item in row["survivor_forcing_rows"]
            }
            transcript = []
            odd_witnesses = [
                prime
                for prime in ticket209.primes_through(bound)
                if prime >= 3
            ]
            for witness in odd_witnesses:
                cover_divisor = next(
                    (
                        item["modulus_q"]
                        for item in row["cover_rows"]
                        if witness % item["modulus_q"]
                        == item["selected_residue_r"]
                    ),
                    None,
                )
                divisor = cover_divisor or survivor_forcing[witness]
                source = "cover" if cover_divisor else "survivor"
                complement = target - witness
                proper = complement > divisor and complement % divisor == 0
                self.assertTrue(proper)
                transcript.append(f"{witness},{divisor},{source},{int(proper)}")
            self.assertEqual(
                len(odd_witnesses), row["excluded_witness_certificate_count"]
            )
            self.assertEqual(
                hashlib.sha256("\n".join(transcript).encode("ascii")).hexdigest(),
                row["excluded_witness_certificate_sha256"],
            )
            ratios.append(float(row["observed_B_over_natural_log_N_decimal"]))
        self.assertTrue(all(right > left for left, right in zip(ratios, ratios[1:])))
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["superlogarithmic_least_witness_sequence_proved"])
        self.assertTrue(aggregate["least_witness_over_log_limsup_is_infinite"])
        self.assertFalse(aggregate["goldbach_counterexample_found"])
        self.assertFalse(aggregate["goldbach_conjecture_resolved"])

    def test_factorial_intervals_force_exact_cyclotomic_cancellation(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["factorial_twin_free_rows"]:
            self.assertEqual(row["candidate_count"], row["requested_length_H"])
            self.assertEqual(row["exact_twin_count_T_I"], 0)
            self.assertEqual(
                row["all_nonzero_modes_raw_aggregate_R_I"],
                -row["requested_length_H"],
            )
            self.assertTrue(row["all_composite_pair_certificates_hold"])
            self.assertTrue(row["exact_identity_M2T_equals_H_plus_R"])
            for certificate in row["certificate_rows"]:
                self.assertTrue(certificate["lower_divisible"])
                self.assertTrue(certificate["upper_divisible"])
                self.assertTrue(certificate["both_proper_composites"])
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["arbitrarily_long_twin_free_intervals_proved"])
        self.assertTrue(aggregate["positive_margin_on_every_interval_refuted"])
        self.assertFalse(aggregate["cofinal_dyadic_positive_remainder_proved"])
        self.assertFalse(aggregate["twin_prime_conjecture_resolved"])

    def test_machine_contract_keeps_all_conjectures_open(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            nodes = self.audit[key]["proof_dag"]["nodes"]
            self.assertEqual(sum(node["status"] == "highest_risk_open" for node in nodes), 1)
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

    def test_written_outputs_match_attempt_contract(self) -> None:
        ticket209.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket209-normalized-fourone-covering-factorial.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], ticket209.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in payload["attempts"]},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        self.assertTrue(
            all(
                attempt["bounded_result"]["audit_ref"]
                == "#/normalized_fourone_covering_factorial_audit"
                for attempt in payload["attempts"]
            )
        )


if __name__ == "__main__":
    unittest.main()
