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
  "TP-TICKET-121 rationalizes low-pair saving into balance times angle defect and refutes both angle-only and balance-only fixed-saving routes"

def topAttackTheoremTicket : String :=
  "TP-TICKET-122 VaughanOuterDivisorKernelBalancedDecorrelatedMass."

def topAttackProofAttemptProtocol : String :=
  "Expand each first-pair cross Gram entry as a signed outer-divisor kernel, prove positive Farey-denominator mass with norm balance and angular decorrelation, and reject both norm-imbalanced anti-alignment and balanced near-alignment countermodels."

end PrimeProject.OpenProblems.TwinPrime
