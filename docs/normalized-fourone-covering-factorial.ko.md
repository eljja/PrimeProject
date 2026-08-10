# TICKET-209: 정규화 경계, 네 개의 valuation-1, 덮개 합동식, factorial 쌍둥이 부재 구간

## 주장 상태

네 상위 추측은 모두 `open_not_proven`, 즉 미해결 상태입니다. TICKET-209는
정확한 부분정리 또는 불가능성 정리 네 건을 증명하지만 리만 가설, 콜라츠
추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 가운데 어느 것도 증명하거나
반증하지 않습니다.

표준 기계 판독 파일은
[`ticket209-normalized-fourone-covering-factorial.json`](../data/open-problem/ticket209-normalized-fourone-covering-factorial.json)입니다.

| 문제 | 이번에 확정한 결과 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 | 무한히 높아지는 전체 경계에서 완성 제타 `xi`의 절댓값에 높이와 무관한 양의 여유를 줄 수 없음을 증명하고, 감마 정규화 뒤 외곽 경계를 분리 | 미해결 | 균일한 절대 `xi` 여유 | 정규화된 중앙 위쪽 경계의 비소멸 | `CofinalGammaNormalizedCentralTopEdgeNonvanishingCertificate` |
| 콜라츠 | valuation-1이 정확히 네 개인 모든 가속 주기를 배제 | 미해결 | 정확히 네-1인 전체 주기 층 | 다섯 개 이상인 주기와 비주기 발산 | `UniformExclusionForPrimitiveValuationNecklacesWithExactlyFiveOnes` |
| 골드바흐 | 어떤 절대상수 `c>0`과 무한히 커지는 짝수 수열에서 `W(N)>c log N log log N`; 따라서 `W(N)/log N`의 상극한은 무한대 | 미해결 | 상수배 로그로 최소 증인을 항상 덮는 주장 | 새 덮개 바닥 너머의 예외 꼬리 상계 | `GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor` |
| 쌍둥이 소수 | 임의 길이 factorial 구간에서 순환 위상 나머지가 정확히 `R_I=-H` | 미해결 | 모든 구간에서 양의 위상 여유 | 평균 또는 선택된 dyadic 구간의 독립 하한 | `IndependentBilinearOmegaPhaseLowerBoundOnInfinitelyManyDyadicIntervals` |

이 결과들은 고전 정리들을 조합해 프로젝트 안에서 명시적으로 증명한
명제입니다. 학술적 신규성이나 우선권은 독립적인 전문가 문헌 검토 전에는
주장하지 않습니다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

완성 제타함수를 다음과 같이 씁니다.

```text
xi(s) = (1/2)s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)
```

무한히 커지는 직사각형 `[-1,2] x [-T,T]`의 전체 경계에서 항상
`|xi(s)|>=epsilon`을 만족하는, 높이와 무관한 고정 `epsilon>0`은 존재할 수
없습니다. 이미 오른쪽 위 끝점에서

```text
|xi(2+iT)| <= U(T) -> 0,

U(T) = zeta(2)/(2 pi)
       sqrt((T^2+4)(T^2+1))
       sqrt((pi T/2)/sinh(pi T/2))
```

이기 때문입니다.

반면 영점을 만들지 않는 다항식과 감마 인자를 제거하면

```text
2 pi^(s/2) xi(s) / (s(s-1) Gamma(s/2)) = zeta(s),
|zeta(2+it)| >= zeta(4)/zeta(2) = pi^2/15
```

이라는 높이와 무관한 산술적 하한이 남습니다. 따라서 완성 제타함수의 절대
크기가 아니라 감마 정규화 뒤의 비소멸을 추적해야 합니다.

### 증명

`s=2+iT`에서 `|zeta(s)|<=zeta(2)`이고,

```text
|s(s-1)| = sqrt((T^2+4)(T^2+1)),
|Gamma(1+iT/2)|^2 = pi(T/2)/sinh(pi T/2)
```

입니다. 첫 항은 다항식 속도로 증가하지만 감마 항은 본질적으로
`exp(-pi T/4)`로 감소하므로 전체 상계는 0으로 갑니다. 모든 위쪽 경계는
`2+iT`를 포함하므로 고정된 양의 절대 여유는 불가능합니다.

