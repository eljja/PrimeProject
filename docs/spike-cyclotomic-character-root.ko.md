# TICKET-257: 스파이크·원분·지표·근 이웃 감사

상태: **이번 회차는 완료되었으나 네 상위 추측은 모두 미해결**이다.

이 문서는 TICKET-256을 잇는다. 각 문제마다 하나의 정확한 목표를 먼저 선언하고, 대수적 증명과 유한 계산을 분리하며, 실패한 경로는 가능한 경우 정확한 no-go로 확정하고, 다음 단일 보조정리 하나만 남긴다. 기계 판독 원본은 `data/open-problem/ticket257-spike-cyclotomic-character-root.json`이며, 네 proof DAG는 형식화된 노드만 사용하고 각각 열린 전선이 정확히 하나다.

## 회차 경계

| 문제 | TICKET-257의 정확한 목표 | 결과 분류 | 상위 문제 |
|---|---|---|---|
| 리만 가설 | `PositiveConvergentPacketEnergyLagPartialSumNoGo` | 정확한 no-go | 미해결 |
| 콜라츠 추측 | `DistinctPrimeCyclotomicPhaseExactCancellationNoGo` | 정확한 no-go | 미해결 |
| 강한 골드바흐 추측 | `QuadraticCharacterReflectionObstructionAndNextPrefixExclusion` | 부분정리 | 미해결 |
| 쌍둥이 소수 추측 | `UniqueRealRootNeighborReductionAndBoundedExclusion` | 부분정리 | 미해결 |

후보 해결은 0건이고 추측 해결도 0건이다.

## 1. 리만 가설

### A. 이번에 증명·반증할 정확한 명제

정규화된 all-ones packet energy가 모든 (L)에서 (E_L\geq1/2)이고 (E_L\to1)이지만, 대칭 lag 부분합은 아래로 유계가 아닌 실수 Toeplitz lag 열이 존재한다. 구체적으로

\[
E_L=\begin{cases}
1-2^{-k},&L=4^k,\ k\geq1,\\
1,&\text{그 밖의 경우}
\end{cases}
\]

로 정하고 (S_n=(n+1)E_{n+1}-nE_n), (a_0=S_0), (a_n=(S_n-S_{n-1})/2)로 복원한다. 그러면 (S_{4^k-1}=1-2^k\to-\infty)이다. 따라서 TICKET-256의 균일 부분합 하한은 packet energy의 양성과 수렴만으로 도출할 수 없다.

동시에 다음 수선 조건을 증명한다.

\[
\delta=\inf_LE_L>0,\qquad V=\sup_LL(E_L-E_{L+1})_+<\delta
\]

이면 모든 (L)에 대해 (S_L\geq\delta-V>0)이다.

### B. 수학적 논증

TICKET-256의 정확한 Cesàro 항등식은

\[
E_L=\frac1L\sum_{n=0}^{L-1}S_n
\]

이다. 차분을 취하면 (S_n=(n+1)E_{n+1}-nE_n)이므로 위 복원이 지정한 에너지를 정확히 실현한다. 에너지의 최솟값은 (1/2)이고 예외점의 결손 (2^{-k})가 0으로 가므로 (E_L\to1)이다. (L=4^k) 직전에는

\[
S_{L-1}=LE_L-(L-1)E_{L-1}=1-2^k
\]

이다. 수선 조건은

\[
S_L=E_{L+1}-L(E_L-E_{L+1})\geq\delta-V
\]

에서 즉시 따른다. 이 논증은 모든 (L)에 대한 대수적 증명이다.

### C. 재현 계산과 적대적 검사

생성기는 정확한 유리수로 lag를 복원하고 (k=1,\ldots,8), 즉 (L=65{,}536)까지 에너지를 원식에서 재계산한다. 모든 행에서 (E_L=1-2^{-k}), (S_{L-1}=1-2^k)를 확인한다. 난수는 쓰지 않는다.

### D. 논리·유한 계산의 한계

이 열은 추상 Toeplitz 열일 뿐 실제 Guinand-Weil 형식에서 나온다고 증명하지 않았다. 따라서 RH를 증명하거나 반증하지 않는다. 유한 8행은 구현 일관성 검사이며, 수렴과 아래로 무계성은 공식이 증명한다.

### E. 경로 판정

- 폐기: 양성과 수렴만으로 균일 lag 부분합 하한을 도출하는 경로.
- 유지: scaled downward variation 수선 기준.
- 다음 단일 보조정리: `ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`.

## 2. 콜라츠 추측

### A. 이번에 증명·반증할 정확한 명제

서로 다른 홀수 소수 (q_1,\ldots,q_N), 원시 (q)차 단위원 (\zeta_q), 임의의 (d_j\bmod q_j)에 대해

\[
\sum_{j=1}^N\zeta_{q_j}^{d_j}\neq0.
\]

따라서 표준 위상

\[
\exp(2\pi iD_q/q),\qquad D_q=5F_q(2)-3F_q(3)
\]

