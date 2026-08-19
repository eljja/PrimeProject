# TICKET-230: 정량 재귀·목걸이 불변성·푸리에 합산·국소 중심화

## 주장 상태

**미해결, 증명되지 않음.** TICKET-230은 네 개의 정확한 구조 정리 또는
불가능성 정리(no-go theorem)를 증명했지만, 리만 가설·콜라츠 추측·강한
골드바흐 추측·쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다.
기계 판독 해결 수는 계속 `0 / 4`이다.

이번 티켓은 TICKET-229가 남긴 네 후속 보조정리의 목표가 올바른지부터
검사했다. 그중 “shift two에서 mod 5 이차 지표가 원시 값 그대로 0으로
상쇄된다”는 목표는 잘못 중심화되어 있었다. 올바른 국소 평균은 `0`이
아니라 `1/3`이다. 어려운 해석 추정을 시작하기 전에 목표 명제부터
교정했다는 점이 이번 반복의 핵심 방법론적 결과다.

## 재현 계약

- 생성기: `scripts/ticket230_quantitative_recurrence_necklace_fourier_centering.py`
- 검사: `tests/test_ticket230_quantitative_recurrence_necklace_fourier_centering.py`
- 통합 JSON: `data/open-problem/ticket230-quantitative-recurrence-necklace-fourier-centering.json`
- 상태: `open_not_proven`(미증명 공개 문제)
- 정확한 부분정리·불가능성 정리: `4`
- 폐기 또는 교정한 경로: `4`
- 해결한 상위 추측: `0`
- 기계 검사 실패: `0`

## 1. 리만 가설 트랙

### 이번에 선언한 정확한 명제

`q_1,...,q_m > 1`을 고정된 정수라 하자. `m >= 2`이고 그중 적어도 두
수가 곱셈적으로 독립이라고 하자. 다음 배율 위상 에너지를 정의한다.

\[
F(t)=\sum_{j=1}^m |1-q_j^{-it}|^2.
\]

모든 정수 `Q >= 2`에 대해 어떤 정수 `1 <= n <= Q^m`이 존재하여

\[
F(n)\le \frac{4\pi^2m}{Q^2}
\]

를 만족한다. 이 증인들에는 무한히 커지는 부분수열이 있으며, 그
부분수열에서는

\[
F(n)\le4\pi^2m\,n^{-2/m}
\]

이다. 따라서 고정된 유한 배율 족에는 `t^(2/m)L(t) -> infinity`를
만족하는 전역 하한 바닥 `L(t)`가 존재할 수 없다.

### 증명

`m`차원 토러스를 한 변 길이가 `1/Q`인 `Q^m`개 상자로 나눈다. 다음
`Q^m+1`개 점을 넣는다.

\[
k\left(\frac{\log q_1}{2\pi},\ldots,\frac{\log q_m}{2\pi}\right)\pmod1,
\qquad0\le k\le Q^m.
\]

비둘기집 원리에 의해 두 점이 같은 상자에 들어간다. 두 첨자의 차를
`n`이라 하면 모든 위상 거리가 `1/Q` 이하이다. 또한

\[
|1-e^{-2\pi ix}|^2=4\sin^2(\pi x)\le4\pi^2\|x\|^2
\]

이므로 에너지 상계가 나온다. `Q`가 커져도 증인이 유한 집합에만
머문다면 하나의 양의 정수 `n`에서 에너지가 정확히 0이어야 한다. 이는
두 독립 정수의 로그 비가 유리수라는 모순을 만든다. 마지막으로
`n <= Q^m`에서 `Q^(-2) <= n^(-2/m)`가 따른다.

### 새로 확정한 것과 한계

기존의 정성적 근접 에일리어스(near alias) 결과를 명시적 다항 속도로
강화했다. 따라서 “준지수적(subexponential) 손실”이라는 말만으로는
충분하지 않으며, 실제 프레임 하한과 Weil 핵 절단 꼬리를 피할 수 없는
재귀 속도와 직접 비교해야 한다.

그러나 Weil 양성, 무한 가중 프레임, 실제 Weil 핵 꼬리 상계는 증명하지
않았다. 리만 가설은 미해결이다.

**폐기:** `T^(-2/m)`보다 느리게 감소하는 고정 유한 족의 전역 하한.

**다음 단일 보조정리:**
`AdaptiveInfiniteDilationFrameWithWeilTailDominanceBelowRecurrenceScale`
(재귀 척도보다 작은 Weil 꼬리를 지배하는 적응형 무한 배율 프레임).

## 2. 콜라츠 추측 트랙

### 이번에 선언한 정확한 명제

