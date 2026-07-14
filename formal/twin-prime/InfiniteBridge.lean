namespace PrimeProject.OpenProblems.TwinPrime

def missingInfiniteBridge : String :=
  "formal exact gap-2 lower-bound theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExactGapTwoLowerBoundBridge implies primeproject_twin_prime_conjecture"

def requiredProofObjects : List String := [
  "exact-pair selector weight family",
  "parity-barrier survival argument",
  "infinitude bridge from positive exact-gap lower bound"
]

def theoremDecomposition : List String := [
  "TP-TD1 ExactPairSelectorWeights",
  "TP-TD2 ParityBarrierSurvival highest_risk_open",
  "TP-TD3 PositiveExactGapLowerBound",
  "TP-TD4 ExactGapInfinitudeBridge"
]

def breakthroughObjectBlueprint : String :=
  "TP-TD2 exact-pair parity witness that survives semiprime countermodels"

def counterexampleGuidedSynthesis : String :=
  "Twin Prime CEGIS: generate exact-pair weights, reject parity-model and wider-gap leakage"

def rankedCegisTarget : String :=
  "TP-TICKET-114 exactly splits Ramanujan means from centered numerator dispersion and leaves a 4M sign-free finite lower expression of 327951.0"

def topAttackTheoremTicket : String :=
  "TP-TICKET-115 EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget."

def topAttackProofAttemptProtocol : String :=
  "Expand the endpoint coefficients into Mobius/divisor bilinear sums and prove an all-sufficiently-large-X centered numerator second-moment budget with fixed margin; reject abstract non-Vaughan extremizers and finite terminal-run inference."

end PrimeProject.OpenProblems.TwinPrime
