function renderTicket249CompactProjectiveParsevalLebesgue(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.compact_projective_parseval_lebesgue_audit || {};
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
    const rows = computation.exact_finite_rank_rows || [];
    detail = [
      '<div class="poc-equation">For every compact K on the full even L2 model, Q<sub>0</sub>(f<sub>n</sub>)≤11/n and ⟨Kf<sub>n</sub>,f<sub>n</sub>⟩→0 along the normalized even Legendre sequence. Compact off-diagonal corrections cannot repair coercivity there.</div>',
      table(["n", "degree", "rank", "moment window", "partial Q0", "bound", "projection", "verified"], rows.map((row) => [
        row.half_degree_n,
        row.legendre_degree,
        row.finite_rank_projection_rank,
        row.checked_moment_window,
        row.exact_partial_unweighted_energy?.exact,
        row.proved_all_moment_energy_bound?.exact,
        row.exact_projection_energy?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Compact no-go</span><strong>' + (aggregate.compact_offdiagonal_coercivity_no_go_proved ? "proved" : "open") + '</strong></div><div><span>Noncompact arithmetic</span><strong>' + (aggregate.noncompact_arithmetic_offdiagonal_control_proved ? "controlled" : "open") + '</strong></div><div><span>Actual Weil closure</span><strong>' + (aggregate.genuine_weil_admissible_closure_reached ? "reached" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_exact_prime_rows || [];
    const fieldRows = computation.exact_finite_field_rows || [];
    const replay = computation.exact_modular_scan || {};
    detail = [
      '<div class="poc-equation">The separated condition is exactly (U<sub>q</sub>,V<sub>q</sub>)=t(3,5) for a unique nonzero t. It is one projective target [3:5], not two independent congruences.</div>',
      table(["q", "Uq", "Vq", "W(32,27)", "W(2,3)", "t", "separated", "verified"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.U_q,
        row.V_q,
        row.W_32_27_mod_q,
        row.W_2_3_mod_q,
        row.projective_parameter_t ?? "—",
        row.separated_bad_prime ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["field q", "pairs", "zero-line points", "nonzero projective points", "verified"], fieldRows.map((row) => [
        row.prime_q,
        formatter.format(row.pairs_checked || 0),
        row.linear_zero_pairs,
        row.nonzero_projective_pairs,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Primes scanned</span><strong>' + formatter.format(replay.primes_checked || 0) + '</strong></div><div><span>Separated hits</span><strong>' + formatter.format((replay.separated_bad_primes || []).length) + '</strong></div><div><span>Occurrence/avoidance</span><strong>' + (aggregate.finite_scan_proves_occurrence_or_avoidance ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_selected_spike_rows || [];
    const replay = computation.exact_group_ring_replay || {};
    detail = [
      '<div class="poc-equation">The centered cosine jet has Fourier support only at ±a<sub>0</sub>; each reduced numerator carries exactly half the total Parseval energy. Abstract centeredness plus mean-square energy cannot force a uniform little-o bound.</div>',
      table(["q", "a0", "support", "D0", "total energy", "each spike", "ratio²", "verified"], rows.map((row) => [
        row.denominator_q,
        row.reduced_frequency_a0,
        (row.nonzero_numerators || []).join(", "),
        row.centered_energy_D0?.exact,
        row.total_parseval_energy?.exact,
        row.each_spike_energy?.exact,
        row.spike_to_total_ratio_squared?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Group-ring cases</span><strong>' + formatter.format(replay.reduced_frequency_cases || 0) + '</strong></div><div><span>Parseval-only route</span><strong>' + (aggregate.abstract_mean_square_to_uniform_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Prime arithmetic saving</span><strong>' + (aggregate.prime_specific_anti_concentration_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_scale_rows || [];
    const witnesses = computation.selected_left_active_witnesses || [];
    detail = [
      '<div class="poc-equation">If p≠3 and p<sup>2m</sup>+2=r<sup>ℓ</sup> for odd primes p,r, then the unique solution is 25+2=27. The external D=2 Lebesgue–Nagell classification is an explicit proof-DAG dependency.</div>',
      table(["X", "L", "even p≠3", "even p=3", "odd exponent", "R", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        row.left_active_composite_pairs_L,
        row.left_even_exponent_base_not_3,
        row.left_even_exponent_base_3,
        row.left_odd_exponent,
        row.right_active_composite_pairs_R,
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["n", "n+2", "left", "right", "category", "verified"], witnesses.map((row) => [
        formatter.format(row.n || 0),
        formatter.format(row.n_plus_2 || 0),
        row.left_representation,
        row.right_representation,
        row.category,
        row.classification_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Even-left p≠3</span><strong>' + (aggregate.even_left_base_not3_classification_proved ? "classified" : "open") + '</strong></div><div><span>Unique pair</span><strong>' + (aggregate.unique_pair || []).join("→") + '</strong></div><div><span>Right contamination</span><strong>' + (aggregate.right_active_contamination_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket249-compact-projective-parseval-lebesgue" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 249 compact perturbations, projective Fermat quotients, Parseval spikes, and active-power classification</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-go results; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket247-audit-table ticket248-audit-table ticket249-audit-table">' + table(["TICKET249 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-249 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/compact-projective-parseval-lebesgue.ko.md">한국어 보고서</a> · <a href="../docs/compact-projective-parseval-lebesgue.md">English report</a> · <a href="../data/open-problem/ticket249-compact-projective-parseval-lebesgue.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
