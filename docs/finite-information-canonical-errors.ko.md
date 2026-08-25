# TICKET-241: 유한 정보, 정규 오차 계약, 고정 밑수 탐색

## 주장 경계

TICKET-241은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았습니다**. 네 개의 정확한 정보 경계
정리를 증명하고, 유한 계산은 명시한 범위 안의 결과로만 기록합니다.
상위 난제 해결 수는 `0`입니다.

기계 판독 감사 파일:
`data/open-problem/ticket241-finite-information-canonical-errors.json`.

재현 및 검증:

```powershell
python scripts/ticket241_finite_information_canonical_errors.py
python -m unittest tests.test_ticket241_finite_information_canonical_errors -v
python scripts/verify_ticket241_structure.py
python scripts/verify_open_problem_structure.py
```

생성기는 `100,000,000` 이하의 모든 소수를 검사합니다. 테스트는 저장된
감사 결과를 읽고 작은 대수 인증서를 독립적으로 다시 검사합니다.

## 결과 요약

| 문제 | TICKET-241의 정확한 결과 | 폐기하거나 좁힌 경로 | 상태 |
|---|---|---|---|
| 리만 | 유한 무부호 소수 코사인 핵의 계수는 소수 지지 크기의 두 배 이하이며, 대각 양성은 강제로 남은 영공간에 인위적으로 삽입됨 | 유한 정규화 Gram 양성을 부호 있는 Weil 양성의 증거로 사용 | `open_not_proven` |
| 콜라츠 | 주단위원 대수는 나쁜 깊이 패턴을 허용하지만 실제 고정 밑수에서는 `10^8`까지 후보가 없음 | LTE 또는 국소 선형대수만으로 전 소수 깊이 지배를 증명 | `open_not_proven` |
| 골드바흐 | 부호 오차는 원래 표현수와 동치이고 절댓값 오차 인증은 고정된 분해와 노름에 의존 | 지정되지 않은 “모든 명시적 오차”를 안정적인 중간 목표로 사용 | `open_not_proven` |
| 쌍둥이 소수 | 모든 유한 주기 fingerprint에는 소수/합성수 후속항 모방자가 무한히 존재 | 유한 주기 특징을 계속 추가하면 쌍둥이를 인증할 수 있다는 경로 | `open_not_proven` |

## 1. 리만 가설

### 선언 명제

유한 소수 집합 `P`, `a_p>=0`, 실수 `t_1,...,t_J`에 대해

```text
K_jk = sum_(p in P) a_p cos((t_j-t_k) log p)
```

로 둡니다. 그러면 `K`는 양의 준정부호이고 `rank(K)<=2|P|`입니다.
상수 벡터에 수직인 공간으로 압축해도 계수는 증가하지 않습니다. 따라서
`J-1>2|P|`이면 압축된 핵은 반드시 특이행렬입니다. `epsilon I`를 더하면
그 강제 영공간의 고윳값은 정확히 `epsilon`이 됩니다.

### 증명

항등식

```text
cos(x-y)=cos(x)cos(y)+sin(x)sin(y)
```

에 의해 `K`는 다음 `2|P|`개 좌표를 가진 벡터들의 Gram 행렬입니다.

```text
sqrt(a_p) cos(t_j log p),  sqrt(a_p) sin(t_j log p)
```

따라서 양의 준정부호성과 계수 상계가 즉시 나옵니다. 계수-영차원 정리로
상수 모드 제거 뒤에도 최소 `J-1-2|P|`개의 영방향이 남습니다. 정규화
항은 이 방향에서 `epsilon I`로 작용하므로, 이 하한은 제타 산술에서
얻은 것이 아니라 외부에서 넣은 값입니다.

네 계산 행은 `|P|=3,5,8,12`, `J=2|P|+4`를 사용했습니다. 모든 행에서
최소 세 개의 강제 영방향을 확인했고 `epsilon=2^-10`을 추가했을 때 최소
압축 고윳값이 허용 오차 안에서 `epsilon`이 됐습니다. 정리 자체는
부동소수점 계산에 의존하지 않는 정확한 정리입니다.

