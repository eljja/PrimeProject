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

### Ticket 59: Symbolic lift mismatch cylinder audit

CO-TICKET-59 SymbolicLiftMismatchCylinderOrCounted40BitCover

Artifacts:

```text
data/open-problem/ticket59-symbolic-lift-mismatch-lab.json
data/open-problem/collatz/co-ticket-59-symbolic-lift-mismatch.json
data/open-problem/riemann/rh-ticket-59-counted-lift-cylinder.json
data/open-problem/goldbach/gb-ticket-59-counted-margin-cylinder.json
data/open-problem/twin-prime/tp-ticket-59-counted-sieve-cylinder.json
```

Status:

```text
symbolic_lift_mismatch_open_no_resolution
```

한국어 요약: TICKET-59는 TICKET-58의 lift mismatch를 단일 샘플로 두지 않고 low40 cylinder 단위로 묶는다. 각 selected low40 cylinder마다 가능한 256개 48-bit extension을 전부 열거한다. 선택된 162개 cylinder에서 41,472개 extension을 검사했고, 그중 535개가 48-bit start-template lift였다. 이 안에서 projection escape는 207개, projection-target lift는 328개, boundary mismatch는 224개, boundary match는 104개였다. mismatch seed cylinder 70개 중 35개는 uniform mismatch였지만, 58개 selected cylinder는 mixed outcome이었다. 따라서 “TICKET58 mismatch는 단일 우연 샘플일 뿐”이라는 약한 반론은 줄어들지만, low40만으로는 symbolic proof coordinate가 충분하지 않다는 장애물도 동시에 생긴다.

English summary: TICKET-59 promotes the TICKET-58 point mismatch into selected counted low40-to-48 cylinder audits. It exactly enumerates 256 possible 48-bit extensions for each selected low40 cylinder. This strengthens the evidence from point samples to finite cylinder facts, but it also shows that low40 is not yet a complete symbolic coordinate because many selected cylinders have mixed outcomes.

Key Collatz result:

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

Discarded route:

```text
Treat one 48-bit mismatch as an isolated anecdote, or assume low40 cylinders are stable without enumerating their 48-bit extensions.
```

Candidate theorem still missing:

```text
Every projection-target lift cylinder is either uniformly closed by the exact32 boundary prediction, uniformly refutes that prediction, or carries an explicit higher coordinate that separates the outcomes.
```

Counterexample target:

```text
A counted or symbolic cylinder with full-period replay, or a mixed cylinder that forces an additional coordinate not present in the current affine boundary.
```

Remaining decisive target:

```text
CO-TICKET-60 MixedCylinderSeparatorOrAutomatonCountedCover
```

Proof boundary:

```text
TICKET-59 does not prove or disprove any of the four open problems. It is an exact enumeration of selected low40-to-48 cylinders induced by TICKET58, not an exhaustive 40-bit or 48-bit theorem.
```

### Ticket 60: Mixed-cylinder separator audit

CO-TICKET-60 MixedCylinderSeparatorOrAutomatonCountedCover

Artifacts:

```text
data/open-problem/ticket60-mixed-cylinder-separator-lab.json
data/open-problem/collatz/co-ticket-60-mixed-cylinder-separator.json
data/open-problem/riemann/rh-ticket-60-mixed-cylinder-separator.json
data/open-problem/goldbach/gb-ticket-60-mixed-margin-separator.json
data/open-problem/twin-prime/tp-ticket-60-mixed-sieve-separator.json
```

Status:

```text
mixed_cylinder_separator_open_no_resolution
```

한국어 요약: TICKET-60은 TICKET-59에서 남은 58개 mixed low40 cylinder를 대상으로 separator ladder를 만든다. 선택된 전체 집합은 low40 cylinder 162개와 start-template lift 535개이고, mixed cylinder 내부에는 lift 210개가 있다. `low40`만 쓰면 mixed cylinder 58개가 모두 모호하고, `certificate_prefix_length`를 더해도 mixed outcome collision group이 36개 남는다. 처음으로 outcome과 boundary prediction label을 동시에 결정적으로 가르는 좌표는 `low40 + failure_offset`이다. 그러나 `failure_offset`은 trajectory replay를 통해 얻는 진단 좌표이므로, 이것만으로는 증명이 아니다. 다음 목표는 이 offset을 사전에 예측하는 symbolic transition theorem 또는 automaton-counted cover다.

English summary: TICKET-60 identifies the first tested separator for the mixed TICKET59 cylinders. `low40 + failure_offset` deterministically separates both observed outcome and boundary-match status on the selected population. This is a useful coordinate discovery, but it is replay-derived; a proof needs a non-circular symbolic predictor for failure offset.

Key Collatz result:

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
full proof status: open
```

Discarded route:

```text
Assume low40 cylinder identity is enough to classify higher-bit outcomes. TICKET60 rejects this because 58 selected cylinders remain mixed under low40 alone.
```

Candidate theorem still missing:

```text
Every mixed low40 cylinder is separated by a bounded higher-coordinate signature, and that signature extends to an automaton-counted cover with no full-period nondecreasing cycle.
```

Counterexample target:

```text
A mixed cylinder whose ambiguity survives every bounded separator short of exact high-extension identity, or a full-period replay inside a separated cylinder.
```

Remaining decisive target:

```text
CO-TICKET-61 SymbolicFailureOffsetPredictorOrCountedCover
```

Proof boundary:

```text
TICKET-60 does not prove or disprove any of the four open problems. It names a replay-derived separator and refutes under-specified boundary proofs; the infinite symbolic transition theorem remains open.
```

### Ticket 61: Symbolic failure-offset pre-replay separator audit

CO-TICKET-61 SymbolicFailureOffsetPredictorOrCountedCover

Artifacts:

```text
data/open-problem/ticket61-symbolic-failure-offset-lab.json
data/open-problem/collatz/co-ticket-61-symbolic-failure-offset.json
data/open-problem/riemann/rh-ticket-61-symbolic-separator.json
data/open-problem/goldbach/gb-ticket-61-symbolic-margin-separator.json
data/open-problem/twin-prime/tp-ticket-61-symbolic-sieve-separator.json
```

Status:

```text
symbolic_failure_offset_open_no_resolution
```

한국어 요약: TICKET-61은 TICKET-60의 가장 큰 약점인 `failure_offset`의 순환성을 제거하는 실험이다. `failure_offset`은 trajectory replay 후에 관측되는 값이므로 그대로는 증명 좌표가 될 수 없다. TICKET-61은 separator key에서 `failure_offset`, `failure_observed`, first-failure certificate를 금지하고, `low40`, certificate prefix length, high-extension bit처럼 replay 전에 알 수 있는 좌표만 사용한다. 결과적으로 mixed 58개 cylinder, 210개 start-template lift에서 `low40 + high_extension mod 16`이 failure offset, observed outcome, boundary prediction label을 모두 결정적으로 분리했다. 이는 증명 경로를 한 단계 강화하지만, 아직 선택된 유한 cylinder 집합 위의 결과다.

English summary: TICKET-61 removes the circular coordinate from TICKET-60. It forbids replay-derived keys and tests whether pre-replay high-extension bits predict the same failure-offset separator. On the selected mixed population, `low40 + high_extension mod 16` is the first joint deterministic pre-replay separator for failure offset, observed outcome, and boundary prediction label. This is not a proof; it is a sharper theorem target.

Key Collatz result:

```text
selected low40 cylinders: 162
selected start-template lifts: 535
mixed cylinders: 58
mixed start-template lifts: 210
low40-only failure-offset collisions: 58 groups / 210 ambiguous rows
low40 + certificate_prefix_length: 36 failure-offset collision groups / 81 ambiguous rows
first mixed pre-replay joint separator: low40_plus_high_extension_mod_2^4
first all-selected pre-replay joint separator: low40_plus_high_extension_mod_2^4
first top-bit joint separator: low40_plus_high_extension_top_6_bits
full proof status: open
```

Discarded route:

```text
Use low40+failure_offset from TICKET60 as if it were a proof coordinate. That is circular because failure_offset is learned only after replaying the trajectory to failure.
```

Candidate theorem still missing:

```text
For every selected mixed low40 cylinder, the mod-16 high-extension residue determines the first failure offset and the boundary prediction label; extend this to a symbolic transition theorem or an automaton-counted cover that excludes full-period nondecreasing cycles.
```

Counterexample target:

```text
A selected or newly lifted mixed cylinder whose failure_offset remains ambiguous under low40 plus high_extension mod 16, or a full-period replay inside a mod-16-separated cylinder.
```

Remaining decisive target:

```text
CO-TICKET-62 Mod16FailureOffsetTransitionOrAutomatonCountedCover
```

Proof boundary:

```text
TICKET-61 does not prove or disprove any of the four open problems. It turns a replay-derived separator into a pre-replay finite-coordinate theorem target, but the infinite symbolic transition theorem remains open.
```

### Ticket 62: Mod16 transition-cover lift audit

CO-TICKET-62 Mod16FailureOffsetTransitionOrAutomatonCountedCover

Artifacts:

```text
data/open-problem/ticket62-mod16-transition-cover-lab.json
data/open-problem/collatz/co-ticket-62-mod16-transition-cover.json
data/open-problem/riemann/rh-ticket-62-transition-closure.json
data/open-problem/goldbach/gb-ticket-62-margin-transition.json
data/open-problem/twin-prime/tp-ticket-62-sieve-transition.json
```

Status:

```text
mod16_transition_cover_open_no_resolution
```

한국어 요약: TICKET-62는 TICKET-61의 pre-replay mod16 좌표가 더 큰 lift에서도 유지되는지 검사한다. 대상은 TICKET-61의 mixed 48비트 start-template row 210개다. 52비트 lift에서는 3,360개 후보 중 55개가 start-template로 남았고, 56비트 lift에서는 53,760개 후보 중 824개가 start-template로 남았다. 두 경우 모두 `low40 + base high_extension mod 16`이 failure offset, observed outcome, boundary prediction label, transition label을 collision 없이 결정했다. full-period replay는 발견되지 않았다. 이는 mod16 automaton-cover 경로를 강화하지만, 아직 유한 lift audit이므로 Collatz 증명은 아니다.

English summary: TICKET-62 tests whether TICKET61's pre-replay mod16 coordinate survives bounded higher lifts. The 52-bit and 56-bit audits find no mod16 collision and no full-period replay among the surviving start-template lifts. This is bounded evidence for a mod16 automaton-cover route, not an infinite theorem.

Key Collatz result:

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
full proof status: open
```

Discarded route:

```text
Promote TICKET61's mod16 separator directly to an infinite theorem without checking higher-bit lift closure. TICKET62 treats that as an unproved shortcut.
```

Candidate theorem still missing:

```text
For every mixed low40 cylinder and every admissible higher lift, the low40 plus high-extension mod16 state either determines a closed failure-offset transition or enters a finite automaton cover with no full-period nondecreasing cycle.
```

Counterexample target:

```text
A higher start-template lift where low40 plus base mod16 admits two different failure offsets, or a full-period replay inside the tested lift family.
```

Remaining decisive target:

```text
CO-TICKET-63 Mod16AutomatonCoverOrLiftCollision
```

Proof boundary:

```text
TICKET-62 does not prove or disprove any of the four open problems. It tests bounded 52/56-bit lift closure for the mod16 coordinate and finds no collision in that audit, but the infinite symbolic automaton-cover theorem remains open.
```

### Ticket 63: Mod16 automaton-cover table and 60-bit chain audit

CO-TICKET-63 Mod16AutomatonCoverOrLiftCollision

Artifacts:

```text
data/open-problem/ticket63-mod16-automaton-cover-lab.json
data/open-problem/collatz/co-ticket-63-mod16-automaton-cover.json
data/open-problem/riemann/rh-ticket-63-automaton-cover.json
data/open-problem/goldbach/gb-ticket-63-margin-automaton.json
data/open-problem/twin-prime/tp-ticket-63-sieve-automaton.json
```

Status:

```text
mod16_automaton_cover_open_no_resolution
```

한국어 요약: TICKET-63은 TICKET-62의 bounded mod16 transition evidence를 automaton-cover 표로 바꾸는 시도다. 48비트 selected mixed cylinder 58개와 start-template lift 210개에서 출발하고, 56비트 생존 row 824개를 부모 row로 삼아 60비트 targeted chain lift 13,184개를 검사했다. 그 결과 start-template target row 209개가 남았고, 이 row들에 대한 state table은 deterministic이며 collision audit은 0개였다. chained 60비트 row에서 첫 결정적 quotient separator는 `low40 mod 2^20 + base_mod16`이다. 이 결과는 다음 정리 목표를 더 명확히 하지만, finite table audit이므로 콜라츠 증명이나 네 난제의 증명은 아니다.

English summary: TICKET-63 converts TICKET62's bounded mod16 transition evidence into an explicit finite automaton-table audit. It chains the 824 surviving 56-bit rows into 13,184 targeted 60-bit lifts and retains 209 start-template target rows. The resulting state tables are deterministic with no audited automaton collisions and no full-period escape. This sharpens the next theorem target, but it is still a finite audit rather than an infinite proof.

