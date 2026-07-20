# PrimeProject Four-Problem Research Consolidation

Date: 2026-07-10

Canonical status: `open_not_proven` for all four problems

Scope: Riemann Hypothesis, Collatz conjecture, binary Goldbach conjecture, Twin Prime conjecture

> **Current continuation / 최신 연속 연구:** this dated consolidation remains a
> historical keep/discard baseline. The current boundary is
> [TICKET-134](uniformity-thresholds-and-scale-no-go.md), which gives a rational
> interval semi-decision for strict finite RH Gram signs, proves that no bounded-
> depth Collatz contracting cover can be complete, identifies the logarithmic
> Goldbach moment threshold for sparse spikes, and extends Twin composite lifts
> to growing primorial levels with an exact `2Wqr` range bound. All four problems
> remain `open_not_proven`.

## 한국어 정리

### 1. 결론부터

PrimeProject는 네 난제 중 어느 것도 증명하거나 반증하지 못했다. 현재까지 얻은 가장 강한 성과는 다음 세 가지다.

1. 유한 계산, 통계적 일치, 투영 그래프, 형식 파일의 문자열을 전역 증명과 구분하는 claim gate를 만들었다.
2. 여러 자연스러운 증명 지름길이 왜 실패하는지 재생 가능한 반례 또는 유한 obstruction으로 기록했다.
3. Collatz에 대해서는 추상적인 방법론 전이를 넘어 exact congruence lift를 실제로 계산하여, 현재 좌표 기반 귀납의 병목을 정량화했다.

#### 2026-07-11 TICKET77-79 교정 및 진전

- TICKET77의 홀수 boundary 값은 소멸이 아니라 equality rollback임을 교정했다. 고정 접두사의 무한 완성은 양의 정수가 아니라 `T^m(N)=-1/3`을 만족하는 2진 점이다.
- TICKET78은 모든 유한 accelerated valuation word가 양의 정수를 무한히 포함하는 정확한 residue cylinder를 정의함을 증명했다. 따라서 유한 2진 정보만으로 자연수와 2진 ghost를 분리하는 경로를 폐기했다.
- TICKET79는 `alpha*log(n)+bounded 2-adic correction` 형태의 보편적 일단계 순위를 정확한 자연수 팽창·수축 가족으로 배제했다. 양의 계수는 임의로 긴 valuation-1 구간, 음의 계수는 `D_r->5`, 0 계수의 유한 상태형은 비둘기집 원리로 실패한다.
- TICKET80은 최소 반례의 유한 접두 비감소 조건이 모든 깊이와 모든 유한 하한에서 양의 정수 해를 가지며, 그 2진 compactness 극한은 `-1`일 수 있음을 증명했다. 따라서 유한 절단과 compactness만으로는 모순 또는 양의 반례를 얻을 수 없다.
- 이 결과들은 콜라츠 추측의 증명이나 반례가 아니다. 다음 실질 목표는 하나의 고정된 자연수 cylinder 경로에 대해 horizon 독립 높이 상한을 도출하는 것이다.

이 문서 이후의 연구 진척은 티켓 수가 아니라 아래 두 조건으로 평가한다.

- 기존 obstruction을 제거한 새 lemma가 만들어졌는가?
- 그 lemma가 유한 horizon에 의존하지 않는 명시적 quantifier와 검증 가능한 proof object를 갖는가?

### 2. 증명과 반례의 승인 기준

| 주장 | 승인에 필요한 최소 조건 | 승인되지 않는 것 |
|---|---|---|
| 전역 증명 | 모든 입력 또는 모든 높이를 덮는 명시적 정리, 비순환 의존성, 독립 재생 가능한 논증 | 큰 유한 범위, 통계적 일치, 그래프가 예뻐 보이는 것 |
| 전역 반례 | 정확한 수학적 객체, 대상 명제의 부정을 직접 만족함, 서로 독립적인 두 검증 경로 | surrogate, coarse pressure path, 수치 오차 안의 후보 |
| 유한 정리 | 범위와 술어가 정확히 고정되고 certificate가 재생됨 | 유한 결과를 무한 명제의 증거로 승격 |
| 방법 반박 | 제안된 lemma의 가정을 만족하면서 결론을 깨는 replayable witness | 원래 난제의 반례라고 부르는 것 |

Collatz의 열린 pressure path는 divergence나 비자명 cycle이 증명되기 전에는 Collatz 반례가 아니다. RH의 surrogate zero packet은 실제 zeta zero가 아니다. Goldbach의 낮은 margin packet은 표현 불가능한 짝수가 아니다. Twin Prime의 deletion model은 소수열 자체가 아니다.

