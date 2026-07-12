import numpy as np
from scipy import linalg
import math
import json

def factorial(n):
    return math.factorial(n)

def compute_matrices(d):
    # Get index pairs (i, j) such that i + j <= d
    pairs = []
    for sum_val in range(d + 1):
        for i in range(sum_val + 1):
            j = sum_val - i
            pairs.append((i, j))

    n_vars = len(pairs)
    A = np.zeros((n_vars, n_vars))
    B = np.zeros((n_vars, n_vars))

    for idx1, (i, j) in enumerate(pairs):
        for idx2, (k, l) in enumerate(pairs):
            # A_((i,j), (k,l)) = \iint_{\Delta_2} t_1^{i+k} t_2^{j+l} dt_1 dt_2
            p = i + k
            q = j + l
            A[idx1, idx2] = factorial(p) * factorial(q) / factorial(p + q + 2)

            # B1_((i,j), (k,l)) = \frac{(j+l)! (i+k+2)!}{(i+1)(k+1) (i+k+j+l+3)!}
            b1 = (factorial(j + l) * factorial(i + k + 2)) / ((i + 1) * (k + 1) * factorial(i + k + j + l + 3))

            # B2_((i,j), (k,l)) = \frac{(i+k)! (j+l+2)!}{(j+1)(l+1) (i+k+j+l+3)!}
            b2 = (factorial(i + k) * factorial(j + l + 2)) / ((j + 1) * (l + 1) * factorial(i + k + j + l + 3))

            B[idx1, idx2] = b1 + b2

    return pairs, A, B

def project_symmetric(pairs, A, B):
    # Find unique symmetric pairs (i, j) with i <= j
    sym_pairs = []
    for i, j in pairs:
        if i <= j:
            sym_pairs.append((i, j))

    n_sym = len(sym_pairs)
    # Projection matrix P from symmetric variables to full variables
    # x_full = P * x_sym
    P = np.zeros((len(pairs), n_sym))

    for idx_full, (i, j) in enumerate(pairs):
        # find corresponding sym index
        if i <= j:
            idx_sym = sym_pairs.index((i, j))
        else:
            idx_sym = sym_pairs.index((j, i))
        P[idx_full, idx_sym] = 1.0

    A_sym = P.T @ A @ P
    B_sym = P.T @ B @ P
    return sym_pairs, A_sym, B_sym

def solve_gep(A, B):
    # Solve B x = \lambda A x
    # Since A is positive definite, we can use eigh
    # To avoid numerical instability, add a small regularization if needed
    eigvals = linalg.eigvalsh(B, A)
    return np.max(eigvals)

def main():
    results = {}
    for d in range(1, 9):
        pairs, A, B = compute_matrices(d)

        # Unrestricted (asymmetric allowed)
        max_ratio_unrestricted = solve_gep(A, B)

        # Symmetric restricted
        sym_pairs, A_sym, B_sym = project_symmetric(pairs, A, B)
        max_ratio_symmetric = solve_gep(A_sym, B_sym)

        results[d] = {
            "num_variables_unrestricted": len(pairs),
            "num_variables_symmetric": len(sym_pairs),
            "max_ratio_unrestricted": float(max_ratio_unrestricted),
            "max_ratio_symmetric": float(max_ratio_symmetric),
            "difference": float(max_ratio_unrestricted - max_ratio_symmetric)
        }
        print(f"Degree {d}: Unrestricted={max_ratio_unrestricted:.6f}, Symmetric={max_ratio_symmetric:.6f}, Diff={max_ratio_unrestricted - max_ratio_symmetric:.6e}")

    with open("d:\\Code\\PrimeProject\\scripts\\sieve_optimization_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
