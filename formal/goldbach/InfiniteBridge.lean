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
  "GB-TD4 LogScaleMomentOrMaximalGoldbachResidualK56 highest_risk_open",
  "GB-TD5 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-134 LogScaleMomentOrMaximalGoldbachResidualK56."

def topAttackProofAttemptProtocol : String :=
  "Prove p_X comparable to log X quantitative residual control or a supremum bound with K<=56 on powers of two and rough evens; every sublogarithmic moment regime misses fixed sparse spikes."

def latestExactResult : String :=
  "PowerOfTwoMomentDetectionThreshold: the exact sparse-spike norm is A exp(-log(N_X/J_X)/p_X), with a detection transition at logarithmic moment order"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "an actual binary Goldbach residual estimate at logarithmic moment order or an explicit maximal K56 bound on the minimal-main hard stratum"

end PrimeProject.OpenProblems.Goldbach
