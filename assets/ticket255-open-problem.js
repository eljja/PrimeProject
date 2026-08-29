function renderTicket255AggregateIncompleteOddLocal(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.aggregate_incomplete_odd_local_audit || {};
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
    const rows = computation.exact_positive_block_rows || [];
    detail = [
      '<div class="poc-equation">A<sub>L</sub>=J<sub>L</sub>+I<sub>L</sub>/L is positive definite and its normalized all-ones packet has energy L+1/L, but 1+1/L≤L-1 for L≥3. Strict diagonal dominance is sufficient at best, not necessary.</div>',
      table(["L", "diagonal", "off-diagonal row sum", "orthogonal eigenvalue", "packet energy", "strict DD", "verified"], rows.map((row) => [
        row.block_dimension_L,
        row.diagonal_entry?.exact,
        row.absolute_off_diagonal_row_sum?.exact,
        row.orthogonal_complement_eigenvalue?.exact,
        row.normalized_dirichlet_packet_energy?.exact,
        row.strictly_diagonally_dominant ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Positive blocks</span><strong>' + (aggregate.positive_definite_for_every_L_at_least_three ? "proved" : "open") + '</strong></div><div><span>Strict-DD necessity</span><strong>' + (aggregate.strict_diagonal_dominance_necessary ? "open" : "rejected") + '</strong></div><div><span>Actual Weil form</span><strong>' + (aggregate.actual_weil_form_analyzed ? "analyzed" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.exact_missing_fourier_coefficient_rows || [];
    detail = [
      '<div class="poc-equation">The point mass at zero has Fourier coefficient 1/q at every frequency. A proper frequency support misses h₀ and has coefficient 0 there, so no signed or complex incomplete sum can recover incidence exactly on all residues.</div>',
      table(["q", "support", "|H|", "missing h₀", "target coefficient", "H-supported coefficient", "verified"], rows.map((row) => [
        row.prime_q,
        row.support_family,
        row.support_size,
        row.missing_frequency_h0,
        row.delta_zero_fourier_coefficient_at_h0?.exact,
        row.any_H_supported_sum_coefficient_at_h0?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Exact replay</span><strong>' + formatter.format(aggregate.exact_replay_case_count || 0) + '</strong></div><div><span>Incomplete exact recovery</span><strong>' + (aggregate.proper_incomplete_support_exact_recovery_possible ? "open" : "impossible") + '</strong></div><div><span>Approximate recovery</span><strong>' + (aggregate.approximate_or_canonical_only_recovery_rejected ? "rejected" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_odd_reflection_prefix_exclusion_rows || [];
    detail = [
      '<div class="poc-equation">For odd m with q∤m, cyclic reflection gives c<sub>m mod q</sub>=-c<sub>0</sub>, forcing 2t-1 primes in that residue. If the first T=qt primes stop before that residue occurrence, the unique prefix is impossible.</div>',
      table(["q", "m", "t", "T", "forced", "actual", "lambda index", "excluded", "verified"], rows.map((row) => [
        row.prime_modulus_q,
        row.odd_cyclotomic_exponent_m,
        String(row.forced_uniform_shift_t),
        String(row.forced_total_prime_count_T),
        String(row.forced_count_at_m_mod_q_2t_minus_1),
        row.actual_first_T_prime_count_at_m_mod_q,
        row.global_index_lambda_of_forced_count_th_residue_prime,
        row.unique_prime_prefix_excluded ? "yes" : "no",
        row.certificate_verified ? "yes" : "no",
      ])),
      '<p><strong>Finite boundary:</strong> ' + formatter.format(aggregate.scanned_odd_pair_count || 0) + ' odd pairs scanned; ' + formatter.format(aggregate.compatible_non_q_divisible_odd_pair_count || 0) + ' compatible rows; ' + formatter.format(aggregate.finite_prefix_certificate_count || 0) + ' rows below T≤50,000 enumerated and excluded.</p>',
      '<div class="poc-head"><div><span>Odd reflection</span><strong>' + (aggregate.odd_reflection_identity_proved ? "proved" : "open") + '</strong></div><div><span>Replayed rows</span><strong>' + (aggregate.all_replayed_pairs_excluded ? "excluded" : "open") + '</strong></div><div><span>q-divisible tails</span><strong>' + (aggregate.q_divisible_compatible_tails_excluded ? "excluded" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_split_prime_local_obstruction_rows || [];
    const witnesses = computation.surviving_twist_integer_witnesses || [];
    detail = [
      '<div class="poc-equation">At the split primes 103, 137, and 409, exact seventeenth-power convolution covers 15 of the 17 coefficient-one Thue twists. Only j=1 and j=16 survive; both have global B<sub>j</sub>=1 witnesses with reduced y=-1, so coefficient-only congruences cannot finish them.</div>',
      table(["p", "sqrt(2)", "obstructed twists", "cumulative survivors", "represented pairs/twist", "verified"], rows.map((row) => [
        row.split_prime_p,
        row.least_square_root_s_of_two_mod_p,
        (row.locally_obstructed_twists || []).join(", "),
        (row.cumulative_surviving_twists || []).join(", "),
        formatter.format(row.represented_uv_residue_pairs_per_twist || 0),
        row.certificate_verified ? "yes" : "no",
      ])),
      table(["j", "u", "v", "A", "B", "reduced y", "admissible"], witnesses.map((row) => [
        row.unit_twist_j, row.u, row.v, row.A_j_u_v, row.B_j_u_v, row.reduced_y,
        row.admissible_positive_point ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Locally excluded</span><strong>' + formatter.format(aggregate.locally_excluded_twist_count || 0) + ' / 17</strong></div><div><span>Survivors</span><strong>' + (aggregate.surviving_twists || []).join(", ") + '</strong></div><div><span>Survivors globally solved</span><strong>' + (aggregate.surviving_twists_globally_solved ? "yes" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket255-aggregate-incomplete-odd-local" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>TICKET-255 aggregate packets, incomplete recovery, odd reflection, and a three-prime Thue obstruction</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>two partial theorems and two exact no-gos; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket250-audit-table ticket254-audit-table">' + table(["TICKET255 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-255 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/aggregate-incomplete-odd-local.ko.md">한국어 보고서</a> · <a href="../docs/aggregate-incomplete-odd-local.md">English report</a> · <a href="../data/open-problem/ticket255-aggregate-incomplete-odd-local.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
