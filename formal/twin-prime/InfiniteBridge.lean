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
  "TP-TICKET-124 proves the exact limsup criterion for the canonical joint obstruction and refutes necessity of the overstrong coordinatewise ratio triple"

def topAttackTheoremTicket : String :=
  "TP-TICKET-125 VaughanCanonicalObstructionLimsup."

def topAttackProofAttemptProtocol : String :=
  "For Q_X=((S_X-D_X)+E_X)/K_X, prove limsup Q_X<1 from the actual Vaughan bilinear arithmetic while preserving paired-boundary compensation, or construct a Vaughan-realizable unbounded subsequence with Q_X>=1."

end PrimeProject.OpenProblems.TwinPrime
