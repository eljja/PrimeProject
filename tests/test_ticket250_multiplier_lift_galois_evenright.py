from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.ticket250_multiplier_lift_galois_evenright import (
    AUDIT_KEY,
    SCHEMA,
    bareiss_determinant,
    build_audit,
    cyclotomic_prime_norm,
    fermat_quotient_residue,
    lifted_fermat_quotient,
    normalized_legendre_x2_expectation,
)


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_NODE_STATUSES = {
    "proved",
    "disproved",
    "computed_finite",
    "external_theorem",
    "assumption",
    "heuristic",
    "open",
}


class Ticket250MultiplierLiftGaloisEvenRightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit()
        cls.root = cls.audit[AUDIT_KEY]

    def test_machine_boundary_and_classifications(self) -> None:
        self.assertEqual(self.audit["schema"], SCHEMA)
        self.assertTrue(self.audit["iteration_complete"])
        self.assertFalse(self.audit["program_complete"])
        machine = self.root["machine_audit"]
        self.assertEqual(machine["exact_theorem_count"], 4)
        self.assertEqual(machine["new_partial_theorem_count"], 2)
        self.assertEqual(machine["exact_no_go_count"], 2)
        self.assertEqual(machine["conjecture_resolution_count"], 0)
        self.assertEqual(machine["candidate_resolution_count"], 0)
        self.assertEqual(machine["deep_focus_problem"], "goldbach")
        self.assertEqual(machine["total_failure_count"], 0)
        self.assertEqual(
            [
                self.root[key]["result_classification"]
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            ],
            ["exact_no_go", "exact_no_go", "partial_theorem", "partial_theorem"],
        )
        self.assertTrue(
            all(
                self.root[key]["problem_status"] == "open_not_proven"
                for key in ("riemann", "collatz", "goldbach", "twin_prime")
            )
        )

    def test_riemann_multiplier_and_concentration_escapes(self) -> None:
        computation = self.root["riemann"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "20099dd1cab1cbcfa5ef4863e9f3c115c9f59af2da902d05bdbe029b5a8c507b",
        )
        self.assertEqual(normalized_legendre_x2_expectation(2), Fraction(11, 21))
        rows = computation["exact_legendre_multiplier_rows"]
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertEqual(rows[-1]["exact_distance_from_one_half"]["exact"], "1/2101242")
        concentration = computation["exact_concentration_escape_rows"]
        self.assertEqual(len(concentration), 12)
        bounds = [Fraction(row["proved_combined_upper_bound"]["exact"]) for row in concentration]
        self.assertTrue(all(right < left for left, right in zip(bounds, bounds[1:])))
        self.assertTrue(
            computation["aggregate"]["legendre_only_noncompact_coercivity_route_refuted"]
        )
        self.assertFalse(computation["aggregate"]["actual_weil_form_controlled"])

    def test_collatz_affine_lift_transitivity(self) -> None:
        computation = self.root["collatz"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "08ee2ee2080e127c58f7120621b39d20213ce2f6cf71987aaf01c7099ad528c2",
        )
        rows = computation["exact_lift_field_rows"]
        self.assertEqual(sum(row["lift_pairs_checked"] for row in rows), 73_901)
        for row in rows:
            q = row["prime_q"]
            self.assertEqual(row["fermat_coordinate_pairs_reached"], q * q)
            self.assertEqual(row["separated_projective_lift_pairs"], q - 1)
            self.assertTrue(row["certificate_verified"])
            u0 = fermat_quotient_residue(2, q)
            for k in (0, 1, q - 1):
                self.assertEqual(
                    lifted_fermat_quotient(2, k, q),
                    (u0 - k * pow(2, -1, q)) % q,
                )
        self.assertTrue(
            computation["aggregate"]["lift_invariant_local_avoidance_route_refuted"]
        )
        self.assertFalse(
            computation["aggregate"]["canonical_fixed_representative_occurrence_decided"]
        )

    def test_goldbach_galois_norm_and_boundary_models(self) -> None:
        computation = self.root["goldbach"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "684fea0b7645dea69f080eddb985918605ef6db23fde35646689556c8cf5c5a1",
        )
        self.assertEqual(bareiss_determinant([[2, 1], [1, 2]]), 3)
        self.assertEqual(cyclotomic_prime_norm([2, -1, -1]), 9)
        self.assertEqual(cyclotomic_prime_norm([4, -1, -1, -1, -1]), 625)
        rows = computation["exact_prime_count_norm_rows"]
        self.assertEqual(len(rows), 35)
        self.assertTrue(all(row["certificate_verified"] for row in rows))
        self.assertTrue(all(int(row["exact_galois_norm"]) != 0 for row in rows))
        self.assertEqual(
            computation["aggregate"]["smallest_replayed_absolute_norm"], "250000"
        )
        boundaries = computation["exact_boundary_countermodels"]
        self.assertEqual(
            [(row["modulus_q"], row["nonzero_frequency_support"]) for row in boundaries],
            [(3, [1, 2]), (4, [1, 3])],
        )
        self.assertFalse(
            computation["aggregate"]["quantitative_pointwise_upper_anti_concentration_proved"]
        )

    def test_twin_all_base_even_left_classification(self) -> None:
        computation = self.root["twin_prime"]["reproducible_computation"]
        self.assertEqual(
            computation["transcript_sha256"],
            "0cf8bd40771dca2cc7e0da725f6bffbaefb50d81c3d73d72731917568fa4dcda",
        )
        rows = computation["exact_scale_rows"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[0]["right_active_even_left_exponent"], 0)
        self.assertEqual(rows[1]["right_active_even_left_exponent"], 1)
        last = rows[-1]
        self.assertEqual(last["right_active_composite_pairs_R"], 136)
        self.assertEqual(last["right_active_even_left_exponent"], 1)
        self.assertEqual(last["right_active_odd_left_exponent"], 135)
        self.assertEqual(
            [
                (row["n"], row["n_plus_2"])
                for row in computation["selected_even_left_witnesses"]
            ],
            [(25, 27)],
        )
        self.assertTrue(
            computation["aggregate"]["base_three_left_exception_eliminated"]
        )
        self.assertFalse(
            computation["aggregate"]["odd_left_right_active_contamination_controlled"]
        )

    def test_proof_dags_are_acyclic_with_one_open_frontier(self) -> None:
        for key in ("riemann", "collatz", "goldbach", "twin_prime"):
            dag = self.root[key]["proof_dag"]
            nodes = dag["nodes"]
            ids = {node["id"] for node in nodes}
            self.assertEqual(len(ids), len(nodes))
            self.assertTrue(all(node["status"] in ALLOWED_NODE_STATUSES for node in nodes))
            self.assertEqual(sum(node["status"] == "open" for node in nodes), 1)
            adjacency = {node_id: [] for node_id in ids}
            indegree = {node_id: 0 for node_id in ids}
            for source, target in dag["edges"]:
                self.assertIn(source, ids)
                self.assertIn(target, ids)
                adjacency[source].append(target)
                indegree[target] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                current = queue.pop()
                visited += 1
                for successor in adjacency[current]:
                    indegree[successor] -= 1
                    if indegree[successor] == 0:
                        queue.append(successor)
            self.assertEqual(visited, len(nodes))

    def test_committed_integrated_json_matches_generator(self) -> None:
        path = ROOT / "data/open-problem/ticket250-multiplier-lift-galois-evenright.json"
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_audit())

    def test_persistent_state_preserves_ticket250_history(self) -> None:
        state = json.loads(
            (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(state["ticket"], 250)
        self.assertEqual(state["parent_ticket"], state["ticket"] - 1)
        self.assertEqual(state["resolved_count"], 0)
        self.assertEqual(state["candidate_resolution_count"], 0)
        self.assertFalse(state["program_complete"])
        if state["ticket"] == 250:
            self.assertEqual(state["deep_focus_problem"], "goldbach")
        historical = {
            "riemann": "NoncompactMultiplierLegendreEscapeInsufficiencyNoGo",
            "collatz": "LocalFermatQuotientLiftTransitivityNoGo",
            "goldbach": "PrimeModulusRationalFourierFullSupportAndNormBarrier",
            "twin_prime": "AllBaseEvenLeftRightActiveClassification",
        }
        for problem_key, theorem in historical.items():
            self.assertIn(theorem, state["problems"][problem_key]["established_results"])
        self.assertTrue(
            all(problem["stagnation_count"] == 0 for problem in state["problems"].values())
        )


if __name__ == "__main__":
    unittest.main()
