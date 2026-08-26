function renderTicket250MultiplierLiftGaloisEvenRight(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.multiplier_lift_galois_evenright_audit || {};
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
    const legendre = computation.exact_legendre_multiplier_rows || [];
    const concentration = computation.exact_concentration_escape_rows || [];
    detail = [
      '<div class="poc-equation">M<sub>x²</sub> is noncompact and ⟨M<sub>x²</sub>φ<sub>2n</sub>,φ<sub>2n</sub>⟩→1/2, but centered indicators have Q<sub>0</sub>+⟨M<sub>x²</sub>·,·⟩→0. Legendre-only validation cannot certify coercivity.</div>',
      table(["n", "degree", "expectation", "distance from 1/2", "verified"], legendre.map((row) => [
        row.half_degree_n,
        row.legendre_degree,
        row.exact_M_x2_expectation?.exact,
        row.exact_distance_from_one_half?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["epsilon", "Q0 upper", "multiplier", "combined upper", "verified"], concentration.map((row) => [
        row.epsilon?.exact,
        row.proved_Q0_upper_bound?.exact,
        row.exact_M_x2_energy?.exact,
        row.proved_combined_upper_bound?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Noncompact</span><strong>' + (aggregate.multiplier_M_x2_noncompact_proved ? "proved" : "open") + '</strong></div><div><span>Concentration escape</span><strong>' + (aggregate.concentration_escape_for_Q0_plus_multiplier_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil form</span><strong>' + (aggregate.actual_weil_form_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_lift_field_rows || [];
    detail = [
      '<div class="poc-equation">F<sub>q</sub>(a+kq)=F<sub>q</sub>(a)-k/a mod q. The two-coordinate lift action is transitive, and every fiber contains exactly q−1 nonzero representatives of projective slope [3:5].</div>',
      table(["q", "lift pairs", "image", "[3:5] hits", "expected", "verified"], rows.map((row) => [
        row.prime_q,
        formatter.format(row.lift_pairs_checked || 0),
        formatter.format(row.fermat_coordinate_pairs_reached || 0),
        row.separated_projective_lift_pairs,
        row.expected_separated_pairs,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Lift pairs</span><strong>' + formatter.format(audit.machine_audit?.collatz_lift_pair_count || 0) + '</strong></div><div><span>Local avoidance</span><strong>' + (aggregate.lift_invariant_local_avoidance_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Canonical representatives</span><strong>' + (aggregate.canonical_fixed_representative_occurrence_decided ? "decided" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_prime_count_norm_rows || [];
    const boundaries = computation.exact_boundary_countermodels || [];
    detail = [
      '<div class="poc-equation">At prime q≥5, every nonconstant rational residue vector has full reduced Fourier support. The product over all reduced frequencies is a nonzero integer Galois norm.</div>',
      table(["X", "q", "nonconstant", "support", "expected", "|norm|", "verified"], rows.map((row) => [
        formatter.format(row.prime_count_limit_X || 0),
        row.prime_modulus_q,
        row.vector_nonconstant ? "yes" : "no",
        row.all_nonzero_frequencies_proved_by_minimal_polynomial ? row.prime_modulus_q - 1 : 0,
        row.prime_modulus_q - 1,
        row.exact_galois_norm,
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["boundary q", "vector", "support", "meaning"], boundaries.map((row) => [
        row.modulus_q,
        "[" + (row.centered_vector || []).join(", ") + "]",
        "[" + (row.nonzero_frequency_support || []).join(", ") + "]",
        row.interpretation,
      ])),
      '<div class="poc-head"><div><span>Exact norm cases</span><strong>' + formatter.format(audit.machine_audit?.goldbach_prime_count_norm_case_count || 0) + '</strong></div><div><span>Full support</span><strong>' + (aggregate.prime_modulus_rational_full_support_proved ? "proved" : "open") + '</strong></div><div><span>Quantitative saving</span><strong>' + (aggregate.quantitative_pointwise_upper_anti_concentration_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_scale_rows || [];
    const witnesses = computation.selected_even_left_witnesses || [];
    detail = [
      '<div class="poc-equation">For odd primes p,r, p<sup>2m</sup>+2=r<sup>ℓ</sup> with ℓ≥2 has the unique solution 25+2=27. The D=2 Lebesgue–Nagell classification is an explicit external theorem dependency.</div>',
      table(["X", "R", "even-left", "odd-left", "verified"], rows.map((row) => [
        formatter.format(row.limit_X || 0),
        row.right_active_composite_pairs_R,
        row.right_active_even_left_exponent,
        row.right_active_odd_left_exponent,
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["n", "n+2", "left", "right", "verified"], witnesses.map((row) => [
        row.n,
        row.n_plus_2,
        row.left_base + "^" + row.left_exponent,
        row.right_base + "^" + row.right_exponent,
        row.classification_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Even-left class</span><strong>' + (aggregate.all_base_even_left_right_active_classification_proved ? "classified" : "open") + '</strong></div><div><span>Unique pair</span><strong>' + (aggregate.unique_pair || []).join("→") + '</strong></div><div><span>Odd-left class</span><strong>' + (aggregate.odd_left_right_active_contamination_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket250-multiplier-lift-galois-evenright" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-250 multiplier escape, lift transitivity, Galois support, and even-left classification</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-go results; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket249-audit-table ticket250-audit-table">' + table(["TICKET250 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-250 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/multiplier-lift-galois-evenright.ko.md">한국어 보고서</a> · <a href="../docs/multiplier-lift-galois-evenright.md">English report</a> · <a href="../data/open-problem/ticket250-multiplier-lift-galois-evenright.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
