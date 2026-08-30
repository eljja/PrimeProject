function renderTicket260WeightedEquidistributionPrimeRaceVariableMod(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.weighted_equidistribution_primerace_variablemod_audit || {};
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
    const rows = computation.exact_summable_variation_rows || [];
    detail = [
      '<div class="poc-equation">If E<sub>n</sub> tends to L&gt;0 and sum n(E<sub>n</sub>-E<sub>n+1</sub>)<sub>+</sub> is finite, then liminf S<sub>n</sub>&gt;=L. The exact model has weighted downward variation 1/3.</div>',
      table(["k", "n", "drop", "n x drop", "S_n", "partial weighted sum", "verified"], rows.map((row) => [row.level_k, row.downward_transition_n, row.drop?.exact, row.weighted_drop_n_times_drop?.exact, row.lag_partial_sum_S_n?.exact, row.partial_weighted_downward_variation?.exact, row.identity_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Weighted criterion</span><strong>' + (aggregate.summable_scaled_downward_variation_implies_eventual_lag_positivity_proved ? "proved" : "open") + '</strong></div><div><span>Model weighted sum</span><strong>' + escapeHtml(computation.weighted_downward_variation_exact?.exact || "missing") + '</strong></div><div><span>Actual Weil summability</span><strong>' + (aggregate.actual_weil_scaled_downward_variation_summable ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const allRows = computation.exact_phase_envelope_rows || [];
    const rows = allRows.length > 15 ? [...allRows.slice(0, 10), ...allRows.slice(-5)] : allRows;
    const modRows = computation.exact_fixed_modulus_balance_rows || [];
    detail = [
      '<div class="poc-equation">d<sub>j</sub>=j is perfectly balanced modulo every fixed M, while q<sub>j</sub>&gt;j<sup>3</sup> makes exp(2 pi i d<sub>j</sub>/q<sub>j</sub>) align at 1. Fixed-modulus exponent statistics do not control moving-modulus angles.</div>',
      table(["j", "q_j", "d_j", "d_j/q_j", "chord bound", "prefix bound", "verified"], rows.map((row) => [row.index_j, row.prime_order_q_j, row.phase_exponent_d_j, row.exponent_over_prime?.exact, row.chord_deviation_upper_bound?.exact, row.normalized_prefix_deviation_upper_bound?.exact, row.row_verified ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 10 and last 5 of ' + formatter.format(allRows.length) + ' exact phase envelopes.</p>',
      table(["fixed M", "N", "residue counts", "max difference", "verified"], modRows.map((row) => [row.fixed_modulus_M, row.prefix_length_N, (row.residue_counts || []).join(", "), row.maximum_count_difference, row.balanced_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Fixed-modulus balance</span><strong>' + (aggregate.fixed_modulus_exponent_equidistribution_proved ? "proved" : "open") + '</strong></div><div><span>Normalized phase limit</span><strong>' + (aggregate.normalized_phase_sum_tends_to_one_proved ? "one" : "open") + '</strong></div><div><span>Canonical angular discrepancy</span><strong>' + (aggregate.canonical_angular_discrepancy_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_q3_prime_race_certificate_rows || [];
    detail = [
      '<div class="poc-equation">For q=3, m=12l+6 and A=3<sup>6l+2</sup>, compatibility forces (1,1+3A,1+3A). Equality with the actual prefix is exactly a mod-3 prime-race tie at T=6A+3.</div>',
      table(["l", "m", "T", "last prime", "forced counts", "actual counts", "Delta_3", "excluded"], rows.map((row) => [row.level_l, row.exponent_m, formatter.format(row.forced_prefix_length_T || 0), formatter.format(row.exact_nth_prime_endpoint || 0), (row.forced_residue_counts || []).join(", "), (row.actual_residue_counts || []).join(", "), row.mod_3_prime_race_difference_N1_minus_N2, row.compatible_prefix_excluded ? "yes" : "no"])),
      '<div class="poc-head"><div><span>q=3 equivalence</span><strong>' + (aggregate.q3_compatible_family_prime_race_equivalence_proved ? "proved" : "open") + '</strong></div><div><span>Independent algorithms</span><strong>' + formatter.format(aggregate.independent_exact_algorithm_count || 0) + '</strong></div><div><span>All q=3 levels</span><strong>' + (aggregate.all_q3_levels_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const passes = computation.first_order_nontrivial_passes || [];
    const rows = computation.exact_variable_denominator_convergent_rows || [];
    const sampleRows = rows.length > 10 ? [...rows.slice(0, 5), ...rows.slice(-5)] : rows;
    detail = [
      '<div class="poc-equation">B<sub>1</sub>(u,v)=epsilon forces u<sup>17</sup>+17u<sup>16</sup>v=epsilon mod v<sup>2</sup>. Both signs fail this scale-dependent condition on 256 certified unique-root convergents.</div>',
      table(["n", "u", "v", "epsilon", "exact B1"], passes.map((row) => [row.term_index, row.numerator, row.denominator, row.epsilon, row.B_1_at_convergent])),
      '<p><strong>First-order-only counterexamples:</strong> ' + formatter.format(passes.length) + '. <strong>Second-order passes:</strong> ' + formatter.format((computation.second_order_nontrivial_passes || []).length) + '.</p>',
      table(["n", "a_n", "denominator digits", "root side", "mod v^2 expansion", "unit hit"], sampleRows.map((row) => [row.term_index, row.partial_quotient, row.denominator_digit_count, row.root_side, row.truncated_expansion_matches_direct_B1_mod_v_squared ? "verified" : "failed", row.direct_unit_coefficient_hit ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 5 and last 5 of ' + formatter.format(rows.length) + ' certified convergents; maximum denominator has ' + formatter.format(aggregate.maximum_denominator_digit_count || 0) + ' digits.</p>',
      '<div class="poc-head"><div><span>Modulo v^2 necessity</span><strong>' + (aggregate.second_order_denominator_congruence_necessary_proved ? "proved" : "open") + '</strong></div><div><span>First-order filter</span><strong>' + (aggregate.first_order_only_filter_complete ? "complete" : "refuted") + '</strong></div><div><span>All convergents</span><strong>' + (aggregate.all_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket260-weighted-equidistribution-primerace-variablemod" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-260 weighted variation, fixed-modulus equidistribution, mod-3 prime race, and variable-denominator sieve</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>3 partial theorems + 1 exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table ticket259-audit-table ticket260-audit-table">' + table(["TICKET260 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-260 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/weighted-equidistribution-primerace-variablemod.ko.md">한국어 보고서</a> · <a href="../docs/weighted-equidistribution-primerace-variablemod.md">English report</a> · <a href="../data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
