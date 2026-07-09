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

## Latest Continuation After TICKET-71

TICKET-71 supersedes the immediate TICKET-70 continuation target. It does not solve Collatz, but it tests whether the TICKET70 re-entry pressure can be separated by explicit pre-outcome coordinates.

Known Collatz result:

```text
Frontier source states: 6,649
Concrete frontier representatives: 49,504
Frontier branch weight: 792,064
Pressure rows: 214,770
Tested coordinate families: 6

base_prefix_consumed:
  expanded graph rank: 7
  child-only frontier after expansion: 8,055
  mixed transition keys: 22,219

base_fullword_residue65536:
  mixed transition keys: 0
  transition keys: 792,064
  state count: 319,801
  child-only frontier after expansion: 254,488
```

Interpretation:

```text
TICKET71 finds a bounded separator, but not a proof. The full valuation-word plus residue mod 2^16 coordinate separates the tested branch outcomes without post-hoc labels, but it behaves like a high-cardinality bounded separator and greatly expands the frontier. The compact baseline coordinate keeps the graph acyclic and small, but leaves mixed transition keys. The next target is not "use the biggest coordinate"; it is to prove horizon-independent lift closure for a compact coordinate, or extract a persistent chain from the mixed keys.
```

Do not claim Collatz from this. A bounded transition separator is not a theorem over all compatible future lifts.

Current best continuation:

```text
CO-TICKET-72 InfiniteFrontierCoordinateLiftClosureOrChain
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-71. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET71 tested six coordinate families on the TICKET70 frontier. base_fullword_residue65536 has zero mixed transition keys on the bounded branch set, but expands the child-only frontier to 254,488 states. base_prefix_consumed keeps the expanded graph acyclic with rank 7 and child-only frontier 8,055, but leaves 22,219 mixed transition keys.

Goal: build CO-TICKET-72. Decide whether the compact expanded DAG admits horizon-independent lift closure, or extract a persistent compatible lift chain from the mixed transition keys.

Tasks:
1. Load data/open-problem/ticket71-stronger-frontier-coordinate-lab.json.
2. Reconstruct mixed transition keys for base_prefix_consumed from scripts/ticket71_stronger_frontier_coordinate_lab.py.
3. Do not use full valuation word as a proof coordinate unless you can state a compact symbolic transition theorem for it.
4. For the top mixed transition keys, lift representative residues one more 4-bit layer and check whether the mixed profile stabilizes, splits by a smaller coordinate, or forms a persistent chain.
5. Test compact candidate coordinates before outcome labels: residue mod 2^k for small k, tail word windows, child_top, prefix/consumed deltas, next valuation, and low40/high-extension style coordinates.
6. If a compact coordinate closes, state the infinite lift-closure theorem needed.
7. If no compact coordinate closes, extract the repeated lift-chain constraints as a counterexample target.
8. Keep the proof boundary explicit: no conjecture is solved without a formal infinite theorem or certified counterexample.

Required output:
- data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite lift theorem or a certified counterexample is supplied
```

## Previous Continuation After TICKET-70

TICKET-70 supersedes the immediate TICKET-69 continuation target. It does not solve Collatz, but it tests the most direct rank-0 frontier closure shortcut and refutes it on the observed concrete representatives.

Known Collatz result:

```text
Coordinate family: base_prefix_consumed
Source frontier states: 6,649
Concrete frontier representatives: 49,504
Expansion edge weight: 792,064
Frontier internal edge weight: 214,770
Outcome counts:
  open_base_cycle_exit = 516,176
  internal_rank_equal_frontier_cycle_pressure = 123,403
  closed_or_terminal_all_lift_descent = 61,118
  internal_new_unranked_state = 59,449
  internal_rank_increase_frontier_cycle_pressure = 31,918
State classes:
  rank0_frontier_reenters_ranked_dag = 4,498
  rank0_frontier_enters_new_unranked_state = 1,125
  rank0_frontier_exits_or_closes = 1,026
Representative-nondeterministic frontier states: 3,537
Combined one-step refined cycle components: 0
```

Interpretation:

```text
The direct proof shortcut "rank-0 frontier states are terminal sinks" is false. Many concrete representatives re-enter known ranked states without rank descent, and many enter internal states that are not in the TICKET69 DAG. However, the one-step combined graph still has no refined cycle, so this is not a Collatz counterexample. The proof target has moved to a stronger pre-replay frontier coordinate or to extraction of a persistent compatible lift cycle.
```

Do not claim Collatz from this. TICKET70 is a bounded representative expansion, not a theorem over all compatible lifts.

Current best continuation:

```text
CO-TICKET-71 StrongerFrontierCoordinateOrPersistentLiftCycle
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-70. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET70 expands the TICKET69 rank-0 prefix/consumed frontier. It refutes direct rank-0 closure: among 792,064 one-step branches, 155,321 re-enter known ranked states without rank descent and 59,449 enter new unranked internal states. No one-step combined refined cycle was found.

Goal: build CO-TICKET-71. Find the smallest pre-replay coordinate that separates the TICKET70 re-entry pressure, or extract a compatible higher-lift chain that keeps re-entering ranked/unranked internal states without descent.

Tasks:
1. Load data/open-problem/ticket70-prefix-frontier-expansion-lab.json.
2. Reconstruct the TICKET70 re-entry examples from scripts/ticket70_prefix_frontier_expansion_lab.py.
3. Split the pressure set into rank-equal, rank-increase, and new-unranked internal transitions.
4. Test candidate coordinates that are available before replay: added low residue bits, tail word, high extension bits, next valuation, prefix/consumed deltas, and source-child transition labels.
5. Reject any coordinate that only labels outcomes after replay.
6. If a coordinate separates the pressure, build a new ranked transition graph and test for cycles.
7. If no coordinate separates it, extract a persistent lift-chain candidate as a serious counterexample target.
8. Keep the proof boundary explicit: a bounded coordinate separator is not a proof until it induces an infinite transition theorem.

Required output:
- data/open-problem/ticket71-stronger-frontier-coordinate-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite transition theorem or a certified counterexample is supplied
```

## Previous Continuation After TICKET-69

TICKET-69 supersedes the immediate TICKET-68 continuation target. It does not solve Collatz, but it converts the TICKET68 prefix/consumed DAG into a stricter bounded rank certificate and identifies the precise frontier that blocks a proof.

Known Collatz result:

```text
Coordinate family: base_prefix_consumed
Rank states: 9,616
Max rank: 5
Source base cycle nodes: 429
Observed internal edge weight: 89,222
Nondecreasing rank edges: 0
Source instances in base cycle: 16,967
Child outcomes:
  internal_rank_descent = 89,222
  open_base_cycle_exit = 174,589
  closed_or_terminal_all_lift_descent = 7,661
Source-expanded states: 3,025
Source-and-child states: 1,390
Source-only states: 1,635
Child-only unexpanded states: 6,649
Unexpanded child-only rank counts: rank 0 = 6,649
```

Interpretation:

```text
The prefix/consumed rank is valid on every observed internal edge: no nondecreasing rank edge remains. The proof gap has moved. It is no longer "find a local rank on the observed SCC"; it is "prove transition-completeness for the 6,649 rank-0 child-only frontier states, or find a higher-lift refined cycle there."
```

Do not claim Collatz from this. A bounded rank certificate is not an infinite proof until the child-only frontier is either theorem-closed or expanded into a persistent refined cycle.

Current best continuation:

```text
CO-TICKET-70 PrefixConsumedFrontierExpansionOrCycle
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-69. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET69 validates the prefix/consumed DAG rank on all 89,222 observed internal Collatz edges: every edge strictly decreases rank and there are zero nondecreasing rank violations. The remaining obstruction is a rank-0 child-only frontier of 6,649 refined states.

Goal: build CO-TICKET-70. Expand the 6,649 rank-0 child-only prefix/consumed frontier states one more transition level. Classify every expansion as exit, descent, rank decrease into an already covered state, or a new refined cycle. If a refined cycle appears, extract its congruence constraints as a serious counterexample target. If no cycle appears, state the next transition-completeness theorem and its remaining infinite bridge.

Tasks:
1. Load data/open-problem/ticket69-prefix-consumed-rank-lab.json.
2. Reconstruct the exact unexpanded rank-0 frontier from scripts/ticket69_prefix_consumed_rank_lab.py.
3. For each frontier state, use concrete representatives already stored in the TICKET69 examples or reconstruct them from TICKET68 transition rows. Do not add post-hoc replay labels.
4. Expand representative states by one 4-bit lift and classify outcomes with the same base_prefix_consumed coordinate.
5. Report whether any nondecreasing refined cycle appears.
6. Keep the proof boundary explicit: a finite expansion is not a proof unless it induces a theorem valid for all compatible lifts.

Required output:
- data/open-problem/ticket70-prefix-frontier-expansion-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite transition-completeness theorem is supplied
```

## Previous Continuation After TICKET-68

TICKET-68 supersedes the immediate TICKET-67 continuation target. It does not solve Collatz, but it tests whether the TICKET67 429-node cyclic quotient survives theorem-plausible coordinate refinements.

Known Collatz result:

```text
Source base transition nodes: 5,100
Source base transition edges: 45,665
Source base transition weight: 265,812
Source cyclic nodes: 429
Source cycle edge weight: 89,222
Open exits from cycle: 174,589
Tested refinement families: 7
Strongest acyclic refinement: base_prefix_consumed
base_prefix_consumed states: 9,616
base_prefix_consumed edges: 41,283
base_prefix_consumed cyclic nodes: 0
base_prefix_consumed observed topological rank: 5
Best tail/residue-only refinement: tail8_res4096_vexact
tail8_res4096_vexact cyclic nodes: 26
tail8_res4096_vexact cyclic edge weight: 129
```

Interpretation:

```text
The TICKET67 429-node quotient cycle is not an unavoidable obstruction. It disappears on the observed transition set once exact prefix_length and consumed_bits are added to the base template. However, this is still bounded evidence. It becomes a proof only if the prefix/consumed refined transition system is shown to be complete for all compatible higher lifts and its DAG rank is well-founded beyond the observed horizon.
```

Do not claim Collatz from this. The next theorem must prove transition-completeness and rank descent for the prefix/consumed DAG, or find a higher-lift refined cycle that survives this coordinate.

Current best continuation:

```text
CO-TICKET-69 PrefixConsumedDAGCompletenessOrPersistentRefinedCycle
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-68. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET68 refines the TICKET67 429-node cyclic SCC with seven coordinate families. The base quotient remains cyclic, but base_template + prefix_length + consumed_bits turns the observed internal SCC transition graph into a DAG with 9,616 states, 41,283 edges, zero cyclic nodes, and observed topological rank 5. Tail/residue-only refinement still leaves 26 cyclic nodes and 129 cyclic edge weight.

Goal: build CO-TICKET-69. Prove that the base_prefix_consumed DAG is transition-complete for all compatible higher lifts and supports a well-founded rank, or find a higher-lift refined cycle that reappears under the same coordinate.

Tasks:
1. Load data/open-problem/ticket68-cycle-scc-refinement-lab.json.
2. Reconstruct the base_prefix_consumed refined graph from scripts/ticket68_cycle_scc_refinement_lab.py.
3. Formalize the exact state variables: base template, prefix_length, consumed_bits, source bits phase, child top, and certificate transition rule.
4. Test one more lift horizon without adding post-hoc replay labels. The only acceptable failure signal is a refined cycle, a transition-completeness violation, or a rank nondecrease inside the refined DAG theorem candidate.
5. If no cycle reappears, state the finite theorem precisely and list every infinite bridge still missing.
6. If a refined cycle reappears, extract the congruence constraints needed for a compatible infinite 2-adic lift.

Required output:
- data/open-problem/ticket69-prefix-consumed-rank-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite transition-completeness theorem is supplied
```

## Previous Continuation After TICKET-67

TICKET-67 supersedes the immediate TICKET-66 continuation target. It does not solve Collatz, but it tests the obvious next rank shortcuts and isolates a sharper finite quotient obstruction.

Known Collatz result:

```text
Source open instances from TICKET66: 17,134
Source open template families: 491
4-bit child lift rows: 274,144
Child needs_split: 265,812
Child all_lift_descent: 8,332
Source instances closed after one split: 13
Source instances still open after one split: 17,121
Open transition edge count: 45,665
Open transition edge weight: 265,812
Transition nodes: 5,100
Child open template families: 5,056
Cyclic SCC count: 1
Cyclic SCC node count: 429
Cycle edge weight: 89,222
Source families reaching the SCC: 458
Debt nondecreasing edges: 96,433
Debt nondecreasing rate: 0.362786480671
```

