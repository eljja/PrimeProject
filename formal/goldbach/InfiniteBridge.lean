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
  "GB-TD4b.2b.4b LocalizedOrthogonalArithmeticK56DualCertificate superseded_underspecified",
  "GB-TD4b.2b.5a RobustDualBasisChangeInvarianceAndHaarK56Reduction closed",
  "GB-TD4b.2b.5b UniformEvenGoldbachHaarScaleBudgetBelow56 highest_risk_open",
  "GB-TD5 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-142 UniformEvenGoldbachHaarScaleBudgetBelow56."

def topAttackProofAttemptProtocol : String :=
  "Define normalized Goldbach residuals on every large dyadic even block and prove that the Haar scaling plus scale-wavelet l1 ledger is uniformly at most 56."

def latestExactResult : String :=
  "RobustDualBasisChangeInvarianceAndHaarK56Reduction: honest basis changes preserve robust recovery, while uniform Haar coefficient budget 23 implies pointwise residual below K=56"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "uniform arithmetic bounds for the actual Goldbach Haar scaling and wavelet coefficients on every sufficiently large dyadic even block"

end PrimeProject.OpenProblems.Goldbach
