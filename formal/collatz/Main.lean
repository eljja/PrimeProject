namespace PrimeProject.OpenProblems.Collatz

def replayStatus : String := "not_replayable_until_barriers_clear"
def publicClaim : String := "bounded_theorem_only"
def targetTheoremName : String := "primeproject_collatz_conjecture"
def targetTheoremStatement : String :=
  "theorem primeproject_collatz_conjecture : forall n : Nat, 0 < n -> exists k, Collatz.iterate k n = 1 := by"

end PrimeProject.OpenProblems.Collatz