의 어떤 유한 접두사도 정확히 상쇄되지 않는다. 이는 유한 pairing/grouping 경로에 대한 정확한 장애물이지 정량적 상쇄 추정은 아니다.

### B. 수학적 논증

모든 (d_j=0)이면 합은 (N\neq0)이다. 어떤 (d_j\neq0)를 택하고 (m=\prod_{i\neq j}q_i), (F=\mathbb Q(\zeta_m))라 하자. 서로소 conductor이므로

\[
\mathbb Q(\zeta_m,\zeta_{q_j})=\mathbb Q(\zeta_{mq_j}).
\]

오일러 (\varphi)의 곱셈성으로 compositum 차수가 ([F:\mathbb Q](q_j-1))이므로 (F\cap\mathbb Q(\zeta_{q_j})=\mathbb Q)이다. 합이 0이면 (\zeta_{q_j}^{d_j}\in F)인데, (d_j)는 (q_j) modulo에서 가역이므로 (\zeta_{q_j}\in F)가 되어 모순이다.

### C. 재현 계산과 적대적 검사

(7\leq q\leq97)인 22개 소수에 대해 Fermat quotient를 정확한 모듈러 산술로 계산했다. 표준 지수는 모두 0이 아니다.

`(7,6), (11,3), (13,4), (17,1), (19,18), (23,11), (29,18), (31,10), (37,25), (41,11), (43,33), (47,46), (53,5), (59,35), (61,19), (67,5), (71,56), (73,56), (79,12), (83,48), (89,47), (97,70)`.

conductor 곱과 원분체 차수도 정수로 재검산한다. 단위원은 지수로 기호 표현하며 부동소수점 near-zero 판정을 사용하지 않는다.

### D. 논리·유한 계산의 한계

0이 아닌 유한합도 계열이 커질 때 0에 매우 가까워질 수 있다. 이 정리는 sublinear bound나 무한 소수 평균을 통제하지 않으며 콜라츠 하강을 함의하지 않는다.

### E. 경로 판정

- 폐기: 서로 다른 소수 modulus의 위상을 유한 pairing/grouping하여 정확한 0을 얻는 경로.
- 유지: 정확한 0과 점근 상쇄를 구분하는 원분체 선형 분리.
- 다음 단일 보조정리: `CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`.

## 3. 강한 골드바흐 추측 — 이번 심층 집중

### A. 이번에 증명·반증할 정확한 명제

(q\geq5)가 소수이고 첫 (T)개 소수의 (q) modulo 잔여류 개수를 (N_r)라 하자. (q) 자체가 한 번 포함되어 (N_0=1)이라 하자. 모든 비영 (r)에 대해 (N_r=N_{-r})이면

\[
\prod_{p\leq p_T,\ p\neq q}\chi_q(p)=\chi_q(-1)^{(T-1)/2}.
\]

따라서 불일치는 정확한 반사 비대칭 인증서이다. 더 일반적으로, 반사 대칭은 모든 홀수 곱셈 지표 moment

\[
\sum_{r\in\mathbb F_q^\times}N_r\chi(r)=0,
\qquad\chi(-1)=-1
\]

의 소멸과 동치다.

다음 호환 가능한 (q)-divisible 사례 ((q,m)=(11,22))에서 강제 접두사 길이는 (T=7{,}759{,}741)이다. 실제 quadratic product는 (-1\equiv10\pmod{11}), 대칭이 요구하는 값은 (+1)이므로 이 소수 접두사는 배제된다.

### B. 수학적 논증

반사 대칭이면 (r,-r) 쌍의 곱은 ((-r^2)^{N_r})이고 르장드르 기호는 (\chi_q(-1)^{N_r})이다. (T-1=2\sum_{\{r,-r\}}N_r)이므로 필요한 곱 항등식이 따른다.

완전 지표 조건에서 홀수 지표는 대칭쌍을 소거한다. 역으로 (A(r)=N_r-N_{-r})는 (\mathbb F_q^\times) 함수공간의 홀수 부분공간에 속한다. 모든 홀수 Fourier 계수가 0이면 곱셈 지표 역변환으로 (A=0), 즉 반사 대칭이다.

### C. 재현 계산과 적대적 검사

모든 소수를 저장하지 않는 exact odd-only segmented sieve로 다음을 얻었다.

| ((q,m)) | (T) | 마지막 소수 | 실제 잔여류 개수 | quadratic 불일치 |
|---|---:|---:|---|---|
| (5,10) | 1,255 | 10,243 | `[1,313,313,317,311]` | 없음 |
| (7,14) | 24,017 | 274,783 | `[1,3993,3991,4003,3998,4016,4015]` | 없음 |
| (11,22) | 7,759,741 | 137,141,243 | `[1,776123,776078,775943,775798,775646,776178,776150,775928,775841,776055]` | 있음 |

(q=11)의 반사 차이는

`[0,68,237,15,-352,-532,532,352,-15,-237,-68]`

