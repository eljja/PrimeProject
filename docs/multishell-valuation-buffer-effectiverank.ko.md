# TICKET-238: 다중 shell 누적, valuation 양화사, 중간 규모 buffer, 유효랭크

## 초록과 주장 상태

TICKET-238은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 증명하거나 반증하려는 PrimeProject의 연구를 이어간다.
**네 상위 난제는 모두 미해결이다.** 이번 보고서는 더 좁은 정확 정리 네
개를 증명하고 불충분한 경로 네 개를 폐기한다. 무한 반례나 상위 난제의
완전한 증명을 주장하지 않는다.

기계 판독 결과는
[`ticket238-multishell-valuation-buffer-effectiverank.json`](../data/open-problem/ticket238-multishell-valuation-buffer-effectiverank.json)에
있다. 재현 명령은 다음과 같다.

```powershell
python scripts/ticket238_multishell_valuation_buffer_effectiverank.py
python -m unittest tests.test_ticket238_multishell_valuation_buffer_effectiverank -v
```

| 문제 | TICKET-238의 정확한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `MultishellNormalizedCrossRowSumCriterionAndPairwiseAngleNoGo` (다중 shell 정규화 교차 행합 조건과 쌍별 각도 한계) | 쌍별 principal angle 간격만으로 전역 양성을 얻는 경로 | `ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells` |
| 콜라츠 | `AdaptiveValuationCriterionEquivalenceAndRunBlockClosure` (적응 valuation 조건 동치와 run-block 종결) | 모든 necklace의 valuation 명제를 비가분성보다 약한 중간정리로 취급 | `RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette` |
| 골드바흐 | `MesoscopicBufferWidthNecessaryForInverseLogReflectedMargin` (역로그 반사 여유에 필요한 중간 규모 buffer) | 발산하기만 하는 모든 endpoint buffer가 충분하다는 경로 | `MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack` |
| 쌍둥이 소수 | `DegreeTwoEnergyEffectiveRankEquivalenceAndSupportGrowthNoGo` (2차 에너지와 유효랭크 동치, support 증가 한계) | support 증가만으로 2차 CRT 비상관을 얻는 경로 | `PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl` |

## 1. 리만 가설 트랙

### 선언 명제

`H=(H_ij)_(1<=i,j<=J)`가 `H_ii=I`, `H_ij=K_ij=K_ji*`인 Hermitian
block 행렬이라고 하자. 다음 값을 정의한다.

\[
\eta=\max_i\sum_{j\ne i}\lVert K_{ij}\rVert_{op}.
\]

`eta<1`이면

\[
H\succeq(1-\eta)I. \tag{RH-238.1}
\]

그러나 쌍별 principal angle(주각)이 양수라는 사실만으로는 이 전역 결론이
나오지 않는다. 스칼라 반례족

\[
H_{ii}=1,\qquad H_{ij}=-\rho\ (i\ne j),\qquad0<\rho<1
\]

에서 모든 두-shell 주부분행렬의 최소 고유값은 `1-rho>0`이다. 반면 전체
행렬의 고유값은

\[
1-(J-1)\rho,\qquad1+\rho\quad(J-1\text{중복}) \tag{RH-238.2}
\]

이다. `rho=1/3,J=4`에서는 양의 준정부호이고 상수 mode 고유값이 0이며,
정규단체의 Gram 행렬로 공동 실현된다. 이 행만으로도 **엄격한** 전역
하한은 반박된다. 같은 추상 대수족은 `(J-1)rho>1`이면 부정부호지만,
그 큰 `J` 행을 공동 Gram 실현이라고 주장하지 않는다.

### 증명

block 벡터 `x=(x_i)`에 대해 교차항에 Cauchy--Schwarz와
`2ab<=a^2+b^2`를 적용하면

\[
\begin{aligned}
\langle Hx,x\rangle
&\ge\sum_i\lVert x_i\rVert^2
-2\sum_{i<j}\lVert K_{ij}\rVert\lVert x_i\rVert\lVert x_j\rVert\\
&\ge\sum_i\left(1-\sum_{j\ne i}\lVert K_{ij}\rVert\right)
\lVert x_i\rVert^2\\
&\ge(1-\eta)\lVert x\rVert^2.
\end{aligned}
\]

반례족의 고유값은 상수 벡터와 그 직교여공간으로 분해하면 즉시 얻는다.

### 재현 계산과 한계

정확 유리수 감사는 `rho=1/3`, `J=2,...,8`을 사용한다. 모든 쌍의 최소
고유값은 `2/3`이지만, 전체 상수 mode는 `J=4`에서 0이고 `J=5`부터
음수다. `J=4`는 실제 정규단체 Gram 장애이고, `J=5,...,8`은 추상
block 누적만 보여 준다. 비교족 `K_ij=1/(4J)`는
`eta=(J-1)/(4J)<1`을 만족한다.

