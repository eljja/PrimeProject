# Proof-or-Counterexample Program

Date: 2026-07-04

This document records the next PrimeProject research posture for the four open problems. A proof attempt is not limited to proving the conjecture directly. It can also:

1. find a direct counterexample;
2. prove the contrapositive;
3. prove that no counterexample can exist;
4. falsify weak proof routes before they waste formalization time.

한국어 요약: 증명은 정면 증명만이 아니다. 반례 하나를 찾으면 추측은 끝나고, 대우법으로 반례가 불가능함을 보이면 증명이 된다. 그래서 PrimeProject는 이제 "증명 후보를 만들고 바로 반례로 부수는" 방식으로 네 난제에 접근한다.

## Executable Artifact

The current executable lab is:

```text
scripts/proof_or_counterexample_lab.py
```

It writes:

```text
data/open-problem/proof-or-counterexample-lab.json
data/open-problem/riemann/rh-ticket-16-proof-or-counterexample.json
data/open-problem/collatz/co-ticket-16-proof-or-counterexample.json
data/open-problem/goldbach/gb-ticket-16-proof-or-counterexample.json
data/open-problem/twin-prime/tp-ticket-16-proof-or-counterexample.json
```

Current status:

```text
attempted_no_full_resolution
```

This is deliberate. A bounded computation can find a counterexample, but a bounded computation cannot prove these universal or infinitude statements by itself.

## Result Summary

### Riemann Hypothesis

Direct RH counterexample search was not attempted in this lab because certified zeta-zero isolation requires a dedicated analytic/numeric verifier.

What was attempted instead:

```text
candidate theorem counterexample
finite-prefix obstruction
contrapositive zero-exclusion route
```

The lab constructs a symmetric surrogate zero model containing an off-critical quartet. The first 80 Li-type coefficients in this surrogate stay nonnegative in the current run. This does not disprove RH. It shows that a finite Li/Jensen/Hermite prefix is not a proof route unless it is upgraded to a uniform all-index theorem.

Next theorem:

```text
RH-TICKET-17 UniformOffCriticalDetector
```

Required breakthrough:

```text
Assume an off-critical zero exists. Construct a Li-type coefficient, kernel, or explicit-formula test functional that becomes negative, uniformly over all heights and all off-critical displacements.
```

한국어 설명: 리만가설은 유한 개의 zero나 유한 개의 Li 계수 확인으로 끝나지 않는다. 반례 방향으로 가려면 "critical line 밖 zero가 있으면 반드시 감지되는 전역 검출기"가 필요하다.

### Collatz Conjecture

Direct search:

```text
starts checked: 100,000
direct counterexample found: no
max steps seen: n = 77,031, steps = 350
```

Candidate proof route falsified:

```text
Every odd accelerated Collatz step descends immediately.
```

This is false. For example, `3 -> 5`, `7 -> 11`, `11 -> 17` under the accelerated odd map. Therefore a one-step descent proof cannot work.

Next theorem:

```text
CO-TICKET-17 ResidueDebtAutomatonLift
```

Required breakthrough:

```text
Build a residue-debt automaton whose rank may temporarily increase but must decrease over every closed or escaping block, then prove that the finite automaton lifts to all integers.
```

한국어 설명: Collatz는 네 문제 중 가장 CEGIS에 잘 맞는다. 직접 반례가 없더라도, 약한 descent 주장은 곧바로 깨진다. 따라서 "한 번에 감소"가 아니라 "debt를 기록하고 블록 단위로 감소"하는 rank가 필요하다.

### Goldbach Conjecture

Direct search:

```text
even n <= 100,000 checked
direct counterexample found: no
```

Candidate proof route stressed:

```text
A uniform lower bound can ignore residue-profile worst cases.
```

This is too weak. The lab identifies hardest even numbers by representation count and normalized margin. These are not Goldbach counterexamples; they are counterexamples to careless lower-bound arguments.

Next theorem:

```text
GB-TICKET-17 ResidueProfileExplicitCutoff
```

Required breakthrough:

```text
For each residue profile, prove an explicit representation-count lower bound whose cutoff lies below the finite verification range.
```

한국어 설명: 골드바흐는 반례 탐색 자체보다 "가장 위험한 짝수 profile"을 찾는 것이 중요하다. 그래야 해석적 lower bound의 상수 손실을 어디서 줄여야 하는지 보인다.

### Twin Prime Conjecture

Finite direct refutation is not possible in the same way, because the negation is eventual:

```text
there exists N such that no twin primes occur after N
```

The lab found:

```text
twin pairs up to 200,000: 2,160
```

Candidate proof route falsified:

```text
bounded gaps imply exact gap 2
```

The gap distribution contains many wider bounded gaps. In the current run, bounded-gap mass up to gap 40 is dominated by wider gaps, so any proof that converts bounded gaps to twin primes without an exact gap-2 projection is invalid.

Next theorem:

```text
TP-TICKET-17 ExactGapTwoProjection
```

Required breakthrough:

```text
Construct a parity-barrier-resistant lower bound for exact gap 2, not merely for some bounded gap.
```

한국어 설명: 쌍둥이 소수에서 가장 위험한 착각은 bounded gap을 gap 2로 바꾸는 것이다. 이 변환은 자동으로 되지 않는다. exact gap-2 mass를 따로 분리하는 정리가 필요하다.

## Unified Method

For every future candidate theorem, PrimeProject should store:

```json
{
  "direct_counterexample": {},
  "candidate_counterexamples_found": {},
  "contrapositive_route": "...",
  "missing_infinite_bridge": "...",
  "next_theorem_to_attempt": "...",
  "claim_boundary": "not a proof"
}
```

Promotion rule:

```text
A candidate can move toward proof status only if:
1. direct counterexample search finds no counterexample in the committed range;
2. candidate-theorem counterexample search does not falsify the route;
3. the contrapositive or infinite bridge is stated exactly;
4. no finite-only, heuristic independence, or target-equivalent axiom is used;
5. the bridge is formalized or accepted as an external theorem.
```

## Current Priority

The strongest next move is:

```text
CO-TICKET-17 ResidueDebtAutomatonLift
```

Reason:

```text
Collatz failures produce concrete residue states, transitions, and SCCs. This gives AI a real counterexample-guided loop rather than only vague analytic pressure.
```

The second priority is:

```text
GB-TICKET-17 ResidueProfileExplicitCutoff
```

Reason:

```text
Goldbach has a clear finite-plus-infinite proof architecture: finite verification below N0 and explicit lower bound above N0.
```

The third priority is:

```text
TP-TICKET-17 ExactGapTwoProjection
```

The fourth priority is:

```text
RH-TICKET-17 UniformOffCriticalDetector
```

## Ticket 17 Breakthrough Attempt Results

Generated artifact:

```text
data/open-problem/ticket17-breakthrough-attempts.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-17-uniform-offcritical-detector.json
data/open-problem/collatz/co-ticket-17-residue-debt-automaton-lift.json
data/open-problem/goldbach/gb-ticket-17-residue-profile-explicit-cutoff.json
data/open-problem/twin-prime/tp-ticket-17-exact-gap-two-projection.json
```

Current verdict:

```text
breakthrough_attempts_open_no_resolution
```

한국어 요약: TICKET-17은 네 난제를 풀었다고 주장하지 않는다. 대신 각 문제의 다음 무한다리 정리를 더 날카롭게 만들었다.

1. RH: finite Li-type detector가 off-critical surrogate를 충분히 빨리 잡는지 실험했다. 현재 결과는 finite detector만으로는 부족하며, 전역 effective detector theorem이 필요하다는 쪽이다.
2. Collatz: accelerated odd trajectory의 residue-debt를 추적했다. 표본상 하강 압력은 보이지만, residue-debt state 전체를 덮는 lifting theorem이 없다.
3. Goldbach: residue profile별 representation lower envelope를 추적했다. finite margin은 양수지만, profile별 analytic error term을 이겨야 한다.
4. Twin Prime: exact gap 2 mass와 wider bounded-gap mass를 분리했다. bounded gap 신호는 wider gap에 크게 오염되므로 exact gap projection theorem이 필요하다.

## Ticket 18 Reduction Lab Results

Generated artifact:

```text
data/open-problem/ticket18-reduction-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-18-finite-prefix-camouflage.json
data/open-problem/collatz/co-ticket-18-valuation-branch-cover.json
data/open-problem/goldbach/gb-ticket-18-explicit-error-budget.json
data/open-problem/twin-prime/tp-ticket-18-bounded-gap-countermodel.json
```

Current verdict:

```text
reduction_attempts_open_no_resolution
```

한국어 요약: TICKET-18은 네 난제를 풀었다고 주장하지 않는다. 대신 "증명처럼 보이는 단축로"를 실제 반례 모델이나 정확한 환원 계산으로 공격한다.

1. RH: high-height off-critical surrogate quartet가 finite Li-prefix에서 거의 보이지 않는 camouflage 현상을 만든다. 따라서 유한 prefix 양성만으로는 리만가설을 증명할 수 없고, height-uniform detector 또는 tail theorem이 필요하다.
2. Collatz: 샘플 궤적 대신 exact accelerated valuation word를 열거했다. 각 branch는 `T^k(n)=(3^k n+c)/2^a` 꼴의 정확한 affine map을 갖는다. 많은 branch는 수축하지만, expanding branch를 전역적으로 낮은 rank로 보내는 branch graph theorem이 아직 필요하다.
3. Goldbach: finite count를 Hardy-Littlewood scale과 residue profile별 margin으로 바꾸어 explicit analytic error budget을 산출했다. 반례는 없지만, 이 margin을 이기는 공개 상수 기반 lower-bound theorem이 없으면 증명이 아니다.
4. Twin Prime: 각 관측 twin pair의 두 번째 소수를 삭제하는 bounded-gap countermodel을 만들었다. 이 모델은 exact gap 2를 0으로 만들면서도 bounded gap 대부분을 유지한다. 따라서 bounded-gap 정리만으로 twin prime conjecture를 증명하는 경로는 차단된다.

Next decisive target:

```text
CO-TICKET-19 BranchGraphRankSearch
```

Reason:

```text
Collatz now has the most concrete finite-to-infinite bridge candidate: exact valuation branches plus a possible well-founded rank over the branch graph.
```

## Ticket 19 Proof Pressure Lab Results

Generated artifact:

```text
data/open-problem/ticket19-proof-pressure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-19-tail-uniformity-pressure.json
data/open-problem/collatz/co-ticket-19-branch-graph-rank-search.json
data/open-problem/goldbach/gb-ticket-19-local-obstruction-elimination.json
data/open-problem/twin-prime/tp-ticket-19-admissibility-vs-exact-gap.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-19는 직접 증명, 반례 탐색, 대우법 후보를 더 압박한다. 결론은 네 문제 모두 여전히 open이다.

1. RH: off-critical surrogate quartet를 height `10,000,000`까지 올리면 첫 200개 Li-type prefix에서 최대 효과가 약 `8.0004e-10`까지 작아진다. 이는 finite prefix positivity가 RH 증명이 될 수 없고 height-uniform tail theorem이 필요하다는 점을 강화한다.
2. Collatz: odd accelerated step 길이 32까지 exact valuation-word density를 계산했다. 32-step에서도 expanding word density가 약 `0.032454323536` 남고, all-ones valuation word는 모든 고정 길이에 대해 확장한다. 따라서 fixed-block contraction 증명은 실패하며 branch graph rank가 필요하다.
3. Goldbach: mod `6, 30, 210, 2310`에서 unit prime residue sum이 모든 target residue를 덮는다. 즉 테스트한 범위에서는 local modular obstruction이 없고, 남은 문제는 explicit analytic lower bound다.
4. Twin Prime: twin pattern은 prime modulus `2..47`에서 locally admissible이지만, 삭제형 countermodel은 exact gap 2를 `2994 -> 0`으로 만들면서 bounded gap의 약 `88.461835%`를 유지한다. 따라서 local admissibility와 bounded-gap 생존은 twin prime infinitude가 아니다.

Next decisive target:

```text
CO-TICKET-20 ValuationPrefixRankCEGIS
```

Reason:

```text
The strongest current path is no longer fixed-length Collatz descent. It is a counterexample-guided search for a well-founded rank over exact valuation prefixes.
```

## Ticket 20 Valuation-Prefix Lab Results

Generated artifact:

```text
data/open-problem/ticket20-valuation-prefix-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-20-uniform-tail-contract.json
data/open-problem/collatz/co-ticket-20-valuation-prefix-rank-cegis.json
data/open-problem/goldbach/gb-ticket-20-local-multiplicity-barrier.json
data/open-problem/twin-prime/tp-ticket-20-admissibility-constant-vs-deletion.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-20은 "유한 계산을 더 늘리는 방식"이 아니라, 네 난제에서 약한 증명 경로가 왜 실패하는지 더 정확한 certificate로 남긴다.

1. RH: finite Li-prefix camouflage를 uniform tail contract 문제로 바꿨다. high-height off-critical surrogate가 유한 prefix에서 약하게 보이는 현상은 유지되며, 실제 증명에는 zero height와 Li index를 동시에 제어하는 tail theorem이 필요하다.
2. Collatz: all-ones accelerated valuation prefix를 길이 64까지 정확한 residue certificate로 만들었다. 길이 64의 대표 residue는 `0x1ffffffffffffffff`, 즉 `-1 mod 2^65`이고, `T^64(n)=(3^64 n + (3^64-2^64))/2^64` branch는 asymptotic multiplier가 약 `1.86140372879e11`이다. 이것은 Collatz 반례가 아니라, fixed-length contraction 증명 경로의 강한 반례다.
3. Goldbach: mod `6, 30, 210, 2310`에서 모든 target residue가 unit prime-residue pair로 덮이며, mod `2310`에서도 최소 ordered unit-pair count가 `135`다. 따라서 이 범위에서는 local congruence obstruction이 아니라 analytic lower bound가 본질이다.
4. Twin Prime: prime modulus `2..47`의 partial singular product는 양수이고 `2C2` 근사도 양수지만, deletion model은 exact gap 2를 `2994 -> 0`으로 만든다. local constant는 필요 조건이지 무조건적 infinitude proof가 아니다.

Next decisive target:

```text
CO-TICKET-21 TwoAdicBranchExclusion
```

Reason:

```text
The all-ones branch is visibly the positive-integer shadow of the 2-adic fixed point -1. A serious Collatz route must prove how such expanding 2-adic shadows are excluded or ranked down for all positive integers.
```

## Ticket 21 Two-Adic Branch Lab Results

Generated artifact:

