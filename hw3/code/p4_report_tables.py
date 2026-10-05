"""
Step 4 (report tables). Reads saved CSVs only (no API, no language detection) and writes
hw3/data/sample_composition.csv plus LaTeX table BODIES in hw3/report/tables/: rows only,
with \\midrule between every row. The report .tex owns the float, caption and column spec.

Tables: stats, sample, first_comments_video_a, first_comments_video_b, engagement,
top_terms_en, top_terms_non_en, top_terms_mixed, shared_terms.
counts.tex holds \\newcommand macros (letters only), one per count a caption or sentence
needs, for each video suffix VideoA / VideoB:
  \\nEn<V> \\nNonEn<V> \\nMixed<V>   comments in the English / non-English / mixed cloud
                                    (\\nEn<V> is also the English comments kept)
  \\nFetched<V>                      top-level comments fetched, all languages
  \\nViews<V> \\nLikes<V> \\nComments<V>   YouTube totals
Cells with non-Latin letters are wrapped as {\\unifont ...}; the .tex defines \\unifont.

Run: uv run python hw3/code/p4_report_tables.py   (after p3_compare.py)
"""

import re
import unicodedata

import pandas as pd
from common import COMMENT_ORDERS, DATA_DIR, HW_DIR, VERSIONS, VIDEOS

__all__ = ["composition", "sanitize_comment", "tex_escape"]

TABLES_DIR = HW_DIR / "report" / "tables"
AS_OF = "2026-10-04"  # owner, 2026-10-05: videos.csv had no fetched_at
N_FIRST = 5
CUT_AT = 120
TOP_SHOWN = 10
KINDS = ("english", "non_english_with_lang", "no_lang")
# Emoji and symbols only. Mn stays: Thai vowels and tone marks are combining marks.
_DROPPED_CATEGORIES = frozenset({"So", "Sk", "Cf", "Cs", "Co", "Cn"})
_LATEX_SPECIAL = re.compile(r"[\\&%$#_{}~^]")
_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    **{c: "\\" + c for c in "&%$#_{}"},
}


# ---------------------------------------------------------------- text cells (pure)

def tex_escape(text: str) -> str:
    """Escape the LaTeX specials in one pass, so the backslash of an escape is never re-escaped."""
    return _LATEX_SPECIAL.sub(lambda m: _LATEX_ESCAPES[m.group()], text)


def _is_non_latin_letter(ch: str) -> bool:
    name = unicodedata.name(ch, "")
    return (ord(ch) > 127 and unicodedata.category(ch)[0] in "LM"
            and not name.startswith(("LATIN", "COMBINING")))


def cell(text: str) -> str:
    """Escaped text cell, wrapped in \\unifont when it holds Hangul, Thai, kana, etc."""
    escaped = tex_escape(text)
    return "{\\unifont " + escaped + "}" if any(map(_is_non_latin_letter, text)) else escaped


def sanitize_comment(text: str, limit: int = CUT_AT) -> str:
    """Comment text for a table cell, not yet escaped: one line, @mentions masked, emoji and
    symbols stripped, cut to about `limit` characters. Cut before escaping so an escape
    sequence such as \\& is never split."""
    text = " ".join(text.split())
    text = re.sub(r"@\S+", "@user", text)
    text = "".join(c for c in text if unicodedata.category(c) not in _DROPPED_CATEGORIES)
    text = " ".join(text.split())
    return text[:limit].rstrip() + "..." if len(text) > limit else text


def body(rows: list[list[str]]) -> str:
    """Table body: one line per row, \\midrule between rows (the .tex adds the rules around)."""
    return "\n\\midrule\n".join(" & ".join(row) + " \\\\" for row in rows) + "\n"


def video_name(label: str) -> str:
    return label.replace("_", " ").title()


def count(n: float) -> str:
    return f"{int(n):,}"


def read(name: str) -> pd.DataFrame:
    """A saved CSV; keep_default_na=False so lang == "" stays an empty string, not NaN."""
    return pd.read_csv(DATA_DIR / name, keep_default_na=False)


# ---------------------------------------------------------------- sample composition

def composition(comments: pd.DataFrame) -> pd.DataFrame:
    """Comments per order (plus a total row) split into English / other language / no language."""
    kind = comments["lang"].map(
        lambda lang: "english" if lang == "en" else "no_lang" if lang == "" else
        "non_english_with_lang")
    table = pd.crosstab(comments["order"], kind).reindex(
        index=list(COMMENT_ORDERS), columns=list(KINDS), fill_value=0)
    table.loc["total"] = table.sum()
    table["total"] = table.sum(axis=1)
    return table.rename_axis("order").reset_index()


# ---------------------------------------------------------------- table builders

