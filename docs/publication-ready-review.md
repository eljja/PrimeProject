# Publication-Ready Document Review / 논문 제출용 문서 검토

## English Summary

This review fixes the public-documentation claim boundary for PrimeProject. The project is manuscript-oriented only if its documents separate supported artifacts from blocked claims:

- Supported: defensive key-quality auditing, synthetic generator-fingerprint experiments, reproducible bounded open-problem certificates, public-safe collection contracts, and publication governance artifacts.
- Not supported yet: real-world generator attribution, Bitcoin wallet/library attribution, cryptographic prime prediction, or a proof of the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, or Twin Prime conjecture.
- Review rule: every document may describe a research route, candidate theorem, falsification test, or bounded certificate, but it must not state or imply that an unsolved conjecture or real-world attribution claim has been proved.

## 한국어 요약

이 검토 문서는 PrimeProject의 공개 문서가 논문 제출 수준의 주장 경계를 유지하는지 정리한다. 논문형 문서로 보려면 지원되는 산출물과 차단된 주장을 분리해야 한다.

- 지원됨: 방어적 키 품질 감사, 합성 생성기 fingerprint 실험, 재현 가능한 bounded open-problem certificate, 공개 안전 수집 계약, 출판 거버넌스 산출물.
- 아직 지원되지 않음: 실세계 생성기 attribution, Bitcoin wallet/library attribution, 암호 소수 예측, 리만가설/콜라츠/골드바흐/Twin Prime의 증명.
- 검토 규칙: 모든 문서는 연구 경로, 후보 정리, 반증 테스트, bounded certificate를 설명할 수 있지만, 미해결 추측이나 실세계 attribution 주장이 증명됐다고 말하면 안 된다.

## Reviewed Documents / 검토 대상 문서

| Document | Manuscript role | Allowed claim | Blocked claim |
| --- | --- | --- | --- |
| `README.md` | project abstract and reproducibility entry point | audited public demo with bounded proof workbench and controlled synthetic evidence | solved conjectures, real-world attribution, cryptographic prime prediction |
| `PrimeProject_Strategic_Review.md` | strategic positioning memo | product/research direction | commercial readiness or novel cryptanalytic break without accepted baselines |
| `docs/PrimeProject_Strategic_Review_V2.md` | advanced strategic review | sim-to-real roadmap and classifier direction | real-world validation already complete |
| `docs/attribution-benchmark-research.md` | controlled benchmark note | synthetic attribution and confound controls | real library attribution |
| `docs/baseline-comparison-research.md` | baseline-comparison design | fingerprint distance framework | production attribution without baselines |
| `docs/bitcoin-practical-research.md` | Bitcoin defensive track | public constants and nonce-risk audit framing | security break from predicting public constants |
| `docs/conjecture-lab.md` | prime-measure experiment note | algorithm-induced observation measures | general prime prediction engine |
| `docs/crypto-prime-catalog.md` | catalog of public cryptographic primes | provenance and parameter recognition | blocked secret-prime recovery |
| `docs/generator-fingerprint-research.md` | generator fingerprint theory | feature extraction and defensive attribution scaffolding | definitive source attribution |
| `docs/open-problem-workbench.md` | open-problem proof lab specification | bounded certificates, AI solver frontier, falsification and proof-obligation tracking | proof of the four open conjectures |
| `docs/prime-regularity-and-crypto-prime-plan.md` | initial research plan | defensive interpretation of prime-generation traces | blocked operational exploitation or blocked private-key recovery |
| `docs/real-world-baseline-research.md` | sim-to-real baseline protocol | collection, provenance, intake, and publication gates | accepted baseline evidence before submission |
| `docs/validation-experiment-results.md` | validation result note | synthetic validation outcomes | deployment-grade attribution |

## 한국어 문서별 판정

