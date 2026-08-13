# TICKET-228: 근접 에일리어스·아핀 언어·잉여류 스펙트럼

English edition: [near-alias-affine-language-residue-spectrum.md](near-alias-affine-language-residue-spectrum.md)

## 초록과 주장 경계

TICKET-228은 TICKET-227이 남긴 네 미해결 보조정리를 실제로 시험했다.
정확한 부분정리 네 개를 증명하고, 제안 경로 네 개를 반박하거나 범위를
축소했으며, 문제별 후속 보조정리 하나를 명시했다. 그러나 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다.

| 문제 | 이번에 확정한 결과 | 폐기·축소한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | 유한한 배율 집합에는 임의로 큰 동시 근접 에일리어스가 존재한다 | 유한한 배율 집합이 전체 주파수축에서 양의 균일 프레임 하한을 가진다는 경로 | `ExplicitDiophantineLossDualDilationFrameBoundOnBandlimitedWeilCores` (대역 제한 Weil 핵에서 디오판토스 손실을 명시한 이중 배율 프레임 하한) |
| 콜라츠 추측 | 같은 기울기의 두 블록이 깊이 `r`마다 `2^r`개의 서로 다른 원시 비순환 word를 하나의 정확한 아핀 원뿔 안에서 만든다 | 보편 소수 거듭제곱 witness가 `D`가 `B`를 나누지 않는다는 조건보다 실질적으로 약한 다리라는 가정 | `CofinalEqualSlopeAffineConeCoverForAllPrimitiveCycleCandidateWords` (모든 원시 순환 후보 word를 종국적으로 덮는 동일 기울기 아핀 원뿔) |
| 강한 골드바흐 | 움직이는 잉여류 연산자의 목표 의존 특이값 스펙트럼과 국소 인수를 정확히 구했다 | 스칼라 국소 밀도만으로 모든 소수 가중 이동 인수 cell을 제어하는 경로 | `UniformMovingTargetCharacterCancellationAfterLocalSpectrumExtraction` (국소 스펙트럼 분리 뒤 움직이는 목표에 대한 균일 지표 상쇄) |
| 쌍둥이 소수 | 두 shift-two 마스크의 교차 Gram 연산자를 정확히 구했고, 두 side channel의 동시 생존은 mod `3`에서 불가능함을 증명했다 | `qr-2`와 `qr+2`의 동시 국소 생존을 결합해 상쇄를 만드는 경로 | `UniformShiftTwoCharacterModeCancellationAcrossCubeRootFactorCells` (세제곱근 인수 cell 전역의 균일 shift-two 지표 mode 상쇄) |

공통 결론은 부정적이지만 중요하다. 단사성, 국소 밀도, 큰 명시적 무한족은
각각 안정적 역변환, 지표 상쇄, 종국적 전면 포괄과 다르다. TICKET-228은
그동안 암묵적으로 건너뛴 단계를 정확한 미해결 명제로 바꾼다.

## 1. 리만 가설

### 명제 RH-228

모든 원소가 `1`보다 큰 유한 집합 `Q={q_1,...,q_m}`에 대해

```text
F_Q(tau) = sum_j |1-q_j^(-i tau)|^2
```

라 두자. 임의의 `T>0`, `epsilon>0`에 대해

```text
tau>T 이고 F_Q(tau)<epsilon인 tau가 존재한다.                 (RH-228.1)
```

따라서 유한한 배율 족은 전체 허수축에서 양의 주파수 균일 하한을 가질 수
없다.

### 증명

`q_1`을 고정하고 `j>=2`에 대해
`alpha_j=log(q_j)/log(q_1)`라 두자. 동시 디리클레 근사 정리에 따르면
모든 정수 `N>=1`에 대해 `1<=n<=N^(m-1)`인 정수 `n`을 골라, 모든
`n alpha_j`와 가장 가까운 정수 사이 거리를 `1/N` 이하로 만들 수 있다.

```text
tau = 2 pi n/log(q_1)
```

로 두면 첫 위상은 정확히 `1`이고 나머지 위상과 `1`의 거리는 각각
`2 pi/N` 이하이다. 선택된 `n`들이 무한히 커지면 큰 근접 에일리어스의
부분수열을 얻는다. 반대로 `n`들이 유계라면 하나의 `n`이 무한히 많은
`N`에서 반복되고, 그 모든 위상 오차는 정확히 `0`이어야 한다. 이때 그
`n`의 양의 정수배가 임의로 큰 정확한 에일리어스를 준다. 두 경우 모두
`(RH-228.1)`이 성립한다.

`Q={2,3}`에서는 `log(3)/log(2)`의 연분수 수렴분수 `p/q`로

```text
tau_q = 2 pi q/log(2),
F_{2,3}(tau_q) = 4 sin^2(pi(q log(3)/log(2)-p))             (RH-228.2)
```

라는 명시적 근접 에일리어스 열을 얻는다.

