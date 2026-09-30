"""Problem 1, Movie Rating data, (d): What is mu and sigma if the distribution is normal?

Run from the repo root:  uv run python hw2/code/p1_movie_d_normal.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.normal_steps(x)
