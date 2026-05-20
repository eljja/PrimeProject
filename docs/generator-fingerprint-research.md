# Generator Fingerprint Research Track

작성일: 2026-05-21

## 목표

목표는 암호 시스템이 만든 수학적 객체에서 생성기의 흔적과 약점을 찾는 것이다. 이 단계에서는 RSA modulus를 직접 깨는 방향이 아니라, 공개 prime-like parameter와 소유 데이터셋의 prime 레코드에서 다음 신호를 추출한다.

- residue class drift
- low-bit collision
- local prime-gap context
- known public parameter recognition
- next-prime exposure signal

## Fingerprint 관점

소수 `p` 하나만 보면 정보가 약하다. 하지만 여러 레코드가 있으면 생성기가 남긴 흔적을 집계할 수 있다.

```text
fingerprint(p) =
  bit_length(p)
  + p mod 30, 210, 2310
  + low16 / low32
  + previous_prime(p), next_prime(p)
  + left_gap / log(p)
  + right_gap / log(p)
```

여기서 특히 중요한 값은 `left_gap / log(p)`이다. `next_prime(x)` 방식으로 생성된 소수는 큰 left gap 뒤의 소수가 더 자주 관측될 수 있다.

## 구현된 CLI

```powershell
python -m prime_audit.cli fingerprint-primes --input data/synthetic_keys.json --output data/generator_fingerprints.json
```

옵션:

```powershell
--gap-max-steps 4096
```

이 값은 주변 prime을 찾기 위해 양쪽으로 탐색하는 최대 step 수다.

## 현재 출력

리포트는 다음을 포함한다.

- `records`: 레코드별 fingerprint.
- `aggregate.bit_lengths`: bit length 분포.
- `aggregate.residue_total_variation`: `mod 30`, `210`, `2310` residue drift.
- `aggregate.low16_unique_ratio`: low-bit 충돌 신호.
- `aggregate.gap_statistics`: local gap 기반 통계.
- `aggregate.generator_signals`: 생성기 편향 후보 신호.
- `findings`: repeated prime, non-prime parameter, residue drift, next-prime exposure 등.

## 해석 원칙

이 도구는 단일 레코드로 생성기를 단정하지 않는다. 신호는 dataset 수준에서 본다.

- `residue_drift_generator_signal`: residue 분포가 균등분포에서 크게 벗어난 경우.
- `next_prime_exposure_signal`: 평균 left gap이 `log(p)` 대비 큰 경우.
- `low_bits_collision_signal`: low bits 충돌이 표본 크기 대비 높은 경우.
- `recognized_public_parameter`: 표준 공개 prime이므로 비밀 생성 약점이 아니라 provenance 정보다.

## 다음 진화 방향

1. RSA private-key owned dataset에서 `p`, `q`만 따로 추출해 fingerprint.
2. 공개 인증서 RSA modulus에서는 shared factor, ROCA, near-square와 fingerprint 리포트 통합.
3. Bitcoin signature audit의 `r` 분포와 generator fingerprint 출력 통합.
4. known-good library별 baseline fingerprint 구축.
5. 의심 데이터셋과 baseline 사이의 거리 측정.