### 3. 산출물 신뢰 등급

| 등급 | 의미 | 현재 취급 |
|---|---|---|
| A | exact bounded certificate 또는 exact counterexample to a proposed lemma | 유지, 재생 테스트 대상 |
| B | 문제 고유 CEGIS로 확인한 유한 obstruction | 유지, 다음 lemma 설계에 사용 |
| C | 다른 문제에서 가져온 proof discipline 또는 theorem template | 참고용, 해당 문제의 진척 수치에서 제외 |
| D | 시각화, heuristic fit, metadata-only formal skeleton | 탐색 보조, 증명 근거에서 제외 |

`formal/*/InfiniteBridge.lean` 파일은 현재 theorem을 증명하는 Lean 코드가 아니라 요구 조건을 기록한 skeleton이다. 그 안의 문자열은 kernel-checked theorem이 아니므로 증명 진척으로 계산하지 않는다.

### 4. 지금까지의 티켓을 압축한 연구 계보

#### TICKET15-18: 목표와 반례 모드 확립

- 각 문제의 첫 candidate theorem과 proof/counterexample gate를 정의했다.
- finite evidence와 full proof 사이의 quantifier gap을 명시했다.
- RH finite-prefix camouflage, Goldbach explicit-error gap, Twin Prime bounded-gap deletion model, Collatz residue-rank 후보를 분리했다.

#### TICKET19-26: 자연스러운 지름길 반박

- RH: 고정된 Li/Jensen prefix가 높은 off-critical surrogate를 놓칠 수 있음을 확인했다.
- Collatz: 단순 valuation rank, basin lexicographic rank, predecessor closure, 평균 drift를 전역 descent로 승격할 수 없음을 확인했다.
- Goldbach: local congruence cover가 analytic positivity를 대신하지 못함을 확인했다.
- Twin Prime: admissibility와 bounded gaps가 exact gap 2를 강제하지 않음을 deletion countermodel로 분리했다.
- TICKET26의 micro-lemma들은 proof-strategy 비보편성에 관한 제한된 정리이며 원래 난제의 정리가 아니다.

#### TICKET27-45: rank, compactness, potential의 한계

- 관측 그래프에서 rank를 만들고 frontier를 확장하는 공통 CEGIS 틀을 구축했다.
- finite DAG rank, null-set argument, density argument, pointwise feature rank가 universal theorem을 대신하지 못함을 반복적으로 확인했다.
- Collatz 이외 세 문제의 이 구간 상당수는 problem-specific 계산이 아니라 공통 proof discipline의 전이다.

#### TICKET46-56: lasso와 terminal-family 닫기

- Collatz의 특정 phase/lasso family를 exact finite partition으로 추적했다.
- 일부 near-lasso와 gate-crosser family는 유한하게 닫혔다.
- 이 결과는 선택된 family를 제거할 뿐, 모든 Collatz trajectory를 덮지 않는다.
- 다른 세 문제의 대응 티켓은 “유한 family 소거를 전역 theorem으로 승격하지 말라”는 방법론 전이다.

#### TICKET57-65: boundary와 lift 안정성

- Collatz에서 low-bit boundary, failure offset, mod-16 extension 좌표를 단계적으로 시험했다.
- 한 horizon에서 결정적인 좌표가 다음 lift에서 깨지는 구체적 mismatch를 찾았다.
- 선택된 start-template chain은 80비트에서 소거됐지만 complement 대부분은 열린 `needs_split` 상태였다.

#### TICKET66-76: complement, frontier, coverage, coordinate closure

- TICKET66은 complement를 열어 제한된 성공 branch 밖의 미분류 질량을 측정했다.
- TICKET67-69는 관측 cyclic SCC를 `prefix_length, consumed_bits`로 분해해 bounded DAG rank를 만들었다.
- TICKET70은 rank-0 frontier를 확장하여 direct rank closure를 반박했다.
- TICKET71-72는 compact coordinate의 collision과 higher-lift mixed pressure를 측정했다.
- TICKET73은 상위 8개 mixed key에서 시작한 strict re-entry tree가 fifth lift에서 비는 것을 정확히 확인했다.
- TICKET74는 그 root family가 전체 mixed key의 0.0386%만 덮으며, strict extinction 뒤에도 pressure가 기존 cover 밖으로 누출됨을 확인했다.
- TICKET75는 고정 유한 좌표 8개를 시험하여 압축과 상태 폭발 사이의 trade-off를 정량화했다.
- TICKET76은 이 trade-off의 원인을 exact boundary quotient recurrence로 환원하고, 고정 low-bit 정밀도가 unresolved lift에서 닫히지 않는 reachable collision을 찾았다.

