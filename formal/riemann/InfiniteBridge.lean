namespace PrimeProject.OpenProblems.Riemann

def missingInfiniteBridge : String :=
  "formal all-x prime-counting error theorem plus formal RH-equivalence bridge"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "KernelConePositivityBridge implies primeproject_riemann_hypothesis"

def requiredProofObjects : List String := [
  "admissible kernel cone definition",
  "non-circular explicit-formula positivity lemma",
  "density bridge into the RH-equivalent test class"
]

def theoremDecomposition : List String := [
  "RH-TD1 AdmissibleKernelCone",
  "RH-TD2 NonCircularExplicitFormulaPositivity highest_risk_open",
  "RH-TD3 KernelConeDensityBridge",
  "RH-TD4 TargetImportAudit"
]

def breakthroughObjectBlueprint : String :=
  "RH-TD2 signed kernel cone plus non-circular positivity certificate"

def counterexampleGuidedSynthesis : String :=
  "RH CEGIS: generate kernel cone candidates, reject circular imports, search adversarial kernels"

def rankedCegisTarget : String :=
  "RH-TICKET-128 proves that compact support removes the infinite prime tail exactly: only prime powers p^m<=B remain in the arithmetic side"

def topAttackTheoremTicket : String :=
  "RH-TICKET-129 ArchimedeanIntervalAndAdmissibleCoreDensity."

def topAttackProofAttemptProtocol : String :=
  "Construct a proved dense compact-support Weil core and certify its archimedean contribution by convergent intervals; the prime-power side is already finite, but finite non-discovery is not RH positivity."

def latestExactResult : String :=
  "CompactSupportFinitePrimeSideReduction: support in [-log B,log B] leaves exactly the finite prime-power pairs p^m<=B; B=1000000 has 78734 terms"

def retiredRoute : String :=
  "full-test-space autocorrelation-cone density"

def retainedOpenPremise : String :=
  "admissible-core density, archimedean interval evaluation, and direct all-test positivity or a certified negative witness"

end PrimeProject.OpenProblems.Riemann
