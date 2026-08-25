function renderTicket241FiniteInformationCanonicalErrors(attempt) {
  if (!attempt) return "";
  const audit = attempt.bounded_result?.finite_information_canonical_error_audit || {};
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
    const rows = computation.prime_cosine_rank_rows || [];
    detail = [
      '<div class="poc-equation">K<sub>jk</sub>=Σ<sub>p∈P</sub>a<sub>p</sub>cos((t<sub>j</sub>−t<sub>k</sub>)log p) is an automatic Gram kernel with rank ≤2|P|. Common-mode removal leaves forced null directions; εI supplies, rather than proves, their lower bound.</div>',
      table(["|P|", "J", "rank cap", "observed rank", "nullity", "regularized minimum"], rows.map((row) => [
        row.prime_support_size_m,
        row.sample_dimension_J,
        row.feature_rank_cap_2m,
        row.numerical_rank,
        row.numerical_nullity,
        Number(row.smallest_regularized_eigenvalue || 0).toExponential(4),
      ])),
      '<div class="poc-head"><div><span>Finite-support rank theorem</span><strong>' + (aggregate.finite_support_rank_cap_proved ? "proved" : "open") + '</strong></div><div><span>Regularized positivity</span><strong>' + (aggregate.regularized_lower_bound_is_tautological ? "route rejected" : "open") + '</strong></div><div><span>Signed Weil form</span><strong>' + (aggregate.signed_guinand_weil_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "collatz") {
    const rows = computation.principal_unit_countermodel_rows || [];
    const scan = computation.bounded_fixed_base_scan || {};
    detail = [
      '<div class="poc-equation">A=1+3q and B=1+5q satisfy A<sup>5</sup>≡B<sup>3</sup> (mod q²) but A≢B (mod q²). Principal-unit algebra alone cannot force 5F<sub>q</sub>(2)=3F<sub>q</sub>(3) ⇒ F<sub>q</sub>(2)=F<sub>q</sub>(3).</div>',
      table(["q", "A", "B", "v_q(A^5-B^3)", "v_q(A-B)", "verified"], rows.map((row) => [
        row.prime_q,
        row.unit_A_1_plus_3q,
        row.unit_B_1_plus_5q,
        row.v_q_A5_minus_B3,
        row.v_q_A_minus_B,
        row.certificate_verified ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Actual primes scanned</span><strong>' + formatter.format(scan.odd_primes_scanned || 0) + '</strong></div><div><span>Search limit</span><strong>' + formatter.format(scan.prime_limit || 0) + '</strong></div><div><span>Actual fixed-base candidates</span><strong>' + (scan.positive_defect_candidate_count ?? "missing") + '</strong></div></div>',
    ].join("");
  } else if (activeProblem === "goldbach") {
    const rows = computation.prime_window_error_contract_rows || [];
    detail = [
      '<div class="poc-equation">R=M+ΣE. Signed aggregation M+ΣE≥1 is exactly R≥1. Absolute aggregation M−Σ|E|≥1 is sufficient only and changes under the harmless split E=(E+L)+(−L).</div>',
      table(["X", "scale", "R", "M", "E", "absolute certificate", "represented"], rows.map((row) => [
        formatter.format(row.cutoff_X || 0),
        row.buffer_scale_multiplier,
        row.representation_count_R,
        Number(row.dc_main_M?.float || 0).toFixed(3),
        Number(row.signed_error_E?.float || 0).toFixed(3),
        row.absolute_certificate_M_minus_abs_E_at_least_one ? "passes" : "fails",
        row.representation_exists ? "yes" : "no",
      ])),
      '<div class="poc-head"><div><span>Signed target</span><strong>' + (aggregate.signed_error_target_is_exact_representation_claim ? "tautological" : "open") + '</strong></div><div><span>Represented rows failing absolute test</span><strong>' + (aggregate.represented_rows_failing_absolute_certificate ?? 0) + '</strong></div><div><span>Canonical arc certificate</span><strong>' + (aggregate.canonical_binary_arc_lower_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  } else {
    const rows = computation.periodic_fingerprint_crt_rows || [];
    detail = [
      '<div class="poc-equation">For every fixed periodic fingerprint F and admissible a (mod M), add p≡−2 (mod ℓ). CRT plus Dirichlet gives infinitely many primes p with the same F but composite p+2.</div>',
      table(["period M", "a", "outside ℓ", "prime p", "composite p+2", "cofactor"], rows.map((row) => [
        formatter.format(row.period_M || 0),
        row.admissible_residue_a,
        row.outside_prime_ell,
        formatter.format(row.prime_witness_p || 0),
        formatter.format(row.forced_composite_successor_p_plus_2 || 0),
        formatter.format(row.successor_cofactor || 0),
      ])),
      '<div class="poc-head"><div><span>Periodic mimicry</span><strong>' + (aggregate.arbitrary_finite_periodic_fingerprint_mimicry_proved ? "proved" : "open") + '</strong></div><div><span>Finite classifier sufficiency</span><strong>' + (aggregate.finite_periodic_twin_classifier_sufficiency_refuted ? "refuted" : "open") + '</strong></div><div><span>Growing Type II bound</span><strong>' + (aggregate.growing_nonperiodic_parity_sensitive_bound_proved ? "proved" : "open") + '</strong></div></div>',
    ].join("");
  }

  return [
    '<div id="ticket241-finite-information-canonical-errors" class="poc-ticket17 poc-ticket128">',
    '<div class="poc-latest-label">LATEST / 최신 연구 경계</div>',
    '<h3>Ticket 241 finite-information rank, fixed-base Fermat search, canonical error contracts, and periodic-fingerprint no-go</h3>',
    '<div class="poc-head"><div><span>Status</span><strong>four exact theorems; all conjectures open</strong></div><div><span>Prime scan bound</span><strong>' + formatter.format(audit.machine_audit?.bounded_prime_scan_limit || 0) + '</strong></div><div><span>Resolution count</span><strong>' + (audit.machine_audit?.conjecture_resolution_count ?? 0) + '</strong></div></div>',
    '<div class="ticket161-audit-table ticket236-audit-table ticket241-audit-table">' + table(["TICKET241 audit", "Value"], [
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
    '<p class="proof-boundary">Finite computations are bounded evidence. TICKET-241 resolves none of the four parent conjectures.</p>',
    '<p><a href="../docs/finite-information-canonical-errors.ko.md">한국어 보고서</a> · <a href="../docs/finite-information-canonical-errors.md">English report</a> · <a href="../data/open-problem/ticket241-finite-information-canonical-errors.json">machine JSON</a></p>',
    '</div>',
  ].join("");
}