### 5. 문제별 최종 감사

#### 5.1 리만가설

유지할 결과:

- 어떤 고정 finite prefix도 별도 tail theorem 없이 RH를 판정할 수 없다는 surrogate-based falsification discipline.
- kernel positivity, Li curvature, Jensen polynomial 등 candidate가 finite test를 통과해도 all-height zero theorem이 되지 않는다는 claim boundary.
- 유한 Jensen hyperbolicity 계산은 구현 검증과 coefficient 탐색 자료로만 유지한다.

폐기하거나 강등할 경로:

- finite Li/Jensen/Hermite positivity에서 모든 zeta zero의 critical-line 위치를 추론하는 경로.
- 실제 zeta zero와 연결되지 않은 surrogate detector를 RH 반례 또는 증명으로 부르는 경로.
- `RH-CEGIS-14`를 infinite bridge 자체로 취급하는 경로.

현재 가장 강한 미해결 정리:

```text
모든 off-critical zeta zero가 존재한다면, 높이와 실수부 편차에 대해 효과적으로 계산 가능한 지수 안에서
부호 위반 또는 positivity 위반을 반드시 만드는 all-height detector theorem.
```

반례 트랙:

- interval arithmetic과 argument principle로 `Re(s) != 1/2`, `0 < Re(s) < 1`인 실제 zeta zero 하나를 인증해야 한다.
- 현재 저장소에는 그런 객체가 없다.

판정: 문제 고유 barrier는 잘 식별했지만, 새로운 analytic inequality는 아직 없다.

#### 5.2 콜라츠 추측

유지할 결과:

- accelerated Collatz residue certificate와 exact `2^k` congruence extension.
- 단순 rank, 평균 drift, bounded SCC, selected lasso family의 실패 또는 유한 소거 certificate.
- TICKET74의 coverage leakage와 TICKET75의 coordinate trade-off.

TICKET75 exact 결과:

- fifth open-pressure rows: `15,696`
- sixth open-pressure rows: `78,315`
- exact extension failures: `0`
- 가장 거친 finite coordinate: 새 sixth row `11 / 78,315`이지만 cyclic nodes `66`, mixed outcome keys `59`
- 가장 세밀한 finite coordinate: mixed outcome keys `4`까지 감소하지만 새 sixth rows `77,998 / 78,315`
- 두 단계 closure gate를 통과한 coordinate: `0 / 8`
- 기존 `base_prefix_consumed` rank는 exact lengths를 포함하므로 fixed finite-state rank가 아니다.

TICKET76 exact 결과:

- lift-stable prefix에 대해 `T^m(r+h2^b)=T^m(r)+h3^m2^(b-s)`를 사용한다.
- `d=b-s`, `A=(3T^m(r)+1)/2^d`, `u=3^(m+1)`라 두면 첫 새 valuation은 `d+v2(A+hu)`다.
- `v2(A+hu)>4`인 unresolved child는 `A_next=(A+hu)/16`을 만족한다.
- fifth/sixth layer transition `297,104`개에서 prefix replay, affine identity, valuation formula, recurrence failure는 모두 `0`이다.
- fixed precision `q=5,9,13,17,21`의 collision key 수는 각각 `165, 1,536, 1,235, 106, 15`다.
- 각 q에서 `q+4` lookahead collision은 모두 `0`이다.

따라서 단순히 boundary quotient의 low bit를 고정 개수 추가하는 방식은 재귀 closure가 아니다. unresolved lift의 `/16` 정규화가 다음 네 상위 비트를 노출한다. 다만 실제 reachable quotient에 별도의 산술 제약이 존재할 가능성, full 2-adic state에 well-founded rank를 결합할 가능성은 아직 열려 있다.

TICKET77 exact 결과:

