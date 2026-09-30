"""Problem 1, Movie Rating data, (i): ... distribution of data if it was normal

Run from the repo root:  uv run python hw2/code/p1_movie_i_normal_plot.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "normal")
