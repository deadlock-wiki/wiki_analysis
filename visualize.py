import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output/top_topics_last_7_days.csv")

# keep only top 10 topics
df = df.sort_values("edit_count", ascending=False).head(10)

plt.figure(figsize=(10, 5))
plt.barh(df["topic"], df["edit_count"])
plt.xlabel("Number of Edits")
plt.title("Top 10 Most Edited Wiki Topics (Last 7 Days)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/edits_trend.png")
plt.show()