### 계산과 한계

연분수 감사는 `q=10,781,274`, `tau=97,729,233.11`까지 계산했고 축약
위상 에너지는 `1.2244060829494818e-14`였다. 이 표는 정리를 시각화하는
유한 검산이며, 모든 주파수에 대한 결론은 디리클레 근사가 증명한다.

TICKET-227의 “배율 `2`와 `3`에는 공통 비영 정확 에일리어스가 없다”는
정리는 그대로 맞다. 그러나 RH-228은 정확한 단사성이 안정적 균일 역변환을
주지 않음을 보인다. 따라서 후속 프레임 정리는 대역을 제한하거나 주파수에
따른 디오판토스 손실을 명시해야 한다. Weil 양성도 리만 가설도 증명하지
않았다.

## 2. 콜라츠 추측

### 명제 CO-228

다음 세 valuation word를 사용한다.

```text
U_0=(1,3,3,1),   U_1=(2,3,1,2),   V=(1,4,1).
```

정규화한 아핀 자료 `(A/C,B/C)`는

```text
U_0: (81/256,221/256),
U_1: (81/256,223/256),
V:   (27/64,47/64)
```

이다. 모든 `r>=1`과 길이 `r`인 모든 이진 word `epsilon`에 대해

```text
W_epsilon=U_(epsilon_1)...U_(epsilon_r)V
```

라 두면, `D=C-A`에 대해

```text
887/700 <= B(W_epsilon)/D(W_epsilon) <= 7123/5600          (CO-228.1)
```

이다. 따라서 `1<B/D<2`이고 `D`는 `B`를 나누지 않는다. 각 word에는
지수 `4`가 정확히 한 번 있으므로 원시적이며 순환 word가 아니다. 깊이
`r`에는 서로 다른 인증 word가 정확히 `2^r`개 있다.

### 증명

두 블록을 공통 기울기 `a=81/256`인 `x -> a x+b_j`로 쓰면
`b_j`는 `[221/256,223/256]` 안에 있다. 블록 `r`개를 합성한 절편 `y`는

```text
b_min(1-a^r)/(1-a) 와 b_max(1-a^r)/(1-a)
```

사이에 있다. `(c,d)=(27/64,47/64)`인 `V`를 붙이면 고정점 비율은

```text
R=(c y+d)/(1-c a^r)
```

이다. 양 끝 절편에서 `R`은 `t=a^r`의 분수선형 함수이며
`0<=t<=a`에서 극이 없다. 따라서 네 끝점 값만 비교하면 되고, 그 최솟값은
`887/700`, 최댓값은 `7123/5600`이다. `(1,2)` 안에는 정수가 없으므로
`D`는 `B`를 나누지 않는다. 비자명한 반복 word에서는 모든 기호 수가
반복 횟수의 배수이지만, 여기서는 `4`가 한 번뿐이므로 원시성도 성립한다.

### 계산과 한계

깊이 `10`까지 모두 `2,046`개 word를 정확한 정수 연산으로 완전 검사했다.
직접 아핀 합성, 원뿔 경계, 비나눗셈, 원시성에서 실패는 없었다. 모든
깊이에 대한 결론은 기호적 구간 증명이 담당하며, 유한 열거는 회귀 검산이다.

이 결과는 지수적으로 분기하는 비순환 언어이지 모든 원시 valuation word를
종국적으로 덮는 정리가 아니다. 비주기 자연수 궤도의 하강도 증명하지
않는다. 또한 TICKET-224가 소수 거듭제곱 witness의 존재와 `D`가 `B`를
나누지 않는 조건이 동치임을 이미 보였으므로, 보편 witness 요구는
순환 배제 목표를 다른 말로 반복한 것일 뿐이다.

## 3. 강한 골드바흐 추측

### 명제 GB-228

홀수 소수 `l`, 곱셈군 `G=(Z/lZ)^*`, `n=l-1`을 잡고, `a mod l`에 대해

```text
M_a(u,v)=1  if uv != a (mod l), otherwise 0
```

인 단위 잉여류 행렬을 정의한다. `a=0`이면 `M_0=J`이고 특이값은
`n,0,...,0`이다. `a!=0`이면

```text
M_a=J-P_a,
M_a^T M_a=I+(n-2)J                                        (GB-228.1)
```

이다. 여기서 `P_a(u,v)=1_(uv=a)`는 대칭 대합 순열행렬이다. 따라서 상수
mode의 특이값은 `l-2`, 비상수 mode의 특이값은 모두 `1`이고 중복도는
`l-2`이다. `a=N mod l`로 적용하면 정확한 국소 생존 비율은 `l|N`일 때
`1`, 그렇지 않을 때 `(l-2)/(l-1)`이다.

### 증명

