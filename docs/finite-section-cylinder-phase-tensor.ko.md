# TICKET-173: finite-section 결손, 콜라츠 cylinder 안정화, 골드바흐 target 위상, tensor-Haar scale pair

## 초록

TICKET-173은 TICKET-172가 남긴 네 OPEN 노드를 이어간다. 이번 결과는
정확한 구조 정리 네 개와 명시적 no-go 네 개다. 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 해결하지 않았다.

리만 트랙은 조밀한 finite section의 음의 하한 결손이 0으로 수렴하면 전역
비음성이 배제된다는 정리를 증명한다. 양의 compact 대각 연산자는 uniform
spectral gap이 필요조건이 아님을 보인다. 콜라츠 트랙은 모든 valuation
cylinder의 최소대표를 정확한 모듈러 식으로 계산하고, 양의 자연수 지지가
최소대표의 eventual stabilization과 동치임을 증명한다. all-one cylinder는
지평선 길이만 사용하는 subexponential 높이 경로를 폐기한다. 골드바흐
트랙은 target에 정렬된 Fourier 양·음 기여를 보존하며, 음의 budget 조건이
필요조건은 아님을 비음수 가중 반례로 증명한다. 쌍둥이 소수 트랙은 행과
열의 Haar scale이 서로 독립이라는 점을 복원하고, same-scale 혼합 변동만
제어하는 경로를 rank-one 반례로 폐기한다.

| 문제 | TICKET-173 정확 결과 | 상태 | 폐기 경로 | 다음 단일 보조정리 |
|---|---|---|---|---|
| 리만 | 조밀한 finite-section 하한 결손 정리 | `open_not_proven` | uniform 양의 gap을 필요조건으로 요구 | `PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero` |
| 콜라츠 | 자연수 지지와 cylinder 대표 안정화의 동치 | `open_not_proven` | 지평선 기반 subexponential 높이 | `EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives` |
| 골드바흐 | target 정렬 부호 spectrum 양성 인증 | `open_not_proven` | 음의 budget이 anchor보다 작아야 한다는 필요조건 | `UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit` |
| 쌍둥이 소수 | 2-매개변수 tensor-Haar 에너지 완전성 | `open_not_proven` | same-scale 변동만으로 완전한 Type-II 제어 | `PrimePairMatrixAllScalePairHaarEnergyPowerSaving` |

## 1. 주장 경계

- `proved_exact`: 표시한 함수해석·모듈러·Fourier·Haar 명제를 완전히 증명했다.
- `refuted_or_insufficient`: 명시적 반례가 제안된 함의를 깨거나 조건이
  불필요하게 강함을 보였다.
- `open_not_proven`: 난제를 닫는 산술 추정은 아직 없다.

유한 계산은 식과 구현을 감사하는 도구다. 무한 범위로 외삽하지 않는다.

## 2. 리만 트랙: uniform coercivity 대신 0으로 가는 하한 결손

### 2.1 정확 명제

연속 Hermitian form `q`와 조밀한 합집합을 갖는 중첩 부분공간 `V_N`을
생각하자. `A_N`은 `V_N`의 orthonormal basis에서 쓴 `q|V_N`의 정확한
행렬이고 계산 행렬 `Atilde_N`이

\[
\|A_N-\widetilde A_N\|\leq\rho_N,
\quad
\lambda_{\min}(\widetilde A_N)-\rho_N\geq-\eta_N,
\quad
\eta_N\to0
\]

을 만족하면 `q>=0`이다. 연속 constraint map `B:H->R^r`는 한 finite
section에서 full row rank가 인증되면 모든 더 큰 중첩 domain에서도 그
rank가 유지된다.

### 2.2 증명

`v in V_M`을 고정하면 모든 `N>=M`에 대해

\[
q(v)\geq-\eta_N\|v\|^2
\]

이다. `N`을 무한대로 보내면 `q(v)>=0`이고, 연속성과 조밀성으로 전체
Hilbert 공간에 확장된다. 더 큰 domain의 `B` 범위는 이미 전사인 작은
domain의 범위를 포함한다.

### 2.3 uniform-gap no-go

