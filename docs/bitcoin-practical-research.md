# Bitcoin Practical Research Track

작성일: 2026-05-18

## 핵심 결론

Bitcoin의 secp256k1 소수 `p`와 group order `n`은 공개 고정값이므로, 이 소수를 예측하는 것은 보안 위협이 아니다. 실용적인 연구 대상은 다음이다.

- 개인키 생성 난수의 편향.
- ECDSA/Schnorr nonce 생성 편향.
- ECDSA `r` 재사용 또는 상관.
- 서명 정규화 문제, 예: high-s.
- 지갑/라이브러리/하드웨어별 서명 fingerprint.

## secp256k1 공개 상수

```text
p = 2^256 - 2^32 - 977
n = FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
curve: y^2 = x^3 + 7 mod p
```

`p`와 `n`은 모두 공개 prime이다. Bitcoin 보안은 이 값을 숨기는 데 있지 않고, 개인키 `d`와 nonce `k`가 예측 불가능하다는 데 있다.

## 구현된 방어적 감사

현재 PrimeProject는 Bitcoin ECDSA 서명 메타데이터에 대해 다음을 점검한다.

- `r`, `s`가 secp256k1 group order 범위 안에 있는지.
- `s`가 low-s 정규화 범위 안에 있는지.
- 동일한 `r`이 여러 서명에서 반복되는지.

반복 `r`은 nonce 재사용 또는 nonce 상관 위험을 의미한다. 이 도구는 방어적 감사를 위해 위험을 보고하지만, 개인키 복구값이나 복구 절차는 출력하지 않는다.

## CLI

```powershell
python -m prime_audit.cli bitcoin-constants --output data/bitcoin_constants.json
python -m prime_audit.cli bitcoin-signature-audit --input data/bitcoin_signatures.json --output data/bitcoin_signature_audit.json
```

입력 예:

```json
{
  "signatures": [
    {
      "signature_id": "tx1:0",
      "public_key": "02...",
      "r": "0x...",
      "s": "0x..."
    }
  ]
}
```

DER 서명도 입력할 수 있다.

```json
{
  "signatures": [
    {
      "signature_id": "tx1:0",
      "public_key": "02...",
      "der": "3045..."
    }
  ]
}
```

## 연구 확장 방향

1. 공개 서명셋의 `r` 분포와 wallet fingerprint 비교.
2. low-s 비율과 시점별 정책 변화 추적.
3. Schnorr/BIP340 nonce 관련 공개 메타데이터 분석.
4. known-good wallet 샘플과 의심 샘플의 분포 차이 측정.
5. 취약 복구가 아니라 취약 징후 탐지 중심의 리포트 자동화.
