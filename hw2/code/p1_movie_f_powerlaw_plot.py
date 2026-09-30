"""Problem 1, Movie Rating data, (f): ... distribution of data if it was power law

Run from the repo root:  uv run python hw2/code/p1_movie_f_powerlaw_plot.py
"""

import common

DATASET = "movie"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "powerlaw")
