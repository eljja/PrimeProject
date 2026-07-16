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
  "GB-TICKET-127 proves the binary singular-series lower bound S(N)>=1, closing normalized A=1 in R(N)=G(N)-S(N)N; only the pointwise signed residual K remains open"

def topAttackTheoremTicket : String :=
  "GB-TICKET-128 ExplicitPointwiseBinaryGoldbachResidualConstant."

def topAttackProofAttemptProtocol : String :=
  "Prove |R(N)|<=K*N/log(N) for every even N>H with an explicit K<42.83274372223497, where R(N)=G(N)-S(N)N and H=4e18."

def latestExactResult : String :=
  "UniformBinaryGoldbachSingularSeriesLowerBound: S(N)>=1 for every positive even N; together with B=2.0949181787429647 this leaves a strict pointwise residual ceiling K<42.83274372223497"

def closedPremise : String :=
  "proper-prime-power contamination constant B and normalized singular-series coefficient A=1"

def retainedOpenPremise : String :=
  "explicit pointwise binary Goldbach residual constant K below 42.83274372223497"

end PrimeProject.OpenProblems.Goldbach