`l2`에서 `Qe_j=e_j/j`라 하자. 모든 비영 벡터에 대해 `<Qv,v>>0`이지만
첫 `N`개 좌표 제한의 최소 고윳값은 `1/N`이다. 따라서 N과 무관한 양의
gap은 단순 비음성보다 강한 coercivity 조건이다. Weil positivity의
필요조건으로 요구할 수 없다.

계산 감사는 `Atilde_N=A_N-(1/N)I`를 사용해 인증 하한 `-1/N`이 정확히
0으로 접근함을 재현한다.

### 2.4 남은 간극

실제 pole-neutral Guinand-Weil 조밀 코어에서 `eta_N->0`을 인증하지
못했다. 대각 연산자 모델은 closure 논리를 검증할 뿐 zeta zero를
배제하지 않는다.

## 3. 콜라츠 트랙: 자연수 지지는 cross-scale 안정화다

### 3.1 정확 명제

accelerated odd valuation word `w=(a_1,...,a_H)`에 대해

\[
S=\sum a_j,
\qquad
2^S T^H(n)=3^Hn+C(w)
\]

라 하자. 이 word를 실현하는 홀수 residue는 modulo `2^(S+1)`에서
정확히 하나이며

\[
r_w\equiv(2^S-C(w))3^{-H}\pmod{2^{S+1}}
\]

이다. 무한 ray의 최소 양의 대표들은 서로 중첩된다. 이 ray가 하나의
양의 자연수 궤도에서 나올 필요충분조건은 대표들이 bounded인 것이며,
이는 eventual stabilization과 동치다.

### 3.2 증명

endpoint가 홀수라는 조건은

\[
3^Hn+C(w)\equiv2^S\pmod{2^{S+1}}
\]

이다. `3`은 2의 거듭제곱 modulo에서 가역이므로 residue가 유일하다.
affine identity를 각 prefix modulo로 줄이면 필요한 `2^(S_j)` 나눗셈이
나오고, 남은 nonempty suffix의 affine constant가 홀수이므로 각 prefix
quotient도 홀수다. 따라서 지정한 valuation이 모두 정확하다. word를
연장하면 이전 residue class를 세분하므로 대표는 compatible하다. 증가하는
2의 거듭제곱 modulo에서 bounded compatible 대표는 결국 더 이상 이동할
수 없다. 반대로 자연수 시작값 `n`은 modulus가 `n`보다 커진 순간부터
최소대표가 된다.

### 3.3 높이 no-go

길이 `H`의 all-one word는

\[
r_H=2^{H+1}-1
\]

을 최소대표로 가진다. 첫 `H`단계는 모두 시작값 이상이다. 따라서 모든
비하강 cylinder를 `H`만으로 덮는 보편 높이 bound는 최소한 지수적이어야
한다. valuation `{1,2,3,4}`의 길이 6 이하 word `5,460`개와 `H=64`까지의
all-one 정확식을 검사했다.

이 반례군은 서로 다른 유한 자연수들의 모음이다. 하나의 발산 궤도가 아니다.

### 3.4 남은 간극

이제 결정적 명제는 분명하다. 모든 무한 prefixwise non-descending ray의
cylinder 대표가 unbounded임을 보여야 한다. stabilization 정리에 의해
이 명제는 양의 자연수 지지를 배제한다. 이번 TICKET은 이를 증명하지 않았다.

## 4. 골드바흐 트랙: target 정렬 양·음 Fourier 질량

### 4.1 정확 명제

`f>=0` on `Z/q`, 비정규화 Fourier transform을 `F`라 하고

\[
c_k(n)=q^{-1}\Re(F(k)^2e(kn/q))
\]

라 하자. 비영 주파수의 양·음 부분을 `P(n),N(n)`이라 하면

\[
(f*f)(n)=F(0)^2/q+P(n)-N(n).
\]

따라서 `F(0)^2/q>N(n)`은 엄밀한 target별 양성 인증이다. 위상을 버린
전체 L1 하한보다 약하지 않다.

### 4.2 정확한 필요성 no-go

`Z/8`에서

\[
f=(0,0,0,0,0,0,1,2)
\]

