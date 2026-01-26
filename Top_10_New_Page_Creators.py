from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "output" / "revisions_raw.csv"
OUTPUT_FILE = BASE_DIR / "output" / "top_new_page_creators.csv"

df = pd.read_csv(INPUT_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Filter window
last_30 = df[df["timestamp"] >= pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=30)]

# Only page creations
new_pages = last_30[last_30["type"] == "new"]

result = (
    new_pages.groupby("user")
             .agg(pages_created=("page", "nunique"))
             .sort_values("pages_created", ascending=False)
)

result.to_csv(OUTPUT_FILE)
print(result.head(10))
