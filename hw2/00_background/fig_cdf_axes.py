"""
Background figure for p1_distributions.tex: the airport data and a power-law sample on
three axes (CDF semi-log, CDF log-log, CCDF log-log). Reuses hw2/code/p1.py.

Run from the repo root:  uv run python hw2/00_background/fig_cdf_axes.py
"""

import sys
from pathlib import Path

HW_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HW_DIR / "code"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import p1  # noqa: E402

OUT = HW_DIR / "figures" / "bg_cdf_axes.png"


def main() -> None:
    x = pd.read_csv(p1.DATA_DIR / "01_airport_routes.csv")["NumberOfRoutes"].to_numpy(float)
    # Same seed and call order as p1.py, so this is the sample in p1a_1_powerlaw.png.
    sample = p1.sample_models(x, np.random.default_rng(p1.SEED))["powerlaw"][1]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    panels = [("CDF, log x only (semi-log)", p1.ecdf, "linear", "P(X ≤ x)"),
              ("CDF, log-log", p1.ecdf, "log", "P(X ≤ x) (log)"),
              ("CCDF, log-log", p1.ccdf, "log", "P(X ≥ x) (log)")]
    for ax, (title, curve, yscale, ylabel) in zip(axes, panels):
        ax.plot(*curve(x), color=p1.DATA_COLOR, lw=2, label="data")
        ax.plot(*curve(sample), color=p1.MODEL_COLOR, lw=2, label="power-law sample")
        ax.set(xscale="log", yscale=yscale, xlabel="routes per airport (log)",
               ylabel=ylabel, title=title)
        ax.legend(loc="lower right" if curve is p1.ecdf else "lower left")
    axes[1].annotate("tail squeezed\nagainst 1", xy=(300, 0.99), xytext=(5, 0.4),
                     arrowprops=dict(arrowstyle="->", color=p1.INK), color=p1.INK)
    fig.suptitle("Airport routes vs power law: the same data on three axes")
    fig.tight_layout()
    fig.savefig(OUT, dpi=160)


if __name__ == "__main__":
    main()
