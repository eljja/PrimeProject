function renderTicket256CesaroKernelQDivGL2(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.cesaro_kernel_qdiv_gl2_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const rows = computation.exact_packet_cesaro_rows || [];
    detail = [
      '<div class="poc-equation">For every real Toeplitz lag sequence, E<sub>L</sub>=L<sup>-1</sup>Σ<sub>n&lt;L</sub>S<sub>n</sub>. Nonnegative lag partial sums are sufficient, but (1,-1,1,0,...) proves they are not necessary.</div>',
      table(["L", "min S_n", "packet energy", "all S_n≥0", "verified"], rows.map((row) => [row.packet_dimension_L, row.minimum_partial_sum?.exact, row.normalized_packet_energy?.exact, row.all_partial_sums_nonnegative ? "yes" : "no", row.identity_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Cesaro identity</span><strong>' + (aggregate.packet_energy_cesaro_identity_proved ? "proved" : "open") + '</strong></div><div><span>Partial-sum necessity</span><strong>' + (aggregate.uniform_partial_sum_lower_bound_is_necessary ? "open" : "rejected") + '</strong></div><div><span>Actual Weil lags</span><strong>' + (aggregate.actual_weil_lag_partial_sums_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_canonical_incomplete_kernel_rows || [];
    detail = [
      '<div class="poc-equation">Omitting one additive character gives exact uniform error 1/q, and no proper support missing it can do better. Its unnormalized prime average vanishes by size decay, not arithmetic phase cancellation.</div>',
      table(["q", "Fq(2)", "Fq(3)", "Dq", "|error|", "running mean", "verified"], rows.map((row) => [row.prime_q, row.fermat_quotient_F_q_2, row.fermat_quotient_F_q_3, row.canonical_slope_D_q, row.exact_error_magnitude?.exact, row.running_mean_absolute_error?.exact, row.certificate_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Sharp uniform error</span><strong>' + (aggregate.one_missing_frequency_minimax_sharp ? "1/q proved" : "open") + '</strong></div><div><span>Unnormalized mean</span><strong>' + (aggregate.unnormalized_canonical_prime_average_tends_to_zero ? "decays" : "open") + '</strong></div><div><span>Renormalized cancellation</span><strong>' + (aggregate.renormalized_cross_prime_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_q_divisible_prefix_exclusion_rows || [];
    detail = [
      '<div class="poc-equation">If q|m and the cyclotomic tail is compatible, Parseval rules out odd m. Even m forces N*<sub>r</sub>=N*<sub>-r</sub>; any asymmetric actual first-T prime prefix is excluded.</div>',
      table(["q", "m", "t", "T", "forced counts", "actual counts", "witness r", "excluded"], rows.map((row) => [row.prime_modulus_q, row.q_divisible_even_exponent_m, String(row.forced_uniform_shift_t), String(row.forced_total_prime_count_T), (row.forced_symmetric_residue_counts || []).join(", "), (row.actual_first_T_prime_residue_counts || []).join(", "), row.least_asymmetry_witness_residue, row.unique_prime_prefix_excluded ? "yes" : "no"])),
      '<p><strong>Finite boundary:</strong> ' + formatter.format(aggregate.scanned_q_divisible_pair_count || 0) + ' q-divisible rows scanned; ' + formatter.format(aggregate.compatible_q_divisible_pair_count || 0) + ' compatible; only ' + formatter.format(aggregate.bounded_prefix_certificate_count || 0) + ' prefixes under T≤100,000 enumerated.</p>',
      '<div class="poc-head"><div><span>Odd q-divisible compatibility</span><strong>' + (aggregate.odd_q_divisible_compatibility_impossible_proved ? "impossible" : "open") + '</strong></div><div><span>Bounded prefixes</span><strong>' + (aggregate.all_bounded_prefixes_excluded ? "excluded" : "open") + '</strong></div><div><span>All even tails</span><strong>' + (aggregate.all_q_divisible_compatible_tails_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_sample_rows || [];
    const box = computation.finite_box_audit || {};
    detail = [
      '<div class="poc-equation">T(u,v)=(-u-2v,u+v) has determinant one and sends twist 1 to twist 16 with B preserved, A negated, and norm negated. The two survivors are one absolute branch.</div>',
      table(["u", "v", "T(u)", "T(v)", "A1", "B1", "A16", "B16", "reduced y", "verified"], rows.map((row) => [row.u, row.v, row.transformed_u, row.transformed_v, row.A_1_u_v, row.B_1_u_v, row.A_16_transformed, row.B_16_transformed, row.reduced_y, row.identities_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>GL2 equivalence</span><strong>' + (aggregate.two_surviving_twists_gl2_equivalent ? "proved" : "open") + '</strong></div><div><span>Independent branches</span><strong>' + formatter.format(aggregate.independent_surviving_branch_count || 0) + '</strong></div><div><span>Remaining branch solved</span><strong>' + (aggregate.single_absolute_branch_globally_solved ? "yes" : "open") + '</strong></div></div>',
      '<p><strong>Finite replay:</strong> ' + formatter.format(box.exact_grid_case_count || 0) + ' integer pairs; ' + formatter.format(box.coefficient_one_point_count || 0) + ' coefficient-one point and ' + formatter.format(box.admissible_absolute_branch_point_count || 0) + ' admissible points in the box. This is not an infinite exclusion.</p>',
    ].join("");
  }

  return [
    '<div id="ticket256-cesaro-kernel-qdiv-gl2" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-256 Cesaro lag sums, sharp incomplete kernels, q-divisible reflection, and a GL2 survivor reduction</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>four partial theorems; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table">' + table(["TICKET256 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-256 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/cesaro-kernel-qdiv-gl2.ko.md">한국어 보고서</a> · <a href="../docs/cesaro-kernel-qdiv-gl2.md">English report</a> · <a href="../data/open-problem/ticket256-cesaro-kernel-qdiv-gl2.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