### 한계와 다음 보조정리

무부호 소수 코사인 PSD는 Guinand-Weil 이차형식이 아닙니다. 아르키메데스
항, 자명한 영점, 부호 있는 소수 거듭제곱 항, 허용 시험함수 조건, 모든
시험함수에 대한 전칭 명제가 빠져 있습니다. Connes와 Consani의 연구는
연산자론적 Weil 양성의 경계와 연산자 구성의 한계를 다루지만,
PrimeProject는 그 추측적 틀을 증명했다고 주장하지 않습니다.

다음:
`SignedGuinandWeilFiniteSectionsConvergeWithoutArtificialDiagonalForEveryAdmissibleTestFamily`.

## 2. 콜라츠 추측

### 선언 명제

TICKET-240은 run-block lifting defect를 Fermat quotient 쌍
`u=F_q(2)`, `v=F_q(3)`으로 환원했습니다.

```text
x-depth >= 2  iff  5u-3v = 0 mod q,
y-depth >= 2  iff   u-v  = 0 mod q.
```

그러나 모든 홀수 소수 `q>5`에 대해 주단위원

```text
A=1+3q,  B=1+5q
```

는 `A^5=B^3 mod q^2`이지만 `A!=B mod q^2`입니다. 더 정확히
`v_q(A^5-B^3)>=2`, `v_q(A-B)=1`입니다.

### 증명과 계산

이항정리로

```text
(1+3q)^5 = 1+15q mod q^2,
(1+5q)^3 = 1+15q mod q^2,
A-B      = -2q
```

를 얻습니다. 즉 주단위원 대수 안에는 양의 결함 패턴이 실제로 존재합니다.
고정 밑수 점 `(F_q(2),F_q(3))`이 이 패턴을 피할 수는 있지만, 이를
증명하려면 LTE나 국소 군 구조에 없는 특별한 산술 정보가 필요합니다.

실제 합동식

```text
32^(q-1) = 27^(q-1) mod q^2
```

을 `5<=q<=100,000,000`인 `5,761,453`개 소수 전부에서 검사했습니다.
해와 양의 결함 후보는 없었습니다. TICKET-240보다 탐색 상한을 다섯 배
높였지만, 이는 전 소수 정리가 아닌 유한 인증입니다.

### 한계와 다음 보조정리

국소 반례 모형은 실제 예외 소수, 콜라츠 궤도 또는 순환이 아닙니다.
반대로 `10^8`까지 예외가 없다는 사실도 더 큰 예외를 배제하지 못합니다.
전 소수 run-block 깊이 지배를 증명해도 일반 necklace와 비주기 하강이
남습니다.

다음:
`FixedBaseFermatQuotientLineAvoidanceFor5Fq2Equals3Fq3UnlessFq2EqualsFq3`.

## 3. 강한 골드바흐 추측

### 선언 명제

정수 표현수의 정확한 분해

```text
R(N)=M(N)+sum_i E_i(N),  M(N)>0
```

에 대해 다음이 성립합니다.

1. `M+sum E_i>=1`은 정확히 `R>=1`이므로 중간 정리가 아닙니다.
2. `M-sum |E_i|>=1`은 충분조건이지만 필요조건은 아닙니다.
3. `E=(E+L)+(-L)`은 `R`을 보존하면서 `|L|`에 따라 절댓값 예산을
   임의로 키우므로, 절댓값 인증은 오차 분할에 대해 불변이 아닙니다.

### 증명과 계산

첫 명제는 대입이고 둘째는 삼각부등식입니다. 상쇄 분할이 셋째를
증명합니다. 따라서 “모든 명시적 오차”라는 표현만으로는 수학적 목표가
정의되지 않습니다. 관측값을 보기 전에 arc 분해, smoothing, 오차 묶음,
노름을 고정해야 합니다.