```text
data/open-problem/ticket21-two-adic-branch-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-21-prefix-evasion-quantifier.json
data/open-problem/collatz/co-ticket-21-two-adic-branch-exclusion.json
data/open-problem/goldbach/gb-ticket-21-witness-spectrum.json
data/open-problem/twin-prime/tp-ticket-21-deletion-persistence-ladder.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-21은 Collatz의 가장 단순한 2-adic obstruction인 all-ones branch를 좁은 의미에서 배제한다. 이것은 전체 Collatz 증명이 아니라, 하나의 무한 2-adic branch가 양의 정수 반례가 될 수 없다는 부분 결과다.

1. RH: finite Li-prefix countermodel pressure를 height별로 다시 계량했다. 결론은 동일하다. 유한 prefix 확인은 uniform tail theorem 없이는 RH 증명이 될 수 없다.
2. Collatz: 양의 홀수 `n`에 대해 `s=v2(n+1)`이면 all-ones accelerated branch를 최대 `s-1`단계만 따라갈 수 있다. 길이 128 shadow `2^129-1`도 all-ones prefix 뒤 다음 valuation에서 탈출한다. 무한 all-ones branch는 2-adic `-1`이고 양의 정수가 아니다.
3. Goldbach: 200,000 이하 직접 반례는 없고, hardest smallest-witness case는 `194470 = 383 + 194087`이다. 이 finite witness spectrum은 분석적 lower bound를 대체하지 않는다.
4. Twin Prime: deletion countermodel을 1,000,000까지 ladder로 반복했다. exact gap 2는 `8169 -> 0`이 되지만 bounded gaps는 약 `89.55%` 유지된다. bounded-gap shortcut은 계속 차단된다.

Next decisive target:

```text
CO-TICKET-22 MixedTwoAdicCylinderRank
```

Reason:

```text
The all-ones 2-adic branch is now isolated. The next useful Collatz step is to handle mixed expanding valuation cylinders and search for a rank that forces every such cylinder to escape into descent.
```

## Ticket 22 Negation Pressure Lab Results

Generated artifact:

```text
data/open-problem/ticket22-negation-pressure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-22-li-detector-horizon.json
data/open-problem/collatz/co-ticket-22-mixed-two-adic-cylinder-rank.json
data/open-problem/goldbach/gb-ticket-22-residue-deletion-obstruction.json
data/open-problem/twin-prime/tp-ticket-22-exact-gap-projection.json
```

Current verdict:

```text
negation_pressure_open_no_resolution
```

한국어 요약: TICKET-22는 네 난제를 "반례를 찾거나, 반례가 없다면 어떤 대우법/무한 정리가 필요한가"라는 관점으로 다시 공격한다. 결론은 아직 증명이나 반증이 아니다. 하지만 각 문제에서 약한 증명 전략이 어디서 깨지는지 더 분명해졌다.

1. RH: off-critical surrogate zero quartet은 결국 Li-type 계수에서 음의 신호를 만들지만, 강한 음의 신호가 나타나는 index가 테스트 범위에서 height squared 규모로 밀린다. 높이 500에서는 threshold `-1.0` 이하 신호가 index `694,274`에서 처음 보였다. 따라서 finite prefix proof는 uniform detector/tail theorem 없이는 계속 차단된다.
2. Collatz: 길이 12, valuation alphabet `{1,2,3}`에서 expanding valuation cylinder `42,502`개를 열거했고, 모두 exact 2-adic lift로 검증됐다. 비자명 positive cycle 후보는 나오지 않았고, known `1` cycle만 보였다. 이 결과는 Collatz 증명이 아니라, fixed-block descent 방식이 왜 실패하는지 보여준다.
3. Goldbach: modulus `30`, `210`, `2310`에서 unit residue sum이 모든 even residue를 덮는지 보았고, local obstruction은 없었다. `2310`에서는 가장 약한 even residue도 obstruction을 만들려면 unit residue class를 최소 `68`개 삭제해야 했다. 즉 단순 congruence obstruction으로 Goldbach 반례를 설명하기 어렵다.
4. Twin Prime: exact-gap projection을 deletion model에 적용했다. `2,000,000`까지 원래 exact gap 2는 `14,871`개였고 deletion model은 `0`개였지만, bounded gaps는 약 `89.96%` 유지됐다. 따라서 bounded-gap evidence와 exact twin-prime infinitude는 계속 분리해야 한다.

Next decisive target:

```text
CO-TICKET-23 CylinderRankCEGIS
```

Reason:

```text
Mixed expanding 2-adic cylinders are now exact finite objects, not vague heuristic examples. The next Collatz attack should synthesize a rank over cylinder transitions and search for a counterexample SCC where that rank cannot descend.
```

## Ticket 23 CEGIS Rank Lab Results

Generated artifact:

```text
data/open-problem/ticket23-cegis-rank-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-23-detector-bound-cegis.json
data/open-problem/collatz/co-ticket-23-cylinder-rank-cegis.json
data/open-problem/goldbach/gb-ticket-23-exceptional-set-cegis.json
data/open-problem/twin-prime/tp-ticket-23-parity-projection-cegis.json
```

Current verdict:

```text
cegis_rank_open_no_resolution
```

한국어 요약: TICKET-23은 증명 후보를 세운 뒤, 그 후보가 깨지는 반례성 구조를 먼저 찾는 CEGIS 방식으로 네 난제를 압박한다. 결론은 여전히 증명이나 반증이 아니다. 다만 “어떤 종류의 정리가 새로 필요하고, 어떤 쉬운 지름길은 실패하는가”가 더 구체화됐다.

1. RH: off-critical surrogate zero quartet에 대해 beta `{0.6, 0.75, 0.9}`, height `{20, 50, 100, 200}`을 테스트했다. 고정 Li-type prefix `180,000` 안에서 beta `0.6`, height `200`은 threshold `-1.0` 이하의 강한 음수 신호를 보이지 않았다. 이것은 RH 반례가 아니라, finite-prefix detector 증명 후보를 깨는 CEGIS witness다.
2. Collatz: odd residue quotient graph를 modulus `2^8, 2^10, 2^12, 2^14`에서 만들었다. 단순 integer-rank는 약 1/3의 edge에서 감소하지 않았고, `2^10`, `2^12` quotient에는 실제 positive cycle로 lift되지 않는 false cycle SCC가 나타났다. 따라서 필요한 정리는 lift-aware well-founded rank다.
3. Goldbach: `1,000,000` 이하 짝수에서 직접 반례는 없었다. hardest smallest-witness case는 `503222 = 523 + 502699`였다. 이 결과는 bounded exceptional set이 비어 있다는 계산 증거이며, 전체 증명에는 큰 N에서 representation count가 양수라는 explicit lower bound가 필요하다.
4. Twin Prime: deletion model은 `3,000,000`까지 exact gap 2를 `20,932 -> 0`으로 제거하지만, gap `<= 60` bounded mass의 약 `90.28%`를 유지한다. 따라서 bounded-gap 생존은 twin-prime infinitude를 증명하지 못하고, exact gap-2 하한 functional이 필요하다.

Next decisive target:

```text
CO-TICKET-24 LiftAwareRankOrExactGapWeight
```

Reason:

```text
TICKET-23 isolates two concrete next proof objects: a lift-aware Collatz rank that defeats false quotient cycles, and an exact-gap sieve weight that cannot be fooled by bounded-gap deletion models. These are narrower than trying to prove all four conjectures at once.
```

## Ticket 24 Bridge-Weight Lab Results

Generated artifact:

```text
data/open-problem/ticket24-bridge-weight-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-24-uniform-detector-budget.json
data/open-problem/collatz/co-ticket-24-lift-aware-rank-probe.json
data/open-problem/goldbach/gb-ticket-24-explicit-window-budget.json
data/open-problem/twin-prime/tp-ticket-24-exact-gap-weight-search.json
```

Current verdict:

```text
bridge_weight_open_no_resolution
```

한국어 요약: TICKET-24는 TICKET-23에서 분리된 두 핵심 후보, 즉 Collatz의 lift-aware rank와 Twin Prime의 exact-gap weight를 더 좁은 보조정리 형태로 압박한다. 결론은 여전히 네 난제의 증명이나 반증이 아니다. 하지만 “반례처럼 보이는 구조를 제거하는 부분 정리”와 “실제 증명에 필요한 exact statistic”이 더 선명해졌다.

1. RH: beta `{0.6, 0.75, 0.9}`, height `{100, 200, 500}`, search cap `1,000,000`에서 uniform detector budget을 만들었다. beta `0.6`, height `500`은 cap 안에서 threshold `-1.0` 이하 신호를 보이지 않았다. 따라서 fixed finite prefix proof는 다시 차단되고, height-uniform detector theorem이 필요하다.
2. Collatz: quotient graph를 `2^8, 2^10, 2^12, 2^14, 2^16, 2^18`까지 확장했다. `2^10`, `2^12`에서 나온 비자명 quotient cycle은 모두 affine lift audit에서 `globally_eliminated_expanding_word`로 제거됐고, `2^14` 이후 테스트한 quotient에는 known `1` cycle만 남았다. 이것은 전체 Collatz 증명이 아니라, false quotient cycle 제거 보조정리 후보다.
3. Goldbach: `2,000,000` 이하 직접 반례는 없었다. hardest first-witness case는 `1077422 = 601 + 1076821`였다. stride `2,000` sampled representation-count budget은 약한 finite window를 찾지만, 전체 증명에는 모든 충분히 큰 짝수에 대한 explicit lower bound가 필요하다.
4. Twin Prime: exact gap weight는 deletion model을 분리한다. `3,000,000`에서 exact gap 2 margin은 `20,932`이고 deletion model은 `0`이다. 반면 gap 2를 제외한 bounded-gap-only mass는 deletion model에서 약 `99.98%` 유지된다. 따라서 bounded-gap-only 통계는 거의 완전히 속고, exact gap 2 하한 정리가 필요하다.

Next decisive target:

```text
CO-TICKET-25 FormalAffineLiftLemma
```

Reason:

```text
TICKET-24 produces the most theorem-like local object so far: a quotient Collatz cycle can be globally eliminated when its exact valuation word has no positive integral affine fixed point. This can be formalized independently before attempting the full Collatz rank theorem.
```

## Ticket 25 Formal Lemma Kernel Results

Generated artifact:

```text
data/open-problem/ticket25-formal-lemma-kernel.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-25-finite-prefix-kernel.json
data/open-problem/collatz/co-ticket-25-affine-lift-lemma.json
data/open-problem/goldbach/gb-ticket-25-finite-exception-kernel.json
data/open-problem/twin-prime/tp-ticket-25-bounded-gap-counterkernel.json
```

Current verdict:

```text
formal_kernel_open_no_resolution
```

한국어 요약: TICKET-25는 TICKET-24의 계산을 “형식화 가능한 작은 kernel lemma”와 “깨진 shortcut”으로 추출한다. 결론은 여전히 네 난제의 증명이나 반증이 아니다. 하지만 Collatz 쪽에서는 실제로 독립 형식화가 가능한 부분 보조정리 후보가 나왔다.

1. RH: finite Li-prefix만 확인하는 proof route는 surrogate family에서 refuted된다. beta `0.6`, height `500`, prefix `1,000,000` 안에서 threshold witness가 없다. 이것은 RH 반례가 아니라 fixed-prefix proof 전략에 대한 kernel counterexample다.
2. Collatz: `2^10`, `2^12` quotient의 비자명 cycle 3개는 valuation word의 affine fixed point 조건을 통과하지 못한다. 모두 `globally_eliminated_expanding_word`이고, positive cycle 후보는 known `1`뿐이다. 이 kernel은 “해당 quotient false cycle은 양의 정수 cycle이 아니다”라는 부분 정리로 형식화할 수 있다.
3. Goldbach: `2,000,000` 이하 finite exception kernel은 counterexample count `0`이다. 이 kernel은 finite range만 닫고, 전체 추측에는 큰 짝수 전체에 대한 explicit lower bound가 따로 필요하다.
4. Twin Prime: bounded-gap-only 통계는 deletion counterkernel에 의해 refuted된다. exact gap 2를 모두 제거해도 gap 2 제외 bounded mass는 거의 보존된다. 따라서 twin-prime proof는 exact-gap-2 lower-bound functional을 사용해야 한다.

Next decisive target:

```text
CO-TICKET-26 LeanAffineLiftMicroProof
```

Reason:

```text
The Collatz affine lift kernel is now small enough to formalize as a standalone micro-proof: derive the affine fixed-point condition for a valuation word and prove that the listed expanding quotient cycles cannot be positive integer cycles.
```

## Ticket 26 Micro-Lemma Closure Results

Generated artifact:

```text
data/open-problem/ticket26-micro-lemma-closure.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-26-finite-universal-gap.json
data/open-problem/collatz/co-ticket-26-affine-fixed-point-proof.json
data/open-problem/goldbach/gb-ticket-26-finite-window-gap.json
data/open-problem/twin-prime/tp-ticket-26-bounded-gap-model-separation.json
```

Current verdict:

```text
micro_lemma_closed_full_conjectures_open
```

한국어 요약: TICKET-26은 네 난제를 풀었다고 주장하지 않는다. 대신 증명 시도 중 실제로 닫을 수 있는 작은 명제를 닫는다. 가장 의미 있는 진전은 Collatz다. quotient graph에서 cycle처럼 보였던 후보가 양의 정수 cycle이 되려면 exact valuation word의 affine fixed point 조건을 통과해야 한다는 산술 lemma를 독립 재계산했다.

1. RH: finite prefix만으로 universal RH-equivalent statement를 증명할 수 없다는 shortcut refutation을 닫았다. 남은 핵심은 unchecked tail을 덮는 all-height theorem이다.
2. Collatz: valuation word `w`의 accelerated composition은 `F_w(n)=(3^k n+c)/2^s`이다. 만약 `F_w(n)=n`인 양의 정수 cycle이면 `(2^s-3^k)n=c`가 필요하다. Ticket 24의 false quotient cycle 3개는 모두 `2^s-3^k <= 0`라서 positive integer fixed point가 불가능하다. positive control인 word `[2]`는 candidate `1`로 정확히 검증된다.
3. Goldbach: finite window certificate는 해당 범위만 닫는다. `2,000,000` 이하 반례 없음은 중요하지만, `2,000,002` 이후를 덮는 explicit large-even theorem 없이는 전체 증명이 아니다.
4. Twin Prime: exact gap 2를 모두 지워도 bounded-gap statistic이 유지되는 finite model separation을 닫았다. 따라서 bounded-gap-only 증명은 twin-prime infinitude를 증명하지 못한다.

Closed micro-lemma:

```text
CO-TICKET-26 AffineFixedPointNecessaryCondition
```

Remaining decisive target:

```text
CO-TICKET-27 LiftAwareNonCyclicRankSearch
```

Reason:

```text
The false-cycle part is now a closed arithmetic micro-lemma. The next real Collatz barrier is not cyclic fixed points; it is proving that every non-cyclic exact branch eventually descends under a well-founded lift-aware rank.
```

## Ticket 27 Rank-Frontier Lab Results

Generated artifact:

```text
data/open-problem/ticket27-rank-frontier-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-27-tail-uniformity-frontier.json
data/open-problem/collatz/co-ticket-27-lift-aware-noncyclic-rank.json
data/open-problem/goldbach/gb-ticket-27-tail-cutoff-frontier.json
data/open-problem/twin-prime/tp-ticket-27-exact-gap-rank-frontier.json
```

Current verdict:

```text
rank_frontier_open_no_resolution
```

한국어 요약: TICKET-27은 TICKET-26에서 닫힌 작은 보조정리를 다음 proof frontier로 밀어붙인다. 가장 중요한 결과는 Collatz다. `mod 2^b` quotient graph에서 known `1` cycle까지의 거리 rank는 대표 residue edge에서는 감소하지만, 실제 integer lift에서는 대량으로 깨진다. 따라서 "finite quotient rank만으로 Collatz를 증명한다"는 전략은 반례로 기각된다.

1. RH: finite prefix shortcut은 닫혔지만, 여전히 unchecked tail 전체를 덮는 uniform explicit-formula theorem이 없다. 다음 실험은 Li/kernel tail majorant의 symbolic separability counterexample 탐색이다.
2. Collatz: `2^12, 2^14, 2^16, 2^18` quotient rank를 테스트했다. `2^14` 이상에서는 quotient가 known `1` cycle로 모두 도달하지만, sampled integer lift에서 rank violation이 각각 `91,591`, `362,379`, `1,447,879`개 발생했다. residue `1`을 제외해도 violation이 남는다. 예를 들어 `mod 2^14`에서 residue `3`, lift `1`, integer `16387`은 quotient rank가 `2`에서 다음 residue rank `56`으로 증가한다.
3. Goldbach: finite window는 base case일 뿐이다. 전체 증명에는 finite certificate ceiling 아래로 내려오는 explicit large-even lower-bound theorem이 필요하다.
4. Twin Prime: bounded-gap deletion model을 통과하는 statistic은 여전히 부적격이다. 다음 proof frontier는 exact gap 2 삭제 시 반드시 붕괴하는 lower-bound functional이다.

Closed shortcut:

```text
finite quotient distance rank implies global Collatz descent
```

Remaining decisive target:

```text
CO-TICKET-28 LiftCoordinateDebtRankCEGIS
```

Reason:

```text
The quotient-only Collatz rank is now refuted by explicit lift counterexamples. A viable rank must include the lift coordinate, valuation debt, or exact 2-adic cylinder data and must decrease after a bounded debt window.
```

## Ticket 28 Trichotomy Descent Lab Results

Generated artifact:

```text
data/open-problem/ticket28-trichotomy-descent-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-28-mertens-tail-trichotomy.json
data/open-problem/collatz/co-ticket-28-lift-coordinate-debt-rank-cegis.json
data/open-problem/goldbach/gb-ticket-28-witness-cutoff-trichotomy.json
data/open-problem/twin-prime/tp-ticket-28-exact-gap-tail-trichotomy.json
```

Current verdict:

```text
trichotomy_descent_open_no_resolution
```

한국어 요약: TICKET-28은 사용자가 제시한 세 가지 증명 경로, 즉 반례 찾기, 반례가 없음을 증명하기, 대우법으로 증명하기를 각 난제에 명시적으로 적용한다. 이번 단계의 실질적 계산 진전은 Collatz exact cylinder descent다. 이는 단순 residue rank가 아니라 valuation word가 실제로 보장되는 `2^m` cylinder 전체에 대해 affine map을 계산하고, 그 cylinder의 모든 양의 lift가 시작값보다 작아지는지를 판정한다.

1. RH: `M(n)/sqrt(n)` Mertens stress를 `5,000,000`까지 계산했다. `n>=10,000`에서 최대 관측값은 `0.4629770364`이고 위치는 `24,185`이다. 이것은 RH와 양립하는 finite stress일 뿐이며, RH 반례나 증명은 아니다. 전체 증명에는 off-critical zero를 배제하는 tail-uniform theorem 또는 동등한 positivity theorem이 필요하다.
2. Collatz: `2^12, 2^14, 2^16, 2^18, 2^20, 2^22` exact cylinder를 검사했다. `2^22`에서는 `2,097,152`개 odd cylinder 중 `1,997,692`개가 all-lift descent로 닫혔고, `99,459`개는 `needs_split`으로 남았다. 또한 `1,000,000` 이하 odd start에서 자기보다 작아지지 않는 finite stopping counterexample은 발견되지 않았고, 최장 stopping-to-below-start는 `626,331`에서 `111` accelerated steps였다.
3. Goldbach: `2,000,000` 이하 모든 짝수에 대해 첫 소수 witness를 찾았다. 반례는 없었고, 가장 늦게 첫 witness가 나온 행은 `1,077,422 = 601 + 1,076,821`이다. 하지만 finite witness scan은 큰 짝수 전체에 대한 explicit lower-bound theorem을 대체하지 못한다.
4. Twin Prime: `10,000,000` 이하 exact gap-2 소수쌍은 `58,980`개이며 마지막 관측 pair는 `(9,999,971, 9,999,973)`이다. 이는 exact-gap finite evidence이지만, 무한히 많은 twin prime을 증명하려면 exact-gap-2 lower-bound functional이 필요하다.

Closed partial theorem:

```text
For every Collatz cylinder marked all_lift_descent in TICKET-28, the exact accelerated affine map sends every positive odd lift in that cylinder below its starting value.
```

Remaining decisive target:

```text
CO-TICKET-29 AdaptiveCylinderSplitTermination
```

Reason:

```text
The exact cylinder method now proves many full lift families, but the proof cannot be promoted while needs_split cylinders remain. The next theorem must show that adaptive splitting of only those cylinders terminates or yields a well-founded valuation-debt descent.
```

## Ticket 29 Adaptive Frontier Lab Results

Generated artifact:

```text
data/open-problem/ticket29-adaptive-frontier-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-29-tail-bridge-frontier.json
data/open-problem/collatz/co-ticket-29-adaptive-cylinder-split.json
data/open-problem/goldbach/gb-ticket-29-least-counterexample-cutoff.json
data/open-problem/twin-prime/tp-ticket-29-exact-gap-tail-pressure.json
```

Current verdict:

```text
adaptive_frontier_open_no_resolution
```

한국어 요약: TICKET-29는 TICKET-28의 `needs_split`을 직접 추적한다. Collatz에서는 전체 `2^28` odd cylinder를 전부 열거하지 않고, `2^12`에서 시작해 닫히지 않은 cylinder만 adaptive하게 쪼갰다. 이 접근은 계산량을 크게 줄이지만, 열린 frontier가 사라지지는 않았다. 따라서 “needs_split만 계속 쪼개면 자연스럽게 증명이 끝난다”는 순진한 전략은 현재 데이터로 지지되지 않는다.

1. RH: Mertens stress를 `10,000,000`까지 확장했다. `M(10,000,000)=1,037`이고, `n>=1,000,000`에서 최대 `|M(n)|/sqrt(n)`는 `0.4182454758` at `1,066,854`이다. 이것은 RH-compatible finite stress이며, 여전히 off-critical zero를 배제하지 못한다.
2. Collatz: adaptive split은 `base_bits=12`, `max_bits=28`에서 `8,687,144`개 상태를 처리했다. 이는 `2^28`의 full odd cylinder `134,217,728`개 중 약 `6.47%`만 본 것이다. 하지만 max depth에서 열린 frontier가 `3,618,400`개 남았고, full max space 기준 open fraction은 `0.02695918`이다. 이는 반례가 아니라, split termination theorem이 아직 없다는 정량적 장애물이다.
3. Goldbach: finite witness scan을 `5,000,000`까지 확장했다. 반례는 없었고 `2,499,999`개 짝수를 확인했다. 가장 늦게 첫 witness가 나온 행은 `3,807,404 = 751 + 3,806,653`이다. 전체 증명은 여전히 large-even tail lower bound에 달려 있다.
4. Twin Prime: exact gap-2 scan을 `20,000,000`까지 확장했다. twin pair count는 `107,407`, 마지막 관측 pair는 `(19,999,547, 19,999,549)`, 관측된 twin-start 간 최대 gap은 `2,190`이다. finite exact-gap persistence는 무한성을 증명하지 못한다.

Closed partial theorem:

```text
Every all_lift_descent state in the Ticket 29 adaptive Collatz run is an exact cylinder whose every positive odd lift descends below its starting value.
```

Refuted shortcut:

```text
Naive adaptive splitting alone is enough evidence for Collatz proof completion.
```

Remaining decisive target:

```text
CO-TICKET-30 ValuationDebtPotentialSynthesis
```

Reason:

```text
The adaptive frontier is smaller than full enumeration but does not vanish. The next proof attempt must synthesize a well-founded potential on open needs_split cylinders, or find a genuine obstruction/counterexample pattern inside that frontier.
```

### Ticket 30: Potential synthesis and obstruction search

Generated artifact:

```text
data/open-problem/ticket30-potential-synthesis-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-30-tail-majorant-synthesis.json
data/open-problem/collatz/co-ticket-30-valuation-debt-potential.json
data/open-problem/goldbach/gb-ticket-30-explicit-constant-ledger.json
data/open-problem/twin-prime/tp-ticket-30-exact-gap-functional.json
```

Aggregate verdict:

```text
potential_synthesis_open_no_resolution
```

한국어 요약: TICKET-30은 네 난제를 증명했다고 주장하지 않는다. 이번 단계의 목표는 TICKET-29에서 남은 열린 경계를 대상으로 “증명으로 이어질 수 있어 보이는 자연스러운 후보”를 실제로 합성하거나, 반대로 그 후보군이 실패한다는 반례 구조를 찾는 것이다. Collatz에서는 `needs_split` 상태들 사이에 항상 감소하는 valuation-debt potential을 만들 수 있는지 검사했다. 결과적으로 단순한 scalar linear potential 계열은 bounded adaptive frontier에서 모두 탈락했다.

1. RH: 더 큰 유한 Mertens scan 대신 tail majorant synthesis 문제로 목표를 바꿨다. 필요한 정리는 “off-critical zero가 있으면 유한 positivity violation으로 내려온다”는 tail-uniform bridge이다. 이 bridge는 아직 열려 있고, 유한 stress만으로 RH를 결정할 수 없다는 경계를 유지한다.
2. Collatz: exact-cylinder frontier에서 네 개 특징량 `coefficient_log2_debt`, `prefix_length`, `consumed_bits`, `next_valuation`에 대한 scalar linear potential을 시험했다. `full_candidate_max_bits=20`에서 candidate parent edge는 `32,951`개이고, `grid_search_max_bits=18`에서 grid parent edge는 `9,610`개이다. 정수 가중치 `[-2,2]^4` 전체에서 살아남은 weight는 `0`개였다. 가장 좋은 weight `[2,-1,-2,-1]`도 `6,826`개 violation, violation rate `0.39157871`을 남겼다. 이것은 Collatz 반례가 아니라, 단순 선형 potential 증명 전략의 bounded falsification이다.
3. Goldbach: finite witness scan의 확장이 아니라 explicit constant ledger로 전환했다. 필요한 남은 정리는 large-even tail에서 minor arc, major arc, exceptional character, singular series 하한을 하나의 검산 가능한 부등식 장부로 닫는 것이다.
4. Twin Prime: 더 긴 exact gap scan 대신 exact-gap functional synthesis로 전환했다. 필요한 남은 정리는 gap-2 선택자가 sieve/RMT/Fredholm 유사량에서 무한히 양의 질량을 유지한다는 tail theorem이다.

Closed partial theorem:

```text
No tested scalar linear valuation-debt potential over the four Ticket 30 Collatz features strictly decreases on every tested open adaptive-frontier edge.
```

Refuted shortcut:

```text
A simple one-dimensional linear potential in debt, prefix length, consumed bits, and next valuation is enough to close the Collatz adaptive frontier.
```

Remaining decisive target:

```text
CO-TICKET-31 LexicographicPiecewisePotentialCEGIS
```

Reason:

```text
The failed scalar potentials do not refute Collatz. They show that a viable proof, if it follows the current exact-cylinder path, probably needs a lexicographic, piecewise, nonlinear, or certificate-carrying descent invariant.
```

### Ticket 31: Feature-stutter obstruction

Generated artifact:

```text
data/open-problem/ticket31-feature-stutter-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-31-finite-stress-stutter.json
data/open-problem/collatz/co-ticket-31-feature-stutter-obstruction.json
data/open-problem/goldbach/gb-ticket-31-cutoff-ledger-stutter.json
data/open-problem/twin-prime/tp-ticket-31-parity-selector-stutter.json
```

Aggregate verdict:

```text
feature_stutter_open_no_resolution
```

한국어 요약: TICKET-31은 TICKET-30보다 더 강한 부정 결과를 준다. TICKET-30은 단순 선형 potential이 실패했다는 계산 결과였다. TICKET-31은 그 실패가 단순히 “선형이라서” 생긴 문제가 아님을 보인다. Collatz exact-cylinder frontier에는 부모와 자식이 같은 관측 특징량을 갖는 feature-stutter edge가 존재한다. 그러면 그 특징량만 입력으로 받는 어떤 함수도 부모와 자식을 구분할 수 없으므로, scalar, lexicographic, nonlinear, learned potential 모두 strict local descent를 만족할 수 없다.

1. RH: finite stress가 아무리 RH-compatible하게 반복되어도 zero-side tail theorem이 없으면 증명으로 승격되지 않는다. TICKET-31에서는 이것을 finite-stress stutter obstruction으로 명시했다.
2. Collatz: `base_bits=12`, `max_bits=21` adaptive frontier에서 parent edge `61,740`개, open child edge `112,860`개를 검사했다. 기본 네 특징량 `coefficient_log2_debt`, `prefix_length`, `consumed_bits`, `next_valuation`만 보면 indistinguishable edge가 `30,997`개, 비율 `0.27465001`이다. prefix word와 low residue까지 추가해도 같은 `30,997`개가 남는다. 따라서 이 local signature만 보는 strict descent proof는 불가능하다.
3. Goldbach: finite witness persistence는 explicit large-even cutoff ledger를 대체하지 못한다. 필요한 대상은 major arc, minor arc, singular series, exceptional character error를 하나의 양의 하한 부등식으로 닫는 검산 가능한 장부이다.
4. Twin Prime: bounded-gap 또는 averaged-pair 통계는 parity-blind stutter를 통과할 수 있다. exact gap 2를 강제하려면 wider gap-only countermodel을 배제하는 selector theorem이 필요하다.

Closed partial theorem:

```text
If an open Collatz exact-cylinder parent and an open child have identical local signature, then no deterministic scalar, lexicographic, nonlinear, or learned potential depending only on that signature can strictly decrease on that edge.
```

Proof sketch:

```text
Let S be the chosen local signature and let P be any deterministic potential that depends only on S.
For a feature-stutter edge, S(parent) = S(child). Therefore P(parent) = P(child).
Strict descent requires P(parent) > P(child), contradiction.
For a lexicographic tuple, the same equality holds componentwise.
```

Refuted shortcut:

```text
Replacing the failed Ticket 30 scalar linear potential with a black-box nonlinear or lexicographic function of the same local features is enough to close the Collatz frontier.
```

Remaining decisive target:

```text
CO-TICKET-32 StatefulMeasureOrAutomatonDescent
```

Reason:

```text
Scale-dependent features such as modulus bits or cylinder mass separate the tested stutters, but they are not by themselves well-founded pointwise descent proofs: bits may grow without a prior bound, and mass may tend to zero. The next proof candidate must supply either a compactness/measure theorem, a stateful automaton invariant, or an eventual-closure theorem for infinite stutter paths.
```

### Ticket 32: Stateful measure and stutter-budget certificate

Generated artifact:

```text
data/open-problem/ticket32-stateful-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-32-stateful-tail-certificate.json
data/open-problem/collatz/co-ticket-32-stateful-measure-descent.json
data/open-problem/goldbach/gb-ticket-32-stateful-cutoff-ledger.json
data/open-problem/twin-prime/tp-ticket-32-stateful-parity-selector.json
```

Aggregate verdict:

```text
stateful_measure_open_no_resolution
```

한국어 요약: TICKET-32는 TICKET-31이 막아낸 local feature-only descent를 우회하기 위해 stateful certificate를 시도한다. Collatz에서는 feature-stutter edge마다 “같은 signature가 앞으로 몇 단계 더 지속되는가”를 lookahead로 계산해 stutter budget으로 붙였다. 이 budget은 반복 low-child stutter 구간에서는 1씩 감소한다. 그러나 이것은 bounded frontier 안의 certificate이지, 모든 cylinder와 high-child/non-stutter branch를 닫는 전역 증명은 아니다.

1. RH: finite stress 대신 tail state certificate가 필요하다는 방향으로 이동했다. off-critical zero가 있으면 finite replayable positivity violation으로 내려온다는 stateful tail bridge는 아직 없다.
2. Collatz: `base_bits=12`, `adaptive_max_bits=22`, `max_chain_bits=96`에서 parent edge `113,115`개, open child edge `208,481`개를 검사했다. feature-stutter edge는 `56,714`개이고 비율은 `0.27203438`이다. 모든 stutter chain은 `signature_changed` `30,939`개 또는 `terminal` `25,775`개로 끝났고, unresolved는 `0`개였다. 최대 same-signature run은 `17`단계이다.
3. Goldbach: finite witness가 아니라 major/minor arc와 error budget을 상태 전이로 보존하는 cutoff ledger state machine이 필요하다.
4. Twin Prime: exact gap 2 mass가 parity countermodel 상태 전이에서 사라지지 않는 selector state machine이 필요하다.

Closed partial theorem:

```text
Every tested same-signature low-child stutter chain in the Ticket 32 Collatz bounded frontier exits the same local signature within the recorded finite budget. A certificate-carrying budget strictly decreases along repeated same-signature low-child stutter moves in this bounded frontier.
```

Refuted shortcut:

```text
The bounded stutter-budget certificate alone proves Collatz.
```

Reason:

```text
The budget is lookahead-derived and bounded to the tested frontier. A full proof still needs a theorem showing that every possible exact-cylinder path has finite budget or zero obstruction mass, and it must also close high-child and non-stutter transitions.
```

Remaining decisive target:

```text
CO-TICKET-33 GlobalMeasureCompactnessOrHighBranchClosure
```

### Ticket 33: Global measure pressure and high-branch obstruction

Generated artifact:

```text
data/open-problem/ticket33-global-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-33-global-tail-compactness.json
data/open-problem/collatz/co-ticket-33-global-measure-compactness.json
data/open-problem/goldbach/gb-ticket-33-global-cutoff-compactness.json
data/open-problem/twin-prime/tp-ticket-33-global-parity-compactness.json
```

Aggregate verdict:

```text
global_measure_open_no_resolution
```

한국어 요약: TICKET-33은 TICKET-32가 닫지 못한 high-child branch와 전역 compactness 문제를 직접 건드린다. Collatz exact-cylinder frontier를 `base_bits=12`에서 `max_bits=28`까지 level-by-level로 추적해 normalized open cylinder mass가 감소하는지 계산했다. 결과적으로 mass는 단조 감소했지만, 마지막 frontier mass는 양수이고 high-child branch도 계속 열려 있었다. 따라서 이것은 전역 증명이 아니라 “전역 measure theorem이 필요하다”는 정량적 증거이다.

1. RH: bounded tail certificate가 있어도 infinitely many zero contribution을 제어하는 global tail compactness theorem이 필요하다.
2. Collatz: open frontier mass는 `1.0`에서 `0.026959180832`까지 단조 감소했다. 마지막 frontier count는 `3,618,400`이다. 마지막 8개 level의 log2 mass fit은 per-bit factor `0.916768160879`를 보였다. 그러나 high-open child edge는 `3,901,346`개이고 high-only open child edge도 `125,449`개다. 즉 high branch가 자동으로 닫힌다는 shortcut은 반례를 갖는다.
3. Goldbach: finite cutoff ledger가 있어도 error term이 cutoff 이후 다시 열리지 않는 global cutoff compactness theorem이 필요하다.
4. Twin Prime: exact-gap selector가 있어도 parity state가 wider-gap leakage로 mass를 잃지 않는 global parity compactness theorem이 필요하다.

Closed partial theorem:

```text
In the tested Collatz adaptive frontier from 12 to 28 bits, normalized open cylinder mass decreases monotonically from 1.0 to 0.026959180832.
```

Refuted shortcut:

```text
High-child branches automatically close once low-child feature stutter is budgeted.
```

Reason:

```text
The tested frontier contains high-only open child edges: the low child can close while the high child remains open. Therefore high-branch closure requires its own theorem or automaton, not just the low-child stutter budget.
```

Remaining decisive target:

```text
CO-TICKET-34 HighBranchAutomatonOrMassLimitTheorem
```

Proof boundary:

```text
Finite monotone mass decrease and a negative fitted slope do not prove that open mass tends to zero. A full proof must establish a global compactness or mass-limit theorem for every future bit length, or a high-branch automaton that closes all remaining obstruction paths.
```

### Ticket 34: High-branch automaton and mass-limit split

Generated artifact:

```text
data/open-problem/ticket34-high-branch-automaton-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-34-tail-automaton-limit.json
data/open-problem/collatz/co-ticket-34-high-branch-automaton.json
data/open-problem/goldbach/gb-ticket-34-cutoff-automaton-limit.json
data/open-problem/twin-prime/tp-ticket-34-parity-automaton-limit.json
```

Aggregate verdict:

```text
high_branch_automaton_open_no_resolution
```

한국어 요약: TICKET-34는 TICKET-33에서 남은 high-branch obstruction을 둘로 분해했다. 첫째, finite automaton state만으로 high branch가 자동으로 닫히는지 검사했다. 둘째, pointwise closure가 실패한다면 aggregate mass contraction이 남는지 finite quotient의 spectral pressure를 계산했다. 결과는 둘 다 조심스럽다. 단순 finite-feature automaton은 state collision 때문에 막혔고, aggregate mass는 계속 줄어드는 압력이 보였지만 이것은 아직 `limsup < 1` 정리가 아니다.

1. RH: tail compactness는 tail automaton 또는 uniform zero-sum mass-limit theorem으로 분해된다. high-height surrogate zero 삽입에서 tail-kernel state collision을 검사해야 한다.
2. Collatz: `base_bits=12`에서 `max_bits=24`까지 high-branch automaton audit를 실행했다. transition parent는 `387,587`개였고, high-open parent는 `346,972`개, high-only parent는 `20,135`개였다. 모든 level의 aggregate open-mass ratio는 1보다 작았고 최대 ratio는 `0.944905286616`이었다. 그러나 both-open parent가 존재해 pointwise contraction은 막혔다.
3. Goldbach: cutoff compactness는 finite error-state automaton 또는 future error-state mass bound로 분해된다.
4. Twin Prime: parity compactness는 exact-gap mass가 wider-gap leakage로 사라지지 않는 automaton 또는 exact-gap mass-limit theorem으로 분해된다.

Finite automaton findings:

```text
coarse_debt: states=995, ambiguous=301, noncontracting=922, radius=0.675222044668
tail2_debt: states=6,532, ambiguous=1,722, noncontracting=5,963, radius=0.692640682511
tail4_debt: states=25,252, ambiguous=5,362, noncontracting=22,567, radius=0.685447084869
tail4_residue64: states=75,871, ambiguous=12,940, noncontracting=66,299, radius=0.674244169297
full_word_residue64: states=282,891, ambiguous=21,138, noncontracting=247,442, radius=0.533111158891
```

Closed partial theorem:

```text
In the tested Collatz frontier from 12 to 24 bits, every evaluated level has aggregate open-mass ratio below one.
```

Refuted shortcuts:

```text
A pointwise high-branch closure proof follows from low-child stutter budgets.
A small finite feature automaton can decide high-branch closure without state collisions.
```

Reason:

```text
The tested quotient families contain ambiguous states: the same finite state can map to different closure labels, including high-open and high-only outcomes. They also contain many pointwise noncontracting states with both children open. Therefore a proof cannot rely on these finite states alone.
```

Remaining decisive target:

```text
CO-TICKET-35 LimsupMassContractionOrStateRefinementTheorem
```

Proof boundary:

```text
Finite aggregate spectral radius below one is evidence for a mass-limit route, not a proof. A full Collatz proof still needs a symbolic theorem that the limsup of all future adaptive open-mass ratios is strictly below one, or a refined well-founded state that eliminates the observed collisions for every cylinder.
```

### Ticket 35: Limsup mass refinement and null-set gap

Generated artifact:

```text
data/open-problem/ticket35-limsup-mass-refinement-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-35-tail-nullset-exclusion.json
data/open-problem/collatz/co-ticket-35-limsup-mass-refinement.json
data/open-problem/goldbach/gb-ticket-35-exceptional-set-elimination.json
data/open-problem/twin-prime/tp-ticket-35-exact-gap-nullset.json
```

Aggregate verdict:

```text
limsup_mass_refinement_open_no_resolution
```

한국어 요약: TICKET-35는 지금까지의 결과를 버리지 않고 정리했다. TICKET-31은 local feature-only descent를 막았고, TICKET-32는 bounded low-child stutter budget을 만들었고, TICKET-33/34는 high branch와 aggregate mass contraction을 분리했다. 이번 결론은 더 엄격하다. Mass contraction은 중요한 신호지만, 그것만으로는 Collatz 증명이 아니다. 왜냐하면 measure-zero 예외 집합 안에도 개별 자연수 counterexample이 있을 수 있기 때문이다.

1. RH: finite-prefix나 measure-small tail failure가 아니라, 모든 off-critical zero를 uniform하게 배제하는 tail theorem이 필요하다.
2. Collatz: exact mass window `12..28 bits`에서 final open mass는 `0.026959180832`, max mass ratio는 `0.944905286616`, tail-window max ratio는 `0.935207747252`, finite candidate epsilon은 `0.064792252748`이다. 그러나 `mass_zero_not_pointwise_proof`가 핵심 장애물로 남았다.
3. Goldbach: almost-all positivity나 density evidence는 sparse exceptional even integer를 제거하지 못한다. pointwise cutoff theorem이 필요하다.
4. Twin Prime: bounded statistics나 typical exact-gap mass는 arbitrarily large exact gap-2 pairs를 강제하지 못한다. uniform exact-gap lower bound가 필요하다.

State refinement findings:

```text
full_word_residue64: blocked_by_state_collision, states=82,273, ambiguous=5,114, noncontracting=74,832
full_word_residue1024_bits_mod16: blocked_by_pointwise_noncontraction, states=113,645, ambiguous=0, noncontracting=99,229
full_word_residue4096_bits_mod32: blocked_by_pointwise_noncontraction, states=114,937, ambiguous=0, noncontracting=99,229
exact_residue_and_bits: collision_free_but_unbounded_identity_state, states=114,937, ambiguous=0, noncontracting=99,229
```

Discarded routes:

```text
mass-only Collatz proof without an arithmetic null-set exclusion theorem
fixed finite-feature automaton closure after observed state collisions
pointwise high-branch closure inherited from low-child stutter budgets
```

Retained routes:

```text
limsup mass contraction as a useful but insufficient global pressure statement
state refinement only if it becomes uniform and well-founded rather than identity-like
contrapositive search for an infinite natural-number path inside the null frontier
```

Closed partial theorem:

```text
The tested Collatz frontier keeps aggregate mass ratios below one through the recorded exact window.
```

Remaining decisive target:

```text
CO-TICKET-36 NullSetArithmeticExclusionOrUniformRankTheorem
```

Proof boundary:

```text
Even a proved measure-zero limiting obstruction set would not by itself prove Collatz for every positive integer. A full proof must either exclude natural-number paths from that null set, or provide a uniform well-founded rank that decreases on every infinite adaptive path.
```

### Ticket 36: Null-frontier arithmetic and pointwise exception exclusion

Generated artifact:

```text
data/open-problem/ticket36-null-frontier-arithmetic-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-36-offcritical-null-exclusion.json
data/open-problem/collatz/co-ticket-36-natural-null-frontier.json
data/open-problem/goldbach/gb-ticket-36-sparse-exception-exclusion.json
data/open-problem/twin-prime/tp-ticket-36-sparse-gap-exclusion.json
```

Aggregate verdict:

```text
null_frontier_arithmetic_open_no_resolution
```

한국어 요약: TICKET-36은 TICKET-35에서 남은 핵심 장애물인 `mass_zero_not_pointwise_proof`를 실제 산술 질문으로 바꿨다. 질량, 밀도, typical behavior가 아무리 좋아도 sparse/null exceptional object가 하나라도 무한히 남으면 난제는 깨진다. 따라서 네 난제 모두에서 필요한 것은 "예외가 드물다"가 아니라 "예외가 없다"는 pointwise theorem이다.

Collatz bounded natural-exit audit:

```text
tested odd n: 50,000 values, all odd n <= 100,000
base bits: 12
shallow probe: up to 96 bits
deep resolve: up to 180 bits
shallow unresolved count: 17
deep unresolved count: 0
max exit bits: 135
max exit slack over bit_length(n): 119
max exit minus odd Collatz steps: 27
direct sample termination: all tested direct orbits reached 1
```

Interpretation:

```text
Every tested odd integer exits the adaptive null frontier by 135 bits, so no bounded Collatz counterexample was found in the tested range. However, the audit refutes shallow natural-exclusion shortcuts: even n <= 100,000 can require much deeper certificate bits than its own bit length.
```

Discarded Collatz routes:

```text
measure-zero frontier proof without natural-integer exclusion
small constant slack theorem exit_bits <= bit_length(n) + C for C <= 112 in the tested range
stopping-time proxy proof unless stopping time is itself bounded by an independent rank
```

Retained Collatz routes:

```text
contrapositive search for a natural n with no frontier exit
uniform well-founded rank that implies finite frontier exit without using orbit termination as an oracle
deep arithmetic exclusion theorem for the limiting 2-adic null frontier
```

Cross-problem transfer:

1. RH: finite-window and measure-small tail tests are insufficient. A proof must exclude every off-critical zero pointwise.
2. Goldbach: almost-all positivity is insufficient. A zero-density infinite set of even exceptions would still falsify the conjecture.
3. Twin Prime: bounded prime statistics are insufficient. A proof must force exact gap 2 infinitely often, not merely bounded gaps or typical pair mass.
4. Collatz: mass decay is insufficient. A proof must exclude every positive integer from the limiting open frontier or give a non-circular decreasing rank.

Remaining decisive target:

```text
CO-TICKET-37 NaturalFrontierRankOrPointwiseExceptionElimination
```

Proof boundary:

```text
TICKET-36 does not prove or disprove any of the four open problems. It closes a methodological loophole: aggregate evidence is not enough. The next proof attempt must synthesize a pointwise rank/exclusion theorem, or deliberately search for a sparse/null counterexample object that survives all aggregate tests.
```

### Ticket 37: Pointwise rank synthesis and weak-rank counterexamples

Generated artifact:

```text
data/open-problem/ticket37-pointwise-rank-synthesis-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-37-pointwise-zero-rank.json
data/open-problem/collatz/co-ticket-37-pointwise-rank-synthesis.json
data/open-problem/goldbach/gb-ticket-37-pointwise-cutoff-rank.json
data/open-problem/twin-prime/tp-ticket-37-exact-gap-rank.json
```

Aggregate verdict:

```text
pointwise_rank_synthesis_open_no_resolution
```

한국어 요약: TICKET-37은 TICKET-36의 natural frontier exit audit을 rank synthesis 문제로 바꿨다. 즉, "모든 자연수가 언젠가 null frontier에서 빠져나간다"를 직접 증명하기 위해 `exit_bits`를 `bit_length(n)` 같은 비순환 양으로 제한할 수 있는지 시험했다. 약한 후보는 반례로 버리고, 아직 살아남은 후보는 증명 대상 정리로만 남겼다.

Collatz bounded rank audit:

```text
tested odd n: 2,500,000 values, all odd n <= 5,000,000
base bits: 12
max probe bits: 320
resolved count: 2,500,000
unresolved count: 0
max exit bits: 228
max exit ratio to bit_length(n): 12.0
max exit slack over bit_length(n): 206
```

Linear rank falsification:

```text
exit_bits <= 8 * bit_length(n): 61 violations
exit_bits <= 9 * bit_length(n): 14 violations
exit_bits <= 10 * bit_length(n): 9 violations
exit_bits <= 11 * bit_length(n): 3 violations
exit_bits <= 12 * bit_length(n): 0 violations in the bounded sample
```

Candidate retained, but not proved:

```text
n >= 128 implies exit_bits <= 11 * bit_length(n); all tested n imply exit_bits <= 12 * bit_length(n)
```

Interpretation:

```text
This is a stronger and more useful target than raw mass decay: it is a pointwise-looking rank statement. But it is still bounded evidence. A proof needs a symbolic extension lemma showing that unseen adaptive frontier states cannot exceed the same piecewise linear rank.
```

Discarded Collatz routes:

```text
exit_bits <= 8 * bit_length(n) as a global rank
exit_bits <= 9 * bit_length(n) as a global rank
exit_bits <= 10 * bit_length(n) as a global rank
unqualified exit_bits <= 11 * bit_length(n) without finite seed handling
```

Retained Collatz routes:

```text
finite seed set plus exit_bits <= 11 * bit_length(n) for n >= 128 as a bounded theorem candidate
global exit_bits <= 12 * bit_length(n) as a weaker bounded theorem candidate
symbolic extension lemma over adaptive frontier states
```

Cross-problem transfer:

1. RH: a pointwise zero-exclusion rank is needed; finite-height verification and smoothed averages remain support only.
2. Goldbach: a pointwise even-cutoff rank is needed; density positivity cannot exclude a sparse exceptional set.
3. Twin Prime: an exact-gap-2 rank is needed; bounded-gap mass must not leak into wider gaps.
4. Collatz: a frontier-exit rank is needed; the bounded candidate is now concrete but still lacks the infinite extension theorem.

Remaining decisive target:

```text
CO-TICKET-38 SymbolicFrontierExtensionLemma
```

Proof boundary:

```text
TICKET-37 does not prove or disprove any of the four open problems. It improves the search by producing bounded counterexamples to weak rank candidates and by naming a sharper surviving theorem target. The next step is not more finite checking alone; it is a symbolic extension lemma or a new counterexample family that breaks the surviving rank.
```

### Ticket 38: Symbolic frontier extension and shortcut rejection

Generated artifact:

```text
data/open-problem/ticket38-symbolic-frontier-extension-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-38-symbolic-zero-extension.json
data/open-problem/collatz/co-ticket-38-symbolic-frontier-extension.json
data/open-problem/goldbach/gb-ticket-38-symbolic-cutoff-extension.json
data/open-problem/twin-prime/tp-ticket-38-symbolic-gap-extension.json
```

Aggregate verdict:

```text
symbolic_frontier_extension_open_no_resolution
```

한국어 요약: TICKET-38은 TICKET-37에서 살아남은 “점별 rank” 후보를 실제 증명으로 끌어올리기 위해 필요한 symbolic extension lemma를 직접 공격했다. 결론은 중요하지만 부정적이다. 고정된 비트 윈도우 안에서 모든 open frontier가 닫힌다는 단순 보조정리와, 하나의 scalar debt 함수가 모든 open edge에서 엄격히 감소한다는 보조정리는 bounded symbolic graph에서 반례성 edge를 대량으로 만들며 실패했다. 따라서 다음 증명 시도는 더 많은 finite checking이 아니라 phase/state-dependent potential 또는 명시적 surviving frontier family 분석이어야 한다.

Collatz symbolic frontier audit:

```text
frontier bits: 12..24
open edge count: 704,456
final frontier count: 317,095
max survival ratio: 0.944905286616
```

Scalar debt falsification:

```text
lambda = 1.45: 427,227 nondecreasing open edges
lambda = 1.50: 452,949 nondecreasing open edges
lambda = log2(3): 452,949 nondecreasing open edges
lambda = 1.60: 452,949 nondecreasing open edges
lambda = 1.70: 452,949 nondecreasing open edges
```

Discarded Collatz routes:

```text
bounded local closure from 12 bits to a fixed later bit depth
single scalar debt potential as a strict descent proof
aggregate mass contraction treated as a pointwise rank extension theorem
```

Retained Collatz routes:

```text
finite seed handling for stutter-like residues
phase/state-dependent potential instead of scalar debt alone
symbolic extension lemma combining aggregate contraction with pointwise rank
```

Cross-problem transfer:

1. RH: finite-height zero checks and averaged pressure are not enough. A proof needs a symbolic zero-exclusion certificate that rejects every hypothetical off-critical configuration.
2. Goldbach: almost-all or averaged representation pressure is not enough. A proof needs a stateful lower-bound certificate that remains positive for every even integer beyond a finite seed interval.
3. Twin Prime: bounded-gap pressure is not enough. A proof needs an exact-gap selector that prevents gap-2 mass from leaking into wider admissible gaps.
4. Collatz: aggregate mass decay and scalar debt are not enough. A proof needs a phase/state extension theorem or an explicit infinite counterexample object.

Remaining decisive target:

```text
CO-TICKET-39 PhaseStatePotentialSynthesis
```

Proof boundary:

```text
TICKET-38 does not prove or disprove any of the four open problems. It removes three tempting but false proof shortcuts and narrows the next viable proof attempt to a stateful symbolic extension lemma. A future proof must either synthesize a verified phase/state potential with no nondecreasing open cycle, or construct a coherent infinite survivor/counterexample object.
```

### Ticket 39: Phase/state potential synthesis

Generated artifact:

```text
data/open-problem/ticket39-phase-state-potential-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-39-phase-state-zero-potential.json
data/open-problem/collatz/co-ticket-39-phase-state-potential.json
data/open-problem/goldbach/gb-ticket-39-state-cone-potential.json
data/open-problem/twin-prime/tp-ticket-39-gap-leakage-potential.json
```

Aggregate verdict:

```text
phase_state_potential_open_no_resolution
```

한국어 요약: TICKET-39는 TICKET-38에서 실패한 scalar debt 방식을 버리고, phase/state quotient 위에서 실제 rank 후보를 합성했다. 거친 상태공간은 cycle이 남아서 폐기되었고, `phase_mod16_tail4_residue256` 상태공간은 finite window에서 DAG가 되어 topological rank를 갖는다. 더 긴 28비트 phase-wrap probe에서도 같은 후보는 sampled cycle 없이 유지되었다. 하지만 이것은 아직 Collatz 증명이 아니다. 빠진 정리는 “앞으로 나타날 모든 reachable state transition도 이 DAG 순서를 벗어나지 않는다”는 transition-closure theorem이다.

Collatz primary phase/state audit:

```text
frontier bits: 12..24
open edge count: 704,456
final frontier count: 317,095
```

State-family comparison:

```text
phase_mod4_tail2_debt: cycle detected, cyclic core 16,245 nodes
phase_mod8_tail4_residue64: cycle detected, cyclic core 63,270 nodes
phase_mod16_tail4_residue256: finite DAG candidate, max topological rank 12, edge violations 0
phase_mod32_tail6_residue1024: finite DAG candidate, max topological rank 12, edge violations 0
identity_residue_bits: acyclic but identity-like and not a uniform proof object
```

Deep phase-wrap probe:

```text
family: phase_mod16_tail4_residue256
frontier bits: 12..28
open edge count: 7,960,722
final frontier count: 3,618,400
status: phase_wrapped_finite_dag_candidate
max topological rank: 16
rank edge violations: 0
```

Discarded Collatz routes:

```text
coarse phase/state quotient after a quotient cycle is detected
identity-like residue+bits state as a uniform proof object
finite-window DAG rank treated as a Collatz proof without future transition closure
```

Retained Collatz routes:

```text
phase_mod16_tail4_residue256 quotient as the current finite theorem candidate
transition-closure theorem for every future reachable phase/state edge
contrapositive search for a future wrap-around cycle or coherent infinite survivor state
```

Cross-problem transfer:

1. RH: replace scalar or averaged zero pressure with a closed finite zero-configuration quotient and positivity rank.
2. Goldbach: replace averaged representation margins with a finite error-cone quotient that keeps each even integer pointwise positive.
3. Twin Prime: replace bounded-gap pressure with an exact-gap leakage quotient that prevents mass from escaping into wider admissible gaps.
4. Collatz: replace scalar debt with a concrete phase/state DAG candidate, then prove closure or find a future state cycle.

Remaining decisive target:

```text
CO-TICKET-40 PhaseStateTransitionClosureOrCycleCounterexample
```

Proof boundary:

```text
TICKET-39 does not prove or disprove any of the four open problems. It is a stronger synthesis step than TICKET-38 because it produces a concrete finite rank candidate and separately rejects coarse cyclic quotients. The next step must either prove symbolic closure of the phase_mod16_tail4_residue256 transition system or find a reachable future cycle/counterexample state that defeats it.
```

### Ticket 40: Transition closure or cycle counterexample

Generated artifact:

```text
data/open-problem/ticket40-transition-closure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-40-zero-transition-closure.json
data/open-problem/collatz/co-ticket-40-transition-closure.json
data/open-problem/goldbach/gb-ticket-40-error-cone-transition-closure.json
data/open-problem/twin-prime/tp-ticket-40-gap-leakage-transition-closure.json
```

Aggregate verdict:

```text
transition_closure_open_no_resolution
```

한국어 요약: TICKET-40은 TICKET-39의 좋은 후보를 그대로 이어받아 “정말 닫힌 전이 정리로 승격 가능한가?”를 공격했다. 결과적으로 `phase_mod16_tail4_residue256` 상태가 branching label 자체는 안정적으로 결정하지만, exact child-state signature는 같은 parent state에서도 여러 방식으로 갈라진다. 따라서 deterministic finite transducer 방식의 증명은 버린다. 그러나 sampled nondeterministic transition relation은 26비트 extension probe까지 cycle 없이 유지되고 topological rank violation도 없었다. 그래서 남은 증명 목표는 결정적 전이가 아니라, 전역적으로 닫힌 비결정적 well-founded relation을 증명하거나 미래 reachable cycle을 찾아 반례 후보를 만드는 것이다.

Collatz primary closure audit:

```text
frontier bits: 12..24
parent instance count: 389,409
state count: 188,651
state edge count: 440,614
ambiguous label states: 0
ambiguous child-signature states: 39,077
max child signatures for one state: 34
deterministic exact-child closure: refuted_by_child_state_signature_collision
```

Collatz extension probe:

```text
frontier bits: 12..26
parent instance count: 1,294,925
state count: 413,343
state edge count: 1,340,093
final frontier count: 1,099,648
ambiguous label states: 0
ambiguous child-signature states: 97,019
sampled cycle detected: false
max topological rank: 14
rank edge violations: 0
```

Discarded Collatz routes:

```text
deterministic exact-child finite transducer for phase_mod16_tail4_residue256
finite-window acyclic rank treated as a global Collatz proof
state quotients that do not state how all future reachable transitions are closed
```

Retained Collatz routes:

```text
label-level closure as a possible symbolic lemma, not yet a theorem
nondeterministic acyclic transition relation with sampled topological rank
contrapositive search for a future reachable cycle or escaping survivor state
```

Cross-problem transfer:

1. RH: split a zero-exclusion route into deterministic zero-state closure, nondeterministic positivity-state rank, and explicit off-critical zero/cycle counterexample targets.
2. Goldbach: split an error-cone route into deterministic error update rejection, nondeterministic pointwise positivity rank, and exceptional even-integer counterexample search.
3. Twin Prime: split an exact-gap route into deterministic leakage rejection, nondeterministic exact-gap residual rank, and last-twin absorbing-cycle search.
4. Collatz: reject deterministic child-state closure while retaining a nondeterministic acyclic rank candidate.

Remaining decisive target:

```text
CO-TICKET-41 SymbolicNondeterministicClosureOrReachableCycle
```

Proof boundary:

```text
TICKET-40 does not prove or disprove any of the four open problems. It is useful because it removes a specific false promotion path: a finite sampled rank cannot be treated as a deterministic closed transducer. The next step must either prove symbolic closure of the nondeterministic transition relation or find a reachable future cycle/counterexample state.
```

### Ticket 41: Rank escape normalization

Generated artifact:

```text
data/open-problem/ticket41-rank-escape-normalization-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-41-parametric-zero-state-normalization.json
data/open-problem/collatz/co-ticket-41-rank-escape-normalization.json
data/open-problem/goldbach/gb-ticket-41-parametric-error-cone-normalization.json
data/open-problem/twin-prime/tp-ticket-41-parametric-gap-leakage-normalization.json
```

Aggregate verdict:

```text
rank_escape_normalization_open_no_resolution
```

한국어 요약: TICKET-41은 TICKET-40의 남은 길을 더 정밀하게 검토했다. 핵심 수정은 `phase_mod16_tail4_residue256`를 전역 finite quotient처럼 부르면 안 된다는 점이다. 이 state에는 `prefix_length`, `consumed_bits`, `rounded_debt` 같은 성장 좌표가 들어가므로 horizon을 늘리면 새 좌표와 새 edge가 계속 생긴다. 따라서 고정된 finite-window DAG는 증명 객체가 될 수 없다. 남는 길은 더 큰 계산이 아니라, 성장 좌표를 포함하는 parametric symbolic transition schema와 well-founded measure를 증명하거나, 그 schema 안에서 nondecreasing cycle 또는 escaping coordinate ray를 찾는 것이다.

Collatz snapshots:

```text
12..24: nodes 282,660, edges 440,614, sinks 101,810, distinct coordinates 1,197, max rank 12
12..25: nodes 413,343, edges 688,432, sinks 145,873, distinct coordinates 1,347, max rank 13
12..26: nodes 590,519, edges 1,049,993, sinks 197,544, distinct coordinates 1,524, max rank 14
```

Fixed-relation escape:

```text
24 -> 25: new edges 247,818, reopened previous sinks 86,620, new coordinates 150
25 -> 26: new edges 361,561, reopened previous sinks 125,505, new coordinates 177
24 -> 26 total distinct coordinate delta: 327
```

Discarded Collatz routes:

```text
fixed finite-window DAG as a global proof object
phase_mod16_tail4_residue256 described as a global finite quotient
rank values computed on a horizon before checking future sink reopening
```

Retained Collatz routes:

```text
parametric symbolic transition schema over phase, tail, residue, and growth coordinates
well-founded ordinal or lexicographic measure that can absorb coordinate growth
counterexample search for reachable cycles, reopened sinks, or escaping coordinate rays
```

Cross-problem transfer:

1. RH: a finite-height zero-state graph must be replaced by a parametric zero-configuration normalization theorem.
2. Goldbach: a finite cutoff error-cone graph must be replaced by a parametric error-cone transition theorem for all large even integers.
3. Twin Prime: a finite exact-gap leakage graph must be replaced by a scale-parametric exact-gap residual theorem.
4. Collatz: a fixed sampled DAG must be replaced by symbolic templates plus a well-founded measure, or by an explicit escaping ray/cycle.

Remaining decisive target:

```text
CO-TICKET-42 ParametricTransitionTemplateOrNondecreasingCycle
```

Proof boundary:

```text
TICKET-41 does not prove or disprove any of the four open problems. It corrects a finite-quotient overstatement and gives a concrete counterexample to fixed finite-window closure. A future proof must normalize the growing coordinates symbolically, while a future disproof route would be a reachable nondecreasing cycle or escaping coordinate ray inside that normalized system.
```

### Ticket 42: Parametric transition template lab

Generated artifact:

```text
data/open-problem/ticket42-parametric-transition-template-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-42-parametric-zero-template.json
data/open-problem/collatz/co-ticket-42-parametric-transition-template.json
data/open-problem/goldbach/gb-ticket-42-parametric-error-template.json
data/open-problem/twin-prime/tp-ticket-42-parametric-gap-template.json
```

Aggregate verdict:

```text
parametric_template_open_no_resolution
```

한국어 요약: TICKET-42는 TICKET-41에서 남긴 숙제인 parametric transition schema를 실제로 만들기 시작한 단계다. 고정된 finite-window graph 대신 `phase`, valuation tail, residue, next valuation을 template node로 두고, `prefix_length`, `consumed_bits`, debt를 성장 좌표로 따로 기록했다. 중요한 결과는 예상과 달리 26-bit 표본에서 template cycle을 찾지 못했다는 점이다. 이것은 proof route를 살리는 좋은 신호지만, 증명은 아니다. 이유는 같은 template edge가 서로 다른 `delta_prefix`, `delta_consumed`, `delta_debt`를 가질 수 있기 때문이다. 따라서 다음 증명 의무는 bounded acyclicity가 아니라, template edge가 어떤 큰 cylinder에서 실제로 lift되는지와 그때 성장 좌표가 항상 well-founded measure를 감소시키는지 증명하는 것이다.

Collatz template families:

```text
phase16_tail2_residue64_v8: nodes 14,357, edges 126,994, ambiguous template edges 8,218, sampled cycles 0
phase16_tail3_residue128_v12: nodes 59,388, edges 352,790, ambiguous template edges 6,887, sampled cycles 0
phase16_tail4_residue256_v16: nodes 165,812, edges 710,227, ambiguous template edges 5,393, sampled cycles 0
phase16_tail4_residue256_vexact: nodes 165,841, edges 710,241, ambiguous template edges 5,393, sampled cycles 0
```

Raw frontier pressure:

```text
raw open edges processed: 2,392,525
raw nondecreasing debt edges: 1,510,781
sampled template cycle status: no_sampled_template_cycle_found_through_26_bits
total ambiguous template edge count across families: 25,891
```

Parametric update schema:

```text
phase' = phase + 1 mod 16
prefix_length' = prefix_length + delta_prefix
consumed_bits' = consumed_bits + delta_consumed
debt' = debt + delta_prefix * log2(3) - delta_consumed
tail' = suffix(tail plus newly consumed valuation word)
```

Discarded Collatz routes:

```text
absence of sampled template cycles treated as a Collatz proof
template cycle interpreted directly as a Collatz counterexample without a compatible lift
finite template edge treated as deterministic without delta guards for prefix, consumed bits, and debt
larger bounded horizon treated as a substitute for parametric lift closure
```

Retained Collatz routes:

```text
parametric transition schema with prefix_length, consumed_bits, and debt deltas
cycle-lift search for a compatible infinite nondecreasing template ray
well-founded measure that uses growth coordinates, not only the finite template node
```

Interpretation:

1. The sampled template graph did not refute the proof route through 26 bits.
2. The sampled graph also does not prove Collatz, because future lift closure is still missing.
3. Ambiguous coordinate deltas show why a finite template node alone is not a deterministic transition theorem.
4. A real counterexample route would need a compatible infinite lift of a nondecreasing cycle, not only a quotient cycle.

Remaining decisive target:

```text
CO-TICKET-43 LiftConstraintSolverOrWellFoundedMeasure
```

Proof boundary:

```text
TICKET-42 does not prove or disprove any of the four open problems. It preserves a promising bounded template-rank route because no sampled template cycle was found, but it rejects the shortcut from bounded acyclicity to truth. A proof now needs parametric lift closure plus a well-founded growth-coordinate measure; a disproof route needs a compatible infinite lift of a nondecreasing cycle.
```

### Ticket 43: Lift constraint and measure lab

Generated artifact:

```text
data/open-problem/ticket43-lift-constraint-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-43-zero-lift-measure.json
data/open-problem/collatz/co-ticket-43-lift-constraint-measure.json
data/open-problem/goldbach/gb-ticket-43-error-lift-measure.json
data/open-problem/twin-prime/tp-ticket-43-gap-lift-measure.json
```

Aggregate verdict:

```text
lift_constraint_measure_open_no_resolution
```

한국어 요약: TICKET-43은 TICKET-42의 약점을 직접 고친다. TICKET-42에서는 26-bit 표본에서 template cycle이 없었기 때문에 "best cycle을 lift한다"는 다음 단계가 논리적으로 맞지 않았다. TICKET-43은 방향을 바꿔, `M(template, debt) = scale * topological_rank(template) + debt` 형태의 bounded measure가 실제 샘플 template edge에서 감소하는지 검사하고, 그 측도가 horizon 확장에서도 닫히는지를 확인한다.

Collatz lift snapshots:

```text
24 bits: nodes 97,806, edges 322,907, max rank 12, scale 11, min margin 0.584962500721
25 bits: nodes 128,371, edges 480,873, max rank 13, scale 11, min margin 0.584962500721
26 bits: nodes 165,841, edges 710,241, max rank 14, scale 11, min margin 0.584962500721
```

Important bounded result:

```text
sampled measure status: sampled_measure_decreases_on_all_template_edges
candidate: M(template, debt) = scale * topological_rank(template) + debt
scale: 11
minimum sampled margin: 0.584962500721
invalid rank-gap edges: 0
```

Important obstruction:

```text
24 -> 25: new template edges 157,966, previous ranks changed 94,080, old-measure unknown-rank edges 157,966
25 -> 26: new template edges 229,368, previous ranks changed 124,027, old-measure unknown-rank edges 229,368
closure status: rank_lift_not_closed_under_horizon_extension
```

Interpretation:

1. The debt-only route is refuted as a proof strategy because many raw edges have nondecreasing debt.
2. A stronger bounded certificate exists in the sampled graph: `scale * rank + debt` decreases on every sampled template edge through 26 bits.
3. This is still not a Collatz proof, because the rank is recomputed when the horizon grows; 25 -> 26 changes 124,027 previous-node ranks and introduces 229,368 new template edges whose ranks were unknown to the old measure.
4. The next theorem is therefore a lift-closure theorem: every future cylinder lift must preserve the template relation and a horizon-independent well-founded measure, or the search must find a future edge that violates all finite-rank extensions.

English summary: TICKET-43 upgrades the Collatz track from finite acyclicity to finite measure synthesis. The sampled measure is a real bounded certificate, not a proof. The remaining infinite obligation is to replace horizon-specific topological rank with a lift-stable rank or another well-founded measure whose decrease can be proved for every future cylinder lift.

Remaining decisive target:

```text
CO-TICKET-44 HorizonIndependentLiftRankOrCounteredge
```

Proof boundary:

```text
TICKET-43 does not prove or disprove any of the four open problems. It improves the proof attempt by producing a bounded decreasing measure, and it improves the counterexample attempt by identifying exactly where future lift edges could break finite-rank extensions.
```

### Ticket 44: Feature-measure counteredge lab

Generated artifact:

```text
data/open-problem/ticket44-feature-measure-counteredge-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-44-zero-feature-counteredge.json
data/open-problem/collatz/co-ticket-44-feature-measure-counteredge.json
data/open-problem/goldbach/gb-ticket-44-margin-feature-counteredge.json
data/open-problem/twin-prime/tp-ticket-44-gap-feature-counteredge.json
```

Aggregate verdict:

```text
feature_measure_counteredge_open_no_resolution
```

한국어 요약: TICKET-44는 TICKET-43에서 남은 가장 위험한 논리적 틈을 공격한다. TICKET-43의 `scale * sampled_rank + debt` 측도는 26-bit 표본에서는 모든 template edge에서 감소하지만, 그 rank는 horizon을 늘릴 때 다시 계산된다. 따라서 이것을 무한 증명으로 승격하려면 horizon에 의존하지 않는 명시적 feature measure가 필요하다. TICKET-44는 여러 feature family를 제안하고, 각 family가 실제 edge에서 감소 측도로 작동하는지 counterexample-guided 방식으로 검사했다. 결과적으로 `debt_only_constant`는 390,494개의 zero-delta refuter로 정확히 반박되었다. 더 풍부한 feature family들은 bounded affine search에서 인증되지 않았지만, 이것은 불가능성 증명이 아니라 현재 feature와 solver의 한계다. 살아남은 방향은 explicit counteredge extraction과 horizon-independent symbolic rank theorem이다.

English summary: TICKET-44 attacks the remaining promotion gap in TICKET-43. A sampled rank table is a useful bounded certificate, but it is not an invariant proof object if the rank changes under horizon extension. TICKET-44 therefore searches for explicit horizon-independent feature measures and records exact counteredges when a candidate family cannot work. The debt-only control is exactly refuted; richer compact affine feature families remain uncertified rather than impossible. This narrows the proof route to a symbolic rank or measure whose decrease is stable under every future cylinder lift.

Collatz feature-measure audit:

```text
template family: phase16_tail4_residue256_vexact
max bits: 26
template nodes: 165,841
template edges: 710,241
raw open edges processed: 2,392,525
exactly refuted feature families: 1
not certified or still open feature families: 4
```

Feature trial summary:

```text
debt_only_constant:
  status: exact_zero_delta_counteredge_refutes_feature_measure
  feature dimension: 1
  unique constraints: 1
  positive-debt pressure edges: 390,494
  zero-delta refuters: 390,494
  affine violations: 1