- canonical four-bit digit `h(A)`를 `A+h(A)3^(m+1) = 0 mod 16`으로 정하고 `P(A)=(A+h(A)3^(m+1))/16`으로 둔다.
- reachability identity `2^d A=3T^m(r)+1`에서 `3`은 `A`를 나누지 않는다.
- `A>3^(m+1)`이면 `0<P(A)<A`이므로 정규화된 경계 궤도는 결국 `1<=A<3^(m+1)`에 들어간다.
- 이 유한 구간에서 `P(A)`는 `16^(-1)A mod 3^(m+1)`의 최소 양의 대표다.
- LTE로 `ord_(3^(m+1))(16)=3^m`이며, 궤도는 같은 nonzero `mod 3` 잉여류 전체를 순회한다.
- `m>=1`이면 궤도에 짝수와 홀수가 모두 있다. 홀수 `P(A)`는 strict-beyond-boundary pressure 구간을 끝내지만 equality valuation은 rollback되므로 stable prefix 자체는 끝나지 않는다.
- 첫 초안의 “홀수 `P(A)`이면 stable-prefix extinction” 주장은 이 equality rollback을 빠뜨렸으므로 철회했다.
- all-depth compatible cylinder의 2-adic 극한 `N`은 `T^m(N)=-1/3`을 만족하며 양의 정수가 아니다.
- 실제 fifth/sixth 경계 소스 `18,569`개는 모두 최대 `15` strict-pressure 단계 안에 equality 경계를 만났고, 전제·항등식·예상 밖 strict cycle·guard failure는 모두 `0`이다.

이 결과는 동일 안정 접두사의 all-depth path가 존재하더라도 양의 정수 반례가 아니라 `-1/3`의 2-adic preimage임을 분류한다. 그러나 양의 정수가 서로 다른 유한 ghost prefix들을 무한히 근사하는 changing-prefix 경로는 배제하지 않는다.

TICKET78 exact 결과:

- positive valuation word `a=(a_1,...,a_m)`와 `S=sum a_i`에 대해 `T^m(n)=(3^m n+C_m)/2^S`다.
- terminal iterate가 odd라는 조건은 하나의 유일한 잉여류 `r_a=3^(-m)(2^S-C_m) mod 2^(S+1)`를 준다.
- cylinder `r_a+q2^(S+1)`에는 양의 정수가 무한히 많다.
- 따라서 모든 finite residue prefix, finite valuation/parity word, continuous finite-state 2-adic classifier는 ghost의 비자연성을 인증할 수 없다.
- `S<=16`의 valuation word `65,535`개와 양의 정수 대표 `262,140`개를 전수 감사했고 collision, formula, replay failure는 모두 `0`이다.
- 이 결과는 Bernstein–Lagarias 2-adic conjugacy를 새로 발견했다는 주장이 아니라, TICKET77 경계 상태에 기존 이론을 정확히 연결한 no-go guard다.

따라서 purely finite 2-adic `ChangingPrefixNaturalAdmissibilityRank`는 폐기한다. 남는 후보는 실제 정수의 Archimedean height와 증가하는 2-adic precision을 함께 사용하는 비국소 rank다.

폐기하거나 강등할 경로:

- TICKET73의 selected strict-tree extinction을 global Collatz closure로 승격.
- bounded DAG rank를 horizon-independent induction으로 승격.
- density-one 또는 높은 stopping-time convergence를 universal convergence로 승격.

현재 가장 강한 미해결 정리:

```text
ArchimedeanTwoAdicCoupledDescent:
모든 positive-integer accelerated trajectory는 known basin으로 들어가거나,
Archimedean height와 growing 2-adic precision을 함께 쓰는 well-founded rank를 엄격히 감소시킨다.
```

대안 반례 트랙:

```text
고정 접두사 경로가 아니라 접두사가 무한히 바뀌는 exact compatible path를 인증하고,
그 경로가 하나의 양의 정수 궤도이며 divergence 또는 비자명 cycle을 만든다는 별도 정리를 증명한다.
```

판정: 네 문제 중 계산 가능한 lemma falsification과 exact sublemma가 가장 진전됐다. fixed-prefix ghost는 분류됐고 finite 2-adic natural separator는 전역적으로 폐기됐지만, Archimedean-coupled changing-prefix rank는 아직 없다.

#### 5.3 이항 골드바흐 추측

유지할 결과:

- 테스트한 local residue system에는 단순 modular obstruction이 없다는 bounded result.
- finite representation certificate와 singular-series error diagnostics.
- `main term - major arc error - minor arc error - exceptional contribution` ledger가 필요하다는 reduction.

폐기하거나 강등할 경로:

- singular-series empirical fit을 positivity theorem으로 승격.
- 평균 또는 almost-all result로 모든 짝수를 덮는 경로.
- ineffective Siegel-zero dependence를 숨긴 explicit cutoff.
- TICKET27 이후의 generic frontier transfer를 Goldbach 고유 계산 진척으로 세는 것.

현재 가장 강한 미해결 정리:

