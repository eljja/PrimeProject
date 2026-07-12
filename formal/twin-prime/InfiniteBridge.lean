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
  "TP-TICKET-112 isolates 162 Farey-cell endpoint sums and refutes independent endpoint triangles after exact Abel reduction"

def topAttackTheoremTicket : String :=
  "TP-TICKET-113 UniformFareyCellEndpointCancellationForVaughanCrossSpectrum."

def topAttackProofAttemptProtocol : String :=
  "Prove a uniform one-sided cancellation estimate for the fixed Farey-cell endpoint sums from Vaughan bilinear coefficients and weighted large-sieve geometry; reject endpoint triangles and finite-holdout inference."

end PrimeProject.OpenProblems.TwinPrime