Interpretation:

```text
The one-step split route and scalar debt-rank route are refuted. The 429-node SCC is not a Collatz counterexample, because it is only a finite quotient cycle. It becomes relevant only if a compatibility theorem constructs an infinite 2-adic lift through it, or if a refinement theorem proves every compatible path exits.
```

Do not claim Collatz from this. The next theorem must refine the cyclic SCC with additional pre-replay coordinates, or prove that no compatible infinite lift can remain inside the SCC.

Current best continuation:

```text
CO-TICKET-68 CycleSCCRefinementOrInfiniteLiftExclusion
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-67. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET67 split TICKET66's 17,134 open source instances by one more 4-bit lift. Only 13 source instances close after that split, 17,121 remain open, and the open transition graph has a 429-node cyclic SCC with 89,222 internal edge weight. Scalar debt rank is also refuted by 96,433 nondecreasing open child transitions.

Goal: build CO-TICKET-68. Refine the 429-node cyclic SCC with additional pre-replay coordinates, or prove that no compatible infinite 2-adic lift can stay inside that SCC forever.

Tasks:
1. Load data/open-problem/ticket67-open-template-rank-lab.json and extract the cycle_example plus top source families.
2. Reconstruct the SCC transitions from scripts/ticket67_open_template_rank_lab.py.
3. Add only pre-replay coordinates: low bits, high-extension residues, source/child top, prefix length, consumed bits, and template tail data. Do not use post-hoc failure labels.
4. Test whether the SCC splits into acyclic components or smaller SCCs under each coordinate family.
5. If a refined SCC remains, try to build a compatible infinite lift path through it and state exactly which congruence constraints must be solved.
6. If all refined paths exit, state the finite refinement theorem and its missing infinite bridge.

Required output:
- data/open-problem/ticket68-cycle-scc-refinement-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite bridge is supplied
```

## Latest Continuation After TICKET-66

TICKET-66 supersedes the immediate TICKET-65 continuation target. It does not solve Collatz, but it checks the exact complement-cover shortcut demanded after the TICKET65 branch extinction and shows that the shortcut fails.

Known Collatz result:

```text
Complement audit lifts: 56->60, 60->64, 64->68, 68->72, 72->76, 76->80
Non-start complement candidates: 17,189
Closed by immediate all-lift descent: 55
Open needs_split instances: 17,134
Descent coverage rate: 0.003199720752
Unique open template families: 491
Largest open family: [12,[1,1,1,1],103,5] with 432 instances
Main exit pressure: open_wrong_tail_target_residue_mod_256 = 14,244; open_target_tail_wrong_next_valuation = 2,890
```

Interpretation:

```text
The tracked TICKET65 branch is closed, but its complement is not. TICKET66 refutes the idea that every non-start-template exit branch is already handled by existing descent or terminal-family closures. The useful next object is no longer a generic complement cover; it is a rank theorem over 491 open template families, or a compatible infinite lift through one family that becomes a genuine counterexample target.
```

Do not claim Collatz from this. The next theorem must either close the 491 open families with a symbolic rank/measure argument or construct a compatible infinite lift through one family.

Current best continuation:

```text
CO-TICKET-67 OpenTemplateFamilyRankOrComplementCounterexample
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-66. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET65 closed the tracked Collatz start-template chain by 80 bits. TICKET66 then audited the complement: 17,189 non-start-template exit candidates were found, only 55 close by immediate all-lift descent, and 17,134 remain open needs_split instances across 491 template families. The largest family is [12,[1,1,1,1],103,5] with 432 instances. The complement-cover shortcut is refuted.

Goal: build CO-TICKET-67. Either prove a symbolic rank/measure theorem over the 491 open complement template families, or construct a compatible infinite lift through one family that becomes a serious counterexample target.

Tasks:
1. Load data/open-problem/ticket66-complement-cover-lab.json and extract the 491 open template families.
2. Start with the largest families and the smallest open residue witness.
3. Define a pre-replay symbolic state that does not depend on post-hoc failure labels.
4. Search for a well-founded rank that decreases under all compatible lifts of each family.
5. If rank synthesis fails, try to construct a compatible infinite lift through one nondecreasing family and record the exact obstruction to making it a true counterexample.
6. Transfer the same complement-discipline to RH, Goldbach, and Twin Prime: no finite branch closure can become a proof until its complement is covered.

Required output:
- data/open-problem/ticket67-open-template-rank-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite bridge is supplied
```

## Latest Continuation After TICKET-65

TICKET-65 supersedes the immediate TICKET-64 continuation target. It still does not solve Collatz, but it closes the concrete start-template survivor chain that TICKET63/TICKET64 had isolated.

Known Collatz result:

```text
Survivor sequence: 56 bits:824 -> 60 bits:209 -> 64 bits:42 -> 68 bits:12 -> 72 bits:3 -> 76 bits:1 -> 80 bits:0
Full-period replays: 0
64-bit gate best compressed near miss: low40_parent_high10_child_top4, 3 collision groups, 6 ambiguous rows
64-bit first deterministic gate: low40_parent_top_parent_high10_child_top4, but it is row-unique
68-bit best compressed near miss: low40_parent_high2_child_top4, 1 collision group, 2 ambiguous rows
68-bit first deterministic gate: state20_base_mod16_child_top4, but it is row-unique
```

Interpretation:

```text
The tracked start-template branch dies by 80 bits. This is useful branch pruning, not a Collatz proof. It does not show that every integer enters this tracked branch, and it does not cover branches that exit the start-template chain. The compact-gate route also remains blocked because the deterministic gates found in this audit collapse to one state per candidate row.
```

Do not claim Collatz from this. The next theorem must cover the complement, not merely replay the extinct branch.

Current best continuation:

```text
CO-TICKET-66 ComplementCoverForStartTemplateExit
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-65. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET65 follows the TICKET63/TICKET64 start-template chain through 80 bits and observes 824 -> 209 -> 42 -> 12 -> 3 -> 1 -> 0 survivors, with zero full-period replays. This closes the tracked branch only. It also shows that deterministic gate separators at 64 and 68 bits are row-unique, not compressed symbolic automata.

Goal: build CO-TICKET-66. Construct a complement cover for branches that leave the start-template chain, or find a branch that re-enters a lasso-like state outside the current cover.

Tasks:
1. Define the exit classes for non-start-template children at each lift step.
2. Track whether those exit classes fall into already closed terminal families from TICKET53/TICKET55/TICKET56, or require a new family.
3. Search for a compact symbolic invariant that covers the complement without using post-replay fields.
4. If a complement class cannot be closed, output the smallest witness branch and its exact missing coordinate.
5. Keep the proof boundary explicit: branch extinction is not a global Collatz proof.

Required output:
- data/open-problem/ticket66-complement-cover-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite bridge is supplied
```

