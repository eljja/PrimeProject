# 소수 규칙성과 암호 소수 해석/예측 연구 계획

작성일: 2026-05-17

## 1. 출발점과 한계

이 문서의 목적은 소수의 수학적 규칙성을 정리하는 데서 끝나지 않고, 실제 암호 시스템에서 쓰이는 소수를 해석하고 약한 생성 패턴을 찾아내는 실용 연구 방향을 세우는 것이다.

중요한 전제는 명확하다. 정상적인 암호 구현에서 RSA 소수나 임의 생성 도메인 소수는 예측 가능하면 안 된다. 따라서 "일반 소수의 다음 값을 맞히는 이론"을 바로 암호 해독 도구로 만들 수 있다는 가정은 현실성이 낮다. 더 실용적인 목표는 다음 세 가지다.

1. 표준과 라이브러리가 소수를 어떤 제약 안에서 고르는지 모델링한다.
2. 실제 배포 키에서 난수 결함, 생성기 결함, 특수 형식 편향을 탐지한다.
3. 특정 구현체가 만든 소수 후보 공간을 줄이는 지문과 점수 함수를 만든다.

이 연구는 방어적 감사, 자체 키 품질 검증, 취약 구현 탐지를 목적으로 한다. 타인의 시스템을 무단으로 공격하거나 개인키를 복구하는 운영 절차는 연구 범위에서 제외한다.

## 2. 기존 이론 지도

### 2.1 소수 분포의 평균 법칙

소수정리(PNT)는 큰 수 주변에서 소수 밀도가 대략 `1 / log n`이라는 평균 법칙을 준다. 이는 큰 구간에서 소수가 얼마나 자주 나오는지를 예측하는 데 유용하지만, 특정 정수가 소수인지 또는 다음 소수가 어디인지 결정적으로 알려주지는 않는다.

암호 적용 관점:

- RSA 후보 생성에서 Miller-Rabin 같은 확률적 소수 판정을 몇 번 반복하면 기대 시도 횟수를 추정할 수 있다.
- `k`비트 난수 후보에서 소수를 찾는 비용과 분포를 예측할 수 있다.
- 개별 키의 보안성을 직접 깨는 정보는 거의 주지 않는다.

### 2.2 리만 가설과 명시 공식

리만 가설은 소수 계수 함수의 오차항을 강하게 제한하는 방향의 이론이다. Clay Mathematics Institute의 설명처럼 소수정리는 평균 분포를 주고, 리만 가설은 그 평균 주변의 오차를 더 정밀하게 통제하려는 문제다.

암호 적용 관점:

- 큰 구간 안에 소수가 존재할 가능성이나 오차 범위를 이론적으로 다듬는 데 의미가 있다.
- RSA나 ECC 키 생성기의 비밀 소수를 예측하는 직접 도구는 아니다.
- 실용 연구에서는 "배경 분포" 또는 이상치 탐지의 기준 모델로만 쓰는 것이 적절하다.

### 2.3 Cramer 확률 모델과 소수 간격

Cramer 모델은 정수 `n`이 확률 `1 / log n`로 소수처럼 행동한다고 보는 확률적 휴리스틱이다. 실제 소수 사이에는 모듈러 제약 때문에 독립성이 완전하지 않지만, 소수 간격과 후보 탐색 비용을 모델링하는 출발점으로 유용하다.

암호 적용 관점:

- 난수 후보에서 다음 소수로 이동하는 방식의 생성기 편향을 분석할 때 기준 모델이 된다.
- 예: "랜덤 홀수에서 다음 소수를 선택"하는 구현은 선택된 소수 앞쪽의 합성수 run 길이에 따라 분포 편향이 생길 수 있다.
- 단독으로는 공격 도구가 아니라, 구현체별 편향을 검정하는 통계 기준이다.

### 2.4 Hardy-Littlewood, k-tuples, twin primes

Hardy-Littlewood류 추측은 특정 선형 패턴 안에 소수가 동시에 나타나는 밀도를 예측한다. 쌍둥이 소수, 소수 k-튜플, 산술진행 소수 같은 구조를 설명하는 데 쓰인다.

암호 적용 관점:

- `p`, `q`, `p-1`, `p+1`, `2q+1` 같은 동시 소수 조건의 밀도 예측에 쓸 수 있다.
- safe prime 또는 Sophie Germain prime 생성 비용을 추정하는 데 유용하다.
- 특정 키의 소수를 맞히기보다, 특수 소수군 생성기의 후보 공간을 계산하는 데 의미가 있다.

### 2.5 Maynard-Tao와 bounded gaps

