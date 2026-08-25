function renderTicket240RouteCorrectionsWieferichPrimeCRT(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.route_corrections_wieferich_prime_crt_audit || {};
  const section = ({
    riemann: audit.riemann,
    collatz: audit.collatz,
    goldbach: audit.goldbach,
    "twin-prime": audit.twin_prime,
  })[attempt.problem_id || problemId] || {};
  const computation = section.reproducible_computation || {};
  const aggregate = computation.aggregate || {};
  const dag = section.proof_dag || {};
  let detail = "";

  if ((attempt.problem_id || problemId) === "riemann") {
    const rows = computation.exact_model_rows || [];
    detail = [
      '<div class="poc-equation">G<sub>J</sub>=(1−C)I+C[(1+|i−j|)<sup>−1</sup>] remains ⪰(1−C)I, while the Cotlar square-root overlap sum grows like Σd<sup>−1/2</sup>. Absolute Cotlar norms do not encode signed Weil cancellation.</div>',
      table(["J", "Gram lower", "absolute row sum", "Cotlar sqrt-overlap sum"], rows.map((row) => [
        row.dimension_J,
        row.uniform_gram_lower_bound?.exact,
        Number(row.maximum_absolute_gram_cross_row_sum?.float || 0).toFixed(4),
        Number(row.maximum_cotlar_sqrt_overlap_row_sum || 0).toFixed(4),
      ])),
      '<div class="poc-head"><div><span>Uniform Gram lower bound</span><strong>' + (aggregate.uniform_positive_gram_family_proved ? "proved" : "open") + '</strong></div><div><span>Cotlar necessity</span><strong>' + (aggregate.cotlar_sqrt_overlap_summability_necessity_refuted ? "refuted" : "open") + '</strong></div><div><span>Arithmetic signed lower bound</span><strong>' + (aggregate.arithmetic_weil_signed_operator_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if ((attempt.problem_id || problemId) === "collatz") {
    const rows = computation.representative_depth_reduction_rows || [];
    const scan = computation.bounded_rational_wieferich_scan || {};
    detail = [
      '<div class="poc-equation">δ<sub>q</sub>=v<sub>q</sub>(32<sup>q−1</sup>−27<sup>q−1</sup>)−v<sub>q</sub>(2<sup>q−1</sup>−3<sup>q−1</sup>). First depth is governed by 5F<sub>q</sub>(2)−3F<sub>q</sub>(3) versus F<sub>q</sub>(2)−F<sub>q</sub>(3).</div>',
      table(["q", "ℓq", "x depth", "y depth", "reduction"], rows.map((row) => [
        row.prime_q,
        row.local_period_ell_q,
        row.fermat_x_depth_W_q_32_over_27,
        row.fermat_y_depth_W_q_2_over_3,
        row.depth_reduction_verified ? "verified" : "failed",
      ])),
      '<div class="poc-head"><div><span>Odd primes scanned</span><strong>' + formatter.format(scan.odd_primes_scanned || 0) + '</strong></div><div><span>x depth ≥ 2</span><strong>' + (scan.x_depth_at_least_two_count ?? "missing") + '</strong></div><div><span>y depth ≥ 2</span><strong>' + (scan.y_depth_at_least_two_primes || []).join(", ") + '</strong></div></div>',
    ].join("");
  } else if ((attempt.problem_id || problemId) === "goldbach") {
    const rows = computation.prime_window_signed_slack_rows || [];
    detail = [
      '<div class="poc-equation">S<sub>A</sub>(h)+DC<sub>A</sub>=R<sub>A</sub>(h)∈Z<sub>≥0</sub>. Therefore S<sub>A</sub>(h)&gt;−DC<sub>A</sub> is exactly R<sub>A</sub>(h)≥1, not a weaker intermediate target.</div>',
      table(["X", "scale", "h", "target N", "R_A(h)", "threshold=existence"], rows.map((row) => [
        formatter.format(row.cutoff_X || 0),
        row.buffer_scale_multiplier,
        row.even_buffer_h,
        formatter.format(row.target_N || 0),
        row.ordered_reflection_count_R_A_h,
        row.equivalence_verified ? "verified" : "failed",
      ])),
      '<div class="poc-head"><div><span>Integrality equivalence</span><strong>' + (aggregate.signed_slack_integrality_equivalence_proved ? "proved" : "open") + '</strong></div><div><span>Window rows</span><strong>' + (aggregate.prime_window_row_count ?? 0) + '</strong></div><div><span>Restricted zero rows</span><strong>' + (aggregate.zero_restricted_window_row_count ?? 0) + '</strong></div></div>',
    ].join("");
  } else {
    const patterns = computation.exact_all_pattern_crt_rows || [];
    const grams = computation.actual_one_sided_prime_weighted_gram_rows || [];
    detail = [
      '<div class="poc-equation">Every complete finite CRT bit pattern contains infinitely many primes p with composite p+2: add one outside congruence p≡−2 (mod ℓ), then apply CRT and Dirichlet. One-sided prime weighting cannot break parity.</div>',
      table(["CRT bits", "residue", "prime witness p", "composite p+2", "outside factor"], patterns.map((row) => [
        (row.local_admissibility_bits || []).join(""),
        row.crt_residue_r,
        formatter.format(row.first_prime_witness_p || 0),
        formatter.format(row.forced_composite_successor_p_plus_2 || 0),
        row.outside_prime_factor,
      ])),
      table(["X", "prime samples", "coordinates", "max correlation", "effective rank", "finite twins"], grams.map((row) => [
        formatter.format(row.upper_scale_X || 0),
        formatter.format(row.prime_sample_count || 0),
        row.coordinate_count_m,
        Number(row.maximum_absolute_pair_correlation_mu || 0).toFixed(6),
        Number(row.gram_effective_rank || 0).toFixed(6),
        formatter.format(row.finite_twin_pair_count_in_sample || 0),
      ])),
      '<div class="poc-head"><div><span>All finite patterns</span><strong>' + (aggregate.all_finite_crt_patterns_have_infinite_prime_composite_successors ? "proved" : "open") + '</strong></div><div><span>One-sided sufficiency</span><strong>' + (aggregate.one_sided_prime_weighted_finite_crt_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Two-sided main term</span><strong>' + (aggregate.two_sided_parity_breaking_main_term_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket240-route-corrections-wieferich-prime-crt" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 240 route corrections, rational Wieferich depths, signed Goldbach integrality, and one-sided prime CRT no-go</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>four exact theorems; all conjectures open</strong></div><div><span>Prime scan bound</span><strong>' + formatter.format(audit.machine_audit?.bounded_prime_scan_limit || 0) + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table">' + table(["TICKET240 audit", "Value"], [
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
    '<p class="proof-boundary">Finite computations are bounded evidence. TICKET-240 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/route-corrections-wieferich-prime-crt.ko.md">한국어 보고서</a> · <a href="../docs/route-corrections-wieferich-prime-crt.md">English report</a> · <a href="../data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
