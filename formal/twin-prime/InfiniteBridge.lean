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
  "TP-TICKET-120 proves the exact low-pair triangle saving identity and refutes every weak-contract fixed positive saving fraction with an aligned rank-one Gram witness"

def topAttackTheoremTicket : String :=
  "TP-TICKET-121 VaughanLowDivisorDenominatorSummedAngleGap."

def topAttackProofAttemptProtocol : String :=
  "Expand the first canonical factor-four outer-divisor pair into signed Mobius bilinear sums and derive a denominator-summed centered-angle gap from arithmetic phase relations; use the aligned rank-one model as a mandatory weak-contract counterexample and reject mean-sign or finite-cosine extrapolation."

end PrimeProject.OpenProblems.TwinPrime
