"""Problem 2, (d): Discussion (what are those distribution?) Why do you think it is like this?

Run from the repo root:  uv run python hw2/code/p2_d_discussion.py
"""

import common_p2

if __name__ == "__main__":
    age = common_p2.load_ages()
    first = common_p2.share_per_value(common_p2.first_digits(age), range(1, 10))
    last = common_p2.share_per_value(common_p2.last_digits(age), range(10))
    print("first digit share:", first.round(4).to_dict())
    print("last digit share: ", last.round(4).to_dict())
    print(f"max |last share - 0.1| = {(last - 0.1).abs().max():.4f}")
    print(f"boundary counts: age in [1, 19] = {int(((age >= 1) & (age <= 19)).sum())}, "
          f"age in [20, 29] = {int(((age >= 20) & (age <= 29)).sum())}")