phase_tail_scalar:
  status: not_certified_by_bounded_affine_search
  feature dimension: 7
  unique constraints: 4,748
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 2,608

numeric_template_coordinates:
  status: not_certified_by_bounded_affine_search
  feature dimension: 7
  unique constraints: 23,067
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 12,290

residue_binary_coordinates:
  status: not_certified_by_bounded_affine_search
  feature dimension: 14
  unique constraints: 23,067
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 12,290

phase_residue_onehot_tail_numeric:
  status: not_certified_by_bounded_affine_search
  feature dimension: 37
  unique constraints: 74,629
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 1,126
```

Preserved TICKET-43 baseline:

```text
sampled rank-debt measure: sampled_measure_decreases_on_all_template_edges
scale: 11
minimum sampled margin: 0.584962500721
invalid rank-gap edges: 0
```

Horizon-extension obstruction:

```text
25 -> 26 new template edges: 229,368
25 -> 26 changed previous-node ranks: 124,027
25 -> 26 old-measure unknown-rank edges: 229,368
closure status: rank_lift_not_closed_under_horizon_extension
```

Discarded Collatz routes:

```text
debt-only descent as a proof measure
observed-node rank table treated as a horizon-independent theorem
bounded affine feature search treated as an impossibility proof for richer nonlinear measures
```

Retained Collatz routes:

```text
exact counteredge extraction for every proposed feature family
horizon-independent symbolic rank or ordinal-valued measure
future-lift theorem proving that every cylinder edge preserves the symbolic decrease
```

Cross-problem transfer:

1. RH: a zero-exclusion feature score must survive exact off-critical zero-lift counteredge extraction before it can be promoted to a positive-kernel theorem.
2. Goldbach: an error-margin feature score must survive exceptional-residue counteredges before it can be promoted to an explicit positivity theorem.
3. Twin Prime: an exact-gap feature score must survive leakage counteredges before it can be promoted to an infinite bounded-gap theorem.
4. Collatz: a finite rank table must be replaced by a symbolic rank or measure, or by a future edge that violates every proposed symbolic measure.

Remaining decisive target:

```text
CO-TICKET-45 SymbolicRankClauseOrFutureCounteredge
```

Proof boundary:

```text
TICKET-44 does not prove or disprove any of the four open problems. It improves the proof attempt by exactly refuting weak horizon-independent measures, preserving the bounded rank-table certificate only as evidence, and isolating the next proof obligation: a symbolic, horizon-stable rank or an explicit future counteredge against it.
```

### Ticket 45: Symbolic rank clause lab

Generated artifact:

```text
data/open-problem/ticket45-symbolic-rank-clause-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-45-symbolic-zero-clause.json
data/open-problem/collatz/co-ticket-45-symbolic-rank-clause.json
data/open-problem/goldbach/gb-ticket-45-symbolic-margin-clause.json
data/open-problem/twin-prime/tp-ticket-45-symbolic-gap-clause.json
```

Aggregate verdict:

```text
symbolic_rank_clause_open_no_resolution
```

한국어 요약: TICKET-45는 TICKET-44에서 남은 목표인 `horizon-independent symbolic rank`를 실제로 압박한다. 핵심 아이디어는 상태들을 symbolic clause로 묶고, nonnegative-debt pressure edge가 같은 clause 안에서 돌거나 pressure graph에 cycle을 만들면 그 clause family는 어떤 scalar rank를 주어도 증명 측도가 될 수 없다는 것이다. 가장 중요한 발견은 `phase_only`가 26-bit와 27-bit에서는 scale 11로 통과하지만, 28-bit에서 phase `11 -> 12` edge가 추가되면서 modulo-16 pressure cycle이 닫힌다는 점이다. 따라서 phase-only rank는 좋은 후보처럼 보이다가 미래 horizon에서 정확히 폐기된다. 이것은 Collatz 반례가 아니라 phase-only 증명 전략의 반례다.

English summary: TICKET-45 turns the remaining symbolic-rank obligation into a counterexample-guided clause test. A symbolic clause family is rejected when nonnegative-pressure edges force a same-clause loop or a pressure cycle. The phase-only family is especially useful as a diagnostic: it passes through 26 and 27 bits, then fails at 28 bits when a new `11 -> 12` pressure edge closes the phase cycle. This refutes the phase-only proof route, not Collatz.

Collatz symbolic-clause audit:

```text
26-bit template nodes: 165,841
26-bit template edges: 710,241
raw open edges processed: 2,392,525
26-bit exactly refuted clause families: 0
future-wrap refuted clause families: 1
sampled clause candidates through 26 bits: 1
```

Clause trial summary at 26 bits:

```text
phase_only:
  status: sampled_symbolic_clause_rank_found_not_proof
  clauses: 15
  pressure clause edges: 14
  selected scale: 11
  minimum sampled margin: 0.584962500721

