"""
Step 3 (assignment item 3: compare the videos). Prints the numbers the discussion cites:
engagement ratios, comment coverage, and shared vs distinctive top terms.

Run: uv run python hw3/code/p3_compare.py   (after p2_wordcloud.py)
"""

import pandas as pd
from common import DATA_DIR, VIDEOS

__all__ = ["top_terms"]

TOP_N = 30


def top_terms(label: str, n: int = TOP_N) -> list[str]:
    """The n most frequent terms of one video."""
    return pd.read_csv(DATA_DIR / f"terms_{label}.csv", keep_default_na=False)["term"].head(n).tolist()


if __name__ == "__main__":
    videos = pd.read_csv(DATA_DIR / "videos.csv").set_index("label")
    videos["likes_per_1k_views"] = 1000 * videos["like_count"] / videos["view_count"]
    videos["comments_per_1k_views"] = 1000 * videos["comment_count"] / videos["view_count"]
    videos["share_collected"] = videos["comments_collected"] / videos["comment_count"]
    print(videos.drop(columns=["video_id"]).T.to_string())

    label_a, label_b = VIDEOS
    a, b = top_terms(label_a), top_terms(label_b)
    print(f"\nTop {TOP_N} terms in both: {', '.join(t for t in a if t in b)}")
    print(f"Only in {label_a}: {', '.join(t for t in a if t not in b)}")
    print(f"Only in {label_b}: {', '.join(t for t in b if t not in a)}")
