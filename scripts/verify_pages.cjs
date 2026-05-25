const path = require("node:path");
const fs = require("node:fs");
const http = require("node:http");
const { chromium } = loadPlaywright();

async function main() {
  const root = path.resolve(__dirname, "..");
  const publicData = loadPublicData(root);
  const serverHandle = await startStaticServer(root);
  const url = serverHandle.url;
  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  let browser = null;
  const errors = [];
  const dataResponses = [];
  let metrics = null;

  try {
    browser = await chromium.launch({
      headless: true,
      executablePath: fs.existsSync(chromePath) ? chromePath : undefined,
    });

    const page = await browser.newPage({
      viewport: { width: 1440, height: 1000 },
      deviceScaleFactor: 1,
    });
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("console", (message) => {
      if (message.type() === "error") errors.push(message.text());
    });
    page.on("response", (response) => {
      const responseUrl = response.url();
      if (responseUrl.includes("/data/") && responseUrl.endsWith(".json")) {
        dataResponses.push({ url: responseUrl, status: response.status() });
      }
      if (response.status() >= 400) {
        errors.push(`${response.status()} ${responseUrl}`);
      }
    });

    await page.goto(url, { waitUntil: "networkidle" });
    await page.click("[data-generator='rejection']");
    await page.click("[data-generator='wheel30_next']");
    await page.locator("#limitRange").evaluate((input) => {
      const min = 20000;
      const max = 10000000;
      input.value = String(Math.round((Math.log(80000 / min) / Math.log(max / min)) * 1000));
      input.dispatchEvent(new Event("input", { bubbles: true }));
    });
    await page.click("#runExperiment");
    await page.waitForTimeout(600);
    await page.waitForSelector("#snapshotButtons button");
    await page.waitForFunction(() =>
      [...document.querySelectorAll(".snapshot-grid img")].every((image) => image.complete && image.naturalWidth > 0),
    );
    await page.click("#snapshotButtons button:nth-child(2)");
    await page.waitForFunction(() => document.querySelector("#snapshotSummary").textContent.includes("10M"));
    await page.waitForFunction(() =>
      [...document.querySelectorAll(".snapshot-grid img")].every((image) => image.complete && image.naturalWidth > 0),
    );
    await page.click("#runPrediction");
    await page.waitForFunction(() => document.querySelectorAll("#predictionRows tr").length >= 8);
    await page.click("[data-scroll-target='evolution-panel']");
    await page.waitForFunction(() => document.querySelectorAll("#evolutionTimeline .evolution-step").length >= 8);
    await page.waitForFunction(() => {
      const rect = document.querySelector("#evolution-panel").getBoundingClientRect();
      const headerHeight = document.querySelector(".topbar").getBoundingClientRect().height;
      return rect.top >= headerHeight - 20 && rect.top <= headerHeight + 28;
    });
    await page.click("[data-scroll-target='attribution-panel']");
    await page.waitForFunction(() => document.querySelectorAll("#attributionProfileRows tr").length >= 3);
    await page.waitForFunction(() => {
      const rect = document.querySelector("#attribution-panel").getBoundingClientRect();
      const headerHeight = document.querySelector(".topbar").getBoundingClientRect().height;
      return rect.top >= headerHeight - 20 && rect.top <= headerHeight + 28;
    });
    await page.click("[data-scroll-target='readiness-panel']");
    await page.waitForFunction(() => document.querySelectorAll("#readinessDimensions .readiness-card").length >= 4);
    await page.click("[data-scroll-target='evidence-panel']");
    await page.waitForFunction(() => document.querySelectorAll("#evidenceGateRows .evidence-row").length >= 5);
    await page.waitForFunction(() => {
      const rect = document.querySelector("#evidence-panel").getBoundingClientRect();
      const headerHeight = document.querySelector(".topbar").getBoundingClientRect().height;
      return rect.top >= headerHeight - 20 && rect.top <= headerHeight + 28;
    });
    await page.screenshot({
      path: path.join(root, "data", "conjecture_lab_desktop.png"),
      fullPage: true,
    });

    metrics = await page.evaluate(() => ({
      pageProtocol: window.location.protocol,
      dataSourceBadge: document.querySelector("#dataSourceBadge").textContent,
      title: document.title,
      primeCount: document.querySelector("#primeCount").textContent,
      drift: document.querySelector("#driftMetric").textContent,
      canvasWidth: document.querySelector("#gapCanvas").getBoundingClientRect().width,
      canvasHeight: document.querySelector("#gapCanvas").getBoundingClientRect().height,
      activeClaim: document.querySelector("#activeClaim").textContent,
      snapshotButtons: document.querySelectorAll("#snapshotButtons button").length,
      snapshotSummary: document.querySelector("#snapshotSummary").textContent,
      snapshotImagesReady: [...document.querySelectorAll(".snapshot-grid img")].every(
        (image) => image.complete && image.naturalWidth > 0,
      ),
      predictionRows: document.querySelectorAll("#predictionRows tr").length,
      predictionMetrics: document.querySelector("#predictionMetrics").textContent,
      evolutionPanel: document.querySelector("#evolution-panel").textContent,
      evolutionImpact: document.querySelector("#evolutionImpact").textContent,
      evolutionSpine: document.querySelector("#evolutionSpine").textContent,
      evolutionDelta: document.querySelector("#evolutionDelta").textContent,
      evolutionSummary: document.querySelector("#evolutionSummary").textContent,
      maturityStages: document.querySelectorAll("#evolutionImpact .maturity-stage").length,
      strategyCards: document.querySelectorAll("#evolutionImpact .strategy-card").length,
      releaseNodes: document.querySelectorAll("#evolutionImpact .release-node").length,
      impactChanges: document.querySelectorAll("#evolutionImpact .impact-change-list div").length,
      evidenceFlowNodes: document.querySelectorAll("#evolutionDelta .evidence-flow-node").length,
      evidenceSpineCards: document.querySelectorAll("#evolutionSpine .spine-card").length,
      deltaTracks: document.querySelectorAll("#evolutionDelta .delta-track").length,
      claimLanes: document.querySelectorAll("#evolutionDelta .claim-lane").length,
      evolutionSteps: document.querySelectorAll("#evolutionTimeline .evolution-step").length,
      evolutionNodes: document.querySelectorAll("#evolutionMap rect").length,
      evolutionGaps: document.querySelectorAll("#evolutionGaps div").length,
      attributionSummary: document.querySelector("#attributionSummary").textContent,
      attributionRows: document.querySelectorAll("#attributionProfileRows tr").length,
      attributionSvgCells: document.querySelectorAll("#attributionGridSvg rect").length,
      attributionHeader: document.querySelector(".attribution-table thead").textContent,
      attributionFirstRow: document.querySelector("#attributionProfileRows tr").textContent,
      nullCalibrationSummary: document.querySelector("#nullCalibrationSummary").textContent,
      nullCalibrationRows: document.querySelectorAll("#nullCalibrationRows .null-row").length,
      replicationAuditSummary: document.querySelector("#replicationAuditSummary").textContent,
      replicationAuditRows: document.querySelectorAll("#replicationAuditRows .replication-row").length,
      bitcoinPanel: document.querySelector("#bitcoin-panel").textContent,
      fingerprintPanel: document.querySelector("#fingerprint-panel").textContent,
      baselinePanel: document.querySelector("#baseline-panel").textContent,
      baselineRegistrySummary: document.querySelector("#baselineRegistrySummary").textContent,
      baselineRegistryRows: document.querySelectorAll("#baselineRegistryRows tr").length,
      collectionMatrixRows: document.querySelectorAll("#collectionMatrixRows .collection-row").length,
      collectionMatrixStatus: document.querySelector("#collectionMatrixStatus").textContent,
      collectionPowerSummary: document.querySelector("#collectionPowerSummary").textContent,
      collectionPowerRows: document.querySelectorAll("#collectionPowerRows .power-row").length,
      collectionPowerStatus: document.querySelector("#collectionPowerStatus").textContent,
      provenanceSummary: document.querySelector("#provenanceSummary").textContent,
      provenanceRows: document.querySelectorAll("#provenanceRows .provenance-row").length,
      provenanceStatus: document.querySelector("#provenanceStatus").textContent,
      provenanceAuditSummary: document.querySelector("#provenanceAuditSummary").textContent,
      provenanceAuditRows: document.querySelectorAll("#provenanceAuditRows .provenance-row").length,
      provenanceAuditStatus: document.querySelector("#provenanceAuditStatus").textContent,
      baselineAcceptanceSummary: document.querySelector("#baselineAcceptanceSummary").textContent,
      baselineAcceptanceRows: document.querySelectorAll("#baselineAcceptanceRows .provenance-row").length,
      baselineAcceptanceStatus: document.querySelector("#baselineAcceptanceStatus").textContent,
      baselinePromotionSummary: document.querySelector("#baselinePromotionSummary").textContent,
      baselinePromotionRows: document.querySelectorAll("#baselinePromotionRows .provenance-row").length,
      baselinePromotionStatus: document.querySelector("#baselinePromotionStatus").textContent,
      collectionHandoffStatus: document.querySelector("#collectionHandoffStatus").textContent,
      collectionHandoffSummary: document.querySelector("#collectionHandoffSummary").textContent,
      collectionHandoffRows: document.querySelectorAll("#collectionHandoffRows .handoff-row").length,
      collectionHandoffContract: document.querySelector("#collectionHandoffContract").textContent,
      collectionSubmissionContractStatus: document.querySelector("#collectionSubmissionContractStatus").textContent,
      collectionSubmissionContractSummary: document.querySelector("#collectionSubmissionContractSummary").textContent,
      collectionSubmissionContractRows: document.querySelectorAll("#collectionSubmissionContractRows .handoff-row").length,
      collectionSubmissionLintStatus: document.querySelector("#collectionSubmissionLintStatus").textContent,
      collectionSubmissionLintSummary: document.querySelector("#collectionSubmissionLintSummary").textContent,
      collectionSubmissionLintRows: document.querySelectorAll("#collectionSubmissionLintRows .intake-row").length,
      collectionFixtureAuditStatus: document.querySelector("#collectionFixtureAuditStatus").textContent,
      collectionFixtureAuditSummary: document.querySelector("#collectionFixtureAuditSummary").textContent,
      collectionFixtureAuditRows: document.querySelectorAll("#collectionFixtureAuditRows .fixture-row").length,
      collectionIntakeStatus: document.querySelector("#collectionIntakeStatus").textContent,
      collectionIntakeSummary: document.querySelector("#collectionIntakeSummary").textContent,
      collectionIntakeRows: document.querySelectorAll("#collectionIntakeRows .intake-row").length,
      readinessPanel: document.querySelector("#readiness-panel").textContent,
      readinessCards: document.querySelectorAll("#readinessDimensions .readiness-card").length,
      readinessActions: document.querySelectorAll("#readinessActions li").length,
      classifierStatus: document.querySelector("#classifierStatus").textContent,
      classifierSummary: document.querySelector("#classifierSummary").textContent,
      classifierLabels: document.querySelectorAll("#classifierLabels .classifier-label-row").length,
      evidencePanel: document.querySelector("#evidence-panel").textContent,
      evidenceSummary: document.querySelector("#evidenceSummary").textContent,
      requiredEvidenceRows: document.querySelector("#requiredEvidenceRows").textContent,
      evidenceGates: document.querySelectorAll("#evidenceGateRows .evidence-row").length,
      evidenceArtifacts: document.querySelectorAll("#evidenceArtifactRows .evidence-row").length,
      requiredEvidenceCount: document.querySelectorAll("#requiredEvidenceRows .required-row").length,
      claimLedgerRows: document.querySelectorAll("#claimLedgerRows .claim-row").length,
      claimLedgerSummary: document.querySelector("#claimLedgerSummary").textContent,
      artifactLineageSummary: document.querySelector("#artifactLineageSummary").textContent,
      artifactLineageRows: document.querySelectorAll("#artifactLineageRows > div").length,
      artifactLineagePaths: document.querySelectorAll("#artifactLineageMap path").length,
      artifactLineageNodes: document.querySelectorAll("#artifactLineageMap rect").length,
      decisionProtocolSummary: document.querySelector("#decisionProtocolSummary").textContent,
      decisionProtocolRows: document.querySelectorAll("#decisionProtocolRows .decision-row").length,
      falsificationSummary: document.querySelector("#falsificationSummary").textContent,
      falsificationRows: document.querySelectorAll("#falsificationRows .falsification-row").length,
      publicationConsistencySummary: document.querySelector("#publicationConsistencySummary").textContent,
      publicationConsistencyRows: document.querySelectorAll("#publicationConsistencyRows .consistency-row").length,
      evidenceTop: Math.round(document.querySelector("#evidence-panel").getBoundingClientRect().top),
    }));
    metrics.fetchedDataJson = dataResponses.filter((response) => response.status >= 200 && response.status < 300).length;

    const mobile = await browser.newPage({
      viewport: { width: 390, height: 900 },
      isMobile: true,
    });
    await mobile.goto(url, { waitUntil: "networkidle" });
    await mobile.screenshot({
      path: path.join(root, "data", "conjecture_lab_mobile.png"),
      fullPage: true,
    });
  } finally {
    if (browser) await browser.close();
    await closeServer(serverHandle.server);
  }

  if (errors.length > 0) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  const expected = buildExpectedPublicText(publicData);
  if (metrics.pageProtocol !== "http:" || metrics.fetchedDataJson < 20) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (!metrics.dataSourceBadge.includes("Public JSON data")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  const exactPublicChecks = [
    [metrics.evolutionSummary, expected.evolution.scale],
    [metrics.evolutionSummary, expected.evolution.snapshots],
    [metrics.evolutionSummary, expected.evolution.controlledSignal],
    [metrics.evolutionSummary, expected.evolution.generatorBaselines],
    [metrics.evolutionSummary, expected.evolution.collection],
    [metrics.evolutionSummary, expected.evolution.evidence],
    [metrics.evolutionSummary, expected.evolution.claimLevel],
    [metrics.readinessPanel, expected.readiness.overall],
    [metrics.readinessPanel, expected.readiness.simToReal],
    [metrics.evidenceSummary, expected.evidence.claimLevel],
    [metrics.evidenceSummary, expected.evidence.failedGates],
    [metrics.evidenceSummary, expected.evidence.artifacts],
    [metrics.claimLedgerSummary, expected.claimLedger],
    [metrics.artifactLineageSummary, expected.lineage],
    [metrics.decisionProtocolSummary, expected.decision],
    [metrics.falsificationSummary, expected.falsification],
    [metrics.publicationConsistencySummary, expected.consistency],
  ];
  const missingPublicChecks = exactPublicChecks
    .filter(([actual, expectedText]) => !String(actual).includes(expectedText))
    .map(([actual, expectedText]) => ({ expected: expectedText, actual }));
  if (missingPublicChecks.length > 0) {
    console.error(JSON.stringify({ errors, missingPublicChecks, metrics }, null, 2));
    process.exit(1);
  }
  if (metrics.snapshotButtons < 2 || !metrics.snapshotImagesReady) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (metrics.predictionRows < 8 || !metrics.predictionMetrics.includes("Observed next")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.evolutionSteps < 8 ||
    metrics.evolutionNodes < 15 ||
    metrics.evolutionGaps < 2 ||
    metrics.strategyCards < 3 ||
    metrics.releaseNodes < 5 ||
    metrics.impactChanges < 5 ||
    metrics.evidenceSpineCards < 5 ||
    metrics.claimLanes < 4 ||
    !metrics.evolutionPanel.includes("Project Evolution") ||
    !metrics.evolutionSummary.includes("Generator baselines") ||
    !metrics.evolutionSummary.includes("0") ||
    !metrics.evolutionSummary.includes("1 public control") ||
    !metrics.evolutionSummary.includes("2 profiles") ||
    !metrics.evolutionSummary.includes("5,000 null iterations") ||
    !metrics.evolutionImpact.includes("Project Logic") ||
    !metrics.evolutionImpact.includes("Supported") ||
    !metrics.evolutionImpact.includes("Not supported yet") ||
    !metrics.evolutionImpact.includes("Next decisive test") ||
    !metrics.evolutionImpact.includes("Visual Change Trail") ||
    !metrics.evolutionImpact.includes("Scale lift") ||
    !metrics.evolutionImpact.includes("Publication guardrails") ||
    !metrics.evolutionImpact.includes("11 guard checks") ||
    !metrics.evolutionSpine.includes("Evidence Spine") ||
    !metrics.evolutionSpine.includes("Sim-to-Real") ||
    !metrics.evolutionSpine.includes("fixture audit") ||
    !metrics.evolutionSpine.includes("21 checked artifacts") ||
    !metrics.evolutionSpine.includes("publication consistency") ||
    !metrics.evolutionDelta.includes("Claim Boundaries") ||
    !metrics.evolutionDelta.includes("controlled grid + null + replication") ||
    !metrics.evolutionDelta.includes("Real-world generator attribution") ||
    !metrics.evolutionDelta.includes("Bitcoin wallet/library attribution") ||
    !metrics.evolutionImpact.includes("Controlled signal") ||
    !metrics.evolutionImpact.includes("Real-world gate") ||
    !metrics.evolutionImpact.includes("Submission discipline") ||
    !metrics.evolutionImpact.includes("Publication guardrail") ||
    !metrics.evolutionPanel.includes("Crypto-classifier baseline") ||
    !metrics.evolutionPanel.includes("Collection handoff") ||
    !metrics.evolutionPanel.includes("Collection intake") ||
    !metrics.evolutionPanel.includes("collection matrix") ||
    !metrics.evolutionPanel.includes("Sample power") ||
    !metrics.evolutionPanel.includes("Provenance") ||
    !metrics.evolutionPanel.includes("Evidence pack") ||
    !metrics.evolutionPanel.includes("Publication consistency")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.attributionRows < 3 ||
    metrics.attributionSvgCells < 3 ||
    !metrics.attributionSummary.includes("Random baseline") ||
    !metrics.attributionHeader.includes("Controlled p")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.nullCalibrationRows < 5 ||
    !metrics.nullCalibrationSummary.includes("5,000") ||
    !metrics.nullCalibrationSummary.includes("gap_only") ||
    !metrics.attributionFirstRow.includes(expected.attribution.topControlledProfile)
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.replicationAuditRows < 5 ||
    !metrics.replicationAuditSummary.includes("8") ||
    !metrics.replicationAuditSummary.includes("gap_only") ||
    !metrics.replicationAuditSummary.includes("controlled_synthetic_only")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (!metrics.bitcoinPanel.includes("secp256k1") || !metrics.bitcoinPanel.includes("Repeated ECDSA r")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (!metrics.fingerprintPanel.includes("Residue drift") || !metrics.fingerprintPanel.includes("Gap context")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    !metrics.baselinePanel.includes("known-good") ||
    !metrics.baselinePanel.includes("fingerprint distance") ||
    !metrics.baselinePanel.includes("Real-World Collection Matrix") ||
    !metrics.baselinePanel.includes("Claim gate") ||
    !metrics.baselinePanel.includes("Collection Power") ||
    !metrics.baselinePanel.includes("4,514") ||
    !metrics.baselinePanel.includes("Provenance Gate") ||
    !metrics.baselinePanel.includes("Provenance Audit") ||
    !metrics.baselinePanel.includes("Baseline Acceptance") ||
    !metrics.baselinePanel.includes("Promotion Plan") ||
    !metrics.baselinePanel.includes("Collection Intake") ||
    !metrics.baselinePanel.includes("Submission Contract") ||
    !metrics.baselinePanel.includes("Submission Lint") ||
    !metrics.baselinePanel.includes("Fixture Audit") ||
    !metrics.baselineRegistrySummary.includes("Registered") ||
    metrics.baselineRegistryRows < 5 ||
    metrics.collectionMatrixRows < 4 ||
    !metrics.collectionMatrixStatus.includes("10") ||
    metrics.collectionPowerRows < 5 ||
    !metrics.collectionPowerStatus.includes("coarse") ||
    !metrics.collectionPowerSummary.includes("multinomial") ||
    !metrics.collectionPowerSummary.includes("Sensitivity") ||
    !metrics.baselinePanel.includes("rsa-prime sensitivity") ||
    metrics.provenanceRows < 4 ||
    !metrics.provenanceStatus.includes("35") ||
    !metrics.provenanceSummary.includes("Required fields") ||
    metrics.provenanceAuditRows < 4 ||
    !metrics.provenanceAuditStatus.includes("4") ||
    !metrics.provenanceAuditSummary.includes("Forbidden") ||
    metrics.baselineAcceptanceRows < 6 ||
    !metrics.baselineAcceptanceStatus.includes("0 accepted") ||
    !metrics.baselineAcceptanceSummary.includes("Minimum") ||
    metrics.baselinePromotionRows < 2 ||
    !metrics.baselinePromotionStatus.includes("2") ||
    !metrics.baselinePromotionSummary.includes("9,028") ||
    metrics.collectionHandoffRows < 4 ||
    !metrics.collectionHandoffStatus.includes("2 P0") ||
    !metrics.collectionHandoffSummary.includes("9,028") ||
    !metrics.collectionHandoffSummary.includes("controlled_synthetic_only") ||
    !metrics.collectionHandoffContract.includes("private material stays local") ||
    metrics.collectionSubmissionContractRows < 4 ||
    !metrics.collectionSubmissionContractStatus.includes("10 templates") ||
    !metrics.collectionSubmissionContractSummary.includes("14") ||
    !metrics.collectionSubmissionContractSummary.includes("forbidden") ||
    metrics.collectionSubmissionLintRows < 4 ||
    !metrics.collectionSubmissionLintStatus.includes("waiting") ||
    !metrics.collectionSubmissionLintSummary.includes("10") ||
    !metrics.collectionSubmissionLintSummary.includes("awaiting_submission") ||
    metrics.collectionFixtureAuditRows < 9 ||
    !metrics.collectionFixtureAuditStatus.includes("pass") ||
    !metrics.collectionFixtureAuditSummary.includes("9") ||
    !metrics.collectionFixtureAuditSummary.includes("0") ||
    metrics.collectionIntakeRows < 4 ||
    !metrics.collectionIntakeStatus.includes("0 accepted") ||
    !metrics.collectionIntakeStatus.includes("10 blocked") ||
    !metrics.collectionIntakeSummary.includes("10") ||
    !metrics.collectionIntakeSummary.includes("2")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.readinessCards < 4 ||
    metrics.readinessActions < 2 ||
    !metrics.readinessPanel.includes("Research Readiness") ||
    !metrics.readinessPanel.includes("prototype_ready") ||
    !metrics.readinessPanel.includes("61.4%") ||
    !metrics.readinessPanel.includes("0 attribution-ready") ||
    !metrics.readinessPanel.includes("cap scaffold_ready from 75.0%") ||
    !metrics.readinessPanel.includes("Crypto-Classifier Baseline") ||
    metrics.classifierLabels < 3 ||
    !metrics.classifierStatus.includes("controlled synthetic only") ||
    !metrics.classifierSummary.includes("12") ||
    !metrics.classifierSummary.includes("33.3%")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.evidenceGates < 11 ||
    metrics.evidenceArtifacts < 17 ||
    metrics.requiredEvidenceCount < 5 ||
    metrics.claimLedgerRows < 5 ||
    metrics.artifactLineageRows < 5 ||
    metrics.artifactLineagePaths < 10 ||
    metrics.artifactLineageNodes < 10 ||
    metrics.decisionProtocolRows < 4 ||
    metrics.falsificationRows < 5 ||
    metrics.publicationConsistencyRows < 5 ||
    !metrics.evidencePanel.includes("Evidence Pack") ||
    !metrics.evidencePanel.includes("Claim Ledger") ||
    !metrics.evidencePanel.includes("Artifact Lineage") ||
    !metrics.evidencePanel.includes("Decision Protocol") ||
    !metrics.evidencePanel.includes("Falsification Battery") ||
    !metrics.evidencePanel.includes("Publication Consistency") ||
    !metrics.evidencePanel.includes("real_world_boundary_consistent") ||
    !metrics.evidencePanel.includes("required_evidence_covers_blockers") ||
    !metrics.evidencePanel.includes("promote_real_world_generator_attribution") ||
    !metrics.evidencePanel.includes("promote_bitcoin_nonce_risk_attribution") ||
    !metrics.decisionProtocolSummary.includes("2 allowed") ||
    !metrics.falsificationSummary.includes("0 fail") ||
    !metrics.evidencePanel.includes("claim_promotion_guard") ||
    !metrics.evidencePanel.includes("controlled_synthetic_only") ||
    !metrics.evidencePanel.includes("reproducible") ||
    !metrics.artifactLineageSummary.includes("23 nodes") ||
    !metrics.evidencePanel.includes("real_world_generator_attribution") ||
    !metrics.evidencePanel.includes("bitcoin_nonce_risk_attribution") ||
    !metrics.evidencePanel.includes("blocked") ||
    !metrics.claimLedgerSummary.includes("3 allowed") ||
    !metrics.evidencePanel.includes("provenance_gate") ||
    !metrics.evidencePanel.includes("provenance_audit_gate") ||
    !metrics.evidencePanel.includes("baseline_acceptance_gate") ||
    !metrics.evidencePanel.includes("collection_intake_gate") ||
    !metrics.evidencePanel.includes("promotion_plan_gate") ||
    !metrics.evidencePanel.includes("provenance_requirements") ||
    !metrics.evidencePanel.includes("provenance_audit") ||
    !metrics.evidencePanel.includes("baseline_acceptance") ||
    !metrics.evidencePanel.includes("baseline_promotion_plan") ||
    !metrics.evidencePanel.includes("collection_handoff") ||
    !metrics.evidencePanel.includes("collection_submission_contract") ||
    !metrics.evidencePanel.includes("collection_submission_lint") ||
    !metrics.evidencePanel.includes("collection_fixture_audit") ||
    !metrics.evidencePanel.includes("collection_fixture_audit_gate") ||
    !metrics.evidencePanel.includes("claim_language_audit") ||
    !metrics.evidencePanel.includes("claim_language_gate") ||
    !metrics.evidencePanel.includes("88 guarded") ||
    !metrics.evidencePanel.includes("quality pass") ||
    !metrics.evidencePanel.includes("collection_intake") ||
    !metrics.evidencePanel.includes("null_calibration") ||
    !metrics.evidencePanel.includes("replication_audit") ||
    !metrics.evidencePanel.includes("feature_vectors") ||
    !metrics.evidencePanel.includes("classifier_report") ||
    !metrics.evidencePanel.includes("public_demo_only") ||
    !metrics.requiredEvidenceRows.includes("real_world_labelled_feature_vectors") ||
    !metrics.requiredEvidenceRows.includes("two_accepted_real_baselines") ||
    !metrics.requiredEvidenceRows.includes("accepted_collection_intake") ||
    !metrics.requiredEvidenceRows.includes("missing")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({ errors, metrics }, null, 2));
}

function loadPublicData(root) {
  return {
    evolution: readJson(root, "data/project_evolution.json"),
    readiness: readJson(root, "data/research_readiness.json"),
    evidence: readJson(root, "data/evidence_pack.json"),
    claimLedger: readJson(root, "data/claim_ledger.json"),
    lineage: readJson(root, "data/artifact_lineage.json"),
    decision: readJson(root, "data/decision_protocol.json"),
    falsification: readJson(root, "data/falsification_battery.json"),
    consistency: readJson(root, "data/publication_consistency.json"),
    attribution: readJson(root, "data/attribution_confound_grid.json"),
  };
}

function readJson(root, relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function buildExpectedPublicText(data) {
  const metrics = data.evolution.metrics || {};
  const readiness = data.readiness;
  const simToReal = readiness.dimensions?.sim_to_real || {};
  const evidence = data.evidence;
  const attributionProfiles = Object.entries(data.attribution.summary?.profiles || {});
  const topControlled = attributionProfiles.sort(
    (left, right) => (right[1].mean_controlled_accuracy || 0) - (left[1].mean_controlled_accuracy || 0),
  )[0];
  const failedGates = (evidence.publication_gates || []).filter((gate) => !gate.passed);
  return {
    attribution: {
      topControlledProfile: topControlled ? topControlled[0] : "",
    },
    evolution: {
      scale: formatCompact(metrics.live_compute_limit || 0),
      snapshots: `${(metrics.precomputed_snapshot_limits || []).map(formatCompact).join(", ")} snapshots`,
      controlledSignal:
        `${formatNumber((metrics.robust_controlled_profiles || []).length)} profiles` +
        `${formatNumber(metrics.null_calibration_iterations || 0)} null iterations`,
      generatorBaselines:
        `${formatNumber(metrics.available_real_baselines || 0)}` +
        `${formatNumber(metrics.public_control_baselines || 0)} public control`,
      collection:
        `${formatNumber(metrics.intake_accepted || 0)}` +
        `${formatNumber(metrics.intake_blocked || 0)} intake blockers`,
      evidence:
        `${formatNumber(metrics.checksummed_artifacts || 0)}` +
        `${formatNumber(metrics.falsification_checks || 0)} falsification · ` +
        `${formatNumber(metrics.publication_consistency_checks || 0)} consistency`,
      claimLevel:
        `${formatClaimLevel(metrics.publication_claim_level)}` +
        `${formatNumber(metrics.blocking_gaps || 0)} blocking gaps`,
    },
    readiness: {
      overall: `${formatPercent(readiness.overall?.score || 0)}${readiness.overall?.label || "unknown"}`,
      simToReal:
        `${formatNumber(simToReal.available_count || 0)} attribution-ready, ` +
        `${formatNumber(simToReal.public_control_count || 0)} public controls, ` +
        `${formatNumber(simToReal.planned_count || 0)} planned.` +
        (simToReal.readiness_cap
          ? ` cap ${simToReal.readiness_cap.max_label || "scaffold_ready"} from ${formatPercent(
              simToReal.raw_score || simToReal.score || 0,
            )}.`
          : ""),
    },
    evidence: {
      claimLevel: `${evidence.claim_level?.level || "unknown"}${evidence.claim_level?.statement || ""}`,
      failedGates:
        `${formatNumber(failedGates.length)}` +
        `${formatNumber(evidence.claim_level?.failed_high_gate_count || 0)} high`,
      artifacts: `${formatNumber(evidence.artifact_count || (evidence.artifacts || []).length)}checksummed`,
    },
    claimLedger:
      `${formatNumber(data.claimLedger.summary?.allowed_count || 0)} allowed / ` +
      `${formatNumber(data.claimLedger.summary?.blocked_count || 0)} blocked`,
    lineage:
      `${formatNumber(data.lineage.summary?.node_count || 0)} nodes / ` +
      `${formatNumber(data.lineage.summary?.edge_count || 0)} edges`,
    decision:
      `${formatNumber(data.decision.summary?.allowed_count || 0)} allowed / ` +
      `${formatNumber(data.decision.summary?.blocked_count || 0)} blocked`,
    falsification:
      `${formatNumber(data.falsification.summary?.pass_count || 0)} pass / ` +
      `${formatNumber(data.falsification.summary?.fail_count || 0)} fail`,
    consistency:
      `${data.consistency.summary?.status || "unknown"} · ` +
      `${formatNumber(data.consistency.summary?.pass_count || 0)} pass / ` +
      `${formatNumber(data.consistency.summary?.fail_count || 0)} fail`,
  };
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function formatCompact(value) {
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

function formatPercent(value) {
  return `${((Number(value) || 0) * 100).toFixed(1)}%`;
}

function formatClaimLevel(level) {
  const value = String(level || "unknown");
  if (value === "public_demo_only") return "public demo";
  if (value === "controlled_synthetic_only") return "synthetic only";
  return value.replace(/_/g, " ");
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    const fallback = findBundledPlaywright();
    if (fallback) return require(fallback);
    throw error;
  }
}

function findBundledPlaywright() {
  const candidates = [
    process.env.PLAYWRIGHT_MODULE_PATH,
    path.join(
      process.env.USERPROFILE || "",
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      ".pnpm",
    ),
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    if (candidate.endsWith("playwright")) return candidate;
    for (const entry of fs.readdirSync(candidate)) {
      if (entry.startsWith("playwright@")) {
        const packagePath = path.join(candidate, entry, "node_modules", "playwright");
        if (fs.existsSync(packagePath)) return packagePath;
      }
    }
  }
  return null;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

function startStaticServer(root) {
  const server = http.createServer((request, response) => {
    try {
      const requestUrl = new URL(request.url || "/", "http://127.0.0.1");
      const pathname = decodeURIComponent(requestUrl.pathname);
      const relativePath = pathname === "/" ? "index.html" : pathname.replace(/^\/+/, "");
      const filePath = path.resolve(root, relativePath);
      if (filePath !== root && !filePath.startsWith(`${root}${path.sep}`)) {
        response.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
        response.end("Forbidden");
        return;
      }
      if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
        response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
        response.end("Not found");
        return;
      }
      response.writeHead(200, {
        "Content-Type": contentType(filePath),
        "Cache-Control": "no-store",
      });
      fs.createReadStream(filePath).pipe(response);
    } catch (error) {
      response.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      response.end(String(error && error.message ? error.message : error));
    }
  });

  return new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => {
      server.off("error", reject);
      const address = server.address();
      resolve({ server, url: `http://127.0.0.1:${address.port}/index.html` });
    });
  });
}

function closeServer(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}

function contentType(filePath) {
  const extension = path.extname(filePath).toLowerCase();
  return (
    {
      ".css": "text/css; charset=utf-8",
      ".html": "text/html; charset=utf-8",
      ".js": "application/javascript; charset=utf-8",
      ".json": "application/json; charset=utf-8",
      ".png": "image/png",
      ".svg": "image/svg+xml; charset=utf-8",
    }[extension] || "application/octet-stream"
  );
}
