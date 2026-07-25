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
  "GB-TD4b.2b.2 PointwiseSignedBinaryGoldbachResidualK56 highest_risk_open",
  "GB-TD5 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-138 PointwiseSignedBinaryGoldbachResidualK56."

def topAttackProofAttemptProtocol : String :=
  "Prove a pointwise signed binary residual bound with K<=56 and join it to the explicit large-even cutoff; every complete-block odd squarefree wheel scale still has at least sqrt(X/2) hard points."

def latestExactResult : String :=
  "AllScaleOddSquarefreeWheelMomentBarrier: every complete-block scale X=2WM has |H_W(X)|>=sqrt(X/2), including M=1 near-full wheel scales"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "a K=56 pointwise signed binary Goldbach residual bound with explicit large-even glue"

end PrimeProject.OpenProblems.Goldbach
