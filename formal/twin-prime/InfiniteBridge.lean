namespace PrimeProject.OpenProblems.TwinPrime

def missingInfiniteBridge : String :=
  "formal exact gap-2 lower-bound theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExactGapTwoLowerBoundBridge implies primeproject_twin_prime_conjecture"

def requiredProofObjects : List String := [
  "scale-growing exact-pair selector weight family",
  "parity-sensitive separation from every finite-residue composite lift",
  "infinitude bridge from positive exact-gap lower bound"
]

def theoremDecomposition : List String := [
  "TP-TD1 EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts closed",
  "TP-TD2 UnboundedParitySensitiveTwinPairSeparation highest_risk_open",
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
  "TP-TICKET-133 UnboundedParitySensitiveTwinPairSeparation."

def topAttackProofAttemptProtocol : String :=
  "Use scale-growing Type II information to distinguish genuine prime pairs from the composite-composite lift of every admissible fixed residue class, then transfer a signed lower bound to exact gap two."

def latestFiniteResult : String :=
  "EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts: CRT maps every admissible class modulo a finite primorial onto an infinite composite-composite progression with the identical residue pattern"

def finiteEvidenceBoundary : String :=
  "the all-class CRT theorem excludes every fixed-modulus classifier but says nothing against unbounded analytic information and is not a Twin Prime counterexample"

def retainedOpenPremise : String :=
  "unbounded Type II transport, parity-sensitive separation from all finite-residue composite lifts, and positive exact-gap mass"

end PrimeProject.OpenProblems.TwinPrime
