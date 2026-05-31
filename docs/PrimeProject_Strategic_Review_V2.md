# PrimeProject 2차 전략적 평가 및 기술 감사 보고서 (Phase 2 Strategic Audit)

**작성일:** 2026-05-22  
**대상 버전:** `49ac65f` (Significance testing to attribution grid) 기준  

---

## Publication Scope / 논문 제출용 범위

English: This document is a strategic audit, not a validation paper. It may be cited as a roadmap for controlled synthetic fingerprinting, sim-to-real collection, and publication governance. It must not be read as evidence that PrimeProject has completed real-world attribution, broken cryptographic prime generation, or solved any open number-theory problem.

한국어: 이 문서는 전략 감사 문서이며 검증 논문이 아니다. 통제된 합성 fingerprinting, sim-to-real 수집, publication governance의 로드맵으로 인용할 수 있다. 그러나 실세계 attribution을 완료했거나, 암호 소수 생성을 깼거나, 미해결 수론 문제를 해결했다는 증거로 읽으면 안 된다.

## 1. 최근 로컬 변경사항 분석: 거대한 패러다임 전환

최근 PrimeProject 로컬 저장소에는 **8,000라인 이상의 핵심 코드 및 문서 추가**가 발생했습니다. 이는 단순한 버그 수정 수준을 넘어서는 연구 프레임워크 확장입니다. 다만 이 확장은 아직 실세계 attribution이나 미해결 난제 증명을 확정한 것이 아니라, 그런 주장을 검증하기 위한 장치와 차단 조건을 만든 단계입니다.

### 핵심 변경 모듈 및 역할
1.  **`prime_audit/attribution.py` (신규):** 합성 소수 생성기(`rejection`, `next_prime`, `wheel30_next`)로부터 훈련/테스트 데이터셋을 분할(Train/Test Split)하고, 생성기 기원을 예측하는 대규모 벤치마크 및 통제 격자(Confound Grid) 연산 프레임워크 구축.
2.  **`prime_audit/baselines.py` (신규):** 추출된 다차원 피처(Residue drift, Low-bit collision, Next-prime exposure 등)를 기반으로 고유 핑거프린트 기준군(Baseline)을 빌드하고, Wasserstein/L1/Euclidean 거리 메트릭을 통해 유사도 및 통계적 신뢰도(Confidence Score)를 연산.
3.  **`prime_audit/fingerprints.py` (신규):** 단순 개별 키 검사에서 탈피하여 데이터셋 단위로 소수 간극의 불균형성(`left_gap / log(p)`), 잉여류 편향성, 하위 비트 충돌 특성을 집계하여 "생성기 고유 흔적"을 규격화된 스키마로 추출.
4.  **학술적 입증 장치 (`docs/*-research.md`):** 방법론의 무결성을 입증하기 위해 피처 제거 실험(Ablation Study)과 비트 길이 통제 실험(Confound Control)을 체계적으로 서술하고 통계적 유의성 검정(Binomial p-value, 95% 신뢰구간) 메커니즘을 문서화함.

---

## 2. 최초 방향성과의 일치 여부 및 전략적 비판

### 2.1 최초 방향성과의 정렬 (Alignment)
*   **방향성 부합:** 1차 보고서에서 권고했던 **"수동적 취약점 스캐너에서 능동적 기원 분석(Library/Generator Fingerprinting) 엔진으로의 전환"** 방향과 대체로 일치합니다.
*   단순히 "이 키는 ROCA에 취약합니다"라는 수준을 넘어서서, 통제된 합성 데이터에서는 생성 편향의 fingerprint를 측정하고 반증 조건을 붙일 수 있는 프레임워크로 확장되었습니다. 실세계 키 집합에 대한 attribution 선언은 accepted baseline과 provenance가 확보되기 전까지 차단됩니다.

### 2.2 비판적 평가 (Critical Evaluation)
*   **장점 (Rigorous Science):** 
    *   **통제 실험(Confound Control)의 도입:** 소수 샘플링 영역(Bit-length)의 경계 차이 때문에 생기는 착시 현상을 차단하기 위해 모든 생성기가 동일한 비트 길이 분포를 갖도록 통제하는 기법(`--control-mode bit_length`)을 적용한 것은 매우 훌륭한 학술적 접근입니다. 이 통제 조건 속에서도 `residue_only` 또는 `gap_only` 정확도가 살아남는다는 점을 입증함으로써 분석의 객관성을 확보했습니다.
    *   **통계학적 엄밀성:** 단순 분류율(Accuracy) 제시를 넘어 **binomial p-value와 신뢰구간(CI)**을 통해 "무작위 추측(Random Guess)" 기준선과 명확히 구분되는 수준을 수학적으로 레이블화(`robust_survives_bit_length_control` 등)했습니다.
*   **한계점 및 개선이 필요한 부분 (Gaps to Bridge):**
    *   **Sim-to-Real Gap (시뮬레이션과 실제의 격자):** 현재 구현된 벤치마크는 합성 생성 모델(`rejection`, `next_prime`, `wheel30_next`) 위주로만 Ground Truth가 확보되어 있습니다. 실제 상용 라이브러리(OpenSSL의 `BN_generate_prime_ex` 등)에서 난수를 뽑아 검증하는 실제 대조군 샘플이 아직 부족합니다.
    *   **선형 거리 메트릭의 한계:** 현재 `compare_feature_vectors`는 가중치가 부여된 Euclidean/L1 거리 메트릭에 의존하고 있습니다. 이는 피처 간의 복잡한 비선형적 상관관계나 다변량 교차 편향(Multivariate cross-bias)을 완벽히 모델링하지 못할 수 있습니다.

