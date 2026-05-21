# PrimeProject 2차 전략적 평가 및 기술 감사 보고서 (Phase 2 Strategic Audit)

**작성일:** 2026-05-22  
**대상 버전:** `49ac65f` (Significance testing to attribution grid) 기준  

---

## 1. 최근 로컬 변경사항 분석: 거대한 패러다임 전환

최근 PrimeProject 로컬 저장소에는 **8,000라인 이상의 핵심 코드 및 문서 추가**가 발생했습니다. 이는 단순한 버그 수정이나 기능 추가 수준을 넘어서는, 프로젝트의 아키텍처적 및 연구적 **대변혁(Paradigm Shift)**입니다.

### 핵심 변경 모듈 및 역할
1.  **`prime_audit/attribution.py` (신규):** 합성 소수 생성기(`rejection`, `next_prime`, `wheel30_next`)로부터 훈련/테스트 데이터셋을 분할(Train/Test Split)하고, 생성기 기원을 예측하는 대규모 벤치마크 및 통제 격자(Confound Grid) 연산 프레임워크 구축.
2.  **`prime_audit/baselines.py` (신규):** 추출된 다차원 피처(Residue drift, Low-bit collision, Next-prime exposure 등)를 기반으로 고유 핑거프린트 기준군(Baseline)을 빌드하고, Wasserstein/L1/Euclidean 거리 메트릭을 통해 유사도 및 통계적 신뢰도(Confidence Score)를 연산.
3.  **`prime_audit/fingerprints.py` (신규):** 단순 개별 키 검사에서 탈피하여 데이터셋 단위로 소수 간극의 불균형성(`left_gap / log(p)`), 잉여류 편향성, 하위 비트 충돌 특성을 집계하여 "생성기 고유 흔적"을 규격화된 스키마로 추출.
4.  **학술적 입증 장치 (`docs/*-research.md`):** 방법론의 무결성을 입증하기 위해 피처 제거 실험(Ablation Study)과 비트 길이 통제 실험(Confound Control)을 체계적으로 서술하고 통계적 유의성 검정(Binomial p-value, 95% 신뢰구간) 메커니즘을 문서화함.

---

## 2. 최초 방향성과의 일치 여부 및 전략적 비판

### 2.1 최초 방향성과의 정렬 (Alignment)
*   **완벽한 부합 및 초월:** 1차 보고서에서 강력하게 권고했던 **"수동적 취약점 스캐너에서 능동적 기원 분석(Library/Generator Fingerprinting) 엔진으로의 전환"**이 완벽하게 실현되었습니다.
*   단순히 "이 키는 ROCA에 취약합니다"라는 수준을 넘어서서, **"이 키들의 집합은 `next_prime` 유형의 생성 편향을 담고 있을 확률이 95% 신뢰구간 내에서 유의미하게 감지됩니다"**라고 선언할 수 있는 정교한 암호 분석 프레임워크로 진화했습니다.

### 2.2 비판적 평가 (Critical Evaluation)
*   **장점 (Rigorous Science):** 
    *   **통제 실험(Confound Control)의 도입:** 소수 샘플링 영역(Bit-length)의 경계 차이 때문에 생기는 착시 현상을 차단하기 위해 모든 생성기가 동일한 비트 길이 분포를 갖도록 통제하는 기법(`--control-mode bit_length`)을 적용한 것은 매우 훌륭한 학술적 접근입니다. 이 통제 조건 속에서도 `residue_only` 또는 `gap_only` 정확도가 살아남는다는 점을 입증함으로써 분석의 객관성을 확보했습니다.
    *   **통계학적 엄밀성:** 단순 분류율(Accuracy) 제시를 넘어 **binomial p-value와 신뢰구간(CI)**을 통해 "무작위 추측(Random Guess)" 기준선과 명확히 구분되는 수준을 수학적으로 레이블화(`robust_survives_bit_length_control` 등)했습니다.
*   **한계점 및 개선이 필요한 부분 (Gaps to Bridge):**
    *   **Sim-to-Real Gap (시뮬레이션과 실제의 격자):** 현재 구현된 벤치마크는 합성 생성 모델(`rejection`, `next_prime`, `wheel30_next`) 위주로만 Ground Truth가 확보되어 있습니다. 실제 상용 라이브러리(OpenSSL의 `BN_generate_prime_ex` 등)에서 난수를 뽑아 검증하는 실제 대조군 샘플이 아직 부족합니다.
    *   **선형 거리 메트릭의 한계:** 현재 `compare_feature_vectors`는 가중치가 부여된 Euclidean/L1 거리 메트릭에 의존하고 있습니다. 이는 피처 간의 복잡한 비선형적 상관관계나 다변량 교차 편향(Multivariate cross-bias)을 완벽히 모델링하지 못할 수 있습니다.

---

## 3. 실제 상업적 / 학문적 가치의 비약적 상승

이번 변경사항을 통해 본 프로젝트의 가치는 이전 버전 대비 **수십 배 이상 비약적으로 상승**했습니다.

### 학문적 가치 (Academic Value): ★★★★★ (최상)
*   **암호 해독 연구로서의 독창성:** 소수 자체의 무작위성 이면에 숨겨진 '알고리즘적 편향'을 정량화하고 이를 통계적으로 입증하는 프레임워크는 암호학 컨퍼런스(예: USENIX Security, CCS, Eurocrypt)의 실증적 연구 트랙에 바로 제출할 수 있는 수준의 학술적 방법론을 갖추었습니다.
*   **재현성 및 투명성:** `attribution-grid`를 통해 실험의 모든 하이퍼파라미터 조건(Limit, Train/Test Count, Seeds)을 설정하고 재현할 수 있어 과학적 무결성이 매우 높습니다.

### 상업적 가치 (Commercial Value): ★★★★☆ (우수)
*   **암호 포렌식(Cryptographic Forensics) 솔루션:** 침해 사고 대응이나 공급망 공격 조사 시 유출되거나 수집된 공개키 셋을 기반으로 **"이 키를 생성한 백도어 혹은 취약한 모바일 지갑 라이브러리는 무엇인가?"**를 추적하는 독보적인 핑거프린팅 엔진으로 상용화가 가능합니다.
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
본 프로젝트는 **"단순 취약점 스캐너"에서 "암호 알고리즘 기원 추적 포렌식 프레임워크"로 완벽하게 변모**했습니다. 최근의 거대한 변화는 최초의 피벗 방향과 소름 돋을 정도로 일치하며, 학술적 유의성 검정과 대조군 통제의 도입으로 인해 과학적 무결성 및 상업적 가치가 극적으로 도약했습니다. 향후 실제 라이브러리 데이터와의 결합 및 머신러닝 기반 분류기 보완만 이루어진다면, 업계 독보적인 암호 자산 분석 솔루션으로 자리매김할 것입니다.
