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
