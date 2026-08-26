function renderTicket248UnweightedWieferichJetActive(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.unweighted_wieferich_jet_active_audit || {};
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
    const rows = computation.exact_legendre_rows || [];
    detail = [
      '<div class="poc-equation">For f<sub>n</sub>=√((4n+1)/2)P<sub>2n</sub>, the raw unweighted infinite-moment energy satisfies Q<sub>0</sub>(f<sub>n</sub>)≤11/n. This removes the Hilbert-Schmidt hypothesis but still gives zero coercivity on the full even L2 sphere.</div>',
      table(["n", "degree", "partial cutoff", "partial Q0", "proved bound", "verified"], rows.map((row) => [
        row.half_degree_n,
        row.legendre_degree,
        row.partial_cutoff_K,
        row.partial_unweighted_energy?.exact,
        row.proved_all_tail_energy_bound?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Unweighted no-go</span><strong>' + (aggregate.unweighted_non_hilbert_schmidt_no_go_proved ? "proved" : "open") + '</strong></div><div><span>Analytic constant</span><strong>' + (aggregate.analytic_bound_constant ?? "missing") + '/n</strong></div><div><span>Actual Weil closure</span><strong>' + (aggregate.genuine_weil_admissible_closure_reached ? "reached" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_exact_rows || [];
    const replay = computation.exact_modular_scan || {};
    detail = [
      '<div class="poc-equation">The actual first-level bad branch is exactly {q:W<sub>q</sub>(32,27)=0}∖{q:W<sub>q</sub>(2,3)=0}. The finite scan has no separated hit, but this is not an all-prime exclusion.</div>',
      table(["q", "W(32,27)", "W(2,3)", "Uq", "Vq", "separated", "verified"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.W_32_27_mod_q,
        row.W_2_3_mod_q,
        row.fermat_quotient_2_mod_q,
        row.fermat_quotient_3_mod_q,
        row.separated_bad_prime ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Primes scanned</span><strong>' + formatter.format(replay.primes_checked || 0) + '</strong></div><div><span>Separated hits</span><strong>' + formatter.format((replay.separated_bad_primes || []).length) + '</strong></div><div><span>Global absence</span><strong>' + (aggregate.finite_scan_proves_global_absence ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_selected_first_jet_rows || [];
    const replay = computation.exact_modular_replay || {};
    detail = [
      '<div class="poc-equation">For J<sub>a</sub>(t)=R<sub>0</sub>(a)+itR<sub>1</sub>(a), Σ<sub>a mod q</sub>|J<sub>a</sub>(t)|²=q(D<sub>0</sub>+t²D<sub>1</sub>) exactly. The arc Taylor remainder is at most 2π²β²M<sub>2</sub>.</div>',
      table(["X", "q", "P", "M", "φD0", "φD1", "M2/X⁴", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        row.denominator_q,
        formatter.format(row.prime_count_P || 0),
        formatter.format(row.prime_first_moment_M || 0),
        row.phi_times_count_variance,
        row.phi_times_first_moment_variance,
        row.beta_squared_remainder_scale_M2_over_X4?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Denominator cases</span><strong>' + formatter.format(replay.denominator_cases || 0) + '</strong></div><div><span>First-jet Parseval</span><strong>' + (aggregate.centered_first_jet_parseval_identity_proved ? "proved" : "open") + '</strong></div><div><span>Uniform numerator saving</span><strong>' + (aggregate.uniform_all_numerator_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_active_contamination_rows || [];
    detail = [
      '<div class="poc-equation">A₂−π₂=L+R−B exactly, where L and R count active composite prime powers with a shift-two prime-power neighbor and B removes the double count. Inactive powers no longer enter the correction.</div>',
      table(["X", "contamination", "L", "R", "B", "active bound", "T247 bound", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        formatter.format(row.exact_contamination_A2_minus_pi2 || 0),
        formatter.format(row.left_active_composite_power_pairs_L || 0),
        formatter.format(row.right_active_composite_power_pairs_R || 0),
        formatter.format(row.both_composite_power_pairs_B || 0),
        formatter.format(row.active_union_bound_L_plus_R || 0),
        formatter.format(row.ticket247_sharp_bound || 0),
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Active identity</span><strong>' + (aggregate.active_contamination_identity_proved ? "proved" : "open") + '</strong></div><div><span>Inactive powers</span><strong>' + (aggregate.inactive_prime_powers_removed_from_correction ? "removed" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.unbounded_type_II_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket248-unweighted-wieferich-jet-active" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 248 unweighted moments, generalized-Wieferich separation, centered first jets, and active contamination</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three partial theorems and one exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket247-audit-table ticket248-audit-table">' + table(["TICKET248 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-248 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/unweighted-wieferich-jet-active.ko.md">한국어 보고서</a> · <a href="../docs/unweighted-wieferich-jet-active.md">English report</a> · <a href="../data/open-problem/ticket248-unweighted-wieferich-jet-active.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
