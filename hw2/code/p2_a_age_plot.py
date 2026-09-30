"""Problem 2, (a): Screenshot of distribution/histogram of the age

Run from the repo root:  uv run python hw2/code/p2_a_age_plot.py
"""

import common_p2

if __name__ == "__main__":
    birth = common_p2.load_birth_dates()
    raw_age = common_p2.raw_ages(birth)
    age = common_p2.compute_ages(birth, common_p2.REFERENCE_YEAR)
    print(f"rows = {len(birth)}, unparseable/placeholder = {birth.isna().sum()}")
    print(f"birth years: min = {birth.dt.year.min():.0f}, max = {birth.dt.year.max():.0f}")
    print(f"ages kept (1-100) = {len(age)}, mean = {age.mean():.2f}, "
          f"median = {age.median():.0f}, min = {age.min()}, max = {age.max()}")
    print(f"dropped: age < 1 = {int((raw_age < 1).sum())}, age > 100 = {int((raw_age > 100).sum())}")
    common_p2.plot_age_filter(raw_age, "p2_0_age_all")
    common_p2.plot_bars(common_p2.share_per_value(age, range(1, 101)), None,
                        f"Age in {common_p2.REFERENCE_YEAR} (n = {len(age):,})", "age (years)",
                        "p2_1_age")
