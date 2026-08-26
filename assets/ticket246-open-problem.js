function renderTicket246MomentAllDepthParsevalPrimePower(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.moment_alldepth_parseval_primepower_audit || {};
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
    const rows = computation.exact_finite_difference_moment_rows || [];
    detail = [
      '<div class="poc-equation">For c<sub>j</sub>=(−1)<sup>j</sup>C(2m,j), the 2m-th finite difference annihilates every even-moment polynomial of degree below 2m. Thus the normalized shell sum has its first m even moments exactly zero.</div>',
      table(["m", "shell dimension", "difference order", "norm²", "support", "verified"], rows.map((row) => [
        row.moment_count_m,
        row.shell_dimension,
        row.finite_difference_order,
        formatter.format(row.unnormalized_L2_norm_squared || 0),
        row.common_compact_support,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>All-m annihilator</span><strong>' + (aggregate.all_finite_moment_annihilators_verified ? "proved" : "open") + '</strong></div><div><span>Finite-moment separation</span><strong>' + (aggregate.finite_even_moment_zero_separation_refuted ? "refuted" : "open") + '</strong></div><div><span>Genuine Weil coercivity</span><strong>' + (aggregate.actual_admissible_weil_infinite_feature_coercivity_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_all_depth_rows || [];
    const replay = computation.exact_modular_replay || {};
    detail = [
      '<div class="poc-equation">With U=(2<sup>q−1</sup>−1)/q and V=(3<sup>q−1</sup>−1)/q, the exact finite polynomial P<sub>q</sub>=5U−3V+q(10U²−3V²)+q²(10U³−V³)+5q³U⁴+q⁴U⁵ satisfies 32<sup>q−1</sup>−27<sup>q−1</sup>=qP<sub>q</sub>.</div>',
      table(["q", "U mod q⁵", "V mod q⁵", "Pq mod q⁵", "bad valuation", "comparison valuation"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.U_mod_q_to_fifth,
        row.V_mod_q_to_fifth,
        row.P_q_mod_q_to_fifth,
        row.bad_difference_q_adic_valuation_capped_at_six,
        row.comparison_difference_q_adic_valuation_capped_at_six,
      ])),
      '<div class="poc-head"><div><span>Primes replayed</span><strong>' + formatter.format(replay.primes_scanned || 0) + '</strong></div><div><span>All-depth identity</span><strong>' + (aggregate.exact_all_depth_polynomial_identity_proved ? "proved" : "open") + '</strong></div><div><span>All-prime domination</span><strong>' + (aggregate.all_prime_valuation_domination_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_selected_residue_variance_rows || [];
    detail = [
      '<div class="poc-equation">At a rational center a/q, the coprime odd-prime sum is its Ramanujan mean plus R(a), and Σ<sub>a mod q</sub>|R(a)|²=qΣ<sub>r∈(Z/qZ)*</sub>δ<sub>r</sub>² exactly.</div>',
      table(["X", "q", "φ(q)", "prime mass", "relative variance", "Parseval energy", "verified"], rows.map((row) => [
        formatter.format(row.prime_limit_X || 0),
        row.denominator_q,
        row.phi_q,
        formatter.format(row.unit_prime_mass || 0),
        row.relative_variance_V?.exact,
        row.parseval_residual_energy?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Center Parseval</span><strong>' + (aggregate.exact_residual_parseval_identity_proved ? "proved" : "open") + '</strong></div><div><span>Growing-q decay</span><strong>' + (aggregate.uniform_growing_denominator_variance_decay_proved ? "proved" : "open") + '</strong></div><div><span>Arc stability</span><strong>' + (aggregate.representative_arc_stability_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_prime_power_proxy_rows || [];
    detail = [
      '<div class="poc-equation">For odd starts n≥3, 0≤A₂(X)−π₂(X)≤2(⌊log₂(X+2)⌋−1)⌊√(X+2)⌋. The uncorrected equality is refuted by the minimal odd false pair (7,9=3²).</div>',
      table(["X", "prime-power pairs", "twin pairs", "contamination", "composite powers", "bound B"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        formatter.format(row.prime_power_pair_count_A2 || 0),
        formatter.format(row.twin_prime_pair_count_pi2 || 0),
        formatter.format(row.composite_prime_power_contamination || 0),
        formatter.format(row.composite_prime_powers_through_X_plus_2 || 0),
        formatter.format(row.explicit_contamination_bound_B || 0),
      ])),
      '<div class="poc-head"><div><span>Contamination bound</span><strong>' + (aggregate.prime_power_proxy_contamination_bound_proved ? "proved" : "open") + '</strong></div><div><span>Uncorrected equality</span><strong>' + (aggregate.uncorrected_prime_power_proxy_equality_refuted ? "refuted" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.scale_local_type_ii_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket246-moment-alldepth-parseval-primepower" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 246 finite-moment annihilators, all-depth Fermat polynomials, rational-center Parseval, and prime-power contamination</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three partial theorems and one exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket246-audit-table">' + table(["TICKET246 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-246 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/moment-alldepth-parseval-primepower.ko.md">한국어 보고서</a> · <a href="../docs/moment-alldepth-parseval-primepower.md">English report</a> · <a href="../data/open-problem/ticket246-moment-alldepth-parseval-primepower.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
