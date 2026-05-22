const state = {
  generator: "next_prime",
  limit: 120000,
  modulo: 30,
  renderedSamples: 2200,
  weighting: "gap",
  lab: null,
  snapshots: [],
  activeSnapshot: 0,
  attributionGrid: null,
  realBaselineManifest: null,
  researchReadiness: null,
  evidencePack: null,
  projectEvolution: null,
  collectionMatrix: null,
  collectionPower: null,
  provenanceRequirements: null,
  provenanceAudit: null,
};

const limitSlider = {
  min: 20000,
  max: 10000000,
  steps: 1000,
};

const bundledSnapshots = [
  {
    label: "1M",
    slug: "prime_measure_1m",
    limit: 1000000,
    modulo: 210,
    prime_count: 78498,
    max_gap: 114,
    mean_gap: 12.739098309489535,
    summary_path: "data/snapshots/prime_measure_1m.summary.json",
    overview_svg: "assets/snapshots/prime_measure_1m_overview.svg",
    gap_distribution_svg: "assets/snapshots/prime_measure_1m_gap_distribution.svg",
    residue_drift_svg: "assets/snapshots/prime_measure_1m_residue_drift.svg",
  },
  {
    label: "10M",
    slug: "prime_measure_10m",
    limit: 10000000,
    modulo: 210,
    prime_count: 664579,
    max_gap: 154,
    mean_gap: 15.047126146216096,
    summary_path: "data/snapshots/prime_measure_10m.summary.json",
    overview_svg: "assets/snapshots/prime_measure_10m_overview.svg",
    gap_distribution_svg: "assets/snapshots/prime_measure_10m_gap_distribution.svg",
    residue_drift_svg: "assets/snapshots/prime_measure_10m_residue_drift.svg",
  },
];

const bundledAttributionGrid = {
  schema: "primeproject.attribution-confound-grid.v1",
  random_baseline_accuracy: 1 / 3,
  repeats: 3,
  deltas: [
    {
      pair_key: "limit=50000;train=40;test=20",
      limit: 50000,
      train_count: 40,
      test_count: 20,
      profile: "all",
      uncontrolled_accuracy: 0.8333,
      controlled_accuracy: 0.5,
      accuracy_drop: 0.3333,
      interpretation: "inconclusive",
    },
    {
      pair_key: "limit=50000;train=40;test=20",
      limit: 50000,
      train_count: 40,
      test_count: 20,
      profile: "bit_length_only",
      uncontrolled_accuracy: 0.8333,
      controlled_accuracy: 0.3333,
      accuracy_drop: 0.5,
      interpretation: "bit_length_confound",
    },
    {
      pair_key: "limit=50000;train=40;test=20",
      limit: 50000,
      train_count: 40,
      test_count: 20,
      profile: "gap_only",
      uncontrolled_accuracy: 0.6667,
      controlled_accuracy: 0.5,
      accuracy_drop: 0.1667,
      interpretation: "inconclusive",
    },
  ],
  summary: {
    profiles: {
      all: {
        mean_uncontrolled_accuracy: 0.8333,
        mean_controlled_accuracy: 0.5,
        mean_accuracy_drop: 0.3333,
        accuracy_drop: { mean: 0.3333, ci95_low: -0.05, ci95_high: 0.72 },
        controlled_significance: { p_value: 0.12, label: "not_significant" },
        robust_interpretation: "inconclusive",
        interpretations: { inconclusive: 1 },
      },
      bit_length_only: {
        mean_uncontrolled_accuracy: 0.8333,
        mean_controlled_accuracy: 0.3333,
        mean_accuracy_drop: 0.5,
        accuracy_drop: { mean: 0.5, ci95_low: -0.02, ci95_high: 1.0 },
        controlled_significance: { p_value: 0.52, label: "not_significant" },
        robust_interpretation: "inconclusive",
        interpretations: { bit_length_confound: 1 },
      },
      gap_only: {
        mean_uncontrolled_accuracy: 0.6667,
        mean_controlled_accuracy: 0.5,
        mean_accuracy_drop: 0.1667,
        accuracy_drop: { mean: 0.1667, ci95_low: -0.21, ci95_high: 0.55 },
        controlled_significance: { p_value: 0.12, label: "not_significant" },
        robust_interpretation: "inconclusive",
        interpretations: { inconclusive: 1 },
      },
    },
    most_confound_sensitive_profiles: [],
  },
};

const bundledRealBaselineManifest = {
  schema: "primeproject.real-world-baseline-manifest.v1",
  entry_count: 5,
  status_counts: { planned: 4, available: 1 },
  entries: [
    {
      baseline_id: "openssl-rsa-prime-owned",
      library: "OpenSSL",
      object_type: "rsa-prime",
      status: "planned",
      sample_count: 0,
      sensitive: true,
    },
    {
      baseline_id: "boringssl-rsa-prime-owned",
      library: "BoringSSL",
      object_type: "rsa-prime",
      status: "planned",
      sample_count: 0,
      sensitive: true,
    },
    {
      baseline_id: "go-crypto-rsa-prime-owned",
      library: "Go crypto/rsa",
      object_type: "rsa-prime",
      status: "planned",
      sample_count: 0,
      sensitive: true,
    },
    {
      baseline_id: "bitcoin-core-ecdsa-signature-public",
      library: "Bitcoin Core / secp256k1 ecosystem",
      object_type: "ecdsa-signature",
      status: "planned",
      sample_count: 0,
      sensitive: false,
    },
    {
      baseline_id: "bitcoin-secp256k1-constants",
      library: "Bitcoin secp256k1",
      object_type: "ecc-field-prime",
      status: "available",
      sample_count: 2,
      sensitive: false,
    },
  ],
};

const bundledCollectionMatrix = {
  schema: "primeproject.real-world-collection-matrix.v1",
  sample_handling: {
    raw_private_material_public: false,
    aggregate_fingerprints_public: true,
    minimum_replicates_per_label: 3,
    publication_unit: "aggregate fingerprint, baseline JSON, and feature vector only",
  },
  row_count: 4,
  target_count: 10,
  complete_target_count: 0,
  blocked_target_count: 10,
  local_sensitive_count: 3,
  completion_ratio: 0,
  claim_gate: {
    status: "blocked",
    available_rsa_libraries: 0,
    minimum_available_rsa_libraries: 2,
    minimum_label_replicates: 3,
    message:
      "Real-world attribution remains blocked until at least two aggregate RSA library baselines and labelled classifier replicates exist.",
  },
  rows: [
    { library: "OpenSSL", track: "rsa-prime-generation", sensitive: true, targets: [{ bit_length: 2048, sample_target: 500, status: "planned" }, { bit_length: 3072, sample_target: 500, status: "planned" }, { bit_length: 4096, sample_target: 500, status: "planned" }] },
    { library: "BoringSSL", track: "rsa-prime-generation", sensitive: true, targets: [{ bit_length: 2048, sample_target: 500, status: "planned" }, { bit_length: 3072, sample_target: 500, status: "planned" }, { bit_length: 4096, sample_target: 500, status: "planned" }] },
    { library: "Go crypto/rsa", track: "rsa-prime-generation", sensitive: true, targets: [{ bit_length: 2048, sample_target: 500, status: "planned" }, { bit_length: 3072, sample_target: 500, status: "planned" }, { bit_length: 4096, sample_target: 500, status: "planned" }] },
    { library: "Bitcoin Core / wallet metadata", track: "signature-nonce-metadata", sensitive: false, targets: [{ bit_length: 256, sample_target: 10000, status: "planned" }] },
  ],
};

