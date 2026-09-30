"""
Shared code for HW2 Problem 2 (age, first digit, last digit of IMDB-WIKI birth dates).
Each answer has its own script, p2_a_age_plot.py ... p2_d_discussion.py.
"""

import numpy as np
import pandas as pd

from common import DATA_COLOR, DATA_DIR, INK, MODEL_COLOR, FIG_DIR, plt, save

DOB_PATH = DATA_DIR / "01_DoB.txt"
REFERENCE_YEAR = 2026  # ages are 2026 minus birth year (owner/professor direction, 2026-09-23)

# Parsing decisions (checked against the raw year counts, not assumed):
# - Dates are "dd-Mon-yy" or "dd-Mon-yyyy". Every 2-digit year is read as 19yy: IMDB-WIKI was
#   crawled in 2015, so "20"-"24" cannot be 2020-2024, and the counts fall smoothly from the
#   1920s down to "00" with no break that would mark a century switch.
# - Year "0000" is a missing-value placeholder and is dropped.
# - Age = REFERENCE_YEAR - birth year (month/day ignored), kept only if 1 <= age <= 100.

def parse_birth_dates(raw: pd.Series) -> pd.Series:
    """dd-Mon-yy / dd-Mon-yyyy -> Timestamp; 2-digit years -> 19yy; year 0000 -> NaT."""
    parts = raw.str.strip().str.split("-", expand=True)
    year = parts[2].astype(int)
    year = year.where(parts[2].str.len() == 4, 1900 + year)
    year = year.where(year > 0)
    text = parts[0] + "-" + parts[1] + "-" + year.astype("Int64").astype(str)
    return pd.to_datetime(text, format="%d-%b-%Y", errors="coerce")


def compute_ages(birth: pd.Series, reference_year: int) -> pd.Series:
    """Year difference only (month/day ignored), restricted to 1-100."""
    age = (reference_year - birth.dt.year).dropna().astype(int)
    return age[(age >= 1) & (age <= 100)]


def load_birth_dates() -> pd.Series:
    raw = pd.read_csv(DOB_PATH, header=None, names=["dob"], dtype=str)["dob"]
    return parse_birth_dates(raw)


def load_ages() -> pd.Series:
    return compute_ages(load_birth_dates(), REFERENCE_YEAR)


def first_digits(age: pd.Series) -> pd.Series:
    return age.astype(str).str[0].astype(int)


def last_digits(age: pd.Series) -> pd.Series:
    return age % 10


def share_per_value(values: pd.Series, support: range) -> pd.Series:
    return values.value_counts(normalize=True).reindex(support, fill_value=0.0)


def benford() -> pd.Series:
    return pd.Series({d: float(np.log10(1 + 1 / d)) for d in range(1, 10)})


def plot_bars(share: pd.Series, uniform: float | None, title: str, xlabel: str, name: str,
              benford_ref: pd.Series | None = None) -> None:
    FIG_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.set_axisbelow(True)  # grid behind the bars
    ax.bar(share.index, share.to_numpy(), width=0.8, color=DATA_COLOR, edgecolor="white", lw=0.5,
           label="data")
    if uniform is not None:
        ax.axhline(uniform, color=INK, ls="--", lw=1.2, label=f"uniform = {uniform:.3f}")
    if benford_ref is not None:
        ax.plot(benford_ref.index, benford_ref.to_numpy(), color=MODEL_COLOR, marker="o", ms=5,
                lw=2, label="Benford log10(1 + 1/d)")
    if uniform is not None or benford_ref is not None:
        top = max(share.max(), 0.0 if benford_ref is None else benford_ref.max())
        ax.set_ylim(top=top * 1.3)
        ax.legend(loc="upper right", ncol=3)  # headroom + one row keeps the legend off the bars
    ax.set(title=title, xlabel=xlabel, ylabel="share of actors")
    save(fig, name)


REMOVED_COLOR = "#ff7f50"  # coral: ages the 1-100 filter drops


def raw_ages(birth: pd.Series) -> pd.Series:
    """Every parseable age before the 1-100 filter (placeholder years are already NaT)."""
    return (REFERENCE_YEAR - birth.dt.year).dropna().astype(int)


def plot_age_filter(age_all: pd.Series, name: str) -> None:
    """All ages, one bar per year; bars the 1-100 filter removes are coral. Log y, because
    the removed years hold 1.5% of people and would be invisible on a linear axis."""
    FIG_DIR.mkdir(exist_ok=True)
    counts = age_all.value_counts().sort_index()
    is_kept = (counts.index >= 1) & (counts.index <= 100)
    n_kept, n_removed = int(counts[is_kept].sum()), int(counts[~is_kept].sum())
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.set_axisbelow(True)
    ax.bar(counts.index[is_kept], counts[is_kept], width=0.9, color=DATA_COLOR,
           label=f"kept, age 1-100 ({n_kept:,})")
    ax.bar(counts.index[~is_kept], counts[~is_kept], width=0.9, color=REMOVED_COLOR,
           label=f"removed, age > 100 ({n_removed:,}, {n_removed / len(age_all):.1%})")
    ax.axvline(100.5, color=INK, ls="--", lw=1)
    ax.set_yscale("log")
    ax.set(title=f"All ages in {REFERENCE_YEAR} before the filter (n = {len(age_all):,})",
           xlabel="age (years)", ylabel="number of actors (log)")
    ax.legend(loc="upper right")
    save(fig, name)
