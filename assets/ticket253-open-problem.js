function renderTicket253DensityCharacterPrefixLebesgue(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.density_character_prefix_lebesgue_audit || {};
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
    const rows = computation.exact_periodic_density_rows || [];
    detail = [
      '<div class="poc-equation">For the normalized Dirichlet packet D<sub>N</sub>, &#10216;P<sub>S</sub>D<sub>N</sub>,D<sub>N</sub>&#10217; is exactly #(S&cap;[-N,N])/(2N+1). Positive symmetric spectral density blocks this canonical interior-packet escape, but no actual Weil domination is proved.</div>',
      table(["N", "2N+1", "selected", "energy", "density", "error", "verified"], rows.map((row) => [
        row.dirichlet_half_bandwidth_N,
        row.frequency_count_2N_plus_1,
        row.selected_frequency_count,
        row.exact_projection_energy?.exact,
        row.limiting_spectral_density?.exact,
        row.exact_absolute_density_error?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Packet concentration</span><strong>' + (aggregate.dirichlet_packet_concentrates_at_interior_zero_proved ? "proved" : "open") + '</strong></div><div><span>Density identity</span><strong>' + (aggregate.projection_energy_equals_symmetric_frequency_density_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil domination</span><strong>' + (aggregate.actual_weil_form_dominates_projection ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_canonical_character_rows || [];
    detail = [
      '<div class="poc-equation">C<sub>q</sub>(D)=q-1 for D=0 and -1 otherwise, hence (1+C<sub>q</sub>(D))/q=1<sub>D=0</sub>. The complete h-sum reconstructs the canonical [3:5] event instead of smoothing it.</div>',
      table(["q", "Uq", "Vq", "Dq", "Cq(Dq)", "average", "separated hit", "verified"], rows.map((row) => [
        row.prime_q,
        row.canonical_U_q,
        row.canonical_V_q,
        row.slope_residue_D_q,
        row.complete_nontrivial_character_sum_exact_integer,
        row.full_orthogonality_average?.exact,
        row.separated_projective_slope_hit ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Exact indicator</span><strong>' + (aggregate.complete_character_sum_is_exact_indicator_proved ? "proved" : "open") + '</strong></div><div><span>Pointwise cancellation route</span><strong>' + (aggregate.generic_pointwise_character_cancellation_route_rejected ? "rejected" : "open") + '</strong></div><div><span>Cross-prime distribution</span><strong>' + (aggregate.cross_prime_distribution_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_compatible_tail_prefix_rows || [];
    detail = [
      '<div class="poc-equation">A zero-residue-compatible cyclotomic tail forces one total T=qt and therefore one residue vector: the first T primes. Actual realization is equivalent to that single exact prefix match.</div>',
      table(["q", "m", "T=qt", "L1 discrepancy", "Linf", "first mismatch", "match", "verified"], rows.map((row) => [
        row.prime_modulus_q,
        row.cyclotomic_exponent_m,
        row.forced_total_prime_count_qt,
        row.l1_discrepancy,
        row.linfinity_discrepancy,
        row.first_mismatch_residue,
        row.actual_prefix_match ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>(q,m)=(5,8) forced vector:</strong> [1, 76, 76, 1, 126] · <strong>L1 discrepancy:</strong> 142</p>',
      '<div class="poc-head"><div><span>Unique-prefix iff</span><strong>' + (aggregate.actual_realizability_iff_unique_prime_prefix_match_proved ? "proved" : "open") + '</strong></div><div><span>Selected tails</span><strong>' + formatter.format(aggregate.selected_compatible_tail_count || 0) + ' excluded</strong></div><div><span>All compatible tails</span><strong>' + (aggregate.all_compatible_tail_exponents_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_remaining_prime_exponent_rows || [];
    const external = computation.external_theorem || {};
    const scan = computation.finite_odd_exponent_factor_scan || {};
    detail = [
      '<div class="poc-equation">If p<sup>k</sup>+2=r<sup>2m</sup> with odd k&ge;3, every prime factor ell of k must be one of 84 primes 17&le;ell&le;911 with ell&equiv;13,17,19,23 (mod 24), and p<sup>k/ell</sup>&gt;10<sup>1000</sup>. The 84 cases remain open.</div>',
      table(["index", "prime exponent ell", "ell mod 24", "verified"], rows.map((row) => [
        row.candidate_index,
        row.prime_exponent_ell,
        row.residue_mod_24,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>External theorem boundary:</strong> ' + escapeHtml(external.name || "missing") + ' · <a href="' + escapeHtml(external.source || "#") + '">arXiv v2 primary source</a></p>',
      '<p><strong>Finite factor replay:</strong> ' + formatter.format(scan.tested_odd_exponent_count || 0) + ' odd k; ' + formatter.format(scan.allowed_exponent_count || 0) + ' supported on the 84-prime set; ' + formatter.format(scan.rejected_exponent_count || 0) + ' rejected.</p>',
      '<div class="poc-head"><div><span>Remaining prime exponents</span><strong>' + formatter.format(aggregate.remaining_prime_exponent_count || 0) + '</strong></div><div><span>Factor reduction</span><strong>' + (aggregate.all_prime_factors_of_k_restricted_to_remaining_set ? "proved" : "open") + '</strong></div><div><span>Global equation</span><strong>' + (aggregate.global_integer_equation_solved ? "solved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket253-density-character-prefix-lebesgue" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-253 density packets, character dichotomy, forced prime prefixes, and the 84-exponent frontier</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three partial theorems and one exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket253-audit-table">' + table(["TICKET253 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-253 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/density-character-prefix-lebesgue.ko.md">한국어 보고서</a> · <a href="../docs/density-character-prefix-lebesgue.md">English report</a> · <a href="../data/open-problem/ticket253-density-character-prefix-lebesgue.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
