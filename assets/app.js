const state = {
  generator: "next_prime",
  limit: 120000,
  modulo: 30,
  renderedSamples: 2200,
  weighting: "gap",
  lab: null,
};

const generatorCopy = {
  next_prime:
    "next_prime sampling changes the observed prime measure by weighting each prime by its left gap.",
  rejection:
    "rejection sampling approximates the counting measure over accepted primes and is the baseline for drift.",
  wheel30_next:
    "wheel sampling observes primes through a sieve-shaped candidate space, compressing part of the gap signal.",
};

const colors = {
  ink: "#17191f",
  muted: "#626873",
  line: "#d9dee7",
  teal: "#087f7a",
  amber: "#d78a11",
  indigo: "#4657d8",
  danger: "#bd3d34",
  soft: "#f4f7fa",
};

const controls = {
  limitRange: document.querySelector("#limitRange"),
  limitValue: document.querySelector("#limitValue"),
  sampleRange: document.querySelector("#sampleRange"),
  sampleValue: document.querySelector("#sampleValue"),
  moduloSelect: document.querySelector("#moduloSelect"),
  weightingSelect: document.querySelector("#weightingSelect"),
  runExperiment: document.querySelector("#runExperiment"),
  densityToggle: document.querySelector("#densityToggle"),
};

const outputs = {
  primeCount: document.querySelector("#primeCount"),
  weightedMeanGap: document.querySelector("#weightedMeanGap"),
  driftMetric: document.querySelector("#driftMetric"),
  entropyMetric: document.querySelector("#entropyMetric"),
  supportMetric: document.querySelector("#supportMetric"),
  maxShareMetric: document.querySelector("#maxShareMetric"),
  activeClaim: document.querySelector("#activeClaim"),
  timelineRows: document.querySelector("#timelineRows"),
  runStatus: document.querySelector("#runStatus"),
  controlStatus: document.querySelector("#controlStatus"),
  controlPrimeCount: document.querySelector("#controlPrimeCount"),
  controlMaxPrime: document.querySelector("#controlMaxPrime"),
  controlThroughput: document.querySelector("#controlThroughput"),
  comparisonCards: document.querySelector("#comparisonCards"),
};

document.querySelectorAll("[data-generator]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-generator]").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    state.generator = button.dataset.generator;
    outputs.activeClaim.textContent = generatorCopy[state.generator];
    render();
  });
});

document.querySelectorAll("[data-scroll-target]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-scroll-target]").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    document.querySelector(`#${button.dataset.scrollTarget}`).scrollIntoView({ block: "start" });
  });
});

controls.limitRange.addEventListener("input", () => {
  state.limit = Number(controls.limitRange.value);
  controls.limitValue.textContent = formatNumber(state.limit);
});

controls.sampleRange.addEventListener("input", () => {
  state.renderedSamples = Number(controls.sampleRange.value);
  controls.sampleValue.textContent = formatNumber(state.renderedSamples);
  render();
});

controls.moduloSelect.addEventListener("change", () => {
  state.modulo = Number(controls.moduloSelect.value);
  runExperiment();
});

controls.weightingSelect.addEventListener("change", () => {
  state.weighting = controls.weightingSelect.value;
  render();
});

controls.densityToggle.addEventListener("change", render);

controls.runExperiment.addEventListener("click", runExperiment);

window.addEventListener("resize", () => {
  window.requestAnimationFrame(render);
});

runExperiment();

function runExperiment() {
  controls.runExperiment.disabled = true;
  controls.runExperiment.textContent = "Running...";
  outputs.runStatus.textContent = "Running";
  outputs.controlStatus.textContent = "Running";
  window.requestAnimationFrame(() => {
    const started = performance.now();
    state.lab = buildLab(state.limit, state.modulo);
    state.lab.elapsedMs = Math.max(1, performance.now() - started);
    controls.runExperiment.disabled = false;
    controls.runExperiment.textContent = "Run Experiment";
    outputs.runStatus.textContent = "Completed";
    outputs.controlStatus.textContent = "Completed";
    render();
  });
}

