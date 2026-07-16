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
  const openProblemSource = fs.readFileSync(path.join(root, "assets", "open-problems.js"), "utf8");
  const priorityLoad = openProblemSource.indexOf("const priorityLoads = await Promise.all([loadTicket127Attempt(), loadTicket126Attempt(), loadTicket125Attempt()]);");
  const priorityRender = openProblemSource.indexOf("render(payload, problem);", priorityLoad);
  const historicalLoad = openProblemSource.indexOf("const labResponse = await fetch", priorityRender);
  if (!(priorityLoad >= 0 && priorityLoad < priorityRender && priorityRender < historicalLoad)) {
    errors.push("TICKET127/TICKET126/TICKET125 priority render must precede historical ticket loading");
  }
  for (const page of ["riemann", "collatz", "goldbach", "twin-prime"]) {
    const source = fs.readFileSync(path.join(root, "open-problems", `${page}.html`), "utf8");
    if (!source.includes("open-problems.js?v=20260717-ticket127-priority")) {
      errors.push(`${page}: missing TICKET127 priority cache key`);
    }
  }

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
    await page.click("[data-scroll-target='research-atlas-panel']");
    await page.waitForFunction(() => document.querySelectorAll("#atlasContributionGrid .atlas-contribution").length >= 4);
    await page.waitForFunction(() => document.querySelectorAll("#atlasProofGrid .atlas-proof-card").length >= 4);
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
      languageSwitchButtons: document.querySelectorAll("[data-lang-set]").length,
      languageNote: document.querySelector(".language-note")?.textContent || "",
      sideNavText: document.querySelector(".side-nav").textContent,
      proofWorkbenchHref: document.querySelector(".side-nav a[href='open-problems/index.html']")?.textContent || "",
      riemannNavHref: document.querySelector(".side-nav a[href='open-problems/riemann.html']")?.textContent || "",
      collatzNavHref: document.querySelector(".side-nav a[href='open-problems/collatz.html']")?.textContent || "",
      goldbachNavHref: document.querySelector(".side-nav a[href='open-problems/goldbach.html']")?.textContent || "",
      twinPrimeNavHref:
        document.querySelector(".side-nav a[href='open-problems/twin-prime.html']")?.textContent || "",
      controlBeforeNotes:
        document.querySelector(".insight-panel").firstElementChild?.classList.contains("control-rail") || false,
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
      atlasPanel: document.querySelector("#research-atlas-panel").textContent,
      atlasContributions: document.querySelectorAll("#atlasContributionGrid .atlas-contribution").length,
      atlasLadderSteps: document.querySelectorAll("#atlasEvidenceLadder .atlas-ladder-step").length,
      atlasProofCards: document.querySelectorAll("#atlasProofGrid .atlas-proof-card").length,
      atlasNextCards: document.querySelectorAll("#atlasNextSteps .atlas-next-card").length,
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

    metrics.openProblemPages = [];
    const proofHub = await browser.newPage({
      viewport: { width: 1280, height: 900 },
      deviceScaleFactor: 1,
    });
    await proofHub.goto(new URL("open-problems/index.html", url).toString(), { waitUntil: "networkidle" });
    metrics.proofHub = await proofHub.evaluate(() => ({
      title: document.title,
      heading: document.querySelector("h1").textContent,
      linkCount: document.querySelectorAll(".proof-card-link").length,
      links: [...document.querySelectorAll(".proof-card-link")].map((link) => link.getAttribute("href")),
      boundary: document.body.textContent,
    }));
    for (const [problemId, href] of [
      ["riemann", "open-problems/riemann.html"],
      ["collatz", "open-problems/collatz.html"],
      ["goldbach", "open-problems/goldbach.html"],
      ["twin-prime", "open-problems/twin-prime.html"],
    ]) {
      const problemPage = await browser.newPage({
        viewport: { width: 1280, height: 900 },
        deviceScaleFactor: 1,
      });
      await problemPage.goto(new URL(href, url).toString(), { waitUntil: "networkidle" });
      await problemPage.waitForFunction(() => document.querySelectorAll(".proof-metric").length >= 3);
      metrics.openProblemPages.push(
        await problemPage.evaluate((expectedProblemId) => ({
          problemId: expectedProblemId,
          title: document.title,
          heading: document.querySelector("#problemTitle").textContent,
          status: document.querySelector("#claimStatus").textContent,
          metricCount: document.querySelectorAll(".proof-metric").length,
          proofVerdictText: document.querySelector("#proofVerdict").textContent,
          actualProofRunnerText: document.querySelector("#actualProofAttemptRunner").textContent,
          actualProofRunnerSteps: document.querySelectorAll("#actualProofAttemptRunner .runner-step").length,
          proofOrCounterexampleText: document.querySelector("#proofOrCounterexampleLab")?.textContent || "",
          proofOrCounterexampleCards: document.querySelectorAll("#proofOrCounterexampleLab .poc-grid section").length,
          candidateLemmaText: document.querySelector("#candidateLemmaWorkbench").textContent,
          candidateLemmaCards: document.querySelectorAll("#candidateLemmaWorkbench .lemma-card").length,
          machineSearchText: document.querySelector("#machineProofSearchTrials").textContent,
          machineSearchCards: document.querySelectorAll("#machineProofSearchTrials .search-trial").length,
          formalUpgradeText: document.querySelector("#formalUpgradeMatrix").textContent,
          formalUpgradeRows: document.querySelectorAll("#formalUpgradeMatrix .upgrade-row").length,
          proofKernelText: document.querySelector("#proofKernelRoadmap").textContent,
          proofKernelSteps: document.querySelectorAll("#proofKernelRoadmap .kernel-step").length,
          formalKernelAuditText: document.querySelector("#formalKernelContractAudit").textContent,
          formalKernelAuditRows: document.querySelectorAll("#formalKernelContractAudit .kernel-audit-row").length,
          invalidShortcutText: document.querySelector("#invalidProofShortcutSuite").textContent,
          invalidShortcutCards: document.querySelectorAll("#invalidProofShortcutSuite .shortcut-card").length,
          aiSolverText: document.querySelector("#aiSolverFrontier").textContent,
          aiSolverSteps: document.querySelectorAll("#aiSolverFrontier .ai-step").length,
          aiBreakthroughText: document.querySelector("#aiBreakthroughProgram").textContent,
          aiBreakthroughAnchors: document.querySelectorAll("#aiBreakthroughProgram .breakthrough-anchor").length,
          aiBreakthroughExperiments: document.querySelectorAll("#aiBreakthroughProgram .breakthrough-experiment").length,
          aiProofForgeText: document.querySelector("#aiProofForge").textContent,
          aiProofForgeLemmaCards: document.querySelectorAll("#aiProofForge .proof-forge-lemma").length,
          aiProofForgeBlueprintSteps: document.querySelectorAll("#aiProofForge .proof-forge-blueprint-next em").length,
          aiProofForgeCegisCandidates: document.querySelectorAll("#aiProofForge .proof-forge-cegis-candidates article").length,
          aiProofForgeCegisRanking: document.querySelectorAll("#aiProofForge .proof-forge-cegis-ranking article").length,
          aiProofForgeTicketSections: document.querySelectorAll("#aiProofForge .proof-forge-ticket-grid section").length,
          aiProofForgeTicketProtocol: document.querySelectorAll("#aiProofForge .proof-forge-ticket-protocol article").length,
          aiProofForgeExperiments: document.querySelectorAll("#aiProofForge .proof-forge-experiment").length,
          aiProofForgeMutations: document.querySelectorAll("#aiProofForge .proof-forge-mutation").length,
          aiProofForgeRunbook: document.querySelectorAll("#aiProofForge .proof-forge-runbook-step").length,
          aiProofForgeScorecard: document.querySelectorAll("#aiProofForge .proof-forge-score").length,
          aiProofForgeSynthesis: document.querySelectorAll("#aiProofForge .proof-forge-synthesis-card").length,
          aiProofForgePortfolio: document.querySelectorAll("#aiProofForge .proof-forge-ranked-track").length,
          proofRouteTriageText: document.querySelector("#proofRouteTriage").textContent,
          proofRouteCards: document.querySelectorAll("#proofRouteTriage .route-card").length,
          decisiveTheoremText: document.querySelector("#decisiveTheoremSpec").textContent,
          decisiveTheoremSections: document.querySelectorAll("#decisiveTheoremSpec .theorem-spec-grid section").length,
          decisiveSubgoalText: document.querySelector("#decisiveTheoremSubgoals").textContent,
          decisiveSubgoalCards: document.querySelectorAll("#decisiveTheoremSubgoals .subgoal-card").length,
          decisiveTicketText: document.querySelector("#decisiveTheoremAttackTickets").textContent,
          decisiveTicketCards: document.querySelectorAll("#decisiveTheoremAttackTickets .attack-ticket-card").length,
          breakthroughText: document.querySelector("#proofBreakthroughAgenda").textContent,
          breakthroughCards: document.querySelectorAll("#proofBreakthroughAgenda .breakthrough-card").length,
          certificateText: document.querySelector("#certificatePanel").textContent,
          proofAttemptText: document.querySelector("#proofAttempt").textContent,
          proofMapText: document.querySelector("#proofMap").textContent,
          proofStatusGateText: document.querySelector("#proofStatusGate").textContent,
          proofExecutionText: document.querySelector("#proofExecutionProtocol").textContent,
          proofExecutionStages: document.querySelectorAll("#proofExecutionProtocol .execution-stage").length,
          proofFrontierText: document.querySelector("#proofFrontierProbe").textContent,
          knownBarrierText: document.querySelector("#knownBarrierAudit").textContent,
          knownBarrierCards: document.querySelectorAll("#knownBarrierAudit .barrier-card").length,
          formalReplayText: document.querySelector("#formalReplayPackage").textContent,
          formalReplayArtifacts: document.querySelectorAll("#formalReplayPackage .replay-artifacts > div").length,
          proofReviewText: document.querySelector("#proofReviewDocket").textContent,
          proofReviewCards: document.querySelectorAll("#proofReviewDocket .review-card").length,
          proofReductionText: document.querySelector("#proofReductionContract").textContent,
          proofReductionPartials: document.querySelectorAll("#proofReductionContract .reduction-partials article").length,
          proofCandidateText: document.querySelector("#proofCandidateIntake").textContent,
          proofCandidateTests: document.querySelectorAll("#proofCandidateIntake .candidate-list article").length,
          proofExecutionLogText: document.querySelector("#proofAttemptExecutionLog").textContent,
          proofExecutionLogCards: document.querySelectorAll("#proofAttemptExecutionLog .execution-log-card").length,
          proofDagText: document.querySelector("#proofObligationDag").textContent,
          proofDagNodes: document.querySelectorAll("#proofObligationDag .dag-node").length,
          proofDagEdges: document.querySelectorAll("#proofObligationDag .dag-edge-list article").length,
          formalSkeletonText: document.querySelector("#formalSkeletonAudit").textContent,
          formalSkeletonFiles: document.querySelectorAll("#formalSkeletonAudit .skeleton-file").length,
          formalContractText: document.querySelector("#formalContract").textContent,
          milestoneQueueText: document.querySelector("#milestoneQueue").textContent,
          milestoneCount: document.querySelectorAll("#milestoneQueue .milestone-card").length,
          decisiveLemmaText: document.querySelector("#decisiveLemmaLab").textContent,
          blockedClaimCount: document.querySelectorAll("#blockedClaims span").length,
          text: document.body.textContent,
        }), problemId),
      );
      await problemPage.close();
    }
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
  if (metrics.languageSwitchButtons < 2 || !metrics.languageNote.includes("Language Coverage")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (!metrics.dataSourceBadge.includes("Public JSON data")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (
    metrics.proofHub?.heading !== "Proof Workbench" ||
    metrics.proofHub?.linkCount !== 6 ||
    !metrics.proofHub?.links.includes("riemann.html") ||
    !metrics.proofHub?.links.includes("collatz.html") ||
    !metrics.proofHub?.links.includes("goldbach.html") ||
    !metrics.proofHub?.links.includes("twin-prime.html") ||
    !metrics.proofHub?.links.includes("../docs/open-problem-research-consolidation-2026-07-10.md") ||
    !metrics.proofHub?.links.includes("../docs/proof-or-counterexample-program.md") ||
    !metrics.proofHub?.boundary.includes("Canonical Research Audit") ||
    !metrics.proofHub?.boundary.includes("Proof or Counterexample Program") ||
    !metrics.proofHub?.boundary.includes("not present a conjecture as solved")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  const missingTicket71Checks = metrics.openProblemPages.flatMap((page) => {
    const checks = [];
    const requireText = (label, text) => {
      if (!page.proofOrCounterexampleText.includes(text)) checks.push(`${page.problemId}: ${label}`);
    };
    requireText("ticket71 title", "Ticket 71 stronger frontier coordinates");
    requireText("ticket71 result table", "Stronger coordinate result");
    if (page.problemId === "collatz") {
      requireText("ticket71 coordinate table", "Coordinate family comparison");
      requireText("ticket71 status", "bounded_transition_separator_found_but_infinite_bridge_open");
      requireText("ticket71 full-word family", "base_fullword_residue65536");
      requireText("ticket71 full-word frontier", "254,488");
      requireText("ticket71 compact mixed keys", "22,219");
      requireText("ticket71 tail12 family", "base_tail12_residue65536");
      requireText("ticket71 next theorem", "InfiniteFrontierCoordinateLiftClosureOrChain");
    }
    requireText("ticket72 title", "Ticket 72 infinite frontier lift closure");
    requireText("ticket72 result table", "Lift-closure result");
    if (page.problemId === "collatz") {
      requireText("ticket72 status", "persistent_mixed_key_lift_chain_pressure_observed_no_resolution");
      requireText("ticket72 second lift rows", "36,848");
      requireText("ticket72 second lift open pressure", "6,857");
      requireText("ticket72 second lift reentry", "4,142");
      requireText("ticket72 third probe reentry", "6,448");
      requireText("ticket72 best compact", "base_tail12_residue65536");
      requireText("ticket72 full-word guard", "base_fullword_residue65536");
      requireText("ticket72 coordinate comparison", "Second-lift coordinate comparison");
      requireText("ticket72 next theorem", "CompactMixedKeyInvariantOrPersistentLiftChain");
    }
    requireText("ticket73 title", "Ticket 73 lineage-constrained pressure forest");
    requireText("ticket73 result table", "Lineage audit");
    if (page.problemId === "collatz") {
      requireText("ticket73 status", "strict reentry tree extinct at fifth lift for selected roots no global conclusion");
      requireText("ticket73 roots", "4,142");
      requireText("ticket73 third reentry", "12,911");
      requireText("ticket73 fourth reentry", "2,873");
      requireText("ticket73 fifth extinction", "45,968");
      requireText("ticket73 fifth strict reentry", "0");
      requireText("ticket73 strict decision", "exact_finite_extinction");
      requireText("ticket73 next theorem", "CoverageCertificateAndAllDepthReentryTreeDecision");
    }
    requireText("ticket74 title", "Ticket 74 coverage leakage and escaping pressure forest");
    requireText("ticket74 result table", "Coverage leakage audit");
    if (page.problemId === "collatz") {
      requireText("ticket74 status", "strict cover leakage and sixth pressure persistence observed no global resolution");
      requireText("ticket74 mixed keys", "20,752");
      requireText("ticket74 selected key coverage", "0.039%");
      requireText("ticket74 fifth escapes", "15,696");
      requireText("ticket74 sixth pressure", "78,315");
      requireText("ticket74 next theorem", "GlobalCoverageCertificateOrEscapingPressureForestDecision");
    }
    requireText("ticket75 title", "Ticket 75 fixed-coordinate closure audit");
    requireText("ticket75 result table", "Coordinate closure audit");
    if (page.problemId === "collatz") {
      requireText("ticket75 status", "all tested finite preoutcome coordinates leak or cycle no global resolution");
      requireText("ticket75 coordinate table", "Compression versus state growth");
      requireText("ticket75 coordinate count", "8");
      requireText("ticket75 replay fifth", "15,696");
      requireText("ticket75 replay sixth", "78,315");
      requireText("ticket75 coarse novelty", "11");
      requireText("ticket75 rich novelty", "77,998");
      requireText("ticket75 unbounded block", "Unbounded reference blocked");
      requireText("ticket75 next theorem", "SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath");
    } else {
      requireText("ticket75 transfer boundary", "method transfer only");
    }
    requireText("ticket76 title", "Ticket 76 symbolic boundary recurrence");
    requireText("ticket76 result table", "Boundary recurrence audit");
    if (page.problemId === "collatz") {
      requireText("ticket76 status", "symbolic formula verified fixed precision closure refuted on tested precisions no global resolution");
      requireText("ticket76 precision table", "Fixed precision versus four-bit lookahead");
      requireText("ticket76 rows", "297,104");
      requireText("ticket76 formula failures", "formula failures0");
      requireText("ticket76 q5 collisions", "165");
      requireText("ticket76 q9 collisions", "1,536");
      requireText("ticket76 valuation rule", "v_new = d + v2(A + h*u)");
      requireText("ticket76 next theorem", "ReachableBoundaryRestrictionOrTwoAdicPressurePath");
    } else {
      requireText("ticket76 transfer boundary", "method transfer only");
    }
    requireText("ticket77 title", "Ticket 77 fixed-prefix boundary orbit");
    requireText("ticket77 result table", "Fixed-prefix boundary orbit audit");
    if (page.problemId === "collatz") {
      requireText("ticket77 status", "fixed prefix boundary orbit classified no collatz resolution");
      requireText("ticket77 orbit table", "Inverse-16 periodic orbit audit");
      requireText("ticket77 sources", "18,569");
      requireText("ticket77 maximum steps", "maximum strict-pressure steps15");
      requireText("ticket77 exact chain", "Exact proof chain");
      requireText("ticket77 ghost", "-1/3");
      requireText("ticket77 correction", "Equality rollback correction");
      requireText("ticket77 discarded inference", "Discarded inference");
      requireText("ticket77 next theorem", "ChangingPrefixNaturalAdmissibilityRank");
    } else {
      requireText("ticket77 transfer boundary", "method transfer only");
    }
    requireText("ticket78 title", "Ticket 78 finite-cylinder admissibility no-go");
    requireText("ticket78 result table", "Finite-cylinder no-go audit");
    if (page.problemId === "collatz") {
      requireText("ticket78 status", "finite two adic natural separator refuted exactly no collatz resolution");
      requireText("ticket78 composition table", "All positive valuation compositions through S=16");
      requireText("ticket78 words", "65,535");
      requireText("ticket78 representatives", "262,140");
      requireText("ticket78 rejected families", "Rejected finite separator families");
      requireText("ticket78 literature", "Bernstein and Lagarias");
      requireText("ticket78 novelty", "Novelty boundary");
      requireText("ticket78 next theorem", "ArchimedeanTwoAdicCoupledDescent");
    } else {
      requireText("ticket78 transfer boundary", "method transfer only");
    }
    requireText("ticket79 title", "Ticket 79 Archimedean-two-adic rank no-go");
    requireText("ticket79 result table", "TICKET79 rank no-go audit");
    if (page.problemId === "collatz") {
      requireText("ticket79 status", "bounded archimedean two adic one step rank refuted exactly no collatz resolution");
      requireText("ticket79 expansion", "Exact expansion family E_(m,1)");
      requireText("ticket79 contraction", "Exact nonterminal contraction family D_r → 5");
      requireText("ticket79 expansion cases", "1,024");
      requireText("ticket79 replays", "131,584");
      requireText("ticket79 rejected", "Rejected one-step rank families");
      requireText("ticket79 next theorem", "MinimalCounterexampleValuationSurplusContradiction");
      requireText("ticket79 equivalence", "Equivalence warning");
    } else {
      requireText("ticket79 transfer boundary", "method transfer only");
    }
    requireText("ticket80 title", "Ticket 80 least-counterexample compactness no-go");
    requireText("ticket80 result table", "TICKET80 compactness no-go audit");
    if (page.problemId === "collatz") {
      requireText("ticket80 status", "least counterexample finite prefix compactness refuted exactly no collatz resolution");
      requireText("ticket80 finite witnesses", "Arbitrarily large finite non-descent witnesses");
      requireText("ticket80 dual topology", "Dual-topology escape x_H → -1 in Z_2");
      requireText("ticket80 cases", "2,560");
      requireText("ticket80 replays", "656,640");
      requireText("ticket80 criterion", "Positive-integer stabilization criterion");
      requireText("ticket80 rejected", "Rejected finite-prefix and compactness routes");
      requireText("ticket80 next theorem", "LeastCounterexampleUniformHeightBound");
    } else {
      requireText("ticket80 transfer boundary", "method transfer only");
    }
    requireText("ticket81 title", "Ticket 81 Mersenne first-compensation no-go");
    requireText("ticket81 result table", "TICKET81 Mersenne compensation audit");
    if (page.problemId === "collatz") {
      requireText("ticket81 status", "mersenne first post compensation descent refuted exactly no collatz resolution");
      requireText("ticket81 exact formulas", "Exact expansion and compensation formulas");
      requireText("ticket81 cases", "1,023");
      requireText("ticket81 replays", "523,776");
      requireText("ticket81 classification", "Complete first-compensation classification");
      requireText("ticket81 rejected", "Rejected single-compensation routes");
      requireText("ticket81 next theorem", "MersenneAdaptiveCompensationWindow");
    } else {
      requireText("ticket81 transfer boundary", "method transfer only");
    }
    requireText("ticket82 title", "Ticket 82 fixed Mersenne compensation-window no-go");
    requireText("ticket82 table", "TICKET82 fixed-window no-go audit");
    if (page.problemId === "collatz") {
      requireText("ticket82 status", "fixed mersenne compensation window refuted exactly no collatz resolution");
      requireText("ticket82 symbolic", "Exact symbolic exponent family");
      requireText("ticket82 progressions", "Explicit exponent progressions");
      requireText("ticket82 states", "8,385");
      requireText("ticket82 transitions", "8,256");
      requireText("ticket82 rejected", "Rejected constant-window routes");
      requireText("ticket82 next", "MersenneGrowingWindowDescent");
    } else {
      requireText("ticket82 transfer boundary", "method transfer only");
    }
    requireText("ticket83 title", "Ticket 83 Mersenne half-log delay lower bound");
    requireText("ticket83 table", "TICKET83 logarithmic delay audit");
    if (page.problemId === "collatz") {
      requireText("ticket83 theorem", "Exact half-log theorem");
      requireText("ticket83 states", "33,150");
      requireText("ticket83 sequence", "Explicit delayed exponent sequence");
      requireText("ticket83 rejected", "Rejected sub-half-log window routes");
      requireText("ticket83 next", "MersenneLogWindowDichotomy");
    } else {
      requireText("ticket83 transfer", "method transfer only");
    }
    requireText("ticket84 title", "Ticket 84 accessible 2-adic cycle and two-thirds log bound");
    requireText("ticket84 table", "TICKET84 two-adic cycle audit");
    if (page.problemId === "collatz") {
      requireText("ticket84 cycle", "Accessible completion cycle");
      requireText("ticket84 precision", "386");
      requireText("ticket84 states", "33,150");
      requireText("ticket84 lifts", "Positive Hensel-lifted exponent certificates");
      requireText("ticket84 next", "AccessibleCycleCoefficientSupremum");
    } else {
      requireText("ticket84 transfer", "method transfer only");
    }
    requireText("ticket85 title", "Ticket 85 accessible cycle coefficient supremum");
    requireText("ticket85 table", "TICKET85 cycle supremum audit");
    if (page.problemId === "collatz") {
      requireText("ticket85 family", "Exact accessible cycle family");
      requireText("ticket85 supremum", "Supremum one, not attained");
      requireText("ticket85 lifts", "32,895");
      requireText("ticket85 states", "33,150");
      requireText("ticket85 next", "CoefficientOneBoundary");
    } else {
      requireText("ticket85 transfer", "method transfer only");
    }
    requireText("ticket86 title", "Ticket 86 infinite coefficient-one Mersenne delay");
    requireText("ticket86 table", "TICKET86 coefficient-one boundary audit");
    if (page.problemId === "collatz") {
      requireText("ticket86 reduction", "Exact fixed-log reduction");
      requireText("ticket86 prefixes", "1,023");
      requireText("ticket86 top bits", "499");
      requireText("ticket86 precision", "1,027");
      requireText("ticket86 states", "16,877");
      requireText("ticket86 next", "TwoAdicDigitRunBoundary");
    } else {
      requireText("ticket86 transfer", "method transfer only");
    }
    requireText("ticket87 title", "Ticket 87 two-adic digit runs and additive-one delay");
    requireText("ticket87 table", "TICKET87 digit-run boundary audit");
    if (page.problemId === "collatz") {
      requireText("ticket87 fixed log", "Fixed two-adic logarithm");
      requireText("ticket87 prefix bits", "262,143");
      requireText("ticket87 top bits", "131,307");
      requireText("ticket87 positive runs", "65,368");
      requireText("ticket87 record", "Finite zero-run record certificates");
      requireText("ticket87 next", "TwoAdicRunLengthTwoInfinitude");
    } else {
      requireText("ticket87 transfer", "method transfer only");
    }
    requireText("ticket88 title", "Ticket 88 run-length-two inference no-go");
    requireText("ticket88 table", "TICKET88 run-length-two no-go audit");
    if (page.problemId === "collatz") {
      requireText("ticket88 countermodel", "Explicit no-00 countermodel");
      requireText("ticket88 complement", "Exact complement orbit");
      requireText("ticket88 observed", "32,753");
      requireText("ticket88 discarded", "Discarded promotion routes");
      requireText("ticket88 next", "FixedLogGoldenMeanExclusion");
    } else {
      requireText("ticket88 transfer", "method transfer only");
    }
    requireText("ticket89 title", "Ticket 89 fixed-log golden-mean valuation reduction");
    requireText("ticket89 table", "TICKET89 fixed-log reduction audit");
    if (page.problemId === "collatz") {
      requireText("ticket89 equivalence", "Exact pattern-valuation equivalence");
      requireText("ticket89 transcendence", "Transcendence no-go");
      requireText("ticket89 pairs", "32,727");
      requireText("ticket89 excess", "8,159");
      requireText("ticket89 next", "FixedLogValuationExcessFiveInfinitude");
    } else {
      requireText("ticket89 transfer", "method transfer only");
    }
    requireText("ticket90 title", "Ticket 90 normalized-error ghost lasso no-go");
    requireText("ticket90 table", "TICKET90 normalized-error audit");
    if (page.problemId === "collatz") {
      requireText("ticket90 recurrence", "Exact normalized-error recurrence");
      requireText("ticket90 limit", "Correction limit");
      requireText("ticket90 ghost", "Limiting ghost fixed point");
      requireText("ticket90 lassos", "63");
      requireText("ticket90 next", "GrowingPrecisionErrorGhostSeparation");
    } else {
      requireText("ticket90 transfer", "method transfer only");
    }
    requireText("ticket91 title", "Ticket 91 error-tail conjugacy and invariant-set correction");
    requireText("ticket91 table", "TICKET91 tail-coordinate audit");
    if (page.problemId === "collatz") {
      requireText("ticket91 identity", "Exact growing-precision identity");
      requireText("ticket91 conjugacy", "Binary-shift conjugacy");
      requireText("ticket91 obstruction", "Full golden-mean obstruction");
      requireText("ticket91 states", "4,096");
      requireText("ticket91 words", "377");
      requireText("ticket91 next", "GoldenMeanInvariantSetEscape");
    } else {
      requireText("ticket91 transfer", "method transfer only");
    }
    requireText("ticket92 title", "Ticket 92 scale-sensitive threshold audit");
    requireText("ticket92 table", "TICKET92 threshold audit");
    if (page.problemId === "collatz") {
      requireText("ticket92 defect", "Second-order p-adic defect");
      requireText("ticket92 no-go", "First-order scale no-go");
      requireText("ticket92 pairs", "131,306");
      requireText("ticket92 events", "32,753");
      requireText("ticket92 collatz next", "FixedLogSecondOrderDefectRecurrence");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket92 Maynard", "Correct Maynard criterion");
      requireText("ticket92 removed", "Removed false promotion");
      requireText("ticket92 threshold", ">4");
      requireText("ticket92 twin rows", "17");
      requireText("ticket92 twin next", "ParityBreakingExactPairCorrelationLowerBound");
    } else {
      requireText("ticket92 transfer", "method transfer only");
    }
    requireText("ticket93 title", "Ticket 93 exact twin-correlation excess bridge");
    requireText("ticket93 table", "TICKET93 exact-correlation audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket93 contamination", "Prime-power contamination bridge");
      requireText("ticket93 typeII", "Signed Type II boundary");
      requireText("ticket93 counterexamples", "Truncated-divisor counterexamples");
      requireText("ticket93 limit", "2,000,000");
      requireText("ticket93 twins", "14,871");
      requireText("ticket93 proper powers", "94");
      requireText("ticket93 next", "ShiftTwoTypeIICorrelationExcess");
    } else {
      requireText("ticket93 transfer", "method transfer only");
    }
    requireText("ticket94 title", "Ticket 94 signed-remainder and Goldbach bridge");
    requireText("ticket94 table", "TICKET94 signed-budget audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket94 decomposition", "Exact signed decomposition");
      requireText("ticket94 norm", "Norm-only lower-bound no-go");
      requireText("ticket94 twin budget", "Twin signed remainder budget");
      requireText("ticket94 twin limit", "200,000");
      requireText("ticket94 twin next", "JointShiftTwoSignedRemainderLowerBound");
    } else if (page.problemId === "goldbach") {
      requireText("ticket94 Goldbach bridge", "Goldbach prime-power contamination bridge");
      requireText("ticket94 Goldbach margins", "Goldbach finite margins");
      requireText("ticket94 Goldbach max", "100,000");
      requireText("ticket94 Goldbach next", "UniformBinaryLambdaCorrelationExcess");
    } else {
      requireText("ticket94 transfer", "method transfer only");
    }
    requireText("ticket95 title", "Ticket 95 sharp contamination and equivalence gate");
    requireText("ticket95 table", "TICKET95 logical-novelty audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket95 mass theorem", "Weighted proper-prime-power mass theorem");
      requireText("ticket95 equivalence", "Equivalence is not a reduction");
      requireText("ticket95 twin budgets", "Sharp contamination budgets");
      requireText("ticket95 twin replay", "Twin exact equivalence replay");
      requireText("ticket95 twin max", "200,000");
      requireText("ticket95 twin next", "IndependentShiftTwoCorrelationExcess");
    } else if (page.problemId === "goldbach") {
      requireText("ticket95 Goldbach mass", "Weighted proper-prime-power mass theorem");
      requireText("ticket95 Goldbach budgets", "Sharp contamination budgets");
      requireText("ticket95 Goldbach screen", "Goldbach all-even numerical screen");
      requireText("ticket95 Goldbach exceptions", "Screen exceptions and direct witnesses");
      requireText("ticket95 Goldbach max", "1,000,000");
      requireText("ticket95 Goldbach targets", "499,999");
      requireText("ticket95 Goldbach next", "UniformBinaryMinorArcDominance");
    } else {
      requireText("ticket95 transfer", "logical novelty transfer only");
    }
    requireText("ticket96 title", "Ticket 96 Fourier phase-information audit");
    requireText("ticket96 table", "TICKET96 phase-information audit");
    if (page.problemId === "goldbach") {
      requireText("ticket96 Goldbach bridge", "Exact finite Fourier bridges");
      requireText("ticket96 Goldbach no-go", "Phase-blind information no-go");
      requireText("ticket96 Goldbach countermodel", "Adversarial spectral countermodel replay");
      requireText("ticket96 Goldbach replay", "Goldbach sparse Farey-mask replay");
      requireText("ticket96 Goldbach max", "100,000");
      requireText("ticket96 Goldbach DFT", "262,144");
      requireText("ticket96 Goldbach next", "ArithmeticMinorArcPhaseCancellation");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket96 Twin bridge", "Exact finite Fourier bridges");
      requireText("ticket96 Twin no-go", "Phase-blind information no-go");
      requireText("ticket96 Twin countermodel", "Adversarial spectral countermodel replay");
      requireText("ticket96 Twin replay", "Twin sparse Farey-mask replay");
      requireText("ticket96 Twin max", "100,000");
      requireText("ticket96 Twin DFT", "262,144");
      requireText("ticket96 Twin next", "ShiftTwoSpectralLocalizationOrTypeIICancellation");
    } else {
      requireText("ticket96 transfer", "spectral gate transfer only");
    }
    requireText("ticket97 title", "Ticket 97 optimal periodic-projection audit");
    requireText("ticket97 table", "TICKET97 finite-modulus audit");
    if (page.problemId === "goldbach") {
      requireText("ticket97 Goldbach projection", "L2-optimal periodic projection");
      requireText("ticket97 Goldbach no-go", "Fixed-modulus sign no-go");
      requireText("ticket97 Goldbach countermodel", "Zero-residue-mean countermodel");
      requireText("ticket97 Goldbach replay", "Goldbach optimal periodic replay");
      requireText("ticket97 Goldbach modulus", "2,310");
      requireText("ticket97 Goldbach next", "GrowingModulusBinaryResidualCancellation");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket97 Twin projection", "L2-optimal periodic projection");
      requireText("ticket97 Twin no-go", "Fixed-modulus sign no-go");
      requireText("ticket97 Twin countermodel", "Zero-residue-mean countermodel");
      requireText("ticket97 Twin replay", "Twin optimal periodic replay");
      requireText("ticket97 Twin modulus", "2,310");
      requireText("ticket97 Twin next", "GrowingModulusShiftTwoResidualCancellation");
    } else {
      requireText("ticket97 transfer", "finite-modulus gate transfer only");
    }
    requireText("ticket98 title", "Ticket 98 growing-modulus leakage audit");
    requireText("ticket98 table", "TICKET98 leakage boundary audit");
    if (page.problemId === "goldbach") {
      requireText("ticket98 Goldbach theorem", "Row-unique identity theorem");
      requireText("ticket98 Goldbach finding", "Certificate leakage finding");
      requireText("ticket98 Goldbach boundary", "Goldbach primorial leakage boundary");
      requireText("ticket98 Goldbach max", "9,699,690");
      requireText("ticket98 Goldbach replay", "yes / exact replay");
      requireText("ticket98 Goldbach next", "OutOfSampleGrowingModulusBinaryResidualCancellation");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket98 Twin theorem", "Row-unique identity theorem");
      requireText("ticket98 Twin finding", "Certificate leakage finding");
      requireText("ticket98 Twin boundary", "Twin primorial leakage boundary");
      requireText("ticket98 Twin max", "9,699,690");
      requireText("ticket98 Twin replay", "yes / exact replay");
      requireText("ticket98 Twin next", "OutOfSampleGrowingModulusShiftTwoResidualCancellation");
    } else {
      requireText("ticket98 transfer", "growing-partition leakage transfer only");
    }
    requireText("ticket99 title", "Ticket 99 out-of-sample local-model audit");
    requireText("ticket99 table", "TICKET99 independent local-model audit");
    if (page.problemId === "goldbach") {
      requireText("ticket99 Goldbach split", "Disjoint cross-fit contract");
      requireText("ticket99 Goldbach main", "Exact external local-main theorem");
      requireText("ticket99 Goldbach replay", "Goldbach cross-fit replay");
      requireText("ticket99 Goldbach envelope", "Finite K/log(n) falsification screen");
      requireText("ticket99 Goldbach sufficient", "Sufficient signed-residual theorem");
      requireText("ticket99 Goldbach K", "1.6");
      requireText("ticket99 Goldbach next", "UniformExternalLocalModelGoldbachResidualDecay");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket99 Twin split", "Disjoint cross-fit contract");
      requireText("ticket99 Twin main", "Exact external local-main theorem");
      requireText("ticket99 Twin replay", "Twin cross-fit replay");
      requireText("ticket99 Twin envelope", "Finite K/log(n) falsification screen");
      requireText("ticket99 Twin sufficient", "Sufficient signed-residual theorem");
      requireText("ticket99 Twin K", "1.6");
      requireText("ticket99 Twin next", "UniformExternalLocalModelShiftTwoResidualDecay");
    } else {
      requireText("ticket99 transfer", "external-model independence transfer only");
    }
    requireText("ticket100 title", "Ticket 100 extended residual and Vaughan audit");
    requireText("ticket100 table", "TICKET100 joint-cancellation audit");
    if (page.problemId === "goldbach") {
      requireText("ticket100 Goldbach identity", "Exact Vaughan identity replay");
      requireText("ticket100 Goldbach counterexample", "Componentwise proof-strategy counterexample");
      requireText("ticket100 Goldbach screen", "Goldbach 6M schedule-transition screen");
      requireText("ticket100 Goldbach components", "One-sided Vaughan component pressure");
      requireText("ticket100 Goldbach contrapositive", "Contrapositive proof program");
      requireText("ticket100 Goldbach witness", "930,930");
      requireText("ticket100 Goldbach next", "JointVaughanGoldbachResidualEnvelope");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket100 Twin identity", "Exact Vaughan identity replay");
      requireText("ticket100 Twin counterexample", "Componentwise proof-strategy counterexample");
      requireText("ticket100 Twin screen", "Twin 10M schedule-transition screen");
      requireText("ticket100 Twin components", "One-sided Vaughan component pressure");
      requireText("ticket100 Twin contrapositive", "Contrapositive proof program");
      requireText("ticket100 Twin next", "JointVaughanShiftTwoResidualEnvelope");
    } else {
      requireText("ticket100 transfer", "joint-component gate transfer only");
    }
    requireText("ticket101 title", "Ticket 101 Vaughan cutoff and energy-equivalence audit");
    requireText("ticket101 table", "TICKET101 cutoff frontier audit");
    if (page.problemId === "goldbach") {
      requireText("ticket101 Goldbach frontier", "Balanced frontier and collapse boundary");
      requireText("ticket101 Goldbach split", "Problem-specific theorem split");
      requireText("ticket101 Goldbach energy", "Energy rewrite novelty verdict");
      requireText("ticket101 Goldbach replay", "Goldbach reflection energy replay");
      requireText("ticket101 Goldbach best", "9.489");
      requireText("ticket101 Goldbach collapse", "314");
      requireText("ticket101 Goldbach next", "JointBalancedVaughanGoldbachResidualEnvelope");
    } else if (page.problemId === "twin-prime") {
      requireText("ticket101 Twin frontier", "Balanced frontier and collapse boundary");
      requireText("ticket101 Twin split", "Problem-specific theorem split");
      requireText("ticket101 Twin energy", "Energy rewrite novelty verdict");
      requireText("ticket101 Twin replay", "Twin shift energy replay");
      requireText("ticket101 Twin candidate", "1.560");
      requireText("ticket101 Twin support", "244,204");
      requireText("ticket101 Twin next", "SeparatedBalancedVaughanTwinBudgets");
    } else if (page.problemId === "riemann") {
      requireText("ticket101 RH transfer", "KernelParameterAndEnergyNoveltyGate");
      requireText("ticket101 RH next", "IndependentKernelMismatchDeficit");
    } else {
      requireText("ticket101 Collatz transfer", "OrbitParameterAndEnergyNoveltyGate");
      requireText("ticket101 Collatz next", "IndependentOrbitMismatchDeficit");
    }
    requireText("ticket102 title", "Ticket 102 Twin dyadic Vaughan holdout");
    requireText("ticket102 table", "TICKET102 dyadic holdout audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket102 Twin replay", "Complete dyadic block replay");
      requireText("ticket102 Twin correction", "Threshold correction");
      requireText("ticket102 Twin rescue", "Fresh 8M rescue holdout");
      requireText("ticket102 Twin refutation", "1.953");
      requireText("ticket102 Twin fresh maximum", "3.3068");
      requireText("ticket102 Twin support", "24.31%");
      requireText("ticket102 Twin failures", "1,000,000");
      requireText("ticket102 Twin next", "UniformFiniteDyadicSeparatedVaughanTwinBudgets");
    } else if (page.problemId === "riemann") {
      requireText("ticket102 RH route", "IndependentKernelPositivityBeforeEnergyRewrite");
      requireText("ticket102 RH next", "NonCircularExplicitFormulaKernelPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket102 Collatz route", "GoldenMeanInvariantSetEscapePriorityCorrection");
      requireText("ticket102 Collatz next", "GoldenMeanInvariantSetEscape");
    } else {
      requireText("ticket102 Goldbach route", "JointBalancedVaughanGoldbachPriority");
      requireText("ticket102 Goldbach next", "JointBalancedVaughanGoldbachResidualEnvelope");
    }
    requireText("ticket103 title", "Ticket 103 Twin exact local-block audit");
    requireText("ticket103 table", "TICKET103 local-block audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket103 Twin blocks", "Exact principal dyadic blocks");
      requireText("ticket103 Twin counterexample", "Small-scale Type II sign counterexample");
      requireText("ticket103 Twin bridge", "Conditional infinite bridge");
      requireText("ticket103 Twin verdict", "Cumulative-to-local verdict");
      requireText("ticket103 Twin structured", "3.7617");
      requireText("ticket103 Twin negative", "-174.7165");
      requireText("ticket103 Twin required", "1.7515");
      requireText("ticket103 Twin next", "UniformDyadicLocalVaughanTwinBlockBudgets");
    } else if (page.problemId === "riemann") {
      requireText("ticket103 RH route", "NonCircularKernelPositivityPreserved");
      requireText("ticket103 RH next", "NonCircularExplicitFormulaKernelPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket103 Collatz route", "GoldenMeanEscapePreserved");
      requireText("ticket103 Collatz next", "GoldenMeanInvariantSetEscape");
    } else {
      requireText("ticket103 Goldbach route", "JointBalancedGoldbachPreserved");
      requireText("ticket103 Goldbach next", "JointBalancedVaughanGoldbachResidualEnvelope");
    }
    requireText("ticket104 title", "Ticket 104 Twin Type II weighted-Mobius anatomy");
    requireText("ticket104 table", "TICKET104 weighted-Mobius audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket104 Twin anatomy", "Exact outer-divisor anatomy");
      requireText("ticket104 Twin reduction", "Exact reduction");
      requireText("ticket104 Twin Abel", "Abel information-loss verdict");
      requireText("ticket104 Twin negative", "39.92");
      requireText("ticket104 Twin envelope", "1088.15");
      requireText("ticket104 Twin next", "WeightedMobiusShiftedPrimeDyadicCancellation");
    } else if (page.problemId === "riemann") {
      requireText("ticket104 RH route", "NonCircularKernelPositivityPreserved");
      requireText("ticket104 RH next", "NonCircularExplicitFormulaKernelPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket104 Collatz route", "GoldenMeanEscapePreserved");
      requireText("ticket104 Collatz next", "GoldenMeanInvariantSetEscape");
    } else {
      requireText("ticket104 Goldbach route", "JointBalancedGoldbachPreserved");
      requireText("ticket104 Goldbach next", "JointBalancedVaughanGoldbachResidualEnvelope");
    }
    requireText("ticket105 title", "Ticket 105 Twin centered progression discrepancy");
    requireText("ticket105 table", "TICKET105 centered progression audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket105 Twin rows", "Baseline and centered discrepancy");
      requireText("ticket105 Twin centering", "Exact centering");
      requireText("ticket105 Twin boundary", "Information boundary");
      requireText("ticket105 Twin negative", "5.41");
      requireText("ticket105 Twin Cauchy", "41.15");
      requireText("ticket105 Twin next", "MobiusWeightedPrimeProgressionDiscrepancyBound");
    } else if (page.problemId === "riemann") {
      requireText("ticket105 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket105 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket105 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket106 title", "Ticket 106 Twin modulus-grouped dispersion");
    requireText("ticket106 table", "TICKET106 grouped dispersion audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket106 Twin rows", "Grouped norm and sparse-cell pressure");
      requireText("ticket106 Twin occupancy", "2M occupancy ladder");
      requireText("ticket106 Twin grouping", "Exact modulus grouping");
      requireText("ticket106 Twin leakage", "Sparse-modulus leakage verdict");
      requireText("ticket106 Twin grouped Cauchy", "249.12");
      requireText("ticket106 Twin sparse fraction", "72.31%");
      requireText("ticket106 Twin sparse contribution", "64933.8");
      requireText("ticket106 Twin next", "NonSparseModulusTwinDispersionWithSparseTailControl");
    } else if (page.problemId === "riemann") {
      requireText("ticket106 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket106 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket106 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket107 title", "Ticket 107 Twin sparse-tail recombination");
    requireText("ticket107 table", "TICKET107 sparse-tail recombination audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket107 Twin rows", "q-to-n compression and signed compensation");
      requireText("ticket107 Twin exact", "Exact Vaughan recombination");
      requireText("ticket107 Twin verdict", "Component-budget verdict");
      requireText("ticket107 Twin L1", "69.53%");
      requireText("ticket107 Twin partial K", "2.59");
      requireText("ticket107 Twin joint K", "0.37");
      requireText("ticket107 Twin next", "JointStructuredSparseDenseTwinDispersion");
    } else if (page.problemId === "riemann") {
      requireText("ticket107 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket107 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket107 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket108 title", "Ticket 108 Twin joint-equivalence and smoothing");
    requireText("ticket108 table", "TICKET108 equivalence and smoothing audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket108 Twin rows", "Hard versus smooth signed residual");
      requireText("ticket108 Twin no reduction", "Algebraic no-reduction");
      requireText("ticket108 Twin bridge", "Nonnegative bump bridge");
      requireText("ticket108 Twin hard K", "0.3691");
      requireText("ticket108 Twin smooth K", "0.4226");
      requireText("ticket108 Twin next", "SmoothedShiftTwoTypeIICorrelationExcess");
    } else if (page.problemId === "riemann") {
      requireText("ticket108 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket108 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket108 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket109 title", "Ticket 109 Twin spectral-phase audit");
    requireText("ticket109 table", "TICKET109 spectral phase audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket109 Twin rows", "Positive and negative phase balance");
      requireText("ticket109 Twin identity", "Exact spectral identity");
      requireText("ticket109 Twin no-go", "Low-frequency no-go");
      requireText("ticket109 Twin ratio", "0.1435");
      requireText("ticket109 Twin next", "RamanujanMajorArcPhaseMarginWithMinorArcControl");
    } else if (page.problemId === "riemann") {
      requireText("ticket109 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket109 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket109 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket110 title", "Ticket 110 Twin rational major-arc budget");
    requireText("ticket110 table", "TICKET110 rational arc audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket110 Twin rows", "Major capture and minor saving gap");
      requireText("ticket110 Twin contract", "Anti-circular major-arc contract");
      requireText("ticket110 Twin no-go", "Trivial minor no-go");
      requireText("ticket110 Twin next", "FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving");
    } else if (page.problemId === "riemann") {
      requireText("ticket110 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket110 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket110 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket111 title", "Ticket 111 Twin Type II minor phase audit");
    requireText("ticket111 table", "TICKET111 Type II phase audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket111 Twin rows", "Phase-aware saving frontier");
      requireText("ticket111 Twin identity", "Exact Vaughan cross-spectrum");
      requireText("ticket111 Twin no-go", "Phase-blind partition no-go");
      requireText("ticket111 Twin holdout", "Registered X^-1/6 candidate");
      requireText("ticket111 Twin finite lower", "257818.2");
      requireText("ticket111 Twin next", "PhaseAwareVaughanTypeIIMinorArcPowerSaving");
    } else if (page.problemId === "riemann") {
      requireText("ticket111 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket111 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket111 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket112 title", "Ticket 112 Twin Farey-cell endpoint Abel audit");
    requireText("ticket112 table", "TICKET112 Farey endpoint audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket112 Twin rows", "Endpoint cancellation frontier");
      requireText("ticket112 Twin identity", "Exact Farey-cell Abel identity");
      requireText("ticket112 Twin no-go", "Endpoint triangle no-go");
      requireText("ticket112 Twin candidate", "Inherited endpoint candidate");
      requireText("ticket112 Twin finite lower", "770014.6");
      requireText("ticket112 Twin next", "UniformFareyCellEndpointCancellationForVaughanCrossSpectrum");
    } else if (page.problemId === "riemann") {
      requireText("ticket112 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket112 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket112 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket113 title", "Ticket 113 Twin Farey denominator endpoint audit");
    requireText("ticket113 table", "TICKET113 Farey denominator audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket113 Twin rows", "Denominator-block cancellation frontier");
      requireText("ticket113 Twin profile", "4M right-denominator block profile");
      requireText("ticket113 Twin identity", "Exact denominator identity");
      requireText("ticket113 Twin no-go", "Magnitude-label countermodel");
      requireText("ticket113 Twin finite lower", "1017376.2");
      requireText("ticket113 Twin adversary lower", "-376366.3");
      requireText("ticket113 Twin next", "UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum");
    } else if (page.problemId === "riemann") {
      requireText("ticket113 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket113 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket113 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket114 title", "Ticket 114 Twin Ramanujan numerator-dispersion audit");
    requireText("ticket114 table", "TICKET114 Ramanujan numerator audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket114 Twin frontier", "Ramanujan and centered-dispersion frontier");
      requireText("ticket114 Twin profile", "4M centered-numerator denominator profile");
      requireText("ticket114 Twin identity", "Exact Ramanujan decomposition");
      requireText("ticket114 Twin support theorem", "Sharp centered support theorem");
      requireText("ticket114 Twin finite lower", "327951.0");
      requireText("ticket114 Twin ratio", "82.50%");
      requireText("ticket114 Twin next", "EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket114 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket114 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket114 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket115 title", "Ticket 115 Twin complex cyclotomic dispersion audit");
    requireText("ticket115 table", "TICKET115 complex cyclotomic audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket115 Twin frontier", "Scalar-aware versus orientation-free frontier");
      requireText("ticket115 Twin profile", "4M denominatorwise scalar-aware budget change");
      requireText("ticket115 Twin identity", "Exact complex cyclotomic decomposition");
      requireText("ticket115 Twin support", "Sharp complex support theorem");
      requireText("ticket115 Twin no-go", "Orientation-free no-go");
      requireText("ticket115 Twin scalar lower", "335523.7");
      requireText("ticket115 Twin free lower", "248127.1");
      requireText("ticket115 Twin next", "EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket115 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket115 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket115 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket116 title", "Ticket 116 Twin Möbius-sign cyclotomic audit");
    requireText("ticket116 table", "TICKET116 Möbius-sign cyclotomic audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket116 Twin frontier", "Signed versus independent Möbius-layer frontier");
      requireText("ticket116 Twin profile", "4M denominatorwise independent-sign loss");
      requireText("ticket116 Twin identity", "Exact Vaughan Möbius-sign lift");
      requireText("ticket116 Twin polarization", "Exact centered polarization");
      requireText("ticket116 Twin no-go", "Independent-sign triangle no-go");
      requireText("ticket116 Twin signed lower", "335523.7");
      requireText("ticket116 Twin independent lower", "-2401998.7");
      requireText("ticket116 Twin next", "EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket116 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket116 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket116 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket117 title", "Ticket 117 Twin signed-dyadic endpoint Gram audit");
    requireText("ticket117 table", "TICKET117 signed-dyadic Gram audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket117 Twin frontier", "Signed, singleton, Cauchy, and adjacent-pair frontier");
      requireText("ticket117 Twin concentration", "4M adjacent-pair budget concentration");
      requireText("ticket117 Twin interactions", "Largest geometry-weighted Gram interactions");
      requireText("ticket117 Twin lift", "Exact signed dyadic lift");
      requireText("ticket117 Twin Gram", "Exact endpoint Gram identity");
      requireText("ticket117 Twin paired lower", "-1236.3");
      requireText("ticket117 Twin next", "EventuallySubcriticalAdjacentDyadicPairVaughanEndpointBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket117 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket117 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket117 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket118 title", "Ticket 118 preregistered canonical adjacent-pair 8M holdout");
    requireText("ticket118 table", "TICKET118 preregistered holdout");
    if (page.problemId === "twin-prime") {
      requireText("ticket118 Twin ledger", "Registered 8M budget ledger");
      requireText("ticket118 Twin groups", "Canonical factor-four group concentration");
      requireText("ticket118 Twin registration", "Preregistration contract");
      requireText("ticket118 Twin lower", "156727.0");
      requireText("ticket118 Twin ratio", "1.193875");
      requireText("ticket118 Twin next", "EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket118 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket118 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket118 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket119 title", "Ticket 119 preregistered canonical-pair 16M persistence holdout");
    requireText("ticket119 table", "TICKET119 registered persistence test");
    if (page.problemId === "twin-prime") {
      requireText("ticket119 Twin scale ledger", "Finite scale falsification ledger");
      requireText("ticket119 Twin budget", "Registered 16M budget ledger");
      requireText("ticket119 Twin groups", "16M canonical group concentration");
      requireText("ticket119 Twin lower", "1479021.8");
      requireText("ticket119 Twin margin", "19.7322%");
      requireText("ticket119 Twin sublemma", "UniformLowDivisorCanonicalPairDispersion");
      requireText("ticket119 Twin next", "EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget");
    } else if (page.problemId === "riemann") {
      requireText("ticket119 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket119 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket119 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket120 title", "Ticket 120 low-divisor pair saving identity and weak-contract no-go");
    requireText("ticket120 table", "TICKET120 low-divisor audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket120 Twin recent", "Recent finite saving diagnosis");
      requireText("ticket120 Twin ledger", "Eight-scale pair-saving ledger");
      requireText("ticket120 Twin extremizers", "Exact weak-contract extremizers");
      requireText("ticket120 Twin saving", "19.7226%");
      requireText("ticket120 Twin mean share", "0.0069%");
      requireText("ticket120 Twin discarded", "UniversalFixedFractionLowDivisorPairSavingUnderGramContract");
      requireText("ticket120 Twin retained", "VaughanLowDivisorDenominatorSummedAngleGap");
    } else if (page.problemId === "riemann") {
      requireText("ticket120 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket120 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket120 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket121 title", "Ticket 121 balance-angle defect correction and single-factor no-go");
    requireText("ticket121 table", "TICKET121 balance-angle audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket121 Twin recent", "Recent balance-angle diagnosis");
      requireText("ticket121 Twin mass", "Eight-scale balanced-decorrelated mass");
      requireText("ticket121 Twin no-go", "Exact single-factor no-go limits");
      requireText("ticket121 Twin bridge", "Full-budget bridge strength");
      requireText("ticket121 Twin mass floor", "63.8848%");
      requireText("ticket121 Twin certificate floor", "17.9685%");
      requireText("ticket121 Twin discarded angle", "FixedSavingFromDenominatorSummedCosineGapAlone");
      requireText("ticket121 Twin retained", "VaughanLowDivisorWeightedBalanceAngleDefectGap");
    } else if (page.problemId === "riemann") {
      requireText("ticket121 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket121 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket121 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket122 title", "Ticket 122 canonical joint scalar-vector identity and local-only no-go");
    requireText("ticket122 table", "TICKET122 canonical joint audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket122 Twin ledger", "Eight-scale full canonical ledger");
      requireText("ticket122 Twin anatomy", "16M canonical pair anatomy");
      requireText("ticket122 Twin no-go", "Exact local-only no-go limits");
      requireText("ticket122 Twin saving floor", "19.3458%");
      requireText("ticket122 Twin certificate floor", "16.0000%");
      requireText("ticket122 Twin discarded local", "LowDivisorBalancedDecorrelatedMassAloneControlsFullCanonicalBudget");
      requireText("ticket122 Twin retained", "VaughanCanonicalPairJointDefectAndResidualBudgetGap");
    } else if (page.problemId === "riemann") {
      requireText("ticket122 RH route", "NonCircularKernelPositivityPreserved");
    } else if (page.problemId === "collatz") {
      requireText("ticket122 Collatz route", "GoldenMeanEscapePreserved");
    } else {
      requireText("ticket122 Goldbach route", "JointBalancedGoldbachPreserved");
    }
    requireText("ticket123 title", "Ticket 123 canonical defect ratio closure bridge");
    requireText("ticket123 table", "TICKET123 ratio bridge");
    if (page.problemId === "twin-prime") {
      requireText("ticket123 Twin ledger", "Eight-scale ratio ledger");
      requireText("ticket123 Twin attribution", "8M to 16M exact margin attribution");
      requireText("ticket123 Twin no-go", "Independent-premise no-go families");
      requireText("ticket123 Twin exact eta", "19.3458%");
      requireText("ticket123 Twin certified eta", "16.0000%");
      requireText("ticket123 Twin bridge", "CanonicalDefectRatioClosureBridge");
      requireText("ticket123 Twin retained", "VaughanCanonicalDefectRatioTriple");
    } else if (page.problemId === "riemann") {
      requireText("ticket123 RH proxy", "finite Jensen-polynomial hyperbolicity");
      requireText("ticket123 RH target", "NonCircularExplicitFormulaKernelPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket123 Collatz proxy", "finite stopping-time and density verification");
      requireText("ticket123 Collatz target", "GoldenMeanInvariantSetEscape");
    } else {
      requireText("ticket123 Goldbach proxy", "finite mean singular-series agreement");
      requireText("ticket123 Goldbach target", "JointBalancedVaughanGoldbachResidualEnvelope");
    }
    requireText("ticket124 title", "Ticket 124 canonical obstruction limsup criterion");
    requireText("ticket124 table", "TICKET124 obstruction audit");
    if (page.problemId === "twin-prime") {
      requireText("ticket124 Twin ledger", "Eight-scale joint obstruction ledger");
      requireText("ticket124 Twin tails", "Observed finite tail envelopes");
      requireText("ticket124 Twin no-go", "Exact prior-target no-go families");
      requireText("ticket124 Twin iff", "EventualPositiveMarginIffLimsupObstructionBelowOne");
      requireText("ticket124 Twin last exact", "0.802678");
      requireText("ticket124 Twin last certificate", "0.834379");
      requireText("ticket124 Twin compensation", "0.8 joint vs 1.6 detached");
      requireText("ticket124 Twin retired", "VaughanCanonicalDefectRatioTriple");
      requireText("ticket124 Twin retained", "VaughanCanonicalObstructionLimsup");
    } else if (page.problemId === "riemann") {
      requireText("ticket124 RH route", "ExactTestClassKernelPositivityContract");
      requireText("ticket124 RH target", "AdmissibleKernelConeDensityAndPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket124 Collatz route", "GoldenMeanRouteScopeCorrection");
      requireText("ticket124 Collatz global", "ResidueRankDescentCover");
    } else {
      requireText("ticket124 Goldbach route", "JointResidualCutoffContract");
      requireText("ticket124 Goldbach target", "ExplicitJointBalancedGoldbachCutoff");
    }
    requireText("ticket127 title", "Ticket 127 exception repair and effective bridges");
    requireText("ticket127 table", "TICKET127 audit");
    requireText("ticket127 latest", "LATEST / 최신 연구 경계");
    requireText("ticket127 scope", "conjecture open / 난제 미해결");
    requireText("ticket127 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket127 RH theorem", "DenseCoreNegativeWitnessSemidecision");
      requireText("ticket127 RH target", "IntervalCertifiedWeilCoreEvaluator");
      requireText("ticket127 RH semidecision", "반결정");
    } else if (page.problemId === "collatz") {
      requireText("ticket127 Collatz theorem", "NontrivialEventuallyLowPathIffFiniteStoppingCounterexample");
      requireText("ticket127 Collatz correction", "n=1은 모든 U_k에 남는");
      requireText("ticket127 Collatz nontrivial", "4,027,109");
      requireText("ticket127 Collatz witnesses", "27, 31");
      requireText("ticket127 Collatz target", "UniformNontrivialEventuallyLowPathExclusion");
    } else if (page.problemId === "goldbach") {
      requireText("ticket127 Goldbach theorem", "UniformBinaryGoldbachSingularSeriesLowerBound");
      requireText("ticket127 Goldbach A", "주항 계수 A=1");
      requireText("ticket127 Goldbach K", "42.832743722235");
      requireText("ticket127 Goldbach target", "ExplicitPointwiseBinaryGoldbachResidualConstant");
    } else {
      requireText("ticket127 Twin theorem", "RawBudgetTransportIffNormalizedAffineContraction");
      requireText("ticket127 Twin gamma", "2.011542095245601");
      requireText("ticket127 Twin u", "1.860330508366795");
      requireText("ticket127 Twin target", "UniformVaughanRawBudgetTransportAndInterpolation");
    }
    requireText("ticket126 title", "Ticket 126 route correction and premise closure");
    requireText("ticket126 table", "TICKET126 audit");
    requireText("ticket126 latest", "LATEST / 최신 연구 계약");
    requireText("ticket126 scope", "intermediate result; conjecture open");
    requireText("ticket126 resolutions", "conjecture resolutions");
    if (page.problemId === "riemann") {
      requireText("ticket126 RH theorem", "ContinuousEvaluationSeparatesAutocorrelationCone");
      requireText("ticket126 RH decision", "DISCARD / 폐기");
      requireText("ticket126 RH target", "NonCircularWeilAutocorrelationPositivity");
    } else if (page.problemId === "collatz") {
      requireText("ticket126 Collatz theorem", "EventuallyLowUnresolvedPathIffFiniteStoppingCounterexample");
      requireText("ticket126 Collatz unresolved", "4,027,110");
      requireText("ticket126 Collatz mass", "3.00043%");
      requireText("ticket126 Collatz target", "UniformNontrivialEventuallyLowPathExclusion");
    } else if (page.problemId === "goldbach") {
      requireText("ticket126 Goldbach theorem", "ExplicitProperPrimePowerContaminationBound");
      requireText("ticket126 Goldbach B", "B = 2.094918178743");
      requireText("ticket126 Goldbach closed", "CLOSED / 폐쇄");
      requireText("ticket126 Goldbach target", "ExplicitGoldbachMajorAndResidualConstants");
    } else {
      requireText("ticket126 Twin theorem", "PreregisteredThirtyTwoMillionDyadicContractionHoldout");
      requireText("ticket126 Twin residual", "0.145872900933948");
      requireText("ticket126 Twin slack", "0.084127099066052");
      requireText("ticket126 Twin provenance", "결과 저장 전 허용오차 게이트 실패 1회");
    }
    requireText("ticket125 title", "Ticket 125 infinite bridge contracts");
    requireText("ticket125 table", "TICKET125 contract audit");
    requireText("ticket125 scope", "conditional bridge proved; conjecture open");
    if (page.problemId === "riemann") {
      requireText("ticket125 RH route", "ContinuousDenseConePositivityExtension");
      requireText("ticket125 RH no-go", "Missing-hypothesis countermodels");
      requireText("ticket125 RH finite Gram", "Finite Gram no-go family");
      requireText("ticket125 RH density", "density");
      requireText("ticket125 RH continuity", "continuity");
    } else if (page.problemId === "collatz") {
      requireText("ticket125 Collatz route", "AdaptiveResidueFiniteStoppingCover");
      requireText("ticket125 Collatz frontier", "Adaptive residue-cylinder frontier");
      requireText("ticket125 Collatz certified", "121,825");
      requireText("ticket125 Collatz unresolved", "9,247");
      requireText("ticket125 Collatz bridge", "UniversalFiniteStoppingDescentIffCollatz");
    } else if (page.problemId === "goldbach") {
      requireText("ticket125 Goldbach route", "ExplicitWeightedGoldbachFiniteGlue");
      requireText("ticket125 Goldbach endpoint", "Endpoint budget at H = 4×10^18");
      requireText("ticket125 Goldbach K", "K = 40");
      requireText("ticket125 Goldbach target", "ExplicitJointBalancedGoldbachCutoff");
    } else {
      requireText("ticket125 Twin route", "DyadicAffineObstructionContraction");
      requireText("ticket125 Twin candidate", "Frozen dyadic contraction candidate");
      requireText("ticket125 Twin recurrence", "Q(2X) ≤ 3Q(X)/4 + 23/100");
      requireText("ticket125 Twin residual", "0.220387");
      requireText("ticket125 Twin target", "DyadicVaughanObstructionContractionAndInterpolation");
    }
    return checks;
  });
  if (missingTicket71Checks.length > 0) {
    console.error(JSON.stringify({ errors, missingTicket71Checks }, null, 2));
    process.exit(1);
  }
  if (
    metrics.openProblemPages.length !== 4 ||
    metrics.openProblemPages.some(
      (page) =>
        !page.status.includes("open not proven") ||
        page.metricCount < 3 ||
        page.blockedClaimCount < 4 ||
        !page.proofVerdictText.includes("Target verdict") ||
        !page.proofVerdictText.includes("not proved by primeproject") ||
        !page.proofVerdictText.includes("Actual proved result") ||
        !page.proofVerdictText.includes("bounded theorem certified") ||
        !page.proofVerdictText.includes("Full proof blocker") ||
        !page.proofVerdictText.includes("PrimeProject may display a proof only when") ||
        !page.actualProofRunnerText.includes("Execution result") ||
        !page.actualProofRunnerText.includes("Why this is not yet a proof") ||
        !page.actualProofRunnerText.includes("Next executable move") ||
        page.actualProofRunnerSteps < 4 ||
        !page.proofOrCounterexampleText.includes("Proof modes") ||
        !page.proofOrCounterexampleText.includes("Direct counterexample search") ||
        !page.proofOrCounterexampleText.includes("Contrapositive route") ||
        !page.proofOrCounterexampleText.includes("Claim boundary") ||
        !page.proofOrCounterexampleText.includes("Ticket 17 breakthrough attempt") ||
        !page.proofOrCounterexampleText.includes("Ticket 18 reduction lab") ||
        !page.proofOrCounterexampleText.includes("Reduction result") ||
        !page.proofOrCounterexampleText.includes("Ticket 19 proof pressure lab") ||
        !page.proofOrCounterexampleText.includes("Proof pressure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 20 valuation-prefix lab") ||
        !page.proofOrCounterexampleText.includes("Valuation-prefix result") ||
        !page.proofOrCounterexampleText.includes("Ticket 21 two-adic branch lab") ||
        !page.proofOrCounterexampleText.includes("Two-adic branch result") ||
        !page.proofOrCounterexampleText.includes("Ticket 22 negation pressure lab") ||
        !page.proofOrCounterexampleText.includes("Negation pressure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 23 CEGIS rank lab") ||
        !page.proofOrCounterexampleText.includes("CEGIS rank result") ||
        !page.proofOrCounterexampleText.includes("Ticket 24 bridge-weight lab") ||
        !page.proofOrCounterexampleText.includes("Bridge-weight result") ||
        !page.proofOrCounterexampleText.includes("Ticket 25 formal lemma kernel") ||
        !page.proofOrCounterexampleText.includes("Formal kernel result") ||
        !page.proofOrCounterexampleText.includes("Ticket 26 micro-lemma closure") ||
        !page.proofOrCounterexampleText.includes("Micro-lemma certificate") ||
        !page.proofOrCounterexampleText.includes("Closed micro-lemma") ||
        !page.proofOrCounterexampleText.includes("Ticket 27 rank-frontier lab") ||
        !page.proofOrCounterexampleText.includes("Rank frontier result") ||
        !page.proofOrCounterexampleText.includes("Ticket 28 trichotomy descent lab") ||
        !page.proofOrCounterexampleText.includes("Trichotomy result") ||
        !page.proofOrCounterexampleText.includes("Ticket 29 adaptive frontier lab") ||
        !page.proofOrCounterexampleText.includes("Adaptive frontier result") ||
        !page.proofOrCounterexampleText.includes("Ticket 30 potential synthesis lab") ||
        !page.proofOrCounterexampleText.includes("Potential synthesis result") ||
        !page.proofOrCounterexampleText.includes("Ticket 31 feature-stutter obstruction") ||
        !page.proofOrCounterexampleText.includes("Feature-stutter result") ||
        !page.proofOrCounterexampleText.includes("Ticket 32 stateful measure lab") ||
        !page.proofOrCounterexampleText.includes("Stateful measure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 33 global measure lab") ||
        !page.proofOrCounterexampleText.includes("Global measure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 34 high-branch automaton lab") ||
        !page.proofOrCounterexampleText.includes("High-branch automaton result") ||
        !page.proofOrCounterexampleText.includes("Ticket 35 limsup mass refinement lab") ||
        !page.proofOrCounterexampleText.includes("Limsup mass refinement result") ||
        !page.proofOrCounterexampleText.includes("Ticket 36 null-frontier arithmetic lab") ||
        !page.proofOrCounterexampleText.includes("Natural frontier exit result") ||
        !page.proofOrCounterexampleText.includes("Ticket 37 pointwise rank synthesis lab") ||
        !page.proofOrCounterexampleText.includes("Pointwise rank synthesis result") ||
        !page.proofOrCounterexampleText.includes("Ticket 38 symbolic frontier extension lab") ||
        !page.proofOrCounterexampleText.includes("Symbolic extension result") ||
        !page.proofOrCounterexampleText.includes("Ticket 39 phase/state potential synthesis lab") ||
        !page.proofOrCounterexampleText.includes("Phase/state potential result") ||
        !page.proofOrCounterexampleText.includes("Ticket 40 transition closure lab") ||
        !page.proofOrCounterexampleText.includes("Transition closure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 41 rank escape normalization lab") ||
        !page.proofOrCounterexampleText.includes("Rank escape result") ||
        !page.proofOrCounterexampleText.includes("Ticket 42 parametric transition template lab") ||
        !page.proofOrCounterexampleText.includes("Template result") ||
        !page.proofOrCounterexampleText.includes("Ticket 43 lift constraint measure lab") ||
        !page.proofOrCounterexampleText.includes("Lift measure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 44 feature-measure counteredge lab") ||
        !page.proofOrCounterexampleText.includes("Feature measure result") ||
        !page.proofOrCounterexampleText.includes("Ticket 45 symbolic rank clause lab") ||
        !page.proofOrCounterexampleText.includes("Symbolic clause result") ||
        !page.proofOrCounterexampleText.includes("Ticket 46 stable clause grammar lab") ||
        !page.proofOrCounterexampleText.includes("Stable grammar result") ||
        !page.proofOrCounterexampleText.includes("Ticket 47 periodic state lasso lab") ||
        !page.proofOrCounterexampleText.includes("Periodic lasso result") ||
        !page.proofOrCounterexampleText.includes("Ticket 48 automaton reachability lab") ||
        !page.proofOrCounterexampleText.includes("Automaton/reachability result") ||
        !page.proofOrCounterexampleText.includes("Ticket 49 symbolic preimage obstruction lab") ||
        !page.proofOrCounterexampleText.includes("Symbolic preimage result") ||
        !page.proofOrCounterexampleText.includes("Ticket 50 phase-lift exception lab") ||
        !page.proofOrCounterexampleText.includes("Phase-lift result") ||
        !page.proofOrCounterexampleText.includes("Ticket 51 phase-15 terminal lift lab") ||
        !page.proofOrCounterexampleText.includes("Terminal lift result") ||
        !page.proofOrCounterexampleText.includes("Ticket 52 frontier budget lab") ||
        !page.proofOrCounterexampleText.includes("Frontier budget result") ||
        !page.proofOrCounterexampleText.includes("Ticket 53 symbolic terminal theorem lab") ||
        !page.proofOrCounterexampleText.includes("Symbolic terminal result") ||
        !page.proofOrCounterexampleText.includes("Ticket 54 new template family lab") ||
        !page.proofOrCounterexampleText.includes("Post-terminal family result") ||
        !page.proofOrCounterexampleText.includes("Ticket 55 phase-5 valuation gate lab") ||
        !page.proofOrCounterexampleText.includes("Gate-to-terminal result") ||
        !page.proofOrCounterexampleText.includes("Ticket 56 pre-gate projection escape lab") ||
        !page.proofOrCounterexampleText.includes("Pre-gate partition result") ||
        !page.proofOrCounterexampleText.includes("Ticket 57 parametric template automaton lab") ||
        !page.proofOrCounterexampleText.includes("Parametric automaton result") ||
        !page.proofOrCounterexampleText.includes("Ticket 58 affine-boundary lift lab") ||
        !page.proofOrCounterexampleText.includes("Affine-boundary lift result") ||
        !page.proofOrCounterexampleText.includes("Ticket 59 symbolic lift mismatch lab") ||
        !page.proofOrCounterexampleText.includes("Counted cylinder result") ||
        !page.proofOrCounterexampleText.includes("Ticket 60 mixed-cylinder separator lab") ||
        !page.proofOrCounterexampleText.includes("Separator result") ||
        !page.proofOrCounterexampleText.includes("Ticket 61 symbolic failure-offset lab") ||
        !page.proofOrCounterexampleText.includes("Pre-replay separator result") ||
        !page.proofOrCounterexampleText.includes("Ticket 62 mod16 transition-cover lab") ||
        !page.proofOrCounterexampleText.includes("Transition-cover result") ||
        !page.proofOrCounterexampleText.includes("Ticket 63 mod16 automaton-cover lab") ||
        !page.proofOrCounterexampleText.includes("Automaton-cover result") ||
        !page.proofOrCounterexampleText.includes("Ticket 64 symbolic mod16 transition lab") ||
        !page.proofOrCounterexampleText.includes("Symbolic transition result") ||
        !page.proofOrCounterexampleText.includes("Ticket 65 start-template chain extinction lab") ||
        !page.proofOrCounterexampleText.includes("Start-template extinction result") ||
        !page.proofOrCounterexampleText.includes("Ticket 66 complement-cover audit") ||
        !page.proofOrCounterexampleText.includes("Complement-cover result") ||
        !page.proofOrCounterexampleText.includes("Ticket 67 open-template rank audit") ||
        !page.proofOrCounterexampleText.includes("Open-template rank result") ||
        !page.proofOrCounterexampleText.includes("Ticket 68 cycle-SCC refinement") ||
        !page.proofOrCounterexampleText.includes("Cycle refinement result") ||
        !page.proofOrCounterexampleText.includes("Ticket 69 prefix/consumed rank certificate") ||
        !page.proofOrCounterexampleText.includes("Rank certificate result") ||
        !page.proofOrCounterexampleText.includes("Ticket 70 prefix frontier expansion") ||
        !page.proofOrCounterexampleText.includes("Frontier expansion result") ||
        !page.proofOrCounterexampleText.includes("Ticket 71 stronger frontier coordinates") ||
        !page.proofOrCounterexampleText.includes("Stronger coordinate result") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Projection escape witness")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("template_plus_prefix_length_residue_mod_2^28")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("no_known_root_replays_full_lasso_period")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Replayable-cycle search")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("refuted_by_sampled_boundary_prediction_mismatch")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Boundary prediction mismatch examples")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("3,086")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("41,472")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("mixed_outcome_cylinder")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("uniform_boundary_mismatch_cylinder")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("low40_plus_failure_offset")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("low40_plus_high_extension_mod_2^4")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("Mod16FailureOffsetTransitionOrAutomatonCountedCover")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("mod16_transition_survives_bounded_lift")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Mod16AutomatonCoverOrLiftCollision")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("53,760")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("58")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("SymbolicMod16AutomatonTransitionProof")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("13,184")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("low40_mod_2^20_plus_base_mod16")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("SymbolicStartTemplateGateAndOffsetTransition")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("3,344")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("0->1")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("0->5")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("56:824")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("80")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("StartTemplateChainExtinctionOrComplementCover")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("low40_parent_high10_child_top4")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("row-unique")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("17,134")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("491")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("OpenTemplateFamilyRankOrComplementCounterexample")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("open_wrong_tail_target_residue_mod_256")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("274,144")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("429")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("96,433")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("CycleSCCRefinementOrInfiniteLiftExclusion")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("refuted_by_template_transition_cycle")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("base_prefix_consumed")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("9,616")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("41,283")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("tail8_res4096_vexact")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("PrefixConsumedDAGCompletenessOrPersistentRefinedCycle")) ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("observed_scc_broken_by_refinement")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("bounded_rank_descent_valid_but_unexpanded_frontier_open")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("89,222")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("6,649")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("open_base_cycle_exit")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("PrefixConsumedRankCompletenessOrFrontierCycle")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("frontier_expansion_refutes_direct_rank_closure_open_no_resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("792,064")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("155,321")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("59,449")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("internal_rank_equal_frontier_cycle_pressure")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("StrongerFrontierCoordinateOrPersistentLiftCycle")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Coordinate family comparison")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("bounded_transition_separator_found_but_infinite_bridge_open")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("base_fullword_residue65536")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("254,488")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("22,219")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("base_tail12_residue65536")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("InfiniteFrontierCoordinateLiftClosureOrChain")) ||
        !page.proofOrCounterexampleText.includes("Ticket 72 infinite frontier lift closure") ||
        !page.proofOrCounterexampleText.includes("Lift-closure result") ||
        (page.problemId === "collatz" &&
          !page.proofOrCounterexampleText.includes("persistent_mixed_key_lift_chain_pressure_observed_no_resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("36,848")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("6,857")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("4,142")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("6,448")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("CompactMixedKeyInvariantOrPersistentLiftChain")) ||
        !page.proofOrCounterexampleText.includes("Ticket 73 lineage-constrained pressure forest") ||
        !page.proofOrCounterexampleText.includes("Lineage audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("strict reentry tree extinct at fifth lift for selected roots no global conclusion")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("12,911")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("2,873")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("45,968")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("CoverageCertificateAndAllDepthReentryTreeDecision")) ||
        !page.proofOrCounterexampleText.includes("Ticket 74 coverage leakage and escaping pressure forest") ||
        !page.proofOrCounterexampleText.includes("Coverage leakage audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("strict cover leakage and sixth pressure persistence observed no global resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("20,752")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("15,696")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("78,315")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("GlobalCoverageCertificateOrEscapingPressureForestDecision")) ||
        !page.proofOrCounterexampleText.includes("Ticket 75 fixed-coordinate closure audit") ||
        !page.proofOrCounterexampleText.includes("Coordinate closure audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("all tested finite preoutcome coordinates leak or cycle no global resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Compression versus state growth")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("77,998")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath")) ||
        (page.problemId !== "collatz" && !page.proofOrCounterexampleText.includes("method transfer only")) ||
        !page.proofOrCounterexampleText.includes("Ticket 76 symbolic boundary recurrence") ||
        !page.proofOrCounterexampleText.includes("Boundary recurrence audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("symbolic formula verified fixed precision closure refuted on tested precisions no global resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Fixed precision versus four-bit lookahead")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("297,104")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("ReachableBoundaryRestrictionOrTwoAdicPressurePath")) ||
        !page.proofOrCounterexampleText.includes("Ticket 77 fixed-prefix boundary orbit") ||
        !page.proofOrCounterexampleText.includes("Fixed-prefix boundary orbit audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("fixed prefix boundary orbit classified no collatz resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("Inverse-16 periodic orbit audit")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("18,569")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("ChangingPrefixNaturalAdmissibilityRank")) ||
        !page.proofOrCounterexampleText.includes("Ticket 78 finite-cylinder admissibility no-go") ||
        !page.proofOrCounterexampleText.includes("Finite-cylinder no-go audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("finite two adic natural separator refuted exactly no collatz resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("65,535")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("262,140")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("ArchimedeanTwoAdicCoupledDescent")) ||
        !page.proofOrCounterexampleText.includes("Ticket 79 Archimedean-two-adic rank no-go") ||
        !page.proofOrCounterexampleText.includes("TICKET79 rank no-go audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("bounded archimedean two adic one step rank refuted exactly no collatz resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("131,584")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("MinimalCounterexampleValuationSurplusContradiction")) ||
        !page.proofOrCounterexampleText.includes("Ticket 80 least-counterexample compactness no-go") ||
        !page.proofOrCounterexampleText.includes("TICKET80 compactness no-go audit") ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("least counterexample finite prefix compactness refuted exactly no collatz resolution")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("656,640")) ||
        (page.problemId === "collatz" && !page.proofOrCounterexampleText.includes("LeastCounterexampleUniformHeightBound")) ||
        !page.proofOrCounterexampleText.includes("Candidate theorem") ||
        !page.proofOrCounterexampleText.includes("Obstruction") ||
        page.proofOrCounterexampleCards < 4 ||
        !page.candidateLemmaText.includes("Tool test") ||
        !page.candidateLemmaText.includes("Next revision") ||
        !page.candidateLemmaText.includes("upgrades the page status only after formal proof") ||
        page.candidateLemmaCards < 3 ||
        !page.machineSearchText.includes("Proof upgrade") ||
        !page.machineSearchText.includes("it is not a proof until") ||
        page.machineSearchCards < 3 ||
        !page.formalUpgradeText.includes("Acceptance test") ||
        !page.formalUpgradeText.includes("Every row except bounded_certificate") ||
        page.formalUpgradeRows < 4 ||
        !page.proofKernelText.includes("Shortcut risk") ||
        !page.proofKernelText.includes("Acceptance test") ||
        !page.proofKernelText.includes("K2-K4 replay successfully") ||
        page.proofKernelSteps < 5 ||
        !page.formalKernelAuditText.includes("contract pass but not proof") ||
        !page.formalKernelAuditText.includes("Expected fragments") ||
        !page.formalKernelAuditText.includes("does not prove the conjecture") ||
        page.formalKernelAuditRows < 4 ||
        !page.invalidShortcutText.includes("rejected shortcut") ||
        !page.invalidShortcutText.includes("Kill condition") ||
        !page.invalidShortcutText.includes("No proof candidate may enter review") ||
        page.invalidShortcutCards < 3 ||
        !page.aiSolverText.includes("Novel attempt") ||
        !page.aiSolverText.includes("Search Space") ||
        !page.aiSolverText.includes("Machine Output") ||
        !page.aiSolverText.includes("live AI-assisted attack plan") ||
        page.aiSolverSteps < 4 ||
        !page.aiBreakthroughText.includes("Source-informed baseline") ||
        !page.aiBreakthroughText.includes("New attack") ||
        !page.aiBreakthroughText.includes("Candidate theorem") ||
        !page.aiBreakthroughText.includes("Machine experiments") ||
        !page.aiBreakthroughText.includes("Red-team rules") ||
        !page.aiBreakthroughText.includes("active unsolved research program") ||
        !page.aiBreakthroughText.includes("not a proof claim") ||
        page.aiBreakthroughAnchors < 2 ||
        page.aiBreakthroughExperiments < 4 ||
        !page.aiProofForgeText.includes("Non-reproduction target") ||
        !page.aiProofForgeText.includes("Next theorem to attempt") ||
        !page.aiProofForgeText.includes("Lean statement draft") ||
        !page.aiProofForgeText.includes("Proof objects needed") ||
        !page.aiProofForgeText.includes("Theorem decomposition") ||
        !page.aiProofForgeText.includes("Highest risk") ||
        !page.aiProofForgeText.includes("Failure test") ||
        !page.aiProofForgeText.includes("open decomposition not proof") ||
        !page.aiProofForgeText.includes("Breakthrough object blueprint") ||
        !page.aiProofForgeText.includes("AI generation prompt") ||
        !page.aiProofForgeText.includes("Minimal counterexample") ||
        !page.aiProofForgeText.includes("Falsification oracle") ||
        !page.aiProofForgeText.includes("Formalization seed") ||
        !page.aiProofForgeText.includes("Counterexample-guided synthesis") ||
        !page.aiProofForgeText.includes("Candidate schema") ||
        !page.aiProofForgeText.includes("Forbidden assumptions") ||
        !page.aiProofForgeText.includes("Oracle pipeline") ||
        !page.aiProofForgeText.includes("Expected failure") ||
        !page.aiProofForgeText.includes("Top CEGIS candidate") ||
        !page.aiProofForgeText.includes("Ranking rule") ||
        !page.aiProofForgeText.includes("Priority score") ||
        !page.aiProofForgeText.includes("attack next") ||
        !page.aiProofForgeText.includes("cegis active no candidate proof") ||
        !page.aiProofForgeText.includes("Top attack theorem ticket") ||
        !page.aiProofForgeText.includes("Candidate theorem") ||
        !page.aiProofForgeText.includes("First counterexample oracle") ||
        !page.aiProofForgeText.includes("Required artifact") ||
        !page.aiProofForgeText.includes("Forbidden premises") ||
        !page.aiProofForgeText.includes("Output:") ||
        !page.aiProofForgeText.includes("Fail exit") ||
        !page.aiProofForgeText.includes("not a proof") ||
        !page.aiProofForgeText.includes("Search grammar") ||
        !page.aiProofForgeText.includes("Countermodel battery") ||
        !page.aiProofForgeText.includes("reproducing known finite checks does not count") ||
        !page.aiProofForgeText.includes("Promotion gate") ||
        !page.aiProofForgeText.includes("Discovery loop") ||
        !page.aiProofForgeText.includes("candidate generation active no solution") ||
        !page.aiProofForgeText.includes("Theorem pressure") ||
        !page.aiProofForgeText.includes("Attack runbook") ||
        !page.aiProofForgeText.includes("Falsification scorecard") ||
        !page.aiProofForgeText.includes("Cross-problem synthesis") ||
        !page.aiProofForgeText.includes("Transfer test") ||
        !page.aiProofForgeText.includes("Failure mode") ||
        !page.aiProofForgeText.includes("Portfolio decision") ||
        !page.aiProofForgeText.includes("Top candidate") ||
        !page.aiProofForgeText.includes("priority") ||
        !page.aiProofForgeText.includes("Required output") ||
        !page.aiProofForgeText.includes("Fail signal") ||
        page.aiProofForgeLemmaCards < 4 ||
        page.aiProofForgeBlueprintSteps < 3 ||
        page.aiProofForgeCegisCandidates < 2 ||
        page.aiProofForgeCegisRanking < 2 ||
        page.aiProofForgeTicketSections < 2 ||
        page.aiProofForgeTicketProtocol < 3 ||
        page.aiProofForgeExperiments < 3 ||
        page.aiProofForgeMutations < 3 ||
        page.aiProofForgeRunbook < 4 ||
        page.aiProofForgeScorecard < 4 ||
        page.aiProofForgeSynthesis < 4 ||
        page.aiProofForgePortfolio < 4 ||
        page.proofRouteCards < 4 ||
        !page.proofRouteTriageText.includes("routes triaged no full proof") ||
        !page.proofRouteTriageText.includes("current decisive route") ||
        !page.proofRouteTriageText.includes("Machine test") ||
        !page.proofRouteTriageText.includes("Required upgrade") ||
        !page.proofRouteTriageText.includes("cannot change the page status") ||
        page.decisiveTheoremSections < 4 ||
        !page.decisiveTheoremText.includes("decisive theorem open") ||
        !page.decisiveTheoremText.includes("missing formal theorem") ||
        !page.decisiveTheoremText.includes("Allowed Inputs") ||
        !page.decisiveTheoremText.includes("Forbidden Shortcuts") ||
        !page.decisiveTheoremText.includes("Machine Checks") ||
        !page.decisiveTheoremText.includes("formal_proof_verified or accepted_theorem") ||
        page.decisiveSubgoalCards < 5 ||
        !page.decisiveSubgoalText.includes("subgoals open") ||
        !page.decisiveSubgoalText.includes("complete bounded support") ||
        !page.decisiveSubgoalText.includes("open infinite bridge") ||
        !page.decisiveSubgoalText.includes("blocked until") ||
        !page.decisiveSubgoalText.includes("Closing test") ||
        !page.decisiveSubgoalText.includes("bounded support") ||
        page.decisiveTicketCards < 4 ||
        !page.decisiveTicketText.includes("attack tickets open") ||
        !page.decisiveTicketText.includes("planned not executed") ||
        !page.decisiveTicketText.includes("First experiment") ||
        !page.decisiveTicketText.includes("Falsification test") ||
        !page.decisiveTicketText.includes("Required output") ||
        !page.decisiveTicketText.includes("planned tickets are not proof artifacts") ||
        page.breakthroughCards < 3 ||
        !page.breakthroughText.includes("breakthrough agenda open") ||
        !page.breakthroughText.includes("research target not proof") ||
        !page.breakthroughText.includes("Minimum new theorem") ||
        !page.breakthroughText.includes("First artifact") ||
        !page.breakthroughText.includes("Kill condition") ||
        !page.breakthroughText.includes("not a proof claim") ||
        !page.certificateText.includes("bounded theorem certified") ||
        !page.certificateText.includes("scripts/verify_open_problem_workbench.py") ||
        !page.proofAttemptText.includes("open infinite obligation") ||
        !page.proofAttemptText.includes("proved by certificate") ||
        !page.proofAttemptText.includes("Falsification targets") ||
        !page.proofMapText.includes("Known theorem bridges") ||
        !page.proofMapText.includes("Lemma candidates") ||
        !page.proofMapText.includes("open bridge") ||
        !page.proofStatusGateText.includes("blocked open infinite obligation") ||
        !page.proofStatusGateText.includes("bounded theorem only") ||
        !page.proofStatusGateText.includes("Machine gate") ||
        page.proofExecutionStages < 5 ||
        !page.proofExecutionText.includes("blocked before full proof") ||
        !page.proofExecutionText.includes("Current frontier") ||
        !page.proofExecutionText.includes("Next experiment") ||
        !page.proofExecutionText.includes("Failure signal") ||
        !page.proofExecutionText.includes("full proof promotion gate") ||
        !page.proofFrontierText.includes("finite probe not proof") ||
        !page.proofFrontierText.includes("Stress Metrics") ||
        !page.proofFrontierText.includes("Proof pressure") ||
        !page.proofFrontierText.includes("Failure signal") ||
        page.knownBarrierCards < 4 ||
        !page.knownBarrierText.includes("barriers not cleared") ||
        !page.knownBarrierText.includes("Clearance") ||
        !page.knownBarrierText.includes("finite_to_infinite_lift") ||
        page.formalReplayArtifacts < 3 ||
        !page.formalReplayText.includes("not replayable until barriers clear") ||
        !page.formalReplayText.includes("Replay commands") ||
        !page.formalReplayText.includes("Forbidden tokens") ||
        !page.formalReplayText.includes("lake env lean") ||
        page.proofReviewCards < 4 ||
        !page.proofReviewText.includes("full proof not accepted") ||
        !page.proofReviewText.includes("accepted for committed limit") ||
        !page.proofReviewText.includes("rejected currently") ||
        !page.proofReviewText.includes("Minimum acceptance conditions") ||
        page.proofReductionPartials < 2 ||
        !page.proofReductionText.includes("target reduction open") ||
        !page.proofReductionText.includes("Decisive reduction") ||
        !page.proofReductionText.includes("Forbidden shortcuts") ||
        !page.proofReductionText.includes("Promotion test") ||
        page.proofCandidateTests < 6 ||
        !page.proofCandidateText.includes("no candidate accepted") ||
        !page.proofCandidateText.includes("Required submission") ||
        !page.proofCandidateText.includes("First executable tests") ||
        !page.proofCandidateText.includes("Automatic rejection rules") ||
        page.proofExecutionLogCards < 2 ||
        !page.proofExecutionLogText.includes("attempts executed no full proof") ||
        !page.proofExecutionLogText.includes("Machine check") ||
        !page.proofExecutionLogText.includes("Next artifact") ||
        !page.proofExecutionLogText.includes("Machine verdict") ||
        page.proofDagNodes < 10 ||
        page.proofDagEdges < 10 ||
        !page.proofDagText.includes("open obligation graph") ||
        !page.proofDagText.includes("Critical path") ||
        !page.proofDagText.includes("Machine rule") ||
        page.formalSkeletonFiles < 4 ||
        !page.formalSkeletonText.includes("skeleton present not replayable") ||
        !page.formalSkeletonText.includes("Forbidden hits") ||
        !page.formalSkeletonText.includes("not a proof") ||
        !page.formalContractText.includes("Lean 4") ||
        !page.formalContractText.includes("Forbidden assumptions") ||
        !page.formalContractText.includes("No `sorry`") ||
        page.milestoneCount < 5 ||
        !page.milestoneQueueText.includes("bounded only infinite proof open") ||
        !page.milestoneQueueText.includes("complete") ||
        !page.milestoneQueueText.includes("open infinite bridge") ||
        !page.decisiveLemmaText.includes("active not proven") ||
        !page.decisiveLemmaText.includes("Candidate statement") ||
        !page.decisiveLemmaText.includes("Proof Obligation") ||
        !page.decisiveLemmaText.includes("Falsification Test") ||
        !page.decisiveLemmaText.includes("Automated Falsification Probe") ||
        !page.decisiveLemmaText.includes("bounded probe passed proof open") ||
        !page.decisiveLemmaText.includes("probe payload certified") ||
        !page.decisiveLemmaText.includes("Merkle root") ||
        !page.decisiveLemmaText.includes("Proof Gap Taxonomy") ||
        !page.decisiveLemmaText.includes("proof gaps open") ||
        !page.decisiveLemmaText.includes("Required artifact") ||
        !page.decisiveLemmaText.includes("Next experiment") ||
        !page.decisiveLemmaText.includes("Failure signal") ||
        !page.decisiveLemmaText.includes("proof") ||
        !page.text.includes("Proof Gates") ||
        !page.text.includes("Candidate Strategy") ||
        !page.text.includes("No proof claim"),
    )
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  const collatzPage = metrics.openProblemPages.find((page) => page.problemId === "collatz");
  if (
    !collatzPage ||
    !collatzPage.proofOrCounterexampleText.includes("Phase-wrap probe") ||
    !collatzPage.proofOrCounterexampleText.includes("pressure_cycle_counterexample_refutes_clause_rank") ||
    !collatzPage.proofOrCounterexampleText.includes("[11] -> [12]")
  ) {
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
    !metrics.sideNavText.includes("Research Atlas") ||
    metrics.proofWorkbenchHref !== "Proof Workbench" ||
    metrics.riemannNavHref !== "Riemann Hypothesis" ||
    metrics.collatzNavHref !== "Collatz Conjecture" ||
    metrics.goldbachNavHref !== "Goldbach Conjecture" ||
    metrics.twinPrimeNavHref !== "Twin Prime Workbench" ||
    !metrics.controlBeforeNotes
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  const evolutionRequiredText = [
    ["panel", metrics.evolutionPanel, "Project Evolution"],
    ["summary", metrics.evolutionSummary, "Generator baselines"],
    ["summary", metrics.evolutionSummary, "0"],
    ["summary", metrics.evolutionSummary, "1 public control"],
    ["summary", metrics.evolutionSummary, "2 profiles"],
    ["summary", metrics.evolutionSummary, "5,000 null iterations"],
    ["impact", metrics.evolutionImpact, "Project Logic"],
    ["impact", metrics.evolutionImpact, "Supported"],
    ["impact", metrics.evolutionImpact, "Not supported yet"],
    ["impact", metrics.evolutionImpact, "Next decisive test"],
    ["impact", metrics.evolutionImpact, "Visual Change Trail"],
    ["impact", metrics.evolutionImpact, "Hardening Map"],
    ["impact", metrics.evolutionImpact, "feature_vector_path_public_relative"],
    ["impact", metrics.evolutionImpact, "Scale lift"],
    ["impact", metrics.evolutionImpact, "Publication guardrails"],
    ["impact", metrics.evolutionImpact, "Boundary state obstruction"],
    ["impact", metrics.evolutionImpact, "2^28 first deterministic"],
    ["impact", metrics.evolutionImpact, "Lift stability refuted"],
    ["impact", metrics.evolutionImpact, "3,086 projection escapes"],
    ["impact", metrics.evolutionImpact, "Cylinder coordinate gap"],
    ["impact", metrics.evolutionImpact, "41,472 extensions"],
    ["impact", metrics.evolutionImpact, "Failure-offset separator"],
    ["impact", metrics.evolutionImpact, "58 mixed"],
    ["impact", metrics.evolutionImpact, "Pre-replay separator"],
    ["impact", metrics.evolutionImpact, "mod 16"],
    ["impact", metrics.evolutionImpact, "Mod16 lift survival"],
    ["impact", metrics.evolutionImpact, "52/56-bit lifts"],
    ["impact", metrics.evolutionImpact, "Mod16 automaton table"],
    ["impact", metrics.evolutionImpact, "60-bit chain"],
    ["impact", metrics.evolutionImpact, "Symbolic gate obstruction"],
    ["impact", metrics.evolutionImpact, "64-bit gate"],
    ["impact", metrics.evolutionImpact, "Refined DAG frontier"],
    ["impact", metrics.evolutionImpact, "9,616 states"],
    ["impact", metrics.evolutionImpact, "tail/residue-only"],
    ["impact", metrics.evolutionImpact, "Rank frontier audit"],
    ["impact", metrics.evolutionImpact, "6,649 frontier"],
    ["impact", metrics.evolutionImpact, "Frontier closure refuted"],
    ["impact", metrics.evolutionImpact, "155,321 nondecreasing"],
    ["impact", metrics.evolutionImpact, "Bounded separator tradeoff"],
    ["impact", metrics.evolutionImpact, "22,219 compact"],
    ["impact", metrics.evolutionImpact, "0 mixed full-word"],
    ["impact", metrics.evolutionImpact, "Persistent lift-chain pressure"],
    ["impact", metrics.evolutionImpact, "4,142 second"],
    ["impact", metrics.evolutionImpact, "6,448 third"],
    ["impact", metrics.evolutionImpact, "11 guard checks"],
    ["spine", metrics.evolutionSpine, "Evidence Spine"],
    ["spine", metrics.evolutionSpine, "Sim-to-Real"],
    ["spine", metrics.evolutionSpine, "fixture audit"],
    ["spine", metrics.evolutionSpine, "21 checked artifacts"],
    ["spine", metrics.evolutionSpine, "publication consistency"],
    ["delta", metrics.evolutionDelta, "Claim Boundaries"],
    ["delta", metrics.evolutionDelta, "controlled grid + null + replication"],
    ["delta", metrics.evolutionDelta, "Real-world generator attribution"],
    ["delta", metrics.evolutionDelta, "Bitcoin wallet/library attribution"],
    ["panel", metrics.evolutionPanel, "Crypto-classifier baseline"],
    ["panel", metrics.evolutionPanel, "Collection handoff"],
    ["panel", metrics.evolutionPanel, "Collection intake"],
    ["panel", metrics.evolutionPanel, "collection matrix"],
    ["panel", metrics.evolutionPanel, "Sample power"],
    ["panel", metrics.evolutionPanel, "Provenance"],
    ["panel", metrics.evolutionPanel, "Evidence pack"],
    ["panel", metrics.evolutionPanel, "Publication consistency"],
    ["panel", metrics.evolutionPanel, "TICKET-57"],
    ["panel", metrics.evolutionPanel, "TICKET-58"],
    ["panel", metrics.evolutionPanel, "TICKET-59"],
    ["panel", metrics.evolutionPanel, "TICKET-60"],
    ["panel", metrics.evolutionPanel, "TICKET-61"],
    ["panel", metrics.evolutionPanel, "TICKET-62"],
    ["panel", metrics.evolutionPanel, "TICKET-63"],
    ["panel", metrics.evolutionPanel, "TICKET-64"],
    ["panel", metrics.evolutionPanel, "TICKET-65"],
    ["panel", metrics.evolutionPanel, "TICKET-66"],
    ["panel", metrics.evolutionPanel, "TICKET-67"],
    ["panel", metrics.evolutionPanel, "TICKET-68"],
    ["panel", metrics.evolutionPanel, "TICKET-70"],
    ["panel", metrics.evolutionPanel, "TICKET-71"],
    ["panel", metrics.evolutionPanel, "TICKET-72"],
    ["panel", metrics.evolutionPanel, "TICKET-73"],
    ["panel", metrics.evolutionPanel, "TICKET-74"],
  ];
  const missingEvolutionChecks = evolutionRequiredText
    .filter(([, actual, expectedText]) => !String(actual).includes(expectedText))
    .map(([section, , expectedText]) => `${section}: ${expectedText}`);
  if (missingEvolutionChecks.length > 0) {
    console.error(JSON.stringify({ errors, missingEvolutionChecks }, null, 2));
    process.exit(1);
  }
  if (
    metrics.atlasContributions < 4 ||
    metrics.atlasLadderSteps < 5 ||
    metrics.atlasProofCards < 4 ||
    metrics.atlasNextCards < 4 ||
    !metrics.atlasPanel.includes("Research Atlas") ||
    !metrics.atlasPanel.includes("PrimeProject is now best understood") ||
    !metrics.atlasPanel.includes("Scale made visible") ||
    !metrics.atlasPanel.includes("Sim-to-real boundary exposed") ||
    !metrics.atlasPanel.includes("Publication claims governed") ||
    !metrics.atlasPanel.includes("Evidence ladder") ||
    !metrics.atlasPanel.includes("Proof workbench") ||
    !metrics.atlasPanel.includes("Riemann Hypothesis") ||
    !metrics.atlasPanel.includes("Twin Prime Conjecture") ||
    !metrics.atlasPanel.includes("Next academic work")
  ) {
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
    !metrics.evolutionImpact.includes("Hardening Map") ||
    !metrics.evolutionImpact.includes("feature_vector_path_public_relative") ||
    !metrics.evolutionImpact.includes("Scale lift") ||
    !metrics.evolutionImpact.includes("Publication guardrails") ||
    !metrics.evolutionImpact.includes("Boundary state obstruction") ||
    !metrics.evolutionImpact.includes("2^28 first deterministic") ||
    !metrics.evolutionImpact.includes("Lift stability refuted") ||
    !metrics.evolutionImpact.includes("3,086 projection escapes") ||
    !metrics.evolutionImpact.includes("Cylinder coordinate gap") ||
    !metrics.evolutionImpact.includes("41,472 extensions") ||
    !metrics.evolutionImpact.includes("Failure-offset separator") ||
    !metrics.evolutionImpact.includes("58 mixed") ||
    !metrics.evolutionImpact.includes("Pre-replay separator") ||
    !metrics.evolutionImpact.includes("mod 16") ||
    !metrics.evolutionImpact.includes("Mod16 lift survival") ||
    !metrics.evolutionImpact.includes("52/56-bit lifts") ||
    !metrics.evolutionImpact.includes("Mod16 automaton table") ||
    !metrics.evolutionImpact.includes("60-bit chain") ||
    !metrics.evolutionImpact.includes("Symbolic gate obstruction") ||
    !metrics.evolutionImpact.includes("64-bit gate") ||
    !metrics.evolutionImpact.includes("Refined DAG frontier") ||
    !metrics.evolutionImpact.includes("9,616 states") ||
    !metrics.evolutionImpact.includes("tail/residue-only") ||
    !metrics.evolutionImpact.includes("Rank frontier audit") ||
    !metrics.evolutionImpact.includes("6,649 frontier") ||
    !metrics.evolutionImpact.includes("Frontier closure refuted") ||
    !metrics.evolutionImpact.includes("155,321 nondecreasing") ||
    !metrics.evolutionImpact.includes("Bounded separator tradeoff") ||
    !metrics.evolutionImpact.includes("22,219 compact") ||
    !metrics.evolutionImpact.includes("0 mixed full-word") ||
    !metrics.evolutionImpact.includes("Persistent lift-chain pressure") ||
    !metrics.evolutionImpact.includes("4,142 second") ||
    !metrics.evolutionImpact.includes("6,448 third") ||
    !metrics.evolutionImpact.includes("Strict re-entry tree exhausted") ||
    !metrics.evolutionImpact.includes("4,142 roots") ||
    !metrics.evolutionImpact.includes("2,873 -> 0") ||
    !metrics.evolutionImpact.includes("Coverage leakage exposed") ||
    !metrics.evolutionImpact.includes("Finite-coordinate closure blocked") ||
    !metrics.evolutionImpact.includes("Boundary recurrence isolated") ||
    !metrics.evolutionImpact.includes("Fixed-prefix ghost classified") ||
    !metrics.evolutionImpact.includes("Finite 2-adic separator blocked") ||
    !metrics.evolutionImpact.includes("15,696 escapes") ||
    !metrics.evolutionImpact.includes("78,315 sixth") ||
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
    !metrics.evolutionPanel.includes("Publication consistency") ||
    !metrics.evolutionPanel.includes("TICKET-57") ||
    !metrics.evolutionPanel.includes("TICKET-58") ||
    !metrics.evolutionPanel.includes("TICKET-59") ||
    !metrics.evolutionPanel.includes("TICKET-60") ||
    !metrics.evolutionPanel.includes("TICKET-61") ||
    !metrics.evolutionPanel.includes("TICKET-62") ||
    !metrics.evolutionPanel.includes("TICKET-63") ||
    !metrics.evolutionPanel.includes("TICKET-64") ||
    !metrics.evolutionPanel.includes("TICKET-65") ||
    !metrics.evolutionPanel.includes("TICKET-66") ||
    !metrics.evolutionPanel.includes("TICKET-67") ||
    !metrics.evolutionPanel.includes("TICKET-68") ||
    !metrics.evolutionPanel.includes("TICKET-70") ||
    !metrics.evolutionPanel.includes("TICKET-71") ||
    !metrics.evolutionPanel.includes("TICKET-72") ||
    !metrics.evolutionPanel.includes("TICKET-73") ||
    !metrics.evolutionPanel.includes("TICKET-74") ||
    !metrics.evolutionPanel.includes("TICKET-77") ||
    !metrics.evolutionPanel.includes("TICKET-78") ||
    !metrics.evolutionPanel.includes("TICKET-79") ||
    !metrics.evolutionPanel.includes("TICKET-80") ||
    !metrics.evolutionPanel.includes("TICKET-81") ||
    !metrics.evolutionPanel.includes("TICKET-82") ||
    !metrics.evolutionPanel.includes("TICKET-83") ||
    !metrics.evolutionPanel.includes("TICKET-84") ||
    !metrics.evolutionPanel.includes("TICKET-85") ||
    !metrics.evolutionPanel.includes("TICKET-86") ||
    !metrics.evolutionPanel.includes("TICKET-87") ||
    !metrics.evolutionPanel.includes("TICKET-88") ||
    !metrics.evolutionPanel.includes("TICKET-89") ||
    !metrics.evolutionPanel.includes("TICKET-90") ||
    !metrics.evolutionPanel.includes("TICKET-91") ||
    !metrics.evolutionPanel.includes("TICKET-92") ||
    !metrics.evolutionPanel.includes("TICKET-93") ||
    !metrics.evolutionPanel.includes("TICKET-94") ||
    !metrics.evolutionPanel.includes("TICKET-95") ||
    !metrics.evolutionPanel.includes("TICKET-96") ||
    !metrics.evolutionPanel.includes("TICKET-97") ||
    !metrics.evolutionPanel.includes("TICKET-98") ||
    !metrics.evolutionPanel.includes("TICKET-99") ||
    !metrics.evolutionPanel.includes("TICKET-100") ||
    !metrics.evolutionPanel.includes("TICKET-101") ||
    !metrics.evolutionPanel.includes("TICKET-102") ||
    !metrics.evolutionPanel.includes("TICKET-103") ||
    !metrics.evolutionPanel.includes("TICKET-104") ||
    !metrics.evolutionPanel.includes("TICKET-105") ||
    !metrics.evolutionPanel.includes("TICKET-106") ||
    !metrics.evolutionPanel.includes("TICKET-107") ||
    !metrics.evolutionPanel.includes("TICKET-108") ||
    !metrics.evolutionPanel.includes("TICKET-109") ||
    !metrics.evolutionPanel.includes("TICKET-110") ||
    !metrics.evolutionPanel.includes("TICKET-111") ||
    !metrics.evolutionPanel.includes("TICKET-112") ||
    !metrics.evolutionPanel.includes("TICKET-113") ||
    !metrics.evolutionPanel.includes("TICKET-114") ||
    !metrics.evolutionPanel.includes("TICKET-115") ||
    !metrics.evolutionPanel.includes("TICKET-116") ||
    !metrics.evolutionPanel.includes("TICKET-117") ||
    !metrics.evolutionPanel.includes("TICKET-118") ||
    !metrics.evolutionPanel.includes("TICKET-119") ||
    !metrics.evolutionPanel.includes("TICKET-120") ||
    !metrics.evolutionPanel.includes("TICKET-121")
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
    metrics.collectionFixtureAuditRows < 10 ||
    !metrics.collectionFixtureAuditStatus.includes("pass") ||
    !metrics.collectionFixtureAuditSummary.includes("10") ||
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
    !metrics.artifactLineageSummary.includes("24 nodes") ||
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
    !metrics.evidencePanel.includes(
      `${formatNumber(publicData.evolution.metrics?.claim_language_guarded_mentions || 0)} guarded`,
    ) ||
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
  const candidatePorts = [41731, 41732, 41733, 41734, 41735, 41736, 41737, 41738, 41739];
  const listenAt = (index) =>
    new Promise((resolve, reject) => {
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
      const onError = (error) => {
        server.close(() => {});
        if (error && error.code === "EADDRINUSE" && index + 1 < candidatePorts.length) {
          listenAt(index + 1).then(resolve, reject);
          return;
        }
        reject(error);
      };
      server.once("error", onError);
      server.listen(candidatePorts[index], "127.0.0.1", () => {
        server.off("error", onError);
        const address = server.address();
        resolve({ server, url: `http://127.0.0.1:${address.port}/index.html` });
      });
    });
  return listenAt(0);
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
