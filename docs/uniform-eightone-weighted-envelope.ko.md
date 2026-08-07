# TICKET-192: 균일 확장, 8-1 콜라츠 주기, 가중 오염 상계

## 1. 주장 경계

TICKET-192는 네 개의 중간 정리를 증명하지만 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 해결하지 않는다. 네
상위 추측의 반례도 발견하지 않았다. 이번에 새로 완전히 닫은 무한 가족은
가속 콜라츠 valuation word에서 정확히 여덟 항이 1이고 나머지가 모두 2인
모든 주기다.

| 문제 | 이번에 증명한 정확 결과 | 폐기하거나 후순위로 내린 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `UniformBoundedCoreExtensionAndPointwiseCauchyNoGo` | 균일 연속성 상계 없이 조밀 코어의 점별 수렴만 승격하는 경로 | `PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreWithUniformAdmissibleNormBound` |
| 콜라츠 | `ExactlyEightValuationOnesOtherwiseTwoCycleExclusion` | 모든 순환 회전을 중복 계산하고 곱 상계 이후에도 열거하는 경로 | `NoContractingValuationWordWithExactlyNineOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction` | 지수 가중치를 버린 개수 기반 예산을 주 목표로 삼는 경로 | `BinaryVonMangoldtCorrelationExceedsWeightedPrimePowerEnvelopeForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `LocalTwoSidedWeightedEnvelopeBridge` | 두 국소 평행이동 구간만 오염시키는데 전역 개수 예산을 사용하는 경로 | `ShiftTwoCorrelationExceedsLocalWeightedPrimePowerEnvelopeOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket192_uniform_eightone_weighted_envelope.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket192_uniform_eightone_weighted_envelope -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

통합 기계 판독 결과는
`data/open-problem/ticket192-uniform-eightone-weighted-envelope.json`에 있다.
네 시도는 모두 `open_not_proven`, 즉 미증명 상태이며 해결 수는 `0 / 4`다.

## 2. 리만 가설

### 2.1 이번에 선언한 명제

복소 Hilbert 공간 `H`에서 `D`가 조밀하고 `q`가 `D` 위 Hermitian 이차형식이라고
하자. `q`가 `H` 전체의 유계 Hermitian 형식으로 유일하게 확장될 필요충분조건은
어떤 유한한 상수 `C`가 존재하여

```text
|q(x)| <= C ||x||^2                    (x in D)
```

가 성립하는 것이다. `D`에서 `q>=0`이면 확장된 형식도 양이다. 반면 가산 조밀
코어에서 유한 절단값이 각 점마다 Cauchy 수열이라는 사실만으로는 연속 확장을
결론낼 수 없다.

### 2.2 증명과 정확한 no-go

유계 확장이 있으면 위 부등식은 제한을 통해 즉시 나온다. 역으로 복소 편극
항등식으로 sesquilinear 형식 `B`를 복원하고 한 인자를 재조정하면

```text
|B(x,y)| <= 2 C ||x|| ||y||
```

를 얻는다. 따라서 `B`는 조밀성에 의해 `H` 전체로 유일하게 연속 확장된다.
양성도 연속성으로 전달된다.

점별 수렴만으로 충분하다는 경로의 반례는 `H=l^2`, `D=c_00`에서

```text
q_N(x) = sum_(k<=N) k |x_k|^2
```

이다. 모든 유한 지지 벡터에서는 결국 값이 고정되고 모든 `q_N`은 양이다.
그러나 극한은 `q(e_k)=k`이므로 하나의 유한 유계 상수가 존재하지 않는다.
생성 데이터는 절단 norm `2,4,8,16,32,64`의 증가를 재현한다.

### 2.3 남은 증명 간극