Maynard-Tao 계열의 연구는 소수 간격에 관한 강한 결과를 제공한다. 이는 소수가 완전히 무작위 점처럼 흩어져 있지 않으며, 특정한 조밀 구간 구조를 갖는다는 점을 보여준다.

암호 적용 관점:

- 이론적 의미는 크지만, 현재의 암호 키 예측에는 직접성이 낮다.
- 특정 후보 생성기가 "가까운 다음 소수"를 선택하는 경우, 간격 분포 분석과 결합할 수 있다.

### 2.6 계산적 소수 판정과 생성

실제 암호에서는 순수 이론보다 계산 절차가 중요하다.

- Miller-Rabin: 빠른 확률적 소수 판정.
- Baillie-PSW: 실무에서 강한 후보 검정으로 자주 쓰이는 조합.
- ECPP/AKS: 증명 가능한 소수성 확인에 가까우나 일반 키 생성에서는 비용 문제가 있다.
- sieving: 작은 소수들로 후보를 빠르게 걸러낸다.

암호 적용 관점:

- 생성기가 어떤 sieve, 어떤 Miller-Rabin base, 어떤 재시도 정책을 쓰는지가 지문이 될 수 있다.
- "수학적 소수 분포"보다 "구현체의 후보 선택 절차"가 더 많은 정보를 남긴다.

## 3. 실제 암호에서 쓰이는 소수의 유형

### 3.1 RSA 소수

RSA는 큰 서로 다른 두 소수 `p`, `q`를 생성하고 `n = p * q`를 공개한다. NIST FIPS 186-5는 RSA 키 생성에서 probable prime과 provable prime 방식, 보조 소수 조건 등을 다룬다. 현재 실용 분석에서 중요한 것은 다음이다.

- `p`, `q`가 충분히 무작위인지.
- 서로 너무 가깝지 않은지.
- 여러 키 사이에 같은 소수 인자가 재사용되지 않았는지.
- 생성 알고리즘의 후보 공간이 비정상적으로 작아졌는지.
- 공개 지수 `e`와 `p-1`, `q-1`의 관계가 조건을 만족하는지.

실제 취약 사례:

- Debian OpenSSL RNG 결함은 키 생성 난수가 예측 가능해져 SSH, TLS, OpenVPN, DNSSEC 키 등에 영향을 준 사례다.
- 2012년 Lenstra 등과 Heninger 등의 연구는 대규모 공개키에서 shared prime이 발견될 수 있음을 보였다.
- ROCA는 Infineon 계열 RSA 생성 방식의 구조적 편향으로 공개키만 보고 취약 키를 식별할 수 있었던 대표 사례다.

### 3.2 유한체 Diffie-Hellman 소수

Finite-field DH에서는 큰 소수 모듈러스 `p`와 생성자 `g`를 사용한다. RFC 7919의 FFDHE 그룹은 safe prime을 사용하며, 새 그룹도 safe prime이어야 한다고 설명한다. RFC 3526의 MODP 그룹도 고정된 큰 소수들을 정의한다.

실용적 의미:

- 이 소수들은 보통 임의 개인키처럼 비밀이 아니라 공개 도메인 파라미터다.
- 예측 대상이 아니라, 검증 대상이다.
- 취약성은 소수 자체보다 작은 subgroup, 비표준 그룹, 재사용 정책, 구현 검증 누락에서 생긴다.

### 3.3 ECC의 prime field 소수

ECC에서는 곡선이 정의되는 유한체 `Fp`의 소수 `p`가 중요하다. 예시는 다음과 같다.

- Curve25519: RFC 7748에서 `2^255 - 19`를 권장한다. 이는 pseudo-Mersenne 형태라 구현 성능이 좋다.
- Curve448: `2^448 - 2^224 - 1`.
- NIST P-256: `2^256 - 2^224 + 2^192 + 2^96 - 1`.
- secp256k1: SEC 2에서 정의된 곡선이며 field prime은 `2^256 - 2^32 - 977`.

실용적 의미:

- ECC field prime은 보통 비밀이 아니라 표준 상수다.
- 보안은 field prime 하나보다 곡선 차수, cofactor, base point, twist security, 구현의 side-channel 저항성에 좌우된다.
- "소수 예측"보다는 "파라미터 선택 동기와 구현 지문" 분석이 실용적이다.

## 4. 실용 분석 방법

### 4.1 공개 RSA 모듈러스 배치 GCD

여러 RSA 공개키의 `n`들을 모아 pairwise 또는 product/remainder tree 방식으로 GCD를 계산한다. 서로 다른 키가 같은 `p`를 공유하면 `gcd(n_i, n_j) = p`가 되어 즉시 취약하다.

용도:

