"""
Problem 2: age, first digit and last digit of IMDB-WIKI birth dates.

Parsing decisions (checked against the raw year counts, not assumed):
- Dates are "dd-Mon-yy" or "dd-Mon-yyyy". Every 2-digit year is read as 19yy: IMDB-WIKI was
  crawled in 2015, so "20"-"24" cannot be 2020-2024, and the counts fall smoothly from the
  1920s down to "00" with no break that would mark a century switch.
- Year "0000" is a missing-value placeholder and is dropped.
- Age = REFERENCE_YEAR - birth year (year difference only, month/day ignored), kept only if
  1 <= age <= 100. Per owner/professor direction (2026-09-23): 2026 is the reference year,
  and ages outside [1, 100] are dropped as unreasonable.

Run from the repo root:  uv run python hw2/code/p2.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: write PNGs only, no GUI backend needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HW_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = HW_DIR / "00_doc" / "01_DoB.txt"
FIG_DIR = HW_DIR / "figures"
REFERENCE_YEAR = 2026

DATA_COLOR = "#2a78d6"
BENFORD_COLOR = "#eb6834"
INK = "#52514e"
GRID = "#e4e3df"

plt.rcParams.update({
    "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 10, "axes.titlesize": 11, "legend.frameon": False,
})


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


def share_per_value(values: pd.Series, support: range) -> pd.Series:
    return values.value_counts(normalize=True).reindex(support, fill_value=0.0)


def plot_bars(share: pd.Series, uniform: float | None, title: str, xlabel: str, name: str,
              benford: pd.Series | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar(share.index, share.to_numpy(), width=0.8, color=DATA_COLOR, edgecolor="white", lw=0.5,
           label="data")
    if uniform is not None:
        ax.axhline(uniform, color=INK, ls="--", lw=1.2, label=f"uniform = {uniform:.3f}")
    if benford is not None:
        ax.plot(benford.index, benford.to_numpy(), color=BENFORD_COLOR, marker="o", ms=5, lw=2,
                label="Benford log10(1 + 1/d)")
    if uniform is not None or benford is not None:
        ax.set_ylim(top=max(share.max(), 0.0 if benford is None else benford.max()) * 1.3)
        ax.legend(loc="upper right", ncol=3)  # headroom + one row keeps the legend off the bars
    ax.set(title=title, xlabel=xlabel, ylabel="share of actors")
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", dpi=160)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)
    raw = pd.read_csv(DATA_PATH, header=None, names=["dob"], dtype=str)["dob"]
    birth = parse_birth_dates(raw)
    print(f"rows = {len(raw)}, unparseable/placeholder = {birth.isna().sum()}")
    print(f"birth years: min = {birth.dt.year.min():.0f}, max = {birth.dt.year.max():.0f}")

    raw_age = (REFERENCE_YEAR - birth.dt.year).dropna().astype(int)
    age = compute_ages(birth, REFERENCE_YEAR)
    first = age.astype(str).str[0].astype(int)
    last = age % 10
    print(f"ages kept (1-100) = {len(age)}, mean = {age.mean():.2f}, median = {age.median():.0f}, "
          f"min = {age.min()}, max = {age.max()}")
    print(f"dropped by reason: unparseable/placeholder = {birth.isna().sum()}, "
          f"age < 1 = {int((raw_age < 1).sum())}, age > 100 = {int((raw_age > 100).sum())}")

    print("boundary counts: "
          f"age in [1, 10] = {int(((age >= 1) & (age <= 10)).sum())}, "
          f"age == 100 = {int((age == 100).sum())}, "
          f"age > 100 = {int((raw_age > 100).sum())}, "
          f"age < 1 = {int((raw_age < 1).sum())}")

    first_share = share_per_value(first, range(1, 10))
    last_share = share_per_value(last, range(10))
    print("first digit share:", first_share.round(4).to_dict())
    print("last digit share: ", last_share.round(4).to_dict())
    benford = pd.Series({d: float(np.log10(1 + 1 / d)) for d in range(1, 10)})
    print("Benford reference:", benford.round(4).to_dict())
    print(f"max |last share - 0.1| = {(last_share - 0.1).abs().max():.4f}")

    plot_bars(share_per_value(age, range(1, 101)), None,
              f"Age in {REFERENCE_YEAR} (n = {len(age):,})", "age (years)", "p2_1_age")
    plot_bars(first_share, 1 / 9, "First digit of age", "first digit", "p2_2_first_digit",
              benford=benford)
    plot_bars(last_share, 1 / 10, "Last digit of age", "last digit", "p2_3_last_digit")


if __name__ == "__main__":
    main()
