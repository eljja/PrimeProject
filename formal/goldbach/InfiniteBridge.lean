namespace PrimeProject.OpenProblems.Goldbach

def missingInfiniteBridge : String :=
  "formal large-even threshold theorem with explicit cutoff"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExplicitGoldbachCutoffBridge implies primeproject_goldbach_conjecture"

def requiredProofObjects : List String := [
  "hard-stratum maximal minor-arc inequality",
  "verified finite overlap certificate",
  "N0 comparison below the certified finite range"
]

def theoremDecomposition : List String := [
  "GB-TD1 PowersOfTwoUniformHardStratum closed",
  "GB-TD2 FiniteCesaroLpPromotionNoGo closed",
  "GB-TD3 HardStratumMaximalBinaryGoldbachResidualK56 highest_risk_open",
  "GB-TD4 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-133 HardStratumMaximalBinaryGoldbachResidualK56."

def topAttackProofAttemptProtocol : String :=
  "Prove a supremum or maximal residual bound with K<=56 on powers of two and rough even integers above the finite cutoff; finite Cesaro Lp control is invalid because exact sparse spikes can defeat every such average."

def latestExactResult : String :=
  "PowerOfTwoSparseSpikesDefeatEveryFiniteCesaroLpBridge: a residual perturbation supported on 2^j has every fixed finite-Lp Cesaro mean tending to zero while reversing the exact K56 endpoint margin at every power of two"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "explicit maximal pointwise binary Goldbach residual bound with K at most 56 on the minimal-main hard stratum"

end PrimeProject.OpenProblems.Goldbach
