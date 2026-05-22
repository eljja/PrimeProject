const path = require("node:path");
const fs = require("node:fs");
const { pathToFileURL } = require("node:url");
const { chromium } = loadPlaywright();

async function main() {
  const root = path.resolve(__dirname, "..");
  const url = pathToFileURL(path.join(root, "index.html")).href;
  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  let browser = null;
  const errors = [];
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
      evolutionDelta: document.querySelector("#evolutionDelta").textContent,
      maturityStages: document.querySelectorAll("#evolutionImpact .maturity-stage").length,
      impactChanges: document.querySelectorAll("#evolutionImpact .impact-change-list div").length,
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
      readinessPanel: document.querySelector("#readiness-panel").textContent,
      readinessCards: document.querySelectorAll("#readinessDimensions .readiness-card").length,
      readinessActions: document.querySelectorAll("#readinessActions li").length,
      evidencePanel: document.querySelector("#evidence-panel").textContent,
      evidenceGates: document.querySelectorAll("#evidenceGateRows .evidence-row").length,
      evidenceArtifacts: document.querySelectorAll("#evidenceArtifactRows .evidence-row").length,
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
      evidenceTop: Math.round(document.querySelector("#evidence-panel").getBoundingClientRect().top),
    }));

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
  }

  if (errors.length > 0) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
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
    metrics.maturityStages < 5 ||
    metrics.impactChanges < 4 ||
    metrics.deltaTracks < 4 ||
    metrics.claimLanes < 4 ||
    !metrics.evolutionPanel.includes("Project Evolution") ||
    !metrics.evolutionImpact.includes("Change Dashboard") ||
    !metrics.evolutionDelta.includes("Research Delta") ||
    !metrics.evolutionDelta.includes("10M live compute") ||
    !metrics.evolutionDelta.includes("controlled grid + null + replication") ||
    !metrics.evolutionDelta.includes("Real-world generator attribution") ||
    !metrics.evolutionDelta.includes("Bitcoin wallet/library attribution") ||
    !metrics.evolutionImpact.includes("Baseline promotion plan") ||
    !metrics.evolutionImpact.includes("Claim ledger") ||
    !metrics.evolutionImpact.includes("Artifact lineage") ||
    !metrics.evolutionImpact.includes("Decision protocol") ||
    !metrics.evolutionImpact.includes("Falsification battery") ||
    !metrics.evolutionImpact.includes("Null calibration") ||
    !metrics.evolutionImpact.includes("Replication audit") ||
    !metrics.evolutionImpact.includes("13 artifacts") ||
    !metrics.evolutionPanel.includes("collection matrix") ||
    !metrics.evolutionPanel.includes("Sample power") ||
    !metrics.evolutionPanel.includes("Provenance") ||
    !metrics.evolutionPanel.includes("Evidence pack")
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
    !metrics.attributionFirstRow.includes("all")
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
    !metrics.baselineRegistrySummary.includes("Registered") ||
    metrics.baselineRegistryRows < 5 ||
    metrics.collectionMatrixRows < 4 ||
    !metrics.collectionMatrixStatus.includes("10") ||
    metrics.collectionPowerRows < 5 ||
    !metrics.collectionPowerStatus.includes("coarse") ||
    !metrics.collectionPowerSummary.includes("multinomial") ||
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
    !metrics.baselinePromotionSummary.includes("9,028")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.readinessCards < 4 ||
    metrics.readinessActions < 2 ||
    !metrics.readinessPanel.includes("Research Readiness") ||
    !metrics.readinessPanel.includes("prototype_ready")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.evidenceGates < 10 ||
    metrics.evidenceArtifacts < 13 ||
    metrics.claimLedgerRows < 5 ||
    metrics.artifactLineageRows < 5 ||
    metrics.artifactLineagePaths < 10 ||
    metrics.artifactLineageNodes < 10 ||
    metrics.decisionProtocolRows < 4 ||
    metrics.falsificationRows < 5 ||
    !metrics.evidencePanel.includes("Evidence Pack") ||
    !metrics.evidencePanel.includes("Claim Ledger") ||
    !metrics.evidencePanel.includes("Artifact Lineage") ||
    !metrics.evidencePanel.includes("Decision Protocol") ||
    !metrics.evidencePanel.includes("Falsification Battery") ||
    !metrics.evidencePanel.includes("promote_real_world_generator_attribution") ||
    !metrics.evidencePanel.includes("promote_bitcoin_nonce_risk_attribution") ||
    !metrics.decisionProtocolSummary.includes("2 allowed") ||
    !metrics.falsificationSummary.includes("0 fail") ||
    !metrics.evidencePanel.includes("claim_promotion_guard") ||
    !metrics.evidencePanel.includes("controlled_synthetic_only") ||
    !metrics.evidencePanel.includes("reproducible") ||
    !metrics.artifactLineageSummary.includes("15 nodes") ||
    !metrics.evidencePanel.includes("real_world_generator_attribution") ||
    !metrics.evidencePanel.includes("bitcoin_nonce_risk_attribution") ||
    !metrics.evidencePanel.includes("blocked") ||
    !metrics.claimLedgerSummary.includes("3 allowed") ||
    !metrics.evidencePanel.includes("provenance_gate") ||
    !metrics.evidencePanel.includes("provenance_audit_gate") ||
    !metrics.evidencePanel.includes("baseline_acceptance_gate") ||
    !metrics.evidencePanel.includes("promotion_plan_gate") ||
    !metrics.evidencePanel.includes("provenance_requirements") ||
    !metrics.evidencePanel.includes("provenance_audit") ||
    !metrics.evidencePanel.includes("baseline_acceptance") ||
    !metrics.evidencePanel.includes("baseline_promotion_plan") ||
    !metrics.evidencePanel.includes("null_calibration") ||
    !metrics.evidencePanel.includes("replication_audit") ||
    !metrics.evidencePanel.includes("public_demo_only")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({ errors, metrics }, null, 2));
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
