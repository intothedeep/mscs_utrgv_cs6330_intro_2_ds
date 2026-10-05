"""
Step 3 (assignment item 3: compare the videos). Prints the numbers the discussion cites
(engagement ratios, comment coverage, shared vs distinctive top terms) and saves them:
hw3/data/compare_videos.csv (one row per video) and hw3/data/compare_terms.csv (one row per
comment version, terms joined by ", "). p4_report_tables.py reads these files.

Run: uv run python hw3/code/p3_compare.py   (after p2_wordcloud.py)
"""

import pandas as pd
from common import DATA_DIR, VERSIONS, VIDEOS

__all__ = ["top_terms"]

TOP_N = 30


def top_terms(label: str, version: str, n: int = TOP_N) -> list[str]:
    """The n most frequent terms of one video in one comment version."""
    terms = pd.read_csv(DATA_DIR / f"terms_{label}_{version}.csv", keep_default_na=False)
    return terms["term"].head(n).tolist()


if __name__ == "__main__":
    videos = pd.read_csv(DATA_DIR / "videos.csv").set_index("label")
    videos["likes_per_1k_views"] = 1000 * videos["like_count"] / videos["view_count"]
    videos["comments_per_1k_views"] = 1000 * videos["comment_count"] / videos["view_count"]
    # Two shares: everything fetched (all languages) and the English part the clouds use.
    videos["share_fetched"] = videos["comments_fetched"] / videos["comment_count"]
    videos["share_english"] = videos["comments_collected"] / videos["comment_count"]
    print(videos.drop(columns=["video_id"]).T.to_string())
    videos[["likes_per_1k_views", "comments_per_1k_views", "share_fetched", "share_english"]
           ].to_csv(DATA_DIR / "compare_videos.csv")

    label_a, label_b = VIDEOS
    rows = []
    for version, name in VERSIONS.items():
        a, b = top_terms(label_a, version), top_terms(label_b, version)
        both = [t for t in a if t in b]
        only_a = [t for t in a if t not in b]
        only_b = [t for t in b if t not in a]
        rows.append({"version": version, "in_both": ", ".join(both),
                     "only_a": ", ".join(only_a), "only_b": ", ".join(only_b)})
        print(f"\n## {name}")
        print(f"Top {TOP_N} terms in both: {', '.join(both)}")
        print(f"Only in {label_a}: {', '.join(only_a)}")
        print(f"Only in {label_b}: {', '.join(only_b)}")
    pd.DataFrame(rows).to_csv(DATA_DIR / "compare_terms.csv", index=False)
