"""
Background figure for p1_distributions.tex: the airport data and a power-law sample on
three axes (CDF semi-log, CDF log-log, CCDF log-log). Reuses hw2/code/common.py.

Run from the repo root:  uv run python hw2/00_background/fig_cdf_axes.py
"""

import sys
from pathlib import Path

HW_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HW_DIR / "code"))

import matplotlib.pyplot as plt  # noqa: E402

import common  # noqa: E402

OUT = HW_DIR / "figures" / "bg_cdf_axes.png"


def main() -> None:
    x = common.load_airports()
    # The same sample as in p1a_1_powerlaw.png.
    sample = common.model_samples("airport")["powerlaw"][1]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    panels = [("CDF, log x only (semi-log)", common.ecdf, "linear", "P(X ≤ x)"),
              ("CDF, log-log", common.ecdf, "log", "P(X ≤ x) (log)"),
              ("CCDF, log-log", common.ccdf, "log", "P(X ≥ x) (log)")]
    for ax, (title, curve, yscale, ylabel) in zip(axes, panels):
        ax.plot(*curve(x), color=common.DATA_COLOR, lw=2, label="data")
        ax.plot(*curve(sample), color=common.MODEL_COLOR, lw=2, label="power-law sample")
        ax.set(xscale="log", yscale=yscale, xlabel="routes per airport (log)",
               ylabel=ylabel, title=title)
        ax.legend(loc="lower right" if curve is common.ecdf else "lower left")
    axes[1].annotate("tail squeezed\nagainst 1", xy=(300, 0.99), xytext=(5, 0.4),
                     arrowprops=dict(arrowstyle="->", color=common.INK), color=common.INK)
    fig.suptitle("Airport routes vs power law: the same data on three axes")
    fig.tight_layout()
    fig.savefig(OUT, dpi=160)


if __name__ == "__main__":
    main()