Key Collatz result:

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
full proof status: open
```

Discarded route:

```text
Treat deterministic 52/56-bit mod16 survival as a proof of Collatz. TICKET63 rejects this route because closure under all higher lifts and all relevant cylinders is still missing.
```

Candidate theorem still missing:

```text
For every admissible lift of the selected mixed-cylinder family, the mod16 state together with the finite quotient low40 mod 2^20 induces a symbolic transition that either stays inside a counted automaton cover with no nondecreasing full-period cycle, or produces an explicit lift collision.
```

Counterexample target:

```text
A higher chained lift or newly admitted mixed cylinder with the same low40 mod 2^20 plus base_mod16 state but conflicting transition label, failure offset, or boundary outcome; alternatively, a full-period replay inside the automaton cover.
```

Remaining decisive target:

```text
CO-TICKET-64 SymbolicMod16AutomatonTransitionProof
```

Proof boundary:

```text
TICKET-63 does not prove or disprove any of the four open problems. It extracts deterministic finite state tables and a stronger quotient separator, but the infinite symbolic transition theorem and any independent formal proof remain open.
```

### Ticket 64: Symbolic mod16 transition gate obstruction

CO-TICKET-64 SymbolicMod16AutomatonTransitionProof

Artifacts:

```text
data/open-problem/ticket64-symbolic-mod16-transition-lab.json
data/open-problem/collatz/co-ticket-64-symbolic-mod16-transition.json
data/open-problem/riemann/rh-ticket-64-gate-predicate.json
data/open-problem/goldbach/gb-ticket-64-cutoff-gate.json
data/open-problem/twin-prime/tp-ticket-64-parity-gate.json
```

Status:

```text
symbolic_mod16_transition_open_no_resolution
```

한국어 요약: TICKET-64는 TICKET-63의 다음 목표였던 `SymbolicMod16AutomatonTransitionProof`를 직접 압박했다. TICKET63에서 얻은 60비트 survivor row 209개 각각에 대해 64비트 후보 자식 16개씩, 총 3,344개를 만들었다. 이 중 start-template child는 42개뿐이고, non-start child는 3,302개였다. 기존 quotient state `low40 mod 2^20 + base_mod16`는 start-template gate를 결정하지 못했다. 같은 state 안에서 start-template/non-start-template이 갈라지는 gate collision group이 42개 나왔다. 더 중요하게, admitted 64비트 child 자체도 더 이상 낙관적 `0->0` 전이를 따르지 않았다. transition label은 `0->1` 20개, `0->2` 11개, `0->3` 5개, `0->5` 3개, `0->4` 3개로 갈라졌다. 따라서 TICKET64는 증명이 아니라, TICKET63의 직접 승격 경로를 반박하고 “symbolic start-template gate + offset-transition relation”을 다음 정리 목표로 만든다.

English summary: TICKET-64 tests the symbolic transition target produced by TICKET63. It extends the 209 retained 60-bit rows to 3,344 candidate 64-bit children. Only 42 are admitted start-template children. The retained quotient state cannot decide the admissibility gate, and the optimistic admitted-child `0->0` transition already fails at 64 bits. This is a useful obstruction to a shortcut, not a proof or counterexample to Collatz.

Key Collatz result:

```text
60-bit parent rows: 209
64-bit candidate children: 3,344
64-bit start-template children: 42
64-bit non-start children: 3,302
state20 gate collision groups: 42
state20+top4 gate collision groups: 24
64-bit admitted transition labels: 0->1:20, 0->2:11, 0->3:5, 0->5:3, 0->4:3
first admitted-child quotient separator: low40_mod_2^16_plus_base_mod16
optimistic 0->0 admitted-child formula: refuted at 64 bits
full proof status: open
```

Discarded route:

```text
Promote the TICKET63 quotient state and the 60-bit 0->0 transition directly to an infinite symbolic theorem. TICKET64 rejects this shortcut because both the next admissibility gate and the admitted-child transition split at 64 bits.
```

Candidate theorem still missing:

```text
For every admissible lift, a symbolic start-template gate first selects the valid children; inside that selected subcover, an explicit offset-transition relation is closed and a well-founded cover excludes full-period nondecreasing cycles.
```

Counterexample target:

```text
A pair of candidate children sharing the refined symbolic gate state but disagreeing on start-template admissibility, or a pair of admitted children sharing the refined transition state but disagreeing on the offset-transition label.
```

Remaining decisive target:

```text
CO-TICKET-65 SymbolicStartTemplateGateAndOffsetTransition
```

Proof boundary:

```text
TICKET-64 does not prove or disprove any of the four open problems. It refutes one overly optimistic finite-to-symbolic promotion path and replaces it with a sharper gate-plus-offset theorem target.
```

### Ticket 65: Start-template chain extinction and gate-compression obstruction

CO-TICKET-65 StartTemplateChainExtinctionOrComplementCover

Artifacts:

```text
data/open-problem/ticket65-start-template-chain-extinction-lab.json
data/open-problem/collatz/co-ticket-65-start-template-chain-extinction.json
data/open-problem/riemann/rh-ticket-65-branch-extinction.json
data/open-problem/goldbach/gb-ticket-65-cutoff-complement.json
data/open-problem/twin-prime/tp-ticket-65-parity-complement.json
```

Status:

```text
start_template_chain_extinction_open_no_resolution
```

한국어 요약: TICKET-65는 TICKET-64가 남긴 `SymbolicStartTemplateGateAndOffsetTransition` 목표를 직접 추적했다. 결과적으로 현재 추적 중인 start-template chain은 `56 bits:824 -> 60 bits:209 -> 64 bits:42 -> 68 bits:12 -> 72 bits:3 -> 76 bits:1 -> 80 bits:0`으로 소멸했다. full-period replay는 0개였다. 따라서 TICKET63/TICKET64에서 가장 강하게 남아 있던 구체 branch는 80비트에서 닫혔다. 그러나 gate separator 탐색은 좋은 소식만은 아니다. 64비트와 68비트에서 결정적 gate는 찾을 수 있지만, 그 결정성은 압축된 symbolic automaton이 아니라 row-unique state로 붕괴한다. 즉 이 결과는 “현재 branch closure”이지 “전역 Collatz proof”가 아니다.

English summary: TICKET-65 follows the retained TICKET63/TICKET64 start-template chain until it becomes extinct at 80 bits. This is strong branch pruning, but not a global theorem. The audit also shows that the deterministic gate separators found at 64 and 68 bits are row-unique, so the compact finite-automaton route remains blocked.

Key Collatz result:

```text
survivor sequence: 824 -> 209 -> 42 -> 12 -> 3 -> 1 -> 0
extinction at bits: 80
full-period replays: 0
64-bit best compressed near miss: low40_parent_high10_child_top4, 3 collision groups, 6 ambiguous rows
64-bit first deterministic gate: low40_parent_top_parent_high10_child_top4, row-unique
68-bit best compressed near miss: low40_parent_high2_child_top4, 1 collision group, 2 ambiguous rows
68-bit first deterministic gate: state20_base_mod16_child_top4, row-unique
full proof status: open
```

Discarded route:

```text
Treat the TICKET63/TICKET64 start-template survivor chain as a compact repeating automaton. TICKET65 closes that concrete chain by 80 bits and shows that the deterministic gate keys are row-unique rather than compressed.
```

Candidate theorem still missing:

```text
StartTemplateChainExtinctionOrComplementCover: every branch in the current start-template cover either exits the cover in finite symbolic time or is captured by a non-row-unique gate predicate with a well-founded offset transition.
```

Counterexample target:

```text
A 4-bit lift branch beyond the current cover that re-enters a start-template lasso with a repeated non-row-unique gate state, or a compact gate separator that remains deterministic beyond the 80-bit extinction audit.
```

Remaining decisive target:

```text
CO-TICKET-66 ComplementCoverForStartTemplateExit
```

Proof boundary:

```text
TICKET-65 does not prove or disprove any of the four open problems. It closes one tracked Collatz branch, but it does not prove that every integer enters that branch or that every branch leaving it descends.
```

### Ticket 66: Complement-cover audit and open-template frontier

CO-TICKET-66 ComplementCoverForStartTemplateExit

Artifacts:

```text
data/open-problem/ticket66-complement-cover-lab.json
data/open-problem/collatz/co-ticket-66-complement-cover.json
data/open-problem/riemann/rh-ticket-66-complement-cover.json
data/open-problem/goldbach/gb-ticket-66-complement-cover.json
data/open-problem/twin-prime/tp-ticket-66-complement-cover.json
```

Status:

```text
complement_cover_open_no_resolution
```

한국어 요약: TICKET-66은 TICKET-65가 요구한 보완 덮개 정리를 직접 검사한다. TICKET-65에서 추적한 start-template chain은 80비트에서 닫혔지만, 그것만으로는 전역 Collatz 증명이 되지 않는다. 따라서 모든 non-start-template exit branch가 이미 descent/terminal machinery로 닫히는지 확인해야 한다. 계산 결과는 부정적이다. 56->60, 60->64, 64->68, 68->72, 72->76, 76->80 lift에서 나온 non-start-template 후보는 총 17,189개이고, 그중 55개만 즉시 all-lift descent로 닫힌다. 나머지 17,134개는 491개 열린 `needs_split` template family로 남는다. 이는 “보완 덮개가 이미 있다”는 지름길을 반박하고, 다음 표적을 열린 template family rank theorem 또는 실제 무한 lift 반례 후보로 좁힌다.

English summary: TICKET-66 audits the complement theorem required after TICKET-65. The result is not a proof. It refutes the shortcut that every branch outside the tracked start-template chain is already covered by existing descent or terminal-family arguments. The next decisive object is a rank theorem over the 491 open template families, or a compatible infinite lift through one of them.

Key Collatz result:

```text
non-start complement candidates: 17,189
closed by immediate all-lift descent: 55
open needs_split instances: 17,134
descent coverage rate: 0.003199720752
unique open template families: 491
largest open family: [12,[1,1,1,1],103,5] with 432 instances
exit pressure: open_wrong_tail_target_residue_mod_256 = 14,244; open_target_tail_wrong_next_valuation = 2,890
full proof status: open
```

Discarded route:

```text
Assume that every branch leaving the TICKET65 start-template chain is already handled by the existing descent or terminal-family closures. TICKET66 refutes that shortcut: only 55 of 17,189 complement candidates close by immediate all-lift descent.
```

Candidate theorem still missing:

```text
OpenTemplateFamilyRankOrComplementCounterexample: every open template family left by ComplementCoverForStartTemplateExit admits a well-founded symbolic rank after a finite split, or there exists a compatible infinite lift preserving one nondecreasing template family.
```

Counterexample target:

```text
A compatible infinite lift through one of the 491 open complement template families, starting with the smallest open residue or one of the largest families such as [12,[1,1,1,1],103,5].
```

Remaining decisive target:

```text
CO-TICKET-67 OpenTemplateFamilyRankOrComplementCounterexample
```

Proof boundary:

```text
TICKET-66 does not prove or disprove any of the four open problems. It narrows the next Collatz proof/counterexample frontier to 491 open complement template families and explicitly blocks the claim that the TICKET-65 complement was already covered.
```

### Ticket 67: Open-template rank audit and cyclic frontier extraction

CO-TICKET-67 OpenTemplateFamilyRankOrComplementCounterexample

Artifacts:

```text
data/open-problem/ticket67-open-template-rank-lab.json
data/open-problem/collatz/co-ticket-67-open-template-rank.json
data/open-problem/riemann/rh-ticket-67-rank-cycle-frontier.json
data/open-problem/goldbach/gb-ticket-67-rank-cycle-frontier.json
data/open-problem/twin-prime/tp-ticket-67-rank-cycle-frontier.json
```

Status:

```text
rank_cycle_frontier_open_no_resolution
```

한국어 요약: TICKET-67은 TICKET-66에서 남은 491개 열린 template family를 한 단계 더 공격한다. 각 열린 source instance를 4비트 더 lift하여 16개 child를 검사했고, 총 274,144개 child lift를 만들었다. 결과는 단순 rank route에 부정적이다. 17,134개 source instance 중 모든 child가 닫힌 것은 13개뿐이고, 17,121개는 계속 열린 child를 가진다. child 상태는 `needs_split = 265,812`, `all_lift_descent = 8,332`이다. open transition graph는 45,665개의 distinct edge와 265,812 edge weight를 가지며, 5,100개 node 중 429개 node가 하나의 cyclic SCC를 이룬다. source family 458개가 이 cycle에 도달한다. 또한 scalar debt rank도 실패한다. open child transition 중 96,433개가 debt를 감소시키지 않는다. 따라서 다음 정리는 단순 template rank가 아니라 429-node SCC를 더 세밀한 pre-replay coordinate로 분해하거나, 그 SCC 안에 무한히 머무는 compatible lift가 불가능함을 보여야 한다.

English summary: TICKET-67 tests whether TICKET66's 491 open families close after one more 4-bit split or admit a simple rank. Both shortcuts fail. The finite quotient has a 429-node cyclic SCC and many nondecreasing debt edges. This is not a counterexample; it is a precise finite obstruction that must be refined or ruled out by an infinite compatibility theorem.

Key Collatz result:

```text
source open instances: 17,134
source open template families: 491
child lift rows: 274,144
child needs_split: 265,812
child all_lift_descent: 8,332
source instances closed after one split: 13
source instances still open after one split: 17,121
open transition edge count: 45,665
open transition edge weight: 265,812
transition nodes: 5,100
child open template families: 5,056
cyclic components: 1
cyclic nodes: 429
largest cyclic component: 429
cycle edge weight: 89,222
source families reaching cycle: 458
debt nondecreasing edges: 96,433
debt nondecreasing rate: 0.362786480671
full proof status: open
```

Discarded route:

```text
Try to close the 491 open template families by one 4-bit split or by a scalar debt rank. TICKET67 refutes both shortcuts: 17,121 of 17,134 source instances still have open children, the template graph has a large cyclic component, and many open child transitions do not decrease debt.
```

Candidate theorem still missing:

```text
CycleSCCRefinementOrInfiniteLiftExclusion: every edge inside the TICKET67 cyclic template SCC either exits under a finite pre-replay coordinate refinement with a well-founded rank, or no compatible infinite 2-adic lift can follow the SCC forever.
```

Counterexample target:

```text
A compatible infinite lift that stays inside the 429-node cyclic template SCC while avoiding all descent closures. The TICKET67 SCC is only a quotient-cycle candidate, not a Collatz counterexample.
```

Remaining decisive target:

```text
CO-TICKET-68 CycleSCCRefinementOrInfiniteLiftExclusion
```

Proof boundary:

```text
TICKET-67 does not prove or disprove any of the four open problems. It refutes two simpler rank routes and isolates a finite quotient-cycle obstruction that still requires an infinite compatibility theorem.
```

### Ticket 68: Cycle-SCC refinement and bounded DAG extraction

CO-TICKET-68 CycleSCCRefinementOrInfiniteLiftExclusion

Artifacts:

```text
data/open-problem/ticket68-cycle-scc-refinement-lab.json
data/open-problem/collatz/co-ticket-68-cycle-scc-refinement.json
data/open-problem/riemann/rh-ticket-68-frontier-refinement.json
data/open-problem/goldbach/gb-ticket-68-frontier-refinement.json
data/open-problem/twin-prime/tp-ticket-68-frontier-refinement.json
```

Status:

```text
cycle_scc_refined_open_no_resolution
```

한국어 요약: TICKET-68은 TICKET-67에서 나온 429-node cyclic SCC를 실제 반례 후보처럼 취급하지 않고, 더 세밀한 pre-replay coordinate로 다시 분해한다. 총 7개 refinement family를 시험했다. `base_template` 좌표에서는 429개 cyclic node와 89,222 cycle edge weight가 그대로 남는다. 그러나 `base_template + prefix_length + consumed_bits` 좌표를 추가하면 관측된 SCC 내부 transition graph가 9,616개 state, 41,283개 edge의 DAG로 깨지고 cyclic node는 0개가 된다. 더 약한 tail/residue-only refinement 중 가장 강한 `tail8_res4096_vexact`도 cyclic node를 429개에서 26개, cyclic edge weight를 89,222에서 129로 줄인다. 이 결과는 증명이 아니다. 하지만 TICKET-67의 순환이 피할 수 없는 구조라는 해석은 버려야 하며, 다음 증명 목표는 prefix/consumed DAG가 모든 compatible higher lift에 대해 transition-complete인지 증명하는 것이다.

English summary: TICKET-68 refines the TICKET67 429-node quotient cycle instead of treating it as a counterexample. The observed cycle disappears under the `base_prefix_consumed` coordinate: 9,616 refined states, 41,283 refined edges, zero cyclic nodes, and observed topological rank 5. Tail/residue-only refinement still leaves 26 cyclic nodes, so the missing theorem is not merely "more residue bits"; it is a transition-completeness and well-foundedness theorem for the prefix/consumed DAG.

Key Collatz result:

```text
source base transition nodes: 5,100
source base transition edges: 45,665
source base transition weight: 265,812
source cyclic nodes: 429
source cycle edge weight: 89,222
open exits from cycle: 174,589
tested refinement families: 7
strongest acyclic refinement: base_prefix_consumed
base_prefix_consumed states: 9,616
base_prefix_consumed edges: 41,283
base_prefix_consumed cyclic nodes: 0
base_prefix_consumed observed topological rank: 5
best tail/residue-only refinement: tail8_res4096_vexact
tail8_res4096_vexact cyclic nodes: 26
tail8_res4096_vexact cyclic edge weight: 129
full proof status: open
```

Discarded route:

```text
Treat the 429-node TICKET67 cycle as an unavoidable obstruction at every finite refinement. TICKET68 refutes that overstatement on the observed transition set: adding prefix_length and consumed_bits makes the observed internal cycle graph acyclic.
```

Candidate theorem still missing:

```text
PrefixConsumedDAGCompletenessOrPersistentRefinedCycle: every compatible lift inside the TICKET67 SCC is represented by the base_template + prefix_length + consumed_bits refined transition system and decreases its observed DAG rank, or a new persistent refined cycle appears at a higher lift.
```

Counterexample target:

```text
A compatible infinite 2-adic lift whose refined state either escapes the observed prefix/consumed DAG completeness conditions or creates a new refined cycle beyond the current bounded horizon.
```

Remaining decisive target:

```text
CO-TICKET-69 PrefixConsumedDAGCompletenessOrPersistentRefinedCycle
```

Proof boundary:

```text
TICKET-68 does not prove or disprove any of the four open problems. It breaks the observed TICKET67 SCC under a stronger coordinate, but the missing infinite bridge is transition-completeness and well-foundedness for all higher lifts.
```

### Ticket 69: Prefix/consumed rank certificate and frontier audit

CO-TICKET-69 PrefixConsumedDAGCompletenessOrPersistentRefinedCycle

Artifacts:

```text
data/open-problem/ticket69-prefix-consumed-rank-lab.json
data/open-problem/collatz/co-ticket-69-prefix-consumed-rank.json
data/open-problem/riemann/rh-ticket-69-rank-completeness.json
data/open-problem/goldbach/gb-ticket-69-rank-completeness.json
data/open-problem/twin-prime/tp-ticket-69-rank-completeness.json
```

Status:

```text
prefix_consumed_rank_frontier_open_no_resolution
```

한국어 요약: TICKET-69는 TICKET-68의 prefix/consumed DAG를 실제 rank certificate 후보로 검사한다. 결과는 양면적이다. 관측된 내부 edge 89,222개는 모두 rank를 엄격히 감소시킨다. nondecreasing rank edge는 0개이며, rank delta는 1부터 5까지 모두 양수다. 또한 base-cycle source instance 16,967개에서 child는 `internal_rank_descent = 89,222`, `open_base_cycle_exit = 174,589`, `closed_or_terminal_all_lift_descent = 7,661`로 분류된다. 그러나 이 결과는 아직 증명이 아니다. rank 0 상태 6,733개 중 6,649개는 child-only unexpanded frontier로 남는다. 즉 현재 DAG는 관측 내부 edge에 대해서는 rank이지만, 그 frontier의 다음 transition-completeness가 아직 없다.

English summary: TICKET-69 turns the TICKET68 acyclic graph into a stricter rank certificate candidate. All 89,222 observed internal edges strictly decrease the prefix/consumed rank, and there are zero nondecreasing rank edges. The blocking issue is not local rank descent anymore; it is transition-completeness of the frontier. There are 6,649 rank-0 child-only states that still need expansion or theorem-level closure.

Key Collatz result:

```text
coordinate family: base_prefix_consumed
rank states: 9,616
max rank: 5
source base cycle nodes: 429
observed internal edge weight: 89,222
nondecreasing rank edges: 0
source instances in base cycle: 16,967
child outcomes: internal_rank_descent = 89,222; open_base_cycle_exit = 174,589; closed_or_terminal_all_lift_descent = 7,661
source-expanded states: 3,025
source-and-child states: 1,390
source-only states: 1,635
child-only unexpanded states: 6,649
unexpanded child-only rank counts: rank 0 = 6,649
full proof status: open
```

Discarded route:

```text
Promote the observed prefix/consumed DAG directly to a proof. TICKET69 blocks that shortcut: the internal observed edges strictly decrease the DAG rank, but many child-only refined states have not yet been expanded as source states.
```

Candidate theorem still missing:

```text
PrefixConsumedRankCompleteness: every compatible branch represented by a TICKET68 child-only prefix/consumed state has a complete next-transition expansion whose internal children strictly decrease the same DAG rank, or a new refined cycle is produced.
```

Counterexample target:

```text
A higher-lift expansion of an unexpanded child-only prefix/consumed state that re-enters a nondecreasing refined cycle.
```

Remaining decisive target:

```text
CO-TICKET-70 PrefixConsumedFrontierExpansionOrCycle
```

Proof boundary:

```text
TICKET-69 does not prove or disprove any of the four open problems. It validates strict rank descent on observed internal edges, but the unexpanded child-only frontier is the missing infinite bridge.
```

### Ticket 70: Prefix/consumed frontier expansion and direct-rank closure refutation

CO-TICKET-70 PrefixConsumedFrontierExpansionOrCycle

Artifacts:

```text
data/open-problem/ticket70-prefix-frontier-expansion-lab.json
data/open-problem/collatz/co-ticket-70-prefix-frontier-expansion.json
data/open-problem/riemann/rh-ticket-70-frontier-expansion.json
data/open-problem/goldbach/gb-ticket-70-frontier-expansion.json
data/open-problem/twin-prime/tp-ticket-70-frontier-expansion.json
```

Status:

```text
prefix_frontier_expansion_open_no_resolution
```

한국어 요약: TICKET-70은 TICKET-69가 남긴 rank-0 child-only frontier를 실제로 한 단계 확장한다. 기준은 TICKET-69와 동일하다. frontier state는 6,649개이고, 그 state에 도달한 concrete representative는 49,504개다. 각 representative에 4비트 child 16개를 붙여 총 792,064개 branch를 검사했다. 결론은 직접 rank closure의 반박이다. 516,176개 branch는 base cycle 밖으로 exit하고 61,118개는 all-lift descent로 닫히지만, 123,403개는 rank 0으로 재진입하고 31,918개는 rank 1 이상으로 올라간다. 또한 59,449개 branch는 기존 DAG에 없던 unranked internal state로 들어간다. 따라서 "TICKET69 rank-0 sink는 자동 terminal"이라는 shortcut은 버려야 한다.

English summary: TICKET-70 expands the TICKET69 rank-0 child-only frontier by one 4-bit lift. It does not find a combined refined cycle in this one-step audit, but it refutes the direct rank-0 closure shortcut. The expanded frontier has 155,321 known-rank nondecreasing re-entry edges, 59,449 new unranked internal edges, and 3,537 representative-nondeterministic frontier states.

Key Collatz result:

```text
coordinate family: base_prefix_consumed
source frontier states: 6,649
frontier concrete representatives: 49,504
expansion edge weight: 792,064
frontier internal edge weight: 214,770
open base-cycle exits: 516,176
closed all-lift descent branches: 61,118
known-rank nondecreasing re-entry edges: 155,321
  rank-equal re-entry edges: 123,403
  rank-increase re-entry edges: 31,918