정규화한 몫은 정확히 `zeta(s)`입니다. `Re(s)=2`에서는 절대수렴하는 오일러
곱으로 `|zeta(2+it)|>=pi^2/15`를 얻습니다. 임의의 고정 `delta>0`에 대해
`Re(s)>=1+delta`인 위쪽 외곽은 오일러 곱으로 영점이 없고,
`xi(s)=xi(1-s)`가 `Re(s)<=-delta` 외곽도 처리합니다. `delta=1/4`로 두면
프로젝트의 초등적 환원에서 남는 구간은 `-1/4<=Re(s)<=5/4`입니다.

### 한계

이 결과는 높이에 따라 작아지는 구간 인증서를 반박하지 않습니다. 중앙
수평변이 무한히 많은 높이에서 영점을 피한다는 것도 증명하지 않습니다.
비임계선 영점을 찾거나 리만 가설의 영점 개수를 전역적으로 세지 않았습니다.

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

홀수만 보는 가속 사상

```text
T(x)=(3x+1)/2^v2(3x+1)
```

에서 valuation 값 1이 정확히 네 번 나타나고 나머지가 모두 2 이상인 양의
비자명 주기는 존재하지 않습니다. TICKET-206부터 208까지의 결과와 합치면,
가상의 양의 비자명 주기는 valuation-1을 최소 다섯 개 포함해야 합니다.

### 무한 문제를 유한 문제로 줄이는 증명

가상 주기를 최소 홀수 `m>=3`에서 시작하도록 회전합니다. 첫 valuation은
반드시 1이고 마지막 valuation은 2 이상입니다. 길이를 `h`, valuation 합을
`A`라 하면 주기를 한 바퀴 곱해서

```text
2^A = product_i (3+1/x_i) <= (10/3)^h
```

를 얻습니다. 1이 정확히 네 개이면 `A>=2h-4`입니다. `h=16`에서

```text
2^28 3^16 = 11555266180939776 > 10^16
```

이고 길이가 하나 늘 때 왼쪽과 오른쪽의 비율은 `6/5`배가 되므로 모든
`h>=16`이 배제됩니다.

`5<=h<=15`에서는 같은 부등식이 `A`를 유한 범위로 제한합니다. 최소점
회전을 고정한 뒤 남는 valuation 단어는 정확히 2,292개입니다. 각 단어의
affine 합성을 유리수로 정확히 계산했으며 양의 홀수 정수 고정점은 0개입니다.

| `h` | 최소 `A` | 최대 `A` | 단어 수 | 양의 홀수 정수 고정점 |
|---:|---:|---:|---:|---:|
| 5 | 6 | 8 | 3 | 0 |
| 6 | 8 | 10 | 24 | 0 |
| 7 | 10 | 12 | 100 | 0 |
| 8 | 12 | 13 | 100 | 0 |
| 9 | 14 | 15 | 210 | 0 |
| 10 | 16 | 17 | 392 | 0 |
| 11 | 18 | 19 | 672 | 0 |
| 12 | 20 | 20 | 120 | 0 |
| 13 | 22 | 22 | 165 | 0 |
| 14 | 24 | 24 | 220 | 0 |
| 15 | 26 | 26 | 286 | 0 |

### 한계

이 정리는 하나의 주기 층만 완전히 닫습니다. valuation-1이 다섯 개 이상인
주기와 비주기 발산 궤도는 여전히 열려 있습니다.

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

`N-p`도 소수가 되는 가장 작은 소수 `p`를 `W(N)`이라 하고, 표현이 없으면
`W(N)=infinity`로 둡니다. 어떤 절대상수 `c>0`과 무한히 커지는 짝수 수열이
존재해

```text
W(N) > c log N log log N
```

을 만족합니다. 따라서

```text
limsup_(N even) W(N)/log N = infinity
```

입니다.

### 탐욕 덮개와 CRT 증명

큰 `B`에 대해 `z=floor(B/(log B)^2)`로 둡니다. 처음에는 `B` 이하의 모든
홀수 소수를 후보로 둡니다. 각 홀수 소수 `q<=z`마다 아직 덮이지 않은 후보가
가장 많이 들어 있는 잔여류 `r_q mod q`를 선택합니다. 한 단계 뒤 남는 후보
비율은 최대 `1-1/q`이므로 Mertens 곱 정리와 소수정리에서

```text
S <= pi(B) product_(3<=q<=z) (1-1/q)
  = O(B/(log B log z))
```

개의 후보만 남습니다.

남은 각 소수 `p`에 `(B,2B)` 안의 서로 다른 소수 `Q_p`를 하나씩 배정합니다.
그 뒤 중국인의 나머지 정리(CRT)로

