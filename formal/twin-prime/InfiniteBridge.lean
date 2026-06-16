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
  "TP-CEGIS-12 attack_next"

def topAttackTheoremTicket : String :=
  "TP-TICKET-12 PolignacGapsFredholmTracyWidomDysonCircular: Polignac multi-gap prime pairs satisfy joint Fredholm determinant Airy kernel Tracy-Widom Dyson circular ensemble scaling."

def topAttackProofAttemptProtocol : String :=
  "Compute exact Polignac prime pair counts for gaps g in {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36}; calculate the joint covariance matrix and its Dyson circular ensemble determinant; audit Fredholm trace scaling against GUE/GOE Airy kernel Dyson circular ensemble predictions."

end PrimeProject.OpenProblems.TwinPrime
