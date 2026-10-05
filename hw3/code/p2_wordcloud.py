"""
Step 2 (R: Corpus, DocumentTermMatrix, colSums, wordcloud).

For each video and each comment version (VERSIONS: English, non-English, mixed), count terms
over the comments (tm-style cleaning, see common.clean_terms), write
hw3/data/terms_<label>_<version>.csv and draw hw3/figures/wordcloud_<label>_<version>.png,
plus one grid hw3/figures/wordcloud_grid.png (rows = videos, columns = versions).

Run: uv run python hw3/code/p2_wordcloud.py   (after p1_collect.py)
"""

from collections import Counter

import matplotlib

matplotlib.use("Agg")  # headless: write PNGs only
import matplotlib.pyplot as plt
import pandas as pd
from common import DATA_DIR, FIG_DIR, INK, SEED, VERSIONS, VIDEOS, count_terms
from wordcloud import WordCloud

# Video titles can hold Hangul (e.g. BTS (방탄소년단)); AppleGothic is the macOS fallback.
plt.rcParams["font.family"] = ["DejaVu Sans", "AppleGothic"]

__all__ = ["load_comments", "make_cloud"]

MAX_WORDS = 150
# The non-English and mixed clouds hold Hangul, kana, Thai and Cyrillic; the wordcloud
# default font draws Latin only. Arabic draws unjoined (no text shaping).
CLOUD_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def load_comments(label: str, version: str) -> list[str]:
    """One video's comment texts for one version, from the file that keeps every language."""
    comments = pd.read_csv(DATA_DIR / f"comments_{label}_all.csv", keep_default_na=False)
    is_english = comments["lang"] == "en"
    keep = {"en": is_english, "non_en": ~is_english, "mixed": is_english | ~is_english}[version]
    return comments.loc[keep, "text_original"].astype(str).tolist()


def make_cloud(counts: Counter[str]) -> WordCloud:
    """Word size proportional to term frequency; fixed seed so the layout is reproducible."""
    return WordCloud(width=1200, height=800, background_color="white", colormap="viridis",
                     max_words=MAX_WORDS, random_state=SEED, font_path=CLOUD_FONT,
                     collocations=False).generate_from_frequencies(counts)


if __name__ == "__main__":
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    titles = pd.read_csv(DATA_DIR / "videos.csv").set_index("label")["title"]
    fig, axes = plt.subplots(len(VIDEOS), len(VERSIONS), figsize=(18, 8))
    for row, label in zip(axes, VIDEOS):
        for ax, (version, name) in zip(row, VERSIONS.items()):
            texts = load_comments(label, version)
            counts = count_terms(texts)
            pd.DataFrame(counts.most_common(), columns=["term", "count"]).to_csv(
                DATA_DIR / f"terms_{label}_{version}.csv", index=False)
            cloud = make_cloud(counts)
            cloud.to_file(str(FIG_DIR / f"wordcloud_{label}_{version}.png"))
            ax.imshow(cloud, interpolation="bilinear")
            ax.set_title(f"{titles[label]}\n{name}, {len(texts):,} comments", color=INK,
                         fontsize=10)
            ax.axis("off")
            print(f"\n== {label} {version}: {len(texts):,} comments, "
                  f"{len(counts):,} distinct terms, top 15:")
            print(", ".join(f"{t} {c}" for t, c in counts.most_common(15)))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "wordcloud_grid.png", dpi=150)
