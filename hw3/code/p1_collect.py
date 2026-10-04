"""
Step 1 (R: get_stats, get_video_details, get_comment_threads, write.csv).

For each video in common.VIDEOS: fetch statistics and details, then up to MAX_COMMENTS
top-level comments. Writes hw3/data/videos.csv (one row per video) and
hw3/data/comments_<label>.csv, and prints the first rows, the R script's View().

Run: uv run python hw3/code/p1_collect.py
"""

import pandas as pd
from common import COMMENT_ORDER, DATA_DIR, MAX_COMMENTS, VIDEOS, api_get, load_api_key

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
    }


def fetch_comments(video_id: str, key: str) -> pd.DataFrame:
    """Top-level comments, 100 per page, until MAX_COMMENTS or the last page."""
    rows: list[dict[str, str | int]] = []
    params: dict[str, str | int] = {
        "part": "snippet", "videoId": video_id, "maxResults": 100,
        "order": COMMENT_ORDER, "textFormat": "plainText",
    }
    while len(rows) < MAX_COMMENTS:
        page = api_get("commentThreads", params, key)
        for item in page["items"]:
            top = item["snippet"]["topLevelComment"]["snippet"]
            rows.append({
                "author": top.get("authorDisplayName", ""),
                "published_at": top["publishedAt"],
                "like_count": top.get("likeCount", 0),
                "reply_count": item["snippet"].get("totalReplyCount", 0),
                "text_original": top["textOriginal"],
            })
        if "nextPageToken" not in page:
            break
        params["pageToken"] = page["nextPageToken"]
    return pd.DataFrame(rows[:MAX_COMMENTS])


if __name__ == "__main__":
    if not all(VIDEOS.values()):
        raise SystemExit("Fill in both video IDs in common.VIDEOS first.")
    key = load_api_key()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    videos = []
    for label, video_id in VIDEOS.items():
        video = {"label": label, **fetch_video(video_id, key)}
        comments = fetch_comments(video_id, key)
        video["comments_collected"] = len(comments)
        comments.to_csv(DATA_DIR / f"comments_{label}.csv", index=False)
        videos.append(video)
        print(f"\n== {label}: {video['title']} ({video['channel']})")
        print(f"views {video['view_count']:,}  likes {video['like_count']:,}  "
              f"comments {video['comment_count']:,}  collected {len(comments):,} "
              f"(top-level, order={COMMENT_ORDER})")
        print(comments.head().to_string(max_colwidth=60))
    pd.DataFrame(videos).to_csv(DATA_DIR / "videos.csv", index=False)
