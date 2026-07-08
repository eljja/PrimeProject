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

## Latest Continuation After TICKET-48

TICKET-48 supersedes the arbitrary finite-state part of the TICKET-47 continuation. It keeps the same 16-edge positive-debt Collatz template lasso and proves a sharper abstract no-go discipline:

- if a fixed finite total deterministic state update is applied to a repeatable lasso word, then one lasso period induces a finite map \(F:S\to S\);
- iterating \(F\) repeats a finite state after at most `state_count + 1` periods;
- the template node also returns to the lasso start, so the expanded template/state quotient contains a finite directed cycle;
- therefore a finite-state strict-descent proof over this abstract lasso cannot work.

The concrete reachability probe then scans the bounded 28-bit frontier:

```text
start-template candidates: 4
step 1 surviving paths: 2
step 2 surviving paths: 1
step 3 surviving paths: 0
complete positive-pressure lasso period: none found
best partial depth: 2
best partial debt: 1.169925001442
```

This is still not a Collatz proof and not a Collatz counterexample. It narrows the next real mathematical target: either prove symbolic reachability exclusion for the lasso family, or find a concrete periodic lift witness at a larger horizon and then prove it repeats unboundedly.

Current best continuation:

```text
CO-TICKET-49 SymbolicReachabilityExclusionOrConcretePeriodicLift
```

Updated copy-paste prompt:

```text
Act as a skeptical theorem-search and counterexample-synthesis agent working from PrimeProject TICKET-48.

Known result: scalar clause ranks failed at TICKET-46. Bounded suffix-memory repairs failed at TICKET-47. TICKET-48 strengthens the abstract obstruction: any fixed finite total deterministic state repair over the extracted 16-edge positive-debt abstract lasso repeats under the one-period map. However, the bounded concrete residue-lift probe found only a 2-step concrete partial path and no complete lasso period through 28 bits.

Do not retry scalar rank, bounded suffix-memory, or finite total deterministic automaton repair as a proof route over the same abstract lasso.

Goal: either prove a symbolic reachability-exclusion theorem for the TICKET47/TICKET48 lasso family, or find a concrete periodic lift witness at a larger horizon and state the exact unbounded repetition theorem it would require.

Tasks:
1. Formalize the lasso word as constraints on residue classes, valuations, phase, tail word, residue mod 256, and next valuation.
2. Derive the symbolic preimage relation for one lasso period, not just sampled frontier starts.
3. Decide whether the period-preimage system is empty for every future phase-compatible modulus.
4. If empty, state the reachability-exclusion lemma in machine-checkable form.
5. If nonempty, extract a concrete residue path, compute its actual delta debt on every step, and test whether the period map can repeat.
6. For RH, Goldbach, and Twin Prime, transfer only the method: lasso reachability must be separated from finite-state repair; do not claim a conjecture theorem without the infinite bridge.

End with exactly one status:
- symbolic_reachability_exclusion_candidate
- concrete_periodic_lift_candidate
- bounded_probe_inconclusive
- invalid_finite_state_repair

Never output `Collatz proved` unless the all-future reachability or descent theorem is supplied in independently checkable form.
```

## Latest Continuation After TICKET-49

TICKET-49 supersedes the vague reachability part of the TICKET-48 continuation. It does not solve Collatz, but it identifies the exact local coordinate where the first concrete lasso-prefix attempt fails.

Exact 16-bit result:

```text
start template: [0,[1,1,1,1],103,1]
start candidates: 26471, 28007, 34919, 48743
forced-low survivors after step 1: 2
forced-low survivors after step 2: 1
forced-low survivors after step 3: 0
minimal dead step: 3
obstruction coordinate: next_valuation
observed third template on unique survivor: [3,[1,1,1,1],103,5]
required third template: [3,[1,1,1,1],103,1]
```

The next question is no longer “try another finite automaton.” It is:

```text
CO-TICKET-50 AllPhaseNextValuationPreimageOrHigherBitException
```

