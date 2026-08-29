function renderTicket254DiagonalWeightedReflectionThue(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.diagonal_weighted_reflection_thue_audit || {};
  const section = ({
    riemann: audit.riemann,
    collatz: audit.collatz,
    goldbach: audit.goldbach,
    "twin-prime": audit.twin_prime,
  })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const rows = computation.exact_block_operator_rows || [];
    detail = [
      '<div class="poc-equation">On the L=2N+1 packet block, A<sub>N</sub>=L/(L-1)I-J/(L-1) is positive with every Fourier diagonal equal to 1, yet the normalized all-ones Dirichlet packet has energy 0. Positive diagonal data alone cannot prove packet domination.</div>',
      table(["N", "L", "diagonal", "off diagonal", "packet energy", "other eigenvalue", "verified"], rows.map((row) => [
        row.dirichlet_half_bandwidth_N,
        row.block_dimension_L,
        row.fourier_diagonal?.exact,
        row.common_off_diagonal?.exact,
        row.dirichlet_packet_energy?.exact,
        row.orthogonal_complement_eigenvalue?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Diagonal = 1</span><strong>' + (aggregate.every_fourier_diagonal_equals_one ? "proved" : "open") + '</strong></div><div><span>Diagonal-only route</span><strong>' + (aggregate.diagonal_only_domination_route_rejected ? "rejected" : "open") + '</strong></div><div><span>Actual Weil form</span><strong>' + (aggregate.actual_weil_form_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_nonnegative_weighted_rows || [];
    detail = [
      '<div class="poc-equation">Complete additive-character orthogonality turns every normalized detector into an exact incidence indicator. Any finite nonnegative cross-prime weighting is therefore the same weighted incidence count and has no cancellation.</div>',
      table(["scenario", "weight", "detector sum", "incidence sum", "verified"], rows.map((row) => [
        row.scenario,
        row.nonnegative_weight_family,
        row.weighted_complete_detector_sum?.exact,
        row.weighted_incidence_sum?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>Pointwise replay:</strong> ' + formatter.format((computation.exact_detector_rows || []).length) + ' exact detector rows across canonical, hit, miss, and origin scenarios.</p>',
      '<div class="poc-head"><div><span>Weighted identity</span><strong>' + (aggregate.all_nonnegative_weighted_complete_averages_equal_incidence ? "proved" : "open") + '</strong></div><div><span>Nonnegative average route</span><strong>' + (aggregate.cross_prime_complete_detector_cancellation_route_rejected ? "rejected" : "open") + '</strong></div><div><span>Signed incomplete route</span><strong>' + (aggregate.signed_incomplete_character_route_rejected ? "rejected" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_even_reflection_exclusion_rows || [];
    detail = [
      '<div class="poc-equation">For even m with q not dividing m, cyclic reflection forces c<sub>m mod q</sub>=c<sub>0</sub>, so the compatible tail demands exactly one prime in that nonzero residue. Once the forced prefix reaches its second residue prime, the unique-prefix criterion excludes it.</div>',
      table(["q", "m", "r=m mod q", "T", "second prime", "global index", "forced count", "excluded", "verified"], rows.map((row) => [
        row.prime_modulus_q,
        row.even_cyclotomic_exponent_m,
        row.reflected_nonzero_residue_m_mod_q,
        String(row.forced_total_prime_count_T),
        row.second_prime_in_reflected_residue,
        row.global_index_of_second_residue_prime,
        row.forced_count_at_reflected_residue,
        row.unique_prime_prefix_excluded ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>First certificate:</strong> (q,m)=(5,8), r=3, T=280; the second prime 13 occurs at global prime index 6. Huge prefixes are not enumerated.</p>',
      '<div class="poc-head"><div><span>Reflection identity</span><strong>' + (aggregate.even_reflection_identity_proved ? "proved" : "open") + '</strong></div><div><span>Selected compatible pairs</span><strong>' + formatter.format(aggregate.compatible_non_q_divisible_even_pair_count || 0) + ' excluded</strong></div><div><span>Odd or q-divisible tails</span><strong>' + (aggregate.odd_or_q_divisible_compatible_tails_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_unit_twisted_thue_polynomials || [];
    const finiteBox = computation.finite_box_audit || {};
    detail = [
      '<div class="poc-equation">In Z[sqrt(2)], x²-2=y<sup>17</sup> is equivalent to one of 17 unit-twisted coefficient-one equations B<sub>j</sub>(u,v)=1 with A<sub>j</sub>&gt;0 and (-1)<sup>j</sup>(u²-2v²)&gt;0. This is an exact finite Thue reduction, not a solution of those equations.</div>',
      table(["j", "unit rational part", "unit sqrt(2) part", "A coefficients", "B coefficients"], rows.map((row) => [
        row.unit_twist_j,
        row.unit_rational_part_a_j,
        row.unit_sqrt2_part_b_j,
        (row.A_j_coefficients_for_u_power_17_minus_k_v_power_k || []).length,
        (row.B_j_coefficients_for_u_power_17_minus_k_v_power_k || []).length,
      ])),
      '<p><strong>Exact finite-box audit:</strong> radius ' + formatter.format(finiteBox.coordinate_radius || 0) + '; ' + formatter.format(finiteBox.exact_grid_case_count || 0) + ' twist-points; ' + formatter.format(finiteBox.coefficient_one_point_count || 0) + ' coefficient-one points; ' + formatter.format(finiteBox.admissible_positive_point_count || 0) + ' admissible positive points. This bounded search has no global force.</p>',
      '<div class="poc-head"><div><span>17-equation equivalence</span><strong>' + (aggregate.coefficient_one_thue_equivalence_proved ? "proved" : "open") + '</strong></div><div><span>Unit twists</span><strong>' + formatter.format(aggregate.unit_twist_count || 0) + '</strong></div><div><span>All Thue equations</span><strong>' + (aggregate.all_seventeen_thue_equations_solved ? "solved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket254-diagonal-weighted-reflection-thue" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-254 positive diagonal, weighted detector, even reflection, and exponent-17 Thue reduction</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-gos; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table">' + table(["TICKET254 audit", "Value"], [
      ["ticket", attempt.ticket_id || "missing"],
      ["classification / 분류", section.result_classification || attempt.result_classification || "missing"],
      ["exact theorem / 정확한 정리", section.theorem_name || attempt.new_result || "missing"],
      ["declared proposition / 선언 명제", section.declared_proposition || attempt.declared_proposition || "missing"],
      ["stagnation / 정체", section.stagnation_count ?? attempt.stagnation_count ?? "missing"],
      ["next theorem / 다음 정리", attempt.candidate_theorem || "missing"],
    ]) + '</div>',
    detail,
    '<h3>Proof DAG / 증명 의존성</h3>',
    table(["node", "theorem", "status"], (dag.nodes || []).map((node) => [node.id, node.label, node.status])),
    table(["from", "to"], (dag.edges || []).map((edge) => edge)),
    '<div class="poc-route-decision"><section><span>DISCARD / 폐기</span><strong>' + escapeHtml(section.route_decision?.discard || attempt.discarded_route || "") + '</strong></section><section><span>KEEP / 유지</span><strong>' + escapeHtml(section.route_decision?.retain || "") + '</strong></section></div>',
    '<div class="poc-bridge"><section><h3>Established / 확립</h3><p>' + escapeHtml(section.mathematical_argument || computation.proof || "") + '</p></section><section><h3>Finite boundary / 유한 계산 한계</h3><p>' + escapeHtml(section.finite_computation_boundary || "") + '</p><h3>Remaining proof gap / 남은 증명 간극</h3><p>' + escapeHtml(section.logical_limit || attempt.remaining_gap || "") + '</p><p><strong>Next:</strong> ' + escapeHtml(attempt.candidate_theorem || "") + '</p></section></div>',
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-254 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/diagonal-weighted-reflection-thue.ko.md">한국어 보고서</a> · <a href="../docs/diagonal-weighted-reflection-thue.md">English report</a> · <a href="../data/open-problem/ticket254-diagonal-weighted-reflection-thue.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
