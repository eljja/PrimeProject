const path = require("node:path");
const fs = require("node:fs");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

async function main() {
  const root = path.resolve(__dirname, "..");
  const url = pathToFileURL(path.join(root, "index.html")).href;
  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  const browser = await chromium.launch({
    headless: true,
    executablePath: fs.existsSync(chromePath) ? chromePath : undefined,
  });
  const errors = [];

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
  await page.screenshot({
    path: path.join(root, "data", "conjecture_lab_desktop.png"),
    fullPage: true,
  });

  const metrics = await page.evaluate(() => ({
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
    bitcoinPanel: document.querySelector("#bitcoin-panel").textContent,
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

  await browser.close();

  if (errors.length > 0) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (metrics.snapshotButtons < 2 || !metrics.snapshotImagesReady) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (metrics.predictionRows < 8 || !metrics.predictionMetrics.includes("Actual next")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  if (!metrics.bitcoinPanel.includes("secp256k1") || !metrics.bitcoinPanel.includes("Repeated ECDSA r")) {
    console.error(JSON.stringify({ errors, metrics }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({ errors, metrics }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
