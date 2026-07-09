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
  nullCalibration: null,
  replicationAudit: null,
  realBaselineManifest: null,
  researchReadiness: null,
  featureVectors: null,
  cryptoClassifier: null,
  evidencePack: null,
  claimLedger: null,
  artifactLineage: null,
  decisionProtocol: null,
  falsificationBattery: null,
  publicationConsistency: null,
  projectEvolution: null,
  collectionMatrix: null,
  collectionPower: null,
  provenanceRequirements: null,
  provenanceAudit: null,
  baselineAcceptance: null,
  baselinePromotion: null,
  collectionHandoff: null,
  collectionSubmissionContract: null,
  collectionSubmissionLint: null,
  collectionFixtureAudit: null,
  collectionIntake: null,
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

const bundledNullCalibration = {
  schema: "primeproject.null-calibration.v1",
  source: {
    controlled_row_count: 24,
    profile_count: 5,
    random_baseline_accuracy: 1 / 3,
  },
  method: {
    name: "row-structured binomial null calibration",
    iterations: 5000,
    familywise_control: "maximum observed lift across profiles per simulated iteration",
  },
  summary: {
    profile_count: 5,
    familywise_survivor_count: 2,
    top_profile: "gap_only",
    top_familywise_p_value: 0.0002,
    claim_floor: "controlled_synthetic_only",
  },
  profiles: [
    { profile: "gap_only", observed_controlled_accuracy: 0.606481, observed_lift: 0.273148, null_ci95_low: 0.273148, null_ci95_high: 0.398148, pointwise_p_value: 0.0002, familywise_p_value: 0.0002, interpretation: "familywise_survives_null" },
    { profile: "all", observed_controlled_accuracy: 0.550926, observed_lift: 0.217593, null_ci95_low: 0.273148, null_ci95_high: 0.398148, pointwise_p_value: 0.0002, familywise_p_value: 0.0002, interpretation: "familywise_survives_null" },
    { profile: "bit_length_only", observed_controlled_accuracy: 0.333333, observed_lift: 0, null_ci95_low: 0.268519, null_ci95_high: 0.398148, pointwise_p_value: 0.529494, familywise_p_value: 0.977604, interpretation: "near_null" },
    { profile: "low_bits_only", observed_controlled_accuracy: 0.333333, observed_lift: 0, null_ci95_low: 0.273148, null_ci95_high: 0.398148, pointwise_p_value: 0.525495, familywise_p_value: 0.977604, interpretation: "near_null" },
    { profile: "residue_only", observed_controlled_accuracy: 0.291667, observed_lift: -0.041667, null_ci95_low: 0.273148, null_ci95_high: 0.398148, pointwise_p_value: 0.911818, familywise_p_value: 1, interpretation: "near_null" },
  ],
};

