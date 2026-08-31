# TICKET-261: 날카로움, Weyl 조화성분, 특수 동률, 양방향 합동

상태: **이번 회차는 완료되었지만 네 상위 추측은 모두 미해결·미증명이다.**

TICKET-261은 exact route no-go 두 개와 부분정리 두 개를 확립한다. 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다. 정준 기계 기록은 `data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json`이다.

| 문제 | 공격한 정확 명제 | 결과 | 분류 | 상위 문제 상태 |
|---|---|---|---|---|
| 리만 가설 | eventual positive packet lag이면 scaled downward variation이 합 가능하다 | reciprocal-tail 정확 반례 | `exact_no_go` | `open_not_proven` |
| 콜라츠 추측 | 증가 모듈러스의 첫 Weyl 조화성분 상쇄가 angular discrepancy 0을 강제한다 | 두 cluster 소수 모듈러스 정확 반례 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | 특수 q=3 소수경주 동률이 임의의 비영 residue product와 양립한다 | 동률은 product `+1 mod 3`을 강제하며 `-1`은 동률을 배제 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 남은 coefficient-one 가지에는 분모 쪽 2차 합동만 존재한다 | 분자 쪽 dual 합동과 1,024 수렴분수 인증 | `partial_theorem` | `open_not_proven` |

## 재현 계약

```powershell
python scripts/ticket261_sharpness_weyl_ties_dualcongruence.py
python -m unittest tests.test_ticket261_sharpness_weyl_ties_dualcongruence
python scripts/verify_ticket261_structure.py
```

증명에 쓰이는 계산은 전부 정수 또는 `Fraction`이다. fraction record의 부동소수점 필드는 표시 전용이며 증명에 사용하지 않는다. 난수 seed는 없다. 각 transcript SHA-256은 machine JSON에 기록된다.

## 1. 리만 가설

### A. 정확한 명제

임의의 실수 `L,c>0`에 대해

\[
E_n=L+\frac{c}{n},\qquad
d_n=(E_n-E_{n+1})_+,\qquad
S_n=(n+1)E_{n+1}-nE_n
\]

으로 둔다. 그러면 `E_n -> L`, 모든 `S_n=L>0`이지만

\[
\sum_{n\ge1}n d_n=\infty.
\]

따라서 TICKET-260의 summable scaled-downward-variation 조건은 eventual lag positivity의 충분조건이지만 필요조건은 아니다.

### B–D. 정의, 증명, 단계별 근거

직접 빼면

\[
d_n=\frac{c}{n(n+1)},\qquad nd_n=\frac{c}{n+1}.
\]

조화급수가 발산하므로 가중 하강변동 급수는 발산한다. 반면

\[
nE_n=nL+c,\qquad (n+1)E_{n+1}=(n+1)L+c
\]

이므로 모든 `n`에서 `S_n=L`이다. 무한 결론은 닫힌식과 조화급수 발산에서 나오며 유한 계산에 의존하지 않는다.

### E. 반례와 경계조건

이 counterfamily는 합 가능성을 제외한 추상 전제를 만족하고, 원하는 결론을 정확한 상수 margin으로 만족한다. 따라서 TICKET-260 조건을 특성화 정리로 올릴 수 없다.

이 수열은 실제 Guinand-Weil packet이 아니다. 그러므로 추상 조건의 필요성만 반박하며, 실제 packet의 합 가능성이나 RH를 반박하지 않는다.

### F–H. 재현 계산과 유한 한계

생성기는 `L=c=1`, `1<=n<=128`에서

\[
E_n=1+1/n,\ d_n=1/[n(n+1)],\ nd_n=1/(n+1),\ S_n=1
\]

을 exact rational arithmetic으로 확인한다. 복잡도는 `O(N)`이다. 128행은 재현용이며 발산의 근거가 아니다. 실제 Weil 계수는 계산하지 않는다.

Transcript: `8242a67f0d5c2c2b451cef1cb2c48100ffaa008fa05b402ac6274da8a88b670b`.

### I–K. 분류, 남은 간극, 다음 보조정리