단위의 곱은 `0`이 아니므로 `M_0=J`다. `a!=0`이면 각 행과 열에서 금지되는
항이 하나씩이고, `u -> a/u`는 대합이므로 `P_a=P_a^T`, `P_a^2=I`,
`JP_a=P_aJ=J`다. `J^2=nJ`를 이용해 `(J-P_a)^2`를 전개하면
`(GB-228.1)`을 얻는다. 상수 벡터와 그 직교여공간으로 제한하면 특이값과
국소 비율이 바로 나온다.

### 계산과 한계

`43` 이하 첫 `13`개 홀수 소수의 모든 목표 잉여류 `279`개를 정확한 행렬
곱으로 검사했다. TICKET-227의 `N=10^4,10^5,10^6` 세제곱근 인수 cell도
이 마스크에 투영했다. `l|N`인 경우 거친 인수 곱이 배제되지 않는다는
예측도 모두 일치했다. 이때 각 소인수는 세제곱근 cutoff보다 크므로 `l`로
나누어지지 않는다.

하지만 스칼라 국소 인수는 소수 가중 이동 cell을 제어하지 못한다.
`(GB-228.1)`에서 모든 비상수 지표 방향이 특이값 `1`로 살아남기 때문이다.
무한히 커지는 목표와 인수 cell 전역에서 이 mode들을 균일하게 상쇄하는
정리가 남아 있다. 강한 골드바흐는 해결되지 않았다.

## 4. 쌍둥이 소수 추측

### 명제 TP-228

`G` 위의 두 side-channel 마스크 `M_2`, `M_{-2}`에 대해

```text
M_2^T M_{-2}=(l-3)J+P_2P_{-2}                              (TP-228.1)
```

이다. 합이 `0`인 부분공간에서 `P_2P_{-2}`는 `-1`을 곱하는 순열로
작용한다. 따라서 두 side channel에는 서로 결맞은 비상수 mode가 남는다.
`l=3`에서는 금지 잉여류 `2`와 `-2`가 모든 단위를 차지하므로 동시 국소
생존 마스크가 항등적으로 `0`이다.

### 증명

`JP_a=P_aJ=J`, `n=l-1`을 사용해 `(J-P_2)(J-P_{-2})`를 전개하면
`(TP-228.1)`을 얻는다. `u -> 2/u`와 `u -> -2/u`를 합성하면 `u -> -u`가
된다. `l>3`에서는 두 금지 잉여류가 다르므로 각 행의 `l-1`개 항 중
`l-3`개가 남는다. `l=3`에서는 두 금지 잉여류가 두 단위를 모두 소진한다.

### 계산과 한계

`43` 이하 홀수 소수 `13`개에서 교차 Gram 항등식과 동시 생존 개수를
정확히 검사했다. 세 계산 범위의 세제곱근 인수 cell에서도 mod `3` 동시
생존자가 `0`임을 확인했다.

이는 제안된 결합 경로 하나에 대한 no-go 정리이지 쌍둥이 소수 하한이
아니다. 실제 `qr-2`, `qr+2` 소수 합은 별도로 추정해야 하며, 남아 있는
비상수 지표 mode에 균일한 power saving이 필요하다.

## 문헌 및 우선권 경계

- Connes와 Consani의 [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771)는 Weil 양성의 배경이다. RH-228은 유한 배율 안정성 장애만 증명한다.
- Lagarias의 [The 3x+1 problem: an overview](https://arxiv.org/abs/2111.02635)는 콜라츠 문제와 알려진 장벽을 정리한다. CO-228은 발산하는 비주기 궤도를 배제하지 않는다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 거의 모든 궤도 정리이지 모든 궤도 정리가 아니다.
- Helfgott의 [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)는 삼항 정리이며 강한 이항 골드바흐를 함의하지 않는다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)는 스칼라 국소 인수에 빠진 Type-I·Type-II 정보와 관련된다.
- Polymath의 [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897)는 bounded gap 정리이며 간격 `2`가 무한히 많다는 정리가 아니다.

디리클레 근사, 유한군 순열 연산자, Collatz 아핀 합성은 고전적 재료다.
PrimeProject는 이 재료의 문헌 우선권을 주장하지 않는다. 여기서 기록하는
기여는 정확한 결합, 증명 ledger, 실패 경로 감사, 재현 가능한 데이터다.
새로움에 대한 주장은 별도 문헌 조사와 동료 심사를 거쳐야 한다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket228_near_alias_affine_language_residue_spectrum.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket228_near_alias_affine_language_residue_spectrum -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

기계 판독 결과:

- `data/open-problem/ticket228-near-alias-affine-language-residue-spectrum.json`
- `data/open-problem/riemann/rh-ticket-228-finite-dilation-near-alias.json`
- `data/open-problem/collatz/co-ticket-228-branching-affine-language.json`
- `data/open-problem/goldbach/gb-ticket-228-moving-residue-spectrum.json`
- `data/open-problem/twin-prime/tp-ticket-228-shift-two-residue-spectrum.json`
