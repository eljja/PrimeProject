# TICKET-196: Rouché 소진, 콜라츠 밀도, 중복 보정 소수 거듭제곱 예산

## 초록

TICKET-196은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 계속 공격한다. 그러나 **어느 모가설도 해결하지 않았다.**
이번 티켓은 증명 탐색의 방향을 교정하는 네 개의 정확한 결과를 확립한다.

1. entire function의 Taylor 절단에 대한 소진형 무영점 Rouché 인증은
   그 함수의 모든 영점이 실수라는 명제와 동치다. 따라서 이전 RH 목표는
   더 약한 중간 보조정리가 아니었다.
2. `{1,2}` 콜라츠 valuation word에 적용한 두 스칼라 부등식은
   `(h,r)=(3k,k)`라는 무한 후보 프로필을 남긴다.
3. 골드바흐의 proper-prime-power 오염에서 `(Q*Q)(N)` 중복을 정확히 뺄
   수 있다.
4. 쌍둥이 소수 shift-two 오염에서도 `sum Q(n)Q(n+2)` 중복을 정확히
   뺄 수 있다.

네 문제 상태는 모두 `open_not_proven`이다. 기계 판독 결과는
[`ticket196-rouche-density-overlap.json`](../data/open-problem/ticket196-rouche-density-overlap.json)에 있다.

## 주장 경계

| 문제 | 이번 티켓에서 증명한 것 | 증명하지 못한 것 |
|---|---|---|
| 리만 가설 | Rouché 소진 조건과 전 영점 실수성의 동치 | 실제 Xi 인증, RH, 비임계선 영점 |
| 콜라츠 | 스칼라 밀도 no-go와 무한 생존 count-profile | affine divisibility, 비자명 순환, 전역 수렴 |
| 골드바흐 | 정확 inclusion-exclusion과 더 작은 오염 상계 | 모든 큰 짝수의 상관 하한 |
| 쌍둥이 소수 | 정확 shift-two inclusion-exclusion과 더 작은 국소 상계 | 무한히 많은 블록의 parity-breaking 하한 |

아래 유한 계산은 항등식과 반례를 검사한다. 유한 성공을 무한 명제로
승격하지 않는다.

## 1. 리만 가설 트랙

### 1.1 선언 명제

`F`를 실수 entire function, `S_n`을 Taylor 절단이라 하자. `m>=2`에 대해

```text
D_m^+ = { z : |Re z| < m, 1/m < Im z < m },
D_m^- = conjugate(D_m^+)
```

로 둔다. 다음 두 명제는 동치다.

1. `F`의 모든 영점은 실수다.
2. 모든 `m`과 두 부호에 대해 어떤 `S_n`이 `D_m^sign` 안에서 영점 수
   0을 가지며 다음을 만족한다.

```text
sup_{boundary D_m^sign} |F-S_n|
  < inf_{boundary D_m^sign} |S_n|
```

따라서 Riemann Xi 함수에 대한 2번 조건은 RH와 동치다. 더 약한 중간
목표가 아니다.

### 1.2 증명

`F`의 모든 영점이 실수라고 하자. 각 off-real 사각형의 compact closure는
영점 집합과 만나지 않으므로

```text
delta_m = min_{closure D_m^sign}|F| > 0
```

이다. Taylor 절단은 compact 집합에서 균일 수렴한다. closure 전체에서
`sup|F-S_n|<delta_m/3`인 `n`을 택하면 `|S_n|>2delta_m/3`이다. 따라서
절단은 closure에서 무영점이고 strict Rouché 부등식이 성립한다.

반대로 각 인증은 `F`와 `S_n`의 사각형 내부 영점 수가 같고 0임을 준다.
이 사각형들의 합집합은 `C\R`이므로 `F`에는 비실수 영점이 없다.

### 1.3 재현 계산과 한계

`m=2,...,12`에서 다음 두 다항식을 비교한다.

- `F_real(z)=z^2-1`: 정확한 2차 절단이며 off-real 영점이 없고 경계에서
  `|F_real(z)|>=1/m^2`이다.