- 분류: `exact_no_go`.
- 폐기: summable scaled variation을 eventual packet-lag positivity의 필요조건으로 사용하는 경로.
- 남은 간극: 실제 Guinand-Weil packet에 대해 더 약한 scaled-jump 추정도 증명되지 않았다.
- 다음 단일 보조정리: `ActualWeilPacketScaledDownwardJumpLimsupBelowLimit`.

## 2. 콜라츠 추측

### A. 정확한 명제

서로 다른 증가하는 홀수 소수 `q_j`와 `1<=d_j<q_j`가 존재하여

\[
\frac1N\sum_{j\le N}\exp(2\pi i d_j/q_j)\longrightarrow0
\]

이지만 `x_j=d_j/q_j`의 star discrepancy는 `liminf`가 적어도 `1/6`이다. 즉 첫 Weyl 조화성분 하나의 상쇄만으로 증가 소수 모듈러스 각도 균등분포를 얻을 수 없다.

### B–D. 구성과 증명

`q_j`를 `max(q_(j-1),j^3,13)`보다 큰 최소 소수로 두고

\[
d_j=\lfloor q_j/4\rfloor\quad(j\text{ 홀수}),\qquad
d_j=\lfloor3q_j/4\rfloor\quad(j\text{ 짝수})
\]

로 둔다. 정규화된 점은 `1/4`, `3/4`에서 각각 `1/q_j` 이내다. 이상적인 첫 조화성분은 `i,-i`로 쌍마다 상쇄된다. `pi<4`와 chord bound를 쓰면 각 오차는 `8/q_j` 이하이고,

\[
\sum_j 8/q_j<8\sum_jj^{-3}<16.
\]

따라서 `N`으로 나눈 첫 조화성분은 0으로 간다.

한편 `[0,1/3)`에는 정확히 `ceil(N/2)`개의 점이 있으므로

\[
D_N^*\ge\frac{\lceil N/2\rceil}{N}-\frac13\longrightarrow\frac16.
\]

이는 선언된 증가 소수 모듈러스 정의역 안의 정확한 반례다.

### E. 적대적 검사와 canonical 계산

이 구성의 지수는 의도적으로 canonical Fermat quotient가 아니다. 일반적인 one-harmonic 전달 명제를 반박할 뿐 canonical 수열을 판정하지 않는다.

별도의 유한 진단으로 소수 `q>5`에 대해

\[
F_q(a)=\frac{a^{q-1}-1}{q}\pmod q,\qquad
D_q=5F_q(2)-3F_q(3)\pmod q
\]

를 exact 계산한다. 최초 `2^k`, `k=3,...,14`개의 canonical 점 `D_q/q`에 대한 star discrepancy를 유리수로 계산했다. dyadic prefix에서 단조 감소하지 않으며, 최초 증가는 2,048에서 4,096으로 갈 때 발생하고 16,384에서도 다시 증가한다. 이것은 단조 prefix 외삽의 유한 반례이지 eventual decay의 반례가 아니다.

### F–H. 재현 계산과 유한 한계

- countermodel: 소수 모듈러스 128행과 exact rational chord envelope.
- canonical 진단: `q=180539`까지 16,384개 소수, dyadic discrepancy 12행.
- `D_2048*=111589/7366144`, `D_4096*=656411/39704576`이며 뒤 값이 더 크다.
- 복잡도: 결정적 소수 탐색, modular exponentiation, `O(P log P)` Fraction 정렬.
- 복소 부동소수점 단위근은 계산하지 않는다.

Transcript: `35619c4243f9a4fa6ba7eff5764787d0ee3212d8f9decca0e85938e01b2de750`.

유한 canonical 표는 discrepancy의 극한을 증명하지 않는다.

### I–K. 분류, 남은 간극, 다음 보조정리

- 분류: `exact_no_go`.
- 폐기: 첫 growing-modulus Weyl 조화성분만으로 angular discrepancy decay를 얻는 경로.
- 남은 간극: canonical Fermat-quotient 각도의 모든 비영 조화성분에 대한 상쇄 정리가 없다.
- 다음 단일 보조정리: `CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH`.

