# TICKET-260: 가중 변동, 고정 모듈러스 균등분포, mod-3 소수경주, 가변 분모 체

날짜: 2026-08-31  
상태: 네 상위 추측 모두 `open_not_proven`  
Deep focus: 쌍둥이 소수 추측

이번 회차는 부분정리 3개와 정확한 경로 no-go 1개를 확정한다. 네 상위 추측 중 어느 것도 증명하거나 반증하지 않았다. 표준 기계 판독 기록은 `data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json`이다. 모든 증명 의존 계산은 정수 또는 유리수이며 부동소수점 값을 증명으로 사용하지 않는다.

## 1. 리만 가설

### A. 정확한 명제

`SummableScaledDownwardVariationForcesEventualLagPositivity`.

양의 실수열 ((E_n)_{n\ge1})이 (E_n\to L>0)을 만족한다고 하자. 다음을 정의한다.

\[
d_n=(E_n-E_{n+1})_+,
\qquad
S_n=(n+1)E_{n+1}-nE_n.
\]

만약

\[
\sum_{n\ge1} n d_n<\infty
\]

이면

\[
\liminf_{n\to\infty}S_n\ge L
\]

이고, 따라서 충분히 큰 모든 (n)에서 (S_n>0)이다.

참이면 TICKET-258의 유계 총변동 no-go와 TICKET-259의 임계 등호 no-go를 피하는 명시적 충분조건을 준다. 거짓이면 가중 단측 변동 경로를 폐기해야 한다.

### B–E. 정의, 증명, 적대적 감사

정확한 항등식

\[
S_n=E_{n+1}-n(E_n-E_{n+1})
\]

으로부터 (S_n\ge E_{n+1}-nd_n)이다. 음이 아닌 항의 급수가 수렴하면 각 항은 0으로 가므로 (nd_n\to0)이다. 또한 (E_{n+1}\to L)이므로 하극한을 취하면 명제가 증명된다.

양화사는 각 수열에 대한 점별 명제다. 이 정리는 수열들의 클래스 전체에 공통인 cutoff를 주장하지 않는다. 실제 Weil 형식의 양성을 전제로 다시 사용하지도 않는다.

### F–H. 재현 계산과 유한 경계

정확 재생 모형은

\[
E_{2^k+1}=1-2^{-3k},\qquad E_n=1\ \text{(그 밖의 경우)}
\]

이다. 가중 하강변동은

\[
\sum_{k\ge1}2^k2^{-3k}=\frac13
\]

이고 (n=2^k)에서

\[
S_n=1-\frac{n+1}{n^3}>0
\]

이다. `Fraction` 16행은 구현 재현용이며 무한 정리 자체의 근거는 위 논증이다. 실제 Guinand-Weil 계수는 계산하지 않았다.

### I–K. 분류, 간극, 다음 보조정리

- 분류: `partial_theorem`.
- 새 사실: 가중된 단측 하강변동의 합 가능성은 충분조건이다.
- 폐기 경로: (n)-가중 단측 조건 없는 통상적 유계 총변동만으로의 추론.
- 최소 간극: 실제 packet energy가 이 가정을 만족함을 증명해야 한다.
- 다음 단일 보조정리: `ActualWeilPacketScaledDownwardVariationIsSummable`.

## 2. 콜라츠 추측

### A. 정확한 명제

`FixedModulusExponentEquidistributionPhaseAlignmentNoGo`.

서로 다른 소수 (q_j)와 (1\le d_j<q_j)인 정수열이 존재하여, 모든 고정 (M\ge2)와 모든 (N\ge1)에 대해 (d_1,\ldots,d_N)의 mod (M) 잔여류 개수 차이가 최대 1이지만

\[
\frac1N\sum_{j\le N}\exp(2\pi i d_j/q_j)\longrightarrow1
\]

이다. 따라서 모든 고정 모듈러스에서의 지수 균등분포만으로 성장하는 소수 모듈러스의 위상 상쇄를 도출할 수 없다.

### B–E. 구성, 증명, 반례 감사

(q_j)를 (q_{j-1})과 (j^3)보다 큰 최소 소수로 재귀 정의하고 (d_j=j)로 둔다. 소수의 무한성으로 정의가 가능하다. 연속 정수의 고정 mod (M) prefix 개수 차이는 항상 최대 1이다.

