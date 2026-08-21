# TICKET-234: 연산자 영공간, 이진 sieve 거짓양성, Goldbach half-channel, Poisson CRT noise

## 주장 상태

**미해결(`open_not_proven`)**. 이번 티켓은 정확한 부분정리·동치정리·no-go
정리 네 개를 증명했지만, 리만 가설·콜라츠 추측·강한 골드바흐 추측·쌍둥이
소수 추측 중 어느 것도 해결하지 않았다. 기계 판독 해결 수는 `0 / 4`다.

2026-08-21 현재 외부 상태는
[Clay 미해결 Millennium 목록](https://www.claymath.org/problem/unsolved/),
[2026 Collatz 유한 검증 알고리즘](https://arxiv.org/abs/2602.10466),
[최근 Goldbach exceptional-set/major-arc 연구](https://arxiv.org/abs/2607.27282),
[Thorner--Zaman Siegel--Walfisz 정리](https://arxiv.org/abs/2108.10878),
[Maynard의 작은 소수 간격 정리](https://annals.math.princeton.edu/2015/181-1/p07)로
확인했다. 외부 정리는 아래에서 명시한 곳에만 사용한다.

## 재현 계약

- 생성기: `scripts/ticket234_operator_kernel_density_minor_cesaro.py`
- 테스트: `tests/test_ticket234_operator_kernel_density_minor_cesaro.py`
- 통합 JSON: `data/open-problem/ticket234-operator-kernel-density-minor-cesaro.json`
- 정확한 새 정리: `4`
- 폐기된 경로군: `4`
- 해결된 상위 추측: `0`
- 기계 실패: `0`

## 1. 리만 가설 트랙

### 이번에 선언한 정확 명제

`ScalarDiagonalFrameRankAndSignedTailTransferNoGo`.

TICKET-233의 `M x T` dilation 분석행렬을

\[
V_{j,n}=\sqrt{w_j/W}(1-e^{-in\theta_j})
\]

라 하자. `T>M`이면 `rank(V)<=M`이므로 Gram 형식 `G=V*V`에는 0이
아닌 영벡터가 존재한다. 이는 모든 대각 에너지 `G_nn`이 1 이상이어도
마찬가지다. 단위 영벡터 `u`와 임의의 `epsilon>0`에 대해

\[
H_\varepsilon=G-\varepsilon uu^*
\]

를 잡으면 tail의 연산자 norm은 `epsilon`, 모든 성분의 절댓값도
`epsilon` 이하이지만

\[
u^*H_\varepsilon u=-\varepsilon<0.
\]

따라서 각 순수 주파수의 scalar floor만으로 signed Guinand--Weil 이차형의
양성을 이전할 수 없다.

### 논증과 exact 계산

핵심은 rank-nullity다. `M=ceil(8 log(2T))<T`는 `T=35`부터 성립한다.
유리 위상 표본에는 더 명시적인 영다항식도 있다. 서로 다른 비자명 위상근
집합을 `Z`라 하면

\[
C(x)=x(x-1)\prod_{z\in Z}(x-z)=\sum_{n\ge1}c_nx^n
\]

이고

\[
\sum_nc_n(1-z_j^n)=C(1)-C(z_j)=0.
\]

이를 primitive `P`차 단위근이 있는 보조 유한체로 내린 exact-int 감사에서
모든 residual이 0이었다.

| `T` | `M` | 영공간 차원 하한 | 보조 소수 | 영다항식 차수 |
|---:|---:|---:|---:|---:|
| 64 | 39 | 25 | 269 | 34 |
| 256 | 50 | 206 | 1543 | 51 |
| 1024 | 61 | 963 | 2063 | 61 |
| 4096 | 73 | 4023 | 73783 | 75 |

**폐기한 경로.** scalar 대각 floor와 tail 크기만으로 full Weil 양성을 얻는
이전.

**논리적 한계.** 음의 rank-one tail은 실제 산술 Weil tail이 아니라 추상
Hermitian 반례다. 실제 tail이 영공간에서 특별한 부호·정렬을 가질 가능성은
남아 있다. zeta 영점에 대한 유한 계산도 아니다.

**다음 단일 보조정리.**
`ArithmeticWeilTailKernelCompatibilityAndPositiveSchurComplement`.

## 2. 콜라츠 트랙

### 이번에 선언한 정확 명제

`UniformBinaryDensityBandFixedFiniteAffineSieveNoGo`.

임의의 `K>=13`과 `gcd(M,6)=1`인 유한 비공집합 모듈러스족을 고정하자.
그러면 무한히 많은 `k>=K`에 대해

\[
w_k=1^k2^{2k}
\]

및 모든 순환 회전은 primitive 이진 density-band word이고, 모든 고정
검사에서 `M|D`와 `M|B`를 동시에 통과하지만 실제로는 `D`가 `B`를 나누지
않는다.

### 증명과 exact-int 감사

`Z/MZ` 위 affine permutation

\[
F_a(x)=2^{-a}(3x+1),\quad a\in\{1,2\}
\]

의 order를 `r_1,r_2`라 하자. 모든 모듈러스에 대한 이 order들의 공배수의
충분히 큰 배수 `k`를 택하면

\[
F_{w_k}=F_2^{2k}\circ F_1^k=\mathrm{id}.
\]

일반 반복식 `F_a(x)=2^{-S}(3^hx+B)`에서 곧 모든 고정 `M`이 `D,B`를
나눈다. 그러나 TICKET-197 닫힌식은

\[
D_k=32^k-27^k,
\qquad
B_k=32^k+27^k-2\cdot18^k,
\]

\[
B_k-D_k=2\cdot9^k(3^k-2^k)
\]

를 준다. `gcd(D_k,18)=1`이므로 `D_k|B_k`라면
`D_k|(3^k-2^k)`여야 한다. 하지만

\[
0<3^k-2^k<5\cdot27^{k-1}\le D_k
\]

라서 불가능하다. 두 cyclic transition만 있으므로 word는 primitive이고,
`216<250`, `27<32`에서 density band 안이다. 회전식
`2^(a_0)B'=3B+D`가 모든 회전에 결론을 이전한다.

`5<=M<200`의 대상 66개를 exact-int로 검사해 실패 0, 최대 기본 `k=198`을
얻었다. `(5,7)`, `(5,7,11)`, `(5,7,11,13)` 동시 모듈러스도 실패가 없었다.
별도 factor scan은 높이 22까지 raw word `1,893,010`개, primitive necklace
`90,272`개에서 `rad(D)|B`이지만 `D∤B`인 이진 반례를 찾지 못했다.

**폐기한 경로.** 고정된 유한 affine modulus 또는 고정 유한 prime-power
sieve를 cofinal 증명으로 승격하는 전략.

**논리적·유한 계산 한계.** word에 따라 커지는 adaptive prime/modulus는
폐기되지 않았다. radical scan은 현재 `k>=13` frontier에 도달하지 않는다.
valuation 3 이상과 aperiodic 발산도 남아 있다.

**다음 단일 보조정리.** `UniformBinaryDensityBandAdaptiveRadicalDeficit`:
모든 남은 primitive 이진 후보에는 `q|D`, `q∤B`인 word-adaptive 소수 `q`가
존재한다.

## 3. 강한 골드바흐 트랙

### 이번에 선언한 정확 명제

`MinorArcMarginGoldbachEquivalenceAndPrimeHalfChannelCancellationNoGo`.

\[
S_N(\alpha)=\sum_{p\le N}\log p\,e(p\alpha),
\quad
G_\theta(N)=\int_0^1S_N(\alpha)^2e(-N\alpha)d\alpha
\]

라 하자. 임의의 대칭 major/minor 분할에서 major 실수부 `M_N>0`이면

\[
m_N>-M_N\iff G_\theta(N)>0.
\]

즉 TICKET-233의 “모든 target에 대한 strict full minor margin”은 약한
보조정리가 아니라 weighted Goldbach endpoint 자체와 동치다.

더 구조적인 exact no-go도 성립한다. 소수합을 `N/2` 아래 `L_N`, 위
`U_N`, 중앙항으로 나누면

\[
[e(N\alpha)]L_N^2=[e(N\alpha)]U_N^2=0.
\]

반면 중앙 호 `||alpha||<=1/(4N)`에서 kernel은

\[
K_N(d)=\frac{\sin(\pi d/(2N))}{\pi d}
\]

이고 same-half offset에 대해 `K_N(d)>=1/(pi N)`이다. 따라서

\[
M_{LL}\ge {W_L^2\over\pi N},\qquad
M_{UU}\ge {W_U^2\over\pi N}.
\]

전체 target coefficient가 0이므로 각각의 minor는 정확히 `-M_LL,-M_UU`다.
PNT에 의해 크기는 각각 `-(1/(4*pi)+o(1))N` 이하이다.

상반부를 target에 관해 반사한 `V_N`을 쓰면

\[
G_\theta(N)=2\langle L_N,V_N\rangle
+1_{N/2\ \mathrm{prime}}\log^2(N/2).
\]

따라서 실제 정보는 marginal shell이나 norm이 아니라 low prime과 reflected
high prime 사이의 target-dependent joint phase다. 두 half-channel 모두
Siegel--Walfisz를 `N,N/2`에 적용해 TICKET-233 polylog rational-center
점근식을 만족하지만, same-half minor는 major를 정확히 상쇄한다.

| `N` | 중앙 `LL` | 중앙 `UU` | 중앙 `LU` | full reflection cross |
|---:|---:|---:|---:|---:|
| 100 | 7.550355 | 8.210933 | 8.627483 | 73.090775 |
| 1000 | 100.463917 | 102.698832 | 112.386938 | 911.522295 |
| 10000 | 1070.810337 | 1099.953125 | 1203.390134 | 8371.568403 |

**폐기한 경로.** strict full minor margin을 더 약한 lemma로 취급하는 것,
rational-center 또는 dyadic square-channel norm에서 targetwise minor 부호를
자동 이전하는 것.

**논리적·유한 계산 한계.** 올바르게 결합된 full-prime minor 추정은 반증하지
않았다. 표의 로그·삼각함수 적분은 부동소수 감사이며, exact한 부분은 Fourier
직교에 의한 상쇄다. inverse-log cross coherence는 미증명이다.

**다음 단일 보조정리.**
`ComplementaryHalfPrimeReflectionMinorCoherenceAtInverseLogScale`.

## 4. 쌍둥이 소수 트랙

### 이번에 선언한 정확 명제

`PoissonizedFixedDegreeCesaroCriterionAndMovingPrimeNoGo`.

TICKET-233의 centered quadratic CRT 계수에 대해

\[
E_{m,k}={1\over{m\choose k}}\sum_{|S|=k}|b_{m,S}|^2,
\qquad
D_m=\sum_{S\ne\varnothing}m^{-|S|}|b_{m,S}|^2
\]

라 하자. probability measure 또는 total variation 1 이하 signed measure에서

\[
D_m\to0\iff E_{m,k}\to0\quad(\text{모든 고정 }k).
\]

차수별로 묶으면 weight는 `{m choose k}m^(-k)`이고 `1/k!`로 수렴한다.
또 `E_(m,k)<=2^k`라서 `2^k/k!` dominated convergence가 양방향을 증명한다.
좌표를 확률 `1/(m+1)`로 고르는 exact 표현에서 차수는 `Poisson(1)`로
수렴한다.

고정 label별 coefficient 소멸은 충분하지 않다. 뒤쪽 절반 좌표의 밀도

\[
g_m=\prod_{i>\lfloor m/2\rfloor}(1+\psi_i/2)
\]

는 양수·정규화되고 모든 고정 label 계수가 결국 0이지만

\[
D_m=\left(1+{1\over4m}\right)^{\lceil m/2\rceil}-1
\to e^{1/8}-1>0.
\]

`m=4,8,16,32`의 exact 값은 `33/256`에서 `0.132598...`로 수렴했다. 실제
twin start에 조건화한 별도 exact rational 감사에서는 `X=10^4,m=4`에서
`12301/5222912`, `X=10^5,m=6,8`에서 각각 `0.000612907...`,
`0.000560975...`를 얻었다.

**폐기한 경로.** 모든 고정 labelled CRT coefficient의 pointwise 소멸만으로
critical noise 소멸을 결론내리는 것.

**논리적·유한 계산 한계.** moving-half는 실제 prime weight가 아니다. 유한
twin 감사는 이미 존재하는 twin start에 조건화됐으며 점근 증명이 아니다.
critical noise가 닫혀도 parity-retaining transfer와 양의 principal mass가
남는다.

**다음 단일 보조정리.**
`PrimeWeightedFixedDegreeCesaroCRTCorrelationDecayAtTwinScale`.

## 통합 proof DAG

```text
RH-T233 -> RH-T234 -> RH-N234 [폐기]
                   -> RH-OPEN234 -> RH [미해결]

CO-T197 + CO-T223 + CO-T233 -> CO-T234 -> CO-N234 [폐기]
                                         -> CO-OPEN234 -> periodic/aperiodic gap -> CO [미해결]

GB-T233 + PNT -> GB-T234 -> GB-N234 [폐기]
                           -> GB-OPEN234 -> GB [미해결]

TP-T233 -> TP-T234 -> TP-N234 [폐기]
                   -> TP-OPEN234 -> parity/principal-mass gap -> TP [미해결]
```

## 최종 경계

이번 결과는 네 접근의 잘못된 양화사와 구조적 간극을 더 좁혔다. 어느 상위
추측도 증명·반증하지 않았다. 유한 계산은 표시한 항등식과 반례 모형의 재현
감사일 뿐이며, 계산 범위를 넘는 결론은 본문에서 증명한 대수·점근 논증에만
근거한다.
