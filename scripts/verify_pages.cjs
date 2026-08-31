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
  const ticket242Load = openProblemSource.indexOf("const ticket242Loaded = await loadTicket242Attempt();");
  const ticket245Load = openProblemSource.indexOf("const ticket245Loaded = await loadTicket245Attempt();");
  const ticket246Load = openProblemSource.indexOf("const ticket246Loaded = await loadTicket246Attempt();");
  const ticket247Load = openProblemSource.indexOf("const ticket247Loaded = await loadTicket247Attempt();");
  const ticket248Load = openProblemSource.indexOf("const ticket248Loaded = await loadTicket248Attempt();");
  const ticket249Load = openProblemSource.indexOf("const ticket249Loaded = await loadTicket249Attempt();");
  const ticket250Load = openProblemSource.indexOf("const ticket250Loaded = await loadTicket250Attempt();");
  const ticket264Load = openProblemSource.indexOf("const ticket264Loaded = await loadTicket264Attempt();");
  const ticket263Load = openProblemSource.indexOf("const ticket263Loaded = await loadTicket263Attempt();");
  const ticket262Load = openProblemSource.indexOf("const ticket262Loaded = await loadTicket262Attempt();");
  const ticket261Load = openProblemSource.indexOf("const ticket261Loaded = await loadTicket261Attempt();");
  const ticket260Load = openProblemSource.indexOf("const ticket260Loaded = await loadTicket260Attempt();");
  const ticket259Load = openProblemSource.indexOf("const ticket259Loaded = await loadTicket259Attempt();");
  const ticket258Load = openProblemSource.indexOf("const ticket258Loaded = await loadTicket258Attempt();");
  const ticket257Load = openProblemSource.indexOf("const ticket257Loaded = await loadTicket257Attempt();");
  const ticket256Load = openProblemSource.indexOf("const ticket256Loaded = await loadTicket256Attempt();");
  const ticket255Load = openProblemSource.indexOf("const ticket255Loaded = await loadTicket255Attempt();");
  const ticket254Load = openProblemSource.indexOf("const ticket254Loaded = await loadTicket254Attempt();");
  const ticket253Load = openProblemSource.indexOf("const ticket253Loaded = await loadTicket253Attempt();");
  const ticket252Load = openProblemSource.indexOf("const ticket252Loaded = await loadTicket252Attempt();");
  const ticket251Load = openProblemSource.indexOf("const ticket251Loaded = await loadTicket251Attempt();");
  const ticket244Load = openProblemSource.indexOf("const ticket244Loaded = await loadTicket244Attempt();");
  const ticket243Load = openProblemSource.indexOf("const ticket243Loaded = await loadTicket243Attempt();");
  const ticket241Load = openProblemSource.indexOf("const ticket241Loaded = await loadTicket241Attempt();");
  const ticket240Load = openProblemSource.indexOf("const ticket240Loaded = await loadTicket240Attempt();");
  const ticket239Load = openProblemSource.indexOf("const ticket239Loaded = await loadTicket239Attempt();");
  const ticket238Load = openProblemSource.indexOf("const ticket238Loaded = await loadTicket238Attempt();");
  const ticket237Load = openProblemSource.indexOf("const ticket237Loaded = await loadTicket237Attempt();");
  const ticket236Load = openProblemSource.indexOf("const ticket236Loaded = await loadTicket236Attempt();");
  const ticket235Load = openProblemSource.indexOf("const ticket235Loaded = await loadTicket235Attempt();");
  const ticket234Load = openProblemSource.indexOf("const ticket234Loaded = await loadTicket234Attempt();");
  const ticket233Load = openProblemSource.indexOf("const ticket233Loaded = await loadTicket233Attempt();");
  const ticket232Load = openProblemSource.indexOf("const ticket232Loaded = await loadTicket232Attempt();");
  const ticket231Load = openProblemSource.indexOf("const ticket231Loaded = await loadTicket231Attempt();");
  const ticket230Load = openProblemSource.indexOf("const ticket230Loaded = await loadTicket230Attempt();");
  const ticket229Load = openProblemSource.indexOf("const ticket229Loaded = await loadTicket229Attempt();");
  const ticket228Load = openProblemSource.indexOf("const ticket228Loaded = await loadTicket228Attempt();");
  const ticket227Load = openProblemSource.indexOf("const ticket227Loaded = await loadTicket227Attempt();");
  const ticket226Load = openProblemSource.indexOf("const ticket226Loaded = await loadTicket226Attempt();");
  const ticket225Load = openProblemSource.indexOf("const ticket225Loaded = await loadTicket225Attempt();");
  const ticket224Load = openProblemSource.indexOf("const ticket224Loaded = await loadTicket224Attempt();");
  const ticket223Load = openProblemSource.indexOf("const ticket223Loaded = await loadTicket223Attempt();");
  const ticket222Load = openProblemSource.indexOf("const ticket222Loaded = await loadTicket222Attempt();");
  const ticket221Load = openProblemSource.indexOf("const ticket221Loaded = await loadTicket221Attempt();");
  const ticket240EarlyRender = openProblemSource.indexOf("render(payload, problem);", ticket240Load);
  const ticket220Load = openProblemSource.indexOf("const ticket220Loaded = await loadTicket220Attempt();");
  const ticket219Load = openProblemSource.indexOf("const ticket219Loaded = await loadTicket219Attempt();");
  const ticket218Load = openProblemSource.indexOf("const ticket218Loaded = await loadTicket218Attempt();");
  const ticket217Load = openProblemSource.indexOf("const ticket217Loaded = await loadTicket217Attempt();");
  const ticket216Load = openProblemSource.indexOf("const ticket216Loaded = await loadTicket216Attempt();");
  const ticket215Load = openProblemSource.indexOf("const ticket215Loaded = await loadTicket215Attempt();");
  const ticket214Load = openProblemSource.indexOf("const ticket214Loaded = await loadTicket214Attempt();");
  const ticket213Load = openProblemSource.indexOf("const ticket213Loaded = await loadTicket213Attempt();");
  const ticket212Load = openProblemSource.indexOf("const ticket212Loaded = await loadTicket212Attempt();");
  const ticket211Load = openProblemSource.indexOf("const ticket211Loaded = await loadTicket211Attempt();");
  const ticket210Load = openProblemSource.indexOf("const ticket210Loaded = await loadTicket210Attempt();");
  const ticket209Load = openProblemSource.indexOf("const ticket209Loaded = await loadTicket209Attempt();");
  const ticket208Load = openProblemSource.indexOf("const ticket208Loaded = await loadTicket208Attempt();");
  const ticket207Load = openProblemSource.indexOf("const ticket207Loaded = await loadTicket207Attempt();");
  const ticket206Load = openProblemSource.indexOf("const ticket206Loaded = await loadTicket206Attempt();");
  const ticket205Load = openProblemSource.indexOf("const ticket205Loaded = await loadTicket205Attempt();");
  const ticket204Load = openProblemSource.indexOf("const ticket204Loaded = await loadTicket204Attempt();");
  const ticket203Load = openProblemSource.indexOf("const ticket203Loaded = await loadTicket203Attempt();");
  const ticket202Load = openProblemSource.indexOf("const ticket202Loaded = await loadTicket202Attempt();");
  const ticket201Load = openProblemSource.indexOf("const ticket201Loaded = await loadTicket201Attempt();");
  const ticket200Load = openProblemSource.indexOf("const ticket200Loaded = await loadTicket200Attempt();");
  const ticket199Load = openProblemSource.indexOf("const ticket199Loaded = await loadTicket199Attempt();");
  const ticket198Load = openProblemSource.indexOf("const ticket198Loaded = await loadTicket198Attempt();");
  const ticket197Load = openProblemSource.indexOf("const ticket197Loaded = await loadTicket197Attempt();");
  const ticket196Load = openProblemSource.indexOf("const ticket196Loaded = await loadTicket196Attempt();");
  const ticket195Load = openProblemSource.indexOf("const ticket195Loaded = await loadTicket195Attempt();");
  const ticket194Load = openProblemSource.indexOf("const ticket194Loaded = await loadTicket194Attempt();");
  const ticket193Load = openProblemSource.indexOf("const ticket193Loaded = await loadTicket193Attempt();");
  const ticket192Load = openProblemSource.indexOf("const ticket192Loaded = await loadTicket192Attempt();");
  const ticket191Load = openProblemSource.indexOf("const ticket191Loaded = await loadTicket191Attempt();");
  const ticket190Load = openProblemSource.indexOf("const ticket190Loaded = await loadTicket190Attempt();");
  const ticket189Load = openProblemSource.indexOf("const ticket189Loaded = await loadTicket189Attempt();");
  const ticket188Load = openProblemSource.indexOf("const ticket188Loaded = await loadTicket188Attempt();");
  const ticket187Load = openProblemSource.indexOf("const ticket187Loaded = await loadTicket187Attempt();");
  const ticket186Load = openProblemSource.indexOf("const ticket186Loaded = await loadTicket186Attempt();");
  const ticket185Load = openProblemSource.indexOf("const ticket185Loaded = await loadTicket185Attempt();");
  const ticket184Load = openProblemSource.indexOf("const ticket184Loaded = await loadTicket184Attempt();");
  const ticket183Load = openProblemSource.indexOf("const ticket183Loaded = await loadTicket183Attempt();");
  const ticket182Load = openProblemSource.indexOf("const ticket182Loaded = await loadTicket182Attempt();");
  const ticket181Load = openProblemSource.indexOf("const ticket181Loaded = await loadTicket181Attempt();");
  const ticket180Load = openProblemSource.indexOf("const ticket180Loaded = await loadTicket180Attempt();");
  const ticket179Load = openProblemSource.indexOf("const ticket179Loaded = await loadTicket179Attempt();");
  const ticket178Load = openProblemSource.indexOf("const ticket178Loaded = await loadTicket178Attempt();");
  const ticket177Load = openProblemSource.indexOf("const ticket177Loaded = await loadTicket177Attempt();");
  const ticket176Load = openProblemSource.indexOf("const ticket176Loaded = await loadTicket176Attempt();");
  const ticket175Load = openProblemSource.indexOf("const ticket175Loaded = await loadTicket175Attempt();");
  const ticket174Load = openProblemSource.indexOf("const ticket174Loaded = await loadTicket174Attempt();");
  const ticket173Load = openProblemSource.indexOf("const ticket173Loaded = await loadTicket173Attempt();");
  const ticket172Load = openProblemSource.indexOf("const ticket172Loaded = await loadTicket172Attempt();");
  const ticket171Load = openProblemSource.indexOf("const ticket171Loaded = await loadTicket171Attempt();");
  const ticket170Load = openProblemSource.indexOf("const ticket170Loaded = await loadTicket170Attempt();");
  const ticket169Load = openProblemSource.indexOf("const ticket169Loaded = await loadTicket169Attempt();");
  const priorityLoad = openProblemSource.indexOf("const priorityLoads = await Promise.all([loadTicket168Attempt(), loadTicket167Attempt(), loadTicket166Attempt()");
  const priorityRender = openProblemSource.indexOf("render(payload, problem);", priorityLoad);
  const historicalLoad = openProblemSource.indexOf("const labResponse = await fetch", priorityRender);
  if (!(ticket243Load >= 0 && ticket243Load < ticket242Load && ticket242Load < ticket241Load && ticket241Load < ticket240Load && ticket240Load < ticket239Load && ticket239Load < ticket238Load && ticket238Load < ticket237Load && ticket237Load < ticket236Load && ticket236Load < ticket235Load && ticket235Load < ticket234Load && ticket234Load < ticket233Load && ticket233Load < ticket232Load && ticket232Load < ticket231Load && ticket231Load < ticket230Load && ticket230Load < ticket229Load && ticket229Load < ticket228Load && ticket228Load < ticket227Load && ticket227Load < ticket226Load && ticket226Load < ticket225Load && ticket225Load < ticket224Load && ticket224Load < ticket223Load && ticket223Load < ticket222Load && ticket222Load < ticket221Load && ticket221Load < ticket220Load && ticket220Load < ticket240EarlyRender && ticket240EarlyRender < ticket219Load && ticket219Load < ticket218Load && ticket218Load < ticket217Load && ticket217Load < ticket216Load && ticket216Load < ticket215Load && ticket215Load < ticket214Load && ticket214Load < ticket213Load && ticket213Load < ticket212Load && ticket212Load < ticket211Load && ticket211Load < ticket210Load && ticket210Load < ticket209Load && ticket209Load < ticket208Load && ticket208Load < ticket207Load && ticket207Load < ticket206Load && ticket206Load < ticket205Load && ticket205Load < ticket204Load && ticket204Load < ticket203Load && ticket203Load < ticket202Load && ticket202Load < ticket201Load && ticket201Load < ticket200Load && ticket200Load < ticket199Load && ticket199Load < ticket198Load && ticket198Load < ticket197Load && ticket197Load < ticket196Load && ticket196Load < ticket195Load && ticket195Load < ticket194Load && ticket194Load < ticket193Load && ticket193Load < ticket192Load && ticket192Load < ticket191Load && ticket191Load < ticket190Load && ticket190Load < ticket189Load && ticket189Load < ticket188Load && ticket188Load < ticket187Load && ticket187Load < ticket186Load && ticket186Load < ticket185Load && ticket185Load < ticket184Load && ticket184Load < ticket183Load && ticket183Load < ticket182Load && ticket182Load < ticket181Load && ticket181Load < ticket180Load && ticket180Load < ticket179Load && ticket179Load < ticket178Load && ticket178Load < ticket177Load && ticket177Load < ticket176Load && ticket176Load < ticket175Load && ticket175Load < ticket174Load && ticket174Load < ticket173Load && ticket173Load < ticket172Load && ticket172Load < ticket171Load && ticket171Load < ticket170Load && ticket170Load < ticket169Load && ticket169Load < priorityLoad && priorityLoad < priorityRender && priorityRender < historicalLoad)) {
  if (!(ticket245Load >= 0 && ticket245Load < ticket244Load)) {
  if (!(ticket246Load >= 0 && ticket246Load < ticket245Load)) {
    errors.push("TICKET246 must load before TICKET245");
  }
  if (!(ticket247Load >= 0 && ticket247Load < ticket246Load)) {
    errors.push("TICKET247 must load before TICKET246");
  }
  if (!(ticket248Load >= 0 && ticket248Load < ticket247Load)) {
    errors.push("TICKET248 must load before TICKET247");
  }
  if (!(ticket249Load >= 0 && ticket249Load < ticket248Load)) {
    errors.push("TICKET249 must load before TICKET248");
  }
    errors.push("TICKET245 must load before TICKET244");
  }
  if (!(ticket244Load >= 0 && ticket244Load < ticket243Load)) {
    errors.push("TICKET244 must load before TICKET243");
  }
    errors.push("TICKET243 must render before archive loading, and TICKET243 through TICKET125 must precede historical ticket loading");
  }
  if (!(ticket250Load >= 0 && ticket250Load < ticket249Load)) {
    errors.push("TICKET250 must load before TICKET249");
  }
  if (!(ticket264Load >= 0 && ticket264Load < ticket263Load)) {
    errors.push("TICKET264 must load before TICKET263");
  }
  if (!(ticket263Load >= 0 && ticket263Load < ticket262Load)) {
    errors.push("TICKET263 must load before TICKET262");
  }
  if (!(ticket262Load >= 0 && ticket262Load < ticket261Load)) {
    errors.push("TICKET262 must load before TICKET261");
  }
  if (!(ticket261Load >= 0 && ticket261Load < ticket260Load)) {
    errors.push("TICKET261 must load before TICKET260");
  }
  if (!(ticket260Load >= 0 && ticket260Load < ticket259Load)) {
    errors.push("TICKET260 must load before TICKET259");
  }
  if (!(ticket259Load >= 0 && ticket259Load < ticket258Load)) {
    errors.push("TICKET259 must load before TICKET258");
  }
  if (!(ticket258Load >= 0 && ticket258Load < ticket257Load)) {
    errors.push("TICKET258 must load before TICKET257");
  }
  if (!(ticket257Load >= 0 && ticket257Load < ticket256Load)) {
    errors.push("TICKET257 must load before TICKET256");
  }
  if (!(ticket256Load >= 0 && ticket256Load < ticket255Load)) {
    errors.push("TICKET256 must load before TICKET255");
  }
  if (!(ticket255Load >= 0 && ticket255Load < ticket254Load)) {
    errors.push("TICKET255 must load before TICKET254");
  }
  if (!(ticket254Load >= 0 && ticket254Load < ticket253Load)) {
    errors.push("TICKET254 must load before TICKET253");
  }
  if (!(ticket253Load >= 0 && ticket253Load < ticket252Load)) {
    errors.push("TICKET253 must load before TICKET252");
  }
  if (!(ticket252Load >= 0 && ticket252Load < ticket251Load)) {
    errors.push("TICKET252 must load before TICKET251");
  }
  if (!(ticket251Load >= 0 && ticket251Load < ticket250Load)) {
    errors.push("TICKET251 must load before TICKET250");
  }
  for (const page of ["riemann", "collatz", "goldbach", "twin-prime"]) {
    const source = fs.readFileSync(path.join(root, "open-problems", `${page}.html`), "utf8");
    if (!source.includes("open-problems.js?v=20260901-ticket264") || !source.includes("ticket264-open-problem.js?v=20260901-ticket264") || !source.includes("ticket263-open-problem.js?v=20260901-ticket263") || !source.includes("ticket262-open-problem.js?v=20260831-ticket262") || !source.includes("ticket261-open-problem.js?v=20260831-ticket261") || !source.includes("ticket260-open-problem.js?v=20260831-ticket260") || !source.includes("ticket259-open-problem.js?v=20260831-ticket259") || !source.includes("ticket258-open-problem.js?v=20260831-ticket258") || !source.includes("ticket257-open-problem.js?v=20260831-ticket257") || !source.includes("ticket256-open-problem.js?v=20260829-ticket256") || !source.includes("ticket255-open-problem.js?v=20260829-ticket255") || !source.includes("ticket254-open-problem.js?v=20260829-ticket254") || !source.includes("ticket253-open-problem.js?v=20260829-ticket253") || !source.includes("ticket252-open-problem.js?v=20260829-ticket252") || !source.includes("ticket251-open-problem.js?v=20260827-ticket251") || !source.includes("ticket250-open-problem.js?v=20260827-ticket250") || !source.includes("ticket249-open-problem.js?v=20260826-ticket249") || !source.includes("ticket248-open-problem.js?v=20260826-ticket248") || !source.includes("ticket247-open-problem.js?v=20260826-ticket247") || !source.includes("ticket246-open-problem.js?v=20260826-ticket246") || !source.includes("ticket245-open-problem.js?v=20260826-ticket245") || !source.includes("ticket244-open-problem.js?v=20260826-ticket244") || !source.includes("ticket243-open-problem.js?v=20260826-ticket243") || !source.includes("ticket242-open-problem.js?v=20260825-ticket242")) {
      errors.push(`${page}: missing evidence-first proof-page cache key`);
    }
    if (!source.includes("styles.css?v=20260901-ticket264-layout")) {
      errors.push(`${page}: missing evidence-first style cache key`);
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
    await page.screenshot({
      path: path.join(root, "data", "conjecture_lab_desktop.png"),
      fullPage: false,
    });
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
    metrics = await page.evaluate(() => ({
      pageProtocol: window.location.protocol,
      dataSourceBadge: document.querySelector("#dataSourceBadge").textContent,
      title: document.title,
      languageSwitchButtons: document.querySelectorAll("[data-lang-set]").length,
      languageNote: document.querySelector(".language-note")?.textContent || "",
      sideNavText: document.querySelector(".side-nav").textContent,
      navGroupCount: document.querySelectorAll(".nav-group-label").length,
      currentBriefText: document.querySelector("#research-brief-panel")?.textContent || "",
      currentBriefCards: document.querySelectorAll("#research-brief-panel .brief-problem-card").length,
      railResearchText: document.querySelector(".rail-research-status")?.textContent || "",
      railResearchTicket: document.querySelector(".rail-research-status strong")?.textContent || "",
      desktopViewportWidth: window.innerWidth,
      desktopHorizontalOverflow:
        document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      desktopWorkspaceFits: (() => {
        const workspace = document.querySelector(".workspace")?.getBoundingClientRect();
        const insight = document.querySelector(".insight-panel")?.getBoundingClientRect();
        return Boolean(
          workspace &&
            insight &&
            workspace.left >= -1 &&
            workspace.right <= window.innerWidth + 1 &&
            insight.left >= -1 &&
            insight.right <= window.innerWidth + 1,
        );
      })(),
      desktopColumnsDoNotOverlap: (() => {
        const visual = document.querySelector(".visual-area")?.getBoundingClientRect();
        const insight = document.querySelector(".insight-panel")?.getBoundingClientRect();
        return Boolean(visual && insight && visual.right <= insight.left - 10);
      })(),
      currentBriefOverflow: (() => {
        const panel = document.querySelector("#research-brief-panel");
        return !panel || panel.scrollWidth > panel.clientWidth + 1;
      })(),
      currentBriefGeometry: (() => {
        const measure = (selector) => {
          const node = document.querySelector(selector);
          const rect = node?.getBoundingClientRect();
          const style = node ? getComputedStyle(node) : null;
          return node && rect ? {
            clientWidth: node.clientWidth,
            scrollWidth: node.scrollWidth,
            left: Math.round(rect.left),
            right: Math.round(rect.right),
            width: Math.round(rect.width),
            whiteSpace: style.whiteSpace,
            overflowWrap: style.overflowWrap,
          } : null;
        };
        return {
          panel: measure("#research-brief-panel"),
          heading: measure(".brief-heading"),
          title: measure(".brief-heading h1"),
          verdict: measure(".brief-verdict"),
          card: measure(".brief-problem-card:nth-child(2)"),
        };
      })(),
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
    metrics.mobileNavigationCollapsed = await mobile.evaluate(() => {
      const disclosure = document.querySelector(".navigation-disclosure");
      const brief = document.querySelector("#research-brief-panel");
      return Boolean(disclosure && !disclosure.open && brief && brief.getBoundingClientRect().top < window.innerHeight);
    });
    metrics.mobileHorizontalOverflow = await mobile.evaluate(() =>
      document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    );
    await mobile.screenshot({
      path: path.join(root, "data", "conjecture_lab_mobile.png"),
      fullPage: false,
    });

    metrics.openProblemPages = [];
    const proofHub = await browser.newPage({
      viewport: { width: 1280, height: 900 },
      deviceScaleFactor: 1,
    });
    await proofHub.goto(new URL("open-problems/index.html", url).toString(), { waitUntil: "networkidle" });
    await proofHub.screenshot({
      path: path.join(root, "data", "conjecture_lab_proof_workbench_desktop.png"),
      fullPage: false,
    });
    metrics.proofHub = await proofHub.evaluate(() => ({
      title: document.title,
      heading: document.querySelector("h1").textContent,
      linkCount: document.querySelectorAll(".proof-card-link").length,
      links: [...document.querySelectorAll(".proof-card-link")].map((link) => link.getAttribute("href")),
      boundary: document.body.textContent,
      currentCards: document.querySelectorAll(".workbench-problem-card").length,
      progressionEras: document.querySelectorAll(".workbench-progression li").length,
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
      problemPage.on("pageerror", (error) => errors.push(`${problemId}: ${error.message}`));
      problemPage.on("console", (message) => {
        if (message.type() === "error") errors.push(`${problemId}: ${message.text()}`);
      });
      await problemPage.goto(new URL(href, url).toString(), { waitUntil: "networkidle" });
      try {
        await problemPage.waitForFunction(() => document.querySelectorAll(".proof-metric").length >= 3);
        await problemPage.waitForFunction(
          () => document.querySelector("#currentResearch")?.textContent.includes("TICKET-264")
            && document.querySelector("#proofOrCounterexampleLab")?.textContent.includes("Ticket 71"),
          null,
          { timeout: 120000 },
        );
      } catch (error) {
        errors.push(`${problemId}: ${error.message}`);
      }
      if (problemId === "riemann") {
        await problemPage.screenshot({
          path: path.join(root, "data", "conjecture_lab_riemann_workbench_desktop.png"),
          fullPage: false,
        });
      }
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
          proofOrCounterexampleText: `${document.querySelector("#currentResearch")?.textContent || ""}\n${document.querySelector("#proofOrCounterexampleLab")?.textContent || ""}`,
          currentResearchText: document.querySelector("#currentResearch")?.textContent || "",
          currentBoundaryLabel: document.querySelector(".proof-current-heading span")?.textContent || "",
          proofSectionGroups: document.querySelectorAll(".proof-section-group").length,
          openProofSectionGroups: document.querySelectorAll(".proof-section-group[open]").length,
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
          ticket264AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket264-asymmetric-threshold-fixed2adic-head .ticket264-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket262AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket262-limsup-finiteharmonic-mod8-thirdorder .ticket262-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket261AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket261-sharpness-weyl-ties-dualcongruence .ticket261-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),          ticket252AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket252-sparse-marginal-zeroresidue-local .ticket252-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket245AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket245-closure-second-order-klein-linnik .ticket245-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket244AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry .ticket244-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket242AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket242-quantifier-order-parseval-diagonal-crt .ticket242-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),          ticket234AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket234-operator-kernel-density-minor-cesaro .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket231AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket231-summable-frame-critical-strip-gauss-crt .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket227AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket227-mellin-block-buchstab-lifts .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket223AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket223-exponential-tail-local-duality-no-go .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket221AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket221-sharp-obstruction-certificates .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket205AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket205-winding-extremal-finite-omega .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket201AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket201-finite-information-allrun-liouville-parity .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket199AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket199-symmetric-sampling-two-run-squarefree-filter .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket194AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket194-densecore-tenone-theta-layers .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket193AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket193-everywhere-nineone-parity-envelope .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket192AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket192-uniform-eightone-weighted-envelope .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket191AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket191-probe-sevenone-budget-granularity .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket190AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket190-cauchy-sixone-quantifier-transfer .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket189AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket189-corefive-sublinear-shift .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket188AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket188-nested-fourone-primepower-dyadic .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket187AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket187-positive-ray-threeone-signature-interval .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket186AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket186-codimension-twoone-layercake-quantization .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket185AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket185-spectral-cycle-factor-granularity .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket184AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket184-information-sufficiency-route-correction .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket183AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket183-abel-primitive-spectral-haar .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket182AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket182-sobolev-divisibility-translation-sibling .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket181AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket181-regularized-localization-quantized-slack .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket179AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket179-symbol-adaptive-discrete-centering .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket177AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket177-comparison-wheel-sobolev-crossgram .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket176AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket176-relative-cone-harmonic-alias-schur .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket175AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket175-relative-equivalence-signed-block .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket174AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket174-tail-lift-adaptive-scalepair .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket173AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket173-finite-section-cylinder-phase-tensor .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket172AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket172-structure-equivalence-l1-variation .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket171AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket171-relative-ghost-phase-haar .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket170AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket170-interval-tail-besov-multiscale .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket169AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket169-kkt-childlift-autocorrelation-primepower .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket168AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket168-fixedcore-leastrealizer-phase-paritymain .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket167AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket167-cofinal-residue-besov-parity .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket166AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket166-tail-adaptive-bandlimited-diagonal .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket165AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket165-vanishing-defect-logtail-variation-signed-dual .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket164AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket164-core-eigen-first-crossing-pointwise-product .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
          ticket163AuditOverflow: (() => {
            const wrapper = document.querySelector(
              "#ticket163-local-certificate-realizer-trace-carleson .ticket161-audit-table .proof-table-wrap",
            );
            return !wrapper || wrapper.scrollWidth > wrapper.clientWidth;
          })(),
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
    metrics.navGroupCount !== 4 ||
    metrics.currentBriefCards !== 4 ||
    metrics.desktopHorizontalOverflow ||
    !metrics.desktopWorkspaceFits ||
    !metrics.desktopColumnsDoNotOverlap ||
    metrics.currentBriefOverflow ||
    !metrics.currentBriefText.includes("TICKET-264") ||
    !metrics.currentBriefText.includes("ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit") ||
    !metrics.currentBriefText.includes("CanonicalFermatQuotientThresholdCutoffDiverges") ||
    !metrics.currentBriefText.includes("Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo") ||
    !metrics.currentBriefText.includes("NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences") ||
    !metrics.currentBriefText.includes("0 / 4 resolved") ||
    !metrics.currentBriefText.includes("OpenSSL") ||
    metrics.railResearchTicket.trim() !== "TICKET-264" ||
    !metrics.railResearchText.includes("TICKET-264") ||
    !metrics.railResearchText.includes("resolution count of zero") ||
    metrics.mobileHorizontalOverflow ||
    !metrics.mobileNavigationCollapsed
  ) {
    console.error(JSON.stringify({ errors: ["evidence-first landing page contract failed"], metrics }, null, 2));
    process.exit(1);
  }
  const proofHubChecks = [
    ["heading", metrics.proofHub?.heading === "Proof Workbench"],
    ["four problem links", metrics.proofHub?.linkCount === 4],
    ["four current cards", metrics.proofHub?.currentCards === 4],
    ["four progression eras", metrics.proofHub?.progressionEras === 4],
    ["Riemann link", metrics.proofHub?.links.includes("riemann.html")],
    ["Collatz link", metrics.proofHub?.links.includes("collatz.html")],
    ["Goldbach link", metrics.proofHub?.links.includes("goldbach.html")],
    ["Twin link", metrics.proofHub?.links.includes("twin-prime.html")],
    ["TICKET-264 boundary", metrics.proofHub?.boundary.includes("What TICKET-264 actually changed")],
    ["TICKET-260 preserved", metrics.proofHub?.boundary.includes("TICKET-260 machine JSON")],
    ["Riemann next lemma", metrics.proofHub?.boundary.includes("ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit")],
    ["Collatz next lemma", metrics.proofHub?.boundary.includes("CanonicalFermatQuotientThresholdCutoffDiverges")],
    ["Goldbach next lemma", metrics.proofHub?.boundary.includes("Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo")],
    ["Twin next lemma", metrics.proofHub?.boundary.includes("NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences")],
    ["progression range", metrics.proofHub?.boundary.includes("TICKET-161–264")],
    ["resolution count label", metrics.proofHub?.boundary.includes("Resolution count")],
    ["zero resolution count", metrics.proofHub?.boundary.includes("0")],
    ["claim boundary", metrics.proofHub?.boundary.includes("not present a conjecture as solved")],
  ];
  const failedProofHubChecks = proofHubChecks.filter(([, passed]) => !passed).map(([label]) => label);
  if (failedProofHubChecks.length > 0) {
    console.error(JSON.stringify({ errors: failedProofHubChecks, metrics }, null, 2));
    process.exit(1);
  }
  const invalidProofOrganization = metrics.openProblemPages.flatMap((page) => {
    const failures = [];
    if (page.proofSectionGroups !== 5) failures.push(`${page.problemId}: expected five semantic proof groups`);
    if (page.openProofSectionGroups !== 1) failures.push(`${page.problemId}: expected only core proof status open`);
    if (!page.currentBoundaryLabel.includes("TICKET-264 · CURRENT RESEARCH BOUNDARY")) failures.push(`${page.problemId}: static TICKET-264 boundary label missing`);
    if (!page.currentResearchText.includes("TICKET-264 asymmetric envelope, explicit threshold cutoff, fixed two-adic no-go, and finite-head closure")) failures.push(`${page.problemId}: current TICKET-264 boundary missing`);
    if (!page.currentResearchText.includes("Remaining proof gap / 남은 증명 간극")) failures.push(`${page.problemId}: current remaining gap missing`);
    return failures;
  });
  if (invalidProofOrganization.length) {
    console.error(JSON.stringify({ errors: invalidProofOrganization, metrics }, null, 2));
    process.exit(1);
  }
  const missingTicket71Checks = metrics.openProblemPages.flatMap((page) => {
    const checks = [];
    const requireText = (label, text) => {
      if (!page.proofOrCounterexampleText.includes(text)) checks.push(`${page.problemId}: ${label}`);
    };
    const requireCurrentText = (label, text) => {
      if (!page.currentResearchText.includes(text)) checks.push(`${page.problemId}: ${label}`);
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
    requireCurrentText("ticket264 title", "TICKET-264 asymmetric envelope, explicit threshold cutoff, fixed two-adic no-go, and finite-head closure");
    requireCurrentText("ticket264 table", "TICKET264 audit");
    requireCurrentText("ticket264 latest", "LATEST / 최신 연구 경계");
    requireCurrentText("ticket264 resolutions", "Resolution count0");
    requireCurrentText("ticket264 proof DAG", "Proof DAG / 증명 의존성");
    requireCurrentText("ticket264 completion guard", "TICKET-264 resolves none of the four parent conjectures");
    if (page.ticket264AuditOverflow) checks.push(`${page.problemId}: ticket264 audit table overflow`);
    if (page.problemId === "riemann") {
      requireCurrentText("ticket264 RH theorem", "AsymmetricReciprocalEnvelopeForScaledJumpMargin");
      requireCurrentText("ticket264 RH target", "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit");
      requireCurrentText("ticket264 RH exact", "Asymmetric boundproved");
      requireCurrentText("ticket264 RH sharp", "Joint sharpnessproved");
      requireCurrentText("ticket264 RH open", "Actual Weil sumopen");
    } else if (page.problemId === "collatz") {
      requireCurrentText("ticket264 Collatz theorem", "PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges");
      requireCurrentText("ticket264 Collatz target", "CanonicalFermatQuotientThresholdCutoffDiverges");
      requireCurrentText("ticket264 Collatz rows", "Exact checks252");
      requireCurrentText("ticket264 Collatz exact", "Explicit equivalenceproved");
      requireCurrentText("ticket264 Collatz open", "Canonical divergenceopen");
    } else if (page.problemId === "goldbach") {
      requireCurrentText("ticket264 Goldbach theorem", "EveryFixedTwoAdicTieSignatureHasNonTieCountModels");
      requireCurrentText("ticket264 Goldbach target", "Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo");
      requireCurrentText("ticket264 Goldbach no-go", "All fixed signaturesrefuted");
      requireCurrentText("ticket264 Goldbach models", "242 shifted-count countermodels");
      requireCurrentText("ticket264 Goldbach open", "Actual prime raceopen");
    } else {
      requireCurrentText("ticket264 Twin theorem", "AllSubthresholdUniqueRootConvergentsAreUnitFree");
      requireCurrentText("ticket264 Twin target", "NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences");
      requireCurrentText("ticket264 Twin crossing", "309742427372962732");
      requireCurrentText("ticket264 Twin head", "Complete finite headproved");
      requireCurrentText("ticket264 Twin count", "Head size38");
      requireCurrentText("ticket264 Twin open", "Infinite tailopen");
    }
    requireText("ticket194 historical title", "Ticket 194 dense-core extension, ten-one cycles, and theta layers");
    requireText("ticket194 historical table", "TICKET194 audit");
    requireText("ticket194 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket194AuditOverflow) checks.push(`${page.problemId}: ticket194 audit table overflow`);
    requireText("ticket193 historical title", "Ticket 193 everywhere extension, nine-one cycles, and parity envelopes");
    requireText("ticket193 historical table", "TICKET193 audit");
    requireText("ticket193 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket193AuditOverflow) checks.push(`${page.problemId}: ticket193 audit table overflow`);
    requireText("ticket192 historical title", "Ticket 192 uniform extension, eight-one cycles, and weighted envelopes");
    requireText("ticket192 historical table", "TICKET192 audit");
    requireText("ticket192 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket192AuditOverflow) checks.push(`${page.problemId}: ticket192 audit table overflow`);
    requireText("ticket191 historical title", "Ticket 191 probe topology, seven-one cycles, and exact arithmetic targets");
    requireText("ticket191 historical table", "TICKET191 audit");
    requireText("ticket191 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket191AuditOverflow) checks.push(`${page.problemId}: ticket191 audit table overflow`);
    requireText("ticket190 historical title", "Ticket 190 Cauchy cores, six-one cycles, and quantifier transfer");
    requireText("ticket190 historical table", "TICKET190 audit");
    requireText("ticket190 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket190AuditOverflow) checks.push(`${page.problemId}: ticket190 audit table overflow`);
    requireText("ticket189 historical title", "Ticket 189 summable cores, five-one cycles, and prime-power subtraction");
    requireText("ticket189 historical table", "TICKET189 audit");
    requireText("ticket189 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket189AuditOverflow) checks.push(`${page.problemId}: ticket189 audit table overflow`);
    requireText("ticket188 historical title", "Ticket 188 common forms, four-one cycles, prime-power contamination, and dyadic oracles");
    requireText("ticket188 historical table", "TICKET188 audit");
    requireText("ticket188 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket188AuditOverflow) checks.push(`${page.problemId}: ticket188 audit table overflow`);
    requireText("ticket187 historical title", "Ticket 187 finite Weil provenance, three-one cycles, survivor signatures, and quantized intervals");
    requireText("ticket187 historical table", "TICKET187 audit");
    requireText("ticket187 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket187AuditOverflow) checks.push(`${page.problemId}: ticket187 audit table overflow`);
    requireText("ticket186 historical title", "Ticket 186 codimension, two-one cycles, survivor layers, and quantized margins");
    requireText("ticket186 historical table", "TICKET186 audit");
    requireText("ticket186 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket186AuditOverflow) checks.push(`${page.problemId}: ticket186 audit table overflow`);
    requireText("ticket185 historical title", "Ticket 185 spectral escape, cycle exclusion, factor horizons, and integer granularity");
    requireText("ticket185 historical table", "TICKET185 audit");
    requireText("ticket185 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket185AuditOverflow) checks.push(`${page.problemId}: ticket185 audit table overflow`);
    requireText("ticket184 historical title", "Ticket 184 information sufficiency and proof-route correction");
    requireText("ticket184 historical table", "TICKET184 audit");
    requireText("ticket184 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket184AuditOverflow) checks.push(`${page.problemId}: ticket184 audit table overflow`);
    requireText("ticket183 historical title", "Ticket 183 Abel transfer, primitive Collatz words, Fourier margins, and Haar paths");
    requireText("ticket183 historical table", "TICKET183 audit");
    requireText("ticket183 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket183AuditOverflow) checks.push(`${page.problemId}: ticket183 audit table overflow`);
    requireText("ticket182 historical title", "Ticket 182 Sobolev energy, affine divisibility, translation moduli, and sibling contrasts");
    requireText("ticket182 historical table", "TICKET182 audit");
    requireText("ticket182 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket182AuditOverflow) checks.push(`${page.problemId}: ticket182 audit table overflow`);
    requireText("ticket181 historical title", "Ticket 181 regularized localization, quantized slack, and path variation");
    requireText("ticket181 historical table", "TICKET181 audit");
    requireText("ticket181 historical label", "PREVIOUS / 이전 연구 경계");
    if (page.ticket181AuditOverflow) checks.push(`${page.problemId}: ticket181 audit table overflow`);
    requireText("ticket177 title", "Ticket 177 comparison majorants, six-wheel envelopes, Sobolev certificates, and signed cross-Gram data");
    requireText("ticket177 table", "TICKET177 audit");
    requireText("ticket177 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket177 resolutions", "Resolution count0");
    requireText("ticket177 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket177AuditOverflow) checks.push(`${page.problemId}: ticket177 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket177 RH theorem", "RelativeComparisonMajorantCertificateAndFreeWeightCircularityNoGo");
      requireText("ticket177 RH target", "PoleNeutralWeilWhitenedTailHasPredeclaredComparisonMajorantBelowCoreMargin");
      requireText("ticket177 RH metric", "comparison ρ(M)");
    } else if (page.problemId === "collatz") {
      requireText("ticket177 Collatz theorem", "PostFirstStepSixWheelHarmonicEnvelopeAndStaticWheelNoGo");
      requireText("ticket177 Collatz starts", "Odd starts49,999");
      requireText("ticket177 Collatz exception", "Non-crossing starts63");
      requireText("ticket177 Collatz ratio", "Coefficient ratio0.6667");
      requireText("ticket177 Collatz target", "AperiodicNonDescendingValuationDiscrepancyExceedsSixWheelHarmonicEnvelope");
    } else if (page.problemId === "goldbach") {
      requireText("ticket177 Goldbach theorem", "AliasedMinorSobolevPointwiseCertificateAndRawScaleFailure");
      requireText("ticket177 Goldbach supports", "Raw supports5");
      requireText("ticket177 Goldbach failures", "Certificates passed0");
      requireText("ticket177 Goldbach no-go", "Energy-only no-go4");
      requireText("ticket177 Goldbach target", "ParityAliasedMinorHasMultiscaleEnergyDerivativePowerSavingBelowMajorMain");
    } else {
      requireText("ticket177 Twin theorem", "SignedCrossGramIdentityAndBlockNormInformationLossNoGo");
      requireText("ticket177 Twin families", "Same norm summary3 families");
      requireText("ticket177 Twin norms", "Aggregate norms0 / 1 / 2");
      requireText("ticket177 Twin missing", "Missing cross-Gram4 rows");
      requireText("ticket177 Twin target", "PrimePairHaarSignedCrossGramHasPowerSavingRelativeToDiagonalEnergy");
    }
    requireText("ticket176 title", "Ticket 176 relative cones, harmonic corrections, parity aliases, and weighted Schur circularity");
    requireText("ticket176 table", "TICKET176 audit");
    requireText("ticket176 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket176 resolutions", "Resolution count0");
    requireText("ticket176 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket176AuditOverflow) checks.push(`${page.problemId}: ticket176 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket176 RH theorem", "RelativeLoewnerConeCertificateAndDiagonalTailNoGo");
      requireText("ticket176 RH target", "PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin");
      requireText("ticket176 RH margin", "relative margin");
    } else if (page.problemId === "collatz") {
      requireText("ticket176 Collatz theorem", "AperiodicNonDescentHarmonicCorrectionBoundAndFixedHorizonNoGo");
      requireText("ticket176 Collatz starts", "Odd starts49,999");
      requireText("ticket176 Collatz exception", "Non-crossing starts63");
      requireText("ticket176 Collatz target", "AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope");
    } else if (page.problemId === "goldbach") {
      requireText("ticket176 Goldbach theorem", "EvenTargetParityAliasQuotientAndPreAliasAbsoluteValueNoGo");
      requireText("ticket176 Goldbach targets", "Finite targets987");
      requireText("ticket176 Goldbach gain", "Certificate gain+10");
      requireText("ticket176 Goldbach target", "ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain");
    } else {
      requireText("ticket176 Twin theorem", "WeightedSchurExactOptimizationAndCircularityNoGo");
      requireText("ticket176 Twin target", "PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums");
      requireText("ticket176 Twin equation", "inf");
    }
    requireText("ticket175 title", "Ticket 175 relative spectral resolution, Collatz equivalence, signed Farey minors, and Haar block operators");
    requireText("ticket175 table", "TICKET175 audit");
    requireText("ticket175 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket175 resolutions", "Resolution count0");
    requireText("ticket175 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket175AuditOverflow) checks.push(`${page.problemId}: ticket175 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket175 RH theorem", "AbsoluteTailMarginResolutionBarrierAndRelativeErrorNoGo");
      requireText("ticket175 RH rows", "Resolution rows4");
      requireText("ticket175 RH scale", "Largest target digits333.68");
      requireText("ticket175 RH target", "StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale");
    } else if (page.problemId === "collatz") {
      requireText("ticket175 Collatz theorem", "ZeroLiftNonDescentEquivalenceAndIntermediateTargetNoGo");
      requireText("ticket175 Collatz starts", "Odd starts499,999");
      requireText("ticket175 Collatz failures", "Finite failures0");
      requireText("ticket175 Collatz target", "EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary");
    } else if (page.problemId === "goldbach") {
      requireText("ticket175 Goldbach theorem", "FixedFareyAbsoluteMinorDoubleLossAndSignedCancellationNeed");
      requireText("ticket175 Goldbach targets", "Finite targets987");
      requireText("ticket175 Goldbach failures", "Identity failures0");
      requireText("ticket175 Goldbach target", "FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly");
    } else {
      requireText("ticket175 Twin theorem", "HaarBlockOperatorDominationAndLogLossRecovery");
      requireText("ticket175 Twin projections", "Matched projections6");
      requireText("ticket175 Twin finite", "Finite Type-II rows4");
      requireText("ticket175 Twin target", "PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm");
    }
    requireText("ticket174 title", "Ticket 174 tail schedules, unique zero lifts, adaptive Fourier selection, and sharp scale aggregation");
    requireText("ticket174 table", "TICKET174 audit");
    requireText("ticket174 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket174 resolutions", "Resolution count0");
    requireText("ticket174 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket174AuditOverflow) checks.push(`${page.problemId}: ticket174 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket174 RH theorem", "DiagonalTailScheduleCertificateAndCriticalCutoffNoGo");
      requireText("ticket174 RH rows", "Schedule rows9");
      requireText("ticket174 RH open", "Core signOPEN");
      requireText("ticket174 RH target", "PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero");
    } else if (page.problemId === "collatz") {
      requireText("ticket174 Collatz theorem", "UniqueZeroLiftChildAndLocalDensityNoGo");
      requireText("ticket174 Collatz words", "Words checked5,460");
      requireText("ticket174 Collatz children", "Child valuations1..32");
      requireText("ticket174 Collatz target", "NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren");
    } else if (page.problemId === "goldbach") {
      requireText("ticket174 Goldbach theorem", "AdaptivePositiveSpectrumEquivalenceAndCircularityNoGo");
      requireText("ticket174 Goldbach targets", "Finite targets987");
      requireText("ticket174 Goldbach failures", "Equivalence failures0");
      requireText("ticket174 Goldbach target", "FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly");
    } else {
      requireText("ticket174 Twin theorem", "ScalePairMaximumAggregationAndSharpLogarithmicLoss");
      requireText("ticket174 Twin sizes", "Sharp sizes6");
      requireText("ticket174 Twin norm", "Largest saturated norm7");
      requireText("ticket174 Twin target", "PrimePairEveryScalePairHaarEnergyPowerSavingUniformly");
    }
    requireText("ticket173 title", "Ticket 173 finite-section defects, Collatz cylinder stabilization, target-aligned phase, and tensor-Haar pairs");
    requireText("ticket173 table", "TICKET173 audit");
    requireText("ticket173 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket173 resolutions", "Resolution count0");
    requireText("ticket173 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket173AuditOverflow) checks.push(`${page.problemId}: ticket173 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket173 RH theorem", "CofinalFiniteSectionPositivityAndUniformCoercivityNoGo");
      requireText("ticket173 RH rows", "Lower-defect rows7");
      requireText("ticket173 RH rank", "Rank rows7");
      requireText("ticket173 RH target", "PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero");
    } else if (page.problemId === "collatz") {
      requireText("ticket173 Collatz theorem", "NaturalSupportCylinderStabilizationAndSubexponentialHeightNoGo");
      requireText("ticket173 Collatz words", "Words checked5,460");
      requireText("ticket173 Collatz no-go", "Exponential no-go rows7");
      requireText("ticket173 Collatz target", "EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives");
    } else if (page.problemId === "goldbach") {
      requireText("ticket173 Goldbach theorem", "TargetAlignedNegativeSpectrumCertificateAndPositiveMassNoGo");
      requireText("ticket173 Goldbach targets", "Finite targets987");
      requireText("ticket173 Goldbach passes", "Phase-gate passes1");
      requireText("ticket173 Goldbach target", "UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit");
    } else {
      requireText("ticket173 Twin theorem", "TensorHaarAllScalePairCompletenessAndDiagonalScaleNoGo");
      requireText("ticket173 Twin rows", "Finite Type-II rows4");
      requireText("ticket173 Twin no-go", "Cross-scale no-go sizes5");
      requireText("ticket173 Twin target", "PrimePairMatrixAllScalePairHaarEnergyPowerSaving");
    }
    requireText("ticket172 title", "Ticket 172 structured KKT blocks, Collatz bridge equivalence, Fourier L1, and dyadic mixed variation");
    requireText("ticket172 table", "TICKET172 audit");
    requireText("ticket172 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket172 resolutions", "Resolution count0");
    requireText("ticket172 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket172AuditOverflow) checks.push(`${page.problemId}: ticket172 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket172 RH theorem", "StructuredKKTBlockInertiaCertificateAndWholeRelativeNormNecessityNoGo");
      requireText("ticket172 RH rows", "Structured certificates6");
      requireText("ticket172 RH no-go", "Relative-norm no-go rows6");
      requireText("ticket172 RH target", "CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate");
    } else if (page.problemId === "collatz") {
      requireText("ticket172 Collatz theorem", "NaturalSupportedResidualRayEquivalenceAndFinitePrefixDecisionNoGo");
      requireText("ticket172 Collatz rows", "Prefix bifurcations7");
      requireText("ticket172 Collatz finite", "Finite odd starts49,999");
      requireText("ticket172 Collatz target", "LeastCounterexampleCrossScaleCylinderHeightBound");
    } else if (page.problemId === "goldbach") {
      requireText("ticket172 Goldbach theorem", "FourierL1AnchorCertificateAndShellMagnitudeSharpnessNoGo");
      requireText("ticket172 Goldbach rows", "Exact sharpness rows5");
      requireText("ticket172 Goldbach finite", "Finite prime spectra4");
      requireText("ticket172 Goldbach target", "UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm");
    } else {
      requireText("ticket172 Twin theorem", "DyadicMixedVariationHaarIdentityAndMarginalControlNoGo");
      requireText("ticket172 Twin rows", "Finite Type-II identities4");
      requireText("ticket172 Twin no-go", "Marginal no-go sizes6");
      requireText("ticket172 Twin target", "PrimePairMatrixWeightedDyadicMixedVariationPowerSaving");
    }
    requireText("ticket171 title", "Ticket 171 relative KKT geometry, Collatz ghost rays, signed Goldbach phase, and Haar Type II");
    requireText("ticket171 table", "TICKET171 audit");
    requireText("ticket171 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket171 resolutions", "Resolution count0");
    requireText("ticket171 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket171AuditOverflow) checks.push(`${page.problemId}: ticket171 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket171 RH theorem", "RelativeKKTSignNormalizationCertificateAndGlobalMinimumGapRequirementNoGo");
      requireText("ticket171 RH rows", "Exact anisotropic rows6");
      requireText("ticket171 RH gates", "Relative gates passed6");
      requireText("ticket171 RH target", "CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket171 Collatz theorem", "AllOneNonDescendingGhostRayAndResidualTreeWellFoundednessNoGo");
      requireText("ticket171 Collatz rows", "Ghost-ray rows7");
      requireText("ticket171 Collatz limit", "2-adic limit-1 in Z_2");
      requireText("ticket171 Collatz target", "NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay");
    } else if (page.problemId === "goldbach") {
      requireText("ticket171 Goldbach theorem", "PositiveAutocorrelationPhaseAmbiguityAndShellEnergyOnlyNoGo");
      requireText("ticket171 Goldbach pairs", "Exact positive pairs5");
      requireText("ticket171 Goldbach magnitudes", "Magnitude profiles equal5");
      requireText("ticket171 Goldbach target", "UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin");
    } else {
      requireText("ticket171 Twin theorem", "HaarTypeIIResolutionCompletenessBridgeAndFiniteDepthNoGo");
      requireText("ticket171 Twin rows", "Finite Haar rows4");
      requireText("ticket171 Twin no-go", "Fixed depths refuted5");
      requireText("ticket171 Twin target", "UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants");
    }
    requireText("ticket170 title", "Ticket 170 interval KKT gaps, Collatz tail closure, autocorrelation Besov control, and multiscale Type II");
    requireText("ticket170 table", "TICKET170 audit");
    requireText("ticket170 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket170 resolutions", "Resolution count0");
    requireText("ticket170 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket170AuditOverflow) checks.push(`${page.problemId}: ticket170 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket170 RH theorem", "IntervalKKTGapStabilityAndVanishingEntrywiseRadiusNoGo");
      requireText("ticket170 RH rows", "Exact interval rows6");
      requireText("ticket170 RH no-go", "Entrywise no-goproved");
      requireText("ticket170 RH target", "CofinalDimensionScaledIntervalKKTErrorBelowCertifiedSpectralGapOnFixedWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket170 Collatz theorem", "PrefixwiseFiniteChildTailDescentAndGlobalImmediateDescentThresholdNoGo");
      requireText("ticket170 Collatz rows", "Prefix tail rows8");
      requireText("ticket170 Collatz threshold", "All-one m=64 threshold40");
      requireText("ticket170 Collatz target", "WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure");
    } else if (page.problemId === "goldbach") {
      requireText("ticket170 Goldbach theorem", "AutocorrelationBesovPointwiseBridgeAndFixedLagWindowNoGo");
      requireText("ticket170 Goldbach gates", "Finite shell gates5");
      requireText("ticket170 Goldbach no-go", "Fixed windows refuted6");
      requireText("ticket170 Goldbach target", "UniformBinaryGoldbachAutocorrelationBesovOneBudgetBelowAnchorMargin");
    } else {
      requireText("ticket170 Twin theorem", "TypeIISpectralBilinearBridgeAndFixedPartitionInvisibilityNoGo");
      requireText("ticket170 Twin rows", "Finite Type-II rows4");
      requireText("ticket170 Twin no-go", "Exact invisible refinements4");
      requireText("ticket170 Twin target", "UniformMultiscaleCubicRoughTypeIISpectralDecayWithPrimeProducingConstants");
    }
    requireText("ticket169 title", "Ticket 169 KKT inertia, exact Collatz child lifts, spectral autocorrelation, and Twin prime-power removal");
    requireText("ticket169 table", "TICKET169 audit");
    requireText("ticket169 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket169 resolutions", "Resolution count0");
    requireText("ticket169 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket169AuditOverflow) checks.push(`${page.problemId}: ticket169 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket169 RH theorem", "ConstrainedFormKKTInertiaBridgeAndFixedPenaltyNoGo");
      requireText("ticket169 RH rows", "Exact KKT rows5");
      requireText("ticket169 RH no-go", "Fixed-penalty no-goproved");
      requireText("ticket169 RH target", "CofinalIntervalKKTInertiaCertificatesOnFixedPoleNeutralGuinandWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket169 Collatz theorem", "ExactChildLiftRecurrenceAndFixedResidueMemoryNoGo");
      requireText("ticket169 Collatz child rows", "Exact child rows8");
      requireText("ticket169 Collatz widths", "Residue widths refuted15");
      requireText("ticket169 Collatz target", "UniformPositiveLeastRealizerSlackInvariantUnderExactChildLifts");
    } else if (page.problemId === "goldbach") {
      requireText("ticket169 Goldbach theorem", "SpectralAutocorrelationPointwiseBridgeAndDiagonalEnergyNoGo");
      requireText("ticket169 Goldbach gates", "Finite gates passed5");
      requireText("ticket169 Goldbach exact no-go", "Exact energy no-go rows4");
      requireText("ticket169 Goldbach target", "UniformBinaryGoldbachSpectralAutocorrelationBudgetBelowAnchorMargin");
    } else {
      requireText("ticket169 Twin theorem", "OddVonMangoldtPrimePowerRemovalAndEndgameEquivalence");
      requireText("ticket169 Twin count", "Last finite twin count860");
      requireText("ticket169 Twin contamination", "Last contaminated count41");
      requireText("ticket169 Twin target", "UniformCubicRoughCenteredIncidenceSpectralDecayWithPrimeProducingConstants");
    }
    requireText("ticket168 title", "Ticket 168 fixed neutral cores, least-realizer descent, phase-blind minimax, and Twin parity main terms");
    requireText("ticket168 table", "TICKET168 audit");
    requireText("ticket168 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket168 resolutions", "Resolution count0");
    requireText("ticket168 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket168AuditOverflow) checks.push(`${page.problemId}: ticket168 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket168 RH theorem", "FixedMomentCorrectorCoreBridgeAndCutoffVaryingConstraintNoGo");
      requireText("ticket168 RH core", "Largest exact core64");
      requireText("ticket168 RH target", "CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket168 Collatz theorem", "LeastRealizerDescentMonotonicityAndModularShadowNoGo");
      requireText("ticket168 Collatz length", "Maximum exact length20");
      requireText("ticket168 Collatz words", "Words counted7,553,085");
      requireText("ticket168 Collatz bad count", "Bad realizers0");
      requireText("ticket168 Collatz target", "UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord");
    } else if (page.problemId === "goldbach") {
      requireText("ticket168 Goldbach theorem", "PhaseBlindSpectralL1MinimaxAndMagnitudeOnlyNoGo");
      requireText("ticket168 Goldbach failed gates", "Finite gates passed0");
      requireText("ticket168 Goldbach target", "UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin");
    } else {
      requireText("ticket168 Twin theorem", "FinestParityHalfCorrelationIdentityAndCancellationTargetNoGo");
      requireText("ticket168 Twin last count", "Last finite twin count860");
      requireText("ticket168 Twin last size", "65,536");
      requireText("ticket168 Twin last half", "430/1");
      requireText("ticket168 Twin target", "PositiveLinearOddVonMangoldtFinestParityPairing");
    }
    requireText("ticket167 title", "Ticket 167 cofinal cores, exact Collatz realizer counts, Goldbach Besov tails, and the finest Twin parity scale");
    requireText("ticket167 table", "TICKET167 audit");
    requireText("ticket167 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket167 resolutions", "Resolution count0");
    requireText("ticket167 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket167AuditOverflow) checks.push(`${page.problemId}: ticket167 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket167 RH theorem", "CofinalNestedCoreCertificateBridgeAndNonDenseSubspaceNoGo");
      requireText("ticket167 RH last pivot", "Last proxy pivot1/65536");
      requireText("ticket167 RH target", "CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket167 Collatz theorem", "ExactBadRealizerCountAndWordwiseDensityZeroNoGo");
      requireText("ticket167 Collatz words", "Words counted1,120,444");
      requireText("ticket167 Collatz bad count", "Bad realizers0");
      requireText("ticket167 Collatz target", "UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord");
    } else if (page.problemId === "goldbach") {
      requireText("ticket167 Goldbach theorem", "BesovOneShellAnchorBridgeAndAlignedScaleL2NoGo");
      requireText("ticket167 Goldbach failed gates", "Finite gates passed0");
      requireText("ticket167 Goldbach target", "UniformBinaryGoldbachBesovOneTailBelowAnchorMargin");
    } else {
      requireText("ticket167 Twin theorem", "FinestParityScaleExtractionAndCoarseControlNoGo");
      requireText("ticket167 Twin last size", "256×256");
      requireText("ticket167 Twin last energy", "127/1");
      requireText("ticket167 Twin target", "PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving");
    }
    requireText("ticket166 title", "Ticket 166 positive tails, start-adaptive Collatz windows, bandlimited Goldbach anchors, and shifted-diagonal Haar duality");
    requireText("ticket166 table", "TICKET166 audit");
    requireText("ticket166 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket166 resolutions", "Resolution count0");
    requireText("ticket166 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket166AuditOverflow) checks.push(`${page.problemId}: ticket166 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket166 RH theorem", "PositiveTailDiagonalCoreBridgeAndAmbiguousBandNoGo");
      requireText("ticket166 RH ambiguity", "Ambiguous sign pairs5");
      requireText("ticket166 RH target", "IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket166 Collatz theorem", "StartAdaptiveFinalExcessReductionAndZeroExcessMagnitudeNoGo");
      requireText("ticket166 Collatz adaptive", "adaptive residuals");
      requireText("ticket166 Collatz target", "UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow");
    } else if (page.problemId === "goldbach") {
      requireText("ticket166 Goldbach theorem", "BandlimitedAnchorClosureAndFullBandwidthSpikeNoGo");
      requireText("ticket166 Goldbach targets", "Finite targets16,384");
      requireText("ticket166 Goldbach target", "UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit");
    } else {
      requireText("ticket166 Twin theorem", "ShiftedDiagonalHaarDualityAndCenteredPermutationNoGo");
      requireText("ticket166 Twin last size", "128×128");
      requireText("ticket166 Twin last energy", "512001/4096");
      requireText("ticket166 Twin target", "PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity");
    }
    requireText("ticket165 title", "Ticket 165 vanishing defects, logarithmic Collatz tails, Goldbach variation, and signed Haar duality");
    requireText("ticket165 table", "TICKET165 audit");
    requireText("ticket165 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket165 resolutions", "Resolution count0");
    requireText("ticket165 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket165AuditOverflow) checks.push(`${page.problemId}: ticket165 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket165 RH theorem", "VanishingDefectCoreLimitBridgeAndUniformGapNoGo");
      requireText("ticket165 RH last gap", "1/1376");
      requireText("ticket165 RH target", "ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect");
    } else if (page.problemId === "collatz") {
      requireText("ticket165 Collatz theorem", "UniformLogarithmicFinalExcessReductionAndConstantExcessNoGo");
      requireText("ticket165 Collatz tail", "Length 1,024 residuals7");
      requireText("ticket165 Collatz target", "UniformResidueSlackForLogarithmicFirstCrossingExcessWindow");
    } else if (page.problemId === "goldbach") {
      requireText("ticket165 Goldbach theorem", "SparseAnchorVariationPointwiseBridgeAndFiniteMomentSpikeNoGo");
      requireText("ticket165 Goldbach stride", "Largest passing stride16");
      requireText("ticket165 Goldbach target", "UniformDyadicMinorDeficitAnchorMarginAndVariationDecay");
    } else {
      requireText("ticket165 Twin theorem", "SignedProductHaarDualityAndUnsignedEnergyNoGo");
      requireText("ticket165 Twin size", "128×128");
      requireText("ticket165 Twin positive model", "2/1");
      requireText("ticket165 Twin zero model", "0/1");
      requireText("ticket165 Twin target", "PrimeWeightedSignedProductCarlesonDualMarginBeyondParity");
    }
    requireText("ticket164 title", "Ticket 164 constraint-core eigenvalues, first-crossing residues, pointwise Goldbach gates, and product Haar localization");
    requireText("ticket164 table", "TICKET164 audit");
    requireText("ticket164 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket164 resolutions", "Resolution count0");
    requireText("ticket164 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket164AuditOverflow) checks.push(`${page.problemId}: ticket164 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket164 RH theorem", "ConstraintCoreCompressionAndScalarCancellationNoGo");
      requireText("ticket164 RH determinant", "3D compressed determinant-5");
      requireText("ticket164 RH witness", "Negative core witness-2");
      requireText("ticket164 RH target", "UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket164 Collatz theorem", "FirstContractingLayerFiniteCertificateAndFinalValuationBound");
      requireText("ticket164 Collatz replays", "Exact candidate replays464,921");
      requireText("ticket164 Collatz length", "Maximum full length17");
      requireText("ticket164 Collatz target", "UniformFirstContractingLayerResidueSlack");
    } else if (page.problemId === "goldbach") {
      requireText("ticket164 Goldbach theorem", "PointwiseIntegralExceptionEquivalenceAndL2NonNecessityNoGo");
      requireText("ticket164 Goldbach gates", "Finite pointwise gates9/9 pass");
      requireText("ticket164 Goldbach budget", "No-go L2 budget256/1");
      requireText("ticket164 Goldbach target", "UniformDyadicPointwiseMinorDeficitStrictlyBelowOne");
    } else {
      requireText("ticket164 Twin theorem", "ProductHaarParsevalAndEqualScaleTensorNoGo");
      requireText("ticket164 Twin size", "128×128");
      requireText("ticket164 Twin energy", "128/1");
      requireText("ticket164 Twin target", "UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity");
    }
    requireText("ticket163 title", "Ticket 163 local certificates, natural realizers, trace cancellation, and Carleson localization");
    requireText("ticket163 table", "TICKET163 audit");
    requireText("ticket163 historical", "HISTORICAL / 과거 연구 경계");
    requireText("ticket163 resolutions", "Resolution count0");
    requireText("ticket163 proof DAG", "Proof DAG / 증명 의존성");
    if (page.ticket163AuditOverflow) checks.push(`${page.problemId}: ticket163 audit table overflow`);
    if (page.problemId === "riemann") {
      requireText("ticket163 RH theorem", "FinitePrimeTraceH1ContinuityAndAbsoluteMassNoGo");
      requireText("ticket163 RH endpoint", "1,000,000");
      requireText("ticket163 RH absolute bound", "55,248.845");
      requireText("ticket163 RH target", "CancellationAwareUniformGuinandWeilTraceBoundOnConstraintCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket163 Collatz theorem", "AffineCorrectionMajorizationAndNaturalRealizerCouplingNoGo");
      requireText("ticket163 Collatz start", "Exact no-go start165");
      requireText("ticket163 Collatz endpoint", "Length-17 endpoint167");
      requireText("ticket163 Collatz front margin", "Front margin10,154,448");
      requireText("ticket163 Collatz target", "FirstContractingLayerNaturalRealizerDescent");
    } else if (page.problemId === "goldbach") {
      requireText("ticket163 Goldbach theorem", "DyadicIntegralExceptionCertificateAndDilutedSpikeNoGo");
      requireText("ticket163 Goldbach shell", "(32,768, 65,536]");
      requireText("ticket163 Goldbach budget", "57.452");
      requireText("ticket163 Goldbach target", "UniformDyadicNormalizedNegativeMinorBudgetBelowOne");
    } else {
      requireText("ticket163 Twin theorem", "LocalDyadicVarianceIdentityAndGlobalDilutionNoGo");
      requireText("ticket163 Twin size", "128×128");
      requireText("ticket163 Twin global density", "0.000977");
      requireText("ticket163 Twin local density", "1.000");
      requireText("ticket163 Twin target", "UniformPrimeWeightedLocalCarlesonPowerSavingBeyondParity");
    }
    requireText("ticket162 title", "Ticket 162 H1 form transport, explicit Collatz closure, integral Goldbach budgets, and multiscale Twin Type II");
    requireText("ticket162 table", "TICKET162 audit");
    requireText("ticket162 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket162 resolutions", "Resolution count0");
    requireText("ticket162 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket162 RH theorem", "ResolvedH2ToH1TransportAndUniformH1BallNoGo");
      requireText("ticket162 RH rows", "Transport rows15");
      requireText("ticket162 RH error", "Resolved final H1 error0.002256");
      requireText("ticket162 RH no-go", "H1 unit-ball no-go rows5");
      requireText("ticket162 RH target", "UniformFiniteGuinandWeilH1ContinuityOnResolvedCommonCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket162 Collatz theorem", "ExplicitMinimalFrontLoadedFamilyClosureAndCoverageNoGo");
      requireText("ticket162 Collatz threshold", "Explicit threshold M21,554,214,227");
      requireText("ticket162 Collatz candidates", "Primitive candidates10");
      requireText("ticket162 Collatz closure", "Closed lengthsall m ≥ 2");
      requireText("ticket162 Collatz target", "EveryNaturalOddOrbitHitsAFrontLoadedDominatingDescentPrefix");
    } else if (page.problemId === "goldbach") {
      requireText("ticket162 Goldbach theorem", "IntegralExceptionalSetMomentBridgeAndUnitSpikeSharpness");
      requireText("ticket162 Goldbach rows", "Prime DFT rows5");
      requireText("ticket162 Goldbach budget", "Budget range7.13 → 135.36");
      requireText("ticket162 Goldbach spike", "Sharp unit spikes5");
      requireText("ticket162 Goldbach target", "UniformNormalizedNegativeMinorMomentBelowOneAfterCutoff");
    } else {
      requireText("ticket162 Twin theorem", "DyadicIncidenceEnergyDecompositionAndFixedBinNoGo");
      requireText("ticket162 Twin coarse", "Coarse checkerboard energy0/1");
      requireText("ticket162 Twin fine", "Fine checkerboard energy16/1");
      requireText("ticket162 Twin target", "UniformMultiscaleCenteredIncidenceCarlesonBoundWithPrimeWeights");
    }
    requireText("ticket161 title", "Ticket 161 common-core resolution, Baker reduction, reflection angles, and Type II incidence");
    requireText("ticket161 table", "TICKET161 audit");
    requireText("ticket161 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket161 resolutions", "Resolution count0");
    requireText("ticket161 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket161 RH theorem", "ResolvedCommonCoreL2TransportAndFormNormNoGo");
      requireText("ticket161 RH rows", "Transport rows15");
      requireText("ticket161 RH error", "Resolved final error0.000791");
      requireText("ticket161 RH target", "UniformWeilFormGraphNormTransportOnResolvedCommonCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket161 Collatz theorem", "AsymptoticMinimalFrontLoadedDescentAndConvergentReduction");
      requireText("ticket161 Collatz scan", "Exact scan50,000");
      requireText("ticket161 Collatz failures", "Observed failures0");
      requireText("ticket161 Collatz ratio", "Minimum ratio13/7");
      requireText("ticket161 Collatz target", "ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily");
    } else if (page.problemId === "goldbach") {
      requireText("ticket161 Goldbach theorem", "TargetwiseReflectionAngleCriterionAndAverageAngleNoGo");
      requireText("ticket161 Goldbach rows", "Prime angle rows5");
      requireText("ticket161 Goldbach energy", "Energy certificates0");
      requireText("ticket161 Goldbach phase", "Phase-aware certificates15,495");
      requireText("ticket161 Goldbach target", "UniformPrimeMinorReflectionAngleBelowMajorArcMargin");
    } else {
      requireText("ticket161 Twin theorem", "ZeroMarginalCheckerboardAndTypeIIBilinearNecessity");
      requireText("ticket161 Twin checkerboards", "Checkerboards4");
      requireText("ticket161 Twin scales", "Type II scales4");
      requireText("ticket161 Twin ratio", "10M spectral ratio0.0124");
      requireText("ticket161 Twin target", "UniformCubicRoughCenteredIncidenceSpectralDecay");
    }
    requireText("ticket160 title", "Ticket 160 exact support, natural cylinders, bilinear phase, and wheel limits");
    requireText("ticket160 table", "TICKET160 audit");
    requireText("ticket160 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket160 resolutions", "Resolution count0");
    requireText("ticket160 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket160 RH theorem", "ExactPrimeSupportClosureAndCrossCutoffNestingNoGo");
      requireText("ticket160 RH support", "Prime-support audits4");
      requireText("ticket160 RH remainder", "Omitted remainder0");
      requireText("ticket160 RH target", "EffectiveCommonNestedWeilCoreTransport");
    } else if (page.problemId === "collatz") {
      requireText("ticket160 Collatz theorem", "UniqueCylinderAndFrontLoadedNaturalTransferNoGo");
      requireText("ticket160 Collatz rows", "Cylinder rows4");
      requireText("ticket160 Collatz depth", "Front-loaded max m1,024");
      requireText("ticket160 Collatz target", "MinimalContractingFrontLoadedNaturalTransfer");
    } else if (page.problemId === "goldbach") {
      requireText("ticket160 Goldbach theorem", "MinorReflectionBilinearProxyIdentityAndSharpAmbientNoGo");
      requireText("ticket160 Goldbach identities", "Proxy identities4");
      requireText("ticket160 Goldbach sharpness", "Sharp counterexamples4");
      requireText("ticket160 Goldbach target", "PrimeRestrictedMinorProxyDefectBelowExplicitSingularSeriesMargin");
    } else {
      requireText("ticket160 Twin theorem", "FixedWheelCRTBlindnessAndExactFactorHorizonThreshold");
      requireText("ticket160 Twin CRT", "CRT wheel rows10");
      requireText("ticket160 Twin horizon", "Factor horizon at 10M3,037");
      requireText("ticket160 Twin target", "IndependentCubicRoughBilinearIncidenceDeficit");
    }
    requireText("ticket159 title", "Ticket 159 diagonal cutoff selection, affine thresholds, Fourier phase, and rough-fiber parity");
    requireText("ticket159 table", "TICKET159 audit");
    requireText("ticket159 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket159 resolutions", "Resolution count0");
    requireText("ticket159 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket159 RH theorem", "EffectiveDiagonalCutoffSelectorAndPreassignedScheduleNoGo");
      requireText("ticket159 RH selectors", "Diagonal selectors5");
      requireText("ticket159 RH no-gos", "Preassigned-rate no-gos4");
      requireText("ticket159 RH target", "CertifiedPrimeBandMajorantAndPositiveGalerkinMarginOnEveryNestedWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket159 Collatz theorem", "ContractingCylinderTailAndAverageExcessThresholdNoGo");
      requireText("ticket159 Collatz records", "Threshold records11");
      requireText("ticket159 Collatz length", "Max audited m768");
      requireText("ticket159 Collatz target", "EveryNaturalOddOrbitHasARealizedPrefixAboveItsExactAffineThreshold");
    } else if (page.problemId === "goldbach") {
      requireText("ticket159 Goldbach theorem", "MinorArcEnergyCoefficientBoundAndPhaseBlindnessNoGo");
      requireText("ticket159 Goldbach passes", "Energy-only passes0/8");
      requireText("ticket159 Goldbach pairs", "Opposite-sign counterpairs4");
      requireText("ticket159 Goldbach target", "PhaseSensitiveBilinearMinorArcCoefficientBelowExplicitSingularSeriesMargin");
    } else {
      requireText("ticket159 Twin theorem", "RoughStratumSigmaAlgebraBlindnessAndParitySensitiveFeatureNecessity");
      requireText("ticket159 Twin fibers", "Rough fibers10");
      requireText("ticket159 Twin labels", "Both labels in every fiberyes");
      requireText("ticket159 Twin target", "NonlocalTypeIIOrParitySensitiveCorrelationSeparatesPrimePairsFromRoughCompositePairsUniformly");
    }
    requireText("ticket158 title", "Ticket 158 two-cutoff composition, localized inversion gain, phase variation, and directional information");
    requireText("ticket158 table", "TICKET158 audit");
    requireText("ticket158 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket158 resolutions", "Resolution count0");
    requireText("ticket158 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket158 RH theorem", "TwoCutoffFormBudgetCompositionAndSingleCutoffNoGo");
      requireText("ticket158 RH compositions", "Positive compositions4");
      requireText("ticket158 RH no-gos", "Single-cutoff no-gos4");
      requireText("ticket158 RH target", "UniformPrimeBandRemainderOnExplicitNestedWeilCoreWithJointCutoffSchedule");
    } else if (page.problemId === "collatz") {
      requireText("ticket158 Collatz theorem", "LocalizedInversionGainAndCoarseStatisticNoGo");
      requireText("ticket158 Collatz signatures", "Coarse signatures3,862");
      requireText("ticket158 Collatz ambiguous", "Ambiguous signatures677");
      requireText("ticket158 Collatz target", "NaturalValuationPrefixLocalizedGainCrossesAffineThresholdOnEveryRay");
    } else if (page.problemId === "goldbach") {
      requireText("ticket158 Goldbach theorem", "MovingAverageVariationProxyAndSharpnessNoGo");
      requireText("ticket158 Goldbach proxies", "Variation-proxy passes0/18");
      requireText("ticket158 Goldbach sharpness", "Sharpness rows3");
      requireText("ticket158 Goldbach target", "ArithmeticMinorArcPhaseVariationBelowMajorMarginWithEffectiveFiniteJoin");
    } else {
      requireText("ticket158 Twin theorem", "SignedInformationBudgetAndDirectionBlindnessNoGo");
      requireText("ticket158 Twin certificates", "Directional certificates5/5");
      requireText("ticket158 Twin savings", "Strict savings4");
      requireText("ticket158 Twin target", "UniformPositiveCubicRoughInformationBudgetOrSemiprimeAnticorrelationAfterEffectiveCutoff");
    }
    requireText("ticket157 title", "Ticket 157 form-core promotion, valuation inversion gain, phase-proxy stability, and information margins");
    requireText("ticket157 table", "TICKET157 audit");
    requireText("ticket157 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket157 resolutions", "Resolution count0");
    requireText("ticket157 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket157 RH theorem", "NestedFormCorePromotionAndFiniteCoreSweepNoGo");
      requireText("ticket157 RH cores", "Nested core rows5");
      requireText("ticket157 RH no-gos", "Hidden-direction no-gos4");
      requireText("ticket157 RH target", "UniformArchimedeanTailFormBoundOnNestedExplicitWeilCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket157 Collatz theorem", "ValuationRearrangementInversionGainDescentCertificate");
      requireText("ticket157 Collatz worst", "Worst-order passes49,733");
      requireText("ticket157 Collatz natural", "Natural-order required266");
      requireText("ticket157 Collatz target", "NaturalValuationInversionGainDominatesWorstOrderThresholdExcess");
    } else if (page.problemId === "goldbach") {
      requireText("ticket157 Goldbach theorem", "NegativePhaseL1StabilityAndL2DimensionLossNoGo");
      requireText("ticket157 Goldbach proxies", "Block-proxy passes0/18");
      requireText("ticket157 Goldbach L2", "L2 sharpness rows4");
      requireText("ticket157 Goldbach target", "ArithmeticBinaryGoldbachPhaseProxyWithUniformL1ResidualAndFiniteJoin");
    } else {
      requireText("ticket157 Twin theorem", "InformationBudgetMarginCertificateAndLittleONecessityNoGo");
      requireText("ticket157 Twin certificates", "Finite certificates5/5");
      requireText("ticket157 Twin no-gos", "Little-o no-gos6");
      requireText("ticket157 Twin target", "UniformCubicRoughInformationBudgetBelowSemiprimeMarginAfterEffectiveCutoff");
    }
    requireText("ticket156 title", "Ticket 156 cutoff error, weighted potential, signed minor mass, and normalized information");
    requireText("ticket156 table", "TICKET156 audit");
    requireText("ticket156 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket156 resolutions", "Resolution count0");
    requireText("ticket156 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket156 RH theorem", "ThreeAxisSpectralCertificateAndCutoffStabilityNoGo");
      requireText("ticket156 RH budgets", "Error budgets2");
      requireText("ticket156 RH reversals", "Cutoff sign reversals6");
      requireText("ticket156 RH target", "ExplicitWeilGalerkinCoreAndUniformTwoAxisOperatorErrorBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket156 Collatz theorem", "WeightedSuffixPotentialIdentityAndFloorTwoStrictnessNoGo");
      requireText("ticket156 Collatz starts", "Audited odd starts49,999");
      requireText("ticket156 Collatz failures", "Floor-two failures12,991");
      requireText("ticket156 Collatz target", "EveryNaturalValuationRayCrossesItsWeightedSuffixPotential");
    } else if (page.problemId === "goldbach") {
      requireText("ticket156 Goldbach theorem", "SignedMinorNegativeMassCertificateAndAbsoluteBudgetNoGo");
      requireText("ticket156 Goldbach one-sided", "One-sided passes3/6");
      requireText("ticket156 Goldbach phase-blind", "Phase-blind passes0/6");
      requireText("ticket156 Goldbach target", "UniformBinaryGoldbachMinorNegativePhaseMassBoundWithFiniteJoin");
    } else {
      requireText("ticket156 Twin theorem", "RareEventNormalizedInformationTransferAndVanishingInformationNoGo");
      requireText("ticket156 Twin scales", "Arithmetic scales5");
      requireText("ticket156 Twin no-gos", "Rare-event no-gos6");
      requireText("ticket156 Twin limit", "Limit I/ρ0.081093022");
      requireText("ticket156 Twin target", "ShiftTwoCubicRoughMutualInformationLittleOSelectionMass");
    }
    requireText("ticket155 title", "Ticket 155 range exactness, initial-prefix descent, sublinear wheels, and conditional transfer");
    requireText("ticket155 table", "TICKET155 audit");
    requireText("ticket155 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket155 resolutions", "Resolution count0");
    requireText("ticket155 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket155 RH theorem", "FiniteCoreRangeExactnessAndCoordinateTailProfileNoGo");
      requireText("ticket155 RH rows", "Profile rows6");
      requireText("ticket155 RH rank", "Coupling rank1");
      requireText("ticket155 RH target", "ActualWeilFiniteCoreRangeConstructionAndPositiveSchurMatrix");
    } else if (page.problemId === "collatz") {
      requireText("ticket155 Collatz theorem", "InitialPrefixRecordCriterionAndLaterLocalDescentNoGo");
      requireText("ticket155 Collatz samples", "Infinite-family samples6");
      requireText("ticket155 Collatz delay", "Largest all-one delay20");
      requireText("ticket155 Collatz target", "EveryNaturalStartCrossesAnInitialAffineDescentThreshold");
    } else if (page.problemId === "goldbach") {
      requireText("ticket155 Goldbach theorem", "SublinearPowerWheelEnergyVanishingAndResolutionSqueeze");
      requireText("ticket155 Goldbach schedules", "Sublinear schedules3");
      requireText("ticket155 Goldbach wheel", "Largest W2,310");
      requireText("ticket155 Goldbach target", "EffectiveGoldbachMajorMinorArcReflectionLowerBoundWithFiniteJoin");
    } else {
      requireText("ticket155 Twin theorem", "ConditionalSemiprimeTransferIdentityAndRareEventCovarianceNoGo");
      requireText("ticket155 Twin scales", "Arithmetic scales5");
      requireText("ticket155 Twin no-gos", "Rare-event no-gos5");
      requireText("ticket155 Twin shift", "Fixed normalized shift1/5");
      requireText("ticket155 Twin target", "ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving");
    }
    requireText("ticket154 title", "Ticket 154 compact Schur tails, reverse-suffix descent, wheel projection, and least-factor deficit");
    requireText("ticket154 table", "TICKET154 audit");
    requireText("ticket154 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket154 resolutions", "Resolution count0");
    requireText("ticket154 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket154 RH theorem", "CompactCouplingFiniteSectionPromotionAndHiddenTailNoGo");
      requireText("ticket154 RH compact", "Compact-tail rows6");
      requireText("ticket154 RH hidden", "Hidden rank-one no-gos5");
      requireText("ticket154 RH target", "ActualWeilCompactCouplingWithEffectivePreconditionedTailRate");
    } else if (page.problemId === "collatz") {
      requireText("ticket154 Collatz theorem", "ReverseSuffixSurplusAffineDescentAndTotalSurplusNoGo");
      requireText("ticket154 Collatz certificates", "Affine certificates7");
      requireText("ticket154 Collatz ballot", "Ballot mass scales8");
      requireText("ticket154 Collatz thresholds", "5/7 vs 11/7");
      requireText("ticket154 Collatz target", "EveryNaturalValuationRayHitsAReverseSuffixSurplusDescentBlock");
    } else if (page.problemId === "goldbach") {
      requireText("ticket154 Goldbach theorem", "SymmetricWheelProjectionCertificateAndFixedModulusEnergyNoGo");
      requireText("ticket154 Goldbach rows", "Fixed-wheel rows9");
      requireText("ticket154 Goldbach fraction", "Largest-N W=210 fraction0.241528");
      requireText("ticket154 Goldbach target", "EffectiveGrowingWheelProjectionDominanceAtEveryLargeEvenEndpoint");
    } else {
      requireText("ticket154 Twin theorem", "CubicRoughLeastFactorDeficitIdentityAndSmallPrimeFingerprintNoGo");
      requireText("ticket154 Twin scales", "Least-factor scales5");
      requireText("ticket154 Twin collisions", "PP/QQ fingerprint collisions5");
      requireText("ticket154 Twin ratio", "Largest finite M/R0.720860");
      requireText("ticket154 Twin target", "UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne");
    }
    requireText("ticket153 title", "Ticket 153 essential tails, geometric cylinders, reflection energy, and cubic-rough parity");
    requireText("ticket153 table", "TICKET153 audit");
    requireText("ticket153 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket153 resolutions", "Resolution count0");
    requireText("ticket153 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket153 RH theorem", "PositiveEssentialTailSchurComplementAndFiniteRankNormNoGo");
      requireText("ticket153 RH essential", "Essential-norm witnesses5");
      requireText("ticket153 RH Schur", "Exact Schur margins8");
      requireText("ticket153 RH target", "ActualWeilPositiveTailDecompositionWithCertifiedSchurComplement");
    } else if (page.problemId === "collatz") {
      requireText("ticket153 Collatz theorem", "CountableGeometricCylinderPartitionAndNegativeDriftLaw");
      requireText("ticket153 Collatz children", "Geometric child audits21");
      requireText("ticket153 Collatz drift", "Exact drift tails6");
      requireText("ticket153 Collatz target", "UniformAffineOffsetControlOnNaturalValuationRays");
    } else if (page.problemId === "goldbach") {
      requireText("ticket153 Goldbach theorem", "PrimeThetaReflectionEnergyIdentityAndSymmetricBaselineNoGo");
      requireText("ticket153 Goldbach scales", "Reflection scales4");
      requireText("ticket153 Goldbach largest", "Largest N1,000,000");
      requireText("ticket153 Goldbach target", "ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArcReflectionGap");
    } else {
      requireText("ticket153 Twin theorem", "CubicRoughLiouvilleParityIdentity");
      requireText("ticket153 Twin scales", "Cubic-rough scales5");
      requireText("ticket153 Twin excess", "Largest finite excess39,891");
      requireText("ticket153 Twin target", "UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs");
    }
    requireText("ticket152 title", "Ticket 152 compression exhaustion, Collatz cylinders, Goldbach energy, and Twin selection");
    requireText("ticket152 table", "TICKET152 audit");
    requireText("ticket152 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket152 resolutions", "Resolution count0");
    requireText("ticket152 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket152 RH theorem", "NestedCompressionExhaustionAndFiniteCutoffNoGo");
      requireText("ticket152 RH hidden", "Hidden directions7");
      requireText("ticket152 RH tails", "Tail certificates9");
      requireText("ticket152 RH target", "ActualWeilCoreCompressionWithCertifiedOperatorNormTailBelowMargin");
    } else if (page.problemId === "collatz") {
      requireText("ticket152 Collatz theorem", "AffineCylinderTailAndFiniteExtensionCoverNoGo");
      requireText("ticket152 Collatz cylinders", "Exact cylinders10");
      requireText("ticket152 Collatz witnesses", "Unbounded-next witnesses25");
      requireText("ticket152 Collatz target", "TypeTwoCountableExtensionCoverWithUniformAnalyticValuationTail");
    } else if (page.problemId === "goldbach") {
      requireText("ticket152 Goldbach theorem", "VonMangoldtGlobalL2HoleBallDivergenceNoGo");
      requireText("ticket152 Goldbach scales", "Energy scales4");
      requireText("ticket152 Goldbach ratio", "Largest ratio23.61");
      requireText("ticket152 Goldbach target", "EndpointBilinearVonMangoldtErrorBelowSingularSeriesMainTermK56");
    } else {
      requireText("ticket152 Twin theorem", "SharpMarginalDeletionTransferAndVanishingCoverageNoGo");
      requireText("ticket152 Twin scales", "Selection scales4");
      requireText("ticket152 Twin sharp", "Sharp counterselections4");
      requireText("ticket152 Twin target", "DirectShiftedCubicRoughLiouvilleSumNegativeProportion");
    }
    requireText("ticket151 title", "Ticket 151 negative spectrum, affine thresholds, reflection transversals, and log-two selection");
    requireText("ticket151 table", "TICKET151 audit");
    requireText("ticket151 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket151 resolutions", "Resolution count0");
    requireText("ticket151 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket151 RH theorem", "OneSidedNegativeRelativeFormCriterionAndFullNormNoGo");
      requireText("ticket151 RH positive rows", "Harmless positive-spectrum rows48");
      requireText("ticket151 RH failure rows", "Boundary failures16");
      requireText("ticket151 RH target", "ActualWeilNegativeRelativeFormPartBoundAtMostOne");
    } else if (page.problemId === "collatz") {
      requireText("ticket151 Collatz theorem", "ExactAffineStoppingThresholdAndPositiveSurplusNoGo");
      requireText("ticket151 Collatz counterrows", "Positive-surplus non-descents32");
      requireText("ticket151 Collatz forced rows", "Forced D<0 words35");
      requireText("ticket151 Collatz target", "TypeTwoAffineThresholdCylinderCoverBelowShadowEntry");
    } else if (page.problemId === "goldbach") {
      requireText("ticket151 Goldbach theorem", "WeightedReflectionHoleRadiusAndPermutationMomentNoGo");
      requireText("ticket151 Goldbach moments", "same moments 1..6");
      requireText("ticket151 Goldbach finite scale", "20,000");
      requireText("ticket151 Goldbach target", "OrbitResolvedVonMangoldtApproximationInsideWeightedHoleRadiusK56");
    } else {
      requireText("ticket151 Twin theorem", "CubicRoughLogTwoBiasAndShiftedSelectionNoGo");
      requireText("ticket151 Twin populations", "Population scales4");
      requireText("ticket151 Twin shifted", "Actual shifted scales4");
      requireText("ticket151 Twin target", "PositiveGapTwoCubicRoughMassAndShiftedLogTwoMarginalTransfer");
    }
    requireText("ticket150 title", "Ticket 150 relative form, arbitrary delay, sharp endpoint holes, and parity equivalence");
    requireText("ticket150 table", "TICKET150 audit");
    requireText("ticket150 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket150 resolutions", "Resolution count0");
    requireText("ticket150 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket150 RH theorem", "RelativeFormThresholdAndCompactAmbientCoercivityNoGo");
      requireText("ticket150 RH threshold rows", "Relative threshold rows96");
      requireText("ticket150 RH compact witnesses", "Compact floor witnesses16");
      requireText("ticket150 RH target", "ActualWeilPrimeArchimedeanRelativeFormBoundAtMostOne");
    } else if (page.problemId === "collatz") {
      requireText("ticket150 Collatz theorem", "ThreeExitLocalCompensationAndTypeTwoArbitraryDelayNoGo");
      requireText("ticket150 Collatz exits", "Local exits3,000");
      requireText("ticket150 Collatz delays", "CRT delay witnesses42");
      requireText("ticket150 Collatz target", "TypeTwoAdaptiveValuationSurplusDescentBelowShadowEntry");
    } else if (page.problemId === "goldbach") {
      requireText("ticket150 Goldbach theorem", "SharpWheelEndpointHoleRadiusAndGrowingRelativeL2NoGo");
      requireText("ticket150 Goldbach wheels", "Exact wheels4");
      requireText("ticket150 Goldbach primorials", "Primorial rows13");
      requireText("ticket150 Goldbach target", "VonMangoldtEndpointReflectionMassRetentionK56");
    } else {
      requireText("ticket150 Twin theorem", "SemiprimeCoverDeficitExactParityEquivalence");
      requireText("ticket150 Twin scales", "Exact source scales4");
      requireText("ticket150 Twin separation", "Separation tables4");
      requireText("ticket150 Twin target", "PositiveCubicRoughMassAndOneSidedLiouvilleMarginalGap");
    }
    requireText("ticket149 title", "Ticket 149 smooth cores, exact shadow escape, wheel transfer, and semiprime cover");
    requireText("ticket149 table", "TICKET149 audit");
    requireText("ticket149 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket149 resolutions", "Resolution count0");
    requireText("ticket149 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket149 RH theorem", "SmoothSchwartzCoreAndAbsoluteCompactTailNoGo");
      requireText("ticket149 RH rows", "Exact compact operators16");
      requireText("ticket149 RH tail", "Smallest audited tail1/289");
      requireText("ticket149 RH target", "ExplicitWeilWaveletCoerciveReferenceAndRelativeTailNormBelowOne");
    } else if (page.problemId === "collatz") {
      requireText("ticket149 Collatz theorem", "MinusFiveShadowExactEscapeAndDescentNoGo");
      requireText("ticket149 Collatz orders", "Exact shadow orders48");
      requireText("ticket149 Collatz starts", "Bounded odd starts100,000");
      requireText("ticket149 Collatz target", "ThreeExitTypePostShadowAdaptiveDescent");
    } else if (page.problemId === "goldbach") {
      requireText("ticket149 Goldbach theorem", "SquarefreeWheelLocalMainTermAndResidualTransferNoGo");
      requireText("ticket149 Goldbach wheels", "Exact wheels4");
      requireText("ticket149 Goldbach largest", "Largest wheel2,310");
      requireText("ticket149 Goldbach target", "VonMangoldtWheelResidualPointwiseBilinearSavingK56");
    } else {
      requireText("ticket149 Twin theorem", "CubicRoughSemiprimeEndpointCoverReduction");
      requireText("ticket149 Twin scales", "Exact cover scales4");
      requireText("ticket149 Twin route", "Best available routesemiprime endpoint deficit");
      requireText("ticket149 Twin target", "CubicRoughSemiprimeEndpointCoverDeficit");
    }
    requireText("ticket148 title", "Ticket 148 multiscale completeness, renewal shadows, phase sharpness, and matching coupling");
    requireText("ticket148 table", "TICKET148 audit");
    requireText("ticket148 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket148 resolutions", "Resolution count0");
    requireText("ticket148 correction", "Historical corrections1");
    requireText("ticket148 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket148 RH theorem", "DyadicHaarMultiscaleCompletenessAndFiniteScalePositivityNoGo");
      requireText("ticket148 RH rows", "Exact Haar levels8");
      requireText("ticket148 RH dimension", "Largest dimension256");
      requireText("ticket148 RH target", "SmoothWeilWaveletCoreAndUniformMatrixTailPositivityBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket148 Collatz theorem", "MinusFiveCylinderNoFixedRenewalHorizon");
      requireText("ticket148 Collatz horizons", "Exact horizons16");
      requireText("ticket148 Collatz word", "Longest valuation word32");
      requireText("ticket148 Collatz target", "AdaptiveRenewalRankEscapingMinusFiveTwoAdicShadow");
    } else if (page.problemId === "goldbach") {
      requireText("ticket148 Goldbach theorem", "NonnegativeEndpointPhaseQuantizationOrderSharpness");
      requireText("ticket148 Goldbach examples", "Nonnegative examples6");
      requireText("ticket148 Goldbach order", "Sharp orderE / M");
      requireText("ticket148 Goldbach target", "VonMangoldtEndpointSectorCancellationBeyondSharpGeometricRate");
    } else {
      requireText("ticket148 Twin theorem", "CubicRoughGapTwoMatchingAndCouplingNoGo");
      requireText("ticket148 Twin geometry", "Geometrymatching, not long paths");
      requireText("ticket148 Twin counterfamily", "Coupling counterfamilies16");
      requireText("ticket148 Twin target", "CubicRoughLiouvilleMatchingCouplingTypeIIBound");
    }
    requireText("ticket147 title", "Ticket 147 fiber completeness, compensation cover, phase resolution, and path cuts");
    requireText("ticket147 table", "TICKET147 audit");
    requireText("ticket147 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket147 resolutions", "Resolution count0");
    requireText("ticket147 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket147 RH theorem", "FiniteGeneratorLatticeShiftFiberIncompleteness");
      requireText("ticket147 RH rows", "Exact fiber rows8");
      requireText("ticket147 RH ambient", "Ambient fiberinfinite-dimensional");
      requireText("ticket147 RH target", "InfiniteMultiscaleWeilFiberCompletenessAndMatrixSchurBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket147 Collatz theorem", "FirstRunCompensationTwoThirdsPointwiseDescentCover");
      requireText("ticket147 Collatz mass", "Exact Haar cover2/3");
      requireText("ticket147 Collatz starts", "Bounded starts audited100,000");
      requireText("ticket147 Collatz residual", "Residual b=2 rows12");
      requireText("ticket147 Collatz target", "ResidualThirdIteratedRunCompensationRenewalDescent");
    } else if (page.problemId === "goldbach") {
      requireText("ticket147 Goldbach theorem", "EndpointPhaseQuantizationEnergyBoundAndFixedResolutionNoGo");
      requireText("ticket147 Goldbach finite", "Finite Fourier rows12");
      requireText("ticket147 Goldbach scales", "Scale rows10");
      requireText("ticket147 Goldbach target", "ArithmeticPhaseSectorImbalanceBoundSummableK56");
    } else {
      requireText("ticket147 Twin theorem", "GapTwoPathCutMarginalNoGoAndArithmeticLabelReduction");
      requireText("ticket147 Twin counterfamily", "Abstract counterfamily rows16");
      requireText("ticket147 Twin arithmetic", "Arithmetic audit rows4");
      requireText("ticket147 Twin target", "CubicRoughLiouvillePathSwitchDeficitTypeIIBound");
    }
    requireText("ticket146 title", "Ticket 146 Toeplitz reflection, polynomial ranks, Fourier phase, and Frechet bounds");
    requireText("ticket146 table", "TICKET146 audit");
    requireText("ticket146 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket146 resolutions", "Resolution count0");
    requireText("ticket146 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket146 RH theorem", "ShiftGeneratedWeilToeplitzLevinsonReductionAndFiniteLagNoGo");
      requireText("ticket146 RH sample", "Exact sample orders6");
      requireText("ticket146 RH no-go", "Fixed-lag no-go rows12");
      requireText("ticket146 RH pivot", "Unseen pivot-3");
      requireText("ticket146 RH target", "ExplicitWeilShiftCoreReflectionCoefficientUnitDiskBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket146 Collatz theorem", "FiniteModulusPiecewisePolynomialCollatzRankNoGo");
      requireText("ticket146 Collatz rows", "Exact rows30");
      requireText("ticket146 Collatz degrees", "Polynomial degrees0–5");
      requireText("ticket146 Collatz target", "SymbolicCylinderAdaptiveBlockDescentBeyondPolynomialRanks");
    } else if (page.problemId === "goldbach") {
      requireText("ticket146 Goldbach theorem", "PowerSpectrumInsufficiencyForPointwiseBinaryConvolution");
      requireText("ticket146 Goldbach rows", "Exact cyclic rows6");
      requireText("ticket146 Goldbach power", "Same power dataall frequencies");
      requireText("ticket146 Goldbach endpoint", "Endpoint split1 vs 0");
      requireText("ticket146 Goldbach target", "PhaseResolvedBinaryGoldbachScaleEnvelopeSummableK56");
    } else {
      requireText("ticket146 Twin theorem", "FrechetMarginalLiouvilleNoGoAndOneSidedWalshReduction");
      requireText("ticket146 Twin marginals", "Same marginalsA10=A01=0");
      requireText("ticket146 Twin split", "Twin split0 vs 25");
      requireText("ticket146 Twin target", "CubicRoughOneSidedJointLiouvilleTypeIIMargin");
    }
    requireText("ticket145 title", "Ticket 145 normalization, affine ranks, signed endpoints, and separable Walsh no-go theorems");
    requireText("ticket145 table", "TICKET145 audit");
    requireText("ticket145 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket145 resolutions", "Resolution count0");
    requireText("ticket145 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket145 RH theorem", "SchurPivotBasisScalingNoGoAndNormalizedAngleReduction");
      requireText("ticket145 RH rows", "Exact rows20");
      requireText("ticket145 RH eta", "Hilbert η at N=121/497634306624");
      requireText("ticket145 RH target", "ExplicitWeilFormCoreNormalizedSchurSignRecurrence");
    } else if (page.problemId === "collatz") {
      requireText("ticket145 Collatz theorem", "FiniteModulusPiecewiseAffineCollatzRankNoGo");
      requireText("ticket145 Collatz rows", "Exact family rows48");
      requireText("ticket145 Collatz quantifier", "Quantifierevery M,k≥1");
      requireText("ticket145 Collatz target", "NonlinearLiftClosedCollatzRankBeyondFiniteResidueAffine");
    } else if (page.problemId === "goldbach") {
      requireText("ticket145 Goldbach theorem", "SignedMartingaleEndpointEquivalenceAndAggregateCancellationNoGo");
      requireText("ticket145 Goldbach rows", "Exact spike rows9");
      requireText("ticket145 Goldbach endpoint", "Bad endpoint57 > 56");
      requireText("ticket145 Goldbach target", "ArithmeticBinaryGoldbachScaleEnvelopeSummableK56");
    } else {
      requireText("ticket145 Twin theorem", "AdverseWalshSlackIdentityAndMinimalSeparableMajorantNoGo");
      requireText("ticket145 Twin grid", "Majorant grid4,913");
      requireText("ticket145 Twin witness", "B=178 > A00=100, twins=1");
      requireText("ticket145 Twin target", "IndependentCubicRoughJointWalshTypeIIBound");
    }
    requireText("ticket144 title", "Ticket 144 Schur pivots, rank equivalence, martingale variation, and adverse Walsh control");
    requireText("ticket144 table", "TICKET144 audit");
    requireText("ticket144 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket144 resolutions", "Resolution count0");
    requireText("ticket144 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket144 RH theorem", "NestedGramSchurPivotCertificateAndFinitePrefixExtensionNoGo");
      requireText("ticket144 RH rows", "Schur rows15");
      requireText("ticket144 RH pivot", "Hilbert N=10 pivot1/44914183600");
      requireText("ticket144 RH target", "ExplicitWeilFormCoreSchurPivotLowerBound");
    } else if (page.problemId === "collatz") {
      requireText("ticket144 Collatz theorem", "GlobalWellFoundedRankIffCollatzTermination");
      requireText("ticket144 Collatz rows", "Rank rows8");
      requireText("ticket144 Collatz rank", "Bounded max rank129 at 77,031");
      requireText("ticket144 Collatz target", "ExplicitLiftClosedFiniteDescriptionCollatzRank");
    } else if (page.problemId === "goldbach") {
      requireText("ticket144 Goldbach theorem", "BoundedSignalLinearAbsoluteMartingaleVariationNoGo");
      requireText("ticket144 Goldbach rows", "Variation rows9");
      requireText("ticket144 Goldbach crossing", "First depth above 56113");
      requireText("ticket144 Goldbach target", "ArithmeticBinaryGoldbachSignedMartingaleCancellationK56");
    } else {
      requireText("ticket144 Twin theorem", "WalshL1SimplexBalanceIdentityAndAdversePartReduction");
      requireText("ticket144 Twin rows", "Adverse rows4");
      requireText("ticket144 Twin observed", "Observed adverse B0 on all four finite rows");
      requireText("ticket144 Twin target", "UniformCubicRoughAdverseWalshPartContraction");
    }
    requireText("ticket143 title", "Ticket 143 form cores, published period floors, martingales, and Walsh inversion");
    requireText("ticket143 table", "TICKET143 audit");
    requireText("ticket143 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket143 resolutions", "Resolution count0");
    requireText("ticket143 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket143 RH theorem", "ClosedFormCoreFiniteSectionBridgeAndHilbertDenseNoGo");
      requireText("ticket143 RH rows", "Form-core rows8");
      requireText("ticket143 RH target", "ExplicitWeilFormCoreCompressionCertificateFamily");
    } else if (page.problemId === "collatz") {
      requireText("ticket143 Collatz theorem", "PublishedOddPeriodFloorRetiresPeriod15601AndCompositionExplosionNoGo");
      requireText("ticket143 Collatz digits", "Raw word-count digits7,069");
      requireText("ticket143 Collatz target", "PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness");
    } else if (page.problemId === "goldbach") {
      requireText("ticket143 Goldbach theorem", "DyadicMartingaleResidualIdentityAndRootModeScalingNoGo");
      requireText("ticket143 Goldbach rows", "Martingale rows5");
      requireText("ticket143 Goldbach target", "UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56");
    } else {
      requireText("ticket143 Twin theorem", "WalshHadamardRoughPairInversionAndCircularGapNoGo");
      requireText("ticket143 Twin rows", "Walsh rows4");
      requireText("ticket143 Twin target", "UniformCubicRoughWalshL1ContractionBelowOne");
    }
    requireText("ticket142 title", "Ticket 142 effective rank, cycle direction, Haar duals, and Liouville parity");
    requireText("ticket142 table", "TICKET142 audit");
    requireText("ticket142 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket142 resolutions", "Resolution count0");
    requireText("ticket142 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket142 RH theorem", "EffectiveRankShiftedMomentIdentityAndSharpLogCoefficientNoGo");
      requireText("ticket142 RH rows", "Effective-rank rows8");
      requireText("ticket142 RH target", "ExplicitProjectedWeilFiniteSectionAndTailConvergenceContract");
    } else if (page.problemId === "collatz") {
      requireText("ticket142 Collatz theorem", "PrimitiveCycleSuccessorDistinctProductUpperBoundAndTargetCollapseNoGo");
      requireText("ticket142 Collatz rows", "Exact period rows8");
      requireText("ticket142 Collatz target", "Period15601AffineNumeratorNondivisibilityCertificate");
    } else if (page.problemId === "goldbach") {
      requireText("ticket142 Goldbach theorem", "RobustDualBasisChangeInvarianceAndHaarK56Reduction");
      requireText("ticket142 Goldbach rows", "Dual rows5");
      requireText("ticket142 Goldbach target", "UniformEvenGoldbachHaarScaleBudgetBelow56");
    } else {
      requireText("ticket142 Twin theorem", "CubicRoughnessLiouvilleExactTwinProjector");
      requireText("ticket142 Twin rows", "Liouville ledger rows4");
      requireText("ticket142 Twin target", "OneSidedCubicRoughLiouvilleLedgerGap");
    }
    requireText("ticket141 title", "Ticket 141 one-sided spectra, moving floors, robust duals, and large sieve");
    requireText("ticket141 table", "TICKET141 audit");
    requireText("ticket141 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket141 resolutions", "Resolution count0");
    requireText("ticket141 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket141 RH theorem", "ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo");
      requireText("ticket141 RH rows", "Shifted rows6");
      requireText("ticket141 RH target", "ProjectedWeilShiftedLogMomentBelowTailGap");
    } else if (page.problemId === "collatz") {
      requireText("ticket141 Collatz theorem", "PeriodDependentFloorLinearGrowthBarrier");
      requireText("ticket141 Collatz rows", "Moving-floor rows6");
      requireText("ticket141 Collatz target", "CycleMinimumAboveExactPowerOfTwoWindowThreshold");
    } else if (page.problemId === "goldbach") {
      requireText("ticket141 Goldbach theorem", "PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo");
      requireText("ticket141 Goldbach orders", "Conditioning orders8");
      requireText("ticket141 Goldbach target", "LocalizedOrthogonalArithmeticK56DualCertificate");
    } else {
      requireText("ticket141 Twin theorem", "QuadraticIrrationalBilinearLargeSieveCancellation");
      requireText("ticket141 Twin rows", "Bilinear rows5");
      requireText("ticket141 Twin target", "UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass");
    }
    requireText("ticket140 title", "Ticket 140 spectral moments, fixed-floor limits, duality, and rotation");
    requireText("ticket140 table", "TICKET140 audit");
    requireText("ticket140 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket140 resolutions", "Resolution count0");
    requireText("ticket140 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket140 RH theorem", "EvenTraceMomentSpectralCertificateAndLogOrderBarrier");
      requireText("ticket140 RH rows", "Moment rows6");
      requireText("ticket140 RH target", "ProjectedWeilLogOrderEvenTraceMomentBelowTailGap");
    } else if (page.problemId === "collatz") {
      requireText("ticket140 Collatz theorem", "FixedCycleMinimumWindowEventuallyVacuousNoGo");
      requireText("ticket140 Collatz rows", "Floor rows6");
      requireText("ticket140 Collatz target", "PeriodDependentCycleMinimumDiophantineSeparation");
    } else if (page.problemId === "goldbach") {
      requireText("ticket140 Goldbach theorem", "FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo");
      requireText("ticket140 Goldbach orders", "Measurement orders10");
      requireText("ticket140 Goldbach target", "ArithmeticK56DualCertificateOnPowerOfTwoHardStratum");
    } else {
      requireText("ticket140 Twin theorem", "QuadraticIrrationalSobolevRotationCancellation");
      requireText("ticket140 Twin rows", "Sobolev rows5");
      requireText("ticket140 Twin target", "DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass");
    }
    requireText("ticket139 title", "Ticket 139 uniformity, Diophantine windows, and complexity");
    requireText("ticket139 table", "TICKET139 audit");
    requireText("ticket139 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket139 resolutions", "Resolution count0");
    requireText("ticket139 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket139 RH theorem", "TwoMutuallyUnbiasedBasesCrossGramL1NoGo");
      requireText("ticket139 RH rows", "Tight-frame rows4");
      requireText("ticket139 RH target", "ProjectedWeilSignedGramSpectralRadiusBelowTailGap");
    } else if (page.problemId === "collatz") {
      requireText("ticket139 Collatz theorem", "CollatzCycleDiophantineWindowAndVerifiedFloorExclusion");
      requireText("ticket139 Collatz periods", "Periods audited20,000");
      requireText("ticket139 Collatz target", "AllPeriodSupercriticalCycleDiophantineExclusion");
    } else if (page.problemId === "goldbach") {
      requireText("ticket139 Goldbach theorem", "PowerOfTwoBarycentricMomentAnnihilatorNoGo");
      requireText("ticket139 Goldbach moments", "Moment orders10");
      requireText("ticket139 Goldbach target", "LocalizedPowerOfTwoSignedGoldbachResidualK56");
    } else {
      requireText("ticket139 Twin theorem", "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo");
      requireText("ticket139 Twin rows", "Orbit rows9");
      requireText("ticket139 Twin target", "UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass");
    }
    requireText("ticket138 title", "Ticket 138 correlation, periodicity, and scale closure");
    requireText("ticket138 table", "TICKET138 audit");
    requireText("ticket138 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket138 resolutions", "Resolution count0");
    requireText("ticket138 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket138 RH theorem", "CrossGramCorrelationBlockPositivityCriterion");
      requireText("ticket138 RH no-go", "signed-mean no-go");
      requireText("ticket138 RH target", "ProjectedWeilCrossGramCorrelationBudgetBelowTailGap");
    } else if (page.problemId === "collatz") {
      requireText("ticket138 Collatz theorem", "SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding");
      requireText("ticket138 Collatz words", "Words replayed9,840");
      requireText("ticket138 Collatz target", "AffineCappedNaturalCodeWellFoundedness");
    } else if (page.problemId === "goldbach") {
      requireText("ticket138 Goldbach theorem", "AllScaleOddSquarefreeWheelMomentBarrier");
      requireText("ticket138 Goldbach near-full", "M=1 near-full");
      requireText("ticket138 Goldbach target", "PointwiseSignedBinaryGoldbachResidualK56");
    } else {
      requireText("ticket138 Twin theorem", "IrrationalInjectivityWithoutRegularityIsTautologicalNoGo");
      requireText("ticket138 Twin Pell", "Pell rows12");
      requireText("ticket138 Twin target", "RegularAperiodicTypeIICancellationWithPositiveTwinMass");
    }
    requireText("ticket137 title", "Ticket 137 cancellation, entropy, and information budgets");
    requireText("ticket137 table", "TICKET137 audit");
    requireText("ticket137 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket137 resolutions", "Resolution count0");
    requireText("ticket137 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket137 RH theorem", "HadamardCancellationSchurOverestimateNoGo");
      requireText("ticket137 RH no-go", "true margin");
      requireText("ticket137 RH target", "ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin");
    } else if (page.problemId === "collatz") {
      requireText("ticket137 Collatz theorem", "AffineCappedValuationCylinderMassDecay");
      requireText("ticket137 Collatz mass", "all-prefix mass");
      requireText("ticket137 Collatz target", "ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet");
    } else if (page.problemId === "goldbach") {
      requireText("ticket137 Goldbach theorem", "SubpowerGrowingWheelLogMomentBarrier");
      requireText("ticket137 Goldbach barrier", "minimum p for ≤6/5");
      requireText("ticket137 Goldbach target", "NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56");
    } else {
      requireText("ticket137 Twin theorem", "RationalFourierInformationBudgetLowerBound");
      requireText("ticket137 Twin collisions", "Collisions");
      requireText("ticket137 Twin target", "IrrationalOrSupercriticalAperiodicTypeIITwinSeparation");
    }
    requireText("ticket136 title", "Ticket 136 scale-sensitive obstructions and affine descent bridge");
    requireText("ticket136 table", "TICKET136 audit");
    requireText("ticket136 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket136 resolutions", "Resolution count0");
    requireText("ticket136 proof DAG", "Proof DAG / 증명 의존성");
    if (page.problemId === "riemann") {
      requireText("ticket136 RH theorem", "SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo");
      requireText("ticket136 RH no-go", "operator witness");
      requireText("ticket136 RH target", "ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin");
    } else if (page.problemId === "collatz") {
      requireText("ticket136 Collatz theorem", "LeastCounterexampleAffineCorrectionInequality");
      requireText("ticket136 Collatz identity", "Exact identities");
      requireText("ticket136 Collatz target", "UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes");
    } else if (page.problemId === "goldbach") {
      requireText("ticket136 Goldbach theorem", "FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier");
      requireText("ticket136 Goldbach barrier", "minimum p for ≤6/5");
      requireText("ticket136 Goldbach target", "BinaryGoldbachGrowingWheelResidualBoundK56");
    } else {
      requireText("ticket136 Twin theorem", "FiniteRationalFourierAlgebraCompositeLift");
      requireText("ticket136 Twin factors", "forced factors");
      requireText("ticket136 Twin target", "AperiodicScaleGrowingTypeIITwinSeparation");
    }
    requireText("ticket135 title", "Ticket 135 conditional bridges and exceptional-set boundaries");
    requireText("ticket135 table", "TICKET135 audit");
    requireText("ticket135 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket135 resolutions", "Resolution count0");
    if (page.problemId === "riemann") {
      requireText("ticket135 RH theorem", "SharpBlockTailPositivityCertificate");
      requireText("ticket135 RH margin", "Schur margin");
      requireText("ticket135 RH target", "ProjectedWeilBlockConstantsWithPositiveSchurMargin");
    } else if (page.problemId === "collatz") {
      requireText("ticket135 Collatz theorem", "MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover");
      requireText("ticket135 Collatz boundary", "Natural-code promotioninvalid");
      requireText("ticket135 Collatz target", "NaturalCodesCrossAffineDescentThreshold");
    } else if (page.problemId === "goldbach") {
      requireText("ticket135 Goldbach theorem", "SparseHardStratumMomentToMaximumBridge");
      requireText("ticket135 Goldbach factor", "inflation");
      requireText("ticket135 Goldbach target", "BinaryGoldbachHardStratumLogMomentBoundK56");
    } else {
      requireText("ticket135 Twin theorem", "FiniteCongruenceTranscriptCompositeLift");
      requireText("ticket135 Twin witnesses", "Witnesses111");
      requireText("ticket135 Twin target", "NonCongruenceTypeIITwinSeparation");
    }
    requireText("ticket134 title", "Ticket 134 uniformity thresholds and scale no-go theorems");
    requireText("ticket134 table", "TICKET134 audit");
    requireText("ticket134 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket134 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket134 RH theorem", "RationalCongruenceIntervalDichotomy");
      requireText("ticket134 RH certificate", "preconditioned margins");
      requireText("ticket134 RH target", "UniformProjectedWeilGramTailCertificate");
    } else if (page.problemId === "collatz") {
      requireText("ticket134 Collatz theorem", "NoBoundedDepthContractingPrefixCover");
      requireText("ticket134 Collatz no-go", "Finite coverimpossible");
      requireText("ticket134 Collatz target", "WellFoundedUnboundedContractingPrefixCover");
    } else if (page.problemId === "goldbach") {
      requireText("ticket134 Goldbach theorem", "PowerOfTwoMomentDetectionThreshold");
      requireText("ticket134 Goldbach threshold", "moment-scale threshold");
      requireText("ticket134 Goldbach target", "LogScaleMomentOrMaximalGoldbachResidualK56");
    } else {
      requireText("ticket134 Twin theorem", "ScaleDependentPrimorialCompositeLiftBound");
      requireText("ticket134 Twin classes", "Classes lifted23,913");
      requireText("ticket134 Twin target", "NearFullScaleParitySensitiveTwinSeparation");
    }
    requireText("ticket133 title", "Ticket 133 quantifier-promotion exact reductions");
    requireText("ticket133 table", "TICKET133 audit");
    requireText("ticket133 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket133 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket133 RH theorem", "ProjectedWeilCoreGramFamilyEquivalence");
      requireText("ticket133 RH reduction", "projected Gram reduction");
      requireText("ticket133 RH target", "IntervalCertifiedProjectedWeilGramFamily");
    } else if (page.problemId === "collatz") {
      requireText("ticket133 Collatz theorem", "ContractingValuationCylinderLeastCounterexampleExclusion");
      requireText("ticket133 Collatz count", "Contracting3,861");
      requireText("ticket133 Collatz target", "PrefixFreeContractingCylinderCoverOfEveryNaturalCode");
    } else if (page.problemId === "goldbach") {
      requireText("ticket133 Goldbach theorem", "PowerOfTwoSparseSpikesDefeatEveryFiniteCesaroLpBridge");
      requireText("ticket133 Goldbach spike", "power-of-two spike contract");
      requireText("ticket133 Goldbach target", "HardStratumMaximalBinaryGoldbachResidualK56");
    } else {
      requireText("ticket133 Twin theorem", "EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts");
      requireText("ticket133 Twin classes", "Classes lifted1,638");
      requireText("ticket133 Twin target", "UnboundedParitySensitiveTwinPairSeparation");
    }
    requireText("ticket132 title", "Ticket 132 admissibility and pointwise boundary audit");
    requireText("ticket132 table", "TICKET132 audit");
    requireText("ticket132 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket132 scope", "허용공간 · 점별 경계");
    requireText("ticket132 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket132 RH theorem", "ConstraintPreservingEnumerableWeilCoreProjection");
      requireText("ticket132 RH repair", "허용공간 수리");
      requireText("ticket132 RH determinant", "e^(-1/2)-e^(1/2)<0");
      requireText("ticket132 RH target", "NonnegativeProjectedWeilCoreCertificate");
    } else if (page.problemId === "collatz") {
      requireText("ticket132 Collatz theorem", "NaturalCollatzCodesAreCountableDenseAndNull");
      requireText("ticket132 Collatz topology", "countable + dense + null + eventually residue-stable");
      requireText("ticket132 Collatz replay", "natural representatives replayed");
      requireText("ticket132 Collatz target", "PointwiseArchimedeanDescentOnDenseNullNaturalCodes");
    } else if (page.problemId === "goldbach") {
      requireText("ticket132 Goldbach theorem", "PowersOfTwoRemainTheUniformGoldbachHardStratum");
      requireText("ticket132 Goldbach hard", "무한 hard stratum");
      requireText("ticket132 Goldbach K56", "23019645297/2140000000000");
      requireText("ticket132 Goldbach target", "PointwiseBinaryGoldbachResidualK56OnPowersOfTwoAndRoughStrata");
    } else {
      requireText("ticket132 Twin theorem", "FiniteLocalSieveDataCannotCertifyTwinPrimality");
      requireText("ticket132 Twin CRT", "first composite-pair start");
      requireText("ticket132 Twin levels", "Audited levels4");
      requireText("ticket132 Twin target", "UnboundedTypeIIParitySensitiveExactGapCertificate");
    }
    requireText("ticket131 title", "Ticket 131 proof viability and target correction");
    requireText("ticket131 table", "TICKET131 audit");
    requireText("ticket131 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket131 scope", "증명 가능성 감사 / 난제 미해결");
    requireText("ticket131 proximity", "proof proximity / 증명 근접도");
    if (page.problemId === "riemann") {
      requireText("ticket131 RH theorem", "FiniteDimensionalPositivityCannotCertifyUniversalWeilPositivity");
      requireText("ticket131 RH blind spot", "유한 양성의 한계");
      requireText("ticket131 RH target", "WeilSpecificCoerciveTailOrMonotoneOperatorLimit");
    } else if (page.problemId === "collatz") {
      requireText("ticket131 Collatz theorem", "NaturalRealizationIffCylinderResiduesEventuallyStabilize");
      requireText("ticket131 Collatz correction", "strict valuation cap은");
      requireText("ticket131 Collatz criterion", "eventually stabilize");
      requireText("ticket131 Collatz target", "NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope");
    } else if (page.problemId === "goldbach") {
      requireText("ticket131 Goldbach theorem", "ArithmeticStratifiedGoldbachResidualBudgets");
      requireText("ticket131 Goldbach stratum", "p≤103");
      requireText("ticket131 Goldbach margin", "98007974997/216140000000000");
      requireText("ticket131 Goldbach target", "PointwiseBinaryGoldbachResidualByRoughnessStratum");
    } else {
      requireText("ticket131 Twin theorem", "RelativeIncrementTargetIsExactReparameterization");
      requireText("ticket131 Twin identity", "(a-k)/(1+k)=QX/QY-1");
      requireText("ticket131 Twin correction", "R<2/23은 새 cancellation 정리가 아니라");
      requireText("ticket131 Twin target", "UniformSignedVaughanBlockTransportWithParityBridge");
    }
    requireText("ticket130 title", "Ticket 130 computability, cap-language no-go, and route optimality");
    requireText("ticket130 table", "TICKET130 audit");
    requireText("ticket130 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket130 scope", "conjecture open / 난제 미해결");
    requireText("ticket130 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket130 RH theorem", "ComputableWeilCoreValueAndNegativeWitnessSemidecision");
      requireText("ticket130 RH interval", "width <2-s");
      requireText("ticket130 RH halt", "interval_upper<0");
      requireText("ticket130 RH target", "UniversalNonnegativeWeilCoreCertificate");
    } else if (page.problemId === "collatz") {
      requireText("ticket130 Collatz theorem", "CapLanguageNonExtinctionAndExponentialDensityZero");
      requireText("ticket130 Collatz correction", "finite cap-language extinction 목표는 불가능");
      requireText("ticket130 Collatz rho", "0.946620415970");
      requireText("ticket130 Collatz target", "ArchimedeanNaturalExclusionForAllInfiniteCapPaths");
    } else if (page.problemId === "goldbach") {
      requireText("ticket130 Goldbach theorem", "K56OptimalIntegerForFixedUniformCoefficientGlue");
      requireText("ticket130 Goldbach chain", "A≤2C2<2P47<57/43<57/log H");
      requireText("ticket130 Goldbach K56", "largest integer available");
      requireText("ticket130 Goldbach target", "PointwiseBinaryGoldbachResidualK56");
    } else {
      requireText("ticket130 Twin theorem", "DimensionlessRelativeIncrementReduction");
      requireText("ticket130 Twin identity", "D(Y)=QYR(Y)");
      requireText("ticket130 Twin threshold", "2/23");
      requireText("ticket130 Twin refined target", "UniformSignedVaughanBlockTransportWithParityBridge");
    }
    requireText("ticket129 title", "Ticket 129 enumerable core, valuation cap, and endpoint budget");
    requireText("ticket129 table", "TICKET129 audit");
    requireText("ticket129 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket129 scope", "conjecture open / 난제 미해결");
    requireText("ticket129 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket129 RH theorem", "EnumerableRationalBumpAutocorrelationCoreDensity");
      requireText("ticket129 RH density", "dense inside the autocorrelation image");
      requireText("ticket129 RH atoms", "219,490,560");
      requireText("ticket129 RH target", "CertifiedWeilValuesOnRationalBumpCore");
    } else if (page.problemId === "collatz") {
      requireText("ticket129 Collatz theorem", "LeastCounterexampleInitialValuationCap");
      requireText("ticket129 Collatz horizon", "536,870,912");
      requireText("ticket129 Collatz cap", "valuation sum cap");
      requireText("ticket129 Collatz mass", "4.7634970603e-9");
      requireText("ticket129 Collatz superseded target", "Superseded: ArchimedeanNaturalExclusionForAllInfiniteCapPaths");
    } else if (page.problemId === "goldbach") {
      requireText("ticket129 Goldbach theorem", "ExactRationalGoldbachResidualK56Sufficiency");
      requireText("ticket129 Goldbach K56", "K=56 sufficient");
      requireText("ticket129 Goldbach margin", "0.010756843597");
      requireText("ticket129 Goldbach K57", "K=57 same-budget margin");
      requireText("ticket129 Goldbach target", "PointwiseBinaryGoldbachResidualK56");
    } else {
      requireText("ticket129 Twin theorem", "ExactWithinBlockIncrementSynchronizationCriterion");
      requireText("ticket129 Twin identity", "target limsup D(2j)<0.08");
      requireText("ticket129 Twin midpoint", "1.84");
      requireText("ticket129 Twin defect", "midpoint increment defect");
      requireText("ticket129 Twin target", "AsymptoticVaughanIncrementSynchronizationBelow008");
    }
    requireText("ticket128 title", "Ticket 128 finite core, prefix closure, constant sharpening, and interpolation");
    requireText("ticket128 table", "TICKET128 audit");
    requireText("ticket128 previous", "PREVIOUS / 이전 연구 경계");
    requireText("ticket128 scope", "conjecture open / 난제 미해결");
    requireText("ticket128 resolutions", "conjecture resolutions / 난제 해결");
    if (page.problemId === "riemann") {
      requireText("ticket128 RH theorem", "CompactSupportFinitePrimeSideReduction");
      requireText("ticket128 RH prime powers", "78,734");
      requireText("ticket128 RH target", "ArchimedeanIntervalAndAdmissibleCoreDensity");
    } else if (page.problemId === "collatz") {
      requireText("ticket128 Collatz theorem", "FinitePrefixEventuallyLowExclusion");
      requireText("ticket128 Collatz direct closure", "4,027,109");
      requireText("ticket128 Collatz zero survivors", "step-cap survivors");
      requireText("ticket128 Collatz max steps", "249");
      requireText("ticket128 Collatz witness", "217,740,015");
      requireText("ticket128 Collatz peak", "2,134,932,387,040,421");
      requireText("ticket128 Collatz target", "UnboundedPrefixClosureOrUniformNontrivialPathRank");
    } else if (page.problemId === "goldbach") {
      requireText("ticket128 Goldbach theorem", "ExplicitTwinConstantTailLowerBound");
      requireText("ticket128 Goldbach A", "A > 1.31917");
      requireText("ticket128 Goldbach K", "candidate residual K");
      requireText("ticket128 Goldbach margin", "0.009644249026");
      requireText("ticket128 Goldbach target", "PointwiseBinaryGoldbachResidualK55");
    } else {
      requireText("ticket128 Twin theorem", "DyadicEndpointInsufficiencyAndAllScaleEnvelope");
      requireText("ticket128 Twin countermodel", "dyadic endpoint에서 Q=0.92");
      requireText("ticket128 Twin condition", "0.92*c+delta<1");
      requireText("ticket128 Twin target", "VaughanWithinDyadicBlockEnvelopeC1DeltaBelow008");
    }
    requireText("ticket127 title", "Ticket 127 exception repair and effective bridges");
    requireText("ticket127 table", "TICKET127 audit");
    requireText("ticket127 previous", "PREVIOUS / 이전 연구 경계");
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
    requireText("ticket126 foundation", "FOUNDATION / 기초 연구 계약");
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
    ["panel", metrics.evolutionPanel, "TICKET-245"],
    ["panel", metrics.evolutionPanel, "TICKET-264"],
    ["panel", metrics.evolutionPanel, "4 current cards / 264 tickets"],
    ["panel", metrics.evolutionPanel, "TICKET-247"],
    ["panel", metrics.evolutionPanel, "TICKET-249"],
    ["panel", metrics.evolutionPanel, "TICKET-248"],
    ["panel", metrics.evolutionPanel, "TICKET-246"],
    ["panel", metrics.evolutionPanel, "TICKET-149"],
    ["panel", metrics.evolutionPanel, "Open-Proof"],
    ["panel", metrics.evolutionPanel, "TICKET-243"],
    ["panel", metrics.evolutionPanel, "TICKET-244"],
    ["panel", metrics.evolutionPanel, "Multishell accumulation"],
    ["panel", metrics.evolutionPanel, "99%"],
    ["panel", metrics.evolutionPanel, "Adaptive clearance, single-one exclusion, CRT witnesses"],
    ["panel", metrics.evolutionPanel, "Form-core topology"],
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
    !metrics.atlasPanel.includes("TICKET-264") ||
    !metrics.atlasPanel.includes("ActualWeilPacketReciprocalEnvelopeBelowHalfLimit") ||
    !metrics.atlasPanel.includes("CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation") ||
    !metrics.atlasPanel.includes("Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo") ||
    !metrics.atlasPanel.includes("NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences") ||
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
    !metrics.evolutionPanel.includes("TICKET-245") ||
    !metrics.evolutionPanel.includes("TICKET-247") ||
    !metrics.evolutionPanel.includes("TICKET-254") ||
    !metrics.evolutionPanel.includes("TICKET-253") ||
    !metrics.evolutionPanel.includes("TICKET-252") ||
    !metrics.evolutionPanel.includes("TICKET-251") ||
    !metrics.evolutionPanel.includes("TICKET-250") ||
    !metrics.evolutionPanel.includes("TICKET-249") ||
    !metrics.evolutionPanel.includes("TICKET-248") ||
    !metrics.evolutionPanel.includes("TICKET-246") ||
    !metrics.evolutionPanel.includes("Evidence pack") ||
    !metrics.evolutionPanel.includes("Publication consistency") ||
    !metrics.evolutionPanel.includes("TICKET-242") ||
    !metrics.evolutionPanel.includes("TICKET-243") ||
    !metrics.evolutionPanel.includes("TICKET-244") ||
    !metrics.evolutionPanel.includes("TICKET-239") ||
    !metrics.evolutionPanel.includes("TICKET-233") ||
    !metrics.evolutionPanel.includes("TICKET-232") ||
    !metrics.evolutionPanel.includes("TICKET-231") ||
    !metrics.evolutionPanel.includes("TICKET-230") ||
    !metrics.evolutionPanel.includes("TICKET-229") ||
    !metrics.evolutionPanel.includes("TICKET-228") ||
    !metrics.evolutionPanel.includes("TICKET-227") ||
    !metrics.evolutionPanel.includes("TICKET-226") ||
    !metrics.evolutionPanel.includes("TICKET-225") ||
    !metrics.evolutionPanel.includes("TICKET-224") ||
    !metrics.evolutionPanel.includes("TICKET-223") ||
    !metrics.evolutionPanel.includes("TICKET-222") ||
    !metrics.evolutionPanel.includes("TICKET-221") ||
    !metrics.evolutionPanel.includes("TICKET-220") ||
    !metrics.evolutionPanel.includes("TICKET-219") ||
    !metrics.evolutionPanel.includes("TICKET-218") ||
    !metrics.evolutionPanel.includes("TICKET-217") ||
    !metrics.evolutionPanel.includes("TICKET-216") ||
    !metrics.evolutionPanel.includes("TICKET-215") ||
    !metrics.evolutionPanel.includes("TICKET-214") ||
    !metrics.evolutionPanel.includes("TICKET-213") ||
    !metrics.evolutionPanel.includes("TICKET-212") ||
    !metrics.evolutionPanel.includes("TICKET-211") ||
    !metrics.evolutionPanel.includes("TICKET-210") ||
    !metrics.evolutionPanel.includes("TICKET-209") ||
    !metrics.evolutionPanel.includes("TICKET-208") ||
    !metrics.evolutionPanel.includes("TICKET-207") ||
    !metrics.evolutionPanel.includes("TICKET-205") ||
    !metrics.evolutionPanel.includes("TICKET-204") ||
    !metrics.evolutionPanel.includes("TICKET-203") ||
    !metrics.evolutionPanel.includes("TICKET-202") ||
    !metrics.evolutionPanel.includes("TICKET-201") ||
    !metrics.evolutionPanel.includes("TICKET-200") ||
    !metrics.evolutionPanel.includes("TICKET-199") ||
    !metrics.evolutionPanel.includes("TICKET-197") ||
    !metrics.evolutionPanel.includes("TICKET-195") ||
    !metrics.evolutionPanel.includes("TICKET-194") ||
    !metrics.evolutionPanel.includes("TICKET-193") ||
    !metrics.evolutionPanel.includes("TICKET-192") ||
    !metrics.evolutionPanel.includes("TICKET-191") ||
    !metrics.evolutionPanel.includes("TICKET-153") ||
    !metrics.evolutionPanel.includes("TICKET-152") ||
    !metrics.evolutionPanel.includes("TICKET-151") ||
    !metrics.evolutionPanel.includes("TICKET-150") ||
    !metrics.evolutionPanel.includes("TICKET-149") ||
    !metrics.evolutionPanel.includes("Essential tails") ||
    !metrics.evolutionPanel.includes("Compression exhaustion") ||
    !metrics.evolutionPanel.includes("Negative spectra") ||
    !metrics.evolutionPanel.includes("0 conjecture resolutions") ||
    !metrics.evolutionPanel.includes("Open-Proof") ||
    !metrics.evolutionPanel.includes("99%") ||
    !metrics.evolutionPanel.includes("Adaptive clearance, single-one exclusion, CRT witnesses") ||
    metrics.evolutionPanel.includes("TICKET200 proves four exact partial theorems") ||
    !metrics.evolutionPanel.includes("Form-core topology") ||
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
    !metrics.evolutionPanel.includes("TICKET-121") ||
    !metrics.evolutionPanel.includes("TICKET-161") ||
    !metrics.evolutionPanel.includes("TICKET-162") ||
    !metrics.evolutionPanel.includes("TICKET-163") ||
    !metrics.evolutionPanel.includes("TICKET-164") ||
    !metrics.evolutionPanel.includes("TICKET-165") ||
    !metrics.evolutionPanel.includes("TICKET-166") ||
    !metrics.evolutionPanel.includes("TICKET-167") ||
    !metrics.evolutionPanel.includes("TICKET-168") ||
    !metrics.evolutionPanel.includes("TICKET-169") ||
    !metrics.evolutionPanel.includes("TICKET-170") ||
    !metrics.evolutionPanel.includes("gap-relative operator control") ||
    !metrics.evolutionPanel.includes("large-valuation Collatz child tail") ||
    !metrics.evolutionPanel.includes("fixed coarse Type-II partitions can hide") ||
    !metrics.evolutionPanel.includes("constrained RH positivity to KKT inertia") ||
    !metrics.evolutionPanel.includes("phase-sensitive Goldbach pointwise certificate") ||
    !metrics.evolutionPanel.includes("positive linear Twin finest-pairing bound is already an endgame theorem") ||
    !metrics.evolutionPanel.includes("TICKET-168 proves that a fixed bounded corrector") ||
    !metrics.evolutionPanel.includes("spectral l1 is the optimal phase-blind Goldbach bound") ||
    !metrics.evolutionPanel.includes("contains exactly half") ||
    !metrics.evolutionPanel.includes("TICKET-167 reduces RH finite certification") ||
    !metrics.evolutionPanel.includes("exact floor formula") ||
    !metrics.evolutionPanel.includes("finest 2x2 Haar projection") ||
    !metrics.evolutionPanel.includes("TICKET-129") ||
    !metrics.evolutionPanel.includes("TICKET-130") ||
    !metrics.evolutionPanel.includes("TICKET-131")
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