const bundledCollectionPower = {
  schema: "primeproject.collection-power.v1",
  method: {
    name: "multinomial screening floor",
    alpha: 0.05,
    target_tv: 0.1,
    modulo: 210,
    interpretation:
      "This is a conservative planning heuristic for aggregate fingerprints, not a proof of generator attribution.",
  },
  summary: {
    target_count: 10,
    coarse_count: 9,
    screening_count: 0,
    strong_count: 1,
    minimum_recommended_replicates: 3,
    weakest_targets: [
      { library: "OpenSSL", bit_length: 2048, sample_target: 500, conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
      { library: "OpenSSL", bit_length: 3072, sample_target: 500, conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
      { library: "OpenSSL", bit_length: 4096, sample_target: 500, conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    ],
  },
  rows: [
    { library: "OpenSSL", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "OpenSSL", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "OpenSSL", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", conservative_tv_floor_95: 0.300457, min_samples_for_10pct_tv: 4514 },
    { library: "Bitcoin Core / wallet metadata", bit_length: 256, sample_target: 10000, object_type: "ecdsa-signature", power_tier: "strong", conservative_tv_floor_95: 0.077784, min_samples_for_10pct_tv: 6051 },
  ],
  recommendations: [
    {
      priority: "P0",
      track: "rsa-prime-generation",
      action:
        "Treat 500 RSA primes per bit length as coarse screening; target about 4514 primes per library/bit-length for conservative 10% TV drift claims.",
    },
  ],
};

const bundledProvenanceRequirements = {
  schema: "primeproject.provenance-requirements.v1",
  required_fields: [
    "baseline_id",
    "library",
    "library_version",
    "algorithm",
    "object_type",
    "bit_length",
    "sample_count",
    "collector",
    "collection_date",
    "host_platform",
    "source_commit",
    "build_config",
    "rng_source",
    "generation_command",
    "raw_material_policy",
    "aggregate_artifact_sha256",
  ],
  forbidden_public_fields: ["private_key", "private_prime", "wallet_seed", "raw_signature_owner"],
  row_count: 4,
  missing_required_count: 35,
  public_safety: {
    raw_private_material_public: false,
    aggregate_artifacts_public: true,
    review_required_before_status_available: true,
  },
  claim_gate: {
    status: "blocked",
    message: "Real-world baselines need complete provenance before being used for attribution claims.",
  },
  rows: [
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", missing_required_count: 9, completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"] },
    { baseline_id: "boringssl-rsa-prime-owned", library: "BoringSSL", object_type: "rsa-prime", missing_required_count: 9, completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"] },
    { baseline_id: "go-crypto-rsa-prime-owned", library: "Go crypto/rsa", object_type: "rsa-prime", missing_required_count: 9, completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"] },
    { baseline_id: "bitcoin-core-ecdsa-signature-public", library: "Bitcoin Core / secp256k1 ecosystem", object_type: "ecdsa-signature", missing_required_count: 8, completion_ratio: 0.5, missing_required_fields: ["collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"] },
  ],
};

const bundledProvenanceAudit = {
  schema: "primeproject.provenance-audit.v1",
  requirements_schema: "primeproject.provenance-requirements.v1",
  row_count: 4,
  pass_count: 0,
  blocked_count: 4,
  summary: {
    total_missing_required: 35,
    forbidden_public_field_count: 0,
    invalid_field_count: 0,
    public_safe: true,
  },
  claim_gate: {
    status: "blocked",
    message: "Attribution claims stay blocked until provenance records are complete and public-safe.",
  },
  rows: [
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", status: "blocked", completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"], forbidden_public_fields: [], invalid_fields: [] },
    { baseline_id: "boringssl-rsa-prime-owned", library: "BoringSSL", object_type: "rsa-prime", status: "blocked", completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"], forbidden_public_fields: [], invalid_fields: [] },
    { baseline_id: "go-crypto-rsa-prime-owned", library: "Go crypto/rsa", object_type: "rsa-prime", status: "blocked", completion_ratio: 0.4375, missing_required_fields: ["bit_length", "collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"], forbidden_public_fields: [], invalid_fields: [] },
    { baseline_id: "bitcoin-core-ecdsa-signature-public", library: "Bitcoin Core / secp256k1 ecosystem", object_type: "ecdsa-signature", status: "blocked", completion_ratio: 0.5, missing_required_fields: ["collector", "collection_date", "host_platform", "source_commit", "build_config", "rng_source", "generation_command", "aggregate_artifact_sha256"], forbidden_public_fields: [], invalid_fields: [] },
  ],
};

const bundledResearchReadiness = {
  schema: "primeproject.research-readiness.v1",
  overall: { score: 0.5869, label: "prototype_ready" },
  dimensions: {
    sim_to_real: {
      score: 0.8125,
      label: "research_ready",
      registered_count: 5,
      available_count: 1,
      planned_count: 4,
      sensitive_count: 3,
      gaps: [{ code: "insufficient_available_real_baselines", severity: "high" }],
    },
    attribution_validation: {
      score: 1,
      label: "research_ready",
      rows: 48,
      repeats: 3,
      robust_profiles: ["all", "gap_only"],
      gaps: [],
    },
    classifier: {
      score: 0,
      label: "not_started",
      vector_count: 0,
      label_count: 0,
      gaps: [{ code: "missing_classifier_report", severity: "high" }],
    },
    bitcoin_integration: {
      score: 0.35,
      label: "scaffold_ready",
      related_baseline_count: 1,
      gaps: [{ code: "missing_bitcoin_risk_report", severity: "medium" }],
    },
  },
  blocking_gaps: [
    { dimension: "sim_to_real", code: "insufficient_available_real_baselines", severity: "high" },
    { dimension: "classifier", code: "missing_classifier_report", severity: "high" },
  ],
  next_actions: [
    {
      priority: "P0",
      track: "sim-to-real",
      action: "Generate at least two local owned-library aggregate baselines with matched bit-length and sample counts.",
    },
    {
      priority: "P0",
      track: "classifier",
      action: "Export labelled feature vectors for OpenSSL, BoringSSL, Go, and a suspicious sample before trusting classifier output.",
    },
    {
      priority: "P1",
      track: "bitcoin",
      action: "Bundle a Bitcoin risk report from owned or public metadata summaries and compare it with registered baselines.",
    },
  ],
};

const bundledEvidencePack = {
  schema: "primeproject.evidence-pack.v1",
  claim_level: {
    level: "public_demo_only",
    statement: "Safe to publish as a research scaffold, not as real-world attribution evidence.",
    failed_gate_count: 3,
    failed_high_gate_count: 2,
  },
  publication_gates: [
    { code: "sensitive_publication_gate", passed: true, severity: "critical" },
    { code: "real_baseline_gate", passed: false, severity: "high" },
    { code: "controlled_signal_gate", passed: true, severity: "high" },
    { code: "classifier_gate", passed: false, severity: "high" },
    { code: "bitcoin_integration_gate", passed: false, severity: "medium" },
    { code: "reproducibility_gate", passed: true, severity: "medium" },
    { code: "provenance_gate", passed: true, severity: "medium" },
    { code: "provenance_audit_gate", passed: true, severity: "medium" },
  ],
  artifact_count: 9,
  artifacts: [
    { role: "attribution_grid", schema: "primeproject.attribution-confound-grid.v1", sha256: "4873f01f4deec22f70c3a98563cd37e0ccbb587313e4d70befebff30e3f12318" },
    { role: "collection_matrix", schema: "primeproject.real-world-collection-matrix.v1", sha256: "703703591cbfb4ca35f3c5dcb350043e75c698a8df750fb7a77c500bc4fc6f92" },
    { role: "collection_power", schema: "primeproject.collection-power.v1", sha256: "2093411a402d68d3df0e16591369a0b63816780a0bc6a460c7a38437d102540b" },
    { role: "manifest", schema: "primeproject.real-world-baseline-manifest.v1", sha256: "fb55fabb2ddf378a3f2a7065cee7bf1d5db1b1eda7ca5c659fddc9e0e037b2c7" },
    { role: "project_evolution", schema: "primeproject.project-evolution.v1", sha256: "c45981c6bc09c0fb7ffa49a5a224207d7a25bddb55cde65bf8e9ba35bf366803" },
    { role: "provenance_audit", schema: "primeproject.provenance-audit.v1", sha256: "3862c5032dc3caed31ef7a2aa9b491e109bdbd846e9e485ea50e7f68784813dd" },
    { role: "provenance_requirements", schema: "primeproject.provenance-requirements.v1", sha256: "e08ad1eac816bbbd725abeab1702ae0b03b7af2281bf5b0581e5e0c7aa8642e0" },
    { role: "readiness", schema: "primeproject.research-readiness.v1", sha256: "1cbc7b7e045128afe264c71ee5b14c3fa2e780cf5cf93fd93155e11ed29f83dc" },
    { role: "snapshot_manifest", schema: "primeproject.snapshot-manifest.v1", sha256: "ff9fea32962c21607de547e13d6385b0a0d9d13efa08c8df25b0e72806be84e0" },
  ],
};

const bundledProjectEvolution = {
  schema: "primeproject.project-evolution.v1",
  headline: "From prime regularity exploration to generator-fingerprint research tooling.",
  metrics: {
    live_compute_limit: 10000000,
    precomputed_snapshot_limits: [1000000, 10000000],
    registered_real_baselines: 5,
    available_real_baselines: 1,
    collection_targets: 10,
    collection_complete_targets: 0,
    collection_power_strong_targets: 1,
    collection_power_coarse_targets: 9,
    provenance_rows: 4,
    provenance_missing_required: 35,
    provenance_audit_blocked_rows: 4,
    provenance_audit_forbidden_fields: 0,
    attribution_grid_rows: 48,
    attribution_repeats: 3,
    robust_controlled_profiles: ["all", "gap_only"],
    publication_claim_level: "public_demo_only",
    checksummed_artifacts: 9,
    blocking_gaps: 2,
  },
  phases: [
    { id: "regularity-plan", label: "Prime regularity plan", status: "complete", layer: "theory" },
    { id: "conjecture-lab", label: "Interactive Conjecture Lab", status: "complete", layer: "visualization" },
    { id: "static-snapshots", label: "10M research snapshots", status: "complete", layer: "evidence" },
    { id: "bitcoin-track", label: "Bitcoin defensive track", status: "complete", layer: "crypto" },
    { id: "fingerprint-baseline", label: "Generator fingerprint baseline", status: "complete", layer: "analysis" },
    { id: "attribution-grid", label: "Controlled attribution grid", status: "complete", layer: "validation" },
    { id: "real-world-registry", label: "Real-world baseline registry", status: "scaffolded", layer: "sim-to-real" },
    { id: "collection-matrix", label: "Real-world collection matrix", status: "active", layer: "sim-to-real" },
    { id: "collection-power", label: "Sample power calibration", status: "active", layer: "statistics" },
    { id: "provenance-gate", label: "Provenance requirements", status: "active", layer: "governance" },
    { id: "provenance-audit", label: "Provenance audit", status: "active", layer: "governance" },
    { id: "readiness-gates", label: "Research readiness scoring", status: "active", layer: "governance" },
    { id: "evidence-pack", label: "Evidence pack gates", status: "active", layer: "publication" },
  ],
  connections: [
    ["regularity-plan", "conjecture-lab"],
    ["conjecture-lab", "static-snapshots"],
    ["conjecture-lab", "fingerprint-baseline"],
    ["bitcoin-track", "real-world-registry"],
    ["fingerprint-baseline", "attribution-grid"],
    ["attribution-grid", "readiness-gates"],
    ["real-world-registry", "collection-matrix"],
    ["collection-matrix", "collection-power"],
    ["collection-power", "provenance-gate"],
    ["provenance-gate", "provenance-audit"],
    ["provenance-audit", "readiness-gates"],
    ["readiness-gates", "evidence-pack"],
  ],
  open_gaps: [
    { priority: "P0", track: "sim-to-real", gap: "Need at least two available real-world aggregate baselines before real attribution claims." },
    { priority: "P0", track: "classifier", gap: "Need labelled feature vectors across OpenSSL, BoringSSL, Go, and suspicious samples." },
    { priority: "P1", track: "bitcoin", gap: "Need a bundled Bitcoin nonce-risk report from owned or public metadata summaries." },
  ],
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
  predictionStart: document.querySelector("#predictionStart"),
  predictionSpan: document.querySelector("#predictionSpan"),
  runPrediction: document.querySelector("#runPrediction"),
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
  predictionMetrics: document.querySelector("#predictionMetrics"),
  predictionRows: document.querySelector("#predictionRows"),
  snapshotButtons: document.querySelector("#snapshotButtons"),
  snapshotSummary: document.querySelector("#snapshotSummary"),
  snapshotOverview: document.querySelector("#snapshotOverview"),
  snapshotGapDistribution: document.querySelector("#snapshotGapDistribution"),
  snapshotResidueDrift: document.querySelector("#snapshotResidueDrift"),
  evolutionSummary: document.querySelector("#evolutionSummary"),
  evolutionMap: document.querySelector("#evolutionMap"),
  evolutionTimeline: document.querySelector("#evolutionTimeline"),
  evolutionGaps: document.querySelector("#evolutionGaps"),
  baselineRegistrySummary: document.querySelector("#baselineRegistrySummary"),
  baselineRegistryRows: document.querySelector("#baselineRegistryRows"),
  collectionMatrixStatus: document.querySelector("#collectionMatrixStatus"),
  collectionMatrixRows: document.querySelector("#collectionMatrixRows"),
  collectionPowerStatus: document.querySelector("#collectionPowerStatus"),
  collectionPowerSummary: document.querySelector("#collectionPowerSummary"),
  collectionPowerRows: document.querySelector("#collectionPowerRows"),
  provenanceStatus: document.querySelector("#provenanceStatus"),
  provenanceSummary: document.querySelector("#provenanceSummary"),
  provenanceRows: document.querySelector("#provenanceRows"),
  provenanceAuditStatus: document.querySelector("#provenanceAuditStatus"),
  provenanceAuditSummary: document.querySelector("#provenanceAuditSummary"),
  provenanceAuditRows: document.querySelector("#provenanceAuditRows"),
  readinessSummary: document.querySelector("#readinessSummary"),
  readinessDimensions: document.querySelector("#readinessDimensions"),
  readinessActions: document.querySelector("#readinessActions"),
  evidenceSummary: document.querySelector("#evidenceSummary"),
  evidenceGateRows: document.querySelector("#evidenceGateRows"),
  evidenceArtifactRows: document.querySelector("#evidenceArtifactRows"),
  attributionSummary: document.querySelector("#attributionSummary"),
  attributionGridSvg: document.querySelector("#attributionGridSvg"),
  attributionProfileRows: document.querySelector("#attributionProfileRows"),
};

controls.limitRange.value = limitToSlider(state.limit);
controls.limitValue.textContent = formatNumber(state.limit);

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
    const target = document.querySelector(`#${button.dataset.scrollTarget}`);
    if (!target) return;
    scrollToPanel(target);
  });
});