Updated copy-paste prompt:

```text
Act as a skeptical theorem-search and counterexample-synthesis agent working from PrimeProject TICKET-49.

Known result: scalar ranks failed at TICKET-46. Bounded suffix memory failed at TICKET-47. Fixed finite total state repairs over the abstract lasso failed at TICKET-48. TICKET-49 identifies the first concrete lasso-prefix obstruction: at the exact 16-bit phase-compatible start, the forced-low prefix has survivor counts 4 -> 2 -> 1 -> 0, and the unique two-step survivor has next_valuation 5 at the third phase instead of the required 1.

Do not retry scalar rank, bounded memory, or finite-state repair. Do not merely run a larger sample without explaining the next_valuation preimage.

Goal: either prove that the third-step next_valuation obstruction persists for every phase-compatible modulus b == 0 mod 16, or find a higher-bit exception where the same lasso-prefix reaches next_valuation 1 and can continue.

Tasks:
1. Formalize the first three lasso-prefix constraints as a symbolic preimage condition on residue classes.
2. Derive the recurrence for the next_valuation after two forced-low matching steps.
3. Decide whether next_valuation = 1 is impossible at the third step for every b == 0 mod 16.
4. If impossible, state the all-phase obstruction theorem in machine-checkable form.
5. If possible, extract the smallest higher-bit residue exception and continue the full 16-edge lasso test.
6. Transfer the method to RH, Goldbach, and Twin Prime only as a coordinate-obstruction discipline; do not claim those conjectures are solved.

End with exactly one status:
- all_phase_next_valuation_obstruction_candidate
- higher_bit_exception_found
- recurrence_derivation_incomplete
- invalid_finite_state_retry

Never output `Collatz proved` unless the all-future obstruction or a complete independent descent theorem is supplied in checkable form.
```

## Latest Continuation After TICKET-50

TICKET-50 supersedes the TICKET-49 all-phase next-valuation continuation target. It preserves the 16-bit obstruction, but proves that the proposed global obstruction was too strong by finding higher-bit phase-compatible exceptions.

New exact findings:

```text
16-bit start-template matches: 4
16-bit four-consecutive-one exceptions: 0
16-bit max lasso-prefix depth: 3
32-bit start-template matches: 69,092
32-bit four-consecutive-one exceptions: 8,684
32-bit max lasso-prefix depth: 15
32-bit depth-15 residues: 1471663463, 3206130791
terminal failures:
  1471663463 -> phase 15 tail shift [1,1,1,10] with next_valuation 1
  3206130791 -> all_lift_descent at bits 47
```

The local valuation-run lemma is now explicit:

```text
For odd boundary x, r consecutive accelerated valuations equal 1 iff x == -1 mod 2^(r+1).
```

Do not attempt to prove the old TICKET-49 candidate theorem. It is already refuted by the 32-bit phase-compatible exception scan. Do not claim a Collatz counterexample from the depth-15 residues; neither completes the full lasso period.

Current best Collatz continuation:

```text
CO-TICKET-51 Phase15TerminalLiftOrFullLassoCompletion
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-50. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-49 found a 16-bit Collatz next_valuation obstruction, but TICKET-50 refuted the all-phase version at 32 bits. At 32 bits, the start template [0,[1,1,1,1],103,1] has 69,092 exact valuation-word matches, 8,684 four-consecutive-one low-lift exceptions, and two residues reaching 15 of the 16 lasso-prefix templates: 1471663463 and 3206130791. The first fails by tail shift at phase 15; the second closes by all_lift_descent at bits 47.

Goal: build CO-TICKET-51. Lift only these two depth-15 residues through the missing phase-15 edge. Classify all descendants into: all_lift_descent closure, tail shift away from [1,1,1,1], next_valuation mismatch, or full lasso completion. If a full completion appears, replay it for at least two periods and state the exact infinite periodicity theorem still required. If no completion appears within the symbolic lift envelope, formulate the terminal obstruction as a candidate theorem.

Required output:
- data/open-problem/ticket51-phase15-terminal-lift-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless an infinite replay theorem is supplied
```

