# LLM Open-Problem Handoff

## Purpose

이 문서는 다른 LLM이 PrimeProject의 현재 연구 상태를 이어받아 리만가설, 콜라츠 추측, 골드바흐 추측, Twin Prime 추측에 대한 AI-assisted proof search를 계속 진행하기 위한 handoff 문서다.

중요한 경계:

- PrimeProject는 현재 네 난제 중 어느 것도 증명하지 않았다.
- 현재 산출물은 증명 논문이 아니라 `open_not_proven` 상태의 proof-search workbench다.
- 목표는 이미 알려진 유한 계산, 시각화, 휴리스틱을 재현하는 것이 아니다.
- 목표는 새 수학적 객체, 새 보조정리, 반례 오라클, 형식화 가능한 증명 티켓을 만들어 실제 미해결 장벽을 공격하는 것이다.

## Current Repository State

Primary public page:

- `https://eljja.github.io/PrimeProject/`

Open-problem pages:

- `https://eljja.github.io/PrimeProject/open-problems/riemann.html`
- `https://eljja.github.io/PrimeProject/open-problems/collatz.html`
- `https://eljja.github.io/PrimeProject/open-problems/goldbach.html`
- `https://eljja.github.io/PrimeProject/open-problems/twin-prime.html`

Core files:

- `data/open_problem_workbench.json`: generated open-problem research state.
- `scripts/generate_open_problem_workbench.py`: generator for bounded evidence, proof workbench objects, CEGIS loops, theorem tickets.
- `scripts/verify_open_problem_workbench.py`: conservative verifier that blocks proof claims.
- `assets/open-problems.js`: GitHub Pages renderer for the four workbench pages.
- `formal/*/InfiniteBridge.lean`: Lean-oriented skeleton contracts. These are not proofs.
- `docs/open-problem-workbench.md`: public workbench specification.

Regeneration and verification commands:

```powershell
python scripts/generate_open_problem_workbench.py --limit 1000000 --output data/open_problem_workbench.json
python scripts/verify_open_problem_workbench.py
node scripts/verify_pages.cjs
python -m unittest discover -s tests -p "test_*.py"
python scripts/reproduce_publication.py
```

## What Has Been Built

The workbench currently provides:

- bounded certificates for finite evidence only;
- proof verdict panels that keep all four conjectures `open_not_proven`;
- invalid shortcut rejection rules;
- decisive theorem specs and subgoals;
- AI proof forge sections;
- theorem decomposition for the next attempted theorem;
- breakthrough object blueprints;
- counterexample-guided synthesis loops;
- ranked CEGIS candidates;
- top attack theorem tickets;
- proof attempt protocols with required outputs and fail exits.

This is useful because it prevents the common failure mode where an LLM produces a plausible but invalid proof by silently replacing an infinite theorem with finite evidence, a heuristic, or a weaker theorem.

## Current Top Attack Tickets

### Riemann Hypothesis

Top ticket:

- `RH-TICKET-1 CompactKernelConePositivity`

Candidate theorem:

- Every admissible kernel in a generated two-parameter compact cone has a non-circular positivity certificate whose explicit-formula image is valid for all heights.

Attack direction:

- Construct signed kernel cones with machine-checkable positivity certificates.
- Audit every imported theorem so no RH-equivalent premise enters.
- Search adversarial kernels outside the generated cone.

Failure condition:

- The route fails if positivity is only finite-height, sampled, or dependent on an RH-equivalent theorem.

### Collatz Conjecture

Top ticket:

- `CO-TICKET-1 ValuationDebtSccDescent`

Candidate theorem:

- Every non-basin strongly connected component in an accelerated residue-debt automaton has an exact rational exit edge that strictly decreases valuation-debt rank.

Attack direction:

- Build an accelerated residue partition.
- Attach exact rational rank inequalities to every edge.
- Use SCC search to find nondecreasing counterexamples.

Failure condition:

- The route fails if any residue block is uncovered or any SCC admits a nondecreasing closed path.

### Goldbach Conjecture

Top ticket:

- `GB-TICKET-1 ExplicitBudgetCutoffBelowCertificate`

Candidate theorem:

- A normalized major/minor arc budget gives `R_2(n) > 0` for every even `n >= N0`, with `N0` below the finite certificate ceiling.

Attack direction:

- Convert every analytic term into a budget line with theorem source, constant, and validity range.
- Compute `N0` exactly.
- Check finite-large interval glue.

Failure condition:

