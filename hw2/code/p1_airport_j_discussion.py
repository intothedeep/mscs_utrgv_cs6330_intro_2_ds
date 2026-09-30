"""Problem 1, Airport data, (j): What is the distribution of data based on your observation? (KS distances)

Run from the repo root:  uv run python hw2/code/p1_airport_j_discussion.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    common.ks_table(DATASET)
