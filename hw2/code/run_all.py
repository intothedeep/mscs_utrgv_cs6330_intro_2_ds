"""
Run every HW2 answer script in report order and print what each one reports.

Run from the repo root:  uv run python hw2/code/run_all.py
"""

import runpy
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
# Report order: airport (a)-(j), movie (a)-(j), then Problem 2 (a)-(d).
SCRIPTS = (sorted(CODE_DIR.glob("p1_airport_*.py")) + sorted(CODE_DIR.glob("p1_movie_*.py"))
           + sorted(CODE_DIR.glob("p2_*.py")))

if __name__ == "__main__":
    for script in SCRIPTS:
        print(f"\n##### {script.name}")
        runpy.run_path(str(script), run_name="__main__")
