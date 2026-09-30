"""Problem 1, Airport data, (f): ... distribution of data if it was power law

Run from the repo root:  uv run python hw2/code/p1_airport_f_powerlaw_plot.py
"""

import common

DATASET = "airport"

if __name__ == "__main__":
    common.plot_model_figure(DATASET, "powerlaw")
