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
  "TP-TICKET-113 groups 162 Farey endpoints into 31 right-denominator blocks, survives a fresh 4M holdout, and refutes magnitude-label-only cancellation"

def topAttackTheoremTicket : String :=
  "TP-TICKET-114 UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum."

def topAttackProofAttemptProtocol : String :=
  "Prove a uniform one-sided budget for the 31 canonical right-denominator endpoint blocks from Vaughan bilinear coefficient phases; reject magnitude-label-only arguments, abstract non-Vaughan adversaries, and finite-holdout inference."

end PrimeProject.OpenProblems.TwinPrime
