"""
Shared code for HW3 (YouTube comments). The professor's R script (00_doc/
Homework_YoutubeVideo_1__1_.R) uses tuber + tm + wordcloud; this module does the same steps in
Python: YouTube Data API v3 over plain REST, tm-style term cleaning, and the plot style.

Steps:   p1_collect.py   stats, details, comments  -> hw3/data/
         p2_wordcloud.py term counts, word clouds  -> hw3/data/, hw3/figures/
         p3_compare.py   side-by-side numbers for the discussion
Run all: uv run python hw3/code/run_all.py

The API key is read from hw3/.env (YOUTUBE_DATA_API_KEY=...), which .gitignore excludes.
Reading public comments needs only an API key, not OAuth.
"""

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from lingua import Language, LanguageDetectorBuilder

__all__ = [
    "COMMENT_ORDERS",
    "DATA_DIR",
    "FIG_DIR",
    "GRID",
    "HW_DIR",
    "INK",
    "MAX_COMMENTS",
    "MAX_PAGES",
    "SEED",
    "VIDEOS",
    "api_get",
    "clean_terms",
    "count_terms",
    "detect_language",
    "load_api_key",
]

HW_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HW_DIR / "data"
FIG_DIR = HW_DIR / "figures"
SEED = 20701313  # owner's student ID, same as hw2

# Two videos to compare, label -> video ID (the string after watch?v=).
# TODO(owner): pick the pair; verify each with p1_collect.py (commentCount > 0 and a
# successful first comment page) and note the date here: "verified via videos.list on ____".
VIDEOS: dict[str, str] = {
    "video_a": "gdZLi9oWNZg",  # owner's pick, 2026-10-03 (search "bts")
    "video_b": "2S24-y0Ij3Y",  # owner's pick, 2026-10-04 (search "blackpink"), replaces Bad Bunny
}

# commentThreads.list returns top-level comments only (as tuber's get_comment_threads does),
# 100 per page, 1 quota unit per page. MAX_COMMENTS counts English comments only (tm's
# stopwords are English, so other languages would flood the cloud with their function words).
# MAX_PAGES caps a run at 50 units per video when few comments are English.
MAX_COMMENTS = 1000
MAX_PAGES = 50
# Relevance paging ends after ~1,100-1,250 comments (~600 English), so collection then
# continues newest-first until MAX_COMMENTS English (owner, 2026-10-04). Each row keeps its order.
COMMENT_ORDERS = ("relevance", "time")

INK = "#52514e"
GRID = "#e4e3df"

API_ROOT = "https://www.googleapis.com/youtube/v3/"
RETRIES = 3

# tm::stopwords("english"), the list DocumentTermMatrix(stopwords=TRUE) removes.
TM_STOPWORDS = frozenset(
    [
        "i",
        "me",
        "my",
        "myself",
        "we",
        "our",
        "ours",
        "ourselves",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
        "he",
        "him",
        "his",
        "himself",
        "she",
        "her",
        "hers",
        "herself",
        "it",
        "its",
        "itself",
        "they",
        "them",
        "their",
        "theirs",
        "themselves",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "having",
        "do",
        "does",
        "did",
        "doing",
        "would",
        "should",
        "could",
        "ought",
        "i'm",
        "you're",
        "he's",
        "she's",
        "it's",
        "we're",
        "they're",
        "i've",
        "you've",
        "we've",
        "they've",
        "i'd",
        "you'd",
        "he'd",
        "she'd",
        "we'd",
        "they'd",
        "i'll",
        "you'll",
        "he'll",
        "she'll",
        "we'll",
        "they'll",
        "isn't",
        "aren't",
        "wasn't",
        "weren't",
        "hasn't",
        "haven't",
        "hadn't",
        "doesn't",
        "don't",
        "didn't",
        "won't",
        "wouldn't",
        "shan't",
        "shouldn't",
        "can't",
        "cannot",
        "couldn't",
        "mustn't",
        "let's",
        "that's",
        "who's",
        "what's",
        "here's",
        "there's",
        "when's",
        "where's",
        "why's",
        "how's",
        "a",
        "an",
        "the",
        "and",
        "but",
        "if",
        "or",
        "because",
        "as",
        "until",
        "while",
        "of",
        "at",
        "by",
        "for",
        "with",
        "about",
        "against",
        "between",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "to",
        "from",
        "up",
        "down",
        "in",
        "out",
        "on",
        "off",
        "over",
        "under",
        "again",
        "further",
        "then",
        "once",
        "here",
        "there",
        "when",
        "where",
        "why",
        "how",
        "all",
        "any",
        "both",
        "each",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
    ]
)