이다. count vector에서 오일러 판정으로 곱을 독립 재계산했다. (q=5,7) 행은 적대적 대조군이다. 벡터는 비대칭이지만 quadratic bit는 대칭 기대값과 일치한다. 따라서 한 개의 quadratic character는 충분조건일 뿐 필요조건은 아니다.

### D. 논리·유한 계산의 한계

계산한 호환 행은 세 개뿐이고 최대 접두사 길이는 7,759,741이다. 유한 접두사 배제는 강한 골드바흐에 필요한 전칭 명제를 증명하지 않는다. 지표 역변환은 동치 재정식화이지 모든 접두사의 nonvanishing 증명이 아니다.

### E. 경로 판정

- 폐기: quadratic-character 1비트를 완전한 비대칭 검출기로 사용하는 경로. (q=5,7)이 정확한 반례다.
- 유지: 1비트 장애물, 모든 홀수 지표의 동치, 새 (q=11) 배제.
- 다음 단일 보조정리: `EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`.

## 4. 쌍둥이 소수 추측

### A. 이번에 증명·반증할 정확한 명제

(B_1(u,v))를

\[
(1+\sqrt2)(u+v\sqrt2)^{17}
\]

의 (\sqrt2) 계수라 하고 (P(x)=B_1(x,1))라 하자. (P)는 실수 전체에서 엄격히 증가하고 ((-1,0))에 유일한 무리근 (\rho)를 갖는다. 모든 정수해 (B_1(u,v)=1)은 ((1,0))이거나

\[
u=\lceil\rho v\rceil\ (v>0),\qquad
u=-\lfloor\rho|v|\rfloor\ (v<0)
\]

이다. (v\neq0)인 해는 primitive이고

\[
v\mid u^{17}-1,\qquad u\mid256v^{17}-1
\]

을 만족한다. 정확한 근 구간

\[
-0.073255<\rho<-0.07325499
\]

은 (0<|v|\leq200{,}000)의 모든 경우를 400,399개 정수 평가로 축소하며, 그중 값 1은 없다.

### B. 수학적 논증

(\varepsilon=1+\sqrt2)라 쓰면 켤레를 통해

\[
P(x)=\frac{\varepsilon(x+\sqrt2)^{17}+\varepsilon^{-1}(x-\sqrt2)^{17}}{2\sqrt2}
\]

를 얻는다. 도함수는 양의 짝수 거듭제곱 두 항의 합에 17을 곱한 것이므로 항상 양수다. 정확값 (P(-1)=-470832), (P(0)=256)으로 유일근이 ((-1,0))에 있고, 유리근 정리로 무리수다.

(v>0)를 고정하면 (B_1(u,v)=v^{17}P(u/v))는 (u)에 대해 엄격히 증가하는 정수열이다. 첫 양수는 (u=\lceil\rho v\rceil)에서 나오며 이후 값은 적어도 2이므로 이 점만 1일 수 있다. 홀수 차수 동차성으로 음의 (v) 공식이 따른다. 동차성은 (gcd(u,v)=1)도 강제하고, (v) 및 (u) modulo로 form을 줄이면 두 나눗셈 조건을 얻는다.

근 구간은 분모를 제거한 정수 다항식 부호로 검증한다. 구간 폭에 200,000을 곱한 값이 1보다 작으므로 부호별 후보가 최대 두 개다.

### C. 재현 계산과 적대적 검사

생성기는 구간 끝점의 부호를 정수로 계산하고 후보 완전한 1차원 열을 훑는다. 17차 정수 평가 400,399번에서 (v\neq0) 해는 없었다. (v=0)에서는 ((u,v)=(1,0))만 있으며 reduced norm은 (-1)이라 목표 branch에는 부적합하다. 난수는 쓰지 않는다.

### D. 논리·유한 계산의 한계

후보 축소는 전역 정리지만 배제 계산은 (|v|\leq200{,}000)에만 해당한다. 모든 분모의 coefficient-one 부재, 지수 17의 전역 배제, 쌍둥이 소수 추측은 증명하지 않았다.

### E. 경로 판정

- 폐기: surviving branch를 본질적인 2차원 (O(V^2)) box search로 다루는 경로.
- 유지: 정확한 1차원 근 이웃 열과 primitive 나눗셈 필터.
- 다음 단일 보조정리: `EveryNonzeroDenominatorUniqueRootNeighborMissesCoefficientOne`.

## 재현 및 감사 명령

```text
python scripts/ticket257_spike_cyclotomic_character_root.py
python -m unittest tests.test_ticket257_spike_cyclotomic_character_root -v
python scripts/verify_ticket257_structure.py
```

생성기는 정수·유리수 exact 산술을 사용한다. Goldbach 체는 결정적인 유한 계산이다. transcript SHA-256, 계산 범위, 개수, proof DAG, 경로 판정, claim boundary는 통합 JSON과 네 개의 문제별 JSON에 저장된다.

## 최종 판정

이번 회차에는 정확한 no-go 두 개와 부분정리 두 개가 새로 확정되었다. 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명되거나 반증되지 않았다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
