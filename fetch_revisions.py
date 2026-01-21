import requests
import pandas as pd
from datetime import datetime, timedelta, UTC
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


API_URL = "https://deadlock.wiki/api.php"

def fetch_recent_revisions(days=7, limit=500):
    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()

    params = {
        "action": "query",
        "format": "json",
        "list": "recentchanges",
        "rcprop": "title|timestamp",
        "rclimit": limit,
        "rcstart": since,
        "rcdir": "newer"
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    records = [
        {
            "page": rc["title"],
            "timestamp": rc["timestamp"]
        }
        for rc in data["query"]["recentchanges"]
    ]

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = fetch_recent_revisions(days=7)
    df.to_csv(OUTPUT_DIR / "revisions_raw.csv", index=False)