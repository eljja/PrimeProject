function renderTicket262LimsupFiniteHarmonicMod8ThirdOrder(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.limsup_finiteharmonic_mod8_thirdorder_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const strict = computation.exact_reciprocal_tail_identity_rows || [];
    const critical = computation.exact_critical_boundary_rows || [];
    const rows = strict.length > 12 ? [...strict.slice(0, 6), ...strict.slice(-6)] : strict;
    detail = [
      '<div class="poc-equation">S<sub>n</sub>=E<sub>n+1</sub>-J<sub>n</sub>, so liminf S<sub>n</sub>=0 with a strict margin exactly when limsup J<sub>n</sub>&lt;L. Equality is insufficient.</div>',
      table(["n", "E_n", "E_(n+1)", "J_n", "S_n", "verified"], rows.map((row) => [row.index_n, row.energy_E_n?.exact, row.next_energy_E_n_plus_1?.exact, row.scaled_signed_jump_J_n?.exact, row.lag_S_n?.exact, row.row_verified ? "yes" : "no"])),
      table(["critical k", "n=4^k", "J_n", "S_n", "verified"], critical.map((row) => [row.power_k, formatter.format(row.index_n || 0), row.scaled_signed_jump_J_n?.exact, row.lag_S_n?.exact, row.critical_equality_verified ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 6 and last 6 of ' + formatter.format(strict.length) + ' strict rows, plus all ' + formatter.format(critical.length) + ' critical rows.</p>',
      '<div class="poc-head"><div><span>Exact limsup iff</span><strong>' + (aggregate.lag_margin_iff_scaled_signed_jump_limsup_below_limit_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil bound</span><strong>' + (aggregate.actual_weil_packet_limsup_bound_proved ? "proved" : "open") + '</strong></div><div><span>RH</span><strong>' + (aggregate.riemann_hypothesis_resolved ? "resolved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const cases = computation.exact_finite_harmonic_cutoff_cases || [];
    detail = [
      '<div class="poc-equation">For every fixed H, M=H+1 midpoint clusters cancel every 1&le;|h|&le;H ideal block, while D* has liminf at least 1/[4(H+1)].</div>',
      table(["H", "M", "phase cases", "blocks", "exact D* lower bound", "harmonics", "verified"], cases.map((row) => [row.harmonic_cutoff_H, row.cluster_modulus_M, row.phase_case_count, row.complete_block_count, row.star_discrepancy_lower_bound?.exact, (row.harmonic_rows || []).length, row.case_verified ? "yes" : "no"])),
      '<p><strong>Exact replay:</strong> ' + formatter.format(aggregate.total_replayed_phase_case_count || 0) + ' prime-modulus phase cases. The construction is proved for every fixed H, but it is not the canonical Fermat-quotient sequence.</p>',
      '<div class="poc-head"><div><span>Every finite cutoff insufficient</span><strong>' + (aggregate.arbitrary_fixed_finite_harmonic_cutoff_insufficient_proved ? "proved" : "open") + '</strong></div><div><span>Largest replay H</span><strong>' + formatter.format(aggregate.largest_replayed_harmonic_cutoff || 0) + '</strong></div><div><span>Canonical all-h theorem</span><strong>' + (aggregate.canonical_all_nonzero_harmonic_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const actual = computation.exact_q3_mod8_certificate_rows || [];
    const abstractRows = computation.exact_sharpness_countermodel_rows || [];
    const sample = abstractRows.length > 8 ? [...abstractRows.slice(0, 4), ...abstractRows.slice(-4)] : abstractRows;
    detail = [
      '<div class="poc-equation">A q=3 special tie forces N<sub>2</sub>=3<sup>6l+3</sup>+1=4 mod 8 and v<sub>2</sub>(N<sub>2</sub>)=2. This is necessary, not sufficient.</div>',
      table(["l", "T_l", "last prime", "actual N_2", "N_2 mod 8", "tie count mod 8", "tie excluded"], actual.map((row) => [row.level_l, formatter.format(row.special_prime_prefix_length_T_l || 0), formatter.format(row.exact_nth_prime_endpoint || 0), formatter.format(row.minus_one_residue_count_N_2 || 0), row.minus_one_residue_count_mod_8, row.tie_forced_count_mod_8, row.tie_excluded_by_mod_8_contrapositive ? "yes" : "no"])),
      table(["abstract l", "tie count", "+2 model N_2 mod 8", "+8 model N_2 mod 8", "both non-ties"], sample.map((row) => [row.level_l, row.tie_count, row.product_plus_one_but_non_tie_counts?.N_2_mod_8, row.N_2_congruent_four_but_non_tie_counts?.N_2_mod_8, row.row_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Tie => N_2=4 mod 8</span><strong>' + (aggregate.tie_forces_minus_count_four_mod_8_proved ? "proved" : "open") + '</strong></div><div><span>Actual certificates</span><strong>' + formatter.format(aggregate.actual_mod8_non_tie_certificate_count || 0) + '</strong></div><div><span>All special counts</span><strong>' + (aggregate.all_special_minus_counts_not_four_mod_8_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_bidirectional_third_order_convergent_rows || [];
    const sampleRows = rows.length > 10 ? [...rows.slice(0, 5), ...rows.slice(-5)] : rows;
    detail = [
      '<div class="poc-equation">B<sub>1</sub>(u,v)=epsilon forces third-order congruences modulo v<sup>3</sup> and u<sup>3</sup>, with coefficients 272 and 17408 at the new terms.</div>',
      table(["n", "a_n", "denominator digits", "root side", "third-order expansions", "unit hit"], sampleRows.map((row) => [row.term_index, row.partial_quotient, row.denominator_digit_count, row.root_side, row.both_third_order_expansions_match_direct_B1 ? "verified" : "failed", row.direct_unit_coefficient_hit ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 5 and last 5 of ' + formatter.format(rows.length) + ' convergents; maximum denominator has ' + formatter.format(aggregate.maximum_denominator_digit_count || 0) + ' digits. Joint third-order passes: ' + formatter.format(aggregate.joint_third_order_pass_count || 0) + '.</p>',
      '<div class="poc-head"><div><span>Dual mod u^3/v^3 necessity</span><strong>' + (aggregate.bidirectional_third_order_congruence_necessary_proved ? "proved" : "open") + '</strong></div><div><span>Prefix excluded</span><strong>' + formatter.format(aggregate.certified_convergent_count || 0) + '</strong></div><div><span>All convergents</span><strong>' + (aggregate.all_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket262-limsup-finiteharmonic-mod8-thirdorder" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-262 limsup threshold, every finite harmonic cutoff, q=3 mod-8 tie obstruction, and third-order congruences</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>3 partial theorems + 1 exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table ticket259-audit-table ticket260-audit-table ticket261-audit-table ticket262-audit-table">' + table(["TICKET262 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-262 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/limsup-finiteharmonic-mod8-thirdorder.ko.md">한국어 보고서</a> · <a href="../docs/limsup-finiteharmonic-mod8-thirdorder.md">English report</a> · <a href="../data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