controls.limitRange.addEventListener("input", () => {
  state.limit = sliderToLimit(Number(controls.limitRange.value));
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

controls.runPrediction.addEventListener("click", renderPrediction);

controls.runExperiment.addEventListener("click", runExperiment);

window.addEventListener("resize", () => {
  window.requestAnimationFrame(render);
});

runExperiment();
loadSnapshots();
loadProjectEvolution();
loadRealBaselineManifest();
loadCollectionMatrix();
loadCollectionPower();
loadProvenanceRequirements();
loadProvenanceAudit();
loadResearchReadiness();
loadEvidencePack();
loadAttributionGrid();
renderPrediction();

function scrollToPanel(target) {
  const topbarOffset = document.querySelector(".topbar")?.getBoundingClientRect().height || 0;
  const targetTop = target.getBoundingClientRect().top + window.pageYOffset - topbarOffset - 12;
  window.scrollTo({
    top: Math.max(0, targetTop),
    left: 0,
    behavior: "auto",
  });
}

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
    maxWeightShare: maxOf(weights) / totalWeight,
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
  const maxPrime = primes.at(-1) || 2;
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
  const maxGap = maxBy(state.lab.observations, (observation) => observation.gap);
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
  const maxGap = maxBy(observations, (observation) => observation.gap);
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
  const maxGap = maxBy(observations, (observation) => observation.gap);
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

function renderPrediction() {
  if (!outputs.predictionMetrics || !outputs.predictionRows) return;
  const start = Math.max(10, Number(controls.predictionStart.value) || 100000);
  const span = Math.max(40, Math.min(5000, Number(controls.predictionSpan.value) || 640));
  controls.predictionStart.value = start;
  controls.predictionSpan.value = span;
  const result = scoreNextPrimeCandidates(start, span, 210, 12);
  outputs.predictionMetrics.innerHTML = `
    <div><span>Observed next</span><strong>${formatNumber(result.actualNextPrime)}</strong></div>
    <div><span>Observed offset</span><strong>+${formatNumber(result.actualOffset)}</strong></div>
    <div><span>Observed rank</span><strong>#${result.rankOfActual || `>${result.topCandidates.length}`}</strong></div>
    <div><span>Candidates scored</span><strong>${formatNumber(result.candidatesScored)}</strong></div>
  `;
  outputs.predictionRows.innerHTML = result.topCandidates
    .map(
      (candidate, index) => `<tr class="${candidate.isPrime ? "is-prime" : ""}">
        <td>#${index + 1}</td>
        <td>${formatNumber(candidate.candidate)}</td>
        <td>+${formatNumber(candidate.offset)}</td>
        <td>${candidate.score.toFixed(5)}</td>
        <td>${candidate.candidate % result.modulo}</td>
        <td>${candidate.candidate === result.actualNextPrime ? "next prime" : candidate.isPrime ? "prime" : "composite"}</td>
      </tr>`,
    )
    .join("");
}

function scoreNextPrimeCandidates(start, span, modulo, top) {
  const end = start + span;
  const primes = sievePrimes(end);
  const primeSet = new Set(primes);
  const actualNextPrime = primes.find((prime) => prime > start) || null;
  const residueFactors = buildPredictionResidueFactors(primes, modulo);
  const residues = residueClasses(modulo);
  const wheelFactor = modulo / residues.length;
  const expectedGap = Math.max(2, Math.log(Math.max(start, 3)));
  const candidates = [];
  for (let candidate = start + 1; candidate <= end; candidate += 1) {
    if (candidate > 2 && candidate % 2 === 0) continue;
    if (candidate !== 2 && gcd(candidate, modulo) !== 1) continue;
    const offset = candidate - start;
    const baseDensity = 1 / Math.log(Math.max(candidate, 3));
    const residueFactor = residueFactors.get(candidate % modulo) || 1;
    const gapSurvival = Math.exp(-offset / expectedGap);
    const score = baseDensity * wheelFactor * residueFactor * gapSurvival;
    candidates.push({
      candidate,
      offset,
      score,
      baseDensity,
      wheelFactor,
      residueFactor,
      gapSurvival,
      isPrime: primeSet.has(candidate),
    });
  }
  const ranked = candidates.sort((a, b) => b.score - a.score);
  const actualIndex =
    actualNextPrime === null ? -1 : ranked.findIndex((candidate) => candidate.candidate === actualNextPrime);
  return {
    start,
    span,
    modulo,
    actualNextPrime,
    actualOffset: actualNextPrime === null ? null : actualNextPrime - start,
    rankOfActual: actualIndex >= 0 ? actualIndex + 1 : null,
    candidatesScored: ranked.length,
    topCandidates: ranked.slice(0, top),
  };
}

function buildPredictionResidueFactors(primes, modulo) {
  const residues = residueClasses(modulo);
  const totals = new Map(residues.map((residue) => [residue, 0]));
  let totalWeight = 0;
  for (let index = 1; index < primes.length; index += 1) {
    const prime = primes[index];
    const gap = prime - primes[index - 1];
    const residue = prime % modulo;
    if (!totals.has(residue)) continue;
    totals.set(residue, totals.get(residue) + gap);
    totalWeight += gap;
  }
  const uniform = 1 / residues.length;
  const factors = new Map();
  residues.forEach((residue) => {
    const mass = totalWeight > 0 ? totals.get(residue) / totalWeight : uniform;
    factors.set(residue, Math.max(0.2, Math.min(5, mass / uniform)));
  });
  return factors;
}

async function loadSnapshots() {
  try {
    if (window.location.protocol === "file:") {
      state.snapshots = bundledSnapshots;
    } else {
      const response = await fetch("data/snapshots/manifest.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`snapshot manifest ${response.status}`);
      const manifest = await response.json();
      state.snapshots = Array.isArray(manifest.snapshots) ? manifest.snapshots : bundledSnapshots;
    }
  } catch (error) {
    state.snapshots = bundledSnapshots;
  }
  renderSnapshots();
}

function renderSnapshots() {
  if (!outputs.snapshotButtons || !outputs.snapshotSummary) return;
  if (state.snapshots.length === 0) {
    outputs.snapshotSummary.textContent = "No precomputed snapshots are bundled.";
    return;
  }
  outputs.snapshotButtons.innerHTML = state.snapshots
    .map(
      (snapshot, index) =>
        `<button type="button" class="${index === state.activeSnapshot ? "is-active" : ""}" data-snapshot-index="${index}">${snapshot.label}</button>`,
    )
    .join("");
  outputs.snapshotButtons.querySelectorAll("[data-snapshot-index]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeSnapshot = Number(button.dataset.snapshotIndex);
      renderSnapshots();
    });
  });

  const snapshot = state.snapshots[state.activeSnapshot] || state.snapshots[0];
  outputs.snapshotSummary.innerHTML = `
    <div><span>Limit</span><strong>${formatCompact(snapshot.limit)}</strong></div>
    <div><span>Primes</span><strong>${formatNumber(snapshot.prime_count)}</strong></div>
    <div><span>Modulo</span><strong>${snapshot.modulo}</strong></div>
    <div><span>Mean gap</span><strong>${snapshot.mean_gap.toFixed(2)}</strong></div>
    <div><span>Max gap</span><strong>${snapshot.max_gap}</strong></div>
  `;
  setSnapshotImage(outputs.snapshotOverview, snapshot.overview_svg, `${snapshot.label} overview snapshot`);
  setSnapshotImage(
    outputs.snapshotGapDistribution,
    snapshot.gap_distribution_svg,
    `${snapshot.label} gap distribution snapshot`,
  );
  setSnapshotImage(outputs.snapshotResidueDrift, snapshot.residue_drift_svg, `${snapshot.label} residue drift snapshot`);
}