| 문서 | 논문상 역할 | 허용되는 주장 | 차단되는 주장 |
| --- | --- | --- | --- |
| `README.md` | 프로젝트 초록 및 재현성 진입점 | bounded proof workbench와 통제 합성 증거를 포함한 감사 가능한 공개 데모 | 난제 해결, 실세계 attribution, 암호 소수 예측 |
| `PrimeProject_Strategic_Review.md` | 전략 포지셔닝 메모 | 제품/연구 방향 제안 | accepted baseline 없는 상용 준비 완료 또는 새로운 암호 해독 성과 |
| `docs/PrimeProject_Strategic_Review_V2.md` | 고도화 전략 검토 | sim-to-real 로드맵과 분류기 방향 | 실세계 검증 완료 주장 |
| `docs/attribution-benchmark-research.md` | 통제 벤치마크 노트 | 합성 attribution과 confound control | 실제 라이브러리 attribution |
| `docs/baseline-comparison-research.md` | 기준군 비교 설계 | fingerprint distance 프레임워크 | 기준군 없는 운영 attribution |
| `docs/bitcoin-practical-research.md` | Bitcoin 방어 트랙 | 공개 상수와 nonce-risk 감사 프레이밍 | 공개 상수 예측을 통한 보안 붕괴 |
| `docs/conjecture-lab.md` | prime-measure 실험 노트 | 알고리즘이 유도한 관측 measure | 일반 소수 예측 엔진 |
| `docs/crypto-prime-catalog.md` | 공개 암호 소수 카탈로그 | provenance와 parameter recognition | 비밀 소수 복원 |
| `docs/generator-fingerprint-research.md` | 생성기 fingerprint 이론 | feature extraction 및 방어적 attribution scaffolding | 단정적 source attribution |
| `docs/open-problem-workbench.md` | 미해결 문제 proof lab 규격 | bounded certificate, AI solver frontier, 반증/증명 의무 추적 | 네 개 난제의 증명 |
| `docs/prime-regularity-and-crypto-prime-plan.md` | 초기 연구 계획 | 소수 생성 흔적의 방어적 해석 | 차단된 운영 공격 또는 차단된 private-key 복구 |
| `docs/real-world-baseline-research.md` | sim-to-real baseline 프로토콜 | 수집, provenance, intake, publication gate | 제출 전 accepted baseline evidence가 이미 있다는 주장 |
| `docs/validation-experiment-results.md` | 검증 결과 노트 | 합성 검증 결과 | 배포 수준 attribution |

## Logical Fixes Applied / 적용한 논리 수정

1. `README.md` points readers to this publication review and states the bilingual claim boundary near the entry point.
2. `README.md` includes explicit English/Korean entry links for GitHub Pages and a Korean reader section that summarizes the supported scope, blocked claims, and main pages.
3. GitHub Pages includes an `EN / KO` switch. The Korean mode localizes the page shell and adds Korean explanation boxes for research panels, but canonical artifact schema labels remain English for reproducibility.
4. `docs/open-problem-workbench.md` has a bilingual abstract and includes the newest proof-workbench schemas, so the document no longer lags behind GitHub Pages.
5. The reviewed-document tables now repeat `blocked`/`차단` inside sensitive blocked-claim cells, reducing the risk that an older planning phrase is read as an endorsed attack or recovery claim.
6. This review records the allowed and blocked claim for every Markdown document, reducing the risk that an older strategic or planning document is read as a proof or real-world attribution result.

## Submission Boundary / 제출 경계

English: A paper submission may present PrimeProject as a reproducible, defensive, claim-gated research framework. It may not present the project as having solved any of the four open conjectures or as having attributed real cryptographic keys to specific libraries without accepted real-world baselines.

한국어: 논문 제출 시 PrimeProject는 재현 가능한 방어적 claim-gated 연구 프레임워크로 제시할 수 있다. 네 개 난제를 해결했다고 쓰거나, accepted real-world baseline 없이 실제 암호 키의 라이브러리 기원을 단정했다고 쓰면 안 된다.

## Required Reviewer Checks / 필수 리뷰어 체크

- Re-run `python scripts/reproduce_publication.py` before submission.
- Re-run `node scripts/verify_pages.cjs` before publishing GitHub Pages changes.
- Confirm that `data/claim_language_audit.json`, `data/evidence_pack.json`, `data/claim_ledger.json`, `data/artifact_lineage.json`, `data/decision_protocol.json`, `data/falsification_battery.json`, and `data/publication_consistency.json` are regenerated after public wording changes.
- Confirm that open-problem pages remain `open_not_proven` until an independently checkable infinite theorem is supplied.
