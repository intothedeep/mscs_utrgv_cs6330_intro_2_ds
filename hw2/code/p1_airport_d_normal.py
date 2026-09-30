"""Problem 1, Airport data, (d): What is mu and sigma if the distribution is normal?

Run from the repo root:  uv run python hw2/code/p1_airport_d_normal.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.normal_steps(x)
