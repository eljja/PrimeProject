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
  "TP-TICKET-116 lifts the cyclotomic endpoint into exact Mobius sign layers and refutes independent sign-layer triangles on all six scales"

def topAttackTheoremTicket : String :=
  "TP-TICKET-117 EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget."

def topAttackProofAttemptProtocol : String :=
  "Estimate the signed outer-Mobius endpoint functional before norms, or prove a denominator-summed covariance lower bound with a fixed all-sufficiently-large-X margin; reject independent sign-layer triangles and finite covariance-sign inference."

end PrimeProject.OpenProblems.TwinPrime
