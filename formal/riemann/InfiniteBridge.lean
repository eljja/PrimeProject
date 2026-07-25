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
  "RH-TD4b.2b.3 EvenTraceMomentSpectralCertificateAndLogOrderBarrier closed",
  "RH-TD4b.2b.4a ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo closed",
  "RH-TD4b.2b.4b ProjectedWeilShiftedLogMomentBelowTailGap highest_risk_open",
  "RH-TD5 WeilPositivityToRHImportAudit"
]

def breakthroughObjectBlueprint : String :=
  "RH-TD2 signed kernel cone plus non-circular positivity certificate"

def counterexampleGuidedSynthesis : String :=
  "RH CEGIS: generate kernel cone candidates, reject circular imports, search adversarial kernels"

def rankedCegisTarget : String :=
  "RH-TICKET-128 proves that compact support removes the infinite prime tail exactly: only prime powers p^m<=B remain in the arithmetic side"

def topAttackTheoremTicket : String :=
  "RH-TICKET-141 ProjectedWeilShiftedLogMomentBelowTailGap."

def topAttackProofAttemptProtocol : String :=
  "Prove an upper spectral input and a logarithmic-order shifted trace-moment bound for the actual projected Weil tail below the independently certified positivity threshold."

def latestExactResult : String :=
  "ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo: a shifted moment sees the negative spectral edge, while every unshifted even moment is identical on opposite scalar spikes"

def retiredRoute : String :=
  "full-test-space autocorrelation-cone density"

def retainedOpenPremise : String :=
  "an upper spectral bound and logarithmic-order shifted moments of the projected Weil tail remain below the one-sided positivity threshold, or a certified strict-negative witness"

end PrimeProject.OpenProblems.Riemann
