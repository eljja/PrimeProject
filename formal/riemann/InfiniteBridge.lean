namespace PrimeProject.OpenProblems.Riemann

def missingInfiniteBridge : String :=
  "formal all-x prime-counting error theorem plus formal RH-equivalence bridge"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "KernelConePositivityBridge implies primeproject_riemann_hypothesis"

def requiredProofObjects : List String := [
  "two-moment projected core definition",
  "rational-congruence interval certificates for strict finite Gram signs",
  "uniform projected Weil Gram-tail certificate or one strict negative witness"
]

def theoremDecomposition : List String := [
  "RH-TD1 ConstraintPreservingEnumerableWeilCoreProjection closed",
  "RH-TD2 ProjectedWeilCoreGramFamilyEquivalence closed",
  "RH-TD3 RationalCongruenceIntervalDichotomy closed",
  "RH-TD4a SharpBlockTailPositivityCertificate closed",
  "RH-TD4b.1 SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo closed",
  "RH-TD4b.2a HadamardCancellationSchurOverestimateNoGo closed",
  "RH-TD4b.2b.1 CrossGramCorrelationBlockPositivityCriterion closed",
  "RH-TD4b.2b.2 TwoMutuallyUnbiasedBasesCrossGramL1NoGo closed",
  "RH-TD4b.2b.3 ProjectedWeilSignedGramSpectralRadiusBelowTailGap highest_risk_open",
  "RH-TD5 WeilPositivityToRHImportAudit"
]

def breakthroughObjectBlueprint : String :=
  "RH-TD2 signed kernel cone plus non-circular positivity certificate"

def counterexampleGuidedSynthesis : String :=
  "RH CEGIS: generate kernel cone candidates, reject circular imports, search adversarial kernels"

def rankedCegisTarget : String :=
  "RH-TICKET-128 proves that compact support removes the infinite prime tail exactly: only prime powers p^m<=B remain in the arithmetic side"

def topAttackTheoremTicket : String :=
  "RH-TICKET-139 ProjectedWeilSignedGramSpectralRadiusBelowTailGap."

def topAttackProofAttemptProtocol : String :=
  "Estimate the signed spectral radius of the projected Weil Gram tail directly, preserving cancellation instead of replacing it by an absolute cross-Gram row budget."

def latestExactResult : String :=
  "TwoMutuallyUnbiasedBasesCrossGramL1NoGo: a tight frame has exact squared operator norm one while the absolute cross-Gram bound grows as (1+sqrt N)/2"

def retiredRoute : String :=
  "full-test-space autocorrelation-cone density"

def retainedOpenPremise : String :=
  "the projected Weil signed Gram spectral radius is uniformly smaller than the positive tail-gap product, or a certified strict-negative witness"

end PrimeProject.OpenProblems.Riemann