function buildLab(limit, modulo) {
  const primes = sievePrimes(limit);
  const observations = [];
  for (let index = 1; index < primes.length; index += 1) {
    const previousPrime = primes[index - 1];
    const prime = primes[index];
    const gap = prime - previousPrime;
    observations.push({
      prime,
      previousPrime,
      gap,
      rejection: 1,
      next_prime: gap,
      wheel30_next: countWheel30(previousPrime, prime),
    });
  }
  const summaries = {};
  for (const generator of ["rejection", "next_prime", "wheel30_next"]) {
    summaries[generator] = summarize(observations, generator, modulo);
  }
  return { limit, modulo, primes, observations, summaries };
}

function sievePrimes(limit) {
  const sieve = new Uint8Array(limit + 1);
  sieve.fill(1);
  sieve[0] = 0;
  sieve[1] = 0;
  for (let candidate = 2; candidate * candidate <= limit; candidate += 1) {
    if (!sieve[candidate]) continue;
    for (let multiple = candidate * candidate; multiple <= limit; multiple += candidate) {
      sieve[multiple] = 0;
    }
  }
  const primes = [];
  for (let value = 2; value <= limit; value += 1) {
    if (sieve[value]) primes.push(value);
  }
  return primes;
}

function countWheel30(previousPrime, prime) {
  let count = 0;
  for (let value = previousPrime + 1; value <= prime; value += 1) {
    const residue = value % 30;
    if ([1, 7, 11, 13, 17, 19, 23, 29].includes(residue)) count += 1;
  }
  return Math.max(1, count);
}

function summarize(observations, generator, modulo) {
  const weights = observations.map((observation) => observation[generator]);
  const totalWeight = sum(weights);
  const probabilities = weights.map((weight) => weight / totalWeight);
  const entropyBits = -sum(probabilities.map((probability) => (probability > 0 ? probability * Math.log2(probability) : 0)));
  const meanGap = sum(observations.map((observation) => observation.gap)) / observations.length;
  const weightedMeanGap =
    sum(observations.map((observation, index) => observation.gap * weights[index])) / totalWeight;
  const residueDistribution = weightedResidueDistribution(observations, weights, modulo);
  const residueTotalVariation = totalVariation(residueDistribution, modulo);
  return {
    totalWeight,
    entropyBits,
    effectiveSupport: 2 ** entropyBits,
    maxWeightShare: Math.max(...probabilities),
    meanGap,
    weightedMeanGap,
    residueTotalVariation,
    residueDistribution,
  };
}

function weightedResidueDistribution(observations, weights, modulo) {
  const distribution = new Map();
  let totalWeight = 0;
  observations.forEach((observation, index) => {
    const residue = observation.prime % modulo;
    if (gcd(residue, modulo) !== 1) return;
    const weight = weights[index];
    distribution.set(residue, (distribution.get(residue) || 0) + weight);
    totalWeight += weight;
  });
  return [...distribution.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([residue, weight]) => ({ residue, mass: weight / totalWeight }));
}

function totalVariation(distribution, modulo) {
  const residues = [];
  for (let residue = 0; residue < modulo; residue += 1) {
    if (gcd(residue, modulo) === 1) residues.push(residue);
  }
  const uniform = 1 / residues.length;
  const lookup = new Map(distribution.map((entry) => [entry.residue, entry.mass]));
  return 0.5 * sum(residues.map((residue) => Math.abs((lookup.get(residue) || 0) - uniform)));
}