## Latest Continuation After TICKET-64

TICKET-64 supersedes the immediate TICKET-63 continuation target. It does not solve Collatz, but it is a useful negative result: the direct promotion from the TICKET63 finite automaton table to a simple symbolic transition theorem fails at the next 64-bit audit.

Known Collatz result:

```text
60-bit parent rows: 209
64-bit candidate children: 3,344
64-bit start-template children: 42
64-bit non-start children: 3,302
state20 gate collision groups: 42
state20+top4 gate collision groups: 24
64-bit admitted transition labels: 0->1:20, 0->2:11, 0->3:5, 0->5:3, 0->4:3
first admitted-child quotient separator: low40_mod_2^16_plus_base_mod16
```

Interpretation:

```text
TICKET-63 suggested a finite automaton-cover route. TICKET-64 tests the missing symbolic gate. The retained quotient state low40 mod 2^20 + base_mod16 cannot decide which 64-bit children remain in the start-template cover. The admitted children also refute the optimistic 0->0 transition continuation. The next theorem must include both an admissibility gate predicate and an offset-transition relation.
```

Do not claim Collatz from this. It is neither a Collatz proof nor a Collatz counterexample. It is a concrete obstruction to an over-simple proof route and a sharper specification for the next theorem.

Current best continuation:

```text
CO-TICKET-65 SymbolicStartTemplateGateAndOffsetTransition
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-64. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: The TICKET63 finite automaton table cannot be promoted directly. TICKET64 extends 209 retained 60-bit rows to 3,344 candidate 64-bit children. Only 42 are start-template children. The state low40 mod 2^20 + base_mod16 has 42 gate collision groups, and even state20+top4 has 24 gate collision groups. Among admitted 64-bit children, transition labels split into 0->1, 0->2, 0->3, 0->4, and 0->5, so the optimistic 0->0 formula is refuted.

Goal: build CO-TICKET-65. Derive a symbolic start-template gate and offset-transition relation, or find the first refined-state collision.

Tasks:
1. Define candidate gate states that include the minimum necessary coordinates beyond low40 mod 2^20 + base_mod16.
2. Test whether the gate state deterministically selects start-template children across 64-bit candidate children.
3. Separately test whether admitted children have deterministic offset-transition labels under a refined state.
4. If a deterministic state is found, state the symbolic gate theorem and the symbolic offset-transition theorem separately.
5. If no deterministic state is found, output the smallest collision examples and the exact coordinate that failed.

Required discipline:
- Do not treat finite deterministic rows as proof.
- Do not use post-replay fields as gate keys.
- A gate collision refutes only the proposed abstraction, not Collatz.
- A proof needs an infinite symbolic gate, a closed offset-transition relation, and a well-founded cycle exclusion argument.

Required output:
- data/open-problem/ticket65-start-template-chain-extinction-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the infinite bridge is supplied
```

## Latest Continuation After TICKET-63

TICKET-63 supersedes the immediate TICKET-62 continuation target. It still does not solve Collatz or any of the other three open problems, but it turns the bounded mod16 lift-survival signal into an explicit finite automaton-table audit and a sharper symbolic theorem target.

Known Collatz result:

```text
base mixed cylinders: 58
base mixed start-template lifts: 210
56-bit parent survivor rows: 824
60-bit chain tested lifts: 13,184
60-bit start-template chain lifts: 209
60-bit automaton states: 145
automaton collision audits: 0
full-period escapes: 0
first 60-bit quotient separator: low40_mod_2^20_plus_base_mod16
```

Interpretation:

```text
TICKET-62 showed that low40 + base high_extension mod 16 remains deterministic on selected 52/56-bit surviving lifts. TICKET-63 extracts the corresponding state tables, chains the 56-bit survivors one targeted step to 60 bits, and finds that the 60-bit chained rows are deterministic only after retaining low40 mod 2^20 together with base_mod16. This is a finite quotient/automaton audit, not a proof.
```

Do not claim Collatz from this. The result narrows the next proof obligation: replace the finite state table with a symbolic transition theorem for all admissible lifts, or find the first lift/cylinder collision that breaks the proposed automaton cover.

Current best continuation:

```text
CO-TICKET-64 SymbolicMod16AutomatonTransitionProof
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-63. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-63 extracts finite deterministic state tables from the Collatz mod16 route. The selected 56-bit survivor population has 824 rows. A targeted 60-bit chain audit tests 13,184 chain lifts and keeps 209 start-template target rows. No automaton collision audit and no full-period escape is found. The first deterministic quotient separator for the chained 60-bit rows is low40 mod 2^20 + base_mod16.

Goal: build CO-TICKET-64. Replace the finite table with a symbolic transition theorem, or break it with a concrete collision.

Tasks:
1. Define the exact symbolic state: base_mod16, low40 mod 2^20, template id, edge index, valuation gate, and any necessary affine-boundary residue.
2. Derive the transition formula algebraically from the accelerated Collatz map and the start-template constraints.
3. Prove closure for every admissible higher lift, not just the sampled 60-bit rows, or exhibit two admissible lifts with the same symbolic state and conflicting transition labels.
4. If closure holds, build a counted automaton cover and a rank/energy rule that forbids full-period nondecreasing cycles.
5. If closure fails, record the exact residues, lift bits, replay certificate, violated state equality, and conflicting labels.

Required discipline:
- Do not use failure_offset, observed outcome, or first_failure certificate fields as separator keys.
- Treat deterministic finite tables as theorem targets, not as proof.
- A collision in the automaton theorem is useful even if it is not a Collatz counterexample.
- A Collatz proof requires an independently checkable infinite argument or a formally accepted theorem, not just bounded computation.

Required output:
- data/open-problem/ticket64-symbolic-mod16-transition-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless the symbolic infinite bridge is supplied
```

## Latest Continuation After TICKET-62

TICKET-62 supersedes the immediate TICKET-61 continuation target. It does not solve Collatz, but it upgrades the mod16 separator from a 48-bit separator into a bounded higher-lift transition candidate.

