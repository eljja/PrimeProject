function renderTicket259CriticalAlignmentCompatibilityLocal(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.critical_alignment_compatibility_local_audit || {};
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
    const rows = computation.exact_critical_threshold_rows || [];
    detail = [
      '<div class="poc-equation">E<sub>4<sup>k</sup>+1</sub>=1-4<sup>-k</sup>, otherwise E<sub>L</sub>=1: total variation 2/3, scaled drop 1, but S<sub>4<sup>k</sup></sub>=-4<sup>-k</sup>. Equality is insufficient.</div>',
      table(["k", "n", "drop", "n x drop", "S_n", "verified"], rows.map((row) => [row.level_k, row.downward_transition_n, row.critical_drop?.exact, row.scaled_downward_jump_n_times_drop?.exact, row.lag_partial_sum_S_n?.exact, row.identity_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Total variation</span><strong>' + escapeHtml(computation.total_variation_exact?.exact || "missing") + '</strong></div><div><span>Critical equality</span><strong>' + (aggregate.nonstrict_critical_threshold_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Actual Weil packets</span><strong>' + (aggregate.actual_weil_packet_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const allRows = computation.exact_alignment_envelope_rows || [];
    const rows = allRows.length > 15 ? [...allRows.slice(0, 10), ...allRows.slice(-5)] : allRows;
    detail = [
      '<div class="poc-equation">z<sub>j</sub>=exp(2 pi i/q<sub>j</sub>) has distinct nontrivial prime order and Q-independence, yet N<sup>-1</sup> sum z<sub>j</sub> tends to 1. Structural order data alone do not force cancellation.</div>',
      table(["N", "q_N", "sum 1/q", "deviation envelope", "magnitude lower", "verified"], rows.map((row) => [row.prefix_length_N, row.prime_order_q_N, row.reciprocal_prime_sum?.exact, row.rigorous_normalized_deviation_upper_bound?.exact, row.rigorous_normalized_magnitude_lower_bound?.exact, row.envelope_verified ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 10 and last 5 of ' + formatter.format(allRows.length) + ' exact rational envelopes through q=' + formatter.format(computation.prime_limit || 0) + '.</p>',
      '<div class="poc-head"><div><span>Aligned magnitude</span><strong>' + (aggregate.normalized_phase_sum_tends_to_one_proved ? "linear" : "open") + '</strong></div><div><span>Order-only sublinearity</span><strong>' + (aggregate.sublinear_from_order_data_alone_refuted ? "refuted" : "open") + '</strong></div><div><span>Canonical D_q sum</span><strong>' + (aggregate.canonical_sublinear_phase_sum_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const allRows = computation.exact_compatibility_classification_rows || [];
    const rows = allRows.filter((row) => row.prime_q === 13);
    const certificate = computation.q13_m26_exact_prime_prefix_certificate || {};
    detail = [
      '<div class="poc-equation">For odd prime q and m=qs, cyclic compatibility holds iff s is 2 modulo 4. The new q=13,m=26 forced prefix is excluded by two independent exact prime-residue algorithms.</div>',
      table(["q", "s", "m", "c0", "shift t", "compatible"], rows.map((row) => [row.prime_q, row.ratio_s_equals_m_over_q, row.exponent_m, row.zero_coefficient_c0, row.forced_shift_t, row.compatible ? "yes" : "no"])),
      '<p><strong>q=13,m=26:</strong> T=' + formatter.format(certificate.forced_total_prime_count_T || 0) + ', last prime=' + formatter.format(certificate.exact_nth_prime_endpoint || 0) + ', primitive remainder [' + (certificate.primitive_odd_character_moment_remainder || []).join(", ") + '], certificate=' + (certificate.certificate_verified ? "verified" : "failed") + '.</p>',
      table(["residue r", "forced", "actual", "reflection difference"], (certificate.forced_symmetric_residue_counts || []).map((value, index) => [index, value, certificate.actual_first_T_prime_residue_counts?.[index], certificate.actual_reflection_differences?.[index]])),
      '<div class="poc-head"><div><span>Compatibility iff</span><strong>' + (aggregate.q_divisible_compatibility_iff_ratio_two_mod_four_proved ? "proved" : "open") + '</strong></div><div><span>Independent algorithms</span><strong>' + (aggregate.independent_exact_residue_algorithms_agree ? "agree" : "failed") + '</strong></div><div><span>Universal prefix theorem</span><strong>' + (aggregate.all_compatible_even_q_divisible_prefixes_excluded ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_local_witness_rows || [];
    detail = [
      '<div class="poc-equation">For every fixed M and rational I inside (-1,0), infinitely many primitive admissible (u,v) in I satisfy B<sub>1</sub>(u,v)=1 mod M. Fixed local congruences plus a fixed root window cannot close exponent 17.</div>',
      table(["M", "N", "u", "v=M^N", "u/v", "B1 mod M", "verified"], rows.map((row) => [row.modulus_M, row.power_exponent_N, row.primitive_numerator_u, row.denominator_v_equals_M_power_N, row.ratio_u_over_v?.exact, row.B1_mod_M, row.witness_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Local witnesses</span><strong>' + (aggregate.primitive_admissible_fixed_window_local_witnesses_proved ? "infinite" : "open") + '</strong></div><div><span>Fixed congruence route</span><strong>' + (aggregate.finite_coefficient_congruence_plus_fixed_window_route_refuted ? "refuted" : "open") + '</strong></div><div><span>All convergents</span><strong>' + (aggregate.scale_dependent_convergent_exclusion_proved ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket259-critical-alignment-compatibility-local" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-259 critical threshold, aligned phases, exact compatibility, and local congruence no-go</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>3 exact no-gos + 1 partial theorem; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table ticket259-audit-table">' + table(["TICKET259 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-259 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/critical-alignment-compatibility-local.ko.md">한국어 보고서</a> · <a href="../docs/critical-alignment-compatibility-local.md">English report</a> · <a href="../data/open-problem/ticket259-critical-alignment-compatibility-local.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