이 정리는 필요한 위상을 정확히 분리했을 뿐 실제 pole-neutral Weil 이차형식의
수렴이나 균일 admissible norm 상계를 증명하지 않는다. 다음 보조정리는 가우스
유리수 코어의 스칼라 수렴과 하나의 균일 norm 상계를 동시에 제공해야 한다.
최근 screw-function 연구도 결정적 극한 연산자를 추측으로 제시한다:
[Suzuki 2026](https://arxiv.org/abs/2606.09096).

## 3. 콜라츠 추측

### 3.1 이번에 선언한 명제

가속 콜라츠 양의 주기 중 정확히 여덟 valuation이 `v_i=1`이고 나머지가 모두
`v_i=2`인 주기는 원시·비원시 여부와 무관하게 존재하지 않는다.

### 3.2 전 범위 증명

길이 `h`인 word의 총 valuation은 `2h-8`이며 주기 방정식의 분모는

```text
D = 2^(2h-8) - 3^h
```

이다. `h<20`에서는 `D<=0`이므로 양의 주기가 불가능하다. `20<=h<=30`에서는
여덟 개의 1 중 하나가 처음에 오도록 word를 회전한다. 다음 항등식과 `D`의
홀수성 때문에 나눗셈 가능성은 회전에 불변이다.

```text
2^v B_shift = 3B + D
```

따라서 다음 개수만 검사하면 모든 순환 궤도를 포함한다.

```text
sum_(h=20)^30 C(h-1,7)
  = C(30,8)-C(19,8)
  = 5,777,343
```

정확한 정수 계산에서 `D|B` hit는 0개다. 각 horizon의 나머지 transcript에는
재현 가능한 SHA-256 해시를 기록했다.

이 층의 비자명한 양의 홀수 주기는 1을 포함할 수 없으므로 모든 값이 3 이상이다.
주기 전체를 곱하면

```text
1 <= 256 (5/6)^h
```

를 얻는다. `h=31`에서 우변은 정확히 `256*5^31/6^31<1`이며 이후 계속
감소한다. 따라서 `h>=31`도 모두 모순이고 전체 층이 닫힌다.

### 3.3 남은 증명 간극

1이 아홉 번 이상 나오는 valuation word, 3 이상의 valuation, 비주기 발산 궤도는
다루지 못했다. 최근 parity-vector 연구도 콜라츠 증명을 주장하지 않는다:
[Niu 2026](https://arxiv.org/abs/2605.13886).

## 4. 강한 골드바흐 추측

### 4.1 이번에 선언한 명제

다음 가중 proper-prime-power 질량을 정의한다.

```text
W_pp(X) = sum_(p^k<=X, k>=2) log p
```

이진 von Mangoldt 상관에서 적어도 한 항이 proper prime power인 오염량을
`E_pp(N)`이라 하면

```text
E_pp(N) <= 2 log(N) W_pp(N)
```

이다. `A(N)`이 `N` 이하 proper prime power의 개수라면

```text
W_pp(N) <= A(N) log(N)/2,
E_pp(N) <= A(N)(log N)^2.
```

따라서 TICKET-191의 대응 count-based 충분 예산에서 계수 2를 제거할 수 있다.

### 4.2 증명과 유한 진단

오염된 순서쌍을 왼쪽 또는 오른쪽 proper prime power에 부과한다. 상대 항의
von Mangoldt 가중치는 최대 `log N`이다. 또 `q=p^k`, `k>=2`이면
`log p=log(q)/k<=log(N)/2`이므로 두 부등식이 성립한다.

결국

```text
R_Lambda(N) > 2 log(N) W_pp(N)
```

이면 소수-소수 질량이 양수이고 골드바흐 표현이 존재한다. `64`부터
`1,048,576`까지의 표본 8개는 모두 새 상계를 넘었다. 이것은 유한 재현 진단일
뿐 모든 짝수에 대한 정리가 아니다.

### 4.3 남은 증명 간극

모든 충분히 큰 짝수 `N`에서 위 엄격 부등식을 증명하지 못했다. 예외집합 연구는
이 모든-대상 이진 정량자를 제공하지 않는다:
[Grimmelt–Teravainen 2025](https://arxiv.org/abs/2508.16400).

## 5. 쌍둥이 소수 추측

### 5.1 이번에 선언한 명제

이진 블록 `[X,2X)`의 shift-two von Mangoldt 상관을 `S_2(X)`라고 하자.
proper-prime-power 오염량은 다음 국소 상계 이하이다.

```text
U_2(X) = log(2X+2) [
  W_pp([X,2X)) + W_pp([X+2,2X+2))
]
```

따라서 `S_2(X)>U_2(X)`이면 해당 블록에 쌍둥이 소수가 있다. 이 국소 가중
상계 역시 앞선 전역 count 예산의 계수 2 이상을 제거한다.

### 5.2 증명과 유한 진단

오염 항에서는 `n` 또는 `n+2`가 proper prime power다. 이를 각각 위 두 구간에
부과하면 상대 가중치는 최대 `log(2X+2)`이므로 상계가 나온다. 전체 상관에서
이 상계를 빼고도 양수이면 남는 소수-소수 항이 존재한다.

정확한 유한 재현은 `j=4,...,19`의 16개 블록을 다루며 모두 충분 부등식을
통과한다. 이들은 이미 쌍둥이 소수가 있는 유한 블록이므로 무한성에 대한 논증은
아니다.

### 5.3 남은 증명 간극

무한히 많은 무한대 방향 이진 블록에서 충분 부등식이 성립함을 증명해야 한다.
유계 소수 간격 정리는 정확한 간격 2를 강제하지 않는다:
[Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07),
[Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. 문제 간 결론

두 소수 상관 트랙에 공통으로 도입한 객체는 가중 proper-prime-power 질량
`W_pp`다. 단순 개수 예산이 버리던 실제 von Mangoldt 가중치를 유지하여 더
작고 국소적인 충분 목표를 만든다. 네 트랙에 공통으로 남은 장애물은 유한 계산이
제공하지 못하는 무한 균일성이다. 즉 형식의 균일 상계, 더 큰 valuation 층,
모든 짝수의 상관 초과, 무한히 많은 블록의 shift 초과가 각각 남아 있다.