- `F_nonreal(z)=z^2+1`: `D_m^+`에 `i`, `D_m^-`에 `-i`가 있다.

이는 양화 구조를 검사하는 합성 예시다. 실제 Xi의 Taylor remainder나
영점 수는 계산하지 않았다.

### 1.4 경로 결정

- **폐기:** 완전한 Xi Rouché 소진 family를 더 약한 중간 보조정리라고
  부르는 경로.
- **유지:** 실제 Xi에 대해 bounded rational rectangle을 하나씩 interval
  방식으로 인증하는 경로.
- **다음 보조정리:**
  `ActualXiTaylorSectionHasCertifiedZeroCountOnFirstOffRealRationalRectangle`.

## 2. 콜라츠 트랙

### 2.1 선언 명제

양의 accelerated Collatz 순환이 `{1,2}`에 속하는 `h`개 valuation을 가지며
그중 정확히 `r`개가 1이라고 하자. TICKET-195의 수축 조건과 순환 곱
조건은

```text
log_2(6/5) <= r/h < 2-log_2(3)
```

을 강제한다. 이 구간에는 `1/3`이 들어 있다. 모든 `k>=1`에서
`(h,r)=(3k,k)`는 두 조건을 정확히 통과한다.

```text
2^(2h-r)=2^(5k)=32^k>27^k=3^h,
2^r(5/6)^h=(125/108)^k>1.
```

따라서 두 스칼라 부등식만으로 모든 `{1,2}` cycle word를 배제할 수 없다.

### 2.2 증명과 계산

두 부등식에 base-two logarithm을 취하면 밀도 구간이 나온다. 위 정수
부등식은 수치 근사 없이 무한 프로필 family가 살아남음을 보인다. 생성기는
`k=1,...,64`를 재생하고 프로필마다 첫 좌표를 1로 고정한 선형 word가
`C(3k-1,k-1)`개임을 기록하며 정확 정수를 해시한다. 이 수를 순환 회전
동치류의 개수라고 주장하지 않는다.

이 프로필은 순환이 아니다. 계산은 의도적으로
`affine_divisibility_verified=false`를 기록한다. 순서 의존 affine numerator와
양의 정수 고정점 조건이 남아 있다.

### 2.3 경로 결정

- **폐기:** 수축·곱 밀도 조건만으로 모든 `{1,2}` word를 닫는 경로.
- **유지:** 정확 밀도 구간 안에서 순서에 민감한 divisibility obstruction을
  균일하게 증명하는 경로.
- **다음 보조정리:**
  `UniformAffineDivisibilityObstructionForOneTwoWordsInTheAdmissibleDensityWindow`.

## 3. 강한 골드바흐 트랙

### 3.1 선언 명제

홀수에서 von Mangoldt support를

```text
Lambda_o=P+Q
```

로 나눈다. `P`는 홀수 소수, `Q`는 홀수 proper prime power에 지지된다.
짝수 `N`에서 `(Lambda_o*Lambda_o)(N)` 중 적어도 한 좌표가 `Q`인 가중
오염을 `E_o(N)`이라 하면

```text
E_o(N)=2(Q*Lambda_o)(N)-(Q*Q)(N)
```

이다. `W_Q(N)=sum_{q<N}Q(q)`라 하면 TICKET-195 상계는 정확히 다음처럼
개선된다.

```text
E(N) <= 2 log(N)W_Q(N) - (Q*Q)(N) + B_2(N)
```

`B_2(N)`은 TICKET-194의 정확한 2의 거듭제곱 항이다.

### 3.2 증명과 반례

`(P+Q)^2-P^2`을 전개하면 `PQ+QP+Q^2`이다. convolution의 교환법칙을
쓰면 `2Q(P+Q)-Q^2`이다. 이전 union bound는 `Q^2`을 두 번 청구했으므로
한 번 빼야 정확하다. 상대 von Mangoldt weight는 `log N` 이하이므로 위
상계가 따른다.

중복 청구의 정확한 반례는

```text
18=9+9=3^2+3^2
```

이며 양의 overlap weight는 `(log 3)^2`이다. `18,34,52`와 `2^6`부터
`2^20`까지 18개 target에서 support 분해, inclusion-exclusion, parity 분해,
보정 상계를 재생한다.

