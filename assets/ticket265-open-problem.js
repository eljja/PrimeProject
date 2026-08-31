function renderTicket265SparseCutoffGrowingTwoAdicMod32(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.sparse_cutoff_growing2adic_mod32_audit || {};
  const section = ({ riemann: audit.riemann, collatz: audit.collatz, goldbach: audit.goldbach, "twin-prime": audit.twin_prime })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  const activeProblem = attempt.problem_id || problemId;
  let detail = "";

  if (activeProblem === "riemann") {
    const rows = computation.exact_sparse_reciprocal_spike_rows || [];
    detail = [
      '<div class="poc-equation">Density-one exact reciprocal control can coexist with S<sub>2^k</sub>=L-P-M&lt;0 on infinitely many adjacent spikes.</div>',
      table(["k", "n=2^k", "n a_n+", "(n+1) a_(n+1)-", "lag S_n", "zero gap"], rows.map((row) => [row.spike_exponent_k, row.positive_spike_index_n, row.scaled_positive_error?.exact, row.scaled_negative_error?.exact, row.lag_S_n?.exact, row.zero_error_gap_before_next_pair])),
      '<div class="poc-head"><div><span>Density-one sufficiency</span><strong>' + (aggregate.density_one_reciprocal_control_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Sparse pairs</span><strong>' + formatter.format(aggregate.replayed_spike_pair_count || 0) + '</strong></div><div><span>Actual Weil envelope</span><strong>' + (aggregate.actual_weil_one_sided_envelope_sum_below_limit_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_dyadic_good_bad_prefix_rows || [];
    detail = [
      '<div class="poc-equation">K<sub>q</sub>=q-1 but K<sub>3q/4</sub>&le;5 for every dyadic q&ge;8; limsup K<sub>N</sub>=&infin; does not imply K<sub>N</sub>&rarr;&infin;.</div>',
      table(["q", "good N", "good K_N", "bad N", "bad K_N upper", "|W_N(1)| lower"], rows.map((row) => [row.dyadic_grid_modulus_q, row.complete_grid_good_prefix_N, row.exact_good_cutoff_K_N, row.positive_arc_bad_prefix_N, row.bad_prefix_cutoff_upper_bound, row.exact_rational_lower_bound_for_abs_W_N_1?.exact])),
      '<div class="poc-head"><div><span>Unbounded sufficiency</span><strong>' + (aggregate.unbounded_cutoff_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>liminf K_N</span><strong>&le;5</strong></div><div><span>Canonical no bounded subsequence</span><strong>' + (aggregate.canonical_fermat_quotient_threshold_cutoff_diverges_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_growing_modulus_threshold_rows || [];
    detail = [
      '<div class="poc-equation">N<sub>1</sub>+N<sub>2</sub>=2M and N<sub>2</sub>&equiv;M (mod 2<sup>m</sup>) force a tie for all nonnegative pairs iff 2<sup>m</sup>&gt;M.</div>',
      table(["level l", "M_l", "least m_l", "decisive 2^m_l", "largest insufficient"], rows.slice(0, 12).map((row) => [row.level_l, row.tie_count_M_l, row.least_decisive_exponent_m_l, row.least_decisive_modulus_two_to_m_l, row.largest_insufficient_modulus_two_to_m_l_minus_1])),
      '<p><strong>Finite actual replay:</strong> ' + formatter.format(aggregate.inherited_actual_decisive_certificate_count || 0) + ' SHA-256-pinned q=3 levels; no all-level conclusion.</p>',
      '<div class="poc-head"><div><span>Sharp growing threshold</span><strong>' + (aggregate.sharp_growing_modulus_threshold_proved ? "proved" : "open") + '</strong></div><div><span>Lower-exponent models</span><strong>' + formatter.format(aggregate.lower_exponent_countermodel_count || 0) + '</strong></div><div><span>Actual all-level avoidance</span><strong>' + (aggregate.actual_q3_special_prime_race_nonvanishing_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.certified_convergent_mod32_filter_rows || [];
    const survivors = rows.filter((row) => row.either_sign_filter);
    detail = [
      '<div class="poc-equation">gcd(u,v)=1 and B<sub>1</sub>(u,v)=&epsilon;&isin;{&plusmn;1} imply v even and u+v&equiv;&epsilon; (mod 32); the converse has explicit infinite counterfamilies.</div>',
      table(["n", "u mod 32", "v mod 32", "+ filter", "- filter", "later tail"], survivors.map((row) => [row.term_index, row.u_mod_32, row.v_mod_32, row.plus_diagonal_filter ? "yes" : "no", row.minus_diagonal_filter ? "yes" : "no", row.later_than_subthreshold_head ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Necessary mod-32 filter</span><strong>' + (aggregate.primitive_unit_implies_mod32_diagonal_filter_proved ? "proved" : "open") + '</strong></div><div><span>Filter survivors</span><strong>' + formatter.format(aggregate.either_sign_filter_count || 0) + '</strong></div><div><span>Later survivors</span><strong>' + formatter.format(aggregate.later_either_sign_filter_count || 0) + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket265-sparse-cutoff-growing2adic-mod32" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-265 sparse-envelope and cutoff no-go, growing two-adic tie test, and mod-32 Twin filter</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>2 partial theorems + 2 exact no-go results; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket265-audit-table">' + table(["TICKET265 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-265 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/sparse-cutoff-growing2adic-mod32.ko.md">한국어 보고서</a> · <a href="../docs/sparse-cutoff-growing2adic-mod32.md">English report</a> · <a href="../data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
