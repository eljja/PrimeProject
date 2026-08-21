# TICKET-235 [parent conjecture claims blocked · open_not_proven]: Schur 보완, 소수 거듭제곱 결손, 위상 복원, CRT overlap

## 주장 상태

**미해결(`open_not_proven`)**. 이번 티켓은 정확한 부분정리 또는 no-go 정리
네 개를 증명했지만 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측 중 어느 것도 해결하지 않았다. 기계 판독 해결 수는 `0 / 4`다.

2026-08-21 현재 외부 상태는 [Clay 리만 가설
페이지](https://www.claymath.org/millennium/Riemann-Hypothesis/), 최신
[Collatz 검증 알고리즘](https://arxiv.org/abs/2602.10466)과
[실시간 검증 기록](https://pcbarina.fit.vut.cz/), 최근
[Goldbach exceptional-set 연구](https://arxiv.org/abs/2607.27282),
[Maynard의 bounded-gap 정리](https://annals.math.princeton.edu/2015/181-1/p07)로
확인했다. 이는 연구 전선을 확인하는 출처일 뿐 네 추측의 증명으로 사용하지
않는다.

## 재현 계약

- 생성기: `scripts/ticket235_schur_primepower_phase_overlap.py`
- 테스트: `tests/test_ticket235_schur_primepower_phase_overlap.py`
- 통합 JSON: `data/open-problem/ticket235-schur-primepower-phase-overlap.json`
- 정확한 새 부분/no-go 정리: `4`
- 폐기한 경로군: `4`
- 해결된 상위 추측: `0`
- 기계 실패: `0`

모든 유리수 인증은 Python 정수와 `Fraction`으로 생성한다. 유한 계산은
전 매개변수 논증의 exact 사례를 검산할 뿐 점근 정리를 대신하지 않는다.

## 1. 리만 가설 트랙

### 이번에 선언한 정확 명제

`ExactKernelSchurComplementCriterionAndCrossBlockNoGo`.

TICKET-234 Weil 형식의 유한 절단을 `K=ker(G)`와 `R=K`의 직교여공간에
대해

\[
H=G+E=\begin{pmatrix}A&B\\B^*&C\end{pmatrix},\qquad A>0
\]

로 쓰면 정확히

\[
H\ge0\iff C-B^*A^{-1}B\ge0
\]

이다. 영공간 압축 `C>0`와 절대적 `B=o(1)`만으로는 충분하지 않다.

\[
G=\operatorname{diag}(I_M,0_d),\quad C=T^{-2}I_d,
\quad B=(2/T)e_1f_1^*
\]

이면 `C>0`이고 `B`의 모든 성분이 0으로 가지만 Schur 최소 고윳값은
`-3/T^2`다.

### 증명과 exact 계산

완전제곱을 만들면

\[
\langle H(r,k),(r,k)\rangle
=\langle A(r+A^{-1}Bk),r+A^{-1}Bk\rangle
+\langle(C-B^*A^{-1}B)k,k\rangle
\]

이므로 양방향 동치가 나온다. 같은 `C=T^(-2)I`에 교차항을 `1/(2T)`로
바꾸면 Schur 값이 `3/(4T^2)>0`이 된다. 즉 필요한 것은 단순한 절대
소량성이 아니라 영공간 양성 scale에 상대적인 제어다.

| `T` | `M` | 영공간 차원 | 반례 Schur 값 | 안전 Schur 값 |
|---:|---:|---:|---:|---:|
| 64 | 39 | 25 | `-3/4096` | `3/16384` |
| 256 | 50 | 206 | `-3/65536` | `3/262144` |
| 1024 | 61 | 963 | `-3/1048576` | `3/4194304` |
| 4096 | 73 | 4023 | `-3/16777216` | `3/67108864` |

**폐기한 경로.** 영공간 압축의 양성과 교차 블록의 절대적 entrywise 또는
operator-norm 소량성만으로 Weil 양성을 이전하는 경로.

**논리적 한계.** 이 행렬은 실제 Guinand--Weil 산술 tail이 아니라 추상
Hermitian 절단이다. zeta 영점을 계산하지 않았고 산술 상대 form bound도
증명하지 않았다.

**다음 단일 보조정리.**
`ArithmeticWeilTailRelativeCrossBlockSchurDominanceOnCofinalLogarithmicFrames`.

## 2. 콜라츠 트랙

### 이번에 선언한 정확 명제

`BinaryRunBlockPrimitiveDivisorOrderCharacterizationAndSelectionNoGo`.

valuation word `a=(a_0,...,a_(h-1))`에 대해

\[
D=2^{\sum a_i}-3^h,qquad
B=\sum_{j=0}^{h-1}3^{h-1-j}2^{\sum_{i<j}a_i}
\]

라 하자. **계보 교정:** 일반 valuation word를 소수 존재 여부만으로 배제하는
전략의 불완전성은 이미 TICKET-224가 증명했다. 그 primitive witness

\[
a=(1,1,2,4,3)
\]

에 대해

\[
D=1805=5\cdot19^2,qquad B=475=5^2\cdot19
\]

에서는 `rad(D)=95`가 `B`를 나누지만 `D`는 `B`를 나누지 않는다. 이는
`already_closed_regression_only`로 유지하며 TICKET-235의 새 결과로 세지 않는다.

TICKET-235의 새 정리는 binary frontier의 다음 order 특성화다.
`w_k=1^k2^(2k)`이면

\[
D_k=32^k-27^k,qquad B_k=32^k+27^k-2\cdot18^k
\]

이고, `q`가 6을 나누지 않는 소수일 때

\[
q\mid\gcd(D_k,B_k)
\iff \operatorname{ord}_q(3/2)\mid k
\text{ 이고 }\operatorname{ord}_q(4)\mid k.
\]

`k=14,q=29`에서는 `ord_29(32/27)=14`이므로 `q`가 `D_14`의 primitive
divisor지만, 나머지 order가 `7,14`라 `B_14`도 나눈다. 따라서 임의의
primitive divisor 하나를 택하는 것은 인증이 아니다.

### 증명과 exact 계산

첫 반례는 정수 인수분해로 끝난다. 두 번째는 `B_k-D_k=0 (mod q)`에서
`(3/2)^k=1`을 얻고, `32/27=4(3/2)^(-3)`를 `D_k=0`에 대입해 `4^k=1`을
얻는다. 역방향도 같은 식을 거꾸로 적용하면 된다.

`{1,2,3,4,5}` alphabet, 높이 `2..8`, `D>1`의 canonical primitive
necklace scan은 확장된 계보 회귀 검사다.

| canonical word | primitive necklace | `rad(D)|B`, `D∤B` |
|---:|---:|---:|
| 63,426 | 63,185 | 1 |

유일한 행은 이미 알려진 TICKET-224 witness다. 새 order 감사에서는
`q<=5000`, `13<=k<=256`을 검사해 order 동치 실패
0, `D_k`의 primitive divisor이면서 `B_k`도 나누는 행 56개를 얻었다.

**폐기한 경로.** 이미 닫힌 TICKET-224 radical 표적을 새 open node로 다시
공격하는 것, binary density band에서 임의 primitive divisor를 택하는 경로.

**논리적·유한 계산 한계.** 첫 반례는 valuation `3,4`를 포함하므로 기존
순수 `{1,2}` adaptive-radical 보조정리를 반증하지 않는다. `q=29`도 다른
order-separated 소수의 존재를 막지 않는다. 무한 word, 일반 valuation,
aperiodic 거동은 남아 있다.

**다음 단일 보조정리.**
`UniformBinaryDensityBandOrderSeparatedAdaptivePrimeWitness`.

## 3. 강한 골드바흐 트랙

### 이번에 선언한 정확 명제

`CompleteMarginalPowerSpectrumPhaseRetrievalNoGo`.

완전한 주변 Fourier power조차 target-reflected cross coefficient를 결정하지
못한다. 모든 홀수 `q>=5`에 대해 `Z/qZ` 위에서

\[
x=1_{\{0,1\}},\quad y_0=1_{\{0,-1\}},\quad y_2=1_{\{1,2\}}
\]

라 하자. `y_2`는 `y_0`의 평행이동이므로 full autocorrelation과 모든
Fourier power가 같다.

\[
|\widehat y_0(a)|^2=|\widehat y_2(a)|^2
\]

이지만

\[
(x*y_0)(0)=2,qquad (x*y_2)(0)=0.
\]

### 증명과 exact 계산

평행이동은 Fourier 변환에 절댓값 1인 위상만 곱하므로 power를 보존한다.
반면 target 0 convolution은 `sum_t x(t)y(-t)`다. `y_0`에서는 `t=0,1`이
모두 기여하고 `y_2`에서는 둘 다 기여하지 않는다.

`5<=q<=101`의 소수 24개를 exact integer cyclic autocorrelation으로 검사해
모든 주변 좌표가 일치하고 target 값은 항상 `2,0`임을 확인했다.

**폐기한 경로.** 별도의 완전한 marginal power spectrum, shell energy,
autocorrelation만으로 TICKET-234의 reflected low-high coherence를 복원하는
경로.

**논리적·유한 계산 한계.** 두 점 측도는 실제 소수 가중치가 아니다.
`p+(N-p)=N`을 사용하는 joint arithmetic phase 추정을 반증하지 않으며
Goldbach 반례도 아니다.

**다음 단일 보조정리.**
`ActualPrimeReflectedCrossSpectrumPhaseLockingAtInverseLogScale`.

## 4. 쌍둥이 소수 트랙

### 이번에 선언한 정확 명제

`FixedDegreeCesaroOverlapMomentReductionAndDegreeOneNoGo`.

centered normalized CRT 좌표에 대해

\[
b_S=\mathbb E_\nu\prod_{i\in S}\psi_i,qquad
E_{m,k}={1\over{m\choose k}}\sum_{|S|=k}b_S^2
\]

라 하자. 독립인 `X,Y~nu`, `z_i=psi_i(X)psi_i(Y)`,
`R_m=m^(-1)sum_i z_i`를 잡으면

\[
E_{m,k}=\mathbb E{e_k(z_1,\ldots,z_m)\over{m\choose k}}
\]

가 정확히 성립하고

\[
|E_{m,k}-\mathbb E R_m^k|
\le2^{k+1}\left(1-{(m)_k\over m^k}\right)
\le{2^kk(k-1)\over m}
\]

이다. 그러나 degree 1만으로는 충분하지 않다. Rademacher product 공간의

\[
\nu={1\over2}\delta_{(+1,\ldots,+1)}
+{1\over2}\delta_{(-1,\ldots,-1)}
\]

에서는 모든 singleton coefficient가 0이고 모든 pair coefficient가 1이다.
즉 모든 `m`에서 `E_(m,1)=0`, `E_(m,2)=1`이다.

### 증명과 exact 계산

두 독립 표본으로 `b_S^2`를 전개하고 모든 `k`-subset을 평균하면 elementary
symmetric 항등식이 된다. `R_m^k`는 좌표를 복원추출하고 Cesaro 식은
비복원추출한다. 중복 확률 `1-(m)_k/m^k`와 각 곱의 절댓값 상계 `2^k`가
오차식을 준다.

`X=10,000` 아래 twin start 202개와 CRT 소수 `(5,7,11,13)`에 조건화한
exact 진단에서 네 차수의 Cesaro energy와 elementary overlap moment가
각각 정확히 일치했다.

| 차수 | exact 공통값 |
|---:|---:|
| 1 | `3257/1958592` |
| 2 | `9265/5875776` |
| 3 | `6301/3917184` |
| 4 | `9/81608` |

**폐기한 경로.** degree-one Cesaro 소멸 또는 평균 pair overlap만으로 모든
고정 차수를 제어하는 경로.

**논리적·유한 계산 한계.** Rademacher 혼합은 소수 가중치가 아니다. 실제
twin-start 행은 이미 존재하는 쌍에 조건화하므로 무한성 문제에는 순환적인
유한 진단일 뿐이다. Type-II overlap concentration, parity 이전, 양의 주항은
모두 남아 있다.

**다음 단일 보조정리.**
`PrimeWeightedCRTPairOverlapMomentConcentrationAtTwinScale`.

## Proof DAG와 최종 경계

각 기계 판독 DAG에는 `closed` TICKET-235 노드 하나, 범위가 명시된
`refuted_or_limited` 노드 하나, `highest_risk_open` 후속 보조정리 하나,
`open_not_proven` 상위 추측이 있다. 정확한 노드와 edge는 통합 JSON이
권위 자료다.

이번 결과는 구조적 환원과 인증된 no-go 정리다. 네 추측 중 어느 것의
증명이나 반증도 아니다.
