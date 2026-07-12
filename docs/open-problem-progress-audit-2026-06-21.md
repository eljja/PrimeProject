# PrimeProject Open-Problem Progress Audit

Date: 2026-06-21

Superseded on 2026-07-10 by `docs/open-problem-research-consolidation-2026-07-10.md`. This file is retained as a historical snapshot only. Its TICKET14 “top attack” ordering is no longer current, and the Jensen, stopping-time-density, singular-series, and Maynard-weight artifacts are finite diagnostics rather than infinite-bridge theorems.

This audit records what changed in the current PrimeProject open-problem workbench and how far the project has advanced toward four unsolved problems: the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, and Twin Prime conjecture.

## Executive Claim Boundary

PrimeProject has not proved any of the four open problems.

The meaningful progress is different: the repository now contains a proof-attempt workbench that can generate bounded certificates, rank candidate theorem attacks, reject common proof shortcuts, and expose the exact infinite bridge still missing for each problem. This is the correct research posture for an AI-assisted attempt: finite computation and heuristic structure are treated as falsification tools and lemma generators, not as full proofs.

## What Changed

1. Tier 13 and Tier 14 CEGIS artifacts were added for the four problems.
2. `data/open_problem_workbench.json` now exposes proof gates, proof verdicts, AI proof-forge entries, theorem decomposition, and attack tickets.
3. Formal skeletons exist under `formal/*/InfiniteBridge.lean` as Lean-oriented handoff files.
4. The workbench now blocks full-proof promotion through `proof_status_gate`, `proof_verdict`, `formal_replay_package`, and `formal_skeleton_audit`.
5. A fast structural verifier was added at `scripts/verify_open_problem_structure.py`.
6. Expensive Tier 14 artifacts are now cached by default in `scripts/generate_open_problem_workbench.py`; set `PRIMEPROJECT_RECOMPUTE_TIER14=1` to force recomputation.

## Verification Status

Structural verification passes:

```text
open problem structure verified
```

The older full recomputation verifier remains too slow for routine GitHub Pages validation because it recomputes expensive CEGIS audits. It should be retained as a heavy audit path, not as the default publication gate.

The Twin Prime formal skeleton was corrected. It no longer contains `axiom`, `sorry`, or direct theorem claims that would falsely suggest a proof.

## Problem-by-Problem Progress

### 1. Riemann Hypothesis

Current top attack ticket: `RH-TICKET-14`

The workbench tests Jensen-polynomial hyperbolicity, Turan-type inequalities, Hermite decay, and finite xi-function coefficient behavior. This is aligned with a serious modern direction because Jensen polynomial hyperbolicity is connected to deep structure around the Riemann xi function.

Current limit: finite coefficient and finite degree evidence only.

Missing bridge:

```text
Uniform all-degree/all-shift hyperbolicity or an equivalent non-circular analytic theorem that forces every non-trivial zeta zero onto Re(s)=1/2.
```

Best next attack:

Define a uniform envelope theorem for xi Taylor coefficients that is stronger than observed finite Jensen behavior but weaker than directly assuming RH. Then run a CEGIS loop that searches for adversarial coefficient perturbations preserving all bounded tests while violating the proposed envelope. If no perturbation survives, formalize the envelope as the next target theorem.

### 2. Collatz Conjecture

Current top attack ticket: `CO-TICKET-14`

The workbench computes stopping-time density up to 10,000,000 and residue statistics. This is useful because Collatz proof attempts often fail by proving only high-density convergence rather than universal convergence.

Current limit: finite stopping-time density and residue evidence.

Missing bridge:

```text
A well-founded residue-rank descent theorem covering every residue block and excluding nondecreasing strongly connected components.
```

Best next attack:

Use the stopping-time residue data to synthesize a candidate rank function over accelerated Collatz residue blocks:

```text
R(n) = a log n + b v2(3n+1) + residue_potential(n mod 2^k 3^m)
```

Then require an exact edge-by-edge descent certificate for every block. This is the most practical AI route among the four problems because failures produce concrete counterexample blocks rather than only analytic gaps.

### 3. Goldbach Conjecture

Current top attack ticket: `GB-TICKET-14`

The workbench audits Hardy-Littlewood singular-series precision and finite representation counts. This is valuable for finding where explicit lower-bound arguments lose too much margin.

Current limit: finite verification and heuristic singular-series agreement.

Missing bridge:

```text
An explicit large-even lower-bound theorem with constants and cutoff small enough to overlap the finite certificate.
```

Best next attack:

Convert the empirical singular-series margin into an explicit inequality budget:

```text
R(n) >= main_term(n) - major_arc_error(n) - minor_arc_error(n) > 0
```

The AI task is not to rediscover Hardy-Littlewood heuristics. It is to search the constant budget and find whether any known or newly proposed bound can push the analytic cutoff below the certified finite range.

### 4. Twin Prime Conjecture

Current top attack ticket: `TP-TICKET-14`

The workbench uses Maynard/Selberg-style weight diagnostics and bounded-gap comparison. This is meaningful because bounded gaps are the strongest proven neighborhood around twin primes.

Current limit: bounded gaps are not exact gap 2.

Missing bridge:

```text
A positive exact gap-2 lower-bound theorem that survives parity barriers and does not import Hardy-Littlewood k-tuple behavior as an axiom.
```

Best next attack:

Separate bounded-gap mass from exact-gap-2 mass. The candidate theorem should subtract all wider admissible gaps from a bounded interval and still leave a positive exact-pair projection. The expected failure mode is parity-barrier collapse; that failure is useful because it localizes precisely what a new idea must overcome.

## Cross-Problem Strategy

The strongest unified direction is not "predict primes." It is "find the missing infinite bridge by adversarially testing candidate lemmas."

PrimeProject should therefore prioritize:

1. Candidate theorem generation.
2. Counterexample-guided synthesis.
3. Formal forbidden-shortcut audits.
4. Exact failure localization.
5. Only then Lean formalization.

The project should avoid claiming success from:

1. Larger finite bounds.
2. Smooth plots.
3. Distributional agreement alone.
4. Heuristic independence assumptions.
5. Imported theorem statements equivalent to the target conjecture.

## Next Concrete Research Move

The most promising immediate target is Collatz, because a failed candidate produces an explicit residue block. The next artifact should be:

```text
CO-TICKET-15 ResidueRankSynthesis
```

Required output:

1. A generated candidate rank over accelerated residue classes.
2. A complete transition graph for a chosen modulus.
3. A machine-checkable list of descending edges.
4. A counterexample list of nondecreasing SCCs.
5. A promotion rule that blocks proof claims unless every SCC descends or enters the known basin.

If this fails, the failed SCCs become the next AI design prompt. If it succeeds for one modulus, the next step is a lifting theorem from modulus `M` to `2M` or `3M`, which is the actual infinite bridge.

## Korean Summary

현재 프로젝트는 네 난제를 푼 것이 아니라, 네 난제에 대해 "증명이라고 말하려면 무엇이 아직 부족한가"를 자동으로 드러내는 연구 장치로 진화했다. 가장 중요한 진전은 proof gate, CEGIS ticket, formal skeleton audit, theorem decomposition이 결합되어 finite evidence와 full proof claim을 분리한다는 점이다.

다음에 가장 실용적으로 공격할 문제는 Collatz다. 리만가설, 골드바흐, 쌍둥이 소수는 분석적 무한 다리의 난도가 매우 높고 실패가 추상적이다. 반면 Collatz residue-rank 접근은 실패하면 구체적인 residue block 또는 SCC가 나오므로 AI가 반복 개선하기 좋다.
