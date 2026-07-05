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
