from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "output" / "revisions_raw.csv"
OUTPUT_FILE = BASE_DIR / "output" / "top_editors.csv"

df = pd.read_csv(INPUT_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Filter window
last_30 = df[df["timestamp"] >= pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=30)]

# Only edits (not page creation)
edits = last_30[last_30["type"] == "edit"]

result = (
    edits.groupby("user")
         .agg(
             total_edits=("page", "count"),
             unique_pages=("page", "nunique")
         )
         .sort_values("total_edits", ascending=False)
)

result.to_csv(OUTPUT_FILE)
print(result.head(10))