- The route fails if any line is heuristic, asymptotic-only, uncited, ineffective, or if `N0` remains above the verified finite range.

### Twin Prime Conjecture

Top ticket:

- `TP-TICKET-1 ExactPairSelectorParitySurvival`

Candidate theorem:

- An exact-pair selector with explicit wider-gap subtraction has positive exact gap-2 mass after parity-model stress.

Attack direction:

- Define exact-pair selector weights.
- Subtract wider-gap leakage.
- Replay the selector in semiprime parity countermodels before using prime data.

Failure condition:

- The route fails if the positive mass can be reinterpreted as bounded gaps or survives in a parity model without forcing exact twin primes.

## Recommended Strategy For The Next LLM

Do not try to solve all four at once. Pick one ticket and make one mathematical object more precise.

Most practical next target:

- Collatz `CO-TICKET-1`, because the target can be attacked with exact finite automata, SCC search, rational inequalities, and a clear fail oracle.

Highest mathematical upside:

- Riemann `RH-TICKET-1`, but this is much more likely to fail through circularity or insufficient density.

Most publication-friendly:

- Goldbach `GB-TICKET-1`, because it can be framed as explicit-constant auditing even if the final cutoff does not close.

Hardest barrier:

- Twin Prime `TP-TICKET-1`, because parity barrier survival is exactly where ordinary sieve routes fail.

## Copy-Paste Prompt For Another LLM

```text
You are continuing PrimeProject, an AI-assisted proof-search project for four open problems:
1. Riemann Hypothesis
2. Collatz Conjecture
3. Goldbach Conjecture
4. Twin Prime Conjecture

Important truth boundary:
- PrimeProject has not proved any of these four conjectures.
- You must not claim a proof unless you produce an independently checkable infinite argument or a formal proof artifact.
- Finite computation, visual evidence, heuristic density, known equivalent restatements, and weaker theorems do not count as solving the target problem.
- Your task is not to reproduce known easy results. Your task is to search for a genuinely new theorem, object, or proof route that attacks a known barrier.

Repository context:
- Main generated data: data/open_problem_workbench.json
- Generator: scripts/generate_open_problem_workbench.py
- Verifier: scripts/verify_open_problem_workbench.py
- Renderer: assets/open-problems.js
- Formal skeletons: formal/*/InfiniteBridge.lean
- Workbench doc: docs/open-problem-workbench.md
- LLM handoff doc: docs/llm-open-problem-handoff.md

Current proof-search structures:
- theorem_decomposition
- breakthrough_object_blueprint
- counterexample_guided_synthesis
- ranked CEGIS candidates
- top_attack_theorem_ticket
- proof_attempt_protocol

Current top attack tickets:
- Riemann: RH-TICKET-1 CompactKernelConePositivity
- Collatz: CO-TICKET-1 ValuationDebtSccDescent
- Goldbach: GB-TICKET-1 ExplicitBudgetCutoffBelowCertificate
- Twin Prime: TP-TICKET-1 ExactPairSelectorParitySurvival

Your first job:
Pick exactly one ticket, preferably CO-TICKET-1 unless you can justify another choice. Then:
1. Restate the candidate theorem in precise mathematical language.
2. List every assumption.
3. Identify which assumptions are already accepted, which are generated by PrimeProject, and which are unproved.
4. Construct the smallest possible object needed for the theorem.
5. Try to falsify it with the listed counterexample oracle.
6. If it fails, write the failure as a precise lemma or counterexample class.
7. If it survives, propose the next formal artifact to add under formal/<problem>/.
8. Keep the public claim status open_not_proven unless the infinite bridge is actually closed.

Required output:
- A short mathematical analysis.
- A proposed patch to data/open_problem_workbench.json generation logic, not hand-edited generated JSON.
- Any needed update to formal/*/InfiniteBridge.lean as a skeleton only.
- Verification commands to run.
- A final statement that clearly distinguishes progress from proof.

Do not:
- claim that finite verification proves an infinite conjecture;
- use RH-equivalent assumptions to prove RH;
- use density or random drift to prove Collatz for all values;
- replace strong Goldbach with weak/almost-all Goldbach;
- replace exact twin primes with bounded prime gaps;
- hide a missing infinite theorem inside prose.
```

## Stronger Prompt For A Math-Focused LLM

