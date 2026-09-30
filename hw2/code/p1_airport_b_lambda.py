"""Problem 1, Airport data, (b): What is the lambda if the distribution is exponential?

Run from the repo root:  uv run python hw2/code/p1_airport_b_lambda.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.exponential_steps(x)
