namespace PrimeProject.OpenProblems.Goldbach

def missingInfiniteBridge : String :=
  "formal large-even threshold theorem with explicit cutoff"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExplicitGoldbachCutoffBridge implies primeproject_goldbach_conjecture"

def requiredProofObjects : List String := [
  "log-scale moment or hard-stratum maximal minor-arc inequality",
  "verified finite overlap certificate",
  "N0 comparison below the certified finite range"
]

def theoremDecomposition : List String := [
  "GB-TD1 PowersOfTwoUniformHardStratum closed",
  "GB-TD2 FiniteCesaroLpPromotionNoGo closed",
  "GB-TD3 PowerOfTwoMomentDetectionThreshold closed",
  "GB-TD4a SparseHardStratumMomentToMaximumBridge closed",
  "GB-TD4b.1 FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier closed",
  "GB-TD4b.2a SubpowerGrowingWheelLogMomentBarrier closed",
  "GB-TD4b.2b.1 AllScaleOddSquarefreeWheelMomentBarrier closed",
  "GB-TD4b.2b.2 PowerOfTwoBarycentricMomentAnnihilatorNoGo closed",
  "GB-TD4b.2b.3 FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo closed",
  "GB-TD4b.2b.4a PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo closed",
  "GB-TD4b.2b.4b LocalizedOrthogonalArithmeticK56DualCertificate highest_risk_open",
  "GB-TD5 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-141 LocalizedOrthogonalArithmeticK56DualCertificate."

def topAttackProofAttemptProtocol : String :=
  "Replace raw monomial moments by localized orthogonal major/minor-arc measurements and prove that the resulting arithmetic dual norm fits inside the exact K=56 residual margin."

def latestExactResult : String :=
  "PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo: endpoint reconstruction from raw moments has dual norm greater than 2^(q(q-1)/2)"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "a localized orthogonal arithmetic K=56 dual certificate with uniformly controlled norm on the power-of-two hard stratum and explicit large-even glue"

end PrimeProject.OpenProblems.Goldbach