```text
명시적이고 출처가 추적되는 상수들로 모든 N >= N0에 대해 R(N) > 0을 보이며,
N0가 저장소의 exact finite verification 상한과 겹치는 large-even lower-bound theorem.
```

반례 트랙:

- 정확한 primality certificate와 exhaustive decomposition check로 표현 불가능한 짝수 하나를 인증해야 한다.
- 현재 저장소에는 그런 객체가 없다.

판정: 올바른 analytic budget 형태는 정리됐지만 새 minor-arc 또는 exceptional-zero bound는 아직 없다.

#### 5.4 쌍둥이 소수 추측

유지할 결과:

- bounded gaps와 exact gap 2가 논리적으로 다르다는 deletion countermodel.
- exact-gap projection candidate가 wider-gap leakage와 parity model을 반드시 통과해야 한다는 CEGIS gate.
- Maynard/Selberg 계산은 bounded-gap 도구의 finite implementation test로만 유지한다.

폐기하거나 강등할 경로:

- bounded gaps, admissibility, positive singular series만으로 infinitely many gap-2 pairs를 추론.
- finite Fredholm/RMT fit을 exact prime-pair lower bound로 해석.
- `TP-CEGIS-14` finite weight optimization을 parity barrier 해결로 취급.
- generic Collatz frontier transfer를 Twin Prime 계산 진척으로 세는 것.

현재 가장 강한 미해결 정리:

```text
parity/deletion adversary를 통과하면서 exact gap-2 mass에 대해 무한히 자주 양의 하한을 주는
unconditional signed projection 또는 새로운 bilinear estimate.
```

반례에 관한 주의:

- Twin Prime 추측은 존재 명제이므로 유한 범위에서 pair가 없다는 사실은 반례가 아니다.
- 반증에는 어떤 유한 지점 이후 gap 2가 절대 나타나지 않는다는 전역 정리가 필요하다.

판정: bounded-gap 기술과 exact-gap 목표의 차이는 명확해졌지만 parity barrier를 넘는 새 estimate는 없다.

### 6. 유지, 보관, 폐기 정책

유지:

- bounded certificate와 그 생성 스크립트.
- candidate lemma를 직접 깨는 replayable witness.
- claim-language audit, artifact lineage, independent reproduction test.
- Collatz TICKET66-76 exact frontier 및 symbolic recurrence 계보.

보관하되 기본 화면에서 강등:

- 문제 고유 계산이 없는 cross-problem transfer 티켓.
- RMT/Fredholm/분포 적합처럼 탐색 아이디어만 제공하는 진단.
- CEGIS14 finite diagnostics.

증명 경로에서 폐기:

- finite-to-infinite promotion.
- density-one-to-universal promotion.
- bounded-gap-to-exact-gap substitution.
- surrogate-to-target substitution.
- exact length를 포함한 growing coordinate를 finite automaton이라고 부르는 것.

### 7. 다음 연구 순서

1. Collatz: TICKET85가 접근 가능한 cycle coefficient supremum `1`을 판정했으므로, `D(k)>=log2(k)-B(k)`의 additive loss를 줄이고 모든 메르센 지수의 `log2(k)+O(1)` upper bound를 별도로 공격한다.
2. Collatz: 반례 트랙은 한 fixed-prefix ghost를 자연수로 오인하지 말고, prefix length가 무한히 바뀌는 compatible positive-integer path의 존재와 divergence를 각각 인증한다.
3. RH: finite coefficient 실험을 늘리지 말고, 실제 explicit formula에서 off-critical zero의 detector latency를 상계하는 inequality만 공격한다.
4. Goldbach: 모든 상수를 출처와 함께 ledger에 넣고 cutoff overlap 가능성을 interval arithmetic으로 판정한다.
5. Twin Prime: bounded-gap 가중치 최적화를 중단하고 exact gap-2 signed projection의 parity adversary부터 통과시킨다.
6. 네 문제 공통: 새 후보는 먼저 CEGIS로 반박하고, 살아남은 경우에만 Lean/interval certificate로 승격한다.

### 8. 현재 순위

| 문제 | 실제 문제 고유 계산 | 가장 강한 산출물 | 핵심 공백 | 우선순위 |
|---|---:|---|---|---:|
| Collatz | 높음 | finite 2-adic natural-separator no-go | Archimedean + 2-adic coupled descent | 1 |
| Goldbach | 중간 | finite representation과 explicit-budget reduction | effective positive lower bound | 2 |
| Riemann | 중간 | finite-prefix nonuniversality discipline | actual-zeta all-height detector | 3 |
| Twin Prime | 중간 | exact-gap/deletion separation | parity-breaking gap-2 lower bound | 4 |