## 3. 강한 골드바흐 추측

### A. 정확한 명제

`l>=0`에 대해

\[
T_l=6\cdot3^{6l+2}+3
\]

로 두고, 최초 `T_l`개 소수 중 소수 3을 제외한 수의 mod 3 곱을 `P_l`이라 하자. `T_l`에서 mod-3 소수경주가 동률이면

\[
P_l\equiv1\pmod3.
\]

따라서 `P_l=-1 mod 3`은 TICKET-260 compatible prefix를 배제하는 정확한 충분 certificate다.

### B–D. 정의와 증명

소수 3 이후의 소수는 mod 3에서 `+1` 또는 `-1`이다. 동률이면

\[
N_1=N_2=(T_l-1)/2=3\cdot3^{6l+2}+1.
\]

`3^(6l+2)`는 홀수이므로 이 공통 개수는 짝수다. 따라서 비영 residue symbol의 곱은

\[
(+1)^{N_1}(-1)^{N_2}=+1\pmod3.
\]

그 대우가 product-minus-one certificate를 준다.

### E. density-only no-go

하나의 zero symbol 뒤에 `+1,-1`을 무한히 교대로 놓는다. 모든 보통 prefix discrepancy는 1 이하이고 두 비영 symbol의 밀도는 각각 1/2로 간다. 그러나 모든 `T_l-1`은 짝수이므로 모든 특수 prefix에서 정확한 동률이며 곱은 `+1`이다.

따라서 PNT-in-progressions 수준의 밀도 균형, 심지어 이 추상 residue 모델의 bounded discrepancy만으로 sparse exact tie를 배제할 수 없다. 이 수열을 실제 소수 residue 수열이라고 주장하지 않는다.

### F–H. 정확 certificate와 유한 한계

TICKET-260의 두 독립 residue 알고리즘을 `l=0,1,2`에서 재사용한다. 실제 `N_2`는 모두 홀수이므로 `P_l=-1 mod 3`이다.

| `l` | `T_l` | 끝점 | `(N_0,N_1,N_2)` | `P_l mod 3` |
|---:|---:|---:|---:|---:|
| 0 | 57 | 269 | `(1,25,31)` | 2 |
| 1 | 39,369 | 471,749 | `(1,19,663,19,705)` | 2 |
| 2 | 28,697,817 | 547,035,959 | `(1,14,347,849,14,349,967)` | 2 |

16개 symbolic alternating level은 무한 no-go를 재현한다. 실제 소수 계산은 여전히 세 level뿐이다.

Transcript: `7c01ec5d388159c3ba032b8f87459f71cbd4bc339f2f181ef6bc6113075d810c`.

### I–K. 분류, 남은 간극, 다음 보조정리

- 분류: `partial_theorem`.
- 폐기: density balance만으로 exact non-tie를 얻는 경로.
- 남은 간극: 모든 특수 prime prefix에서 `P_l=-1 mod 3`임을 보이는 정리가 없다.
- 다음 단일 보조정리: `Q3SpecialPrimePrefixProductIsMinusOneModuloThree`.

## 4. 쌍둥이 소수 추측 — deep focus

### A. 정확한 명제

`B_1(u,v)`를

\[
(1+\sqrt2)(u+v\sqrt2)^{17}
\]

의 `sqrt(2)` 계수라 하자. `uv!=0`, `epsilon in {-1,1}`인 정수에 대해 `B_1(u,v)=epsilon`이면

\[
u^{17}+17u^{16}v\equiv\epsilon\pmod{v^2}
\]

이고 동시에

\[
256v^{17}+4352uv^{16}\equiv\epsilon\pmod{u^2}
\]

이다. TICKET-258이 격리한 유일한 근의 최초 1,024개 인증 연분수 수렴분수에서는 양 부호 모두 공동 2차 조건을 통과하지 못한다.

### B–D. 전개와 증명

동차형의 낮은 `v` 차수 쪽은

\[
B_1(u,v)=u^{17}+17u^{16}v+v^2R(u,v)
\]

이다. 낮은 `u` 차수 쪽의 마지막 두 이항계수는

