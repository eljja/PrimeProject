function renderTicket247HilbertHenselLipschitzPrimePower(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.hilbert_hensel_lipschitz_primepower_audit || {};
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
    const rows = computation.exact_legendre_certificates || [];
    detail = [
      '<div class="poc-equation">For f<sub>n</sub>=√((4n+1)/2)P<sub>2n</sub>, the first n even moments vanish and Q<sub>w</sub>(f<sub>n</sub>) is bounded by the summable feature tail. Every Hilbert-Schmidt weighted-moment coercivity constant is therefore zero.</div>',
      table(["n", "degree", "norm²", "dyadic tail bound", "moments zero", "verified"], rows.map((row) => [
        row.legendre_half_degree_n,
        row.polynomial_degree,
        row.unnormalized_L2_norm_squared?.exact,
        row.dyadic_weight_feature_tail_upper_bound?.exact,
        row.all_exact_moments_zero ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Hilbert-Schmidt coercivity</span><strong>' + (aggregate.hilbert_schmidt_weighted_moment_coercivity_refuted ? "refuted" : "open") + '</strong></div><div><span>Normalized weak sequence</span><strong>' + (aggregate.explicit_normalized_weak_sequence_proved ? "proved" : "open") + '</strong></div><div><span>Arithmetic Weil coercivity</span><strong>' + (aggregate.non_hilbert_schmidt_arithmetic_weil_coercivity_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_hensel_countermodels || [];
    const replay = computation.exact_modular_replay || {};
    detail = [
      '<div class="poc-equation">With U=3, V=5 is a simple root of P<sub>q</sub>(U,V) modulo every prime q&gt;5 because ∂P/∂V=−3(1+qV)². Its Hensel branch has v<sub>q</sub>(P) arbitrarily large while v<sub>q</sub>(U−V)=0.</div>',
      table(["q", "depth", "V mod q^depth", "P residue", "U−V mod q", "verified"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.lift_depth,
        row.lifted_V_mod_q_to_depth,
        row.P_q_mod_q_to_depth,
        row.U_minus_V_mod_q,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Primes replayed</span><strong>' + formatter.format(replay.primes_checked || 0) + '</strong></div><div><span>Formal domination</span><strong>' + (aggregate.formal_unrestricted_valuation_domination_refuted ? "refuted" : "open") + '</strong></div><div><span>Actual quotient exclusion</span><strong>' + (aggregate.actual_fermat_quotients_excluded_from_hensel_branch ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_selected_arc_rows || [];
    detail = [
      '<div class="poc-equation">At α=a/q+β, the rational-center residual bound gains exactly the deterministic displacement 2π|β|M. The family exp(2πiNβ)−1 proves that center values alone cannot give a frequency-uniform arc modulus.</div>',
      table(["X", "q", "prime mass", "first moment M", "φD", "M/X²", "verified"], rows.map((row) => [
        formatter.format(row.prime_limit_X || 0),
        row.denominator_q,
        formatter.format(row.unit_prime_mass || 0),
        formatter.format(row.unit_prime_first_moment_M || 0),
        row.residual_pointwise_squared_bound_phi_D,
        row.lipschitz_budget_M_abs_beta_without_2pi?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Center-to-arc bridge</span><strong>' + (aggregate.rational_center_arc_lipschitz_bridge_proved ? "proved" : "open") + '</strong></div><div><span>Center-only modulus</span><strong>' + (aggregate.center_only_uniform_modulus_refuted ? "refuted" : "open") + '</strong></div><div><span>Signed arc saving</span><strong>' + (aggregate.uniform_signed_first_moment_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_sharp_contamination_rows || [];
    detail = [
      '<div class="poc-equation">N<sub>odd</sub>(Y)=Σ<sub>k≥2</sub>π<sub>odd</sub>(⌊Y<sup>1/k</sup>⌋) exactly, and A₂−π₂≤2N<sub>odd</sub>. Splitting squares from all higher powers gives the sharper square/cube correction.</div>',
      table(["X", "contamination", "exact Nodd", "sharp bound", "old bound", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        formatter.format(row.composite_prime_power_contamination || 0),
        formatter.format(row.exact_odd_composite_prime_powers_N || 0),
        formatter.format(row.sharp_contamination_bound || 0),
        formatter.format(row.ticket246_exponent_blind_bound || 0),
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Exact power count</span><strong>' + (aggregate.exact_odd_composite_prime_power_formula_proved ? "proved" : "open") + '</strong></div><div><span>Sharp correction</span><strong>' + (aggregate.sharp_contamination_bound_proved ? "proved" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.scale_local_type_ii_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket247-hilbert-hensel-lipschitz-primepower" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 247 Hilbert-Schmidt no-go, Hensel countermodels, arc Lipschitz transfer, and sharp prime-power contamination</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-go results; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket247-audit-table">' + table(["TICKET247 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-247 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/hilbert-hensel-lipschitz-primepower.ko.md">한국어 보고서</a> · <a href="../docs/hilbert-hensel-lipschitz-primepower.md">English report</a> · <a href="../data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
