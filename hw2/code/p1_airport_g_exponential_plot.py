"""Problem 1, Airport data, (g): ... distribution of data if it was exponential

Run from the repo root:  uv run python hw2/code/p1_airport_g_exponential_plot.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "exponential")
