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
  "TP-TICKET-115 separates the full complex cyclotomic mean, improves the scalar-aware budget on six scales, and refutes orientation-free extraction as an improvement"

def topAttackTheoremTicket : String :=
  "TP-TICKET-116 EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget."

def topAttackProofAttemptProtocol : String :=
  "Expand M_q and Z_q into Mobius/divisor bilinear sums, retain Re(M_q H_q), and prove a fixed-margin all-sufficiently-large-X scalar-mean plus complex-centered budget; reject orientation-free mean loss and finite terminal-run inference."

end PrimeProject.OpenProblems.TwinPrime
