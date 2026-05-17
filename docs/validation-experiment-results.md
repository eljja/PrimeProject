# 5단계 검증 실험 결과

작성일: 2026-05-17

## 실험 목적

`prime_audit`의 초기 분석 엔진이 통제된 합성 데이터에서 의도한 위험 신호를 탐지하는지 확인한다.

## 실험 데이터

생성 명령:

```powershell
python -m prime_audit.cli simulate --output data/synthetic_keys.json --bits 128 --include-standards
```

데이터 구성:

- 정상 toy RSA 모듈러스 1개.
- shared-prime toy RSA 모듈러스 2개.
- near-square toy RSA 모듈러스 1개.
- increment-to-next-prime 방식 toy RSA 모듈러스 1개.
- Curve25519 field prime 1개.
- NIST P-256 field prime 1개.

toy RSA는 빠른 검증을 위해 128비트로 생성한다. 실제 보안 수준의 키가 아니며, 모든 RSA 샘플은 작은 크기 경고를 내는 것이 정상이다.

## 실행 명령

```powershell
python -m unittest discover -s tests
python -m prime_audit.cli audit --input data/synthetic_keys.json --output data/audit_report.json
```

## 기대 결과

- shared-prime 샘플 2개에서 `shared_prime_factor` critical finding.
- near-square 샘플에서 `near_square_factorization` high finding.
- 표준 ECC field prime 2개에서 `standard_public_prime` info finding.
- 모든 128비트 RSA 샘플에서 `rsa_modulus_too_small` medium finding.

## 해석

현재 결과는 1차 목표에 부합한다. 분석 엔진은 공개 모듈러스만으로 공유 소수와 근접 인수 위험을 찾고, 공개 field prime은 표준 카탈로그와 대조한다.

다음 개선 항목:

- PEM/DER 공개키 파서 추가.
- RFC 7919/RFC 3526 FFDHE/MODP 전체 상수 카탈로그 확장.
- 생성기 지문 비교를 통계 검정으로 확장.
- 대규모 키셋용 product/remainder tree 최적화.

