function renderTicket251InteriorCrtCyclotomicRightEven(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.interior_crt_cyclotomic_righteven_audit || {};
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
    const rows = computation.exact_interior_concentration_rows || [];
    detail = [
      '<div class="poc-equation">Every continuous even nonnegative local multiplier with an interior zero admits normalized symmetric concentrations for which Q<sub>0</sub>+⟨M<sub>w</sub>·,·⟩→0.</div>',
      table(["delta", "support", "rho", "multiplier upper", "Q0 upper", "combined", "verified"], rows.map((row) => [
        row.delta?.exact,
        row.symmetric_support_measure?.exact,
        row.support_radius_rho?.exact,
        row.proved_multiplier_energy_upper?.exact,
        row.proved_raw_moment_energy_upper?.exact,
        row.proved_combined_upper?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Interior-zero class</span><strong>' + (aggregate.all_continuous_even_nonnegative_interior_zero_multipliers_excluded ? "excluded" : "open") + '</strong></div><div><span>Noncompactness</span><strong>' + (aggregate.noncompactness_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil form</span><strong>' + (aggregate.actual_weil_form_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_CRT_interpolation_rows || [];
    detail = [
      '<div class="poc-equation">F<sub>q</sub>(a+kq)=F<sub>q</sub>(a)−k/a mod q and CRT interpolate arbitrary target pairs over every finite prime set. This does not control the canonical fixed pair 2,3.</div>',
      table(["case", "primes", "target", "M", "A", "B", "verified"], rows.map((row) => [
        row.case,
        (row.prime_set || []).join(", "),
        "[" + (row.common_target_pair || []).join(", ") + "]",
        row.CRT_modulus,
        row.least_nonnegative_A,
        row.least_nonnegative_B,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>CRT cases</span><strong>' + formatter.format(audit.machine_audit?.collatz_CRT_case_count || 0) + '</strong></div><div><span>Finite patterns</span><strong>' + (aggregate.arbitrary_finite_prime_patterns_interpolated ? "interpolated" : "open") + '</strong></div><div><span>Canonical pair</span><strong>' + (aggregate.canonical_fixed_pair_distribution_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_cyclotomic_unit_rows || [];
    detail = [
      '<div class="poc-equation">F<sub>m</sub>(a)=q(1−ζ<sub>q</sub><sup>a</sup>)<sup>m</sup> has full support and norm q<sup>q−1+m</sup>, yet its energy concentrates on the maximal conjugate pair as m→∞.</div>',
      table(["q", "m", "counts n", "exact norm", "outside/pair upper", "verified"], rows.map((row) => [
        row.prime_modulus_q,
        row.exponent_m,
        "[" + (row.nonnegative_counts_n || []).join(", ") + "]",
        row.exact_galois_norm,
        Number(row.outside_pair_to_max_pair_energy_upper_display || 0).toExponential(4),
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Cyclotomic cases</span><strong>' + formatter.format(audit.machine_audit?.goldbach_cyclotomic_case_count || 0) + '</strong></div><div><span>Structural anti-concentration</span><strong>' + (aggregate.structural_only_quantitative_anti_concentration_refuted ? "refuted" : "open") + '</strong></div><div><span>Actual prime counts</span><strong>' + (aggregate.actual_prime_count_vectors_excluded_from_family ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_scale_rows || [];
    const witnesses = (computation.selected_witnesses || []).slice(0, 16);
    detail = [
      '<div class="poc-equation">For odd primes p,r, p<sup>k</sup>+2=r<sup>2m</sup> implies k odd and p≡7 (mod 8). Conversely those conditions are congruence-compatible, so modulo 8 alone cannot force k=1.</div>',
      table(["X", "right-even pairs", "composite-left", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        row.right_even_active_pair_count,
        row.left_exponent_at_least_two_count,
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["p", "r^(2m)", "left exponent", "right base/exponent", "verified"], witnesses.map((row) => [
        row.p_power,
        row.right_even_power,
        row.left_exponent_k,
        row.right_prime_r + "^" + row.right_exponent_2m,
        row.classification_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Modulo-eight constraint</span><strong>' + (aggregate.right_even_modulo_eight_constraint_proved ? "proved" : "open") + '</strong></div><div><span>Composite-left witnesses ≤10M</span><strong>' + formatter.format(aggregate.finite_scan_composite_left_witness_count || 0) + ' (finite)</strong></div><div><span>All-X Diophantine exclusion</span><strong>open</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket251-interior-crt-cyclotomic-righteven" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-251 interior concentration, finite-prime CRT, cyclotomic concentration, and a right-even modulo-eight constraint</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three exact no-go results and one partial theorem; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket251-audit-table">' + table(["TICKET251 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-251 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/interior-crt-cyclotomic-righteven.ko.md">한국어 보고서</a> · <a href="../docs/interior-crt-cyclotomic-righteven.md">English report</a> · <a href="../data/open-problem/ticket251-interior-crt-cyclotomic-righteven.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