가속 홀수 콜라츠 valuation word(2로 나누는 횟수 열)
`a=(a_0,...,a_(h-1))`에 대해

\[
S=\sum_j a_j,\qquad D=2^S-3^h
\]

및

\[
B(a)=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}}
\]

를 정의한다. `rho(a)`를 한 칸 왼쪽 순환 회전이라 하면

\[
2^{a_0}B(\rho a)=3B(a)+D
\]

이다. `D>0`이면

\[
\gcd(D,B(\rho a))=\gcd(D,B(a))
\]

이며 `D | B(rho a)`와 `D | B(a)`는 동치다.

### 증명

`B(a)=3^(h-1)+2^(a_0)C`로 첫 항을 분리한다. 회전된 분자를 전개하면
`B(rho a)=3C+2^(S-a_0)`이다. 양변에 `2^(a_0)`을 곱하면
`3B(a)+2^S-3^h=3B(a)+D`가 된다. `D`는 홀수이고,
`D = 2^S (mod 3)`이므로 `3`과도 서로소다. 따라서 `2^(a_0)`와 `3`은
modulo `D`에서 역원이 있어 최대공약수와 나눗셈 가능성이 보존된다.

### 새로 확정한 것과 한계

순환 조건 `D|B`는 word 자체가 아니라 순환 회전 동치류인 목걸이
(necklace)의 불변량이다. 같은 word의 모든 회전을 별개의 증거로 세면
중복이다. 유한 검사는 알파벳 `{1,...,5}`의 원시 양의 분모 word를 높이
6까지 확인했고, 높이 6의 `15,402`개 word를 `2,567`개 목걸이 대표로
줄였으며 항등식 실패는 없었다.

이 계산은 모든 원시 목걸이에서 `D`가 `B`를 나누지 못한다는 증명이
아니다. 그 전역 비나눗셈 정리를 증명하더라도 비주기 발산 궤적을 따로
배제해야 한다.

**폐기:** 한 word의 순환 회전을 독립적인 순환 검사로 세는 방식.

**다음 단일 보조정리:**
`NecklaceRepresentativeNondivisibilityForEveryPrimitivePositiveDenominatorWord`
(모든 원시 양의 분모 word의 목걸이 대표에 대한 비나눗셈).

## 3. 강한 골드바흐 추측 트랙

### 이번에 선언한 정확한 명제

푸리에 모드 각각의 상대 크기가 0으로 가는 것만으로는 차원이 커지는
순환군의 점별 합성곱 양성을 얻을 수 없다. `L=m^2`이고 `Z/LZ`에서

\[
w_m(x)=1+m\,1_{x=a}
\]

로 두자. 전체 질량은 `W=m^2+m`이고 모든 비주 지표 푸리에 계수의
절댓값은 `m`이다. 따라서

\[
\max_{k\ne0}\frac{|\widehat w_m(k)|}{W}=\frac1{m+1}\to0.
\]

하지만 목표 `2a`에서는

\[
(w_m*w_m)(2a)=2m^2+2m,
\qquad\frac{W^2}{L}=m^2+2m+1
\]

이며, 목표 위상에 정렬된 비주 성분 오차는 `m^2-1`이다. 이는 주항과
같은 차수다.

### 증명

상수 배경의 비영 주파수 푸리에 변환은 0이다. spike는
`m exp(-2 pi i k a/L)`를 준다. 목표가 `2a`이면 이 계수의 제곱과 역변환
위상이 모든 `k`에서 정확히 상쇄되어 `L-1`개 비주 모드가 같은 방향으로
정렬된다. 합은 `m^2(L-1)/L=m^2-1`이다. 직접 합성곱 전개도 같은 값을
준다.

### 새로 확정한 것과 한계

이것은 골드바흐 반례가 아니라 잘못된 추론 규칙의 반례다. 모드 수가
함께 늘어날 때 각 모드에 대한 별도의 `o(W)` 상계는 부호와 목표 위상이
정렬된 전체 합을 제어하지 못한다. 실제 소수 가중 문제에는 주호·부호
구간(major/minor arcs) 분해와 목표 정렬 합 전체에 대한 상계가 필요하다.

여기서 만든 가중치는 소수 가중치가 아니다. 이 결과는 이항 소수
합성곱의 점별 하한을 주지 않는다.

**폐기:** 성장하는 모든 모드의 개별 상계만으로 점별 골드바흐 양성을
결론내리는 방식.

**다음 단일 보조정리:**
`UniformBinaryPrimeMinorArcSignedAggregateBelowSingularSeriesMainTerm`
(이항 소수 minor arc의 부호 있는 전체 합이 singular series 주항보다
작다는 균일 정리).

