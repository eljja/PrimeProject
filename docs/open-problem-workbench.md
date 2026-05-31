# Open Problem Proof Workbench

## Bilingual abstract / 한영 초록

English: This document specifies a proof workbench for four still-open problems: the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, and Twin Prime conjecture. PrimeProject does not claim proofs. It records bounded evidence, proof obligations, invalid shortcuts, AI-assisted search frontiers, formal replay contracts, and the exact conditions required before any claim can move beyond `open_not_proven`.

한국어: 이 문서는 아직 미해결인 네 문제, 즉 리만가설, 콜라츠 추측, 골드바흐 추측, Twin Prime 추측을 위한 proof workbench 규격이다. PrimeProject는 증명을 주장하지 않는다. 대신 bounded evidence, proof obligation, invalid shortcut, AI-assisted search frontier, formal replay contract, 그리고 `open_not_proven`을 넘기 위해 필요한 조건을 기록한다.

PrimeProject now has four GitHub Pages subpages for:

- Riemann Hypothesis
- Collatz Conjecture
- Goldbach Conjecture
- Twin Prime Conjecture

The purpose is not to publish a fake proof. The workbench is a disciplined proof lab: each page shows a proof verdict, actual proof attempt runner, candidate lemma workbench, machine proof search trials, formal upgrade matrix, proof kernel roadmap, formal kernel contract audit, invalid proof shortcut suite, AI solver frontier, proof-route triage, a decisive theorem spec, decisive theorem subgoals, decisive theorem attack tickets, a breakthrough agenda, finite evidence, a bounded certificate, a proof-attempt ledger, a proof attack map, a machine proof-status gate, a proof execution protocol, a proof frontier probe, a known-barrier audit, a formal replay package, a proof review docket, a proof reduction contract, proof candidate intake rules, proof attempt execution logs, a proof obligation DAG, formal skeleton audits, a Lean-oriented formal proof contract, a proof milestone queue, a decisive lemma lab with certified automated falsification probes, a proof-gap taxonomy, the missing infinite proof gates, candidate strategies, and blocked claim language. The public claim level is `proof_workbench_only`.

## Public Pages

- `open-problems/riemann.html`
- `open-problems/collatz.html`
- `open-problems/goldbach.html`
- `open-problems/twin-prime.html`

All four pages read `data/open_problem_workbench.json` through the same GitHub Pages public JSON path.

## Generated Evidence

Regenerate the bounded evidence bundle:

```powershell
python scripts/generate_open_problem_workbench.py --limit 1000000 --output data/open_problem_workbench.json
```

Verify the committed bounded certificates:

```powershell
python scripts/verify_open_problem_workbench.py
```

Current bounded checks:

- Riemann: prime-counting and Chebyshev theta diagnostics through 1,000,000.
- Collatz: exhaustive trajectory replay for start values through 1,000,000.
- Goldbach: exhaustive even-number decomposition check through 1,000,000.
- Twin Prime: twin-pair counts and Hardy-Littlewood heuristic comparison through 1,000,000.

Each problem includes a `primeproject.bounded-proof-certificate.v1` object. The certificate hashes every bounded witness or diagnostic row, groups leaves into deterministic chunks, and exposes a Merkle root that CI recomputes. This is a real proof artifact for the bounded theorem only. It is intentionally not a proof of the unbounded conjecture.

Each problem now also includes a `primeproject.proof-verdict.v1` object. The verdict is the first panel on every problem page: it names the target as `not_proved_by_primeproject`, names the bounded theorem that is actually certified, exposes the current full-proof blocker, and states the machine rule that must pass before any page may display a proof claim.

Each problem also includes a `primeproject.actual-proof-attempt-runner.v1` object. The runner executes the current proof route as far as the project can honestly go: bounded certificate replay, frontier falsification, route triage, and decisive theorem gating. Its status remains `executed_full_proof_blocked` while the infinite bridge is missing.

Each problem also includes a `primeproject.candidate-lemma-workbench.v1` object. The workbench records candidate lemmas, tool tests, current results, reasons for rejection or blockage, and next revisions. Candidate lemmas can guide the search but cannot upgrade a page without a formal proof or accepted theorem.

Each problem also includes a `primeproject.machine-proof-search-trials.v1` object. These trials close finite pieces or reject shortcuts. They are not proofs until the required proof upgrade is supplied as a formal artifact or accepted theorem.

Each problem also includes a `primeproject.formal-upgrade-matrix.v1` object. The matrix separates bounded certificate replay, the decisive infinite theorem, kernel formalization, and independent review. Every non-bounded row must close before a page can make a full-proof claim.

Each problem also includes a `primeproject.proof-kernel-roadmap.v1` object. The roadmap states the kernel path from formal definitions to bounded certificate import, decisive infinite lemma, bridge to the target theorem, and independent kernel replay.