const bundledReplicationAudit = {
  schema: "primeproject.replication-audit.v1",
  method: {
    lift_threshold: 0.1,
    minimum_replicated_ratio: 0.75,
  },
  summary: {
    profile_count: 5,
    setting_count: 8,
    stable_profile_count: 2,
    stable_profiles: ["gap_only", "all"],
    claim_floor: "controlled_synthetic_only",
  },
  profiles: [
    { profile: "gap_only", setting_count: 8, replicated_setting_count: 8, replicated_ratio: 1, mean_controlled_accuracy: 0.606482, minimum_setting_lift: 0.185185, null_interpretation: "familywise_survives_null", familywise_p_value: 0.0002, status: "replicated_and_null_calibrated", weak_settings: [] },
    { profile: "all", setting_count: 8, replicated_setting_count: 8, replicated_ratio: 1, mean_controlled_accuracy: 0.550926, minimum_setting_lift: 0.111111, null_interpretation: "familywise_survives_null", familywise_p_value: 0.0002, status: "replicated_and_null_calibrated", weak_settings: [] },
    { profile: "bit_length_only", setting_count: 8, replicated_setting_count: 0, replicated_ratio: 0, mean_controlled_accuracy: 0.333333, minimum_setting_lift: 0, null_interpretation: "near_null", familywise_p_value: 0.977604, status: "not_replicated", weak_settings: ["all settings"] },
    { profile: "low_bits_only", setting_count: 8, replicated_setting_count: 0, replicated_ratio: 0, mean_controlled_accuracy: 0.333333, minimum_setting_lift: 0, null_interpretation: "near_null", familywise_p_value: 0.977604, status: "not_replicated", weak_settings: ["all settings"] },
    { profile: "residue_only", setting_count: 8, replicated_setting_count: 0, replicated_ratio: 0, mean_controlled_accuracy: 0.291666, minimum_setting_lift: -0.148148, null_interpretation: "near_null", familywise_p_value: 1, status: "not_replicated", weak_settings: ["all settings"] },
  ],
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
    interval_confidence: 0.95,
    interval_label: "95pct",
    target_tv: 0.1,
    target_tv_label: "10pct",
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
      { library: "OpenSSL", bit_length: 2048, sample_target: 500, interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
      { library: "OpenSSL", bit_length: 3072, sample_target: 500, interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
      { library: "OpenSSL", bit_length: 4096, sample_target: 500, interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    ],
  },
  rows: [
    { library: "OpenSSL", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "OpenSSL", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "OpenSSL", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "BoringSSL", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 2048, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 3072, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "Go crypto/rsa", bit_length: 4096, sample_target: 500, object_type: "rsa-prime", power_tier: "coarse", interval_label: "95pct", conservative_tv_floor_interval: 0.300457, conservative_tv_floor_95: 0.300457, target_tv_label: "10pct", min_samples_for_target_tv: 4514, min_samples_for_10pct_tv: 4514 },
    { library: "Bitcoin Core / wallet metadata", bit_length: 256, sample_target: 10000, object_type: "ecdsa-signature", power_tier: "strong", interval_label: "95pct", conservative_tv_floor_interval: 0.077784, conservative_tv_floor_95: 0.077784, target_tv_label: "10pct", min_samples_for_target_tv: 6051, min_samples_for_10pct_tv: 6051 },
  ],
  sensitivity: {
    alpha_values: [0.1, 0.05, 0.01, 0.001],
    target_tv_values: [0.2, 0.1, 0.05],
    rows: [
      { object_type: "rsa-prime", bucket_count: 48, planned_sample_target: 500, alpha: 0.05, target_tv: 0.2, target_tv_label: "20pct", min_samples: 1129, sample_gap_vs_planned_target: 629 },
      { object_type: "rsa-prime", bucket_count: 48, planned_sample_target: 500, alpha: 0.05, target_tv: 0.1, target_tv_label: "10pct", min_samples: 4514, sample_gap_vs_planned_target: 4014 },
      { object_type: "rsa-prime", bucket_count: 48, planned_sample_target: 500, alpha: 0.05, target_tv: 0.05, target_tv_label: "5pct", min_samples: 18055, sample_gap_vs_planned_target: 17555 },
      { object_type: "rsa-prime", bucket_count: 48, planned_sample_target: 500, alpha: 0.001, target_tv: 0.05, target_tv_label: "5pct", min_samples: 50890, sample_gap_vs_planned_target: 50390 },
      { object_type: "ecdsa-signature", bucket_count: 64, planned_sample_target: 10000, alpha: 0.05, target_tv: 0.1, target_tv_label: "10pct", min_samples: 6051, sample_gap_vs_planned_target: 0 },
    ],
  },
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

const bundledBaselineAcceptance = {
  schema: "primeproject.baseline-acceptance.v1",
  row_count: 10,
  accepted_count: 0,
  screening_only_count: 0,
  blocked_count: 10,
  summary: {
    accepted_rsa_library_count: 0,
    accepted_rsa_libraries: [],
    minimum_rsa_libraries: 2,
    public_safe: true,
    dominant_blockers: [
      { reason: "manifest_not_available", count: 10 },
      { reason: "provenance_not_passed", count: 10 },
      { reason: "target_not_available", count: 10 },
    ],
  },
  claim_gate: {
    status: "blocked",
    message:
      "Real-world attribution remains blocked until at least two RSA libraries pass availability, provenance, and power gates.",
  },
  rows: [
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", bit_length: 2048, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", bit_length: 3072, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", bit_length: 4096, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
    { baseline_id: "boringssl-rsa-prime-owned", library: "BoringSSL", object_type: "rsa-prime", bit_length: 2048, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
    { baseline_id: "boringssl-rsa-prime-owned", library: "BoringSSL", object_type: "rsa-prime", bit_length: 3072, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
    { baseline_id: "go-crypto-rsa-prime-owned", library: "Go crypto/rsa", object_type: "rsa-prime", bit_length: 2048, acceptance: "blocked", power_tier: "coarse", blocking_reasons: ["manifest_not_available", "target_not_available", "provenance_not_passed"] },
  ],
};

const bundledBaselinePromotion = {
  schema: "primeproject.baseline-promotion-plan.v1",
  row_count: 10,
  summary: {
    ready_count: 0,
    p0_target_count: 9,
    minimal_unlock_target_count: 2,
    projected_samples_for_minimal_unlock: 9028,
    dominant_next_step: "collect_aggregate_baseline",
  },
  minimal_unlock_targets: [
    { baseline_id: "openssl-rsa-prime-owned", library: "OpenSSL", object_type: "rsa-prime", bit_length: 2048, priority: "P0", current_acceptance: "blocked", promotion_state: "collect_and_document", next_step: "collect_aggregate_baseline", current_samples: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, remaining_samples_to_10pct_tv: 4514, power_tier: "coarse" },
    { baseline_id: "boringssl-rsa-prime-owned", library: "BoringSSL", object_type: "rsa-prime", bit_length: 2048, priority: "P0", current_acceptance: "blocked", promotion_state: "collect_and_document", next_step: "collect_aggregate_baseline", current_samples: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, remaining_samples_to_10pct_tv: 4514, power_tier: "coarse" },
  ],
  claim_gate: {
    status: "blocked",
    message: "Promotion plan identifies the shortest public-safe path from blocked baselines to accepted real-world evidence.",
  },
};

const bundledCollectionHandoff = {
  schema: "primeproject.collection-handoff.v1",
  summary: {
    task_count: 10,
    p0_count: 2,
    blocked_count: 10,
    remaining_p0_samples_for_10pct_tv: 9028,
    missing_provenance_field_count: 89,
    classifier_scope: "controlled_synthetic_only",
    classifier_label_count: 3,
    next_unlock: "collect OpenSSL 2048-bit and BoringSSL 2048-bit aggregate RSA-prime baselines with complete provenance",
  },
  claim_gate: {
    status: "blocked",
    message: "Handoff is ready for collection execution, but real-world attribution claims remain blocked.",
  },
  public_artifact_contract: {
    publish_private_material: false,
    required_public_outputs: [
      "aggregate fingerprint JSON",
      "baseline JSON",
      "feature vector JSON",
      "provenance record JSON",
      "SHA-256 checksum",
    ],
  },
  rows: [
    { priority: "P0", library: "BoringSSL", baseline_id: "boringssl-rsa-prime-owned", track: "rsa-prime-generation", object_type: "rsa-prime", bit_length: 2048, remaining_samples_to_plan: 500, remaining_samples_to_10pct_tv: 4514, acceptance: "blocked", provenance_status: "blocked", public_output: "aggregate fingerprint + baseline + feature vector", collector_contract: { minimum_replicates: 3, must_not_publish: ["private_key", "private_prime", "raw_key_file"] } },
    { priority: "P0", library: "OpenSSL", baseline_id: "openssl-rsa-prime-owned", track: "rsa-prime-generation", object_type: "rsa-prime", bit_length: 2048, remaining_samples_to_plan: 500, remaining_samples_to_10pct_tv: 4514, acceptance: "blocked", provenance_status: "blocked", public_output: "aggregate fingerprint + baseline + feature vector", collector_contract: { minimum_replicates: 3, must_not_publish: ["private_key", "private_prime", "raw_key_file"] } },
    { priority: "P1", library: "Bitcoin Core / wallet metadata", baseline_id: "bitcoin-core-ecdsa-signature-public", track: "signature-nonce-metadata", object_type: "ecdsa-signature", bit_length: 256, remaining_samples_to_plan: 10000, remaining_samples_to_10pct_tv: 10000, acceptance: "blocked", provenance_status: "blocked", public_output: "nonce-risk summary + distribution fingerprint", collector_contract: { minimum_replicates: 1, must_not_publish: ["wallet_seed", "private_key", "raw_signature_owner"] } },
    { priority: "P1", library: "Go crypto/rsa", baseline_id: "go-crypto-rsa-prime-owned", track: "rsa-prime-generation", object_type: "rsa-prime", bit_length: 2048, remaining_samples_to_plan: 500, remaining_samples_to_10pct_tv: 4514, acceptance: "blocked", provenance_status: "blocked", public_output: "aggregate fingerprint + baseline + feature vector", collector_contract: { minimum_replicates: 3, must_not_publish: ["private_key", "private_prime", "raw_key_file"] } },
  ],
};

const bundledCollectionSubmissionContract = {
  schema: "primeproject.collection-submission-contract.v1",
  summary: {
    task_count: 10,
    p0_count: 2,
    required_record_field_count: 7,
    required_scalar_feature_count: 14,
    forbidden_public_field_count: 5,
    claim_scope_required: "real_world",
    feature_vector_schema: "generator-feature-vector.v1",
    private_material_publication_allowed: false,
  },
  record_contract: {
    required_fields: [
      "task_id",
      "sample_count",
      "claim_scope",
      "aggregate_artifact_sha256",
      "provenance_record",
      "feature_vector_path",
      "feature_vector_summary",
    ],
    claim_scope_must_equal: "real_world",
  },
  feature_vector_contract: {
    schema: "generator-feature-vector.v1",
    required_scalar_features: [
      "record_count_log2",
      "bit_length_mean",
      "bit_length_stddev",
      "bit_length_entropy",
      "bit_length_max_mass",
      "residue_tv_30",
      "residue_tv_210",
      "residue_tv_2310",
      "low16_collision_rate",
      "next_prime_exposure_score",
      "mean_left_gap_over_logp",
      "mean_right_gap_over_logp",
      "large_left_gap_ratio",
      "max_residue_tv",
    ],
    record_count_must_equal_sample_count: true,
    bit_length_mean_must_match_task_bit_length: true,
  },
  public_safety: {
    forbidden_field_names: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"],
    private_material_publication_allowed: false,
  },
  acceptance_checks: [
    { code: "known_task", blocks: true },
    { code: "single_submission_per_task", blocks: true },
    { code: "sample_floor", blocks: true },
    { code: "checksum_integrity", blocks: true },
    { code: "provenance_record", blocks: true },
    { code: "feature_vector_contract", blocks: true },
    { code: "public_safety", blocks: true },
  ],
  task_templates: [
    { task_id: "boringssl-rsa-prime-owned:2048:rsa-prime", priority: "P0", library: "BoringSSL", object_type: "rsa-prime", bit_length: 2048, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, must_not_publish: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"] },
    { task_id: "openssl-rsa-prime-owned:2048:rsa-prime", priority: "P0", library: "OpenSSL", object_type: "rsa-prime", bit_length: 2048, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, must_not_publish: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"] },
    { task_id: "bitcoin-core-ecdsa-signature-public:256:ecdsa-signature", priority: "P1", library: "Bitcoin Core / wallet metadata", object_type: "ecdsa-signature", bit_length: 256, planned_sample_target: 10000, target_samples_for_10pct_tv: 10000, must_not_publish: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"] },
    { task_id: "go-crypto-rsa-prime-owned:2048:rsa-prime", priority: "P1", library: "Go crypto/rsa", object_type: "rsa-prime", bit_length: 2048, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, must_not_publish: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"] },
  ],
};

const bundledCollectionSubmissionLint = {
  schema: "primeproject.collection-submission-lint.v1",
  summary: {
    task_count: 10,
    submitted_count: 0,
    awaiting_submission_count: 10,
    pass_count: 0,
    warning_count: 0,
    blocked_count: 0,
    forbidden_public_field_count: 0,
    feature_vector_blocked_count: 0,
    reused_aggregate_hash_count: 0,
    dominant_blockers: [],
    dominant_warnings: [{ reason: "awaiting_submission", count: 10 }],
  },
  lint_gate: {
    status: "waiting",
    message: "No submitted records are available; collectors can use the task templates before intake.",
  },
  rows: [
    { priority: "P0", library: "BoringSSL", baseline_id: "boringssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, sample_count: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, warning_reasons: ["awaiting_submission"], blocking_reasons: [], status: "awaiting_submission" },
    { priority: "P0", library: "OpenSSL", baseline_id: "openssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, sample_count: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, warning_reasons: ["awaiting_submission"], blocking_reasons: [], status: "awaiting_submission" },
    { priority: "P1", library: "Bitcoin Core / wallet metadata", baseline_id: "bitcoin-core-ecdsa-signature-public", object_type: "ecdsa-signature", bit_length: 256, submitted: false, sample_count: 0, planned_sample_target: 10000, target_samples_for_10pct_tv: 10000, warning_reasons: ["awaiting_submission"], blocking_reasons: [], status: "awaiting_submission" },
    { priority: "P1", library: "Go crypto/rsa", baseline_id: "go-crypto-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, sample_count: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, warning_reasons: ["awaiting_submission"], blocking_reasons: [], status: "awaiting_submission" },
    { priority: "P2", library: "BoringSSL", baseline_id: "boringssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 3072, submitted: false, sample_count: 0, planned_sample_target: 500, target_samples_for_10pct_tv: 4514, warning_reasons: ["awaiting_submission"], blocking_reasons: [], status: "awaiting_submission" },
  ],
};

const bundledCollectionFixtureAudit = {
  schema: "primeproject.collection-fixture-audit.v1",
  summary: {
    fixture_count: 10,
    passed_expectation_count: 10,
    failed_expectation_count: 0,
    expected_pass_count: 1,
    expected_warning_count: 1,
    expected_blocked_count: 8,
    actual_pass_count: 1,
    actual_warning_count: 1,
    actual_blocked_count: 8,
    public_safe_fixture_count: 10,
  },
  quality_gate: {
    status: "pass",
    message: "Submission lint behavior matches all public-safe fixture expectations.",
  },
  lint_summary: {
    submitted_count: 10,
    awaiting_submission_count: 0,
    pass_count: 1,
    warning_count: 1,
    blocked_count: 8,
    reused_aggregate_hash_count: 2,
  },
  rows: [
    { fixture_id: "valid_warning", library: "BoringSSL", object_type: "rsa-prime", bit_length: 2048, expected_status: "warning", actual_status: "warning", expected_reasons: ["below_10pct_tv_floor"], actual_reasons: ["below_10pct_tv_floor"], expectation_met: true, public_safe: true },
    { fixture_id: "valid_ready", library: "OpenSSL", object_type: "rsa-prime", bit_length: 2048, expected_status: "pass", actual_status: "pass", expected_reasons: [], actual_reasons: [], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_missing_feature", library: "Bitcoin Core / wallet metadata", object_type: "ecdsa-signature", bit_length: 256, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["feature_vector_missing_features"], actual_reasons: ["feature_vector_missing_features"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_forbidden_field", library: "Go crypto/rsa", object_type: "rsa-prime", bit_length: 2048, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["forbidden_public_fields"], actual_reasons: ["forbidden_public_fields"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_provenance_identity", library: "BoringSSL", object_type: "rsa-prime", bit_length: 3072, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["provenance_baseline_id_mismatch"], actual_reasons: ["provenance_baseline_id_mismatch"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_feature_label", library: "BoringSSL", object_type: "rsa-prime", bit_length: 4096, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["feature_vector_label_mismatch"], actual_reasons: ["feature_vector_label_mismatch"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_record_identity", library: "Go crypto/rsa", object_type: "rsa-prime", bit_length: 3072, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["record_baseline_id_mismatch"], actual_reasons: ["record_baseline_id_mismatch"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_feature_path", library: "Go crypto/rsa", object_type: "rsa-prime", bit_length: 4096, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["feature_vector_path_public_relative"], actual_reasons: ["feature_vector_path_public_relative"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_reused_checksum_a", library: "OpenSSL", object_type: "rsa-prime", bit_length: 3072, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["aggregate_artifact_sha256_reused"], actual_reasons: ["aggregate_artifact_sha256_reused"], expectation_met: true, public_safe: true },
    { fixture_id: "blocked_reused_checksum_b", library: "OpenSSL", object_type: "rsa-prime", bit_length: 4096, expected_status: "blocked", actual_status: "blocked", expected_reasons: ["aggregate_artifact_sha256_reused"], actual_reasons: ["aggregate_artifact_sha256_reused"], expectation_met: true, public_safe: true },
  ],
};

const bundledCollectionIntake = {
  schema: "primeproject.collection-intake.v1",
  summary: {
    task_count: 10,
    submitted_count: 0,
    accepted_count: 0,
    screening_only_count: 0,
    blocked_count: 10,
    p0_blocked_count: 2,
    accepted_rsa_library_count: 0,
    accepted_rsa_libraries: [],
    remaining_p0_samples_for_10pct_tv: 9028,
    forbidden_public_field_count: 0,
    duplicate_submission_count: 0,
    reused_aggregate_hash_count: 0,
    feature_vector_contract_blocked_count: 0,
    dominant_blockers: [{ reason: "intake_record", count: 10 }],
  },
  claim_gate: {
    status: "blocked",
    message: "Real-world intake remains blocked until at least two RSA library tasks pass sample, provenance, checksum, feature-vector contract, duplicate-submission, reused-artifact, and public-safety checks.",
  },
  rows: [
    { priority: "P0", library: "BoringSSL", baseline_id: "boringssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, submission_count: 0, sample_count: 0, planned_sample_target: 500, remaining_samples_to_10pct_tv: 4514, claim_scope: "not_submitted", status: "blocked", blocking_reasons: ["intake_record"], forbidden_public_fields: [] },
    { priority: "P0", library: "OpenSSL", baseline_id: "openssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, submission_count: 0, sample_count: 0, planned_sample_target: 500, remaining_samples_to_10pct_tv: 4514, claim_scope: "not_submitted", status: "blocked", blocking_reasons: ["intake_record"], forbidden_public_fields: [] },
    { priority: "P1", library: "Bitcoin Core / wallet metadata", baseline_id: "bitcoin-core-ecdsa-signature-public", object_type: "ecdsa-signature", bit_length: 256, submitted: false, submission_count: 0, sample_count: 0, planned_sample_target: 10000, remaining_samples_to_10pct_tv: 10000, claim_scope: "not_submitted", status: "blocked", blocking_reasons: ["intake_record"], forbidden_public_fields: [] },
    { priority: "P1", library: "Go crypto/rsa", baseline_id: "go-crypto-rsa-prime-owned", object_type: "rsa-prime", bit_length: 2048, submitted: false, submission_count: 0, sample_count: 0, planned_sample_target: 500, remaining_samples_to_10pct_tv: 4514, claim_scope: "not_submitted", status: "blocked", blocking_reasons: ["intake_record"], forbidden_public_fields: [] },
    { priority: "P2", library: "BoringSSL", baseline_id: "boringssl-rsa-prime-owned", object_type: "rsa-prime", bit_length: 3072, submitted: false, submission_count: 0, sample_count: 0, planned_sample_target: 500, remaining_samples_to_10pct_tv: 4514, claim_scope: "not_submitted", status: "blocked", blocking_reasons: ["intake_record"], forbidden_public_fields: [] },
  ],
  public_safety: {
    forbidden_field_names: ["private_key", "private_prime", "raw_key_file", "raw_signature_owner", "wallet_seed"],
    private_material_publication_allowed: false,
  },
};

const bundledResearchReadiness = {
  schema: "primeproject.research-readiness.v1",
  overall: { score: 0.614, label: "prototype_ready" },
  dimensions: {
    sim_to_real: {
      score: 0.54,
      label: "scaffold_ready",
      raw_score: 0.75,
      readiness_cap: {
        max_score: 0.54,
        max_label: "scaffold_ready",
        reason: "Sim-to-real evidence cannot be research-ready until at least two aggregate generator baselines are available; public constants count only as controls.",
      },
      registered_count: 5,
      available_count: 0,
      manifest_available_count: 1,
      public_control_count: 1,
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
      score: 0.49,
      label: "scaffold_ready",
      vector_count: 12,
      label_count: 3,
      claim_scope: "controlled_synthetic_only",
      real_world_claim_ready: false,
      accuracy: 1 / 3,
      total: 12,
      gaps: [{ code: "classifier_scope_not_real_world", severity: "high" }],
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
    { dimension: "classifier", code: "classifier_scope_not_real_world", severity: "high" },
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
      action: "Export real-world labelled feature vectors for OpenSSL, BoringSSL, Go, and a suspicious sample before trusting classifier output.",
    },
    {
      priority: "P1",
      track: "bitcoin",
      action: "Bundle a Bitcoin risk report from owned or public metadata summaries and compare it with registered baselines.",
    },
  ],
};

const bundledFeatureVectors = {
  schema: "primeproject.generator-feature-vectors.v1",
  claim_scope: "controlled_synthetic_only",
  vector_count: 12,
  labels: ["next_prime", "rejection", "wheel30_next"],
  feature_names: [
    "record_count_log2",
    "bit_length_mean",
    "bit_length_stddev",
    "bit_length_entropy",
    "bit_length_max_mass",
    "residue_tv_30",
    "residue_tv_210",
    "residue_tv_2310",
    "low16_collision_rate",
    "next_prime_exposure_score",
    "mean_left_gap_over_logp",
    "mean_right_gap_over_logp",
    "large_left_gap_ratio",
    "max_residue_tv",
  ],
};

const bundledCryptoClassifier = {
  schema: "primeproject.crypto-classifier-report.v1",
  model: {
    family: "nearest-centroid",
    feature_space: "interaction",
    dependency: "stdlib",
  },
  claim_scope: "controlled_synthetic_only",
  vector_count: 12,
  usable_vector_count: 12,
  label_count: 3,
  accuracy: 1 / 3,
  correct: 4,
  total: 12,
  labels: {
    next_prime: { total: 4, correct: 0, accuracy: 0 },
    rejection: { total: 4, correct: 4, accuracy: 1 },
    wheel30_next: { total: 4, correct: 0, accuracy: 0 },
  },
  findings: [
    {
      check: "classifier_scope_limited",
      severity: "info",
      message: "Classifier report is not real-world attribution evidence; it can only validate the classifier plumbing and controlled-synthetic signal.",
    },
  ],
};

const bundledEvidencePack = {
  schema: "primeproject.evidence-pack.v1",
  claim_level: {
    level: "public_demo_only",
    statement: "Safe to publish as a research scaffold, not as real-world attribution evidence.",
    failed_gate_count: 5,
    failed_high_gate_count: 4,
  },
  publication_gates: [
    { code: "sensitive_publication_gate", passed: true, severity: "critical" },
    { code: "real_baseline_gate", passed: false, severity: "high" },
    { code: "controlled_signal_gate", passed: true, severity: "high" },
    { code: "classifier_gate", passed: false, severity: "high" },
    { code: "bitcoin_integration_gate", passed: false, severity: "medium" },
    { code: "reproducibility_gate", passed: true, severity: "medium" },
    {
      code: "claim_language_gate",
      passed: true,
      severity: "high",
      evidence: { quality_gate_status: "pass", fail_count: 0, scanned_file_count: 14 },
    },
    { code: "provenance_gate", passed: true, severity: "medium" },
    { code: "provenance_audit_gate", passed: true, severity: "medium" },
    { code: "collection_submission_contract_gate", passed: true, severity: "medium" },
    { code: "collection_submission_lint_gate", passed: true, severity: "medium" },
    {
      code: "collection_fixture_audit_gate",
      passed: true,
      severity: "medium",
      evidence: { quality_gate_status: "pass", fixture_count: 10, failed_expectation_count: 0, public_safe_fixture_count: 10 },
    },
    { code: "baseline_acceptance_gate", passed: false, severity: "high" },
    { code: "collection_intake_gate", passed: false, severity: "high" },
    { code: "promotion_plan_gate", passed: true, severity: "medium" },
  ],
  artifact_count: 21,
  artifacts: [
    { role: "attribution_grid", schema: "primeproject.attribution-confound-grid.v1", sha256: "4873f01f4deec22f70c3a98563cd37e0ccbb587313e4d70befebff30e3f12318" },
    { role: "baseline_acceptance", schema: "primeproject.baseline-acceptance.v1", sha256: "11bfcc840ff2cda806a9abca4c914475bd0f049cf9f5a5f930eafc5aec8657b3" },
    { role: "baseline_promotion_plan", schema: "primeproject.baseline-promotion-plan.v1", sha256: "4636041a732e84825a9c0af28075583927e1be1edbe25bbf988eb1333a509bd6" },
    { role: "classifier_report", schema: "primeproject.crypto-classifier-report.v1", sha256: "970185d874983453e0a2a27562e30d02f1e96826ad55a0216e93b504e3f10663" },
    { role: "claim_language_audit", schema: "primeproject.claim-language-audit.v1", sha256: "bundled-fallback", quality_gate_status: "pass", scanned_file_count: 15, scanned_line_count: 7006, claim_language_triggered_count: 89, claim_language_guarded_count: 89, claim_language_fail_count: 0 },
    { role: "collection_handoff", schema: "primeproject.collection-handoff.v1", sha256: "47e75e611e98837cac5ecc690cc49900a2b757a7b2d857d474988a4406a5f232" },
    { role: "collection_fixture_audit", schema: "primeproject.collection-fixture-audit.v1", sha256: "bundled-fallback", quality_gate_status: "pass", fixture_count: 10, failed_expectation_count: 0, public_safe_fixture_count: 10 },
    { role: "collection_intake", schema: "primeproject.collection-intake.v1", sha256: "9179e93a350bcebc96db80f095b4966f5514ae53c9866264d2c8731408d9469b" },
    { role: "collection_matrix", schema: "primeproject.real-world-collection-matrix.v1", sha256: "703703591cbfb4ca35f3c5dcb350043e75c698a8df750fb7a77c500bc4fc6f92" },
    { role: "collection_power", schema: "primeproject.collection-power.v1", sha256: "2a2472a6b27874b4e9d8e8dd8025f0d4452a89206cd44a2838ea2e23505edd15" },
    { role: "collection_submission_contract", schema: "primeproject.collection-submission-contract.v1", sha256: "c298e17b6dfb8779e04c6bff957658723ae5c57486e0a831980e147c1bac364f" },
    { role: "collection_submission_lint", schema: "primeproject.collection-submission-lint.v1", sha256: "7ab44e09bc80c5bbe75690f754e406f3e0c3df2d4455bd5b665d2c1538cd3564" },
    { role: "feature_vectors", schema: "primeproject.generator-feature-vectors.v1", sha256: "fe1b9e5a443a4159b58bc87eaf10adaad396fe00ffd553439aa8821bbad1d538" },
    { role: "manifest", schema: "primeproject.real-world-baseline-manifest.v1", sha256: "fb55fabb2ddf378a3f2a7065cee7bf1d5db1b1eda7ca5c659fddc9e0e037b2c7" },
    { role: "null_calibration", schema: "primeproject.null-calibration.v1", sha256: "9e71d4fe726202d2a7945aa3b18f28d665a2caea073aa4a1ed0ad0dd91262e40" },
    { role: "project_evolution", schema: "primeproject.project-evolution.v1", sha256: "bundled-fallback" },
    { role: "provenance_audit", schema: "primeproject.provenance-audit.v1", sha256: "3862c5032dc3caed31ef7a2aa9b491e109bdbd846e9e485ea50e7f68784813dd" },
    { role: "provenance_requirements", schema: "primeproject.provenance-requirements.v1", sha256: "e08ad1eac816bbbd725abeab1702ae0b03b7af2281bf5b0581e5e0c7aa8642e0" },
    { role: "readiness", schema: "primeproject.research-readiness.v1", sha256: "ed06deee979aa2845454739f1d8e67cdfe4128309b0867835a4d812d1f3e4c53" },
    { role: "replication_audit", schema: "primeproject.replication-audit.v1", sha256: "b37b9d357f5a02140ce61570d71aa93f2ad4eb616e7ea208ee447918c1212b1b" },
    { role: "snapshot_manifest", schema: "primeproject.snapshot-manifest.v1", sha256: "ff9fea32962c21607de547e13d6385b0a0d9d13efa08c8df25b0e72806be84e0" },
  ],
  required_evidence: [
    {
      item: "two_available_real_baselines",
      status: "missing",
      reason: "Needed to compare suspicious objects against more than one real generator family.",
    },
    {
      item: "real_world_labelled_feature_vectors",
      status: "missing",
      reason:
        "Needed before classifier output can support real-world attribution, not just controlled synthetic validation.",
    },
    {
      item: "two_accepted_real_baselines",
      status: "missing",
      reason: "Needed before the baseline acceptance gate can support real-world attribution.",
    },
    {
      item: "accepted_collection_intake",
      status: "missing",
      reason: "Needed before submitted aggregate artifacts can support real-world attribution claims.",
    },
    {
      item: "bitcoin_nonce_risk_report",
      status: "missing",
      reason: "Needed for wallet/library nonce fingerprint claims.",
    },
  ],
};

const bundledClaimLedger = {
  schema: "primeproject.claim-ledger.v1",
  source: {
    claim_level: "public_demo_only",
    failed_gate_count: 5,
  },
  summary: {
    claim_count: 5,
    allowed_count: 3,
    qualified_count: 0,
    blocked_count: 2,
    public_claim_ceiling: "public_demo_only",
  },
  claims: [
    {
      claim_id: "prime_measure_visualization",
      title: "Prime-measure visualization is reproducible enough for public demo use",
      category: "visualization",
      claim_level: "visual_demo",
      status: "allowed",
      public_statement: "The GitHub Pages visualizations may be described as reproducible exploratory views over bundled/live prime-measure experiments.",
      failed_required_gates: [],
      missing_required_artifacts: [],
    },
    {
      claim_id: "synthetic_generator_attribution",
      title: "Controlled synthetic generator fingerprints are observable",
      category: "controlled_validation",
      claim_level: "controlled_synthetic",
      status: "allowed",
      public_statement: "Synthetic generator families can be compared under controlled experiments, with bit-length confounds explicitly reported.",
      failed_required_gates: [],
      missing_required_artifacts: [],
    },
    {
      claim_id: "real_world_generator_attribution",
      title: "Real-world library generator attribution is supported",
      category: "sim_to_real",
      claim_level: "real_world_candidate",
      status: "blocked",
      public_statement: "Do not claim real-world generator attribution. Current evidence is a scaffold and planning system, not accepted attribution evidence.",
      failed_required_gates: ["real_baseline_gate", "classifier_gate", "baseline_acceptance_gate", "collection_intake_gate"],
      missing_required_artifacts: [],
    },
    {
      claim_id: "bitcoin_nonce_risk_attribution",
      title: "Bitcoin wallet/library nonce-risk attribution is supported",
      category: "bitcoin",
      claim_level: "wallet_nonce_candidate",
      status: "blocked",
      public_statement: "Do not claim Bitcoin wallet/library attribution. Public secp256k1 constants are not the risk surface; nonce metadata evidence is still missing.",
      failed_required_gates: ["bitcoin_integration_gate"],
      missing_required_artifacts: ["bitcoin_risk_report"],
    },
    {
      claim_id: "public_safety_and_reproducibility",
      title: "Public artifact bundle is safe enough to inspect",
      category: "publication",
      claim_level: "publication_scaffold",
      status: "allowed",
      public_statement: "The public bundle can be inspected as a defensive research scaffold with private key material and sensitive prime samples excluded.",
      failed_required_gates: [],
      missing_required_artifacts: [],
    },
  ],
  blocked_claim_ids: ["real_world_generator_attribution", "bitcoin_nonce_risk_attribution"],
};

const bundledArtifactLineage = {
  schema: "primeproject.artifact-lineage.v1",
  summary: {
    node_count: 23,
    edge_count: 53,
    missing_count: 0,
    invalid_edge_count: 0,
    checksum_mismatch_count: 0,
    cycle_count: 0,
    reproducible: true,
  },
  policy: {
    lineage_is_outside_evidence_pack: true,
    reason: "The lineage report audits the evidence pack and claim ledger, so it is generated after them to avoid circular checksums.",
  },
  nodes: [
    { role: "manifest", schema: "primeproject.real-world-baseline-manifest.v1", exists: true, sha256: "fb55fabb2ddf378a3f2a7065cee7bf1d5db1b1eda7ca5c659fddc9e0e037b2c7" },
    { role: "attribution_grid", schema: "primeproject.attribution-confound-grid.v1", exists: true, sha256: "4873f01f4deec22f70c3a98563cd37e0ccbb587313e4d70befebff30e3f12318" },
    { role: "feature_vectors", schema: "primeproject.generator-feature-vectors.v1", exists: true, sha256: "fe1b9e5a443a4159b58bc87eaf10adaad396fe00ffd553439aa8821bbad1d538" },
    { role: "classifier_report", schema: "primeproject.crypto-classifier-report.v1", exists: true, sha256: "970185d874983453e0a2a27562e30d02f1e96826ad55a0216e93b504e3f10663" },
    { role: "claim_language_audit", schema: "primeproject.claim-language-audit.v1", exists: true, sha256: "bundled-fallback" },
    { role: "collection_handoff", schema: "primeproject.collection-handoff.v1", exists: true, sha256: "47e75e611e98837cac5ecc690cc49900a2b757a7b2d857d474988a4406a5f232" },
    { role: "collection_submission_contract", schema: "primeproject.collection-submission-contract.v1", exists: true, sha256: "c298e17b6dfb8779e04c6bff957658723ae5c57486e0a831980e147c1bac364f" },
    { role: "collection_submission_lint", schema: "primeproject.collection-submission-lint.v1", exists: true, sha256: "7ab44e09bc80c5bbe75690f754e406f3e0c3df2d4455bd5b665d2c1538cd3564" },
    { role: "collection_fixture_audit", schema: "primeproject.collection-fixture-audit.v1", exists: true, sha256: "bundled-fallback" },
    { role: "collection_intake", schema: "primeproject.collection-intake.v1", exists: true, sha256: "9179e93a350bcebc96db80f095b4966f5514ae53c9866264d2c8731408d9469b" },
    { role: "readiness", schema: "primeproject.research-readiness.v1", exists: true, sha256: "ed06deee979aa2845454739f1d8e67cdfe4128309b0867835a4d812d1f3e4c53" },
    { role: "evidence_pack", schema: "primeproject.evidence-pack.v1", exists: true, sha256: "bundled-fallback" },
    { role: "claim_ledger", schema: "primeproject.claim-ledger.v1", exists: true, sha256: "bundled-fallback" },
    { role: "null_calibration", schema: "primeproject.null-calibration.v1", exists: true, sha256: "9e71d4fe726202d2a7945aa3b18f28d665a2caea073aa4a1ed0ad0dd91262e40" },
    { role: "replication_audit", schema: "primeproject.replication-audit.v1", exists: true, sha256: "b37b9d357f5a02140ce61570d71aa93f2ad4eb616e7ea208ee447918c1212b1b" },
    { role: "project_evolution", schema: "primeproject.project-evolution.v1", exists: true, sha256: "bundled-fallback" },
  ],
  edges: [
    { from: "manifest", to: "collection_matrix", valid: true },
    { from: "collection_matrix", to: "collection_power", valid: true },
    { from: "manifest", to: "provenance_requirements", valid: true },
    { from: "provenance_requirements", to: "provenance_audit", valid: true },
    { from: "manifest", to: "baseline_acceptance", valid: true },
    { from: "collection_matrix", to: "baseline_acceptance", valid: true },
    { from: "collection_power", to: "baseline_acceptance", valid: true },
    { from: "provenance_audit", to: "baseline_acceptance", valid: true },
    { from: "baseline_acceptance", to: "baseline_promotion_plan", valid: true },
    { from: "baseline_acceptance", to: "collection_handoff", valid: true },
    { from: "baseline_promotion_plan", to: "collection_handoff", valid: true },
    { from: "classifier_report", to: "collection_handoff", valid: true },
    { from: "collection_matrix", to: "collection_handoff", valid: true },
    { from: "collection_power", to: "collection_handoff", valid: true },
    { from: "manifest", to: "collection_handoff", valid: true },
    { from: "provenance_audit", to: "collection_handoff", valid: true },
    { from: "provenance_requirements", to: "collection_handoff", valid: true },
    { from: "collection_handoff", to: "collection_submission_contract", valid: true },
    { from: "collection_submission_contract", to: "collection_submission_lint", valid: true },
    { from: "collection_submission_contract", to: "collection_fixture_audit", valid: true },
    { from: "collection_submission_lint", to: "collection_fixture_audit", valid: true },
    { from: "collection_handoff", to: "collection_intake", valid: true },
    { from: "collection_submission_contract", to: "collection_intake", valid: true },
    { from: "attribution_grid", to: "null_calibration", valid: true },
    { from: "attribution_grid", to: "replication_audit", valid: true },
    { from: "null_calibration", to: "replication_audit", valid: true },
    { from: "attribution_grid", to: "readiness", valid: true },
    { from: "feature_vectors", to: "classifier_report", valid: true },
    { from: "classifier_report", to: "readiness", valid: true },
    { from: "manifest", to: "readiness", valid: true },
    { from: "readiness", to: "evidence_pack", valid: true },
    { from: "baseline_acceptance", to: "evidence_pack", valid: true },
    { from: "baseline_promotion_plan", to: "evidence_pack", valid: true },
    { from: "null_calibration", to: "evidence_pack", valid: true },
    { from: "replication_audit", to: "evidence_pack", valid: true },
    { from: "feature_vectors", to: "evidence_pack", valid: true },
    { from: "classifier_report", to: "evidence_pack", valid: true },
    { from: "claim_language_audit", to: "evidence_pack", valid: true },
    { from: "collection_handoff", to: "evidence_pack", valid: true },
    { from: "collection_submission_contract", to: "evidence_pack", valid: true },
    { from: "collection_submission_lint", to: "evidence_pack", valid: true },
    { from: "collection_fixture_audit", to: "evidence_pack", valid: true },
    { from: "collection_intake", to: "evidence_pack", valid: true },
    { from: "project_evolution", to: "evidence_pack", valid: true },
    { from: "evidence_pack", to: "claim_ledger", valid: true },
  ],
  checksum_checks: [
    { role: "manifest", status: "match" },
    { role: "readiness", status: "match" },
    { role: "project_evolution", status: "match" },
  ],
  findings: [
    {
      severity: "info",
      check: "lineage_reproducible",
      message: "Declared artifacts exist, evidence-pack checksums match, and dependency graph is acyclic.",
    },
  ],
};

const bundledDecisionProtocol = {
  schema: "primeproject.decision-protocol.v1",
  source: {
    claim_level: "public_demo_only",
    lineage_reproducible: true,
  },
  summary: {
    decision_count: 4,
    allowed_count: 2,
    blocked_count: 2,
    qualified_count: 0,
    public_claim_ceiling: "public_demo_only",
  },
  decisions: [
    {
      decision_id: "publish_public_demo",
      title: "Publish public demo and exploratory visualizations",
      track: "publication",
      status: "allowed",
      threshold: "No sensitive material, at least three checksummed artifacts, and acyclic lineage.",
      statement: "Public demo language is allowed when labelled as exploratory visualization.",
      blocking_items: [],
      next_action: "Keep limitations attached and preserve current evidence snapshots.",
    },
    {
      decision_id: "report_controlled_synthetic_signal",
      title: "Report controlled synthetic generator signal",
      track: "controlled-validation",
      status: "allowed",
      threshold: "Controlled attribution grid is present and at least one profile survives bit-length control.",
      statement: "Controlled synthetic attribution may be reported with confound limits attached.",
      blocking_items: [],
      next_action: "Keep limitations attached and preserve current evidence snapshots.",
    },
    {
      decision_id: "promote_real_world_generator_attribution",
      title: "Promote real-world generator attribution claim",
      track: "sim-to-real",
      status: "blocked",
      threshold: "At least two accepted RSA library baselines, complete provenance, accepted collection intake, labelled classifier vectors across at least three labels, and matching evidence-pack checksums.",
      statement: "Real-world generator attribution must remain a blocked claim.",
      blocking_items: ["gate:real_baseline_gate", "gate:classifier_gate", "gate:baseline_acceptance_gate", "gate:collection_intake_gate", "claim:real_world_generator_attribution:blocked"],
      next_action: "Collect accepted OpenSSL/BoringSSL aggregate baselines, pass collection intake, complete provenance, and export labelled classifier vectors.",
    },
    {
      decision_id: "promote_bitcoin_nonce_risk_attribution",
      title: "Promote Bitcoin wallet/library nonce-risk attribution claim",
      track: "bitcoin",
      status: "blocked",
      threshold: "A bundled Bitcoin nonce-risk report exists and is linked to wallet/library baseline metadata.",
      statement: "Bitcoin attribution must stay blocked until nonce-risk evidence is bundled.",
      blocking_items: ["gate:bitcoin_integration_gate", "artifact:bitcoin_risk_report", "claim:bitcoin_nonce_risk_attribution:blocked"],
      next_action: "Bundle a public-safe Bitcoin nonce-risk report from owned or public metadata summaries.",
    },
  ],
};

const bundledFalsificationBattery = {
  schema: "primeproject.falsification-battery.v1",
  source: {
    random_baseline_accuracy: 1 / 3,
    controlled_profiles: ["all", "gap_only"],
  },
  summary: {
    check_count: 5,
    pass_count: 5,
    warn_count: 0,
    fail_count: 0,
    claim_floor: "controlled_synthetic_only",
    interpretation:
      "Falsification battery supports controlled synthetic reporting only; real-world promotion stays blocked.",
  },
  downgrade_triggers: [
    "missing_paired_controls",
    "bit_length_only_survives_control",
    "negative_controls_exceed_floor",
    "decision_protocol_promotes_blocked_claim",
    "real_world_or_bitcoin_claim_without_bundled_evidence",
  ],
  checks: [
    {
      check: "paired_control_presence",
      status: "pass",
      severity: "critical",
      message: "Paired uncontrolled and bit-length-controlled attribution rows are present.",
      evidence: { control_modes: ["bit_length", "none"] },
    },
    {
      check: "controlled_signal_above_random",
      status: "pass",
      severity: "high",
      message: "At least one nontrivial profile remains above random after bit-length control.",
      evidence: { profiles: ["all", "gap_only"], minimum_lift: 0.1 },
    },
    {
      check: "bit_length_confound_guard",
      status: "pass",
      severity: "critical",
      message: "The bit-length-only profile collapses near random after control.",
      evidence: { bit_length_only_controlled_accuracy: 0.333333 },
    },
    {
      check: "negative_control_floor",
      status: "pass",
      severity: "medium",
      message: "Low-bit and residue-only controls remain near the random floor.",
      evidence: { floor: 0.533333, exceeding: [] },
    },
    {
      check: "claim_promotion_guard",
      status: "pass",
      severity: "critical",
      message: "Real-world and Bitcoin attribution promotion remain blocked until required evidence exists.",
      evidence: {
        required_blocked_decisions: [
          "promote_real_world_generator_attribution",
          "promote_bitcoin_nonce_risk_attribution",
        ],
      },
    },
  ],
};

const bundledPublicationConsistency = {
  schema: "primeproject.publication-consistency.v1",
  source: {
    claim_level: "public_demo_only",
    falsification_claim_floor: "controlled_synthetic_only",
  },
  summary: {
    status: "pass",
    check_count: 6,
    pass_count: 6,
    warn_count: 0,
    fail_count: 0,
    high_risk_claims_blocked: true,
    high_risk_decisions_blocked: true,
  },
  policy: {
    post_pack_audit: true,
    reason:
      "This consistency report consumes the evidence pack, claim ledger, decision protocol, and falsification battery after those artifacts are generated.",
  },
  checks: [
    {
      check: "generated_at_alignment",
      status: "pass",
      severity: "high",
      message: "Publication governance artifacts share the same generated_at timestamp.",
      evidence: { unique_generated_at: ["2026-05-24T16:56:40+00:00"], missing_generated_at: [] },
    },
    {
      check: "real_world_boundary_consistent",
      status: "pass",
      severity: "critical",
      message: "Real-world attribution is blocked by matching evidence, ledger, decision, and missing-evidence signals.",
      evidence: {
        missing_required_evidence: [
          "two_available_real_baselines",
          "real_world_labelled_feature_vectors",
          "two_accepted_real_baselines",
          "accepted_collection_intake",
        ],
      },
    },
    {
      check: "bitcoin_boundary_consistent",
      status: "pass",
      severity: "critical",
      message: "Bitcoin nonce-risk attribution is blocked consistently until a bundled risk report exists.",
      evidence: { required_evidence_status: "missing" },
    },
    {
      check: "decision_claim_alignment",
      status: "pass",
      severity: "critical",
      message: "No decision promotes a claim that the claim ledger blocks.",
      evidence: { contradictions: [] },
    },
    {
      check: "falsification_guard_alignment",
      status: "pass",
      severity: "critical",
      message: "The falsification guard agrees that high-risk attribution decisions remain blocked.",
      evidence: { claim_promotion_guard_status: "pass" },
    },
    {
      check: "required_evidence_covers_blockers",
      status: "pass",
      severity: "high",
      message: "Every high-risk failed gate has a matching required-evidence item.",
      evidence: { missing_explanations: [] },
    },
  ],
};

const bundledProjectEvolution = {
  schema: "primeproject.project-evolution.v1",
  headline: "From prime regularity exploration to generator-fingerprint research tooling.",
  metrics: {
    live_compute_limit: 10000000,
    precomputed_snapshot_limits: [1000000, 10000000],
    registered_real_baselines: 5,
    available_real_baselines: 0,
    manifest_available_baselines: 1,
    public_control_baselines: 1,
    collection_targets: 10,
    collection_complete_targets: 0,
    collection_power_strong_targets: 1,
    collection_power_coarse_targets: 9,
    provenance_rows: 4,
    provenance_missing_required: 35,
    provenance_audit_blocked_rows: 4,
    provenance_audit_forbidden_fields: 0,
    baseline_acceptance_rows: 10,
    baseline_acceptance_accepted: 0,
    baseline_acceptance_blocked: 10,
    promotion_minimal_unlock_targets: 2,
    promotion_projected_samples: 9028,
    submission_contract_tasks: 10,
    submission_contract_required_fields: 7,
    submission_contract_scalar_features: 14,
    submission_lint_tasks: 10,
    submission_lint_submitted: 0,
    submission_lint_blocked: 0,
    submission_lint_waiting: 10,
    submission_fixture_cases: 10,
    submission_fixture_expectation_failures: 0,
    submission_fixture_public_safe: 10,
    intake_tasks: 10,
    intake_submitted: 0,
    intake_accepted: 0,
    intake_blocked: 10,
    intake_p0_blocked: 2,
    intake_feature_vector_contract_blocked: 0,
    attribution_grid_rows: 48,
    attribution_repeats: 3,
    robust_controlled_profiles: ["all", "gap_only"],
    classifier_vector_count: 12,
    classifier_label_count: 3,
    classifier_accuracy: 1 / 3,
    classifier_claim_scope: "controlled_synthetic_only",
    publication_claim_level: "public_demo_only",
    checksummed_artifacts: 21,
    claim_language_scanned_files: 19,
    claim_language_scanned_lines: 11697,
    claim_language_triggered_mentions: 117,
    claim_language_guarded_mentions: 117,
    claim_language_failures: 0,
    blocking_gaps: 2,
    claim_ledger_allowed: 3,
    claim_ledger_blocked: 2,
    lineage_nodes: 24,
    lineage_edges: 54,
    lineage_checksum_mismatches: 0,
    lineage_cycles: 0,
    decision_protocol_allowed: 2,
    decision_protocol_blocked: 2,
    falsification_checks: 5,
    falsification_failures: 0,
    falsification_claim_floor: "controlled_synthetic_only",
    publication_consistency_checks: 6,
    publication_consistency_failures: 0,
    publication_consistency_status: "pass",
    publication_guard_artifacts: 6,
    publication_guard_checks: 11,
    null_calibration_iterations: 5000,
    null_familywise_survivors: 2,
    null_top_profile: "gap_only",
    replication_setting_count: 8,
    replication_stable_profiles: 2,
  },
  change_dashboard: {
    headline:
      "PrimeProject moved from exploratory prime regularity visuals into publication-gated real-world generator fingerprint tooling.",
    maturity_ladder: [
      { stage: "Explore", phase_ids: ["regularity-plan", "conjecture-lab", "static-snapshots"], status: "complete", signal: "10M browser compute and static snapshots" },
      { stage: "Fingerprint", phase_ids: ["fingerprint-baseline", "attribution-grid", "null-calibration", "replication-audit", "crypto-classifier"], status: "complete", signal: "controlled attribution, null calibration, 8-setting replication audit, and scoped classifier baseline" },
      { stage: "Sim-to-Real", phase_ids: ["real-world-registry", "collection-matrix", "collection-power", "collection-handoff", "collection-submission-contract", "collection-submission-lint", "collection-fixture-audit", "collection-intake"], status: "active", signal: "OpenSSL/BoringSSL/Go/Bitcoin collection targets, sample-power floors, handoff, submission contract, fixture audit, pre-intake lint, and intake validation" },
      { stage: "Govern", phase_ids: ["provenance-gate", "provenance-audit", "baseline-acceptance", "baseline-promotion", "collection-handoff", "collection-submission-contract", "collection-submission-lint", "collection-fixture-audit", "collection-intake"], status: "active", signal: "provenance, acceptance, promotion, handoff, submission-contract, lint-fixture, and intake gates before claims" },
      { stage: "Publish", phase_ids: ["readiness-gates", "claim-language-audit", "evidence-pack", "claim-ledger", "artifact-lineage", "decision-protocol", "falsification-battery", "publication-consistency"], status: "active", signal: "5 falsification checks, 6 consistency checks, and controlled-synthetic-only claim floor" },
    ],
    visual_rollup: {
      headline: "Visible change history: exploration scale, controlled signal, sim-to-real gates, and publication guardrails.",
      release_trail: [
        { marker: "01", title: "Prime regularity demo", state: "complete", measure: "browser experiment", proof: "interactive gap, residue, and next-prime measure views" },
        { marker: "02", title: "Scale lift", state: "complete", measure: "10M live + 1M/10M snapshots", proof: "larger local runs are visible on GitHub Pages without recomputation" },
        { marker: "03", title: "Controlled attribution", state: "complete", measure: "48 rows / 5,000 null iterations / 8 replication settings", proof: "signal must survive bit-length control, null calibration, and replication" },
        { marker: "04", title: "Sim-to-real gates", state: "blocked", measure: "10 targets / 9,028 P0 samples left", proof: "OpenSSL/BoringSSL/Go/Bitcoin baselines are registered but not accepted" },
        { marker: "05", title: "Publication guardrails", state: "guarded", measure: "21 checked artifacts / 15 gates / 11 guard checks", proof: "claim-language audit, claim ledger, lineage, decision protocol, falsification battery, and consistency audit prevent overclaiming" },
        { marker: "06", title: "Proof route pruning", state: "open", measure: "5/5 scalar clause-rank grammars refuted at 28 bits", proof: "TICKET-46 turns the Collatz scalar-rank route into a restricted no-go result, not a conjecture proof" },
        { marker: "07", title: "Stateful lasso pruning", state: "open", measure: "5/5 bounded suffix-memory repairs refuted", proof: "TICKET-47 extracts a 16-edge positive-debt lasso and blocks zero-memory through last-4 edge-memory repairs" },
        { marker: "08", title: "Automaton reachability split", state: "open", measure: "9 finite-state rows / 4 starts / 0 full periods", proof: "TICKET-48 blocks fixed finite total state repairs over the abstract lasso and isolates concrete reachability as the next theorem" },
        { marker: "09", title: "Preimage obstruction isolated", state: "open", measure: "dead step 3 / next_valuation 5 vs 1", proof: "TICKET-49 identifies the first local coordinate that blocks the concrete Collatz lasso prefix" },
        { marker: "10", title: "Phase-lift exception promoted", state: "open", measure: "32-bit: 69,092 starts / 8,684 exceptions / depth 15", proof: "TICKET-50 refutes the local all-phase obstruction and promotes two near-lasso witnesses instead" },
        { marker: "11", title: "Terminal lift closed", state: "open", measure: "2 roots / 4 terminal branches / 0 survivors", proof: "TICKET-51 closes both depth-15 near-lasso ancestries at phase 15 without claiming Collatz" },
        { marker: "12", title: "48-bit frontier exposed", state: "open", measure: "83.4B words / 1 sampled depth-15 root / 0 survivors", proof: "TICKET-52 finds and terminally closes one new 48-bit near-lasso witness while proving blind enumeration is no longer viable" },
        { marker: "13", title: "Terminal theorem isolated", state: "open", measure: "3 roots / high branch v=9 / 0 terminal matches", proof: "TICKET-53 refutes the extracted phase-15 lasso family by a symbolic low/high terminal mismatch theorem" },
        { marker: "14", title: "Next family extracted", state: "open", measure: "69,090 remaining starts / max depth 5 / 4,372 phase-5 gates", proof: "TICKET-54 removes the terminal family and identifies Phase5ValuationGate as the strongest remaining bounded Collatz family" },
        { marker: "15", title: "Gate tunnel closed", state: "open", measure: "3 gate crossers / 3 tunnels / 0 terminal target matches", proof: "TICKET-55 proves the extracted phase-5 gate crossers tunnel into the TICKET53 terminal no-go" },
        { marker: "16", title: "Projection escape isolated", state: "open", measure: "69,092 exact starts / 1 sampled projection escape", proof: "TICKET-56 closes the exact 32-bit lasso partition but refutes simple projection-closure globalization" },
        { marker: "17", title: "Boundary state obstruction", state: "open", measure: "2^28 first deterministic / 0 full replays", proof: "TICKET-57 shows exact32 outcomes need affine boundary coordinates and finds no full-period replay among known near-lasso roots" },
        { marker: "18", title: "Lift stability refuted", state: "open", measure: "3,086 projection escapes / 70 lift mismatches", proof: "TICKET-58 replays the deterministic 48-bit sample and refutes unchanged exact32 affine-boundary lifting" },
        { marker: "19", title: "Cylinder coordinate gap", state: "open", measure: "41,472 extensions / 58 mixed cylinders / 0 full periods", proof: "TICKET-59 turns sampled lift mismatches into counted low40-to-48 cylinders and shows low40 is still not a complete coordinate" },
        { marker: "20", title: "Failure-offset separator", state: "open", measure: "58 mixed cylinders / 210 lifts / first joint separator", proof: "TICKET-60 finds low40 + failure_offset separates selected mixed cylinders but remains replay-derived" },
      ],
      evidence_flow: [
        { stage: "Explore", score: 100, status: "complete", evidence: "10M compute and static snapshots" },
        { stage: "Controlled signal", score: 100, status: "complete", evidence: "null-calibrated, replicated synthetic generator fingerprints" },
        { stage: "Real baseline", score: 0, status: "blocked", evidence: "0 accepted RSA library baselines" },
        { stage: "Intake contract", score: 0, status: "blocked", evidence: "10 task templates; 10 lint fixtures pass expectations; 0 submitted artifacts" },
        { stage: "Publish claims", score: 60, status: "guarded", evidence: "public_demo_only; real-world and Bitcoin attribution blocked" },
      ],
      hardening_map: [
        { step: "01", layer: "Task provenance", risk: "Submitted provenance can name the wrong baseline or library.", guard: "provenance_record must match task baseline_id and library.", evidence: "provenance_baseline_id_mismatch fixture", status: "blocked" },
        { step: "02", layer: "Feature label", risk: "A feature vector can be labelled as a different generator family.", guard: "feature_vector_summary.label must match the task library.", evidence: "feature_vector_label_mismatch fixture", status: "blocked" },
        { step: "03", layer: "Record identity", risk: "Top-level baseline/library fields can contradict the task.", guard: "Optional record identity fields must match the task when present.", evidence: "record_baseline_id_mismatch fixture", status: "blocked" },
        { step: "04", layer: "Public path", risk: "A public artifact can leak local paths, URLs, or parent traversal.", guard: "feature_vector_path must be a public relative path.", evidence: "feature_vector_path_public_relative fixture", status: "blocked" },
        { step: "05", layer: "Fixture replay", risk: "Lint behavior can drift after contract changes.", guard: "10 public-safe fixtures replay pass/warn/block boundaries before intake.", evidence: "10 fixtures, 0 expectation failures", status: "guarded" },
      ],
      evidence_spine: [
        { layer: "Scale", score: 100, status: "complete", artifacts: ["data/snapshots/manifest.json", "assets/snapshots/*.svg"], gate: "10M live compute plus 1M/10M static snapshots", proof: "The original browser experiment is now backed by larger reproducible local snapshots." },
        { layer: "Signal", score: 100, status: "complete", artifacts: ["data/attribution_confound_grid.json", "data/null_calibration.json", "data/replication_audit.json"], gate: "48 grid rows, 5,000 null iterations, 8 replication settings", proof: "Generator-fingerprint claims are limited to controlled synthetic evidence that survives confound checks." },
        { layer: "Sim-to-Real", score: 35, status: "blocked", artifacts: ["data/collection_handoff.json", "data/collection_submission_contract.json", "data/collection_fixture_audit.json", "data/collection_intake.json"], gate: "10 targets, 10 public-safe fixtures, 0 accepted real submissions", proof: "OpenSSL/BoringSSL/Go/Bitcoin collection is specified and lint-tested, but real aggregate baselines are not accepted yet." },
        { layer: "Governance", score: 65, status: "guarded", artifacts: ["data/provenance_requirements.json", "data/provenance_audit.json", "data/baseline_acceptance.json", "data/baseline_promotion_plan.json"], gate: "0 accepted baselines, 4 provenance rows blocked, 9,028 P0 samples projected", proof: "The project now states exactly why stronger real-world claims remain blocked." },
        { layer: "Publication", score: 80, status: "guarded", artifacts: ["data/evidence_pack.json", "data/open_problem_workbench.json", "data/claim_language_audit.json", "data/claim_ledger.json", "data/artifact_lineage.json", "data/decision_protocol.json", "data/falsification_battery.json", "data/publication_consistency.json"], gate: "21 checked artifacts, 15 gates, 24 lineage nodes, 11 guard checks", proof: "Public statements are constrained by claim-language audit, checksums, lineage, decision rules, falsification guards, and consistency checks." },
        { layer: "Open-Proof", score: 60, status: "open", artifacts: ["data/open-problem/ticket46-stable-clause-grammar-lab.json", "data/open-problem/ticket47-periodic-state-lasso-lab.json", "data/open-problem/ticket48-automaton-reachability-lab.json", "data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json", "data/open-problem/ticket50-phase-lift-exception-lab.json", "data/open-problem/ticket51-phase15-terminal-lift-lab.json", "data/open-problem/ticket52-frontier-budget-lab.json", "data/open-problem/ticket53-symbolic-terminal-theorem-lab.json", "data/open-problem/ticket54-new-template-family-lab.json", "data/open-problem/ticket55-phase5-valuation-gate-lab.json", "data/open-problem/ticket56-pre-gate-projection-escape-lab.json", "data/open-problem/ticket57-parametric-template-automaton-lab.json", "data/open-problem/ticket58-affine-boundary-lift-lab.json", "data/open-problem/ticket59-symbolic-lift-mismatch-lab.json", "data/open-problem/ticket60-mixed-cylinder-separator-lab.json", "docs/proof-or-counterexample-program.md"], gate: "The selected mixed cylinders separate under failure_offset, but that coordinate is replay-derived; no full proof claim", proof: "The proof workbench now targets a symbolic failure-offset predictor or automaton-counted cover." },
      ],
    },
    latest_changes: [
      { label: "Scale evidence", impact: "The browser demo is now backed by 10M live compute plus static 1M/10M snapshots.", metric: "10M live / 2 snapshots" },
      { label: "Controlled signal", impact: "Synthetic generator fingerprints must survive bit-length controls, null calibration, and replication before they count.", metric: "48 rows / 5,000 null / 8 settings" },
      { label: "Real-world gate", impact: "OpenSSL/BoringSSL/Go/Bitcoin targets are registered, but attribution remains blocked until accepted aggregate baselines arrive.", metric: "0 accepted / 10 blocked" },
      { label: "Submission discipline", impact: "Collection contract, lint fixtures, and intake validation define exactly what public-safe evidence must contain.", metric: "10 templates / 10 fixtures" },
      { label: "Publication guardrail", impact: "Claim-language audit, claim ledger, lineage, decision rules, falsification checks, and consistency checks keep the public page at demo/scaffold claim strength.", metric: "21 artifacts / 11 guard checks" },
      { label: "Proof route pruning", impact: "TICKET-46 refutes all five tested Collatz scalar clause-rank grammars at 28 bits, so the remaining target is an ordinal/stateful infinite bridge.", metric: "5 refuted / 0 stable" },
      { label: "Stateful lasso pruning", impact: "TICKET-47 refutes bounded suffix-memory repairs on a 16-edge positive-debt pressure lasso; arbitrary automaton CEGIS and reachability remain open.", metric: "16-edge lasso / 5 memory repairs" },
      { label: "Automaton reachability split", impact: "TICKET-48 refutes fixed finite total state repairs over the abstract lasso and shows the bounded concrete probe reaches only two positive steps, not a full lasso period.", metric: "9 rows / 4 starts / 2 steps" },
      { label: "Preimage obstruction isolated", impact: "TICKET-49 classifies the first concrete lasso-prefix failure as a next_valuation mismatch: the unique two-step survivor reaches 5 where the lasso requires 1.", metric: "dead step 3 / 5 != 1" },
      { label: "Phase-lift exception promoted", impact: "TICKET-50 refutes the TICKET-49 all-phase obstruction candidate at 32 bits and promotes two depth-15 near-lasso residues as the next terminal-lift targets.", metric: "69,092 / 8,684 / depth 15" },
      { label: "Terminal lift closed", impact: "TICKET-51 opens all low/high terminal branches for the two TICKET-50 near-lasso roots and finds zero full-lasso completions.", metric: "2 roots / 4 branches / 0 survivors" },
      { label: "48-bit frontier exposed", impact: "TICKET-52 quantifies the 48-bit valuation frontier, finds one new sampled depth-15 near-lasso root outside the closed ancestry, and terminally closes it.", metric: "83.4B words / 1 root / 0 survivors" },
      { label: "Terminal theorem isolated", impact: "TICKET-53 turns the repeated phase-15 failure into a symbolic low/high branch mismatch theorem for the extracted lasso family.", metric: "3 roots / v_high=9 / 0 matches" },
      { label: "Next family extracted", impact: "TICKET-54 removes the TICKET53 terminal family and shows the exact 32-bit post-discard frontier drops to max depth 5 at the Phase5ValuationGate.", metric: "69,090 remain / 4,372 gates" },
      { label: "Gate tunnel closed", impact: "TICKET-55 shows every known phase-5 gate crosser preserves the same pending valuation through phase 14 and then hits the TICKET53 terminal no-go.", metric: "3 gate / 3 tunnel / 0 target" },
      { label: "Projection escape isolated", impact: "TICKET-56 closes the exact 32-bit start-template lasso partition, then discards simple projection closure because a sampled 48-bit depth-15 witness projects outside the 32-bit model.", metric: "69,092 exact / 1 escape" },
      { label: "Boundary state obstruction", impact: "TICKET-57 shows the exact32 partition is not governed by template-only automata: 2^26 boundary still has 92 collisions, while 2^28 first becomes deterministic and known roots have 0 full-period replays.", metric: "2^28 boundary / 0 replay" },
      { label: "Lift stability refuted", impact: "TICKET-58 replays the deterministic 48-bit sample and shows unchanged exact32 affine-boundary lifting fails: 3,086 projection escapes and 70 projection-target outcome mismatches.", metric: "3,086 escape / 70 mismatch" },
      { label: "Cylinder coordinate gap", impact: "TICKET-59 exhaustively enumerates 162 selected low40-to-48 cylinders, strengthening the mismatch evidence while showing low40 leaves 58 mixed-outcome cylinders.", metric: "41,472 extensions / 58 mixed" },
      { label: "Failure-offset separator", impact: "TICKET-60 shows low40 plus failure_offset deterministically separates the selected mixed cylinders, turning the next target into a symbolic predictor for that offset.", metric: "58 mixed / 210 lifts" },
    ],
    research_delta: {
      headline: "What changed from the original prime-regularity demo to the current research scaffold.",
      claim_state: {
        before: "Exploratory prime regularity visualization with synthetic generator intuition.",
        current: "Controlled synthetic fingerprint evidence is null-calibrated and replication-audited, while real-world and Bitcoin attribution remain gated.",
        next: "Accepted OpenSSL/BoringSSL/Go baselines plus labelled classifier vectors are required before real-world attribution claims can move.",
      },
      tracks: [
        { track: "Scale", before: "300K-style browser exploration", current: "10M live compute and 1M/10M static snapshots", state: "complete" },
        { track: "Signal", before: "Residue and gap visual drift", current: "48-row attribution grid, 5,000 null iterations, 8-setting replication audit, 12 classifier vectors", state: "complete" },
        { track: "Reality", before: "No real-world generator baseline gate", current: "5 registered baseline families, 10 collection targets, 10 handoff tasks, 10 submission templates, pre-intake lint, 10 fixture cases, 10 intake blockers, 0 accepted baselines", state: "blocked" },
        { track: "Publication", before: "Informal narrative claims", current: "22 checksummed artifacts, claim-language audit, open-problem certificates, claim ledger, lineage DAG, decision protocol, falsification battery, consistency audit", state: "guarded" },
        { track: "Open proof search", before: "Scalar rank and symbolic clause candidates could still look plausible on bounded horizons.", current: "TICKET-46 refutes 5/5 tested finite template-local scalar clause-rank grammars; TICKET-47 refutes bounded suffix-memory repairs; TICKET-48 refutes fixed finite total state repairs over the abstract lasso; TICKET-49 localizes the first concrete prefix failure to next_valuation; TICKET-50 refutes that obstruction's all-phase extension; TICKET-51 closes the two known depth-15 near-lasso roots at phase 15; TICKET-52 finds a new sampled 48-bit depth-15 root and closes it; TICKET-53 explains all known terminal closures by a symbolic mismatch theorem and discards the extracted lasso family; TICKET-54 extracts Phase5ValuationGate as the strongest remaining bounded family; TICKET-55 proves the known gate crossers tunnel into the terminal no-go; TICKET-56 closes the exact 32-bit partition but refutes simple projection-closure globalization; TICKET-57 shows exact32 outcomes need affine boundary coordinates; TICKET-58 refutes unchanged exact32 affine-boundary lifting in the replayed 48-bit sample; TICKET-59 counts selected low40-to-48 cylinders and shows the next missing coordinate is inside mixed cylinders; TICKET-60 identifies failure_offset as the first deterministic separator but leaves symbolic prediction open.", state: "open" },
      ],
      claim_lanes: [
        { claim: "Public demo", status: "allowed", basis: "safe public artifact bundle" },
        { claim: "Controlled synthetic signal", status: "allowed", basis: "controlled grid + null + replication + scoped classifier" },
        { claim: "Real-world generator attribution", status: "blocked", basis: "accepted baselines and classifier vectors missing" },
        { claim: "Bitcoin wallet/library attribution", status: "blocked", basis: "nonce-risk report and wallet baseline metadata missing" },
      ],
    },
  },
  phases: [
    { id: "regularity-plan", label: "Prime regularity plan", status: "complete", layer: "theory" },
    { id: "conjecture-lab", label: "Interactive Conjecture Lab", status: "complete", layer: "visualization" },
    { id: "static-snapshots", label: "10M research snapshots", status: "complete", layer: "evidence" },
    { id: "bitcoin-track", label: "Bitcoin defensive track", status: "complete", layer: "crypto" },
    { id: "fingerprint-baseline", label: "Generator fingerprint baseline", status: "complete", layer: "analysis" },
    { id: "attribution-grid", label: "Controlled attribution grid", status: "complete", layer: "validation" },
    { id: "null-calibration", label: "Null calibration", status: "complete", layer: "statistics" },
    { id: "replication-audit", label: "Replication audit", status: "complete", layer: "statistics" },
    { id: "crypto-classifier", label: "Crypto-classifier baseline", status: "active", layer: "analysis" },
    { id: "real-world-registry", label: "Real-world baseline registry", status: "scaffolded", layer: "sim-to-real" },
    { id: "collection-matrix", label: "Real-world collection matrix", status: "active", layer: "sim-to-real" },
    { id: "collection-power", label: "Sample power calibration", status: "active", layer: "statistics" },
    { id: "provenance-gate", label: "Provenance requirements", status: "active", layer: "governance" },
    { id: "provenance-audit", label: "Provenance audit", status: "active", layer: "governance" },
    { id: "baseline-acceptance", label: "Baseline acceptance", status: "active", layer: "publication" },
    { id: "baseline-promotion", label: "Promotion plan", status: "active", layer: "planning" },
    { id: "collection-handoff", label: "Collection handoff", status: "active", layer: "sim-to-real" },
    { id: "collection-submission-contract", label: "Submission contract", status: "active", layer: "sim-to-real" },
    { id: "collection-submission-lint", label: "Submission lint", status: "active", layer: "sim-to-real" },
    { id: "collection-fixture-audit", label: "Fixture audit", status: "active", layer: "validation" },
    { id: "collection-intake", label: "Collection intake", status: "active", layer: "sim-to-real" },
    { id: "readiness-gates", label: "Research readiness scoring", status: "active", layer: "governance" },
    { id: "evidence-pack", label: "Evidence pack gates", status: "active", layer: "publication" },
    { id: "claim-language-audit", label: "Claim-language audit", status: "active", layer: "publication" },
    { id: "claim-ledger", label: "Claim ledger", status: "active", layer: "publication" },
    { id: "artifact-lineage", label: "Artifact lineage", status: "active", layer: "reproducibility" },
    { id: "decision-protocol", label: "Decision protocol", status: "active", layer: "governance" },
    { id: "falsification-battery", label: "Falsification battery", status: "active", layer: "validation" },
    { id: "publication-consistency", label: "Publication consistency", status: "active", layer: "publication" },
  ],
  connections: [
    ["regularity-plan", "conjecture-lab"],
    ["conjecture-lab", "static-snapshots"],
    ["conjecture-lab", "fingerprint-baseline"],
    ["bitcoin-track", "real-world-registry"],
    ["fingerprint-baseline", "attribution-grid"],
    ["attribution-grid", "null-calibration"],
    ["null-calibration", "replication-audit"],
    ["replication-audit", "crypto-classifier"],
    ["crypto-classifier", "readiness-gates"],
    ["replication-audit", "readiness-gates"],
    ["null-calibration", "readiness-gates"],
    ["attribution-grid", "readiness-gates"],
    ["real-world-registry", "collection-matrix"],
    ["collection-matrix", "collection-power"],
    ["collection-power", "provenance-gate"],
    ["provenance-gate", "provenance-audit"],
    ["provenance-audit", "baseline-acceptance"],
    ["baseline-acceptance", "baseline-promotion"],
    ["baseline-promotion", "collection-handoff"],
    ["collection-handoff", "collection-submission-contract"],
    ["collection-submission-contract", "collection-submission-lint"],
    ["collection-submission-lint", "collection-fixture-audit"],
    ["collection-fixture-audit", "collection-intake"],
    ["collection-intake", "readiness-gates"],
    ["claim-language-audit", "evidence-pack"],
    ["collection-intake", "evidence-pack"],
    ["readiness-gates", "evidence-pack"],
    ["evidence-pack", "claim-ledger"],
    ["evidence-pack", "artifact-lineage"],
    ["claim-ledger", "decision-protocol"],
    ["artifact-lineage", "decision-protocol"],
    ["attribution-grid", "falsification-battery"],
    ["decision-protocol", "falsification-battery"],
    ["falsification-battery", "publication-consistency"],
    ["evidence-pack", "publication-consistency"],
    ["claim-ledger", "publication-consistency"],
  ],
  open_gaps: [
    { priority: "P0", track: "sim-to-real", gap: "Need at least two available aggregate generator baselines before real attribution claims." },
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
  dataSourceBadge: document.querySelector("#dataSourceBadge"),
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
  evolutionImpact: document.querySelector("#evolutionImpact"),
  evolutionSpine: document.querySelector("#evolutionSpine"),
  evolutionDelta: document.querySelector("#evolutionDelta"),
  evolutionMap: document.querySelector("#evolutionMap"),
  evolutionTimeline: document.querySelector("#evolutionTimeline"),
  evolutionGaps: document.querySelector("#evolutionGaps"),
  atlasHero: document.querySelector("#atlasHero"),
  atlasContributionGrid: document.querySelector("#atlasContributionGrid"),
  atlasEvidenceLadder: document.querySelector("#atlasEvidenceLadder"),
  atlasProofGrid: document.querySelector("#atlasProofGrid"),
  atlasNextSteps: document.querySelector("#atlasNextSteps"),
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
  baselineAcceptanceStatus: document.querySelector("#baselineAcceptanceStatus"),
  baselineAcceptanceSummary: document.querySelector("#baselineAcceptanceSummary"),
  baselineAcceptanceRows: document.querySelector("#baselineAcceptanceRows"),
  baselinePromotionStatus: document.querySelector("#baselinePromotionStatus"),
  baselinePromotionSummary: document.querySelector("#baselinePromotionSummary"),
  baselinePromotionRows: document.querySelector("#baselinePromotionRows"),
  collectionHandoffStatus: document.querySelector("#collectionHandoffStatus"),
  collectionHandoffSummary: document.querySelector("#collectionHandoffSummary"),
  collectionHandoffRows: document.querySelector("#collectionHandoffRows"),
  collectionHandoffContract: document.querySelector("#collectionHandoffContract"),
  collectionSubmissionContractStatus: document.querySelector("#collectionSubmissionContractStatus"),
  collectionSubmissionContractSummary: document.querySelector("#collectionSubmissionContractSummary"),
  collectionSubmissionContractRows: document.querySelector("#collectionSubmissionContractRows"),
  collectionSubmissionLintStatus: document.querySelector("#collectionSubmissionLintStatus"),
  collectionSubmissionLintSummary: document.querySelector("#collectionSubmissionLintSummary"),
  collectionSubmissionLintRows: document.querySelector("#collectionSubmissionLintRows"),
  collectionFixtureAuditStatus: document.querySelector("#collectionFixtureAuditStatus"),
  collectionFixtureAuditSummary: document.querySelector("#collectionFixtureAuditSummary"),
  collectionFixtureAuditRows: document.querySelector("#collectionFixtureAuditRows"),
  collectionIntakeStatus: document.querySelector("#collectionIntakeStatus"),
  collectionIntakeSummary: document.querySelector("#collectionIntakeSummary"),
  collectionIntakeRows: document.querySelector("#collectionIntakeRows"),
  readinessSummary: document.querySelector("#readinessSummary"),
  readinessDimensions: document.querySelector("#readinessDimensions"),
  readinessActions: document.querySelector("#readinessActions"),
  classifierStatus: document.querySelector("#classifierStatus"),
  classifierSummary: document.querySelector("#classifierSummary"),
  classifierLabels: document.querySelector("#classifierLabels"),
  evidenceSummary: document.querySelector("#evidenceSummary"),
  evidenceGateRows: document.querySelector("#evidenceGateRows"),
  evidenceArtifactRows: document.querySelector("#evidenceArtifactRows"),
  requiredEvidenceRows: document.querySelector("#requiredEvidenceRows"),
  claimLedgerSummary: document.querySelector("#claimLedgerSummary"),
  claimLedgerRows: document.querySelector("#claimLedgerRows"),
  artifactLineageSummary: document.querySelector("#artifactLineageSummary"),
  artifactLineageMap: document.querySelector("#artifactLineageMap"),
  artifactLineageRows: document.querySelector("#artifactLineageRows"),
  decisionProtocolSummary: document.querySelector("#decisionProtocolSummary"),
  decisionProtocolRows: document.querySelector("#decisionProtocolRows"),
  falsificationSummary: document.querySelector("#falsificationSummary"),
  falsificationRows: document.querySelector("#falsificationRows"),
  publicationConsistencySummary: document.querySelector("#publicationConsistencySummary"),
  publicationConsistencyRows: document.querySelector("#publicationConsistencyRows"),
  attributionSummary: document.querySelector("#attributionSummary"),
  attributionGridSvg: document.querySelector("#attributionGridSvg"),
  attributionProfileRows: document.querySelector("#attributionProfileRows"),
  nullCalibrationSummary: document.querySelector("#nullCalibrationSummary"),
  nullCalibrationRows: document.querySelector("#nullCalibrationRows"),
  replicationAuditSummary: document.querySelector("#replicationAuditSummary"),
  replicationAuditRows: document.querySelector("#replicationAuditRows"),
};

function renderDataSourceBadge() {
  if (!outputs.dataSourceBadge) return;
  const isFileMode = window.location.protocol === "file:";
  const i18n = window.PrimeProjectI18n;
  outputs.dataSourceBadge.textContent = i18n
    ? i18n.t(isFileMode ? "top.offline" : "top.public")
    : isFileMode
      ? "Offline fallback data"
      : "Public JSON data";
  outputs.dataSourceBadge.classList.toggle("is-fallback", isFileMode);
  outputs.dataSourceBadge.classList.toggle("is-public", !isFileMode);
  outputs.dataSourceBadge.title = isFileMode
    ? "Direct file mode cannot fetch the public data/*.json bundle; panels use embedded fallback constants."
    : "Panels are loaded through the public data/*.json artifact bundle used by GitHub Pages.";
}

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

window.addEventListener("primeproject:languagechange", renderDataSourceBadge);

runExperiment();
renderDataSourceBadge();
loadSnapshots();
loadProjectEvolution();
loadRealBaselineManifest();
loadCollectionMatrix();
loadCollectionPower();
loadProvenanceRequirements();
loadProvenanceAudit();
loadBaselineAcceptance();
loadBaselinePromotion();
loadCollectionHandoff();
loadCollectionSubmissionContract();
loadCollectionSubmissionLint();
loadCollectionFixtureAudit();
loadCollectionIntake();
loadResearchReadiness();
loadClassifierLab();
loadEvidencePack();
loadClaimLedger();
loadArtifactLineage();
loadDecisionProtocol();
loadFalsificationBattery();
loadPublicationConsistency();
loadAttributionGrid();
loadNullCalibration();
loadReplicationAudit();
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
    ${koGuide("프로젝트 진화 읽는 법", [
      "Scale은 브라우저와 스냅샷이 다룰 수 있는 계산 범위입니다.",
      "Controlled signal은 합성 데이터에서 편향 신호가 통계 검사를 통과했는지를 뜻합니다.",
      "Claim level은 현재 공개적으로 주장해도 되는 최대 수준입니다. 지금은 실세계 attribution이나 난제 증명이 아닙니다.",
    ])}
    <div><span>Scale</span><strong>${formatCompact(metrics.live_compute_limit || 0)}</strong><small>${(metrics.precomputed_snapshot_limits || []).map(formatCompact).join(", ")} snapshots</small></div>
    <div><span>Controlled signal</span><strong>${formatNumber(metrics.robust_controlled_profiles?.length || 0)} profiles</strong><small>${formatNumber(metrics.null_calibration_iterations || 0)} null iterations</small></div>
    <div><span>Generator baselines</span><strong>${formatNumber(metrics.available_real_baselines || 0)}</strong><small>${formatNumber(metrics.public_control_baselines || 0)} public control</small></div>
    <div><span>Collection</span><strong>${formatNumber(metrics.intake_accepted || 0)}</strong><small>${formatNumber(metrics.intake_blocked || 0)} intake blockers</small></div>
    <div><span>Evidence</span><strong>${formatNumber(metrics.checksummed_artifacts || 0)}</strong><small>${formatNumber(metrics.falsification_checks || 0)} falsification · ${formatNumber(metrics.publication_consistency_checks || 0)} consistency</small></div>
    <div><span>Claim level</span><strong>${escapeHtml(formatClaimLevel(metrics.publication_claim_level))}</strong><small>${formatNumber(metrics.blocking_gaps || 0)} blocking gaps</small></div>
  `;
  renderEvolutionImpact(evolution);
  renderResearchAtlas(evolution);
  renderEvolutionSpine(evolution);
  renderEvolutionDelta(evolution);
  renderEvolutionMap(evolution);
  const spotlightIds = new Set([
    "conjecture-lab",
    "static-snapshots",
    "attribution-grid",
    "null-calibration",
    "replication-audit",
    "collection-fixture-audit",
    "collection-intake",
    "evidence-pack",
    "decision-protocol",
    "falsification-battery",
    "publication-consistency",
  ]);
  const spotlightPhases = phases.filter((phase) => spotlightIds.has(phase.id));
  outputs.evolutionTimeline.innerHTML = spotlightPhases
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

function renderResearchAtlas(evolution) {
  if (!outputs.atlasHero || !outputs.atlasContributionGrid || !outputs.atlasEvidenceLadder) return;
  const metrics = evolution.metrics || {};
  const dashboard = evolution.change_dashboard || bundledProjectEvolution.change_dashboard || {};
  const rollup = dashboard.visual_rollup || {};
  const spine = rollup.evidence_spine || [];
  const atlas = buildResearchAtlas(evolution);
  outputs.atlasHero.innerHTML = `
    ${koGuide("연구 지도 요약", [
      "이 페이지는 소수 예측기가 아니라 생성기 fingerprint와 증명 의무를 추적하는 연구 도구입니다.",
      "supported는 현재 산출물로 뒷받침되는 내용이고, blocked는 아직 주장하면 안 되는 내용입니다.",
      "real-world attribution은 OpenSSL/BoringSSL/Go 같은 실제 기준군이 accepted 상태가 되기 전까지 차단됩니다.",
    ])}
    <div class="atlas-hero-copy">
      <span>Research claim map</span>
      <strong>${escapeHtml(atlas.thesis)}</strong>
      <p>${escapeHtml(atlas.boundary)}</p>
    </div>
    <div class="atlas-hero-metrics">
      <div><span>Live scale</span><strong>${formatCompact(metrics.live_compute_limit || 0)}</strong><small>browser computation ceiling</small></div>
      <div><span>Controlled signal</span><strong>${formatNumber(metrics.robust_controlled_profiles?.length || 0)}</strong><small>${formatNumber(metrics.null_calibration_iterations || 0)} null iterations</small></div>
      <div><span>Publication artifacts</span><strong>${formatNumber(metrics.checksummed_artifacts || 0)}</strong><small>${formatNumber(metrics.publication_guard_checks || 0)} guard checks</small></div>
      <div><span>Open problems</span><strong>4</strong><small>proof workbench pages</small></div>
    </div>
  `;
  outputs.atlasContributionGrid.innerHTML = atlas.contributions
    .map((item) => `
      <article class="atlas-contribution is-${escapeHtml(item.status)}">
        <span>${escapeHtml(item.statusLabel)}</span>
        <strong>${escapeHtml(item.title)}</strong>
        <p>${escapeHtml(item.value)}</p>
        <em>${escapeHtml(item.evidence)}</em>
      </article>
    `)
    .join("");
  outputs.atlasEvidenceLadder.innerHTML = `
    <div class="atlas-section-head">
      <span>Evidence ladder</span>
      <strong>Every strong claim must climb from computation to controls, then to real baselines and publication gates.</strong>
    </div>
    ${koGuide("Evidence ladder란?", [
      "계산 결과만으로 강한 주장을 하지 않고, 통계 통제, 실세계 기준군, 출판 게이트를 차례로 통과해야 한다는 단계표입니다.",
      "Sim-to-Real 단계가 낮으면 실제 라이브러리나 지갑을 단정하는 주장은 아직 불가능합니다.",
    ])}
    <div class="atlas-ladder-grid">
      ${spine
        .map((item, index) => {
          const score = Math.max(0, Math.min(100, Number(item.score) || 0));
          return `
            <article class="atlas-ladder-step is-${escapeHtml(item.status || "active")}">
              <i>${String(index + 1).padStart(2, "0")}</i>
              <strong>${escapeHtml(item.layer || "Layer")}</strong>
              <span>${formatNumber(score)}%</span>
              <b><u style="width: ${score}%"></u></b>
              <p>${escapeHtml(item.gate || "")}</p>
            </article>
          `;
        })
        .join("")}
    </div>
  `;
  outputs.atlasProofGrid.innerHTML = `
    <div class="atlas-section-head">
      <span>Proof workbench</span>
      <strong>Finite certificates and attack tickets are useful only when they name the missing infinite theorem.</strong>
    </div>
    ${koGuide("증명 워크벤치 해석", [
      "finite certificate는 정해진 범위 안의 계산 증거입니다. 무한히 많은 경우를 증명하지 않습니다.",
      "missing infinite theorem은 검색 한계를 제거하는 핵심 수학 정리입니다. 이것이 없으면 open_not_proven 상태가 유지됩니다.",
    ])}
    ${atlas.openProblems
      .map((problem) => `
        <a class="atlas-proof-card" href="${escapeHtml(problem.href)}">
          <span>${escapeHtml(problem.status)}</span>
          <strong>${escapeHtml(problem.name)}</strong>
          <p>${escapeHtml(problem.route)}</p>
          <em>${escapeHtml(problem.artifact)}</em>
        </a>
      `)
      .join("")}
  `;
  outputs.atlasNextSteps.innerHTML = `
    <div class="atlas-section-head">
      <span>Next academic work</span>
      <strong>The shortest path to stronger claims is explicit and still blocked.</strong>
    </div>
    ${koGuide("다음 연구 과제", [
      "P0는 논문 주장을 강화하기 전에 먼저 해결해야 하는 최우선 작업입니다.",
      "classifier는 합성 데이터에서만 충분하지 않고, labelled real-world feature vector가 있어야 실세계 주장으로 이동할 수 있습니다.",
    ])}
    ${atlas.nextSteps
      .map((item) => `
        <article class="atlas-next-card is-${escapeHtml(item.priority || "P1")}">
          <span>${escapeHtml(item.priority || "P1")} · ${escapeHtml(item.track)}</span>
          <strong>${escapeHtml(item.action)}</strong>
          <p>${escapeHtml(item.unlock)}</p>
        </article>
      `)
      .join("")}
  `;
}

function buildResearchAtlas(evolution) {
  const metrics = evolution.metrics || {};
  const openGaps = evolution.open_gaps || [];
  return {
    thesis:
      "PrimeProject is now best understood as a falsifiable generator-fingerprint and proof-obligation workbench, not a prime-prediction claim.",
    boundary:
      "The supported result is controlled synthetic signal plus reproducible bounded evidence; real-world attribution and the four open conjectures remain blocked until their named artifacts exist.",
    contributions: [
      {
        title: "Scale made visible",
        status: "complete",
        statusLabel: "supported",
        value: "10M live browser computation plus static 1M/10M snapshots make finite behavior inspectable without recomputing on GitHub Pages.",
        evidence: `${formatCompact(metrics.live_compute_limit || 0)} live limit · ${(metrics.precomputed_snapshot_limits || []).length} snapshot tiers`,
      },
      {
        title: "Generator fingerprints controlled",
        status: "complete",
        statusLabel: "supported",
        value: "Residue, low-bit, and gap-context fingerprints are tested against bit-length controls, null calibration, and replication.",
        evidence: `${formatNumber(metrics.attribution_grid_rows || 0)} grid rows · ${formatNumber(metrics.replication_setting_count || 0)} replication settings`,
      },
      {
        title: "Sim-to-real boundary exposed",
        status: "blocked",
        statusLabel: "blocked",
        value: "OpenSSL, BoringSSL, Go, Bitcoin Core, and wallet/library baselines are registered, but accepted aggregate submissions are still missing.",
        evidence: `${formatNumber(metrics.baseline_acceptance_accepted || 0)} accepted baselines · ${formatNumber(metrics.intake_blocked || 0)} intake blockers`,
      },
      {
        title: "Publication claims governed",
        status: "guarded",
        statusLabel: "guarded",
        value: "Claim-language audit, claim ledger, lineage checks, decision protocol, falsification battery, and consistency audit constrain public statements.",
        evidence: `${formatNumber(metrics.checksummed_artifacts || 0)} artifacts · ${formatNumber(metrics.claim_language_failures || 0)} language failures`,
      },
    ],
    openProblems: [
      {
        name: "Riemann Hypothesis",
        href: "open-problems/riemann.html",
        status: "open not proven",
        route: "Requires an all-x prime-counting or zero-equivalent theorem, not finite checkpoint agreement.",
        artifact: "missing: formal all-x analytic theorem",
      },
      {
        name: "Collatz Conjecture",
        href: "open-problems/collatz.html",
        status: "open not proven",
        route: "Requires a symbolic residue-block descent cover, not trajectory replay through a limit.",
        artifact: "missing: global descent cover",
      },
      {
        name: "Goldbach Conjecture",
        href: "open-problems/goldbach.html",
        status: "open not proven",
        route: "Requires a positive binary representation lower bound with explicit cutoff.",
        artifact: "missing: compatible large-even theorem",
      },
      {
        name: "Twin Prime Conjecture",
        href: "open-problems/twin-prime.html",
        status: "open not proven",
        route: "Requires an exact gap-2 lower bound, not bounded-gap or Hardy-Littlewood-scale evidence.",
        artifact: "missing: unconditional exact gap-2 theorem",
      },
    ],
    nextSteps: [
      ...openGaps.map((gap) => ({
        priority: gap.priority || "P1",
        track: gap.track || "research",
        action: gap.gap || "Close open research gap.",
        unlock: "Required before stronger public claims can move beyond the current scaffold.",
      })),
      {
        priority: "P0",
        track: "proof",
        action: "Convert one breakthrough agenda item into a formal theorem statement with a falsification test.",
        unlock: "Required before any open-problem page can move from proof workbench to proof candidate review.",
      },
    ],
  };
}

function renderEvolutionSpine(evolution) {
  if (!outputs.evolutionSpine) return;
  const dashboard = evolution.change_dashboard || bundledProjectEvolution.change_dashboard || {};
  const rollup = dashboard.visual_rollup || {};
  const spine = rollup.evidence_spine || [];
  outputs.evolutionSpine.innerHTML = `
    <div class="spine-heading">
      <span>Evidence Spine</span>
      <strong>One evidence layer per claim question, with artifact names shown once.</strong>
    </div>
    <div class="spine-grid">
      ${spine
        .map((item) => {
          const score = Math.max(0, Math.min(100, Number(item.score) || 0));
          const artifacts = item.artifacts || [];
          return `
            <div class="spine-card is-${escapeHtml(item.status || "active")}">
              <div class="spine-card-top">
                <strong>${escapeHtml(item.layer || "Layer")}</strong>
                <em>${formatNumber(score)}%</em>
              </div>
              <i><b style="width: ${score}%"></b></i>
              <span>${escapeHtml(item.gate || "")}</span>
              <p>${escapeHtml(item.proof || "")}</p>
              <code>${formatNumber(artifacts.length)} artifacts: ${escapeHtml(artifacts.map(shortArtifactName).join(", "))}</code>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function shortArtifactName(path) {
  return String(path || "")
    .replace(/^data\//, "")
    .replace(/^assets\/snapshots\/\*\.svg$/, "snapshot SVGs")
    .replace(/\.json$/, "")
    .replace(/_/g, " ");
}

function formatClaimLevel(level) {
  const value = String(level || "unknown");
  if (value === "public_demo_only") return "public demo";
  if (value === "controlled_synthetic_only") return "synthetic only";
  return value.replace(/_/g, " ");
}

function renderEvolutionImpact(evolution) {
  if (!outputs.evolutionImpact) return;
  const dashboard = evolution.change_dashboard || bundledProjectEvolution.change_dashboard || {};
  const metrics = evolution.metrics || {};
  const rollup = dashboard.visual_rollup || {};
  const releaseTrail = rollup.release_trail || [];
  const hardeningMap = rollup.hardening_map || [];
  const changes = (dashboard.latest_changes || []).slice(0, 5);
  outputs.evolutionImpact.innerHTML = `
    <div class="impact-narrative">
      <span>Project Logic</span>
      <strong>${escapeHtml(dashboard.headline || "Research workflow maturity over time.")}</strong>
    </div>
    <div class="strategic-summary">
      <div class="strategy-card is-complete">
        <span>Supported</span>
        <strong>Controlled synthetic fingerprints</strong>
        <em>${formatNumber(metrics.attribution_grid_rows || 0)} rows · ${formatNumber(metrics.replication_setting_count || 0)} replication settings</em>
      </div>
      <div class="strategy-card is-blocked">
        <span>Not supported yet</span>
        <strong>Real-world or Bitcoin attribution</strong>
        <em>${formatNumber(metrics.baseline_acceptance_accepted || 0)} accepted baselines · ${formatNumber(metrics.intake_accepted || 0)} accepted submissions</em>
      </div>
      <div class="strategy-card is-guarded">
        <span>Next decisive test</span>
        <strong>Accepted library baselines + labelled vectors</strong>
        <em>${formatNumber(metrics.promotion_minimal_unlock_targets || 0)} unlock targets · ${formatNumber(metrics.promotion_projected_samples || 0)} projected samples</em>
      </div>
    </div>
    <div class="release-trail">
      <div class="release-trail-heading">
        <span>Visual Change Trail</span>
        <strong>${escapeHtml(rollup.headline || "How the project changed across research milestones.")}</strong>
      </div>
      ${releaseTrail
        .map((item) => `
          <div class="release-node is-${escapeHtml(item.state || "active")}">
            <i>${escapeHtml(item.marker || "")}</i>
            <strong>${escapeHtml(item.title || "milestone")}</strong>
            <em>${escapeHtml(item.measure || "")}</em>
            <span>${escapeHtml(item.proof || "")}</span>
          </div>
        `)
        .join("")}
    </div>
    <div class="hardening-map">
      <div class="hardening-heading">
        <span>Hardening Map</span>
        <strong>Recent fixes converted silent data contamination paths into explicit public contract blockers.</strong>
      </div>
      ${hardeningMap
        .map((item) => `
          <div class="hardening-node is-${escapeHtml(item.status || "guarded")}">
            <i>${escapeHtml(item.step || "")}</i>
            <strong>${escapeHtml(item.layer || "Guard")}</strong>
            <span>${escapeHtml(item.risk || "")}</span>
            <em>${escapeHtml(item.guard || "")}</em>
            <code>${escapeHtml(item.evidence || "")}</code>
          </div>
        `)
        .join("")}
    </div>
    <div class="impact-change-list">
      ${changes
        .map((change) => `
          <div>
            <strong>${escapeHtml(change.label || "change")}</strong>
            <span>${escapeHtml(change.impact || "")}</span>
            <em>${escapeHtml(change.metric || "")}</em>
          </div>
        `)
        .join("")}
    </div>
  `;
}

function renderEvolutionDelta(evolution) {
  if (!outputs.evolutionDelta) return;
  const dashboard = evolution.change_dashboard || bundledProjectEvolution.change_dashboard || {};
  const delta = dashboard.research_delta || {};
  const claimState = delta.claim_state || {};
  const lanes = delta.claim_lanes || [];
  outputs.evolutionDelta.innerHTML = `
    <div class="delta-heading">
      <span>Claim Boundaries</span>
      <strong>${escapeHtml(delta.headline || "Visible before/current/next state of the research program.")}</strong>
    </div>
    <div class="delta-state">
      <div>
        <span>Before</span>
        <strong>${escapeHtml(claimState.before || "Exploratory visualization")}</strong>
      </div>
      <div>
        <span>Current</span>
        <strong>${escapeHtml(claimState.current || "Gated research scaffold")}</strong>
      </div>
      <div>
        <span>Next unlock</span>
        <strong>${escapeHtml(claimState.next || "Real-world baselines and classifier vectors")}</strong>
      </div>
    </div>
    <div class="claim-lane-grid">
      ${lanes
        .map((lane) => `
          <div class="claim-lane is-${escapeHtml(lane.status || "blocked")}">
            <span>${escapeHtml(lane.status || "blocked")}</span>
            <strong>${escapeHtml(lane.claim || "claim")}</strong>
            <em>${escapeHtml(lane.basis || "")}</em>
          </div>
        `)
        .join("")}
    </div>
  `;
}

function renderEvolutionMap(evolution) {
  const svg = outputs.evolutionMap;
  const width = 1340;
  const height = 410;
  const phases = evolution.phases || [];
  const columns = [
    ["regularity-plan", "bitcoin-track"],
    ["conjecture-lab"],
    ["static-snapshots", "fingerprint-baseline"],
    ["attribution-grid", "null-calibration", "replication-audit", "crypto-classifier", "real-world-registry"],
    ["collection-matrix", "collection-power"],
    ["provenance-gate", "provenance-audit", "baseline-acceptance", "baseline-promotion"],
    ["collection-handoff", "collection-submission-contract", "collection-submission-lint", "collection-fixture-audit", "collection-intake", "readiness-gates"],
    ["evidence-pack", "claim-ledger", "artifact-lineage"],
    ["decision-protocol", "falsification-battery"],
    ["publication-consistency"],
  ];
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  const positions = new Map();
  const left = 32;
  const top = 42;
  const columnGap = 130;
  const rowGap = 56;
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
    ${koGuide("Baseline Lab 해설", [
      "baseline은 비교 기준군입니다. 실제 라이브러리별 aggregate fingerprint가 있어야 의심 데이터셋과 거리를 비교할 수 있습니다.",
      "local-sensitive는 raw key나 private prime을 공개하지 않고 로컬에서 집계값만 다뤄야 한다는 뜻입니다.",
      "available이 0이면 실세계 attribution 주장은 아직 차단됩니다.",
    ])}
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
  const sensitivityRows = sensitivityRowsForDisplay(power);
  outputs.collectionPowerStatus.textContent =
    `${formatNumber(summary.strong_count || 0)} strong · ${formatNumber(summary.coarse_count || 0)} coarse`;
  outputs.collectionPowerSummary.innerHTML = `
    ${koGuide("Collection Power 해석", [
      "sample floor는 통계적으로 의미 있는 차이를 보려면 최소 몇 개의 aggregate sample이 필요한지 추정한 값입니다.",
      "coarse는 거친 선별만 가능하다는 뜻이고, strong은 더 강한 주장에 가까운 표본 규모를 뜻합니다.",
      "이 표는 실제 키를 공개하라는 요구가 아니라, 공개 가능한 집계 fingerprint 수집량을 정하는 기준입니다.",
    ])}
    <div><span>Method</span><strong>${escapeHtml(power.method?.name || "unknown")}</strong><small>${displayTvLabel(power.method?.interval_label, power.method?.interval_confidence)} interval</small></div>
    <div><span>Targets</span><strong>${formatNumber(summary.target_count || rows.length)}</strong><small>${formatNumber(summary.minimum_recommended_replicates || 0)} replicates</small></div>
    <div><span>Strong</span><strong>${formatNumber(summary.strong_count || 0)}</strong><small>claim-ready floor</small></div>
    <div><span>Sensitivity</span><strong>${formatNumber((power.sensitivity?.rows || []).length)}</strong><small>alpha x TV grid</small></div>
  `;
  const targetRowsHtml = rows
    .slice()
    .sort((a, b) => (b.conservative_tv_floor_interval || b.conservative_tv_floor_95) - (a.conservative_tv_floor_interval || a.conservative_tv_floor_95))
    .slice(0, 5)
    .map((row) => {
      const targetLabel = displayTvLabel(row.target_tv_label, row.target_tv ?? power.method?.target_tv);
      const targetSamples = row.min_samples_for_target_tv || row.min_samples_for_10pct_tv || 0;
      const intervalLabel = displayTvLabel(row.interval_label, row.interval_confidence ?? power.method?.interval_confidence);
      const intervalFloor = row.conservative_tv_floor_interval || row.conservative_tv_floor_95 || 0;
      return `
        <div class="power-row">
          <strong>${escapeHtml(row.library || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
          <em class="is-${escapeHtml(row.power_tier || "coarse")}">${escapeHtml(row.power_tier || "coarse")}</em>
          <span>${escapeHtml(intervalLabel)} TV floor ${formatPercent(intervalFloor)}</span>
          <span>${escapeHtml(targetLabel)} TV n≈${formatNumber(targetSamples)}</span>
        </div>
      `;
    })
    .join("");
  const sensitivityHtml = sensitivityRows
    .map((row) => `
      <div class="power-row is-sensitivity">
        <strong>${escapeHtml(row.object_type || "object")} sensitivity</strong>
        <em class="is-screening">alpha ${escapeHtml(String(row.alpha))}</em>
        <span>${escapeHtml(displayTvLabel(row.target_tv_label, row.target_tv))} TV · ${formatNumber(row.bucket_count || 0)} buckets</span>
        <span>n≈${formatNumber(row.min_samples || 0)}</span>
      </div>
    `)
    .join("");
  outputs.collectionPowerRows.innerHTML = targetRowsHtml + sensitivityHtml;
}

function sensitivityRowsForDisplay(power) {
  const rows = power.sensitivity?.rows || [];
  const defaultAlpha = Number(power.method?.alpha ?? 0.05);
  const rsaRows = rows
    .filter((row) => row.object_type === "rsa-prime" && Math.abs(Number(row.alpha) - defaultAlpha) < 1e-12)
    .sort((a, b) => Number(b.target_tv || 0) - Number(a.target_tv || 0));
  const strictRsa = rows.find(
    (row) => row.object_type === "rsa-prime" && Number(row.alpha) === 0.001 && Number(row.target_tv) === 0.05
  );
  return [...rsaRows.slice(0, 3), strictRsa].filter(Boolean);
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

async function loadBaselineAcceptance() {
  try {
    if (window.location.protocol === "file:") {
      state.baselineAcceptance = bundledBaselineAcceptance;
    } else {
      const response = await fetch("data/baseline_acceptance.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`baseline acceptance ${response.status}`);
      state.baselineAcceptance = await response.json();
    }
  } catch (error) {
    state.baselineAcceptance = bundledBaselineAcceptance;
  }
  renderBaselineAcceptance();
}

function renderBaselineAcceptance() {
  if (!outputs.baselineAcceptanceStatus || !outputs.baselineAcceptanceSummary || !outputs.baselineAcceptanceRows) return;
  const acceptance = state.baselineAcceptance || bundledBaselineAcceptance;
  const summary = acceptance.summary || {};
  const rows = acceptance.rows || [];
  const gate = acceptance.claim_gate || {};
  outputs.baselineAcceptanceStatus.textContent =
    `${formatNumber(acceptance.accepted_count || 0)} accepted · ${escapeHtml(gate.status || "unknown")}`;
  outputs.baselineAcceptanceSummary.innerHTML = `
    <div><span>Targets</span><strong>${formatNumber(acceptance.row_count || rows.length)}</strong><small>${formatNumber(acceptance.blocked_count || 0)} blocked</small></div>
    <div><span>Accepted</span><strong>${formatNumber(acceptance.accepted_count || 0)}</strong><small>${formatNumber(summary.accepted_rsa_library_count || 0)} RSA libs</small></div>
    <div><span>Screening</span><strong>${formatNumber(acceptance.screening_only_count || 0)}</strong><small>not claim-ready</small></div>
    <div><span>Minimum</span><strong>${formatNumber(summary.minimum_rsa_libraries || 0)}</strong><small>RSA libraries</small></div>
  `;
  outputs.baselineAcceptanceRows.innerHTML = rows
    .slice()
    .sort((a, b) => {
      const rank = { accepted: 0, screening_only: 1, blocked: 2 };
      return (rank[a.acceptance] ?? 3) - (rank[b.acceptance] ?? 3);
    })
    .slice(0, 6)
    .map((row) => `
      <div class="provenance-row audit-row">
        <strong>${escapeHtml(row.library || row.baseline_id || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
        <span>${escapeHtml(row.power_tier || "unknown")} power</span>
        <em class="is-${escapeHtml(row.acceptance || "blocked").replace("_", "-")}">${escapeHtml(row.acceptance || "blocked")}</em>
        <code>${escapeHtml((row.blocking_reasons || [])[0] || "claim-ready")}</code>
      </div>
    `)
    .join("");
}

async function loadBaselinePromotion() {
  try {
    if (window.location.protocol === "file:") {
      state.baselinePromotion = bundledBaselinePromotion;
    } else {
      const response = await fetch("data/baseline_promotion_plan.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`baseline promotion ${response.status}`);
      state.baselinePromotion = await response.json();
    }
  } catch (error) {
    state.baselinePromotion = bundledBaselinePromotion;
  }
  renderBaselinePromotion();
}

function renderBaselinePromotion() {
  if (!outputs.baselinePromotionStatus || !outputs.baselinePromotionSummary || !outputs.baselinePromotionRows) return;
  const plan = state.baselinePromotion || bundledBaselinePromotion;
  const summary = plan.summary || {};
  const rows = plan.minimal_unlock_targets || [];
  outputs.baselinePromotionStatus.textContent =
    `${formatNumber(summary.minimal_unlock_target_count || rows.length)} target unlock path`;
  outputs.baselinePromotionSummary.innerHTML = `
    <div><span>Unlock targets</span><strong>${formatNumber(summary.minimal_unlock_target_count || rows.length)}</strong><small>RSA libraries</small></div>
    <div><span>Projected n</span><strong>${formatNumber(summary.projected_samples_for_minimal_unlock || 0)}</strong><small>10% TV floor</small></div>
    <div><span>P0 targets</span><strong>${formatNumber(summary.p0_target_count || 0)}</strong><small>collection queue</small></div>
    <div><span>Next step</span><strong>${escapeHtml(summary.dominant_next_step || "ready")}</strong><small>dominant blocker</small></div>
  `;
  outputs.baselinePromotionRows.innerHTML = rows
    .map((row) => `
      <div class="provenance-row audit-row">
        <strong>${escapeHtml(row.library || row.baseline_id || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
        <span>${formatNumber(row.target_samples_for_10pct_tv || 0)} samples</span>
        <em class="is-screening-only">${escapeHtml(row.priority || "P0")}</em>
        <code>${escapeHtml(row.next_step || "ready")}</code>
      </div>
    `)
    .join("");
}

async function loadCollectionHandoff() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionHandoff = bundledCollectionHandoff;
    } else {
      const response = await fetch("data/collection_handoff.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection handoff ${response.status}`);
      state.collectionHandoff = await response.json();
    }
  } catch (error) {
    state.collectionHandoff = bundledCollectionHandoff;
  }
  renderCollectionHandoff();
}

function renderCollectionHandoff() {
  if (
    !outputs.collectionHandoffStatus ||
    !outputs.collectionHandoffSummary ||
    !outputs.collectionHandoffRows ||
    !outputs.collectionHandoffContract
  ) {
    return;
  }
  const handoff = state.collectionHandoff || bundledCollectionHandoff;
  const summary = handoff.summary || {};
  const rows = handoff.rows || [];
  const contract = handoff.public_artifact_contract || {};
  const requiredOutputs = contract.required_public_outputs || [];
  outputs.collectionHandoffStatus.textContent =
    `${formatNumber(summary.p0_count || 0)} P0 · ${escapeHtml(handoff.claim_gate?.status || "unknown")}`;
  outputs.collectionHandoffSummary.innerHTML = `
    <div><span>Tasks</span><strong>${formatNumber(summary.task_count || rows.length)}</strong><small>${formatNumber(summary.blocked_count || 0)} blocked</small></div>
    <div><span>P0 samples</span><strong>${formatNumber(summary.remaining_p0_samples_for_10pct_tv || 0)}</strong><small>10% TV floor</small></div>
    <div><span>Provenance</span><strong>${formatNumber(summary.missing_provenance_field_count || 0)}</strong><small>field references</small></div>
    <div><span>Classifier</span><strong>${escapeHtml(summary.classifier_scope || "missing")}</strong><small>${formatNumber(summary.classifier_label_count || 0)} labels</small></div>
  `;
  outputs.collectionHandoffRows.innerHTML = rows
    .slice()
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority))
    .slice(0, 5)
    .map((row) => `
      <div class="handoff-row">
        <div>
          <strong>${escapeHtml(row.library || row.baseline_id || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
          <span>${escapeHtml(row.public_output || row.track || "")}</span>
        </div>
        <em class="priority-${escapeHtml(row.priority || "P2").toLowerCase()}">${escapeHtml(row.priority || "P2")}</em>
        <span>${formatNumber(row.remaining_samples_to_10pct_tv || 0)} samples</span>
        <code>${escapeHtml((row.collector_contract?.must_not_publish || []).slice(0, 2).join(", ") || "aggregate-only")}</code>
      </div>
    `)
    .join("");
  outputs.collectionHandoffContract.innerHTML = `
    <strong>Public contract</strong>
    <span>${contract.publish_private_material ? "private material publication allowed" : "private material stays local"}</span>
    <code>${escapeHtml(requiredOutputs.join(" · ") || "aggregate outputs only")}</code>
  `;
}

async function loadCollectionSubmissionContract() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionSubmissionContract = bundledCollectionSubmissionContract;
    } else {
      const response = await fetch("data/collection_submission_contract.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection submission contract ${response.status}`);
      state.collectionSubmissionContract = await response.json();
    }
  } catch (error) {
    state.collectionSubmissionContract = bundledCollectionSubmissionContract;
  }
  renderCollectionSubmissionContract();
}

function renderCollectionSubmissionContract() {
  if (
    !outputs.collectionSubmissionContractStatus ||
    !outputs.collectionSubmissionContractSummary ||
    !outputs.collectionSubmissionContractRows
  ) {
    return;
  }
  const contract = state.collectionSubmissionContract || bundledCollectionSubmissionContract;
  const summary = contract.summary || {};
  const recordContract = contract.record_contract || {};
  const vectorContract = contract.feature_vector_contract || {};
  const safety = contract.public_safety || {};
  const templates = contract.task_templates || [];
  outputs.collectionSubmissionContractStatus.textContent =
    `${formatNumber(summary.task_count || templates.length)} templates · ${escapeHtml(summary.claim_scope_required || "real_world")}`;
  outputs.collectionSubmissionContractSummary.innerHTML = `
    <div><span>Record fields</span><strong>${formatNumber(summary.required_record_field_count || (recordContract.required_fields || []).length)}</strong><small>${escapeHtml((recordContract.required_fields || []).slice(0, 3).join(", "))}</small></div>
    <div><span>Vector schema</span><strong>${formatNumber(summary.required_scalar_feature_count || (vectorContract.required_scalar_features || []).length)}</strong><small>${escapeHtml(vectorContract.schema || "missing")}</small></div>
    <div><span>Public safety</span><strong>${formatNumber(summary.forbidden_public_field_count || (safety.forbidden_field_names || []).length)}</strong><small>forbidden fields</small></div>
    <div><span>Acceptance checks</span><strong>${formatNumber((contract.acceptance_checks || []).length)}</strong><small>pre-intake blockers</small></div>
  `;
  outputs.collectionSubmissionContractRows.innerHTML = templates
    .slice()
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority))
    .slice(0, 5)
    .map((template) => `
      <div class="handoff-row">
        <div>
          <strong>${escapeHtml(template.library || template.baseline_id || "unknown")} ${formatNumber(template.bit_length || 0)}b</strong>
          <span>${escapeHtml(template.object_type || "object")} · ${formatNumber(template.target_samples_for_10pct_tv || 0)} target samples</span>
        </div>
        <em class="priority-${escapeHtml(template.priority || "P2").toLowerCase()}">${escapeHtml(template.priority || "P2")}</em>
        <span>${formatNumber(template.planned_sample_target || 0)} planned</span>
        <code>${escapeHtml((template.must_not_publish || []).slice(0, 3).join(", ") || "aggregate-only")}</code>
      </div>
    `)
    .join("");
}

async function loadCollectionSubmissionLint() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionSubmissionLint = bundledCollectionSubmissionLint;
    } else {
      const response = await fetch("data/collection_submission_lint.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection submission lint ${response.status}`);
      state.collectionSubmissionLint = await response.json();
    }
  } catch (error) {
    state.collectionSubmissionLint = bundledCollectionSubmissionLint;
  }
  renderCollectionSubmissionLint();
}

function renderCollectionSubmissionLint() {
  if (!outputs.collectionSubmissionLintStatus || !outputs.collectionSubmissionLintSummary || !outputs.collectionSubmissionLintRows) {
    return;
  }
  const lint = state.collectionSubmissionLint || bundledCollectionSubmissionLint;
  const summary = lint.summary || {};
  const rows = lint.rows || [];
  const gate = lint.lint_gate || {};
  outputs.collectionSubmissionLintStatus.textContent =
    `${formatNumber(summary.pass_count || 0)} pass · ${escapeHtml(gate.status || "waiting")}`;
  outputs.collectionSubmissionLintSummary.innerHTML = `
    <div><span>Submitted</span><strong>${formatNumber(summary.submitted_count || 0)}</strong><small>${formatNumber(summary.task_count || rows.length)} lint tasks</small></div>
    <div><span>Waiting</span><strong>${formatNumber(summary.awaiting_submission_count || 0)}</strong><small>contract templates</small></div>
    <div><span>Blocked</span><strong>${formatNumber(summary.blocked_count || 0)}</strong><small>pre-intake errors</small></div>
    <div><span>Warnings</span><strong>${formatNumber(summary.warning_count || 0)}</strong><small>${escapeHtml((summary.dominant_warnings || [])[0]?.reason || "none")}</small></div>
    <div><span>Vectors</span><strong>${formatNumber(summary.feature_vector_blocked_count || 0)}</strong><small>lint blocked</small></div>
    <div><span>Reuse</span><strong>${formatNumber(summary.reused_aggregate_hash_count || 0)}</strong><small>checksum collisions</small></div>
  `;
  outputs.collectionSubmissionLintRows.innerHTML = rows
    .slice()
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority))
    .slice(0, 5)
    .map((row) => {
      const issue = (row.blocking_reasons || [])[0] || (row.warning_reasons || [])[0] || "contract-ready";
      const sampleText = row.submitted ? `${formatNumber(row.sample_count || 0)} samples` : "awaiting submission";
      return `
        <div class="intake-row">
          <div>
            <strong>${escapeHtml(row.library || row.baseline_id || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
            <span>${escapeHtml(row.object_type || "object")} · ${escapeHtml(sampleText)}</span>
          </div>
          <em class="priority-${escapeHtml(row.priority || "P2").toLowerCase()}">${escapeHtml(row.priority || "P2")}</em>
          <span>${escapeHtml(row.status || "waiting")}</span>
          <code>${escapeHtml(issue)}</code>
        </div>
      `;
    })
    .join("");
}

async function loadCollectionFixtureAudit() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionFixtureAudit = bundledCollectionFixtureAudit;
    } else {
      const response = await fetch("data/collection_fixture_audit.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection fixture audit ${response.status}`);
      state.collectionFixtureAudit = await response.json();
    }
  } catch (error) {
    state.collectionFixtureAudit = bundledCollectionFixtureAudit;
  }
  renderCollectionFixtureAudit();
}

function renderCollectionFixtureAudit() {
  if (!outputs.collectionFixtureAuditStatus || !outputs.collectionFixtureAuditSummary || !outputs.collectionFixtureAuditRows) {
    return;
  }
  const audit = state.collectionFixtureAudit || bundledCollectionFixtureAudit;
  const summary = audit.summary || {};
  const gate = audit.quality_gate || {};
  const lint = audit.lint_summary || {};
  const rows = audit.rows || [];
  outputs.collectionFixtureAuditStatus.textContent =
    `${formatNumber(summary.passed_expectation_count || 0)} met · ${escapeHtml(gate.status || "unknown")}`;
  outputs.collectionFixtureAuditSummary.innerHTML = `
    <div><span>Fixtures</span><strong>${formatNumber(summary.fixture_count || rows.length)}</strong><small>public-safe cases</small></div>
    <div><span>Failures</span><strong>${formatNumber(summary.failed_expectation_count || 0)}</strong><small>expected vs actual</small></div>
    <div><span>Pass/Warning</span><strong>${formatNumber((summary.actual_pass_count || 0) + (summary.actual_warning_count || 0))}</strong><small>${formatNumber(summary.actual_blocked_count || 0)} blocked cases</small></div>
    <div><span>Lint replay</span><strong>${formatNumber(lint.submitted_count || 0)}</strong><small>${formatNumber(lint.reused_aggregate_hash_count || 0)} reused hashes</small></div>
  `;
  outputs.collectionFixtureAuditRows.innerHTML = rows
    .slice(0, 10)
    .map((row) => {
      const reason = (row.actual_reasons || [])[0] || "contract-ready";
      return `
        <div class="intake-row fixture-row ${row.expectation_met ? "is-pass" : "is-fail"}">
          <div>
            <strong>${escapeHtml(row.fixture_id || "fixture")}</strong>
            <span>${escapeHtml(row.library || "unknown")} · ${escapeHtml(row.object_type || "object")} ${formatNumber(row.bit_length || 0)}b</span>
          </div>
          <em class="${row.expectation_met ? "is-pass" : "is-fail"}">${row.expectation_met ? "met" : "fail"}</em>
          <span>${escapeHtml(row.expected_status || "expected")} &rarr; ${escapeHtml(row.actual_status || "actual")}</span>
          <code>${escapeHtml(reason)}</code>
        </div>
      `;
    })
    .join("");
}

async function loadCollectionIntake() {
  try {
    if (window.location.protocol === "file:") {
      state.collectionIntake = bundledCollectionIntake;
    } else {
      const response = await fetch("data/collection_intake.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`collection intake ${response.status}`);
      state.collectionIntake = await response.json();
    }
  } catch (error) {
    state.collectionIntake = bundledCollectionIntake;
  }
  renderCollectionIntake();
}

function renderCollectionIntake() {
  if (!outputs.collectionIntakeStatus || !outputs.collectionIntakeSummary || !outputs.collectionIntakeRows) return;
  const intake = state.collectionIntake || bundledCollectionIntake;
  const summary = intake.summary || {};
  const rows = intake.rows || [];
  const gate = intake.claim_gate || {};
  outputs.collectionIntakeStatus.textContent =
    `${formatNumber(summary.accepted_count || 0)} accepted · ${formatNumber(summary.blocked_count || 0)} blocked`;
  outputs.collectionIntakeSummary.innerHTML = `
    <div><span>Submitted</span><strong>${formatNumber(summary.submitted_count || 0)}</strong><small>${formatNumber(summary.task_count || rows.length)} intake tasks</small></div>
    <div><span>Accepted</span><strong>${formatNumber(summary.accepted_count || 0)}</strong><small>${formatNumber(summary.accepted_rsa_library_count || 0)} RSA libs</small></div>
    <div><span>P0 blocked</span><strong>${formatNumber(summary.p0_blocked_count || 0)}</strong><small>${formatNumber(summary.remaining_p0_samples_for_10pct_tv || 0)} samples left</small></div>
    <div><span>Vectors</span><strong>${formatNumber(summary.feature_vector_contract_blocked_count || 0)}</strong><small>contract blocked</small></div>
    <div><span>Collisions</span><strong>${formatNumber((summary.duplicate_submission_count || 0) + (summary.reused_aggregate_hash_count || 0))}</strong><small>duplicate / reused</small></div>
    <div><span>Forbidden</span><strong>${formatNumber(summary.forbidden_public_field_count || 0)}</strong><small>${escapeHtml(gate.status || "unknown")}</small></div>
  `;
  outputs.collectionIntakeRows.innerHTML = rows
    .slice()
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority))
    .slice(0, 5)
    .map((row) => {
      const issue = (row.forbidden_public_fields || [])[0] || (row.blocking_reasons || [])[0] || "claim-ready";
      const submitted = row.submitted ? `${formatNumber(row.sample_count || 0)} samples` : "not submitted";
      return `
        <div class="intake-row">
          <div>
            <strong>${escapeHtml(row.library || row.baseline_id || "unknown")} ${formatNumber(row.bit_length || 0)}b</strong>
            <span>${escapeHtml(row.object_type || row.track || "")} · ${escapeHtml(submitted)}</span>
          </div>
          <em class="priority-${escapeHtml(row.priority || "P2").toLowerCase()}">${escapeHtml(row.priority || "P2")}</em>
          <span>${escapeHtml(row.status || "blocked")}</span>
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
    ${koGuide("Readiness 해설", [
      "readiness는 연구가 논문 주장으로 올라갈 준비가 얼마나 되었는지 보는 점수입니다.",
      "blocking gap은 현재 주장을 강하게 만들 수 없게 막는 핵심 결손입니다.",
      "Real baselines가 부족하면 실세계 라이브러리 attribution은 계속 blocked 상태입니다.",
    ])}
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

async function loadClassifierLab() {
  try {
    if (window.location.protocol === "file:") {
      state.featureVectors = bundledFeatureVectors;
      state.cryptoClassifier = bundledCryptoClassifier;
    } else {
      const [featureResponse, classifierResponse] = await Promise.all([
        fetch("data/feature_vectors.json", { cache: "no-cache" }),
        fetch("data/crypto_classifier_report.json", { cache: "no-cache" }),
      ]);
      if (!featureResponse.ok) throw new Error(`feature vectors ${featureResponse.status}`);
      if (!classifierResponse.ok) throw new Error(`crypto classifier ${classifierResponse.status}`);
      state.featureVectors = await featureResponse.json();
      state.cryptoClassifier = await classifierResponse.json();
    }
  } catch (error) {
    state.featureVectors = bundledFeatureVectors;
    state.cryptoClassifier = bundledCryptoClassifier;
  }
  renderClassifierLab();
}

function renderClassifierLab() {
  if (!outputs.classifierStatus || !outputs.classifierSummary || !outputs.classifierLabels) return;
  const features = state.featureVectors || bundledFeatureVectors;
  const report = state.cryptoClassifier || bundledCryptoClassifier;
  const scope = report.claim_scope || features.claim_scope || "unknown";
  outputs.classifierStatus.textContent = scope === "real_world" ? "real-world scoped" : "controlled synthetic only";
  outputs.classifierSummary.innerHTML = `
    <div><span>Vectors</span><strong>${formatNumber(report.usable_vector_count || report.vector_count || 0)}</strong><small>${formatNumber(report.label_count || 0)} labels</small></div>
    <div><span>Accuracy</span><strong>${report.accuracy == null ? "n/a" : formatPercent(report.accuracy)}</strong><small>${formatNumber(report.correct || 0)} / ${formatNumber(report.total || 0)}</small></div>
    <div><span>Feature space</span><strong>${escapeHtml(report.model?.feature_space || "unknown")}</strong><small>${formatNumber((features.feature_names || []).length)} features</small></div>
    <div><span>Claim scope</span><strong>${escapeHtml(scope)}</strong><small>not real-world attribution</small></div>
  `;
  outputs.classifierLabels.innerHTML = Object.entries(report.labels || {})
    .map(([label, summary]) => `
      <div class="classifier-label-row">
        <strong>${escapeHtml(label)}</strong>
        <span>${formatNumber(summary.correct || 0)} / ${formatNumber(summary.total || 0)}</span>
        <meter min="0" max="1" value="${Number(summary.accuracy || 0)}"></meter>
        <em>${summary.accuracy == null ? "n/a" : formatPercent(summary.accuracy)}</em>
      </div>
    `)
    .join("") + `
      <div class="classifier-finding">
        <strong>${escapeHtml((report.findings || [])[0]?.check || "scope_gate")}</strong>
        <span>${escapeHtml((report.findings || [])[0]?.message || "Classifier output is gated before real-world attribution claims.")}</span>
      </div>
    `;
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
  if (!outputs.evidenceSummary || !outputs.evidenceGateRows || !outputs.evidenceArtifactRows || !outputs.requiredEvidenceRows) return;
  const pack = state.evidencePack || bundledEvidencePack;
  const claim = pack.claim_level || {};
  const gates = pack.publication_gates || [];
  const failed = gates.filter((gateItem) => !gateItem.passed);
  outputs.evidenceSummary.innerHTML = `
    ${koGuide("Evidence Pack 읽는 법", [
      "Claim level은 현재 공개 페이지와 README가 넘지 말아야 하는 주장 한계입니다.",
      "Failed gates는 아직 논문/실세계 주장으로 승격하지 못하게 막는 안전장치입니다.",
      "Artifacts는 JSON 산출물과 checksum입니다. 같은 결과가 재현되는지 확인하기 위한 공개 증거 묶음입니다.",
    ])}
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
    .map((artifact) => {
      let semantic = "";
      if (artifact.role === "claim_language_audit") {
        semantic =
          ` · quality ${artifact.quality_gate_status || "unknown"}` +
          ` · ${formatNumber(artifact.claim_language_guarded_count || 0)} guarded` +
          ` · ${formatNumber(artifact.claim_language_fail_count || 0)} failures`;
      } else if (artifact.quality_gate_status) {
        semantic = ` · quality ${artifact.quality_gate_status} · ${formatNumber(artifact.failed_expectation_count || 0)} failures`;
      }
      return `
        <div class="evidence-row artifact-row">
          <strong>${escapeHtml(artifact.role || "artifact")}</strong>
          <span>${escapeHtml(artifact.schema || "unknown schema")}${escapeHtml(semantic)}</span>
          <code>${escapeHtml(shortHash(artifact.sha256))}</code>
        </div>
      `;
    })
    .join("");
  outputs.requiredEvidenceRows.innerHTML = (pack.required_evidence || [])
    .map((item) => `
      <div class="evidence-row required-row">
        <strong>${escapeHtml(item.item || "required_evidence")}</strong>
        <em class="${item.status === "complete" ? "is-pass" : "is-fail"}">${escapeHtml(item.status || "missing")}</em>
        <span>${escapeHtml(item.reason || "")}</span>
      </div>
    `)
    .join("");
}

async function loadClaimLedger() {
  try {
    if (window.location.protocol === "file:") {
      state.claimLedger = bundledClaimLedger;
    } else {
      const response = await fetch("data/claim_ledger.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`claim ledger ${response.status}`);
      state.claimLedger = await response.json();
    }
  } catch (error) {
    state.claimLedger = bundledClaimLedger;
  }
  renderClaimLedger();
}

function renderClaimLedger() {
  if (!outputs.claimLedgerSummary || !outputs.claimLedgerRows) return;
  const ledger = state.claimLedger || bundledClaimLedger;
  const summary = ledger.summary || {};
  const claims = ledger.claims || [];
  outputs.claimLedgerSummary.textContent =
    `${formatNumber(summary.allowed_count || 0)} allowed / ${formatNumber(summary.blocked_count || 0)} blocked`;
  outputs.claimLedgerRows.innerHTML = claims
    .map((claim) => {
      const failed = [
        ...(claim.failed_required_gates || []),
        ...(claim.missing_required_artifacts || []).map((role) => `missing:${role}`),
      ];
      return `
        <div class="claim-row">
          <div>
            <strong>${escapeHtml(claim.claim_id || "claim")}</strong>
            <span>${escapeHtml(claim.title || "")}</span>
          </div>
          <em class="claim-status ${claimStatusClass(claim.status)}">${escapeHtml(claim.status || "unknown")}</em>
          <small>${escapeHtml(claim.claim_level || "unknown")}</small>
          <p>${escapeHtml(claim.public_statement || "")}</p>
          <code>${failed.length ? escapeHtml(failed.join(", ")) : "evidence gates satisfied"}</code>
        </div>
      `;
    })
    .join("") + koGuide("Claim Ledger 해설", [
      "allowed는 현재 evidence gate가 허용하는 공개 주장입니다.",
      "blocked는 증거가 부족해 논문이나 GitHub Pages에서 강하게 말하면 안 되는 주장입니다.",
      "missing 항목은 어떤 산출물이 추가되어야 차단이 풀리는지 보여줍니다.",
    ]);
}

async function loadArtifactLineage() {
  try {
    if (window.location.protocol === "file:") {
      state.artifactLineage = bundledArtifactLineage;
    } else {
      const response = await fetch("data/artifact_lineage.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`artifact lineage ${response.status}`);
      state.artifactLineage = await response.json();
    }
  } catch (error) {
    state.artifactLineage = bundledArtifactLineage;
  }
  renderArtifactLineage();
}

function renderArtifactLineage() {
  if (!outputs.artifactLineageSummary || !outputs.artifactLineageMap || !outputs.artifactLineageRows) return;
  const lineage = state.artifactLineage || bundledArtifactLineage;
  const summary = lineage.summary || {};
  outputs.artifactLineageSummary.textContent =
    `${formatNumber(summary.node_count || 0)} nodes / ${formatNumber(summary.edge_count || 0)} edges`;
  renderArtifactLineageMap(lineage);
  const rows = [
    { label: "Missing", value: summary.missing_count || 0 },
    { label: "Checksum mismatch", value: summary.checksum_mismatch_count || 0 },
    { label: "Cycles", value: summary.cycle_count || 0 },
    { label: "Evidence checks", value: (lineage.checksum_checks || []).length },
  ];
  outputs.artifactLineageRows.innerHTML = `
    ${koGuide("Artifact Lineage 해설", [
      "lineage는 공개 JSON 산출물이 어떤 순서로 서로 의존하는지 보여주는 그래프입니다.",
      "cycle이 있으면 재현성 검사가 자기 자신을 참조하게 되므로 논문용 evidence bundle로 부적절합니다.",
      "checksum mismatch가 0이어야 GitHub Pages의 숫자와 로컬 재현 결과가 같은 산출물을 가리킨다고 볼 수 있습니다.",
    ])}
    <div class="lineage-health ${summary.reproducible ? "is-pass" : "is-fail"}">
      <strong>${summary.reproducible ? "reproducible" : "needs review"}</strong>
      <span>${escapeHtml(lineage.policy?.reason || "")}</span>
    </div>
    ${rows
      .map((row) => `
        <div class="lineage-stat">
          <span>${escapeHtml(row.label)}</span>
          <strong>${formatNumber(row.value)}</strong>
        </div>
      `)
      .join("")}
    ${(lineage.findings || [])
      .slice(0, 2)
      .map((finding) => `
        <div class="lineage-finding">
          <strong>${escapeHtml(finding.check || "finding")}</strong>
          <span>${escapeHtml(finding.message || "")}</span>
        </div>
      `)
      .join("")}
  `;
}

function renderArtifactLineageMap(lineage) {
  const svg = outputs.artifactLineageMap;
  const width = 1180;
  const height = 380;
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.innerHTML = "";
  const positions = new Map([
    ["manifest", { x: 30, y: 42 }],
    ["snapshot_manifest", { x: 198, y: 42 }],
    ["collection_matrix", { x: 198, y: 102 }],
    ["collection_power", { x: 366, y: 102 }],
    ["provenance_requirements", { x: 198, y: 162 }],
    ["provenance_audit", { x: 366, y: 162 }],
    ["baseline_acceptance", { x: 534, y: 102 }],
    ["baseline_promotion_plan", { x: 702, y: 102 }],
    ["collection_handoff", { x: 534, y: 162 }],
    ["collection_submission_contract", { x: 702, y: 162 }],
    ["collection_submission_lint", { x: 870, y: 132 }],
    ["collection_fixture_audit", { x: 870, y: 192 }],
    ["collection_intake", { x: 1020, y: 162 }],
    ["attribution_grid", { x: 30, y: 252 }],
    ["null_calibration", { x: 198, y: 252 }],
    ["replication_audit", { x: 366, y: 252 }],
    ["feature_vectors", { x: 198, y: 312 }],
    ["classifier_report", { x: 366, y: 312 }],
    ["readiness", { x: 534, y: 252 }],
    ["project_evolution", { x: 534, y: 312 }],
    ["evidence_pack", { x: 870, y: 242 }],
    ["claim_ledger", { x: 1020, y: 242 }],
  ]);
  appendSvg(svg, "text", { x: 30, y: 24, class: "chart-title" }).textContent = "artifact dependency DAG";
  (lineage.edges || []).forEach((edge) => {
    const start = positions.get(edge.from);
    const end = positions.get(edge.to);
    if (!start || !end) return;
    appendSvg(svg, "path", {
      d: `M ${start.x + 112} ${start.y + 20} C ${start.x + 150} ${start.y + 20}, ${end.x - 36} ${end.y + 20}, ${end.x} ${end.y + 20}`,
      fill: "none",
      stroke: edge.valid ? "#c6ccd8" : colors.danger,
      "stroke-width": 2,
    });
  });
  const nodesByRole = new Map((lineage.nodes || []).map((node) => [node.role, node]));
  positions.forEach((point, role) => {
    const node = nodesByRole.get(role) || {};
    const exists = node.exists !== false;
    const color = !exists ? colors.danger : role === "evidence_pack" || role === "claim_ledger" ? colors.indigo : colors.teal;
    appendSvg(svg, "rect", {
      x: point.x,
      y: point.y,
      width: 124,
      height: 44,
      rx: 7,
      fill: "#ffffff",
      stroke: color,
      "stroke-width": 2,
    });
    appendSvg(svg, "circle", { cx: point.x + 14, cy: point.y + 15, r: 4, fill: color });
    wrapSvgText(svg, role.replaceAll("_", " "), point.x + 26, point.y + 16, 14, 2);
  });
}

async function loadDecisionProtocol() {
  try {
    if (window.location.protocol === "file:") {
      state.decisionProtocol = bundledDecisionProtocol;
    } else {
      const response = await fetch("data/decision_protocol.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`decision protocol ${response.status}`);
      state.decisionProtocol = await response.json();
    }
  } catch (error) {
    state.decisionProtocol = bundledDecisionProtocol;
  }
  renderDecisionProtocol();
}

function renderDecisionProtocol() {
  if (!outputs.decisionProtocolSummary || !outputs.decisionProtocolRows) return;
  const protocol = state.decisionProtocol || bundledDecisionProtocol;
  const summary = protocol.summary || {};
  outputs.decisionProtocolSummary.textContent =
    `${formatNumber(summary.allowed_count || 0)} allowed / ${formatNumber(summary.blocked_count || 0)} blocked`;
  outputs.decisionProtocolRows.innerHTML = (protocol.decisions || [])
    .map((decision) => `
      <div class="decision-row">
        <div>
          <strong>${escapeHtml(decision.decision_id || "decision")}</strong>
          <span>${escapeHtml(decision.title || "")}</span>
        </div>
        <em class="claim-status ${claimStatusClass(decision.status)}">${escapeHtml(decision.status || "unknown")}</em>
        <small>${escapeHtml(decision.track || "research")}</small>
        <p>${escapeHtml(decision.threshold || "")}</p>
        <code>${(decision.blocking_items || []).length ? escapeHtml(decision.blocking_items.join(", ")) : "promotion rule satisfied"}</code>
      </div>
    `)
    .join("");
}

async function loadFalsificationBattery() {
  try {
    if (window.location.protocol === "file:") {
      state.falsificationBattery = bundledFalsificationBattery;
    } else {
      const response = await fetch("data/falsification_battery.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`falsification battery ${response.status}`);
      state.falsificationBattery = await response.json();
    }
  } catch (error) {
    state.falsificationBattery = bundledFalsificationBattery;
  }
  renderFalsificationBattery();
}

function renderFalsificationBattery() {
  if (!outputs.falsificationSummary || !outputs.falsificationRows) return;
  const battery = state.falsificationBattery || bundledFalsificationBattery;
  const summary = battery.summary || {};
  outputs.falsificationSummary.textContent =
    `${formatNumber(summary.pass_count || 0)} pass / ${formatNumber(summary.fail_count || 0)} fail`;
  outputs.falsificationRows.innerHTML = (battery.checks || [])
    .map((check) => `
      <div class="falsification-row">
        <div>
          <strong>${escapeHtml(check.check || "check")}</strong>
          <span>${escapeHtml(check.message || "")}</span>
        </div>
        <em class="check-status ${checkStatusClass(check.status)}">${escapeHtml(check.status || "unknown")}</em>
        <small>${escapeHtml(check.severity || "research")}</small>
        <p>${escapeHtml(summary.claim_floor || "unknown")}</p>
        <code>${escapeHtml(compactEvidence(check.evidence || {}))}</code>
      </div>
    `)
    .join("");
}

async function loadPublicationConsistency() {
  try {
    if (window.location.protocol === "file:") {
      state.publicationConsistency = bundledPublicationConsistency;
    } else {
      const response = await fetch("data/publication_consistency.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`publication consistency ${response.status}`);
      state.publicationConsistency = await response.json();
    }
  } catch (error) {
    state.publicationConsistency = bundledPublicationConsistency;
  }
  renderPublicationConsistency();
}

function renderPublicationConsistency() {
  if (!outputs.publicationConsistencySummary || !outputs.publicationConsistencyRows) return;
  const report = state.publicationConsistency || bundledPublicationConsistency;
  const summary = report.summary || {};
  outputs.publicationConsistencySummary.textContent =
    `${escapeHtml(summary.status || "unknown")} · ${formatNumber(summary.pass_count || 0)} pass / ${formatNumber(summary.fail_count || 0)} fail`;
  outputs.publicationConsistencyRows.innerHTML = (report.checks || [])
    .map((check) => `
      <div class="consistency-row">
        <div>
          <strong>${escapeHtml(check.check || "check")}</strong>
          <span>${escapeHtml(check.message || "")}</span>
        </div>
        <em class="check-status ${checkStatusClass(check.status)}">${escapeHtml(check.status || "unknown")}</em>
        <small>${escapeHtml(check.severity || "research")}</small>
        <p>${escapeHtml(report.policy?.post_pack_audit ? "post-pack audit" : "inline audit")}</p>
        <code>${escapeHtml(compactEvidence(check.evidence || {}))}</code>
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
    ${koGuide("Attribution Grid 해설", [
      "attribution은 의심 데이터셋이 어떤 생성기 계열과 통계적으로 가까운지 비교하는 작업입니다.",
      "controlled accuracy는 bit length 같은 단순 confound를 통제한 뒤에도 분류 신호가 남는지 보는 값입니다.",
      "여기서 좋은 결과가 나와도 현재 범위는 합성 데이터 검증이며, 실제 라이브러리 단정은 아닙니다.",
    ])}
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

async function loadNullCalibration() {
  try {
    if (window.location.protocol === "file:") {
      state.nullCalibration = bundledNullCalibration;
    } else {
      const response = await fetch("data/null_calibration.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`null calibration ${response.status}`);
      state.nullCalibration = await response.json();
    }
  } catch (error) {
    state.nullCalibration = bundledNullCalibration;
  }
  renderNullCalibration();
}

function renderNullCalibration() {
  if (!outputs.nullCalibrationSummary || !outputs.nullCalibrationRows) return;
  const calibration = state.nullCalibration || bundledNullCalibration;
  const summary = calibration.summary || {};
  const method = calibration.method || {};
  outputs.nullCalibrationSummary.innerHTML = `
    <div><span>Iterations</span><strong>${formatNumber(method.iterations || 0)}</strong><small>row-structured null</small></div>
    <div><span>Top profile</span><strong>${escapeHtml(summary.top_profile || "n/a")}</strong><small>family-wise p ${formatPValue(summary.top_familywise_p_value)}</small></div>
    <div><span>Survivors</span><strong>${formatNumber(summary.familywise_survivor_count || 0)}</strong><small>family-wise controlled</small></div>
    <div><span>Claim floor</span><strong>${escapeHtml(summary.claim_floor || "unknown")}</strong><small>not real-world attribution</small></div>
  `;
  outputs.nullCalibrationRows.innerHTML = (calibration.profiles || [])
    .map((profile) => `
      <div class="null-row">
        <strong>${escapeHtml(profile.profile || "profile")}</strong>
        <span>${formatPercent(profile.observed_controlled_accuracy)} observed</span>
        <span>${formatSignedPercent(profile.observed_lift)} lift</span>
        <span>${formatPercent(profile.null_ci95_low)}-${formatPercent(profile.null_ci95_high)} null 95%</span>
        <code>FW p=${formatPValue(profile.familywise_p_value)}</code>
        <em class="${profile.interpretation === "familywise_survives_null" ? "is-pass" : "is-null"}">${escapeHtml(profile.interpretation || "unknown")}</em>
      </div>
    `)
    .join("");
}

async function loadReplicationAudit() {
  try {
    if (window.location.protocol === "file:") {
      state.replicationAudit = bundledReplicationAudit;
    } else {
      const response = await fetch("data/replication_audit.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`replication audit ${response.status}`);
      state.replicationAudit = await response.json();
    }
  } catch (error) {
    state.replicationAudit = bundledReplicationAudit;
  }
  renderReplicationAudit();
}

function renderReplicationAudit() {
  if (!outputs.replicationAuditSummary || !outputs.replicationAuditRows) return;
  const audit = state.replicationAudit || bundledReplicationAudit;
  const summary = audit.summary || {};
  const method = audit.method || {};
  outputs.replicationAuditSummary.innerHTML = `
    <div><span>Settings</span><strong>${formatNumber(summary.setting_count || 0)}</strong><small>limit/train/test cells</small></div>
    <div><span>Stable profiles</span><strong>${formatNumber(summary.stable_profile_count || 0)}</strong><small>${escapeHtml((summary.stable_profiles || []).join(", ") || "none")}</small></div>
    <div><span>Lift threshold</span><strong>${formatSignedPercent(method.lift_threshold || 0)}</strong><small>over random baseline</small></div>
    <div><span>Claim floor</span><strong>${escapeHtml(summary.claim_floor || "unknown")}</strong><small>synthetic only</small></div>
  `;
  outputs.replicationAuditRows.innerHTML = (audit.profiles || [])
    .map((profile) => `
      <div class="replication-row">
        <strong>${escapeHtml(profile.profile || "profile")}</strong>
        <span>${formatNumber(profile.replicated_setting_count || 0)} / ${formatNumber(profile.setting_count || 0)} settings</span>
        <span>${formatPercent(profile.replicated_ratio || 0)} replicated</span>
        <span>${formatSignedPercent(profile.minimum_setting_lift || 0)} min lift</span>
        <code>FW p=${formatPValue(profile.familywise_p_value)}</code>
        <em class="${profile.status === "replicated_and_null_calibrated" ? "is-pass" : "is-null"}">${escapeHtml(profile.status || "unknown")}</em>
      </div>
    `)
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

function formatDimensionName(value) {
  return String(value).replaceAll("_", " ");
}

function readinessClass(label) {
  if (label === "research_ready") return "is-ready";
  if (label === "prototype_ready") return "is-prototype";
  if (label === "scaffold_ready") return "is-scaffold";
  return "is-not-started";
}

function priorityRank(priority) {
  return { P0: 0, P1: 1, P2: 2 }[priority] ?? 9;
}

function claimStatusClass(status) {
  if (status === "allowed") return "is-allowed";
  if (status === "qualified") return "is-qualified";
  if (status === "blocked") return "is-blocked";
  return "is-unknown";
}

function checkStatusClass(status) {
  if (status === "pass") return "is-pass";
  if (status === "warn") return "is-warn";
  if (status === "fail") return "is-fail";
  return "is-unknown";
}

function compactEvidence(evidence) {
  const entries = Object.entries(evidence || {}).slice(0, 3);
  if (!entries.length) return "no extra evidence";
  return entries
    .map(([key, value]) => {
      const text = Array.isArray(value)
        ? value
            .map((item) => (typeof item === "object" ? item.profile || item.check || JSON.stringify(item) : item))
            .join("|")
        : typeof value === "object"
          ? JSON.stringify(value)
          : String(value);
      return `${key}:${text}`;
    })
    .join(", ");
}

function formatDimensionEvidence(name, dimension) {
  if (name === "sim_to_real") {
    const cap = dimension.readiness_cap
      ? ` cap ${escapeHtml(dimension.readiness_cap.max_label || "scaffold_ready")} from ${formatPercent(dimension.raw_score || dimension.score || 0)}.`
      : "";
    return `${formatNumber(dimension.available_count || 0)} attribution-ready, ${formatNumber(dimension.public_control_count || 0)} public controls, ${formatNumber(dimension.planned_count || 0)} planned.${cap}`;
  }
  if (name === "attribution_validation") {
    return `${formatNumber(dimension.rows || 0)} rows, ${formatNumber(dimension.repeats || 0)} repeats, ${(dimension.robust_profiles || []).join(", ") || "no robust profile"}.`;
  }
  if (name === "classifier") {
    return `${formatNumber(dimension.vector_count || 0)} vectors across ${formatNumber(dimension.label_count || 0)} labels, scope ${dimension.claim_scope || "unknown"}.`;
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

function displayTvLabel(label, targetTv) {
  if (Number.isFinite(Number(targetTv))) {
    return formatPercent(Number(targetTv)).replace(".0%", "%");
  }
  const match = String(label || "").match(/^(\d+)(?:_(\d+))?pct$/);
  if (match) return `${match[1]}${match[2] ? `.${match[2]}` : ""}%`;
  return String(label || "target");
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
