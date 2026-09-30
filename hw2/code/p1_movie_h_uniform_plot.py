"""Problem 1, Movie Rating data, (h): ... distribution of data if it was uniform

Run from the repo root:  uv run python hw2/code/p1_movie_h_uniform_plot.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "uniform")
