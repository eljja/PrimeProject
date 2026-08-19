# PrimeProject

[![PrimeProject CI](https://github.com/eljja/PrimeProject/actions/workflows/ci.yml/badge.svg)](https://github.com/eljja/PrimeProject/actions/workflows/ci.yml)

<p align="right">
  <a href="#english"><strong>English</strong></a>
  ·
  <a href="#한국어"><strong>한국어</strong></a>
  ·
  <a href="https://eljja.github.io/PrimeProject/?lang=en"><strong>GitHub Pages EN</strong></a>
  ·
  <a href="https://eljja.github.io/PrimeProject/?lang=ko"><strong>GitHub Pages KO</strong></a>
</p>

## English

`PrimeProject` is a dual-track research platform: it audits proof routes for four open problems and studies generator fingerprints in cryptographic mathematical objects. The implementation separates exact mathematics, bounded computation, rejected routes, and blocked real-world attribution claims.

Language support: the GitHub Pages app includes an `EN / KO` switch in the top bar. The switch localizes the page shell, navigation, main headings, proof workbench labels, and publication-boundary guidance while keeping canonical artifact schema labels in English for reproducibility.

## Publication claim boundary / 논문 제출용 주장 경계

English: PrimeProject is a reproducible defensive research framework. It supports bounded certificates, controlled synthetic generator-fingerprint experiments, public-safe collection contracts, and claim-governance artifacts. It does not claim to predict secure cryptographic primes, attribute real-world keys without accepted baselines, or prove the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, or Twin Prime conjecture.

한국어: PrimeProject는 재현 가능한 방어적 연구 프레임워크다. 현재 지원하는 것은 bounded certificate, 통제된 합성 generator-fingerprint 실험, 공개 안전 수집 계약, claim-governance 산출물이다. 안전한 암호 소수를 예측했다거나, accepted baseline 없이 실세계 키의 생성 라이브러리를 단정했다거나, 리만가설/콜라츠/골드바흐/Twin Prime을 증명했다고 주장하지 않는다.

All Markdown documents are reviewed against this boundary in [Publication-Ready Document Review](docs/publication-ready-review.md).

For transferring the open-problem workbench to another LLM, see [LLM Open-Problem Handoff](docs/llm-open-problem-handoff.md). It includes the current top attack tickets and copy-paste prompts for continuing the proof-search attempt without overstating the result.

For the canonical keep/discard audit of all four open-problem tracks, see [Four-Problem Research Consolidation](docs/open-problem-research-consolidation-2026-07-10.md). This bilingual document separates problem-specific computation from methodological transfer artifacts and names the exact infinite theorem still missing in each problem.

The latest four-problem continuation is
[TICKET-230: Quantitative Recurrence, Necklace Invariance, Fourier Aggregation, and Local Centering](docs/quantitative-recurrence-necklace-fourier-centering.md),
with a separate [Korean report](docs/quantitative-recurrence-necklace-fourier-centering.ko.md).
It proves four narrower structural results: an unavoidable `T^(-2/m)` near-
alias rate for every fixed finite dilation family; cyclic-necklace invariance
of Collatz cycle divisibility and `gcd(D,B)`; a Fourier counterfamily showing
that modewise `o(W)` does not imply pointwise convolution positivity; and the
exact modulo-five shift-two quadratic mean `1/3`, correcting the previous raw-
zero target. These are partial structural and no-go lemmas, not parent-problem
resolutions. TICKET-229 is preserved in
[English](docs/band-frame-semilinear-character-barriers.md) and
[Korean](docs/band-frame-semilinear-character-barriers.ko.md). TICKET-228 is preserved in
[English](docs/near-alias-affine-language-residue-spectrum.md) and
[Korean](docs/near-alias-affine-language-residue-spectrum.ko.md). TICKET-227 is
preserved in [English](docs/mellin-block-buchstab-lifts.md) and
[Korean](docs/mellin-block-buchstab-lifts.ko.md).
Every conjecture remains `open_not_proven`; the machine resolution count is
zero.

The immediate predecessor is
[TICKET-225: Arithmetic Remainder Localization](docs/arithmetic-remainder-localization.md),
with a [Korean report](docs/arithmetic-remainder-localization.ko.md).
The earlier threshold result is
[TICKET-224: Sharp Completeness Thresholds](docs/sharp-completeness-thresholds.md),
with its [Korean report](docs/sharp-completeness-thresholds.ko.md).

An earlier preserved input is
[TICKET-223: Exponential Tails, Local Duality, and Fixed-Sieve No-Go Results](docs/exponential-tail-local-duality-no-go.md),
with its [Korean report](docs/exponential-tail-local-duality-no-go.ko.md).

An earlier preserved input is
[TICKET-222: Lossless Coupling and Biased-Parity Corrections](docs/lossless-coupling-biased-parity.md),
with its [Korean report](docs/lossless-coupling-biased-parity.ko.md).

The preserved direct input is
[TICKET-221: Sharp Obstruction Certificates](docs/sharp-obstruction-certificates.md),
with its [Korean report](docs/sharp-obstruction-certificates.ko.md).

The preserved direct input is
[TICKET-220: Dyadic Partition, Primitive-Word Closure, Refinement Stability, and a Finite-Wheel CRT No-Go](docs/dyadic-partition-primitive-refinement-crt.md),
with its [Korean report](docs/dyadic-partition-primitive-refinement-crt.ko.md).

The preserved direct input is
[TICKET-219: Band-pass Defects, Matveev Closure, Cross-fitted Moments, and Qualitative Abel Growth](docs/bandpass-matveev-crossfit-qualitative-abel.md),
with its [Korean report](docs/bandpass-matveev-crossfit-qualitative-abel.ko.md).

The preserved direct input is
[TICKET-218: Adaptive Radii, Exponential Spikes, Residual Moments, and Abel Surplus](docs/adaptive-radius-spike-residual-surplus.md),
with a separate [Korean report](docs/adaptive-radius-spike-residual-surplus.ko.md).

The preserved direct input is
[TICKET-217: Relative Thresholds, Convergent Compression, Moment Support, and Critical Abel Tails](docs/relative-threshold-convergent-moment-tail.md),
with a separate [Korean report](docs/relative-threshold-convergent-moment-tail.ko.md).
It proves the normalized multi-radius RH defect certificate; compresses every
single-mountain Collatz candidate to an upper continued-fraction convergent and
excludes `k<71,356,888`; proves the sharp weighted second-moment Goldbach
full-support condition; and fixes the critical `2 log log X` Twin Abel-tail
asymptotic.
These are exact partial or no-go results, not resolutions. Every conjecture
remains `open_not_proven`; the machine resolution count is zero.

The preserved direct input is
[TICKET-216: Laplace Defects, Cross-Power GCDs, Radix Histograms, and Tauberian Tails](docs/laplace-gcd-radix-tauberian.md),
with a separate [Korean report](docs/laplace-gcd-radix-tauberian.ko.md).
It proves the first-atom RH Laplace certificate, a cross-power gcd necessity
for single-mountain Collatz cycles, a lossless exact finite Goldbach histogram
radix, and a quantitative Twin Abel-to-count bracket with its fixed-dilation
tail limitation.

The preserved direct input is
[TICKET-215: Lattice Certificates, Power Near-Collisions, Exception Counts, and Abel Boundaries](docs/lattice-nearcollision-exception-abel.md),
with a separate [Korean report](docs/lattice-nearcollision-exception-abel.ko.md).
It proves a sharp even-lattice interface for cofinal RH defect certificates;
reduces single-mountain Collatz words `1^k2^m` to one exponential
near-collision per `k` and excludes it through `k=4096`; upgrades the
Goldbach exponential selector to exact exception counting with a sharp scale;
and converts the exact Twin gap-two channel into an Abel boundary-divergence
target while refuting finite-radius promotion.

The preserved direct input is
[TICKET-214: Cofinal Defects, Seven-One Cycles, Exponential Witnesses, and Cardinal Gap Selection](docs/cofinal-sevenone-exponential-cardinal.md),
with a separate [Korean report](docs/cofinal-sevenone-exponential-cardinal.ko.md).

The preserved direct input is
[TICKET-213: Multiplicity, Six-One Cycles, Polynomial Majorants, and Gap Selectors](docs/multiplicity-sixone-polynomial-selector.md),
with a separate [Korean report](docs/multiplicity-sixone-polynomial-selector.ko.md).

The preserved direct input is
[TICKET-212: Even Defect, 2-Adic Ghosts, Full-Witness Products, and Gap Channels](docs/even-defect-ghost-bonferroni-gapchannel.md),
with a separate [Korean report](docs/even-defect-ghost-bonferroni-gapchannel.ko.md).

The preserved direct input is
[TICKET-211: Winding Localization, Collatz Integrality, Full-Range Goldbach Exceptions, and Unit-Scale Twin Deserts](docs/winding-density-fullrange-unitscale.md),
with a separate [Korean report](docs/winding-density-fullrange-unitscale.ko.md).

The preserved direct input is
[TICKET-210: Cofinal Lines, Five-One Cycles, Prime-Gap Transfer, and Scaled Twin Deserts](docs/cofinal-fiveone-primegap-scaledtwin.md),
with a separate [Korean report](docs/cofinal-fiveone-primegap-scaledtwin.ko.md).

The preserved direct input is
[TICKET-209: Normalized Boundaries, Four-One Cycles, Covering Congruences, and Factorial Twin Deserts](docs/normalized-fourone-covering-factorial.md),
with a separate [Korean report](docs/normalized-fourone-covering-factorial.ko.md).

The preserved direct input is
[TICKET-208: Vertical Clearance, Three-One Cycles, Unit-Log Witnesses, and Cyclotomic Correlations](docs/vertical-threeone-unitlog-cyclotomic.md),
with a separate [Korean report](docs/vertical-threeone-unitlog-cyclotomic.ko.md).

The preserved previous boundary is
[TICKET-207: Dihedral Boundaries, Two-One Cycles, Logarithmic Witnesses, and Abel Leakage](docs/dihedral-twoone-logwitness-abel.md),
with a separate [Korean report](docs/dihedral-twoone-logwitness-abel.ko.md).

The preserved previous boundary is
[TICKET-206: Adaptive Certificates, Single-One Cycles, CRT Witnesses, and Omega Projectors](docs/adaptive-singleone-crt-projector.md),
with a separate [Korean report](docs/adaptive-singleone-crt-projector.ko.md).

The preserved previous boundary is
[TICKET-205: Winding Certificates, Cycle Extrema, Finite Witnesses, and Omega Weights](docs/winding-extremal-finite-omega.md),
with a separate [Korean report](docs/winding-extremal-finite-omega.ko.md).

The preserved previous boundary is
[TICKET-204: Continuous Certificates, Primitive Necklaces, and Parity Kernels](docs/mesh-necklace-exceptional-kernel.md),
with a separate [Korean report](docs/mesh-necklace-exceptional-kernel.ko.md).

The earlier preserved boundary is
[TICKET-203: Rouché Transfer, Signed Valuation Transfer, and Pointwise Target Correction](docs/rouche-transfer-pointwise-primorial.md),
with a separate [Korean report](docs/rouche-transfer-pointwise-primorial.ko.md).

The earlier preserved boundary is
[TICKET-202: Exact Hermite Data, Long-Run Deformations, and Parity Scale](docs/exact-hermite-deformation-parity-scale.md),
with a separate [Korean report](docs/exact-hermite-deformation-parity-scale.ko.md).
It strengthens the RH finite-information no-go to finitely many exact Hermite
constraints; excludes every `r,k>=2`, `t>=0`, and cyclic rotation of
`1^k 2^(2k+t) (1 2^2)^(r-1)`; proves that the aggregate Goldbach `P2` relative
Liouville defect tends to zero; and proves that a fixed Twin relative defect
plus Chen-order mass would imply a Hardy-Littlewood-order quantitative lower
bound. These are exact partial theorems and target recalibrations, not
resolutions. Every conjecture remains `open_not_proven`; the machine resolution
count is zero.

The preserved previous boundary is
[TICKET-201: Finite Information, All-Run Collatz, and Liouville Parity](docs/finite-information-allrun-liouville-parity.md),
with a separate [Korean report](docs/finite-information-allrun-liouville-parity.ko.md).

The preserved previous boundary is
[TICKET-199: Symmetric Sampling, Two-Run Obstruction, and the Squarefree-Lambda Filter](docs/symmetric-sampling-two-run-squarefree-filter.md),
with a separate [Korean report](docs/symmetric-sampling-two-run-squarefree-filter.ko.md).

The preserved previous boundary is
[TICKET-198: Verified Height, Primitive Words, and Quantifier Strength](docs/verified-height-primitive-word-quantifier-strength.md),
with a separate [Korean report](docs/verified-height-primitive-word-quantifier-strength.ko.md).
It transfers the peer-reviewed finite-height RH result, proves fixed-run
primitive scalar-admissible Collatz families remain infinite, and corrects the
quantifier strength of the previous Goldbach and Twin targets.

The preserved previous boundary is
[TICKET-196: Rouché Exhaustion, Collatz Density, and Overlap-Corrected Prime-Power Budgets](docs/rouche-density-overlap.md),
with a separate [Korean report](docs/rouche-density-overlap.ko.md).

The preserved previous boundary is
[TICKET-195: Finite-Jet Boundaries, Eleven-One Decidability, and Prime-Square Layers](docs/finitejet-elevenone-squarelayer.md),
with a separate [Korean report](docs/finitejet-elevenone-squarelayer.ko.md).

The preserved previous boundary is
[TICKET-194: Dense-Core Extension, Ten-One Cycles, and Theta Layers](docs/densecore-tenone-theta-layers.md),
with a separate [Korean report](docs/densecore-tenone-theta-layers.ko.md).

The preserved previous boundary is
[TICKET-193: Everywhere Extension, Nine-One Cycles, and Parity Envelopes](docs/everywhere-nineone-parity-envelope.md),
with a separate [Korean report](docs/everywhere-nineone-parity-envelope.ko.md).

The preserved previous boundary is
[TICKET-192: Uniform Extension, Eight-One Cycles, and Weighted Envelopes](docs/uniform-eightone-weighted-envelope.md),
with a separate [Korean report](docs/uniform-eightone-weighted-envelope.ko.md).

The preserved previous boundary is
[TICKET-191: Probe Topology, Seven-One Cycles, and Exact Arithmetic Targets](docs/probe-sevenone-budget-granularity.md),
with a separate [Korean report](docs/probe-sevenone-budget-granularity.ko.md).

The preserved previous boundary is
[TICKET-190: Cauchy Cores, Six-One Cycles, and Quantifier Transfer](docs/cauchy-sixone-quantifier-transfer.md),
with a separate [Korean report](docs/cauchy-sixone-quantifier-transfer.ko.md).

The preserved previous boundary is
[TICKET-189: Summable Cores, Five-One Cycles, and Prime-Power Subtraction](docs/summable-core-fiveone-sublinear-shift.md),
with a separate [Korean report](docs/summable-core-fiveone-sublinear-shift.ko.md).

The preserved previous boundary is
[TICKET-188: Common Forms, Four-One Cycles, Prime-Power Contamination, and Dyadic Oracles](docs/nested-fourone-primepower-dyadic.md),
with a separate [Korean report](docs/nested-fourone-primepower-dyadic.ko.md).

The preserved previous boundary is
[TICKET-187: Finite Weil Provenance, Three-One Cycles, Survivor Signatures, and Quantized Intervals](docs/positive-ray-threeone-signature-interval.md),
with a separate [Korean report](docs/positive-ray-threeone-signature-interval.ko.md).

The preserved previous boundary is
[TICKET-186: Codimension, Two-One Cycles, Survivor Layers, and Quantized Margins](docs/codimension-twoone-layercake-quantization.md),
with a separate [Korean report](docs/codimension-twoone-layercake-quantization.ko.md).

An earlier preserved boundary is
[TICKET-185: Spectral Escape, Cycle Exclusion, Factor Horizons, and Integer Granularity](docs/spectral-cycle-factor-granularity.md),
with a separate [Korean report](docs/spectral-cycle-factor-granularity.ko.md).

An earlier preserved boundary is
[TICKET-184: Information Sufficiency and Proof-Route Correction](docs/information-sufficiency-route-correction.md),
with a separate [Korean report](docs/information-sufficiency-route-correction.ko.md).

The preserved previous boundary is
[TICKET-182: Sobolev, Divisibility, Translation, and Sibling Localization](docs/sobolev-divisibility-translation-sibling.md),
with a separate [Korean report](docs/sobolev-divisibility-translation-sibling.ko.md).

The preserved previous boundary is
[TICKET-181: Regularized Localization and Quantized Slack](docs/regularized-localization-quantized-slack.md),
with a separate [Korean report](docs/regularized-localization-quantized-slack.ko.md).

The preserved previous boundary is
[TICKET-180: Finite-Information Localization](docs/finite-information-localization.md),
with a separate [Korean report](docs/finite-information-localization.ko.md).

The preserved previous boundary is
[TICKET-179: Signed Symbols, Adaptive Valuation Layers, Discrete Targets, and
Centered Energy](docs/symbol-adaptive-discrete-centering.md), with a separate
[Korean report](docs/symbol-adaptive-discrete-centering.ko.md).

The preserved previous boundary is
[TICKET-178: Toeplitz Summability, Collatz Low Bits, Goldbach Frequency Splits,
and Cross-Gram Zero Modes](docs/toeplitz-lowbit-frequency-split-zeromode.md),
with a separate [Korean report](docs/toeplitz-lowbit-frequency-split-zeromode.ko.md).

The preserved previous boundary is
[TICKET-177: Comparison Majorants, Six-Wheel Collatz Envelopes, Sobolev
Certificates, and Signed Cross-Gram Data](docs/comparison-wheel-sobolev-crossgram.md),
with a separate [Korean report](docs/comparison-wheel-sobolev-crossgram.ko.md).

The preserved previous boundary is [TICKET-176: Relative Cones, Harmonic
Collatz Corrections, Parity Aliases, and Weighted Schur
Circularity](docs/relative-cone-harmonic-alias-schur.md), with a separate
[Korean report](docs/relative-cone-harmonic-alias-schur.ko.md).

The preserved previous boundary is [TICKET-175: Relative Spectral Resolution,
Collatz-Equivalent Zero Lifts, Signed Farey Minors, and Haar Block
Operators](docs/relative-equivalence-signed-block.md), with a separate
[Korean report](docs/relative-equivalence-signed-block.ko.md).

The preserved previous boundary is
[TICKET-174: Tail Schedules, Unique Collatz Zero Lifts, Adaptive Goldbach
Selection, and Sharp Haar Scale Aggregation](docs/tail-lift-adaptive-scalepair.md),
with a separate [Korean report](docs/tail-lift-adaptive-scalepair.ko.md).

The earlier boundary is
[TICKET-173: Finite-Section Defects, Collatz Cylinder Stabilization,
Target-Aligned Goldbach Phase, and Tensor-Haar Scale Pairs](docs/finite-section-cylinder-phase-tensor.md),
with a separate [Korean report](docs/finite-section-cylinder-phase-tensor.ko.md).

The earlier boundary is
[TICKET-172: Structured KKT Inertia, Collatz Bridge Equivalence, Fourier L1
Positivity, and Dyadic Mixed Variation](docs/structure-equivalence-l1-variation.md),
with a separate [Korean report](docs/structure-equivalence-l1-variation.ko.md).

The earlier boundary is
[TICKET-171: Relative KKT Geometry, a Collatz Ghost Ray, Signed Goldbach Phase,
and Haar Type II](docs/relative-ghost-phase-haar.md), with a separate
[Korean report](docs/relative-ghost-phase-haar.ko.md).

The earlier boundary is
[TICKET-170: Interval Gaps, Collatz Tail Closure, Autocorrelation Besov Control,
and Multiscale Type II](docs/interval-tail-besov-multiscale.md).

The earlier boundary is
[TICKET-169: KKT Inertia, Exact Collatz Child Lifts, Spectral Autocorrelation,
and Twin Prime-Power Removal](docs/kkt-childlift-autocorrelation-primepower.md).

The earlier boundary is
[TICKET-168: Fixed Neutral Cores, Least-Realizer Descent, Phase-Blind Minimax,
and Twin Parity Main Terms](docs/fixedcore-leastrealizer-phase-paritymain.md).

The earlier boundary is
[TICKET-167: Cofinal Cores, Exact Collatz Realizer Counts, Goldbach Besov
Tails, and the Finest Twin Parity Scale](docs/cofinal-residue-besov-parity.md).

The earlier boundary is
[TICKET-155: Range Exactness, Initial-Prefix Descent, Sublinear Wheels, and
Conditional Transfer](docs/range-prefix-sublinear-conditional.md).

The still earlier boundary is
[TICKET-154: Compact Schur Tails, Reverse-Suffix Descent, Wheel Projection,
and Least-Factor Deficit](docs/compact-suffix-wheel-leastfactor.md). Its
Collatz occurrence-to-induction bridge is superseded by the explicit
TICKET-155 correction.

The corrected TICKET77 sublemma is written separately in [Collatz Fixed-Prefix Boundary Orbit](docs/collatz-fixed-prefix-boundary-orbit.md), with a bilingual theorem statement, equality-rollback correction, periodic-orbit classification, 2-adic admissibility analysis, and explicit remaining bridge.

TICKET78 is documented in [Collatz Finite-Cylinder Natural-Admissibility No-Go](docs/collatz-finite-cylinder-admissibility-no-go.md). It connects the corrected boundary orbit to established 2-adic conjugacy, proves that every finite accelerated valuation cylinder contains infinitely many positive integers, and blocks finite purely 2-adic natural classifiers without claiming novelty for the classical conjugacy.

## What it does

- Loads RSA modulus and public prime records from JSON, CSV, PEM, DER, certificate, and CSR inputs.
- Extracts bit-length, low-bit, and small-prime residue fingerprints.
- Checks RSA datasets for duplicate moduli, shared prime factors, small modulus size, near-square factorization risk, and ROCA-like constrained residue fingerprints.
- Recognizes selected ECC field primes.
- Generates synthetic toy RSA datasets for validation experiments.
- Explores algorithm-induced prime measures and next-prime candidate ranking in the PrimeProject Conjecture Lab.
- Extracts generator fingerprints from prime-like parameters, including residues, low bits, and local prime-gap context.
- Builds known-good generator baselines and compares suspicious datasets by fingerprint distance with sample-quality confidence.
- Benchmarks generator attribution against synthetic ground-truth samples with accuracy, confusion matrices, feature ablation, bit-length confound control, and paired confound-grid deltas.
- Calibrates controlled attribution profiles against a row-structured random-label null with family-wise correction across multiple profiles.
- Audits setting-level replication so null-calibrated profiles must repeat across limit, train-count, and test-count cells.
- Registers real-world baseline manifests for OpenSSL, BoringSSL, Go, Bitcoin Core, and wallet/library samples without publishing sensitive key material.
- Defines a real-world collection matrix for matched OpenSSL/BoringSSL/Go RSA-prime targets and Bitcoin signature metadata before stronger claims are allowed.
- Estimates sample-size power floors so collection targets are marked as coarse screening or stronger evidence before publication claims.
- Generates and audits provenance contracts for real-world baselines so library version, build flags, RNG source, commands, aggregate artifact hashes, and forbidden public sensitive fields are checked before attribution claims.
- Combines availability, provenance, and sample-power tiers into baseline acceptance gates before a real-world baseline can support attribution claims.
- Produces a baseline promotion plan that identifies the shortest collection/provenance path from blocked baselines to accepted real-world evidence.
- Converts the promotion path into a public-safe collection handoff packet with prioritized tasks, sample floors, provenance blockers, and forbidden raw-material fields.
- Publishes a machine-readable collection submission contract with task templates, required record fields, checksum rules, optional record identity binding, public feature-vector path policy, provenance identity binding, feature-vector schema rules, and forbidden public fields.
- Lints candidate public collection submissions against that contract before intake so collectors can fix task, checksum, feature-vector, duplicate, sample-floor, and public-safety errors locally.
- Audits public-safe submission fixtures that prove the linter's pass, warning, missing-feature, forbidden-field, provenance-identity, feature-label, record-identity, feature-path, and reused-checksum behavior before real collection records are accepted.
- Validates submitted collection artifacts with an intake gate for sample floors, checksums, provenance records, embedded public feature-vector contracts, claim scope, duplicate task submissions, reused aggregate hashes, and forbidden public fields.
- Exports fixed-length fingerprint vectors and runs a dependency-free Crypto-Classifier baseline before heavier ML experiments.
- Scores end-to-end research readiness across Sim-to-Real baselines, attribution validation, classifier data, and Bitcoin integration.
- Bundles checksummed evidence packs that state publication gates and claim limits.
- Builds a claim ledger that maps each public-facing research claim to the gates and artifacts that allow, qualify, or block it.
- Builds an artifact lineage graph that audits public JSON dependencies, Evidence Pack checksums, and cyclic dependency risk.
- Audits public README/docs/GitHub Pages language so visible claims cannot exceed the current evidence boundary.
- Applies a pre-registered decision protocol that separates public demo, controlled synthetic, real-world attribution, and Bitcoin nonce-risk claim promotion.
- Runs a falsification battery with paired controls, negative controls, bit-length confound guards, and claim-promotion guards before stronger attribution claims can advance.
- Runs a publication consistency audit that checks Evidence Pack, Claim Ledger, Decision Protocol, and Falsification Battery agree on the same high-risk claim boundary.
- Audits Bitcoin secp256k1 constants and ECDSA signature metadata for defensive nonce-risk indicators.

## Interactive Conjecture Lab

Open the GitHub Pages app: [https://eljja.github.io/PrimeProject/](https://eljja.github.io/PrimeProject/)

The landing view is evidence-first. It starts with the current TICKET-230 boundary, four exact structural lemmas, four discarded or corrected routes, the unresolved lemma for each problem, and a visible `0 / 4 resolved` guard. The historical experiment dashboard remains available as **Prime Explorer**, while detailed evidence is grouped under Research, Open Problems, Applied Labs, Evidence, and More Analysis.

Open problem subpages:

- [Riemann Workbench](https://eljja.github.io/PrimeProject/open-problems/riemann.html)
- [Collatz Workbench](https://eljja.github.io/PrimeProject/open-problems/collatz.html)
- [Goldbach Workbench](https://eljja.github.io/PrimeProject/open-problems/goldbach.html)
- [Twin Prime Workbench](https://eljja.github.io/PrimeProject/open-problems/twin-prime.html)

GitHub Pages is the canonical public runtime and loads the current public `data/*.json` artifact bundle. Direct `file://` opening is only an offline fallback smoke view and may show bundled fallback data. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

The live browser experiment can compute directly up to 10M with a logarithmic search-limit slider. Larger local runs can also be bundled as static Research Snapshots on GitHub Pages, so visitors can inspect precomputed SVG charts without recalculating them in the browser. The Bias Ranking Lab orders next-prime candidates with a toy density/residue/gap score for generator-bias analysis; it is not a cryptographic prime prediction engine.

The Research Atlas and Project Evolution panels read `data/project_evolution.json` and present a condensed research narrative: the supported contribution map, evidence ladder, open-problem proof map, academic blockers, six decisive metrics, a versioned visual change trail, a Hardening Map, one Evidence Spine, and a claim-boundary view that separates supported controlled-synthetic results from blocked real-world and Bitcoin attribution claims.

The Open Problem Proof Workbench provides four subpages for the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, and Twin Prime conjecture. Each page leads with the current exact theorem, discarded route, proof DAG, and remaining gap. The complete machinery remains available in five semantic groups: core status, reproducible evidence, proof program, formal review, and the historical ticket archive. No conjecture is presented as solved until an independently checkable infinite argument survives formal and peer review.

The latest proof-search track is TICKET-230. The RH track quantifies an
unavoidable `T^(-2/m)` near-alias sequence for every fixed finite dilation
family. The Collatz track proves cycle divisibility and `gcd(D,B)` are cyclic-
necklace invariants. Goldbach gives an exact aligned Fourier counterfamily to
modewise-to-pointwise promotion. Twin corrects the raw modulo-five quadratic
mean from zero to `1/3`. These are exact partial and no-go theorems, not
solutions. All four parent conjectures remain open and the machine resolution
count is zero.
See [TICKET230 EN](docs/quantitative-recurrence-necklace-fourier-centering.md),
[TICKET230 KO](docs/quantitative-recurrence-necklace-fourier-centering.ko.md),
[TICKET229 EN](docs/band-frame-semilinear-character-barriers.md),
[TICKET229 KO](docs/band-frame-semilinear-character-barriers.ko.md),
[TICKET228 EN](docs/near-alias-affine-language-residue-spectrum.md),
[TICKET228 KO](docs/near-alias-affine-language-residue-spectrum.ko.md),
[TICKET227 EN](docs/mellin-block-buchstab-lifts.md),
[TICKET227 KO](docs/mellin-block-buchstab-lifts.ko.md),
[TICKET226 EN](docs/signal-transfer-same-order-obstructions.md),
[TICKET226 KO](docs/signal-transfer-same-order-obstructions.ko.md),
[TICKET225 EN](docs/arithmetic-remainder-localization.md),
[TICKET225 KO](docs/arithmetic-remainder-localization.ko.md),
[TICKET224 EN](docs/sharp-completeness-thresholds.md),
[TICKET224 KO](docs/sharp-completeness-thresholds.ko.md),
[TICKET223 EN](docs/exponential-tail-local-duality-no-go.md),
[TICKET223 KO](docs/exponential-tail-local-duality-no-go.ko.md),
[TICKET222 EN](docs/lossless-coupling-biased-parity.md),
[TICKET222 KO](docs/lossless-coupling-biased-parity.ko.md),
[TICKET221 EN](docs/sharp-obstruction-certificates.md),
[TICKET221 KO](docs/sharp-obstruction-certificates.ko.md),
[TICKET220 EN](docs/dyadic-partition-primitive-refinement-crt.md),
[TICKET220 KO](docs/dyadic-partition-primitive-refinement-crt.ko.md),
[TICKET219 EN](docs/bandpass-matveev-crossfit-qualitative-abel.md),
[TICKET219 KO](docs/bandpass-matveev-crossfit-qualitative-abel.ko.md),
[TICKET218 EN](docs/adaptive-radius-spike-residual-surplus.md),
[TICKET218 KO](docs/adaptive-radius-spike-residual-surplus.ko.md),
[TICKET217 EN](docs/relative-threshold-convergent-moment-tail.md),
[TICKET217 KO](docs/relative-threshold-convergent-moment-tail.ko.md),
[TICKET216 EN](docs/laplace-gcd-radix-tauberian.md),
[TICKET216 KO](docs/laplace-gcd-radix-tauberian.ko.md),
[TICKET215 EN](docs/lattice-nearcollision-exception-abel.md),
[TICKET215 KO](docs/lattice-nearcollision-exception-abel.ko.md),
[TICKET214 EN](docs/cofinal-sevenone-exponential-cardinal.md),
[TICKET214 KO](docs/cofinal-sevenone-exponential-cardinal.ko.md),
[TICKET213 EN](docs/multiplicity-sixone-polynomial-selector.md),
[TICKET213 KO](docs/multiplicity-sixone-polynomial-selector.ko.md),
[TICKET212 EN](docs/even-defect-ghost-bonferroni-gapchannel.md),
[TICKET212 KO](docs/even-defect-ghost-bonferroni-gapchannel.ko.md),
[TICKET211 EN](docs/winding-density-fullrange-unitscale.md),
[TICKET211 KO](docs/winding-density-fullrange-unitscale.ko.md),
[TICKET210 EN](docs/cofinal-fiveone-primegap-scaledtwin.md),
[TICKET210 KO](docs/cofinal-fiveone-primegap-scaledtwin.ko.md),
[TICKET209 EN](docs/normalized-fourone-covering-factorial.md),
[TICKET209 KO](docs/normalized-fourone-covering-factorial.ko.md),
[TICKET208 EN](docs/vertical-threeone-unitlog-cyclotomic.md),
[TICKET208 KO](docs/vertical-threeone-unitlog-cyclotomic.ko.md),
[TICKET207 EN](docs/dihedral-twoone-logwitness-abel.md),
[TICKET207 KO](docs/dihedral-twoone-logwitness-abel.ko.md),
[TICKET206 EN](docs/adaptive-singleone-crt-projector.md),
[TICKET206 KO](docs/adaptive-singleone-crt-projector.ko.md),
[TICKET205 EN](docs/winding-extremal-finite-omega.md),
[TICKET205 KO](docs/winding-extremal-finite-omega.ko.md),
[TICKET204 EN](docs/mesh-necklace-exceptional-kernel.md),
[TICKET204 KO](docs/mesh-necklace-exceptional-kernel.ko.md),
[TICKET203 EN](docs/rouche-transfer-pointwise-primorial.md),
[TICKET203 KO](docs/rouche-transfer-pointwise-primorial.ko.md),
[TICKET202 EN](docs/exact-hermite-deformation-parity-scale.md),
[TICKET202 KO](docs/exact-hermite-deformation-parity-scale.ko.md),
[TICKET201 EN](docs/finite-information-allrun-liouville-parity.md),
[TICKET201 KO](docs/finite-information-allrun-liouville-parity.ko.md),
[TICKET200 EN](docs/derivative-mesh-three-run-chen-channels.md),
[TICKET200 KO](docs/derivative-mesh-three-run-chen-channels.ko.md),
[TICKET199 EN](docs/symmetric-sampling-two-run-squarefree-filter.md),
[TICKET199 KO](docs/symmetric-sampling-two-run-squarefree-filter.ko.md),
[TICKET198 EN](docs/verified-height-primitive-word-quantifier-strength.md),
[TICKET198 KO](docs/verified-height-primitive-word-quantifier-strength.ko.md),
[TICKET197 EN](docs/first-rectangle-run-block-sparse-collision.md),
[TICKET197 KO](docs/first-rectangle-run-block-sparse-collision.ko.md),
[TICKET196 EN](docs/rouche-density-overlap.md),
[TICKET196 KO](docs/rouche-density-overlap.ko.md),
[TICKET195 EN](docs/finitejet-elevenone-squarelayer.md),
[TICKET195 KO](docs/finitejet-elevenone-squarelayer.ko.md),
[TICKET194 EN](docs/densecore-tenone-theta-layers.md),
[TICKET194 KO](docs/densecore-tenone-theta-layers.ko.md),
[TICKET193 EN](docs/everywhere-nineone-parity-envelope.md),
[TICKET193 KO](docs/everywhere-nineone-parity-envelope.ko.md),
[TICKET192 EN](docs/uniform-eightone-weighted-envelope.md),
[TICKET192 KO](docs/uniform-eightone-weighted-envelope.ko.md),
[TICKET191 EN](docs/probe-sevenone-budget-granularity.md),
[TICKET191 KO](docs/probe-sevenone-budget-granularity.ko.md),
[TICKET190 EN](docs/cauchy-sixone-quantifier-transfer.md),
[TICKET190 KO](docs/cauchy-sixone-quantifier-transfer.ko.md),
[TICKET189 EN](docs/summable-core-fiveone-sublinear-shift.md),
[TICKET189 KO](docs/summable-core-fiveone-sublinear-shift.ko.md),
[TICKET188 EN](docs/nested-fourone-primepower-dyadic.md),
[TICKET188 KO](docs/nested-fourone-primepower-dyadic.ko.md),
[TICKET187 EN](docs/positive-ray-threeone-signature-interval.md),
[TICKET187 KO](docs/positive-ray-threeone-signature-interval.ko.md),
[TICKET186 EN](docs/codimension-twoone-layercake-quantization.md),
[TICKET186 KO](docs/codimension-twoone-layercake-quantization.ko.md),
[TICKET185 EN](docs/spectral-cycle-factor-granularity.md),
[TICKET185 KO](docs/spectral-cycle-factor-granularity.ko.md),
[TICKET184 EN](docs/information-sufficiency-route-correction.md),
[TICKET184 KO](docs/information-sufficiency-route-correction.ko.md),
[TICKET183 EN](docs/abel-primitive-spectral-haar.md),
[TICKET183 KO](docs/abel-primitive-spectral-haar.ko.md),
[TICKET182 EN](docs/sobolev-divisibility-translation-sibling.md),
[TICKET182 KO](docs/sobolev-divisibility-translation-sibling.ko.md),
[TICKET181 EN](docs/regularized-localization-quantized-slack.md),
[TICKET181 KO](docs/regularized-localization-quantized-slack.ko.md),
[TICKET180 EN](docs/finite-information-localization.md),
[TICKET180 KO](docs/finite-information-localization.ko.md),
[TICKET179 EN](docs/symbol-adaptive-discrete-centering.md),
[TICKET179 KO](docs/symbol-adaptive-discrete-centering.ko.md),
[TICKET178 EN](docs/toeplitz-lowbit-frequency-split-zeromode.md),
[TICKET178 KO](docs/toeplitz-lowbit-frequency-split-zeromode.ko.md),
[TICKET177 EN](docs/comparison-wheel-sobolev-crossgram.md),
[TICKET177 KO](docs/comparison-wheel-sobolev-crossgram.ko.md),
[TICKET176 EN](docs/relative-cone-harmonic-alias-schur.md),
[TICKET176 KO](docs/relative-cone-harmonic-alias-schur.ko.md),
[TICKET175 EN](docs/relative-equivalence-signed-block.md),
[TICKET175 KO](docs/relative-equivalence-signed-block.ko.md),
[TICKET174 EN](docs/tail-lift-adaptive-scalepair.md),
[TICKET174 KO](docs/tail-lift-adaptive-scalepair.ko.md),
[TICKET173 EN](docs/finite-section-cylinder-phase-tensor.md),
[TICKET173 KO](docs/finite-section-cylinder-phase-tensor.ko.md),
[TICKET172 EN](docs/structure-equivalence-l1-variation.md),
[TICKET172 KO](docs/structure-equivalence-l1-variation.ko.md),
[TICKET171 EN](docs/relative-ghost-phase-haar.md),
[TICKET171 KO](docs/relative-ghost-phase-haar.ko.md),
[TICKET170](docs/interval-tail-besov-multiscale.md),
[TICKET169](docs/kkt-childlift-autocorrelation-primepower.md),
[TICKET168](docs/fixedcore-leastrealizer-phase-paritymain.md),
[TICKET167](docs/cofinal-residue-besov-parity.md),
[TICKET166](docs/tail-adaptive-bandlimited-diagonal.md),
[TICKET165](docs/vanishing-defect-logtail-variation-signed-dual.md),
[TICKET164](docs/core-eigen-first-crossing-pointwise-product.md),
[TICKET163](docs/local-certificate-realizer-trace-carleson.md),
[TICKET162](docs/formnorm-explicitbaker-integral-multiscale.md),
[TICKET161](docs/commoncore-baker-angle-typeii.md),
[TICKET160](docs/exact-support-cylinder-bilinear-wheel.md),
[TICKET159](docs/diagonal-threshold-phase-parity.md),
[TICKET158](docs/two-cutoff-localized-variation-directional.md),
[TICKET157](docs/formcore-inversion-proxy-margin.md),
[TICKET156](docs/cutoff-potential-signed-information.md),
[TICKET155](docs/range-prefix-sublinear-conditional.md),
[TICKET154](docs/compact-suffix-wheel-leastfactor.md),
[TICKET153](docs/essential-tail-geometric-reflection-parity.md),
[TICKET152](docs/compression-cylinder-energy-selection.md),
[TICKET151](docs/negative-affine-transversal-logtwo.md),
[TICKET150](docs/relative-delay-hole-parity.md),
[TICKET149](docs/smooth-escape-wheel-cover.md),
[TICKET148](docs/multiscale-renewal-sharpness-matching.md),
[TICKET147](docs/fiber-compensation-phase-graph.md),
[TICKET146](docs/toeplitz-polynomial-phase-frechet.md),
[TICKET145](docs/normalization-affine-endpoint-separable-no-go.md),
[TICKET144](docs/schur-rank-equivalence-variation-adverse-walsh.md), and
[TICKET143](docs/form-core-period-floor-martingale-walsh.md).

한국어 최신 요약: 최신 탐색은 TICKET-230입니다. 리만 트랙은 모든 고정
유한 배율 족에 `T^(-2/m)` 속도의 무한 근접 재귀가 생김을 증명했습니다.
콜라츠 트랙은 순환 나눗셈과 `gcd(D,B)`가 목걸이 불변량임을 증명했습니다.
골드바흐는 각 푸리에 모드가 작아도 목표 정렬 전체 오차가 주항과 같은
차수가 될 수 있다는 정확한 반례족을 만들었습니다. 쌍둥이 소수는 mod
`5` 원시 이차지표의 올바른 허용 평균이 `0`이 아니라 `1/3`임을
확정했습니다. 네 상위 문제의 해결 수는 여전히 0입니다.

The bundled Crypto-Classifier panel is intentionally scoped to `controlled_synthetic_only`: it proves the feature-vector and classifier plumbing on synthetic generator fingerprints, then keeps real-world attribution blocked until OpenSSL, BoringSSL, Go, and suspicious labelled baselines are collected with provenance.

The Attribution Grid panel displays a bundled paired benchmark from `data/attribution_confound_grid.json`, `data/null_calibration.json`, and `data/replication_audit.json`, highlighting which fingerprint profiles survive bit-length control, which ones are likely range confounds, whether the strongest controlled profiles survive random-label null simulation after family-wise profile selection, and whether those profiles replicate across settings.

The Baseline Lab panel reads `data/baselines/real_world/manifest.json`, `data/collection_matrix.json`, `data/collection_power.json`, `data/provenance_requirements.json`, `data/provenance_audit.json`, `data/baseline_acceptance.json`, `data/baseline_promotion_plan.json`, `data/collection_handoff.json`, `data/collection_submission_contract.json`, `data/collection_submission_lint.json`, `data/collection_fixture_audit.json`, and `data/collection_intake.json` to show which real-world baseline families are registered, whether targets are only coarse screening or strong enough for tighter claims, which baselines still block publication, which public-safe collection tasks should be executed first, what collectors must submit, what pre-intake lint would reject, whether lint behavior is covered by pass/warn/block fixtures, and whether submitted aggregate artifacts are acceptable without feature-vector contract failures, identity mismatches, non-public feature-vector paths, duplicate submission collisions, or reused aggregate checksums.

The Research Readiness panel reads `data/research_readiness.json` and surfaces blocking gaps before any real-world attribution claim is treated as strong.

The Evidence Pack panel reads `data/evidence_pack.json`, `data/claim_language_audit.json`, `data/claim_ledger.json`, `data/artifact_lineage.json`, `data/decision_protocol.json`, `data/falsification_battery.json`, and `data/publication_consistency.json` to show checksums, semantic publication gates, the maximum safe claim level, which public claims are currently allowed or blocked, whether public wording stays inside the evidence boundary, whether the public artifact dependency graph is acyclic and checksum-consistent, which claim-promotion decisions are pre-registered as allowed or blocked, which falsification checks prevent overclaiming, and whether all public governance artifacts agree on the same high-risk claim boundary. The fixture-audit gate now checks `quality_gate.status`, fixture count, public-safety count, and failed expectation count instead of only checking that the file exists.

## 한국어

`PrimeProject`는 네 난제의 증명 경로를 감사하고, 암호 시스템이 만든 수학적 객체에서 생성기의 흔적과 약점을 찾는 이중 연구 플랫폼입니다. 정확한 수학적 결과, 유한 계산, 폐기된 경로, 실세계 attribution의 차단 조건을 서로 구분합니다.

언어 지원: [GitHub Pages KO](https://eljja.github.io/PrimeProject/?lang=ko)에서 `EN / KO` 전환 버튼을 사용할 수 있습니다. 전환 대상은 페이지 구조, 좌측 메뉴, 주요 제목, proof workbench 라벨, 논문 제출용 주장 경계 안내입니다. 재현 가능한 JSON artifact의 schema label은 논문/검증 스크립트와 맞추기 위해 영어 원문을 유지합니다.

핵심 경계: 이 프로젝트는 안전한 암호 소수를 예측했다거나, accepted real-world baseline 없이 실제 키의 생성 라이브러리를 단정했다거나, 리만가설/콜라츠/골드바흐/Twin Prime을 증명했다고 주장하지 않습니다. 현재 강하게 말할 수 있는 범위는 bounded certificate, 통제된 합성 generator fingerprint, 공개 안전 수집 계약, claim-language audit, evidence pack, publication consistency audit입니다.

최신 난제 연구 트랙은 TICKET-230입니다.
[정량 재귀·목걸이 불변성·푸리에 합산·국소 중심화 한국어 보고서](docs/quantitative-recurrence-necklace-fourier-centering.ko.md)와
[영문 보고서](docs/quantitative-recurrence-necklace-fourier-centering.md)는 네 트랙의
정확 명제, 증명, 재현 계산, 폐기 경로와 남은 무한 간극을 분리합니다.
현재 결정적 미해결 보조정리는 실제 Weil 핵 꼬리를 재귀 척도 아래서
지배하는 적응형 무한 frame, 모든 원시 양의 분모 Collatz 목걸이 대표의
비나눗셈, 골드바흐 이항 소수 minor arc의 부호 있는 전체 합 상계,
쌍둥이 소수 mod `5` 중심화 Type-II 절약과 양의 주항입니다.

주요 진입점:

- [메인 연구실](https://eljja.github.io/PrimeProject/?lang=ko): TICKET-230의 현재 연구 경계, 네 문제의 부분정리·폐기 경로·남은 간극을 먼저 보고 소수 탐색기와 암호 fingerprint 실험으로 이동합니다.
- [Proof Workbench](https://eljja.github.io/PrimeProject/open-problems/index.html): 네 문제의 현재 보조정리를 한 화면에서 비교하며, 230개 티켓은 네 연구 시대와 재현 기록으로 압축해 탐색합니다.
- [Riemann Workbench](https://eljja.github.io/PrimeProject/open-problems/riemann.html), [Collatz Workbench](https://eljja.github.io/PrimeProject/open-problems/collatz.html), [Goldbach Workbench](https://eljja.github.io/PrimeProject/open-problems/goldbach.html), [Twin Prime Workbench](https://eljja.github.io/PrimeProject/open-problems/twin-prime.html): 각 난제의 `open_not_proven` 상태와 필요한 무한 논증을 확인합니다.
- [Publication-Ready Document Review](docs/publication-ready-review.md): 모든 공개 문서의 허용 주장과 차단 주장을 한글/영문 기준으로 검토합니다.

## Input format

```json
{
  "records": [
    {
      "key_id": "example",
      "algorithm": "rsa",
      "value": "0x...",
      "public_exponent": 65537,
      "source": "owned-test"
    }
  ]
}
```

`algorithm` can be `rsa`, `dh`, `ffdhe`, `modp`, `ecc`, `ec`, `field-prime`, or `prime`. PEM, DER, X.509 certificate, and CSR inputs currently extract RSA public modulus and exponent records.

## Usage

```powershell
python -m prime_audit.cli simulate --output data/synthetic_keys.json --bits 128 --include-standards
python -m prime_audit.cli audit --input data/synthetic_keys.json --output data/audit_report.json --fail-on high
python -m prime_audit.cli fingerprint-primes --input data/synthetic_keys.json --output data/generator_fingerprints.json
python -m prime_audit.cli build-baseline --fingerprint data/generator_fingerprints.json --name openssl-owned-sample --output data/baselines/openssl_owned.json
python -m prime_audit.cli compare-baselines --fingerprint data/generator_fingerprints.json --baselines data/baselines/openssl_owned.json --output data/baseline_comparison.json
python -m prime_audit.cli real-baseline-manifest --output data/baselines/real_world/manifest.json
python -m prime_audit.cli collection-matrix --manifest data/baselines/real_world/manifest.json --output data/collection_matrix.json
python -m prime_audit.cli collection-power --matrix data/collection_matrix.json --output data/collection_power.json
python -m prime_audit.cli provenance-requirements --manifest data/baselines/real_world/manifest.json --output data/provenance_requirements.json
python -m prime_audit.cli provenance-audit --requirements data/provenance_requirements.json --output data/provenance_audit.json
python -m prime_audit.cli baseline-acceptance --manifest data/baselines/real_world/manifest.json --matrix data/collection_matrix.json --power data/collection_power.json --provenance-audit data/provenance_audit.json --output data/baseline_acceptance.json
python -m prime_audit.cli baseline-promotion-plan --acceptance data/baseline_acceptance.json --power data/collection_power.json --output data/baseline_promotion_plan.json
python -m prime_audit.cli synthetic-feature-vectors --limit 200000 --samples-per-label 4 --record-count 80 --seed 20260523 --gap-max-steps 1024 --output data/feature_vectors.json
python -m prime_audit.cli export-feature-vectors --fingerprints openssl=data/openssl_fingerprint.json suspicious=data/suspicious_fingerprint.json --claim-scope real_world --output data/feature_vectors.json
python -m prime_audit.cli crypto-classifier --features data/feature_vectors.json --feature-space interaction --output data/crypto_classifier_report.json
python -m prime_audit.cli collection-handoff --manifest data/baselines/real_world/manifest.json --matrix data/collection_matrix.json --power data/collection_power.json --provenance-requirements data/provenance_requirements.json --provenance-audit data/provenance_audit.json --baseline-acceptance data/baseline_acceptance.json --promotion-plan data/baseline_promotion_plan.json --classifier-report data/crypto_classifier_report.json --output data/collection_handoff.json
python -m prime_audit.cli collection-submission-contract --handoff data/collection_handoff.json --output data/collection_submission_contract.json
python -m prime_audit.cli collection-submission-lint --contract data/collection_submission_contract.json --output data/collection_submission_lint.json
python -m prime_audit.cli collection-fixture-audit --contract data/collection_submission_contract.json --output data/collection_fixture_audit.json
python -m prime_audit.cli collection-intake --handoff data/collection_handoff.json --output data/collection_intake.json
python -m prime_audit.cli claim-language-audit --generated-at 2026-05-24T16:56:40+00:00 --output data/claim_language_audit.json
python -m prime_audit.cli research-readiness --manifest data/baselines/real_world/manifest.json --attribution-grid data/attribution_confound_grid.json --classifier-report data/crypto_classifier_report.json --output data/research_readiness.json
python -m prime_audit.cli evidence-pack --manifest data/baselines/real_world/manifest.json --readiness data/research_readiness.json --attribution-grid data/attribution_confound_grid.json --baseline-acceptance data/baseline_acceptance.json --collection-intake data/collection_intake.json --classifier-report data/crypto_classifier_report.json --artifact project_evolution=data/project_evolution.json snapshot_manifest=data/snapshots/manifest.json collection_matrix=data/collection_matrix.json collection_power=data/collection_power.json provenance_requirements=data/provenance_requirements.json provenance_audit=data/provenance_audit.json baseline_promotion_plan=data/baseline_promotion_plan.json collection_handoff=data/collection_handoff.json collection_submission_contract=data/collection_submission_contract.json collection_submission_lint=data/collection_submission_lint.json collection_fixture_audit=data/collection_fixture_audit.json claim_language_audit=data/claim_language_audit.json null_calibration=data/null_calibration.json replication_audit=data/replication_audit.json feature_vectors=data/feature_vectors.json --generated-at 2026-05-24T16:56:40+00:00 --output data/evidence_pack.json
python -m prime_audit.cli claim-ledger --evidence-pack data/evidence_pack.json --generated-at 2026-05-24T16:56:40+00:00 --output data/claim_ledger.json
python -m prime_audit.cli artifact-lineage --generated-at 2026-05-24T16:56:40+00:00 --output data/artifact_lineage.json
python -m prime_audit.cli decision-protocol --evidence-pack data/evidence_pack.json --claim-ledger data/claim_ledger.json --artifact-lineage data/artifact_lineage.json --generated-at 2026-05-24T16:56:40+00:00 --output data/decision_protocol.json
python -m prime_audit.cli falsification-battery --attribution-grid data/attribution_confound_grid.json --decision-protocol data/decision_protocol.json --generated-at 2026-05-24T16:56:40+00:00 --output data/falsification_battery.json
python -m prime_audit.cli publication-consistency --evidence-pack data/evidence_pack.json --claim-ledger data/claim_ledger.json --decision-protocol data/decision_protocol.json --falsification-battery data/falsification_battery.json --generated-at 2026-05-24T16:56:40+00:00 --output data/publication_consistency.json
python -m prime_audit.cli null-calibration --attribution-grid data/attribution_confound_grid.json --iterations 5000 --output data/null_calibration.json
python -m prime_audit.cli replication-audit --attribution-grid data/attribution_confound_grid.json --null-calibration data/null_calibration.json --output data/replication_audit.json
python -m prime_audit.cli attribution-benchmark --limit 200000 --train-count 80 --test-count 40 --trials 3 --control-mode bit_length --output data/attribution_benchmark.json
python -m prime_audit.cli attribution-grid --limits 50000 200000 --train-counts 40 80 --test-counts 20 40 --trials 3 --repeats 3 --output data/attribution_confound_grid.json
python -m prime_audit.cli gap-lab --limit 100000 --modulo 30 --output data/conjecture_lab_100k.json
python -m prime_audit.cli bias-rank --start 100000 --span 640 --modulo 210 --output data/bias_rank_100k.json
python -m prime_audit.cli bitcoin-constants --output data/bitcoin_constants.json
python -m prime_audit.cli bitcoin-signature-audit --input data/bitcoin_signatures.json --output data/bitcoin_signature_audit.json
python -m prime_audit.cli bitcoin-risk-report --signature-audit data/bitcoin_signature_audit.json --manifest data/baselines/real_world/manifest.json --output data/bitcoin_generator_risk_report.json
python -m prime_audit.cli snapshot --limit 10000000 --modulo 210 --output data/snapshots/prime_measure_10m.summary.json --assets-dir assets/snapshots --slug prime_measure_10m
python -m prime_audit.cli snapshot-manifest --inputs data/snapshots/prime_measure_1m.summary.json data/snapshots/prime_measure_10m.summary.json --output data/snapshots/manifest.json
python scripts/benchmark_shared_factors.py --count 1000 --bits 128 --output data/shared_factor_benchmark.json
```

To audit the current publication bundle without overwriting files, run:

```bash
python scripts/reproduce_publication.py
```

The script starts by regenerating `data/claim_language_audit.json` in a temporary directory and compares it with the public artifact, so stale public wording checks cannot pass unnoticed. Add `--report publication_reproduction_report.json` to save the compared canonical JSON hashes, raw file hashes, and command trace with temporary output paths normalized to `{tmp}`. Local reproduction reports matching `publication_reproduction_report*.json` are ignored by git so audit scratch output does not enter the public evidence bundle by accident.

To verify the GitHub Pages surface, run:

```bash
node scripts/verify_pages.cjs
```

The verifier serves the repository over local HTTP, so it exercises the same `data/*.json` fetch path used by GitHub Pages instead of the `file://` fallback constants.

To verify the open-problem bounded certificates, run:

```bash
python scripts/verify_open_problem_workbench.py
```

The bundled Codex runtime Python can also run the same commands.

## Continuous Verification

GitHub Actions now runs the publication guard on pushes and pull requests to `main`: Python compile checks, publication-critical unit checks, publication artifact reproduction, JavaScript syntax checks, Playwright-based GitHub Pages verification, and a final committed-artifact drift check. This keeps the public research bundle from silently diverging from the audited evidence files. Run `python -m unittest discover -s tests -p "test_*.py"` locally for the full suite.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).

본 프로젝트의 코드, 문서 및 배포 자료는 별도 표기가 없는 한 Apache License 2.0에 따라 제공됩니다. 자세한 조건은 [LICENSE](LICENSE)에서 확인할 수 있습니다.
