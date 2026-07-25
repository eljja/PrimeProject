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
  "GB-TD4b.2b.3 LocalizedPowerOfTwoSignedGoldbachResidualK56 highest_risk_open",
  "GB-TD5 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-139 LocalizedPowerOfTwoSignedGoldbachResidualK56."

def topAttackProofAttemptProtocol : String :=
  "Prove an all-frequency or localized maximal K<=56 estimate for the actual signed binary Goldbach residual on the power-of-two hard stratum, then join it to the explicit large-even cutoff."

def latestExactResult : String :=
  "PowerOfTwoBarycentricMomentAnnihilatorNoGo: for every q there is a nonzero primitive signed signal on q+1 powers of two whose first q polynomial moments vanish exactly"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "a localized K=56 signed binary Goldbach residual bound on the power-of-two hard stratum with explicit large-even glue"

end PrimeProject.OpenProblems.Goldbach
