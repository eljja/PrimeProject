# TICKET-193: 전 공간 수렴, 9-1 콜라츠 주기, parity 오염 상계

## 1. 주장 경계

TICKET-193은 네 개의 중간 정리를 증명하지만 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 해결하지 않는다. 네
상위 추측의 반례도 발견하지 않았다. 이번에 완전히 닫은 새 무한 가족은
가속 콜라츠 valuation word에서 정확히 아홉 항이 1이고 나머지가 모두 2인
모든 주기다.

| 문제 | 이번에 증명한 정확 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension` | 조밀 코어의 점별 수렴만으로 Banach-Steinhaus를 적용하는 경로 | `PoleNeutralWeilFiniteSectionsConvergeOnEveryVectorOfACompleteAdmissibleHilbertCompletion` |
| 콜라츠 | `ExactlyNineValuationOnesOtherwiseTwoCycleExclusion` | 52,157,326개 word의 pairwise 열거 | `NoContractingValuationWordWithExactlyTenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `ParitySeparatedPrimePowerContaminationEnvelope` | 2의 거듭제곱까지 모두 `log N` union bound로 부과하는 경로 | `BinaryCorrelationExceedsParitySeparatedPrimePowerEnvelopeForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `OddOnlyShiftTwoContaminationEnvelope` | `X>=4`인 shift-2 블록의 오염에 2의 거듭제곱을 포함하는 경로 | `ShiftTwoCorrelationExceedsOddLocalWeightedEnvelopeOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket193_everywhere_nineone_parity_envelope.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket193_everywhere_nineone_parity_envelope -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

통합 기계 판독 결과는
`data/open-problem/ticket193-everywhere-nineone-parity-envelope.json`에 있다.
네 시도는 모두 `open_not_proven`이며 해결 수는 `0 / 4`다.

## 2. 리만 가설

### 2.1 선언 명제

복소 Hilbert 공간 `H`에서 `q_n`을 연속 Hermitian 이차형식이라 하고 연관
Hermitian 형식을 `B_n`이라 하자. 모든 `x in H`에 대해 `q_n(x)`가 수렴하면

```text
sup_n ||B_n|| < infinity
```

이며 모든 `x,y in H`에서 `B_n(x,y)`가 수렴한다. 그 극한 `B`는 유계
Hermitian 형식이고 `B(x,x)=lim_n q_n(x)`이다. 모든 `q_n`이 양이면 극한도
양이다.

### 2.2 증명

복소 편극 항등식은 `q_n(x+i^k y)` 네 값으로 `B_n(x,y)`를 복원한다. 따라서
대각값이 모든 벡터에서 수렴하면 `B_n(x,y)`도 모든 `x,y`에서 수렴하고 특히
점별 유계다.

`x`를 고정하면 `y -> B_n(x,y)`는 유계 선형 functional의 점별 유계
가족이다. 첫 번째 uniform boundedness principle, 즉 Banach-Steinhaus 정리로

```text
sup_n ||B_n(x, .)|| < infinity
```

를 얻는다. Riesz 표현으로 `B_n(x,y)=<T_n x,y>`라 쓰면 모든 `x`에 대해
`sup_n ||T_n x||<infinity`다. 두 번째 Banach-Steinhaus 적용으로
`sup_n ||T_n||<infinity`가 된다. 따라서 점별 극한형식은 하나의 공통 상수로
유계이고 Hermitian 성질과 양성은 극한으로 전달된다.

### 2.3 조밀 코어만으로 부족하다는 정확한 no-go

`H=l^2`, `D=c_00`에서

```text
q_n(x)=n|x_n|^2
```

로 둔다. 모든 유한 지지 벡터에는 결국 `q_n(x)=0`이므로 `D`에서는 0으로
수렴하지만 `||B_n||=n`이다. 이 실패가 완비공간 바깥의 형식적 현상이 아님은

```text
x_(2^j)=sqrt(j/2^j),  x_n=0 otherwise
```

로 확인된다. `sum_j j/2^j=2`이므로 `x in l^2`지만
`q_(2^j)(x)=j`는 발산한다.

### 2.4 남은 간극