현 길이 부등식과 (pi<4)로

\[
\left|e^{2\pi i j/q_j}-1\right|<\frac{8j}{q_j}<\frac8{j^2}.
\]

또한

\[
\sum_{j\ge1}\frac1{j^2}\le1+\sum_{j\ge2}\frac1{j(j-1)}=2
\]

이므로 정규화 편차는 (16/N) 이하이고 0으로 간다. 폐기 대상 함의의 모든 전제를 만족하면서 결론은 선형 규모로 실패한다.

이 반례군은 실제 canonical Fermat quotient 지수를 사용하지 않는다. 따라서 고정 모듈러스 정보만의 일반 추론을 막지만 canonical 수열의 특수 산술 정리를 막지는 않는다.

### F–H. 재현 계산과 유한 경계

소수 차수 64개와 정확한 유리수 envelope를 구성하고 (M=2,\ldots,16)을 검사한다. 점근 결론은 기호적 증명이며 유한 행은 재현용이다. 복소 부동소수점 근은 계산하지 않는다.

### I–K. 분류, 간극, 다음 보조정리

- 분류: `exact_no_go`.
- 정확 반례: 모든 고정 모듈러스 균등분포와 정규화 위상합의 1 수렴이 공존한다.
- 폐기 경로: 고정 모듈러스 지수 통계만으로 상쇄를 도출하는 방법.
- 최소 간극: canonical Fermat quotient의 가변 모듈러스 각도 분포 정리.
- 다음 단일 보조정리: `CanonicalFermatQuotientAngularDiscrepancyTendsToZero`.

## 3. 강한 골드바흐 추측

### A. 정확한 명제

`Q3CompatibleFamilyPrimeRaceEquivalence`.

모든 정수 (ell\ge0)에 대해

\[
q=3,\qquad m=12\ell+6,\qquad A=3^{6\ell+2}
\]

로 둔다. ((1-X)^m\bmod(X^3-1))의 순환계수는

\[
(c_0,c_1,c_2)=(-2A,A,A)
\]

이고, 유일한 호환 강제 prefix 벡터는

\[
(1,1+3A,1+3A)
\]

이며 길이는 (T_\ell=6A+3)이다. 이 벡터가 처음 (T_\ell)개 소수의 잔여벡터와 같은 것은 정확히

\[
\Delta_3(T_\ell):=N_1(T_\ell)-N_2(T_\ell)=0
\]

일 때뿐이다.

### B–E. 증명과 경계 감사

원시 세제곱근 (zeta)에 대해 root-of-unity filter의 (1) 항은 0이다. (m=12\ell+6)이므로

\[
(1-\zeta)^m=(1-\bar\zeta)^m=-3^{m/2}.
\]

Fourier 역변환으로 (c_0=-2\cdot3^{m/2-1}=-2A), (c_1=c_2=A)를 얻는다. 강제 이동량은 (t=1-c_0=1+2A)이므로 벡터와 길이 공식이 따른다.

각 prefix에서 3으로 나누어지는 소수는 3 하나뿐이다. 따라서 실제 벡터의 0번 성분은 1이고, 나머지 두 성분이 강제 벡터와 같은 것과 두 잔여류 개수가 동률인 것은 동치다. 경험적 prime-race 편향을 가정하지 않았다.

### F–H. 재현 계산과 유한 경계

정수 quotient-state 조합 체와 독립 direct segmented sieve가 다음에 일치한다.

| \(\ell\) | \(m\) | \(T_\ell\) | 마지막 소수 | 실제 \((N_0,N_1,N_2)\) | \(\Delta_3\) |
|---:|---:|---:|---:|---:|---:|
| 0 | 6 | 57 | 269 | (1, 25, 31) | -6 |
| 1 | 18 | 39,369 | 471,749 | (1, 19,663, 19,705) | -42 |
| 2 | 30 | 28,697,817 | 547,035,959 | (1, 14,347,849, 14,349,967) | -2,118 |

세 비소멸 값은 유한 certificate일 뿐 모든 (ell)의 비소멸을 뜻하지 않는다.

### I–K. 분류, 간극, 다음 보조정리

