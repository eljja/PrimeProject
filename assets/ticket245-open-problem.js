function renderTicket245ClosureSecondOrderKleinLinnik(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.closure_second_order_klein_linnik_audit || {};
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
    const rows = computation.exact_exhaustion_margin_rows || [];
    detail = [
      '<div class="poc-equation">For f<sub>t</sub>=(t e<sub>0</sub>+e<sub>1</sub>)/√(1+t²), Q(f<sub>t</sub>)=t²/(1+t²). The jointly tight family is pointwise positive, while its closure contains f<sub>0</sub> with Q=0.</div>',
      table(["lower t", "exact class margin", "norm²", "support", "verified"], rows.map((row) => [
        row.compact_class_K_m_lower_t?.exact,
        row.exact_minimum_Q_on_K_m?.exact,
        row.normalized_L2_norm_squared?.exact,
        row.common_physical_support,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Closure zero-set criterion</span><strong>' + (aggregate.closure_zero_set_margin_criterion_proved ? "proved" : "open") + '</strong></div><div><span>Pointwise-to-uniform route</span><strong>' + (aggregate.joint_tightness_plus_pointwise_positivity_uniform_margin_refuted ? "refuted" : "open") + '</strong></div><div><span>Genuine Weil closure separation</span><strong>' + (aggregate.actual_weil_functional_zero_free_on_closure_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_exact_second_order_rows || [];
    const first = computation.adversarial_first_layer_scan || {};
    const second = computation.second_order_replay || {};
    detail = [
      '<div class="poc-equation">With U=(2<sup>q−1</sup>−1)/q and V=(3<sup>q−1</sup>−1)/q mod q², q³|(32<sup>q−1</sup>−27<sup>q−1</sup>) iff 5U−3V+q(10U²−3V²)=0 mod q²; q³|(2<sup>q−1</sup>−3<sup>q−1</sup>) iff U−V=0 mod q².</div>',
      table(["q", "U mod q²", "V mod q²", "bad first", "comparison first", "bad digit", "comparison digit"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.Qq2_mod_q_squared,
        row.Qq3_mod_q_squared,
        row.bad_line_first_layer ? "yes" : "no",
        row.comparison_line_first_layer ? "yes" : "no",
        row.bad_line_second_digit_mod_q_squared,
        row.comparison_second_digit_mod_q_squared,
      ])),
      '<div class="poc-head"><div><span>First-layer primes scanned</span><strong>' + formatter.format(first.primes_scanned || 0) + '</strong></div><div><span>Bad-line rows</span><strong>' + (first.bad_line_prime_count ?? "missing") + '</strong></div><div><span>q³ identity replays</span><strong>' + formatter.format(second.primes_scanned || 0) + '</strong></div></div>',
      '<div class="poc-head"><div><span>Second-order criterion</span><strong>' + (aggregate.exact_second_order_digit_criteria_proved ? "proved" : "open") + '</strong></div><div><span>All-prime depth domination</span><strong>' + (aggregate.all_depth_fixed_base_domination_proved ? "proved" : "open") + '</strong></div><div><span>Collatz</span><strong>open</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_rational_center_orbit_rows || [];
    detail = [
      '<div class="poc-equation">For even N, I(α+1/2)=I(α) and I(−α)=conj(I(α)). Four disjoint Klein images contribute exactly 4 Re∫<sub>E</sub>I, and every rational center has a representative in [0,1/4].</div>',
      table(["seed Q", "seeds", "closed centers", "quarter orbits", "size 2", "size 4", "max denominator"], rows.map((row) => [
        row.seed_denominator_limit_Q,
        formatter.format(row.reduced_rational_seed_count || 0),
        formatter.format(row.klein_closed_center_count || 0),
        formatter.format(row.canonical_quarter_torus_orbit_count || 0),
        row.orbit_size_two_count,
        formatter.format(row.orbit_size_four_count || 0),
        row.maximum_denominator_after_half_turn,
      ])),
      '<div class="poc-head"><div><span>Klein symmetry</span><strong>' + (aggregate.klein_four_integrand_symmetry_proved ? "proved" : "open") + '</strong></div><div><span>Quarter-torus reduction</span><strong>' + (aggregate.all_rational_centers_reduce_to_quarter_torus ? "proved" : "open") + '</strong></div><div><span>Signed residual saving</span><strong>' + (aggregate.signed_residual_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_polynomial_height_witness_rows || [];
    detail = [
      '<div class="poc-equation">For a fixed period M, two Bertrand primes force p+2 to have two factors in one reduced CRT class of modulus Q&lt;8M³. Linnik gives a prime mimic p≤CM<sup>3L</sup>.</div>',
      table(["M", "a", "ℓ₁", "ℓ₂", "Q", "prime p", "factorization of p+2"], rows.map((row) => [
        formatter.format(row.period_M || 0),
        row.admissible_residue_a,
        formatter.format(row.bertrand_prime_ell_1 || 0),
        formatter.format(row.bertrand_prime_ell_2 || 0),
        formatter.format(row.crt_modulus_Q || 0),
        formatter.format(row.first_prime_in_crt_class || 0),
        row.successor_factorization,
      ])),
      '<div class="poc-head"><div><span>Polynomial-height mimicry</span><strong>' + (aggregate.polynomial_height_periodic_mimicry_proved ? "proved" : "open") + '</strong></div><div><span>Global prefix period bound</span><strong>' + (aggregate.global_prefix_period_lower_bound_proved ? "proved" : "open") + '</strong></div><div><span>Scale-local nonperiodic Type II</span><strong>' + (aggregate.nonperiodic_type_ii_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket245-closure-second-order-klein-linnik" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 245 closure margins, second Fermat digits, Klein arc orbits, and Linnik-height mimicry</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-gos; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket245-audit-table">' + table(["TICKET245 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-245 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/closure-second-order-klein-linnik.ko.md">한국어 보고서</a> · <a href="../docs/closure-second-order-klein-linnik.md">English report</a> · <a href="../data/open-problem/ticket245-closure-second-order-klein-linnik.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