new unranked internal edges: 59,449
representative-nondeterministic frontier states: 3,537
combined one-step cycle components: 0
full proof status: open
```

Discarded route:

```text
Treat every TICKET69 rank-0 child-only state as a terminal sink. TICKET70 directly refutes this route: many concrete representatives re-enter ranked or new unranked internal states after one 4-bit expansion.
```

Retained route:

```text
The next useful theorem must add a stronger frontier coordinate, or prove that nondecreasing re-entry pressure cannot persist along compatible infinite lifts. If persistence is possible, extract it as a refined counterexample target.
```

Candidate theorem still missing:

```text
StrongerFrontierCoordinateOrPersistentLiftCycle: every compatible expansion of a TICKET70 rank-0 frontier state is separated by a pre-replay coordinate that supplies a well-founded rank, or it admits a compatible infinite lift cycle/re-entry chain.
```

Counterexample target:

```text
A compatible higher-lift path that starts in one of the rank-0 child-only prefix/consumed states and repeatedly re-enters known ranked or new unranked internal states without descent.
```

Remaining decisive target:

```text
CO-TICKET-71 StrongerFrontierCoordinateOrPersistentLiftCycle
```

Proof boundary:

```text
TICKET-70 does not prove or disprove any of the four open problems. It refutes a direct frontier-closure shortcut and narrows the next target to a stronger coordinate or a persistent lift-cycle extraction.
```

### Ticket 71: Stronger frontier coordinates and bounded separator tradeoff

CO-TICKET-71 StrongerFrontierCoordinateOrPersistentLiftCycle

Artifacts:

```text
data/open-problem/ticket71-stronger-frontier-coordinate-lab.json
data/open-problem/collatz/co-ticket-71-stronger-frontier-coordinate.json
data/open-problem/riemann/rh-ticket-71-stronger-frontier-coordinate.json
data/open-problem/goldbach/gb-ticket-71-stronger-frontier-coordinate.json
data/open-problem/twin-prime/tp-ticket-71-stronger-frontier-coordinate.json
```

Status:

```text
stronger_frontier_coordinate_open_no_resolution
```

한국어 요약: TICKET-71은 TICKET-70의 재진입 압력을 outcome label 없이 분리할 수 있는지 검사한다. 시험한 좌표는 `base_prefix_consumed`, residue mod `2^12`, residue mod `2^16`, tail8+residue, tail12+residue, full valuation word+residue mod `2^16`이다. 결과는 tradeoff다. compact한 `base_prefix_consumed`는 expanded graph를 acyclic하게 유지하고 rank 7을 만들며 child-only frontier를 8,055개로 가장 작게 유지한다. 하지만 mixed transition key가 22,219개 남는다. 반대로 `base_fullword_residue65536`은 bounded transition key를 완전히 분리해서 mixed key 0개를 만든다. 그러나 state count가 319,801개, child-only frontier가 254,488개로 폭증한다. 따라서 "분리 가능한 좌표가 있다"와 "증명 가능한 compact invariant가 있다"는 같은 말이 아니다.

English summary: TICKET-71 finds a bounded separator but not a proof. The full valuation-word plus residue mod `2^16` coordinate gives zero mixed transition keys across the TICKET70 branch set, but it overfits the bounded data and expands the child-only frontier. The compact baseline coordinate keeps the expanded graph small and acyclic, but leaves mixed transition keys. The next proof target is an infinite lift-closure theorem for a compact coordinate, or a persistent lift-chain counterexample target extracted from the remaining mixed keys.

Key Collatz result:

```text
frontier source states: 6,649
frontier concrete representatives: 49,504
frontier branch weight: 792,064
pressure rows: 214,770
tested coordinate families: 6
best bounded transition separator: base_fullword_residue65536
best separator mixed transition keys: 0
best separator transition keys: 792,064
best separator child-only frontier: 254,488
best compact frontier reduction: base_prefix_consumed
compact expanded graph rank: 7
compact child-only frontier after expansion: 8,055
compact mixed transition keys: 22,219
full proof status: open
```

Discarded route:

```text
Treat a large full-word separator as a Collatz proof. TICKET71 blocks that shortcut: the coordinate separates the bounded branch set but explodes the frontier and still has no infinite lift-closure theorem.
```

Retained route:

```text
Either prove that a compact coordinate such as base_prefix_consumed has horizon-independent lift closure after frontier expansion, or extract a persistent lift chain from the mixed transition keys that survive compact coordinates.
```

Candidate theorem still missing:

```text
InfiniteFrontierCoordinateLiftClosureOrChain: every compatible future lift of the expanded frontier is closed by a compact pre-outcome coordinate with a well-founded rank, or there exists a compatible infinite chain through a mixed transition key.
```

Counterexample target:

```text
A repeated lift chain through a mixed transition key or child-only expanded state that survives every tested low-residue and valuation-word coordinate without descent.
```

Remaining decisive target:

```text
CO-TICKET-72 InfiniteFrontierCoordinateLiftClosureOrChain
```

Proof boundary:

```text
TICKET-71 does not prove or disprove any of the four open problems. It identifies a bounded coordinate separator and a compact-coordinate obstruction; the infinite lift theorem remains missing.
```

### Ticket 72: Infinite-frontier lift closure and persistent mixed-key pressure

CO-TICKET-72 InfiniteFrontierCoordinateLiftClosureOrChain

Artifacts:

```text
data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json
data/open-problem/collatz/co-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/riemann/rh-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/goldbach/gb-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/twin-prime/tp-ticket-72-infinite-frontier-lift-closure.json
```

Status:

```text
infinite_frontier_lift_closure_open_no_resolution
```

한국어 요약: TICKET-72는 TICKET-71의 남은 compact mixed key가 단순한 1단계 관측 착시인지, 아니면 lift를 해도 계속 남는 구조적 압력인지 검사한다. 중요한 논리 수정은 `pressure_rank_descent`를 열린 압력에서 제외한 점이다. rank가 내려가는 branch는 증명 관점에서 진전이므로, 열린 압력은 `pressure_rank_equal`, `pressure_rank_increase`, `pressure_new_unranked_internal`만으로 다시 센다. 이 보수적 기준에서도 TICKET70 frontier branch weight 792,064, compact mixed transition key 22,219개, open-pressure mixed transition key 20,752개가 재구성된다. 상위 8개 compact mixed key를 한 단계 lift하면 36,848개 second-layer row가 나오고, 그중 6,857개가 open pressure이며, 4,142개가 open-pressure mixed-key로 재진입한다. 2,048개 source에 대한 제한된 third probe에서도 32,768개 row 중 12,300개 open pressure와 6,448개 open-pressure mixed-key 재진입이 남는다. `base_tail12_residue65536`은 가장 좋은 compact 후보지만 mixed key 540개를 남기고, `base_fullword_residue65536`은 mixed key 0개를 만들지만 overfit guard로만 남는다.

English summary: TICKET-72 does not solve Collatz. It refines the TICKET71 obstruction by separating rank descent from open pressure, then lifting the top compact mixed transition keys. The result is persistent bounded pressure: open-pressure mixed-key re-entry survives the second lift and a capped third probe. This strengthens the next target from "try a bigger coordinate" to a sharper dichotomy: prove a compact mixed-key invariant under all future lifts, or extract a compatible persistent lift chain.

Key Collatz result:

```text
reconstructed frontier branch weight: 792,064
compact mixed transition keys: 22,219
compact open-pressure mixed transition keys: 20,752
selected top mixed keys: 8
first-layer rows selected: 2,512
first-layer pressure rows selected: 2,303
second-layer rows: 36,848
second-layer open-pressure rows: 6,857
second-layer rank-descent rows: 2,021
second-layer mixed-key re-entries: 9,584
second-layer open-pressure mixed-key re-entries: 4,142
third-probe sources: 2,048
third-probe rows: 32,768
third-probe open-pressure rows: 12,300
third-probe rank-descent rows: 342
third-probe mixed-key re-entries: 11,455
third-probe open-pressure mixed-key re-entries: 6,448
best compact candidate: base_tail12_residue65536, 540 mixed keys
bounded overfit guard: base_fullword_residue65536, 0 mixed keys
full proof status: open
```

Discarded route:

```text
Treat rank descent as proof pressure, or treat a full valuation word as a compact invariant. TICKET72 blocks both shortcuts: rank descent is progress, not an obstruction, while the full-word coordinate closes only the bounded rows and has no compact infinite transition theorem.
```

Retained route:

```text
Prove that a compact coordinate such as base_tail12_residue65536 has horizon-independent mixed-key closure, or extract a persistent compatible lift chain from the open-pressure mixed-key re-entries.
```

Candidate theorem still missing:

```text
CompactMixedKeyInvariantOrPersistentLiftChain: every compatible future lift of the TICKET72 compact mixed-key frontier is controlled by a finite pre-outcome coordinate with well-founded descent, or there exists a compatible infinite chain that repeatedly re-enters open-pressure mixed keys.
```

Counterexample target:

```text
A compatible infinite lift chain whose every finite prefix survives the compact coordinates and whose transition profile repeatedly enters pressure_rank_equal, pressure_rank_increase, or pressure_new_unranked_internal without a well-founded descent certificate.
```

Remaining decisive target:

```text
CO-TICKET-73 CompactMixedKeyInvariantOrPersistentLiftChain
```

Proof boundary:

```text
TICKET-72 does not prove or disprove any of the four open problems. It only shows that the compact mixed-key obstruction persists under the tested second and third lifts, so an independently checkable infinite theorem or certified counterexample is still required.
```

### Ticket 73: Lineage-constrained strict re-entry tree

CO-TICKET-73 FiniteRootReentryTreeExtinctionOrKonigWitness

Artifacts:

```text
data/open-problem/ticket73-lineage-pressure-forest-lab.json
data/open-problem/collatz/co-ticket-73-lineage-pressure-forest.json
data/open-problem/riemann/rh-ticket-73-lineage-pressure-forest.json
data/open-problem/goldbach/gb-ticket-73-lineage-pressure-forest.json
data/open-problem/twin-prime/tp-ticket-73-lineage-pressure-forest.json
```

Status:

```text
strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion
```

한국어 요약: TICKET-73은 TICKET-72의 4,142개 open-pressure mixed-key 재진입 row 전체를 root로 삼아, 이전의 2,048개 제한 third probe를 제거했다. 각 root의 자식은 4비트 상위 확장 16개를 모두 정확히 열거하고, 자식 residue가 부모 residue를 mod `2^parent_bits`에서 보존하는지 검사했다. third lift 66,272개 row 중 strict 재진입은 12,911개(1,835개 root), fourth lift 206,576개 row 중 2,873개(614개 root)였다. 이 2,873개를 다시 전부 열어 fifth lift 45,968개를 검사했을 때 strict 재진입은 0개였다. 따라서 선택된 finite root 집합에서 “매 lift마다 open pressure이면서 원래 compact mixed-key로 재진입”하는 무한 사슬은 없다. 이 유한 소거는 Collatz 전체에 대한 결론이 아니다. root가 모든 미해결 Collatz 궤적을 덮는다는 coverage 정리가 없고, strict predicate 밖의 압력 사슬도 배제하지 않았기 때문이다.

English summary: TICKET-73 removes the TICKET-72 third-probe cap by using all 4,142 open-pressure mixed-key re-entry rows as roots. It enumerates all sixteen exact four-bit congruence extensions at each retained node and checks parent-child residue compatibility. The all-root third lift has 66,272 rows with 12,911 strict re-entries across 1,835 roots; the fourth lift has 206,576 rows with 2,873 strict re-entries across 614 roots; the fifth lift has 45,968 rows with zero strict re-entries. Hence no infinite chain through this selected finite root set can satisfy the strict condition of open pressure plus re-entry to the original compact mixed-key predicate at every lift. This is a finite elimination of one counterexample route, not a Collatz proof: no coverage theorem connects these roots to every unresolved trajectory, and other pressure predicates remain possible.

Exact finite result:

```text
selected strict roots: 4,142
third lift:  66,272 rows, 12,911 strict re-entries, 1,835 surviving roots
fourth lift: 206,576 rows, 2,873 strict re-entries, 614 surviving roots
fifth lift:  45,968 rows, 0 strict re-entries, 0 surviving roots

