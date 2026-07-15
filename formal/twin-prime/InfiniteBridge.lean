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
  "TP-TICKET-122 proves the exact all-canonical-pair scalar-vector saving identity and refutes both first-pair-only and centered-only global-saving routes"

def topAttackTheoremTicket : String :=
  "TP-TICKET-123 VaughanCanonicalPairJointDefectAndResidualBudgetGap."

def topAttackProofAttemptProtocol : String :=
  "Prove a fixed positive normalized surplus for the exact canonical mean-plus-centered saving after every outer pair, residual shell, and boundary term, or construct a Vaughan-realizable unbounded sequence with nonpositive or vanishing surplus."

end PrimeProject.OpenProblems.TwinPrime
