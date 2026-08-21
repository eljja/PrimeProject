# TICKET-233: 로그 프레임, Collatz 12-one 층, squarefree Goldbach shell, CRT 엔트로피

## 주장 상태

**미해결, 증명되지 않음.** 이번 티켓은 정확한 부분정리·점근정리·no-go
정리 네 개를 확정하지만, 리만 가설·콜라츠 추측·강한 골드바흐 추측·
쌍둥이 소수 추측 중 어느 것도 해결하지 않는다. 기계 판독 해결 수는
`0 / 4`다.

2026-08-21 현재 외부 상태는
[Clay 미해결 Millennium 문제 목록](https://www.claymath.org/problem/unsolved/),
[최신 Collatz 유한 검증 알고리즘](https://arxiv.org/abs/2602.10466),
[Goldbach exceptional set 및 major arc 연구](https://arxiv.org/abs/2607.27282),
[Thorner--Zaman의 Siegel--Walfisz 입력](https://arxiv.org/abs/2108.10878),
[Maynard의 bounded-gap 정리](https://annals.math.princeton.edu/2015/181-1/p07)로
확인했다. 외부 정리는 아래에서 명시한 곳에만 사용한다.

## 재현 계약

- 생성기: `scripts/ticket233_logarithmic_frame_density_shell_entropy.py`
- 테스트: `tests/test_ticket233_logarithmic_frame_density_shell_entropy.py`
- 통합 JSON: `data/open-problem/ticket233-logarithmic-frame-density-shell-entropy.json`
- 확정 부분/점근/no-go 정리: `4`
- 정정 또는 폐기 경로: `4`
- 해결한 원 추측: `0`
- 기계 검증 실패: `0`

## 1. 리만 가설 트랙

### 이번에 증명할 정확한 명제

`LogarithmicAdaptiveScalarFrameExistenceAndSharpDimensionThreshold`.
정수 `T>=2`, 소수 `P>T`,

\[
M=\lceil8\log(2T)\rceil
\]

에 대해 모든 `1<=n<=T`에서 동시에

\[
{1\over M}\sum_{j=1}^M|1-e^{-2\pi i n r_j/P}|^2\ge1
\]

을 만족하는 법 `P` 잉여 `r_1,...,r_M`이 존재한다. 영 잉여의 실수
대표를 `1`로 바꾸고 `q_j=exp(2*pi*alpha_j)>1`로 두면 좌표
`O(log T)`인 적응형 scalar dilation frame을 얻는다. TICKET-232의
`Omega(log T)` 하한과 합치면 스칼라 유효 차원 문턱은 `Theta(log T)`다.

### 논증과 계산

`r_j`를 독립 균등하게 고른다. `P>T`이므로 고정된 `n`을 곱하는 것은
잉여류의 순열이고,

\[
X_j=|1-e^{-2\pi i n r_j/P}|^2\in[0,4],\qquad E X_j=2.
\]

Hoeffding 부등식과 `T`개 진동수의 union bound는 실패확률을
`T exp(-M/8)<=1/2`로 제한한다. 따라서 공통 프레임이 존재한다. 생성기는
`T=16,64,256,1024,4096`의 고정 seed 예시도 모두 최소 에너지 `>=1`로
검산한다.

**폐기한 경로:** scalar phase energy에 초로그 차원이 반드시 필요하다는
주장.

**논리/유한 계산 한계:** seed 행은 존재정리의 구현 검산일 뿐이다. signed
Guinand--Weil 이차형으로의 이전과 산술 tail 지배는 증명하지 않았다.

**다음 단일 보조정리:**
`LogarithmicAdaptiveScalarFrameToWeilKernelTransferWithExplicitSignedTailDominance`.

## 2. 콜라츠 추측 트랙

### 이번에 증명할 정확한 명제

`BinaryLineageCorrectionTwelveOneExclusionAndFixedStratumNoGo`.
`a in {1,2}^h`, `k=#\{j:a_j=1\}`에 대해

\[
D=2^{2h-k}-3^h,
\qquad
B=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}}.
\]

TICKET-182에 의해 `D>0` 및 `D|B`는 양의 가속 주기의 실현과 동치다.
TICKET-232가 다음 문제로 둔 four-one 층은 이미 TICKET-188에서 닫혔고,
더 강한 arbitrary-tail 형태도 TICKET-209에서 닫혔다. 실제로
TICKETS 188--195가 이진 `4<=k<=11`을 모두 닫았다.

이번 티켓은 첫 실제 열린 이진 고정 층을 닫는다.

> valuation `1`이 정확히 12개이고 나머지가 모두 `2`인 양의 가속
> Collatz 주기는 없다.

따라서 가상의 이진 주기는 `k>=13`, 일반 valuation 주기는 기존
arbitrary-tail 계보에 의해 `k>=8`이어야 한다. 이진 후보는 primitive
necklace로 줄일 수 있고

\[
\log_2(6/5)\le k/h<2-\log_2 3
\]

을 만족해야 한다.

### 정확 증명과 계산

첫 `1`을 `p_0=0<p_1<...<p_11<h`로 회전 정규화한다. 이전 `1`의 개수를
세는 계단함수를 망원합하면 정확히

\[
B=C_h+\sum_{i=1}^{11}E_{i,h}(p_i)
\]

가 된다. `12<=h<=18`의 정규화 단어 `18,564`개 전부와 결정 범위의
고정 seed 표본 `2,176`개에서 직접 prefix 합과 비교해 불일치 `0`을
확인했다.

수축 `D>0`은 `h=29`부터 시작한다. 양의 주기의 필요조건

\[
1\le2^{12}(5/6)^h
\]

은 `h=45`에서는 성립하지만 `h=46`부터 실패하므로 `29<=h<=45`만 남는다.
11개 경계항을 `5+6`으로 분할하고 `p_5<p_6`일 때만 왼쪽 나머지를
활성화하여 오른쪽의 보수 나머지를 법 `D`에서 찾는다. Vandermonde
항등식으로 완전한 커버리지는

\[
\sum_{h=29}^{45}{h-1\choose11}
={45\choose12}-{28\choose12}=28,729,599,990
\]

이다. exact-integer MITM에서 나눗셈 hit는 `0`이며, 높이별 개수와
SHA-256 transcript를 JSON에 저장했다.

고정 층 반복 자체에는 엄밀한 no-go가 있다. 모든 `m>=1`에서 primitive
단어 `1^m2^(2m)`은 `(h,k)=(3m,m)`이고 `216<250`, `27<32` 때문에 밀도
띠 안에 있다. 소수 `k`에 대해 `h=3k` 층의 primitive necklace 수는

\[
({3k\choose k}-3)/(3k)
\]

이다. 따라서 회전 몫을 취해도 유한 fixed-`k` ladder는 cofinal하지 않다.
이는 uniform 해석적 정리의 가능성을 막는 결과는 아니다.

**폐기한 경로:** 이미 닫힌 four-one을 새 open node로 다시 공격하는 것,
유한 고정 multiplicity 열거를 cofinal 증명으로 승격하는 것.

**논리/유한 계산 한계:** `k=12` 전수 계산은 독립 부등식이 무한 문제를
`h=29..45`로 줄였기 때문에만 완전하다. `h<=22` 밀도 scan은 회귀 검증일
뿐이다. 이진 `k>=13`, valuation `>=3`, 비주기 발산은 남는다.

**다음 단일 보조정리:**
`UniformBinaryDensityBandPrimitiveNecklaceNondivisibility`.

## 3. 강한 골드바흐 추측 트랙

### 이번에 증명할 정확한 명제

`PolylogarithmicSquarefreePrimeShellAsymptoticAndSparseDenominatorNoGo`.
홀수 squarefree `q`의 reduced residue 질량을 `W_r`, 평균을
`mu=W/phi(q)`, 최대 상대 편차를
`epsilon=max|W_r-mu|/mu`라 하면 reduced rational shell은

\[
T_q(N)=\mu^2c_q(N)+R_q(N),
\]

\[
|R_q(N)|\le\mu^2(2\phi(q)^2\epsilon+\phi(q)^3\epsilon^2).
\]

따라서 log-prime 가중치와 고정 `B`에 대해, 모든 홀수 squarefree
`q<=(log X)^B`와 모든 `N`에서 균일하게

\[
T_{q,X}(N)=\mu^2c_q(N)+o_B(\mu^2)
=\mu^2c_q(N)(1+o_B(1)).
\]

### 논증, Parseval, no-go

squarefree `q`와 reduced `a`에서는 `c_q(a)=Mobius(q)`다. residue Fourier
합을 `mu*Mobius(q)+D_a`로 쓰면 `|D_a|<=phi(q)epsilon mu`이고, 제곱 전개와
합으로 결정론적 오차계를 얻는다. Siegel--Walfisz의
`epsilon=O_B(q exp(-c_B sqrt(log X)))`가 polylog 범위에 충분하다.

소수 분모 `l`에서는 정확히

\[
\sum_{n\bmod l}|R_l(n)|^2
=l\sum_{a=1}^{l-1}|S(a/l)^2-\mu^2|^2.
\]

따라서 energy `o(mu^4)`는 RMS/대부분 target만 주며, energy만으로 uniform
maximum 제어를 얻는 충분조건은 `o(mu^4/l)`이다. 필요조건이라고 주장하지
않는다.

무제약 분모 성장에는 실제 소수 counterfamily가 있다. `l>2X+1`인 소수를
고르고 `n=2X+1`, 짝수 `N=l+n`으로 두면 `p,q<=X`인 쌍은 목표 잉여에
도달하지 못해

\[
T_l(N)=-W^2,\qquad |R_l(N)|/\mu^2=l(l-2)\to\infty.
\]

이는 의도적으로 `X<N/2`이므로 Goldbach 반례가 아니다.

**폐기한 경로:** 분모--cutoff--target 결합이 없는 전 growing-denominator
점근식, RMS에서 모든 target으로의 자동 승격.

**논리/유한 계산 한계:** exact 행은 대수와 반례족을 검산한다.
Siegel--Walfisz 입력은 비효과적이다. arc 근방, targetwise minor-arc 음의
질량, 모든 짝수의 양의 하한은 증명하지 않았다.

**다음 단일 보조정리:**
`UniformTargetAlignedBinaryPrimeMinorArcNegativeMassBelowPolylogMajorArcMargin`.

## 4. 쌍둥이 소수 추측 트랙

### 이번에 증명할 정확한 명제

`CriticalEntropyDampedSignedCRTLargeSieveAndParityRetentionNoGo`.
TICKET-232의 centered CRT 부호 `psi_l`, `b_S=E_nu psi_S`를 쓰고
`x_S=product_(l in S)x_l`, `c_l=(l-1)/(l-3)<=2`라 하면

\[
\sum_{S\ne\varnothing}x_Sb_S^2
\le\prod_l(1+c_lx_l)-1.
\]

또 `|sigma_S|<=1`에 대해

\[
|\sum_{S\ne\varnothing}\sigma_Sx_Sb_S|^2
\le(\prod_l(1+x_l)-1)(\prod_l(1+c_lx_l)-1).
\]

따라서 `sum x_l=o(1)`이면 보편적 signed saving이 성립한다.

### 증명과 두 no-go

`psi_l^2`의 두 값은 `(l-3)/(l-1)`, `(l-1)/(l-3)`이다. Jensen으로
`b_S^2<=E_nu psi_S^2`, 곱 전개로 energy bound, Cauchy로 signed bound를
얻는다.

하지만 임계 damping `x_l=tau/m`에서 비음수 정규화 밀도

\[
g={1\over2}\prod_l(1+\psi_l/2)
+{1\over2}\prod_l(1-\psi_l/2)
\]

는 singleton과 모든 홀수 차 계수가 `0`인데도 양의 signed aggregate가
`cosh(tau/2)-1`로 수렴한다. local centering과 임계 엔트로피만으로는
saving을 얻지 못한다.

full parity multiplier `x_L>=eta>0`를 보존하려 하면

\[
\sum_lx_l\ge m\eta^{1/m},\qquad
\prod_l(1+x_l)-1\ge2^m\sqrt\eta-1.
\]

따라서 bounded product entropy와 full parity 보존은 양립하지 않는다.

**폐기한 경로:** critical product entropy와 centered marginal만으로
보편 signed saving을 얻는 경로, bounded entropy와 full parity retention을
동시에 요구하는 경로.

**논리/유한 계산 한계:** counterfamily는 CRT 확률모형이지 실제 prime
weight가 아니다. 양의 twin main term과 쌍둥이 소수의 무한성/유한성 어느
쪽도 증명하지 않는다.

**다음 단일 보조정리:**
`PrimeWeightedCriticalNoiseCRTChiSquareDecayAtTwinScale`.

## Proof DAG

- `RH-T232 -> RH-T233 -> RH-OPEN233 -> RH`
- `CO-T182,T188,T195,T209,T214 -> CO-T233`; 잘못 열린 옛 노드는
  `CO-N232`로 정정한다. `CO-T233 -> CO-OPEN233`은 전체 periodic 경계로
  이어지고, 별도의 aperiodic 경계까지 닫혀야 `CO`에 도달한다.
- `GB-T232, Siegel--Walfisz -> GB-T233 -> GB-OPEN233 -> GB`
- `TP-T232 -> TP-T233 -> TP-OPEN233 -> TP`

네 원 추측 노드는 모두 `open_not_proven` 상태다.
