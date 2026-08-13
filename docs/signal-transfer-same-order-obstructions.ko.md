# TICKET-226: 신호 전달과 같은 차수 방해항

English edition: [signal-transfer-same-order-obstructions.md](signal-transfer-same-order-obstructions.md)

## 초록과 주장 경계

TICKET-226은 TICKET-225가 남긴 네 후속 경로가 실제로 성립할 수 있는지
검사한다. 네 개의 더 좁은 정리 또는 불가능성 정리를 증명했지만, 리만
가설·콜라츠 추측·강한 골드바흐 추측·쌍둥이 소수 추측 중 어느 것도
해결하지 않았다.

| 문제 | TICKET-226에서 확립한 결과 | 폐기·교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | 실제 소수 band는 음·양 커널 질량이 각각 `-1/4`, `+1/4`인 Chebyshev 오차의 균형 contrast다 | band 부호를 곧바로 Weil 양성으로 해석 | `ExplicitFormulaControlOfBalancedChebyshevBandsOnDenseWeilCore` |
| 콜라츠 추측 | 무한 원시족 `(1,1,3)^r,2`는 비순환이지만 모든 순환 intercept가 `D`보다 크다 | 모든 비순환 word가 `min B_i<D`로 인증된다는 경로 | `NoNontrivialPrimitiveValuationWordSatisfiesDDividesB` |
| 강한 골드바흐 | 세제곱근 거친 반소수는 `S_z(X)~log(2)X/log X`로 소수와 같은 차수다 | 반소수 오염을 낮은 차수의 주변분포 오차로 처리 | `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly` |
| 쌍둥이 소수 | 같은 주변분포 방해가 존재하며, 유한 gap-two 자료에서도 오염 `<PP`가 두 범위에서 실패한다 | Type-I 주변분포만으로 shifted pair를 분리 | `ShiftedCubeRootParityTypeIIBilinearPowerSavingOnUnboundedBlocks` |

공통 결론은 **신호 전달**에 관한 것이다. 계산 가능한 관측량이 정확해도
증명에 필요한 양성 구조와 부호 구조가 다를 수 있다. 오차의 산술 형태를
정확히 분류해도 그 오차가 목표 신호와 같은 점근 차수라면 단순 희소성으로
제거할 수 없다.

## 1. 리만 가설

### 명제 RH-226

다음을 정의하자.

```text
psi(x) = sum_(n<=x) Lambda(n),
E(x)   = psi(x)-x,
P(a)   = sum_(n>=2) Lambda(n)[exp(-an)-exp(-2an)]-1/(2a).
```

모든 `a>0`에서

```text
P(a) = a integral_0^infinity E(x)[exp(-ax)-2exp(-2ax)] dx.   (RH-226.1)
```

`u=ax`로 두면 커널 `k(u)=exp(-u)-2exp(-2u)`는 `u=log 2`에서 부호가
바뀐다. 음·양 구간의 적분은 정확히

```text
integral_0^log(2) k(u) du = -1/4,
integral_log(2)^infinity k(u) du = +1/4.                     (RH-226.2)
```

이다. 따라서 `P(a)`는 Chebyshev 오차의 두 영역을 비교하는 전체 질량
0의 대조량이다. 양의 함수에 대한 양의 선형 범함수가 아니므로, 그 부호를
Weil 양성으로 바로 읽을 수 없다.

### 증명

Stieltjes 부분적분으로 `c>0`일 때

```text
sum Lambda(n)exp(-can) = ca integral_0^infinity psi(x)exp(-cax) dx
```

를 얻는다. `c=1,2`를 대입해 빼고 `psi=x+E`를 사용하면
`(RH-226.1)`이 나온다. `k`의 원시함수
`-exp(-u)+exp(-2u)`를 `0`, `log 2`, 무한대에 대입하면
`(RH-226.2)`가 증명된다.

### 재현 계산과 한계