MIN_WORD_LENGTH = 3  # tm's default wordLengths = c(3, Inf)


def load_api_key() -> str:
    """YOUTUBE_DATA_API_KEY from the environment, else from hw3/.env. Never printed."""
    key = os.environ.get("YOUTUBE_DATA_API_KEY", "")
    env_file = HW_DIR / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "YOUTUBE_DATA_API_KEY":
                key = value.strip().strip('"').strip("'")
    if not key:
        raise SystemExit("No API key: put YOUTUBE_DATA_API_KEY=... in hw3/.env (see the HW3 notes).")
    return key


def api_get(resource: str, params: dict[str, str | int], key: str) -> dict:
    """GET one YouTube Data API v3 resource. Fails fast with the API's own error reason,
    after RETRIES tries for the API's transient errors (processingFailure, HTTP 5xx)."""
    query = urllib.parse.urlencode({**params, "key": key})
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(f"{API_ROOT}{resource}?{query}", timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            body = json.loads(err.read() or b"{}").get("error", {})
            reasons = [e.get("reason", "") for e in body.get("errors", [])]
            is_transient = err.code >= 500 or "processingFailure" in reasons
            if is_transient and attempt < RETRIES:
                time.sleep(2 * attempt)
                continue
            # The key is in the URL, so report the reason only, never the request.
            raise SystemExit(f"{resource}: HTTP {err.code} {reasons} {body.get('message', '')}")
    raise AssertionError("unreachable")


# ---------------------------------------------------------------- language detection

_URL_OR_MENTION = re.compile(r"https?://\S+|@\S+")
# Candidate languages for K-pop comment sections. With all 75 languages, short English
# comments ("2026 anyone?", "Lets go") were labelled Sotho or Tswana (first run, 2026-10-04).
LANGUAGES = (
    Language.ENGLISH, Language.SPANISH, Language.PORTUGUESE, Language.FRENCH,
    Language.GERMAN, Language.ITALIAN, Language.INDONESIAN, Language.MALAY,
    Language.TAGALOG, Language.VIETNAMESE, Language.THAI, Language.TURKISH,
    Language.RUSSIAN, Language.ARABIC, Language.HINDI, Language.KOREAN,
    Language.JAPANESE, Language.CHINESE, Language.POLISH, Language.DUTCH,
)
_detector = None  # built on first use, so importing common stays cheap for p2/p3


def detect_language(text: str) -> str:
    """ISO 639-1 code of one comment's language, or "" when there are no words to judge
    (emoji-only, links only). URLs and @mentions are removed first: they are not language."""
    global _detector
    if _detector is None:
        _detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()
    language = _detector.detect_language_of(_URL_OR_MENTION.sub(" ", text))
    return language.iso_code_639_1.name.lower() if language else ""


# ---------------------------------------------------------------- term cleaning (pure)

# Keep letters of any script, apostrophes and spaces. This drops punctuation and numbers
# (as tm does) and emoji, which tm keeps but no word cloud font draws. Non-Latin words stay
# (as in tm) so the non-English and mixed clouds have them.
_NON_WORD = re.compile(r"(?:[^\w' ]|[\d_])+")


def clean_terms(text: str) -> list[str]:
    """One comment -> its terms: lowercase, strip punctuation/numbers/emoji, drop
    English stopwords, then words shorter than 3 letters. No stemming (the R script loads
    SnowballC but never calls it)."""
    words = _NON_WORD.sub(" ", text.lower().replace("’", "'")).split()
    words = [w.strip("'") for w in words if w.strip("'") not in TM_STOPWORDS]
    return [w.replace("'", "") for w in words if len(w.replace("'", "")) >= MIN_WORD_LENGTH]


def count_terms(texts: list[str]) -> Counter[str]:
    """Column sums of the document-term matrix, i.e. total count of each term."""
    counts: Counter[str] = Counter()
    for text in texts:
        counts.update(clean_terms(text))
    return counts
