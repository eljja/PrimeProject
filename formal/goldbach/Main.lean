namespace PrimeProject.OpenProblems.Goldbach

def replayStatus : String := "not_replayable_until_barriers_clear"
def publicClaim : String := "bounded_theorem_only"
def targetTheoremName : String := "primeproject_goldbach_conjecture"
def targetTheoremStatement : String :=
  "theorem primeproject_goldbach_conjecture : forall n : Nat, Even n -> 2 < n -> exists p q : Nat, Nat.Prime p /\\ Nat.Prime q /\\ n = p + q := by"

end PrimeProject.OpenProblems.Goldbach