실제 von Mangoldt 소수 거듭제곱을 사용해 `a=2^-j`, `j=3,...,13`인
11개 scale을 계산했다. cutoff는 `48/a`다. 직접 소수 합과 Chebyshev
커널 항등식의 차이는 모두 `10^-12` 미만이며, TICKET-225의 명시적
꼬리 상계를 더한 뒤에도 11개 음의 부호가 유지된다.

이 계산은 관측량을 해석하지만 RH 기준으로 승격하지 않는다. 전체 band
profile은 특정 측도 공간에서 정보를 보존할 수 있으나, 이를 조밀한 Weil
핵의 양성으로 옮기는 균일한 명시공식 추정은 아직 없다.

## 2. 콜라츠 추측

### 명제 CO-226

모든 정수 `r>=1`에 대해

```text
w_r = (1,1,3)^r,2
```

를 정의한다. 이 word는 원시적이다. affine 분모와 가장 작은 순환
intercept는

```text
D_r = 4*32^r-3*27^r,
B_r = (62*32^r-57*27^r)/5.                                  (CO-226.1)
```

이며 모든 순환 intercept가 `B_r` 이상이다. 또한

```text
D_r < B_r < 4D_r,
D_r는 B_r를 나누지 않는다.                                (CO-226.2)
```

따라서 모든 `w_r`는 비순환이지만 어느 것도 `min_i B_i<D` 검사로는
인증되지 않는다. TICKET-225의 최소-intercept 검사는 충분조건일 뿐
필요조건이 아니다.

### 증명

마지막 지수 `2`가 정확히 한 번만 나타나므로 비자명 주기를 가질 수 없다.
블록 `U=(1,1,3)`의 affine 자료는 `(27,32,19)`다. `U^r` 뒤에 마지막
지수를 연결하면 `(CO-226.1)`을 얻는다.

`n_0=B_r/D_r`라 두면

```text
B_r-D_r       = 42(32^r-27^r)/5 > 0,
19D_r-5B_r    = 14*32^r > 0
```

이므로 `1<n_0<19/5`다. 각 `U` 안의 첫 두 가속 단계는 값을 증가시키고,
전체 블록은 `n -> (27n+19)/32`로 작용한다. 이 함수는 `n<19/5`에서
값을 증가시키면서 같은 구간을 보존한다. 따라서 `n_0`가 가장 작은 순환
상태이고 `B_r`가 최소 intercept다.

`1<B_r/D_r<4`이므로 정수라면 `2` 또는 `3`이어야 한다. 두 경우는 각각

```text
22*32^r = 27*27^r,
2*32^r  = 12*27^r
```

를 요구하지만 소인수분해의 유일성에 모순이다. 따라서 `D_r`는 `B_r`를
나누지 않으며 cycle이 아니다.

### 재현 계산과 한계

`r=1,...,40`의 모든 회전을 검사했고, 높이 `121`까지 선택한 행을 JSON에
저장했다. 유한 계산은 위의 모든-`r` 증명을 회귀 검사하는 역할만 한다.

이 정리는 콜라츠 반례를 만들지 않았고 모든 비자명 cycle도 배제하지
않았다. 최소 크기 경로 하나를 폐기했으며, 정확한 `D|B` 배제와 비주기
자연수 궤도의 하강은 별도 과제로 남는다.

## 3. 강한 골드바흐 추측

### 명제 GB-226

`z=X^(1/3)`라 하고, `z<p<=q`인 소수의 곱 `pq<=X`의 개수를
`S_z(X)`라 하자. 그러면

```text
S_z(X) = sum_(z<p<=sqrt(X)) [pi(X/p)-pi(p-1)]                (GB-226.1)
```

이고 소수정리(PNT)에 의해

```text
S_z(X) ~ (log 2) X/log X,
S_z(X)/pi(X) -> log 2.                                      (GB-226.2)
```

즉 세제곱근 거친 반소수는 소수와 같은 주변분포 점근 차수다. additive
correlation을 분석하기 전에 `o(P)` 오차로 버릴 수 없다.

### 증명

각 거친 반소수는 더 작은 소인수 `p`가 유일하므로 `(GB-226.1)`이
성립한다. `pi(p-1)`의 총 기여는 `O(X/log^2 X)`다. 나머지 합에 PNT와
소수 부분합을 적용하고 `t=X^u`로 치환하면