phase_tail_mass_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 2,413
  pressure clause edges: 25,530

phase_tail_residue16_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 46,885
  pressure clause edges: 149,685

phase_tail_residue64_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 90,008
  pressure clause edges: 248,120

phase_tail_residue256_vexact:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 165,841
  pressure clause edges: 390,494
```

Phase-wrap counteredge:

```text
probe: 27 -> 28 bits
status: pressure_cycle_counterexample_refutes_clause_rank
new pressure clause edge: [11] -> [12]
max delta debt: 7.415037499279
edge count represented by this clause edge: 3,618,400
example parent template: [11,[1,1,1,9],191,1]
example child template: [12,[1,1,1,1],191,12]
```

Interpretation:

1. The phase-only rank looked promising because the observed phase chain had not wrapped yet.
2. Once the 28-bit horizon exposes the `11 -> 12` pressure edge, phase-only rank would require a strict decrease around a full modulo-16 cycle, which is impossible.
3. Richer finite clause families were not certified by the current pressure-rank interval. This is not an impossibility proof for every nonlinear or ordinal-valued measure.
4. The observed exact-template rank remains a bounded ceiling certificate, but its clause and pressure-edge sets change under horizon extension.

Discarded Collatz routes:

```text
phase-only rank as a Collatz proof measure
coarse symbolic quotients promoted before phase-wrap testing
observed exact-template rank table treated as an infinite theorem
```

Retained Collatz routes:

```text
pressure-cycle extraction for proposed symbolic clauses
stable symbolic family whose pressure graph remains acyclic under future lifts
parametric clause grammar plus a proof that every future lifted edge keeps a nonempty scale interval
```

Cross-problem transfer:

1. RH: a symbolic zero-clause grammar must survive off-critical pressure-cycle extraction before it can become a zero-free theorem.
2. Goldbach: a symbolic margin-clause grammar must survive exceptional-residue pressure cycles before it can become a positivity theorem.
3. Twin Prime: a symbolic exact-gap grammar must survive leakage pressure cycles before it can become an exact gap-2 lower-bound theorem.
4. Collatz: any low-dimensional symbolic rank must be tested not only at the current horizon but also at the first horizon where its quotient cycles can close.

Remaining decisive target:

```text
CO-TICKET-46 StableClauseGrammarOr27PlusCounteredge
```

Proof boundary:

```text
TICKET-45 does not prove or disprove any of the four open problems. It improves the proof attempt by finding a concrete future-horizon counteredge against the tempting phase-only symbolic rank, and it improves the search protocol by requiring every proposed symbolic clause grammar to survive pressure-cycle extraction before formal promotion.
```

### Ticket 46: Stable clause grammar lab

Generated artifact:

```text
data/open-problem/ticket46-stable-clause-grammar-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-46-stable-zero-grammar.json
data/open-problem/collatz/co-ticket-46-stable-clause-grammar.json
data/open-problem/goldbach/gb-ticket-46-stable-margin-grammar.json
data/open-problem/twin-prime/tp-ticket-46-stable-gap-grammar.json
```

Aggregate verdict:

```text
stable_clause_grammar_restricted_no_go_open_no_resolution
```

한국어 요약: TICKET-46은 TICKET-45에서 남은 질문을 더 강하게 압박한다. TICKET-45는 `phase_only`가 28-bit에서 깨진다는 것을 보였지만, 더 정교한 clause grammar들이 28-bit wrap 이후에도 버틸 수 있는지는 남아 있었다. TICKET-46은 같은 28-bit horizon에서 다섯 family 모두를 다시 검사했고, `phase_only`, `phase_tail_mass_vbucket`, `phase_tail_residue16_vbucket`, `phase_tail_residue64_vbucket`, `phase_tail_residue256_vexact` 전부가 nonnegative-pressure cycle을 갖는다는 결과를 얻었다. 따라서 이 다섯 종류의 finite template-local scalar clause-rank 증명 전략은 제한된 의미에서 모두 폐기된다. 이것은 Collatz의 반례도 아니고 Collatz 증명도 아니다. 정확한 결론은 “현재 테스트한 scalar clause-rank proof route는 더 이상 남아 있지 않다”이다.

English summary: TICKET-46 strengthens the TICKET-45 obstruction. TICKET-45 showed that the phase-only rank fails at the first visible modulo-16 wrap. TICKET-46 reruns the clause-rank stress test at the same 28-bit horizon for all five TICKET45 families. Every tested finite template-local scalar clause grammar becomes pressure-cyclic, including the exact observed-template table. This is a restricted no-go theorem for those proof routes, not a proof or disproof of Collatz.

Collatz stable-clause audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
raw open edges processed: 7,960,722
tested clause families: 5
28-bit refuted clause families: 5
28-bit stable clause families: 0
```