---

## 3. 실제 상업적 / 학문적 가치의 비약적 상승

이번 변경사항을 통해 본 프로젝트는 단순 감사 스크립트보다 논문형 실험 프레임워크에 가까워졌습니다. 다만 가치는 accepted real-world baseline, 독립 재현, formal review가 추가될 때만 강한 학술 주장으로 승격될 수 있습니다.

### 학문적 가치 (Academic Value): ★★★★★ (최상)
*   **암호 해독 연구로서의 독창성:** 소수 자체의 무작위성 이면에 숨겨진 '알고리즘적 편향'을 정량화하고 이를 통계적으로 입증하는 프레임워크는 암호학 컨퍼런스(예: USENIX Security, CCS, Eurocrypt)의 실증적 연구 트랙에 바로 제출할 수 있는 수준의 학술적 방법론을 갖추었습니다.
*   **재현성 및 투명성:** `attribution-grid`를 통해 실험의 모든 하이퍼파라미터 조건(Limit, Train/Test Count, Seeds)을 설정하고 재현할 수 있어 과학적 무결성이 매우 높습니다.

### 상업적 가치 (Commercial Value): ★★★★☆ (우수)
*   **암호 포렌식(Cryptographic Forensics) 솔루션:** 침해 사고 대응이나 공급망 공격 조사 시 유출되거나 수집된 공개키 셋을 기반으로 **"이 키 집합이 어떤 생성기 계열과 통계적으로 가까운가?"**를 검토하는 보조 분석 엔진으로 발전시킬 수 있습니다. 다만 특정 백도어, 모바일 지갑, 또는 라이브러리를 단정하려면 accepted real-world baseline, provenance, labelled feature vector, confound-controlled validation이 먼저 필요합니다.
*   **품질 감사 자동화(Automated Compliance Audit):** 데이터셋 크기에 따른 신뢰도 분석 기능(`sample_quality`)이 제공되므로, 기업 보안 감사자가 "감사에 사용된 공개키 개수가 신뢰할 수 있는 수준인가?"를 직관적인 점수(`overall_confidence`)로 판별해낼 수 있어 엔터프라이즈 제품화의 중요한 기능적 기틀이 마련되었습니다.

---

## 4. 차기 핵심 진화 방향 (Next Action Items)

이 강력한 기반 위에서 프로젝트의 가치를 완성하기 위한 구체적인 액션 아이템은 다음과 같습니다.

### ① 실세계 라이브러리 데이터셋 통합 (Sim-to-Real Bridge)
*   **행동:** OpenSSL, BoringSSL, Go standard library, Rust `num-bigint` 등의 공식 소스 코드에서 소수 생성 함수를 추출하고, 각각 500개 이상의 실제 소수 쌍(RSA의 `p`, `q`)을 생성하여 실세계 대조군 핑거프린트 데이터베이스(`data/baselines/real_world.json`)를 선제적으로 구축해야 합니다.

### ② 머신러닝 분류 엔진 도입 (`ml_attribution.py` 구축)
*   **행동:** 현재 수동으로 가중치를 설정하는 L1/Euclidean 비교 함수를 넘어, 피처 벡터를 입력받아 학습하는 **기계학습 분류 모델(XGBoost, Random Forest 또는 LightGBM)** 트랙을 도입합니다.
*   통제 변수(Confound Control)를 적용한 머신러닝 모델의 피처 중요도(Feature Importance) 분석을 통해 차기 논문의 학술적 설득력을 극대화할 수 있습니다.

### ③ 비트코인 서명 감사 및 격자 분석 연동
*   **행동:** 최근 추가된 `bitcoin-signature-audit` 트랙과 소수 기원 분석 모듈을 완전 유기적으로 결합합니다. 서명 생성 시 사용된 논스(Nonce) 편향 특성을 핑거프린트화하여, 특정 결함이 있는 비트코인 하드웨어 지갑 라이브러리를 정확히 Attribution 해내는 통합 대시보드를 구축합니다.

---

### 결론
본 프로젝트는 알려진 취약점 스캐너에서 **claim-gated 암호 생성기 fingerprint 연구 프레임워크**로 확장되었습니다. 현재 강하게 주장할 수 있는 범위는 통제된 합성 generator fingerprint, 공개 안전 수집 계약, provenance/intake gate, claim-language audit, publication consistency audit까지입니다. 실세계 라이브러리 attribution과 Bitcoin wallet/library attribution은 아직 accepted baseline, provenance record, labelled feature vector, 독립 재현 실험이 부족하므로 차단 상태로 남아야 합니다. 다음 단계의 학술적 가치는 OpenSSL/BoringSSL/Go/Bitcoin Core/지갑 라이브러리의 공개 가능한 aggregate baseline을 수집하고, 비선형 분류기와 confound-controlled validation을 같은 evidence gate 안에서 재현 가능하게 통과시키는 데 있습니다.