```text
N = 0   (mod 2),
N = r_q (mod q),
N = p   (mod Q_p)
```

를 동시에 만족시킵니다. 전체 모듈러스 곱을 `M`이라 할 때 `M<N<=2M`인 짝수
대표를 선택하면 모든 소수 `p<=B`에 대해 `N-p`가 진합성수가 됩니다. 따라서
`W(N)>B`입니다. 또한

```text
log M <= theta(z) + S log(2B) = O(B/log B)
```

이므로 어떤 절대상수 `c>0`에 대해 `B>=c log N log log N`을 얻습니다.

### 한계

구성은 `p<=B`만 막습니다. 더 큰 소수가 골드바흐 표현을 만들 수 있으므로
반례가 아닙니다. 전체 예외집합의 크기도 상계하지 않습니다. 이 결과는
“최소 증인은 항상 `C log N` 이하”라는 지나치게 강한 경로를 폐기하고, 그보다
높은 바닥 너머의 꼬리 정리가 필요함을 확정합니다.

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

모든 `H>=1`에 대해 길이 `H`인 연속 구간 중 쌍둥이 소수의 아래쪽 후보가
하나도 없는 구간이 존재합니다. TICKET-208의 정확한 순환 필터 항등식

```text
M^2 T_I = H + R_I
```

에서 이 구간은 `T_I=0`, 따라서 `R_I=-H`를 만족합니다. 그러므로 모든
구간에서 `R_I>=-H+epsilon(H)`이고 `epsilon(H)>0`이라고 주장하는 방식은
불가능합니다.

### 증명

`K=H+3`, `N=K!`로 둡니다. `j=2,...,K-2`마다

```text
j     divides N+j,
j+2   divides N+j+2
```

입니다. 두 수는 표시한 약수보다 크므로 모두 합성수입니다. 이런 `j`가 정확히
`H`개 연속으로 있으므로 임의로 긴 쌍둥이 부재 구간을 얻습니다. 정확한 순환
필터 항등식에 `T_I=0`을 대입하면 `R_I=-H`입니다.

### 한계

factorial 구간은 위치에 비해 매우 짧고 쌍둥이 소수의 무한성을 다루는 확장
dyadic 구간이 아닙니다. 이 반례족은 모든 구간에서의 양성만 폐기합니다.
평균적인 위상 하한이나 선택된 무한 dyadic 구간의 하한은 여전히 가능하지만
증명되지 않았습니다.

## 재현 방법

```powershell
python scripts/ticket209_normalized_fourone_covering_factorial.py
python -m unittest tests.test_ticket209_normalized_fourone_covering_factorial -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

생성기는 통합 감사 JSON과 네 트랙별 JSON을 만듭니다. 테스트는 Collatz
2,292개 단어, 모든 Goldbach 덮개-CRT 나눗셈 인증, factorial 합성수 인증,
proof DAG와 `open_not_proven` 상태를 독립적으로 다시 검사합니다.

GitHub Pages를 가볍게 유지하기 위해 Goldbach JSON은 탐욕 덮개, 모든
생존자-강제소수 배정, 전체 인증 수와 SHA-256 transcript를 저장하고 이미
덮인 소수마다 같은 행을 반복하지 않습니다. 테스트가 생략된 모든 `p<=B`
나눗셈 인증을 다시 구성해 검증합니다.

## 문헌 및 우선권 경계

- 리만 가설의 공식 상태는 [Clay Mathematics Institute](https://www.claymath.org/millennium/riemann-hypothesis/)에서 확인할 수 있고, 감마함수 절댓값 항등식은 [NIST DLMF](https://dlmf.nist.gov/5.4.E3)에 정리되어 있습니다.
- Tao의 [거의 모든 Collatz 궤도 정리](https://doi.org/10.1017/fmp.2022.8)는 전칭 명제가 아니므로 모든 궤도의 하강을 주지 않습니다.
- 유한 골드바흐 검증은 [Oliveira e Silva, Herzog, Pardi](https://doi.org/10.1090/S0025-5718-2013-02787-1)에 정리되어 있지만 유한 검증은 전체 자연수 증명이 아닙니다.
- Maynard의 [유계 소수 간격 정리](https://doi.org/10.4007/annals.2015.181.1.7)는 간격 2를 강제하지 않습니다.

Collatz 층 배제와 Goldbach 덮개 형식의 정확성 및 문헌상 우선권은 정수론
전문가의 독립 검토 전까지 프로젝트 내부 결과로만 표시합니다.