function render() {
  if (!state.lab) return;
  const summary = state.lab.summaries[state.generator];
  outputs.primeCount.textContent = formatNumber(state.lab.primes.length);
  outputs.weightedMeanGap.textContent = summary.weightedMeanGap.toFixed(2);
  outputs.driftMetric.textContent = summary.residueTotalVariation.toFixed(4);
  outputs.entropyMetric.textContent = `${summary.entropyBits.toFixed(2)} bits`;
  outputs.supportMetric.textContent = formatNumber(Math.round(summary.effectiveSupport));
  outputs.maxShareMetric.textContent = `${(summary.maxWeightShare * 100).toFixed(3)}%`;
  outputs.controlPrimeCount.textContent = formatNumber(state.lab.primes.length);
  outputs.controlMaxPrime.textContent = formatNumber(state.lab.primes.at(-1) || 0);
  outputs.controlThroughput.textContent = `${formatNumber(Math.round(state.lab.primes.length / (state.lab.elapsedMs / 1000)))}/s`;
  renderTimeline();
  renderOverviewCanvas();
  renderGapCanvas();
  renderResidueWheel();
  renderGapDistribution();
  renderHistogram();
  renderLocalScaleCanvas();
  renderHeatmap();
  renderComparisons();
}

function renderTimeline() {
  const generators = ["next_prime", "rejection", "wheel30_next"];
  outputs.timelineRows.innerHTML = generators
    .map((generator, index) => {
      const summary = state.lab.summaries[generator];
      return `<tr>
        <td>#${String(index + 1).padStart(3, "0")}</td>
        <td>${labelForGenerator(generator)}</td>
        <td>2-${formatCompact(state.lab.limit)}</td>
        <td>mod ${state.modulo}</td>
        <td>${formatNumber(state.lab.primes.length)}</td>
        <td>${summary.weightedMeanGap.toFixed(2)}</td>
        <td>${summary.residueTotalVariation.toFixed(4)}</td>
        <td><span class="status-dot"></span>Completed</td>
      </tr>`;
    })
    .join("");
}