def stats_rows(videos: pd.DataFrame) -> list[list[str]]:
    """T2, transposed: one row per measure, one column per video."""
    v = videos.set_index("label").loc[list(VIDEOS)]
    as_of = v["fetched_at"].str[:10] if "fetched_at" in v else pd.Series(AS_OF, index=v.index)
    spec = [
        ("Title", v["title"].map(cell)), ("Channel", v["channel"].map(cell)),
        ("Video ID", v["video_id"].map(cell)), ("Published", v["published_at"].str[:10]),
        ("Views", v["view_count"].map(count)), ("Likes", v["like_count"].map(count)),
        ("Comments (YouTube total)", v["comment_count"].map(count)),
        ("Comments fetched", v["comments_fetched"].map(count)),
        ("English comments kept", v["comments_collected"].map(count)),
        ("As of", as_of),
    ]
    return [[name, *col.tolist()] for name, col in spec]


def sample_rows(comp: pd.DataFrame) -> list[list[str]]:
    return [[video_name(r.label), r.order, *(count(getattr(r, k)) for k in (*KINDS, "total"))]
            for r in comp.itertuples()]


def first_comment_rows(comments: pd.DataFrame) -> list[list[str]]:
    """T4: first rows in fetch order; author and comment_id are never read."""
    rows = []
    for i, r in enumerate(comments.head(N_FIRST).itertuples(), start=1):
        rows.append([str(i), r.order, r.published_at[:10], count(r.like_count),
                     count(r.reply_count), r.lang or "none",
                     cell(sanitize_comment(r.text_original))])
    return rows


def engagement_rows(compare: pd.DataFrame) -> list[list[str]]:
    c = compare.set_index("label").loc[list(VIDEOS)]
    # Four decimals: the shares are about 0.01 to 0.1 percent.
    spec = [("Likes per 1k views", "likes_per_1k_views", "{:.2f}"),
            ("Comments per 1k views", "comments_per_1k_views", "{:.2f}"),
            ("Share fetched (of YouTube total)", "share_fetched", "{:.4%}"),
            ("Share English (of YouTube total)", "share_english", "{:.4%}")]
    return [[name, *(fmt.format(x).replace("%", r"\%") for x in c[col])] for name, col, fmt in spec]


def top_term_rows(version: str) -> list[list[str]]:
    a, b = (read(f"terms_{label}_{version}.csv").head(TOP_SHOWN) for label in VIDEOS)
    return [[str(i), cell(ta), count(ca), cell(tb), count(cb)]
            for i, (ta, ca, tb, cb) in enumerate(
                zip(a["term"], a["count"], b["term"], b["count"], strict=True), start=1)]


def shared_rows(terms: pd.DataFrame) -> list[list[str]]:
    return [[cell(VERSIONS[r.version]), cell(r.in_both), cell(r.only_a), cell(r.only_b)]
            for r in terms.itertuples()]


def count_macros(videos: pd.DataFrame, comps: dict[str, pd.DataFrame]) -> str:
    """\\newcommand lines; the macro name is the count's name plus VideoA / VideoB."""
    v = videos.set_index("label")
    lines = []
    for label in VIDEOS:
        total = comps[label].set_index("order").loc["total"]
        suffix = label.replace("_", " ").title().replace(" ", "")
        counts = {
            "nEn": total["english"], "nNonEn": total["total"] - total["english"],
            "nMixed": total["total"], "nFetched": v.loc[label, "comments_fetched"],
            "nViews": v.loc[label, "view_count"], "nLikes": v.loc[label, "like_count"],
            "nComments": v.loc[label, "comment_count"],
        }
        lines += [f"\\newcommand{{\\{name}{suffix}}}{{{count(n)}}}" for name, n in counts.items()]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    videos, compare, compare_terms = read("videos.csv"), read("compare_videos.csv"), read(
        "compare_terms.csv")
    all_comments = {label: read(f"comments_{label}_all.csv") for label in VIDEOS}
    comps = {label: composition(df) for label, df in all_comments.items()}
    pd.concat([c.assign(label=label) for label, c in comps.items()])[
        ["label", "order", *KINDS, "total"]].to_csv(DATA_DIR / "sample_composition.csv", index=False)

    tables = {
        "stats": stats_rows(videos),
        "sample": sample_rows(pd.concat([c.assign(label=label) for label, c in comps.items()])),
        "engagement": engagement_rows(compare),
        "shared_terms": shared_rows(compare_terms),
        **{f"first_comments_{label}": first_comment_rows(df) for label, df in all_comments.items()},
        **{f"top_terms_{version}": top_term_rows(version) for version in VERSIONS},
    }
    for name, rows in tables.items():
        (TABLES_DIR / f"{name}.tex").write_text(body(rows), encoding="utf-8")
    (TABLES_DIR / "counts.tex").write_text(count_macros(videos, comps), encoding="utf-8")
    print(f"wrote {len(tables) + 1} files to {TABLES_DIR} and sample_composition.csv")