Known Collatz result:

```text
base mixed cylinders: 58
base mixed start-template lifts: 210
52-bit tested lifts: 3,360
52-bit start-template lifts: 55
52-bit mod16 failure collisions: 0
56-bit tested lifts: 53,760
56-bit start-template lifts: 824
56-bit mod16 failure collisions: 0
full-period escapes: 0
first joint deterministic separator: low40_plus_base_mod16
```

Interpretation:

```text
TICKET-61 found that low40 + high_extension mod 16 predicts failure_offset on the selected 48-bit mixed-cylinder population. TICKET-62 lifts those rows to 52 and 56 bits and finds that low40 + base high_extension mod 16 remains deterministic for failure_offset, observed outcome, boundary prediction label, and transition label among all surviving start-template lifts.
```

Do not claim Collatz from this. The result is a bounded lift-transition audit. The next theorem must either build a finite automaton cover whose transition table can be proved symbolically, or find the first higher lift where the mod16 state collides.

Current best continuation:

```text
CO-TICKET-63 Mod16AutomatonCoverOrLiftCollision
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-62. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-62 lifts the selected Collatz mixed 48-bit start-template rows to 52 and 56 bits. The mod16 coordinate low40 + base high_extension mod 16 remains deterministic for failure_offset, outcome, boundary prediction label, and transition label on the surviving start-template lifts: 55 rows at 52 bits and 824 rows at 56 bits. No full-period replay is found.

Goal: build CO-TICKET-63. Convert bounded mod16 survival into either an automaton-cover theorem target or a lift-collision obstruction.

Tasks:
1. Extract the actual transition table from low40+base_mod16 state to failure_offset/outcome/transition labels.
2. Minimize the state table: determine whether low40 can be quotient-reduced by residue classes, certificate prefix length, or affine boundary state without introducing collisions.
3. Prove or refute closure one layer beyond the current audit. Acceptable bounded extensions include 60-bit targeted enumeration, symbolic congruence constraints, or a counted sampler with exact rejection conditions.
4. If a collision appears, record the two residues, their shared pre-replay state, and the conflicting labels.
5. If no collision appears, state the exact finite automaton theorem needed: state set, transition relation, acceptance/terminal cover, and the rank that forbids full-period nondecreasing cycles.

Required discipline:
- Do not use failure_offset or first_failure data as a separator key.
- Treat bounded survival as theorem-target evidence, not proof.
- Do not call a finite automaton a proof until every future lift transition is symbolically covered.
- A counterexample to the mod16 theorem is not a Collatz counterexample unless it yields a full-period nondecreasing orbit.

Required output:
- data/open-problem/ticket63-mod16-automaton-cover-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless an infinite bridge is supplied
```

## Latest Continuation After TICKET-61

TICKET-61 supersedes the replay-derived separator route from TICKET-60.

Known Collatz result:

```text
selected low40 cylinders: 162
selected start-template lifts: 535
mixed cylinders: 58
mixed start-template lifts: 210
low40-only failure-offset collisions: 58 groups / 210 ambiguous rows
low40 + certificate_prefix_length: 36 groups / 81 ambiguous rows
first pre-replay joint separator: low40_plus_high_extension_mod_2^4
first top-bit joint separator: low40_plus_high_extension_top_6_bits
proof status: open
```

Interpretation:

```text
TICKET-60 found low40 + failure_offset as a separator, but failure_offset is known only after replay. TICKET-61 forbids replay-derived keys and shows that low40 + high_extension mod 16 already predicts failure_offset, observed outcome, and boundary prediction label on the selected mixed-cylinder population.
```

Do not claim Collatz from this. The result is finite and selected. The next theorem must prove that the mod-16 high-extension coordinate has a symbolic transition law under lifts, or find a new lift/cylinder where mod16 separation fails.

Current best continuation:

```text
CO-TICKET-62 Mod16FailureOffsetTransitionOrAutomatonCountedCover
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-61. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: In the selected Collatz low40-to-48 cylinder cover, 58 low40 cylinders remain mixed and contain 210 start-template lifts. TICKET-60 separated them with low40 + failure_offset, but that was replay-derived. TICKET-61 forbids replay-derived separator keys and finds that low40 + high_extension mod 16 is the first pre-replay joint deterministic separator for failure_offset, observed outcome, and boundary prediction label.

Goal: build CO-TICKET-62. Derive the mod-16 high-extension transition table symbolically. Prove one of the following, or produce a concrete obstruction:
1. The mod-16 separator is closed under the relevant lift transitions for the selected cylinder family.
2. The selected family embeds into a counted automaton cover with no full-period nondecreasing cycle.
3. A newly lifted cylinder or larger selected cover violates mod16 determinism and becomes the next counterexample target.

Required discipline:
- Do not use failure_offset, failure_observed, or first_failure certificate data as separator keys.
- Treat finite deterministic separation as theorem-target evidence, not as proof.
- State the exact quantified theorem before claiming progress.
- If a counterexample is proposed, provide the residue/cylinder, replay certificate, and the violated separator condition.

Required output:
- data/open-problem/ticket62-mod16-transition-cover-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no conjecture is solved unless a symbolic infinite bridge is supplied
```

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

## Latest Continuation After TICKET-52

TICKET-52 supersedes the TICKET-51 continuation target. It confirms that TICKET-51 was an ancestry-local closure, not a 48-bit theorem.

Exact result:

```text
48-bit debt-valid valuation words: 83,401,400,116
64-bit debt-valid valuation words: 2,216,134,944,775,156
deterministic sample seed: 20,260,709
sample count: 200,000
verified open sample words: 100,026
start-template sample matches: 3,184
sampled depth-15 roots: 1
new root: 171308122831719
32-bit projection: 3352230759
projection template: [0,[1,2,1,1],103,2]
terminal step: 15
terminal mismatch counts: {tail_word+next_valuation: 2}
final surviving states: 0
full lasso completions: 0
```

Do not promote TICKET-51 or TICKET-52 into a Collatz proof. TICKET-52 found and closed one sampled 48-bit near-lasso witness, but the sampler is not exhaustive. The key lesson is that the old valuation-word enumeration is no longer a viable main proof route at 48 bits.

Current best Collatz continuation:

