# TICKET-232: 유효차원·콜라츠 binary defect·골드바흐 유리 shell·CRT 희소성

## 주장 상태

**미해결, 증명되지 않음.** TICKET-232는 정확한 부분정리 또는 no-go
정리 네 개를 증명했지만 리만 가설, 콜라츠 추측, 강한 골드바흐 추측,
쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다. 기계 판독
해결 수는 `0 / 4`이다.

2026-08-21 현재 외부 상태는
[Clay의 리만 가설 페이지](https://www.claymath.org/riemann/),
[Tao의 콜라츠 논문](https://arxiv.org/abs/1909.03562), 최신
[골드바흐 예외집합·주호 공식 논문](https://arxiv.org/abs/2607.27282),
[Maynard의 작은 소수 간격 정리](https://annals.math.princeton.edu/2015/181-1/p07)로
확인했다. 이 자료들은 현재 문맥만 제공하며 아래 네 초등 정리의 증명
전제로 사용하지 않았다.

## 재현 계약

- 생성기: `scripts/ticket232_effective_dimension_binary_defect_rational_shell_crt_sparsity.py`
- 검사: `tests/test_ticket232_effective_dimension_binary_defect_rational_shell_crt_sparsity.py`
- 통합 JSON: `data/open-problem/ticket232-effective-dimension-binary-defect-rational-shell-crt-sparsity.json`
- 정확한 부분·no-go 정리: `4`
- 폐기한 후속 경로: `4`
- 해결한 상위 추측: `0`
- 기계 검사 실패: `0`

## 1. 리만 가설 트랙

### 이번에 증명한 정확한 명제

높이 `T`마다 `q_j(T)>1`, `w_j(T)>=0`이고 유한한 전체 질량이
`0<W_T<infinity`라
하자. 다음을 정의한다.

\[
F_T(n)=\sum_jw_j(T)|1-q_j(T)^{-in}|^2.
\]

`Q^M<=T`인 모든 머리 길이 `M`, 정수 `Q>=2`에 대해 어떤
`1<=n<=T`가 존재하여

\[
{F_T(n)\over W_T}\le {4\pi^2\over Q^2}+4\delta_T(M),
\qquad
\delta_T(M)={\sum_{j>M}w_j(T)\over W_T}
\]

를 만족한다. 따라서 모든 `1<=n<=T`에서 `F_T(n)>=cW_T`이고
`delta_T(M)<=c/8`, `4*pi^2/Q^2<c/2`이면

\[
Q^M>T,\qquad M>{\log T\over\log Q}.
\]

즉 고정된 양의 정규화 하한을 가진 적응형 프레임에는 최소
`Omega(log T)`개의 유효 좌표가 필요하다.

### 논증·계산·한계

앞 `M`개 위상에 동시 Dirichlet 비둘기집 근사를 적용하면
`n<=Q^M`인 충돌 증인을 얻는다. 머리는 `4*pi^2/Q^2`, 꼬리는
`|1-z|^2<=4`로 제한한다. 배율의 곱셈적 독립성도 필요 없다.

생성기는 다섯 충돌행과 `c=1/2`, 꼬리 비율 `1/16`, `Q=13`인
`M>log(T)/log(13)`의 명시적 귀결을 검산한다. 유한 행은 구현 인증일
뿐이며 무한 필요조건은 위 비둘기집 논증에서 나온다.

**폐기:** 유효차원이 `o(log T)`인 높이 적응형 프레임으로 TICKET-231
장벽을 피하는 경로.

**남은 간극:** 로그 개수의 적응형 배율로 실제 양의 프레임 하한을
구성하고 그 하한이 Weil 꼬리를 지배함을 증명해야 한다. 현재 정리는
Weil 이차형이 아니라 scalar 위상 에너지 정리다.

**다음 단일 보조정리:**
`LogarithmicEffectiveDimensionAdaptiveWeilFrameWithExplicitTailDominance`.

## 2. 콜라츠 추측 트랙

### 이번에 증명한 정확한 명제

`a in {1,2}^h`에 대해

\[
B(a)=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}},
\qquad D(a)=2^{\sum a_j}-3^h
\]

라 하자. `D(a)>0`이고 `a`에서 값 `1`이 한 개, 두 개 또는 세 개이면

\[
D(a)\nmid B(a).
\]

따라서 비자명한 양의 binary valuation 순환은 값 `1`을 적어도 네 번
포함해야 한다. 모든 항이 `2`인 word는 알려진 자명 순환이므로 남긴다.

순환 회전 `a'=(a_1,...,a_{h-1},a_0)`에는
`2^(a_0)B(a')=3B(a)+D(a)`가 성립하고 `gcd(D,6)=1`이므로
`D|B` 여부는 회전에 불변이다. 따라서 아래의 표준 gap 회전은 정당하다.

### 논증

`1`이 하나이면 `(1,2,...,2)`로 회전하여

\[
B-D=2\,3^{h-1}
\]

을 얻는다. `gcd(D,6)=1`, `D>=5`이므로 나눌 수 없다.

`1`이 둘이면 짧은 간격을 `r`로 잡아

\[
B-D=3^{h-r-1}(2\,3^r+4^r)
\]

을 얻는다. 작은 인수는 `h>=6`에서 2-step 귀납으로 `D`보다 작고,
경계 `h=5`는 `D=13`, 작은 인수 `10,34`로 직접 닫힌다.

`1`이 셋이면 원형 간격을 `r,s,t`로 쓰고 `t`가 최대가 되도록 회전한다.

\[
B-D=3^{t-1}Q_{r,s},\qquad
Q_{r,s}=2\,3^{r+s}+4^r3^s+{4^{r+s}\over2}.
\]

`r+s<=floor(2h/3)`에서 높이 `9,10,11`을 기저로 하는 3-step 귀납을
적용하면 `0<Q<D`이다. `h=8`은 정확 정수로 모두 검사한다.

생성기는 높이 24까지 모든 표시된 인수분해를 독립 정수 산술로
검산하며 실패는 0이다. 유한 계산이 무한 정리의 근거는 아니며,
귀납과 인수분해가 무한 가족을 증명한다.

**폐기:** TICKET-231의 `0<B<D` 크기 인증을 그대로 임계띠에 연장하는
경로. `1`이 하나인 무한 가족은 모든 회전에서 `B>D`이다.

**남은 간극:** `1`이 네 개 이상인 binary word, valuation `3` 이상을
포함하는 임계띠 word, 비주기 발산 궤적은 전혀 배제하지 못했다.

**다음 단일 보조정리:** `BinaryFourOneCriticalStripNondivisibility`.

## 3. 강한 골드바흐 추측 트랙

### 이번에 증명한 정확한 명제

홀수 소수 `l`과 실제 소수 `p<=X`, `p!=l` 위의 비음 가중치
`omega_p`에 대해

\[
S(\alpha)=\sum_p\omega_pe(p\alpha),\quad
W_r=\sum_{p\equiv r\pmod l}\omega_p,\quad W=\sum_rW_r
\]

라 하자. `mu=W/(l-1)`, `delta_r=W_r-mu`, `n=N mod l`이면 완전 유리
shell은 정확히

\[
T_l(N)=\sum_{a=1}^{l-1}S(a/l)^2e(-aN/l)
=l\sum_{r+s\equiv N}W_rW_s-W^2.
\]

`l|N`이면

\[
T_l(N)={W^2\over l-1}+l\sum_r\delta_r\delta_{-r},
\]

`n!=0`이면

\[
T_l(N)=-{W^2\over(l-1)^2}
+l\left(\sum_{r\ne n}\delta_r\delta_{n-r}-2\mu\delta_n\right).
\]

빠진 한 소수 `p=l`도 `2b(lW_n-W)+b^2c_l(N)`로 정확히 복구된다.

### 논증·no-go·계산

Ramanujan 합

\[
\sum_{a=1}^{l-1}e(at/l)=l1_{l\mid t}-1
\]

을 전개하고 `W_r=mu+delta_r`를 대입하면 된다. Cauchy로 오차도
명시적으로 제한된다.

그러나 성장하는 `l`에서 classwise 상대 등분포가 `o(1)`이라는 사실만으로
shell 부호를 보존할 수는 없다. `n=1`, `mu=1`, `epsilon=l^(-1/2)`와

\[
W_1=1-\epsilon,\qquad W_r=1+{\epsilon\over l-2}
\]

를 택하면 최대 상대오차는 0으로 가지만 균일 shell `-1`과 달리

\[
T_l(1)=-1+l\left(2\epsilon+{\epsilon^2\over l-2}\right)>0
\]

이다. 이는 잉여류 가중치 반례이지 골드바흐 반례가 아니다.

실제 소수 지시가중치 40행을 정확 정수로 검사했다. 대표적으로
`X=100,l=5,N=66`에서 잉여 질량 `[5,7,7,5]`는 정확 shell `19`를
주지만 균일 특이계수는 `-36`, 자기상관 보정은 `+55`다.

**폐기:** classwise `o(1)` 상대 등분포만으로 성장 유리 shell을 특이계수로
치환하거나 부호를 추론하는 경로.

**남은 간극:** 유리점 주변 호, 합성 분모, 실제 소수의 성장 분모
자기상관 절약, 서로 다른 분모의 부호 있는 총합은 미해결이다.

**다음 단일 보조정리:**
`UniformGrowingDenominatorPrimeResidueAutocorrelationAtSingularCoefficientScale`.

## 4. 쌍둥이 소수 추측 트랙

### 이번에 증명한 정확한 명제

유한한 `L subset {l prime: l>=5}`에서 shift `2` 허용 잉여류의 중심화
이차지표를 정규화하여 `psi_l`이라 하자. 최대 `N`개의 허용 CRT 점에
비음 가중치를 주고 `psi_S=product_(l in S)psi_l`의 정규화 계수를
`b_S`라 한다. 이차지표 부호 pushforward를 `nu_Y,U_Y`라 하면

\[
\sum_{\varnothing\ne S\subseteq L}b_S^2
=\chi^2(\nu_Y\Vert U_Y)
\ge\max\left(0,{1\over Nu_L}-1\right),
\]

\[
u_L=\prod_{l\in L}{l-1\over2(l-2)}.
\]

`L={5<=l<=sqrt(X)}`, `N<=X`이면 이 하한은 무한대로 간다.

### 논증·no-go·계산

각 `{1,psi_l}`가 두 점 부호공간의 정규직교기저이므로 tensor Parseval이
chi-square 항등식을 준다. 지지집합 `B`에 Cauchy를 적용하면

\[
1\le(\chi^2+1)U_Y(B)\le(\chi^2+1)Nu_L.
\]

소수정리와 `u_L<=2^(-m)e^(m/3)`가 발산을 증명한다. `X=10^4,10^5,10^6`
에서 정확 하한은 약 `266.01`, `2.35e13`, `2.00e43`이다.

또 `m=k^2`, `epsilon=1/k`인 곱 tilt는 모든 개별 비상수 계수가 0으로
가지만 전체 에너지는 `e-1`로 간다. 따라서 개별 모드 소멸을 모든
`2^m` 모드에 단순 합산할 수 없다.

**폐기:** twin-sieve scale에서 full, unweighted, positive CRT interaction
에너지를 주계수 제곱보다 작게 만드는 경로. 고정된 모드나 감쇠된 모드의
개별 절약은 반증하지 않았다.

**남은 간극:** 이 정리는 양의 twin 질량을 만들지 않는다. entropy에 맞춘
차수 감쇠, 부호 있는 Type-II 총합, 별도의 양의 주항 하한이 모두 필요하다.

**다음 단일 보조정리:**
`EntropyMatchedSignedCRTInteractionLargeSieveAtTwinScale`.

## 결과 표

| 문제 | 새 결과 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
|---|---|---|---|---|---|
| 리만 | 양의 적응형 하한에는 로그 유효차원이 필요 | 미해결 | sublog 적응형 프레임 | 실제 Weil 꼬리 지배 | 로그 유효차원 적응형 Weil 프레임 |
| 콜라츠 | binary word의 `1` 최대 세 개 층 비나눗셈 | 미해결 | 동일한 `B<D` 연장 | 네 개 `1`, 큰 valuation, 비주기 궤도 | `BinaryFourOneCriticalStripNondivisibility` |
| 골드바흐 | 실제 소수 유리 shell 자기상관 항등식 | 미해결 | classwise `o(1)`이면 shell 제어 | 성장 분모 실제 소수 자기상관 | singular scale 자기상관 절약 |
| 쌍둥이 소수 | full CRT 에너지=chi-square, 희소성 하한 | 미해결 | full unweighted 양의 에너지 절약 | entropy 감쇠 signed Type-II와 양의 주항 | entropy-matched signed CRT large sieve |

유한 표는 식과 구현을 재현할 뿐이다. 네 상위 추측의 무한 양성·하강·상쇄
간극은 그대로 남아 있다.
