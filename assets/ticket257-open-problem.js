function renderTicket257SpikeCyclotomicCharacterRoot(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.spike_cyclotomic_character_root_audit || {};
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
    const rows = computation.exact_sparse_spike_rows || [];
    detail = [
      '<div class="poc-equation">Prescribe E<sub>4<sup>k</sup></sub>=1-2<sup>-k</sup> and E<sub>L</sub>=1 otherwise. Then E<sub>L</sub>→1 while S<sub>4<sup>k</sup>-1</sub>=1-2<sup>k</sup>→-∞. Positivity plus convergence is insufficient.</div>',
      table(["k", "L=4^k", "E_L", "S_(L-1)", "direct replay", "verified"], rows.map((row) => [row.spike_level_k, row.packet_dimension_L_equals_4_power_k, row.packet_energy_E_L?.exact, row.symmetric_lag_partial_sum_S_L_minus_1?.exact, row.direct_energy_from_reconstructed_lags?.exact, row.identity_verified ? "yes" : "no"])),
      '<div class="poc-head"><div><span>Abstract route</span><strong>' + (aggregate.positivity_and_convergence_only_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Variation repair</span><strong>' + (aggregate.scaled_downward_variation_repair_proved ? "proved" : "open") + '</strong></div><div><span>Actual Weil packets</span><strong>' + (aggregate.actual_weil_packet_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_canonical_phase_prefix_rows || [];
    detail = [
      '<div class="poc-equation">For distinct odd primes q<sub>j</sub>, Σ ζ<sub>qj</sub><sup>dj</sup> never vanishes. Cyclotomic linear disjointness rules out exact finite phase grouping, but gives no sublinear magnitude bound.</div>',
      table(["prefix", "q", "Fq(2)", "Fq(3)", "Dq", "primitive", "exact zero"], rows.map((row) => [row.prefix_length, row.prime_q, row.fermat_quotient_F_q_2, row.fermat_quotient_F_q_3, row.canonical_phase_exponent_D_q, row.phase_is_primitive_qth_root ? "yes" : "no", row.finite_prefix_exact_zero_impossible ? "impossible" : "open"])),
      '<div class="poc-head"><div><span>Canonical rows</span><strong>' + formatter.format(aggregate.prime_count || 0) + '</strong></div><div><span>Finite exact zero</span><strong>' + (aggregate.every_finite_distinct_prime_phase_sum_nonzero_proved ? "impossible" : "open") + '</strong></div><div><span>Sublinear phase sum</span><strong>' + (aggregate.sublinear_phase_sum_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_reflection_character_certificate_rows || [];
    detail = [
      '<div class="poc-equation">Reflection symmetry forces the Legendre product χ<sub>q</sub>(-1)<sup>(T-1)/2</sup>. All odd character moments characterize symmetry; the q=11, m=22 prefix violates the quadratic condition.</div>',
      table(["q", "m", "T", "last prime", "actual counts", "product", "expected", "excluded"], rows.map((row) => [row.prime_q, row.exponent_m, formatter.format(row.prime_prefix_length_T), formatter.format(row.last_prime_in_prefix), (row.actual_prime_residue_counts || []).join(", "), row.actual_quadratic_character_product_mod_q, row.reflection_symmetric_expected_product_mod_q, row.quadratic_character_certificate_excludes_prefix ? "yes" : "no"])),
      '<p><strong>Adversarial boundary:</strong> q=5 and q=7 are asymmetric but pass the one-bit quadratic test. It is sufficient, not complete.</p>',
      '<div class="poc-head"><div><span>q=11 certificate</span><strong>' + (aggregate.new_q11_m22_prefix_excluded ? "excluded" : "open") + '</strong></div><div><span>Odd-character criterion</span><strong>' + (aggregate.all_odd_character_moments_characterize_symmetry_proved ? "proved" : "open") + '</strong></div><div><span>Universal prefix claim</span><strong>' + (aggregate.all_compatible_even_q_divisible_prefixes_excluded ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const bracket = computation.exact_root_bracket || {};
    const finite = computation.finite_denominator_audit || {};
    const samples = computation.exact_candidate_sample_rows || [];
    detail = [
      '<div class="poc-equation">The coefficient form B<sub>1</sub>(u,v)=1 has one real root direction ρ. Every nonzero-v solution must be the unique root neighbor, reducing a 2D box to a 1D sequence.</div>',
      table(["|v|", "positive-v neighbors", "reflected neighbors"], samples.map((row) => [formatter.format(row.absolute_denominator_v), (row.positive_v_candidate_values || []).map((item) => `${item.u}: ${item.B_1}`).join(" · "), (row.negative_v_reflected_candidate_values || []).map((item) => `${item.x_equals_minus_u}: ${item.B_1_x_positive_v}`).join(" · ")])),
      '<p><strong>Exact root bracket:</strong> ' + escapeHtml(bracket.lower?.exact || "missing") + ' &lt; ρ &lt; ' + escapeHtml(bracket.upper?.exact || "missing") + '. <strong>Finite replay:</strong> ' + formatter.format(finite.candidate_evaluation_count || 0) + ' candidates through 0&lt;|v|≤' + formatter.format(finite.absolute_v_limit || 0) + '; ' + formatter.format((finite.nonzero_v_coefficient_one_hits || []).length) + ' nonzero-v hits.</p>',
      '<div class="poc-head"><div><span>Root-neighbor reduction</span><strong>' + (aggregate.all_integral_solutions_reduce_to_unique_root_neighbors_proved ? "proved" : "open") + '</strong></div><div><span>Primitive divisibility</span><strong>' + (aggregate.primitive_double_divisibility_conditions_proved ? "proved" : "open") + '</strong></div><div><span>All denominators</span><strong>' + (aggregate.single_absolute_branch_globally_solved ? "solved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket257-spike-cyclotomic-character-root" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-257 sparse spikes, cyclotomic noncancellation, Goldbach characters, and a Twin root-neighbor reduction</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>2 exact no-gos + 2 partial theorems; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table ticket256-audit-table ticket257-audit-table">' + table(["TICKET257 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-257 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/spike-cyclotomic-character-root.ko.md">한국어 보고서</a> · <a href="../docs/spike-cyclotomic-character-root.md">English report</a> · <a href="../data/open-problem/ticket257-spike-cyclotomic-character-root.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
