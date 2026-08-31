function renderTicket263SharpEnvelopeDiagonalMod32NinthOrder(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.sharp_envelope_diagonal_mod32_ninthorder_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const families = computation.exact_alternating_reciprocal_envelope_families || [];
    detail = [
      '<div class="poc-equation">A=limsup n|E<sub>n</sub>-L| gives limsup J<sub>n</sub>&le;2A and liminf S<sub>n</sub>&ge;L-2A. The factor 2 is sharp.</div>',
      table(["L", "A", "regime", "predicted liminf S", "rows"], families.map((row) => [row.limit_L?.exact, row.reciprocal_envelope_A?.exact, row.regime, row.predicted_liminf_lag?.exact, (row.exact_rows || []).length])),
      '<div class="poc-head"><div><span>Sharp factor two</span><strong>' + (aggregate.optimal_factor_two_proved ? "proved" : "open") + '</strong></div><div><span>Critical margin</span><strong>' + (aggregate.critical_half_limit_margin_refuted ? "refuted" : "open") + '</strong></div><div><span>Actual Weil rate</span><strong>' + (aggregate.actual_weil_reciprocal_envelope_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const cases = computation.exact_complete_grid_replays || [];
    detail = [
      '<div class="poc-equation">All fixed-h Weyl limits vanish iff one data-dependent cutoff H<sub>N</sub>&rarr;&infin; has uniform cancellation over 1&le;|h|&le;H<sub>N</sub>.</div>',
      table(["grid M", "points", "cutoff H", "exact D*", "zero harmonics", "verified"], cases.map((row) => [row.grid_modulus_M, row.point_count_N, row.uniform_cutoff_H, row.exact_star_discrepancy?.exact, (row.harmonic_rows || []).length, row.case_verified ? "yes" : "no"])),
      '<p><strong>Exact replay:</strong> ' + formatter.format(aggregate.complete_grid_harmonic_case_count || 0) + ' complete-root harmonic identities. These grids are not canonical Fermat-quotient prefixes.</p>',
      '<div class="poc-head"><div><span>Diagonal equivalence</span><strong>' + (aggregate.pointwise_all_harmonics_iff_some_growing_uniform_cutoff_proved ? "proved" : "open") + '</strong></div><div><span>Weyl transfer</span><strong>' + (aggregate.weyl_criterion_external_transfer_used ? "external theorem" : "missing") + '</strong></div><div><span>Canonical schedule</span><strong>' + (aggregate.canonical_growing_cutoff_uniform_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const actual = computation.exact_actual_q3_mod32_certificate_rows || [];
    const symbolic = computation.exact_symbolic_mod32_phase_rows || [];
    detail = [
      '<div class="poc-equation">A q=3 special tie forces N<sub>2</sub> mod 32 to cycle through 28, 4, 12, 20 with l mod 4. The condition is necessary, not sufficient.</div>',
      table(["l", "T_l", "last prime", "actual N_2", "actual mod 32", "tie mod 32", "tie excluded"], actual.map((row) => [row.level_l, formatter.format(row.special_prime_prefix_length_T_l || 0), formatter.format(row.exact_nth_prime_endpoint || 0), formatter.format(row.actual_minus_one_count_N_2 || 0), row.actual_N_2_mod_32, row.tie_forced_mod_32, row.tie_excluded_by_mod_32_contrapositive ? "yes" : "no"])),
      table(["l mod 4", "tie N_2 mod 32"], symbolic.slice(0, 4).map((row) => [row.level_phase_mod_4, row.tie_forced_mod_32])),
      '<div class="poc-head"><div><span>Four-phase necessity</span><strong>' + (aggregate.tie_forces_level_phased_mod32_proved ? "proved" : "open") + '</strong></div><div><span>Actual certificates</span><strong>' + formatter.format(aggregate.actual_mod32_non_tie_certificate_count || 0) + '</strong></div><div><span>All actual levels</span><strong>' + (aggregate.all_actual_special_counts_avoid_phased_mod32_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_ninth_order_convergent_rows || [];
    const sampleRows = rows.length > 10 ? [...rows.slice(0, 5), ...rows.slice(-5)] : rows;
    detail = [
      '<div class="poc-equation">On 1/16&le;|u|/v&le;1 and v&gt;188580743973175296, the joint mod v<sup>9</sup>/u<sup>9</sup> truncations are equivalent to B<sub>1</sub>(u,v)=epsilon.</div>',
      table(["n", "a_n", "denominator digits", "root cone", "above V_0", "first failures (-,+)"], sampleRows.map((row) => [row.term_index, row.partial_quotient, row.denominator_digit_count, row.inside_one_sixteenth_to_one_root_cone ? "yes" : "no", row.above_ninth_order_exactness_threshold ? "yes" : "no", (row.sign_tests || []).map((sign) => sign.first_joint_failure_order ?? "none").join(", ")])),
      '<p><strong>Exact replay:</strong> ' + formatter.format(rows.length) + ' convergents, ' + formatter.format(aggregate.tail_exactness_applicable_convergent_count || 0) + ' in the exact tail domain, first at term ' + formatter.format(aggregate.first_tail_exactness_applicable_term_index || 0) + '. Nontrivial joint ninth-order passes: ' + formatter.format(aggregate.joint_ninth_order_pass_count || 0) + '; two modulus-one boundary passes are retained separately.</p>',
      '<div class="poc-head"><div><span>Ninth-order tail iff</span><strong>' + (aggregate.joint_ninth_order_exactness_on_root_cone_proved ? "proved" : "open") + '</strong></div><div><span>Maximum denominator</span><strong>' + formatter.format(aggregate.maximum_denominator_digit_count || 0) + ' digits</strong></div><div><span>All convergents</span><strong>' + (aggregate.all_unique_root_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket263-sharp-envelope-diagonal-mod32-ninthorder" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-263 sharp reciprocal envelope, diagonal Weyl cutoff, q=3 mod-32 phase, and ninth-order tail exactness</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>4 partial theorems; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table ticket259-audit-table ticket260-audit-table ticket261-audit-table ticket262-audit-table ticket263-audit-table">' + table(["TICKET263 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-263 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/sharp-envelope-diagonal-mod32-ninthorder.ko.md">한국어 보고서</a> · <a href="../docs/sharp-envelope-diagonal-mod32-ninthorder.md">English report</a> · <a href="../data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
