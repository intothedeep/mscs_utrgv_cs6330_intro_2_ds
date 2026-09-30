"""Problem 2, (c): Screenshot of distribution/histogram of the last digit of age

Run from the repo root:  uv run python hw2/code/p2_c_last_digit_plot.py
"""

import common_p2

if __name__ == "__main__":
    share = common_p2.share_per_value(common_p2.last_digits(common_p2.load_ages()), range(10))
    print("last digit share:", share.round(4).to_dict())
    common_p2.plot_bars(share, 1 / 10, "Last digit of age", "last digit", "p2_3_last_digit")
