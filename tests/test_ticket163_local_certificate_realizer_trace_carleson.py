from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ticket163_local_certificate_realizer_trace_carleson import (  # noqa: E402
    SCHEMA,
    STATUS,
    build_attempts,
    build_audit,
    collatz_affine_correction,
    collatz_least_realizer,
    collatz_replay,
    dyadic_descendant_energy,
    positive_compositions,
    region_variance,
)


class Ticket163LocalCertificateRealizerTraceCarlesonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket163-local-certificate-realizer-trace-carleson.json"
            ).read_text(encoding="utf-8")
        )

    def test_machine_contract_has_no_failures_or_resolutions(self) -> None:
        machine = self.audit["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["rejected_target_count"], 4)
        self.assertEqual(machine["proof_dag_count"], 4)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["total_failure_count"], 0)

    def test_global_payload_contract(self) -> None:
        self.assertEqual(self.payload["schema"], SCHEMA)
        self.assertEqual(self.payload["status"], STATUS)
        self.assertIn("resolves none", self.payload["claim_boundary"])

    def test_riemann_finite_trace_constants_are_finite_and_growing(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        rows = computation["finite_prime_trace_rows"]
        self.assertEqual(
            [row["prime_power_cutoff_X"] for row in rows],
            [100, 1_000, 10_000, 100_000, 1_000_000],
        )
        self.assertTrue(all(all(row["checks"].values()) for row in rows))
        self.assertTrue(all(computation["trend_checks"].values()))

    def test_collatz_adjacent_swap_identity(self) -> None:
        left = (2, 5, 1, 3)
        right = (5, 2, 1, 3)
        expected = 3 ** (4 - 0 - 2) * (2**5 - 2**2)
        self.assertEqual(
            collatz_affine_correction(right)
            - collatz_affine_correction(left),
            expected,
        )

    def test_collatz_natural_realizer_replays_word(self) -> None:
        word = (4, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 3)
        residue, endpoint, margin = collatz_least_realizer(word)
        self.assertEqual((residue, endpoint, margin), (165, 167, -2))
        self.assertEqual(collatz_replay(residue, len(word)), (word, endpoint))

    def test_collatz_fixed_length_transfer_is_refuted_exactly(self) -> None:
        no_go = self.audit["collatz"]["reproducible_computation"][
            "exact_natural_realizer_coupling_no_go"
        ]
        self.assertGreater(
            no_go["front_loaded"]["correction"],
            no_go["smaller_correction"]["correction"],
        )
        self.assertGreater(no_go["front_loaded"]["margin"], 0)
        self.assertLess(no_go["smaller_correction"]["margin"], 0)
        self.assertTrue(all(no_go["checks"].values()))

    def test_collatz_complete_minimal_layers_are_exactly_counted(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "minimal_layer_complete_rows"
        ]
        self.assertEqual([row["word_length_m"] for row in rows], list(range(2, 14)))
        self.assertEqual(rows[0]["non_strict_count"], 1)
        self.assertTrue(all(row["non_strict_count"] == 0 for row in rows[1:]))
        self.assertTrue(
            all(row["natural_residue_replay_failure_count"] == 0 for row in rows)
        )
        self.assertEqual(len(list(positive_compositions(8, 5))), 35)

    def test_goldbach_shell_certificate_does_not_pass_finite_mask(self) -> None:
        rows = self.audit["goldbach"]["reproducible_computation"][
            "finite_prime_dft_dyadic_shell_rows"
        ]
        self.assertEqual(rows[-1]["dyadic_upper_inclusive"], 65_536)
        self.assertTrue(
            all(
                row["normalized_negative_budget"] >= 1
                and not row["unit_gate_passes"]
                and row["observed_zero_count"] == 0
                and row["fft_positivity_mismatch_count"] == 0
                and all(row["checks"].values())
                for row in rows
            )
        )

    def test_goldbach_diluted_spike_refutes_mean_route(self) -> None:
        computation = self.audit["goldbach"]["reproducible_computation"]
        rows = computation["exact_diluted_unit_spike_rows"]
        self.assertTrue(all(row["normalized_budget"] == 1 for row in rows))
        self.assertGreater(
            rows[0]["mean_normalized_budget"], rows[-1]["mean_normalized_budget"]
        )
        self.assertTrue(all(computation["spike_checks"].values()))

    def test_twin_local_variance_telescopes_exactly(self) -> None:
        matrix = [
            [1, -1, 1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1],
            [-1, 1, -1, 1],
        ]
        self.assertEqual(region_variance(matrix, 0, 0, 4), Fraction(16))
        self.assertEqual(dyadic_descendant_energy(matrix, 0, 0, 4), Fraction(16))

    def test_twin_global_dilution_keeps_local_energy(self) -> None:
        computation = self.audit["twin_prime"]["reproducible_computation"]
        rows = computation["embedded_checkerboard_dilution_rows"]
        self.assertEqual(rows[0]["global_energy_density"], 0.25)
        self.assertEqual(rows[-1]["global_energy_density"], 1 / 1024)
        self.assertTrue(
            all(row["local_four_by_four_energy_density"] == 1 for row in rows)
        )
        self.assertTrue(all(computation["dilution_checks"].values()))

    def test_each_proof_dag_ends_open(self) -> None:
        for key in ["riemann", "collatz", "goldbach", "twin_prime"]:
            nodes = self.audit[key]["proof_dag"]["nodes"]
            self.assertEqual(
                [node["status"] for node in nodes],
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_attempts_have_one_next_lemma_each(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual(len(attempts), 4)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        self.assertTrue(all(attempt["candidate_theorem"] for attempt in attempts))

    def test_per_problem_json_contracts(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-163-prime-trace-continuity.json",
            "collatz": "collatz/co-ticket-163-rearrangement-realizer-coupling.json",
            "goldbach": "goldbach/gb-ticket-163-dyadic-integral-budget.json",
            "twin-prime": "twin-prime/tp-ticket-163-local-carleson-dilution.json",
        }
        for problem_id, relative in paths.items():
            payload = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema"], SCHEMA)
            self.assertEqual(payload["problem_id"], problem_id)
            self.assertEqual(payload["status"], "open_not_proven")
            self.assertIn("No ", payload["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
