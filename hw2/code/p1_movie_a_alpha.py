"""Problem 1, Movie Rating data, (a): What is the alpha if the distribution is power law?

Run from the repo root:  uv run python hw2/code/p1_movie_a_alpha.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    x = common.load(DATASET)
    common.print_header(DATASET, x)
    common.power_law_steps(x)