이 순위는 “증명에 가까운 정도”가 아니라 다음 falsifiable lemma를 만들 수 있는 실용성 순위다.

## English Consolidation

### Executive conclusion

PrimeProject has proved or disproved none of the four open problems. Its defensible contribution is a falsification-oriented workbench that separates bounded certificates from infinite claims, records replayable failures of candidate lemmas, and exposes the missing quantifier in each route.

The only TICKET66-77 track with problem-specific exact computation is Collatz. The corresponding Riemann, Goldbach, and Twin Prime artifacts are methodological transfers unless they contain an explicitly named problem-specific computation. They must not be counted as equal progress.

### Current research boundary

- Riemann: retain finite-prefix nonuniversality and candidate-kernel falsification. The missing object is an effective all-height theorem tied to actual zeta zeros, not a larger Jensen or Li prefix.
- Collatz: retain exact congruence lineage, the TICKET78 finite-cylinder theorem, and the TICKET79 bounded-rank no-go. The missing object is a minimal-counterexample contradiction or an adaptive, unbounded but demonstrably well-founded descent mechanism.
- Goldbach: retain finite representation certificates and the explicit main-term-minus-error reduction. The missing object is an effective positive lower bound whose cutoff overlaps the finite certificate.
- Twin Prime: retain deletion countermodels separating bounded gaps from exact gap 2. The missing object is an unconditional exact-gap lower bound that survives parity adversaries.

### TICKET75 result

TICKET75 replayed all 15,696 fifth-lift and 78,315 sixth-lift Collatz open-pressure rows with zero congruence-extension failures. Eight fixed finite pre-outcome coordinates were tested. None passed the combined observed closure, projected-cycle, and outcome-determinism gate.

The coarsest coordinate leaked only 11 of 78,315 sixth-lift rows, but retained 66 cyclic nodes and 59 mixed outcome keys. The richest coordinate reduced mixed keys to four, but 77,998 of 78,315 rows entered coordinate classes outside the observed source cover. The earlier `base_prefix_consumed` DAG rank is not a finite-state invariant because it contains exact, unbounded prefix and consumed lengths.

This establishes a finite compression-versus-state-growth obstruction for the tested coordinate grammar. It is not a Collatz proof, a Collatz counterexample, or a theorem excluding all possible coordinates.

### TICKET76 result

TICKET76 derives an exact recurrence at the first lift-unstable valuation boundary. For a stable prefix of length `m` consuming `s` bits from a modulus of `b` bits, let `d=b-s`, `A=(3T^m(r)+1)/2^d`, and `u=3^(m+1)`. Appending the four-bit digit `h` gives

```text
v_new = d + v2(A + h*u).
```

If the child remains unresolved, then

```text
A_next = (A + h*u) / 16.
```

All 297,104 audited fifth- and sixth-layer transitions satisfy the stable-prefix replay, affine identity, first-valuation formula, and unresolved recurrence with zero failures. Fixed quotient precisions `q=5,9,13,17,21` have respectively `165, 1,536, 1,235, 106, 15` observed successor-collision keys. Giving the predictor `q+4` quotient bits removes every collision on the same rows.

This explains the TICKET75 state-growth obstruction: division by 16 exposes four previously unrecorded higher bits at every unresolved lift. It refutes fixed-low-bit boundary-quotient closure on the tested reachable states. It does not exclude an arithmetic restriction on all reachable quotients, an infinite-state well-founded rank, or an all-depth 2-adic pressure path.

### TICKET77 result

Let `u=3^(m+1)`, let `h(A)` be the unique digit in `{0,...,15}` satisfying `A+h(A)u = 0 mod 16`, and define `P(A)=(A+h(A)u)/16`.

Reachability gives `2^d A=3T^m(r)+1`, hence `3` does not divide `A`. If `A>u`, then `0<P(A)<A`; any infinite pressure path therefore enters `1<=A<u`. In that interval, `P(A)` is the least positive representative of `16^(-1)A modulo u`. LTE gives

```text
ord_(3^(m+1))(16) = 3^m.
```

For `m>=1`, the orbit is the complete unit class having the same residue modulo 3 and contains both even and odd representatives. The first TICKET77 draft incorrectly promoted odd `P(A)` to stable-prefix extinction. Odd parity only means that the valuation reaches the current modulus boundary exactly; TICKET76 requires that equality step to be rolled back before the next refinement. The normalized fixed-prefix orbit therefore continues.

