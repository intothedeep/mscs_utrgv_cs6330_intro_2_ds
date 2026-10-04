"""
Step 2 (R: Corpus, DocumentTermMatrix, colSums, wordcloud).

For each video: count terms over its collected comments (tm-style cleaning, see
common.clean_terms), write hw3/data/terms_<label>.csv, and draw
hw3/figures/wordcloud_<label>.png plus a side-by-side hw3/figures/wordcloud_both.png.

Run: uv run python hw3/code/p2_wordcloud.py   (after p1_collect.py)
"""

from collections import Counter

import matplotlib

matplotlib.use("Agg")  # headless: write PNGs only
import matplotlib.pyplot as plt
import pandas as pd
from common import DATA_DIR, FIG_DIR, INK, SEED, VIDEOS, count_terms
from wordcloud import WordCloud

__all__ = ["load_counts", "make_cloud"]

MAX_WORDS = 150


def load_counts(label: str) -> Counter[str]:
    """Term counts for one video's saved comments."""
    comments = pd.read_csv(DATA_DIR / f"comments_{label}.csv", keep_default_na=False)
    return count_terms(comments["text_original"].astype(str).tolist())


def make_cloud(counts: Counter[str]) -> WordCloud:
    """Word size proportional to term frequency; fixed seed so the layout is reproducible."""
    return WordCloud(width=1200, height=800, background_color="white", colormap="viridis",
                     max_words=MAX_WORDS, random_state=SEED,
                     collocations=False).generate_from_frequencies(counts)


if __name__ == "__main__":
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    titles = pd.read_csv(DATA_DIR / "videos.csv").set_index("label")["title"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, label in zip(axes, VIDEOS):
        counts = load_counts(label)
        pd.DataFrame(counts.most_common(), columns=["term", "count"]).to_csv(
            DATA_DIR / f"terms_{label}.csv", index=False)
        cloud = make_cloud(counts)
        cloud.to_file(str(FIG_DIR / f"wordcloud_{label}.png"))
        ax.imshow(cloud, interpolation="bilinear")
        ax.set_title(titles[label], color=INK)
        ax.axis("off")
        print(f"\n== {label}: {len(counts):,} distinct terms, top 15:")
        print(", ".join(f"{t} {c}" for t, c in counts.most_common(15)))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "wordcloud_both.png", dpi=150)