```text
S_z(X)
  ~ (X/log X) integral_(1/3)^(1/2) du/[u(1-u)]
  = (log 2)X/log X
```

를 얻는다.

### 유한 경로 반례

TICKET-225의 정확한 분해에서 `E=PS+SP+SS`라 두면 다음과 같다.

| `N` | `PP` | `E` | `E/PP` | `E<PP` |
|---:|---:|---:|---:|---:|
| 10,000 | 254 | 270 | 1.063 | 거짓 |
| 100,000 | 1,620 | 1,812 | 1.119 | 거짓 |
| 1,000,000 | 10,804 | 14,882 | 1.377 | 거짓 |

모든 행에서 `PP>0`이다. 이것은 강한 지배 조건의 반례이지 골드바흐의
반례가 아니다. 또한 PNT 결과는 한 변수 주변분포 정리이므로 모든 짝수에
대한 pointwise convolution 점근식을 주지 않는다. 유지할 경로는 희소성이
아니라 원방법의 주호·부호 오차 사이에서 산술적 상쇄를 증명하는 것이다.

## 4. 쌍둥이 소수 추측

### 명제 TP-226

`(GB-226.2)`의 주변분포 정리는 TICKET-225의 gap-two endpoint에도
적용된다. 따라서 Type-I 주변분포만으로 `PS`, `SP`, `SS`를 낮은 차수로
만들 수 없다. 단, 이것으로 shifted pair 개수의 점근식을 얻었다고
주장하지 않는다. 그 단계에는 Type-II 상관 정보가 필요하다.

완전 유한 분류 결과는 다음과 같다.

| `X` | `PP` | `PS+SP+SS` | 오염/`PP` | 오염 `<PP` |
|---:|---:|---:|---:|---:|
| 10,000 | 205 | 189 | 0.922 | 참 |
| 100,000 | 1,224 | 1,349 | 1.102 | 거짓 |
| 1,000,000 | 8,169 | 11,135 | 1.363 | 거짓 |

유한 pair 지배조차 두 큰 범위에서 실패하지만 쌍둥이 소수 `PP`는 많이
남아 있다. 이 표는 무한성을 증명하지 않는다. 다음 보조정리는 무한히
커지는 block에서 실제 shifted Type-II bilinear power saving을 요구한다.

## 네 트랙의 결론

TICKET-226이 확정한 경로 교정은 다음과 같다.

1. RH에는 균형 contrast의 부호가 아니라 그 전체 profile을 옮기는 정리가
   필요하다.
2. Collatz의 최소-intercept 하강은 보편 비순환 판정이 아니다.
3. Goldbach의 거친 반소수 오염은 소수 신호와 같은 주변분포 차수다.
4. Twin 분리는 Type-I 주변분포가 아니라 shifted Type-II 정보를 요구한다.

이는 탐색 공간을 줄인 부분정리와 불가능성 정리다. 네 상위 추측에 대한
완전한 증명 또는 반례는 아니다.

## 문헌 경계

- Connes와 Consani의 [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)은 semi-local 명시공식과 Weil 양성의 배경이다. 여기의 균형 커널 항등식은 그 논문의 RH 기준이 아니다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 거의 모든 궤도에 대한 정리이며 모든 궤도 문제는 남긴다.
- Helfgott의 [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)은 원방법의 1차 문헌이지만 강한 이항 골드바흐를 증명하지 않는다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)는 소수 생성 하한에 실질적인 Type-II 정보가 필요한 이유를 제공한다.
- Polymath의 [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897)는 bounded gap과 exact-gap parity 경계의 1차 문헌이다.

초등 커널 계산, 명시적 Collatz 무한족, PNT의 거친 반소수 계수 적용에
대해 문헌 최초성을 주장하지 않는다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket226_signal_transfer_same_order_obstructions.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket226_signal_transfer_same_order_obstructions -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

주 기계 판독 산출물:

`data/open-problem/ticket226-signal-transfer-same-order-obstructions.json`