`X=10^3`부터 `10^7`까지 15개의 정확한 제한 소수 창 DFT 행을
감사했습니다. 표현이 존재하는 14개 행 모두에서 DC 절댓값 인증은
실패했지만 부호 항등식은 표현 존재를 정확히 판정했습니다. 이 유한 모형은
고전 major/minor-arc 증명을 반박하지 않습니다. 절댓값 인증이 필요조건이
아니고 임의의 오차 재분할이 허용되지 않음을 증명합니다.

### 한계와 다음 보조정리

실제 이항 소수 major/minor arc에 대한 점별 하한은 증명하지 못했습니다.
Helfgott의 major/minor arc 추정은 삼항 골드바흐의 엄밀한 구조를 제공하지만
여기 필요한 모든 큰 짝수에 대한 이항 추정은 제공하지 않습니다.

다음:
`FixedBinaryPrimeArcDecompositionHasUniformTargetwisePositiveLowerCertificate`.

## 4. 쌍둥이 소수 추측

### 선언 명제

`(n,n+2)`의 유한 특징 모음 `F`가 각각 고정된 법에 대해 주기적이라고
합시다. 공통 주기를 `M`이라 하고

```text
gcd(a,M)=gcd(a+2,M)=1
```

인 잉여류 `a mod M`을 고릅니다. 그러면

```text
F(p,p+2)=F(a,a+2)
```

이면서 `p+2`는 합성수인 소수 `p`가 무한히 존재합니다.

### 증명과 계산

`ell`을 `2M`을 나누지 않는 소수로 잡고

```text
p=a mod M,  p=-2 mod ell
```

을 부과합니다. CRT는 법 `M ell`의 기약 잉여류를 만들고 Dirichlet
정리에 의해 그 잉여류에 소수가 무한히 존재합니다. 주기성 때문에 모든
특징값이 보존되지만 `ell | p+2`이므로 충분히 큰 후속항은 합성수입니다.

주기 `30`부터 `510,510`까지 다섯 개의 정확 인증서를 기록했습니다.
가장 큰 증인은 `p=25,525,529`이고
`p+2=19*1,343,449`입니다. 무한성은 Dirichlet 정리에서 나오며 계산 행은
구현만 검증합니다.

### 한계와 다음 보조정리

이 정리는 쌍둥이 소수가 유한하다고 말하지 않습니다. 유한 주기 특징과
그 특징의 모든 결정적 후처리만을 충분한 인증서에서 제외합니다. 증가하는
법, switching weight, 부호 있는 Type II 정보는 하나의 고정 법에 주기적이지
않으므로 no-go의 적용 대상이 아닙니다. 이는 Polymath bounded-gap 연구가
설명하는 parity 한계와 일치합니다.

다음:
`GrowingModulusParitySensitiveTypeIIBoundForShiftTwoLambdaOnInfinitelyManyDyadicBlocks`.

## Proof DAG 요약

```text
TICKET-240 입력
  -> TICKET-241 폐기 추론
  -> TICKET-241 정확 정리
  -> 단일 최고위험 미해결 보조정리
```

각 트랙 JSON에 확장된 네 노드 DAG가 있습니다. 마지막 노드는 모두
`highest_risk_open`이고 상위 난제 증명 노드는 없습니다.

## 1차 연구 기준선

- Connes와 Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368).
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), 2026년 개정판.
- Sondow, [Lerch Quotients, Lerch Primes, Fermat-Wilson Quotients, and the Wieferich-non-Wilson Primes](https://arxiv.org/abs/1110.3113).
- Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252), [Major arcs for Goldbach's problem](https://arxiv.org/abs/1305.2897).
- D. H. J. Polymath, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).

위 자료는 알려진 학술 경계를 정합니다. 네 정리명은 PrimeProject의 경로
감사 결과이며 위 논문의 결과로 귀속하지 않습니다.