이는 유한 block 선형대수 정리이지 산술 Weil 추정이 아니다. 실제
Guinand--Weil innovation shell의 교차 노름 행합을 제어하지 않았고 zeta
영점을 계산하거나 배제하지 않았다. [Clay Mathematics Institute의 공식
페이지](https://www.claymath.org/riemann/)도 RH를 여전히 미해결 문제로
분류한다.

- 폐기: 쌍별 shell-angle 제어만으로 완성되는 전역 양성 인증.
- 유지: 모든 logarithmic shell 사이의 정규화 교차작용을 합산하는 조건.
- 다음 보조정리:
  **ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells**.

## 2. 콜라츠 추측 트랙

### 선언 명제

양의 정수 `D,B`에 대해 소인수분해의 유일성으로

\[
D\nmid B
\quad\Longleftrightarrow\quad
\exists q\text{ 소수}:v_q(D)>v_q(B) \tag{CO-238.1}
\]

가 성립한다. TICKET-197은 모든 `k>=1`에 대해

\[
D_k=32^k-27^k\nmid
B_k=32^k+27^k-2\cdot18^k
\]

를 증명했다. 따라서 모든 이진 run block `1^k 2^(2k)`에는 단어에 따라
달라지는 prime-power valuation 증인이 존재한다.

반대로 `(CO-238.1)`을 모든 primitive binary density-band necklace에
요구하는 명제는 그 전체 클래스의 affine 비가분성과 정확히 동치다.
valuation 표현은 인증서를 제공하지만 빠진 전칭 양화사를 제거하지 않으므로
더 약한 중간정리가 아니다.

### 증명과 정확 감사

`D=product_q q^(e_q)`라 쓰면 `D|B`는 모든 `q|D`에서
`v_q(B)>=e_q`인 것과 동치다. 이를 부정하면 `(CO-238.1)`이다.
TICKET-197의 닫힌식 부등식이 모든 `k`에서 `D_k not dividing B_k`를
주므로 인수분해를 실제 수행하지 않아도 valuation 증인의 존재가 따른다.

재현 감사에는 `1<=k<=20`의 명시적 증인을 기록했다. 예를 들어 `k=1`의
`q=5`, `k=2`의 `q=59`, `k=8`의 `q=41`, `k=14`의 `q=43`이다. 각
행은 `v_q(D_k)>v_q(B_k)`를 정수 연산으로 직접 검사한다. 모든 `k` 결론은
이 유한 표의 추세가 아니라 TICKET-197과 소인수분해 유일성에서 나온다.

이 결과는 한 run-block 무한족에만 적용된다. 일반 necklace, 2보다 큰
valuation을 포함한 단어, 비주기 발산은 열려 있다. [Angeltveit의 2026년
유한 검증 알고리즘](https://arxiv.org/abs/2602.10466) 같은 계산 개선도 이
무한 양화사를 대신하지 않는다.

- 폐기: 일반 necklace valuation 명제를 universal affine 비가분성보다
  작은 보조정리로 제시하는 경로.
- 유지: 이미 닫힌 run-block에서 증인이 모든 고정 palette 밖으로 빠져나가는
  메커니즘을 먼저 증명한 뒤 run complexity로 확장.
- 다음 보조정리: **RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette**.

## 3. 강한 골드바흐 추측 트랙

### 선언 명제

`x_X`를 `X` 이하 소수의 지시함수, `g_X=x_X*x_X`를 순서 있는 덧셈
convolution이라 하자. `0<=h<=X-2`이면

\[
g_X(2X-h)\le h+1. \tag{GB-238.1}
\]

따라서 정규화된 역로그 여유

\[
{g_X(2X-h)\over\pi(X)}\ge {c\over\log X},\qquad c>0
\]

를 얻으려면 반드시

\[
h+1\ge {c\pi(X)\over\log X}
=(c+o(1)){X\over(\log X)^2} \tag{GB-238.2}
\]

이어야 한다. 즉 `h=o(X/(log X)^2)`인 buffer는 Fourier 추정과 무관하게
TICKET-237의 역로그 목표에 너무 얇다.

### 증명과 계산

`p,q<=X`, `p+q=2X-h`이면 `X-h<=p<=X`다. 가능한 정수 `p`가 최대
`h+1`개이므로 `(GB-238.1)`이 성립한다. 이를 `pi(X)`로 나누고 소수정리를
적용하면 `(GB-238.2)`를 얻는다.

정확 감사는 `X=100,1000,10000,100000`과
`h=0,1,floor(sqrt X)`를 검사한다. 12개 행마다 가능한 정수 구간, 실제
ordered 소수쌍 수, 상계 `(h+1)/pi(X)`를 기록했고 모두 통과했다.

이는 upper endpoint 근처의 필요조건일 뿐이다. `X/(log X)^2` 규모가
충분하다고 증명하지 않았고 실제 reflected minor 항도 제어하지 않았으며
골드바흐 반례도 찾지 않았다. 예외집합 정리는 평균적 덮임을 다루므로 여전히
점별 승격이 필요하다. 최신 1차 문헌 맥락은
[Grimmelt--Bhowmik](https://arxiv.org/abs/2607.27282)을 참고할 수 있다.

- 폐기: “무한히 커지는 buffer면 역로그 gain에 충분하다”는 경로.
- 유지: 최소 `X/(log X)^2` 규모의 중간 buffer와 독립적인 점별 minor 여유.
- 다음 보조정리:
  **MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack**.

## 4. 쌍둥이 소수 추측 트랙

### 선언 명제

`C`를 `m`개의 centered variance-one 좌표의 Gram 행렬이라 하고

\[
E_{m,2}={1\over\binom m2}\sum_{i<j}|C_{ij}|^2,
\qquad
r_{eff}(C)={\operatorname{tr}(C)^2\over\lVert C\rVert_F^2}
\]

로 둔다. 그러면 정확히

\[
r_{eff}(C)={m\over1+(m-1)E_{m,2}},
\qquad
E_{m,2}={m/r_{eff}(C)-1\over m-1}. \tag{TP-238.1}
\]

따라서 `m`이 무한대로 갈 때

\[
E_{m,2}\to0
\quad\Longleftrightarrow\quad
r_{eff}(C)\to\infty. \tag{TP-238.2}
\]

support 증가만으로는 충분하지 않다. 두 개의 centered 직교 mode를 각각
`m/2`번 반복하고 support 크기를 `m+1`로 늘리면

\[
r_{eff}=2,
\qquad
E_{m,2}={m/2-1\over m-1}\longrightarrow{1\over2}. \tag{TP-238.3}
\]

### 증명과 계산

`C_ii=1`이므로

\[
\lVert C\rVert_F^2
=m+2\sum_{i<j}|C_{ij}|^2
=m+m(m-1)E_{m,2}.
\]

이를 유효랭크 정의에 대입하면 `(TP-238.1)`이 나온다. 또한
`1/r_eff=1/m+(1-1/m)E_(m,2)`이므로 `(TP-238.2)`가 성립한다. 반복 mode
반례족의 유일한 비영 Gram 고유값은 `m/2,m/2`여서 `(TP-238.3)`을 준다.
`m=4,8,16,32,64`의 정확 행은 support가 5에서 65로 증가해도
`r_eff=2`임을 검증한다.

이 정리는 TICKET-237의 support-rank 필요조건을 더 정확히 했지만 여전히
추상 Gram 기하학이다. 실제 prime-weighted 유효랭크 발산, 균일 대각
비퇴화, 양의 twin 주성분, parity breaking은 증명하지 않았다. Maynard의
[small-gap 정리](https://annals.math.princeton.edu/2015/181-1/p07)는 bounded
gap을 주지만 고정 간격 2를 주지 않는다.

- 폐기: support 증가만으로 완성되는 decorrelation 인증.
- 유지: 정규화된 CRT Gram 유효랭크의 산술적 발산.
- 다음 보조정리:
  **PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl**.

## 통합 proof DAG

```text
RH-T237 -> RH-T238 -> RH-N238 [폐기]
                    -> RH-OPEN238 -> RH [미해결]

CO-T197 + CO-T237 -> CO-T238 -> CO-N238 [폐기]
                               -> CO-OPEN238 -> 주기 후보 전체 -> CO [미해결]

GB-T237 -> GB-T238 -> GB-N238 [폐기]
                    -> GB-OPEN238 -> GB [미해결]

TP-T237 -> TP-T238 -> TP-N238 [폐기]
                    -> TP-OPEN238 -> parity/주성분 gate -> TP [미해결]
```

## 최종 경계

TICKET-238은 정확한 부분·no-go 정리 네 개, 경로 교정 네 개, 기계 판독
proof DAG 네 개, 계산 실패 0개, 상위 난제 해결 0개를 기록한다. 유한 행은
공식과 인증 구현을 검증한다. 유한 범위를 넘는 결론은 본문에 표시한 대수적
논증에만 의존한다. 학술적 독창성이나 우선권을 주장하려면 독립 전문가의
검토가 추가로 필요하다.
