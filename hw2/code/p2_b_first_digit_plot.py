"""Problem 2, (b): Screenshot of distribution/histogram of the first digit of age

Run from the repo root:  uv run python hw2/code/p2_b_first_digit_plot.py
"""

import common_p2

if __name__ == "__main__":
    share = common_p2.share_per_value(common_p2.first_digits(common_p2.load_ages()), range(1, 10))
    print("first digit share:", share.round(4).to_dict())
    common_p2.plot_bars(share, 1 / 9, "First digit of age", "first digit", "p2_2_first_digit",
                        benford_ref=common_p2.benford())