## 4. 쌍둥이 소수 추측 트랙

### 이번에 선언한 정확한 명제

`l`을 홀수 소수, `h != 0 (mod l)`라 하고, `chi(0)=0`으로 확장한 비주
곱셈 지표 `chi`를 잡는다. shift `h`의 허용 시작 잉여류 집합을

\[
A=\{r\pmod l:r\ne0,\ r+h\ne0\}
\]

라 하면

\[
\sum_{r\in A}\chi(r)=-\chi(-h),
\qquad
\frac1{|A|}\sum_{r\in A}\chi(r)=\frac{-\chi(-h)}{l-2}.
\]

`l=5`, `h=2`, 이차 지표인 경우 `A={1,2,4}`이고 원시 평균은 `1/3`이다.

### 증명

허용 집합은 완전 잉여류계에서 `0`과 `-h`를 제거한 것이다. 비주 곱셈
지표의 완전 합은 0이고 `chi(0)=0`이므로 `-h`를 제거하고 남는 합은
`-chi(-h)`이다. mod 5에서 `1,2,4`의 이차 지표 값은 `1,-1,1`이다.

### 새로 확정한 것과 한계

TICKET-229는 full-size mod 5 이차 모드가 남는다는 점을 정확히 찾았지만,
후속 목표는 원시 평균을 0으로 잘못 잡았다. 올바른 관측량은 이차 지표에서
국소 평균 `1/3`을 뺀 중심화 관측량이다. `10^6` 이하 쌍둥이 소수 유한
표본은 허용 잉여류만 확인하는 계산이며 점근 분포 증명이 아니다.

이 국소 항등식은 쌍둥이 소수가 무한히 많음을 보이지 않고 체의 parity
barrier(짝홀 장벽)도 넘지 않는다. 양의 주성분 하한도 별도로 필요하다.

**폐기:** 원시 mod 5 이차 지표가 0으로 상쇄된다는 목표.

**다음 단일 보조정리:**
`CenteredModFiveQuadraticTypeIISavingAtTwinSieveMainScale`
(쌍둥이 체 주척도에서 중심화한 mod 5 이차 지표의 Type-II 절약).

## 증명 DAG 요약

| 문제 | TICKET-230에서 확정 | 폐기·교정 | 가장 위험한 미증명 보조정리 | 상위 상태 |
|---|---|---|---|---|
| 리만 | 유한 배율의 정량 재귀 | `T^(-2/m)`보다 느린 유한 족 하한 | Weil 꼬리와 맞는 적응형·무한 프레임 | 미해결 |
| 콜라츠 | `D|B`, `gcd(D,B)`의 목걸이 불변성 | 회전을 독립 증거로 계산 | 모든 원시 양의 분모 목걸이의 비나눗셈 | 미해결 |
| 골드바흐 | 정렬 푸리에 반례족 | 모드별 `o(W)`에서 점별 양성 추론 | singular-series 주항보다 작은 부호 있는 minor-arc 전체 합 | 미해결 |
| 쌍둥이 소수 | 허용 지표 평균의 정확식 | raw mod-5 평균 0 | 중심화 Type-II 절약과 양의 주항 | 미해결 |

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket230_quantitative_recurrence_necklace_fourier_centering.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket230_quantitative_recurrence_necklace_fourier_centering -v
```

## 학술 우선권과 참고 경계

이번 티켓은 고전 도구와 PrimeProject 내부의 경로 감사를 결합한다.
동시 디리클레 근사, 콜라츠 순환 분자, 순환 푸리에 역변환, 국소 지표 합
자체에 대한 학술적 최초성을 주장하지 않는다. 새로운 프로젝트 산출물은
이 네 결과를 하나의 검증 계약과 proof DAG로 연결하고 잘못된 후속 목표를
교정한 것이다.

- Connes·Consani, [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771): Weil 양성과 trace formula의 연구 맥락.
- Lagarias, [The 3x+1 problem: an annotated bibliography](https://arxiv.org/abs/math/0309224), [Part II](https://arxiv.org/abs/math/0608208): 콜라츠 문제와 순환 연구의 문헌 경계.
- Helfgott, [The ternary Goldbach conjecture is true](https://arxiv.org/abs/1312.7748): 원 방법과 소수 지수합 맥락. 이 결과는 강한 이항 골드바흐를 해결하지 않는다.
- Maynard, [Small gaps between primes](https://arxiv.org/abs/1311.4600): 유계 소수 간격과 정확한 간격 2 추측의 차이.