```text
CO-TICKET-53 Symbolic48BitFrontierCoverageOrFullLassoReplay
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-52. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-52 quantified the Collatz 48-bit frontier at 83,401,400,116 debt-valid valuation words and the 64-bit frontier at 2,216,134,944,775,156 words. A deterministic 200,000-word sampler found one new 48-bit depth-15 near-lasso root, 171308122831719, whose 32-bit projection has template [0,[1,2,1,1],103,2], outside the TICKET51 closed ancestry. A base-48 terminal lift audit closes this sampled root at phase 15 with tail_word+next_valuation mismatch and no full lasso completion.

Goal: build CO-TICKET-53. Do not merely increase the random sample. Construct a symbolic coverage engine for the 48-bit start-template frontier. Acceptable routes include an automaton-counting DP, SAT/SMT encoding of valuation-word constraints, exact modular affine constraint solving, or a theorem proving that every depth-15 terminal branch must shift tail/next_valuation. If a full lasso completion is found, replay it for multiple periods and state the exact infinite periodicity theorem still required.

Required output:
- data/open-problem/ticket53-symbolic-frontier-coverage-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless an infinite replay theorem is supplied
```

## Latest Continuation After TICKET-56

TICKET-56 supersedes the TICKET-55 continuation target. It keeps the TICKET55 gate tunnel, closes the exact 32-bit extracted lasso route as a finite partition, and rejects simple projection closure as a global proof route.

Current strongest Collatz result:

```text
local theorem: Exact32StartTemplateLassoPartition
exact 32-bit start-template matches: 69,092
pre-gate first failures: 69,090
failure offsets: 1 -> 34,458; 2 -> 17,301; 3 -> 8,649; 4 -> 4,310; 5 -> 4,372
all pre-gate failures are next-valuation mismatch: true
phase-5 failure next_valuation=10 count: 0
gate crossers: 2
gate crossers terminally closed by TICKET55: 2
partition complete for exact32 start-template: true
projection closure: refuted by sampled 48-bit depth-15 witness
escape witness: 171,308,122,831,719
escape projection32 template: [0,[1,2,1,1],103,2]
```

Discarded route:

```text
Do not try to prove Collatz by partitioning only the exact 32-bit start-template population and assuming every higher-bit start-template root projects back into that same 32-bit template. TICKET56 records a sampled 48-bit witness that violates this projection-closure shortcut.
```

Retained route:

```text
CO-TICKET-57 ParametricTemplateAutomatonOrEscapeCycle
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-56. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-56 closes the exact 32-bit extracted Collatz lasso route as a finite partition. The exact 32-bit start-template population has 69,092 matches. Of these, 69,090 fail at offsets 1-5 by next-valuation mismatch, and the remaining 2 phase-5 gate crossers are terminally closed by TICKET55. However, TICKET56 also refutes simple projection closure: the sampled 48-bit depth-15 witness 171308122831719 projects to 32-bit template [0,[1,2,1,1],103,2], outside the exact32 start-template model. Therefore a fixed 32-bit partition cannot be promoted to a global proof by projection.

Goal: build CO-TICKET-57. Construct a parametric template-state automaton over base modulus, phase, tail word, residue class, and pending valuation, or find a higher-bit escape cycle that avoids all known terminal no-go tunnels. Do not resample the TICKET53/TICKET55 closed routes. Do not treat exact32 closure as a proof. The useful output is either (a) a formal candidate theorem with a well-founded rank over all template lifts, or (b) a replayable escape witness that survives at least one full lasso period and is not covered by TICKET53/TICKET55/TICKET56.

Required artifacts:
- data/open-problem/ticket57-parametric-template-automaton-lab.json
- data/open-problem/collatz/co-ticket-57-parametric-template-automaton.json
- updated docs/proof-or-counterexample-program.md
- updated GitHub Pages card
```

## Latest Continuation After TICKET-57

TICKET-57 supersedes the TICKET-56 continuation target. It does not solve Collatz, but it rejects another weak globalization route: a finite template quotient is too coarse unless the boundary coordinates that determine the finite partition are included and then proved stable under lifts.

```text
local theorem target: AffineBoundaryTemplateStateOrEscapeCycle
exact 32-bit start-template matches: 69,092
template-only coarse outcomes in one state: 6
template + prefix_length + residue mod 2^26 collision groups: 92
first deterministic exact32 boundary: template + prefix_length + residue mod 2^28
projection escape witness carried forward: 171,308,122,831,719
escape projection32 template: [0,[1,2,1,1],103,2]
known near-lasso roots replayed: 3
maximum replayed prefix depth: 15
full lasso period replays: 0
cycle status: no_known_root_replays_full_lasso_period
```

Current best Collatz continuation:

```text
CO-TICKET-58 AffineBoundaryLiftStabilityOrFullPeriodEscape
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-57. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-57 shows that the exact32 Collatz lasso partition is not governed by the extracted template alone. The template-only abstraction has 6 coarse outcomes, and even template + prefix_length + residue mod 2^26 leaves 92 collision groups. The first deterministic exact32 boundary in the audited ladder is template + prefix_length + residue mod 2^28. The sampled 48-bit depth-15 witness 171308122831719 still projects outside the exact32 start template, and none of the 3 known near-lasso roots replays a full lasso period.

Goal: build CO-TICKET-58. Do not resample known terminal routes. Prove or falsify lift stability of the first deterministic affine-boundary state. Acceptable success outcomes are: (a) a machine-checkable transition relation showing that the exact32 deterministic boundary lifts to 40/48-bit cylinders with a well-founded decreasing rank, or (b) a full-period higher-bit escape witness whose affine boundary state returns after one lasso period with nondecreasing rank and is not covered by TICKET53/TICKET55/TICKET56/TICKET57.

Required artifacts:
- data/open-problem/ticket58-affine-boundary-lift-lab.json
- data/open-problem/collatz/co-ticket-58-affine-boundary-lift.json
- per-problem transfer artifacts for RH, Goldbach, Twin Prime
- updated docs/proof-or-counterexample-program.md
- updated GitHub Pages card
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the result covers all trajectories or supplies a genuine replayable counterexample
```

## Latest Continuation After TICKET-60

TICKET-60 supersedes the TICKET-59 continuation target. It does not solve Collatz, but it identifies the first tested separator for the mixed low40 cylinders: `low40 + failure_offset`.

