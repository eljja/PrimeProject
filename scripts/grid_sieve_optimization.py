import numpy as np
from scipy import linalg
import json

def solve_grid_sieve(N):
    # Generate grid points
    grid = []
    point_to_idx = {}
    idx = 0
    for i in range(N + 1):
        for j in range(N + 1 - i):
            grid.append((i, j))
            point_to_idx[(i, j)] = idx
            idx += 1

    n_points = len(grid)
    h = 1.0 / N

    # 1. Construct Mass Matrix M (corresponding to J_2)
    # Using simple midpoint/trapezoidal area weights
    M_diag = np.zeros(n_points)
    for idx, (i, j) in enumerate(grid):
        # Weight depends on whether it's an interior, boundary, or corner point on the simplex
        # For simplicity and robust convergence, we use a uniform weight h^2/2 for the simplex triangles.
        # A simple approximation: each grid point represents a small square of area h^2.
        M_diag[idx] = h * h
    M = np.diag(M_diag)

    # 2. Construct Numerator Operator S for I_2^{(1)}
    # S_j(F) = \int_0^{1-t_2} F(t_1, t_2) dt_1  at t_2 = j/N
    # S_j(F) \approx \sum_{i=0}^{N-j} F(i/N, j/N) * h
    S = np.zeros((N + 1, n_points))
    for j in range(N + 1):
        for i in range(N + 1 - j):
            idx_point = point_to_idx[(i, j)]
            S[j, idx_point] = h

    # I_2^{(1)}(F) = \int_0^1 (S_t2(F))^2 dt_2 \approx \sum_{j=0}^{N} (S_j(F))^2 * h
    # This corresponds to the quadratic form F^T (h * S^T * S) F
    N1 = h * (S.T @ S)

    # 3. Construct Numerator Operator R for I_2^{(2)}
    # R_i(F) = \int_0^{1-t_1} F(t_1, t_2) dt_2  at t_1 = i/N
    R = np.zeros((N + 1, n_points))
    for i in range(N + 1):
        for j in range(N + 1 - i):
            idx_point = point_to_idx[(i, j)]
            R[i, idx_point] = h

    N2 = h * (R.T @ R)

    Numerator = N1 + N2

    # Solve GEP: Numerator * v = \lambda * M * v
    # Unrestricted case
    eigvals_unrestricted = linalg.eigvalsh(Numerator, M)
    max_ratio_unrestricted = np.max(eigvals_unrestricted)

    # Symmetric restriction:
    # We construct a projection matrix P from the symmetric space to the full space.
    # A symmetric function satisfies F(i, j) = F(j, i).
    sym_pairs = []
    for i in range(N + 1):
        for j in range(i, N + 1 - i):
            # check if valid point
            if (i, j) in point_to_idx:
                sym_pairs.append((i, j))

    n_sym = len(sym_pairs)
    P = np.zeros((n_points, n_sym))
    for idx_sym, (i, j) in enumerate(sym_pairs):
        idx_full_1 = point_to_idx[(i, j)]
        idx_full_2 = point_to_idx[(j, i)]
        P[idx_full_1, idx_sym] = 1.0
        if idx_full_1 != idx_full_2:
            P[idx_full_2, idx_sym] = 1.0

    M_sym = P.T @ M @ P
    Num_sym = P.T @ Numerator @ P

    eigvals_sym = linalg.eigvalsh(Num_sym, M_sym)
    max_ratio_sym = np.max(eigvals_sym)

    return max_ratio_unrestricted, max_ratio_sym

def main():
    print("Starting Grid Sieve Optimization...")
    results = {}
    for N in [10, 20, 30, 40, 50]:
        unreg, reg = solve_grid_sieve(N)
        results[N] = {
            "unrestricted": float(unreg),
            "symmetric": float(reg),
            "difference": float(unreg - reg)
        }
        print(f"Grid N={N}: Unrestricted={unreg:.6f}, Symmetric={reg:.6f}, Diff={unreg - reg:.6e}")

    with open("d:\\Code\\PrimeProject\\scripts\\grid_sieve_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
