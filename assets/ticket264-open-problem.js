function renderTicket264AsymmetricThresholdFixedTwoAdicHead(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.asymmetric_threshold_fixed2adic_head_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const families = computation.exact_asymmetric_reciprocal_families || [];
    detail = [
      '<div class="poc-equation">limsup J<sub>n</sub>&le;A<sub>+</sub>+A<sub>-</sub>, &nbsp; liminf S<sub>n</sub>&ge;L-A<sub>+</sub>-A<sub>-</sub>; both coefficients are sharp.</div>',
      table(["A+", "A-", "sum", "regime", "liminf S", "rows"], families.map((row) => [row.positive_reciprocal_envelope_A_plus?.exact, row.negative_reciprocal_envelope_A_minus?.exact, row.envelope_sum?.exact, row.regime, row.predicted_liminf_lag?.exact, (row.exact_rows || []).length])),
      '<div class="poc-head"><div><span>Asymmetric bound</span><strong>' + (aggregate.asymmetric_envelope_bound_proved ? "proved" : "open") + '</strong></div><div><span>Joint sharpness</span><strong>' + (aggregate.joint_coefficient_one_sharp_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil sum</span><strong>' + (aggregate.actual_weil_one_sided_envelope_sum_below_limit_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const cases = computation.exact_complete_grid_threshold_replays || [];
    detail = [
      '<div class="poc-equation">K<sub>N</sub>=max{H&le;N:E<sub>N</sub>(H)&le;1/H}; every fixed Weyl harmonic vanishes iff K<sub>N</sub>&rarr;&infin;.</div>',
      table(["complete grid N", "threshold cutoff K_N", "next harmonic fails", "checks"], cases.map((row) => [row.complete_grid_size_N, row.canonical_threshold_cutoff_K_N, row.next_harmonic_fails ? "yes" : "no", (row.harmonic_tests || []).length])),
      '<div class="poc-head"><div><span>Explicit equivalence</span><strong>' + (aggregate.pointwise_weyl_iff_explicit_threshold_cutoff_diverges_proved ? "proved" : "open") + '</strong></div><div><span>Exact checks</span><strong>' + formatter.format(aggregate.harmonic_threshold_case_count || 0) + '</strong></div><div><span>Canonical divergence</span><strong>' + (aggregate.canonical_fermat_quotient_threshold_cutoff_diverges_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const periods = computation.exact_two_adic_phase_period_rows || [];
    detail = [
      '<div class="poc-equation">For every fixed 2<sup>m</sup>, the q=3 tie signature plus total admits explicit non-tie count models.</div>',
      table(["m", "2^m", "least level period", "period verified"], periods.map((row) => [row.modulus_exponent_m, row.modulus_two_to_m, row.least_level_period, row.period_verified ? "yes" : "no"])),
      '<p><strong>Exact replay:</strong> ' + formatter.format(aggregate.countermodel_count || 0) + ' shifted-count countermodels. They are abstract count pairs, not actual prime-residue counts.</p>',
      '<div class="poc-head"><div><span>All fixed signatures</span><strong>' + (aggregate.fixed_two_adic_signature_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Phase periods</span><strong>' + formatter.format(aggregate.phase_period_replay_count || 0) + '</strong></div><div><span>Actual prime race</span><strong>' + (aggregate.actual_q3_special_prime_race_nonvanishing_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_head_and_crossing_rows || [];
    const sampleRows = rows.length > 10 ? [...rows.slice(0, 5), ...rows.slice(-5)] : rows;
    detail = [
      '<div class="poc-equation">q<sub>37</sub>=110221790993960069 &le; V<sub>0</sub> &lt; q<sub>38</sub>=309742427372962732; all 38 subthreshold convergents are unit-free.</div>',
      table(["n", "a_n", "denominator", "below V_0", "unit-free"], sampleRows.map((row) => [row.term_index, row.partial_quotient, row.convergent_denominator, row.at_or_below_exactness_threshold ? "yes" : "no", row.direct_unit_free ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Complete finite head</span><strong>' + (aggregate.all_subthreshold_unique_root_convergents_unit_free_proved ? "proved" : "open") + '</strong></div><div><span>Head size</span><strong>' + formatter.format(aggregate.subthreshold_convergent_count || 0) + '</strong></div><div><span>Infinite tail</span><strong>' + (aggregate.all_unique_root_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket264-asymmetric-threshold-fixed2adic-head" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-264 asymmetric envelope, explicit threshold cutoff, fixed two-adic no-go, and finite-head closure</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>3 partial theorems + 1 exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket264-audit-table">' + table(["TICKET264 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-264 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/asymmetric-threshold-fixed2adic-head.ko.md">한국어 보고서</a> · <a href="../docs/asymmetric-threshold-fixed2adic-head.md">English report</a> · <a href="../data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