를 사용하자. target `4`의 convolution은 `1`이다. zero-mode anchor는
`9/8`이지만 음의 target-aligned budget은 `(1+sqrt(2))/2`로 더 크다.
비교는 `4sqrt(2)>5`, 즉 제곱 후 `32>25`로 끝난다. 인증 gate는
실패하지만 양의 주파수 기여가 실제 값을 1로 복원한다. 음의 budget만
anchor 아래로 누르는 조건은 충분조건이지 필요조건이 아니다.

### 4.3 실제 소수 유한 진단

소수 support `64,128,256,512,1024`에 zero padding을 적용해 cyclic
wraparound를 제거했다. 총 `987`개 짝수 target에서 Fourier 재구성과 ordered
prime-pair count가 일치하고 모두 양수였다. 하지만 음의-budget gate는 단
한 target만 통과했다. 이는 gate가 지나치게 강하다는 유한 증거이지
골드바흐 증명이 아니다.

### 4.4 남은 간극

모든 충분히 큰 짝수에 대해 양의 major-arc 질량이 signed minor-arc deficit을
지배한다는 target-uniform 정리가 필요하다. exceptional-set 결과만으로는
모든 target의 점별 양성이 자동으로 나오지 않는다.

## 5. 쌍둥이 소수 트랙: 두 scale index가 필요하다

### 5.1 정확 명제

완전한 직교 discrete Haar basis를 `H_N`이라 하고 `C=H_N A H_N^T`라 하자.
`A`의 모든 행·열 합이 0이면 constant Haar vector를 포함하는 coefficient는
모두 0이고

\[
\|A\|_F^2=\sum_{j,k\geq1}E_{j,k}
\]

이다. row scale `j`와 column scale `k`는 독립이다.

### 5.2 same-scale no-go

서로 다른 scale의 정규화 Haar wavelet `u,v`를 잡고 `A=uv^T`라 하자.
모든 행·열 합은 0이고 operator/Frobenius norm은 1이다. Haar transform에는
서로 다른 scale pair의 coefficient 하나만 남는다. 모든 same-scale
`E_(j,j)`는 0이지만 전체 Type-II 에너지는 1이다. 이 구조는 모든 dyadic
`N>=4`에서 성립하며 계산은 `N=4,...,64`를 재현한다.

TICKET-161의 `4x4` 행렬도 네 scale pair로 다시 분해했다. 이는 유한
좌표 분석이지 소수쌍의 점근 감쇠가 아니다.

### 5.3 남은 간극

TICKET-172의 same-scale 혼합 차분 항등식은 정확하지만 전체 Type-II
인증으로는 불완전했다. 수정된 목표는 sieve 범위의 모든 row/column scale
pair에 대해 prime-producing 상수와 power saving을 증명하는 것이다.

## 6. 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket173_finite_section_cylinder_phase_tensor.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket173_finite_section_cylinder_phase_tensor -v
```

주 기계 판독 산출물은
`data/open-problem/ticket173-finite-section-cylinder-phase-tensor.json`이다.

## 7. 문헌 경계

- Connes와 Consani, *The Scaling Hamiltonian*, [arXiv:1910.14368](https://arxiv.org/abs/1910.14368): Weil positivity와 pole-neutral 문맥.
- Groskin, *A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form*, [arXiv:2607.02828](https://arxiv.org/abs/2607.02828): RH 주장이 없는 finite Galerkin/tail-budget 문맥.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, [arXiv:1909.03562](https://arxiv.org/abs/1909.03562): every-orbit가 아닌 almost-all 로그 밀도 결과.
- Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, [arXiv:2605.13886](https://arxiv.org/abs/2605.13886): 명시적 non-claim 경계를 둔 유한 parity-vector 결과.
- Grimmelt와 Bhowmik, *The exceptional set of the Goldbach problem*, [arXiv:2607.27282](https://arxiv.org/abs/2607.27282): 명시적 major-arc와 exceptional-set 문맥.
- Ford와 Maynard, *On the theory of prime producing sieves*, [arXiv:2407.14368](https://arxiv.org/abs/2407.14368): 실질적인 Type-I/II 정보의 필요성.

조밀 코어 closure, 모듈러 cylinder 식, Fourier inversion, tensor-Haar
Parseval 항등식 자체에 대한 신규성이나 우선권은 주장하지 않는다. 이번
TICKET의 기여는 검증 가능한 keep/discard 판정과 수정된 증명 의무다.
