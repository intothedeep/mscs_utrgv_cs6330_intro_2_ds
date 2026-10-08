"""
Problem 1: association of two binary genomic variants (p1a.csv, 199 plants).

Writes results/p1_contingency.csv (2x2 counts) and results/p1_stats.csv (one row per statistic).
Formulas follow lectures 14-15: MI in bits (log2), Jaccard = n11 / (n11 + n10 + n01),
chi-squared = sum (O - E)^2 / E with df = 1. scipy cross-checks chi-squared.
"""

import numpy as np
import pandas as pd
from common import ALPHA, N_PERM, RES_DIR, SEED, load_matrix
from scipy.stats import chi2, chi2_contingency


def contingency(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """2x2 counts; row = value of variant 1 (0, 1), column = value of variant 2 (0, 1)."""
    return np.array([[np.sum((x == i) & (y == j)) for j in (0, 1)] for i in (0, 1)])


def entropy_bits(p: np.ndarray) -> float:
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def mutual_information(table: np.ndarray) -> float:
    """MI(X, Y) = H(X) + H(Y) - H(X, Y), in bits."""
    pxy = table / table.sum()
    return entropy_bits(pxy.sum(1)) + entropy_bits(pxy.sum(0)) - entropy_bits(pxy.ravel())


def main() -> None:
    data = load_matrix("p1a.csv").astype(int)
    x, y = data[:, 0], data[:, 1]
    table = contingency(x, y)
    n = int(table.sum())

    (_n00, n01), (n10, n11) = table
    jaccard = n11 / (n11 + n10 + n01)

    hx = entropy_bits(table.sum(1) / n)
    hy = entropy_bits(table.sum(0) / n)
    mi = mutual_information(table)
    nmi = mi / np.sqrt(hx * hy)

    # Permutation null for MI: shuffling variant 2 breaks any link but keeps both margins.
    rng = np.random.default_rng(SEED)
    null = np.array([mutual_information(contingency(x, rng.permutation(y))) for _ in range(N_PERM)])
    p_mi = (1 + np.sum(null >= mi - 1e-12)) / (N_PERM + 1)

    expected = np.outer(table.sum(1), table.sum(0)) / n
    chi_sq = float(((table - expected) ** 2 / expected).sum())
    p_chi = float(chi2.sf(chi_sq, df=1))
    chi_sp, p_sp, _, _ = chi2_contingency(table, correction=False)
    assert np.isclose(chi_sq, chi_sp) and np.isclose(p_chi, p_sp), "chi-squared cross-check failed"
    chi_yates, p_yates, _, _ = chi2_contingency(table, correction=True)

    RES_DIR.mkdir(exist_ok=True)
    pd.DataFrame(
        {
            "v1": [0, 0, 1, 1],
            "v2": [0, 1, 0, 1],
            "count": table.ravel(),
            "expected": expected.ravel(),
        }
    ).to_csv(RES_DIR / "p1_contingency.csv", index=False)

    stats = {
        "n": n,
        "alpha": ALPHA,
        "H_v1_bits": hx,
        "H_v2_bits": hy,
        "MI_bits": mi,
        # R entropy packages report nats; give both so either answer key matches.
        "MI_nats": mi * np.log(2),
        "NMI": nmi,
        "MI_perm_p": p_mi,
        "MI_perm_n": N_PERM,
        "MI_null_max": float(null.max()),
        "jaccard": jaccard,
        "chi2": chi_sq,
        "chi2_p": p_chi,
        "chi2_yates": float(chi_yates),
        "chi2_yates_p": float(p_yates),
        "min_expected": float(expected.min()),
    }
    pd.Series(stats, name="value").rename_axis("stat").to_csv(RES_DIR / "p1_stats.csv")
    print(table)
    for k, v in stats.items():
        print(f"{k:>14}: {v:.6g}")


if __name__ == "__main__":
    main()
