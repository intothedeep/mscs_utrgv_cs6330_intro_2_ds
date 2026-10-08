"""
Raw YouTube Data API responses, one JSON file per call, to show what the API returns.

p1_collect keeps only selected fields in CSV. This script repeats each kind of p1 call once per
video and saves the response unchanged: videos (details and statistics), and commentThreads
for each order in COMMENT_ORDERS. Comment calls ask for SAMPLE_SIZE threads, not p1's 100.
Writes hw3/data/api_responses/<label>_<call>.json and index.json (request of each file,
without the key, and the fetch time). Numbers are as of the fetch time, not p1's run.

Run: uv run python hw3/code/p5_api_samples.py
"""

import json
from datetime import UTC, datetime

from common import COMMENT_ORDERS, DATA_DIR, VIDEOS, api_get, load_api_key

__all__ = ["SAMPLE_SIZE"]

SAMPLE_SIZE = 3  # enough to show the structure; the file stays readable
OUT_DIR = DATA_DIR / "api_responses"

if __name__ == "__main__":
    key = load_api_key()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    calls: list[tuple[str, str, dict[str, str | int]]] = []
    for label, video_id in VIDEOS.items():
        calls.append((f"{label}_videos", "videos", {"part": "snippet,statistics", "id": video_id}))
        for order in COMMENT_ORDERS:
            calls.append((f"{label}_commentThreads_{order}", "commentThreads", {
                "part": "snippet", "videoId": video_id, "maxResults": SAMPLE_SIZE,
                "order": order, "textFormat": "plainText"}))
    index = []
    for name, resource, params in calls:
        response = api_get(resource, params, key)
        (OUT_DIR / f"{name}.json").write_text(json.dumps(response, ensure_ascii=False, indent=2))
        index.append({"file": f"{name}.json", "resource": resource, "params": params,
                      "fetched_at": datetime.now(UTC).isoformat(timespec="seconds")})
        print(f"{name}.json: {len(response.get('items', []))} items")
    (OUT_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2))
