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
  "TP-TICKET-126 executes the preregistered 32M holdout once: certified residual 0.145872900933948 is below beta=0.23, a fifth finite transition only"

def topAttackTheoremTicket : String :=
  "TP-TICKET-127 DyadicVaughanObstructionContractionAndInterpolation."

def topAttackProofAttemptProtocol : String :=
  "Prove the preregistered recurrence uniformly from actual Vaughan coefficients and an all-X between-scale envelope, or construct a Vaughan-realizable failure; the passing 32M holdout cannot supply either theorem."

def latestFiniteResult : String :=
  "PreregisteredThirtyTwoMillionDyadicContractionHoldout: certified Q falls from 0.834379378078478 to 0.771657434492807 and the certified residual 0.145872900933948 leaves 0.0841270990660519 slack"

def finiteEvidenceBoundary : String :=
  "one preregistered dyadic transition is falsification evidence, not a uniform recurrence, interpolation theorem, parity breakthrough, or exact-gap lower bound"

def retainedOpenPremise : String :=
  "uniform Vaughan-realizable affine contraction plus all-X interpolation and exact-gap positivity"

end PrimeProject.OpenProblems.TwinPrime
