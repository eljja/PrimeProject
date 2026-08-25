function renderTicket239CancellationLiftingFourierCRT(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.cancellation_lifting_fourier_crt_audit || {};
  const section = ({
    riemann: audit.riemann,
    collatz: audit.collatz,
    goldbach: audit.goldbach,
    "twin-prime": audit.twin_prime,
  })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || attempt.proof_dag || {};
  let detail = "";

  if ((attempt.problem_id || problemId) === "riemann") {
    const sufficient = computation.exact_summable_power_decay_rows || [];
    const noGo = computation.exact_nonsummable_positive_mixture_rows || [];
    detail = [
      '<div class="poc-equation">2Cζ(α)&lt;1 with α&gt;1 is sufficient. It is not necessary: G<sub>J</sub>=(1−C)I+C[(1+|i−j|)<sup>−α</sup>] stays ⪰(1−C)I for 0&lt;α≤1 although absolute row sums diverge.</div>',
      table(["J", "α", "row-sum η", "Schur lower bound"], sufficient.map((row) => [
        row.shell_count_J,
        row.power_decay_alpha,
        row.maximum_absolute_cross_row_sum_eta_J?.exact,
        row.row_sum_certified_lower_bound?.exact,
      ])),
      table(["J", "α", "row-sum η", "positive lower bound", "row-sum test"], noGo.map((row) => [
        row.shell_count_J,
        row.power_decay_alpha,
        row.maximum_absolute_cross_row_sum_eta_J?.exact,
        row.integral_mixture_uniform_lower_bound?.exact,
        row.absolute_row_sum_certificate_passes ? "passes" : "fails",
      ])),
      '<div class="poc-head"><div><span>Power-decay threshold</span><strong>' + (aggregate.power_decay_schur_threshold_proved ? "proved" : "open") + '</strong></div><div><span>Absolute-sum necessity</span><strong>' + (aggregate.absolute_row_sum_necessity_refuted ? "refuted" : "open") + '</strong></div><div><span>Arithmetic cancellation</span><strong>' + (aggregate.arithmetic_weil_cancellation_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if ((attempt.problem_id || problemId) === "collatz") {
    const rows = computation.representative_local_lifting_rows || [];
    const scan = computation.bounded_exception_scan || {};
    detail = [
      '<div class="poc-equation">For ℓ<sub>q</sub>=lcm(ord<sub>q</sub>(32/27),ord<sub>q</sub>(2/3)), LTE gives v<sub>q</sub>(D<sub>ℓn</sub>)−v<sub>q</sub>(B<sub>ℓn</sub>)=a<sub>q</sub>−c<sub>q</sub>. A prime is enabled for every multiple or disabled for every multiple.</div>',
      table(["q", "ℓq", "a_q", "c_q", "defect"], rows.map((row) => [
        row.prime_q,
        row.local_common_period_ell_q,
        row.depth_a_q,
        row.depth_c_q,
        row.lifting_defect_delta_q,
      ])),
      '<div class="poc-head"><div><span>Lifting dichotomy</span><strong>' + (aggregate.local_lifting_defect_dichotomy_proved ? "proved" : "open") + '</strong></div><div><span>Odd primes scanned</span><strong>' + formatter.format(scan.odd_primes_scanned || 0) + '</strong></div><div><span>Positive defects found</span><strong>' + (scan.positive_lifting_defect_count ?? "missing") + '</strong></div></div>',
    ].join("");
  } else if ((attempt.problem_id || problemId) === "goldbach") {
    const rows = computation.exact_mesoscopic_prime_window_rows || [];
    detail = [
      '<div class="poc-equation">R<sub>A</sub>(h)=M<sup>−1</sup>Σ<sub>j</sub>P<sub>A</sub>(ω<sup>j</sup>)<sup>2</sup>ω<sup>−jh</sup>. Parseval fixes total L2 energy, not this signed reflected coefficient.</div>',
      table(["X", "buffer h", "|A|", "R_A(h)", "DC", "signed nonzero phase"], rows.map((row) => [
        formatter.format(row.cutoff_X || 0),
        row.even_buffer_h,
        row.prime_window_cardinality_m,
        row.ordered_reflection_count_R_A_h,
        row.dc_phase_term_m_squared_over_M?.exact,
        row.signed_nonzero_phase_term?.exact,
      ])),
      '<div class="poc-head"><div><span>Fourier identity</span><strong>' + (aggregate.reflection_fourier_identity_proved ? "proved" : "open") + '</strong></div><div><span>L2 sufficiency</span><strong>' + (aggregate.cardinality_and_parseval_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Prime signed slack</span><strong>' + (aggregate.prime_window_signed_phase_slack_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.exact_uniform_crt_rows || [];
    detail = [
      '<div class="poc-equation">Uniform CRT sampling makes centered local admissibility coordinates orthogonal, so G=I and r<sub>eff</sub>=|Q|. Yet every admissible residue class contains infinitely many pairs n,n+2 that are both composite.</div>',
      table(["|Q|", "W", "effective rank", "admissible r", "constructed composite pair"], rows.map((row) => [
        row.coordinate_count_m,
        formatter.format(row.wheel_modulus_W || 0),
        row.uniform_crt_effective_rank,
        row.chosen_admissible_residue_r,
        (row.constructed_composite_pair || []).join(", "),
      ])),
      '<div class="poc-head"><div><span>Uniform CRT Gram</span><strong>' + (aggregate.uniform_crt_gram_identity_proved ? "proved" : "open") + '</strong></div><div><span>Local rank sufficiency</span><strong>' + (aggregate.local_effective_rank_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Parity transfer</span><strong>' + (aggregate.prime_weighted_parity_sensitive_transfer_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket239-cancellation-lifting-fourier-crt" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 239 cancellation, local lifting defects, reflected Fourier phase, and uniform CRT no-go</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>four exact partial/no-go theorems; conjectures open</strong></div><div><span>Next lemmas</span><strong>' + (audit.machine_audit?.next_single_lemma_count ?? 0) + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table">' + table(["TICKET239 audit", "Value"], [
      ["ticket", attempt.ticket_id || "missing"],
      ["exact theorem / 정확한 정리", section.theorem_name || attempt.new_result || "missing"],
      ["declared proposition / 선언 명제", section.declared_proposition || attempt.declared_proposition || "missing"],
      ["next theorem / 다음 정리", attempt.candidate_theorem || "missing"],
    ]) + '</div>',
    detail,
    '<h3>Proof DAG / 증명 의존성</h3>',
    table(["node", "theorem", "status"], (dag.nodes || []).map((node) => [node.id, node.label, node.status])),
    table(["from", "to"], (dag.edges || []).map((edge) => edge)),
    '<div class="poc-route-decision"><section><span>DISCARD / 폐기</span><strong>' + escapeHtml(section.route_decision?.discard || attempt.discarded_route || "") + '</strong></section><section><span>KEEP / 유지</span><strong>' + escapeHtml(section.route_decision?.retain || "") + '</strong></section></div>',
    '<div class="poc-bridge"><section><h3>Established / 확립</h3><p>' + escapeHtml(section.mathematical_argument || computation.proof || "") + '</p></section><section><h3>Remaining proof gap / 남은 증명 간극</h3><p>' + escapeHtml(section.logical_limit || attempt.remaining_gap || "") + '</p><p><strong>Next:</strong> ' + escapeHtml(attempt.candidate_theorem || "") + '</p></section></div>',
    '<p class="proof-boundary">' + escapeHtml(audit.proof_boundary || "All four parent conjectures remain open.") + '</p>',
    '<p><a href="../docs/cancellation-lifting-fourier-crt.ko.md">한국어 보고서</a> · <a href="../docs/cancellation-lifting-fourier-crt.md">English report</a> · <a href="../data/open-problem/ticket239-cancellation-lifting-fourier-crt.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