Each problem also includes a `primeproject.formal-kernel-contract-audit.v1` object. The audit checks that the Lean-oriented skeleton files contain the expected target theorem name, target theorem statement, bounded-claim status, replay status, and public claim boundary. Passing this audit proves only alignment, not the conjecture.

Each problem also includes a `primeproject.invalid-proof-shortcut-suite.v1` object. The suite rejects common false proof routes: finite-to-infinite jumps, heuristic-to-theorem substitutions, weak theorem substitution, circular bridge imports, and bounded-gap substitution for exact twin gaps.

Each problem also includes a `primeproject.ai-solver-frontier.v1` object. This is the live AI-assisted attack plan: RH uses positivity-kernel search, Collatz uses residue-block descent cover search, Goldbach uses explicit-cutoff optimization for two-prime lower bounds, and Twin Prime uses exact-gap sieve-weight search. These are research frontiers, not solved results.

Each problem also includes a `primeproject.proof-route-triage.v1` object. The triage panel lists candidate proof routes, rejects finite-to-infinite jumps and weaker-theorem substitutions, marks heuristic-only routes, and names the single current decisive route whose required upgrade would move the project closer to a real proof attempt.

Each problem also includes a `primeproject.decisive-theorem-spec.v1` object. The theorem spec turns the current decisive route into one precise missing theorem, with allowed inputs, forbidden shortcuts, machine checks, and the milestones it would close if it were independently proved.

Each problem also includes a `primeproject.decisive-theorem-subgoals.v1` object. The subgoal matrix decomposes that theorem spec into bounded support, formal statement, infinite bridge, finite/infinite glue, and independent replay work. It keeps the theorem open while any subgoal remains open or blocked.

Each problem also includes a `primeproject.decisive-theorem-attack-tickets.v1` object. The ticket list turns every open or blocked subgoal into a planned experiment with a required output and falsification test. Planned tickets are explicitly not proof artifacts.

Each problem also includes a `primeproject.proof-breakthrough-agenda.v1` object. The agenda names routes that would be genuinely novel enough to matter, the exact barrier each route attacks, which PrimeProject tools apply, the minimum new theorem required, the first artifact to produce, and the kill condition that rejects the route. Agenda entries are research targets, not proof claims.

Each problem also includes a `primeproject.proof-attempt-ledger.v1` object. The ledger separates three things:

- `proved_by_certificate`: the finite theorem already verified by the Merkle certificate.
- `open_obligation`: the exact infinite lemma still needed before any solution claim is allowed.
- `falsification_targets`: concrete ways an attempted proof can fail.

The same ledger now includes an attack graph, known theorem bridges, and lemma candidates. This is the proof-search contract for each problem:

- The attack graph shows which edge still has to remove the finite search limit.
- Known theorem bridges record where existing mathematics is usable, insufficient, or only heuristic.
- Lemma candidates state the next target in a form that could later be moved into a formal proof assistant.

Each problem also includes a `primeproject.open-problem-proof-status-gate.v1` object. The gate is intentionally conservative: it blocks a full-proof claim while any obligation, attack-graph edge, theorem bridge, or lemma candidate remains open. `scripts/verify_open_problem_workbench.py` checks that all four pages remain blocked until the finite certificate is joined to an independently checkable infinite proof.

Each problem also includes a `primeproject.proof-execution-protocol.v1` object. This protocol turns the proof attempt into ordered execution stages: bounded certificate replay, formal target normalization, decisive lemma attack, gap work-order falsification, and full-proof promotion. Each stage names its required output and verifier, and the protocol keeps `blocked_before_full_proof` until the machine gate becomes eligible for independent review.

Each problem also includes a `primeproject.proof-frontier-probe.v1` object. This is the computational pressure test for the current proof frontier: Riemann stresses theta-envelope candidates at prime endpoints, Collatz stresses accelerated odd residue descents, Goldbach ranks hard residue classes by first-prime witness, and Twin Prime separates exact gap-2 residue persistence from bounded-gap evidence. The probe status is always `finite_probe_not_proof`; it can falsify or prioritize a proof path but cannot close the conjecture.

Each problem also includes a `primeproject.known-barrier-audit.v1` object. This audit lists barriers that routinely invalidate attempted proofs: finite-to-infinite lifting, proof-assistant replay, RH-equivalence strength, Collatz exceptional residue classes, Goldbach positive lower bounds, Twin Prime exact-gap lower bounds, and heuristic dependencies. A page remains blocked while any barrier lacks a formal clearance artifact.

Each problem also includes a `primeproject.formal-replay-package.v1` object. This package names the Lean-oriented files, replay commands, required artifacts, and forbidden tokens that would be needed before any candidate proof can be submitted for independent review. Its status remains `not_replayable_until_barriers_clear` while known barriers are open.