```text
selected low40 cylinders: 162
selected start-template lifts: 535
mixed cylinders: 58
mixed start-template lifts: 210
low40-only mixed outcome collisions: 58 groups / 210 ambiguous rows
low40 + certificate_prefix_length: 36 outcome collision groups / 81 ambiguous rows
first joint deterministic separator: low40_plus_failure_offset
first high-extension low-bit separator: high_extension mod 2^4
first high-extension top-bit separator: top 6 bits
```

Current best Collatz continuation:

```text
CO-TICKET-61 SymbolicFailureOffsetPredictorOrCountedCover
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-60. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-60 analyzes the 58 mixed low40 cylinders left by TICKET-59. The selected population has 162 low40 cylinders and 535 start-template lifts; the mixed cylinders contain 210 lifts. low40 alone leaves every mixed cylinder ambiguous. low40 plus certificate_prefix_length still leaves 36 outcome collision groups and 81 ambiguous rows. The first tested joint deterministic separator is low40_plus_failure_offset. This separates outcome and boundary-match status on the selected population, but failure_offset is replay-derived and therefore not yet a non-circular proof coordinate.

Goal: build CO-TICKET-61. Replace the replay-derived failure_offset separator with a symbolic predictor or an automaton-counted cover. Acceptable success outcomes are: (a) a symbolic transition theorem predicting failure_offset from pre-replay coordinates, (b) an automaton-counted cover that classifies a larger cylinder family without using replay-derived failure labels, or (c) a full-period affine-boundary escape witness with a replayable nondecreasing cycle.

Required artifacts:
- data/open-problem/ticket61-symbolic-failure-offset-lab.json
- data/open-problem/collatz/co-ticket-61-symbolic-failure-offset.json
- per-problem transfer artifacts for RH, Goldbach, Twin Prime
- updated docs/proof-or-counterexample-program.md
- updated GitHub Pages card
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the result covers all trajectories or supplies a genuine replayable counterexample
```

## Latest Continuation After TICKET-59

TICKET-59 supersedes the TICKET-58 continuation target. It does not solve Collatz, but it upgrades the TICKET58 point mismatch into exact selected low40-to-48 cylinder facts and exposes the next missing coordinate.

```text
selected low40 cylinders: 162
tested 48-bit extensions: 41,472
48-bit start-template lifts: 535
projection escapes inside selected cylinders: 207
projection-target lifts inside selected cylinders: 328
boundary prediction mismatches: 224
boundary prediction matches: 104
mismatch-seed cylinders: 70
uniform mismatch cylinders: 35
mixed/unstable cylinders: 58
full lasso period escapes: 0
```

Current best Collatz continuation:

```text
CO-TICKET-60 MixedCylinderSeparatorOrAutomatonCountedCover
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-59. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-59 takes the TICKET58 deterministic replay and groups every boundary-mismatch and boundary-match seed into low40 cylinders, then enumerates all 256 possible 48-bit extensions for each selected cylinder. Across 162 selected low40 cylinders, 41,472 extensions are tested. The selected cylinders contain 535 48-bit start-template lifts, 207 projection escapes, 328 projection-target lifts, 224 boundary mismatches, and 104 boundary matches. Of 70 mismatch-seed cylinders, 35 are uniform mismatch cylinders, but 58 selected cylinders are mixed/unstable. No full-period lasso replay is found. Therefore low40 is a stronger finite coordinate than a point sample, but it is not sufficient for a proof.

Goal: build CO-TICKET-60. Find the missing coordinate that separates the mixed low40 cylinders, or replace selected-cylinder enumeration with an automaton-counted cover. Acceptable success outcomes are: (a) a symbolic separator that makes every selected mixed cylinder deterministic and names the coordinate needed for a theorem, (b) an automaton-counted cover that classifies a larger cylinder family without blind enumeration, or (c) a full-period affine-boundary escape witness with a replayable nondecreasing cycle.

Required artifacts:
- data/open-problem/ticket60-mixed-cylinder-separator-lab.json
- data/open-problem/collatz/co-ticket-60-mixed-cylinder-separator.json
- per-problem transfer artifacts for RH, Goldbach, Twin Prime
- updated docs/proof-or-counterexample-program.md
- updated GitHub Pages card
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the result covers all trajectories or supplies a genuine replayable counterexample
```

## Latest Continuation After TICKET-58

TICKET-58 supersedes the TICKET-57 continuation target. It does not solve Collatz, but it refutes the next weak proof route: the first deterministic exact32 affine boundary does not lift unchanged to the replayed 48-bit sample.

```text
local theorem target: AffineBoundaryLiftStabilityOrFullPeriodEscape
exact32 boundary width: 28 low bits
exact32 boundary states: 69,092
exact32 boundary collisions: 0
48-bit replayed sample count: 200,000
48-bit start-template matches: 3,184
projection escapes: 3,086
projection-target lifts: 98
boundary prediction matches: 28
boundary prediction mismatches: 70
projection-target prediction rate: 28.57%
full lasso period replays: 0
lift-stability status: refuted_by_sampled_boundary_prediction_mismatch
```

Current best Collatz continuation:

```text
CO-TICKET-59 SymbolicLiftMismatchCylinderOrCounted40BitCover
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-58. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-58 replays the deterministic TICKET52 48-bit sample against the first deterministic exact32 affine boundary from TICKET57. Among 3,184 sampled 48-bit start-template matches, 3,086 project outside the exact32 target. Only 98 project into the exact32 target, and 70 of those disagree with the exact32 boundary-predicted outcome. No sampled root replays a full lasso period. Therefore the shortcut "exact32 deterministic boundary lifts unchanged" is refuted in the sample, but this is not a Collatz proof or counterexample.

Goal: build CO-TICKET-59. Promote the sampled lift mismatch into a symbolic cylinder theorem or replace sample replay with a counted 40-bit/48-bit boundary cover. Acceptable success outcomes are: (a) a symbolic description of all projection escapes and lift mismatches for a nontrivial cylinder family, (b) a counted finite cover that proves every 40-bit start-template lift is classified by projection escape, outcome mismatch, or terminal tunnel, or (c) a full-period affine-boundary escape witness with a replayable nondecreasing cycle.

Required artifacts:
- data/open-problem/ticket59-symbolic-lift-mismatch-lab.json
- data/open-problem/collatz/co-ticket-59-symbolic-lift-mismatch.json
- per-problem transfer artifacts for RH, Goldbach, Twin Prime
- updated docs/proof-or-counterexample-program.md
- updated GitHub Pages card
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the result covers all trajectories or supplies a genuine replayable counterexample
```

