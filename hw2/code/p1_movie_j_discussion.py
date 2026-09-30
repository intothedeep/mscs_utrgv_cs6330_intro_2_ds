"""Problem 1, Movie Rating data, (j): What is the distribution of data based on your observation? (KS distances)

Run from the repo root:  uv run python hw2/code/p1_movie_j_discussion.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    common.ks_table(DATASET)