28-bit stress result:

```text
phase_only:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 16
  pressure clause edges: 16
  new pressure edges from 27->28: 1

phase_tail_mass_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 2,960
  pressure clause edges: 37,948
  new pressure edges from 27->28: 6,042

phase_tail_residue16_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 70,498
  pressure clause edges: 261,971
  new pressure edges from 27->28: 58,393

phase_tail_residue64_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 138,390
  pressure clause edges: 448,510
  new pressure edges from 27->28: 105,553

phase_tail_residue256_vexact:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 261,367
  pressure clause edges: 741,372
  new pressure edges from 27->28: 187,086
```

First shared phase-wrap pressure edge:

```text
edge: [11] -> [12]
max delta debt: 7.415037499279
edge count represented in phase-only quotient: 3,618,400
example parent template: [11,[1,1,1,9],191,1]
example child template: [12,[1,1,1,1],191,12]
```

Escape-coordinate audit:

1. `unwrapped_phase_epoch`: 현재 template key에는 phase modulo 16만 있으므로, unwrapped epoch는 외부 lift depth나 path history를 끌어온다. 이 좌표는 아직 finite horizon-independent grammar가 아니다.
2. `depth_or_max_bits_bucket`: bounded horizon을 기억하면 cycle을 깨는 것처럼 보일 수 있지만, 29-bit, 30-bit로 늘릴 때 다시 커지는 좌표라면 증명 객체가 아니다.
3. `exact_observed_template_table`: 26-bit에서는 bounded ceiling certificate였지만, 28-bit에서는 새 clause와 pressure edge가 대량으로 추가되고 pressure graph도 cyclic이 된다.

