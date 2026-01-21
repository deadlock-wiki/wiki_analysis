import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(OUTPUT_DIR / "revisions_raw.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

df["topic"] = df["page"].str.split("/").str[:2].str.join("/")

EXCLUDED_PREFIXES = (
    "User:",
    "Module:",
    "Template:",
    "File:",
    "Category:",
    "MediaWiki:"
)

df = df[~df["topic"].str.startswith(EXCLUDED_PREFIXES)]
df = df[~df["topic"].str.contains("Sandbox", case=False)]
df = df[~df["topic"].str.fullmatch("Movement|Death")]

page_activity = (
    df.groupby("topic")
      .size()
      .reset_index(name="edit_count")
      .sort_values("edit_count", ascending=False)
)

page_activity.to_csv(OUTPUT_DIR / "top_topics_last_7_days.csv", index=False)

page_activity.head(10).to_json(
    OUTPUT_DIR / "trending_topics.json",
    orient="records"
)
print(page_activity.head(10))