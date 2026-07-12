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

function renderTicket26MicroLemma(attempt) {
  if (!attempt) return "";
  const certificate = attempt.micro_lemma_certificate || {};
  const summaryRows = Object.entries(certificate)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 12);
  const certificateRows = Array.isArray(certificate.false_cycle_certificates)
    ? table(
        ["#", "Status", "Reason", "Denominator", "Candidate"],
        certificate.false_cycle_certificates.slice(0, 6).map((row, index) => [
          index + 1,
          row.independent_status,
          row.reason,
          row.denominator_2s_minus_3k,
          row.candidate_value,
        ]),
      )
    : Array.isArray(certificate.separation_rows)
      ? table(
          ["limit", "exact gap 2 after deletion", "bounded retention", "separates"],
          certificate.separation_rows.map((row) => [
            row.limit,
            row.exact_gap_2_retention_after_deletion,
            row.bounded_without_gap_2_retention_ratio,
            row.separates_bounded_gap_from_exact_gap_2,
          ]),
        )
      : "";
  return `
    <div class="poc-ticket17 poc-ticket26">
      <h3>Ticket 26 micro-lemma closure</h3>
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
          <span>Target</span>
          <strong>${escapeHtml(statusText(attempt.target_status || "open_not_proven"))}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${summaryRows.length ? table(["Micro-lemma certificate", "Value"], summaryRows) : ""}
      ${certificateRows}
      <div class="poc-bridge">
        <section>
          <h3>Closed micro-lemma</h3>
          <p>${escapeHtml(attempt.formal_micro_lemma_statement || "")}</p>
        </section>
        <section>
          <h3>Remaining obligation</h3>
          <p>${escapeHtml(attempt.remaining_obligation || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket27RankFrontier(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 12);
  const frontierRows = Array.isArray(bounded.rank_frontier_rows)
    ? table(
        ["bits", "unreachable", "max rank", "lift violations", "violation rate"],
        bounded.rank_frontier_rows.map((row) => [
          row.modulus_bits,
          row.unreachable_to_known_1_cycle_count,
          row.max_quotient_distance_to_1_cycle,
          row.sampled_lift_rank_violations,
          row.sampled_lift_rank_violation_rate,
        ]),
      )
    : "";
  const exampleRows = Array.isArray(bounded.first_lift_rank_counterexamples)
    ? table(
        ["residue", "lift", "n", "rank", "next rank"],
        bounded.first_lift_rank_counterexamples.map((row) => [
          row.residue,
          row.lift_index,
          row.integer_value,
          row.source_quotient_rank,
          row.target_quotient_rank,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket27">
      <h3>Ticket 27 rank-frontier lab</h3>
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
      ${summaryRows.length ? table(["Rank frontier result", "Value"], summaryRows) : ""}
      ${frontierRows}
      ${exampleRows}
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

function renderTicket28Trichotomy(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 12);
  const routeRows = Array.isArray(bounded.trichotomy_routes)
    ? table(
        ["Mode", "Status", "Open blocker"],
        bounded.trichotomy_routes.map((row) => [
          statusText(row.mode),
          statusText(row.bounded_status),
          row.open_blocker,
        ]),
      )
    : "";
  const cylinderRows = Array.isArray(bounded.cylinder_descent?.cylinder_descent_rows)
    ? table(
        ["bits", "all-lift descent", "needs split", "closed rate", "max prefix"],
        bounded.cylinder_descent.cylinder_descent_rows.map((row) => [
          row.modulus_bits,
          row.all_lift_descent_count,
          row.needs_split_count,
          row.closed_nontrivial_cylinder_rate,
          row.max_exact_prefix_length,
        ]),
      )
    : "";
  const stopping = bounded.stopping_scan;
  const stoppingRows = stopping
    ? table(
        ["Stopping scan", "Value"],
        [
          ["odd start limit", stopping.odd_start_limit],
          ["no counterexample <=", stopping.no_stopping_counterexample_leq_limit],
          ["max steps", stopping.max_stopping_steps?.steps],
          ["max steps n", stopping.max_stopping_steps?.n],
          ["max valuation-debt n", stopping.max_peak_valuation_debt?.n],
        ],
      )
    : "";
  const mertens = bounded.mertens_stress;
  const mertensRows = mertens
    ? table(
        ["Mertens stress", "Value"],
        [
          ["limit", mertens.limit],
          ["M(limit)", mertens.mertens_at_limit],
          ["max |M|/sqrt(n), n>=10k", mertens.max_abs_mertens_over_sqrt_n_from_10000?.value],
          ["argmax n", mertens.max_abs_mertens_over_sqrt_n_from_10000?.n],
        ],
      )
    : "";
  const goldbachScan = bounded.finite_witness_scan;
  const goldbachRows = goldbachScan
    ? table(
        ["Goldbach finite scan", "Value"],
        [
          ["even limit", goldbachScan.even_limit],
          ["checked even count", goldbachScan.checked_even_count],
          ["counterexample found", goldbachScan.counterexample_found ?? "none"],
          ["hardest first witness n", goldbachScan.hardest_first_witness_row?.even_n],
          ["first witness", (goldbachScan.hardest_first_witness_row?.first_witness || []).join(" + ")],
        ],
      )
    : "";
  const twinScan = bounded.finite_exact_gap_scan;
  const twinRows = twinScan
    ? table(
        ["Twin-prime exact-gap scan", "Value"],
        [
          ["prime limit", twinScan.prime_limit],
          ["twin pair count", twinScan.twin_pair_count],
          ["last pair", (twinScan.last_twin_pair_leq_limit || []).join(", ")],
          ["max gap between twin starts", twinScan.max_gap_between_twin_pair_starts?.gap],
        ],
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket28">
      <h3>Ticket 28 trichotomy descent lab</h3>
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
      ${summaryRows.length ? table(["Trichotomy result", "Value"], summaryRows) : ""}
      ${routeRows}
      ${cylinderRows}
      ${stoppingRows}
      ${mertensRows}
      ${goldbachRows}
      ${twinRows}
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

function renderTicket29AdaptiveFrontier(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 12);
  const adaptive = bounded.adaptive_cylinder_split;
  const adaptiveSummary = adaptive
    ? table(
        ["Adaptive split metric", "Value"],
        [
          ["base bits", adaptive.base_modulus_bits],
          ["max bits", adaptive.max_modulus_bits],
          ["processed states", adaptive.processed_state_count],
          ["full max odd cylinders", adaptive.full_odd_cylinders_at_max_bits],
          ["open frontier", adaptive.open_frontier_count_at_max_bits],
          ["open frontier fraction", adaptive.open_frontier_fraction_of_full_max_space],
          ["naive termination verdict", adaptive.naive_termination_verdict],
        ],
      )
    : "";
  const adaptiveRows = Array.isArray(adaptive?.adaptive_depth_rows)
    ? table(
        ["bits", "processed", "closed", "needs split", "frontier", "cumulative"],
        adaptive.adaptive_depth_rows.map((row) => [
          row.modulus_bits,
          row.processed_at_depth,
          row.closed_at_depth,
          row.needs_split_at_depth,
          row.open_frontier_at_depth,
          row.cumulative_processed,
        ]),
      )
    : "";
  const mertens = bounded.mertens_stress;
  const mertensRows = mertens
    ? table(
        ["Mertens stress", "Value"],
        [
          ["limit", mertens.limit],
          ["M(limit)", mertens.mertens_at_limit],
          ["max |M|/sqrt(n), n>=1M", mertens.max_abs_mertens_over_sqrt_n_from_1000000?.value],
          ["argmax n", mertens.max_abs_mertens_over_sqrt_n_from_1000000?.n],
        ],
      )
    : "";
  const goldbachScan = bounded.finite_witness_scan;
  const goldbachRows = goldbachScan
    ? table(
        ["Goldbach finite scan", "Value"],
        [
          ["even limit", goldbachScan.even_limit],
          ["checked even count", goldbachScan.checked_even_count],
          ["counterexample found", goldbachScan.counterexample_found ?? "none"],
          ["hardest first witness n", goldbachScan.hardest_first_witness_row?.even_n],
          ["first witness", (goldbachScan.hardest_first_witness_row?.first_witness || []).join(" + ")],
        ],
      )
    : "";
  const twinScan = bounded.finite_exact_gap_scan;
  const twinRows = twinScan
    ? table(
        ["Twin-prime exact-gap scan", "Value"],
        [
          ["prime limit", twinScan.prime_limit],
          ["twin pair count", twinScan.twin_pair_count],
          ["last pair", (twinScan.last_twin_pair_leq_limit || []).join(", ")],
          ["max gap between twin starts", twinScan.max_gap_between_twin_pair_starts?.gap],
        ],
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket29">
      <h3>Ticket 29 adaptive frontier lab</h3>
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
      ${summaryRows.length ? table(["Adaptive frontier result", "Value"], summaryRows) : ""}
      ${adaptiveSummary}
      ${adaptiveRows}
      ${mertensRows}
      ${goldbachRows}
      ${twinRows}
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

function renderTicket30PotentialSynthesis(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const summaryRows = Object.entries(bounded)
    .filter(([, value]) => typeof value !== "object" || value === null)
    .slice(0, 12);
  const cegis = bounded.potential_cegis;
  const potentialRows = cegis
    ? table(
        ["Potential CEGIS metric", "Value"],
        [
          ["candidate max bits", cegis.full_candidate_max_bits],
          ["grid search max bits", cegis.grid_search_max_bits],
          ["candidate parent edges", cegis.full_candidate_parent_edges],
          ["grid parent edges", cegis.grid_parent_edges],
          ["valid grid weights", cegis.valid_grid_weight_count],
          ["linear potential status", cegis.linear_potential_status],
        ],
      )
    : "";
  const candidateRows = Array.isArray(cegis?.candidate_results)
    ? table(
        ["candidate", "weights", "violations", "rate", "valid"],
        cegis.candidate_results.map((row) => [
          row.name,
          (row.weights || []).join(", "),
          row.violation_count,
          row.violation_rate,
          row.valid_on_tested_edges,
        ]),
      )
    : "";
  const gridRows = Array.isArray(cegis?.best_grid_results)
    ? table(
        ["rank", "weights", "violations", "rate", "worst margin"],
        cegis.best_grid_results.slice(0, 6).map((row, index) => [
          index + 1,
          (row.weights || []).join(", "),
          row.violation_count,
          row.violation_rate,
          row.worst_margin,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket30">
      <h3>Ticket 30 potential synthesis lab</h3>
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
      ${summaryRows.length ? table(["Potential synthesis result", "Value"], summaryRows) : ""}
      ${potentialRows}
      ${candidateRows}
      ${gridRows}
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

function renderTicket31FeatureStutter(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const cegis = bounded.feature_stutter_cegis || {};
  const impossible = cegis.strict_descent_impossibility || {};
  const summaryRows = Object.keys(cegis).length
    ? [
        ["base bits", cegis.base_modulus_bits],
        ["max bits", cegis.max_modulus_bits],
        ["parent edges", cegis.parent_edge_count],
        ["feature-only status", cegis.feature_only_obstruction_status],
        ["base stutter edges", impossible.base_four_indistinguishable_edges],
        ["prefix+residue stutter edges", impossible.prefix_and_low_residue_indistinguishable_edges],
        ["next candidate", cegis.next_candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["frontier status", bounded.frontier_status],
        ["ticket31 transfer", bounded.ticket31_transfer],
      ];
  const familyRows = Array.isArray(cegis.feature_families)
    ? table(
        ["feature family", "open child edges", "indistinguishable", "rate"],
        cegis.feature_families.map((row) => [
          row.family,
          row.open_child_edges,
          row.indistinguishable_open_edges,
          row.indistinguishable_rate,
        ]),
      )
    : "";
  const chainRows = Array.isArray(cegis.low_child_stutter_chains)
    ? table(
        ["residue", "start bits", "same-signature steps", "first change", "terminal"],
        cegis.low_child_stutter_chains.map((row) => [
          row.residue,
          row.start_bits,
          row.same_signature_low_child_steps,
          row.first_signature_change ? `bits ${row.first_signature_change.bits}` : "none",
          row.terminal_non_open_certificate
            ? `${row.terminal_non_open_certificate.status} at bits ${row.terminal_non_open_certificate.bits}`
            : "open or not reached",
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket31">
      <h3>Ticket 31 feature-stutter obstruction</h3>
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
      ${summaryRows.length ? table(["Feature-stutter result", "Value"], summaryRows) : ""}
      ${familyRows}
      ${chainRows}
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

function renderTicket32StatefulMeasure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.stateful_measure_audit || {};
  const budget = audit.stateful_budget_certificate || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["base bits", audit.base_modulus_bits],
        ["adaptive max bits", audit.adaptive_max_modulus_bits],
        ["max chain bits", audit.max_chain_bits],
        ["parent edges", audit.parent_edge_count],
        ["open child edges", audit.open_child_edges],
        ["stutter edges", audit.stutter_edge_count],
        ["stutter rate", audit.stutter_edge_rate],
        ["max same-signature steps", audit.max_same_signature_steps],
        ["budget status", budget.status],
        ["unresolved stutter edges", budget.unresolved_stutter_edges],
        ["next candidate", audit.next_candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["frontier status", bounded.frontier_status],
        ["ticket32 transfer", bounded.ticket32_transfer],
      ];
  const outcomeRows = audit.chain_outcome_counts
    ? table(["outcome", "count"], Object.entries(audit.chain_outcome_counts))
    : "";
  const distributionRows = audit.same_signature_step_distribution
    ? table(
        ["same-signature steps", "count"],
        Object.entries(audit.same_signature_step_distribution).slice(-8),
      )
    : "";
  const examples = Array.isArray(audit.max_stutter_examples)
    ? table(
        ["residue", "bits", "steps", "outcome", "exit"],
        audit.max_stutter_examples.slice(0, 6).map((row) => [
          row.parent_residue,
          row.parent_bits,
          row.same_signature_steps,
          row.outcome,
          `${row.exit_status} at bits ${row.exit_bits}`,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket32">
      <h3>Ticket 32 stateful measure lab</h3>
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
      ${summaryRows.length ? table(["Stateful measure result", "Value"], summaryRows) : ""}
      ${outcomeRows}
      ${distributionRows}
      ${examples}
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

function renderTicket33GlobalMeasure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.global_measure_audit || {};
  const measure = audit.measure_certificate || {};
  const high = audit.high_branch_obstruction || {};
  const fit = audit.tail_log2_mass_fit || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["base bits", audit.base_modulus_bits],
        ["max bits", audit.max_modulus_bits],
        ["initial open mass", audit.initial_open_frontier_mass],
        ["final open count", audit.final_open_frontier_count],
        ["final open mass", audit.final_open_frontier_mass],
        ["monotone mass decrease", audit.monotone_open_mass_decrease],
        ["max mass ratio", audit.max_mass_ratio_to_next],
        ["tail per-bit factor", fit.per_bit_factor],
        ["high open child edges", high.high_open_child_edges],
        ["high-only open child edges", high.high_only_open_child_edges],
        ["compactness status", measure.compactness_status],
        ["next candidate", audit.next_candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["frontier status", bounded.frontier_status],
        ["ticket33 transfer", bounded.ticket33_transfer],
      ];
  const transitionRows = audit.transition_totals
    ? table(["transition", "count"], Object.entries(audit.transition_totals))
    : "";
  const frontierRows = Array.isArray(audit.frontier_rows)
    ? table(
        ["bits", "open count", "open mass", "next mass ratio", "high open"],
        audit.frontier_rows.slice(-8).map((row) => [
          row.bits,
          row.open_frontier_count,
          row.open_frontier_mass,
          row.mass_ratio_to_next ?? "final",
          row.high_open_child_count ?? "final",
        ]),
      )
    : "";
  const highExamples = Array.isArray(high.high_only_examples)
    ? table(
        ["parent", "bits", "high child", "low status", "high status"],
        high.high_only_examples.slice(0, 6).map((row) => [
          row.parent_residue,
          row.parent_bits,
          row.high_child_residue,
          row.low_status,
          row.high_status,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket33">
      <h3>Ticket 33 global measure lab</h3>
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
      ${summaryRows.length ? table(["Global measure result", "Value"], summaryRows) : ""}
      ${frontierRows}
      ${transitionRows}
      ${highExamples}
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

function renderTicket34HighBranchAutomaton(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.high_branch_automaton_audit || {};
  const certificate = audit.automaton_certificate || {};
  const bestRadius = audit.best_finite_quotient_radius || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["base bits", audit.base_modulus_bits],
        ["max bits", audit.max_modulus_bits],
        ["transition parents", audit.transition_parent_count],
        ["high-open parents", audit.high_open_child_parent_count],
        ["high-only parents", audit.high_only_parent_count],
        ["pointwise contraction blocked", audit.pointwise_contraction_blocked],
        ["max mass ratio", audit.max_mass_ratio_to_next],
        ["best finite quotient radius", bestRadius.estimated_radius],
        ["automaton status", certificate.status],
        ["mass-limit status", certificate.mass_limit_status],
        ["next candidate", audit.next_candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["frontier status", bounded.frontier_status],
        ["ticket34 transfer", bounded.ticket34_transfer],
      ];
  const transitionRows = audit.transition_totals
    ? table(["transition", "count"], Object.entries(audit.transition_totals))
    : "";
  const levelRows = Array.isArray(audit.level_rows)
    ? table(
        ["bits", "parents", "next count", "mass ratio", "both-open rate", "high-only rate"],
        audit.level_rows.slice(-8).map((row) => [
          row.bits,
          row.parent_frontier_count,
          row.next_frontier_count,
          row.mass_ratio_to_next,
          row.both_open_parent_rate,
          row.high_only_parent_rate,
        ]),
      )
    : "";
  const familyRows = Array.isArray(audit.automaton_families)
    ? table(
        ["family", "status", "states", "ambiguous", "noncontracting", "radius"],
        audit.automaton_families.map((row) => [
          row.family,
          row.status,
          row.state_count,
          row.ambiguous_state_count,
          row.pointwise_noncontracting_state_count,
          row.aggregate_spectral_pressure?.estimated_radius ?? row.aggregate_spectral_pressure?.status,
        ]),
      )
    : "";
  const firstFamily = Array.isArray(audit.automaton_families) ? audit.automaton_families[0] || {} : {};
  const collisionRows = Array.isArray(firstFamily.collision_examples)
    ? table(
        ["state", "labels"],
        firstFamily.collision_examples.slice(0, 4).map((row) => [row.state, (row.labels || []).join(", ")]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket34">
      <h3>Ticket 34 high-branch automaton lab</h3>
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
      ${summaryRows.length ? table(["High-branch automaton result", "Value"], summaryRows) : ""}
      ${levelRows}
      ${transitionRows}
      ${familyRows}
      ${collisionRows}
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

function renderTicket35LimsupMassRefinement(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.limsup_mass_refinement_audit || {};
  const mass = audit.mass_envelope_audit || {};
  const refinement = audit.state_refinement_audit || {};
  const nullSet = audit.null_set_gap || {};
  const fit = mass.tail_log2_mass_fit || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["mass bits", `${mass.base_modulus_bits}..${mass.max_modulus_bits}`],
        ["final open count", mass.final_open_frontier_count],
        ["final open mass", mass.final_open_mass],
        ["max mass ratio", mass.max_mass_ratio_to_next],
        ["tail max ratio", mass.tail_window_max_ratio],
        ["tail candidate epsilon", mass.tail_window_candidate_epsilon],
        ["tail per-bit factor", fit.per_bit_factor],
        ["null-set gap", nullSet.status],
        ["refinement status", refinement.refinement_status],
        ["next candidate", audit.next_candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["frontier status", bounded.frontier_status],
        ["ticket35 transfer", bounded.ticket35_transfer],
      ];
  const levelRows = Array.isArray(mass.level_rows)
    ? table(
        ["bits", "parents", "next count", "mass ratio", "both-open rate", "high-only rate"],
        mass.level_rows.slice(-8).map((row) => [
          row.bits,
          row.parent_frontier_count,
          row.next_frontier_count,
          row.mass_ratio_to_next,
          row.both_open_parent_rate,
          row.high_only_parent_rate,
        ]),
      )
    : "";
  const refinementRows = Array.isArray(refinement.refinement_rows)
    ? table(
        ["family", "status", "states", "ambiguous", "noncontracting", "finite"],
        refinement.refinement_rows.map((row) => [
          row.family,
          row.status,
          row.state_count,
          row.ambiguous_state_count,
          row.pointwise_noncontracting_state_count,
          row.finite_uniform_candidate,
        ]),
      )
    : "";
  const routeDecision = audit.route_decision || {};
  return `
    <div class="poc-ticket17 poc-ticket35">
      <h3>Ticket 35 limsup mass refinement lab</h3>
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
      ${summaryRows.length ? table(["Limsup mass refinement result", "Value"], summaryRows) : ""}
      ${levelRows}
      ${refinementRows}
      <div class="poc-bridge">
        <section>
          <h3>Discard</h3>
          ${list(routeDecision.discard || [])}
        </section>
        <section>
          <h3>Retain</h3>
          ${list(routeDecision.retain || [])}
        </section>
      </div>
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
      <p class="proof-boundary">${escapeHtml(nullSet.reason || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket36NullFrontierArithmetic(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.natural_null_frontier_audit || {};
  const routeDecision = bounded.route_decision || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["sample limit", audit.sample_limit],
        ["tested odd integers", audit.tested_odd_integer_count],
        ["probe bits", `${audit.base_bits}..${audit.deep_resolve_bits}`],
        ["shallow unresolved", audit.shallow_unresolved_count],
        ["deep unresolved", audit.deep_unresolved_count],
        ["direct orbits terminated", audit.all_direct_orbits_terminated_in_sample],
        ["max exit bits", audit.max_exit_bits],
        ["max slack over bit length", audit.max_exit_slack_over_bit_length],
        ["max exit minus odd steps", audit.max_exit_minus_odd_steps],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["stress result", bounded.stress_result],
        ["discarded route", bounded.discarded_route],
        ["retained route", bounded.retained_route],
      ];
  const topExitRows = Array.isArray(audit.top_exit_examples)
    ? table(
        ["n", "bits", "exit", "slack", "odd steps", "total steps", "max orbit"],
        audit.top_exit_examples.slice(0, 10).map((row) => [
          row.n,
          row.bit_length,
          row.exit_bits,
          row.exit_slack_over_bit_length,
          row.direct_collatz?.odd_steps,
          row.direct_collatz?.total_steps,
          row.direct_collatz?.max_orbit_value,
        ]),
      )
    : "";
  const slackRows = Array.isArray(audit.candidate_bit_length_slack_tests)
    ? table(
        ["candidate bound", "violations"],
        audit.candidate_bit_length_slack_tests.map((row) => [row.candidate_bound, row.violations]),
      )
    : "";
  const proxyRows = Array.isArray(audit.candidate_stopping_proxy_tests)
    ? table(
        ["candidate bound", "violations"],
        audit.candidate_stopping_proxy_tests.map((row) => [row.candidate_bound, row.violations]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket36">
      <h3>Ticket 36 null-frontier arithmetic lab</h3>
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
      ${summaryRows.length ? table(["Natural frontier exit result", "Value"], summaryRows) : ""}
      ${topExitRows}
      ${slackRows}
      ${proxyRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket37PointwiseRankSynthesis(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const probe = bounded.pointwise_rank_probe || {};
  const routeDecision = bounded.route_decision || {};
  const piecewise = probe.candidate_piecewise_linear_rank || {};
  const summaryRows = Object.keys(probe).length
    ? [
        ["sample limit", probe.sample_limit],
        ["tested odd integers", probe.tested_odd_integer_count],
        ["probe bits", `${probe.base_bits}..${probe.max_probe_bits}`],
        ["resolved", probe.resolved_count],
        ["unresolved", probe.unresolved_count],
        ["max exit bits", probe.max_exit_bits],
        ["max exit ratio", probe.max_exit_ratio_to_bit_length],
        ["max slack", probe.max_exit_slack_over_bit_length],
        ["rank status", probe.rank_status],
        ["piecewise candidate", piecewise.candidate],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["bounded rank analogue", bounded.bounded_rank_analogue],
        ["discarded route", bounded.discarded_route],
        ["retained route", bounded.retained_route],
      ];
  const rankRows = Array.isArray(probe.linear_rank_tests)
    ? table(
        ["candidate bound", "violations", "status"],
        probe.linear_rank_tests.map((row) => [row.candidate_bound, row.violations, row.bounded_status]),
      )
    : "";
  const topRows = Array.isArray(probe.top_exit_examples)
    ? table(
        ["n", "bits", "exit", "ratio", "slack", "prefix", "margin"],
        probe.top_exit_examples.slice(0, 10).map((row) => [
          row.n,
          row.bit_length,
          row.exit_bits,
          row.exit_ratio_to_bit_length,
          row.exit_slack_over_bit_length,
          row.prefix_length,
          row.coefficient_log2_margin,
        ]),
      )
    : "";
  const thresholdRows = Array.isArray(probe.threshold_ratio_rows)
    ? table(
        ["min bits", "count", "max ratio", "top n", "top exit"],
        probe.threshold_ratio_rows.map((row) => [
          row.min_bit_length,
          row.tested_count,
          row.max_exit_ratio,
          row.top_example?.n,
          row.top_example?.exit_bits,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket37">
      <h3>Ticket 37 pointwise rank synthesis lab</h3>
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
      ${summaryRows.length ? table(["Pointwise rank synthesis result", "Value"], summaryRows) : ""}
      ${rankRows}
      ${topRows}
      ${thresholdRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(probe.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket38SymbolicFrontierExtension(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_frontier_extension_audit || {};
  const routeDecision = bounded.route_decision || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["frontier bits", `${audit.base_bits}..${audit.max_bits}`],
        ["open edge count", audit.open_edge_count],
        ["final frontier count", audit.final_frontier_count],
        ["max survival ratio", audit.max_survival_ratio],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded extension", bounded.discarded_extension],
        ["retained extension", bounded.retained_extension],
      ];
  const transitionRows = Array.isArray(audit.transition_rows)
    ? table(
        ["bits", "parents", "next", "survival", "both-open", "high-only", "closed"],
        audit.transition_rows.slice(-8).map((row) => [
          row.bits,
          row.parent_frontier_count,
          row.next_frontier_count,
          row.survival_ratio,
          row.transition_counts?.both_open || 0,
          row.transition_counts?.high_only_open || 0,
          row.transition_counts?.both_closed || 0,
        ]),
      )
    : "";
  const potentialRows = Array.isArray(audit.lambda_potential_rows)
    ? table(
        ["potential", "lambda", "nondecreasing edges", "rate", "status"],
        audit.lambda_potential_rows.map((row) => [
          row.name,
          row.lambda,
          row.nondecreasing_open_edges,
          row.nondecreasing_open_edge_rate,
          row.status,
        ]),
      )
    : "";
  const extensionRows = Array.isArray(audit.simple_extension_tests)
    ? table(
        ["candidate", "status", "detail"],
        audit.simple_extension_tests.map((row) => [
          row.candidate,
          row.status,
          row.reason || row.survivor_count || (Array.isArray(row.tested_lambdas) ? row.tested_lambdas.join(", ") : ""),
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket38">
      <h3>Ticket 38 symbolic frontier extension lab</h3>
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
      ${summaryRows.length ? table(["Symbolic extension result", "Value"], summaryRows) : ""}
      ${transitionRows}
      ${potentialRows}
      ${extensionRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket39PhaseStatePotential(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.phase_state_potential_audit || {};
  const routeDecision = bounded.route_decision || {};
  const deep = audit.deep_wrap_probe || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["frontier bits", `${audit.base_bits}..${audit.max_bits}`],
        ["open edge count", audit.open_edge_count],
        ["final frontier count", audit.final_frontier_count],
        ["deep wrap bits", `${deep.base_bits || ""}..${deep.max_bits || ""}`],
        ["deep wrap open edges", deep.open_edge_count],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded state", bounded.discarded_state],
        ["retained state", bounded.retained_state],
      ];
  const familyRows = Array.isArray(audit.family_rows)
    ? table(
        ["family", "status", "nodes", "state edges", "cycle", "core", "rank", "violations"],
        audit.family_rows.map((row) => [
          row.family,
          row.status,
          row.node_count,
          row.state_edge_count,
          row.topological_potential?.cycle_detected,
          row.topological_potential?.cyclic_core_node_count,
          row.topological_potential?.max_topological_rank,
          row.topological_potential?.rank_edge_violations,
        ]),
      )
    : "";
  const deepRows = Object.keys(deep).length
    ? table(
        ["deep probe", "value"],
        [
          ["family", deep.family],
          ["status", deep.status],
          ["open edges", deep.open_edge_count],
          ["final frontier", deep.final_frontier_count],
          ["nodes", deep.node_count],
          ["state edges", deep.state_edge_count],
          ["cycle detected", deep.topological_potential?.cycle_detected],
          ["max rank", deep.topological_potential?.max_topological_rank],
          ["rank violations", deep.topological_potential?.rank_edge_violations],
        ],
      )
    : "";
  const testRows = Array.isArray(audit.phase_state_tests)
    ? table(
        ["candidate", "family", "status", "detail"],
        audit.phase_state_tests.map((row) => [
          row.candidate,
          row.family || "",
          row.status,
          row.reason || row.cyclic_core_node_count || row.max_topological_rank || "",
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket39">
      <h3>Ticket 39 phase/state potential synthesis lab</h3>
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
      ${summaryRows.length ? table(["Phase/state potential result", "Value"], summaryRows) : ""}
      ${familyRows}
      ${deepRows}
      ${testRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket40TransitionClosure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.transition_closure_audit || {};
  const primary = audit.primary_window || {};
  const extension = audit.extension_probe || {};
  const routeDecision = bounded.route_decision || {};
  const deterministic = primary.deterministic_transition_closure || {};
  const nondeterministic = extension.nondeterministic_transition_relation || {};
  const topo = nondeterministic.topological_potential || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["primary bits", `${primary.base_bits || ""}..${primary.max_bits || ""}`],
        ["primary ambiguous child states", primary.ambiguous_child_signature_state_count],
        ["extension bits", `${extension.base_bits || ""}..${extension.max_bits || ""}`],
        ["extension ambiguous child states", extension.ambiguous_child_signature_state_count],
        ["extension frontier", extension.final_frontier_count],
        ["max sampled rank", topo.max_topological_rank],
        ["rank violations", topo.rank_edge_violations],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded deterministic shortcut", bounded.discarded_deterministic_shortcut],
        ["retained nondeterministic target", bounded.retained_nondeterministic_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const closureRows = Array.isArray(audit.closure_tests)
    ? table(
        ["closure candidate", "status", "evidence"],
        audit.closure_tests.map((row) => [row.candidate, row.status, row.evidence]),
      )
    : "";
  const primaryRows = Object.keys(primary).length
    ? table(
        ["primary closure field", "value"],
        [
          ["family", primary.family],
          ["parent instances", primary.parent_instance_count],
          ["states", primary.state_count],
          ["state edges", primary.state_edge_count],
          ["label collisions", primary.ambiguous_label_state_count],
          ["child signature collisions", primary.ambiguous_child_signature_state_count],
          ["max signatures/state", primary.max_child_signature_count_for_one_state],
          ["deterministic status", deterministic.status],
        ],
      )
    : "";
  const extensionRows = Object.keys(extension).length
    ? table(
        ["extension closure field", "value"],
        [
          ["family", extension.family],
          ["parent instances", extension.parent_instance_count],
          ["states", extension.state_count],
          ["state edges", extension.state_edge_count],
          ["label collisions", extension.ambiguous_label_state_count],
          ["child signature collisions", extension.ambiguous_child_signature_state_count],
          ["cycle detected", topo.cycle_detected],
          ["max rank", topo.max_topological_rank],
          ["rank violations", topo.rank_edge_violations],
        ],
      )
    : "";
  const examples = Array.isArray(deterministic.ambiguous_examples)
    ? deterministic.ambiguous_examples.slice(0, 3).map((example) => [
        example.state,
        example.occurrences,
        example.signature_count,
        (example.observations || [])
          .slice(0, 2)
          .map((observation) => `${observation.bits}:${observation.parent_residue}:${observation.label}`)
          .join(" / "),
      ])
    : [];
  const exampleRows = examples.length
    ? table(["ambiguous state", "occurrences", "signatures", "sample observations"], examples)
    : "";
  return `
    <div class="poc-ticket17 poc-ticket40">
      <h3>Ticket 40 transition closure lab</h3>
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
      ${summaryRows.length ? table(["Transition closure result", "Value"], summaryRows) : ""}
      ${closureRows}
      ${primaryRows}
      ${extensionRows}
      ${exampleRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket41RankEscapeNormalization(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.rank_escape_normalization_audit || {};
  const routeDecision = bounded.route_decision || {};
  const snapshots = Array.isArray(audit.snapshots) ? audit.snapshots : [];
  const comparisons = Array.isArray(audit.extension_comparisons) ? audit.extension_comparisons : [];
  const growth = audit.coordinate_growth_after_primary || {};
  const summaryRows = Object.keys(audit).length
    ? [
        ["family", audit.family],
        ["snapshots", snapshots.map((row) => `${row.base_bits}..${row.max_bits}`).join(", ")],
        ["24->25 new edges", comparisons[0]?.new_state_edge_count],
        ["24->25 reopened sinks", comparisons[0]?.previous_sink_reopened_count],
        ["25->26 new edges", comparisons[1]?.new_state_edge_count],
        ["25->26 reopened sinks", comparisons[1]?.previous_sink_reopened_count],
        ["coordinate delta", growth.distinct_coordinate_delta],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const snapshotRows = snapshots.length
    ? table(
        ["bits", "nodes", "edges", "sinks", "coords", "max prefix", "max rank", "violations"],
        snapshots.map((row) => [
          `${row.base_bits}..${row.max_bits}`,
          row.node_count,
          row.state_edge_count,
          row.sink_state_count,
          row.coordinate_summary?.distinct_coordinate_count,
          row.coordinate_summary?.max_prefix_length,
          row.topological_potential?.max_topological_rank,
          row.topological_potential?.rank_edge_violations,
        ]),
      )
    : "";
  const comparisonRows = comparisons.length
    ? table(
        ["extension", "status", "new nodes", "new edges", "known-parent new edges", "reopened sinks", "new coords", "rank +"],
        comparisons.map((row) => [
          `${row.from_max_bits}->${row.to_max_bits}`,
          row.closure_status,
          row.new_node_count,
          row.new_state_edge_count,
          row.known_parent_new_edge_count,
          row.previous_sink_reopened_count,
          row.new_coordinate_count,
          row.rank_horizon_increase,
        ]),
      )
    : "";
  const fixedTests = Array.isArray(audit.fixed_relation_tests)
    ? table(
        ["fixed relation test", "status", "evidence"],
        audit.fixed_relation_tests.map((row) => [row.candidate, row.status, row.evidence]),
      )
    : "";
  const reopenedExamples = comparisons[0]?.reopened_sink_examples || [];
  const reopenedRows = reopenedExamples.length
    ? table(
        ["reopened sink state", "new outgoing", "coordinate"],
        reopenedExamples.slice(0, 4).map((row) => [
          row.state,
          row.new_outgoing_edge_count,
          JSON.stringify(row.coordinates || {}),
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket41">
      <h3>Ticket 41 rank escape normalization lab</h3>
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
      ${summaryRows.length ? table(["Rank escape result", "Value"], summaryRows) : ""}
      ${snapshotRows}
      ${comparisonRows}
      ${fixedTests}
      ${reopenedRows}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket42ParametricTemplate(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.parametric_transition_template_audit || {};
  const routeDecision = audit.route_decision || {};
  const familyRows = Array.isArray(audit.family_rows) ? audit.family_rows : [];
  const sharp = familyRows[familyRows.length - 1] || {};
  const transferRows = Object.keys(audit).length
    ? [
        ["base bits", audit.base_bits],
        ["max bits", audit.max_bits],
        ["cycle search", audit.cycle_search_status],
        ["sharp family", sharp.family],
        ["sharp status", audit.sharp_family_status],
        ["sharp ambiguous edges", sharp.ambiguous_template_edge_count],
        ["total ambiguous edges", audit.total_ambiguous_template_edge_count],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const familyTable = familyRows.length
    ? table(
        ["family", "nodes", "edges", "raw open", "nondec rate", "cycles", "ambiguous", "status"],
        familyRows.map((row) => [
          row.family,
          row.template_node_count,
          row.template_edge_count,
          row.raw_open_edge_count,
          row.raw_nondecreasing_debt_rate,
          row.cyclic_component_count,
          row.ambiguous_template_edge_count,
          row.strict_template_rank_status,
        ]),
      )
    : "";
  const schema = audit.parametric_schema || {};
  const sharpExamples = Array.isArray(sharp.ambiguous_template_edge_examples)
    ? sharp.ambiguous_template_edge_examples
    : [];
  const ambiguityTable = sharpExamples.length
    ? table(
        ["parent template", "child template", "count", "min debt", "max debt", "delta signatures"],
        sharpExamples.slice(0, 4).map((row) => [
          row.parent_template,
          row.child_template,
          row.count,
          row.min_delta_debt,
          row.max_delta_debt,
          JSON.stringify(row.delta_signatures || {}),
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket42">
      <h3>Ticket 42 parametric transition template lab</h3>
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
      ${table(["Template result", "Value"], transferRows)}
      ${familyTable}
      ${ambiguityTable}
      ${
        schema.state_variables || schema.template_update
          ? `<div class="poc-bridge">
              <section>
                <h3>State variables</h3>
                ${list(schema.state_variables || [])}
              </section>
              <section>
                <h3>Template update</h3>
                ${list(schema.template_update || [])}
                <p>${escapeHtml(schema.missing_lift_theorem || "")}</p>
              </section>
            </div>`
          : ""
      }
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket43LiftConstraintMeasure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.lift_constraint_measure_audit || {};
  const snapshots = Array.isArray(audit.snapshots) ? audit.snapshots : [];
  const comparisons = Array.isArray(audit.extension_comparisons) ? audit.extension_comparisons : [];
  const routeDecision = audit.route_decision || {};
  const finalSnapshot = snapshots[snapshots.length - 1] || {};
  const finalMeasure = finalSnapshot.sampled_rank_debt_measure || {};
  const latestComparison = comparisons[comparisons.length - 1] || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["base bits", audit.base_bits ?? finalSnapshot.base_bits],
        ["max bits", audit.max_bits ?? finalSnapshot.max_bits],
        ["family", audit.family],
        ["measure status", finalMeasure.status],
        ["measure scale", finalMeasure.scale],
        ["minimum margin", finalMeasure.min_margin],
        ["25->26 new template edges", latestComparison.new_template_edge_count],
        ["25->26 changed previous ranks", latestComparison.rank_changed_previous_node_count],
        ["closure status", latestComparison.closure_status],
        ["source ticket", bounded.source_ticket],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const snapshotTable = snapshots.length
    ? table(
        ["bits", "nodes", "edges", "raw open", "ambiguous", "sinks", "max rank", "scale", "min margin", "measure"],
        snapshots.map((row) => [
          row.max_bits,
          row.template_node_count,
          row.template_edge_count,
          row.raw_open_edge_count,
          row.ambiguous_template_edge_count,
          row.sink_template_count,
          (row.topological_template_rank || row.topological_rank)?.max_topological_rank,
          row.sampled_rank_debt_measure?.scale,
          row.sampled_rank_debt_measure?.min_margin,
          row.sampled_rank_debt_measure?.status,
        ]),
      )
    : "";
  const comparisonTable = comparisons.length
    ? table(
        [
          "extension",
          "new nodes",
          "new edges",
          "reopened sinks",
          "changed ranks",
          "old-measure unknown edges",
          "closure",
        ],
        comparisons.map((row) => [
          `${row.from_max_bits}->${row.to_max_bits}`,
          row.new_template_node_count,
          row.new_template_edge_count,
          row.previous_sink_reopened_count,
          row.rank_changed_previous_node_count,
          row.old_measure_unknown_rank_edges,
          row.closure_status,
        ]),
      )
    : "";
  const marginExamples = Array.isArray(finalMeasure.worst_margin_examples)
    ? finalMeasure.worst_margin_examples
    : [];
  const marginTable = marginExamples.length
    ? table(
        ["parent template", "child template", "rank gap", "max debt delta", "margin"],
        marginExamples.slice(0, 5).map((row) => [
          row.parent_template,
          row.child_template,
          row.rank_gap,
          row.max_delta_debt,
          row.margin_at_scale,
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket43">
      <h3>Ticket 43 lift constraint measure lab</h3>
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
      ${table(["Lift measure result", "Value"], resultRows)}
      ${snapshotTable}
      ${comparisonTable}
      ${marginTable}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(finalMeasure.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket44FeatureMeasureCounteredge(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.feature_measure_counteredge_audit || {};
  const trials = Array.isArray(audit.feature_trials) ? audit.feature_trials : [];
  const routeDecision = audit.route_decision || {};
  const rankBaseline = audit.rank_table_baseline || {};
  const rankMeasure = rankBaseline.sampled_rank_debt_measure || {};
  const extension = audit.horizon_extension_gate || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["max bits", audit.max_bits],
        ["template nodes", audit.template_node_count],
        ["template edges", audit.template_edge_count],
        ["raw open edges", audit.raw_open_edge_count],
        ["exactly refuted feature families", audit.exactly_refuted_feature_family_count],
        ["not certified or open families", audit.not_certified_or_open_feature_family_count],
        ["rank-table measure", rankMeasure.status],
        ["25->26 new template edges", extension.new_template_edge_count],
        ["25->26 changed previous ranks", extension.rank_changed_previous_node_count],
        ["closure status", extension.closure_status],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const trialTable = trials.length
    ? table(
        ["feature family", "status", "dim", "constraints", "positive debt", "zero refuters", "affine violations"],
        trials.map((row) => [
          row.feature_family,
          row.status,
          row.feature_dimension,
          row.unique_constraint_count,
          row.positive_debt_pressure_edge_count,
          row.zero_delta_refuter_count,
          row.sampled_affine_search?.violating_unique_constraints,
        ]),
      )
    : "";
  const counteredges = Array.isArray(audit.strongest_counteredges) ? audit.strongest_counteredges : [];
  const counteredgeTable = counteredges.length
    ? table(
        ["feature family", "status", "zero refuters", "reverse conflicts", "first refuter"],
        counteredges.slice(0, 5).map((row) => [
          row.feature_family,
          row.status,
          row.zero_delta_refuter_count,
          row.reverse_conflict_count,
          row.first_zero_delta_refuter?.parent_template
            ? `${row.first_zero_delta_refuter.parent_template} -> ${row.first_zero_delta_refuter.child_template}`
            : "n/a",
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket44">
      <h3>Ticket 44 feature-measure counteredge lab</h3>
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
      ${table(["Feature measure result", "Value"], resultRows)}
      ${trialTable}
      ${counteredgeTable}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket45SymbolicRankClause(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_rank_clause_audit || {};
  const trials = Array.isArray(audit.clause_trials) ? audit.clause_trials : [];
  const routeDecision = audit.route_decision || {};
  const phaseWrap = audit.phase_wrap_probe_28 || {};
  const phaseWrapAnalysis = phaseWrap.analysis || {};
  const phaseWrapExtension = phaseWrap.extension || {};
  const wrapExample = Array.isArray(phaseWrapExtension.new_pressure_examples)
    ? phaseWrapExtension.new_pressure_examples[0]
    : null;
  const resultRows = Object.keys(audit).length
    ? [
        ["max bits", audit.max_bits],
        ["template nodes", audit.template_node_count],
        ["template edges", audit.template_edge_count],
        ["raw open edges", audit.raw_open_edge_count],
        ["26-bit refuted clauses", audit.exactly_refuted_clause_family_count],
        ["future-wrap refuted clauses", audit.future_refuted_clause_family_count],
        ["sampled clause candidates", audit.sampled_clause_candidate_count],
        ["exact template clause status", audit.exact_template_clause_status],
        ["exact template 25->26 new clauses", audit.exact_template_new_clause_count_25_to_26],
        ["exact template 25->26 new pressure edges", audit.exact_template_new_pressure_edge_count_25_to_26],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const trialTable = trials.length
    ? table(
        ["clause family", "status", "clauses", "pressure edges", "scale", "min margin", "cycle"],
        trials.map((row) => [
          row.clause_family,
          row.status,
          row.clause_count,
          row.pressure_clause_edge_count,
          row.scale_interval?.selected_scale,
          row.scale_interval?.min_margin_at_selected_scale,
          row.pressure_topology?.cycle_detected,
        ]),
      )
    : "";
  const phaseWrapRows = Object.keys(phaseWrap).length
    ? [
        ["probe", phaseWrap.purpose],
        ["from->to", `${phaseWrap.from_max_bits} -> ${phaseWrap.to_max_bits}`],
        ["wrap status", phaseWrapAnalysis.status],
        ["new pressure clause edges", phaseWrapExtension.new_pressure_clause_edge_count],
        ["closure status", phaseWrapExtension.closure_status],
        [
          "first wrap edge",
          wrapExample
            ? `${wrapExample.parent_clause} -> ${wrapExample.child_clause}, delta ${formatValue(wrapExample.max_delta_debt)}`
            : "n/a",
        ],
      ]
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45">
      <h3>Ticket 45 symbolic rank clause lab</h3>
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
      ${table(["Symbolic clause result", "Value"], resultRows)}
      ${trialTable}
      ${phaseWrapRows.length ? table(["Phase-wrap probe", "Value"], phaseWrapRows) : ""}
      ${
        routeDecision.discard || routeDecision.retain
          ? `<div class="poc-bridge">
              <section>
                <h3>Discard</h3>
                ${list(routeDecision.discard || [])}
              </section>
              <section>
                <h3>Retain</h3>
                ${list(routeDecision.retain || [])}
              </section>
            </div>`
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket46StableClauseGrammar(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.stable_clause_grammar_audit || {};
  const summary = Array.isArray(audit.stability_summary) ? audit.stability_summary : [];
  const escapeAudit = Array.isArray(audit.escape_coordinate_audit) ? audit.escape_coordinate_audit : [];
  const firstWrap = audit.first_phase_wrap_pressure_edge || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["max bits", audit.max_bits],
        ["template nodes", audit.template_node_count_28],
        ["template edges", audit.template_edge_count_28],
        ["raw open edges", audit.raw_open_edge_count_28],
        ["tested clause families", audit.tested_clause_family_count],
        ["28-bit refuted families", audit.refuted_clause_family_count_28],
        ["28-bit stable families", audit.stable_clause_family_count_28],
        ["restricted no-go", audit.restricted_no_go_statement],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const summaryTable = summary.length
    ? table(
        ["grammar", "status", "clauses 28", "pressure 28", "new pressure 27->28", "cycle"],
        summary.map((row) => [
          row.clause_family,
          row.status,
          row.clause_count_28,
          row.pressure_clause_edge_count_28,
          row.new_pressure_edge_count_27_to_28,
          row.cycle_detected_28,
        ]),
      )
    : "";
  const escapeTable = escapeAudit.length
    ? table(
        ["repair candidate", "classification", "required next theorem"],
        escapeAudit.map((row) => [
          row.candidate,
          row.classification,
          row.required_next_theorem,
        ]),
      )
    : "";
  const firstWrapRows = firstWrap.parent_clause
    ? [
        ["edge", `${firstWrap.parent_clause} -> ${firstWrap.child_clause}`],
        ["max delta debt", firstWrap.max_delta_debt],
        ["count", firstWrap.count],
        ["example", JSON.stringify(firstWrap.example || {})],
      ]
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket46">
      <h3>Ticket 46 stable clause grammar lab</h3>
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
      ${table(["Stable grammar result", "Value"], resultRows)}
      ${summaryTable}
      ${firstWrapRows.length ? table(["First wrap pressure edge", "Value"], firstWrapRows) : ""}
      ${escapeTable}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket47PeriodicStateLasso(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.periodic_state_lasso_audit || {};
  const cycle = audit.cycle_summary || {};
  const automata = Array.isArray(audit.memory_automata) ? audit.memory_automata : [];
  const firstEdge = Array.isArray(cycle.cycle_edges_sample) ? cycle.cycle_edges_sample[0] : null;
  const resultRows = Object.keys(audit).length
    ? [
        ["max bits", audit.max_bits],
        ["template nodes", audit.template_node_count_28],
        ["template edges", audit.template_edge_count_28],
        ["pressure edges", audit.pressure_edge_count_28],
        ["raw open edges", audit.raw_open_edge_count_28],
        ["cycle edges", cycle.cycle_edge_count],
        ["unique symbols", cycle.unique_symbol_count],
        ["period debt", cycle.total_max_delta_debt],
        ["tested memory automata", audit.tested_memory_automaton_count],
        ["refuted memory automata", audit.refuted_memory_automaton_count],
        ["restricted no-go", audit.restricted_no_go_statement],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["discarded shortcut", bounded.discarded_shortcut],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const automataTable = automata.length
    ? table(
        ["automaton", "depth", "status", "returns after period"],
        automata.map((row) => [
          row.automaton,
          row.depth,
          row.periodic_lasso_status,
          row.returns_to_same_state_after_one_period,
        ]),
      )
    : "";
  const edgeRows = firstEdge
    ? [
        ["edge", `${firstEdge.parent_template} -> ${firstEdge.child_template}`],
        ["symbol", firstEdge.symbol],
        ["max delta debt", firstEdge.max_delta_debt],
        ["count", firstEdge.count],
      ]
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket47">
      <h3>Ticket 47 periodic state lasso lab</h3>
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
      ${table(["Periodic lasso result", "Value"], resultRows)}
      ${automataTable}
      ${edgeRows.length ? table(["First lasso edge", "Value"], edgeRows) : ""}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket48AutomatonReachability(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.automaton_reachability_audit || {};
  const cycle = audit.cycle_summary || {};
  const finite = audit.finite_state_period_map || {};
  const reachability = audit.reachability_probe || {};
  const startScan = audit.start_candidate_scan || {};
  const stateRows = Array.isArray(finite.state_rows) ? finite.state_rows : [];
  const stepRows = Array.isArray(reachability.step_rows_sample) ? reachability.step_rows_sample : [];
  const periodRows = Array.isArray(reachability.period_rows) ? reachability.period_rows : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["max bits", audit.max_bits],
        ["template nodes", audit.template_node_count_28],
        ["pressure edges", audit.pressure_edge_count_28],
        ["cycle edges", cycle.cycle_edge_count],
        ["period debt", cycle.total_max_delta_debt],
        ["finite-state lemma", finite.status],
        ["start-template matches", startScan.total_start_template_matches],
        ["stored starts", startScan.stored_start_candidate_count],
        ["reachability", reachability.status],
        ["completed lasso steps", reachability.completed_steps],
        ["best partial depth", reachability.best_partial_depth],
        ["best partial debt", reachability.best_partial_debt],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["finite-state no-go", bounded.finite_state_no_go],
        ["retained target", bounded.retained_target],
        ["counterexample target", bounded.counterexample_target],
      ];
  const finiteTable = stateRows.length
    ? table(
        ["finite states", "period bound", "expanded edges", "status"],
        stateRows.slice(0, 9).map((row) => [
          row.finite_state_count,
          row.period_map_cycle_bound,
          row.expanded_edge_bound,
          row.status,
        ]),
      )
    : "";
  const stepTable = stepRows.length
    ? table(
        ["step", "input paths", "matches", "nonnegative", "survivors"],
        stepRows.slice(0, 8).map((row) => [
          row.step,
          row.input_paths,
          row.matching_transitions,
          row.nonnegative_step_transitions,
          row.surviving_paths,
        ]),
      )
    : "";
  const periodTable = periodRows.length
    ? table(
        ["period", "node paths", "positive pressure paths", "best matching debt", "best pressure debt"],
        periodRows.map((row) => [
          row.period,
          row.matching_node_paths,
          row.positive_nonnegative_pressure_paths,
          row.best_matching_debt,
          row.best_pressure_debt,
        ]),
      )
    : `<p class="proof-note">No complete concrete lasso period was reached in the bounded residue-lift probe.</p>`;
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket48">
      <h3>Ticket 48 automaton reachability lab</h3>
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
      ${table(["Automaton/reachability result", "Value"], resultRows)}
      ${finiteTable}
      ${stepTable}
      ${periodTable}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket49SymbolicPreimage(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_preimage_obstruction_audit || {};
  const minimal = audit.minimal_obstruction || {};
  const forced = audit.forced_low_prefix || {};
  const anyDirection = audit.any_direction_prefix || {};
  const forcedRows = Array.isArray(forced.rows) ? forced.rows : [];
  const anyRows = Array.isArray(anyDirection.rows) ? anyDirection.rows : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["family", audit.family],
        ["start template", forced.start_template],
        ["start candidates", Array.isArray(forced.start_candidates) ? forced.start_candidates.length : null],
        ["forced-low dead step", minimal.dead_step],
        ["obstruction coordinate", minimal.obstruction_coordinate],
        ["required template", minimal.required_template],
        ["best partial depth", forced.best_partial_depth],
        ["best partial debt", forced.best_partial_debt],
        ["bounded statement", audit.closed_bounded_statement],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["obstruction coordinate", bounded.obstruction_coordinate],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  const forcedTable = forcedRows.length
    ? table(
        ["step", "input", "tested", "matches", "survivors", "mismatch"],
        forcedRows.map((row) => [
          row.step,
          row.input_states,
          row.tested_transitions,
          row.matching_transitions,
          row.surviving_states,
          JSON.stringify(row.mismatch_counts || {}),
        ]),
      )
    : "";
  const anyTable = anyRows.length
    ? table(
        ["any-dir step", "tested", "matches", "survivors", "mismatch"],
        anyRows.map((row) => [
          row.step,
          row.tested_transitions,
          row.matching_transitions,
          row.surviving_states,
          JSON.stringify(row.mismatch_counts || {}),
        ]),
      )
    : "";
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket49">
      <h3>Ticket 49 symbolic preimage obstruction lab</h3>
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
      ${table(["Symbolic preimage result", "Value"], resultRows)}
      ${forcedTable}
      ${anyTable}
      <p class="proof-note">${escapeHtml(minimal.interpretation || "")}</p>
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket50PhaseLiftException(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.phase_lift_exception_audit || {};
  const scans = Array.isArray(audit.phase_scans) ? audit.phase_scans : [];
  const lemma = audit.valuation_run_lemma || {};
  const scanRows = scans.map((scan) => [
    scan.bits,
    scan.open_valuation_words_with_tail,
    scan.verified_open_word_count,
    scan.start_template_match_count,
    scan.four_consecutive_one_exception_count,
    scan.max_lasso_prefix_depth,
    JSON.stringify(scan.lasso_prefix_depth_counts || {}),
  ]);
  const strongest = scans.flatMap((scan) =>
    Array.isArray(scan.strongest_near_lasso_examples)
      ? scan.strongest_near_lasso_examples.slice(0, 4).map((example) => [
          scan.bits,
          example.residue,
          example.lasso_prefix_depth,
          Array.isArray(example.next_valuation_window) ? example.next_valuation_window.join(", ") : "",
          example.first_failure?.observed || "none",
        ])
      : [],
  );
  const transferRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["method", audit.valuation_word_method],
        ["ticket49 candidate theorem", audit.ticket49_candidate_theorem_status],
        ["closed bounded statement", audit.closed_bounded_statement],
        ["next frontier", audit.next_frontier],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket50_transfer],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket50">
      <h3>Ticket 50 phase-lift exception lab</h3>
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
      ${table(["Phase-lift result", "Value"], transferRows)}
      ${
        lemma.statement
          ? `<p class="proof-note"><strong>Valuation-run lemma:</strong> ${escapeHtml(lemma.statement)} ${escapeHtml(lemma.proof_sketch || "")}</p>`
          : ""
      }
      ${
        scanRows.length
          ? table(
              ["bits", "open words", "verified", "start matches", "4x v=1 exceptions", "max lasso depth", "depth counts"],
              scanRows,
            )
          : ""
      }
      ${
        strongest.length
          ? table(["bits", "residue", "depth", "next valuation window", "first failure"], strongest)
          : ""
      }
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket51TerminalLift(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.phase15_terminal_lift_audit || {};
  const rows = Array.isArray(audit.rows) ? audit.rows : [];
  const terminalRows = rows.slice(-3).map((row) => [
    row.step,
    row.input_states,
    row.tested_branches,
    row.matching_branches,
    row.surviving_states,
    JSON.stringify(row.mismatch_counts || {}),
  ]);
  const terminalExamples = rows
    .slice(-1)
    .flatMap((row) => (Array.isArray(row.mismatch_examples) ? row.mismatch_examples.slice(0, 6) : []))
    .map((example) => [
      example.direction,
      example.root_residue,
      example.bits,
      example.observed,
      example.reason,
    ]);
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["roots", Array.isArray(audit.source_roots) ? audit.source_roots.join(", ") : ""],
        ["terminal step", audit.terminal_step],
        ["terminal mismatch", JSON.stringify(audit.terminal_mismatch_counts || {})],
        ["final survivors", audit.final_surviving_states],
        ["full lasso completions", audit.full_lasso_completion_count],
        ["best template depth", audit.best_template_depth],
        ["closed bounded statement", audit.closed_bounded_statement],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket51_transfer],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket51">
      <h3>Ticket 51 phase-15 terminal lift lab</h3>
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
      ${table(["Terminal lift result", "Value"], resultRows)}
      ${terminalRows.length ? table(["step", "input", "branches", "matches", "survivors", "mismatch"], terminalRows) : ""}
      ${terminalExamples.length ? table(["direction", "root", "bits", "observed", "reason"], terminalExamples) : ""}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket52FrontierBudget(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.frontier_budget_audit || {};
  const sample = audit.sampled_48bit_frontier || {};
  const terminal = sample.terminal_lift_audit || {};
  const counts = Array.isArray(audit.exact_open_word_counts) ? audit.exact_open_word_counts : [];
  const countRows = counts.map((row) => [row.bits, row.open_valuation_words_with_tail]);
  const stats = sample.statistics || {};
  const roots = Array.isArray(sample.new_depth15_roots) ? sample.new_depth15_roots : [];
  const rootRows = roots.map((root) => [
    root.sample_index,
    root.residue,
    root.projection32?.residue,
    root.projection32?.template,
    root.lasso_prefix_depth,
    root.first_failure?.observed || "none",
  ]);
  const terminalRows = Array.isArray(terminal.rows)
    ? terminal.rows.slice(-3).map((row) => [
        row.step,
        row.input_states,
        row.tested_branches,
        row.matching_branches,
        row.surviving_states,
        JSON.stringify(row.mismatch_counts || {}),
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["48-bit frontier", audit.direct_48bit_exhaustive_search_status],
        ["64-bit frontier", audit.direct_64bit_exhaustive_search_status],
        ["sample", `${sample.sample_count || 0} words / seed ${sample.sample_seed || ""}`],
        ["verified open words", stats.verified_open_word],
        ["start-template matches", stats.start_template_match],
        ["max sampled depth", sample.max_sampled_lasso_prefix_depth],
        ["new depth-15 roots", sample.new_depth15_root_count],
        ["terminal mismatch", JSON.stringify(terminal.terminal_mismatch_counts || {})],
        ["full lasso completions", terminal.full_lasso_completion_count],
        ["projection gap", audit.projection_completeness_failure],
        ["closed bounded statement", audit.closed_bounded_statement],
        ["next frontier", audit.next_frontier],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket52_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket52">
      <h3>Ticket 52 frontier budget lab</h3>
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
      ${table(["Frontier budget result", "Value"], resultRows)}
      ${countRows.length ? table(["bits", "open valuation words"], countRows) : ""}
      ${rootRows.length ? table(["sample", "48-bit residue", "projection32", "projection template", "depth", "first failure"], rootRows) : ""}
      ${terminalRows.length ? table(["step", "input", "branches", "matches", "survivors", "mismatch"], terminalRows) : ""}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket53SymbolicTerminal(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_terminal_theorem_audit || {};
  const roots = Array.isArray(audit.machine_checked_roots) ? audit.machine_checked_roots : [];
  const rootRows = roots.map((root) => [
    root.source_ticket,
    root.base_bits,
    root.residue,
    root.parent_template,
    root.low_terminal?.reason,
    root.high_terminal?.reason,
    root.high_next_valuation_before_terminal,
    root.terminal_target_matched ? "match" : "no match",
  ]);
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["theorem", audit.theorem_name],
        ["parent premise", audit.all_checked_roots_satisfy_parent_premise],
        ["terminal target matches", audit.terminal_target_match_count],
        ["low branch", audit.low_branch_argument],
        ["high branch", audit.high_branch_argument],
        ["scope", audit.terminal_theorem_scope],
        ["closed bounded statement", audit.closed_bounded_statement],
        ["next frontier", audit.next_frontier],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket53_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket53">
      <h3>Ticket 53 symbolic terminal theorem lab</h3>
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
      ${table(["Symbolic terminal result", "Value"], resultRows)}
      ${rootRows.length ? table(["source", "base bits", "residue", "parent", "low", "high", "high v", "target"], rootRows) : ""}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket54NewTemplateFamily(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.new_template_family_audit || {};
  const exact = audit.exact_32bit_post_terminal_reaudit || {};
  const sample = audit.sampled_48bit_post_terminal_summary || {};
  const candidate = audit.new_candidate_family || {};
  const phase5Rows = Object.entries(exact.phase5_next_valuation_counts || {}).map(([next, count]) => [
    next,
    count,
  ]);
  const topTemplateRows = Array.isArray(exact.top_phase5_gate_templates)
    ? exact.top_phase5_gate_templates.map((row) => [row.observed_template, row.count])
    : [];
  const sampleRows = sample.sample_count
    ? [
        ["sample words", sample.sample_count],
        ["start-template matches", sample.statistics?.start_template_match],
        ["discarded depth-15 samples", sample.discarded_depth15_sample_count],
        ["post-discard max depth", sample.max_remaining_depth_after_ticket53_discard],
        ["phase-5 gate samples", sample.phase5_gate_sample_count],
        ["boundary", sample.sample_boundary],
      ]
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["discarded theorem", audit.discarded_family?.source_theorem],
        ["exact 32-bit starts", exact.exact_start_template_matches],
        ["discarded exact depth-15 roots", exact.discarded_depth15_family_count],
        ["remaining exact starts", exact.remaining_after_ticket53_discard],
        ["post-discard max exact depth", exact.max_remaining_depth_after_ticket53_discard],
        ["phase-5 gate exact roots", exact.phase5_gate_count],
        ["phase-5 next=10 failures", exact.phase5_exact_next10_failure_count],
        ["new candidate family", candidate.name],
        ["next frontier", audit.next_frontier],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket54_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket54">
      <h3>Ticket 54 new template family lab</h3>
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
      ${table(["Post-terminal family result", "Value"], resultRows)}
      ${phase5Rows.length ? table(["phase-5 next valuation", "exact 32-bit count"], phase5Rows) : ""}
      ${topTemplateRows.length ? table(["top phase-5 template", "count"], topTemplateRows) : ""}
      ${sampleRows.length ? table(["48-bit sample field", "value"], sampleRows) : ""}
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(candidate.candidate_theorem || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(candidate.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket55Phase5Gate(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.phase5_gate_tunnel_audit || {};
  const bounded32 = audit.bounded_32bit_closure || {};
  const sample48 = audit.sampled_48bit_closure || {};
  const roots = Array.isArray(audit.machine_checked_roots) ? audit.machine_checked_roots : [];
  const rootRows = roots.map((root) => [
    root.source_ticket,
    root.base_bits,
    root.residue,
    root.gate_matches ? "gate" : "miss",
    root.tunnel_all_offsets_match ? "tunnel" : "break",
    root.terminal_reason,
    root.terminal_target_matched ? "match" : "no match",
  ]);
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["theorem", audit.theorem_name],
        ["gate matches", audit.gate_match_count],
        ["tunnel matches", audit.tunnel_match_count],
        ["same pending certificates", audit.same_pending_certificate_count],
        ["terminal target matches", audit.terminal_target_match_count],
        ["all gate roots closed", audit.all_gate_roots_tunnel_to_terminal_no_go],
        ["exact 32-bit starts", bounded32.exact_start_template_matches],
        ["failed before/at phase 5", bounded32.failed_before_or_at_phase5],
        ["gate crossers", bounded32.gate_crossers],
        ["gate crossers terminally closed", bounded32.gate_crossers_terminally_closed],
        ["48-bit sample gate count", sample48.phase5_gate_sample_count],
        ["next frontier", audit.next_frontier],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket55_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket55">
      <h3>Ticket 55 phase-5 valuation gate lab</h3>
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
      ${table(["Gate-to-terminal result", "Value"], resultRows)}
      ${rootRows.length ? table(["source", "base bits", "residue", "gate", "tunnel", "terminal reason", "target"], rootRows) : ""}
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
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket56PreGateProjection(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.pre_gate_projection_escape_audit || {};
  const exact32 = audit.exact32_pre_gate_partition || {};
  const projection = audit.projection_escape_audit || {};
  const offsetRows = Object.entries(exact32.pre_gate_failure_offsets || {}).map(([offset, count]) => [
    offset,
    count,
    (exact32.observed_next_valuation_by_offset || {})[offset]
      ? Object.entries(exact32.observed_next_valuation_by_offset[offset]).slice(0, 5).map(([value, n]) => `${value}:${n}`).join(", ")
      : "",
  ]);
  const escapeRows = Array.isArray(projection.escape_witnesses)
    ? projection.escape_witnesses.map((witness) => [
        witness.sample_index,
        witness.bits,
        witness.residue,
        witness.lasso_prefix_depth,
        witness.projection32?.template || "",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["local theorem", audit.local_theorem_name],
        ["exact 32-bit starts", exact32.exact_start_template_matches],
        ["pre-gate failures", exact32.pre_gate_failure_count],
        ["complete exact32 partition", exact32.partition_is_complete_for_exact32_start_template],
        ["phase-5 observed next=10", exact32.phase5_observed_next10_count],
        ["gate crossers", exact32.phase5_gate_crosser_count],
        ["projection closure", projection.simple_projection_closure_status],
        ["escape witnesses", escapeRows.length],
        ["retained route", audit.retained_route],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket56_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["candidate theorem", bounded.candidate_theorem],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket56">
      <h3>Ticket 56 pre-gate projection escape lab</h3>
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
      ${table(["Pre-gate partition result", "Value"], resultRows)}
      ${offsetRows.length ? table(["first-failure offset", "exact 32-bit count", "top next valuations"], offsetRows) : ""}
      ${escapeRows.length ? `<h3>Projection escape witness</h3>${table(["sample", "bits", "residue", "depth", "projection32 template"], escapeRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket57ParametricAutomaton(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.parametric_template_automaton_audit || {};
  const summary = audit.exact32_outcome_summary || {};
  const determinism = audit.exact32_state_determinism || {};
  const projection = audit.projection_escape_carry_forward || {};
  const replay = audit.known_root_replay_audit || {};
  const ladder = Array.isArray(determinism.ladder) ? determinism.ladder : [];
  const selectedLadder = ladder.filter((row) =>
    [
      "template_only",
      "template_plus_prefix_length",
      "template_plus_prefix_length_residue_mod_2^20",
      "template_plus_prefix_length_residue_mod_2^24",
      "template_plus_prefix_length_residue_mod_2^26",
      "template_plus_prefix_length_residue_mod_2^28",
    ].includes(row.abstraction),
  );
  const ladderRows = selectedLadder.map((row) => [
    row.abstraction,
    row.state_count,
    row.collision_group_count,
    row.ambiguous_candidate_count,
    row.largest_group_size,
  ]);
  const outcomeRows = Object.entries(summary.coarse_outcome_counts || {}).map(([outcome, count]) => [outcome, count]);
  const replayRows = Array.isArray(replay.replay_rows)
    ? replay.replay_rows.slice(0, 6).map((row) => [
        row.source,
        row.base_bits,
        row.residue,
        row.matched_prefix_templates,
        row.full_lasso_period_replayed ? "full replay" : "stops",
      ])
    : [];
  const escapeRows = Array.isArray(projection.escape_witnesses)
    ? projection.escape_witnesses.map((row) => [
        row.bits,
        row.residue,
        row.lasso_prefix_depth,
        row.projection_template,
        row.projection_matches_exact32_target ? "target" : "escape",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["theorem", audit.theorem_name],
        ["exact 32-bit starts", summary.total],
        ["first deterministic boundary", determinism.first_deterministic_abstraction],
        ["projection closure", projection.simple_projection_closure_status],
        ["projection escape witnesses", projection.escape_witness_count],
        ["known roots replayed", replay.known_root_count],
        ["max replayed depth", replay.max_replayed_prefix_depth],
        ["full lasso period replays", replay.full_lasso_period_replay_count],
        ["cycle status", replay.cycle_status],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket57_transfer],
        ["required variables", (bounded.required_state_variables || []).join(", ")],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket57">
      <h3>Ticket 57 parametric template automaton lab</h3>
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
      ${table(["Parametric automaton result", "Value"], resultRows)}
      ${outcomeRows.length ? table(["Exact32 outcome", "count"], outcomeRows) : ""}
      ${ladderRows.length ? table(["abstraction", "states", "collision groups", "ambiguous candidates", "largest group"], ladderRows) : ""}
      ${escapeRows.length ? `<h3>Projection escape carried forward</h3>${table(["bits", "residue", "depth", "projection template", "class"], escapeRows)}` : ""}
      ${replayRows.length ? `<h3>Replayable-cycle search</h3>${table(["source", "base bits", "residue", "matched depth", "period status"], replayRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket58AffineBoundaryLift(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.affine_boundary_lift_audit || {};
  const exact = audit.exact32_boundary || {};
  const sample = audit.sampled_48bit_lift_stability || {};
  const stats = sample.statistics || {};
  const depthRows = Object.entries(sample.depth_counts || {}).map(([depth, count]) => [depth, count]);
  const projectionRows = Object.entries(sample.projection32_template_counts || {})
    .slice(0, 8)
    .map(([template, count]) => [template, count]);
  const mismatchRows = Array.isArray(sample.boundary_prediction_mismatch_examples)
    ? sample.boundary_prediction_mismatch_examples.slice(0, 6).map((row) => [
        row.sample_index,
        row.residue,
        row.projection_residue,
        row.predicted_exact32_outcome,
        row.observed_48bit_outcome,
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", bounded.source_ticket],
        ["theorem", audit.theorem_name],
        ["exact32 boundary low bits", exact.low_bits],
        ["exact32 boundary states", exact.boundary_state_count],
        ["exact32 boundary collisions", exact.collision_count],
        ["48-bit sample count", sample.sample_count],
        ["48-bit start matches", stats.start_template_match],
        ["projection escapes", stats.projection_escape],
        ["projection target lifts", stats.projection_target],
        ["boundary prediction matches", stats.boundary_prediction_match],
        ["boundary prediction mismatches", stats.boundary_prediction_mismatch],
        ["target prediction rate", sample.projection_target_prediction_rate],
        ["lift stability", sample.lift_stability_status],
        ["full-period escape", sample.full_period_escape_status],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket58_transfer],
        ["lift gate", bounded.lift_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58">
      <h3>Ticket 58 affine-boundary lift lab</h3>
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
      ${table(["Affine-boundary lift result", "Value"], resultRows)}
      ${depthRows.length ? table(["48-bit matched depth", "count"], depthRows) : ""}
      ${projectionRows.length ? table(["projection32 template", "count"], projectionRows) : ""}
      ${mismatchRows.length ? `<h3>Boundary prediction mismatch examples</h3>${table(["sample", "residue", "projection32", "exact32 prediction", "48-bit outcome"], mismatchRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket59SymbolicLiftMismatch(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const cover = bounded.selected_low40_cylinder_cover || {};
  const aggregate = cover.aggregate_cylinder_statistics || {};
  const statusRows = Object.entries(cover.cylinder_status_counts || {}).map(([status, count]) => [status, count]);
  const representativeRows = Array.isArray(cover.representative_cylinders)
    ? cover.representative_cylinders.slice(0, 6).map((row) => [
        row.low40_residue,
        Array.isArray(row.seed_kinds) ? row.seed_kinds.join(", ") : "",
        row.statistics?.start_template_match,
        row.statistics?.projection_target,
        row.statistics?.boundary_prediction_mismatch,
        row.status,
      ])
    : [];
  const resultRows = Object.keys(cover).length
    ? [
        ["source ticket", cover.source_ticket],
        ["theorem", cover.theorem_name],
        ["low cylinder bits", cover.cylinder_low_bits],
        ["extension bits", cover.cylinder_extension_bits],
        ["selected cylinders", cover.selected_cylinder_count],
        ["tested 48-bit extensions", aggregate.tested_48bit_extensions],
        ["start-template lifts", aggregate.start_template_match],
        ["projection escapes", aggregate.projection_escape],
        ["projection target lifts", aggregate.projection_target],
        ["boundary matches", aggregate.boundary_prediction_match],
        ["boundary mismatches", aggregate.boundary_prediction_mismatch],
        ["mismatch seed cylinders", cover.boundary_mismatch_seed_cylinders],
        ["uniform mismatch cylinders", cover.boundary_mismatch_seed_cylinders_uniform],
        ["mixed/unstable cylinders", cover.mixed_or_unstable_cylinder_count],
        ["full-period escapes", cover.full_period_escape_count],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket59_transfer],
        ["cylinder gate", bounded.cylinder_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59">
      <h3>Ticket 59 symbolic lift mismatch lab</h3>
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
      ${table(["Counted cylinder result", "Value"], resultRows)}
      ${statusRows.length ? table(["cylinder status", "count"], statusRows) : ""}
      ${representativeRows.length ? `<h3>Representative low40 cylinders</h3>${table(["low40", "seed kind", "start lifts", "target lifts", "mismatches", "status"], representativeRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(cover.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(cover.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(cover.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket60MixedCylinderSeparator(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.mixed_cylinder_separator_audit || {};
  const mixed = audit.mixed_cylinder_separator_ladder || {};
  const all = audit.all_selected_separator_ladder || {};
  const scope = audit.separator_scope || {};
  const statusRows = Object.entries(audit.cylinder_status_counts || {}).map(([status, count]) => [status, count]);
  const outcomeRows = Object.entries(audit.outcome_counts || {}).map(([outcome, count]) => [outcome, count]);
  const ladderRows = Array.isArray(mixed.outcome_ladder)
    ? mixed.outcome_ladder.slice(0, 12).map((row) => [
        row.separator,
        row.state_count,
        row.collision_group_count,
        row.ambiguous_row_count,
        row.deterministic ? "yes" : "no",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem", audit.theorem_name],
        ["selected cylinders", audit.selected_low40_cylinder_count],
        ["selected start lifts", audit.selected_start_template_lift_count],
        ["mixed cylinders", audit.mixed_cylinder_count],
        ["mixed start lifts", audit.mixed_start_template_lift_count],
        ["low bits", scope.low_bits],
        ["extension bits", scope.extension_bits],
        ["mixed first outcome separator", mixed.first_outcome_deterministic_separator],
        ["mixed first prediction separator", mixed.first_prediction_deterministic_separator],
        ["mixed first joint separator", mixed.first_joint_deterministic_separator],
        ["all first joint separator", all.first_joint_deterministic_separator],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket60_transfer],
        ["separator gate", bounded.separator_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60">
      <h3>Ticket 60 mixed-cylinder separator lab</h3>
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
      ${table(["Separator result", "Value"], resultRows)}
      ${statusRows.length ? table(["cylinder status", "count"], statusRows) : ""}
      ${outcomeRows.length ? table(["selected outcome", "count"], outcomeRows) : ""}
      ${ladderRows.length ? `<h3>Mixed-cylinder outcome separator ladder</h3>${table(["separator", "states", "collision groups", "ambiguous rows", "deterministic"], ladderRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket61SymbolicFailureOffset(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_failure_offset_audit || {};
  const mixed = audit.mixed_pre_replay_separator_ladder || {};
  const all = audit.all_selected_pre_replay_separator_ladder || {};
  const mod16 = audit.mod16_mixed_joint_row || {};
  const top6 = audit.top6_mixed_joint_row || {};
  const failureRows = Array.isArray(mixed.failure_offset_ladder)
    ? mixed.failure_offset_ladder.slice(0, 12).map((row) => [
        row.separator,
        row.state_count,
        row.collision_group_count,
        row.ambiguous_row_count,
        row.deterministic ? "yes" : "no",
      ])
    : [];
  const jointRows = Array.isArray(mixed.joint_ladder)
    ? mixed.joint_ladder.slice(0, 12).map((row) => [
        row.separator,
        row.state_count,
        row.collision_groups ? row.collision_groups.failure_offset : "",
        row.collision_groups ? row.collision_groups.outcome_label : "",
        row.collision_groups ? row.collision_groups.prediction_label : "",
        row.deterministic_for_all_labels ? "yes" : "no",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["replay separator replaced", audit.source_replay_separator],
        ["theorem", audit.theorem_name],
        ["selected cylinders", audit.selected_low40_cylinder_count],
        ["selected start lifts", audit.selected_start_template_lift_count],
        ["mixed cylinders", audit.mixed_cylinder_count],
        ["mixed start lifts", audit.mixed_start_template_lift_count],
        ["mixed first failure separator", mixed.first_failure_offset_deterministic_separator],
        ["mixed first joint separator", mixed.first_joint_deterministic_separator],
        ["mixed first top-bit separator", mixed.first_top_bit_joint_deterministic_separator],
        ["all first joint separator", all.first_joint_deterministic_separator],
        ["mod16 joint deterministic", mod16.deterministic_for_all_labels ? "yes" : "no"],
        ["top6 joint deterministic", top6.deterministic_for_all_labels ? "yes" : "no"],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket61_transfer],
        ["symbolic gate", bounded.symbolic_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61">
      <h3>Ticket 61 symbolic failure-offset lab</h3>
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
      ${table(["Pre-replay separator result", "Value"], resultRows)}
      ${failureRows.length ? `<h3>Failure-offset pre-replay ladder</h3>${table(["separator", "states", "collision groups", "ambiguous rows", "deterministic"], failureRows)}` : ""}
      ${jointRows.length ? `<h3>Joint pre-replay ladder</h3>${table(["separator", "states", "failure collisions", "outcome collisions", "prediction collisions", "all deterministic"], jointRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket62Mod16TransitionCover(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.mod16_transition_cover_audit || {};
  const liftRows = Array.isArray(audit.lift_audits)
    ? audit.lift_audits.map((row) => [
        row.bits,
        row.status,
        row.statistics ? row.statistics.tested_lifts : "",
        row.statistics ? row.statistics.start_template_lift : "",
        row.base_rows_with_start_template_extension,
        row.base_mod16_joint_row && row.base_mod16_joint_row.collision_groups
          ? row.base_mod16_joint_row.collision_groups.failure_offset
          : "",
        row.first_joint_deterministic_separator,
      ])
    : [];
  const ladderRows = Array.isArray(audit.lift_audits) && audit.lift_audits[1] && Array.isArray(audit.lift_audits[1].joint_ladder)
    ? audit.lift_audits[1].joint_ladder.slice(0, 10).map((row) => [
        row.separator,
        row.state_count,
        row.collision_groups ? row.collision_groups.failure_offset : "",
        row.collision_groups ? row.collision_groups.transition_label : "",
        row.deterministic_for_all_labels ? "yes" : "no",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem", audit.theorem_name],
        ["base bits", audit.base_bits],
        ["base mixed cylinders", audit.base_mixed_cylinder_count],
        ["base mixed lifts", audit.base_mixed_start_template_lift_count],
        ["tested lift bits", Array.isArray(audit.tested_lift_bits) ? audit.tested_lift_bits.join(", ") : ""],
        ["mod16 obstruction count", audit.obstruction_count],
        ["full-period escapes", audit.full_period_escape_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket62_transfer],
        ["transition gate", bounded.transition_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62">
      <h3>Ticket 62 mod16 transition-cover lab</h3>
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
      ${table(["Transition-cover result", "Value"], resultRows)}
      ${liftRows.length ? `<h3>Bounded lift audits</h3>${table(["bits", "status", "tested lifts", "start-template lifts", "base rows with lift", "mod16 failure collisions", "first separator"], liftRows)}` : ""}
      ${ladderRows.length ? `<h3>56-bit joint separator ladder</h3>${table(["separator", "states", "failure collisions", "transition collisions", "all deterministic"], ladderRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket63Mod16AutomatonCover(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.mod16_automaton_cover_audit || {};
  const rowAuditRows = Array.isArray(audit.row_audits)
    ? audit.row_audits.map((row) => [
        row.label,
        row.row_count,
        row.state_table ? row.state_table.state_count : "",
        row.state_table ? row.state_table.collision_state_count : "",
        row.first_quotient_separator,
      ])
    : [];
  const chainStats = audit.chain_lift_statistics || {};
  const quotientRows = Array.isArray(audit.row_audits)
    ? ((audit.row_audits.find((row) => row.label === "60_bit_chained_from_56_survivors") || {}).quotient_ladder || {}).joint_ladder || []
    : [];
  const quotientTableRows = Array.isArray(quotientRows)
    ? quotientRows.slice(0, 8).map((row) => [
        row.separator,
        row.state_count,
        row.collision_groups ? row.collision_groups.root_transition_label : "",
        row.deterministic_for_all_labels ? "yes" : "no",
      ])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem", audit.theorem_name],
        ["base mixed cylinders", audit.base_mixed_cylinder_count],
        ["base mixed lifts", audit.base_mixed_start_template_lift_count],
        ["56-bit parent rows", audit.chain_parent_rows],
        ["60-bit chain target rows", audit.chain_target_rows],
        ["chain tested lifts", chainStats.tested_chain_lifts],
        ["chain start-template lifts", chainStats.start_template_chain_lift],
        ["automaton collision audits", audit.collision_audit_count],
        ["full-period escapes", audit.full_period_escape_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["source route", bounded.source_route],
        ["transfer", bounded.ticket63_transfer],
        ["automaton gate", bounded.automaton_gate],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63">
      <h3>Ticket 63 mod16 automaton-cover lab</h3>
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
      ${table(["Automaton-cover result", "Value"], resultRows)}
      ${rowAuditRows.length ? `<h3>State-table audits</h3>${table(["audit", "rows", "states", "collisions", "first quotient"], rowAuditRows)}` : ""}
      ${quotientTableRows.length ? `<h3>60-bit quotient ladder</h3>${table(["separator", "states", "root-transition collisions", "all deterministic"], quotientTableRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket64SymbolicMod16Transition(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_mod16_transition_audit || {};
  const gate = audit.gate_ladder || {};
  const state20 = gate.state20_gate_row || {};
  const state20Top4 = gate.state20_top4_gate_row || {};
  const formula = audit.symbolic_formula_pressure || {};
  const admitted = audit.admitted_child_audit || {};
  const table64 = admitted.state_table || {};
  const gateRows = Array.isArray(gate.gate_ladder)
    ? gate.gate_ladder.slice(0, 8).map((row) => [
        row.separator,
        row.state_count,
        row.collision_group_count,
        row.ambiguous_row_count,
        row.deterministic ? "yes" : "no",
      ])
    : [];
  const transitionRows = table64.transition_label_counts
    ? Object.entries(table64.transition_label_counts).map(([label, count]) => [label, count])
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["60-bit parent rows", audit.parent_60_rows],
        ["64-bit admitted rows", audit.target_64_rows],
        ["64-bit candidate children", audit.candidate_child_rows],
        ["start-template children", gate.start_template_count],
        ["non-start children", gate.non_start_template_count],
        ["state20 gate collisions", state20.collision_group_count],
        ["state20+top4 gate collisions", state20Top4.collision_group_count],
        ["optimistic 0->0 formula holds", formula.admitted_child_formula_holds ? "yes" : "no"],
        ["optimistic 0->0 formula fails", formula.admitted_child_formula_fails ? "yes" : "no"],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket64_transfer],
        ["gate", bounded.gate_name],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64">
      <h3>Ticket 64 symbolic mod16 transition lab</h3>
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
      ${table(["Symbolic transition result", "Value"], resultRows)}
      ${gateRows.length ? `<h3>64-bit admissibility gate ladder</h3>${table(["separator", "states", "gate collisions", "ambiguous rows", "deterministic"], gateRows)}` : ""}
      ${transitionRows.length ? `<h3>64-bit admitted transition labels</h3>${table(["transition", "count"], transitionRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket65StartTemplateChainExtinction(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.start_template_chain_extinction_audit || {};
  const survivorRows = Array.isArray(audit.survivor_sequence)
    ? audit.survivor_sequence.map((row) => [row.bits, row.rows])
    : [];
  const chainRows = Array.isArray(audit.chain_steps)
    ? audit.chain_steps.map((row) => [
        `${row.parent_bits}->${row.target_bits}`,
        row.parent_rows,
        row.tested_chain_lifts,
        row.start_template_chain_lift,
        row.non_start_template_chain_lift,
        row.boundary_match,
        row.boundary_mismatch,
      ])
    : [];
  const gateRows = Array.isArray(audit.gate_audits)
    ? audit.gate_audits.map((row) => {
        const summary = row.pre_replay_summary || {};
        const near = summary.best_compressed_near_miss || {};
        return [
          `${row.parent_bits}->${row.target_bits}`,
          row.candidate_child_rows,
          row.start_template_count,
          summary.first_compressed_deterministic_separator || "none",
          summary.first_row_unique_deterministic_separator || "none",
          near.separator || "none",
          near.collision_group_count ?? "",
          near.ambiguous_row_count ?? "",
        ];
      })
    : [];
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["survivor sequence", survivorRows.map((row) => `${row[0]}:${row[1]}`).join(" -> ")],
        ["extinction observed", audit.extinction_observed ? "yes" : "no"],
        ["extinction at bits", audit.extinction_at_bits],
        ["last nonempty bits", audit.last_nonempty_bits],
        ["last nonempty rows", audit.last_nonempty_rows],
        ["full-period replays", audit.full_lasso_period_replay_count],
        ["compressed gate found", audit.gate_compression_obstruction ? "no" : "check artifact"],
        ["bounded branch closed", audit.bounded_branch_closed ? "yes" : "no"],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket65_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65">
      <h3>Ticket 65 start-template chain extinction lab</h3>
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
      ${table(["Start-template extinction result", "Value"], resultRows)}
      ${survivorRows.length ? `<h3>Survivor sequence</h3>${table(["bits", "rows"], survivorRows)}` : ""}
      ${chainRows.length ? `<h3>Chain extinction ladder</h3>${table(["lift", "parents", "tested", "start", "non-start", "match", "mismatch"], chainRows)}` : ""}
      ${gateRows.length ? `<h3>Gate compression audit</h3>${table(["lift", "candidates", "starts", "compressed separator", "row-unique separator", "best near miss", "collisions", "ambiguous rows"], gateRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket66ComplementCover(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.complement_cover_audit || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["non-start complement candidates", audit.total_non_start_template_candidates],
        ["closed by immediate descent", audit.descent_closed_count],
        ["open needs_split instances", audit.open_needs_split_count],
        ["descent coverage rate", audit.descent_coverage_rate],
        ["unique open template families", audit.unique_open_template_count],
        ["largest open family", audit.largest_open_template_family ? `${audit.largest_open_template_family.key} (${audit.largest_open_template_family.count})` : "none"],
        ["complement cover status", audit.complement_cover_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket66_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  const perLiftRows = Array.isArray(audit.per_lift)
    ? audit.per_lift.map((row) => [
        `${row.parent_bits}->${row.target_bits}`,
        row.candidate_child_rows,
        row.start_template_count,
        row.non_start_template_count,
        row.status_counts?.needs_split ?? 0,
        row.status_counts?.all_lift_descent ?? 0,
        row.unique_open_templates,
      ])
    : [];
  const reasonRows = audit.global_reason_counts
    ? Object.entries(audit.global_reason_counts).map(([key, value]) => [key, value])
    : [];
  const templateRows = Array.isArray(audit.top_global_templates)
    ? audit.top_global_templates.slice(0, 8).map((row) => [row.key, row.count])
    : [];
  const tailRows = Array.isArray(audit.top_global_tail4)
    ? audit.top_global_tail4.slice(0, 8).map((row) => [row.key, row.count])
    : [];
  const nextRows = Array.isArray(audit.global_next_valuation_counts)
    ? audit.global_next_valuation_counts.slice(0, 8).map((row) => [row.key, row.count])
    : [];
  const openExampleRows = Array.isArray(audit.open_template_examples)
    ? audit.open_template_examples.slice(0, 5).map((row) => [
        row.lift,
        row.residue,
        row.template,
        row.reason,
        row.certificate?.prefix_length ?? "",
        row.certificate?.consumed_bits ?? "",
      ])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66">
      <h3>Ticket 66 complement-cover audit</h3>
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
      ${table(["Complement-cover result", "Value"], resultRows)}
      ${perLiftRows.length ? `<h3>Complement frontier by lift</h3>${table(["lift", "candidates", "start", "non-start", "needs_split", "descent", "open families"], perLiftRows)}` : ""}
      ${reasonRows.length ? `<h3>Exit class pressure</h3>${table(["class", "count"], reasonRows)}` : ""}
      ${templateRows.length ? `<h3>Largest open template families</h3>${table(["template", "count"], templateRows)}` : ""}
      ${tailRows.length ? `<h3>Tail-4 pressure</h3>${table(["tail4", "count"], tailRows)}` : ""}
      ${nextRows.length ? `<h3>Next-valuation pressure</h3>${table(["next valuation", "count"], nextRows)}` : ""}
      ${openExampleRows.length ? `<h3>Open complement examples</h3>${table(["lift", "residue", "template", "reason", "prefix", "consumed"], openExampleRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket67OpenTemplateRank(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.open_template_rank_audit || {};
  const graph = audit.graph_cycle_summary || {};
  const debt = audit.debt_rank_summary || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["source open instances", audit.source_open_instances],
        ["source template families", audit.source_open_template_families],
        ["child lift rows", audit.child_lift_rows],
        ["child needs_split", audit.child_status_counts?.needs_split ?? ""],
        ["child all_lift_descent", audit.child_status_counts?.all_lift_descent ?? ""],
        ["sources closed after one split", audit.closed_source_instances_after_one_split],
        ["sources still open after one split", audit.open_source_instances_after_one_split],
        ["one-step split closure rate", audit.one_step_split_closure_rate],
        ["open transition edges", audit.open_transition_edge_count],
        ["open transition weight", audit.open_transition_edge_weight],
        ["transition nodes", audit.transition_node_count],
        ["child open families", audit.child_open_template_families],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket67_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  const graphRows = Object.keys(graph).length
    ? [
        ["strict template rank", graph.strict_template_rank_status],
        ["cyclic components", graph.cyclic_component_count],
        ["cyclic nodes", graph.cyclic_node_count],
        ["largest cyclic component", graph.largest_cyclic_component_size],
        ["cycle edge weight", graph.cycle_edge_weight],
        ["source families reaching cycle", graph.source_families_reaching_cycle],
        ["cycle example", Array.isArray(graph.cycle_example) ? graph.cycle_example.join(" -> ") : ""],
      ]
    : [];
  const debtRows = Object.keys(debt).length
    ? [
        ["scalar debt rank", debt.scalar_debt_rank_status],
        ["negative delta", debt.debt_delta_counts?.negative ?? 0],
        ["positive delta", debt.debt_delta_counts?.positive ?? 0],
        ["zero delta", debt.debt_delta_counts?.zero ?? 0],
        ["nondecreasing edges", debt.nondecreasing_debt_edges],
        ["nondecreasing rate", debt.nondecreasing_debt_rate],
        ["max delta debt", debt.max_delta_debt],
        ["min delta debt", debt.min_delta_debt],
      ]
    : [];
  const sourceRows = Array.isArray(audit.top_source_families)
    ? audit.top_source_families.slice(0, 8).map((row) => [
        row.family,
        row.source_instances,
        row.open_child_edge_weight,
        row.distinct_child_templates,
        row.instances_with_open_child,
        row.in_cyclic_component ? "yes" : "no",
      ])
    : [];
  const edgeRows = Array.isArray(audit.top_transition_edges)
    ? audit.top_transition_edges.slice(0, 8).map((row) => [row.source, row.target, row.count])
    : [];
  const childRows = Array.isArray(audit.top_child_templates)
    ? audit.top_child_templates.slice(0, 8).map((row) => [row.key, row.count])
    : [];
  const nondecreasingRows = Array.isArray(debt.nondecreasing_examples)
    ? debt.nondecreasing_examples.slice(0, 5).map((row) => [
        row.source_template,
        row.child_template,
        row.source_bits,
        row.child_top,
        row.delta_debt,
      ])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67">
      <h3>Ticket 67 open-template rank audit</h3>
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
      ${table(["Open-template rank result", "Value"], resultRows)}
      ${graphRows.length ? `<h3>Template transition cycle</h3>${table(["Graph field", "Value"], graphRows)}` : ""}
      ${debtRows.length ? `<h3>Scalar debt-rank pressure</h3>${table(["Debt field", "Value"], debtRows)}` : ""}
      ${sourceRows.length ? `<h3>Largest source families</h3>${table(["family", "instances", "open child weight", "child templates", "open instances", "in cycle"], sourceRows)}` : ""}
      ${edgeRows.length ? `<h3>Heaviest open transitions</h3>${table(["source", "target", "count"], edgeRows)}` : ""}
      ${childRows.length ? `<h3>Top child templates</h3>${table(["template", "count"], childRows)}` : ""}
      ${nondecreasingRows.length ? `<h3>Nondecreasing debt examples</h3>${table(["source", "child", "bits", "child top", "delta debt"], nondecreasingRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket68CycleSccRefinement(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.cycle_scc_refinement_audit || {};
  const source = audit.source_cycle_summary || {};
  const strongest = audit.strongest_acyclic_refinement || {};
  const tail = audit.strongest_tail_residue_refinement_without_prefix_consumed || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["base transition nodes", source.base_transition_nodes],
        ["base transition edges", source.base_transition_edges],
        ["base transition weight", source.base_transition_weight],
        ["base cyclic nodes", source.cyclic_node_count],
        ["base cycle edge weight", source.cycle_edge_weight],
        ["internal SCC transition weight", audit.source_internal_cycle_transition_weight],
        ["open exits from cycle", audit.source_open_exits_from_cycle_weight],
        ["tested refinement families", audit.tested_refinement_family_count],
        ["refinement status", audit.refinement_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket68_transfer],
        ["frontier rule", bounded.frontier_rule],
        ["counterexample target", bounded.counterexample_target],
      ];
  const strongestRows = Object.keys(strongest).length
    ? [
        ["acyclic refinement", strongest.family_id],
        ["refined states", strongest.state_count],
        ["refined edges", strongest.edge_count],
        ["observed topological rank", strongest.max_observed_topological_rank],
      ]
    : [];
  const tailRows = Object.keys(tail).length
    ? [
        ["tail/residue refinement", tail.family_id],
        ["remaining cyclic nodes", tail.cyclic_node_count],
        ["largest component", tail.largest_cyclic_component_size],
        ["cyclic edge weight", tail.cyclic_edge_weight],
      ]
    : [];
  const refinementRows = Array.isArray(audit.refinement_rows)
    ? audit.refinement_rows.map((row) => [
        row.family_id,
        row.state_count,
        row.edge_count,
        row.cyclic_node_count,
        row.largest_cyclic_component_size,
        row.cyclic_edge_weight,
        row.graph_status,
      ])
    : [];
  const dag = Array.isArray(audit.refinement_rows)
    ? (audit.refinement_rows.find((row) => row.family_id === strongest.family_id) || {}).dag_rank_summary || {}
    : {};
  const topRankRows = Array.isArray(dag.top_rank_states)
    ? dag.top_rank_states.slice(0, 5).map((row) => [row.state, row.rank])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68">
      <h3>Ticket 68 cycle-SCC refinement</h3>
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
      ${table(["Cycle refinement result", "Value"], resultRows)}
      ${strongestRows.length ? `<h3>Strongest acyclic refinement</h3>${table(["Field", "Value"], strongestRows)}` : ""}
      ${tailRows.length ? `<h3>Best tail/residue-only pressure</h3>${table(["Field", "Value"], tailRows)}` : ""}
      ${refinementRows.length ? `<h3>Refinement family comparison</h3>${table(["family", "states", "edges", "cyclic nodes", "largest cycle", "cycle weight", "status"], refinementRows)}` : ""}
      ${topRankRows.length ? `<h3>Observed DAG rank states</h3>${table(["state", "rank"], topRankRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket69PrefixConsumedRank(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.prefix_consumed_rank_audit || {};
  const rank = audit.rank_summary || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["coordinate family", audit.coordinate_family],
        ["source base cycle nodes", audit.source_base_cycle_nodes],
        ["internal transition weight", audit.source_internal_transition_weight],
        ["rank status", rank.status],
        ["rank states", rank.rank_map_state_count],
        ["max rank", rank.max_rank],
        ["rank edge weight", audit.rank_edge_weight],
        ["nondecreasing rank edges", audit.rank_nondecreasing_edge_count],
        ["source instances in base cycle", audit.source_instances_in_base_cycle],
        ["source-expanded states", audit.source_expanded_state_count],
        ["child-only unexpanded states", audit.child_only_unexpanded_state_count],
        ["rank certificate status", audit.rank_certificate_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket69_transfer],
        ["counterexample target", bounded.counterexample_target],
      ];
  const outcomeRows = audit.child_outcome_counts
    ? Object.entries(audit.child_outcome_counts).map(([key, value]) => [key, value])
    : [];
  const rankLevelRows = Array.isArray(audit.rank_level_rows)
    ? audit.rank_level_rows.map((row) => [
        row.rank,
        row.state_count,
        row.source_representative_weight,
        row.child_representative_weight,
        row.concrete_source_instances,
        row.unexpanded_child_only_states,
      ])
    : [];
  const deltaRows = audit.weighted_rank_edge_delta_counts
    ? Object.entries(audit.weighted_rank_edge_delta_counts).map(([key, value]) => [key, value])
    : [];
  const frontierRows = Array.isArray(audit.unexpanded_frontier_examples)
    ? audit.unexpanded_frontier_examples.slice(0, 5).map((row) => [
        row.state,
        row.rank,
        row.child_representatives,
      ])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69">
      <h3>Ticket 69 prefix/consumed rank certificate</h3>
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
      ${table(["Rank certificate result", "Value"], resultRows)}
      ${outcomeRows.length ? `<h3>Concrete child outcomes</h3>${table(["outcome", "count"], outcomeRows)}` : ""}
      ${rankLevelRows.length ? `<h3>Rank frontier by level</h3>${table(["rank", "states", "source edge reps", "child reps", "source instances", "unexpanded child-only"], rankLevelRows)}` : ""}
      ${deltaRows.length ? `<h3>Weighted rank-edge deltas</h3>${table(["rank delta", "edge weight"], deltaRows)}` : ""}
      ${frontierRows.length ? `<h3>Unexpanded frontier examples</h3>${table(["state", "rank", "child reps"], frontierRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket70PrefixFrontierExpansion(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.prefix_frontier_expansion_audit || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["coordinate family", audit.coordinate_family],
        ["source frontier states", audit.source_child_only_frontier_states],
        ["frontier representatives", audit.frontier_representative_count],
        ["expansion edge weight", audit.expansion_edge_weight],
        ["frontier internal edges", audit.frontier_internal_edge_weight],
        ["known-rank nondecreasing edges", audit.known_rank_nondecreasing_edge_count],
        ["rank-equal re-entry edges", audit.known_rank_equal_edge_count],
        ["rank-increase re-entry edges", audit.known_rank_increase_edge_count],
        ["new unranked internal edges", audit.new_unranked_internal_edge_count],
        ["representative-nondeterministic states", audit.frontier_state_nondeterminism_count],
        ["one-step cycle components", audit.combined_graph_cycle_summary?.cyclic_component_count],
        ["frontier expansion status", audit.frontier_expansion_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket70_transfer],
        ["counterexample target", bounded.counterexample_target],
      ];
  const outcomeRows = audit.outcome_counts
    ? Object.entries(audit.outcome_counts).map(([key, value]) => [key, value])
    : [];
  const stateClassRows = audit.state_class_counts
    ? Object.entries(audit.state_class_counts).map(([key, value]) => [key, value])
    : [];
  const deltaRows = audit.rank_delta_counts
    ? Object.entries(audit.rank_delta_counts).map(([key, value]) => [key, value])
    : [];
  const profileRows = Array.isArray(audit.top_state_outcome_profiles)
    ? audit.top_state_outcome_profiles.slice(0, 5).map((row) => [row.key, row.count])
    : [];
  const exampleRows = Array.isArray(audit.frontier_state_examples)
    ? audit.frontier_state_examples.slice(0, 5).map((row) => [
        row.state,
        row.representative_count,
        row.state_class,
      ])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70">
      <h3>Ticket 70 prefix frontier expansion</h3>
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
      ${table(["Frontier expansion result", "Value"], resultRows)}
      ${outcomeRows.length ? `<h3>One-step branch outcomes</h3>${table(["outcome", "count"], outcomeRows)}` : ""}
      ${stateClassRows.length ? `<h3>Frontier state classes</h3>${table(["state class", "count"], stateClassRows)}` : ""}
      ${deltaRows.length ? `<h3>Known-rank re-entry deltas</h3>${table(["rank delta", "edge count"], deltaRows)}` : ""}
      ${profileRows.length ? `<h3>Top outcome profiles</h3>${table(["profile", "state count"], profileRows)}` : ""}
      ${exampleRows.length ? `<h3>Frontier state examples</h3>${table(["state", "representatives", "class"], exampleRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket71StrongerFrontierCoordinate(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.stronger_frontier_coordinate_audit || {};
  const bestTransition = audit.best_transition_separator || {};
  const bestFrontier = audit.best_frontier_reduction || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["frontier states", audit.frontier_source_state_count],
        ["frontier representatives", audit.frontier_representative_count],
        ["branch weight", audit.frontier_branch_weight],
        ["tested coordinate families", audit.tested_coordinate_family_count],
        ["best separator", bestTransition.family_id],
        ["best separator mixed keys", bestTransition.mixed_transition_key_count],
        ["best separator transition keys", bestTransition.transition_key_count],
        ["best separator child-only frontier", bestTransition.child_only_after_expansion_state_count],
        ["best compact frontier", bestFrontier.family_id],
        ["compact child-only frontier", bestFrontier.child_only_after_expansion_state_count],
        ["frontier coordinate status", audit.frontier_coordinate_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket71_transfer],
        ["counterexample target", bounded.counterexample_target],
      ];
  const pressureRows = audit.pressure_outcome_counts
    ? Object.entries(audit.pressure_outcome_counts).map(([key, value]) => [key, value])
    : [];
  const coordinateRows = Array.isArray(audit.coordinate_rows)
    ? audit.coordinate_rows.map((row) => [
        row.family_id,
        row.state_count,
        row.child_only_after_expansion_state_count,
        row.transition_key_count,
        row.mixed_transition_key_count,
        row.rank_summary?.max_rank,
        row.rank_summary?.status,
      ])
    : [];
  const mixedRows = Array.isArray(audit.coordinate_rows)
    ? (audit.coordinate_rows.find((row) => row.family_id === "base_prefix_consumed")?.mixed_transition_examples || [])
        .slice(0, 4)
        .map((row) => [row.transition_key, JSON.stringify(row.outcome_profile)])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71">
      <h3>Ticket 71 stronger frontier coordinates</h3>
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
      ${table(["Stronger coordinate result", "Value"], resultRows)}
      ${pressureRows.length ? `<h3>Pressure outcomes</h3>${table(["outcome", "count"], pressureRows)}` : ""}
      ${coordinateRows.length ? `<h3>Coordinate family comparison</h3>${table(["family", "states", "child-only frontier", "transition keys", "mixed keys", "max rank", "rank status"], coordinateRows)}` : ""}
      ${mixedRows.length ? `<h3>Compact-coordinate mixed examples</h3>${table(["transition key", "outcome profile"], mixedRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket72InfiniteFrontierLiftClosure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.infinite_frontier_lift_closure_audit || {};
  const best = audit.best_candidate_coordinate || {};
  const bestCompact = audit.best_compact_candidate_coordinate || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["theorem pressure target", audit.theorem_name],
        ["reconstructed branch weight", audit.reconstructed_frontier_branch_weight],
        ["mixed transition keys", audit.reconstructed_mixed_transition_key_count],
        ["open-pressure mixed keys", audit.reconstructed_pressure_mixed_transition_key_count],
        ["top mixed keys tested", audit.selected_top_mixed_key_count],
        ["first-layer pressure rows", audit.selected_first_layer_pressure_rows],
        ["second-layer rows", audit.selected_second_layer_rows],
        ["second-layer open pressure", audit.selected_second_layer_open_pressure_rows],
        ["second-layer rank descents", audit.selected_second_layer_rank_descent_rows],
        ["open-pressure mixed-key re-entry", audit.selected_second_layer_open_pressure_mixed_key_reentry_count],
        ["third-probe open pressure", audit.third_probe_open_pressure_rows],
        ["third-probe open-pressure re-entry", audit.third_probe_open_pressure_mixed_key_reentry_count],
        ["best candidate", best.family_id],
        ["best candidate mixed keys", best.mixed_transition_key_count],
        ["best compact candidate", bestCompact.family_id],
        ["best compact mixed keys", bestCompact.mixed_transition_key_count],
        ["lift closure status", audit.lift_closure_status],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [
        ["source ticket", bounded.source_ticket],
        ["transfer", bounded.ticket72_transfer],
        ["counterexample target", bounded.counterexample_target],
      ];
  const outcomeRows = audit.selected_second_layer_outcome_counts
    ? Object.entries(audit.selected_second_layer_outcome_counts).map(([key, value]) => [key, value])
    : [];
  const coordinateRows = Array.isArray(audit.candidate_coordinate_rows)
    ? audit.candidate_coordinate_rows.map((row) => [
        row.family_id,
        row.scope,
        row.state_count,
        row.transition_key_count,
        row.mixed_transition_key_count,
        row.pressure_transition_key_count,
      ])
    : [];
  const selectedRows = Array.isArray(audit.selected_key_summaries)
    ? audit.selected_key_summaries.slice(0, 8).map((row) => [
        row.transition_key,
        row.first_layer_rows,
        row.first_layer_pressure_rows,
        row.second_layer_rows,
        row.second_layer_open_pressure_mixed_key_reentry_count,
      ])
    : [];
  const reentryRows = Array.isArray(audit.examples?.second_layer_open_pressure_mixed_reentry)
    ? audit.examples.second_layer_open_pressure_mixed_reentry.slice(0, 4).map((row) => [
        row.source_transition_key,
        row.outcome_class,
        row.source_rank,
        row.child_rank,
      ])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72">
      <h3>Ticket 72 infinite frontier lift closure</h3>
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
      ${table(["Lift-closure result", "Value"], resultRows)}
      ${outcomeRows.length ? `<h3>Second-lift outcomes</h3>${table(["outcome", "count"], outcomeRows)}` : ""}
      ${coordinateRows.length ? `<h3>Second-lift coordinate comparison</h3>${table(["family", "scope", "states", "transition keys", "mixed keys", "open-pressure keys"], coordinateRows)}` : ""}
      ${selectedRows.length ? `<h3>Top mixed-key lift summaries</h3>${table(["first transition key", "rows", "open pressure", "second rows", "open-pressure re-entry"], selectedRows)}` : ""}
      ${reentryRows.length ? `<h3>Open-pressure re-entry examples</h3>${table(["transition key", "outcome", "source rank", "child rank"], reentryRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Counterexample target</h3>
          <p>${escapeHtml(audit.counterexample_target || bounded.counterexample_target || attempt.obstruction || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket73LineagePressureForest(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.lineage_pressure_forest_audit || {};
  const third = audit.third_all_source_reentry_audit || {};
  const fourth = audit.fourth_reentry_audit || {};
  const fifth = audit.fifth_reentry_audit || {};
  const survival = audit.root_survival_counts || {};
  const logic = audit.logical_boundary_audit || {};
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["finite-root theorem target", audit.theorem_name],
        ["strict re-entry roots", audit.reconstructed_second_layer_open_pressure_mixed_root_count],
        ["third-lift exact rows", third.row_count],
        ["third strict re-entries", third.open_pressure_mixed_key_reentry_count],
        ["fourth-lift exact rows", fourth.row_count],
        ["fourth strict re-entries", fourth.open_pressure_mixed_key_reentry_count],
        ["fifth-lift exact rows", fifth.row_count],
        ["fifth strict re-entries", fifth.open_pressure_mixed_key_reentry_count],
        ["roots surviving third / fourth / fifth", `${survival.through_third_lift ?? "-"} / ${survival.through_fourth_lift ?? "-"} / ${survival.through_fifth_lift ?? "-"}`],
        ["last tested modulus bits", logic.tested_last_modulus_bits],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket73_transfer || attempt.route || "missing"]];
  const outcomeRows = Object.keys(audit).length
    ? [
        ["third", third.open_pressure_rows, third.mixed_key_reentry_count, third.open_pressure_mixed_key_reentry_count],
        ["fourth", fourth.open_pressure_rows, fourth.mixed_key_reentry_count, fourth.open_pressure_mixed_key_reentry_count],
        ["fifth", fifth.open_pressure_rows, fifth.mixed_key_reentry_count, fifth.open_pressure_mixed_key_reentry_count],
      ]
    : [];
  const witness = audit.witness_pressure_reentry_spine || {};
  const witnessRows = Array.isArray(witness.rows)
    ? witness.rows.map((row) => [row.depth, row.outcome_class, row.source_rank, row.child_rank, row.child_certificate?.modulus_bits])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73">
      <h3>Ticket 73 lineage-constrained pressure forest</h3>
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
      ${table(["Lineage audit", "Value"], resultRows)}
      ${outcomeRows.length ? `<h3>Strict re-entry exhaustion</h3>${table(["lift", "open pressure", "mixed re-entry", "strict re-entry"], outcomeRows)}` : ""}
      ${witnessRows.length ? `<h3>Exact finite witness spine</h3>${table(["depth", "outcome", "source rank", "child rank", "child modulus"], witnessRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Finite decision</h3>
          <p>${escapeHtml(logic.strict_reentry_chain_decision || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Coverage boundary</h3>
          <p>${escapeHtml(logic.coverage_gap || attempt.claim_boundary || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket74CoverageLeakageEscapeForest(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.coverage_leakage_escape_forest_audit || {};
  const coverage = audit.coverage_audit || {};
  const fifth = audit.fifth_open_pressure_escape_audit || {};
  const sixth = audit.sixth_escape_pressure_audit || {};
  const formatRatio = (value) => (value && value.denominator ? `${formatValue(value.numerator)} / ${formatValue(value.denominator)} (${(Number(value.fraction) * 100).toFixed(3)}%)` : "-");
  const resultRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["coverage theorem target", audit.theorem_name],
        ["pressure mixed keys", audit.reconstructed_pressure_mixed_transition_key_count],
        ["selected top-key coverage", formatRatio(coverage.selected_top_mixed_key_coverage)],
        ["selected row coverage", formatRatio(coverage.selected_first_layer_row_coverage)],
        ["selected open-pressure coverage", formatRatio(coverage.selected_first_layer_open_pressure_coverage)],
        ["selected strict roots", coverage.selected_root_count],
        ["fifth open pressure", fifth.open_pressure_count],
        ["fifth original-cover re-entry", fifth.open_pressure_original_mixed_reentry_count],
        ["fifth new unranked pressure", fifth.new_unranked_internal_count],
        ["sixth exact rows", sixth.row_count],
        ["sixth open pressure", sixth.open_pressure_count],
        ["sixth original-cover re-entry", sixth.open_pressure_original_mixed_reentry_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket74_transfer || attempt.route || "missing"]];
  const leakageRows = Object.keys(audit).length
    ? [
        ["fifth", fifth.source_count, fifth.row_count, fifth.open_pressure_count, fifth.open_pressure_original_mixed_reentry_count, fifth.new_unranked_internal_count],
        ["sixth", sixth.source_count, sixth.row_count, sixth.open_pressure_count, sixth.open_pressure_original_mixed_reentry_count, sixth.new_unranked_internal_count],
      ]
    : [];
  const escapeRows = Array.isArray(fifth.examples)
    ? fifth.examples.slice(0, 4).map((row) => [row.source_transition_key, row.outcome_class, row.child_certificate?.modulus_bits, row.transition_key_is_original_mixed])
    : [];
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74">
      <h3>Ticket 74 coverage leakage and escaping pressure forest</h3>
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
      ${table(["Coverage leakage audit", "Value"], resultRows)}
      ${leakageRows.length ? `<h3>Escaping-pressure expansion</h3>${table(["lift", "sources", "exact rows", "open pressure", "old-cover re-entry", "new unranked"], leakageRows)}` : ""}
      ${escapeRows.length ? `<h3>Fifth-lift escaping examples</h3>${table(["transition key", "outcome", "child modulus", "old-cover re-entry"], escapeRows)}` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket75EscapeCoordinateClosure(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.escape_coordinate_closure_audit || {};
  const replay = audit.replay_audit || {};
  const families = Array.isArray(audit.coordinate_family_results) ? audit.coordinate_family_results : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["fixed finite coordinates", audit.fixed_finite_coordinate_family_count],
        ["fifth open pressure", replay.fifth_open_pressure_row_count],
        ["sixth open pressure", replay.sixth_open_pressure_row_count],
        ["extension failures", replay.exact_extension_failure_count],
        ["passing coordinates", (audit.two_layer_gate_passing_family_ids || []).length],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket75_transfer || attempt.route || "missing"]];
  const familyRows = families.map((family) => {
    const graph = family.observed_pressure_graph || {};
    const novelty = family.novel_sixth_open_row_ratio || {};
    return [
      family.family_id,
      family.novel_sixth_open_row_count,
      novelty.fraction == null ? "-" : `${(Number(novelty.fraction) * 100).toFixed(3)}%`,
      graph.cyclic_node_count,
      graph.mixed_pressure_outcome_key_count,
      family.two_layer_finite_closure_gate_passed ? "pass" : "blocked",
    ];
  });
  const reference = audit.unbounded_reference_coordinate || {};
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75">
      <h3>Ticket 75 fixed-coordinate closure audit</h3>
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
          <span>Evidence scope</span>
          <strong>${Object.keys(audit).length ? "Collatz exact replay" : "method transfer only"}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${table(["Coordinate closure audit", "Value"], summaryRows)}
      ${familyRows.length ? `<h3>Compression versus state growth</h3>${table(["finite coordinate", "novel sixth rows", "novel share", "cyclic nodes", "mixed keys", "gate"], familyRows)}` : ""}
      ${reference.reason ? `<div class="proof-note"><strong>Unbounded reference blocked:</strong> ${escapeHtml(reference.reason)}</div>` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket76SymbolicBoundaryRecurrence(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.symbolic_boundary_recurrence_audit || {};
  const fifth = audit.fifth_formula_audit || {};
  const sixth = audit.sixth_formula_audit || {};
  const symbolic = audit.symbolic_objects || {};
  const precisions = Array.isArray(audit.precision_closure_audits) ? audit.precision_closure_audits : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["audited transitions", audit.combined_formula_row_count],
        ["formula failures", audit.combined_formula_failure_count],
        ["fifth unresolved children", fifth.unresolved_same_prefix_child_count],
        ["sixth unresolved children", sixth.unresolved_same_prefix_child_count],
        ["fixed precisions refuted", (audit.fixed_precision_collision_precisions || []).join(", ")],
        ["lookahead failures", (audit.lookahead_failure_precisions || []).length],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket76_transfer || attempt.route || "missing"]];
  const precisionRows = precisions.map((item) => [
    item.precision_bits,
    item.unresolved_same_prefix_row_count,
    item.fixed_precision_transition_key_count,
    item.fixed_precision_collision_key_count,
    item.lookahead_precision_bits,
    item.lookahead_collision_key_count,
    item.fixed_precision_successor_sufficient_on_observed_rows ? "pass" : "refuted",
  ]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76">
      <h3>Ticket 76 symbolic boundary recurrence</h3>
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
          <span>Evidence scope</span>
          <strong>${Object.keys(audit).length ? "Collatz exact recurrence" : "method transfer only"}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${table(["Boundary recurrence audit", "Value"], summaryRows)}
      ${precisionRows.length ? `<h3>Fixed precision versus four-bit lookahead</h3>${table(["q bits", "unresolved rows", "fixed keys", "fixed collisions", "lookahead bits", "lookahead collisions", "fixed-q verdict"], precisionRows)}` : ""}
      ${Object.keys(symbolic).length ? `
        <div class="poc-bridge">
          <section>
            <h3>Exact valuation rule</h3>
            <p>${escapeHtml(symbolic.first_new_valuation_formula || "")}</p>
            <p>${escapeHtml(symbolic.unresolved_recurrence || "")}</p>
          </section>
          <section>
            <h3>Information-loss result</h3>
            <p>${escapeHtml(symbolic.precision_loss || "")}</p>
          </section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket77FixedPrefixBoundaryOrbit(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.fixed_prefix_boundary_orbit_audit || {};
  const observed = audit.observed_source_audit || {};
  const orbit = audit.orbit_identity || {};
  const orbitAudits = Array.isArray(orbit.audits) ? orbit.audits : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["observed boundary sources", observed.source_count],
        ["strict segments reaching equality", observed.strict_pressure_equality_boundary_count],
        ["maximum strict-pressure steps", observed.max_strict_pressure_step_count],
        ["prerequisite failures", observed.prerequisite_failure_count],
        ["one-step identity failures", observed.one_step_identity_failure_count],
        ["unexpected strict cycles", observed.unexpected_strict_cycle_count],
        ["orbit audit failures", orbit.audit_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket77_transfer || attempt.route || "missing"]];
  const orbitRows = orbitAudits.map((item) => {
    const classes = Array.isArray(item.class_audits) ? item.class_audits : [];
    return [
      item.prefix_length,
      item.unit,
      item.expected_order,
      classes.map((row) => `${row.odd_representative_count}/${row.even_representative_count}`).join(" / "),
      item.order_identity_holds && item.order_minimality_holds && classes.every((row) => row.covers_residue_class)
        ? "verified"
        : "failed",
    ];
  });
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77">
      <h3>Ticket 77 fixed-prefix boundary orbit</h3>
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
          <span>Evidence scope</span>
          <strong>${Object.keys(audit).length ? "Collatz exact orbit classification" : "method transfer only"}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 교정:</strong> 홀수 P(A)는 안정 접두사 소멸이 아니라 equality valuation입니다. 이 step은 rollback되므로 strict pressure 구간만 끝나고 정규화된 고정 접두사 궤도는 계속됩니다. all-depth 완성은 T^m(N)=-1/3인 2-adic ghost이며 양의 정수가 아닙니다.</p>` : ""}
      ${table(["Fixed-prefix boundary orbit audit", "Value"], summaryRows)}
      ${orbitRows.length ? `<h3>Inverse-16 periodic orbit audit</h3>${table(["prefix m", "3^(m+1)", "order", "odd/even states by mod-3 class", "verdict"], orbitRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section>
            <h3>Exact proof chain</h3>
            ${list(audit.proof_chain || [])}
          </section>
          <section>
            <h3>Equality rollback correction</h3>
            <p>Odd P(A) reaches the modulus boundary exactly and is rolled back. The compatible fixed-prefix limit satisfies T^m(N)=-1/3 in Z_2 and is not a positive integer.</p>
          </section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded inference</h3>
          <p>${escapeHtml(audit.discarded_route || "")}</p>
        </section>
        <section>
          <h3>Closed counterexample route</h3>
          <p>${escapeHtml(audit.closed_route || attempt.obstruction || "")}</p>
        </section>
      </div>
      <div class="poc-bridge">
        <section>
          <h3>Remaining obstruction</h3>
          <p>${escapeHtml(audit.remaining_obstruction || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket78FiniteCylinderNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.finite_cylinder_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const perTotal = Array.isArray(machine.per_total_valuation) ? machine.per_total_valuation : [];
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["finite valuation words", machine.total_word_count],
        ["positive representatives", machine.total_positive_representative_count],
        ["residue collisions", machine.residue_collision_count],
        ["formula failures", machine.formula_failure_count],
        ["representative replay failures", machine.representative_replay_failure_count],
        ["count-identity failures", machine.count_identity_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket78_transfer || attempt.route || "missing"]];
  const totalRows = perTotal.map((item) => [
    item.total_valuation,
    item.word_count,
    item.unique_residue_count,
    item.shifted_positive_representative_count,
    item.residue_collision_count,
    item.representative_replay_failure_count,
  ]);
  const rejectedRows = rejected.map((item) => [item.family, statusText(item.status), item.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77 poc-ticket78">
      <h3>Ticket 78 finite-cylinder admissibility no-go</h3>
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
          <span>Evidence scope</span>
          <strong>${Object.keys(audit).length ? "Collatz exact no-go lemma" : "method transfer only"}</strong>
        </div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 모든 유한 accelerated valuation word는 정확한 하나의 residue cylinder를 만들고, 그 cylinder에는 양의 정수가 무한히 많습니다. 따라서 고정된 residue bit나 유한 parity/valuation word만으로 2-adic ghost와 모든 자연수를 분리할 수 없습니다.</p>` : ""}
      ${table(["Finite-cylinder no-go audit", "Value"], summaryRows)}
      ${totalRows.length ? `<h3>All positive valuation compositions through S=16</h3>${table(["S", "words", "unique residues", "positive replays", "collisions", "replay failures"], totalRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected finite separator families</h3>${table(["family", "status", "exact counteredge"], rejectedRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section>
            <h3>Exact proof chain</h3>
            ${list(audit.proof_chain || [])}
          </section>
          <section>
            <h3>Literature boundary</h3>
            ${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}
          </section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section>
          <h3>Discarded route</h3>
          <p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p>
        </section>
        <section>
          <h3>Retained route</h3>
          <p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p>
        </section>
      </div>
      <div class="poc-bridge">
        <section>
          <h3>Candidate theorem</h3>
          <p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p>
        </section>
        <section>
          <h3>Novelty boundary</h3>
          <p>${escapeHtml(audit.novelty_boundary || attempt.claim_boundary || "")}</p>
        </section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket79ArchimedeanTwoAdicRankNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.archimedean_two_adic_rank_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const families = machine.exact_families || {};
  const thresholds = machine.rank_thresholds || {};
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const expansionSamples = Array.isArray(families.expansion_samples) ? families.expansion_samples : [];
  const contractionSamples = Array.isArray(families.contraction_samples) ? families.contraction_samples : [];
  const positiveRows = Array.isArray(thresholds.positive_alpha_rows) ? thresholds.positive_alpha_rows.slice(0, 8) : [];
  const negativeRows = Array.isArray(thresholds.negative_alpha_rows) ? thresholds.negative_alpha_rows.slice(0, 8) : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["expansion family cases", families.expansion_family_case_count],
        ["accelerated expansion replays", families.expansion_step_replay_count],
        ["nonterminal contraction cases", families.contraction_family_case_count],
        ["exact-family failures", families.exact_family_failure_count],
        ["coefficient threshold certificates", (thresholds.positive_alpha_certificate_count || 0) + (thresholds.negative_alpha_certificate_count || 0) + (thresholds.zero_alpha_certificate_count || 0)],
        ["threshold failures", thresholds.threshold_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket79_transfer || attempt.route || "missing"]];
  const expansionRows = expansionSamples.map((row) => [row.m, row.start, row.terminal, row.valuation_word]);
  const contractionRows = contractionSamples.map((row) => [row.r, row.start, row.terminal, row.valuation]);
  const thresholdRows = [
    ...positiveRows.map((row) => [row.alpha, row.bounded_correction_oscillation, `m=${row.witness_depth_m}`, row.lower_bound_on_total_rank_change]),
    ...negativeRows.map((row) => [row.alpha, row.bounded_correction_oscillation, `r=${row.witness_r}`, row.lower_bound_on_one_step_rank_change]),
  ];
  const rejectedRows = rejected.map((row) => [row.family, statusText(row.status), row.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77 poc-ticket78 poc-ticket79">
      <h3>Ticket 79 Archimedean-two-adic rank no-go</h3>
      <div class="poc-head">
        <div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div>
        <div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div>
        <div><span>Evidence scope</span><strong>${Object.keys(audit).length ? "exact Collatz rank no-go" : "method transfer only"}</strong></div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 실제 자연수 가족 E_(m,q)는 임의로 긴 valuation-1 팽창을 만들고, D_r는 임의로 커지면서도 한 단계에 terminal이 아닌 5로 내려갑니다. 따라서 log(n)에 bounded 2-adic 보정을 더한 보편적 일단계 순위는 계수의 부호와 무관하게 실패합니다.</p>` : ""}
      ${table(["TICKET79 rank no-go audit", "Value"], summaryRows)}
      ${expansionRows.length ? `<h3>Exact expansion family E_(m,1)</h3>${table(["m", "start", "terminal", "valuation word"], expansionRows)}` : ""}
      ${contractionRows.length ? `<h3>Exact nonterminal contraction family D_r → 5</h3>${table(["r", "start", "terminal", "valuation"], contractionRows)}` : ""}
      ${thresholdRows.length ? `<h3>Coefficient and correction-budget stress certificates</h3>${table(["alpha", "oscillation W", "witness", "positive rank-change lower bound"], thresholdRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected one-step rank families</h3>${table(["family", "status", "exact counteredge"], rejectedRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section>
          <section><h3>Literature boundary</h3>${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}</section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section>
        <section><h3>Retained route</h3><p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p></section>
      </div>
      <div class="poc-bridge">
        <section><h3>Next contrapositive target</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section>
        <section><h3>Equivalence warning</h3><p>${escapeHtml(audit.equivalence_warning || audit.novelty_boundary || attempt.claim_boundary || "")}</p></section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket80LeastCounterexampleCompactnessNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.least_counterexample_compactness_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const finite = machine.finite_witnesses || {};
  const dual = machine.dual_topology_escape || {};
  const criterion = audit.positive_integer_cylinder_stabilization_criterion || {};
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const finiteSamples = Array.isArray(finite.samples) ? finite.samples.slice(0, 12) : [];
  const dualSamples = Array.isArray(dual.samples) ? dual.samples : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["maximum audited horizon", finite.max_horizon],
        ["lower-bound regimes", finite.lower_bound_count],
        ["finite witness cases", finite.finite_witness_case_count],
        ["accelerated step replays", finite.accelerated_step_replay_count],
        ["finite witness failures", finite.finite_witness_failure_count],
        ["2-adic compactness limit", dual.two_adic_limit],
        ["dual-topology failures", dual.dual_topology_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket80_transfer || attempt.route || "missing"]];
  const finiteRows = finiteSamples.map((row) => [row.bound_name, row.horizon, row.start, row.terminal, row.all_prefix_iterates_strictly_above_start]);
  const dualRows = dualSamples.map((row) => [row.horizon, row.positive_integer, row.archimedean_lower_bound, row.two_adic_precision_to_minus_one]);
  const rejectedRows = rejected.map((row) => [row.family, statusText(row.status), row.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77 poc-ticket78 poc-ticket79 poc-ticket80">
      <h3>Ticket 80 least-counterexample compactness no-go</h3>
      <div class="poc-head">
        <div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div>
        <div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div>
        <div><span>Evidence scope</span><strong>${Object.keys(audit).length ? "exact finite-prefix no-go" : "method transfer only"}</strong></div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 임의의 깊이 H와 유한 하한 B 위에서 all-ones valuation cylinder가 최소반례의 유한 비감소 필요조건을 모두 만족합니다. 이 증인들은 실수 크기로 무한대로 이탈하면서 2진 위상에서는 양의 정수가 아닌 -1로 수렴하므로, finite prefix와 compactness만으로는 모순이나 양의 반례를 얻을 수 없습니다.</p>` : ""}
      ${table(["TICKET80 compactness no-go audit", "Value"], summaryRows)}
      ${finiteRows.length ? `<h3>Arbitrarily large finite non-descent witnesses</h3>${table(["lower bound", "H", "start n", "A^H(n)", "all prefixes > n"], finiteRows)}` : ""}
      ${dualRows.length ? `<h3>Dual-topology escape x_H → -1 in Z_2</h3>${table(["H", "x_H", "ordinary lower bound", "2-adic precision"], dualRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected finite-prefix and compactness routes</h3>${table(["family", "status", "exact counteredge"], rejectedRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section>
          <section><h3>Positive-integer stabilization criterion</h3><p>${escapeHtml(criterion.statement || "")}</p><p>${escapeHtml(criterion.ticket80_application || "")}</p></section>
        </div>
        <div class="poc-bridge">
          <section><h3>Literature boundary</h3>${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}</section>
          <section><h3>Equivalence warning</h3><p>${escapeHtml(audit.equivalence_warning || "")}</p></section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section>
        <section><h3>Retained route</h3><p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p></section>
      </div>
      <div class="poc-bridge">
        <section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section>
        <section><h3>Novelty boundary</h3><p>${escapeHtml(audit.novelty_boundary || attempt.claim_boundary || "")}</p></section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket81MersennePostCompensationNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.mersenne_post_compensation_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const exact = audit.exact_formula || {};
  const classification = audit.classification || {};
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const samples = Array.isArray(machine.samples) ? machine.samples.slice(0, 10) : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["family", audit.family],
        ["maximum audited exponent", machine.max_k],
        ["Mersenne starts", machine.mersenne_case_count],
        ["initial expansion replays", machine.initial_step_replay_count],
        ["post-compensation non-descents", machine.post_compensation_non_descent_count],
        ["descent exponents", (machine.descent_exception_k || []).join(", ")],
        ["total audit failures", machine.total_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket81_transfer || attempt.route || "missing"]];
  const sampleRows = samples.map((row) => [
    row.k,
    row.start,
    row.initial_valuation_one_steps,
    row.first_post_block_valuation,
    row.post_block_iterate,
    row.classification,
  ]);
  const exactRows = Object.entries(exact);
  const rejectedRows = rejected.map((row) => [row.family, statusText(row.status), row.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77 poc-ticket78 poc-ticket79 poc-ticket80 poc-ticket81">
      <h3>Ticket 81 Mersenne first-compensation no-go</h3>
      <div class="poc-head">
        <div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div>
        <div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div>
        <div><span>Evidence scope</span><strong>${Object.keys(audit).length ? "exact Mersenne-family no-go" : "method transfer only"}</strong></div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> N_k=2^k-1의 정확한 valuation-one 팽창 구간 뒤 첫 보상 단계를 완전히 분류했습니다. 하강은 k=2,4,8에서만 일어나고, 모든 홀수 k>=3과 모든 짝수 k>=10을 포함한 무한 계열에서는 일어나지 않습니다. 따라서 안정화된 양의 cylinder에서도 보상 한 번만으로 하강을 증명할 수 없습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 콜라츠의 메르센 식을 전이하지 않습니다. 한 번의 국소 보상으로 전역 결손을 해소했다고 가정하지 말라는 검증 규율만 적용합니다.</p>`}
      ${table(["TICKET81 Mersenne compensation audit", "Value"], summaryRows)}
      ${exactRows.length ? `<h3>Exact expansion and compensation formulas</h3>${table(["identity", "exact statement"], exactRows)}` : ""}
      ${sampleRows.length ? `<h3>Audited Mersenne samples</h3>${table(["k", "N_k", "v2=1 steps", "a_k", "A^k(N_k)", "classification"], sampleRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected single-compensation routes</h3>${table(["candidate family", "status", "exact counteredge"], rejectedRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section>
          <section><h3>Complete first-compensation classification</h3><p><strong>Descent:</strong> ${escapeHtml(classification.descent_exceptions || "")}</p>${list(classification.non_descent_infinite_families || [])}</section>
        </div>
        <div class="poc-bridge">
          <section><h3>Literature boundary</h3>${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}</section>
          <section><h3>Equivalence warning</h3><p>${escapeHtml(audit.equivalence_warning || "")}</p></section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section>
        <section><h3>Retained cumulative route</h3><p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p></section>
      </div>
      <div class="poc-bridge">
        <section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section>
        <section><h3>Novelty boundary</h3><p>${escapeHtml(audit.novelty_boundary || attempt.claim_boundary || "")}</p></section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket82FixedMersenneWindowNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.fixed_mersenne_compensation_window_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const symbolic = audit.exact_symbolic_family || {};
  const progressions = audit.explicit_progressions || {};
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const samples = Array.isArray(machine.samples) ? machine.samples : [];
  const summaryRows = Object.keys(audit).length
    ? [
        ["source ticket", audit.source_ticket],
        ["maximum audited horizon", machine.max_horizon],
        ["horizon cases", machine.horizon_case_count],
        ["symbolic states", machine.symbolic_state_count],
        ["transition conditions", machine.transition_condition_count],
        ["audit failures", machine.total_failure_count],
        ["next theorem target", audit.next_theorem_target],
      ]
    : [["transfer route", bounded.ticket82_transfer || attempt.route || "missing"]];
  const sampleRows = samples.map((row) => [
    row.horizon,
    (row.post_reference_word_prefix || []).join(","),
    row.required_precision_bits,
    `2^${row.progression_period_log2}`,
    row.dominance_threshold,
    row.first_certified_progression_exponent,
  ]);
  const rejectedRows = rejected.map((row) => [row.family, statusText(row.status), row.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket45 poc-ticket58 poc-ticket59 poc-ticket60 poc-ticket61 poc-ticket62 poc-ticket63 poc-ticket64 poc-ticket65 poc-ticket66 poc-ticket67 poc-ticket68 poc-ticket69 poc-ticket70 poc-ticket71 poc-ticket72 poc-ticket73 poc-ticket74 poc-ticket75 poc-ticket76 poc-ticket77 poc-ticket78 poc-ticket79 poc-ticket80 poc-ticket81 poc-ticket82">
      <h3>Ticket 82 fixed Mersenne compensation-window no-go</h3>
      <div class="poc-head">
        <div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div>
        <div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div>
        <div><span>Evidence scope</span><strong>${Object.keys(audit).length ? "all fixed horizons, Mersenne only" : "method transfer only"}</strong></div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 임의의 고정 H에 대해 첫 보상 이후 H단계 동안 시작값보다 큰 메르센 시작값이 무한히 많습니다. 합동류는 H>=2에서 k=3 mod 2^(2H+3)로 명시됩니다. 이는 유한 지연이 무한히 커진다는 정리이며 발산을 뜻하지 않습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 메르센 합동류 정리를 전이하지 않습니다. 고정된 국소 관찰 창을 전역 정리로 승격하지 말라는 검증 규율만 적용합니다.</p>`}
      ${table(["TICKET82 fixed-window no-go audit", "Value"], summaryRows)}
      ${Object.keys(symbolic).length ? `<h3>Exact symbolic exponent family</h3>${table(["identity", "statement"], Object.entries(symbolic))}` : ""}
      ${Object.keys(progressions).length ? `<h3>Explicit exponent progressions</h3>${table(["range", "progression or reason"], Object.entries(progressions))}` : ""}
      ${sampleRows.length ? `<h3>Symbolic horizon certificates</h3>${table(["H", "word prefix", "Q bits", "period", "growth threshold", "first certified k"], sampleRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected constant-window routes</h3>${table(["candidate family", "status", "exact counteredge"], rejectedRows)}` : ""}
      ${Object.keys(audit).length ? `
        <div class="poc-bridge">
          <section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section>
          <section><h3>Unbounded-delay theorem</h3><p>${escapeHtml(audit.statement || "")}</p><p>Modular exponentiation audits exact valuation prefixes; Archimedean growth proves eventual dominance. The large exponents are symbolic certificates, not materialized trajectories.</p></section>
        </div>
        <div class="poc-bridge">
          <section><h3>Literature boundary</h3>${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}</section>
          <section><h3>Equivalence warning</h3><p>${escapeHtml(audit.equivalence_warning || "")}</p></section>
        </div>
      ` : ""}
      <div class="poc-bridge">
        <section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section>
        <section><h3>Retained growing-window route</h3><p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p></section>
      </div>
      <div class="poc-bridge">
        <section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section>
        <section><h3>Novelty boundary</h3><p>${escapeHtml(audit.novelty_boundary || attempt.claim_boundary || "")}</p></section>
      </div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket83MersenneLogWindowLowerBound(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.mersenne_log_window_lower_bound_audit || {};
  const machine = audit.machine_audit || {};
  const samples = Array.isArray(machine.samples) ? machine.samples : [];
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const literature = Array.isArray(audit.literature_context) ? audit.literature_context : [];
  const summaryRows = Object.keys(audit).length ? [
    ["explicit sequence", audit.explicit_sequence], ["maximum audited horizon", machine.max_horizon],
    ["horizon cases", machine.horizon_case_count], ["symbolic states", machine.symbolic_state_count],
    ["audit failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket83_transfer || attempt.route || "missing"]];
  const sampleRows = samples.map((row) => [row.horizon, row.explicit_exponent, row.post_descent_delay_strict_lower_bound, row.maximum_denominator_power, row.logarithmic_lower_bound]);
  const rejectedRows = rejected.map((row) => [row.family, statusText(row.status), row.counteredge]);
  return `
    <div class="poc-ticket17 poc-ticket81 poc-ticket82 poc-ticket83">
      <h3>Ticket 83 Mersenne half-log delay lower bound</h3>
      <div class="poc-head">
        <div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div>
        <div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div>
        <div><span>Evidence scope</span><strong>${Object.keys(audit).length ? "exact Mersenne subsequence bound" : "method transfer only"}</strong></div>
      </div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> k_H=3+2^(2H+3)에서 D(k_H)>H>(1/2)log2(k_H)-2를 증명했습니다. 따라서 o(log k) 창과 계수 1/2 미만의 로그 창은 무한히 실패합니다. 이는 발산이 아니라 유한 하강 지연의 하한입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 메르센 하한을 전이하지 않고, 필요한 전역 스케일을 먼저 정량화하라는 검증 규율만 적용합니다.</p>`}
      ${table(["TICKET83 logarithmic delay audit", "Value"], summaryRows)}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact half-log theorem</h3><p>${escapeHtml(audit.delay_definition || "")}</p><p>${escapeHtml(audit.statement || "")}</p></section><section><h3>Proof chain</h3>${list(audit.proof_chain || [])}</section></div>` : ""}
      ${sampleRows.length ? `<h3>Explicit delayed exponent sequence</h3>${table(["H", "k_H", "D(k_H) lower", "max d_t", "log bound"], sampleRows)}` : ""}
      ${rejectedRows.length ? `<h3>Rejected sub-half-log window routes</h3>${table(["candidate", "status", "counteredge"], rejectedRows)}` : ""}
      <div class="poc-bridge"><section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section><section><h3>Retained logarithmic-scale route</h3><p>${escapeHtml(audit.retained_route || attempt.candidate_theorem || "")}</p></section></div>
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Literature boundary</h3>${literature.map((item) => `<p><a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(item.citation || "source")}</a><br />${escapeHtml(item.role || "")}</p>`).join("")}</section><section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || "")}</p><p>${escapeHtml(audit.equivalence_warning || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket84TwoAdicCycleLogDelay(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.two_adic_cycle_log_delay_audit || {};
  const machine = audit.machine_audit || {};
  const cycle = audit.two_adic_cycle || {};
  const samples = Array.isArray(machine.samples) ? machine.samples : [];
  const rejected = Array.isArray(audit.rejected_candidate_families) ? audit.rejected_candidate_families : [];
  const rows = Object.keys(audit).length ? [
    ["cycle", cycle.cycle], ["valuation word", cycle.valuation_word], ["mean valuation", cycle.average_valuation],
    ["horizon cases", machine.horizon_case_count], ["maximum Hensel precision", machine.maximum_precision],
    ["symbolic states", machine.symbolic_state_count], ["failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket84_transfer || attempt.route || "missing"]];
  const sampleRows = samples.map((row) => [row.horizon, row.precision, row.residue, row.exponent, row.logarithmic_lower_bound]);
  return `
    <div class="poc-ticket17 poc-ticket82 poc-ticket83 poc-ticket84">
      <h3>Ticket 84 accessible 2-adic cycle and two-thirds log bound</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "positive finite-prefix lifts only" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 3^kappa=-13에서 얻는 음의 2진 주기 -7↔-5는 자연수 반례가 아닙니다. 유한 valuation 접두만 양의 지수로 lift하여 D(k_H)>H>(2/3)log2(k_H)-1을 증명합니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 콜라츠 주기를 전이하지 않고 completion 객체와 실제 반례를 구분하는 규율만 적용합니다.</p>`}
      ${table(["TICKET84 two-adic cycle audit", "Value"], rows)}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Accessible completion cycle</h3>${table(["field", "value"], Object.entries(cycle))}</section><section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section></div>` : ""}
      ${sampleRows.length ? `<h3>Positive Hensel-lifted exponent certificates</h3>${table(["H", "Q bits", "r_H", "k_H", "delay bound"], sampleRows)}` : ""}
      ${rejected.length ? `<h3>Rejected coefficient and ghost routes</h3>${table(["candidate", "status", "counteredge"], rejected.map((row) => [row.family, statusText(row.status), row.counteredge]))}` : ""}
      <div class="poc-bridge"><section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section><section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section></div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket85AccessibleCycleSupremum(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.accessible_cycle_supremum_audit || {};
  const machine = audit.machine_audit || {};
  const family = audit.cycle_family || {};
  const samples = Array.isArray(machine.samples) ? machine.samples : [];
  const rows = Object.keys(audit).length ? [["cases", machine.horizon_case_count], ["Hensel lifts", machine.hensel_lift_count], ["maximum precision", machine.maximum_precision], ["symbolic states", machine.symbolic_state_count], ["failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target]] : [["transfer route", bounded.ticket85_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket83 poc-ticket84 poc-ticket85">
      <h3>Ticket 85 accessible cycle coefficient supremum</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "exact cycle-family optimization" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> w_m=(2,1,...,1)의 계수 m/(m+1)가 1에 접근하고 모든 valuation은 1 이상이므로 supremum은 정확히 1입니다. all-ones cycle -1은 exponent image 밖이어서 달성되지 않습니다. 양의 lift는 D(k_H)>log2(k_H)-2를 만족합니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 Collatz cycle을 전이하지 않고 admissible family를 먼저 증명하라는 규율만 적용합니다.</p>`}
      ${table(["TICKET85 cycle supremum audit", "Value"], rows)}
      ${Object.keys(family).length ? `<div class="poc-bridge"><section><h3>Exact accessible cycle family</h3>${table(["field", "formula"], Object.entries(family))}</section><section><h3>Supremum one, not attained</h3><p>${escapeHtml(audit.supremum_statement || "")}</p><p>${escapeHtml(audit.delay_statement || "")}</p></section></div>` : ""}
      ${samples.length ? `<h3>Coefficient-one-minus-two lift certificates</h3>${table(["H", "mean", "reciprocal", "Q", "k_H", "bound"], samples.map((row) => [row.horizon, row.mean_valuation, row.reciprocal_mean, row.precision, row.exponent, row.logarithmic_lower_bound]))}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Rejected boundary routes</h3>${table(["candidate", "status", "counteredge"], (audit.rejected_candidate_families || []).map((row) => [row.family, statusText(row.status), row.counteredge]))}</section></div>` : ""}
      <div class="poc-bridge"><section><h3>Discarded route</h3><p>${escapeHtml(audit.discarded_route || attempt.obstruction || "")}</p></section><section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || attempt.candidate_theorem || "")}</p></section></div>
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket86CoefficientOneBoundary(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.coefficient_one_boundary_audit || {};
  const machine = audit.machine_audit || {};
  const reduction = audit.exact_reduction || {};
  const samples = Array.isArray(machine.samples) ? machine.samples : [];
  const rows = Object.keys(audit).length ? [
    ["nested prefixes", machine.prefix_case_count], ["top-bit heights", machine.top_bit_case_count],
    ["zero-bit heights", machine.zero_bit_case_count], ["longest observed zero run", machine.longest_observed_zero_run],
    ["maximum precision", machine.maximum_precision], ["symbolic states", machine.symbolic_state_count],
    ["failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket86_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket84 poc-ticket85 poc-ticket86">
      <h3>Ticket 86 infinite coefficient-one Mersenne delay</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "infinite restricted subsequence" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 주기점 목표를 3^(r_H+1)=-7 (mod 2^(H+3))로 정확히 환원합니다. 잉여류의 새 최상위 비트는 무한히 추가되며, 그 높이에서는 추가 주기 없이 k=r_H를 사용해 D(k)>log2(k)를 얻습니다. 이는 유한 하강 지연 정리이지 발산 궤도나 콜라츠 해결이 아닙니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 콜라츠 결론을 옮기지 않고 중첩 증인이 무한히 갱신됨을 별도로 증명하는 규율만 전이합니다.</p>`}
      ${table(["TICKET86 coefficient-one boundary audit", "Value"], rows)}
      ${Object.keys(reduction).length ? `<div class="poc-bridge"><section><h3>Exact fixed-log reduction</h3>${table(["field", "identity"], Object.entries(reduction))}</section><section><h3>Infinite top-bit theorem</h3><p>${escapeHtml(audit.infinite_jump_lemma || "")}</p><p>${escapeHtml(audit.delay_statement || "")}</p></section></div>` : ""}
      ${samples.length ? `<h3>Nested residue prefix samples</h3>${table(["H", "bits", "top bit", "zero run", "Q"], samples.map((row) => [row.horizon, row.residue_bit_length, row.top_bit_added ? "added" : "unchanged", row.zero_run_length, row.precision]))}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Remaining additive boundary</h3><p>${escapeHtml(audit.candidate_theorem || "")}</p><p>${escapeHtml(audit.discarded_route || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket87TwoAdicDigitRunBoundary(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.two_adic_digit_run_audit || {};
  const machine = audit.machine_audit || {};
  const fixed = audit.fixed_two_adic_exponent || {};
  const records = Array.isArray(machine.record_runs) ? machine.record_runs : [];
  const rows = Object.keys(audit).length ? [
    ["audited prefix bits", machine.prefix_bit_count], ["top-bit positions", machine.top_bit_count],
    ["zero-bit positions", machine.zero_bit_count], ["positive zero runs", machine.positive_zero_run_count],
    ["longest observed run", machine.longest_observed_zero_run], ["Hensel cross-check", machine.hensel_crosscheck_horizon],
    ["failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket87_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket85 poc-ticket86 poc-ticket87">
      <h3>Ticket 87 two-adic digit runs and additive-one delay</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "infinite additive-one subsequence" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 고정 2-adic 지수에는 0과 1이 모두 무한히 나타나므로 1→0 전환도 무한합니다. 각 전환에서 같은 양의 지수의 정확한 접두가 한 단계 연장되어 D(k)&gt;log2(k)+1을 만족하는 k가 무한히 존재합니다. 길이 16의 관측 기록은 유한 인증서일 뿐 unbounded run 증명이 아닙니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 두 extension symbol의 무한 재등장을 먼저 증명하는 규율만 전이하며 Collatz 결과를 옮기지 않습니다.</p>`}
      ${table(["TICKET87 digit-run boundary audit", "Value"], rows)}
      ${Object.keys(fixed).length ? `<div class="poc-bridge"><section><h3>Fixed two-adic logarithm</h3>${table(["field", "identity"], Object.entries(fixed))}</section><section><h3>Two-sided digit infinitude</h3><p>${escapeHtml(audit.infinite_digit_lemma || "")}</p><p>${escapeHtml(audit.delay_statement || "")}</p></section></div>` : ""}
      ${records.length ? `<h3>Finite zero-run record certificates</h3>${table(["H", "next H", "zero run", "valuation", "k bits", "delay excess"], records.map((row) => [row.start_horizon, row.next_top_bit_horizon, row.zero_run_length, row.exact_valuation, row.exponent_bit_length, `>${row.strict_additive_delay_excess}`]))}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Rejected finite inference</h3><p>${escapeHtml(audit.discarded_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket88RunLengthTwoNoGo(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.run_length_two_no_go_audit || {};
  const machine = audit.machine_audit || {};
  const countermodel = audit.logical_countermodel || {};
  const complement = audit.complement_route_audit || {};
  const discarded = Array.isArray(audit.discarded_routes) ? audit.discarded_routes : [];
  const rows = Object.keys(audit).length ? [
    ["countermodel bits", machine.countermodel_horizon], ["countermodel zeros", machine.countermodel_zero_count],
    ["adjacent zeros", machine.countermodel_adjacent_zero_count], ["complement precision", machine.complement_horizon],
    ["observed runs >=2", machine.observed_run_length_two_or_more_count], ["failures", machine.total_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket88_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket86 poc-ticket87 poc-ticket88">
      <h3>Ticket 88 run-length-two inference no-go</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "proof-route no-go" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 0과 1이 모두 무한하다는 사실만으로 00의 무한 반복은 나오지 않습니다. 제곱수 위치만 0인 비주기적 반모형에는 00이 전혀 없습니다. 비트 보수 s=-r도 검사했지만 valuation 주기가 (1,3), 평균 2로 퇴화해 계수 1 구조를 보존하지 못합니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 반복 symbol 승격 전에 symbolic countermodel과 dual-strength 보존을 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET88 run-length-two no-go audit", "Value"], rows)}
      ${Object.keys(countermodel).length ? `<div class="poc-bridge"><section><h3>Explicit no-00 countermodel</h3>${table(["field", "value"], Object.entries(countermodel))}</section><section><h3>Exact complement orbit</h3>${table(["field", "value"], Object.entries(complement).filter(([key]) => !key.endsWith("failure_count")))}</section></div>` : ""}
      ${discarded.length ? `<h3>Discarded promotion routes</h3>${table(["route", "status", "counteredge"], discarded.map((row) => [row.route, statusText(row.status), row.counteredge]))}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact no-go proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Target-specific remaining bridge</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket89FixedLogGoldenMeanReduction(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.fixed_log_golden_mean_reduction_audit || {};
  const machine = audit.machine_audit || {};
  const equivalence = audit.exact_equivalence || {};
  const transcendence = audit.transcendence_no_go || {};
  const discarded = Array.isArray(audit.discarded_routes) ? audit.discarded_routes : [];
  const rows = Object.keys(audit).length ? [
    ["maximum horizon", machine.max_horizon], ["top-bit positions", machine.top_bit_count],
    ["complete jump pairs", machine.complete_jump_pair_count], ["excess >=5", machine.valuation_excess_at_least_five_count],
    ["maximum excess", machine.maximum_valuation_excess], ["direct check", machine.direct_check_horizon],
    ["failures", machine.total_failure_count], ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket89_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket87 poc-ticket88 poc-ticket89">
      <h3>Ticket 89 fixed-log golden-mean valuation reduction</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "exact symbolic-to-arithmetic reduction" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 100 패턴의 무한 반복을 정확히 v2(3^(k+1)+7)≥floor(log2(k))+5 사건의 무한 반복으로 환원했습니다. no-00 subshift에는 초월적 2-adic 수도 비가산개 존재하므로 초월성만으로는 배제할 수 없습니다. 다음 의무는 특정 지수 부분수열의 valuation 초과량 5 재발 정리입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 symbolic 반복을 target-specific arithmetic threshold로 먼저 바꾸는 규율만 전이합니다.</p>`}
      ${table(["TICKET89 fixed-log reduction audit", "Value"], rows)}
      ${Object.keys(equivalence).length ? `<div class="poc-bridge"><section><h3>Exact pattern-valuation equivalence</h3>${table(["field", "identity"], Object.entries(equivalence))}</section><section><h3>Transcendence no-go</h3>${table(["field", "statement"], Object.entries(transcendence))}</section></div>` : ""}
      ${discarded.length ? `<h3>Discarded generic proof routes</h3>${table(["route", "status", "counteredge"], discarded.map((row) => [row.route, statusText(row.status), row.counteredge]))}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact reduction proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Contrapositive valuation cap</h3><p>${escapeHtml(audit.contrapositive_target || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket90NormalizedErrorGhostLasso(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.normalized_error_ghost_lasso_audit || {};
  const machine = audit.machine_audit || {};
  const error = audit.normalized_error || {};
  const limit = audit.correction_limit || {};
  const ghost = audit.limiting_ghost || {};
  const rows = Object.keys(audit).length ? [
    ["audited transitions", machine.audited_transition_count], ["error bits", machine.error_bits],
    ["lasso precisions", machine.lasso_precision_count], ["maximum precision", machine.maximum_lasso_precision],
    ["beta low 20", machine.beta_low_20], ["failures", machine.total_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket90_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket88 poc-ticket89 poc-ticket90">
      <h3>Ticket 90 normalized-error ghost lasso no-go</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "fixed-precision proof-route no-go" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 정규화 오차 e_H의 lift recurrence와 보정항 극한 beta를 정확히 유도했습니다. limiting map에는 e=beta라는 홀수 fixed point가 있어 모든 고정 정밀도 automaton에 목표 e=0 mod 4를 회피하는 lasso가 남습니다. 이는 실제 궤도 반례가 아니라 fixed-state 증명 전략의 반모형입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 normalized limiting map의 ghost lasso를 먼저 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET90 normalized-error audit", "Value"], rows)}
      ${Object.keys(error).length ? `<div class="poc-bridge"><section><h3>Exact normalized-error recurrence</h3>${table(["field", "identity"], Object.entries(error))}</section><section><h3>Correction limit</h3>${table(["field", "identity"], Object.entries(limit))}</section></div>` : ""}
      ${Object.keys(ghost).length ? `<div class="poc-bridge"><section><h3>Limiting ghost fixed point</h3>${table(["field", "statement"], Object.entries(ghost))}</section><section><h3>Growing-precision requirement</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      ${Object.keys(audit).length ? `<h3>Exact no-go proof chain</h3>${list(audit.proof_chain || [])}` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket91ErrorTailInvariantSet(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.error_tail_invariant_set_audit || {};
  const machine = audit.machine_audit || {};
  const identity = audit.exact_tail_identity || {};
  const conjugacy = audit.limiting_conjugacy || {};
  const obstruction = audit.golden_mean_obstruction || {};
  const discarded = Array.isArray(audit.discarded_routes) ? audit.discarded_routes : [];
  const rows = Object.keys(audit).length ? [
    ["audited horizons", machine.audited_horizon_count], ["tail transitions", machine.audited_tail_transition_count],
    ["conjugacy states", machine.conjugacy_state_count], ["no-00 words", machine.golden_mean_word_count],
    ["distinct images", machine.golden_mean_image_count], ["failures", machine.total_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket91_transfer || attempt.route || "missing"]];
  return `
    <div class="poc-ticket17 poc-ticket89 poc-ticket90 poc-ticket91">
      <h3>Ticket 91 error-tail conjugacy and invariant-set correction</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "exact coordinate theorem and route no-go" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 정규화 오차는 높이 H+2 비트까지 미래 지수 꼬리에 홀수 단위 gamma를 곱한 값과 같습니다. beta 고정점은 미래 비트가 모두 1인 꼬리 하나일 뿐입니다. 실제 장애물은 00을 피하는 모든 꼬리의 황금평균 불변집합이므로, 다음 목표를 단일 ghost 분리에서 전체 불변집합의 무한 탈출로 교정했습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 단일 극한 상태가 아니라 목표를 회피하는 전체 불변집합을 먼저 찾는 검증 규율만 전이합니다.</p>`}
      ${table(["TICKET91 tail-coordinate audit", "Value"], rows)}
      ${Object.keys(identity).length ? `<div class="poc-bridge"><section><h3>Exact growing-precision identity</h3>${table(["field", "identity"], Object.entries(identity))}</section><section><h3>Binary-shift conjugacy</h3>${table(["field", "statement"], Object.entries(conjugacy))}</section></div>` : ""}
      ${Object.keys(obstruction).length ? `<div class="poc-bridge"><section><h3>Full golden-mean obstruction</h3>${table(["field", "statement"], Object.entries(obstruction))}</section><section><h3>Corrected theorem target</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      ${discarded.length ? `<h3>Discarded incomplete routes</h3>${table(["route", "status", "counteredge"], discarded.map((row) => [row.route, statusText(row.status), row.counteredge]))}` : ""}
      ${Object.keys(audit).length ? `<h3>Exact correction proof chain</h3>${list(audit.proof_chain || [])}` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket92ScaleSensitiveThreshold(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const collatz = bounded.second_order_defect_audit || {};
  const twin = bounded.maynard_threshold_correction || {};
  const audit = Object.keys(collatz).length ? collatz : twin;
  const machine = audit.machine_audit || {};
  const coordinate = collatz.exact_second_order_coordinate || {};
  const scaleNoGo = collatz.first_order_scale_no_go || {};
  const criterion = twin.criterion || {};
  const discarded = Array.isArray(audit.discarded_routes) ? audit.discarded_routes : [];
  let rows;
  if (Object.keys(collatz).length) {
    rows = [
      ["maximum horizon", machine.max_horizon], ["jump pairs", machine.complete_jump_pair_count],
      ["Delta >=3 events", machine.second_order_target_event_count], ["maximum Delta", machine.maximum_floor_defect],
      ["countermodel bits", machine.countermodel_bits], ["failures", machine.total_failure_count],
      ["next theorem", collatz.next_theorem_target],
    ];
  } else if (Object.keys(twin).length) {
    rows = [
      ["corrected rows", machine.corrected_row_count], ["legacy false gap promotions", machine.legacy_false_gap_promotion_count],
      ["certified M_k rows", machine.certified_M_k_row_count], ["certified two-prime rows", machine.certified_two_prime_row_count],
      ["remaining implied gaps", machine.remaining_implied_gap_count], ["failures", machine.total_failure_count],
      ["next theorem", twin.next_theorem_target],
    ];
  } else {
    rows = [["transfer route", bounded.ticket92_transfer || attempt.route || "missing"]];
  }
  return `
    <div class="poc-ticket17 poc-ticket90 poc-ticket91 poc-ticket92">
      <h3>Ticket 92 scale-sensitive threshold audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(collatz).length ? "exact second-order coordinate" : Object.keys(twin).length ? "primary-source threshold correction" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(collatz).length ? `<p><strong>한국어 해설:</strong> 00 두 비트는 정규화 근사 지수에서 O(1/H)로 사라집니다. 따라서 H로 나누기 전의 상수항 Delta_H를 보존해야 하며, 목표는 정확히 Delta_H>=3의 무한 재발입니다. 표준 1차 무리수 지수와 상한형 선형형식은 이 목표를 강제하지 못합니다.</p>` : Object.keys(twin).length ? `<p><strong>한국어 해설:</strong> 기존 TP-TICKET-14의 2/k 임계값은 Maynard 판정식이 아니었습니다. 무조건적 theta<1/2에서 두 소수를 얻으려면 검증된 M_k>4가 필요합니다. 기존 점수 17개는 M_k 인증이 아니므로 gap 2를 포함한 모든 implied gap 승격을 제거했습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 목표 사건이 정규화 과정에서 소실되지 않는지 먼저 확인하는 규율만 전이합니다.</p>`}
      ${table(["TICKET92 threshold audit", "Value"], rows)}
      ${Object.keys(coordinate).length ? `<div class="poc-bridge"><section><h3>Second-order p-adic defect</h3>${table(["field", "identity"], Object.entries(coordinate))}</section><section><h3>First-order scale no-go</h3>${table(["field", "statement"], Object.entries(scaleNoGo))}</section></div>` : ""}
      ${Object.keys(criterion).length ? `<div class="poc-bridge"><section><h3>Correct Maynard criterion</h3>${table(["field", "statement"], Object.entries(criterion))}</section><section><h3>Removed false promotion</h3><p>${escapeHtml(twin.discarded_route || "")}</p><p>${escapeHtml(twin.retained_route || "")}</p></section></div>` : ""}
      ${discarded.length ? `<h3>Discarded target-erasing routes</h3>${table(["route", "status", "counteredge"], discarded.map((row) => [row.route, statusText(row.status), row.counteredge]))}` : ""}
      ${Object.keys(collatz).length ? `<h3>Exact scale audit proof chain</h3>${list(collatz.proof_chain || [])}` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket93TwinCorrelationExcess(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_correlation_excess_audit || {};
  const machine = audit.machine_audit || {};
  const bridge = audit.exact_correlation_bridge || {};
  const surrogate = audit.surrogate_no_go || {};
  const typeII = audit.type_ii_boundary || {};
  const rows = Object.keys(audit).length ? [
    ["correlation limit", machine.correlation_limit], ["Lambda correlation", Number(machine.final_lambda_correlation || 0).toFixed(2)],
    ["twin pairs", machine.final_twin_pair_count], ["proper-power pairs", machine.final_proper_prime_power_pair_count],
    ["prime-power contamination", Number(machine.final_contamination || 0).toFixed(2)], ["safe excess", Number(machine.final_correlation_minus_bound || 0).toFixed(2)],
    ["surrogate truncations", machine.truncation_count], ["failures", machine.total_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [["transfer route", bounded.ticket93_transfer || attempt.route || "missing"]];
  const surrogateRows = Array.isArray(surrogate.rows) ? surrogate.rows.map((row) => [
    row.truncation, row.pointwise_minorant_violation_count, row.pair_false_positive_count,
    Number(row.surrogate_to_exact_ratio || 0).toFixed(3), statusText(row.positive_surrogate_is_not_lower_bound),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket91 poc-ticket92 poc-ticket93">
      <h3>Ticket 93 exact twin-correlation excess bridge</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(audit).length ? "exact sufficiency bridge and surrogate no-go" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> Lambda(n)Lambda(n+2) 상관합에서 proper prime power 오염을 명시적으로 상계했습니다. 상관합이 이 상계를 무한히 크게 넘으면 쌍둥이 소수가 무한하다는 충분조건은 증명했지만, 그 excess 자체는 아직 증명하지 못했습니다. 절단 divisor surrogate 네 개는 모두 수만 개의 false-positive pair를 만들었으므로 양수라는 이유만으로 실제 하한이 될 수 없습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 정확한 목표 상관과 희소 오염을 분리하고, surrogate가 실제 하한인지 반례로 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET93 exact-correlation audit", "Value"], rows)}
      ${Object.keys(bridge).length ? `<div class="poc-bridge"><section><h3>Prime-power contamination bridge</h3>${table(["field", "statement"], Object.entries(bridge))}</section><section><h3>Signed Type II boundary</h3>${table(["field", "statement"], Object.entries(typeII))}</section></div>` : ""}
      ${surrogateRows.length ? `<h3>Truncated-divisor counterexamples</h3>${table(["R", "minorant violations", "false-positive pairs", "surrogate / exact", "route blocked"], surrogateRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact sufficiency proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Remaining correlation theorem</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket94SignedRemainderAndGoldbach(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const twin = bounded.twin_signed_remainder_audit || {};
  const goldbach = bounded.goldbach_correlation_bridge_audit || {};
  const audit = Object.keys(twin).length ? twin : goldbach;
  const machine = audit.machine_audit || {};
  const decomposition = twin.exact_decomposition || {};
  const normNoGo = twin.norm_only_no_go || {};
  const goldbachBridge = goldbach.exact_bridge || {};
  let rows;
  if (Object.keys(twin).length) {
    rows = [
      ["audit limit", machine.limit], ["truncations", machine.truncation_count],
      ["exact correlation", Number(machine.exact_correlation || 0).toFixed(2)], ["positive norm lower bounds", machine.positive_norm_lower_bound_count],
      ["decomposition failures", machine.decomposition_failure_count], ["failures", machine.total_failure_count],
      ["next theorem", twin.next_theorem_target],
    ];
  } else if (Object.keys(goldbach).length) {
    rows = [
      ["checkpoints", machine.checkpoint_count], ["maximum N", machine.maximum_checkpoint],
      ["positive certified margins", machine.positive_certified_margin_count], ["decomposition failures", machine.decomposition_failure_count],
      ["failures", machine.total_failure_count], ["next theorem", goldbach.next_theorem_target],
    ];
  } else {
    rows = [["transfer route", bounded.ticket94_transfer || attempt.route || "missing"]];
  }
  const twinRows = Array.isArray(machine.rows) && Object.keys(twin).length ? machine.rows.map((row) => [
    row.truncation, Number(row.least_squares_alpha || 0).toFixed(4), Number(row.surrogate_main_term || 0).toFixed(1),
    Number(row.combined_signed_remainder || 0).toFixed(1), Number(row.norm_only_lower_bound || 0).toFixed(1),
  ]) : [];
  const goldbachRows = Array.isArray(machine.rows) && Object.keys(goldbach).length ? machine.rows.map((row) => [
    row.even_target, Number(row.lambda_additive_correlation || 0).toFixed(1), row.ordered_prime_pair_count,
    row.ordered_proper_power_pair_count, Number(row.certified_margin || 0).toFixed(1),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket92 poc-ticket93 poc-ticket94">
      <h3>Ticket 94 signed-remainder and Goldbach bridge</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(twin).length ? "Twin signed-remainder no-go" : Object.keys(goldbach).length ? "Goldbach exact sufficiency bridge" : "method transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(twin).length ? `<p><strong>한국어 해설:</strong> Lambda=alpha Lambda_R+E의 shift-2 상관을 네 항으로 정확히 분해했습니다. 네 truncation 모두 exact reconstruction은 통과했지만 residual 항을 각각 Cauchy bound로 누른 하한은 음수였습니다. 다음 정리는 세 residual 항의 합을 하나의 signed Type II 객체로 제어해야 합니다.</p>` : Object.keys(goldbach).length ? `<p><strong>한국어 해설:</strong> 짝수 N의 additive Lambda correlation에서 proper prime power 오염을 분리했습니다. correlation이 명시적 오염 상계를 넘으면 Goldbach 표현이 존재하지만, 네 finite checkpoint의 안전 margin은 모두 음수여서 uniform theorem은 아직 열려 있습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 residual의 크기만이 아니라 결합된 부호를 보존하는 검증 규율만 전이합니다.</p>`}
      ${table(["TICKET94 signed-budget audit", "Value"], rows)}
      ${Object.keys(decomposition).length ? `<div class="poc-bridge"><section><h3>Exact signed decomposition</h3>${table(["field", "identity"], Object.entries(decomposition))}</section><section><h3>Norm-only lower-bound no-go</h3>${table(["field", "statement"], Object.entries(normNoGo))}</section></div>` : ""}
      ${twinRows.length ? `<h3>Twin signed remainder budget</h3>${table(["R", "alpha", "surrogate main", "signed remainder", "norm-only lower"], twinRows)}` : ""}
      ${Object.keys(goldbachBridge).length ? `<h3>Goldbach prime-power contamination bridge</h3>${table(["field", "statement"], Object.entries(goldbachBridge))}` : ""}
      ${goldbachRows.length ? `<h3>Goldbach finite margins</h3>${table(["N", "Lambda correlation", "prime pairs", "proper-power pairs", "certified margin"], goldbachRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Proof chain</h3>${list(audit.proof_chain || [])}</section><section><h3>Remaining theorem</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket95SharpContaminationAndEquivalence(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const twin = bounded.twin_ticket95_audit || {};
  const goldbach = bounded.goldbach_sharp_budget_audit || {};
  const audit = Object.keys(twin).length ? twin : goldbach;
  const machine = audit.machine_audit || {};
  const sharp = audit.sharp_budget_theorem || {};
  const equivalence = twin.equivalence_no_reduction || {};
  const screen = machine.all_even_screen || {};
  let rows;
  if (Object.keys(twin).length) {
    rows = [
      ["checkpoints", machine.checkpoint_count], ["maximum x", machine.maximum_checkpoint],
      ["budget failures", machine.budget_failure_count], ["equivalence failures", machine.equivalence_failure_count],
      ["total failures", machine.total_failure_count], ["next theorem", twin.next_theorem_target],
    ];
  } else if (Object.keys(goldbach).length) {
    rows = [
      ["checkpoints", machine.checkpoint_count], ["maximum N", machine.maximum_checkpoint],
      ["positive sharp margins", machine.positive_sharp_margin_count], ["all-even screen", screen.screen_limit],
      ["nonpositive screen margins", screen.nonpositive_margin_count], ["observed positive suffix", screen.observed_positive_suffix_start],
      ["failures", machine.total_failure_count], ["next theorem", goldbach.next_theorem_target],
    ];
  } else {
    rows = [["transfer route", bounded.ticket95_transfer || attempt.route || "missing"]];
  }
  const budgetRows = Array.isArray(machine.checkpoint_rows) ? machine.checkpoint_rows.map((row) => [
    row.limit || row.even_target,
    Number(row.old_contamination_bound || 0).toFixed(1),
    Number(row.sharp_contamination_bound || 0).toFixed(1),
    Number(row.bound_improvement_factor || 0).toFixed(1),
    Number(row.sharp_certified_margin || 0).toFixed(1),
  ]) : [];
  const equivalenceRows = Array.isArray(machine.equivalence_rows) ? machine.equivalence_rows.map((row) => [
    row.truncation,
    Number(row.surrogate_main_term || 0).toFixed(1),
    Number(row.combined_signed_remainder || 0).toFixed(1),
    Number(row.original_correlation_excess || 0).toFixed(1),
    Number(row.target_equivalence_error || 0).toExponential(2),
  ]) : [];
  const screenRows = Array.isArray(screen.nonpositive_margin_rows) ? screen.nonpositive_margin_rows.map((row) => [
    row.even_target,
    Number(row.sharp_margin || 0).toFixed(3),
    Array.isArray(row.direct_goldbach_witness) ? row.direct_goldbach_witness.join(" + ") : "missing",
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket93 poc-ticket94 poc-ticket95">
      <h3>Ticket 95 sharp contamination and equivalence gate</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${Object.keys(twin).length ? "Twin sharp budget and no-reduction audit" : Object.keys(goldbach).length ? "Goldbach sharp budget and numerical screen" : "logical novelty transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(twin).length ? `<p><strong>한국어 해설:</strong> proper prime power의 실제 Lambda 질량 H를 사용해 오염 상계를 크게 줄였습니다. 동시에 D_R=C_2-alpha^2 S_R이므로 TICKET94의 D_R 목표는 원래 C_2 하한과 정확히 동치임을 확인했습니다. 유효한 재서술이지만 독립 추정 없이는 문제 축약이 아니므로 진전 등급을 낮췄습니다.</p>` : Object.keys(goldbach).length ? `<p><strong>한국어 해설:</strong> 지수별 sqrt(N) 개수 상계 대신 실제 proper-prime-power Lambda 질량을 사용했습니다. 백만 이하 전 짝수 화면에서 새 기준식의 비양수 margin은 38 이하 열 건뿐이며 모두 직접 Goldbach 증인이 있습니다. FFT 화면은 유한 수치 증거이지 무한 증명이 아닙니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 미해결 명제와 동치인 기호 재배열을 증명 진전으로 세지 않는 독립정보 검사를 전이합니다.</p>`}
      ${table(["TICKET95 logical-novelty audit", "Value"], rows)}
      ${Object.keys(sharp).length ? `<h3>Weighted proper-prime-power mass theorem</h3>${table(["field", "statement"], Object.entries(sharp))}` : ""}
      ${Object.keys(equivalence).length ? `<h3>Equivalence is not a reduction</h3>${table(["field", "statement"], Object.entries(equivalence))}` : ""}
      ${budgetRows.length ? `<h3>Sharp contamination budgets</h3>${table(["scale", "old bound", "sharp bound", "improvement x", "sharp margin"], budgetRows)}` : ""}
      ${equivalenceRows.length ? `<h3>Twin exact equivalence replay</h3>${table(["R", "surrogate main", "signed remainder", "original excess", "equivalence error"], equivalenceRows)}` : ""}
      ${Object.keys(screen).length ? `<div class="poc-bridge"><section><h3>Goldbach all-even numerical screen</h3>${table(["field", "value"], [["limit", screen.screen_limit], ["targets", screen.even_target_count], ["nonpositive margins", screen.nonpositive_margin_count], ["last nonpositive", screen.last_nonpositive_margin_target], ["positive suffix start", screen.observed_positive_suffix_start], ["FFT/direct max error", Number(screen.maximum_fft_direct_error || 0).toExponential(2)], ["proof status", screen.proof_status]])}</section><section><h3>Screen exceptions and direct witnesses</h3>${table(["N", "sharp margin", "prime witness"], screenRows)}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Retained independent route</h3><p>${escapeHtml(audit.retained_route || "")}</p></section><section><h3>Next theorem</h3><p>${escapeHtml(audit.candidate_theorem || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket96FourierPhaseInformation(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.fourier_phase_information_audit || {};
  const machine = audit.machine_audit || {};
  const bridges = audit.exact_fourier_bridges || {};
  const noGo = audit.information_no_go || {};
  const countermodels = audit.countermodel_audit || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const rows = Object.keys(audit).length ? [
    ["checkpoints", machine.checkpoint_count], ["maximum scale", machine.maximum_checkpoint],
    ["configurations per checkpoint", machine.configuration_count_per_checkpoint], ["sparse density ceiling", machine.sparse_mask_density_ceiling],
    ["Goldbach sparse certificates", machine.sparse_goldbach_certificate_count], ["Twin sparse certificates", machine.sparse_twin_certificate_count],
    ["reconstruction failures", machine.reconstruction_failure_count], ["failures", machine.total_failure_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [["transfer route", bounded.ticket96_transfer || attempt.route || "missing"]];
  const checkpointRows = Array.isArray(machine.checkpoint_rows) ? machine.checkpoint_rows.map((row) => {
    const best = isGoldbach ? row.best_sparse_goldbach_row : row.best_sparse_twin_row;
    return [
      row.target,
      row.transform_size,
      Number(isGoldbach ? row.goldbach_dft_error : row.twin_dft_error).toExponential(2),
      Number(isGoldbach ? row.exact_goldbach_correlation : row.exact_twin_correlation).toFixed(1),
      Number(isGoldbach ? row.goldbach_sharp_budget : row.twin_sharp_budget).toFixed(1),
      `${(Number(best?.major_density || 0) * 100).toFixed(2)}%`,
      Number(isGoldbach ? best?.goldbach_energy_only_lower_bound : best?.twin_energy_only_lower_bound).toFixed(1),
    ];
  }) : [];
  return `
    <div class="poc-ticket17 poc-ticket94 poc-ticket95 poc-ticket96">
      <h3>Ticket 96 Fourier phase-information audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "binary additive Fourier coefficient" : isTwin ? "shift-two Fourier coefficient" : "spectral gate transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 상관합을 zero-padded DFT 계수로 정확히 재구성한 뒤 낮은 분모 주파수 창과 minor 영역을 분리했습니다. 희소 major mask에서 minor의 signed contribution 대신 Parseval energy를 사용하면 하한이 모두 실패합니다. 이는 푸리에 방법 전체의 실패가 아니라 위상과 주파수 위치를 버린 전제의 정보 부족입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 크기나 에너지 자료를 유지한 채 필요한 부호를 뒤집는 spectral countermodel이 있는지 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET96 phase-information audit", "Value"], rows)}
      ${Object.keys(bridges).length ? `<div class="poc-bridge"><section><h3>Exact finite Fourier bridges</h3>${table(["field", "identity"], Object.entries(bridges))}</section><section><h3>Phase-blind information no-go</h3>${table(["field", "statement"], Object.entries(noGo))}</section></div>` : ""}
      ${Object.keys(countermodels).length ? `<h3>Adversarial spectral countermodel replay</h3>${table(["problem", "pair energy", "target coefficient", "envelope error"], ["goldbach", "twin"].map((problem) => [problem, Number(countermodels[problem]?.pair_energy || 0).toFixed(6), Number(countermodels[problem]?.target_coefficient || 0).toFixed(6), Number(countermodels[problem]?.negative_energy_envelope_error || 0).toExponential(2)]))}` : ""}
      ${checkpointRows.length ? `<h3>${isGoldbach ? "Goldbach" : "Twin"} sparse Farey-mask replay</h3>${table(["scale", "DFT size", "replay error", "exact correlation", "sharp budget", "best mask density", "energy-only lower"], checkpointRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded phase-blind routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained arithmetic route</h3><p>${escapeHtml(isGoldbach ? audit.retained_goldbach_route : audit.retained_twin_route)}</p><p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket97PeriodicProjectionResidual(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.periodic_projection_residual_audit || {};
  const machine = audit.machine_audit || {};
  const projection = audit.projection_theorem || {};
  const noGo = audit.fixed_modulus_no_go || {};
  const countermodel = audit.countermodel_audit || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const rows = Object.keys(audit).length ? [
    ["checkpoints", machine.checkpoint_count], ["maximum scale", machine.maximum_checkpoint],
    ["moduli", Array.isArray(machine.moduli) ? machine.moduli.join(", ") : "missing"],
    ["Goldbach certificates", machine.goldbach_certificate_count], ["Twin certificates", machine.twin_certificate_count],
    ["projection failures", machine.projection_failure_count], ["countermodel failures", machine.countermodel_failure_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [["transfer route", bounded.ticket97_transfer || attempt.route || "missing"]];
  const projectionRows = [];
  if (Array.isArray(machine.checkpoint_rows)) {
    machine.checkpoint_rows.forEach((checkpoint) => {
      (checkpoint.rows || []).forEach((row) => {
        projectionRows.push([
          checkpoint.target,
          row.modulus,
          Number(row.relative_residual_norm || 0).toFixed(3),
          Number(row.maximum_absolute_residue_residual_sum || 0).toExponential(2),
          Number(isGoldbach ? row.goldbach_periodic_main : row.twin_periodic_main).toFixed(1),
          Number(isGoldbach ? row.goldbach_signed_residual : row.twin_signed_residual).toFixed(1),
          Number(isGoldbach ? row.goldbach_norm_only_lower_bound : row.twin_norm_only_lower_bound).toFixed(1),
        ]);
      });
    });
  }
  return `
    <div class="poc-ticket17 poc-ticket95 poc-ticket96 poc-ticket97">
      <h3>Ticket 97 optimal periodic-projection audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "Goldbach optimal residue projection" : isTwin ? "Twin optimal residue projection" : "finite-modulus gate transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 각 modulus에서 Lambda의 실제 residue 평균을 사용하는 L2 최적 주기 모델을 만들었습니다. residual은 모든 residue에서 평균 0이고 주기 함수와 직교하지만, 두 점 상관의 부호는 여전히 결정되지 않습니다. 고정 modulus의 one-point 정보와 residual norm만으로는 sharp budget을 인증할 수 없습니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 유한 residue 정보가 target의 signed two-point correlation을 결정하는지 반대모형으로 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET97 finite-modulus audit", "Value"], rows)}
      ${Object.keys(projection).length ? `<div class="poc-bridge"><section><h3>L2-optimal periodic projection</h3>${table(["field", "statement"], Object.entries(projection))}</section><section><h3>Fixed-modulus sign no-go</h3>${table(["field", "statement"], Object.entries(noGo))}</section></div>` : ""}
      ${Object.keys(countermodel).length ? `<h3>Zero-residue-mean countermodel</h3>${table(["field", "value"], [["modulus", countermodel.modulus], ["sequence", JSON.stringify(countermodel.residual_sequence || [])], ["residue sums", JSON.stringify(countermodel.residue_sums || [])], ["Goldbach coefficient", countermodel.goldbach_additive_coefficient], ["shift-two coefficient", countermodel.twin_shift_two_coefficient], ["scope", countermodel.scope]])}` : ""}
      ${projectionRows.length ? `<h3>${isGoldbach ? "Goldbach" : "Twin"} optimal periodic replay</h3>${table(["scale", "W", "residual norm ratio", "max residue error", "periodic main", "signed residual", "norm-only lower"], projectionRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded fixed-modulus routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained growing-modulus route</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket98GrowingModulusLeakage(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.growing_modulus_leakage_audit || {};
  const machine = audit.machine_audit || {};
  const identity = audit.row_unique_identity_theorem || {};
  const finding = audit.leakage_finding || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const rows = Object.keys(audit).length ? [
    ["checkpoints", machine.checkpoint_count], ["maximum scale", machine.maximum_checkpoint],
    ["primorial moduli", Array.isArray(machine.primorial_moduli) ? machine.primorial_moduli.join(", ") : "missing"],
    ["non-row-unique Goldbach certificates", machine.non_row_unique_goldbach_certificate_count],
    ["non-row-unique Twin certificates", machine.non_row_unique_twin_certificate_count],
    ["first-certificate mismatches", machine.first_certificate_mismatch_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [["transfer route", bounded.ticket98_transfer || attempt.route || "missing"]];
  const checkpointRows = Array.isArray(machine.checkpoint_rows) ? machine.checkpoint_rows.map((checkpoint) => {
    const allRows = checkpoint.rows || [];
    const firstIndex = allRows.findIndex((row) => row.modulus === checkpoint.first_row_unique_modulus);
    const first = firstIndex >= 0 ? allRows[firstIndex] : {};
    const prior = firstIndex > 0 ? allRows[firstIndex - 1] : {};
    return [
      checkpoint.target,
      checkpoint.first_row_unique_modulus,
      Number(first.average_samples_per_occupied_residue || 0).toFixed(3),
      first.row_unique_leakage ? "yes / exact replay" : "no",
      prior.modulus || "none",
      prior.maximum_samples_per_occupied_residue || "none",
      isGoldbach ? checkpoint.non_row_unique_goldbach_certificate_count : checkpoint.non_row_unique_twin_certificate_count,
    ];
  }) : [];
  return `
    <div class="poc-ticket17 poc-ticket96 poc-ticket97 poc-ticket98">
      <h3>Ticket 98 growing-modulus leakage audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "Goldbach fitted-modulus leakage" : isTwin ? "Twin fitted-modulus leakage" : "growing-partition leakage transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> modulus를 키웠을 때 최초 인증은 세 scale 모두 각 residue에 관측값이 하나만 남는 지점에서 발생했습니다. 이때 주기 projection은 Lambda 원자료와 같고 residual은 0이므로, 인증은 새로운 산술 정리가 아니라 target correlation의 in-sample 재생입니다. row-unique 이전 인증은 0건입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 성장하는 partition이 관측값을 하나씩 식별해 residual을 인위적으로 0으로 만드는지 검사하는 누출 기준만 전이합니다.</p>`}
      ${table(["TICKET98 leakage boundary audit", "Value"], rows)}
      ${Object.keys(identity).length ? `<div class="poc-bridge"><section><h3>Row-unique identity theorem</h3><p>${escapeHtml(identity.statement || "")}</p>${list(identity.proof_steps || [])}</section><section><h3>Certificate leakage finding</h3>${table(["field", "statement"], Object.entries(finding))}</section></div>` : ""}
      ${checkpointRows.length ? `<h3>${isGoldbach ? "Goldbach" : "Twin"} primorial leakage boundary</h3>${table(["scale", "first certificate W", "samples / residue", "row unique", "preceding W", "preceding max samples", "pre-leak certificates"], checkpointRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded fitted-modulus routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained out-of-sample route</h3><p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket99OutOfSampleLocalModel(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.out_of_sample_local_model_audit || {};
  const machine = audit.machine_audit || {};
  const crossFit = audit.cross_fit_contract || {};
  const localMain = audit.external_local_main_theorem || {};
  const sufficient = audit.sufficient_residual_theorem || {};
  const envelope = machine.finite_residual_envelope_screen || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const rows = Object.keys(audit).length ? [
    ["checkpoints", machine.checkpoint_count], ["maximum checkpoint", machine.maximum_checkpoint],
    ["cross-fit configurations", machine.cross_fit_configuration_count],
    ["cross-fit Goldbach certificates", machine.cross_fit_goldbach_certificate_count],
    ["cross-fit Twin certificates", machine.cross_fit_twin_certificate_count],
    ["external norm certificates", isGoldbach ? machine.external_goldbach_norm_certificate_count : machine.external_twin_norm_certificate_count],
    ["finite envelope K", envelope.candidate_log_envelope_constant],
    ["total contract failures", machine.total_failure_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [["transfer route", bounded.ticket99_transfer || attempt.route || "missing"]];
  const crossRows = Array.isArray(machine.cross_fit_checkpoint_rows) ? machine.cross_fit_checkpoint_rows.map((checkpoint) => {
    const best = isGoldbach ? checkpoint.best_nonempty_goldbach_row : checkpoint.best_nonempty_twin_row;
    return [checkpoint.target, checkpoint.nonempty_configuration_count, checkpoint.empty_configuration_count, best?.modulus, best?.minimum_train_count, `${(Number(best?.evaluation_fraction || 0) * 100).toFixed(1)}%`, Number(isGoldbach ? best?.goldbach_margin_over_full_contamination_budget : best?.twin_margin_over_full_contamination_budget).toFixed(1)];
  }) : [];
  const envelopeRows = Object.keys(envelope).length ? [
    ["Goldbach calibration", envelope.goldbach?.calibration_maximum_row?.number, Number(envelope.goldbach?.calibration_maximum_row?.required_log_envelope_constant || 0).toFixed(3)],
    ["Goldbach validation", envelope.goldbach?.validation_maximum_row?.number, Number(envelope.goldbach?.validation_maximum_row?.required_log_envelope_constant || 0).toFixed(3)],
    ["Twin calibration", envelope.twin?.calibration_maximum_row?.number, Number(envelope.twin?.calibration_maximum_row?.required_log_envelope_constant || 0).toFixed(3)],
    ["Twin validation", envelope.twin?.validation_maximum_row?.number, Number(envelope.twin?.validation_maximum_row?.required_log_envelope_constant || 0).toFixed(3)],
  ] : [];
  return `
    <div class="poc-ticket17 poc-ticket97 poc-ticket98 poc-ticket99">
      <h3>Ticket 99 out-of-sample local-model audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "Goldbach external local residual" : isTwin ? "Twin external local residual" : "external-model independence transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> 학습 period와 평가 period를 분리한 120개 cross-fit 조합에서는 norm 인증이 0건이었습니다. 이어서 소수 데이터를 전혀 사용하지 않는 coprime 모델의 local main을 CRT로 정확히 하한화했습니다. 백만 범위에서 K=1.6 residual 후보가 holdout을 통과했지만, 이것은 무한 정리가 아니라 다음 Type II/dispersion 증명 목표입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 target과 분리된 구조 모델만 허용하고 signed residual을 별도 정리로 증명해야 한다는 독립성 규율만 전이합니다.</p>`}
      ${table(["TICKET99 independent local-model audit", "Value"], rows)}
      ${Object.keys(crossFit).length ? `<div class="poc-bridge"><section><h3>Disjoint cross-fit contract</h3>${table(["field", "statement"], Object.entries(crossFit))}</section><section><h3>Exact external local-main theorem</h3>${table(["field", "statement"], Object.entries(localMain))}</section></div>` : ""}
      ${crossRows.length ? `<h3>${isGoldbach ? "Goldbach" : "Twin"} cross-fit replay</h3>${table(["scale", "nonempty", "empty", "best W", "min train", "coverage", "norm margin"], crossRows)}` : ""}
      ${envelopeRows.length ? `<h3>Finite K/log(n) falsification screen</h3>${table(["track", "worst n", "required K"], envelopeRows)}<p>${escapeHtml(envelope.status || "")}; validation failures: ${Number(envelope.goldbach_validation_failure_count || 0) + Number(envelope.twin_validation_failure_count || 0)}.</p>` : ""}
      ${Object.keys(sufficient).length ? `<div class="poc-bridge"><section><h3>Sufficient signed-residual theorem</h3>${table(["field", "statement"], Object.entries(sufficient))}</section><section><h3>Discarded and retained routes</h3>${list(audit.discarded_routes || [])}<p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket100ExtendedResidualVaughan(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.extended_residual_vaughan_audit || {};
  const machine = audit.machine_audit || {};
  const search = audit.extended_counterexample_search || {};
  const vaughan = audit.vaughan_joint_cancellation_audit || {};
  const identity = audit.vaughan_identity || {};
  const contrapositive = audit.contrapositive_program || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const screen = isGoldbach ? search.goldbach : search.twin;
  const track = isGoldbach ? vaughan.goldbach : vaughan.twin;
  const rows = Object.keys(audit).length ? [
    ["Goldbach screen", machine.goldbach_screen_limit], ["Twin screen", machine.twin_screen_limit],
    ["Vaughan audit", machine.vaughan_limit], ["candidate K", machine.candidate_constant],
    ["screen failures", screen?.candidate_failure_count], ["overall required K", Number(screen?.overall_maximum_required_constant || 0).toFixed(3)],
    ["identity error", Number(identity.audit?.direct_type_ii_max_error || 0).toExponential(2)],
    ["contract failures", machine.total_failure_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [["transfer route", bounded.ticket100_transfer || attempt.route || "missing"]];
  const segmentRows = Array.isArray(screen?.segment_rows) ? screen.segment_rows.map((row) => [row.modulus, row.start, row.end, row.evaluated_count, Number(row.maximum_required_constant).toFixed(3), row.candidate_failure_count]) : [];
  const componentRows = track?.maximum_rows ? ["structured", "type_ii", "joint"].map((label) => {
    const row = track.maximum_rows[label] || {};
    return [label, row.number, row.modulus, Number(row.required_log_envelope_constant || 0).toFixed(3), Number(row.contribution_over_external_main || 0).toFixed(4)];
  }) : [];
  return `
    <div class="poc-ticket17 poc-ticket98 poc-ticket99 poc-ticket100">
      <h3>Ticket 100 extended residual and Vaughan audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "Goldbach joint Vaughan residual" : isTwin ? "Twin joint Vaughan residual" : "joint-component gate transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> Goldbach 6M 전수 짝수와 Twin 10M 누적 범위에서 K=1.6 반례는 없었습니다. 그러나 Vaughan Type II 항만 같은 상수로 따로 하한화하는 명제는 Goldbach N=930,930에서 필요한 K=7.91로 반증됐습니다. 구조항의 보상을 보존하는 결합 부호 정리만 유효한 다음 경로입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 개별 성분의 절댓값 경계가 아니라 결합된 signed cancellation을 증명해야 한다는 전략 반례만 전이합니다.</p>`}
      ${table(["TICKET100 joint-cancellation audit", "Value"], rows)}
      ${Object.keys(identity).length ? `<div class="poc-bridge"><section><h3>Exact Vaughan identity replay</h3>${table(["field", "statement"], Object.entries(identity).filter(([key]) => key !== "audit"))}${table(["audit", "value"], Object.entries(identity.audit || {}))}</section><section><h3>Componentwise proof-strategy counterexample</h3>${table(["field", "statement"], Object.entries(vaughan.componentwise_no_go || {}))}</section></div>` : ""}
      ${segmentRows.length ? `<h3>${isGoldbach ? "Goldbach 6M" : "Twin 10M"} schedule-transition screen</h3>${table(["W", "start", "end", "count", "max K", "failures"], segmentRows)}` : ""}
      ${componentRows.length ? `<h3>One-sided Vaughan component pressure</h3>${table(["component", "worst n", "W", "required K", "component / main"], componentRows)}` : ""}
      ${Object.keys(contrapositive).length ? `<div class="poc-bridge"><section><h3>Contrapositive proof program</h3>${table(["field", "statement"], Object.entries(contrapositive))}</section><section><h3>Discarded and retained routes</h3>${list(audit.discarded_routes || [])}<p>${escapeHtml(audit.retained_route || "")}</p><p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket101VaughanCutoffEnergy(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.vaughan_cutoff_energy_audit || {};
  const machine = audit.machine_audit || {};
  const frontier = audit.cutoff_frontier || {};
  const split = audit.problem_split || {};
  const energy = audit.energy_equivalence_audit || {};
  const isGoldbach = attempt.problem_id === "goldbach";
  const isTwin = attempt.problem_id === "twin-prime";
  const rows = Object.keys(audit).length ? [
    ["scale", machine.limit], ["candidate K", machine.candidate_constant],
    ["balanced pairs", machine.balanced_pair_count], ["Goldbach survivors", machine.balanced_goldbach_survivor_count],
    ["Twin survivors", machine.balanced_twin_survivor_count], ["energy failures", machine.energy_failure_count],
    ["next theorem", isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target],
  ] : [
    ["transfer route", bounded.ticket101_transfer || attempt.route || "missing"],
    ["independent target", bounded.independent_target || "missing"],
  ];
  const bestRows = Object.keys(frontier).length ? [
    ["Goldbach balanced best", frontier.best_balanced_goldbach_row?.u, frontier.best_balanced_goldbach_row?.v, frontier.best_balanced_goldbach_row?.type_ii_support_count, Number(frontier.best_balanced_goldbach_row?.goldbach?.separate_budget_sum || 0).toFixed(3)],
    ["Twin balanced best", frontier.best_balanced_twin_row?.u, frontier.best_balanced_twin_row?.v, frontier.best_balanced_twin_row?.type_ii_support_count, Number(frontier.best_balanced_twin_row?.twin?.separate_budget_sum || 0).toFixed(3)],
    ["Goldbach near-collapse", frontier.first_tested_near_collapse_goldbach_survivor?.u, frontier.first_tested_near_collapse_goldbach_survivor?.v, frontier.first_tested_near_collapse_goldbach_survivor?.type_ii_support_count, Number(frontier.first_tested_near_collapse_goldbach_survivor?.goldbach?.separate_budget_sum || 0).toFixed(3)],
    ["full collapse", frontier.full_collapse_row?.u, frontier.full_collapse_row?.v, frontier.full_collapse_row?.type_ii_support_count, Number(frontier.full_collapse_row?.goldbach?.separate_budget_sum || 0).toFixed(3)],
  ] : [];
  const energyRows = Array.isArray(energy.checkpoint_rows) ? energy.checkpoint_rows.map((row) => [row.target, Number(isGoldbach ? row.goldbach_mismatch_over_twice_energy : row.twin_mismatch_over_total_energy).toFixed(4), Number(isGoldbach ? row.goldbach_identity_error : row.twin_identity_error).toExponential(2), Number(isGoldbach ? row.goldbach_target_equivalence_error : row.twin_target_equivalence_error).toExponential(2)]) : [];
  return `
    <div class="poc-ticket17 poc-ticket99 poc-ticket100 poc-ticket101">
      <h3>Ticket 101 Vaughan cutoff and energy-equivalence audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isGoldbach ? "Goldbach balanced joint route" : isTwin ? "Twin separated balanced route" : "parameter and equivalence gate transfer only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${Object.keys(audit).length ? `<p><strong>한국어 해설:</strong> cutoff 최적화 결과 이번 감사가 비붕괴 균형 범위로 정한 U,V≤N^(1/3)에서 Goldbach 분리 예산 생존자는 없지만 Twin은 U=100,V=84에서 합 K=1.560으로 살아납니다. Goldbach의 제곱근 근처 성공은 Type II가 314개로 축소되거나 0이 되는 분해 붕괴입니다. 에너지 mismatch 표현은 원래 correlation 하한과 정확히 동치입니다.</p>` : `<p><strong>한국어 해설:</strong> 이 문제에는 parameter 최적화 없이 no-go를 일반화하지 않고, 에너지 재표현의 논리적 신규성을 검사하는 규율만 전이합니다.</p>`}
      ${table(["TICKET101 cutoff frontier audit", "Value"], rows)}
      ${bestRows.length ? `<h3>Balanced frontier and collapse boundary</h3>${table(["route", "U", "V", "Type II support", "budget sum"], bestRows)}` : ""}
      ${Object.keys(split).length ? `<div class="poc-bridge"><section><h3>Problem-specific theorem split</h3>${table(["problem", "finding"], [["Goldbach", split.goldbach?.finding], ["Twin", split.twin?.finding], ["Twin candidate", split.twin?.rounded_candidate]])}</section><section><h3>Energy rewrite novelty verdict</h3>${table(["field", "statement"], [["Goldbach identity", energy.identities?.goldbach], ["Twin identity", energy.identities?.twin], ["verdict", energy.novelty_verdict], ["independent use", energy.independent_use]])}</section></div>` : ""}
      ${energyRows.length ? `<h3>${isGoldbach ? "Goldbach reflection" : "Twin shift"} energy replay</h3>${table(["scale", "mismatch ratio", "identity error", "equivalence error"], energyRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Contrapositive boundary</h3>${table(["field", "statement"], Object.entries(audit.contrapositive_boundary || {}))}</section><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}<p>${escapeHtml(isGoldbach ? audit.goldbach_next_theorem_target : audit.twin_next_theorem_target)}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket102TwinDyadicHoldout(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_dyadic_vaughan_holdout || {};
  const machine = audit.machine_audit || {};
  const dyadic = audit.dyadic_holdout_audit || {};
  const rescue = audit.fresh_rescue_holdout || {};
  const correction = audit.constant_threshold_correction || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["post-selection points", machine.holdout_evaluated_count],
    ["structured failures", machine.holdout_structured_failure_count],
    ["Type II failures", machine.holdout_type_ii_failure_count],
    ["fresh 8M points", machine.fresh_rescue_evaluated_count],
    ["fresh rescue failures", machine.fresh_rescue_failure_count],
    ["contract failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["priority route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const dyadicRows = Array.isArray(dyadic.rows) ? dyadic.rows.map((row) => [
    row.horizon,
    row.split,
    `${row.u}/${row.v}`,
    Number(row.structured?.maximum_row?.required_log_envelope_constant || 0).toFixed(3),
    row.structured?.failure_count,
    Number(row.type_ii?.maximum_row?.required_log_envelope_constant || 0).toFixed(3),
    row.type_ii?.failure_count,
    `${(100 * Number(row.type_ii_support_fraction || 0)).toFixed(2)}%`,
  ]) : [];
  const rescueRow = rescue.row || {};
  return `
    <div class="poc-ticket17 poc-ticket100 poc-ticket101 poc-ticket102">
      <h3>Ticket 102 Twin dyadic Vaughan holdout</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "post-selection Twin budget falsification" : "problem-specific priority correction only"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 1M에서 선택한 구조항 K=1.40은 독립 2M 구간의 100만 점 모두에서 실패했습니다. 그러나 1.6은 필수 문턱이 아니며, 전 규모에서 고정된 유한 K가 존재하면 충분합니다. 실패를 본 뒤 새로 등록한 K_S=4, K_II=1은 이전에 열지 않은 8M 구간 400만 점에서 통과했지만 아직 유한 증거입니다.</p>` : `<p><strong>한국어 해설:</strong> 일반 에너지 재표현보다 이 문제 고유의 독립 정리를 우선하도록 연구 목표를 교정했습니다. TICKET-102는 이 문제의 새 무한 정리를 증명하지 않습니다.</p>`}
      ${table(["TICKET102 dyadic holdout audit", "Value"], summaryRows)}
      ${dyadicRows.length ? `<h3>Complete dyadic block replay</h3>${table(["X", "split", "U/V", "structured K", "failures", "Type II K", "failures", "Type II support"], dyadicRows)}` : ""}
      ${Object.keys(correction).length ? `<div class="poc-bridge"><section><h3>Threshold correction</h3>${table(["field", "statement"], Object.entries(correction))}</section><section><h3>Fresh 8M rescue holdout</h3>${table(["field", "value"], [["status", rescue.status], ["budgets", `${rescueRow.structured?.budget} + ${rescueRow.type_ii?.budget}`], ["maximum structured K", Number(rescueRow.structured?.maximum_row?.required_log_envelope_constant || 0).toFixed(4)], ["maximum Type II K", Number(rescueRow.type_ii?.maximum_row?.required_log_envelope_constant || 0).toFixed(4)], ["Type II support", `${(100 * Number(rescueRow.type_ii_support_fraction || 0)).toFixed(2)}%`], ["relative replay error", Number(rescueRow.joint_reconstruction_max_relative_error || 0).toExponential(2)]])}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact logical upgrade</h3>${table(["field", "statement"], Object.entries(audit.logical_upgrade || {}))}</section><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket103TwinLocalBlock(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_local_block_audit || {};
  const machine = audit.machine_audit || {};
  const local = audit.local_block_audit || {};
  const oracle = audit.small_scale_sign_oracle || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["local-block integers", machine.evaluated_integer_count],
    ["large negative Type II blocks", machine.negative_type_ii_block_count],
    ["small sign counterexamples", machine.small_sign_negative_block_count],
    ["maximum structured K", Number(local.maximum_structured_required_constant || 0).toFixed(4)],
    ["maximum Type II K", Number(local.maximum_type_ii_required_constant || 0).toFixed(4)],
    ["maximum joint K", Number(local.maximum_joint_required_constant || 0).toFixed(4)],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const blockRows = Array.isArray(local.rows) ? local.rows.map((row) => [
    row.horizon,
    `${row.block_start}-${row.block_end}`,
    `${row.u}/${row.v}`,
    row.modulus,
    Number(row.structured_required_constant || 0).toFixed(3),
    Number(row.type_ii_required_constant || 0).toFixed(3),
    Number(row.joint_required_constant || 0).toFixed(3),
    `${(100 * Number(row.type_ii_support_fraction || 0)).toFixed(2)}%`,
  ]) : [];
  const counterexample = oracle.first_counterexample || {};
  return `
    <div class="poc-ticket17 poc-ticket101 poc-ticket102 poc-ticket103">
      <h3>Ticket 103 Twin exact local-block audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "cumulative masking removal" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 누적 0..x 상관을 실제 (X/2,X] 국소 블록으로 바꿨습니다. 125K~8M 주요 블록의 Type II 합은 양수였지만 X=1000에서 -174.7165인 정확한 부호 반례가 나왔습니다. 따라서 항상 비음수라는 경로는 폐기하고 sufficiently large 블록의 고정 유한 하한만 유지합니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 국소 블록 교정을 다른 문제의 지름길로 전이하지 않고, 기존 문제 고유의 무한 정리를 그대로 유지합니다.</p>`}
      ${table(["TICKET103 local-block audit", "Value"], summaryRows)}
      ${blockRows.length ? `<h3>Exact principal dyadic blocks</h3>${table(["X", "block", "U/V", "W", "structured K", "Type II K", "joint K", "Type II support"], blockRows)}` : ""}
      ${Object.keys(counterexample).length ? `<div class="poc-bridge"><section><h3>Small-scale Type II sign counterexample</h3>${table(["field", "value"], [["X", counterexample.horizon], ["block", `${counterexample.block_start}-${counterexample.block_end}`], ["Type II correlation", Number(counterexample.type_ii_local_correlation).toFixed(4)], ["required K", Number(counterexample.type_ii_required_constant).toFixed(4)], ["replay error", Number(counterexample.reconstruction_relative_error).toExponential(2)]])}</section><section><h3>Conditional infinite bridge</h3>${table(["field", "statement"], Object.entries(audit.conditional_bridge || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Cumulative-to-local verdict</h3><p>${escapeHtml(audit.cumulative_to_local_verdict || "")}</p></section><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket104TwinTypeIIMobius(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_typeii_mobius_anatomy || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["anatomy rows", machine.row_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const anatomyRows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    Number(row.outer_weight_signed_sum || 0).toFixed(2),
    Number(row.signed_over_l1_mass || 0).toFixed(4),
    Number(row.actual_required_constant || 0).toFixed(2),
    Number(row.negative_mass_required_constant || 0).toFixed(2),
    Number(row.abel_triangle_required_constant || 0).toFixed(2),
    Number(row.outer_identity_absolute_error || 0).toExponential(2),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket102 poc-ticket103 poc-ticket104">
      <h3>Ticket 104 Twin Type II weighted-Mobius anatomy</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "exact Type II identity and lossy-bound audit" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 국소 Type II 항을 T_X=Σμ(d)A_X(d), A_X(d)≥0으로 정확히 분해했습니다. 직접 항은 큰 블록에서 양수지만 음의 항을 따로 합치면 K가 21.75→39.92, Abel 뒤 삼각부등식은 354→1088로 커집니다. 발산을 증명한 것은 아니며, shifted-prime 가중치와 Möbius 부호의 결합을 보존해야 한다는 정보 경계입니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 weighted-Mobius 구조를 다른 문제에 전이하지 않고 기존 문제 고유의 무한 목표를 유지합니다.</p>`}
      ${table(["TICKET104 weighted-Mobius audit", "Value"], summaryRows)}
      ${anatomyRows.length ? `<h3>Exact outer-divisor anatomy</h3>${table(["X", "direct T", "T/L1", "actual K", "negative-mass K", "Abel-triangle K", "identity error"], anatomyRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact reduction</h3>${table(["field", "statement"], Object.entries(audit.exact_reduction || {}))}</section><section><h3>Abel information-loss verdict</h3>${table(["field", "statement"], [["finding", audit.abel_no_go?.finding], ["scope", audit.abel_no_go?.scope]])}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket105TwinCenteredProgression(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_centered_progression_discrepancy || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["centered rows", machine.row_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    Number(row.exact_type_ii || 0).toFixed(2),
    Number(row.progression_baseline_component || 0).toFixed(2),
    Number(row.centered_progression_discrepancy || 0).toFixed(2),
    Number(row.negative_centered_mass_required_constant || 0).toFixed(2),
    Number(row.cauchy_centered_required_constant || 0).toFixed(2),
    Number(row.mobius_centered_cosine || 0).toFixed(4),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket103 poc-ticket104 poc-ticket105">
      <h3>Ticket 105 Twin centered progression discrepancy</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "independent progression centering" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 홀수 진행식의 독립 주항 q/φ(q)를 먼저 제거했습니다. 중심화 후 음의 항별 K는 4.50→5.15→5.41로 줄었지만 전체 Cauchy 경계는 26.69→37.12→41.15입니다. 남은 객체는 Möbius 부호와 소수 산술진행 분포 오차의 bilinear 결합이며 아직 균일 정리가 아닙니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 산술진행 중심화를 다른 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET105 centered progression audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>Baseline and centered discrepancy</h3>${table(["X", "Type II", "progression main", "centered", "negative-mass K", "Cauchy K", "cosine"], rows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact centering</h3>${table(["field", "statement"], Object.entries(audit.exact_centering || {}))}</section><section><h3>Information boundary</h3>${table(["field", "statement"], [["finding", audit.information_boundary?.finding], ["scope", audit.information_boundary?.scope]])}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket106TwinGroupedDispersion(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_modulus_grouped_dispersion || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["grouped rows", machine.row_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    row.support_count,
    Number(row.grouped_cauchy_required_constant || 0).toFixed(2),
    Number(row.outer_d_cauchy_required_constant || 0).toFixed(2),
    `${(100 * Number(row.row_unique_support_fraction || 0)).toFixed(2)}%`,
    Number(row.row_unique_signed_contribution || 0).toFixed(1),
    Number(row.non_row_unique_signed_contribution || 0).toFixed(1),
  ]) : [];
  const last = rows.length ? audit.rows[audit.rows.length - 1] : {};
  const occupancyRows = Array.isArray(last.occupancy_rows) ? last.occupancy_rows.map((row) => [
    row.maximum_occupancy,
    row.support_count,
    `${(100 * Number(row.support_fraction || 0)).toFixed(2)}%`,
    Number(row.signed_contribution || 0).toFixed(1),
    Number(row.complement_signed_contribution || 0).toFixed(1),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket104 poc-ticket105 poc-ticket106">
      <h3>Ticket 106 Twin modulus-grouped dispersion</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "grouped dispersion and sparse leakage" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 같은 q=dr를 먼저 합쳤지만 2M grouped Cauchy는 K=249.12로 악화됐습니다. support의 72.31%가 표본 1개 이하이고 중심화 총합의 약 96%를 공급하므로 양의 신호 대부분은 조밀 progression 평균이 아니라 희소 행 재생입니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 희소-modulus 누출을 다른 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET106 grouped dispersion audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>Grouped norm and sparse-cell pressure</h3>${table(["X", "q support", "grouped Cauchy K", "outer-d Cauchy K", "one-sample support", "sparse contribution", "dense complement"], rows)}` : ""}
      ${occupancyRows.length ? `<h3>2M occupancy ladder</h3>${table(["max samples", "support", "fraction", "sparse contribution", "complement"], occupancyRows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact modulus grouping</h3>${table(["field", "statement"], Object.entries(audit.exact_grouping || {}))}</section><section><h3>Sparse-modulus leakage verdict</h3>${table(["field", "statement"], Object.entries(audit.dispersion_boundary || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket107TwinSparseTail(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_sparse_tail_recombination || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["recombination rows", machine.row_count],
    ["sparse sign count", machine.centered_sparse_sign_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    `${row.sparse_q_support_count} -> ${row.sparse_n_support_count}`,
    `${(100 * Number(row.n_grouping_l1_retention || 0)).toFixed(2)}%`,
    Number(row.structured_residual || 0).toFixed(1),
    Number(row.sparse_type_ii_correlation || 0).toFixed(1),
    Number(row.dense_type_ii_correlation || 0).toFixed(1),
    Number(row.structured_sparse_required_constant || 0).toFixed(2),
    Number(row.joint_required_constant || 0).toFixed(2),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket105 poc-ticket106 poc-ticket107">
      <h3>Ticket 107 Twin sparse-tail recombination</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "q-to-n recombination and three-way signed audit" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 8M에서 희소 q 셀 1,589,098개는 n 셀 1,099,268개로 합쳐지고 L1 질량은 69.53%만 남습니다. 구조화 잔차 -1,281,289.5, 희소 II +399,460.6, 조밀 II +756,121.9를 함께 보존해야 공동 K=0.37이 되며, 구조화+희소만 분리하면 K=2.59입니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 q-to-n 재결합 결과를 이 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET107 sparse-tail recombination audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>q-to-n compression and signed compensation</h3>${table(["X", "sparse q -> n", "L1 retained", "structured residual", "sparse II", "dense II", "partial K", "joint K"], rows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact Vaughan recombination</h3>${table(["field", "statement"], Object.entries(audit.exact_recombination || {}))}</section><section><h3>Component-budget verdict</h3>${table(["field", "statement"], Object.entries(audit.route_verdict || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket108TwinSmoothing(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_joint_equivalence_smoothing || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["audit rows", machine.row_count],
    ["smooth improvements", machine.smoothing_improvement_count],
    ["smooth worsenings", machine.smoothing_worsening_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    Number(row.hard_joint_required_constant || 0).toFixed(4),
    Number(row.smooth_joint_required_constant || 0).toFixed(4),
    Number(row.hard_joint_equivalence_absolute_error || 0).toExponential(2),
    Number(row.smooth_structured_residual || 0).toFixed(1),
    Number(row.smooth_sparse_type_ii || 0).toFixed(1),
    Number(row.smooth_dense_type_ii || 0).toFixed(1),
    Number(row.smooth_proper_prime_power_contamination || 0).toFixed(1),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket106 poc-ticket107 poc-ticket108">
      <h3>Ticket 108 Twin joint-equivalence and smoothing</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "no-reduction audit and nonnegative bump bridge" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 세 성분 hard-cutoff 하한은 원래 잔차 하한과 정확히 같아 새 환원이 아닙니다. 비음수 bump는 정확한 대우 연결을 주지만 6개 중 2개 블록에서만 개선됐고, 8M에서는 hard K=0.3691보다 smooth K=0.4226이 큽니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 smoothing 결과를 이 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET108 equivalence and smoothing audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>Hard versus smooth signed residual</h3>${table(["X", "hard K", "smooth K", "equivalence error", "smooth structured", "smooth sparse II", "smooth dense II", "power contamination"], rows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Algebraic no-reduction</h3>${table(["field", "statement"], Object.entries(audit.equivalence_no_go || {}))}</section><section><h3>Nonnegative bump bridge</h3>${table(["field", "statement"], Object.entries(audit.smoothed_excess_bridge || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket109TwinSpectralPhase(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_spectral_phase_audit || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["spectral rows", machine.row_count],
    ["low-frequency refutations", machine.low_frequency_refutation_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [
    ["preserved route", attempt.route || "missing"],
    ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"],
  ];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    Number(row.symmetric_bump_correlation || 0).toFixed(1),
    Number(row.positive_phase_contribution || 0).toFixed(1),
    Number(row.negative_phase_contribution || 0).toFixed(1),
    Number(row.phase_cancellation_ratio || 0).toFixed(4),
    Number(row.best_low_frequency_lower_bound || 0).toFixed(1),
    Number(row.spectral_identity_absolute_error || 0).toExponential(2),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket107 poc-ticket108 poc-ticket109">
      <h3>Ticket 109 Twin spectral-phase audit</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "exact phase identity and low-frequency no-go" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 1.05M에서 양의 위상 1.829M과 음의 위상 -1.370M의 차이가 실제 상관 0.459M을 만듭니다. 최선의 원점 저주파 하한은 -3.338M이므로 유리수 major arc 구조 없이 양의 하한을 얻을 수 없습니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 spectral no-go를 이 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET109 spectral phase audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>Positive and negative phase balance</h3>${table(["X", "exact correlation", "positive phase", "negative phase", "cancellation ratio", "best low-frequency bound", "identity error"], rows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Exact spectral identity</h3>${table(["field", "statement"], Object.entries(audit.exact_spectral_identity || {}))}</section><section><h3>Low-frequency no-go</h3>${table(["field", "statement"], Object.entries(audit.low_frequency_no_go || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderTicket110TwinRationalArcs(attempt) {
  if (!attempt) return "";
  const bounded = attempt.bounded_result || {};
  const audit = bounded.twin_rational_arc_budget || {};
  const machine = audit.machine_audit || {};
  const isTwin = attempt.problem_id === "twin-prime";
  const summaryRows = Object.keys(audit).length ? [
    ["maximum horizon", machine.maximum_horizon],
    ["audit rows", machine.row_count],
    ["Q cutoffs", machine.cutoff_count],
    ["trivial-minor refutations", machine.trivial_minor_refutation_count],
    ["identity failures", machine.contract_failure_count],
    ["next theorem", audit.next_theorem_target],
  ] : [["preserved route", attempt.route || "missing"], ["independent target", bounded.independent_target || attempt.candidate_theorem || "missing"]];
  const rows = Array.isArray(audit.rows) ? audit.rows.map((row) => [
    row.horizon,
    row.best_denominator_cutoff,
    `${(100 * Number(row.best_major_energy_fraction || 0)).toFixed(2)}%`,
    Number(row.best_major_phase_contribution || 0).toFixed(1),
    Number(row.best_minor_phase_contribution || 0).toFixed(1),
    Number(row.best_minor_phase_to_energy_ratio || 0).toExponential(2),
    Number(row.best_trivial_minor_lower_bound || 0).toFixed(1),
    Number(row.best_rigorous_total_lower_bound || 0).toFixed(1),
  ]) : [];
  return `
    <div class="poc-ticket17 poc-ticket108 poc-ticket109 poc-ticket110">
      <h3>Ticket 110 Twin rational major-arc budget</h3>
      <div class="poc-head"><div><span>Status</span><strong>${escapeHtml(statusText(attempt.status))}</strong></div><div><span>Route</span><strong>${escapeHtml(attempt.route || "missing")}</strong></div><div><span>Scope</span><strong>${isTwin ? "anti-circular major arcs and minor no-go" : "problem-specific target preserved"}</strong></div></div>
      <p>${escapeHtml(attempt.attempt || "")}</p>
      ${isTwin ? `<p><strong>한국어 해설:</strong> 1.05M에서 Q=32 major 기여 461,203.6과 실제 minor -2,063.7이 상관을 재구성하지만 trivial minor 하한은 -3,105,699.1입니다. 필요한 것은 minor 에너지 대비 약 6.6e-4 수준의 signed Type II 상쇄 정리입니다.</p>` : `<p><strong>한국어 해설:</strong> Twin의 major-arc 결과를 이 문제에 전이하지 않고 기존 독립 목표를 유지합니다.</p>`}
      ${table(["TICKET110 rational arc audit", "Value"], summaryRows)}
      ${rows.length ? `<h3>Major capture and minor saving gap</h3>${table(["X", "best Q", "major energy", "major phase", "minor phase", "minor/energy", "trivial minor", "rigorous total"], rows)}` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Anti-circular major-arc contract</h3>${table(["field", "statement"], Object.entries(audit.major_arc_contract || {}))}</section><section><h3>Trivial minor no-go</h3>${table(["field", "statement"], Object.entries(audit.minor_arc_no_go || {}))}</section></div>` : ""}
      ${Object.keys(audit).length ? `<div class="poc-bridge"><section><h3>Discarded routes</h3>${list(audit.discarded_routes || [])}</section><section><h3>Retained theorem</h3><p>${escapeHtml(audit.next_theorem_target || "")}</p></section></div>` : ""}
      <p class="proof-boundary">${escapeHtml(audit.proof_boundary || attempt.claim_boundary || "")}</p>
    </div>
  `;
}

function renderProofOrCounterexample(ticket, breakthroughTicket, reductionTicket, pressureTicket, valuationPrefixTicket, twoAdicBranchTicket, negationPressureTicket, cegisRankTicket, bridgeWeightTicket, formalKernelTicket, microLemmaTicket, rankFrontierTicket, trichotomyTicket, adaptiveFrontierTicket, potentialSynthesisTicket, featureStutterTicket, statefulMeasureTicket, globalMeasureTicket, highBranchAutomatonTicket, limsupMassRefinementTicket, nullFrontierArithmeticTicket, pointwiseRankSynthesisTicket, symbolicFrontierExtensionTicket, phaseStatePotentialTicket, transitionClosureTicket, rankEscapeNormalizationTicket, parametricTemplateTicket, liftConstraintMeasureTicket, featureMeasureCounteredgeTicket, symbolicRankClauseTicket, stableClauseGrammarTicket, periodicStateLassoTicket, automatonReachabilityTicket, symbolicPreimageTicket, phaseLiftExceptionTicket, terminalLiftTicket, frontierBudgetTicket, symbolicTerminalTicket, newTemplateFamilyTicket, phase5GateTicket, preGateProjectionTicket, parametricAutomatonTicket, affineBoundaryLiftTicket, symbolicLiftMismatchTicket, mixedCylinderSeparatorTicket, symbolicFailureOffsetTicket, mod16TransitionCoverTicket, mod16AutomatonCoverTicket, symbolicMod16TransitionTicket, startTemplateChainExtinctionTicket, complementCoverTicket, openTemplateRankTicket, cycleSccRefinementTicket, prefixConsumedRankTicket, prefixFrontierExpansionTicket, strongerFrontierCoordinateTicket, infiniteFrontierLiftClosureTicket, lineagePressureForestTicket, coverageLeakageEscapeForestTicket, escapeCoordinateClosureTicket, symbolicBoundaryRecurrenceTicket, fixedPrefixBoundaryOrbitTicket, finiteCylinderNoGoTicket, archimedeanTwoAdicRankNoGoTicket, leastCounterexampleCompactnessNoGoTicket, mersennePostCompensationNoGoTicket, fixedMersenneWindowNoGoTicket, mersenneLogWindowLowerBoundTicket, twoAdicCycleLogDelayTicket, accessibleCycleSupremumTicket, coefficientOneBoundaryTicket, digitRunBoundaryTicket, runLengthTwoNoGoTicket, goldenMeanReductionTicket, normalizedErrorTicket, errorTailInvariantSetTicket, scaleSensitiveThresholdTicket, twinCorrelationExcessTicket, signedRemainderGoldbachTicket, sharpContaminationEquivalenceTicket, fourierPhaseInformationTicket, periodicProjectionResidualTicket, growingModulusLeakageTicket, outOfSampleLocalModelTicket, extendedResidualVaughanTicket, vaughanCutoffEnergyTicket, twinDyadicHoldoutTicket, twinLocalBlockTicket, twinTypeIIMobiusTicket, twinCenteredProgressionTicket, twinGroupedDispersionTicket, twinSparseTailTicket, twinSmoothingTicket, twinSpectralTicket, twinRationalArcTicket) {
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
    ${renderTicket26MicroLemma(microLemmaTicket)}
    ${renderTicket27RankFrontier(rankFrontierTicket)}
    ${renderTicket28Trichotomy(trichotomyTicket)}
    ${renderTicket29AdaptiveFrontier(adaptiveFrontierTicket)}
    ${renderTicket30PotentialSynthesis(potentialSynthesisTicket)}
    ${renderTicket31FeatureStutter(featureStutterTicket)}
    ${renderTicket32StatefulMeasure(statefulMeasureTicket)}
    ${renderTicket33GlobalMeasure(globalMeasureTicket)}
    ${renderTicket34HighBranchAutomaton(highBranchAutomatonTicket)}
    ${renderTicket35LimsupMassRefinement(limsupMassRefinementTicket)}
    ${renderTicket36NullFrontierArithmetic(nullFrontierArithmeticTicket)}
    ${renderTicket37PointwiseRankSynthesis(pointwiseRankSynthesisTicket)}
    ${renderTicket38SymbolicFrontierExtension(symbolicFrontierExtensionTicket)}
    ${renderTicket39PhaseStatePotential(phaseStatePotentialTicket)}
    ${renderTicket40TransitionClosure(transitionClosureTicket)}
    ${renderTicket41RankEscapeNormalization(rankEscapeNormalizationTicket)}
    ${renderTicket42ParametricTemplate(parametricTemplateTicket)}
    ${renderTicket43LiftConstraintMeasure(liftConstraintMeasureTicket)}
    ${renderTicket44FeatureMeasureCounteredge(featureMeasureCounteredgeTicket)}
    ${renderTicket45SymbolicRankClause(symbolicRankClauseTicket)}
    ${renderTicket46StableClauseGrammar(stableClauseGrammarTicket)}
    ${renderTicket47PeriodicStateLasso(periodicStateLassoTicket)}
    ${renderTicket48AutomatonReachability(automatonReachabilityTicket)}
    ${renderTicket49SymbolicPreimage(symbolicPreimageTicket)}
    ${renderTicket50PhaseLiftException(phaseLiftExceptionTicket)}
    ${renderTicket51TerminalLift(terminalLiftTicket)}
    ${renderTicket52FrontierBudget(frontierBudgetTicket)}
    ${renderTicket53SymbolicTerminal(symbolicTerminalTicket)}
    ${renderTicket54NewTemplateFamily(newTemplateFamilyTicket)}
    ${renderTicket55Phase5Gate(phase5GateTicket)}
    ${renderTicket56PreGateProjection(preGateProjectionTicket)}
    ${renderTicket57ParametricAutomaton(parametricAutomatonTicket)}
    ${renderTicket58AffineBoundaryLift(affineBoundaryLiftTicket)}
    ${renderTicket59SymbolicLiftMismatch(symbolicLiftMismatchTicket)}
    ${renderTicket60MixedCylinderSeparator(mixedCylinderSeparatorTicket)}
    ${renderTicket61SymbolicFailureOffset(symbolicFailureOffsetTicket)}
    ${renderTicket62Mod16TransitionCover(mod16TransitionCoverTicket)}
    ${renderTicket63Mod16AutomatonCover(mod16AutomatonCoverTicket)}
    ${renderTicket64SymbolicMod16Transition(symbolicMod16TransitionTicket)}
    ${renderTicket65StartTemplateChainExtinction(startTemplateChainExtinctionTicket)}
    ${renderTicket66ComplementCover(complementCoverTicket)}
    ${renderTicket67OpenTemplateRank(openTemplateRankTicket)}
    ${renderTicket68CycleSccRefinement(cycleSccRefinementTicket)}
    ${renderTicket69PrefixConsumedRank(prefixConsumedRankTicket)}
    ${renderTicket70PrefixFrontierExpansion(prefixFrontierExpansionTicket)}
    ${renderTicket71StrongerFrontierCoordinate(strongerFrontierCoordinateTicket)}
    ${renderTicket72InfiniteFrontierLiftClosure(infiniteFrontierLiftClosureTicket)}
    ${renderTicket73LineagePressureForest(lineagePressureForestTicket)}
    ${renderTicket74CoverageLeakageEscapeForest(coverageLeakageEscapeForestTicket)}
    ${renderTicket75EscapeCoordinateClosure(escapeCoordinateClosureTicket)}
    ${renderTicket76SymbolicBoundaryRecurrence(symbolicBoundaryRecurrenceTicket)}
    ${renderTicket77FixedPrefixBoundaryOrbit(fixedPrefixBoundaryOrbitTicket)}
    ${renderTicket78FiniteCylinderNoGo(finiteCylinderNoGoTicket)}
    ${renderTicket79ArchimedeanTwoAdicRankNoGo(archimedeanTwoAdicRankNoGoTicket)}
    ${renderTicket80LeastCounterexampleCompactnessNoGo(leastCounterexampleCompactnessNoGoTicket)}
    ${renderTicket81MersennePostCompensationNoGo(mersennePostCompensationNoGoTicket)}
    ${renderTicket82FixedMersenneWindowNoGo(fixedMersenneWindowNoGoTicket)}
    ${renderTicket83MersenneLogWindowLowerBound(mersenneLogWindowLowerBoundTicket)}
    ${renderTicket84TwoAdicCycleLogDelay(twoAdicCycleLogDelayTicket)}
    ${renderTicket85AccessibleCycleSupremum(accessibleCycleSupremumTicket)}
    ${renderTicket86CoefficientOneBoundary(coefficientOneBoundaryTicket)}
    ${renderTicket87TwoAdicDigitRunBoundary(digitRunBoundaryTicket)}
    ${renderTicket88RunLengthTwoNoGo(runLengthTwoNoGoTicket)}
    ${renderTicket89FixedLogGoldenMeanReduction(goldenMeanReductionTicket)}
    ${renderTicket90NormalizedErrorGhostLasso(normalizedErrorTicket)}
    ${renderTicket91ErrorTailInvariantSet(errorTailInvariantSetTicket)}
    ${renderTicket92ScaleSensitiveThreshold(scaleSensitiveThresholdTicket)}
    ${renderTicket93TwinCorrelationExcess(twinCorrelationExcessTicket)}
    ${renderTicket94SignedRemainderAndGoldbach(signedRemainderGoldbachTicket)}
    ${renderTicket95SharpContaminationAndEquivalence(sharpContaminationEquivalenceTicket)}
    ${renderTicket96FourierPhaseInformation(fourierPhaseInformationTicket)}
    ${renderTicket97PeriodicProjectionResidual(periodicProjectionResidualTicket)}
    ${renderTicket98GrowingModulusLeakage(growingModulusLeakageTicket)}
    ${renderTicket99OutOfSampleLocalModel(outOfSampleLocalModelTicket)}
    ${renderTicket100ExtendedResidualVaughan(extendedResidualVaughanTicket)}
    ${renderTicket101VaughanCutoffEnergy(vaughanCutoffEnergyTicket)}
    ${renderTicket102TwinDyadicHoldout(twinDyadicHoldoutTicket)}
    ${renderTicket103TwinLocalBlock(twinLocalBlockTicket)}
    ${renderTicket104TwinTypeIIMobius(twinTypeIIMobiusTicket)}
    ${renderTicket105TwinCenteredProgression(twinCenteredProgressionTicket)}
    ${renderTicket106TwinGroupedDispersion(twinGroupedDispersionTicket)}
    ${renderTicket107TwinSparseTail(twinSparseTailTicket)}
    ${renderTicket108TwinSmoothing(twinSmoothingTicket)}
    ${renderTicket109TwinSpectralPhase(twinSpectralTicket)}
    ${renderTicket110TwinRationalArcs(twinRationalArcTicket)}
  `;
}

function render(payload, problem, proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt, ticket26Attempt, ticket27Attempt, ticket28Attempt, ticket29Attempt, ticket30Attempt, ticket31Attempt, ticket32Attempt, ticket33Attempt, ticket34Attempt, ticket35Attempt, ticket36Attempt, ticket37Attempt, ticket38Attempt, ticket39Attempt, ticket40Attempt, ticket41Attempt, ticket42Attempt, ticket43Attempt, ticket44Attempt, ticket45Attempt, ticket46Attempt, ticket47Attempt, ticket48Attempt, ticket49Attempt, ticket50Attempt, ticket51Attempt, ticket52Attempt, ticket53Attempt, ticket54Attempt, ticket55Attempt, ticket56Attempt, ticket57Attempt, ticket58Attempt, ticket59Attempt, ticket60Attempt, ticket61Attempt, ticket62Attempt, ticket63Attempt, ticket64Attempt, ticket65Attempt, ticket66Attempt, ticket67Attempt, ticket68Attempt, ticket69Attempt, ticket70Attempt, ticket71Attempt, ticket72Attempt, ticket73Attempt, ticket74Attempt, ticket75Attempt, ticket76Attempt, ticket77Attempt, ticket78Attempt, ticket79Attempt, ticket80Attempt, ticket81Attempt, ticket82Attempt, ticket83Attempt, ticket84Attempt, ticket85Attempt, ticket86Attempt, ticket87Attempt, ticket88Attempt, ticket89Attempt, ticket90Attempt, ticket91Attempt, ticket92Attempt, ticket93Attempt, ticket94Attempt, ticket95Attempt, ticket96Attempt, ticket97Attempt, ticket98Attempt, ticket99Attempt, ticket100Attempt, ticket101Attempt, ticket102Attempt, ticket103Attempt, ticket104Attempt, ticket105Attempt, ticket106Attempt, ticket107Attempt, ticket108Attempt, ticket109Attempt, ticket110Attempt) {
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
  if (pocPanel) pocPanel.innerHTML = renderProofOrCounterexample(proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt, ticket26Attempt, ticket27Attempt, ticket28Attempt, ticket29Attempt, ticket30Attempt, ticket31Attempt, ticket32Attempt, ticket33Attempt, ticket34Attempt, ticket35Attempt, ticket36Attempt, ticket37Attempt, ticket38Attempt, ticket39Attempt, ticket40Attempt, ticket41Attempt, ticket42Attempt, ticket43Attempt, ticket44Attempt, ticket45Attempt, ticket46Attempt, ticket47Attempt, ticket48Attempt, ticket49Attempt, ticket50Attempt, ticket51Attempt, ticket52Attempt, ticket53Attempt, ticket54Attempt, ticket55Attempt, ticket56Attempt, ticket57Attempt, ticket58Attempt, ticket59Attempt, ticket60Attempt, ticket61Attempt, ticket62Attempt, ticket63Attempt, ticket64Attempt, ticket65Attempt, ticket66Attempt, ticket67Attempt, ticket68Attempt, ticket69Attempt, ticket70Attempt, ticket71Attempt, ticket72Attempt, ticket73Attempt, ticket74Attempt, ticket75Attempt, ticket76Attempt, ticket77Attempt, ticket78Attempt, ticket79Attempt, ticket80Attempt, ticket81Attempt, ticket82Attempt, ticket83Attempt, ticket84Attempt, ticket85Attempt, ticket86Attempt, ticket87Attempt, ticket88Attempt, ticket89Attempt, ticket90Attempt, ticket91Attempt, ticket92Attempt, ticket93Attempt, ticket94Attempt, ticket95Attempt, ticket96Attempt, ticket97Attempt, ticket98Attempt, ticket99Attempt, ticket100Attempt, ticket101Attempt, ticket102Attempt, ticket103Attempt, ticket104Attempt, ticket105Attempt, ticket106Attempt, ticket107Attempt, ticket108Attempt, ticket109Attempt, ticket110Attempt);
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
  let ticket26Attempt = null;
  let ticket27Attempt = null;
  let ticket28Attempt = null;
  let ticket29Attempt = null;
  let ticket30Attempt = null;
  let ticket31Attempt = null;
  let ticket32Attempt = null;
  let ticket33Attempt = null;
  let ticket34Attempt = null;
  let ticket35Attempt = null;
  let ticket36Attempt = null;
  let ticket37Attempt = null;
  let ticket38Attempt = null;
  let ticket39Attempt = null;
  let ticket40Attempt = null;
  let ticket41Attempt = null;
  let ticket42Attempt = null;
  let ticket43Attempt = null;
  let ticket44Attempt = null;
  let ticket45Attempt = null;
  let ticket46Attempt = null;
  let ticket47Attempt = null;
  let ticket48Attempt = null;
  let ticket49Attempt = null;
  let ticket50Attempt = null;
  let ticket51Attempt = null;
  let ticket52Attempt = null;
  let ticket53Attempt = null;
  let ticket54Attempt = null;
  let ticket55Attempt = null;
  let ticket56Attempt = null;
  let ticket57Attempt = null;
  let ticket58Attempt = null;
  let ticket59Attempt = null;
  let ticket60Attempt = null;
  let ticket61Attempt = null;
  let ticket62Attempt = null;
  let ticket63Attempt = null;
  let ticket64Attempt = null;
  let ticket65Attempt = null;
  let ticket66Attempt = null;
  let ticket67Attempt = null;
  let ticket68Attempt = null;
  let ticket69Attempt = null;
  let ticket70Attempt = null;
  let ticket71Attempt = null;
  let ticket72Attempt = null;
  let ticket73Attempt = null;
  let ticket74Attempt = null;
  let ticket75Attempt = null;
  let ticket76Attempt = null;
  let ticket77Attempt = null;
  let ticket78Attempt = null;
  let ticket79Attempt = null;
  let ticket80Attempt = null;
  let ticket81Attempt = null;
  let ticket82Attempt = null;
  let ticket83Attempt = null;
  let ticket84Attempt = null;
  let ticket85Attempt = null;
  let ticket86Attempt = null;
  let ticket87Attempt = null;
  let ticket88Attempt = null;
  let ticket89Attempt = null;
  let ticket90Attempt = null;
  let ticket91Attempt = null;
  let ticket92Attempt = null;
  let ticket93Attempt = null;
  let ticket94Attempt = null;
  let ticket95Attempt = null;
  let ticket96Attempt = null;
  let ticket97Attempt = null;
  let ticket98Attempt = null;
  let ticket99Attempt = null;
  let ticket100Attempt = null;
  let ticket101Attempt = null;
  let ticket102Attempt = null;
  let ticket103Attempt = null;
  let ticket104Attempt = null;
  let ticket105Attempt = null;
  let ticket106Attempt = null;
  let ticket107Attempt = null;
  let ticket108Attempt = null;
  let ticket109Attempt = null;
  let ticket110Attempt = null;
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
  try {
    const ticket26Response = await fetch("../data/open-problem/ticket26-micro-lemma-closure.json", { cache: "no-store" });
    if (ticket26Response.ok) {
      const ticket26Payload = await ticket26Response.json();
      ticket26Attempt = (ticket26Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket26Attempt = null;
  }
  try {
    const ticket27Response = await fetch("../data/open-problem/ticket27-rank-frontier-lab.json", { cache: "no-store" });
    if (ticket27Response.ok) {
      const ticket27Payload = await ticket27Response.json();
      ticket27Attempt = (ticket27Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket27Attempt = null;
  }
  try {
    const ticket28Response = await fetch("../data/open-problem/ticket28-trichotomy-descent-lab.json", { cache: "no-store" });
    if (ticket28Response.ok) {
      const ticket28Payload = await ticket28Response.json();
      ticket28Attempt = (ticket28Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket28Attempt = null;
  }
  try {
    const ticket29Response = await fetch("../data/open-problem/ticket29-adaptive-frontier-lab.json", { cache: "no-store" });
    if (ticket29Response.ok) {
      const ticket29Payload = await ticket29Response.json();
      ticket29Attempt = (ticket29Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket29Attempt = null;
  }
  try {
    const ticket30Response = await fetch("../data/open-problem/ticket30-potential-synthesis-lab.json", { cache: "no-store" });
    if (ticket30Response.ok) {
      const ticket30Payload = await ticket30Response.json();
      ticket30Attempt = (ticket30Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket30Attempt = null;
  }
  try {
    const ticket31Response = await fetch("../data/open-problem/ticket31-feature-stutter-lab.json", { cache: "no-store" });
    if (ticket31Response.ok) {
      const ticket31Payload = await ticket31Response.json();
      ticket31Attempt = (ticket31Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket31Attempt = null;
  }
  try {
    const ticket32Response = await fetch("../data/open-problem/ticket32-stateful-measure-lab.json", { cache: "no-store" });
    if (ticket32Response.ok) {
      const ticket32Payload = await ticket32Response.json();
      ticket32Attempt = (ticket32Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket32Attempt = null;
  }
  try {
    const ticket33Response = await fetch("../data/open-problem/ticket33-global-measure-lab.json", { cache: "no-store" });
    if (ticket33Response.ok) {
      const ticket33Payload = await ticket33Response.json();
      ticket33Attempt = (ticket33Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket33Attempt = null;
  }
  try {
    const ticket34Response = await fetch("../data/open-problem/ticket34-high-branch-automaton-lab.json", { cache: "no-store" });
    if (ticket34Response.ok) {
      const ticket34Payload = await ticket34Response.json();
      ticket34Attempt = (ticket34Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket34Attempt = null;
  }
  try {
    const ticket35Response = await fetch("../data/open-problem/ticket35-limsup-mass-refinement-lab.json", { cache: "no-store" });
    if (ticket35Response.ok) {
      const ticket35Payload = await ticket35Response.json();
      ticket35Attempt = (ticket35Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket35Attempt = null;
  }
  try {
    const ticket36Response = await fetch("../data/open-problem/ticket36-null-frontier-arithmetic-lab.json", { cache: "no-store" });
    if (ticket36Response.ok) {
      const ticket36Payload = await ticket36Response.json();
      ticket36Attempt = (ticket36Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket36Attempt = null;
  }
  try {
    const ticket37Response = await fetch("../data/open-problem/ticket37-pointwise-rank-synthesis-lab.json", { cache: "no-store" });
    if (ticket37Response.ok) {
      const ticket37Payload = await ticket37Response.json();
      ticket37Attempt = (ticket37Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket37Attempt = null;
  }
  try {
    const ticket38Response = await fetch("../data/open-problem/ticket38-symbolic-frontier-extension-lab.json", { cache: "no-store" });
    if (ticket38Response.ok) {
      const ticket38Payload = await ticket38Response.json();
      ticket38Attempt = (ticket38Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket38Attempt = null;
  }
  try {
    const ticket39Response = await fetch("../data/open-problem/ticket39-phase-state-potential-lab.json", { cache: "no-store" });
    if (ticket39Response.ok) {
      const ticket39Payload = await ticket39Response.json();
      ticket39Attempt = (ticket39Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket39Attempt = null;
  }
  try {
    const ticket40Response = await fetch("../data/open-problem/ticket40-transition-closure-lab.json", { cache: "no-store" });
    if (ticket40Response.ok) {
      const ticket40Payload = await ticket40Response.json();
      ticket40Attempt = (ticket40Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket40Attempt = null;
  }
  try {
    const ticket41Response = await fetch("../data/open-problem/ticket41-rank-escape-normalization-lab.json", { cache: "no-store" });
    if (ticket41Response.ok) {
      const ticket41Payload = await ticket41Response.json();
      ticket41Attempt = (ticket41Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket41Attempt = null;
  }
  try {
    const ticket42Response = await fetch("../data/open-problem/ticket42-parametric-transition-template-lab.json", { cache: "no-store" });
    if (ticket42Response.ok) {
      const ticket42Payload = await ticket42Response.json();
      ticket42Attempt = (ticket42Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket42Attempt = null;
  }
  try {
    const ticket43Response = await fetch("../data/open-problem/ticket43-lift-constraint-measure-lab.json", { cache: "no-store" });
    if (ticket43Response.ok) {
      const ticket43Payload = await ticket43Response.json();
      ticket43Attempt = (ticket43Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket43Attempt = null;
  }
  try {
    const ticket44Response = await fetch("../data/open-problem/ticket44-feature-measure-counteredge-lab.json", { cache: "no-store" });
    if (ticket44Response.ok) {
      const ticket44Payload = await ticket44Response.json();
      ticket44Attempt = (ticket44Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket44Attempt = null;
  }
  try {
    const ticket45Response = await fetch("../data/open-problem/ticket45-symbolic-rank-clause-lab.json", { cache: "no-store" });
    if (ticket45Response.ok) {
      const ticket45Payload = await ticket45Response.json();
      ticket45Attempt = (ticket45Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket45Attempt = null;
  }
  try {
    const ticket46Response = await fetch("../data/open-problem/ticket46-stable-clause-grammar-lab.json", { cache: "no-store" });
    if (ticket46Response.ok) {
      const ticket46Payload = await ticket46Response.json();
      ticket46Attempt = (ticket46Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket46Attempt = null;
  }
  try {
    const ticket47Response = await fetch("../data/open-problem/ticket47-periodic-state-lasso-lab.json", { cache: "no-store" });
    if (ticket47Response.ok) {
      const ticket47Payload = await ticket47Response.json();
      ticket47Attempt = (ticket47Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket47Attempt = null;
  }
  try {
    const ticket48Response = await fetch("../data/open-problem/ticket48-automaton-reachability-lab.json", { cache: "no-store" });
    if (ticket48Response.ok) {
      const ticket48Payload = await ticket48Response.json();
      ticket48Attempt = (ticket48Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket48Attempt = null;
  }
  try {
    const ticket49Response = await fetch("../data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json", { cache: "no-store" });
    if (ticket49Response.ok) {
      const ticket49Payload = await ticket49Response.json();
      ticket49Attempt = (ticket49Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket49Attempt = null;
  }
  try {
    const ticket50Response = await fetch("../data/open-problem/ticket50-phase-lift-exception-lab.json", { cache: "no-store" });
    if (ticket50Response.ok) {
      const ticket50Payload = await ticket50Response.json();
      ticket50Attempt = (ticket50Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket50Attempt = null;
  }
  try {
    const ticket51Response = await fetch("../data/open-problem/ticket51-phase15-terminal-lift-lab.json", { cache: "no-store" });
    if (ticket51Response.ok) {
      const ticket51Payload = await ticket51Response.json();
      ticket51Attempt = (ticket51Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket51Attempt = null;
  }
  try {
    const ticket52Response = await fetch("../data/open-problem/ticket52-frontier-budget-lab.json", { cache: "no-store" });
    if (ticket52Response.ok) {
      const ticket52Payload = await ticket52Response.json();
      ticket52Attempt = (ticket52Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket52Attempt = null;
  }
  try {
    const ticket53Response = await fetch("../data/open-problem/ticket53-symbolic-terminal-theorem-lab.json", { cache: "no-store" });
    if (ticket53Response.ok) {
      const ticket53Payload = await ticket53Response.json();
      ticket53Attempt = (ticket53Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket53Attempt = null;
  }
  try {
    const ticket54Response = await fetch("../data/open-problem/ticket54-new-template-family-lab.json", { cache: "no-store" });
    if (ticket54Response.ok) {
      const ticket54Payload = await ticket54Response.json();
      ticket54Attempt = (ticket54Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket54Attempt = null;
  }
  try {
    const ticket55Response = await fetch("../data/open-problem/ticket55-phase5-valuation-gate-lab.json", { cache: "no-store" });
    if (ticket55Response.ok) {
      const ticket55Payload = await ticket55Response.json();
      ticket55Attempt = (ticket55Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket55Attempt = null;
  }
  try {
    const ticket56Response = await fetch("../data/open-problem/ticket56-pre-gate-projection-escape-lab.json", { cache: "no-store" });
    if (ticket56Response.ok) {
      const ticket56Payload = await ticket56Response.json();
      ticket56Attempt = (ticket56Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket56Attempt = null;
  }
  try {
    const ticket57Response = await fetch("../data/open-problem/ticket57-parametric-template-automaton-lab.json", { cache: "no-store" });
    if (ticket57Response.ok) {
      const ticket57Payload = await ticket57Response.json();
      ticket57Attempt = (ticket57Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket57Attempt = null;
  }
  try {
    const ticket58Response = await fetch("../data/open-problem/ticket58-affine-boundary-lift-lab.json", { cache: "no-store" });
    if (ticket58Response.ok) {
      const ticket58Payload = await ticket58Response.json();
      ticket58Attempt = (ticket58Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket58Attempt = null;
  }
  try {
    const ticket59Response = await fetch("../data/open-problem/ticket59-symbolic-lift-mismatch-lab.json", { cache: "no-store" });
    if (ticket59Response.ok) {
      const ticket59Payload = await ticket59Response.json();
      ticket59Attempt = (ticket59Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket59Attempt = null;
  }
  try {
    const ticket60Response = await fetch("../data/open-problem/ticket60-mixed-cylinder-separator-lab.json", { cache: "no-store" });
    if (ticket60Response.ok) {
      const ticket60Payload = await ticket60Response.json();
      ticket60Attempt = (ticket60Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket60Attempt = null;
  }
  try {
    const ticket61Response = await fetch("../data/open-problem/ticket61-symbolic-failure-offset-lab.json", { cache: "no-store" });
    if (ticket61Response.ok) {
      const ticket61Payload = await ticket61Response.json();
      ticket61Attempt = (ticket61Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket61Attempt = null;
  }
  try {
    const ticket62Response = await fetch("../data/open-problem/ticket62-mod16-transition-cover-lab.json", { cache: "no-store" });
    if (ticket62Response.ok) {
      const ticket62Payload = await ticket62Response.json();
      ticket62Attempt = (ticket62Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket62Attempt = null;
  }
  try {
    const ticket63Response = await fetch("../data/open-problem/ticket63-mod16-automaton-cover-lab.json", { cache: "no-store" });
    if (ticket63Response.ok) {
      const ticket63Payload = await ticket63Response.json();
      ticket63Attempt = (ticket63Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket63Attempt = null;
  }
  try {
    const ticket64Response = await fetch("../data/open-problem/ticket64-symbolic-mod16-transition-lab.json", { cache: "no-store" });
    if (ticket64Response.ok) {
      const ticket64Payload = await ticket64Response.json();
      ticket64Attempt = (ticket64Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket64Attempt = null;
  }
  try {
    const ticket65Response = await fetch("../data/open-problem/ticket65-start-template-chain-extinction-lab.json", { cache: "no-store" });
    if (ticket65Response.ok) {
      const ticket65Payload = await ticket65Response.json();
      ticket65Attempt = (ticket65Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket65Attempt = null;
  }
  try {
    const ticket66Response = await fetch("../data/open-problem/ticket66-complement-cover-lab.json", { cache: "no-store" });
    if (ticket66Response.ok) {
      const ticket66Payload = await ticket66Response.json();
      ticket66Attempt = (ticket66Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket66Attempt = null;
  }
  try {
    const ticket67Response = await fetch("../data/open-problem/ticket67-open-template-rank-lab.json", { cache: "no-store" });
    if (ticket67Response.ok) {
      const ticket67Payload = await ticket67Response.json();
      ticket67Attempt = (ticket67Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket67Attempt = null;
  }
  try {
    const ticket68Response = await fetch("../data/open-problem/ticket68-cycle-scc-refinement-lab.json", { cache: "no-store" });
    if (ticket68Response.ok) {
      const ticket68Payload = await ticket68Response.json();
      ticket68Attempt = (ticket68Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket68Attempt = null;
  }
  try {
    const ticket69Response = await fetch("../data/open-problem/ticket69-prefix-consumed-rank-lab.json", { cache: "no-store" });
    if (ticket69Response.ok) {
      const ticket69Payload = await ticket69Response.json();
      ticket69Attempt = (ticket69Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket69Attempt = null;
  }
  try {
    const ticket70Response = await fetch("../data/open-problem/ticket70-prefix-frontier-expansion-lab.json", { cache: "no-store" });
    if (ticket70Response.ok) {
      const ticket70Payload = await ticket70Response.json();
      ticket70Attempt = (ticket70Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket70Attempt = null;
  }
  try {
    const ticket71Response = await fetch("../data/open-problem/ticket71-stronger-frontier-coordinate-lab.json", { cache: "no-store" });
    if (ticket71Response.ok) {
      const ticket71Payload = await ticket71Response.json();
      ticket71Attempt = (ticket71Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket71Attempt = null;
  }
  try {
    const ticket72Response = await fetch("../data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json", { cache: "no-store" });
    if (ticket72Response.ok) {
      const ticket72Payload = await ticket72Response.json();
      ticket72Attempt = (ticket72Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket72Attempt = null;
  }
  try {
    const ticket73Response = await fetch("../data/open-problem/ticket73-lineage-pressure-forest-lab.json", { cache: "no-store" });
    if (ticket73Response.ok) {
      const ticket73Payload = await ticket73Response.json();
      ticket73Attempt = (ticket73Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket73Attempt = null;
  }
  try {
    const ticket74Response = await fetch("../data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json", { cache: "no-store" });
    if (ticket74Response.ok) {
      const ticket74Payload = await ticket74Response.json();
      ticket74Attempt = (ticket74Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket74Attempt = null;
  }
  try {
    const ticket75Response = await fetch("../data/open-problem/ticket75-escape-coordinate-closure-lab.json", { cache: "no-store" });
    if (ticket75Response.ok) {
      const ticket75Payload = await ticket75Response.json();
      ticket75Attempt = (ticket75Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket75Attempt = null;
  }
  try {
    const ticket76Response = await fetch("../data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json", { cache: "no-store" });
    if (ticket76Response.ok) {
      const ticket76Payload = await ticket76Response.json();
      ticket76Attempt = (ticket76Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket76Attempt = null;
  }
  try {
    const ticket77Response = await fetch("../data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json", { cache: "no-store" });
    if (ticket77Response.ok) {
      const ticket77Payload = await ticket77Response.json();
      ticket77Attempt = (ticket77Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket77Attempt = null;
  }
  try {
    const ticket78Response = await fetch("../data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json", { cache: "no-store" });
    if (ticket78Response.ok) {
      const ticket78Payload = await ticket78Response.json();
      ticket78Attempt = (ticket78Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket78Attempt = null;
  }
  try {
    const ticket79Response = await fetch("../data/open-problem/ticket79-archimedean-two-adic-rank-no-go-lab.json", { cache: "no-store" });
    if (ticket79Response.ok) {
      const ticket79Payload = await ticket79Response.json();
      ticket79Attempt = (ticket79Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket79Attempt = null;
  }
  try {
    const ticket80Response = await fetch("../data/open-problem/ticket80-least-counterexample-compactness-no-go-lab.json", { cache: "no-store" });
    if (ticket80Response.ok) {
      const ticket80Payload = await ticket80Response.json();
      ticket80Attempt = (ticket80Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket80Attempt = null;
  }
  try {
    const ticket81Response = await fetch("../data/open-problem/ticket81-mersenne-post-compensation-no-go-lab.json", { cache: "no-store" });
    if (ticket81Response.ok) {
      const ticket81Payload = await ticket81Response.json();
      ticket81Attempt = (ticket81Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket81Attempt = null;
  }
  try {
    const ticket82Response = await fetch("../data/open-problem/ticket82-fixed-mersenne-compensation-window-no-go-lab.json", { cache: "no-store" });
    if (ticket82Response.ok) {
      const ticket82Payload = await ticket82Response.json();
      ticket82Attempt = (ticket82Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket82Attempt = null;
  }
  try {
    const ticket83Response = await fetch("../data/open-problem/ticket83-mersenne-log-window-lower-bound-lab.json", { cache: "no-store" });
    if (ticket83Response.ok) {
      const ticket83Payload = await ticket83Response.json();
      ticket83Attempt = (ticket83Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket83Attempt = null;
  }
  try {
    const ticket84Response = await fetch("../data/open-problem/ticket84-two-adic-cycle-log-delay-lab.json", { cache: "no-store" });
    if (ticket84Response.ok) {
      const ticket84Payload = await ticket84Response.json();
      ticket84Attempt = (ticket84Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket84Attempt = null;
  }
  try {
    const ticket85Response = await fetch("../data/open-problem/ticket85-accessible-cycle-supremum-lab.json", { cache: "no-store" });
    if (ticket85Response.ok) {
      const ticket85Payload = await ticket85Response.json();
      ticket85Attempt = (ticket85Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket85Attempt = null;
  }
  try {
    const ticket86Response = await fetch("../data/open-problem/ticket86-coefficient-one-boundary-lab.json", { cache: "no-store" });
    if (ticket86Response.ok) {
      const ticket86Payload = await ticket86Response.json();
      ticket86Attempt = (ticket86Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket86Attempt = null;
  }
  try {
    const ticket87Response = await fetch("../data/open-problem/ticket87-two-adic-digit-run-boundary-lab.json", { cache: "no-store" });
    if (ticket87Response.ok) {
      const ticket87Payload = await ticket87Response.json();
      ticket87Attempt = (ticket87Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket87Attempt = null;
  }
  try {
    const ticket88Response = await fetch("../data/open-problem/ticket88-run-length-two-no-go-lab.json", { cache: "no-store" });
    if (ticket88Response.ok) {
      const ticket88Payload = await ticket88Response.json();
      ticket88Attempt = (ticket88Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket88Attempt = null;
  }
  try {
    const ticket89Response = await fetch("../data/open-problem/ticket89-fixed-log-golden-mean-reduction-lab.json", { cache: "no-store" });
    if (ticket89Response.ok) {
      const ticket89Payload = await ticket89Response.json();
      ticket89Attempt = (ticket89Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket89Attempt = null;
  }
  try {
    const ticket90Response = await fetch("../data/open-problem/ticket90-normalized-error-ghost-lasso-lab.json", { cache: "no-store" });
    if (ticket90Response.ok) {
      const ticket90Payload = await ticket90Response.json();
      ticket90Attempt = (ticket90Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket90Attempt = null;
  }
  try {
    const ticket91Response = await fetch("../data/open-problem/ticket91-error-tail-invariant-set-lab.json", { cache: "no-store" });
    if (ticket91Response.ok) {
      const ticket91Payload = await ticket91Response.json();
      ticket91Attempt = (ticket91Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket91Attempt = null;
  }
  try {
    const ticket92Response = await fetch("../data/open-problem/ticket92-scale-sensitive-threshold-audit.json", { cache: "no-store" });
    if (ticket92Response.ok) {
      const ticket92Payload = await ticket92Response.json();
      ticket92Attempt = (ticket92Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket92Attempt = null;
  }
  try {
    const ticket93Response = await fetch("../data/open-problem/ticket93-twin-correlation-excess-bridge.json", { cache: "no-store" });
    if (ticket93Response.ok) {
      const ticket93Payload = await ticket93Response.json();
      ticket93Attempt = (ticket93Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket93Attempt = null;
  }
  try {
    const ticket94Response = await fetch("../data/open-problem/ticket94-signed-remainder-and-goldbach-bridge.json", { cache: "no-store" });
    if (ticket94Response.ok) {
      const ticket94Payload = await ticket94Response.json();
      ticket94Attempt = (ticket94Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket94Attempt = null;
  }
  try {
    const ticket95Response = await fetch("../data/open-problem/ticket95-sharp-contamination-and-equivalence-audit.json", { cache: "no-store" });
    if (ticket95Response.ok) {
      const ticket95Payload = await ticket95Response.json();
      ticket95Attempt = (ticket95Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
    }
  } catch (error) {
    ticket95Attempt = null;
  }
  try {
    const ticket96Response = await fetch("../data/open-problem/ticket96-fourier-phase-information-audit.json", { cache: "no-store" });
    if (ticket96Response.ok) {
      const ticket96Payload = await ticket96Response.json();
      ticket96Attempt = (ticket96Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket96Attempt && ticket96Attempt.bounded_result?.audit_ref === "fourier_phase_information_audit") {
        ticket96Attempt.bounded_result.fourier_phase_information_audit = ticket96Payload.fourier_phase_information_audit || {};
      }
    }
  } catch (error) {
    ticket96Attempt = null;
  }
  try {
    const ticket97Response = await fetch("../data/open-problem/ticket97-periodic-projection-residual-audit.json", { cache: "no-store" });
    if (ticket97Response.ok) {
      const ticket97Payload = await ticket97Response.json();
      ticket97Attempt = (ticket97Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket97Attempt && ticket97Attempt.bounded_result?.audit_ref === "periodic_projection_residual_audit") {
        ticket97Attempt.bounded_result.periodic_projection_residual_audit = ticket97Payload.periodic_projection_residual_audit || {};
      }
    }
  } catch (error) {
    ticket97Attempt = null;
  }
  try {
    const ticket98Response = await fetch("../data/open-problem/ticket98-growing-modulus-leakage-audit.json", { cache: "no-store" });
    if (ticket98Response.ok) {
      const ticket98Payload = await ticket98Response.json();
      ticket98Attempt = (ticket98Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket98Attempt && ticket98Attempt.bounded_result?.audit_ref === "growing_modulus_leakage_audit") {
        ticket98Attempt.bounded_result.growing_modulus_leakage_audit = ticket98Payload.growing_modulus_leakage_audit || {};
      }
    }
  } catch (error) {
    ticket98Attempt = null;
  }
  try {
    const ticket99Response = await fetch("../data/open-problem/ticket99-out-of-sample-local-model-audit.json", { cache: "no-store" });
    if (ticket99Response.ok) {
      const ticket99Payload = await ticket99Response.json();
      ticket99Attempt = (ticket99Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket99Attempt && ticket99Attempt.bounded_result?.audit_ref === "out_of_sample_local_model_audit") {
        ticket99Attempt.bounded_result.out_of_sample_local_model_audit = ticket99Payload.out_of_sample_local_model_audit || {};
      }
    }
  } catch (error) {
    ticket99Attempt = null;
  }
  try {
    const ticket100Response = await fetch("../data/open-problem/ticket100-extended-residual-vaughan-audit.json", { cache: "no-store" });
    if (ticket100Response.ok) {
      const ticket100Payload = await ticket100Response.json();
      ticket100Attempt = (ticket100Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket100Attempt && ticket100Attempt.bounded_result?.audit_ref === "extended_residual_vaughan_audit") {
        ticket100Attempt.bounded_result.extended_residual_vaughan_audit = ticket100Payload.extended_residual_vaughan_audit || {};
      }
    }
  } catch (error) {
    ticket100Attempt = null;
  }
  try {
    const ticket101Response = await fetch("../data/open-problem/ticket101-vaughan-cutoff-energy-audit.json", { cache: "no-store" });
    if (ticket101Response.ok) {
      const ticket101Payload = await ticket101Response.json();
      ticket101Attempt = (ticket101Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket101Attempt && ticket101Attempt.bounded_result?.audit_ref === "vaughan_cutoff_energy_audit") {
        ticket101Attempt.bounded_result.vaughan_cutoff_energy_audit = ticket101Payload.vaughan_cutoff_energy_audit || {};
      }
    }
  } catch (error) {
    ticket101Attempt = null;
  }
  try {
    const ticket102Response = await fetch("../data/open-problem/ticket102-twin-dyadic-vaughan-holdout.json", { cache: "no-store" });
    if (ticket102Response.ok) {
      const ticket102Payload = await ticket102Response.json();
      ticket102Attempt = (ticket102Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket102Attempt && ticket102Attempt.bounded_result?.audit_ref === "twin_dyadic_vaughan_holdout") {
        ticket102Attempt.bounded_result.twin_dyadic_vaughan_holdout = ticket102Payload.twin_dyadic_vaughan_holdout || {};
      }
    }
  } catch (error) {
    ticket102Attempt = null;
  }
  try {
    const ticket103Response = await fetch("../data/open-problem/ticket103-twin-local-block-audit.json", { cache: "no-store" });
    if (ticket103Response.ok) {
      const ticket103Payload = await ticket103Response.json();
      ticket103Attempt = (ticket103Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket103Attempt && ticket103Attempt.bounded_result?.audit_ref === "twin_local_block_audit") {
        ticket103Attempt.bounded_result.twin_local_block_audit = ticket103Payload.twin_local_block_audit || {};
      }
    }
  } catch (error) {
    ticket103Attempt = null;
  }
  try {
    const ticket104Response = await fetch("../data/open-problem/ticket104-twin-typeii-mobius-anatomy.json", { cache: "no-store" });
    if (ticket104Response.ok) {
      const ticket104Payload = await ticket104Response.json();
      ticket104Attempt = (ticket104Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket104Attempt && ticket104Attempt.bounded_result?.audit_ref === "twin_typeii_mobius_anatomy") {
        ticket104Attempt.bounded_result.twin_typeii_mobius_anatomy = ticket104Payload.twin_typeii_mobius_anatomy || {};
      }
    }
  } catch (error) {
    ticket104Attempt = null;
  }
  try {
    const ticket105Response = await fetch("../data/open-problem/ticket105-twin-centered-progression-discrepancy.json", { cache: "no-store" });
    if (ticket105Response.ok) {
      const ticket105Payload = await ticket105Response.json();
      ticket105Attempt = (ticket105Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket105Attempt && ticket105Attempt.bounded_result?.audit_ref === "twin_centered_progression_discrepancy") {
        ticket105Attempt.bounded_result.twin_centered_progression_discrepancy = ticket105Payload.twin_centered_progression_discrepancy || {};
      }
    }
  } catch (error) {
    ticket105Attempt = null;
  }
  try {
    const ticket106Response = await fetch("../data/open-problem/ticket106-twin-modulus-grouped-dispersion.json", { cache: "no-store" });
    if (ticket106Response.ok) {
      const ticket106Payload = await ticket106Response.json();
      ticket106Attempt = (ticket106Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket106Attempt && ticket106Attempt.bounded_result?.audit_ref === "twin_modulus_grouped_dispersion") {
        ticket106Attempt.bounded_result.twin_modulus_grouped_dispersion = ticket106Payload.twin_modulus_grouped_dispersion || {};
      }
    }
  } catch (error) {
    ticket106Attempt = null;
  }
  try {
    const ticket107Response = await fetch("../data/open-problem/ticket107-twin-sparse-tail-recombination.json", { cache: "no-store" });
    if (ticket107Response.ok) {
      const ticket107Payload = await ticket107Response.json();
      ticket107Attempt = (ticket107Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket107Attempt && ticket107Attempt.bounded_result?.audit_ref === "twin_sparse_tail_recombination") {
        ticket107Attempt.bounded_result.twin_sparse_tail_recombination = ticket107Payload.twin_sparse_tail_recombination || {};
      }
    }
  } catch (error) {
    ticket107Attempt = null;
  }
  try {
    const ticket108Response = await fetch("../data/open-problem/ticket108-twin-joint-equivalence-smoothing.json", { cache: "no-store" });
    if (ticket108Response.ok) {
      const ticket108Payload = await ticket108Response.json();
      ticket108Attempt = (ticket108Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket108Attempt && ticket108Attempt.bounded_result?.audit_ref === "twin_joint_equivalence_smoothing") {
        ticket108Attempt.bounded_result.twin_joint_equivalence_smoothing = ticket108Payload.twin_joint_equivalence_smoothing || {};
      }
    }
  } catch (error) {
    ticket108Attempt = null;
  }
  try {
    const ticket109Response = await fetch("../data/open-problem/ticket109-twin-spectral-phase-audit.json", { cache: "no-store" });
    if (ticket109Response.ok) {
      const ticket109Payload = await ticket109Response.json();
      ticket109Attempt = (ticket109Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket109Attempt && ticket109Attempt.bounded_result?.audit_ref === "twin_spectral_phase_audit") {
        ticket109Attempt.bounded_result.twin_spectral_phase_audit = ticket109Payload.twin_spectral_phase_audit || {};
      }
    }
  } catch (error) {
    ticket109Attempt = null;
  }
  try {
    const ticket110Response = await fetch("../data/open-problem/ticket110-twin-rational-arc-budget.json", { cache: "no-store" });
    if (ticket110Response.ok) {
      const ticket110Payload = await ticket110Response.json();
      ticket110Attempt = (ticket110Payload.attempts || []).find((item) => item.problem_id === problemId) || null;
      if (ticket110Attempt && ticket110Attempt.bounded_result?.audit_ref === "twin_rational_arc_budget") {
        ticket110Attempt.bounded_result.twin_rational_arc_budget = ticket110Payload.twin_rational_arc_budget || {};
      }
    }
  } catch (error) {
    ticket110Attempt = null;
  }
  render(payload, problem, proofOrCounterexampleTicket, ticket17Attempt, ticket18Attempt, ticket19Attempt, ticket20Attempt, ticket21Attempt, ticket22Attempt, ticket23Attempt, ticket24Attempt, ticket25Attempt, ticket26Attempt, ticket27Attempt, ticket28Attempt, ticket29Attempt, ticket30Attempt, ticket31Attempt, ticket32Attempt, ticket33Attempt, ticket34Attempt, ticket35Attempt, ticket36Attempt, ticket37Attempt, ticket38Attempt, ticket39Attempt, ticket40Attempt, ticket41Attempt, ticket42Attempt, ticket43Attempt, ticket44Attempt, ticket45Attempt, ticket46Attempt, ticket47Attempt, ticket48Attempt, ticket49Attempt, ticket50Attempt, ticket51Attempt, ticket52Attempt, ticket53Attempt, ticket54Attempt, ticket55Attempt, ticket56Attempt, ticket57Attempt, ticket58Attempt, ticket59Attempt, ticket60Attempt, ticket61Attempt, ticket62Attempt, ticket63Attempt, ticket64Attempt, ticket65Attempt, ticket66Attempt, ticket67Attempt, ticket68Attempt, ticket69Attempt, ticket70Attempt, ticket71Attempt, ticket72Attempt, ticket73Attempt, ticket74Attempt, ticket75Attempt, ticket76Attempt, ticket77Attempt, ticket78Attempt, ticket79Attempt, ticket80Attempt, ticket81Attempt, ticket82Attempt, ticket83Attempt, ticket84Attempt, ticket85Attempt, ticket86Attempt, ticket87Attempt, ticket88Attempt, ticket89Attempt, ticket90Attempt, ticket91Attempt, ticket92Attempt, ticket93Attempt, ticket94Attempt, ticket95Attempt, ticket96Attempt, ticket97Attempt, ticket98Attempt, ticket99Attempt, ticket100Attempt, ticket101Attempt, ticket102Attempt, ticket103Attempt, ticket104Attempt, ticket105Attempt, ticket106Attempt, ticket107Attempt, ticket108Attempt, ticket109Attempt, ticket110Attempt);
}

main().catch((error) => {
  document.querySelector("#finiteEvidence").innerHTML = `<div class="proof-note is-error">${escapeHtml(error.message)}</div>`;
});
