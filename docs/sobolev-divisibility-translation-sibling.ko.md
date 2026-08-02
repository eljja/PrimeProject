# TICKET-182: Sobolev 에너지, 나눗셈 조건, 평행이동, 형제 블록 국소화

## 상태와 주장 경계

TICKET-182는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. TICKET-181의 조건부 연결을 각
문제의 실제 표현에 더 가까운 형태로 정밀화한 정확한 중간 정리 네 개와
유한 산술 진단을 제공한다. 유한 계산은 전칭 정리를 대신하지 않는다.

| 문제 | 이번에 확정한 결과 | 해결 상태 |
|---|---|---|
| 리만 가설 | `FejerH1TailCertificateAndRawPrimeEnergyNoGo` | 중간 정리 증명, 리만 가설 미해결 |
| 콜라츠 | `AcceleratedCycleIffAffineDivisibility` | 중간 정리 증명, 콜라츠 미해결 |
| 골드바흐 | `WeightedTranslationModulusCertificateAndRmsSpikeNoGo` | 중간 정리 증명, 골드바흐 미해결 |
| 쌍둥이 소수 | `WeightedSiblingContrastIdentityAndMeanPathNoGo` | 중간 정리 증명, 쌍둥이 소수 미해결 |

독립적인 신규성 검토 전에는 학술적 최초 발견이라고 주장하지 않는다.
이번 결과의 목적은 남은 증명 의무를 정확하고 계산 가능한 형태로 만드는
것이다.

## TICKET-181 이후 무엇이 달라졌는가

```text
리만:       Lipschitz 연속성 -> Fourier multiplier에 맞춘 H1 에너지
콜라츠:     slack equality -> 정확한 affine 나눗셈 조건
골드바흐:   인접 표적 차이 -> 가중 균일 평행이동 modulus
쌍둥이:     추상 경로 증분 -> 질량 가중 형제 블록 대비
```

공통 문제는 집중 현상이다. 유한 표본, 평균 valuation, RMS 평행이동,
level 평균 진동은 모두 하나의 결정적 방향이나 예외 경로를 숨길 수 있다.

## 1. 리만 가설

### 선언 명제

절대연속인 주기함수

```text
f(theta)=sum_k a_k exp(i k theta)
```

에 대해 정규화한 도함수 에너지를

```text
D2^2 = integral |f'|^2/(2*pi) = sum_k k^2|a_k|^2
```

라 하자. `sigma_N f`가 차수 `N`의 Fejer 평균이고

```text
C_N^2 = 2((N-1)/N^2 + sum_(k>=N)1/k^2)
```

이면

```text
||f-sigma_N f||_infinity <= C_N D2.
```

따라서

```text
||sigma_N f||_infinity+C_N D2<delta
```

는 `||f||_infinity<delta`의 엄밀한 인증서다.

### 증명

Fejer 잔차 multiplier는 `q_N(k)=min(|k|/N,1)`이다. 각 Fourier 항에
`|k|`와 `1/|k|`를 삽입해 Cauchy-Schwarz 부등식을 적용하면

```text
sum q_N(k)|a_k|
 <= (sum q_N(k)^2/k^2)^(1/2)(sum k^2|a_k|^2)^(1/2)
 = C_N D2.
```

표본값과 표본 도함수를 동시에 보더라도 전역 `D2`를 알 수는 없다.
`A(1-cos(N theta))`와 그 도함수는 `N`개 격자점에서 모두 0이지만 실제
함수의 최대 노름은 `2A`이고 도함수 에너지는 `AN/sqrt(2)`다.

### 원시 prime proxy의 no-go

```text
f_P(theta)=sum_(n<=P) Lambda(n)/sqrt(n) cos(n theta)
```

로 정의한 유한 proxy는

```text
D2(P)^2=(1/2)sum_(n<=P)n Lambda(n)^2
```

를 갖는다. 소수 항만 보아도 이 합은 발산한다. 실제 계산에서도 `P`가
100에서 100,000으로 증가할 때 `D2`가 약 94에서 165,913으로 커졌다.

이 proxy는 실제 pole-neutral Weil 기호가 아니다. 여기서 폐기되는 것은
양의 prime 계수를 smoothing 없이 그대로 `H1` 인증서에 넣는 경로다.

