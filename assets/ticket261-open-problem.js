function renderTicket261SharpnessWeylTiesDualCongruence(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.sharpness_weyl_ties_dualcongruence_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const allRows = computation.exact_reciprocal_tail_rows || [];
    const rows = allRows.length > 16 ? [...allRows.slice(0, 8), ...allRows.slice(-8)] : allRows;
    detail = [
      '<div class="poc-equation">E<sub>n</sub>=L+c/n has S<sub>n</sub>=L exactly, while sum n(E<sub>n</sub>-E<sub>n+1</sub>) diverges. TICKET-260 summability is sufficient but not necessary.</div>',
      table(["n", "E_n", "d_n", "n d_n", "S_n", "partial sum", "verified"], rows.map((row) => [row.index_n, row.energy_E_n?.exact, row.downward_drop_d_n?.exact, row.scaled_drop_n_d_n?.exact, row.lag_S_n?.exact, row.partial_scaled_downward_variation?.exact, row.row_verified ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 8 and last 8 of ' + formatter.format(allRows.length) + ' exact Fraction rows.</p>',
      '<div class="poc-head"><div><span>Lag positivity</span><strong>' + (aggregate.eventual_lag_positivity_proved ? "proved" : "open") + '</strong></div><div><span>Scaled sum</span><strong>' + (aggregate.scaled_downward_variation_diverges_proved ? "diverges" : "open") + '</strong></div><div><span>Actual Weil packet</span><strong>' + (aggregate.actual_weil_packet_used ? "used" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const allRows = computation.exact_first_harmonic_countermodel_rows || [];
    const rows = allRows.length > 10 ? [...allRows.slice(0, 5), ...allRows.slice(-5)] : allRows;
    const canonical = computation.exact_canonical_star_discrepancy_rows || [];
    detail = [
      '<div class="poc-equation">Alternating clusters near 1/4 and 3/4 cancel the first Weyl harmonic, but [0,1/3) witnesses star discrepancy tending to 1/6.</div>',
      table(["j", "q_j", "d_j", "d_j/q_j", "first-harmonic bound", "D* witness", "verified"], rows.map((row) => [row.index_j, row.prime_modulus_q_j, row.phase_exponent_d_j, row.normalized_point_d_j_over_q_j?.exact, row.normalized_first_harmonic_upper_bound?.exact, row.star_discrepancy_interval_witness?.exact, row.row_verified ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 5 and last 5 of ' + formatter.format(allRows.length) + ' countermodel rows.</p>',
      table(["canonical prefix", "largest q", "exact D*", "dyadic increase", "witness q"], canonical.map((row) => [formatter.format(row.canonical_prime_prefix_count || 0), formatter.format(row.largest_prime_q || 0), row.exact_star_discrepancy?.exact, row.increased_from_previous_dyadic_prefix ? "yes" : "no", row.extremal_witness?.prime_q])),
      '<div class="poc-head"><div><span>First harmonic</span><strong>' + (aggregate.first_harmonic_cancellation_proved ? "cancels" : "open") + '</strong></div><div><span>Countermodel liminf D*</span><strong>' + escapeHtml(aggregate.star_discrepancy_liminf_lower_bound?.exact || "missing") + '</strong></div><div><span>Canonical all-harmonic theorem</span><strong>' + (aggregate.canonical_angular_discrepancy_tends_to_zero_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const actual = computation.exact_q3_product_parity_certificate_rows || [];
    const abstractRows = computation.exact_density_only_tie_countermodel_rows || [];
    const sample = abstractRows.length > 8 ? [...abstractRows.slice(0, 4), ...abstractRows.slice(-4)] : abstractRows;
    detail = [
      '<div class="poc-equation">A q=3 special prime-race tie forces the nonzero prime-prefix product to be +1 mod 3. Product -1 is an exact non-tie certificate.</div>',
      table(["l", "T_l", "last prime", "actual counts", "N_2", "product mod 3", "tie excluded"], actual.map((row) => [row.level_l, formatter.format(row.special_prime_prefix_length_T_l || 0), formatter.format(row.exact_nth_prime_endpoint || 0), (row.actual_residue_counts_mod_3 || []).join(", "), row.minus_one_residue_count_N_2, row.prime_prefix_product_mod_3_excluding_prime_3, row.minus_one_product_excludes_tie ? "yes" : "no"])),
      table(["abstract l", "T_l", "+ count", "- count", "difference", "product"], sample.map((row) => [row.level_l, row.special_prefix_length_T_l, row.alternating_plus_count, row.alternating_minus_count, row.prefix_difference, row.abstract_product_mod_3])),
      '<p><strong>Density-only no-go:</strong> an alternating residue sequence ties at every special prefix while every ordinary prefix discrepancy is at most one.</p>',
      '<div class="poc-head"><div><span>Tie => product +1</span><strong>' + (aggregate.tie_forces_product_plus_one_mod_3_proved ? "proved" : "open") + '</strong></div><div><span>Actual -1 certificates</span><strong>' + formatter.format(aggregate.actual_product_minus_one_certificate_count || 0) + '</strong></div><div><span>All special products</span><strong>' + (aggregate.all_special_prime_prefix_products_minus_one_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_bidirectional_convergent_rows || [];
    const sampleRows = rows.length > 10 ? [...rows.slice(0, 5), ...rows.slice(-5)] : rows;
    const denominatorPasses = computation.denominator_first_order_nontrivial_passes || [];
    const numeratorPasses = computation.numerator_first_order_nontrivial_passes || [];
    detail = [
      '<div class="poc-equation">B<sub>1</sub>(u,v)=epsilon forces both u<sup>17</sup>+17u<sup>16</sup>v=epsilon mod v<sup>2</sup> and 256v<sup>17</sup>+4352uv<sup>16</sup>=epsilon mod u<sup>2</sup>.</div>',
      table(["filter", "n", "u", "v", "epsilon"], [...denominatorPasses.map((row) => ["denominator order 1", row.term_index, row.numerator, row.denominator, row.epsilon]), ...numeratorPasses.map((row) => ["numerator order 1", row.term_index, row.numerator, row.denominator, row.epsilon])]),
      table(["n", "a_n", "denominator digits", "root side", "two expansions", "unit hit"], sampleRows.map((row) => [row.term_index, row.partial_quotient, row.denominator_digit_count, row.root_side, row.both_truncated_expansions_match_direct_B1 ? "verified" : "failed", row.direct_unit_coefficient_hit ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 5 and last 5 of ' + formatter.format(rows.length) + ' convergents; maximum denominator has ' + formatter.format(aggregate.maximum_denominator_digit_count || 0) + ' digits. Joint second-order passes: ' + formatter.format(aggregate.joint_second_order_pass_count || 0) + '.</p>',
      '<div class="poc-head"><div><span>Dual mod u^2/v^2 necessity</span><strong>' + (aggregate.bidirectional_second_order_congruence_necessary_proved ? "proved" : "open") + '</strong></div><div><span>First-order pair</span><strong>' + (aggregate.bidirectional_first_order_filter_complete ? "complete" : "refuted") + '</strong></div><div><span>All convergents</span><strong>' + (aggregate.all_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket261-sharpness-weyl-ties-dualcongruence" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-261 sharpness, Weyl harmonics, q=3 product parity, and bidirectional congruences</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>2 partial theorems + 2 exact no-gos; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table ticket259-audit-table ticket260-audit-table ticket261-audit-table">' + table(["TICKET261 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-261 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/sharpness-weyl-ties-dualcongruence.ko.md">한국어 보고서</a> · <a href="../docs/sharpness-weyl-ties-dualcongruence.md">English report</a> · <a href="../data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
