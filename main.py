import numpy as np
import argparse
from sklearn.decomposition import NMF
from sklearn.metrics import adjusted_rand_score
from scipy.optimize import nnls
from coneClustering import *
from nmf import *

def arg_parser():
    parser = argparse.ArgumentParser(description="Iterative subspace clustering with NMF")
    parser.add_argument('--m', type=int, default=50, help='Dimension of the ambient space (default: 50)')
    parser.add_argument('--r', type=int, default=5, help='Dimension (rank) of each subspace (default: 5)')
    parser.add_argument('--n', type=int, default=100, help='Number of points per subspace (default: 100)')
    parser.add_argument('--K', type=int, default=4, help='Number of subspaces (default: 3)')
    parser.add_argument('--sigma', type=float, default=0.0, help='Standard deviation of Gaussian noise (default: 0.0)')
    parser.add_argument('--max_iter', type=int, default=200, help='Maximum number of iterations (default: 50)')
    parser.add_argument('--tol', type=float, default=1e-6, help='Tolerance for stopping criterion (default: 1e-6)')
    parser.add_argument('--random_state', type=int, default=42, help='Random seed for clustering (default: None)')
    parser.add_argument('--NMF_method', choices=['anls', 'NMF'], default='anls', help='NMF method to use')
    parser.add_argument('--NMF_solver', choices=['cd', 'mu'], default='cd', help='Solver for NMF')
    return parser.parse_args()


def main(m, r, n_k, K, sigma=0.0, random_state=None, max_iter=50, tol=1e-6):

    wandb.init(
        project="coneClustering",
        name = "iterativeConeClus-Baseline"
    )
    # 1. Generate distinct subspace data
    X, true_labels = data_simulation(m, r, n_k, K, sigma=sigma, random_state=random_state)

    # 2. Run iterative subspace clustering
    X_new, cluster_labels, errors, accuracy, neg_prop, iterations, loss = coneClus_iterative(
        X, K, r, true_labels, max_iter=max_iter, tol=tol, random_state=random_state
    )

    # 3. Log results
    wandb.log({
        "accuracy": accuracy,
        "reconstruction_error": loss
    })

    print("\n--- Results ---")
    print(f"Clustering Accuracy (ARI): {accuracy:.4f}")
    print(f"Final Reconstruction Loss: {loss:.4f}")

if __name__ == "__main__":
    args = arg_parser()
    m = args.m
    r = args.r
    n_k = args.n
    K = args.K
    sigma = args.sigma
    random_state = args.random_state
    max_iter = args.max_iter
    tol = args.tol
    main(m, r, n_k, K, sigma=sigma, random_state=random_state, max_iter=max_iter, tol=tol)
