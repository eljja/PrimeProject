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
  "TP-TICKET-128 gives an exact endpoint-only countermodel and proves that a within-dyadic-block envelope yields limsup Q<=0.92*c+delta"

def topAttackTheoremTicket : String :=
  "TP-TICKET-129 VaughanWithinDyadicBlockEnvelopeC1DeltaBelow008."

def topAttackProofAttemptProtocol : String :=
  "Derive Q_X<=Q_(2^j)+delta with delta<0.08 throughout every dyadic block from actual Vaughan coefficients, or construct a Vaughan-realizable interpolation failure; endpoint values alone are invalid."

def latestFiniteResult : String :=
  "DyadicEndpointInsufficiencyAndAllScaleEnvelope: endpoint limsup 0.92 needs the independent condition 0.92*c+delta<1; c=1 requires delta<0.08"

def finiteEvidenceBoundary : String :=
  "the interpolation theorem is exact, but c=1 and delta=0.07 are algebraic candidates rather than proved Vaughan constants, parity breakthroughs, or exact-gap lower bounds"

def retainedOpenPremise : String :=
  "uniform Vaughan raw-budget transport, a within-block envelope satisfying 0.92*c+delta<1, parity survival, and exact-gap positivity"

end PrimeProject.OpenProblems.TwinPrime
