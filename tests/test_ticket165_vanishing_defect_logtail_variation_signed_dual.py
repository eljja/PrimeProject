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

from ticket165_vanishing_defect_logtail_variation_signed_dual import (  # noqa: E402
    SCHEMA,
    STATUS,
    affine_correction,
    build_attempts,
    build_audit,
    critical_prefix_sums,
    first_automatic_excess,
    sparse_anchor_variation_bound,
)


class Ticket165VanishingDefectLogTailVariationSignedDualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.payload = json.loads(
            (
                ROOT
                / "data"
                / "open-problem"
                / "ticket165-vanishing-defect-logtail-variation-signed-dual.json"
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

    def test_riemann_path_laplacian_rayleigh_formula_is_exact(self) -> None:
        rows = self.audit["riemann"]["reproducible_computation"][
            "path_laplacian_no_uniform_gap_rows"
        ]
        self.assertEqual([row["dimension"] for row in rows], [4, 8, 16, 32, 64, 128])
        for row in rows:
            dimension = row["dimension"]
            self.assertEqual(
                Fraction(row["rayleigh_upper_bound_for_core_minimum"]["exact"]),
                Fraction(12, dimension * (dimension + 1)),
            )
            self.assertTrue(all(row["checks"].values()))

    def test_riemann_positive_finite_cores_have_no_uniform_gap(self) -> None:
        computation = self.audit["riemann"]["reproducible_computation"]
        rows = computation["path_laplacian_no_uniform_gap_rows"]
        ratios = [
            Fraction(row["rayleigh_upper_bound_for_core_minimum"]["exact"])
            for row in rows
        ]
        self.assertTrue(all(left > right for left, right in zip(ratios, ratios[1:])))
        self.assertLess(ratios[-1], Fraction(1, 1000))
        self.assertTrue(all(computation["global_checks"].values()))

    def test_collatz_logarithmic_tail_threshold_is_minimal(self) -> None:
        for length in [8, 16, 32, 64, 128, 256, 512, 1024]:
            threshold = first_automatic_excess(length)
            self.assertGreater(9 * ((1 << threshold) - 1), length)
            self.assertLessEqual(9 * ((1 << (threshold - 1)) - 1), length)

    def test_collatz_critical_word_is_first_crossing(self) -> None:
        length = 127
        final_excess = 2
        sums = critical_prefix_sums(length, final_excess)
        word = [sums[index] - sums[index - 1] for index in range(1, len(sums))]
        correction, total = affine_correction(word)
        self.assertTrue(all((1 << sums[index]) <= 3**index for index in range(1, length)))
        self.assertGreater(1 << total, 3**length)
        self.assertGreater(correction, 0)

    def test_collatz_constant_excess_envelope_no_go_is_exact(self) -> None:
        rows = self.audit["collatz"]["reproducible_computation"][
            "fixed_excess_envelope_no_go_rows"
        ]
        self.assertEqual([row["fixed_final_excess"] for row in rows], list(range(6)))
        self.assertEqual([row["constructed_word_length"] for row in rows], [19, 55, 127, 271, 559, 1135])
        self.assertTrue(all(row["automatic_n3_margin_sign"] == -1 for row in rows))
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_goldbach_sparse_anchor_bound_is_deterministic(self) -> None:
        values = [0.1, 0.2, 0.3, 0.2, 0.1]
        row = sparse_anchor_variation_bound(values, 4)
        self.assertAlmostEqual(row["maximum_anchor_deficit"], 0.1)
        self.assertAlmostEqual(row["maximum_segment_path_variation"], 0.2)
        self.assertAlmostEqual(row["certified_pointwise_upper_bound"], 0.3)
        self.assertTrue(row["pointwise_unit_gate_certified"])

    def test_goldbach_finite_net_dominates_every_deficit(self) -> None:
        shell = self.audit["goldbach"]["reproducible_computation"]["finite_shell"]
        self.assertEqual(shell["dyadic_upper_inclusive"], 65_536)
        self.assertLess(shell["actual_maximum_deficit"], 1)
        self.assertTrue(all(all(row["checks"].values()) for row in shell["net_rows"]))
        by_stride = {row["anchor_stride_in_even_targets"]: row for row in shell["net_rows"]}
        self.assertTrue(by_stride[16]["pointwise_unit_gate_certified"])
        self.assertFalse(by_stride[32]["pointwise_unit_gate_certified"])

    def test_goldbach_finite_p_moment_spike_retains_exception(self) -> None:
        no_go = self.audit["goldbach"]["reproducible_computation"]["finite_p_spike_no_go"]
        rows = no_go["rows"]
        self.assertTrue(all(row["exception_count"] == 1 for row in rows))
        self.assertTrue(all(row["maximum_deficit"] == 1 for row in rows))
        self.assertEqual(rows[-1]["moments"]["4"]["normalized_pth_moment"]["exact"], "1/2048")
        self.assertTrue(all(no_go["checks"].values()))

    def test_twin_unsigned_energy_cannot_determine_signed_pairing(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "signed_dual_sharpness_rows"
        ]
        self.assertEqual([row["dimension"] for row in rows], [8, 16, 32, 64, 128])
        self.assertTrue(all(row["positive_signed_pairing"]["exact"] == "1/1" for row in rows))
        self.assertTrue(all(row["negative_signed_pairing"]["exact"] == "-1/1" for row in rows))
        self.assertTrue(all(row["positive_model_count"]["exact"] == "2/1" for row in rows))
        self.assertTrue(all(row["zero_model_count"]["exact"] == "0/1" for row in rows))
        self.assertTrue(all(all(row["checks"].values()) for row in rows))

    def test_twin_signed_dual_budget_is_sharp(self) -> None:
        rows = self.audit["twin_prime"]["reproducible_computation"][
            "signed_dual_sharpness_rows"
        ]
        self.assertTrue(all(row["cauchy_budget_squared"]["exact"] == "1/1" for row in rows))
        self.assertEqual(rows[-1]["primal_product_haar_energy"], 128)

    def test_attempts_and_proof_dags_remain_open(self) -> None:
        attempts = build_attempts(self.audit)
        self.assertEqual(
            {attempt["problem_id"] for attempt in attempts},
            {"riemann", "collatz", "goldbach", "twin-prime"},
        )
        for attempt in attempts:
            self.assertEqual(attempt["status"], "open_not_proven")
            self.assertEqual(
                [node["status"] for node in attempt["proof_dag"]["nodes"]],
                ["refuted_or_insufficient", "proved_exact", "open_not_proven"],
            )

    def test_per_problem_artifacts_match_global_sections(self) -> None:
        paths = {
            "riemann": "riemann/rh-ticket-165-vanishing-defect.json",
            "collatz": "collatz/co-ticket-165-logarithmic-excess.json",
            "goldbach": "goldbach/gb-ticket-165-anchor-variation.json",
            "twin-prime": "twin-prime/tp-ticket-165-signed-dual.json",
        }
        attempts = {row["problem_id"]: row for row in self.payload["attempts"]}
        for problem_id, relative in paths.items():
            artifact = json.loads(
                (ROOT / "data" / "open-problem" / relative).read_text(encoding="utf-8")
            )
            self.assertEqual(artifact["schema"], SCHEMA)
            self.assertEqual(artifact["status"], "open_not_proven")
            self.assertEqual(artifact["theorem_name"], attempts[problem_id]["new_result"])
            self.assertEqual(artifact["candidate_theorem"], attempts[problem_id]["candidate_theorem"])


if __name__ == "__main__":
    unittest.main()