bounded lemma: the selected strict re-entry tree is empty at the fifth retained lift.
```

Discarded route:

```text
Treat the TICKET72 repeated re-entry counts as evidence for an infinite chain. The all-root strict tree is exactly empty at its fifth retained lift, so that particular persistent-chain specification cannot supply a Collatz counterexample.
```

Retained route:

```text
Either prove that a theorem-level coverage certificate reduces every unresolved Collatz trajectory to a finite collection of exactly exhaustible root trees, or define a different pressure predicate and prove nonempty compatible descendants at every depth before invoking Konig's lemma.
```

Candidate theorem still missing:

```text
CoverageCertificateAndAllDepthReentryTreeDecision: every unresolved Collatz trajectory is covered by a finite, exact congruence-root family whose admissible pressure tree either becomes empty at a finite lift or is nonempty at every depth; only the latter permits an infinite compatible path by Konig's lemma, and an additional dynamical argument is required to turn that path into a counterexample.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
Bounded survivors are not theorem candidates until their frontier coverage, lineage compatibility, and all-scale decision rule are separately established. Ticket 73 records those obligations on all four pages but transfers no Collatz counts to the other problems.
```

Proof boundary:

```text
TICKET-73 does not prove or disprove any of the four open problems. It proves only a finite extinction statement for a precisely selected Collatz re-entry predicate and leaves the global coverage and infinite-theorem obligations open.
```

### Ticket 74: Coverage leakage and escaping-pressure forest

CO-TICKET-74 FiniteRootCoverageLeakageOrEscapingPressureForest

Artifacts:

```text
data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json
data/open-problem/collatz/co-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/riemann/rh-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/goldbach/gb-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/twin-prime/tp-ticket-74-coverage-leakage-escape-forest.json
```

Status:

```text
strict_cover_leakage_and_sixth_pressure_persistence_observed_no_global_resolution
```

한국어 요약: TICKET-74는 TICKET-73의 strict 재진입 트리 소거가 전체 pressure closure인지 검사한다. 결론은 아니다. TICKET73의 4,142개 root는 T70의 open-pressure mixed key 20,752개 중 상위 8개에서 나온다. key 기준 coverage는 `8 / 20,752 = 0.038551%`, first-layer row 기준은 `2,512 / 371,343 = 0.676464%`, first-layer open-pressure row 기준은 `2,303 / 180,385 = 1.276714%`다. strict tree의 fifth lift는 열린 압력 15,696개를 남기지만, 기존 compact mixed-key cover 재진입은 0개다. 그중 15,593개(99.343782%)가 새 `pressure_new_unranked_internal` 상태로 빠져나간다. 이 escape 15,696개를 전부 sixth lift로 확장하면 251,136개 row 중 열린 압력 78,315개가 남고, 기존 cover 재진입은 5개뿐이다. 따라서 strict predicate의 유한 소거는 전역 pressure 소거나 전역 coverage 정리가 아니다.

English summary: TICKET-74 tests whether the TICKET-73 strict re-entry-tree extinction is actual pressure closure. It is not. The 4,142 TICKET73 roots arise from only the top 8 of 20,752 T70 open-pressure mixed keys: `8 / 20,752 = 0.038551%` by key, `2,512 / 371,343 = 0.676464%` by first-layer row, and `2,303 / 180,385 = 1.276714%` by first-layer open-pressure row. The strict tree's fifth lift leaves 15,696 open-pressure rows but zero re-entries to the original compact mixed-key cover; 15,593 rows (99.343782%) enter new unranked internal states. Expanding all 15,696 escapes produces 251,136 sixth-lift rows with 78,315 open-pressure rows and only 5 old-cover re-entries. Strict-predicate extinction is therefore not global pressure extinction or a coverage theorem.

Exact coverage and leakage result:

```text
T70 open-pressure mixed keys: 20,752
TICKET73 selected keys: 8 (0.038551%)
selected first-layer rows: 2,512 / 371,343 (0.676464%)
selected first-layer open-pressure rows: 2,303 / 180,385 (1.276714%)

fifth lift: 45,968 exact rows, 15,696 open pressure, 0 old-cover re-entries,
             15,593 new unranked internal states, 0 extension-compatibility failures
sixth lift: 251,136 exact rows, 78,315 open pressure, 5 old-cover re-entries,
             78,315 new unranked internal states, 0 extension-compatibility failures
