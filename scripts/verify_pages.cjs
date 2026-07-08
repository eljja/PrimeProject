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
    metrics.proofHub?.linkCount !== 5 ||
    !metrics.proofHub?.links.includes("riemann.html") ||
    !metrics.proofHub?.links.includes("collatz.html") ||
    !metrics.proofHub?.links.includes("goldbach.html") ||
    !metrics.proofHub?.links.includes("twin-prime.html") ||
    !metrics.proofHub?.links.includes("../docs/proof-or-counterexample-program.md") ||
    !metrics.proofHub?.boundary.includes("Proof or Counterexample Program") ||
    !metrics.proofHub?.boundary.includes("not present a conjecture as solved")
  ) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
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
