"""Problem 1, Airport data, (c): What is [a, b] if the distribution is uniform?

Run from the repo root:  uv run python hw2/code/p1_airport_c_uniform.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.uniform_steps(x)