async function loadProjectEvolution() {
  try {
    if (window.location.protocol === "file:") {
      state.projectEvolution = bundledProjectEvolution;
    } else {
      const response = await fetch("data/project_evolution.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`project evolution ${response.status}`);
      state.projectEvolution = await response.json();
    }
  } catch (error) {
    state.projectEvolution = bundledProjectEvolution;
  }
  renderProjectEvolution();
}

function renderProjectEvolution() {
  if (!outputs.evolutionSummary || !outputs.evolutionMap || !outputs.evolutionTimeline || !outputs.evolutionGaps) return;
  const evolution = state.projectEvolution || bundledProjectEvolution;
  const metrics = evolution.metrics || {};
  const phases = evolution.phases || [];
  outputs.evolutionSummary.innerHTML = `
    <div><span>Live compute</span><strong>${formatCompact(metrics.live_compute_limit || 0)}</strong><small>browser limit</small></div>
    <div><span>Snapshots</span><strong>${formatNumber((metrics.precomputed_snapshot_limits || []).length)}</strong><small>${(metrics.precomputed_snapshot_limits || []).map(formatCompact).join(", ")}</small></div>
    <div><span>Baselines</span><strong>${formatNumber(metrics.registered_real_baselines || 0)}</strong><small>${formatNumber(metrics.available_real_baselines || 0)} available</small></div>
    <div><span>Collection targets</span><strong>${formatNumber(metrics.collection_targets || 0)}</strong><small>${formatNumber(metrics.collection_complete_targets || 0)} complete</small></div>
    <div><span>Power floor</span><strong>${formatNumber(metrics.collection_power_strong_targets || 0)}</strong><small>${formatNumber(metrics.collection_power_coarse_targets || 0)} coarse</small></div>
    <div><span>Provenance</span><strong>${formatNumber(metrics.provenance_rows || 0)}</strong><small>${formatNumber(metrics.provenance_missing_required || 0)} missing</small></div>
    <div><span>Audit block</span><strong>${formatNumber(metrics.provenance_audit_blocked_rows || 0)}</strong><small>${formatNumber(metrics.provenance_audit_forbidden_fields || 0)} forbidden fields</small></div>
    <div><span>Attribution rows</span><strong>${formatNumber(metrics.attribution_grid_rows || 0)}</strong><small>${formatNumber(metrics.attribution_repeats || 0)} repeats</small></div>
    <div><span>Claim level</span><strong>${escapeHtml(metrics.publication_claim_level || "unknown")}</strong><small>${formatNumber(metrics.blocking_gaps || 0)} blocking gaps</small></div>
  `;
  renderEvolutionMap(evolution);
  outputs.evolutionTimeline.innerHTML = phases
    .map((phase, index) => `
      <div class="evolution-step">
        <i>${String(index + 1).padStart(2, "0")}</i>
        <strong>${escapeHtml(phase.label || phase.id)}</strong>
        <em class="${phase.status === "complete" ? "is-complete" : "is-active"}">${escapeHtml(phase.status || "planned")}</em>
        <span>${escapeHtml(phase.summary || phase.layer || "")}</span>
      </div>
    `)
    .join("");
  outputs.evolutionGaps.innerHTML = (evolution.open_gaps || [])
    .map((gap) => `
      <div>
        <strong>${escapeHtml(gap.priority || "P?")} ${escapeHtml(gap.track || "research")}</strong>
        <span>${escapeHtml(gap.gap || "")}</span>
      </div>
    `)
    .join("");
}

function renderEvolutionMap(evolution) {
  const svg = outputs.evolutionMap;
  const width = 1060;
  const height = 360;
  const phases = evolution.phases || [];
  const columns = [
    ["regularity-plan", "bitcoin-track"],
    ["conjecture-lab"],
    ["static-snapshots", "fingerprint-baseline"],
    ["attribution-grid", "real-world-registry"],
    ["collection-matrix", "collection-power"],
    ["provenance-gate", "provenance-audit", "readiness-gates"],
    ["evidence-pack"],
  ];
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  const positions = new Map();
  const left = 32;
  const top = 52;
  const columnGap = 145;
  const rowGap = 92;
  columns.forEach((column, columnIndex) => {
    const yOffset = column.length === 1 ? rowGap / 2 : 0;
    column.forEach((id, rowIndex) => {
      positions.set(id, {
        x: left + columnIndex * columnGap,
        y: top + yOffset + rowIndex * rowGap,
      });
    });
  });
  svg.innerHTML = "";
  appendSvg(svg, "text", { x: 44, y: 26, class: "chart-title" }).textContent =
    "research stack evolution";
  (evolution.connections || []).forEach(([from, to]) => {
    const start = positions.get(from);
    const end = positions.get(to);
    if (!start || !end) return;
    const x1 = start.x + 112;
    const y1 = start.y + 22;
    const x2 = end.x - 8;
    const y2 = end.y + 22;
    appendSvg(svg, "path", {
      d: `M ${x1} ${y1} C ${x1 + 42} ${y1}, ${x2 - 42} ${y2}, ${x2} ${y2}`,
      fill: "none",
      stroke: "#c6ccd8",
      "stroke-width": 2,
    });
  });
  phases.forEach((phase) => {
    const point = positions.get(phase.id);
    if (!point) return;
    const color = phase.status === "complete" ? colors.teal : phase.status === "active" ? colors.indigo : colors.amber;
    appendSvg(svg, "rect", {
      x: point.x,
      y: point.y,
      width: 124,
      height: 58,
      rx: 8,
      fill: "#ffffff",
      stroke: color,
      "stroke-width": 2,
    });
    appendSvg(svg, "circle", { cx: point.x + 16, cy: point.y + 17, r: 5, fill: color });
    appendSvg(svg, "text", { x: point.x + 28, y: point.y + 20, class: "evolution-node-layer" }).textContent =
      phase.layer || "";
    wrapSvgText(svg, phase.label || phase.id, point.x + 14, point.y + 39, 100, 2);
  });
}

async function loadRealBaselineManifest() {
  try {
    if (window.location.protocol === "file:") {
      state.realBaselineManifest = bundledRealBaselineManifest;
    } else {
      const response = await fetch("data/baselines/real_world/manifest.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`real baseline manifest ${response.status}`);
      state.realBaselineManifest = await response.json();
    }
  } catch (error) {
    state.realBaselineManifest = bundledRealBaselineManifest;
  }
  renderRealBaselineManifest();
}

function renderRealBaselineManifest() {
  if (!outputs.baselineRegistrySummary || !outputs.baselineRegistryRows) return;
  const manifest = state.realBaselineManifest || bundledRealBaselineManifest;
  const entries = manifest.entries || [];
  const counts = manifest.status_counts || {};
  const sensitiveCount = entries.filter((entry) => entry.sensitive).length;
  outputs.baselineRegistrySummary.innerHTML = `
    <div><span>Registered</span><strong>${formatNumber(entries.length)}</strong></div>
    <div><span>Available</span><strong>${formatNumber(counts.available || 0)}</strong></div>
    <div><span>Planned</span><strong>${formatNumber(counts.planned || 0)}</strong></div>
    <div><span>Local-sensitive</span><strong>${formatNumber(sensitiveCount)}</strong></div>
  `;
  outputs.baselineRegistryRows.innerHTML = entries
    .map((entry) => {
      const handling = entry.sensitive ? "local aggregate only" : "public summary";
      const statusClass = entry.status === "available" ? "is-available" : "is-planned";
      return `
        <tr>
          <td><strong>${escapeHtml(entry.library || entry.baseline_id || "unknown")}</strong><span>${escapeHtml(entry.baseline_id || "")}</span></td>
          <td>${escapeHtml(entry.object_type || "unknown")}</td>
          <td><em class="${statusClass}">${escapeHtml(entry.status || "planned")}</em></td>
          <td>${formatNumber(entry.sample_count || 0)}</td>
          <td>${handling}</td>
        </tr>
      `;
    })
    .join("");
}

async function loadCollectionMatrix() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionMatrix = bundledCollectionMatrix;
    } else {
      const response = await fetch("data/collection_matrix.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection matrix ${response.status}`);
      state.collectionMatrix = await response.json();
    }
  } catch (error) {
    state.collectionMatrix = bundledCollectionMatrix;
  }
  renderCollectionMatrix();
}