실제 pole-neutral Weil finite section이 하나의 완비 admissible Hilbert
completion의 **모든** 벡터에서 수렴한다는 정리를 증명하지 못했다. 조밀한
Gaussian-rational core의 수렴만으로는 이번 정리를 적용할 수 없다. 최근
screw-function 연산자 연구에서도 결정적 극한 연산자는 추측 단계다:
[Suzuki 2026](https://arxiv.org/abs/2606.09096).

## 3. 콜라츠 추측

### 3.1 선언 명제

가속 콜라츠 양의 주기 중 정확히 아홉 valuation이 `v_i=1`이고 나머지가 모두
`v_i=2`인 주기는 원시·비원시 여부와 무관하게 존재하지 않는다.

### 3.2 수축 범위와 아핀 분해

길이 `h`인 word의 총 valuation은 `2h-9`이고 주기 방정식의 분모는

```text
D_h=2^(2h-9)-3^h.
```

`h<=21`에서는 `D_h<=0`이므로 양의 주기가 없다. `h>=22`에서는 아홉 개의
1 중 하나가 첫 위치에 오도록 회전한다. `D_h`가 홀수이고

```text
2^v B_shift = 3B + D_h
```

이므로 `D_h|B` 여부는 순환 회전에 불변이다.

정규화 위치를 `0=p_0<p_1<...<p_8<h`라 하자. 다음 prefix를 정의한다.

```text
P_r(t)=sum_(0<=j<t, 2j>=r) 3^(h-1-j) 2^(2j-r)
C_h=3^(h-1)+P_9(h)-P_1(1)
d_i(p)=P_i(p+1)-P_(i+1)(p+1).
```

기존 recurrence로 계산한 아핀 분자는 정확히

```text
B_h(p_1,...,p_8)=C_h+sum_(i=1)^8 d_i(p_i)
```

이다. 이 등식은 `h=9,...,15`의 모든 정규화 word에서 기존 recurrence와
독립 대조했다.

### 3.3 4+4 meet-in-the-middle 완전성

왼쪽 residue를

```text
C_h+d_1(p_1)+...+d_4(p_4) mod D_h
```

로 저장한다. 오른쪽 첫 위치 `p_5=c`를 처리할 때 `p_4<c`인 왼쪽 tuple만
활성화하고

```text
-(d_5(p_5)+...+d_8(p_8)) mod D_h
```

가 활성 residue 집합에 있는지 검사한다. Python 정수와 집합 membership은
정확하므로 부동소수점 허용오차가 없다.

각 오른쪽 tuple이 대표하는 왼쪽 tuple 수는 `C(c-1,4)`이고 전체 포괄 수는

```text
sum_(h=22)^34 C(h-1,8)
  = C(34,9)-C(21,9)
  = 52,157,326.
```

모든 residue 조회에서 hit는 0개였다. 각 horizon의 조회 transcript에는
SHA-256을 기록했다. 이것은 무작위 표본이 아니라 해당 유한 범위의 완전
결정 절차다.

### 3.4 무한 꼬리

비자명한 양의 홀수 주기는 1을 포함하지 않으므로 모든 상태가 3 이상이다.
주기 전체를 곱하면

```text
1 <= 512(5/6)^h.
```

우변은 `h=34`에서 1보다 크지만 `h=35`에서 1보다 작고 이후 감소한다. 따라서
`h>=35`도 모두 모순이다. 이로써 9-one/rest-two 층 전체가 닫힌다.

### 3.5 남은 간극

1이 열 번 이상 나오는 valuation word, 3 이상의 valuation, 비주기 발산은
다루지 못했다. 최근 가속 map 연구도 전역 Collatz 증명을 제공하지 않는다:
[Niu 2026](https://arxiv.org/abs/2605.13886).

## 4. 강한 골드바흐 추측

### 4.1 선언 명제

`W_odd(N)`을 `N` 이하의 홀수 proper prime power `p^k`, `k>=2`에 대한
`log p`의 합으로 정의한다. `C_2(N)`은

```text
2^a+2^b=N,  a,b>=1, max(a,b)>=2
```

인 ordered pair가 주는 정확한 von Mangoldt 질량이다. 그러면 짝수 `N>=6`의
proper-prime-power 오염량은

```text
E_pp(N) <= 2 log(N) W_odd(N) + C_2(N),
C_2(N) <= 2(log 2)^2.
```

### 4.2 parity 분리 증명

짝수의 두 합항은 같은 parity다. von Mangoldt support를 가진 짝수는 2의
거듭제곱뿐이다. 따라서 짝수-짝수 오염은 `C_2(N)`에 정확히 들어간다. 두
거듭제곱의 합의 이진 표현은 ordered 해를 최대 두 개만 허용한다.

나머지 오염쌍은 적어도 한 좌표가 홀수 proper prime power다. 그 좌표에
오염을 부과하면 상대 가중치는 최대 `log N`이고 좌우 두 위치 때문에 첫
부등식이 나온다. 이는 모든 2의 거듭제곱을 `log N`으로 과대 부과하던
TICKET-192 상계보다 작거나 같다.

### 4.3 prime-base 압축

`y=floor(sqrt N)`라 하자. 홀수 소수 `p<=y`에 대해 가능한 지수의 최댓값을
`K=floor(log_p N)`라 하면 그 base의 전체 질량은

```text
(K-1)log p <= log N-log p.
```

따라서 Chebyshev 함수 표기로

```text
W_odd(N)
 <= (pi(y)-1)log N-(theta(y)-log 2)
 <= sqrt(N)log N.
```

즉 새 parity 상계는 명시적으로 `O(sqrt(N)log^2 N)`이다. `2^10`부터
`2^20`까지의 11개 유한 표본은 모두 새 상계를 넘었지만 이는 모든 짝수에
대한 정리가 아니다.

### 4.4 남은 간극

모든 충분히 큰 짝수에서 이진 von Mangoldt 상관이
`2log(N)W_odd(N)+C_2(N)`을 넘는다는 점별 하한이 필요하다. 예외집합 정리는
이 모든-대상 정량자를 제공하지 않는다:
[Grimmelt–Teravainen 2025](https://arxiv.org/abs/2508.16400).

## 5. 쌍둥이 소수 추측

### 5.1 선언 명제

`X>=4`이고 `X<=n<2X`일 때, `n`과 `n+2`가 모두 von Mangoldt support에
있다면 둘은 반드시 홀수다. 따라서 shift-two proper-prime-power 오염량은

```text
log(2X+2) [
  W_odd([X,2X)) + W_odd([X+2,2X+2))
]
```

이하이다. 전체 shift-two 상관이 이 odd-only 국소 상계를 넘으면 해당 블록에
쌍둥이 소수가 있다.

### 5.2 짝수 support 배제

짝수 support pair가 있다면 `n=2^a`, `n+2=2^b`이고

```text
2^a(2^(b-a)-1)=2.
```

따라서 `a=1`이고 유일한 pair는 `{2,4}`다. 그러나 `X>=4`이면 `n>=4`이므로
이 pair는 블록에 들어오지 않는다. 모든 실제 support pair는 odd-odd이고,
오염은 홀수 proper prime power에만 부과할 수 있다.

`j=4,...,19`의 16개 이진 블록은 모두 새 odd-only 상계를 넘었다. 이 유한
성공은 무한히 많은 성공 블록을 뜻하지 않는다.

### 5.3 남은 간극

무한히 많은 이진 블록에서 shift-two 상관이 odd-only 상계를 넘음을 증명해야
한다. 유계 소수 간격은 정확한 간격 2를 강제하지 않는다:
[Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07),
[Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. 결론

이번 티켓의 공통 원리는 **필요한 전역 구조를 정확히 지정하는 것**이다.
리만 트랙에서는 조밀성이 아니라 완비공간 전체의 점별 수렴이 균일 유계성을
만들고, 두 소수 상관 트랙에서는 전체 prime-power 집합이 아니라 parity와
호환되는 홀수 부분만 오염시킨다. Collatz 트랙에서는 52,157,326개 pairwise
검사를 8개 경계항의 저차원 residue 문제로 바꾸되 조합적 포괄 범위는 줄이지
않았다. 이 세 개선 모두 상위 네 추측의 남은 무한 정량자를 제거하지는 않는다.