### 판단

- **폐기:** 원시 prime 계수의 `H1` 에너지와 격자에서 추정한 도함수
- **유지:** 위상 정보를 보존하면서 smoothing한 pole-neutral 기호의 전역 에너지
- **남은 간극:** 실제 기호의 에너지가 core margin보다 작다는 정리가 없다.
- **다음 보조정리:**
  `SmoothedPoleNeutralWeilSymbolHasWeightedH1EnergyBelowCoreMargin`

최근의 유한 Weil operator 계산도 수치적 증거이며 RH 증명이 아님을 명시한다
([Kim 외 2026](https://arxiv.org/abs/2607.24830),
[Groskin 2026](https://arxiv.org/abs/2605.20224)).

## 2. 콜라츠 추측

### 선언 명제

양의 accelerated valuation word `w=(v_0,...,v_(h-1))`에 대해

```text
S=sum_j v_j,
B(w)=sum_j 3^(h-1-j)2^(v_0+...+v_(j-1)),
D=2^S-3^h
```

라 하자. `w`가 양의 홀수 콜라츠 주기의 정확한 valuation word일 필요충분조건은

```text
D>0 이고 D가 B(w)를 나눈다.
```

`w_j`가 `j`번째 순환 회전이면 주기 원소는 `n_j=B(w_j)/D`다.

### 증명

주기라면 `2^S n_0=3^h n_0+B(w)`이므로 `Dn_0=B(w)`다. 반대로 순환
회전의 분자 `B_j` 사이에는

```text
3B_j+D=2^(v_j)B_(j+1)
```

가 정확히 성립한다. `D`는 홀수이므로 `D|B_0`는 모든 회전에 전파된다.
따라서 `n_j=B_j/D`는 양의 홀수이고

```text
3n_j+1=2^(v_j)n_(j+1)
```

가 성립한다. 다음 원소가 홀수이므로 `v_j`는 실제 2-adic valuation과 같다.

### 재현 가능한 유한 계산

valuation `{1,2,3,4,5}`와 길이 1부터 8까지 총 488,280개 word를 정확
계산했다. `D|B`인 경우는 각 길이마다 하나씩 총 8개였고, 모두
`(2,...,2)`와 값 1인 고정점 반복이었다. 비자명 후보는 0개였다.

이 결과는 길이 9 이상이나 valuation 6 이상을 다루지 않는다.

### no-go와 판단

평균 `S/h`만으로 equality를 배제할 수 없다. `(2,...,2)`는 모든 길이에서
`D>0`이고 `D|B`다. 순서 있는 affine numerator가 반드시 필요하다.

- **폐기:** 평균 valuation surplus와 유한 slack 양성만으로 주기를 배제하는 경로
- **유지:** 모든 순서 있는 word에 대한 정확한 affine 나눗셈 조건
- **남은 간극:** 임의 길이의 비상수 word에서 `D`가 `B(w)`를 나누지 않음을
  증명하지 못했다.
- **다음 보조정리:**
  `OnlyConstantTwoValuationWordsSatisfyPositiveAffineCycleDivisibility`

거의 모든 orbit에 대한 결과는 이 모든-word 나눗셈 배제를 주지 않는다
([Tao 2019/2026](https://arxiv.org/abs/1909.03562)).

## 3. 강한 골드바흐 추측

### 선언 명제

`Z/LZ` 위의 실수 sequence `e`와 비음수 단위질량 kernel `w`에 대해

```text
omega_e(t)=max_j|e_j-e_(j-t)|
```

라 하면

```text
||e-w*e||_infinity <= sum_t w_t omega_e(t).
```

`D`가 최대 인접 차이면 `omega_e(t)<=D d_L(0,t)`이므로 이 상계는
TICKET-181의 인접차 상계보다 나쁘지 않다.

### 증명과 RMS no-go

```text
e_j-(w*e)_j=sum_t w_t(e_j-e_(j-t))
```

에 삼각부등식을 적용하면 된다. 긴 shift에서 실제로 생기는 상쇄를 인접차의
반복 합으로 버리지 않는다는 점이 개선이다.

그러나 균일 modulus를 RMS로 바꾸면 틀린다. 높이 `A`인 한 점 spike의
평행이동 RMS는 `A sqrt(2/L)`로 0에 가지만, Fejer 잔차는 차수가 `o(L)`이면
`A(1-w_0)`에서 `A`로 간다. 모델 `L=64,...,1024`에서 RMS 예산/실제 오차
비율은 약 0.18에서 0.04로 감소했다.

### 실제 소수 유한 진단

20,000 이하 짝수의 홀수 소수쌍 표현 수를 계산했다. 10,002부터 20,000까지
5,000개 표적을 경험적 block 평균으로 정규화했을 때 shift
`2,4,8,16,32,64`의 균일 modulus는 약 2.00~2.07, RMS modulus는 약
0.66~0.67이었다.

경험적 평균은 증명된 circle-method 주항이 아니다. 이 계산은 실제 데이터의
집중 정도를 진단할 뿐 무한 명제를 증명하지 않는다.

### 판단

- **폐기:** RMS 또는 평균 평행이동 regularity를 every-target 상계로 쓰는 경로
- **유지:** 실제 잔차에 맞춘 Fejer 가중 균일 평행이동 modulus
- **남은 간극:** 모든 큰 block에서 필요한 산술 상계가 없다.
- **다음 보조정리:**
  `GoldbachResidualHasWeightedUniformTranslationModulusBelowLowPassMarginOnEveryLargeBlock`

예외집합 정리는 예외 표적을 허용하므로 이 균일 modulus를 제공하지 않는다
([Grimmelt·Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. 쌍둥이 소수 추측

### 선언 명제

두 자식 block의 양의 질량이 `m_L,m_R`, 가법적 통계가 `S_L,S_R`, 비율이
`r_L=S_L/m_L`, `r_R=S_R/m_R`이면

```text
r_P=(m_Lr_L+m_Rr_R)/(m_L+m_R),
r_L-r_P=m_R(r_L-r_R)/(m_L+m_R),
r_R-r_P=m_L(r_R-r_L)/(m_L+m_R).
```

즉 경로 증분은 질량 가중 형제 block 대비와 정확히 같다.

### 평균 경로 no-go

깊이 `L`인 균일 tree의 leaf 하나에만 값 1을 놓자. root 비율은 `2^(-L)`,
선택 leaf 비율은 1, 선택 경로 총변화는 `1-2^(-L)`다. 하지만 각 level의
평균 절대 증분은 `2^(-L)`뿐이므로 level 평균의 합은

```text
L/2^L -> 0
```

이다. tree 전체 평균 regularity로 한 예외 경로를 제어할 수 없다.

### 실제 쌍둥이 소수 유한 진단

구간 `[100000,362144)`에서 실제 쌍둥이 소수 시작점 2,298개를 계산했다.
Hardy-Littlewood 기대질량으로 block을 정규화한 결과 root 비율은 1.00038,
가장 높은 길이 1,024 leaf 비율은 1.94275, 그 경로의 `l1` 변화량은
1.08179였다. 형제 항등식의 수치 오차는 `1.2e-16` 이하였다.

이는 한 유한 tree이며 이후 모든 block의 하계를 주지 않는다.

### 판단

- **폐기:** level 평균 진동과 한 번의 양호한 유한 tree
- **유지:** 모든 dyadic 경로에서 제어되는 질량 가중 형제 대비
- **남은 간극:** 실제 prime-pair block의 균일 경로 예산과 parity를 넘는 양의
  하계가 없다.
- **다음 보조정리:**
  `PrimePairSiblingContrastHasUniformCarlesonPathBudgetBelowCancellationMargin`

## 결론

TICKET-182는 정확한 정리 4개와 잘못된 승격 경로 4개를 확정했다. 그러나
다음 무한 산술 전제는 모두 열려 있다.

```text
리만:       smoothing된 실제 기호의 H1 에너지가 core margin 아래
콜라츠:     모든 비상수 valuation word에서 D가 B(w)를 나누지 않음
골드바흐:   모든 큰 block의 균일 평행이동 잔차 상계
쌍둥이:     모든 경로의 형제 대비 예산과 parity를 넘는 양성
```

기계 판정은 정확한 정리 4, 폐기 경로 4, proof DAG 4, 실패 0, 난제 해결 0이다.

