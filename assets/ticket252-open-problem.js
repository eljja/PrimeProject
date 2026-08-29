function renderTicket252SparseMarginalZeroResidueLocal(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.sparse_marginal_zeroresidue_local_audit || {};
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
    const rows = computation.exact_sparse_projection_rows || [];
    detail = [
      '<div class="poc-equation">A positive self-adjoint noncompact sparse Fourier projection can still admit normalized packets with Q<sub>0</sub>+&#10216;P<sub>S</sub>g,g&#10217;&rarr;0; these abstract operator properties do not imply RH coercivity.</div>',
      table(["delta", "pairs below 1/delta", "projection upper", "Q0 upper", "combined upper", "verified"], rows.map((row) => [
        row.delta?.exact,
        row.sparse_frequency_pair_count_below_inverse_scale,
        row.proved_sparse_projection_energy_upper?.exact,
        row.proved_raw_moment_energy_upper?.exact,
        row.proved_combined_upper?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Projection escape</span><strong>' + (aggregate.zero_density_projection_escape_proved ? "proved" : "open") + '</strong></div><div><span>Nonmultiplication</span><strong>' + (aggregate.operator_nonmultiplication_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil kernel</span><strong>' + (aggregate.actual_weil_kernel_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_uniform_marginal_countermodel_rows || [];
    detail = [
      '<div class="poc-equation">The graphs (U,V)=(3t,5t) and (t,t) have identical uniform marginals, but separated slope [3:5] mass (q-1)/q and 0. Marginals alone cannot detect the canonical joint event.</div>',
      table(["q", "hit graph", "miss graph", "hit mass", "miss mass", "uniform marginals", "verified"], rows.map((row) => [
        row.prime_q,
        row.hit_graph,
        row.miss_graph,
        row.hit_graph_target_mass?.exact,
        row.miss_graph_target_mass?.exact,
        row.each_of_four_marginals_is_exactly_uniform ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>Exact joint detector:</strong> ' + escapeHtml(computation.canonical_exact_indicator || "missing") + '</p>',
      '<div class="poc-head"><div><span>Marginal no-go</span><strong>' + (aggregate.uniform_marginals_do_not_control_joint_slope_proved ? "proved" : "open") + '</strong></div><div><span>Joint characters</span><strong>' + (aggregate.joint_character_control_required ? "required" : "open") + '</strong></div><div><span>Canonical pair</span><strong>' + (aggregate.canonical_fixed_pair_distribution_controlled ? "controlled" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_zero_residue_criterion_rows || [];
    const compatible = rows.filter((row) => row.zero_residue_compatibility);
    detail = [
      '<div class="poc-equation">For cyclic coefficients c of (1-X)<sup>m</sup> modulo X<sup>q</sup>-1, a nonnegative integer vector N=c+t compatible with N<sub>0</sub>&isin;{0,1} exists iff c<sub>0</sub>-min(c)&le;1. Hence every 1&le;m&lt;q is excluded, but the criterion alone has a compatible tail.</div>',
      table(["q", "m", "c0-min(c)", "compatible", "shift", "vector", "verified"], rows.map((row) => [
        row.prime_modulus_q,
        row.exponent_m,
        row.c0_minus_min_c,
        row.zero_residue_compatibility ? "yes" : "no",
        row.compatible_uniform_shift ?? "-",
        row.compatible_nonnegative_integer_vector ? "[" + row.compatible_nonnegative_integer_vector.join(", ") + "]" : "-",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Criterion</span><strong>' + (aggregate.zero_residue_compatibility_iff_proved ? "iff proved" : "open") + '</strong></div><div><span>Compatible tail rows</span><strong>' + formatter.format(compatible.length) + '</strong></div><div><span>Actual prime counts</span><strong>' + (aggregate.actual_prime_count_vectors_fully_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_finite_modulus_rows || [];
    const external = computation.external_theorem || {};
    detail = [
      '<div class="poc-equation">For every fixed M and odd k&ge;3, choose primes p&equiv;-1 and r&equiv;1 (mod 8M). Then p<sup>k</sup>+2&equiv;r<sup>2m</sup> (mod M), so no fixed finite congruence list can exclude all right-even candidates.</div>',
      table(["M", "8M", "prime p", "prime r", "k", "m", "residual", "verified"], rows.map((row) => [
        row.modulus_M,
        row.combined_modulus_8M,
        row.prime_p_minus_one_class,
        row.prime_r_plus_one_class,
        row.odd_left_exponent_k,
        row.right_half_exponent_m,
        row.equation_residual_mod_M,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>External theorem boundary:</strong> ' + escapeHtml(external.name || "missing") + ' — ' + escapeHtml(external.statement_used || "") + '</p>',
      '<div class="poc-head"><div><span>Local solutions</span><strong>' + (aggregate.prime_residue_local_solutions_for_every_fixed_modulus_proved ? "proved" : "open") + '</strong></div><div><span>Finite congruence obstruction</span><strong>' + (aggregate.fixed_finite_congruence_obstruction_excluded ? "excluded" : "open") + '</strong></div><div><span>Global equation</span><strong>' + (aggregate.global_integer_equation_solved ? "solved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket252-sparse-marginal-zeroresidue-local" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-252 sparse projection, marginal blindness, zero-residue compatibility, and finite-congruence local solubility</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three exact no-go results and one partial theorem; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket252-audit-table">' + table(["TICKET252 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-252 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/sparse-marginal-zeroresidue-local.ko.md">한국어 보고서</a> · <a href="../docs/sparse-marginal-zeroresidue-local.md">English report</a> · <a href="../data/open-problem/ticket252-sparse-marginal-zeroresidue-local.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
