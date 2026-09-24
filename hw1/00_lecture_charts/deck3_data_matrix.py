"""Deck 3 (Data and Matrix) -> figures on values transcribed from slides.md
(notes_text/3_DataAndMatrix/) and recomputed per arch-deck3.md SS4/SS5.

Every value lives once here, with its slide source noted in a comment; this
script only plots, loads data (sklearn.datasets.load_iris() for values only,
data.load() for the HW1 workbook) and does exact arithmetic. It never fits or
trains anything.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3D projection)
from sklearn.datasets import load_iris
from style import ACCENT, CATEGORICAL, INK, MUTED, save

__all__ = ["build_all"]

# source: slide 8, media/image5.png (Name, Salary, Age); also used for the
# 2D scatter per arch-deck3.md SS5.1 (03_01, slide 10's own concept)
NAMES = ["Jane", "John", "Delilah", "Dave", "Ellen"]
SALARY = np.array([90000, 85000, 75000, 90000, 82000])
AGE = np.array([52, 48, 32, 53, 44])

# source: slide 11, media/image9.png (Salary, Age, Years in service); row
# order matches image5 by (salary, age) pair
SERVICE = np.array([10, 20, 30, 40, 20])

# source: slide 13, media/image11.png (Feature 1, Feature 2)
VEC_X = np.array([20, 30, 28, 40, 35])
VEC_Y = np.array([90000, 85000, 40000, 95000, 42000])

# source: slide 19, media/image21.jpeg, adjacency matrix read row by row
ADJ_NODES = ["A", "B", "C", "D", "E"]
ADJ = np.array([
    [0, 1, 1, 1, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0],
])

# source: slide 14, media/image13.png, the 10 printed rows (sepal length,
# sepal width, petal length, petal width); checked for membership in
# sklearn's load_iris() array (R11), not for matching row index (the slide's
# x1..x8 are not sklearn's row order)
IRIS_SLIDE_ROWS = np.array([
    [5.9, 3.0, 4.2, 1.5],  # x1
    [6.9, 3.1, 4.9, 1.5],  # x2
    [6.6, 2.9, 4.6, 1.3],  # x3
    [4.6, 3.2, 1.4, 0.2],  # x4
    [6.0, 2.2, 4.0, 1.0],  # x5
    [4.7, 3.2, 1.3, 0.2],  # x6
    [6.5, 3.0, 5.8, 2.2],  # x7
    [5.8, 2.7, 5.1, 1.9],  # x8
    [7.7, 3.8, 6.7, 2.2],  # x149
    [5.1, 3.4, 1.5, 0.2],  # x150
])


def _salary_age_2d() -> str:
    """Slide 10 (arch-deck3.md fig:attr-2d-scatter): age vs salary, 5 named
    points; Jane and Dave nearly overlap (both salary 90000), called out with
    an annotation instead of the slide's own unreadable overlap.
    """
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.scatter(AGE, SALARY, color=ACCENT, s=90, zorder=3)
    label_offsets = {"Jane": (8, 12), "Dave": (8, -16)}
    for name, x, y in zip(NAMES, AGE, SALARY):
        xytext = label_offsets.get(name, (8, 6))
        ax.annotate(name, (x, y), textcoords="offset points", xytext=xytext, fontsize=10, color=INK)
    ax.annotate("Jane and Dave nearly overlap\n(same salary, 1 year apart)",
                (52.5, 90000), textcoords="offset points", xytext=(-155, -35), fontsize=9, color=MUTED,
                arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8})
    ax.set_xlabel("age (years)")
    ax.set_ylabel("salary ($)")
    ax.set_ylim(74000, 93000)
    ax.set_title("2-dimensional data: 5 points in the (age, salary) plane (slide 10)", fontsize=12)
    fig.tight_layout()
    return str(save(fig, "03_01_salary_age_2d"))


def _salary_age_service_3d() -> str:
    """Slide 11 (fig:attr-3d-scatter): salary, age, years-in-service, 5
    points, axis ranges set to include every point (fixes C1: the slide's own
    image10 clips Delilah's salary and Delilah/Dave's age).
    """
    fig = plt.figure(figsize=(7.6, 6.2))
    ax = fig.add_subplot(projection="3d")
    ax.scatter(AGE, SALARY, SERVICE, color=ACCENT, s=90, depthshade=False)
    for name, x, y, z in zip(NAMES, AGE, SALARY, SERVICE):
        ax.text(x, y, z, f"  {name}", color=INK, fontsize=9)
    ax.set_xlabel("age (years)")
    ax.set_ylabel("salary ($)")
    ax.set_zlabel("years in service")
    ax.set_xlim(AGE.min() - 3, AGE.max() + 3)
    ax.set_ylim(SALARY.min() - 3000, SALARY.max() + 3000)
    ax.set_zlim(SERVICE.min() - 3, SERVICE.max() + 3)
    ax.set_title("3-dimensional data: array size 5x3, space dimension 3 (slide 11)", fontsize=12)
    fig.tight_layout()

    cells = SALARY.size + AGE.size + SERVICE.size  # R4: 5x3 stored as 3 columns of 5
    print(f"  03_02 R4 cell count = {cells} (arch-deck3.md: 15)")
    print("  03_02 R5 array dimension = 2 (row index, column index), "
          "space dimension = 3 (salary, age, service) (arch-deck3.md: 2, 3)")
    return str(save(fig, "03_02_salary_age_service_3d"))


def _vectors_origin() -> str:
    """Slide 13 (fig:attr-vectors): 5 points as arrows from the origin,
    arrowhead ending exactly at the point (fixes C2: the slide's image12
    overshoots past the point).
    """
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    for x, y in zip(VEC_X, VEC_Y):
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                     arrowprops={"arrowstyle": "-|>", "color": ACCENT, "lw": 1.8,
                                 "shrinkA": 0, "shrinkB": 0})
        ax.scatter([x], [y], color=ACCENT, s=40, zorder=3)
    ax.set_xlim(0, VEC_X.max() * 1.15)
    ax.set_ylim(0, VEC_Y.max() * 1.15)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title("Each row is a vector from the origin to the point (slide 13)", fontsize=12)
    fig.tight_layout()
    return str(save(fig, "03_03_vectors_origin"))


def _iris_points_mean() -> str:
    """Slide 15 (fig:attr-iris-mean): sklearn's load_iris() sepal length vs
    sepal width, 150 points with transparency, mean point and dashed guides.
    Data only, no model fitting.
    """
    iris = load_iris()
    x1 = iris.data[:, 0]  # sepal length
    x2 = iris.data[:, 1]  # sepal width
    mean_x1, mean_x2 = float(x1.mean()), float(x2.mean())

    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    ax.scatter(x1, x2, color=CATEGORICAL[2], s=45, alpha=0.45, edgecolors="none", zorder=2)
    ax.scatter([mean_x1], [mean_x2], color=INK, s=90, zorder=3, label="mean point")
    ax.plot([mean_x1, mean_x1], [x2.min(), mean_x2], color=MUTED, lw=1.0, ls="--", zorder=1)
    ax.plot([x1.min(), mean_x1], [mean_x2, mean_x2], color=MUTED, lw=1.0, ls="--", zorder=1)
    ax.set_xlabel("$X_1$: sepal length")
    ax.set_ylabel("$X_2$: sepal width")
    ax.set_title("Iris dataset as points/vectors, solid point = mean (slide 15)", fontsize=12)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()

    membership = np.array([
        bool(np.any(np.all(np.isclose(iris.data, row, atol=1e-9), axis=1)))
        for row in IRIS_SLIDE_ROWS
    ])
    print(f"  03_04 R11 slide rows found in load_iris(): {int(membership.sum())}/10 "
          "(arch-deck3.md: 10/10 expected)")
    print(f"  03_04 R12 mean point = ({mean_x1:.4f}, {mean_x2:.4f}) "
          "(arch-deck3.md hand calc: 5.843, 3.057)")
    return str(save(fig, "03_04_iris_points_mean"))


def _network_adjacency() -> None:
    """Slide 19 (media/image21.jpeg): print-only check, no figure (the graph
    and matrix diagram itself is TikZ, drawn by T12). Confirms R15-R17.
    """
    symmetric = bool(np.array_equal(ADJ, ADJ.T))
    row_sums = ADJ.sum(axis=1)
    total = int(ADJ.sum())
    print(f"  network R15 shape = {ADJ.shape} (arch-deck3.md: 5x5), symmetric = {symmetric} "
          "(arch-deck3.md: True)")
    print(f"  network R16 self-loop A[D,D] = {ADJ[3, 3]} (arch-deck3.md: 1)")
    print(f"  network R17 row sums = {row_sums.tolist()} (arch-deck3.md: [3, 3, 2, 5, 2]), "
          f"element sum = {total} (arch-deck3.md: 15)")


def _hw1_matrix_and_distances(df: pd.DataFrame) -> None:
    """arch-deck3.md sec:attr-apply: HW1 workbook counted three ways, plus
    the item-column identifier check (R18), plus the SS4.2 distance pair.
    """
    n_rows, n_cols = df.shape
    n_attrs = n_cols - 1  # drop "item" as the identifier column
    numeric_cols = ["serving_size", "calories", "fat", "sodium", "sugars"]
    item_unique = int(df["item"].nunique())
    print(f"  apply R18 df.shape = {df.shape} (arch-deck3.md: 126x8), "
          f"attributes = {n_attrs} (arch-deck3.md: 7), "
          f"numeric D shape = ({n_rows}, {len(numeric_cols)}) (arch-deck3.md: 126x5)")
    print(f"  apply R18 item unique values = {item_unique} (arch-deck3.md hand note: "
          "126 if unique, else 'identifier-like but not unique')")
    if item_unique != n_rows:
        print(f"  apply R18 disagreement: item has {item_unique} unique values over {n_rows} "
              "rows -> identifier-like but not unique, per arch-deck3.md SS4.1 note")

    # SS4.2: slide 10 data (age, salary), Jane-Dave and Jane-John pairs
    age_range = float(AGE.max() - AGE.min())
    salary_range = float(SALARY.max() - SALARY.min())
    pairs = [("Jane-Dave", 0, 3), ("Jane-John", 0, 1)]
    for label, i, j in pairs:
        raw = float(np.sqrt((AGE[i] - AGE[j]) ** 2 + (SALARY[i] - SALARY[j]) ** 2))
        normed = float(np.sqrt(((AGE[i] - AGE[j]) / age_range) ** 2
                                + ((SALARY[i] - SALARY[j]) / salary_range) ** 2))
        print(f"  apply SS4.2 {label}: raw = {raw:.4f}, normalized = {normed:.4f}")


def build_all(df: pd.DataFrame) -> list[str]:
    """Render every deck-3 figure; returns saved paths. Also prints every
    hand-computed value arch-deck3.md asks to confirm, next to its value.
    """
    paths = [_salary_age_2d(), _salary_age_service_3d(), _vectors_origin(), _iris_points_mean()]
    _network_adjacency()
    _hw1_matrix_and_distances(df)
    return paths


if __name__ == "__main__":
    from data import load
    from style import apply_style

    apply_style()
    print("Deck 3 - Data and Matrix")
    build_all(load())
