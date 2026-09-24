"""Deck 7 (Q-Q Plot and Normalization) -> transcribed slide constants and the
exact-arithmetic helpers that check them, per architecture.md SS8.4/8.5/8.7.

Every value lives once here, with its slide source noted in a comment. No
plotting; deck7_qq_normalization.py does the figures.
"""

from collections import Counter

import numpy as np

__all__ = [
    "AGE", "E1_DATA", "E3_A", "E3_B", "E4_A", "E4_B", "INCOME",
    "IRIS_TENTH_COUNTS", "QNORM_MATRIX", "check_iris_transcription",
    "qq_positions", "quantile_normalize",
]

# source: media/image46.png (slide 18), transcribed row by row
AGE = np.array([12., 14, 18, 23, 27, 28, 34, 37, 39, 40])
INCOME = np.array([300., 500, 1000, 2000, 3500, 4000, 4300, 6000, 2500, 2700])

# source: media/image64.png (slide 20). Columns = samples, rows = genes
# ("sort each column", R24).
QNORM_MATRIX = np.array([
    [1., 5, 3, 5],
    [2., 1, 6, 7],
    [3., 2, 2, 6],
    [4., 6, 1, 8],
])

# source: architecture.md SS8.7(b), the standard Fisher-iris sepal-length
# value counts (tenths of cm -> count, 35 distinct values, sum 150). Used only
# to cross-check the scikit-learn copy (Q13); never plotted directly.
IRIS_TENTH_COUNTS: dict[int, int] = {
    43: 1, 44: 3, 45: 1, 46: 4, 47: 2, 48: 5, 49: 6, 50: 10, 51: 9,
    52: 4, 53: 1, 54: 6, 55: 7, 56: 6, 57: 8, 58: 7,
    59: 3, 60: 6, 61: 6, 62: 4, 63: 9, 64: 7,
    65: 5, 66: 2, 67: 8, 68: 3, 69: 4, 70: 1, 71: 1, 72: 3, 73: 1,
    74: 1, 76: 1, 77: 4, 79: 1,
}

# Book's own worked examples (not on the slides), architecture.md SS8.5.
E1_DATA = np.array([3., 4, 5, 6, 12])  # ex:qq-by-hand
E3_A = np.array([2., 3, 3.5, 4, 4.5, 5, 5, 5.5, 6, 6, 6.5, 7, 8, 9, 11])  # ex:qq-two-samples, n=15
E3_B = np.array([4., 5.5, 7, 9.5])  # n=4
E4_A = np.array([5., 2, 3])  # ex:qq-quantile-norm tie example
E4_B = np.array([4., 4, 1])


def qq_positions(n: int) -> np.ndarray:
    """Slide 6 plotting position p_i = i/(n+1) (R10). NOT scipy.stats.probplot's
    rule. Shared by deck7_qq_normalization.py and deck7_transforms.py (I4: was
    duplicated in both).
    """
    return np.arange(1, n + 1) / (n + 1)


def check_iris_transcription(sklearn_sepal_length: np.ndarray) -> int:
    """Compare scikit-learn's sepal length (rounded to tenths) against the
    slide-15 derived table (SS8.7). Returns the multiset mismatch count.
    """
    tenths = np.rint(sklearn_sepal_length * 10).astype(int)
    mine = Counter(tenths.tolist())
    slide = Counter(IRIS_TENTH_COUNTS)
    diff = mine - slide
    diff_back = slide - mine
    mismatches = sum(diff.values()) + sum(diff_back.values())
    print(f"  iris transcription check: n = {tenths.size}, sum table = {sum(slide.values())}, "
          f"mismatches = {mismatches}, sklearn-extra = {dict(diff)}, table-extra = {dict(diff_back)}")
    return mismatches


def quantile_normalize(matrix: np.ndarray) -> np.ndarray:
    """Slide 20 (R24): sort each column, average each row across columns,
    then unsort back into the original column order. Ties (any group size)
    get the mean of the reference values (row_means) at every rank position
    the tied group occupies (book's rule (ii), E4). E.g. a 3-way tie
    occupying ranks 1, 2, 3 gets mean(row_means[1], row_means[2],
    row_means[3]), not just the value at the mean rank.
    """
    n_cols = matrix.shape[1]
    order = np.argsort(matrix, axis=0)
    sorted_matrix = np.take_along_axis(matrix, order, axis=0)
    row_means = sorted_matrix.mean(axis=1)

    result = np.empty_like(matrix)
    for col in range(n_cols):
        col_vals = matrix[:, col]
        for value in np.unique(col_vals):
            idx = np.flatnonzero(col_vals == value)
            positions = np.flatnonzero(np.isin(order[:, col], idx))
            result[idx, col] = row_means[positions].mean()
    return result