## Latest Continuation After TICKET-51

TICKET-51 supersedes the TICKET-50 terminal-lift continuation target. It starts only from the two 32-bit depth-15 near-lasso roots and opens every low/high branch through the missing phase-15 edge.

Exact result:

```text
source roots: 1471663463, 3206130791
terminal step: 15
terminal branches tested: 4
matching terminal branches: 0
final surviving states: 0
full lasso completions: 0
terminal mismatch counts:
  all_lift_descent: 2
  tail_word+next_valuation: 2
```

Do not continue treating either TICKET-50 root as a live counterexample candidate. Both ancestries are terminally closed for the extracted lasso template. The remaining search must either find new roots outside this ancestry or prove a symbolic terminal-closure theorem.

Current best Collatz continuation:

```text
CO-TICKET-52 New48Or64BitRootSearchOrTerminalTheorem
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-51. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-51 closes the terminal low/high lift tree for the two known 32-bit Collatz near-lasso roots 1471663463 and 3206130791. No branch completes the phase-15 template; two branches fail by tail_word+next_valuation shift and two by all_lift_descent. Therefore these two roots are no longer live counterexample candidates.

Goal: build CO-TICKET-52. Search for genuinely new 48-bit or 64-bit start-template roots with lasso-prefix depth >= 15, without reusing the two closed TICKET-50 ancestries. Use exact valuation-word or symbolic lift constraints, not blind residue enumeration. If no new roots are found within the declared envelope, formulate the terminal-closure theorem that would be needed. If a full lasso completion is found, replay it for at least two periods and state the exact infinite periodicity theorem still required.

Required output:
- data/open-problem/ticket52-new-root-search-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless an infinite replay theorem is supplied
```

## Latest Continuation After TICKET-47

TICKET-47 supersedes the bounded suffix-memory part of the TICKET-46 continuation. It extracts a 16-edge positive-debt lasso from the 28-bit Collatz exact-template pressure graph and refutes:

- zero-memory pressure rank;
- last-1 edge-signature memory;
- last-2 edge-signature memory;
- last-3 edge-signature memory;
- last-4 edge-signature memory.

This is not a Collatz counterexample because the lasso is an abstract template-pressure cycle, not a certified single reachable Collatz orbit.

Current best continuation:

```text
CO-TICKET-48 AutomatonCEGISOr29BitReachability
```

Updated copy-paste prompt:

```text
Act as a skeptical theorem-search and counterexample-synthesis agent working from PrimeProject TICKET-47.

Known result: scalar clause ranks failed at TICKET-46. Bounded suffix-memory stateful repairs up to last-4 edge signatures failed at TICKET-47 on a 16-edge positive-debt abstract pressure lasso.

Do not retry scalar rank or bounded suffix-memory repair as a proof route.

Goal: either prove that the extracted abstract pressure lasso is unreachable by concrete Collatz lift paths, or synthesize/refute arbitrary small finite-state automata on the pressure relation.

Tasks:
1. Formalize the 28-bit lasso as an abstract transition word.
2. State exactly what concrete reachability would mean for residues and lifted paths.
3. Search for a concrete 29-bit/30-bit realization of the lasso. If found, record it as a stronger counteredge against template-based proof routes.
4. If no concrete realization is found, state the reachability exclusion lemma that would be needed.
5. In parallel, synthesize arbitrary finite-state automata with 2, 3, 4, ... states and test whether the lasso or a larger pressure graph creates an expanded-state cycle.
6. If every small automaton fails, record the minimal failing lasso certificate.
7. If one survives, state the exact infinite theorem required before it can support Collatz.

End with exactly one status:
- concrete_lasso_counteredge_found
- reachability_exclusion_lemma_needed
- finite_automaton_refuted
- bounded_survivor_needs_infinite_bridge

Never output `Collatz proved` unless the all-future lift theorem is supplied in independently checkable form.
```
