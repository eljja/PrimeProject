namespace PrimeProject.OpenProblems.Riemann

def replayStatus : String := "not_replayable_until_barriers_clear"
def publicClaim : String := "bounded_theorem_only"
def targetTheoremName : String := "primeproject_riemann_hypothesis"
def targetTheoremStatement : String :=
  "theorem primeproject_riemann_hypothesis : forall rho, Zeta.NontrivialZero rho -> rho.re = (1/2 : Real) := by"

end PrimeProject.OpenProblems.Riemann
