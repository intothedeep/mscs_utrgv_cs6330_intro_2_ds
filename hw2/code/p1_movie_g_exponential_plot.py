"""Problem 1, Movie Rating data, (g): ... distribution of data if it was exponential

Run from the repo root:  uv run python hw2/code/p1_movie_g_exponential_plot.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "exponential")
