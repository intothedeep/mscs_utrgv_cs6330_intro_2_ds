"""
Run the four HW3 steps in order.

Run from the repo root:  uv run python hw3/code/run_all.py
"""

import runpy
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
SCRIPTS = ("p1_collect.py", "p2_wordcloud.py", "p3_compare.py", "p4_report_tables.py")

if __name__ == "__main__":
    for name in SCRIPTS:
        print(f"\n##### {name}")
        runpy.run_path(str(CODE_DIR / name), run_name="__main__")
