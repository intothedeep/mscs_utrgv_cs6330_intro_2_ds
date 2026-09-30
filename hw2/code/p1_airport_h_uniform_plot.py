"""Problem 1, Airport data, (h): ... distribution of data if it was uniform

Run from the repo root:  uv run python hw2/code/p1_airport_h_uniform_plot.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "uniform")