- 자체 인프라 인증서, 장비 키, 펌웨어 내장 키의 품질 감사.
- 저엔트로피 장비군 탐지.

한계:

- shared prime이 없으면 아무것도 깨지지 않는다.
- 정상적인 현대 키에서는 거의 발견되지 않아야 한다.

### 4.2 Fermat 근접 소수 검사

`p`와 `q`가 지나치게 가까우면 Fermat factorization이 빨라진다. 정상적인 무작위 RSA에서는 두 소수가 공격 가능할 정도로 가까울 확률이 극히 낮지만, 잘못된 생성기가 상위 비트를 공유하거나 좁은 범위에서 뽑으면 문제가 된다.

용도:

- 커스텀 RSA 생성기 검증.
- 임베디드/스마트카드 키 생성 품질 확인.

### 4.3 생성기 지문 분석

공개키만 보고도 다음 특징을 측정할 수 있다.

- modulus bit length와 최상위/최하위 비트 패턴.
- `n mod m` 분포.
- `p`, `q`를 직접 알 수 없더라도 ROCA처럼 `n mod small primes` 패턴으로 생성기 편향 탐지.
- 인증서 발급 시점, 제조사, 펌웨어 버전, 라이브러리 버전과 키 패턴의 상관.

핵심은 소수 자체를 일반 이론으로 예측하는 것이 아니라, "어떤 생성기가 만든 결과인지"를 추정하는 것이다.

### 4.4 표준 소수와 특수형 소수 검증

DH/ECC에서 공개 도메인 소수는 특수한 형태가 많다.

- safe prime: `p = 2q + 1`, `q`도 소수.
- pseudo-Mersenne prime: `2^k - c`.
- Solinas prime: 빠른 reduction을 위한 sparse form.

용도:

- 구현 성능 분석.
- 상수 검증.
- 비표준 파라미터가 안전 조건을 만족하는지 확인.

### 4.5 후보 생성 시뮬레이터

라이브러리별 RSA 생성 절차를 재현한다.

- 랜덤 바이트 생성.
- 상위/하위 비트 강제.
- 홀수화.
- 작은 소수 sieve.
- Miller-Rabin 반복.
- 조건 불만족 시 증가 방식 또는 재샘플링 방식.

그 뒤 실제 공개키 집합의 통계와 비교한다. 이 접근은 예측이라기보다 attribution과 anomaly detection에 가깝다.

## 5. 우리만의 제안: 생성기-제약 지문 이론

### 5.1 핵심 명제

암호 소수는 "소수 전체 집합"에서 균일하게 나타나는 것이 아니라, 특정 구현체가 만든 후보 생성 공간과 검정 절차를 통과한 산물이다. 따라서 실용적 예측 가능성은 소수의 보편 규칙성보다 다음 세 요인에 의해 결정된다.

1. 후보 공간 제약: bit length, congruence, safe prime 조건, strong prime 조건, top/bottom bit 강제.
2. 생성 절차 편향: increment-to-next-prime, rejection sampling, sieve window, Miller-Rabin base 선택.
3. 엔트로피 결함: seed 재사용, 낮은 entropy, VM/임베디드 부팅 시점, 취약 CSPRNG.

이를 합쳐 각 공개키 또는 도메인 소수에 대해 "생성기-제약 지문"을 계산한다.

### 5.2 실용 점수 함수

각 키 또는 소수 후보에 대해 다음 점수를 만든다.

- `ConstraintFit`: 표준/라이브러리별 제약과 얼마나 잘 맞는가.
- `DistributionSurprise`: 정상 무작위 모델 대비 residue, gap, bit pattern이 얼마나 이상한가.
- `GeneratorLikelihood`: 알려진 생성기 모델 중 어느 것과 가장 가까운가.
- `EntropyRisk`: 같은 제조사/시점/장비군에서 충돌이나 근접성이 관측되는가.
- `ExploitabilityBound`: 실제 공격 가능성을 보수적으로 상한 평가한다.

목표는 "이 키를 깰 수 있다"가 아니라 "이 키 집합은 어떤 생성기에서 왔고, 어떤 검사가 우선순위인가"를 판단하는 것이다.

### 5.3 연구 가설

가설 A: 정상 라이브러리별 RSA 공개키는 `n mod small primes`, bit pattern, 인증서 메타데이터의 결합 특징에서 약한 생성기와 구분 가능하다.

가설 B: 취약 생성기는 prime gap 자체보다 후보 선택 정책의 흔적을 더 강하게 남긴다.

가설 C: ECC/DH의 공개 소수는 예측 문제가 아니라 파라미터 provenance 문제이며, 안전성 평가는 소수 형태와 그룹 구조를 함께 보아야 한다.

