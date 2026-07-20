namespace PrimeProject.OpenProblems.TwinPrime

def missingInfiniteBridge : String :=
  "formal exact gap-2 lower-bound theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExactGapTwoLowerBoundBridge implies primeproject_twin_prime_conjecture"

def requiredProofObjects : List String := [
  "scale-growing exact-pair selector weight family",
  "near-full-scale parity-sensitive separation from quantitative primorial composite lifts",
  "infinitude bridge from positive exact-gap lower bound"
]

def theoremDecomposition : List String := [
  "TP-TD1 EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts closed",
  "TP-TD2 ScaleDependentPrimorialCompositeLiftBound closed",
  "TP-TD3 NearFullScaleParitySensitiveTwinSeparation highest_risk_open",
  "TP-TD4 PositiveExactGapLowerBound",
  "TP-TD5 ExactGapInfinitudeBridge"
]

def breakthroughObjectBlueprint : String :=
  "TP-TD2 exact-pair parity witness that survives semiprime countermodels"

def counterexampleGuidedSynthesis : String :=
  "Twin Prime CEGIS: generate exact-pair weights, reject parity-model and wider-gap leakage"

def rankedCegisTarget : String :=
  "TP-TICKET-128 gives an exact endpoint-only countermodel and proves that a within-dyadic-block envelope yields limsup Q<=0.92*c+delta"

def topAttackTheoremTicket : String :=
  "TP-TICKET-134 NearFullScaleParitySensitiveTwinSeparation."

def topAttackProofAttemptProtocol : String :=
  "Use near-full-scale Type II information that does not factor through W(z) for z<=(1-epsilon)log X, distinguish the n<2Wqr composite lifts, and transfer a signed lower bound to exact gap two."

def latestFiniteResult : String :=
  "ScaleDependentPrimorialCompositeLiftBound: every admissible a mod W has a composite-pair witness below 2Wqr, extending the residue-only obstruction to growing primorial levels"

def finiteEvidenceBoundary : String :=
  "the quantitative CRT theorem excludes residue-only z(X)<=(1-epsilon)log X classifiers but says nothing against near-full-scale analytic information and is not a Twin Prime counterexample"

def retainedOpenPremise : String :=
  "near-full-scale Type II transport, parity-sensitive separation from quantitative composite lifts, and positive exact-gap mass"

end PrimeProject.OpenProblems.TwinPrime
