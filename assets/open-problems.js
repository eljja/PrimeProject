const problemId = document.body.dataset.problem;
const formatter = new Intl.NumberFormat("en-US");

const pageLinks = {
  riemann: "riemann.html",
  collatz: "collatz.html",
  goldbach: "goldbach.html",
  "twin-prime": "twin-prime.html",
};

const labels = {
  riemann: "Riemann",
  collatz: "Collatz",
  goldbach: "Goldbach",
  "twin-prime": "Twin Prime",
};

function formatValue(value) {
  if (typeof value === "number") {
    if (Number.isInteger(value)) return formatter.format(value);
    return value.toLocaleString("en-US", { maximumFractionDigits: 6 });
  }
  if (Array.isArray(value)) return value.map(formatValue).join(", ");
  if (value === null || value === undefined) return "n/a";
  return String(value);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function metricCards(problem) {
  const result = problem.finite_result || {};
  if (problem.id === "riemann") {
    return [
      ["Search limit", result.limit],
      ["Checkpoints", result.checkpoints?.length || 0],
      ["Max scaled theta error", result.max_scaled_theta_error],
    ];
  }
  if (problem.id === "collatz") {
    return [
      ["Start values", result.tested_start_values],
      ["Counterexamples", result.counterexamples],
      ["Max stopping time", `${formatValue(result.max_total_stopping_time?.steps)} at ${formatValue(result.max_total_stopping_time?.n)}`],
    ];
  }
  if (problem.id === "goldbach") {
    return [
      ["Even values", result.tested_even_values],
      ["Counterexamples", result.counterexamples],
      ["Hardest smallest p", `${formatValue(result.hardest_smallest_prime_decomposition?.smallest_prime)} for ${formatValue(result.hardest_smallest_prime_decomposition?.even)}`],
    ];
  }
  return [
    ["Search limit", result.limit],
    ["Twin pairs", result.twin_pair_count],
    ["Largest pair", result.largest_pair_seen],
  ];
}

function renderTable(problem) {
  const result = problem.finite_result || {};
  if (problem.id === "riemann") {
    return table(
      ["x", "pi(x)", "li approx", "pi - li", "theta - x", "scaled theta error"],
      (result.checkpoints || []).map((row) => [
        row.x,
        row.pi_x,
        row.li_approx,
        row.pi_minus_li_approx,
        row.theta_minus_x,
        row.scaled_theta_error,
      ]),
    );
  }
  if (problem.id === "collatz") {
    return table(
      ["measure", "n", "value"],
      [
        ["max total stopping time", result.max_total_stopping_time?.n, result.max_total_stopping_time?.steps],
        ["max peak ratio", result.max_peak_ratio?.n, result.max_peak_ratio?.ratio],
        ["max peak value", result.max_peak_ratio?.n, result.max_peak_ratio?.peak],
      ],
    );
  }
  if (problem.id === "goldbach") {
    const hardest = result.hardest_smallest_prime_decomposition || {};
    return [
      table(["even", "p", "q"], result.sample_decompositions?.map((row) => [row.even, row.p, row.q]) || []),
      `<div class="proof-note">Hardest bounded case by smallest first prime: ${escapeHtml(formatValue(hardest.even))} = ${escapeHtml(formatValue(hardest.smallest_prime))} + ${escapeHtml(formatValue(hardest.partner))}</div>`,
    ].join("");
  }
  return table(
    ["x", "observed twin pairs", "Hardy-Littlewood estimate"],
    (result.checkpoints || []).map((row) => [row.x, row.twin_pairs, row.hardy_littlewood_estimate]),
  );
}

function table(headers, rows) {
  return `
    <div class="proof-table-wrap">
      <table class="proof-table">
        <thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows
            .map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(formatValue(cell))}</td>`).join("")}</tr>`)
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function list(items) {
  return `<ol>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ol>`;
}

function renderCertificate(problem) {
  const certificate = problem.certificate || {};
  const merkleRoot = certificate.merkle_root || "n/a";
  const status = String(certificate.status || "missing").replaceAll("_", " ");
  return `
    <div class="certificate-grid">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(status)}</strong>
      </div>
      <div>
        <span>Leaves</span>
        <strong>${escapeHtml(formatValue(certificate.leaf_count))}</strong>
      </div>
      <div>
        <span>Chunks</span>
        <strong>${escapeHtml(formatValue(certificate.chunk_count))}</strong>
      </div>
      <div>
        <span>Merkle root</span>
        <code>${escapeHtml(merkleRoot)}</code>
      </div>
    </div>
    <p class="certificate-statement">${escapeHtml(certificate.statement || "")}</p>
    <p class="certificate-verifier">Verifier: <code>${escapeHtml(certificate.verifier || "")}</code></p>
  `;
}

function renderProofAttempt(problem) {
  const attempt = problem.proof_attempt || {};
  const obligations = attempt.obligations || [];
  const targets = attempt.falsification_targets || [];
  return `
    <div class="attempt-summary">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(String(attempt.status || "missing").replaceAll("_", " "))}</strong>
      </div>
      <div>
        <span>Bounded theorem</span>
        <strong>${escapeHtml(String(attempt.bounded_theorem_status || "missing").replaceAll("_", " "))}</strong>
      </div>
    </div>
    <p class="attempt-route">${escapeHtml(attempt.attack_route || "")}</p>
    <div class="obligation-list">
      ${obligations
        .map(
          (item) => `
            <div class="obligation-item is-${escapeHtml(item.status || "open")}">
              <span>${escapeHtml(item.id || "")}</span>
              <strong>${escapeHtml(String(item.status || "").replaceAll("_", " "))}</strong>
              <p>${escapeHtml(item.claim || "")}</p>
              <em>${escapeHtml(item.verifier || "")}</em>
            </div>
          `,
        )
        .join("")}
    </div>
    <div class="falsification-targets">
      <strong>Falsification targets</strong>
      <ul>${targets.map((target) => `<li>${escapeHtml(target)}</li>`).join("")}</ul>
    </div>
    <p class="certificate-verifier">Formal target: <code>${escapeHtml(attempt.next_formalization_target?.statement || "")}</code></p>
  `;
}

function statusText(value) {
  return String(value || "missing").replaceAll("_", " ");
}

function renderProofMap(problem) {
  const attempt = problem.proof_attempt || {};
  const graph = attempt.attack_graph || {};
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const bridges = attempt.known_theorem_bridges || [];
  const lemmas = attempt.lemma_candidates || [];
  return `
    <div class="proof-map-grid">
      ${nodes
        .map(
          (node) => `
            <div class="proof-node is-${escapeHtml(node.status || "open")}">
              <span>${escapeHtml(node.id || "")}</span>
              <strong>${escapeHtml(node.label || "")}</strong>
              <em>${escapeHtml(statusText(node.status))}</em>
            </div>
          `,
        )
        .join("")}
    </div>
    <div class="proof-edge-list">
      ${edges
        .map(
          (edge) => `
            <div class="proof-edge is-${escapeHtml(edge.status || "open")}">
              <code>${escapeHtml(edge.from || "")} -> ${escapeHtml(edge.to || "")}</code>
              <span>${escapeHtml(edge.label || "")}</span>
              <strong>${escapeHtml(statusText(edge.status))}</strong>
            </div>
          `,
        )
        .join("")}
    </div>
    <div class="bridge-lemma-grid">
      <section>
        <h3>Known theorem bridges</h3>
        ${bridges
          .map(
            (bridge) => `
              <article class="bridge-card is-${escapeHtml(bridge.status || "open")}">
                <span>${escapeHtml(bridge.id || "")}</span>
                <strong>${escapeHtml(bridge.name || "")}</strong>
                <p>${escapeHtml(bridge.role || "")}</p>
                <em>${escapeHtml(statusText(bridge.status))}</em>
              </article>
            `,
          )
          .join("")}
      </section>
      <section>
        <h3>Lemma candidates</h3>
        ${lemmas
          .map(
            (lemma) => `
              <article class="bridge-card is-${escapeHtml(lemma.status || "open")}">
                <span>${escapeHtml(lemma.id || "")}</span>
                <strong>${escapeHtml(lemma.statement || "")}</strong>
                <p>${escapeHtml(lemma.evidence || "")}</p>
                <p>${escapeHtml(lemma.required_upgrade || "")}</p>
                <em>${escapeHtml(statusText(lemma.status))}</em>
              </article>
            `,
          )
          .join("")}
      </section>
    </div>
  `;
}

function renderProofStatusGate(problem) {
  const gate = problem.proof_status_gate || {};
  const rows = [
    ["Promotion status", statusText(gate.promotion_status)],
    ["Allowed public claim", statusText(gate.allowed_public_claim)],
    ["Formal contract", statusText(gate.formal_contract_status)],
    ["Open obligations", (gate.open_obligations || []).join(", ") || "none"],
    ["Open graph links", (gate.open_attack_graph_links || []).join(", ") || "none"],
    ["Unsatisfied bridges", (gate.unsatisfied_known_theorem_bridges || []).join(", ") || "none"],
    ["Open lemma candidates", (gate.open_lemma_candidates || []).join(", ") || "none"],
  ];
  return `
    <div class="proof-gate-status is-${escapeHtml(gate.promotion_status || "missing")}">
      <span>Machine gate</span>
      <strong>${escapeHtml(statusText(gate.promotion_status))}</strong>
      <p>${escapeHtml(gate.machine_rule || "")}</p>
    </div>
    <div class="proof-gate-table">
      ${rows
        .map(
          ([label, value]) => `
            <div>
              <span>${escapeHtml(label)}</span>
              <strong>${escapeHtml(value)}</strong>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderFormalContract(problem) {
  const contract = problem.formal_proof_contract || {};
  return `
    <div class="formal-contract-head">
      <div>
        <span>Target</span>
        <strong>${escapeHtml(contract.proof_assistant_target || "missing")}</strong>
      </div>
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(contract.status))}</strong>
      </div>
      <div>
        <span>Theorem</span>
        <strong>${escapeHtml(contract.theorem_name || "missing")}</strong>
      </div>
    </div>
    <pre class="formal-statement"><code>${escapeHtml(contract.lean_statement || "")}</code></pre>
    <div class="bridge-lemma-grid">
      <section>
        <h3>Required artifacts</h3>
        ${list(contract.required_artifacts || [])}
      </section>
      <section>
        <h3>Forbidden assumptions</h3>
        ${list(contract.forbidden_assumptions || [])}
      </section>
    </div>
    <div class="formal-rules">
      <strong>Acceptance rules</strong>
      ${list(contract.acceptance_rules || [])}
    </div>
  `;
}

function renderMilestoneQueue(problem) {
  const queue = problem.proof_milestone_queue || {};
  const milestones = queue.milestones || [];
  return `
    <div class="milestone-summary">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(queue.status))}</strong>
      </div>
      <div>
        <span>Complete</span>
        <strong>${escapeHtml(formatValue(queue.completed_count || 0))}</strong>
      </div>
      <div>
        <span>Open</span>
        <strong>${escapeHtml(formatValue(queue.open_count || 0))}</strong>
      </div>
      <div>
        <span>Blocked</span>
        <strong>${escapeHtml(formatValue(queue.blocked_count || 0))}</strong>
      </div>
    </div>
    <p class="attempt-route">${escapeHtml(queue.decisive_next_task || "")}</p>
    <div class="milestone-list">
      ${milestones
        .map(
          (item) => `
            <article class="milestone-card is-${escapeHtml(item.status || "open")}">
              <span>${escapeHtml(item.id || "")}</span>
              <strong>${escapeHtml(item.title || "")}</strong>
              <em>${escapeHtml(statusText(item.status))}</em>
              <p>${escapeHtml(item.artifact || "")}</p>
              <small>${escapeHtml(item.exit_criterion || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="certificate-verifier">${escapeHtml(queue.promotion_rule || "")}</p>
  `;
}

function renderDecisiveLemmaLab(problem) {
  const lab = problem.decisive_lemma_lab || {};
  const probe = lab.finite_probe || {};
  const probeRows = Object.entries(probe);
  const falsificationProbe = lab.automated_falsification_probe || {};
  const probeCertificate = falsificationProbe.probe_certificate || {};
  const strongestRows = Object.entries(falsificationProbe.strongest_observed || {});
  return `
    <div class="decisive-lab-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(lab.status))}</strong>
      </div>
      <div>
        <span>Lemma</span>
        <strong>${escapeHtml(lab.lemma_id || "missing")}</strong>
      </div>
      <div>
        <span>Would close</span>
        <strong>${escapeHtml((lab.closes_milestones || []).join(", ") || "none")}</strong>
      </div>
    </div>
    <p class="attempt-route">${escapeHtml(lab.decisive_question || "")}</p>
    <div class="decisive-statement">
      <span>Candidate statement</span>
      <p>${escapeHtml(lab.candidate_statement || "")}</p>
    </div>
    <div class="decisive-grid">
      <section>
        <h3>Finite Probe</h3>
        <div class="proof-gate-table">
          ${probeRows
            .map(
              ([label, value]) => `
                <div>
                  <span>${escapeHtml(label.replaceAll("_", " "))}</span>
                  <strong>${escapeHtml(formatValue(value))}</strong>
                </div>
              `,
            )
            .join("")}
        </div>
      </section>
      <section>
        <h3>Proof Obligation</h3>
        <p>${escapeHtml(lab.proof_obligation || "")}</p>
        <h3>Falsification Test</h3>
        <p>${escapeHtml(lab.falsification_test || "")}</p>
      </section>
    </div>
    <div class="falsification-probe is-${escapeHtml(falsificationProbe.result_status || "missing")}">
      <div class="falsification-probe-head">
        <span>Automated Falsification Probe</span>
        <strong>${escapeHtml(statusText(falsificationProbe.result_status))}</strong>
      </div>
      <div class="proof-gate-table">
        <div>
          <span>scope</span>
          <strong>${escapeHtml(falsificationProbe.scope || "missing")}</strong>
        </div>
        <div>
          <span>probe count</span>
          <strong>${escapeHtml(formatValue(falsificationProbe.probe_count || 0))}</strong>
        </div>
        <div>
          <span>violated count</span>
          <strong>${escapeHtml(formatValue(falsificationProbe.violated_count || 0))}</strong>
        </div>
        <div>
          <span>pass condition</span>
          <strong>${escapeHtml(falsificationProbe.pass_condition || "missing")}</strong>
        </div>
      </div>
      <div class="probe-observed">
        ${strongestRows
          .map(
            ([label, value]) => `
              <div>
                <span>${escapeHtml(label.replaceAll("_", " "))}</span>
                <strong>${escapeHtml(formatValue(value))}</strong>
              </div>
            `,
          )
          .join("")}
      </div>
      <p>${escapeHtml(falsificationProbe.proof_gap || "")}</p>
      <div class="probe-certificate">
        <div>
          <span>Certificate</span>
          <strong>${escapeHtml(statusText(probeCertificate.status))}</strong>
        </div>
        <div>
          <span>Merkle root</span>
          <code>${escapeHtml(probeCertificate.merkle_root || "missing")}</code>
        </div>
        <div>
          <span>Verifier</span>
          <strong>${escapeHtml(probeCertificate.verifier || "missing")}</strong>
        </div>
      </div>
    </div>
    <div class="decisive-current">
      <strong>${escapeHtml(lab.current_result || "")}</strong>
      <p>${escapeHtml(lab.next_action || "")}</p>
      <small>${escapeHtml(lab.promotion_rule || "")}</small>
    </div>
  `;
}

function render(payload, problem) {
  document.title = `${problem.title} - PrimeProject Proof Workbench`;
  document.querySelector("#problemTitle").textContent = problem.title;
  document.querySelector("#problemKoreanTitle").textContent = problem.korean_title;
  document.querySelector("#problemStatement").textContent = problem.target_statement;
  document.querySelector("#claimStatus").textContent = problem.status.replaceAll("_", " ");
  document.querySelector("#generatedAt").textContent = payload.generated_at;
  document.querySelector("#searchLimit").textContent = formatValue(payload.search_limit);
  document.querySelector("#claimPolicy").textContent = payload.claim_policy.reason;
  document.querySelector("#toolPosition").textContent = problem.tool_position;
  document.querySelector("#claimBoundary").textContent = problem.claim_boundary;

  document.querySelector("#problemNav").innerHTML = Object.entries(pageLinks)
    .map(([id, href]) => `<a class="${id === problem.id ? "is-active" : ""}" href="${href}">${labels[id]}</a>`)
    .join("");

  document.querySelector("#metricCards").innerHTML = metricCards(problem)
    .map(
      ([label, value]) => `
        <div class="proof-metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(formatValue(value))}</strong>
        </div>
      `,
    )
    .join("");

  document.querySelector("#finiteEvidence").innerHTML = renderTable(problem);
  document.querySelector("#certificatePanel").innerHTML = renderCertificate(problem);
  document.querySelector("#proofAttempt").innerHTML = renderProofAttempt(problem);
  document.querySelector("#proofMap").innerHTML = renderProofMap(problem);
  document.querySelector("#proofStatusGate").innerHTML = renderProofStatusGate(problem);
  document.querySelector("#formalContract").innerHTML = renderFormalContract(problem);
  document.querySelector("#milestoneQueue").innerHTML = renderMilestoneQueue(problem);
  document.querySelector("#decisiveLemmaLab").innerHTML = renderDecisiveLemmaLab(problem);
  document.querySelector("#proofGates").innerHTML = list(problem.proof_gates || []);
  document.querySelector("#candidateStrategy").innerHTML = list(problem.candidate_strategy || []);
  document.querySelector("#blockedClaims").innerHTML = (payload.claim_policy.blocked_claims || [])
    .map((claim) => `<span>${escapeHtml(claim)}</span>`)
    .join("");
}

async function main() {
  const response = await fetch("../data/open_problem_workbench.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Failed to load workbench data: ${response.status}`);
  const payload = await response.json();
  const problem = payload.problems.find((item) => item.id === problemId);
  if (!problem) throw new Error(`Unknown problem: ${problemId}`);
  render(payload, problem);
}

main().catch((error) => {
  document.querySelector("#finiteEvidence").innerHTML = `<div class="proof-note is-error">${escapeHtml(error.message)}</div>`;
});
