import numpy as np
from scipy import linalg
import math
import json

def factorial(n):
    return math.factorial(n)

def compute_fractional_matrices(d, alpha=0.5):
    # Get index pairs (i, j) such that i + j <= d
    pairs = []
    for sum_val in range(d + 1):
        for i in range(sum_val + 1):
            j = sum_val - i
            pairs.append((i, j))

    n_vars = len(pairs)
    A = np.zeros((n_vars, n_vars))
    B = np.zeros((n_vars, n_vars))

    # We will introduce a symmetry-breaking operator T_alpha acting on the coefficients.
    # Specifically, we perturb the numerator matrix B to B_perturbed = B + \epsilon * (K - K.T)
    # where K represents the coupling of the polynomial with its fractional derivative.
    # For a simple representation, let's define K_{(i,j), (k,l)} as the coupling:
    # \iint_{\Delta_2} t_1^i t_2^j \cdot (d^\alpha/dt_1^\alpha)[t_1^k] t_2^l dt_1 dt_2
    # Using the Riemann-Liouville fractional derivative:
    # d^\alpha/dt^\alpha [t^k] = \frac{\Gamma(k+1)}{\Gamma(k+1-\alpha)} t^{k-\alpha}
    # Thus, the integral is:
    # \frac{\Gamma(k+1)}{\Gamma(k+1-\alpha)} \iint_{\Delta_2} t_1^{i+k-\alpha} t_2^{j+l} dt_1 dt_2
    # = \frac{\Gamma(k+1)}{\Gamma(k+1-\alpha)} \frac{\Gamma(i+k+1-\alpha) \Gamma(j+l+1)}{\Gamma(i+k+j+l+2-\alpha)}

    K = np.zeros((n_vars, n_vars))
    for idx1, (i, j) in enumerate(pairs):
        for idx2, (k, l) in enumerate(pairs):
            # compute standard A and B
            p = i + k
            q = j + l
            A[idx1, idx2] = factorial(p) * factorial(q) / factorial(p + q + 2)

            b1 = (factorial(j + l) * factorial(i + k + 2)) / ((i + 1) * (k + 1) * factorial(i + k + j + l + 3))
            b2 = (factorial(i + k) * factorial(j + l + 2)) / ((j + 1) * (l + 1) * factorial(i + k + j + l + 3))
            B[idx1, idx2] = b1 + b2

            # compute fractional coupling K
            if k >= 0:
                g_k = math.gamma(k + 1)
                g_k_alpha = math.gamma(k + 1 - alpha)
                g_num = math.gamma(i + k + 1 - alpha)
                g_den = math.gamma(i + k + j + l + 2 - alpha)
                K[idx1, idx2] = (g_k / g_k_alpha) * (g_num * factorial(j + l)) / g_den

    return pairs, A, B, K

def main():
    d = 4
    alpha = 0.5
    pairs, A, B, K = compute_fractional_matrices(d, alpha)

    results = []
    # Test different coupling strengths epsilon
    for eps in np.linspace(0.0, 0.5, 6):
        # The perturbed numerator matrix is symmetric:
        # We add a symmetric perturbation based on the fractional coupling:
        # B_perturbed = B + eps * (K + K.T)
        B_perturbed = B + eps * (K + K.T)

        # Check if the GEP ratio increases
        max_ratio = np.max(linalg.eigvalsh(B_perturbed, A))
        results.append({
            "epsilon": float(eps),
            "max_ratio": float(max_ratio)
        })
        print(f"Epsilon={eps:.2f}: Max Ratio={max_ratio:.6f}")

    with open("d:\\Code\\PrimeProject\\scripts\\hilbert_sieve_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
