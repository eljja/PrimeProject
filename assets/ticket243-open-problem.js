function renderTicket243BandlimitPrincipalUnitHalfArcDyadicMimicry(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.bandlimit_principal_unit_half_arc_dyadic_mimicry_audit || {};
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
    const rows = computation.exact_cosine_gram_rows || [];
    detail = [
      '<div class="poc-equation">g<sub>n</sub>(ξ)=π<sup>−1/2</sup>cos(nξ) on [−π,π] gives normalized real-even inverse transforms with one fixed Fourier support and Gram matrix I. Frequency tightness alone is not compactness.</div>',
      table(["family size", "support", "Gram diagonal", "max off-diagonal", "min distance²"], rows.map((row) => [
        row.orthonormal_family_size,
        row.fourier_support,
        row.gram_diagonal?.exact,
        row.maximum_off_diagonal_absolute_value?.exact,
        row.minimum_pair_distance_squared?.exact,
      ])),
      '<div class="poc-head"><div><span>Fixed bandlimit</span><strong>' + (aggregate.fixed_frequency_support_proved ? "proved" : "open") + '</strong></div><div><span>Relative compactness</span><strong>' + (aggregate.relative_compactness_refuted ? "refuted" : "open") + '</strong></div><div><span>Uniform Weil tail</span><strong>' + (aggregate.uniform_signed_guinand_weil_tail_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.selected_principal_unit_rows || [];
    const scan = computation.bounded_universal_model_replay || {};
    detail = [
      '<div class="poc-equation">For every q&gt;5, Teichmüller lift T and A=T(1+3q), B=T(1+5q) give V=A⁵/B³=T² of order (q−1)/2 with V<sup>d</sup>=1 mod q², while U=A/B=1−2q mod q² has exact depth one.</div>',
      table(["q", "primitive t", "order d", "U mod q²", "V mod q²", "verified"], rows.map((row) => [
        formatter.format(row.prime_q || 0),
        row.primitive_root_t,
        formatter.format(row.order_d_of_V_mod_q || 0),
        formatter.format(row.U_equals_A_over_B_mod_q_squared || 0),
        formatter.format(row.V_equals_A_power_5_over_B_power_3_mod_q_squared || 0),
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Local models scanned</span><strong>' + formatter.format(scan.primes_scanned || 0) + '</strong></div><div><span>Largest model order</span><strong>' + formatter.format(scan.largest_countermodel_order || 0) + '</strong></div><div><span>Failures</span><strong>' + (scan.failure_count ?? "missing") + '</strong></div></div>',
      '<div class="poc-head"><div><span>Unbounded-order family</span><strong>' + (aggregate.unbounded_order_local_countermodel_family_proved ? "proved" : "open") + '</strong></div><div><span>Universal local transfer</span><strong>' + (aggregate.universal_local_order_core_transfer_refuted ? "refuted" : "open") + '</strong></div><div><span>Fixed-base exclusion</span><strong>' + (aggregate.fixed_base_32_over_27_exception_excluded ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.exact_half_frequency_rows || [];
    detail = [
      '<div class="poc-equation">On |β|≤1/(6X), |S<sub>X</sub>(1/2+β)|≥(π(X)−3)/2, so the full parity-frequency neighborhood carries at least (π(X)−3)²/(12X) absolute energy, asymptotic to X/(12log²X).</div>',
      table(["X", "π(X)", "half-width", "pointwise floor", "energy floor", "floor / natural scale"], rows.map((row) => [
        formatter.format(row.prime_cutoff_X || 0),
        formatter.format(row.prime_count_pi_X || 0),
        row.half_frequency_arc_half_width?.exact,
        row.pointwise_absolute_S_floor?.exact,
        row.exact_integrated_energy_floor?.exact,
        Number(row.energy_floor_over_X_log_squared_X || 0).toFixed(5),
      ])),
      '<div class="poc-head"><div><span>Half-arc floor</span><strong>' + (aggregate.half_frequency_pointwise_floor_proved ? "proved" : "open") + '</strong></div><div><span>Omitted-major route</span><strong>' + (aggregate.minor_arc_omission_route_refuted ? "refuted" : "open") + '</strong></div><div><span>Signed residual saving</span><strong>' + (aggregate.signed_targetwise_residual_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.finite_dyadic_witness_rows || [];
    detail = [
      '<div class="poc-equation">For fixed Q=Mℓ, PNT in arithmetic progressions puts a CRT prime mimic in every sufficiently large [X,2X], while ℓ|p+2. Fixed periodic fingerprints fail even under eventual dyadic scale sampling.</div>',
      table(["M", "outside ℓ", "Q", "X", "prime p", "composite p+2"], rows.map((row) => [
        formatter.format(row.fixed_period_M || 0),
        row.outside_prime_ell,
        formatter.format(row.combined_modulus_Q || 0),
        formatter.format(row.dyadic_block_start_X || 0),
        formatter.format(row.prime_mimic_p || 0),
        formatter.format(row.forced_composite_successor_p_plus_2 || 0),
      ])),
      '<div class="poc-head"><div><span>Every-large-block fixed-period mimicry</span><strong>' + (aggregate.fixed_period_every_large_dyadic_mimicry_proved ? "proved" : "open") + '</strong></div><div><span>Growing-modulus uniformity</span><strong>' + (aggregate.growing_modulus_uniformity_proved ? "proved" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.scale_local_type_ii_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 243 bandlimit, principal-unit transfer, half-arc energy, and dyadic mimicry</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>three exact no-go theorems and one partial theorem; all conjectures open</strong></div><div><span>Deep focus</span><strong>' + escapeHtml(audit.machine_audit?.deep_focus_problem || "missing") + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket243-audit-table">' + table(["TICKET243 audit", "Value"], [
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
    '<p class="proof-boundary">Iteration complete does not mean problem resolved. TICKET-243 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/bandlimit-principal-unit-half-arc-dyadic-mimicry.ko.md">한국어 보고서</a> · <a href="../docs/bandlimit-principal-unit-half-arc-dyadic-mimicry.md">English report</a> · <a href="../data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