Discarded Collatz routes:

```text
phase-only scalar clause rank
coarse tail-mass scalar clause rank
low-residue scalar clause rank
exact observed-template scalar clause rank treated as an infinite theorem
horizon-depth or max_bits escape coordinate promoted before a well-founded theorem is proved
```

Retained Collatz routes:

```text
ordinal-valued or stateful measure with a template-local update rule
explicit 29-bit/30-bit counteredge extraction against any proposed compact update rule
a formal theorem that the measure is fixed before horizon extension and decreases under every future lift
```

Cross-problem transfer:

1. RH: a zero grammar repaired by a height-dependent coordinate is not enough; it must become a compact positive-kernel theorem or yield an off-critical pressure counterexample.
2. Goldbach: a margin grammar repaired by cutoff-dependent constants is not enough; constants must be fixed before extension or produce an exceptional-residue counterexample.
3. Twin Prime: an exact-gap selector repaired by range-dependent leakage coordinates is not enough; fixed selector mass must survive extension or produce a leakage cycle.
4. Collatz: the next real proof route is no longer scalar clause-rank; it must be ordinal/stateful and horizon-independent.

Remaining decisive target:

```text
CO-TICKET-47 OrdinalStatefulMeasureOr29BitCounteredge
```

Proof boundary:

```text
TICKET-46 does not prove or disprove any of the four open problems. It proves a restricted no-go result for the tested finite scalar template-local clause-rank proof routes, and it moves the Collatz proof attempt to a sharper target: a horizon-independent ordinal/stateful measure or a future counteredge against such a measure.
```

### Ticket 47: Periodic state lasso lab

Generated artifact:

```text
data/open-problem/ticket47-periodic-state-lasso-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-47-zero-lasso-automaton.json
data/open-problem/collatz/co-ticket-47-periodic-state-lasso.json
data/open-problem/goldbach/gb-ticket-47-margin-lasso-automaton.json
data/open-problem/twin-prime/tp-ticket-47-gap-lasso-automaton.json
```

Aggregate verdict:

```text
periodic_state_lasso_restricted_no_go_open_no_resolution
```

한국어 요약: TICKET-47은 TICKET-46의 scalar clause-rank 폐기 결과를 한 단계 더 밀어붙인다. 단순 scalar rank가 안 되면 bounded memory를 붙인 stateful automaton으로 살릴 수 있는지 묻는다. 28-bit exact-template pressure graph에서 16-edge positive-debt lasso를 추출했고, zero-memory 및 last-1부터 last-4 edge-signature memory까지 모두 한 period 뒤 같은 expanded state로 되돌아오는 것을 확인했다. 따라서 이 bounded suffix-memory 수리 계열은 strict well-founded descent가 될 수 없다. 하지만 이것도 Collatz 반례는 아니다. 이 cycle은 abstract template pressure relation의 lasso이며, 하나의 실제 Collatz orbit으로 reachable하다는 증명은 아직 없다.

English summary: TICKET-47 upgrades the TICKET-46 scalar-rank obstruction to a bounded-memory stateful obstruction. It extracts a 16-edge positive-debt lasso from the 28-bit exact-template pressure graph. Zero-memory and last-1 through last-4 edge-signature memory automata all return to the same expanded state after one lasso period, so none of these bounded suffix-memory repairs can support a strict well-founded descent. This is still not a Collatz counterexample: the lasso is an abstract template-pressure object, not a certified single reachable orbit.

