"""Problem 1, Movie Rating data, (c): What is [a, b] if the distribution is uniform?

Run from the repo root:  uv run python hw2/code/p1_movie_c_uniform.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.uniform_steps(x)
