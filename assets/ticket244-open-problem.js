function renderTicket244JointTightnessHarmonicParityFoldPolylogMimicry(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.joint_tightness_harmonic_parity_fold_polylog_mimicry_audit || {};
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
    const rows = computation.exact_translation_bound_rows || [];
    detail = [
      '<div class="poc-equation">For bounded K⊂L²(R), uniform physical and Fourier tails are together equivalent to relative compactness. The exact translation estimate is ‖τ<sub>h</sub>f−f‖²≤R²h²B²+4ε; either tail condition alone fails.</div>',
      table(["R", "h", "Fourier tail ε", "translation bound²", "verified"], rows.map((row) => [
        row.frequency_radius_R,
        row.translation_h?.exact,
        row.uniform_frequency_tail_budget_epsilon?.exact,
        row.squared_L2_translation_bound?.exact,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Joint tightness ⇔ compactness</span><strong>' + (aggregate.joint_tightness_characterizes_relative_compactness ? "proved" : "open") + '</strong></div><div><span>Physical-only route</span><strong>' + (aggregate.physical_tightness_alone_refuted ? "refuted" : "open") + '</strong></div><div><span>Uniform signed Weil tail</span><strong>' + (aggregate.uniform_signed_guinand_weil_tail_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_exact_harmonic_rows || [];
    const replay = computation.bounded_harmonic_replay || {};
    detail = [
      '<div class="poc-equation">For q&gt;5, 2F<sub>q</sub>(2)=−H<sub>(q−1)/2</sub> and 3F<sub>q</sub>(3)=−2H<sub>⌊q/3⌋</sub>. Hence the fixed-base bad line is exactly 4H<sub>⌊q/3⌋</sub>=5H<sub>(q−1)/2</sub> mod q. This is a first q-adic layer only.</div>',
      table(["q", "Fq(2)", "Fq(3)", "H half", "H third", "bad line", "verified"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.fermat_quotient_Fq2,
        row.fermat_quotient_Fq3,
        row.half_harmonic_H_floor_q_over_2_mod_q,
        row.third_harmonic_H_floor_q_over_3_mod_q,
        row.rational_wieferich_bad_line ? "yes" : "no",
        row.harmonic_equivalences_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Primes replayed</span><strong>' + formatter.format(replay.primes_scanned || 0) + '</strong></div><div><span>Bad-line rows</span><strong>' + (replay.bad_line_count ?? "missing") + '</strong></div><div><span>Identity failures</span><strong>' + (replay.failure_count ?? "missing") + '</strong></div></div>',
      '<div class="poc-head"><div><span>Harmonic reduction</span><strong>' + (aggregate.lerch_harmonic_reduction_proved ? "proved" : "open") + '</strong></div><div><span>All-prime nonvanishing</span><strong>' + (aggregate.all_prime_harmonic_bad_line_nonvanishing_proved ? "proved" : "open") + '</strong></div><div><span>Collatz</span><strong>open</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_parity_fold_rows || [];
    detail = [
      '<div class="poc-equation">O<sub>X</sub>(α+1/2)=−O<sub>X</sub>(α). For even N, O<sub>X</sub>(α)²e(−Nα) is exactly half-periodic, and for N≥6 its coefficient equals the full-prime binary coefficient.</div>',
      table(["X", "odd primes", "even targets", "min ordered count", "coefficient failures", "phase failures"], rows.map((row) => [
        formatter.format(row.prime_cutoff_X || 0),
        formatter.format(row.odd_prime_count || 0),
        formatter.format(row.even_targets_6_through_X_checked || 0),
        row.minimum_ordered_odd_prime_representation_count,
        row.full_sum_vs_odd_sum_coefficient_failures,
        row.exact_half_turn_phase_failures,
      ])),
      '<div class="poc-head"><div><span>Exact parity fold</span><strong>' + (aggregate.even_binary_integrand_half_periodicity_proved ? "proved" : "open") + '</strong></div><div><span>Finite targets</span><strong>' + formatter.format(aggregate.finite_even_targets_checked || 0) + '</strong></div><div><span>Signed residual saving</span><strong>' + (aggregate.signed_residual_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.finite_polylog_period_witness_rows || [];
    detail = [
      '<div class="poc-equation">For every fixed A, even scale-varying periods M<sub>X</sub>≤(log₂X)<sup>A</sup> are mimicked in every sufficiently large [X,2X]. Bertrand gives ℓ<2M and Siegel–Walfisz is uniform for Q=Mℓ&lt;2(log₂X)<sup>2A</sup>.</div>',
      table(["M(X)", "ℓ(X)", "Q(X)", "X", "prime p", "composite p+2"], rows.map((row) => [
        formatter.format(row.scale_dependent_period_M_X || 0),
        formatter.format(row.bertrand_prime_ell_X || 0),
        formatter.format(row.combined_modulus_Q_X || 0),
        formatter.format(row.dyadic_block_start_X || 0),
        formatter.format(row.prime_mimic_p || 0),
        formatter.format(row.forced_composite_successor_p_plus_2 || 0),
      ])),
      '<div class="poc-head"><div><span>Polylog-period mimicry</span><strong>' + (aggregate.polylog_growing_period_every_large_dyadic_mimicry_proved ? "proved" : "open") + '</strong></div><div><span>Pure periodic route</span><strong>' + (aggregate.pure_polylog_periodic_classifier_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.scale_local_type_ii_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 244 joint tightness, harmonic bad line, parity folding, and polylog mimicry</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three partial theorems and one exact no-go; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket244-audit-table">' + table(["TICKET244 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-244 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/joint-tightness-harmonic-parity-fold-polylog-mimicry.ko.md">한국어 보고서</a> · <a href="../docs/joint-tightness-harmonic-parity-fold-polylog-mimicry.md">English report</a> · <a href="../data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