Collatz periodic-lasso audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
28-bit pressure edges: 741,372
raw open edges processed: 7,960,722
lasso cycle edges: 16
unique edge symbols: 16
total max delta debt over period: 5.84962500721
tested bounded-memory automata: 5
refuted bounded-memory automata: 5
```

Tested stateful repairs:

```text
zero_memory_pressure_lasso: refuted_by_periodic_pressure_lasso
last1_edge_signature: refuted_by_periodic_pressure_lasso
last2_edge_signature: refuted_by_periodic_pressure_lasso
last3_edge_signature: refuted_by_periodic_pressure_lasso
last4_edge_signature: refuted_by_periodic_pressure_lasso
```

First lasso edge:

```text
[0,[1,1,1,1],103,1] -> [1,[1,1,1,1],103,1]
symbol: dir=low|label=both_open|dp=1|dc=1|phase=0->1|v=1->1
max delta debt: 0.584962500721
```

Discarded Collatz routes:

```text
zero-memory exact-template pressure rank
bounded suffix-memory stateful repair using last 1-4 pressure-edge signatures
any proof object that silently treats a periodic bounded-memory lasso as a strict descent
```

Retained Collatz routes:

```text
prove that the abstract pressure lasso is unreachable by any concrete Collatz lift path
synthesize arbitrary small finite-state automata and refute them by CEGIS rather than only suffix memory
define a genuinely ordinal/stateful measure whose state is fixed before horizon extension and is not bounded suffix memory
push surviving automata to 29-bit/30-bit reachability stress
```

Cross-problem transfer:

1. RH: a bounded zero-state memory that repeats on an off-critical kernel lasso cannot prove zero exclusion.
2. Goldbach: a bounded cutoff ledger that repeats on an exceptional-residue margin lasso cannot prove positivity.
3. Twin Prime: a bounded leakage memory that repeats on a wider-gap lasso cannot prove exact gap-2 infinitude.
4. Collatz: stateful repairs must now pass lasso reachability or arbitrary finite-automaton CEGIS, not just bounded suffix memory.

Remaining decisive target:

```text
CO-TICKET-48 AutomatonCEGISOr29BitReachability
```

Proof boundary:

```text
TICKET-47 does not prove or disprove any of the four open problems. It proves a restricted no-go result for bounded suffix-memory repairs over the 28-bit abstract template pressure lasso. It does not prove the lasso is a single reachable Collatz orbit and does not refute arbitrary finite automata or ordinal-valued measures.
```

### Ticket 48: Automaton reachability lab

Generated artifact:

```text
data/open-problem/ticket48-automaton-reachability-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-48-kernel-period-map.json
data/open-problem/collatz/co-ticket-48-automaton-reachability.json
data/open-problem/goldbach/gb-ticket-48-margin-period-map.json
data/open-problem/twin-prime/tp-ticket-48-gap-period-map.json
```

Aggregate verdict:

```text
automaton_reachability_split_open_no_resolution
```

한국어 요약: TICKET-48은 TICKET-47의 약한 고리를 둘로 나눴다. 첫째, 추상 template-pressure lasso가 반복 가능하다고 가정하면 bounded suffix-memory뿐 아니라 임의의 고정된 유한상태 total deterministic update도 strict descent를 만들 수 없다. 한 period가 finite state set 위의 함수 \(F:S\to S\)를 만들고, \(F\)를 반복하면 어떤 state가 다시 나타나므로 template/state expanded quotient에서 finite directed cycle이 생기기 때문이다. 둘째, 이 추상 lasso가 실제 Collatz residue lift path로 이어지는지를 별도 bounded probe로 검사했다. 28-bit frontier 안에서는 start-template candidate 4개를 찾았고, 그중 concrete positive step은 2단계까지 이어졌지만 3단계에서 surviving transition이 0개가 되어 한 period도 완성하지 못했다.

English summary: TICKET-48 separates the abstract automaton obstruction from concrete Collatz reachability. Conditional on the repeatable abstract lasso, any fixed finite total deterministic state update induces a one-period map on a finite state set, and iterating that map eventually repeats the expanded template/state while the abstract lasso carries positive pressure debt. A bounded concrete lift probe then checks whether the same lasso can be realized by compatible residues. It finds four start-template candidates and two positive concrete steps, but no surviving transition at the third step and no complete positive-pressure period.

Collatz automaton/reachability audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
28-bit pressure edges: 741,372
raw open edges processed: 7,960,722
lasso cycle edges: 16
total max delta debt over abstract period: 5.84962500721
finite-state period-map rows: 9
start-template candidates in bounded frontier: 4
concrete lasso steps completed: 3 checked, 0 survivors at step 3
best concrete partial depth: 2
best concrete partial debt: 1.169925001442
```

Discarded Collatz routes:

```text
any fixed finite total deterministic state repair over the repeatable abstract lasso
any finite quotient proof that silently treats the abstract lasso as a strict descent object
any claim that TICKET47/TICKET48 already supplies a Collatz counterexample without concrete infinite reachability
```

Retained Collatz routes:

```text
prove the TICKET47/TICKET48 lasso family is unreachable by all concrete residue lifts
find a concrete periodic lift witness at a larger horizon and test whether it repeats unboundedly
define a genuinely ordinal or unbounded-state measure fixed before horizon extension
turn the reachability probe into a symbolic preimage automaton rather than relying on sampled starts
```

Cross-problem transfer:

1. RH: a finite kernel-state repair cannot certify zero exclusion if a repeatable off-critical zero lasso remains reachable.
2. Goldbach: a finite cutoff-state repair cannot certify positivity if an exceptional-residue margin lasso remains reachable.
3. Twin Prime: a finite selector-state repair cannot certify exact gap-2 infinitude if wider-gap leakage lassos remain reachable.
4. Collatz: the next target is not another finite automaton wrapper; it is reachability exclusion, concrete periodic lift extraction, or a non-finite-state descent theorem.

Remaining decisive target:

```text
CO-TICKET-49 SymbolicReachabilityExclusionOrConcretePeriodicLift
```

Proof boundary:

```text
TICKET-48 does not prove or disprove any of the four open problems. It proves a conditional abstract no-go for fixed finite total deterministic state repairs over the extracted Collatz template lasso and reports a bounded concrete reachability failure through one full period. The unresolved theorem is still infinite: either exclude the lasso family for all future residue lifts, or produce a certified unbounded concrete lift witness.
```

### Ticket 49: Symbolic preimage obstruction lab

Generated artifact:

```text
data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-49-zero-kernel-preimage.json
data/open-problem/collatz/co-ticket-49-symbolic-preimage-obstruction.json
data/open-problem/goldbach/gb-ticket-49-residue-margin-preimage.json
data/open-problem/twin-prime/tp-ticket-49-gap-selector-preimage.json
```

Aggregate verdict:

```text
symbolic_preimage_obstruction_open_no_resolution
```

한국어 요약: TICKET-49는 TICKET-48의 concrete reachability 실패를 “왜 실패했는가”까지 좁힌다. 16-bit phase-compatible start template `[0,[1,1,1,1],103,1]`을 만족하는 residue는 정확히 4개다. forced-low lasso prefix에서 이들은 step 1 뒤 2개, step 2 뒤 1개, step 3 뒤 0개가 된다. 마지막 생존 residue는 세 번째 phase에서 phase, tail word, residue mod 256은 맞지만 `next_valuation = 5`가 되어, lasso가 요구하는 `next_valuation = 1`과 충돌한다.

English summary: TICKET-49 turns the TICKET-48 reachability failure into a coordinate-level obstruction. The exact 16-bit phase-compatible start set has four residues. Along the forced-low lasso prefix, the survivor counts are 4 -> 2 -> 1 -> 0. The unique two-step survivor reaches the third phase with the correct phase, tail word, and residue mod 256, but with next valuation 5 rather than the lasso-required 1.

Collatz symbolic-preimage audit:

```text
start template: [0,[1,1,1,1],103,1]
start candidates: 26471, 28007, 34919, 48743
forced-low survivors: 4 -> 2 -> 1 -> 0
dead step: 3
obstruction coordinate: next_valuation
required third template: [3,[1,1,1,1],103,1]
observed third template on the unique survivor: [3,[1,1,1,1],103,5]
best partial depth: 2
best partial debt: 1.169925001442
```

Discarded Collatz routes:

```text
blindly rerunning larger frontier probes without naming the failed coordinate
claiming the abstract TICKET47/TICKET48 lasso is concrete after only two matching steps
treating finite-state or bounded-prefix failure as a Collatz proof
```

Retained Collatz routes:

```text
prove the next_valuation obstruction for every b == 0 mod 16 compatible lift
derive a symbolic preimage recurrence for the third low-prefix step
search for a higher-bit exception that changes next_valuation 5 back to 1
if such an exception exists, test whether it can complete and repeat the full lasso period
```

Cross-problem transfer:

1. RH: after a zero-kernel lasso attempt fails, identify the first failed kernel coordinate before proposing a larger automaton.
2. Goldbach: after a residue-margin lasso attempt fails, identify whether the obstruction is residue class, singular-series margin, or cutoff leakage.
3. Twin Prime: after a gap-selector lasso attempt fails, identify whether exact gap-2 mass fails at selector state or leakage class.
4. Collatz: the next theorem is now a next-valuation preimage theorem, not another finite-state wrapper.

Remaining decisive target:

```text
CO-TICKET-50 AllPhaseNextValuationPreimageOrHigherBitException
```

Proof boundary:

```text
TICKET-49 does not prove or disprove any of the four open problems. It identifies the first local coordinate that blocks the 16-bit Collatz lasso-prefix realization. The unresolved theorem is still infinite: prove the same next-valuation obstruction for every compatible modulus, or find a higher-bit exception and test whether it becomes an unbounded concrete lasso.
```

### Ticket 50: Phase-lift exception lab

Generated artifact:

```text
data/open-problem/ticket50-phase-lift-exception-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-50-zero-kernel-exception.json
data/open-problem/collatz/co-ticket-50-phase-lift-exception.json
data/open-problem/goldbach/gb-ticket-50-residue-margin-exception.json
data/open-problem/twin-prime/tp-ticket-50-gap-selector-exception.json
```

Aggregate verdict:

```text
phase_lift_exception_open_no_resolution
```

한국어 요약: TICKET-50은 TICKET-49의 16비트 장애물을 무시하지 않는다. 오히려 그 장애물을 전역 정리로 승격할 수 있는지 시험했고, 32비트 phase-compatible lift에서 반례를 찾았다. 즉 “모든 b == 0 mod 16에서 세 번째 low-prefix의 `next_valuation = 1`은 불가능하다”는 프로젝트 내부 후보 정리는 틀렸다. 대신 32비트에서 훨씬 강한 near-lasso 후보 2개가 발견됐다. 이들은 16개 lasso-prefix 템플릿 중 15개까지 따라가지만 마지막 phase에서 tail shift 또는 all_lift_descent로 실패한다.

English summary: TICKET-50 does not discard TICKET-49. It stress-tests the proposed all-phase extension and refutes that project-local candidate theorem at 32 bits. The same start template has 69,092 exact valuation-word matches, 8,684 four-consecutive-one low-lift exceptions, and two near-lasso witnesses that match 15 of the 16 lasso-prefix templates before terminal failure.

Exact Collatz audit:

```text
valuation-run lemma: r consecutive accelerated valuations equal 1 iff boundary x == -1 mod 2^(r+1)
16-bit start-template matches: 4
16-bit four-consecutive-one exceptions: 0
16-bit max lasso-prefix depth: 3
32-bit start-template matches: 69,092
32-bit four-consecutive-one exceptions: 8,684
32-bit max lasso-prefix depth: 15
32-bit depth counts: {1: 34,458; 2: 17,301; 3: 8,649; 4: 4,310; 5: 4,372; 15: 2}
```

Discarded Collatz route:

```text
the TICKET-49 all-phase next_valuation obstruction as stated
any proof route that treats the 16-bit obstruction as universal without checking higher phase-compatible lifts
```

Retained and strengthened Collatz routes:

```text
classify every 48-bit child of the two 32-bit depth-15 near-lasso residues
prove the phase-15 terminal obstruction for all descendants, or find a child that completes the final lasso template
if a full lasso completion appears, replay it as a concrete periodic-lift candidate before making any counterexample claim
```

Cross-problem transfer:

1. RH: if a local zero-kernel obstruction fails at a higher height, promote the zero-kernel exception and classify the terminal coordinate.
2. Goldbach: if a residue-margin obstruction fails at a larger cutoff, promote the exceptional even integer or character instead of discarding it.
3. Twin Prime: if an exact-gap selector obstruction fails at a larger sieve level, promote the surviving gap-2 packet as the next stress witness.
4. Collatz: the active target is now a phase-15 terminal lift theorem or a 48-bit completion witness.

Remaining decisive target:

```text
CO-TICKET-51 Phase15TerminalLiftOrFullLassoCompletion
```

Proof boundary:

```text
TICKET-50 does not prove or disprove any of the four open problems. It refutes one PrimeProject candidate obstruction and creates stronger finite stress witnesses. The unresolved theorem remains infinite: either all descendants of the near-lasso witnesses terminate by descent/tail shift, or a concrete lift completes and repeats the lasso.
```

### Ticket 51: Phase-15 terminal lift closure

Generated artifact:

```text
data/open-problem/ticket51-phase15-terminal-lift-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-51-terminal-witness-closure.json
data/open-problem/collatz/co-ticket-51-phase15-terminal-lift.json
data/open-problem/goldbach/gb-ticket-51-terminal-witness-closure.json
data/open-problem/twin-prime/tp-ticket-51-terminal-witness-closure.json
```

Aggregate verdict:

```text
phase15_terminal_lift_closed_open_no_resolution
```

한국어 요약: TICKET-51은 TICKET-50에서 발견된 두 개의 32-bit depth-15 near-lasso residue를 반례 후보로 방치하지 않는다. 각 residue에서 phase-15로 가는 low/high lift를 모두 열어 terminal branch를 분류했다. 결과적으로 surviving branch는 0개다. 두 branch는 `tail_word+next_valuation` shift로 lasso template을 벗어나고, 두 branch는 `all_lift_descent`로 닫힌다.

English summary: TICKET-51 terminally classifies the two strongest 32-bit near-lasso witnesses from TICKET-50. Opening every low/high branch through the missing phase-15 edge leaves zero survivors: two branches shift the tail and next valuation, and two branches close by all-lift descent.

Exact Collatz audit:

```text
source roots: 1471663463, 3206130791
base bits: 32
terminal step: 15
tested terminal branches: 4
matching terminal branches: 0
final surviving states: 0
full lasso completions: 0
best template depth: 15
terminal mismatch counts: {all_lift_descent: 2, tail_word+next_valuation: 2}
```

Discarded Collatz route:

```text
using either TICKET-50 depth-15 residue as a concrete Collatz counterexample candidate
relifting the same two roots without a new terminal theorem
```

Retained Collatz routes:

```text
search for genuinely new 48-bit or 64-bit start-template roots with lasso-prefix depth >= 15
derive a symbolic theorem explaining why phase-15 terminal branches always shift or descend
if a future root completes the full lasso, replay it for at least two periods before any counterexample claim
```

Remaining decisive target:

```text
CO-TICKET-52 New48Or64BitRootSearchOrTerminalTheorem
```

Proof boundary:

```text
TICKET-51 does not prove or disprove any of the four open problems. It closes only the terminal lift tree descending from the two known 32-bit near-lasso roots. It does not exclude new 48-bit roots outside that ancestry and does not prove global Collatz descent.
```

### Ticket 52: 48-bit frontier budget and sampled witness closure

Generated artifact:

```text
data/open-problem/ticket52-frontier-budget-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-52-frontier-budget-contract.json
data/open-problem/collatz/co-ticket-52-frontier-budget-sample-closure.json
data/open-problem/goldbach/gb-ticket-52-frontier-budget-contract.json
data/open-problem/twin-prime/tp-ticket-52-frontier-budget-contract.json
```

Aggregate verdict:

```text
frontier_budget_open_no_resolution
```

한국어 요약: TICKET-52는 TICKET-51의 한계를 정면으로 확인한다. TICKET-51은 두 개의 32비트 near-lasso ancestry를 닫았지만, 48비트 start-template root가 반드시 그 두 ancestry로 투영되는 것은 아니다. 실제로 재현 가능한 200,000개 debt-valid valuation-word 샘플에서 새 48비트 depth-15 near-lasso root `171308122831719`가 발견됐고, 이 root의 32비트 projection은 `[0,[1,2,1,1],103,2]`라서 기존 닫힌 start-template ancestry 밖에 있다. 이 새 후보도 base-48 terminal lift audit에서 phase 15에 닫혔다.

English summary: TICKET-52 shows that the TICKET-51 closure is ancestry-local, not a 48-bit theorem. The exact 48-bit frontier has 83,401,400,116 debt-valid valuation words, and a deterministic 200,000-word sampler finds one new 48-bit depth-15 near-lasso root outside the closed 32-bit ancestry. A generalized base-48 terminal lift audit closes that witness at phase 15 with no full lasso completion.

Exact Collatz audit:

```text
48-bit debt-valid valuation words: 83,401,400,116
64-bit debt-valid valuation words: 2,216,134,944,775,156
sample seed: 20,260,709
sample count: 200,000
verified open sample words: 100,026
start-template sample matches: 3,184
sampled depth counts: {1: 1,650; 2: 763; 3: 406; 4: 189; 5: 175; 15: 1}
new sampled depth-15 root: 171308122831719
32-bit projection: 3352230759
projection template: [0,[1,2,1,1],103,2]
terminal step: 15
terminal mismatch counts: {tail_word+next_valuation: 2}
final surviving states: 0
full lasso completions: 0
```

Discarded Collatz route:

```text
promoting the TICKET51 two-root closure to a 48-bit theorem
continuing with blind 48-bit or 64-bit valuation-word enumeration as the main proof route
treating a sampled closure as evidence that all unsampled roots close
```

Retained Collatz routes:

```text
build a symbolic counter for all 48-bit start-template roots
encode the valuation-word frontier as a SAT/SMT or automaton-counting problem
prove a phase-15 terminal mismatch theorem for every depth-15 root
if a future root completes the full lasso, replay it for multiple periods and then state the independent infinite periodicity theorem required
```

Remaining decisive target:

```text
CO-TICKET-53 Symbolic48BitFrontierCoverageOrFullLassoReplay
```

Proof boundary:

```text
TICKET-52 does not prove or disprove any of the four open problems. It finds and closes one new sampled 48-bit Collatz near-lasso witness, and it proves that the old valuation-word enumeration has reached an infeasible frontier. The sampler is not exhaustive and cannot exclude unsampled 48-bit roots.
```

### Ticket 53: Symbolic phase-15 terminal mismatch theorem

Generated artifact:

```text
data/open-problem/ticket53-symbolic-terminal-theorem-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-53-terminal-no-go-theorem.json
data/open-problem/collatz/co-ticket-53-symbolic-terminal-theorem.json
data/open-problem/goldbach/gb-ticket-53-terminal-no-go-theorem.json
data/open-problem/twin-prime/tp-ticket-53-terminal-no-go-theorem.json
```

Aggregate verdict:

```text
symbolic_terminal_theorem_open_no_resolution
```

