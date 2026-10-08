"""
Shared paths and helpers for HW4 (pairwise association).

Steps:   p1_association.py  binary pair p1a.csv: 2x2 table, MI, Jaccard, chi-squared -> results/
         p2_correlation.py  continuous pairs p2a/b/c.csv: Pearson r, p, scatter plots -> results/, figures/
         p3_report_tables.py  saved results -> LaTeX macros and tables in report/tables/
Run all: uv run python hw4/code/run_all.py

p1b.csv (199 x 15) ships with the data but no part of the assignment uses it.
"""

import math
from pathlib import Path

import numpy as np

__all__ = [
    "ALPHA",
    "DATA_DIR",
    "FIG_DIR",
    "GRID",
    "INK",
    "N_PERM",
    "PAIRS",
    "RES_DIR",
    "SEED",
    "TAB_DIR",
    "load_matrix",
    "sci",
]

HW_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = HW_DIR / "data"
RES_DIR = HW_DIR / "results"
FIG_DIR = HW_DIR / "figures"
TAB_DIR = HW_DIR / "report" / "tables"

# Significance level for every test in the report, fixed before looking at the results.
ALPHA = 0.05
# Permutation test for MI (lecture 15, slide 26): shuffles of variable 2.
N_PERM = 10_000
SEED = 6330

# Problem 2 parts and their files.
PAIRS = {"a": "p2a.csv", "b": "p2b.csv", "c": "p2c.csv"}

INK = "#52514e"
GRID = "#e4e3df"


def load_matrix(name: str) -> np.ndarray:
    """Headerless CSV -> float array, one row per sample."""
    return np.loadtxt(DATA_DIR / name, delimiter=",", ndmin=2)


def sci(log10_value: float, digits: int = 2) -> tuple[float, int]:
    """log10 of a tiny number -> (mantissa, exponent); avoids float underflow to 0."""
    exp = math.floor(log10_value)
    mant = 10 ** (log10_value - exp)
    if round(mant, digits) >= 10:
        mant, exp = mant / 10, exp + 1
    return mant, exp