async function loadCollectionPower() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionPower = bundledCollectionPower;
    } else {
      const response = await fetch("data/collection_power.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection power ${response.status}`);
      state.collectionPower = await response.json();
    }
  } catch (error) {
    state.collectionPower = bundledCollectionPower;
  }
  renderCollectionPower();
}

function renderCollectionPower() {
  if (!outputs.collectionPowerStatus || !outputs.collectionPowerSummary || !outputs.collectionPowerRows) return;
  const power = state.collectionPower || bundledCollectionPower;
  const summary = power.summary || {};
  const rows = power.rows || [];
  outputs.collectionPowerStatus.textContent =
    `${formatNumber(summary.strong_count || 0)} strong · ${formatNumber(summary.coarse_count || 0)} coarse`;
  outputs.collectionPowerSummary.innerHTML = `
    <div><span>Method</span><strong>${escapeHtml(power.method?.name || "unknown")}</strong><small>${formatPercent(power.method?.target_tv || 0)} TV target</small></div>
    <div><span>Targets</span><strong>${formatNumber(summary.target_count || rows.length)}</strong><small>${formatNumber(summary.minimum_recommended_replicates || 0)} replicates</small></div>
    <div><span>Strong</span><strong>${formatNumber(summary.strong_count || 0)}</strong><small>claim-ready floor</small></div>
    <div><span>Coarse</span><strong>${formatNumber(summary.coarse_count || 0)}</strong><small>screening only</small></div>
  `;
  outputs.collectionPowerRows.innerHTML = rows
    .slice()
    .sort((a, b) => b.conservative_tv_floor_95 - a.conservative_tv_floor_95)
    .slice(0, 5)
    .map((row) => `
      <div class="power-row">
        <strong>${escapeHtml(row.library || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
        <em class="is-${escapeHtml(row.power_tier || "coarse")}">${escapeHtml(row.power_tier || "coarse")}</em>
        <span>95% TV floor ${formatPercent(row.conservative_tv_floor_95 || 0)}</span>
        <span>10% TV n≈${formatNumber(row.min_samples_for_10pct_tv || 0)}</span>
      </div>
    `)
    .join("");
}