한국어 요약: TICKET-53은 TICKET-50부터 TICKET-52까지 반복된 phase-15 terminal failure를 더 큰 샘플로 밀어붙이지 않고, 상징 정리로 분리한다. 현재 추출된 lasso family에서 phase 14 parent가 `[14,[1,1,1,1],103,10]`이면, low terminal branch는 대기 중인 valuation `10`을 정확히 소비하므로 tail에 `10`이 들어간다. high terminal branch는 prefix 이후 boundary가 `3^m * 2^9`만큼 바뀌므로 next valuation이 `9`로 강제된다. 따라서 두 branch 모두 phase-15 target `[15,[1,1,1,1],103,10]`에 도달할 수 없다.

English summary: TICKET-53 converts the repeated terminal failure into a local theorem. For the extracted lasso family, a phase-14 parent with template `[14,[1,1,1,1],103,10]` cannot reach the phase-15 target on either branch. The low branch consumes the pending valuation `10`, forcing a tail mismatch. The high branch shifts the boundary by `3^m * 2^9`, forcing next valuation `9`, so it also cannot match the target.

Exact Collatz audit:

```text
theorem: Phase15TerminalMismatchForExtractedLasso
checked roots: 1471663463 at 32 bits; 3206130791 at 32 bits; 171308122831719 at 48 bits
all checked roots satisfy parent premise: true
low branch next valuation before terminal: 10
high branch next valuation before terminal: 9
terminal target matches: 0
```

Discarded Collatz route:

```text
the extracted phase-15 lasso family as a counterexample route
larger sampling inside the same terminal template family
relifting known roots after the symbolic mismatch theorem already applies
```

Retained Collatz routes:

```text
extract genuinely new lasso-template families from the frontier graph
search for a global descent invariant not based on the discarded phase-15 family
formalize Phase15TerminalMismatchForExtractedLasso in the proof kernel as a local no-go lemma
```

Remaining decisive target:

```text
CO-TICKET-54 NewTemplateFamilyExtractionOrGlobalDescentInvariant
```

Proof boundary:

```text
TICKET-53 does not prove or disprove any of the four open problems. It refutes one extracted Collatz lasso family, including all currently known near-lasso witnesses for that family. A full Collatz proof still requires a global argument covering all trajectories or all remaining template families.
```

### Ticket 54: Post-terminal new template family extraction

Generated artifact:

```text
data/open-problem/ticket54-new-template-family-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-54-post-nogo-family-triage.json
data/open-problem/collatz/co-ticket-54-new-template-family.json
data/open-problem/goldbach/gb-ticket-54-post-nogo-family-triage.json
data/open-problem/twin-prime/tp-ticket-54-post-nogo-family-triage.json
```

Aggregate verdict:

```text
new_template_family_extracted_open_no_resolution
```

한국어 요약: TICKET-54는 TICKET-53에서 폐기된 phase-15 terminal family를 더 이상 샘플링하지 않는다. 대신 그 family를 제거한 뒤 남는 Collatz frontier를 다시 세어, 다음으로 공격해야 할 family를 추출한다. exact 32-bit 시작 template은 69,092개이고, 이 중 TICKET-53이 폐기한 depth-15 root 2개를 제거하면 69,090개가 남는다. 남은 후보의 최대 lasso-prefix depth는 5로 내려가며, 4,372개가 phase-5 `next_valuation=10` gate에서 막힌다. 이 phase-5 실패군 안에서 observed next valuation이 10인 경우는 0개다.

English summary: TICKET-54 stops spending search budget on the TICKET-53 terminal family. It removes that family, re-audits the remaining exact 32-bit start-template frontier, and extracts `Phase5ValuationGate` as the strongest remaining bounded Collatz family. The post-discard frontier has max depth 5, with 4,372 exact roots failing at the phase-5 next-valuation gate.

Exact Collatz audit:

```text
exact 32-bit start-template matches: 69,092
discarded TICKET-53 depth-15 roots: 2
remaining exact starts: 69,090
post-discard max exact depth: 5
phase-5 gate exact roots: 4,372
phase-5 failures with observed next_valuation=10: 0
48-bit deterministic sample post-discard max depth: 5
48-bit deterministic sample phase-5 gate roots: 175
```

New candidate family:

```text
Phase5ValuationGate
```

Candidate theorem:

```text
Every phase-compatible start that reaches the first five lasso templates either belongs to the discarded phase-15 terminal family, closes by descent, or fails the phase-5 next_valuation=10 gate.
```

Counterexample target:

```text
Find a root outside the TICKET-53 terminal family that reaches phase 5 with next_valuation=10 and then survives into a different replayable lasso template.
```

Discarded or deprioritized routes:

```text
repeating random samples inside the TICKET-53 terminal family
treating the 26-bit finite template-rank measure as a Collatz proof
blindly enlarging the template graph without a parametric closure theorem
```

Remaining decisive target:

```text
CO-TICKET-55 Phase5ValuationGateTheoremOrCounterexample
```

Proof boundary:

```text
TICKET-54 does not prove or disprove any of the four open problems. It prunes one terminal family and extracts the next finite Collatz family to attack. A full Collatz proof still requires an all-lift phase-5 gate theorem, a global descent invariant, or a genuine replayable counterexample.
```

### Ticket 55: Phase-5 gate-to-terminal tunnel theorem

Generated artifact:

```text
data/open-problem/ticket55-phase5-valuation-gate-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-55-gate-terminal-tunnel.json
data/open-problem/collatz/co-ticket-55-phase5-gate-tunnel.json
data/open-problem/goldbach/gb-ticket-55-gate-terminal-tunnel.json
data/open-problem/twin-prime/tp-ticket-55-gate-terminal-tunnel.json
```

Aggregate verdict:

```text
phase5_gate_tunnel_open_no_resolution
```

한국어 요약: TICKET-55는 TICKET-54에서 남은 `Phase5ValuationGate`를 더 큰 샘플로 키우지 않고, gate를 통과한 후보가 어디로 가는지 증명 의무를 분리한다. phase 5에서 `[5,[1,1,1,1],103,10]`에 도달하고 `consumed_bits = b+5`이면, pending valuation `10`은 phase 6부터 phase 14까지 소비되지 않는다. 따라서 같은 prefix, 같은 consumed bit count, 같은 next valuation을 유지한 채 phase 좌표만 증가한다. phase 15에서는 그 `10`이 소비되어 tail이 `[1,1,1,10]`으로 바뀌거나 descent로 닫히므로, target `[15,[1,1,1,1],103,10]`에는 도달하지 못한다.

English summary: TICKET-55 proves a local gate-to-terminal tunnel for the extracted low-lift family. If a root reaches the phase-5 gate with consumed bits equal to the gate modulus, the pending valuation `10` survives unchanged through phases 6-14. At phase 15 it is consumed, forcing the TICKET53 terminal no-go.

Exact Collatz audit:

```text
theorem: Phase5GateToTerminalTunnel
checked gate-crossing roots: 3
gate matches: 3
tunnel matches through phases 5-14: 3
same pending certificate through tunnel: 3
terminal target matches: 0
exact 32-bit start-template matches: 69,092
exact 32-bit starts failed before or at phase 5: 69,090
exact 32-bit gate crossers: 2
exact 32-bit gate crossers terminally closed: 2
48-bit deterministic sample phase-5 gate roots: 175
```

Local theorem:

```text
Phase5GateToTerminalTunnel
```

Candidate theorem still missing:

```text
Every phase-compatible start outside the current low-lift family either fails before or at a finite valuation gate, or enters a separately terminally closed family.
```

Counterexample target:

```text
Find a root outside the current low-lift start-template model that crosses the finite gate and avoids every known terminal no-go tunnel.
```

Remaining decisive target:

```text
CO-TICKET-56 PreGateResidueClosureOrTemplateModelEscape
```

Proof boundary:

```text
TICKET-55 does not prove or disprove any of the four open problems. It closes the extracted low-lift lasso route for the exact 32-bit start-template population and the known 48-bit sampled gate-crosser, but it does not cover every Collatz trajectory, every base modulus, or every possible template family.
```

### Ticket 56: Pre-gate partition and projection escape

Generated artifact:

```text
data/open-problem/ticket56-pre-gate-projection-escape-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-56-projection-escape-frontier.json
data/open-problem/collatz/co-ticket-56-pre-gate-projection-escape.json
data/open-problem/goldbach/gb-ticket-56-lift-escape-frontier.json
data/open-problem/twin-prime/tp-ticket-56-lift-escape-frontier.json
```

Aggregate verdict:

```text
pre_gate_projection_escape_open_no_resolution
```

한국어 요약: TICKET-56은 TICKET-55 이후 남은 가장 쉬운 오해를 제거한다. exact 32-bit start-template 안에서는 현재 추출된 lasso route가 완전히 분할된다. `69,092`개 후보 중 `69,090`개는 offset 1-5에서 next-valuation mismatch로 실패하고, 남은 `2`개 gate crosser는 TICKET-55에서 terminal no-go로 닫혔다. 하지만 이 finite partition을 전역 귀납으로 올리는 것은 틀린 경로다. TICKET-52에서 기록된 48-bit depth-15 witness `171308122831719`는 32-bit projection이 `[0,[1,2,1,1],103,2]`라서 exact32 start-template 밖으로 벗어난다.

English summary: TICKET-56 closes the exact 32-bit extracted-lasso route as a finite partition, then rejects the simple projection-closure route. A higher-bit start-template witness can project outside the fixed 32-bit start-template model, so the next theorem must be parametric in base modulus and template state.

Exact Collatz audit:

```text
local theorem: Exact32StartTemplateLassoPartition
exact 32-bit start-template matches: 69,092
pre-gate first failures: 69,090
failure offsets: 1 -> 34,458; 2 -> 17,301; 3 -> 8,649; 4 -> 4,310; 5 -> 4,372
all pre-gate failures are next-valuation mismatch: true
phase-5 observed next_valuation=10 among failures: 0
gate crossers: 2
partition sum: 69,092
partition complete for exact32 start-template: true
projection-closure status: refuted by sampled 48-bit depth-15 witness
escape witness: 171,308,122,831,719
```

Discarded route:

```text
A proof that partitions only the exact 32-bit start-template population and assumes every higher-bit start-template root projects back into that same 32-bit template.
```

Candidate theorem still missing:

```text
For every phase-compatible base modulus, every extracted-lasso start-template state either fails a finite next-valuation gate, enters a terminal no-go tunnel, or maps into a strictly smaller closed template family under a well-founded parametric rank.
```

Counterexample target:

```text
Find a higher-bit start-template root outside the exact32 projection model that reaches a finite gate, avoids the TICKET53/TICKET55 terminal tunnel, and replays through at least one full lasso period.
```

Remaining decisive target:

```text
CO-TICKET-57 ParametricTemplateAutomatonOrEscapeCycle
```

Proof boundary:

```text
TICKET-56 does not prove or disprove any of the four open problems. It proves only a finite partition for one extracted Collatz lasso route at 32 bits and identifies why simple projection-based globalization fails.
```

### Ticket 57: Parametric boundary-state automaton audit

Generated artifact:

```text
data/open-problem/ticket57-parametric-template-automaton-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-57-boundary-state-model.json
data/open-problem/collatz/co-ticket-57-parametric-template-automaton.json
data/open-problem/goldbach/gb-ticket-57-boundary-margin-model.json
data/open-problem/twin-prime/tp-ticket-57-boundary-sieve-model.json
```

Aggregate verdict:

```text
parametric_boundary_state_open_no_resolution
```

한국어 요약: TICKET-57은 TICKET-56 이후의 가장 중요한 약한 지점을 공격한다. exact32 finite partition이 있더라도, 그 분기 결과가 단순 template state로 결정되지 않으면 전역 automaton 증명으로 올릴 수 없다. 계산 결과 template만으로는 6개의 coarse outcome이 한 상태에 섞이고, `template + prefix_length + residue mod 2^26`까지 추가해도 92개 collision group이 남는다. audited ladder에서 처음으로 exact32 coarse outcome이 결정되는 경계는 `template + prefix_length + residue mod 2^28`이다. 또한 알려진 near-lasso root 3개는 최대 depth 15까지만 재생되고 full lasso period replay는 0개다.

English summary: TICKET-57 rejects the shortcut from a finite template quotient to a proof. The exact32 partition needs boundary coordinates before even its bounded outcomes become deterministic. The first deterministic audited boundary is `template + prefix_length + residue mod 2^28`, and no known near-lasso root replays a full lasso period.

Exact Collatz audit:

```text
local theorem target: AffineBoundaryTemplateStateOrEscapeCycle
exact 32-bit start-template matches: 69,092
coarse outcomes: fail_offset_1 -> 34,458; fail_offset_2 -> 17,301; fail_offset_3 -> 8,649; fail_offset_4 -> 4,310; fail_offset_5 -> 4,372; phase5_gate_terminal_tunnel -> 2
template-only max outcomes per state: 6
template + prefix_length + residue mod 2^26 collision groups: 92
first deterministic exact32 boundary: template + prefix_length + residue mod 2^28
projection escape carried forward: sampled 48-bit depth-15 witness 171,308,122,831,719 projects to [0,[1,2,1,1],103,2]
known near-lasso roots replayed: 3
maximum replayed prefix depth: 15
full lasso period replays: 0
cycle status: no_known_root_replays_full_lasso_period
```

Discarded routes:

```text
template-only rank or transition relation
exact32 finite partition promoted by simple projection closure
near-lasso prefix treated as a counterexample without full-period replay and lift compatibility
```

Candidate theorem still missing:

```text
For every phase-compatible start cylinder, a boundary-state transition either reaches a finite next-valuation failure gate, enters the Phase5GateToTerminalTunnel, or strictly decreases a well-founded rank defined on the full affine boundary state.
```

Counterexample target:

```text
Find a higher-bit root whose full affine boundary state returns after one lasso period with nondecreasing rank and whose trajectory is not covered by TICKET53, TICKET55, or TICKET56.
```

Remaining decisive target:

```text
CO-TICKET-58 AffineBoundaryLiftStabilityOrFullPeriodEscape
```

Proof boundary:

```text
TICKET-57 does not prove or disprove any of the four open problems. It rejects weaker finite-state proof shortcuts and finds no replayable cycle among known near-lasso roots; the remaining obligation is a parametric affine-boundary lift theorem or a new full-period escape witness.
```

### Ticket 58: Affine-boundary lift stability audit

Generated artifact:

```text
data/open-problem/ticket58-affine-boundary-lift-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-58-zero-kernel-lift-stability.json
data/open-problem/collatz/co-ticket-58-affine-boundary-lift.json
data/open-problem/goldbach/gb-ticket-58-margin-lift-stability.json
data/open-problem/twin-prime/tp-ticket-58-sieve-boundary-lift.json
```

Aggregate verdict:

```text
affine_boundary_lift_open_no_resolution
```

한국어 요약: TICKET-58은 TICKET-57에서 처음 결정적이었던 exact32 affine boundary가 48-bit lift에서도 유지되는지 검사한다. 같은 TICKET52 deterministic 48-bit sample을 재생한 결과, start-template match `3,184`개 중 `3,086`개가 exact32 target 밖으로 projection escape했다. exact32 target 안으로 들어온 `98`개 중 `28`개만 exact32 boundary prediction과 맞았고, `70`개는 다른 outcome을 보였다. 따라서 “exact32 deterministic boundary를 그대로 lift하면 된다”는 경로는 샘플에서 반박된다. full lasso period를 재생한 샘플은 0개다.

English summary: TICKET-58 tests lift stability for the first deterministic exact32 affine boundary. The replayed 48-bit sample refutes the unchanged-boundary lift shortcut: most start-template matches project outside the exact32 target, and most projection-target lifts disagree with the exact32 predicted outcome.

Exact Collatz audit:

```text
local theorem target: AffineBoundaryLiftStabilityOrFullPeriodEscape
exact32 boundary width: 28 low bits
exact32 boundary states: 69,092
exact32 boundary collisions: 0
48-bit replayed sample count: 200,000
verified open words: 100,027
48-bit start-template matches: 3,184
projection escapes: 3,086
projection-target lifts: 98
boundary prediction matches: 28
boundary prediction mismatches: 70
projection-target prediction rate: 28.57%
full lasso period replays: 0
lift-stability status: refuted_by_sampled_boundary_prediction_mismatch
```

Discarded route:

```text
Promote the exact32 deterministic boundary to a global theorem without proving projection inclusion and lift-stable outcome preservation.
```

Candidate theorem still missing:

```text
For every 48-bit and then every higher phase-compatible start, either projection leaves the exact32 model in a separately classified way, or the affine boundary transition preserves the finite gate outcome and decreases a well-founded rank.
```

Counterexample target:

```text
Find a higher-bit start whose projection lies in the deterministic exact32 boundary but whose lift outcome differs, then extend it to a full-period nondecreasing affine-boundary cycle.
```

Remaining decisive target:

```text
CO-TICKET-59 SymbolicLiftMismatchCylinderOrCounted40BitCover
```

Proof boundary:

```text
TICKET-58 does not prove or disprove any of the four open problems. It refutes one sampled lift-stability shortcut and finds no sampled full-period escape; the remaining obligation is symbolic coverage of projection escapes/lift mismatches or a genuine full-period counterexample.
```
