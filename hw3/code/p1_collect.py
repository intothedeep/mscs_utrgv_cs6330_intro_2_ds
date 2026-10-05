"""
Step 1 (R: get_stats, get_video_details, get_comment_threads, write.csv).

For each video in common.VIDEOS: fetch statistics and details, then top-level comments
page by page, by relevance and then newest first (COMMENT_ORDERS), until MAX_COMMENTS of
them are English or MAX_PAGES pages are used.
Writes hw3/data/videos.csv (one row per video, with a fetched_at timestamp), hw3/data/comments_<label>_all.csv (every
fetched comment with its detected language) and hw3/data/comments_<label>.csv (English
only, the input of p2), and prints the first rows, the R script's View().

Run: uv run python hw3/code/p1_collect.py
"""

from datetime import UTC, datetime

import pandas as pd
from common import (
    COMMENT_ORDERS,
    DATA_DIR,
    MAX_COMMENTS,
    MAX_PAGES,
    VIDEOS,
    api_get,
    detect_language,
    load_api_key,
)

__all__ = ["fetch_comments", "fetch_video"]


def fetch_video(video_id: str, key: str) -> dict[str, str | int]:
    """Details (title, channel, date) and statistics (views, likes, comments) of one video."""
    items = api_get("videos", {"part": "snippet,statistics", "id": video_id}, key)["items"]
    if not items:
        raise SystemExit(f"{video_id}: no such public video")
    snippet, stats = items[0]["snippet"], items[0]["statistics"]
    return {
        "video_id": video_id,
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "published_at": snippet["publishedAt"],
        "view_count": int(stats.get("viewCount", 0)),
        "like_count": int(stats.get("likeCount", 0)),
        # Missing when comments are turned off; the assignment needs them open.
        "comment_count": int(stats.get("commentCount", 0)),
        # Stats change daily, so the report needs the read date (UTC, ISO 8601).
        "fetched_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def fetch_comments(video_id: str, key: str) -> pd.DataFrame:
    """Top-level comments with `order` and `lang` columns, 100 per page, through each of
    COMMENT_ORDERS in turn until MAX_COMMENTS English comments or MAX_PAGES pages in total.
    A comment seen under an earlier order is skipped (same comment ID). Rows after the
    MAX_COMMENTS-th English one are not kept."""
    rows: list[dict[str, str | int]] = []
    seen: set[str] = set()
    n_english = n_pages = 0
    for order in COMMENT_ORDERS:
        params: dict[str, str | int] = {
            "part": "snippet", "videoId": video_id, "maxResults": 100,
            "order": order, "textFormat": "plainText",
        }
        while n_pages < MAX_PAGES:
            page = api_get("commentThreads", params, key)
            n_pages += 1
            for item in page["items"]:
                if item["id"] in seen:
                    continue
                seen.add(item["id"])
                top = item["snippet"]["topLevelComment"]["snippet"]
                lang = detect_language(top["textOriginal"])
                n_english += lang == "en"
                rows.append({
                    "comment_id": item["id"],
                    "order": order,
                    "author": top.get("authorDisplayName", ""),
                    "published_at": top["publishedAt"],
                    "like_count": top.get("likeCount", 0),
                    "reply_count": item["snippet"].get("totalReplyCount", 0),
                    "lang": lang,
                    "text_original": top["textOriginal"],
                })
                if n_english == MAX_COMMENTS:
                    return pd.DataFrame(rows)
            if "nextPageToken" not in page:
                break
            params["pageToken"] = page["nextPageToken"]
    return pd.DataFrame(rows)


if __name__ == "__main__":
    if not all(VIDEOS.values()):
        raise SystemExit("Fill in both video IDs in common.VIDEOS first.")
    key = load_api_key()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    videos = []
    for label, video_id in VIDEOS.items():
        video = {"label": label, **fetch_video(video_id, key)}
        fetched = fetch_comments(video_id, key)
        comments = fetched[fetched["lang"] == "en"]
        video["comments_fetched"] = len(fetched)
        video["comments_collected"] = len(comments)
        fetched.to_csv(DATA_DIR / f"comments_{label}_all.csv", index=False)
        comments.to_csv(DATA_DIR / f"comments_{label}.csv", index=False)
        videos.append(video)
        print(f"\n== {label}: {video['title']} ({video['channel']})")
        print(f"views {video['view_count']:,}  likes {video['like_count']:,}  "
              f"comments {video['comment_count']:,}  fetched {len(fetched):,}  "
              f"English {len(comments):,} (top-level)")
        print("English by order:", comments["order"].value_counts().to_dict())
        print("languages:", fetched["lang"].replace("", "none").value_counts().head(8).to_dict())
        print(comments.head().to_string(max_colwidth=60))
    pd.DataFrame(videos).to_csv(DATA_DIR / "videos.csv", index=False)