```

Discarded route:

```text
Infer global Collatz closure from the TICKET73 strict-tree extinction. TICKET74 gives an exact counterexample to that inference: the old compact cover does not contain the fifth-lift open-pressure successors.
```

Retained route:

```text
Prove a horizon-independent global coverage certificate for every escaping needs_split state, or define a larger pressure predicate whose exact compatible forest can be shown empty at finite depth or nonempty at every depth.
```

Candidate theorem still missing:

```text
GlobalCoverageCertificateOrEscapingPressureForestDecision: every unresolved Collatz trajectory is covered by a fixed, exact congruence-state family with a well-founded descent coordinate, or every escaping successor belongs to a precisely defined pressure forest whose all-depth compatible paths are decided. Any surviving path still requires a separate proof that it represents divergence or a nontrivial cycle.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
Every bounded zero, exceptional-even, or exact-gap frontier must prove successor closure under its claimed cover. A bounded extinction result that merely leaks to untracked states is not a theorem for any of the four problems.
```

Proof boundary:

```text
TICKET-74 does not prove or disprove any of the four open problems. It refutes one invalid globalization step, records an exact escaping-pressure forest through the sixth lift, and leaves the required global coverage theorem open.
```

### Ticket 75: Fixed finite coordinate closure audit

CO-TICKET-75 EscapeCoordinateClosureOrNovelClassGrowth

Artifacts:

```text
data/open-problem/ticket75-escape-coordinate-closure-lab.json
data/open-problem/collatz/co-ticket-75-escape-coordinate-closure.json
data/open-problem/riemann/rh-ticket-75-escape-coordinate-closure.json
data/open-problem/goldbach/gb-ticket-75-escape-coordinate-closure.json
data/open-problem/twin-prime/tp-ticket-75-escape-coordinate-closure.json
```

Status:

```text
all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution
```

한국어 요약: TICKET-75는 TICKET-74의 fifth-lift 열린 압력 15,696개와 sixth-lift 열린 압력 78,315개를 exact congruence extension 실패 0개로 다시 재생했다. 기존 `base_prefix_consumed` DAG 좌표는 exact `prefix_length`와 `consumed_bits`를 포함하므로 고정 유한 상태가 아니라는 점을 명시적으로 강등했다. 대신 valuation tail, low residue, clipped next valuation, prefix/consumed modular data만 사용하는 고정 유한 pre-outcome 좌표 8개를 시험했다. 어느 좌표도 관측된 successor closure, projected-cycle exclusion, pressure-outcome determinism을 동시에 통과하지 못했다. 가장 거친 좌표는 새 sixth row가 `11 / 78,315`뿐이지만 cyclic node 66개와 mixed key 59개를 남겼다. 가장 세밀한 좌표는 mixed key를 4개까지 줄였지만 `77,998 / 78,315` row가 관측 source cover 밖의 새 class로 빠졌다. 이것은 시험한 coordinate grammar의 압축-상태성장 trade-off이며 Collatz 전체에 관한 정리가 아니다.

English summary: TICKET-75 exactly replays all 15,696 fifth-lift and 78,315 sixth-lift open-pressure rows from TICKET74 with zero congruence-extension failures. It demotes the earlier `base_prefix_consumed` DAG coordinate because exact prefix and consumed lengths make it an unbounded diagnostic rather than a fixed finite state. Eight fixed finite pre-outcome coordinates built from clipped valuation tails, low residues, clipped next valuations, and modular prefix/consumed data are tested instead. None passes observed successor closure, projected-cycle exclusion, and pressure-outcome determinism simultaneously. The coarsest coordinate leaks only `11 / 78,315` sixth-lift rows but retains 66 cyclic nodes and 59 mixed keys. The richest coordinate reduces mixed keys to four but sends `77,998 / 78,315` rows into classes outside the observed source cover. This is a finite compression-versus-state-growth obstruction for the tested grammar, not a Collatz theorem.

Exact result:

```text
fifth open pressure: 15,696
sixth open pressure: 78,315
source identity failures: 0
exact extension failures: 0
fixed finite coordinate families tested: 8
two-layer closure gates passed: 0

coarsest family: 11 novel rows, 66 cyclic nodes, 59 mixed keys
richest family: 77,998 novel rows, 373 cyclic nodes, 4 mixed keys
```

Discarded route:

```text
Treat a bounded DAG rank that contains exact growing lengths as a finite automaton, or choose a coordinate only because it is collision-free at one horizon. A valid induction coordinate must be fixed, successor-closed, outcome-sufficient, and well-founded for every compatible lift.
```

Retained route:

```text
Derive a symbolic successor formula and prove a horizon-independent closure/rank theorem, or construct a nonempty exact compatible pressure tree at every depth and then separately prove that one path represents divergence or a nontrivial cycle.
```

Candidate theorem still missing:

```text
SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath: a fixed pre-outcome coordinate covers every compatible open-pressure successor and carries a strictly decreasing well-founded rank, or there exists an all-depth exact compatible pressure path escaping every certified cover.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
TICKET75 performs no problem-specific coordinate computation for these three problems. Their TICKET75 artifacts transfer only the rule that bounded or horizon-dependent state summaries cannot be promoted without a problem-specific all-height successor theorem.
```

Proof boundary:

```text
TICKET-75 proves or disproves none of the four open problems. It falsifies eight finite Collatz coordinate candidates and identifies a measurable coordinate-design obstruction.
```

### Ticket 76: Exact boundary quotient recurrence

CO-TICKET-76 FourBitBoundaryQuotientRecurrenceAndFixedPrecisionLoss

Artifacts:

```text
data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json
data/open-problem/collatz/co-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/riemann/rh-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/goldbach/gb-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/twin-prime/tp-ticket-76-symbolic-boundary-recurrence.json
```

Status:

```text
symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution
```

한국어 요약: TICKET-76은 TICKET75의 압축-상태성장 현상을 exact arithmetic으로 설명한다. modulus `2^b`에서 누적 consumed bits가 `b`에 닿는 valuation은 상위 bit lift에서 바뀔 수 있으므로 먼저 equality step을 rollback하여 lift-stable prefix를 정의한다. 그 prefix의 길이를 `m`, consumed bits를 `s`, `d=b-s`, `A=(3T^m(r)+1)/2^d`, `u=3^(m+1)`라 두면 상위 네 비트 digit `h`를 붙인 자식의 첫 새 valuation은 정확히 `d+v2(A+hu)`다. `v2(A+hu)>4`이면 자식은 같은 prefix에서 미해결이고 다음 quotient는 `(A+hu)/16`이다. fifth/sixth source의 297,104개 자식을 전부 검사한 결과 prefix replay, affine identity, valuation, recurrence failure는 0개였다. 하지만 quotient precision `q=5,9,13,17,21`은 각각 165, 1,536, 1,235, 106, 15개의 reachable successor collision key를 남겼다. 같은 row에서 `q+4`비트를 제공하면 collision은 모두 0개다. 따라서 fixed low-bit repair는 재귀적으로 닫히지 않는다.

English summary: TICKET-76 derives the exact first-boundary recurrence behind the TICKET75 compression-versus-state-growth obstruction. A valuation whose cumulative consumption exactly reaches `b` is not lift-stable, so the audit first rolls that equality step back. For the resulting stable prefix, `T^m(r+h2^b)=T^m(r)+h3^m2^(b-s)`. With `d=b-s`, `A=(3T^m(r)+1)/2^d`, and `u=3^(m+1)`, the first new valuation is `d+v2(A+hu)`. If it remains unresolved after a four-bit lift, then `A_next=(A+hu)/16`. All 297,104 audited children satisfy the replay and recurrence identities with zero failures. Fixed quotient precisions `q=5,9,13,17,21` have 165, 1,536, 1,235, 106, and 15 reachable collision keys, while `q+4` lookahead has zero collisions in every case.

Exact finite and symbolic result:

```text
fifth source rows:  2,873 sources, 45,968 children, 1,398 unresolved-same-prefix
sixth source rows: 15,696 sources, 251,136 children, 7,751 unresolved-same-prefix
combined transition rows: 297,104
prefix/affine/valuation/recurrence failures: 0