### 3.3 경로 결정

- **폐기:** 왼쪽과 오른쪽 proper-power 오염 청구가 서로 겹치지 않는다는
  가정.
- **유지:** 정확 overlap subtraction을 명시적 major/minor arc 부등식에
  삽입하는 경로.
- **다음 보조정리:**
  `ExplicitGoldbachMajorArcMainTermDominatesMinorArcAbsoluteErrorAndCollisionCorrectedContaminationForEveryLargeEvenTarget`.

## 4. 쌍둥이 소수 트랙

### 4.1 선언 명제

dyadic block `[X,2X)`에서 shift-two correlation의 정확 proper-power 오염은

```text
E_X = sum Q(n)Lambda(n+2)
    + sum Lambda(n)Q(n+2)
    - sum Q(n)Q(n+2)
    + E_X,even
```

이다. 따라서 국소 union envelope에서 정확한 `Q(n)Q(n+2)` collision
mass를 뺄 수 있다.

### 4.2 증명과 반례

`Lambda=P+Q`를 각 항에 대입하면 항등식이 나온다. 처음 두 합은 각 구간
`Q` mass에 `log(2X+2)`를 곱해 상계하고, `Q-Q` 중복은 정확히 빼며, 짝수
항은 정확히 유지한다.

중복 반례는

```text
(25,27)=(5^2,3^3) in [16,32)
```

이고 보정량은 `log(5)log(3)`이다. `2^4`부터 `2^20`까지 17개 dyadic
block에서 정확 항등식과 기준 상관을 재생한다.

### 4.3 경로 결정

- **폐기:** left-shift와 right-shift proper-power 청구가 서로 겹치지 않는다는
  가정.
- **유지:** 보정된 예산을 사용한 뒤 parity-sensitive 소수쌍 하한을 직접
  공격하는 경로.
- **다음 보조정리:**
  `ParityBreakingShiftTwoLowerBoundDominatesCollisionCorrectedContaminationOnInfinitelyManyDyadicBlocks`.

## 5. Proof DAG 요약

```text
TICKET-195 열린 목표
        |
        v
TICKET-196 정확 정리 ---- 폐기된 대체 명제
        |
        v
단일 다음 보조정리(open_not_proven)
```

문제별 JSON에 전체 node와 edge가 있다. 어떤 DAG도 모가설로 가는
`proved` 경로를 포함하지 않는다.

## 6. 재현 방법

```powershell
python scripts/ticket196_rouche_density_overlap.py
python -m unittest tests.test_ticket196_rouche_density_overlap
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

예상 기계 경계는 다음과 같다.

```text
정확 정리:                         4
Rouché 목표 동치:                  1
스칼라 밀도 no-go:                 1
중복 보정 오염 상계:               2
난제 해결:                         0
기계 실패:                         0
```

## 7. 학술 경계

- [Clay Mathematics Institute의 RH 명세](https://www.claymath.org/millennium/riemann-hypothesis/)가
  여전히 목표다. compact Taylor 수렴과 Rouché 정리는 고전적이며 새로운
  Xi estimate를 주장하지 않는다.
- Tao의 결과는 logarithmic density 의미의 almost-all 결과이지 전칭 수렴이
  아니다([arXiv:1909.03562](https://arxiv.org/abs/1909.03562)). 최근 parity-vector
  연구도 추측 해결을 주장하지 않는다
  ([arXiv:2605.13886](https://arxiv.org/abs/2605.13886)).
- 강한 골드바흐의 `4*10^18` 검증은 유한 검증이다
  ([Mathematics of Computation 83 (2014)](https://doi.org/10.1090/S0025-5718-2013-02787-1)).
- Maynard의 bounded-gap 정리는 정확한 간격 2를 증명하지 않는다
  ([Annals of Mathematics 181 (2015)](https://doi.org/10.4007/annals.2015.181.1.7)).

이번 티켓의 elementary equivalence와 inclusion-exclusion 항등식은 문헌
최초 주장 없이 프로젝트 내부 증명 경로 교정으로 제시한다.
