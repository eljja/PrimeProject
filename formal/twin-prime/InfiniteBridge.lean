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
  "TP-TICKET-125 proves an affine dyadic contraction implies a limsup below one and freezes alpha=3/4 beta=23/100 as finite candidate data only"

def topAttackTheoremTicket : String :=
  "TP-TICKET-126 DyadicVaughanObstructionContractionAndInterpolation."

def topAttackProofAttemptProtocol : String :=
  "Preregister a 32M falsification holdout for Q_(2X)<=3*Q_X/4+23/100, then independently prove the recurrence from actual Vaughan coefficients and an all-X between-scale envelope, or construct a Vaughan-realizable unbounded failure sequence."

end PrimeProject.OpenProblems.TwinPrime
