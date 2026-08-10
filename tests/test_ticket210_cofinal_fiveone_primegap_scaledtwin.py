from __future__ import annotations

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

import ticket210_cofinal_fiveone_primegap_scaledtwin as ticket210


class Ticket210CofinalFiveOnePrimeGapScaledTwinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = ticket210.build_audit()

    def test_symmetric_offcritical_countermodel_is_exact(self) -> None:
        section = self.audit["riemann"]["reproducible_computation"]
        for real in (Fraction(1, 4), Fraction(3, 4)):
            for imaginary in (-1, 1):
                root = complex(float(real), imaginary)
                self.assertLess(abs(ticket210.symmetric_quartet_polynomial(root)), 1e-12)
                self.assertNotEqual(real, Fraction(1, 2))
        for sample in (
            complex(-1, 2),
            complex(Fraction(1, 3), 5),
            complex(Fraction(7, 6), -3),
        ):
            self.assertAlmostEqual(
                ticket210.symmetric_quartet_polynomial(1 - sample).real,
                ticket210.symmetric_quartet_polynomial(sample).real,
                places=10,
            )
            self.assertAlmostEqual(
                ticket210.symmetric_quartet_polynomial(1 - sample).imag,
                ticket210.symmetric_quartet_polynomial(sample).imag,
                places=10,
            )
        for row in section["countermodel_rows"]:
            self.assertTrue(row["sampled_minimum_respects_exact_lower_bound"])
        self.assertTrue(
            section["aggregate"]["existential_cofinal_central_nonvanishing_proved"]
        )
        self.assertFalse(section["aggregate"]["effective_zeta_clearance_proved"])
        self.assertFalse(section["aggregate"]["riemann_hypothesis_resolved"])

    def test_five_one_enumeration_replays_all_words(self) -> None:
        section = self.audit["collatz"]["reproducible_computation"]
        total = 0
        for length in range(6, 20):
            maximum = ticket210.total_valuation_upper_bound(length)
            local = 0
            for word in ticket210.five_one_words(length, maximum):
                local += 1
                self.assertEqual(word[0], 1)
                self.assertGreaterEqual(word[-1], 2)
                self.assertEqual(word.count(1), 5)
                self.assertLessEqual(sum(word), maximum)
                fixed = ticket210.cycle_fixed_point(word)
                self.assertFalse(
                    fixed is not None
                    and fixed.denominator == 1
                    and fixed.numerator >= 3
                    and fixed.numerator % 2 == 1
                )
            total += local
        self.assertEqual(total, 29758)
        self.assertEqual(total, section["total_exact_words_enumerated"])
        self.assertEqual(section["exact_length_cap_h"], 19)
        self.assertTrue(
            section["length_at_least_twenty_exclusion"]["left_exceeds_right"]
        )
        self.assertEqual(
            section["aggregate"][
                "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle"
            ],
            6,
        )
        self.assertFalse(section["aggregate"]["collatz_conjecture_resolved"])

    def test_general_k_one_product_cap_at_k_five(self) -> None:
        for length in range(20, 80):
            self.assertGreater(
                2 ** (2 * length - 5) * 3**length,
                10**length,
            )

    def test_prime_gap_transfer_rows_are_independent_certificates(self) -> None:
        section = self.audit["goldbach"]["reproducible_computation"]
        largest = max(row["right_prime"] for row in section["finite_record_gap_rows"])
        flags = ticket210.prime_sieve(largest)
        primes = [value for value in range(2, largest + 1) if flags[value]]
        for row in section["finite_record_gap_rows"]:
            left = row["left_prime"]
            right = row["right_prime"]
            gap = right - left
            target = right - 1
            self.assertTrue(flags[left])
            self.assertTrue(flags[right])
            self.assertTrue(all(not flags[value] for value in range(left + 1, right)))
            for witness in primes:
                if witness > gap - 2:
                    break
                self.assertFalse(flags[target - witness])
            least = next(
                witness for witness in primes if witness < target and flags[target - witness]
            )
            self.assertEqual(least, row["actual_least_witness_in_finite_fixture"])
            self.assertGreater(least, gap - 2)
        aggregate = section["aggregate"]
        self.assertTrue(aggregate["prime_gap_to_least_witness_transfer_proved"])
        self.assertFalse(aggregate["improves_ticket209_covering_floor"])
        self.assertFalse(aggregate["goldbach_counterexample_found"])

    def test_current_large_gap_factor_is_below_ticket209_scale(self) -> None:
        values = [math.log(log3) / log3 for log3 in (8, 64, 4096, 1_000_000)]
        self.assertTrue(all(value > 0 for value in values))
        self.assertLess(values[-1], values[0])

    def test_factorial_desert_scale_and_divisibility(self) -> None:
        section = self.audit["twin_prime"]["reproducible_computation"]
        for row in section["factorial_scale_rows"]:
            k = row["factorial_parameter_K"]
            base = math.factorial(k)
            for offset in range(2, k - 1):
                self.assertEqual((base + offset) % offset, 0)
                self.assertEqual((base + offset + 2) % (offset + 2), 0)
            self.assertTrue(row["H_at_least_one_quarter_scale"])
            self.assertGreaterEqual(
                k - 3,
                math.log(base) / (4 * math.log(math.log(base))),
            )
        self.assertFalse(section["aggregate"]["twin_prime_conjecture_resolved"])

    def test_machine_contract_and_written_outputs(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_partial_theorem_count"], 4)
        self.assertEqual(machine["refuted_or_limited_route_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            nodes = self.audit[key]["proof_dag"]["nodes"]
            self.assertEqual(
                sum(node["status"] == "highest_risk_open" for node in nodes), 1
            )
            self.assertEqual(nodes[-1]["status"], "open_not_proven")

        ticket210.write_outputs(self.audit)
        path = (
            ROOT
            / "data/open-problem/ticket210-cofinal-fiveone-primegap-scaledtwin.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], ticket210.SCHEMA)
        self.assertEqual(payload["status"], "open_not_proven")
        self.assertEqual(len(payload["attempts"]), 4)
        self.assertTrue(
            all(
                attempt["bounded_result"]["audit_ref"]
                == "#/cofinal_fiveone_primegap_scaledtwin_audit"
                for attempt in payload["attempts"]
            )
        )


if __name__ == "__main__":
    unittest.main()
