function renderTicket242QuantifierOrderParsevalDiagonalCRT(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.quantifier_order_parseval_diagonal_crt_audit || {};
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
    const rows = computation.moving_vector_rows || [];
    detail = [
      '<div class="poc-equation">A<sub>n</sub>=I−2⟨·,e<sub>n</sub>⟩e<sub>n</sub>: every fixed test converges to a positive limit, but the moving test e<sub>n</sub> has value −1. Pointwise convergence does not transfer positivity to a growing family.</div>',
      table(["n", "moving coordinate", "minimum eigenvalue", "fixed probe", "normalized trace", "||A_n-I||"], rows.map((row) => [
        row.finite_section_dimension_n,
        row.moving_negative_coordinate_index,
        row.smallest_eigenvalue?.exact,
        row.fixed_early_coordinate_probe_value?.exact,
        row.normalized_trace?.exact,
        row.operator_norm_distance_from_identity?.exact,
      ])),
      '<div class="poc-head"><div><span>Fixed-test convergence</span><strong>' + (aggregate.fixed_test_pointwise_convergence_proved ? "proved" : "open") + '</strong></div><div><span>Growing-family positivity</span><strong>' + (aggregate.growing_family_uniform_positivity_refuted ? "refuted" : "open") + '</strong></div><div><span>Uniform Weil tail</span><strong>' + (aggregate.signed_guinand_weil_uniform_tail_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.order_growth_rows || [];
    const scan = computation.bounded_identity_scan || {};
    detail = [
      '<div class="poc-equation">For d=ord<sub>q</sub>(32/27), LTE gives v<sub>q</sub>(32<sup>q−1</sup>−27<sup>q−1</sup>)=v<sub>q</sub>(32<sup>d</sup>−27<sup>d</sup>). The orders d are unbounded, so bounded-order checking cannot settle the fixed-base line.</div>',
      table(["prime cutoff", "largest order", "witness prime"], rows.map((row) => [
        formatter.format(row.prime_cutoff || 0),
        formatter.format(row.largest_order_seen || 0),
        formatter.format(row.order_witness_prime || 0),
      ])),
      '<div class="poc-head"><div><span>Order-core LTE</span><strong>' + (aggregate.order_core_lte_reduction_proved ? "proved" : "open") + '</strong></div><div><span>Bounded-order route</span><strong>' + (aggregate.bounded_order_core_route_sufficient_refuted ? "refuted" : "open") + '</strong></div><div><span>All-order transfer</span><strong>' + (aggregate.all_prime_order_core_square_divisor_transfer_proved ? "proved" : "open") + '</strong></div></div>',
      '<div class="poc-head"><div><span>Replay primes scanned</span><strong>' + formatter.format(scan.odd_primes_scanned || 0) + '</strong></div><div><span>Replay limit</span><strong>' + formatter.format(scan.prime_limit || 0) + '</strong></div><div><span>Identity failures / bad candidates</span><strong>' + (scan.order_core_lifting_identity_failures ?? "missing") + ' / ' + (scan.bad_line_candidate_count ?? "missing") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.parseval_scale_rows || [];
    detail = [
      '<div class="poc-equation">Parseval gives ∫|S<sub>X</sub>(α)|²dα=π(X), hence the L²-plus-triangle minor-arc coefficient bound is π(X). This cannot close against a target main scale o(π(X)), including X/log²X.</div>',
      table(["X", "π(X)", "sample N", "ordered reps", "X/log²X", "Parseval / scale"], rows.map((row) => [
        formatter.format(row.prime_cutoff_X || 0),
        formatter.format(row.parseval_global_L2_energy_pi_X || 0),
        formatter.format(row.sample_even_target_N || 0),
        formatter.format(row.ordered_representation_count_R_X_N || 0),
        Number(row.binary_natural_scale_X_over_log_squared_X || 0).toFixed(3),
        Number(row.parseval_to_natural_scale_ratio || 0).toFixed(3),
      ])),
      '<div class="poc-head"><div><span>Parseval bound</span><strong>' + (aggregate.global_parseval_minor_bound_proved ? "proved" : "open") + '</strong></div><div><span>L2-only certificate</span><strong>' + (aggregate.l2_only_natural_scale_certificate_refuted ? "refuted" : "open") + '</strong></div><div><span>Signed minor saving</span><strong>' + (aggregate.signed_minor_fourier_coefficient_saving_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.growing_modulus_diagonal_crt_rows || [];
    detail = [
      '<div class="poc-equation">At each growing period M<sub>j</sub>, impose p≡a<sub>j</sub> (mod M<sub>j</sub>) and p≡−2 (mod ℓ<sub>j</sub>). CRT plus Dirichlet supplies an increasing prime mimic while ℓ<sub>j</sub>|p+2.</div>',
      table(["stage", "M_j", "a_j", "outside ℓ_j", "prime p_j", "composite p_j+2", "cofactor"], rows.map((row) => [
        row.stage_j,
        formatter.format(row.growing_period_M_j || 0),
        row.admissible_residue_a_j,
        row.outside_prime_ell_j,
        formatter.format(row.strictly_increasing_prime_witness_p_j || 0),
        formatter.format(row.forced_composite_successor_p_j_plus_2 || 0),
        formatter.format(row.successor_cofactor || 0),
      ])),
      '<div class="poc-head"><div><span>Growing-period mimicry</span><strong>' + (aggregate.arbitrary_growing_period_diagonal_mimicry_proved ? "proved" : "open") + '</strong></div><div><span>Growth-alone sufficiency</span><strong>' + (aggregate.modulus_growth_alone_sufficient_refuted ? "refuted" : "open") + '</strong></div><div><span>Scale-local Type II</span><strong>' + (aggregate.scale_local_type_ii_cancellation_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket242-quantifier-order-parseval-diagonal-crt" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 242 quantifier order, order-core lifting, Parseval scale, and growing-period diagonal CRT</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>four exact boundary theorems; all conjectures open</strong></div><div><span>Bounded replay limit</span><strong>' + formatter.format(audit.machine_audit?.bounded_order_scan_limit || 0) + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket242-audit-table">' + table(["TICKET242 audit", "Value"], [
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
    '<p class="proof-boundary">Finite computations are bounded evidence. TICKET-242 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/quantifier-order-parseval-diagonal-crt.ko.md">한국어 보고서</a> · <a href="../docs/quantifier-order-parseval-diagonal-crt.md">English report</a> · <a href="../data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
