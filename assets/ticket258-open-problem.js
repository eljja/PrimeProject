function renderTicket258VariationCharacterConvergent(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.variation_character_convergent_audit || {};
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
    const rows = computation.exact_bounded_variation_spike_rows || [];
    detail = [
      '<div class="poc-equation">E<sub>4<sup>k</sup></sub>=1-2<sup>-k</sup>, E<sub>L</sub>=1 otherwise has total variation 2, but S<sub>4<sup>k</sup>-1</sub>=1-2<sup>k</sup>→-∞. Ordinary bounded variation is insufficient.</div>',
      table(["k", "L", "depth", "partial variation", "S_(L-1)", "verified"], rows.map((row) => [row.spike_level_k, row.packet_dimension_L, row.spike_depth?.exact, row.partial_total_variation_through_return?.exact, row.lag_partial_sum_S_L_minus_1?.exact, row.identity_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Total variation</span><strong>' + escapeHtml(computation.total_variation_exact?.exact || "missing") + '</strong></div><div><span>BV-only repair</span><strong>' + (aggregate.ordinary_bounded_variation_repair_refuted ? "refuted" : "open") + '</strong></div><div><span>Actual Weil packets</span><strong>' + (aggregate.actual_weil_packet_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const allRows = computation.exact_canonical_phase_rows || [];
    const rows = allRows.length > 15 ? [...allRows.slice(0, 10), ...allRows.slice(-5)] : allRows;
    detail = [
      '<div class="poc-equation">For distinct odd primes and nonzero exponents, 1 and one primitive root from each prime conductor are Q-linearly independent. No nonzero rationally weighted finite cancellation exists.</div>',
      table(["index", "q", "Fq(2)", "Fq(3)", "Dq", "nontrivial"], rows.map((row) => [row.index, row.prime_q, row.fermat_quotient_F_q_2, row.fermat_quotient_F_q_3, row.canonical_phase_exponent_D_q, row.phase_is_nontrivial_primitive_qth_root ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first 10 and last 5 of ' + formatter.format(allRows.length) + ' exact rows through q=' + formatter.format(computation.prime_limit || 0) + '.</p>',
      '<div class="poc-head"><div><span>Q-independence</span><strong>' + (aggregate.rational_linear_independence_proved_for_nontrivial_distinct_prime_phases ? "proved" : "open") + '</strong></div><div><span>Trivial phases</span><strong>' + formatter.format((aggregate.trivial_phase_primes || []).length) + '</strong></div><div><span>Sublinear magnitude</span><strong>' + (aggregate.sublinear_phase_sum_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_modulus_classification_rows || [];
    const q5 = computation.actual_q5_quartic_certificate || {};
    detail = [
      '<div class="poc-equation">One primitive odd character detects every reflection asymmetry iff q-1 is a power of two. Otherwise Φ<sub>q-1</sub> supplies an exact blind vector.</div>',
      table(["q", "q-1", "power of 2", "single character complete", "blind vector"], rows.map((row) => [row.prime_q, row.character_order_q_minus_1, row.q_minus_1_is_power_of_two ? "yes" : "no", row.one_primitive_odd_character_is_complete ? "yes" : "no", row.blind_vector_certificate ? (row.blind_vector_certificate.antisymmetric_half_vector || []).join(", ") : "none"])),
      '<p><strong>Actual q=5 prefix:</strong> counts [' + (q5.residue_counts || []).join(", ") + '], antisymmetric vector [' + (q5.antisymmetric_half_vector || []).join(", ") + '], quartic moment nonzero=' + (q5.quartic_character_detects_asymmetry ? "yes" : "no") + '.</p>',
      '<div class="poc-head"><div><span>Completeness classification</span><strong>' + (aggregate.single_primitive_character_complete_iff_fermat_modulus_proved ? "proved" : "open") + '</strong></div><div><span>Blind vectors</span><strong>' + formatter.format(aggregate.non_power_two_blind_vector_count || 0) + '</strong></div><div><span>Universal prime prefix</span><strong>' + (aggregate.all_compatible_even_q_divisible_prefixes_excluded ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.certified_convergent_rows || [];
    const shown = rows.length > 16 ? [...rows.slice(0, 8), ...rows.slice(-8)] : rows;
    const finite = computation.finite_convergent_audit || {};
    detail = [
      '<div class="poc-equation">P′(x)&gt;544 on [-1,0]. Any B<sub>1</sub>=±1 solution satisfies |ρ-p/q|&lt;1/(2q²), hence is a continued-fraction convergent of ρ.</div>',
      table(["index", "a_n", "p", "q", "B1(p,q)", "side", "unit hit"], shown.map((row) => [row.term_index, row.partial_quotient, row.convergent_numerator, row.convergent_denominator, row.B_1_at_convergent, row.root_side, row.unit_coefficient_hit ? "yes" : "no"])),
      '<p><strong>Displayed:</strong> first and last 8 of ' + formatter.format(finite.term_count || 0) + ' certified convergents. <strong>Maximum excluded denominator:</strong> ' + escapeHtml(finite.maximum_excluded_denominator || "missing") + ' (' + formatter.format(finite.maximum_excluded_denominator_digit_count || 0) + ' digits).</p>',
      '<div class="poc-head"><div><span>Convergent necessity</span><strong>' + (aggregate.continued_fraction_necessity_proved ? "proved" : "open") + '</strong></div><div><span>Linear scan necessity</span><strong>' + (aggregate.linear_denominator_scan_necessity_refuted ? "refuted" : "open") + '</strong></div><div><span>All convergents</span><strong>' + (aggregate.all_convergents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket258-variation-character-convergent" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-258 bounded variation, rational independence, character completeness, and Twin root convergents</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>2 exact no-gos + 2 partial theorems; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table ticket258-audit-table">' + table(["TICKET258 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-258 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/variation-character-convergent.ko.md">한국어 보고서</a> · <a href="../docs/variation-character-convergent.md">English report</a> · <a href="../data/open-problem/ticket258-variation-character-convergent.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