- 분류: `partial_theorem`.
- 새 사실: 전체 (q=3) 호환 무한족이 정확히 하나의 스칼라 소수경주 문제로 환원된다.
- 폐기 경로: 이 족에도 고차원 odd-character detector 전체가 필요하다는 경로.
- 최소 간극: 특수 지수 (6\cdot3^{6\ell+2}+3)에서 동률이 없음을 증명해야 한다.
- 다음 단일 보조정리: `Q3SpecialPrimeRaceNeverTiesAtSixTimesPowerOfThreePlusThree`.

## 4. 쌍둥이 소수 추측 — deep focus

### A. 정확한 명제

`SecondOrderDenominatorCongruenceAnd256ConvergentCertificate`.

정수 (u,v), (v\ge2), (arepsilon\in\{-1,1\})에 대해

\[
B_1(u,v)=\varepsilon
\]

이면

\[
u^{17}\equiv\varepsilon\pmod v
\]

이고 더 강하게

\[
u^{17}+17u^{16}v\equiv\varepsilon\pmod {v^2}
\]

이다. TICKET-258에서 분리한 유일 실근의 처음 256개 인증 연분수 수렴분수는 두 부호 모두 두 번째 조건을 통과하지 못한다.

### B–E. 증명, 반례, 적대적 감사

정확한 형식은 어떤 정수계수 다항식 (R)에 대해

\[
B_1(u,v)=u^{17}+17u^{16}v+v^2R(u,v)
\]

로 시작한다. mod (v), mod (v^2)로 줄이면 두 필요조건이 증명된다. 역은 주장하지 않는다. 합동조건 통과는 Thue 방정식의 해라는 뜻이 아니다.

약한 1차 조건은 실제로 불충분하다. 검사한 비자명 수렴분수 중

\[
(u,v,\varepsilon)=(-1,13,-1),\quad(-1,14,-1)
\]

이 이를 통과하지만 정확한 형식값은 각각

\[
-95516898540708139236,
\qquad
168149422466766035245
\]

이다. 둘 다 mod (v^2)에서 탈락한다. 이는 1차 필터의 완전성에 대한 정확한 반례이지 쌍둥이 소수 추측의 반례가 아니다.

각 수렴분수와 두 부호에 대해 모듈러 거듭제곱 결과를 전체 정수 (B_1(u,v)mod v^2)와 독립 대조했다. 분모 1인 두 수렴분수는 직접 검사했다. proof DAG는 TICKET-258의 “모든 unit-coefficient 해는 수렴분수” 정리를 사용하지만 처음 256개가 전부라고 가정하지 않는다.

### F–H. 재현 계산과 유한 경계

처음 256개 인증 수렴분수, 최대 121자리 분모까지 검사했다. 1차 통과는 2개, 2차 통과는 0개다. 이 결과는 유한 prefix만 배제한다. 뒤의 무한히 많은 수렴분수에 대한 귀납이나 주기성은 증명되지 않았다.

### I–K. 분류, 간극, 다음 보조정리

- 분류: `partial_theorem`.
- 새 사실: 제한 없는 가변 분모 mod (v^2) 필요조건과 256개 수렴분수 certificate.
- 폐기 경로: 1차 분모 합동만으로 완전 배제하는 방법. 위 두 반례가 이를 정확히 막는다.
- 최소 간극: 모든 이후 수렴분수에서 2차 조건을 배제해야 한다.
- 다음 단일 보조정리: `NoUniqueRootConvergentSatisfiesSecondOrderDenominatorCongruence`.

## 재현 계약

```powershell
python scripts/ticket260_weighted_equidistribution_primerace_variablemod.py
python -m unittest tests.test_ticket260_weighted_equidistribution_primerace_variablemod
python scripts/verify_ticket260_structure.py
```

- 산술: 증명 의존 계산은 정수와 `Fraction`만 사용한다.
- random seed: 없음. 모든 알고리즘은 결정적이다.
- 정확 사례: RH 16행, Collatz 위상 64개와 고정 모듈러스 15개, Goldbach prefix 3개와 독립 알고리즘 2개, Twin 수렴분수 256개와 각 두 부호.
- 실패 수: 커밋된 certificate에서 0.
- 주장 경계: `iteration_complete`는 산출물의 일치를 뜻할 뿐 상위 추측의 해결을 뜻하지 않는다.