## Latest Continuation After TICKET-55

TICKET-55 supersedes the TICKET-54 continuation target for the current extracted low-lift Collatz family. It does not solve Collatz, but it closes the known phase-5 gate-crossing route into the TICKET53 terminal no-go.

```text
local theorem: Phase5GateToTerminalTunnel
checked gate-crossing roots: 3
gate matches: 3
tunnel matches through phases 5-14: 3
same pending certificate through tunnel: 3
terminal target matches: 0
exact 32-bit starts failed before or at phase 5: 69,090
exact 32-bit gate crossers: 2
exact 32-bit gate crossers terminally closed: 2
```

Current best Collatz continuation:

```text
CO-TICKET-56 PreGateResidueClosureOrTemplateModelEscape
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-55. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-55 proves a local gate-to-terminal tunnel for the extracted low-lift Collatz family. If a root reaches the phase-5 gate [5,[1,1,1,1],103,10] with consumed_bits = b+5, the pending valuation 10 remains unconsumed through phases 6-14 and then is consumed at phase 15, where the TICKET53 terminal no-go applies. The exact 32-bit start-template population is closed with respect to this extracted lasso route: 69,090 starts fail before or at phase 5, and the 2 gate crossers are terminally closed. This is not a Collatz proof because it does not cover every base modulus, every trajectory, or every template family.

Goal: build CO-TICKET-56. Do not resample the TICKET53 terminal family or the already closed phase-5 gate crossers. Attack the remaining pre-gate failure population or escape the current low-lift start-template model. Acceptable routes: derive a residue-class theorem that explains why the 69,090 exact 32-bit starts fail before/at phase 5; construct a parametric theorem for all base moduli; or find a root outside the current low-lift template model that crosses a finite gate and avoids every known terminal no-go tunnel.

Required output:
- data/open-problem/ticket56-pre-gate-projection-escape-lab.json
- data/open-problem/collatz/co-ticket-56-pre-gate-projection-escape.json
- per-problem transfer artifacts for RH, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the result covers all trajectories or supplies a genuine replayable counterexample
```

## Latest Continuation After TICKET-54

TICKET-54 supersedes the TICKET-53 continuation target. The TICKET-53 phase-15 terminal family is locally refuted and should no longer consume random-sampling budget. TICKET-54 removes that family and extracts the next bounded Collatz target:

```text
new family: Phase5ValuationGate
exact 32-bit start-template matches: 69,092
discarded TICKET-53 depth-15 roots: 2
remaining exact starts: 69,090
post-discard max exact depth: 5
phase-5 gate exact roots: 4,372
phase-5 failures with observed next_valuation=10: 0
48-bit deterministic sample post-discard max depth: 5
48-bit deterministic sample phase-5 gate roots: 175
```

Current best Collatz continuation:

```text
CO-TICKET-55 Phase5ValuationGateTheoremOrCounterexample
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-54. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-53 locally refutes the extracted phase-15 Collatz lasso family. TICKET-54 removes that family and re-audits the remaining exact 32-bit start-template frontier. After removing the two discarded depth-15 roots, 69,090 exact 32-bit starts remain and the maximum remaining lasso-prefix depth drops to 5. The strongest remaining bounded family is Phase5ValuationGate: 4,372 exact 32-bit roots stop at the phase-5 next_valuation=10 gate, and none of those phase-5 failures has observed next_valuation=10. The 48-bit deterministic sample agrees at the level of post-discard max depth 5 and 175 phase-5 gate samples.

Goal: build CO-TICKET-55. Do not resample the TICKET53 terminal family. Attack Phase5ValuationGate directly. Either prove an all-lift theorem saying every remaining phase-compatible start that reaches the first five lasso templates closes, enters the discarded terminal family, or fails next_valuation=10 at phase 5; or produce a concrete root outside the discarded family that reaches phase 5 with next_valuation=10 and survives into a different replayable lasso template.

Required output:
- data/open-problem/ticket55-phase5-valuation-gate-lab.json
- per-problem transfer artifacts for RH, Collatz, Goldbach, Twin Prime
- docs/proof-or-counterexample-program.md update
- GitHub Pages card update
- explicit proof boundary saying no Collatz proof and no Collatz counterexample unless the all-lift theorem or a genuine replayable counterexample is supplied
```

## Latest Continuation After TICKET-53

TICKET-53 supersedes the TICKET-52 continuation target for the specific extracted phase-15 lasso family. It does not cover every possible Collatz template, but it explains why all currently known near-lasso witnesses in this family close terminally.

Exact result:

```text
theorem: Phase15TerminalMismatchForExtractedLasso
checked roots:
  1471663463 at base bits 32
  3206130791 at base bits 32
  171308122831719 at base bits 48
all checked roots satisfy parent premise: true
terminal target matches: 0
low branch terminal mechanism: pending valuation 10 is consumed and enters the tail
high branch terminal mechanism: boundary shift 3^m * 2^9 forces next valuation 9
```

Do not keep sampling or relifting this same phase-15 lasso family as a counterexample route. The family is locally refuted. This is not a Collatz proof because it does not cover different lasso templates or all trajectories.

Current best Collatz continuation:

```text
CO-TICKET-54 NewTemplateFamilyExtractionOrGlobalDescentInvariant
```

Prompt for the next LLM:

```text
You are continuing PrimeProject after TICKET-53. The project is trying to solve or refute RH, Collatz, Goldbach, and Twin Prime, but must not claim a proof without an independently checkable infinite argument.

Known result: TICKET-53 proves a local no-go theorem for the extracted Collatz phase-15 lasso family. If a phase-14 parent has template [14,[1,1,1,1],103,10] and consumed bits b+5, the low terminal branch must consume the pending valuation 10, causing a tail mismatch, and the high terminal branch must force next valuation 9 after the boundary shift 3^m * 2^9. Therefore the phase-15 target [15,[1,1,1,1],103,10] cannot be reached by either terminal branch. This refutes the current lasso family as a counterexample route but does not prove Collatz.

Goal: build CO-TICKET-54. Do not resample the discarded lasso family. Extract new lasso-template families from the frontier graph, or build a global descent invariant that does not depend on the discarded phase-15 family. For every new family, first state the terminal/no-go theorem it must evade. If a family survives, produce a replayable witness and state the exact infinite theorem still required.

Required output:
- data/open-problem/ticket54-new-template-family-lab.json
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
