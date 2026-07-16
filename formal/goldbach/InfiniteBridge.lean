namespace PrimeProject.OpenProblems.Goldbach

def missingInfiniteBridge : String :=
  "formal large-even threshold theorem with explicit cutoff"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExplicitGoldbachCutoffBridge implies primeproject_goldbach_conjecture"

def requiredProofObjects : List String := [
  "explicit major/minor arc inequality budget",
  "verified finite overlap certificate",
  "N0 comparison below the certified finite range"
]

def theoremDecomposition : List String := [
  "GB-TD1 ExplicitTwoPrimeBudget",
  "GB-TD2 ErrorTermsReplayable",
  "GB-TD3 CutoffBelowFiniteCertificate highest_risk_open",
  "GB-TD4 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-128 proves the rational tail bound 2*C2>1.31917 and makes the conservative pointwise residual target K=55 sufficient above H=4e18"

def topAttackTheoremTicket : String :=
  "GB-TICKET-129 PointwiseBinaryGoldbachResidualK55."

def topAttackProofAttemptProtocol : String :=
  "Prove |R(N)|<=55*N/log(N) for every even N>H, where R(N)=G(N)-S(N)N and H=4e18; the strengthened singular-series coefficient leaves a rigorous positive endpoint margin."

def latestExactResult : String :=
  "ExplicitTwinConstantTailLowerBound: at M=1000, 2*C2>1.31917; with B<2.1 and 42<log H<43, K=55 leaves endpoint margin above 0.009644249"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "explicit pointwise binary Goldbach residual bound with K at most 55"

end PrimeProject.OpenProblems.Goldbach
