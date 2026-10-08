"""
Run the three HW4 steps in order.

Run from the repo root:  uv run python hw4/code/run_all.py
"""

import runpy
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
SCRIPTS = ("p1_association.py", "p2_correlation.py", "p3_report_tables.py")

if __name__ == "__main__":
    sys.path.insert(0, str(CODE_DIR))
    for name in SCRIPTS:
        print(f"\n##### {name}")
        runpy.run_path(str(CODE_DIR / name), run_name="__main__")
