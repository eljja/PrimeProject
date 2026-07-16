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
  "TP-TICKET-127 proves that normalized affine contraction is equivalent to raw adverse-numerator transport and decomposes the 32M residual into paired 0.14135151084290043 plus boundary 0.004521390091047683"

def topAttackTheoremTicket : String :=
  "TP-TICKET-128 UniformVaughanRawBudgetTransportAndInterpolation."

def topAttackProofAttemptProtocol : String :=
  "Prove raw adverse-numerator and positive-denominator transport uniformly from actual Vaughan coefficients plus an all-X interpolation envelope, or construct a Vaughan-realizable failure."

def latestFiniteResult : String :=
  "RawBudgetTransportIffNormalizedAffineContraction: at 16M-to-32M the adverse numerator grows by 1.8603305083667954 while the positive denominator grows by 2.0115420952456007"

def finiteEvidenceBoundary : String :=
  "one preregistered dyadic transition is falsification evidence, not a uniform recurrence, interpolation theorem, parity breakthrough, or exact-gap lower bound"

def retainedOpenPremise : String :=
  "uniform Vaughan raw-budget transport plus all-X interpolation, parity survival, and exact-gap positivity"

end PrimeProject.OpenProblems.TwinPrime
