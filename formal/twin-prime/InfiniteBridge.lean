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
  "TP-TD3a FiniteCongruenceTranscriptCompositeLift closed",
  "TP-TD3b.1 FiniteRationalFourierAlgebraCompositeLift closed",
  "TP-TD3b.2 AperiodicScaleGrowingTypeIITwinSeparation highest_risk_open",
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
  "TP-TICKET-136 AperiodicScaleGrowingTypeIITwinSeparation."

def topAttackProofAttemptProtocol : String :=
  "Use near-full-scale Type II information that does not factor through W(z) for z<=(1-epsilon)log X, distinguish the n<2Wqr composite lifts, and transfer a signed lower bound to exact gap two."

def latestFiniteResult : String :=
  "FiniteRationalFourierAlgebraCompositeLift: finitely many rational additive characters factor through their denominator lcm and inherit a proper composite-pair CRT witness"

def finiteEvidenceBoundary : String :=
  "the quantitative CRT theorem excludes residue-only z(X)<=(1-epsilon)log X classifiers but says nothing against near-full-scale analytic information and is not a Twin Prime counterexample"

def retainedOpenPremise : String :=
  "an aperiodic scale-growing factor-sensitive Type II separator, its signed transport, and positive exact-gap-two mass"

end PrimeProject.OpenProblems.TwinPrime