function renderOverviewCanvas() {
  const canvas = document.querySelector("#overviewCanvas");
  const context = canvas.getContext("2d");
  const ratio = window.devicePixelRatio || 1;
  const bounds = canvas.getBoundingClientRect();
  canvas.width = Math.floor(bounds.width * ratio);
  canvas.height = Math.floor(bounds.height * ratio);
  context.scale(ratio, ratio);

  const width = bounds.width;
  const height = bounds.height;
  const padding = { top: 30, right: 26, bottom: 46, left: 62 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;
  const primes = state.lab.primes.slice(1);
  const maxIndex = primes.length;
  const maxPrime = Math.max(...primes);
  const minPrime = 2;
  const generators = [
    ["next_prime", colors.teal],
    ["rejection", colors.amber],
    ["wheel30_next", colors.indigo],
  ];

  context.clearRect(0, 0, width, height);
  context.fillStyle = "#fff";
  context.fillRect(0, 0, width, height);
  drawLogGrid(context, padding, plotWidth, plotHeight, maxIndex, minPrime, maxPrime);

  generators.forEach(([generator, color], seriesIndex) => {
    const observations = thinObservations(state.lab.observations, Math.min(state.renderedSamples, 1800));
    const maxWeight = Math.max(...observations.map((observation) => transformedWeight(observation, generator)));
    observations.forEach((observation, index) => {
      const primeIndex = Math.max(1, Math.floor((index / observations.length) * maxIndex));
      const x = padding.left + (Math.log10(primeIndex) / Math.log10(maxIndex)) * plotWidth;
      const y = padding.top + plotHeight - (Math.log10(observation.prime / minPrime) / Math.log10(maxPrime / minPrime)) * plotHeight;
      const weight = transformedWeight(observation, generator);
      const jitter = (seriesIndex - 1) * 2.4;
      context.globalAlpha = controls.densityToggle.checked ? 0.22 : 0.46;
      context.fillStyle = color;
      context.beginPath();
      context.arc(x + jitter, y + jitter, 1.2 + 2.2 * Math.sqrt(weight / maxWeight), 0, Math.PI * 2);
      context.fill();
    });
  });
  context.globalAlpha = 1;

  context.setLineDash([6, 5]);
  context.strokeStyle = "#343a43";
  context.lineWidth = 1.2;
  context.beginPath();
  for (let i = 3; i <= maxIndex; i += Math.ceil(maxIndex / 120)) {
    const approx = Math.max(3, i * Math.log(i));
    const x = padding.left + (Math.log10(i) / Math.log10(maxIndex)) * plotWidth;
    const y = padding.top + plotHeight - (Math.log10(approx / minPrime) / Math.log10(maxPrime / minPrime)) * plotHeight;
    if (i === 3) context.moveTo(x, y);
    else context.lineTo(x, y);
  }
  context.stroke();
  context.setLineDash([]);
  context.fillStyle = colors.ink;
  context.font = "700 12px Inter, system-ui, sans-serif";
  context.fillText("dashed baseline: p_n ≈ n log n", padding.left + plotWidth - 190, padding.top + 18);
}

function renderGapCanvas() {
  const canvas = document.querySelector("#gapCanvas");
  const context = canvas.getContext("2d");
  const ratio = window.devicePixelRatio || 1;
  const bounds = canvas.getBoundingClientRect();
  canvas.width = Math.floor(bounds.width * ratio);
  canvas.height = Math.floor(bounds.height * ratio);
  context.scale(ratio, ratio);

  const width = bounds.width;
  const height = bounds.height;
  const padding = { top: 28, right: 32, bottom: 46, left: 62 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;
  const observations = thinObservations(state.lab.observations, state.renderedSamples);
  const maxPrime = state.lab.limit;
  const maxGap = Math.max(...state.lab.observations.map((observation) => observation.gap));
  const weights = observations.map((observation) => transformedWeight(observation, state.generator));
  const maxWeight = Math.max(...weights);

  context.clearRect(0, 0, width, height);
  context.fillStyle = "#fff";
  context.fillRect(0, 0, width, height);
  drawGrid(context, padding, plotWidth, plotHeight, maxPrime, maxGap);

  observations.forEach((observation) => {
    const x = padding.left + (observation.prime / maxPrime) * plotWidth;
    const y = padding.top + plotHeight - (observation.gap / maxGap) * plotHeight;
    const weight = transformedWeight(observation, state.generator);
    const radius = 1.4 + 5.8 * Math.sqrt(weight / maxWeight);
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.fillStyle = pointColor(weight / maxWeight, observation.gap / maxGap);
    context.globalAlpha = 0.76;
    context.fill();
  });
  context.globalAlpha = 1;

  context.fillStyle = colors.ink;
  context.font = "700 12px Inter, system-ui, sans-serif";
  context.fillText(`${labelForGenerator(state.generator)} observation measure`, padding.left, 18);
  context.fillStyle = colors.muted;
  context.font = "650 11px Inter, system-ui, sans-serif";
  context.fillText("prime value", padding.left + plotWidth - 56, height - 12);
  context.save();
  context.translate(16, padding.top + 96);
  context.rotate(-Math.PI / 2);
  context.fillText("prime gap", 0, 0);
  context.restore();
}

function drawLogGrid(context, padding, plotWidth, plotHeight, maxIndex, minPrime, maxPrime) {
  context.strokeStyle = colors.line;
  context.lineWidth = 1;
  context.fillStyle = colors.muted;
  context.font = "11px Inter, system-ui, sans-serif";
  const indexTicks = [10, 100, 1000, 10000, 100000].filter((tick) => tick <= maxIndex);
  indexTicks.forEach((tick) => {
    const x = padding.left + (Math.log10(tick) / Math.log10(maxIndex)) * plotWidth;
    context.beginPath();
    context.moveTo(x, padding.top);
    context.lineTo(x, padding.top + plotHeight);
    context.stroke();
    context.fillText(formatCompact(tick), x - 8, padding.top + plotHeight + 22);
  });
  const primeTicks = [10, 100, 1000, 10000, 100000, 1000000].filter(
    (tick) => tick >= minPrime && tick <= maxPrime,
  );
  primeTicks.forEach((tick) => {
    const y = padding.top + plotHeight - (Math.log10(tick / minPrime) / Math.log10(maxPrime / minPrime)) * plotHeight;
    context.beginPath();
    context.moveTo(padding.left, y);
    context.lineTo(padding.left + plotWidth, y);
    context.stroke();
    context.fillText(formatCompact(tick), 20, y + 4);
  });
}

function drawGrid(context, padding, plotWidth, plotHeight, maxPrime, maxGap) {
  context.strokeStyle = colors.line;
  context.lineWidth = 1;
  context.fillStyle = colors.muted;
  context.font = "11px Inter, system-ui, sans-serif";
  for (let tick = 0; tick <= 4; tick += 1) {
    const x = padding.left + (plotWidth * tick) / 4;
    context.beginPath();
    context.moveTo(x, padding.top);
    context.lineTo(x, padding.top + plotHeight);
    context.stroke();
    context.fillText(formatCompact((maxPrime * tick) / 4), x - 10, padding.top + plotHeight + 22);
  }
  for (let tick = 0; tick <= 4; tick += 1) {
    const y = padding.top + plotHeight - (plotHeight * tick) / 4;
    context.beginPath();
    context.moveTo(padding.left, y);
    context.lineTo(padding.left + plotWidth, y);
    context.stroke();
    context.fillText(String(Math.round((maxGap * tick) / 4)), 24, y + 4);
  }
}

function renderResidueWheel() {
  const svg = document.querySelector("#residueWheel");
  const summary = state.lab.summaries[state.generator];
  const distribution = summary.residueDistribution;
  const maxMass = Math.max(...distribution.map((entry) => entry.mass));
  const bounds = svg.getBoundingClientRect();
  const width = Math.max(320, Math.floor(bounds.width || 420));
  const height = Math.max(340, Math.floor(bounds.height || 380));
  const cx = width / 2;
  const cy = height / 2 + 12;
  const manyResidues = distribution.length > 24;
  const availableRadius = Math.min(width, height) / 2 - 42;
  const radius = Math.max(42, availableRadius * (manyResidues ? 0.46 : 0.5));
  const maxBar = Math.max(42, availableRadius - radius - 12);
  const labelRadius = radius + maxBar + (manyResidues ? 10 : 16);
  const labelStep = manyResidues ? Math.ceil(distribution.length / 24) : 1;
  svg.innerHTML = "";
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

  appendSvg(svg, "circle", { cx, cy, r: radius, fill: "none", stroke: colors.line, "stroke-width": 1 });
  appendSvg(svg, "text", {
    x: cx,
    y: 28,
    "text-anchor": "middle",
    class: "chart-title",
  }).textContent = `mod ${state.modulo} weighted residue mass`;

  distribution.forEach((entry, index) => {
    const angle = -Math.PI / 2 + (index / distribution.length) * Math.PI * 2;
    const massRadius = 18 + (entry.mass / maxMass) * maxBar;
    const x = cx + Math.cos(angle) * radius;
    const y = cy + Math.sin(angle) * radius;
    const endX = cx + Math.cos(angle) * (radius + massRadius);
    const endY = cy + Math.sin(angle) * (radius + massRadius);
    appendSvg(svg, "line", {
      x1: x,
      y1: y,
      x2: endX,
      y2: endY,
      stroke: index % 2 === 0 ? colors.teal : colors.indigo,
      "stroke-width": 4,
      "stroke-linecap": "square",
    });
    appendSvg(svg, "circle", { cx: endX, cy: endY, r: 4, fill: colors.amber });
    if (index % labelStep === 0) {
      const labelX = cx + Math.cos(angle) * labelRadius;
      const labelY = cy + Math.sin(angle) * labelRadius;
      appendSvg(svg, "text", {
        x: labelX,
        y: labelY,
        "text-anchor": "middle",
        class: "chart-label",
      }).textContent = entry.residue;
    }
  });

  appendSvg(svg, "text", {
    x: cx,
    y: cy - 4,
    "text-anchor": "middle",
    class: "chart-title",
  }).textContent = summary.residueTotalVariation.toFixed(4);
  appendSvg(svg, "text", {
    x: cx,
    y: cy + 15,
    "text-anchor": "middle",
    class: "chart-label",
  }).textContent = "TV drift";
}

function renderGapDistribution() {
  const svg = document.querySelector("#gapDistribution");
  const observations = state.lab.observations;
  const width = 520;
  const height = 420;
  const padding = { top: 44, right: 28, bottom: 44, left: 54 };
  const maxGap = Math.max(...observations.map((observation) => observation.gap));
  const bins = 28;
  const generators = [
    ["next_prime", colors.teal],
    ["rejection", colors.amber],
    ["wheel30_next", colors.indigo],
  ];
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;
  svg.innerHTML = "";
  appendSvg(svg, "text", { x: padding.left, y: 24, class: "chart-title" }).textContent =
    "Histogram / CCDF-style gap tail";
  appendSvg(svg, "line", {
    x1: padding.left,
    y1: padding.top + plotHeight,
    x2: padding.left + plotWidth,
    y2: padding.top + plotHeight,
    stroke: colors.line,
  });
  appendSvg(svg, "line", {
    x1: padding.left,
    y1: padding.top,
    x2: padding.left,
    y2: padding.top + plotHeight,
    stroke: colors.line,
  });
  generators.forEach(([generator, color], seriesIndex) => {
    const hist = buildGapHistogram(generator, bins, maxGap);
    const maxMass = Math.max(...hist.map((bin) => bin.mass));
    const points = hist.map((bin, index) => {
      const x = padding.left + (index / (bins - 1)) * plotWidth;
      const y = padding.top + plotHeight - (bin.mass / maxMass) * (plotHeight - 10) - seriesIndex * 2;
      return `${x},${y}`;
    });
    appendSvg(svg, "polyline", {
      points: points.join(" "),
      fill: "none",
      stroke: color,
      "stroke-width": 2.2,
      "stroke-linejoin": "round",
    });
  });
  appendSvg(svg, "text", { x: padding.left, y: height - 12, class: "axis-label" }).textContent = "gap Δ";
  appendSvg(svg, "text", { x: padding.left, y: padding.top + 18, class: "chart-label" }).textContent =
    "teal next | amber rejection | indigo wheel";
}

function renderHistogram() {
  const svg = document.querySelector("#histogram");
  const observations = state.lab.observations;
  const width = 520;
  const height = 320;
  const padding = { top: 36, right: 22, bottom: 34, left: 42 };
  const maxGap = Math.max(...observations.map((observation) => observation.gap));
  const bins = 18;
  const histogram = Array.from({ length: bins }, (_, index) => ({
    start: Math.floor((index / bins) * maxGap),
    end: Math.ceil(((index + 1) / bins) * maxGap),
    mass: 0,
  }));
  const totalWeight = sum(observations.map((observation) => transformedWeight(observation, state.generator)));
  observations.forEach((observation) => {
    const bin = Math.min(bins - 1, Math.floor((observation.gap / (maxGap + 1)) * bins));
    histogram[bin].mass += transformedWeight(observation, state.generator) / totalWeight;
  });
  const maxMass = Math.max(...histogram.map((bin) => bin.mass));
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;
  const barGap = 5;
  const barWidth = plotWidth / bins - barGap;

  svg.innerHTML = "";
  appendSvg(svg, "text", { x: padding.left, y: 22, class: "chart-title" }).textContent =
    `${labelForGenerator(state.generator)} gap-weight mass`;
  appendSvg(svg, "line", {
    x1: padding.left,
    y1: padding.top + plotHeight,
    x2: padding.left + plotWidth,
    y2: padding.top + plotHeight,
    stroke: colors.line,
  });
  appendSvg(svg, "line", {
    x1: padding.left,
    y1: padding.top,
    x2: padding.left,
    y2: padding.top + plotHeight,
    stroke: colors.line,
  });

  histogram.forEach((bin, index) => {
    const barHeight = (bin.mass / maxMass) * (plotHeight - 8);
    const x = padding.left + index * (plotWidth / bins);
    const y = padding.top + plotHeight - barHeight;
    appendSvg(svg, "rect", {
      x,
      y,
      width: barWidth,
      height: barHeight,
      fill: index % 3 === 0 ? colors.teal : index % 3 === 1 ? colors.amber : colors.indigo,
    });
    if (index % 5 === 0) {
      appendSvg(svg, "text", {
        x,
        y: height - 12,
        class: "axis-label",
      }).textContent = bin.start;
    }
  });
}

function renderLocalScaleCanvas() {
  const canvas = document.querySelector("#localScaleCanvas");
  const context = canvas.getContext("2d");
  const ratio = window.devicePixelRatio || 1;
  const bounds = canvas.getBoundingClientRect();
  canvas.width = Math.floor(bounds.width * ratio);
  canvas.height = Math.floor(bounds.height * ratio);
  context.scale(ratio, ratio);
  const width = bounds.width;
  const height = bounds.height;
  const padding = { top: 26, right: 24, bottom: 42, left: 50 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;
  const observations = thinObservations(state.lab.observations, Math.min(state.renderedSamples, 1800));
  const values = observations.map((observation) => observation.gap / Math.log(observation.prime));
  const maxValue = Math.max(...values);
  context.clearRect(0, 0, width, height);
  context.fillStyle = "#fff";
  context.fillRect(0, 0, width, height);
  context.strokeStyle = colors.line;
  context.fillStyle = colors.muted;
  context.font = "11px Inter, system-ui, sans-serif";
  for (let tick = 0; tick <= 4; tick += 1) {
    const y = padding.top + plotHeight - (plotHeight * tick) / 4;
    context.beginPath();
    context.moveTo(padding.left, y);
    context.lineTo(padding.left + plotWidth, y);
    context.stroke();
    context.fillText(((maxValue * tick) / 4).toFixed(1), 16, y + 4);
  }
  observations.forEach((observation, index) => {
    const x = padding.left + (observation.prime / state.lab.limit) * plotWidth;
    const value = values[index];
    const y = padding.top + plotHeight - (value / maxValue) * plotHeight;
    context.globalAlpha = 0.36;
    context.fillStyle = value > 3 ? colors.amber : colors.teal;
    context.beginPath();
    context.arc(x, y, 1.7, 0, Math.PI * 2);
    context.fill();
  });
  context.globalAlpha = 1;
  const median = medianOf(values);
  const medianY = padding.top + plotHeight - (median / maxValue) * plotHeight;
  context.setLineDash([5, 5]);
  context.strokeStyle = colors.indigo;
  context.beginPath();
  context.moveTo(padding.left, medianY);
  context.lineTo(padding.left + plotWidth, medianY);
  context.stroke();
  context.setLineDash([]);
  context.fillStyle = colors.ink;
  context.font = "700 12px Inter, system-ui, sans-serif";
  context.fillText(`median Δ/log p = ${median.toFixed(2)}`, padding.left, 18);
}

function renderHeatmap() {
  const svg = document.querySelector("#heatmap");
  const width = 620;
  const height = 300;
  const padding = { top: 38, right: 18, bottom: 28, left: 92 };
  const generators = ["next_prime", "rejection", "wheel30_next"];
  const residues = residueClasses(state.modulo);
  const maxColumns = Math.min(residues.length, 32);
  const shownResidues = residues.filter((_, index) => index % Math.ceil(residues.length / maxColumns) === 0);
  const cellWidth = (width - padding.left - padding.right) / shownResidues.length;
  const cellHeight = 44;
  svg.innerHTML = "";
  appendSvg(svg, "text", { x: padding.left, y: 24, class: "chart-title" }).textContent =
    `generator x residue drift, mod ${state.modulo}`;
  generators.forEach((generator, rowIndex) => {
    appendSvg(svg, "text", {
      x: 16,
      y: padding.top + rowIndex * cellHeight + 28,
      class: "chart-label",
    }).textContent = labelForGenerator(generator);
    const dist = new Map(state.lab.summaries[generator].residueDistribution.map((entry) => [entry.residue, entry.mass]));
    const uniform = 1 / residues.length;
    shownResidues.forEach((residue, columnIndex) => {
      const delta = (dist.get(residue) || 0) - uniform;
      const intensity = Math.min(1, Math.abs(delta) / uniform);
      const fill = delta >= 0 ? rgbaHex(colors.teal, 0.18 + intensity * 0.72) : rgbaHex(colors.amber, 0.18 + intensity * 0.72);
      appendSvg(svg, "rect", {
        x: padding.left + columnIndex * cellWidth,
        y: padding.top + rowIndex * cellHeight,
        width: Math.max(1, cellWidth - 2),
        height: cellHeight - 8,
        fill,
      });
      if (rowIndex === generators.length - 1 && columnIndex % Math.ceil(shownResidues.length / 10) === 0) {
        appendSvg(svg, "text", {
          x: padding.left + columnIndex * cellWidth,
          y: height - 10,
          class: "axis-label",
        }).textContent = residue;
      }
    });
  });
}

function renderComparisons() {
  const rows = ["next_prime", "rejection", "wheel30_next"].map((generator) => {
    const summary = state.lab.summaries[generator];
    return {
      label: labelForGenerator(generator),
      drift: summary.residueTotalVariation,
      support: summary.effectiveSupport,
      gap: summary.weightedMeanGap,
      max: summary.maxWeightShare,
    };
  });
  outputs.comparisonCards.innerHTML = rows
    .map(
      (row) => `<div class="comparison-card">
        <strong>${row.label}</strong><em>${row.drift.toFixed(4)}</em>
        <span>TV residue drift</span><span>${formatNumber(Math.round(row.support))} effective support</span>
        <span>weighted gap ${row.gap.toFixed(2)}</span><span>max share ${(row.max * 100).toFixed(3)}%</span>
      </div>`,
    )
    .join("");
}

function buildGapHistogram(generator, bins, maxGap) {
  const histogram = Array.from({ length: bins }, (_, index) => ({
    start: Math.floor((index / bins) * maxGap),
    mass: 0,
  }));
  const totalWeight = sum(state.lab.observations.map((observation) => transformedWeight(observation, generator)));
  state.lab.observations.forEach((observation) => {
    const bin = Math.min(bins - 1, Math.floor((observation.gap / (maxGap + 1)) * bins));
    histogram[bin].mass += transformedWeight(observation, generator) / totalWeight;
  });
  return histogram;
}

function transformedWeight(observation, generator) {
  const base = observation[generator];
  if (state.weighting === "inverse") return 1 / Math.max(1, observation.gap);
  if (state.weighting === "normalized") return base / Math.max(1, Math.log(observation.prime));
  return base;
}

function thinObservations(observations, target) {
  if (observations.length <= target) return observations;
  const step = observations.length / target;
  const thinned = [];
  for (let index = 0; index < target; index += 1) {
    thinned.push(observations[Math.floor(index * step)]);
  }
  return thinned;
}

function residueClasses(modulo) {
  const residues = [];
  for (let residue = 0; residue < modulo; residue += 1) {
    if (gcd(residue, modulo) === 1) residues.push(residue);
  }
  return residues;
}

function medianOf(values) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor(sorted.length / 2)] || 0;
}

function rgbaHex(hex, alpha) {
  const parsed = hex.replace("#", "");
  const r = parseInt(parsed.slice(0, 2), 16);
  const g = parseInt(parsed.slice(2, 4), 16);
  const b = parseInt(parsed.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function pointColor(weightShare, gapShare) {
  if (gapShare > 0.72) return colors.danger;
  if (weightShare > 0.44) return colors.amber;
  return state.generator === "rejection" ? colors.indigo : colors.teal;
}

function appendSvg(svg, tagName, attributes) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tagName);
  for (const [key, value] of Object.entries(attributes)) {
    element.setAttribute(key, value);
  }
  svg.appendChild(element);
  return element;
}

function labelForGenerator(generator) {
  return {
    next_prime: "next_prime",
    rejection: "rejection",
    wheel30_next: "wheel30_next",
  }[generator];
}

function gcd(a, b) {
  let x = Math.abs(a);
  let y = Math.abs(b);
  while (y !== 0) {
    const remainder = x % y;
    x = y;
    y = remainder;
  }
  return x;
}

function sum(values) {
  return values.reduce((total, value) => total + value, 0);
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function formatCompact(value) {
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}