The all-depth compatible cylinders converge to a 2-adic point `N` satisfying `T^m(N)=-1/3`, which is not a positive integer. All 18,569 reconstructed fifth- and sixth-layer sources reach an equality boundary within at most 15 strict-pressure steps, with zero prerequisite, one-step identity, unexpected-strict-cycle, or trace-guard failures. This classifies a fixed-prefix false-counterexample route; it does not prove Collatz. The unresolved question is whether changing-prefix approximations by positive integers admit a well-founded admissibility rank.

### TICKET78 result

For a positive accelerated valuation word `a=(a_1,...,a_m)` with total `S`, exact composition gives

```text
T^m(n) = (3^m*n+C_m)/2^S,
r_a = 3^(-m)*(2^S-C_m) mod 2^(S+1).
```

The word is realized exactly by the cylinder `n=r_a+q2^(S+1)`. It therefore has infinitely many positive-integer realizers. Every finite neighborhood of a TICKET77 ghost contains positive naturals, and no locally constant finite-state 2-adic classifier can accept every positive integer while rejecting that ghost.

The machine audit enumerates all 65,535 positive valuation compositions with `S<=16` and replays four positive representatives per word, 262,140 representatives total. Residue collisions, formula failures, replay failures, and count-identity failures are all zero.

This no-go result is an elementary consequence of finite cylinders and 2-adic density, placed in the established Bernstein–Lagarias conjugacy context. It does not claim a new conjugacy theorem. It rules out a purely finite 2-adic natural-admissibility rank and promotes `ArchimedeanTwoAdicCoupledDescent` as the next target.

### TICKET79 result

TICKET79 tests the first bounded Archimedean-plus-2-adic rank class left by TICKET78:

```text
R(n)=alpha*log(n)+b(s(n)), with finite S and bounded b:S->R.
```

Two exact positive-integer families give a complete coefficient trichotomy. The family `E_(m,q)=2^(m+1)q-1` has `m` consecutive accelerated valuations equal to 1 and grows by more than `(3/2)^m`. It defeats every positive log coefficient plus bounded correction. The family `D_r=(5*2^(2r+1)-1)/3` maps in one accelerated step to the nonterminal value 5 and defeats every negative log coefficient plus bounded correction. When the log coefficient is zero, a `K`-state correction repeats a state on a `K`-edge expansion block and cannot strictly decrease on every edge.

For nonzero log coefficient the correction may use infinitely many states or growing 2-adic precision; boundedness alone is enough for the contradiction. The audit checks 1,024 expansion cases, 131,584 accelerated expansion steps, 128 nonterminal contractions, and 35 coefficient-budget examples with zero failures.

This is a restricted one-step rank no-go theorem, not a Collatz proof. Adaptive multi-step descent and unbounded corrections remain open, but any unbounded correction must also have an independently proved global lower bound. The next target is `MinimalCounterexampleValuationSurplusContradiction`, combining every least-counterexample non-descent inequality with the exact TICKET78 cylinder congruences.

### TICKET80 result

For every finite horizon `H` and finite lower bound `B`, the positive integer

```text
q=ceil((B+1)/2^(H+1)), n=2^(H+1)q-1
```

has `H` consecutive accelerated valuations equal to 1 and satisfies `A^j(n)>n` for every `1<=j<=H`. Hence every finite truncation of the exact cylinder and least-counterexample prefix non-descent constraints is satisfiable arbitrarily far out.

The nested witnesses `x_H=2^(H+1)-1` tend to positive infinity ordinarily but converge to `-1` in `Z_2`; `-1` is an accelerated valuation-1 fixed point and is not positive. Thus 2-adic compactness alone cannot promote finite witnesses to a positive counterexample. A compatible nested cylinder represents a positive ordinary integer exactly when its least nonnegative residues eventually stabilize at one positive value.

The audit checks 2,560 horizon/lower-bound witnesses and 656,640 accelerated steps through horizon 512 with zero failures. The symbolic theorem is valid for arbitrary finite `H,B`. This is a finite-prefix compactness no-go, not a Collatz result. The next target is `LeastCounterexampleUniformHeightBound` for one fixed stabilized natural cylinder path.

### TICKET81 결과 / result

TICKET81은 TICKET80의 양의 정수 안정화 조건을 실제로 만족하는 메르센 시작값 `N_k=2^k-1`을 사용해, 첫 보상 valuation이 하강을 강제하는지 판정했다. 처음 `k-1`단계는 정확히

```text
A^j(N_k)=3^j*2^(k-j)-1,  a_1=...=a_(k-1)=1
```

