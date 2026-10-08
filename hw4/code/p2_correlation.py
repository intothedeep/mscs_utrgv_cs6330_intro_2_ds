"""
Problem 2: Pearson correlation of two genes in p2a/p2b/p2c.csv, its p-value, and scatter plots.

p-value: two-sided t-test of H0 rho = 0, t = r sqrt(n-2) / sqrt(1-r^2), df = n-2 (lecture 14,
slide 34). log10 p is kept too, because p can underflow to 0 in float64 for large n.
Writes results/p2_stats.csv and figures/scatter_<part>.png.
"""

import math

import matplotlib

matplotlib.use("Agg")  # files only; this pyenv build has no Tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import ALPHA, FIG_DIR, GRID, INK, PAIRS, RES_DIR, load_matrix
from scipy.stats import pearsonr, spearmanr, t


def pearson_test(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    n = len(x)
    r = float(np.corrcoef(x, y)[0, 1])
    df = n - 2
    t_stat = r * math.sqrt(df) / math.sqrt(1 - r * r)
    log10_p = (math.log(2) + t.logsf(abs(t_stat), df)) / math.log(10)
    res = pearsonr(x, y)
    assert np.isclose(r, res.statistic), "Pearson r cross-check failed"
    if res.pvalue > 1e-300:
        assert np.isclose(10**log10_p, res.pvalue, rtol=1e-6), "p-value cross-check failed"
    return {
        "n": n,
        "r": r,
        "t": t_stat,
        "df": df,
        "p": float(res.pvalue),
        "log10_p": log10_p,
        "spearman": float(spearmanr(x, y).statistic),
        # V-shaped pairs (gene 2 ~ |gene 1|) show here, not in r.
        "r_abs_x": float(np.corrcoef(np.abs(x), y)[0, 1]),
    }


def scatter(part: str, x: np.ndarray, y: np.ndarray, r: float, lims: tuple[float, float]) -> None:
    fig, ax = plt.subplots(figsize=(2.35, 2.5), layout="constrained")
    ax.scatter(x, y, s=3, alpha=0.45, color=INK, edgecolors="none")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7.5)
    ax.grid(color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_xlabel("Gene 1 expression", fontsize=8)
    ax.set_ylabel("Gene 2 expression", fontsize=8)
    ax.set_title(f"({part}) n = {len(x)}, r = {r:.3f}", fontsize=8)
    fig.savefig(FIG_DIR / f"scatter_{part}.png", dpi=200)
    plt.close(fig)


def main() -> None:
    plt.rcParams["font.family"] = ["Apple SD Gothic Neo", "DejaVu Sans"]
    data = {part: load_matrix(name) for part, name in PAIRS.items()}
    # One shared axis range so the three plots compare at the same scale.
    span = max(np.abs(d).max() for d in data.values())
    lims = (-math.ceil(span), math.ceil(span))

    RES_DIR.mkdir(exist_ok=True)
    FIG_DIR.mkdir(exist_ok=True)
    rows = []
    for part, d in data.items():
        st = pearson_test(d[:, 0], d[:, 1])
        st["reject_h0"] = st["log10_p"] < math.log10(ALPHA)
        rows.append({"part": part, "file": PAIRS[part], **st})
        scatter(part, d[:, 0], d[:, 1], st["r"], lims)

    # p2b's gene 1 is the first 110 values of p2c's gene 1; the discussion cites this.
    shared = bool(np.array_equal(data["b"][:, 0], data["c"][: len(data["b"]), 0]))

    out = pd.DataFrame(rows)
    out["b_gene1_is_c_prefix"] = shared
    out.to_csv(RES_DIR / "p2_stats.csv", index=False)
    print(out.to_string())


if __name__ == "__main__":
    main()