fixed-q collision keys:
q=5: 165
q=9: 1,536
q=13: 1,235
q=17: 106
q=21: 15
q+4 lookahead collisions: 0 for every tested q
```

Discarded route:

```text
Append a fixed number of low boundary-quotient bits to the TICKET75 coordinate. On an unresolved lift, division by 16 exposes four new higher bits, and exact reachable witnesses show that the fixed-q successor is not determined.
```

Retained route:

```text
Prove that the reachable boundary quotients occupy a restricted arithmetic subset on which a finite quotient closes, or retain the full 2-adic quotient and find a separate well-founded rank. The counterexample route is an exact all-depth compatible path in this recurrence followed by a separate integer-dynamical proof.
```

Candidate theorem still missing:

```text
ReachableBoundaryRestrictionOrTwoAdicPressurePath: reachable Collatz boundary quotients obey a uniform arithmetic restriction yielding finite successor closure and strict descent, or the exact 2-adic recurrence admits an all-depth compatible pressure path requiring separate divergence/cycle classification.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
No TICKET76 arithmetic or counts are transferred. Only the requirement to account for information lost under each problem's exact scale/refinement recurrence is transferred.
```

Proof boundary:

```text
TICKET-76 proves the displayed recurrence identity and bounded collision statements. It does not prove Collatz, produce a divergent integer orbit, or solve any of the other three problems.
```

### Ticket 77: Fixed stable-prefix boundary orbit classification

CO-TICKET-77 FixedStablePrefixBoundaryOrbitAndTwoAdicGhostClassification

Artifacts:

```text
data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json
data/open-problem/collatz/co-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/riemann/rh-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/goldbach/gb-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/twin-prime/tp-ticket-77-fixed-prefix-boundary-orbit.json
```

Status:

```text
fixed_prefix_boundary_orbit_classified_no_collatz_resolution
```

한국어 요약: TICKET-77은 TICKET76의 경계 몫 재귀식을 고정 stable prefix 전체에서 분류한다. `u=3^(m+1)`이고 `h(A)`가 `A+h(A)u = 0 mod 16`을 만족하는 유일한 4비트 digit일 때 `P(A)=(A+h(A)u)/16`이다. Reachability에서 `3∤A`이고 `A>u`이면 `P(A)<A`다. `A<u`에서는 `16^(-1)A mod u`의 최소 양의 대표이며 LTE로 주기가 정확히 `3^m`임을 얻는다. 첫 초안은 홀수 `P(A)`를 stable-prefix extinction으로 잘못 승격했다. 실제로 홀수는 valuation이 현재 modulus 경계에 정확히 닿는 equality 사건이며, TICKET76 규칙에 따라 rollback된다. 따라서 strict pressure 구간만 끝나고 정규화된 fixed-prefix 궤도는 계속된다. all-depth compatible cylinder는 `T^m(N)=-1/3`인 2-adic ghost로 수렴하며 양의 정수가 아니다.

English summary: TICKET-77 classifies the TICKET76 recurrence for a fixed stable prefix. The map contracts while `A>u` and then becomes the inverse-16 orbit modulo `u=3^(m+1)`, with exact period `3^m`. Odd successors end only strict-beyond-boundary runs; the equality valuation is rolled back and the normalized orbit continues. Its compatible limit is a 2-adic preimage of `-1/3`, not a positive integer.

Exact audit:

```text
reconstructed fifth/sixth boundary sources: 18,569
strict segments reaching equality:          18,569
maximum strict-pressure steps:               15
prerequisite failures:                       0
one-step identity failures:                  0
unexpected strict cycles:                    0
trace-guard failures:                        0
finite orbit audit:                          m=0,...,10, failures 0
```

Discarded route:

```text
Treat odd P(A) as extinction of the stable prefix. It is an equality-boundary event whose valuation must be rolled back before the next lift.
```

Closed counterexample route:

```text
Promote a fixed-prefix all-depth compatible cylinder directly to a natural-number counterexample. Its exact completion is a 2-adic preimage of -1/3, not a positive integer.
```

Candidate theorem still missing:

```text
ChangingPrefixNaturalAdmissibilityRank: every positive-integer boundary refinement enters the known basin or strictly decreases a global rank, while every nondecreasing compatible limit is proved non-natural.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
No TICKET77 Collatz orbit theorem or count is transferred. The other artifacts record only the discipline of classifying normalized recurrent states and testing whether completion points are admissible for the original problem.
```

Proof boundary:

```text
TICKET-77 classifies fixed-prefix compatible completions as 2-adic ghosts. It does not exclude infinitely many changing-prefix events, divergence, or nontrivial accelerated cycles, and it proves or disproves none of the other three open problems.
```

### Ticket 78: Finite-cylinder natural-admissibility no-go

CO-TICKET-78 FiniteValuationCylinderNaturalDensityNoGo

Artifacts:

```text
data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json
data/open-problem/collatz/co-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/riemann/rh-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/goldbach/gb-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/twin-prime/tp-ticket-78-finite-cylinder-admissibility-no-go.json
```

Status:

```text
finite_two_adic_natural_separator_refuted_exactly_no_collatz_resolution
```

한국어 요약: positive accelerated valuation word `a=(a_1,...,a_m)`와 `S=sum a_i`에 대해 affine composition은 `T^m(n)=(3^m n+C_m)/2^S`다. terminal odd 조건은 유일한 cylinder `n=r_a mod 2^(S+1)`를 주고, 이 cylinder에는 `r_a+q2^(S+1)` 꼴의 양의 정수가 무한히 많다. 따라서 fixed residue bits, finite valuation/parity word, continuous finite-state 2-adic classifier는 TICKET77 ghost의 비자연성을 인증할 수 없다. 모든 유한 2-adic neighborhood에 자연수가 있기 때문이다.

English summary: Every finite accelerated valuation word defines one exact residue class modulo `2^(S+1)`, and that class contains infinitely many positive integers. Positive integers are dense in `Z_2`, so no locally constant finite-prefix classifier can accept every positive integer and reject a TICKET77 ghost.

Exact audit:

```text
total valuation S:                 1,...,16
finite valuation words:           65,535
expected composition count:       65,535
positive representatives replayed: 262,140
residue collisions:               0
formula failures:                 0
representative replay failures:   0
count-identity failures:           0
```

Literature boundary:

```text
The 2-adic shift conjugacy is established by Bernstein and Lagarias. TICKET78 claims no rediscovery. Its project-specific role is to connect finite accelerated valuation cylinders to the corrected TICKET77 boundary state and enforce a no-go guard.
```

Discarded route:

```text
Any natural-admissibility classifier or rank that factors through fixed residue bits, a finite parity/valuation word, or another continuous finite-state coordinate on Z_2.
```

Candidate theorem still missing:

```text
ArchimedeanTwoAdicCoupledDescent: every positive-integer accelerated trajectory enters the known basin or strictly decreases a well-founded rank using both Archimedean height and growing 2-adic precision; the rank cannot factor through a fixed finite 2-adic quotient.
```

Transfer discipline:

```text
No Collatz formula, count, density theorem, or conclusion is transferred to RH, Goldbach, or Twin Prime. Their artifacts record only a requirement to prove a problem-specific local-to-global obstruction before using the analogy.
```

Proof boundary:

```text
TICKET-78 proves a proof-route no-go lemma. It does not construct the required coupled rank, prove Collatz, or solve any of the other three problems.
```
## TICKET79: bounded Archimedean-two-adic one-step rank no-go

TICKET79 attacks the first rank class left open by TICKET78:

```text
R(n)=alpha*log(n)+b(s(n))
```

For a finite state set and bounded correction, all coefficient signs fail. The exact expansion family `2^(m+1)q-1` gives arbitrarily long valuation-1 blocks; the exact nonterminal contraction family `(5*2^(2r+1)-1)/3` maps to 5; and the zero-log finite-state case fails by pigeonhole repetition. This is a theorem about the proposed rank family, not about Collatz itself.

The next accepted route is a minimal-counterexample contrapositive. Assuming a least counterexample `N`, every valuation prefix must obey

```text
2^S*N <= 3^m*N+C_m.
```

TICKET80 must combine these inequalities with exact cylinder congruences. A finite-horizon fit, bounded residue table, or an unbounded correction without a proved lower bound is not an acceptable proof object.
## TICKET80: least-counterexample finite-prefix compactness no-go

TICKET80 attacks the direct contrapositive proposed after TICKET79. A least counterexample must satisfy `A^j(N)>=N` for every prefix, but every finite subset of those inequalities remains satisfiable above every finite lower bound:

```text
n=2^(H+1)*ceil((B+1)/2^(H+1))-1
A^j(n)=3^j*2^(H+1-j)*q-1>n for 1<=j<=H.
```

The nested `q=1` witnesses escape to infinity in ordinary size while converging to `-1` in `Z_2`. Thus finite satisfiability and 2-adic compactness do not produce a positive counterexample or a contradiction. A positive ordinary limit requires eventual stabilization of the least nonnegative cylinder residues.

The next accepted route must track one fixed stabilized integer and derive a horizon-independent upper bound. Repeating a finite-prefix search at a larger bound is no longer an admissible proof strategy.

## TICKET81: Mersenne first-compensation no-go

TICKET81 tests the first positive-integer stabilization repair suggested by TICKET80. Let `N_k=2^k-1`. The first `k-1` accelerated steps have valuation one and satisfy

```text
A^j(N_k)=3^j*2^(k-j)-1>N_k, 1<=j<=k-1.
```

The exact cylinder modulus at that depth is `2^k=N_k+1`, so its least residue is already the positive integer `N_k`. Nevertheless,

```text
A^k(N_k)=oddpart(3^k-1)
a_k=2 for odd k
a_k=3+v2(k) for even k.
```

The first compensation step descends exactly for `k in {2,4,8}`. It does not descend for every odd `k>=3`, for `k=6`, or for any even `k>=10`. The latter infinite class follows from `2^(2+v2(k))<=4k` and `(3^k-1)/(4k)>2^k-1`.

Rejected candidate theorem:

```text
The first non-1 valuation after any sufficiently long stabilized expansion block forces descent.
```

Accepted next target:

```text
MersenneAdaptiveCompensationWindow: prove an explicit cumulative valuation window L(k) sends every Mersenne start below itself.
```

Even if established, this target is an infinite-family theorem only. Extending it from Mersenne starts to every stabilized positive cylinder without a separate argument would reintroduce the full Collatz conjecture.

## TICKET82: fixed Mersenne compensation-window no-go

TICKET82 refutes every constant-window repair of TICKET81. For the reference exponent `k=3`, the first post-compensation value is 13 and its additional valuation word is `3,4,2,2,...`. The symbolic family

```text
x_t(k)=A^(k+t)(2^k-1)=(3^(k+t)+c_t)/2^d_t
c_(t+1)=3*c_t+2^d_t
```

is preserved through any fixed horizon `H` by the explicit progression `k=3 mod 2^(2H+3)` for `H>=2`. Since each fixed symbolic iterate grows like `3^k` divided by a constant while the start grows like `2^k`, every sufficiently large exponent in that progression remains above its start through the whole window.

Therefore Mersenne post-expansion stopping delay is unbounded. The route “choose a large but constant lookahead” is permanently rejected. The next admissible target is

```text
MersenneGrowingWindowDescent: construct an explicit unbounded L(k) and prove some post-expansion iterate through L(k) lies below 2^k-1.
```

This does not imply divergence; each constructed finite prefix may descend later. It also does not transfer a Collatz theorem to the other three problems.

## TICKET83: Mersenne half-log delay lower bound

For `k_H=3+2^(2H+3)`, the TICKET82 symbolic family satisfies `|c_t|<2^d_t` and `d_t<=2H+4`. Since `k_H>=4H+11`, exact integer inequalities give every post-expansion iterate through `H` above its start. As `k_H<2^(2H+4)`,

```text
D(k_H)>H>(1/2)*log2(k_H)-2.
```

This rejects every universal `o(log k)` Mersenne window and every logarithmic coefficient below `1/2`. The coefficient is certified, not claimed optimal. The next target is `MersenneLogWindowDichotomy`: optimize the lower coefficient and seek or refute a finite logarithmic upper coefficient for all Mersenne exponents.

## TICKET84: accessible 2-adic cycle and two-thirds log bound

The odd 2-adic equation `3^kappa=-13` produces the post-value cycle `-7 -> -5 -> -7` with valuation word `2,1`. Unique finite exponent residues modulo `2^(d_H-1)` preserve this word through `H`; adding one period produces positive ordinary exponents. The ghost is never classified as natural. Exact affine and growth bounds give

```text
D(k_H)>H>(2/3)*log2(k_H)-1.
```

Thus every coefficient below `2/3` fails infinitely often. The next target classifies all periodic valuation words whose cycles lie in the 2-adic exponent image and optimizes reciprocal mean valuation.

## TICKET85: accessible cycle coefficient supremum

The exact family `w_m=(2,1^(m-1))` has cycle value `C_m/(2^(m+1)-3^m)`, is `1 mod 8`, and has reciprocal mean `m/(m+1)`. Therefore the accessible coefficient supremum is 1. It is not attained because the all-ones fixed point `-1` targets `7 mod 8`, outside the odd exponent image. Choosing `m=H` gives

```text
D(k_H)>H>log2(k_H)-2.
```

All subunit logarithmic coefficients, even with arbitrary fixed additive constants, are rejected. The next target is the coefficient-one additive boundary and a separate universal Mersenne upper bound.

## TICKET86: infinite coefficient-one Mersenne delay

The cycle target at horizon `H` reduces exactly to the fixed congruence

```text
3^(r_H+1) = -7 mod 2^(H+3).
```

The least odd residues are nested: the next lift either keeps `r_H` or adds the new top bit. Top-bit additions occur infinitely often, because eventual stabilization at a positive ordinary integer `r` would make `3^(r+1)+7` divisible by arbitrarily high powers of two and hence force the impossible equality `3^(r+1)=-7`.

At every top-bit height, `2^H<=r_H<2^(H+1)`. The exact valuation prefix, affine constant bound, and elementary growth estimate prove

```text
D(r_H)>H,
D(r_H)>=H+1>log2(r_H).
```

This refutes `D(k)<=log2(k)` on an infinite Mersenne-exponent subsequence. It does not refute `D(k)<=log2(k)+C` for a positive constant, does not construct a divergent orbit, and does not resolve Collatz. The next target is `TwoAdicDigitRunBoundary`: connect binary zero-run structure of the fixed 2-adic logarithm to an unbounded additive delay excess, or produce a rigorous obstruction.

## TICKET87: two-adic digit runs and additive-one delay

The fixed exponent solving `3^(r+1)=-7` has infinitely many one bits and infinitely many zero bits. Finitely many one bits would stabilize the nested residues at a nonnegative integer. Finitely many zero bits would make the exponent an eventually-all-one negative integer. Either case turns the 2-adic equation into an impossible rational equality.

Consequently one-to-zero transitions occur infinitely often. At each transition the same positive exponent preserves the exact valuation prefix for one additional horizon. Reusing the affine growth bound and integrality of the delay gives

```text
D(k)>log2(k)+1
```

for infinitely many positive odd exponents. A zero run of length `L` gives the more general finite bound `D(k)-log2(k)>min(L,k-H-2)`. The 262,144-height audit observes a length-16 run and certifies one finite excess above 16, but this does not prove unbounded run length. The next target is infinitude of the `100` pattern, which would cross additive constant 2 on an infinite subsequence.

## TICKET88: run-length-two promotion no-go

Two-sided digit infinitude does not imply `100` recurrence. The explicit digit sequence with zeros at square positions is non-eventually-periodic, has infinitely many zeros and ones, and has no adjacent zeros. The natural dual exponent `s=-r` complements every bit above bit zero, but its post-value `-5/7` enters the exact accelerated cycle `5/7 -> 11/7 -> 5/7` with valuation word `(1,3)`. Its reciprocal mean is `1/2`, so the coefficient-one delay geometry is not preserved.

TICKET88 therefore rejects both the generic symbolic inference and the complement transfer. The next theorem must use the arithmetic identity of the specific fixed logarithm:

```text
FixedLogGoldenMeanExclusion:
for every H0, some h>=H0 has r_h r_(h+1) r_(h+2)=100.
```

The 32,753 finite observed runs of length at least two are falsification evidence only.

## TICKET89: fixed-log golden-mean valuation reduction

For consecutive top-bit heights `H<J` and the positive least residue `k=r_H`, exact lift failure at `J` gives

```text
v2(3^(k+1)+7)=J+2,
v2(3^(k+1)+7)-floor(log2(k))=(J-H-1)+3.
```

Therefore `100` at `H` is equivalent to valuation excess at least five. Eventual golden-mean membership is equivalent to an eventual excess cap of four. The no-`00` subshift contains uncountably many transcendental 2-adic numbers and has positive entropy, so transcendence and counting alone cannot contradict the cap. The next theorem is `FixedLogValuationExcessFiveInfinitude` for the exact nested residues.

## TICKET90: normalized-error ghost-lasso no-go

Define `e_H=(3^(r_H+1)+7)/2^(H+3)`. Its parity is the next lift bit, and its exact branch recurrence is forced by `A_H=(3^(2^(H+1))-1)/2^(H+3)`. The identity `A_(H+1)=A_H+2^(H+2)A_H^2` yields the limiting odd forcing constant `beta=-7 log_2adic(-3)/4`. The limiting map fixes `e=beta`, so every fixed precision contains a target-avoiding lasso. Any continuation must use precision growing with H and quantitatively separate the actual error orbit from this ghost.

## TICKET91: error-tail conjugacy and invariant-set correction

Let `R` be the fixed 2-adic solution of `3^(R+1)=-7` and write `R=r_H+2^(H+1)t_H`. Substitution gives

```text
e_H = 7(1-(1+2^(H+3)A_H)^(-t_H))/2^(H+3),
e_H = 7A_H t_H (mod 2^(H+3)),
e_H = gamma t_H (mod 2^(H+2)),
gamma = 7 log_2adic(-3)/4.
```

The tail update is the one-sided binary shift. Multiplication by odd `gamma` conjugates it to the limiting normalized-error map. Hence `beta=-gamma` corresponds exactly to `t=-1`, the all-one tail. Distance from beta measures only the number of initial future one bits, so beta separation cannot force `00`.

The complete target-avoiding set is the golden-mean subshift `G` of tails without `00`; its error-coordinate image `gamma G` is invariant and has `F_(n+2)` words at depth `n`. TICKET91 therefore retires `GrowingPrecisionErrorGhostSeparation` as insufficient and replaces it with `GoldenMeanInvariantSetEscape`. No `00` recurrence, additive-two infinite delay result, or Collatz theorem is claimed.

## TICKET92: scale-sensitive threshold correction

For Collatz, consecutive top-bit heights `H<J` give

```text
Delta_H = v2(R-r_H)-floor(log2(r_H)) = J-H.
```

The `100` target is exactly `Delta_H>=3`. Dividing by `H` produces `1+Delta_H/H`, which converges to one for every bounded defect and therefore cannot distinguish the target from an eventual no-`00` sequence. The next admissible target is `FixedLogSecondOrderDefectRecurrence`; first-order irrationality exponents and upper-bound linear-form estimates are retired for this constant-additive event.

For Twin Prime, the former TP-TICKET-14 threshold `M_k>2/k` was not Maynard's criterion. Proposition 4.2 uses `ceil(theta*M_k/2)`. With unconditional `theta<1/2`, a two-prime conclusion requires a certified strict `M_k>4` in the limiting threshold. The 17 legacy scores were not variational certificates, so all implied bounded gaps were removed. A valid bounded-gap certificate would still not isolate exact gap 2; the remaining target is a parity-breaking exact-pair correlation lower bound.

## TICKET93: exact twin-correlation excess bridge

Set `C_2(x)=sum Lambda(n)Lambda(n+2)`. Proper prime powers contribute at most

```text
B(x)=2 sqrt(x+2) floor(log2(x+2)) log^2(x+2).
```

Thus unbounded `C_2(x)-B(x)` forces the genuine twin-prime weight to be unbounded and proves twin-prime infinitude. The bridge is exact and unconditional, but the required lower bound remains open.

The truncated divisor surrogate `Lambda_R=sum_{d|n,d<=R}mu(d)log(R/d)` is not a minorant. For every tested truncation it exceeds `Lambda` pointwise at many integers and creates positive shift-two pairs with exact product zero. Its positive correlation cannot be promoted without a signed Type II remainder estimate. The next theorem is `ShiftTwoTypeIICorrelationExcess`.

## TICKET94: signed remainder and Goldbach bridge

For Twin Prime, write `Lambda=alpha Lambda_R+E_R` and expand the shift-two correlation exactly. The surrogate main term is corrected by two cross terms and one residual autocorrelation. Separate Cauchy bounds are negative for every tested truncation, so L2 proximity alone cannot supply the one-sided lower bound. The next theorem must estimate the combined signed remainder directly.

For even `N`, the Goldbach correlation `G(N)=sum Lambda(n)Lambda(N-n)` has proper-prime-power contamination at most `2 sqrt(N) floor(log2(N)) log^2(N)`. Correlation above this threshold certifies a genuine prime representation. Binary Goldbach is reduced to a uniform all-large-even correlation excess plus finite verification; neither part is claimed complete.

## TICKET95: sharp contamination and equivalence audit

Define the cumulative proper-prime-power Mangoldt mass

```text
H(y)=sum_{m<=y, m=p^k, k>=2} Lambda(m).
```

Charging a contaminated pair to its proper-power endpoint proves the sharper unconditional bounds

```text
Twin:    E_pp(x) <= log(x+2)(H(x)+H(x+2)),
Goldbach: E_pp(N) <= 2 log(N) H(N).
```

These replace the TICKET93/94 exponent-count envelopes. Every stored checkpoint passes the new bounds, and their numerical size is roughly 27 to 238 times smaller. A Goldbach FFT screen over all 499,999 even targets through one million observes a positive sharp margin for every even `N>=40`; the ten smaller nonpositive criterion cases all have direct prime witnesses. The screen is explicitly labelled non-rigorous floating-point evidence.

TICKET95 also audits the Twin signed-remainder target:

```text
D_R=C_2-alpha_R^2S_R,
D_R>=-alpha_R^2S_R+B_#+omega  iff  C_2>=B_#+omega.
```

Thus the TICKET94 target is a valid reformulation but not a weaker theorem. It remains useful only if an independent Type II estimate controls `D_R` without importing the exact correlation. The retained targets are `IndependentShiftTwoCorrelationExcess` and `UniformBinaryMinorArcDominance`. No open conjecture or counterexample is claimed.

## TICKET96: Fourier phase-information audit

Let `F(z)=sum Lambda(n)z^n` and zero-pad beyond twice the audited range. Exact inverse DFT coefficient extraction gives

```text
Goldbach: coefficient_N F(z)^2 = G(N),
Twin:     coefficient_shift2 |F(z)|^2 = C_2(x).
```

Every frequency mask therefore supplies an exact signed major/minor decomposition. Replacing the signed minor coefficient by its Parseval-energy envelope is valid but loses decisive information. At 10,000 and 100,000, 36 low-denominator mask configurations per scale are replayed; no mask with density at most ten percent certifies either TICKET95 contamination budget through energy alone.

Two abstract countermodels explain the failure. Goldbach minor magnitudes admit conjugate-symmetric phase choices that align the target coefficient negatively. Twin total minor energy admits conjugate-symmetric placement at frequencies with negative shift-two cosine. These countermodels are not prime sequences; they prove only that phase-blind premises are logically insufficient without extra arithmetic constraints.

The retained targets are

```text
ArithmeticMinorArcPhaseCancellation,
ShiftTwoSpectralLocalizationOrTypeIICancellation.
```

Dense data-dependent masks and exact sampled DFT replay are not promoted to asymptotic theorems. No open conjecture or certified prime counterexample is claimed.

## TICKET97: optimal periodic projection and residual-sign audit

For each fixed modulus `W`, project Lambda onto its exact finite-interval residue-class means. This conditional expectation is the unique L2-optimal W-periodic model, and its residual has zero mean in every residue class. Goldbach and shift-two correlations split exactly into periodic main, two cross terms, and a residual correlation.

The audit uses `W=2,6,30,210,2310` at scales 10,000 and 100,000. All projection and reconstruction contracts pass, but no separate norm-only lower bound certifies either TICKET95 sharp budget. Fixed-modulus one-point arithmetic structure remains insufficient.

The explicit signed residual

```text
[1,1,-1,-1,-1,-1,1,1]
```

has zero sums in both mod-2 residue classes while producing additive coefficient `-4` and shift-two coefficient `-2`. This proves an information no-go for residue means, not a prime counterexample.

The retained targets are `GrowingModulusBinaryResidualCancellation` and `GrowingModulusShiftTwoResidualCancellation`: the modulus must grow under independent distribution estimates, and the signed residual correlation must be controlled by Type II or higher-order uniformity.

## TICKET98: growing-modulus leakage boundary

For a finite dataset indexed by `0,...,L-1`, a fitted residue projection with `W>=L` is the identity: distinct indices have distinct residues, every occupied residue mean equals its only observation, and therefore `P_W x=x`, `E_W=0`. Any norm certificate at that point is an exact replay of the observed target correlation.

The primorial audit through `W=9,699,690` uses scales 10,000, 100,000, and 1,000,000. At each scale the first Goldbach and Twin certificate is exactly the first row-unique modulus; there are no non-row-unique certificates. Even the near-saturated case `N=1,000,000`, `W=510,510`, with at most two observations per occupied residue, certifies neither target.

The fitted-growing-modulus shortcut is retired. The retained targets are `OutOfSampleGrowingModulusBinaryResidualCancellation` and `OutOfSampleGrowingModulusShiftTwoResidualCancellation`: estimate the arithmetic projection independently of the evaluated correlation, retain a nondegenerate occupancy regime, and prove a signed residual estimate uniform in scale. This leakage theorem proves none of the four conjectures.

## TICKET99: out-of-sample and external local model

The period-parity cross-fit uses disjoint Lambda samples for training and evaluation and rejects empty evaluation sets. Across 120 preregistered configurations, separate norm lower bounds certify neither Goldbach nor Twin Prime.

The external coprime model `A_W(n)=W/phi(W) 1_(n,W)=1` removes fitted-data dependence entirely. CRT gives the exact common lower density

```text
d_W = 2 product_{3<=p|W}(1-1/(p-1)^2),
M_G(N), M_2(x) >= d_W max(0,scale+1-W).
```

Thus the main term is linear and target-independent. The only unresolved object is the signed residual. For the largest primorial `W(n)` with `W(n)^2<=n`, the finite candidate

```text
R_W(n) >= -1.6 M_W(n)/log(n)
```

has zero post-calibration failures through one million on both tracks. If proved uniformly and independently, it combines with the `o(n)` prime-power contamination budgets to imply Goldbach after finite verification and Twin Prime infinitude. The screen is double-precision candidate discovery, not proof. Generic W-trick transference and one-point progression control do not resolve these affine-degenerate binary residuals.

## TICKET100: extended residual and joint Vaughan cancellation

The `K=1.6` candidate has zero finite failures through every even Goldbach target at 6M and every cumulative Twin target at 10M, including the first `210 -> 2310` primorial transition. This remains finite evidence.

With `Lambda=I_(U,V)+II_(U,V)`, substitute one factor only:

```text
C-M = (<I,Lambda_shift>-M) + <II,Lambda_shift>.
```

At Goldbach `N=930,930`, the Type II component alone has required constant `K=7.9099`, whereas the joint residual's worst constant remains below `1.6`. This is a concrete counterexample to separate componentwise K/log lower bounds. The structured term and Type II term must be estimated jointly with their signs intact.

The contrapositive program is now exact: a large Goldbach counterexample or finite Twin set forces the residual-to-main ratio toward `-1`, contradicting any independently proved joint `-K/log n` lower envelope. The remaining targets are `JointVaughanGoldbachResidualEnvelope` and `JointVaughanShiftTwoResidualEnvelope`.

## TICKET101: balanced cutoff frontier and energy-equivalence audit

The TICKET100 `U=V=100` obstruction is not promoted without a parameter audit. At scale one million, TICKET101 evaluates 39 Vaughan cutoff pairs, including 28 balanced pairs satisfying `U,V<=N^(1/3)=100`.

Goldbach has no separated-budget survivor in that balanced range. The best tested row remains `U=V=100`, with structured constant `1.5791`, Type II constant `7.9099`, and total `9.4890`. A numerical pass first appears at `U=V=960`, but only 314 Type II coordinates remain. At `U=V=1000`, Type II is zero and the structured term equals Lambda. This is decomposition collapse, so the retained Goldbach target is `JointBalancedVaughanGoldbachResidualEnvelope`.

Twin Prime has four balanced survivors. The best tested pair `U=100,V=84` has a nonzero Type II support of 244,204 coordinates and constants

```text
structured K = 1.3889576,
Type II K    = 0.1710919,
sum          = 1.5600495 < 1.6.
```

This corrects the broad joint-only continuation. The next Twin target is `SeparatedBalancedVaughanTwinBudgets`, with rounded discovery budgets `1.40` and `0.18`. Both all-scale inequalities remain unproved.

Finally, the Goldbach reflection identity and Twin shift-mismatch identity rewrite correlation as an energy deficit. The rewrite is exact, but the desired energy inequality is algebraically equivalent to the original correlation lower bound. It is not a reduction unless an independent mismatch theorem contributes new information. TICKET101 proves neither a conjecture nor a conjecture counterexample.

## TICKET102: Twin dyadic holdout and finite-constant correction

Use the data-independent scale-local rule `U(X)=round(X^(1/3))`, `V(X)=round(0.84U(X))` and inspect every `x` in `(X/2,X]`. The registered structured budget `K_S=1.40` is refuted at `X=2M`: all one million post-selection points fail, with maximum required constant `1.9532`. The Type II `K_II=0.18` budget has no failures. This is a proof-strategy counterexample, not a Twin Prime counterexample.

The former `1.6` gate was unnecessarily strong. For any fixed finite `K_S,K_II`, the two component bounds imply

```text
C_2(x) >= M(x)(1-(K_S+K_II)/log(x)).
```

The external local main has a positive linear lower bound up to lower-order modulus loss, and proper-prime-power contamination is `o(x)`. Thus any horizon-uniform finite constants are sufficient; no optimization against `1.6` is needed.

After the failure is observed through 4M, register `K_S=4,K_II=1` before opening the 8M block. All four million fresh points pass. The maximum required structured constant is `3.3068`, Type II is nonnegative throughout the block, and Type II support is `24.31%`. Support is only a noncollapse guard, not an analytic Type II estimate.

The retained target is `UniformFiniteDyadicSeparatedVaughanTwinBudgets`. RH returns to non-circular kernel positivity, Collatz to `GoldenMeanInvariantSetEscape`, and Goldbach to joint balanced signed cancellation. TICKET102 proves none of the four conjectures.

## TICKET103: exact Twin local-block audit

TICKET102's endpoint audit uses cumulative component correlations from zero. TICKET103 fixes one external model and one Vaughan split per dyadic horizon, then evaluates the exact identity only on `(X/2,X]`. This removes the possibility that earlier positive Type II mass hides a negative current block.

The seven principal blocks from 125K through 8M have positive Type II sums. Their maximum structured required constant is `3.7617`, maximum Type II required constant is `0`, and maximum joint required constant is `0.6430`. All reconstruction and support contracts pass.

Universal positivity is nevertheless false. At `X=1000`, the local Type II correlation on `(500,1000]` equals `-174.7165`, requiring `K_II=1.7515`. This exact finite counterexample retires Type II nonnegativity as an identity or all-scale lemma. It does not refute eventual finite bounds and is not a Twin Prime counterexample.

The retained target is `UniformDyadicLocalVaughanTwinBlockBudgets`: prove some fixed finite local structured and Type II constants on every sufficiently large dyadic block. Such bounds, combined with the linear local main and `o(X)` contamination, are sufficient for twin-prime infinitude. TICKET103 proves none of the four conjectures.

## TICKET104: exact Type II weighted-Möbius anatomy

Expanding the local Vaughan Type II kernel gives the exact finite identity

```text
T_X = sum_{d>U} mu(d) A_X(d),
A_X(d) >= 0.
```

The weights contain `Lambda(r)Lambda(drm+2)` on the current dyadic block. Thus the open estimate is weighted Möbius cancellation against shifted-prime mass, not an unweighted Mertens bound.

The identity and Abel summation replay to numerical errors below `1e-9`. At 125K, 1M, and 2M the actual Type II term is positive. Independent negative-term bounds require constants `21.75,34.79,39.92`; Abel summation followed by triangle inequality requires `354.06,799.04,1088.15`. At `X=1000`, actual required `K=1.7515` while the Abel-triangle envelope requires `61.83`.

This does not prove those envelopes diverge. It refutes presenting their finite information-losing forms as the desired cancellation estimate. The retained theorem is `WeightedMobiusShiftedPrimeDyadicCancellation`, preserving the relation between Möbius signs and weight differences before taking absolute values. TICKET104 proves none of the four conjectures.

## TICKET105: coprime progression centering

For each `q=dr`, replace the shifted prime value by its independent progression mean `q/phi(q)` when `q` is odd and zero when `q` is even. This produces an exact baseline-plus-centered decomposition of the TICKET104 weighted Möbius sum.

The identity replays below `1.7e-10` through 2M. At 125K, 1M, and 2M, negative centered-mass bounds require `K=4.50,5.15,5.41`, compared with the uncentered `21.75,34.79,39.92`. Full-vector Cauchy-Schwarz remains much weaker at `26.69,37.12,41.15`.

The remaining term couples `mu(d)` to arithmetic-progression errors `Lambda(drm+2)-dr/phi(dr)`. This is the precise object for dispersion or bilinear large-sieve analysis. The retained target is `MobiusWeightedPrimeProgressionDiscrepancyBound`. Finite improvement after centering is not a proof of a uniform bound, and TICKET105 proves none of the four conjectures.

## TICKET106: modulus grouping and sparse-progression leakage

Combine every repeated factorization `q=dr` before taking norms. The exact centered sum becomes `sum_q c_X(q)Delta_X(q)` and replays below `4.3e-10`. At 2M, however, grouped Cauchy needs `K=249.12` versus outer-`d` `41.15`, and grouped negative mass needs `55.29` versus `5.41`.

Occupancy explains the failure. Moduli with at most one block sample form `72.31%` of support and supply `64,933.8` of centered total `67,608.8`. Their progression cells identify individual rows, analogous to TICKET98's row-unique fitted-modulus leakage. Positive sparse-tail mass is not a dense distribution theorem.

The retained target is `NonSparseModulusTwinDispersionWithSparseTailControl`: separate a nondegenerate-occupancy dispersion estimate from an independently controlled sparse tail. TICKET106 proves none of the four conjectures.

## TICKET-107: sparse-tail Vaughan recombination

TICKET107 maps every occupancy-one modulus `q` back to its unique integer `n=qm`, combines repeated n values, and compares the resulting q-built Type II vector with an independently constructed Vaughan decomposition. All q-to-n, Vaughan-vector, and correlation identities pass through 8M.

At 8M, 1,589,098 sparse q cells compress to 1,099,268 n cells; 247,461 n cells receive two sparse-q representations, and n-grouping retains only `69.53%` of q-level L1 mass. The structured residual is `-1,281,289.5`, sparse Type II is `+399,460.6`, dense Type II is `+756,121.9`, and the full residual is `-125,707.0`. The structured-plus-sparse required constant is `2.59`, versus `0.37` for the full joint residual.

This refutes fixed-sign sparse-tail and independent one-sided component-budget shortcuts on the audited data. The retained theorem is `JointStructuredSparseDenseTwinDispersion`, which must preserve all three signed components through the final uniform estimate. TICKET107 proves none of the four conjectures.

## TICKET-108: joint equivalence no-go and smoothed excess bridge

TICKET108 recombines `Lambda=I+II_sparse+II_dense` symbolically and numerically. The proposed joint hard-cutoff lower bound is exactly the original correlation residual lower bound; the maximum audited equality error through 8M is below `4.2e-9`. `JointStructuredSparseDenseTwinDispersion` is therefore discarded as a no-reduction restatement.

The replacement fixes the nonnegative bump `W(t)=16(t-1/2)(1-t)` on `[1/2,1]`. Since `0<=W<=1`, the weighted proper-prime-power contamination is at most the explicit TICKET93 bound `B(X)`. Thus `limsup(S_W(X)-B(X))=+infinity` implies infinitely many twin primes by contrapositive.

The bump improves only 2/6 finite blocks and worsens all four from 1M through 8M, so it is retained for Fourier/Mellin transform structure rather than numerical dominance. The next target is `SmoothedShiftTwoTypeIICorrelationExcess`. TICKET108 proves none of the four conjectures.

## TICKET-109: spectral phase audit

TICKET109 proves the exact finite identity `sum f(n)f(n+2)=N^(-1)sum |F(k)|^2 cos(4 pi k/N)` for the symmetric fixed bump, with maximum error below `2.4e-10` through `X=1,048,576`. The identity is equivalent to the correlation and is not counted as a lower-bound theorem.

Every tested one-band origin-centered low-frequency lower bound is negative. At the largest horizon the positive phase contribution is `1.829M`, the negative contribution is `-1.370M`, the exact correlation is `0.459M`, and the best tested sufficient lower bound is `-3.338M`.

The discarded route is single-origin frequency concentration with worst-case outside phase. The retained target is `RamanujanMajorArcPhaseMarginWithMinorArcControl`, combining rational major arcs and an independently controlled Type II minor-arc remainder. TICKET109 proves none of the four conjectures.

## TICKET-110: rational major-arc budget

TICKET110 fixes all reduced rational centers `a/q`, `q<=Q`, and widths `Q/(qX)` before reading target contributions, then partitions the discrete spectrum exactly. At `X=1,048,576`, `Q=32` produces major contribution `461,203.6`, actual minor contribution `-2,063.7`, and exact correlation `459,139.9`.

The trivial minor-energy lower bound is `-3,105,699.1`, yielding total lower bound `-2,644,495.5`. Thus rational masking captures the observed arithmetic signal but cannot replace a signed Type II minor-arc estimate.

The retained target is `FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving`. TICKET110 proves none of the four conjectures.

## TICKET-111: Vaughan Type II minor cross-spectrum

TICKET111 connects the fixed `Q=32` rational arc mask to the exact Vaughan decomposition. For the symmetric bump sequence, the shift-two correlation and its fixed minor part split exactly into Type I and Type II cross-spectra against the shifted full von Mangoldt target. Component reconstruction errors remain below the registered tolerance through the fresh 2M holdout.

Consider every proof template that partitions the fixed minor bins, applies Cauchy-Schwarz independently on each cell, and discards complex phase. Its envelope is bounded below by the singleton-bin expression

```text
E_bin(X)=sum_minor m_k |TypeII_hat(k)||Lambda_hat(k)|/N.
```

This smallest phase-blind envelope fails on all five audited horizons. At 2M, known major plus Type-I minor is `929,258.9`, `E_bin=7,596,484.2`, and the resulting lower bound is `-6,667,225.4`. This is a finite no-go for the stated argument class, not for Type II analysis itself.

The candidate `TypeII_minor >= -X^(-1/6)E_bin` was frozen after the rows at or below 1M. It survives the first post-selection 2M holdout: actual Type-II minor `+14,783.4`, candidate envelope `671,440.7`, and finite lower expression `257,818.2`. Finite survival does not prove uniformity.

The retained target is `PhaseAwareVaughanTypeIIMinorArcPowerSaving`. It must preserve bilinear phase and be proved independently of the observed target correlation. TICKET111 proves none of the four conjectures.

## TICKET-112: Farey-cell endpoint Abel audit

TICKET112 applies exact discrete Abel summation inside all 162 connected cells of the fixed `Q=32` minor mask. The Type II minor contribution becomes the sum of cell endpoint terms plus smooth within-cell phase-variation terms. The identity replays below tolerance through 2M.

At 2M, the Farey-Abel envelope is `1,280,365.2`, only 16.85% of TICKET111's phase-blind singleton envelope `7,596,484.2`. This substantial improvement is still insufficient: the known major-plus-Type-I-minor contribution is `929,258.9`, leaving lower bound `-351,106.4`.

The remaining loss is concentrated at cell endpoints. Endpoint absolute mass is `1,229,823.0`, or 96.05% of the Abel envelope; within-cell variation is `50,542.3`. Actual signed endpoint contribution is `+11,146.8`. Independent endpoint triangles are therefore discarded.

Applying the already-frozen `X^(-1/6)` factor only to endpoint mass leaves finite lower expression `770,014.6` at the 2M holdout. This is not an all-scale estimate.

The retained target is `UniformFareyCellEndpointCancellationForVaughanCrossSpectrum`. TICKET112 proves none of the four conjectures.

## TICKET-113: right-Farey-denominator endpoint audit

TICKET113 freezes one structural rule after the exploratory `X=262,144` row: assign every TICKET112 Abel endpoint to the denominator of its immediate right Farey boundary. All `q=2,...,32` are retained, giving 31 complex blocks from 162 cells. No sign, subset, weight, or exponent is fitted.

The exact identity is `sum_C E_C=sum_q D_q`, where `D_q` is the sum of endpoints whose right boundary has denominator `q`. Taking absolute values only after forming each `D_q` retains within-denominator phase cancellation. The unchanged Abel variation envelope is then added.

At the new 4M holdout, endpoint absolute mass is `2,161,424.6`, the 31-block endpoint envelope is `767,682.2`, variation costs `89,185.2`, and known major-plus-Type-I-minor is `1,874,243.5`. The resulting finite lower expression is `1,017,376.2`. Both the Abel identity and denominator grouping identity replay within `3.2e-9`.

This finite success does not establish uniformity. A countermodel replaces each endpoint by `-|E_C|` while preserving cell labels, group counts, magnitudes, and magnitude-only norms. It gives lower expression `-376,366.3` at 4M and fails closure on all six scales. Thus Farey labels and magnitudes alone are insufficient; any proof must use phase relations imposed by the actual Vaughan bilinear coefficients. The countermodel is not claimed to be Vaughan-realizable.

The retained target is `UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum`. TICKET113 proves none of the four conjectures.

## TICKET-114: Ramanujan mean and centered-numerator dispersion

TICKET114 opens each TICKET113 right-denominator block by reduced numerator. If `P_{q,a}` is the unphased Abel endpoint coefficient for the cell immediately left of `a/q`, the endpoint phase is transferred to the exact rational phase `rho_{q,a}=exp(4 pi i a/q)`. The signed transfer error is retained exactly and bounded by `4 pi |P_{q,a}| |alpha-a/q|`.

Writing `Re(P_{q,a})=m_q+x_{q,a}` with `sum_a x_{q,a}=0` gives an exact rational-boundary decomposition. The mean contribution is `m_q c_q(2)/2` for `q>2` and `m_2 c_2(2)` for `q=2`. The remainder is the inner product of `(x_{q,a}, Im P_{q,a})` with `(cos(4 pi a/q)-mean(cos), -sin(4 pi a/q))`.

Cauchy-Schwarz gives the projected L2 support envelope. This bound is sharp under the stated weak contract: choosing the coefficient vector opposite to the projected phase vector attains the negative support value. This proves that no generic rearrangement or repeated Cauchy argument can improve the bound without adding arithmetic constraints. The abstract extremizer is not asserted to be Vaughan-realizable.

Across `X=4K,32K,262K,1M,2M,4M`, the signed-mean lower expression is positive on four scales and the stronger sign-free expression is positive only on the last three. At 4M the sign-free adverse budget is `82.50%` of the known major-plus-Type-I-minor term and leaves finite lower expression `327,951.0`. Small-scale failures are retained, so the terminal run is theorem-selection evidence rather than a uniform estimate.

The retained target is `EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget`. It must derive, from actual Möbius/divisor bilinear coefficients, a fixed-margin all-sufficiently-large-scale bound for the mean, centered, boundary-transfer, and variation envelopes. A valid negative result would be a Vaughan-realizable coefficient family violating that margin. TICKET114 proves none of the four conjectures.

## TICKET-115: complex cyclotomic mean and orientation no-go

TICKET115 writes every numerator endpoint block as `P_{q,a}=M_q+Z_{q,a}` with complex zero-sum `Z`, and retains the exact half-Farey phase sum `H_q=sum_a exp(4 pi i a/q)`. This gives the exact identity `Re sum P rho=Re(M_qH_q)+Re sum Z(rho-mean rho)` and the exact geometry `||rho-mean rho||_2^2=n_q-|H_q|^2/n_q`.

The complex-centered remainder has a sharp L2 support bound. Under only complex zero mean and a fixed norm, the negative conjugate projected phase attains equality. Any stronger theorem must therefore use actual Vaughan arithmetic.

The finite audit separates two contracts. Paying `sum_q |Re(M_qH_q)|` improves the TICKET114 numerator budget on all six scales and gives 4M lower expression `335,523.7`. Paying the orientation-free `sum_q |M_q||H_q|` worsens all six scales and gives only `248,127.1` at 4M; it also loses the 1M finite closure. Thus orientation-free complex centering is discarded.

The retained target is `EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget`. It must prove a fixed-margin all-sufficiently-large-`X` estimate for the scalar cyclotomic mean, complex-centered projected norm, boundary transfer, and Abel variation, and must establish the positive comparison scale independently. TICKET115 proves none of the four conjectures.

## TICKET-116: Möbius-sign lift and polarization no-go

TICKET116 expands the actual Vaughan Type-II sequence into nonnegative outer-divisor layers `II=II_plus-II_minus`, separated by `mu(d)=+1` and `mu(d)=-1`. Linearity carries this identity through the DFT, fixed minor-cell prefix sums, and half-Farey endpoint map. Complex centering therefore gives `M=M_plus-M_minus` and `Z=Z_plus-Z_minus` for all 31 denominator blocks.

The exact centered polarization identity is `||Z||^2=||Z_plus||^2+||Z_minus||^2-2 Re<Z_plus,Z_minus>`. The covariance is negative on the first two audited rows and positive on the next four, so a favorable sign is not assumed. Bounding the two sign layers independently is deterministically weaker by triangle inequality and empirically worsens all six rows. At 4M, the numerator budget grows from `1,449,516.0` to `4,187,038.4`, and the finite lower expression changes from `335,523.7` to `-2,401,998.7`.

Independent Möbius-sign triangles are therefore discarded. The retained target is `EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget`: derive the endpoint estimate from the signed outer-Möbius bilinear sum before norms, or prove a denominator-summed covariance lower bound strong enough to preserve a fixed all-sufficiently-large-scale margin. An unbounded sequence of actual Vaughan layers violating every such margin would refute this target. TICKET116 proves none of the four conjectures.