이고, 그 다음은 `A^k(N_k)=oddpart(3^k-1)`이다. LTE에 의해 다음 valuation은 홀수 `k`에서 `2`, 짝수 `k`에서 `3+v2(k)`다. 첫 보상 뒤 하강은 정확히 `k={2,4,8}`에서만 발생하고, 모든 홀수 `k>=3`, `k=6`, 모든 짝수 `k>=10`에서는 발생하지 않는다. 무한 구간은 기호 부등식으로 증명하고 네 개의 작은 짝수만 직접 계산했다.

The machine audit replays 1,023 starts and 523,776 expansion steps through `k=1024`, with zero formula or classification failures. Computation audits the implementation; the exact induction, LTE identity, and inequalities prove the classification for every `k>=2`.

폐기할 경로는 “안정화된 긴 팽창 뒤 첫 큰 valuation 하나가 누적 팽창을 상쇄한다”는 규칙이다. 다음 허용 목표는 `MersenneAdaptiveCompensationWindow`이며, 메르센 계열의 이후 여러 단계에 대한 누적 valuation을 다룬다. 성공해도 메르센 무한 계열 정리일 뿐 콜라츠 전체 증명은 아니다. 다른 세 난제에는 국소 보상 하나를 전역 논증으로 승격하지 말라는 검증 규율만 전이하며, 콜라츠 식이나 결론을 전이하지 않는다.

### TICKET82 결과 / result

TICKET82는 적응 창의 첫 후보인 모든 상수 길이를 제거했다. 기준 지수 `k=3`의 post-compensation valuation word `3,4,2,2,...`는 `H>=2`에 대해 `k=3 mod 2^(2H+3)`인 지수 합동류 전체에서 깊이 `H`까지 정확히 보존된다. 각 기호 iterate는 `(3^(k+t)+c_t)/2^d_t`이고, 고정 `H`에서는 `c_t,d_t`가 상수이므로 충분히 큰 합동류 지수에서 모든 `0<=t<=H` iterate가 `2^k-1`보다 크다.

Thus the Mersenne post-expansion stopping delay is unbounded. The audit covers 129 horizons, 8,385 symbolic states, and 8,256 transition conditions with zero failures. This proves neither divergence nor Collatz: each finite prefix may descend after its prescribed horizon. The next target is the genuinely growing-window theorem `MersenneGrowingWindowDescent`.

### TICKET83 결과 / result

명시적 수열 `k_H=3+2^(2H+3)`에서 TICKET82의 접두 보존과 `|c_t|<2^d_t`, `d_t<=2H+4`를 결합하면 `D(k_H)>H`다. 또한 `k_H<2^(2H+4)`이므로 `D(k_H)>H>(1/2)log2(k_H)-2`다. 따라서 `o(log k)` 창과 계수 `1/2` 미만의 로그 창은 무한 부분수열에서 실패한다. 255개 horizon과 33,150개 기호 상태를 감사했고 실패는 0개다. 이는 발산이 아니라 유한 하강 지연의 정량 하한이다.

### TICKET84 결과 / result

`3^kappa=-13`인 접근 가능한 2진 지수는 `-7↔-5` valuation 주기 `2,1`을 만든다. 유한 정밀도 잔여만 양의 지수로 lift하면 `D(k_H)>H>(2/3)log2(k_H)-1`이다. 음의 주기는 자연수 반례가 아니며 유한 접두 생성기다. TICKET83의 계수 `1/2`는 폐기되고 `2/3`으로 개선됐지만 최적성은 열려 있다.

### TICKET85 결과 / result

`w_m=(2,1^(m-1))`은 모든 `m>=2`에서 exact하고 exponent image에 접근 가능하며 reciprocal mean `m/(m+1)`을 갖는다. 따라서 supremum은 1이다. all-ones cycle `-1`은 exponent target이 `7 mod 8`이므로 달성되지 않는다. `m=H`를 선택하면 `D(k_H)>H>log2(k_H)-2`이고 모든 `c<1` 로그 창은 고정 additive constant와 무관하게 실패한다.

### Promotion rule

A future ticket may be described as proof progress only if it does at least one of the following:

1. proves a new problem-specific infinite lemma without importing an equivalent form of the target conjecture;
2. certifies an exact counterexample to the original statement;
3. strictly removes a recorded obstruction with a replayable proof object;
4. gives a formal reduction whose remaining assumptions are strictly weaker and independently checkable.

Larger finite bounds, better plots, statistical fit, metadata-only Lean files, and generic cross-problem transfers do not satisfy this rule.