\[
2^8v^{17}=256v^{17},\qquad17\cdot2^8uv^{16}=4352uv^{16}
\]

이므로

\[
B_1(u,v)=256v^{17}+4352uv^{16}+u^2Q(u,v).
\]

각각 mod `v^2`, mod `u^2`로 줄이면 두 필요조건이 나온다. 이 합동 유도에는 근의 수치 근사가 사용되지 않는다.

### E. 약한 경로의 정확 반례

분모 1차 조건은 `(-1,13,-1)`, `(-1,14,-1)`을 통과시킨다. 비자명 분자 1차 조건은 `(-3,41,-1)`을 통과시키지만 새 mod `u^2` 조건에서는 실패한다. 따라서 분자·분모 1차 필터는 2차 조건의 완전한 대체물이 아니다.

이 witness들은 `B_1(u,v)=epsilon`을 만족하지 않는다. 이들은 필요 1차 필터의 완전성만 반박한다.

### F–H. 재현 계산과 유한 한계

1,024개 인증 수렴분수와 두 부호 각각에 대해 생성기는 다음을 수행한다.

1. 두 1차 residue 계산;
2. mod `v^2`, mod `u^2` truncated residue 계산;
3. 전체 정수 `B_1` 독립 계산;
4. 두 truncated residue와 전체 값 비교;
5. 전체 계수 hash와 유리수 근 bracket 기록.

마지막 분모는 519자리다.

- 분모 1차 비자명 통과: 2;
- 분모 2차 통과: 0;
- 분자 1차 비자명 통과: 1;
- 분자 2차 비자명 통과: 0;
- 공동 2차 통과: 0.

복잡도는 인증 수렴분수 수에 선형이며 growing exact integer에서 modular arithmetic을 수행한다. 1,024개에서 hit가 없다는 사실은 유한 certificate일 뿐이다.

Transcript: `3327f229884ca78a1b95a3b2336cc245e4e99cbfff8f2020a24db3299754b70e`.

### I–K. 분류, 남은 간극, 다음 보조정리

- 분류: `partial_theorem`.
- 폐기: 두 1차 합동을 완전한 convergent filter로 사용하는 경로.
- 남은 간극: 뒤의 무한히 많은 unique-root 수렴분수는 통제되지 않았다.
- 다음 단일 보조정리: `NoUniqueRootConvergentSatisfiesBothSecondOrderCongruences`.

## 적대적 증명 감사

- 양화사: 무한 명제는 기호적으로 증명했고 모든 prefix 계산은 유한으로 표시했다.
- 균일성: 점별 결론을 actual-Weil, canonical-angle, all-level prime-race, all-convergent 정리로 확대하지 않았다.
- 정의역: Collatz no-go는 실제 서로 다른 소수 모듈러스지만 비정준 지수를 쓴다. Goldbach alternating 수열은 추상 모델이다. Twin 합동은 비영 정수 `u,v`에 적용된다.
- 분모: `u=0`은 dual 합동 명제 밖이며 `B_1(u,v)=±1`을 풀 수 없다. 인증 가지에서 modulus는 `|u|`와 양의 `v`를 쓴다.
- 독립 검사: Goldbach는 두 residue 알고리즘을 유지한다. Twin은 두 truncated 전개를 전체 form과 비교한다. Collatz는 Fermat quotient와 정렬 discrepancy witness를 다시 계산한다.
- proof DAG: 각 track은 proved 선행 노드, proved TICKET-261 정리, finite certificate, disproved 경로, 하나의 open frontier를 가진다. 네 DAG 모두 비순환이다.

## 최종 주장 경계

새로 확정: exact route no-go 두 개와 부분정리 두 개. 폐기: RH scaled-variation 합 가능성의 필요성, Collatz one-harmonic discrepancy 전달, Goldbach density-only tie 배제, Twin bidirectional first-order 완전 필터. 미증명: actual-Weil 추정 전부, canonical Fermat quotient 모든 조화성분 추정, all-level q=3 product 부호, all-convergent 2차 배제, 네 상위 추측 전부.