```text
Act as a skeptical mathematical proof reviewer and theorem-search agent.

We are not asking for a polished explanation of known results. We are trying to discover whether an LLM can produce a genuinely new route on one of four open problems. You must be honest, adversarial, and precise.

Choose one PrimeProject top attack theorem ticket:
- RH-TICKET-1 CompactKernelConePositivity
- CO-TICKET-1 ValuationDebtSccDescent
- GB-TICKET-1 ExplicitBudgetCutoffBelowCertificate
- TP-TICKET-1 ExactPairSelectorParitySurvival

For the chosen ticket:
1. Formalize the candidate theorem as sharply as possible.
2. State the minimal definitions required.
3. State the exact theorem that, if proved, would move the project closer to the full conjecture.
4. Try to disprove the candidate theorem before trying to prove it.
5. Produce either:
   - a counterexample/failure mode;
   - a strictly weaker theorem that is actually provable and useful;
   - or a precise formalization target that should be added to Lean.

You must not produce inspirational prose. You must produce mathematical objects, assumptions, implications, and failure tests.

End with one of these statuses:
- failed_candidate
- weaker_theorem_found
- formalization_target_ready
- infinite_bridge_candidate_found

Only use `infinite_bridge_candidate_found` if you can clearly state the new all-cases theorem and why it avoids the known barrier.
```

## Suggested First Continuation

Start with `CO-TICKET-1 ValuationDebtSccDescent`.

Reason:

- It has the clearest computational counterexample oracle: SCC search for nondecreasing cycles.
- It can be made exact with rational inequalities.
- It does not require deep analytic number theory constants or RH-equivalent criteria.
- It is still genuinely hard because a single exceptional SCC breaks the route.

Initial task:

Define a small accelerated odd-residue system modulo `2^k`, attach a valuation-debt rank, compute SCCs, and search for a nondecreasing closed path. If one exists, record the obstruction as the next lemma to defeat. If none exists at that modulus, increase only the obstructing components rather than claiming global proof.

## Claim Boundary For Future Work

Any future LLM must preserve this statement:

> PrimeProject can organize proof search and falsification for these four open problems, but it does not prove any of them until an independently checkable infinite argument or formal proof artifact closes the missing infinite bridge.

## Latest Continuation After TICKET-46

TICKET-46 supersedes the earlier Collatz scalar-rank continuation target. The project pushed the Collatz lift-template stress test to 28 bits and found that every tested finite template-local scalar clause-rank grammar is pressure-cyclic:

- `phase_only`
- `phase_tail_mass_vbucket`
- `phase_tail_residue16_vbucket`
- `phase_tail_residue64_vbucket`
- `phase_tail_residue256_vexact`

The exact observed-template table is therefore no longer a viable scalar clause-rank proof route after 28-bit wrap stress. This is a restricted no-go theorem for the tested proof route, not a Collatz proof or counterexample.

Current best Collatz continuation:

```text
CO-TICKET-47 OrdinalStatefulMeasureOr29BitCounteredge
```

Required direction:

1. Do not retry a scalar rank on the five TICKET45/TICKET46 grammars.
2. Propose an ordinal-valued or stateful measure whose update rule is template-local and fixed before increasing `max_bits`.
3. Explicitly reject any repair that uses `max_bits`, lift depth, or an unwrapped phase epoch unless that coordinate is defined by a horizon-independent transition theorem.
4. Search for a 29-bit or 30-bit counteredge against the proposed update rule before attempting proof.
5. If a candidate survives bounded stress, state the exact infinite theorem needed to promote it.

Updated copy-paste prompt:

```text
Act as a skeptical mathematical theorem-search agent working from PrimeProject TICKET-46.

Known result: at 28 bits, all five tested finite template-local scalar Collatz clause-rank grammars are refuted by nonnegative-pressure cycles. Therefore you must not repeat phase-only, tail-mass, residue16, residue64, or exact observed-template scalar rank as a proof route.

Goal: either find a genuinely stronger horizon-independent ordinal/stateful Collatz measure, or find a counteredge against such a candidate.

Tasks:
1. Define the candidate state space and measure in precise mathematical language.
2. Prove that the state update is independent of max_bits and lift depth, or explicitly mark it as invalid.
3. State the decrease inequality for every future lifted open edge.
4. Try to falsify the inequality with a 29-bit/30-bit lift counteredge.
5. If falsified, record the exact failing edge class.
6. If not falsified, state the remaining infinite bridge theorem without claiming Collatz is proved.

End with exactly one status:
- invalid_horizon_dependent_coordinate
- counteredge_found
- bounded_survivor_needs_infinite_bridge
- formal_theorem_candidate_ready

Never output `Collatz proved` unless the all-future lift theorem is supplied in independently checkable form.
```