Each problem also includes a `primeproject.proof-review-docket.v1` object. The docket acts like a reviewer checklist: the bounded theorem is accepted only for the committed finite limit, while the full conjecture claim, formal replay readiness, and barrier clearance remain rejected or blocked until the proof-status gate can be promoted.

Each problem also includes a `primeproject.proof-reduction-contract.v1` object. The contract states the smallest theorem package that would make a full-proof claim reviewable, separates accepted partial results from the target conjecture, and lists forbidden shortcuts such as replacing strong Goldbach with weak Goldbach or replacing exact twin gaps with bounded gaps.

Each problem also includes a `primeproject.proof-candidate-intake.v1` object. The intake rules say what a future proof candidate must submit, which executable tests run first, and which shortcuts cause automatic rejection before review.

Each problem also includes a `primeproject.proof-attempt-execution-log.v1` object. The log records executed proof routes, the machine checks applied to each route, the bounded or rejected result, the failure reason, and the exact next artifact required before the route can be promoted.

Each problem also includes a `primeproject.proof-obligation-dag.v1` object. The DAG links attempts, proof gaps, milestones, the decisive reduction theorem, and the open target claim so that every remaining proof obligation is visible as a node with a required artifact and dependency edge.

Each problem also includes a `primeproject.formal-skeleton-audit.v1` object. The audit checks that the named Lean-oriented replay skeleton files exist under `formal/`, contain no forbidden proof-hole tokens, and remain explicitly marked as not proving any infinite bridge.

Each problem also includes a `primeproject.formal-proof-contract.v1` object. The contract records a Lean 4 target theorem, required artifacts, forbidden assumptions, and acceptance rules. This is not a formal proof yet; it is the kernel-facing contract that any future proof must satisfy before the status gate can move.

Each problem also includes a `primeproject.proof-milestone-queue.v1` object. The queue turns the proof contract into work items: the bounded certificate is the only completed milestone, while formal definitions, infinite bridge theorems, and independent kernel review remain open or blocked.

Each problem also includes a `primeproject.decisive-lemma-lab.v1` object. This is the current proof-forge target: it names the single lemma that would close the most important open milestones, records the finite probe that PrimeProject can already replay, and states the proof obligation and falsification test that prevent finite evidence from being misrepresented as a full solution. The same object now carries an automated falsification probe with bounded pass conditions, violation counts, strongest observed stress cases, the explicit proof gap that keeps the problem open, and a `primeproject.decisive-lemma-probe-certificate.v1` hash certificate over the probe payload.

The decisive lemma lab also carries a `primeproject.proof-gap-taxonomy.v1` object. This breaks the remaining proof gap into named open or blocked items such as infinite-lift, theorem-bridge, formalization, dependency-control, and independent-review gaps. Each gap must name the artifact needed to close it, the next experiment to run, and the failure signal that would invalidate that path.

## Claim Boundary

The pages must keep these claims blocked:

- unverified full-proof claim for the Riemann Hypothesis
- unverified full-proof claim for the Collatz conjecture
- unverified full-proof claim for the Goldbach conjecture
- unverified full-proof claim for the Twin Prime conjecture

Finite computation can disprove a universal conjecture if it finds a counterexample, but it cannot prove these universal or infinitude statements by itself. Any future promotion from `open_not_proven` requires an independently checkable argument that removes the search limit.

한국어 경계: 유한 계산은 반례를 찾으면 보편 명제를 반박할 수 있지만, 그 자체로 보편 명제나 무한히 많은 대상의 존재를 증명하지 못한다. `open_not_proven`에서 승격하려면 search limit을 제거하는 독립 검증 가능한 무한 논증이 필요하다.

## Research Direction

The next useful step is to convert repeated empirical structure into explicit lemmas and then aggressively falsify them:

- Riemann: run positivity-kernel search over explicit-formula test functions, then reject any kernel that needs an RH-equivalent assumption.
- Collatz: build residue-block descent certificates and prove recursive coverage of all blocks with a strict well-founded ranking function.
- Goldbach: optimize explicit two-prime lower-bound constants until the analytic cutoff can be joined to the bounded certificate.
- Twin Prime: isolate admissible two-point patterns and search for exact-gap sieve weights that do not collapse to bounded-gap evidence.

한국어 연구 방향:

- 리만가설: explicit formula test function에 대한 positivity-kernel search를 실행하고, RH와 동치인 가정을 요구하는 kernel은 제거한다.
- 콜라츠: residue-block descent certificate와 strict well-founded ranking function을 찾아 모든 block을 덮는다.
- 골드바흐: two-prime lower bound의 explicit constant를 최적화해 analytic cutoff를 bounded certificate와 연결한다.
- Twin Prime: admissible two-point pattern과 exact-gap sieve weight를 탐색하되, bounded-gap 결과로 약화되는 후보는 제거한다.
