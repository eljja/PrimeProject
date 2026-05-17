const state = {
  generator: "next_prime",
  limit: 120000,
  modulo: 30,
  renderedSamples: 2200,
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
  runExperiment: document.querySelector("#runExperiment"),
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

controls.runExperiment.addEventListener("click", runExperiment);

window.addEventListener("resize", () => {
  window.requestAnimationFrame(render);
});

runExperiment();

function runExperiment() {
  controls.runExperiment.disabled = true;
  controls.runExperiment.textContent = "Running...";
  outputs.runStatus.textContent = "Running";
  window.requestAnimationFrame(() => {
    state.lab = buildLab(state.limit, state.modulo);
    controls.runExperiment.disabled = false;
    controls.runExperiment.textContent = "Run Experiment";
    outputs.runStatus.textContent = "Completed";
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
  renderTimeline();
  renderGapCanvas();
  renderResidueWheel();
  renderHistogram();
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
  const weights = observations.map((observation) => observation[state.generator]);
  const maxWeight = Math.max(...weights);

  context.clearRect(0, 0, width, height);
  context.fillStyle = "#fff";
  context.fillRect(0, 0, width, height);
  drawGrid(context, padding, plotWidth, plotHeight, maxPrime, maxGap);

  observations.forEach((observation) => {
    const x = padding.left + (observation.prime / maxPrime) * plotWidth;
    const y = padding.top + plotHeight - (observation.gap / maxGap) * plotHeight;
    const weight = observation[state.generator];
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
  const cx = 210;
  const cy = 160;
  const radius = 96;
  const labelRadius = 132;
  svg.innerHTML = "";

  appendSvg(svg, "circle", { cx, cy, r: radius, fill: "none", stroke: colors.line, "stroke-width": 1 });
  appendSvg(svg, "text", {
    x: cx,
    y: 26,
    "text-anchor": "middle",
    class: "chart-title",
  }).textContent = `mod ${state.modulo} weighted residue mass`;

  distribution.forEach((entry, index) => {
    const angle = -Math.PI / 2 + (index / distribution.length) * Math.PI * 2;
    const massRadius = 16 + (entry.mass / maxMass) * 74;
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
    const labelX = cx + Math.cos(angle) * labelRadius;
    const labelY = cy + Math.sin(angle) * labelRadius;
    appendSvg(svg, "text", {
      x: labelX,
      y: labelY,
      "text-anchor": "middle",
      class: "chart-label",
    }).textContent = entry.residue;
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
  const totalWeight = sum(observations.map((observation) => observation[state.generator]));
  observations.forEach((observation) => {
    const bin = Math.min(bins - 1, Math.floor((observation.gap / (maxGap + 1)) * bins));
    histogram[bin].mass += observation[state.generator] / totalWeight;
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

function thinObservations(observations, target) {
  if (observations.length <= target) return observations;
  const step = observations.length / target;
  const thinned = [];
  for (let index = 0; index < target; index += 1) {
    thinned.push(observations[Math.floor(index * step)]);
  }
  return thinned;
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