가설 D: 실용적 "소수 예측"은 일반 수론 문제로 풀기보다, 생성기 모델을 역추정해 후보 공간을 줄이는 문제로 재정의해야 한다.

## 6. 단계별 실행 계획

### 1단계: 기준 문헌과 표준 정리

목표:

- RSA, DH, ECC에서 소수가 쓰이는 위치를 분리한다.
- 표준 소수와 비밀 소수를 구분한다.
- 약한 키 사례를 재현 가능한 검사 항목으로 바꾼다.

산출물:

- 표준 소수 카탈로그.
- RSA 생성 절차 비교표.
- 취약 패턴 체크리스트.

### 2단계: 데이터 모델 설계

대상 데이터:

- RSA 공개키 모듈러스 `n`.
- 인증서 메타데이터: 발급자, subject, serial, validity, key size, signature algorithm.
- DH/ECC 도메인 파라미터.
- 자체 생성 실험 키.

스키마:

- `key_id`
- `algorithm`
- `modulus_or_prime`
- `bit_length`
- `source`
- `created_at`
- `issuer_or_vendor`
- `observed_features`
- `risk_scores`

### 3단계: 분석 엔진 구현

필수 모듈:

- RSA modulus parser.
- batch GCD.
- near-square/Fermat risk estimator.
- residue fingerprint extractor.
- known weak generator fingerprint checker.
- standard DH/ECC parameter recognizer.
- report generator.

초기 구현은 공격 자동화가 아니라 품질 감사 도구로 제한한다.

### 4단계: 생성기 시뮬레이터 구현

모델:

- ideal rejection sampling.
- increment-to-next-prime.
- fixed-seed deterministic generator.
- low-entropy seed family.
- safe-prime generator.
- pseudo-Mersenne/Solinas prime selector.

목표:

- 각 모델이 남기는 통계 흔적을 만든다.
- 실제 키 집합과 비교해 생성기 가능성을 점수화한다.

### 5단계: 검증 실험

실험군:

- 정상 OpenSSL/BoringSSL/RustCrypto 등으로 생성한 키.
- 의도적으로 낮은 entropy로 만든 테스트 키.
- p와 q가 가까운 테스트 키.
- shared-prime 테스트 키.
- 표준 DH/ECC 파라미터.

검증 지표:

- 취약 키 탐지율.
- 정상 키 오탐률.
- 생성기 attribution 정확도.
- 대규모 키셋 처리 시간.

### 6단계: 연구 문서화와 공개 범위 결정

공개 가능한 내용:

- 방어적 키 감사 방법.
- 표준 파라미터 검증.
- 통계 모델과 안전한 실험 데이터.

주의해서 다룰 내용:

- 실제 취약 키의 개인 인자.
- 특정 타깃 서비스의 키 분석 결과.
- 취약 생성기에서 개인키 후보를 좁히는 절차.

## 7. 우선순위

가장 먼저 할 일은 일반 소수 예측 모델을 만드는 것이 아니다. 다음 순서가 실용적이다.

1. RSA 공개키 품질 감사 도구: batch GCD, Fermat risk, bit/residue fingerprint.
2. 표준 DH/ECC 소수 카탈로그: RFC/NIST/SEC 상수 검증.
3. 생성기 시뮬레이터: 정상/취약 생성기의 통계 흔적 비교.
4. 생성기-제약 지문 점수화: 키셋 단위 위험도와 provenance 추정.
5. 이론 확장: 소수 간격/분포 모델을 점수 함수의 background model로 통합.

## 8. 참고 자료

- [NIST FIPS 186-5: Digital Signature Standard](https://csrc.nist.gov/pubs/fips/186-5/final)
- [NIST SP 800-186: Elliptic Curve Domain Parameters](https://csrc.nist.gov/pubs/sp/800/186/final)
- [RFC 7919: Negotiated FFDHE Parameters for TLS](https://www.rfc-editor.org/rfc/rfc7919.html)
- [RFC 3526: MODP Diffie-Hellman Groups for IKE](https://www.rfc-editor.org/rfc/rfc3526)
- [RFC 7748: Elliptic Curves for Security](https://www.rfc-editor.org/rfc/rfc7748.html)
- [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)
- [Clay Mathematics Institute: Riemann Hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/)
- [USENIX: Mining Your Ps and Qs](https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/heninger)
- [Lenstra et al.: Ron was wrong, Whit is right](https://eprint.iacr.org/2012/064.pdf)
- [CERT VU#925211: Debian/Ubuntu OpenSSL predictable RNG](https://www.kb.cert.org/vuls/id/925211/)

