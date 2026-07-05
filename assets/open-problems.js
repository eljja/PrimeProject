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
  if (value === null || value === undefined) return "n/a";
  if (Array.isArray(value)) return value.map(formatValue).join(", ");
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function koGuide(title, items) {
  return `
    <div class="ko-helper">
      <strong>${escapeHtml(title)}</strong>
      <ul>
        ${(items || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
    </div>
  `;
}

function problemKoGuide(problem) {
  const guides = {
    riemann: [
      "이 페이지는 리만가설을 증명했다고 주장하지 않습니다. 유한 계산과 필요한 무한 정리를 분리해 보여줍니다.",
      "zero-line, explicit formula, positivity kernel 같은 영어 용어는 연구 문헌의 표준 표현입니다. 옆의 blocker와 gate가 아직 남은 이유를 설명합니다.",
      "open_not_proven은 독립 검증 가능한 무한 논증이 없다는 뜻입니다.",
    ],
    collatz: [
      "이 페이지는 콜라츠 추측의 궤적 계산과 전역 descent 증명을 구분합니다.",
      "bounded trajectory는 정해진 범위에서 확인한 계산 결과이고, global descent cover는 모든 자연수를 덮는 별도 증명입니다.",
      "ranking function은 값이 반드시 줄어드는 순서를 만들어 무한 반복을 막는 수학적 장치입니다.",
    ],
    goldbach: [
      "이 페이지는 골드바흐 추측의 유한 검증과 큰 짝수 전체에 대한 정리를 구분합니다.",
      "exception search는 반례 후보를 찾는 계산이고, lower-bound theorem은 모든 충분히 큰 짝수에 표현이 존재함을 보이는 증명입니다.",
      "현재 계산은 반례를 찾지 못했다는 증거이지, 전체 추측의 증명은 아닙니다.",
    ],
    "twin-prime": [
      "이 페이지는 쌍둥이 소수가 많이 관측된다는 사실과 무한히 많다는 증명을 분리합니다.",
      "exact gap-2는 차이가 정확히 2인 소수쌍을 뜻합니다. bounded gap 정리는 더 약한 명제입니다.",
      "필요한 핵심은 gap 2 소수쌍이 임의로 큰 범위까지 계속 존재한다는 무조건적 하한 정리입니다.",
    ],
  };
  return koGuide("한국어 해설", guides[problem.id] || [
    "이 페이지는 유한 계산, 후보 전략, 차단된 주장, 필요한 무한 증명을 분리해 보여줍니다.",
    "영문 라벨은 논문/검증 스크립트와 맞추기 위한 표준 artifact 이름이며, 한국어 해설은 그 의미를 설명합니다.",
  ]);
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

function renderProofVerdict(problem) {
  const verdict = problem.proof_verdict || {};
  return `
    <div class="verdict-grid">
      <div>
        <span>Target verdict</span>
        <strong>${escapeHtml(statusText(verdict.target_verdict))}</strong>
      </div>
      <div>
        <span>Actual proved result</span>
        <strong>${escapeHtml(statusText(verdict.actual_proved_status))}</strong>
      </div>
      <div>
        <span>Full proof blocker</span>
        <strong>${escapeHtml(verdict.full_proof_blocker || "missing")}</strong>
      </div>
      <div>
        <span>Gate</span>
        <strong>${escapeHtml(statusText(verdict.gate_status))}</strong>
      </div>
    </div>
    <div class="verdict-body">
      <p><strong>Bounded theorem:</strong> ${escapeHtml(verdict.actual_proved_result || "")}</p>
      <p><strong>Next decisive attempt:</strong> ${escapeHtml(verdict.next_decisive_attempt || "")}</p>
      <p>${escapeHtml(verdict.machine_rule || "")}</p>
    </div>
  `;
}

function renderActualProofAttemptRunner(problem) {
  const runner = problem.actual_proof_attempt_runner || {};
  const steps = runner.runner_steps || [];
  return `
    <div class="runner-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(runner.runner_status))}</strong>
      </div>
      <div>
        <span>Problem</span>
        <strong>${escapeHtml(problem.title || "")}</strong>
      </div>
      <div>
        <span>Steps</span>
        <strong>${escapeHtml(formatValue(steps.length))}</strong>
      </div>
    </div>
    <article class="runner-bridge">
      <span>${escapeHtml(runner.attempt_title || "")}</span>
      <p>${escapeHtml(runner.candidate_bridge || "")}</p>
      <small>Observed signal: ${escapeHtml(runner.observed_signal || "")}</small>
    </article>
    <div class="runner-step-list">
      ${steps
        .map(
          (step) => `
            <article class="runner-step">
              <span>${escapeHtml(step.id || "")} · ${escapeHtml(step.tool || "")}</span>
              <strong>${escapeHtml(statusText(step.status))}</strong>
              <p>${escapeHtml(step.input || "")}</p>
              <small>Output: ${escapeHtml(step.output || "")}</small>
              <em>${escapeHtml(step.proof_effect || "")}</em>
            </article>
          `,
        )
        .join("")}
    </div>
    <div class="runner-outcome">
      <section>
        <h3>Closed By Tools</h3>
        ${list(runner.closed_items || [])}
      </section>
      <section>
        <h3>Still Open</h3>
        ${list(runner.open_items || [])}
      </section>
    </div>
    <div class="runner-verdict">
      <p><strong>Execution result:</strong> ${escapeHtml(runner.machine_verdict || "")}</p>
      <p><strong>Why this is not yet a proof:</strong> ${escapeHtml(runner.failure_reason || "")}</p>
      <p><strong>Next executable move:</strong> ${escapeHtml(runner.next_executable_move || "")}</p>
      <p>${escapeHtml(runner.promotion_rule || "")}</p>
    </div>
  `;
}

function renderCandidateLemmaWorkbench(problem) {
  const workbench = problem.candidate_lemma_workbench || {};
  const lemmas = workbench.lemmas || [];
  return `
    <div class="lemma-workbench-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(workbench.status))}</strong>
      </div>
      <div>
        <span>Closed</span>
        <strong>${escapeHtml(formatValue(workbench.closed_count || 0))}</strong>
      </div>
      <div>
        <span>Open / blocked</span>
        <strong>${escapeHtml(formatValue(workbench.open_or_blocked_count || 0))}</strong>
      </div>
    </div>
    <article class="lemma-workbench-target">
      <span>${escapeHtml(workbench.workbench_title || "")}</span>
      <p>${escapeHtml(workbench.target || "")}</p>
    </article>
    <div class="lemma-card-list">
      ${lemmas
        .map(
          (lemma) => `
            <article class="lemma-card is-${escapeHtml(lemma.result || "unknown")}">
              <span>${escapeHtml(lemma.id || "")} · ${escapeHtml(statusText(lemma.result))}</span>
              <strong>${escapeHtml(lemma.statement || "")}</strong>
              <p>Tool test: ${escapeHtml(lemma.tool_test || "")}</p>
              <p>Result reason: ${escapeHtml(lemma.reason || "")}</p>
              <small>Next revision: ${escapeHtml(lemma.next_revision || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(workbench.claim_rule || "")}</p>
  `;
}

function renderMachineProofSearchTrials(problem) {
  const report = problem.machine_proof_search_trials || {};
  const trials = report.trials || [];
  return `
    <div class="search-trials-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(report.status))}</strong>
      </div>
      <div>
        <span>Trials</span>
        <strong>${escapeHtml(formatValue(report.trial_count || 0))}</strong>
      </div>
      <div>
        <span>Finite closed</span>
        <strong>${escapeHtml(formatValue(report.closed_finite_count || 0))}</strong>
      </div>
      <div>
        <span>Rejected</span>
        <strong>${escapeHtml(formatValue(report.rejected_count || 0))}</strong>
      </div>
    </div>
    <div class="search-trial-list">
      ${trials
        .map(
          (trial) => `
            <article class="search-trial is-${escapeHtml(trial.verdict || "unknown")}">
              <span>${escapeHtml(trial.id || "")} · ${escapeHtml(statusText(trial.verdict))}</span>
              <strong>${escapeHtml(trial.hypothesis || "")}</strong>
              <p>Execution: ${escapeHtml(trial.execution || "")}</p>
              <p>Observed: ${escapeHtml(trial.observed || "")}</p>
              <p>Blocker: ${escapeHtml(trial.blocker || "")}</p>
              <small>Proof upgrade: ${escapeHtml(trial.proof_upgrade || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(report.claim_rule || "")}</p>
  `;
}

function renderFormalUpgradeMatrix(problem) {
  const matrix = problem.formal_upgrade_matrix || {};
  const rows = matrix.rows || [];
  return `
    <div class="upgrade-matrix-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(matrix.status))}</strong>
      </div>
      <div>
        <span>Target theorem</span>
        <strong>${escapeHtml(matrix.target_theorem || "missing")}</strong>
      </div>
      <div>
        <span>Open rows</span>
        <strong>${escapeHtml(formatValue(matrix.open_row_count || 0))}</strong>
      </div>
      <div>
        <span>Review</span>
        <strong>${escapeHtml(statusText(matrix.review_status))}</strong>
      </div>
    </div>
    <div class="upgrade-matrix-table">
      ${rows
        .map(
          (row) => `
            <article class="upgrade-row is-${escapeHtml(row.status || "unknown")}">
              <span>${escapeHtml(row.stage || "")}</span>
              <strong>${escapeHtml(statusText(row.status))}</strong>
              <p>Artifact: ${escapeHtml(row.artifact || "")}</p>
              <p>Acceptance test: ${escapeHtml(row.acceptance_test || "")}</p>
              <small>Blocks full proof: ${escapeHtml(statusText(row.blocks_full_proof))}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(matrix.machine_rule || "")}</p>
  `;
}

function renderProofKernelRoadmap(problem) {
  const roadmap = problem.proof_kernel_roadmap || {};
  const steps = roadmap.steps || [];
  return `
    <div class="kernel-roadmap-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(roadmap.status))}</strong>
      </div>
      <div>
        <span>Namespace</span>
        <strong>${escapeHtml(roadmap.namespace || "missing")}</strong>
      </div>
      <div>
        <span>Target theorem</span>
        <strong>${escapeHtml(roadmap.target_theorem || "missing")}</strong>
      </div>
      <div>
        <span>Open steps</span>
        <strong>${escapeHtml(formatValue(roadmap.open_step_count || 0))}</strong>
      </div>
    </div>
    <article class="kernel-roadmap-risk">
      <span>Main file</span>
      <code>${escapeHtml(roadmap.main_file || "missing")}</code>
      <p>Shortcut risk: ${escapeHtml(roadmap.shortcut_risk || "")}</p>
    </article>
    <div class="kernel-roadmap-list">
      ${steps
        .map(
          (step) => `
            <article class="kernel-step is-${escapeHtml(step.status || "unknown")}">
              <span>${escapeHtml(step.id || "")} · ${escapeHtml(step.stage || "")}</span>
              <strong>${escapeHtml(statusText(step.status))}</strong>
              <p>Artifact: ${escapeHtml(step.artifact || "")}</p>
              <small>Acceptance test: ${escapeHtml(step.acceptance_test || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(roadmap.claim_rule || "")}</p>
  `;
}

function renderFormalKernelContractAudit(problem) {
  const audit = problem.formal_kernel_contract_audit || {};
  const rows = audit.rows || [];
  return `
    <div class="kernel-audit-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(audit.status))}</strong>
      </div>
      <div>
        <span>Package</span>
        <strong>${escapeHtml(audit.package_dir || "missing")}</strong>
      </div>
      <div>
        <span>Target theorem</span>
        <strong>${escapeHtml(audit.target_theorem || "missing")}</strong>
      </div>
      <div>
        <span>Blocked rows</span>
        <strong>${escapeHtml(formatValue(audit.blocked_row_count || 0))}</strong>
      </div>
    </div>
    <div class="kernel-audit-list">
      ${rows
        .map(
          (row) => `
            <article class="kernel-audit-row is-${escapeHtml(row.status || "unknown")}">
              <span>${escapeHtml(row.file || "")}</span>
              <strong>${escapeHtml(statusText(row.status))}</strong>
              <p>Expected fragments: ${escapeHtml(formatValue(row.expected_fragment_count || 0))}</p>
              <p>Missing: ${escapeHtml(formatValue(row.missing_fragments || []))}</p>
              <small>Forbidden hits: ${escapeHtml(formatValue(row.forbidden_hits || []))}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(audit.claim_rule || "")}</p>
  `;
}

function renderInvalidProofShortcutSuite(problem) {
  const suite = problem.invalid_proof_shortcut_suite || {};
  const shortcuts = suite.shortcuts || [];
  return `
    <div class="shortcut-suite-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(suite.status))}</strong>
      </div>
      <div>
        <span>Shortcuts</span>
        <strong>${escapeHtml(formatValue(suite.shortcut_count || 0))}</strong>
      </div>
      <div>
        <span>Rejected</span>
        <strong>${escapeHtml(formatValue(suite.rejected_count || 0))}</strong>
      </div>
      <div>
        <span>Certificate root</span>
        <code>${escapeHtml(String(suite.bounded_certificate_root || "missing").slice(0, 16))}</code>
      </div>
    </div>
    <div class="shortcut-suite-list">
      ${shortcuts
        .map(
          (item) => `
            <article class="shortcut-card is-${escapeHtml(item.verdict || "unknown")}">
              <span>${escapeHtml(item.id || "")} · ${escapeHtml(item.class || "")}</span>
              <strong>${escapeHtml(item.shortcut || "")}</strong>
              <em>${escapeHtml(statusText(item.verdict))}</em>
              <p>Red-team test: ${escapeHtml(item.red_team_test || "")}</p>
              <p>Rejection reason: ${escapeHtml(item.rejection_reason || "")}</p>
              <small>Kill condition: ${escapeHtml(item.kill_condition || "")}</small>
              <small>Required upgrade: ${escapeHtml(item.required_upgrade || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(suite.claim_rule || "")}</p>
  `;
}

function renderAiSolverFrontier(problem) {
  const frontier = problem.ai_solver_frontier || {};
  const steps = frontier.solver_steps || [];
  const searchSpace = frontier.search_space || [];
  const machineOutput = Object.entries(frontier.machine_output || {});
  return `
    <div class="ai-frontier-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(frontier.status))}</strong>
      </div>
      <div>
        <span>Engine</span>
        <strong>${escapeHtml(frontier.engine || "missing")}</strong>
      </div>
    </div>
    <article class="ai-frontier-thesis">
      <span>Novel attempt</span>
      <p>${escapeHtml(frontier.novel_attempt || "")}</p>
      <strong>${escapeHtml(frontier.best_current_candidate || "")}</strong>
      <small>Blocking obstruction: ${escapeHtml(frontier.blocking_obstruction || "")}</small>
    </article>
    <div class="ai-frontier-grid">
      <section>
        <h3>Search Space</h3>
        ${list(searchSpace)}
      </section>
      <section>
        <h3>Machine Output</h3>
        <div class="ai-output-list">
          ${machineOutput
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
    </div>
    <div class="ai-step-list">
      ${steps
        .map(
          (step) => `
            <article class="ai-step is-${escapeHtml(step.status || "unknown")}">
              <span>${escapeHtml(step.id || "")} · ${escapeHtml(step.stage || "")}</span>
              <strong>${escapeHtml(statusText(step.status))}</strong>
              <p>Acceptance test: ${escapeHtml(step.acceptance_test || "")}</p>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">Next experiment: ${escapeHtml(frontier.next_experiment || "")}</p>
    <p class="route-rule">${escapeHtml(frontier.claim_rule || "")}</p>
  `;
}

function renderAiBreakthroughProgram(problem) {
  const program = problem.ai_breakthrough_program || {};
  const anchors = program.literature_anchor || [];
  const experiments = program.machine_experiments || [];
  const redTeamRules = program.red_team_rules || [];
  return `
    <div class="ai-breakthrough-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(program.status))}</strong>
      </div>
      <div>
        <span>Program</span>
        <strong>${escapeHtml(program.program_title || "missing")}</strong>
      </div>
    </div>
    <article class="ai-breakthrough-thesis">
      <span>New attack</span>
      <p>${escapeHtml(program.new_hypothesis || "")}</p>
      <strong>Candidate theorem: ${escapeHtml(program.candidate_theorem || "")}</strong>
      <small>Current obstruction: ${escapeHtml(program.current_obstruction || "")}</small>
    </article>
    <div class="ai-breakthrough-grid">
      <section>
        <h3>Source-informed baseline</h3>
        <div class="breakthrough-anchor-list">
          ${anchors
            .map(
              (anchor) => `
                <article class="breakthrough-anchor">
                  <span>${escapeHtml(anchor.source || "")}</span>
                  <p>${escapeHtml(anchor.use || "")}</p>
                  <small>Boundary: ${escapeHtml(anchor.limit || "")}</small>
                  <a href="${escapeHtml(anchor.url || "#")}" target="_blank" rel="noreferrer">Source</a>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
      <section>
        <h3>Machine experiments</h3>
        <div class="breakthrough-experiment-list">
          ${experiments
            .map(
              (experiment) => `
                <article class="breakthrough-experiment">
                  <span>${escapeHtml(experiment.id || "")}</span>
                  <strong>${escapeHtml(experiment.purpose || "")}</strong>
                  <p>Artifact: ${escapeHtml(experiment.artifact || "")}</p>
                  <p>Pass condition: ${escapeHtml(experiment.pass_condition || "")}</p>
                  <small>Failure signal: ${escapeHtml(experiment.failure_signal || "")}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
    </div>
    <div class="ai-breakthrough-grid">
      <section>
        <h3>AI search protocol</h3>
        ${list(program.ai_search_protocol || [])}
      </section>
      <section>
        <h3>Red-team rules</h3>
        ${list(redTeamRules)}
      </section>
    </div>
    <p class="route-rule">First machine artifact: ${escapeHtml(program.first_machine_artifact || "")}</p>
    <p class="route-rule">Decisive success condition: ${escapeHtml(program.decisive_success_condition || "")}</p>
    <p class="route-rule">Upgrade condition: ${escapeHtml(program.upgrade_condition || "")}</p>
    <p class="route-rule">${escapeHtml(program.claim_rule || "")}</p>
  `;
}

function renderAiProofForge(problem) {
  const forge = problem.ai_proof_forge || {};
  const experiments = forge.experiments || [];
  const discovery = forge.discovery_loop || {};
  const mutations = discovery.candidate_mutations || [];
  const attackRunbook = discovery.attack_runbook || [];
  const scorecard = discovery.falsification_scorecard || [];
  const synthesis = discovery.cross_problem_synthesis || [];
  const portfolio = discovery.portfolio_decision || {};
  const rankedTracks = portfolio.ranked_tracks || [];
  const decomposition = forge.theorem_decomposition || [];
  const decompositionSummary = forge.decomposition_summary || {};
  const blueprint = forge.breakthrough_object_blueprint || {};
  const cegis = forge.counterexample_guided_synthesis || {};
  const theoremTicket = forge.top_attack_theorem_ticket || {};
  return `
    <div class="proof-forge-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(forge.status))}</strong>
      </div>
      <div>
        <span>Forge</span>
        <strong>${escapeHtml(forge.forge_title || "missing")}</strong>
      </div>
    </div>
    <article class="proof-forge-thesis">
      <span>Non-reproduction target</span>
      <strong>${escapeHtml(forge.minimal_breakthrough_theorem || "")}</strong>
      <p>${escapeHtml(forge.new_object || "")}</p>
      <small>${escapeHtml(forge.non_reproduction_rule || "")}</small>
    </article>
    <article class="proof-forge-theorem-draft">
      <span>Next theorem to attempt</span>
      <strong>${escapeHtml(forge.next_theorem_to_attempt || "")}</strong>
      <p>Lean statement draft: ${escapeHtml(forge.lean_statement_draft || "")}</p>
      <small>Proof objects needed: ${escapeHtml(formatValue(forge.proof_objects_needed || []))}</small>
    </article>
    <div class="proof-forge-decomposition">
      <div class="proof-forge-head">
        <div>
          <span>Theorem decomposition</span>
          <strong>${escapeHtml(statusText(decompositionSummary.status))}</strong>
        </div>
        <div>
          <span>Highest risk</span>
          <strong>${escapeHtml(decompositionSummary.highest_risk || "missing")} · ${escapeHtml(decompositionSummary.highest_risk_lemma || "")}</strong>
        </div>
      </div>
      <div class="proof-forge-decomposition-list">
        ${decomposition
          .map(
            (lemma) => `
              <article class="proof-forge-lemma is-${escapeHtml(lemma.status || "unknown")}">
                <span>${escapeHtml(lemma.id || "")} · ${escapeHtml(statusText(lemma.status))}</span>
                <strong>${escapeHtml(lemma.lemma || "")}</strong>
                <p>Role: ${escapeHtml(lemma.role || "")}</p>
                <p>Risk: ${escapeHtml(lemma.risk || "")}</p>
                <p>Proof artifact: ${escapeHtml(lemma.proof_artifact || "")}</p>
                <small>Failure test: ${escapeHtml(lemma.failure_test || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
      <p>${escapeHtml(decompositionSummary.closure_rule || "")}</p>
    </div>
    <article class="proof-forge-blueprint">
      <span>Breakthrough object blueprint</span>
      <strong>${escapeHtml(blueprint.target_lemma || "missing")} · ${escapeHtml(statusText(blueprint.status))}</strong>
      <p>New object family: ${escapeHtml(blueprint.new_object_family || "")}</p>
      <p>AI generation prompt: ${escapeHtml(blueprint.ai_generation_prompt || "")}</p>
      <p>Minimal counterexample: ${escapeHtml(blueprint.minimal_counterexample || "")}</p>
      <p>Falsification oracle: ${escapeHtml(blueprint.falsification_oracle || "")}</p>
      <p>Formalization seed: ${escapeHtml(blueprint.formalization_seed || "")}</p>
      <small>Success upgrade: ${escapeHtml(blueprint.success_upgrade || "")}</small>
      <div class="proof-forge-blueprint-next">
        ${(blueprint.next_experiments || [])
          .map((experiment) => `<em>${escapeHtml(experiment)}</em>`)
          .join("")}
      </div>
      <small>${escapeHtml(blueprint.why_not_reproduction || "")}</small>
    </article>
    <article class="proof-forge-cegis">
      <span>Counterexample-guided synthesis</span>
      <strong>${escapeHtml(cegis.loop_name || "missing")} · ${escapeHtml(statusText(cegis.status))}</strong>
      <p>Candidate schema: ${escapeHtml(cegis.candidate_schema || "")}</p>
      <p>Top CEGIS candidate: ${escapeHtml(cegis.top_candidate || "missing")}</p>
      <p>Ranking rule: ${escapeHtml(cegis.ranking_rule || "")}</p>
      <p>Promotion rule: ${escapeHtml(cegis.promotion_rule || "")}</p>
      <div class="proof-forge-cegis-grid">
        <section>
          <h3>Forbidden assumptions</h3>
          ${list(cegis.forbidden_assumptions || [])}
        </section>
        <section>
          <h3>Oracle pipeline</h3>
          ${list(cegis.oracle_pipeline || [])}
        </section>
      </div>
      <div class="proof-forge-cegis-candidates">
        ${(cegis.seed_candidates || [])
          .map(
            (candidate) => `
              <article>
                <span>${escapeHtml(candidate.id || "")}</span>
                <strong>${escapeHtml(candidate.candidate || "")}</strong>
                <p>Priority score: ${escapeHtml(formatValue(candidate.priority_score ?? "n/a"))} · Decision: ${escapeHtml(statusText(candidate.decision))}</p>
                <p>Expected failure: ${escapeHtml(candidate.expected_failure || "")}</p>
                <small>Next verifier: ${escapeHtml(candidate.next_verifier || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
      <div class="proof-forge-cegis-ranking">
        ${(cegis.ranked_candidates || [])
          .map(
            (candidate) => `
              <article>
                <span>#${escapeHtml(formatValue(candidate.rank || 0))} · ${escapeHtml(formatValue(candidate.priority_score ?? "n/a"))}</span>
                <strong>${escapeHtml(candidate.id || "")} · ${escapeHtml(statusText(candidate.decision))}</strong>
                <p>${escapeHtml(candidate.candidate || "")}</p>
                <small>Verifier: ${escapeHtml(candidate.next_verifier || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
    </article>
    <article class="proof-forge-ticket">
      <span>Top attack theorem ticket</span>
      <strong>${escapeHtml(theoremTicket.ticket_id || "missing")} · ${escapeHtml(statusText(theoremTicket.status))}</strong>
      <p>Source candidate: ${escapeHtml(theoremTicket.source_candidate || "")}</p>
      <p>Candidate theorem: ${escapeHtml(theoremTicket.candidate_theorem || "")}</p>
      <p>Target conclusion: ${escapeHtml(theoremTicket.target_conclusion || "")}</p>
      <p>First counterexample oracle: ${escapeHtml(theoremTicket.first_counterexample_oracle || "")}</p>
      <p>Required artifact: ${escapeHtml(theoremTicket.required_artifact || "")}</p>
      <p>Lean stub: ${escapeHtml(theoremTicket.lean_stub || "")}</p>
      <small>Success condition: ${escapeHtml(theoremTicket.success_condition || "")}</small>
      <div class="proof-forge-ticket-grid">
        <section>
          <h3>Input objects</h3>
          ${list(theoremTicket.input_objects || [])}
        </section>
        <section>
          <h3>Forbidden premises</h3>
          ${list(theoremTicket.forbidden_premises || [])}
        </section>
      </div>
      <div class="proof-forge-ticket-protocol">
        ${(theoremTicket.proof_attempt_protocol || [])
          .map(
            (step) => `
              <article>
                <span>${escapeHtml(step.step || "")}</span>
                <strong>${escapeHtml(step.action || "")}</strong>
                <p>Output: ${escapeHtml(step.output || "")}</p>
                <small>Fail exit: ${escapeHtml(step.fail_exit || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
    </article>
    <div class="proof-forge-grid">
      <section>
        <h3>Search grammar</h3>
        ${list(forge.search_grammar || [])}
      </section>
      <section>
        <h3>Countermodel battery</h3>
        ${list(forge.countermodel_battery || [])}
      </section>
    </div>
    <div class="proof-forge-experiments">
      ${experiments
        .map(
          (experiment) => `
            <article class="proof-forge-experiment">
              <span>${escapeHtml(experiment.id || "")}</span>
              <strong>${escapeHtml(experiment.generator || "")}</strong>
              <p>Artifact: ${escapeHtml(experiment.artifact || "")}</p>
              <p>Success rule: ${escapeHtml(experiment.success_rule || "")}</p>
              <small>Failure rule: ${escapeHtml(experiment.failure_rule || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <div class="proof-forge-discovery">
      <div class="proof-forge-head">
        <div>
          <span>Discovery loop</span>
          <strong>${escapeHtml(statusText(discovery.status))}</strong>
        </div>
        <div>
          <span>Survivors / blocked</span>
          <strong>${escapeHtml(formatValue(discovery.survivor_count || 0))} / ${escapeHtml(formatValue(discovery.blocked_count || 0))}</strong>
        </div>
      </div>
      <p>${escapeHtml(discovery.iteration_contract || "")}</p>
      <div class="proof-forge-mutations">
        ${mutations
          .map(
            (mutation) => `
              <article class="proof-forge-mutation is-${escapeHtml(mutation.current_verdict || "unknown")}">
                <span>${escapeHtml(mutation.id || "")} · ${escapeHtml(statusText(mutation.current_verdict))}</span>
                <strong>${escapeHtml(mutation.mutation || "")}</strong>
                <p>Theorem pressure: ${escapeHtml(mutation.theorem_pressure || "")}</p>
                <p>Verifier: ${escapeHtml(mutation.verifier || "")}</p>
                <small>Next action: ${escapeHtml(mutation.next_action || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
      <div class="proof-forge-runbook">
        <section>
          <h3>Attack runbook</h3>
          ${attackRunbook
            .map(
              (step) => `
                <article class="proof-forge-runbook-step">
                  <span>${escapeHtml(step.step || "")} · ${escapeHtml(step.name || "")}</span>
                  <strong>${escapeHtml(step.action || "")}</strong>
                  <p>Required output: ${escapeHtml(step.required_output || "")}</p>
                  <small>Failure exit: ${escapeHtml(step.failure_exit || "")}</small>
                </article>
              `,
            )
            .join("")}
        </section>
        <section>
          <h3>Falsification scorecard</h3>
          ${scorecard
            .map(
              (row) => `
                <article class="proof-forge-score">
                  <span>${escapeHtml(row.test || "")} · ${escapeHtml(statusText(row.status))}</span>
                  <strong>${escapeHtml(row.question || "")}</strong>
                  <p>Pass signal: ${escapeHtml(row.pass_signal || "")}</p>
                  <small>Fail signal: ${escapeHtml(row.fail_signal || "")}</small>
                </article>
              `,
            )
            .join("")}
        </section>
      </div>
      <div class="proof-forge-synthesis">
        <h3>Cross-problem synthesis</h3>
        <div class="proof-forge-synthesis-grid">
          ${synthesis
            .map(
              (item) => `
              <article class="proof-forge-synthesis-card is-${escapeHtml(item.status || "unknown")}">
                <span>${escapeHtml(item.pattern || "")} · ${escapeHtml(statusText(item.status))}</span>
                <strong>${escapeHtml(item.source_problem || "")} -> ${escapeHtml(item.target_problem || "")}</strong>
                <p>Hypothesis: ${escapeHtml(item.hypothesis || "")}</p>
                <p>Transfer test: ${escapeHtml(item.transfer_test || "")}</p>
                <p>Priority score: ${escapeHtml(formatValue(item.priority_score ?? "n/a"))} · Decision: ${escapeHtml(statusText(item.decision))}</p>
                <small>Failure mode: ${escapeHtml(item.failure_mode || "")}</small>
              </article>
              `,
            )
            .join("")}
        </div>
      </div>
      <div class="proof-forge-portfolio">
        <h3>Portfolio decision</h3>
        <div class="proof-forge-portfolio-head">
          <div>
            <span>Status</span>
            <strong>${escapeHtml(statusText(portfolio.status))}</strong>
          </div>
          <div>
            <span>Top candidate</span>
            <strong>${escapeHtml(portfolio.top_candidate || "missing")}</strong>
          </div>
        </div>
        <p>${escapeHtml(portfolio.ranking_rule || "")}</p>
        <p>${escapeHtml(portfolio.stop_rule || "")}</p>
        <div class="proof-forge-ranked-tracks">
          ${rankedTracks
            .map(
              (track) => `
                <article class="proof-forge-ranked-track">
                  <span>#${escapeHtml(formatValue(track.rank || 0))} · ${escapeHtml(formatValue(track.priority_score ?? "n/a"))}</span>
                  <strong>${escapeHtml(track.pattern || "")}</strong>
                  <p>${escapeHtml(track.source_problem || "")} -> ${escapeHtml(track.target_problem || "")}</p>
                  <small>${escapeHtml(statusText(track.decision))}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </div>
    </div>
    <p class="route-rule">Formal target: ${escapeHtml(forge.formal_target || "")}</p>
    <p class="route-rule">Promotion gate: ${escapeHtml(forge.promotion_gate || "")}</p>
  `;
}

function renderProofRouteTriage(problem) {
  const triage = problem.proof_route_triage || {};
  const routes = triage.routes || [];
  return `
    <div class="route-triage-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(triage.status))}</strong>
      </div>
      <div>
        <span>Routes</span>
        <strong>${escapeHtml(formatValue(triage.route_count || 0))}</strong>
      </div>
      <div>
        <span>Rejected</span>
        <strong>${escapeHtml(formatValue(triage.rejected_count || 0))}</strong>
      </div>
      <div>
        <span>Current route</span>
        <strong>${escapeHtml(triage.current_decisive_route || "missing")}</strong>
      </div>
    </div>
    <div class="route-triage-list">
      ${routes
        .map(
          (route) => `
            <article class="route-card is-${escapeHtml(route.status || "unknown")}">
              <span>${escapeHtml(route.id || "")}</span>
              <strong>${escapeHtml(route.route || "")}</strong>
              <em>${escapeHtml(statusText(route.status))}</em>
              <p>Machine test: ${escapeHtml(route.machine_test || "")}</p>
              <small>Required upgrade: ${escapeHtml(route.required_upgrade || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(triage.machine_rule || "")}</p>
  `;
}

function renderDecisiveTheoremSpec(problem) {
  const spec = problem.decisive_theorem_spec || {};
  return `
    <div class="theorem-spec-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(spec.status))}</strong>
      </div>
      <div>
        <span>Target route</span>
        <strong>${escapeHtml(spec.target_route || "missing")}</strong>
      </div>
      <div>
        <span>Artifact</span>
        <strong>${escapeHtml(statusText(spec.artifact_status))}</strong>
      </div>
      <div>
        <span>Spec</span>
        <strong>${escapeHtml(spec.spec_id || "missing")}</strong>
      </div>
    </div>
    <article class="theorem-statement-card">
      <span>${escapeHtml(spec.title || "")}</span>
      <p>${escapeHtml(spec.candidate_statement || "")}</p>
      <small>Blocking gap: ${escapeHtml(spec.blocking_gap || "")}</small>
    </article>
    <div class="theorem-spec-grid">
      <section>
        <h3>Allowed Inputs</h3>
        ${list(spec.allowed_inputs || [])}
      </section>
      <section>
        <h3>Forbidden Shortcuts</h3>
        ${list(spec.forbidden_shortcuts || [])}
      </section>
      <section>
        <h3>Machine Checks</h3>
        ${list(spec.machine_checks || [])}
      </section>
      <section>
        <h3>Would Close</h3>
        ${list(spec.would_close || [])}
      </section>
    </div>
    <p class="route-rule">${escapeHtml(spec.promotion_rule || "")}</p>
  `;
}

function renderDecisiveTheoremSubgoals(problem) {
  const report = problem.decisive_theorem_subgoals || {};
  const subgoals = report.subgoals || [];
  return `
    <div class="subgoal-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(report.status))}</strong>
      </div>
      <div>
        <span>Complete</span>
        <strong>${escapeHtml(formatValue(report.complete_count || 0))}</strong>
      </div>
      <div>
        <span>Open</span>
        <strong>${escapeHtml(formatValue(report.open_count || 0))}</strong>
      </div>
      <div>
        <span>Blocked</span>
        <strong>${escapeHtml(formatValue(report.blocked_count || 0))}</strong>
      </div>
    </div>
    <div class="subgoal-list">
      ${subgoals
        .map(
          (item) => `
            <article class="subgoal-card is-${escapeHtml(item.status || "unknown")}">
              <span>${escapeHtml(item.id || "")}</span>
              <strong>${escapeHtml(item.label || "")}</strong>
              <em>${escapeHtml(statusText(item.status))}</em>
              <p>Artifact: ${escapeHtml(item.artifact || "")}</p>
              <small>Closing test: ${escapeHtml(item.closing_test || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(report.machine_rule || "")}</p>
  `;
}

function renderDecisiveTheoremAttackTickets(problem) {
  const report = problem.decisive_theorem_attack_tickets || {};
  const tickets = report.tickets || [];
  return `
    <div class="attack-ticket-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(report.status))}</strong>
      </div>
      <div>
        <span>Tickets</span>
        <strong>${escapeHtml(formatValue(report.ticket_count || 0))}</strong>
      </div>
      <div>
        <span>P0</span>
        <strong>${escapeHtml(formatValue(report.p0_count || 0))}</strong>
      </div>
    </div>
    <div class="attack-ticket-list">
      ${tickets
        .map(
          (ticket) => `
            <article class="attack-ticket-card is-${escapeHtml(ticket.priority || "P1")}">
              <span>${escapeHtml(ticket.id || "")} · ${escapeHtml(ticket.subgoal_id || "")}</span>
              <strong>${escapeHtml(ticket.attack_hypothesis || "")}</strong>
              <em>${escapeHtml(ticket.priority || "")} · ${escapeHtml(statusText(ticket.status))}</em>
              <p>First experiment: ${escapeHtml(ticket.first_experiment || "")}</p>
              <p>Falsification test: ${escapeHtml(ticket.falsification_test || "")}</p>
              <small>Required output: ${escapeHtml(ticket.required_output || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(report.machine_rule || "")}</p>
  `;
}

function renderProofBreakthroughAgenda(problem) {
  const agenda = problem.proof_breakthrough_agenda || {};
  const routes = agenda.routes || [];
  return `
    <div class="breakthrough-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(agenda.status))}</strong>
      </div>
      <div>
        <span>Routes</span>
        <strong>${escapeHtml(formatValue(agenda.route_count || 0))}</strong>
      </div>
      <div>
        <span>Barriers</span>
        <strong>${escapeHtml(formatValue(agenda.barrier_count || 0))}</strong>
      </div>
      <div>
        <span>Target spec</span>
        <strong>${escapeHtml(agenda.target_spec || "missing")}</strong>
      </div>
    </div>
    <div class="breakthrough-list">
      ${routes
        .map(
          (route) => `
            <article class="breakthrough-card">
              <span>${escapeHtml(route.id || "")} · ${escapeHtml(route.barrier_target || "")}</span>
              <strong>${escapeHtml(route.novelty_claim || "")}</strong>
              <em>${escapeHtml(statusText(route.status))}</em>
              <p>Minimum new theorem: ${escapeHtml(route.minimum_new_theorem || "")}</p>
              <p>First artifact: ${escapeHtml(route.first_artifact || "")}</p>
              <p>Kill condition: ${escapeHtml(route.kill_condition || "")}</p>
              <small>Tools: ${escapeHtml(formatValue(route.uses_primeproject_tools || []))}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="route-rule">${escapeHtml(agenda.machine_rule || "")}</p>
  `;
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

function renderProofExecutionProtocol(problem) {
  const protocol = problem.proof_execution_protocol || {};
  const stages = protocol.stages || [];
  return `
    <div class="execution-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(protocol.status))}</strong>
      </div>
      <div>
        <span>Mode</span>
        <strong>${escapeHtml(statusText(protocol.execution_mode))}</strong>
      </div>
      <div>
        <span>Primary gap</span>
        <strong>${escapeHtml(protocol.primary_open_gap || "missing")}</strong>
      </div>
    </div>
    <div class="execution-frontier">
      <span>Current frontier</span>
      <p>${escapeHtml(protocol.current_frontier || "")}</p>
      <span>Next experiment</span>
      <p>${escapeHtml(protocol.primary_next_experiment || "")}</p>
      <span>Failure signal</span>
      <p>${escapeHtml(protocol.primary_failure_signal || "")}</p>
    </div>
    <div class="execution-stage-list">
      ${stages
        .map(
          (stage) => `
            <article class="execution-stage is-${escapeHtml(stage.status || "missing")}">
              <span>${escapeHtml(stage.id || "")}</span>
              <strong>${escapeHtml(stage.name || "")}</strong>
              <em>${escapeHtml(statusText(stage.status))}</em>
              <p>${escapeHtml(stage.proof_value || "")}</p>
              <small>Required output: ${escapeHtml(stage.required_output || "")}</small>
              <small>Verifier: ${escapeHtml(stage.verifier || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="certificate-verifier">${escapeHtml(protocol.promotion_rule || "")}</p>
  `;
}

function renderProofFrontierProbe(problem) {
  const probe = problem.proof_frontier_probe || {};
  const metrics = Object.entries(probe.metrics || {});
  const observations = probe.observations || [];
  return `
    <div class="frontier-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(probe.status))}</strong>
      </div>
      <div>
        <span>Limit</span>
        <strong>${escapeHtml(formatValue(probe.limit))}</strong>
      </div>
      <div>
        <span>Objective</span>
        <strong>${escapeHtml(probe.objective || "")}</strong>
      </div>
    </div>
    <div class="frontier-grid">
      <section>
        <h3>Stress Metrics</h3>
        <div class="proof-gate-table">
          ${metrics
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
        <h3>Observations</h3>
        <div class="frontier-observations">
          ${observations
            .map(
              (item) => `
                <div>
                  <span>${escapeHtml(item.label || "")}</span>
                  <strong>${escapeHtml(formatValue(item.value))}</strong>
                </div>
              `,
            )
            .join("")}
        </div>
      </section>
    </div>
    <div class="frontier-pressure">
      <strong>Proof pressure</strong>
      <p>${escapeHtml(probe.proof_pressure || "")}</p>
      <strong>Failure signal</strong>
      <p>${escapeHtml(probe.failure_signal || "")}</p>
      <small>${escapeHtml(probe.promotion_rule || "")}</small>
    </div>
  `;
}

function renderKnownBarrierAudit(problem) {
  const audit = problem.known_barrier_audit || {};
  const barriers = audit.barriers || [];
  return `
    <div class="barrier-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(audit.status))}</strong>
      </div>
      <div>
        <span>Open barriers</span>
        <strong>${escapeHtml(formatValue(audit.open_count || 0))}</strong>
      </div>
      <div>
        <span>Cleared</span>
        <strong>${escapeHtml(formatValue(audit.cleared_count || 0))}</strong>
      </div>
    </div>
    <div class="barrier-list">
      ${barriers
        .map(
          (barrier) => `
            <article class="barrier-card is-${escapeHtml(barrier.status || "missing")}">
              <span>${escapeHtml(barrier.id || "")}</span>
              <strong>${escapeHtml(barrier.barrier || "")}</strong>
              <em>${escapeHtml(statusText(barrier.status))}</em>
              <p>${escapeHtml(barrier.why_it_matters || "")}</p>
              <small>Clearance: ${escapeHtml(barrier.required_clearance || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="certificate-verifier">${escapeHtml(audit.promotion_rule || "")}</p>
  `;
}

function renderFormalReplayPackage(problem) {
  const replay = problem.formal_replay_package || {};
  const artifacts = replay.required_artifacts || [];
  const files = replay.candidate_files || [];
  const commands = replay.replay_commands || [];
  const forbidden = replay.forbidden_tokens || [];
  return `
    <div class="replay-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(replay.status))}</strong>
      </div>
      <div>
        <span>Kernel</span>
        <strong>${escapeHtml(replay.target_kernel || "missing")}</strong>
      </div>
      <div>
        <span>Package</span>
        <strong>${escapeHtml(replay.package_dir || "missing")}</strong>
      </div>
      <div>
        <span>Open barriers</span>
        <strong>${escapeHtml(formatValue(replay.open_barriers || 0))}</strong>
      </div>
    </div>
    <pre class="formal-statement"><code>${escapeHtml(replay.theorem_statement || "")}</code></pre>
    <div class="replay-grid">
      <section>
        <h3>Candidate files</h3>
        ${list(files)}
      </section>
      <section>
        <h3>Replay commands</h3>
        ${list(commands)}
      </section>
      <section>
        <h3>Required artifacts</h3>
        <div class="replay-artifacts">
          ${artifacts
            .map(
              (artifact) => `
                <div>
                  <span>${escapeHtml(artifact.name || "")}</span>
                  <strong>${escapeHtml(statusText(artifact.status))}</strong>
                  <code>${escapeHtml(formatValue(artifact.value))}</code>
                </div>
              `,
            )
            .join("")}
        </div>
      </section>
      <section>
        <h3>Forbidden tokens</h3>
        ${list(forbidden)}
      </section>
    </div>
    <p class="certificate-verifier">${escapeHtml(replay.acceptance_rule || "")}</p>
  `;
}

function renderProofReviewDocket(problem) {
  const docket = problem.proof_review_docket || {};
  const verdicts = docket.verdicts || [];
  return `
    <div class="review-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(docket.status))}</strong>
      </div>
      <div>
        <span>Stage</span>
        <strong>${escapeHtml(statusText(docket.review_stage))}</strong>
      </div>
      <div>
        <span>Reviewer stance</span>
        <strong>${escapeHtml(docket.reviewer_stance || "")}</strong>
      </div>
    </div>
    <div class="review-verdicts">
      ${verdicts
        .map(
          (item) => `
            <article class="review-card is-${escapeHtml(item.verdict || "missing")}">
              <span>${escapeHtml(item.claim || "")}</span>
              <strong>${escapeHtml(statusText(item.verdict))}</strong>
              <code>${escapeHtml(formatValue(item.evidence))}</code>
              <p>${escapeHtml(item.reason || "")}</p>
            </article>
          `,
        )
        .join("")}
    </div>
    <div class="review-rules">
      <section>
        <h3>Minimum acceptance conditions</h3>
        ${list(docket.minimum_acceptance_conditions || [])}
      </section>
      <section>
        <h3>Rejection rule</h3>
        <p>${escapeHtml(docket.rejection_rule || "")}</p>
      </section>
    </div>
  `;
}

function renderProofReductionContract(problem) {
  const contract = problem.proof_reduction_contract || {};
  const reduction = contract.decisive_reduction || {};
  const partials = contract.accepted_partial_results || [];
  return `
    <div class="reduction-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(contract.status))}</strong>
      </div>
      <div>
        <span>Bridge</span>
        <strong>${escapeHtml(statusText(contract.bridge_status))}</strong>
      </div>
      <div>
        <span>Goal</span>
        <strong>${escapeHtml(contract.goal || "")}</strong>
      </div>
    </div>
    <div class="reduction-main">
      <section>
        <h3>Decisive reduction</h3>
        <p>${escapeHtml(reduction.statement || "")}</p>
        <small>Would promote if: ${escapeHtml(reduction.would_promote_if || "")}</small>
        <small>Missing artifact: ${escapeHtml(reduction.missing_artifact || "")}</small>
      </section>
      <section>
        <h3>Accepted partial results</h3>
        <div class="reduction-partials">
          ${partials
            .map(
              (item) => `
                <article>
                  <span>${escapeHtml(item.name || "")}</span>
                  <strong>${escapeHtml(item.allowed_use || "")}</strong>
                  <small>Does not prove: ${escapeHtml(item.does_not_prove || "")}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
    </div>
    <div class="reduction-rules">
      <section>
        <h3>Forbidden shortcuts</h3>
        ${list(contract.forbidden_shortcuts || [])}
      </section>
      <section>
        <h3>Review questions</h3>
        ${list(contract.review_questions || [])}
      </section>
      <section>
        <h3>Promotion test</h3>
        <p>${escapeHtml(contract.promotion_test || "")}</p>
      </section>
    </div>
  `;
}

function renderProofCandidateIntake(problem) {
  const intake = problem.proof_candidate_intake || {};
  const submissions = intake.required_submission || [];
  const tests = intake.first_executable_tests || [];
  return `
    <div class="candidate-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(intake.status))}</strong>
      </div>
      <div>
        <span>Stage</span>
        <strong>${escapeHtml(statusText(intake.intake_stage))}</strong>
      </div>
      <div>
        <span>Candidate target</span>
        <strong>${escapeHtml(intake.candidate_target || "")}</strong>
      </div>
    </div>
    <div class="candidate-grid">
      <section>
        <h3>Required submission</h3>
        <div class="candidate-list">
          ${submissions
            .map(
              (item) => `
                <article>
                  <span>${escapeHtml(item.name || "")}</span>
                  <strong>${escapeHtml(item.format || "")}</strong>
                  <small>${escapeHtml(item.minimum_content || "")}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
      <section>
        <h3>First executable tests</h3>
        <div class="candidate-list">
          ${tests
            .map(
              (item) => `
                <article>
                  <span>${escapeHtml(item.id || "")} · ${escapeHtml(item.name || "")}</span>
                  <strong>${escapeHtml(item.pass_condition || "")}</strong>
                  <small>Reject if: ${escapeHtml(item.reject_if || "")}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
    </div>
    <div class="candidate-rules">
      <section>
        <h3>Automatic rejection rules</h3>
        ${list(intake.automatic_rejection_rules || [])}
      </section>
      <section>
        <h3>Review output</h3>
        <div class="candidate-output">
          ${Object.entries(intake.review_output || {})
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
      </section>
      <section>
        <h3>Claim boundary</h3>
        <p>${escapeHtml(intake.claim_boundary || "")}</p>
      </section>
    </div>
  `;
}

function renderProofAttemptExecutionLog(problem) {
  const log = problem.proof_attempt_execution_log || {};
  const attempts = log.attempts || [];
  return `
    <div class="execution-log-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(log.status))}</strong>
      </div>
      <div>
        <span>Candidate tests</span>
        <strong>${escapeHtml(formatValue(log.candidate_test_count || 0))}</strong>
      </div>
      <div>
        <span>Frontier objective</span>
        <strong>${escapeHtml(log.frontier_objective || "")}</strong>
      </div>
    </div>
    <div class="execution-log-list">
      ${attempts
        .map(
          (item) => `
            <article class="execution-log-card is-${escapeHtml(item.result || "open")}">
              <span>${escapeHtml(item.id || "")}</span>
              <strong>${escapeHtml(item.route || "")}</strong>
              <small>Machine check: ${escapeHtml(item.machine_check || "")}</small>
              <em>${escapeHtml(statusText(item.result))}</em>
              <p>${escapeHtml(item.failure_reason || "")}</p>
              <small>Next artifact: ${escapeHtml(item.next_artifact || "")}</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <div class="execution-log-rules">
      <section>
        <h3>Blocking gap</h3>
        <p>${escapeHtml(log.blocking_gap || "")}</p>
      </section>
      <section>
        <h3>Decisive missing artifact</h3>
        <p>${escapeHtml(log.decisive_missing_artifact || "")}</p>
      </section>
      <section>
        <h3>Machine verdict</h3>
        <p>${escapeHtml(log.machine_verdict || "")}</p>
        <small>${escapeHtml(log.publication_rule || "")}</small>
      </section>
    </div>
  `;
}

function renderProofObligationDag(problem) {
  const dag = problem.proof_obligation_dag || {};
  const nodes = dag.nodes || [];
  const edges = dag.edges || [];
  return `
    <div class="dag-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(dag.status))}</strong>
      </div>
      <div>
        <span>Nodes</span>
        <strong>${escapeHtml(formatValue(dag.node_count || nodes.length))}</strong>
      </div>
      <div>
        <span>Edges</span>
        <strong>${escapeHtml(formatValue(dag.edge_count || edges.length))}</strong>
      </div>
      <div>
        <span>Open nodes</span>
        <strong>${escapeHtml(formatValue(dag.open_node_count || 0))}</strong>
      </div>
    </div>
    <div class="dag-grid">
      <section>
        <h3>Obligation nodes</h3>
        <div class="dag-node-list">
          ${nodes
            .map(
              (node) => `
                <article class="dag-node is-${escapeHtml(node.status || "open")}">
                  <span>${escapeHtml(node.id || "")} · ${escapeHtml(node.type || "")}</span>
                  <strong>${escapeHtml(node.label || "")}</strong>
                  <em>${escapeHtml(statusText(node.status))}</em>
                  <small>${escapeHtml(node.required_artifact || "")}</small>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
      <section>
        <h3>Dependency edges</h3>
        <div class="dag-edge-list">
          ${edges
            .map(
              (edge) => `
                <article>
                  <span>${escapeHtml(edge.from || "")} -> ${escapeHtml(edge.to || "")}</span>
                  <strong>${escapeHtml(statusText(edge.status))}</strong>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>
    </div>
    <div class="dag-rule">
      <section>
        <h3>Critical path</h3>
        ${list(dag.critical_path || [])}
      </section>
      <section>
        <h3>Machine rule</h3>
        <p>${escapeHtml(dag.machine_rule || "")}</p>
      </section>
    </div>
  `;
}

function renderFormalSkeletonAudit(problem) {
  const audit = problem.formal_skeleton_audit || {};
  const files = audit.file_checks || [];
  return `
    <div class="skeleton-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(audit.status))}</strong>
      </div>
      <div>
        <span>Files present</span>
        <strong>${escapeHtml(formatValue(audit.present_count || 0))} / ${escapeHtml(formatValue(audit.candidate_file_count || 0))}</strong>
      </div>
      <div>
        <span>Forbidden hits</span>
        <strong>${escapeHtml(formatValue(audit.forbidden_hit_count || 0))}</strong>
      </div>
    </div>
    <div class="skeleton-file-list">
      ${files
        .map(
          (item) => `
            <article class="skeleton-file is-${escapeHtml(item.status || "missing")}">
              <span>${escapeHtml(item.path || "")}</span>
              <strong>${escapeHtml(statusText(item.status))}</strong>
              <small>${escapeHtml(formatValue(item.line_count || 0))} lines</small>
            </article>
          `,
        )
        .join("")}
    </div>
    <p class="skeleton-boundary">${escapeHtml(audit.claim_boundary || "")}</p>
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
  const taxonomy = lab.proof_gap_taxonomy || {};
  const gaps = taxonomy.gaps || [];
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
    <div class="proof-gap-taxonomy">
      <div class="proof-gap-head">
        <span>Proof Gap Taxonomy</span>
        <strong>${escapeHtml(statusText(taxonomy.status))}</strong>
        <em>${escapeHtml(formatValue(taxonomy.open_gap_count || 0))} open / ${escapeHtml(formatValue(taxonomy.blocked_gap_count || 0))} blocked</em>
      </div>
      <div class="proof-gap-list">
        ${gaps
          .map(
            (gap) => `
              <article class="proof-gap-card is-${escapeHtml(gap.status || "open")}">
                <span>${escapeHtml(gap.id || "")} · ${escapeHtml(gap.type || "")}</span>
                <strong>${escapeHtml(statusText(gap.status))}</strong>
                <p>${escapeHtml(gap.description || "")}</p>
                <small>Required artifact: ${escapeHtml(gap.required_artifact || "")}</small>
                <small>Next experiment: ${escapeHtml(gap.next_experiment || "")}</small>
                <small>Failure signal: ${escapeHtml(gap.failure_signal || "")}</small>
              </article>
            `,
          )
          .join("")}
      </div>
      <p>${escapeHtml(taxonomy.closure_rule || "")}</p>
    </div>
  `;
}

function renderTicket17Breakthrough(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 8);
  return `
    <div class="poc-ticket17">
      <h3>Ticket 17 breakthrough attempt</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Bounded result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket18Reduction(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket18">
      <h3>Ticket 18 reduction lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Reduction result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket19ProofPressure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket19">
      <h3>Ticket 19 proof pressure lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Proof pressure result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket20ValuationPrefix(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket20">
      <h3>Ticket 20 valuation-prefix lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Valuation-prefix result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket21TwoAdicBranch(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket21">
      <h3>Ticket 21 two-adic branch lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Two-adic branch result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket22NegationPressure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket22">
      <h3>Ticket 22 negation pressure lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Negation pressure result", "Value"], summaryRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket23Evidence(attempt) {
  const bounded = attempt?.bounded_result || {};
  if (Array.isArray(bounded.detector_rows)) {
    return table(
      ["beta", "height", "first negative", "first below threshold", "threshold seen"],
      bounded.detector_rows.slice(0, 12).map((row) => [
        row.offcritical_beta,
        row.height,
        row.first_negative_li_index,
        row.first_below_threshold_index,
        row.threshold_seen,
      ]),
    );
  }
  if (Array.isArray(bounded.modulus_rows)) {
    return table(
      ["bits", "states", "cycles", "false cycles", "integer rank nondecrease"],
      bounded.modulus_rows.map((row) => [
        row.modulus_bits,
        row.odd_state_count,
        row.cycle_component_count,
        row.nontrivial_cycle_component_count,
        row.integer_rank_nondecreasing_rate,
      ]),
    );
  }
  if (Array.isArray(bounded.sample_decompositions)) {
    const hardest = bounded.hardest_smallest_prime_witness || {};
    return [
      table(["even", "p", "q"], bounded.sample_decompositions.map((row) => [row.even, row.p, row.q])),
      `<p class="proof-note">Hardest bounded witness: ${escapeHtml(formatValue(hardest.even))} = ${escapeHtml(formatValue(hardest.smallest_prime))} + ${escapeHtml(formatValue(hardest.partner))}</p>`,
    ].join("");
  }
  if (Array.isArray(bounded.projection_rows)) {
    return table(
      ["limit", "gap 2", "deletion gap 2", "bounded retention"],
      bounded.projection_rows.map((row) => [
        row.limit,
        row.original_exact_gap_2,
        row.deletion_model_exact_gap_2,
        row.bounded_gap_retention_ratio,
      ]),
    );
  }
  return "";
}

function renderTicket23CegisRank(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket23">
      <h3>Ticket 23 CEGIS rank lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["CEGIS rank result", "Value"], summaryRows) : ""}
      ${renderTicket23Evidence(attempt)}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket24Evidence(attempt) {
  const bounded = attempt?.bounded_result || {};
  if (Array.isArray(bounded.detector_budget_rows)) {
    return table(
      ["beta", "height", "search cap", "threshold index", "seen"],
      bounded.detector_budget_rows.map((row) => [
        row.offcritical_beta,
        row.height,
        row.search_limit,
        row.first_below_threshold_index,
        row.threshold_seen,
      ]),
    );
  }
  if (Array.isArray(bounded.lift_rows)) {
    return table(
      ["bits", "states", "nontrivial cycles", "largest cycle", "rank nondecrease"],
      bounded.lift_rows.map((row) => [
        row.modulus_bits,
        row.odd_state_count,
        row.nontrivial_cycle_component_count,
        row.largest_cycle_component_size,
        row.integer_rank_nondecreasing_rate,
      ]),
    );
  }
  if (Array.isArray(bounded.sampled_count_rows)) {
    return [
      table(
        ["even", "representations", "N/log^2N", "ratio"],
        bounded.sampled_count_rows.slice(0, 12).map((row) => [
          row.even,
          row.representation_count,
          row.n_over_log_squared_n,
          row.count_to_scale_ratio,
        ]),
      ),
      `<p class="proof-note">Weakest sampled ratio: ${escapeHtml(formatValue(bounded.weakest_sampled_count_to_scale_ratio?.even))} with ratio ${escapeHtml(formatValue(bounded.weakest_sampled_count_to_scale_ratio?.count_to_scale_ratio))}</p>`,
    ].join("");
  }
  if (Array.isArray(bounded.weight_rows)) {
    return table(
      ["limit", "gap 2 margin", "bounded retention", "bounded w/o gap 2 retention"],
      bounded.weight_rows.map((row) => [
        row.limit,
        row.exact_gap_weight_margin,
        row.bounded_gap_retention_ratio,
        row.bounded_without_gap_2_retention_ratio,
      ]),
    );
  }
  return "";
}

function renderTicket24BridgeWeight(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  return `
    <div class="poc-ticket17 poc-ticket24">
      <h3>Ticket 24 bridge-weight lab</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Bridge-weight result", "Value"], summaryRows) : ""}
      ${renderTicket24Evidence(attempt)}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket25FormalKernel(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 10);
  const kernelRows = Array.isArray(bounded.kernel_rows)
    ? table(
        ["#", "Kernel row"],
        bounded.kernel_rows.slice(0, 8).map((row, index) => [index + 1, JSON.stringify(row)]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket25">
      <h3>Ticket 25 formal lemma kernel</h3>
      <div class="poc-head">
        <div>
          <span>Status</span>
          <strong>${escapeHtml(statusText(attempt.status))}</strong>
        </div>
        <div>
          <span>Route</span>
          <strong>${escapeHtml(attempt.route || "missing")}</strong>
        </div>
        <div>
          <span>Mode</span>
          <strong>${escapeHtml(statusText(attempt.proof_or_counterexample_mode))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Formal kernel result", "Value"], summaryRows) : ""}
      ${kernelRows}
      <div class="poc-bridge">
        <section>
          <h3>Formal kernel statement</h3>
          <p>${escapeHtml(attempt.formal_kernel_statement || "")}</p>
        </section>
        <section>
          <h3>Obstruction</h3>
          <p>${escapeHtml(attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderProofOrCounterexample(ticket, breakthroughTicket, reductionTicket, pressureTicket, valuationPrefixTicket, twoAdicBranchTicket, negationPressureTicket, cegisRankTicket, bridgeWeightTicket, formalKernelTicket) {
  if (!ticket) {
    return `<div class="proof-note is-error">Proof-or-counterexample lab artifact is not available on this page.</div>`;
  }
  const direct = ticket.direct_counterexample || {};
  const candidate = ticket.candidate_counterexamples_found || {};
  const directRows = Object.entries(direct)
    .filter(([key]) => !["candidates"].includes(key))
    .slice(0, 8);
  const examples = candidate.examples || direct.candidates || [];
  const exampleRows = Array.isArray(examples)
    ? examples.slice(0, 6).map((item, index) => [
        index + 1,
        typeof item === "object" ? JSON.stringify(item) : item,
      ])
    : [];

  return `
    <div class="poc-head">
      <div>
        <span>Status</span>
        <strong>${escapeHtml(statusText(ticket.status))}</strong>
      </div>
      <div>
        <span>Ticket</span>
        <strong>${escapeHtml(ticket.ticket_id || "missing")}</strong>
      </div>
      <div>
        <span>Next theorem</span>
        <strong>${escapeHtml(ticket.next_theorem_to_attempt || "missing")}</strong>
      </div>
    </div>
    <div class="poc-grid">
      <section>
        <h3>Proof modes</h3>
        ${list(ticket.proof_modes || [])}
      </section>
      <section>
        <h3>Direct counterexample search</h3>
        ${table(["Field", "Value"], directRows)}
      </section>
      <section>
        <h3>Candidate-proof falsification</h3>
        <p><strong>Target claim:</strong> ${escapeHtml(candidate.target_claim || "missing")}</p>
        <p><strong>Result:</strong> ${escapeHtml(statusText(candidate.result))}</p>
        <p>${escapeHtml(candidate.reason || "")}</p>
      </section>
      <section>
        <h3>Contrapositive route</h3>
        <p>${escapeHtml(ticket.contrapositive_route || "")}</p>
      </section>
    </div>
    ${
      exampleRows.length
        ? `<div class="poc-examples"><h3>Counterexample or stress examples</h3>${table(["#", "Example"], exampleRows)}</div>`
        : ""
    }
    <div class="poc-bridge">
      <section>
        <h3>Missing infinite bridge</h3>
        <p>${escapeHtml(ticket.missing_infinite_bridge || "")}</p>
      </section>
      <section>
        <h3>Claim boundary</h3>
        <p>${escapeHtml(ticket.claim_boundary || "")}</p>
      </section>
    </div>
    ${renderTicket17Breakthrough(breakthroughTicket)}
    ${renderTicket18Reduction(reductionTicket)}
    ${renderTicket19ProofPressure(pressureTicket)}
    ${renderTicket20ValuationPrefix(valuationPrefixTicket)}
    ${renderTicket21TwoAdicBranch(twoAdicBranchTicket)}
    ${renderTicket22NegationPressure(negationPressureTicket)}
    ${renderTicket23CegisRank(cegisRankTicket)}
    ${renderTicket24BridgeWeight(bridgeWeightTicket)}
    ${renderTicket25FormalKernel(formalKernelTicket)}
  `;
}

function render(payload, problem, proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt) {
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
  const existingGuide = document.querySelector("#problemKoGuide");
  if (existingGuide) existingGuide.innerHTML = problemKoGuide(problem);

  document.querySelector("#problemNav").innerHTML = [
    `<a href="index.html">Workbench</a>`,
    ...Object.entries(pageLinks).map(
      ([id, href]) => `<a class="${id === problem.id ? "is-active" : ""}" href="${href}">${labels[id]}</a>`,
    ),
  ].join("");

  document.querySelector("#proofVerdict").innerHTML = renderProofVerdict(problem);
  document.querySelector("#actualProofAttemptRunner").innerHTML = renderActualProofAttemptRunner(problem);
  const pocPanel = document.querySelector("#proofOrCounterexampleLab");
  if (pocPanel) pocPanel.innerHTML = renderProofOrCounterexample(proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt);
  document.querySelector("#candidateLemmaWorkbench").innerHTML = renderCandidateLemmaWorkbench(problem);
  document.querySelector("#machineProofSearchTrials").innerHTML = renderMachineProofSearchTrials(problem);
  document.querySelector("#formalUpgradeMatrix").innerHTML = renderFormalUpgradeMatrix(problem);
  document.querySelector("#proofKernelRoadmap").innerHTML = renderProofKernelRoadmap(problem);
  document.querySelector("#formalKernelContractAudit").innerHTML = renderFormalKernelContractAudit(problem);
  document.querySelector("#invalidProofShortcutSuite").innerHTML = renderInvalidProofShortcutSuite(problem);
  document.querySelector("#aiSolverFrontier").innerHTML = renderAiSolverFrontier(problem);
  document.querySelector("#aiBreakthroughProgram").innerHTML = renderAiBreakthroughProgram(problem);
  document.querySelector("#aiProofForge").innerHTML = renderAiProofForge(problem);
  document.querySelector("#proofRouteTriage").innerHTML = renderProofRouteTriage(problem);
  document.querySelector("#decisiveTheoremSpec").innerHTML = renderDecisiveTheoremSpec(problem);
  document.querySelector("#decisiveTheoremSubgoals").innerHTML = renderDecisiveTheoremSubgoals(problem);
  document.querySelector("#decisiveTheoremAttackTickets").innerHTML = renderDecisiveTheoremAttackTickets(problem);
  document.querySelector("#proofBreakthroughAgenda").innerHTML = renderProofBreakthroughAgenda(problem);
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
  document.querySelector("#proofExecutionProtocol").innerHTML = renderProofExecutionProtocol(problem);
  document.querySelector("#proofFrontierProbe").innerHTML = renderProofFrontierProbe(problem);
  document.querySelector("#knownBarrierAudit").innerHTML = renderKnownBarrierAudit(problem);
  document.querySelector("#formalReplayPackage").innerHTML = renderFormalReplayPackage(problem);
  document.querySelector("#proofReviewDocket").innerHTML = renderProofReviewDocket(problem);
  document.querySelector("#proofReductionContract").innerHTML = renderProofReductionContract(problem);
  document.querySelector("#proofCandidateIntake").innerHTML = renderProofCandidateIntake(problem);
  document.querySelector("#proofAttemptExecutionLog").innerHTML = renderProofAttemptExecutionLog(problem);
  document.querySelector("#proofObligationDag").innerHTML = renderProofObligationDag(problem);
  document.querySelector("#formalSkeletonAudit").innerHTML = renderFormalSkeletonAudit(problem);
  document.querySelector("#formalContract").innerHTML = renderFormalContract(problem);
  document.querySelector("#milestoneQueue").innerHTML = renderMilestoneQueue(problem);
  document.querySelector("#decisiveLemmaLab").innerHTML = renderDecisiveLemmaLab(problem);
  document.querySelector("#proofGates").innerHTML = list(problem.proof_gates || []);
  document.querySelector("#candidateStrategy").innerHTML = list(problem.candidate_strategy || []);
  document.querySelector("#blockedClaims").innerHTML = (payload.claim_policy.blocked_claims || [])
    .map((claim) => `<span>${escapeHtml(claim)}</span>`)
    .join("");
  if (window.PrimeProjectI18n) window.PrimeProjectI18n.apply();
}

async function main() {
  const response = await fetch("../data/open_problem_workbench.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Failed to load workbench data: ${response.status}`);
  const payload = await response.json();
  const problem = payload.problems.find((item) => item.id === problemId);
  if (!problem) throw new Error(`Unknown problem: ${problemId}`);
  let proofOrCounterexampleTicket = null;
  let ticket17Attempt = null;
  let ticket18Attempt = null;
  let ticket19Attempt = null;
  let ticket20Attempt = null;
  let ticket21Attempt = null;
  let ticket22Attempt = null;
  let ticket23Attempt = null;
  let ticket24Attempt = null;
  let ticket25Attempt = null;
  try {
    const labResponse = await fetch("../data/open-problem/proof-or-counterexample-lab.json", { cache: "no-store" });
    if (labResponse.ok) {
      const labPayload = await labResponse.json();
      proofOrCounterexampleTicket = (labPayload.problems || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    proofOrCounterexampleTicket = null;
  }
  try {
    const ticket17Response = await fetch("../data/open-problem/ticket17-breakthrough-attempts.json", { cache: "no-store" });
    if (ticket17Response.ok) {
      const ticket17Payload = await ticket17Response.json();
      ticket17Attempt = (ticket17Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket17Attempt = null;
  }
  try {
    const ticket18Response = await fetch("../data/open-problem/ticket18-reduction-lab.json", { cache: "no-store" });
    if (ticket18Response.ok) {
      const ticket18Payload = await ticket18Response.json();
      ticket18Attempt = (ticket18Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket18Attempt = null;
  }
  try {
    const ticket19Response = await fetch("../data/open-problem/ticket19-proof-pressure-lab.json", { cache: "no-store" });
    if (ticket19Response.ok) {
      const ticket19Payload = await ticket19Response.json();
      ticket19Attempt = (ticket19Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket19Attempt = null;
  }
  try {
    const ticket20Response = await fetch("../data/open-problem/ticket20-valuation-prefix-lab.json", { cache: "no-store" });
    if (ticket20Response.ok) {
      const ticket20Payload = await ticket20Response.json();
      ticket20Attempt = (ticket20Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket20Attempt = null;
  }
  try {
    const ticket21Response = await fetch("../data/open-problem/ticket21-two-adic-branch-lab.json", { cache: "no-store" });
    if (ticket21Response.ok) {
      const ticket21Payload = await ticket21Response.json();
      ticket21Attempt = (ticket21Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket21Attempt = null;
  }
  try {
    const ticket22Response = await fetch("../data/open-problem/ticket22-negation-pressure-lab.json", { cache: "no-store" });
    if (ticket22Response.ok) {
      const ticket22Payload = await ticket22Response.json();
      ticket22Attempt = (ticket22Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket22Attempt = null;
  }
  try {
    const ticket23Response = await fetch("../data/open-problem/ticket23-cegis-rank-lab.json", { cache: "no-store" });
    if (ticket23Response.ok) {
      const ticket23Payload = await ticket23Response.json();
      ticket23Attempt = (ticket23Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket23Attempt = null;
  }
  try {
    const ticket24Response = await fetch("../data/open-problem/ticket24-bridge-weight-lab.json", { cache: "no-store" });
    if (ticket24Response.ok) {
      const ticket24Payload = await ticket24Response.json();
      ticket24Attempt = (ticket24Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket24Attempt = null;
  }
  try {
    const ticket25Response = await fetch("../data/open-problem/ticket25-formal-lemma-kernel.json", { cache: "no-store" });
    if (ticket25Response.ok) {
      const ticket25Payload = await ticket25Response.json();
      ticket25Attempt = (ticket25Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket25Attempt = null;
  }
  render(payload, problem, proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt);
}

main().catch((error) => {
  document.querySelector("#finiteEvidence").innerHTML = `<div class="proof-note is-error">${escapeHtml(error.message)}</div>`;
});
