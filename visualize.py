import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(OUTPUT_DIR / "top_topics_last_7_days.csv")

# keep only top 10 topics
df = df.sort_values("edit_count", ascending=False).head(10)

plt.figure(figsize=(10, 5))
plt.barh(df["topic"], df["edit_count"])
plt.xlabel("Number of Edits")
plt.title("Top 10 Most Edited Wiki Topics (Last 7 Days)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "edits_trend.png")
plt.show()