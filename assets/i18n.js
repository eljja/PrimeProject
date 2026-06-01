(function () {
  const STORAGE_KEY = "primeproject.language";
  const DEFAULT_LANGUAGE = "en";
  const SUPPORTED = new Set(["en", "ko"]);

  const dictionary = {
    "brand.title": {
      en: "PrimeProject Conjecture Lab",
      ko: "PrimeProject 추측 연구실",
    },
    "top.github": {
      en: "GitHub",
      ko: "GitHub",
    },
    "top.loading": {
      en: "Loading data",
      ko: "데이터 로딩 중",
    },
    "top.offline": {
      en: "Offline fallback data",
      ko: "오프라인 내장 데이터",
    },
    "top.public": {
      en: "Public JSON data",
      ko: "공개 JSON 데이터",
    },
    "menu.title": {
      en: "PrimeProject Menu",
      ko: "PrimeProject 메뉴",
    },
    "nav.overview": { en: "Overview", ko: "개요" },
    "nav.researchAtlas": { en: "Research Atlas", ko: "연구 지도" },
    "nav.evolution": { en: "Evolution", ko: "진화 기록" },
    "nav.proofWorkbench": { en: "Proof Workbench", ko: "증명 워크벤치" },
    "nav.riemann": { en: "Riemann Hypothesis", ko: "리만가설" },
    "nav.collatz": { en: "Collatz Conjecture", ko: "콜라츠 추측" },
    "nav.goldbach": { en: "Goldbach Conjecture", ko: "골드바흐 추측" },
    "nav.twinPrime": { en: "Twin Prime Workbench", ko: "쌍둥이 소수 워크벤치" },
    "nav.gapMeasure": { en: "Gap Measure", ko: "간극 측도" },
    "nav.biasRanking": { en: "Bias Ranking", ko: "편향 순위" },
    "nav.bitcoinLab": { en: "Bitcoin Lab", ko: "Bitcoin 연구실" },
    "nav.fingerprintLab": { en: "Fingerprint Lab", ko: "Fingerprint 연구실" },
    "nav.baselineLab": { en: "Baseline Lab", ko: "기준군 연구실" },
    "nav.readiness": { en: "Readiness", ko: "준비도" },
    "nav.evidence": { en: "Evidence", ko: "증거 번들" },
    "nav.attributionGrid": { en: "Attribution Grid", ko: "Attribution 격자" },
    "nav.residueDrift": { en: "Residue Drift", ko: "잉여류 드리프트" },
    "nav.gapDistribution": { en: "Gap Distribution", ko: "간극 분포" },
    "nav.snapshots": { en: "Research Snapshots", ko: "연구 스냅샷" },
    "nav.heatmap": { en: "Heatmap", ko: "히트맵" },
    "nav.comparisons": { en: "Comparisons", ko: "비교" },
    "nav.logs": { en: "Logs", ko: "로그" },
    "nav.notes": { en: "Conjecture Notes", ko: "추측 노트" },
    "overview.title": { en: "Prime Index vs Prime Value", ko: "소수 인덱스와 소수값" },
    "overview.subtitle": {
      en: "Generator-weighted observations compared with the baseline p ≈ n log n.",
      ko: "생성기 가중 관측값을 p ≈ n log n 기준선과 비교합니다.",
    },
    "overview.density": { en: "Density", ko: "밀도" },
    "gapDistribution.title": { en: "Gap Distribution", ko: "간극 분포" },
    "gapDistribution.subtitle": {
      en: "Mass of Δ = p_n+1 - p_n by generator.",
      ko: "생성기별 Δ = p_n+1 - p_n 질량입니다.",
    },
    "language.note.title": {
      en: "Language Coverage",
      ko: "언어 전환 범위",
    },
    "language.note.body": {
      en:
        "The switch localizes the page shell, navigation, core headings, and publication-boundary guidance. Research artifacts remain machine-readable and retain their canonical English schema labels.",
      ko:
        "전환 버튼은 페이지 구조, 좌측 메뉴, 핵심 제목, publication boundary 안내를 현지화합니다. 연구 산출물은 재현성을 위해 표준 영문 스키마 라벨을 유지합니다.",
    },
    "atlas.title": { en: "Research Atlas", ko: "연구 지도" },
    "atlas.subtitle": {
      en: "Academic map of what PrimeProject currently supports, what remains blocked, and which proof targets would matter.",
      ko: "PrimeProject가 현재 지원하는 것, 아직 차단된 주장, 의미 있는 증명 목표를 정리한 학술 지도입니다.",
    },
    "evolution.title": { en: "Project Evolution", ko: "프로젝트 진화" },
    "evolution.subtitle": {
      en: "Visual history of the research stack, from prime-measure experiments to publication-gated evidence.",
      ko: "소수 측도 실험에서 publication-gated evidence까지 이어지는 연구 스택의 시각적 기록입니다.",
    },
    "proof.back": { en: "PrimeProject", ko: "PrimeProject" },
    "proof.nav.workbench": { en: "Workbench", ko: "워크벤치" },
    "proof.nav.riemann": { en: "Riemann", ko: "리만" },
    "proof.nav.collatz": { en: "Collatz", ko: "콜라츠" },
    "proof.nav.goldbach": { en: "Goldbach", ko: "골드바흐" },
    "proof.nav.twinPrime": { en: "Twin Prime", ko: "쌍둥이 소수" },
    "proof.hub.eyebrow": { en: "Open Problem Proof Workbench", ko: "미해결 문제 증명 워크벤치" },
    "proof.hub.title": { en: "Proof Workbench", ko: "증명 워크벤치" },
    "proof.hub.body": {
      en:
        "A bounded-evidence workspace for the four open problems tracked by PrimeProject. These pages separate finite computation, falsification checks, proof obligations, and unresolved barriers.",
      ko:
        "PrimeProject가 추적하는 네 미해결 문제의 bounded-evidence 작업 공간입니다. 유한 계산, 반증 검사, 증명 의무, 미해결 장벽을 분리합니다.",
    },
    "proof.hub.status": { en: "status", ko: "상태" },
    "proof.hub.claimLevel": { en: "claim level", ko: "주장 수준" },
    "proof.hub.pages": { en: "pages", ko: "페이지" },
    "proof.card.riemann.body": {
      en:
        "Tracks zero-line evidence, equivalent criteria, proof obligations, and barriers that cannot be discharged by finite verification.",
      ko: "영점선 증거, 동치 기준, 증명 의무, 유한 검증으로 해소할 수 없는 장벽을 추적합니다.",
    },
    "proof.card.collatz.body": {
      en: "Separates trajectory-scale computation from the missing global descent argument needed for a proof.",
      ko: "궤적 규모 계산과 증명에 필요한 전역 descent 논증의 결손을 분리합니다.",
    },
    "proof.card.goldbach.body": {
      en:
        "Organizes even-integer verification, density heuristics, exception search, and the finite-to-infinite gap.",
      ko: "짝수 검증, 밀도 휴리스틱, 예외 탐색, 유한-무한 간극을 정리합니다.",
    },
    "proof.card.twin.body": {
      en:
        "Focuses on prime-pair gaps, residue constraints, admissible patterns, and why bounded twin-prime counts are not yet infinitude.",
      ko: "소수쌍 간극, 잉여류 제약, admissible pattern, bounded twin-prime count가 아직 무한성을 뜻하지 않는 이유를 다룹니다.",
    },
    "proof.open.riemann": { en: "Open Riemann page", ko: "리만 페이지 열기" },
    "proof.open.collatz": { en: "Open Collatz page", ko: "콜라츠 페이지 열기" },
    "proof.open.goldbach": { en: "Open Goldbach page", ko: "골드바흐 페이지 열기" },
    "proof.open.twin": { en: "Open Twin Prime page", ko: "쌍둥이 소수 페이지 열기" },
    "proof.boundary.title": { en: "Research Boundary", ko: "연구 경계" },
    "proof.boundary.body": {
      en:
        "PrimeProject can make failed proof routes visible, reproduce finite evidence, and rank obligations. It must not present a conjecture as solved until an infinite argument survives formal and peer review.",
      ko:
        "PrimeProject는 실패한 증명 경로를 보이게 하고, 유한 증거를 재현하며, 증명 의무의 우선순위를 정할 수 있습니다. 형식 검증과 동료 검토를 통과한 무한 논증 전에는 어떤 추측도 해결됐다고 제시하지 않습니다.",
    },
    "proof.section.verdict": { en: "Proof Verdict", ko: "증명 판정" },
    "proof.section.actualRunner": { en: "Actual Proof Attempt Runner", ko: "실제 증명 시도 러너" },
    "proof.section.lemma": { en: "Candidate Lemma Workbench", ko: "후보 보조정리 워크벤치" },
    "proof.section.machine": { en: "Machine Proof Search Trials", ko: "기계 증명 탐색 실험" },
    "proof.section.formalMatrix": { en: "Formal Upgrade Matrix", ko: "형식화 승격 매트릭스" },
    "proof.section.kernelRoadmap": { en: "Proof Kernel Roadmap", ko: "증명 커널 로드맵" },
    "proof.section.kernelAudit": { en: "Formal Kernel Contract Audit", ko: "형식 커널 계약 감사" },
    "proof.section.shortcut": { en: "Invalid Proof Shortcut Suite", ko: "잘못된 증명 지름길 모음" },
    "proof.section.aiFrontier": { en: "AI Solver Frontier", ko: "AI 풀이 전선" },
    "proof.section.aiBreakthrough": { en: "AI Breakthrough Program", ko: "AI 돌파 프로그램" },
    "proof.section.route": { en: "Proof Route Triage", ko: "증명 경로 분류" },
    "proof.section.spec": { en: "Decisive Theorem Spec", ko: "결정적 정리 규격" },
    "proof.section.subgoals": { en: "Decisive Theorem Subgoals", ko: "결정적 정리 하위 목표" },
    "proof.section.tickets": { en: "Decisive Theorem Attack Tickets", ko: "결정적 정리 공격 티켓" },
    "proof.section.agenda": { en: "Breakthrough Agenda", ko: "돌파구 의제" },
    "proof.section.evidence": { en: "Bounded Evidence", ko: "유한 증거" },
    "proof.section.certificate": { en: "Merkle Certificate", ko: "Merkle 인증서" },
    "proof.section.attempt": { en: "Proof Attempt Ledger", ko: "증명 시도 장부" },
    "proof.section.map": { en: "Proof Attack Map", ko: "증명 공격 지도" },
    "proof.section.statusGate": { en: "Proof Status Gate", ko: "증명 상태 게이트" },
    "proof.section.execution": { en: "Proof Execution Protocol", ko: "증명 실행 프로토콜" },
    "proof.section.frontier": { en: "Proof Frontier Probe", ko: "증명 전선 프로브" },
    "proof.section.barrier": { en: "Known Barrier Audit", ko: "알려진 장벽 감사" },
    "proof.section.replay": { en: "Formal Replay Package", ko: "형식 재생 패키지" },
    "proof.section.review": { en: "Proof Review Docket", ko: "증명 리뷰 문서철" },
    "proof.section.reduction": { en: "Proof Reduction Contract", ko: "증명 환원 계약" },
    "proof.section.intake": { en: "Proof Candidate Intake", ko: "증명 후보 접수" },
    "proof.section.log": { en: "Proof Attempt Execution Log", ko: "증명 시도 실행 로그" },
    "proof.section.dag": { en: "Proof Obligation DAG", ko: "증명 의무 DAG" },
    "proof.section.skeleton": { en: "Formal Skeleton Audit", ko: "형식 스켈레톤 감사" },
    "proof.section.contract": { en: "Formal Proof Contract", ko: "형식 증명 계약" },
    "proof.section.milestones": { en: "Proof Milestone Queue", ko: "증명 마일스톤 큐" },
    "proof.section.lemmaLab": { en: "Decisive Lemma Lab", ko: "결정적 보조정리 연구실" },
    "proof.section.gates": { en: "Proof Gates", ko: "증명 게이트" },
    "proof.section.strategy": { en: "Candidate Strategy", ko: "후보 전략" },
    "proof.section.claimPolicy": { en: "Claim Policy", ko: "주장 정책" },
  };

  function getInitialLanguage() {
    const fromUrl = new URLSearchParams(window.location.search).get("lang");
    if (SUPPORTED.has(fromUrl)) return fromUrl;
    const fromStorage = window.localStorage.getItem(STORAGE_KEY);
    if (SUPPORTED.has(fromStorage)) return fromStorage;
    return DEFAULT_LANGUAGE;
  }

  function translateElement(element, language) {
    const key = element.dataset.i18n;
    const entry = dictionary[key];
    if (!entry) return;
    element.textContent = entry[language] || entry[DEFAULT_LANGUAGE] || "";
  }

  function translateExactText(language) {
    const byEnglish = new Map(
      Object.values(dictionary)
        .filter((entry) => entry && entry.en)
        .map((entry) => [entry.en, entry[language] || entry.en]),
    );
    document
      .querySelectorAll(".proof-page h1, .proof-page h2, .proof-page a, .proof-page button")
      .forEach((element) => {
        if (element.dataset.i18n || element.dataset.langSet) return;
        const original = element.dataset.i18nOriginal || element.textContent.trim();
        if (!byEnglish.has(original)) return;
        element.dataset.i18nOriginal = original;
        element.textContent = language === DEFAULT_LANGUAGE ? original : byEnglish.get(original);
      });
  }

  function applyLanguage(language) {
    const nextLanguage = SUPPORTED.has(language) ? language : DEFAULT_LANGUAGE;
    window.localStorage.setItem(STORAGE_KEY, nextLanguage);
    document.documentElement.lang = nextLanguage;
    document.querySelectorAll("[data-i18n]").forEach((element) => translateElement(element, nextLanguage));
    translateExactText(nextLanguage);
    document.querySelectorAll("[data-lang-set]").forEach((button) => {
      const active = button.dataset.langSet === nextLanguage;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
    window.dispatchEvent(new CustomEvent("primeproject:languagechange", { detail: { language: nextLanguage } }));
  }

  function init() {
    const language = getInitialLanguage();
    document.querySelectorAll("[data-lang-set]").forEach((button) => {
      button.addEventListener("click", () => applyLanguage(button.dataset.langSet));
    });
    applyLanguage(language);
  }

  window.PrimeProjectI18n = {
    apply: () => applyLanguage(getInitialLanguage()),
    setLanguage: applyLanguage,
    getLanguage: getInitialLanguage,
    t: (key, language = getInitialLanguage()) =>
      (dictionary[key] && (dictionary[key][language] || dictionary[key][DEFAULT_LANGUAGE])) || key,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
