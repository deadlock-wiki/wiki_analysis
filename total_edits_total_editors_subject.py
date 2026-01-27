from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "output" / "revisions_raw.csv"
OUTPUT_FILE = BASE_DIR / "output" / "editors_by_subject.csv"

# =========================
# Load data
# =========================
df = pd.read_csv(INPUT_FILE)

# =========================
# Prompt user
# =========================
subject = input("Enter subject / keyword to search for: ").strip()

if not subject:
    raise ValueError("Subject cannot be empty")

# =========================
# Filters (ALL TIME)
# =========================
# Only edits
df = df[df["type"] == "edit"]

# Subject match (case-insensitive)
pattern = re.escape(subject)
df = df[df["page"].astype(str).str.contains(pattern, case=False, regex=True)]

# =========================
# All editors (no ranking)
# =========================
editors = (
    df.groupby("user")
      .size()
      .reset_index(name="edit_count")
)

# =========================
# Total edits (all users)
# =========================
total_edits = len(df)

# =========================
# Output
# =========================
editors.to_csv(OUTPUT_FILE, index=False)

print(f"\nAll editors who edited subject '{subject}' (all time):")
print(editors.head(20))
print(f"\nTotal editors: {len(editors)} | Total edits: {total_edits}")