async function loadProvenanceRequirements() {
  try {
    if (window.location.protocol === "file:") {
      state.provenanceRequirements = bundledProvenanceRequirements;
    } else {
      const response = await fetch("data/provenance_requirements.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`provenance requirements ${response.status}`);
      state.provenanceRequirements = await response.json();
    }
  } catch (error) {
    state.provenanceRequirements = bundledProvenanceRequirements;
  }
  renderProvenanceRequirements();
}

function renderProvenanceRequirements() {
  if (!outputs.provenanceStatus || !outputs.provenanceSummary || !outputs.provenanceRows) return;
  const provenance = state.provenanceRequirements || bundledProvenanceRequirements;
  const gate = provenance.claim_gate || {};
  const rows = provenance.rows || [];
  outputs.provenanceStatus.textContent =
    `${formatNumber(provenance.missing_required_count || 0)} fields missing · ${escapeHtml(gate.status || "unknown")}`;
  outputs.provenanceSummary.innerHTML = `
    <div><span>Rows</span><strong>${formatNumber(provenance.row_count || rows.length)}</strong><small>non-standard baselines</small></div>
    <div><span>Required fields</span><strong>${formatNumber((provenance.required_fields || []).length)}</strong><small>per template</small></div>
    <div><span>Missing</span><strong>${formatNumber(provenance.missing_required_count || 0)}</strong><small>before collection</small></div>
    <div><span>Public safety</span><strong>${provenance.public_safety?.raw_private_material_public ? "fail" : "pass"}</strong><small>aggregate only</small></div>
  `;
  outputs.provenanceRows.innerHTML = rows
    .slice()
    .sort((a, b) => b.missing_required_count - a.missing_required_count)
    .map((row) => `
      <div class="provenance-row">
        <strong>${escapeHtml(row.library || row.baseline_id || "unknown")}</strong>
        <span>${formatPercent(row.completion_ratio || 0)} complete</span>
        <em>${formatNumber(row.missing_required_count || 0)} missing</em>
        <code>${escapeHtml((row.missing_required_fields || []).slice(0, 3).join(", ") || "complete")}</code>
      </div>
    `)
    .join("");
}

async function loadProvenanceAudit() {
  try {
    if (window.location.protocol === "file:") {
      state.provenanceAudit = bundledProvenanceAudit;
    } else {
      const response = await fetch("data/provenance_audit.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`provenance audit ${response.status}`);
      state.provenanceAudit = await response.json();
    }
  } catch (error) {
    state.provenanceAudit = bundledProvenanceAudit;
  }
  renderProvenanceAudit();
}

function renderProvenanceAudit() {
  if (!outputs.provenanceAuditStatus || !outputs.provenanceAuditSummary || !outputs.provenanceAuditRows) return;
  const audit = state.provenanceAudit || bundledProvenanceAudit;
  const summary = audit.summary || {};
  const rows = audit.rows || [];
  const gate = audit.claim_gate || {};
  outputs.provenanceAuditStatus.textContent =
    `${formatNumber(audit.blocked_count || 0)} blocked · ${escapeHtml(gate.status || "unknown")}`;
  outputs.provenanceAuditSummary.innerHTML = `
    <div><span>Audited rows</span><strong>${formatNumber(audit.row_count || rows.length)}</strong><small>${formatNumber(audit.pass_count || 0)} passed</small></div>
    <div><span>Blocked</span><strong>${formatNumber(audit.blocked_count || 0)}</strong><small>claim gate</small></div>
    <div><span>Forbidden</span><strong>${formatNumber(summary.forbidden_public_field_count || 0)}</strong><small>public field paths</small></div>
    <div><span>Checksums</span><strong>${formatNumber(summary.invalid_field_count || 0)}</strong><small>invalid sha256</small></div>
  `;
  outputs.provenanceAuditRows.innerHTML = rows
    .slice()
    .sort((a, b) => {
      const aPenalty = (a.missing_required_fields || []).length + (a.forbidden_public_fields || []).length;
      const bPenalty = (b.missing_required_fields || []).length + (b.forbidden_public_fields || []).length;
      return bPenalty - aPenalty;
    })
    .map((row) => {
      const forbidden = row.forbidden_public_fields || [];
      const invalid = row.invalid_fields || [];
      const issue = forbidden[0] || invalid[0]?.field || (row.missing_required_fields || [])[0] || "public-safe";
      return `
        <div class="provenance-row audit-row">
          <strong>${escapeHtml(row.library || row.baseline_id || "unknown")}</strong>
          <span>${formatPercent(row.completion_ratio || 0)} complete</span>
          <em class="${row.status === "pass" ? "is-pass" : "is-blocked"}">${escapeHtml(row.status || "blocked")}</em>
          <code>${escapeHtml(issue)}</code>
        </div>
      `;
    })
    .join("");
}

function renderCollectionMatrix() {
  if (!outputs.collectionMatrixStatus || !outputs.collectionMatrixRows) return;
  const matrix = state.collectionMatrix || bundledCollectionMatrix;
  const gate = matrix.claim_gate || {};
  outputs.collectionMatrixStatus.textContent =
    `${formatNumber(matrix.complete_target_count || 0)} / ${formatNumber(matrix.target_count || 0)} targets complete · ${escapeHtml(gate.status || "unknown")}`;
  outputs.collectionMatrixRows.innerHTML = (matrix.rows || [])
    .map((row) => `
      <div class="collection-row">
        <div>
          <strong>${escapeHtml(row.library || "unknown")}</strong>
          <span>${escapeHtml(row.track || "")}${row.sensitive ? " · local raw data" : " · public metadata"}</span>
        </div>
        <div class="collection-targets">
          ${(row.targets || [])
            .map((target) => `
              <em class="${target.status === "available" ? "is-available" : "is-planned"}" title="${escapeHtml(target.public_output || "")}">
                ${formatNumber(target.bit_length || 0)}b / ${formatNumber(target.sample_target || 0)}
              </em>
            `)
            .join("")}
        </div>
      </div>
    `)
    .join("") + `
      <div class="collection-gate">
        <strong>Claim gate</strong>
        <span>${escapeHtml(gate.message || "No claim gate is defined.")}</span>
      </div>
    `;
}

async function loadResearchReadiness() {
  try {
    if (window.location.protocol === "file:") {
      state.researchReadiness = bundledResearchReadiness;
    } else {
      const response = await fetch("data/research_readiness.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`research readiness ${response.status}`);
      state.researchReadiness = await response.json();
    }
  } catch (error) {
    state.researchReadiness = bundledResearchReadiness;
  }
  renderResearchReadiness();
}

function renderResearchReadiness() {
  if (!outputs.readinessSummary || !outputs.readinessDimensions || !outputs.readinessActions) return;
  const report = state.researchReadiness || bundledResearchReadiness;
  const overall = report.overall || {};
  const dimensions = report.dimensions || {};
  const blocking = report.blocking_gaps || [];
  outputs.readinessSummary.innerHTML = `
    <div><span>Overall</span><strong>${formatPercent(overall.score || 0)}</strong><small>${escapeHtml(overall.label || "unknown")}</small></div>
    <div><span>Blocking gaps</span><strong>${formatNumber(blocking.length)}</strong><small>high priority</small></div>
    <div><span>Real baselines</span><strong>${formatNumber(dimensions.sim_to_real?.available_count || 0)}</strong><small>available</small></div>
    <div><span>Robust profiles</span><strong>${formatNumber((dimensions.attribution_validation?.robust_profiles || []).length)}</strong><small>controlled</small></div>
  `;
  outputs.readinessDimensions.innerHTML = Object.entries(dimensions)
    .map(([name, dimension]) => {
      const gaps = dimension.gaps || [];
      return `
        <div class="readiness-card">
          <div>
            <strong>${formatDimensionName(name)}</strong>
            <em class="${readinessClass(dimension.label)}">${escapeHtml(dimension.label || "unknown")}</em>
          </div>
          <meter min="0" max="1" value="${Number(dimension.score || 0)}"></meter>
          <span>${formatPercent(dimension.score || 0)} readiness</span>
          <p>${formatDimensionEvidence(name, dimension)}</p>
          <small>${gaps.length ? `${gaps.length} gap${gaps.length === 1 ? "" : "s"}` : "no active gap"}</small>
        </div>
      `;
    })
    .join("");
  outputs.readinessActions.innerHTML = (report.next_actions || [])
    .map((action) => `
      <li>
        <strong>${escapeHtml(action.priority || "P?")} ${escapeHtml(action.track || "research")}</strong>
        <span>${escapeHtml(action.action || "")}</span>
      </li>
    `)
    .join("");
}

async function loadEvidencePack() {
  try {
    if (window.location.protocol === "file:") {
      state.evidencePack = bundledEvidencePack;
    } else {
      const response = await fetch("data/evidence_pack.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`evidence pack ${response.status}`);
      state.evidencePack = await response.json();
    }
  } catch (error) {
    state.evidencePack = bundledEvidencePack;
  }
  renderEvidencePack();
}

function renderEvidencePack() {
  if (!outputs.evidenceSummary || !outputs.evidenceGateRows || !outputs.evidenceArtifactRows) return;
  const pack = state.evidencePack || bundledEvidencePack;
  const claim = pack.claim_level || {};
  const gates = pack.publication_gates || [];
  const failed = gates.filter((gateItem) => !gateItem.passed);
  outputs.evidenceSummary.innerHTML = `
    <div><span>Claim level</span><strong>${escapeHtml(claim.level || "unknown")}</strong><small>${escapeHtml(claim.statement || "")}</small></div>
    <div><span>Failed gates</span><strong>${formatNumber(failed.length)}</strong><small>${formatNumber(claim.failed_high_gate_count || 0)} high</small></div>
    <div><span>Artifacts</span><strong>${formatNumber(pack.artifact_count || (pack.artifacts || []).length)}</strong><small>checksummed</small></div>
  `;
  outputs.evidenceGateRows.innerHTML = gates
    .map((gateItem) => `
      <div class="evidence-row">
        <strong>${escapeHtml(gateItem.code || "gate")}</strong>
        <em class="${gateItem.passed ? "is-pass" : "is-fail"}">${gateItem.passed ? "pass" : "fail"}</em>
        <span>${escapeHtml(gateItem.severity || "unknown")}</span>
      </div>
    `)
    .join("");
  outputs.evidenceArtifactRows.innerHTML = (pack.artifacts || [])
    .map((artifact) => `
      <div class="evidence-row artifact-row">
        <strong>${escapeHtml(artifact.role || "artifact")}</strong>
        <span>${escapeHtml(artifact.schema || "unknown schema")}</span>
        <code>${escapeHtml(shortHash(artifact.sha256))}</code>
      </div>
    `)
    .join("");
}

async function loadAttributionGrid() {
  try {
    if (window.location.protocol === "file:") {
      state.attributionGrid = bundledAttributionGrid;
    } else {
      const response = await fetch("data/attribution_confound_grid.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`attribution grid ${response.status}`);
      state.attributionGrid = await response.json();
    }
  } catch (error) {
    state.attributionGrid = bundledAttributionGrid;
  }
  renderAttributionGrid();
}

function renderAttributionGrid() {
  if (!outputs.attributionSummary || !outputs.attributionGridSvg || !outputs.attributionProfileRows) return;
  const grid = state.attributionGrid;
  if (!grid || !grid.summary) {
    outputs.attributionSummary.textContent = "No attribution grid data is bundled.";
    return;
  }
  const profiles = Object.entries(grid.summary.profiles || {}).map(([profile, summary]) => ({
    profile,
    ...summary,
  }));
  const strongestControlled = [...profiles].sort(
    (a, b) => b.mean_controlled_accuracy - a.mean_controlled_accuracy,
  )[0];
  const strongestConfound = (grid.summary.most_confound_sensitive_profiles || [])[0];
  outputs.attributionSummary.innerHTML = `
    <div><span>Runs</span><strong>${formatNumber((grid.rows || []).length || (grid.deltas || []).length)}</strong></div>
    <div><span>Repeats</span><strong>${formatNumber(grid.repeats || 1)}</strong></div>
    <div><span>Random baseline</span><strong>${formatPercent(grid.random_baseline_accuracy || 1 / 3)}</strong></div>
    <div><span>Best controlled</span><strong>${strongestControlled ? strongestControlled.profile : "n/a"}</strong></div>
    <div><span>Controlled accuracy</span><strong>${strongestControlled ? formatPercent(strongestControlled.mean_controlled_accuracy) : "n/a"}</strong></div>
    <div><span>Top confound</span><strong>${strongestConfound ? strongestConfound.profile : "none"}</strong></div>
  `;
  renderAttributionHeatmap(grid);
  outputs.attributionProfileRows.innerHTML = profiles
    .sort((a, b) => b.mean_controlled_accuracy - a.mean_controlled_accuracy)
    .map((profile) => {
      const dropStats = profile.accuracy_drop || { mean: profile.mean_accuracy_drop };
      const interpretation = profile.robust_interpretation || dominantInterpretation(profile.interpretations || {});
      return `<tr>
        <td>${profile.profile}</td>
        <td>${formatPercent(profile.mean_uncontrolled_accuracy)}</td>
        <td>${formatPercent(profile.mean_controlled_accuracy)}</td>
        <td>${formatPValue(profile.controlled_significance?.p_value)}</td>
        <td class="${profile.mean_accuracy_drop > 0.05 ? "is-drop" : "is-stable"}">${formatSignedPercent(profile.mean_accuracy_drop)}</td>
        <td>${formatPercentInterval(dropStats)}</td>
        <td>${interpretation}</td>
      </tr>`;
    })
    .join("");
}

function renderAttributionHeatmap(grid) {
  const svg = outputs.attributionGridSvg;
  const width = 760;
  const height = 360;
  const padding = { top: 48, right: 34, bottom: 54, left: 126 };
  const deltas = aggregateAttributionDeltas(grid.deltas || []);
  const profiles = [...new Set(deltas.map((delta) => delta.profile))];
  const pairs = [...new Set(deltas.map((delta) => delta.base_pair_key || delta.pair_key))];
  const maxPairs = Math.min(10, pairs.length);
  const shownPairs = pairs.slice(0, maxPairs);
  const cellWidth = (width - padding.left - padding.right) / Math.max(1, shownPairs.length);
  const cellHeight = Math.min(42, (height - padding.top - padding.bottom) / Math.max(1, profiles.length));
  const lookup = new Map(deltas.map((delta) => [`${delta.profile}|${delta.base_pair_key || delta.pair_key}`, delta]));
  svg.innerHTML = "";
  appendSvg(svg, "text", { x: padding.left, y: 24, class: "chart-title" }).textContent =
    "accuracy drop after bit-length control";
  appendSvg(svg, "text", { x: padding.left + 250, y: 24, class: "chart-label" }).textContent =
    "amber = confound-sensitive, teal = survives control";

  profiles.forEach((profile, rowIndex) => {
    const y = padding.top + rowIndex * cellHeight;
    appendSvg(svg, "text", {
      x: 18,
      y: y + cellHeight * 0.62,
      class: "chart-label",
    }).textContent = profile;
    shownPairs.forEach((pair, columnIndex) => {
      const delta = lookup.get(`${profile}|${pair}`);
      const drop = delta ? delta.accuracy_drop : 0;
      const intensity = Math.min(1, Math.abs(drop) / 0.5);
      const fill = drop >= 0 ? rgbaHex(colors.amber, 0.18 + intensity * 0.72) : rgbaHex(colors.teal, 0.18 + intensity * 0.72);
      const x = padding.left + columnIndex * cellWidth;
      appendSvg(svg, "rect", {
        x,
        y,
        width: Math.max(2, cellWidth - 4),
        height: Math.max(10, cellHeight - 6),
        fill,
      });
      appendSvg(svg, "text", {
        x: x + cellWidth / 2,
        y: y + cellHeight * 0.62,
        "text-anchor": "middle",
        class: "axis-label",
      }).textContent = formatSignedPercent(drop);
      if (rowIndex === profiles.length - 1) {
        appendSvg(svg, "text", {
          x: x + cellWidth / 2,
          y: height - 18,
          "text-anchor": "middle",
          class: "axis-label",
        }).textContent = compactPairLabel(pair);
      }
    });
  });
}

function aggregateAttributionDeltas(deltas) {
  const grouped = new Map();
  deltas.forEach((delta) => {
    const pair = delta.base_pair_key || delta.pair_key;
    const key = `${delta.profile}|${pair}`;
    if (!grouped.has(key)) {
      grouped.set(key, {
        profile: delta.profile,
        pair_key: pair,
        base_pair_key: pair,
        values: [],
      });
    }
    grouped.get(key).values.push(delta.accuracy_drop);
  });
  return [...grouped.values()].map((entry) => ({
    profile: entry.profile,
    pair_key: entry.pair_key,
    base_pair_key: entry.base_pair_key,
    accuracy_drop: mean(entry.values),
  }));
}

function setSnapshotImage(image, path, alt) {
  if (!image) return;
  image.src = path;
  image.alt = alt;
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

function wrapSvgText(svg, text, x, y, maxChars, maxLines) {
  const words = String(text).split(/\s+/);
  const lines = [];
  let current = "";
  words.forEach((word) => {
    const next = current ? `${current} ${word}` : word;
    if (next.length > maxChars && current) {
      lines.push(current);
      current = word;
    } else {
      current = next;
    }
  });
  if (current) lines.push(current);
  lines.slice(0, maxLines).forEach((line, index) => {
    const visible = index === maxLines - 1 && lines.length > maxLines ? `${line.slice(0, Math.max(0, maxChars - 1))}...` : line;
    appendSvg(svg, "text", { x, y: y + index * 13, class: "evolution-node-label" }).textContent = visible;
  });
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

function mean(values) {
  return values.length ? sum(values) / values.length : 0;
}

function maxOf(values) {
  let maximum = -Infinity;
  values.forEach((value) => {
    if (value > maximum) maximum = value;
  });
  return maximum;
}

function maxBy(values, mapper) {
  let maximum = -Infinity;
  values.forEach((value) => {
    const mapped = mapper(value);
    if (mapped > maximum) maximum = mapped;
  });
  return maximum;
}

function sliderToLimit(position) {
  const ratio = Math.max(0, Math.min(limitSlider.steps, position)) / limitSlider.steps;
  const raw = limitSlider.min * (limitSlider.max / limitSlider.min) ** ratio;
  const step = raw < 1000000 ? 10000 : 100000;
  return Math.max(limitSlider.min, Math.round(raw / step) * step);
}

function limitToSlider(limit) {
  const bounded = Math.max(limitSlider.min, Math.min(limitSlider.max, limit));
  return Math.round((Math.log(bounded / limitSlider.min) / Math.log(limitSlider.max / limitSlider.min)) * limitSlider.steps);
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => (
    {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[character]
  ));
}

function formatDimensionName(value) {
  return String(value).replaceAll("_", " ");
}

function readinessClass(label) {
  if (label === "research_ready") return "is-ready";
  if (label === "prototype_ready") return "is-prototype";
  if (label === "scaffold_ready") return "is-scaffold";
  return "is-not-started";
}

function formatDimensionEvidence(name, dimension) {
  if (name === "sim_to_real") {
    return `${formatNumber(dimension.registered_count || 0)} registered, ${formatNumber(dimension.planned_count || 0)} planned, ${formatNumber(dimension.sensitive_count || 0)} local-sensitive.`;
  }
  if (name === "attribution_validation") {
    return `${formatNumber(dimension.rows || 0)} rows, ${formatNumber(dimension.repeats || 0)} repeats, ${(dimension.robust_profiles || []).join(", ") || "no robust profile"}.`;
  }
  if (name === "classifier") {
    return `${formatNumber(dimension.vector_count || 0)} vectors across ${formatNumber(dimension.label_count || 0)} labels.`;
  }
  if (name === "bitcoin_integration") {
    return `${formatNumber(dimension.related_baseline_count || 0)} related baseline, risk ${dimension.risk_level || "not bundled"}.`;
  }
  return `${formatNumber(dimension.gaps?.length || 0)} active gaps.`;
}

function shortHash(value) {
  if (!value) return "missing";
  return `${String(value).slice(0, 10)}...`;
}

function formatCompact(value) {
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

function formatPercent(value) {
  return `${((Number(value) || 0) * 100).toFixed(1)}%`;
}

function formatSignedPercent(value) {
  const numeric = Number(value) || 0;
  const sign = numeric > 0 ? "+" : "";
  return `${sign}${(numeric * 100).toFixed(1)}%`;
}

function formatPercentInterval(summary) {
  if (summary && Number.isFinite(summary.ci95_low) && Number.isFinite(summary.ci95_high)) {
    return `${formatSignedPercent(summary.ci95_low)} to ${formatSignedPercent(summary.ci95_high)}`;
  }
  return "n/a";
}

function formatPValue(value) {
  if (!Number.isFinite(value)) return "n/a";
  if (value < 0.001) return "<0.001";
  return value.toFixed(3);
}

function dominantInterpretation(interpretations) {
  const entries = Object.entries(interpretations);
  if (entries.length === 0) return "inconclusive";
  return entries.sort((a, b) => b[1] - a[1])[0][0];
}

function compactPairLabel(pairKey) {
  const match = /limit=(\d+);train=(\d+);test=(\d+)/.exec(pairKey);
  if (!match) return pairKey;
  return `${formatCompact(Number(match[1]))}/${match[2]}/${match[3]}`;
}
