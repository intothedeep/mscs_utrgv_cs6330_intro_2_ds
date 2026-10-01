"""Problem 2, (b): Screenshot of distribution/histogram of the first digit of age

Run from the repo root:  uv run python hw2/code/p2_b_first_digit_plot.py
"""

import common_p2

if __name__ == "__main__":
    digits = common_p2.first_digits(common_p2.load_ages())
    share = common_p2.share_per_value(digits, range(1, 10))
    normal = common_p2.normal_ref(digits, range(1, 10))
    print("first digit share:", share.round(4).to_dict())
    print(normal[1], normal[0].round(4).to_dict())
    common_p2.plot_bars(share, 1 / 9, "First digit of age", "first digit", "p2_2_first_digit",
                        normal=normal,
                        n=len(digits), values=digits,
                        show_spread=True, legend_on_top=True, show_mode=True)
